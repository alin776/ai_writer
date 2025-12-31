from sqlalchemy import Column, String, DateTime, ForeignKey, Enum, Text, UniqueConstraint
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
import uuid
import enum

from app.core.database import Base


class JoinRequestStatus(str, enum.Enum):
    """申请状态"""
    PENDING = "pending"  # 待审核
    APPROVED = "approved"  # 已通过
    REJECTED = "rejected"  # 已拒绝


class ChannelJoinRequest(Base):
    """频道加入申请模型"""

    __tablename__ = "channel_join_requests"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)

    # 关联信息
    channel_id = Column(UUID(as_uuid=True), ForeignKey("channels.id", ondelete="CASCADE"), nullable=False, index=True)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)

    # 申请信息
    message = Column(Text, nullable=True, comment="申请留言")
    status = Column(
        Enum('pending', 'approved', 'rejected', name='joinrequeststatus'),
        nullable=False,
        default='pending',
        index=True
    )

    # 审批信息
    reviewed_by = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="SET NULL"), nullable=True)
    reviewed_at = Column(DateTime(timezone=True), nullable=True)
    reject_reason = Column(Text, nullable=True, comment="拒绝原因")

    # 时间戳
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)

    # 关联关系
    channel = relationship("Channel", foreign_keys=[channel_id])
    user = relationship("User", foreign_keys=[user_id])
    reviewer = relationship("User", foreign_keys=[reviewed_by])

    # 注意：不使用唯一约束，因为用户可能被拒绝多次后重新申请
    # 改为在代码中检查是否有 pending 申请

    def __repr__(self):
        return f"<ChannelJoinRequest user_id={self.user_id} channel_id={self.channel_id} status={self.status}>"
