"""
Humanize API - AI去痕迹功能管理接口
"""

from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func, and_
from typing import List
from uuid import UUID
from datetime import datetime, timedelta

from app.core.database import get_db
from app.core.security import get_current_active_user
from app.models.user import User
from app.models.humanize_session import HumanizeSession, HumanizeSessionDetail
from app.schemas.humanize import (
    UserProfileResponse,
    UserProfileUpdateRequest,
    HumanizeSessionResponse,
    HumanizeHistoryResponse,
    HumanizeStatsResponse,
    UserFeedbackRequest,
)
from app.services.user_profile_service import UserProfileService

router = APIRouter()


@router.get("/profile", response_model=UserProfileResponse)
async def get_user_profile(
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db)
):
    """
    获取当前用户的去痕迹画像

    返回用户的偏好设置、使用统计、开关配置等信息
    """
    profile_service = UserProfileService(db)
    profile = await profile_service.get_or_create_profile(current_user.id)

    return UserProfileResponse(
        id=profile.id,
        user_id=profile.user_id,
        total_uses=profile.total_uses,
        avg_text_length=profile.avg_text_length,
        most_used_function=profile.most_used_function,
        preferred_intensity=profile.preferred_intensity,
        preferred_speed_over_quality=profile.preferred_speed_over_quality,
        is_novel_writer=profile.is_novel_writer,
        total_accepted=profile.total_accepted,
        total_rejected=profile.total_rejected,
        accept_rate=profile.accept_rate,
        humanize_enabled_global=profile.humanize_enabled_global,
        humanize_enabled_by_function=profile.humanize_enabled_by_function,
        display_mode=profile.display_mode,
        created_at=profile.created_at,
        updated_at=profile.updated_at
    )


@router.put("/profile/settings", response_model=UserProfileResponse)
async def update_profile_settings(
    settings: UserProfileUpdateRequest,
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db)
):
    """
    更新用户的去痕迹设置

    可以更新:
    - 全局开关
    - 分功能开关
    - 偏好强度
    """
    profile_service = UserProfileService(db)

    profile = await profile_service.update_profile_settings(
        current_user.id,
        settings
    )

    return UserProfileResponse(
        id=profile.id,
        user_id=profile.user_id,
        total_uses=profile.total_uses,
        avg_text_length=profile.avg_text_length,
        most_used_function=profile.most_used_function,
        preferred_intensity=profile.preferred_intensity,
        preferred_speed_over_quality=profile.preferred_speed_over_quality,
        is_novel_writer=profile.is_novel_writer,
        total_accepted=profile.total_accepted,
        total_rejected=profile.total_rejected,
        accept_rate=profile.accept_rate,
        humanize_enabled_global=profile.humanize_enabled_global,
        humanize_enabled_by_function=profile.humanize_enabled_by_function,
        display_mode=profile.display_mode,
        created_at=profile.created_at,
        updated_at=profile.updated_at
    )


@router.get("/history", response_model=HumanizeHistoryResponse)
async def get_humanize_history(
    page: int = Query(1, ge=1, description="页码"),
    page_size: int = Query(20, ge=1, le=100, description="每页数量"),
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db)
):
    """
    获取去痕迹历史记录 (分页)

    返回用户的历史去痕迹会话,包含核心数据和详情数据(如果未过期)
    """
    # 计算分页
    offset = (page - 1) * page_size

    # 查询总数
    count_result = await db.execute(
        select(func.count(HumanizeSession.id))
        .where(HumanizeSession.user_id == current_user.id)
    )
    total = count_result.scalar_one()

    # 查询会话列表
    result = await db.execute(
        select(HumanizeSession)
        .where(HumanizeSession.user_id == current_user.id)
        .order_by(HumanizeSession.created_at.desc())
        .offset(offset)
        .limit(page_size)
    )
    sessions = result.scalars().all()

    # 构建响应
    items = []
    for session in sessions:
        # 尝试加载详情数据 (如果未过期)
        detail_result = await db.execute(
            select(HumanizeSessionDetail)
            .where(
                and_(
                    HumanizeSessionDetail.session_id == session.id,
                    HumanizeSessionDetail.expires_at > datetime.utcnow()
                )
            )
        )
        detail = detail_result.scalar_one_or_none()

        items.append(HumanizeSessionResponse(
            id=session.id,
            user_id=session.user_id,
            ai_function=session.ai_function,
            score_before=session.score_before,
            score_after=session.score_after,
            improvement=session.improvement,
            intensity=session.intensity,
            user_accepted=session.user_accepted,
            processing_time=session.processing_time,
            tokens_used=session.tokens_used,
            cost=session.cost,
            created_at=session.created_at,
            detail=detail if detail else None
        ))

    return HumanizeHistoryResponse(
        total=total,
        items=items,
        page=page,
        page_size=page_size
    )


