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
from app.services.agent.utils.chapter_cache import ChapterCache

# 导入 @tool 版本用于降级
from app.services.agent.langgraph_tools import (
    analyze_text_tool,
    analyze_content,
    get_context_tool,
    read_chapter_tool,
    get_chapter_by_order_tool,
    search_analysis_fragments_tool,
    search_content,
    smart_rewrite,
    smart_continue,
    smart_insert,
    apply_chapter_edit,
)

if TYPE_CHECKING:
    from app.services.agent.langgraph_agent import AgentState

logger = logging.getLogger(__name__)


# ==================== 工具分类列表（2026-01-09）====================

# 创作类工具：AI生成内容，不直接修改数据库
CREATIVE_TOOLS = [
    "smart_rewrite",
    "smart_continue",
    "smart_insert",
    "show_emotion_tool",
    "enhance_scene_tool",
    "learn_style_tool",
]

# 操作类工具：直接修改数据库，需要用户确认
OPERATION_TOOLS = [
    "apply_chapter_edit",
    "create_chapter",
    "update_chapter_title",
    "delete_chapter",
    "update_chapter_content",
    "operate_apply",  # 2026-01-23: ContentOperator 统一入口
]

# 查询类工具：只读取数据，不修改
QUERY_TOOLS = [
    "get_context_tool",
    "read_chapter_tool",
    "get_chapter_by_order_tool",
    "search_analysis_fragments_tool",
    "search_content",
    "get_writing_context",
    "get_worldview_summary",
    "get_style_guidance_tool",
    "explore_content",  # 2026-01-18: 统一信息获取入口
    "load_explore_artifact",  # 2026-02-03: Explore Artifact 读取
    "locate_content",   # 2026-01-18: 定位工具
]

# 分析类工具：分析内容，不修改数据
ANALYSIS_TOOLS = [
    "analyze_text_tool",
    "analyze_content",
    "check_story_consistency_tool",
    "analyze_style_tool",
]


def get_tool_category(tool_name: str) -> str:
    """获取工具分类

    Args:
        tool_name: 工具名称

    Returns:
        工具分类: "creative" | "operation" | "query" | "analysis" | "unknown"
    """
    if tool_name in CREATIVE_TOOLS:
        return "creative"
    elif tool_name in OPERATION_TOOLS:
        return "operation"
    elif tool_name in QUERY_TOOLS:
        return "query"
    elif tool_name in ANALYSIS_TOOLS:
        return "analysis"
    return "unknown"


def requires_confirmation(tool_name: str) -> bool:
    """判断工具是否需要用户确认

    Args:
        tool_name: 工具名称

    Returns:
        是否需要用户确认
    """
    return tool_name in OPERATION_TOOLS


