from sqlalchemy import Column, String, DateTime, Integer, Text, ForeignKey, Enum, Boolean
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
import uuid
import enum

from app.core.database import Base


class MessageType(str, enum.Enum):
    """消息类型"""
    NORMAL = "normal"  # 普通消息
    ANNOUNCEMENT = "announcement"  # 公告
    MENTION = "mention"  # @消息


class ChannelMessage(Base):
    """频道消息模型"""

    __tablename__ = "channel_messages"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)

    # 关联信息
    channel_id = Column(UUID(as_uuid=True), ForeignKey("channels.id", ondelete="CASCADE"), nullable=False, index=True)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="SET NULL"), nullable=True, index=True)

    # 消息内容
    content = Column(Text, nullable=False)
    type = Column(Enum('normal', 'announcement', 'mention', name='messagetype'), nullable=False, default='normal')

    # 消息属性
    is_pinned = Column(Boolean, default=False, nullable=False, comment="是否置顶")
    is_deleted = Column(Boolean, default=False, nullable=False, comment="是否已删除")

    # 引用消息（回复功能）
    reply_to_id = Column(UUID(as_uuid=True), ForeignKey("channel_messages.id", ondelete="SET NULL"), nullable=True)

    # 统计信息
    reaction_count = Column(Integer, default=0, nullable=False, comment="反应数量")

    # 时间戳
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False, index=True)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)
    deleted_at = Column(DateTime(timezone=True), nullable=True)

    # 关联关系
    channel = relationship("Channel", back_populates="messages")
    user = relationship("User", back_populates="channel_messages")
    reply_to = relationship("ChannelMessage", remote_side=[id], backref="replies")
    reports = relationship("MessageReport", back_populates="message", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<ChannelMessage id={self.id} channel_id={self.channel_id}>"
