"""
AI Writer 监控和统计系统

提供全面的系统监控、性能统计、健康检查、异常检测和告警功能。
"""

import asyncio
import time
import json
import threading
from typing import Dict, Any, List, Optional, Callable, Union
from datetime import datetime, timedelta
from dataclasses import dataclass, field, asdict
from collections import defaultdict, deque
from enum import Enum
import statistics
import psutil
import os

from .logger import get_logger
from app.utils.datetime_utils import get_utc_now

logger = get_logger("monitoring")


class MetricType(Enum):
    """指标类型"""
    COUNTER = "counter"      # 计数器
    GAUGE = "gauge"          # 仪表盘
    HISTOGRAM = "histogram"  # 直方图
    TIMER = "timer"          # 计时器


class AlertLevel(Enum):
    """告警级别"""
    INFO = "info"
    WARNING = "warning"
    ERROR = "error"
    CRITICAL = "critical"


class HealthStatus(Enum):
    """健康状态"""
    HEALTHY = "healthy"
    WARNING = "warning"
    UNHEALTHY = "unhealthy"
    UNKNOWN = "unknown"


@dataclass
class Metric:
    """监控指标"""
    name: str
    value: Union[int, float]
    metric_type: MetricType
    timestamp: datetime = field(default_factory=datetime.now)
    labels: Dict[str, str] = field(default_factory=dict)
    unit: str = ""
    description: str = ""

    def to_dict(self) -> Dict[str, Any]:
        """转换为字典"""
        return {
            "name": self.name,
            "value": self.value,
            "type": self.metric_type.value,
            "timestamp": self.timestamp.isoformat(),
            "labels": self.labels,
            "unit": self.unit,
            "description": self.description
        }


@dataclass
class Alert:
    """告警信息"""
    id: str
    level: AlertLevel
    title: str
    message: str
    timestamp: datetime = field(default_factory=datetime.now)
    resolved: bool = False
    resolved_at: Optional[datetime] = None
    metadata: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        """转换为字典"""
        return {
            "id": self.id,
            "level": self.level.value,
            "title": self.title,
            "message": self.message,
            "timestamp": self.timestamp.isoformat(),
            "resolved": self.resolved,
            "resolved_at": self.resolved_at.isoformat() if self.resolved_at else None,
            "metadata": self.metadata
        }


@dataclass
class HealthCheck:
    """健康检查结果"""
    name: str
    status: HealthStatus
    message: str = ""
    timestamp: datetime = field(default_factory=datetime.now)
    response_time: float = 0.0
    details: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        """转换为字典"""
        return {
            "name": self.name,
            "status": self.status.value,
            "message": self.message,
            "timestamp": self.timestamp.isoformat(),
            "response_time": self.response_time,
            "details": self.details
        }


