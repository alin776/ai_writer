"""
世界观扫描进度管理服务（导入解析）
"""
import json
import logging
from datetime import datetime
from typing import Optional, Dict, Any
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.models.worldview_scan_progress import WorldviewScanProgress
from app.utils.datetime_utils import get_utc_now

logger = logging.getLogger(__name__)


class WorldviewScanProgressService:
    """世界观扫描进度服务"""

    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_progress(self, work_id: str) -> Optional[WorldviewScanProgress]:
        result = await self.db.execute(
            select(WorldviewScanProgress).where(WorldviewScanProgress.work_id == work_id)
        )
        return result.scalar_one_or_none()

    async def start_progress(
        self,
        work_id: str,
        scan_mode: str,
        chapters_total: int,
        batches_total: int = 0,
        metadata: Optional[Dict[str, Any]] = None
    ) -> WorldviewScanProgress:
        progress = await self.get_progress(work_id)
        if not progress:
            progress = WorldviewScanProgress(
                id=work_id,
                work_id=work_id,
                status="running",
                scan_mode=scan_mode,
                chapters_total=chapters_total,
                chapters_processed=0,
                batches_total=batches_total,
                batches_completed=0,
                metadata_json=json.dumps(metadata) if metadata else None
            )
            self.db.add(progress)
        else:
            progress.status = "running"
            progress.scan_mode = scan_mode
            progress.chapters_total = chapters_total
            progress.chapters_processed = 0
            progress.batches_total = batches_total
            progress.batches_completed = 0
            progress.characters_created = 0
            progress.characters_updated = 0
            progress.locations_created = 0
            progress.locations_updated = 0
            progress.settings_created = 0
            progress.settings_updated = 0
            progress.relationships_created = 0
            progress.last_error = None
            progress.metadata_json = json.dumps(metadata) if metadata else None
            progress.updated_at = get_utc_now()
            progress.completed_at = None

        await self.db.commit()
        await self.db.refresh(progress)
        return progress

    async def update_progress(
        self,
        work_id: str,
        chapters_processed: int,
        chapters_total: int,
        batches_completed: int,
        batches_total: int
    ) -> bool:
        try:
            progress = await self.get_progress(work_id)
            if not progress:
                return False

            progress.chapters_processed = chapters_processed
            progress.chapters_total = chapters_total
            progress.batches_completed = batches_completed
            progress.batches_total = batches_total
            progress.updated_at = get_utc_now()

            await self.db.commit()
            return True
        except Exception as e:
            logger.error(f"更新扫描进度失败: work_id={work_id}, error={e}")
            await self.db.rollback()
            return False

    async def update_results(self, work_id: str, stats: Dict[str, int]) -> bool:
        try:
            progress = await self.get_progress(work_id)
            if not progress:
                return False

            progress.characters_created = stats.get("characters_created", progress.characters_created)
            progress.characters_updated = stats.get("characters_updated", progress.characters_updated)
            progress.locations_created = stats.get("locations_created", progress.locations_created)
            progress.locations_updated = stats.get("locations_updated", progress.locations_updated)
            progress.settings_created = stats.get("settings_created", progress.settings_created)
            progress.settings_updated = stats.get("settings_updated", progress.settings_updated)
            progress.relationships_created = stats.get("relationships_created", progress.relationships_created)
            progress.updated_at = get_utc_now()

            await self.db.commit()
            return True
        except Exception as e:
            logger.error(f"更新扫描结果失败: work_id={work_id}, error={e}")
            await self.db.rollback()
            return False

    async def mark_completed(self, work_id: str, extra: Optional[Dict[str, Any]] = None) -> bool:
        try:
            progress = await self.get_progress(work_id)
            if not progress:
                return False

            progress.status = "completed"
            progress.completed_at = get_utc_now()
            progress.updated_at = get_utc_now()

            if extra:
                try:
                    metadata = json.loads(progress.metadata_json) if progress.metadata_json else {}
                except json.JSONDecodeError:
                    metadata = {}
                metadata.update(extra)
                progress.metadata_json = json.dumps(metadata)

            await self.db.commit()
            return True
        except Exception as e:
            logger.error(f"标记扫描完成失败: work_id={work_id}, error={e}")
            await self.db.rollback()
            return False

    async def mark_failed(self, work_id: str, error_message: str) -> bool:
        try:
            progress = await self.get_progress(work_id)
            if not progress:
                progress = WorldviewScanProgress(
                    id=work_id,
                    work_id=work_id,
                    status="failed",
                    last_error=error_message
                )
                self.db.add(progress)
            else:
                progress.status = "failed"
                progress.last_error = error_message
                progress.updated_at = get_utc_now()

            await self.db.commit()
            return True
        except Exception as e:
            logger.error(f"标记扫描失败失败: work_id={work_id}, error={e}")
            await self.db.rollback()
            return False
