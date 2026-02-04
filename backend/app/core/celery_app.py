"""
Celery异步任务配置

功能:
- 作品级评审异步处理
- 定时清理任务
- 批量导出任务
"""

from celery import Celery
from kombu import Queue
from app.core.config import settings

# 从 REDIS_URL 构建 Celery broker URL
# 使用不同的 db: broker=1, backend=2
redis_url = settings.REDIS_URL.replace("/0", "")  # 移除 /0

celery_app = Celery(
    'novel_review',
    broker=f'{redis_url}/1',  # 使用 db 1 作为消息队列
    backend=f'{redis_url}/2'  # 使用 db 2 作为结果存储
)

# Celery配置
celery_app.conf.update(
    task_serializer='json',
    accept_content=['json'],
    result_serializer='json',
    timezone='Asia/Shanghai',
    enable_utc=True,
    task_track_started=True,
    task_time_limit=3600,  # 任务最长1小时
    result_expires=86400,  # 结果保留24小时
    worker_prefetch_multiplier=1,  # 每次只取一个任务
    worker_max_tasks_per_child=50,  # 每个worker执行50个任务后重启
    task_queues=(
        Queue('worldview', routing_key='worldview'),
        Queue('vectorize', routing_key='vectorize'),
    ),
    task_routes={
        'import.extract_worldview': {'queue': 'worldview', 'routing_key': 'worldview'},
        'import.vectorize_chapter': {'queue': 'vectorize', 'routing_key': 'vectorize'},
    }
)

# 自动发现任务
celery_app.autodiscover_tasks(['app.tasks'])
