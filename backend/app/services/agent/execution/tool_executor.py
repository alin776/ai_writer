# -*- coding: utf-8 -*-
"""
工具执行器

从 langgraph_agent.py 提取的工具调用逻辑：
- 统一工具调用接口
- 参数预处理
- 结果提取
- 降级兜底
"""

from typing import Dict, Any, Optional
import json
import logging

from app.services.agent.tools import registry

logger = logging.getLogger(__name__)


# 工具名称映射（@tool 名称 → StandardTool 名称）
TOOL_NAME_MAPPING = {
    "analyze_text_tool": "analyze_text",
    "smart_rewrite": "smart_rewrite",
    "smart_continue": "smart_continue",
    "smart_insert": "smart_insert",
    "apply_chapter_edit": "apply_chapter_edit",
    # 章节工具
    "get_context_tool": "get_context",
    "read_chapter_tool": "read_chapter",
    "get_chapter_by_order_tool": "get_chapter_by_order",
    "search_analysis_fragments_tool": "search_analysis_fragments",
    # 世界观工具
    "get_worldview_summary": "get_worldview_summary",
    # 分析工具
    "evaluate_quality_tool": "evaluate_quality",
    "analyze_content_tool": "analyze_content",
    # 章节管理工具（OPERATION 类）
    "create_chapter": "create_chapter",
    "update_chapter_title": "update_chapter_title",
    "delete_chapter": "delete_chapter",
    "update_chapter_content": "update_chapter_content",
}


