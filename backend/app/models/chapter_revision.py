from sqlalchemy import Column, String, DateTime, Integer, Text, ForeignKey, Enum
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
import uuid
import enum

from app.core.database import Base


class ChapterRevisionStatus(str, enum.Enum):
    """Revision status for chapter edits."""

    PENDING = "pending"
    ACCEPTED = "accepted"
    DISCARDED = "discarded"
    CONFLICT = "conflict"


class ChapterRevision(Base):
    """Pending revision created by agent edits."""

    __tablename__ = "chapter_revisions"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    request_id = Column(String(64), unique=True, nullable=False, index=True)

    work_id = Column(UUID(as_uuid=True), ForeignKey("works.id", ondelete="CASCADE"), nullable=False, index=True)
    chapter_id = Column(UUID(as_uuid=True), ForeignKey("chapters.id", ondelete="CASCADE"), nullable=False, index=True)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=True, index=True)

    status = Column(
        Enum(ChapterRevisionStatus, name="chapterrevisionstatus", values_callable=lambda x: [e.value for e in x]),
        nullable=False,
        default=ChapterRevisionStatus.PENDING,
        index=True
    )

    operation = Column(String(20), nullable=False)
    original_text = Column(Text, nullable=True)
    new_text = Column(Text, nullable=False)

    position = Column(JSONB, nullable=True)
    before_anchor = Column(Text, nullable=True)
    after_anchor = Column(Text, nullable=True)
    node_id = Column(String(64), nullable=True)
    paragraph_index = Column(Integer, nullable=True)
    base_version = Column(Integer, nullable=True)

    description = Column(Text, nullable=True)

    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)
    applied_at = Column(DateTime(timezone=True), nullable=True)

    chapter = relationship("Chapter", back_populates="revisions")

    def __repr__(self):
        return f"<ChapterRevision {self.id} status={self.status} operation={self.operation}>"
