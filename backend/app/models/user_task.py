"""用户任务系统模型"""
from sqlalchemy import Column, String, DateTime, Integer, Boolean, ForeignKey, Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
import uuid

from app.core.database import Base


class TaskTemplate(Base):
    """任务模板（管理员配置）"""

    __tablename__ = "task_templates"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)

    # 任务基本信息
    task_key = Column(String(50), unique=True, nullable=False, index=True, comment="任务唯一标识")
    title = Column(String(100), nullable=False, comment="任务标题")
    description = Column(Text, nullable=True, comment="任务描述")
    icon = Column(String(50), nullable=True, comment="任务图标")

    # 任务类型: daily(每日), once(一次性), repeatable(可重复)
    task_type = Column(String(20), nullable=False, server_default="once")

    # 奖励积分
    reward_credits = Column(Integer, nullable=False, default=0, comment="奖励积分")

    # 任务目标（JSON格式存储具体要求）
    # 例如: {"type": "write_words", "target": 1000} 或 {"type": "set_avatar"}
    target_config = Column(Text, nullable=True, comment="任务目标配置")

    # 状态
    is_active = Column(Boolean, default=True, nullable=False, comment="是否启用")
    sort_order = Column(Integer, default=0, nullable=False, comment="排序")

    # 时间戳
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)

    # 关联关系
    user_tasks = relationship("UserTask", back_populates="template", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<TaskTemplate {self.task_key}>"


class UserTask(Base):
    """用户任务完成记录"""

    __tablename__ = "user_tasks"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    template_id = Column(UUID(as_uuid=True), ForeignKey("task_templates.id", ondelete="CASCADE"), nullable=False, index=True)

    # 任务进度
    current_progress = Column(Integer, default=0, nullable=False, comment="当前进度")
    target_progress = Column(Integer, default=1, nullable=False, comment="目标进度")

    # 完成状态
    is_completed = Column(Boolean, default=False, nullable=False, comment="是否完成")
    completed_at = Column(DateTime(timezone=True), nullable=True, comment="完成时间")

    # 奖励领取
    is_claimed = Column(Boolean, default=False, nullable=False, comment="是否已领取奖励")
    claimed_at = Column(DateTime(timezone=True), nullable=True, comment="领取时间")
    claimed_credits = Column(Integer, default=0, nullable=False, comment="领取的积分数")

    # 每日任务重置日期（仅每日任务使用）
    reset_date = Column(DateTime(timezone=True), nullable=True, comment="重置日期")

    # 时间戳
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)

    # 关联关系
    user = relationship("User", back_populates="user_tasks")
    template = relationship("TaskTemplate", back_populates="user_tasks")

    def __repr__(self):
        return f"<UserTask user={self.user_id} template={self.template_id}>"
