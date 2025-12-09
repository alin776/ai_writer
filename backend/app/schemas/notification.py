from pydantic import BaseModel, Field, field_serializer
from typing import Optional, List, Dict, Any
from datetime import datetime
from uuid import UUID

from app.models.notification import (
    NotificationCategory,
    NotificationType,
    NotificationPriority,
    NotificationStatus,
    TargetUserType
)


# ==================== 行动按钮模型 ====================
class ActionButton(BaseModel):
    """行动按钮"""
    text: str = Field(..., min_length=1, max_length=50, description="按钮文字")
    url: str = Field(..., min_length=1, max_length=500, description="跳转链接")


# ==================== 通知基础模型 ====================
class NotificationBase(BaseModel):
    """通知基础模型"""
    title: str = Field(..., min_length=1, max_length=200, description="通知标题")
    content: Optional[str] = Field(None, description="通知内容（支持Markdown）")
    cover_image_url: Optional[str] = Field(None, max_length=500, description="封面图URL")

    category: NotificationCategory = Field(default=NotificationCategory.SYSTEM, description="通知分类")
    type: NotificationType = Field(..., description="通知类型")
    priority: NotificationPriority = Field(default=NotificationPriority.NORMAL, description="优先级")

    display_type: List[str] = Field(
        default=["notification"],
        description="展示方式：modal(弹窗), banner(横幅), notification(铃铛通知)"
    )
    action_button: Optional[ActionButton] = Field(None, description="行动按钮")
    banner_color: Optional[str] = Field(None, max_length=20, description="Banner背景颜色")

    target_users: TargetUserType = Field(default=TargetUserType.ALL, description="目标用户类型")
    custom_user_ids: Optional[List[UUID]] = Field(None, description="自定义用户列表")

    allow_dismiss: bool = Field(default=True, description="允许用户关闭")
    show_once: bool = Field(default=False, description="每个用户只展示一次")


# ==================== 创建通知 ====================
class NotificationCreate(NotificationBase):
    """创建通知"""
    valid_from: Optional[datetime] = Field(None, description="有效期开始时间")
    valid_until: Optional[datetime] = Field(None, description="有效期结束时间")
    publish_type: str = Field(
        default="immediate",
        description="发布类型：immediate(立即发布), scheduled(定时发布), draft(保存草稿)"
    )
    scheduled_at: Optional[datetime] = Field(None, description="定时发布时间")


# ==================== 更新通知 ====================
class NotificationUpdate(BaseModel):
    """更新通知"""
    title: Optional[str] = Field(None, min_length=1, max_length=200)
    content: Optional[str] = None
    cover_image_url: Optional[str] = Field(None, max_length=500)

    type: Optional[NotificationType] = None
    priority: Optional[NotificationPriority] = None

    display_type: Optional[List[str]] = None
    action_button: Optional[ActionButton] = None
    banner_color: Optional[str] = Field(None, max_length=20)

    target_users: Optional[TargetUserType] = None
    custom_user_ids: Optional[List[UUID]] = None

    valid_from: Optional[datetime] = None
    valid_until: Optional[datetime] = None

    allow_dismiss: Optional[bool] = None
    show_once: Optional[bool] = None

    status: Optional[NotificationStatus] = None


# ==================== 通知响应 ====================
class NotificationResponse(NotificationBase):
    """通知响应"""
    id: UUID
    category: NotificationCategory
    status: NotificationStatus

    published_at: Optional[datetime] = None
    valid_from: Optional[datetime] = None
    valid_until: Optional[datetime] = None

    created_by: Optional[UUID] = None
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

    @field_serializer('id', 'created_by')
    def serialize_uuid(self, value: Optional[UUID], _info) -> Optional[str]:
        """将 UUID 序列化为字符串"""
        return str(value) if value else None

    @field_serializer('custom_user_ids')
    def serialize_uuid_list(self, value: Optional[List[UUID]], _info) -> Optional[List[str]]:
        """将 UUID 列表序列化为字符串列表"""
        return [str(uid) for uid in value] if value else None


