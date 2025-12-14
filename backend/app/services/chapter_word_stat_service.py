from typing import Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from uuid import UUID
from datetime import datetime, timedelta, timezone
import logging

from app.models.chapter_word_stat import ChapterWordStat
from app.models.chapter import Chapter
from app.models.work import Work

logger = logging.getLogger(__name__)

# 中国时区 UTC+8
CHINA_TZ = timezone(timedelta(hours=8))


class ChapterWordStatService:
    """章节字数增量统计服务"""

    def __init__(self, db: AsyncSession):
        self.db = db

    async def check_edit_event_exists(self, edit_event_id: str) -> bool:
        """
        检查编辑事件是否已存在（幂等性检查）

        Args:
            edit_event_id: 编辑事件唯一标识

        Returns:
            True 表示已存在，False 表示不存在
        """
        if not edit_event_id:
            return False

        result = await self.db.execute(
            select(ChapterWordStat.id)
            .where(ChapterWordStat.edit_event_id == edit_event_id)
            .limit(1)
        )
        return result.scalar_one_or_none() is not None

    async def add_delta(
        self,
        chapter_id: str | UUID,
        delta: int,
        edit_event_id: Optional[str] = None,
        auto_commit: bool = True
    ) -> Optional[ChapterWordStat]:
        """
        记录一次字数增量（仅记录正增量，支持幂等）

        Args:
            chapter_id: 章节ID
            delta: 字数增量（仅正数会被记录）
            edit_event_id: 编辑事件唯一标识（用于幂等性检查）
            auto_commit: 是否自动提交事务（默认True，适用于独立调用）

        Returns:
            ChapterWordStat对象，如果delta<=0或重复则返回None

        Note:
            - 只记录正增量（delta > 0）
            - 如果 edit_event_id 已存在，跳过记录（幂等）
        """
        # 只记录正增量
        if delta <= 0:
            logger.debug(f"跳过非正增量: chapter_id={chapter_id}, delta={delta}")
            return None

        # 幂等性检查
        if edit_event_id and await self.check_edit_event_exists(edit_event_id):
            logger.info(f"编辑事件已存在，跳过: edit_event_id={edit_event_id}")
            return None

        stat = ChapterWordStat(
            chapter_id=UUID(str(chapter_id)),
            delta=delta,
            edit_event_id=edit_event_id,
        )
        self.db.add(stat)

        if auto_commit:
            await self.db.commit()
            await self.db.refresh(stat)

        logger.info(f"记录字数增量: chapter_id={chapter_id}, delta={delta}, edit_event_id={edit_event_id}")
        return stat

    async def sum_delta_for_author_since(self, author_id: str, since: datetime) -> int:
        """汇总作者自指定时间以来的正增量"""
        result = await self.db.execute(
            select(func.coalesce(func.sum(ChapterWordStat.delta), 0))
            .select_from(ChapterWordStat)
            .join(Chapter, Chapter.id == ChapterWordStat.chapter_id)
            .join(Work, Work.id == Chapter.work_id)
            .where(
                Work.author_id == UUID(str(author_id)),
                ChapterWordStat.created_at >= since,
                ChapterWordStat.delta > 0,  # 只计正增量
            )
        )
        return result.scalar() or 0

    async def sum_positive_delta_for_author_this_week(self, author_id: str) -> int:
        """
        汇总作者本周（自然周）的正增量

        自然周定义：周一00:00 ~ 周日23:59（中国时区 UTC+8）
        数据库存储使用 UTC，查询时需要转换
        """
        # 获取当前中国时间
        now = datetime.now(CHINA_TZ)

        # 计算本周一 00:00（中国时区）
        days_since_monday = now.weekday()  # 0=周一, 6=周日
        week_start_cn = now.replace(hour=0, minute=0, second=0, microsecond=0) - timedelta(days=days_since_monday)

        # 转换为 UTC 时间（数据库存储的是 UTC）
        week_start_utc = week_start_cn.astimezone(timezone.utc)

        logger.debug(f"统计自然周: {week_start_cn} (CN) = {week_start_utc} (UTC), author_id={author_id}")

        result = await self.db.execute(
            select(func.coalesce(func.sum(ChapterWordStat.delta), 0))
            .select_from(ChapterWordStat)
            .join(Chapter, Chapter.id == ChapterWordStat.chapter_id)
            .join(Work, Work.id == Chapter.work_id)
            .where(
                Work.author_id == UUID(str(author_id)),
                ChapterWordStat.created_at >= week_start_utc,  # 使用 UTC 时间比较
                ChapterWordStat.delta > 0,  # 只计正增量
            )
        )
        return result.scalar() or 0