class MetricsCollector:
    """指标收集器"""

    def __init__(self, max_history: int = 1000):
        """
        初始化指标收集器

        Args:
            max_history: 最大历史记录数量
        """
        self.max_history = max_history
        self._metrics: Dict[str, deque] = defaultdict(lambda: deque(maxlen=max_history))
        self._counters: Dict[str, int] = defaultdict(int)
        self._gauges: Dict[str, float] = defaultdict(float)
        self._histograms: Dict[str, List[float]] = defaultdict(list)
        self._timers: Dict[str, List[float]] = defaultdict(list)
        self._lock = threading.Lock()

    def increment_counter(self, name: str, value: int = 1, labels: Dict[str, str] = None) -> None:
        """增加计数器"""
        with self._lock:
            key = self._make_key(name, labels)
            self._counters[key] += value

            metric = Metric(
                name=name,
                value=self._counters[key],
                metric_type=MetricType.COUNTER,
                labels=labels or {}
            )
            self._metrics[key].append(metric)

    def set_gauge(self, name: str, value: float, labels: Dict[str, str] = None) -> None:
        """设置仪表盘值"""
        with self._lock:
            key = self._make_key(name, labels)
            self._gauges[key] = value

            metric = Metric(
                name=name,
                value=value,
                metric_type=MetricType.GAUGE,
                labels=labels or {}
            )
            self._metrics[key].append(metric)

    def record_histogram(self, name: str, value: float, labels: Dict[str, str] = None) -> None:
        """记录直方图数据"""
        with self._lock:
            key = self._make_key(name, labels)
            self._histograms[key].append(value)

            metric = Metric(
                name=name,
                value=value,
                metric_type=MetricType.HISTOGRAM,
                labels=labels or {}
            )
            self._metrics[key].append(metric)

    def record_timer(self, name: str, duration: float, labels: Dict[str, str] = None) -> None:
        """记录计时器数据"""
        with self._lock:
            key = self._make_key(name, labels)
            self._timers[key].append(duration)

            metric = Metric(
                name=name,
                value=duration,
                metric_type=MetricType.TIMER,
                labels=labels or {},
                unit="seconds"
            )
            self._metrics[key].append(metric)

    def _make_key(self, name: str, labels: Dict[str, str] = None) -> str:
        """生成指标键"""
        if not labels:
            return name

        label_str = ",".join(f"{k}={v}" for k, v in sorted(labels.items()))
        return f"{name}[{label_str}]"

    def get_metric(self, name: str, labels: Dict[str, str] = None) -> Optional[Metric]:
        """获取最新的指标值"""
        with self._lock:
            key = self._make_key(name, labels)
            if key in self._metrics and self._metrics[key]:
                return self._metrics[key][-1]
            return None

    def get_metrics_history(self, name: str, labels: Dict[str, str] = None,
                           since: Optional[datetime] = None) -> List[Metric]:
        """获取指标历史记录"""
        with self._lock:
            key = self._make_key(name, labels)
            if key not in self._metrics:
                return []

            history = list(self._metrics[key])
            if since:
                history = [m for m in history if m.timestamp >= since]

            return history

    def get_statistics(self, name: str, labels: Dict[str, str] = None) -> Dict[str, float]:
        """获取指标统计信息"""
        with self._lock:
            key = self._make_key(name, labels)

            if key in self._histograms and self._histograms[key]:
                values = self._histograms[key]
                return {
                    "count": len(values),
                    "min": min(values),
                    "max": max(values),
                    "mean": statistics.mean(values),
                    "median": statistics.median(values),
                    "sum": sum(values)
                }
            elif key in self._timers and self._timers[key]:
                values = self._timers[key]
                return {
                    "count": len(values),
                    "min": min(values),
                    "max": max(values),
                    "mean": statistics.mean(values),
                    "median": statistics.median(values),
                    "sum": sum(values)
                }
            elif key in self._counters:
                return {
                    "value": self._counters[key]
                }
            elif key in self._gauges:
                return {
                    "value": self._gauges[key]
                }

            return {}

    def get_all_metrics(self) -> Dict[str, List[Dict[str, Any]]]:
        """获取所有指标数据"""
        result = {}
        with self._lock:
            for key, metrics in self._metrics.items():
                result[key] = [metric.to_dict() for metric in metrics]
        return result

    def clear_metrics(self, name: Optional[str] = None) -> None:
        """清空指标数据"""
        with self._lock:
            if name:
                keys_to_clear = [k for k in self._metrics.keys() if k.startswith(name)]
                for key in keys_to_clear:
                    self._metrics[key].clear()
                    self._counters.pop(key, None)
                    self._gauges.pop(key, None)
                    self._histograms.pop(key, None)
                    self._timers.pop(key, None)
            else:
                self._metrics.clear()
                self._counters.clear()
                self._gauges.clear()
                self._histograms.clear()
                self._timers.clear()


