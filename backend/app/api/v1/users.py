from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File
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
)
from app.services.user_service import UserService
from app.services.cos_service import get_cos_service
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
        user = await user_service.update_user(str(current_user.id), user_data)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found"
            )
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
        return await user_service.update_notification_settings(str(current_user.id), settings)
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
        return await user_service.update_preferences(str(current_user.id), preferences)
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
        return ChangePasswordResponse(detail="密码修改成功")
    except ValueError as exc:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(exc)
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
    skip: int = 0,
    limit: int = 100,
    search: str = None,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """
    获取用户列表

    - **skip**: 跳过的记录数（分页）
    - **limit**: 返回的最大记录数
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
        return {"detail": f"Logged out {count} sessions successfully", "count": count}
    except Exception as error:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to logout other sessions: {str(error)}"
        )

