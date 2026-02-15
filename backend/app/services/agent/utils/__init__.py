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

from .performance import (
    MemoryCache,
    IndexManager,
    BatchProcessor,
    PerformanceOptimizer,
    get_performance_optimizer,
    cache_result,
    parallel_execute,
    clear_all_caches,
    get_performance_summary,
    performance_optimizer
)

from .llm_optimizer import (
    LLMOptimizer,
    get_llm_optimizer,
    optimized_llm_call,
    clear_llm_cache,
    get_llm_performance_stats
)

from .context_builder import (
    _compress_task_result,
    _build_summarization_context,
    _build_knowledge_system_messages,
    _build_worldview_system_messages
)

from .tool_helpers import (
    resolve_version_reference,
    normalize_tool_params
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
    "default_logger",

    # 性能优化
    "MemoryCache",
    "IndexManager",
    "BatchProcessor",
    "PerformanceOptimizer",
    "get_performance_optimizer",
    "cache_result",
    "parallel_execute",
    "clear_all_caches",
    "get_performance_summary",
    "performance_optimizer",

    # LLM优化
    "LLMOptimizer",
    "get_llm_optimizer",
    "optimized_llm_call",
    "clear_llm_cache",
    "get_llm_performance_stats",

    # 上下文构建
    "_compress_task_result",
    "_build_summarization_context",
    "_build_knowledge_system_messages",
    "_build_worldview_system_messages",

    # 工具辅助
    "resolve_version_reference",
    "normalize_tool_params",
]