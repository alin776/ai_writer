# -*- coding: utf-8 -*-
"""
Agent章节管理工具 - 允许Agent创建和管理章节

v2.0 (2026-01-10): 改为乐观执行模式
- 工具直接执行数据库操作（不再需要用户确认）
- 记录操作日志，支持回滚
- 用户在执行完成后选择采纳或弃用
"""
from typing import Optional
import logging
import json
import uuid
import redis

from langchain_core.tools import tool
from .tool_registry import register_as_tool
from app.core.database import AsyncSessionLocal
from app.services.chapter_service import ChapterService
from app.schemas.chapter import ChapterCreate, ChapterUpdate
from .operation_log import OperationLogManager

logger = logging.getLogger(__name__)

# 全局 Redis 连接池（复用，避免每次都创建新连接）
_chapter_tools_redis_pool = None


def _get_operation_log_manager():
    """获取操作日志管理器（使用全局连接池）"""
    global _chapter_tools_redis_pool

    if _chapter_tools_redis_pool is None:
        _chapter_tools_redis_pool = redis.ConnectionPool(
            host='localhost', port=6379, db=1,
            decode_responses=False, max_connections=10
        )

    return OperationLogManager(redis.Redis(connection_pool=_chapter_tools_redis_pool))


@tool
@register_as_tool(
    "create_chapter",
    "operation",
    "创建新章节（直接执行，支持回滚）"
)
async def create_chapter(
    work_id: str,
    title: str,
    content: str = "",
    order: Optional[int] = None,
    conversation_id: Optional[str] = None
) -> str:
    """
    创建新章节（直接执行）

    Args:
        work_id: 作品ID
        title: 章节标题
        content: 章节内容（可选）
        order: 章节顺序（可选，默认追加到末尾）
        conversation_id: 会话ID（用于记录操作日志）

    Returns:
        执行结果
    """
    try:
        chapter_id = str(uuid.uuid4())

        async with AsyncSessionLocal() as db:
            chapter_svc = ChapterService(db)
            chapter = await chapter_svc.create_chapter_simple(
                work_id=work_id,
                title=title,
                content=content,
                order=order,
                chapter_id=chapter_id
            )

            # 记录操作日志（用于回滚）
            if conversation_id:
                op_log = _get_operation_log_manager()
                op_log.record_operation(
                    conversation_id=conversation_id,
                    op_id=str(uuid.uuid4()),
                    op_type="create_chapter",
                    chapter_id=chapter_id,
                    work_id=work_id,
                    rollback_data={},  # 创建操作的回滚就是删除
                    description=f"创建章节：{title}"
                )

            return json.dumps({
                "success": True,
                "action_type": "create",
                "chapter_id": chapter_id,
                "work_id": work_id,
                "chapter_title": title,
                "word_count": chapter.word_count,
                "description": f"已创建章节：{title}"
            }, ensure_ascii=False)

    except Exception as e:
        logger.error(f"create_chapter failed: {e}")
        return json.dumps({"success": False, "error": str(e)}, ensure_ascii=False)


