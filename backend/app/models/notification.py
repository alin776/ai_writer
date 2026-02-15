from sqlalchemy import Column, String, DateTime, Boolean, Text, ForeignKey, Enum, ARRAY
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
import uuid
import enum

from app.core.database import Base


class NotificationCategory(str, enum.Enum):
    """通知分类"""
    SYSTEM = "system"  # 系统自动通知
    ANNOUNCEMENT = "announcement"  # 运营通知/活动
    INTERACTION = "interaction"  # 互动通知（评论回复、收藏等）


class NotificationType(str, enum.Enum):
    """通知类型"""
    # 系统通知类型
    AI_TASK_COMPLETED = "ai_task_completed"  # AI任务完成
    ANALYSIS_READY = "analysis_ready"  # 分析报告生成
    SMART_REMINDER = "smart_reminder"  # 智能提醒
    MILESTONE = "milestone"  # 里程碑达成
    INACTIVITY_ALERT = "inactivity_alert"  # 灵感保鲜提醒
    WARNING = "warning"  # 警告通知（举报处理）

    # 运营通知类型
    EVENT = "event"  # 活动
    FEATURE = "feature"  # 新功能上线
    ANNOUNCEMENT = "announcement"  # 公告
    MAINTENANCE = "maintenance"  # 系统维护

    # 互动通知类型
    COMMENT_REPLY = "comment_reply"  # 评论被回复
    WORK_FAVORITED = "work_favorited"  # 作品被收藏


class NotificationPriority(str, enum.Enum):
    """通知优先级"""
    URGENT = "urgent"  # 紧急（Banner + 弹窗）
    IMPORTANT = "important"  # 重要（弹窗）
    NORMAL = "normal"  # 普通（仅通知列表）


class NotificationStatus(str, enum.Enum):
    """通知状态"""
    DRAFT = "draft"  # 草稿
    SCHEDULED = "scheduled"  # 已定时
    ACTIVE = "active"  # 进行中
    EXPIRED = "expired"  # 已过期


class TargetUserType(str, enum.Enum):
    """目标用户类型"""
    ALL = "all"  # 全部用户
    ACTIVE = "active"  # 活跃用户（最近7天登录）
    INACTIVE = "inactive"  # 不活跃用户（超过7天未登录）
    CUSTOM = "custom"  # 自定义用户列表


class Notification(Base):
    """通知模型"""

    __tablename__ = "notifications"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)

    # 基础信息
    title = Column(String(200), nullable=False)
    content = Column(Text, nullable=True)
    cover_image_url = Column(String(500), nullable=True)

    # 分类
    category = Column(
        Enum(NotificationCategory),
        nullable=False,
        default=NotificationCategory.SYSTEM,
        index=True
    )
    type = Column(
        Enum(NotificationType),
        nullable=False,
        index=True
    )
    priority = Column(
        Enum(NotificationPriority),
        nullable=False,
        default=NotificationPriority.NORMAL
    )

    # 展示配置
    display_type = Column(
        ARRAY(String),
        nullable=False,
        server_default="{notification}"  # 可选值: modal, banner, notification
    )
    action_button = Column(
        JSONB,
        nullable=True  # {text: "立即参与", url: "/activities/xxx"}
    )
    banner_color = Column(String(20), nullable=True)  # 如 "#FF5733"

    # 目标受众
    target_users = Column(
        Enum(TargetUserType),
        nullable=False,
        default=TargetUserType.ALL
    )
    custom_user_ids = Column(
        ARRAY(UUID(as_uuid=True)),
        nullable=True
    )

    # 发布管理
    status = Column(
        Enum(NotificationStatus),
        nullable=False,
        default=NotificationStatus.DRAFT,
        index=True
    )
    published_at = Column(DateTime(timezone=True), nullable=True)
    valid_from = Column(DateTime(timezone=True), nullable=True)
    valid_until = Column(DateTime(timezone=True), nullable=True, index=True)

    # 行为配置
    allow_dismiss = Column(Boolean, default=True, nullable=False)  # 允许用户关闭
    show_once = Column(Boolean, default=False, nullable=False)  # 每个用户只展示一次

    # 活动相关字段（仅当 type 为 EVENT 时使用）
    activity_type = Column(String(50), nullable=True)  # 活动类型：invitation, competition, points 等
    activity_rules = Column(JSONB, nullable=True)  # 活动规则，根据 activity_type 不同而不同

    # 创建者（仅运营通知有，系统通知为NULL）
    created_by = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=True)

    # 时间戳
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)

    # 关联关系
    creator = relationship("User", foreign_keys=[created_by])
    user_notifications = relationship(
        "UserNotification",
        back_populates="notification",
        cascade="all, delete-orphan"
    )

    def __repr__(self):
        return f"<Notification {self.title}>"


class UserNotification(Base):
    """用户-通知关系表"""

    __tablename__ = "user_notifications"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False, index=True)
    notification_id = Column(UUID(as_uuid=True), ForeignKey("notifications.id"), nullable=False, index=True)

    # 状态
    is_read = Column(Boolean, default=False, nullable=False, index=True)
    read_at = Column(DateTime(timezone=True), nullable=True)
    is_dismissed = Column(Boolean, default=False, nullable=False)  # 用户关闭了弹窗
    dismissed_at = Column(DateTime(timezone=True), nullable=True)

    # 交互
    clicked = Column(Boolean, default=False, nullable=False)  # 用户点击了行动按钮
    clicked_at = Column(DateTime(timezone=True), nullable=True)

    # 时间戳
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)

    # 关联关系
    user = relationship("User")
    notification = relationship("Notification", back_populates="user_notifications")

    def __repr__(self):
        return f"<UserNotification user={self.user_id} notification={self.notification_id}>"


class NotificationTemplate(Base):
    """通知模板（用于系统自动通知）"""

    __tablename__ = "notification_templates"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)

    # 基础信息
    name = Column(String(100), nullable=False, unique=True)  # 模板名称，如 "ai_task_completed"
    type = Column(
        Enum(NotificationType),
        nullable=False,
        index=True
    )

    # 模板内容（支持变量替换，如 {{username}}, {{chapter_title}}）
    title_template = Column(String(200), nullable=False)
    content_template = Column(Text, nullable=True)

    # 默认配置
    default_priority = Column(
        Enum(NotificationPriority),
        nullable=False,
        default=NotificationPriority.NORMAL
    )

    # 时间戳
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)

    def __repr__(self):
        return f"<NotificationTemplate {self.name}>"
