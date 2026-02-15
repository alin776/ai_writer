"""消息书签模型"""
from sqlalchemy import Column, String, DateTime, ForeignKey, UniqueConstraint
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
import uuid

from app.core.database import Base


class MessageBookmark(Base):
    """消息书签模型"""

    __tablename__ = "message_bookmarks"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)

    # 关联信息
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    message_id = Column(UUID(as_uuid=True), ForeignKey("channel_messages.id", ondelete="CASCADE"), nullable=False, index=True)
    channel_id = Column(UUID(as_uuid=True), ForeignKey("channels.id", ondelete="CASCADE"), nullable=False, index=True)

    # 书签信息
    note = Column(String(500), nullable=True, comment="书签备注")

    # 时间戳
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)

    # 唯一约束
    __table_args__ = (
        UniqueConstraint('user_id', 'message_id', name='uq_user_message_bookmark'),
    )

    # 关联关系
    user = relationship("User", back_populates="message_bookmarks")
    message = relationship("ChannelMessage", back_populates="bookmarks")
    channel = relationship("Channel", back_populates="bookmarks")

    def __repr__(self):
        return f"<MessageBookmark user_id={self.user_id} message_id={self.message_id}>"
