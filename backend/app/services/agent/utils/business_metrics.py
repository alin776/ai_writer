"""
业务指标监控模块

专门用于监控AI Writer系统的业务指标，包括用户操作、内容生成、质量评估等。
"""

import time
from typing import Dict, Any, List, Optional
from datetime import datetime, timedelta
from dataclasses import dataclass, field
from enum import Enum
from collections import defaultdict, deque
import threading

from .monitoring import get_system_monitor, MetricType, HealthStatus, HealthCheck
from .logger import get_logger
from app.utils.datetime_utils import get_utc_now

logger = get_logger("business_metrics")


class ContentType(Enum):
    """内容类型"""
    NOVEL_CHAPTER = "novel_chapter"
    NOVEL_OUTLINE = "novel_outline"
    CHARACTER_PROFILE = "character_profile"
    STORY_SYNOPSIS = "story_synopsis"
    DIALOGUE = "dialogue"
    SCENE_DESCRIPTION = "scene_description"
    OTHER = "other"


class OperationType(Enum):
    """操作类型"""
    CONTENT_GENERATION = "content_generation"
    CONTENT_EDITING = "content_editing"
    CONTENT_ANALYSIS = "content_analysis"
    QUALITY_EVALUATION = "quality_evaluation"
    EXPORT = "export"
    IMPORT = "import"
    SEARCH = "search"


class UserAction(Enum):
    """用户操作"""
    LOGIN = "login"
    LOGOUT = "logout"
    CREATE_PROJECT = "create_project"
    OPEN_PROJECT = "open_project"
    SAVE_PROJECT = "save_project"
    GENERATE_CONTENT = "generate_content"
    EDIT_CONTENT = "edit_content"
    DELETE_CONTENT = "delete_content"


@dataclass
class ContentMetrics:
    """内容指标"""
    content_id: str
    content_type: ContentType
    operation: OperationType
    user_id: Optional[str] = None
    project_id: Optional[str] = None

    # 生成指标
    tokens_generated: int = 0
    generation_time: float = 0.0
    quality_score: float = 0.0

    # 编辑指标
    edit_count: int = 0
    last_edited: Optional[datetime] = None

    # 元数据
    metadata: Dict[str, Any] = field(default_factory=dict)
    timestamp: datetime = field(default_factory=datetime.now)


@dataclass
class UserMetrics:
    """用户指标"""
    user_id: str
    session_id: Optional[str] = None

    # 活动指标
    actions_count: int = 0
    session_duration: float = 0.0
    last_activity: Optional[datetime] = None

    # 生成指标
    total_content_generated: int = 0
    total_tokens_generated: int = 0
    average_quality_score: float = 0.0

    # 项目指标
    projects_created: int = 0
    projects_modified: int = 0

    # 元数据
    metadata: Dict[str, Any] = field(default_factory=dict)

    timestamp: datetime = field(default_factory=datetime.now)


@dataclass
class SystemPerformanceMetrics:
    """系统性能指标"""
    # LLM 调用指标
    llm_calls_total: int = 0
    llm_calls_successful: int = 0
    llm_calls_failed: int = 0
    llm_response_time_total: float = 0.0
    llm_tokens_total: int = 0
    llm_cost_total: float = 0.0

    # 工具调用指标
    tool_calls_total: int = 0
    tool_calls_successful: int = 0
    tool_calls_failed: int = 0
    tool_response_time_total: float = 0.0

    # 缓存指标
    cache_hits: int = 0
    cache_misses: int = 0
    cache_hit_rate: float = 0.0

    # 内存指标
    memory_usage_mb: float = 0.0
    memory_peak_mb: float = 0.0

    # 元数据
    metadata: Dict[str, Any] = field(default_factory=dict)

    timestamp: datetime = field(default_factory=datetime.now)