@tool
@register_as_tool(
    "update_chapter_title",
    "operation",
    "修改章节标题（直接执行，支持回滚）"
)
async def update_chapter_title(
    chapter_id: str,
    new_title: str,
    old_title: Optional[str] = None,
    conversation_id: Optional[str] = None,
    work_id: Optional[str] = None  # v8.0: 添加 work_id 用于章节序号解析
) -> str:
    """
    修改章节标题（直接执行）

    Args:
        chapter_id: 章节ID（支持 UUID 或章节序号如 "1", "2"）
        new_title: 新标题
        old_title: 原标题（可选，用于显示对比）
        conversation_id: 会话ID（用于记录操作日志）
        work_id: 作品ID（当 chapter_id 为序号时必需）

    Returns:
        执行结果
    """
    try:
        from app.services.agent.langgraph_tools import resolve_chapter_id

        async with AsyncSessionLocal() as db:
            # v8.0: 支持章节序号自动转换为 UUID
            resolved_chapter_id = chapter_id
            if work_id and not chapter_id.count('-') == 4:  # 不是 UUID 格式
                resolved_id, error = await resolve_chapter_id(work_id, chapter_id, db)
                if error:
                    return error
                if resolved_id:
                    resolved_chapter_id = resolved_id
                    logger.info(f"[update_chapter_title] 章节序号 {chapter_id} -> UUID {resolved_chapter_id}")

            chapter_svc = ChapterService(db)
            chapter = await chapter_svc.get_chapter_by_id(resolved_chapter_id)

            if not chapter:
                return json.dumps({"success": False, "error": f"章节不存在: {chapter_id}"}, ensure_ascii=False)

            actual_old_title = old_title or chapter.title
            actual_work_id = str(chapter.work_id)

            # 执行更新
            await chapter_svc.update_chapter(resolved_chapter_id, ChapterUpdate(title=new_title))

            # 记录操作日志（用于回滚）
            if conversation_id:
                op_log = _get_operation_log_manager()
                op_log.record_operation(
                    conversation_id=conversation_id,
                    op_id=str(uuid.uuid4()),
                    op_type="update_title",
                    chapter_id=resolved_chapter_id,
                    work_id=actual_work_id,
                    rollback_data={"old_title": actual_old_title},
                    description=f"修改标题：{actual_old_title} → {new_title}"
                )

            return json.dumps({
                "success": True,
                "action_type": "rename",
                "chapter_id": resolved_chapter_id,
                "work_id": actual_work_id,
                "old_title": actual_old_title,
                "new_title": new_title,
                "description": f"已修改标题：{actual_old_title} → {new_title}"
            }, ensure_ascii=False)

    except Exception as e:
        logger.error(f"update_chapter_title failed: {e}")
        return json.dumps({"success": False, "error": str(e)}, ensure_ascii=False)


@tool
@register_as_tool(
    "delete_chapter",
    "operation",
    "删除章节（直接执行，支持回滚）"
)
async def delete_chapter(
    chapter_id: str,
    chapter_title: Optional[str] = None,
    conversation_id: Optional[str] = None,
    work_id: Optional[str] = None,  # v8.0: 添加 work_id 用于章节序号解析
    step_reasoning: Optional[str] = None
) -> str:
    """
    删除章节（直接执行）

    Args:
        chapter_id: 章节ID（支持 UUID 或章节序号如 "1", "2"）
        chapter_title: 章节标题（用于确认显示）
        conversation_id: 会话ID（用于记录操作日志）
        work_id: 作品ID（当 chapter_id 为序号时必需）

    Returns:
        执行结果
    """
    try:
        from app.services.agent.langgraph_tools import resolve_chapter_id

        async with AsyncSessionLocal() as db:
            # v8.0: 支持章节序号自动转换为 UUID
            resolved_chapter_id = chapter_id
            if work_id and not chapter_id.count('-') == 4:  # 不是 UUID 格式
                resolved_id, error = await resolve_chapter_id(work_id, chapter_id, db)
                if error:
                    return error
                if resolved_id:
                    resolved_chapter_id = resolved_id
                    logger.info(f"[delete_chapter] 章节序号 {chapter_id} -> UUID {resolved_chapter_id}")

            chapter_svc = ChapterService(db)
            chapter = await chapter_svc.get_chapter_by_id(resolved_chapter_id)

            if not chapter:
                return json.dumps({"success": False, "error": f"章节不存在: {chapter_id}"}, ensure_ascii=False)

            actual_title = chapter_title or chapter.title
            actual_work_id = str(chapter.work_id)

            # 保存章节数据用于回滚
            chapter_data = {
                "id": resolved_chapter_id,
                "work_id": actual_work_id,
                "title": chapter.title,
                "content": chapter.content,
                "order": chapter.order
            }

            # 执行删除
            await chapter_svc.delete_chapter(resolved_chapter_id)

            # 记录操作日志（用于回滚）
            if conversation_id:
                op_log = _get_operation_log_manager()
                op_log.record_operation(
                    conversation_id=conversation_id,
                    op_id=str(uuid.uuid4()),
                    op_type="delete_chapter",
                    chapter_id=resolved_chapter_id,
                    work_id=actual_work_id,
                    rollback_data={"chapter_data": chapter_data},
                    description=f"删除章节：{actual_title}"
                )

            return json.dumps({
                "success": True,
                "action_type": "delete",
                "chapter_id": resolved_chapter_id,
                "work_id": actual_work_id,
                "chapter_title": actual_title,
                "description": f"已删除章节：{actual_title}"
            }, ensure_ascii=False)

    except Exception as e:
        logger.error(f"delete_chapter failed: {e}")
        return json.dumps({"success": False, "error": str(e)}, ensure_ascii=False)


