"""
✅ P3-1修复: 增强日志记录系统

提供详细的记忆操作日志，包括：
- 操作类型和详细信息
- 性能指标（耗时、内存使用）
- 遗忘原因和决策过程
- Redis操作统计
- 异常和错误追踪
"""
import logging
import time
import functools
from typing import Dict, Any, Optional, List, Callable
from datetime import datetime, timezone
from enum import Enum
import json
import traceback


class LogLevel(Enum):
    """日志级别"""
    DEBUG = "DEBUG"
    INFO = "INFO"
    WARNING = "WARNING"
    ERROR = "ERROR"
    CRITICAL = "CRITICAL"


class OperationType(Enum):
    """操作类型"""
    ADD_MEMORY = "add_memory"
    RETRIEVE_MEMORY = "retrieve_memory"
    UPDATE_MEMORY = "update_memory"
    DELETE_MEMORY = "delete_memory"
    FORGET_MEMORY = "forget_memory"
    COMPRESS_MEMORY = "compress_memory"
    DEDUPLICATE = "deduplicate"
    ADJUST_IMPORTANCE = "adjust_importance"
    CREATE_VERSION = "create_version"
    ROLLBACK_VERSION = "rollback_version"
    EXPORT_MEMORY = "export_memory"
    IMPORT_MEMORY = "import_memory"
    REDIS_OPERATION = "redis_operation"


