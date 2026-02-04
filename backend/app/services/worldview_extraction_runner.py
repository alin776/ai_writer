"""
世界观解析后台任务执行器
用于 BackgroundTasks / Celery 复用
"""
import logging
from typing import Optional, List

from app.core.database import async_session_maker
from app.services.worldview_sync_service import WorldviewSyncService
from app.services.worldview_scan_progress_service import WorldviewScanProgressService

logger = logging.getLogger(__name__)


async def run_worldview_extraction(
    work_id: str,
    user_id: str,
    scan_mode: str = "incremental",
    chapter_ids: Optional[List[str]] = None,
    preface_text: Optional[str] = None
) -> None:
    """执行世界观解析任务（可由 Celery/BackgroundTasks 调用）"""
    try:
        logger.info(f"[世界观提取] 开始为作品 {work_id} 提取世界观")

        async with async_session_maker() as db_session:
            sync_service = WorldviewSyncService(db_session, user_id=user_id)
            progress_service = WorldviewScanProgressService(db_session)

            if scan_mode == "full":
                chapters = await sync_service.get_chapters_by_work(work_id)
            else:
                chapters = await sync_service.get_chapters_by_ids(work_id, chapter_ids or [])

            chapters_total = len(chapters)
            await progress_service.start_progress(
                work_id=work_id,
                scan_mode=scan_mode,
                chapters_total=chapters_total,
                batches_total=0,
                status="preparing",
                metadata={
                    "chapter_ids": chapter_ids or [],
                    "preface_included": bool(preface_text)
                }
            )

            if not chapters and not preface_text:
                await progress_service.mark_completed(work_id)
                logger.info(f"[世界观提取] 未找到可解析的章节")
                return

            async def progress_callback(chapters_processed: int, chapters_total: int, batches_completed: int, batches_total: int):
                await progress_service.update_progress(
                    work_id=work_id,
                    chapters_processed=chapters_processed,
                    chapters_total=chapters_total,
                    batches_completed=batches_completed,
                    batches_total=batches_total
                )

            async def status_callback(status: str):
                await progress_service.update_status(work_id=work_id, status=status)

            changes, scan_meta = await sync_service.scan_chapters_for_changes_by_ids(
                work_id=work_id,
                chapter_ids=[str(ch.id) for ch in chapters],
                preface_text=preface_text,
                progress_callback=progress_callback,
                status_callback=status_callback
            )

            scanned = changes.get("scanned_chapters", 0)
            new_chars = len(changes.get("new_characters", []))
            updated_chars = len(changes.get("updated_characters", []))
            new_locs = len(changes.get("new_locations", []))
            new_sets = len(changes.get("new_settings", []))
            rel_changes = len(changes.get("relationship_changes", []))

            logger.info(f"[世界观提取] 扫描完成: {scanned}章, 发现 {new_chars}人物, {new_locs}地点, {new_sets}设定")

            if new_chars > 0 or updated_chars > 0 or new_locs > 0 or new_sets > 0 or rel_changes > 0:
                await progress_service.update_status(work_id=work_id, status="applying")
                stats = await sync_service.apply_changes(work_id, changes)
                await progress_service.update_results(work_id, stats)
                logger.info(f"[世界观提取] 应用完成: {stats}")
            else:
                logger.info(f"[世界观提取] 未发现新的世界观元素")
                await progress_service.update_results(work_id, {})

            await progress_service.mark_completed(
                work_id,
                extra={"scanned_chapters": scanned, **(scan_meta or {})}
            )
    except Exception as e:
        logger.error(f"[世界观提取] 提取失败: work_id={work_id}, error={e}", exc_info=True)
        try:
            async with async_session_maker() as db_session:
                await WorldviewScanProgressService(db_session).mark_failed(work_id, str(e))
        except Exception:
            logger.error(f"[世界观提取] 记录失败状态失败: work_id={work_id}", exc_info=True)
