"""
定时任务 - 清理过期的去痕迹会话详情 & Agent 会话
"""

import logging
from datetime import datetime, timedelta
from sqlalchemy import delete
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger

from app.models.humanize_session import HumanizeSessionDetail
from app.models.agent_session import AgentSession
from app.core.database import async_session_maker

logger = logging.getLogger(__name__)


async def cleanup_expired_humanize_details():
  """
  删除所有 expires_at < now 的去痕迹会话详情
  """
  logger.info("开始清理过期的去痕迹会话详情...")
  try:
    async with async_session_maker() as db:
      result = await db.execute(
        delete(HumanizeSessionDetail).where(HumanizeSessionDetail.expires_at < datetime.utcnow())
      )
      deleted_count = result.rowcount or 0
      await db.commit()
      logger.info(f"清理完成, 共删除 {deleted_count} 条过期记录")
  except Exception as e:
    logger.error(f"清理过期数据失败: {e}")


async def cleanup_expired_agent_sessions():
  """
  删除所有 expires_at < now 的 Agent 会话
  """
  logger.info("开始清理过期的 Agent 会话...")
  try:
    async with async_session_maker() as db:
      result = await db.execute(
        delete(AgentSession).where(
          AgentSession.expires_at.isnot(None),
          AgentSession.expires_at < datetime.utcnow()
        )
      )
      deleted_count = result.rowcount or 0
      await db.commit()
      logger.info(f"清理完成, 共删除 {deleted_count} 条过期会话")
  except Exception as e:
    logger.error(f"清理过期 Agent 会话失败: {e}")


async def cleanup_old_humanize_details(days: int = 30):
  """
  手动清理指定天数前的去痕迹会话详情
  """
  logger.info(f"开始清理 {days} 天前的去痕迹会话详情...")
  try:
    async with async_session_maker() as db:
      cutoff_date = datetime.utcnow() - timedelta(days=days)
      result = await db.execute(
        delete(HumanizeSessionDetail).where(HumanizeSessionDetail.created_at < cutoff_date)
      )
      deleted_count = result.rowcount or 0
      await db.commit()
      logger.info(f"清理完成, 共删除 {deleted_count} 条记录")
  except Exception as e:
    logger.error(f"清理旧数据失败: {e}")


# ========== APScheduler 调度器 ==========

scheduler = AsyncIOScheduler()


async def start_scheduler():
  """
  启动定时任务调度器
  """
  scheduler.add_job(
    cleanup_expired_humanize_details,
    trigger=CronTrigger(hour=2, minute=0),
    id="cleanup_humanize_details",
    name="清理过期的去痕迹会话详情",
    replace_existing=True,
  )
  scheduler.add_job(
    cleanup_expired_agent_sessions,
    trigger=CronTrigger(hour=3, minute=0),
    id="cleanup_agent_sessions",
    name="清理过期的 Agent 会话",
    replace_existing=True,
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
