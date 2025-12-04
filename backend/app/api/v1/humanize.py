"""
Humanize API - AI去痕迹功能管理接口
"""

import logging
import json
import time
from fastapi import APIRouter, Depends, HTTPException, status, Query, Request
from fastapi.responses import StreamingResponse
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func, and_
from typing import List
from uuid import UUID
from datetime import datetime, timedelta

from app.core.database import get_db
from app.core.security import get_current_active_user
from app.models.user import User
from app.models.humanize_session import HumanizeSession, HumanizeSessionDetail
from app.models.ai_call_log import AICallLog  # 新增：AI调用日志
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
from app.services.ai.http_ai_service import HTTPAIService
from app.core.humanize_config import HumanizeConfig
from app.services.agent.utils.monitoring import increment_counter, record_timer
from app.api.middleware.rate_limiter import rate_limit, get_user_identifier
from app.utils.cost_calculator import CostCalculator
from app.core.request_context import set_request_context  # ✅ 新增：用于FastAI成本追踪
from app.utils.datetime_utils import get_utc_now

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
                    HumanizeSessionDetail.expires_at > get_utc_now()
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
                HumanizeSessionDetail.expires_at > get_utc_now()
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
@rate_limit(max_requests=20, window_seconds=60, identifier_func=get_user_identifier)  # 每分钟最多20次
async def humanize_rewrite(
    request_data: HumanizeRequest,
    request: Request,
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
    # 0. 安全验证：检查文本字节数（防止超大文本攻击）
    text_bytes = len(request_data.text.encode('utf-8'))
    if text_bytes > HumanizeConfig().max_text_bytes:
        raise HTTPException(
            status_code=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE,
            detail=f"文本字节数超过限制 (当前: {text_bytes} bytes, 最大: {HumanizeConfig().max_text_bytes} bytes)"
        )

    # 1. 获取用户画像，根据用户配置决定是否启用验证
    profile_service = UserProfileService(db)
    profile = await profile_service.get_or_create_profile(current_user.id)

    # 2. 创建配置 (根据用户画像)
    config = HumanizeConfig(
        enable_detection=True,  # 总是启用检测
        enable_verification=profile.humanize_enabled_by_function.get("rewrite", False),  # 根据用户配置
    )

    # 3. 设置请求上下文（用于FastAI成本追踪）
    # ✅ 2025-12-02: FastAIService使用get_request_user_id()获取user_id
    set_request_context(db, str(current_user.id))

    # 4. 初始化HumanizeService
    # 2025-12-01: 传递db和user_id以启用成本追踪
    ai_service = HTTPAIService(db=db, user_id=str(current_user.id))
    humanize_service = HumanizeService(ai_service=ai_service, config=config)

    # 记录请求开始
    request_start = time.time()
    increment_counter("humanize_requests_total", labels={"intensity": request_data.intensity, "function": request_data.ai_function or "rewrite"})

    try:
        # 4. 执行完整的去痕迹流程
        result = await humanize_service.full_humanize_process(
            text=request_data.text,
            intensity=request_data.intensity,
            skip_detection=False,
            skip_verification=None,  # 使用config配置
            use_nlp_preprocessing=None  # 使用config配置
        )

        detection = result.get("detection")
        humanized_text = result.get("humanized_text", "")
        verification = result.get("verification")
        processing_time = result.get("processing_time", 0)

        # 5. 计算token和成本 (使用实际值)
        text_length = len(request_data.text)  # 提前定义
        total_tokens = result.get("total_tokens", 0)
        detection_tokens = result.get("detection_tokens", 0)
        rewrite_tokens = result.get("rewrite_tokens", 0)
        verification_tokens = result.get("verification_tokens", 0)

        # 提取详细的prompt/completion token信息
        detection_prompt = result.get("detection_prompt_tokens", 0)
        detection_completion = result.get("detection_completion_tokens", 0)
        rewrite_prompt = result.get("rewrite_prompt_tokens", 0)
        rewrite_completion = result.get("rewrite_completion_tokens", 0)
        verification_prompt = result.get("verification_prompt_tokens", 0)
        verification_completion = result.get("verification_completion_tokens", 0)

        # 如果没有获取到实际token,使用估算
        if total_tokens == 0:
            total_tokens = int(text_length * 1.5 * 2.5)  # 降级估算
            logger.warning(f"未获取到实际token消耗,使用估算值: {total_tokens}")

        # 计算成本 (使用CostCalculator和实际的prompt/completion token)
        # 检测+验证使用gemini-2.5-flash-lite，改写使用gemini-2.5-pro
        detection_cost_result = CostCalculator.calculate_cost(
            "gemini-2.5-flash-lite",
            detection_prompt,
            detection_completion
        )
        rewrite_cost_result = CostCalculator.calculate_cost(
            "gemini-2.5-pro",
            rewrite_prompt,
            rewrite_completion
        )
        verification_cost_result = CostCalculator.calculate_cost(
            "gemini-2.5-flash-lite",
            verification_prompt,
            verification_completion
        )

        detection_cost = detection_cost_result["total_cost"]
        rewrite_cost = rewrite_cost_result["total_cost"]
        verification_cost = verification_cost_result["total_cost"]
        estimated_cost = detection_cost + rewrite_cost + verification_cost

        logger.info(
            f"Token统计 - 总计: {total_tokens} "
            f"(检测:{detection_tokens}[P:{detection_prompt},C:{detection_completion}], "
            f"改写:{rewrite_tokens}[P:{rewrite_prompt},C:{rewrite_completion}], "
            f"验证:{verification_tokens}[P:{verification_prompt},C:{verification_completion}]), "
            f"成本: ${estimated_cost:.6f}"
        )

        # 6. 构建会话数据
        score_before = detection.overall_score if detection else 70.0
        score_after = verification.score_after if verification else score_before
        improvement = score_before - score_after

        # 创建会话记录
        session = HumanizeSession(
            user_id=current_user.id,
            ai_function=request_data.ai_function or "rewrite",
            score_before=score_before,
            score_after=score_after,
            improvement=improvement,
            intensity=request_data.intensity,
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
            original_preview=request_data.text[:200],  # 仅保存前200字符
            humanized_preview=humanized_text[:200],
            original_full=request_data.text,
            humanized_full=humanized_text,
            dimensions_before=dimensions_before_dict,  # ← 使用转换后的字典
            dimensions_after={},  # 验证阶段不返回详细维度
            detected_patterns=(
                (detection.detected_patterns if detection else [])
                + ([f"NLP:{c}" for c in result.get("nlp_changes", [])] if result.get("nlp_changes") else [])
            ),
            expires_at=get_utc_now() + timedelta(days=7)
        )

        db.add(detail)

        # ✅ 2025-12-02: 移除手动AICallLog记录（会导致重复记录）
        # HTTPAIService和FastAIService已启用自动成本追踪：
        # - 检测阶段: FastAIService._track_cost() → operation_type="humanize_detect"
        # - 改写阶段: HTTPAIService._track_api_cost() → operation_type="content_creation"
        # - 验证阶段: FastAIService._track_cost() → operation_type="humanize_verify"

        # 7. 更新用户画像统计
        await profile_service.record_humanize_use(
            user_id=current_user.id,
            text_length=text_length,
            ai_function=request_data.ai_function or "rewrite",
            intensity=request_data.intensity,
            improvement=improvement
        )

        # 8. 提交事务
        await db.commit()
        await db.refresh(session)
        await db.refresh(detail)

        logger.info(
            f"去痕迹会话已保存: session_id={session.id}, "
            f"improvement={improvement:.1f}, tokens={total_tokens}"
        )

        # 记录监控指标
        request_duration = time.time() - request_start
        record_timer("humanize_request_duration_seconds", request_duration, labels={"intensity": request_data.intensity})
        increment_counter("humanize_requests_success", labels={"intensity": request_data.intensity})
        record_timer("humanize_tokens_used", total_tokens, labels={"intensity": request_data.intensity})
        record_timer("humanize_improvement", improvement, labels={"intensity": request_data.intensity})

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

        # 记录失败指标
        increment_counter("humanize_requests_failed", labels={"intensity": request_data.intensity, "error": type(e).__name__})

        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"AI去痕迹处理失败: {str(e)}"
        )
    finally:
        # 确保关闭Service
        await humanize_service.close()


