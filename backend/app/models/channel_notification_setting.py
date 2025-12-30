"""频道通知设置模型"""
from sqlalchemy import Column, DateTime, ForeignKey, Boolean, UniqueConstraint
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
import uuid

from app.core.database import Base


class ChannelNotificationSetting(Base):
    """频道通知设置模型"""

    __tablename__ = "channel_notification_settings"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)

    # 关联信息
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    channel_id = Column(UUID(as_uuid=True), ForeignKey("channels.id", ondelete="CASCADE"), nullable=False, index=True)

    # 通知设置
    is_muted = Column(Boolean, default=False, nullable=False, comment="是否静音")
    mute_until = Column(DateTime(timezone=True), nullable=True, comment="静音到期时间")
    notify_mentions = Column(Boolean, default=True, nullable=False, comment="是否通知@提醒")
    notify_announcements = Column(Boolean, default=True, nullable=False, comment="是否通知公告")

    # 时间戳
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)

    # 唯一约束
    __table_args__ = (
        UniqueConstraint('user_id', 'channel_id', name='uq_user_channel_notification'),
    )

    # 关联关系
    user = relationship("User", back_populates="channel_notification_settings")
    channel = relationship("Channel", back_populates="notification_settings")

    def __repr__(self):
        return f"<ChannelNotificationSetting user_id={self.user_id} channel_id={self.channel_id}>"
