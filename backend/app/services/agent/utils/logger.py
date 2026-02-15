"""
Agent 结构化日志系统

提供统一的、结构化的日志记录，便于调试、监控和分析。
"""

import logging
import json
import time
from typing import Dict, Any, Optional
from datetime import datetime
from functools import wraps
import traceback
import asyncio
from contextlib import asynccontextmanager
from app.utils.datetime_utils import get_utc_now

# 尝试导入 structlog，如果不可用则使用标准 logging
try:
    import structlog
    STRUCTLOG_AVAILABLE = True
except ImportError:
    STRUCTLOG_AVAILABLE = False


class AgentLogger:
    """
    Agent 专用日志记录器

    支持结构化日志、性能追踪和异步操作
    """

    def __init__(
        self,
        name: str,
        level: str = "INFO",
        structured: bool = True,
        enable_performance: bool = True
    ):
        self.name = name
        self.level = getattr(logging, level.upper())
        self.structured = structured and STRUCTLOG_AVAILABLE
        self.enable_performance = enable_performance

        # 创建标准 logger
        self.logger = logging.getLogger(name)
        self.logger.setLevel(self.level)

        # 创建 structlog logger（如果可用）
        if self.structured:
            self.struct_logger = structlog.get_logger(name)
        else:
            self.struct_logger = None

        # 性能追踪数据
        self.performance_data = {}

    def _format_structured_log(
        self,
        level: str,
        message: str,
        **kwargs
    ) -> Dict[str, Any]:
        """格式化结构化日志"""
        log_entry = {
            "timestamp": get_utc_now().isoformat() + "Z",
            "level": level,
            "logger": self.name,
            "message": message,
            **kwargs
        }

        # 添加性能数据（如果启用）
        if self.enable_performance and "duration" not in kwargs:
            log_entry["performance"] = self.performance_data

        return log_entry

    def _log_structured(
        self,
        level: str,
        message: str,
        **kwargs
    ):
        """记录结构化日志"""
        if self.struct_logger:
            log_method = getattr(self.struct_logger, level.lower(), self.struct_logger.info)
            log_method(message, **kwargs)
        else:
            # 降级到标准日志
            log_entry = self._format_structured_log(level, message, **kwargs)
            log_method = getattr(self.logger, level.lower(), self.logger.info)
            log_method(json.dumps(log_entry, ensure_ascii=False))

    def info(self, message: str, **kwargs):
        """记录信息日志"""
        if self.structured:
            self._log_structured("INFO", message, **kwargs)
        else:
            self.logger.info(message)

    def warning(self, message: str, **kwargs):
        """记录警告日志"""
        if self.structured:
            self._log_structured("WARNING", message, **kwargs)
        else:
            self.logger.warning(message)

    def error(self, message: str, **kwargs):
        """记录错误日志"""
        if "error" not in kwargs:
            kwargs["error"] = True

        if "exception" in kwargs:
            kwargs["traceback"] = traceback.format_exc()

        if self.structured:
            self._log_structured("ERROR", message, **kwargs)
        else:
            self.logger.error(message)

    def debug(self, message: str, **kwargs):
        """记录调试日志"""
        if self.structured:
            self._log_structured("DEBUG", message, **kwargs)
        else:
            self.logger.debug(message)

    def critical(self, message: str, **kwargs):
        """记录严重错误日志"""
        if "critical" not in kwargs:
            kwargs["critical"] = True

        if "exception" in kwargs:
            kwargs["traceback"] = traceback.format_exc()

        if self.structured:
            self._log_structured("CRITICAL", message, **kwargs)
        else:
            self.logger.critical(message)

    # ==================== 业务日志方法 ====================

    def log_action_start(
        self,
        action_name: str,
        user_id: Optional[str] = None,
        conversation_id: Optional[str] = None,
        **kwargs
    ):
        """记录 Action 开始"""
        self.info(
            f"Action started: {action_name}",
            action_name=action_name,
            user_id=user_id,
            conversation_id=conversation_id,
            event_type="action_started",
            **kwargs
        )

    def log_action_complete(
        self,
        action_name: str,
        duration: float,
        success: bool = True,
        user_id: Optional[str] = None,
        conversation_id: Optional[str] = None,
        **kwargs
    ):
        """记录 Action 完成"""
        self.info(
            f"Action completed: {action_name}",
            action_name=action_name,
            duration=duration,
            success=success,
            user_id=user_id,
            conversation_id=conversation_id,
            event_type="action_completed",
            **kwargs
        )

    def log_action_error(
        self,
        action_name: str,
        error: Exception,
        user_id: Optional[str] = None,
        conversation_id: Optional[str] = None,
        **kwargs
    ):
        """记录 Action 错误"""
        self.error(
            f"Action failed: {action_name}",
            action_name=action_name,
            error_type=type(error).__name__,
            error_message=str(error),
            user_id=user_id,
            conversation_id=conversation_id,
            event_type="action_failed",
            exception=error,
            **kwargs
        )

    def log_tool_call(
        self,
        tool_name: str,
        parameters: Dict[str, Any],
        result: Any,
        duration: float,
        success: bool = True,
        **kwargs
    ):
        """记录工具调用"""
        self.info(
            f"Tool call: {tool_name}",
            tool_name=tool_name,
            parameters=parameters,
            result_type=type(result).__name__,
            duration=duration,
            success=success,
            event_type="tool_call",
            **kwargs
        )

    def log_llm_call(
        self,
        model: str,
        tokens_used: Dict[str, int],
        cost: float,
        duration: float,
        success: bool = True,
        **kwargs
    ):
        """记录 LLM 调用"""
        self.info(
            f"LLM call: {model}",
            model=model,
            tokens_used=tokens_used,
            cost=cost,
            duration=duration,
            success=success,
            event_type="llm_call",
            **kwargs
        )

    def log_memory_operation(
        self,
        operation: str,
        user_id: str,
        memory_count: Optional[int] = None,
        **kwargs
    ):
        """记录 Memory 操作"""
        self.info(
            f"Memory operation: {operation}",
            operation=operation,
            user_id=user_id,
            memory_count=memory_count,
            event_type="memory_operation",
            **kwargs
        )

    def log_quality_evaluation(
        self,
        content_id: str,
        overall_score: float,
        dimension_scores: Dict[str, float],
        passes: bool,
        **kwargs
    ):
        """记录质量评估"""
        self.info(
            f"Quality evaluation: {overall_score:.2f}",
            content_id=content_id,
            overall_score=overall_score,
            dimension_scores=dimension_scores,
            passes=passes,
            event_type="quality_evaluation",
            **kwargs
        )


