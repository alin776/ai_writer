"""
Explore result cache invalidation helpers.

Provide a single entry to clear explore_content result caches after chapter updates.
"""

from typing import Optional
import logging

from app.core.redis import RedisClient

logger = logging.getLogger(__name__)

EXPLORE_RESULT_CACHE_PREFIX = "explore:result"


async def invalidate_explore_result_cache(work_id: str) -> int:
    """Clear explore_content result caches for a work."""
    work_id = str(work_id or "").strip()
    if not work_id:
        return 0
    pattern = f"{EXPLORE_RESULT_CACHE_PREFIX}:*:{work_id}:*"
    deleted = 0
    try:
        deleted = await RedisClient.delete_pattern(pattern)
    except Exception as exc:
        logger.debug(f"[ExploreCache] Failed to invalidate cache: {exc}")
        deleted = 0

    # 同步清理 Explore Artifact（落盘结果）
    try:
        from app.services.agent.utils.explore_artifact import invalidate_explore_artifacts
        deleted += await invalidate_explore_artifacts(work_id)
    except Exception as exc:
        logger.debug(f"[ExploreCache] Failed to invalidate artifacts: {exc}")

    return deleted
