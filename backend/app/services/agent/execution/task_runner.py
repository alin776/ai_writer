# -*- coding: utf-8 -*-
"""
任务执行器

负责执行单个任务（DeepAgent 模式使用）

从 langgraph_agent.py 拆分，减少主文件复杂度
"""

import json
import re
import logging
from typing import Dict, Any, Optional, Callable, Awaitable

from app.services.agent.tools import registry
from app.services.agent.utils.tool_helpers import normalize_tool_params
from app.services.agent.langgraph_tools import (
    analyze_text_tool,
    read_chapter_tool,
    get_chapter_by_order_tool,
    get_context_tool,
    search_analysis_fragments_tool,
)
from app.services.agent.tools.editor_tools import smart_continue

logger = logging.getLogger(__name__)


class TaskRunner:
    """任务执行器

    负责执行单个任务，支持 StandardTool 和 @tool 降级
    """

    # 工具名称映射
    TOOL_NAME_MAPPING = {
        "smart_continue": "smart_continue",
        "analyze_text_tool": "analyze_text",
        "analyze_content_tool": "analyze_text",  # 兼容：统一使用 analyze_text
        "analyze_content": "analyze_text",       # 兼容：统一使用 analyze_text
        "get_context_tool": "get_context",
        "read_chapter_tool": "read_chapter",
        "get_chapter_by_order_tool": "get_chapter_by_order",
        "search_analysis_fragments_tool": "search_analysis_fragments",
    }

    def __init__(
        self,
        call_tool_via_registry_func: Callable[..., Awaitable[str]],
        extract_tool_result_func: Callable[[str, Dict], str]
    ):
        """
        初始化

        Args:
            call_tool_via_registry_func: 通过 registry 调用工具的函数
            extract_tool_result_func: 提取工具结果的函数
        """
        self._call_tool_via_registry = call_tool_via_registry_func
        self._extract_tool_result = extract_tool_result_func

    async def execute_task(
        self,
        task: Dict[str, Any],
        work_id: str,
        chapter_id: str,
        context: str,
        context_payload: Optional[Dict[str, Any]] = None,
        on_progress: Optional[Callable] = None,
        conversation_id: Optional[str] = None  # v8.0: 添加 conversation_id 用于操作日志
    ) -> str:
        """执行单个任务（DeepAgent 模式使用）

        Args:
            task: 任务配置
            work_id: 作品ID
            chapter_id: 章节ID
            context: 上下文
            context_payload: 结构化上下文（原始 request.context）
            on_progress: 进度回调
            conversation_id: 会话ID（用于操作日志记录）

        Returns:
            任务执行结果
        """
        tool_name = task.get("tool", "analyze_text")
        # 处理 auto 工具名
        if tool_name == "auto":
            tool_name = "analyze_text"
        params = task.get("params", {})

        # 标准化参数格式
        params = normalize_tool_params(tool_name, params)

        if on_progress:
            await on_progress(task, "正在执行...")

        try:
            normalized_name = self.TOOL_NAME_MAPPING.get(tool_name, tool_name)

            # 准备工具参数
            tool_params = self._prepare_tool_params(
                tool_name=tool_name,
                params=params,
                work_id=work_id,
                chapter_id=chapter_id,
                context=context,
                task=task
            )

            # 如果返回的是结果字符串（特殊情况处理），直接返回
            if isinstance(tool_params, str):
                if on_progress:
                    await on_progress(task, "完成")
                return tool_params

            # 如果返回 None，表示需要使用统一接口
            if tool_params is None:
                logger.info(f"[TaskRunner] 使用统一接口调用未知工具: {tool_name}")
                state_context = context_payload if isinstance(context_payload, dict) else {}
                result = await self._call_tool_via_registry(
                    tool_name=tool_name,
                    tool_args=params,
                    state={
                        "work_id": work_id,
                        "chapter_id": chapter_id,
                        "last_user_message": context,
                        "conversation_id": conversation_id or "",
                        "context": state_context
                    }
                )
                if on_progress:
                    await on_progress(task, "完成")
                return result

            # 调用 StandardTool
            logger.info(f"[TaskRunner] 调用 registry.call_tool({normalized_name})")
            result_data = await registry.call_tool(normalized_name, tool_params)

            # 提取结果
            if isinstance(result_data, dict) and result_data.get("success"):
                result = self._extract_tool_result(normalized_name, result_data)
                logger.info(f"[TaskRunner] {normalized_name} 执行成功（DeepAgent模式）")
            else:
                error_msg = result_data.get("message", "执行失败") if isinstance(result_data, dict) else "未知错误"
                result = json.dumps({"error": "tool_failed", "message": error_msg}, ensure_ascii=False)
                logger.error(f"[TaskRunner] {normalized_name} 执行失败（DeepAgent模式）: {error_msg}")

        except ValueError as e:
            error_msg = str(e)
            if "validation error" in error_msg.lower():
                logger.error(f"[TaskRunner] {tool_name} 参数验证失败: {error_msg}")
                logger.error(f"[TaskRunner] 传入的参数: {tool_params if 'tool_params' in dir() else params}")
            else:
                logger.warning(f"[TaskRunner] StandardTool '{tool_name}' 不存在，降级到 @tool: {e}")
            result = await self._fallback_legacy_execute(tool_name, params, work_id, chapter_id, context)

        except Exception as e:
            logger.error(f"[TaskRunner] StandardTool 调用失败: {tool_name}, 错误: {e}")
            result = await self._fallback_legacy_execute(tool_name, params, work_id, chapter_id, context)

        if on_progress:
            await on_progress(task, "完成")

        return result

    def _prepare_tool_params(
        self,
        tool_name: str,
        params: Dict[str, Any],
        work_id: str,
        chapter_id: str,
        context: str,
        task: Dict[str, Any]
    ) -> Optional[Dict[str, Any] | str]:
        """准备工具参数

        Args:
            tool_name: 工具名称
            params: 原始参数
            work_id: 作品ID
            chapter_id: 章节ID
            context: 上下文
            task: 任务配置

        Returns:
            工具参数字典，或结果字符串（特殊情况），或 None（使用统一接口）
        """
        if tool_name == "get_chapter_by_order_tool":
            return {
                "work_id": work_id,
                "chapter_order": str(params.get("chapter_order", "1"))  # 确保字符串类型
            }

        elif tool_name == "get_context_tool":
            return {
                "work_id": work_id,
                "chapter_id": chapter_id or ""
            }

        elif tool_name == "read_chapter_tool":
            if "chapter_id" not in params or not params["chapter_id"]:
                logger.warning(
                    f"[TaskRunner] read_chapter_tool 缺少 chapter_id 参数，"
                    f"将使用当前章节ID: {chapter_id}。"
                    f"任务描述: {task.get('description', 'N/A')}"
                )
            return {
                "work_id": work_id,
                "chapter_id": params.get("chapter_id") or chapter_id or ""
            }

        elif tool_name == "search_analysis_fragments_tool":
            if not work_id:
                logger.warning(
                    f"[TaskRunner] search_analysis_fragments_tool 需要 work_id 参数，"
                    f"但当前 work_id 为空。任务描述: {task.get('description', 'N/A')}"
                )
                return json.dumps({
                    "error": "需要指定作品ID才能检索分析片段",
                    "message": "请在聊天时指定作品ID，或在作品详情页使用此功能",
                    "tool": "search_analysis_fragments_tool"
                }, ensure_ascii=False, indent=2)
            return {
                "work_id": work_id,
                "query": params.get("query", "相关内容"),
                "top_k": params.get("top_k", 5),
                "chapter_id": chapter_id or "",
                "include_current": params.get("include_current", True),
                "look_ahead": params.get("look_ahead", 0),
                "max_content_length": params.get("max_content_length", 2000),
            }

        elif tool_name == "smart_continue":
            context_param = self._extract_context_param(params, context)
            # 🔧 2026-01-09: 修复 chapter_id 参数处理，与其他工具保持一致
            # 优先使用 params 中的 chapter_id，否则使用传入的 chapter_id
            # 🔧 2026-01-11: 修复参数名 - SmartContinueInput 期望 chapter_content，不是 content
            return {
                "chapter_content": context_param,  # 修复：content -> chapter_content
                "chapter_id": params.get("chapter_id") or chapter_id or "",
                "user_requirement": params.get("user_requirement"),  # 添加用户要求
                "word_count": params.get("word_count", 500),  # 添加字数
            }

        elif tool_name == "analyze_text_tool":
            text_param, focus_param = self._extract_analyze_params(params, context)
            return {
                "text": text_param,
                "focus": focus_param
            }

        else:
            # 未知工具，返回 None 表示使用统一接口
            return None

    def _extract_context_param(self, params: Dict[str, Any], context: str) -> str:
        """提取续写上下文参数

        优先使用选中文本作为续写上下文
        """
        context_param = params.get("context", "").strip()
        if not context_param or "$TASK_" in context_param:
            selected_text_extracted = self._extract_selected_text(context)
            if selected_text_extracted and len(selected_text_extracted) >= 5:
                logger.info(f"[TaskRunner] smart_continue 优先使用选中文本（{len(selected_text_extracted)}字符）")
                context_param = selected_text_extracted
            else:
                context_param = context
        return context_param

    def _extract_analyze_params(self, params: Dict[str, Any], context: str) -> tuple:
        """提取分析参数

        Returns:
            (text_param, focus_param)
        """
        text_param = params.get("text", "").strip()

        # 处理空值和占位符 - 优先使用选中文本
        if not text_param or "$TASK_" in text_param:
            selected_text_extracted = self._extract_selected_text(context)
            if selected_text_extracted and len(selected_text_extracted) >= 5:
                logger.info(f"[TaskRunner] analyze_text_tool 优先使用选中文本（{len(selected_text_extracted)}字符）")
                text_param = selected_text_extracted
            else:
                logger.info(f"[TaskRunner] analyze_text_tool 的 text 参数为空或含占位符，使用 context 兜底（{len(context)}字符）")
                text_param = context[:50000]

        # focus 参数处理
        focus_param = params.get("focus", "all")
        if not focus_param or "$TASK_" in str(focus_param):
            focus_param = "all"
            logger.info(f"[TaskRunner] analyze_text_tool 的 focus 参数为空/占位符，使用默认值 'all'")
        else:
            logger.info(f"[TaskRunner] analyze_text_tool 使用 focus: '{str(focus_param)[:80]}...'")

        return text_param, focus_param

    def _extract_selected_text(self, context: str) -> Optional[str]:
        """从上下文中提取选中文本"""
        if "用户选中的文本：" in context:
            match = re.search(r'用户选中的文本：\n---\n(.*?)\n---', context, re.DOTALL)
            if match:
                return match.group(1).strip()
        return None

    async def _fallback_legacy_execute(
        self,
        tool_name: str,
        params: dict,
        work_id: str,
        chapter_id: str,
        context: str
    ) -> str:
        """DeepAgent 模式的降级执行（使用 @tool）

        Args:
            tool_name: 工具名称
            params: 工具参数
            work_id: 作品ID
            chapter_id: 章节ID
            context: 上下文

        Returns:
            工具执行结果
        """
        if tool_name == "get_chapter_by_order_tool":
            return await get_chapter_by_order_tool.ainvoke({
                "work_id": work_id,
                "chapter_order": str(params.get("chapter_order", "1"))  # 确保字符串类型
            })
        elif tool_name == "get_context_tool":
            return await get_context_tool.ainvoke({
                "work_id": work_id,
                "chapter_id": chapter_id or ""
            })
        elif tool_name == "read_chapter_tool":
            return await read_chapter_tool.ainvoke({
                "work_id": work_id,
                "chapter_id": params.get("chapter_id") or chapter_id or ""
            })
        elif tool_name == "search_analysis_fragments_tool":
            return await search_analysis_fragments_tool.ainvoke({
                "work_id": work_id,
                "query": params.get("query", "相关内容"),
                "top_k": params.get("top_k", 5),
                "chapter_id": chapter_id or "",
                "include_current": params.get("include_current", True),
                "look_ahead": params.get("look_ahead", 0),
                "max_content_length": params.get("max_content_length", 2000),
            })
        elif tool_name == "smart_continue":
            # 🔧 2026-01-11: 修复参数名 - smart_continue 期望 chapter_content，不是 content
            return await smart_continue.ainvoke({
                "chapter_id": params.get("chapter_id", ""),
                "chapter_content": params.get("chapter_content") or params.get("content") or context,
                "user_requirement": params.get("user_requirement"),
                "word_count": params.get("word_count", 500),
            })
        elif tool_name == "analyze_text_tool":
            return await analyze_text_tool.ainvoke({
                "text": params.get("text", ""),
                "focus": params.get("focus", "all")
            })
        else:
            return f"任务 {tool_name} 需要手动处理"
