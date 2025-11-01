"""
高级任务队列管理系统

提供高性能、可扩展的任务队列功能，支持优先级调度、批量处理、失败重试、监控统计等。
"""

import asyncio
import time
import uuid
import json
import threading
from typing import Dict, Any, List, Optional, Callable, Union, TypeVar
from dataclasses import dataclass, field
from enum import Enum
from datetime import datetime, timedelta
from collections import defaultdict, deque
import heapq

from ..utils.logger import get_logger
from ..utils.error_handler import robust_retry

logger = get_logger("advanced_task_queue")

T = TypeVar('T')


class TaskStatus(Enum):
    """任务状态"""
    PENDING = "pending"
    QUEUED = "queued"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"
    RETRYING = "retrying"


class TaskPriority(Enum):
    """任务优先级"""
    LOW = 1
    NORMAL = 2
    HIGH = 3
    CRITICAL = 4
    URGENT = 5


class TaskType(Enum):
    """任务类型"""
    ONE_TIME = "one_time"           # 一次性任务
    RECURRING = "recurring"         # 周期性任务
    DELAYED = "delayed"            # 延迟任务
    DEPENDENT = "dependent"        # 依赖任务
    BATCH = "batch"               # 批量任务


@dataclass
class TaskResult:
    """任务结果"""
    task_id: str
    success: bool
    result: Any = None
    error: Optional[str] = None
    execution_time: float = 0.0
    retry_count: int = 0
    completed_at: Optional[datetime] = None
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class Task:
    """任务定义"""
    task_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    name: str = ""
    task_type: TaskType = TaskType.ONE_TIME
    priority: TaskPriority = TaskPriority.NORMAL
    handler: Optional[Callable] = None
    args: tuple = field(default_factory=tuple)
    kwargs: Dict[str, Any] = field(default_factory=dict)

    # 调度相关
    scheduled_at: Optional[datetime] = None
    delay_seconds: float = 0.0
    max_retries: int = 3
    retry_delay: float = 1.0
    timeout: float = 30.0

    # 依赖相关
    dependencies: List[str] = field(default_factory=list)
    dependents: List[str] = field(default_factory=list)

    # 周期性任务相关
    cron_expression: Optional[str] = None
    interval_seconds: Optional[float] = None

    # 批量任务相关
    batch_items: List[Any] = field(default_factory=list)
    batch_size: int = 10

    # 状态相关
    status: TaskStatus = TaskStatus.PENDING
    created_at: datetime = field(default_factory=datetime.now)
    queued_at: Optional[datetime] = None
    started_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None

    # 运行时
    current_retry: int = 0
    execution_context: Dict[str, Any] = field(default_factory=dict)
    result: Optional[TaskResult] = None

    # 元数据
    metadata: Dict[str, Any] = field(default_factory=dict)
    tags: List[str] = field(default_factory=list)


