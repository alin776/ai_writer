# -*- coding: utf-8 -*-
"""
工具辅助方法

从 langgraph_agent.py 提取的工具相关辅助方法：
- 版本引用解析
- 工具参数标准化
"""

import logging
from typing import Dict, Any, Optional

logger = logging.getLogger(__name__)


def resolve_version_reference(reference: str, versions: Dict[str, str]) -> Optional[str]:
    """智能解析版本引用，支持多种表达方式

    Args:
        reference: 用户的版本引用表达（如"第二版"、"版本B"、"$VERSION_B$"、"2"等）
        versions: 版本内容字典 {"version_a": "...", "version_b": "...", "version_c": "..."}

    Returns:
        匹配到的版本内容，如果没有匹配返回None
    """
    if not reference or not versions:
        return None

    ref = reference.lower().strip()

    # 版本A的各种表达方式
    version_a_patterns = [
        "版本a", "version_a", "version a", "$version_a$",
        "第一版", "第1版", "一版", "1版", "a版", "a",
        "第一个", "第1个", "1", "一"
    ]

    # 版本B的各种表达方式
    version_b_patterns = [
        "版本b", "version_b", "version b", "$version_b$",
        "第二版", "第2版", "二版", "2版", "b版", "b",
        "第二个", "第2个", "2", "二"
    ]

    # 版本C的各种表达方式
    version_c_patterns = [
        "版本c", "version_c", "version c", "$version_c$",
        "第三版", "第3版", "三版", "3版", "c版", "c",
        "第三个", "第3个", "3", "三"
    ]

    # 检查是否匹配版本A
    if any(p in ref or ref == p for p in version_a_patterns):
        content = versions.get("version_a", "")
        if content:
            return content

    # 检查是否匹配版本B
    if any(p in ref or ref == p for p in version_b_patterns):
        content = versions.get("version_b", "")
        if content:
            return content

    # 检查是否匹配版本C
    if any(p in ref or ref == p for p in version_c_patterns):
        content = versions.get("version_c", "")
        if content:
            return content

    # 如果reference本身就是版本内容（长度>50），直接返回
    if len(reference) > 50:
        return reference

    logger.warning(f"[ToolHelpers] 无法解析版本引用: '{reference}'")
    return None


def normalize_tool_params(tool_name: str, params: Dict[str, Any]) -> Dict[str, Any]:
    """标准化工具参数，将不符合格式的参数转换为正确格式

    Args:
        tool_name: 工具名称
        params: 原始参数

    Returns:
        标准化后的参数
    """
    normalized = params.copy()

    # continue_writing_tool 的 requirements 必须是字符串
    if tool_name == "continue_writing_tool":
        requirements = params.get("requirements", "")
        if isinstance(requirements, dict):
            # 将字典转换为可读的字符串
            parts = []
            for key, value in requirements.items():
                parts.append(f"{key}: {value}")
            normalized["requirements"] = "，".join(parts)
            logger.info(f"[参数标准化] continue_writing_tool.requirements: dict → str")

    # 🔧 2025-12-14: analyze_content → analyze_text 参数转换
    # analyze_content 使用 content 参数，analyze_text 使用 text 参数
    elif tool_name in ("analyze_content", "analyze_content_tool", "analyze_text_tool", "analyze_text"):
        # 如果有 content 但没有 text，转换参数名
        if "content" in params and "text" not in params:
            normalized["text"] = params["content"]
            del normalized["content"]
            logger.info(f"[参数标准化] {tool_name}.content → text")
        if "text" in normalized and not isinstance(normalized["text"], str):
            normalized["text"] = str(normalized["text"])
            logger.info(f"[参数标准化] {tool_name}.text: {type(params.get('text', params.get('content'))).__name__} → str")
        if "focus" in params and not isinstance(params["focus"], str):
            normalized["focus"] = str(params["focus"])

    return normalized
