"""
Redis降级处理模块 (修复P0-8)

统一的Redis故障降级策略，确保系统在Redis不可用时仍能正常运行。

功能:
1. 内存降级存储 - Redis故障时使用内存存储
2. 自动恢复 - Redis恢复后自动同步数据
3. 统一告警 - 发送降级告警通知
4. 降级统计 - 记录降级事件用于分析
"""

import json
import logging
import time
import asyncio
from datetime import datetime, timezone
from typing import Dict, Any, Optional, List, Callable
from dataclasses import dataclass, field
from enum import Enum
from collections import defaultdict
import threading

logger = logging.getLogger(__name__)


class FallbackReason(Enum):
    """降级原因"""
    CONNECTION_ERROR = "connection_error"
    TIMEOUT = "timeout"
    MEMORY_FULL = "memory_full"
    UNKNOWN = "unknown"


@dataclass
class FallbackEntry:
    """降级存储条目"""
    key: str
    value: Any
    timestamp: datetime
    ttl: Optional[int] = None  # 秒
    operation: str = "set"  # set, lpush, zadd, etc.
    retries: int = 0
    last_retry: Optional[datetime] = None


class RedisFallbackStore:
    """
    Redis降级存储

    当Redis不可用时，数据会暂存在内存中。
    当Redis恢复后，自动同步数据到Redis。
    """

    _instance: Optional['RedisFallbackStore'] = None
    _lock = threading.Lock()

    def __new__(cls, *args, **kwargs):
        """单例模式"""
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:
                    cls._instance = super().__new__(cls)
                    cls._instance._initialized = False
        return cls._instance

    def __init__(self, max_entries: int = 10000, sync_interval: int = 30):
        """
        初始化降级存储

        Args:
            max_entries: 最大存储条目数
            sync_interval: 同步间隔（秒）
        """
        if self._initialized:
            return

        self._fallback_data: Dict[str, FallbackEntry] = {}
        self._dirty_keys: set = set()
        self._max_entries = max_entries
        self._sync_interval = sync_interval
        self._stats = defaultdict(int)
        self._is_fallback_mode = False
        self._fallback_start_time: Optional[datetime] = None
        self._alert_callbacks: List[Callable] = []
        self._sync_task: Optional[asyncio.Task] = None
        self._initialized = True

        logger.info(f"RedisFallbackStore initialized: max_entries={max_entries}")

    @property
    def is_fallback_mode(self) -> bool:
        """是否处于降级模式"""
        return self._is_fallback_mode

    def enter_fallback_mode(self, reason: FallbackReason = FallbackReason.UNKNOWN):
        """
        进入降级模式

        Args:
            reason: 降级原因
        """
        if not self._is_fallback_mode:
            self._is_fallback_mode = True
            self._fallback_start_time = datetime.now(timezone.utc)
            self._stats["fallback_count"] += 1
            self._stats[f"fallback_reason_{reason.value}"] += 1

            logger.warning(
                f"[RedisFallback] 进入降级模式: reason={reason.value}, "
                f"fallback_count={self._stats['fallback_count']}"
            )

            # 触发告警回调
            for callback in self._alert_callbacks:
                try:
                    callback("enter_fallback", {"reason": reason.value})
                except Exception as e:
                    logger.error(f"Alert callback failed: {e}")

    def exit_fallback_mode(self):
        """退出降级模式"""
        if self._is_fallback_mode:
            duration = (datetime.now(timezone.utc) - self._fallback_start_time).total_seconds()
            self._is_fallback_mode = False
            self._stats["total_fallback_duration"] += duration

            logger.info(
                f"[RedisFallback] 退出降级模式: duration={duration:.1f}s, "
                f"dirty_keys={len(self._dirty_keys)}"
            )

            # 触发告警回调
            for callback in self._alert_callbacks:
                try:
                    callback("exit_fallback", {"duration": duration})
                except Exception as e:
                    logger.error(f"Alert callback failed: {e}")

    def set(self, key: str, value: Any, ttl: Optional[int] = None) -> bool:
        """
        设置值（降级存储）

        Args:
            key: 键
            value: 值
            ttl: 过期时间（秒）

        Returns:
            是否成功
        """
        if len(self._fallback_data) >= self._max_entries:
            # 清理过期条目
            self._cleanup_expired()

            if len(self._fallback_data) >= self._max_entries:
                logger.error(f"[RedisFallback] 存储已满，无法添加新条目: {key}")
                self._stats["storage_full_errors"] += 1
                return False

        entry = FallbackEntry(
            key=key,
            value=value,
            timestamp=datetime.now(timezone.utc),
            ttl=ttl,
            operation="set"
        )

        self._fallback_data[key] = entry
        self._dirty_keys.add(key)
        self._stats["fallback_writes"] += 1

        logger.debug(f"[RedisFallback] 存储降级数据: key={key}, ttl={ttl}")
        return True

    def get(self, key: str) -> Optional[Any]:
        """
        获取值（从降级存储）

        Args:
            key: 键

        Returns:
            值，如果不存在或已过期返回None
        """
        entry = self._fallback_data.get(key)
        if entry is None:
            return None

        # 检查是否过期
        if entry.ttl is not None:
            elapsed = (datetime.now(timezone.utc) - entry.timestamp).total_seconds()
            if elapsed > entry.ttl:
                del self._fallback_data[key]
                self._dirty_keys.discard(key)
                return None

        self._stats["fallback_reads"] += 1
        return entry.value

    def lpush(self, key: str, value: Any, ttl: Optional[int] = None) -> bool:
        """
        列表头部插入（降级存储）

        Args:
            key: 键
            value: 值
            ttl: 过期时间

        Returns:
            是否成功
        """
        existing = self._fallback_data.get(key)
        if existing and isinstance(existing.value, list):
            existing.value.insert(0, value)
            existing.timestamp = datetime.now(timezone.utc)
            if ttl:
                existing.ttl = ttl
        else:
            entry = FallbackEntry(
                key=key,
                value=[value],
                timestamp=datetime.now(timezone.utc),
                ttl=ttl,
                operation="lpush"
            )
            self._fallback_data[key] = entry

        self._dirty_keys.add(key)
        self._stats["fallback_writes"] += 1
        return True

    def zadd(self, key: str, mapping: Dict[str, float], ttl: Optional[int] = None) -> bool:
        """
        有序集合添加（降级存储）

        Args:
            key: 键
            mapping: 成员-分数映射
            ttl: 过期时间

        Returns:
            是否成功
        """
        existing = self._fallback_data.get(key)
        if existing and isinstance(existing.value, dict):
            existing.value.update(mapping)
            existing.timestamp = datetime.now(timezone.utc)
            if ttl:
                existing.ttl = ttl
        else:
            entry = FallbackEntry(
                key=key,
                value=dict(mapping),
                timestamp=datetime.now(timezone.utc),
                ttl=ttl,
                operation="zadd"
            )
            self._fallback_data[key] = entry

        self._dirty_keys.add(key)
        self._stats["fallback_writes"] += 1
        return True

    async def sync_to_redis(self, redis_client) -> int:
        """
        同步数据到Redis

        Args:
            redis_client: Redis客户端

        Returns:
            成功同步的条目数
        """
        if not self._dirty_keys:
            return 0

        synced = 0
        failed_keys = set()

        for key in list(self._dirty_keys):
            entry = self._fallback_data.get(key)
            if entry is None:
                self._dirty_keys.discard(key)
                continue

            try:
                if entry.operation == "set":
                    if entry.ttl:
                        redis_client.setex(key, entry.ttl, json.dumps(entry.value))
                    else:
                        redis_client.set(key, json.dumps(entry.value))

                elif entry.operation == "lpush":
                    # 先删除再重建
                    redis_client.delete(key)
                    if entry.value:
                        for item in reversed(entry.value):
                            redis_client.lpush(key, json.dumps(item) if not isinstance(item, str) else item)
                    if entry.ttl:
                        redis_client.expire(key, entry.ttl)

                elif entry.operation == "zadd":
                    redis_client.delete(key)
                    if entry.value:
                        redis_client.zadd(key, entry.value)
                    if entry.ttl:
                        redis_client.expire(key, entry.ttl)

                synced += 1
                self._dirty_keys.discard(key)
                del self._fallback_data[key]

                logger.debug(f"[RedisFallback] 同步成功: key={key}")

            except Exception as e:
                entry.retries += 1
                entry.last_retry = datetime.now(timezone.utc)
                failed_keys.add(key)
                logger.warning(f"[RedisFallback] 同步失败: key={key}, error={e}, retries={entry.retries}")

        if synced > 0:
            logger.info(f"[RedisFallback] 同步完成: synced={synced}, failed={len(failed_keys)}")
            self._stats["sync_success"] += synced

        if failed_keys:
            self._stats["sync_failures"] += len(failed_keys)

        return synced

    def _cleanup_expired(self):
        """清理过期条目"""
        now = datetime.now(timezone.utc)
        expired_keys = []

        for key, entry in self._fallback_data.items():
            if entry.ttl is not None:
                elapsed = (now - entry.timestamp).total_seconds()
                if elapsed > entry.ttl:
                    expired_keys.append(key)

        for key in expired_keys:
            del self._fallback_data[key]
            self._dirty_keys.discard(key)

        if expired_keys:
            logger.debug(f"[RedisFallback] 清理过期条目: count={len(expired_keys)}")

    def get_stats(self) -> Dict[str, Any]:
        """获取统计信息"""
        return {
            "is_fallback_mode": self._is_fallback_mode,
            "fallback_entries": len(self._fallback_data),
            "dirty_keys": len(self._dirty_keys),
            "max_entries": self._max_entries,
            **dict(self._stats)
        }

    def register_alert_callback(self, callback: Callable):
        """注册告警回调"""
        self._alert_callbacks.append(callback)

    def clear(self):
        """清空所有降级数据（谨慎使用）"""
        self._fallback_data.clear()
        self._dirty_keys.clear()
        logger.warning("[RedisFallback] 所有降级数据已清空")


