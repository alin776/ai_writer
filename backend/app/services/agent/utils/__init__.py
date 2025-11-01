"""
Agent Utils 工具模块

提供统一的工具类和辅助函数，包括：
- 错误处理和重试机制
- 日志系统
- 配置管理
- 性能监控
"""

from .error_handler import (
    ErrorHandler,
    ErrorInfo,
    ErrorSeverity,
    ErrorCategory,
    RetryStrategy,
    FallbackStrategy,
    global_error_handler,
    robust_retry,
    circuit_breaker,
    timeout_handler,
    safe_execute,
    safe_execute_async
)

from .logger import (
    AgentLogger,
    get_logger,
    setup_logging,
    log_performance,
    log_operation_context,
    default_logger
)

__all__ = [
    # 错误处理
    "ErrorHandler",
    "ErrorInfo",
    "ErrorSeverity",
    "ErrorCategory",
    "RetryStrategy",
    "FallbackStrategy",
    "global_error_handler",
    "robust_retry",
    "circuit_breaker",
    "timeout_handler",
    "safe_execute",
    "safe_execute_async",

    # 日志系统
    "AgentLogger",
    "get_logger",
    "setup_logging",
    "log_performance",
    "log_operation_context",
    "default_logger"
]