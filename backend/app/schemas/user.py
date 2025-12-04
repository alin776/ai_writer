from pydantic import BaseModel, EmailStr, Field, field_serializer
from typing import Optional, Literal
from datetime import datetime
from uuid import UUID


class NotificationSettings(BaseModel):
    """通知设置"""
    email_notifications: bool = True
    browser_notifications: bool = False
    new_chapter: bool = True
    comments: bool = True
    mentions: bool = True
    system_updates: bool = False


class Preferences(BaseModel):
    """用户偏好设置"""
    theme: Literal['light', 'dark', 'auto'] = 'light'
    language: Literal['zh-CN', 'en-US'] = 'zh-CN'
    font_size: Literal['small', 'medium', 'large'] = 'medium'
    auto_save: bool = True
    auto_save_interval: int = Field(30, ge=5, le=600)


class ChangePasswordRequest(BaseModel):
    """修改密码请求"""
    current_password: str = Field(..., min_length=6, max_length=50)
    new_password: str = Field(..., min_length=6, max_length=50)


class ChangePasswordResponse(BaseModel):
    """修改密码响应"""
    detail: str = "Password updated successfully"


class DeleteAccountRequest(BaseModel):
    """删除账号请求"""
    password: str = Field(..., min_length=6, max_length=50)


class DeleteAccountResponse(BaseModel):
    """删除账号响应"""
    detail: str = "Account deleted successfully"


class AvatarUploadResponse(BaseModel):
    """头像上传响应"""
    avatar_url: str


class UserBase(BaseModel):
    """用户基础模型"""
    username: str = Field(..., min_length=3, max_length=50)
    email: EmailStr


class UserCreate(UserBase):
    """创建用户"""
    password: str = Field(..., min_length=6, max_length=50)
    invitation_code: str = Field(..., min_length=8, max_length=8, description="邀请码")
    device_fingerprint: Optional[str] = Field(None, max_length=255, description="设备指纹（用于防刷）")


class UserLogin(BaseModel):
    """用户登录"""
    username: str
    password: str


class UserUpdate(BaseModel):
    """更新用户"""
    email: Optional[EmailStr] = None
    username: Optional[str] = Field(None, min_length=3, max_length=50)
    full_name: Optional[str] = Field(None, max_length=100)
    avatar: Optional[str] = None
    bio: Optional[str] = None
    notification_settings: Optional[NotificationSettings] = None
    preferences: Optional[Preferences] = None


class UserResponse(UserBase):
    """用户响应"""
    # 放宽响应校验，兼容占位域名等非标准邮箱
    email: Optional[str] = None
    id: UUID
    full_name: Optional[str] = None
    avatar: Optional[str] = None
    bio: Optional[str] = None
    notification_settings: NotificationSettings = Field(default_factory=NotificationSettings)
    preferences: Preferences = Field(default_factory=Preferences)
    is_active: bool
    is_admin: bool
    is_verified: bool
    created_at: datetime
    updated_at: datetime
    last_login_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True
    
    @field_serializer('id')
    def serialize_id(self, value: UUID, _info) -> str:
        """将 UUID 序列化为字符串"""
        return str(value)


class Token(BaseModel):
    """JWT Token"""
    access_token: str
    refresh_token: str
    token_type: str = "bearer"


class AuthResponse(BaseModel):
    """认证响应（注册/登录后返回）"""
    user: UserResponse
    access_token: str
    refresh_token: str
    token_type: str = "bearer"


class TokenData(BaseModel):
    """Token 数据"""
    user_id: Optional[str] = None


class UserSessionResponse(BaseModel):
    """用户会话响应"""
    id: UUID
    device_type: Optional[str] = None
    device_name: Optional[str] = None
    browser: Optional[str] = None
    browser_version: Optional[str] = None
    operating_system: Optional[str] = None
    ip_address: Optional[str] = None
    location: Optional[str] = None
    is_active: bool
    is_current: bool = False  # 是否为当前会话，由服务层计算
    created_at: datetime
    last_active_at: Optional[datetime] = None

    class Config:
        from_attributes = True

    @field_serializer('id')
    def serialize_id(self, value: UUID, _info) -> str:
        """将 UUID 序列化为字符串"""
        return str(value)
