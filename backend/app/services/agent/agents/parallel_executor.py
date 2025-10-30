"""
并行任务执行模块 (Parallelization)

这是Agentic AI的9大核心工作流模式之一

功能:
1. 将大任务拆分为独立子任务
2. 并发执行多个子任务
3. 汇总并合并结果
4. 大幅提升执行速度 (2-5倍)

使用场景:
- 生成5个章节大纲 → 并发生成
- 批量分析多个章节 → 并发分析
- 创建多个角色 → 并发创建

性能对比:
- 串行: 5个任务 × 10秒 = 50秒
- 并行: max(10秒) = 10秒 (提速5倍)
"""

from typing import Dict, List, Optional, Any, Callable, TypeVar
from datetime import datetime
from pydantic import BaseModel
from enum import Enum
import asyncio


T = TypeVar('T')


class SubTask(BaseModel):
    """子任务"""
    task_id: str
    description: str
    parameters: Dict[str, Any]
    status: str = "pending"  # pending/running/completed/failed
    result: Optional[Any] = None
    error: Optional[str] = None
    start_time: Optional[str] = None
    end_time: Optional[str] = None
    duration_seconds: float = 0.0


class ParallelExecutionResult(BaseModel):
    """并行执行结果"""
    total_tasks: int
    completed_tasks: int
    failed_tasks: int
    results: List[Any]  # 成功任务的结果列表
    errors: List[str]  # 失败任务的错误列表
    total_duration_seconds: float  # 总耗时
    speedup_factor: float  # 加速倍数 (相对于串行执行)


class ParallelExecutor:
    """并行执行器"""

    def __init__(self, max_concurrent: int = 5):
        """
        初始化并行执行器

        Args:
            max_concurrent: 最大并发数
        """
        self.max_concurrent = max_concurrent

    async def execute_parallel(
        self,
        tasks: List[SubTask],
        executor_fn: Callable[[SubTask], Any],
        on_task_complete: Optional[Callable] = None,
        on_task_failed: Optional[Callable] = None
    ) -> ParallelExecutionResult:
        """
        并行执行多个任务

        Args:
            tasks: 任务列表
            executor_fn: 执行函数 (task) -> result
            on_task_complete: 任务完成回调
            on_task_failed: 任务失败回调

        Returns:
            ParallelExecutionResult: 执行结果
        """
        start_time = datetime.now()

        # 创建信号量控制并发数
        semaphore = asyncio.Semaphore(self.max_concurrent)

        async def execute_one(task: SubTask):
            """执行单个任务"""
            async with semaphore:
                task.status = "running"
                task.start_time = datetime.now().isoformat()

                try:
                    # 执行任务
                    result = await executor_fn(task)
                    task.result = result
                    task.status = "completed"

                    if on_task_complete:
                        await on_task_complete(task)

                except Exception as e:
                    task.error = str(e)
                    task.status = "failed"

                    if on_task_failed:
                        await on_task_failed(task, e)

                finally:
                    task.end_time = datetime.now().isoformat()
                    if task.start_time:
                        start = datetime.fromisoformat(task.start_time)
                        end = datetime.fromisoformat(task.end_time)
                        task.duration_seconds = (end - start).total_seconds()

        # 并发执行所有任务
        await asyncio.gather(*[execute_one(task) for task in tasks])

        # 统计结果
        end_time = datetime.now()
        total_duration = (end_time - start_time).total_seconds()

        completed = [t for t in tasks if t.status == "completed"]
        failed = [t for t in tasks if t.status == "failed"]

        # 计算加速倍数
        # 串行执行时间 = 所有任务时长之和
        # 并行执行时间 = 实际总耗时
        serial_duration = sum(t.duration_seconds for t in tasks)
        speedup = serial_duration / total_duration if total_duration > 0 else 1.0

        return ParallelExecutionResult(
            total_tasks=len(tasks),
            completed_tasks=len(completed),
            failed_tasks=len(failed),
            results=[t.result for t in completed],
            errors=[t.error for t in failed if t.error],
            total_duration_seconds=total_duration,
            speedup_factor=round(speedup, 2)
        )

    async def map_parallel(
        self,
        items: List[Any],
        map_fn: Callable[[Any], Any],
        task_description_fn: Optional[Callable[[Any], str]] = None
    ) -> ParallelExecutionResult:
        """
        并行映射（类似Python的map）

        Args:
            items: 输入项列表
            map_fn: 映射函数 (item) -> result
            task_description_fn: 生成任务描述的函数

        Returns:
            ParallelExecutionResult: 执行结果
        """
        import uuid

        # 将items转换为SubTask
        tasks = []
        for i, item in enumerate(items):
            description = task_description_fn(item) if task_description_fn else f"Task {i+1}"
            tasks.append(SubTask(
                task_id=str(uuid.uuid4()),
                description=description,
                parameters={"item": item, "index": i}
            ))

        # 定义执行器
        async def executor(task: SubTask):
            item = task.parameters["item"]
            return await map_fn(item)

        return await self.execute_parallel(tasks, executor)


# ==================== 预定义的并行任务 ====================

