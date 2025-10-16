from sqlalchemy import Column, String, DateTime, Integer, Text, ForeignKey, Boolean
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
import uuid

from app.core.database import Base


class Chapter(Base):
    """章节模型"""
    
    __tablename__ = "chapters"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    work_id = Column(UUID(as_uuid=True), ForeignKey("works.id"), nullable=False, index=True)
    
    # 基本信息
    title = Column(String(200), nullable=False)
    content = Column(Text, nullable=True, default="")
    
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
    
    def __repr__(self):
        return f"<Chapter {self.title}>"
