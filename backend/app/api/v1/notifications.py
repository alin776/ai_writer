from fastapi import APIRouter, Depends, HTTPException, status, Query, File, UploadFile
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List, Optional
from uuid import UUID

from app.core.database import get_db
from app.core.security import get_current_active_user, get_current_admin_user
from app.core.config import settings
from app.services.cos_service import CosService
from app.models.user import User
from app.models.notification import NotificationCategory, NotificationType, NotificationStatus
from app.schemas.notification import (
    NotificationCreate,
    NotificationUpdate,
    NotificationResponse,
    NotificationListResponse,
    UserNotificationListResponse,
    UnreadCountResponse,
    MarkReadRequest,
    DismissNotificationRequest,
    ClickActionRequest,
    NotificationStatsResponse,
    BatchOperationResponse,
)
from app.services.notification_service import NotificationService

router = APIRouter()


# ==================== 用户端API ====================

@router.get("/user/notifications", response_model=UserNotificationListResponse)
async def get_my_notifications(
    page: int = Query(1, ge=1, description="页码"),
    page_size: int = Query(20, ge=1, le=100, description="每页数量"),
    is_read: Optional[bool] = Query(None, description="筛选已读/未读"),
    display_type: Optional[str] = Query(None, description="展示类型筛选(modal/banner/notification)"),
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db)
):
    """
    获取当前用户的通知列表

    - 支持分页
    - 支持筛选已读/未读
    - 支持筛选展示类型
    """
    notification_service = NotificationService(db)

    skip = (page - 1) * page_size
    notifications, total, unread_count = await notification_service.get_user_notifications(
        user_id=current_user.id,
        skip=skip,
        limit=page_size,
        is_read=is_read,
        display_type=display_type
    )

    return {
        "total": total,
        "unread_count": unread_count,
        "page": page,
        "page_size": page_size,
        "items": notifications
    }


@router.get("/user/notifications/unread-count", response_model=UnreadCountResponse)
async def get_unread_count(
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db)
):
    """获取当前用户的未读通知数量"""
    notification_service = NotificationService(db)
    unread_count = await notification_service.get_unread_count(current_user.id)

    return {"unread_count": unread_count}


@router.post("/user/notifications/mark-read", response_model=BatchOperationResponse)
async def mark_notifications_as_read(
    request: MarkReadRequest,
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db)
):
    """
    标记通知为已读

    - 如果 notification_ids 为空，则标记全部未读为已读
    - 如果提供 notification_ids，则只标记指定的通知
    """
    notification_service = NotificationService(db)

    affected_count = await notification_service.mark_as_read(
        user_id=current_user.id,
        notification_ids=request.notification_ids
    )

    return {
        "success": True,
        "message": "Notifications marked as read",
        "affected_count": affected_count
    }


@router.post("/user/notifications/{notification_id}/dismiss", response_model=BatchOperationResponse)
async def dismiss_notification(
    notification_id: UUID,
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db)
):
    """关闭通知弹窗（用户点击关闭按钮时调用）"""
    notification_service = NotificationService(db)

    success = await notification_service.dismiss_notification(
        user_id=current_user.id,
        notification_id=notification_id
    )

    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Notification not found"
        )

    return {
        "success": True,
        "message": "Notification dismissed",
        "affected_count": 1
    }


@router.post("/user/notifications/{notification_id}/click", response_model=BatchOperationResponse)
async def click_action_button(
    notification_id: UUID,
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db)
):
    """记录用户点击了通知的行动按钮"""
    notification_service = NotificationService(db)

    success = await notification_service.click_action_button(
        user_id=current_user.id,
        notification_id=notification_id
    )

    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Notification not found"
        )

    return {
        "success": True,
        "message": "Action button clicked",
        "affected_count": 1
    }


# ==================== 管理员API ====================

@router.post("/admin/notifications", response_model=NotificationResponse, status_code=status.HTTP_201_CREATED)
async def create_notification(
    notification_data: NotificationCreate,
    current_user: User = Depends(get_current_admin_user),
    db: AsyncSession = Depends(get_db)
):
    """
    创建通知/活动（管理员）

    - 支持立即发布、定时发布、保存草稿
    - 支持多种展示方式（弹窗、横幅、通知列表）
    - 支持目标用户筛选
    """
    notification_service = NotificationService(db)

    try:
        notification = await notification_service.create_notification(
            notification_data=notification_data,
            created_by=current_user.id
        )
        return notification
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


