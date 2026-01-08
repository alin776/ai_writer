# -*- coding: utf-8 -*-
"""
Agent章节管理工具 - 允许Agent创建和管理章节

这些工具需要用户确认才能执行实际操作。
"""
from typing import Optional
import logging
import json

from langchain_core.tools import tool
from .tool_registry import register_as_tool
from app.core.database import AsyncSessionLocal
from app.services.chapter_service import ChapterService
from app.schemas.chapter import ChapterCreate, ChapterUpdate

logger = logging.getLogger(__name__)


@tool
@register_as_tool(
    "create_chapter",
    "chapter",
    "创建新章节。此操作需要用户确认。"
)
async def create_chapter(
    work_id: str,
    title: str,
    content: str = "",
    order: int = None
) -> str:
    """
    创建新章节

    Args:
        work_id: 作品ID
        title: 章节标题
        content: 章节内容（可选）
        order: 章节顺序（可选，默认追加到末尾）

    Returns:
        包含确认请求的结果
    """
    try:
        # 生成内容预览
        content_preview = content[:50] if content and len(content) > 50 else content

        return json.dumps({
            "success": True,
            "requires_confirmation": True,
            "action_type": "create",
            "work_id": work_id,
            "chapter_title": title,
            "content": content,
            "content_preview": content_preview,
            "order": order,
            "description": f"创建新章节：{title}"
        }, ensure_ascii=False)

    except Exception as e:
        logger.error(f"create_chapter failed: {e}")
        return json.dumps({"success": False, "error": str(e)}, ensure_ascii=False)


@tool
@register_as_tool(
    "update_chapter_title",
    "chapter",
    "修改章节标题。此操作需要用户确认。"
)
async def update_chapter_title(
    chapter_id: str,
    new_title: str,
    old_title: str = None
) -> str:
    """
    修改章节标题

    Args:
        chapter_id: 章节ID
        new_title: 新标题
        old_title: 原标题（可选，用于显示对比）

    Returns:
        包含确认请求的结果
    """
    try:
        # 如果没有提供原标题，尝试获取
        actual_old_title = old_title
        if not actual_old_title:
            try:
                async with AsyncSessionLocal() as db:
                    chapter_svc = ChapterService(db)
                    chapter = await chapter_svc.get_chapter_by_id(chapter_id)
                    if chapter:
                        actual_old_title = chapter.title
            except Exception as e:
                logger.warning(f"获取原标题失败: {e}")

        return json.dumps({
            "success": True,
            "requires_confirmation": True,
            "action_type": "rename",
            "chapter_id": chapter_id,
            "old_title": actual_old_title,
            "new_title": new_title,
            "description": f"修改标题：{actual_old_title or '未知'} → {new_title}"
        }, ensure_ascii=False)

    except Exception as e:
        logger.error(f"update_chapter_title failed: {e}")
        return json.dumps({"success": False, "error": str(e)}, ensure_ascii=False)
