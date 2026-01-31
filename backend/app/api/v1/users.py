from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File, Query
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, or_, func
from typing import List
from uuid import UUID

from app.core.database import get_db
from app.core.security import get_current_active_user, oauth2_scheme
from app.models.user import User
from app.models.work import Work
from app.models.friendship import Friendship
from app.models.friend_request import FriendRequest
from app.models.user_report import UserReport, UserReportReason, UserReportStatus
from app.schemas.user import (
    UserProfileStats,
    UserRelation,
    WorkBrief,
    UserProfileResponse,
    UserResponse,
    UserUpdate,
    NotificationSettings,
    Preferences,
    ChangePasswordRequest,
    ChangePasswordResponse,
    DeleteAccountRequest,
    DeleteAccountResponse,
    AvatarUploadResponse,
    UserSessionResponse,
    SendEmailCodeRequest,
    SendEmailCodeResponse,
    VerifyAndUpdateEmailRequest,
    VerifyAndUpdateEmailResponse,
    UpdateOnlineStatusRequest,
)
from app.schemas.friend import UserSearchResponse, UserSearchResult
from app.services.user_service import UserService
from app.services.cos_service import get_cos_service
from app.services.email_verification_service import get_email_verification_service
from app.services.task_service import TaskService
from app.api.v1.ws import update_user_online_status
from app.core.config import settings

router = APIRouter()


@router.get("/me", response_model=UserResponse)
async def get_current_user_info(
    current_user: User = Depends(get_current_active_user)
):
    """获取当前用户信息"""
    return current_user


@router.put("/me", response_model=UserResponse)
async def update_current_user(
    user_data: UserUpdate,
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db)
):
    """更新当前用户信息"""
    user_service = UserService(db)

    try:
        # 检查是否修改了用户名
        username_changed = user_data.username and user_data.username != current_user.username

        user = await user_service.update_user(str(current_user.id), user_data)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found"
            )

        # 如果修改了用户名，触发任务检查（失败不影响用户名更新）
        if username_changed:
            print(f"[Username Update] About to check username task for user {current_user.id}")
            try:
                await TaskService.check_username_task(db, current_user.id)
                print(f"[Username Update] Username task check completed")
            except Exception as task_error:
                print(f"[Username Update] Task check failed (non-critical): {task_error}")
                import traceback
                traceback.print_exc()

        await db.commit()
        print(f"[Username Update] Transaction committed")
        return user
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


@router.get("/me/notification-settings", response_model=NotificationSettings)
async def get_my_notification_settings(
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db)
):
    """获取当前用户的通知设置"""
    user_service = UserService(db)
    try:
        return await user_service.get_notification_settings(str(current_user.id))
    except ValueError:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")


@router.put("/me/notification-settings", response_model=NotificationSettings)
async def update_my_notification_settings(
    settings: NotificationSettings,
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db)
):
    """更新当前用户的通知设置"""
    user_service = UserService(db)
    try:
        result = await user_service.update_notification_settings(str(current_user.id), settings)
        await db.commit()
        return result
    except ValueError:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")


@router.get("/me/preferences", response_model=Preferences)
async def get_my_preferences(
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db)
):
    """获取当前用户的偏好设置"""
    user_service = UserService(db)
    try:
        return await user_service.get_preferences(str(current_user.id))
    except ValueError:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")


@router.put("/me/preferences", response_model=Preferences)
async def update_my_preferences(
    preferences: Preferences,
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db)
):
    """更新当前用户的偏好设置"""
    user_service = UserService(db)
    try:
        result = await user_service.update_preferences(str(current_user.id), preferences)
        await db.commit()
        return result
    except ValueError:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")


@router.put("/me/status", response_model=UserResponse)
async def update_online_status(
    payload: UpdateOnlineStatusRequest,
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db)
):
    """更新用户在线状态"""
    current_user.online_status = payload.status
    await db.commit()
    await db.refresh(current_user)

    # 更新 WebSocket 内存状态并广播到所有相关频道
    await update_user_online_status(current_user.id, payload.status)

    return current_user


@router.post("/me/change-password", response_model=ChangePasswordResponse)
async def change_my_password(
    payload: ChangePasswordRequest,
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db)
):
    """修改当前用户密码"""
    user_service = UserService(db)
    try:
        await user_service.change_password(
            str(current_user.id),
            payload.current_password,
            payload.new_password
        )
        await db.commit()
        return ChangePasswordResponse(detail="密码修改成功")
    except ValueError as exc:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(exc)
        )


# ==================== 修改邮箱 ====================

