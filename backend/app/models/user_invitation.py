from sqlalchemy import Column, String, DateTime, ForeignKey, Integer, DECIMAL, CheckConstraint
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from decimal import Decimal
import uuid

from app.core.database import Base


class UserInvitation(Base):
    """用户邀请码"""

    __tablename__ = "user_invitations"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(
        UUID(as_uuid=True),
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
        index=True
    )

    # 邀请码信息
    code = Column(String(8), nullable=False, unique=True, index=True)
    max_uses = Column(Integer, nullable=False, default=10)
    used_count = Column(Integer, nullable=False, default=0)

    # 激活统计
    activated_count = Column(Integer, nullable=False, default=0)
    total_rewards = Column(DECIMAL(10, 2), nullable=False, default=Decimal("0.00"))

    # 有效期
    expires_at = Column(DateTime(timezone=True), nullable=True, index=True)

    # 时间戳
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)

    # 关联关系
    inviter = relationship("User", backref="invitations")
    usages = relationship("InvitationUsage", back_populates="invitation", cascade="all, delete-orphan")

    # 数据完整性约束
    __table_args__ = (
        CheckConstraint('used_count >= 0', name='check_used_count_non_negative'),
        CheckConstraint('used_count <= max_uses', name='check_used_count_limit'),
        CheckConstraint('activated_count >= 0', name='check_activated_count_non_negative'),
        CheckConstraint('activated_count <= used_count', name='check_activated_count_limit'),
    )

    def __repr__(self):
        return f"<UserInvitation code={self.code} user_id={self.user_id} used={self.used_count}/{self.max_uses}>"
