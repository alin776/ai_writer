"""
长期记忆系统 (Long-Term Memory Service)

功能:
1. 跨会话记忆用户偏好
2. 记录用户写作习惯
3. 学习用户风格特征
4. 记住用户反馈（喜欢/不喜欢）

存储结构 (Redis):
- user:{user_id}:preferences - 用户偏好
- user:{user_id}:writing_style - 写作风格
- user:{user_id}:feedback_history - 反馈历史
- user:{user_id}:conversation_summary - 会话摘要
"""

from typing import Dict, List, Optional, Any
from datetime import datetime, timedelta
import json
import redis
import logging
from pydantic import BaseModel
from app.utils.datetime_utils import get_utc_now

logger = logging.getLogger(__name__)


class UserPreferences(BaseModel):
    """用户偏好模型"""
    # 写作偏好
    preferred_length: Optional[str] = "medium"  # short/medium/long
    preferred_style: Optional[str] = None  # 现代/古风/都市/玄幻等
    tone: Optional[str] = "neutral"  # formal/casual/neutral

    # AI行为偏好
    verbosity: str = "balanced"  # concise/balanced/detailed
    creativity_level: float = 0.7  # 0-1, 创意程度

    # 常用功能
    frequent_operations: List[str] = []  # ["continue", "polish", "expand"]

    # 禁忌词/表达
    avoided_words: List[str] = []
    avoided_expressions: List[str] = []

    # 更新时间
    updated_at: str = ""


class WritingStyleProfile(BaseModel):
    """写作风格档案"""
    # 句式特征
    avg_sentence_length: Optional[int] = None
    paragraph_structure: Optional[str] = None  # 短段落/长段落

    # 词汇特征
    vocabulary_richness: Optional[float] = None  # 词汇丰富度
    common_phrases: List[str] = []

    # 叙事特征
    pov: Optional[str] = None  # first_person/third_person
    tense: Optional[str] = None  # past/present

    # 描写偏好
    description_density: Optional[str] = "medium"  # low/medium/high
    dialogue_frequency: Optional[str] = "medium"

    # 样本数量
    sample_count: int = 0
    updated_at: str = ""


class FeedbackEntry(BaseModel):
    """反馈记录"""
    timestamp: str
    operation: str  # continue/polish/expand等
    feedback_type: str  # like/dislike/regenerate
    context: Dict[str, Any]  # 当时的上下文
    reason: Optional[str] = None  # 用户说明的原因


