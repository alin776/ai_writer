"""
Agent编辑器工具 - 允许Agent直接修改编辑器内容

这些工具需要用户确认才能执行实际修改。

修复说明（2025-12-09）：
- 添加 LangChain @tool 装饰器，支持 .ainvoke() 方法调用
- 保留 @register_as_tool 用于自定义注册表兼容
"""
from typing import Dict, Any, Optional, List
from uuid import UUID
import logging
import asyncio
import json

from langchain_core.tools import tool
from .tool_registry import register_as_tool
from .position_inferrer import position_inferrer
from .tool_behaviors import creative_output_filter
from .style_adapter import style_adapter
from app.services.rate_limiter import agent_edit_limiter
from app.core.database import AsyncSessionLocal
from app.services.ai.http_ai_service import HTTPAIService
from app.services.agent.model_selector import TaskType

logger = logging.getLogger(__name__)

# AI服务实例（延迟初始化）
_ai_service: Optional[HTTPAIService] = None


def _get_ai_service() -> HTTPAIService:
    """获取AI服务实例"""
    global _ai_service
    if _ai_service is None:
        _ai_service = HTTPAIService()
    return _ai_service


async def _generate_rewrite_versions(
    original_text: str,
    chapter_content: str,
    user_requirement: Optional[str] = None,
    base_version: Optional[str] = None,
    num_versions: int = 3
) -> List[Dict[str, Any]]:
    """
    使用AI生成多个改写版本

    成本追踪：通过请求上下文自动获取user_id（无需显式传递参数）

    Args:
        original_text: 要改写的原文
        chapter_content: 章节完整内容（用于分析风格）
        user_requirement: 用户的具体要求（如"加强情感描写"、"更简洁一些"）
        base_version: 基准版本（如果用户要求"在第二版基础上改"，传入第二版内容）
        num_versions: 生成的版本数量

    Returns:
        改写版本列表，每个包含 style_name, reason, content
    """
    # ✅ 2025-12-01: 全局ai_service会自动从请求上下文获取user_id
    ai_service = _get_ai_service()

    # 🆕 双Prompt架构：从配置中读取
    from app.core.config import settings
    use_dual_prompt = settings.AGENT_USE_DUAL_PROMPT

    if use_dual_prompt:
        # === 阶段2：使用创作层Prompt（重量级，包含Few-Shot） ===
        try:
            from app.prompts import get_prompt_manager
            prompt_manager = get_prompt_manager()

            # 提取风格参考（前500字）
            style_reference = ""
            if chapter_content and len(chapter_content) > 100:
                import re
                text = re.sub(r'<[^>]+>', '', chapter_content)
                style_reference = text[:500]

            # 渲染创作层Prompt
            creative_prompt = prompt_manager.render(
                "creative_writing_prompt",
                task_type="rewrite",
                original_text=original_text,
                user_requirement=user_requirement or "",
                base_version=base_version or "",
                style_reference=style_reference,
                current_plot="",  # TODO: 如果有剧情状态可以传入
                character_context=""  # TODO: 如果有角色信息可以传入
            )

            # 添加JSON格式要求
            creative_prompt += f"""

【输出格式要求】
请严格按以下JSON格式返回（不要添加markdown代码块标记）：
[
  {{
    "style_name": "版本A",
    "reason": "简短说明这个版本的特点（8-15字）",
    "content": "改写后的内容"
  }},
  {{
    "style_name": "版本B",
    "reason": "简短说明这个版本的特点（8-15字）",
    "content": "改写后的内容"
  }},
  {{
    "style_name": "版本C",
    "reason": "简短说明这个版本的特点（8-15字）",
    "content": "改写后的内容"
  }}
]"""

            logger.info(f"[smart_rewrite] 使用创作层Prompt (双Prompt架构)")

            # 调用AI生成
            response_text = await ai_service.call_ai(
                system_prompt="你是资深网文作家，专注于高质量内容创作。",
                user_prompt=creative_prompt,
                max_tokens=4000,
                temperature=0.8,
                task_type=TaskType.CONTENT_CREATION
            )

        except Exception as e:
            logger.warning(f"[smart_rewrite] 创作层Prompt失败，回退到旧版本: {e}")
            use_dual_prompt = False

    if not use_dual_prompt:
        # === 原有单Prompt架构（备用方案） ===
        # 分析原文风格特点
        style_context = ""
        if chapter_content and len(chapter_content) > 100:
            # 取前500字作为风格参考
            style_context = f"\n\n【小说风格参考（前500字）】\n{chapter_content[:500]}"

        # 如果有基准版本，说明用户要迭代改进
        base_version_context = ""
        if base_version:
            base_version_context = f"\n\n【基准版本（用户要在此基础上改进）】\n{base_version}"

        # 如果有用户要求，添加到prompt
        user_requirement_context = ""
        if user_requirement:
            user_requirement_context = f"\n\n【用户的具体要求】\n{user_requirement}\n\n请严格按照用户的要求进行改写，3个版本都要体现用户的要求。"

        # 构建生成3个版本的prompt
        prompt = f"""你是专业的小说改写助手。任务：基于小说现有风格，生成3个改写版本。

【待改写的原文】
{original_text}
{style_context}
{base_version_context}
{user_requirement_context}

【改写要求】
1. **风格一致性**：改写必须与小说整体风格一致，不能改变文风
2. **字数控制**：与原文长度相差不超过30%
3. **不扩写**：只改写这部分内容，不要增加额外情节

【版本命名】
- 使用"版本A"、"版本B"、"版本C"这种中性命名
- 不要使用"细腻描写版"、"简洁明快版"等风格标签

【重要】：
- 如果用户提出了具体要求，3个版本都必须满足用户的要求，只是实现方式稍有不同
- 如果有基准版本，以基准版本为基础进行改进
- 如果没有用户要求，生成3个不同表达方式的版本，保持风格一致

请严格按以下JSON格式返回（不要添加markdown代码块标记）：
[
  {{
    "style_name": "版本A",
    "reason": "简短说明这个版本的特点（8-15字）",
    "content": "改写后的内容"
  }},
  {{
    "style_name": "版本B",
    "reason": "简短说明这个版本的特点（8-15字）",
    "content": "改写后的内容"
  }},
  {{
    "style_name": "版本C",
    "reason": "简短说明这个版本的特点（8-15字）",
    "content": "改写后的内容"
  }}
]"""

        logger.info(f"[smart_rewrite] 使用传统单Prompt架构")

        # 调用AI生成（使用call_ai非流式方法）
        response_text = await ai_service.call_ai(
            system_prompt="你是专业的小说改写助手。",
            user_prompt=prompt,
            max_tokens=4000,  # 需要足够的token来生成3个版本
            temperature=0.8,  # 稍高的温度以获得更多样化的结果
            task_type=TaskType.CONTENT_CREATION
        )

    # === 解析AI响应（两种架构共用） ===
    try:
        logger.info(f"[smart_rewrite] AI返回长度: {len(response_text)}")

        # 解析JSON
        import json
        import re

        # 尝试提取JSON部分
        json_match = re.search(r'\[[\s\S]*\]', response_text)
        if json_match:
            versions = json.loads(json_match.group())

            # 验证格式
            valid_versions = []
            for v in versions:
                if isinstance(v, dict) and "content" in v:
                    valid_versions.append({
                        "style_name": v.get("style_name", f"版本{len(valid_versions)+1}"),
                        "reason": v.get("reason", ""),
                        "content": v.get("content", "")
                    })

            if valid_versions:
                logger.info(f"[smart_rewrite] 成功生成{len(valid_versions)}个改写版本")
                return valid_versions

        # 解析失败，返回默认提示
        logger.warning(f"[smart_rewrite] JSON解析失败，返回默认版本")

    except Exception as e:
        logger.error(f"[smart_rewrite] AI生成失败: {e}", exc_info=True)

    # 失败时返回原文作为唯一版本
    return [{
        "style_name": "原文",
        "reason": "AI生成失败，显示原文",
        "content": original_text
    }]


