"""
实体关系模型
用于管理角色、地点、设定之间的关系
"""
from sqlalchemy import Column, String, Integer, Text, TIMESTAMP, ARRAY, ForeignKey, CheckConstraint, func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
import uuid
from datetime import datetime

from app.core.database import Base


class EntityRelationship(Base):
    """实体关系表"""
    __tablename__ = "entity_relationships"

    # 主键
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    work_id = Column(UUID(as_uuid=True), ForeignKey("works.id", ondelete="CASCADE"), nullable=False)
    
    # 源节点
    source_id = Column(UUID(as_uuid=True), nullable=False)
    source_type = Column(String(50), nullable=False)  # 'character', 'location', 'setting'
    
    # 目标节点
    target_id = Column(UUID(as_uuid=True), nullable=False)
    target_type = Column(String(50), nullable=False)
    
    # 关系属性
    relationship_type = Column(String(100), nullable=False)  # '师徒', '好友', '敌对' 等
    label = Column(String(200), nullable=True)  # 显示标签
    description = Column(Text, nullable=True)   # 详细描述
    strength = Column(Integer, default=5)       # 关系强度 1-10
    direction = Column(String(20), default='one-way')  # 'one-way', 'two-way'
    
    # 时间线（可选）
    start_chapter_id = Column(UUID(as_uuid=True), ForeignKey("chapters.id"), nullable=True)
    end_chapter_id = Column(UUID(as_uuid=True), ForeignKey("chapters.id"), nullable=True)
    start_time = Column(TIMESTAMP, nullable=True)
    end_time = Column(TIMESTAMP, nullable=True)
    
    # 样式
    color = Column(String(20), nullable=True)   # HEX颜色
    line_style = Column(String(20), default='solid')  # 'solid', 'dashed', 'dotted'
    
    # 标签和分类
    tags = Column(ARRAY(Text), nullable=True)
    category = Column(String(100), nullable=True)
    
    # 时间戳
    created_at = Column(TIMESTAMP(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(TIMESTAMP(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)
    
    # 约束
    __table_args__ = (
        CheckConstraint("source_type IN ('character', 'location', 'setting')", name='valid_source_type'),
        CheckConstraint("target_type IN ('character', 'location', 'setting')", name='valid_target_type'),
        CheckConstraint("direction IN ('one-way', 'two-way')", name='valid_direction'),
        CheckConstraint("line_style IN ('solid', 'dashed', 'dotted')", name='valid_line_style'),
        CheckConstraint("strength BETWEEN 1 AND 10", name='valid_strength'),
    )
    
    # 关系（用于ORM级联删除）
    work = relationship("Work", back_populates="entity_relationships")
