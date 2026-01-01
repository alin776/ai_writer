from pydantic import BaseModel, EmailStr, Field, field_serializer, field_validator
from typing import Optional, Literal, List
from datetime import datetime
from uuid import UUID
import re


def validate_password_strength(password: str) -> str:
    """
    验证密码强度
    - 长度8-20位
    - 必须包含字母、数字、特殊符号三种字符
    """
    if len(password) < 8:
        raise ValueError("密码长度至少为8位")
    if len(password) > 20:
        raise ValueError("密码长度不能超过20位")

    has_letter = bool(re.search(r'[a-zA-Z]', password))
    has_number = bool(re.search(r'\d', password))
    has_special = bool(re.search(r'[!@#$%^&*()_+\-=\[\]{};\':"\\|,.<>\/?]', password))

    if not (has_letter and has_number and has_special):
        raise ValueError("密码必须包含字母、数字、特殊符号三种字符")

    return password


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
    language: Literal['zh-CN', 'zh-TW', 'en-US'] = 'zh-CN'
    font_size: Literal['small', 'medium', 'large'] = 'medium'
    auto_save: bool = True
    auto_save_interval: int = Field(30, ge=5, le=600)
    ai_auto_complete: bool = False  # AI 自动补全开关，默认关闭


class ChangePasswordRequest(BaseModel):
    """修改密码请求"""
    current_password: str = Field(..., min_length=1, max_length=50)
    new_password: str = Field(..., min_length=8, max_length=20)

    @field_validator('new_password')
    @classmethod
    def validate_new_password(cls, v: str) -> str:
        return validate_password_strength(v)


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
    username: str = Field(..., min_length=2, max_length=50)
    email: EmailStr


class UserCreate(UserBase):
    """创建用户"""
    password: str = Field(..., min_length=8, max_length=20)
    invitation_code: str = Field(..., min_length=8, max_length=8, description="邀请码")
    email_verification_code: str = Field(..., min_length=6, max_length=6, description="邮箱验证码")
    device_fingerprint: Optional[str] = Field(None, max_length=255, description="设备指纹（用于防刷）")

    @field_validator('password')
    @classmethod
    def validate_password(cls, v: str) -> str:
        return validate_password_strength(v)


class UserLogin(BaseModel):
    """用户登录"""
    username: str
    password: str


class UserUpdate(BaseModel):
    """更新用户"""
    email: Optional[EmailStr] = None
    username: Optional[str] = Field(None, min_length=2, max_length=50)
    full_name: Optional[str] = Field(None, max_length=100)
    avatar: Optional[str] = None
    bio: Optional[str] = None
    honor: Optional[str] = Field(None, max_length=50)  # 用户称号
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
    honor: Optional[str] = None  # 用户称号
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
    expires_at: Optional[int] = None  # access token 过期时间戳（秒）
    refresh_expires_at: Optional[int] = None  # refresh token 过期时间戳（秒）


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


# ==================== 修改邮箱相关 ====================

class SendEmailCodeRequest(BaseModel):
    """发送邮箱验证码请求"""
    new_email: EmailStr = Field(..., description="新邮箱地址")


class SendEmailCodeResponse(BaseModel):
    """发送邮箱验证码响应"""
    detail: str = "验证码已发送"


class VerifyAndUpdateEmailRequest(BaseModel):
    """验证并更新邮箱请求"""
    new_email: EmailStr = Field(..., description="新邮箱地址")
    code: str = Field(..., min_length=6, max_length=6, description="验证码")


class VerifyAndUpdateEmailResponse(BaseModel):
    """验证并更新邮箱响应"""
    detail: str = "邮箱修改成功"


# ==================== 忘记密码相关 ====================

class ForgotPasswordRequest(BaseModel):
    """忘记密码 - 发送验证码请求"""
    email: EmailStr = Field(..., description="注册邮箱地址")


class ForgotPasswordResponse(BaseModel):
    """忘记密码 - 发送验证码响应"""
    detail: str = "如果该邮箱已注册，验证码已发送"


class ResetPasswordRequest(BaseModel):
    """重置密码请求"""
    email: EmailStr = Field(..., description="注册邮箱地址")
    code: str = Field(..., min_length=6, max_length=6, description="验证码")
    new_password: str = Field(..., min_length=8, max_length=20, description="新密码")

    @field_validator('new_password')
    @classmethod
    def validate_new_password(cls, v: str) -> str:
        return validate_password_strength(v)


class ResetPasswordResponse(BaseModel):
    """重置密码响应"""
    detail: str = "密码重置成功，请使用新密码登录"

# ==================== 用户主页相关 ====================

class UserProfileStats(BaseModel):
    """用户统计数据"""
    work_count: int
    total_words: int
    total_favorites: int
    friend_count: int

    class Config:
        from_attributes = True


class UserRelation(BaseModel):
    """与当前用户的关系"""
    is_self: bool
    is_friend: bool
    private_channel_id: Optional[UUID] = None
    pending_request: Optional[dict] = None  # 包含 id, direction, status

    class Config:
        from_attributes = True

    @field_serializer('private_channel_id')
    def serialize_channel_id(self, value: Optional[UUID], _info) -> Optional[str]:
        """将 UUID 序列化为字符串"""
        return str(value) if value else None


class WorkBrief(BaseModel):
    """作品简要信息（用于主页展示）"""
    id: UUID
    title: str
    cover_image: Optional[str] = None
    total_words: int
    favorite_count: int
    genre: str
    status: str

    class Config:
        from_attributes = True

    @field_serializer('id')
    def serialize_id(self, value: UUID, _info) -> str:
        """将 UUID 序列化为字符串"""
        return str(value)


class UserProfileResponse(BaseModel):
    """用户主页响应"""
    user: UserResponse
    stats: UserProfileStats
    relation: UserRelation
    works: List[WorkBrief]