@tool
@register_as_tool(
    "apply_chapter_edit",
    "operation",
    "将已有内容写入章节（只负责写入，不生成内容）。需要先用 smart_continue 生成内容，再调用此工具。"
)
async def apply_chapter_edit(
    chapter_id: str,
    content: str,
    operation: str = "append",
    position: Optional[int] = None,
    user_id: Optional[str] = None,
    description: Optional[str] = None
) -> str:
    """
    对章节执行编辑操作

    Args:
        chapter_id: 章节ID
        content: 要添加/替换的内容
        operation: 操作类型 ("append" | "replace" | "insert")
        position: 插入位置（仅insert操作需要）
        user_id: 用户ID
        description: 操作描述

    Returns:
        包含确认请求的结果
    """
    try:
        # 检查速率限制
        if user_id:
            is_allowed, remaining = await agent_edit_limiter.check(user_id)
            if not is_allowed:
                return json.dumps({
                    "success": False,
                    "error": "rate_limit_exceeded",
                    "message": f"操作过于频繁，请稍后再试。剩余配额将在1分钟后恢复。",
                    "retry_after": 60
                }, ensure_ascii=False)

        # 验证参数
        if not chapter_id:
            return json.dumps({"success": False, "error": "missing_chapter_id"}, ensure_ascii=False)

        if not content or not content.strip():
            return json.dumps({"success": False, "error": "empty_content"}, ensure_ascii=False)

        if operation not in ["append", "replace", "insert"]:
            return json.dumps({"success": False, "error": "invalid_operation"}, ensure_ascii=False)

        if operation == "insert" and position is None:
            return json.dumps({"success": False, "error": "missing_position_for_insert"}, ensure_ascii=False)

        # 返回需要用户确认的信息
        return json.dumps({
            "success": True,
            "requires_confirmation": True,
            "action_type": "edit",
            "chapter_id": chapter_id,
            "operation": operation,
            "content": content,
            "content_length": len(content),
            "position": position,
            "description": description or f"AI{_get_operation_name(operation)}：+{len(content)}字",
            "remaining_quota": remaining if user_id else None
        }, ensure_ascii=False)

    except Exception as e:
        logger.error(f"apply_chapter_edit failed: {e}")
        return json.dumps({"success": False, "error": str(e)}, ensure_ascii=False)


