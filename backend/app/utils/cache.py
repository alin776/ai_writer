"""
缓存工具模块

提供缓存装饰器和缓存管理工具

TODO: Redis暂时禁用，所有缓存操作为空操作
"""
import functools
import logging
from typing import Any, Callable, Optional
# from app.core.redis import redis_client, CacheExpire  # TODO: Redis暂时禁用

logger = logging.getLogger(__name__)


# TODO: Redis暂时禁用，定义占位符类
class CacheExpire:
    """缓存过期时间常量 (占位符)"""
    STATIC = 3600  # 1小时
    DYNAMIC = 300  # 5分钟
    SHORT = 60     # 1分钟


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
            # TODO: Redis暂时禁用，直接执行原函数
            logger.debug(f"Cache disabled, executing function directly: {func.__name__}")
            result = await func(*args, **kwargs)
            return result
        
        return wrapper
    return decorator


async def invalidate_cache(pattern: str) -> int:
    """
    使缓存失效
    
    TODO: Redis暂时禁用，返回0
    """
    logger.debug(f"Cache invalidation skipped (Redis disabled): {pattern}")
    return 0


async def get_cached(key: str) -> Any:
    """
    直接获取缓存值
    
    TODO: Redis暂时禁用，返回None
    """
    logger.debug(f"Cache get skipped (Redis disabled): {key}")
    return None


async def set_cached(key: str, value: Any, expire: Optional[int] = None) -> bool:
    """
    直接设置缓存值
    
    TODO: Redis暂时禁用，返回False
    """
    logger.debug(f"Cache set skipped (Redis disabled): {key}")
    return False


class CacheInvalidator:
    """缓存失效管理器 - TODO: Redis暂时禁用，所有操作为空"""
    
    @staticmethod
    async def invalidate_work(work_id: str) -> None:
        """使作品相关的所有缓存失效"""
        # TODO: Redis暂时禁用
        logger.debug(f"Cache invalidation skipped (Redis disabled): work {work_id}")
        pass
    
    @staticmethod
    async def invalidate_chapter(chapter_id: str, work_id: str) -> None:
        """使章节相关的所有缓存失效"""
        # TODO: Redis暂时禁用
        logger.debug(f"Cache invalidation skipped (Redis disabled): chapter {chapter_id}")
        pass
    
    @staticmethod
    async def invalidate_worldview(work_id: str) -> None:
        """使世界观相关的所有缓存失效"""
        # TODO: Redis暂时禁用
        logger.debug(f"Cache invalidation skipped (Redis disabled): worldview {work_id}")
        pass
    
    @staticmethod
    async def invalidate_analysis(work_id: str) -> None:
        """使分析相关的所有缓存失效"""
        # TODO: Redis暂时禁用
        logger.debug(f"Cache invalidation skipped (Redis disabled): analysis {work_id}")
        pass
