"""管理员邀请系统 Schemas"""

from datetime import datetime
from typing import Optional, List
from decimal import Decimal

from pydantic import BaseModel, Field, field_validator


# ============ 管理员邀请码生成 ============

class AdminInvitationGenerateRequest(BaseModel):
    """管理员邀请码生成请求"""
    custom_code: Optional[str] = Field(
        None,
        min_length=3,
        max_length=8,
        description="自定义邀请码（3-8位，可选）"
    )
    max_uses: int = Field(
        1,
        ge=1,
        le=100,
        description="最大使用次数（1-100）"
    )
    expires_days: int = Field(
        90,
        ge=1,
        le=365,
        description="有效期天数（1-365）"
    )
    remark: Optional[str] = Field(
        None,
        max_length=255,
        description="备注信息"
    )

    @field_validator('custom_code')
    @classmethod
    def validate_custom_code(cls, v: Optional[str]) -> Optional[str]:
        """验证自定义邀请码格式"""
        if v is None:
            return None
        # 转换为大写并去除空格
        code = v.upper().strip()
        # 验证只包含字母和数字
        if not code.isalnum():
            raise ValueError("邀请码只能包含字母和数字")
        return code


class AdminInvitationResponse(BaseModel):
    """管理员邀请码响应"""
    id: str
    code: str = Field(..., description="邀请码")
    max_uses: int = Field(..., description="最大使用次数")
    used_count: int = Field(..., description="已使用次数")
    activated_count: int = Field(..., description="已激活次数")
    total_rewards: float = Field(..., description="累计奖励")
    expires_at: Optional[str] = Field(None, description="过期时间")
    remark: Optional[str] = Field(None, description="备注信息")
    created_by: str = Field(..., description="创建者用户ID")
    creator_username: Optional[str] = Field(None, description="创建者用户名")
    created_at: str = Field(..., description="创建时间")
    status: str = Field(..., description="状态: active/expired/exhausted")

    class Config:
        from_attributes = True


# ============ 管理员邀请码列表查询 ============

class AdminInvitationListRequest(BaseModel):
    """管理员邀请码列表查询请求"""
    page: int = Field(1, ge=1, description="页码")
    page_size: int = Field(20, ge=1, le=100, description="每页数量")
    status: Optional[str] = Field(
        None,
        description="状态筛选: active/expired/exhausted/all"
    )
    creator_id: Optional[str] = Field(None, description="创建者ID筛选")
    search: Optional[str] = Field(None, description="搜索关键词（邀请码或备注）")


class AdminInvitationListItem(BaseModel):
    """管理员邀请码列表项"""
    id: str
    code: str = Field(..., description="邀请码")
    max_uses: int = Field(..., description="最大使用次数")
    used_count: int = Field(..., description="已使用次数")
    activated_count: int = Field(..., description="已激活次数")
    total_rewards: float = Field(..., description="累计奖励")
    usage_rate: float = Field(..., description="使用率（百分比）")
    expires_at: Optional[str] = Field(None, description="过期时间")
    remark: Optional[str] = Field(None, description="备注信息")
    creator_username: Optional[str] = Field(None, description="创建者用户名")
    created_at: str = Field(..., description="创建时间")
    status: str = Field(..., description="状态: active/expired/exhausted")

    class Config:
        from_attributes = True


class AdminInvitationListResponse(BaseModel):
    """管理员邀请码列表响应"""
    total: int = Field(..., description="总数")
    page: int = Field(..., description="当前页")
    page_size: int = Field(..., description="每页数量")
    total_pages: int = Field(..., description="总页数")
    items: List[AdminInvitationListItem] = Field(
        default_factory=list,
        description="邀请码列表"
    )
    stats: "AdminInvitationStats" = Field(..., description="统计信息")


class AdminInvitationStats(BaseModel):
    """管理员邀请码统计"""
    total_codes: int = Field(0, description="邀请码总数")
    active_codes: int = Field(0, description="有效邀请码数")
    expired_codes: int = Field(0, description="已过期邀请码数")
    exhausted_codes: int = Field(0, description="已用完邀请码数")
    total_usages: int = Field(0, description="总使用次数")
    total_activated: int = Field(0, description="总激活次数")
    total_rewards: float = Field(0, description="总奖励积分")


# ============ 删除邀请码 ============

class AdminInvitationDeleteResponse(BaseModel):
    """删除邀请码响应"""
    success: bool = Field(..., description="是否成功")
    message: str = Field(..., description="消息")
