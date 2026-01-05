# -*- coding: utf-8 -*-
"""
上下文构建工具

从 langgraph_agent.py 拆分的辅助函数：
- _build_knowledge_system_messages: 知识库文档消息构建
- _build_summarization_context: 构建摘要上下文
- _compress_task_result: 压缩任务结果
"""

import json
import logging
from typing import Dict, Any, List, Optional

from langchain_core.messages import SystemMessage

logger = logging.getLogger(__name__)


# === 小说写作专用：任务感知压缩配置 ===
# 参考 KoboldAI 的关键词触发机制
# 根据工具名称决定保留长度（更可靠）
FULL_CONTENT_TOOLS = {
    # 章节读取类工具 - 需要完整内容
    "read_chapter_tool": 8000,
    "get_chapter_by_order_tool": 8000,
    "get_context_tool": 6000,
    # 分析类工具 - 需要较多内容
    "analyze_text_tool": 5000,
    # 检索类工具 - 保留中等内容
    "search_analysis_fragments_tool": 4000,
}

# 任务描述关键词匹配（作为备用方案）
FULL_CONTENT_KEYWORDS = {
    # 章节读取类 - 支持中英文
    "读取章节": 8000,
    "获取第": 8000,      # 匹配 "获取第X章"
    "读取第": 8000,      # 匹配 "读取第X章"
    "章节内容": 8000,
    # 分析类
    "分析": 5000,
    "概括": 5000,
    # 检索类
    "检索": 4000,
    "搜索": 4000,
}


def _compress_task_result(
    task_id: int,
    task_description: str,
    task_result: str,
    max_length: int = 2000,
    tool_name: str = ""
) -> str:
    """智能压缩任务结果

    Args:
        task_id: 任务ID
        task_description: 任务描述
        task_result: 原始任务结果
        max_length: 最大保留长度
        tool_name: 工具名称（优先使用）

    Returns:
        压缩后的结果
    """
    # 类型安全检查
    if not isinstance(task_result, str):
        logger.warning(
            f"[Compress] 任务{task_id}结果不是字符串: {type(task_result)}, "
            f"已转换为字符串"
        )
        task_result = str(task_result) if task_result is not None else ""

    # === 方案1：优先根据工具名称决定保留长度（最可靠） ===
    if tool_name and tool_name in FULL_CONTENT_TOOLS:
        limit = FULL_CONTENT_TOOLS[tool_name]
        if len(task_result) <= limit:
            logger.debug(
                f"[Compress] 任务{task_id}工具'{tool_name}'，"
                f"内容长度{len(task_result)}<=限制{limit}，保留完整内容"
            )
            return task_result
        # 超出限制时，保留首尾内容（70%头部 + 30%尾部）
        head_len = int(limit * 0.7)
        tail_len = int(limit * 0.3)
        omitted = len(task_result) - limit
        logger.info(
            f"[Compress] 任务{task_id}工具'{tool_name}'，"
            f"内容长度{len(task_result)}，保留{limit}字符（省略{omitted}字符）"
        )
        return f"{task_result[:head_len]}\n\n...[省略 {omitted} 字符]...\n\n{task_result[-tail_len:]}"

    # === 方案2：根据任务描述关键词匹配（备用方案） ===
    for keyword, limit in FULL_CONTENT_KEYWORDS.items():
        if keyword in task_description:
            if len(task_result) <= limit:
                logger.debug(
                    f"[Compress] 任务{task_id}匹配关键词'{keyword}'，"
                    f"内容长度{len(task_result)}<=限制{limit}，保留完整内容"
                )
                return task_result
            # 超出限制时，保留首尾内容
            head_len = int(limit * 0.7)
            tail_len = int(limit * 0.3)
            omitted = len(task_result) - limit
            logger.info(
                f"[Compress] 任务{task_id}匹配关键词'{keyword}'，"
                f"内容长度{len(task_result)}，保留{limit}字符（省略{omitted}字符）"
            )
            return f"{task_result[:head_len]}\n\n...[省略 {omitted} 字符]...\n\n{task_result[-tail_len:]}"

    # 如果结果很短，直接返回
    if len(task_result) <= max_length:
        return task_result

    # 尝试解析JSON格式的工具返回结果
    try:
        data = json.loads(task_result)
        if isinstance(data, dict) and 'content' in data:
            content = data.get('content')
            task_result = content if content is not None else ""
            if len(task_result) <= max_length:
                return task_result
    except (json.JSONDecodeError, TypeError, ValueError):
        pass

    # 章节内容：只保留摘要
    if "章" in task_result and ("第" in task_result or "标题" in task_result):
        lines = task_result.split('\n')
        summary_lines = []

        for line in lines[:10]:
            if "标题" in line or "章" in line or "摘要" in line:
                summary_lines.append(line)

        if summary_lines:
            compressed = '\n'.join(summary_lines)
            return f"[章节信息摘要]\n{compressed}\n[完整内容已压缩]"
        else:
            return f"[章节内容摘要]\n{task_result[:1500]}...\n{task_result[-500:]}"

    # RAG检索结果
    if "检索" in task_description or "搜索" in task_description:
        return f"[检索结果摘要]\n{task_result[:max_length]}"

    # 其他类型结果：保留前后部分
    half = max_length // 2
    return f"{task_result[:half]}...[省略{len(task_result)-max_length}字符]...{task_result[-half:]}"