class BusinessMetricsCollector:
    """业务指标收集器"""

    def __init__(self, max_history: int = 10000):
        """
        初始化业务指标收集器

        Args:
            max_history: 最大历史记录数量
        """
        self.max_history = max_history
        self._lock = threading.Lock()

        # 指标存储
        self._content_metrics: deque = deque(maxlen=max_history)
        self._user_metrics: Dict[str, deque] = defaultdict(lambda: deque(maxlen=1000))
        self._performance_metrics: deque = deque(maxlen=1000)

        # 统计缓存
        self._daily_stats: Dict[str, Dict[str, Any]] = {}
        self._hourly_stats: Dict[str, Dict[str, Any]] = {}

        # 获取系统监控器
        self.system_monitor = get_system_monitor()

        # 注册业务健康检查
        self._register_health_checks()

    def track_content_generation(
        self,
        content_id: str,
        content_type: ContentType,
        user_id: str,
        project_id: str,
        tokens_generated: int,
        generation_time: float,
        quality_score: float,
        metadata: Dict[str, Any] = None
    ) -> None:
        """跟踪内容生成"""
        with self._lock:
            # 记录内容指标
            content_metric = ContentMetrics(
                content_id=content_id,
                content_type=content_type,
                operation=OperationType.CONTENT_GENERATION,
                user_id=user_id,
                project_id=project_id,
                tokens_generated=tokens_generated,
                generation_time=generation_time,
                quality_score=quality_score,
                metadata=metadata or {}
            )
            self._content_metrics.append(content_metric)

            # 更新系统监控指标
            self.system_monitor.metrics_collector.increment_counter(
                "content_generation_total",
                labels={"content_type": content_type.value, "user_id": user_id}
            )
            self.system_monitor.metrics_collector.record_timer(
                "content_generation_time",
                generation_time,
                labels={"content_type": content_type.value}
            )
            self.system_monitor.metrics_collector.increment_counter(
                "tokens_generated_total",
                tokens_generated,
                labels={"content_type": content_type.value}
            )
            self.system_monitor.metrics_collector.set_gauge(
                "content_quality_score",
                quality_score,
                labels={"content_type": content_type.value}
            )

        logger.info(f"Tracked content generation: {content_type.value} - {tokens_generated} tokens, quality: {quality_score:.2f}")

    def track_content_editing(
        self,
        content_id: str,
        content_type: ContentType,
        user_id: str,
        edit_operation: str,
        metadata: Dict[str, Any] = None
    ) -> None:
        """跟踪内容编辑"""
        with self._lock:
            # 查找现有内容指标
            existing_metric = None
            for metric in reversed(self._content_metrics):
                if metric.content_id == content_id:
                    existing_metric = metric
                    break

            if existing_metric:
                existing_metric.edit_count += 1
                existing_metric.last_edited = get_utc_now()
                existing_metric.metadata.update(metadata or {})

            # 更新系统监控指标
            self.system_monitor.metrics_collector.increment_counter(
                "content_editing_total",
                labels={"content_type": content_type.value, "operation": edit_operation}
            )

        logger.info(f"Tracked content editing: {content_type.value} - {edit_operation}")

    def track_user_action(
        self,
        user_id: str,
        action: UserAction,
        session_id: Optional[str] = None,
        metadata: Dict[str, Any] = None
    ) -> None:
        """跟踪用户操作"""
        with self._lock:
            # 获取或创建用户指标队列
            user_queue = self._user_metrics[user_id]

            # 创建用户指标
            user_metric = UserMetrics(
                user_id=user_id,
                session_id=session_id,
                actions_count=1,
                last_activity=get_utc_now(),
                metadata=metadata or {}
            )

            # 根据操作类型更新指标
            if action == UserAction.CREATE_PROJECT:
                user_metric.projects_created = 1
            elif action in [UserAction.GENERATE_CONTENT, UserAction.EDIT_CONTENT]:
                user_metric.total_content_generated = 1

            user_queue.append(user_metric)

            # 更新系统监控指标
            self.system_monitor.metrics_collector.increment_counter(
                "user_actions_total",
                labels={"action": action.value, "user_id": user_id}
            )
            self.system_monitor.metrics_collector.set_gauge(
                "active_users",
                len(self._get_active_users()),
                labels={"time_window": "1h"}
            )

        logger.info(f"Tracked user action: {user_id} - {action.value}")

    def track_llm_call(
        self,
        model: str,
        tokens_used: Dict[str, int],
        cost: float,
        response_time: float,
        success: bool,
        metadata: Dict[str, Any] = None
    ) -> None:
        """跟踪LLM调用"""
        total_tokens = sum(tokens_used.values())

        with self._lock:
            # 记录性能指标
            perf_metric = SystemPerformanceMetrics(
                llm_calls_total=1,
                llm_calls_successful=1 if success else 0,
                llm_calls_failed=0 if success else 1,
                llm_response_time_total=response_time,
                llm_tokens_total=total_tokens,
                llm_cost_total=cost,
                metadata=metadata or {}
            )
            self._performance_metrics.append(perf_metric)

            # 更新系统监控指标
            self.system_monitor.metrics_collector.increment_counter(
                "llm_calls_total",
                labels={"model": model, "success": str(success)}
            )
            self.system_monitor.metrics_collector.record_timer(
                "llm_response_time",
                response_time,
                labels={"model": model}
            )
            self.system_monitor.metrics_collector.increment_counter(
                "llm_tokens_total",
                total_tokens,
                labels={"model": model}
            )
            self.system_monitor.metrics_collector.increment_counter(
                "llm_cost_total",
                cost,
                labels={"model": model}
            )

        logger.info(f"Tracked LLM call: {model} - {total_tokens} tokens, cost: ${cost:.4f}")

    def track_tool_call(
        self,
        tool_name: str,
        parameters: Dict[str, Any],
        response_time: float,
        success: bool,
        metadata: Dict[str, Any] = None
    ) -> None:
        """跟踪工具调用"""
        with self._lock:
            # 记录性能指标
            perf_metric = SystemPerformanceMetrics(
                tool_calls_total=1,
                tool_calls_successful=1 if success else 0,
                tool_calls_failed=0 if success else 1,
                tool_response_time_total=response_time,
                metadata=metadata or {}
            )
            self._performance_metrics.append(perf_metric)

            # 更新系统监控指标
            self.system_monitor.metrics_collector.increment_counter(
                "tool_calls_total",
                labels={"tool": tool_name, "success": str(success)}
            )
            self.system_monitor.metrics_collector.record_timer(
                "tool_response_time",
                response_time,
                labels={"tool": tool_name}
            )

        logger.info(f"Tracked tool call: {tool_name} - success: {success}")

    def track_cache_operation(self, hit: bool, cache_type: str = "default") -> None:
        """跟踪缓存操作"""
        with self._lock:
            # 更新系统监控指标
            self.system_monitor.metrics_collector.increment_counter(
                "cache_operations_total",
                labels={"type": cache_type, "result": "hit" if hit else "miss"}
            )

        logger.debug(f"Cache {cache_type}: {'hit' if hit else 'miss'}")

    def _get_active_users(self, time_window_minutes: int = 60) -> List[str]:
        """获取活跃用户列表"""
        cutoff_time = get_utc_now() - timedelta(minutes=time_window_minutes)
        active_users = set()

        for user_id, user_queue in self._user_metrics.items():
            for metric in user_queue:
                if metric.last_activity and metric.last_activity >= cutoff_time:
                    active_users.add(user_id)
                    break

        return list(active_users)

    def _register_health_checks(self) -> None:
        """注册业务健康检查"""
        self.system_monitor.health_checker.register_check(
            "content_quality",
            self._check_content_quality
        )
        self.system_monitor.health_checker.register_check(
            "llm_performance",
            self._check_llm_performance
        )
        self.system_monitor.health_checker.register_check(
            "user_activity",
            self._check_user_activity
        )

    def _check_content_quality(self) -> HealthCheck:
        """检查内容质量"""
        with self._lock:
            if not self._content_metrics:
                return HealthCheck(
                    name="content_quality",
                    status=HealthStatus.UNKNOWN,
                    message="No content metrics available"
                )

            # 计算最近1小时的质量分数
            cutoff_time = get_utc_now() - timedelta(hours=1)
            recent_metrics = [
                m for m in self._content_metrics
                if m.timestamp >= cutoff_time and m.quality_score > 0
            ]

            if not recent_metrics:
                return HealthCheck(
                    name="content_quality",
                    status=HealthStatus.UNKNOWN,
                    message="No recent content quality data"
                )

            avg_quality = sum(m.quality_score for m in recent_metrics) / len(recent_metrics)

            if avg_quality < 0.6:
                status = HealthStatus.WARNING
                message = f"Low average content quality: {avg_quality:.2f}"
            else:
                status = HealthStatus.HEALTHY
                message = f"Average content quality: {avg_quality:.2f}"

            return HealthCheck(
                name="content_quality",
                status=status,
                message=message,
                details={
                    "average_quality": avg_quality,
                    "sample_count": len(recent_metrics),
                    "time_window": "1h"
                }
            )

    def _check_llm_performance(self) -> HealthCheck:
        """检查LLM性能"""
        with self._lock:
            if not self._performance_metrics:
                return HealthCheck(
                    name="llm_performance",
                    status=HealthStatus.UNKNOWN,
                    message="No performance metrics available"
                )

            # 计算最近1小时的LLM调用
            cutoff_time = get_utc_now() - timedelta(hours=1)
            recent_metrics = [
                m for m in self._performance_metrics
                if m.timestamp >= cutoff_time and m.llm_calls_total > 0
            ]

            if not recent_metrics:
                return HealthCheck(
                    name="llm_performance",
                    status=HealthStatus.UNKNOWN,
                    message="No recent LLM calls"
                )

            total_calls = sum(m.llm_calls_total for m in recent_metrics)
            successful_calls = sum(m.llm_calls_successful for m in recent_metrics)
            success_rate = successful_calls / total_calls if total_calls > 0 else 0

            avg_response_time = sum(m.llm_response_time_total for m in recent_metrics) / len(recent_metrics)

            if success_rate < 0.9:
                status = HealthStatus.WARNING
                message = f"Low LLM success rate: {success_rate:.1%}"
            elif avg_response_time > 30:
                status = HealthStatus.WARNING
                message = f"High LLM response time: {avg_response_time:.1f}s"
            else:
                status = HealthStatus.HEALTHY
                message = f"LLM performance: {success_rate:.1%} success, {avg_response_time:.1f}s avg"

            return HealthCheck(
                name="llm_performance",
                status=status,
                message=message,
                details={
                    "success_rate": success_rate,
                    "average_response_time": avg_response_time,
                    "total_calls": total_calls,
                    "time_window": "1h"
                }
            )

    def _check_user_activity(self) -> HealthCheck:
        """检查用户活动"""
        active_users = self._get_active_users(time_window_minutes=60)

        if len(active_users) == 0:
            status = HealthStatus.WARNING
            message = "No active users in the last hour"
        else:
            status = HealthStatus.HEALTHY
            message = f"{len(active_users)} active users in the last hour"

        return HealthCheck(
            name="user_activity",
            status=status,
            message=message,
            details={
                "active_users_count": len(active_users),
                "active_users": active_users,
                "time_window": "1h"
            }
        )

    def get_business_summary(self, time_window_hours: int = 24) -> Dict[str, Any]:
        """获取业务摘要"""
        cutoff_time = get_utc_now() - timedelta(hours=time_window_hours)

        with self._lock:
            # 内容统计
            recent_content = [
                m for m in self._content_metrics
                if m.timestamp >= cutoff_time
            ]

            content_stats = {
                "total_generated": len(recent_content),
                "by_type": defaultdict(int),
                "average_quality": 0.0,
                "total_tokens": 0,
                "unique_users": len(set(m.user_id for m in recent_content if m.user_id))
            }

            if recent_content:
                content_stats["average_quality"] = sum(m.quality_score for m in recent_content if m.quality_score > 0) / len([m for m in recent_content if m.quality_score > 0])
                content_stats["total_tokens"] = sum(m.tokens_generated for m in recent_content)

                for m in recent_content:
                    content_stats["by_type"][m.content_type.value] += 1

            # 用户活动统计
            active_users = self._get_active_users(time_window_minutes=time_window_hours * 60)

            # 性能统计
            recent_performance = [
                m for m in self._performance_metrics
                if m.timestamp >= cutoff_time
            ]

            performance_stats = {
                "llm_calls_total": sum(m.llm_calls_total for m in recent_performance),
                "llm_success_rate": 0.0,
                "llm_avg_response_time": 0.0,
                "llm_total_cost": sum(m.llm_cost_total for m in recent_performance),
                "tool_calls_total": sum(m.tool_calls_total for m in recent_performance)
            }

            if recent_performance:
                total_llm_calls = sum(m.llm_calls_total for m in recent_performance)
                successful_llm_calls = sum(m.llm_calls_successful for m in recent_performance)
                performance_stats["llm_success_rate"] = successful_llm_calls / total_llm_calls if total_llm_calls > 0 else 0

                if total_llm_calls > 0:
                    performance_stats["llm_avg_response_time"] = sum(m.llm_response_time_total for m in recent_performance) / total_llm_calls

            return {
                "time_window_hours": time_window_hours,
                "content_metrics": content_stats,
                "user_metrics": {
                    "active_users_count": len(active_users),
                    "active_users": active_users
                },
                "performance_metrics": performance_stats,
                "timestamp": get_utc_now().isoformat()
            }

    def get_detailed_metrics(self, limit: int = 1000) -> Dict[str, Any]:
        """获取详细指标"""
        with self._lock:
            return {
                "content_metrics": [
                    {
                        "content_id": m.content_id,
                        "content_type": m.content_type.value,
                        "operation": m.operation.value,
                        "user_id": m.user_id,
                        "project_id": m.project_id,
                        "tokens_generated": m.tokens_generated,
                        "generation_time": m.generation_time,
                        "quality_score": m.quality_score,
                        "edit_count": m.edit_count,
                        "timestamp": m.timestamp.isoformat(),
                        "metadata": m.metadata
                    }
                    for m in list(self._content_metrics)[-limit:]
                ],
                "user_metrics": {
                    user_id: [
                        {
                            "session_id": m.session_id,
                            "actions_count": m.actions_count,
                            "session_duration": m.session_duration,
                            "total_content_generated": m.total_content_generated,
                            "projects_created": m.projects_created,
                            "timestamp": m.timestamp.isoformat()
                        }
                        for m in list(metrics)[-limit:]
                    ]
                    for user_id, metrics in self._user_metrics.items()
                },
                "performance_metrics": [
                    {
                        "llm_calls_total": m.llm_calls_total,
                        "llm_calls_successful": m.llm_calls_successful,
                        "llm_calls_failed": m.llm_calls_failed,
                        "llm_response_time_total": m.llm_response_time_total,
                        "llm_tokens_total": m.llm_tokens_total,
                        "llm_cost_total": m.llm_cost_total,
                        "tool_calls_total": m.tool_calls_total,
                        "timestamp": m.timestamp.isoformat()
                    }
                    for m in list(self._performance_metrics)[-limit:]
                ]
            }