class TaskQueue:
    """任务队列"""

    def __init__(self, name: str, max_size: int = 1000):
        """
        初始化任务队列

        Args:
            name: 队列名称
            max_size: 最大队列大小
        """
        self.name = name
        self.max_size = max_size
        self._queue = []
        self._task_index = {}  # task_id -> index in heap
        self._lock = threading.Lock()
        self._stats = {
            "total_enqueued": 0,
            "total_dequeued": 0,
            "total_completed": 0,
            "total_failed": 0,
            "current_size": 0,
            "peak_size": 0
        }

    def enqueue(self, task: Task) -> bool:
        """
        将任务加入队列

        Args:
            task: 任务对象

        Returns:
            bool: 是否成功入队
        """
        with self._lock:
            if len(self._queue) >= self.max_size:
                logger.warning(f"Task queue {self.name} is full")
                return False

            task.status = TaskStatus.QUEUED
            task.queued_at = datetime.now()

            # 使用堆实现优先级队列
            priority_value = -task.priority.value  # 负值实现最大堆
            heap_item = (priority_value, task.scheduled_at or datetime.min, task.task_id, task)

            heapq.heappush(self._queue, heap_item)
            self._task_index[task.task_id] = len(self._queue) - 1

            self._stats["total_enqueued"] += 1
            self._stats["current_size"] = len(self._queue)
            self._stats["peak_size"] = max(self._stats["peak_size"], len(self._queue))

            logger.debug(f"Task {task.task_id} enqueued to {self.name}")
            return True

    def dequeue(self) -> Optional[Task]:
        """
        从队列中取出任务

        Returns:
            Optional[Task]: 任务对象，如果队列为空则返回None
        """
        with self._lock:
            if not self._queue:
                return None

            # 取出最高优先级的任务
            priority, scheduled_at, task_id, task = heapq.heappop(self._queue)
            del self._task_index[task_id]

            # 检查是否到了执行时间
            if scheduled_at > datetime.now():
                # 还没到时间，重新入队
                heapq.heappush(self._queue, (priority, scheduled_at, task_id, task))
                self._task_index[task_id] = len(self._queue) - 1
                return None

            self._stats["total_dequeued"] += 1
            self._stats["current_size"] = len(self._queue)

            logger.debug(f"Task {task.task_id} dequeued from {self.name}")
            return task

    def peek(self) -> Optional[Task]:
        """
        查看队列头部的任务（不取出）

        Returns:
            Optional[Task]: 任务对象，如果队列为空则返回None
        """
        with self._lock:
            if not self._queue:
                return None

            priority, scheduled_at, task_id, task = self._queue[0]

            # 检查是否到了执行时间
            if scheduled_at > datetime.now():
                return None

            return task

    def size(self) -> int:
        """获取队列大小"""
        with self._lock:
            return len(self._queue)

    def is_empty(self) -> bool:
        """检查队列是否为空"""
        with self._lock:
            return len(self._queue) == 0

    def get_stats(self) -> Dict[str, Any]:
        """获取队列统计信息"""
        with self._lock:
            return self._stats.copy()

    def remove_task(self, task_id: str) -> bool:
        """
        从队列中移除指定任务

        Args:
            task_id: 任务ID

        Returns:
            bool: 是否成功移除
        """
        with self._lock:
            if task_id not in self._task_index:
                return False

            index = self._task_index[task_id]
            if index < len(self._queue):
                # 标记为已删除
                self._queue[index] = self._queue[-1]
                self._queue.pop()
                heapq.heapify(self._queue)
                del self._task_index[task_id]

                # 重建索引
                self._task_index.clear()
                for i, (_, _, tid, _) in enumerate(self._queue):
                    self._task_index[tid] = i

                self._stats["current_size"] = len(self._queue)
                return True

            return False