def _build_summarization_context(
    user_message: str,
    task_results: List[Dict[str, Any]],
    max_context_length: int = 3000
) -> str:
    """构建Summarization的压缩上下文

    Args:
        user_message: 用户原始请求
        task_results: 任务执行结果列表
        max_context_length: 最大上下文长度（字符）

    Returns:
        压缩后的上下文字符串
    """
    context_parts = [f"用户请求：{user_message}\n\n执行结果："]
    current_length = len(context_parts[0])

    for task in task_results:
        task_id = task["task_id"]
        description = task["description"]
        tool_name = task.get("tool", "")  # 获取工具名称
        result = task.get("result")
        result = result if result is not None else ""
        status = task["status"]

        # 压缩结果（传递工具名称以便精确匹配）
        if status == "completed":
            compressed_result = _compress_task_result(
                task_id=task_id,
                task_description=description,
                task_result=result,
                max_length=2000,
                tool_name=tool_name  # 新增：传递工具名称
            )
        else:
            compressed_result = result[:200] if result else ""

        # 构建任务文本
        task_text = f"\n任务{task_id}（{description}）：\n{compressed_result}\n"

        # 检查是否超过限制
        if current_length + len(task_text) > max_context_length:
            task_text = f"\n任务{task_id}：[结果已省略]\n"

        context_parts.append(task_text)
        current_length += len(task_text)

        # 如果已经接近限制，停止添加
        if current_length >= max_context_length * 0.95:
            remaining_tasks = len(task_results) - task_id
            if remaining_tasks > 0:
                omit_msg = f"\n[还有{remaining_tasks}个任务结果已省略]\n"
                if current_length + len(omit_msg) <= max_context_length:
                    context_parts.append(omit_msg)
            break

    return ''.join(context_parts)