@tool
@register_as_tool(
    "update_chapter_content",
    "operation",
    "更新章节内容（直接执行，支持回滚）"
)
async def update_chapter_content(
    chapter_id: str,
    new_content: str,
    operation: str = "replace",
    position: Optional[dict] = None,
    conversation_id: Optional[str] = None,
    work_id: Optional[str] = None,  # v8.0: 添加 work_id 用于章节序号解析
    step_reasoning: Optional[str] = None
) -> str:
    """
    更新章节内容（直接执行）

    Args:
        chapter_id: 章节ID（支持 UUID 或章节序号如 "1", "2"）
        new_content: 新内容
        operation: 操作类型 ("replace" | "append" | "insert")
        position: 位置信息（仅 insert 操作需要）
        conversation_id: 会话ID（用于记录操作日志）
        work_id: 作品ID（当 chapter_id 为序号时必需）

    Returns:
        执行结果
    """
    try:
        if not chapter_id:
            return json.dumps({"success": False, "error": "missing_chapter_id"}, ensure_ascii=False)

        if not new_content:
            return json.dumps({"success": False, "error": "empty_content"}, ensure_ascii=False)

        # v8.0: 智能解析 - 如果 new_content 是 JSON 格式，提取其中的 content 字段
        # 这解决了 Agent 把 smart_continue 返回的整个 JSON 传入的问题
        actual_content = new_content
        if new_content.strip().startswith('{'):
            try:
                parsed = json.loads(new_content)
                if isinstance(parsed, dict) and 'content' in parsed:
                    actual_content = parsed['content']
                    logger.info(f"[update_chapter_content] 从 JSON 中提取 content 字段，长度: {len(actual_content)}")
            except json.JSONDecodeError:
                pass  # 不是有效 JSON，使用原始内容

        from app.services.agent.langgraph_tools import resolve_chapter_id

        async with AsyncSessionLocal() as db:
            # v8.0: 支持章节序号自动转换为 UUID
            resolved_chapter_id = chapter_id
            if work_id and not chapter_id.count('-') == 4:  # 不是 UUID 格式
                resolved_id, error = await resolve_chapter_id(work_id, chapter_id, db)
                if error:
                    return error
                if resolved_id:
                    resolved_chapter_id = resolved_id
                    logger.info(f"[update_chapter_content] 章节序号 {chapter_id} -> UUID {resolved_chapter_id}")

            chapter_svc = ChapterService(db)
            chapter = await chapter_svc.get_chapter_by_id(resolved_chapter_id)

            if not chapter:
                return json.dumps({"success": False, "error": f"章节不存在: {chapter_id}"}, ensure_ascii=False)

            actual_work_id = str(chapter.work_id)
            chapter_title = chapter.title
            old_content = chapter.content or ""

            # 根据操作类型构建最终内容
            if operation == "append":
                final_content = old_content + actual_content
            elif operation == "insert" and position:
                pos = position.get("from", len(old_content))
                final_content = old_content[:pos] + actual_content + old_content[pos:]
            else:  # replace
                final_content = actual_content

            # 执行更新
            await chapter_svc.update_chapter(resolved_chapter_id, ChapterUpdate(content=final_content))

            # 记录操作日志（用于回滚）
            if conversation_id:
                op_log = _get_operation_log_manager()
                op_log.record_operation(
                    conversation_id=conversation_id,
                    op_id=str(uuid.uuid4()),
                    op_type="update_content",
                    chapter_id=resolved_chapter_id,
                    work_id=actual_work_id,
                    rollback_data={"old_content": old_content},
                    description=f"更新章节内容（{operation}）：{chapter_title}"
                )

            # 重新获取更新后的章节
            updated_chapter = await chapter_svc.get_chapter_by_id(resolved_chapter_id)

            operation_names = {
                "replace": "替换",
                "append": "追加",
                "insert": "插入"
            }

            return json.dumps({
                "success": True,
                "action_type": "update_content",
                "chapter_id": resolved_chapter_id,
                "work_id": actual_work_id,
                "chapter_title": chapter_title,
                "operation": operation,
                "word_count": updated_chapter.word_count if updated_chapter else 0,
                "description": f"已{operation_names.get(operation, operation)}章节内容：{chapter_title}（{len(actual_content)}字）"
            }, ensure_ascii=False)

    except Exception as e:
        logger.error(f"update_chapter_content failed: {e}")
        return json.dumps({"success": False, "error": str(e)}, ensure_ascii=False)


