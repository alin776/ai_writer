from sqlalchemy import Column, String, DateTime, ForeignKey, Index
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
import uuid

from app.core.database import Base


class InvitationUsage(Base):
    """邀请使用记录"""

    __tablename__ = "invitation_usages"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    invitation_id = Column(
        UUID(as_uuid=True),
        ForeignKey("user_invitations.id", ondelete="CASCADE"),
        nullable=False,
        index=True
    )
    invitee_id = Column(
        UUID(as_uuid=True),
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
        unique=True,  # 每个用户只能被邀请一次
        index=True
    )

    # 防刷信息
    ip_address = Column(String(45), nullable=True)  # 支持IPv6
    device_fingerprint = Column(String(255), nullable=True)

    # 激活状态
    status = Column(String(20), nullable=False, default="pending", index=True)  # pending/active/expired
    activated_at = Column(DateTime(timezone=True), nullable=True)

    # 时间戳
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)

    # 关联关系
    invitation = relationship("UserInvitation", back_populates="usages")
    invitee = relationship("User", backref="invitation_record")

    # 复合索引（用于防刷检查）
    __table_args__ = (
        Index('ix_invitation_usages_ip_time', 'ip_address', 'created_at'),
        Index('ix_invitation_usages_device_time', 'device_fingerprint', 'created_at'),
    )

    def __repr__(self):
        return f"<InvitationUsage invitation_id={self.invitation_id} invitee_id={self.invitee_id} status={self.status}>"
