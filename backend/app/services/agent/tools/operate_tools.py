# -*- coding: utf-8 -*-
"""
ContentOperator - Create 工具输出的统一接收者

注意：ContentOperator 是工具路由器/编排层，不是 SubAgent。
与 Explore SubAgent 不同，它没有独立的 AI 决策循环。

核心理念：用户调用 AI Agent 是为了让 AI 生成内容
所有需要 AI 的场景都是 Create → Operate 流程

职责：
1. 意图路由：根据 operation 选择底层工具和目标操作
2. 智能定位：仅 replace/insert 需要，支持 direct/text_match/semantic 三种方式
3. 执行操作：调用底层工具
4. 返回结果：包含 HITL 确认信息
"""
import json
import logging
from typing import Optional, Dict, Any, Tuple
from dataclasses import dataclass, asdict
from enum import Enum

from pydantic import Field
from langchain_core.tools import tool

from .tool_registry import register_as_tool
from .tool_types import ToolInput, ToolOutput, ToolCategory, StandardTool
from .locate_tools import locate_content
from .editor_tools import apply_chapter_edit
from .chapter_tools import create_chapter, update_chapter_title

logger = logging.getLogger(__name__)


class OperationType(str, Enum):
    """操作类型枚举（完整 6 种）"""
    APPEND = "append"    # 续写
    REPLACE = "replace"  # 改写
    INSERT = "insert"    # 插入
    CONTENT = "content"  # 整体替换（映射到 replace_all）
    CREATE = "create"    # 写新章节
    TITLE = "title"      # 改进标题


# ==================== 数据结构 ====================

@dataclass
class OperateResult:
    """操作结果"""
    success: bool
    message: str
    operation: str                            # 请求的操作类型
    target_operation: Optional[str] = None    # 实际执行的底层操作（如 content → replace_all）
    action_type: Optional[str] = None         # apply_chapter_edit 的 action_type
    chapter_id: Optional[str] = None
    chapter_title: Optional[str] = None
    tool_used: Optional[str] = None
    located: bool = False
    paragraph_index: Optional[int] = None
    node_id: Optional[str] = None
    locate_method: str = "none"
    requires_confirmation: bool = False
    revision_id: Optional[str] = None
    request_id: Optional[str] = None
    description: Optional[str] = None
    content: Optional[str] = None
    position: Optional[Dict[str, Any]] = None
    before_anchor: Optional[str] = None
    after_anchor: Optional[str] = None
    old_title: Optional[str] = None
    new_title: Optional[str] = None
    # 内容信息（文档要求）
    content_length: Optional[int] = None      # 写入内容长度
    original_text: Optional[str] = None       # 原文（replace 时）

    def to_dict(self) -> Dict[str, Any]:
        """转换为字典"""
        return asdict(self)

    def to_json(self) -> str:
        """转换为 JSON 字符串"""
        return json.dumps(asdict(self), ensure_ascii=False)


