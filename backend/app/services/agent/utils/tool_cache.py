# -*- coding: utf-8 -*-
"""
Tool cache helpers.

Provides a Redis-backed cache with an in-memory fallback for tool results.
"""

from dataclasses import dataclass
from typing import Any, Dict, Optional
import hashlib
import json
import logging

from app.core.redis_client import redis_client
from app.core.config import settings
from app.services.agent.utils.performance import MemoryCache

logger = logging.getLogger(__name__)

TOOL_CACHE_PREFIX = "tool_cache"

# Tools that are cacheable by default (normalized tool names).
CACHEABLE_TOOLS = {
    "get_writing_context",
    "locate_content",
    "search_content",
    "search_analysis_fragments",
}

# Alias tools that should share cache policy with get_writing_context.
TOOL_ALIASES = {
    "read_chapter": "get_writing_context",
    "get_chapter_by_order": "get_writing_context",
    "get_context": "get_writing_context",
    "get_worldview_summary": "get_writing_context",
}

# TTL mapping (seconds) for non-aggregated tools.
TOOL_TTL_SECONDS = {
    "locate_content": 5 * 60,
    "search_content": 2 * 60,
    "search_analysis_fragments": 2 * 60,
}

# Volatile params that should not affect cache keys.
VOLATILE_ARG_KEYS = {
    "conversation_id",
    "request_id",
    "trace_id",
    "task_id",
    "session_id",
    "timestamp",
    "ts",
    "time",
    "use_cache",
}

# Local fallback cache when Redis is unavailable.
_local_cache = MemoryCache(max_size=2000, default_ttl=3600)


def _load_cache_whitelist() -> set:
    raw_value = getattr(settings, "TOOL_CACHE_WHITELIST", "") or ""
    if not isinstance(raw_value, str):
        return set(CACHEABLE_TOOLS)
    items = {item.strip() for item in raw_value.split(",") if item.strip()}
    return items or set(CACHEABLE_TOOLS)


