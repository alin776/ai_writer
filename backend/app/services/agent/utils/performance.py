"""
性能优化工具模块

提供缓存、索引、批量处理等性能优化功能。
"""

import asyncio
import time
import hashlib
import json
from typing import Dict, Any, List, Optional, Callable, TypeVar, Union
from functools import wraps, lru_cache
from datetime import datetime, timedelta
from dataclasses import dataclass
from collections import defaultdict
import threading

T = TypeVar('T')


@dataclass
class CacheEntry:
    """缓存条目"""
    value: Any
    timestamp: datetime
    access_count: int = 0
    ttl: Optional[float] = None

    def is_expired(self) -> bool:
        """检查是否过期"""
        if self.ttl is None:
            return False
        return (datetime.now() - self.timestamp).total_seconds() > self.ttl

    def access(self) -> Any:
        """访问缓存条目"""
        self.access_count += 1
        self.timestamp = datetime.now()
        return self.value


class MemoryCache:
    """内存缓存管理器"""

    def __init__(self, max_size: int = 1000, default_ttl: Optional[float] = None):
        self.max_size = max_size
        self.default_ttl = default_ttl
        self._cache: Dict[str, CacheEntry] = {}
        self._lock = threading.RLock()
        self._hits = 0
        self._misses = 0

    def get(self, key: str) -> Optional[Any]:
        """获取缓存值"""
        with self._lock:
            entry = self._cache.get(key)
            if entry is None:
                self._misses += 1
                return None

            if entry.is_expired():
                del self._cache[key]
                self._misses += 1
                return None

            self._hits += 1
            return entry.access()

    def set(self, key: str, value: Any, ttl: Optional[float] = None) -> None:
        """设置缓存值"""
        with self._lock:
            # 如果缓存已满，删除最少使用的条目
            if len(self._cache) >= self.max_size:
                self._evict_lru()

            ttl = ttl or self.default_ttl
            self._cache[key] = CacheEntry(
                value=value,
                timestamp=datetime.now(),
                ttl=ttl
            )

    def delete(self, key: str) -> bool:
        """删除缓存值"""
        with self._lock:
            return self._cache.pop(key, None) is not None

    def clear(self) -> None:
        """清空缓存"""
        with self._lock:
            self._cache.clear()
            self._hits = 0
            self._misses = 0

    def _evict_lru(self) -> None:
        """删除最少使用的条目"""
        if not self._cache:
            return

        lru_key = min(self._cache.keys(), key=lambda k: self._cache[k].access_count)
        del self._cache[lru_key]

    def get_stats(self) -> Dict[str, Any]:
        """获取缓存统计信息"""
        with self._lock:
            total_requests = self._hits + self._misses
            hit_rate = self._hits / total_requests if total_requests > 0 else 0

            return {
                "size": len(self._cache),
                "max_size": self.max_size,
                "hits": self._hits,
                "misses": self._misses,
                "hit_rate": hit_rate,
                "memory_usage": sum(len(str(entry.value)) for entry in self._cache.values())
            }


class IndexManager:
    """索引管理器 - 用于快速查找"""

    def __init__(self):
        self._indexes: Dict[str, Dict[Any, List[str]]] = defaultdict(dict)
        self._lock = threading.RLock()

    def create_index(self, index_name: str, key_func: Callable[[Any], Any]) -> None:
        """创建索引"""
        with self._lock:
            if index_name not in self._indexes:
                self._indexes[index_name] = defaultdict(list)

    def add_to_index(self, index_name: str, item: Any, item_id: str) -> None:
        """添加项到索引"""
        with self._lock:
            if index_name in self._indexes:
                # 根据索引类型提取键值
                if hasattr(item, index_name):
                    key = getattr(item, index_name)
                elif isinstance(item, dict) and index_name in item:
                    key = item[index_name]
                else:
                    return

                self._indexes[index_name][key].append(item_id)

    def remove_from_index(self, index_name: str, item: Any, item_id: str) -> None:
        """从索引中移除项"""
        with self._lock:
            if index_name in self._indexes:
                if hasattr(item, index_name):
                    key = getattr(item, index_name)
                elif isinstance(item, dict) and index_name in item:
                    key = item[index_name]
                else:
                    return

                if item_id in self._indexes[index_name][key]:
                    self._indexes[index_name][key].remove(item_id)

                    # 如果列表为空，删除键
                    if not self._indexes[index_name][key]:
                        del self._indexes[index_name][key]

    def query_index(self, index_name: str, key: Any) -> List[str]:
        """查询索引"""
        with self._lock:
            return self._indexes[index_name].get(key, []).copy()