# ==================== 性能监控装饰器 ====================

def log_performance(
    logger: AgentLogger,
    operation_name: str,
    log_args: bool = True,
    log_result: bool = False
):
    """
    性能监控装饰器

    Args:
        logger: 日志记录器
        operation_name: 操作名称
        log_args: 是否记录参数
        log_result: 是否记录结果
    """
    def decorator(func):
        @wraps(func)
        async def async_wrapper(*args, **kwargs):
            start_time = time.time()
            operation_id = f"{operation_name}_{start_time}"

            # 记录开始
            logger.info(
                f"Operation started: {operation_name}",
                operation_name=operation_name,
                operation_id=operation_id,
                args=args if log_args else None,
                kwargs=kwargs if log_args else None,
                event_type="operation_started"
            )

            try:
                result = await func(*args, **kwargs)
                duration = time.time() - start_time

                # 记录完成
                logger.info(
                    f"Operation completed: {operation_name}",
                    operation_name=operation_name,
                    operation_id=operation_id,
                    duration=duration,
                    success=True,
                    result_type=type(result).__name__ if log_result else None,
                    event_type="operation_completed"
                )

                return result

            except Exception as e:
                duration = time.time() - start_time

                # 记录失败
                logger.error(
                    f"Operation failed: {operation_name}",
                    operation_name=operation_name,
                    operation_id=operation_id,
                    duration=duration,
                    success=False,
                    error_type=type(e).__name__,
                    error_message=str(e),
                    exception=e,
                    event_type="operation_failed"
                )

                raise

        @wraps(func)
        def sync_wrapper(*args, **kwargs):
            start_time = time.time()
            operation_id = f"{operation_name}_{start_time}"

            # 记录开始
            logger.info(
                f"Operation started: {operation_name}",
                operation_name=operation_name,
                operation_id=operation_id,
                args=args if log_args else None,
                kwargs=kwargs if log_args else None,
                event_type="operation_started"
            )

            try:
                result = func(*args, **kwargs)
                duration = time.time() - start_time

                # 记录完成
                logger.info(
                    f"Operation completed: {operation_name}",
                    operation_name=operation_name,
                    operation_id=operation_id,
                    duration=duration,
                    success=True,
                    result_type=type(result).__name__ if log_result else None,
                    event_type="operation_completed"
                )

                return result

            except Exception as e:
                duration = time.time() - start_time

                # 记录失败
                logger.error(
                    f"Operation failed: {operation_name}",
                    operation_name=operation_name,
                    operation_id=operation_id,
                    duration=duration,
                    success=False,
                    error_type=type(e).__name__,
                    error_message=str(e),
                    exception=e,
                    event_type="operation_failed"
                )

                raise

        # 根据函数类型返回对应的包装器
        if asyncio.iscoroutinefunction(func):
            return async_wrapper
        else:
            return sync_wrapper

    return decorator


