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
from typing import Dict, List, Any, Optional, TYPE_CHECKING

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

        # 构建规划 prompt（异步）
        plan_prompt = await self._build_plan_prompt_async(
            message=message,
            work_id=work_id,
            chapter_id=chapter_id,
            context=context,
            conversation_history=conversation_history,
            enable_reflection=enable_reflection
        )

        # 调用 AI 生成规划
        plan_text = ""
        plan_data = None

        try:
            for retry_attempt in range(self.MAX_PLANNING_RETRIES):
                plan_result = await self.agent._generate_text(
                    prompt=plan_prompt,
                    temperature=0.3 + (retry_attempt * 0.1),
                    max_tokens=2000,
                    task_type=TaskType.SIMPLE_QA
                )
                plan_text = plan_result.get("text", "").strip()

                if plan_text:
                    plan_data = self.agent._extract_json_from_text(plan_text)
                    if plan_data and plan_data.get("tasks"):
                        if retry_attempt > 0:
                            logger.info(f"[Planning] 第{retry_attempt + 1}次重试成功")
                        break
                    else:
                        logger.warning(f"[Planning] 第{retry_attempt + 1}次尝试: JSON解析失败或无任务")
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

        if not plan_data or "tasks" not in plan_data:
            plan_data = self._create_default_plan()

        # 规划后处理
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
        from app.services.agent.prompt_cache import (
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

        # 组装完整 prompt
        plan_prompt = f"""AI写作助手。{history_section}{knowledge_section}{selected_text_section}
用户: {message}
work_id: {work_id}
chapter_id: {chapter_id}

{static_prompt}{chapter_planning_hint}"""

        return plan_prompt

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
  2. 任务2: 调用 analyze_text_tool 分析原文中该句话的场景、情绪、角色状态
  3. 任务3: 基于分析结果，给出符合场景的多个修改建议（用 analyze_text_tool 输出）
- ✅ 正确示例：read_chapter_tool → analyze_text_tool(focus="分析'微光如露落雪'在原文中的场景和情绪，给出符合语境的改写建议")
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
                    "tool": "analyze_text_tool",
                    "params": {
                        "text": "$TASK_1$",
                        "focus": "根据用户请求进行分析或回答"
                    },
                    "estimated_time": "10秒"
                }
            ]
        }

    def _post_process_plan(self, plan_data: Dict[str, Any], message: str) -> Dict[str, Any]:
        """
        规划后处理：补充验收标准与 checkpoint

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
        return plan_data

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
