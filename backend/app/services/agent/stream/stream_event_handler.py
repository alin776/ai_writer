# -*- coding: utf-8 -*-
"""
流式事件处理器

从 langgraph_agent.py 的 _handle_stream_event 方法中拆分。
负责处理 LangGraph 流式事件，包括：
- 进度追踪
- 工具调用缓存
- HITL 确认请求处理
- 内容生成检测
- 执行轨迹事件 (v6.0)
"""

import json
import logging
from typing import Dict, Any, Optional, List, TYPE_CHECKING

from langchain_core.messages import AIMessage, ToolMessage

from .flow_events import FlowEventBuilder, get_tool_icon

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
        self._on_flow_event: Optional[callable] = None  # 执行轨迹事件回调
        self._step_counter = 0  # 步骤计数器

    def set_approval_callback(self, callback: Optional[callable]):
        """设置 HITL 确认请求回调"""
        self._approval_callback = callback

    def set_flow_event_callback(self, callback: Optional[callable]):
        """设置执行轨迹事件回调"""
        self._on_flow_event = callback

    def reset_step_counter(self):
        """重置步骤计数器"""
        self._step_counter = 0

    async def emit_flow_event(self, event: dict):
        """发送执行轨迹事件"""
        if self._on_flow_event:
            try:
                await self._on_flow_event(event)
            except Exception as e:
                logger.error(f"[FlowEvent] 发送失败: {e}")

    async def emit_agent_header(self, name: str = "文枢AI", badge: str = ""):
        """发送Agent头部事件"""
        await self.emit_flow_event(FlowEventBuilder.agent_header(name, badge))

    async def emit_text(self, content: str):
        """发送文本消息事件"""
        await self.emit_flow_event(FlowEventBuilder.text(content))

    async def emit_step_start(self, title: str) -> int:
        """发送步骤开始事件，返回步骤ID"""
        self._step_counter += 1
        await self.emit_flow_event(FlowEventBuilder.step_start(self._step_counter, title))
        return self._step_counter

    async def emit_knowledge_loaded(
        self,
        step_id: int,
        knowledge_type: str,
        title: str,
        icon: str,
        items: List[Dict[str, Any]]
    ):
        """发送知识加载完成事件"""
        await self.emit_flow_event(FlowEventBuilder.knowledge_loaded(
            step_id, knowledge_type, title, icon, items
        ))

    async def emit_step_complete(
        self,
        step_id: int,
        description: str,
        tool_name: Optional[str] = None
    ):
        """发送步骤完成事件"""
        tool_call = None
        if tool_name:
            tool_call = {"icon": get_tool_icon(tool_name), "name": tool_name}
        await self.emit_flow_event(FlowEventBuilder.step_complete(
            step_id, description, tool_call
        ))

    async def emit_output_ready(
        self,
        title: str,
        content: str,
        intro: Optional[str] = None,
        intro_highlight: Optional[str] = None
    ):
        """发送输出就绪事件"""
        await self.emit_flow_event(FlowEventBuilder.output_ready(
            title, content, intro, intro_highlight
        ))

    async def emit_completion(self, text: str = "任务已完成"):
        """发送完成状态事件"""
        await self.emit_flow_event(FlowEventBuilder.completion(text))

    async def emit_summarization_start(
        self,
        task_classification: Dict[str, List[Dict[str, Any]]],
        context_stats: Dict[str, Any]
    ):
        """发送AI整合分析开始事件"""
        logger.info(f"[StreamEventHandler] emit_summarization_start 被调用, _on_flow_event={self._on_flow_event is not None}")
        await self.emit_flow_event(FlowEventBuilder.summarization_start(
            task_classification, context_stats
        ))

    async def emit_summarization_complete(self):
        """发送AI整合分析完成事件"""
        await self.emit_flow_event(FlowEventBuilder.summarization_complete())

    async def emit_revision(
        self,
        revision_type: str,
        request_id: str = None,
        chapter_id: str = None,
        chapter_title: str = None,
        content_preview: str = None,
        old_title: str = None,
        new_title: str = None,
        versions: list = None
    ):
        """发送修订请求事件 (v7.0)"""
        await self.emit_flow_event(FlowEventBuilder.revision(
            revision_type=revision_type,
            request_id=request_id,
            chapter_id=chapter_id,
            chapter_title=chapter_title,
            content_preview=content_preview,
            old_title=old_title,
            new_title=new_title,
            versions=versions
        ))

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
                    "original_content": (
                        tool_result.get("original_text")
                        or tool_result.get("original_content")
                        or tool_result.get("old_title")
                    ),
                    "new_content": (
                        tool_result.get("content")
                        or tool_result.get("new_content")
                        or tool_result.get("new_title")
                    ),
                    "description": tool_result.get("description"),
                    "versions": versions,
                    "chapter_id": tool_result.get("chapter_id"),
                    "chapter_title": tool_result.get("chapter_title"),
                    "work_id": tool_result.get("work_id"),
                    "old_title": tool_result.get("old_title"),
                    "new_title": tool_result.get("new_title"),
                    "editor_action": tool_result.get("editor_action")
                }

                # 若工具返回 position 但未提供 editor_action，推断编辑类型
                if not approval_data.get("editor_action") and tool_result.get("position") is not None:
                    position_value = tool_result.get("position")
                    if isinstance(position_value, dict) and "from" in position_value:
                        position_payload = position_value
                    else:
                        position_payload = {"from": position_value, "to": position_value}

                    operation = approval_data.get("operation")
                    inferred_type = "modify"
                    if operation == "append":
                        inferred_type = "continue"
                    elif operation == "insert":
                        inferred_type = "insert"

                    approval_data["editor_action"] = {
                        "type": inferred_type,
                        "position": position_payload,
                        "requires_confirmation": True
                    }

                logger.info(
                    f"[HITL] 准备调用回调: request_id={approval_data['request_id']}, "
                    f"versions数量={len(versions) if versions else 0}, "
                    f"editor_action={approval_data.get('editor_action')}"
                )

                callback_result = await self._approval_callback(approval_data)
                logger.info(f"[HITL] ✅ 回调执行成功")

                request_id = approval_data.get("request_id")
                if isinstance(callback_result, dict) and callback_result.get("request_id"):
                    request_id = callback_result.get("request_id")
                elif isinstance(callback_result, str):
                    request_id = callback_result

                # v7.0: 发送 revision 事件到执行轨迹
                action_type = tool_result.get("action_type", "edit")
                operation = tool_result.get("operation")

                # 映射 action_type/operation 到 revision_type
                revision_type_map = {
                    "rewrite": "replace",
                    "edit": "replace",
                    "continue": "append",
                    "insert": "insert",
                    "create": "create",
                    "rename": "rename"
                }
                revision_type = revision_type_map.get(action_type, "replace")
                if operation == "append":
                    revision_type = "append"
                elif operation == "insert":
                    revision_type = "insert"

                # 生成内容预览（前50字）
                content_preview = None
                new_content = tool_result.get("content") or tool_result.get("new_content")
                if new_content:
                    content_preview = new_content[:50] if len(new_content) > 50 else new_content

                # 发送 revision 事件
                await self.emit_revision(
                    revision_type=revision_type,
                    request_id=request_id,
                    chapter_id=tool_result.get("chapter_id"),
                    chapter_title=tool_result.get("chapter_title"),
                    content_preview=content_preview,
                    old_title=tool_result.get("old_title"),
                    new_title=tool_result.get("new_title"),
                    versions=versions
                )
                logger.info(f"[HITL] ✅ revision 事件已发送: type={revision_type}")

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