class ContentOperator:
    """
    ContentOperator 核心类

    三阶段流程：
    1. 意图路由：根据 operation 选择底层工具和目标操作
    2. 智能定位：仅 replace/insert 需要，支持 direct 直通
    3. 执行操作：调用底层工具
    """

    # 路由表：operation(字符串) -> (底层工具名, 底层operation, 是否需要定位)
    ROUTING_TABLE: Dict[str, Tuple[str, Optional[str], bool]] = {
        "append":  ("apply_chapter_edit", "append", False),
        "replace": ("apply_chapter_edit", "replace", True),
        "insert":  ("apply_chapter_edit", "insert", True),
        "content": ("apply_chapter_edit", "replace_all", False),
        "create":  ("create_chapter", None, False),
        "title":   ("update_chapter_title", None, False),
    }

    async def operate(
        self,
        operation: str,
        chapter_id: Optional[str] = None,
        work_id: Optional[str] = None,
        content: Optional[str] = None,
        title: Optional[str] = None,
        original_text: Optional[str] = None,
        target_description: Optional[str] = None,
        paragraph_index: Optional[int] = None,
        node_id: Optional[str] = None,
        nodes_info: Optional[str] = None,
        user_id: Optional[str] = None,
        conversation_id: Optional[str] = None,
        **kwargs
    ) -> OperateResult:
        """
        执行操作

        Args:
            operation: 操作类型 (append/replace/insert/content/create/title)
            chapter_id: 章节ID（create 时不需要）
            work_id: 作品ID（create 时必填）
            content: AI生成的内容
            title: AI生成的标题（create/title 时使用）
            original_text: 原文（replace 时用于 text_match 定位）
            target_description: 目标位置描述（insert 时用于 semantic 定位）
            paragraph_index: 段落索引（direct 定位，优先级最高）
            node_id: 节点ID（direct 定位，优先级最高）
            user_id: 用户ID
            conversation_id: 会话ID

        Returns:
            OperateResult
        """
        logger.info(f"[Operate] 开始: op={operation}, chapter={chapter_id}")

        # ═══════════════════════════════════════
        # 参数验证
        # ═══════════════════════════════════════
        if operation == "create":
            if not work_id:
                return OperateResult(
                    success=False,
                    message="create 操作需要提供 work_id",
                    operation=operation
                )
        elif operation == "title":
            if not chapter_id:
                return OperateResult(
                    success=False,
                    message="title 操作需要提供 chapter_id",
                    operation=operation
                )
            if not title:
                return OperateResult(
                    success=False,
                    message="title 操作需要提供 title 参数",
                    operation=operation
                )
        else:
            # append/replace/insert/content 都需要 chapter_id
            if not chapter_id:
                return OperateResult(
                    success=False,
                    message=f"{operation} 操作需要提供 chapter_id",
                    operation=operation
                )

        # ═══════════════════════════════════════
        # 阶段1：意图路由
        # ═══════════════════════════════════════
        tool_name, target_operation, needs_locate = self._route_operation(operation)
        logger.info(f"[Operate] 路由: tool={tool_name}, target_op={target_operation}, needs_locate={needs_locate}")

        # ═══════════════════════════════════════
        # 阶段2：智能定位（仅 replace/insert）
        # ═══════════════════════════════════════
        located_paragraph_index = paragraph_index
        located_node_id = node_id
        locate_method = "none"
        locate_before_anchor = None
        locate_after_anchor = None

        if needs_locate:
            locate_result = await self._smart_locate(
                chapter_id=chapter_id,
                operation=operation,
                original_text=original_text,
                target_description=target_description,
                paragraph_index=paragraph_index,
                node_id=node_id,
                nodes_info=nodes_info,
            )
            located_paragraph_index = locate_result.get("paragraph_index")
            located_node_id = locate_result.get("node_id")
            locate_method = locate_result.get("method", "none")
            locate_before_anchor = locate_result.get("before_anchor")
            locate_after_anchor = locate_result.get("after_anchor")

            if not locate_result.get("success"):
                if operation == "insert" and locate_result.get("fallback"):
                    logger.warning(f"[Operate] insert 定位失败，降级为 append")
                    target_operation = "append"
                    locate_method = "fallback"
                else:
                    return OperateResult(
                        success=False,
                        message=locate_result.get("message", "定位失败"),
                        operation=operation,
                        target_operation=target_operation,  # 记录原计划的目标操作
                        chapter_id=chapter_id,
                        tool_used=tool_name,
                        locate_method="failed"
                    )

            logger.info(f"[Operate] 定位完成: method={locate_method}, para={located_paragraph_index}")

        # ═══════════════════════════════════════
        # 阶段3：执行操作
        # ═══════════════════════════════════════
        try:
            result = await self._execute_operation(
                tool_name=tool_name,
                target_operation=target_operation,
                chapter_id=chapter_id,
                work_id=work_id,
                content=content,
                title=title,
                paragraph_index=located_paragraph_index,
                node_id=located_node_id,
                before_anchor=locate_before_anchor,
                after_anchor=locate_after_anchor,
                original_text=original_text,
                user_id=user_id,
                conversation_id=conversation_id,
            )

            action_type = result.get("action_type")
            description = result.get("description", result.get("message"))
            content_value = result.get("content") or result.get("new_content") or content
            position_value = result.get("position")
            before_anchor = result.get("before_anchor") or locate_before_anchor
            after_anchor = result.get("after_anchor") or locate_after_anchor

            return OperateResult(
                success=result.get("success", False),
                message=description or "操作完成",
                operation=operation,
                target_operation=target_operation,
                chapter_id=chapter_id or result.get("chapter_id"),
                chapter_title=result.get("chapter_title"),
                tool_used=tool_name,
                located=needs_locate,
                paragraph_index=result.get("paragraph_index", located_paragraph_index),
                node_id=result.get("node_id", located_node_id),
                locate_method=locate_method,
                requires_confirmation=result.get("requires_confirmation", False),
                revision_id=result.get("revision_id"),
                request_id=result.get("request_id"),
                action_type=action_type,
                description=description,
                content=content_value,
                position=position_value,
                before_anchor=before_anchor,
                after_anchor=after_anchor,
                old_title=result.get("old_title"),
                new_title=result.get("new_title"),
                content_length=len(content_value) if content_value else None,
                original_text=original_text or result.get("original_text"),
            )

        except Exception as e:
            logger.error(f"[Operate] 执行失败: {e}")
            return OperateResult(
                success=False,
                message=f"操作失败: {str(e)}",
                operation=operation,
                chapter_id=chapter_id,
                tool_used=tool_name,
                locate_method=locate_method
            )

    def _route_operation(self, operation: str) -> Tuple[str, Optional[str], bool]:
        """阶段1：意图路由"""
        return self.ROUTING_TABLE.get(
            operation,
            ("apply_chapter_edit", "append", False)
        )

    async def _smart_locate(
        self,
        chapter_id: Optional[str],
        operation: str,
        original_text: Optional[str],
        target_description: Optional[str],
        paragraph_index: Optional[int] = None,
        node_id: Optional[str] = None,
        nodes_info: Optional[str] = None,
    ) -> Dict[str, Any]:
        """阶段2：智能定位"""
        # 优先级1：DIRECT 定位
        if paragraph_index is not None or node_id is not None:
            logger.info(f"[Operate] 使用 DIRECT 定位: para={paragraph_index}, node={node_id}")
            return {
                "success": True,
                "paragraph_index": paragraph_index,
                "node_id": node_id,
                "method": "direct"
            }

        # 需要调用 locate_content 时，chapter_id 必须存在
        if not chapter_id:
            return {
                "success": False,
                "fallback": operation == "insert",
                "message": f"定位需要 chapter_id，但未提供"
            }

        # 优先级2/3：TEXT_MATCH / SEMANTIC
        query = None
        method = None

        if operation == "replace" and original_text:
            query = original_text[:200]
            method = "text_match"
        elif operation == "insert" and target_description:
            query = target_description
            method = "semantic"

        if not query:
            if operation == "insert":
                return {
                    "success": False,
                    "fallback": True,
                    "message": "insert 操作未提供定位信息，将降级为 append"
                }
            else:
                return {
                    "success": False,
                    "fallback": False,
                    "message": f"{operation} 操作需要提供定位信息（original_text）"
                }

        # 调用 locate_content
        try:
            locate_params = {
                "chapter_id": chapter_id,
                "query": query
            }
            if nodes_info is not None:
                if not isinstance(nodes_info, str):
                    nodes_info = json.dumps(nodes_info, ensure_ascii=False)
                locate_params["nodes_info"] = nodes_info
            result_str = await locate_content.ainvoke(locate_params)
            result = json.loads(result_str) if isinstance(result_str, str) else result_str

            if result.get("success"):
                return {
                    "success": True,
                    "paragraph_index": result.get("paragraph_index"),
                    "node_id": result.get("node_id"),
                    "before_anchor": result.get("before_anchor"),
                    "after_anchor": result.get("after_anchor"),
                    "method": method
                }
            else:
                if operation == "insert":
                    return {
                        "success": False,
                        "fallback": True,
                        "message": f"无法定位: {result.get('message', '未找到匹配内容')}，将降级为 append"
                    }
                else:
                    return {
                        "success": False,
                        "fallback": False,
                        "message": f"无法定位: {result.get('message', '未找到匹配内容')}"
                    }

        except Exception as e:
            logger.warning(f"[Operate] 定位调用失败: {e}")
            if operation == "insert":
                return {
                    "success": False,
                    "fallback": True,
                    "message": f"定位失败: {str(e)}，将降级为 append"
                }
            else:
                return {
                    "success": False,
                    "fallback": False,
                    "message": f"定位失败: {str(e)}"
                }

    async def _execute_operation(
        self,
        tool_name: str,
        target_operation: Optional[str],
        chapter_id: Optional[str],
        work_id: Optional[str],
        content: Optional[str],
        title: Optional[str],
        paragraph_index: Optional[int],
        node_id: Optional[str],
        before_anchor: Optional[str],
        after_anchor: Optional[str],
        original_text: Optional[str],
        user_id: Optional[str],
        conversation_id: Optional[str],
    ) -> Dict[str, Any]:
        """阶段3：执行操作"""
        if tool_name == "apply_chapter_edit":
            result_str = await apply_chapter_edit.ainvoke({
                "chapter_id": chapter_id,
                "content": content,
                "operation": target_operation,
                "paragraph_index": paragraph_index,
                "node_id": node_id,
                "before_anchor": before_anchor,
                "after_anchor": after_anchor,
                "original_text": original_text,
                "user_id": user_id,
                "conversation_id": conversation_id,
                "work_id": work_id,
            })
            return json.loads(result_str) if isinstance(result_str, str) else result_str

        elif tool_name == "create_chapter":
            result_str = await create_chapter.ainvoke({
                "work_id": work_id,
                "title": title or "新章节",
                "content": content or "",
                "conversation_id": conversation_id,
            })
            return json.loads(result_str) if isinstance(result_str, str) else result_str

        elif tool_name == "update_chapter_title":
            result_str = await update_chapter_title.ainvoke({
                "chapter_id": chapter_id,
                "new_title": title,
                "conversation_id": conversation_id,
                "work_id": work_id,
            })
            return json.loads(result_str) if isinstance(result_str, str) else result_str

        else:
            raise ValueError(f"未知工具: {tool_name}")


