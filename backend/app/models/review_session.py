from sqlalchemy import Column, String, DateTime, Integer, Float, ForeignKey, Enum
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
import uuid
import enum

from app.core.database import Base


class ReviewLevel(str, enum.Enum):
    """评审粒度"""
    PARAGRAPH = "paragraph"  # 段落级
    CHAPTER = "chapter"      # 章节级
    WORK = "work"            # 作品级


class ReviewType(str, enum.Enum):
    """评审深度"""
    QUICK = "quick"        # 快速评审
    STANDARD = "standard"  # 标准评审
    DEEP = "deep"          # 深度评审


class ReviewSession(Base):
    """评审会话模型"""

    __tablename__ = "review_sessions"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False, index=True)

    # 评审对象
    review_level = Column(
        Enum(ReviewLevel, name="reviewlevel", values_callable=lambda x: [e.value for e in x]),
        nullable=False,
        index=True
    )
    target_id = Column(UUID(as_uuid=True), nullable=False, index=True, comment="段落ID/章节ID/作品ID")

    # 评审结果
    overall_score = Column(Float, nullable=True, comment="总分 (0-100)")
    dimension_scores = Column(JSONB, nullable=True, comment="各维度评分")
    highlights = Column(JSONB, nullable=True, comment="优点列表")
    issues = Column(JSONB, nullable=True, comment="问题列表")
    suggestions = Column(JSONB, nullable=True, comment="改进建议")

    # 元数据
    word_count = Column(Integer, nullable=True, comment="评审文本字数")
    review_type = Column(
        Enum(ReviewType, name="reviewtype", values_callable=lambda x: [e.value for e in x]),
        nullable=False,
        default=ReviewType.STANDARD,
        comment="评审深度"
    )
    ai_model = Column(String(50), nullable=True, comment="使用的AI模型")
    ai_call_log_id = Column(UUID(as_uuid=True), ForeignKey("ai_call_logs.id"), nullable=True, comment="关联AI日志")

    # 时间戳
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)

    # 关联关系
    user = relationship("User", backref="review_sessions")
    ai_call_log = relationship("AICallLog", backref="review_sessions")
    tasks = relationship("ReviewTask", back_populates="review_session", cascade="all, delete-orphan")
    versions = relationship("ChapterVersion", back_populates="review_session")

    def __repr__(self):
        return f"<ReviewSession level={self.review_level} score={self.overall_score}>"
