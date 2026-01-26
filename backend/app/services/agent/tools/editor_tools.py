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
import re
import uuid
import redis

from langchain_core.tools import tool
from .tool_registry import register_as_tool
from .position_inferrer import position_inferrer
from .tool_behaviors import creative_output_filter
from .style_adapter import style_adapter
from app.services.rate_limiter import agent_edit_limiter
from app.core.database import AsyncSessionLocal
from app.services.ai.http_ai_service import HTTPAIService
from app.services.agent.model_selector import TaskType
from app.services.agent.tools.operation_log import OperationLogManager

logger = logging.getLogger(__name__)

# AI服务实例（延迟初始化）
_ai_service: Optional[HTTPAIService] = None

# Global Redis pool for operation logs
_operation_redis_pool = None


def _get_operation_log_manager() -> OperationLogManager:
    """Get operation log manager with a shared Redis connection pool."""
    global _operation_redis_pool
    if _operation_redis_pool is None:
        _operation_redis_pool = redis.ConnectionPool(
            host='localhost', port=6379, db=1,
            decode_responses=False, max_connections=10
        )
    return OperationLogManager(redis.Redis(connection_pool=_operation_redis_pool))


def _get_ai_service() -> HTTPAIService:
    """获取AI服务实例"""
    global _ai_service
    if _ai_service is None:
        _ai_service = HTTPAIService()
    return _ai_service


