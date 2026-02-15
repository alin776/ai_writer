"""
速率限制中间件

简单的内存限流实现，支持：
- 基于IP的限流
- 基于用户的限流
- 滑动窗口算法
"""

import time
from collections import defaultdict, deque
from typing import Dict, Tuple
import logging
from fastapi import Request, HTTPException, status
from functools import wraps

logger = logging.getLogger(__name__)


class RateLimiter:
    """内存型速率限制器（滑动窗口算法）"""

    def __init__(self):
        # key: (identifier, endpoint) -> deque of timestamps
        self._requests: Dict[Tuple[str, str], deque] = defaultdict(deque)
        self._window_seconds: Dict[Tuple[str, str], int] = {}
        self._last_cleanup = time.time()

    def check_rate_limit(
        self,
        identifier: str,
        endpoint: str,
        max_requests: int,
        window_seconds: int
    ) -> Tuple[bool, dict]:
        """
        检查是否超过限流

        Args:
            identifier: 唯一标识（IP或用户ID）
            endpoint: API端点
            max_requests: 时间窗口内最大请求数
            window_seconds: 时间窗口（秒）

        Returns:
            (是否允许, 限流信息字典)
        """
        current_time = time.time()
        key = (identifier, endpoint)
        self._window_seconds[key] = window_seconds

        # 定期清理旧数据（每5分钟）
        if current_time - self._last_cleanup > 300:
            self._cleanup_old_entries(current_time)
            self._last_cleanup = current_time

        # 获取请求队列
        requests = self._requests[key]

        # 移除窗口外的请求
        cutoff_time = current_time - window_seconds
        while requests and requests[0] < cutoff_time:
            requests.popleft()

        # 检查是否超限
        current_count = len(requests)

        if current_count >= max_requests:
            # 超过限制
            oldest_request = requests[0]
            retry_after = int(oldest_request + window_seconds - current_time) + 1

            logger.warning(
                f"速率限制触发: identifier={identifier}, endpoint={endpoint}, "
                f"count={current_count}/{max_requests}, window={window_seconds}s"
            )

            return False, {
                "allowed": False,
                "current": current_count,
                "limit": max_requests,
                "remaining": 0,
                "reset": int(oldest_request + window_seconds),
                "retry_after": retry_after
            }

        # 允许请求
        requests.append(current_time)
        remaining = max_requests - current_count - 1

        return True, {
            "allowed": True,
            "current": current_count + 1,
            "limit": max_requests,
            "remaining": remaining,
            "reset": int(current_time + window_seconds)
        }

    def _cleanup_old_entries(self, current_time: float):
        """清理5分钟以上没有请求的条目"""
        keys_to_delete = []

        for key, requests in self._requests.items():
            window_seconds = self._window_seconds.get(key, 300)
            cutoff = current_time - window_seconds

            while requests and requests[0] < cutoff:
                requests.popleft()

            if not requests:
                keys_to_delete.append(key)

        for key in keys_to_delete:
            del self._requests[key]
            self._window_seconds.pop(key, None)

        if keys_to_delete:
            logger.debug(f"清理了 {len(keys_to_delete)} 个过期限流条目")


# 全局限流器实例
_rate_limiter = RateLimiter()


def get_rate_limiter() -> RateLimiter:
    """获取限流器单例"""
    return _rate_limiter


def rate_limit(
    max_requests: int = 10,
    window_seconds: int = 60,
    identifier_func=None
):
    """
    速率限制装饰器

    Args:
        max_requests: 时间窗口内最大请求数
        window_seconds: 时间窗口（秒）
        identifier_func: 自定义标识符获取函数（接收request，返回字符串）

    Example:
        @rate_limit(max_requests=10, window_seconds=60)  # 每分钟最多10次
        async def my_endpoint(request: Request):
            ...
    """
    def decorator(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            # 查找Request对象
            request = None
            for arg in args:
                if isinstance(arg, Request):
                    request = arg
                    break
            if not request:
                request = kwargs.get('request')

            if not request:
                # 没有Request对象，跳过限流
                return await func(*args, **kwargs)

            # 获取标识符
            if identifier_func:
                identifier = identifier_func(request)
            else:
                # 默认使用IP地址
                identifier = request.client.host if request.client else "unknown"

            # 获取端点名称
            endpoint = request.url.path

            # 检查限流
            limiter = get_rate_limiter()
            allowed, info = limiter.check_rate_limit(
                identifier=identifier,
                endpoint=endpoint,
                max_requests=max_requests,
                window_seconds=window_seconds
            )

            # 添加限流头
            if hasattr(request.state, '_rate_limit_info'):
                request.state._rate_limit_info = info

            if not allowed:
                # 触发限流
                raise HTTPException(
                    status_code=status.HTTP_429_TOO_MANY_REQUESTS,
                    detail=f"请求过于频繁，请在 {info['retry_after']} 秒后重试",
                    headers={
                        "X-RateLimit-Limit": str(info['limit']),
                        "X-RateLimit-Remaining": "0",
                        "X-RateLimit-Reset": str(info['reset']),
                        "Retry-After": str(info['retry_after'])
                    }
                )

            # 允许请求
            return await func(*args, **kwargs)

        return wrapper
    return decorator


def get_user_identifier(request: Request) -> str:
    """
    获取用户标识符（用于基于用户的限流）

    优先使用用户ID，fallback到IP地址
    """
    # 尝试从request.state获取当前用户
    if hasattr(request.state, 'user'):
        user = request.state.user
        if user and hasattr(user, 'id'):
            return f"user:{user.id}"

    # fallback到IP
    return f"ip:{request.client.host if request.client else 'unknown'}"