# ==================== 用户通知响应（包含已读状态） ====================
class UserNotificationResponse(BaseModel):
    """用户通知响应（包含已读等状态）"""
    # 通知基本信息
    id: UUID
    title: str
    content: Optional[str] = None
    cover_image_url: Optional[str] = None

    category: NotificationCategory
    type: NotificationType
    priority: NotificationPriority

    display_type: List[str]
    action_button: Optional[Dict[str, str]] = None  # ActionButton 转换为 dict
    banner_color: Optional[str] = None

    # 用户特定状态
    is_read: bool
    read_at: Optional[datetime] = None
    is_dismissed: bool
    dismissed_at: Optional[datetime] = None
    clicked: bool
    clicked_at: Optional[datetime] = None

    # 时间信息
    created_at: datetime
    published_at: Optional[datetime] = None
    valid_from: Optional[datetime] = None
    valid_until: Optional[datetime] = None

    class Config:
        from_attributes = True

    @field_serializer('id')
    def serialize_uuid(self, value: UUID, _info) -> str:
        """将 UUID 序列化为字符串"""
        return str(value)


# ==================== 通知列表响应 ====================
class NotificationListResponse(BaseModel):
    """通知列表响应（管理员视角）"""
    total: int
    page: int
    page_size: int
    items: List[NotificationResponse]


class UserNotificationListResponse(BaseModel):
    """用户通知列表响应"""
    total: int
    unread_count: int
    page: int
    page_size: int
    items: List[UserNotificationResponse]


# ==================== 未读数量响应 ====================
class UnreadCountResponse(BaseModel):
    """未读数量响应"""
    unread_count: int


# ==================== 标记已读请求 ====================
class MarkReadRequest(BaseModel):
    """标记已读请求"""
    notification_ids: Optional[List[UUID]] = Field(None, description="要标记的通知ID列表，为空则标记全部")


# ==================== 关闭弹窗请求 ====================
class DismissNotificationRequest(BaseModel):
    """关闭弹窗请求"""
    notification_id: UUID = Field(..., description="通知ID")


# ==================== 点击按钮请求 ====================
class ClickActionRequest(BaseModel):
    """点击行动按钮请求"""
    notification_id: UUID = Field(..., description="通知ID")


# ==================== 通知统计响应 ====================
class NotificationStatsResponse(BaseModel):
    """通知统计响应"""
    notification_id: UUID
    title: str

    # 触达统计
    total_users: int = Field(..., description="总触达用户数")
    read_count: int = Field(..., description="已读用户数")
    dismissed_count: int = Field(..., description="关闭弹窗用户数")
    clicked_count: int = Field(..., description="点击行动按钮用户数")

    # 比率
    read_rate: float = Field(..., description="查看率（百分比）")
    click_rate: float = Field(..., description="点击率（百分比）")

    # 时间信息
    published_at: Optional[datetime] = None
    valid_until: Optional[datetime] = None

    @field_serializer('notification_id')
    def serialize_uuid(self, value: UUID, _info) -> str:
        """将 UUID 序列化为字符串"""
        return str(value)


# ==================== 通知模板相关 ====================
class NotificationTemplateBase(BaseModel):
    """通知模板基础模型"""
    name: str = Field(..., min_length=1, max_length=100, description="模板名称")
    type: NotificationType = Field(..., description="通知类型")
    title_template: str = Field(..., min_length=1, max_length=200, description="标题模板")
    content_template: Optional[str] = Field(None, description="内容模板")
    default_priority: NotificationPriority = Field(default=NotificationPriority.NORMAL)


class NotificationTemplateCreate(NotificationTemplateBase):
    """创建通知模板"""
    pass


class NotificationTemplateUpdate(BaseModel):
    """更新通知模板"""
    title_template: Optional[str] = Field(None, min_length=1, max_length=200)
    content_template: Optional[str] = None
    default_priority: Optional[NotificationPriority] = None


class NotificationTemplateResponse(NotificationTemplateBase):
    """通知模板响应"""
    id: UUID
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

    @field_serializer('id')
    def serialize_uuid(self, value: UUID, _info) -> str:
        """将 UUID 序列化为字符串"""
        return str(value)


# ==================== 批量操作响应 ====================
class BatchOperationResponse(BaseModel):
    """批量操作响应"""
    success: bool
    message: str
    affected_count: int = Field(..., description="影响的记录数")
