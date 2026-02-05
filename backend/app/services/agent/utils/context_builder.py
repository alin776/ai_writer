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
from app.utils.content_sanitizer import content_sanitizer

logger = logging.getLogger(__name__)


# === 小说写作专用：任务感知压缩配置 ===
# 参考 KoboldAI 的关键词触发机制
# 根据工具名称决定保留长度（更可靠）
# 🆕 2026-01-21: 完善工具截断配置，确保所有返回大量内容的工具都有合适的限制
FULL_CONTENT_TOOLS = {
    # === 章节读取类工具 - 需要完整内容 ===
    "read_chapter_tool": 8000,
    "read_chapter": 8000,  # 兼容不带 _tool 后缀
    "get_chapter_by_order_tool": 8000,
    "get_chapter_by_order": 8000,  # 兼容不带 _tool 后缀
    "get_context_tool": 6000,
    "get_context": 6000,  # 兼容不带 _tool 后缀
    # === 聚合工具 - 返回内容较多 ===
    "get_writing_context": 12000,
    # === 分析类工具 - 需要较多内容 ===
    "analyze_text_tool": 5000,
    "analyze_text": 5000,  # 兼容不带 _tool 后缀
    "analyze_content": 8000,
    "analyze_style_tool": 4000,  # 风格分析报告
    "analyze_style": 4000,  # 兼容不带 _tool 后缀
    # === 检索/定位类工具 ===
    "search_analysis_fragments_tool": 4000,
    "search_analysis_fragments": 4000,  # 兼容不带 _tool 后缀
    "search_content": 2000,
    "locate_content": 4000,  # 定位工具返回段落文本+锚点
    "read_paragraph": 3000,  # 读取段落完整内容
    # === 探索类工具 - 返回大量证据 ===
    "explore_content": 20000,
    "load_explore_artifact": 8000,
    # === 世界观/一致性类工具 ===
    "get_worldview_summary": 6000,  # 角色/地点/设定列表
    "check_story_consistency_tool": 5000,  # 一致性分析报告
    "check_consistency": 5000,  # 兼容不带 _tool 后缀
    # === 风格类工具 ===
    "get_style_guidance_tool": 4000,
    "get_style_guidance": 4000,  # 兼容不带 _tool 后缀
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


def _collect_worldview_parts(
    worldview: Dict[str, Any],
    max_items_per_category: int
) -> List[str]:
    """收集世界观软约束片段（人物/地点/设定/规范）"""
    parts: List[str] = []
    def _clip(text: Any, max_len: int = 120) -> str:
        value = str(text or "").strip()
        if not value:
            return ""
        if len(value) > max_len:
            return value[:max_len] + "…"
        return value

    # 构建人物信息
    characters = worldview.get("characters", [])
    if characters:
        char_lines = ["【人物设定】"]
        for char in characters[:max_items_per_category]:
            name = char.get("name", "未知")
            role = char.get("role", "")
            desc = char.get("description", "")
            tags = char.get("tags", [])
            relationships = char.get("relations") or char.get("relationships") or []
            constraints = char.get("constraints") or []

            char_info = f"• {name}"
            if role:
                char_info += f"（{role}）"
            if desc:
                char_info += f"：{_clip(desc, 120)}"
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
                        elif rel_name:
                            rel_strs.append(str(rel_name))
                    elif rel:
                        rel_strs.append(str(rel))
                if rel_strs:
                    char_info += f" [关系: {', '.join(rel_strs)}]"
            if constraints:
                constraint_items = [str(c) for c in constraints if str(c).strip()][:3]
                if constraint_items:
                    char_info += f" [约束: {', '.join(constraint_items)}]"

            char_lines.append(char_info)

        parts.append("\n".join(char_lines))

    # 构建地点信息
    locations = worldview.get("locations", [])
    if locations:
        loc_lines = ["【地点设定】"]
        for loc in locations[:max_items_per_category]:
            name = loc.get("name", "未知")
            loc_type = loc.get("type", "")
            desc = loc.get("description", "")
            relations = loc.get("relations") or loc.get("related_locations") or []
            constraints = loc.get("constraints") or []

            loc_info = f"• {name}"
            if loc_type:
                loc_info += f"（{loc_type}）"
            if desc:
                loc_info += f"：{_clip(desc, 120)}"
            if relations:
                rel_items = []
                for rel in relations[:3]:
                    if isinstance(rel, dict):
                        rel_name = rel.get("name") or rel.get("target_name") or rel.get("title")
                    else:
                        rel_name = rel
                    if rel_name and str(rel_name).strip():
                        rel_items.append(str(rel_name))
                if rel_items:
                    loc_info += f" [关联: {', '.join(rel_items)}]"
            if constraints:
                constraint_items = [str(c) for c in constraints if str(c).strip()][:3]
                if constraint_items:
                    loc_info += f" [约束: {', '.join(constraint_items)}]"

            loc_lines.append(loc_info)

        parts.append("\n".join(loc_lines))

    # 构建设定信息
    settings = worldview.get("settings", [])
    if settings:
        setting_lines = ["【世界设定】"]
        for setting in settings[:max_items_per_category]:
            title = setting.get("title", "未知")
            category = setting.get("category", "")
            content = setting.get("content", "")
            relations = setting.get("relations") or setting.get("related_items") or []
            constraints = setting.get("constraints") or []

            setting_info = f"• {title}"
            if category:
                setting_info += f"（{category}）"
            if content:
                setting_info += f"：{_clip(content, 120)}"
            if relations:
                rel_items = []
                for rel in relations[:3]:
                    if isinstance(rel, dict):
                        rel_name = rel.get("name") or rel.get("target_name") or rel.get("title")
                    else:
                        rel_name = rel
                    if rel_name and str(rel_name).strip():
                        rel_items.append(str(rel_name))
                if rel_items:
                    setting_info += f" [关联: {', '.join(rel_items)}]"
            if constraints:
                constraint_items = [str(c) for c in constraints if str(c).strip()][:3]
                if constraint_items:
                    setting_info += f" [约束: {', '.join(constraint_items)}]"

            setting_lines.append(setting_info)

        parts.append("\n".join(setting_lines))

    # 构建术语表
    glossary = worldview.get("glossary", [])
    if glossary:
        glossary_lines = ["【术语表】"]
        for item in glossary[:max_items_per_category]:
            term = item.get("term") or item.get("name") or "未命名"
            desc = item.get("definition") or item.get("description") or ""
            line = f"• {term}"
            if desc:
                line += f"：{_clip(desc, 120)}"
            glossary_lines.append(line)
        parts.append("\n".join(glossary_lines))

    # 构建时间线
    timeline = worldview.get("timeline", [])
    if timeline:
        timeline_lines = ["【时间线】"]
        for event in timeline[:max_items_per_category]:
            title = event.get("title") or "事件"
            chapter_no = event.get("chapter_number")
            desc = event.get("description") or ""
            prefix = f"第{chapter_no}章" if chapter_no else ""
            line = f"• {prefix} {title}".strip()
            if desc:
                line += f"：{_clip(desc, 100)}"
            timeline_lines.append(line)
        parts.append("\n".join(timeline_lines))

    # 构建作品规范
    guidelines = worldview.get("guidelines", {})
    if guidelines:
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

        parts.append("\n".join(guide_lines))

    return parts


def _build_worldview_system_messages(
    context: Optional[Dict[str, Any]],
    max_total_chars: int = 3000,
    max_items_per_category: int = 8
) -> List[SystemMessage]:
    """将世界观软约束构造成系统提示（优先使用 worldview_pack）

    Args:
        context: 上下文字典，包含 worldview_data
        max_total_chars: 总最大字符数

    Returns:
        SystemMessage 列表
    """
    if not context:
        return []

    worldview_pack = context.get("worldview_pack")
    if isinstance(worldview_pack, dict) and worldview_pack:
        worldview = worldview_pack
    else:
        worldview = context.get("worldview_data")
    if not isinstance(worldview, dict) or not worldview:
        return []

    parts: List[str] = []
    total = 0
    for part in _collect_worldview_parts(worldview, max_items_per_category):
        if total + len(part) <= max_total_chars:
            parts.append(part)
            total += len(part)
        if total >= max_total_chars:
            break

    if not parts:
        return []

    system_text = (
        "以下是本作品的世界观设定，请在创作时严格遵循这些设定，确保内容一致性：\n\n"
        + "\n\n".join(parts)
        + "\n\n请基于以上世界观设定进行创作，保持人物性格、地点描述、世界规则的一致性。"
    )

    return [SystemMessage(content=system_text)]


def _build_worldview_context_text(
    context: Optional[Dict[str, Any]],
    max_total_chars: int = 1800,
    max_items_per_category: int = 6
) -> str:
    """构建世界观软约束文本（用于创作提示词注入）"""
    if not context:
        return ""
    worldview_pack = context.get("worldview_pack")
    if isinstance(worldview_pack, dict) and worldview_pack:
        worldview = worldview_pack
    else:
        worldview = context.get("worldview_data")
    if not isinstance(worldview, dict) or not worldview:
        return ""
    parts: List[str] = []
    total = 0
    for part in _collect_worldview_parts(worldview, max_items_per_category):
        if total + len(part) <= max_total_chars:
            parts.append(part)
            total += len(part)
        if total >= max_total_chars:
            break
    if not parts:
        return ""
    content = "【世界观参考】\n" + "\n\n".join(parts)
    if len(content) > max_total_chars:
        content = content[:max_total_chars] + "…"
    return content


def _build_worldview_hard_constraints(
    context: Optional[Dict[str, Any]],
    max_total_chars: int = 800,
    max_items_per_section: int = 6
) -> str:
    """从 worldview_data 中提取硬约束（规则/禁忌/风格）"""
    if not context:
        return ""

    worldview_pack = context.get("worldview_pack")
    worldview_data = context.get("worldview_data")
    worldview = worldview_pack if isinstance(worldview_pack, dict) and worldview_pack else worldview_data
    if not isinstance(worldview, dict) or not worldview:
        return ""

    def _normalize_list(value: Any) -> List[str]:
        if not value:
            return []
        if isinstance(value, list):
            items = [str(v).strip() for v in value if str(v).strip()]
            return items[:max_items_per_section]
        text = str(value).strip()
        return [text] if text else []

    fallback = worldview_data if isinstance(worldview_data, dict) else {}
    rules_list = _normalize_list(worldview.get("world_rules") or fallback.get("world_rules"))
    constraints_list = _normalize_list(worldview.get("constraints") or fallback.get("constraints"))
    taboo_list = _normalize_list(worldview.get("taboo") or fallback.get("taboo"))

    guidelines = worldview.get("guidelines") or fallback.get("guidelines")
    if not isinstance(guidelines, dict):
        guidelines = {}

    guidelines = content_sanitizer.sanitize_worldview_item(guidelines, max_field_length=400)

    parts: List[str] = []

    def add(label: str, value: Any, max_len: int = 260) -> None:
        if value is None:
            return
        text = str(value).strip()
        if not text:
            return
        if len(text) > max_len:
            text = text[:max_len] + "…"
        parts.append(f"- {label}：{text}")

    if rules_list:
        for item in rules_list:
            add("世界规则", item, max_len=220)
    else:
        add("世界规则", guidelines.get("world_rules"))
    if constraints_list:
        for item in constraints_list:
            add("约束", item, max_len=220)
    else:
        add("约束", guidelines.get("constraints"))
    if taboo_list:
        for item in taboo_list:
            add("禁忌", item, max_len=220)
    else:
        add("禁忌", guidelines.get("taboo"))
    add("力量体系", guidelines.get("power_system"))
    add("整体风格", guidelines.get("style"))
    add("语言风格", guidelines.get("tone"))
    add("剧情走向", guidelines.get("plot_direction"))
    add("主题", guidelines.get("main_theme"))
    add("目标读者", guidelines.get("target_audience"))
    if guidelines.get("words_per_chapter"):
        add("每章字数", f"约{guidelines.get('words_per_chapter')}字", max_len=80)
    if not taboo_list:
        add("备注/禁忌", guidelines.get("notes"))

    if not parts:
        return ""

    text = "【硬约束（必须遵守）】\n" + "\n".join(parts)
    if len(text) > max_total_chars:
        text = text[:max_total_chars] + "…"
    return text


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
    "_build_worldview_hard_constraints",
]
