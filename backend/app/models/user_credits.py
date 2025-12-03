from sqlalchemy import Column, DateTime, ForeignKey, DECIMAL, CheckConstraint
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from decimal import Decimal
import uuid

from app.core.database import Base


class UserCredits(Base):
    """用户积分"""

    __tablename__ = "user_credits"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(
        UUID(as_uuid=True),
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
        unique=True,
        index=True
    )

    # 积分信息
    balance = Column(DECIMAL(10, 2), nullable=False, default=Decimal("0.00"))
    total_recharged = Column(DECIMAL(10, 2), nullable=False, default=Decimal("0.00"))
    total_consumed = Column(DECIMAL(10, 2), nullable=False, default=Decimal("0.00"))
    total_gifted = Column(DECIMAL(10, 2), nullable=False, default=Decimal("0.00"))

    # 有效期
    expires_at = Column(DateTime(timezone=True), nullable=True)

    # 时间戳
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)

    # 关联关系
    # ✅ 修复overlaps警告：这个关系只读User，不会冲突
    user = relationship("User", backref="credits")
    # ✅ 修复: 显式指定通过 user_id 关联，并声明与User.credit_transactions重叠
    transactions = relationship(
        "CreditTransaction",
        foreign_keys="[CreditTransaction.user_id]",
        primaryjoin="UserCredits.user_id == CreditTransaction.user_id",
        back_populates="user_credits",
        cascade="all, delete-orphan",
        overlaps="credit_transactions"
    )

    # 数据完整性约束
    __table_args__ = (
        CheckConstraint('balance >= 0', name='check_balance_non_negative'),
        CheckConstraint('total_recharged >= 0', name='check_recharged_non_negative'),
        CheckConstraint('total_consumed >= 0', name='check_consumed_non_negative'),
        CheckConstraint('total_gifted >= 0', name='check_gifted_non_negative'),
    )

    def __repr__(self):
        return f"<UserCredits user_id={self.user_id} balance={self.balance}>"
