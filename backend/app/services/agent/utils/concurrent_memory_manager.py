"""
并发内存管理器

提供高性能的内存数据库并发访问控制，包括连接池、缓存优化、分布式锁等功能。
"""

import asyncio
import threading
import time
from typing import Dict, Any, List, Optional, Union, Callable
from dataclasses import dataclass
from enum import Enum
from datetime import datetime, timedelta
from contextlib import asynccontextmanager
from collections import defaultdict
import json
import hashlib

import redis
from redis.asyncio import Redis as AsyncRedis
from redis.client import Redis as SyncRedis
import redis.asyncio as aioredis

from ..utils.logger import get_logger
from ..utils.error_handler import robust_retry
from ..utils.performance import cache_result

logger = get_logger("concurrent_memory_manager")


class LockType(Enum):
    """锁类型"""
    READ = "read"        # 读锁（共享锁）
    WRITE = "write"      # 写锁（排他锁）
    UPDATE = "update"    # 更新锁
    DELETE = "delete"    # 删除锁


@dataclass
class ConnectionConfig:
    """连接配置"""
    host: str = "localhost"
    port: int = 6379
    db: int = 0
    password: Optional[str] = None
    max_connections: int = 20
    retry_on_timeout: bool = True
    socket_timeout: float = 5.0
    socket_connect_timeout: float = 5.0
    health_check_interval: int = 30


@dataclass
class CacheEntry:
    """缓存条目"""
    key: str
    value: Any
    ttl: float
    created_at: datetime
    access_count: int = 0
    last_accessed: Optional[datetime] = None

    def is_expired(self) -> bool:
        """检查是否过期"""
        return (datetime.now() - self.created_at).total_seconds() > self.ttl

    def update_access(self) -> None:
        """更新访问信息"""
        self.access_count += 1
        self.last_accessed = datetime.now()


class AsyncRedisPool:
    """异步Redis连接池"""

    def __init__(self, config: ConnectionConfig):
        """
        初始化异步连接池

        Args:
            config: 连接配置
        """
        self.config = config
        self._pool: Optional[aioredis.ConnectionPool] = None
        self._redis: Optional[AsyncRedis] = None
        self._initialized = False
        self._lock = asyncio.Lock()

    async def initialize(self) -> None:
        """初始化连接池"""
        async with self._lock:
            if self._initialized:
                return

            try:
                self._pool = aioredis.ConnectionPool(
                    host=self.config.host,
                    port=self.config.port,
                    db=self.config.db,
                    password=self.config.password,
                    max_connections=self.config.max_connections,
                    retry_on_timeout=self.config.retry_on_timeout,
                    socket_timeout=self.config.socket_timeout,
                    socket_connect_timeout=self.config.socket_connect_timeout,
                    health_check_interval=self.config.health_check_interval
                )

                self._redis = AsyncRedis(connection_pool=self._pool)

                # 测试连接
                await self._redis.ping()
                self._initialized = True

                logger.info(f"Async Redis pool initialized: {self.config.host}:{self.config.port}")

            except Exception as e:
                logger.error(f"Failed to initialize async Redis pool: {e}")
                raise

    async def get_redis(self) -> AsyncRedis:
        """获取Redis客户端"""
        if not self._initialized:
            await self.initialize()
        return self._redis

    async def close(self) -> None:
        """关闭连接池"""
        if self._redis:
            await self._redis.close()
        if self._pool:
            await self._pool.disconnect()


class DistributedLockManager:
    """分布式锁管理器"""

    def __init__(self, redis_client: AsyncRedis, default_timeout: float = 30.0):
        """
        初始化分布式锁管理器

        Args:
            redis_client: Redis客户端
            default_timeout: 默认锁超时时间
        """
        self.redis = redis_client
        self.default_timeout = default_timeout
        self._locks: Dict[str, asyncio.Lock] = {}

    @asynccontextmanager
    async def acquire_lock(
        self,
        key: str,
        timeout: Optional[float] = None,
        lock_type: LockType = LockType.WRITE
    ):
        """
        获取分布式锁

        Args:
            key: 锁键
            timeout: 超时时间
            lock_type: 锁类型
        """
        timeout = timeout or self.default_timeout
        lock_key = f"lock:{lock_type.value}:{key}"
        lock_value = f"{threading.get_ident()}:{time.time()}"

        # 尝试获取锁
        acquired = await self.redis.set(
            lock_key, lock_value, ex=timeout, nx=True
        )

        if not acquired:
            # 等待锁释放
            start_time = time.time()
            while time.time() - start_time < timeout:
                await asyncio.sleep(0.01)
                acquired = await self.redis.set(
                    lock_key, lock_value, ex=timeout, nx=True
                )
                if acquired:
                    break

            if not acquired:
                raise TimeoutError(f"Failed to acquire lock: {lock_key}")

        try:
            logger.debug(f"Acquired {lock_type.value} lock: {key}")
            yield

        finally:
            # 释放锁
            await self.redis.delete(lock_key)
            logger.debug(f"Released {lock_type.value} lock: {key}")

    async def try_lock(
        self,
        key: str,
        timeout: float = 10.0,
        lock_type: LockType = LockType.WRITE
    ) -> bool:
        """
        尝试获取锁（非阻塞）

        Args:
            key: 锁键
            timeout: 超时时间
            lock_type: 锁类型

        Returns:
            bool: 是否成功获取锁
        """
        lock_key = f"lock:{lock_type.value}:{key}"
        lock_value = f"{threading.get_ident()}:{time.time()}"

        return await self.redis.set(
            lock_key, lock_value, ex=timeout, nx=True
        )


