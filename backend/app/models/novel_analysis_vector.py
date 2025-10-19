"""
小说分析向量存储模型
用于存储微观分析JSON的向量表示，支持RAG检索
"""
from sqlalchemy import Column, String, Text, Integer, ForeignKey, Index
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.orm import relationship
from pgvector.sqlalchemy import Vector
import uuid

from app.core.database import Base


class NovelAnalysisVector(Base):
    """小说分析向量存储"""
    
    __tablename__ = "novel_analysis_vectors"
    
    # 主键
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    
    # 关联
    work_id = Column(UUID(as_uuid=True), ForeignKey("works.id", ondelete="CASCADE"), nullable=False)
    chapter_id = Column(UUID(as_uuid=True), ForeignKey("chapters.id", ondelete="CASCADE"), nullable=False)
    analysis_id = Column(UUID(as_uuid=True), ForeignKey("novel_analyses.id", ondelete="CASCADE"), nullable=False)
    
    # 向量数据
    embedding = Column(Vector(384), nullable=False)  # 384维向量（MiniLM模型）
    
    # 原始数据
    content_text = Column(Text, nullable=False)  # 向量化的文本内容（JSON字符串）
    micro_data = Column(JSONB, nullable=False)   # 完整的微观分析JSON
    
    # 元数据
    chunk_index = Column(Integer, nullable=False)  # 章节内的块索引（一章可能分多块）
    
    # 关系
    work = relationship("Work", back_populates="analysis_vectors")
    chapter = relationship("Chapter", back_populates="analysis_vectors")
    analysis = relationship("NovelAnalysis", back_populates="vectors")
    
    # 索引
    __table_args__ = (
        Index('idx_novel_vectors_work_id', 'work_id'),
        Index('idx_novel_vectors_chapter_id', 'chapter_id'),
        Index('idx_novel_vectors_analysis_id', 'analysis_id'),
    )
    
    def __repr__(self):
        return f"<NovelAnalysisVector(work_id={self.work_id}, chapter_id={self.chapter_id}, chunk={self.chunk_index})>"
