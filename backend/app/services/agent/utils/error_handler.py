"""
统一错误处理器 - 提升系统稳定性和边界情况处理

提供统一的异常处理、重试机制、降级策略和错误恢复功能。
"""

import time
import asyncio
import logging
from typing import Any, Callable, Dict, Optional, Type, Union, List
from functools import wraps
from enum import Enum
from dataclasses import dataclass
from datetime import datetime

logger = logging.getLogger(__name__)


class ErrorSeverity(Enum):
    """错误严重程度"""
    LOW = "low"          # 轻微错误，不影响主流程
    MEDIUM = "medium"    # 中等错误，影响部分功能
    HIGH = "high"        # 严重错误，影响核心功能
    CRITICAL = "critical"  # 致命错误，需要立即处理


class ErrorCategory(Enum):
    """错误类别"""
    NETWORK = "network"          # 网络相关错误
    DATABASE = "database"        # 数据库相关错误
    REDIS = "redis"              # Redis相关错误
    LLM_SERVICE = "llm_service"  # LLM服务相关错误
    VALIDATION = "validation"    # 输入验证错误
    TIMEOUT = "timeout"          # 超时错误
    MEMORY = "memory"            # 内存相关错误
    BUSINESS = "business"        # 业务逻辑错误
    SYSTEM = "system"            # 系统级错误


@dataclass
class ErrorInfo:
    """错误信息"""
    category: ErrorCategory
    severity: ErrorSeverity
    message: str
    original_error: Exception
    context: Dict[str, Any]
    timestamp: datetime
    retry_count: int = 0
    user_id: Optional[str] = None
    conversation_id: Optional[str] = None
    action_name: Optional[str] = None


class RetryStrategy:
    """重试策略配置"""

    def __init__(
        self,
        max_attempts: int = 3,
        base_delay: float = 1.0,
        max_delay: float = 60.0,
        exponential_base: float = 2.0,
        jitter: bool = True
    ):
        self.max_attempts = max_attempts
        self.base_delay = base_delay
        self.max_delay = max_delay
        self.exponential_base = exponential_base
        self.jitter = jitter

    def get_delay(self, attempt: int) -> float:
        """计算重试延迟"""
        delay = self.base_delay * (self.exponential_base ** attempt)
        delay = min(delay, self.max_delay)

        if self.jitter:
            delay *= (0.5 + (hash(time.time()) % 100) / 200)  # 0.5-1.0倍随机

        return delay


class FallbackStrategy:
    """���级策略配置"""

    def __init__(
        self,
        fallback_enabled: bool = True,
        fallback_data: Optional[Dict[str, Any]] = None,
        fallback_function: Optional[Callable] = None
    ):
        self.fallback_enabled = fallback_enabled
        self.fallback_data = fallback_data or {}
        self.fallback_function = fallback_function


