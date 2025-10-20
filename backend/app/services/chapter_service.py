from typing import List, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
import re

from app.models.chapter import Chapter
from app.schemas.chapter import ChapterCreate, ChapterUpdate
from app.utils.cache import CacheInvalidator
from app.core.redis import redis_client, CacheKey, CacheExpire


def calculate_word_count(content: str) -> int:
    """
    计算文本字数（去除HTML标签）
    - 移除所有HTML标签
    - 中文：按字符数
    - 英文：按单词数
    - 数字：按字符数
    """
    if not content:
        return 0
    
    # 移除HTML标签
    text = re.sub(r'<[^>]+>', '', content)
    
    # 移除多余的空白字符
    text = re.sub(r'\s+', ' ', text).strip()
    
    # 计算中文字符数
    chinese_chars = len(re.findall(r'[\u4e00-\u9fff]', text))
    
    # 计算英文单词数
    english_words = len(re.findall(r'[a-zA-Z]+', text))
    
    # 计算数字字符数
    digits = len(re.findall(r'[0-9]', text))
    
    # 返回总字数（中文字符 + 英文单词 + 数字）
    return chinese_chars + english_words + digits


class ChapterService:
    """章节服务"""
    
    def __init__(self, db: AsyncSession):
        self.db = db
    
    async def get_chapter_by_id(self, chapter_id: str) -> Optional[Chapter]:
        """根据 ID 获取章节"""
        result = await self.db.execute(
            select(Chapter).where(Chapter.id == chapter_id)
        )
        return result.scalar_one_or_none()
    
    async def get_chapters_by_work(
        self,
        work_id: str,
        skip: int = 0,
        limit: int = 1000
    ) -> List[Chapter]:
        """获取作品的章节列表"""
        from uuid import UUID
        import logging
        logger = logging.getLogger(__name__)
        
        # 将字符串转换为UUID对象
        if isinstance(work_id, str):
            work_id_uuid = UUID(work_id)
        else:
            work_id_uuid = work_id
        
        logger.info(f"[ChapterService] Querying chapters for work_id={work_id_uuid}, type={type(work_id_uuid)}")
        
        result = await self.db.execute(
            select(Chapter)
            .where(Chapter.work_id == work_id_uuid)
            .order_by(Chapter.order)
            .offset(skip)
            .limit(limit)
        )
        chapters = list(result.scalars().all())
        
        logger.info(f"[ChapterService] Found {len(chapters)} chapters")
        for ch in chapters:
            logger.info(f"  - Chapter: {ch.title}, order={ch.order}")
        
        return chapters
    
    async def create_chapter(self, chapter_data: ChapterCreate) -> Chapter:
        """创建章节"""
        # 如果没有指定顺序，自动计算
        if chapter_data.order is None:
            result = await self.db.execute(
                select(func.max(Chapter.order))
                .where(Chapter.work_id == chapter_data.work_id)
            )
            max_order = result.scalar()
            order = (max_order or 0) + 1
        else:
            order = chapter_data.order
        
        # 计算字数（去除HTML标签）
        word_count = calculate_word_count(chapter_data.content)
        
        chapter = Chapter(
            work_id=chapter_data.work_id,
            title=chapter_data.title,
            content=chapter_data.content,
            order=order,
            word_count=word_count,
        )
        
        self.db.add(chapter)
        await self.db.commit()
        await self.db.refresh(chapter)
        
        return chapter
    
    async def update_chapter(self, chapter_id: str, chapter_data: ChapterUpdate) -> Optional[Chapter]:
        """更新章节"""
        chapter = await self.get_chapter_by_id(chapter_id)
        if not chapter:
            return None
        
        work_id = str(chapter.work_id)
        
        # 更新字段
        update_data = chapter_data.model_dump(exclude_unset=True)
        
        # 如果更新了内容，重新计算字数（去除HTML标签）
        if "content" in update_data:
            update_data["word_count"] = calculate_word_count(update_data["content"])
        
        for field, value in update_data.items():
            setattr(chapter, field, value)
        
        await self.db.commit()
        await self.db.refresh(chapter)
        
        # 使缓存失效
        await CacheInvalidator.invalidate_chapter(chapter_id, work_id)
        
        return chapter
    
    async def delete_chapter(self, chapter_id: str) -> bool:
        """删除章节"""
        chapter = await self.get_chapter_by_id(chapter_id)
        if not chapter:
            return False
        
        work_id = chapter.work_id
        work_id_str = str(work_id)
        order = chapter.order
        
        # 删除章节
        await self.db.delete(chapter)
        
        # 重新排序后续章节
        result = await self.db.execute(
            select(Chapter)
            .where(Chapter.work_id == work_id, Chapter.order > order)
        )
        subsequent_chapters = result.scalars().all()
        
        for ch in subsequent_chapters:
            ch.order -= 1
        
        await self.db.commit()
        
        # 使缓存失效
        await CacheInvalidator.invalidate_chapter(chapter_id, work_id_str)
        
        return True
    
    async def reorder_chapters(self, work_id: str, chapter_ids: List[str]) -> bool:
        """重新排序章节"""
        for index, chapter_id in enumerate(chapter_ids):
            chapter = await self.get_chapter_by_id(chapter_id)
            if chapter and chapter.work_id == work_id:
                chapter.order = index + 1
        
        await self.db.commit()
        return True
