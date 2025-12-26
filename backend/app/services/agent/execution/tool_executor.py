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
    "continue_writing_tool": "continue_writing",
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
    # 分析工具
    "evaluate_quality_tool": "evaluate_quality",
    "analyze_content_tool": "analyze_content",
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
            params.setdefault("target_length", 500)
            params.setdefault("style", "")

        elif tool_name == "analyze_text":
            params.setdefault("text", last_user_message)
            params.setdefault("focus", "all")

        elif tool_name == "smart_rewrite":
            params.setdefault("chapter_id", state.get("chapter_id", ""))
            params.setdefault("text_to_rewrite", None)
            params.setdefault("chapter_content", None)
            params.setdefault("user_requirement", None)
            params.setdefault("base_version", None)
            params.setdefault("user_id", state.get("user_id"))

        elif tool_name == "smart_continue":
            params.setdefault("chapter_id", state.get("chapter_id", ""))
            params.setdefault("user_id", state.get("user_id"))

        elif tool_name == "smart_insert":
            params.setdefault("chapter_id", state.get("chapter_id", ""))
            params.setdefault("chapter_content", None)
            params.setdefault("context", None)
            params.setdefault("user_id", state.get("user_id"))

        elif tool_name == "apply_chapter_edit":
            params.setdefault("chapter_id", state.get("chapter_id", ""))
            params.setdefault("operation", "append")
            params.setdefault("position", None)
            params.setdefault("user_id", state.get("user_id"))
            params.setdefault("description", None)

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
            params.setdefault("look_ahead", 2)

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

        elif tool_name == "get_context":
            return data.get("context", "")

        elif tool_name == "read_chapter":
            return data.get("chapter_info", "")

        elif tool_name == "get_chapter_by_order":
            return data.get("chapter_info", "")

        elif tool_name == "search_analysis_fragments":
            return data.get("fragments", "")

        elif tool_name == "evaluate_quality":
            feedback = data.get("feedback", "")
            overall_score = data.get("overall_score", 0)
            grade = data.get("grade", "B")
            return f"评分: {overall_score}/100 (等级: {grade})\n\n{feedback}"

        elif tool_name == "analyze_content":
            return data.get("analysis", data.get("summary", ""))

        return json.dumps(data, ensure_ascii=False)

    async def fallback_to_legacy(
        self,
        tool_name: str,
        tool_args: dict,
        state: dict
    ) -> str:
        """降级到 @tool 版本（向后兼容）"""
        from app.services.agent.langgraph_tools import (
            continue_writing_tool,
            analyze_text_tool,
        )
        from app.services.agent.tools.editor_tools import (
            smart_rewrite,
            smart_continue,
            smart_insert,
            apply_chapter_edit,
        )

        last_user_message = state.get("last_user_message", "")

        LEGACY_TOOLS = {
            "continue_writing_tool": continue_writing_tool,
            "analyze_text_tool": analyze_text_tool,
            "smart_rewrite": smart_rewrite,
            "smart_continue": smart_continue,
            "smart_insert": smart_insert,
            "apply_chapter_edit": apply_chapter_edit,
        }

        legacy_tool = LEGACY_TOOLS.get(tool_name)
        if legacy_tool:
            logger.info(f"[LegacyTool] 使用 @tool 版本: {tool_name}")
            try:
                if tool_name == "continue_writing_tool":
                    params = {
                        "context": tool_args.get("context", last_user_message),
                        "requirements": tool_args.get("requirements", "")
                    }
                elif tool_name == "analyze_text_tool":
                    params = {
                        "text": tool_args.get("text", last_user_message),
                        "focus": tool_args.get("focus", "all")
                    }
                else:
                    params = tool_args

                return await legacy_tool.ainvoke(params)
            except Exception as e:
                logger.error(f"[LegacyTool] 调用失败: {e}")
                return json.dumps({"error": "legacy_tool_failed", "message": str(e)}, ensure_ascii=False)

        logger.error(f"[ToolCall] 未知工具: {tool_name}")
        return json.dumps({"error": "unknown_tool", "message": f"未知工具: {tool_name}"}, ensure_ascii=False)
