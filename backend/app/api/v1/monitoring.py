"""
监控和健康检查API端点

提供：
- Prometheus格式的指标导出
- 系统健康检查
- 业务指标查询
"""

from fastapi import APIRouter, Response, Query
from typing import Dict, Any

from app.services.agent.utils.monitoring import get_system_monitor
from app.services.agent.utils.business_metrics import get_business_metrics_collector

router = APIRouter()


@router.get("/metrics")
async def get_prometheus_metrics():
    """
    导出Prometheus格式的指标

    Returns:
        Prometheus text format metrics
    """
    monitor = get_system_monitor()

    # TODO: Task 3 - 实现 export_prometheus() 方法
    # 目前先返回JSON格式的所有指标
    metrics_data = monitor.metrics_collector.get_all_metrics()

    # 临时返回JSON格式（Task 3将实现Prometheus格式）
    import json
    return Response(
        content=json.dumps(metrics_data, indent=2, ensure_ascii=False),
        media_type="application/json"
    )


@router.get("/health")
async def health_check() -> Dict[str, Any]:
    """
    健康检查端点

    Returns:
        系统监控摘要，包括CPU、内存、磁盘等信息
    """
    monitor = get_system_monitor()
    return monitor.get_monitoring_summary()


@router.get("/metrics/business")
async def get_business_metrics(
    time_window_hours: int = Query(24, ge=1, le=2160)
) -> Dict[str, Any]:
    """
    获取业务指标

    Args:
        time_window_hours: 时间窗口（小时），默认24小时，范围1-2160（最多90天）

    Returns:
        业务指标摘要，包括内容生成、LLM调用、用户行为等
    """
    collector = get_business_metrics_collector()
    return collector.get_business_summary(time_window_hours=time_window_hours)
