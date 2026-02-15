"""频道消息附件模型"""
from sqlalchemy import Column, String, DateTime, Integer, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
import uuid

from app.core.database import Base


class MessageAttachment(Base):
    """消息附件模型"""

    __tablename__ = "message_attachments"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)

    # 关联信息
    message_id = Column(UUID(as_uuid=True), ForeignKey("channel_messages.id", ondelete="CASCADE"), nullable=True, index=True)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="SET NULL"), nullable=True, index=True)
    channel_id = Column(UUID(as_uuid=True), ForeignKey("channels.id", ondelete="CASCADE"), nullable=False, index=True)

    # 文件信息
    file_name = Column(String(255), nullable=False, comment="原始文件名")
    file_type = Column(String(100), nullable=False, comment="MIME类型")
    file_size = Column(Integer, nullable=False, comment="文件大小(字节)")
    file_url = Column(String(500), nullable=False, comment="COS存储URL")
    thumbnail_url = Column(String(500), nullable=True, comment="缩略图URL(图片)")

    # 时间戳
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)

    # 关联关系
    message = relationship("ChannelMessage", back_populates="attachments")
    user = relationship("User", back_populates="message_attachments")
    channel = relationship("Channel", back_populates="attachments")

    def __repr__(self):
        return f"<MessageAttachment id={self.id} file_name={self.file_name}>"