@router.post("/me/send-email-code", response_model=SendEmailCodeResponse)
async def send_email_verification_code(
    payload: SendEmailCodeRequest,
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db)
):
    """发送邮箱验证码"""
    user_service = UserService(db)

    # 检查新邮箱是否已被使用
    existing = await user_service.get_user_by_email(payload.new_email)
    if existing and str(existing.id) != str(current_user.id):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="该邮箱已被其他用户使用"
        )

    # 检查是否与当前邮箱相同
    if current_user.email == payload.new_email:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="新邮箱不能与当前邮箱相同"
        )

    try:
        email_service = await get_email_verification_service()
        await email_service.send_verification_code(payload.new_email)
        return SendEmailCodeResponse(detail="验证码已发送到新邮箱")
    except ValueError as exc:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(exc)
        )
    except Exception as exc:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"发送验证码失败: {str(exc)}"
        )


@router.post("/me/verify-and-update-email", response_model=UserResponse)
async def verify_and_update_email(
    payload: VerifyAndUpdateEmailRequest,
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db)
):
    """验证并更新邮箱"""
    try:
        # 验证验证码
        email_service = await get_email_verification_service()
        is_valid = await email_service.verify_code(
            email=payload.new_email,
            code=payload.code
        )

        if not is_valid:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="验证码无效或已过期"
            )

        # 更新邮箱
        user_service = UserService(db)
        updated_user = await user_service.update_email(
            user_id=str(current_user.id),
            new_email=payload.new_email
        )
        await db.commit()

        return updated_user
    except ValueError as exc:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(exc)
        )
    except HTTPException:
        raise
    except Exception as exc:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"更新邮箱失败: {str(exc)}"
        )


@router.delete("/me", response_model=DeleteAccountResponse)
async def delete_my_account(
    payload: DeleteAccountRequest,
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db)
):
    """删除当前用户账号（软删除）"""
    user_service = UserService(db)
    try:
        await user_service.soft_delete_user(str(current_user.id), payload.password)
        await db.commit()
        return DeleteAccountResponse(detail="账号已删除")
    except ValueError as exc:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(exc)
        )


@router.post("/me/avatar", response_model=AvatarUploadResponse)
async def upload_my_avatar(
    file: UploadFile = File(...),
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db)
):
    """上传并更新当前用户头像"""
    allowed_types = {"image/jpeg", "image/png", "image/webp"}
    if file.content_type not in allowed_types:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="仅支持 JPG/PNG/WebP 图片文件"
        )

    content = await file.read()
    max_size = settings.MAX_UPLOAD_SIZE or 10485760
    if len(content) > max_size:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="文件过大，请选择 10MB 以下的图片"
        )

    try:
        cos_service = get_cos_service()
    except RuntimeError as exc:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(exc)
        )

    avatar_url = await cos_service.upload_avatar(
        user_id=str(current_user.id),
        filename=file.filename,
        content=content,
        content_type=file.content_type
    )

    user_service = UserService(db)
    try:
        await user_service.update_avatar(str(current_user.id), avatar_url)

        # 触发头像设置任务检查（失败不影响头像上传）
        print(f"[Avatar Upload] About to check avatar task for user {current_user.id}")
        try:
            await TaskService.check_avatar_task(db, current_user.id)
            print(f"[Avatar Upload] Avatar task check completed")
        except Exception as task_error:
            print(f"[Avatar Upload] Task check failed (non-critical): {task_error}")
            import traceback
            traceback.print_exc()

        await db.commit()
        print(f"[Avatar Upload] Transaction committed")
    except ValueError as exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(exc)
        )

    return AvatarUploadResponse(avatar_url=avatar_url)


# ==================== 用户搜索 ====================
# 注意：此路由必须在 /{user_id} 之前，否则 "search" 会被当作 user_id 匹配

