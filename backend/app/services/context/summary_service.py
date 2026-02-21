"""
摘要生成服务 - 使用LLM生成高质量对话摘要

目标: 将摘要质量从3/10提升到8/10
策略: 使用gpt-4o-mini生成结构化摘要，降级到简单提取
"""

import logging
from typing import List, Optional
from datetime import datetime

from app.services.context.models import Message
from app.services.agent.model_selector import TaskType  # ✅ 新增：用于成本追踪

logger = logging.getLogger(__name__)


class SummaryService:
    """摘要生成服务 - LLM驱动"""

    def __init__(self, ai_service):
        """
        初始化摘要服务

        Args:
            ai_service: HTTPAIService实例（懒加载）
        """
        self.ai_service = ai_service
        self.default_model = "gpt-5.2"

    async def summarize_conversation(
        self,
        messages: List[Message],
        max_length: int = 200,
        language: str = "zh"
    ) -> str:
        """
        生成对话摘要（主入口）

        Args:
            messages: 对话消息列表
            max_length: 最大摘要长度（字符）
            language: 语言 (zh/en)

        Returns:
            对话摘要（结构化）
        """
        if not messages:
            return ""

        # 检查AI服务是否可用
        if self.ai_service is None:
            logger.warning("AI服务不可用，使用降级策略")
            return self._fallback_summary(messages, max_length)

        try:
            # 构建Prompt
            system_prompt, user_prompt = self._build_summary_prompt(
                messages, max_length, language
            )

            # 调用LLM生成摘要
            logger.info(f"使用LLM生成摘要（{len(messages)}条消息）")
            summary = await self.ai_service.call_ai(
                system_prompt=system_prompt,
                user_prompt=user_prompt,
                max_tokens=300,  # 控制输出长度
                temperature=0.3,  # 低温度保证稳定性
                task_type=TaskType.SUMMARIZATION  # ✅ 新增：摘要任务
            )

            # 验证摘要质量
            if self._validate_summary(summary, max_length):
                logger.info(f"✅ LLM摘要生成成功: {len(summary)}字符")
                return summary.strip()
            else:
                logger.warning("⚠️ LLM摘要质量不达标，使用降级策略")
                return self._fallback_summary(messages, max_length)

        except Exception as e:
            logger.error(f"❌ LLM摘要生成失败: {e}，使用降级策略")
            return self._fallback_summary(messages, max_length)

    def _build_summary_prompt(
        self,
        messages: List[Message],
        max_length: int,
        language: str
    ) -> tuple[str, str]:
        """
        构建结构化Prompt

        Returns:
            (system_prompt, user_prompt)
        """
        # 系统提示词（定义任务）
        if language == "zh":
            system_prompt = f"""你是一个专业的对话摘要助手。
请为用户和AI助手的对话生成简洁摘要，长度控制在{max_length}字以内。

摘要要求：
1. 提取用户的核心需求和问题
2. 总结已完成的任务和决策
3. 列出重要的事实和结论
4. 保持客观中立，不添加评价

输出格式示例：
用户需求：[核心需求]
讨论内容：[关键讨论点]
重要决策：[决策或结论]
待办事项：[未完成的任务]（如有）"""
        else:
            system_prompt = f"""You are a professional conversation summarizer.
Generate a concise summary (max {max_length} chars) of the user-assistant conversation.

Requirements:
1. Extract core user needs and questions
2. Summarize completed tasks and decisions
3. List important facts and conclusions
4. Stay objective, no opinions

Output format example:
User needs: [core needs]
Discussion: [key points]
Decisions: [decisions or conclusions]
Todo: [pending tasks] (if any)"""

        # 用户提示词（提供对话内容）
        conversation_text = self._format_messages(messages)
        user_prompt = f"请为以下对话生成摘要：\n\n{conversation_text}"

        return system_prompt, user_prompt

    def _format_messages(self, messages: List[Message]) -> str:
        """
        格式化消息为文本

        Args:
            messages: 消息列表

        Returns:
            格式化的对话文本
        """
        lines = []
        for msg in messages:
            role = "用户" if msg.role == "user" else "助手"
            # 限制每条消息长度，避免Prompt过长
            content = msg.content[:500] if len(msg.content) > 500 else msg.content
            lines.append(f"{role}: {content}")

        return "\n".join(lines)

    def _validate_summary(self, summary: str, max_length: int) -> bool:
        """
        验证摘要质量

        质量标准:
        1. 长度合理（不为空，不超过max_length*1.2）
        2. 包含关键词（用户/需求/助手/讨论等）
        3. 不是错误信息

        Args:
            summary: 生成的摘要
            max_length: 最大允许长度

        Returns:
            是否通过验证
        """
        if not summary or len(summary) < 10:
            logger.warning(f"摘要过短: {len(summary)}字符")
            return False

        if len(summary) > max_length * 1.5:
            logger.warning(f"摘要过长: {len(summary)} > {max_length * 1.5}")
            return False

        # 检查是否包含基本关键词（中文或英文）
        keywords_zh = ["用户", "需求", "讨论", "决策", "任务"]
        keywords_en = ["user", "need", "discussion", "decision", "task"]

        has_keywords = (
            any(kw in summary for kw in keywords_zh) or
            any(kw.lower() in summary.lower() for kw in keywords_en)
        )

        if not has_keywords:
            logger.warning("摘要缺少关键结构")
            return False

        # 检查是否为错误信息
        error_patterns = ["error", "failed", "错误", "失败", "异常"]
        if any(pattern in summary.lower() for pattern in error_patterns):
            logger.warning("摘要包含错误信息")
            return False

        return True

    def _fallback_summary(
        self,
        messages: List[Message],
        max_length: int
    ) -> str:
        """
        降级策略：简单提取式摘要

        策略:
        1. 提取第一个用户消息（用户需求）
        2. 提取最后一个助手消息（当前状态）
        3. 添加统计信息

        Args:
            messages: 消息列表
            max_length: 最大长度

        Returns:
            简单摘要
        """
        if not messages:
            return ""

        # 提取用户消息和助手消息
        user_messages = [m for m in messages if m.role == "user"]
        assistant_messages = [m for m in messages if m.role == "assistant"]

        summary_parts = []

        # 第一个用户请求
        if user_messages:
            first_user = user_messages[0].content[:100]
            summary_parts.append(f"用户请求: {first_user}...")

        # 最后一个助手回复
        if assistant_messages:
            last_assistant = assistant_messages[-1].content[:100]
            summary_parts.append(f"当前进展: {last_assistant}...")

        # 统计信息
        summary_parts.append(
            f"共{len(messages)}条消息，"
            f"{len(user_messages)}个用户请求，"
            f"{len(assistant_messages)}个助手回复"
        )

        summary = " ".join(summary_parts)

        # 截断到max_length
        if len(summary) > max_length:
            summary = summary[:max_length - 3] + "..."

        return summary
