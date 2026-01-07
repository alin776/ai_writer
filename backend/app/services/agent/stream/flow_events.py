# -*- coding: utf-8 -*-
"""
执行轨迹流式事件定义

定义前端ExecutionFlow组件所需的SSE事件类型：
- agent_header: Agent头部
- step_start: 步骤开始
- knowledge_loaded: 知识加载完成
- step_complete: 步骤完成
- output_ready: 输出就绪
- completion: 任务完成
"""

from typing import List, Optional, Dict, Any
from dataclasses import dataclass, asdict
from app.utils.datetime_utils import get_utc_now


@dataclass
class KnowledgeItem:
    """知识项"""
    name: str
    tag: Optional[str] = None
    similarity: Optional[float] = None


@dataclass
class KnowledgeData:
    """知识调取数据"""
    title: str
    icon: str  # "BookOpen" | "FileText" | "Search"
    items: List[KnowledgeItem]


@dataclass
class ToolCallData:
    """工具调用数据"""
    icon: str
    name: str


class FlowEventBuilder:
    """执行轨迹事件构建器"""

    @staticmethod
    def agent_header(name: str = "文枢AI", badge: str = "") -> dict:
        """构建Agent头部事件"""
        return {
            "type": "agent_header",
            "data": {
                "name": name,
                "badge": badge
            },
            "timestamp": get_utc_now().isoformat()
        }

    @staticmethod
    def text(content: str) -> dict:
        """构建文本消息事件"""
        return {
            "type": "text",
            "data": {
                "content": content
            },
            "timestamp": get_utc_now().isoformat()
        }

    @staticmethod
    def step_start(step_id: int, title: str) -> dict:
        """构建步骤开始事件"""
        return {
            "type": "step_start",
            "step_id": step_id,
            "title": title,
            "status": "running",
            "timestamp": get_utc_now().isoformat()
        }

    @staticmethod
    def knowledge_loaded(
        step_id: int,
        knowledge_type: str,
        title: str,
        icon: str,
        items: List[Dict[str, Any]]
    ) -> dict:
        """构建知识加载完成事件

        Args:
            step_id: 步骤ID
            knowledge_type: 知识类型 ("worldview" | "chapters" | "search")
            title: 显示标题 (如 "世界观已加载(5)")
            icon: 图标名 ("BookOpen" | "FileText" | "Search")
            items: 知识项列表 [{"name": "...", "tag": "...", "similarity": 0.89}]
        """
        return {
            "type": "knowledge_loaded",
            "step_id": step_id,
            "knowledge_type": knowledge_type,
            "title": title,
            "icon": icon,
            "items": items,
            "timestamp": get_utc_now().isoformat()
        }

    @staticmethod
    def step_complete(
        step_id: int,
        description: str,
        tool_call: Optional[Dict[str, str]] = None
    ) -> dict:
        """构建步骤完成事件

        Args:
            step_id: 步骤ID
            description: 步骤描述
            tool_call: 工具调用信息 {"icon": "Wrench", "name": "tool_name"}
        """
        return {
            "type": "step_complete",
            "step_id": step_id,
            "description": description,
            "tool_call": tool_call,
            "status": "done",
            "timestamp": get_utc_now().isoformat()
        }

    @staticmethod
    def output_ready(
        title: str,
        content: str,
        intro: Optional[str] = None,
        intro_highlight: Optional[str] = None
    ) -> dict:
        """构建输出就绪事件

        Args:
            title: 输出标题 (如 "第五章：外门初修")
            content: 输出内容 (支持HTML)
            intro: 介绍文字 (如 "第五章已续写完成！本章主要讲述{highlight}的经历")
            intro_highlight: 高亮文字 (如 "林逸开始外门修炼")
        """
        return {
            "type": "output_ready",
            "title": title,
            "content": content,
            "intro": intro,
            "intro_highlight": intro_highlight,
            "timestamp": get_utc_now().isoformat()
        }

    @staticmethod
    def completion(text: str = "任务已完成") -> dict:
        """构建完成状态事件"""
        return {
            "type": "completion",
            "data": {
                "text": text
            },
            "timestamp": get_utc_now().isoformat()
        }


# 工具图标映射
TOOL_ICONS = {
    # 世界观/知识类
    "get_worldview_summary": "BookOpen",
    "get_worldview_tool": "BookOpen",
    # 章节类
    "get_chapter_by_order_tool": "FileText",
    "read_chapter_tool": "FileText",
    "get_context_tool": "BookOpen",
    # 检索类
    "search_analysis_fragments_tool": "Search",
    "search_memory_tool": "Search",
    "search_knowledge_advanced": "Search",
    # 写作类
    "continue_writing_tool": "PenTool",
    "smart_continue": "ArrowRight",
    "expand_text": "Maximize2",
    # 编辑类
    "smart_rewrite": "Edit3",
    "smart_insert": "Plus",
    # 默认
    "_default": "Wrench"
}


def get_tool_icon(tool_name: str) -> str:
    """获取工具对应的图标名"""
    return TOOL_ICONS.get(tool_name, TOOL_ICONS["_default"])
