"""
AI评价记录模型

记录AI对生成内容的评价结果，用于质量分析和优化
"""

from sqlalchemy import Column, String, Integer, Float, DateTime, ForeignKey, Index
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
import uuid

from app.core.database import Base


class EvaluationRecord(Base):
    """AI评价记录"""

    __tablename__ = "evaluation_records"

    # 主键
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)

    # 用户信息
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)

    # 关联信息
    work_id = Column(UUID(as_uuid=True), ForeignKey("works.id", ondelete="SET NULL"), nullable=True, index=True)
    chapter_id = Column(UUID(as_uuid=True), ForeignKey("chapters.id", ondelete="SET NULL"), nullable=True, index=True)

    # 操作类型 (续写/润色/扩写/翻译/总结)
    operation_type = Column(String(50), nullable=False, index=True)

    # 评分数据
    overall_score = Column(Float, nullable=False)  # 总分 (0-100)

    # 5维度评分 (JSON格式)
    dimensions = Column(
        JSONB,
        nullable=False,
        comment="5维度评分: literary_quality, coherence, creativity, emotional_impact, pacing"
    )

    # 评价详情 (JSON格式)
    evaluation_details = Column(
        JSONB,
        nullable=False,
        default=lambda: {},
        comment="评价详情: highlights(优点), issues(问题), suggestions(建议)"
    )

    # 关联的AI调用日志ID
    ai_call_log_id = Column(UUID(as_uuid=True), ForeignKey("ai_call_logs.id", ondelete="SET NULL"), nullable=True, index=True)

    # 时间戳
    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
        index=True
    )

    # 关联关系
    user = relationship("User", backref="evaluation_records")
    work = relationship("Work", backref="evaluation_records")
    chapter = relationship("Chapter", backref="evaluation_records")
    ai_call_log = relationship("AICallLog", backref="evaluation_records")

    # 索引优化
    __table_args__ = (
        # 复合索引：按用户查询评价历史
        Index('ix_eval_user_created', 'user_id', 'created_at'),
        # 复合索引：按操作类型分析质量趋势
        Index('ix_eval_operation_created', 'operation_type', 'created_at'),
        # 复合索引：按作品查询生成质量
        Index('ix_eval_work_created', 'work_id', 'created_at'),
    )

    def __repr__(self):
        return (
            f"<EvaluationRecord(id={self.id}, user_id={self.user_id}, "
            f"operation={self.operation_type}, overall_score={self.overall_score})>"
        )