@router.get("/search", response_model=UserSearchResponse)
async def search_users(
    keyword: str = Query(..., min_length=1, description="搜索关键词"),
    skip: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=50),
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """
    全站搜索用户

    - 搜索字段：username, full_name
    - 返回用户与当前用户的关系状态
    - 排除当前用户自己
    """
    # 1. 基础搜索（排除自己，排除非活跃用户）
    query = select(User).where(
        User.id != current_user.id,
        User.is_active == True,
        or_(
            User.username.ilike(f"%{keyword}%"),
            User.full_name.ilike(f"%{keyword}%")
        )
    )

    # 获取总数
    count_query = select(func.count()).select_from(query.subquery())
    total = (await db.execute(count_query)).scalar()

    # 获取用户列表
    query = query.order_by(User.username).offset(skip).limit(limit)
    result = await db.execute(query)
    users = result.scalars().all()

    if not users:
        return UserSearchResponse(total=0, items=[])

    # 2. 批量查询关系状态
    user_ids = [u.id for u in users]

    # 查询好友关系
    friendships_result = await db.execute(
        select(Friendship.friend_id).where(
            Friendship.user_id == current_user.id,
            Friendship.friend_id.in_(user_ids)
        )
    )
    friend_ids = set(row[0] for row in friendships_result.fetchall())

    # 查询我发出的请求
    sent_requests_result = await db.execute(
        select(FriendRequest.to_user_id).where(
            FriendRequest.from_user_id == current_user.id,
            FriendRequest.to_user_id.in_(user_ids),
            FriendRequest.status == 'pending'
        )
    )
    sent_request_ids = set(row[0] for row in sent_requests_result.fetchall())

    # 查询我收到的请求
    received_requests_result = await db.execute(
        select(FriendRequest.from_user_id).where(
            FriendRequest.to_user_id == current_user.id,
            FriendRequest.from_user_id.in_(user_ids),
            FriendRequest.status == 'pending'
        )
    )
    received_request_ids = set(row[0] for row in received_requests_result.fetchall())

    # 3. 组装结果
    items = []
    for user in users:
        if user.id in friend_ids:
            relation_status = "friend"
        elif user.id in sent_request_ids:
            relation_status = "request_sent"
        elif user.id in received_request_ids:
            relation_status = "request_received"
        else:
            relation_status = "none"

        items.append(UserSearchResult(
            id=user.id,
            username=user.username,
            full_name=user.full_name,
            avatar=user.avatar,
            relation_status=relation_status
        ))

    return UserSearchResponse(total=total, items=items)


# ==================== 用户主页 ====================

async def get_user_stats(db: AsyncSession, user_id: UUID) -> UserProfileStats:
    """获取用户统计数据"""
    # 作品统计（只统计已发布的）
    result = await db.execute(
        select(
            func.count(Work.id).label('work_count'),
            func.coalesce(func.sum(Work.total_words), 0).label('total_words'),
            func.coalesce(func.sum(Work.favorite_count), 0).label('total_favorites')
        ).where(
            Work.author_id == user_id,
            Work.is_published == True
        )
    )
    work_stats = result.first()

    # 好友数量
    friend_result = await db.execute(
        select(func.count(Friendship.id)).where(
            Friendship.user_id == user_id
        )
    )
    friend_count = friend_result.scalar() or 0

    return UserProfileStats(
        work_count=work_stats.work_count or 0,
        total_words=work_stats.total_words or 0,
        total_favorites=work_stats.total_favorites or 0,
        friend_count=friend_count
    )


async def get_user_relation(
    db: AsyncSession,
    current_user_id: UUID,
    target_user_id: UUID
) -> UserRelation:
    """获取与目标用户的关系"""
    # 是否是自己
    if current_user_id == target_user_id:
        return UserRelation(is_self=True, is_friend=False)

    # 检查好友关系
    friendship_result = await db.execute(
        select(Friendship).where(
            Friendship.user_id == current_user_id,
            Friendship.friend_id == target_user_id
        )
    )
    friendship = friendship_result.scalar_one_or_none()

    if friendship:
        return UserRelation(
            is_self=False,
            is_friend=True,
            private_channel_id=friendship.private_channel_id
        )

    # 检查待处理请求 - 我发出的请求
    sent_result = await db.execute(
        select(FriendRequest).where(
            FriendRequest.from_user_id == current_user_id,
            FriendRequest.to_user_id == target_user_id,
            FriendRequest.status == 'pending'
        )
    )
    sent = sent_result.scalar_one_or_none()
    if sent:
        return UserRelation(
            is_self=False,
            is_friend=False,
            pending_request={"id": str(sent.id), "direction": "sent", "status": "pending"}
        )

    # 检查待处理请求 - 我收到的请求
    received_result = await db.execute(
        select(FriendRequest).where(
            FriendRequest.from_user_id == target_user_id,
            FriendRequest.to_user_id == current_user_id,
            FriendRequest.status == 'pending'
        )
    )
    received = received_result.scalar_one_or_none()
    if received:
        return UserRelation(
            is_self=False,
            is_friend=False,
            pending_request={"id": str(received.id), "direction": "received", "status": "pending"}
        )

    # 陌生人
    return UserRelation(is_self=False, is_friend=False)


