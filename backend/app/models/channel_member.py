from sqlalchemy import Column, String, DateTime, ForeignKey, Enum, Boolean, UniqueConstraint
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
import uuid
import enum

from app.core.database import Base


class MemberRole(str, enum.Enum):
    """成员角色"""
    OWNER = "owner"  # 所有者（创建者）
    ADMIN = "admin"  # 管理员
    MEMBER = "member"  # 普通成员


class ChannelMember(Base):
    """频道成员模型"""

    __tablename__ = "channel_members"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)

    # 关联信息
    channel_id = Column(UUID(as_uuid=True), ForeignKey("channels.id", ondelete="CASCADE"), nullable=False, index=True)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)

    # 成员信息
    role = Column(Enum('owner', 'admin', 'member', name='memberrole'), nullable=False, default='member')
    is_muted = Column(Boolean, default=False, nullable=False, comment="是否禁言")
    muted_until = Column(DateTime(timezone=True), nullable=True, comment="禁言到期时间")
    is_banned = Column(Boolean, default=False, nullable=False, comment="是否被封禁")

    # 用户称号（可选，显示在消息旁边）
    custom_title = Column(String(50), nullable=True, comment="自定义称号")
    title_color = Column(String(20), nullable=True, comment="称号颜色")

    # 时间戳
    joined_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    last_read_at = Column(DateTime(timezone=True), nullable=True, comment="最后阅读时间")

    # 关联关系
    channel = relationship("Channel", back_populates="members")
    user = relationship("User", back_populates="channel_memberships")

    # 唯一约束：一个用户在一个频道只能有一个成员记录
    __table_args__ = (
        UniqueConstraint('channel_id', 'user_id', name='uix_channel_user'),
    )

    def __repr__(self):
        return f"<ChannelMember user_id={self.user_id} channel_id={self.channel_id}>"
