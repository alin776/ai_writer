"""导入服务"""
import json
import logging
import re
import threading
from pathlib import Path
from typing import Optional, Dict, Any, List
from uuid import UUID
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.work import Work, WorkGenre, WorkStatus
from app.models.ai_guidelines import AIGuidelines
from app.services.agent.deep_agent import DATA_ROOT
from app.services.agent.deep_agent.frontmatter import build_chapter, chapter_filename
from app.services.agent.deep_agent.rag_tool import update_chapter_vectors
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
    ) -> ImportResponse:
        """导入作品

        Returns:
            ImportResponse: 导入结果
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
    ) -> ImportResponse:
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
            total_words=0,
            total_chapters=0
        )
        self.db.add(work)
        await self.db.flush()

        # 写入章节 .md 文件
        chapters_created = 0
        total_words = 0
        work_path = DATA_ROOT / str(user_id) / "works" / str(work.id)
        chapters_dir = work_path / "chapters"
        chapters_dir.mkdir(parents=True, exist_ok=True)

        for idx, chapter_data in enumerate(chapters_data):
            content_text = chapter_data.get('content', '')
            word_count = chapter_data.get('word_count') or self._calculate_word_count(content_text)
            total_words += word_count

            num = chapter_data.get('order', idx + 1)
            status = chapter_data.get('status', 'draft')
            if status not in ('draft', 'completed', 'published'):
                status = 'draft'
            md_content = build_chapter(chapter_data['title'], status, content_text)
            chapter_file = chapters_dir / chapter_filename(num, chapter_data['title'])
            chapter_file.write_text(md_content, encoding="utf-8")
            chapters_created += 1

        # 生成世界观 .md 文件
        if worldview_data:
            self._generate_worldview_files(work_path, worldview_data)

        # 导入AI规范（保留 DB 写入）
        if options.include_guidelines and guidelines_data:
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
        work.total_words = total_words
        await self.db.commit()

        # 后台向量化
        self._vectorize_chapters_background(str(work.id), chapters_dir)

        logger.info(f"导入完成: 作品ID={work.id}, 章节={chapters_created}")

        return ImportResponse(
            work_id=work.id,
            chapters_created=chapters_created,
            message="导入成功"
        )
    
    async def _import_text(
        self,
        content: bytes,
        user_id: UUID,
        options: ImportOptions,
        append_to: Optional[str] = None
    ) -> ImportResponse:
        """导入文本/Markdown格式"""
        logger.info(f"用户 {user_id} 开始导入文本数据")

        text = self._smart_decode(content)

        # 智能提取元信息（标题、简介）
        metadata = self._extract_metadata(text)
        title = metadata['title']
        description = metadata['description']

        # 分割章节
        chapters = self._split_chapters(text)
        if not chapters:
            chapters = [{'title': title, 'content': text.strip()}]

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
            # 从文件系统获取最大章节序号
            chapters_dir = DATA_ROOT / str(work.author_id) / "works" / str(work.id) / "chapters"
            if chapters_dir.exists():
                existing_nums = [
                    int(m.group(1))
                    for p in chapters_dir.glob("*.md")
                    if (m := re.match(r"^(\d+)-", p.stem))
                ]
                starting_order = max(existing_nums) if existing_nums else 0
            else:
                starting_order = 0
            total_words = work.total_words or 0
        else:
            # 解析 genre
            genre = WorkGenre.OTHER
            if options.genre:
                try:
                    genre = WorkGenre(options.genre)
                except ValueError:
                    genre = WorkGenre.OTHER

            work = Work(
                author_id=user_id,
                title=title,
                description=description,
                genre=genre,
                status=WorkStatus.DRAFT,
                total_words=0,
                total_chapters=0
            )
            self.db.add(work)
            await self.db.flush()

        # 写入章节 .md 文件
        chapters_created = 0
        work_path = DATA_ROOT / str(work.author_id) / "works" / str(work.id)
        chapters_dir = work_path / "chapters"
        chapters_dir.mkdir(parents=True, exist_ok=True)

        for idx, chapter_data in enumerate(chapters):
            content_text = chapter_data['content']
            word_count = self._calculate_word_count(content_text)
            total_words += word_count

            num = starting_order + idx + 1
            md_content = build_chapter(chapter_data['title'], "draft", content_text)
            chapter_file = chapters_dir / chapter_filename(num, chapter_data['title'])
            chapter_file.write_text(md_content, encoding="utf-8")
            chapters_created += 1

        # 更新作品统计
        work.total_chapters = (work.total_chapters or 0) + chapters_created
        work.total_words = total_words
        await self.db.commit()

        # 后台向量化
        self._vectorize_chapters_background(str(work.id), chapters_dir)

        logger.info(f"文本导入完成: 作品ID={work.id}, 章节={chapters_created}")

        return ImportResponse(
            work_id=work.id,
            chapters_created=chapters_created,
            message="导入成功"
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
            if idx < start_line:
                continue
            stripped = line.strip()

            # 检查是否匹配章节标题
            chapter_title = None
            for pattern, pattern_type in compiled_patterns:
                match = pattern.match(stripped)
                if match:
                    if pattern_type == 'bracket':
                        # 【第X章 标题】格式，group(1)是完整标题
                        full_title = match.group(1).strip()
                        # 去掉章节号前缀，只保留标题名
                        title_only = re.sub(r'^第[零一二三四五六七八九十百千万\d]+[章回节]\s*', '', full_title).strip()
                        suffix = match.group(2).strip() if match.group(2) else ''
                        if suffix:
                            chapter_title = f"{title_only} {suffix}".strip() if title_only else suffix
                        else:
                            chapter_title = title_only or full_title
                    elif pattern_type == 'chinese_with_title':
                        # 第X章 标题 格式 → 只保留标题部分
                        chapter_title = match.group(2).strip()
                    elif pattern_type == 'chinese_only':
                        # 第X章 单独格式（无标题名），保留完整作为标题
                        chapter_title = match.group(1)
                    elif pattern_type == 'english':
                        # Chapter X 格式 → 只保留标题部分
                        title_part = match.group(2).strip() if match.group(2) else ''
                        chapter_title = title_part or match.group(1)
                    elif pattern_type == 'markdown':
                        # Markdown格式
                        chapter_title = match.group(1).strip()
                    break

            if chapter_title:
                # 保存上一章节
                if current_chapter:
                    raw_content = '\n'.join(current_content).strip('\n\r\t ')
                    chapters.append({
                        'title': current_chapter,
                        'content': raw_content
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
            raw_content = '\n'.join(current_content).strip('\n\r\t ')
            chapters.append({
                'title': current_chapter,
                'content': raw_content
            })

        return chapters

    @staticmethod
    def _generate_worldview_files(work_path: Path, worldview_data: Dict[str, Any]) -> None:
        """从世界观数据生成 .md 文件（characters.md + worldview.md）"""
        work_path.mkdir(parents=True, exist_ok=True)

        # 生成 characters.md
        characters = worldview_data.get('characters', [])
        if characters:
            lines = ["# 人物设定\n"]
            for c in characters:
                lines.append(f"## {c.get('name', '未知')}")
                if c.get('role'):
                    lines.append(f"- 角色：{c['role']}")
                if c.get('description'):
                    lines.append(f"- 描述：{c['description']}")
                tags = c.get('tags', [])
                if tags:
                    lines.append(f"- 标签：{'、'.join(tags)}")
                lines.append("")
            (work_path / "characters.md").write_text('\n'.join(lines), encoding="utf-8")

        # 生成 worldview.md（地点 + 设定）
        locations = worldview_data.get('locations', [])
        settings = worldview_data.get('settings', [])
        if locations or settings:
            lines = ["# 世界观设定\n"]
            if locations:
                lines.append("## 地点")
                for loc in locations:
                    lines.append(f"### {loc.get('name', '未知')}")
                    if loc.get('type'):
                        lines.append(f"- 类型：{loc['type']}")
                    if loc.get('description'):
                        lines.append(f"- 描述：{loc['description']}")
                    lines.append("")
            if settings:
                lines.append("## 设定")
                for s in settings:
                    lines.append(f"### {s.get('title', '未知')}")
                    if s.get('category'):
                        lines.append(f"- 分类：{s['category']}")
                    if s.get('content'):
                        lines.append(f"- 内容：{s['content']}")
                    lines.append("")
            (work_path / "worldview.md").write_text('\n'.join(lines), encoding="utf-8")

    @staticmethod
    def _vectorize_chapters_background(work_id: str, chapters_dir: Path) -> None:
        """后台线程调用 update_chapter_vectors / update_knowledge_vectors 对章节和知识库进行向量化"""
        def _run():
            try:
                from app.services.agent.deep_agent.frontmatter import parse_chapter
                from app.services.agent.deep_agent.rag_tool import update_chapter_vectors, update_knowledge_vectors
                # 索引章节
                for md_file in sorted(chapters_dir.glob("*.md")):
                    raw = md_file.read_text(encoding="utf-8")
                    parsed = parse_chapter(raw)
                    content = parsed.get("content", "").strip()
                    if len(content) < 100:
                        continue
                    path = f"/chapters/{md_file.name}"
                    update_chapter_vectors(work_id, path, content)

                # 索引知识库文件
                knowledge_dir = chapters_dir.parent / "knowledge"
                if knowledge_dir.is_dir():
                    for md_file in knowledge_dir.rglob("*.md"):
                        raw = md_file.read_text(encoding="utf-8")
                        if len(raw.strip()) < 50:
                            continue
                        rel_path = "/" + str(md_file.relative_to(chapters_dir.parent)).replace("\\", "/")
                        update_knowledge_vectors(work_id, rel_path, raw)
            except Exception as exc:
                logger.warning("[ImportService] 后台向量化失败: %s", exc)

        thread = threading.Thread(target=_run, daemon=True)
        thread.start()
