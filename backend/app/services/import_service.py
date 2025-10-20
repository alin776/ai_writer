"""导入服务"""
import json
import logging
import re
from typing import Optional, Dict, Any, List, Tuple
from uuid import UUID
from datetime import datetime
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.models.work import Work, WorkGenre, WorkStatus
from app.models.chapter import Chapter
from app.models.character import Character
from app.models.location import Location
from app.models.setting import Setting
from app.models.work_guidelines import WorkGuidelines
from app.models.ai_guidelines import AIGuidelines
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
        
        Args:
            content: 文件内容
            user_id: 用户ID
            options: 导入选项
        
        Returns:
            导入结果
        """
        try:
            if options.format == "json":
                return await self._import_json(content, user_id, options)
            elif options.format in ["markdown", "txt"]:
                return await self._import_text(content, user_id, options)
            else:
                raise ValueError(f"不支持的导入格式: {options.format}")
        except Exception as e:
            logger.error(f"导入作品失败: {e}", exc_info=True)
            await self.db.rollback()
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
        
        # 构建预览信息
        preview_work = ImportPreviewWork(
            title=work_data['title'],
            description=work_data.get('description'),
            genre=work_data.get('genre'),
            total_words=work_data.get('total_words', 0),
            total_chapters=len(chapters_data)
        )
        
        preview_chapters = [
            ImportPreviewChapter(
                title=c['title'],
                word_count=c.get('word_count', 0),
                order=c.get('order', idx + 1)
            )
            for idx, c in enumerate(chapters_data)
        ]
        
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
        text = content.decode('utf-8')
        
        # 提取标题（第一行或第一个#标题）
        title = self._extract_title(text)
        
        # 智能章节分割
        chapters = self._split_chapters(text)
        
        # 计算总字数
        total_words = len(text.replace('\n', '').replace(' ', ''))
        
        preview_work = ImportPreviewWork(
            title=title,
            description=None,
            genre=None,
            total_words=total_words,
            total_chapters=len(chapters)
        )
        
        preview_chapters = [
            ImportPreviewChapter(
                title=c['title'],
                word_count=len(c['content'].replace('\n', '').replace(' ', '')),
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
            total_words=0,  # 后续重新计算
            total_chapters=0
        )
        self.db.add(work)
        await self.db.flush()
        
        # 导入章节
        chapters_created = 0
        for idx, chapter_data in enumerate(chapters_data):
            chapter = Chapter(
                work_id=work.id,
                title=chapter_data['title'],
                content=chapter_data.get('content', ''),
                summary=chapter_data.get('summary'),
                order=chapter_data.get('order', idx + 1),
                word_count=chapter_data.get('word_count', 0),
                is_published=chapter_data.get('is_published', False)
            )
            self.db.add(chapter)
            chapters_created += 1
        
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
        work.total_words = sum(c.word_count for c in work.chapters)
        
        await self.db.commit()
        
        logger.info(f"导入完成: 作品ID={work.id}, 章节={chapters_created}, 人物={characters_created}")
        
        return ImportResponse(
            work_id=work.id,
            chapters_created=chapters_created,
            characters_created=characters_created,
            locations_created=locations_created,
            settings_created=settings_created,
            message="导入成功"
        )
    
    async def _import_text(
        self,
        content: bytes,
        user_id: UUID,
        options: ImportOptions
    ) -> ImportResponse:
        """导入文本/Markdown格式"""
        logger.info(f"用户 {user_id} 开始导入文本数据")
        
        text = content.decode('utf-8')
        
        # 提取标题
        title = self._extract_title(text)
        
        # 分割章节
        chapters = self._split_chapters(text)
        
        # 如果没有检测到章节，整个文本作为单章
        if not chapters:
            chapters = [{'title': '第一章', 'content': text}]
        
        # 创建作品
        work = Work(
            author_id=user_id,
            title=title,
            description=None,
            genre=WorkGenre.OTHER,
            status=WorkStatus.DRAFT,
            total_words=0,
            total_chapters=0
        )
        self.db.add(work)
        await self.db.flush()
        
        # 导入章节
        chapters_created = 0
        for idx, chapter_data in enumerate(chapters):
            content = chapter_data['content']
            word_count = len(content.replace('\n', '').replace(' ', ''))
            
            chapter = Chapter(
                work_id=work.id,
                title=chapter_data['title'],
                content=f"<p>{content.replace(chr(10), '</p><p>')}</p>",  # 简单HTML转换
                order=idx + 1,
                word_count=word_count,
                is_published=False
            )
            self.db.add(chapter)
            chapters_created += 1
        
        # 更新作品统计
        work.total_chapters = chapters_created
        work.total_words = sum(c.word_count for c in work.chapters)
        
        await self.db.commit()
        
        logger.info(f"文本导入完成: 作品ID={work.id}, 章节={chapters_created}")
        
        return ImportResponse(
            work_id=work.id,
            chapters_created=chapters_created,
            message="导入成功"
        )
    
    def _extract_title(self, text: str) -> str:
        """从文本中提取标题"""
        lines = text.strip().split('\n')
        
        # 尝试从Markdown标题提取
        for line in lines[:10]:  # 只检查前10行
            line = line.strip()
            if line.startswith('# '):
                return line[2:].strip()[:200]
        
        # 使用第一行非空行作为标题
        for line in lines[:5]:
            line = line.strip()
            if line and len(line) <= 200:
                return line
        
        return "未命名作品"
    
    def _split_chapters(self, text: str) -> List[Dict[str, str]]:
        """智能分割章节
        
        识别模式：
        - "第X章" "Chapter X"
        - "## 第X章"（Markdown）
        - "# 标题"（Markdown一级标题）
        """
        chapters = []
        
        # 模式1: 第X章
        pattern1 = r'第[零一二三四五六七八九十百千万\d]+章[\s：:]+(.+)?'
        # 模式2: Chapter X
        pattern2 = r'Chapter\s+\d+[\s：:]*(.+)?'
        # 模式3: Markdown标题
        pattern3 = r'^##\s+(.+)$'
        
        lines = text.split('\n')
        current_chapter = None
        current_content = []
        
        for line in lines:
            # 检查是否匹配章节标题
            match1 = re.match(pattern1, line.strip())
            match2 = re.match(pattern2, line.strip(), re.IGNORECASE)
            match3 = re.match(pattern3, line.strip())
            
            if match1 or match2 or match3:
                # 保存上一章节
                if current_chapter:
                    chapters.append({
                        'title': current_chapter,
                        'content': '\n'.join(current_content).strip()
                    })
                
                # 开始新章节
                current_chapter = line.strip().lstrip('#').strip()
                current_content = []
            else:
                # 累积内容
                if current_chapter:
                    current_content.append(line)
        
        # 保存最后一章
        if current_chapter and current_content:
            chapters.append({
                'title': current_chapter,
                'content': '\n'.join(current_content).strip()
            })
        
        return chapters
