"""
实体分组Schema定义
用于API请求和响应的数据验证
"""
from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any
from datetime import datetime
from uuid import UUID


# ============ 分组成员 ============

class GroupMemberBase(BaseModel):
    """分组成员基础Schema"""
    entity_id: UUID
    entity_type: str = Field(..., pattern="^(character|location|setting)$")
    order_index: int = 0


class GroupMemberCreate(GroupMemberBase):
    """创建分组成员"""
    pass


class GroupMemberResponse(GroupMemberBase):
    """分组成员响应"""
    id: UUID
    group_id: UUID
    created_at: datetime

    class Config:
        from_attributes = True


# ============ 实体分组 ============

class EntityGroupBase(BaseModel):
    """实体分组基础Schema"""
    name: str = Field(..., min_length=1, max_length=200)
    description: Optional[str] = None
    group_type: str = Field(default='manual', pattern="^(manual|auto)$")
    auto_rule: Optional[Dict[str, Any]] = None
    color: Optional[str] = Field(None, pattern="^#[0-9A-Fa-f]{6}$")
    icon: Optional[str] = None
    parent_group_id: Optional[UUID] = None
    order_index: int = 0


class EntityGroupCreate(EntityGroupBase):
    """创建实体分组"""
    work_id: UUID


class EntityGroupUpdate(BaseModel):
    """更新实体分组"""
    name: Optional[str] = Field(None, min_length=1, max_length=200)
    description: Optional[str] = None
    auto_rule: Optional[Dict[str, Any]] = None
    color: Optional[str] = Field(None, pattern="^#[0-9A-Fa-f]{6}$")
    icon: Optional[str] = None
    parent_group_id: Optional[UUID] = None
    order_index: Optional[int] = None


class EntityGroupResponse(EntityGroupBase):
    """实体分组响应"""
    id: UUID
    work_id: UUID
    members: List[GroupMemberResponse] = []
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


# ============ 批量操作 ============

class BatchAddMembersRequest(BaseModel):
    """批量添加分组成员请求"""
    members: List[GroupMemberCreate] = Field(..., min_items=1)


class BatchRemoveMembersRequest(BaseModel):
    """批量移除分组成员请求"""
    member_ids: List[UUID] = Field(..., min_items=1)
