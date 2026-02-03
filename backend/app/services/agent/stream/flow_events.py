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
- revision: 修订请求 (v7.0)
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
    def step_start(step_id: int, title: str, description: Optional[str] = None) -> dict:
        """构建步骤开始事件"""
        event = {
            "type": "step_start",
            "step_id": step_id,
            "title": title,
            "status": "running",
            "timestamp": get_utc_now().isoformat()
        }
        if description:
            event["description"] = description
        return event

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
        intro_highlight: Optional[str] = None,
        is_applicable: bool = False
    ) -> dict:
        """构建输出就绪事件

        Args:
            title: 输出标题 (如 "第五章：外门初修")
            content: 输出内容 (支持Markdown)
            intro: 介绍文字 (如 "第五章已续写完成！本章主要讲述{highlight}的经历")
            intro_highlight: 高亮文字 (如 "林逸开始外门修炼")
            is_applicable: 是否可应用到编辑器（显示"应用到章节"按钮）
        """
        return {
            "type": "output_ready",
            "title": title,
            "content": content,
            "intro": intro,
            "intro_highlight": intro_highlight,
            "is_applicable": is_applicable,
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

    @staticmethod
    def summarization_start(
        task_classification: Dict[str, List[Dict[str, Any]]],
        context_stats: Dict[str, Any],
        reason: str = ""
    ) -> dict:
        """构建AI整合分析开始事件

        Args:
            task_classification: 任务分类 {
                "input_tasks": [{"tool": "...", "description": "..."}],
                "output_tasks": [...],
                "display_tasks": [...]
            }
            context_stats: 上下文统计 {
                "original_length": 6048,
                "compressed_length": 5643,
                "mode": "流式生成"
            }
            reason: AI 生成的简短理由（可为空）
        """
        return {
            "type": "summarization_start",
            "task_classification": task_classification,
            "context_stats": context_stats,
            "reason": reason,
            "status": "running",
            "timestamp": get_utc_now().isoformat()
        }

    @staticmethod
    def summarization_complete() -> dict:
        """构建AI整合分析完成事件"""
        return {
            "type": "summarization_complete",
            "status": "done",
            "timestamp": get_utc_now().isoformat()
        }

    @staticmethod
    def revision(
        revision_type: str,
        request_id: Optional[str] = None,
        chapter_id: Optional[str] = None,
        chapter_title: Optional[str] = None,
        content: Optional[str] = None,
        content_preview: Optional[str] = None,
        original_content: Optional[str] = None,
        position: Optional[Dict[str, Any]] = None,
        operation: Optional[str] = None,
        editor_action: Optional[Dict[str, Any]] = None,
        old_title: Optional[str] = None,
        new_title: Optional[str] = None,
        versions: Optional[List[Dict[str, str]]] = None
    ) -> dict:
        """构建修订请求事件 (v7.5 非阻塞式修订)

        Args:
            revision_type: 修订类型 ("append" | "replace" | "insert" | "create" | "rename")
            request_id: 对应的审批请求ID（用于前端关联）
            chapter_id: 章节ID
            chapter_title: 章节标题
            content: 完整内容
            content_preview: 内容预览（前50字）
            original_content: 原内容（replace类型需要）
            position: 位置信息 {"from": int, "to": int}
            operation: 操作类型 ("append" | "replace" | "insert")
            editor_action: 编辑器操作信息 {"type": str, "position": dict, ...}
            old_title: 原标题（rename 类型）
            new_title: 新标题（rename 类型）
            versions: 改写版本列表（replace 类型）
        """
        data = {
            "revisionType": revision_type,
            "status": "pending"
        }
        if request_id:
            data["requestId"] = request_id
        if chapter_id:
            data["chapterId"] = chapter_id
        if chapter_title:
            data["chapterTitle"] = chapter_title
        if content:
            data["content"] = content
        if content_preview:
            data["contentPreview"] = content_preview
        if original_content:
            data["originalContent"] = original_content
        if position:
            data["position"] = position
        if operation:
            data["operation"] = operation
        if editor_action:
            data["editorAction"] = editor_action
        if old_title:
            data["oldTitle"] = old_title
        if new_title:
            data["newTitle"] = new_title
        if versions:
            data["versions"] = versions

        return {
            "type": "revision",
            "data": data,
            "timestamp": get_utc_now().isoformat()
        }


    @staticmethod
    def explore_round(
        step_id: int,
        round_idx: int,
        title: str,
        tool_calls: List[Dict[str, Any]],
        hit_count: int,
        missing_items: List[str],
        status_text: str,
        evidences: List[Dict[str, Any]],
        review_status: str,
        reason: str = "",  # AI 生成的决策理由（完整）
        status: str = "done"
    ) -> dict:
        """构建 Explore 轮次事件

        Args:
            step_id: 步骤ID
            round_idx: 轮次索引（从1开始）
            title: 轮次标题（固定简短标题，如"初次检索与定位"）
            tool_calls: 工具调用列表 [{"type": "Search", "value": "...", "highlight": "..."}]
            hit_count: 命中条数
            missing_items: 缺失项列表（黄色警告）
            status_text: 状态文本（灰色，如"补漏完成"/"覆盖度达标"）
            evidences: 证据片段列表 [{"chapter": 5, "paragraph": 7, "text": "..."}]
            review_status: 审查状态（"覆盖不足"/"补齐要点"/"通过"）
            reason: AI 生成的决策理由（完整，单独显示）
            status: 轮次状态（"running"/"done"）
        """
        return {
            "type": "explore_round",
            "step_id": step_id,
            "round_idx": round_idx,
            "title": title,
            "reason": reason,  # AI 决策理由（完整）
            "tool_calls": tool_calls,
            "hit_count": hit_count,
            "missing_items": missing_items,
            "status_text": status_text,
            "evidences": evidences,
            "review_status": review_status,
            "status": status,
            "timestamp": get_utc_now().isoformat()
        }

    @staticmethod
    def explore_summary(
        step_id: int,
        total_rounds: int,
        summary: str,
        next_action: str,
        next_tool: Optional[str],
        stats: Dict[str, Any],
        sufficient: Optional[bool] = None,
        coverage: Optional[str] = None
    ) -> dict:
        """构建 Explore AI 分析与规划事件

        Args:
            step_id: 步骤ID
            total_rounds: 总轮次数
            summary: 探索总结
            next_action: 下一步行动描述
            next_tool: 下一步要调用的工具名（如 "smart_continue"）
            stats: 统计信息 {"worldview": 5, "chapters": "1-4", "evidences": 13, "coverage": "95%"}
            sufficient: 是否已判定信息充足
            coverage: 覆盖度说明
        """
        event = {
            "type": "explore_summary",
            "step_id": step_id,
            "total_rounds": total_rounds,
            "summary": summary,
            "next_tool": next_tool,
            "stats": stats,
            "timestamp": get_utc_now().isoformat()
        }
        if next_action:
            event["next_action"] = next_action
        if sufficient is not None:
            event["sufficient"] = sufficient
        if coverage is not None:
            event["coverage"] = coverage
        return event


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
    "search_content": "Search",
    "search_memory_tool": "Search",
    "search_knowledge_advanced": "Search",
    # 写作类
    "smart_continue": "PenTool",
    "expand_text": "Maximize2",
    # 编辑类
    "smart_rewrite": "Edit3",
    "smart_insert": "Plus",
    # Explore 相关
    "explore_content": "Scan",
    "read_paragraph": "FileText",
    # 默认
    "_default": "Wrench"
}

# Explore 工具标签类型图标映射
EXPLORE_TAG_ICONS = {
    "Search": "search",
    "Locate": "crosshair",
    "ReadRaw": "file-text",
    "Review": "check-circle",
}


def get_tool_icon(tool_name: str) -> str:
    """获取工具对应的图标名"""
    return TOOL_ICONS.get(tool_name, TOOL_ICONS["_default"])
