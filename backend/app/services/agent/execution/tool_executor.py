# -*- coding: utf-8 -*-
"""
工具执行器

从 langgraph_agent.py 提取的工具调用逻辑：
- 统一工具调用接口
- 参数预处理
- 结果提取
- 降级兜底
"""

from typing import Dict, Any, Optional, Tuple
import json
import logging
import re

from app.services.agent.tools import registry
from app.services.agent.langgraph_tools import resolve_chapter_id, is_chapter_order, read_paragraph
from app.services.agent.utils.chapter_cache import ChapterCache
from app.services.agent.utils.tool_cache import ToolCache
from app.services.agent.utils.tool_context import (
    set_stream_event_handler,
    reset_stream_event_handler,
    set_explore_step_id,
    reset_explore_step_id,
)

logger = logging.getLogger(__name__)


# 工具名称映射（@tool 名称 → StandardTool 名称）
TOOL_NAME_MAPPING = {
    "analyze_text_tool": "analyze_content",
    "smart_rewrite": "smart_rewrite",
    "smart_continue": "smart_continue",
    "smart_insert": "smart_insert",
    "apply_chapter_edit": "apply_chapter_edit",
    # 章节工具
    "get_context_tool": "get_context",
    "read_chapter_tool": "read_chapter",
    "get_chapter_by_order_tool": "get_chapter_by_order",
    "search_analysis_fragments_tool": "search_content",
    "search_analysis_fragments": "search_content",
    "search_content": "search_content",
    # 世界观工具
    "get_worldview_summary": "get_worldview_summary",
    # 分析工具
    "evaluate_quality_tool": "evaluate_quality",
    "analyze_content_tool": "analyze_content",
    # 章节管理工具（OPERATION 类）
    "create_chapter": "create_chapter",
    "update_chapter_title": "update_chapter_title",
    "delete_chapter": "delete_chapter",
    "update_chapter_content": "update_chapter_content",
    # 聚合工具（2026-01-12）
    "get_writing_context": "get_writing_context",
    "get_style_guidance_tool": "get_style_guidance",
}

TOOL_CACHE_INVALIDATION_TOOLS = {
    "apply_chapter_edit",
    "update_chapter_content",
    "update_chapter_title",
    "delete_chapter",
    "create_chapter",
    "operate_apply",
}

GWC_ALIAS_TOOL_INCLUDES = {
    "read_chapter": "chapter",
    "get_chapter_by_order": "chapter",
    "get_context": "work,chapter,rag",
    "get_worldview_summary": "worldview",
}


