from sqlalchemy import Column, String, DateTime, ForeignKey, DECIMAL, Boolean
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
import uuid

from app.core.database import Base


class RedeemCode(Base):
    """兑换码"""

    __tablename__ = "redeem_codes"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)

    # 兑换码信息
    code = Column(String(12), nullable=False, unique=True, index=True)
    credits = Column(DECIMAL(10, 2), nullable=False)

    # 状态
    is_used = Column(Boolean, nullable=False, default=False, index=True)
    used_by = Column(
        UUID(as_uuid=True),
        ForeignKey("users.id", ondelete="SET NULL"),
        nullable=True
    )
    used_at = Column(DateTime(timezone=True), nullable=True)

    # 有效期
    expires_at = Column(DateTime(timezone=True), nullable=True, index=True)

    # 创建信息
    created_by = Column(
        UUID(as_uuid=True),
        ForeignKey("users.id", ondelete="SET NULL"),
        nullable=True,
        index=True
    )
    remark = Column(String(255), nullable=True)

    # 时间戳
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)

    # 关联关系
    user = relationship("User", foreign_keys=[used_by], backref="used_redeem_codes")
    creator = relationship("User", foreign_keys=[created_by], backref="created_redeem_codes")

    def __repr__(self):
        return f"<RedeemCode code={self.code} credits={self.credits} is_used={self.is_used}>"