class HealthChecker:
    """健康检查器"""

    def __init__(self):
        self._checks: Dict[str, Callable] = {}
        self._last_results: Dict[str, HealthCheck] = {}

    def register_check(self, name: str, check_func: Callable[[], HealthCheck]) -> None:
        """
        注册健康检查

        Args:
            name: 检查名称
            check_func: 检查函数，返回 HealthCheck 对象
        """
        self._checks[name] = check_func
        logger.info(f"Registered health check: {name}")

    def unregister_check(self, name: str) -> None:
        """注销健康检查"""
        self._checks.pop(name, None)
        self._last_results.pop(name, None)
        logger.info(f"Unregistered health check: {name}")

    async def run_check(self, name: str) -> HealthCheck:
        """运行单个健康检查"""
        if name not in self._checks:
            return HealthCheck(
                name=name,
                status=HealthStatus.UNKNOWN,
                message="Check not found"
            )

        start_time = time.time()
        try:
            result = self._checks[name]()
            if isinstance(result, HealthCheck):
                result.response_time = time.time() - start_time
                self._last_results[name] = result
                return result
            else:
                # 如果返回的不是 HealthCheck 对象，创建一个默认的
                health_check = HealthCheck(
                    name=name,
                    status=HealthStatus.HEALTHY if result else HealthStatus.UNHEALTHY,
                    message="Check completed" if result else "Check failed",
                    response_time=time.time() - start_time
                )
                self._last_results[name] = health_check
                return health_check

        except Exception as e:
            health_check = HealthCheck(
                name=name,
                status=HealthStatus.UNHEALTHY,
                message=f"Check failed: {str(e)}",
                response_time=time.time() - start_time,
                details={"error": str(e), "error_type": type(e).__name__}
            )
            self._last_results[name] = health_check
            logger.error(f"Health check {name} failed: {e}")
            return health_check

    async def run_all_checks(self) -> Dict[str, HealthCheck]:
        """运行所有健康检查"""
        results = {}
        tasks = []

        for name in self._checks.keys():
            task = asyncio.create_task(self.run_check(name))
            tasks.append((name, task))

        for name, task in tasks:
            try:
                results[name] = await task
            except Exception as e:
                results[name] = HealthCheck(
                    name=name,
                    status=HealthStatus.UNHEALTHY,
                    message=f"Check execution failed: {str(e)}",
                    details={"error": str(e)}
                )

        return results

    def get_last_results(self) -> Dict[str, HealthCheck]:
        """获取最后检查结果"""
        return self._last_results.copy()

    def get_overall_status(self) -> HealthStatus:
        """获取总体健康状态"""
        if not self._last_results:
            return HealthStatus.UNKNOWN

        statuses = [check.status for check in self._last_results.values()]

        if any(status == HealthStatus.UNHEALTHY for status in statuses):
            return HealthStatus.UNHEALTHY
        elif any(status == HealthStatus.WARNING for status in statuses):
            return HealthStatus.WARNING
        elif all(status == HealthStatus.HEALTHY for status in statuses):
            return HealthStatus.HEALTHY
        else:
            return HealthStatus.UNKNOWN


class AlertManager:
    """告警管理器"""

    def __init__(self, max_alerts: int = 1000):
        """
        初始化告警管理器

        Args:
            max_alerts: 最大告警数量
        """
        self.max_alerts = max_alerts
        self._alerts: deque = deque(maxlen=max_alerts)
        self._alert_rules: Dict[str, Callable] = {}
        self._alert_handlers: List[Callable[[Alert], None]] = []
        self._lock = threading.Lock()

    def add_alert_rule(self, name: str, rule_func: Callable[[], Optional[Alert]]) -> None:
        """
        添加告警规则

        Args:
            name: 规则名称
            rule_func: 规则函数，返回 Alert 对象或 None
        """
        self._alert_rules[name] = rule_func
        logger.info(f"Added alert rule: {name}")

    def remove_alert_rule(self, name: str) -> None:
        """移除告警规则"""
        self._alert_rules.pop(name, None)
        logger.info(f"Removed alert rule: {name}")

    def add_alert_handler(self, handler: Callable[[Alert], None]) -> None:
        """
        添加告警处理器

        Args:
            handler: 告警处理函数
        """
        self._alert_handlers.append(handler)
        logger.info(f"Added alert handler: {handler.__name__}")

    async def check_alerts(self) -> List[Alert]:
        """检查告警规则"""
        new_alerts = []

        for name, rule_func in self._alert_rules.items():
            try:
                alert = rule_func()
                if alert:
                    if not self._is_duplicate_alert(alert):
                        with self._lock:
                            self._alerts.append(alert)
                        new_alerts.append(alert)

                        # 调用告警处理器
                        for handler in self._alert_handlers:
                            try:
                                handler(alert)
                            except Exception as e:
                                logger.error(f"Alert handler failed: {e}")

            except Exception as e:
                logger.error(f"Alert rule {name} failed: {e}")

        return new_alerts

    def _is_duplicate_alert(self, alert: Alert) -> bool:
        """检查是否为重复告警"""
        for existing_alert in reversed(self._alerts):
            if (existing_alert.title == alert.title and
                existing_alert.message == alert.message and
                existing_alert.level == alert.level and
                not existing_alert.resolved and
                (get_utc_now() - existing_alert.timestamp).total_seconds() < 300):  # 5分钟内
                return True
        return False

    def create_alert(
        self,
        level: AlertLevel,
        title: str,
        message: str,
        metadata: Dict[str, Any] = None
    ) -> Alert:
        """创建告警"""
        alert = Alert(
            id=f"{int(time.time())}_{hash(title + message)}",
            level=level,
            title=title,
            message=message,
            metadata=metadata or {}
        )

        with self._lock:
            self._alerts.append(alert)

        # 调用告警处理器
        for handler in self._alert_handlers:
            try:
                handler(alert)
            except Exception as e:
                logger.error(f"Alert handler failed: {e}")

        return alert

    def resolve_alert(self, alert_id: str) -> bool:
        """解决告警"""
        with self._lock:
            for alert in reversed(self._alerts):
                if alert.id == alert_id and not alert.resolved:
                    alert.resolved = True
                    alert.resolved_at = get_utc_now()
                    logger.info(f"Alert resolved: {alert.title}")
                    return True
        return False

    def get_active_alerts(self) -> List[Alert]:
        """获取活跃告警"""
        with self._lock:
            return [alert for alert in self._alerts if not alert.resolved]

    def get_all_alerts(self, limit: int = 100) -> List[Alert]:
        """获取所有告警"""
        with self._lock:
            return list(self._alerts)[-limit:]

    def get_alerts_by_level(self, level: AlertLevel) -> List[Alert]:
        """按级别获取告警"""
        with self._lock:
            return [alert for alert in self._alerts if alert.level == level]