# ==================== 全局实例 ====================

_operator: Optional[ContentOperator] = None


def get_operator() -> ContentOperator:
    """获取全局 ContentOperator 实例"""
    global _operator
    if _operator is None:
        _operator = ContentOperator()
    return _operator


# ==================== operate_apply 工具 ====================

@tool
@register_as_tool(
    "operate_apply",
    "operation",
    """统一应用 AI 生成的内容到章节。

    这是 Create 工具输出的统一接收者，支持 6 种操作：
    - append: 续写（追加到章节末尾）
    - replace: 改写（替换指定段落）
    - insert: 插入（在指定位置插入）
    - content: 整章替换（替换整个章节内容）
    - create: 创建新章节
    - title: 修改标题

    【使用方式】
    1. 先用 smart_continue/smart_rewrite/smart_insert 生成内容
    2. 再用 operate_apply 将内容写入章节
    """
)
async def operate_apply(
    operation: str,
    chapter_id: Optional[str] = None,
    work_id: Optional[str] = None,
    content: Optional[str] = None,
    title: Optional[str] = None,
    original_text: Optional[str] = None,
    target_description: Optional[str] = None,
    paragraph_index: Optional[int] = None,
    node_id: Optional[str] = None,
    nodes_info: Optional[str] = None,
    user_id: Optional[str] = None,
    conversation_id: Optional[str] = None,
) -> str:
    """
    统一应用 AI 生成的内容

    Args:
        operation: 操作类型 (append/replace/insert/content/create/title)
        chapter_id: 章节ID（create 时不需要）
        work_id: 作品ID（create 时必填）
        content: AI生成的内容
        title: AI生成的标题（create/title 时使用）
        original_text: 原文（replace 时用于定位）
        target_description: 目标位置描述（insert 时用于语义定位）
        paragraph_index: 段落索引（优先级最高的定位方式）
        node_id: 节点ID（优先级最高的定位方式）
        user_id: 用户ID
        conversation_id: 会话ID

    Returns:
        JSON 格式的操作结果
    """
    operator = get_operator()
    result = await operator.operate(
        operation=operation,
        chapter_id=chapter_id,
        work_id=work_id,
        content=content,
        title=title,
        original_text=original_text,
        target_description=target_description,
        paragraph_index=paragraph_index,
        node_id=node_id,
        nodes_info=nodes_info,
        user_id=user_id,
        conversation_id=conversation_id,
    )
    return result.to_json()


