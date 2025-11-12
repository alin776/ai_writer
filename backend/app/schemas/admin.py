"""
管理后台相关的Pydantic schemas
用于请求参数验证和响应数据格式化
"""
from pydantic import BaseModel, Field
from typing import Optional
from uuid import UUID


class UsersGrowthParams(BaseModel):
    """
    用户增长趋势查询参数
    
    限制days参数范围，防止DoS攻击
    """
    days: int = Field(
        default=7,
        ge=1,
        le=90,
        description="统计天数，范围1-90天"
    )


class RecentActivitiesParams(BaseModel):
    """
    最近活动记录查询参数
    
    限制limit参数范围，防止过大的查询
    """
    limit: int = Field(
        default=10,
        ge=1,
        le=100,
        description="返回记录数，范围1-100条"
    )


class UserBasicInfo(BaseModel):
    """
    用户基本信息响应模型
    """
    id: UUID
    username: str
    email: Optional[str]  # email可以为None
    is_active: bool
    is_admin: bool

    class Config:
        from_attributes = True


class UserActionResponse(BaseModel):
    """
    用户操作响应模型（封禁/解封/角色切换）
    """
    message: str
    user: UserBasicInfo
