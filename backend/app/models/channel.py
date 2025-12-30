from sqlalchemy import Column, String, DateTime, Integer, Text, ForeignKey, Enum, Boolean, false
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
import uuid
import enum

from app.core.database import Base


class ChannelType(str, enum.Enum):
    """频道类型"""
    OFFICIAL = "official"  # 官方频道
    FANGROUP = "fangroup"  # 粉丝群频道
    WORK = "work"  # 作品频道


class ChannelStatus(str, enum.Enum):
    """频道状态"""
    ACTIVE = "active"  # 活跃
    WARNING = "warning"  # 警告（即将折叠）
    LOCKED = "locked"  # 已折叠


class Channel(Base):
    """频道模型"""

    __tablename__ = "channels"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)

    # 基本信息
    name = Column(String(100), nullable=False, index=True)
    description = Column(Text, nullable=True)
    cover_image = Column(String(500), nullable=True)

    # 频道类型和状态
    type = Column(Enum('official', 'fangroup', 'work', name='channeltype'), nullable=False, index=True)
    status = Column(Enum('active', 'warning', 'locked', name='channelstatus'), nullable=False, default='active')

    # 所有者信息（粉丝群频道需要）
    creator_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=True, index=True)

    # 关联作品（作品频道需要）
    work_id = Column(UUID(as_uuid=True), ForeignKey("works.id"), nullable=True, index=True)

    # 频道属性
    is_permanent = Column(Boolean, default=False, server_default=false(), nullable=False, comment="是否永久频道")
    is_pinned = Column(Boolean, default=False, server_default=false(), nullable=False, comment="是否置顶")
    trial_end_at = Column(DateTime(timezone=True), nullable=True, comment="测试期结束时间")

    # 统计信息
    member_count = Column(Integer, default=0, nullable=False, comment="成员数量")
    message_count = Column(Integer, default=0, nullable=False, comment="消息数量")

    # 活跃度追踪（用于作品频道自动折叠）
    last_message_at = Column(DateTime(timezone=True), nullable=True, comment="最后消息时间")
    warning_days = Column(Integer, nullable=True, comment="警告剩余天数")

    # 进入要求配置
    join_requirement = Column(Text, nullable=True, comment="进入要求配置(JSON)")

    # 慢速模式
    slowmode_interval = Column(Integer, nullable=True, comment="慢速模式间隔(秒)，null表示关闭")

    # 时间戳
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)
    locked_at = Column(DateTime(timezone=True), nullable=True, comment="折叠时间")

    # 关联关系
    creator = relationship("User", foreign_keys=[creator_id], back_populates="created_channels")
    work = relationship("Work", back_populates="channel")
    members = relationship("ChannelMember", back_populates="channel", cascade="all, delete-orphan")
    messages = relationship("ChannelMessage", back_populates="channel", cascade="all, delete-orphan", order_by="ChannelMessage.created_at")
    attachments = relationship("MessageAttachment", back_populates="channel", cascade="all, delete-orphan")
    invites = relationship("ChannelInvite", back_populates="channel", cascade="all, delete-orphan")
    bookmarks = relationship("MessageBookmark", back_populates="channel", cascade="all, delete-orphan")
    notification_settings = relationship("ChannelNotificationSetting", back_populates="channel", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<Channel {self.name} ({self.type})>"
