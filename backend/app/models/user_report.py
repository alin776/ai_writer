"""用户举报模型"""
from sqlalchemy import Column, String, DateTime, Text, ForeignKey, Enum
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
import uuid
import enum

from app.core.database import Base


class UserReportReason(str, enum.Enum):
    """举报原因枚举"""
    spam = "spam"  # 垃圾信息
    harassment = "harassment"  # 骚扰行为
    inappropriate = "inappropriate"  # 不当内容
    impersonation = "impersonation"  # 冒充他人
    other = "other"  # 其他


class UserReportStatus(str, enum.Enum):
    """举报状态枚举"""
    pending = "pending"  # 待处理
    reviewed = "reviewed"  # 已审核
    dismissed = "dismissed"  # 已驳回
    actioned = "actioned"  # 已处理


class UserReport(Base):
    """用户举报"""
    __tablename__ = "user_reports"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    reporter_id = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True, comment="举报者ID")
    reported_user_id = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True, comment="被举报用户ID")
    reason = Column(Enum('spam', 'harassment', 'inappropriate', 'impersonation', 'other', name='userreportreason'), nullable=False, comment="举报原因")
    description = Column(Text, nullable=True, comment="详细描述")
    status = Column(Enum('pending', 'reviewed', 'dismissed', 'actioned', name='userreportstatus'), default='pending', nullable=False, comment="举报状态")
    reviewed_at = Column(DateTime(timezone=True), nullable=True, comment="审核时间")
    reviewed_by = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="SET NULL"), nullable=True, comment="审核人ID")
    admin_note = Column(Text, nullable=True, comment="管理员备注")

    # 时间戳
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)

    # 关系
    reporter = relationship("User", foreign_keys=[reporter_id], backref="reports_made")
    reported_user = relationship("User", foreign_keys=[reported_user_id], backref="reports_received")
    reviewer = relationship("User", foreign_keys=[reviewed_by])

    def __repr__(self):
        return f"<UserReport reporter_id={self.reporter_id} reported_user_id={self.reported_user_id} reason={self.reason}>"