@router.get("/history/{session_id}", response_model=HumanizeSessionResponse)
async def get_humanize_session(
    session_id: UUID,
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db)
):
    """
    获取单条去痕迹历史详情

    返回指定会话的完整信息
    """
    # 查询会话
    result = await db.execute(
        select(HumanizeSession)
        .where(
            and_(
                HumanizeSession.id == session_id,
                HumanizeSession.user_id == current_user.id
            )
        )
    )
    session = result.scalar_one_or_none()

    if not session:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Session not found"
        )

    # 尝试加载详情数据
    detail_result = await db.execute(
        select(HumanizeSessionDetail)
        .where(
            and_(
                HumanizeSessionDetail.session_id == session.id,
                HumanizeSessionDetail.expires_at > datetime.utcnow()
            )
        )
    )
    detail = detail_result.scalar_one_or_none()

    return HumanizeSessionResponse(
        id=session.id,
        user_id=session.user_id,
        ai_function=session.ai_function,
        score_before=session.score_before,
        score_after=session.score_after,
        improvement=session.improvement,
        intensity=session.intensity,
        user_accepted=session.user_accepted,
        processing_time=session.processing_time,
        tokens_used=session.tokens_used,
        cost=session.cost,
        created_at=session.created_at,
        detail=detail if detail else None
    )


@router.get("/stats", response_model=HumanizeStatsResponse)
async def get_humanize_stats(
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db)
):
    """
    获取去痕迹统计数据

    返回总使用次数、平均改进幅度、接受率、Token消耗等统计信息
    """
    # 查询统计数据
    result = await db.execute(
        select(
            func.count(HumanizeSession.id).label("total_uses"),
            func.avg(HumanizeSession.improvement).label("avg_improvement"),
            func.sum(HumanizeSession.tokens_used).label("total_tokens"),
            func.sum(HumanizeSession.cost).label("total_cost")
        )
        .where(HumanizeSession.user_id == current_user.id)
    )
    stats = result.one()

    # 查询最常用功能
    function_result = await db.execute(
        select(
            HumanizeSession.ai_function,
            func.count(HumanizeSession.id).label("count")
        )
        .where(HumanizeSession.user_id == current_user.id)
        .group_by(HumanizeSession.ai_function)
        .order_by(func.count(HumanizeSession.id).desc())
        .limit(1)
    )
    most_used = function_result.first()

    # 计算接受率
    feedback_result = await db.execute(
        select(
            func.count(HumanizeSession.id).filter(HumanizeSession.user_accepted == True).label("accepted"),
            func.count(HumanizeSession.id).filter(HumanizeSession.user_accepted == False).label("rejected")
        )
        .where(HumanizeSession.user_id == current_user.id)
    )
    feedback = feedback_result.one()

    total_feedback = (feedback.accepted or 0) + (feedback.rejected or 0)
    accept_rate = (feedback.accepted or 0) / total_feedback if total_feedback > 0 else 0.0

    return HumanizeStatsResponse(
        total_uses=stats.total_uses or 0,
        avg_improvement=float(stats.avg_improvement) if stats.avg_improvement else 0.0,
        accept_rate=accept_rate,
        total_tokens=stats.total_tokens or 0,
        total_cost=float(stats.total_cost) if stats.total_cost else 0.0,
        most_used_function=most_used.ai_function if most_used else None
    )


@router.post("/feedback")
async def submit_feedback(
    feedback: UserFeedbackRequest,
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db)
):
    """
    提交用户反馈

    用户可以对去痕迹结果进行评价(接受/拒绝)
    """
    # 查询会话
    result = await db.execute(
        select(HumanizeSession)
        .where(
            and_(
                HumanizeSession.id == feedback.session_id,
                HumanizeSession.user_id == current_user.id
            )
        )
    )
    session = result.scalar_one_or_none()

    if not session:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Session not found"
        )

    # 更新会话反馈
    session.user_accepted = feedback.accepted

    # 更新用户画像
    profile_service = UserProfileService(db)
    await profile_service.record_feedback(current_user.id, feedback.accepted)

    await db.commit()

    return {"detail": "Feedback submitted successfully"}
