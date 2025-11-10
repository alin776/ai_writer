"""并行工具节点 - 复用Planning模式的并行执行框架

本模块实现了支持并行执行的工具节点，直接复用Planning模式的核心逻辑：
- 智能分组（并行安全工具 vs 串行工具）
- Semaphore限流机制（max_concurrent=5）
- 自动重试机制（网络/超时错误，指数退避）
- 优雅降级（return_exceptions=True）

代码复用来源：
- backend/app/services/agent/langgraph_agent.py:3080-3389 (Planning并行执行框架)
"""

import asyncio
import logging
from typing import Any, Dict, List, Optional

from langchain_core.messages import AIMessage, ToolMessage
from langgraph.prebuilt.tool_node import ToolNode

logger = logging.getLogger(__name__)

# 🟢 直接复用Planning的定义：可以并行执行的独立数据获取工具
PARALLEL_SAFE_TOOLS = {
    "get_context_tool",
    "read_chapter_tool",
    "get_chapter_by_order_tool",
    "search_analysis_fragments_tool"
    # 注意：以下工具不能并行
    # - continue_writing_tool: 数据写入，必须串行
    # - polish_text_tool: 数据写入，必须串行
    # - analyze_text_tool: 可能依赖其他工具结果，应串行
}


class ParallelToolNode(ToolNode):
    """支持并行执行的工具节点

    核心功能（95%复用Planning模式）:
    1. 智能分类工具调用（并行安全 vs 串行）
    2. Semaphore限流（避免数据库连接池耗尽）
    3. 自动重试机制（网络/超时错误）
    4. 优雅降级（一个工具失败不影响其他）

    Args:
        tools: 工具列表
        max_concurrent: 最大并发数（默认5，基于数据库连接池大小）
    """

    def __init__(self, tools, max_concurrent: int = 5):
        super().__init__(tools)
        self.max_concurrent = max_concurrent
        logger.info(
            f"[ParallelToolNode] 初始化完成，最大并发数={max_concurrent}，"
            f"并行安全工具={len(PARALLEL_SAFE_TOOLS)}个"
        )

    async def ainvoke(self, input: Dict[str, Any], config: Optional[Dict] = None):
        """异步调用（支持并行）

        🟢 核心逻辑复用自Planning模式的_execute_tasks_in_parallel方法

        Args:
            input: 输入状态，包含messages
            config: 配置参数

        Returns:
            包含ToolMessage列表的字典
        """
        # 提取工具调用
        tool_calls = self._extract_tool_calls(input.get("messages", []))

        if not tool_calls:
            logger.debug("[ParallelToolNode] 无工具调用")
            return {"messages": []}

        # 🟢 复用：智能分类工具调用（并行 vs 串行）
        parallel_calls = [
            call for call in tool_calls
            if call["name"] in PARALLEL_SAFE_TOOLS
        ]
        serial_calls = [
            call for call in tool_calls
            if call["name"] not in PARALLEL_SAFE_TOOLS
        ]

        logger.info(
            f"[ParallelToolNode] 工具分组: "
            f"并行={len(parallel_calls)}, 串行={len(serial_calls)}"
        )

        results = []

        # 🟢 第1批：并行执行安全工具（带限流）
        if parallel_calls:
            logger.info(f"[ParallelToolNode] 开始并行执行{len(parallel_calls)}个工具")

            # 🟢 复用：Semaphore限流
            semaphore = asyncio.Semaphore(self.max_concurrent)

            async def execute_with_semaphore(call):
                """限流执行（复用Planning的Semaphore模式）"""
                async with semaphore:
                    return await self._execute_tool_with_retry(call)

            # 🟢 复用：asyncio.gather + return_exceptions
            parallel_results = await asyncio.gather(
                *[execute_with_semaphore(call) for call in parallel_calls],
                return_exceptions=True  # ← 优雅降级：一个失败不影响其他
            )

            # 🟢 复用：处理异常结果
            for i, result in enumerate(parallel_results):
                if isinstance(result, Exception):
                    logger.error(
                        f"[ParallelToolNode] 工具{parallel_calls[i]['name']}失败: {result}"
                    )
                    # 创建失败消息
                    results.append(ToolMessage(
                        content=f"工具执行失败: {str(result)}",
                        tool_call_id=parallel_calls[i]["id"],
                        name=parallel_calls[i]["name"]
                    ))
                else:
                    results.append(result)

            logger.info(
                f"[ParallelToolNode] 并行执行完成，"
                f"成功={len([r for r in results if not isinstance(r, Exception)])}，"
                f"失败={len([r for r in results if isinstance(r, Exception)])}"
            )

        # 🟢 第2批：串行执行不安全工具
        if serial_calls:
            logger.info(f"[ParallelToolNode] 开始串行执行{len(serial_calls)}个工具")
            for call in serial_calls:
                logger.info(f"[ParallelToolNode] 串行执行工具: {call['name']}")
                result = await self._execute_tool_with_retry(call)
                results.append(result)

        return {"messages": results}

    async def _execute_tool_with_retry(self, tool_call: Dict) -> ToolMessage:
        """执行工具（带重试机制）

        🟢 直接复用Planning的重试逻辑（langgraph_agent.py:3178-3248）

        Args:
            tool_call: 工具调用信息，包含name, args, id

        Returns:
            ToolMessage（成功或失败）
        """
        # 🟢 复用：重试配置
        max_retries = 2
        tool_name = tool_call["name"]
        tool_id = tool_call["id"]

        for retry_count in range(max_retries + 1):
            try:
                # 执行工具
                result = await self._execute_tool(tool_call)

                if retry_count > 0:
                    logger.info(
                        f"[ParallelToolNode] 工具{tool_name}重试{retry_count}次后成功"
                    )

                return result

            except Exception as e:
                # 🟢 复用：判断是否为可重试的错误
                is_retryable = any(keyword in str(e).lower() for keyword in [
                    "timeout", "connection", "network", "网络", "连接", "超时"
                ])

                if is_retryable and retry_count < max_retries:
                    # 🟢 复用：指数退避（2, 4, 8秒）
                    wait_time = 2 ** (retry_count + 1)
                    logger.warning(
                        f"[ParallelToolNode] 工具{tool_name}失败，"
                        f"{wait_time}秒后重试（{retry_count + 1}/{max_retries}）: {e}"
                    )
                    await asyncio.sleep(wait_time)
                else:
                    # 不可重试或已达最大次数
                    logger.error(
                        f"[ParallelToolNode] 工具{tool_name}最终失败: {e}"
                    )
                    return ToolMessage(
                        content=f"错误: {str(e)}",
                        tool_call_id=tool_id,
                        name=tool_name
                    )

        # 理论上不会到这里（for循环已处理所有情况）
        return ToolMessage(
            content=f"错误: 工具执行失败（已重试{max_retries}次）",
            tool_call_id=tool_id,
            name=tool_name
        )

    async def _execute_tool(self, tool_call: Dict) -> ToolMessage:
        """执行单个工具（调用实际的工具函数）

        Args:
            tool_call: 工具调用信息

        Returns:
            ToolMessage

        Raises:
            ValueError: 工具不存在
            Exception: 工具执行失败
        """
        tool_name = tool_call["name"]
        tool_input = tool_call["args"]
        tool_id = tool_call["id"]

        # 🟢 从父类ToolNode获取tools_by_name
        tool_obj = self.tools_by_name.get(tool_name)
        if not tool_obj:
            raise ValueError(f"工具 {tool_name} 不存在")

        # 执行工具（异步）
        try:
            result = await tool_obj.ainvoke(tool_input)
        except Exception as e:
            logger.error(f"[ParallelToolNode] 工具{tool_name}执行失败: {e}")
            raise

        # 返回ToolMessage
        return ToolMessage(
            content=str(result),
            tool_call_id=tool_id,
            name=tool_name
        )

    def _extract_tool_calls(self, messages: List) -> List[Dict]:
        """从消息列表中提取工具调用

        Args:
            messages: 消息列表

        Returns:
            工具调用列表，每个包含name, args, id
        """
        # 从最后一条AIMessage中提取tool_calls
        for msg in reversed(messages):
            if isinstance(msg, AIMessage) and hasattr(msg, 'tool_calls') and msg.tool_calls:
                return msg.tool_calls
        return []
