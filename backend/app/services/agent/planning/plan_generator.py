# -*- coding: utf-8 -*-
"""
规划生成器

从 langgraph_agent.py 的 chat_with_planning 方法中提取的规划生成逻辑：
- 构建规划 Prompt
- 调用 AI 生成规划
- 解析规划 JSON
- 规划后处理（验收标准、checkpoint）
"""

import asyncio
import copy
import json
import logging
import os
import re
from typing import Dict, List, Any, Optional, TYPE_CHECKING, Tuple

from pydantic import ValidationError

import httpx

if TYPE_CHECKING:
    from app.services.agent.langgraph_agent import WritingAgentGraph

logger = logging.getLogger(__name__)


class PlanGenerator:
    """规划生成器 - 生成任务规划"""

    # 规划重试配置
    MAX_PLANNING_RETRIES = 2
    EDIT_CONTENT_TOOLS = {"smart_rewrite", "smart_insert"}
    EDIT_OPERATION_TOOLS = {"operate_apply", "apply_chapter_edit"}
    EDIT_OPERATIONS = {"replace", "insert"}
    INTERNAL_EXPLORE_TOOLS = {
        "list_chapters",
        "list_paragraphs",
        "read_paragraphs",
    }
    LEGACY_EXPLORE_TOOL_ALIASES = {
        "read_paragraph_tool": "read_paragraph",
        "read_paragraphs_tool": "read_paragraphs",
        "list_paragraphs_tool": "list_paragraphs",
        "list_chapters_tool": "list_chapters",
    }
    FRESHNESS_KEYWORDS = (
        "重新", "最新", "更新", "再查", "再次", "再搜", "再探索", "重新探索",
        "重新搜索", "重做", "不要复用", "忽略历史", "不使用历史", "不要用历史"
    )

    def __init__(self, agent: "WritingAgentGraph"):
        """
        初始化规划生成器

        Args:
            agent: WritingAgentGraph 实例
        """
        self.agent = agent

    async def generate_plan(
        self,
        message: str,
        work_id: Optional[str] = None,
        chapter_id: Optional[str] = None,
        context: Optional[Dict[str, Any]] = None,
        conversation_history: str = ""
    ) -> Dict[str, Any]:
        """
        生成任务规划

        Args:
            message: 用户消息
            work_id: 作品ID
            chapter_id: 章节ID
            context: 额外上下文
            conversation_history: 对话历史
        Returns:
            规划数据字典，包含 tasks 列表
        """
        from app.services.agent.utils.monitoring import increment_counter
        from app.services.agent.model_selector import TaskType

        increment_counter("planning_phase_start")
        logger.info(f"[Planning] 开始规划: {message[:50]}...")

        tool_policy = self._resolve_tool_policy(context)
        if tool_policy == "no_tool":
            direct_answer = await self._generate_direct_answer(
                message=message,
                conversation_history=conversation_history,
                context=context
            )
            if not direct_answer:
                direct_answer = "抱歉，当前策略禁止调用工具，且上下文不足以生成可靠答复。"
            return {
                "user_intent": "直接回答（禁用工具）",
                "direct_answer": direct_answer,
                "tasks": []
            }

        # 构建规划 prompt（异步）
        plan_prompt_base = await self._build_plan_prompt_async(
            message=message,
            work_id=work_id,
            chapter_id=chapter_id,
            context=context,
            conversation_history=conversation_history
        )
        # 🔧 2026-01-21: 禁用枚举项检测功能
        # 原因：提取算法误判严重，产生大量噪音（如"干了"、"需要回答"），触发无意义重试
        # enumerated_items = self._extract_enumerated_items(message)
        # if enumerated_items:
        #     logger.info(f"[Planning] 检测到枚举项: {enumerated_items}")

        # 调用 AI 生成规划
        plan_text = ""
        plan_data = None

        try:
            response_format = {"type": "json_object"}
            for retry_attempt in range(self.MAX_PLANNING_RETRIES):
                # 🔧 2025-12-29: 规划任务需要理解对话上下文，使用 STORY_PLANNING 选择更强模型
                plan_result = await self.agent._generate_text(
                    prompt=plan_prompt_base,
                    temperature=0.3 + (retry_attempt * 0.1),
                    max_tokens=2000,
                    task_type=TaskType.STORY_PLANNING,
                    response_format=response_format
                )
                plan_text = plan_result.get("text", "").strip()

                if plan_text:
                    plan_data = self.agent._extract_json_from_text(plan_text)
                    # 🆕 支持 direct_answer：如果 AI 决定直接回答，tasks 可以为空
                    if plan_data:
                        # 🔧 严格空值检查：排除空字符串和空白字符串
                        raw_direct_answer = plan_data.get("direct_answer")
                        has_direct_answer = (
                            raw_direct_answer is not None
                            and isinstance(raw_direct_answer, str)
                            and raw_direct_answer.strip()
                        )
                        has_tasks = plan_data.get("tasks") and len(plan_data.get("tasks", [])) > 0
                        if has_direct_answer or has_tasks:
                            # 🔧 2026-01-21: 禁用枚举项覆盖检查，不再触发重试
                            if retry_attempt > 0:
                                logger.info(f"[Planning] 第{retry_attempt + 1}次重试成功")
                            # 🆕 日志：记录是直接回答还是任务规划
                            if has_direct_answer and not has_tasks:
                                logger.info(f"[Planning] AI 决定直接回答，跳过任务执行")
                            break
                    else:
                        logger.warning(f"[Planning] 第{retry_attempt + 1}次尝试: JSON解析失败")
                        logger.warning(f"[Planning] JSON解析失败原文: {plan_text}")
                else:
                    logger.warning(f"[Planning] 第{retry_attempt + 1}次尝试: AI返回空响应")

                if retry_attempt < self.MAX_PLANNING_RETRIES - 1:
                    await asyncio.sleep(1)

            # 记录 thinking 字段用于调试
            if plan_data and "thinking" in plan_data:
                thinking = plan_data["thinking"]
                logger.info(
                    f"[Planning] 思维链: "
                    f"输出={thinking.get('step1_output', '?')[:30]}, "
                    f"原料={thinking.get('step2_material', '?')[:20]}, "
                    f"处理={thinking.get('step3_process', '?')[:20]}"
                )

        except Exception as e:
            logger.error(f"[Planning Agent] 执行失败: {e}", exc_info=True)
            plan_data = self._handle_planning_error(e)
            if plan_data is None:
                raise

        # 如果解析失败，使用默认规划
        if not plan_data:
            logger.warning(f"[Planning] 无法解析规划JSON，AI返回: {plan_text[:500]}")

        # 🆕 支持 direct_answer：有直接回答时不需要创建默认规划
        # 🔧 严格空值检查
        if not plan_data:
            plan_data = self._create_default_plan()
        else:
            raw_direct_answer = plan_data.get("direct_answer")
            has_valid_direct_answer = (
                raw_direct_answer is not None
                and isinstance(raw_direct_answer, str)
                and raw_direct_answer.strip()
            )
            has_tasks = plan_data.get("tasks") and len(plan_data.get("tasks", [])) > 0

            if not has_valid_direct_answer and not has_tasks:
                # 没有有效的 direct_answer 也没有 tasks，创建默认规划
                plan_data = self._create_default_plan()

        # 🆕 如果是直接回答模式，确保 tasks 为空列表
        raw_direct_answer = plan_data.get("direct_answer")
        has_valid_direct_answer = (
            raw_direct_answer is not None
            and isinstance(raw_direct_answer, str)
            and raw_direct_answer.strip()
        )
        if has_valid_direct_answer:
            if not plan_data.get("tasks"):
                plan_data["tasks"] = []
            logger.info(f"[Planning] 直接回答模式，答案长度: {len(raw_direct_answer)}")
        else:
            # 规划后处理（只对有任务的规划进行）
            plan_data = self._post_process_plan(
                plan_data,
                message,
                context=context,
                work_id=work_id
            )

        increment_counter("planning_phase_completed")
        logger.info(f"[Planning] 规划生成成功，共{len(plan_data['tasks'])}个任务")

        return plan_data

    async def _build_plan_prompt_async(
        self,
        message: str,
        work_id: Optional[str],
        chapter_id: Optional[str],
        context: Optional[Dict[str, Any]],
        conversation_history: str
    ) -> str:
        """
        异步构建规划 Prompt

        Args:
            message: 用户消息
            work_id: 作品ID
            chapter_id: 章节ID
            context: 额外上下文
            conversation_history: 对话历史
        Returns:
            规划 prompt 字符串
        """
        from app.services.agent.prompts import get_planning_static_prompt

        # 历史部分
        history_section = ""
        if conversation_history:
            history_section = f"""
【对话历史】
{conversation_history}

"""

        # 获取静态 Prompt
        static_prompt = await get_planning_static_prompt()

        # 知识库文档部分
        knowledge_section = self._build_knowledge_section(context)

        # 选中文本部分
        selected_text_section = self._build_selected_text_section(context)

        # 章节上下文提示
        chapter_planning_hint = self._build_chapter_hint(work_id, chapter_id)
        tool_policy = self._resolve_tool_policy(context)

        # 组装完整 prompt
        plan_prompt = f"""AI写作助手。{history_section}{knowledge_section}{selected_text_section}
用户: {message}

【内部参数 - 用户不可见】
work_id: {work_id}
chapter_id: {chapter_id}
tool_policy: {tool_policy}

⚠️⚠️⚠️ 极其重要 - 任务描述规则 ⚠️⚠️⚠️
任务的 description 字段会直接显示给用户！绝对禁止在 description 中包含：
- work_id 的值（如 "550e8400-e29b-41d4-a716..."）
- chapter_id 的值（如 "e100be81-0b53-4ca2..."）
- 任何 UUID 格式的字符串

✅ 正确示例：
  - "读取当前章节内容"
  - "分析本章内容"
  - "获取作品上下文"

❌ 错误示例：
  - "读取 work_id: 550e8400... 的内容"
  - "读取 chapter_id: e100be81... 的章节"

工具调用的 params 中仍需使用完整 UUID，但 description 必须用中文描述！

{static_prompt}{chapter_planning_hint}"""

        return plan_prompt

    def _resolve_tool_policy(self, context: Optional[Dict[str, Any]]) -> str:
        if not context:
            return "auto"
        raw_policy = context.get("tool_policy") or ""
        policy = str(raw_policy).strip().lower()
        if policy in {"no_tool", "cache_only", "auto"}:
            return policy
        return "auto"

    async def _generate_direct_answer(
        self,
        message: str,
        conversation_history: str,
        context: Optional[Dict[str, Any]]
    ) -> str:
        from app.services.agent.model_selector import TaskType

        prompt = self._build_direct_answer_prompt(
            message=message,
            conversation_history=conversation_history,
            context=context
        )
        result = await self.agent._generate_text(
            prompt=prompt,
            temperature=0.3,
            max_tokens=2000,
            task_type=TaskType.CONTENT_CREATION
        )
        return result.get("text", "").strip()

    def _build_direct_answer_prompt(
        self,
        message: str,
        conversation_history: str,
        context: Optional[Dict[str, Any]]
    ) -> str:
        history_section = ""
        if conversation_history:
            history_section = f"""
【对话历史】
{conversation_history}

"""

        knowledge_section = self._build_knowledge_section(context)
        selected_text_section = self._build_selected_text_section(context)

        return f"""AI写作助手。{history_section}{knowledge_section}{selected_text_section}
用户: {message}

【要求】
1) 不调用任何工具，只能基于已提供的上下文回答。
2) 直接输出最终答案，不要输出计划或JSON。
3) 如果上下文不足，请明确说明信息不足。
"""

    def _build_knowledge_section(self, context: Optional[Dict[str, Any]]) -> str:
        """构建知识库文档部分"""
        if not context:
            return ""

        knowledge_docs = context.get("knowledge_docs", [])
        if not knowledge_docs:
            return ""

        logger.info(f"[Planning] 注入 {len(knowledge_docs)} 个知识库文档到prompt")
        knowledge_parts = []

        for doc in knowledge_docs[:3]:  # 最多3个文档
            title = doc.get("title") or "未命名文档"
            tags = doc.get("tags") or []
            source = doc.get("source_type") or "unknown"
            content = doc.get("content") or ""
            snippet = content.strip()[:800] if content else ""

            if snippet:
                tags_str = ', '.join(tags) if tags else '无'
                knowledge_parts.append(
                    f"=== 知识库文档 ===\n"
                    f"文档标题: {title}\n"
                    f"文档来源: {source}\n"
                    f"文档标签: {tags_str}\n"
                    f"文档正文内容:\n{snippet}\n"
                    f"=== 文档结束 ==="
                )

        if knowledge_parts:
            return "\n\n【用户引用的知识库文档】\n请参考以下文档内容回答用户问题：\n\n" + "\n\n".join(knowledge_parts) + "\n\n"

        return ""

    def _build_selected_text_section(self, context: Optional[Dict[str, Any]]) -> str:
        """构建选中文本部分"""
        if not context:
            return ""

        selected_text = context.get("selected_text") or ""
        instruction_context = context.get("instruction_context") or ""
        selection_position = context.get("selection_position")

        if selected_text:
            logger.info(f"[Planning] 注入选中文本到prompt: {selected_text[:50]}...")
            return f"""

【用户选中的文本】
以下是用户在编辑器中选中的文本，请针对这段文本执行用户的指令：
---
{selected_text}
---
选区位置: from={selection_position.get('from') if selection_position else 'N/A'}, to={selection_position.get('to') if selection_position else 'N/A'}

"""
        elif instruction_context:
            logger.info(f"[Planning] 注入指令上下文到prompt")
            return f"""

【用户指令上下文】
{instruction_context}

"""

        return ""

    def _build_chapter_hint(self, work_id: Optional[str], chapter_id: Optional[str]) -> str:
        """构建章节上下文提示

        🔧 2026-01-28: 移除硬编码的 UUID 值，避免 AI 复制错误的 ID
        """
        if not chapter_id:
            return ""

        return """

⚠️ 【章节上下文提示】：
- 当前用户在章节聊天面板中
- 用户要求修改/润色本章内容时，必须使用以下流程：
  1. 任务1: 调用 explore_content 或 read_chapter_tool 读取章节内容
  2. 任务2: 调用 analyze_content 分析原文中该句话的场景、情绪、角色状态（analysis_types="text"）
  3. 任务3: 基于分析结果，给出符合场景的修改建议
- ⚠️ 重要：chapter_id 和 work_id 应从 explore_content 或 read_chapter_tool 的返回结果中获取，不要硬编码
- ✅ 使用 $TASK_N.chapter_id$ 引用前置任务返回的章节ID
"""

    def _handle_planning_error(self, e: Exception) -> Optional[Dict[str, Any]]:
        """
        处理规划阶段的错误

        Args:
            e: 异常

        Returns:
            简化的规划数据，或 None（非网络错误时）
        """
        # 定义网络相关异常类型
        network_related_errors = (
            httpx.ConnectTimeout,
            httpx.ReadTimeout,
            httpx.NetworkError,
            httpx.HTTPError,
            ConnectionError,
            TimeoutError,
        )

        # 检查是否是网络相关错误
        is_network_error = (
            isinstance(e, network_related_errors) or
            any(keyword in str(e).lower() for keyword in
                ["网络", "连接", "超时", "timeout", "connection", "network"])
        )

        if is_network_error:
            logger.warning(f"[Planning] 检测到网络错误，使用简化规划流程")
            return {
                "user_intent": "执行用户请求",
                "tasks": [
                    {
                        "task_id": 1,
                        "description": "直接执行用户请求",
                        "tool": "get_context_tool",
                        "estimated_time": "5秒"
                    }
                ]
            }

        return None

    def _create_default_plan(self) -> Dict[str, Any]:
        """创建默认规划（当 AI 规划失败时的兜底方案）"""
        return {
            "user_intent": "执行用户请求",
            "tasks": [
                {
                    "task_id": 1,
                    "description": "理解用户意图并获取相关上下文",
                    "tool": "get_context_tool",
                    "estimated_time": "5秒"
                },
                {
                    "task_id": 2,
                    "description": "基于上下文响应用户请求",
                    "tool": "analyze_content",
                    "params": {
                        "content": {"$ref": {"task_id": 1, "path": ""}},
                        "analysis_types": "text",
                        "focus": "根据用户请求进行分析或回答"
                    },
                    "depends_on": [1],
                    "estimated_time": "10秒"
                }
            ]
        }

    def _post_process_plan(
        self,
        plan_data: Dict[str, Any],
        message: str,
        context: Optional[Dict[str, Any]] = None,
        work_id: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        规划后处理：补充验收标准与 checkpoint，并进行验证和自动修复

        Args:
            plan_data: 规划数据
            message: 用户消息

        Returns:
            处理后的规划数据
        """
        acceptance_hint = self._quick_acceptance_from_text(
            plan_data.get("user_intent") or message
        )

        tasks = plan_data.get("tasks") or []
        tasks = self._auto_reuse_explore_artifacts(tasks, message, context, work_id)
        for idx, t in enumerate(tasks):
            if acceptance_hint and not t.get("acceptance"):
                t["acceptance"] = acceptance_hint
            # 保证至少首个任务打 checkpoint，便于早期反思校验
            if "checkpoint" not in t:
                t["checkpoint"] = (idx == 0)

        plan_data["tasks"] = tasks

        # 🔧 2025-12-25: 新增规划验证和自动修复
        plan_data = self._validate_and_fix_plan(plan_data, message)
        plan_data["tasks"] = self._split_multi_edit_tasks(plan_data.get("tasks", []), message)
        plan_data["tasks"] = self._apply_locator_selection(plan_data.get("tasks", []), message)
        plan_data["tasks"] = self._ensure_explore_force_global_search(plan_data.get("tasks", []), message)
        plan_data["tasks"] = self._ensure_explore_strict_locator(plan_data.get("tasks", []))
        plan_data["tasks"] = self._ensure_chapter_id_from_locate(plan_data.get("tasks", []))
        plan_data["tasks"] = self._ensure_editor_apply_tasks(plan_data.get("tasks", []))
        plan_data["tasks"] = self._ensure_replace_original_text(plan_data.get("tasks", []))

        return self._normalize_plan_schema(plan_data)

    def _auto_reuse_explore_artifacts(
        self,
        tasks: List[Dict[str, Any]],
        message: str,
        context: Optional[Dict[str, Any]],
        work_id: Optional[str]
    ) -> List[Dict[str, Any]]:
        """自动复用 Explore Artifact，按条目补缺失项（轻量规则）"""
        if not tasks or not message or not isinstance(context, dict):
            return tasks
        if self._message_requires_fresh(message):
            return tasks

        session_artifacts = context.get("session_artifacts")
        if not isinstance(session_artifacts, list) or not session_artifacts:
            return tasks

        requested_items = self._extract_requested_items(message)
        if not requested_items:
            return tasks

        artifact = self._select_session_artifact(session_artifacts, work_id)
        if not artifact:
            return tasks

        summary_text = str(artifact.get("preview") or "").strip()
        if not summary_text:
            return tasks

        covered: List[str] = []
        missing: List[str] = []
        for item in requested_items:
            if self._is_item_covered(item, summary_text):
                covered.append(item)
            else:
                missing.append(item)

        if not covered:
            return tasks

        # 避免编辑链路误判：存在写回/改写任务时不自动裁剪
        if self._has_edit_tasks(tasks):
            return tasks

        tasks = self._ensure_load_explore_task(tasks, artifact, work_id)

        if not missing:
            # 全部覆盖：可尝试移除无依赖的 explore_content，避免重复探索
            tasks = self._drop_explore_tasks_if_safe(tasks)
            return tasks

        tasks = self._adjust_explore_tasks_for_missing(tasks, missing, covered)
        return tasks

    def _message_requires_fresh(self, message: str) -> bool:
        if not message:
            return False
        return any(keyword in message for keyword in self.FRESHNESS_KEYWORDS)

    @staticmethod
    def _normalize_text(text: str) -> str:
        if not text:
            return ""
        cleaned = re.sub(r"[\s，,。.;；:：/\\\-—_]", "", str(text))
        return cleaned.strip().lower()

    @classmethod
    def _is_item_covered(cls, item: str, summary: str) -> bool:
        item_norm = cls._normalize_text(item)
        summary_norm = cls._normalize_text(summary)
        if not item_norm or not summary_norm:
            return False
        if len(item_norm) >= 2 and item_norm in summary_norm:
            return True
        for part in re.split(r"[、,，;/\s]+", item):
            part_norm = cls._normalize_text(part)
            if len(part_norm) >= 2 and part_norm in summary_norm:
                return True
        return False

    @staticmethod
    def _extract_requested_items(message: str) -> List[str]:
        if not message:
            return []

        items: List[str] = []

        def _add_item(text: str) -> None:
            cleaned = (text or "").strip()
            if len(cleaned) < 2:
                return
            if len(cleaned) > 80:
                cleaned = cleaned[:80]
            items.append(cleaned)

        for line in message.splitlines():
            line = line.strip()
            if not line:
                continue
            match = re.match(r"^(?:[-•*]|\d+[.)、]|[一二三四五六七八九十]+[、.])\s*(.+)$", line)
            if match:
                _add_item(match.group(1))

            if "：" in line or ":" in line:
                parts = re.split(r"[：:]", line, maxsplit=1)
                if len(parts) == 2:
                    tail = parts[1]
                    if any(sep in tail for sep in ["、", ",", "，"]):
                        for seg in re.split(r"[、,，]", tail):
                            _add_item(seg)

        inline_items = re.findall(r"(?:^|\s)(?:\d+[.)、])\s*([^\d]{2,60})", message)
        for seg in inline_items:
            _add_item(seg)

        unique: List[str] = []
        seen = set()
        for item in items:
            key = PlanGenerator._normalize_text(item)
            if not key or key in seen:
                continue
            seen.add(key)
            unique.append(item)

        return unique[:10]

    @staticmethod
    def _select_session_artifact(artifacts: List[Dict[str, Any]], work_id: Optional[str]) -> Optional[Dict[str, Any]]:
        if not artifacts:
            return None
        if work_id:
            for item in artifacts:
                if str(item.get("work_id")) == str(work_id):
                    return item
        return artifacts[0]

    def _ensure_load_explore_task(
        self,
        tasks: List[Dict[str, Any]],
        artifact: Dict[str, Any],
        work_id: Optional[str]
    ) -> List[Dict[str, Any]]:
        artifact_id = str(artifact.get("artifact_id") or "").strip()
        if not artifact_id:
            return tasks
        for task in tasks:
            if task.get("tool") == "load_explore_artifact":
                params = task.get("params", {}) or {}
                if str(params.get("artifact_id") or "") == artifact_id:
                    return tasks

        new_task_id = self._next_task_id(tasks)
        new_task = {
            "task_id": new_task_id,
            "tool": "load_explore_artifact",
            "description": "读取最近探索摘要（复用已有信息）",
            "params": {
                "artifact_id": artifact_id,
                "mode": "summary"
            }
        }
        if work_id:
            new_task["params"]["work_id"] = work_id

        insert_idx = next((i for i, t in enumerate(tasks) if t.get("tool") == "explore_content"), len(tasks))
        new_tasks = list(tasks)
        new_tasks.insert(insert_idx, new_task)
        return new_tasks

    def _adjust_explore_tasks_for_missing(
        self,
        tasks: List[Dict[str, Any]],
        missing: List[str],
        covered: List[str]
    ) -> List[Dict[str, Any]]:
        if not missing:
            return tasks
        missing_text = "、".join(missing[:8])
        covered_text = "、".join(covered[:6])
        note = f"仅补充缺失项：{missing_text}"
        if covered_text:
            note += f"（已覆盖：{covered_text}）"

        for task in tasks:
            if task.get("tool") != "explore_content":
                continue
            params = task.get("params", {}) or {}
            target_task = str(params.get("target_task") or "").strip()
            if target_task:
                params["target_task"] = f"{target_task}\n{note}"
            else:
                params["target_task"] = note

            scope_tuple = self._extract_scope_tuple_from_params(params)
            existing_intent = params.get("retrieval_intent") if isinstance(params.get("retrieval_intent"), dict) else None
            retrieval_intent = self._build_retrieval_intent_payload(
                target_task=params["target_task"],
                keywords=missing[:8],
                scope=scope_tuple,
                existing=existing_intent,
            )
            params["retrieval_intent"] = retrieval_intent
            task["params"] = params
        return tasks

    def _drop_explore_tasks_if_safe(self, tasks: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        from app.services.agent.parameter_resolver import ParameterResolver

        explore_ids = {
            int(t.get("task_id"))
            for t in tasks
            if t.get("tool") == "explore_content" and isinstance(t.get("task_id"), int)
        }
        if not explore_ids:
            return tasks

        for task in tasks:
            if task.get("tool") == "explore_content":
                continue
            deps = ParameterResolver.extract_dependencies(task.get("params", {}))
            if explore_ids & deps:
                return tasks

        return [t for t in tasks if t.get("tool") != "explore_content"]

    def _has_edit_tasks(self, tasks: List[Dict[str, Any]]) -> bool:
        if not tasks:
            return False
        edit_tools = {
            "smart_rewrite",
            "smart_insert",
            "smart_continue",
            "operate_apply",
            "apply_chapter_edit"
        }
        return any(task.get("tool") in edit_tools for task in tasks)

    @staticmethod
    def _next_task_id(tasks: List[Dict[str, Any]]) -> int:
        max_task_id = 0
        for task in tasks:
            try:
                task_id = int(task.get("task_id", 0))
            except (TypeError, ValueError):
                task_id = 0
            max_task_id = max(max_task_id, task_id)
        return max_task_id + 1

    def _ensure_explore_strict_locator(self, tasks: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        if not tasks:
            return tasks
        if not self._plan_requires_strict_locator(tasks):
            return tasks
        for task in tasks:
            if task.get("tool") != "explore_content":
                continue
            params = task.get("params", {}) or {}
            if "require_paragraph_index" not in params or params.get("require_paragraph_index") is None:
                params["require_paragraph_index"] = True
            target_task = params.get("target_task")
            if isinstance(target_task, str) and "段落" not in target_task and "paragraph" not in target_task:
                params["target_task"] = f"{target_task}（需精确段落定位）"
            task["params"] = params
        return tasks

    @staticmethod
    def _message_explicitly_specifies_chapter(message: str) -> bool:
        if not message:
            return False
        text = message
        if re.search(r"(本章|当前章|当前章节|这一章|该章|此章)", text):
            return True
        if re.search(r"第\s*[一二两三四五六七八九十百千万\d]+\s*章", text):
            return True
        if re.search(r"前\s*[一二两三四五六七八九十\d]+\s*章", text):
            return True
        if re.search(r"章节\s*\d+\s*[到至\-~—～–]\s*\d+", text):
            return True
        if re.search(r"章节\s*\d+\s*章", text):
            return True
        return False

    def _should_force_global_search(self, message: str) -> bool:
        if not message:
            return False
        if self._message_explicitly_specifies_chapter(message):
            return False
        quoted = self._extract_quoted_segments(message)
        return bool(quoted)

    def _ensure_explore_force_global_search(self, tasks: List[Dict[str, Any]], message: str) -> List[Dict[str, Any]]:
        if not tasks:
            return tasks
        if not self._plan_requires_strict_locator(tasks):
            return tasks
        if not self._should_force_global_search(message):
            return tasks
        for task in tasks:
            if task.get("tool") != "explore_content":
                continue
            params = task.get("params", {}) or {}
            if params.get("force_global_search") is None:
                params["force_global_search"] = True
            target_task = params.get("target_task")
            if isinstance(target_task, str) and "全文" not in target_task and "全书" not in target_task:
                params["target_task"] = f"{target_task}（全文范围搜索）"
            task["params"] = params
        return tasks

    @staticmethod
    def _extract_quoted_segments_with_spans(message: str) -> List[Tuple[str, int, int]]:
        if not message:
            return []
        segments: List[Tuple[str, int, int]] = []
        seen = set()
        for match in re.finditer(r'["“”‘’「」『』](.+?)["“”‘’「」『』]', message):
            seg = (match.group(1) or "").strip()
            if not seg or len(seg) < 4:
                continue
            if seg in seen:
                continue
            segments.append((seg, match.start(), match.end()))
            seen.add(seg)
        return segments

    @classmethod
    def _extract_quoted_segments(cls, message: str) -> List[str]:
        return [seg for seg, _, _ in cls._extract_quoted_segments_with_spans(message)]

    @staticmethod
    def _normalize_quote_context(text: str) -> str:
        return re.sub(r"\s+", "", text or "")

    @classmethod
    def _classify_quote_role(cls, before_text: str, after_text: str) -> str:
        before = cls._normalize_quote_context(before_text)
        after = cls._normalize_quote_context(after_text)
        # 替换后的文本（改为/替换为/改成）通常出现在引号之前
        if re.search(r"(改为|改成|替换为|替换成|换成|变更为|改做)[:：]?$", before):
            return "replacement"
        # 原句通常出现在“将/把…改为/替换为”之前
        if re.match(r"^(改为|改成|替换为|替换成|换成|变更为|改做)", after):
            return "target"
        # 上下文/定位提示
        if re.match(r"^(上下文|语境|背景|附近|前后文|前文|后文|之前|之后|之间|处|位置|段落|句子)", after):
            return "context"
        if re.search(r"(上下文|语境|背景|附近|前后文|前文|后文|之前|之后|之间|处|位置|段落|句子)$", before):
            return "context"
        return "unknown"

    @classmethod
    def _classify_quoted_segments(cls, message: str) -> List[Tuple[str, str]]:
        classified: List[Tuple[str, str]] = []
        for seg, start, end in cls._extract_quoted_segments_with_spans(message):
            before = message[max(0, start - 20):start]
            after = message[end:min(len(message), end + 20)]
            role = cls._classify_quote_role(before, after)
            classified.append((seg, role))
        return classified

    @staticmethod
    def _message_forces_single_edit(message: str) -> bool:
        if not message:
            return False
        return bool(re.search(r"(只|仅|仅仅|仅需|只替换|仅替换|只改|仅改|只修改|仅修改|首次|第一处|第1处)", message))

    @staticmethod
    def _message_allows_multi_edit(message: str) -> bool:
        if not message:
            return False
        return bool(re.search(r"(分别|各自|逐一|每处|每一处|多处|全部|所有|都替换|全部替换|逐条|每段|每句|每个|两处|三处|四处|两段|三段|四段|两句|三句|四句)", message))

    @staticmethod
    def _chinese_numeral_to_int(value: str) -> Optional[int]:
        if not value:
            return None
        if value.isdigit():
            try:
                return int(value)
            except ValueError:
                return None
        mapping = {
            "零": 0,
            "一": 1,
            "二": 2,
            "两": 2,
            "三": 3,
            "四": 4,
            "五": 5,
            "六": 6,
            "七": 7,
            "八": 8,
            "九": 9,
            "十": 10,
        }
        if value == "十":
            return 10
        if "十" in value:
            parts = value.split("十")
            tens = mapping.get(parts[0], 1) if parts[0] else 1
            ones = mapping.get(parts[1], 0) if len(parts) > 1 and parts[1] else 0
            return tens * 10 + ones
        if value in mapping:
            return mapping[value]
        return None

    def _extract_locator_index(self, message: str) -> Optional[int]:
        if not message:
            return None
        m = re.search(r"第\s*([一二三四五六七八九十两0-9]{1,3})\s*(处|段|句|个|条)", message)
        if m:
            raw = m.group(1)
            number = self._chinese_numeral_to_int(raw)
            if number and number > 0:
                return number - 1
        if re.search(r"(前者|前一|前段|上一处|上一个|首处|首段|第一处|第一段|第一句)", message):
            return 0
        if re.search(r"(后者|后一|后段|下一处|下一个|末处|末段|最后一处|最后一段|最后)", message):
            return -1
        return None

    def _extract_locator_hint(self, message: str) -> Optional[str]:
        classified = self._classify_quoted_segments(message)
        if not classified:
            segments = []
        else:
            context_segments = [seg for seg, role in classified if role == "context"]
            if context_segments:
                return context_segments[0]
            segments = [seg for seg, role in classified if role != "replacement"]
        if len(segments) == 1:
            return segments[0]
        if len(segments) >= 2:
            between_match = re.search(r"(之间|之間|介于|介於|在.*和.*之间|在.*與.*之間)", message)
            if between_match:
                return segments[0]
        m = re.search(r"(?:包含|含有|带有|提到|提及|关于|出现|描写|说到)([^，。；;,.]{2,20})", message)
        if m:
            hint = (m.group(1) or "").strip()
            hint = re.sub(r"(的|那句|这一句|那段|这一段|那处|这一处|部分|内容)$", "", hint).strip()
            if 2 <= len(hint) <= 30 and re.search(r"[一-鿿A-Za-z0-9]", hint):
                return hint
        return None

    @staticmethod
    def _coerce_locate_target_index(value: Any) -> Optional[int]:
        if value is None:
            return None
        if isinstance(value, int):
            return value
        if isinstance(value, str):
            stripped = value.strip()
            if stripped.lstrip("-").isdigit():
                try:
                    return int(stripped)
                except ValueError:
                    return None
        return None

    @staticmethod
    def _locate_target_path_from_index(index: Optional[int], field: str) -> str:
        if index is None or index < 0:
            return f"locate_targets[0].{field}"
        return f"locate_targets[{index}].{field}"

    def _locate_target_path(self, params: Dict[str, Any], field: str) -> str:
        index = self._coerce_locate_target_index(params.get("locate_target_index"))
        return self._locate_target_path_from_index(index, field)

    def _replace_locate_target_refs(self, value: Any, index: Optional[int]) -> Any:
        if index is None or index < 0:
            return value
        if isinstance(value, dict):
            ref_obj = value.get("$ref") or value.get("ref")
            if isinstance(ref_obj, dict):
                path = ref_obj.get("path")
                if isinstance(path, str) and "locate_targets[0]" in path:
                    ref_obj["path"] = path.replace("locate_targets[0]", f"locate_targets[{index}]")
                return value
            return {k: self._replace_locate_target_refs(v, index) for k, v in value.items()}
        if isinstance(value, list):
            return [self._replace_locate_target_refs(item, index) for item in value]
        return value

    def _apply_locator_selection(self, tasks: List[Dict[str, Any]], message: str) -> List[Dict[str, Any]]:
        if not tasks or not message:
            return tasks
        target_index = self._extract_locator_index(message)
        target_hint = self._extract_locator_hint(message)
        if target_index is None and not target_hint:
            return tasks
        edit_tasks = [t for t in tasks if t.get("tool") in self.EDIT_CONTENT_TOOLS]
        if len(edit_tasks) != 1:
            return tasks

        for task in tasks:
            if not self._is_edit_task(task.get("tool"), task.get("params")):
                continue
            params = task.get("params", {}) or {}
            if target_index is not None:
                params.setdefault("locate_target_index", target_index)
                params = self._replace_locate_target_refs(params, target_index)
            if target_hint:
                params.setdefault("locate_target_hint", target_hint)
            task["params"] = params
        return tasks

    @staticmethod
    def _replace_task_id_refs(value: Any, old_id: int, new_id: int) -> Any:
        if isinstance(value, dict):
            if "$ref" in value or "ref" in value:
                ref_obj = value.get("$ref") or value.get("ref")
                if isinstance(ref_obj, dict):
                    ref_task_id = ref_obj.get("task_id")
                    if str(ref_task_id) == str(old_id):
                        ref_obj["task_id"] = new_id
                return value
            return {k: PlanGenerator._replace_task_id_refs(v, old_id, new_id) for k, v in value.items()}
        if isinstance(value, list):
            return [PlanGenerator._replace_task_id_refs(item, old_id, new_id) for item in value]
        if isinstance(value, str):
            return value.replace(f"$TASK_{old_id}", f"$TASK_{new_id}")
        return value

    def _split_multi_edit_tasks(self, tasks: List[Dict[str, Any]], message: str) -> List[Dict[str, Any]]:
        if not tasks or not message:
            return tasks
        if not self._plan_requires_strict_locator(tasks):
            return tasks

        if self._message_forces_single_edit(message):
            return tasks
        if not self._message_allows_multi_edit(message):
            return tasks

        classified = self._classify_quoted_segments(message)
        segments = [seg for seg, role in classified if role in {"target", "unknown"}]
        if len(segments) < 2:
            return tasks

        rewrite_indices = [idx for idx, t in enumerate(tasks) if t.get("tool") == "smart_rewrite"]
        if len(rewrite_indices) != 1:
            return tasks

        rewrite_idx = rewrite_indices[0]
        rewrite_task = tasks[rewrite_idx]
        rewrite_params = rewrite_task.get("params", {}) or {}
        text_to_rewrite = rewrite_params.get("text_to_rewrite")
        if text_to_rewrite and not isinstance(text_to_rewrite, dict):
            return tasks

        from app.services.agent.parameter_resolver import ParameterResolver

        rewrite_task_id = rewrite_task.get("task_id")
        if not rewrite_task_id:
            return tasks

        apply_indices = []
        for idx, task in enumerate(tasks):
            if task.get("tool") not in {"operate_apply", "apply_chapter_edit"}:
                continue
            deps = ParameterResolver.extract_dependencies(task.get("params", {}))
            if rewrite_task_id in deps:
                apply_indices.append(idx)
        if len(apply_indices) != 1:
            return tasks

        apply_idx = apply_indices[0]
        apply_task = tasks[apply_idx]

        max_task_id = 0
        for task in tasks:
            try:
                task_id = int(task.get("task_id", 0))
                max_task_id = max(max_task_id, task_id)
            except (TypeError, ValueError):
                continue
        next_task_id = max_task_id + 1

        new_tasks: List[Dict[str, Any]] = []
        for idx, task in enumerate(tasks):
            if idx == rewrite_idx:
                rewrite_params = dict(rewrite_task.get("params", {}) or {})
                rewrite_params["text_to_rewrite"] = segments[0]
                rewrite_task["params"] = rewrite_params
                new_tasks.append(rewrite_task)
                continue
            new_tasks.append(task)
            if idx != apply_idx:
                continue
            for seg_idx, segment in enumerate(segments[1:], start=2):
                new_rewrite = copy.deepcopy(rewrite_task)
                new_rewrite["task_id"] = next_task_id
                next_task_id += 1
                new_rewrite_params = dict(new_rewrite.get("params", {}) or {})
                new_rewrite_params["text_to_rewrite"] = segment
                new_rewrite["params"] = new_rewrite_params
                if new_rewrite.get("description"):
                    new_rewrite["description"] = f"{new_rewrite['description']}（第{seg_idx}处）"

                new_apply = copy.deepcopy(apply_task)
                new_apply["task_id"] = next_task_id
                next_task_id += 1
                new_apply["params"] = self._replace_task_id_refs(
                    new_apply.get("params", {}),
                    old_id=int(rewrite_task_id),
                    new_id=int(new_rewrite["task_id"])
                )
                depends_on = self._normalize_dep_list(new_apply.get("depends_on"))
                depends_on = [new_rewrite["task_id"] if d == rewrite_task_id else d for d in depends_on]
                new_apply["depends_on"] = depends_on
                if new_apply.get("description"):
                    new_apply["description"] = f"{new_apply['description']}（第{seg_idx}处）"

                new_tasks.extend([new_rewrite, new_apply])

        return new_tasks

    def _extract_enumerated_items(self, message: str) -> List[str]:
        if not message:
            return []

        items: List[str] = []
        seen = set()

        quoted_segments = re.findall(r'["“”‘’「」『』](.+?)["“”‘’「」『』]', message)
        for segment in quoted_segments:
            for part in self._split_enumerated_items(segment):
                normalized = self._normalize_enumerated_item(part)
                if normalized and normalized not in seen:
                    items.append(normalized)
                    seen.add(normalized)

        enum_pattern = re.compile(
            r'([一-鿿A-Za-z0-9]{1,20}(?:[、,/，;；|｜]+[一-鿿A-Za-z0-9]{1,20})+)'
        )
        for segment in enum_pattern.findall(message):
            for part in self._split_enumerated_items(segment):
                normalized = self._normalize_enumerated_item(part)
                if normalized and normalized not in seen:
                    items.append(normalized)
                    seen.add(normalized)

        return items

    @staticmethod
    def _split_enumerated_items(segment: str) -> List[str]:
        if not segment:
            return []
        return [part.strip() for part in re.split(r'[、,/，;；|｜]+', segment) if part.strip()]

    @staticmethod
    def _normalize_enumerated_item(raw: str) -> str:
        if not raw:
            return ""
        item = raw.strip()
        item = item.strip("\"“”'‘’「」『』[]()（）{}<>《》")
        item = re.sub(r'^[：:、,，;；|/]+|[：:、,，;；|/]+$', "", item)
        item = item.strip()

        if not item:
            return ""
        if len(item) > 30:
            return ""
        if any(ch in item for ch in ["=", "{", "}"]):
            return ""
        if not re.search(r'[一-鿿A-Za-z]', item):
            return ""
        if re.fullmatch(r'\d+', item):
            return ""
        if re.fullmatch(r'第\d+章', item) or re.fullmatch(r'第\d+段', item):
            return ""

        return item

    @classmethod
    def _is_edit_task(cls, tool: Optional[str], params: Optional[Dict[str, Any]] = None) -> bool:
        if not tool:
            return False
        if tool in cls.EDIT_CONTENT_TOOLS:
            return True
        if tool in cls.EDIT_OPERATION_TOOLS:
            operation = (params or {}).get("operation")
            return operation in cls.EDIT_OPERATIONS
        return False

    @classmethod
    def _plan_requires_strict_locator(cls, tasks: List[Dict[str, Any]]) -> bool:
        if not tasks:
            return False
        for task in tasks:
            if cls._is_edit_task(task.get("tool"), task.get("params", {})):
                return True
        return False

    @staticmethod
    def _should_enforce_enumerated_items(tasks: List[Dict[str, Any]]) -> bool:
        if not tasks:
            return False
        tools = {task.get("tool") for task in tasks if task.get("tool")}
        if not tools:
            return False
        return not tools.issubset({"get_writing_context"})

    def _find_missing_enumerated_items(
        self,
        tasks: List[Dict[str, Any]],
        enumerated_items: List[str]
    ) -> List[str]:
        if not tasks or not enumerated_items:
            return []

        task_texts: List[str] = []
        for task in tasks:
            parts = []
            title = task.get("title")
            if title:
                parts.append(str(title))
            description = task.get("description")
            if description:
                parts.append(str(description))
            tool = task.get("tool")
            if tool:
                parts.append(str(tool))
            params = task.get("params", {})
            if params:
                try:
                    parts.append(json.dumps(params, ensure_ascii=False))
                except Exception:
                    parts.append(str(params))
            if parts:
                task_texts.append(" ".join(parts))

        lowered_texts = [text.lower() for text in task_texts]
        missing = []
        for item in enumerated_items:
            needle = item.lower()
            if not any(needle in text for text in lowered_texts):
                missing.append(item)

        return missing

    @staticmethod
    def _build_enumerated_items_prompt(missing_items: List[str]) -> str:
        items_text = "、".join(missing_items)
        return f"""

⚠️ 补充硬约束：用户列出的枚举项必须逐项覆盖，不可合并或省略。
当前未覆盖的枚举项：{items_text}
请重新生成完整 tasks，确保每一项至少在一个任务 description 或 params 中显式出现，并安排对应操作（搜索/定位/分析/改写等）。
"""

    def _normalize_plan_schema(self, plan_data: Dict[str, Any]) -> Dict[str, Any]:
        """校验并归一化规划输出结构，补齐 depends_on。"""
        from app.services.agent.parameter_resolver import ParameterResolver
        from app.services.agent.planning.plan_schema import PlanSchema

        try:
            plan = PlanSchema.model_validate(plan_data)
        except ValidationError as exc:
            logger.warning(f"[Planning] 规划结构校验失败，尝试转换占位符: {exc}")
            tasks = plan_data.get("tasks", []) or []
            for task in tasks:
                task_id = task.get("task_id")
                params = task.get("params", {})
                converted_params, has_legacy, has_unconverted = self._convert_placeholders_to_ref(params)
                if has_legacy:
                    task["params"] = converted_params
                if has_unconverted:
                    logger.warning(
                        f"[Planning] 发现嵌入式旧占位符，保留原字符串等待解析: task_id={task_id}"
                    )
                depends_on = self._normalize_dep_list(task.get("depends_on"))
                inferred = ParameterResolver.extract_dependencies(task.get("params", {}))
                if task_id:
                    try:
                        inferred.discard(int(task_id))
                    except (TypeError, ValueError):
                        pass
                if inferred:
                    depends_on = sorted(set(depends_on).union(inferred))
                task["depends_on"] = depends_on
            plan_data["tasks"] = tasks
            return plan_data

        normalized = plan.model_dump()
        tasks = normalized.get("tasks", []) or []

        for task in tasks:
            task_id = task.get("task_id")
            params = task.get("params", {})
            converted_params, has_legacy, has_unconverted = self._convert_placeholders_to_ref(params)
            if has_legacy:
                task["params"] = converted_params
                logger.warning(
                    f"[Planning] 检测到旧占位符，已转换为 $ref: task_id={task_id}"
                )
            if has_unconverted:
                logger.warning(
                    f"[Planning] 发现嵌入式旧占位符，保留原字符串等待解析: task_id={task_id}"
                )
            depends_on = self._normalize_dep_list(task.get("depends_on"))
            inferred = ParameterResolver.extract_dependencies(task.get("params", {}))
            if task_id:
                try:
                    inferred.discard(int(task_id))
                except (TypeError, ValueError):
                    pass
            if inferred:
                depends_on = sorted(set(depends_on).union(inferred))
            task["depends_on"] = depends_on

        normalized["tasks"] = tasks
        return normalized

    def _convert_placeholders_to_ref(self, value: Any) -> Tuple[Any, bool, bool]:
        """将纯占位符字符串转换为 $ref，并标记残留占位符。"""
        from app.services.agent.parameter_resolver import ParameterResolver

        has_legacy = False
        has_unconverted = False

        if isinstance(value, str):
            match = ParameterResolver.PLACEHOLDER_PATTERN.fullmatch(value)
            if not match:
                match = ParameterResolver.LOOSE_PLACEHOLDER_PATTERN.fullmatch(value)
            if match:
                has_legacy = True
                task_id = match.group(1)
                path = match.group(2) or ""
                try:
                    task_id = int(task_id)
                except (TypeError, ValueError):
                    return value, True, True
                return {"$ref": {"task_id": task_id, "path": path}}, True, False

            if (ParameterResolver.PLACEHOLDER_PATTERN.search(value)
                    or ParameterResolver.LOOSE_PLACEHOLDER_PATTERN.search(value)):
                has_legacy = True
                has_unconverted = True

            return value, has_legacy, has_unconverted

        if isinstance(value, dict):
            if "$ref" in value or "ref" in value:
                return value, False, False
            converted: Dict[str, Any] = {}
            for key, item in value.items():
                new_value, found, unconverted = self._convert_placeholders_to_ref(item)
                converted[key] = new_value
                has_legacy = has_legacy or found
                has_unconverted = has_unconverted or unconverted
            return converted, has_legacy, has_unconverted

        if isinstance(value, list):
            converted_list: List[Any] = []
            for item in value:
                new_value, found, unconverted = self._convert_placeholders_to_ref(item)
                converted_list.append(new_value)
                has_legacy = has_legacy or found
                has_unconverted = has_unconverted or unconverted
            return converted_list, has_legacy, has_unconverted

        return value, False, False

    @staticmethod
    def _normalize_dep_list(value: Any) -> List[int]:
        """把 depends_on 归一化为 int 列表。"""
        if value is None:
            return []
        if isinstance(value, (int, str)):
            try:
                return [int(value)]
            except (TypeError, ValueError):
                return []
        if isinstance(value, list):
            normalized = []
            for item in value:
                try:
                    normalized.append(int(item))
                except (TypeError, ValueError):
                    continue
            return normalized
        return []

    @staticmethod
    def _extract_internal_keywords(params: Dict[str, Any]) -> List[str]:
        intent = params.get("retrieval_intent") if isinstance(params, dict) else None
        if isinstance(intent, dict):
            intent_values: List[str] = []
            for key in ("entities", "actions", "timeline", "risks"):
                raw_value = intent.get(key)
                if isinstance(raw_value, list):
                    intent_values.extend(str(item) for item in raw_value if str(item).strip())
            if intent_values:
                chunks = intent_values
            else:
                chunks = []
        else:
            chunks = []

        raw = params.get("keywords")
        if raw is None:
            raw = params.get("keyword")
        if raw is None:
            raw = params.get("query")

        if isinstance(raw, list):
            chunks.extend(str(item) for item in raw if str(item).strip())
        elif isinstance(raw, str):
            chunks.append(raw)
        elif raw is not None:
            chunks.append(str(raw))

        keywords: List[str] = []
        seen = set()
        for chunk in chunks:
            for part in re.split(r"[,\s，、;；|｜/]+", chunk):
                kw = str(part).strip().strip("\"'“”‘’《》")
                if not kw or kw in seen:
                    continue
                seen.add(kw)
                keywords.append(kw)
                if len(keywords) >= 8:
                    return keywords
        return keywords

    @staticmethod
    def _extract_scope_tuple_from_params(params: Dict[str, Any]) -> Optional[Tuple[int, int]]:
        if not isinstance(params, dict):
            return None

        def _coerce(value: Any) -> Optional[int]:
            if isinstance(value, int):
                return value
            if isinstance(value, str):
                text = value.strip()
                if text.isdigit():
                    return int(text)
            return None

        raw_range = params.get("chapter_range")
        if isinstance(raw_range, (list, tuple)) and len(raw_range) >= 2:
            start = _coerce(raw_range[0])
            end = _coerce(raw_range[1])
            if isinstance(start, int) and isinstance(end, int):
                return (min(start, end), max(start, end))

        raw_ranges = params.get("chapter_ranges")
        if isinstance(raw_ranges, list) and raw_ranges:
            starts: List[int] = []
            ends: List[int] = []
            for item in raw_ranges:
                if isinstance(item, (list, tuple)) and len(item) >= 2:
                    start = _coerce(item[0])
                    end = _coerce(item[1])
                    if isinstance(start, int) and isinstance(end, int):
                        starts.append(min(start, end))
                        ends.append(max(start, end))
            if starts and ends:
                return (min(starts), max(ends))

        raw_orders = params.get("chapter_orders") or params.get("chapter_order")
        numbers: List[int] = []
        if isinstance(raw_orders, (list, tuple, set)):
            for item in raw_orders:
                num = _coerce(item)
                if isinstance(num, int):
                    numbers.append(num)
        elif isinstance(raw_orders, str):
            numbers.extend(int(n) for n in re.findall(r"\d+", raw_orders))
        else:
            num = _coerce(raw_orders)
            if isinstance(num, int):
                numbers.append(num)
        if numbers:
            return (min(numbers), max(numbers))
        return None

    def _build_retrieval_intent_payload(
        self,
        *,
        target_task: str,
        keywords: List[str],
        scope: Optional[Tuple[int, int]],
        existing: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, Any]:
        payload: Dict[str, Any] = {
            "goal": target_task or "",
            "entities": list(dict.fromkeys((keywords or [])[:8])),
        }

        if isinstance(existing, dict) and existing:
            for key, value in existing.items():
                if value is None:
                    continue
                if isinstance(value, list) and value:
                    payload[key] = value
                elif isinstance(value, dict) and value:
                    merged = dict(payload.get(key) or {})
                    merged.update(value)
                    payload[key] = merged
                elif value not in ("", []):
                    payload[key] = value

        if scope:
            constraints = dict(payload.get("constraints") or {})
            constraints["chapter_scope"] = [scope[0], scope[1]]
            payload["constraints"] = constraints
        return payload

    def _rewrite_internal_explore_tasks(self, tasks: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        if not tasks:
            return tasks

        for task in tasks:
            tool_raw = str(task.get("tool") or "").strip()
            normalized_tool = self.LEGACY_EXPLORE_TOOL_ALIASES.get(tool_raw, tool_raw)
            is_native_explore = normalized_tool == "explore_content"
            if normalized_tool not in self.INTERNAL_EXPLORE_TOOLS and not is_native_explore:
                continue

            params = task.get("params") or {}
            keywords = self._extract_internal_keywords(params)

            target_lines: List[str] = []
            desc = str(task.get("description") or "").strip()
            title = str(task.get("title") or "").strip()
            explicit_target_task = str(params.get("target_task") or "").strip()
            if explicit_target_task:
                target_lines.append(explicit_target_task)
            elif desc:
                target_lines.append(desc)
            elif title:
                target_lines.append(title)

            if normalized_tool in {"read_paragraph", "read_paragraphs", "list_paragraphs"}:
                target_lines.append("按段落读取并提取可定位原文证据。")
            else:
                target_lines.append("收集完成任务所需的原文证据。")

            chapter_scope = (
                params.get("chapter_range")
                or params.get("chapter_ranges")
                or params.get("chapter_orders")
                or params.get("chapter_order")
            )
            if chapter_scope:
                target_lines.append(f"章节范围：{chapter_scope}")
            if keywords:
                target_lines.append(f"关键词：{'、'.join(keywords[:8])}")

            target_task = "\n".join(line for line in target_lines if line).strip()
            if not target_task:
                target_task = "收集完成任务所需的原文证据。"

            scope_tuple = self._extract_scope_tuple_from_params(params)
            retrieval_intent = self._build_retrieval_intent_payload(
                target_task=target_task,
                keywords=keywords,
                scope=scope_tuple,
                existing=params.get("retrieval_intent") if isinstance(params.get("retrieval_intent"), dict) else None,
            )

            rewritten_params: Dict[str, Any] = {
                "target_task": target_task,
                "retrieval_intent": retrieval_intent,
            }
            if normalized_tool in {"read_paragraph", "read_paragraphs"}:
                rewritten_params["require_paragraph_index"] = True

            for key in (
                "max_rounds",
                "max_tool_calls",
                "max_read_paragraphs",
                "output_mode",
                "force_global_search",
                "use_cache",
                "force_refresh",
            ):
                if key in params:
                    rewritten_params[key] = params.get(key)

            task["tool"] = "explore_content"
            task["params"] = rewritten_params
            if not is_native_explore:
                logger.warning(
                    "[Planning] 内部检索工具已纠偏为 explore_content: %s -> explore_content (task_id=%s)",
                    tool_raw,
                    task.get("task_id"),
                )

        return tasks

    def _validate_and_fix_plan(self, plan_data: Dict[str, Any], message: str) -> Dict[str, Any]:
        """
        验证规划并自动修复问题

        检查项：
        1. 人物查询是否先搜索
        2. 多章节请求的任务完整性
        3. explore_content 任务约束补齐

        Args:
            plan_data: 规划数据
            message: 用户消息

        Returns:
            修复后的规划数据
        """
        tasks = plan_data.get("tasks", [])
        if not tasks:
            return plan_data

        # 验证0: 统一检索契约（内部工具全部收敛到 explore_content）
        tasks = self._rewrite_internal_explore_tasks(tasks)

        # 验证1: 人物查询必须先搜索
        tasks = self._validate_search_before_read(tasks, message)

        # 验证2: 检查多章节批量读取格式（现在工具支持范围格式）
        tasks = self._optimize_multi_chapter_tasks(tasks, message)

        # 验证3: 约束补齐（范围/段落/禁止整章/禁止越界）
        constraints = self._extract_task_constraints(message)
        if constraints:
            tasks = self._apply_constraints_to_tasks(tasks, constraints)

        # 验证4: 旧链路兼容（自动补齐 explore_content output_mode）
        tasks = self._auto_set_explore_output_mode(tasks)

        plan_data["tasks"] = tasks
        return plan_data

    @staticmethod
    def _extract_task_constraints(message: str) -> Dict[str, str]:
        if not message:
            return {}
        constraints: Dict[str, str] = {}
        scope_text = PlanGenerator._extract_scope_text(message)
        if scope_text:
            constraints["scope_text"] = scope_text
        if any(keyword in message for keyword in ["段落号", "只允许精确段落", "只读段落", "仅段落"]):
            constraints["require_paragraph"] = "true"
        if any(keyword in message for keyword in ["不要整章", "不读整章", "禁止整章", "不要全文", "不读全文", "不要全章", "不读全章"]):
            constraints["forbid_full_chapter"] = "true"
        if any(keyword in message for keyword in ["不得引用范围外内容", "禁止引用范围外内容"]):
            constraints["forbid_out_of_scope"] = "true"
        return constraints

    @staticmethod
    def _extract_scope_text(message: str) -> str:
        if not message:
            return ""
        matches: List[str] = []
        patterns = [
            r"第\s*\d+\s*(?:章)?\s*[到至\-~—～–]\s*第?\s*\d+\s*章",
            r"第\s*[一二两三四五六七八九十]+\s*章?\s*[到至\-~—～–]\s*第?\s*[一二两三四五六七八九十]+\s*章",
            r"章节\s*\(?\s*\d+\s*[到至\-~—～–]\s*\d+\s*\)?",
            r"\d+\s*[到至\-~—～–]\s*\d+\s*章",
            r"第\s*\d+\s*章",
            r"第\s*[一二两三四五六七八九十]+\s*章",
            r"章节\s*\d+\s*章",
        ]
        for pattern in patterns:
            matches.extend(re.findall(pattern, message))
        if not matches:
            return ""
        deduped = []
        seen = set()
        for item in matches:
            if item not in seen:
                deduped.append(item)
                seen.add(item)
        return "、".join(deduped)

    @staticmethod
    def _apply_constraints_to_tasks(
        tasks: List[Dict[str, Any]],
        constraints: Dict[str, str]
    ) -> List[Dict[str, Any]]:
        if not tasks or not constraints:
            return tasks

        constraint_parts: List[str] = []
        scope_text = constraints.get("scope_text")
        if scope_text:
            constraint_parts.append(f"章节范围：{scope_text}")
        if constraints.get("forbid_full_chapter"):
            constraint_parts.append("不要整章阅读")
        if constraints.get("require_paragraph"):
            constraint_parts.append("只允许精确段落读取")
        if constraints.get("forbid_out_of_scope"):
            constraint_parts.append("不得引用范围外内容")
        if not constraint_parts:
            return tasks

        constraint_text = "；".join(constraint_parts)
        for task in tasks:
            if task.get("tool") != "explore_content":
                continue
            params = task.get("params") or {}
            target_task = params.get("target_task") or task.get("description") or ""
            if constraint_text and constraint_text not in target_task:
                if target_task:
                    target_task = f"{target_task}\n约束：{constraint_text}"
                else:
                    target_task = f"约束：{constraint_text}"
            params["target_task"] = target_task
            task["params"] = params

        return tasks

    @staticmethod
    def _auto_set_explore_output_mode(tasks: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """旧链路兼容：当下游参数引用旧字段时，自动为 explore_content 补 output_mode=full。"""
        if not tasks:
            return tasks

        task_by_id: Dict[int, Dict[str, Any]] = {}
        for task in tasks:
            try:
                task_id = int(task.get("task_id", 0))
            except (TypeError, ValueError):
                continue
            task_by_id[task_id] = task

        legacy_ref_task_ids: set[int] = set()
        for task in tasks:
            params = task.get("params") or {}
            legacy_ref_task_ids.update(PlanGenerator._find_legacy_ref_task_ids(params))

        if not legacy_ref_task_ids:
            return tasks

        for task_id in legacy_ref_task_ids:
            target_task = task_by_id.get(task_id)
            if not target_task or target_task.get("tool") != "explore_content":
                continue
            params = target_task.get("params") or {}
            if params.get("output_mode"):
                continue
            params["output_mode"] = "full"
            target_task["params"] = params

        return tasks

    @staticmethod
    def _find_legacy_ref_task_ids(value: Any) -> set[int]:
        """在参数中查找旧字段引用并返回 task_id 集合。"""
        legacy_keywords = (
            "chapters",
            "context_for_task",
            "explore_summary",
            "frontend_display",
            "front_end",
        )

        def _contains_legacy(text: str) -> bool:
            return any(keyword in text for keyword in legacy_keywords)

        task_ids: set[int] = set()

        if isinstance(value, dict):
            ref_obj = value.get("$ref") or value.get("ref")
            if isinstance(ref_obj, dict):
                ref_path = ref_obj.get("path") or ""
                ref_task_id = ref_obj.get("task_id")
                if isinstance(ref_path, str) and _contains_legacy(ref_path):
                    try:
                        task_ids.add(int(ref_task_id))
                    except (TypeError, ValueError):
                        pass
            for nested_value in value.values():
                task_ids.update(PlanGenerator._find_legacy_ref_task_ids(nested_value))
            return task_ids

        if isinstance(value, list):
            for item in value:
                task_ids.update(PlanGenerator._find_legacy_ref_task_ids(item))
            return task_ids

        if isinstance(value, str):
            if "$TASK_" in value and _contains_legacy(value):
                for match in re.finditer(r"\$TASK_(\d+)", value):
                    try:
                        task_ids.add(int(match.group(1)))
                    except (TypeError, ValueError):
                        continue
            return task_ids

        return task_ids

    def _validate_search_before_read(self, tasks: List[Dict], message: str) -> List[Dict]:
        """
        验证人物/地点查询必须先搜索

        🔧 2026-01-10: 暂时禁用此功能
        原因：正则表达式误判严重，把"增加环境描写"识别为人物名
        后续可考虑用 jieba 词性标注来智能判断

        Args:
            tasks: 任务列表
            message: 用户消息

        Returns:
            原始任务列表（不再自动插入搜索任务）
        """
        # 🔧 暂时禁用，直接返回原任务列表
        return tasks

    def _optimize_multi_chapter_tasks(self, tasks: List[Dict], message: str) -> List[Dict]:
        """
        优化多章节读取任务

        检测连续的多个 get_chapter_by_order_tool 任务，合并成一个批量读取任务

        Args:
            tasks: 任务列表
            message: 用户消息

        Returns:
            优化后的任务列表
        """
        # 找到连续的 get_chapter_by_order_tool 任务
        chapter_tasks = []
        other_tasks = []
        chapter_indices = []

        for i, task in enumerate(tasks):
            if task.get("tool") == "get_chapter_by_order_tool":
                params = task.get("params", {})
                chapter_order = params.get("chapter_order")
                if chapter_order is not None:
                    # 检查是否已经是批量格式
                    if isinstance(chapter_order, str) and ("-" in str(chapter_order) or "," in str(chapter_order)):
                        other_tasks.append(task)
                    else:
                        try:
                            order = int(chapter_order)
                            chapter_tasks.append((i, order, task))
                            chapter_indices.append(i)
                        except (ValueError, TypeError):
                            other_tasks.append(task)
                else:
                    other_tasks.append(task)
            else:
                other_tasks.append(task)

        # 如果只有0-1个章节任务，不需要优化
        if len(chapter_tasks) <= 1:
            return tasks

        # 检查是否是连续的章节序号
        orders = sorted([t[1] for t in chapter_tasks])
        is_continuous = all(orders[i+1] - orders[i] == 1 for i in range(len(orders) - 1))

        if not is_continuous or len(orders) < 2:
            return tasks

        # 合并成一个批量读取任务
        start_order = orders[0]
        end_order = orders[-1]

        logger.info(f"[PlanOptimizer] 合并 {len(orders)} 个章节读取任务为批量读取: {start_order}-{end_order}")

        merged_task = {
            "task_id": 1,
            "description": f"批量读取第{start_order}-{end_order}章",
            "tool": "get_chapter_by_order_tool",
            "params": {"chapter_order": f"{start_order}-{end_order}"},
            "checkpoint": False
        }

        # 重建任务列表
        new_tasks = [merged_task]
        task_id = 2
        for task in other_tasks:
            task["task_id"] = task_id
            # 更新参数中的任务引用（$TASK_N$ 格式）
            self._update_task_references(task, chapter_indices, len(orders))
            new_tasks.append(task)
            task_id += 1

        return new_tasks

    def _update_task_references(self, task: Dict, old_indices: List[int], merged_count: int):
        """
        更新任务参数中的任务引用

        当多个任务被合并后，需要更新后续任务中的 $TASK_N$ 引用

        Args:
            task: 任务
            old_indices: 被合并的任务索引列表
            merged_count: 被合并的任务数量

        🔧 2025-12-25: 同时处理 $TASK_N$ 和 $TASK_N.content$ 两种格式
        """
        params = task.get("params", {})
        if not params:
            return

        params_str = json.dumps(params, ensure_ascii=False)

        # 替换 $TASK_N.content$ 和 $TASK_N$ 为 $TASK_1.chapters$（后续统一转为 $ref）
        # 例如：$TASK_1.content$\n$TASK_2.content$... → $TASK_1.chapters$
        for old_idx in sorted(old_indices, reverse=True):
            # 处理 $TASK_N.content$ 格式
            old_ref_content = f"$TASK_{old_idx + 1}.content$"
            # 处理 $TASK_N$ 格式（完整输出）
            old_ref_full = f"$TASK_{old_idx + 1}$"

            # 只需要替换第一个，其余的会被删除
            if old_idx == old_indices[0]:
                params_str = params_str.replace(old_ref_content, "$TASK_1.chapters$")
                params_str = params_str.replace(old_ref_full, "$TASK_1.chapters$")
            else:
                # 删除后续的引用（连接符也删除）
                for old_ref in [old_ref_content, old_ref_full]:
                    params_str = params_str.replace(f"\\n\\n{old_ref}", "")
                    params_str = params_str.replace(f"\\n{old_ref}", "")
                    params_str = params_str.replace(old_ref, "")

        try:
            task["params"] = json.loads(params_str)
        except json.JSONDecodeError:
            pass  # 保持原样

    def _ensure_editor_apply_tasks(self, tasks: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Ensure smart_* editor tasks are followed by operate_apply (default version A)."""
        if not tasks:
            return tasks

        max_task_id = 0
        for task in tasks:
            try:
                task_id = int(task.get("task_id", 0))
                max_task_id = max(max_task_id, task_id)
            except (TypeError, ValueError):
                continue

        next_task_id = max_task_id + 1
        last_locate_task_id: Optional[int] = None
        last_explore_task_id: Optional[int] = None
        idx = 0

        while idx < len(tasks):
            task = tasks[idx]
            tool = task.get("tool")
            task_id = task.get("task_id")
            params = task.get("params", {}) or {}

            if tool == "locate_content":
                last_locate_task_id = task_id
            elif tool == "explore_content":
                last_explore_task_id = task_id

            if tool in {"smart_rewrite", "smart_continue", "smart_insert", "rewrite_chapter_content"} and task_id:
                if not params.get("chapter_id"):
                    idx += 1
                    continue
                if self._has_apply_task(tasks, task_id):
                    idx += 1
                    continue

                apply_task = self._build_apply_task(
                    source_tool=tool,
                    source_task_id=task_id,
                    locate_task_id=last_locate_task_id,
                    explore_task_id=last_explore_task_id,
                    new_task_id=next_task_id,
                    source_params=params
                )
                if apply_task:
                    tasks.insert(idx + 1, apply_task)
                    next_task_id += 1
                    idx += 2
                    continue

            idx += 1

        return tasks

    def _ensure_replace_original_text(self, tasks: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """补齐 replace 操作的 original_text（优先取 smart_rewrite 输出）"""
        if not tasks:
            return tasks

        from app.services.agent.parameter_resolver import ParameterResolver

        task_by_id: Dict[int, Dict[str, Any]] = {}
        for task in tasks:
            try:
                task_id = int(task.get("task_id", 0))
            except (TypeError, ValueError):
                continue
            task_by_id[task_id] = task

        for task in tasks:
            if task.get("tool") not in {"operate_apply", "apply_chapter_edit"}:
                continue
            params = task.get("params", {}) or {}
            if params.get("operation") != "replace":
                continue
            if params.get("original_text"):
                continue

            deps = ParameterResolver.extract_dependencies(params)
            source_task_id = None
            for dep_id in deps:
                dep_task = task_by_id.get(dep_id)
                if dep_task and dep_task.get("tool") == "smart_rewrite":
                    source_task_id = dep_id
                    break

            if source_task_id:
                params["original_text"] = {
                    "$ref": {
                        "task_id": source_task_id,
                        "path": "data.original_text"
                    }
                }
                # 方案1：强制修正 smart_rewrite 的写回 content 路径
                content_ref = params.get("content")
                if isinstance(content_ref, dict):
                    ref_obj = content_ref.get("$ref") or content_ref.get("ref") or {}
                    if ref_obj.get("task_id") == source_task_id:
                        ref_path = ref_obj.get("path") or ""
                        if ref_path in {"content", "versions[0].content", "data.content"}:
                            params["content"] = {
                                "$ref": {
                                    "task_id": source_task_id,
                                    "path": "data.versions[0].content"
                                }
                            }
                task["params"] = params

        return tasks

    @staticmethod
    def _should_override_chapter_id(chapter_id: Any, locate_task_id: Optional[int]) -> bool:
        if not locate_task_id:
            return False
        if not chapter_id:
            return True
        if isinstance(chapter_id, dict):
            ref_obj = chapter_id.get("$ref") or chapter_id.get("ref") or {}
            if not ref_obj:
                return False
            ref_task_id = ref_obj.get("task_id")
            ref_path = ref_obj.get("path") or ""
            if str(ref_task_id) == str(locate_task_id) and ref_path == "chapter_id":
                return False
            return True
        if isinstance(chapter_id, str):
            if "$TASK_" in chapter_id or "chapters[" in chapter_id or "chapters" in chapter_id:
                return True
        return False

    def _ensure_chapter_id_from_locate(self, tasks: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """优先使用 locate_content 的 chapter_id，避免 chapters[1] 越界导致 None。"""
        if not tasks:
            return tasks

        from app.services.agent.parameter_resolver import ParameterResolver

        task_by_id: Dict[int, Dict[str, Any]] = {}
        for task in tasks:
            try:
                task_id = int(task.get("task_id", 0))
            except (TypeError, ValueError):
                continue
            task_by_id[task_id] = task

        last_locate_task_id: Optional[int] = None
        last_explore_task_id: Optional[int] = None
        for task in tasks:
            tool = task.get("tool")
            task_id = task.get("task_id")
            params = task.get("params", {}) or {}

            if tool == "locate_content":
                try:
                    last_locate_task_id = int(task_id)
                except (TypeError, ValueError):
                    last_locate_task_id = task_id
                continue
            if tool == "explore_content":
                try:
                    last_explore_task_id = int(task_id)
                except (TypeError, ValueError):
                    last_explore_task_id = task_id
                continue

            if tool in {"smart_rewrite", "smart_insert", "smart_continue", "operate_apply", "apply_chapter_edit"}:
                allow_locator_override = True
                if tool in {"operate_apply", "apply_chapter_edit"}:
                    operation = str(params.get("operation") or "").strip().lower()
                    if operation not in {"replace", "insert"}:
                        allow_locator_override = False
                if allow_locator_override:
                    force_override = tool in {"smart_rewrite", "smart_insert", "operate_apply", "apply_chapter_edit"} and (
                        last_locate_task_id or last_explore_task_id
                    )
                    if last_locate_task_id and (force_override or self._should_override_chapter_id(params.get("chapter_id"), last_locate_task_id)):
                        params["chapter_id"] = {
                            "$ref": {
                                "task_id": last_locate_task_id,
                                "path": "chapter_id"
                            }
                        }
                    elif last_explore_task_id and (force_override or self._should_override_chapter_id(params.get("chapter_id"), last_explore_task_id)):
                        params["chapter_id"] = {
                            "$ref": {
                                "task_id": last_explore_task_id,
                                "path": self._locate_target_path(params, "chapter_id"),
                                "default": params.get("chapter_id")
                            }
                        }
                if tool in {"smart_rewrite", "smart_insert"}:
                    if last_locate_task_id:
                        if tool == "smart_rewrite" and not params.get("text_to_rewrite"):
                            params["text_to_rewrite"] = {
                                "$ref": {"task_id": last_locate_task_id, "path": "text"}
                            }
                        if tool == "smart_insert" and not params.get("insert_context"):
                            params["insert_context"] = {
                                "$ref": {"task_id": last_locate_task_id, "path": "text"}
                            }
                        params.setdefault(
                            "source_locator",
                            {
                                "chapter_id": {"$ref": {"task_id": last_locate_task_id, "path": "chapter_id"}},
                                "paragraph_index": {"$ref": {"task_id": last_locate_task_id, "path": "paragraph_index"}},
                                "node_id": {"$ref": {"task_id": last_locate_task_id, "path": "node_id"}},
                                "text": {"$ref": {"task_id": last_locate_task_id, "path": "text"}}
                            }
                        )
                    elif last_explore_task_id:
                        if tool == "smart_rewrite" and not params.get("text_to_rewrite"):
                            params["text_to_rewrite"] = {
                                "$ref": {"task_id": last_explore_task_id, "path": self._locate_target_path(params, "text")}
                            }
                        if tool == "smart_insert" and not params.get("insert_context"):
                            params["insert_context"] = {
                                "$ref": {"task_id": last_explore_task_id, "path": self._locate_target_path(params, "insert_context")}
                            }
                        params.setdefault(
                            "source_locator",
                            {
                                "chapter_id": {"$ref": {"task_id": last_explore_task_id, "path": self._locate_target_path(params, "chapter_id")}},
                                "paragraph_index": {"$ref": {"task_id": last_explore_task_id, "path": self._locate_target_path(params, "paragraph_index")}},
                                "node_id": {"$ref": {"task_id": last_explore_task_id, "path": self._locate_target_path(params, "node_id")}},
                                "text": {"$ref": {"task_id": last_explore_task_id, "path": self._locate_target_path(params, "text")}}
                            }
                        )
                        params.setdefault("__auto_locator", True)
                # 绑定写回目标章节（供执行阶段一致性校验）
                # 优先使用 locate/explore 结果，避免显式 chapter_id 固化为错误章
                if "__target_chapter_id" not in params:
                    if last_locate_task_id:
                        params["__target_chapter_id"] = {
                            "$ref": {
                                "task_id": last_locate_task_id,
                                "path": "chapter_id"
                            }
                        }
                    elif last_explore_task_id:
                        params["__target_chapter_id"] = {
                            "$ref": {
                                "task_id": last_explore_task_id,
                                "path": self._locate_target_path(params, "chapter_id")
                            }
                        }
                    elif params.get("chapter_id"):
                        params["__target_chapter_id"] = params.get("chapter_id")

                if tool in {"operate_apply", "apply_chapter_edit"}:
                    source_task_id: Optional[int] = None
                    deps = ParameterResolver.extract_dependencies(params)
                    for dep_id in deps:
                        dep_task = task_by_id.get(dep_id)
                        if dep_task and dep_task.get("tool") in {"smart_rewrite", "smart_insert", "smart_continue"}:
                            source_task_id = dep_id
                            break
                    if params.get("operation") in {"replace", "insert"}:
                        params.setdefault("__require_source_locator", True)
                        if last_locate_task_id:
                            params["node_id"] = {"$ref": {"task_id": last_locate_task_id, "path": "node_id"}}
                            params["paragraph_index"] = {"$ref": {"task_id": last_locate_task_id, "path": "paragraph_index"}}
                            params["source_locator"] = {
                                "chapter_id": {"$ref": {"task_id": last_locate_task_id, "path": "chapter_id"}},
                                "paragraph_index": {"$ref": {"task_id": last_locate_task_id, "path": "paragraph_index"}},
                                "node_id": {"$ref": {"task_id": last_locate_task_id, "path": "node_id"}},
                                "text": {"$ref": {"task_id": last_locate_task_id, "path": "text"}}
                            }
                        elif last_explore_task_id:
                            params["node_id"] = {"$ref": {"task_id": last_explore_task_id, "path": self._locate_target_path(params, "node_id")}}
                            params["paragraph_index"] = {"$ref": {"task_id": last_explore_task_id, "path": self._locate_target_path(params, "paragraph_index")}}
                            params["source_locator"] = {
                                "chapter_id": {"$ref": {"task_id": last_explore_task_id, "path": self._locate_target_path(params, "chapter_id")}},
                                "paragraph_index": {"$ref": {"task_id": last_explore_task_id, "path": self._locate_target_path(params, "paragraph_index")}},
                                "node_id": {"$ref": {"task_id": last_explore_task_id, "path": self._locate_target_path(params, "node_id")}},
                                "text": {"$ref": {"task_id": last_explore_task_id, "path": self._locate_target_path(params, "text")}}
                            }
                            params.setdefault("__auto_locator", True)
                        elif source_task_id and not params.get("source_locator"):
                            params["source_locator"] = {
                                "$ref": {"task_id": source_task_id, "path": "data.source_locator"}
                            }
                            params.setdefault("node_id", {"$ref": {"task_id": source_task_id, "path": "data.source_locator.node_id"}})
                            params.setdefault(
                                "paragraph_index",
                                {"$ref": {"task_id": source_task_id, "path": "data.source_locator.paragraph_index"}}
                            )
                            source_task = task_by_id.get(source_task_id, {})
                            if source_task.get("params", {}).get("__auto_locator"):
                                params.setdefault("__auto_locator", True)

                task["params"] = params

        return tasks

    def _has_apply_task(self, tasks: List[Dict[str, Any]], source_task_id: int) -> bool:
        from app.services.agent.parameter_resolver import ParameterResolver

        needle = f"$TASK_{source_task_id}"
        for task in tasks:
            if task.get("tool") not in {"operate_apply", "apply_chapter_edit"}:
                continue
            params = task.get("params", {})
            if source_task_id in ParameterResolver.extract_dependencies(params):
                return True
            try:
                params_str = json.dumps(params, ensure_ascii=False)
            except Exception:
                params_str = str(params)
            if needle in params_str or f"\"task_id\": {source_task_id}" in params_str:
                return True
        return False

    def _build_apply_task(
        self,
        source_tool: str,
        source_task_id: int,
        locate_task_id: Optional[int],
        explore_task_id: Optional[int],
        new_task_id: int,
        source_params: Optional[Dict[str, Any]] = None
    ) -> Optional[Dict[str, Any]]:
        # 🔧 2026-01-12: 跨章节修复 - chapter_id 优先使用 locate_content 的结果
        # locate_content 会在全局搜索时返回目标章节的 chapter_id
        chapter_id_ref = {
            "$ref": {
                "task_id": locate_task_id or source_task_id,
                "path": "chapter_id"
            }
        }

        if source_tool == "smart_rewrite":
            params = {
                "chapter_id": chapter_id_ref,
                "operation": "replace",
                "content": {"$ref": {"task_id": source_task_id, "path": "data.versions[0].content"}},
                "original_text": {"$ref": {"task_id": source_task_id, "path": "data.original_text"}}
            }
        elif source_tool == "smart_continue":
            params = {
                "chapter_id": chapter_id_ref,
                "operation": "append",
                "content": {"$ref": {"task_id": source_task_id, "path": "data.content"}}
            }
        elif source_tool == "rewrite_chapter_content":
            params = {
                "chapter_id": chapter_id_ref,
                "operation": "content",
                "content": {"$ref": {"task_id": source_task_id, "path": "data.content"}}
            }
        elif source_tool == "smart_insert":
            params = {
                "chapter_id": chapter_id_ref,
                "operation": "insert",
                "content": {"$ref": {"task_id": source_task_id, "path": "data.content"}}
            }
            if source_params and source_params.get("user_intent"):
                params["target_description"] = source_params.get("user_intent")
            locate_text_ref = None
            if locate_task_id:
                locate_text_ref = {"$ref": {"task_id": locate_task_id, "path": "text"}}
            elif explore_task_id:
                locate_text_ref = {
                    "$ref": {
                        "task_id": explore_task_id,
                        "path": self._locate_target_path(source_params or {}, "text")
                    }
                }
            if locate_text_ref:
                params.setdefault("locate_target_hint", locate_text_ref)
                params.setdefault("target_description", locate_text_ref)
        else:
            return None

        target_index = None
        target_hint = None
        if source_params:
            target_index = self._coerce_locate_target_index(source_params.get("locate_target_index"))
            target_hint = source_params.get("locate_target_hint")

        if target_index is not None:
            params.setdefault("locate_target_index", target_index)
        if target_hint:
            params.setdefault("locate_target_hint", target_hint)

        # 续写 append 与整章改写不应携带定位字段
        if source_tool not in {"smart_continue", "rewrite_chapter_content"}:
            if locate_task_id:
                params.setdefault("node_id", {"$ref": {"task_id": locate_task_id, "path": "node_id"}})
                params.setdefault("paragraph_index", {"$ref": {"task_id": locate_task_id, "path": "paragraph_index"}})
            elif explore_task_id:
                params.setdefault(
                    "node_id",
                    {"$ref": {"task_id": explore_task_id, "path": self._locate_target_path_from_index(target_index, "node_id")}}
                )
                params.setdefault(
                    "paragraph_index",
                    {"$ref": {"task_id": explore_task_id, "path": self._locate_target_path_from_index(target_index, "paragraph_index")}}
                )
                params.setdefault("__auto_locator", True)

        if source_tool in {"smart_rewrite", "smart_insert"}:
            params.setdefault("__require_source_locator", True)
            params.setdefault(
                "source_locator",
                {"$ref": {"task_id": source_task_id, "path": "data.source_locator"}}
            )
            params.setdefault(
                "node_id",
                {"$ref": {"task_id": source_task_id, "path": "data.source_locator.node_id"}}
            )
            params.setdefault(
                "paragraph_index",
                {"$ref": {"task_id": source_task_id, "path": "data.source_locator.paragraph_index"}}
            )
            if locate_task_id or explore_task_id:
                params.setdefault("__auto_locator", True)

        return {
            "task_id": new_task_id,
            "description": "应用到编辑器",
            "tool": "operate_apply",
            "params": params
        }

    @staticmethod
    def _quick_acceptance_from_text(text: str) -> Optional[Dict[str, Any]]:
        """
        快速提取验收标准

        🔧 2025-12-13: 致命BUG修复 - 正则表达式从\\d{1,3}改为\\d{1,5}
        原正则只匹配1-3位数字，导致"2000字"被错误匹配为"000字"

        Args:
            text: 文本

        Returns:
            验收标准字典，或 None
        """
        m = re.search(
            r"(\d{1,5})\s*(个|条|点|段|篇|章节|章|转折点|要点|场景|角色|人物|种|类|组|步|项|处|部分|方面|建议|方案|问题|观点|字)",
            text or ""
        )
        if m:
            return {"expected_count": int(m.group(1)), "requirement": m.group(0)}
        return None
