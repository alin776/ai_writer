"""积分系统 Schemas"""

from datetime import datetime
from decimal import Decimal
from typing import Optional, List, Dict, Any
from uuid import UUID

from pydantic import BaseModel, Field, field_validator, ConfigDict


# ============ Token 详情 ============

class TokenDetailInfo(BaseModel):
    """AI 调用 token 详情（附带在交易记录中）"""
    model_name: str = ""
    prompt_tokens: int = 0
    completion_tokens: int = 0
    total_tokens: int = 0
    cache_read_tokens: int = 0
    cache_creation_tokens: int = 0
    reasoning_tokens: int = 0
    prompt_cost: float = 0.0
    completion_cost: float = 0.0
    total_cost: float = 0.0


# ============ 积分余额 ============

class BalanceResponse(BaseModel):
    """余额响应"""
    balance: float = Field(..., description="当前余额")
    total_recharged: float = Field(..., description="累计充值")
    total_consumed: float = Field(..., description="累计消费")
    total_gifted: float = Field(..., description="累计赠送")
    expires_at: Optional[str] = Field(None, description="过期时间")
    is_expired: bool = Field(..., description="是否已过期")

    model_config = ConfigDict(from_attributes=True)
# ============ 交易记录 ============

class TransactionResponse(BaseModel):
    """交易记录响应"""
    id: str
    type: str = Field(..., description="类型: recharge/consume/gift/expire/refund")
    amount: float = Field(..., description="金额（正数为增加，负数为减少）")
    balance_before: float = Field(..., description="交易前余额")
    balance_after: float = Field(..., description="交易后余额")
    description: str = Field(..., description="描述")
    related_type: Optional[str] = Field(None, description="关联类型")
    related_id: Optional[str] = Field(None, description="关联ID")
    created_at: str = Field(..., description="创建时间")
    token_details: Optional[TokenDetailInfo] = Field(None, description="Token 详情（仅 ai_call 类型）")

    model_config = ConfigDict(from_attributes=True)
class TransactionListRequest(BaseModel):
    """交易记录查询请求"""
    page: int = Field(1, ge=1, description="页码")
    page_size: int = Field(20, ge=1, le=100, description="每页数量")
    type: Optional[str] = Field(None, description="筛选类型")
    start_date: Optional[datetime] = Field(None, description="开始日期")
    end_date: Optional[datetime] = Field(None, description="结束日期")


class TransactionListResponse(BaseModel):
    """交易记录列表响应"""
    items: List[TransactionResponse]
    total: int
    page: int
    page_size: int
    total_pages: int
    pricing_info: Optional[Dict[str, Any]] = Field(None, description="定价元数据")


# ============ 兑换码 ============

class RedeemRequest(BaseModel):
    """兑换码兑换请求"""
    code: str = Field(..., min_length=12, max_length=12, description="兑换码")

    @field_validator('code')
    @classmethod
    def validate_code(cls, v: str) -> str:
        """验证兑换码格式"""
        return v.upper().strip()


class RedeemResponse(BaseModel):
    """兑换码兑换响应"""
    credits: float = Field(..., description="兑换的积分")
    balance_before: float = Field(..., description="兑换前余额")
    balance_after: float = Field(..., description="兑换后余额")

    model_config = ConfigDict(from_attributes=True)
