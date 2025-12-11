from typing import Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from uuid import UUID
from datetime import datetime, timedelta, timezone

from app.models.chapter_word_stat import ChapterWordStat
from app.models.chapter import Chapter
from app.models.work import Work


class ChapterWordStatService:
    """章节字数增量统计服务"""

    def __init__(self, db: AsyncSession):
        self.db = db

    async def add_delta(self, chapter_id: str | UUID, delta: int, auto_commit: bool = True) -> Optional[ChapterWordStat]:
        """
        记录一次字数增量（delta 可为负，0 则跳过）

        Args:
            chapter_id: 章节ID
            delta: 字数增量（正数表示新增，负数表示减少）
            auto_commit: 是否自动提交事务（默认True，适用于独立调用）

        Returns:
            ChapterWordStat对象，如果delta为0则返回None

        Note:
            - 默认auto_commit=True是为了向后兼容和简化使用
            - 如果在同一事务中调用，设置auto_commit=False
        """
        if delta == 0:
            return None
        stat = ChapterWordStat(
            chapter_id=UUID(str(chapter_id)),
            delta=delta,
        )
        self.db.add(stat)

        if auto_commit:
            await self.db.commit()
            await self.db.refresh(stat)

        return stat

    async def sum_delta_for_author_since(self, author_id: str, since: datetime) -> int:
        """汇总作者自指定时间以来的增量"""
        result = await self.db.execute(
            select(func.coalesce(func.sum(ChapterWordStat.delta), 0))
            .select_from(ChapterWordStat)
            .join(Chapter, Chapter.id == ChapterWordStat.chapter_id)
            .join(Work, Work.id == Chapter.work_id)
            .where(
                Work.author_id == UUID(str(author_id)),
                ChapterWordStat.created_at >= since,
            )
        )
        return result.scalar() or 0