class MemoryLogger:
    """增强的记忆日志记录器"""

    def __init__(self, logger_name: str = "memory_system"):
        self.logger = logging.getLogger(logger_name)
        self._setup_logger()

    def _setup_logger(self):
        """配置日志器"""
        if not self.logger.handlers:
            handler = logging.StreamHandler()
            formatter = logging.Formatter(
                '[%(asctime)s] %(levelname)s [%(name)s:%(lineno)d] %(message)s',
                datefmt='%Y-%m-%d %H:%M:%S'
            )
            handler.setFormatter(formatter)
            self.logger.addHandler(handler)
            self.logger.setLevel(logging.INFO)

    def log_operation(
        self,
        operation: OperationType,
        user_id: str,
        details: Dict[str, Any],
        level: LogLevel = LogLevel.INFO,
        duration_ms: Optional[float] = None,
        success: bool = True,
        error: Optional[str] = None
    ):
        """
        记录操作日志

        Args:
            operation: 操作类型
            user_id: 用户ID
            details: 操作详细信息
            level: 日志级别
            duration_ms: 操作耗时（毫秒）
            success: 是否成功
            error: 错误信息
        """
        log_data = {
            "operation": operation.value,
            "user_id": user_id,
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "success": success,
            **details
        }

        if duration_ms is not None:
            log_data["duration_ms"] = round(duration_ms, 2)

        if error:
            log_data["error"] = error

        message = self._format_message(log_data)

        log_method = getattr(self.logger, level.value.lower())
        log_method(message)

    def _format_message(self, data: Dict[str, Any]) -> str:
        """格式化日志消息"""
        operation = data.get("operation", "unknown")
        user_id = data.get("user_id", "unknown")
        success = "✓" if data.get("success", True) else "✗"

        parts = [f"[{operation}] {success} user={user_id}"]

        # 添加耗时
        if "duration_ms" in data:
            parts.append(f"duration={data['duration_ms']}ms")

        # 添加关键信息
        for key, value in data.items():
            if key not in ["operation", "user_id", "timestamp", "success", "duration_ms", "error"]:
                if isinstance(value, (list, dict)):
                    parts.append(f"{key}={json.dumps(value, ensure_ascii=False)[:100]}")
                else:
                    parts.append(f"{key}={value}")

        # 添加错误信息
        if "error" in data:
            parts.append(f"error={data['error']}")

        return " | ".join(parts)

    def log_memory_add(
        self,
        user_id: str,
        memory_id: str,
        content_length: int,
        importance: float,
        layer: str,
        duration_ms: float
    ):
        """记录添加记忆操作"""
        self.log_operation(
            operation=OperationType.ADD_MEMORY,
            user_id=user_id,
            details={
                "memory_id": memory_id,
                "content_length": content_length,
                "importance": round(importance, 3),
                "layer": layer
            },
            duration_ms=duration_ms
        )

    def log_memory_retrieve(
        self,
        user_id: str,
        query: Optional[str],
        result_count: int,
        total_available: int,
        duration_ms: float,
        retrieval_method: str = "basic"
    ):
        """记录检索记忆操作"""
        self.log_operation(
            operation=OperationType.RETRIEVE_MEMORY,
            user_id=user_id,
            details={
                "query": query[:50] if query else None,
                "result_count": result_count,
                "total_available": total_available,
                "retrieval_method": retrieval_method,
                "hit_rate": f"{result_count/max(total_available, 1)*100:.1f}%"
            },
            duration_ms=duration_ms
        )

    def log_memory_forget(
        self,
        user_id: str,
        memory_id: str,
        reason: str,
        forget_score: float,
        age_days: float,
        importance: float,
        access_count: int,
        duration_ms: float
    ):
        """
        记录遗忘操作（详细记录遗忘原因）

        这是P3-1的重点：详细记录为什么某个记忆被遗忘
        """
        self.log_operation(
            operation=OperationType.FORGET_MEMORY,
            user_id=user_id,
            details={
                "memory_id": memory_id,
                "reason": reason,
                "forget_score": round(forget_score, 3),
                "age_days": round(age_days, 1),
                "importance": round(importance, 3),
                "access_count": access_count,
                "decision": self._format_forget_decision(
                    forget_score, age_days, importance, access_count
                )
            },
            duration_ms=duration_ms,
            level=LogLevel.INFO
        )

    def _format_forget_decision(
        self,
        score: float,
        age: float,
        importance: float,
        access: int
    ) -> str:
        """格式化遗忘决策信息"""
        reasons = []
        if age > 30:
            reasons.append(f"aged({age:.1f}d)")
        if importance < 0.3:
            reasons.append(f"low_importance({importance:.2f})")
        if access < 2:
            reasons.append(f"rarely_accessed({access})")
        if score > 0.8:
            reasons.append(f"high_score({score:.2f})")
        return "+".join(reasons) if reasons else "normal"

    def log_importance_adjustment(
        self,
        user_id: str,
        memory_id: str,
        old_importance: float,
        new_importance: float,
        adjustment_type: str,
        factors: Dict[str, float],
        duration_ms: float
    ):
        """记录重要度调整操作"""
        delta = new_importance - old_importance
        self.log_operation(
            operation=OperationType.ADJUST_IMPORTANCE,
            user_id=user_id,
            details={
                "memory_id": memory_id,
                "old_importance": round(old_importance, 3),
                "new_importance": round(new_importance, 3),
                "delta": f"{delta:+.3f}",
                "adjustment_type": adjustment_type,
                "factors": {k: round(v, 3) for k, v in factors.items()}
            },
            duration_ms=duration_ms
        )

    def log_redis_operation(
        self,
        operation: str,
        key_pattern: str,
        success: bool,
        duration_ms: float,
        error: Optional[str] = None,
        metadata: Optional[Dict[str, Any]] = None
    ):
        """
        记录Redis操作性能指标

        这是P3-1的重点：记录Redis操作的性能
        """
        details = {
            "redis_op": operation,
            "key_pattern": key_pattern,
            "performance": self._classify_performance(duration_ms)
        }

        if metadata:
            details.update(metadata)

        self.log_operation(
            operation=OperationType.REDIS_OPERATION,
            user_id="system",
            details=details,
            duration_ms=duration_ms,
            success=success,
            error=error,
            level=LogLevel.WARNING if duration_ms > 1000 else LogLevel.DEBUG
        )

    def _classify_performance(self, duration_ms: float) -> str:
        """分类性能等级"""
        if duration_ms < 10:
            return "excellent"
        elif duration_ms < 50:
            return "good"
        elif duration_ms < 200:
            return "acceptable"
        elif duration_ms < 1000:
            return "slow"
        else:
            return "critical"

    def log_batch_operation(
        self,
        operation: OperationType,
        user_id: str,
        total_count: int,
        success_count: int,
        failed_count: int,
        duration_ms: float,
        errors: Optional[List[str]] = None
    ):
        """记录批量操作"""
        self.log_operation(
            operation=operation,
            user_id=user_id,
            details={
                "total": total_count,
                "success": success_count,
                "failed": failed_count,
                "success_rate": f"{success_count/max(total_count, 1)*100:.1f}%",
                "avg_time_ms": round(duration_ms / max(total_count, 1), 2),
                "errors_sample": errors[:3] if errors else None
            },
            duration_ms=duration_ms,
            level=LogLevel.WARNING if failed_count > 0 else LogLevel.INFO
        )

    def log_error(
        self,
        operation: OperationType,
        user_id: str,
        error: Exception,
        context: Dict[str, Any]
    ):
        """记录错误和异常"""
        self.log_operation(
            operation=operation,
            user_id=user_id,
            details={
                "error_type": type(error).__name__,
                "error_message": str(error),
                "traceback": traceback.format_exc(),
                **context
            },
            success=False,
            level=LogLevel.ERROR
        )

    def log_performance_metrics(
        self,
        user_id: str,
        metrics: Dict[str, Any]
    ):
        """记录性能指标"""
        self.logger.info(
            f"[Performance Metrics] user={user_id} | "
            + " | ".join(f"{k}={v}" for k, v in metrics.items())
        )


