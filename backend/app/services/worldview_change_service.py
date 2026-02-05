"""
世界观变更回写服务

负责：pending 变更创建、查询、应用、拒绝，以及版本递增
"""
from typing import Optional, List, Dict, Any, Tuple
from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.worldview_change import WorldviewChange, WorldviewChangeStatus
from app.models.work import Work
from app.services.worldview_sync_service import WorldviewSyncService
from app.utils.datetime_utils import get_utc_now


class WorldviewChangeService:
    """世界观变更回写服务"""

    def __init__(self, db: AsyncSession, user_id: Optional[str] = None):
        self.db = db
        self.user_id = user_id

    async def create_pending_change(
        self,
        *,
        work_id: str,
        user_id: str,
        changes: Dict[str, Any],
        source: Optional[str] = "manual",
        selected_items: Optional[Dict[str, List[str]]] = None,
        evidence: Optional[Dict[str, Any]] = None,
        user_notes: Optional[str] = None
    ) -> WorldviewChange:
        work = await self._get_work(work_id)
        version_before = work.worldview_version if work else None

        change = WorldviewChange(
            work_id=work_id,
            user_id=user_id,
            status=WorldviewChangeStatus.PENDING,
            source=source or "manual",
            changes=changes,
            selected_items=selected_items,
            evidence=evidence,
            user_notes=user_notes,
            version_before=version_before
        )
        self.db.add(change)
        await self.db.commit()
        await self.db.refresh(change)
        try:
            from app.services.agent.utils.monitoring import increment_counter
            increment_counter("worldview_change_pending_total")
        except Exception:
            pass
        return change

    async def list_changes(
        self,
        *,
        work_id: str,
        status: Optional[WorldviewChangeStatus] = None,
        limit: int = 50,
        offset: int = 0
    ) -> Tuple[List[WorldviewChange], int]:
        query = select(WorldviewChange).where(WorldviewChange.work_id == work_id)
        count_query = select(func.count(WorldviewChange.id)).where(WorldviewChange.work_id == work_id)
        if status:
            query = query.where(WorldviewChange.status == status)
            count_query = count_query.where(WorldviewChange.status == status)

        query = query.order_by(WorldviewChange.created_at.desc()).limit(limit).offset(offset)
        result = await self.db.execute(query)
        items = result.scalars().all()

        count_result = await self.db.execute(count_query)
        total = count_result.scalar() or 0
        return items, total

    async def get_change_by_id(self, change_id: str) -> Optional[WorldviewChange]:
        return await self.db.get(WorldviewChange, change_id)

    async def apply_change(
        self,
        *,
        change: WorldviewChange,
        applied_by: str,
        selected_items_override: Optional[Dict[str, List[str]]] = None,
        user_notes: Optional[str] = None
    ) -> Dict[str, Any]:
        if change.status != WorldviewChangeStatus.PENDING:
            return change.apply_stats or {}

        selected_items = selected_items_override if selected_items_override is not None else change.selected_items

        sync_service = WorldviewSyncService(self.db, user_id=applied_by)
        stats = await sync_service.apply_changes(
            work_id=str(change.work_id),
            changes=change.changes or {},
            selected_items=selected_items
        )

        work = await self._get_work_for_update(str(change.work_id))
        if work:
            version_before = work.worldview_version or 1
            work.worldview_version = version_before + 1
            change.version_before = version_before
            change.version_after = work.worldview_version

        change.status = WorldviewChangeStatus.APPLIED
        change.applied_by = applied_by
        change.applied_at = get_utc_now()
        change.apply_stats = stats
        if selected_items_override is not None:
            change.selected_items = selected_items_override
        if user_notes:
            change.user_notes = user_notes

        await self.db.commit()
        await self.db.refresh(change)
        try:
            from app.services.agent.utils.monitoring import increment_counter
            increment_counter("worldview_change_applied_total")
        except Exception:
            pass
        return stats

    async def reject_change(
        self,
        *,
        change: WorldviewChange,
        user_notes: Optional[str] = None
    ) -> WorldviewChange:
        if change.status == WorldviewChangeStatus.REJECTED:
            return change

        change.status = WorldviewChangeStatus.REJECTED
        if user_notes:
            change.user_notes = user_notes
        await self.db.commit()
        await self.db.refresh(change)
        try:
            from app.services.agent.utils.monitoring import increment_counter
            increment_counter("worldview_change_rejected_total")
        except Exception:
            pass
        return change

    async def _get_work(self, work_id: str) -> Optional[Work]:
        result = await self.db.execute(
            select(Work).where(Work.id == work_id)
        )
        return result.scalar_one_or_none()

    async def _get_work_for_update(self, work_id: str) -> Optional[Work]:
        result = await self.db.execute(
            select(Work).where(Work.id == work_id).with_for_update()
        )
        return result.scalar_one_or_none()
