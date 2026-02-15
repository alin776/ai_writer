"""导出服务"""
import json
import logging
from typing import Optional, List
from uuid import UUID
from datetime import datetime
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.orm import selectinload

from app.models.work import Work
from app.models.chapter import Chapter
from app.models.character import Character
from app.models.location import Location
from app.models.setting import Setting
from app.models.work_guidelines import WorkGuidelines
from app.models.ai_guidelines import AIGuidelines
from app.models.novel_analysis import NovelAnalysis
from app.schemas.export import (
    ExportOptions,
    ExportData,
    ExportWork,
    ExportChapter,
    ExportCharacter,
    ExportLocation,
    ExportSetting,
    ExportWorldview,
    ExportGuidelines
)
from app.utils.markdown_generator import MarkdownGenerator
from app.utils.file_storage import temp_storage
from app.utils.datetime_utils import get_utc_now
from app.services.chapter_content_provider import ChapterContentProvider

logger = logging.getLogger(__name__)


class ExportService:
    """导出服务类"""
    
    def __init__(self, db: AsyncSession):
        self.db = db
        self.content_provider = ChapterContentProvider()
    
    async def export_work(
        self, 
        work_id: UUID, 
        user_id: UUID, 
        options: ExportOptions
    ) -> tuple[bytes, str]:
        """导出作品
        
        Args:
            work_id: 作品ID
            user_id: 用户ID（权限验证）
            options: 导出选项
        
        Returns:
            (文件内容, 文件名)
        """
        # 验证权限
        work = await self._get_work_with_permission(work_id, user_id)
        if not work:
            raise ValueError("作品不存在或无权限")
        
        # 根据格式导出
        if options.format == "json":
            return await self._export_json(work, options)
        elif options.format == "markdown":
            return await self._export_markdown(work, options)
        else:
            raise ValueError(f"不支持的导出格式: {options.format}")
    
    async def _get_work_with_permission(
        self, 
        work_id: UUID, 
        user_id: UUID
    ) -> Optional[Work]:
        """获取作品并验证权限"""
        stmt = select(Work).where(
            Work.id == work_id,
            Work.author_id == user_id
        ).options(
            selectinload(Work.chapters),
            selectinload(Work.characters),
            selectinload(Work.locations),
            selectinload(Work.settings),
            selectinload(Work.guidelines),
            selectinload(Work.ai_guidelines),
            selectinload(Work.novel_analysis)
        )
        
        result = await self.db.execute(stmt)
        return result.scalar_one_or_none()
    
    async def _export_json(
        self, 
        work: Work, 
        options: ExportOptions
    ) -> tuple[bytes, str]:
        """导出为JSON格式"""
        logger.info(f"导出作品 {work.id} 为JSON格式")
        
        # 构建导出数据
        export_data = ExportData(
            version="1.0",
            exported_at=get_utc_now(),
            work=self._serialize_work(work),
            chapters=self._serialize_chapters(work, options) if options.include_chapters else [],
            worldview=self._serialize_worldview(work) if options.include_worldview else None,
            guidelines=self._serialize_guidelines(work) if options.include_guidelines else None,
            analysis=self._serialize_analysis(work) if options.include_analysis else None
        )
        
        # 转换为JSON
        json_str = export_data.model_dump_json(indent=2, exclude_none=True)
        content = json_str.encode('utf-8')
        
        # 生成文件名
        filename = f"{work.title}_{get_utc_now().strftime('%Y%m%d')}.json"
        
        return content, filename
    
    async def _export_markdown(
        self, 
        work: Work, 
        options: ExportOptions
    ) -> tuple[bytes, str]:
        """导出为Markdown格式"""
        logger.info(f"导出作品 {work.id} 为Markdown格式")
        
        md = MarkdownGenerator()
        
        # 添加标题和元数据
        md.add_title(work.title)
        md.add_metadata({
            'genre': work.genre.value if work.genre else '未知',
            'status': work.status.value if work.status else '未知',
            'total_words': work.total_words,
            'updated_at': work.updated_at.isoformat() if work.updated_at else ''
        })
        
        # 添加简介
        md.add_description(work.description)
        
        # 添加章节
        if options.include_chapters:
            chapters = work.chapters
            
            # 如果指定了章节ID，只导出这些章节
            if options.chapter_ids:
                chapter_ids_set = set(options.chapter_ids)
                chapters = [c for c in chapters if c.id in chapter_ids_set]
            
            # 按order排序
            chapters = sorted(chapters, key=lambda c: c.order)
            
            for chapter in chapters:
                content = self.content_provider.read_content(
                    str(chapter.work_id), str(chapter.id)
                ) or ""
                md.add_chapter(chapter.title, content)
        
        # 添加世界观附录
        if options.include_worldview:
            characters = [self._character_to_dict(c) for c in work.characters]
            locations = [self._location_to_dict(l) for l in work.locations]
            settings = [self._setting_to_dict(s) for s in work.settings]
            
            md.add_worldview_appendix(characters, locations, settings)
        
        # 生成Markdown文本
        markdown_text = md.generate()
        content = markdown_text.encode('utf-8')
        
        # 生成文件名
        filename = f"{work.title}_{get_utc_now().strftime('%Y%m%d')}.md"
        
        return content, filename
    
    def _serialize_work(self, work: Work) -> ExportWork:
        """序列化作品信息"""
        return ExportWork(
            id=work.id,
            title=work.title,
            description=work.description,
            genre=work.genre.value if work.genre else 'other',
            status=work.status.value if work.status else 'draft',
            total_words=work.total_words,
            total_chapters=work.total_chapters,
            created_at=work.created_at,
            updated_at=work.updated_at
        )
    
    def _serialize_chapters(
        self, 
        work: Work, 
        options: ExportOptions
    ) -> List[ExportChapter]:
        """序列化章节列表"""
        chapters = work.chapters
        
        # 如果指定了章节ID，只导出这些章节
        if options.chapter_ids:
            chapter_ids_set = set(options.chapter_ids)
            chapters = [c for c in chapters if c.id in chapter_ids_set]
        
        # 按order排序
        chapters = sorted(chapters, key=lambda c: c.order)
        
        return [
            ExportChapter(
                id=c.id,
                title=c.title,
                content=self.content_provider.read_content(
                    str(c.work_id), str(c.id)
                ) or "",
                summary=c.summary,
                order=c.order,
                word_count=c.word_count,
                is_published=c.is_published,
                created_at=c.created_at,
                updated_at=c.updated_at
            )
            for c in chapters
        ]
    
    def _serialize_worldview(self, work: Work) -> ExportWorldview:
        """序列化世界观数据"""
        return ExportWorldview(
            characters=[
                ExportCharacter(
                    id=c.id,
                    name=c.name,
                    role=c.role,
                    description=c.description,
                    tags=c.tags or [],
                    relationships=c.relationships or []
                )
                for c in work.characters
            ],
            locations=[
                ExportLocation(
                    id=l.id,
                    name=l.name,
                    type=l.type,
                    description=l.description,
                    tags=l.tags or [],
                    related_locations=l.related_locations or []
                )
                for l in work.locations
            ],
            settings=[
                ExportSetting(
                    id=s.id,
                    title=s.title,
                    category=s.category,
                    content=s.content,
                    tags=s.tags or []
                )
                for s in work.settings
            ]
        )
    
    def _serialize_guidelines(self, work: Work) -> ExportGuidelines:
        """序列化规范数据"""
        work_guidelines = None
        ai_guidelines = None
        
        if work.guidelines:
            work_guidelines = {
                'genre': work.guidelines.genre,
                'tone': work.guidelines.tone,
                'theme': work.guidelines.theme,
                'target_audience': work.guidelines.target_audience
            }
        
        if work.ai_guidelines:
            ag = work.ai_guidelines
            ai_guidelines = {
                'business_goal': ag.business_goal,
                'target_audience': ag.target_audience,
                'commercial_benchmark': ag.commercial_benchmark,
                'high_concept': ag.high_concept,
                'core_paradox': ag.core_paradox,
                'dominant_emotion': ag.dominant_emotion,
                'core_ip_symbols': ag.core_ip_symbols,
                'protagonist_arc': ag.protagonist_arc,
                'core_conflict': ag.core_conflict,
                'narrative_rhythm': ag.narrative_rhythm,
                'writing_style': ag.writing_style,
                'style_notes': ag.style_notes,
                'chapter_length': ag.chapter_length,
                'content_taboos': ag.content_taboos,
                'primary_genre': ag.primary_genre,
                'secondary_tags': ag.secondary_tags,
                'creative_tone': ag.creative_tone,
                'world_intro': ag.world_intro,
                'main_locations': ag.main_locations,
                'world_rules': ag.world_rules,
                'power_system_name': ag.power_system_name,
                'power_levels': ag.power_levels,
                'power_cost': ag.power_cost,
                'protagonist_name': ag.protagonist_name,
                'protagonist_identity': ag.protagonist_identity,
                'protagonist_traits': ag.protagonist_traits,
                'protagonist_goal': ag.protagonist_goal,
                'conflict_design': ag.conflict_design,
                'act_one': ag.act_one,
                'act_two': ag.act_two,
                'act_three': ag.act_three
            }
        
        return ExportGuidelines(
            work_guidelines=work_guidelines,
            ai_guidelines=ai_guidelines
        )
    
    def _serialize_analysis(self, work: Work) -> Optional[dict]:
        """序列化分析报告"""
        if not work.novel_analysis:
            return None
        
        analysis = work.novel_analysis
        return {
            'status': analysis.status,
            'micro_analysis': analysis.micro_analysis,
            'macro_analysis': analysis.macro_analysis,
            'created_at': analysis.created_at.isoformat() if analysis.created_at else None,
            'completed_at': analysis.completed_at.isoformat() if analysis.completed_at else None
        }
    
    def _character_to_dict(self, character: Character) -> dict:
        """转换人物为字典"""
        return {
            'name': character.name,
            'role': character.role,
            'description': character.description,
            'tags': character.tags or []
        }
    
    def _location_to_dict(self, location: Location) -> dict:
        """转换地点为字典"""
        return {
            'name': location.name,
            'type': location.type,
            'description': location.description,
            'tags': location.tags or []
        }
    
    def _setting_to_dict(self, setting: Setting) -> dict:
        """转换设定为字典"""
        return {
            'title': setting.title,
            'category': setting.category,
            'content': setting.content
        }