# ==================== StandardTool 包装版本 ====================

class OperateApplyInput(ToolInput):
    """operate_apply 工具输入"""
    operation: str = Field(..., description="操作类型：append/replace/insert/content/create/title")
    chapter_id: Optional[str] = Field(default=None, description="章节ID（create 时不需要）")
    work_id: Optional[str] = Field(default=None, description="作品ID（create 时必填）")
    content: Optional[str] = Field(default=None, description="AI生成的内容")
    title: Optional[str] = Field(default=None, description="AI生成的标题（create/title 时使用）")
    original_text: Optional[str] = Field(default=None, description="原文（replace 时用于定位）")
    target_description: Optional[str] = Field(default=None, description="目标位置描述（insert 时用于语义定位）")
    paragraph_index: Optional[int] = Field(default=None, description="段落索引（优先级最高的定位方式）")
    node_id: Optional[str] = Field(default=None, description="节点ID（优先级最高的定位方式）")
    nodes_info: Optional[str] = Field(default=None, description="节点列表（可选，JSON字符串）")
    user_id: Optional[str] = Field(default=None, description="用户ID")
    conversation_id: Optional[str] = Field(default=None, description="会话ID")


class OperateApplyOutput(ToolOutput):
    """operate_apply 工具输出"""
    pass


