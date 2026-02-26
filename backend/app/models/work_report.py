"""
小说举报模型
"""
from sqlalchemy import Column, String, DateTime, Text, ForeignKey, Boolean, Enum
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship, backref
import uuid
import enum

from app.core.database import Base


class WorkReportReason(str, enum.Enum):
    """小说举报原因"""
    SPAM = "spam"  # 垃圾广告
    PORN = "porn"  # 色情低俗
    ILLEGAL = "illegal"  # 违法违规
    PLAGIARISM = "plagiarism"  # 抄袭侵权
    FALSE = "false"  # 虚假信息
    OTHER = "other"  # 其他


class WorkReportStatus(str, enum.Enum):
    """举报处理状态"""
    PENDING = "pending"  # 待处理
    REVIEWED = "reviewed"  # 已审核
    DISMISSED = "dismissed"  # 已驳回
    ACTIONED = "actioned"  # 已处理


class WorkReport(Base):
    """小说举报模型"""

    __tablename__ = "work_reports"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    work_id = Column(UUID(as_uuid=True), ForeignKey("works.id", ondelete="CASCADE"), nullable=False, index=True)
    reporter_id = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)

    # 举报原因
    reason = Column(Enum('spam', 'porn', 'illegal', 'plagiarism', 'false', 'other', name='workreportreason'), nullable=False)
    description = Column(Text, nullable=True, comment="详细描述")

    # 处理状态
    status = Column(Enum('pending', 'reviewed', 'dismissed', 'actioned', name='workreportstatus'), default='pending', nullable=False, comment="处理状态")
    action_taken = Column(String(50), nullable=True, comment="采取的措施: warn, delete, ban")
    admin_note = Column(Text, nullable=True, comment="管理员备注")

    # 处理信息
    reviewed_at = Column(DateTime(timezone=True), nullable=True, comment="处理时间")
    reviewed_by = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="SET NULL"), nullable=True, comment="处理人")

    # 时间戳
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)

    # 关联关系
    work = relationship("Work", backref=backref("reports", passive_deletes=True))
    reporter = relationship("User", foreign_keys=[reporter_id], backref="work_reports_submitted")
    reviewer = relationship("User", foreign_keys=[reviewed_by])

    def __repr__(self):
        return f"<WorkReport work_id={self.work_id} reporter_id={self.reporter_id} reason={self.reason}>"
