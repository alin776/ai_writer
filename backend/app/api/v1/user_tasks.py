"""用户任务奖励系统API"""
from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.core.security import get_current_active_user, get_current_admin_user
from app.models.user import User
from app.services.task_service import TaskService
from app.schemas.user_task import (
    TaskListResponse,
    TaskTemplateResponse,
    TaskTemplateUpdate
)

router = APIRouter()


@router.get("/user/my-tasks", response_model=TaskListResponse)
async def get_my_tasks(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """获取当前用户的所有任务"""
    try:
        return await TaskService.get_user_tasks(db, current_user.id)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to get tasks: {str(e)}"
        )


@router.post("/user/progress/{task_key}")
async def update_task_progress(
    task_key: str,
    progress_increment: int = 1,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """手动更新任务进度（主要用于测试）"""
    try:
        user_task = await TaskService.update_task_progress(
            db, current_user.id, task_key, progress_increment
        )
        if not user_task:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Task not found or inactive"
            )
        return {"message": "Progress updated successfully", "task": user_task}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to update progress: {str(e)}"
        )


@router.get("/admin/templates", response_model=list[TaskTemplateResponse])
async def get_all_templates(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_admin_user)
):
    """获取所有任务模板（管理员）"""
    try:
        templates = await TaskService.get_all_templates(db)
        return [TaskTemplateResponse.model_validate(t) for t in templates]
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to get templates: {str(e)}"
        )


@router.patch("/admin/templates/{template_id}", response_model=TaskTemplateResponse)
async def update_template(
    template_id: UUID,
    update_data: TaskTemplateUpdate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_admin_user)
):
    """更新任务模板（管理员）"""
    try:
        template = await TaskService.update_template(db, template_id, update_data)
        if not template:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Template not found"
            )
        return TaskTemplateResponse.model_validate(template)
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to update template: {str(e)}"
        )
