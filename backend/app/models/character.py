from sqlalchemy import Column, String, DateTime, Text, ForeignKey, JSON
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
import uuid

from app.core.database import Base


class Character(Base):
    """人物模型"""
    
    __tablename__ = "characters"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    work_id = Column(UUID(as_uuid=True), ForeignKey("works.id", ondelete="CASCADE"), nullable=False, index=True)
    
    # 基本信息
    name = Column(String(200), nullable=False)
    avatar = Column(String(500), nullable=True)
    description = Column(Text, nullable=False)
    role = Column(String(100), nullable=True)  # 角色定位
    status = Column(String(100), nullable=True)  # 角色状态（可选）
    voice = Column(String(200), nullable=True)  # 语言/叙述声音（可选）
    
    # 扩展信息（使用JSON存储）
    tags = Column(JSON, nullable=True, default=list)  # 标签数组
    aliases = Column(JSON, nullable=True, default=list)  # 别名数组
    relationships = Column(JSON, nullable=True, default=list)  # 关系数组
    constraints = Column(JSON, nullable=True, default=list)  # 约束清单
    evidence = Column(JSON, nullable=True, default=list)  # 证据（章节/片段/来源/置信度）
    
    # 时间戳
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)
    
    # 关联关系
    work = relationship("Work", back_populates="characters")
    
    def __repr__(self):
        return f"<Character {self.name}>"
