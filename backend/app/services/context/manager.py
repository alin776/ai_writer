"""
上下文管理 - 核心管理器

为chat_stream()提供上下文管理能力：
- 构建上下文：从存储加载并格式化为LLM消息
- 更新上下文：保存新的对话轮次
- 压缩上下文：当Token超限时自动压缩
"""

import time
import logging
from typing import List, Optional, Dict, Any

from app.services.context.models import (
    Context, Message, ShortMemory, SummaryMemory, TokenBudget
)
from app.services.context.store import ContextStore, RedisContextStore
from app.services.context.monitoring_integration import (
    monitor_context_build,
    monitor_context_update,
    monitor_summary_generation,
    record_compression_metrics,
    record_memory_size
)

logger = logging.getLogger(__name__)


class ContextManager:
    """上下文管理器 - 专为chat_stream优化"""

    def __init__(
        self,
        store: Optional[ContextStore] = None,
        token_budget: Optional[TokenBudget] = None,
        ai_service: Optional[Any] = None  # ✅ 新增：AI服务（用于LLM摘要）
    ):
        self.store = store or RedisContextStore()
        self.token_budget = token_budget or TokenBudget()
        self.ai_service = ai_service  # ✅ 保存AI服务引用
        self._summary_service = None  # ✅ 懒加载摘要服务

    @monitor_context_build
    async def build_context(
        self,
        session_id: str,
        system_prompt: str = ""
    ) -> Dict[str, Any]:
        """
        构建上下文 - 用于chat_stream方法

        Returns:
            Dict包含:
            - messages: List[Dict] - 格式化的LLM消息列表
            - metadata: Dict - 元数据（token数、消息数等）
            - context: Context - 原始Context对象（供后续更新使用）
        """
        # 加载或创建上下文
        context = await self.store.load(session_id)

        if not context:
            context = Context(
                session_id=session_id,
                system_prompt=system_prompt
            )
            logger.info(f"[ContextManager] 创建新上下文: {session_id}")

        # 检查Token使用情况
        total_tokens = context.get_total_tokens()
        max_tokens = self.token_budget.total

        logger.info(f"[ContextManager] Session {session_id}: {total_tokens}/{max_tokens} tokens")

        # 如果超过80%预算，触发压缩
        if total_tokens > max_tokens * 0.8:
            logger.warning(f"[ContextManager] Token使用率过高 ({total_tokens}/{max_tokens}), 触发压缩")
            await self.compress_context(context)

        # 构建LLM消息列表
        messages = self._build_messages(context)

        return {
            "messages": messages,
            "metadata": {
                "session_id": session_id,
                "token_count": context.get_total_tokens(),
                "short_memory_size": len(context.short_memory.messages),
                "has_summary": bool(context.summary_memory.summary),
                "compression_triggered": total_tokens > max_tokens * 0.8
            },
            "context": context  # 返回context对象供后续更新
        }

    def _build_messages(self, context: Context) -> List[Dict]:
        """
        构建LLM消息列表

        按照Token预算分配：
        1. 系统提示 (20%)
        2. 摘要上下文 (25%)
        3. 近期对话 (35%)
        """
        messages = []

        # 1. 系统提示词 (20%)
        if context.system_prompt:
            messages.append({
                "role": "system",
                "content": context.system_prompt
            })

        # 2. 摘要上下文 (25%)
        if context.summary_memory.summary:
            summary_content = f"对话摘要：\n{context.summary_memory.summary}"

            # 添加重要事实
            if context.summary_memory.important_facts:
                facts = "\n".join(f"- {fact}" for fact in context.summary_memory.important_facts)
                summary_content += f"\n\n重要信息：\n{facts}"

            messages.append({
                "role": "system",
                "content": summary_content
            })

        # 3. 近期对话 (35%)
        for msg in context.short_memory.messages:
            messages.append({
                "role": msg.role,
                "content": msg.content
            })

        return messages

    @monitor_context_update
    async def update_context(
        self,
        session_id: str,
        new_messages: List[Dict],
        context: Optional[Context] = None
    ):
        """
        更新上下文 - chat_stream完成后调用

        Args:
            session_id: 会话ID
            new_messages: 新消息列表 [{"role": "user", "content": "..."}, ...]
            context: 现有上下文（如果有）
        """
        if not context:
            context = await self.store.load(session_id)
            if not context:
                context = Context(session_id=session_id)

        # 添加新消息到短期记忆
        for msg_dict in new_messages:
            message = Message(
                role=msg_dict["role"],
                content=msg_dict["content"],
                timestamp=time.time(),
                metadata=msg_dict.get("metadata", {})
            )
            context.short_memory.add_message(message)

        # 保存更新后的上下文
        await self.store.save(context)

        logger.info(
            f"[ContextManager] 更新上下文: {session_id}, "
            f"消息数={len(context.short_memory.messages)}, "
            f"Token={context.get_total_tokens()}"
        )

    async def compress_context(self, context: Context):
        """
        压缩上下文 - 当Token超限时调用

        策略：
        1. 保留最近2轮对话（4条消息）
        2. 将旧消息生成摘要
        3. 提取重要事实
        """
        logger.info(f"[ContextManager] 开始压缩: {context.session_id}")

        # ✅ 记录压缩前的Token数（用于监控）
        original_tokens = context.get_total_tokens()

        # 获取需要摘要的消息（保留最近2轮）
        messages_to_summarize = context.short_memory.messages[:-4] if len(context.short_memory.messages) > 4 else []

        if not messages_to_summarize:
            logger.info(f"[ContextManager] 消息数不足，无需压缩")
            return

        # 生成摘要
        new_summary = await self._generate_summary(messages_to_summarize)

        # 合并到现有摘要
        if context.summary_memory.summary:
            context.summary_memory.summary = f"{context.summary_memory.summary}\n\n---\n\n{new_summary}"
        else:
            context.summary_memory.summary = new_summary

        context.summary_memory.last_updated = time.time()

        # 清理已摘要的消息，只保留最近4条
        context.short_memory.messages = context.short_memory.messages[-4:] if len(context.short_memory.messages) > 4 else context.short_memory.messages

        # ✅ 记录压缩后的Token数和内存使用（用于监控）
        compressed_tokens = context.get_total_tokens()
        record_compression_metrics(original_tokens, compressed_tokens, context.session_id)
        record_memory_size(
            len(context.short_memory.messages),
            len(context.summary_memory.summary),
            context.session_id
        )

        logger.info(
            f"[ContextManager] 压缩完成: {context.session_id}, "
            f"保留{len(context.short_memory.messages)}条消息, "
            f"摘要长度={len(context.summary_memory.summary)}"
        )

    @monitor_summary_generation
    async def _generate_summary(self, messages: List[Message]) -> str:
        """
        生成对话摘要（LLM驱动）

        策略：
        1. 如果有AI服务，使用LLM生成高质量摘要
        2. 如果没有AI服务，使用降级策略（简单提取）
        """
        if not messages:
            return ""

        # ✅ 如果没有AI服务，使用降级策略
        if self.ai_service is None:
            logger.info("[ContextManager] AI服务未配置，使用简单摘要策略")
            return self._fallback_summary(messages)

        try:
            # ✅ 懒加载摘要服务
            if self._summary_service is None:
                from app.services.context.summary_service import SummaryService
                self._summary_service = SummaryService(self.ai_service)
                logger.info("[ContextManager] ✅ SummaryService已初始化")

            # ✅ 调用LLM生成摘要
            summary = await self._summary_service.summarize_conversation(
                messages,
                max_length=200
            )
            return summary

        except Exception as e:
            logger.error(f"[ContextManager] ❌ LLM摘要失败: {e}，使用降级策略")
            return self._fallback_summary(messages)

    def _fallback_summary(self, messages: List[Message]) -> str:
        """
        降级策略：简单提取式摘要（当LLM不可用时）

        策略与SummaryService._fallback_summary相同
        """
        if not messages:
            return ""

        # 简单策略：提取用户请求和助手回复的关键信息
        summary_parts = []

        user_messages = [m for m in messages if m.role == "user"]
        assistant_messages = [m for m in messages if m.role == "assistant"]

        if user_messages:
            first_user = user_messages[0].content[:100]
            summary_parts.append(f"用户请求: {first_user}...")

        if assistant_messages:
            first_assistant = assistant_messages[0].content[:100]
            summary_parts.append(f"助手回复: {first_assistant}...")

        # 统计信息
        summary_parts.append(f"共{len(messages)}条消息")

        return " | ".join(summary_parts)

    async def clear_context(self, session_id: str):
        """清除上下文 - 用于重置会话"""
        await self.store.delete(session_id)
        logger.info(f"[ContextManager] 清除上下文: {session_id}")

    def set_ai_service(self, ai_service: Any):
        """
        设置AI服务（向后兼容）

        用于在创建ContextManager后注入AI服务

        Args:
            ai_service: HTTPAIService实例
        """
        self.ai_service = ai_service
        self._summary_service = None  # 重置摘要服务，下次使用时重新初始化
        logger.info("[ContextManager] ✅ AI服务已设置")
