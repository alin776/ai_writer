"""
Debounced knowledge->worldview sync scheduler.

Goal:
- Keep knowledge updates timely (trailing sync after a quiet window)
- Avoid syncing on every tiny edit burst
"""

from __future__ import annotations

import asyncio
import logging
import time
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Optional

from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import settings
from app.core.database import create_db_session
from app.services.worldview_knowledge_bridge import WorldviewKnowledgeBridge

logger = logging.getLogger(__name__)


@dataclass
class _SyncState:
    lock: asyncio.Lock = field(default_factory=asyncio.Lock)
    pending_paths: set[str] = field(default_factory=set)
    pending_events: int = 0
    last_synced_at: float = 0.0
    timer_task: Optional[asyncio.Task] = None


_states: dict[str, _SyncState] = {}
_states_lock = asyncio.Lock()


def _normalize_rel_path(path: str) -> str:
    rel = (path or "").strip().replace("\\", "/")
    while rel.startswith("./"):
        rel = rel[2:]
    return rel.lstrip("/")


def _debounce_seconds() -> int:
    return max(0, int(settings.WORLDVIEW_KNOWLEDGE_SYNC_DEBOUNCE_SECONDS))


def _batch_limit() -> int:
    return max(1, int(settings.WORLDVIEW_KNOWLEDGE_SYNC_BATCH_LIMIT))


async def _get_state(work_id: str) -> _SyncState:
    async with _states_lock:
        state = _states.get(work_id)
        if state is None:
            state = _SyncState()
            _states[work_id] = state
        return state


async def _run_sync_once(
    *,
    work_id: str,
    work_dir: Path,
    touched_paths: list[str],
    sync_mode: str,
    db: Optional[AsyncSession] = None,
) -> dict[str, Any]:
    if not touched_paths:
        return {"status": "skipped", "reason": "no_touched_paths"}

    if db is not None:
        bridge = WorldviewKnowledgeBridge(db)
        result = await bridge.sync_cards_from_knowledge(
            work_id=work_id,
            touched_paths=touched_paths,
            work_dir=work_dir,
            sync_mode=sync_mode,
        )
    else:
        async with create_db_session() as session:
            bridge = WorldviewKnowledgeBridge(session)
            result = await bridge.sync_cards_from_knowledge(
                work_id=work_id,
                touched_paths=touched_paths,
                work_dir=work_dir,
                sync_mode=sync_mode,
            )

    payload = dict(result)
    payload["status"] = "synced"
    payload["touched_paths"] = touched_paths
    return payload


async def _delayed_sync_task(work_id: str, work_dir: Path, sync_mode: str, delay_seconds: float) -> None:
    try:
        if delay_seconds > 0:
            await asyncio.sleep(delay_seconds)
    except asyncio.CancelledError:
        return

    state = await _get_state(work_id)

    async with state.lock:
        touched_paths = sorted(state.pending_paths)
        state.pending_paths.clear()
        state.pending_events = 0

    if not touched_paths:
        async with state.lock:
            state.timer_task = None
        return

    try:
        await _run_sync_once(
            work_id=work_id,
            work_dir=work_dir,
            touched_paths=touched_paths,
            sync_mode=sync_mode,
            db=None,
        )
    except Exception as exc:
        logger.warning("[knowledge_sync_scheduler] delayed sync failed for work=%s: %s", work_id, exc)
    finally:
        async with state.lock:
            state.last_synced_at = time.monotonic()
            state.timer_task = None
            # If new changes arrived while syncing, schedule another trailing run.
            if state.pending_paths:
                state.timer_task = asyncio.create_task(
                    _delayed_sync_task(work_id, work_dir, sync_mode, _debounce_seconds())
                )


async def request_worldview_sync(
    *,
    db: Optional[AsyncSession],
    work_id: str,
    work_dir: Path,
    touched_paths: list[str],
    sync_mode: str,
) -> Optional[dict[str, Any]]:
    """
    Debounced entrypoint for knowledge->worldview synchronization.

    Returns:
    - None: no tracked path touched
    - dict: sync result or queued status
    """
    normalized = [_normalize_rel_path(path) for path in (touched_paths or []) if path]
    if not WorldviewKnowledgeBridge.has_tracked_path(normalized):
        return None

    state = await _get_state(work_id)
    debounce = _debounce_seconds()
    batch_limit = _batch_limit()
    now = time.monotonic()

    run_now_paths: Optional[list[str]] = None

    async with state.lock:
        state.pending_paths.update(normalized)
        state.pending_events += 1

        if state.last_synced_at <= 0:
            elapsed = float("inf")
        else:
            elapsed = now - state.last_synced_at

        should_run_now = (
            debounce == 0
            or elapsed >= debounce
            or state.pending_events >= batch_limit
        )

        if should_run_now:
            run_now_paths = sorted(state.pending_paths)
            state.pending_paths.clear()
            state.pending_events = 0
            if state.timer_task and not state.timer_task.done():
                state.timer_task.cancel()
            state.timer_task = None
        else:
            due_in = max(0.0, debounce - elapsed)
            if state.timer_task is None or state.timer_task.done():
                state.timer_task = asyncio.create_task(
                    _delayed_sync_task(work_id, work_dir, sync_mode, due_in)
                )
            return {
                "status": "queued",
                "reason": "debounced",
                "due_in_seconds": round(due_in, 2),
                "pending_events": state.pending_events,
                "tracked_paths": sorted(state.pending_paths),
            }

    if not run_now_paths:
        return {
            "status": "queued",
            "reason": "empty",
            "pending_events": 0,
        }

    try:
        result = await _run_sync_once(
            work_id=work_id,
            work_dir=work_dir,
            touched_paths=run_now_paths,
            sync_mode=sync_mode,
            db=db,
        )
    finally:
        async with state.lock:
            state.last_synced_at = time.monotonic()

    return result