class TaskScheduler:
    """任务调度器"""

    def __init__(self, max_workers: int = 10):
        """
        初始化任务调度器

        Args:
            max_workers: 最大工作线程数
        """
        self.max_workers = max_workers
        self.queues: Dict[str, TaskQueue] = {}
        self.running_tasks: Dict[str, Task] = {}
        self.completed_tasks: Dict[str, TaskResult] = {}
        self.failed_tasks: Dict[str, Task] = {}

        self._workers = []
        self._scheduler_task: Optional[asyncio.Task] = None
        self._running = False
        self._lock = threading.Lock()

        # 统计信息
        self._stats = {
            "total_tasks": 0,
            "completed_tasks": 0,
            "failed_tasks": 0,
            "running_tasks": 0,
            "avg_execution_time": 0.0,
            "throughput_per_second": 0.0
        }

    def create_queue(self, name: str, max_size: int = 1000) -> TaskQueue:
        """
        创建任务队列

        Args:
            name: 队列名称
            max_size: 最大队列大小

        Returns:
            TaskQueue: 任务队列对象
        """
        with self._lock:
            if name in self.queues:
                return self.queues[name]

            queue = TaskQueue(name, max_size)
            self.queues[name] = queue
            logger.info(f"Created task queue: {name}")
            return queue

    def get_queue(self, name: str) -> Optional[TaskQueue]:
        """
        获取任务队列

        Args:
            name: 队列名称

        Returns:
            Optional[TaskQueue]: 任务队列对象
        """
        with self._lock:
            return self.queues.get(name)

    def submit_task(
        self,
        handler: Callable,
        args: tuple = (),
        kwargs: Dict[str, Any] = None,
        queue_name: str = "default",
        priority: TaskPriority = TaskPriority.NORMAL,
        delay_seconds: float = 0.0,
        max_retries: int = 3,
        timeout: float = 30.0,
        task_type: TaskType = TaskType.ONE_TIME,
        **task_kwargs
    ) -> str:
        """
        提交任务

        Args:
            handler: 任务处理函数
            args: 位置参数
            kwargs: 关键字参数
            queue_name: 队列名称
            priority: 任务优先级
            delay_seconds: 延迟执行时间（秒）
            max_retries: 最大重试次数
            timeout: 超时时间
            task_type: 任务类型
            **task_kwargs: 其他任务参数

        Returns:
            str: 任务ID
        """
        kwargs = kwargs or {}

        # 创建任务对象
        task = Task(
            handler=handler,
            args=args,
            kwargs=kwargs,
            priority=priority,
            delay_seconds=delay_seconds,
            max_retries=max_retries,
            timeout=timeout,
            task_type=task_type,
            scheduled_at=datetime.now() + timedelta(seconds=delay_seconds),
            **task_kwargs
        )

        # 获取或创建队列
        queue = self.get_queue(queue_name) or self.create_queue(queue_name)

        # 将任务加入队列
        if queue.enqueue(task):
            with self._lock:
                self._stats["total_tasks"] += 1
            logger.info(f"Task {task.task_id} submitted to queue {queue_name}")
            return task.task_id
        else:
            logger.error(f"Failed to enqueue task {task.task_id}")
            raise Exception("Task queue is full")

    def submit_batch_task(
        self,
        handler: Callable,
        items: List[Any],
        batch_size: int = 10,
        queue_name: str = "default",
        **kwargs
    ) -> str:
        """
        提交批量任务

        Args:
            handler: 任务处理函数
            items: 批量处理项目
            batch_size: 批处理大小
            queue_name: 队列名称
            **kwargs: 其他参数

        Returns:
            str: 任务ID
        """
        return self.submit_task(
            handler=handler,
            queue_name=queue_name,
            task_type=TaskType.BATCH,
            batch_items=items,
            batch_size=batch_size,
            **kwargs
        )

    async def start(self) -> None:
        """启动调度器"""
        if self._running:
            return

        self._running = True

        # 启动工作线程
        for i in range(self.max_workers):
            worker = asyncio.create_task(self._worker(f"worker-{i}"))
            self._workers.append(worker)

        # 启动调度器主循环
        self._scheduler_task = asyncio.create_task(self._scheduler_loop())

        logger.info(f"Task scheduler started with {self.max_workers} workers")

    async def stop(self) -> None:
        """停止调度器"""
        if not self._running:
            return

        self._running = False

        # 停止调度器主循环
        if self._scheduler_task:
            self._scheduler_task.cancel()
            try:
                await self._scheduler_task
            except asyncio.CancelledError:
                pass

        # 等待所有工作线程完成
        await asyncio.gather(*self._workers, return_exceptions=True)

        logger.info("Task scheduler stopped")

    async def _worker(self, worker_id: str) -> None:
        """工作线程"""
        logger.info(f"Worker {worker_id} started")

        while self._running:
            task = None

            # 从所有队列中获取任务
            for queue in self.queues.values():
                task = queue.dequeue()
                if task:
                    break

            if not task:
                await asyncio.sleep(0.1)
                continue

            # 执行任务
            try:
                await self._execute_task(task)
            except Exception as e:
                logger.error(f"Worker {worker_id} failed to execute task {task.task_id}: {e}")

        logger.info(f"Worker {worker_id} stopped")

    async def _scheduler_loop(self) -> None:
        """调度器主循环"""
        logger.info("Scheduler loop started")

        while self._running:
            try:
                # 处理周期性任务
                await self._handle_recurring_tasks()

                # 处理延迟任务
                await self._handle_delayed_tasks()

                # 处理依赖任务
                await self._handle_dependent_tasks()

                # 更新统计信息
                self._update_stats()

                await asyncio.sleep(1.0)  # 每秒检查一次

            except asyncio.CancelledError:
                break
            except Exception as e:
                logger.error(f"Scheduler loop error: {e}")
                await asyncio.sleep(1.0)

        logger.info("Scheduler loop stopped")

    async def _execute_task(self, task: Task) -> None:
        """
        执行任务

        Args:
            task: 任务对象
        """
        task.status = TaskStatus.RUNNING
        task.started_at = datetime.now()

        with self._lock:
            self.running_tasks[task.task_id] = task
            self._stats["running_tasks"] += 1

        try:
            logger.debug(f"Executing task {task.task_id}")

            # 根据任务类型执行
            if task.task_type == TaskType.BATCH:
                result = await self._execute_batch_task(task)
            else:
                result = await self._execute_single_task(task)

            task.result = result
            task.status = TaskStatus.COMPLETED
            task.completed_at = datetime.now()

            # 记录成功结果
            self.completed_tasks[task.task_id] = result

            with self._lock:
                self._stats["completed_tasks"] += 1
                self._stats["running_tasks"] -= 1

            logger.info(f"Task {task.task_id} completed successfully")

        except Exception as e:
            error_msg = str(e)
            logger.error(f"Task {task.task_id} failed: {error_msg}")

            # 处理重试
            if task.current_retry < task.max_retries:
                task.current_retry += 1
                task.status = TaskStatus.RETRYING

                # 延迟重试
                retry_delay = task.retry_delay * (2 ** task.current_retry)  # 指数退避
                task.scheduled_at = datetime.now() + timedelta(seconds=retry_delay)

                # 重新入队
                queue = self.get_queue("default") or self.create_queue("retry")
                queue.enqueue(task)

                logger.info(f"Task {task.task_id} will retry in {retry_delay}s (attempt {task.current_retry})")

            else:
                task.status = TaskStatus.FAILED
                task.completed_at = datetime.now()

                # 记录失败结果
                self.failed_tasks[task.task_id] = task

                with self._lock:
                    self._stats["failed_tasks"] += 1
                    self._stats["running_tasks"] -= 1

                logger.error(f"Task {task.task_id} failed permanently after {task.max_retries} retries")

        finally:
            # 从运行任务列表中移除
            self.running_tasks.pop(task.task_id, None)

    async def _execute_single_task(self, task: Task) -> TaskResult:
        """
        执行单个任务

        Args:
            task: 任务对象

        Returns:
            TaskResult: 任务结果
        """
        start_time = time.time()

        try:
            # 执行任务处理函数
            if asyncio.iscoroutinefunction(task.handler):
                result = await asyncio.wait_for(
                    task.handler(*task.args, **task.kwargs),
                    timeout=task.timeout
                )
            else:
                # 在线程池中执行同步函数
                loop = asyncio.get_event_loop()
                result = await asyncio.wait_for(
                    loop.run_in_executor(None, task.handler, *task.args, **task.kwargs),
                    timeout=task.timeout
                )

            execution_time = time.time() - start_time

            return TaskResult(
                task_id=task.task_id,
                success=True,
                result=result,
                execution_time=execution_time,
                retry_count=task.current_retry,
                completed_at=datetime.now()
            )

        except Exception as e:
            execution_time = time.time() - start_time

            return TaskResult(
                task_id=task.task_id,
                success=False,
                error=str(e),
                execution_time=execution_time,
                retry_count=task.current_retry,
                completed_at=datetime.now()
            )

    async def _execute_batch_task(self, task: Task) -> TaskResult:
        """
        执行批量任务

        Args:
            task: 任务对象

        Returns:
            TaskResult: 任务结果
        """
        start_time = time.time()
        batch_results = []

        try:
            items = task.batch_items
            batch_size = task.batch_size

            # 分批处理
            for i in range(0, len(items), batch_size):
                batch_items = items[i:i + batch_size]

                # 并行处理批次内的项目
                if asyncio.iscoroutinefunction(task.handler):
                    batch_tasks = [
                        task.handler(item, **task.kwargs)
                        for item in batch_items
                    ]
                    batch_results.extend(await asyncio.gather(*batch_tasks, return_exceptions=True))
                else:
                    loop = asyncio.get_event_loop()
                    batch_tasks = [
                        loop.run_in_executor(None, task.handler, item, **task.kwargs)
                        for item in batch_items
                    ]
                    batch_results.extend(await asyncio.gather(*batch_tasks, return_exceptions=True))

            execution_time = time.time() - start_time

            # 统计成功和失败的数量
            success_count = sum(1 for r in batch_results if not isinstance(r, Exception))
            error_count = len(batch_results) - success_count

            return TaskResult(
                task_id=task.task_id,
                success=error_count == 0,
                result={
                    "batch_size": len(items),
                    "success_count": success_count,
                    "error_count": error_count,
                    "results": batch_results
                },
                execution_time=execution_time,
                retry_count=task.current_retry,
                completed_at=datetime.now()
            )

        except Exception as e:
            execution_time = time.time() - start_time

            return TaskResult(
                task_id=task.task_id,
                success=False,
                error=str(e),
                execution_time=execution_time,
                retry_count=task.current_retry,
                completed_at=datetime.now()
            )

    async def _handle_recurring_tasks(self) -> None:
        """处理周期性任务"""
        # 这里可以实现cron表达式解析和周期性任务调度
        pass

    async def _handle_delayed_tasks(self) -> None:
        """处理延迟任务"""
        # 延迟任务已经在队列中处理，这里可以添加额外的逻辑
        pass

    async def _handle_dependent_tasks(self) -> None:
        """处理依赖任务"""
        # 这里可以实现依赖任务的调度逻辑
        pass

    def _update_stats(self) -> None:
        """更新统计信息"""
        with self._lock:
            total_completed = self._stats["completed_tasks"]
            total_time = sum(
                result.execution_time for result in self.completed_tasks.values()
            )

            if total_completed > 0:
                self._stats["avg_execution_time"] = total_time / total_completed

    def get_task_status(self, task_id: str) -> Optional[TaskStatus]:
        """
        获取任务状态

        Args:
            task_id: 任务ID

        Returns:
            Optional[TaskStatus]: 任务状态
        """
        # 检查运行中的任务
        if task_id in self.running_tasks:
            return self.running_tasks[task_id].status

        # 检查已完成的任务
        if task_id in self.completed_tasks:
            return TaskStatus.COMPLETED

        # 检查失败的任务
        if task_id in self.failed_tasks:
            return TaskStatus.FAILED

        # 检查队列中的任务
        for queue in self.queues.values():
            # 这里需要实现队列中的任务查找
            pass

        return None

    def get_task_result(self, task_id: str) -> Optional[TaskResult]:
        """
        获取任务结果

        Args:
            task_id: 任务ID

        Returns:
            Optional[TaskResult]: 任务结果
        """
        return self.completed_tasks.get(task_id)

    def get_stats(self) -> Dict[str, Any]:
        """获取统计信息"""
        with self._lock:
            stats = self._stats.copy()

            # 添加队列统计
            stats["queues"] = {
                name: queue.get_stats()
                for name, queue in self.queues.items()
            }

            return stats

    def cancel_task(self, task_id: str) -> bool:
        """
        取消任务

        Args:
            task_id: 任务ID

        Returns:
            bool: 是否成功取消
        """
        # 尝试从队列中移除
        for queue in self.queues.values():
            if queue.remove_task(task_id):
                logger.info(f"Task {task_id} cancelled from queue")
                return True

        # 如果任务正在运行，无法取消
        if task_id in self.running_tasks:
            logger.warning(f"Cannot cancel running task {task_id}")
            return False

        return False