class BatchProcessor:
    """批量处理器"""

    def __init__(self, batch_size: int = 100, max_wait_time: float = 1.0):
        self.batch_size = batch_size
        self.max_wait_time = max_wait_time
        self._queue: List[Any] = []
        self._lock = threading.Lock()
        self._last_flush = time.time()
        self._processor: Optional[Callable] = None

    def set_processor(self, processor: Callable[[List[Any]], None]) -> None:
        """设置批处理器"""
        self._processor = processor

    def add(self, item: Any) -> None:
        """添加项到批处理队列"""
        with self._lock:
            self._queue.append(item)

            # 检查是否需要立即处理
            if (len(self._queue) >= self.batch_size or
                time.time() - self._last_flush >= self.max_wait_time):
                self._flush()

    def _flush(self) -> None:
        """刷新队列"""
        if not self._queue or not self._processor:
            return

        items = self._queue.copy()
        self._queue.clear()
        self._last_flush = time.time()

        # 异步处理或同步处理
        if asyncio.iscoroutinefunction(self._processor):
            # 对于异步处理器，创建任务
            asyncio.create_task(self._processor(items))
        else:
            # 同步处理
            self._processor(items)

    def flush(self) -> None:
        """手动刷新队列"""
        with self._lock:
            self._flush()


