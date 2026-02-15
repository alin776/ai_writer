"""
记忆系统监控和指标收集模块 (P1-5修复)

提供完整的监控能力:
1. 容量指标 - 短期/中期/长期记忆使用率
2. 性能指标 - 检索/写入延迟、遗忘操作耗时
3. 质量指标 - 记忆召回率、重要度分布
4. 异常指标 - Redis故障、降级触发、数据丢失
5. 健康检查 - 系统状态评估和告警
"""

import time
import logging
from datetime import datetime, timezone
from typing import Dict, Any, List, Optional, Callable
from dataclasses import dataclass, field
from enum import Enum
from collections import defaultdict, deque
import threading
import statistics

logger = logging.getLogger(__name__)


class HealthStatus(Enum):
    """健康状态"""
    HEALTHY = "healthy"          # 健康
    DEGRADED = "degraded"        # 降级运行
    CRITICAL = "critical"        # 严重异常
    UNKNOWN = "unknown"          # 未知状态


class MetricType(Enum):
    """指标类型"""
    COUNTER = "counter"          # 计数器（单调递增）
    GAUGE = "gauge"              # 仪表盘（当前值）
    HISTOGRAM = "histogram"      # 直方图（分布统计）
    SUMMARY = "summary"          # 摘要（百分位数）


@dataclass
class Alert:
    """告警信息"""
    level: str                   # "info", "warning", "error", "critical"
    title: str
    message: str
    metric_name: str
    current_value: Any
    threshold: Any
    timestamp: datetime = field(default_factory=lambda: datetime.now(timezone.utc))


@dataclass
class HealthReport:
    """健康检查报告"""
    status: HealthStatus
    timestamp: datetime
    capacity_metrics: Dict[str, Any]
    performance_metrics: Dict[str, Any]
    quality_metrics: Dict[str, Any]
    error_metrics: Dict[str, Any]
    alerts: List[Alert]
    summary: str


class Counter:
    """计数器指标"""

    def __init__(self, name: str, description: str = ""):
        self.name = name
        self.description = description
        self._value = 0
        self._lock = threading.Lock()

    def inc(self, amount: int = 1):
        """增加计数"""
        with self._lock:
            self._value += amount

    def get(self) -> int:
        """获取当前值"""
        with self._lock:
            return self._value

    def reset(self):
        """重置计数"""
        with self._lock:
            self._value = 0


class Gauge:
    """仪表盘指标（当前值）"""

    def __init__(self, name: str, description: str = ""):
        self.name = name
        self.description = description
        self._value = 0.0
        self._lock = threading.Lock()

    def set(self, value: float):
        """设置值"""
        with self._lock:
            self._value = value

    def inc(self, amount: float = 1.0):
        """增加值"""
        with self._lock:
            self._value += amount

    def dec(self, amount: float = 1.0):
        """减少值"""
        with self._lock:
            self._value -= amount

    def get(self) -> float:
        """获取当前值"""
        with self._lock:
            return self._value


class Histogram:
    """直方图指标（分布统计）"""

    def __init__(self, name: str, description: str = "", max_size: int = 1000):
        self.name = name
        self.description = description
        self._values = deque(maxlen=max_size)
        self._lock = threading.Lock()

    def observe(self, value: float):
        """记录观测值"""
        with self._lock:
            self._values.append(value)

    def get_percentile(self, percentile: float) -> Optional[float]:
        """获取百分位数 (0.0 - 1.0)"""
        with self._lock:
            if not self._values:
                return None
            sorted_values = sorted(self._values)
            index = int(len(sorted_values) * percentile)
            index = min(index, len(sorted_values) - 1)
            return sorted_values[index]

    def get_stats(self) -> Dict[str, Any]:
        """获取统计信息"""
        with self._lock:
            if not self._values:
                return {
                    "count": 0,
                    "min": None,
                    "max": None,
                    "mean": None,
                    "p50": None,
                    "p95": None,
                    "p99": None
                }

            values_list = list(self._values)
            return {
                "count": len(values_list),
                "min": min(values_list),
                "max": max(values_list),
                "mean": statistics.mean(values_list),
                "p50": self.get_percentile(0.5),
                "p95": self.get_percentile(0.95),
                "p99": self.get_percentile(0.99)
            }

    def reset(self):
        """重置"""
        with self._lock:
            self._values.clear()