class LongTermMemoryService:
    """长期记忆服务"""

    def __init__(self, redis_client: redis.Redis):
        """
        初始化长期记忆服务

        Args:
            redis_client: Redis客户端实例
        """
        self.redis = redis_client
        self.memory_ttl = 60 * 60 * 24 * 14  # 14天过期

    # ==================== 用户偏好管理 ====================

    def get_user_preferences(self, user_id: str) -> UserPreferences:
        """
        获取用户偏好

        Args:
            user_id: 用户ID

        Returns:
            UserPreferences: 用户偏好对象
        """
        key = f"user:{user_id}:preferences"
        data = self.redis.get(key)

        if data:
            return UserPreferences(**json.loads(data))
        else:
            # 返回默认偏好
            return UserPreferences(
                updated_at=get_utc_now().isoformat()
            )

    def update_user_preferences(
        self,
        user_id: str,
        preferences: Dict[str, Any]
    ) -> UserPreferences:
        """
        更新用户偏好

        Args:
            user_id: 用户ID
            preferences: 要更新的偏好字段

        Returns:
            UserPreferences: 更新后的偏好对象
        """
        current = self.get_user_preferences(user_id)

        # 更新字段
        for key, value in preferences.items():
            if hasattr(current, key):
                setattr(current, key, value)

        current.updated_at = get_utc_now().isoformat()

        # 保存到Redis
        key = f"user:{user_id}:preferences"
        self.redis.setex(
            key,
            self.memory_ttl,
            json.dumps(current.dict())
        )

        return current

    def add_frequent_operation(self, user_id: str, operation: str):
        """
        记录常用操作

        Args:
            user_id: 用户ID
            operation: 操作名称
        """
        prefs = self.get_user_preferences(user_id)

        # 添加操作（保持最近20个）
        if operation not in prefs.frequent_operations:
            prefs.frequent_operations.insert(0, operation)
            prefs.frequent_operations = prefs.frequent_operations[:20]

            self.update_user_preferences(
                user_id,
                {"frequent_operations": prefs.frequent_operations}
            )

    def add_avoided_expression(
        self,
        user_id: str,
        expression: str,
        is_word: bool = False
    ):
        """
        添加禁忌词/表达

        Args:
            user_id: 用户ID
            expression: 禁忌词或表达
            is_word: 是否是单个词（True）还是短语（False）
        """
        prefs = self.get_user_preferences(user_id)

        if is_word:
            if expression not in prefs.avoided_words:
                prefs.avoided_words.append(expression)
        else:
            if expression not in prefs.avoided_expressions:
                prefs.avoided_expressions.append(expression)

        self.update_user_preferences(user_id, {
            "avoided_words": prefs.avoided_words,
            "avoided_expressions": prefs.avoided_expressions
        })

    # ==================== 写作风格管理 ====================

    def get_writing_style(self, user_id: str) -> WritingStyleProfile:
        """
        获取用户写作风格档案

        Args:
            user_id: 用户ID

        Returns:
            WritingStyleProfile: 写作风格档案
        """
        key = f"user:{user_id}:writing_style"
        data = self.redis.get(key)

        if data:
            return WritingStyleProfile(**json.loads(data))
        else:
            return WritingStyleProfile(
                updated_at=get_utc_now().isoformat()
            )

    def update_writing_style(
        self,
        user_id: str,
        style_data: Dict[str, Any]
    ) -> WritingStyleProfile:
        """
        更新写作风格档案

        Args:
            user_id: 用户ID
            style_data: 风格数据

        Returns:
            WritingStyleProfile: 更新后的风格档案
        """
        current = self.get_writing_style(user_id)

        # 更新字段
        for key, value in style_data.items():
            if hasattr(current, key):
                setattr(current, key, value)

        current.sample_count += 1
        current.updated_at = get_utc_now().isoformat()

        # 保存到Redis
        key = f"user:{user_id}:writing_style"
        self.redis.setex(
            key,
            self.memory_ttl,
            json.dumps(current.dict())
        )

        return current

    def learn_from_text(self, user_id: str, text: str):
        """
        从用户文本学习风格特征

        Args:
            user_id: 用户ID
            text: 用户撰写的文本
        """
        # 简单的风格分析
        sentences = text.split('。')
        avg_length = sum(len(s) for s in sentences) / len(sentences) if sentences else 0

        # 检测人称
        pov = "third_person"
        if "我" in text[:100]:
            pov = "first_person"

        # 更新风格档案
        self.update_writing_style(user_id, {
            "avg_sentence_length": int(avg_length),
            "pov": pov
        })

    # ==================== 反馈历史管理 ====================

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
            feedback_type: 反馈类型（like/dislike/regenerate）
            context: 上下文信息
            reason: 反馈原因
        """
        feedback = FeedbackEntry(
            timestamp=get_utc_now().isoformat(),
            operation=operation,
            feedback_type=feedback_type,
            context=context,
            reason=reason
        )

        # 保存到列表（最多保留100条）
        key = f"user:{user_id}:feedback_history"
        self.redis.lpush(key, json.dumps(feedback.dict()))
        self.redis.ltrim(key, 0, 99)  # 只保留最近100条
        self.redis.expire(key, self.memory_ttl)

        # 根据反馈更新偏好
        if feedback_type == "dislike" and reason:
            # 如果用户明确说不喜欢某种表达，记录下来
            if "不要" in reason or "别" in reason:
                # 简单的提取逻辑，实际可以用NLP
                self.add_avoided_expression(user_id, reason, is_word=False)

    def get_feedback_history(
        self,
        user_id: str,
        limit: int = 20
    ) -> List[FeedbackEntry]:
        """
        获取反馈历史

        Args:
            user_id: 用户ID
            limit: 返回数量限制

        Returns:
            List[FeedbackEntry]: 反馈记录列表
        """
        key = f"user:{user_id}:feedback_history"
        items = self.redis.lrange(key, 0, limit - 1)

        return [
            FeedbackEntry(**json.loads(item))
            for item in items
        ]

    def get_feedback_stats(self, user_id: str) -> Dict[str, Any]:
        """
        获取反馈统计

        Args:
            user_id: 用户ID

        Returns:
            Dict: 统计信息
        """
        history = self.get_feedback_history(user_id, limit=100)

        stats = {
            "total": len(history),
            "likes": 0,
            "dislikes": 0,
            "regenerates": 0,
            "by_operation": {}
        }

        for entry in history:
            if entry.feedback_type == "like":
                stats["likes"] += 1
            elif entry.feedback_type == "dislike":
                stats["dislikes"] += 1
            elif entry.feedback_type == "regenerate":
                stats["regenerates"] += 1

            # 按操作统计
            op = entry.operation
            if op not in stats["by_operation"]:
                stats["by_operation"][op] = {"likes": 0, "dislikes": 0}

            if entry.feedback_type == "like":
                stats["by_operation"][op]["likes"] += 1
            elif entry.feedback_type == "dislike":
                stats["by_operation"][op]["dislikes"] += 1

        return stats

    # ==================== 会话摘要管理 ====================

    def save_conversation_summary(
        self,
        user_id: str,
        conversation_id: str,
        summary: str,
        key_points: List[str],
        work_id: Optional[str] = None  # ✅ 新增：作品ID（用于隔离不同作品的记忆）
    ):
        """
        保存会话摘要（用于跨会话记忆）

        Args:
            user_id: 用户ID
            conversation_id: 会话ID
            summary: 会话摘要
            key_points: 关键要点
            work_id: 作品ID（可选，用于隔离不同作品的对话记忆）
        """
        data = {
            "conversation_id": conversation_id,
            "work_id": work_id,  # ✅ 新增：记录work_id
            "summary": summary,
            "key_points": key_points,
            "timestamp": get_utc_now().isoformat()
        }

        key = f"user:{user_id}:conv_summary:{conversation_id}"
        self.redis.setex(
            key,
            self.memory_ttl,
            json.dumps(data)
        )

        # ✅ 新增：如果有work_id，按作品分组保存
        if work_id:
            work_list_key = f"user:{user_id}:work:{work_id}:conversations"
            self.redis.lpush(work_list_key, conversation_id)
            self.redis.ltrim(work_list_key, 0, 49)  # 最多保留50个会话
            self.redis.expire(work_list_key, self.memory_ttl)
            logger.info(f"[LTM] 保存对话到作品 {work_id} 的记忆列表")

        # 添加到全局会话列表（保留原有逻辑，作为降级方案）
        list_key = f"user:{user_id}:conversation_list"
        self.redis.lpush(list_key, conversation_id)
        self.redis.ltrim(list_key, 0, 49)  # 最多保留50个会话
        self.redis.expire(list_key, self.memory_ttl)

    def get_recent_conversations(
        self,
        user_id: str,
        limit: int = 10,
        work_id: Optional[str] = None  # ✅ 新增：作品ID过滤
    ) -> List[Dict[str, Any]]:
        """
        获取最近的会话摘要

        Args:
            user_id: 用户ID
            limit: 返回数量
            work_id: 作品ID（可选，用于只获取特定作品的对话）

        Returns:
            List[Dict]: 会话摘要列表
        """
        # 🔧 P0-3修复：规范化work_id
        work_id = work_id if work_id and work_id.strip() else None

        # ✅ 优先从work-specific列表检索
        if work_id:
            list_key = f"user:{user_id}:work:{work_id}:conversations"
            conv_ids = self.redis.lrange(list_key, 0, limit - 1)
            logger.info(f"[LTM] 从作品 {work_id} 检索到 {len(conv_ids)} 条对话ID")
        else:
            # 降级：使用全局列表（可能跨作品污染）
            list_key = f"user:{user_id}:conversation_list"
            conv_ids = self.redis.lrange(list_key, 0, limit - 1)
            logger.warning(f"[LTM] work_id未设置，使用全局对话列表（可能跨作品污染）")

        summaries = []
        for conv_id in conv_ids:
            key = f"user:{user_id}:conv_summary:{conv_id.decode()}"
            data = self.redis.get(key)
            if data:
                conv_data = json.loads(data)

                # ✅ 二次过滤：确保work_id匹配（防止数据不一致）
                # 🔧 修复：严格work_id隔离 - 指定work_id时只返回匹配的数据
                stored_work_id = conv_data.get("work_id")

                if work_id:
                    # 当指定了work_id时，只接受完全匹配的数据
                    if stored_work_id != work_id:
                        # 过滤掉：不匹配的数据 或 旧数据（None）
                        if stored_work_id is None:
                            logger.info(f"[LTM] 过滤旧数据（无work_id）：conv_id={conv_id.decode()}, "
                                      f"当前查询work_id={work_id}")
                        else:
                            logger.debug(f"[LTM] 过滤不匹配对话：conv_id={conv_id.decode()}, "
                                       f"expected={work_id}, actual={stored_work_id}")
                        continue

                # work_id未指定时，接受所有数据（包括旧数据）
                summaries.append(conv_data)

        logger.info(f"[LTM] 最终返回 {len(summaries)} 条对话摘要 (work_id={work_id})")
        return summaries

    # ==================== 综合记忆检索 ====================

    def get_user_context(self, user_id: str, work_id: Optional[str] = None) -> Dict[str, Any]:
        """
        获取用户的完整记忆上下文
        （供Agent使用，包含所有相关记忆）

        Args:
            user_id: 用户ID
            work_id: 作品ID（可选，用于隔离不同作品的对话记忆）

        Returns:
            Dict: 完整的用户上下文
        """
        preferences = self.get_user_preferences(user_id)
        style = self.get_writing_style(user_id)
        feedback_stats = self.get_feedback_stats(user_id)
        # ✅ P0遗漏修复：传递work_id以隔离不同作品的对话
        recent_convs = self.get_recent_conversations(
            user_id=user_id,
            limit=3,
            work_id=work_id
        )

        return {
            "preferences": preferences.dict(),
            "writing_style": style.dict(),
            "feedback_stats": feedback_stats,
            "recent_conversations": recent_convs,
            "memory_quality": self._assess_memory_quality(
                preferences,
                style,
                feedback_stats
            )
        }

    def _assess_memory_quality(
        self,
        preferences: UserPreferences,
        style: WritingStyleProfile,
        feedback_stats: Dict[str, Any]
    ) -> str:
        """
        评估记忆质量

        Returns:
            str: low/medium/high
        """
        score = 0

        # 有偏好设置
        if preferences.preferred_style:
            score += 1

        # 有风格样本
        if style.sample_count > 0:
            score += 1
        if style.sample_count > 5:
            score += 1

        # 有反馈历史
        if feedback_stats["total"] > 0:
            score += 1
        if feedback_stats["total"] > 10:
            score += 1

        if score <= 1:
            return "low"
        elif score <= 3:
            return "medium"
        else:
            return "high"

    def format_memory_for_prompt(self, user_id: str, work_id: Optional[str] = None) -> str:
        """
        将用户记忆格式化为Prompt文本
        （供Agent的system prompt使用）

        Args:
            user_id: 用户ID
            work_id: 作品ID（可选，用于记忆隔离）

        Returns:
            str: 格式化的记忆文本
        """
        context = self.get_user_context(user_id, work_id=work_id)
        prefs = context["preferences"]
        style = context["writing_style"]

        prompt_parts = ["# 用户记忆上下文\n"]

        # 写作偏好
        if prefs.get("preferred_style"):
            prompt_parts.append(f"- 用户偏好的写作风格: {prefs['preferred_style']}")

        prompt_parts.append(f"- 用户偏好的内容长度: {prefs['preferred_length']}")
        prompt_parts.append(f"- 用户偏好的语气: {prefs['tone']}")
        prompt_parts.append(f"- AI输出详细程度: {prefs['verbosity']}")

        # 写作风格
        if style.get("pov"):
            prompt_parts.append(f"- 用户常用人称: {style['pov']}")

        if style.get("avg_sentence_length"):
            prompt_parts.append(f"- 用户平均句长: {style['avg_sentence_length']}字")

        # 禁忌
        if prefs.get("avoided_expressions"):
            avoided = ", ".join(prefs["avoided_expressions"][:5])
            prompt_parts.append(f"- 用户不喜欢的表达: {avoided}")

        # 常用功能
        if prefs.get("frequent_operations"):
            frequent = ", ".join(prefs["frequent_operations"][:5])
            prompt_parts.append(f"- 用户常用功能: {frequent}")

        # 记忆质量提示
        quality = context["memory_quality"]
        if quality == "low":
            prompt_parts.append("\n注意: 这是新用户，记忆数据较少，建议主动询问偏好。")
        elif quality == "high":
            prompt_parts.append("\n注意: 这是老用户，已有丰富的偏好数据，请严格遵循用户习惯。")

        return "\n".join(prompt_parts)
