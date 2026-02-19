"""
定时任务模块 & Celery异步任务模块
"""

from app.services.channel_scheduler import init_scheduler as init_channel_scheduler, start_scheduler as start_channel_scheduler, shutdown_scheduler as shutdown_channel_scheduler

def start_scheduler():
    """启动所有调度器"""
    init_channel_scheduler()
    start_channel_scheduler()

def stop_scheduler():
    """停止所有调度器"""
    shutdown_channel_scheduler()

# Celery异步任务将在 Phase 4 添加
# from app.tasks.review_tasks import async_review_work

__all__ = ["start_scheduler", "stop_scheduler"]