class MemoryMetrics:
    """
    记忆系统监控指标收集器 (P1-5修复)

    提供完整的监控能力，包括容量、性能、质量和异常指标。
    """

    _instance: Optional['MemoryMetrics'] = None
    _lock = threading.Lock()

    def __new__(cls, *args, **kwargs):
        """单例模式"""
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:
                    cls._instance = super().__new__(cls)
                    cls._instance._initialized = False
        return cls._instance

    def __init__(self):
        if self._initialized:
            return

        # === 容量指标 ===
        self.short_term_usage = Gauge("short_term_memory_usage", "短期记忆使用量")
        self.medium_term_usage = Gauge("medium_term_memory_usage", "中期记忆使用量")
        self.long_term_usage = Gauge("long_term_memory_usage", "长期记忆使用量")
        self.redis_memory_usage = Gauge("redis_memory_usage_bytes", "Redis内存使用（字节）")

        # === 性能指标 ===
        self.retrieval_latency = Histogram("memory_retrieval_latency_ms", "记忆检索延迟（毫秒）")
        self.write_latency = Histogram("memory_write_latency_ms", "记忆写入延迟（毫秒）")
        self.forget_latency = Histogram("memory_forget_latency_ms", "遗忘操作延迟（毫秒）")
        self.context_build_latency = Histogram("context_build_latency_ms", "上下文构建延迟（毫秒）")

        # === 质量指标 ===
        self.memory_recall_rate = Gauge("memory_recall_rate", "记忆召回率")
        self.importance_distribution = Histogram("memory_importance_distribution", "记忆重要度分布")
        self.summary_quality_score = Gauge("summary_quality_score", "摘要质量评分")

        # === 异常指标 ===
        self.redis_errors = Counter("redis_connection_errors_total", "Redis连接错误总数")
        self.fallback_triggered = Counter("fallback_triggered_total", "降级触发总数")
        self.data_loss_events = Counter("data_loss_events_total", "数据丢失事件总数")
        self.truncation_events = Counter("context_truncation_events_total", "上下文截断事件总数")

        # === 操作计数 ===
        self.total_retrievals = Counter("memory_retrievals_total", "总检索次数")
        self.total_writes = Counter("memory_writes_total", "总写入次数")
        self.total_forgets = Counter("memory_forgets_total", "总遗忘次数")

        # === 告警配置 ===
        self._alert_callbacks: List[Callable[[Alert], None]] = []
        self._alert_thresholds = {
            "short_term_usage_rate": 0.9,      # 短期记忆使用率 > 90%
            "retrieval_latency_p95": 500,      # P95延迟 > 500ms
            "redis_error_rate": 0.1,           # 错误率 > 10%
            "fallback_count": 5,               # 降级次数 > 5次/小时
        }

        self._initialized = True
        logger.info("[MemoryMetrics] 监控系统已初始化")

    # === 性能测量装饰器 ===

    def measure_latency(self, metric_name: str):
        """测量延迟的装饰器"""
        def decorator(func):
            def wrapper(*args, **kwargs):
                start_time = time.time()
                try:
                    result = func(*args, **kwargs)
                    return result
                finally:
                    elapsed_ms = (time.time() - start_time) * 1000
                    metric = getattr(self, metric_name, None)
                    if isinstance(metric, Histogram):
                        metric.observe(elapsed_ms)
            return wrapper
        return decorator

    # === 容量监控 ===

    def update_capacity_metrics(
        self,
        short_term_count: int,
        short_term_limit: int,
        medium_term_count: int,
        medium_term_limit: int,
        redis_memory_bytes: Optional[int] = None
    ):
        """更新容量指标"""
        self.short_term_usage.set(short_term_count / short_term_limit if short_term_limit > 0 else 0)
        self.medium_term_usage.set(medium_term_count / medium_term_limit if medium_term_limit > 0 else 0)

        if redis_memory_bytes is not None:
            self.redis_memory_usage.set(redis_memory_bytes)

        # 检查容量告警
        if self.short_term_usage.get() > self._alert_thresholds["short_term_usage_rate"]:
            self._trigger_alert(
                Alert(
                    level="warning",
                    title="短期记忆容量告警",
                    message=f"短期记忆使用率达到 {self.short_term_usage.get():.1%}",
                    metric_name="short_term_usage",
                    current_value=self.short_term_usage.get(),
                    threshold=self._alert_thresholds["short_term_usage_rate"]
                )
            )

    # === 性能监控 ===

    def record_retrieval(self, latency_ms: float, success: bool = True):
        """记录检索操作"""
        self.total_retrievals.inc()
        self.retrieval_latency.observe(latency_ms)

        # 检查延迟告警
        stats = self.retrieval_latency.get_stats()
        if stats["p95"] and stats["p95"] > self._alert_thresholds["retrieval_latency_p95"]:
            self._trigger_alert(
                Alert(
                    level="warning",
                    title="检索延迟告警",
                    message=f"P95检索延迟达到 {stats['p95']:.1f}ms",
                    metric_name="retrieval_latency_p95",
                    current_value=stats["p95"],
                    threshold=self._alert_thresholds["retrieval_latency_p95"]
                )
            )

    def record_write(self, latency_ms: float):
        """记录写入操作"""
        self.total_writes.inc()
        self.write_latency.observe(latency_ms)

    def record_forget(self, latency_ms: float):
        """记录遗忘操作"""
        self.total_forgets.inc()
        self.forget_latency.observe(latency_ms)

    # === 质量监控 ===

    def record_importance(self, importance: float):
        """记录记忆重要度"""
        self.importance_distribution.observe(importance)

    def update_recall_rate(self, rate: float):
        """更新召回率"""
        self.memory_recall_rate.set(rate)

    # === 异常监控 ===

    def record_redis_error(self):
        """记录Redis错误"""
        self.redis_errors.inc()

        # 检查错误率告警
        total_ops = (self.total_retrievals.get() + self.total_writes.get() +
                     self.total_forgets.get())
        if total_ops > 0:
            error_rate = self.redis_errors.get() / total_ops
            if error_rate > self._alert_thresholds["redis_error_rate"]:
                self._trigger_alert(
                    Alert(
                        level="error",
                        title="Redis错误率告警",
                        message=f"Redis错误率达到 {error_rate:.1%}",
                        metric_name="redis_error_rate",
                        current_value=error_rate,
                        threshold=self._alert_thresholds["redis_error_rate"]
                    )
                )

    def record_fallback(self):
        """记录降级触发"""
        self.fallback_triggered.inc()

        if self.fallback_triggered.get() > self._alert_thresholds["fallback_count"]:
            self._trigger_alert(
                Alert(
                    level="warning",
                    title="降级触发告警",
                    message=f"降级已触发 {self.fallback_triggered.get()} 次",
                    metric_name="fallback_triggered",
                    current_value=self.fallback_triggered.get(),
                    threshold=self._alert_thresholds["fallback_count"]
                )
            )

    def record_data_loss(self):
        """记录数据丢失事件"""
        self.data_loss_events.inc()

        self._trigger_alert(
            Alert(
                level="critical",
                title="数据丢失告警",
                message=f"检测到数据丢失事件（总计 {self.data_loss_events.get()} 次）",
                metric_name="data_loss_events",
                current_value=self.data_loss_events.get(),
                threshold=0
            )
        )

    def record_truncation(self):
        """记录截断事件"""
        self.truncation_events.inc()

    # === 健康检查 ===

    def health_check(self) -> HealthReport:
        """执行健康检查并生成报告"""
        alerts = []

        # 收集所有指标
        capacity_metrics = {
            "short_term_usage": self.short_term_usage.get(),
            "medium_term_usage": self.medium_term_usage.get(),
            "long_term_usage": self.long_term_usage.get(),
            "redis_memory_bytes": self.redis_memory_usage.get()
        }

        performance_metrics = {
            "retrieval_latency": self.retrieval_latency.get_stats(),
            "write_latency": self.write_latency.get_stats(),
            "forget_latency": self.forget_latency.get_stats(),
            "context_build_latency": self.context_build_latency.get_stats()
        }

        quality_metrics = {
            "recall_rate": self.memory_recall_rate.get(),
            "importance_distribution": self.importance_distribution.get_stats(),
            "summary_quality_score": self.summary_quality_score.get()
        }

        error_metrics = {
            "redis_errors": self.redis_errors.get(),
            "fallback_triggered": self.fallback_triggered.get(),
            "data_loss_events": self.data_loss_events.get(),
            "truncation_events": self.truncation_events.get()
        }

        # 评估健康状态
        status = HealthStatus.HEALTHY

        # Critical 条件
        if error_metrics["data_loss_events"] > 0:
            status = HealthStatus.CRITICAL
            alerts.append(Alert(
                level="critical",
                title="系统严重异常",
                message="检测到数据丢失事件",
                metric_name="data_loss_events",
                current_value=error_metrics["data_loss_events"],
                threshold=0
            ))

        # Degraded 条件
        elif (capacity_metrics["short_term_usage"] > 0.9 or
              error_metrics["fallback_triggered"] > 5 or
              error_metrics["redis_errors"] > 10):
            status = HealthStatus.DEGRADED
            alerts.append(Alert(
                level="warning",
                title="系统运行降级",
                message="检测到容量告警或降级运行",
                metric_name="system_status",
                current_value=status.value,
                threshold="healthy"
            ))

        # 生成摘要
        summary = self._generate_summary(status, capacity_metrics, performance_metrics, error_metrics)

        return HealthReport(
            status=status,
            timestamp=datetime.now(timezone.utc),
            capacity_metrics=capacity_metrics,
            performance_metrics=performance_metrics,
            quality_metrics=quality_metrics,
            error_metrics=error_metrics,
            alerts=alerts,
            summary=summary
        )

    def _generate_summary(
        self,
        status: HealthStatus,
        capacity: Dict,
        performance: Dict,
        errors: Dict
    ) -> str:
        """生成健康检查摘要"""
        parts = [f"状态: {status.value}"]

        # 容量摘要
        parts.append(
            f"容量: 短期{capacity['short_term_usage']:.1%} "
            f"中期{capacity['medium_term_usage']:.1%}"
        )

        # 性能摘要
        retrieval_p95 = performance['retrieval_latency'].get('p95')
        if retrieval_p95:
            parts.append(f"检索P95: {retrieval_p95:.1f}ms")

        # 异常摘要
        if errors['redis_errors'] > 0 or errors['fallback_triggered'] > 0:
            parts.append(
                f"异常: Redis错误{errors['redis_errors']}次 "
                f"降级{errors['fallback_triggered']}次"
            )

        return " | ".join(parts)

    # === 告警管理 ===

    def register_alert_callback(self, callback: Callable[[Alert], None]):
        """注册告警回调函数"""
        self._alert_callbacks.append(callback)

    def _trigger_alert(self, alert: Alert):
        """触发告警"""
        logger.warning(
            f"[MemoryMetrics] 告警: [{alert.level}] {alert.title} - {alert.message}"
        )

        for callback in self._alert_callbacks:
            try:
                callback(alert)
            except Exception as e:
                logger.error(f"[MemoryMetrics] 告警回调失败: {e}")

    # === 导出指标 ===

    def export_metrics(self) -> Dict[str, Any]:
        """导出所有指标（用于Prometheus等监控系统）"""
        return {
            "capacity": {
                "short_term_usage": self.short_term_usage.get(),
                "medium_term_usage": self.medium_term_usage.get(),
                "long_term_usage": self.long_term_usage.get(),
                "redis_memory_bytes": self.redis_memory_usage.get()
            },
            "performance": {
                "retrieval_latency": self.retrieval_latency.get_stats(),
                "write_latency": self.write_latency.get_stats(),
                "forget_latency": self.forget_latency.get_stats(),
                "context_build_latency": self.context_build_latency.get_stats()
            },
            "quality": {
                "recall_rate": self.memory_recall_rate.get(),
                "importance_distribution": self.importance_distribution.get_stats(),
                "summary_quality_score": self.summary_quality_score.get()
            },
            "errors": {
                "redis_errors": self.redis_errors.get(),
                "fallback_triggered": self.fallback_triggered.get(),
                "data_loss_events": self.data_loss_events.get(),
                "truncation_events": self.truncation_events.get()
            },
            "operations": {
                "total_retrievals": self.total_retrievals.get(),
                "total_writes": self.total_writes.get(),
                "total_forgets": self.total_forgets.get()
            }
        }


# 全局指标实例
_metrics: Optional[MemoryMetrics] = None


def get_metrics() -> MemoryMetrics:
    """获取全局指标实例"""
    global _metrics
    if _metrics is None:
        _metrics = MemoryMetrics()
    return _metrics
