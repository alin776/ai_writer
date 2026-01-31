"""通用重试装饰器和错误分类工具

本模块提供统一的重试机制和错误分类功能，直接复用Planning模式的重试逻辑。

代码复用来源：
- backend/app/services/agent/langgraph_agent.py:3178-3248 (Planning重试机制)
- backend/app/services/agent/langgraph_agent.py:3461-3474 (优雅降级)

核心功能：
- @retry_on_failure: 自动重试装饰器（网络/超时错误）
- ErrorType: 错误类型枚举
- classify_error: 智能错误分类
"""

import asyncio
import logging
from enum import Enum
from functools import wraps
from typing import Callable, Any, TypeVar, Optional

logger = logging.getLogger(__name__)

# 类型变量，用于保持装饰器的类型提示
T = TypeVar('T')


class ErrorType(str, Enum):
    """错误类型分类

    用于识别和分类不同类型的错误，以决定是否重试和如何处理
    """
    NETWORK = "network"       # 网络错误（可重试）
    TIMEOUT = "timeout"       # 超时错误（可重试）
    CONNECTION = "connection" # 连接错误（可重试）
    PARAMETER = "parameter"   # 参数错误（不可重试）
    BUSINESS = "business"     # 业务错误（不可重试）
    DATABASE = "database"     # 数据库错误（可重试）
    UNKNOWN = "unknown"       # 未知错误（不可重试）


def classify_error(error: Exception) -> ErrorType:
    """智能错误分类

    根据错误消息内容自动分类错误类型，用于决定是否应该重试。

    Args:
        error: 异常对象

    Returns:
        错误类型枚举值

    Examples:
        >>> classify_error(TimeoutError("Request timeout"))
        ErrorType.TIMEOUT

        >>> classify_error(ValueError("Invalid parameter"))
        ErrorType.PARAMETER
    """
    error_str = str(error).lower()
    error_type_name = type(error).__name__.lower()

    # 网络相关错误
    if any(keyword in error_str for keyword in ["network", "网络"]):
        return ErrorType.NETWORK

    # 连接相关错误
    if any(keyword in error_str for keyword in ["connection", "连接", "connect"]):
        return ErrorType.CONNECTION

    # 超时相关错误
    if any(keyword in error_str for keyword in ["timeout", "超时", "timed out"]):
        return ErrorType.TIMEOUT

    # 数据库相关错误
    if any(keyword in error_str for keyword in ["database", "数据库", "sql", "deadlock"]):
        return ErrorType.DATABASE

    # 参数相关错误
    if any(keyword in error_str for keyword in ["invalid", "参数", "parameter", "argument"]):
        return ErrorType.PARAMETER

    # 业务相关错误
    if any(keyword in error_str for keyword in ["章节不存在", "作品不存在", "权限不足", "not found"]):
        return ErrorType.BUSINESS

    # 根据异常类型判断
    if "timeout" in error_type_name:
        return ErrorType.TIMEOUT
    if "value" in error_type_name or "type" in error_type_name:
        return ErrorType.PARAMETER

    return ErrorType.UNKNOWN


def is_retryable_error(error: Exception) -> bool:
    """判断错误是否可重试

    🟢 直接复用Planning模式的判断逻辑 (langgraph_agent.py:3225-3227)

    Args:
        error: 异常对象

    Returns:
        True: 可重试, False: 不可重试
    """
    error_type = classify_error(error)

    # 可重试的错误类型
    retryable_types = {
        ErrorType.NETWORK,
        ErrorType.TIMEOUT,
        ErrorType.CONNECTION,
        ErrorType.DATABASE
    }

    return error_type in retryable_types


