from sqlalchemy import Column, DateTime, ForeignKey, Index, Integer
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
import uuid

from app.core.database import Base


class ChannelReadState(Base):
    """频道已读状态模型"""
    __tablename__ = "channel_read_states"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)

    # 关联信息
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    channel_id = Column(UUID(as_uuid=True), ForeignKey("channels.id", ondelete="CASCADE"), nullable=False)

    # 已读位置（最后一条已读消息的ID）
    last_read_message_id = Column(UUID(as_uuid=True), ForeignKey("channel_messages.id", ondelete="SET NULL"), nullable=True)

    # 统计信息
    unread_count = Column(Integer, default=0, nullable=False, comment="未读消息数")
    mention_count = Column(Integer, default=0, nullable=False, comment="@我的消息数")

    # 时间戳
    last_read_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)

    # 关系
    user = relationship("User")
    channel = relationship("Channel")
    last_read_message = relationship("ChannelMessage", foreign_keys=[last_read_message_id])

    # 复合索引：确保每个用户在每个频道只有一条记录
    __table_args__ = (
        Index('idx_user_channel', 'user_id', 'channel_id', unique=True),
    )

    def __repr__(self):
        return f"<ChannelReadState user_id={self.user_id} channel_id={self.channel_id}>"
