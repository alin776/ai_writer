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

    # 慢速模式
    slowmode_interval: Optional[int] = None  # 慢速模式间隔(秒)

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


class MessageEditRequest(BaseModel):
    """编辑消息请求Schema"""
    content: str = Field(..., min_length=1, max_length=5000)


class ChannelMessageResponse(ChannelMessageBase):
    """频道消息响应Schema"""
    id: UUID
    channel_id: UUID
    user_id: Optional[UUID]
    type: MessageType
    is_pinned: bool
    is_deleted: bool
    is_edited: bool = False
    reply_to_id: Optional[UUID]
    forwarded_from_id: Optional[UUID] = None  # 转发来源消息ID
    reaction_count: int
    created_at: datetime
    updated_at: datetime
    deleted_at: Optional[datetime]
    edited_at: Optional[datetime] = None

    # 用户信息
    user_name: Optional[str] = None
    user_avatar: Optional[str] = None
    user_honor: Optional[str] = None  # 用户全局称号
    user_title: Optional[str] = None  # 频道内自定义称号
    user_title_color: Optional[str] = None

    # 附件列表
    attachments: List["AttachmentResponse"] = []

    class Config:
        from_attributes = True


class ChannelMessageListResponse(BaseModel):
    """消息列表响应"""
    messages: List[ChannelMessageResponse]
    total: int
    has_more: bool


# ========== Message Reaction Schemas ==========

class ReactionCreate(BaseModel):
    """添加反应Schema"""
    emoji: str = Field(..., min_length=1, max_length=50)


class ReactionUserResponse(BaseModel):
    """反应用户信息"""
    user_id: UUID
    username: str
    avatar: Optional[str] = None

    class Config:
        from_attributes = True


class ReactionSummary(BaseModel):
    """反应汇总（用于消息列表）"""
    emoji: str
    count: int
    has_reacted: bool = False  # 当前用户是否已反应


class ReactionDetailResponse(BaseModel):
    """反应详情响应（用于查看具体用户）"""
    emoji: str
    count: int
    users: List[ReactionUserResponse]


class MessageReactionsResponse(BaseModel):
    """消息的所有反应汇总"""
    message_id: UUID
    reactions: List[ReactionSummary]
    total_count: int


# ========== Message Pin Schemas ==========

class PinnedMessageResponse(BaseModel):
    """置顶消息响应"""
    id: UUID
    channel_id: UUID
    content: str
    user_id: Optional[UUID]
    user_name: Optional[str] = None
    user_avatar: Optional[str] = None
    is_pinned: bool = True
    pinned_at: Optional[datetime] = None
    pinned_by: Optional[UUID] = None
    pinned_by_name: Optional[str] = None
    created_at: datetime

    class Config:
        from_attributes = True


class PinnedMessagesListResponse(BaseModel):
    """置顶消息列表响应"""
    messages: List[PinnedMessageResponse]
    total: int


# ========== Message Attachment Schemas ==========

class AttachmentResponse(BaseModel):
    """附件响应"""
    id: UUID
    file_name: str
    file_type: str
    file_size: int
    file_url: str
    thumbnail_url: Optional[str] = None
    created_at: datetime

    class Config:
        from_attributes = True


class AttachmentUploadResponse(BaseModel):
    """附件上传响应"""
    id: UUID
    file_name: str
    file_type: str
    file_size: int
    file_url: str
    thumbnail_url: Optional[str] = None


class MessageWithAttachmentsResponse(ChannelMessageResponse):
    """带附件的消息响应"""
    attachments: List[AttachmentResponse] = []


# ========== Message Forward Schemas ==========

class ForwardMessageRequest(BaseModel):
    """转发消息请求"""
    target_channel_ids: List[UUID] = Field(..., min_length=1, max_length=10, description="目标频道ID列表")
    add_comment: Optional[str] = Field(None, max_length=500, description="转发时附加的评论")


class ForwardedMessageInfo(BaseModel):
    """转发来源信息"""
    original_message_id: UUID
    original_channel_id: UUID
    original_channel_name: str
    original_user_name: str
    original_content: str
    original_created_at: datetime


class ForwardMessageResponse(BaseModel):
    """转发消息响应"""
    forwarded_count: int
    failed_channels: List[UUID] = []
    messages: List[dict] = []
