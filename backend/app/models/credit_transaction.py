from sqlalchemy import Column, String, DateTime, ForeignKey, DECIMAL, Index
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
import uuid

from app.core.database import Base


class CreditTransaction(Base):
    """积分变动记录"""

    __tablename__ = "credit_transactions"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(
        UUID(as_uuid=True),
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
        index=True
    )

    # 交易信息
    type = Column(String(20), nullable=False, index=True)  # recharge/consume/gift/expire/refund
    amount = Column(DECIMAL(10, 2), nullable=False)
    balance_before = Column(DECIMAL(10, 2), nullable=False)
    balance_after = Column(DECIMAL(10, 2), nullable=False)

    # 描述
    description = Column(String(255), nullable=True)

    # 关联
    related_type = Column(String(50), nullable=True)  # ai_call/redeem_code/admin_gift/new_user
    related_id = Column(UUID(as_uuid=True), nullable=True)

    # 时间戳
    created_at = Column(DateTime(timezone=True), server_default=func.now(), index=True, nullable=False)

    # 关联关系
    # ✅ 修复overlaps警告1: 与user_credits关系重叠（都操作user_id）
    user = relationship("User", backref="credit_transactions", overlaps="user_credits")
    # ✅ 修复overlaps警告2: 与user关系重叠（都操作user_id）
    user_credits = relationship(
        "UserCredits",
        foreign_keys="[CreditTransaction.user_id]",
        primaryjoin="CreditTransaction.user_id == UserCredits.user_id",
        back_populates="transactions",
        overlaps="user,credit_transactions"
    )

    # 复合索引
    __table_args__ = (
        Index('ix_credit_trans_user_created', 'user_id', 'created_at'),
    )

    def __repr__(self):
        return f"<CreditTransaction user_id={self.user_id} type={self.type} amount={self.amount}>"
