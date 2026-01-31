"""
并发工具调用优化器

提供高级的工具调用并行处理功能，包括智能调度、批量处理、结果聚合等。
"""

import asyncio
import time
from typing import Dict, Any, List, Optional, Callable, Union, TypeVar
from dataclasses import dataclass, field
from enum import Enum
from datetime import datetime
from collections import defaultdict
import uuid

from ..tools.tool_registry import DynamicToolRegistry
from ..utils.logger import get_logger
from ..utils.error_handler import robust_retry
from ..utils.performance import performance_optimizer
from app.utils.datetime_utils import get_utc_now

logger = get_logger("concurrent_tool_optimizer")

T = TypeVar('T')


class ToolPriority(Enum):
    """工具调用优先级"""
    LOW = 1
    NORMAL = 2
    HIGH = 3
    CRITICAL = 4


class ToolExecutionMode(Enum):
    """工具执行模式"""
    SEQUENTIAL = "sequential"  # 顺序执行
    PARALLEL = "parallel"     # 并行执行
    BATCH = "batch"          # 批量执行
    ADAPTIVE = "adaptive"    # 自适应模式


@dataclass
class ToolCall:
    """工具调用封装"""
    tool_id: str
    parameters: Dict[str, Any]
    call_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    priority: ToolPriority = ToolPriority.NORMAL
    execution_mode: ToolExecutionMode = ToolExecutionMode.ADAPTIVE
    dependencies: List[str] = field(default_factory=list)  # 依赖的call_id列表
    timeout: float = 30.0
    retry_count: int = 3
    metadata: Dict[str, Any] = field(default_factory=dict)

    # 运行时状态
    status: str = "pending"  # pending/running/completed/failed/cancelled
    result: Any = None
    error: Optional[str] = None
    start_time: Optional[datetime] = None
    end_time: Optional[datetime] = None
    duration: float = 0.0
    attempts: int = 0


@dataclass
class BatchToolCall:
    """批量工具调用"""
    tool_id: str
    calls: List[ToolCall]
    batch_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    batch_size: int = 5
    max_wait_time: float = 1.0

    # 批处理配置
    merge_strategy: str = "parallel"  # parallel/sequential/merge
    result_aggregation: str = "list"  # list/dict/merged