class ErrorHandler:
    """统一错误处理器"""

    def __init__(self):
        self.error_stats: Dict[ErrorCategory, int] = {cat: 0 for cat in ErrorCategory}
        self.error_history: List[ErrorInfo] = []
        self.max_history_size = 1000

    def classify_error(self, error: Exception, context: Dict[str, Any] = None) -> ErrorInfo:
        """分类错误并创建错误信息"""
        context = context or {}

        # 根据异常类型和消息确定错误类别
        if isinstance(error, (ConnectionError, TimeoutError)):
            category = ErrorCategory.NETWORK
            severity = ErrorSeverity.MEDIUM
        elif "redis" in str(type(error).__name__).lower() or "redis" in str(error).lower():
            category = ErrorCategory.REDIS
            severity = ErrorSeverity.MEDIUM
        elif "database" in str(error).lower() or "sql" in str(error).lower():
            category = ErrorCategory.DATABASE
            severity = ErrorSeverity.MEDIUM
        elif "timeout" in str(error).lower():
            category = ErrorCategory.TIMEOUT
            severity = ErrorSeverity.MEDIUM
        elif "memory" in str(error).lower() or "overflow" in str(error).lower():
            category = ErrorCategory.MEMORY
            severity = ErrorSeverity.HIGH
        elif isinstance(error, (ValueError, TypeError)):
            category = ErrorCategory.VALIDATION
            severity = ErrorSeverity.LOW
        else:
            category = ErrorCategory.SYSTEM
            severity = ErrorSeverity.HIGH

        return ErrorInfo(
            category=category,
            severity=severity,
            message=str(error),
            original_error=error,
            context=context,
            timestamp=datetime.now(),
            user_id=context.get("user_id"),
            conversation_id=context.get("conversation_id"),
            action_name=context.get("action_name")
        )

    def handle_error(self, error_info: ErrorInfo) -> Dict[str, Any]:
        """处理错误"""
        # 更新统计
        self.error_stats[error_info.category] += 1

        # 记录历史
        self.error_history.append(error_info)
        if len(self.error_history) > self.max_history_size:
            self.error_history = self.error_history[-self.max_history_size:]

        # 结构化日志
        self._log_error(error_info)

        # 错误处理逻辑
        if error_info.severity == ErrorSeverity.CRITICAL:
            logger.critical(f"Critical error occurred: {error_info.message}")
            return {"status": "error", "should_retry": False, "error": error_info}
        elif error_info.severity == ErrorSeverity.HIGH:
            logger.error(f"High severity error: {error_info.message}")
            return {"status": "error", "should_retry": True, "error": error_info}
        else:
            logger.warning(f"Medium/Low severity error: {error_info.message}")
            return {"status": "warning", "should_retry": True, "error": error_info}

    def _log_error(self, error_info: ErrorInfo):
        """记录结构化错误日志"""
        log_data = {
            "error_category": error_info.category.value,
            "error_severity": error_info.severity.value,
            "error_message": error_info.message,
            "error_type": type(error_info.original_error).__name__,
            "context": error_info.context,
            "timestamp": error_info.timestamp.isoformat(),
            "retry_count": error_info.retry_count,
            "user_id": error_info.user_id,
            "conversation_id": error_info.conversation_id,
            "action_name": error_info.action_name
        }

        if error_info.severity in [ErrorSeverity.HIGH, ErrorSeverity.CRITICAL]:
            logger.error(f"Agent error: {log_data}")
        else:
            logger.warning(f"Agent warning: {log_data}")

    def get_error_summary(self) -> Dict[str, Any]:
        """获取错误统计摘要"""
        recent_errors = [
            e for e in self.error_history
            if (datetime.now() - e.timestamp).total_seconds() < 3600
        ]

        return {
            "total_errors": len(self.error_history),
            "recent_errors": len(recent_errors),
            "error_by_category": dict(self.error_stats),
            "error_rate_per_hour": len(recent_errors),
            "last_error_time": self.error_history[-1].timestamp.isoformat() if self.error_history else None
        }


# 全局错误处理器实例
global_error_handler = ErrorHandler()