class ToolExecutor:
    """工具执行器

    负责统一管理工具调用：
    1. StandardTool 优先
    2. @tool 降级兜底
    """

    def __init__(self):
        pass

    async def call_tool(
        self,
        tool_name: str,
        tool_args: dict,
        state: dict
    ) -> str:
        """通过 registry 统一调用工具（StandardTool 优先，@tool 兜底）

        Args:
            tool_name: 工具名称
            tool_args: 工具参数
            state: Agent 状态

        Returns:
            str: 工具执行结果（字符串格式）
        """
        # 规范化工具名称
        tool_args = dict(tool_args or {})
        normalized_name = TOOL_NAME_MAPPING.get(tool_name, tool_name)
        tool_policy = self._resolve_tool_policy(state)

        if tool_policy == "no_tool":
            return json.dumps({
                "error": "tool_disabled",
                "message": "tool_policy=no_tool",
                "tool": normalized_name,
            }, ensure_ascii=False)

        if tool_policy == "auto" and normalized_name == "locate_content":
            tool_args = await self._autofill_locate_chapter_id(tool_args, state)

        # 🆕 2026-01-12: 章节缓存检查
        if normalized_name in ["read_chapter", "get_chapter_by_order"]:
            cached_result = self._check_chapter_cache(normalized_name, tool_args, state)
            if cached_result:
                return cached_result

        # 🆕 2026-01-12: get_writing_context 也使用章节缓存
        if normalized_name == "get_writing_context":
            cached_result = self._check_writing_context_cache(tool_args, state)
            if cached_result:
                return cached_result

        try:
            # 准备参数
            params = self.prepare_params(normalized_name, tool_args, state)
            if normalized_name == "smart_insert":
                params = await self._augment_insert_context(params, state)
            elif normalized_name == "smart_rewrite":
                params = await self._augment_rewrite_context(params, state)

            # 🛡️ 章节一致性校验：写回阶段必须与目标章节一致
            expected_chapter_id, expected_source = self._get_target_chapter_id(state)
            if normalized_name in {"operate_apply", "apply_chapter_edit"} and expected_chapter_id:
                operation = params.get("operation")
                if operation in {"append", "replace", "insert", "content", "replace_all"}:
                    actual_chapter_id = params.get("chapter_id")
                    if actual_chapter_id and str(actual_chapter_id) != str(expected_chapter_id):
                        # 允许章节序号与UUID的等价匹配
                        work_id = params.get("work_id") or state.get("work_id")
                        actual_norm = str(actual_chapter_id)
                        expected_norm = str(expected_chapter_id)
                        if work_id:
                            if is_chapter_order(actual_norm):
                                resolved_actual, _ = await resolve_chapter_id(work_id, actual_norm)
                                if resolved_actual:
                                    actual_norm = str(resolved_actual)
                            if is_chapter_order(expected_norm):
                                resolved_expected, _ = await resolve_chapter_id(work_id, expected_norm)
                                if resolved_expected:
                                    expected_norm = str(resolved_expected)
                        if actual_norm == expected_norm:
                            logger.info(
                                "[ToolExecutor] chapter_id 等价匹配通过: actual=%s expected=%s",
                                actual_chapter_id,
                                expected_chapter_id
                            )
                        else:
                            logger.error(
                                "[ToolExecutor] chapter_id 不一致，已阻止写回: actual=%s expected=%s source=%s",
                                actual_chapter_id,
                                expected_chapter_id,
                                expected_source
                            )
                            return json.dumps({
                                "error": "chapter_id_mismatch",
                                "message": "写回章节与目标章节不一致，已阻止操作。",
                                "expected_chapter_id": expected_chapter_id,
                                "actual_chapter_id": actual_chapter_id,
                                "expected_source": expected_source
                            }, ensure_ascii=False)

            # 🔧 2026-01-26: fail-fast，避免 chapter_id 为空导致隐式失败
            if normalized_name in {"smart_rewrite", "smart_insert", "smart_continue"}:
                if not params.get("chapter_id"):
                    return json.dumps({
                        "error": "missing_chapter_id",
                        "message": "chapter_id 为空，请检查是否引用 locate_content 的 chapter_id（引用路径错误）"
                    }, ensure_ascii=False)
            if normalized_name in {"operate_apply", "apply_chapter_edit"}:
                operation = params.get("operation")
                if operation in {"replace", "insert", "append", "content"} and not params.get("chapter_id"):
                    return json.dumps({
                        "error": "missing_chapter_id",
                        "message": "chapter_id 为空，请检查是否引用 locate_content 的 chapter_id（引用路径错误）"
                    }, ensure_ascii=False)
                require_locator = bool(params.pop("__require_source_locator", False))
                auto_locator = bool(params.pop("__auto_locator", False))
                explicit_locator = bool(
                    params.get("locate_target_index") is not None
                    or params.get("locator_id")
                    or params.get("locate_target_id")
                    or params.get("locate_target_hint")
                )
                if operation in {"replace", "insert"} and require_locator and (auto_locator or explicit_locator):
                    locator_error = self._ensure_source_locator(
                        params,
                        state,
                        text_hint=params.get("original_text") or params.get("target_description", ""),
                        force=True
                    )
                    if locator_error:
                        return json.dumps(locator_error, ensure_ascii=False)
                if operation in {"replace", "insert"} and require_locator:
                    locator_error = self._validate_source_locator(params, auto_locator=auto_locator)
                    if locator_error:
                        return json.dumps(locator_error, ensure_ascii=False)
                if operation in {"replace", "insert", "append", "content", "replace_all"}:
                    content = params.get("content")
                    if content is None or (isinstance(content, str) and not content.strip()):
                        return json.dumps({
                            "error": "missing_content",
                            "message": "写回内容为空，可能是内容引用路径错误（请检查 data.content/data.versions[0].content）"
                        }, ensure_ascii=False)
                    if not isinstance(content, str):
                        return json.dumps({
                            "error": "invalid_content",
                            "message": "写回内容类型非法（期望字符串），请检查内容引用路径"
                        }, ensure_ascii=False)
                if operation in {"replace", "insert"} and not params.get("node_id") and params.get("paragraph_index") is None:
                    return json.dumps({
                        "error": "missing_locator",
                        "message": "replace/insert 必须提供 node_id 或 paragraph_index（请先定位段落）"
                    }, ensure_ascii=False)
                if normalized_name == "apply_chapter_edit":
                    params.pop("source_locator", None)

            if isinstance(params, dict) and params.get("__locator_error"):
                error_payload = params.get("__locator_error") or {}
                if isinstance(error_payload, dict):
                    return json.dumps(error_payload, ensure_ascii=False)
                return json.dumps({
                    "error": "locator_error",
                    "message": str(error_payload)
                }, ensure_ascii=False)

            cached_result = self._read_cover_cache(normalized_name, params, state)
            if cached_result is not None:
                return cached_result

            # 工具层缓存命中检查
            cache_ctx = ToolCache.get_context(normalized_name, params, state)
            if tool_policy == "cache_only":
                if cache_ctx:
                    cached_result = ToolCache.read(cache_ctx)
                    if cached_result is not None:
                        return cached_result
                return json.dumps({
                    "error": "tool_cache_miss",
                    "message": "tool_policy=cache_only",
                    "tool": normalized_name,
                }, ensure_ascii=False)
            if cache_ctx:
                cached_result = ToolCache.read(cache_ctx)
                if cached_result is not None:
                    return cached_result

            # 调用 StandardTool
            stream_token = None
            step_token = None
            if normalized_name == "explore_content" and isinstance(state, dict):
                stream_handler = state.get("stream_event_handler")
                if stream_handler:
                    stream_token = set_stream_event_handler(stream_handler)
                step_id = state.get("step_id")
                if isinstance(step_id, str):
                    try:
                        step_id = int(step_id)
                    except ValueError:
                        step_id = None
                if isinstance(step_id, int):
                    step_token = set_explore_step_id(step_id)
            try:
                result = await registry.call_tool(normalized_name, params)
            finally:
                if step_token is not None:
                    reset_explore_step_id(step_token)
                if stream_token is not None:
                    reset_stream_event_handler(stream_token)

            # 🔧 处理返回值为 JSON 字符串的情况（如 locate_content、@tool 装饰器返回值）
            if isinstance(result, str):
                try:
                    result = json.loads(result)
                except json.JSONDecodeError:
                    pass  # 保持原样，让后续逻辑处理

            # 提取返回值
            if isinstance(result, dict) and result.get("success"):
                if normalized_name == "explore_content":
                    try:
                        tool_result = json.dumps(result, ensure_ascii=False)
                    except Exception:
                        tool_result = str(result)
                else:
                    tool_result = self.extract_result(normalized_name, result)
                logger.info(f"[StandardTool] {normalized_name} 执行成功")

                if cache_ctx:
                    ToolCache.write(cache_ctx, tool_result)

                # 🆕 2026-01-12: 章节缓存写入
                if normalized_name in ["read_chapter", "get_chapter_by_order"]:
                    self._update_chapter_cache(normalized_name, result, state)

                # 🆕 2026-01-12: get_writing_context 章节缓存写入
                if normalized_name == "get_writing_context":
                    self._update_writing_context_cache(result, state)

                self._invalidate_tool_cache_if_needed(normalized_name, params, result, state)
                return tool_result
            else:
                error_msg = result.get("message", "执行失败") if isinstance(result, dict) else "未知错误"
                logger.error(f"[StandardTool] {normalized_name} 执行失败: {error_msg}")
                return json.dumps({"error": "tool_failed", "message": error_msg}, ensure_ascii=False)

        except ValueError as e:
            # StandardTool 不存在，降级到 @tool
            logger.warning(f"[StandardTool] '{normalized_name}' 不存在，降级到 @tool: {e}")
            return await self.fallback_to_legacy(tool_name, tool_args, state)

        except Exception as e:
            # 其他错误，也尝试降级
            logger.error(f"[StandardTool] 调用失败: {e}")
            return await self.fallback_to_legacy(tool_name, tool_args, state)

    def _invalidate_tool_cache_if_needed(
        self,
        tool_name: str,
        params: dict,
        result: dict,
        state: dict
    ) -> None:
        if tool_name not in TOOL_CACHE_INVALIDATION_TOOLS:
            return

        data = result.get("data", {}) if isinstance(result, dict) else {}
        work_id = data.get("work_id") or params.get("work_id") or state.get("work_id")
        chapter_id = data.get("chapter_id") or params.get("chapter_id") or state.get("chapter_id")
        include_work_scope = tool_name in {"create_chapter", "delete_chapter"} or not chapter_id

        ToolCache.invalidate(
            work_id=str(work_id) if work_id else None,
            chapter_id=str(chapter_id) if chapter_id else None,
            include_work_scope=include_work_scope,
            include_multi_scope=True,
        )

    def prepare_params(
        self,
        tool_name: str,
        tool_args: dict,
        state: dict
    ) -> dict:
        """准备工具参数（处理特殊情况）"""
        params = dict(tool_args)
        last_user_message = state.get("last_user_message", "")
        evidence_context = self._build_evidence_context(state)

        # 工具特定的参数处理
        if tool_name == "continue_writing":
            params.setdefault("context", last_user_message)
            params.setdefault("requirements", "")
            # 🔧 默认值从 500 改为 2000，更符合实际续写需求
            params.setdefault("target_length", 2000)
            params.setdefault("style", "")

        elif tool_name == "analyze_text":
            params.setdefault("text", last_user_message)
            params.setdefault("focus", "all")

        elif tool_name == "smart_rewrite":
            # P1修复：从 state 获取上下文信息作为兜底，避免参数全为 None
            current_chapter_id = state.get("chapter_id", "")
            context_data = state.get("context", {}) if isinstance(state.get("context"), dict) else {}
            selected_text = context_data.get("selected_text", "")
            locate_original_text = context_data.get("locate_original_text", "")

            # 2026-01-27: 检测 chapter_id 是否为 None（引用解析失败）
            # 如果 chapter_id 是 None（不是空字符串或未设置），说明 $ref 解析越界
            # 此时应该报错而不是静默使用当前章节
            param_chapter_id = params.get("chapter_id")
            if param_chapter_id is None:
                if "chapter_id" in params:
                    # 参数中明确有 chapter_id 但值为 None，说明引用解析失败
                    logger.error(
                        "[ToolExecutor] smart_rewrite chapter_id 引用解析失败（越界或路径错误），"
                        f"原始参数: {params}, state.chapter_id: {current_chapter_id}"
                    )
                    logger.warning(
                        "[ToolExecutor] 降级使用当前章节作为 chapter_id，可能导致修改位置错误"
                    )
                # 强制设置 chapter_id（setdefault 不会覆盖 None 值）
                params["chapter_id"] = current_chapter_id
            else:
                params.setdefault("chapter_id", current_chapter_id)

            # text_to_rewrite: 优先使用参数值，其次使用选中文本
            if not params.get("text_to_rewrite"):
                params["text_to_rewrite"] = selected_text or locate_original_text or ""
            if not params.get("text_to_rewrite"):
                params["text_to_rewrite"] = self._pick_evidence_text(state) or ""

            # 🔧 2026-01-12: 确保 chapter_content 是字符串类型
            chapter_content = params.get("chapter_content")
            if chapter_content is not None and not isinstance(chapter_content, str):
                if isinstance(chapter_content, list) and len(chapter_content) > 0:
                    first_item = chapter_content[0]
                    if isinstance(first_item, dict):
                        params["chapter_content"] = first_item.get("content", "")
                    else:
                        params["chapter_content"] = str(chapter_content)
                else:
                    params["chapter_content"] = str(chapter_content) if chapter_content else ""
            # chapter_content: 兜底使用 text_to_rewrite
            if not params.get("chapter_content"):
                params["chapter_content"] = params.get("text_to_rewrite", "")

            # user_requirement: 从用户消息中提取改写要求
            if not params.get("user_requirement"):
                params["user_requirement"] = state.get("last_user_message", "")
            if evidence_context and not params.get("evidence_context"):
                params["evidence_context"] = evidence_context
            if "evidence_context" in params and not isinstance(params.get("evidence_context"), str):
                logger.warning("[ToolExecutor] smart_rewrite evidence_context 非字符串，已强制转换")
                params["evidence_context"] = self._coerce_evidence_context(params.get("evidence_context"))

            auto_locator = bool(params.get("__auto_locator"))
            explicit_locator = bool(
                params.get("locate_target_index") is not None
                or params.get("locator_id")
                or params.get("locate_target_id")
                or params.get("locate_target_hint")
            )
            locator_error = self._ensure_source_locator(
                params,
                state,
                text_hint=params.get("text_to_rewrite", ""),
                force=auto_locator or explicit_locator
            )
            if locator_error:
                params["__locator_error"] = locator_error
            else:
                source_locator = params.get("source_locator") if isinstance(params.get("source_locator"), dict) else {}
                locator_text = source_locator.get("text") if isinstance(source_locator, dict) else None
                if locator_text and (explicit_locator or not params.get("text_to_rewrite")):
                    params["text_to_rewrite"] = locator_text

            # 清理不再使用的多版本参数（smart_rewrite 仅生成单个结果）
            params.pop("base_version", None)
            params.setdefault("user_id", state.get("user_id"))

        elif tool_name == "smart_continue":
            # 2026-01-27: 检测 chapter_id 是否为 None（引用解析失败）
            current_chapter_id = state.get("chapter_id", "")
            expected_chapter_id, expected_source = self._get_target_chapter_id(state)
            param_chapter_id = params.get("chapter_id")
            chapter_source = "explicit"
            if param_chapter_id is None or (isinstance(param_chapter_id, str) and not param_chapter_id.strip()):
                if "chapter_id" in params:
                    logger.error(
                        "[ToolExecutor] smart_continue chapter_id 引用解析失败（越界或路径错误），"
                        f"原始参数: {params}, state.chapter_id: {current_chapter_id}"
                    )
                    logger.warning(
                        "[ToolExecutor] 降级使用当前章节作为 chapter_id，可能导致续写位置错误"
                    )
                if expected_chapter_id:
                    params["chapter_id"] = expected_chapter_id
                    chapter_source = expected_source
                    logger.info(
                        "[ToolExecutor] smart_continue chapter_id 使用目标章节: %s (source=%s)",
                        expected_chapter_id,
                        expected_source
                    )
                else:
                    params["chapter_id"] = current_chapter_id
                    chapter_source = "state_fallback"
            else:
                params.setdefault("chapter_id", current_chapter_id)
                if not param_chapter_id:
                    chapter_source = "state_fallback"
                    params["chapter_id"] = current_chapter_id
                else:
                    chapter_source = "explicit"
                if expected_chapter_id and str(param_chapter_id) != str(expected_chapter_id):
                    logger.warning(
                        "[ToolExecutor] smart_continue chapter_id 与目标章节不一致: actual=%s expected=%s source=%s",
                        param_chapter_id,
                        expected_chapter_id,
                        expected_source
                    )
            logger.info(
                "[ToolExecutor] smart_continue chapter_id 来源=%s value=%s",
                chapter_source,
                params.get("chapter_id")
            )
            # 🔧 2026-01-12: 确保 chapter_content 是字符串类型
            chapter_content = params.get("chapter_content")
            if chapter_content is not None and not isinstance(chapter_content, str):
                if isinstance(chapter_content, list) and len(chapter_content) > 0:
                    first_item = chapter_content[0]
                    if isinstance(first_item, dict):
                        params["chapter_content"] = first_item.get("content", "")
                    else:
                        params["chapter_content"] = str(chapter_content)
                else:
                    params["chapter_content"] = str(chapter_content) if chapter_content else None
            params.setdefault("user_id", state.get("user_id"))
            if evidence_context and not params.get("evidence_context"):
                params["evidence_context"] = evidence_context
            if "evidence_context" in params and not isinstance(params.get("evidence_context"), str):
                logger.warning("[ToolExecutor] smart_continue evidence_context 非字符串，已强制转换")
                params["evidence_context"] = self._coerce_evidence_context(params.get("evidence_context"))

        elif tool_name == "smart_insert":
            # 2026-01-27: 检测 chapter_id 是否为 None（引用解析失败）
            current_chapter_id = state.get("chapter_id", "")
            param_chapter_id = params.get("chapter_id")
            if param_chapter_id is None:
                if "chapter_id" in params:
                    logger.error(
                        "[ToolExecutor] smart_insert chapter_id 引用解析失败（越界或路径错误），"
                        f"原始参数: {params}, state.chapter_id: {current_chapter_id}"
                    )
                    logger.warning(
                        "[ToolExecutor] 降级使用当前章节作为 chapter_id，可能导致插入位置错误"
                    )
                params["chapter_id"] = current_chapter_id
            else:
                params.setdefault("chapter_id", current_chapter_id)
            params.setdefault("work_id", state.get("work_id", ""))
            # 🔧 2026-01-12: 确保 chapter_content 是字符串类型，避免 AI 传入列表导致验证失败
            chapter_content = params.get("chapter_content")
            if chapter_content is not None and not isinstance(chapter_content, str):
                # 如果是列表（如 get_chapter_by_order 返回的章节列表），尝试提取内容
                if isinstance(chapter_content, list) and len(chapter_content) > 0:
                    first_item = chapter_content[0]
                    if isinstance(first_item, dict):
                        params["chapter_content"] = first_item.get("content", "")
                    else:
                        params["chapter_content"] = str(chapter_content)
                else:
                    params["chapter_content"] = str(chapter_content) if chapter_content else None
            params.setdefault("context", None)
            params.setdefault("user_id", state.get("user_id"))
            insert_context = params.get("insert_context")
            if insert_context is not None and not isinstance(insert_context, str):
                params["insert_context"] = self._coerce_evidence_context(insert_context)
            if evidence_context and not params.get("evidence_context"):
                params["evidence_context"] = evidence_context
            if "evidence_context" in params and not isinstance(params.get("evidence_context"), str):
                logger.warning("[ToolExecutor] smart_insert evidence_context 非字符串，已强制转换")
                params["evidence_context"] = self._coerce_evidence_context(params.get("evidence_context"))

            auto_locator = bool(params.get("__auto_locator"))
            explicit_locator = bool(
                params.get("locate_target_index") is not None
                or params.get("locator_id")
                or params.get("locate_target_id")
                or params.get("locate_target_hint")
            )
            locator_error = self._ensure_source_locator(
                params,
                state,
                text_hint=params.get("insert_context") or params.get("user_intent", ""),
                force=auto_locator or explicit_locator
            )
            if locator_error:
                params["__locator_error"] = locator_error
            else:
                source_locator = params.get("source_locator") if isinstance(params.get("source_locator"), dict) else {}
                insert_context = source_locator.get("text") if isinstance(source_locator, dict) else None
                if insert_context and (explicit_locator or not params.get("insert_context")):
                    params["insert_context"] = insert_context

        elif tool_name == "locate_content":
            # 🔧 2026-01-12: 移除不支持的 work_id 参数，避免 AI 规划错误导致工具调用失败
            params.pop("work_id", None)
            ignore_state = self._should_ignore_state_chapter_id(state, params)
            if not ignore_state:
                params.setdefault("chapter_id", state.get("chapter_id", ""))
            context = state.get("context", {}) if isinstance(state.get("context"), dict) else {}
            state_chapter_id = str(state.get("chapter_id", "") or "").strip()
            target_chapter_id = str(params.get("chapter_id", "") or "").strip()
            use_context_locate = bool(
                target_chapter_id
                and state_chapter_id
                and target_chapter_id == state_chapter_id
            )
            if use_context_locate:
                params.setdefault("node_id", context.get("locate_node_id"))
            nodes_info = params.get("nodes_info")
            if nodes_info is not None and not isinstance(nodes_info, str):
                params["nodes_info"] = json.dumps(nodes_info, ensure_ascii=False)
            elif not nodes_info and use_context_locate:
                context_nodes = context.get("nodes_info")
                if context_nodes:
                    params["nodes_info"] = (
                        context_nodes
                        if isinstance(context_nodes, str)
                        else json.dumps(context_nodes, ensure_ascii=False)
                    )

        elif tool_name == "apply_chapter_edit":
            context = state.get("context", {}) if isinstance(state.get("context"), dict) else {}
            params.setdefault("chapter_id", state.get("chapter_id", ""))
            params.setdefault("operation", "append")
            params.setdefault("position", None)
            params.setdefault("before_anchor", None)  # 🆕 锚点定位
            params.setdefault("after_anchor", None)   # 🆕 锚点定位
            params.setdefault("original_text", None)  # 🆕 原文（用于前端定位）
            params.setdefault("node_id", context.get("locate_node_id"))
            params.setdefault("paragraph_index", context.get("locate_paragraph_index"))
            # 🔧 2026-01-12: 确保 paragraph_index 是整数或 None，避免上游任务失败时传入错误字符串
            pi = params.get("paragraph_index")
            if pi is not None and not isinstance(pi, int):
                try:
                    params["paragraph_index"] = int(pi)
                except (ValueError, TypeError):
                    params["paragraph_index"] = None
            if not params.get("node_id"):
                params["node_id"] = context.get("locate_node_id")
            if params.get("paragraph_index") is None:
                params["paragraph_index"] = context.get("locate_paragraph_index")
            if not params.get("before_anchor"):
                params["before_anchor"] = context.get("locate_before_anchor")
            if not params.get("after_anchor"):
                params["after_anchor"] = context.get("locate_after_anchor")
            if not params.get("original_text"):
                params["original_text"] = context.get("locate_original_text")
            params.setdefault("user_id", state.get("user_id"))
            params.setdefault("description", None)
            params.setdefault("conversation_id", state.get("conversation_id", ""))
            params.setdefault("work_id", state.get("work_id", ""))

        elif tool_name == "get_context":
            params.setdefault("work_id", state.get("work_id", ""))
            params.setdefault("chapter_id", state.get("chapter_id", ""))

        elif tool_name == "read_chapter":
            params.setdefault("work_id", state.get("work_id", ""))
            params.setdefault("chapter_id", state.get("chapter_id", ""))

        elif tool_name == "get_chapter_by_order":
            params.setdefault("work_id", state.get("work_id", ""))
            params.setdefault("chapter_order", "1")  # 字符串类型

        elif tool_name == "search_analysis_fragments":
            params.setdefault("work_id", state.get("work_id", ""))
            params.setdefault("query", last_user_message)
            params.setdefault("top_k", 5)
            params.setdefault("chapter_id", state.get("chapter_id", ""))
            params.setdefault("include_current", True)
            params.setdefault("look_ahead", 0)
            params.setdefault("max_content_length", 200)

        elif tool_name == "search_content":
            params.setdefault("work_id", state.get("work_id", ""))
            params.setdefault("query", last_user_message)
            params.setdefault("top_k", 10)
            ignore_state = self._should_ignore_state_chapter_id(state, params)
            params.setdefault("chapter_id", "" if ignore_state else state.get("chapter_id", ""))
            params.setdefault("look_ahead", 0)
            try:
                top_k = int(params.get("top_k", 10))
            except (TypeError, ValueError):
                top_k = 10
            if top_k < 1:
                top_k = 1
            if top_k > 50:
                top_k = 50
            params["top_k"] = top_k

        elif tool_name == "get_worldview_summary":
            params.setdefault("work_id", state.get("work_id", ""))

        # 🆕 2026-01-12: get_writing_context 聚合工具
        elif tool_name == "get_writing_context":
            params.setdefault("work_id", state.get("work_id", ""))
            params.setdefault("chapter_id", state.get("chapter_id", ""))
            params.setdefault("chapter_orders", "")
            params.setdefault("user_id", state.get("user_id", ""))
            params.setdefault("include", "work,chapter,worldview,style,rag")
            params.setdefault("rag_query", "")
            params.setdefault("rag_top_k", 5)
            params.setdefault("use_cache", True)

        # 🆕 2026-01-17: explore_content 深度探索工具
        elif tool_name == "explore_content":
            params.setdefault("work_id", state.get("work_id", ""))
            params.setdefault("user_id", state.get("user_id", ""))
            # target_task 必须由 AI 提供，不设默认值
            params.setdefault("max_rounds", 10)
            params.setdefault("conversation_id", state.get("conversation_id", ""))
            allowed_keys = {
                "work_id",
                "target_task",
                "search_keywords",
                "max_rounds",
                "explore_mode",
                "max_tool_calls",
                "max_read_paragraphs",
                "output_mode",
                "require_paragraph_index",
                "user_id",
                "conversation_id",
                "use_cache",
                "force_refresh"
            }
            params = {key: value for key, value in params.items() if key in allowed_keys}

        elif tool_name == "load_explore_artifact":
            params.setdefault("work_id", state.get("work_id", ""))
            params.setdefault("user_id", state.get("user_id", ""))
            params.setdefault("mode", "full")

        # 🆕 2026-01-23: operate_apply 统一操作工具
        elif tool_name == "operate_apply":
            # 2026-01-27: 检测 chapter_id 是否为 None（引用解析失败）
            current_chapter_id = state.get("chapter_id", "")
            expected_chapter_id, expected_source = self._get_target_chapter_id(state)
            param_chapter_id = params.get("chapter_id")
            chapter_source = "explicit"
            if param_chapter_id is None or (isinstance(param_chapter_id, str) and not param_chapter_id.strip()):
                if "chapter_id" in params:
                    logger.error(
                        "[ToolExecutor] operate_apply chapter_id 引用解析失败（越界或路径错误），"
                        f"原始参数: {params}, state.chapter_id: {current_chapter_id}"
                    )
                    logger.warning(
                        "[ToolExecutor] 降级使用当前章节作为 chapter_id，可能导致操作位置错误"
                    )
                if expected_chapter_id:
                    params["chapter_id"] = expected_chapter_id
                    chapter_source = expected_source
                    logger.info(
                        "[ToolExecutor] operate_apply chapter_id 使用目标章节: %s (source=%s)",
                        expected_chapter_id,
                        expected_source
                    )
                else:
                    params["chapter_id"] = current_chapter_id
                    chapter_source = "state_fallback"
            else:
                params.setdefault("chapter_id", current_chapter_id)
                if not param_chapter_id:
                    chapter_source = "state_fallback"
                    params["chapter_id"] = current_chapter_id
                else:
                    chapter_source = "explicit"
                if expected_chapter_id and str(param_chapter_id) != str(expected_chapter_id):
                    logger.warning(
                        "[ToolExecutor] operate_apply chapter_id 与目标章节不一致: actual=%s expected=%s source=%s",
                        param_chapter_id,
                        expected_chapter_id,
                        expected_source
                    )
                    operation = params.get("operation")
                    force_target = operation in {"replace", "insert"} and bool(
                        params.get("__auto_locator") or params.get("__require_source_locator")
                    )
                    if force_target:
                        params["chapter_id"] = expected_chapter_id
                        chapter_source = f"override:{expected_source}"
                        logger.info(
                            "[ToolExecutor] operate_apply chapter_id 覆盖为目标章节: actual=%s expected=%s source=%s",
                            param_chapter_id,
                            expected_chapter_id,
                            expected_source
                        )
            logger.info(
                "[ToolExecutor] operate_apply chapter_id 来源=%s value=%s",
                chapter_source,
                params.get("chapter_id")
            )
            params.setdefault("work_id", state.get("work_id", ""))
            params.setdefault("user_id", state.get("user_id", ""))
            params.setdefault("conversation_id", state.get("conversation_id", ""))
            # 🔧 2026-01-30: 确保 paragraph_index 是整数或 None
            pi = params.get("paragraph_index")
            if pi is not None and not isinstance(pi, int):
                try:
                    params["paragraph_index"] = int(pi)
                except (ValueError, TypeError):
                    params["paragraph_index"] = None

        # 🆕 2026-01-17: read_paragraph 段落精确读取工具
        elif tool_name == "read_paragraph":
            params.setdefault("work_id", state.get("work_id", ""))
            # chapter_order 和 paragraph_index 必须由 AI 提供
            params.setdefault("context_before", 2)
            params.setdefault("context_after", 2)

        elif tool_name == "evaluate_quality":
            if "text" in params and "content" not in params:
                params["content"] = params.pop("text")
            params.setdefault("content", last_user_message)
            params.setdefault("context", "novel")
            params.setdefault("criteria", ["readability", "creativity", "coherence", "engagement"])
            params.setdefault("reference", "")

        elif tool_name == "analyze_content":
            params.setdefault("content", last_user_message)
            params.setdefault("aspects", ["grammar", "logic", "style", "structure"])
            params.setdefault("analysis_types", ["text", "style"])
            params.setdefault("focus", "all")
            params.setdefault("depth", "normal")
            params.setdefault("context", "")
            params.setdefault("work_id", state.get("work_id", ""))
            params.setdefault("chapter_id", state.get("chapter_id", ""))
            if isinstance(params.get("analysis_types"), str):
                params["analysis_types"] = [
                    item.strip().lower()
                    for item in params["analysis_types"].split(",")
                    if item.strip()
                ]
            if isinstance(params.get("aspects"), str):
                params["aspects"] = [
                    item.strip().lower()
                    for item in params["aspects"].split(",")
                    if item.strip()
                ]

        # 章节管理工具（OPERATION 类）- 需要传递 conversation_id
        elif tool_name == "create_chapter":
            params.setdefault("work_id", state.get("work_id", ""))
            params.setdefault("title", "")
            params.setdefault("content", "")
            params.setdefault("order", None)
            params.setdefault("conversation_id", state.get("conversation_id", ""))

        elif tool_name == "update_chapter_title":
            params.setdefault("chapter_id", state.get("chapter_id", ""))
            params.setdefault("new_title", "")
            params.setdefault("old_title", None)
            params.setdefault("conversation_id", state.get("conversation_id", ""))
            params.setdefault("work_id", state.get("work_id", ""))  # v8.0: 用于章节序号解析

        elif tool_name == "delete_chapter":
            params.setdefault("chapter_id", state.get("chapter_id", ""))
            params.setdefault("chapter_title", None)
            params.setdefault("conversation_id", state.get("conversation_id", ""))
            params.setdefault("work_id", state.get("work_id", ""))  # v8.0: 用于章节序号解析

        elif tool_name == "update_chapter_content":
            params.setdefault("chapter_id", state.get("chapter_id", ""))
            params.setdefault("new_content", "")
            params.setdefault("operation", "replace")
            params.setdefault("position", None)
            params.setdefault("conversation_id", state.get("conversation_id", ""))
            params.setdefault("work_id", state.get("work_id", ""))  # v8.0: 用于章节序号解析

        return params

    async def _augment_insert_context(self, params: dict, state: dict) -> dict:
        """为 smart_insert 动态补充前后文（仅在有定位信息时生效）"""
        if not isinstance(params, dict):
            return params
        source_locator = params.get("source_locator")
        if not isinstance(source_locator, dict):
            return params

        paragraph_index = source_locator.get("paragraph_index")
        if paragraph_index is None:
            paragraph_index = params.get("paragraph_index")
        try:
            paragraph_index = int(paragraph_index) if paragraph_index is not None else None
        except (ValueError, TypeError):
            paragraph_index = None
        if paragraph_index is None:
            return params

        current_context = (params.get("insert_context") or "").strip()
        source_text = (source_locator.get("text") or "").strip()
        # 已有明显扩展上下文时不覆盖
        if current_context and source_text:
            if current_context != source_text and len(current_context) > len(source_text) + 20:
                return params

        ctx_before, ctx_after = self._infer_context_window(params, state)
        if ctx_before <= 0 and ctx_after <= 0:
            return params

        chapter_id = params.get("chapter_id") or source_locator.get("chapter_id") or state.get("chapter_id", "")
        work_id = params.get("work_id") or state.get("work_id", "")
        if not chapter_id:
            return params

        read_params = {
            "work_id": work_id,
            "chapter_order": 0,
            "chapter_id": chapter_id,
            "paragraph_index": paragraph_index,
            "context_before": ctx_before,
            "context_after": ctx_after,
            "index_base": "zero"
        }
        read_result = await read_paragraph.ainvoke(read_params)
        if isinstance(read_result, str):
            try:
                read_result = json.loads(read_result)
            except json.JSONDecodeError:
                read_result = {}
        if not isinstance(read_result, dict) or not read_result.get("success"):
            return params

        context_text = self._build_insert_context_from_read(read_result, ctx_before, ctx_after)

        # 失败时扩读一次（受上限约束）
        max_ctx = 5
        word_count = self._extract_word_count(params, state)
        if (
            word_count
            and word_count >= 120
            and ctx_before < max_ctx
            and ctx_after < max_ctx
            and (not context_text or len(context_text) < 120)
        ):
            ctx_before = min(max_ctx, ctx_before + 1)
            ctx_after = min(max_ctx, ctx_after + 1)
            read_params.update({
                "context_before": ctx_before,
                "context_after": ctx_after
            })
            read_result = await read_paragraph.ainvoke(read_params)
            if isinstance(read_result, str):
                try:
                    read_result = json.loads(read_result)
                except json.JSONDecodeError:
                    read_result = {}
            if isinstance(read_result, dict) and read_result.get("success"):
                context_text = self._build_insert_context_from_read(read_result, ctx_before, ctx_after) or context_text

        if context_text:
            params["insert_context"] = context_text
        return params

    async def _augment_rewrite_context(self, params: dict, state: dict) -> dict:
        """为 smart_rewrite 动态补充前后文（仅在有定位信息时生效）"""
        if not isinstance(params, dict):
            return params
        source_locator = params.get("source_locator")
        if not isinstance(source_locator, dict):
            return params

        paragraph_index = source_locator.get("paragraph_index")
        if paragraph_index is None:
            paragraph_index = params.get("paragraph_index")
        try:
            paragraph_index = int(paragraph_index) if paragraph_index is not None else None
        except (ValueError, TypeError):
            paragraph_index = None
        if paragraph_index is None:
            return params

        evidence_context = str(params.get("evidence_context") or "").strip()
        if evidence_context and "【前文】" in evidence_context and "【后文】" in evidence_context:
            return params

        ctx_before, ctx_after = self._infer_context_window(params, state)
        if ctx_before <= 0 and ctx_after <= 0:
            return params

        chapter_id = params.get("chapter_id") or source_locator.get("chapter_id") or state.get("chapter_id", "")
        work_id = params.get("work_id") or state.get("work_id", "")
        if not chapter_id:
            return params

        read_params = {
            "work_id": work_id,
            "chapter_order": 0,
            "chapter_id": chapter_id,
            "paragraph_index": paragraph_index,
            "context_before": ctx_before,
            "context_after": ctx_after,
            "index_base": "zero"
        }
        read_result = await read_paragraph.ainvoke(read_params)
        if isinstance(read_result, str):
            try:
                read_result = json.loads(read_result)
            except json.JSONDecodeError:
                read_result = {}
        if not isinstance(read_result, dict) or not read_result.get("success"):
            return params

        context_text = self._build_insert_context_from_read(read_result, ctx_before, ctx_after)
        if not context_text:
            return params

        if evidence_context:
            params["evidence_context"] = f"{evidence_context}\n\n【段落上下文】\n{context_text}"
        else:
            params["evidence_context"] = f"【段落上下文】\n{context_text}"
        return params

    @staticmethod
    def _extract_word_count(params: dict, state: dict) -> Optional[int]:
        word_count = params.get("word_count") if isinstance(params, dict) else None
        if isinstance(word_count, int) and word_count > 0:
            return word_count
        user_intent = str(params.get("user_intent") or "")
        user_message = str(state.get("last_user_message") or "")
        text = user_intent or user_message
        if "一句" in text or "一句话" in text:
            return 20
        match = re.search(r"(\d{1,4})\s*字", text)
        if match:
            try:
                return int(match.group(1))
            except (ValueError, TypeError):
                return None
        return None

    def _infer_context_window(self, params: dict, state: dict) -> Tuple[int, int]:
        user_intent = str(params.get("user_intent") or state.get("last_user_message") or "")
        word_count = self._extract_word_count(params, state)
        max_ctx = 5
        if word_count is not None:
            if word_count <= 30:
                ctx = 1
            elif word_count <= 80:
                ctx = 2
            elif word_count <= 150:
                ctx = 3
            elif word_count <= 300:
                ctx = 4
            else:
                ctx = max_ctx
        else:
            ctx = 2

        if any(kw in user_intent for kw in ["一句", "一句话", "简短", "简要", "20字", "30字"]):
            ctx = 1
        if any(kw in user_intent for kw in ["更多上下文", "多读", "前后多段", "详细铺垫"]):
            ctx = max_ctx
        if any(kw in user_intent for kw in ["承接", "铺垫", "过渡", "氛围", "心理", "场景", "细节", "展开", "描写", "扩写", "延展", "补充"]):
            ctx = max(ctx, 3)

        ctx = max(1, min(max_ctx, ctx))
        return ctx, ctx

    @staticmethod
    def _build_insert_context_from_read(read_result: dict, max_before: int, max_after: int) -> str:
        paragraphs = read_result.get("paragraphs")
        if not isinstance(paragraphs, list):
            return ""
        target_index = read_result.get("target_index")
        before_texts = []
        after_texts = []
        target_text = ""
        for para in paragraphs:
            if not isinstance(para, dict):
                continue
            text = (para.get("text") or "").strip()
            if not text:
                continue
            if para.get("is_target"):
                target_text = text
                continue
            if isinstance(target_index, int):
                idx = para.get("index")
                if isinstance(idx, int) and idx < target_index:
                    before_texts.append(text)
                elif isinstance(idx, int) and idx > target_index:
                    after_texts.append(text)
            else:
                if not target_text:
                    before_texts.append(text)
                else:
                    after_texts.append(text)

        if max_before > 0 and len(before_texts) > max_before:
            before_texts = before_texts[-max_before:]
        if max_after > 0 and len(after_texts) > max_after:
            after_texts = after_texts[:max_after]

        parts = []
        if before_texts:
            parts.append("【前文】\n" + "\n".join(before_texts))
        if target_text:
            parts.append("【目标段落】\n" + target_text)
        if after_texts:
            parts.append("【后文】\n" + "\n".join(after_texts))
        return "\n\n".join(parts)

    @staticmethod
    def _load_explore_result(state: dict) -> dict:
        """从共享 state 中读取 explore_content 原始结果"""
        if not isinstance(state, dict):
            return {}
        raw = state.get("last_explore_result")
        if isinstance(raw, dict):
            return raw
        if isinstance(raw, str):
            try:
                parsed = json.loads(raw)
                return parsed if isinstance(parsed, dict) else {}
            except json.JSONDecodeError:
                return {}
        return {}

    def _pick_evidence_text(self, state: dict) -> str:
        """从 explore 结果中挑一条可用原文（用于兜底）"""
        data = self._load_explore_result(state)
        evidences = data.get("evidences") if isinstance(data, dict) else None
        if isinstance(evidences, list):
            for item in evidences:
                if isinstance(item, dict) and item.get("text"):
                    return str(item.get("text"))
        return ""

    def _build_evidence_context(self, state: dict, max_evidences: int = 6, max_chars: int = 1800) -> str:
        """拼接 Explore 证据/定位候选，注入 smart_* 上下文"""
        data = self._load_explore_result(state)
        if not data:
            return ""
        parts = []
        summary = data.get("explore_summary") or data.get("context_for_task")
        if isinstance(summary, str) and summary.strip():
            summary = summary.strip()
            if len(summary) > 400:
                summary = summary[:400] + "..."
            parts.append("【探索摘要】" + summary)

        evidences = data.get("evidences")
        if isinstance(evidences, list) and evidences:
            lines = []
            for item in evidences:
                if not isinstance(item, dict):
                    continue
                text = (item.get("text") or "").strip()
                if not text:
                    continue
                chapter_order = item.get("chapter_order") or item.get("chapter") or ""
                paragraph_index = item.get("paragraph_index")
                node_id = item.get("node_id") or ""
                prefix = []
                if chapter_order:
                    prefix.append(f"第{chapter_order}章")
                if paragraph_index is not None:
                    prefix.append(f"段落{paragraph_index}")
                if node_id:
                    prefix.append(f"node_id={node_id}")
                prefix_text = " ".join(prefix)
                line = f"- {prefix_text}: {text}" if prefix_text else f"- {text}"
                lines.append(line)
                if len(lines) >= max_evidences:
                    break
            if lines:
                parts.append("【探索证据】\n" + "\n".join(lines))

        locate_targets = data.get("locate_targets")
        if isinstance(locate_targets, list) and locate_targets:
            lines = []
            for item in locate_targets[:max_evidences]:
                if not isinstance(item, dict):
                    continue
                chapter_id = item.get("chapter_id") or ""
                paragraph_index = item.get("paragraph_index")
                node_id = item.get("node_id") or ""
                reason = item.get("reason") or ""
                line = f"- chapter_id={chapter_id}, paragraph_index={paragraph_index}, node_id={node_id}"
                if reason:
                    line += f", reason={reason}"
                lines.append(line)
            if lines:
                parts.append("【定位候选】\n" + "\n".join(lines))

        if not parts:
            return ""
        merged = "\n".join(parts)
        if len(merged) > max_chars:
            return merged[:max_chars] + "..."
        return merged

    @staticmethod
    def _extract_target_chapter_id(explore_result: dict) -> tuple[str, str]:
        """从 explore_content 结果中推断目标章节ID与来源。"""
        if not isinstance(explore_result, dict):
            return "", ""
        locate_targets = explore_result.get("locate_targets")
        if isinstance(locate_targets, list):
            for item in locate_targets:
                if isinstance(item, dict) and item.get("chapter_id"):
                    return str(item.get("chapter_id")), "explore.locate_targets"
        evidences = explore_result.get("evidences")
        if isinstance(evidences, list):
            for item in evidences:
                if isinstance(item, dict) and item.get("chapter_id"):
                    return str(item.get("chapter_id")), "explore.evidences"
        chapters = explore_result.get("chapters")
        if isinstance(chapters, list) and len(chapters) == 1:
            entry = chapters[0]
            if isinstance(entry, dict) and entry.get("id"):
                return str(entry.get("id")), "explore.chapters"
        return "", ""

    def _get_target_chapter_id(self, state: dict) -> tuple[str, str]:
        if not isinstance(state, dict):
            return "", ""
        target_id = state.get("target_chapter_id")
        if isinstance(target_id, str) and target_id:
            source = state.get("target_chapter_source") or "state"
            return target_id, str(source)
        explore_result = self._load_explore_result(state)
        return self._extract_target_chapter_id(explore_result)

    @staticmethod
    def _coerce_evidence_context(value: Any) -> str:
        """将 evidence_context 统一为字符串，避免 Pydantic 校验失败。"""
        if value is None:
            return ""
        if isinstance(value, str):
            return value
        if isinstance(value, list):
            lines = []
            for item in value[:6]:
                if isinstance(item, dict):
                    text = item.get("text") or item.get("content") or item.get("snippet") or ""
                    if text:
                        lines.append(str(text))
                elif isinstance(item, str):
                    lines.append(item)
            if lines:
                return "\n".join(lines)
            return json.dumps(value, ensure_ascii=False)
        if isinstance(value, dict):
            text = value.get("text") or value.get("content") or value.get("snippet")
            if isinstance(text, str) and text.strip():
                return text
            return json.dumps(value, ensure_ascii=False)
        return str(value)

    @staticmethod
    def _normalize_locator_text(text: str) -> str:
        if not text:
            return ""
        return re.sub(r"\s+", "", str(text)).strip()

    def _select_locate_target(
        self,
        locate_targets: list,
        text_hint: str = "",
        node_id: Optional[str] = None,
        paragraph_index: Optional[int] = None,
        target_index: Optional[int] = None,
        locator_id: Optional[str] = None,
        target_hint: str = ""
    ) -> tuple[Optional[dict], Optional[dict]]:
        if not isinstance(locate_targets, list) or not locate_targets:
            return None, {
                "error": "missing_locate_targets",
                "message": "缺少可定位段落，请先读取目标段落（read_paragraph/read_paragraphs）。"
            }
        if locator_id:
            matches = []
            for item in locate_targets:
                if not isinstance(item, dict):
                    continue
                if str(item.get("locator_id")) == str(locator_id):
                    matches.append(item)
            if len(matches) == 1:
                return matches[0], None
            if len(matches) > 1:
                return None, {
                    "error": "ambiguous_locator",
                    "message": "定位候选不唯一，请指定第几处或提供更明确的定位信息。"
                }
            return None, {
                "error": "locator_not_found",
                "message": "未找到对应的定位候选，请重新指定目标段落。"
            }
        if isinstance(target_index, int):
            if target_index < 0:
                target_index = len(locate_targets) + target_index
            if 0 <= target_index < len(locate_targets):
                return locate_targets[target_index], None
            return None, {
                "error": "locator_index_out_of_range",
                "message": f"定位候选索引超范围（共{len(locate_targets)}个）"
            }

        if node_id or paragraph_index is not None:
            matches = []
            for item in locate_targets:
                if not isinstance(item, dict):
                    continue
                if node_id and item.get("node_id") == node_id:
                    matches.append(item)
                elif paragraph_index is not None and item.get("paragraph_index") == paragraph_index:
                    matches.append(item)
            if len(matches) == 1:
                return matches[0], None
            if len(matches) > 1:
                return None, {
                    "error": "ambiguous_locator",
                    "message": "定位候选不唯一，请明确指定段落或 node_id。"
                }

        normalized_target_hint = self._normalize_locator_text(target_hint)
        if normalized_target_hint:
            matches = []
            for item in locate_targets:
                if not isinstance(item, dict):
                    continue
                candidate_values = [
                    item.get("text"),
                    item.get("query"),
                    item.get("insert_context"),
                    item.get("before_anchor"),
                    item.get("after_anchor")
                ]
                for candidate in candidate_values:
                    normalized_candidate = self._normalize_locator_text(candidate or "")
                    if not normalized_candidate:
                        continue
                    if (
                        normalized_target_hint == normalized_candidate
                        or normalized_target_hint in normalized_candidate
                        or normalized_candidate in normalized_target_hint
                    ):
                        matches.append(item)
                        break
            if len(matches) == 1:
                return matches[0], None
            if len(matches) > 1:
                return None, {
                    "error": "ambiguous_locator",
                    "message": "多个段落与目标关键词匹配，请指定第几处。"
                }

        normalized_hint = self._normalize_locator_text(text_hint)
        if normalized_hint:
            matches = []
            for item in locate_targets:
                if not isinstance(item, dict):
                    continue
                candidate_text = item.get("text") or item.get("query") or ""
                normalized_candidate = self._normalize_locator_text(candidate_text)
                if not normalized_candidate:
                    continue
                if normalized_hint == normalized_candidate or normalized_hint in normalized_candidate or normalized_candidate in normalized_hint:
                    matches.append(item)
            if len(matches) == 1:
                return matches[0], None
            if len(matches) > 1:
                return None, {
                    "error": "ambiguous_locator",
                    "message": "多个段落与目标文本匹配，请指定第几处。"
                }

        if len(locate_targets) == 1:
            return locate_targets[0], None

        return None, {
            "error": "ambiguous_locator",
            "message": "存在多个定位候选，请指定第几处或提供更明确的定位信息。"
        }

    def _ensure_source_locator(
        self,
        params: Dict[str, Any],
        state: dict,
        text_hint: str = "",
        force: bool = False
    ) -> Optional[Dict[str, Any]]:
        if isinstance(params.get("source_locator"), dict) and not force:
            return None
        explore_result = self._load_explore_result(state)
        locate_targets = explore_result.get("locate_targets") if isinstance(explore_result, dict) else []
        context = state.get("context", {}) if isinstance(state.get("context"), dict) else {}
        locator_id = params.get("locator_id") or params.get("locate_target_id")
        target_hint = params.get("locate_target_hint") or ""
        target_index = params.get("locate_target_index")
        if isinstance(target_index, str):
            stripped = target_index.strip()
            if stripped.lstrip("-").isdigit():
                target_index = int(stripped)
        has_explicit_selection = bool(locator_id or target_hint or target_index is not None)
        node_id = None
        paragraph_index = None
        if not (force and not has_explicit_selection):
            node_id = params.get("node_id") or context.get("locate_node_id")
            paragraph_index = params.get("paragraph_index")
            if paragraph_index is None:
                paragraph_index = context.get("locate_paragraph_index")

        selected, error = self._select_locate_target(
            locate_targets=locate_targets,
            text_hint=text_hint,
            node_id=node_id,
            paragraph_index=paragraph_index,
            target_index=target_index,
            locator_id=locator_id,
            target_hint=target_hint
        )
        if error:
            return error
        if selected and isinstance(selected, dict):
            params["source_locator"] = {
                "chapter_id": selected.get("chapter_id"),
                "paragraph_index": selected.get("paragraph_index"),
                "node_id": selected.get("node_id"),
                "text": selected.get("text") or selected.get("query")
            }
            params["node_id"] = selected.get("node_id")
            params["paragraph_index"] = selected.get("paragraph_index")
        return None

    @staticmethod
    def _validate_source_locator(
        params: Dict[str, Any],
        auto_locator: bool = False
    ) -> Optional[Dict[str, Any]]:
        source_locator = params.get("source_locator")
        if not isinstance(source_locator, dict):
            logger.warning("[ToolExecutor] 缺少 source_locator，阻止写回")
            return {
                "error": "missing_source_locator",
                "message": "缺少 source_locator，无法校验定位一致性，请先完成段落定位。"
            }

        src_node_id = source_locator.get("node_id") or ""
        src_paragraph_index = source_locator.get("paragraph_index")
        if src_paragraph_index is not None and not isinstance(src_paragraph_index, int):
            try:
                src_paragraph_index = int(src_paragraph_index)
            except (ValueError, TypeError):
                src_paragraph_index = None

        if not src_node_id and src_paragraph_index is None:
            logger.warning("[ToolExecutor] source_locator 不完整，阻止写回: %s", source_locator)
            return {
                "error": "invalid_source_locator",
                "message": "source_locator 缺少 node_id/paragraph_index，无法校验定位一致性，请重新定位目标段落。"
            }

        node_id = params.get("node_id")
        paragraph_index = params.get("paragraph_index")
        if node_id and src_node_id and str(node_id) != str(src_node_id):
            logger.error(
                "[ToolExecutor] node_id 与 source_locator 不一致，阻止写回: actual=%s expected=%s",
                node_id,
                src_node_id
            )
            return {
                "error": "source_locator_mismatch",
                "message": "node_id 与 source_locator 不一致，已阻止写回。",
                "expected_node_id": src_node_id,
                "actual_node_id": node_id,
                "auto_locator": auto_locator
            }
        if paragraph_index is not None and src_paragraph_index is not None:
            try:
                actual_pi = int(paragraph_index)
            except (ValueError, TypeError):
                actual_pi = paragraph_index
            if actual_pi != src_paragraph_index:
                logger.error(
                    "[ToolExecutor] paragraph_index 与 source_locator 不一致，阻止写回: actual=%s expected=%s",
                    paragraph_index,
                    src_paragraph_index
                )
                return {
                    "error": "source_locator_mismatch",
                    "message": "paragraph_index 与 source_locator 不一致，已阻止写回。",
                    "expected_paragraph_index": src_paragraph_index,
                    "actual_paragraph_index": paragraph_index,
                    "auto_locator": auto_locator
                }

        if not node_id and src_node_id:
            params["node_id"] = src_node_id
        if paragraph_index is None and src_paragraph_index is not None:
            params["paragraph_index"] = src_paragraph_index

        return None

    async def _autofill_locate_chapter_id(self, tool_args: dict, state: dict) -> dict:
        chapter_id = str(tool_args.get("chapter_id", "") or "").strip()
        state_chapter_id = str(state.get("chapter_id", "") or "").strip()
        ignore_state = self._should_ignore_state_chapter_id(state, tool_args)
        work_id = str(state.get("work_id", "") or "").strip()
        if chapter_id:
            resolved_id = await self._resolve_locate_chapter_id(work_id, chapter_id)
            if resolved_id:
                tool_args["chapter_id"] = resolved_id
                logger.info(
                    "[ToolExecutor] locate_content 章节序号已解析: %s -> %s",
                    chapter_id,
                    resolved_id
                )
            elif is_chapter_order(chapter_id):
                if work_id:
                    logger.warning(
                        "[ToolExecutor] locate_content 章节序号解析失败: chapter_id=%s",
                        chapter_id
                    )
                else:
                    logger.warning(
                        "[ToolExecutor] locate_content 无法解析章节序号，缺少 work_id: chapter_id=%s",
                        chapter_id
                    )
            return tool_args
        if state_chapter_id and not ignore_state:
            resolved_state_id = await self._resolve_locate_chapter_id(work_id, state_chapter_id)
            if resolved_state_id:
                tool_args["chapter_id"] = resolved_state_id
                logger.info(
                    "[ToolExecutor] locate_content 状态章节序号已解析: %s -> %s",
                    state_chapter_id,
                    resolved_state_id
                )
            else:
                tool_args["chapter_id"] = state_chapter_id
                if is_chapter_order(state_chapter_id):
                    if work_id:
                        logger.warning(
                            "[ToolExecutor] locate_content 状态章节序号解析失败: chapter_id=%s",
                            state_chapter_id
                        )
                    else:
                        logger.warning(
                            "[ToolExecutor] locate_content 无法解析状态章节序号，缺少 work_id: chapter_id=%s",
                            state_chapter_id
                        )
            return tool_args

        if not work_id:
            return tool_args

        query = tool_args.get("query") or state.get("last_user_message", "")
        query = str(query).strip()
        if not query:
            return tool_args

        try:
            search_result = await registry.call_tool("search_content", {
                "work_id": work_id,
                "query": query,
                "top_k": 1,
                "chapter_id": "",
                "look_ahead": 0
            })
            chapter_id = self._extract_first_chapter_id(search_result)
            if chapter_id:
                tool_args["chapter_id"] = chapter_id
                logger.info("[ToolExecutor] locate_content 缺少 chapter_id，已通过 search_content 自动补全")
        except Exception as e:
            logger.warning(f"[ToolExecutor] locate_content 自动补全 chapter_id 失败: {e}")

        return tool_args

    @staticmethod
    async def _resolve_locate_chapter_id(work_id: str, chapter_id: str) -> str:
        work_id = str(work_id or "").strip()
        chapter_id = str(chapter_id or "").strip()
        if not work_id or not chapter_id or not is_chapter_order(chapter_id):
            return ""
        resolved_id, error = await resolve_chapter_id(work_id, chapter_id)
        if error:
            logger.warning("[ToolExecutor] locate_content 章节序号解析失败: %s", error)
            return ""
        return str(resolved_id or "").strip()

    @staticmethod
    def _should_ignore_state_chapter_id(state: dict, tool_args: dict) -> bool:
        message = str(state.get("last_user_message", "") or "")
        query = str(tool_args.get("query", "") or "")
        combined = f"{message} {query}".strip()
        if not combined:
            return False

        unknown_hints = [
            "不记得", "记不清", "记不住", "记不得", "想不起来",
            "忘了", "忘记", "不确定", "不知道", "不清楚", "不太记得",
        ]
        chapter_hints = [
            "第几章", "哪章", "哪一章", "哪个章",
            "章节", "哪一节", "第几节",
        ]
        return any(hint in combined for hint in unknown_hints) and any(
            hint in combined for hint in chapter_hints
        )

    @staticmethod
    def _extract_first_chapter_id(search_result: Any) -> str:
        if not isinstance(search_result, dict) or not search_result.get("success"):
            return ""

        data = search_result.get("data", {})
        if not isinstance(data, dict):
            return ""

        results_payload = data.get("results")
        if isinstance(results_payload, str):
            try:
                results_payload = json.loads(results_payload)
            except Exception:
                return ""

        if isinstance(results_payload, dict):
            results_list = results_payload.get("results", [])
        elif isinstance(results_payload, list):
            results_list = results_payload
        else:
            return ""

        if not results_list:
            return ""

        first_item = results_list[0]
        if isinstance(first_item, dict):
            return str(first_item.get("chapter_id", "") or "").strip()
        return ""

    def extract_result(self, tool_name: str, result: dict) -> str:
        """从 StandardTool 返回值中提取实际结果"""
        data = result.get("data", {})

        if tool_name == "continue_writing":
            return data.get("generated_text", "")

        elif tool_name == "analyze_text":
            return data.get("analysis_report", "")

        elif tool_name in ["smart_rewrite", "smart_continue", "smart_insert", "apply_chapter_edit"]:
            return json.dumps(data, ensure_ascii=False)

        elif tool_name == "locate_content":
            # locate_content 返回的 success 在顶层，data 就是整个结果
            # 返回完整 JSON 供下游工具使用
            return json.dumps(result, ensure_ascii=False)

        elif tool_name == "load_explore_artifact":
            # load_explore_artifact 返回 summary 在顶层，需保留完整 JSON
            return json.dumps(result, ensure_ascii=False)

        elif tool_name == "get_context":
            return data.get("context", "")

        elif tool_name == "get_writing_context":
            context = data.get("context", "")
            if context is None:
                return ""
            if isinstance(context, (dict, list)):
                try:
                    return json.dumps(context, ensure_ascii=False)
                except Exception:
                    return str(context)
            return context

        elif tool_name == "read_chapter":
            return data.get("chapter_info", "")

        elif tool_name == "get_chapter_by_order":
            return data.get("chapter_info", "")

        elif tool_name == "search_analysis_fragments":
            return data.get("fragments", "")

        elif tool_name == "search_content":
            return data.get("results", "")

        elif tool_name == "get_worldview_summary":
            # 返回 JSON 字符串格式的世界观摘要
            return json.dumps(data, ensure_ascii=False)

        elif tool_name == "evaluate_quality":
            feedback = data.get("feedback", "")
            overall_score = data.get("overall_score", 0)
            grade = data.get("grade", "B")
            return f"评分: {overall_score}/100 (等级: {grade})\n\n{feedback}"

        elif tool_name == "analyze_content":
            return data.get("analysis", data.get("summary", ""))

        # 🆕 2026-01-18: explore_content 深度探索工具
        elif tool_name == "explore_content":
            # explore_content 返回的 JSON 结构不包含 data 字段
            return json.dumps(result, ensure_ascii=False)

        # 🆕 2026-01-23: operate_apply 统一操作工具
        elif tool_name == "operate_apply":
            return json.dumps(data, ensure_ascii=False)

        # 章节管理工具（OPERATION 类）- 返回完整 JSON 供 HITL 处理
        elif tool_name in ["create_chapter", "update_chapter_title", "delete_chapter", "update_chapter_content"]:
            return json.dumps(data, ensure_ascii=False)

        return json.dumps(data, ensure_ascii=False)

    async def fallback_to_legacy(
        self,
        tool_name: str,
        tool_args: dict,
        state: dict
    ) -> str:
        """降级到 @tool 版本（向后兼容）"""
        from app.services.agent.langgraph_tools import (
            analyze_text_tool,
            analyze_content,
            get_worldview_summary,
            get_writing_context,
            search_content,
            read_paragraph,
            explore_content,
        )
        from app.services.agent.tools.editor_tools import (
            smart_rewrite,
            smart_continue,
            smart_insert,
            apply_chapter_edit,
        )
        from app.services.agent.tools.operate_tools import operate_apply
        from app.services.agent.tools.show_dont_tell import (
            show_emotion_tool,
            enhance_scene_tool,
        )
        from app.services.agent.tools.style_learning import (
            learn_style_tool,
            analyze_style_tool,
            get_style_guidance_tool,
        )
        from app.services.agent.tools.chapter_tools import (
            create_chapter,
            update_chapter_title,
            delete_chapter,
            update_chapter_content,
        )
        from app.services.agent.tools.consistency_checker import (
            check_story_consistency_tool,
        )

        last_user_message = state.get("last_user_message", "")

        LEGACY_TOOLS = {
            "analyze_text_tool": analyze_text_tool,
            "analyze_content": analyze_content,
            "smart_rewrite": smart_rewrite,
            "smart_continue": smart_continue,
            "smart_insert": smart_insert,
            "apply_chapter_edit": apply_chapter_edit,
            "get_worldview_summary": get_worldview_summary,
            # 聚合工具（2026-01-12）
            "get_writing_context": get_writing_context,
            "search_content": search_content,
            # 深度探索工具（2026-01-17）
            "read_paragraph": read_paragraph,
            "explore_content": explore_content,
            # 统一操作工具（2026-01-23）
            "operate_apply": operate_apply,
            # 创作增强工具
            "show_emotion_tool": show_emotion_tool,
            "enhance_scene_tool": enhance_scene_tool,
            "learn_style_tool": learn_style_tool,
            "analyze_style_tool": analyze_style_tool,
            "get_style_guidance_tool": get_style_guidance_tool,
            # 章节操作工具
            "create_chapter": create_chapter,
            "update_chapter_title": update_chapter_title,
            "delete_chapter": delete_chapter,
            "update_chapter_content": update_chapter_content,
            # 分析工具
            "check_story_consistency_tool": check_story_consistency_tool,
        }

        legacy_tool = LEGACY_TOOLS.get(tool_name)
        if legacy_tool:
            logger.info(f"[LegacyTool] 使用 @tool 版本: {tool_name}")
            try:
                if tool_name == "analyze_text_tool":
                    params = {
                        "text": tool_args.get("text", last_user_message),
                        "focus": tool_args.get("focus", "all")
                    }
                elif tool_name == "analyze_content":
                    params = {
                        "content": tool_args.get("content", last_user_message),
                        "text": tool_args.get("text", ""),
                        "analysis_types": tool_args.get("analysis_types", "text,style"),
                        "focus": tool_args.get("focus", "all"),
                        "depth": tool_args.get("depth", "normal"),
                        "context": tool_args.get("context", ""),
                        "work_id": tool_args.get("work_id", state.get("work_id", "")),
                        "chapter_id": tool_args.get("chapter_id", state.get("chapter_id", ""))
                    }
                elif tool_name == "get_worldview_summary":
                    params = {
                        "work_id": tool_args.get("work_id", state.get("work_id", ""))
                    }
                elif tool_name == "search_content":
                    params = {
                        "work_id": tool_args.get("work_id", state.get("work_id", "")),
                        "query": tool_args.get("query", last_user_message),
                        "top_k": tool_args.get("top_k", 10),
                        "chapter_id": tool_args.get("chapter_id", state.get("chapter_id", "")),
                        "look_ahead": tool_args.get("look_ahead", 0),
                    }
                elif tool_name == "show_emotion_tool":
                    params = {
                        "emotion": tool_args.get("emotion", ""),
                        "intensity": tool_args.get("intensity", 3)
                    }
                elif tool_name == "enhance_scene_tool":
                    params = {
                        "description": tool_args.get("description", tool_args.get("text", last_user_message))
                    }
                elif tool_name == "analyze_style_tool":
                    params = {
                        "text": tool_args.get("text", last_user_message)
                    }
                elif tool_name == "learn_style_tool":
                    params = {
                        "user_id": tool_args.get("user_id", state.get("user_id", "")),
                        "text": tool_args.get("text", last_user_message),
                        "profile_name": tool_args.get("profile_name", "default")
                    }
                elif tool_name == "get_style_guidance_tool":
                    params = {
                        "user_id": tool_args.get("user_id", state.get("user_id", "")),
                        "profile_name": tool_args.get("profile_name", "default")
                    }
                # 章节操作工具
                elif tool_name == "create_chapter":
                    params = {
                        "work_id": tool_args.get("work_id", state.get("work_id", "")),
                        "title": tool_args.get("title", ""),
                        "content": tool_args.get("content", ""),
                        "order": tool_args.get("order"),
                        "conversation_id": tool_args.get("conversation_id", state.get("conversation_id", ""))
                    }
                elif tool_name == "update_chapter_title":
                    params = {
                        "chapter_id": tool_args.get("chapter_id", state.get("chapter_id", "")),
                        "new_title": tool_args.get("new_title", ""),
                        "old_title": tool_args.get("old_title"),
                        "conversation_id": tool_args.get("conversation_id", state.get("conversation_id", "")),
                        "work_id": tool_args.get("work_id", state.get("work_id", ""))
                    }
                elif tool_name == "delete_chapter":
                    params = {
                        "chapter_id": tool_args.get("chapter_id", state.get("chapter_id", "")),
                        "chapter_title": tool_args.get("chapter_title"),
                        "conversation_id": tool_args.get("conversation_id", state.get("conversation_id", "")),
                        "work_id": tool_args.get("work_id", state.get("work_id", ""))
                    }
                elif tool_name == "update_chapter_content":
                    params = {
                        "chapter_id": tool_args.get("chapter_id", state.get("chapter_id", "")),
                        "new_content": tool_args.get("new_content", tool_args.get("content", "")),
                        "operation": tool_args.get("operation", "replace"),
                        "position": tool_args.get("position"),
                        "conversation_id": tool_args.get("conversation_id", state.get("conversation_id", "")),
                        "work_id": tool_args.get("work_id", state.get("work_id", ""))
                    }
                elif tool_name == "apply_chapter_edit":
                    # 🔧 2026-01-13: 添加调试日志
                    logger.info(f"[apply_chapter_edit] tool_args: chapter_id={tool_args.get('chapter_id')}, content_len={len(tool_args.get('content', '')) if tool_args.get('content') else 0}")
                    params = {
                        "chapter_id": tool_args.get("chapter_id", state.get("chapter_id", "")),
                        "content": tool_args.get("content", ""),
                        "operation": tool_args.get("operation", "replace"),
                        "position": tool_args.get("position"),
                        "before_anchor": tool_args.get("before_anchor"),
                        "after_anchor": tool_args.get("after_anchor"),
                        "original_text": tool_args.get("original_text"),
                        "node_id": tool_args.get("node_id"),
                        "paragraph_index": tool_args.get("paragraph_index"),
                        "user_id": tool_args.get("user_id", state.get("user_id", "")),
                        "description": tool_args.get("description"),
                        "conversation_id": tool_args.get("conversation_id", state.get("conversation_id", "")),
                        "work_id": tool_args.get("work_id", state.get("work_id", ""))
                    }
                # 分析工具
                elif tool_name == "check_story_consistency_tool":
                    params = {
                        "work_id": tool_args.get("work_id", state.get("work_id", "")),
                        "chapters_json": tool_args.get("chapters_json", "[]"),
                        "characters_json": tool_args.get("characters_json", "[]"),
                        "worldview_json": tool_args.get("worldview_json", "{}")
                    }
                # 聚合工具（2026-01-12）
                elif tool_name == "get_writing_context":
                    params = {
                        "work_id": tool_args.get("work_id", state.get("work_id", "")),
                        "chapter_id": tool_args.get("chapter_id", state.get("chapter_id", "")),
                        "chapter_orders": tool_args.get("chapter_orders", ""),
                        "user_id": tool_args.get("user_id", state.get("user_id", "")),
                        "include": tool_args.get("include", "work,chapter,worldview,style,rag"),
                        "rag_query": tool_args.get("rag_query", ""),
                        "rag_top_k": tool_args.get("rag_top_k", 5),
                        "use_cache": tool_args.get("use_cache", True)
                    }
                # 深度探索工具（2026-01-17）
                elif tool_name == "read_paragraph":
                    chapter_order = tool_args.get("chapter_order")
                    paragraph_index = tool_args.get("paragraph_index")
                    # 验证必需参数
                    if chapter_order is None or paragraph_index is None:
                        return json.dumps({
                            "success": False,
                            "error": f"缺少必需参数: chapter_order={chapter_order}, paragraph_index={paragraph_index}"
                        }, ensure_ascii=False)
                    params = {
                        "work_id": tool_args.get("work_id", state.get("work_id", "")),
                        "chapter_order": int(chapter_order),
                        "paragraph_index": int(paragraph_index),
                        "context_before": tool_args.get("context_before") or 2,
                        "context_after": tool_args.get("context_after") or 2
                    }
                elif tool_name == "explore_content":
                    params = {
                        "work_id": tool_args.get("work_id", state.get("work_id", "")),
                        "target_task": tool_args.get("target_task", ""),
                        "max_rounds": tool_args.get("max_rounds", 10),
                        "user_id": tool_args.get("user_id", state.get("user_id", ""))
                    }
                elif tool_name == "operate_apply":
                    context = state.get("context", {}) if isinstance(state.get("context"), dict) else {}
                    state_chapter_id = state.get("chapter_id")
                    target_chapter_id = tool_args.get("chapter_id") or state_chapter_id
                    same_chapter = True
                    if target_chapter_id and state_chapter_id and target_chapter_id != state_chapter_id:
                        same_chapter = False
                    params = {
                        "operation": tool_args.get("operation", "append"),
                        "chapter_id": tool_args.get("chapter_id", state.get("chapter_id", "")),
                        "work_id": tool_args.get("work_id", state.get("work_id", "")),
                        "content": tool_args.get("content"),
                        "title": tool_args.get("title"),
                        "original_text": tool_args.get("original_text"),
                        "target_description": tool_args.get("target_description"),
                        "paragraph_index": tool_args.get("paragraph_index"),
                        "node_id": tool_args.get("node_id"),
                        "nodes_info": tool_args.get("nodes_info"),
                        "user_id": tool_args.get("user_id", state.get("user_id", "")),
                        "conversation_id": tool_args.get("conversation_id", state.get("conversation_id", "")),
                    }
                    if same_chapter:
                        if not params.get("original_text") and context.get("locate_original_text"):
                            params["original_text"] = context.get("locate_original_text")
                        if params.get("node_id") is None and context.get("locate_node_id"):
                            params["node_id"] = context.get("locate_node_id")
                        if params.get("paragraph_index") is None and context.get("locate_paragraph_index") is not None:
                            params["paragraph_index"] = context.get("locate_paragraph_index")
                        if params.get("nodes_info") is None and context.get("nodes_info"):
                            params["nodes_info"] = context.get("nodes_info")
                    nodes_info = params.get("nodes_info")
                    if nodes_info is not None and not isinstance(nodes_info, str):
                        params["nodes_info"] = json.dumps(nodes_info, ensure_ascii=False)
                    pi = params.get("paragraph_index")
                    if pi is not None and not isinstance(pi, int):
                        try:
                            params["paragraph_index"] = int(pi)
                        except (ValueError, TypeError):
                            params["paragraph_index"] = None
                else:
                    params = tool_args

                result = await legacy_tool.ainvoke(params)

                # 🆕 2026-01-18: explore_content 返回完整 JSON，不在此处提取 explore_summary
                # 让 parallel_executor 可以解析 frontend_display 并发射事件
                # explore_summary 的提取移到 parallel_executor 中进行
                return result
            except Exception as e:
                logger.error(f"[LegacyTool] 调用失败: {e}")
                return json.dumps({"error": "legacy_tool_failed", "message": str(e)}, ensure_ascii=False)

        logger.error(f"[ToolCall] 未知工具: {tool_name}")
        return json.dumps({"error": "unknown_tool", "message": f"未知工具: {tool_name}"}, ensure_ascii=False)

    def _read_cover_cache(
        self,
        tool_name: str,
        params: dict,
        state: dict
    ) -> Optional[str]:
        if tool_name == "get_writing_context":
            cached = ToolCache.read_covering_gwc(params, state)
            if cached is None:
                return None
            include_set = self._normalize_include_set(params.get("include"))
            filtered = self._filter_gwc_context(cached, include_set)
            return filtered or cached

        if tool_name in GWC_ALIAS_TOOL_INCLUDES:
            gwc_params = self._build_gwc_params_for_alias(tool_name, params, state)
            cached = ToolCache.read_covering_gwc(gwc_params, state)
            if cached is None:
                return None
            converted = self._convert_gwc_to_alias(tool_name, cached)
            if converted is not None:
                return converted
        return None

    @staticmethod
    def _normalize_include_set(include_value: Any) -> set:
        if include_value is None:
            return set()
        if isinstance(include_value, str):
            return set(item.strip() for item in include_value.split(",") if item.strip())
        if isinstance(include_value, (list, tuple, set)):
            return set(str(item).strip() for item in include_value if str(item).strip())
        return set([str(include_value).strip()])

    @staticmethod
    def _load_gwc_context(result_str: str) -> Optional[Dict[str, Any]]:
        if not isinstance(result_str, str) or not result_str.strip():
            return None
        try:
            data = json.loads(result_str)
        except Exception:
            return None
        return data if isinstance(data, dict) else None

    def _filter_gwc_context(self, result_str: str, include_set: set) -> Optional[str]:
        if not include_set:
            return None
        data = self._load_gwc_context(result_str)
        if not data:
            return None
        keep_keys = {"work_id"}
        if "work" in include_set:
            keep_keys.add("work_info")
        if "chapter" in include_set:
            keep_keys.add("chapters")
        if "worldview" in include_set:
            keep_keys.add("worldview")
        if "style" in include_set:
            keep_keys.add("style_guidance")
        if "rag" in include_set:
            keep_keys.add("rag_context")
        filtered = {k: v for k, v in data.items() if k in keep_keys}
        return json.dumps(filtered, ensure_ascii=False, indent=2)

    def _build_gwc_params_for_alias(
        self,
        tool_name: str,
        params: dict,
        state: dict
    ) -> dict:
        include_value = GWC_ALIAS_TOOL_INCLUDES.get(tool_name, "")
        gwc_params = {
            "work_id": params.get("work_id") or state.get("work_id", ""),
            "chapter_id": params.get("chapter_id") or state.get("chapter_id", ""),
            "chapter_orders": "",
            "user_id": params.get("user_id") or state.get("user_id", ""),
            "include": include_value,
            "rag_query": "",
            "rag_top_k": 5,
            "use_cache": params.get("use_cache", True)
        }
        if tool_name == "get_chapter_by_order":
            gwc_params["chapter_orders"] = str(params.get("chapter_order") or "").strip()
        return gwc_params

    def _convert_gwc_to_alias(self, tool_name: str, result_str: str) -> Optional[str]:
        data = self._load_gwc_context(result_str)
        if not data:
            return None

        if tool_name in {"read_chapter", "get_chapter_by_order"}:
            chapters = data.get("chapters", [])
            if not isinstance(chapters, list):
                return None
            if len(chapters) == 1:
                payload = self._format_chapter_payload(chapters[0])
                return json.dumps(payload, ensure_ascii=False, indent=2)
            if len(chapters) > 1:
                return json.dumps({
                    "type": "multi_chapter",
                    "count": len(chapters),
                    "chapters": [self._format_chapter_payload(ch) for ch in chapters]
                }, ensure_ascii=False, indent=2)
            return None

        if tool_name == "get_context":
            converted = {
                "work_id": data.get("work_id"),
                "work_info": data.get("work_info", {}),
                "current_chapter": {},
                "related_context": data.get("rag_context", [])
            }
            chapters = data.get("chapters", [])
            if chapters:
                ch = chapters[0]
                content = ch.get("content", "") if isinstance(ch, dict) else ""
                converted["current_chapter"] = {
                    "chapter_id": ch.get("id") if isinstance(ch, dict) else "",
                    "title": ch.get("title") if isinstance(ch, dict) else "",
                    "order": ch.get("order") if isinstance(ch, dict) else None,
                    "content_preview": content[:1000],
                    "word_count": ch.get("word_count") if isinstance(ch, dict) else None
                }
            return json.dumps(converted, ensure_ascii=False, indent=2)

        if tool_name == "get_worldview_summary":
            worldview = data.get("worldview", {}) if isinstance(data.get("worldview"), dict) else {}
            converted = {
                "total": {
                    "characters": len(worldview.get("characters", [])),
                    "locations": len(worldview.get("locations", [])),
                    "settings": len(worldview.get("settings", []))
                },
                "characters": worldview.get("characters", []),
                "locations": worldview.get("locations", []),
                "settings": worldview.get("settings", [])
            }
            return json.dumps(converted, ensure_ascii=False, indent=2)

        return None

    @staticmethod
    def _format_chapter_payload(chapter: Dict[str, Any]) -> Dict[str, Any]:
        content = chapter.get("content", "") or ""
        return {
            "chapter_id": chapter.get("chapter_id") or chapter.get("id"),
            "title": chapter.get("title"),
            "order": chapter.get("order"),
            "content": content,
            "content_length": len(content),
            "word_count": chapter.get("word_count"),
            "status": chapter.get("status", "unknown")
        }

    # ==================== 章节缓存方法 ====================

    def _check_chapter_cache(
        self,
        tool_name: str,
        tool_args: dict,
        state: dict
    ) -> Optional[str]:
        """检查章节缓存

        Args:
            tool_name: 工具名称（read_chapter 或 get_chapter_by_order）
            tool_args: 工具参数
            state: Agent 状态

        Returns:
            缓存命中时返回结果字符串，否则返回 None
        """
        work_id = tool_args.get("work_id") or state.get("work_id", "")

        if tool_name == "read_chapter":
            chapter_id = tool_args.get("chapter_id")
            if chapter_id and "," not in chapter_id:  # 单章节才检查缓存
                cached = ChapterCache.get_by_id(state, chapter_id)
                if cached:
                    payload = self._format_chapter_payload(cached)
                    return json.dumps(payload, ensure_ascii=False, indent=2)

        elif tool_name == "get_chapter_by_order":
            chapter_order = str(tool_args.get("chapter_order", "1"))
            # 只对单章节检查缓存（不含逗号和横杠）
            if chapter_order.isdigit():
                order = int(chapter_order)
                cached = ChapterCache.get_by_order(state, work_id, order)
                if cached:
                    payload = self._format_chapter_payload(cached)
                    return json.dumps(payload, ensure_ascii=False, indent=2)

        return None

    def _update_chapter_cache(
        self,
        tool_name: str,
        result: dict,
        state: dict
    ) -> None:
        """更新章节缓存

        Args:
            tool_name: 工具名称
            result: 工具返回结果
            state: Agent 状态
        """
        if not isinstance(result, dict) or not result.get("success"):
            return

        data = result.get("data", {})
        work_id = state.get("work_id", "")

        # 解析章节数据
        chapter_info = data.get("chapter_info")
        if not chapter_info:
            return

        try:
            if isinstance(chapter_info, str):
                chapter_info = json.loads(chapter_info)

            # 单章节
            if isinstance(chapter_info, dict) and "chapter_id" in chapter_info:
                ChapterCache.set(state, chapter_info, work_id)
            # 多章节
            elif isinstance(chapter_info, dict) and "chapters" in chapter_info:
                ChapterCache.set_batch(state, chapter_info["chapters"], work_id)
        except Exception as e:
            logger.warning(f"[ChapterCache] 缓存写入失败: {e}")

    # ==================== get_writing_context 缓存方法 ====================

    def _check_writing_context_cache(
        self,
        tool_args: dict,
        state: dict
    ) -> Optional[str]:
        """检查 get_writing_context 的章节缓存

        如果请求的所有章节都在缓存中，直接返回缓存结果。
        注意：只有当 include 仅包含 chapter 时才使用缓存，
        因为 worldview/rag 等数据需要实时查询。

        Args:
            tool_args: 工具参数
            state: Agent 状态

        Returns:
            缓存命中时返回结果字符串，否则返回 None
        """
        work_id = tool_args.get("work_id") or state.get("work_id", "")
        include_value = tool_args.get("include", "work,chapter,worldview,style,rag")
        if isinstance(include_value, (list, tuple, set)):
            include_value = ",".join([str(i).strip() for i in include_value if str(i).strip()])

        # 只有当 include 仅包含 chapter 时才使用缓存
        include_set = set(i.strip() for i in str(include_value).split(",") if i.strip())
        if include_set != {"chapter"}:
            # 包含其他数据类型，无法使用缓存
            return None

        chapter_orders = tool_args.get("chapter_orders", "")
        chapter_id = tool_args.get("chapter_id", "")

        # 解析章节序号
        if chapter_orders:
            orders = self._parse_chapter_orders(chapter_orders)
            if not orders:
                return None

            # 检查所有章节是否都在缓存中
            cached_chapters = []
            for order in orders:
                cached = ChapterCache.get_by_order(state, work_id, order)
                if not cached:
                    return None  # 有一章未命中，放弃缓存
                cached_chapters.append({
                    "id": cached.get("chapter_id"),
                    "title": cached.get("title"),
                    "order": cached.get("order"),
                    "content": cached.get("content", ""),
                    "word_count": cached.get("word_count")
                })

            logger.info(f"[ChapterCache] ✅ get_writing_context 缓存命中: {len(cached_chapters)} 章")
            return json.dumps({
                "work_id": work_id,
                "chapters": cached_chapters
            }, ensure_ascii=False, indent=2)

        elif chapter_id:
            cached = ChapterCache.get_by_id(state, chapter_id)
            if cached:
                logger.info(f"[ChapterCache] ✅ get_writing_context 缓存命中: {chapter_id[:8]}...")
                return json.dumps({
                    "work_id": work_id,
                    "chapters": [{
                        "id": cached.get("chapter_id"),
                        "title": cached.get("title"),
                        "order": cached.get("order"),
                        "content": cached.get("content", ""),
                        "word_count": cached.get("word_count")
                    }]
                }, ensure_ascii=False, indent=2)

        return None

    def _update_writing_context_cache(
        self,
        result: dict,
        state: dict
    ) -> None:
        """更新 get_writing_context 返回的章节缓存

        Args:
            result: 工具返回结果
            state: Agent 状态
        """
        if not isinstance(result, dict) or not result.get("success"):
            return

        data = result.get("data", {})
        work_id = state.get("work_id", "")

        # 从 context 字段解析章节数据
        context_str = data.get("context")
        if not context_str:
            return

        try:
            if isinstance(context_str, str):
                context_data = json.loads(context_str)
            else:
                context_data = context_str

            chapters = context_data.get("chapters", [])
            if not chapters:
                return

            # 转换格式并写入缓存
            for ch in chapters:
                if isinstance(ch, dict) and ch.get("id"):
                    chapter_data = {
                        "chapter_id": ch.get("id"),
                        "title": ch.get("title"),
                        "order": ch.get("order"),
                        "content": ch.get("content", ""),
                        "word_count": ch.get("word_count")
                    }
                    ChapterCache.set(state, chapter_data, work_id)

            logger.info(f"[ChapterCache] 📝 get_writing_context 缓存写入: {len(chapters)} 章")

        except Exception as e:
            logger.warning(f"[ChapterCache] get_writing_context 缓存写入失败: {e}")

    def _parse_chapter_orders(self, chapter_order: str) -> list:
        """解析章节序号参数"""
        if isinstance(chapter_order, int):
            return [chapter_order]

        chapter_order = str(chapter_order).strip()

        # 范围格式 "1-5"
        if "-" in chapter_order and "," not in chapter_order:
            parts = chapter_order.split("-")
            if len(parts) == 2:
                try:
                    start = int(parts[0].strip())
                    end = int(parts[1].strip())
                    if start <= end:
                        return list(range(start, end + 1))
                except ValueError:
                    pass

        # 多个格式 "1,2,3"
        if "," in chapter_order:
            orders = []
            for part in chapter_order.split(","):
                try:
                    orders.append(int(part.strip()))
                except ValueError:
                    continue
            return sorted(set(orders))

        # 单个格式 "1"
        try:
            return [int(chapter_order)]
        except ValueError:
            return []

    @staticmethod
    def _resolve_tool_policy(state: dict) -> str:
        if not isinstance(state, dict):
            return "auto"
        policy = str(state.get("tool_policy") or "").strip().lower()
        if policy in {"auto", "no_tool", "cache_only"}:
            return policy
        return "auto"