class ConcurrentToolExecutor:
    """并发工具执行器"""

    def __init__(
        self,
        max_concurrent: int = 10,
        batch_size: int = 5,
        default_timeout: float = 30.0
    ):
        """
        初始化并发工具执行器

        Args:
            max_concurrent: 最大并发数
            batch_size: 默认批处理大小
            default_timeout: 默认超时时间
        """
        self.max_concurrent = max_concurrent
        self.batch_size = batch_size
        self.default_timeout = default_timeout
        self.tool_registry = DynamicToolRegistry()

        # 并发控制
        self._semaphore = asyncio.Semaphore(max_concurrent)
        self._running_tasks: Dict[str, asyncio.Task] = {}
        self._pending_calls: List[ToolCall] = []
        self._completed_calls: Dict[str, ToolCall] = {}

        # 性能统计
        self._stats = {
            "total_calls": 0,
            "completed_calls": 0,
            "failed_calls": 0,
            "batch_calls": 0,
            "parallel_efficiency": 0.0,
            "avg_duration": 0.0,
            "tool_stats": defaultdict(lambda: {
                "calls": 0,
                "successes": 0,
                "failures": 0,
                "avg_duration": 0.0
            })
        }

        logger.info(f"ConcurrentToolExecutor initialized: max_concurrent={max_concurrent}")

    async def execute_tool(
        self,
        tool_id: str,
        parameters: Dict[str, Any],
        priority: ToolPriority = ToolPriority.NORMAL,
        timeout: Optional[float] = None,
        **kwargs
    ) -> Any:
        """
        执行单个工具调用

        Args:
            tool_id: 工具ID
            parameters: 工具参数
            priority: 调用优先级
            timeout: 超时时间

        Returns:
            Any: 工具执行结果
        """
        call = ToolCall(
            tool_id=tool_id,
            parameters=parameters,
            priority=priority,
            timeout=timeout or self.default_timeout,
            **kwargs
        )

        result = await self.execute_single(call)
        return result.result

    async def execute_tools_parallel(
        self,
        tool_calls: List[Dict[str, Any]],
        max_concurrent: Optional[int] = None
    ) -> List[Any]:
        """
        并行执行多个工具调用

        Args:
            tool_calls: 工具调用列表 [{"tool_id": str, "parameters": dict, ...}, ...]
            max_concurrent: 最大并发数，如果为None则使用默认值

        Returns:
            List[Any]: 执行结果列表
        """
        # 创建ToolCall对象
        calls = []
        for call_config in tool_calls:
            call = ToolCall(
                tool_id=call_config["tool_id"],
                parameters=call_config["parameters"],
                priority=ToolPriority(call_config.get("priority", 2)),
                timeout=call_config.get("timeout", self.default_timeout)
            )
            calls.append(call)

        # 执行并发调用
        results = await self.execute_parallel(calls, max_concurrent)
        return [result.result for result in results if result.status == "completed"]

    async def execute_tools_batch(
        self,
        tool_id: str,
        parameter_sets: List[Dict[str, Any]],
        batch_size: Optional[int] = None
    ) -> List[Any]:
        """
        批量执行相同工具的不同参数

        Args:
            tool_id: 工具ID
            parameter_sets: 参数集列表
            batch_size: 批处理大小

        Returns:
            List[Any]: 执行结果列表
        """
        batch_size = batch_size or self.batch_size

        # 创建批量调用
        batch_call = BatchToolCall(
            tool_id=tool_id,
            calls=[],
            batch_size=batch_size
        )

        # 将参数集转换为ToolCall
        for i, params in enumerate(parameter_sets):
            call = ToolCall(
                tool_id=tool_id,
                parameters=params,
                execution_mode=ToolExecutionMode.BATCH,
                metadata={"batch_index": i}
            )
            batch_call.calls.append(call)

        return await self.execute_batch(batch_call)

    async def execute_with_dependencies(
        self,
        tool_calls: List[Dict[str, Any]]
    ) -> Dict[str, Any]:
        """
        执行有依赖关系的工具调用

        Args:
            tool_calls: 工具调用列表，支持dependencies字段

        Returns:
            Dict[str, Any]: 执行结果映射
        """
        # 创建调用对象和依赖图
        calls = {}
        for call_config in tool_calls:
            call = ToolCall(
                tool_id=call_config["tool_id"],
                parameters=call_config["parameters"],
                dependencies=call_config.get("dependencies", [])
            )
            calls[call.call_id] = call

        # 拓扑排序执行
        results = {}
        executed = set()

        async def execute_call(call_id: str):
            """执行单个调用及其依赖"""
            if call_id in executed:
                return

            call = calls[call_id]

            # 先执行依赖
            for dep_id in call.dependencies:
                if dep_id not in executed:
                    await execute_call(dep_id)
                    if dep_id in results:
                        # 将依赖结果注入到参数中
                        call.parameters[f"__dep_{dep_id}"] = results[dep_id]

            # 执行当前调用
            result = await self.execute_single(call)
            if result.status == "completed":
                results[call_id] = result.result
                executed.add(call_id)
            else:
                raise Exception(f"Tool call {call_id} failed: {result.error}")

        # 并发执行无依赖的调用
        independent_calls = [
            call_id for call_id, call in calls.items()
            if not call.dependencies
        ]

        if independent_calls:
            await asyncio.gather(*[
                execute_call(call_id) for call_id in independent_calls
            ])

        return results

    async def execute_single(self, call: ToolCall) -> ToolCall:
        """
        执行单个工具调用

        Args:
            call: 工具调用对象

        Returns:
            ToolCall: 执行后的调用对象
        """
        call.status = "running"
        call.start_time = get_utc_now()
        call.attempts += 1

        async with self._semaphore:
            try:
                # 获取工具函数
                tool_info = self.tool_registry.get_tool(call.tool_id)
                if not tool_info:
                    raise ValueError(f"Tool {call.tool_id} not found")

                # 执行工具调用（带重试）
                @robust_retry(max_attempts=call.retry_count, delay=0.1)
                async def execute_with_retry():
                    return await self.tool_registry.call_tool(
                        call.tool_id,
                        call.parameters
                    )

                result = await asyncio.wait_for(
                    execute_with_retry(),
                    timeout=call.timeout
                )

                call.result = result
                call.status = "completed"

                # 更新统计
                self._update_stats(call, True)

                logger.debug(f"Tool {call.tool_id} completed successfully")

            except asyncio.TimeoutError:
                call.error = f"Tool call timed out after {call.timeout}s"
                call.status = "failed"
                self._update_stats(call, False)
                logger.warning(f"Tool {call.tool_id} timed out")

            except Exception as e:
                call.error = str(e)
                call.status = "failed"
                self._update_stats(call, False)
                logger.error(f"Tool {call.tool_id} failed: {e}")

            finally:
                call.end_time = get_utc_now()
                if call.start_time:
                    call.duration = (call.end_time - call.start_time).total_seconds()

        return call

    async def execute_parallel(
        self,
        calls: List[ToolCall],
        max_concurrent: Optional[int] = None
    ) -> List[ToolCall]:
        """
        并行执行多个工具调用

        Args:
            calls: 工具调用列表
            max_concurrent: 最大并发数

        Returns:
            List[ToolCall]: 执行结果列表
        """
        max_concurrent = max_concurrent or self.max_concurrent
        semaphore = asyncio.Semaphore(max_concurrent)

        async def execute_with_semaphore(call: ToolCall) -> ToolCall:
            async with semaphore:
                return await self.execute_single(call)

        # 按优先级排序
        calls.sort(key=lambda c: c.priority.value, reverse=True)

        # 并发执行
        start_time = time.time()
        tasks = [execute_with_semaphore(call) for call in calls]
        results = await asyncio.gather(*tasks, return_exceptions=True)

        # 处理异常结果
        processed_results = []
        for i, result in enumerate(results):
            if isinstance(result, Exception):
                calls[i].status = "failed"
                calls[i].error = str(result)
                processed_results.append(calls[i])
            else:
                processed_results.append(result)

        # 计算并发效率
        total_duration = time.time() - start_time
        serial_duration = sum(call.duration for call in processed_results)
        efficiency = serial_duration / total_duration if total_duration > 0 else 1.0

        self._stats["parallel_efficiency"] = min(efficiency, max_concurrent)

        return processed_results

    async def execute_batch(self, batch: BatchToolCall) -> List[Any]:
        """
        执行批量工具调用

        Args:
            batch: 批量调用对象

        Returns:
            List[Any]: 执行结果列表
        """
        results = []

        # 分批处理
        for i in range(0, len(batch.calls), batch.batch_size):
            batch_calls = batch.calls[i:i + batch.batch_size]

            if batch.merge_strategy == "parallel":
                batch_results = await self.execute_parallel(batch_calls)
                results.extend([r.result for r in batch_results if r.status == "completed"])

            elif batch.merge_strategy == "sequential":
                for call in batch_calls:
                    result = await self.execute_single(call)
                    if result.status == "completed":
                        results.append(result.result)

            elif batch.merge_strategy == "merge":
                # 尝试合并参数进行批量调用
                merged_params = self._merge_parameters(batch_calls)
                if merged_params:
                    # 使用合并后的参数进行单次调用
                    merged_call = ToolCall(
                        tool_id=batch.tool_id,
                        parameters=merged_params,
                        metadata={"batch_merged": True}
                    )
                    result = await self.execute_single(merged_call)
                    if result.status == "completed":
                        results.append(result.result)
                else:
                    # 无法合并，回退到并行处理
                    batch_results = await self.execute_parallel(batch_calls)
                    results.extend([r.result for r in batch_results if r.status == "completed"])

        # 更新统计
        self._stats["batch_calls"] += 1

        return results

    def _merge_parameters(self, calls: List[ToolCall]) -> Optional[Dict[str, Any]]:
        """
        合并多个工具调用的参数

        Args:
            calls: 工具调用列表

        Returns:
            Optional[Dict[str, Any]]: 合并后的参数，如果无法合并则返回None
        """
        if not calls:
            return None

        # 简单的参数合并策略
        # 这里可以根据具体工具类型实现更智能的合并逻辑
        try:
            merged = {}
            for call in calls:
                # 检查参数是否兼容
                for key, value in call.parameters.items():
                    if key not in merged:
                        merged[key] = []
                    merged[key].append(value)

            # 将列表转换为批量格式
            batch_params = {}
            for key, values in merged.items():
                if all(isinstance(v, type(values[0])) for v in values):
                    batch_params[key] = values
                else:
                    # 类型不兼容，无法合并
                    return None

            return batch_params

        except Exception:
            return None

    def _update_stats(self, call: ToolCall, success: bool) -> None:
        """更新性能统计"""
        self._stats["total_calls"] += 1

        if success:
            self._stats["completed_calls"] += 1
        else:
            self._stats["failed_calls"] += 1

        # 更新工具特定统计
        tool_stats = self._stats["tool_stats"][call.tool_id]
        tool_stats["calls"] += 1

        if success:
            tool_stats["successes"] += 1
        else:
            tool_stats["failures"] += 1

        # 更新平均执行时间
        if call.duration > 0:
            current_avg = tool_stats["avg_duration"]
            tool_stats["avg_duration"] = (
                (current_avg * (tool_stats["calls"] - 1) + call.duration) /
                tool_stats["calls"]
            )

        # 更新全局平均执行时间
        if call.duration > 0:
            total_completed = self._stats["completed_calls"]
            current_avg = self._stats["avg_duration"]
            self._stats["avg_duration"] = (
                (current_avg * (total_completed - 1) + call.duration) /
                total_completed
            )

    def get_performance_stats(self) -> Dict[str, Any]:
        """获取性能统计信息"""
        stats = self._stats.copy()

        # 计算成功率
        if stats["total_calls"] > 0:
            stats["success_rate"] = stats["completed_calls"] / stats["total_calls"]
        else:
            stats["success_rate"] = 0.0

        # 计算并发效率
        stats["concurrency_utilization"] = stats["parallel_efficiency"] / self.max_concurrent

        # 格式化工具统计
        stats["tool_stats"] = dict(stats["tool_stats"])

        return stats

    def clear_stats(self) -> None:
        """清空统计信息"""
        self._stats = {
            "total_calls": 0,
            "completed_calls": 0,
            "failed_calls": 0,
            "batch_calls": 0,
            "parallel_efficiency": 0.0,
            "avg_duration": 0.0,
            "tool_stats": defaultdict(lambda: {
                "calls": 0,
                "successes": 0,
                "failures": 0,
                "avg_duration": 0.0
            })
        }


