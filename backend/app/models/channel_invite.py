"""频道邀请链接模型"""
from sqlalchemy import Column, String, DateTime, Integer, ForeignKey, Boolean
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
import uuid
import secrets

from app.core.database import Base


def generate_invite_code():
    """生成8位随机邀请码"""
    return secrets.token_urlsafe(6)[:8]


class ChannelInvite(Base):
    """频道邀请链接模型"""

    __tablename__ = "channel_invites"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)

    # 关联信息
    channel_id = Column(UUID(as_uuid=True), ForeignKey("channels.id", ondelete="CASCADE"), nullable=False, index=True)
    creator_id = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="SET NULL"), nullable=True, index=True)

    # 邀请码
    code = Column(String(20), unique=True, nullable=False, index=True, default=generate_invite_code)

    # 使用限制
    max_uses = Column(Integer, nullable=True, comment="最大使用次数，null表示无限制")
    use_count = Column(Integer, default=0, nullable=False, comment="已使用次数")
    expires_at = Column(DateTime(timezone=True), nullable=True, comment="过期时间，null表示永不过期")

    # 状态
    is_active = Column(Boolean, default=True, nullable=False, comment="是否有效")

    # 时间戳
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)

    # 关联关系
    channel = relationship("Channel", back_populates="invites")
    creator = relationship("User", back_populates="channel_invites")

    def __repr__(self):
        return f"<ChannelInvite code={self.code} channel_id={self.channel_id}>"

    @property
    def is_valid(self):
        """检查邀请链接是否有效"""
        if not self.is_active:
            return False
        if self.max_uses and self.use_count >= self.max_uses:
            return False
        if self.expires_at:
            from datetime import datetime, timezone
            if datetime.now(timezone.utc) > self.expires_at:
                return False
        return True
