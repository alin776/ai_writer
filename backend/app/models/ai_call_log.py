"""
AI调用日志模型

记录每次AI API调用的详细信息，用于成本监控和使用分析
"""

from sqlalchemy import Column, String, Integer, Float, DateTime, Text, Boolean, ForeignKey, Index
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
import uuid

from app.core.database import Base


class AICallLog(Base):
    """AI调用日志"""

    __tablename__ = "ai_call_logs"

    # 主键
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)

    # 用户信息
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)

    # 调用信息
    model_name = Column(String(100), nullable=False, index=True)  # AI模型名称 (如: gpt-4, gemini-2.5-pro)
    operation_type = Column(String(50), nullable=False, index=True)  # 操作类型 (如: continue, polish, summary, translate, expand, analyze_micro, analyze_macro)

    # 关联信息
    work_id = Column(UUID(as_uuid=True), ForeignKey("works.id", ondelete="SET NULL"), nullable=True, index=True)
    chapter_id = Column(UUID(as_uuid=True), ForeignKey("chapters.id", ondelete="SET NULL"), nullable=True, index=True)
    analysis_id = Column(UUID(as_uuid=True), ForeignKey("novel_analyses.id", ondelete="SET NULL"), nullable=True, index=True)

    # Token统计
    prompt_tokens = Column(Integer, nullable=False, default=0)  # 提示词token数
    completion_tokens = Column(Integer, nullable=False, default=0)  # 生成内容token数
    total_tokens = Column(Integer, nullable=False, default=0)  # 总token数

    # 成本信息 (单位: 美元)
    prompt_cost = Column(Float, nullable=False, default=0.0)  # 提示词成本
    completion_cost = Column(Float, nullable=False, default=0.0)  # 生成内容成本
    total_cost = Column(Float, nullable=False, default=0.0)  # 总成本

    # 性能信息
    duration_ms = Column(Integer, nullable=True)  # 调用耗时(毫秒)
    is_success = Column(Boolean, nullable=False, default=True)  # 是否成功
    error_message = Column(Text, nullable=True)  # 错误信息(如果失败)

    # 额外数据 (JSON格式，用于存储请求参数、响应摘要等)
    extra_data = Column(
        JSONB,
        nullable=False,
        default=lambda: {},
        comment="额外数据，如temperature、max_tokens等参数"
    )

    # 时间戳
    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
        index=True
    )

    # 关联关系
    user = relationship("User", backref="ai_call_logs")
    work = relationship("Work", backref="ai_call_logs")
    chapter = relationship("Chapter", backref="ai_call_logs")
    analysis = relationship("NovelAnalysis", backref="ai_call_logs")

    # 索引优化
    __table_args__ = (
        # 复合索引：按用户查询成本统计
        Index('ix_ai_logs_user_created', 'user_id', 'created_at'),
        # 复合索引：按模型统计使用量
        Index('ix_ai_logs_model_created', 'model_name', 'created_at'),
        # 复合索引：按操作类型分析
        Index('ix_ai_logs_operation_created', 'operation_type', 'created_at'),
        # 复合索引：按作品查询AI使用情况
        Index('ix_ai_logs_work_created', 'work_id', 'created_at'),
    )

    def __repr__(self):
        return (
            f"<AICallLog(id={self.id}, user_id={self.user_id}, "
            f"model={self.model_name}, operation={self.operation_type}, "
            f"tokens={self.total_tokens}, cost=${self.total_cost:.6f})>"
        )