# 全局调度器实例
_task_scheduler: Optional[TaskScheduler] = None


def get_task_scheduler(max_workers: int = 10) -> TaskScheduler:
    """获取全局任务调度器实例"""
    global _task_scheduler
    if _task_scheduler is None:
        _task_scheduler = TaskScheduler(max_workers)
    return _task_scheduler


# 便捷函数
async def start_task_scheduler(max_workers: int = 10) -> None:
    """启动任务调度器"""
    scheduler = get_task_scheduler(max_workers)
    await scheduler.start()


async def stop_task_scheduler() -> None:
    """停止任务调度器"""
    scheduler = get_task_scheduler()
    await scheduler.stop()


def submit_task(
    handler: Callable,
    args: tuple = (),
    kwargs: Dict[str, Any] = None,
    queue_name: str = "default",
    priority: TaskPriority = TaskPriority.NORMAL,
    **task_kwargs
) -> str:
    """提交任务的便捷函数"""
    scheduler = get_task_scheduler()
    return scheduler.submit_task(
        handler=handler,
        args=args,
        kwargs=kwargs,
        queue_name=queue_name,
        priority=priority,
        **task_kwargs
    )


async def get_task_result(task_id: str) -> Optional[TaskResult]:
    """获取任务结果的便捷函数"""
    scheduler = get_task_scheduler()
    return scheduler.get_task_result(task_id)


def get_task_stats() -> Dict[str, Any]:
    """获取任务统计的便捷函数"""
    scheduler = get_task_scheduler()
    return scheduler.get_stats()