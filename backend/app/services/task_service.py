"""任务奖励系统服务"""
from datetime import datetime, timedelta
from typing import List, Optional
from uuid import UUID
from decimal import Decimal
from sqlalchemy import select, and_
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.models.user_task import TaskTemplate, UserTask
from app.models.user import User
from app.models.user_credits import UserCredits
from app.models.credit_transaction import CreditTransaction
from app.schemas.user_task import (
    TaskTemplateUpdate,
    TaskListResponse,
    UserTaskWithTemplate,
    UserTaskResponse,
    TaskTemplateResponse
)


class TaskService:
    """任务服务"""

    @staticmethod
    async def get_user_tasks(db: AsyncSession, user_id: UUID) -> TaskListResponse:
        """获取用户所有任务及进度"""
        # 获取所有激活的任务模板
        templates_result = await db.execute(
            select(TaskTemplate).where(TaskTemplate.is_active == True).order_by(TaskTemplate.sort_order)
        )
        templates = templates_result.scalars().all()

        # 获取用户已有的任务记录
        user_tasks_result = await db.execute(
            select(UserTask)
            .options(selectinload(UserTask.template))
            .where(UserTask.user_id == user_id)
        )
        user_tasks = {ut.template_id: ut for ut in user_tasks_result.scalars().all()}

        # 为用户创建缺失的任务记录
        tasks_with_templates = []
        for template in templates:
            user_task = user_tasks.get(template.id)
            if not user_task:
                # 创建新的用户任务记录
                import json
                target_config = json.loads(template.target_config) if template.target_config else {}
                target_progress = target_config.get("target", 1)

                user_task = UserTask(
                    user_id=user_id,
                    template_id=template.id,
                    current_progress=0,
                    target_progress=target_progress,
                    is_completed=False,
                    is_claimed=False,
                    claimed_credits=0
                )
                db.add(user_task)
                await db.flush()
                await db.refresh(user_task)

            # 检查是否需要重置每日任务
            if template.task_type == "daily" and user_task.reset_date:
                if datetime.utcnow().date() > user_task.reset_date.date():
                    user_task.current_progress = 0
                    user_task.is_completed = False
                    user_task.is_claimed = False
                    user_task.reset_date = None

            # 计算进度百分比
            progress_percentage = min(100, int((user_task.current_progress / user_task.target_progress) * 100))

            tasks_with_templates.append(UserTaskWithTemplate(
                task=UserTaskResponse.model_validate(user_task),
                template=TaskTemplateResponse.model_validate(template),
                progress_percentage=progress_percentage
            ))

        await db.commit()

        # 统计信息
        completed_count = sum(1 for t in tasks_with_templates if t.task.is_completed)
        total_credits_earned = sum(t.task.claimed_credits for t in tasks_with_templates)

        return TaskListResponse(
            tasks=tasks_with_templates,
            total=len(tasks_with_templates),
            completed_count=completed_count,
            total_credits_earned=total_credits_earned
        )

    @staticmethod
    async def update_task_progress(
        db: AsyncSession,
        user_id: UUID,
        task_key: str,
        progress_increment: int = 1
    ) -> Optional[UserTask]:
        """更新任务进度"""
        # 获取任务模板
        template_result = await db.execute(
            select(TaskTemplate).where(TaskTemplate.task_key == task_key)
        )
        template = template_result.scalar_one_or_none()
        if not template or not template.is_active:
            return None

        # 获取或创建用户任务
        user_task_result = await db.execute(
            select(UserTask).where(
                and_(
                    UserTask.user_id == user_id,
                    UserTask.template_id == template.id
                )
            )
        )
        user_task = user_task_result.scalar_one_or_none()

        if not user_task:
            import json
            target_config = json.loads(template.target_config) if template.target_config else {}
            target_progress = target_config.get("target", 1)

            user_task = UserTask(
                user_id=user_id,
                template_id=template.id,
                current_progress=0,
                target_progress=target_progress,
                is_completed=False,
                is_claimed=False,
                claimed_credits=0
            )
            db.add(user_task)

        # 如果是每日任务且已过期，重置进度
        if template.task_type == "daily" and user_task.reset_date:
            if datetime.utcnow().date() > user_task.reset_date.date():
                user_task.current_progress = 0
                user_task.is_completed = False
                user_task.is_claimed = False
                user_task.reset_date = None

        # 如果已完成且是一次性任务，不再更新
        if user_task.is_completed and template.task_type == "once":
            return user_task

        # 更新进度
        user_task.current_progress += progress_increment
        user_task.updated_at = datetime.utcnow()

        # 检查是否完成
        if user_task.current_progress >= user_task.target_progress and not user_task.is_completed:
            user_task.is_completed = True
            user_task.completed_at = datetime.utcnow()

            # 自动领取奖励
            await TaskService.claim_task_reward(db, user_id, user_task, template)

        # 不在这里commit，让调用者控制事务
        await db.flush()  # 确保数据写入但不提交事务
        return user_task

    @staticmethod
    async def claim_task_reward(
        db: AsyncSession,
        user_id: UUID,
        user_task: UserTask,
        template: TaskTemplate
    ) -> bool:
        """领取任务奖励"""
        print(f"[TaskService] Claiming reward for task {template.task_key}, user {user_id}")

        if user_task.is_claimed:
            print(f"[TaskService] Task already claimed")
            return False

        # 获取或创建用户积分记录
        user_credits_result = await db.execute(
            select(UserCredits).where(UserCredits.user_id == user_id)
        )
        user_credits = user_credits_result.scalar_one_or_none()

        if not user_credits:
            # 如果用户没有积分记录，创建一个
            user_credits = UserCredits(
                user_id=user_id,
                balance=Decimal("0.00")
            )
            db.add(user_credits)
            await db.flush()
            print(f"[TaskService] Created new credits record for user {user_id}")

        # 发放积分
        old_balance = user_credits.balance
        reward_amount = Decimal(str(template.reward_credits))
        new_balance = old_balance + reward_amount

        user_credits.balance = new_balance
        user_credits.total_gifted += reward_amount

        # 创建积分流水记录
        transaction = CreditTransaction(
            user_id=user_id,
            type="gift",
            amount=reward_amount,
            balance_before=old_balance,
            balance_after=new_balance,
            description=f"完成任务奖励: {template.title}",
            related_type="task_reward",
            related_id=user_task.id
        )
        db.add(transaction)

        user_task.is_claimed = True
        user_task.claimed_at = datetime.utcnow()
        user_task.claimed_credits = template.reward_credits

        print(f"[TaskService] Credits updated: {old_balance} -> {new_balance} (+{reward_amount})")
        print(f"[TaskService] Credit transaction created: {transaction.id}")

        # 如果是每日任务，设置重置日期
        if template.task_type == "daily":
            user_task.reset_date = datetime.utcnow() + timedelta(days=1)

        # 不在这里commit，让调用者控制事务
        await db.flush()
        print(f"[TaskService] Reward claimed successfully")
        return True

    @staticmethod
    async def get_all_templates(db: AsyncSession) -> List[TaskTemplate]:
        """获取所有任务模板（管理员）"""
        result = await db.execute(
            select(TaskTemplate).order_by(TaskTemplate.sort_order)
        )
        return list(result.scalars().all())

    @staticmethod
    async def update_template(
        db: AsyncSession,
        template_id: UUID,
        update_data: TaskTemplateUpdate
    ) -> Optional[TaskTemplate]:
        """更新任务模板（管理员）"""
        result = await db.execute(
            select(TaskTemplate).where(TaskTemplate.id == template_id)
        )
        template = result.scalar_one_or_none()
        if not template:
            return None

        # 更新字段
        update_dict = update_data.model_dump(exclude_unset=True)
        for field, value in update_dict.items():
            setattr(template, field, value)

        template.updated_at = datetime.utcnow()
        await db.commit()
        await db.refresh(template)
        return template

    @staticmethod
    async def check_avatar_task(db: AsyncSession, user_id: UUID) -> None:
        """检查头像设置任务"""
        print(f"[TaskService] Checking avatar task for user {user_id}")
        result = await TaskService.update_task_progress(db, user_id, "set_avatar", 1)
        print(f"[TaskService] Avatar task result: {result}")

    @staticmethod
    async def check_username_task(db: AsyncSession, user_id: UUID) -> None:
        """检查用户名修改任务"""
        print(f"[TaskService] Checking username task for user {user_id}")
        result = await TaskService.update_task_progress(db, user_id, "change_username", 1)
        print(f"[TaskService] Username task result: {result}")

    @staticmethod
    async def check_daily_writing_task(db: AsyncSession, user_id: UUID, word_count: int) -> None:
        """检查每日写作任务"""
        print(f"[TaskService] Checking daily writing task for user {user_id}, word_count: {word_count}")
        result = await TaskService.update_task_progress(db, user_id, "daily_write_1000", word_count)
        print(f"[TaskService] Daily writing task result: {result}")

    @staticmethod
    async def check_channel_message_task(db: AsyncSession, user_id: UUID) -> None:
        """检查每日频道发言任务"""
        print(f"[TaskService] Checking channel message task for user {user_id}")
        result = await TaskService.update_task_progress(db, user_id, "daily_channel_messages", 1)
        print(f"[TaskService] Channel message task result: {result}")