class ToolDispatcher:
    """工具分发器 - 统一工具调用分发"""

    # 编辑意图关键词
    # 2026-01-09: 添加"优化"、"扩写"、"润色"，与 secondary_tool_handler.py 保持一致
    MODIFY_KEYWORDS = [
        "修改", "改写", "重写", "续写", "插入", "帮我改", "你来改",
        "来帮我改", "改一下", "太平淡", "帮改", "改改",
        "优化", "扩写", "润色"  # 2026-01-09 新增
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

        # 1. 分析工具
        if tool_name == "analyze_text_tool":
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

        # 6.1 搜索内容工具
        elif tool_name == "search_content":
            return await self._call_search_content(tool_args, state, last_user_message)

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

        # 11. 删除章节工具（2026-01-09 新增）
        elif tool_name == "delete_chapter":
            return await self._call_delete_chapter(tool_args, state)

        # 12. 更新章节内容工具（2026-01-09 新增）
        elif tool_name == "update_chapter_content":
            return await self._call_update_chapter_content(tool_args, state)

        # 13. operate_apply 统一操作工具（2026-01-23 新增）
        elif tool_name == "operate_apply":
            return await self._call_operate_apply(tool_args, state)

        # 其他工具：使用统一接口
        else:
            return await self._call_generic_tool(tool_name, tool_args, state)

    # ==================== 具体工具调用实现 ====================

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

        chapter_id = tool_args.get("chapter_id") or state.get("chapter_id") or ""

        # 🆕 2026-01-12: 缓存检查
        if chapter_id and "," not in chapter_id:
            cached = ChapterCache.get_by_id(state, chapter_id)
            if cached:
                return json.dumps(cached, ensure_ascii=False, indent=2)

        try:
            result = await registry.call_tool("read_chapter", {
                "work_id": work_id_value,
                "chapter_id": chapter_id
            })

            if isinstance(result, dict) and result.get("success"):
                tool_result = result.get("data", {}).get("chapter_info", "")
                logger.info(f"[StandardTool] read_chapter 执行成功")

                # 🆕 2026-01-12: 缓存写入
                self._update_chapter_cache(tool_result, work_id_value, state)

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

        chapter_order = tool_args.get("chapter_order", 1)

        # 🆕 2026-01-12: 缓存检查（只对单章节）
        chapter_order_str = str(chapter_order)
        if chapter_order_str.isdigit():
            cached = ChapterCache.get_by_order(state, work_id_value, int(chapter_order_str))
            if cached:
                return json.dumps(cached, ensure_ascii=False, indent=2)

        logger.info(f"[ToolDispatcher] 🚀 准备调用 get_chapter_by_order_tool, work_id={work_id_value}")
        try:
            result = await registry.call_tool("get_chapter_by_order", {
                "work_id": work_id_value,
                "chapter_order": chapter_order
            })

            if isinstance(result, dict) and result.get("success"):
                tool_result = result.get("data", {}).get("chapter_info", "")
                logger.info(f"[StandardTool] get_chapter_by_order 执行成功")

                # 🆕 2026-01-12: 缓存写入
                self._update_chapter_cache(tool_result, work_id_value, state)

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
                "look_ahead": tool_args.get("look_ahead", 0),
                "max_content_length": tool_args.get("max_content_length", 200)
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
                "look_ahead": tool_args.get("look_ahead", 0),
                "max_content_length": tool_args.get("max_content_length", 200),
            })

    async def _call_search_content(
        self, tool_args: Dict[str, Any], state: "AgentState", last_user_message: str
    ) -> str:
        """调用搜索内容工具"""
        work_id_value = state.get("work_id")
        if not work_id_value:
            logger.warning(f"[ToolDispatcher] ⚠️ search_content 缺少必需参数 work_id")
            return json.dumps({
                "error": "missing_work_id",
                "message": "需要提供作品ID才能搜索内容",
                "user_prompt": "请先告诉我您要搜索哪部作品的内容？"
            }, ensure_ascii=False)

        try:
            result = await registry.call_tool("search_content", {
                "work_id": work_id_value,
                "query": tool_args.get("query", last_user_message),
                "top_k": tool_args.get("top_k", 10),
                "chapter_id": state.get("chapter_id", ""),
                "look_ahead": tool_args.get("look_ahead", 0),
            })

            if isinstance(result, dict) and result.get("success"):
                tool_result = result.get("data", {}).get("results", "")
                logger.info(f"[StandardTool] search_content 执行成功")
                return tool_result
            else:
                error_msg = result.get("message", "执行失败") if isinstance(result, dict) else "未知错误"
                logger.error(f"[StandardTool] search_content 执行失败: {error_msg}")
                return json.dumps({"error": "tool_failed", "message": error_msg}, ensure_ascii=False)

        except Exception as e:
            logger.warning(f"[StandardTool] search_content 调用失败，降级到 @tool: {e}")
            return await search_content.ainvoke({
                "work_id": work_id_value,
                "query": tool_args.get("query", last_user_message),
                "top_k": tool_args.get("top_k", 10),
                "chapter_id": state.get("chapter_id", ""),
                "look_ahead": tool_args.get("look_ahead", 0),
            })

    async def _call_smart_rewrite(
        self, tool_args: Dict[str, Any], state: "AgentState"
    ) -> str:
        """调用智能改写工具"""
        # P2修复：多层兜底逻辑，避免参数为空
        text_to_rewrite = (
            tool_args.get("text_to_rewrite") or
            tool_args.get("content", "") or
            state.get("context", {}).get("selected_text", "")  # 兜底：从 state 获取选中文本
        )

        # chapter_content 兜底：使用 text_to_rewrite
        chapter_content = tool_args.get("chapter_content", "") or text_to_rewrite

        # user_requirement 兜底：从用户消息中提取
        user_requirement = tool_args.get("user_requirement", "") or state.get("last_user_message", "")

        # 诊断日志：帮助定位参数问题
        logger.info(f"[ToolDispatcher] smart_rewrite 参数检查: "
                    f"chapter_id={tool_args.get('chapter_id', '(空)')}, "
                    f"text_len={len(text_to_rewrite) if text_to_rewrite else 0}, "
                    f"chapter_content_len={len(chapter_content) if chapter_content else 0}, "
                    f"user_req_len={len(user_requirement) if user_requirement else 0}")

        # InlineAI 支持：优先使用 context 中的 selected_text
        context = state.get("context", {})
        selected_text = context.get("selected_text", "")
        locate_original_text = context.get("locate_original_text", "")
        selection_position = context.get("selection_position", None)

        # 如果有 selected_text，强制使用它
        if selected_text:
            logger.info(f"[ToolDispatcher] 📝 强制使用 InlineAI selected_text ({len(selected_text)} 字符)")
            text_to_rewrite = selected_text
        elif locate_original_text:
            logger.info(f"[ToolDispatcher] 🧭 使用 locate_original_text ({len(locate_original_text)} 字符)")
            text_to_rewrite = locate_original_text

        logger.info(f"[ToolDispatcher] 🚀 准备调用 smart_rewrite")

        try:
            result = await registry.call_tool("smart_rewrite", {
                "chapter_id": tool_args.get("chapter_id") or state.get("chapter_id") or "",
                "text_to_rewrite": text_to_rewrite,
                "chapter_content": chapter_content,
                "user_requirement": user_requirement,
                "user_id": state.get("user_id"),
                "source_locator": tool_args.get("source_locator")
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
                "chapter_id": tool_args.get("chapter_id") or state.get("chapter_id") or "",
                "text_to_rewrite": text_to_rewrite,
                "chapter_content": chapter_content,
                "user_requirement": user_requirement,
                "user_id": state.get("user_id"),
                "source_locator": tool_args.get("source_locator")
            })

        # 保存版本记忆
        self._save_version_memory(tool_result, state, selected_text, selection_position, text_to_rewrite, chapter_content)

        return tool_result

    async def _call_smart_continue(
        self, tool_args: Dict[str, Any], state: "AgentState"
    ) -> str:
        """调用智能续写工具"""
        logger.info(f"[ToolDispatcher] 🚀 准备调用 smart_continue")

        try:
            # 🔧 2026-01-09: 更新参数以匹配新的 smart_continue 签名
            result = await registry.call_tool("smart_continue", {
                "chapter_id": tool_args.get("chapter_id") or state.get("chapter_id") or "",
                "chapter_content": tool_args.get("chapter_content"),
                "user_requirement": tool_args.get("user_requirement", ""),
                "word_count": tool_args.get("word_count", 500),
                "user_id": state.get("user_id"),
                "source_locator": tool_args.get("source_locator")
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
                "chapter_id": tool_args.get("chapter_id") or state.get("chapter_id") or "",
                "chapter_content": tool_args.get("chapter_content"),
                "user_requirement": tool_args.get("user_requirement", ""),
                "word_count": tool_args.get("word_count", 500),
                "user_id": state.get("user_id"),
                "source_locator": tool_args.get("source_locator")
            })

        # 🔧 2026-01-09: CREATIVE 工具不再添加 editor_action，不触发 HITL 确认
        return tool_result

    async def _call_smart_insert(
        self, tool_args: Dict[str, Any], state: "AgentState"
    ) -> str:
        """调用智能插入工具"""
        logger.info(f"[ToolDispatcher] 🚀 准备调用 smart_insert")

        try:
            # 🔧 2026-01-09: 更新参数以匹配新的 smart_insert 签名
            result = await registry.call_tool("smart_insert", {
                "chapter_id": tool_args.get("chapter_id") or state.get("chapter_id") or "",
                "user_intent": tool_args.get("user_intent") or tool_args.get("position", "插入内容"),
                "chapter_content": tool_args.get("chapter_content"),
                "insert_context": tool_args.get("insert_context"),
                "word_count": tool_args.get("word_count", 200),
                "user_id": state.get("user_id"),
                "source_locator": tool_args.get("source_locator")
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
                "chapter_id": tool_args.get("chapter_id") or state.get("chapter_id") or "",
                "user_intent": tool_args.get("user_intent") or tool_args.get("position", "插入内容"),
                "chapter_content": tool_args.get("chapter_content"),
                "insert_context": tool_args.get("insert_context"),
                "word_count": tool_args.get("word_count", 200),
                "user_id": state.get("user_id"),
                "source_locator": tool_args.get("source_locator")
            })

        # 🔧 2026-01-09: CREATIVE 工具不再添加 editor_action，不触发 HITL 确认
        return tool_result

    async def _call_apply_chapter_edit(
        self, tool_args: Dict[str, Any], state: "AgentState"
    ) -> str:
        """调用应用章节编辑工具"""
        logger.info(f"[ToolDispatcher] 🚀 准备调用 apply_chapter_edit")
        context = state.get("context", {}) if isinstance(state.get("context"), dict) else {}
        node_id = tool_args.get("node_id") or context.get("locate_node_id")
        paragraph_index = tool_args.get("paragraph_index") or context.get("locate_paragraph_index")
        before_anchor = tool_args.get("before_anchor") or context.get("locate_before_anchor")
        after_anchor = tool_args.get("after_anchor") or context.get("locate_after_anchor")
        original_text = tool_args.get("original_text") or context.get("locate_original_text")

        try:
            result = await registry.call_tool("apply_chapter_edit", {
                "chapter_id": tool_args.get("chapter_id") or state.get("chapter_id") or "",
                "content": tool_args.get("content", ""),
                "operation": tool_args.get("operation", "replace"),
                "position": tool_args.get("position"),
                "before_anchor": before_anchor,
                "after_anchor": after_anchor,
                "original_text": original_text,
                "node_id": node_id,
                "paragraph_index": paragraph_index,
                "user_id": state.get("user_id"),
                "description": tool_args.get("description"),
                "conversation_id": tool_args.get("conversation_id") or state.get("conversation_id"),
                "work_id": tool_args.get("work_id") or state.get("work_id")
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
                "chapter_id": tool_args.get("chapter_id") or state.get("chapter_id") or "",
                "content": tool_args.get("content", ""),
                "operation": tool_args.get("operation", "replace"),
                "position": tool_args.get("position"),
                "before_anchor": before_anchor,
                "after_anchor": after_anchor,
                "original_text": original_text,
                "node_id": node_id,
                "paragraph_index": paragraph_index,
                "user_id": state.get("user_id"),
                "description": tool_args.get("description"),
                "conversation_id": tool_args.get("conversation_id") or state.get("conversation_id"),
                "work_id": tool_args.get("work_id") or state.get("work_id")
            })

        return tool_result

    async def _call_delete_chapter(
        self, tool_args: Dict[str, Any], state: "AgentState"
    ) -> str:
        """调用删除章节工具（2026-01-09 新增）"""
        logger.info(f"[ToolDispatcher] 🚀 准备调用 delete_chapter")

        from app.services.agent.tools.chapter_tools import delete_chapter
        return await delete_chapter.ainvoke(tool_args)

    async def _call_update_chapter_content(
        self, tool_args: Dict[str, Any], state: "AgentState"
    ) -> str:
        """调用更新章节内容工具（2026-01-09 新增）"""
        logger.info(f"[ToolDispatcher] 🚀 准备调用 update_chapter_content")

        from app.services.agent.tools.chapter_tools import update_chapter_content
        return await update_chapter_content.ainvoke(tool_args)

    async def _call_operate_apply(
        self, tool_args: Dict[str, Any], state: "AgentState"
    ) -> str:
        """调用 operate_apply 统一操作工具（2026-01-23 新增）"""
        logger.info(f"[ToolDispatcher] 🚀 准备调用 operate_apply, operation={tool_args.get('operation')}")

        context = state.get("context", {}) if isinstance(state.get("context"), dict) else {}
        state_chapter_id = state.get("chapter_id")
        target_chapter_id = tool_args.get("chapter_id") or state_chapter_id
        same_chapter = True
        if target_chapter_id and state_chapter_id and target_chapter_id != state_chapter_id:
            same_chapter = False

        # 补充 state 中的参数
        if not tool_args.get("chapter_id") and state.get("chapter_id"):
            tool_args["chapter_id"] = state.get("chapter_id")
        if not tool_args.get("work_id") and state.get("work_id"):
            tool_args["work_id"] = state.get("work_id")
        if not tool_args.get("user_id") and state.get("user_id"):
            tool_args["user_id"] = state.get("user_id")
        if not tool_args.get("conversation_id") and state.get("conversation_id"):
            tool_args["conversation_id"] = state.get("conversation_id")
        if same_chapter:
            if tool_args.get("node_id") is None and context.get("locate_node_id"):
                tool_args["node_id"] = context.get("locate_node_id")
            if tool_args.get("paragraph_index") is None and context.get("locate_paragraph_index") is not None:
                tool_args["paragraph_index"] = context.get("locate_paragraph_index")
            if not tool_args.get("original_text") and context.get("locate_original_text"):
                tool_args["original_text"] = context.get("locate_original_text")
            if not tool_args.get("nodes_info") and context.get("nodes_info"):
                tool_args["nodes_info"] = context.get("nodes_info")

        from app.services.agent.tools.operate_tools import operate_apply
        return await operate_apply.ainvoke(tool_args)

    async def _call_generic_tool(
        self, tool_name: str, tool_args: Dict[str, Any], state: "AgentState"
    ) -> str:
        """使用统一接口调用其他工具"""
        logger.info(f"[ToolDispatcher] 使用统一接口调用工具: {tool_name}")
        try:
            call_state = state
            step_id = None
            if tool_name == "explore_content":
                if isinstance(state, dict):
                    call_state = dict(state)
                    step_id = state.get("step_id")
                else:
                    call_state = {}
                call_state["emit_explore_events"] = True
                stream_handler = getattr(self.agent, "stream_event_handler", None)
                if stream_handler:
                    call_state["stream_event_handler"] = stream_handler
                if isinstance(step_id, int):
                    call_state["step_id"] = step_id

            tool_result = await self.agent._call_tool_via_registry(
                tool_name=tool_name,
                tool_args=tool_args,
                state=call_state
            )
            logger.info(f"[ToolDispatcher] ✅ 统一接口调用成功: {tool_name}")
            if tool_name == "explore_content":
                return await self._handle_explore_content_result(tool_result, step_id)
            return tool_result
        except Exception as e:
            logger.error(f"[ToolDispatcher] 统一接口调用失败: {tool_name}, 错误: {e}")
            return json.dumps({
                "error": "tool_call_failed",
                "message": f"工具调用失败: {str(e)}",
                "user_prompt": "抱歉，我在处理您的请求时遇到了问题。能否换个方式描述？"
            }, ensure_ascii=False)

    async def _handle_explore_content_result(
        self,
        tool_result: Any,
        step_id: Optional[int] = None
    ) -> str:
        result_data = tool_result
        if isinstance(tool_result, str):
            try:
                result_data = json.loads(tool_result)
            except json.JSONDecodeError:
                return tool_result

        if not isinstance(result_data, dict):
            return tool_result if isinstance(tool_result, str) else str(tool_result)

        if not result_data.get("success"):
            return tool_result if isinstance(tool_result, str) else json.dumps(result_data, ensure_ascii=False)

        if result_data.get("frontend_display") and not result_data.get("events_emitted"):
            await self._emit_explore_events(result_data, step_id)

        explore_summary = result_data.get("explore_summary") or result_data.get("context_for_task", "")
        if explore_summary:
            return explore_summary

        return tool_result if isinstance(tool_result, str) else json.dumps(result_data, ensure_ascii=False)

    async def _emit_explore_events(
        self,
        result_data: Dict[str, Any],
        step_id: Optional[int] = None
    ) -> None:
        if not hasattr(self.agent, "stream_event_handler"):
            logger.warning("[ToolDispatcher] agent 没有 stream_event_handler，无法发射 explore 事件")
            return

        stream_handler = self.agent.stream_event_handler
        if not stream_handler:
            return

        frontend_display = result_data.get("frontend_display", {})
        if not frontend_display:
            logger.warning("[ToolDispatcher] explore_content 结果缺少 frontend_display")
            return

        from app.services.agent.stream.flow_events import FlowEventBuilder

        rounds = frontend_display.get("rounds", [])
        if not rounds:
            logger.warning("[ToolDispatcher] explore_content frontend_display.rounds 为空，跳过事件发射")
            return

        emit_step_id = step_id if isinstance(step_id, int) else 1

        for round_data in rounds:
            try:
                event = FlowEventBuilder.explore_round(
                    step_id=emit_step_id,
                    round_idx=round_data.get("round_idx", 1),
                    title=round_data.get("title", "探索"),
                    tool_calls=round_data.get("tool_calls", []),
                    hit_count=round_data.get("hit_count", 0),
                    missing_items=round_data.get("missing_items", []),
                    status_text=round_data.get("status_text", ""),
                    evidences=round_data.get("evidences", []),
                    review_status=round_data.get("review_status", ""),
                    reason=round_data.get("reason", "")
                )
                await stream_handler.emit_flow_event(event)
            except Exception as e:
                logger.error(f"[ToolDispatcher] 发射 explore_round 事件失败: {e}")

        ai_analysis = frontend_display.get("ai_analysis", {})
        try:
            event = FlowEventBuilder.explore_summary(
                step_id=emit_step_id,
                total_rounds=len(rounds),
                summary=ai_analysis.get("summary", result_data.get("analysis", "")),
                next_action=ai_analysis.get("next_action", ""),
                next_tool=ai_analysis.get("next_tool", ""),
                stats=ai_analysis.get("stats", result_data.get("stats", {})),
                sufficient=ai_analysis.get("sufficient"),
                coverage=ai_analysis.get("coverage")
            )
            await stream_handler.emit_flow_event(event)
        except Exception as e:
            logger.error(f"[ToolDispatcher] 发射 explore_summary 事件失败: {e}")

    # ==================== 辅助方法 ====================

    def _save_version_memory(
        self,
        tool_result: str,
        state: "AgentState",
        selected_text: str,
        selection_position: Optional[Dict],
        text_to_rewrite: str,
        chapter_content: str = "",  # 新增：章节内容用于生成锚点
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
                    editor_action = {
                        "type": "modify",
                        "original_text": text_to_rewrite,
                        "position": selection_position,
                        "requires_confirmation": True
                    }

                    # 🆕 生成锚点用于位置失效时重新定位
                    if chapter_content and selection_position:
                        pos_from = selection_position.get("from", 0)
                        pos_to = selection_position.get("to", 0)
                        # 提取修改点前30-50字作为前锚点
                        anchor_start = max(0, pos_from - 50)
                        before_anchor = chapter_content[anchor_start:pos_from]
                        # 提取修改点后30-50字作为后锚点
                        anchor_end = min(len(chapter_content), pos_to + 50)
                        after_anchor = chapter_content[pos_to:anchor_end]

                        if before_anchor:
                            editor_action["before_anchor"] = before_anchor
                        if after_anchor:
                            editor_action["after_anchor"] = after_anchor
                        logger.info(f"[ToolDispatcher] 🔗 添加锚点: before={len(before_anchor)}字, after={len(after_anchor)}字")

                    result_obj["editor_action"] = editor_action
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

    # ==================== 章节缓存方法（2026-01-12 新增）====================

    def _update_chapter_cache(
        self,
        tool_result: str,
        work_id: str,
        state: "AgentState"
    ) -> None:
        """更新章节缓存

        Args:
            tool_result: 工具返回结果（JSON 字符串）
            work_id: 作品ID
            state: Agent 状态
        """
        try:
            data = json.loads(tool_result) if isinstance(tool_result, str) else tool_result

            # 单章节
            if isinstance(data, dict) and "chapter_id" in data:
                ChapterCache.set(state, data, work_id)
            # 多章节
            elif isinstance(data, dict) and "chapters" in data:
                ChapterCache.set_batch(state, data["chapters"], work_id)
        except Exception as e:
            logger.warning(f"[ToolDispatcher] 缓存写入失败: {e}")