# ==================== 2026-01-10: StandardTool 包装版本 ====================
# 为章节管理工具创建 StandardTool 包装，以支持元数据驱动和执行监控

from .tool_types import ToolInput, ToolOutput, ToolCategory, StandardTool
from pydantic import Field


# ==================== 1. CreateChapter StandardTool ====================

class CreateChapterInput(ToolInput):
    """创建章节工具输入"""
    work_id: str = Field(..., description="作品ID")
    title: str = Field(..., description="章节标题")
    content: str = Field(default="", description="章节内容")
    order: Optional[int] = Field(default=None, description="章节顺序")
    conversation_id: Optional[str] = Field(default=None, description="会话ID（用于操作日志）")


class CreateChapterOutput(ToolOutput):
    """创建章节工具输出"""
    pass


async def create_chapter_executor(input_data: CreateChapterInput) -> CreateChapterOutput:
    """创建章节执行器"""
    try:
        result_str = await create_chapter.ainvoke({
            "work_id": input_data.work_id,
            "title": input_data.title,
            "content": input_data.content,
            "order": input_data.order,
            "conversation_id": input_data.conversation_id
        })
        result_data = json.loads(result_str) if isinstance(result_str, str) else result_str
        return CreateChapterOutput(
            success=result_data.get("success", True),
            message=result_data.get("description", "章节创建请求已提交"),
            data=result_data,
            metadata={"tool": "create_chapter"}
        )
    except Exception as e:
        logger.error(f"create_chapter_executor 失败: {e}")
        return CreateChapterOutput(
            success=False,
            message=f"创建章节失败: {str(e)}",
            data=None,
            metadata={"error": str(e)}
        )


create_chapter_tool = StandardTool(
    name="create_chapter",
    description="创建新章节（需要用户确认）",
    category=ToolCategory.OPERATION,
    input_schema=CreateChapterInput,
    output_schema=CreateChapterOutput,
    executor=create_chapter_executor,
    tags=["chapter", "create", "hitl"],
    version="1.0.0"
)


# ==================== 2. UpdateChapterTitle StandardTool ====================

class UpdateChapterTitleInput(ToolInput):
    """修改章节标题工具输入"""
    chapter_id: str = Field(..., description="章节ID（支持 UUID 或章节序号）")
    new_title: str = Field(..., description="新标题")
    old_title: Optional[str] = Field(default=None, description="原标题")
    work_id: Optional[str] = Field(default=None, description="作品ID（章节序号解析时必需）")
    conversation_id: Optional[str] = Field(default=None, description="会话ID（用于操作日志）")


class UpdateChapterTitleOutput(ToolOutput):
    """修改章节标题工具输出"""
    pass


async def update_chapter_title_executor(input_data: UpdateChapterTitleInput) -> UpdateChapterTitleOutput:
    """修改章节标题执行器"""
    try:
        result_str = await update_chapter_title.ainvoke({
            "chapter_id": input_data.chapter_id,
            "new_title": input_data.new_title,
            "old_title": input_data.old_title,
            "work_id": input_data.work_id,
            "conversation_id": input_data.conversation_id
        })
        result_data = json.loads(result_str) if isinstance(result_str, str) else result_str
        return UpdateChapterTitleOutput(
            success=result_data.get("success", True),
            message=result_data.get("description", "标题修改请求已提交"),
            data=result_data,
            metadata={"tool": "update_chapter_title"}
        )
    except Exception as e:
        logger.error(f"update_chapter_title_executor 失败: {e}")
        return UpdateChapterTitleOutput(
            success=False,
            message=f"修改标题失败: {str(e)}",
            data=None,
            metadata={"error": str(e)}
        )


