from sqlalchemy import Column, String, DateTime, ForeignKey, UniqueConstraint, CheckConstraint
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import uuid

from app.core.database import Base


class FriendRequest(Base):
    """好友请求模型"""

    __tablename__ = "friend_requests"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    from_user_id = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    to_user_id = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    message = Column(String(200), nullable=True, comment="请求消息")
    status = Column(String(20), default='pending', nullable=False, index=True, comment="状态: pending/accepted/rejected")
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)

    # 关系
    from_user = relationship("User", foreign_keys=[from_user_id])
    to_user = relationship("User", foreign_keys=[to_user_id])

    __table_args__ = (
        UniqueConstraint('from_user_id', 'to_user_id', name='uq_friend_request'),
        CheckConstraint('from_user_id != to_user_id', name='ck_not_self_request'),
        CheckConstraint("status IN ('pending', 'accepted', 'rejected')", name='ck_valid_status'),
    )

    def __repr__(self):
        return f"<FriendRequest {self.from_user_id} -> {self.to_user_id} ({self.status})>"