def _load_tool_ttl_minutes() -> Dict[str, int]:
    raw_value = getattr(settings, "TOOL_CACHE_TTL_MINUTES", "") or ""
    if not isinstance(raw_value, str) or not raw_value.strip():
        return {k: v // 60 for k, v in TOOL_TTL_SECONDS.items()}

    mapping: Dict[str, int] = {}
    for token in raw_value.split(","):
        token = token.strip()
        if not token or "=" not in token:
            continue
        key, value = token.split("=", 1)
        key = key.strip()
        value = value.strip()
        if not key or not value:
            continue
        try:
            mapping[key] = int(float(value))
        except ValueError:
            continue

    if not mapping:
        return {k: v // 60 for k, v in TOOL_TTL_SECONDS.items()}
    return mapping


def _load_gwc_ttl_minutes() -> Dict[str, int]:
    raw_value = getattr(settings, "TOOL_CACHE_GWC_TTL_MINUTES", "") or ""
    default_mapping = {
        "default": 3,
        "chapter": 5,
        "rag": 2,
        "worldview": 30,
        "work": 10,
        "style": 30,
    }
    if not isinstance(raw_value, str) or not raw_value.strip():
        return default_mapping

    mapping = dict(default_mapping)
    for token in raw_value.split(","):
        token = token.strip()
        if not token or "=" not in token:
            continue
        key, value = token.split("=", 1)
        key = key.strip()
        value = value.strip()
        if not key or not value:
            continue
        try:
            mapping[key] = int(float(value))
        except ValueError:
            continue
    return mapping


_CACHE_WHITELIST = _load_cache_whitelist()
_TOOL_TTL_MINUTES = _load_tool_ttl_minutes()
_GWC_TTL_MINUTES = _load_gwc_ttl_minutes()


@dataclass(frozen=True)
class ToolCacheContext:
    key: str
    ttl_seconds: int


class ToolCache:
    """Unified tool cache helpers."""

    @staticmethod
    def get_context(tool_name: str, params: Dict[str, Any], state: Dict[str, Any]) -> Optional[ToolCacheContext]:
        if not ToolCache._should_cache(tool_name, params):
            return None

        work_id = _resolve_work_id(params, state)
        if not work_id:
            return None

        user_id = _resolve_user_id(params, state) or "anonymous"
        scope = _resolve_scope(params)
        ttl_seconds = ToolCache._get_ttl_seconds(tool_name, params)
        if not ttl_seconds:
            return None

        args_hash = _hash_tool_args(tool_name, params)
        cache_key = f"{TOOL_CACHE_PREFIX}:{user_id}:{work_id}:{scope}:{tool_name}:{args_hash}"
        return ToolCacheContext(key=cache_key, ttl_seconds=ttl_seconds)

    @staticmethod
    def read(cache_ctx: ToolCacheContext) -> Optional[str]:
        if redis_client.is_available():
            cached = redis_client.get(cache_ctx.key)
            if cached is not None:
                logger.info(f"[ToolCache] hit: {cache_ctx.key}")
                return cached
            logger.debug(f"[ToolCache] miss: {cache_ctx.key}")
            return None

        cached = _local_cache.get(cache_ctx.key)
        if cached is not None:
            logger.info(f"[ToolCache] hit(local): {cache_ctx.key}")
            return cached
        logger.debug(f"[ToolCache] miss(local): {cache_ctx.key}")
        return None

    @staticmethod
    def write(cache_ctx: ToolCacheContext, value: str) -> None:
        if redis_client.is_available():
            success = redis_client.set(cache_ctx.key, value, cache_ctx.ttl_seconds)
            if not success:
                logger.warning(f"[ToolCache] write failed: {cache_ctx.key}")
            return

        _local_cache.set(cache_ctx.key, value, ttl=cache_ctx.ttl_seconds)

    @staticmethod
    def invalidate(
        work_id: Optional[str],
        chapter_id: Optional[str] = None,
        include_work_scope: bool = False,
        include_multi_scope: bool = True,
    ) -> int:
        if not work_id:
            return 0

        patterns = []
        if chapter_id:
            patterns.append(f"{TOOL_CACHE_PREFIX}:*:{work_id}:chapter:{chapter_id}:*")
            if include_multi_scope:
                patterns.append(f"{TOOL_CACHE_PREFIX}:*:{work_id}:chapters:*")
                patterns.append(f"{TOOL_CACHE_PREFIX}:*:{work_id}:chapter_order:*")
        if include_work_scope:
            patterns.append(f"{TOOL_CACHE_PREFIX}:*:{work_id}:work:*")

        if not patterns:
            return 0

        if not redis_client.is_available():
            _local_cache.clear()
            logger.info("[ToolCache] local cache cleared (no redis)")
            return 0

        deleted = 0
        for pattern in patterns:
            try:
                keys = redis_client.client.keys(pattern)
                if keys:
                    redis_client.client.delete(*keys)
                    deleted += len(keys)
                    logger.info(f"[ToolCache] invalidated {len(keys)} keys: {pattern}")
            except Exception as exc:
                logger.warning(f"[ToolCache] invalidation failed: {pattern} ({exc})")
        return deleted

    @staticmethod
    def _should_cache(tool_name: str, params: Dict[str, Any]) -> bool:
        if not getattr(settings, "TOOL_CACHE_ENABLED", True):
            return False
        if params.get("use_cache") is False:
            return False
        canonical = TOOL_ALIASES.get(tool_name, tool_name)
        return canonical in _CACHE_WHITELIST

    @staticmethod
    def _get_ttl_seconds(tool_name: str, params: Dict[str, Any]) -> int:
        canonical = TOOL_ALIASES.get(tool_name, tool_name)
        if canonical == "get_writing_context":
            return _get_writing_context_ttl_seconds(params)
        minutes = _TOOL_TTL_MINUTES.get(canonical)
        if minutes is None:
            return TOOL_TTL_SECONDS.get(canonical, 0)
        return max(minutes, 0) * 60


def _get_writing_context_ttl_seconds(params: Dict[str, Any]) -> int:
    include_set = _normalize_include_set(params.get("include"))
    if include_set == {"chapter"}:
        return max(_GWC_TTL_MINUTES.get("chapter", 5), 0) * 60
    if include_set == {"worldview"}:
        return max(_GWC_TTL_MINUTES.get("worldview", 30), 0) * 60
    if include_set == {"work"}:
        return max(_GWC_TTL_MINUTES.get("work", 10), 0) * 60
    if include_set == {"style"}:
        return max(_GWC_TTL_MINUTES.get("style", 30), 0) * 60
    if include_set == {"rag"}:
        return max(_GWC_TTL_MINUTES.get("rag", 2), 0) * 60
    return max(_GWC_TTL_MINUTES.get("default", 3), 0) * 60


def _resolve_work_id(params: Dict[str, Any], state: Dict[str, Any]) -> str:
    work_id = params.get("work_id") or state.get("work_id") or ""
    return str(work_id).strip()


def _resolve_user_id(params: Dict[str, Any], state: Dict[str, Any]) -> str:
    user_id = params.get("user_id") or state.get("user_id") or ""
    return str(user_id).strip()


def _resolve_scope(params: Dict[str, Any]) -> str:
    chapter_id = str(params.get("chapter_id") or "").strip()
    if chapter_id:
        return f"chapter:{chapter_id}"

    chapter_orders = str(params.get("chapter_orders") or "").strip()
    if chapter_orders:
        orders = _parse_chapter_orders(chapter_orders)
        if len(orders) == 1:
            return f"chapter_order:{orders[0]}"
        return "chapters"

    return "work"


def _hash_tool_args(tool_name: str, params: Dict[str, Any]) -> str:
    normalized = _normalize_tool_args(tool_name, params)
    payload = json.dumps(normalized, sort_keys=True, ensure_ascii=True, separators=(",", ":"))
    return hashlib.md5(payload.encode("utf-8")).hexdigest()[:16]


def _normalize_tool_args(tool_name: str, params: Dict[str, Any]) -> Dict[str, Any]:
    normalized: Dict[str, Any] = {}
    for key, value in params.items():
        if key in VOLATILE_ARG_KEYS:
            continue
        if key == "include":
            normalized[key] = _normalize_include_value(value)
            continue
        if key == "chapter_orders":
            normalized[key] = str(value).replace(" ", "")
            continue
        normalized[key] = _normalize_value(value)
    return normalized


def _normalize_value(value: Any) -> Any:
    if isinstance(value, dict):
        return {str(k): _normalize_value(v) for k, v in sorted(value.items(), key=lambda x: str(x[0]))}
    if isinstance(value, (list, tuple)):
        return [_normalize_value(v) for v in value]
    if isinstance(value, set):
        return sorted(_normalize_value(v) for v in value)
    if value is None:
        return None
    if isinstance(value, (str, int, float, bool)):
        return value
    return str(value)


def _normalize_include_value(include_value: Any) -> str:
    return ",".join(sorted(_normalize_include_set(include_value)))


def _normalize_include_set(include_value: Any) -> set:
    if include_value is None:
        return set()
    if isinstance(include_value, str):
        items = [item.strip() for item in include_value.split(",") if item.strip()]
        return set(items)
    if isinstance(include_value, (list, tuple, set)):
        return set(str(item).strip() for item in include_value if str(item).strip())
    return set([str(include_value).strip()])


def _parse_chapter_orders(chapter_orders: str) -> list:
    chapter_orders = str(chapter_orders).strip()
    if not chapter_orders:
        return []
    if "-" in chapter_orders and "," not in chapter_orders:
        parts = chapter_orders.split("-")
        if len(parts) == 2:
            try:
                start = int(parts[0].strip())
                end = int(parts[1].strip())
                if start <= end:
                    return list(range(start, end + 1))
            except ValueError:
                return []
    if "," in chapter_orders:
        orders = []
        for part in chapter_orders.split(","):
            try:
                orders.append(int(part.strip()))
            except ValueError:
                continue
        return sorted(set(orders))
    try:
        return [int(chapter_orders)]
    except ValueError:
        return []