def _build_worldview_system_messages(
    context: Optional[Dict[str, Any]],
    max_total_chars: int = 3000
) -> List[SystemMessage]:
    """将 worldview_data 构造成系统提示

    Args:
        context: 上下文字典，包含 worldview_data
        max_total_chars: 总最大字符数

    Returns:
        SystemMessage 列表
    """
    if not context:
        return []

    worldview = context.get("worldview_data")
    if not isinstance(worldview, dict) or not worldview:
        return []

    parts: List[str] = []
    total = 0

    # 构建人物信息
    characters = worldview.get("characters", [])
    if characters:
        char_lines = ["【人物设定】"]
        for char in characters:
            name = char.get("name", "未知")
            role = char.get("role", "")
            desc = char.get("description", "")
            tags = char.get("tags", [])
            relationships = char.get("relationships", [])

            char_info = f"• {name}"
            if role:
                char_info += f"（{role}）"
            if desc:
                char_info += f"：{desc}"
            if tags:
                char_info += f" [标签: {', '.join(tags[:5])}]"
            if relationships:
                # 解析关系数组
                rel_strs = []
                for rel in relationships[:3]:  # 最多3个关系
                    if isinstance(rel, dict):
                        rel_name = rel.get("target_name", rel.get("name", ""))
                        rel_type = rel.get("relationship_type", rel.get("type", ""))
                        if rel_name and rel_type:
                            rel_strs.append(f"{rel_name}({rel_type})")
                if rel_strs:
                    char_info += f" [关系: {', '.join(rel_strs)}]"

            char_lines.append(char_info)

        char_block = "\n".join(char_lines)
        if total + len(char_block) <= max_total_chars:
            parts.append(char_block)
            total += len(char_block)

    # 构建地点信息
    locations = worldview.get("locations", [])
    if locations and total < max_total_chars:
        loc_lines = ["【地点设定】"]
        for loc in locations:
            name = loc.get("name", "未知")
            loc_type = loc.get("type", "")
            desc = loc.get("description", "")

            loc_info = f"• {name}"
            if loc_type:
                loc_info += f"（{loc_type}）"
            if desc:
                loc_info += f"：{desc}"

            loc_lines.append(loc_info)

        loc_block = "\n".join(loc_lines)
        if total + len(loc_block) <= max_total_chars:
            parts.append(loc_block)
            total += len(loc_block)

    # 构建设定信息
    settings = worldview.get("settings", [])
    if settings and total < max_total_chars:
        setting_lines = ["【世界设定】"]
        for setting in settings:
            title = setting.get("title", "未知")
            category = setting.get("category", "")
            content = setting.get("content", "")

            setting_info = f"• {title}"
            if category:
                setting_info += f"（{category}）"
            if content:
                setting_info += f"：{content}"

            setting_lines.append(setting_info)

        setting_block = "\n".join(setting_lines)
        if total + len(setting_block) <= max_total_chars:
            parts.append(setting_block)
            total += len(setting_block)

    # 构建作品规范
    guidelines = worldview.get("guidelines", {})
    if guidelines and total < max_total_chars:
        guide_lines = ["【写作规范】"]

        # 大纲流程
        outline = guidelines.get("outline", "")
        if outline:
            guide_lines.append(f"• 大纲流程：{outline[:500]}")

        # 风格相关
        style = guidelines.get("style", "")
        if style:
            guide_lines.append(f"• 整体风格：{style}")

        tone = guidelines.get("tone", "")
        if tone:
            guide_lines.append(f"• 语言风格：{tone}")

        # 写作参数
        words_per_chapter = guidelines.get("words_per_chapter")
        if words_per_chapter:
            guide_lines.append(f"• 每章字数：约{words_per_chapter}字")

        # 世界规则
        power_system = guidelines.get("power_system", "")
        if power_system:
            guide_lines.append(f"• 力量体系：{power_system[:300]}")

        world_rules = guidelines.get("world_rules", "")
        if world_rules:
            guide_lines.append(f"• 世界规则：{world_rules[:300]}")

        # 创作目标
        target_audience = guidelines.get("target_audience", "")
        if target_audience:
            guide_lines.append(f"• 目标读者：{target_audience}")

        main_theme = guidelines.get("main_theme", "")
        if main_theme:
            guide_lines.append(f"• 主题：{main_theme}")

        plot_direction = guidelines.get("plot_direction", "")
        if plot_direction:
            guide_lines.append(f"• 剧情走向：{plot_direction[:300]}")

        notes = guidelines.get("notes", "")
        if notes:
            guide_lines.append(f"• 备注：{notes[:200]}")

        guide_block = "\n".join(guide_lines)
        if total + len(guide_block) <= max_total_chars:
            parts.append(guide_block)
            total += len(guide_block)

    if not parts:
        return []

    system_text = (
        "以下是本作品的世界观设定，请在创作时严格遵循这些设定，确保内容一致性：\n\n"
        + "\n\n".join(parts)
        + "\n\n请基于以上世界观设定进行创作，保持人物性格、地点描述、世界规则的一致性。"
    )

    return [SystemMessage(content=system_text)]


def _build_knowledge_system_messages(
    context: Optional[Dict[str, Any]],
    max_docs: int = 3,
    max_snippet_chars: int = 800,
    max_total_chars: int = 2400
) -> List[SystemMessage]:
    """将 knowledge_docs 构造成系统提示

    Args:
        context: 上下文字典，包含 knowledge_docs
        max_docs: 最大文档数
        max_snippet_chars: 单个文档最大字符数
        max_total_chars: 总最大字符数

    Returns:
        SystemMessage 列表
    """
    if not context:
        return []

    docs = context.get("knowledge_docs")
    if not isinstance(docs, list) or not docs:
        return []

    parts: List[str] = []
    total = 0

    for doc in docs[:max_docs]:
        title = doc.get("title") or "未命名文档"
        tags = doc.get("tags") or []
        source = doc.get("source_type") or "unknown"
        highlight = doc.get("highlight")
        content = highlight or doc.get("content") or ""
        snippet = content.strip()[:max_snippet_chars]

        if not snippet:
            continue

        tags_str = ', '.join(tags) if tags else '无'
        block = (
            f"=== 知识库文档 ===\n"
            f"文档标题: {title}\n"
            f"文档来源: {source}\n"
            f"文档标签: {tags_str}\n"
            f"文档正文内容:\n{snippet}\n"
            f"=== 文档结束 ==="
        )

        if total + len(block) > max_total_chars:
            break

        parts.append(block)
        total += len(block)

    if not parts:
        return []

    system_text = (
        "以下是用户指定或检索到的知识库文档，请严格参考其内容回答，避免臆造：\n\n"
        + "\n\n".join(parts)
    )

    return [SystemMessage(content=system_text)]


__all__ = [
    "_compress_task_result",
    "_build_summarization_context",
    "_build_knowledge_system_messages",
    "_build_worldview_system_messages",
]