class SystemMonitor:
    """系统监控器"""

    def __init__(self):
        self.metrics_collector = MetricsCollector()
        self.health_checker = HealthChecker()
        self.alert_manager = AlertManager()
        self._running = False
        self._monitor_task: Optional[asyncio.Task] = None

        # 注册默认的健康检查
        self._register_default_health_checks()

        # 注册默认的告警规则
        self._register_default_alert_rules()

    def _register_default_health_checks(self) -> None:
        """注册默认健康检查"""
        self.health_checker.register_check("cpu_usage", self._check_cpu_usage)
        self.health_checker.register_check("memory_usage", self._check_memory_usage)
        self.health_checker.register_check("disk_usage", self._check_disk_usage)
        self.health_checker.register_check("process_status", self._check_process_status)

    def _register_default_alert_rules(self) -> None:
        """注册默认告警规则"""
        self.alert_manager.add_alert_rule("high_cpu_usage", self._alert_high_cpu)
        self.alert_manager.add_alert_rule("high_memory_usage", self._alert_high_memory)
        self.alert_manager.add_alert_rule("low_disk_space", self._alert_low_disk)

    def _check_cpu_usage(self) -> HealthCheck:
        """检查CPU使用率"""
        try:
            cpu_percent = psutil.cpu_percent(interval=1)
            self.metrics_collector.set_gauge("system_cpu_usage", cpu_percent)

            if cpu_percent > 90:
                return HealthCheck(
                    name="cpu_usage",
                    status=HealthStatus.WARNING,
                    message=f"High CPU usage: {cpu_percent:.1f}%",
                    details={"cpu_percent": cpu_percent}
                )
            else:
                return HealthCheck(
                    name="cpu_usage",
                    status=HealthStatus.HEALTHY,
                    message=f"CPU usage: {cpu_percent:.1f}%",
                    details={"cpu_percent": cpu_percent}
                )
        except Exception as e:
            return HealthCheck(
                name="cpu_usage",
                status=HealthStatus.UNHEALTHY,
                message=f"Failed to check CPU usage: {str(e)}",
                details={"error": str(e)}
            )

    def _check_memory_usage(self) -> HealthCheck:
        """检查内存使用率"""
        try:
            memory = psutil.virtual_memory()
            self.metrics_collector.set_gauge("system_memory_usage", memory.percent)
            self.metrics_collector.set_gauge("system_memory_available_gb", memory.available / (1024**3))

            if memory.percent > 90:
                return HealthCheck(
                    name="memory_usage",
                    status=HealthStatus.WARNING,
                    message=f"High memory usage: {memory.percent:.1f}%",
                    details={"memory_percent": memory.percent, "available_gb": memory.available / (1024**3)}
                )
            else:
                return HealthCheck(
                    name="memory_usage",
                    status=HealthStatus.HEALTHY,
                    message=f"Memory usage: {memory.percent:.1f}%",
                    details={"memory_percent": memory.percent, "available_gb": memory.available / (1024**3)}
                )
        except Exception as e:
            return HealthCheck(
                name="memory_usage",
                status=HealthStatus.UNHEALTHY,
                message=f"Failed to check memory usage: {str(e)}",
                details={"error": str(e)}
            )

    def _check_disk_usage(self) -> HealthCheck:
        """检查磁盘使用率"""
        try:
            disk = psutil.disk_usage('/')
            disk_percent = (disk.used / disk.total) * 100
            self.metrics_collector.set_gauge("system_disk_usage", disk_percent)
            self.metrics_collector.set_gauge("system_disk_free_gb", disk.free / (1024**3))

            if disk_percent > 90:
                return HealthCheck(
                    name="disk_usage",
                    status=HealthStatus.WARNING,
                    message=f"Low disk space: {disk_percent:.1f}% used",
                    details={"disk_percent": disk_percent, "free_gb": disk.free / (1024**3)}
                )
            else:
                return HealthCheck(
                    name="disk_usage",
                    status=HealthStatus.HEALTHY,
                    message=f"Disk usage: {disk_percent:.1f}%",
                    details={"disk_percent": disk_percent, "free_gb": disk.free / (1024**3)}
                )
        except Exception as e:
            return HealthCheck(
                name="disk_usage",
                status=HealthStatus.UNHEALTHY,
                message=f"Failed to check disk usage: {str(e)}",
                details={"error": str(e)}
            )

    def _check_process_status(self) -> HealthCheck:
        """检查进程状态"""
        try:
            process = psutil.Process()
            self.metrics_collector.set_gauge("process_cpu_usage", process.cpu_percent())
            self.metrics_collector.set_gauge("process_memory_mb", process.memory_info().rss / (1024**2))

            return HealthCheck(
                name="process_status",
                status=HealthStatus.HEALTHY,
                message="Process running normally",
                details={
                    "pid": process.pid,
                    "cpu_percent": process.cpu_percent(),
                    "memory_mb": process.memory_info().rss / (1024**2),
                    "status": process.status()
                }
            )
        except Exception as e:
            return HealthCheck(
                name="process_status",
                status=HealthStatus.UNHEALTHY,
                message=f"Failed to check process: {str(e)}",
                details={"error": str(e)}
            )

    def _alert_high_cpu(self) -> Optional[Alert]:
        """高CPU使用率告警"""
        metric = self.metrics_collector.get_metric("system_cpu_usage")
        if metric and metric.value > 90:
            return self.alert_manager.create_alert(
                level=AlertLevel.WARNING,
                title="High CPU Usage",
                message=f"CPU usage is {metric.value:.1f}%",
                metadata={"cpu_percent": metric.value}
            )
        return None

    def _alert_high_memory(self) -> Optional[Alert]:
        """高内存使用率告警"""
        metric = self.metrics_collector.get_metric("system_memory_usage")
        if metric and metric.value > 90:
            return self.alert_manager.create_alert(
                level=AlertLevel.WARNING,
                title="High Memory Usage",
                message=f"Memory usage is {metric.value:.1f}%",
                metadata={"memory_percent": metric.value}
            )
        return None

    def _alert_low_disk(self) -> Optional[Alert]:
        """磁盘空间不足告警"""
        metric = self.metrics_collector.get_metric("system_disk_usage")
        if metric and metric.value > 90:
            return self.alert_manager.create_alert(
                level=AlertLevel.ERROR,
                title="Low Disk Space",
                message=f"Disk usage is {metric.value:.1f}%",
                metadata={"disk_percent": metric.value}
            )
        return None

    async def start_monitoring(self, interval: float = 30.0) -> None:
        """
        开始监控

        Args:
            interval: 监控间隔（秒）
        """
        if self._running:
            return

        self._running = True
        self._monitor_task = asyncio.create_task(self._monitor_loop(interval))
        logger.info(f"System monitoring started with {interval}s interval")

    async def stop_monitoring(self) -> None:
        """停止监控"""
        if not self._running:
            return

        self._running = False
        if self._monitor_task:
            self._monitor_task.cancel()
            try:
                await self._monitor_task
            except asyncio.CancelledError:
                pass

        logger.info("System monitoring stopped")

    async def _monitor_loop(self, interval: float) -> None:
        """监控循环"""
        logger.info("Monitor loop started")

        while self._running:
            try:
                # 运行健康检查
                health_results = await self.health_checker.run_all_checks()

                # 检查告警
                alerts = await self.alert_manager.check_alerts()

                # 记录监控指标
                self.metrics_collector.increment_counter("monitoring_cycles")
                self.metrics_collector.set_gauge("active_health_checks", len(health_results))
                self.metrics_collector.set_gauge("active_alerts", len(self.alert_manager.get_active_alerts()))

                await asyncio.sleep(interval)

            except asyncio.CancelledError:
                break
            except Exception as e:
                logger.error(f"Monitor loop error: {e}")
                await asyncio.sleep(interval)

        logger.info("Monitor loop stopped")

    def get_monitoring_summary(self) -> Dict[str, Any]:
        """获取监控摘要"""
        health_results = self.health_checker.get_last_results()
        active_alerts = self.alert_manager.get_active_alerts()

        return {
            "overall_health": self.health_checker.get_overall_status().value,
            "health_checks": {name: check.to_dict() for name, check in health_results.items()},
            "active_health_checks": len(health_results),
            "active_alerts_count": len(active_alerts),
            "active_alerts": [alert.to_dict() for alert in active_alerts],
            "monitoring_running": self._running,
            "timestamp": get_utc_now().isoformat()
        }

    def get_metrics_summary(self) -> Dict[str, Any]:
        """获取指标摘要"""
        return {
            "metrics": self.metrics_collector.get_all_metrics(),
            "timestamp": get_utc_now().isoformat()
        }


