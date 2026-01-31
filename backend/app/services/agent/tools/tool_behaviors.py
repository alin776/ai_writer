"""
工具行为约束系统 (Tool Behavior System)

为不同分类的工具定义行为规则，确保：
- CREATIVE 工具：输出纯净内容，自动过滤脏信息
- OPERATION 工具：需要 HITL 确认，直接修改数据
- QUERY 工具：只读取数据，不修改
- ANALYSIS 工具：分析内容，不修改数据

使用方式：
    from .tool_behaviors import creative_output_filter, get_category_behavior

    # 在 CREATIVE 工具返回前过滤
    content = creative_output_filter(raw_content)
"""

import re
import logging
from typing import Dict, Any, Optional, Callable
from enum import Enum
from dataclasses import dataclass

logger = logging.getLogger(__name__)


# ==================== 分类行为定义 ====================

@dataclass
class CategoryBehavior:
    """分类行为定义"""
    requires_hitl: bool          # 是否需要 HITL 确认
    modifies_data: bool          # 是否修改数据
    generates_content: bool      # 是否生成内容
    needs_output_filter: bool    # 是否需要输出过滤
    description: str             # 分类描述


# 分类行为映射
CATEGORY_BEHAVIORS: Dict[str, CategoryBehavior] = {
    "creative": CategoryBehavior(
        requires_hitl=False,
        modifies_data=False,
        generates_content=True,
        needs_output_filter=True,  # CREATIVE 需要过滤
        description="AI生成内容，不直接修改数据库"
    ),
    "operation": CategoryBehavior(
        requires_hitl=True,  # OPERATION 需要 HITL
        modifies_data=True,
        generates_content=False,
        needs_output_filter=False,
        description="直接修改数据库或编辑器内容，需要用户确认"
    ),
    "query": CategoryBehavior(
        requires_hitl=False,
        modifies_data=False,
        generates_content=False,
        needs_output_filter=False,
        description="只读取数据，不修改"
    ),
    "analysis": CategoryBehavior(
        requires_hitl=False,
        modifies_data=False,
        generates_content=False,
        needs_output_filter=False,
        description="分析内容，不修改数据"
    ),
}


def get_category_behavior(category: str) -> CategoryBehavior:
    """获取分类的行为定义"""
    return CATEGORY_BEHAVIORS.get(category, CATEGORY_BEHAVIORS["query"])


# ==================== CREATIVE 输出过滤器 ====================

# 开头的脏信息模式
_DIRTY_PATTERNS_START = [
    r'^好的[，,。].*?[：:]\s*\n*',
    r'^我来帮你.*?[：:]\s*\n*',
    r'^以下是.*?[：:]\s*\n*',
    r'^根据.*?[，,].*?[：:]\s*\n*',
    r'^接下来.*?[：:]\s*\n*',
    r'^我将为你.*?[：:]\s*\n*',
    r'^让我.*?[：:]\s*\n*',
    r'^现在.*?[：:]\s*\n*',
    r'^首先.*?[：:]\s*\n*',
    r'^好[，,].*?[：:]\s*\n*',
    r'^当然[，,].*?[：:]\s*\n*',
    r'^没问题[，,].*?[：:]\s*\n*',
]

# 结尾的脏信息模式
_DIRTY_PATTERNS_END = [
    r'\n*以上是.*?[。！]$',
    r'\n*希望.*?[。！]$',
    r'\n*如果你.*?[。！]$',
    r'\n*如果有.*?[。！]$',
    r'\n*总结[：:].*$',
    r'\n*这就是.*?[。！]$',
    r'\n*以上就是.*?[。！]$',
]

# 协议格式标记
_BODY_PATTERN = re.compile(r'---BODY---\s*(.*?)\s*---END---', re.DOTALL)


def creative_output_filter(content: str) -> str:
    """
    CREATIVE 工具的输出过滤器

    功能：
    1. 提取 BODY 块（如果有协议格式）
    2. 去除开头的提示语（"好的，我来帮你..."）
    3. 去除结尾的总结语（"以上是..."）

    Args:
        content: 原始 AI 生成内容

    Returns:
        过滤后的纯净内容
    """
    if not content:
        return content

    original_length = len(content)

    # 1. 尝试提取 BODY 块（如果有协议格式）
    body_match = _BODY_PATTERN.search(content)
    if body_match:
        content = body_match.group(1)
        logger.info(f"[creative_filter] 提取 BODY 块: {original_length} -> {len(content)}")

    # 2. 去除开头的脏信息
    for pattern in _DIRTY_PATTERNS_START:
        content = re.sub(pattern, '', content, flags=re.IGNORECASE)

    # 3. 去除结尾的脏信息
    for pattern in _DIRTY_PATTERNS_END:
        content = re.sub(pattern, '', content, flags=re.IGNORECASE)

    # 4. 清理多余空白
    content = content.strip()

    # 记录过滤效果
    if len(content) != original_length:
        logger.info(f"[creative_filter] 过滤完成: {original_length} -> {len(content)} 字符")

    return content


def apply_category_filter(category: str, content: str) -> str:
    """
    根据分类应用相应的过滤器

    Args:
        category: 工具分类
        content: 原始内容

    Returns:
        过滤后的内容
    """
    behavior = get_category_behavior(category)

    if behavior.needs_output_filter:
        return creative_output_filter(content)

    return content


# ==================== 工具装饰器 ====================

def with_creative_filter(func: Callable) -> Callable:
    """
    装饰器：自动为 CREATIVE 工具的输出添加过滤

    使用方式：
        @with_creative_filter
        async def smart_continue(...):
            content = await ai_service.call_ai(...)
            return content  # 会自动过滤
    """
    import asyncio
    import functools

    @functools.wraps(func)
    async def wrapper(*args, **kwargs):
        result = await func(*args, **kwargs)

        # 如果返回的是字符串，直接过滤
        if isinstance(result, str):
            return creative_output_filter(result)

        # 如果返回的是 dict，过滤 content 字段
        if isinstance(result, dict) and 'content' in result:
            result['content'] = creative_output_filter(result['content'])

        return result

    return wrapper


# ==================== 导出 ====================

__all__ = [
    "CategoryBehavior",
    "CATEGORY_BEHAVIORS",
    "get_category_behavior",
    "creative_output_filter",
    "apply_category_filter",
    "with_creative_filter",
]
