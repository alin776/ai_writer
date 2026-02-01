from pydantic import BaseModel, Field, ConfigDict
from typing import Optional, List, Literal
from uuid import UUID
from datetime import datetime


# ========== 用户简要信息 ==========

class UserBrief(BaseModel):
    """用户简要信息"""
    id: UUID
    username: str
    full_name: Optional[str] = None
    avatar: Optional[str] = None

    model_config = ConfigDict(from_attributes=True)
# ========== 好友请求 Schemas ==========

class FriendRequestCreate(BaseModel):
    """发送好友请求"""
    to_user_id: UUID
    message: Optional[str] = Field(None, max_length=200)


class FriendRequestAction(BaseModel):
    """处理好友请求"""
    action: Literal["accept", "reject"]


class FriendRequestResponse(BaseModel):
    """好友请求响应"""
    id: UUID
    from_user: UserBrief
    to_user: UserBrief
    message: Optional[str] = None
    status: str
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)
class FriendRequestListResponse(BaseModel):
    """好友请求列表响应"""
    total: int
    items: List[FriendRequestResponse]


# ========== 好友关系 Schemas ==========

class FriendshipResponse(BaseModel):
    """好友关系响应"""
    id: UUID
    friend: UserBrief
    private_channel_id: Optional[UUID] = None
    last_message_at: Optional[datetime] = None  # 私聊频道最后消息时间
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)
class FriendListResponse(BaseModel):
    """好友列表响应"""
    total: int
    items: List[FriendshipResponse]


class AcceptRequestResponse(BaseModel):
    """同意好友请求响应"""
    message: str
    friendship: FriendshipResponse
    private_channel_id: UUID


class RejectRequestResponse(BaseModel):
    """拒绝好友请求响应"""
    message: str


# ========== 好友关系检查 ==========

class PendingRequestInfo(BaseModel):
    """待处理请求信息"""
    id: UUID
    direction: Literal["sent", "received"]
    status: str


class FriendCheckResponse(BaseModel):
    """好友关系检查响应"""
    is_friend: bool
    friendship_id: Optional[UUID] = None
    private_channel_id: Optional[UUID] = None
    pending_request: Optional[PendingRequestInfo] = None


class PendingCountResponse(BaseModel):
    """待处理请求数量响应"""
    pending_count: int


# ========== 用户搜索 ==========

class UserSearchResult(BaseModel):
    """用户搜索结果"""
    id: UUID
    username: str
    full_name: Optional[str] = None
    avatar: Optional[str] = None
    relation_status: Literal["none", "friend", "request_sent", "request_received"]

    model_config = ConfigDict(from_attributes=True)
class UserSearchResponse(BaseModel):
    """用户搜索响应"""
    total: int
    items: List[UserSearchResult]
