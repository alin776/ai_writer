"""
Humanize API - AI去痕迹功能管理接口
"""

import logging
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
    HumanizeRequest,
    HumanizeSessionResponse,
    HumanizeHistoryResponse,
    HumanizeStatsResponse,
    UserFeedbackRequest,
    HumanizeSessionCreate,
)
from app.services.user_profile_service import UserProfileService
from app.services.ai.humanize_service import HumanizeService
from app.core.humanize_config import HumanizeConfig

router = APIRouter()
logger = logging.getLogger(__name__)


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


@router.post("/rewrite", response_model=HumanizeSessionResponse)
async def humanize_rewrite(
    request: HumanizeRequest,
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db)
):
    """
    执行去痕迹改写并保存会话

    完整流程:
    1. 检测AI痕迹 (使用快速模型)
    2. 执行改写 (使用标准模型)
    3. (可选)验证效果 (使用快速模型)
    4. 保存会话到数据库
    5. 更新用户画像

    Args:
        request: 去痕迹请求 (text, intensity, ai_function)

    Returns:
        HumanizeSessionResponse: 包含改写结果和会话ID的响应
    """
    # 1. 获取用户画像，根据用户配置决定是否启用验证
    profile_service = UserProfileService(db)
    profile = await profile_service.get_or_create_profile(current_user.id)

    # 2. 创建配置 (根据用户画像)
    config = HumanizeConfig(
        enable_detection=True,  # 总是启用检测
        enable_verification=profile.humanize_enabled_by_function.get("rewrite", False),  # 根据用户配置
    )

    # 3. 初始化HumanizeService
    humanize_service = HumanizeService(config=config)

    try:
        # 4. 执行完整的去痕迹流程
        result = await humanize_service.full_humanize_process(
            text=request.text,
            intensity=request.intensity,
            skip_detection=False,
            skip_verification=None  # 使用config配置
        )

        detection = result.get("detection")
        humanized_text = result.get("humanized_text", "")
        verification = result.get("verification")
        processing_time = result.get("processing_time", 0)

        # 5. 计算token和成本 (使用实际值)
        total_tokens = result.get("total_tokens", 0)
        detection_tokens = result.get("detection_tokens", 0)
        rewrite_tokens = result.get("rewrite_tokens", 0)
        verification_tokens = result.get("verification_tokens", 0)

        # 如果没有获取到实际token,使用估算
        if total_tokens == 0:
            text_length = len(request.text)
            total_tokens = int(text_length * 1.5 * 2.5)  # 降级估算
            logger.warning(f"未获取到实际token消耗,使用估算值: {total_tokens}")

        # 计算成本 (gemini-2.5-flash-lite + gpt-4o-mini混合定价)
        # 检测+验证使用快速模型,改写使用标准模型
        detection_cost = detection_tokens * 0.0000002  # flash-lite更便宜
        rewrite_cost = rewrite_tokens * 0.000002  # 标准模型
        verification_cost = verification_tokens * 0.0000002
        estimated_cost = detection_cost + rewrite_cost + verification_cost

        logger.info(
            f"Token统计 - 总计: {total_tokens} "
            f"(检测:{detection_tokens}, 改写:{rewrite_tokens}, 验证:{verification_tokens}), "
            f"成本: ${estimated_cost:.6f}"
        )

        # 6. 构建会话数据
        score_before = detection.overall_score if detection else 70.0
        score_after = verification.score_after if verification else 50.0
        improvement = score_before - score_after

        # 创建会话记录
        session = HumanizeSession(
            user_id=current_user.id,
            ai_function=request.ai_function or "rewrite",
            score_before=score_before,
            score_after=score_after,
            improvement=improvement,
            intensity=request.intensity,
            processing_time=processing_time,
            tokens_used=total_tokens,  # 使用实际token
            cost=estimated_cost,  # 使用实际成本
            user_accepted=None  # 用户稍后反馈
        )

        db.add(session)
        await db.flush()  # 刷新以获取session.id

        # 转换DimensionScore对象为字典 (JSONB字段需要纯字典)
        dimensions_before_dict = {}
        if detection and detection.dimensions:
            dimensions_before_dict = {
                key: dim.model_dump()  # Pydantic v2: model_dump(), v1: dict()
                for key, dim in detection.dimensions.items()
            }

        # 创建会话详情 (包含完整数据,7天后过期)
        detail = HumanizeSessionDetail(
            session_id=session.id,
            original_preview=request.text[:200],  # 仅保存前200字符
            humanized_preview=humanized_text[:200],
            dimensions_before=dimensions_before_dict,  # ← 使用转换后的字典
            dimensions_after={},  # 验证阶段不返回详细维度
            detected_patterns=detection.detected_patterns if detection else [],
            expires_at=datetime.utcnow() + timedelta(days=7)
        )

        db.add(detail)

        # 7. 更新用户画像统计
        await profile_service.record_humanize_use(
            user_id=current_user.id,
            text_length=text_length,
            ai_function=request.ai_function or "rewrite",
            intensity=request.intensity,
            improvement=improvement
        )

        # 8. 提交事务
        await db.commit()
        await db.refresh(session)
        await db.refresh(detail)

        logger.info(
            f"去痕迹会话已保存: session_id={session.id}, "
            f"improvement={improvement:.1f}, tokens={estimated_tokens}"
        )

        # 9. 返回响应
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
            detail=detail
        )

    except Exception as e:
        logger.error(f"去痕迹改写失败: {type(e).__name__}: {e}")
        await db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"AI去痕迹处理失败: {str(e)}"
        )
    finally:
        # 确保关闭Service
        await humanize_service.close()
