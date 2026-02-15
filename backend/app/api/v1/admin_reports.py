"""
管理员举报处理 API

提供消息举报、评论举报、小说举报、用户举报的管理功能
"""
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func, update
from sqlalchemy.orm import joinedload
from datetime import datetime
from typing import Optional
from uuid import UUID

from app.core.database import get_db
from app.core.security import get_current_active_user
from app.models.user import User
from app.models.work import Work
from app.models.comment import Comment, CommentReport
from app.models.message_report import MessageReport
from app.models.channel_message import ChannelMessage
from app.models.work_report import WorkReport, WorkReportStatus
from app.models.user_report import UserReport, UserReportStatus
from app.models.notification import (
    Notification,
    UserNotification,
    NotificationCategory,
    NotificationType,
    NotificationPriority,
    NotificationStatus,
    TargetUserType,
)
from app.schemas.work_report import (
    MessageReportAdminResponse,
    CommentReportAdminResponse,
    WorkReportAdminResponse,
    UserReportAdminResponse,
    ReportProcessRequest,
    ReportSummary,
)
from app.utils.datetime_utils import get_utc_now
from datetime import datetime, timezone


async def send_warning_notification(
    db: AsyncSession,
    user_id: UUID,
    title: str,
    content: str
):
    """发送警告通知给用户（仅在通知列表显示）"""
    notification = Notification(
        title=title,
        content=content,
        category=NotificationCategory.SYSTEM,
        type=NotificationType.WARNING,
        priority=NotificationPriority.IMPORTANT,  # 使用 IMPORTANT 优先级
        display_type=["notification"],  # 仅在通知列表显示
        target_users=TargetUserType.CUSTOM,
        custom_user_ids=[user_id],
        status=NotificationStatus.ACTIVE,
        published_at=get_utc_now(),
        allow_dismiss=True,
        show_once=False
    )
    db.add(notification)
    await db.flush()

    # 创建用户通知关联
    user_notification = UserNotification(
        user_id=user_id,
        notification_id=notification.id,
        is_read=False,
        is_dismissed=False,
        clicked=False
    )
    db.add(user_notification)

router = APIRouter()


def check_admin_permission(current_user: User = Depends(get_current_active_user)) -> User:
    """检查是否为管理员"""
    if not current_user.is_admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Admin permission required"
        )
    return current_user


@router.get("/summary", response_model=ReportSummary)
async def get_reports_summary(
    current_user: User = Depends(check_admin_permission),
    db: AsyncSession = Depends(get_db)
):
    """
    获取举报统计概览
    """
    # 使用不带时区的 datetime（兼容 message_reports 表）
    today_start_naive = datetime.utcnow().replace(hour=0, minute=0, second=0, microsecond=0)
    today_start_tz = get_utc_now().replace(hour=0, minute=0, second=0, microsecond=0)

    # 消息举报统计（使用不带时区的 datetime）
    message_total = await db.scalar(select(func.count(MessageReport.id))) or 0
    message_pending = await db.scalar(
        select(func.count(MessageReport.id)).where(MessageReport.status == "pending")
    ) or 0
    message_today = await db.scalar(
        select(func.count(MessageReport.id)).where(MessageReport.reviewed_at >= today_start_naive)
    ) or 0

    # 评论举报统计（使用带时区的 datetime）
    comment_total = await db.scalar(select(func.count(CommentReport.id))) or 0
    comment_pending = await db.scalar(
        select(func.count(CommentReport.id)).where(CommentReport.is_processed == False)
    ) or 0
    comment_today = await db.scalar(
        select(func.count(CommentReport.id)).where(CommentReport.processed_at >= today_start_tz)
    ) or 0

    # 小说举报统计（使用带时区的 datetime）
    work_total = await db.scalar(select(func.count(WorkReport.id))) or 0
    work_pending = await db.scalar(
        select(func.count(WorkReport.id)).where(WorkReport.status == "pending")
    ) or 0
    work_today = await db.scalar(
        select(func.count(WorkReport.id)).where(WorkReport.reviewed_at >= today_start_tz)
    ) or 0

    # 用户举报统计（使用带时区的 datetime）
    user_total = await db.scalar(select(func.count(UserReport.id))) or 0
    user_pending = await db.scalar(
        select(func.count(UserReport.id)).where(UserReport.status == "pending")
    ) or 0
    user_today = await db.scalar(
        select(func.count(UserReport.id)).where(UserReport.reviewed_at >= today_start_tz)
    ) or 0

    return ReportSummary(
        message_reports={"total": message_total, "pending": message_pending, "processed_today": message_today},
        comment_reports={"total": comment_total, "pending": comment_pending, "processed_today": comment_today},
        work_reports={"total": work_total, "pending": work_pending, "processed_today": work_today},
        user_reports={"total": user_total, "pending": user_pending, "processed_today": user_today},
    )


