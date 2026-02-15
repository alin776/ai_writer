# -*- coding: utf-8 -*-
"""
章节缓存模块

提供章节内容的缓存功能，避免 Planning 和 Execution 阶段重复读取数据库。
缓存存储在 AgentState.context["chapter_cache"] 中，跨轮次自动保留。

使用方式：
    from app.services.agent.utils.chapter_cache import ChapterCache

    # 检查缓存
    cached = ChapterCache.get_by_order(state, work_id, order=5)
    if cached:
        return cached

    # 写入缓存
    ChapterCache.set(state, chapter_data, work_id)
"""

import time
import json
import logging
from typing import Dict, Any, Optional, List

logger = logging.getLogger(__name__)

# 缓存配置
CACHE_TTL = 300  # 5分钟过期
CACHE_MAX_SIZE = 20  # 最多缓存20章


class ChapterCache:
    """章节缓存管理器"""

    @staticmethod
    def _get_cache(state: Dict[str, Any]) -> Dict[str, Any]:
        """获取缓存字典（自动初始化）"""
        if "context" not in state or not isinstance(state.get("context"), dict):
            state["context"] = {}

        context = state["context"]
        if "chapter_cache" not in context:
            context["chapter_cache"] = {}
        if "cache_stats" not in context:
            context["cache_stats"] = {"hits": 0, "misses": 0}

        return context["chapter_cache"]

    @staticmethod
    def get_by_id(state: Dict[str, Any], chapter_id: str) -> Optional[Dict[str, Any]]:
        """通过 chapter_id 获取缓存

        Args:
            state: AgentState
            chapter_id: 章节UUID

        Returns:
            缓存的章节数据（不含 cached_at），或 None（未命中/已过期）
        """
        if not chapter_id:
            return None

        cache = ChapterCache._get_cache(state)
        cached = cache.get(chapter_id)

        if cached and ChapterCache._is_valid(cached):
            stats = state["context"]["cache_stats"]
            stats["hits"] = stats.get("hits", 0) + 1
            logger.info(f"[ChapterCache] ✅ 命中: {chapter_id[:8]}... (hits={stats['hits']})")
            # 返回时移除 cached_at，保持与原始格式一致
            return {k: v for k, v in cached.items() if k != "cached_at"}

        stats = state["context"]["cache_stats"]
        stats["misses"] = stats.get("misses", 0) + 1
        return None

    @staticmethod
    def get_by_order(state: Dict[str, Any], work_id: str, order: int) -> Optional[Dict[str, Any]]:
        """通过章节序号获取缓存

        Args:
            state: AgentState
            work_id: 作品ID
            order: 章节序号

        Returns:
            缓存的章节数据，或 None
        """
        if not work_id or order < 1:
            return None

        cache = ChapterCache._get_cache(state)

        # 查找序号映射
        order_key = f"order_{work_id}_{order}"
        chapter_id = cache.get(order_key)
        if chapter_id and isinstance(chapter_id, str):
            return ChapterCache.get_by_id(state, chapter_id)

        # 遍历缓存查找
        for key, value in cache.items():
            if isinstance(value, dict) and value.get("order") == order:
                if ChapterCache._is_valid(value):
                    stats = state["context"]["cache_stats"]
                    stats["hits"] = stats.get("hits", 0) + 1
                    logger.info(f"[ChapterCache] ✅ 命中(order): 第{order}章")
                    # 返回时移除 cached_at，保持与原始格式一致
                    return {k: v for k, v in value.items() if k != "cached_at"}

        stats = state["context"]["cache_stats"]
        stats["misses"] = stats.get("misses", 0) + 1
        return None

    @staticmethod
    def set(state: Dict[str, Any], chapter_data: Dict[str, Any], work_id: str = "") -> None:
        """写入缓存

        Args:
            state: AgentState
            chapter_data: 章节数据（必须包含 chapter_id）
            work_id: 作品ID（用于序号映射）
        """
        chapter_id = chapter_data.get("chapter_id")
        if not chapter_id:
            return

        cache = ChapterCache._get_cache(state)

        # 检查大小，必要时清理
        if len(cache) >= CACHE_MAX_SIZE * 2:
            ChapterCache._evict_oldest(cache)

        # 添加时间戳并写入
        chapter_data["cached_at"] = time.time()
        cache[chapter_id] = chapter_data

        # 建立序号映射
        order = chapter_data.get("order")
        if order and work_id:
            cache[f"order_{work_id}_{order}"] = chapter_id

        logger.info(f"[ChapterCache] 📝 写入: {chapter_id[:8]}... (第{order}章)")

    @staticmethod
    def set_batch(state: Dict[str, Any], chapters: List[Dict[str, Any]], work_id: str = "") -> None:
        """批量写入缓存"""
        for chapter in chapters:
            if isinstance(chapter, dict) and "chapter_id" in chapter:
                ChapterCache.set(state, chapter, work_id)
        logger.info(f"[ChapterCache] 📝 批量写入: {len(chapters)} 章")

    @staticmethod
    def invalidate(state: Dict[str, Any], chapter_id: str) -> None:
        """使缓存失效"""
        cache = ChapterCache._get_cache(state)
        if chapter_id in cache:
            cached = cache.pop(chapter_id)
            # 删除序号映射
            if isinstance(cached, dict):
                order = cached.get("order")
                if order:
                    for key in list(cache.keys()):
                        if key.startswith("order_") and cache.get(key) == chapter_id:
                            cache.pop(key, None)
            logger.info(f"[ChapterCache] 🗑️ 失效: {chapter_id[:8]}...")

    @staticmethod
    def get_stats(state: Dict[str, Any]) -> Dict[str, int]:
        """获取缓存统计"""
        context = state.get("context", {})
        return context.get("cache_stats", {"hits": 0, "misses": 0})

    @staticmethod
    def _is_valid(cached: Dict[str, Any]) -> bool:
        """检查缓存是否有效"""
        cached_at = cached.get("cached_at", 0)
        return (time.time() - cached_at) < CACHE_TTL

    @staticmethod
    def _evict_oldest(cache: Dict[str, Any]) -> None:
        """淘汰最旧的缓存项"""
        oldest_key = None
        oldest_time = float('inf')

        for key, value in cache.items():
            if isinstance(value, dict) and "cached_at" in value:
                if value["cached_at"] < oldest_time:
                    oldest_time = value["cached_at"]
                    oldest_key = key

        if oldest_key:
            cache.pop(oldest_key, None)
            logger.info(f"[ChapterCache] 🗑️ 淘汰: {oldest_key[:8]}...")