update_chapter_title_tool = StandardTool(
    name="update_chapter_title",
    description="修改章节标题（需要用户确认）",
    category=ToolCategory.OPERATION,
    input_schema=UpdateChapterTitleInput,
    output_schema=UpdateChapterTitleOutput,
    executor=update_chapter_title_executor,
    tags=["chapter", "rename", "hitl"],
    version="1.0.0"
)


# ==================== 3. DeleteChapter StandardTool ====================

class DeleteChapterInput(ToolInput):
    """删除章节工具输入"""
    chapter_id: str = Field(..., description="章节ID（支持 UUID 或章节序号）")
    chapter_title: Optional[str] = Field(default=None, description="章节标题")
    work_id: Optional[str] = Field(default=None, description="作品ID（章节序号解析时必需）")
    conversation_id: Optional[str] = Field(default=None, description="会话ID（用于操作日志）")


class DeleteChapterOutput(ToolOutput):
    """删除章节工具输出"""
    pass


async def delete_chapter_executor(input_data: DeleteChapterInput) -> DeleteChapterOutput:
    """删除章节执行器"""
    try:
        result_str = await delete_chapter.ainvoke({
            "chapter_id": input_data.chapter_id,
            "chapter_title": input_data.chapter_title,
            "work_id": input_data.work_id,
            "conversation_id": input_data.conversation_id
        })
        result_data = json.loads(result_str) if isinstance(result_str, str) else result_str
        return DeleteChapterOutput(
            success=result_data.get("success", True),
            message=result_data.get("description", "删除请求已提交"),
            data=result_data,
            metadata={"tool": "delete_chapter"}
        )
    except Exception as e:
        logger.error(f"delete_chapter_executor 失败: {e}")
        return DeleteChapterOutput(
            success=False,
            message=f"删除章节失败: {str(e)}",
            data=None,
            metadata={"error": str(e)}
        )


delete_chapter_tool = StandardTool(
    name="delete_chapter",
    description="删除章节（需要用户确认）",
    category=ToolCategory.OPERATION,
    input_schema=DeleteChapterInput,
    output_schema=DeleteChapterOutput,
    executor=delete_chapter_executor,
    tags=["chapter", "delete", "hitl"],
    version="1.0.0"
)


# ==================== 4. UpdateChapterContent StandardTool ====================

class UpdateChapterContentInput(ToolInput):
    """修改章节内容工具输入"""
    chapter_id: str = Field(..., description="章节ID（支持 UUID 或章节序号）")
    new_content: str = Field(..., description="新内容")
    operation: str = Field(default="replace", description="操作类型：replace/append/insert")
    position: Optional[dict] = Field(default=None, description="位置信息")
    work_id: Optional[str] = Field(default=None, description="作品ID（章节序号解析时必需）")
    conversation_id: Optional[str] = Field(default=None, description="会话ID（用于操作日志）")


class UpdateChapterContentOutput(ToolOutput):
    """修改章节内容工具输出"""
    pass


async def update_chapter_content_executor(input_data: UpdateChapterContentInput) -> UpdateChapterContentOutput:
    """修改章节内容执行器"""
    try:
        result_str = await update_chapter_content.ainvoke({
            "chapter_id": input_data.chapter_id,
            "new_content": input_data.new_content,
            "operation": input_data.operation,
            "position": input_data.position,
            "work_id": input_data.work_id,
            "conversation_id": input_data.conversation_id
        })
        result_data = json.loads(result_str) if isinstance(result_str, str) else result_str
        return UpdateChapterContentOutput(
            success=result_data.get("success", True),
            message=result_data.get("description", "内容修改请求已提交"),
            data=result_data,
            metadata={"tool": "update_chapter_content"}
        )
    except Exception as e:
        logger.error(f"update_chapter_content_executor 失败: {e}")
        return UpdateChapterContentOutput(
            success=False,
            message=f"修改内容失败: {str(e)}",
            data=None,
            metadata={"error": str(e)}
        )


update_chapter_content_tool = StandardTool(
    name="update_chapter_content",
    description="直接修改章节内容（需要用户确认）",
    category=ToolCategory.OPERATION,
    input_schema=UpdateChapterContentInput,
    output_schema=UpdateChapterContentOutput,
    executor=update_chapter_content_executor,
    tags=["chapter", "content", "hitl"],
    version="1.0.0"
)