def robust_retry(
    max_attempts: int = 3,
    delay: float = 1.0,
    backoff: float = 2.0,
    exceptions: Union[Type[Exception], tuple] = Exception,
    fallback_result: Any = None,
    log_context: Dict[str, Any] = None
):
    """
    健壮的重试装饰器

    Args:
        max_attempts: 最大重试次数
        delay: 初��延迟秒数
        backoff: 延迟倍数
        exceptions: 需要重试的异常类型
        fallback_result: 重试失败时的降级返回值
        log_context: 日志上下文信息
    """
    def decorator(func: Callable):
        @wraps(func)
        async def async_wrapper(*args, **kwargs):
            last_exception = None

            for attempt in range(max_attempts):
                try:
                    return await func(*args, **kwargs)
                except exceptions as e:
                    last_exception = e

                    # 创建错误信息
                    error_info = global_error_handler.classify_error(
                        e, log_context or {}
                    )
                    error_info.retry_count = attempt

                    # 处理错误
                    result = global_error_handler.handle_error(error_info)

                    if attempt < max_attempts - 1:
                        # 计算延迟时间
                        current_delay = delay * (backoff ** attempt)
                        logger.warning(
                            f"Retry {attempt + 1}/{max_attempts} for {func.__name__} "
                            f"in {current_delay:.2f}s. Error: {e}"
                        )
                        await asyncio.sleep(current_delay)
                    else:
                        logger.error(f"All {max_attempts} attempts failed for {func.__name__}")

            # 所有重试都失败，返回降级结果
            if fallback_result is not None:
                logger.warning(f"Using fallback result for {func.__name__}")
                return fallback_result
            else:
                raise last_exception

        @wraps(func)
        def sync_wrapper(*args, **kwargs):
            last_exception = None

            for attempt in range(max_attempts):
                try:
                    return func(*args, **kwargs)
                except exceptions as e:
                    last_exception = e

                    # 创建错误信息
                    error_info = global_error_handler.classify_error(
                        e, log_context or {}
                    )
                    error_info.retry_count = attempt

                    # 处理错误
                    global_error_handler.handle_error(error_info)

                    if attempt < max_attempts - 1:
                        current_delay = delay * (backoff ** attempt)
                        logger.warning(
                            f"Retry {attempt + 1}/{max_attempts} for {func.__name__} "
                            f"in {current_delay:.2f}s. Error: {e}"
                        )
                        time.sleep(current_delay)
                    else:
                        logger.error(f"All {max_attempts} attempts failed for {func.__name__}")

            # 所有重试都失败，返回降级结果
            if fallback_result is not None:
                logger.warning(f"Using fallback result for {func.__name__}")
                return fallback_result
            else:
                raise last_exception

        # 根据函数类型返回对应的包装器
        if asyncio.iscoroutinefunction(func):
            return async_wrapper
        else:
            return sync_wrapper

    return decorator


def circuit_breaker(
    failure_threshold: int = 5,
    recovery_timeout: float = 60.0,
    expected_exception: Type[Exception] = Exception
):
    """
    熔断器装饰器 - 防止级联失败

    Args:
        failure_threshold: 失败次数阈值
        recovery_timeout: 恢复超时时间
        expected_exception: 预期的异常类型
    """
    class CircuitBreakerState:
        def __init__(self):
            self.failure_count = 0
            self.last_failure_time = None
            self.state = "closed"  # closed, open, half_open

    state = CircuitBreakerState()

    def decorator(func: Callable):
        @wraps(func)
        async def async_wrapper(*args, **kwargs):
            # 检查熔断器状态
            if state.state == "open":
                if time.time() - state.last_failure_time > recovery_timeout:
                    state.state = "half_open"
                    logger.info(f"Circuit breaker half-open for {func.__name__}")
                else:
                    logger.warning(f"Circuit breaker open for {func.__name__}")
                    raise RuntimeError(f"Circuit breaker is open for {func.__name__}")

            try:
                result = await func(*args, **kwargs)

                # 成功执行，重置计数器
                if state.state == "half_open":
                    state.state = "closed"
                    state.failure_count = 0
                    logger.info(f"Circuit breaker closed for {func.__name__}")

                return result

            except expected_exception as e:
                state.failure_count += 1
                state.last_failure_time = time.time()

                if state.failure_count >= failure_threshold:
                    state.state = "open"
                    logger.error(f"Circuit breaker opened for {func.__name__} after {state.failure_count} failures")

                raise e

        @wraps(func)
        def sync_wrapper(*args, **kwargs):
            # 检查熔断器状态
            if state.state == "open":
                if time.time() - state.last_failure_time > recovery_timeout:
                    state.state = "half_open"
                    logger.info(f"Circuit breaker half-open for {func.__name__}")
                else:
                    logger.warning(f"Circuit breaker open for {func.__name__}")
                    raise RuntimeError(f"Circuit breaker is open for {func.__name__}")

            try:
                result = func(*args, **kwargs)

                # 成功执行，重置计数器
                if state.state == "half_open":
                    state.state = "closed"
                    state.failure_count = 0
                    logger.info(f"Circuit breaker closed for {func.__name__}")

                return result

            except expected_exception as e:
                state.failure_count += 1
                state.last_failure_time = time.time()

                if state.failure_count >= failure_threshold:
                    state.state = "open"
                    logger.error(f"Circuit breaker opened for {func.__name__} after {state.failure_count} failures")

                raise e

        # 根据函数类型返回对应的包装器
        if asyncio.iscoroutinefunction(func):
            return async_wrapper
        else:
            return sync_wrapper

    return decorator