class ConcurrentCacheManager:
    """并发缓存管理器"""

    def __init__(self, max_size: int = 10000, default_ttl: float = 3600):
        """
        初始化缓存管理器

        Args:
            max_size: 最大缓存条目数
            default_ttl: 默认TTL（秒）
        """
        self.max_size = max_size
        self.default_ttl = default_ttl
        self._cache: Dict[str, CacheEntry] = {}
        self._lock = threading.RLock()
        self._access_order: List[str] = []
        self._stats = {
            "hits": 0,
            "misses": 0,
            "evictions": 0,
            "total_requests": 0
        }

    def get(self, key: str) -> Optional[Any]:
        """
        获取缓存值

        Args:
            key: 缓存键

        Returns:
            Optional[Any]: 缓存值
        """
        with self._lock:
            self._stats["total_requests"] += 1

            if key in self._cache:
                entry = self._cache[key]

                if entry.is_expired():
                    del self._cache[key]
                    self._access_order.remove(key)
                    self._stats["misses"] += 1
                    return None

                # 更新访问信息
                entry.update_access()
                self._update_access_order(key)
                self._stats["hits"] += 1

                return entry.value

            self._stats["misses"] += 1
            return None

    def set(
        self,
        key: str,
        value: Any,
        ttl: Optional[float] = None
    ) -> None:
        """
        设置缓存值

        Args:
            key: 缓存键
            value: 缓存值
            ttl: TTL（秒）
        """
        with self._lock:
            ttl = ttl or self.default_ttl

            # 如果缓存已满，进行LRU淘汰
            if len(self._cache) >= self.max_size and key not in self._cache:
                self._evict_lru()

            # 创建新的缓存条目
            entry = CacheEntry(
                key=key,
                value=value,
                ttl=ttl,
                created_at=datetime.now()
            )

            self._cache[key] = entry
            self._update_access_order(key)

    def delete(self, key: str) -> bool:
        """
        删除缓存条目

        Args:
            key: 缓存键

        Returns:
            bool: 是否成功删除
        """
        with self._lock:
            if key in self._cache:
                del self._cache[key]
                self._access_order.remove(key)
                return True
            return False

    def clear(self) -> None:
        """清空缓存"""
        with self._lock:
            self._cache.clear()
            self._access_order.clear()
            self._stats = {
                "hits": 0,
                "misses": 0,
                "evictions": 0,
                "total_requests": 0
            }

    def _update_access_order(self, key: str) -> None:
        """更新访问顺序"""
        if key in self._access_order:
            self._access_order.remove(key)
        self._access_order.append(key)

    def _evict_lru(self) -> None:
        """淘汰最久未使用的缓存条目"""
        if self._access_order:
            lru_key = self._access_order.pop(0)
            if lru_key in self._cache:
                del self._cache[lru_key]
                self._stats["evictions"] += 1

    def get_stats(self) -> Dict[str, Any]:
        """获取缓存统计信息"""
        total = self._stats["total_requests"]
        hits = self._stats["hits"]
        hit_rate = hits / total if total > 0 else 0

        return {
            "cache_size": len(self._cache),
            "max_size": self.max_size,
            "hits": hits,
            "misses": self._stats["misses"],
            "hit_rate": hit_rate,
            "evictions": self._stats["evictions"],
            "total_requests": total
        }


