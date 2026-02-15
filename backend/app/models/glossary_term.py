"""
术语表模型（世界观术语）
"""
from sqlalchemy import Column, String, DateTime, Text, ForeignKey, JSON
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
import uuid

from app.core.database import Base


class GlossaryTerm(Base):
    """术语表模型"""

    __tablename__ = "glossary_terms"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    work_id = Column(UUID(as_uuid=True), ForeignKey("works.id", ondelete="CASCADE"), nullable=False, index=True)

    # 基本信息
    term = Column(String(200), nullable=False)
    definition = Column(Text, nullable=False)

    # 扩展信息
    aliases = Column(JSON, nullable=True, default=list)  # 别名数组
    tags = Column(JSON, nullable=True, default=list)  # 标签数组
    evidence = Column(JSON, nullable=True, default=list)  # 证据（章节/片段/来源/置信度）

    # 时间戳
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)

    # 关联关系
    work = relationship("Work", back_populates="glossary_terms")

    def __repr__(self):
        return f"<GlossaryTerm {self.term}>"
