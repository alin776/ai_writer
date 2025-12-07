"""DeepAgent 模块

提供动态反思和重规划能力，基于 Deep Agents 设计理念。

使用方式：
    from .deep_agent import DeepAgentExecutor

    executor = DeepAgentExecutor(
        agent_graph=self,
        on_plan=on_plan,
        on_task_start=on_task_start,
        on_task_progress=on_task_progress,
        on_task_done=on_task_done,
        on_content=on_content,
    )
    result = await executor.execute_with_reflection(plan, context, execute_func)
"""

from .executor import DeepAgentExecutor
from .reflection import think_tool, should_reflect, ReflectionResult
from .config import DeepAgentConfig

__all__ = [
    "DeepAgentExecutor",
    "think_tool",
    "should_reflect",
    "ReflectionResult",
    "DeepAgentConfig",
]
