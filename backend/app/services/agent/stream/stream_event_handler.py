# -*- coding: utf-8 -*-
"""
流式事件处理器

从 langgraph_agent.py 的 _handle_stream_event 方法中拆分。
负责处理 LangGraph 流式事件，包括：
- 进度追踪
- 工具调用缓存
- HITL 确认请求处理
- 内容生成检测
"""

import json
import logging
from typing import Dict, Any, Optional, List, TYPE_CHECKING

from langchain_core.messages import AIMessage, ToolMessage

if TYPE_CHECKING:
    from app.services.agent.stream.event_parser import EventParser
    from app.services.agent.progress_tracker import ProgressTracker

logger = logging.getLogger(__name__)


class StreamEventHandler:
    """流式事件处理器

    处理 LangGraph astream_events 产生的各类事件，
    并触发相应的回调函数。
    """

    def __init__(
        self,
        event_parser: "EventParser",
        cached_tool_calls: Dict[str, Any],
        approval_callback: Optional[callable] = None
    ):
        """
        Args:
            event_parser: 事件解析器实例
            cached_tool_calls: 缓存的工具调用参数（引用）
            approval_callback: HITL 确认请求回调
        """
        self.event_parser = event_parser
        self._cached_tool_calls = cached_tool_calls
        self._approval_callback = approval_callback

    def set_approval_callback(self, callback: Optional[callable]):
        """设置 HITL 确认请求回调"""
        self._approval_callback = callback

    async def handle_event(
        self,
        event: dict,
        on_progress: Optional[callable] = None,
        on_tool_call: Optional[callable] = None,
        on_content: Optional[callable] = None,
        progress_tracker: Optional["ProgressTracker"] = None,
        context: Optional[dict] = None
    ):
        """处理 astream 事件，转换为用户友好的进度信息并触发回调

        Args:
            event: LangGraph 节点事件 {node_name: node_data}
            on_progress: 进度回调
            on_tool_call: 工具调用回调
            on_content: 内容生成回调
            progress_tracker: 进度追踪器
            context: 上下文（用于 HITL）
        """
        if not event:
            return

        # 提取节点名和数据
        node_name = list(event.keys())[0]
        node_data = event[node_name]

        logger.info(f"[Stream Event] 节点: {node_name}")

        # 1. 追踪节点完成
        if progress_tracker:
            progress_tracker.end_node(node_name)
            logger.debug(f"[ProgressTracker] 节点完成: {node_name}")

        # 2. 缓存 agent 节点的工具调用参数
        self._cache_tool_calls_from_agent(node_name, node_data)

        # 3. 解析进度事件并触发 on_progress
        if on_progress:
            await self._handle_progress(node_name, node_data, on_progress, progress_tracker)

        # 4. 检测工具调用并触发 on_tool_call + HITL
        if node_name == "tools":
            if on_tool_call:
                await self._handle_tool_calls(node_data, on_tool_call)

            # HITL 确认请求处理
            await self._handle_hitl_confirmation(node_data)

        # 5. 检测内容生成并触发 on_content
        if on_content:
            await self._handle_content(node_name, node_data, on_content)

    def _cache_tool_calls_from_agent(self, node_name: str, node_data: dict):
        """缓存 agent 节点的工具调用参数（用于后续 tools 节点显示）"""
        agent_nodes = [
            "writing_agent", "planning_agent", "analysis_agent",
            "stuck_agent", "general_agent"
        ]

        if node_name not in agent_nodes:
            return

        messages = node_data.get("messages", [])
        for msg in reversed(messages):
            if isinstance(msg, AIMessage) and hasattr(msg, "tool_calls") and msg.tool_calls:
                for tool_call in msg.tool_calls:
                    tool_name = tool_call.get("name")
                    tool_args = tool_call.get("args", {})
                    if tool_name:
                        self._cached_tool_calls[tool_name] = tool_args
                        logger.debug(f"[Cache] 缓存工具参数: {tool_name} -> {tool_args}")
                break  # 只缓存最新的一条 AIMessage

    async def _handle_progress(
        self,
        node_name: str,
        node_data: dict,
        on_progress: callable,
        progress_tracker: Optional["ProgressTracker"]
    ):
        """处理进度事件"""
        progress_event = self.event_parser.parse_node_event(
            node_name, node_data, progress_tracker
        )
        if progress_event:
            logger.info(f"[Stream Event] progress_event = {progress_event}")
            try:
                await on_progress(progress_event)
                logger.info(f"[Stream Event] on_progress 回调已调用")
            except Exception as e:
                logger.error(f"[Stream] 进度回调失败: {e}")

    async def _handle_tool_calls(self, node_data: dict, on_tool_call: callable):
        """处理工具调用"""
        tool_calls = self.event_parser.extract_tool_calls(node_data)
        for tool_name, tool_args in tool_calls:
            try:
                await on_tool_call(tool_name, tool_args)
            except Exception as e:
                logger.error(f"[Stream] 工具回调失败: {e}")

    async def _handle_hitl_confirmation(self, node_data: dict):
        """处理 HITL 确认请求"""
        if not self._approval_callback:
            return

        messages = node_data.get("messages", [])

        for msg in messages:
            if not isinstance(msg, ToolMessage):
                continue

            try:
                # 尝试解析工具返回结果
                content_length = len(msg.content) if msg.content else 0
                logger.info(
                    f"[HITL] 检查工具消息: {msg.name}, "
                    f"content长度={content_length}, 前100字符: {msg.content[:100]}"
                )

                tool_result = json.loads(msg.content)

                logger.info(
                    f"[HITL] 解析成功，"
                    f"requires_confirmation={tool_result.get('requires_confirmation')}, "
                    f"keys={list(tool_result.keys())}"
                )

                # 检查是否需要用户确认
                if not tool_result.get("requires_confirmation"):
                    continue

                logger.info(f"[HITL] 检测到确认请求: {tool_result.get('action_type')}")

                # 构建审批数据
                versions = tool_result.get("versions") or tool_result.get("recommendations")
                approval_data = {
                    "request_id": f"{msg.name}_{msg.tool_call_id}",
                    "action_type": tool_result.get("action_type", "edit"),
                    "operation": tool_result.get("operation"),
                    "original_content": tool_result.get("original_text"),
                    "new_content": tool_result.get("content"),
                    "description": tool_result.get("description"),
                    "versions": versions,
                    "chapter_id": tool_result.get("chapter_id"),
                    "editor_action": tool_result.get("editor_action")
                }

                logger.info(
                    f"[HITL] 准备调用回调: request_id={approval_data['request_id']}, "
                    f"versions数量={len(versions) if versions else 0}, "
                    f"editor_action={approval_data.get('editor_action')}"
                )

                await self._approval_callback(approval_data)
                logger.info(f"[HITL] ✅ 回调执行成功")

            except json.JSONDecodeError as e:
                logger.warning(
                    f"[HITL] JSON解析失败: {msg.name}, error={e}, "
                    f"content前200字符={msg.content[:200]}"
                )
            except Exception as e:
                logger.error(
                    f"[HITL] 处理确认请求失败: {msg.name}, error={e}",
                    exc_info=True
                )

    async def _handle_content(
        self,
        node_name: str,
        node_data: dict,
        on_content: callable
    ):
        """处理内容生成"""
        content = self.event_parser.extract_content(node_name, node_data)
        if content:
            try:
                await on_content(content)
            except Exception as e:
                logger.error(f"[Stream] 内容回调失败: {e}")
