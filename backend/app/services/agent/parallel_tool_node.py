"""Parallel tool execution node for LangGraph."""

import asyncio
import json
import logging
from typing import Any, Dict, List, Optional

from langchain_core.messages import AIMessage, ToolMessage
from langgraph.prebuilt.tool_node import ToolNode

logger = logging.getLogger(__name__)

PARALLEL_SAFE_TOOLS = {
    "get_context_tool",
    "read_chapter_tool",
    "get_chapter_by_order_tool",
    "search_analysis_fragments_tool",
    "search_content",
    "analyze_content",
}

SERIAL_ONLY_TOOLS = {
    "smart_continue",
    "smart_rewrite",
    "smart_insert",
    "analyze_text_tool",
}


class ParallelToolNode(ToolNode):
    """Tool node that runs safe calls concurrently and unsafe calls serially."""

    def __init__(self, tools, max_concurrent: int = 5):
        super().__init__(tools)
        self.max_concurrent = max_concurrent
        logger.info(
            "[ParallelToolNode] initialized, max_concurrent=%s, safe_tools=%s",
            max_concurrent,
            len(PARALLEL_SAFE_TOOLS),
        )

    async def ainvoke(self, input: Dict[str, Any], config: Optional[Dict] = None):
        tool_calls = self._extract_tool_calls(input.get("messages", []))
        if not tool_calls:
            return {"messages": []}

        parallel_calls = [
            call for call in tool_calls if self._is_parallel_safe(call["name"])
        ]
        serial_calls = [
            call for call in tool_calls if not self._is_parallel_safe(call["name"])
        ]

        logger.info(
            "[ParallelToolNode] grouped tool calls: parallel=%s serial=%s",
            len(parallel_calls),
            len(serial_calls),
        )

        results: List[ToolMessage] = []

        if parallel_calls:
            semaphore = asyncio.Semaphore(self.max_concurrent)

            async def execute_with_semaphore(call: Dict[str, Any]) -> ToolMessage:
                async with semaphore:
                    return await self._execute_tool_with_retry(call)

            parallel_results = await asyncio.gather(
                *[execute_with_semaphore(call) for call in parallel_calls],
                return_exceptions=True,
            )

            for i, result in enumerate(parallel_results):
                if isinstance(result, Exception):
                    call = parallel_calls[i]
                    logger.error(
                        "[ParallelToolNode] tool %s failed: %s", call["name"], result
                    )
                    results.append(
                        ToolMessage(
                            content=f"tool execution failed: {type(result).__name__}: {result}",
                            tool_call_id=call["id"],
                            name=call["name"],
                        )
                    )
                else:
                    results.append(result)

        if serial_calls:
            for call in serial_calls:
                results.append(await self._execute_tool_with_retry(call))

        return {"messages": results}

    async def _execute_tool_with_retry(self, tool_call: Dict[str, Any]) -> ToolMessage:
        max_retries = 2
        tool_name = tool_call["name"]
        tool_id = tool_call["id"]

        for retry_count in range(max_retries + 1):
            try:
                result = await self._execute_tool(tool_call)
                if retry_count > 0:
                    logger.info(
                        "[ParallelToolNode] tool %s succeeded after retry %s",
                        tool_name,
                        retry_count,
                    )
                return result
            except Exception as e:
                is_retryable = any(
                    keyword in str(e).lower()
                    for keyword in (
                        "timeout",
                        "connection",
                        "network",
                        "connect",
                        "timed out",
                    )
                )

                if is_retryable and retry_count < max_retries:
                    wait_time = 2 ** (retry_count + 1)
                    logger.warning(
                        "[ParallelToolNode] tool %s failed, retrying in %ss (%s/%s): %s",
                        tool_name,
                        wait_time,
                        retry_count + 1,
                        max_retries,
                        e,
                    )
                    await asyncio.sleep(wait_time)
                    continue

                logger.error("[ParallelToolNode] tool %s final failure: %s", tool_name, e)
                return ToolMessage(
                    content=f"error: {e}",
                    tool_call_id=tool_id,
                    name=tool_name,
                )

        return ToolMessage(
            content=f"error: tool execution failed after {max_retries} retries",
            tool_call_id=tool_id,
            name=tool_name,
        )

    def _is_parallel_safe(self, tool_name: str) -> bool:
        if tool_name in SERIAL_ONLY_TOOLS:
            return False
        if tool_name in PARALLEL_SAFE_TOOLS:
            return True

        normalized = tool_name.lower()
        if any(k in normalized for k in ("read_", "get_", "search_")):
            return True
        if "analyze" in normalized:
            return False
        if any(k in normalized for k in ("write", "insert", "rewrite", "update", "delete")):
            return False
        return False

    async def _execute_tool(self, tool_call: Dict[str, Any]) -> ToolMessage:
        tool_name = tool_call["name"]
        tool_input = tool_call["args"]
        tool_id = tool_call["id"]

        tool_obj = self.tools_by_name.get(tool_name)
        if not tool_obj:
            raise ValueError(f"tool not found: {tool_name}")

        result = await tool_obj.ainvoke(tool_input)
        if isinstance(result, dict):
            content = json.dumps(result, ensure_ascii=False)
        else:
            content = str(result)

        return ToolMessage(content=content, tool_call_id=tool_id, name=tool_name)

    def _extract_tool_calls(self, messages: List[Any]) -> List[Dict[str, Any]]:
        for msg in reversed(messages):
            if isinstance(msg, AIMessage) and getattr(msg, "tool_calls", None):
                return msg.tool_calls
        return []
