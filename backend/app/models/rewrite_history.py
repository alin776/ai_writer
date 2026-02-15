"""改写历史数据库模型"""
from sqlalchemy import Column, String, DateTime, Text, Float, Integer, Boolean, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
import uuid

from app.core.database import Base


class RewriteSession(Base):
    """改写会话表 - 记录每次改写请求"""

    __tablename__ = "rewrite_sessions"

    # 主键
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)

    # 用户信息
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)

    # 原文和上下文
    original_text = Column(Text, nullable=False)
    context_before = Column(Text, nullable=True)
    context_after = Column(Text, nullable=True)

    # 改写配置
    mode = Column(String(50), nullable=False)  # optimize, expand, compress, custom
    custom_requirement = Column(String(500), nullable=True)  # 自定义要求（仅当mode=custom时）

    # 时间戳
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False, index=True)

    # 关联关系
    user = relationship("User", backref="rewrite_sessions")
    results = relationship(
        "RewriteResult",
        back_populates="session",
        cascade="all, delete-orphan",
        order_by="RewriteResult.created_at"
    )

    def __repr__(self):
        return f"<RewriteSession {self.id} user_id={self.user_id} mode={self.mode}>"


class RewriteResult(Base):
    """改写结果表 - 记录每个模型的改写结果"""

    __tablename__ = "rewrite_results"

    # 主键
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)

    # 会话关联
    session_id = Column(UUID(as_uuid=True), ForeignKey("rewrite_sessions.id", ondelete="CASCADE"), nullable=False, index=True)

    # 模型信息
    model_name = Column(String(100), nullable=False)

    # 改写结果
    rewritten_text = Column(Text, nullable=False)
    word_count = Column(Integer, nullable=False)

    # 性能指标
    elapsed_time = Column(Float, nullable=False)  # 耗时（秒）

    # 错误信息（如果失败）
    error = Column(Text, nullable=True)

    # 用户选择
    is_selected = Column(Boolean, default=False, nullable=False)  # 用户是否选择了这个结果

    # 时间戳
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)

    # 关联关系
    session = relationship("RewriteSession", back_populates="results")

    def __repr__(self):
        return f"<RewriteResult {self.id} session_id={self.session_id} model={self.model_name}>"
