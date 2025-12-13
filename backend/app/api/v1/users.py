from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File, Query
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List

from app.core.database import get_db
from app.core.security import get_current_active_user, oauth2_scheme
from app.models.user import User
from app.schemas.user import (
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
)
from app.services.user_service import UserService
from app.services.cos_service import get_cos_service
from app.services.task_service import TaskService
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
        await email_service.send_verification_code(
            user_id=str(current_user.id),
            new_email=payload.new_email,
            current_email=current_user.email
        )
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
            user_id=str(current_user.id),
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

