"""
Planning Agent
"""

from typing import Dict, List, Optional, Any, Callable
from enum import Enum
from pydantic import BaseModel, Field
import logging
from app.utils.datetime_utils import get_utc_now

logger = logging.getLogger(__name__)


class TaskStatus(str, Enum):
    """Task status."""
    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"
    SKIPPED = "skipped"
    BLOCKED = "blocked"


class TaskType(str, Enum):
    """Task type."""
    # Planning
    ANALYZE_REQUIREMENT = "analyze_requirement"
    CREATE_PLAN = "create_plan"

    # Creation
    CREATE_WORLDVIEW = "create_worldview"
    CREATE_CHARACTER = "create_character"
    CREATE_OUTLINE = "create_outline"
    WRITE_CHAPTER = "write_chapter"

    # Analysis
    ANALYZE_WORK = "analyze_work"
    DIAGNOSE_ISSUE = "diagnose_issue"
    SUGGEST_FIX = "suggest_fix"

    # Tooling
    SEARCH_KNOWLEDGE = "search_knowledge"
    RETRIEVE_CONTEXT = "retrieve_context"


class Task(BaseModel):
    """Task definition."""
    task_id: str
    task_type: TaskType
    description: str

    parameters: Dict[str, Any] = Field(default_factory=dict)
    dependencies: List[str] = Field(default_factory=list)

    status: TaskStatus = TaskStatus.PENDING
    result: Optional[Any] = None
    error: Optional[str] = None

    created_at: str
    started_at: Optional[str] = None
    completed_at: Optional[str] = None

    max_retries: int = 3
    retry_count: int = 0

    priority: int = 0


class ExecutionPlan(BaseModel):
    """Execution plan."""
    plan_id: str
    goal: str

    tasks: List[Task] = Field(default_factory=list)
    current_task_index: int = 0

    status: str = "pending"
    progress: float = 0.0

    created_at: str
    started_at: Optional[str] = None
    completed_at: Optional[str] = None

    context: Dict[str, Any] = Field(default_factory=dict)