@asynccontextmanager
async def log_operation_context(
    logger: AgentLogger,
    operation_name: str,
    **context
):
    """
    操作上下文管理器

    Args:
        logger: 日志记录器
        operation_name: 操作名称
        **context: 上下文信息
    """
    start_time = time.time()
    operation_id = f"{operation_name}_{start_time}"

    # 记录开始
    logger.info(
        f"Operation started: {operation_name}",
        operation_name=operation_name,
        operation_id=operation_id,
        **context,
        event_type="operation_started"
    )

    try:
        yield operation_id

        # 记录完成
        duration = time.time() - start_time
        logger.info(
            f"Operation completed: {operation_name}",
            operation_name=operation_name,
            operation_id=operation_id,
            duration=duration,
            success=True,
            **context,
            event_type="operation_completed"
        )

    except Exception as e:
        # 记录失败
        duration = time.time() - start_time
        logger.error(
            f"Operation failed: {operation_name}",
            operation_name=operation_name,
            operation_id=operation_id,
            duration=duration,
            success=False,
            error_type=type(e).__name__,
            error_message=str(e),
            exception=e,
            **context,
            event_type="operation_failed"
        )

        raise


# ==================== 全局日志记录器 ====================

# 创建默认日志记录器
default_logger = AgentLogger("agent")


def get_logger(name: str, **kwargs) -> AgentLogger:
    """
    获取日志记录器实例

    Args:
        name: 日志记录器名称
        **kwargs: 其他配置参数

    Returns:
        AgentLogger: 日志记录器实例
    """
    return AgentLogger(name, **kwargs)


def setup_logging(
    level: str = "INFO",
    structured: bool = True,
    format_string: Optional[str] = None
):
    """
    设置全局日志配置

    Args:
        level: 日志级别
        structured: 是否启用结构化日志
        format_string: 自定义格式字符串
    """
    if STRUCTLOG_AVAILABLE and structured:
        # 配置 structlog
        structlog.configure(
            processors=[
                structlog.stdlib.filter_by_level,
                structlog.stdlib.add_logger_name,
                structlog.stdlib.add_log_level,
                structlog.stdlib.PositionalArgumentsFormatter(),
                structlog.processors.TimeStamper(fmt="iso"),
                structlog.processors.StackInfoRenderer(),
                structlog.processors.format_exc_info,
                structlog.processors.UnicodeDecoder(),
                structlog.processors.JSONRenderer()
            ],
            context_class=dict,
            logger_factory=structlog.stdlib.LoggerFactory(),
            wrapper_class=structlog.stdlib.BoundLogger,
            cache_logger_on_first_use=True,
        )
    else:
        # 配置标准 logging
        logging.basicConfig(
            level=getattr(logging, level.upper()),
            format=format_string or "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S"
        )


# 导出常用功能
__all__ = [
    "AgentLogger",
    "get_logger",
    "setup_logging",
    "log_performance",
    "log_operation_context",
    "default_logger"
]