@router.get("/messages", response_model=list[MessageReportAdminResponse])
async def get_message_reports(
    status: Optional[str] = Query(None, description="筛选状态: pending, reviewed, dismissed, actioned"),
    skip: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=100),
    current_user: User = Depends(check_admin_permission),
    db: AsyncSession = Depends(get_db)
):
    """
    获取消息举报列表
    """
    query = select(MessageReport).options(
        joinedload(MessageReport.message).joinedload(ChannelMessage.channel),
        joinedload(MessageReport.message).joinedload(ChannelMessage.user),
        joinedload(MessageReport.reporter),
    ).order_by(MessageReport.created_at.desc())

    if status:
        query = query.where(MessageReport.status == status)

    query = query.offset(skip).limit(limit)
    result = await db.execute(query)
    reports = result.unique().scalars().all()

    response_list = []
    for report in reports:
        response_list.append(MessageReportAdminResponse(
            id=report.id,
            message_id=report.message_id,
            reporter_id=report.reporter_id,
            reason=report.reason,
            description=report.description,
            status=report.status,
            created_at=report.created_at,
            reviewed_at=report.reviewed_at,
            reviewed_by=report.reviewed_by,
            message_content=report.message.content if report.message else None,
            channel_name=report.message.channel.name if report.message and report.message.channel else None,
            reporter_name=report.reporter.full_name or report.reporter.username if report.reporter else None,
            reported_user_name=report.message.user.full_name or report.message.user.username if report.message and report.message.user else None,
        ))

    return response_list


@router.get("/comments", response_model=list[CommentReportAdminResponse])
async def get_comment_reports(
    is_processed: Optional[bool] = Query(None, description="是否已处理"),
    skip: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=100),
    current_user: User = Depends(check_admin_permission),
    db: AsyncSession = Depends(get_db)
):
    """
    获取评论举报列表
    """
    query = select(CommentReport).options(
        joinedload(CommentReport.comment).joinedload(Comment.work),
        joinedload(CommentReport.comment).joinedload(Comment.user),
        joinedload(CommentReport.user),
    ).order_by(CommentReport.created_at.desc())

    if is_processed is not None:
        query = query.where(CommentReport.is_processed == is_processed)

    query = query.offset(skip).limit(limit)
    result = await db.execute(query)
    reports = result.unique().scalars().all()

    response_list = []
    for report in reports:
        response_list.append(CommentReportAdminResponse(
            id=report.id,
            comment_id=report.comment_id,
            user_id=report.user_id,
            reason=report.reason.value if hasattr(report.reason, 'value') else report.reason,
            description=report.description,
            is_processed=report.is_processed,
            processed_at=report.processed_at,
            processed_by=report.processed_by,
            created_at=report.created_at,
            comment_content=report.comment.content if report.comment else None,
            work_title=report.comment.work.title if report.comment and report.comment.work else None,
            reporter_name=report.user.full_name or report.user.username if report.user else None,
            commented_user_name=report.comment.user.full_name or report.comment.user.username if report.comment and report.comment.user else None,
        ))

    return response_list