# 全局降级存储实例
_fallback_store: Optional[RedisFallbackStore] = None


def get_fallback_store() -> RedisFallbackStore:
    """获取全局降级存储实例"""
    global _fallback_store
    if _fallback_store is None:
        _fallback_store = RedisFallbackStore()
    return _fallback_store


def redis_fallback(fallback_value: Any = None, log_error: bool = True):
    """
    Redis操作降级装饰器

    当Redis操作失败时，自动使用降级存储。

    Args:
        fallback_value: 降级时的默认返回值
        log_error: 是否记录错误日志

    Example:
        @redis_fallback(fallback_value=[])
        def get_memories(self, user_id: str):
            return self.redis.lrange(f"memory:{user_id}", 0, -1)
    """
    def decorator(func):
        def wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except Exception as e:
                if log_error:
                    logger.warning(f"[RedisFallback] Redis操作失败: {func.__name__}, error={e}")

                store = get_fallback_store()
                store.enter_fallback_mode(
                    FallbackReason.CONNECTION_ERROR if "connection" in str(e).lower()
                    else FallbackReason.TIMEOUT if "timeout" in str(e).lower()
                    else FallbackReason.UNKNOWN
                )

                return fallback_value

        return wrapper
    return decorator


async def auto_sync_fallback_data(redis_client, interval: int = 30):
    """
    自动同步降级数据到Redis的后台任务

    Args:
        redis_client: Redis客户端
        interval: 检查间隔（秒）
    """
    store = get_fallback_store()

    while True:
        try:
            await asyncio.sleep(interval)

            if store.is_fallback_mode:
                # 尝试检测Redis是否恢复
                try:
                    redis_client.ping()
                    # Redis恢复，同步数据
                    synced = await store.sync_to_redis(redis_client)
                    if synced > 0 or not store._dirty_keys:
                        store.exit_fallback_mode()
                except Exception:
                    pass  # Redis仍不可用，继续等待

        except asyncio.CancelledError:
            break
        except Exception as e:
            logger.error(f"[RedisFallback] 自动同步任务异常: {e}")
