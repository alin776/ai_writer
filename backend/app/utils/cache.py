"""
缓存工具模块

提供缓存装饰器和缓存管理工具
"""
import functools
import logging
from typing import Any, Callable, Optional
from app.core.redis import redis_client, CacheExpire

logger = logging.getLogger(__name__)


def cache_result(
    key_prefix: str,
    expire: int = CacheExpire.DYNAMIC,
    key_builder: Optional[Callable] = None
):
    """
    缓存函数结果的装饰器
    
    使用示例：
    ```python
    @cache_result("works:list", expire=300)
    async def get_works():
        return await db.query(Work).all()
    
    @cache_result(
        "works:detail",
        expire=600,
        key_builder=lambda work_id: f"works:detail:{work_id}"
    )
    async def get_work(work_id: str):
        return await db.query(Work).get(work_id)
    ```
    
    Args:
        key_prefix: 缓存键前缀
        expire: 过期时间（秒）
        key_builder: 自定义键生成函数，接收函数参数，返回完整的缓存键
    """
    def decorator(func: Callable) -> Callable:
        @functools.wraps(func)
        async def wrapper(*args, **kwargs) -> Any:
            # 生成缓存键
            if key_builder:
                # 使用自定义键生成器
                try:
                    cache_key = key_builder(*args, **kwargs)
                except Exception as e:
                    logger.warning(f"Key builder failed: {e}, falling back to default")
                    cache_key = f"{key_prefix}:{':'.join(map(str, args))}"
            else:
                # 默认键生成：prefix:arg1:arg2...
                if args:
                    cache_key = f"{key_prefix}:{':'.join(map(str, args))}"
                else:
                    cache_key = key_prefix
            
            # 尝试从缓存获取
            try:
                cached_value = await redis_client.get(cache_key)
                if cached_value is not None:
                    logger.info(f"🎯 Cache HIT: {cache_key}")
                    return cached_value
                
                logger.info(f"❌ Cache MISS: {cache_key}")
            except Exception as e:
                logger.error(f"Cache get error [{cache_key}]: {e}")
            
            # 执行原函数
            result = await func(*args, **kwargs)
            
            # 存入缓存
            try:
                await redis_client.set(cache_key, result, expire)
                logger.info(f"✅ Cache SET: {cache_key} (expire={expire}s)")
            except Exception as e:
                logger.error(f"Cache set error [{cache_key}]: {e}")
            
            return result
        
        return wrapper
    return decorator


async def invalidate_cache(pattern: str) -> int:
    """
    使缓存失效
    
    Args:
        pattern: 缓存键模式（支持通配符 *）
        
    Returns:
        删除的键数量
        
    示例：
    ```python
    # 删除所有作品相关缓存
    await invalidate_cache("works:*")
    
    # 删除特定作品的缓存
    await invalidate_cache(f"works:detail:{work_id}")
    ```
    """
    try:
        deleted = await redis_client.delete_pattern(pattern)
        logger.info(f"🗑️ Invalidated {deleted} cache keys: {pattern}")
        return deleted
    except Exception as e:
        logger.error(f"Cache invalidation error [{pattern}]: {e}")
        return 0


async def get_cached(key: str) -> Any:
    """
    直接获取缓存值
    
    Args:
        key: 缓存键
        
    Returns:
        缓存值或 None
    """
    return await redis_client.get(key)


async def set_cached(key: str, value: Any, expire: Optional[int] = None) -> bool:
    """
    直接设置缓存值
    
    Args:
        key: 缓存键
        value: 缓存值
        expire: 过期时间（秒）
        
    Returns:
        是否设置成功
    """
    return await redis_client.set(key, value, expire)


class CacheInvalidator:
    """缓存失效管理器"""
    
    @staticmethod
    async def invalidate_work(work_id: str) -> None:
        """使作品相关的所有缓存失效"""
        patterns = [
            "works:list",  # 作品列表
            f"works:detail:{work_id}",  # 作品详情
            f"works:{work_id}:*",  # 作品的章节等
            f"worldview:{work_id}:*",  # 世界观数据
            f"analysis:{work_id}:*",  # 分析数据
        ]
        for pattern in patterns:
            await invalidate_cache(pattern)
    
    @staticmethod
    async def invalidate_chapter(chapter_id: str, work_id: str) -> None:
        """使章节相关的所有缓存失效"""
        patterns = [
            f"chapters:detail:{chapter_id}",  # 章节详情
            f"works:{work_id}:chapters",  # 章节列表
            f"chapters:{chapter_id}:*",  # 章节相关数据
        ]
        for pattern in patterns:
            await invalidate_cache(pattern)
    
    @staticmethod
    async def invalidate_worldview(work_id: str) -> None:
        """使世界观相关的所有缓存失效"""
        patterns = [
            f"worldview:{work_id}:*",  # 所有世界观数据
        ]
        for pattern in patterns:
            await invalidate_cache(pattern)
    
    @staticmethod
    async def invalidate_analysis(work_id: str) -> None:
        """使分析相关的所有缓存失效"""
        patterns = [
            f"analysis:{work_id}:*",  # 所有分析数据
        ]
        for pattern in patterns:
            await invalidate_cache(pattern)