@router.get("/{user_id}/profile", response_model=UserProfileResponse)
async def get_user_profile(
    user_id: UUID,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """
    获取用户主页数据（聚合接口）
    
    返回用户信息、统计数据、与当前用户的关系、已发布作品列表
    """
    # 1. 获取目标用户
    result = await db.execute(select(User).where(User.id == user_id))
    target_user = result.scalar_one_or_none()
    if not target_user:
        raise HTTPException(status_code=404, detail="用户不存在")

    # 2. 获取统计数据
    stats = await get_user_stats(db, user_id)

    # 3. 获取关系
    relation = await get_user_relation(db, current_user.id, user_id)

    # 4. 获取已发布作品
    works_result = await db.execute(
        select(Work)
        .where(Work.author_id == user_id, Work.is_published == True)
        .order_by(Work.published_at.desc())
        .limit(50)
    )
    works = works_result.scalars().all()

    # 转换作品为 WorkBrief
    works_brief = [
        WorkBrief(
            id=w.id,
            title=w.title,
            cover_image=w.cover_image,
            total_words=w.total_words,
            favorite_count=w.favorite_count,
            genre=w.genre.value if hasattr(w.genre, 'value') else str(w.genre),
            status=w.status.value if hasattr(w.status, 'value') else str(w.status)
        )
        for w in works
    ]

    return UserProfileResponse(
        user=target_user,
        stats=stats,
        relation=relation,
        works=works_brief
    )



@router.get("/{user_id}", response_model=UserResponse)
async def get_user(
    user_id: str,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """根据 ID 获取用户信息"""
    user_service = UserService(db)
    user = await user_service.get_user_by_id(user_id)

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )

    return user


@router.get("", response_model=List[UserResponse])
async def get_users(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=100),
    search: str = None,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """
    获取用户列表

    - **skip**: 跳过的记录数（分页），范围 >= 0
    - **limit**: 返回的最大记录数，范围 1-100
    - **search**: 搜索关键词（用户名或邮箱）
    """
    user_service = UserService(db)
    users = await user_service.get_users(skip=skip, limit=limit, search=search)
    return users


# ==================== 会话管理 ====================

@router.get("/me/sessions", response_model=List[UserSessionResponse])
async def get_my_sessions(
    current_user: User = Depends(get_current_active_user),
    token: str = Depends(oauth2_scheme),
    db: AsyncSession = Depends(get_db)
):
    """获取当前用户的所有活跃会话"""
    user_service = UserService(db)
    try:
        sessions = await user_service.get_user_sessions(
            user_id=str(current_user.id),
            current_token=token
        )
        return sessions
    except Exception as error:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to get sessions: {str(error)}"
        )


@router.delete("/me/sessions/{session_id}")
async def logout_session(
    session_id: str,
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db)
):
    """退出指定会话"""
    user_service = UserService(db)
    try:
        await user_service.logout_session(
            user_id=str(current_user.id),
            session_id=session_id
        )
        await db.commit()
        return {"detail": "Session logged out successfully"}
    except ValueError as exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(exc)
        )
    except Exception as error:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to logout session: {str(error)}"
        )


@router.post("/me/sessions/logout-others")
async def logout_other_sessions(
    current_user: User = Depends(get_current_active_user),
    token: str = Depends(oauth2_scheme),
    db: AsyncSession = Depends(get_db)
):
    """退出除当前会话外的所有会话"""
    user_service = UserService(db)
    try:
        count = await user_service.logout_other_sessions(
            user_id=str(current_user.id),
            current_token=token
        )
        await db.commit()
        return {"detail": f"Logged out {count} sessions successfully", "count": count}
    except Exception as error:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to logout other sessions: {str(error)}"
        )


# ==================== 举报用户 ====================

@router.post("/{user_id}/report")
async def report_user(
    user_id: UUID,
    reason: str = Query(..., description="举报原因: spam, harassment, inappropriate, impersonation, other"),
    description: str = Query(None, description="详细描述"),
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """
    举报用户

    - reason: spam(垃圾信息), harassment(骚扰行为), inappropriate(不当内容), impersonation(冒充他人), other(其他)
    """
    # 不能举报自己
    if user_id == current_user.id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="不能举报自己"
        )

    # 检查被举报用户是否存在
    result = await db.execute(select(User).where(User.id == user_id))
    target_user = result.scalar_one_or_none()
    if not target_user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="用户不存在"
        )

    # 验证举报原因
    try:
        report_reason = UserReportReason(reason)
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="无效的举报原因"
        )

    # 检查是否已经举报过（待处理状态）
    existing_report = await db.execute(
        select(UserReport).where(
            UserReport.reporter_id == current_user.id,
            UserReport.reported_user_id == user_id,
            UserReport.status == UserReportStatus.pending
        )
    )
    if existing_report.scalar_one_or_none():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="您已举报过该用户，请等待处理"
        )

    # 创建举报记录
    report = UserReport(
        reporter_id=current_user.id,
        reported_user_id=user_id,
        reason=report_reason,
        description=description,
        status=UserReportStatus.pending
    )
    db.add(report)
    await db.commit()

    return {"message": "举报已提交，我们会尽快处理"}