async def operate_apply_executor(input_data: OperateApplyInput) -> OperateApplyOutput:
    """operate_apply 执行器"""
    try:
        result_str = await operate_apply.ainvoke({
            "operation": input_data.operation,
            "chapter_id": input_data.chapter_id,
            "work_id": input_data.work_id,
            "content": input_data.content,
            "title": input_data.title,
            "original_text": input_data.original_text,
            "target_description": input_data.target_description,
            "paragraph_index": input_data.paragraph_index,
            "node_id": input_data.node_id,
            "nodes_info": input_data.nodes_info,
            "user_id": input_data.user_id,
            "conversation_id": input_data.conversation_id,
        })

        result_data = json.loads(result_str) if isinstance(result_str, str) else result_str

        return OperateApplyOutput(
            success=result_data.get("success", False),
            message=result_data.get("message", "操作完成"),
            data=result_data,
            metadata={"tool": "operate_apply", "operation": input_data.operation}
        )
    except Exception as e:
        logger.error(f"operate_apply_executor 失败: {e}")
        return OperateApplyOutput(
            success=False,
            message=f"操作失败: {str(e)}",
            data=None,
            metadata={"error": str(e)}
        )


operate_apply_tool = StandardTool(
    name="operate_apply",
    description="统一应用 AI 生成的内容到章节（支持续写、改写、插入、整章替换、创建章节、修改标题）",
    category=ToolCategory.OPERATION,
    input_schema=OperateApplyInput,
    output_schema=OperateApplyOutput,
    executor=operate_apply_executor,
    tags=["editor", "operate", "hitl"],
    version="1.0.0"
)


# ==================== 导出 ====================

__all__ = [
    "ContentOperator",
    "OperationType",
    "OperateResult",
    "get_operator",
    "operate_apply",
    "operate_apply_tool",
]