# 全局监控实例
_system_monitor: Optional[SystemMonitor] = None


def get_system_monitor() -> SystemMonitor:
    """获取系统监控实例"""
    global _system_monitor
    if _system_monitor is None:
        _system_monitor = SystemMonitor()
    return _system_monitor


# 便捷函数
async def start_monitoring(interval: float = 30.0) -> None:
    """启动系统监控"""
    monitor = get_system_monitor()
    await monitor.start_monitoring(interval)


async def stop_monitoring() -> None:
    """停止系统监控"""
    monitor = get_system_monitor()
    await monitor.stop_monitoring()


def increment_counter(name: str, value: int = 1, labels: Dict[str, str] = None) -> None:
    """增加计数器"""
    monitor = get_system_monitor()
    monitor.metrics_collector.increment_counter(name, value, labels)


def set_gauge(name: str, value: float, labels: Dict[str, str] = None) -> None:
    """设置仪表盘值"""
    monitor = get_system_monitor()
    monitor.metrics_collector.set_gauge(name, value, labels)


def record_timer(name: str, duration: float, labels: Dict[str, str] = None) -> None:
    """记录计时器"""
    monitor = get_system_monitor()
    monitor.metrics_collector.record_timer(name, duration, labels)


def create_alert(level: AlertLevel, title: str, message: str, metadata: Dict[str, Any] = None) -> Alert:
    """创建告警"""
    monitor = get_system_monitor()
    return monitor.alert_manager.create_alert(level, title, message, metadata)


def register_health_check(name: str, check_func: Callable[[], HealthCheck]) -> None:
    """注册健康检查"""
    monitor = get_system_monitor()
    monitor.health_checker.register_check(name, check_func)


# 导出常用功能
__all__ = [
    "SystemMonitor",
    "MetricsCollector",
    "HealthChecker",
    "AlertManager",
    "Metric",
    "Alert",
    "HealthCheck",
    "MetricType",
    "AlertLevel",
    "HealthStatus",
    "get_system_monitor",
    "start_monitoring",
    "stop_monitoring",
    "increment_counter",
    "set_gauge",
    "record_timer",
    "create_alert",
    "register_health_check"
]