def timeout_handler(timeout_seconds: float):
    """
    超时处理装饰器

    Args:
        timeout_seconds: 超时时间（秒）
    """
    def decorator(func: Callable):
        @wraps(func)
        async def async_wrapper(*args, **kwargs):
            try:
                return await asyncio.wait_for(func(*args, **kwargs), timeout=timeout_seconds)
            except asyncio.TimeoutError:
                error_info = ErrorInfo(
                    category=ErrorCategory.TIMEOUT,
                    severity=ErrorSeverity.MEDIUM,
                    message=f"Function {func.__name__} timed out after {timeout_seconds} seconds",
                    original_error=asyncio.TimeoutError(),
                    context={"timeout_seconds": timeout_seconds},
                    timestamp=datetime.now()
                )
                global_error_handler.handle_error(error_info)
                raise TimeoutError(f"Function {func.__name__} timed out after {timeout_seconds} seconds")

        @wraps(func)
        def sync_wrapper(*args, **kwargs):
            import signal

            def timeout_handler(signum, frame):
                raise TimeoutError(f"Function {func.__name__} timed out after {timeout_seconds} seconds")

            # 设置超时信号
            signal.signal(signal.SIGALRM, timeout_handler)
            signal.alarm(int(timeout_seconds))

            try:
                result = func(*args, **kwargs)
                signal.alarm(0)  # 取消超时
                return result
            except TimeoutError as e:
                error_info = ErrorInfo(
                    category=ErrorCategory.TIMEOUT,
                    severity=ErrorSeverity.MEDIUM,
                    message=str(e),
                    original_error=e,
                    context={"timeout_seconds": timeout_seconds},
                    timestamp=datetime.now()
                )
                global_error_handler.handle_error(error_info)
                raise

        # 根据函数类型返回对应的包装器
        if asyncio.iscoroutinefunction(func):
            return async_wrapper
        else:
            return sync_wrapper

    return decorator


def safe_execute(
    func: Callable,
    *args,
    fallback_result: Any = None,
    log_errors: bool = True,
    context: Dict[str, Any] = None,
    **kwargs
) -> Any:
    """
    安全执行函数，捕获所有异常

    Args:
        func: 要执行的函数
        *args: 函数参数
        fallback_result: 出错时的降级返回值
        log_errors: 是否记录错误
        context: 上下文信息
        **kwargs: 函数关键字参数
    """
    try:
        return func(*args, **kwargs)
    except Exception as e:
        if log_errors:
            error_info = global_error_handler.classify_error(e, context or {})
            global_error_handler.handle_error(error_info)

        return fallback_result


async def safe_execute_async(
    func: Callable,
    *args,
    fallback_result: Any = None,
    log_errors: bool = True,
    context: Dict[str, Any] = None,
    **kwargs
) -> Any:
    """
    安全执行异步函数，捕获所有异常

    Args:
        func: 要执行的异步函数
        *args: 函数参数
        fallback_result: 出错时的降级返回值
        log_errors: 是否记录错误
        context: 上下文信息
        **kwargs: 函数关键字参数
    """
    try:
        return await func(*args, **kwargs)
    except Exception as e:
        if log_errors:
            error_info = global_error_handler.classify_error(e, context or {})
            global_error_handler.handle_error(error_info)

        return fallback_result