@tool
@register_as_tool(
    "smart_continue",
    "creative",
    "生成续写内容（只生成，不写入编辑器）。返回纯净的小说正文，由前端决定是否应用。"
)
async def smart_continue(
    chapter_id: str,
    chapter_content: Optional[str] = None,
    user_requirement: Optional[str] = None,
    word_count: int = 500,
    user_id: Optional[str] = None
) -> str:
    """
    智能续写 - 生成续写内容（不直接修改编辑器）

    Args:
        chapter_id: 章节ID
        chapter_content: 章节当前内容（用于上下文）
        user_requirement: 用户的续写要求
        word_count: 期望续写字数
        user_id: 用户ID

    Returns:
        生成的续写内容
    """
    try:
        # 如果没有提供章节内容，自动获取
        if not chapter_content and chapter_id:
            try:
                async with AsyncSessionLocal() as db:
                    from app.services.chapter_service import ChapterService
                    chapter_svc = ChapterService(db)
                    chapter = await chapter_svc.get_chapter_by_id(chapter_id)
                    if chapter and chapter.content:
                        chapter_content = chapter.content
            except Exception as e:
                logger.warning(f"[smart_continue] 获取章节内容失败: {e}")

        if not chapter_content:
            return json.dumps({
                "success": False,
                "error": "missing_content",
                "message": "缺少章节内容"
            }, ensure_ascii=False)

        # 使用AI生成续写内容
        ai_service = _get_ai_service()

        # 取最后1000字作为上下文
        context = chapter_content[-1000:] if len(chapter_content) > 1000 else chapter_content

        requirement_text = f"\n用户要求：{user_requirement}" if user_requirement else ""

        prompt = f"""你是专业的小说续写助手。请根据以下内容续写约{word_count}字。

【当前内容（最后部分）】
{context}
{requirement_text}

【续写要求】
1. 保持风格一致
2. 情节自然衔接
3. 约{word_count}字

请直接输出续写内容，不要添加任何解释。"""

        continued_content = await ai_service.call_ai(
            system_prompt="你是专业的小说续写助手。",
            user_prompt=prompt,
            max_tokens=word_count * 2,
            temperature=0.8,
            task_type=TaskType.CONTENT_CREATION
        )

        # CREATIVE 工具：应用输出过滤器，去除脏信息
        continued_content = creative_output_filter(continued_content)

        return json.dumps({
            "success": True,
            "action_type": "continue",
            "chapter_id": chapter_id,
            "content": continued_content,
            "content_length": len(continued_content),
            "description": f"AI续写：生成{len(continued_content)}字"
        }, ensure_ascii=False)

    except Exception as e:
        logger.error(f"smart_continue failed: {e}")
        return json.dumps({"success": False, "error": str(e)}, ensure_ascii=False)


