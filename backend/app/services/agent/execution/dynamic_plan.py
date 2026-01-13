# -*- coding: utf-8 -*-
"""
DynamicPlan - 动态计划管理

约束：
- task_id 使用 int（参数解析器依赖）
- status 使用 pending/running/completed/failed/skipped
- 保留 checkpoint/acceptance/is_remedy/params/description/tool 等字段
"""

from typing import List, Dict, Any, Optional, Iterable


class DynamicPlan:
    """动态计划管理"""

    def __init__(self, tasks: List[Dict[str, Any]]):
        self._current_index: int = -1
        self._tasks: List[Dict[str, Any]] = []
        self.replace_tasks(tasks)

    @property
    def current_index(self) -> int:
        return self._current_index

    @property
    def tasks(self) -> List[Dict[str, Any]]:
        return self._tasks

    def has_pending(self) -> bool:
        return any(t.get("status") == "pending" for t in self._tasks)

    def get_total_count(self) -> int:
        return len(self._tasks)

    def get_next(self) -> Optional[Dict[str, Any]]:
        """获取下一个待执行任务，并标记为 running"""
        for idx in range(self._current_index + 1, len(self._tasks)):
            task = self._tasks[idx]
            if task.get("status") == "pending":
                self._current_index = idx
                task["status"] = "running"
                return task
        return None

    def get_remaining(self) -> List[Dict[str, Any]]:
        """获取剩余待执行任务"""
        remaining: List[Dict[str, Any]] = []
        for idx in range(self._current_index + 1, len(self._tasks)):
            task = self._tasks[idx]
            if task.get("status") == "pending":
                remaining.append(task)
        return remaining

    def mark_completed(self, task_id: int) -> bool:
        task = self._find_task(task_id)
        if not task:
            return False
        task["status"] = "completed"
        return True

    def mark_failed(self, task_id: int) -> bool:
        task = self._find_task(task_id)
        if not task:
            return False
        task["status"] = "failed"
        return True

    def skip_next(self) -> Optional[Dict[str, Any]]:
        """跳过下一个 pending 任务"""
        for idx in range(self._current_index + 1, len(self._tasks)):
            task = self._tasks[idx]
            if task.get("status") == "pending":
                task["status"] = "skipped"
                return task
        return None

    def insert_after_current(self, task_dict: Dict[str, Any]) -> int:
        """在当前任务后插入新任务（标记为 is_dynamic）"""
        new_task = dict(task_dict or {})
        new_task_id = self._next_task_id()
        new_task["task_id"] = new_task_id
        new_task.setdefault("status", "pending")
        new_task["status"] = self._normalize_status(new_task.get("status"))
        new_task["is_dynamic"] = True

        insert_pos = self._current_index + 1
        self._tasks.insert(insert_pos, new_task)
        return new_task_id

    def update_task(self, index: int, task: Dict[str, Any]) -> Dict[str, Any]:
        """更新任务（保留 status/is_dynamic 等关键字段）"""
        if index < 0 or index >= len(self._tasks):
            return task
        current = self._tasks[index]
        merged = dict(current)
        merged.update(task or {})
        merged.setdefault("status", current.get("status", "pending"))
        merged["status"] = self._normalize_status(merged.get("status"))
        merged.setdefault("is_dynamic", current.get("is_dynamic", False))
        merged["task_id"] = self._coerce_task_id(merged.get("task_id"), fallback_id=current.get("task_id"))
        self._tasks[index] = merged
        return merged

    def replace_tasks(
        self,
        tasks: List[Dict[str, Any]],
        current_index: Optional[int] = None,
        new_task_ids: Optional[Iterable[int]] = None,
    ) -> None:
        """替换任务列表（保留已知状态）"""
        status_map = {t.get("task_id"): t.get("status") for t in self._tasks}
        dynamic_ids = set(new_task_ids or [])
        self._tasks = self._normalize_tasks(tasks, status_map=status_map, new_task_ids=dynamic_ids)
        if current_index is not None:
            self._current_index = min(current_index, len(self._tasks) - 1)
        elif self._current_index >= len(self._tasks):
            self._current_index = len(self._tasks) - 1

    def to_display_list(self) -> List[Dict[str, Any]]:
        """用于前端展示的任务列表（保留原字段）"""
        return [self._display_task(t) for t in self._tasks]

    def _display_task(self, task: Dict[str, Any]) -> Dict[str, Any]:
        data = dict(task)
        data.setdefault("status", "pending")
        data["status"] = self._normalize_status(data.get("status"))
        data.setdefault("is_dynamic", False)
        return data

    def _find_task(self, task_id: int) -> Optional[Dict[str, Any]]:
        for task in self._tasks:
            if task.get("task_id") == task_id:
                return task
        return None

    def _normalize_tasks(
        self,
        tasks: List[Dict[str, Any]],
        status_map: Optional[Dict[Any, str]] = None,
        new_task_ids: Optional[set] = None,
    ) -> List[Dict[str, Any]]:
        normalized: List[Dict[str, Any]] = []
        used_ids = set()
        max_id = self._max_task_id(tasks)

        for raw in tasks or []:
            task = dict(raw) if isinstance(raw, dict) else {"description": str(raw)}
            task_id = self._coerce_task_id(task.get("task_id"), fallback_id=None)
            if not task_id:
                max_id += 1
                task_id = max_id
            while task_id in used_ids:
                task_id += 1
            used_ids.add(task_id)

            task["task_id"] = task_id
            status = task.get("status") or (status_map.get(task_id) if status_map else None) or "pending"
            task["status"] = self._normalize_status(status)

            if new_task_ids and task_id in new_task_ids:
                task["is_dynamic"] = True
            task.setdefault("is_dynamic", False)

            normalized.append(task)

        return normalized

    @staticmethod
    def _normalize_status(status: Optional[str]) -> str:
        if status == "in_progress":
            return "running"
        return status or "pending"

    @staticmethod
    def _coerce_task_id(value: Any, fallback_id: Optional[int]) -> Optional[int]:
        if isinstance(value, int):
            return value
        if isinstance(value, str) and value.isdigit():
            return int(value)
        return fallback_id

    def _max_task_id(self, tasks: List[Dict[str, Any]]) -> int:
        max_id = 0
        for task in tasks or []:
            task_id = task.get("task_id") if isinstance(task, dict) else None
            try:
                task_id = int(task_id)
            except (TypeError, ValueError):
                continue
            max_id = max(max_id, task_id)
        return max_id

    def _next_task_id(self) -> int:
        return self._max_task_id(self._tasks) + 1