@router.get("/works", response_model=list[WorkReportAdminResponse])
async def get_work_reports(
    status: Optional[str] = Query(None, description="筛选状态: pending, reviewed, dismissed, actioned"),
    skip: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=100),
    current_user: User = Depends(check_admin_permission),
    db: AsyncSession = Depends(get_db)
):
    """
    获取小说举报列表
    """
    query = select(WorkReport).options(
        joinedload(WorkReport.work).joinedload(Work.author),
        joinedload(WorkReport.reporter),
    ).order_by(WorkReport.created_at.desc())

    if status:
        query = query.where(WorkReport.status == status)

    query = query.offset(skip).limit(limit)
    result = await db.execute(query)
    reports = result.unique().scalars().all()

    response_list = []
    for report in reports:
        response_list.append(WorkReportAdminResponse(
            id=report.id,
            work_id=report.work_id,
            reporter_id=report.reporter_id,
            reason=report.reason,
            description=report.description,
            status=report.status,
            action_taken=report.action_taken,
            admin_note=report.admin_note,
            reviewed_at=report.reviewed_at,
            reviewed_by=report.reviewed_by,
            created_at=report.created_at,
            work_title=report.work.title if report.work else None,
            work_author_name=report.work.author.full_name or report.work.author.username if report.work and report.work.author else None,
            reporter_name=report.reporter.full_name or report.reporter.username if report.reporter else None,
        ))

    return response_list


@router.patch("/messages/{report_id}")
async def process_message_report(
    report_id: UUID,
    request: ReportProcessRequest,
    current_user: User = Depends(check_admin_permission),
    db: AsyncSession = Depends(get_db)
):
    """
    处理消息举报

    action 可选值:
    - dismiss: 驳回举报
    - delete: 删除消息
    - warn: 警告用户
    - ban: 禁言用户
    """
    report = await db.get(MessageReport, report_id)
    if not report:
        raise HTTPException(status_code=404, detail="Report not found")

    # 举报原因中文映射
    reason_map = {
        'spam': '垃圾广告',
        'abuse': '辱骂攻击',
        'porn': '色情低俗',
        'illegal': '违法违规',
        'plagiarism': '抄袭侵权',
        'false': '虚假信息',
        'other': '其他',
    }
    reason_text = reason_map.get(report.reason, report.reason)

    # 获取消息内容
    message = await db.get(ChannelMessage, report.message_id)
    message_preview = ""
    if message:
        # 截取消息前50个字符作为预览
        content = message.content or ""
        message_preview = content[:50] + ("..." if len(content) > 50 else "")

    # 根据 action 执行不同操作
    if request.action == "dismiss":
        report.status = "dismissed"
    elif request.action == "delete":
        # 删除消息
        if message:
            message.is_deleted = True
        report.status = "actioned"
    elif request.action == "warn":
        # 警告用户并删除消息
        if message:
            message.is_deleted = True  # 警告时也删除违规消息
            if message.user_id:
                await send_warning_notification(
                    db=db,
                    user_id=message.user_id,
                    title="⚠️ 内容违规警告",
                    content=f"您在频道中发送的消息因违规已被删除并收到警告。\n\n违规消息：「{message_preview}」\n违规原因：{reason_text}\n\n请遵守社区规范，避免发布违规内容。如有疑问，请联系管理员。"
                )
        report.status = "actioned"
    elif request.action == "ban":
        # 禁言用户并删除消息
        if message:
            message.is_deleted = True  # 禁言时也删除违规消息
            if message.user_id:
                await send_warning_notification(
                    db=db,
                    user_id=message.user_id,
                    title="🚫 账号已被禁言",
                    content=f"因多次违规，您的账号已被禁言。\n\n违规消息：「{message_preview}」\n违规原因：{reason_text}\n\n如有疑问，请联系管理员。"
                )
        report.status = "actioned"
    else:
        report.status = "reviewed"

    report.reviewed_at = datetime.utcnow()  # message_reports 使用不带时区的 datetime
    report.reviewed_by = current_user.id

    await db.commit()

    return {"message": f"Report processed with action: {request.action}"}