class ParallelWritingTasks:
    """并行写作任务"""

    def __init__(self, ai_service: Any):
        """
        初始化

        Args:
            ai_service: AI服务实例
        """
        self.ai_service = ai_service
        self.executor = ParallelExecutor(max_concurrent=5)

    async def generate_multiple_outlines(
        self,
        count: int,
        genre: str,
        context: Dict[str, Any] = None
    ) -> ParallelExecutionResult:
        """
        并发生成多个大纲方案

        Args:
            count: 生成数量
            genre: 类型
            context: 上下文

        Returns:
            ParallelExecutionResult: 执行结果
        """
        import uuid

        tasks = []
        for i in range(count):
            tasks.append(SubTask(
                task_id=str(uuid.uuid4()),
                description=f"生成大纲方案{i+1}",
                parameters={
                    "index": i,
                    "genre": genre,
                    "context": context
                }
            ))

        async def executor(task: SubTask):
            # 调用AI生成大纲
            # 这里应该调用实际的大纲生成服务
            await asyncio.sleep(1)  # 模拟AI调用
            return {
                "outline": f"大纲方案{task.parameters['index'] + 1}",
                "chapters": 20
            }

        return await self.executor.execute_parallel(tasks, executor)

    async def generate_multiple_chapters(
        self,
        chapter_numbers: List[int],
        work_context: Dict[str, Any]
    ) -> ParallelExecutionResult:
        """
        并发生成多个章节

        Args:
            chapter_numbers: 章节编号列表
            work_context: 作品上下文

        Returns:
            ParallelExecutionResult: 执行结果
        """
        import uuid

        tasks = []
        for chapter_num in chapter_numbers:
            tasks.append(SubTask(
                task_id=str(uuid.uuid4()),
                description=f"生成第{chapter_num}章",
                parameters={
                    "chapter_number": chapter_num,
                    "work_context": work_context
                }
            ))

        async def executor(task: SubTask):
            # 调用章节生成服务
            await asyncio.sleep(2)  # 模拟AI调用
            chapter_num = task.parameters["chapter_number"]
            return {
                "chapter_number": chapter_num,
                "content": f"第{chapter_num}章的内容...",
                "word_count": 3000
            }

        return await self.executor.execute_parallel(tasks, executor)

    async def analyze_multiple_chapters(
        self,
        chapter_ids: List[str]
    ) -> ParallelExecutionResult:
        """
        并发分析多个章节

        Args:
            chapter_ids: 章节ID列表

        Returns:
            ParallelExecutionResult: 执行结果
        """
        import uuid

        tasks = []
        for chapter_id in chapter_ids:
            tasks.append(SubTask(
                task_id=str(uuid.uuid4()),
                description=f"分析章节 {chapter_id}",
                parameters={"chapter_id": chapter_id}
            ))

        async def executor(task: SubTask):
            # 调用章节分析服务
            await asyncio.sleep(1.5)  # 模拟AI调用
            return {
                "chapter_id": task.parameters["chapter_id"],
                "quality_score": 85,
                "issues": [],
                "suggestions": []
            }

        return await self.executor.execute_parallel(tasks, executor)

    async def create_multiple_characters(
        self,
        character_configs: List[Dict[str, Any]]
    ) -> ParallelExecutionResult:
        """
        并发创建多个角色

        Args:
            character_configs: 角色配置列表

        Returns:
            ParallelExecutionResult: 执行结果
        """
        import uuid

        tasks = []
        for config in character_configs:
            tasks.append(SubTask(
                task_id=str(uuid.uuid4()),
                description=f"创建角色「{config.get('name', '未命名')}」",
                parameters=config
            ))

        async def executor(task: SubTask):
            # 调用角色创建服务
            await asyncio.sleep(1)  # 模拟AI调用
            return {
                "name": task.parameters.get("name"),
                "role": task.parameters.get("role"),
                "description": f"{task.parameters.get('name')}的角色卡片",
                "created": True
            }

        return await self.executor.execute_parallel(tasks, executor)


# ==================== 便捷函数 ====================

async def parallel_generate_outlines(
    count: int,
    genre: str,
    ai_service: Any,
    max_concurrent: int = 3
) -> List[Dict]:
    """
    并行生成多个大纲

    Args:
        count: 数量
        genre: 类型
        ai_service: AI服务
        max_concurrent: 最大并发数

    Returns:
        List[Dict]: 大纲列表
    """
    tasks = ParallelWritingTasks(ai_service)
    result = await tasks.generate_multiple_outlines(count, genre)
    return result.results


async def parallel_analyze_chapters(
    chapter_ids: List[str],
    ai_service: Any,
    max_concurrent: int = 5
) -> List[Dict]:
    """
    并行分析多个章节

    Args:
        chapter_ids: 章节ID列表
        ai_service: AI服务
        max_concurrent: 最大并发数

    Returns:
        List[Dict]: 分析结果列表
    """
    tasks = ParallelWritingTasks(ai_service)
    result = await tasks.analyze_multiple_chapters(chapter_ids)
    return result.results


async def parallel_map(
    items: List[T],
    async_fn: Callable[[T], Any],
    max_concurrent: int = 5
) -> List[Any]:
    """
    通用的并行映射函数

    Args:
        items: 输入项列表
        async_fn: 异步处理函数
        max_concurrent: 最大并发数

    Returns:
        List[Any]: 结果列表
    """
    executor = ParallelExecutor(max_concurrent=max_concurrent)
    result = await executor.map_parallel(items, async_fn)
    return result.results
