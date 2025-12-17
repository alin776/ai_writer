from sqlalchemy import Column, String, DateTime, Integer, Text, ForeignKey, Enum
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
import uuid
import enum

from app.core.database import Base


class TaskPriority(str, enum.Enum):
    """任务优先级"""
    P0 = "P0"  # 紧急
    P1 = "P1"  # 重要
    P2 = "P2"  # 优化


class TaskStatus(str, enum.Enum):
    """任务状态"""
    PENDING = "pending"          # 待处理
    IN_PROGRESS = "in_progress"  # 进行中
    COMPLETED = "completed"      # 已完成
    SKIPPED = "skipped"          # 已跳过


class TaskSource(str, enum.Enum):
    """任务来源"""
    AI = "ai"        # AI生成
    MANUAL = "manual"  # 手动添加


class ReviewTask(Base):
    """评审任务模型"""

    __tablename__ = "review_tasks"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)

    # 关联关系
    review_session_id = Column(UUID(as_uuid=True), ForeignKey("review_sessions.id"), nullable=True, index=True)
    chapter_id = Column(UUID(as_uuid=True), ForeignKey("chapters.id"), nullable=False, index=True)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False, index=True)

    # 任务基本信息
    title = Column(String(200), nullable=False, comment="任务标题")
    description = Column(Text, nullable=False, comment="详细描述")
    source = Column(
        Enum(TaskSource, name="tasksource", values_callable=lambda x: [e.value for e in x]),
        nullable=False,
        default=TaskSource.AI,
        comment="任务来源"
    )

    # 定位信息 (精确到段落)
    location = Column(JSONB, nullable=True, comment="定位信息: {paragraph_index, start_pos, end_pos, text_snippet}")

    # 任务属性
    priority = Column(
        Enum(TaskPriority, name="taskpriority", values_callable=lambda x: [e.value for e in x]),
        nullable=False,
        default=TaskPriority.P1,
        index=True,
        comment="优先级"
    )
    category = Column(String(50), nullable=True, comment="分类: character/plot/pacing...")
    status = Column(
        Enum(TaskStatus, name="taskstatus", values_callable=lambda x: [e.value for e in x]),
        nullable=False,
        default=TaskStatus.PENDING,
        index=True,
        comment="任务状态"
    )

    # AI生成的元数据
    related_score = Column(String(50), nullable=True, comment="关联的评审维度")
    current_score = Column(Integer, nullable=True, comment="该维度当前分数")
    estimated_time = Column(Integer, nullable=True, comment="预估修改时间(分钟)")
    tags = Column(JSONB, nullable=True, comment="标签数组")

    # 依赖关系
    depends_on = Column(JSONB, nullable=True, comment="依赖的任务ID列表")
    blocks = Column(JSONB, nullable=True, comment="阻塞的任务ID列表")

    # 用户操作
    user_notes = Column(Text, nullable=True, comment="用户备注")
    completed_at = Column(DateTime(timezone=True), nullable=True, comment="完成时间")
    skipped_reason = Column(String(200), nullable=True, comment="跳过原因")

    # 排序
    sort_order = Column(Integer, default=0, nullable=False, comment="排序序号")

    # 时间戳
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)

    # 关联关系
    review_session = relationship("ReviewSession", back_populates="tasks")
    chapter = relationship("Chapter", back_populates="review_tasks")
    user = relationship("User", backref="review_tasks")

    def __repr__(self):
        return f"<ReviewTask {self.title} priority={self.priority} status={self.status}>"
