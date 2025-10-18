from sqlalchemy import Column, String, DateTime, Text, ForeignKey, Integer
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
import uuid

from app.core.database import Base


class WorkGuidelines(Base):
    """作品规范模型"""
    
    __tablename__ = "work_guidelines"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    work_id = Column(UUID(as_uuid=True), ForeignKey("works.id", ondelete="CASCADE"), nullable=False, unique=True, index=True)
    
    # 基本信息
    outline = Column(Text, nullable=True)  # 大纲流程
    style = Column(String(200), nullable=True)  # 整体风格
    tone = Column(String(200), nullable=True)  # 语言风格
    
    # 写作规范
    words_per_chapter = Column(Integer, nullable=True)  # 每章字数
    update_frequency = Column(String(100), nullable=True)  # 更新频率
    
    # 设定约束
    power_system = Column(Text, nullable=True)  # 力量体系
    world_rules = Column(Text, nullable=True)  # 世界规则
    
    # 创作目标
    target_audience = Column(String(200), nullable=True)  # 目标读者
    main_theme = Column(String(200), nullable=True)  # 主题
    plot_direction = Column(Text, nullable=True)  # 剧情走向
    
    # 其他
    notes = Column(Text, nullable=True)  # 备注
    
    # 时间戳
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)
    
    # 关联关系
    work = relationship("Work", back_populates="guidelines", uselist=False)
    
    def __repr__(self):
        return f"<WorkGuidelines for work_id={self.work_id}>"
