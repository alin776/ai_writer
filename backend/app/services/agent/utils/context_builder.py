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


def _compress_task_result(
    task_id: int,
    task_description: str,
    task_result: str,
    max_length: int = 2000
) -> str:
    """智能压缩任务结果

    Args:
        task_id: 任务ID
        task_description: 任务描述
        task_result: 原始任务结果
        max_length: 最大保留长度

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
        result = task.get("result")
        result = result if result is not None else ""
        status = task["status"]

        # 压缩结果
        if status == "completed":
            compressed_result = _compress_task_result(
                task_id=task_id,
                task_description=description,
                task_result=result,
                max_length=2000
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
]
