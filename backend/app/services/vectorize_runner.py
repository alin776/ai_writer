"""
导入章节向量化执行器
用于 BackgroundTasks / Celery 复用
"""
import logging

from app.core.database import async_session_maker
from app.services.chapter_vector_service import ChapterVectorService

logger = logging.getLogger(__name__)


async def run_vectorize_chapter(
    work_id: str,
    chapter_id: str,
    chapter_order: int,
    chapter_title: str,
    content: str
) -> None:
    """执行单章向量化"""
    try:
        async with async_session_maker() as db_session:
            service = ChapterVectorService(db_session)
            await service.store_chapter_vector(
                work_id=work_id,
                chapter_id=chapter_id,
                chapter_order=chapter_order,
                chapter_title=chapter_title,
                content=content
            )
    except Exception as e:
        logger.error(
            f"导入章节向量化失败（后台任务）: work_id={work_id}, chapter_id={chapter_id}, error={e}",
            exc_info=True
        )
