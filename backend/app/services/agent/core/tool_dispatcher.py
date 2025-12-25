"""
工具分发模块 - 统一工具调用分发

从 langgraph_agent.py 的 _handle_with_httpai 方法中拆分。
负责根据工具名称分发到具体的工具调用逻辑。
"""

import json
import logging
import re
from typing import Dict, Any, Optional, TYPE_CHECKING

from app.services.agent.tools.tool_registry import registry
from app.services.agent.utils.tool_helpers import resolve_version_reference

# 导入 @tool 版本用于降级
from app.services.agent.langgraph_tools import (
    continue_writing_tool,
    analyze_text_tool,
    get_context_tool,
    read_chapter_tool,
    get_chapter_by_order_tool,
    search_analysis_fragments_tool,
    smart_rewrite,
    smart_continue,
    smart_insert,
    apply_chapter_edit,
)

if TYPE_CHECKING:
    from app.services.agent.langgraph_agent import AgentState

logger = logging.getLogger(__name__)


class ToolDispatcher:
    """工具分发器 - 统一工具调用分发"""

    # 编辑意图关键词
    MODIFY_KEYWORDS = [
        "修改", "改写", "重写", "续写", "插入", "帮我改", "你来改",
        "来帮我改", "改一下", "太平淡", "帮改", "改改"
    ]

    def __init__(self, agent):
        """
        初始化工具分发器

        Args:
            agent: WritingAgentGraph 实例（用于访问其方法和状态）
        """
        self.agent = agent

    async def dispatch_tool(
        self,
        tool_name: str,
        tool_args: Dict[str, Any],
        state: "AgentState",
        last_user_message: str,
    ) -> str:
        """
        根据工具名称分发到具体的工具调用

        Args:
            tool_name: 工具名称
            tool_args: 工具参数
            state: Agent 状态
            last_user_message: 最后的用户消息

        Returns:
            工具执行结果（字符串）
        """
        logger.info(f"[ToolDispatcher] 分发工具调用: {tool_name}")

        # 1. 续写工具
        if tool_name == "continue_writing_tool":
            return await self._call_continue_writing(tool_args, last_user_message)

        # 2. 分析工具
        elif tool_name == "analyze_text_tool":
            return await self._call_analyze_text(tool_args, last_user_message)

        # 3. 获取上下文工具
        elif tool_name == "get_context_tool":
            return await self._call_get_context(tool_args, state)

        # 4. 读取章节工具
        elif tool_name == "read_chapter_tool":
            return await self._call_read_chapter(tool_args, state)

        # 5. 按序号获取章节工具
        elif tool_name == "get_chapter_by_order_tool":
            return await self._call_get_chapter_by_order(tool_args, state)

        # 6. 搜索分析片段工具
        elif tool_name == "search_analysis_fragments_tool":
            return await self._call_search_analysis_fragments(tool_args, state, last_user_message)

        # 7. 智能改写工具
        elif tool_name == "smart_rewrite":
            return await self._call_smart_rewrite(tool_args, state)

        # 8. 智能续写工具
        elif tool_name == "smart_continue":
            return await self._call_smart_continue(tool_args, state)

        # 9. 智能插入工具
        elif tool_name == "smart_insert":
            return await self._call_smart_insert(tool_args, state)

        # 10. 应用章节编辑工具
        elif tool_name == "apply_chapter_edit":
            return await self._call_apply_chapter_edit(tool_args, state)

        # 其他工具：使用统一接口
        else:
            return await self._call_generic_tool(tool_name, tool_args, state)

    # ==================== 具体工具调用实现 ====================

    async def _call_continue_writing(
        self, tool_args: Dict[str, Any], last_user_message: str
    ) -> str:
        """调用续写工具"""
        try:
            result = await registry.call_tool("continue_writing", {
                "context": tool_args.get("context", last_user_message),
                "requirements": tool_args.get("requirements", ""),
                "target_length": tool_args.get("target_length", 500),
                "style": tool_args.get("style", "")
            })

            if isinstance(result, dict) and result.get("success"):
                tool_result = result.get("data", {}).get("generated_text", "")
                logger.info(f"[StandardTool] continue_writing 执行成功，字数: {len(tool_result)}")
                return tool_result
            else:
                error_msg = result.get("message", "执行失败") if isinstance(result, dict) else "未知错误"
                logger.error(f"[StandardTool] continue_writing 执行失败: {error_msg}")
                return json.dumps({"error": "tool_failed", "message": error_msg}, ensure_ascii=False)

        except Exception as e:
            logger.warning(f"[StandardTool] 调用失败，降级到 @tool 版本: {e}")
            return await continue_writing_tool.ainvoke({
                "context": tool_args.get("context", last_user_message),
                "requirements": tool_args.get("requirements", "")
            })

    async def _call_analyze_text(
        self, tool_args: Dict[str, Any], last_user_message: str
    ) -> str:
        """调用分析工具"""
        try:
            result = await registry.call_tool("analyze_text", {
                "text": tool_args.get("text", last_user_message),
                "focus": tool_args.get("focus", "all")
            })

            if isinstance(result, dict) and result.get("success"):
                tool_result = result.get("data", {}).get("analysis_report", "")
                logger.info(f"[StandardTool] analyze_text 执行成功，结果长度: {len(tool_result)}")
                return tool_result
            else:
                error_msg = result.get("message", "执行失败") if isinstance(result, dict) else "未知错误"
                logger.error(f"[StandardTool] analyze_text 执行失败: {error_msg}")
                return json.dumps({"error": "tool_failed", "message": error_msg}, ensure_ascii=False)

        except Exception as e:
            logger.warning(f"[StandardTool] 调用失败，降级到 @tool 版本: {e}")
            return await analyze_text_tool.ainvoke({
                "text": tool_args.get("text", last_user_message),
                "focus": tool_args.get("focus", "all")
            })

    async def _call_get_context(
        self, tool_args: Dict[str, Any], state: "AgentState"
    ) -> str:
        """调用获取上下文工具"""
        work_id_value = state.get("work_id")
        if not work_id_value:
            logger.warning(f"[ToolDispatcher] ⚠️ get_context_tool 缺少必需参数 work_id")
            return json.dumps({
                "error": "missing_work_id",
                "message": "需要提供作品ID才能获取上下文",
                "user_prompt": "请先告诉我您要操作哪部作品？"
            }, ensure_ascii=False)

        logger.info(f"[ToolDispatcher] 🚀 准备调用 get_context_tool, work_id={work_id_value}")
        try:
            result = await registry.call_tool("get_context", {
                "work_id": work_id_value,
                "chapter_id": state.get("chapter_id", "")
            })

            if isinstance(result, dict) and result.get("success"):
                tool_result = result.get("data", {}).get("context", "")
                logger.info(f"[StandardTool] get_context 执行成功，长度: {len(tool_result)} 字符")
                return tool_result
            else:
                error_msg = result.get("message", "执行失败") if isinstance(result, dict) else "未知错误"
                logger.error(f"[StandardTool] get_context 执行失败: {error_msg}")
                return json.dumps({"error": "tool_failed", "message": error_msg}, ensure_ascii=False)

        except Exception as e:
            logger.warning(f"[StandardTool] get_context 调用失败，降级到 @tool: {e}")
            return await get_context_tool.ainvoke({
                "work_id": work_id_value,
                "chapter_id": state.get("chapter_id", "")
            })

    async def _call_read_chapter(
        self, tool_args: Dict[str, Any], state: "AgentState"
    ) -> str:
        """调用读取章节工具"""
        work_id_value = state.get("work_id")
        if not work_id_value:
            logger.warning(f"[ToolDispatcher] ⚠️ read_chapter_tool 缺少必需参数 work_id")
            return json.dumps({
                "error": "missing_work_id",
                "message": "需要提供作品ID才能读取章节",
                "user_prompt": "请先告诉我您要读取哪部作品的章节？"
            }, ensure_ascii=False)

        try:
            result = await registry.call_tool("read_chapter", {
                "work_id": work_id_value,
                "chapter_id": tool_args.get("chapter_id") or state.get("chapter_id") or ""
            })

            if isinstance(result, dict) and result.get("success"):
                tool_result = result.get("data", {}).get("chapter_info", "")
                logger.info(f"[StandardTool] read_chapter 执行成功")
                return tool_result
            else:
                error_msg = result.get("message", "执行失败") if isinstance(result, dict) else "未知错误"
                logger.error(f"[StandardTool] read_chapter 执行失败: {error_msg}")
                return json.dumps({"error": "tool_failed", "message": error_msg}, ensure_ascii=False)

        except Exception as e:
            logger.warning(f"[StandardTool] read_chapter 调用失败，降级到 @tool: {e}")
            return await read_chapter_tool.ainvoke({
                "work_id": work_id_value,
                "chapter_id": tool_args.get("chapter_id") or state.get("chapter_id") or ""
            })

    async def _call_get_chapter_by_order(
        self, tool_args: Dict[str, Any], state: "AgentState"
    ) -> str:
        """调用按序号获取章节工具"""
        work_id_value = state.get("work_id")
        if not work_id_value:
            logger.warning(f"[ToolDispatcher] ⚠️ get_chapter_by_order_tool 缺少必需参数 work_id")
            return json.dumps({
                "error": "missing_work_id",
                "message": "需要提供作品ID才能查询章节",
                "user_prompt": "请先告诉我您要查看哪部作品的章节？您可以说：\n- 「我想看《作品名》的第X章」\n- 或者先创建一部新作品"
            }, ensure_ascii=False)

        logger.info(f"[ToolDispatcher] 🚀 准备调用 get_chapter_by_order_tool, work_id={work_id_value}")
        try:
            result = await registry.call_tool("get_chapter_by_order", {
                "work_id": work_id_value,
                "chapter_order": tool_args.get("chapter_order", 1)
            })

            if isinstance(result, dict) and result.get("success"):
                tool_result = result.get("data", {}).get("chapter_info", "")
                logger.info(f"[StandardTool] get_chapter_by_order 执行成功")
                return tool_result
            else:
                error_msg = result.get("message", "执行失败") if isinstance(result, dict) else "未知错误"
                logger.error(f"[StandardTool] get_chapter_by_order 执行失败: {error_msg}")
                return json.dumps({"error": "tool_failed", "message": error_msg}, ensure_ascii=False)

        except Exception as e:
            logger.warning(f"[StandardTool] get_chapter_by_order 调用失败，降级到 @tool: {e}")
            return await get_chapter_by_order_tool.ainvoke({
                "work_id": work_id_value,
                "chapter_order": tool_args.get("chapter_order", 1)
            })

    async def _call_search_analysis_fragments(
        self, tool_args: Dict[str, Any], state: "AgentState", last_user_message: str
    ) -> str:
        """调用搜索分析片段工具"""
        work_id_value = state.get("work_id")
        if not work_id_value:
            logger.warning(f"[ToolDispatcher] ⚠️ search_analysis_fragments_tool 缺少必需参数 work_id")
            return json.dumps({
                "error": "missing_work_id",
                "message": "需要提供作品ID才能搜索分析片段",
                "user_prompt": "请先告诉我您要搜索哪部作品的分析片段？"
            }, ensure_ascii=False)

        try:
            result = await registry.call_tool("search_analysis_fragments", {
                "work_id": work_id_value,
                "query": tool_args.get("query", last_user_message),
                "top_k": tool_args.get("top_k", 5),
                "chapter_id": state.get("chapter_id", ""),
                "include_current": tool_args.get("include_current", True),
                "look_ahead": tool_args.get("look_ahead", 2)
            })

            if isinstance(result, dict) and result.get("success"):
                tool_result = result.get("data", {}).get("fragments", "")
                logger.info(f"[StandardTool] search_analysis_fragments 执行成功")
                return tool_result
            else:
                error_msg = result.get("message", "执行失败") if isinstance(result, dict) else "未知错误"
                logger.error(f"[StandardTool] search_analysis_fragments 执行失败: {error_msg}")
                return json.dumps({"error": "tool_failed", "message": error_msg}, ensure_ascii=False)

        except Exception as e:
            logger.warning(f"[StandardTool] search_analysis_fragments 调用失败，降级到 @tool: {e}")
            return await search_analysis_fragments_tool.ainvoke({
                "work_id": work_id_value,
                "query": tool_args.get("query", last_user_message),
                "top_k": tool_args.get("top_k", 5),
                "chapter_id": state.get("chapter_id", ""),
                "include_current": tool_args.get("include_current", True),
                "look_ahead": tool_args.get("look_ahead", 2),
            })

    async def _call_smart_rewrite(
        self, tool_args: Dict[str, Any], state: "AgentState"
    ) -> str:
        """调用智能改写工具"""
        text_to_rewrite = tool_args.get("text_to_rewrite") or tool_args.get("content", "")
        chapter_content = tool_args.get("chapter_content", "")
        user_requirement = tool_args.get("user_requirement", "")
        base_version = tool_args.get("base_version", "")

        # InlineAI 支持：优先使用 context 中的 selected_text
        context = state.get("context", {})
        selected_text = context.get("selected_text", "")
        selection_position = context.get("selection_position", None)

        # 如果有 selected_text，强制使用它
        if selected_text:
            logger.info(f"[ToolDispatcher] 📝 强制使用 InlineAI selected_text ({len(selected_text)} 字符)")
            text_to_rewrite = selected_text

        # 智能版本引用
        last_versions = state.get("context", {}).get("last_rewrite_versions", {})
        if base_version and last_versions:
            resolved_version = resolve_version_reference(base_version, last_versions)
            if resolved_version:
                logger.info(f"[ToolDispatcher] 🔄 智能版本解析成功")
                base_version = resolved_version

        logger.info(f"[ToolDispatcher] 🚀 准备调用 smart_rewrite")

        try:
            result = await registry.call_tool("smart_rewrite", {
                "chapter_id": tool_args.get("chapter_id", ""),
                "text_to_rewrite": text_to_rewrite,
                "chapter_content": chapter_content,
                "user_requirement": user_requirement,
                "base_version": base_version,
                "user_id": state.get("user_id")
            })

            if isinstance(result, dict) and result.get("success"):
                tool_result = json.dumps(result.get("data", {}), ensure_ascii=False)
                logger.info(f"[StandardTool] smart_rewrite 执行成功")
            else:
                error_msg = result.get("message", "执行失败") if isinstance(result, dict) else "未知错误"
                tool_result = json.dumps({"error": "tool_failed", "message": error_msg}, ensure_ascii=False)
                logger.error(f"[StandardTool] smart_rewrite 执行失败: {error_msg}")

        except Exception as e:
            logger.warning(f"[StandardTool] smart_rewrite 调用失败，降级到 @tool: {e}")
            tool_result = await smart_rewrite.ainvoke({
                "chapter_id": tool_args.get("chapter_id", ""),
                "text_to_rewrite": text_to_rewrite,
                "chapter_content": chapter_content,
                "user_requirement": user_requirement,
                "base_version": base_version,
                "user_id": state.get("user_id")
            })

        # 保存版本记忆
        self._save_version_memory(tool_result, state, selected_text, selection_position, text_to_rewrite)

        return tool_result

    async def _call_smart_continue(
        self, tool_args: Dict[str, Any], state: "AgentState"
    ) -> str:
        """调用智能续写工具"""
        logger.info(f"[ToolDispatcher] 🚀 准备调用 smart_continue")

        context = state.get("context", {})
        selected_text = context.get("selected_text", "")
        selection_position = context.get("selection_position", None)

        try:
            result = await registry.call_tool("smart_continue", {
                "chapter_id": tool_args.get("chapter_id", ""),
                "content": tool_args.get("context", ""),
                "user_id": state.get("user_id")
            })

            if isinstance(result, dict) and result.get("success"):
                tool_result = json.dumps(result.get("data", {}), ensure_ascii=False)
                logger.info(f"[StandardTool] smart_continue 执行成功")
            else:
                error_msg = result.get("message", "执行失败") if isinstance(result, dict) else "未知错误"
                tool_result = json.dumps({"error": "tool_failed", "message": error_msg}, ensure_ascii=False)
                logger.error(f"[StandardTool] smart_continue 执行失败: {error_msg}")

        except Exception as e:
            logger.warning(f"[StandardTool] smart_continue 调用失败，降级到 @tool: {e}")
            tool_result = await smart_continue.ainvoke({
                "chapter_id": tool_args.get("chapter_id", ""),
                "content": tool_args.get("context", ""),
                "user_id": state.get("user_id")
            })

        # InlineAI: 添加 editor_action 字段
        if selected_text and selection_position:
            try:
                result_obj = json.loads(tool_result) if isinstance(tool_result, str) else tool_result
                result_obj["editor_action"] = {
                    "type": "continue",
                    "position": selection_position,
                    "requires_confirmation": True
                }
                tool_result = json.dumps(result_obj, ensure_ascii=False)
                logger.info(f"[ToolDispatcher] 📝 添加 editor_action (continue)")
            except Exception as e:
                logger.warning(f"[ToolDispatcher] 添加 editor_action 失败: {e}")

        return tool_result

    async def _call_smart_insert(
        self, tool_args: Dict[str, Any], state: "AgentState"
    ) -> str:
        """调用智能插入工具"""
        logger.info(f"[ToolDispatcher] 🚀 准备调用 smart_insert")

        try:
            result = await registry.call_tool("smart_insert", {
                "chapter_id": tool_args.get("chapter_id", ""),
                "content": tool_args.get("content", ""),
                "user_intent": tool_args.get("position", "end"),
                "chapter_content": None,
                "context": None,
                "user_id": state.get("user_id")
            })

            if isinstance(result, dict) and result.get("success"):
                tool_result = json.dumps(result.get("data", {}), ensure_ascii=False)
                logger.info(f"[StandardTool] smart_insert 执行成功")
            else:
                error_msg = result.get("message", "执行失败") if isinstance(result, dict) else "未知错误"
                tool_result = json.dumps({"error": "tool_failed", "message": error_msg}, ensure_ascii=False)
                logger.error(f"[StandardTool] smart_insert 执行失败: {error_msg}")

        except Exception as e:
            logger.warning(f"[StandardTool] smart_insert 调用失败，降级到 @tool: {e}")
            tool_result = await smart_insert.ainvoke({
                "chapter_id": tool_args.get("chapter_id", ""),
                "content": tool_args.get("content", ""),
                "user_intent": tool_args.get("position", "end"),
                "chapter_content": None,
                "context": None,
                "user_id": state.get("user_id")
            })

        return tool_result

    async def _call_apply_chapter_edit(
        self, tool_args: Dict[str, Any], state: "AgentState"
    ) -> str:
        """调用应用章节编辑工具"""
        logger.info(f"[ToolDispatcher] 🚀 准备调用 apply_chapter_edit")

        try:
            result = await registry.call_tool("apply_chapter_edit", {
                "chapter_id": tool_args.get("chapter_id", ""),
                "content": tool_args.get("content", ""),
                "operation": tool_args.get("operation", "replace"),
                "position": None,
                "user_id": state.get("user_id"),
                "description": None
            })

            if isinstance(result, dict) and result.get("success"):
                tool_result = json.dumps(result.get("data", {}), ensure_ascii=False)
                logger.info(f"[StandardTool] apply_chapter_edit 执行成功")
            else:
                error_msg = result.get("message", "执行失败") if isinstance(result, dict) else "未知错误"
                tool_result = json.dumps({"error": "tool_failed", "message": error_msg}, ensure_ascii=False)
                logger.error(f"[StandardTool] apply_chapter_edit 执行失败: {error_msg}")

        except Exception as e:
            logger.warning(f"[StandardTool] apply_chapter_edit 调用失败，降级到 @tool: {e}")
            tool_result = await apply_chapter_edit.ainvoke({
                "chapter_id": tool_args.get("chapter_id", ""),
                "content": tool_args.get("content", ""),
                "operation": tool_args.get("operation", "replace"),
                "position": None,
                "user_id": state.get("user_id"),
                "description": None
            })

        return tool_result

    async def _call_generic_tool(
        self, tool_name: str, tool_args: Dict[str, Any], state: "AgentState"
    ) -> str:
        """使用统一接口调用其他工具"""
        logger.info(f"[ToolDispatcher] 使用统一接口调用工具: {tool_name}")
        try:
            tool_result = await self.agent._call_tool_via_registry(
                tool_name=tool_name,
                tool_args=tool_args,
                state=state
            )
            logger.info(f"[ToolDispatcher] ✅ 统一接口调用成功: {tool_name}")
            return tool_result
        except Exception as e:
            logger.error(f"[ToolDispatcher] 统一接口调用失败: {tool_name}, 错误: {e}")
            return json.dumps({
                "error": "tool_call_failed",
                "message": f"工具调用失败: {str(e)}",
                "user_prompt": "抱歉，我在处理您的请求时遇到了问题。能否换个方式描述？"
            }, ensure_ascii=False)

    # ==================== 辅助方法 ====================

    def _save_version_memory(
        self,
        tool_result: str,
        state: "AgentState",
        selected_text: str,
        selection_position: Optional[Dict],
        text_to_rewrite: str,
    ) -> None:
        """保存版本记忆"""
        try:
            result_obj = json.loads(tool_result) if isinstance(tool_result, str) else tool_result

            if result_obj.get("success") and result_obj.get("versions"):
                versions = result_obj["versions"]
                state["context"] = state.get("context", {})
                state["context"]["last_rewrite_versions"] = {
                    "version_a": versions[0].get("content", "") if len(versions) > 0 else "",
                    "version_b": versions[1].get("content", "") if len(versions) > 1 else "",
                    "version_c": versions[2].get("content", "") if len(versions) > 2 else ""
                }
                logger.info(f"[ToolDispatcher] 💾 已保存 {len(versions)} 个改写版本到 context")

                # InlineAI: 添加 editor_action 字段
                if selected_text and selection_position:
                    result_obj["editor_action"] = {
                        "type": "modify",
                        "original_text": text_to_rewrite,
                        "position": selection_position,
                        "requires_confirmation": True
                    }
                    logger.info(f"[ToolDispatcher] 📝 添加 editor_action (modify)")
        except Exception as e:
            logger.warning(f"[ToolDispatcher] 保存版本记忆失败: {e}")

    @classmethod
    def needs_second_tool_call(cls, user_message: str, agent_type: str) -> bool:
        """
        检查是否需要二次工具调用

        Args:
            user_message: 用户消息
            agent_type: Agent 类型

        Returns:
            是否需要二次工具调用
        """
        if agent_type != "writing":
            return False
        return any(kw in user_message for kw in cls.MODIFY_KEYWORDS)

    @classmethod
    def parse_decision_json(cls, decision_text: str) -> Optional[Dict[str, Any]]:
        """
        解析 AI 决策 JSON

        Args:
            decision_text: AI 返回的决策文本

        Returns:
            解析后的决策字典，解析失败返回 None
        """
        # 方法 1: 尝试直接解析整个文本
        try:
            decision = json.loads(decision_text.strip())
            logger.info(f"[ToolDispatcher] 方法1成功: 直接解析整个文本")
            return decision
        except:
            pass

        # 方法 2: 使用正则提取 JSON
        json_matches = re.finditer(r'\{(?:[^{}]|(?:\{[^}]*\}))*\}', decision_text)
        for match in json_matches:
            try:
                candidate = json.loads(match.group())
                if "need_tools" in candidate:
                    logger.info(f"[ToolDispatcher] 方法2成功: 正则提取 JSON")
                    return candidate
            except:
                continue

        # 方法 3: 解析失败
        logger.warning(f"[ToolDispatcher] 无法解析JSON决策，原文前200字符: {decision_text[:200]}")
        return None

    @classmethod
    def check_tool_error(cls, tool_result: str) -> Optional[str]:
        """
        检查工具是否返回错误

        Args:
            tool_result: 工具返回结果

        Returns:
            如果是错误，返回友好提示；否则返回 None
        """
        try:
            tool_result_obj = json.loads(tool_result)
            error_type = tool_result_obj.get("error")
            if error_type in ["missing_work_id", "unknown_tool"]:
                logger.info(f"[ToolDispatcher] 🎯 检测到工具错误({error_type})")
                return tool_result_obj.get("user_prompt", "请先告诉我您要操作哪部作品？")
        except json.JSONDecodeError:
            pass
        except Exception as e:
            logger.warning(f"[ToolDispatcher] 解析工具结果异常: {e}")

        return None
