"""用户任务相关Schema"""
from datetime import datetime
from typing import Optional
from uuid import UUID
from pydantic import BaseModel, Field


class TaskTemplateResponse(BaseModel):
    """任务模板响应"""
    id: UUID
    task_key: str
    title: str
    description: Optional[str] = None
    icon: Optional[str] = None
    task_type: str
    reward_credits: int
    target_config: Optional[str] = None
    is_active: bool
    sort_order: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class TaskTemplateUpdate(BaseModel):
    """更新任务模板（管理员）"""
    reward_credits: Optional[int] = None
    is_active: Optional[bool] = None
    description: Optional[str] = None


class UserTaskResponse(BaseModel):
    """用户任务响应"""
    id: UUID
    user_id: UUID
    template_id: UUID
    current_progress: int
    target_progress: int
    is_completed: bool
    completed_at: Optional[datetime] = None
    is_claimed: bool
    claimed_at: Optional[datetime] = None
    claimed_credits: int
    reset_date: Optional[datetime] = None
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class UserTaskWithTemplate(BaseModel):
    """带模板信息的用户任务"""
    task: UserTaskResponse
    template: TaskTemplateResponse
    progress_percentage: int

    class Config:
        from_attributes = True


class TaskListResponse(BaseModel):
    """任务列表响应"""
    tasks: list[UserTaskWithTemplate]
    total: int
    completed_count: int
    total_credits_earned: int

    class Config:
        from_attributes = True
