# 03 - 动态计划管理

## 文件位置

`backend/app/services/agent/execution/dynamic_plan.py`

## 类设计

> ⚠️ 兼容约束（与现有实现一致）：
> - `task_id` 使用 **int**（参数解析器依赖数值 ID），动态任务用递增整数。
> - `status` 使用 `pending/running/completed/failed/skipped`，与前端 TaskList 保持一致。
> - 任务对象需保留 `checkpoint/acceptance/is_remedy/params/description/tool` 等字段。

```python
from typing import List, Dict, Any, Optional
from dataclasses import dataclass, field
from enum import Enum


class TaskStatus(Enum):
    """任务状态"""
    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    SKIPPED = "skipped"
    FAILED = "failed"


@dataclass
class Task:
    """任务定义"""
    task_id: int
    title: str
    tool: str
    params: Dict[str, Any] = field(default_factory=dict)
    description: str = ""
    status: TaskStatus = TaskStatus.PENDING
    is_dynamic: bool = False  # 是否动态添加的任务


class DynamicPlan:
    """动态计划管理

    支持：
    - 获取下一个待执行任务
    - 在当前位置后插入新任务
    - 跳过任务
    - 标记任务完成
    - 获取计划状态
    """

    def __init__(self, tasks: List[Dict[str, Any]]):
        """初始化

        Args:
            tasks: 初始任务列表（来自 PlanGenerator）
        """
        self._tasks: List[Task] = []
        self._current_index: int = -1

        # 转换为 Task 对象
        for i, t in enumerate(tasks):
            self._tasks.append(Task(
                task_id=int(t.get("task_id", i + 1)),
                title=t.get("title", f"任务{i + 1}"),
                tool=t.get("tool", "unknown"),
                params=t.get("params", {}),
                description=t.get("description", ""),
                status=TaskStatus.PENDING,
                is_dynamic=False
            ))

    def has_pending(self) -> bool:
        """是否还有待执行任务"""
        return any(t.status == TaskStatus.PENDING for t in self._tasks)

    def get_next(self) -> Optional[Dict[str, Any]]:
        """获取下一个待执行任务

        Returns:
            任务字典，或 None（无待执行任务）
        """
        for i, task in enumerate(self._tasks):
            if i > self._current_index and task.status == TaskStatus.PENDING:
                self._current_index = i
                task.status = TaskStatus.RUNNING
                return self._task_to_dict(task)
        return None

    def get_remaining(self) -> List[Dict[str, Any]]:
        """获取剩余待执行任务"""
        remaining = []
        for i, task in enumerate(self._tasks):
            if i > self._current_index and task.status == TaskStatus.PENDING:
                remaining.append(self._task_to_dict(task))
        return remaining

    def insert_after_current(self, task_dict: Dict[str, Any]) -> str:
        """在当前任务后插入新任务

        Args:
            task_dict: 新任务配置

        Returns:
            新任务的 task_id
        """
        # 生成新的 task_id
        new_id = max(t.task_id for t in self._tasks) + 1

        new_task = Task(
            task_id=new_id,
            title=task_dict.get("title", "动态任务"),
            tool=task_dict.get("tool", "unknown"),
            params=task_dict.get("params", {}),
            description=task_dict.get("description", ""),
            status=TaskStatus.PENDING,
            is_dynamic=True
        )

        # 插入到当前位置之后
        insert_pos = self._current_index + 1
        self._tasks.insert(insert_pos, new_task)

        return new_id

    def skip_next(self) -> Optional[Dict[str, Any]]:
        """跳过下一个任务

        Returns:
            被跳过的任务，或 None
        """
        for i, task in enumerate(self._tasks):
            if i > self._current_index and task.status == TaskStatus.PENDING:
                task.status = TaskStatus.SKIPPED
                return self._task_to_dict(task)
        return None

    def mark_completed(self, task_id: str) -> bool:
        """标记任务完成

        Args:
            task_id: 任务ID

        Returns:
            是否成功
        """
        for task in self._tasks:
            if task.task_id == task_id:
                task.status = TaskStatus.COMPLETED
                return True
        return False

    def mark_failed(self, task_id: str) -> bool:
        """标记任务失败"""
        for task in self._tasks:
            if task.task_id == task_id:
                task.status = TaskStatus.FAILED
                return True
        return False

    def to_display_list(self) -> List[Dict[str, Any]]:
        """转换为前端展示格式"""
        return [
            {
                "task_id": t.task_id,
                "title": t.title,
                "tool": t.tool,
                "status": t.status.value,
                "is_dynamic": t.is_dynamic
            }
            for t in self._tasks
        ]

    def get_completed_count(self) -> int:
        """获取已完成任务数"""
        return sum(1 for t in self._tasks if t.status == TaskStatus.COMPLETED)

    def get_total_count(self) -> int:
        """获取总任务数"""
        return len(self._tasks)

    def _task_to_dict(self, task: Task) -> Dict[str, Any]:
        """Task 对象转字典"""
        return {
            "task_id": task.task_id,
            "title": task.title,
            "tool": task.tool,
            "params": task.params,
            "description": task.description,
            "status": task.status.value,
            "is_dynamic": task.is_dynamic
        }
```

## 使用示例

```python
# 初始化
tasks = [
    {"task_id": "1", "title": "获取上下文", "tool": "get_writing_context"},
    {"task_id": "2", "title": "续写章节", "tool": "smart_continue"},
    {"task_id": "3", "title": "应用编辑", "tool": "apply_chapter_edit"},
]
plan = DynamicPlan(tasks)

# 获取下一个任务
task = plan.get_next()  # 返回任务1

# 执行后，插入新任务
plan.insert_after_current({
    "title": "获取世界观",
    "tool": "get_worldview_summary"
})

# 标记完成
plan.mark_completed("1")

# 获取下一个（会是刚插入的任务）
        task = plan.get_next()  # 返回 "获取世界观"

# 查看当前状态
print(plan.to_display_list())
# [
#   {"task_id": "1", "status": "completed", ...},
#   {"task_id": "4", "status": "running", "is_dynamic": True, ...},
#   {"task_id": "2", "status": "pending", ...},
#   {"task_id": "3", "status": "pending", ...},
# ]
```

## 前端展示映射

| 状态 | 图标 | 颜色 |
|------|------|------|
| pending | ⏳ | 灰色 |
| running | 🔄 | 蓝色 |
| completed | ✅ | 绿色 |
| skipped | ⏭️ | 黄色 |
| failed | ❌ | 红色 |
