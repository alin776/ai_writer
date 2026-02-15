"""
世界观智能建议模型

记录AI生成的可关联世界观元素建议
"""

import enum
from datetime import datetime
from sqlalchemy import Column, String, Text, DateTime, Enum as SQLEnum, Float, ForeignKey, func
from sqlalchemy.dialects.postgresql import UUID, JSONB
import uuid

from app.core.database import Base


class SuggestionType(str, enum.Enum):
    """建议类型"""
    CHARACTER = "character"  # 角色
    LOCATION = "location"  # 地点
    POWER_SYSTEM = "power_system"  # 力量体系
    SETTING = "setting"  # 设定
    RELATIONSHIP = "relationship"  # 关系


class SuggestionAction(str, enum.Enum):
    """建议动作"""
    CREATE_NEW = "create_new"  # 创建新元素
    UPDATE_EXISTING = "update_existing"  # 更新现有元素
    MERGE = "merge"  # 合并元素


class SuggestionStatus(str, enum.Enum):
    """建议状态"""
    PENDING = "pending"  # 待处理
    ADOPTED = "adopted"  # 已采纳
    REJECTED = "rejected"  # 已拒绝
    IGNORED = "ignored"  # 已忽略


class WorldviewSuggestion(Base):
    """世界观智能建议表"""
    __tablename__ = "worldview_suggestions"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), nullable=False, index=True)
    job_id = Column(UUID(as_uuid=True), ForeignKey("book_analysis_jobs.id", ondelete="CASCADE"), nullable=False, index=True)
    work_id = Column(UUID(as_uuid=True))  # 关联作品ID (可选)

    # 建议内容
    suggestion_type = Column(SQLEnum(SuggestionType), nullable=False)
    action = Column(SQLEnum(SuggestionAction), default=SuggestionAction.CREATE_NEW, nullable=False)
    suggested_data = Column(JSONB, nullable=False)  # 预填充的数据

    # AI评估
    confidence_score = Column(Float)  # AI置信度 (0.0-1.0)
    reason = Column(Text)  # 建议理由

    # 用户操作
    status = Column(SQLEnum(SuggestionStatus), default=SuggestionStatus.PENDING, nullable=False, index=True)
    adopted_at = Column(DateTime(timezone=True))
    adopted_as_id = Column(UUID(as_uuid=True))  # 采纳后创建的元素ID
    user_notes = Column(Text)  # 用户备注

    # 时间戳
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    def __repr__(self):
        return f"<WorldviewSuggestion(id={self.id}, type={self.suggestion_type}, status={self.status})>"
