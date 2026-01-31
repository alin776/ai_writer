"""
章节内容向量存储模型
用于RAG续写上下文检索，与分析向量解耦
"""
from sqlalchemy import Column, String, Text, Integer, ForeignKey, Index, DateTime
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from pgvector.sqlalchemy import Vector
import uuid

from app.core.database import Base


class NovelChapterVector(Base):
    """章节内容向量存储 - 专门用于RAG续写"""

    __tablename__ = "novel_chapter_vectors"

    # 主键
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)

    # 关联
    work_id = Column(UUID(as_uuid=True), ForeignKey("works.id", ondelete="CASCADE"), nullable=False, index=True)
    chapter_id = Column(UUID(as_uuid=True), ForeignKey("chapters.id", ondelete="CASCADE"), nullable=False, index=True)

    # 章节元数据（冗余，便于查询）
    chapter_order = Column(Integer, nullable=False, index=True)  # 🔑 关键：支持时序过滤
    chapter_title = Column(String(255), nullable=False)

    # 内容分段
    chunk_index = Column(Integer, nullable=False, default=0)  # 段落索引
    chunk_text = Column(Text, nullable=False)  # 原文内容

    # 向量数据
    embedding = Column(Vector(384), nullable=False)  # 384维向量（MiniLM模型）

    # 时间戳
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)

    # 关系
    work = relationship("Work", back_populates="chapter_vectors")
    chapter = relationship("Chapter", back_populates="chapter_vectors")

    # 索引
    __table_args__ = (
        Index('idx_chapter_vectors_work_order', 'work_id', 'chapter_order'),  # 时序查询优化
        Index('idx_chapter_vectors_chapter_chunks', 'chapter_id', 'chunk_index'),  # 章节段落查询
    )

    def __repr__(self):
        return f"<NovelChapterVector(chapter={self.chapter_title}, order={self.chapter_order}, chunk={self.chunk_index})>"