class ToolExecutor:
    """工具执行器

    负责统一管理工具调用：
    1. StandardTool 优先
    2. @tool 降级兜底
    """

    def __init__(self):
        pass

    async def call_tool(
        self,
        tool_name: str,
        tool_args: dict,
        state: dict
    ) -> str:
        """通过 registry 统一调用工具（StandardTool 优先，@tool 兜底）

        Args:
            tool_name: 工具名称
            tool_args: 工具参数
            state: Agent 状态

        Returns:
            str: 工具执行结果（字符串格式）
        """
        # 规范化工具名称
        normalized_name = TOOL_NAME_MAPPING.get(tool_name, tool_name)

        try:
            # 准备参数
            params = self.prepare_params(normalized_name, tool_args, state)

            # 调用 StandardTool
            result = await registry.call_tool(normalized_name, params)

            # 🔧 处理返回值为 JSON 字符串的情况（如 locate_content、@tool 装饰器返回值）
            if isinstance(result, str):
                try:
                    result = json.loads(result)
                except json.JSONDecodeError:
                    pass  # 保持原样，让后续逻辑处理

            # 提取返回值
            if isinstance(result, dict) and result.get("success"):
                tool_result = self.extract_result(normalized_name, result)
                logger.info(f"[StandardTool] {normalized_name} 执行成功")
                return tool_result
            else:
                error_msg = result.get("message", "执行失败") if isinstance(result, dict) else "未知错误"
                logger.error(f"[StandardTool] {normalized_name} 执行失败: {error_msg}")
                return json.dumps({"error": "tool_failed", "message": error_msg}, ensure_ascii=False)

        except ValueError as e:
            # StandardTool 不存在，降级到 @tool
            logger.warning(f"[StandardTool] '{normalized_name}' 不存在，降级到 @tool: {e}")
            return await self.fallback_to_legacy(tool_name, tool_args, state)

        except Exception as e:
            # 其他错误，也尝试降级
            logger.error(f"[StandardTool] 调用失败: {e}")
            return await self.fallback_to_legacy(tool_name, tool_args, state)

    def prepare_params(
        self,
        tool_name: str,
        tool_args: dict,
        state: dict
    ) -> dict:
        """准备工具参数（处理特殊情况）"""
        params = dict(tool_args)
        last_user_message = state.get("last_user_message", "")

        # 工具特定的参数处理
        if tool_name == "continue_writing":
            params.setdefault("context", last_user_message)
            params.setdefault("requirements", "")
            # 🔧 默认值从 500 改为 2000，更符合实际续写需求
            params.setdefault("target_length", 2000)
            params.setdefault("style", "")

        elif tool_name == "analyze_text":
            params.setdefault("text", last_user_message)
            params.setdefault("focus", "all")

        elif tool_name == "smart_rewrite":
            # P1修复：从 state 获取上下文信息作为兜底，避免参数全为 None
            current_chapter_id = state.get("chapter_id", "")
            context_data = state.get("context", {}) if isinstance(state.get("context"), dict) else {}
            selected_text = context_data.get("selected_text", "")
            locate_original_text = context_data.get("locate_original_text", "")

            params.setdefault("chapter_id", current_chapter_id)

            # text_to_rewrite: 优先使用参数值，其次使用选中文本
            if not params.get("text_to_rewrite"):
                params["text_to_rewrite"] = selected_text or locate_original_text or ""

            # chapter_content: 兜底使用 text_to_rewrite
            if not params.get("chapter_content"):
                params["chapter_content"] = params.get("text_to_rewrite", "")

            # user_requirement: 从用户消息中提取改写要求
            if not params.get("user_requirement"):
                params["user_requirement"] = state.get("last_user_message", "")

            # base_version: 默认空字符串（不是 None）
            params.setdefault("base_version", "")
            base_version = params.get("base_version")
            if base_version is None:
                params["base_version"] = ""
            elif not isinstance(base_version, str):
                if isinstance(base_version, (int, float)) and base_version == 0:
                    params["base_version"] = ""
                else:
                    params["base_version"] = str(base_version)
            params.setdefault("user_id", state.get("user_id"))

        elif tool_name == "smart_continue":
            params.setdefault("chapter_id", state.get("chapter_id", ""))
            params.setdefault("user_id", state.get("user_id"))

        elif tool_name == "smart_insert":
            params.setdefault("chapter_id", state.get("chapter_id", ""))
            params.setdefault("chapter_content", None)
            params.setdefault("context", None)
            params.setdefault("user_id", state.get("user_id"))

        elif tool_name == "locate_content":
            params.setdefault("chapter_id", state.get("chapter_id", ""))
            params.setdefault("node_id", state.get("context", {}).get("locate_node_id"))
            nodes_info = params.get("nodes_info")
            if nodes_info is not None and not isinstance(nodes_info, str):
                params["nodes_info"] = json.dumps(nodes_info, ensure_ascii=False)
            elif not nodes_info:
                context_nodes = state.get("context", {}).get("nodes_info")
                if context_nodes:
                    params["nodes_info"] = (
                        context_nodes
                        if isinstance(context_nodes, str)
                        else json.dumps(context_nodes, ensure_ascii=False)
                    )

        elif tool_name == "apply_chapter_edit":
            context = state.get("context", {}) if isinstance(state.get("context"), dict) else {}
            params.setdefault("chapter_id", state.get("chapter_id", ""))
            params.setdefault("operation", "append")
            params.setdefault("position", None)
            params.setdefault("before_anchor", None)  # 🆕 锚点定位
            params.setdefault("after_anchor", None)   # 🆕 锚点定位
            params.setdefault("original_text", None)  # 🆕 原文（用于前端定位）
            params.setdefault("node_id", context.get("locate_node_id"))
            params.setdefault("paragraph_index", context.get("locate_paragraph_index"))
            if not params.get("node_id"):
                params["node_id"] = context.get("locate_node_id")
            if params.get("paragraph_index") is None:
                params["paragraph_index"] = context.get("locate_paragraph_index")
            if not params.get("before_anchor"):
                params["before_anchor"] = context.get("locate_before_anchor")
            if not params.get("after_anchor"):
                params["after_anchor"] = context.get("locate_after_anchor")
            if not params.get("original_text"):
                params["original_text"] = context.get("locate_original_text")
            params.setdefault("user_id", state.get("user_id"))
            params.setdefault("description", None)
            params.setdefault("conversation_id", state.get("conversation_id", ""))
            params.setdefault("work_id", state.get("work_id", ""))

        elif tool_name == "get_context":
            params.setdefault("work_id", state.get("work_id", ""))
            params.setdefault("chapter_id", state.get("chapter_id", ""))

        elif tool_name == "read_chapter":
            params.setdefault("work_id", state.get("work_id", ""))
            params.setdefault("chapter_id", state.get("chapter_id", ""))

        elif tool_name == "get_chapter_by_order":
            params.setdefault("work_id", state.get("work_id", ""))
            params.setdefault("chapter_order", "1")  # 字符串类型

        elif tool_name == "search_analysis_fragments":
            params.setdefault("work_id", state.get("work_id", ""))
            params.setdefault("query", last_user_message)
            params.setdefault("top_k", 5)
            params.setdefault("chapter_id", state.get("chapter_id", ""))
            params.setdefault("include_current", True)
            params.setdefault("look_ahead", 0)
            params.setdefault("max_content_length", 2000)

        elif tool_name == "get_worldview_summary":
            params.setdefault("work_id", state.get("work_id", ""))

        elif tool_name == "evaluate_quality":
            if "text" in params and "content" not in params:
                params["content"] = params.pop("text")
            params.setdefault("content", last_user_message)
            params.setdefault("context", "novel")
            params.setdefault("criteria", ["readability", "creativity", "coherence", "engagement"])
            params.setdefault("reference", "")

        elif tool_name == "analyze_content":
            params.setdefault("content", last_user_message)
            params.setdefault("aspects", ["grammar", "logic", "style", "structure"])
            params.setdefault("depth", "normal")
            params.setdefault("context", "")

        # 章节管理工具（OPERATION 类）- 需要传递 conversation_id
        elif tool_name == "create_chapter":
            params.setdefault("work_id", state.get("work_id", ""))
            params.setdefault("title", "")
            params.setdefault("content", "")
            params.setdefault("order", None)
            params.setdefault("conversation_id", state.get("conversation_id", ""))

        elif tool_name == "update_chapter_title":
            params.setdefault("chapter_id", state.get("chapter_id", ""))
            params.setdefault("new_title", "")
            params.setdefault("old_title", None)
            params.setdefault("conversation_id", state.get("conversation_id", ""))
            params.setdefault("work_id", state.get("work_id", ""))  # v8.0: 用于章节序号解析

        elif tool_name == "delete_chapter":
            params.setdefault("chapter_id", state.get("chapter_id", ""))
            params.setdefault("chapter_title", None)
            params.setdefault("conversation_id", state.get("conversation_id", ""))
            params.setdefault("work_id", state.get("work_id", ""))  # v8.0: 用于章节序号解析

        elif tool_name == "update_chapter_content":
            params.setdefault("chapter_id", state.get("chapter_id", ""))
            params.setdefault("new_content", "")
            params.setdefault("operation", "replace")
            params.setdefault("position", None)
            params.setdefault("conversation_id", state.get("conversation_id", ""))
            params.setdefault("work_id", state.get("work_id", ""))  # v8.0: 用于章节序号解析

        return params

    def extract_result(self, tool_name: str, result: dict) -> str:
        """从 StandardTool 返回值中提取实际结果"""
        data = result.get("data", {})

        if tool_name == "continue_writing":
            return data.get("generated_text", "")

        elif tool_name == "analyze_text":
            return data.get("analysis_report", "")

        elif tool_name in ["smart_rewrite", "smart_continue", "smart_insert", "apply_chapter_edit"]:
            return json.dumps(data, ensure_ascii=False)

        elif tool_name == "locate_content":
            # locate_content 返回的 success 在顶层，data 就是整个结果
            # 返回完整 JSON 供下游工具使用
            return json.dumps(result, ensure_ascii=False)

        elif tool_name == "get_context":
            return data.get("context", "")

        elif tool_name == "read_chapter":
            return data.get("chapter_info", "")

        elif tool_name == "get_chapter_by_order":
            return data.get("chapter_info", "")

        elif tool_name == "search_analysis_fragments":
            return data.get("fragments", "")

        elif tool_name == "get_worldview_summary":
            # 返回 JSON 字符串格式的世界观摘要
            return json.dumps(data, ensure_ascii=False)

        elif tool_name == "evaluate_quality":
            feedback = data.get("feedback", "")
            overall_score = data.get("overall_score", 0)
            grade = data.get("grade", "B")
            return f"评分: {overall_score}/100 (等级: {grade})\n\n{feedback}"

        elif tool_name == "analyze_content":
            return data.get("analysis", data.get("summary", ""))

        # 章节管理工具（OPERATION 类）- 返回完整 JSON 供 HITL 处理
        elif tool_name in ["create_chapter", "update_chapter_title", "delete_chapter", "update_chapter_content"]:
            return json.dumps(data, ensure_ascii=False)

        return json.dumps(data, ensure_ascii=False)

    async def fallback_to_legacy(
        self,
        tool_name: str,
        tool_args: dict,
        state: dict
    ) -> str:
        """降级到 @tool 版本（向后兼容）"""
        from app.services.agent.langgraph_tools import (
            analyze_text_tool,
            get_worldview_summary,
        )
        from app.services.agent.tools.editor_tools import (
            smart_rewrite,
            smart_continue,
            smart_insert,
            apply_chapter_edit,
        )
        from app.services.agent.tools.show_dont_tell import (
            show_emotion_tool,
            enhance_scene_tool,
        )
        from app.services.agent.tools.style_learning import (
            learn_style_tool,
            analyze_style_tool,
            get_style_guidance_tool,
        )
        from app.services.agent.tools.chapter_tools import (
            create_chapter,
            update_chapter_title,
            delete_chapter,
            update_chapter_content,
        )
        from app.services.agent.tools.consistency_checker import (
            check_story_consistency_tool,
        )

        last_user_message = state.get("last_user_message", "")

        LEGACY_TOOLS = {
            "analyze_text_tool": analyze_text_tool,
            "smart_rewrite": smart_rewrite,
            "smart_continue": smart_continue,
            "smart_insert": smart_insert,
            "apply_chapter_edit": apply_chapter_edit,
            "get_worldview_summary": get_worldview_summary,
            # 创作增强工具
            "show_emotion_tool": show_emotion_tool,
            "enhance_scene_tool": enhance_scene_tool,
            "learn_style_tool": learn_style_tool,
            "analyze_style_tool": analyze_style_tool,
            "get_style_guidance_tool": get_style_guidance_tool,
            # 章节操作工具
            "create_chapter": create_chapter,
            "update_chapter_title": update_chapter_title,
            "delete_chapter": delete_chapter,
            "update_chapter_content": update_chapter_content,
            # 分析工具
            "check_story_consistency_tool": check_story_consistency_tool,
        }

        legacy_tool = LEGACY_TOOLS.get(tool_name)
        if legacy_tool:
            logger.info(f"[LegacyTool] 使用 @tool 版本: {tool_name}")
            try:
                if tool_name == "analyze_text_tool":
                    params = {
                        "text": tool_args.get("text", last_user_message),
                        "focus": tool_args.get("focus", "all")
                    }
                elif tool_name == "get_worldview_summary":
                    params = {
                        "work_id": tool_args.get("work_id", state.get("work_id", ""))
                    }
                elif tool_name == "show_emotion_tool":
                    params = {
                        "emotion": tool_args.get("emotion", ""),
                        "intensity": tool_args.get("intensity", 3)
                    }
                elif tool_name == "enhance_scene_tool":
                    params = {
                        "description": tool_args.get("description", tool_args.get("text", last_user_message))
                    }
                elif tool_name == "analyze_style_tool":
                    params = {
                        "text": tool_args.get("text", last_user_message)
                    }
                elif tool_name == "learn_style_tool":
                    params = {
                        "user_id": tool_args.get("user_id", state.get("user_id", "")),
                        "text": tool_args.get("text", last_user_message),
                        "profile_name": tool_args.get("profile_name", "default")
                    }
                elif tool_name == "get_style_guidance_tool":
                    params = {
                        "user_id": tool_args.get("user_id", state.get("user_id", "")),
                        "profile_name": tool_args.get("profile_name", "default")
                    }
                # 章节操作工具
                elif tool_name == "create_chapter":
                    params = {
                        "work_id": tool_args.get("work_id", state.get("work_id", "")),
                        "title": tool_args.get("title", ""),
                        "content": tool_args.get("content", ""),
                        "order": tool_args.get("order"),
                        "conversation_id": tool_args.get("conversation_id", state.get("conversation_id", ""))
                    }
                elif tool_name == "update_chapter_title":
                    params = {
                        "chapter_id": tool_args.get("chapter_id", state.get("chapter_id", "")),
                        "new_title": tool_args.get("new_title", ""),
                        "old_title": tool_args.get("old_title"),
                        "conversation_id": tool_args.get("conversation_id", state.get("conversation_id", "")),
                        "work_id": tool_args.get("work_id", state.get("work_id", ""))
                    }
                elif tool_name == "delete_chapter":
                    params = {
                        "chapter_id": tool_args.get("chapter_id", state.get("chapter_id", "")),
                        "chapter_title": tool_args.get("chapter_title"),
                        "conversation_id": tool_args.get("conversation_id", state.get("conversation_id", "")),
                        "work_id": tool_args.get("work_id", state.get("work_id", ""))
                    }
                elif tool_name == "update_chapter_content":
                    params = {
                        "chapter_id": tool_args.get("chapter_id", state.get("chapter_id", "")),
                        "new_content": tool_args.get("new_content", tool_args.get("content", "")),
                        "operation": tool_args.get("operation", "replace"),
                        "position": tool_args.get("position"),
                        "conversation_id": tool_args.get("conversation_id", state.get("conversation_id", "")),
                        "work_id": tool_args.get("work_id", state.get("work_id", ""))
                    }
                elif tool_name == "apply_chapter_edit":
                    params = {
                        "chapter_id": tool_args.get("chapter_id", state.get("chapter_id", "")),
                        "content": tool_args.get("content", ""),
                        "operation": tool_args.get("operation", "replace"),
                        "position": tool_args.get("position"),
                        "before_anchor": tool_args.get("before_anchor"),
                        "after_anchor": tool_args.get("after_anchor"),
                        "original_text": tool_args.get("original_text"),
                        "node_id": tool_args.get("node_id"),
                        "paragraph_index": tool_args.get("paragraph_index"),
                        "user_id": tool_args.get("user_id", state.get("user_id", "")),
                        "description": tool_args.get("description"),
                        "conversation_id": tool_args.get("conversation_id", state.get("conversation_id", "")),
                        "work_id": tool_args.get("work_id", state.get("work_id", ""))
                    }
                # 分析工具
                elif tool_name == "check_story_consistency_tool":
                    params = {
                        "work_id": tool_args.get("work_id", state.get("work_id", "")),
                        "chapters_json": tool_args.get("chapters_json", "[]"),
                        "characters_json": tool_args.get("characters_json", "[]"),
                        "worldview_json": tool_args.get("worldview_json", "{}")
                    }
                else:
                    params = tool_args

                return await legacy_tool.ainvoke(params)
            except Exception as e:
                logger.error(f"[LegacyTool] 调用失败: {e}")
                return json.dumps({"error": "legacy_tool_failed", "message": str(e)}, ensure_ascii=False)

        logger.error(f"[ToolCall] 未知工具: {tool_name}")
        return json.dumps({"error": "unknown_tool", "message": f"未知工具: {tool_name}"}, ensure_ascii=False)
