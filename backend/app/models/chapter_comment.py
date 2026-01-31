"""
章节评论模型
支持章节级、段落级、句子级三种评论粒度
"""
from sqlalchemy import Column, String, Integer, DateTime, Text, ForeignKey, Boolean, Enum, UniqueConstraint
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
import uuid
import enum

from app.core.database import Base


class CommentLocationType(str, enum.Enum):
    """评论位置类型"""
    CHAPTER = "chapter"      # 章节级评论
    PARAGRAPH = "paragraph"  # 段落级评论
    SENTENCE = "sentence"    # 句子级评论


class ChapterComment(Base):
    """章节评论模型"""

    __tablename__ = "chapter_comments"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    chapter_id = Column(UUID(as_uuid=True), ForeignKey("chapters.id", ondelete="CASCADE"), nullable=False, index=True)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)

    # 位置定位
    location_type = Column(
        Enum('chapter', 'paragraph', 'sentence', name='commentlocationtype'),
        nullable=False,
        default='chapter',
        comment="评论位置类型: chapter/paragraph/sentence"
    )
    paragraph_index = Column(Integer, nullable=True, comment="段落索引 (0-based)")
    sentence_index = Column(Integer, nullable=True, comment="句子索引 (段落内, 0-based)")
    quoted_text = Column(Text, nullable=True, comment="被引用的原文片段")

    # 评论内容
    content = Column(Text, nullable=False, comment="评论内容")

    # 回复支持
    parent_id = Column(UUID(as_uuid=True), ForeignKey("chapter_comments.id", ondelete="CASCADE"), nullable=True, index=True)
    reply_to_user_id = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="SET NULL"), nullable=True, comment="回复目标用户ID")

    # 互动数据
    like_count = Column(Integer, default=0, comment="点赞数")
    is_deleted = Column(Boolean, default=False, comment="是否已删除")

    # 时间戳
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # 关联关系
    chapter = relationship("Chapter", backref="chapter_comments")
    user = relationship("User", foreign_keys=[user_id], backref="chapter_comments")
    reply_to_user = relationship("User", foreign_keys=[reply_to_user_id])
    parent = relationship("ChapterComment", remote_side=[id], backref="replies")

    def __repr__(self):
        return f"<ChapterComment chapter_id={self.chapter_id} user_id={self.user_id} location={self.location_type}>"


class ChapterCommentLike(Base):
    """章节评论点赞模型"""

    __tablename__ = "chapter_comment_likes"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    comment_id = Column(UUID(as_uuid=True), ForeignKey("chapter_comments.id", ondelete="CASCADE"), nullable=False, index=True)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)

    # 唯一约束：一个用户只能对一条评论点赞一次
    __table_args__ = (
        UniqueConstraint('comment_id', 'user_id', name='uq_chapter_comment_like'),
    )

    # 关联关系
    comment = relationship("ChapterComment", backref="likes")
    user = relationship("User", backref="chapter_comment_likes")

    def __repr__(self):
        return f"<ChapterCommentLike comment_id={self.comment_id} user_id={self.user_id}>"


class ChapterCommentReportReason(str, enum.Enum):
    """举报原因"""
    SPAM = "spam"        # 垃圾广告
    ABUSE = "abuse"      # 辱骂攻击
    PORN = "porn"        # 色情低俗
    ILLEGAL = "illegal"  # 违法违规
    FALSE = "false"      # 虚假信息
    OTHER = "other"      # 其他


class ChapterCommentReport(Base):
    """章节评论举报模型"""

    __tablename__ = "chapter_comment_reports"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    comment_id = Column(UUID(as_uuid=True), ForeignKey("chapter_comments.id", ondelete="CASCADE"), nullable=False, index=True)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)

    # 举报信息
    reason = Column(
        Enum('spam', 'abuse', 'porn', 'illegal', 'false', 'other', name='chaptercommentreportreason'),
        nullable=False,
        comment="举报原因"
    )
    description = Column(Text, nullable=True, comment="详细描述")

    # 处理状态
    is_processed = Column(Boolean, default=False, comment="是否已处理")
    processed_at = Column(DateTime(timezone=True), nullable=True, comment="处理时间")
    processed_by = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="SET NULL"), nullable=True, comment="处理人")
    admin_note = Column(Text, nullable=True, comment="管理员备注")

    # 时间戳
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)

    # 唯一约束：一个用户只能对一条评论举报一次
    __table_args__ = (
        UniqueConstraint('comment_id', 'user_id', name='uq_chapter_comment_report'),
    )

    # 关联关系
    comment = relationship("ChapterComment", backref="reports")
    user = relationship("User", foreign_keys=[user_id], backref="chapter_comment_reports")
    processor = relationship("User", foreign_keys=[processed_by])

    def __repr__(self):
        return f"<ChapterCommentReport comment_id={self.comment_id} user_id={self.user_id} reason={self.reason}>"
