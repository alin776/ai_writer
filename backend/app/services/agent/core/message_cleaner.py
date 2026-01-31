"""
消息清理模块 - 智能清理累积的消息

从 langgraph_agent.py 的 _handle_with_httpai 方法中拆分。
负责防止消息上下文无限增长。
"""

import logging
from typing import List

from langchain_core.messages import (
    BaseMessage,
    SystemMessage,
    HumanMessage,
    AIMessage,
    ToolMessage,
)

logger = logging.getLogger(__name__)


class MessageCleaner:
    """消息清理器 - 智能清理累积的消息，防止上下文无限增长"""

    # 触发清理的消息数量阈值
    CLEANUP_THRESHOLD = 8

    # 最大保留的 AI-Tool 交互对数
    MAX_PAIRS = 2

    @classmethod
    def clean_messages(cls, messages: List[BaseMessage]) -> List[BaseMessage]:
        """
        智能清理累积的消息

        清理策略：
        1. 保留所有系统消息（通常只有1条）
        2. 保留最近的1条用户消息（当前请求）
        3. 保留最近的2对 AI-Tool 交互（最多4条）
        总共最多保留: 1(system) + 1(user) + 4(ai+tool) = 6条

        Args:
            messages: 当前消息列表

        Returns:
            清理后的消息列表
        """
        message_count = len(messages)

        # 消息数量未超过阈值，无需清理
        if message_count <= cls.CLEANUP_THRESHOLD:
            logger.debug(f"[MessageCleaner] 消息数量 {message_count} 条，无需清理")
            return messages

        # 分类消息
        system_messages = []
        user_messages = []
        ai_messages = []
        tool_messages = []

        for msg in messages:
            if isinstance(msg, SystemMessage):
                system_messages.append(msg)
            elif isinstance(msg, HumanMessage):
                user_messages.append(msg)
            elif isinstance(msg, AIMessage):
                ai_messages.append(msg)
            elif isinstance(msg, ToolMessage):
                tool_messages.append(msg)

        # 开始清理
        cleaned_messages = system_messages.copy()

        # 保留最近的用户消息
        if user_messages:
            cleaned_messages.append(user_messages[-1])

        # 智能成对保留最近的 AI-Tool 交互
        # 确保 AI 消息和 Tool 消息成对保留，避免破坏对话连贯性
        recent_pairs = cls._get_recent_pairs(
            ai_messages, tool_messages, messages
        )
        cleaned_messages.extend(recent_pairs)

        # 计算压缩率
        compression_rate = 100 - len(cleaned_messages) * 100 // message_count
        logger.info(
            f"[MessageCleaner] 🧹 智能清理累积消息："
            f"{message_count}条 -> 保留{len(cleaned_messages)}条"
            f"（压缩率 {compression_rate}%）"
        )

        return cleaned_messages

    @classmethod
    def _get_recent_pairs(
        cls,
        ai_messages: List[AIMessage],
        tool_messages: List[ToolMessage],
        original_messages: List[BaseMessage],
    ) -> List[BaseMessage]:
        """
        获取最近的 AI-Tool 消息对

        Args:
            ai_messages: AI 消息列表
            tool_messages: Tool 消息列表
            original_messages: 原始消息列表（用于保持顺序）

        Returns:
            按原始顺序排列的最近消息对
        """
        recent_pairs = []
        ai_idx = len(ai_messages) - 1
        tool_idx = len(tool_messages) - 1

        # 从最新的开始，成对保留最多 MAX_PAIRS 对交互
        pairs_count = 0
        while pairs_count < cls.MAX_PAIRS and ai_idx >= 0 and tool_idx >= 0:
            # 成对添加（先 AI 后 Tool）
            recent_pairs.insert(0, tool_messages[tool_idx])
            recent_pairs.insert(0, ai_messages[ai_idx])
            ai_idx -= 1
            tool_idx -= 1
            pairs_count += 1

        # 按原始顺序重组
        result = []
        for msg in original_messages:
            if msg in recent_pairs:
                result.append(msg)

        return result

    @classmethod
    def should_clean(cls, messages: List[BaseMessage]) -> bool:
        """检查是否需要清理消息"""
        return len(messages) > cls.CLEANUP_THRESHOLD
