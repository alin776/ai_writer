from sqlalchemy import Column, String, DateTime, Text, ForeignKey, JSON
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
import uuid

from app.core.database import Base


class Setting(Base):
    """设定模型"""
    
    __tablename__ = "settings"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    work_id = Column(UUID(as_uuid=True), ForeignKey("works.id", ondelete="CASCADE"), nullable=False, index=True)
    
    # 基本信息
    title = Column(String(200), nullable=False)
    category = Column(String(100), nullable=True)  # 分类
    content = Column(Text, nullable=True)
    
    # 扩展信息（使用JSON存储）
    tags = Column(JSON, nullable=True, default=list)  # 标签数组
    related_items = Column(JSON, nullable=True, default=list)  # 相关项数组
    
    # 时间戳
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)
    
    # 关联关系
    work = relationship("Work", back_populates="settings")
    
    def __repr__(self):
        return f"<Setting {self.title}>"
