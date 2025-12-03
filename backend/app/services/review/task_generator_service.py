"""
任务生成服务
负责将评审结果转化为具体的修改任务
"""

import json
import re
import logging
from typing import List, Optional, Dict, Any
from uuid import UUID
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, and_

from app.models.review_session import ReviewSession
from app.models.review_task import ReviewTask, TaskPriority, TaskStatus, TaskSource
from app.models.chapter import Chapter
from app.schemas.review import (
    ReviewTaskCreate,
    ReviewTaskUpdate,
    ReviewTaskResponse,
    ReviewTaskStatusUpdate,
    TaskStatsResponse,
    BatchOperationRequest
)
from app.prompts.review_prompts import ReviewPromptTemplates
from app.services.ai.http_ai_service import HTTPAIService
from app.services.ai_log_service import AILogService
# 导入 TaskType 用于智能模型选择
from app.services.agent.model_selector import TaskType
# 导入 JSON 提取函数
from app.services.review.novel_review_service import extract_json_from_response
from app.utils.datetime_utils import get_utc_now

logger = logging.getLogger(__name__)


class TaskGeneratorService:
    """任务生成服务"""

    def __init__(self, db: AsyncSession):
        self.db = db
        # ❌ DEPRECATED - 2025-12-01
        # self.ai_service = HTTPAIService()
        # ✅ 新增：传递db给HTTPAIService
        self.ai_service = HTTPAIService(db=db, user_id=None)
        self.ai_log_service = AILogService(db)
        self.prompts = ReviewPromptTemplates()

    async def generate_tasks_from_review(
        self,
        review_session_id: UUID,
        chapter_id: UUID,
        user_id: UUID
    ) -> List[ReviewTask]:
        """
        根据评审结果自动生成任务

        Args:
            review_session_id: 评审会话ID
            chapter_id: 章节ID
            user_id: 用户ID

        Returns:
            生成的任务列表
        """
        # 1. 获取评审会话
        session = await self._get_review_session(review_session_id)
        if not session:
            raise ValueError(f"评审会话不存在: {review_session_id}")

        # 2. 获取章节内容
        chapter = await self._get_chapter(chapter_id)
        if not chapter:
            raise ValueError(f"章节不存在: {chapter_id}")

        logger.info(
            f"[TaskGeneratorService] 开始生成任务: session_id={review_session_id}, "
            f"overall_score={session.overall_score}"
        )

        # 3. 调用 AI 生成任务
        tasks_data = await self._generate_tasks_with_ai(
            session=session,
            chapter_content=chapter.content,
            user_id=user_id
        )

        # 4. 保存任务到数据库
        tasks = await self._save_tasks(
            tasks_data=tasks_data,
            review_session_id=review_session_id,
            chapter_id=chapter_id,
            user_id=user_id
        )

        logger.info(
            f"[TaskGeneratorService] 任务生成完成: 共生成 {len(tasks)} 个任务"
        )

        return tasks

    async def create_manual_task(
        self,
        user_id: UUID,
        request: ReviewTaskCreate
    ) -> ReviewTask:
        """手动创建任务"""

        # 获取当前最大排序号
        max_order = await self._get_max_sort_order(request.chapter_id)

        task = ReviewTask(
            review_session_id=None,  # 手动创建的任务没有关联评审会话
            chapter_id=request.chapter_id,
            user_id=user_id,
            title=request.title,
            description=request.description,
            source=TaskSource.MANUAL,
            location=request.location.model_dump() if request.location else None,
            priority=request.priority,
            category=request.category,
            status=TaskStatus.PENDING,
            estimated_time=request.estimated_time,
            tags=request.tags,
            sort_order=max_order + 1
        )

        self.db.add(task)
        await self.db.commit()
        await self.db.refresh(task)

        logger.info(f"[TaskGeneratorService] 手动创建任务: task_id={task.id}")

        return task

    async def update_task(
        self,
        task_id: UUID,
        request: ReviewTaskUpdate
    ) -> ReviewTask:
        """更新任务"""
        task = await self._get_task(task_id)
        if not task:
            raise ValueError(f"任务不存在: {task_id}")

        # 更新字段
        if request.title is not None:
            task.title = request.title
        if request.description is not None:
            task.description = request.description
        if request.priority is not None:
            task.priority = request.priority
        if request.category is not None:
            task.category = request.category
        if request.status is not None:
            task.status = request.status
            if request.status == TaskStatus.COMPLETED:
                from datetime import datetime
                task.completed_at = get_utc_now()
        if request.user_notes is not None:
            task.user_notes = request.user_notes
        if request.skipped_reason is not None:
            task.skipped_reason = request.skipped_reason
        if request.sort_order is not None:
            task.sort_order = request.sort_order

        await self.db.commit()
        await self.db.refresh(task)

        return task

    async def update_task_status(
        self,
        task_id: UUID,
        request: ReviewTaskStatusUpdate
    ) -> ReviewTask:
        """更新任务状态"""
        task = await self._get_task(task_id)
        if not task:
            raise ValueError(f"任务不存在: {task_id}")

        task.status = request.status

        if request.status == TaskStatus.COMPLETED:
            from datetime import datetime
            task.completed_at = get_utc_now()

        if request.status == TaskStatus.SKIPPED and request.skipped_reason:
            task.skipped_reason = request.skipped_reason

        if request.notes:
            task.user_notes = request.notes

        await self.db.commit()
        await self.db.refresh(task)

        logger.info(
            f"[TaskGeneratorService] 任务状态更新: task_id={task_id}, "
            f"status={request.status}"
        )

        return task

    async def batch_operation(
        self,
        request: BatchOperationRequest
    ) -> Dict[str, Any]:
        """批量操作任务"""
        result = {"success": 0, "failed": 0, "errors": []}

        for task_id in request.task_ids:
            try:
                if request.action == "complete":
                    await self.update_task_status(
                        task_id,
                        ReviewTaskStatusUpdate(
                            status=TaskStatus.COMPLETED,
                            notes=request.notes
                        )
                    )
                elif request.action == "skip":
                    await self.update_task_status(
                        task_id,
                        ReviewTaskStatusUpdate(
                            status=TaskStatus.SKIPPED,
                            skipped_reason=request.reason
                        )
                    )
                elif request.action == "delete":
                    await self.delete_task(task_id)
                elif request.action == "update_priority":
                    if request.new_priority:
                        await self.update_task(
                            task_id,
                            ReviewTaskUpdate(priority=request.new_priority)
                        )

                result["success"] += 1

            except Exception as e:
                result["failed"] += 1
                result["errors"].append({"task_id": str(task_id), "error": str(e)})
                logger.error(f"[TaskGeneratorService] 批量操作失败: {str(e)}")

        logger.info(
            f"[TaskGeneratorService] 批量操作完成: action={request.action}, "
            f"success={result['success']}, failed={result['failed']}"
        )

        return result

    async def get_tasks_by_chapter(
        self,
        chapter_id: UUID,
        status: Optional[TaskStatus] = None,
        priority: Optional[TaskPriority] = None,
        skip: int = 0,
        limit: int = 100
    ) -> List[ReviewTask]:
        """获取章节的任务列表"""
        conditions = [ReviewTask.chapter_id == chapter_id]

        if status:
            conditions.append(ReviewTask.status == status)
        if priority:
            conditions.append(ReviewTask.priority == priority)

        result = await self.db.execute(
            select(ReviewTask)
            .where(and_(*conditions))
            .order_by(ReviewTask.sort_order, ReviewTask.created_at.desc())
            .offset(skip)
            .limit(limit)
        )

        return list(result.scalars().all())

    async def get_task_stats(
        self,
        chapter_id: Optional[UUID] = None,
        user_id: Optional[UUID] = None
    ) -> TaskStatsResponse:
        """获取任务统计"""
        conditions = []
        if chapter_id:
            conditions.append(ReviewTask.chapter_id == chapter_id)
        if user_id:
            conditions.append(ReviewTask.user_id == user_id)

        result = await self.db.execute(
            select(ReviewTask).where(and_(*conditions))
        )
        tasks = list(result.scalars().all())

        # 统计
        total = len(tasks)
        by_status = {}
        by_priority = {}
        estimated_total_time = 0

        for task in tasks:
            # 按状态统计
            status_key = task.status.value
            by_status[status_key] = by_status.get(status_key, 0) + 1

            # 按优先级统计
            priority_key = task.priority.value
            by_priority[priority_key] = by_priority.get(priority_key, 0) + 1

            # 累计预估时间
            if task.estimated_time:
                estimated_total_time += task.estimated_time

        # 计算完成率
        completed_count = by_status.get(TaskStatus.COMPLETED.value, 0)
        completion_rate = completed_count / total if total > 0 else 0.0

        return TaskStatsResponse(
            total=total,
            by_status=by_status,
            by_priority=by_priority,
            estimated_total_time=estimated_total_time,
            completion_rate=completion_rate
        )

    async def delete_task(self, task_id: UUID):
        """删除任务"""
        task = await self._get_task(task_id)
        if task:
            await self.db.delete(task)
            await self.db.commit()

    # ==================== 私有方法 ====================

    async def _generate_tasks_with_ai(
        self,
        session: ReviewSession,
        chapter_content: str,
        user_id: UUID
    ) -> List[Dict[str, Any]]:
        """使用 AI 生成任务"""

        system_prompt, user_prompt = self.prompts.get_task_generation_prompt(
            overall_score=session.overall_score,
            dimension_scores=session.dimension_scores,
            issues=session.issues or [],
            suggestions=session.suggestions or [],
            content=chapter_content[:5000]  # 限制长度
        )

        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ]

        # 记录 AI 调用
        ai_log_id = await self.ai_log_service.log_ai_call_start(
            user_id=user_id,
            operation="task_generation",
            prompt_text=user_prompt,
            model_name=self.ai_service.model
        )

        try:
            full_response = ""
            last_usage = None  # 保存最后的 usage 数据
            async for chunk in self.ai_service._stream_chat(
                messages=messages,
                max_tokens=3000,
                temperature=0.7,
                task_type=TaskType.STORY_PLANNING  # 启用智能模型选择
            ):
                # chunk 是 tuple (文本片段, usage统计)
                text_chunk, usage = chunk
                full_response += text_chunk
                # 保存 usage（最后一个块包含完整的 usage 数据）
                if usage is not None:
                    last_usage = usage

            logger.info(f"[TaskGeneratorService] AI 响应长度: {len(full_response)} 字符")
            logger.debug(f"[TaskGeneratorService] AI 响应前200字符: {full_response[:200]}")

            # 使用智能提取函数解析 JSON（与 NovelReviewService 一致）
            tasks_data = extract_json_from_response(full_response)

            logger.info(f"[TaskGeneratorService] 成功生成 {len(tasks_data) if isinstance(tasks_data, list) else 0} 个任务")

            # 提取真实的 token 数据
            prompt_tokens = last_usage.get("prompt_tokens", 0) if last_usage else 0
            completion_tokens = last_usage.get("completion_tokens", 0) if last_usage else 0

            await self.ai_log_service.log_ai_call_success(
                log_id=ai_log_id,
                response_text=full_response,
                prompt_tokens=prompt_tokens,
                completion_tokens=completion_tokens
            )

            return tasks_data

        except (json.JSONDecodeError, ValueError) as e:
            logger.error(f"[TaskGeneratorService] JSON 解析失败: {str(e)}")
            logger.error(f"[TaskGeneratorService] 原始响应: {full_response[:500] if 'full_response' in locals() else 'N/A'}")
            await self.ai_log_service.log_ai_call_error(
                log_id=ai_log_id,
                error_message=f"JSON解析失败: {str(e)}"
            )
            raise ValueError(f"AI 返回的任务数据格式错误: {str(e)}")

        except Exception as e:
            logger.error(f"[TaskGeneratorService] AI 调用失败: {str(e)}")
            await self.ai_log_service.log_ai_call_error(
                log_id=ai_log_id,
                error_message=str(e)
            )
            raise

    async def _save_tasks(
        self,
        tasks_data: List[Dict[str, Any]],
        review_session_id: UUID,
        chapter_id: UUID,
        user_id: UUID
    ) -> List[ReviewTask]:
        """保存任务到数据库"""
        tasks = []

        for i, task_data in enumerate(tasks_data):
            task = ReviewTask(
                review_session_id=review_session_id,
                chapter_id=chapter_id,
                user_id=user_id,
                title=task_data.get("title"),
                description=task_data.get("description"),
                source=TaskSource.AI,
                location=task_data.get("location"),
                priority=TaskPriority(task_data.get("priority", "P1")),
                category=task_data.get("category"),
                status=TaskStatus.PENDING,
                related_score=task_data.get("related_score"),
                current_score=task_data.get("current_score"),
                estimated_time=task_data.get("estimated_time"),
                tags=task_data.get("tags"),
                sort_order=i
            )
            self.db.add(task)
            tasks.append(task)

        await self.db.commit()

        # 刷新所有任务
        for task in tasks:
            await self.db.refresh(task)

        return tasks

    async def _get_review_session(self, session_id: UUID) -> Optional[ReviewSession]:
        """获取评审会话"""
        result = await self.db.execute(
            select(ReviewSession).where(ReviewSession.id == session_id)
        )
        return result.scalar_one_or_none()

    async def _get_chapter(self, chapter_id: UUID) -> Optional[Chapter]:
        """获取章节"""
        result = await self.db.execute(
            select(Chapter).where(Chapter.id == chapter_id)
        )
        return result.scalar_one_or_none()

    async def _get_task(self, task_id: UUID) -> Optional[ReviewTask]:
        """获取任务"""
        result = await self.db.execute(
            select(ReviewTask).where(ReviewTask.id == task_id)
        )
        return result.scalar_one_or_none()

    async def _get_max_sort_order(self, chapter_id: UUID) -> int:
        """获取章节任务的最大排序号"""
        from sqlalchemy import func

        result = await self.db.execute(
            select(func.max(ReviewTask.sort_order))
            .where(ReviewTask.chapter_id == chapter_id)
        )
        max_order = result.scalar()
        return max_order if max_order is not None else -1
