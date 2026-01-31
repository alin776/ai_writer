"""
世界观提取进度管理服务
提供进度持久化、恢复和状态管理功能
"""
import json
import logging
from datetime import datetime
from typing import Optional, Dict, Any, List
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update, delete

from app.models.worldview_progress import WorldviewExtractionProgress
from app.core.config import settings
from app.utils.datetime_utils import get_utc_now

logger = logging.getLogger(__name__)


class WorldviewProgressService:
    """世界观提取进度管理服务"""

    def __init__(self, db: AsyncSession):
        self.db = db

    async def create_progress(
        self,
        work_id: str,
        characters_total: int = 0,
        locations_total: int = 0,
        settings_total: int = 0,
        metadata: Optional[Dict[str, Any]] = None
    ) -> WorldviewExtractionProgress:
        """创建新的进度记录"""
        progress = WorldviewExtractionProgress(
            id=work_id,
            work_id=work_id,
            status="running",
            characters_total=characters_total,
            locations_total=locations_total,
            settings_total=settings_total,
            metadata_json=json.dumps(metadata) if metadata else None
        )

        self.db.add(progress)
        await self.db.commit()
        await self.db.refresh(progress)

        logger.info(f"创建世界观提取进度记录: work_id={work_id}")
        return progress

    async def get_progress(self, work_id: str) -> Optional[WorldviewExtractionProgress]:
        """获取进度记录"""
        result = await self.db.execute(
            select(WorldviewExtractionProgress).where(
                WorldviewExtractionProgress.work_id == work_id
            )
        )
        return result.scalar_one_or_none()

    async def update_phase_progress(
        self,
        work_id: str,
        phase: str,  # characters, locations, settings
        processed_count: int,
        batch_index: int,
        total_batches: int,
        results: Optional[Dict[str, int]] = None
    ) -> bool:
        """更新特定阶段的进度"""
        try:
            progress = await self.get_progress(work_id)
            if not progress:
                logger.warning(f"未找到进度记录: work_id={work_id}")
                return False

            # 更新阶段进度
            if phase == "characters":
                progress.characters_processed = processed_count
                progress.characters_batches_completed = batch_index + 1
                if results:
                    progress.characters_created += results.get("created", 0)
                    progress.characters_updated += results.get("updated", 0)
            elif phase == "locations":
                progress.locations_processed = processed_count
                progress.locations_batches_completed = batch_index + 1
                if results:
                    progress.locations_created += results.get("created", 0)
                    progress.locations_updated += results.get("updated", 0)
            elif phase == "settings":
                progress.settings_processed = processed_count
                progress.settings_batches_completed = batch_index + 1
                if results:
                    progress.settings_created += results.get("created", 0)
                    progress.settings_updated += results.get("updated", 0)

            progress.current_phase = phase
            progress.updated_at = get_utc_now()

            await self.db.commit()
            return True

        except Exception as e:
            logger.error(f"更新进度失败: work_id={work_id}, phase={phase}, error={e}")
            await self.db.rollback()
            return False

    async def update_totals(
        self,
        work_id: str,
        characters_total: int,
        locations_total: int,
        settings_total: int
    ) -> bool:
        """更新各阶段的总数"""
        try:
            progress = await self.get_progress(work_id)
            if not progress:
                return False

            progress.characters_total = characters_total
            progress.locations_total = locations_total
            progress.settings_total = settings_total
            progress.characters_batches_total = (characters_total + settings.WORLDVIEW_CHARACTER_BATCH_SIZE - 1) // settings.WORLDVIEW_CHARACTER_BATCH_SIZE
            progress.locations_batches_total = (locations_total + settings.WORLDVIEW_LOCATION_BATCH_SIZE - 1) // settings.WORLDVIEW_LOCATION_BATCH_SIZE
            progress.settings_batches_total = (settings_total + settings.WORLDVIEW_SETTING_BATCH_SIZE - 1) // settings.WORLDVIEW_SETTING_BATCH_SIZE

            await self.db.commit()
            return True

        except Exception as e:
            logger.error(f"更新总数失败: work_id={work_id}, error={e}")
            await self.db.rollback()
            return False

    async def mark_completed(self, work_id: str) -> bool:
        """标记提取完成"""
        try:
            progress = await self.get_progress(work_id)
            if not progress:
                return False

            progress.status = "completed"
            progress.completed_at = get_utc_now()
            progress.updated_at = get_utc_now()

            await self.db.commit()
            logger.info(f"世界观提取完成: work_id={work_id}")
            return True

        except Exception as e:
            logger.error(f"标记完成失败: work_id={work_id}, error={e}")
            await self.db.rollback()
            return False

    async def mark_failed(self, work_id: str, error_message: str) -> bool:
        """标记提取失败"""
        try:
            progress = await self.get_progress(work_id)
            if not progress:
                return False

            progress.status = "failed"
            progress.last_error = error_message
            progress.updated_at = get_utc_now()

            await self.db.commit()
            logger.error(f"世界观提取失败: work_id={work_id}, error={error_message}")
            return True

        except Exception as e:
            logger.error(f"标记失败失败: work_id={work_id}, error={e}")
            await self.db.rollback()
            return False

    async def add_failed_batch(
        self,
        work_id: str,
        phase: str,
        batch_index: int,
        error_message: str,
        batch_data: Optional[List[Dict[str, Any]]] = None
    ) -> bool:
        """记录失败的批次信息"""
        try:
            progress = await self.get_progress(work_id)
            if not progress:
                return False

            # 获取现有的失败批次信息
            failed_batches = []
            if progress.failed_batches:
                try:
                    failed_batches = json.loads(progress.failed_batches)
                except json.JSONDecodeError:
                    failed_batches = []

            # 添加新的失败批次
            failed_batch = {
                "phase": phase,
                "batch_index": batch_index,
                "error_message": error_message,
                "timestamp": get_utc_now().isoformat(),
                "batch_size": len(batch_data) if batch_data else 0
            }
            failed_batches.append(failed_batch)

            # 限制保存的失败批次数量
            if len(failed_batches) > 50:
                failed_batches = failed_batches[-50:]

            progress.failed_batches = json.dumps(failed_batches)
            progress.updated_at = get_utc_now()

            await self.db.commit()
            return True

        except Exception as e:
            logger.error(f"记录失败批次失败: work_id={work_id}, error={e}")
            await self.db.rollback()
            return False

    async def can_resume(self, work_id: str) -> bool:
        """检查是否可以从中断处恢复"""
        progress = await self.get_progress(work_id)
        if not progress:
            return False

        return progress.status in ["running", "failed", "paused"]

    async def get_resume_point(self, work_id: str) -> Optional[Dict[str, Any]]:
        """获取恢复点信息"""
        progress = await self.get_progress(work_id)
        if not progress:
            return None

        return {
            "work_id": work_id,
            "status": progress.status,
            "current_phase": progress.current_phase,
            "characters": {
                "total": progress.characters_total,
                "processed": progress.characters_processed,
                "next_batch": progress.characters_batches_completed
            },
            "locations": {
                "total": progress.locations_total,
                "processed": progress.locations_processed,
                "next_batch": progress.locations_batches_completed
            },
            "settings": {
                "total": progress.settings_total,
                "processed": progress.settings_processed,
                "next_batch": progress.settings_batches_completed
            },
            "results": {
                "characters": {"created": progress.characters_created, "updated": progress.characters_updated},
                "locations": {"created": progress.locations_created, "updated": progress.locations_updated},
                "settings": {"created": progress.settings_created, "updated": progress.settings_updated}
            }
        }

    async def delete_progress(self, work_id: str) -> bool:
        """删除进度记录"""
        try:
            await self.db.execute(
                delete(WorldviewExtractionProgress).where(
                    WorldviewExtractionProgress.work_id == work_id
                )
            )
            await self.db.commit()
            logger.info(f"删除进度记录: work_id={work_id}")
            return True

        except Exception as e:
            logger.error(f"删除进度记录失败: work_id={work_id}, error={e}")
            await self.db.rollback()
            return False

    async def list_all_progress(self) -> List[WorldviewExtractionProgress]:
        """列出所有进度记录"""
        result = await self.db.execute(
            select(WorldviewExtractionProgress).order_by(
                WorldviewExtractionProgress.updated_at.desc()
            )
        )
        return result.scalars().all()