@tool
@register_as_tool(
    "smart_rewrite",
    "creative",
    """生成改写版本（只生成，不写入编辑器）。返回3个改写版本供用户选择，由前端决定是否应用。

    【重要】此工具只生成内容，不会修改编辑器。

    【使用步骤】：
    1. 先用read_chapter_tool读取章节内容
    2. 定位用户提到的文本
    3. 调用本工具生成改写版本
    4. 用户在前端选择版本后，由前端应用到编辑器"""
)
async def smart_rewrite(
    chapter_id: str,
    text_to_rewrite: Optional[str] = None,
    chapter_content: Optional[str] = None,
    user_requirement: Optional[str] = None,
    base_version: Optional[str] = None,
    user_id: Optional[str] = None
) -> str:
    """
    智能改写 - 改写用户指定范围的文本

    成本追踪：优先使用请求上下文中的user_id，如果显式传递则使用传递的值

    Args:
        chapter_id: 章节ID
        text_to_rewrite: 要改写的文本。应该是从章节中提取的句子/段落，不要传入整章内容
        chapter_content: 章节完整内容（用于风格分析）
        user_requirement: 用户的具体要求（如"加强情感描写"、"更简洁"、"更有画面感"）
        base_version: 基准版本内容（用户要在此基础上改进）
        user_id: 用户ID（可选，优先从请求上下文获取）

    Returns:
        包含3个改写版本和确认请求的结果
    """
    try:
        # ✅ 2025-12-01: 优先从请求上下文获取user_id
        from app.core.request_context import get_request_user_id
        actual_user_id = user_id or get_request_user_id()

        # 检查速率限制
        if actual_user_id:
            is_allowed, remaining = await agent_edit_limiter.check(actual_user_id)
            if not is_allowed:
                return json.dumps({
                    "success": False,
                    "error": "rate_limit_exceeded",
                    "message": "操作过于频繁，请稍后再试。",
                    "retry_after": 60
                }, ensure_ascii=False)

        # ✅ P0-6修复：如果没有提供text_to_rewrite，自动获取章节内容
        if not text_to_rewrite and chapter_id:
            logger.info(f"[smart_rewrite] 未提供text_to_rewrite，自动获取章节内容: {chapter_id}")
            try:
                # 使用async with管理数据库连接
                async with AsyncSessionLocal() as db:
                    from app.services.chapter_service import ChapterService
                    chapter_svc = ChapterService(db)
                    chapter = await chapter_svc.get_chapter_by_id(chapter_id)
                    if chapter and chapter.content:
                        text_to_rewrite = chapter.content
                        chapter_content = chapter.content  # 同时用于风格分析
                        logger.info(f"[smart_rewrite] 自动获取章节内容成功，长度: {len(text_to_rewrite)}")
                    else:
                        return json.dumps({
                            "success": False,
                            "error": "chapter_not_found",
                            "message": f"无法获取章节内容: {chapter_id}"
                        }, ensure_ascii=False)
            except Exception as e:
                logger.error(f"[smart_rewrite] 获取章节内容失败: {e}")
                return json.dumps({
                    "success": False,
                    "error": "fetch_chapter_failed",
                    "message": f"获取章节内容失败: {str(e)}"
                }, ensure_ascii=False)

        # 验证text_to_rewrite
        if not text_to_rewrite:
            return json.dumps({
                "success": False,
                "error": "missing_content",
                "message": "缺少要改写的内容"
            }, ensure_ascii=False)

        # ✅ 使用AI生成3个实际的改写版本
        logger.info(f"[smart_rewrite] 开始生成改写版本，原文长度: {len(text_to_rewrite)}, 用户要求: {user_requirement}, 基准版本: {'有' if base_version else '无'}")
        # ✅ 2025-12-01: 成本追踪通过请求上下文自动完成，无需传递user_id
        versions = await _generate_rewrite_versions(
            original_text=text_to_rewrite,
            chapter_content=chapter_content or text_to_rewrite,
            user_requirement=user_requirement,
            base_version=base_version,
            num_versions=3
        )

        return json.dumps({
            "success": True,
            "action_type": "rewrite",
            "chapter_id": chapter_id,
            "original_text": text_to_rewrite,
            "versions": versions,
            "description": f"AI改写：{len(text_to_rewrite)}字 → 生成{len(versions)}个版本"
        }, ensure_ascii=False)

    except Exception as e:
        logger.error(f"smart_rewrite failed: {e}")
        return json.dumps({"success": False, "error": str(e)}, ensure_ascii=False)


