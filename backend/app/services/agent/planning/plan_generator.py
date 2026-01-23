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
        conversation_history: str = "",
        enable_reflection: bool = False
    ) -> Dict[str, Any]:
        """
        生成任务规划

        Args:
            message: 用户消息
            work_id: 作品ID
            chapter_id: 章节ID
            context: 额外上下文
            conversation_history: 对话历史
            enable_reflection: 是否启用反思模式

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
            conversation_history=conversation_history,
            enable_reflection=enable_reflection
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
            for retry_attempt in range(self.MAX_PLANNING_RETRIES):
                # 🔧 2025-12-29: 规划任务需要理解对话上下文，使用 STORY_PLANNING 选择更强模型
                plan_result = await self.agent._generate_text(
                    prompt=plan_prompt_base,
                    temperature=0.3 + (retry_attempt * 0.1),
                    max_tokens=2000,
                    task_type=TaskType.STORY_PLANNING
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
            plan_data = self._post_process_plan(plan_data, message)

        increment_counter("planning_phase_completed")
        logger.info(f"[Planning] 规划生成成功，共{len(plan_data['tasks'])}个任务")

        return plan_data

    async def _build_plan_prompt_async(
        self,
        message: str,
        work_id: Optional[str],
        chapter_id: Optional[str],
        context: Optional[Dict[str, Any]],
        conversation_history: str,
        enable_reflection: bool
    ) -> str:
        """
        异步构建规划 Prompt

        Args:
            message: 用户消息
            work_id: 作品ID
            chapter_id: 章节ID
            context: 额外上下文
            conversation_history: 对话历史
            enable_reflection: 是否启用反思模式

        Returns:
            规划 prompt 字符串
        """
        from app.services.agent.prompts import (
            get_planning_static_prompt,
            get_planning_agent_mode_prompt
        )

        # 历史部分
        history_section = ""
        if conversation_history:
            history_section = f"""
【对话历史】
{conversation_history}

"""

        # 获取静态 Prompt
        if enable_reflection:
            static_prompt = await get_planning_agent_mode_prompt()
        else:
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
        """构建章节上下文提示"""
        if not chapter_id:
            return ""

        return f"""

⚠️ 【章节上下文提示】：
- 当前用户在章节聊天面板中（chapter_id={chapter_id}）
- 用户要求修改/润色本章内容时，必须使用以下流程：
  1. 任务1: 调用 read_chapter_tool(work_id="{work_id}", chapter_id="{chapter_id}") 读取章节完整内容
  2. 任务2: 调用 analyze_content 分析原文中该句话的场景、情绪、角色状态（analysis_types="text"）
  3. 任务3: 基于分析结果，给出符合场景的多个修改建议（用 analyze_content 输出）
- ✅ 正确示例：read_chapter_tool → analyze_content(focus="场景情绪分析", analysis_types="text")
- ⚠️ focus 参数必须简洁（15字以内）
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

    def _post_process_plan(self, plan_data: Dict[str, Any], message: str) -> Dict[str, Any]:
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
        for idx, t in enumerate(tasks):
            if acceptance_hint and not t.get("acceptance"):
                t["acceptance"] = acceptance_hint
            # 保证至少首个任务打 checkpoint，便于早期反思校验
            if "checkpoint" not in t:
                t["checkpoint"] = (idx == 0)

        plan_data["tasks"] = tasks

        # 🔧 2025-12-25: 新增规划验证和自动修复
        plan_data = self._validate_and_fix_plan(plan_data, message)
        plan_data["tasks"] = self._ensure_editor_apply_tasks(plan_data.get("tasks", []))

        return self._normalize_plan_schema(plan_data)

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

        # 验证1: 人物查询必须先搜索
        tasks = self._validate_search_before_read(tasks, message)

        # 验证2: 检查多章节批量读取格式（现在工具支持范围格式）
        tasks = self._optimize_multi_chapter_tasks(tasks, message)

        # 验证3: 约束补齐（范围/段落/禁止整章/禁止越界）
        constraints = self._extract_task_constraints(message)
        if constraints:
            tasks = self._apply_constraints_to_tasks(tasks, constraints)

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
            r"第\s*\d+\s*[到至\-~—～]\s*\d+\s*章",
            r"第\s*[一二两三四五六七八九十]+\s*[到至\-~—～]\s*[一二两三四五六七八九十]+\s*章",
            r"章节\s*\(?\s*\d+\s*[到至\-~—～]\s*\d+\s*\)?",
            r"\d+\s*[到至\-~—～]\s*\d+\s*章",
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
        idx = 0

        while idx < len(tasks):
            task = tasks[idx]
            tool = task.get("tool")
            task_id = task.get("task_id")
            params = task.get("params", {}) or {}

            if tool == "locate_content":
                last_locate_task_id = task_id

            if tool in {"smart_rewrite", "smart_continue", "smart_insert"} and task_id:
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
                "content": {"$ref": {"task_id": source_task_id, "path": "versions[0].content"}},
                "original_text": {"$ref": {"task_id": source_task_id, "path": "original_text"}}
            }
        elif source_tool == "smart_continue":
            params = {
                "chapter_id": chapter_id_ref,
                "operation": "append",
                "content": {"$ref": {"task_id": source_task_id, "path": "content"}}
            }
        elif source_tool == "smart_insert":
            params = {
                "chapter_id": chapter_id_ref,
                "operation": "insert",
                "content": {"$ref": {"task_id": source_task_id, "path": "content"}}
            }
            if source_params and source_params.get("user_intent"):
                params["target_description"] = source_params.get("user_intent")
        else:
            return None

        if locate_task_id:
            params.setdefault("node_id", {"$ref": {"task_id": locate_task_id, "path": "node_id"}})
            params.setdefault("paragraph_index", {"$ref": {"task_id": locate_task_id, "path": "paragraph_index"}})

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