# 全局业务指标收集器实例
_business_metrics_collector: Optional[BusinessMetricsCollector] = None


def get_business_metrics_collector() -> BusinessMetricsCollector:
    """获取业务指标收集器实例"""
    global _business_metrics_collector
    if _business_metrics_collector is None:
        _business_metrics_collector = BusinessMetricsCollector()
    return _business_metrics_collector


# 便捷函数
def track_content_generation(
    content_id: str,
    content_type: ContentType,
    user_id: str,
    project_id: str,
    tokens_generated: int,
    generation_time: float,
    quality_score: float,
    metadata: Dict[str, Any] = None
) -> None:
    """跟踪内容生成"""
    collector = get_business_metrics_collector()
    collector.track_content_generation(
        content_id, content_type, user_id, project_id,
        tokens_generated, generation_time, quality_score, metadata
    )


def track_user_action(
    user_id: str,
    action: UserAction,
    session_id: Optional[str] = None,
    metadata: Dict[str, Any] = None
) -> None:
    """跟踪用户操作"""
    collector = get_business_metrics_collector()
    collector.track_user_action(user_id, action, session_id, metadata)


def track_llm_call(
    model: str,
    tokens_used: Dict[str, int],
    cost: float,
    response_time: float,
    success: bool,
    metadata: Dict[str, Any] = None
) -> None:
    """跟踪LLM调用"""
    collector = get_business_metrics_collector()
    collector.track_llm_call(model, tokens_used, cost, response_time, success, metadata)


def get_business_summary(time_window_hours: int = 24) -> Dict[str, Any]:
    """获取业务摘要"""
    collector = get_business_metrics_collector()
    return collector.get_business_summary(time_window_hours)


# 导出常用功能
__all__ = [
    "BusinessMetricsCollector",
    "ContentMetrics",
    "UserMetrics",
    "SystemPerformanceMetrics",
    "ContentType",
    "OperationType",
    "UserAction",
    "get_business_metrics_collector",
    "track_content_generation",
    "track_user_action",
    "track_llm_call",
    "get_business_summary"
]