@tool
@register_as_tool(
    "smart_insert",
    "creative",
    "生成插入内容（只生成，不写入编辑器）。返回生成的内容和推荐位置，由前端决定是否应用。"
)
async def smart_insert(
    chapter_id: str,
    user_intent: str,
    chapter_content: Optional[str] = None,
    insert_context: Optional[str] = None,
    word_count: int = 200,
    user_id: Optional[str] = None
) -> str:
    """
    智能插入 - 生成要插入的内容（不直接修改编辑器）

    Args:
        chapter_id: 章节ID
        user_intent: 用户的意图描述（如"在这里加一段心理描写"）
        chapter_content: 章节完整内容
        insert_context: 插入点附近的上下文
        word_count: 期望生成字数
        user_id: 用户ID

    Returns:
        生成的插入内容和位置推断
    """
    try:
        # 如果没有提供章节内容，自动获取
        if not chapter_content and chapter_id:
            try:
                async with AsyncSessionLocal() as db:
                    from app.services.chapter_service import ChapterService
                    chapter_svc = ChapterService(db)
                    chapter = await chapter_svc.get_chapter_by_id(chapter_id)
                    if chapter and chapter.content:
                        chapter_content = chapter.content
            except Exception as e:
                logger.warning(f"[smart_insert] 获取章节内容失败: {e}")

        # 使用AI生成插入内容
        ai_service = _get_ai_service()

        context_text = f"\n【插入点上下文】\n{insert_context}" if insert_context else ""

        prompt = f"""你是专业的小说创作助手。请根据用户意图生成约{word_count}字的内容。

【用户意图】
{user_intent}
{context_text}

【章节内容参考】
{chapter_content[:1500] if chapter_content and len(chapter_content) > 1500 else chapter_content or "无"}

【生成要求】
1. 符合用户意图
2. 与上下文风格一致
3. 约{word_count}字

请直接输出生成的内容，不要添加任何解释。"""

        generated_content = await ai_service.call_ai(
            system_prompt="你是专业的小说创作助手。",
            user_prompt=prompt,
            max_tokens=word_count * 2,
            temperature=0.8,
            task_type=TaskType.CONTENT_CREATION
        )

        # CREATIVE 工具：应用输出过滤器，去除脏信息
        generated_content = creative_output_filter(generated_content)

        # 推断插入位置
        position_result = {"position": "cursor", "confidence": 0.8, "reason": "根据用户意图"}
        if chapter_content:
            position_result = position_inferrer.infer_position(
                chapter_content=chapter_content,
                operation="insert",
                user_intent=user_intent,
                context={"insert_context": insert_context} if insert_context else None
            )

        return json.dumps({
            "success": True,
            "action_type": "insert",
            "chapter_id": chapter_id,
            "content": generated_content,
            "content_length": len(generated_content),
            "position_inference": position_result,
            "description": f"AI生成插入内容：{len(generated_content)}字"
        }, ensure_ascii=False)

    except Exception as e:
        logger.error(f"smart_insert failed: {e}")
        return json.dumps({"success": False, "error": str(e)}, ensure_ascii=False)


def _get_operation_name(operation: str) -> str:
    """获取操作的中文名称"""
    names = {
        "append": "续写",
        "replace": "替换",
        "insert": "插入"
    }
    return names.get(operation, operation)


def register_editor_tools():
    """注册所有编辑器工具"""
    logger.info("Registering editor tools...")
    tools = [
        "apply_chapter_edit",
        "smart_continue",
        "smart_rewrite",
        "smart_insert"
    ]
    for tool_name in tools:
        logger.info(f"  - {tool_name}")
    logger.info(f"Registered {len(tools)} editor tools")


# 模块加载时自动注册
register_editor_tools()


# ==================== 2025-12-14: StandardTool 包装版本 ====================
# 为编辑器工具创建 StandardTool 包装，以支持元数据驱动和执行监控

from .tool_types import ToolInput, ToolOutput, ToolCategory, StandardTool
from pydantic import Field


# ==================== 1. SmartRewrite StandardTool ====================

class SmartRewriteInput(ToolInput):
    """智能改写工具输入"""
    chapter_id: str = Field(..., description="章节ID")
    text_to_rewrite: Optional[str] = Field(default=None, description="要改写的文本")
    chapter_content: Optional[str] = Field(default=None, description="章节完整内容")
    user_requirement: Optional[str] = Field(default=None, description="用户的具体要求")
    base_version: Optional[str] = Field(default=None, description="基准版本内容")
    user_id: Optional[str] = Field(default=None, description="用户ID")


