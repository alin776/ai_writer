"""邀请系统 Schemas"""

from datetime import datetime
from typing import Optional, List

from pydantic import BaseModel, Field, field_validator


# ============ 邀请码生成 ============

class InvitationGenerateRequest(BaseModel):
    """邀请码生成请求"""
    max_uses: int = Field(10, ge=1, le=100, description="最大使用次数")
    expires_days: Optional[int] = Field(None, ge=1, le=365, description="有效期天数")


class InvitationResponse(BaseModel):
    """邀请码响应"""
    id: str
    code: str = Field(..., description="邀请码")
    max_uses: int = Field(..., description="最大使用次数")
    used_count: int = Field(..., description="已使用次数")
    activated_count: int = Field(..., description="已激活次数")
    total_rewards: float = Field(..., description="累计奖励")
    expires_at: Optional[str] = Field(None, description="过期时间")
    created_at: str = Field(..., description="创建时间")
    invitees: List["InviteeInfo"] = Field(default_factory=list, description="被邀请人列表")

    class Config:
        from_attributes = True


class InviteeInfo(BaseModel):
    """被邀请人信息"""
    username: str = Field(..., description="用户名")
    status: str = Field(..., description="状态: pending/active/expired")
    registered_at: str = Field(..., description="注册时间")
    activated_at: Optional[str] = Field(None, description="激活时间")

    class Config:
        from_attributes = True


# ============ 邀请码验证 ============

class InvitationValidateRequest(BaseModel):
    """邀请码验证请求"""
    code: str = Field(..., min_length=8, max_length=8, description="邀请码")
    ip_address: Optional[str] = Field(None, max_length=45, description="IP地址")
    device_fingerprint: Optional[str] = Field(None, max_length=255, description="设备指纹")

    @field_validator('code')
    @classmethod
    def validate_code(cls, v: str) -> str:
        """验证邀请码格式"""
        return v.upper().strip()


class InvitationValidateResponse(BaseModel):
    """邀请码验证响应"""
    valid: bool = Field(..., description="是否有效")
    message: str = Field(..., description="验证消息")


# ============ 邀请统计 ============

class InvitationStatsResponse(BaseModel):
    """邀请统计响应"""
    total_invitations: int = Field(..., description="邀请码总数")
    total_used: int = Field(..., description="总使用次数")
    total_activated: int = Field(..., description="总激活次数")
    total_rewards: float = Field(..., description="总奖励积分")
    can_generate_more: bool = Field(..., description="是否可以生成更多")
    remaining_quota: int = Field(..., description="剩余配额")

    class Config:
        from_attributes = True
