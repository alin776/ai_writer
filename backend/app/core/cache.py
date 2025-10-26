"""
缓存装饰器

功能:
- 自动缓存评审结果
- 减少AI调用成本
- 支持过期时间设置
"""

from functools import wraps
from app.core.redis_client import redis_client
import json
import hashlib
import logging
from typing import Callable, Any

logger = logging.getLogger(__name__)


def cache_review(expire: int = 3600, key_prefix: str = "review"):
    """
    缓存评审结果装饰器

    Args:
        expire: 过期时间(秒) - 默认1小时
        key_prefix: 缓存key前缀

    使用示例:
        @cache_review(expire=86400)  # 缓存24小时
        async def review_chapter(chapter_id):
            pass

    注意:
        - 如果Redis不可用,装饰器会自动降级,直接执行函数
        - 缓存键基于函数名和参数生成
    """
    def decorator(func: Callable) -> Callable:
        @wraps(func)
        async def wrapper(*args, **kwargs) -> Any:
            # 检查Redis是否可用
            if not redis_client.is_available():
                logger.warning(f"[缓存装饰器] Redis不可用,直接执行函数: {func.__name__}")
                return await func(*args, **kwargs)

            # 生成缓存key (基于函数名和参数)
            cache_key = _generate_cache_key(
                key_prefix, func.__name__, args, kwargs
            )

            # 查询缓存
            cached = redis_client.get_json(cache_key)
            if cached:
                logger.info(f"✅ 缓存命中: {cache_key}")
                return cached

            logger.info(f"⚠️ 缓存未命中: {cache_key}")

            # 执行函数
            result = await func(*args, **kwargs)

            # 缓存结果
            success = redis_client.set_json(cache_key, result, expire)
            if success:
                logger.info(f"💾 缓存已保存: {cache_key} (expire={expire}s)")
            else:
                logger.warning(f"⚠️ 缓存保存失败: {cache_key}")

            return result

        return wrapper
    return decorator


def _generate_cache_key(prefix: str, func_name: str, args: tuple, kwargs: dict) -> str:
    """
    生成缓存key

    Args:
        prefix: key前缀
        func_name: 函数名
        args: 位置参数
        kwargs: 关键字参数

    Returns:
        缓存key字符串

    示例:
        review:review_chapter:a1b2c3d4
    """
    # 将参数序列化为字符串
    params_dict = {
        'args': [_serialize_arg(arg) for arg in args],
        'kwargs': {k: _serialize_arg(v) for k, v in kwargs.items()}
    }

    params_str = json.dumps(params_dict, sort_keys=True, ensure_ascii=False)

    # MD5哈希 (取前16位)
    params_hash = hashlib.md5(params_str.encode()).hexdigest()[:16]

    return f"{prefix}:{func_name}:{params_hash}"


def _serialize_arg(arg: Any) -> str:
    """
    序列化参数为字符串

    Args:
        arg: 参数值

    Returns:
        序列化后的字符串
    """
    # 基本类型
    if isinstance(arg, (str, int, float, bool, type(None))):
        return str(arg)

    # UUID
    if hasattr(arg, 'hex'):  # UUID对象
        return arg.hex

    # 字典
    if isinstance(arg, dict):
        return json.dumps(arg, sort_keys=True, ensure_ascii=False)

    # 列表/元组
    if isinstance(arg, (list, tuple)):
        return json.dumps(arg, ensure_ascii=False)

    # 其他对象 (尝试转为字符串)
    return str(arg)


def invalidate_cache(key_pattern: str):
    """
    清除匹配的缓存

    Args:
        key_pattern: 缓存key模式 (支持通配符 *)

    示例:
        invalidate_cache("review:review_chapter:*")  # 清除所有章节评审缓存
    """
    if not redis_client.is_available():
        logger.warning("[缓存清除] Redis不可用")
        return

    try:
        # 扫描匹配的key
        keys = redis_client.client.keys(key_pattern)
        if keys:
            redis_client.client.delete(*keys)
            logger.info(f"🗑️ 已清除 {len(keys)} 个缓存: {key_pattern}")
        else:
            logger.info(f"ℹ️ 未找到匹配的缓存: {key_pattern}")
    except Exception as e:
        logger.error(f"[缓存清除] 错误: {e}")
