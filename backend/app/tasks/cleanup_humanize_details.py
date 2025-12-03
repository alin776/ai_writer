"""
定时清理任务 - 清理过期的去痕迹会话详情数据

使用 APScheduler 实现定时任务,每天凌晨执行
"""

import logging
from datetime import datetime, timedelta
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import delete
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger

from app.models.humanize_session import HumanizeSessionDetail
from app.core.database import async_session_maker
from app.utils.datetime_utils import get_utc_now

logger = logging.getLogger(__name__)


async def cleanup_expired_humanize_details():
    """
    清理过期的去痕迹会话详情数据

    删除所有 expires_at < 当前时间的记录
    """
    logger.info("开始清理过期的去痕迹会话详情数据...")

    try:
        async with async_session_maker() as db:
            # 删除过期的详情数据
            result = await db.execute(
                delete(HumanizeSessionDetail)
                .where(HumanizeSessionDetail.expires_at < get_utc_now())
            )

            deleted_count = result.rowcount
            await db.commit()

            logger.info(f"清理完成,共删除 {deleted_count} 条过期记录")

    except Exception as e:
        logger.error(f"清理过期数据失败: {e}")


async def cleanup_old_humanize_details(days: int = 30):
    """
    清理指定天数之前的详情数据 (手动调用)

    Args:
        days: 保留最近多少天的数据
    """
    logger.info(f"开始清理 {days} 天前的去痕迹会话详情数据...")

    try:
        async with async_session_maker() as db:
            cutoff_date = get_utc_now() - timedelta(days=days)

            result = await db.execute(
                delete(HumanizeSessionDetail)
                .where(HumanizeSessionDetail.created_at < cutoff_date)
            )

            deleted_count = result.rowcount
            await db.commit()

            logger.info(f"清理完成,共删除 {deleted_count} 条记录")

    except Exception as e:
        logger.error(f"清理旧数据失败: {e}")


# ========== APScheduler 调度器配置 ==========

scheduler = AsyncIOScheduler()


async def start_scheduler():
    """
    启动定时任务调度器
    """
    # 每天凌晨 2:00 执行清理任务
    scheduler.add_job(
        cleanup_expired_humanize_details,
        trigger=CronTrigger(hour=2, minute=0),
        id="cleanup_humanize_details",
        name="清理过期的去痕迹会话详情",
        replace_existing=True
    )

    scheduler.start()
    logger.info("定时任务调度器已启动")


async def stop_scheduler():
    """
    停止定时任务调度器
    """
    if scheduler.running:
        scheduler.shutdown(wait=False)
        logger.info("定时任务调度器已停止")
