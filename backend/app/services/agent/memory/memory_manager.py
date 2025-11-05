"""
记忆管理器 (Memory Manager)

统一管理Agent的所有记忆模块:
- 短期记忆: 对话历史
- 长期记忆: 用户偏好
- 用户画像: 行为模式
- 知识库: 作品设定

供Agent调用的统一接口
"""

from typing import Dict, List, Optional, Any
from datetime import datetime
import redis
import logging
import asyncio

from .long_term_memory import LongTermMemoryService
from .user_profile import UserProfileMemory

logger = logging.getLogger(__name__)


class MemoryManager:
    """统一记忆管理器"""

    def __init__(self, redis_client: redis.Redis):
        """
        初始化记忆管理器

        Args:
            redis_client: Redis客户端
        """
        self.long_term_memory = LongTermMemoryService(redis_client)
        self.user_profile = UserProfileMemory(redis_client)
        self.redis = redis_client

    # ==================== 统一记忆检索接口 ====================

    async def get_complete_context(
        self,
        user_id: str,
        include_profile: bool = True,
        include_preferences: bool = True,
        include_recent_conversations: bool = True
    ) -> Dict[str, Any]:
        """
        获取完整的用户记忆上下文
        （供Agent使用）

        Args:
            user_id: 用户ID
            include_profile: 是否包含用户画像
            include_preferences: 是否包含用户偏好
            include_recent_conversations: 是否包含最近会话

        Returns:
            Dict: 完整上下文
        """
        context = {
            "user_id": user_id,
            "retrieved_at": datetime.now().isoformat()
        }

        if include_preferences:
            # 使用 asyncio.to_thread() 包装同步Redis调用，避免阻塞事件循环
            context["user_context"] = await asyncio.to_thread(
                self.long_term_memory.get_user_context,
                user_id
            )

        if include_profile:
            context["user_profile"] = await asyncio.to_thread(
                self.user_profile.get_full_profile,
                user_id
            )

        if include_recent_conversations:
            context["recent_conversations"] = await asyncio.to_thread(
                self.long_term_memory.get_recent_conversations,
                user_id,
                3  # limit参数
            )

        return context

    def format_context_for_agent(
        self,
        user_id: str,
        mode: str = "full"
    ) -> str:
        """
        为Agent格式化记忆上下文
        （生成Agent的system prompt补充内容）

        Args:
            user_id: 用户ID
            mode: full/minimal/preferences_only

        Returns:
            str: 格式化的上下文文本
        """
        if mode == "preferences_only":
            return self.long_term_memory.format_memory_for_prompt(user_id)

        elif mode == "minimal":
            # 只包含最关键的信息
            prefs = self.long_term_memory.get_user_preferences(user_id)
            skill = self.user_profile.get_skill_level(user_id)

            return f"""# 用户基本信息
- 技能等级: {skill.overall_level}
- 偏好风格: {prefs.preferred_style or '未设置'}
- 偏好长度: {prefs.preferred_length}
"""

        else:  # full
            # 完整上下文
            part1 = self.long_term_memory.format_memory_for_prompt(user_id)
            part2 = self.user_profile.format_profile_for_agent(user_id)

            parts = [part1, "\n", part2]
            return "\n".join(parts)

    # ==================== 记忆更新接口 ====================

    def record_user_interaction(
        self,
        user_id: str,
        interaction_type: str,
        data: Dict[str, Any]
    ):
        """
        记录用户交互
        （自动更新相关记忆模块）

        Args:
            user_id: 用户ID
            interaction_type: 交互类型
            data: 交互数据
        """
        # 记录到用户画像
        self.user_profile.track_action(
            user_id,
            interaction_type,
            data
        )

        # 如果是常用操作，更新偏好
        if interaction_type in ["continue", "polish", "expand", "rewrite"]:
            self.long_term_memory.add_frequent_operation(user_id, interaction_type)

    def record_feedback(
        self,
        user_id: str,
        operation: str,
        feedback_type: str,
        context: Dict[str, Any],
        reason: Optional[str] = None
    ):
        """
        记录用户反馈

        Args:
            user_id: 用户ID
            operation: 操作类型
            feedback_type: 反馈类型
            context: 上下文
            reason: 反馈原因
        """
        self.long_term_memory.record_feedback(
            user_id,
            operation,
            feedback_type,
            context,
            reason
        )

    def learn_from_user_text(self, user_id: str, text: str):
        """
        从用户文本学习风格

        Args:
            user_id: 用户ID
            text: 用户撰写的文本
        """
        self.long_term_memory.learn_from_text(user_id, text)

    # ==================== 会话管理 ====================

    def start_session(self, user_id: str):
        """开始新会话"""
        self.user_profile.track_session_start(user_id)

    def end_session(self, user_id: str, words_created: int = 0):
        """结束会话"""
        self.user_profile.track_session_end(user_id, words_created)

    def save_conversation(
        self,
        user_id: str,
        conversation_id: str,
        messages: List[Dict[str, Any]]
    ):
        """
        保存对话历史（带自动摘要）

        Args:
            user_id: 用户ID
            conversation_id: 会话ID
            messages: 对话消息列表
        """
        # 简单的摘要生成（实际可以用LLM生成）
        summary = f"共{len(messages)}轮对话"

        # 提取关键操作
        key_points = []
        for msg in messages:
            if msg.get("role") == "user":
                content = msg.get("content", "")
                if len(content) > 10:
                    key_points.append(content[:50])

        self.long_term_memory.save_conversation_summary(
            user_id,
            conversation_id,
            summary,
            key_points[:5]
        )

    # ==================== 智能推荐 ====================

    def get_personalized_suggestions(self, user_id: str) -> List[str]:
        """
        获取个性化建议

        Args:
            user_id: 用户ID

        Returns:
            List[str]: 建议列表
        """
        profile = self.user_profile.get_full_profile(user_id)
        return profile.get("recommendations", [])

    def should_use_agent_mode(self, user_id: str) -> bool:
        """
        判断是否推荐使用Agent模式

        Args:
            user_id: 用户ID

        Returns:
            bool: 是否推荐Agent模式
        """
        skill = self.user_profile.get_skill_level(user_id)
        interaction = self.user_profile.get_interaction_mode(user_id)

        # 新手或高度依赖Agent的用户，推荐Agent模式
        return (
            skill.overall_level == "novice" or
            interaction.agent_dependency > 0.6
        )

    # ==================== 记忆统计 ====================

    def get_memory_stats(self, user_id: str) -> Dict[str, Any]:
        """
        获取记忆统计信息

        Args:
            user_id: 用户ID

        Returns:
            Dict: 统计信息
        """
        user_context = self.long_term_memory.get_user_context(user_id)
        profile = self.user_profile.get_full_profile(user_id)

        return {
            "memory_quality": user_context["memory_quality"],
            "skill_level": profile["skill_level"]["overall_level"],
            "total_feedback": user_context["feedback_stats"]["total"],
            "sessions_per_week": profile["behavior_pattern"]["sessions_per_week"],
            "agent_dependency": profile["interaction_mode"]["agent_dependency"]
        }