class PerformanceOptimizer:
    """性能优化器"""

    def __init__(self):
        self.cache = MemoryCache(max_size=2000, default_ttl=3600)  # 1小时TTL
        self.index_manager = IndexManager()
        self.batch_processor = BatchProcessor(batch_size=50, max_wait_time=0.5)
        self._performance_stats = defaultdict(list)

    def cache_result(self, ttl: Optional[float] = None):
        """缓存结果装饰器"""
        def decorator(func: Callable[..., T]) -> Callable[..., T]:
            @wraps(func)
            def wrapper(*args, **kwargs) -> T:
                # 生成缓存键
                cache_key = self._generate_cache_key(func.__name__, args, kwargs)

                # 尝试从缓存获取
                cached_result = self.cache.get(cache_key)
                if cached_result is not None:
                    return cached_result

                # 执行函数并缓存结果
                start_time = time.time()
                result = func(*args, **kwargs)
                execution_time = time.time() - start_time

                self.cache.set(cache_key, result, ttl)
                self._record_performance(func.__name__, execution_time)

                return result

            @wraps(func)
            async def async_wrapper(*args, **kwargs) -> T:
                # 生成缓存键
                cache_key = self._generate_cache_key(func.__name__, args, kwargs)

                # 尝试从缓存获取
                cached_result = self.cache.get(cache_key)
                if cached_result is not None:
                    return cached_result

                # 执行异步函数并缓存结果
                start_time = time.time()
                result = await func(*args, **kwargs)
                execution_time = time.time() - start_time

                self.cache.set(cache_key, result, ttl)
                self._record_performance(func.__name__, execution_time)

                return result

            # 根据函数类型返回对应的包装器
            if asyncio.iscoroutinefunction(func):
                return async_wrapper
            else:
                return wrapper

        return decorator

    def parallel_execute(self, max_workers: int = 5):
        """并行执行装饰器"""
        def decorator(func: Callable[..., T]) -> Callable[..., T]:
            @wraps(func)
            async def async_wrapper(*args, **kwargs) -> List[T]:
                # 如果参数是列表，并行处理
                if args and isinstance(args[0], list):
                    items = args[0]
                    if len(items) == 0:
                        return []

                    # 限制并发数
                    semaphore = asyncio.Semaphore(max_workers)

                    async def process_item(item):
                        async with semaphore:
                            return await func(item, *args[1:], **kwargs)

                    # 并行处理所有项
                    tasks = [process_item(item) for item in items]
                    results = await asyncio.gather(*tasks, return_exceptions=True)

                    # 过滤异常结果
                    valid_results = []
                    for result in results:
                        if not isinstance(result, Exception):
                            valid_results.append(result)

                    return valid_results
                else:
                    # 单个项正常处理
                    return await func(*args, **kwargs)

            return async_wrapper

        return decorator

    def _generate_cache_key(self, func_name: str, args: tuple, kwargs: dict) -> str:
        """生成缓存键"""
        # 将参数序列化为字符串
        try:
            args_str = str(args)
            kwargs_str = str(sorted(kwargs.items()))
            combined = f"{func_name}:{args_str}:{kwargs_str}"
            return hashlib.md5(combined.encode()).hexdigest()
        except Exception:
            # 如果序列化失败，使用函数名和参数长度
            return f"{func_name}:{len(args)}:{len(kwargs)}"

    def _record_performance(self, operation: str, execution_time: float) -> None:
        """记录性能数据"""
        self._performance_stats[operation].append(execution_time)

        # 只保留最近100条记录
        if len(self._performance_stats[operation]) > 100:
            self._performance_stats[operation] = self._performance_stats[operation][-100:]

    def get_performance_stats(self, operation: Optional[str] = None) -> Dict[str, Any]:
        """获取性能统计"""
        if operation:
            times = self._performance_stats.get(operation, [])
            if not times:
                return {"operation": operation, "count": 0}

            return {
                "operation": operation,
                "count": len(times),
                "avg_time": sum(times) / len(times),
                "min_time": min(times),
                "max_time": max(times),
                "recent_times": times[-10:]  # 最近10次
            }
        else:
            # 返回所有操作的统计
            stats = {}
            for op, times in self._performance_stats.items():
                if times:
                    stats[op] = {
                        "count": len(times),
                        "avg_time": sum(times) / len(times),
                        "min_time": min(times),
                        "max_time": max(times)
                    }
            return stats

    def clear_cache(self) -> None:
        """清空缓存"""
        self.cache.clear()

    def get_cache_stats(self) -> Dict[str, Any]:
        """获取缓存统计"""
        return self.cache.get_stats()

    def optimize_memory_access(self, items: List[Any], key_func: Callable) -> Dict[Any, List[Any]]:
        """优化内存访问 - 按键分组"""
        groups = defaultdict(list)
        for item in items:
            try:
                key = key_func(item)
                groups[key].append(item)
            except Exception:
                # 如果获取键失败，使用None作为键
                groups[None].append(item)

        return dict(groups)


# 全局性能优化器实例
performance_optimizer = PerformanceOptimizer()


def get_performance_optimizer() -> PerformanceOptimizer:
    """获取全局性能优化器实例"""
    return performance_optimizer


# 便捷的装饰器
def cache_result(ttl: Optional[float] = None):
    """缓存结果装饰器的便捷函数"""
    return performance_optimizer.cache_result(ttl)


def parallel_execute(max_workers: int = 5):
    """并行执行装饰器的便捷函数"""
    return performance_optimizer.parallel_execute(max_workers)


# 缓存清理函数
def clear_all_caches() -> None:
    """清空所有缓存"""
    performance_optimizer.clear_cache()


def get_performance_summary() -> Dict[str, Any]:
    """获取性能摘要"""
    cache_stats = performance_optimizer.get_cache_stats()
    perf_stats = performance_optimizer.get_performance_stats()

    return {
        "cache": cache_stats,
        "performance": perf_stats,
        "timestamp": datetime.now().isoformat()
    }