@router.get("/admin/notifications", response_model=NotificationListResponse)
async def get_notifications(
    page: int = Query(1, ge=1, description="页码"),
    page_size: int = Query(20, ge=1, le=100, description="每页数量"),
    category: Optional[NotificationCategory] = Query(None, description="通知分类"),
    status: Optional[NotificationStatus] = Query(None, description="通知状态"),
    type: Optional[NotificationType] = Query(None, description="通知类型"),
    current_user: User = Depends(get_current_admin_user),
    db: AsyncSession = Depends(get_db)
):
    """
    获取通知列表（管理员）

    - 支持分页
    - 支持按分类、状态、类型筛选
    """
    notification_service = NotificationService(db)

    skip = (page - 1) * page_size
    notifications, total = await notification_service.get_notifications(
        skip=skip,
        limit=page_size,
        category=category,
        status=status,
        type=type
    )

    return {
        "total": total,
        "page": page,
        "page_size": page_size,
        "items": notifications
    }


@router.get("/admin/notifications/{notification_id}", response_model=NotificationResponse)
async def get_notification(
    notification_id: UUID,
    current_user: User = Depends(get_current_admin_user),
    db: AsyncSession = Depends(get_db)
):
    """获取单个通知详情（管理员）"""
    notification_service = NotificationService(db)

    notification = await notification_service.get_notification(notification_id)
    if not notification:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Notification not found"
        )

    return notification


@router.put("/admin/notifications/{notification_id}", response_model=NotificationResponse)
async def update_notification(
    notification_id: UUID,
    notification_data: NotificationUpdate,
    current_user: User = Depends(get_current_admin_user),
    db: AsyncSession = Depends(get_db)
):
    """更新通知（管理员）"""
    notification_service = NotificationService(db)

    notification = await notification_service.update_notification(
        notification_id=notification_id,
        notification_data=notification_data
    )

    if not notification:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Notification not found"
        )

    return notification


@router.delete("/admin/notifications/{notification_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_notification(
    notification_id: UUID,
    current_user: User = Depends(get_current_admin_user),
    db: AsyncSession = Depends(get_db)
):
    """删除通知（管理员）"""
    notification_service = NotificationService(db)

    success = await notification_service.delete_notification(notification_id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Notification not found"
        )


@router.post("/admin/notifications/{notification_id}/publish", response_model=NotificationResponse)
async def publish_notification(
    notification_id: UUID,
    current_user: User = Depends(get_current_admin_user),
    db: AsyncSession = Depends(get_db)
):
    """
    发布通知（管理员）

    - 将草稿或定时通知设为激活状态
    - 立即创建用户通知关系
    """
    notification_service = NotificationService(db)

    notification = await notification_service.publish_notification(notification_id)
    if not notification:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Notification not found"
        )

    return notification


@router.get("/admin/notifications/{notification_id}/stats", response_model=NotificationStatsResponse)
async def get_notification_stats(
    notification_id: UUID,
    current_user: User = Depends(get_current_admin_user),
    db: AsyncSession = Depends(get_db)
):
    """
    获取通知统计数据（管理员）

    - 总触达用户数
    - 已读用户数、已读率
    - 点击用户数、点击率
    """
    notification_service = NotificationService(db)

    stats = await notification_service.get_notification_stats(notification_id)
    if not stats:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Notification not found"
        )

    return stats


@router.post("/admin/notifications/upload-cover")
async def upload_notification_cover(
    file: UploadFile = File(...),
    current_user: User = Depends(get_current_admin_user),
    db: AsyncSession = Depends(get_db)
):
    """上传通知封面图片（管理员）"""
    # 验证文件类型
    allowed_types = {"image/jpeg", "image/png", "image/webp", "image/gif"}
    if file.content_type not in allowed_types:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="仅支持 JPG/PNG/WebP/GIF 图片文件"
        )

    # 读取文件内容
    content = await file.read()

    # 验证文件大小 (10MB限制)
    max_size = settings.MAX_UPLOAD_SIZE or 10485760
    if len(content) > max_size:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="文件过大，请选择 10MB 以下的图片"
        )

    # 上传到腾讯云COS
    cos_service = CosService()
    try:
        cover_url = await cos_service.upload_notification_cover(
            filename=file.filename,
            content=content,
            content_type=file.content_type
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"图片上传失败: {str(e)}"
        )

    return {"coverUrl": cover_url}
