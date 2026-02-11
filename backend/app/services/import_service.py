"""导入服务"""
import json
import logging
import re
from typing import Optional, Dict, Any, List
from uuid import UUID
from datetime import datetime
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.models.work import Work, WorkGenre, WorkStatus
from app.models.chapter import Chapter, ChapterStatus
from app.models.character import Character
from app.models.location import Location
from app.models.setting import Setting
from app.models.work_guidelines import WorkGuidelines
from app.models.ai_guidelines import AIGuidelines
from app.utils.chapter_file_storage import chapter_storage
from app.services.chapter_content_index_service import ChapterContentIndexService
from app.schemas.export import (
    ImportOptions,
    ImportPreviewResponse,
    ImportPreviewWork,
    ImportPreviewChapter,
    ImportResponse
)

logger = logging.getLogger(__name__)


class ImportService:
    """导入服务类"""
    
    def __init__(self, db: AsyncSession):
        self.db = db
    
    async def preview_import(
        self,
        content: bytes,
        format: str
    ) -> ImportPreviewResponse:
        """预览导入数据
        
        解析文件并返回将要导入的数据概览
        """
        try:
            if format == "json":
                return await self._preview_json(content)
            elif format in ["markdown", "txt"]:
                return await self._preview_text(content, format)
            else:
                raise ValueError(f"不支持的导入格式: {format}")
        except json.JSONDecodeError as e:
            logger.error(f"JSON解析失败: {e}")
            raise ValueError("JSON格式错误，请检查文件格式")
        except Exception as e:
            logger.error(f"预览导入数据失败: {e}", exc_info=True)
            raise ValueError(f"文件解析失败: {str(e)}")
    
    async def import_work(
        self,
        content: bytes,
        user_id: UUID,
        options: ImportOptions
    ) -> tuple[ImportResponse, list[Dict[str, Any]], Dict[str, Any]]:
        """导入作品

        Returns:
            (ImportResponse, List[Dict], Dict): 导入结果、需异步向量化的章节任务、导入上下文
        """
        try:
            if options.format == "json":
                if options.work_id:
                    raise ValueError("JSON 导入暂不支持追加到已有作品")
                return await self._import_json(content, user_id, options)
            elif options.format in ["markdown", "txt"]:
                # 安全校验：创建新作品时不允许传 work_id，避免误追加
                if options.create_new and options.work_id:
                    raise ValueError("create_new=true 时不能传 work_id，如需追加导入请设置 create_new=false")
                if not options.create_new and not options.work_id:
                    raise ValueError("缺少目标作品，无法追加导入")
                return await self._import_text(content, user_id, options, append_to=options.work_id if not options.create_new else None)
            else:
                raise ValueError(f"不支持的导入格式: {options.format}")
        except Exception as e:
            logger.error(f"导入作品失败: {e}", exc_info=True)
            try:
                await self.db.rollback()
            except Exception as rollback_error:
                logger.error(f"回滚失败: {rollback_error}", exc_info=True)
            raise
    
    async def _preview_json(self, content: bytes) -> ImportPreviewResponse:
        """预览JSON格式"""
        data = json.loads(content.decode('utf-8'))
        
        # 验证数据结构
        if 'work' not in data:
            raise ValueError("缺少作品信息")
        
        work_data = data['work']
        chapters_data = data.get('chapters', [])
        worldview_data = data.get('worldview', {})
        
        # 构建章节预览并补全缺失的字数
        preview_chapters = []
        computed_total_words = 0
        for idx, c in enumerate(chapters_data):
            content_text = c.get('content', '')
            word_count = c.get('word_count') or self._calculate_word_count(content_text)
            computed_total_words += word_count
            preview_chapters.append(
                ImportPreviewChapter(
                    title=c['title'],
                    word_count=word_count,
                    order=c.get('order', idx + 1)
                )
            )
        
        total_words = work_data.get('total_words', 0) or computed_total_words
        
        # 构建预览信息
        preview_work = ImportPreviewWork(
            title=work_data['title'],
            description=work_data.get('description'),
            genre=work_data.get('genre'),
            total_words=total_words,
            total_chapters=len(chapters_data)
        )
        
        # 统计世界观数据
        characters_count = len(worldview_data.get('characters', []))
        locations_count = len(worldview_data.get('locations', []))
        settings_count = len(worldview_data.get('settings', []))
        
        # 检查警告信息
        warnings = []
        if len(chapters_data) == 0:
            warnings.append("未检测到章节数据")
        if len(preview_work.title) > 200:
            warnings.append("作品标题过长（超过200字符）")
        
        return ImportPreviewResponse(
            work=preview_work,
            chapters=preview_chapters,
            characters_count=characters_count,
            locations_count=locations_count,
            settings_count=settings_count,
            warnings=warnings
        )
    
    async def _preview_text(
        self,
        content: bytes,
        format: str
    ) -> ImportPreviewResponse:
        """预览文本/Markdown格式"""
        text = self._smart_decode(content)

        # 智能提取元信息（标题、简介）
        metadata = self._extract_metadata(text)
        title = metadata['title']
        description = metadata['description']

        # 智能章节分割
        chapters = self._split_chapters(text)

        # 计算总字数
        total_words = self._calculate_word_count(text)

        preview_work = ImportPreviewWork(
            title=title,
            description=description,  # 使用提取的简介
            genre=None,
            total_words=total_words,
            total_chapters=len(chapters)
        )
        
        preview_chapters = [
            ImportPreviewChapter(
                title=c['title'],
                word_count=self._calculate_word_count(c['content']),
                order=idx + 1
            )
            for idx, c in enumerate(chapters)
        ]
        
        warnings = []
        if not chapters:
            warnings.append("未检测到章节，将作为单章导入")
        if len(title) > 200:
            warnings.append("作品标题过长（超过200字符）")
        
        return ImportPreviewResponse(
            work=preview_work,
            chapters=preview_chapters,
            warnings=warnings
        )
    
    async def _import_json(
        self,
        content: bytes,
        user_id: UUID,
        options: ImportOptions
    ) -> tuple[ImportResponse, list[Dict[str, Any]], Dict[str, Any]]:
        """导入JSON格式"""
        logger.info(f"用户 {user_id} 开始导入JSON数据")
        
        data = json.loads(content.decode('utf-8'))
        
        work_data = data['work']
        chapters_data = data.get('chapters', [])
        worldview_data = data.get('worldview', {})
        guidelines_data = data.get('guidelines', {})
        
        # 创建作品
        work = Work(
            author_id=user_id,
            title=work_data['title'],
            description=work_data.get('description'),
            genre=WorkGenre(work_data.get('genre', 'other')),
            status=WorkStatus(work_data.get('status', 'draft')),
            total_words=0,  # 后续重新计算
            total_chapters=0
        )
        self.db.add(work)
        await self.db.flush()
        
        # 导入章节
        chapters_created = 0
        total_words = 0  # 累计总字数
        created_chapters: List[Chapter] = []
        created_contents: List[str] = []
        for idx, chapter_data in enumerate(chapters_data):
            is_published = chapter_data.get('is_published', False)
            raw_status = chapter_data.get('status')
            status = ChapterStatus(raw_status) if raw_status else (ChapterStatus.PUBLISHED if is_published else ChapterStatus.DRAFT)

            content_text = chapter_data.get('content', '')
            word_count = chapter_data.get('word_count') or self._calculate_word_count(content_text)
            total_words += word_count  # 累计字数

            chapter = Chapter(
                work_id=work.id,
                title=chapter_data['title'],
                content="",
                summary=chapter_data.get('summary'),
                order=chapter_data.get('order', idx + 1),
                word_count=word_count,
                status=status,
                is_published=is_published
            )
            self.db.add(chapter)
            chapters_created += 1
            created_chapters.append(chapter)
            created_contents.append(content_text)
        
        # 导入世界观
        characters_created = 0
        locations_created = 0
        settings_created = 0
        
        if options.include_worldview and worldview_data:
            # 导入人物
            for char_data in worldview_data.get('characters', []):
                character = Character(
                    work_id=work.id,
                    name=char_data['name'],
                    role=char_data.get('role'),
                    description=char_data['description'],
                    tags=char_data.get('tags', []),
                    relationships=char_data.get('relationships', [])
                )
                self.db.add(character)
                characters_created += 1
            
            # 导入地点
            for loc_data in worldview_data.get('locations', []):
                location = Location(
                    work_id=work.id,
                    name=loc_data['name'],
                    type=loc_data.get('type'),
                    description=loc_data['description'],
                    tags=loc_data.get('tags', []),
                    related_locations=loc_data.get('related_locations', [])
                )
                self.db.add(location)
                locations_created += 1
            
            # 导入设定
            for setting_data in worldview_data.get('settings', []):
                setting = Setting(
                    work_id=work.id,
                    title=setting_data['title'],
                    category=setting_data.get('category'),
                    content=setting_data.get('content'),
                    tags=setting_data.get('tags', [])
                )
                self.db.add(setting)
                settings_created += 1
        
        # 导入规范
        if options.include_guidelines and guidelines_data:
            # 导入AI规范
            if 'ai_guidelines' in guidelines_data and guidelines_data['ai_guidelines']:
                ag_data = guidelines_data['ai_guidelines']
                ai_guidelines = AIGuidelines(
                    work_id=work.id,
                    business_goal=ag_data.get('business_goal'),
                    target_audience=ag_data.get('target_audience'),
                    commercial_benchmark=ag_data.get('commercial_benchmark'),
                    high_concept=ag_data.get('high_concept'),
                    core_paradox=ag_data.get('core_paradox'),
                    dominant_emotion=ag_data.get('dominant_emotion'),
                    core_ip_symbols=ag_data.get('core_ip_symbols'),
                    protagonist_arc=ag_data.get('protagonist_arc'),
                    core_conflict=ag_data.get('core_conflict'),
                    narrative_rhythm=ag_data.get('narrative_rhythm'),
                    writing_style=ag_data.get('writing_style'),
                    style_notes=ag_data.get('style_notes'),
                    chapter_length=ag_data.get('chapter_length'),
                    content_taboos=ag_data.get('content_taboos'),
                    primary_genre=ag_data.get('primary_genre'),
                    secondary_tags=ag_data.get('secondary_tags'),
                    creative_tone=ag_data.get('creative_tone'),
                    world_intro=ag_data.get('world_intro'),
                    main_locations=ag_data.get('main_locations'),
                    world_rules=ag_data.get('world_rules'),
                    power_system_name=ag_data.get('power_system_name'),
                    power_levels=ag_data.get('power_levels'),
                    power_cost=ag_data.get('power_cost'),
                    protagonist_name=ag_data.get('protagonist_name'),
                    protagonist_identity=ag_data.get('protagonist_identity'),
                    protagonist_traits=ag_data.get('protagonist_traits'),
                    protagonist_goal=ag_data.get('protagonist_goal'),
                    conflict_design=ag_data.get('conflict_design'),
                    act_one=ag_data.get('act_one'),
                    act_two=ag_data.get('act_two'),
                    act_three=ag_data.get('act_three')
                )
                self.db.add(ai_guidelines)
        
        # 更新作品统计
        work.total_chapters = chapters_created
        work.total_words = total_words  # 使用累计的字数，避免查询数据库

        # 2025-12-15: 先 flush 确保所有章节都获得了数据库生成的 ID
        await self.db.flush()

        # 为导入的章节记录delta（在同一事务中）
        from app.services.chapter_word_stat_service import ChapterWordStatService
        stat_service = ChapterWordStatService(self.db)
        for chapter in created_chapters:
            # 2025-12-15: 增加 chapter.id 的有效性检查
            if chapter.id and chapter.word_count and chapter.word_count > 0:
                try:
                    # 使用auto_commit=False，在同一事务中提交
                    await stat_service.add_delta(chapter.id, chapter.word_count, auto_commit=False)
                except Exception as e:
                    logger.warning(f"Failed to record delta for imported chapter {chapter.id}: {e}")

        await self.db.commit()

        index_service = ChapterContentIndexService(self.db)
        index_updated = False
        for chapter, content in zip(created_chapters, created_contents):
            try:
                chapter_storage.write_content(
                    str(chapter.work_id), str(chapter.id), content
                )
                await index_service.upsert_from_content(
                    str(chapter.work_id), str(chapter.id), content, commit=False
                )
                index_updated = True
            except Exception as exc:
                await self.db.rollback()
                logger.warning(f"[ImportService] 写入章节文件或索引失败: {chapter.id} error={exc}")
        if index_updated:
            try:
                await self.db.commit()
                try:
                    from app.services.chapter_vector_service import invalidate_vector_fresh_cache
                    invalidate_vector_fresh_cache(str(work.id))
                except Exception as exc:
                    logger.warning(f"[ImportService] 向量新鲜度缓存失效失败: {exc}")
            except Exception as exc:
                await self.db.rollback()
                logger.warning(f"[ImportService] 提交索引失败: {exc}")
        try:
            from app.services.agent.utils.explore_cache import invalidate_explore_result_cache
            await invalidate_explore_result_cache(str(work.id))
        except Exception as exc:
            logger.warning(f"[ImportService] Explore 结果缓存失效失败: {exc}")

        # 汇总需异步向量化的章节
        vectorize_jobs: list[Dict[str, Any]] = []
        for chapter, content in zip(created_chapters, created_contents):
            if content and len(content.strip()) > 100:
                vectorize_jobs.append(
                    {
                        "work_id": str(work.id),
                        "chapter_id": str(chapter.id),
                        "chapter_order": chapter.order,
                        "chapter_title": chapter.title,
                        "content": content,
                    }
                )

        # 异步插入 LightRAG（不阻塞导入流程）
        await self._insert_chapters_to_lightrag(created_chapters, created_contents)

        logger.info(f"导入完成: 作品ID={work.id}, 章节={chapters_created}, 人物={characters_created}")

        import_context = self._build_import_context(created_chapters)
        
        return (
            ImportResponse(
                work_id=work.id,
                chapters_created=chapters_created,
                characters_created=characters_created,
                locations_created=locations_created,
                settings_created=settings_created,
                message="导入成功",
                import_context=import_context
            ),
            vectorize_jobs,
            import_context
        )
    
    async def _import_text(
        self,
        content: bytes,
        user_id: UUID,
        options: ImportOptions,
        append_to: Optional[str] = None
    ) -> tuple[ImportResponse, list[Dict[str, Any]], Dict[str, Any]]:
        """导入文本/Markdown格式"""
        logger.info(f"用户 {user_id} 开始导入文本数据")

        text = self._smart_decode(content)

        # 智能提取元信息（标题、简介）
        metadata = self._extract_metadata(text)
        title = metadata['title']
        description = metadata['description']

        # 解析前言/设定段落（仅用于世界观解析）
        preface_text = self._extract_preface_for_scan(text)

        # 分割章节
        chapters = self._split_chapters(text)
        if not chapters:
            # 未检测到章节时，整个文本作为单章导入，也需要转换为HTML格式
            html_content = self._convert_text_to_html(text.strip())
            chapters = [{'title': title, 'content': html_content}]
        
        work: Work
        starting_order = 0
        total_words = 0

        if append_to:
            work_id = UUID(str(append_to)) if not isinstance(append_to, UUID) else append_to
            work = await self.db.get(Work, work_id)
            if not work:
                raise ValueError("目标作品不存在，无法导入")
            if str(work.author_id) != str(user_id):
                raise ValueError("无权导入到该作品")
            starting_order = work.total_chapters or 0
            total_words = work.total_words or 0
        else:
            work = Work(
                author_id=user_id,
                title=title,
                description=description,  # 使用提取的简介
                genre=WorkGenre.OTHER,
                status=WorkStatus.DRAFT,
                total_words=0,
                total_chapters=0
            )
            self.db.add(work)
            await self.db.flush()
        
        # 导入章节
        chapters_created = 0
        created_chapters: List[Chapter] = []
        created_contents: List[str] = []
        for idx, chapter_data in enumerate(chapters):
            content_text = chapter_data['content']
            word_count = self._calculate_word_count(content_text)
            total_words += word_count

            chapter = Chapter(
                work_id=work.id,
                title=chapter_data['title'],
                content=content_text,  # HTML格式，已通过 _convert_text_to_html 转换
                order=starting_order + idx + 1,
                word_count=word_count,
                status=ChapterStatus.DRAFT,
                is_published=False
            )
            self.db.add(chapter)
            chapters_created += 1
            created_chapters.append(chapter)
            created_contents.append(content_text)

        # 更新作品统计
        work.total_chapters = (work.total_chapters or 0) + chapters_created
        work.total_words = total_words

        # 2025-12-15: 先 flush 确保所有章节都获得了数据库生成的 ID
        await self.db.flush()

        # 为导入的章节记录delta（在同一事务中）
        from app.services.chapter_word_stat_service import ChapterWordStatService
        stat_service = ChapterWordStatService(self.db)
        for chapter in created_chapters:
            # 2025-12-15: 增加 chapter.id 的有效性检查
            if chapter.id and chapter.word_count and chapter.word_count > 0:
                try:
                    await stat_service.add_delta(chapter.id, chapter.word_count, auto_commit=False)
                except Exception as e:
                    logger.warning(f"Failed to record delta for imported chapter {chapter.id}: {e}")

        await self.db.commit()

        index_service = ChapterContentIndexService(self.db)
        index_updated = False
        for chapter, content in zip(created_chapters, created_contents):
            try:
                chapter_storage.write_content(
                    str(chapter.work_id), str(chapter.id), content
                )
                await index_service.upsert_from_content(
                    str(chapter.work_id), str(chapter.id), content, commit=False
                )
                index_updated = True
            except Exception as exc:
                await self.db.rollback()
                logger.warning(f"[ImportService] 写入章节文件或索引失败: {chapter.id} error={exc}")
        if index_updated:
            try:
                await self.db.commit()
                try:
                    from app.services.chapter_vector_service import invalidate_vector_fresh_cache
                    invalidate_vector_fresh_cache(str(work.id))
                except Exception as exc:
                    logger.warning(f"[ImportService] 向量新鲜度缓存失效失败: {exc}")
            except Exception as exc:
                await self.db.rollback()
                logger.warning(f"[ImportService] 提交索引失败: {exc}")
        try:
            from app.services.agent.utils.explore_cache import invalidate_explore_result_cache
            await invalidate_explore_result_cache(str(work.id))
        except Exception as exc:
            logger.warning(f"[ImportService] Explore 结果缓存失效失败: {exc}")

        # 汇总需异步向量化的章节
        vectorize_jobs: list[Dict[str, Any]] = []
        for chapter, content in zip(created_chapters, created_contents):
            if content and len(content.strip()) > 100:
                vectorize_jobs.append(
                    {
                        "work_id": str(work.id),
                        "chapter_id": str(chapter.id),
                        "chapter_order": chapter.order,
                        "chapter_title": chapter.title,
                        "content": content,
                    }
                )

        # 异步插入 LightRAG（不阻塞导入流程）
        await self._insert_chapters_to_lightrag(created_chapters, created_contents)

        logger.info(f"文本导入完成: 作品ID={work.id}, 章节={chapters_created}")

        import_context = self._build_import_context(created_chapters, preface_text=preface_text)
        
        return (
            ImportResponse(
                work_id=work.id,
                chapters_created=chapters_created,
                message="导入成功",
                import_context=import_context
            ),
            vectorize_jobs,
            import_context
        )

    def _smart_decode(self, content: bytes) -> str:
        """智能解码，支持 UTF-8、GBK、GB18030 等常见中文编码"""
        encodings = ['utf-8', 'gbk', 'gb18030']
        for encoding in encodings:
            try:
                return content.decode(encoding)
            except (UnicodeDecodeError, LookupError):
                continue
        raise ValueError("无法识别文件编码，请将文件转换为 UTF-8 编码后重试")

    def _calculate_word_count(self, content: str) -> int:
        """统一的字数计算逻辑"""
        return len(content.replace('\n', '').replace(' ', ''))

    def _extract_title(self, text: str) -> str:
        """从文本中提取标题（保留向后兼容）"""
        metadata = self._extract_metadata(text)
        return metadata['title']

    def _extract_metadata(self, text: str) -> Dict[str, Any]:
        """智能提取作品元信息（标题、简介）

        解析逻辑：
        1. 第一个非空行作为作品名称
        2. 识别 "简介：" / "简介:" / "内容简介：" 等后的内容作为简介
        3. 遇到第一个章节标题时停止元信息提取

        Returns:
            Dict with keys: title, description, content_start_line
        """
        lines = text.strip().split('\n')

        title = "未命名作品"
        description = None
        content_start_line = 0

        # 章节标题正则（用于判断元信息区域结束）
        chapter_patterns = [
            r'^【第[零一二三四五六七八九十百千万\d]+[章回节]',
            r'^第[零一二三四五六七八九十百千万\d]+[章回节]',
            r'^Chapter\s+\d+',
            r'^##\s+',
        ]

        # 简介标识正则
        intro_pattern = r'^(简介|内容简介|作品简介|摘要)[\s：:]*$'
        intro_inline_pattern = r'^(简介|内容简介|作品简介|摘要)[\s：:]+(.+)$'

        in_intro = False
        intro_lines = []

        for idx, line in enumerate(lines):
            stripped = line.strip()

            # 跳过空行（在找到标题之前）
            if not stripped:
                if in_intro:
                    # 简介中的空行，继续收集
                    continue
                continue

            # 检查是否遇到章节标题
            is_chapter = False
            for pattern in chapter_patterns:
                if re.match(pattern, stripped):
                    is_chapter = True
                    break

            if is_chapter:
                content_start_line = idx
                break

            # 提取标题（第一个非空行，且不是简介标识）
            if title == "未命名作品":
                # 检查是否是Markdown标题
                if stripped.startswith('# '):
                    title = stripped[2:].strip()[:200]
                # 检查不是简介开头
                elif not re.match(intro_pattern, stripped) and not re.match(intro_inline_pattern, stripped):
                    title = stripped[:200]
                continue

            # 检查简介标识（独立行）
            if re.match(intro_pattern, stripped):
                in_intro = True
                continue

            # 检查简介标识（同行带内容）
            inline_match = re.match(intro_inline_pattern, stripped)
            if inline_match:
                intro_lines.append(inline_match.group(2).strip())
                in_intro = True
                continue

            # 收集简介内容
            if in_intro:
                intro_lines.append(stripped)

        # 组装简介
        if intro_lines:
            description = '\n'.join(intro_lines).strip()
            # 限制简介长度
            if len(description) > 2000:
                description = description[:2000] + '...'

        return {
            'title': title,
            'description': description,
            'content_start_line': content_start_line
        }

    def _extract_preface_for_scan(self, text: str) -> str:
        """提取章节标题之前的前言/设定内容（用于世界观解析）"""
        if not text:
            return ""

        lines = text.split('\n')

        # 章节标题正则
        chapter_patterns = [
            r'^【第[零一二三四五六七八九十百千万\d]+[章回节]',
            r'^第[零一二三四五六七八九十百千万\d]+[章回节]',
            r'^Chapter\s+\d+',
            r'^##\s+',
        ]
        compiled_patterns = [re.compile(p, re.IGNORECASE) for p in chapter_patterns]

        chapter_index = None
        for idx, line in enumerate(lines):
            stripped = line.strip()
            if not stripped:
                continue
            if any(p.match(stripped) for p in compiled_patterns):
                chapter_index = idx
                break

        if chapter_index is None:
            return ""

        preface_lines = lines[:chapter_index]
        metadata = self._extract_metadata(text)
        title = (metadata.get('title') or '').strip()

        intro_pattern = r'^(简介|内容简介|作品简介|摘要)[\s：:]*$'
        intro_inline_pattern = r'^(简介|内容简介|作品简介|摘要)[\s：:]+(.+)$'

        cleaned = []
        for line in preface_lines:
            stripped = line.strip()
            if not stripped:
                continue
            if title and (stripped == title or stripped == f'# {title}'):
                continue
            if re.match(intro_pattern, stripped):
                continue
            inline_match = re.match(intro_inline_pattern, stripped)
            if inline_match:
                cleaned.append(inline_match.group(2).strip())
                continue
            cleaned.append(stripped)

        return '\n'.join(cleaned).strip()

    async def _insert_chapters_to_lightrag(
        self,
        chapters: List[Chapter],
        contents: List[str],
    ) -> None:
        """将导入的章节异步插入 LightRAG，file_source=chapter_{chapter_id}。"""
        try:
            from app.services.agent.retrieval.fact_retrieval_gateway import get_gateway
            gateway = get_gateway()
        except Exception as exc:
            logger.warning("[ImportService] LightRAG gateway 初始化失败: %s", exc)
            return

        for chapter, content in zip(chapters, contents):
            if not content or len(content.strip()) < 100:
                continue
            try:
                file_source = f"chapter_{chapter.id}"
                await gateway.insert_document(
                    text=content,
                    file_source=file_source,
                )
            except Exception as exc:
                logger.warning(
                    "[ImportService] LightRAG 插入失败: chapter_id=%s error=%s",
                    chapter.id, exc,
                )

    def _build_import_context(self, chapters: List[Chapter], preface_text: Optional[str] = None) -> Dict[str, Any]:
        """构建导入上下文（用于世界观解析）"""
        if not chapters:
            return {
                "chapter_ids": [],
                "chapter_order_start": None,
                "chapter_order_end": None,
                "preface_text": preface_text
            }

        orders = [c.order for c in chapters if c.order is not None]
        return {
            "chapter_ids": [str(c.id) for c in chapters if c.id],
            "chapter_order_start": min(orders) if orders else None,
            "chapter_order_end": max(orders) if orders else None,
            "preface_text": preface_text
        }
    
    def _split_chapters(self, text: str) -> List[Dict[str, str]]:
        """智能分割章节

        识别模式（按优先级排序）：
        1. 【第X章 标题】 / 【第X章】 - 方括号包裹格式
        2. 第X章 标题 / 第X章：标题 / 第X章 - 标准中文格式
        3. 第X回 / 第X节 - 回目/节格式
        4. Chapter X Title - 英文格式
        5. ## 标题 - Markdown格式

        支持中文数字（零一二三...百千万）和阿拉伯数字
        """
        chapters = []

        # 章节匹配模式（编译正则提高性能）
        chapter_patterns = [
            # 模式1: 【第X章/回/节 标题】 或 【第X章/回/节】
            (r'^【(第[零一二三四五六七八九十百千万\d]+[章回节][^\】]*)】\s*(.*)$', 'bracket'),
            # 模式2: 第X章/回/节 后跟空格、冒号、顿号或直接标题
            (r'^(第[零一二三四五六七八九十百千万\d]+[章回节])[\s：:、]+(.+)$', 'chinese_with_title'),
            # 模式3: 第X章/回/节 单独一行
            (r'^(第[零一二三四五六七八九十百千万\d]+[章回节])\s*$', 'chinese_only'),
            # 模式4: Chapter X 后跟标题（可选）
            (r'^(Chapter\s+\d+)[\s：:]*(.*)$', 'english'),
            # 模式5: Markdown二级标题
            (r'^##\s+(.+)$', 'markdown'),
        ]

        # 编译正则
        compiled_patterns = [(re.compile(p, re.IGNORECASE if t == 'english' else 0), t) for p, t in chapter_patterns]

        lines = text.split('\n')
        current_chapter = None
        current_content = []

        # 跳过元信息区域（标题、简介等）
        metadata = self._extract_metadata(text)
        start_line = metadata.get('content_start_line', 0)

        for idx, line in enumerate(lines):
            stripped = line.strip()

            # 检查是否匹配章节标题
            chapter_title = None
            for pattern, pattern_type in compiled_patterns:
                match = pattern.match(stripped)
                if match:
                    if pattern_type == 'bracket':
                        # 【第X章 标题】格式，group(1)是完整标题
                        chapter_title = match.group(1).strip()
                        # 如果】后还有内容，可能是副标题
                        suffix = match.group(2).strip() if match.group(2) else ''
                        if suffix:
                            chapter_title = f"{chapter_title} {suffix}"
                    elif pattern_type == 'chinese_with_title':
                        # 第X章 标题 格式
                        chapter_num = match.group(1)
                        title_part = match.group(2).strip()
                        chapter_title = f"{chapter_num} {title_part}"
                    elif pattern_type == 'chinese_only':
                        # 第X章 单独格式
                        chapter_title = match.group(1)
                    elif pattern_type == 'english':
                        # Chapter X 格式
                        chapter_num = match.group(1)
                        title_part = match.group(2).strip() if match.group(2) else ''
                        chapter_title = f"{chapter_num} {title_part}".strip()
                    elif pattern_type == 'markdown':
                        # Markdown格式
                        chapter_title = match.group(1).strip()
                    break

            if chapter_title:
                # 保存上一章节
                if current_chapter:
                    raw_content = '\n'.join(current_content).strip()
                    html_content = self._convert_text_to_html(raw_content)
                    chapters.append({
                        'title': current_chapter,
                        'content': html_content
                    })

                # 开始新章节
                current_chapter = chapter_title
                current_content = []
            else:
                # 累积内容（只有在已经开始章节后才累积）
                if current_chapter is not None:
                    current_content.append(line)

        # 保存最后一章
        if current_chapter and current_content:
            raw_content = '\n'.join(current_content).strip()
            html_content = self._convert_text_to_html(raw_content)
            chapters.append({
                'title': current_chapter,
                'content': html_content
            })

        return chapters

    def _convert_text_to_html(self, text: str) -> str:
        """将纯文本转换为HTML段落格式

        中文小说格式：每个非空行都是一个独立段落
        """
        if not text or not text.strip():
            return ""

        # 将每个非空行转换为 <p> 标签
        lines = text.split('\n')
        html_paragraphs = []

        for line in lines:
            stripped_line = line.strip()
            if stripped_line:  # 只处理非空行
                html_paragraphs.append(f'<p>{stripped_line}</p>')

        return ''.join(html_paragraphs)
