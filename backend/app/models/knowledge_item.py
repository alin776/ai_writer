from sqlalchemy import Column, String, DateTime, Integer, Text, ForeignKey, Enum
from sqlalchemy.dialects.postgresql import UUID, JSONB, ARRAY
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
import uuid
import enum

from app.core.database import Base


class KnowledgeCategory(str, enum.Enum):
    """知识条目分类"""
    CHARACTER = "character"  # 人物设定
    WORLDVIEW = "worldview"  # 世界观
    PLOT = "plot"  # 情节灵感
    DIALOGUE = "dialogue"  # 对话金句
    DESCRIPTION = "description"  # 场景描写
    TECHNIQUE = "technique"  # 写作技巧
    REFERENCE = "reference"  # 参考资料
    OTHER = "other"  # 其他


class KnowledgeSource(str, enum.Enum):
    """知识来源类型"""
    MANUAL = "manual"  # 手动创建
    BOOK_ANALYSIS = "book_analysis"  # AI拆书
    AI_GENERATED = "ai_generated"  # AI生成
    IMPORTED = "imported"  # 导入


class KnowledgeItem(Base):
    """知识条目模型"""

    __tablename__ = "knowledge_items"

    # 主键
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False, index=True)

    # 基本信息
    title = Column(String(200), nullable=False, index=True)
    content = Column(Text, nullable=False)
    summary = Column(Text, nullable=True)  # MVP可为空,Week 2 AI生成

    # 分类和标签
    category = Column(Enum(KnowledgeCategory), nullable=False, index=True)
    tags = Column(ARRAY(String), nullable=False, server_default='{}')

    # 来源信息
    source_type = Column(Enum(KnowledgeSource), nullable=False, default=KnowledgeSource.MANUAL)
    source_id = Column(UUID(as_uuid=True), nullable=True)  # 来源ID (如book_analysis_id)
    source_reference = Column(String(500), nullable=True)  # 来源描述 (书名/网址等)

    # 关联作品 (可选)
    work_id = Column(UUID(as_uuid=True), ForeignKey("works.id"), nullable=True, index=True)
    chapter_id = Column(UUID(as_uuid=True), ForeignKey("chapters.id"), nullable=True, index=True)

    # 扩展信息
    extra_data = Column(JSONB, nullable=False, server_default='{}')  # 灵活存储额外信息(避免使用metadata保留字)

    # 使用统计
    view_count = Column(Integer, default=0, nullable=False)
    reference_count = Column(Integer, default=0, nullable=False)

    # 时间戳
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)
    last_accessed_at = Column(DateTime(timezone=True), nullable=True)

    # 关联关系
    user = relationship("User", back_populates="knowledge_items")
    work = relationship("Work", back_populates="knowledge_items")
    chapter = relationship("Chapter", back_populates="knowledge_items")
