from sqlalchemy import Column, String, DateTime, Integer, Float, Text, ForeignKey, Boolean, Enum
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
import uuid
import enum

from app.core.database import Base


class VersionType(str, enum.Enum):
    """版本类型"""
    SNAPSHOT = "snapshot"      # 完整快照
    COMPRESSED = "compressed"  # diff压缩
    ARCHIVED = "archived"      # 对象存储归档


class ChapterVersion(Base):
    """章节版本模型"""

    __tablename__ = "chapter_versions"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    chapter_id = Column(UUID(as_uuid=True), ForeignKey("chapters.id"), nullable=False, index=True)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False, index=True)

    # 版本信息
    version_number = Column(Integer, nullable=False, comment="版本号")
    version_type = Column(
        Enum(VersionType, name="versiontype", values_callable=lambda x: [e.value for e in x]),
        nullable=False,
        default=VersionType.SNAPSHOT,
        comment="版本类型"
    )
    is_milestone = Column(Boolean, default=False, nullable=False, index=True, comment="是否里程碑版本")
    version_tag = Column(String(50), nullable=True, comment="版本标签: 初稿/评审后v1")
    change_summary = Column(Text, nullable=True, comment="本次修改说明")

    # 内容存储 (根据version_type决定使用哪个字段)
    content = Column(Text, nullable=True, comment="完整内容 (snapshot)")
    diff_patch = Column(Text, nullable=True, comment="diff补丁 (compressed)")
    storage_location = Column(String(200), nullable=True, comment="对象存储URL (archived)")

    # 评审数据
    review_session_id = Column(UUID(as_uuid=True), ForeignKey("review_sessions.id"), nullable=True, index=True)
    overall_score = Column(Float, nullable=True, comment="总评分")
    dimension_scores = Column(JSONB, nullable=True, comment="各维度评分")

    # 任务数据
    completed_tasks_count = Column(Integer, default=0, nullable=False, comment="已完成任务数")
    task_completion_rate = Column(Float, nullable=True, comment="任务完成率")

    # 统计数据
    word_count = Column(Integer, nullable=True, comment="字数统计")

    # 时间戳
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    archived_at = Column(DateTime(timezone=True), nullable=True, comment="归档时间")

    # 关联关系
    chapter = relationship("Chapter", back_populates="versions")
    user = relationship("User", backref="chapter_versions")
    review_session = relationship("ReviewSession", back_populates="versions")

    def __repr__(self):
        milestone = "⭐" if self.is_milestone else ""
        return f"<ChapterVersion {milestone}v{self.version_number} type={self.version_type}>"