# 全局实例
_concurrent_executor = None


def get_concurrent_tool_executor() -> ConcurrentToolExecutor:
    """获取全局并发工具执行器实例"""
    global _concurrent_executor
    if _concurrent_executor is None:
        _concurrent_executor = ConcurrentToolExecutor()
    return _concurrent_executor


# 便捷函数
async def execute_tools_parallel(
    tool_calls: List[Dict[str, Any]],
    max_concurrent: int = 5
) -> List[Any]:
    """
    并行执行多个工具调用的便捷函数

    Args:
        tool_calls: 工具调用列表
        max_concurrent: 最大并发数

    Returns:
        List[Any]: 执行结果列表
    """
    executor = get_concurrent_tool_executor()
    return await executor.execute_tools_parallel(tool_calls, max_concurrent)


async def execute_tools_batch(
    tool_id: str,
    parameter_sets: List[Dict[str, Any]],
    batch_size: int = 5
) -> List[Any]:
    """
    批量执行工具调用的便捷函数

    Args:
        tool_id: 工具ID
        parameter_sets: 参数集列表
        batch_size: 批处理大小

    Returns:
        List[Any]: 执行结果列表
    """
    executor = get_concurrent_tool_executor()
    return await executor.execute_tools_batch(tool_id, parameter_sets, batch_size)


def get_tool_performance_stats() -> Dict[str, Any]:
    """获取工具性能统计"""
    executor = get_concurrent_tool_executor()
    return executor.get_performance_stats()