from sqlalchemy import Column, DateTime, ForeignKey, UniqueConstraint, CheckConstraint
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import uuid

from app.core.database import Base


class Friendship(Base):
    """好友关系模型 - 双向存储"""

    __tablename__ = "friendships"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    friend_id = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    private_channel_id = Column(UUID(as_uuid=True), ForeignKey("channels.id", ondelete="SET NULL"), nullable=True, index=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)

    # 关系
    user = relationship("User", foreign_keys=[user_id])
    friend = relationship("User", foreign_keys=[friend_id])
    private_channel = relationship("Channel", foreign_keys=[private_channel_id])

    __table_args__ = (
        UniqueConstraint('user_id', 'friend_id', name='uq_friendship'),
        CheckConstraint('user_id != friend_id', name='ck_not_self_friend'),
    )

    def __repr__(self):
        return f"<Friendship {self.user_id} -> {self.friend_id}>"
