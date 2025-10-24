"""
AI调用日志和成本统计 API

提供日志查询和成本统计接口
"""

from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List, Optional
from datetime import datetime, timedelta, timezone
from uuid import UUID

from app.core.database import get_db
from app.core.security import get_current_active_user
from app.models.user import User
from app.services.ai_log_service import AILogService
from app.schemas.ai_call_log import (
    AICallLogResponse,
    AICallLogPaginatedResponse,
    AICallLogStats,
    CostMetrics
)

router = APIRouter(prefix="/ai-logs", tags=["AI Logs"])


# 辅助函数：检查管理员权限
async def get_current_admin_user(
    current_user: User = Depends(get_current_active_user)
) -> User:
    """验证当前用户是否为管理员"""
    if not current_user.is_admin:
        from fastapi import HTTPException, status
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="需要管理员权限"
        )
    return current_user


@router.get("/me", response_model=AICallLogPaginatedResponse)
async def get_my_logs(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    start_date: Optional[datetime] = None,
    end_date: Optional[datetime] = None,
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db)
):
    """
    获取当前用户的AI调用日志（分页）

    Args:
        skip: 跳过记录数
        limit: 返回数量限制
        start_date: 开始时间
        end_date: 结束时间

    Returns:
        AICallLogPaginatedResponse: 包含日志列表和总数的分页响应
    """
    log_service = AILogService(db)

    # 获取日志列表
    logs = await log_service.get_user_logs(
        user_id=current_user.id,
        skip=skip,
        limit=limit,
        start_date=start_date,
        end_date=end_date
    )

    # 获取总数
    total = await log_service.get_user_logs_count(
        user_id=current_user.id,
        start_date=start_date,
        end_date=end_date
    )

    return AICallLogPaginatedResponse(
        logs=logs,
        total=total,
        skip=skip,
        limit=limit
    )


@router.get("/me/stats", response_model=AICallLogStats)
async def get_my_stats(
    days: int = Query(30, ge=1, le=365, description="统计最近N天的数据"),
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db)
):
    """
    获取当前用户的AI使用统计

    Args:
        days: 统计天数（默认30天）
    """
    log_service = AILogService(db)
    end_date = datetime.now(timezone.utc)
    start_date = end_date - timedelta(days=days)

    stats = await log_service.get_stats(
        user_id=current_user.id,
        start_date=start_date,
        end_date=end_date
    )
    return stats


@router.get("/admin/stats", response_model=AICallLogStats)
async def get_all_stats(
    days: int = Query(30, ge=1, le=365, description="统计最近N天的数据"),
    current_user: User = Depends(get_current_admin_user),
    db: AsyncSession = Depends(get_db)
):
    """
    获取所有用户的AI使用统计（仅管理员）

    Args:
        days: 统计天数（默认30天）
    """
    log_service = AILogService(db)
    end_date = datetime.now(timezone.utc)
    start_date = end_date - timedelta(days=days)

    stats = await log_service.get_stats(
        start_date=start_date,
        end_date=end_date
    )
    return stats


@router.get("/admin/cost-metrics", response_model=CostMetrics)
async def get_cost_metrics(
    current_user: User = Depends(get_current_admin_user),
    db: AsyncSession = Depends(get_db)
):
    """
    获取成本指标（仅管理员）

    返回今日、昨日、本月、上月成本，以及成本趋势和Top用户/模型
    """
    log_service = AILogService(db)
    metrics = await log_service.get_cost_metrics()
    return metrics


@router.get("/admin/user/{user_id}/logs", response_model=List[AICallLogResponse])
async def get_user_logs(
    user_id: UUID,
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    start_date: Optional[datetime] = None,
    end_date: Optional[datetime] = None,
    current_user: User = Depends(get_current_admin_user),
    db: AsyncSession = Depends(get_db)
):
    """
    获取指定用户的AI调用日志（仅管理员）

    Args:
        user_id: 用户ID
        skip: 跳过记录数
        limit: 返回数量限制
        start_date: 开始时间
        end_date: 结束时间
    """
    log_service = AILogService(db)
    logs = await log_service.get_user_logs(
        user_id=user_id,
        skip=skip,
        limit=limit,
        start_date=start_date,
        end_date=end_date
    )
    return logs


@router.get("/admin/user/{user_id}/stats", response_model=AICallLogStats)
async def get_user_stats(
    user_id: UUID,
    days: int = Query(30, ge=1, le=365, description="统计最近N天的数据"),
    current_user: User = Depends(get_current_admin_user),
    db: AsyncSession = Depends(get_db)
):
    """
    获取指定用户的AI使用统计（仅管理员）

    Args:
        user_id: 用户ID
        days: 统计天数（默认30天）
    """
    log_service = AILogService(db)
    end_date = datetime.utcnow()
    start_date = end_date - timedelta(days=days)

    stats = await log_service.get_stats(
        user_id=user_id,
        start_date=start_date,
        end_date=end_date
    )
    return stats
