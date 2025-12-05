from sqlalchemy import Column, String, DateTime, Boolean, Float, Integer, ForeignKey, Index, text, Text
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
import uuid

from app.core.database import Base


class HumanizeSession(Base):
    """去痕迹会话模型 - 核心数据,永久保存"""

    __tablename__ = "humanize_sessions"

    # 主键
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)

    # 关联用户
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)

    # 使用场景
    ai_function = Column(String(50), nullable=False, index=True)  # complete/polish/expand/translate/summarize/rewrite

    # 核心指标
    score_before = Column(Float, nullable=False)  # 去痕迹前AI特征分数 (0-100)
    score_after = Column(Float, nullable=False)   # 去痕迹后AI特征分数 (0-100)
    improvement = Column(Float, nullable=False)   # 改进幅度 (score_before - score_after)

    # 去痕迹强度
    intensity = Column(String(20), nullable=False, server_default="medium")  # light/medium/strong

    # 用户反馈
    user_accepted = Column(Boolean, nullable=True)  # 用户是否接受结果 (null=未反馈)

    # 性能指标
    processing_time = Column(Float, nullable=False)  # 处理耗时(秒)
    tokens_used = Column(Integer, nullable=False)    # 消耗token数
    cost = Column(Float, nullable=False)             # 成本(美元)

    # 时间戳
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False, index=True)

    # 复合索引（优化查询性能）
    __table_args__ = (
        Index('idx_humanize_user_created', 'user_id', 'created_at'),  # 用户历史查询
    )

    # 关联关系
    user = relationship("User", backref="humanize_sessions")
    detail = relationship("HumanizeSessionDetail", back_populates="session", uselist=False, cascade="all, delete-orphan")

    def __repr__(self):
        return f"<HumanizeSession {self.id} - {self.ai_function} - {self.improvement:.1f}分改进>"


class HumanizeSessionDetail(Base):
    """去痕迹会话详情 - 详情数据,7天后自动清理"""

    __tablename__ = "humanize_session_details"

    # 主键
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)

    # 关联会话
    session_id = Column(UUID(as_uuid=True), ForeignKey("humanize_sessions.id", ondelete="CASCADE"), nullable=False, unique=True, index=True)

    # 七维度评分详情 (JSON格式) - V2优化版
    dimensions_before = Column(
        JSONB,
        nullable=False,
        server_default=text("'{}'::jsonb"),
        comment="去痕迹前7维度评分: pattern_repetition, word_choice, sentence_structure, tone_style, formatting, emotional_expression, coherence_flow"
    )
    dimensions_after = Column(
        JSONB,
        nullable=False,
        server_default=text("'{}'::jsonb"),
        comment="去痕迹后7维度评分（验证阶段暂不返回详细维度）"
    )

    # 检测到的AI痕迹 (JSON数组)
    detected_patterns = Column(
        JSONB,
        nullable=False,
        server_default=text("'[]'::jsonb"),
        comment="检测到的AI痕迹列表"
    )

    # 文本预览 (仅保存前100字)
    original_preview = Column(String(200), nullable=True)    # 原文前100字
    humanized_preview = Column(String(200), nullable=True)   # 改写后前100字

    # 全量文本（可选，受存储策略控制）
    original_full = Column(Text, nullable=True)
    humanized_full = Column(Text, nullable=True)

    # 过期时间 (7天后自动清理)
    expires_at = Column(DateTime(timezone=True), nullable=False, index=True)

    # 时间戳
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)

    # 关联关系
    session = relationship("HumanizeSession", back_populates="detail")

    def __repr__(self):
        return f"<HumanizeSessionDetail {self.session_id}>"
