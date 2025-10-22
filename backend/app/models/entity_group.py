"""
实体分组模型
用于世界观关系图中的节点分组管理
"""
from sqlalchemy import Column, String, Integer, ForeignKey, Text, TIMESTAMP, Boolean
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import uuid

from app.core.database import Base


class EntityGroup(Base):
    """实体分组表"""
    __tablename__ = "entity_groups"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    work_id = Column(UUID(as_uuid=True), ForeignKey("works.id", ondelete="CASCADE"), nullable=False, index=True)
    
    # 分组信息
    name = Column(String(200), nullable=False)
    description = Column(Text)
    group_type = Column(String(50), nullable=False, default='manual')  # 'manual' or 'auto'
    
    # 自动分组配置（JSON格式）
    auto_rule = Column(JSONB)  # {"by": "type", "filter": {...}}
    
    # 样式
    color = Column(String(20))
    icon = Column(String(50))
    
    # 层级结构
    parent_group_id = Column(UUID(as_uuid=True), ForeignKey("entity_groups.id", ondelete="SET NULL"))
    order_index = Column(Integer, default=0)
    
    # 元数据
    created_at = Column(TIMESTAMP(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(TIMESTAMP(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)
    
    # 关联
    members = relationship("GroupMember", back_populates="group", cascade="all, delete-orphan")
    parent_group = relationship("EntityGroup", remote_side=[id], backref="child_groups")

    def __repr__(self):
        return f"<EntityGroup(id={self.id}, name={self.name}, type={self.group_type})>"


class GroupMember(Base):
    """分组成员关联表"""
    __tablename__ = "group_members"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    group_id = Column(UUID(as_uuid=True), ForeignKey("entity_groups.id", ondelete="CASCADE"), nullable=False, index=True)
    
    # 实体信息
    entity_id = Column(UUID(as_uuid=True), nullable=False, index=True)
    entity_type = Column(String(50), nullable=False)  # 'character', 'location', 'setting'
    order_index = Column(Integer, default=0)
    
    # 元数据
    created_at = Column(TIMESTAMP(timezone=True), server_default=func.now(), nullable=False)
    
    # 关联
    group = relationship("EntityGroup", back_populates="members")
    
    def __repr__(self):
        return f"<GroupMember(id={self.id}, entity_id={self.entity_id}, entity_type={self.entity_type})>"
