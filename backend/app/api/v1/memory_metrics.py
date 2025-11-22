"""
记忆系统监控API (P1-5修复)

提供监控指标查询和健康检查接口
"""

from fastapi import APIRouter, HTTPException
from typing import Dict, Any
import logging

from app.services.agent.memory import get_metrics, HealthStatus

logger = logging.getLogger(__name__)

router = APIRouter()


@router.get("/metrics", summary="获取记忆系统监控指标")
async def get_memory_metrics() -> Dict[str, Any]:
    """
    获取记忆系统的所有监控指标

    Returns:
        包含容量、性能、质量和异常指标的字典

    示例:
        GET /api/v1/memory-metrics/metrics

        Response:
        {
            "capacity": {
                "short_term_usage": 0.65,
                "medium_term_usage": 0.42,
                ...
            },
            "performance": {
                "retrieval_latency": {
                    "p50": 12.5,
                    "p95": 45.2,
                    "p99": 78.1
                },
                ...
            },
            ...
        }
    """
    try:
        metrics = get_metrics()
        return metrics.export_metrics()
    except Exception as e:
        logger.error(f"Failed to export metrics: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to export metrics: {str(e)}")


@router.get("/health", summary="记忆系统健康检查")
async def health_check() -> Dict[str, Any]:
    """
    执行记忆系统健康检查

    Returns:
        包含健康状态、指标汇总和告警信息的字典

    示例:
        GET /api/v1/memory-metrics/health

        Response:
        {
            "status": "healthy",
            "timestamp": "2025-11-22T10:00:00Z",
            "summary": "状态: healthy | 容量: 短期65% 中期42% | 检索P95: 45.2ms",
            "capacity_metrics": {...},
            "performance_metrics": {...},
            "quality_metrics": {...},
            "error_metrics": {...},
            "alerts": []
        }
    """
    try:
        metrics = get_metrics()
        report = metrics.health_check()

        return {
            "status": report.status.value,
            "timestamp": report.timestamp.isoformat(),
            "summary": report.summary,
            "capacity_metrics": report.capacity_metrics,
            "performance_metrics": report.performance_metrics,
            "quality_metrics": report.quality_metrics,
            "error_metrics": report.error_metrics,
            "alerts": [
                {
                    "level": alert.level,
                    "title": alert.title,
                    "message": alert.message,
                    "metric_name": alert.metric_name,
                    "current_value": alert.current_value,
                    "threshold": alert.threshold,
                    "timestamp": alert.timestamp.isoformat()
                }
                for alert in report.alerts
            ]
        }
    except Exception as e:
        logger.error(f"Health check failed: {e}")
        raise HTTPException(status_code=500, detail=f"Health check failed: {str(e)}")


@router.get("/stats", summary="获取简化的统计信息")
async def get_stats() -> Dict[str, Any]:
    """
    获取简化的统计信息（用于仪表板）

    Returns:
        简化的指标摘要

    示例:
        GET /api/v1/memory-metrics/stats

        Response:
        {
            "status": "healthy",
            "total_operations": 1234,
            "error_rate": 0.02,
            "avg_retrieval_latency_ms": 35.6,
            "capacity_usage": {
                "short_term": 0.65,
                "medium_term": 0.42
            }
        }
    """
    try:
        metrics = get_metrics()
        exported = metrics.export_metrics()

        # 简化统计
        total_ops = (
            exported["operations"]["total_retrievals"] +
            exported["operations"]["total_writes"] +
            exported["operations"]["total_forgets"]
        )

        error_rate = (
            exported["errors"]["redis_errors"] / total_ops
            if total_ops > 0 else 0
        )

        retrieval_stats = exported["performance"]["retrieval_latency"]
        avg_latency = retrieval_stats.get("mean", 0) or 0

        return {
            "status": metrics.health_check().status.value,
            "total_operations": total_ops,
            "error_rate": round(error_rate, 4),
            "avg_retrieval_latency_ms": round(avg_latency, 2),
            "capacity_usage": {
                "short_term": round(exported["capacity"]["short_term_usage"], 2),
                "medium_term": round(exported["capacity"]["medium_term_usage"], 2)
            },
            "error_counts": {
                "redis_errors": exported["errors"]["redis_errors"],
                "fallback_triggered": exported["errors"]["fallback_triggered"],
                "data_loss_events": exported["errors"]["data_loss_events"]
            }
        }
    except Exception as e:
        logger.error(f"Failed to get stats: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to get stats: {str(e)}")


@router.post("/reset", summary="重置监控指标（仅用于测试）")
async def reset_metrics() -> Dict[str, str]:
    """
    重置所有监控指标（仅用于测试环境）

    ⚠️ 警告: 这会清空所有历史监控数据

    Returns:
        操作结果消息
    """
    try:
        metrics = get_metrics()

        # 重置所有计数器和直方图
        metrics.short_term_usage.set(0)
        metrics.medium_term_usage.set(0)
        metrics.long_term_usage.set(0)
        metrics.redis_memory_usage.set(0)

        metrics.retrieval_latency.reset()
        metrics.write_latency.reset()
        metrics.forget_latency.reset()
        metrics.context_build_latency.reset()

        metrics.importance_distribution.reset()

        metrics.redis_errors.reset()
        metrics.fallback_triggered.reset()
        metrics.data_loss_events.reset()
        metrics.truncation_events.reset()

        metrics.total_retrievals.reset()
        metrics.total_writes.reset()
        metrics.total_forgets.reset()

        logger.info("[MemoryMetrics] All metrics have been reset")

        return {"message": "All metrics have been reset successfully"}

    except Exception as e:
        logger.error(f"Failed to reset metrics: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to reset metrics: {str(e)}")