@router.post("/rewrite/stream")
@rate_limit(max_requests=15, window_seconds=60, identifier_func=get_user_identifier)  # 流式API限制更严格
async def humanize_rewrite_stream(
    request_data: HumanizeRequest,
    request: Request,
    current_user: User = Depends(get_current_active_user)
    # ✅ 修复：移除db依赖，避免生命周期不匹配
):
    """
    流式去痕迹改写API

    提供实时反馈，大幅提升用户体验。

    流程：
    1. 验证输入
    2. 流式输出改写内容（SSE格式）
    3. 自动保存会话到数据库
    4. 发送完成事件（包含session_id）

    响应格式（Server-Sent Events）：
    - data: {"type": "chunk", "content": "改写的文本片段"}
    - data: {"type": "progress", "stage": "detecting", "message": "正在检测AI痕迹..."}
    - data: {"type": "done", "session_id": "xxx", "improvement": 25.5}
    - data: {"type": "error", "message": "错误信息"}
    """
    from app.core.database import create_db_session

    # 安全验证
    text_bytes = len(request_data.text.encode('utf-8'))
    if text_bytes > HumanizeConfig().max_text_bytes:
        raise HTTPException(
            status_code=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE,
            detail=f"文本字节数超过限制"
        )

    # ✅ 预加载：在路由级别加载用户画像（用完即关闭）
    async with create_db_session() as preload_db:
        profile_service = UserProfileService(preload_db)
        profile = await profile_service.get_or_create_profile(current_user.id)
        # 默认开启验证阶段；用户画像显式关闭时才跳过
        enable_verification = profile.humanize_enabled_by_function.get("rewrite", True)
        # preload_db在此自动关闭

    async def generate():
        """流式生成器"""
        # ✅ 修复：生成器内创建独立会话，完全控制生命周期
        async with create_db_session() as db:
            humanize_service = None
            humanized_chunks = []
            final_usage = None
            detection_result = None
            verification_result = None
            start_time = time.time()

            # 记录流式请求开始
            increment_counter("humanize_stream_requests_total", labels={"intensity": request_data.intensity, "function": request_data.ai_function or "rewrite"})

            try:
                # 1. 使用预加载的画像（不再从db查询）
                # profile已在路由级别预加载

                # 2. 创建配置（使用预加载的enable_verification）
                config = HumanizeConfig(
                    enable_detection=True,
                    enable_verification=enable_verification,  # ✅ 使用预加载的值
                )

                # 3. 设置请求上下文（用于FastAI成本追踪）
                # ✅ 2025-12-02: FastAIService使用get_request_user_id()获取user_id
                set_request_context(db, str(current_user.id))

                # 4. 初始化Service
                # 2025-12-01: 传递user_id以启用成本追踪
                # 注意：流式API故意不传递db（避免生命周期问题），_track_api_cost会在内部创建独立db会话
                ai_service = HTTPAIService(user_id=str(current_user.id))
                humanize_service = HumanizeService(ai_service=ai_service, config=config)

                # 4. 检测阶段（可选）
                detection_result = None
                detection_usage = None
                if config.enable_detection:
                    yield f"data: {json.dumps({'type': 'progress', 'stage': 'detecting', 'message': '正在检测AI痕迹...'}, ensure_ascii=False)}\n\n"

                    detection_result, detection_usage = await humanize_service.detect_ai_traces(request_data.text)

                    # 检查是否需要去痕迹
                    if detection_result.overall_score < config.detection_threshold:
                        yield f"data: {json.dumps({'type': 'info', 'message': f'AI特征分数较低({detection_result.overall_score:.1f})，无需去痕迹'}, ensure_ascii=False)}\n\n"

                        detection_prompt = detection_usage.get("prompt_tokens", 0) if detection_usage else 0
                        detection_completion = detection_usage.get("completion_tokens", 0) if detection_usage else 0
                        detection_tokens = detection_usage.get("total_tokens", 0) if detection_usage else 0

                        if detection_tokens == 0:
                            detection_tokens = int(len(request_data.text) * 1.5)
                        if detection_prompt == 0 and detection_completion == 0:
                            detection_prompt = detection_tokens // 2
                            detection_completion = detection_tokens - detection_prompt

                        total_tokens = detection_tokens
                        detection_cost_result = CostCalculator.calculate_cost(
                            "gemini-2.5-flash-lite",
                            detection_prompt,
                            detection_completion
                        )
                        estimated_cost = detection_cost_result["total_cost"]

                        score_before = detection_result.overall_score
                        score_after = score_before
                        improvement = 0.0

                        dimensions_before_dict = {}
                        if detection_result and detection_result.dimensions:
                            dimensions_before_dict = {
                                key: dim.model_dump()
                                for key, dim in detection_result.dimensions.items()
                            }

                        session = HumanizeSession(
                            user_id=current_user.id,
                            ai_function=request_data.ai_function or "rewrite",
                            score_before=score_before,
                            score_after=score_after,
                            improvement=improvement,
                            intensity=request_data.intensity,
                            processing_time=time.time() - start_time,
                            tokens_used=total_tokens,
                            cost=estimated_cost,
                            user_accepted=None
                        )
                        db.add(session)
                        await db.flush()

                        detail = HumanizeSessionDetail(
                            session_id=session.id,
                            original_preview=request_data.text[:200],
                            humanized_preview=request_data.text[:200],
                            original_full=request_data.text,
                            humanized_full=request_data.text,
                            dimensions_before=dimensions_before_dict,
                            dimensions_after={},
                            detected_patterns=detection_result.detected_patterns if detection_result else [],
                            expires_at=get_utc_now() + timedelta(days=7)
                        )
                        db.add(detail)

                        try:
                            if detection_tokens > 0:
                                detection_log = AICallLog(
                                    user_id=current_user.id,
                                    model_name="gemini-2.5-flash-lite",
                                    operation_type="humanize_detect_stream",
                                    prompt_tokens=detection_prompt,
                                    completion_tokens=detection_completion,
                                    total_tokens=detection_tokens,
                                    prompt_cost=detection_cost_result["prompt_cost"],
                                    completion_cost=detection_cost_result["completion_cost"],
                                    total_cost=detection_cost_result["total_cost"],
                                    duration_ms=int((time.time() - start_time) * 1000),
                                    is_success=True,
                                    extra_data={
                                        "ai_function": request_data.ai_function or "rewrite",
                                        "intensity": request_data.intensity,
                                        "session_id": str(session.id),
                                        "stream": True,
                                        "skipped": True
                                    }
                                )
                                db.add(detection_log)
                        except Exception as log_err:
                            logger.error(f"记录检测阶段AI日志失败(跳过去痕迹): {log_err}")

                        try:
                            profile_service = UserProfileService(db)
                            await profile_service.record_humanize_use(
                                user_id=current_user.id,
                                text_length=len(request_data.text),
                                ai_function=request_data.ai_function or "rewrite",
                                intensity=request_data.intensity,
                                improvement=improvement
                            )
                        except Exception as profile_err:
                            logger.error(f"更新用户画像失败(跳过去痕迹): {profile_err}")

                        await db.commit()

                        request_duration = time.time() - start_time
                        record_timer("humanize_stream_duration_seconds", request_duration, labels={"intensity": request_data.intensity})
                        increment_counter("humanize_stream_requests_success", labels={"intensity": request_data.intensity})
                        record_timer("humanize_stream_tokens_used", total_tokens, labels={"intensity": request_data.intensity})
                        record_timer("humanize_stream_improvement", improvement, labels={"intensity": request_data.intensity})

                        yield f"data: {json.dumps({'type': 'done', 'session_id': str(session.id), 'improvement': improvement, 'processing_time': request_duration, 'tokens_used': total_tokens, 'skipped': True}, ensure_ascii=False)}\n\n"

                        return

                    yield f"data: {json.dumps({'type': 'progress', 'stage': 'detected', 'score': detection_result.overall_score}, ensure_ascii=False)}\n\n"

                # 5. 改写阶段（流式）
                yield f"data: {json.dumps({'type': 'progress', 'stage': 'rewriting', 'message': '正在人性化改写...'}, ensure_ascii=False)}\n\n"

                async for chunk, usage in humanize_service.humanize_stream(
                    text=request_data.text,
                    intensity=request_data.intensity,
                    use_nlp_preprocessing=None
                ):
                    humanized_chunks.append(chunk)
                    if usage:  # 最后一个chunk包含usage
                        final_usage = usage

                    # 发送文本片段
                    yield f"data: {json.dumps({'type': 'chunk', 'content': chunk}, ensure_ascii=False)}\n\n"

                humanized_text = "".join(humanized_chunks)

                # 6. 验证阶段（可选）
                verification_result = None
                verification_usage = None
                if config.enable_verification:
                    yield f"data: {json.dumps({'type': 'progress', 'stage': 'verifying', 'message': '正在验证效果...'}, ensure_ascii=False)}\n\n"

                    verification_result, verification_usage = await humanize_service.verify_humanization(
                        request_data.text,
                        humanized_text
                    )

                # 7. 保存会话
                processing_time = time.time() - start_time

                # 计算指标
                score_before = detection_result.overall_score if detection_result else 70.0
                score_after = verification_result.score_after if verification_result else score_before
                improvement = score_before - score_after

                # Token和成本计算（使用CostCalculator和实际token）
                # 提取各阶段的token信息
                detection_prompt = detection_usage.get("prompt_tokens", 0) if detection_usage else 0
                detection_completion = detection_usage.get("completion_tokens", 0) if detection_usage else 0
                detection_tokens = detection_usage.get("total_tokens", 0) if detection_usage else 0

                rewrite_prompt = final_usage.get("prompt_tokens", 0) if final_usage else 0
                rewrite_completion = final_usage.get("completion_tokens", 0) if final_usage else 0
                rewrite_tokens = final_usage.get("total_tokens", 0) if final_usage else 0

                verification_prompt = verification_usage.get("prompt_tokens", 0) if verification_usage else 0
                verification_completion = verification_usage.get("completion_tokens", 0) if verification_usage else 0
                verification_tokens = verification_usage.get("total_tokens", 0) if verification_usage else 0

                total_tokens = detection_tokens + rewrite_tokens + verification_tokens

                # 如果没有获取到任何实际token，使用降级估算
                if total_tokens == 0:
                    total_tokens = int(len(request_data.text) * 1.5 * 2.5)
                    # 按比例分配token
                    detection_prompt = int(total_tokens * 0.15)
                    detection_completion = int(total_tokens * 0.15)
                    rewrite_prompt = int(total_tokens * 0.3)
                    rewrite_completion = int(total_tokens * 0.3)
                    verification_prompt = int(total_tokens * 0.05)
                    verification_completion = int(total_tokens * 0.05)

                # 使用CostCalculator计算实际成本
                detection_cost_result = CostCalculator.calculate_cost(
                    "gemini-2.5-flash-lite",
                    detection_prompt,
                    detection_completion
                )
                rewrite_cost_result = CostCalculator.calculate_cost(
                    "gemini-2.5-pro",
                    rewrite_prompt,
                    rewrite_completion
                )
                verification_cost_result = CostCalculator.calculate_cost(
                    "gemini-2.5-flash-lite",
                    verification_prompt,
                    verification_completion
                )

                estimated_cost = (detection_cost_result["total_cost"] +
                                rewrite_cost_result["total_cost"] +
                                verification_cost_result["total_cost"])

                # 创建会话
                session = HumanizeSession(
                    user_id=current_user.id,
                    ai_function=request_data.ai_function or "rewrite",
                    score_before=score_before,
                    score_after=score_after,
                    improvement=improvement,
                    intensity=request_data.intensity,
                    processing_time=processing_time,
                    tokens_used=total_tokens,
                    cost=estimated_cost,
                    user_accepted=None
                )

                db.add(session)
                await db.flush()

                # 转换维度数据
                dimensions_before_dict = {}
                if detection_result and detection_result.dimensions:
                    dimensions_before_dict = {
                        key: dim.model_dump()
                        for key, dim in detection_result.dimensions.items()
                    }

                # 创建详情
                detail = HumanizeSessionDetail(
                    session_id=session.id,
                    original_preview=request_data.text[:200],
                    humanized_preview=humanized_text[:200],
                    original_full=request_data.text,
                    humanized_full=humanized_text,
                    dimensions_before=dimensions_before_dict,
                    dimensions_after={},
                    detected_patterns=(
                        (detection_result.detected_patterns if detection_result else [])
                        + ([f"NLP:{c}" for c in (humanize_service.last_nlp_changes or [])] if humanize_service.last_nlp_changes else [])
                    ),
                    expires_at=get_utc_now() + timedelta(days=7)
                )

                db.add(detail)

                # 记录AI调用日志（用于统一的成本监控和分析）
                # ✅ 使用try-except包裹，避免影响主流程
                try:
                    # 检测阶段
                    if detection_tokens > 0:
                        detection_log = AICallLog(
                            user_id=current_user.id,
                            model_name="gemini-2.5-flash-lite",
                            operation_type="humanize_detect_stream",
                            prompt_tokens=detection_prompt,
                            completion_tokens=detection_completion,
                            total_tokens=detection_tokens,
                            prompt_cost=detection_cost_result["prompt_cost"],
                            completion_cost=detection_cost_result["completion_cost"],
                            total_cost=detection_cost_result["total_cost"],
                            duration_ms=int(processing_time * 1000 * 0.3),
                            is_success=True,
                            extra_data={
                                "ai_function": request_data.ai_function or "rewrite",
                                "intensity": request_data.intensity,
                                "session_id": str(session.id),
                                "stream": True
                            }
                        )
                        db.add(detection_log)

                    # 改写阶段
                    if rewrite_tokens > 0:
                        rewrite_log = AICallLog(
                            user_id=current_user.id,
                            model_name="gemini-2.5-pro",
                            operation_type="humanize_rewrite_stream",
                            prompt_tokens=rewrite_prompt,
                            completion_tokens=rewrite_completion,
                            total_tokens=rewrite_tokens,
                            prompt_cost=rewrite_cost_result["prompt_cost"],
                            completion_cost=rewrite_cost_result["completion_cost"],
                            total_cost=rewrite_cost_result["total_cost"],
                            duration_ms=int(processing_time * 1000 * 0.6),
                            is_success=True,
                            extra_data={
                                "ai_function": request_data.ai_function or "rewrite",
                                "intensity": request_data.intensity,
                                "session_id": str(session.id),
                                "stream": True
                            }
                        )
                        db.add(rewrite_log)

                    # 验证阶段
                    if verification_tokens > 0:
                        verification_log = AICallLog(
                            user_id=current_user.id,
                            model_name="gemini-2.5-flash-lite",
                            operation_type="humanize_verify_stream",
                            prompt_tokens=verification_prompt,
                            completion_tokens=verification_completion,
                            total_tokens=verification_tokens,
                            prompt_cost=verification_cost_result["prompt_cost"],
                            completion_cost=verification_cost_result["completion_cost"],
                            total_cost=verification_cost_result["total_cost"],
                            duration_ms=int(processing_time * 1000 * 0.1),
                            is_success=True,
                            extra_data={
                                "ai_function": request_data.ai_function or "rewrite",
                                "intensity": request_data.intensity,
                                "session_id": str(session.id),
                                "stream": True
                            }
                        )
                        db.add(verification_log)

                except Exception as e:
                    logger.error(f"记录AICallLog失败（不影响主流程）: {e}")
                    # 记录失败不影响主流程，继续执行

                # ✅ 修复：在生成器的db会话中更新用户画像
                try:
                    profile_service = UserProfileService(db)  # 使用生成器的db
                    await profile_service.record_humanize_use(
                        user_id=current_user.id,
                        text_length=len(request_data.text),
                        ai_function=request_data.ai_function or "rewrite",
                        intensity=request_data.intensity,
                        improvement=improvement
                    )
                except Exception as e:
                    logger.error(f"更新用户画像失败: {e}")

                # ✅ 修复：在生成器的独立会话中commit（安全）
                await db.commit()

                # 记录监控指标
                request_duration = time.time() - start_time
                record_timer("humanize_stream_duration_seconds", request_duration, labels={"intensity": request_data.intensity})
                increment_counter("humanize_stream_requests_success", labels={"intensity": request_data.intensity})
                record_timer("humanize_stream_tokens_used", total_tokens, labels={"intensity": request_data.intensity})
                record_timer("humanize_stream_improvement", improvement, labels={"intensity": request_data.intensity})

                # 8. 发送完成事件
                yield f"data: {json.dumps({'type': 'done', 'session_id': str(session.id), 'improvement': improvement, 'processing_time': processing_time, 'tokens_used': total_tokens}, ensure_ascii=False)}\n\n"

                logger.info(f"流式去痕迹完成: session_id={session.id}, improvement={improvement:.1f}, duration={request_duration:.2f}s")

            except GeneratorExit:
                # 用户中断连接
                interrupted_time = time.time() - start_time
                logger.warning(f"用户中断流式响应: 已处理{interrupted_time:.2f}秒, chunks={len(humanized_chunks)}")
                increment_counter("humanize_stream_requests_interrupted", labels={"intensity": request_data.intensity})

                # 保存中断会话记录（用于分析用户行为）
                try:
                    # 计算已收集的数据
                    partial_text = "".join(humanized_chunks) if humanized_chunks else ""
                    estimated_tokens = final_usage.get("total_tokens", 0) if final_usage else int(len(request_data.text) * 1.5)

                    # 使用CostCalculator估算中断时的成本
                    # 假设只完成了rewrite阶段（因为中断了）
                    estimated_prompt = estimated_tokens // 2
                    estimated_completion = estimated_tokens // 2
                    cost_result = CostCalculator.calculate_cost(
                        "gemini-2.5-pro",  # 假设使用pro模型进行改写
                        estimated_prompt,
                        estimated_completion
                    )
                    estimated_cost = cost_result["total_cost"]

                    # 创建中断会话记录
                    session = HumanizeSession(
                        user_id=current_user.id,
                        ai_function=request_data.ai_function or "rewrite",
                        score_before=detection_result.overall_score if detection_result else 70.0,
                        score_after=70.0,  # 未完成，使用默认值
                        improvement=0.0,  # 未完成
                        intensity=request_data.intensity,
                        processing_time=interrupted_time,
                        tokens_used=estimated_tokens,
                        cost=estimated_cost,  # 使用CostCalculator计算的成本
                        user_accepted=False  # 中断视为拒绝
                    )
                    db.add(session)
                    await db.flush()

                    # 创建详情（标记为中断）
                    detail = HumanizeSessionDetail(
                        session_id=session.id,
                        original_preview=request_data.text[:200],
                        humanized_preview=partial_text[:200] if partial_text else "(用户中断，无输出)",
                        original_full=request_data.text,
                        humanized_full=partial_text,
                        dimensions_before={},
                        dimensions_after={},
                        detected_patterns=["USER_INTERRUPTED"],
                        expires_at=get_utc_now() + timedelta(days=7)
                    )
                    db.add(detail)
                    await db.commit()

                    logger.info(f"已保存中断会话: session_id={session.id}, chunks={len(humanized_chunks)}")

                except Exception as save_err:
                    logger.error(f"保存中断会话失败: {save_err}")
                    # 中断处理失败不影响主流程

                # 注意：这里无法继续yield，连接已断开

            except Exception as e:
                logger.error(f"流式去痕迹失败: {type(e).__name__}: {e}", exc_info=True)

                # 记录失败指标
                increment_counter("humanize_stream_requests_failed", labels={"intensity": request_data.intensity, "error": type(e).__name__})

                try:
                    await db.rollback()
                    yield f"data: {json.dumps({'type': 'error', 'message': str(e)}, ensure_ascii=False)}\n\n"
                except:
                    pass  # 如果连接已断开，忽略错误

            finally:
                # 确保关闭Service
                if humanize_service:
                    try:
                        await humanize_service.close()
                    except Exception as e:
                        logger.error(f"关闭Service失败: {e}")

    return StreamingResponse(
        generate(),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "X-Accel-Buffering": "no",  # 禁用nginx缓冲
        }
    )
