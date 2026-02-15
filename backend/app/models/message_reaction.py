"""
消息反应模型

用于存储用户对频道消息的 Emoji 反应
"""

from sqlalchemy import Column, String, DateTime, ForeignKey, Index, UniqueConstraint
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
import uuid

from app.core.database import Base


class MessageReaction(Base):
    """消息反应模型"""

    __tablename__ = "message_reactions"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)

    # 关联信息
    message_id = Column(
        UUID(as_uuid=True),
        ForeignKey("channel_messages.id", ondelete="CASCADE"),
        nullable=False,
        index=True
    )
    user_id = Column(
        UUID(as_uuid=True),
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
        index=True
    )

    # 反应内容（Emoji）
    emoji = Column(String(50), nullable=False)

    # 时间戳
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)

    # 关联关系
    message = relationship("ChannelMessage", back_populates="reactions")
    user = relationship("User", back_populates="message_reactions")

    # 表约束
    __table_args__ = (
        # 每个用户对同一消息的同一 emoji 只能有一个反应
        UniqueConstraint('message_id', 'user_id', 'emoji', name='uq_message_user_emoji'),
        # 索引优化
        Index('idx_reactions_message_emoji', 'message_id', 'emoji'),
    )

    def __repr__(self):
        return f"<MessageReaction id={self.id} emoji={self.emoji}>"
