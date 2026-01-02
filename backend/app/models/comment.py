from sqlalchemy import Column, String, DateTime, Integer, Text, ForeignKey, Boolean, Enum
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
import uuid
import enum

from app.core.database import Base


class ReportReason(str, enum.Enum):
    """举报原因"""
    SPAM = "spam"  # 垃圾广告
    ABUSE = "abuse"  # 辱骂攻击
    PORN = "porn"  # 色情低俗
    ILLEGAL = "illegal"  # 违法违规
    FALSE = "false"  # 虚假信息
    OTHER = "other"  # 其他


class Comment(Base):
    """评论模型"""

    __tablename__ = "comments"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    work_id = Column(UUID(as_uuid=True), ForeignKey("works.id", ondelete="CASCADE"), nullable=False, index=True)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)

    # 评论内容
    content = Column(Text, nullable=False)

    # 回复相关
    parent_id = Column(UUID(as_uuid=True), ForeignKey("comments.id", ondelete="CASCADE"), nullable=True, index=True)
    reply_to_user_id = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="SET NULL"), nullable=True)

    # 点赞数
    like_count = Column(Integer, default=0, nullable=False)

    # 踩数
    dislike_count = Column(Integer, default=0, nullable=False)

    # 是否被删除（软删除）
    is_deleted = Column(Boolean, default=False, nullable=False)

    # 时间戳
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)

    # 关联关系
    work = relationship("Work", back_populates="comments")
    user = relationship("User", foreign_keys=[user_id], backref="comments")
    reply_to_user = relationship("User", foreign_keys=[reply_to_user_id])
    parent = relationship("Comment", remote_side=[id], backref="replies")
    likes = relationship("CommentLike", backref="comment", cascade="all, delete-orphan", passive_deletes=True)
    dislikes = relationship("CommentDislike", backref="comment", cascade="all, delete-orphan", passive_deletes=True)
    reports = relationship("CommentReport", backref="comment", cascade="all, delete-orphan", passive_deletes=True)

    def __repr__(self):
        return f"<Comment by user_id={self.user_id} on work_id={self.work_id}>"


class CommentLike(Base):
    """评论点赞模型"""

    __tablename__ = "comment_likes"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    comment_id = Column(UUID(as_uuid=True), ForeignKey("comments.id", ondelete="CASCADE"), nullable=False, index=True)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)

    # 时间戳
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)

    # 关联关系
    user = relationship("User", backref="comment_likes")

    def __repr__(self):
        return f"<CommentLike comment_id={self.comment_id} user_id={self.user_id}>"


class CommentDislike(Base):
    """评论踩模型"""

    __tablename__ = "comment_dislikes"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    comment_id = Column(UUID(as_uuid=True), ForeignKey("comments.id", ondelete="CASCADE"), nullable=False, index=True)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)

    # 时间戳
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)

    # 关联关系
    user = relationship("User", backref="comment_dislikes")

    def __repr__(self):
        return f"<CommentDislike comment_id={self.comment_id} user_id={self.user_id}>"


class CommentReport(Base):
    """评论举报模型"""

    __tablename__ = "comment_reports"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    comment_id = Column(UUID(as_uuid=True), ForeignKey("comments.id", ondelete="CASCADE"), nullable=False, index=True)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)

    # 举报原因
    reason = Column(Enum(ReportReason), nullable=False)
    description = Column(Text, nullable=True, comment="详细描述")

    # 处理状态
    is_processed = Column(Boolean, default=False, nullable=False, comment="是否已处理")
    processed_at = Column(DateTime(timezone=True), nullable=True, comment="处理时间")
    processed_by = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="SET NULL"), nullable=True, comment="处理人")

    # 时间戳
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)

    # 关联关系
    user = relationship("User", foreign_keys=[user_id], backref="comment_reports")
    processor = relationship("User", foreign_keys=[processed_by])

    def __repr__(self):
        return f"<CommentReport comment_id={self.comment_id} user_id={self.user_id} reason={self.reason}>"
