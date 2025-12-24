from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime
from uuid import UUID

from app.models.channel import ChannelType, ChannelStatus
from app.models.channel_member import MemberRole
from app.models.channel_message import MessageType


# ========== Channel Schemas ==========

class ChannelBase(BaseModel):
    """频道基础Schema"""
    name: str = Field(..., min_length=1, max_length=100)
    description: Optional[str] = None
    cover_image: Optional[str] = None


class ChannelCreate(ChannelBase):
    """创建频道Schema"""
    type: ChannelType
    work_id: Optional[UUID] = None  # 作品频道需要


class FangroupCreate(BaseModel):
    """创建粉丝群Schema（不需要type字段）"""
    name: str = Field(..., min_length=1, max_length=100)
    description: Optional[str] = None
    cover_image: Optional[str] = None


class ChannelUpdate(BaseModel):
    """更新频道Schema"""
    name: Optional[str] = Field(None, min_length=1, max_length=100)
    description: Optional[str] = None
    cover_image: Optional[str] = None
    is_pinned: Optional[bool] = None


class ChannelResponse(ChannelBase):
    """频道响应Schema"""
    id: UUID
    type: ChannelType
    status: ChannelStatus
    creator_id: Optional[UUID]
    work_id: Optional[UUID]
    is_permanent: bool
    is_pinned: bool
    trial_end_at: Optional[datetime]
    member_count: int
    message_count: int
    last_message_at: Optional[datetime]
    warning_days: Optional[int]
    created_at: datetime
    updated_at: datetime
    locked_at: Optional[datetime]

    # 额外信息（用于作品频道）
    book_title: Optional[str] = None
    author: Optional[str] = None
    collect_count: Optional[int] = None

    # 当前用户在该频道中的角色
    current_user_role: Optional[MemberRole] = None

    # 进入要求
    join_requirement: Optional[str] = None
    can_access: bool = True  # 用户是否满足进入要求

    class Config:
        from_attributes = True


class ChannelListResponse(BaseModel):
    """频道列表响应"""
    channels: List[ChannelResponse]
    total: int


# ========== Channel Member Schemas ==========

class ChannelMemberBase(BaseModel):
    """频道成员基础Schema"""
    custom_title: Optional[str] = Field(None, max_length=50)
    title_color: Optional[str] = Field(None, max_length=20)


class ChannelMemberCreate(BaseModel):
    """加入频道Schema"""
    channel_id: UUID


class ChannelMemberUpdate(ChannelMemberBase):
    """更新成员信息Schema"""
    is_muted: Optional[bool] = None


class ChannelMemberResponse(ChannelMemberBase):
    """频道成员响应Schema"""
    id: UUID
    channel_id: UUID
    user_id: UUID
    role: MemberRole
    is_muted: bool
    muted_until: Optional[datetime] = None
    is_banned: bool
    joined_at: datetime
    last_read_at: Optional[datetime]

    # 用户信息
    user_name: Optional[str] = None
    user_avatar: Optional[str] = None

    class Config:
        from_attributes = True


# ========== Channel Message Schemas ==========

class ChannelMessageBase(BaseModel):
    """频道消息基础Schema"""
    content: str = Field(..., min_length=1)


class ChannelMessageCreate(ChannelMessageBase):
    """发送消息Schema"""
    channel_id: UUID
    type: MessageType = MessageType.NORMAL
    reply_to_id: Optional[UUID] = None


class ChannelMessageUpdate(BaseModel):
    """更新消息Schema"""
    content: Optional[str] = Field(None, min_length=1)
    is_pinned: Optional[bool] = None


class ChannelMessageResponse(ChannelMessageBase):
    """频道消息响应Schema"""
    id: UUID
    channel_id: UUID
    user_id: Optional[UUID]
    type: MessageType
    is_pinned: bool
    is_deleted: bool
    reply_to_id: Optional[UUID]
    reaction_count: int
    created_at: datetime
    updated_at: datetime
    deleted_at: Optional[datetime]

    # 用户信息
    user_name: Optional[str] = None
    user_avatar: Optional[str] = None
    user_honor: Optional[str] = None  # 用户全局称号
    user_title: Optional[str] = None  # 频道内自定义称号
    user_title_color: Optional[str] = None

    class Config:
        from_attributes = True


class ChannelMessageListResponse(BaseModel):
    """消息列表响应"""
    messages: List[ChannelMessageResponse]
    total: int
    has_more: bool
