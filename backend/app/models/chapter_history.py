"""
章节历史记录模型 - 用于Agent编辑自动备份
"""
from sqlalchemy import Column, String, DateTime, Integer, Text, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
import uuid

from app.core.database import Base


class ChapterHistory(Base):
    """章节历史记录模型"""

    __tablename__ = "chapter_histories"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    chapter_id = Column(UUID(as_uuid=True), ForeignKey("chapters.id", ondelete="CASCADE"), nullable=False, index=True)

    # 内容快照
    content = Column(Text, nullable=False)
    word_count = Column(Integer, default=0)

    # 版本信息
    version = Column(Integer, nullable=False)
    modified_by = Column(String(50), nullable=False)  # "user" | "agent"
    operation = Column(String(50), nullable=True)  # "append" | "replace" | "insert" | "manual"
    description = Column(String(500), nullable=True)  # 操作描述

    # 时间戳
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)

    # 关联关系
    chapter = relationship("Chapter", back_populates="histories")

    def __repr__(self):
        return f"<ChapterHistory chapter_id={self.chapter_id} version={self.version} modified_by={self.modified_by}>"
