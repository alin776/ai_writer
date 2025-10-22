"""
时间线事件模型
"""
from sqlalchemy import Column, String, Text, Integer, BigInteger, ForeignKey, DateTime
from sqlalchemy.dialects.postgresql import UUID, ENUM
from sqlalchemy.sql import func
import uuid

from app.core.database import Base


class TimelineEvent(Base):
    """时间线事件模型"""
    __tablename__ = "timeline_events"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    work_id = Column(UUID(as_uuid=True), ForeignKey("works.id", ondelete="CASCADE"), nullable=False)
    
    # 关联实体
    entity_id = Column(UUID(as_uuid=True), nullable=False)
    entity_type = Column(
        ENUM('character', 'location', 'setting', 'relationship', name='entity_type_enum'),
        nullable=False
    )
    
    # 事件信息
    event_type = Column(
        ENUM('milestone', 'change', 'created', 'removed', name='event_type_enum'),
        nullable=False
    )
    title = Column(String(200), nullable=False)
    description = Column(Text)
    icon = Column(String(50))  # emoji或图标名
    
    # 时间定位
    chapter_id = Column(UUID(as_uuid=True), ForeignKey("chapters.id", ondelete="SET NULL"))
    chapter_number = Column(Integer)
    timestamp = Column(BigInteger)  # 时间线上的位置（可计算）
    
    # 样式
    color = Column(String(20))
    
    # 元数据
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
