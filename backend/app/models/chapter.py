from sqlalchemy import Column, String, DateTime, Integer, Text, ForeignKey, Boolean, Enum
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
import uuid
import enum

from app.core.database import Base


class ChapterStatus(str, enum.Enum):
    """章节状态"""
    DRAFT = "draft"       # 草稿
    PUBLISHED = "published"  # 已发布
    ARCHIVED = "archived"    # 已归档


class Chapter(Base):
    """章节模型"""
    
    __tablename__ = "chapters"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    work_id = Column(UUID(as_uuid=True), ForeignKey("works.id"), nullable=False, index=True)
    
    # 基本信息
    title = Column(String(200), nullable=False)
    content = Column(Text, nullable=True, default="")
    summary = Column(Text, nullable=True, comment="章节剧情概括")
    status = Column(
        Enum(ChapterStatus, name="chapterstatus", values_callable=lambda x: [e.value for e in x]),
        nullable=False,
        default=ChapterStatus.DRAFT,
        index=True
    )
    
    # 排序和状态
    order = Column(Integer, nullable=False, index=True)
    is_published = Column(Boolean, default=False, nullable=False)
    
    # 统计信息
    word_count = Column(Integer, default=0, nullable=False)
    view_count = Column(Integer, default=0, nullable=False)
    
    # 时间戳
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)
    published_at = Column(DateTime(timezone=True), nullable=True)
    
    # 关联关系
    work = relationship("Work", back_populates="chapters")
    analysis_vectors = relationship("NovelAnalysisVector", back_populates="chapter", cascade="all, delete-orphan")
    knowledge_items = relationship("KnowledgeItem", back_populates="chapter", cascade="all, delete-orphan")
    
    def __repr__(self):
        return f"<Chapter {self.title} status={self.status}>"