def retry_on_failure(
    max_retries: int = 2,
    backoff_base: int = 2,
    retryable_errors: Optional[tuple] = None
):
    """自动重试装饰器（复用Planning模式的重试逻辑）

    🟢 核心逻辑复用自 langgraph_agent.py:3178-3248

    为异步函数添加自动重试功能，支持：
    - 智能错误分类（可重试 vs 不可重试）
    - 指数退避策略（2, 4, 8秒...）
    - 详细的重试日志

    Args:
        max_retries: 最大重试次数（默认2次，总共3次尝试）
        backoff_base: 退避基数（默认2，即2^1, 2^2, 2^3秒）
        retryable_errors: 可重试的异常类型（None则自动判断）

    Returns:
        装饰后的函数

    Examples:
        >>> @retry_on_failure(max_retries=2)
        >>> async def read_from_db():
        >>>     # 数据库读取操作
        >>>     pass
    """
    def decorator(func: Callable[..., T]) -> Callable[..., T]:
        @wraps(func)
        async def wrapper(*args, **kwargs) -> T:
            last_error = None
            func_name = func.__name__

            for retry_count in range(max_retries + 1):
                try:
                    # 执行函数
                    result = await func(*args, **kwargs)

                    # 如果是重试后成功，记录日志
                    if retry_count > 0:
                        logger.info(
                            f"[Retry] {func_name} 重试{retry_count}次后成功"
                        )

                    return result

                except Exception as e:
                    last_error = e

                    # 判断是否为可重试的错误
                    if retryable_errors:
                        # 使用指定的异常类型
                        is_retryable = isinstance(e, retryable_errors)
                    else:
                        # 🟢 复用：自动判断（基于错误内容）
                        is_retryable = is_retryable_error(e)

                    error_type = classify_error(e)

                    if is_retryable and retry_count < max_retries:
                        # 🟢 复用：指数退避策略
                        wait_time = backoff_base ** (retry_count + 1)
                        logger.warning(
                            f"[Retry] {func_name} 失败 (错误类型: {error_type.value})，"
                            f"{wait_time}秒后重试 ({retry_count + 1}/{max_retries}): {e}"
                        )
                        await asyncio.sleep(wait_time)
                    else:
                        # 不可重试或已达最大次数
                        if is_retryable:
                            logger.error(
                                f"[Retry] {func_name} 重试{max_retries}次后仍失败: {e}"
                            )
                        else:
                            logger.error(
                                f"[Retry] {func_name} 遇到不可重试错误 ({error_type.value}): {e}"
                            )
                        raise last_error

            # 理论上不会到这里
            raise last_error

        return wrapper
    return decorator


# 🟢 便捷别名：与现有代码兼容
async def _retry_on_failure(func, *args, max_retries=2, **kwargs):
    """兼容性包装器：与现有的_retry_on_failure函数签名一致

    🟢 保持向后兼容 (langgraph_agent.py:95-123)

    Args:
        func: 要执行的异步函数
        max_retries: 最大重试次数
        *args, **kwargs: 传递给func的参数

    Returns:
        函数执行结果
    """
    retry_count = 0
    last_error = None

    while retry_count <= max_retries:
        try:
            result = await func(*args, **kwargs)
            return result

        except Exception as e:
            last_error = e
            error_type = classify_error(e)
            is_retryable = is_retryable_error(e)

            if is_retryable and retry_count < max_retries:
                retry_count += 1
                wait_time = 2 ** retry_count
                logger.warning(
                    f"[Retry] {func.__name__} 失败 (错误: {error_type.value})，"
                    f"{wait_time}秒后重试 ({retry_count}/{max_retries}): {e}"
                )
                await asyncio.sleep(wait_time)
            else:
                # 不可重试或已达最大次数
                logger.error(
                    f"[Retry] {func.__name__} 最终失败 (错误: {error_type.value}): {e}"
                )
                raise last_error

        retry_count += 1

    # 理论上不会到这里
    raise last_error


__all__ = [
    'ErrorType',
    'classify_error',
    'is_retryable_error',
    'retry_on_failure',
    '_retry_on_failure'  # 向后兼容
]