# 全局日志实例
_global_logger: Optional[MemoryLogger] = None


def get_memory_logger() -> MemoryLogger:
    """获取全局记忆日志实例"""
    global _global_logger
    if _global_logger is None:
        _global_logger = MemoryLogger()
    return _global_logger


def set_memory_logger(logger: MemoryLogger):
    """设置全局记忆日志实例"""
    global _global_logger
    _global_logger = logger


def log_memory_operation(operation: OperationType):
    """
    装饰器：自动记录记忆操作的日志和性能

    使用示例:
        @log_memory_operation(OperationType.ADD_MEMORY)
        async def add_memory(user_id, content):
            ...
    """
    def decorator(func: Callable):
        @functools.wraps(func)
        async def wrapper(*args, **kwargs):
            logger = get_memory_logger()
            start_time = time.time()

            # 提取user_id
            user_id = kwargs.get('user_id') or (args[0] if args else 'unknown')

            try:
                result = await func(*args, **kwargs)
                duration_ms = (time.time() - start_time) * 1000

                # 记录成功操作
                logger.log_operation(
                    operation=operation,
                    user_id=str(user_id),
                    details={"function": func.__name__},
                    duration_ms=duration_ms,
                    success=True
                )

                return result

            except Exception as e:
                duration_ms = (time.time() - start_time) * 1000

                # 记录失败操作
                logger.log_error(
                    operation=operation,
                    user_id=str(user_id),
                    error=e,
                    context={
                        "function": func.__name__,
                        "duration_ms": round(duration_ms, 2)
                    }
                )
                raise

        return wrapper
    return decorator


class StructuredLogger:
    """结构化日志记录器（支持JSON格式）"""

    def __init__(self, logger_name: str = "memory_structured"):
        self.logger = logging.getLogger(logger_name)
        self._setup_logger()

    def _setup_logger(self):
        """配置日志器"""
        if not self.logger.handlers:
            handler = logging.StreamHandler()
            # 使用JSON格式
            formatter = logging.Formatter('%(message)s')
            handler.setFormatter(formatter)
            self.logger.addHandler(handler)
            self.logger.setLevel(logging.INFO)

    def log_json(self, data: Dict[str, Any], level: str = "INFO"):
        """记录JSON格式日志"""
        log_entry = {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "level": level,
            **data
        }

        json_str = json.dumps(log_entry, ensure_ascii=False)
        log_method = getattr(self.logger, level.lower())
        log_method(json_str)


# 便捷函数
def log_memory_add(user_id: str, memory_id: str, **kwargs):
    """便捷函数：记录添加记忆"""
    get_memory_logger().log_memory_add(user_id, memory_id, **kwargs)


def log_memory_forget(user_id: str, memory_id: str, **kwargs):
    """便捷函数：记录遗忘操作"""
    get_memory_logger().log_memory_forget(user_id, memory_id, **kwargs)


def log_redis_op(operation: str, key_pattern: str, **kwargs):
    """便捷函数：记录Redis操作"""
    get_memory_logger().log_redis_operation(operation, key_pattern, **kwargs)


__all__ = [
    "MemoryLogger",
    "StructuredLogger",
    "LogLevel",
    "OperationType",
    "get_memory_logger",
    "set_memory_logger",
    "log_memory_operation",
    "log_memory_add",
    "log_memory_forget",
    "log_redis_op"
]