class PlanningAgent:
    """Planning agent."""

    def __init__(self, task_executors: Dict[TaskType, Callable]):
        if not task_executors:
            raise ValueError("task_executors is required. Register executors via constructor or register_executor.")
        self.task_executors: Dict[TaskType, Callable] = dict(task_executors)

    def register_executor(self, task_type: TaskType, executor: Callable) -> None:
        """Register a single task executor."""
        if not callable(executor):
            raise ValueError("executor must be callable")
        self.task_executors[task_type] = executor

    # ==================== Plan generation ====================

    def create_plan_for_novel_writing(
        self,
        user_goal: str,
        genre: Optional[str] = None,
        context: Optional[Dict[str, Any]] = None,
    ) -> ExecutionPlan:
        import uuid

        plan_id = str(uuid.uuid4())
        tasks: List[Task] = []

        tasks.append(Task(
            task_id=f"{plan_id}_task_1",
            task_type=TaskType.ANALYZE_REQUIREMENT,
            description="Analyze user requirement for the novel (genre/style/theme).",
            parameters={"user_goal": user_goal, "genre": genre},
            created_at=get_utc_now().isoformat(),
            priority=10,
        ))

        tasks.append(Task(
            task_id=f"{plan_id}_task_2",
            task_type=TaskType.CREATE_WORLDVIEW,
            description="Create the novel worldview.",
            parameters={"genre": genre},
            dependencies=[f"{plan_id}_task_1"],
            created_at=get_utc_now().isoformat(),
            priority=9,
        ))

        tasks.append(Task(
            task_id=f"{plan_id}_task_3",
            task_type=TaskType.CREATE_CHARACTER,
            description="Create protagonist character card.",
            parameters={"role": "protagonist"},
            dependencies=[f"{plan_id}_task_2"],
            created_at=get_utc_now().isoformat(),
            priority=8,
        ))

        tasks.append(Task(
            task_id=f"{plan_id}_task_4",
            task_type=TaskType.CREATE_CHARACTER,
            description="Create supporting characters.",
            parameters={"role": "supporting", "count": 2},
            dependencies=[f"{plan_id}_task_3"],
            created_at=get_utc_now().isoformat(),
            priority=7,
        ))

        tasks.append(Task(
            task_id=f"{plan_id}_task_5",
            task_type=TaskType.CREATE_OUTLINE,
            description="Generate story outline (20-30 chapters).",
            parameters={"chapter_count": 25},
            dependencies=[f"{plan_id}_task_4"],
            created_at=get_utc_now().isoformat(),
            priority=6,
        ))

        tasks.append(Task(
            task_id=f"{plan_id}_task_6",
            task_type=TaskType.WRITE_CHAPTER,
            description="Draft the first chapter.",
            parameters={"chapter_number": 1},
            dependencies=[f"{plan_id}_task_5"],
            created_at=get_utc_now().isoformat(),
            priority=5,
        ))

        return ExecutionPlan(
            plan_id=plan_id,
            goal=user_goal,
            tasks=tasks,
            created_at=get_utc_now().isoformat(),
            context=context or {},
        )

    def create_plan_for_work_improvement(
        self,
        work_id: str,
        improvement_goals: List[str],
        context: Optional[Dict[str, Any]] = None,
    ) -> ExecutionPlan:
        import uuid

        plan_id = str(uuid.uuid4())
        tasks: List[Task] = []

        tasks.append(Task(
            task_id=f"{plan_id}_task_1",
            task_type=TaskType.ANALYZE_WORK,
            description="Analyze current work state.",
            parameters={"work_id": work_id},
            created_at=get_utc_now().isoformat(),
            priority=10,
        ))

        tasks.append(Task(
            task_id=f"{plan_id}_task_2",
            task_type=TaskType.DIAGNOSE_ISSUE,
            description="Diagnose issues in the work.",
            parameters={"work_id": work_id, "focus_areas": improvement_goals},
            dependencies=[f"{plan_id}_task_1"],
            created_at=get_utc_now().isoformat(),
            priority=9,
        ))

        tasks.append(Task(
            task_id=f"{plan_id}_task_3",
            task_type=TaskType.SUGGEST_FIX,
            description="Suggest targeted fixes.",
            parameters={"work_id": work_id},
            dependencies=[f"{plan_id}_task_2"],
            created_at=get_utc_now().isoformat(),
            priority=8,
        ))

        return ExecutionPlan(
            plan_id=plan_id,
            goal=f"Improve work: {', '.join(improvement_goals)}",
            tasks=tasks,
            created_at=get_utc_now().isoformat(),
            context=context or {"work_id": work_id},
        )

    def create_custom_plan(
        self,
        goal: str,
        tasks_config: List[Dict[str, Any]],
    ) -> ExecutionPlan:
        import uuid

        plan_id = str(uuid.uuid4())
        tasks: List[Task] = []

        for i, task_cfg in enumerate(tasks_config):
            tasks.append(Task(
                task_id=f"{plan_id}_task_{i+1}",
                task_type=TaskType(task_cfg["type"]),
                description=task_cfg["description"],
                parameters=task_cfg.get("parameters", {}),
                dependencies=task_cfg.get("dependencies", []),
                created_at=get_utc_now().isoformat(),
                priority=task_cfg.get("priority", 5),
                max_retries=task_cfg.get("max_retries", 3),
            ))

        return ExecutionPlan(
            plan_id=plan_id,
            goal=goal,
            tasks=tasks,
            created_at=get_utc_now().isoformat(),
        )

    # ==================== Plan execution ====================

    async def execute_plan(
        self,
        plan: ExecutionPlan,
        on_task_start: Optional[Callable] = None,
        on_task_complete: Optional[Callable] = None,
        on_task_failed: Optional[Callable] = None,
    ) -> ExecutionPlan:
        if not self.task_executors:
            raise ValueError(
                "No task executors configured. Provide task_executors when initializing PlanningAgent or via register_executor()."
            )

        if not plan.tasks:
            logger.warning(f"Plan {plan.plan_id} has no tasks, mark completed.")
            plan.status = "completed"
            plan.progress = 1.0
            plan.completed_at = get_utc_now().isoformat()
            return plan

        missing_executors = [t.task_type.value for t in plan.tasks if t.task_type not in self.task_executors]
        if missing_executors:
            raise ValueError(
                f"Missing executors for task types: {', '.join(sorted(set(missing_executors)))}"
            )

        plan.status = "running"
        plan.started_at = get_utc_now().isoformat()

        try:
            i = 0
            while i < len(plan.tasks):
                task = plan.tasks[i]

                if not self._check_dependencies(task, plan):
                    task.status = TaskStatus.BLOCKED
                    i += 1
                    continue

                task.status = TaskStatus.RUNNING
                task.started_at = get_utc_now().isoformat()

                if on_task_start:
                    await on_task_start(task, plan)

                try:
                    result = await self._execute_task(task, plan)
                    task.result = result
                    task.status = TaskStatus.COMPLETED
                    task.completed_at = get_utc_now().isoformat()

                    plan.context[f"task_{task.task_id}_result"] = result

                    if on_task_complete:
                        await on_task_complete(task, plan)

                except Exception as e:
                    task.error = str(e)
                    task.retry_count += 1

                    if task.retry_count < task.max_retries:
                        task.status = TaskStatus.PENDING
                        continue

                    task.status = TaskStatus.FAILED

                    if on_task_failed:
                        should_continue = await on_task_failed(task, plan)
                        if not should_continue:
                            plan.status = "failed"
                            return plan

                    replan = await self._replan_on_failure(task, plan)
                    if replan:
                        missing = [t.task_type.value for t in replan if t.task_type not in self.task_executors]
                        if missing:
                            logger.warning(f"Replan tasks missing executors: {missing}, skip replan")
                        else:
                            plan.tasks = plan.tasks[: i + 1] + replan

                plan.progress = (i + 1) / max(len(plan.tasks), 1)
                plan.current_task_index = i
                i += 1

            plan.status = "completed"
            plan.completed_at = get_utc_now().isoformat()
            plan.progress = 1.0

        except Exception as e:
            plan.status = "failed"
            plan.context["error"] = str(e)

        return plan

    async def _execute_task(
        self,
        task: Task,
        plan: ExecutionPlan,
    ) -> Any:
        executor = self.task_executors.get(task.task_type)

        if not executor:
            raise ValueError(f"No executor found for task type: {task.task_type}")

        kwargs = {**task.parameters, "context": plan.context, "task": task}
        return await executor(**kwargs)

    def _check_dependencies(
        self,
        task: Task,
        plan: ExecutionPlan,
    ) -> bool:
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
        plan: ExecutionPlan,
    ) -> Optional[List[Task]]:
        import uuid

        if failed_task.task_type == TaskType.CREATE_WORLDVIEW:
            return [
                Task(
                    task_id=str(uuid.uuid4()),
                    task_type=TaskType.CREATE_WORLDVIEW,
                    description="Create simplified worldview after failure.",
                    parameters={"simplified": True, **failed_task.parameters},
                    created_at=get_utc_now().isoformat(),
                    max_retries=1,
                )
            ]
        if failed_task.task_type == TaskType.SEARCH_KNOWLEDGE:
            return []
        return None

    # ==================== Plan adjustment ====================

    def add_task(
        self,
        plan: ExecutionPlan,
        task: Task,
        insert_after: Optional[str] = None,
    ) -> ExecutionPlan:
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
        task_id: str,
    ) -> ExecutionPlan:
        plan.tasks = [t for t in plan.tasks if t.task_id != task_id]
        return plan

    def get_next_task(self, plan: ExecutionPlan) -> Optional[Task]:
        for task in plan.tasks:
            if task.status == TaskStatus.PENDING and self._check_dependencies(task, plan):
                return task
        return None

    def get_plan_summary(self, plan: ExecutionPlan) -> Dict[str, Any]:
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
            "current_task": self.get_next_task(plan).description if self.get_next_task(plan) else None,
        }
