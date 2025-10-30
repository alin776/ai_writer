"""
规划Agent (Planning Agent)

核心功能:
1. 理解用户高层目标 (如"我想写玄幻小说")
2. 自动分解为可执行的子任务
3. 动态调整执行计划
4. 失败自动重试和重规划

这是Agentic AI的9大核心工作流模式之一：Planning
也是文档中「核心场景B」的关键技术

使用场景:
- "我想写玄幻小说" → 自动规划：世界观→人物→大纲→第一章
- "帮我完善这部作品" → 自动规划：分析→诊断→修复建议→执行修复
- "准备一个新的系列小说" → 自动规划：多部作品规划→角色体系→时间线
"""

from typing import Dict, List, Optional, Any, Callable
from datetime import datetime
from enum import Enum
from pydantic import BaseModel
import json


class TaskStatus(str, Enum):
    """任务状态"""
    PENDING = "pending"  # 待执行
    RUNNING = "running"  # 执行中
    COMPLETED = "completed"  # 已完成
    FAILED = "failed"  # 失败
    SKIPPED = "skipped"  # 跳过
    BLOCKED = "blocked"  # 被阻塞


class TaskType(str, Enum):
    """任务类型"""
    # 规划类
    ANALYZE_REQUIREMENT = "analyze_requirement"  # 分析需求
    CREATE_PLAN = "create_plan"  # 创建计划

    # 创作类
    CREATE_WORLDVIEW = "create_worldview"  # 创建世界观
    CREATE_CHARACTER = "create_character"  # 创建角色
    CREATE_OUTLINE = "create_outline"  # 创建大纲
    WRITE_CHAPTER = "write_chapter"  # 撰写章节

    # 分析类
    ANALYZE_WORK = "analyze_work"  # 分析作品
    DIAGNOSE_ISSUE = "diagnose_issue"  # 诊断问题
    SUGGEST_FIX = "suggest_fix"  # 建议修复

    # 工具类
    SEARCH_KNOWLEDGE = "search_knowledge"  # 搜索知识库
    RETRIEVE_CONTEXT = "retrieve_context"  # 检索上下文


class Task(BaseModel):
    """任务定义"""
    task_id: str  # 任务ID
    task_type: TaskType  # 任务类型
    description: str  # 任务描述

    # 执行参数
    parameters: Dict[str, Any] = {}  # 任务参数
    dependencies: List[str] = []  # 依赖的任务ID

    # 执行状态
    status: TaskStatus = TaskStatus.PENDING
    result: Optional[Any] = None  # 执行结果
    error: Optional[str] = None  # 错误信息

    # 时间信息
    created_at: str
    started_at: Optional[str] = None
    completed_at: Optional[str] = None

    # 重试配置
    max_retries: int = 3
    retry_count: int = 0

    # 优先级
    priority: int = 0  # 数字越大优先级越高


class ExecutionPlan(BaseModel):
    """执行计划"""
    plan_id: str  # 计划ID
    goal: str  # 目标描述

    # 任务列表
    tasks: List[Task] = []  # 所有任务
    current_task_index: int = 0  # 当前执行到的任务索引

    # 计划状态
    status: str = "pending"  # pending/running/completed/failed
    progress: float = 0.0  # 进度 0-1

    # 元数据
    created_at: str
    started_at: Optional[str] = None
    completed_at: Optional[str] = None

    # 上下文
    context: Dict[str, Any] = {}  # 执行过程中积累的上下文


