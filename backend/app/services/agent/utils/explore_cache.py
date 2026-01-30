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
    try:
        return await RedisClient.delete_pattern(pattern)
    except Exception as exc:
        logger.debug(f"[ExploreCache] Failed to invalidate cache: {exc}")
        return 0
