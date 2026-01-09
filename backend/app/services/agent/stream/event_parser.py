# -*- coding: utf-8 -*-
"""
事件解析器

从 langgraph_agent.py 提取的流式事件解析逻辑：
- 节点事件解析
- 工具调用提取
- 内容提取
"""

from typing import Dict, Any, Optional, List
import json
import re
import logging

from langchain_core.messages import AIMessage, ToolMessage

from app.utils.datetime_utils import get_utc_now

logger = logging.getLogger(__name__)


class EventParser:
    """事件解析器

    负责将 LangGraph 节点事件转换为用户友好的进度信息
    """

    # 节点映射表
    NODE_MAPPING = {
        "intent_classifier": {
            "step": "intent_analysis",
            "description": "正在分析您的需求..."
        },
        "writing_agent": {
            "step": "thinking",
            "description": "正在思考如何帮助您..."
        },
        "planning_agent": {
            "step": "thinking",
            "description": "正在规划方案..."
        },
        "analysis_agent": {
            "step": "thinking",
            "description": "正在分析内容..."
        },
        "stuck_agent": {
            "step": "thinking",
            "description": "正在寻找解决方案..."
        },
        "general_chat": {
            "step": "thinking",
            "description": "正在思考回复..."
        },
        "tools": {
            "step": "tool_execution",
            "description": "正在调用工具..."
        }
    }

    # 工具显示配置（Lucide 图标名 + 标题）
    TOOL_DISPLAY_CONFIG = {
        # ========== 章节读取类 ==========
        "get_chapter_by_order_tool": {"icon": "FileText", "title": "读取章节"},
        "read_chapter_tool": {"icon": "FileText", "title": "读取章节"},
        "get_context_tool": {"icon": "BookOpen", "title": "获取上下文"},
        # ========== 检索类 ==========
        "search_analysis_fragments_tool": {"icon": "Search", "title": "检索设定"},
        "search_memory_tool": {"icon": "Search", "title": "搜索记忆"},
        "search_knowledge_advanced": {"icon": "Search", "title": "高级知识检索"},
        # ========== 写作类 ==========
        "smart_continue": {"icon": "PenTool", "title": "智能续写"},
        "expand_text": {"icon": "Maximize2", "title": "扩写内容"},
        # ========== 编辑类 ==========
        "smart_rewrite": {"icon": "Edit3", "title": "智能改写"},
        "smart_insert": {"icon": "Plus", "title": "智能插入"},
        "apply_chapter_edit": {"icon": "Check", "title": "应用修改"},
        "deai_rewrite": {"icon": "RefreshCw", "title": "去AI改写"},
        # ========== 分析类 ==========
        "analyze_text_tool": {"icon": "BarChart2", "title": "分析文本"},
        "analyze_content": {"icon": "FileSearch", "title": "内容分析"},
        "book_analysis": {"icon": "BarChart2", "title": "书籍分析"},
        "novel_review": {"icon": "MessageSquare", "title": "小说评审"},
        "ai_evaluation": {"icon": "Sparkles", "title": "AI评估"},
        "evaluate_quality": {"icon": "Star", "title": "质量评估"},
        # ========== 管理类 ==========
        "add_todo_tool": {"icon": "ListTodo", "title": "添加待办"},
        "get_work_details_tool": {"icon": "BookOpen", "title": "获取作品信息"},
        "update_work_metadata_tool": {"icon": "Save", "title": "更新元数据"},
        # ========== 默认 ==========
        "_default": {"icon": "Wrench", "title": "工具调用"}
    }

    # 保留旧映射供兼容
    TOOL_DISPLAY_NAMES = {
        "get_chapter_by_order_tool": "读取章节",
        "smart_continue": "智能续写",
        "search_analysis_fragments_tool": "检索设定",
        "search_memory_tool": "搜索记忆",
        "add_todo_tool": "添加待办",
        "get_work_details_tool": "获取作品信息",
        "update_work_metadata_tool": "更新元数据",
        "analyze_text_tool": "分析文本"
    }

    def __init__(self, cached_tool_calls: Optional[Dict] = None):
        """
        Args:
            cached_tool_calls: 缓存的工具调用参数
        """
        self._cached_tool_calls = cached_tool_calls or {}

    def format_tool_display(self, tool_call: dict) -> dict:
        """格式化工具调用为前端显示格式

        Args:
            tool_call: 包含 name 和 args 的工具调用信息

        Returns:
            前端可直接渲染的工具显示事件
        """
        tool_name = tool_call.get("name", "unknown")
        args = tool_call.get("args", {})

        config = self.TOOL_DISPLAY_CONFIG.get(
            tool_name,
            self.TOOL_DISPLAY_CONFIG["_default"]
        )

        description = self._build_tool_description(tool_name, args)

        return {
            "type": "tool",
            "data": {
                "tool_name": tool_name,
                "icon": config["icon"],
                "title": config["title"],
                "description": description,
                "status": "running"
            }
        }

    def _build_tool_description(self, tool_name: str, args: dict) -> str:
        """根据工具类型构建描述"""
        # 章节读取类
        if tool_name in ["read_chapter_tool", "get_chapter_by_order_tool"]:
            chapter = args.get("chapter_order") or args.get("chapter_id", "")
            if chapter:
                return f"第{chapter}章"
            return ""
        # 检索类
        elif tool_name == "search_analysis_fragments_tool":
            query = args.get("query", "")
            return query[:30] if query else "检索中..."
        elif tool_name == "search_memory_tool":
            query = args.get("query", "")
            return query[:30] if query else "搜索中..."
        elif tool_name == "search_knowledge_advanced":
            query = args.get("query", "")
            return query[:30] if query else "检索中..."
        # 写作类
        elif tool_name == "smart_continue":
            words = args.get("target_words") or args.get("word_count", 500)
            return f"目标{words}字"
        elif tool_name == "expand_text":
            return "扩写中..."
        # 编辑类
        elif tool_name == "smart_rewrite":
            style = args.get("style", "润色优化")
            return style[:20]
        elif tool_name == "smart_insert":
            return "插入中..."
        elif tool_name == "apply_chapter_edit":
            return "保存中..."
        elif tool_name == "deai_rewrite":
            return "改写中..."
        # 分析类
        elif tool_name == "analyze_text_tool":
            focus = args.get("focus", "综合分析")
            return focus
        elif tool_name in ["analyze_content", "book_analysis"]:
            return "分析中..."
        elif tool_name == "novel_review":
            return "评审中..."
        elif tool_name == "ai_evaluation":
            return "评估中..."
        elif tool_name == "evaluate_quality":
            return "评估中..."
        # 管理类
        elif tool_name == "get_context_tool":
            return "加载上下文..."
        elif tool_name == "add_todo_tool":
            return "添加中..."
        elif tool_name == "get_work_details_tool":
            return "获取中..."
        elif tool_name == "update_work_metadata_tool":
            return "更新中..."
        return ""


    def parse_node_event(
        self,
        node_name: str,
        node_data: dict,
        progress_tracker=None
    ) -> Optional[dict]:
        """将LangGraph节点事件转换为用户友好的进度信息"""

        mapping = self.NODE_MAPPING.get(node_name)
        if not mapping:
            return None

        # 复制 mapping 以避免修改原始数据
        mapping = dict(mapping)
        details = {}

        if node_name == "intent_classifier":
            intent = node_data.get("intent")
            if intent:
                details["intent"] = intent
                intent_names = {
                    "writing": "写作任务",
                    "planning": "规划任务",
                    "analysis": "分析任务",
                    "stuck": "卡文求助",
                    "general": "一般对话"
                }
                intent_display = intent_names.get(intent, intent)
                mapping["description"] = f"识别为：{intent_display}"

        elif node_name == "tools":
            tool_info = self._extract_tool_info_from_messages(node_data.get("messages", []))

            if tool_info:
                tool_name = tool_info["name"]
                tool_args = tool_info["args"]

                # 优先使用缓存的参数
                if tool_name in self._cached_tool_calls:
                    tool_args = self._cached_tool_calls[tool_name]
                    del self._cached_tool_calls[tool_name]

                details["tools"] = [tool_name]
                details["tool_args"] = tool_args
                mapping["description"] = self.generate_tool_description(tool_name, tool_args)

        # 从 ProgressTracker 获取进度信息
        progress_data = {}
        if progress_tracker:
            try:
                progress_event = progress_tracker.get_progress_event()
                progress_data = {
                    "progress": progress_event.get("progress"),
                    "eta": progress_event.get("eta"),
                    "eta_display": progress_event.get("eta_display"),
                    "eta_confidence": progress_event.get("eta_confidence"),
                    "current_step": progress_event.get("current_step"),
                    "total_steps": progress_event.get("total_steps"),
                    "step_description": progress_event.get("step_description"),
                    "elapsed": progress_event.get("elapsed")
                }
            except Exception as e:
                logger.error(f"[ProgressTracker] 获取进度失败: {e}")
                progress_data = {}

        return {
            "type": "progress",
            "step": mapping["step"],
            "description": mapping["description"],
            "node": node_name,
            "details": details,
            "timestamp": get_utc_now().isoformat(),
            **progress_data
        }

    def _extract_tool_info_from_messages(self, messages: List) -> Optional[Dict]:
        """从消息列表中提取工具信息"""
        # 寻找 AIMessage 中的 tool_calls（倒序查找最新的）
        for msg in reversed(messages):
            if isinstance(msg, AIMessage) and hasattr(msg, "tool_calls") and msg.tool_calls:
                tool_call = msg.tool_calls[0]
                return {
                    "name": tool_call.get("name"),
                    "args": tool_call.get("args", {})
                }

        # 向后兼容：从 ToolMessage 提取
        for msg in messages:
            if hasattr(msg, "name"):
                return {
                    "name": msg.name,
                    "args": {}
                }

        return None

    def extract_tool_calls(self, node_data: dict) -> list:
        """提取工具调用信息"""
        tool_calls = []
        messages = node_data.get("messages", [])

        for msg in messages:
            if isinstance(msg, ToolMessage) and hasattr(msg, "name"):
                tool_name = msg.name
                tool_args = {}
                tool_calls.append((tool_name, tool_args))

        return tool_calls

    def generate_tool_description(self, tool_name: str, tool_args: dict) -> str:
        """根据工具名称和参数生成具体描述"""

        if tool_name == "get_chapter_by_order_tool":
            chapter_order = tool_args.get("chapter_order", "?")
            return f"📚 正在读取第{chapter_order}章..."

        elif tool_name == "smart_continue":
            target_words = tool_args.get("target_words")
            if target_words:
                return f"✍️ 正在续写内容（目标{target_words}字）..."
            return "✍️ 正在续写内容..."

        elif tool_name == "search_analysis_fragments_tool":
            query = tool_args.get("query", "")
            if query and len(query) <= 20:
                return f"🔍 正在检索「{query}」相关设定..."
            return "🔍 正在检索设定..."

        elif tool_name == "search_memory_tool":
            query = tool_args.get("query", "")
            if query and len(query) <= 20:
                return f"💭 正在搜索「{query}」相关记忆..."
            return "💭 正在搜索记忆..."

        elif tool_name == "analyze_text_tool":
            return "🔍 正在分析文本..."

        elif tool_name == "add_todo_tool":
            return "📝 正在添加待办事项..."

        elif tool_name == "get_work_details_tool":
            return "📖 正在获取作品信息..."

        elif tool_name == "update_work_metadata_tool":
            return "💾 正在更新作品元数据..."

        # 默认描述
        display_name = self.TOOL_DISPLAY_NAMES.get(tool_name, tool_name)
        return f"正在{display_name}..."

    def extract_content(self, node_name: str, node_data: dict) -> Optional[str]:
        """提取生成的内容"""
        if not node_name.endswith("_agent") and node_name != "general_chat":
            return None

        messages = node_data.get("messages", [])
        if not messages:
            return None

        last_message = messages[-1]
        if isinstance(last_message, AIMessage) and last_message.content:
            if not hasattr(last_message, "tool_calls") or not last_message.tool_calls:
                return last_message.content

        return None

    @staticmethod
    def extract_json_from_text(text: str) -> Optional[dict]:
        """从文本中提取JSON对象（增强版，支持更多容错）"""
        text = text.strip()
        if not text:
            return None

        # 方法1: 直接解析
        try:
            return json.loads(text)
        except json.JSONDecodeError:
            pass

        # 方法2: 从 ```json 块提取
        if "```json" in text:
            match = re.search(r'```json\s*\n(.*?)```', text, re.DOTALL)
            if match:
                try:
                    return json.loads(match.group(1).strip())
                except json.JSONDecodeError:
                    pass

        # 方法3: 从 ``` 块提取
        if "```" in text:
            match = re.search(r'```\s*\n(.*?)```', text, re.DOTALL)
            if match:
                try:
                    return json.loads(match.group(1).strip())
                except json.JSONDecodeError:
                    pass

        # 方法4: 查找第一个 { 到最后一个 } 之间的内容（更宽松的匹配）
        first_brace = text.find('{')
        last_brace = text.rfind('}')
        if first_brace != -1 and last_brace > first_brace:
            json_candidate = text[first_brace:last_brace + 1]
            try:
                return json.loads(json_candidate)
            except json.JSONDecodeError:
                # 方法5: 尝试修复常见JSON错误
                fixed = EventParser._fix_common_json_errors(json_candidate)
                if fixed:
                    try:
                        return json.loads(fixed)
                    except json.JSONDecodeError:
                        pass

        return None

    @staticmethod
    def _fix_common_json_errors(text: str) -> Optional[str]:
        """修复常见的JSON格式错误"""
        if not text:
            return None

        # 移除尾随逗号（如 [1,2,] 或 {"a":1,}）
        text = re.sub(r',\s*([}\]])', r'\1', text)

        # 修复字符串中未转义的实际换行符
        # 使用更安全的方式：逐字符处理
        result = []
        in_string = False
        i = 0
        while i < len(text):
            char = text[i]
            if char == '"' and (i == 0 or text[i-1] != '\\'):
                in_string = not in_string
                result.append(char)
            elif in_string and char == '\n':
                result.append('\\n')
            elif in_string and char == '\r':
                result.append('\\r')
            else:
                result.append(char)
            i += 1

        return ''.join(result)