class PlanningAgent:
    """规划Agent"""

    def __init__(self, task_executors: Dict[TaskType, Callable] = None):
        """
        初始化规划Agent

        Args:
            task_executors: 任务执行器映射 {TaskType: executor_function}
        """
        self.task_executors = task_executors or {}

    # ==================== 计划生成 ====================

    def create_plan_for_novel_writing(
        self,
        user_goal: str,
        genre: Optional[str] = None,
        context: Dict[str, Any] = None
    ) -> ExecutionPlan:
        """
        为小说创作生成执行计划

        场景: "我想写玄幻小说"

        Args:
            user_goal: 用户目标
            genre: 小说类型
            context: 上下文信息

        Returns:
            ExecutionPlan: 执行计划
        """
        import uuid

        plan_id = str(uuid.uuid4())
        tasks = []

        # 任务1: 分析需求
        tasks.append(Task(
            task_id=f"{plan_id}_task_1",
            task_type=TaskType.ANALYZE_REQUIREMENT,
            description="分析用户需求，明确小说类型、风格、主题等",
            parameters={"user_goal": user_goal, "genre": genre},
            created_at=datetime.now().isoformat(),
            priority=10
        ))

        # 任务2: 创建世界观
        tasks.append(Task(
            task_id=f"{plan_id}_task_2",
            task_type=TaskType.CREATE_WORLDVIEW,
            description="创建小说世界观设定",
            parameters={"genre": genre},
            dependencies=[f"{plan_id}_task_1"],
            created_at=datetime.now().isoformat(),
            priority=9
        ))

        # 任务3: 创建主角
        tasks.append(Task(
            task_id=f"{plan_id}_task_3",
            task_type=TaskType.CREATE_CHARACTER,
            description="创建主角角色卡片",
            parameters={"role": "protagonist"},
            dependencies=[f"{plan_id}_task_2"],
            created_at=datetime.now().isoformat(),
            priority=8
        ))

        # 任务4: 创建配角
        tasks.append(Task(
            task_id=f"{plan_id}_task_4",
            task_type=TaskType.CREATE_CHARACTER,
            description="创建重要配角",
            parameters={"role": "supporting", "count": 2},
            dependencies=[f"{plan_id}_task_3"],
            created_at=datetime.now().isoformat(),
            priority=7
        ))

        # 任务5: 生成大纲
        tasks.append(Task(
            task_id=f"{plan_id}_task_5",
            task_type=TaskType.CREATE_OUTLINE,
            description="生成小说大纲（20-30章）",
            parameters={"chapter_count": 25},
            dependencies=[f"{plan_id}_task_4"],
            created_at=datetime.now().isoformat(),
            priority=6
        ))

        # 任务6: 撰写第一章
        tasks.append(Task(
            task_id=f"{plan_id}_task_6",
            task_type=TaskType.WRITE_CHAPTER,
            description="撰写第一章",
            parameters={"chapter_number": 1},
            dependencies=[f"{plan_id}_task_5"],
            created_at=datetime.now().isoformat(),
            priority=5
        ))

        return ExecutionPlan(
            plan_id=plan_id,
            goal=user_goal,
            tasks=tasks,
            created_at=datetime.now().isoformat(),
            context=context or {}
        )

    def create_plan_for_work_improvement(
        self,
        work_id: str,
        improvement_goals: List[str],
        context: Dict[str, Any] = None
    ) -> ExecutionPlan:
        """
        为作品改进生成执行计划

        场景: "帮我完善这部作品"

        Args:
            work_id: 作品ID
            improvement_goals: 改进目标列表
            context: 上下文

        Returns:
            ExecutionPlan: 执行计划
        """
        import uuid

        plan_id = str(uuid.uuid4())
        tasks = []

        # 任务1: 分析作品
        tasks.append(Task(
            task_id=f"{plan_id}_task_1",
            task_type=TaskType.ANALYZE_WORK,
            description="全面分析作品现状",
            parameters={"work_id": work_id},
            created_at=datetime.now().isoformat(),
            priority=10
        ))

        # 任务2: 诊断问题
        tasks.append(Task(
            task_id=f"{plan_id}_task_2",
            task_type=TaskType.DIAGNOSE_ISSUE,
            description="诊断作品存在的问题",
            parameters={"work_id": work_id, "focus_areas": improvement_goals},
            dependencies=[f"{plan_id}_task_1"],
            created_at=datetime.now().isoformat(),
            priority=9
        ))

        # 任务3: 生成修复建议
        tasks.append(Task(
            task_id=f"{plan_id}_task_3",
            task_type=TaskType.SUGGEST_FIX,
            description="生成针对性的修复建议",
            parameters={"work_id": work_id},
            dependencies=[f"{plan_id}_task_2"],
            created_at=datetime.now().isoformat(),
            priority=8
        ))

        return ExecutionPlan(
            plan_id=plan_id,
            goal=f"改进作品: {', '.join(improvement_goals)}",
            tasks=tasks,
            created_at=datetime.now().isoformat(),
            context=context or {"work_id": work_id}
        )

    def create_custom_plan(
        self,
        goal: str,
        tasks_config: List[Dict[str, Any]]
    ) -> ExecutionPlan:
        """
        创建自定义执行计划

        Args:
            goal: 目标描述
            tasks_config: 任务配置列表

        Returns:
            ExecutionPlan: 执行计划
        """
        import uuid

        plan_id = str(uuid.uuid4())
        tasks = []

        for i, task_cfg in enumerate(tasks_config):
            tasks.append(Task(
                task_id=f"{plan_id}_task_{i+1}",
                task_type=TaskType(task_cfg["type"]),
                description=task_cfg["description"],
                parameters=task_cfg.get("parameters", {}),
                dependencies=task_cfg.get("dependencies", []),
                created_at=datetime.now().isoformat(),
                priority=task_cfg.get("priority", 5),
                max_retries=task_cfg.get("max_retries", 3)
            ))

        return ExecutionPlan(
            plan_id=plan_id,
            goal=goal,
            tasks=tasks,
            created_at=datetime.now().isoformat()
        )

    # ==================== 计划执行 ====================

    async def execute_plan(
        self,
        plan: ExecutionPlan,
        on_task_start: Optional[Callable] = None,
        on_task_complete: Optional[Callable] = None,
        on_task_failed: Optional[Callable] = None
    ) -> ExecutionPlan:
        """
        执行计划

        Args:
            plan: 执行计划
            on_task_start: 任务开始回调
            on_task_complete: 任务完成回调
            on_task_failed: 任务失败回调

        Returns:
            ExecutionPlan: 更新后的计划
        """
        plan.status = "running"
        plan.started_at = datetime.now().isoformat()

        try:
            for i, task in enumerate(plan.tasks):
                # 检查依赖
                if not self._check_dependencies(task, plan):
                    task.status = TaskStatus.BLOCKED
                    continue

                # 执行任务
                task.status = TaskStatus.RUNNING
                task.started_at = datetime.now().isoformat()

                if on_task_start:
                    await on_task_start(task, plan)

                try:
                    result = await self._execute_task(task, plan)
                    task.result = result
                    task.status = TaskStatus.COMPLETED
                    task.completed_at = datetime.now().isoformat()

                    # 更新计划上下文
                    plan.context[f"task_{task.task_id}_result"] = result

                    if on_task_complete:
                        await on_task_complete(task, plan)

                except Exception as e:
                    # 任务失败，尝试重试
                    task.error = str(e)
                    task.retry_count += 1

                    if task.retry_count < task.max_retries:
                        # 重试
                        task.status = TaskStatus.PENDING
                        continue
                    else:
                        # 达到最大重试次数
                        task.status = TaskStatus.FAILED

                        if on_task_failed:
                            should_continue = await on_task_failed(task, plan)
                            if not should_continue:
                                # 停止执行
                                plan.status = "failed"
                                return plan

                        # 尝试重规划
                        replan = await self._replan_on_failure(task, plan)
                        if replan:
                            # 用新计划替换剩余任务
                            plan.tasks = plan.tasks[:i+1] + replan

                # 更新进度
                plan.progress = (i + 1) / len(plan.tasks)

            # 所有任务完成
            plan.status = "completed"
            plan.completed_at = datetime.now().isoformat()
            plan.progress = 1.0

        except Exception as e:
            plan.status = "failed"
            plan.context["error"] = str(e)

        return plan

    async def _execute_task(
        self,
        task: Task,
        plan: ExecutionPlan
    ) -> Any:
        """
        执行单个任务

        Args:
            task: 任务
            plan: 执行计划

        Returns:
            Any: 任务结果
        """
        # 获取任务执行器
        executor = self.task_executors.get(task.task_type)

        if not executor:
            raise ValueError(f"No executor found for task type: {task.task_type}")

        # 准备参数
        kwargs = {
            **task.parameters,
            "context": plan.context,
            "task": task
        }

        # 执行
        result = await executor(**kwargs)
        return result

    def _check_dependencies(
        self,
        task: Task,
        plan: ExecutionPlan
    ) -> bool:
        """
        检查任务依赖是否满足

        Args:
            task: 任务
            plan: 执行计划

        Returns:
            bool: 依赖是否满足
        """
        if not task.dependencies:
            return True

        task_map = {t.task_id: t for t in plan.tasks}

        for dep_id in task.dependencies:
            dep_task = task_map.get(dep_id)
            if not dep_task or dep_task.status != TaskStatus.COMPLETED:
                return False

        return True

    async def _replan_on_failure(
        self,
        failed_task: Task,
        plan: ExecutionPlan
    ) -> Optional[List[Task]]:
        """
        任务失败时重新规划

        Args:
            failed_task: 失败的任务
            plan: 当前计划

        Returns:
            Optional[List[Task]]: 新的任务列表，如果无法重规划返回None
        """
        import uuid

        # 根据失败类型尝试重规划
        if failed_task.task_type == TaskType.CREATE_WORLDVIEW:
            # 世界观创建失败，尝试更简单的方案
            return [
                Task(
                    task_id=str(uuid.uuid4()),
                    task_type=TaskType.CREATE_WORLDVIEW,
                    description="创建简化的世界观设定",
                    parameters={"simplified": True, **failed_task.parameters},
                    created_at=datetime.now().isoformat(),
                    max_retries=1
                )
            ]

        elif failed_task.task_type == TaskType.SEARCH_KNOWLEDGE:
            # 知识库搜索失败，跳过这一步
            return []

        # 其他情况，无法重规划
        return None

    # ==================== 计划调整 ====================

    def add_task(
        self,
        plan: ExecutionPlan,
        task: Task,
        insert_after: Optional[str] = None
    ) -> ExecutionPlan:
        """
        向计划中添加任务

        Args:
            plan: 执行计划
            task: 新任务
            insert_after: 插入在哪个任务之后（任务ID），None表示追加到末尾

        Returns:
            ExecutionPlan: 更新后的计划
        """
        if insert_after:
            for i, t in enumerate(plan.tasks):
                if t.task_id == insert_after:
                    plan.tasks.insert(i + 1, task)
                    return plan

        plan.tasks.append(task)
        return plan

    def remove_task(
        self,
        plan: ExecutionPlan,
        task_id: str
    ) -> ExecutionPlan:
        """
        从计划中移除任务

        Args:
            plan: 执行计划
            task_id: 任务ID

        Returns:
            ExecutionPlan: 更新后的计划
        """
        plan.tasks = [t for t in plan.tasks if t.task_id != task_id]
        return plan

    def get_next_task(self, plan: ExecutionPlan) -> Optional[Task]:
        """
        获取下一个待执行的任务

        Args:
            plan: 执行计划

        Returns:
            Optional[Task]: 下一个任务，如果没有返回None
        """
        for task in plan.tasks:
            if task.status == TaskStatus.PENDING and self._check_dependencies(task, plan):
                return task

        return None

    def get_plan_summary(self, plan: ExecutionPlan) -> Dict[str, Any]:
        """
        获取计划摘要

        Args:
            plan: 执行计划

        Returns:
            Dict: 摘要信息
        """
        total = len(plan.tasks)
        completed = sum(1 for t in plan.tasks if t.status == TaskStatus.COMPLETED)
        failed = sum(1 for t in plan.tasks if t.status == TaskStatus.FAILED)
        running = sum(1 for t in plan.tasks if t.status == TaskStatus.RUNNING)

        return {
            "plan_id": plan.plan_id,
            "goal": plan.goal,
            "status": plan.status,
            "progress": plan.progress,
            "total_tasks": total,
            "completed_tasks": completed,
            "failed_tasks": failed,
            "running_tasks": running,
            "current_task": self.get_next_task(plan).description if self.get_next_task(plan) else None
        }