async def _generate_rewrite_versions(
    original_text: str,
    chapter_content: str,
    user_requirement: Optional[str] = None
) -> List[Dict[str, Any]]:
    """
    使用AI生成单个改写结果

    成本追踪：通过请求上下文自动获取user_id（无需显式传递参数）

    Args:
        original_text: 要改写的原文
        chapter_content: 章节完整内容（用于分析风格）
        user_requirement: 用户的具体要求（如"加强情感描写"、"更简洁一些"）
        返回单个改写版本

    Returns:
        改写结果列表（仅 1 条），每个包含 style_name, reason, content
    """
    # ✅ 2025-12-01: 全局ai_service会自动从请求上下文获取user_id
    ai_service = _get_ai_service()

    # 🆕 双Prompt架构：从配置中读取
    from app.core.config import settings
    use_dual_prompt = settings.AGENT_USE_DUAL_PROMPT

    response_text = ""
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
    "style_name": "改写内容",
    "reason": "简短说明改写要点（8-15字）",
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

        # 如果有用户要求，添加到prompt
        user_requirement_context = ""
        if user_requirement:
            user_requirement_context = f"\n\n【用户的具体要求】\n{user_requirement}\n\n请严格按照用户的要求进行改写。"

        # 构建单版本改写的 prompt
        prompt = f"""你是专业的小说改写助手。任务：基于小说现有风格，生成1个改写结果。

【待改写的原文】
{original_text}
{style_context}
{user_requirement_context}

【改写要求】
1. **风格一致性**：改写必须与小说整体风格一致，不能改变文风
2. **字数控制**：与原文长度相差不超过30%
3. **不扩写**：只改写这部分内容，不要增加额外情节

【重要】：
- 如果用户提出了具体要求，必须满足用户的要求
- 不要输出编号/版本列表，不要添加解释性文字

请严格按以下JSON格式返回（不要添加markdown代码块标记）：
[
  {{
    "style_name": "改写内容",
    "reason": "简短说明改写要点（8-15字）",
    "content": "改写后的内容"
  }}
]"""

        logger.info(f"[smart_rewrite] 使用传统单Prompt架构")

        # 调用AI生成（使用call_ai非流式方法）
        response_text = await ai_service.call_ai(
            system_prompt="你是专业的小说改写助手。",
            user_prompt=prompt,
            max_tokens=4000,  # 需要足够的token来生成改写内容
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
                        "style_name": v.get("style_name", "改写内容"),
                        "reason": v.get("reason", ""),
                        "content": v.get("content", "")
                    })

            if valid_versions:
                logger.info(f"[smart_rewrite] 成功生成{len(valid_versions)}条改写结果")
                return valid_versions[:1]

        # 尝试解析单个JSON对象
        obj_match = re.search(r'\{[\s\S]*\}', response_text)
        if obj_match:
            obj = json.loads(obj_match.group())
            if isinstance(obj, dict) and obj.get("content"):
                return [{
                    "style_name": obj.get("style_name", "改写内容"),
                    "reason": obj.get("reason", ""),
                    "content": obj.get("content", "")
                }]

        # 解析失败，返回默认提示
        logger.warning(f"[smart_rewrite] JSON解析失败，返回默认版本")

    except Exception as e:
        logger.error(f"[smart_rewrite] AI生成失败: {e}", exc_info=True)

    # 失败时返回原文作为唯一版本
    candidates = _extract_numbered_candidates(response_text if isinstance(response_text, str) else "")
    if candidates:
        return [{
            "style_name": "改写内容",
            "reason": "",
            "content": candidates[0]
        }]
    fallback_text = response_text.strip() if isinstance(response_text, str) else ""
    return [{
        "style_name": "改写内容",
        "reason": "AI解析失败，返回原文",
        "content": fallback_text or original_text
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
    before_anchor: Optional[str] = None,
    after_anchor: Optional[str] = None,
    original_text: Optional[str] = None,  # 🆕 原文（用于前端定位）
    node_id: Optional[str] = None,  # 🆕 节点ID（最高优先级定位）
    paragraph_index: Optional[int] = None,  # 🆕 段落索引（从 locate_content 获取）
    user_id: Optional[str] = None,
    description: Optional[str] = None,
    conversation_id: Optional[str] = None,
    work_id: Optional[str] = None
) -> str:
    """
    对章节执行编辑操作

    Args:
        chapter_id: 章节ID
        content: 要添加/替换的内容
        operation: 操作类型 ("append" | "replace" | "insert")
        position: 插入位置（仅insert操作需要）
        before_anchor: 插入点前面的文本（用于精确定位）
        after_anchor: 插入点后面的文本（用于精确定位）
        original_text: 原文（用于前端定位，replace 操作时传递）
        node_id: 节点ID（最高优先级定位，从 locate_content 获取）
        paragraph_index: 段落索引（从 locate_content 获取，用于映射到 node_id）
        user_id: 用户ID
        description: 操作描述

    Returns:
        包含确认请求的结果
    """
    try:
        # 🔧 2026-01-13: 添加调试日志
        logger.info(f"[apply_chapter_edit] 参数: chapter_id={chapter_id}, operation={operation}, content_len={len(content) if content else 0}")

        # 🔧 2026-01-11: 防御性类型转换 - 确保 paragraph_index 是整数或 None
        if paragraph_index is not None:
            try:
                paragraph_index = int(paragraph_index)
            except (ValueError, TypeError):
                logger.warning(f"[apply_chapter_edit] paragraph_index 类型转换失败: {paragraph_index}")
                paragraph_index = None

        if node_id and len(str(node_id)) > 64:
            logger.warning(f"[apply_chapter_edit] node_id 超长({len(str(node_id))})，已清空")
            node_id = None

        # 🔧 2026-01-11: 防御性处理 - position 参数语义解析
        # LLM 可能误传字符串如 "before"、"after"，尝试解析语义
        if position is not None:
            if isinstance(position, str):
                pos_lower = position.lower().strip()
                # 尝试解析语义，设置 paragraph_index
                if pos_lower in ["before", "start", "开头", "前面", "beginning"]:
                    if paragraph_index is None:
                        paragraph_index = 0
                    logger.info(f"[apply_chapter_edit] position='{position}' 解析为 paragraph_index=0")
                elif pos_lower in ["after", "end", "结尾", "后面", "ending"]:
                    if paragraph_index is None:
                        paragraph_index = -1  # -1 表示最后
                    logger.info(f"[apply_chapter_edit] position='{position}' 解析为 paragraph_index=-1")
                else:
                    logger.warning(f"[apply_chapter_edit] position 收到无法解析的字符串: {position}")
                position = None
            elif not isinstance(position, int):
                try:
                    position = int(position)
                except (ValueError, TypeError):
                    logger.warning(f"[apply_chapter_edit] position 类型转换失败: {position}")
                    position = None

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

        if operation not in ["append", "replace", "insert", "replace_all"]:
            return json.dumps({"success": False, "error": "invalid_operation"}, ensure_ascii=False)

        # insert 操作需要位置信息（position 或 锚点）
        if (
            operation == "insert"
            and position is None
            and not before_anchor
            and not after_anchor
            and not node_id
            and paragraph_index is None
        ):
            return json.dumps({"success": False, "error": "missing_position_for_insert"}, ensure_ascii=False)

        async with AsyncSessionLocal() as db:
            from app.services.chapter_service import ChapterService
            from app.services.agent.langgraph_tools import resolve_chapter_id

            resolved_chapter_id = chapter_id
            if work_id and not chapter_id.count('-') == 4:
                resolved_id, error = await resolve_chapter_id(work_id, chapter_id, db)
                if error:
                    return error
                if resolved_id:
                    resolved_chapter_id = resolved_id

            chapter_svc = ChapterService(db)
            chapter = await chapter_svc.get_chapter_by_id(resolved_chapter_id)
            if not chapter:
                return json.dumps({"success": False, "error": f"chapter_not_found: {chapter_id}"}, ensure_ascii=False)

            old_content = chapter.content or ""

            # 🔧 2026-01-11: 处理 paragraph_index = -1（表示最后一段）
            if paragraph_index == -1 and old_content:
                if '<p' in old_content or '<li' in old_content:
                    pattern = r'<(p|h[1-6]|blockquote|pre|li)[^>]*>(.*?)</\1>'
                    matches = re.findall(pattern, old_content, re.DOTALL | re.IGNORECASE)
                    paragraph_index = len(matches) - 1 if matches else 0
                else:
                    paragraphs = [p.strip() for p in re.split(r'\n\n+|\n', old_content) if p.strip()]
                    paragraph_index = len(paragraphs) - 1 if paragraphs else 0
                logger.info(f"[apply_chapter_edit] paragraph_index=-1 转换为实际索引: {paragraph_index}")

            # 🔧 2026-01-12: 兜底逻辑 - 如果没有定位信息但有 original_text，自动调用 locate_content
            if original_text and not node_id and paragraph_index is None and operation == "replace":
                try:
                    from .locate_tools import locate_content
                    locate_result_str = await locate_content.ainvoke({
                        "chapter_id": resolved_chapter_id,
                        "query": original_text[:100]  # 使用原文前100字作为查询
                    })
                    locate_result = json.loads(locate_result_str) if isinstance(locate_result_str, str) else locate_result_str
                    if locate_result.get("success") and locate_result.get("paragraph_index") is not None:
                        paragraph_index = locate_result["paragraph_index"]
                        node_id = locate_result.get("node_id")
                        before_anchor = before_anchor or locate_result.get("before_anchor")
                        after_anchor = after_anchor or locate_result.get("after_anchor")
                        logger.info(f"[apply_chapter_edit] 自动定位成功: paragraph_index={paragraph_index}, node_id={node_id}")
                except Exception as e:
                    logger.warning(f"[apply_chapter_edit] 自动定位失败: {e}")

            actual_content = content
            if isinstance(actual_content, str) and actual_content.strip().startswith('{'):
                try:
                    parsed = json.loads(actual_content)
                    if isinstance(parsed, dict) and "content" in parsed:
                        actual_content = parsed["content"]
                except json.JSONDecodeError:
                    pass

            if not actual_content or not str(actual_content).strip():
                return json.dumps({"success": False, "error": "empty_content"}, ensure_ascii=False)

            def _replace_by_node_id(raw: str, target_id: str, replacement: str):
                if not target_id:
                    return None
                pattern = rf'(<(p|h[1-6]|blockquote|pre|li)[^>]*\sdata-id=["\']{re.escape(target_id)}["\'][^>]*>)(.*?)(</\2>)'
                match = re.search(pattern, raw, re.DOTALL | re.IGNORECASE)
                if not match:
                    return None
                return raw[:match.start(3)] + replacement + raw[match.end(3):]

            def _insert_after_node_id(raw: str, target_id: str, insertion: str):
                if not target_id:
                    return None
                pattern = rf'(<(p|h[1-6]|blockquote|pre|li)[^>]*\sdata-id=["\']{re.escape(target_id)}["\'][^>]*>.*?</\2>)'
                match = re.search(pattern, raw, re.DOTALL | re.IGNORECASE)
                if not match:
                    return None
                insert_at = match.end(1)
                return raw[:insert_at] + insertion + raw[insert_at:]

            def _get_paragraph_text(raw: str, idx: int):
                if idx is None or idx < 0:
                    return None
                if '<p' in raw or '<li' in raw:
                    pattern = r'<(p|h[1-6]|blockquote|pre|li)[^>]*>(.*?)</\1>'
                    matches = re.findall(pattern, raw, re.DOTALL | re.IGNORECASE)
                    if 0 <= idx < len(matches):
                        inner_html = matches[idx][1]
                        text_value = re.sub(r'<[^>]+>', '', inner_html).strip()
                        return text_value or None
                    return None
                paragraphs = [p.strip() for p in re.split(r'\n\n+|\n', raw) if p.strip()]
                if 0 <= idx < len(paragraphs):
                    return paragraphs[idx]
                return None

            def _get_paragraph_position(raw: str, idx: int, position_type: str = "end"):
                """
                返回第 idx 个段落在 HTML 中的精确位置（避免 find() 命中重复文本）

                Args:
                    raw: HTML 内容
                    idx: 段落索引（0-based）
                    position_type:
                        "start" - 整个段落块开始（<p 前）
                        "end" - 整个段落块结束（</p> 后）
                        "inner_start" - 内部内容开始（<p...> 后）
                        "inner_end" - 内部内容结束（</p> 前）

                Returns:
                    位置索引，或 None
                """
                if idx is None or idx < 0:
                    return None
                if '<p' in raw or '<li' in raw:
                    # 捕获组: (1)标签名 (2)整个开始标签 (3)内部内容
                    pattern = r'(<(p|h[1-6]|blockquote|pre|li)[^>]*>)(.*?)(</\2>)'
                    matches = list(re.finditer(pattern, raw, re.DOTALL | re.IGNORECASE))
                    if 0 <= idx < len(matches):
                        match = matches[idx]
                        if position_type == "start":
                            return match.start()
                        elif position_type == "end":
                            return match.end()
                        elif position_type == "inner_start":
                            return match.start() + len(match.group(1))  # <p...> 后
                        elif position_type == "inner_end":
                            return match.end() - len(match.group(4))    # </p> 前
                    return None
                # 纯文本模式：按非空行分割
                paragraphs = list(re.finditer(r'[^\n]+', raw))
                if 0 <= idx < len(paragraphs):
                    match = paragraphs[idx]
                    return match.end() if position_type in ("end", "inner_end") else match.start()
                return None

            if operation == "append" and old_content.endswith(actual_content):
                return json.dumps({
                    "success": True,
                    "requires_confirmation": False,
                    "action_type": "update_content",
                    "chapter_id": resolved_chapter_id,
                    "work_id": str(chapter.work_id),
                    "operation": operation,
                    "no_change": True,
                    "description": description or "append already applied"
                }, ensure_ascii=False)

            new_content = None
            insert_pos = None

            # replace_all: 整体替换章节内容（不需要定位）
            if operation == "replace_all":
                new_content = actual_content

            elif operation == "append":
                new_content = old_content + actual_content

            elif operation == "insert":
                insert_pos = position
                if isinstance(insert_pos, dict):
                    insert_pos = insert_pos.get("from") or insert_pos.get("to")
                if insert_pos is None and node_id:
                    inserted = _insert_after_node_id(old_content, node_id, actual_content)
                    if inserted is not None:
                        new_content = inserted
                if new_content is None and insert_pos is None and paragraph_index is not None:
                    # 🔧 修复：在段落块后插入新段落，避免 find() 命中重复文本
                    insert_pos = _get_paragraph_position(old_content, paragraph_index, "end")
                    if insert_pos is not None:
                        logger.debug(f"[apply_chapter_edit] insert 按段落索引定位: para_index={paragraph_index}, pos={insert_pos}")
                    else:
                        logger.warning(f"[apply_chapter_edit] insert 段落索引定位失败: para_index={paragraph_index}")
                if new_content is None and insert_pos is None and (before_anchor or after_anchor):
                    inferred = position_inferrer.find_by_anchors(
                        content=old_content,
                        before_anchor=before_anchor,
                        after_anchor=after_anchor,
                        fallback="end"
                    )
                    insert_pos = inferred.get("position")
                if new_content is None:
                    if insert_pos is None:
                        insert_pos = len(old_content)
                    if isinstance(insert_pos, int) and 0 <= insert_pos <= len(old_content):
                        # 🔧 先计算要插入的内容（可能需要包装）
                        content_to_insert = actual_content
                        is_html_context = bool(re.search(r'<(p|h[1-6]|blockquote|pre|li|ul|ol)\b', old_content, re.IGNORECASE))
                        # 识别所有块级元素（p, h1-h6, blockquote, pre, li, ul, ol）
                        is_already_html = bool(re.match(r'^\s*<(p|h[1-6]|blockquote|pre|li|ul|ol)\b', actual_content, re.IGNORECASE))
                        if is_html_context and not is_already_html:
                            content_to_insert = f"<p>{actual_content}</p>"
                            logger.debug(f"[apply_chapter_edit] insert 包装纯文本为段落标签")

                        # 🔧 去重检查（同时检查包装后和原始内容）
                        if old_content[insert_pos:insert_pos + len(content_to_insert)] == content_to_insert:
                            return json.dumps({
                                "success": True,
                                "requires_confirmation": False,
                                "action_type": "update_content",
                                "chapter_id": resolved_chapter_id,
                                "work_id": str(chapter.work_id),
                                "operation": operation,
                                "no_change": True,
                                "description": description or "insert already applied"
                            }, ensure_ascii=False)
                        # 也检查原始内容（兼容未包装的情况）
                        if content_to_insert != actual_content and old_content[insert_pos:insert_pos + len(actual_content)] == actual_content:
                            return json.dumps({
                                "success": True,
                                "requires_confirmation": False,
                                "action_type": "update_content",
                                "chapter_id": resolved_chapter_id,
                                "work_id": str(chapter.work_id),
                                "operation": operation,
                                "no_change": True,
                                "description": description or "insert already applied"
                            }, ensure_ascii=False)

                        new_content = old_content[:insert_pos] + content_to_insert + old_content[insert_pos:]

            elif operation == "replace":
                replaced = None
                if isinstance(position, dict) and "from" in position and "to" in position:
                    try:
                        start_pos = int(position.get("from"))
                        end_pos = int(position.get("to"))
                        if 0 <= start_pos <= end_pos <= len(old_content):
                            replaced = old_content[:start_pos] + actual_content + old_content[end_pos:]
                    except (TypeError, ValueError):
                        replaced = None
                # 🔧 2026-01-11: 添加 replaced is None 检查，避免覆盖 position 对象定位结果
                if replaced is None and node_id:
                    replaced = _replace_by_node_id(old_content, node_id, actual_content)
                if replaced is None and original_text:
                    match_count = old_content.count(original_text)
                    if match_count == 1:
                        # 唯一匹配，直接替换
                        replaced = old_content.replace(original_text, actual_content, 1)
                    elif match_count > 1 and paragraph_index is not None:
                        # 🔧 重复出现，优先用 paragraph_index 定位，避免替换错段
                        inner_start = _get_paragraph_position(old_content, paragraph_index, "inner_start")
                        inner_end = _get_paragraph_position(old_content, paragraph_index, "inner_end")
                        if inner_start is not None and inner_end is not None:
                            replaced = old_content[:inner_start] + actual_content + old_content[inner_end:]
                            logger.debug(f"[apply_chapter_edit] replace original_text 重复({match_count}次)，改用段落索引定位: para_index={paragraph_index}")
                        else:
                            # 段落定位失败，退回第一次出现
                            replaced = old_content.replace(original_text, actual_content, 1)
                            logger.warning(f"[apply_chapter_edit] replace original_text 重复({match_count}次)，段落定位失败，使用第一次出现")
                    elif match_count > 1:
                        # 重复出现但无 paragraph_index，使用第一次出现并警告
                        replaced = old_content.replace(original_text, actual_content, 1)
                        logger.warning(f"[apply_chapter_edit] replace original_text 重复({match_count}次)，无 paragraph_index，使用第一次出现")
                if replaced is None and paragraph_index is not None:
                    # 🔧 修复：只替换段落内部内容，保留 <p> 标签和 data-id
                    inner_start = _get_paragraph_position(old_content, paragraph_index, "inner_start")
                    inner_end = _get_paragraph_position(old_content, paragraph_index, "inner_end")
                    if inner_start is not None and inner_end is not None:
                        replaced = old_content[:inner_start] + actual_content + old_content[inner_end:]
                        logger.debug(f"[apply_chapter_edit] replace 按段落索引定位: para_index={paragraph_index}, inner_start={inner_start}, inner_end={inner_end}")
                    else:
                        logger.warning(f"[apply_chapter_edit] replace 段落索引定位失败: para_index={paragraph_index}")
                if replaced is None and before_anchor and after_anchor:
                    before_idx = old_content.find(before_anchor)
                    if before_idx != -1:
                        start_idx = before_idx + len(before_anchor)
                        after_idx = old_content.find(after_anchor, start_idx)
                        if after_idx != -1:
                            replaced = old_content[:start_idx] + actual_content + old_content[after_idx:]
                if replaced is None:
                    if original_text and actual_content in old_content and original_text not in old_content:
                        return json.dumps({
                            "success": True,
                            "requires_confirmation": False,
                            "action_type": "update_content",
                            "chapter_id": resolved_chapter_id,
                            "work_id": str(chapter.work_id),
                            "operation": operation,
                            "no_change": True,
                            "description": description or "replace already applied"
                        }, ensure_ascii=False)
                    if not original_text and not before_anchor and not after_anchor and not node_id and paragraph_index is None:
                        replaced = actual_content
                    else:
                        return json.dumps({"success": False, "error": "locate_failed"}, ensure_ascii=False)
                new_content = replaced

            # 构建 position 字段（用于前端精确定位）
            result_position = None
            if operation == "insert" and insert_pos is not None:
                result_position = {"from": insert_pos, "to": insert_pos}
            elif operation == "replace" and isinstance(position, dict):
                result_position = position

            from app.services.chapter_revision_service import ChapterRevisionService

            revision_request_id = str(uuid.uuid4())
            revision_service = ChapterRevisionService(db)
            revision = await revision_service.create_revision(
                request_id=revision_request_id,
                work_id=str(chapter.work_id),
                chapter_id=str(chapter.id),
                user_id=str(user_id) if user_id else None,
                operation=operation,
                new_text=actual_content,
                original_text=original_text,
                position=result_position,
                before_anchor=before_anchor,
                after_anchor=after_anchor,
                node_id=node_id,
                paragraph_index=paragraph_index,
                base_version=chapter.version,
                description=description or f"update content ({operation})",
            )

            return json.dumps({
                "success": True,
                "requires_confirmation": True,  # 触发 HITL 流程，发送 revision 事件给前端
                "action_type": "update_content",
                "request_id": revision.request_id,
                "revision_id": str(revision.id),
                "chapter_id": resolved_chapter_id,
                "chapter_title": chapter.title,
                "work_id": str(chapter.work_id),
                "operation": operation,
                "content": actual_content,  # 新内容（用于前端显示）
                "original_text": original_text,  # 原文（用于回滚和定位）
                "position": result_position,  # 位置信息（insert/replace 操作）
                "node_id": node_id,  # 定位信息
                "paragraph_index": paragraph_index,  # 定位信息
                "before_anchor": before_anchor,  # 定位信息
                "after_anchor": after_anchor,  # 定位信息
                "content_length": len(actual_content),
                "description": description or f"update content ({operation})"
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
    """生成改写内容（只生成，不写入编辑器）。返回1个改写结果，由前端决定是否应用。

    【重要】此工具只生成内容，不会修改编辑器。

    【使用步骤】：
    1. 先用read_chapter_tool读取章节内容
    2. 定位用户提到的文本
    3. 调用本工具生成改写内容
    4. 用户确认后，由前端应用到编辑器"""
)
async def smart_rewrite(
    chapter_id: str,
    text_to_rewrite: Optional[str] = None,
    chapter_content: Optional[str] = None,
    user_requirement: Optional[str] = None,
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
        user_id: 用户ID（可选，优先从请求上下文获取）

    Returns:
        包含改写结果和确认请求的结果
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

        # 🆕 2026-01-10: 锚点定位职责已移交给 locate_content 工具
        # smart_rewrite 只负责创作，不再自动获取章节内容计算锚点

        # ✅ 使用AI生成单个改写结果（固定单结果输出）
        logger.info(f"[smart_rewrite] 开始生成改写结果，原文长度: {len(text_to_rewrite)}, 用户要求: {user_requirement}")
        # ✅ 2025-12-01: 成本追踪通过请求上下文自动完成，无需传递user_id
        versions = await _generate_rewrite_versions(
            original_text=text_to_rewrite,
            chapter_content=chapter_content or text_to_rewrite,
            user_requirement=user_requirement
        )

        # 🆕 2026-01-10: 锚点定位职责已移交给 locate_content 工具
        # smart_rewrite 只负责创作，不负责定位

        return json.dumps({
            "success": True,
            "action_type": "rewrite",
            "chapter_id": chapter_id,
            "original_text": text_to_rewrite,
            "versions": versions,
            "description": f"AI改写：{len(text_to_rewrite)}字 → 生成{len(versions)}条结果"
        }, ensure_ascii=False)

    except Exception as e:
        logger.error(f"smart_rewrite failed: {e}")
        return json.dumps({"success": False, "error": str(e)}, ensure_ascii=False)


def _has_multi_version_intent(text: Optional[str]) -> bool:
    if not text:
        return False
    pattern = re.compile(
        r"(?:多|多个|两|二|三|四|五|六|七|八|九|十|\d+)\s*(?:版|版本|方案|候选|备选|选项)"
        r"|(?:版本|方案)[一二三四五六七八九十ABCDabcd]"
        r"|[ABCDabcd]版"
    )
    return bool(pattern.search(text))


def _select_single_content(text: str) -> str:
    if not text:
        return text
    candidates = _extract_numbered_candidates(text)
    if candidates:
        return candidates[0]
    parts = [p.strip() for p in re.split(r"\n\s*\n+", text) if p.strip()]
    if len(parts) >= 2:
        return parts[0]
    return text


def _extract_numbered_candidates(text: str) -> List[str]:
    if not text:
        return []
    # 支持“版本一/版本二”“方案一/方案二”以及“1. / 2.”编号格式
    version_pattern = re.compile(r"(?:版本|方案)[一二三四五六七八九十]+(?:[:：]\s*)?")
    if version_pattern.search(text):
        parts = version_pattern.split(text)
        candidates = [p.strip() for p in parts if p.strip()]
        return candidates if len(candidates) >= 2 else []
    pattern = re.compile(r"(?:^|\s)(\d{1,2})[\.、\)]\s+")
    matches = list(pattern.finditer(text))
    if len(matches) < 2:
        return []
    numbers = [int(m.group(1)) for m in matches]
    if numbers[0] != 1 or numbers[1] != 2:
        return []
    candidates: List[str] = []
    for idx, match in enumerate(matches):
        start = match.end()
        end = matches[idx + 1].start() if idx + 1 < len(matches) else len(text)
        item = text[start:end].strip()
        if item:
            candidates.append(item)
    return candidates if len(candidates) >= 2 else []


# NOTE: multi-candidate selection disabled (single output only)


@tool
@register_as_tool(
    "smart_insert",
    "creative",
    "生成插入内容（只生成，不写入编辑器）。返回生成的内容，由前端决定是否应用。定位由 locate_content 工具负责。"
)
async def smart_insert(
    chapter_id: str,
    user_intent: str,
    chapter_content: Optional[str] = None,
    insert_context: Optional[str] = None,
    word_count: int = 200,
    user_id: Optional[str] = None,
    work_id: Optional[str] = None
) -> str:
    """
    智能插入 - 生成要插入的内容（不直接修改编辑器）

    🆕 2026-01-10: 锚点定位职责已移交给 locate_content 工具
    smart_insert 只负责创作，不负责定位

    Args:
        chapter_id: 章节ID
        user_intent: 用户的意图描述（如"在这里加一段心理描写"）
        chapter_content: 章节完整内容（用于风格分析）
        insert_context: 插入点附近的上下文（从 locate_content 获取）
        word_count: 期望生成字数
        user_id: 用户ID

    Returns:
        生成的插入内容
    """
    try:
        # 如果没有提供章节内容，自动获取
        resolved_chapter_id = chapter_id
        if work_id and chapter_id and chapter_id.count('-') != 4:
            try:
                from app.services.agent.langgraph_tools import resolve_chapter_id
                resolved_id, error = await resolve_chapter_id(work_id, chapter_id)
                if resolved_id:
                    resolved_chapter_id = resolved_id
                elif error:
                    logger.warning(f"[smart_insert] 章节序号解析失败: {error}")
                    resolved_chapter_id = ""
            except Exception as e:
                logger.warning(f"[smart_insert] 章节序号解析异常: {e}")

        if not chapter_content and resolved_chapter_id:
            try:
                async with AsyncSessionLocal() as db:
                    from app.services.chapter_service import ChapterService
                    chapter_svc = ChapterService(db)
                    chapter = await chapter_svc.get_chapter_by_id(resolved_chapter_id)
                    if chapter and chapter.content:
                        chapter_content = chapter.content
            except Exception as e:
                logger.warning(f"[smart_insert] 获取章节内容失败: {e}")

        # 使用AI生成插入内容
        ai_service = _get_ai_service()

        context_text = f"\n【插入点上下文】\n{insert_context}" if insert_context else ""
        multi_version_intent = _has_multi_version_intent(user_intent)
        single_rule = "\n5. 即使用户要求多版本，也只生成一条内容" if multi_version_intent else ""

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
4. 只输出一段正文，不要编号/版本/列表
{single_rule}

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

        description = "AI生成插入内容"
        if multi_version_intent or _extract_numbered_candidates(generated_content):
            normalized = _select_single_content(generated_content)
            if normalized != generated_content:
                generated_content = normalized
                description = "AI生成插入内容：已截取第1条"

        versions = [{
            "style_name": "插入内容",
            "reason": user_intent,
            "content": generated_content
        }]

        # 🆕 2026-01-10: 锚点定位职责已移交给 locate_content 工具
        # smart_insert 只负责创作，不负责定位

        # 🔧 2026-01-25: 统一返回格式，使用 versions 结构与 smart_rewrite 保持一致
        return json.dumps({
            "success": True,
            "action_type": "insert",
            "chapter_id": resolved_chapter_id or chapter_id,
            "content": generated_content,  # 保留原字段以兼容
            "versions": versions,
            "content_length": len(generated_content),
            "description": description
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
    description="智能改写章节文本，生成1个改写结果",
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
    work_id: Optional[str] = Field(default=None, description="作品ID（用于章节序号解析）")


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
            "user_id": input_data.user_id,
            "work_id": input_data.work_id
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
    operation: str = Field(default="append", description="操作类型：append/replace/insert/replace_all", pattern="^(append|replace|insert|replace_all)$")
    position: Optional[int] = Field(default=None, description="插入位置（仅 insert 操作）")
    before_anchor: Optional[str] = Field(default=None, description="插入点前面的文本（用于精确定位）")
    after_anchor: Optional[str] = Field(default=None, description="插入点后面的文本（用于精确定位）")
    original_text: Optional[str] = Field(default=None, description="原文（用于前端定位，replace 操作时传递）")
    node_id: Optional[str] = Field(default=None, description="节点ID（最高优先级定位，从 locate_content 获取）")
    paragraph_index: Optional[int] = Field(default=None, description="段落索引（从 locate_content 获取）")
    user_id: Optional[str] = Field(default=None, description="用户ID")
    description: Optional[str] = Field(default=None, description="操作描述")
    conversation_id: Optional[str] = Field(default=None, description="会话ID（用于操作日志）")
    work_id: Optional[str] = Field(default=None, description="作品ID（可选）")


class ApplyChapterEditOutput(ToolOutput):
    """章节编辑应用工具输出"""
    pass


async def apply_chapter_edit_executor(input_data: ApplyChapterEditInput) -> ApplyChapterEditOutput:
    """章节编辑应用执行器（包装 @tool 版本）"""
    try:
        # 🔧 2025-12-14: @tool 装饰器返回 StructuredTool，需要用 .ainvoke() 调用
        # 🔧 2026-01-10: 添加锚点、原文、node_id、paragraph_index 参数传递
        result_str = await apply_chapter_edit.ainvoke({
            "chapter_id": input_data.chapter_id,
            "content": input_data.content,
            "operation": input_data.operation,
            "position": input_data.position,
            "before_anchor": input_data.before_anchor,
            "after_anchor": input_data.after_anchor,
            "original_text": input_data.original_text,
            "node_id": input_data.node_id,
            "paragraph_index": input_data.paragraph_index,
            "user_id": input_data.user_id,
            "description": input_data.description,
            "conversation_id": input_data.conversation_id,
            "work_id": input_data.work_id
        })

        result_data = json.loads(result_str) if isinstance(result_str, str) else result_str

        # 🔧 2026-01-12: 修复 message 字段，当 success=False 时使用 error 字段
        success = result_data.get("success", True)
        if success:
            message = result_data.get("description", "编辑已应用")
        else:
            message = result_data.get("error", result_data.get("message", "编辑失败"))

        return ApplyChapterEditOutput(
            success=success,
            message=message,
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
