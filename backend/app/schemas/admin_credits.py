"""管理端积分系统 Schemas"""

from datetime import datetime
from decimal import Decimal
from typing import Optional, List
from uuid import UUID

from pydantic import BaseModel, Field, field_validator, EmailStr


# ============ 兑换码管理 ============

class AdminRedeemCodeGenerateRequest(BaseModel):
    """管理端兑换码生成请求"""
    count: int = Field(..., ge=1, le=100, description="生成数量")
    credits: float = Field(..., gt=0, description="每个兑换码的积分数")
    expires_days: Optional[int] = Field(None, ge=1, le=365, description="有效期天数")
    remark: Optional[str] = Field(None, max_length=255, description="备注")


class AdminRedeemCodeResponse(BaseModel):
    """管理端兑换码响应"""
    id: str
    code: str
    credits: float
    is_used: bool
    used_by: Optional[str] = None
    used_at: Optional[str] = None
    expires_at: Optional[str] = None
    is_expired: bool
    created_by: Optional[str] = None
    remark: Optional[str] = None
    created_at: str

    class Config:
        from_attributes = True


class AdminRedeemCodeListRequest(BaseModel):
    """管理端兑换码列表请求"""
    page: int = Field(1, ge=1, description="页码")
    page_size: int = Field(20, ge=1, le=100, description="每页数量")
    is_used: Optional[bool] = Field(None, description="筛选已使用/未使用")
    is_expired: Optional[bool] = Field(None, description="筛选已过期/未过期")


class AdminRedeemCodeListResponse(BaseModel):
    """管理端兑换码列表响应"""
    items: List[AdminRedeemCodeResponse]
    total: int
    page: int
    page_size: int
    total_pages: int
    stats: dict = Field(..., description="统计信息")


# ============ 积分赠送 ============

class AdminGiftCreditsRequest(BaseModel):
    """管理端赠送积分请求"""
    user_email: EmailStr = Field(..., description="用户邮箱")
    amount: float = Field(..., gt=0, description="赠送数量")
    description: str = Field(..., min_length=1, max_length=255, description="赠送原因")


class AdminGiftCreditsResponse(BaseModel):
    """管理端赠送积分响应"""
    user_id: str
    amount: float
    balance_before: float
    balance_after: float
    description: str
    created_at: str

    class Config:
        from_attributes = True


# ============ 积分统计 ============

class AdminCreditsStatsResponse(BaseModel):
    """管理端积分统计响应"""
    total_users: int = Field(..., description="总用户数")
    total_balance: float = Field(..., description="总余额")
    total_recharged: float = Field(..., description="总充值")
    total_consumed: float = Field(..., description="总消费")
    total_gifted: float = Field(..., description="总赠送")
    total_transactions: int = Field(..., description="总交易数")

    class Config:
        from_attributes = True