@router.patch("/comments/{report_id}")
async def process_comment_report(
    report_id: UUID,
    request: ReportProcessRequest,
    current_user: User = Depends(check_admin_permission),
    db: AsyncSession = Depends(get_db)
):
    """
    处理评论举报

    action 可选值:
    - dismiss: 驳回举报
    - delete: 删除评论
    - warn: 警告用户
    - ban: 封禁用户
    """
    report = await db.get(CommentReport, report_id)
    if not report:
        raise HTTPException(status_code=404, detail="Report not found")

    # 举报原因中文映射
    reason_map = {
        'spam': '垃圾信息',
        'abuse': '辱骂内容',
        'porn': '色情内容',
        'illegal': '违法内容',
        'false': '虚假信息',
        'other': '其他',
    }
    # 获取原因的值（可能是枚举或字符串）
    reason_value = report.reason.value if hasattr(report.reason, 'value') else str(report.reason)
    reason_text = reason_map.get(reason_value, reason_value)

    # 根据 action 执行不同操作
    if request.action == "dismiss":
        pass  # 仅标记已处理
    elif request.action == "delete":
        # 软删除评论
        comment = await db.get(Comment, report.comment_id)
        if comment:
            comment.is_deleted = True
    elif request.action == "warn":
        # 发送警告通知给评论者
        comment = await db.get(Comment, report.comment_id)
        if comment and comment.user_id:
            await send_warning_notification(
                db=db,
                user_id=comment.user_id,
                title="⚠️ 评论违规警告",
                content=f"您的评论因被举报已收到警告。请遵守社区规范，文明评论。如有疑问，请联系管理员。\n\n违规原因：{reason_text}"
            )
    elif request.action == "ban":
        # 封禁评论者
        comment = await db.get(Comment, report.comment_id)
        if comment and comment.user_id:
            user = await db.get(User, comment.user_id)
            if user:
                user.is_active = False
            # 发送封禁通知
            await send_warning_notification(
                db=db,
                user_id=comment.user_id,
                title="🚫 账号已被封禁",
                content=f"因多次违规，您的账号已被封禁。如有疑问，请联系管理员。\n\n违规原因：{reason_text}"
            )

    report.is_processed = True
    report.processed_at = get_utc_now()
    report.processed_by = current_user.id

    await db.commit()

    return {"message": f"Report processed with action: {request.action}"}


@router.patch("/works/{report_id}")
async def process_work_report(
    report_id: UUID,
    request: ReportProcessRequest,
    current_user: User = Depends(check_admin_permission),
    db: AsyncSession = Depends(get_db)
):
    """
    处理小说举报

    action 可选值:
    - dismiss: 驳回举报
    - delete: 下架小说
    - warn: 警告作者
    - ban: 封禁作者
    """
    report = await db.get(WorkReport, report_id)
    if not report:
        raise HTTPException(status_code=404, detail="Report not found")

    # 举报原因中文映射
    reason_map = {
        'spam': '垃圾广告',
        'porn': '色情低俗',
        'illegal': '违法违规',
        'plagiarism': '抄袭侵权',
        'false': '虚假信息',
        'other': '其他',
    }
    # 获取原因的值（可能是枚举或字符串）
    reason_value = report.reason.value if hasattr(report.reason, 'value') else str(report.reason)
    reason_text = reason_map.get(reason_value, reason_value)

    # 根据 action 执行不同操作
    if request.action == "dismiss":
        report.status = "dismissed"
    elif request.action == "delete":
        # 下架小说（设置为非公开）
        work = await db.get(Work, report.work_id)
        if work:
            work.is_published = False
        report.status = "actioned"
        report.action_taken = "unpublished"
    elif request.action == "warn":
        # 发送警告通知给作者
        work = await db.get(Work, report.work_id)
        if work and work.author_id:
            await send_warning_notification(
                db=db,
                user_id=work.author_id,
                title="⚠️ 作品违规警告",
                content=f"您的作品《{work.title}》因被举报已收到警告。请检查作品内容，确保符合社区规范。如有疑问，请联系管理员。\n\n违规原因：{reason_text}"
            )
        report.status = "actioned"
        report.action_taken = "warned"
    elif request.action == "ban":
        # 封禁作者
        work = await db.get(Work, report.work_id)
        if work:
            author = await db.get(User, work.author_id)
            if author:
                author.is_active = False
                # 发送封禁通知
                await send_warning_notification(
                    db=db,
                    user_id=work.author_id,
                    title="🚫 账号已被封禁",
                    content=f"因您的作品《{work.title}》严重违规，您的账号已被封禁。如有疑问，请联系管理员。\n\n违规原因：{reason_text}"
                )
        report.status = "actioned"
        report.action_taken = "banned"
    else:
        report.status = "reviewed"

    report.admin_note = request.admin_note
    report.reviewed_at = get_utc_now()
    report.reviewed_by = current_user.id

    await db.commit()

    return {"message": f"Report processed with action: {request.action}"}


