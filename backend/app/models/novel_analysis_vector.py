"""
小说分析向量存储模型
用于存储微观分析JSON的向量表示,支持RAG检索
扩展支持知识库向量存储
"""
from sqlalchemy import Column, String, Text, Integer, ForeignKey, Index
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.orm import relationship
from pgvector.sqlalchemy import Vector
import uuid

from app.core.database import Base


class NovelAnalysisVector(Base):
    """小说分析向量存储 (扩展支持知识库)"""

    __tablename__ = "novel_analysis_vectors"

    # 主键
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)

    # 关联 (可选,支持多种来源类型)
    work_id = Column(UUID(as_uuid=True), ForeignKey("works.id", ondelete="CASCADE"), nullable=True)
    chapter_id = Column(UUID(as_uuid=True), ForeignKey("chapters.id", ondelete="CASCADE"), nullable=True)
    analysis_id = Column(UUID(as_uuid=True), ForeignKey("novel_analyses.id", ondelete="CASCADE"), nullable=True)

    # 用户关联 (知识库需要)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), nullable=True, index=True)

    # 来源类型标识 (用于区分不同用途)
    source_type = Column(String(50), nullable=False, default="novel_analysis", index=True)  # "novel_analysis" or "knowledge"
    source_id = Column(UUID(as_uuid=True), nullable=True, index=True)  # 对应的来源记录ID

    # 向量数据
    embedding = Column(Vector(512), nullable=False)  # 512维向量（bge-small-zh-v1.5 模型）

    # 原始数据
    content_text = Column(Text, nullable=False)  # 向量化的文本内容
    micro_data = Column(JSONB, nullable=True)   # 完整的数据JSON (知识库可能不需要)

    # 元数据
    chunk_index = Column(Integer, nullable=False, default=0)  # 块索引

    # 关系
    work = relationship("Work", back_populates="analysis_vectors")
    chapter = relationship("Chapter", back_populates="analysis_vectors")
    analysis = relationship("NovelAnalysis", back_populates="vectors")

    # 索引
    __table_args__ = (
        Index('idx_novel_vectors_work_id', 'work_id'),
        Index('idx_novel_vectors_chapter_id', 'chapter_id'),
        Index('idx_novel_vectors_analysis_id', 'analysis_id'),
        Index('idx_novel_vectors_user_source', 'user_id', 'source_type'),  # 知识库查询优化
        Index('idx_novel_vectors_source', 'source_type', 'source_id'),  # 通用来源查询
    )

    def __repr__(self):
        return f"<NovelAnalysisVector(source_type={self.source_type}, source_id={self.source_id})>"
