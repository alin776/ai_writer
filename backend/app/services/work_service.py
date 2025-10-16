from typing import List, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from sqlalchemy.orm import selectinload

from app.models.work import Work
from app.models.chapter import Chapter
from app.schemas.work import WorkCreate, WorkUpdate


class WorkService:
    """作品服务"""
    
    def __init__(self, db: AsyncSession):
        self.db = db
    
    async def get_work_by_id(self, work_id: str) -> Optional[Work]:
        """根据 ID 获取作品"""
        result = await self.db.execute(
            select(Work)
            .options(selectinload(Work.chapters))
            .where(Work.id == work_id)
        )
        return result.scalar_one_or_none()
    
    async def get_works(
        self,
        author_id: Optional[str] = None,
        skip: int = 0,
        limit: int = 100,
        search: Optional[str] = None
    ) -> tuple[List[Work], int]:
        """获取作品列表"""
        query = select(Work)
        count_query = select(func.count(Work.id))
        
        if author_id:
            query = query.where(Work.author_id == author_id)
            count_query = count_query.where(Work.author_id == author_id)
        
        if search:
            query = query.where(Work.title.ilike(f"%{search}%"))
            count_query = count_query.where(Work.title.ilike(f"%{search}%"))
        
        # 获取总数
        total_result = await self.db.execute(count_query)
        total = total_result.scalar()
        
        # 获取列表
        query = query.offset(skip).limit(limit).order_by(Work.updated_at.desc())
        result = await self.db.execute(query)
        works = result.scalars().all()
        
        return works, total
    
    async def create_work(self, author_id: str, work_data: WorkCreate) -> Work:
        """创建作品"""
        work = Work(
            author_id=author_id,
            **work_data.model_dump()
        )
        
        self.db.add(work)
        await self.db.commit()
        await self.db.refresh(work)
        
        return work
    
    async def update_work(self, work_id: str, work_data: WorkUpdate) -> Optional[Work]:
        """更新作品"""
        work = await self.get_work_by_id(work_id)
        if not work:
            return None
        
        # 更新字段
        update_data = work_data.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(work, field, value)
        
        await self.db.commit()
        await self.db.refresh(work)
        
        return work
    
    async def delete_work(self, work_id: str) -> bool:
        """删除作品"""
        work = await self.get_work_by_id(work_id)
        if not work:
            return False
        
        await self.db.delete(work)
        await self.db.commit()
        
        return True
    
    async def update_work_stats(self, work_id: str):
        """更新作品统计信息"""
        work = await self.get_work_by_id(work_id)
        if not work:
            return
        
        # 统计章节数和总字数
        result = await self.db.execute(
            select(
                func.count(Chapter.id),
                func.sum(Chapter.word_count)
            ).where(Chapter.work_id == work_id)
        )
        chapter_count, total_words = result.one()
        
        work.total_chapters = chapter_count or 0
        work.total_words = total_words or 0
        
        await self.db.commit()