class ConcurrentMemoryManager:
    """并发内存管理器"""

    def __init__(self, redis_config: ConnectionConfig):
        """
        初始化并发内存管理器

        Args:
            redis_config: Redis连接配置
        """
        self.redis_config = redis_config
        self.async_pool = AsyncRedisPool(redis_config)
        self.cache_manager = ConcurrentCacheManager()
        self._lock_manager: Optional[DistributedLockManager] = None
        self._initialized = False

        # 性能统计
        self._operation_stats = defaultdict(lambda: {
            "count": 0,
            "total_time": 0.0,
            "errors": 0,
            "avg_time": 0.0
        })

    async def initialize(self) -> None:
        """初始化内存管理器"""
        if self._initialized:
            return

        await self.async_pool.initialize()
        redis_client = await self.async_pool.get_redis()
        self._lock_manager = DistributedLockManager(redis_client)
        self._initialized = True

        logger.info("ConcurrentMemoryManager initialized successfully")

    async def get_memory(
        self,
        user_id: str,
        memory_key: str,
        use_cache: bool = True
    ) -> Optional[Any]:
        """
        获取内存数据

        Args:
            user_id: 用户ID
            memory_key: 内存键
            use_cache: 是否使用缓存

        Returns:
            Optional[Any]: 内存数据
        """
        cache_key = f"memory:{user_id}:{memory_key}"

        # 尝试从缓存获取
        if use_cache:
            cached_value = self.cache_manager.get(cache_key)
            if cached_value is not None:
                logger.debug(f"Cache hit for memory: {cache_key}")
                return cached_value

        # 从Redis获取
        try:
            redis_client = await self.async_pool.get_redis()
            async with self._lock_manager.acquire_lock(
                f"memory:{user_id}", lock_type=LockType.READ
            ):
                value = await redis_client.get(cache_key)

                if value:
                    # 解码并缓存结果
                    try:
                        decoded_value = json.loads(value)
                        self.cache_manager.set(cache_key, decoded_value, ttl=1800)
                        return decoded_value
                    except json.JSONDecodeError:
                        # 如果不是JSON，直接返回字符串
                        self.cache_manager.set(cache_key, value, ttl=1800)
                        return value

                return None

        except Exception as e:
            logger.error(f"Failed to get memory {cache_key}: {e}")
            self._update_operation_stats("get_memory", 0, error=True)
            raise

    async def set_memory(
        self,
        user_id: str,
        memory_key: str,
        value: Any,
        ttl: Optional[float] = None,
        update_cache: bool = True
    ) -> bool:
        """
        设置内存数据

        Args:
            user_id: 用户ID
            memory_key: 内存键
            value: 内存值
            ttl: TTL（秒）
            update_cache: 是否更新缓存

        Returns:
            bool: 是否成功设置
        """
        cache_key = f"memory:{user_id}:{memory_key}"
        ttl = ttl or 3600

        try:
            redis_client = await self.async_pool.get_redis()

            # 序列化值
            if isinstance(value, (dict, list)):
                serialized_value = json.dumps(value, ensure_ascii=False)
            else:
                serialized_value = str(value)

            async with self._lock_manager.acquire_lock(
                f"memory:{user_id}", lock_type=LockType.WRITE
            ):
                success = await redis_client.setex(cache_key, ttl, serialized_value)

                if success and update_cache:
                    # 更新本地缓存
                    self.cache_manager.set(cache_key, value, ttl=min(ttl, 1800))

                return bool(success)

        except Exception as e:
            logger.error(f"Failed to set memory {cache_key}: {e}")
            self._update_operation_stats("set_memory", 0, error=True)
            raise

    async def delete_memory(
        self,
        user_id: str,
        memory_key: str
    ) -> bool:
        """
        删除内存数据

        Args:
            user_id: 用户ID
            memory_key: 内存键

        Returns:
            bool: 是否成功删除
        """
        cache_key = f"memory:{user_id}:{memory_key}"

        try:
            redis_client = await self.async_pool.get_redis()

            async with self._lock_manager.acquire_lock(
                f"memory:{user_id}", lock_type=LockType.DELETE
            ):
                # 从Redis删除
                result = await redis_client.delete(cache_key)

                # 从缓存删除
                self.cache_manager.delete(cache_key)

                return result > 0

        except Exception as e:
            logger.error(f"Failed to delete memory {cache_key}: {e}")
            self._update_operation_stats("delete_memory", 0, error=True)
            raise

    async def batch_get_memory(
        self,
        user_id: str,
        memory_keys: List[str],
        use_cache: bool = True
    ) -> Dict[str, Any]:
        """
        批量获取内存数据

        Args:
            user_id: 用户ID
            memory_keys: 内存键列表
            use_cache: 是否使用缓存

        Returns:
            Dict[str, Any]: 内存数据映射
        """
        results = {}
        redis_keys = []

        # 首先尝试从缓存获取
        if use_cache:
            for key in memory_keys:
                cache_key = f"memory:{user_id}:{key}"
                cached_value = self.cache_manager.get(cache_key)
                if cached_value is not None:
                    results[key] = cached_value
                else:
                    redis_keys.append(key)

        # 获取缓存未命中的数据
        if redis_keys:
            try:
                redis_client = await self.async_pool.get_redis()

                async with self._lock_manager.acquire_lock(
                    f"memory:{user_id}", lock_type=LockType.READ
                ):
                    pipeline = redis_client.pipeline()
                    for key in redis_keys:
                        cache_key = f"memory:{user_id}:{key}"
                        pipeline.get(cache_key)

                    values = await pipeline.execute()

                    # 处理结果
                    for i, key in enumerate(redis_keys):
                        value = values[i]
                        if value:
                            try:
                                decoded_value = json.loads(value)
                                results[key] = decoded_value
                                # 更新缓存
                                cache_key = f"memory:{user_id}:{key}"
                                self.cache_manager.set(cache_key, decoded_value, ttl=1800)
                            except json.JSONDecodeError:
                                results[key] = value
                                cache_key = f"memory:{user_id}:{key}"
                                self.cache_manager.set(cache_key, value, ttl=1800)

            except Exception as e:
                logger.error(f"Failed to batch get memory for user {user_id}: {e}")
                self._update_operation_stats("batch_get_memory", 0, error=True)
                raise

        return results

    async def batch_set_memory(
        self,
        user_id: str,
        memory_data: Dict[str, Any],
        ttl: Optional[float] = None,
        update_cache: bool = True
    ) -> Dict[str, bool]:
        """
        批量设置内存数据

        Args:
            user_id: 用户ID
            memory_data: 内存数据映射
            ttl: TTL（秒）
            update_cache: 是否更新缓存

        Returns:
            Dict[str, bool]: 设置结果映射
        """
        results = {}
        ttl = ttl or 3600

        try:
            redis_client = await self.async_pool.get_redis()

            async with self._lock_manager.acquire_lock(
                f"memory:{user_id}", lock_type=LockType.WRITE
            ):
                pipeline = redis_client.pipeline()

                for key, value in memory_data.items():
                    cache_key = f"memory:{user_id}:{key}"

                    # 序列化值
                    if isinstance(value, (dict, list)):
                        serialized_value = json.dumps(value, ensure_ascii=False)
                    else:
                        serialized_value = str(value)

                    pipeline.setex(cache_key, ttl, serialized_value)

                    # 更新本地缓存
                    if update_cache:
                        self.cache_manager.set(cache_key, value, ttl=min(ttl, 1800))

                # 执行批量设置
                pipeline_results = await pipeline.execute()

                # 映射结果
                for i, key in enumerate(memory_data.keys()):
                    results[key] = bool(pipeline_results[i])

            return results

        except Exception as e:
            logger.error(f"Failed to batch set memory for user {user_id}: {e}")
            self._update_operation_stats("batch_set_memory", 0, error=True)
            raise

    def _update_operation_stats(
        self,
        operation: str,
        duration: float,
        error: bool = False
    ) -> None:
        """更新操作统计"""
        stats = self._operation_stats[operation]
        stats["count"] += 1
        stats["total_time"] += duration

        if error:
            stats["errors"] += 1

        stats["avg_time"] = stats["total_time"] / stats["count"]

    def get_performance_stats(self) -> Dict[str, Any]:
        """获取性能统计信息"""
        cache_stats = self.cache_manager.get_stats()

        return {
            "cache": cache_stats,
            "operations": dict(self._operation_stats),
            "timestamp": datetime.now().isoformat()
        }

    async def close(self) -> None:
        """关闭内存管理器"""
        await self.async_pool.close()
        self._initialized = False
        logger.info("ConcurrentMemoryManager closed")