# ==================== 用户举报管理 ====================

@router.get("/users", response_model=list[UserReportAdminResponse])
async def get_user_reports(
    report_status: Optional[str] = Query(None, alias="status", description="筛选状态: pending, reviewed, dismissed, actioned"),
    skip: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=100),
    current_user: User = Depends(check_admin_permission),
    db: AsyncSession = Depends(get_db)
):
    """
    获取用户举报列表
    """
    query = select(UserReport).options(
        joinedload(UserReport.reporter),
        joinedload(UserReport.reported_user),
    ).order_by(UserReport.created_at.desc())

    if report_status:
        query = query.where(UserReport.status == report_status)

    query = query.offset(skip).limit(limit)
    result = await db.execute(query)
    reports = result.unique().scalars().all()

    response_list = []
    for report in reports:
        response_list.append(UserReportAdminResponse(
            id=report.id,
            reporter_id=report.reporter_id,
            reported_user_id=report.reported_user_id,
            reason=report.reason.value if hasattr(report.reason, 'value') else str(report.reason),
            description=report.description,
            status=report.status.value if hasattr(report.status, 'value') else str(report.status),
            admin_note=report.admin_note,
            reviewed_at=report.reviewed_at,
            reviewed_by=report.reviewed_by,
            created_at=report.created_at,
            reporter_name=report.reporter.full_name or report.reporter.username if report.reporter else None,
            reported_user_name=report.reported_user.full_name or report.reported_user.username if report.reported_user else None,
            reported_user_avatar=report.reported_user.avatar if report.reported_user else None,
        ))

    return response_list


@router.patch("/users/{report_id}")
async def process_user_report(
    report_id: UUID,
    request: ReportProcessRequest,
    current_user: User = Depends(check_admin_permission),
    db: AsyncSession = Depends(get_db)
):
    """
    处理用户举报

    action 可选值:
    - dismiss: 驳回举报
    - warn: 警告用户
    - ban: 封禁用户
    """
    report = await db.get(UserReport, report_id)
    if not report:
        raise HTTPException(status_code=404, detail="Report not found")

    # 获取被举报用户
    reported_user = await db.get(User, report.reported_user_id)

    # 举报原因中文映射
    reason_map = {
        'spam': '垃圾信息',
        'harassment': '骚扰行为',
        'inappropriate': '不当内容',
        'impersonation': '冒充他人',
        'other': '其他',
    }
    reason_value = report.reason.value if hasattr(report.reason, 'value') else str(report.reason)
    reason_text = reason_map.get(reason_value, reason_value)

    # 根据 action 执行不同操作
    if request.action == "dismiss":
        report.status = UserReportStatus.dismissed
    elif request.action == "warn":
        # 发送警告通知给被举报用户
        if reported_user:
            await send_warning_notification(
                db=db,
                user_id=reported_user.id,
                title="⚠️ 账号违规警告",
                content=f"您的账号因被举报已收到警告。请遵守社区规范，避免不当行为。如有疑问，请联系管理员。\n\n违规原因：{reason_text}"
            )
        report.status = UserReportStatus.actioned
    elif request.action == "ban":
        # 封禁被举报用户
        if reported_user:
            reported_user.is_active = False
            # 发送封禁通知
            await send_warning_notification(
                db=db,
                user_id=reported_user.id,
                title="🚫 账号已被封禁",
                content=f"因多次违规，您的账号已被封禁。如有疑问，请联系管理员。\n\n违规原因：{reason_text}"
            )
        report.status = UserReportStatus.actioned
    else:
        report.status = UserReportStatus.reviewed

    report.admin_note = request.admin_note
    report.reviewed_at = get_utc_now()
    report.reviewed_by = current_user.id

    await db.commit()

    return {"message": f"User report processed with action: {request.action}"}
