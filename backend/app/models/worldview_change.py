"""
世界观变更记录（pending / applied / rejected）

用于“回写闭环”记录：新事实 -> pending -> 用户确认 -> 落库 -> 版本递增
"""
import enum
import uuid
from sqlalchemy import Column, String, Text, DateTime, Enum as SQLEnum, Integer, ForeignKey, func
from sqlalchemy.dialects.postgresql import UUID, JSONB

from app.core.database import Base


class WorldviewChangeStatus(str, enum.Enum):
    """变更状态"""
    PENDING = "pending"
    APPLIED = "applied"
    REJECTED = "rejected"


class WorldviewChange(Base):
    """世界观变更记录表"""
    __tablename__ = "worldview_changes"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    work_id = Column(UUID(as_uuid=True), ForeignKey("works.id", ondelete="CASCADE"), nullable=False, index=True)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False, index=True)
    applied_by = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=True, index=True)

    status = Column(
        SQLEnum(WorldviewChangeStatus, name="worldviewchangestatus"),
        default=WorldviewChangeStatus.PENDING,
        nullable=False,
        index=True
    )
    source = Column(String(50), nullable=True, default="manual")  # extract/scan/consistency/manual/other

    changes = Column(JSONB, nullable=False)  # 世界观变化内容（同 WorldviewChangesResponse 结构）
    selected_items = Column(JSONB, nullable=True)  # 用户选择应用的条目
    evidence = Column(JSONB, nullable=True)  # 证据/来源信息
    user_notes = Column(Text, nullable=True)

    version_before = Column(Integer, nullable=True)
    version_after = Column(Integer, nullable=True)
    apply_stats = Column(JSONB, nullable=True)

    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    applied_at = Column(DateTime(timezone=True), nullable=True)

    def __repr__(self):
        return f"<WorldviewChange(id={self.id}, status={self.status}, work_id={self.work_id})>"