class SmartRewriteOutput(ToolOutput):
    """智能改写工具输出"""
    pass


async def smart_rewrite_executor(input_data: SmartRewriteInput) -> SmartRewriteOutput:
    """智能改写执行器（包装 @tool 版本）"""
    try:
        # 🔧 2025-12-14: @tool 装饰器返回 StructuredTool，需要用 .ainvoke() 调用
        result_str = await smart_rewrite.ainvoke({
            "chapter_id": input_data.chapter_id,
            "text_to_rewrite": input_data.text_to_rewrite,
            "chapter_content": input_data.chapter_content,
            "user_requirement": input_data.user_requirement,
            "base_version": input_data.base_version,
            "user_id": input_data.user_id
        })

        # 解析返回的 JSON
        import json
        result_data = json.loads(result_str) if isinstance(result_str, str) else result_str

        return SmartRewriteOutput(
            success=result_data.get("success", True),
            message=result_data.get("description", "改写完成"),
            data=result_data,
            metadata={"tool": "smart_rewrite"}
        )
    except Exception as e:
        logger.error(f"smart_rewrite_executor 失败: {e}")
        return SmartRewriteOutput(
            success=False,
            message=f"改写失败: {str(e)}",
            data=None,
            metadata={"error": str(e)}
        )


smart_rewrite_tool = StandardTool(
    name="smart_rewrite",
    description="智能改写章节文本，生成3个版本供用户选择",
    category=ToolCategory.CREATIVE,  # 修正：CREATIVE 而非 WRITING
    input_schema=SmartRewriteInput,
    output_schema=SmartRewriteOutput,
    executor=smart_rewrite_executor,
    tags=["editor", "rewrite", "hitl"],
    version="1.0.0"
)


# ==================== 2. SmartContinue StandardTool ====================

class SmartContinueInput(ToolInput):
    """智能续写工具输入"""
    chapter_id: str = Field(..., description="章节ID")
    chapter_content: Optional[str] = Field(default=None, description="章节当前内容")
    user_requirement: Optional[str] = Field(default=None, description="用户的续写要求")
    word_count: int = Field(default=500, description="期望续写字数")
    user_id: Optional[str] = Field(default=None, description="用户ID")


class SmartContinueOutput(ToolOutput):
    """智能续写工具输出"""
    pass


async def smart_continue_executor(input_data: SmartContinueInput) -> SmartContinueOutput:
    """智能续写执行器（包装 @tool 版本）"""
    try:
        # 🔧 2026-01-09: 更新参数以匹配新的 smart_continue 签名
        result_str = await smart_continue.ainvoke({
            "chapter_id": input_data.chapter_id,
            "chapter_content": input_data.chapter_content,
            "user_requirement": input_data.user_requirement,
            "word_count": input_data.word_count,
            "user_id": input_data.user_id
        })

        result_data = json.loads(result_str) if isinstance(result_str, str) else result_str

        return SmartContinueOutput(
            success=result_data.get("success", True),
            message=result_data.get("description", "续写完成"),
            data=result_data,
            metadata={"tool": "smart_continue"}
        )
    except Exception as e:
        logger.error(f"smart_continue_executor 失败: {e}")
        return SmartContinueOutput(
            success=False,
            message=f"续写失败: {str(e)}",
            data=None,
            metadata={"error": str(e)}
        )


smart_continue_tool = StandardTool(
    name="smart_continue",
    description="智能续写章节内容，根据上下文生成续写内容",
    category=ToolCategory.CREATIVE,  # 修正：CREATIVE 而非 WRITING
    input_schema=SmartContinueInput,
    output_schema=SmartContinueOutput,
    executor=smart_continue_executor,
    tags=["editor", "continue", "creative"],
    version="2.0.0"
)


# ==================== 3. SmartInsert StandardTool ====================

class SmartInsertInput(ToolInput):
    """智能插入工具输入"""
    chapter_id: str = Field(..., description="章节ID")
    user_intent: str = Field(..., description="用户的意图描述")
    chapter_content: Optional[str] = Field(default=None, description="章节完整内容")
    insert_context: Optional[str] = Field(default=None, description="插入点附近的上下文")
    word_count: int = Field(default=200, description="期望生成字数")
    user_id: Optional[str] = Field(default=None, description="用户ID")