# 全局实例
_concurrent_memory_manager: Optional[ConcurrentMemoryManager] = None


async def get_concurrent_memory_manager(
    redis_config: Optional[ConnectionConfig] = None
) -> ConcurrentMemoryManager:
    """获取全局并发内存管理器实例"""
    global _concurrent_memory_manager

    if _concurrent_memory_manager is None:
        if redis_config is None:
            # 使用默认配置
            redis_config = ConnectionConfig()
        _concurrent_memory_manager = ConcurrentMemoryManager(redis_config)
        await _concurrent_memory_manager.initialize()

    return _concurrent_memory_manager


# 便捷函数
async def get_user_memory(
    user_id: str,
    memory_key: str,
    use_cache: bool = True
) -> Optional[Any]:
    """获取用户内存数据的便捷函数"""
    manager = await get_concurrent_memory_manager()
    return await manager.get_memory(user_id, memory_key, use_cache)


async def set_user_memory(
    user_id: str,
    memory_key: str,
    value: Any,
    ttl: Optional[float] = None
) -> bool:
    """设置用户内存数据的便捷函数"""
    manager = await get_concurrent_memory_manager()
    return await manager.set_memory(user_id, memory_key, value, ttl)


async def get_memory_performance_stats() -> Dict[str, Any]:
    """获取内存性能统计的便捷函数"""
    manager = await get_concurrent_memory_manager()
    return manager.get_performance_stats()