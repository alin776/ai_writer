"""
OpenSearch 索引同步状态模型。
用于记录章节级索引同步状态、失败重试信息和最近错误。
"""

import enum
import uuid

from sqlalchemy import Column, DateTime, Enum, ForeignKey, Index, Integer, String, Text, UniqueConstraint
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func

from app.core.database import Base


class OpenSearchSyncStatusEnum(str, enum.Enum):
    """OpenSearch 章节同步状态。"""

    PENDING = "pending"
    SYNCED = "synced"
    DESYNCED = "desynced"
    FAILED = "failed"
    DELETED = "deleted"


class OpenSearchSyncStatus(Base):
    """章节在 OpenSearch 的同步状态。"""

    __tablename__ = "opensearch_sync_statuses"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    work_id = Column(UUID(as_uuid=True), ForeignKey("works.id", ondelete="CASCADE"), nullable=False, index=True)
    chapter_id = Column(UUID(as_uuid=True), ForeignKey("chapters.id", ondelete="CASCADE"), nullable=False, index=True)
    chapter_order = Column(Integer, nullable=True)

    sync_status = Column(
        Enum(
            OpenSearchSyncStatusEnum,
            name="opensearchsyncstatus",
            values_callable=lambda x: [e.value for e in x],
        ),
        nullable=False,
        default=OpenSearchSyncStatusEnum.PENDING,
        index=True,
    )
    last_operation = Column(String(16), nullable=False, default="upsert")
    db_vector_count = Column(Integer, nullable=False, default=0)
    index_vector_count = Column(Integer, nullable=False, default=0)

    retry_count = Column(Integer, nullable=False, default=0)
    next_retry_at = Column(DateTime(timezone=True), nullable=True)
    last_synced_at = Column(DateTime(timezone=True), nullable=True)
    last_error = Column(Text, nullable=True)

    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)

    __table_args__ = (
        UniqueConstraint("chapter_id", name="uq_opensearch_sync_status_chapter"),
        Index("idx_opensearch_sync_status_retry", "sync_status", "next_retry_at"),
        Index("idx_opensearch_sync_status_work_state", "work_id", "sync_status"),
    )