class SmartInsertOutput(ToolOutput):
    """智能插入工具输出"""
    pass


async def smart_insert_executor(input_data: SmartInsertInput) -> SmartInsertOutput:
    """智能插入执行器（包装 @tool 版本）"""
    try:
        # 🔧 2026-01-09: 更新参数以匹配新的 smart_insert 签名
        result_str = await smart_insert.ainvoke({
            "chapter_id": input_data.chapter_id,
            "user_intent": input_data.user_intent,
            "chapter_content": input_data.chapter_content,
            "insert_context": input_data.insert_context,
            "word_count": input_data.word_count,
            "user_id": input_data.user_id
        })

        result_data = json.loads(result_str) if isinstance(result_str, str) else result_str

        return SmartInsertOutput(
            success=result_data.get("success", True),
            message=result_data.get("description", "插入完成"),
            data=result_data,
            metadata={"tool": "smart_insert"}
        )
    except Exception as e:
        logger.error(f"smart_insert_executor 失败: {e}")
        return SmartInsertOutput(
            success=False,
            message=f"插入失败: {str(e)}",
            data=None,
            metadata={"error": str(e)}
        )


smart_insert_tool = StandardTool(
    name="smart_insert",
    description="智能插入内容，根据用户意图生成内容并推断最佳插入位置",
    category=ToolCategory.CREATIVE,  # 修正：CREATIVE 而非 WRITING
    input_schema=SmartInsertInput,
    output_schema=SmartInsertOutput,
    executor=smart_insert_executor,
    tags=["editor", "insert", "creative"],
    version="2.0.0"
)


# ==================== 4. ApplyChapterEdit StandardTool ====================

class ApplyChapterEditInput(ToolInput):
    """章节编辑应用工具输入"""
    chapter_id: str = Field(..., description="章节ID")
    content: str = Field(..., description="编辑内容")
    operation: str = Field(default="append", description="操作类型：append/replace/insert", pattern="^(append|replace|insert)$")
    position: Optional[int] = Field(default=None, description="插入位置（仅 insert 操作）")
    user_id: Optional[str] = Field(default=None, description="用户ID")
    description: Optional[str] = Field(default=None, description="操作描述")


class ApplyChapterEditOutput(ToolOutput):
    """章节编辑应用工具输出"""
    pass


async def apply_chapter_edit_executor(input_data: ApplyChapterEditInput) -> ApplyChapterEditOutput:
    """章节编辑应用执行器（包装 @tool 版本）"""
    try:
        # 🔧 2025-12-14: @tool 装饰器返回 StructuredTool，需要用 .ainvoke() 调用
        result_str = await apply_chapter_edit.ainvoke({
            "chapter_id": input_data.chapter_id,
            "content": input_data.content,
            "operation": input_data.operation,
            "position": input_data.position,
            "user_id": input_data.user_id,
            "description": input_data.description
        })

        result_data = json.loads(result_str) if isinstance(result_str, str) else result_str

        return ApplyChapterEditOutput(
            success=result_data.get("success", True),
            message=result_data.get("message", "编辑已应用"),
            data=result_data,
            metadata={"tool": "apply_chapter_edit", "operation": input_data.operation}
        )
    except Exception as e:
        logger.error(f"apply_chapter_edit_executor 失败: {e}")
        return ApplyChapterEditOutput(
            success=False,
            message=f"编辑应用失败: {str(e)}",
            data=None,
            metadata={"error": str(e)}
        )


apply_chapter_edit_tool = StandardTool(
    name="apply_chapter_edit",
    description="将已生成的内容写入章节（不生成内容，只负责写入）。需要先用 smart_continue/smart_rewrite 生成内容，再用此工具写入。",
    category=ToolCategory.OPERATION,  # 修正：OPERATION（需要HITL确认）
    input_schema=ApplyChapterEditInput,
    output_schema=ApplyChapterEditOutput,
    executor=apply_chapter_edit_executor,
    tags=["editor", "edit", "hitl"],
    version="1.0.0"
)


# ==================== 导出 StandardTool 版本 ====================

__all__ = [
    "apply_chapter_edit",
    "smart_continue",
    "smart_rewrite",
    "smart_insert",
    # StandardTool 版本
    "smart_rewrite_tool",
    "smart_continue_tool",
    "smart_insert_tool",
    "apply_chapter_edit_tool",
]
