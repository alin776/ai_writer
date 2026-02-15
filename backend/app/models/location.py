from sqlalchemy import Column, String, DateTime, Text, ForeignKey, JSON
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
import uuid

from app.core.database import Base


class Location(Base):
    """地点模型"""
    
    __tablename__ = "locations"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    work_id = Column(UUID(as_uuid=True), ForeignKey("works.id", ondelete="CASCADE"), nullable=False, index=True)
    
    # 基本信息
    name = Column(String(200), nullable=False)
    image = Column(String(500), nullable=True)
    description = Column(Text, nullable=False)
    type = Column(String(100), nullable=True)  # 类型：城市、建筑、自然等
    
    # 扩展信息（使用JSON存储）
    tags = Column(JSON, nullable=True, default=list)  # 标签数组
    related_locations = Column(JSON, nullable=True, default=list)  # 相关地点ID数组
    
    # 时间戳
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)
    
    # 关联关系
    work = relationship("Work", back_populates="locations")
    
    def __repr__(self):
        return f"<Location {self.name}>"
