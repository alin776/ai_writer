"""
记忆重要度动态调整器 (P2-2修复)

实现记忆重要度的动态调整机制：
1. 访问时提升重要度（被引用的记忆更重要）
2. 时间衰减（长时间未访问的记忆重要度下降）
3. 上下文关联调整（与当前话题相关的记忆重要度提升）

核心思想：
- 艾宾浩斯遗忘曲线：记忆强度随时间指数衰减
- 使用频率强化：频繁访问的记忆更重要
- 上下文相关性：与当前任务相关的记忆临时提升

使用示例：
```python
adjuster = DynamicImportanceAdjuster(redis_client)

# 访问时调整
new_importance = await adjuster.adjust_on_access(memory)

# 定时衰减
await adjuster.apply_time_decay(user_id)

# 上下文关联调整
await adjuster.adjust_by_context(user_id, current_query)
```
"""

import logging
import math
from datetime import datetime, timezone, timedelta
from typing import List, Dict, Any, Optional
from dataclasses import dataclass, field
from redis import Redis

logger = logging.getLogger(__name__)


@dataclass
class AdjustmentConfig:
    """
    重要度调整配置

    可根据不同场景调整参数
    """
    # === 访问调整参数 ===
    access_boost: float = 0.05           # 每次访问增加的重要度
    access_boost_cap: float = 0.3        # 访问增加的重要度上限
    rapid_access_bonus: float = 0.02     # 短时间内多次访问的额外奖励
    rapid_access_window: int = 3600      # 短时间窗口（秒）

    # === 时间衰减参数 ===
    decay_start_days: int = 7            # 开始衰减的天数（7天后开始衰减）
    decay_rate: float = 0.95             # 每天的衰减率（保留95%）
    min_importance: float = 0.1          # 最低重要度（不会衰减到0）

    # === 上下文调整参数 ===
    context_boost: float = 0.1           # 上下文相关性提升
    context_boost_duration: int = 1800   # 上下文提升持续时间（秒）

    # === 引用调整参数 ===
    reference_boost: float = 0.15        # 被其他记忆引用时的提升
    citation_boost: float = 0.2          # 被用户明确引用时的提升


@dataclass
class AdjustmentEvent:
    """
    重要度调整事件记录

    用于审计和调试
    """
    memory_id: str
    event_type: str                      # access/decay/context/reference
    old_importance: float
    new_importance: float
    reason: str
    timestamp: datetime = field(default_factory=lambda: datetime.now(timezone.utc))


class DynamicImportanceAdjuster:
    """
    动态重要度调整器

    负责记忆重要度的动态调整，包括：
    1. 访问强化：被访问的记忆重要度提升
    2. 时间衰减：长期未访问的记忆重要度下降
    3. 上下文关联：与当前话题相关的记忆临时提升
    4. 引用强化：被引用的记忆重要度提升
    """

    def __init__(
        self,
        redis_client: Redis,
        config: Optional[AdjustmentConfig] = None
    ):
        """
        初始化调整器

        Args:
            redis_client: Redis客户端
            config: 调整配置（可选）
        """
        self.redis = redis_client
        self.config = config or AdjustmentConfig()
        self._event_log: List[AdjustmentEvent] = []

        logger.info(
            f"[ImportanceAdjuster] Initialized: "
            f"decay_start={self.config.decay_start_days}d, "
            f"decay_rate={self.config.decay_rate}, "
            f"access_boost={self.config.access_boost}"
        )

    async def adjust_on_access(
        self,
        user_id: str,
        memory_id: str,
        current_importance: float,
        access_count: int,
        last_access: Optional[datetime] = None
    ) -> float:
        """
        访问时调整重要度

        策略：
        1. 基础提升：每次访问增加importance
        2. 频繁访问奖励：短时间内多次访问额外奖励
        3. 设置访问提升上限，避免无限增长

        Args:
            user_id: 用户ID
            memory_id: 记忆ID
            current_importance: 当前重要度
            access_count: 历史访问次数
            last_access: 上次访问时间

        Returns:
            调整后的重要度
        """
        old_importance = current_importance
        boost = 0.0

        # 1. 基础访问提升（随访问次数递减，避免无限提升）
        # 使用对数衰减：log(1 + count) / log(base)
        diminishing_factor = 1.0 / math.log(2 + access_count)
        base_boost = self.config.access_boost * diminishing_factor
        boost += base_boost

        # 2. 短时间内频繁访问奖励
        if last_access:
            time_since_last = (datetime.now(timezone.utc) - last_access).total_seconds()
            if time_since_last < self.config.rapid_access_window:
                # 越频繁访问，奖励越高
                frequency_factor = 1.0 - (time_since_last / self.config.rapid_access_window)
                rapid_boost = self.config.rapid_access_bonus * frequency_factor
                boost += rapid_boost

        # 3. 计算总提升，应用上限
        total_boost = min(boost, self.config.access_boost_cap)

        # 4. 计算新重要度
        new_importance = min(current_importance + total_boost, 1.0)

        # 5. 更新Redis中的重要度
        await self._update_importance_in_redis(
            user_id, memory_id, new_importance, access_count + 1
        )

        # 6. 记录事件
        self._log_event(AdjustmentEvent(
            memory_id=memory_id,
            event_type="access",
            old_importance=old_importance,
            new_importance=new_importance,
            reason=f"Access #{access_count + 1}, boost={total_boost:.4f}"
        ))

        logger.debug(
            f"[ImportanceAdjuster] Access adjustment: "
            f"memory={memory_id}, {old_importance:.3f} -> {new_importance:.3f} "
            f"(+{total_boost:.4f})"
        )

        return new_importance

    async def apply_time_decay(
        self,
        user_id: str,
        memories: List[Dict[str, Any]]
    ) -> List[Dict[str, Any]]:
        """
        应用时间衰减

        基于艾宾浩斯遗忘曲线的时间衰减：
        - 7天内：不衰减
        - 7天后：每天保留95%

        公式：new_importance = importance * (decay_rate ^ (days - decay_start_days))

        Args:
            user_id: 用户ID
            memories: 记忆列表

        Returns:
            调整后的记忆列表
        """
        now = datetime.now(timezone.utc)
        adjusted_memories = []
        decay_count = 0

        for memory in memories:
            memory_id = memory.get("id", "")
            old_importance = memory.get("importance", 0.5)
            last_access = memory.get("last_access") or memory.get("created_at")

            # 解析时间
            if isinstance(last_access, str):
                try:
                    last_access = datetime.fromisoformat(last_access.replace("Z", "+00:00"))
                except:
                    last_access = now

            if not last_access:
                last_access = now

            # 计算天数
            days_since_access = (now - last_access).days

            # 如果超过衰减起始天数，应用衰减
            if days_since_access > self.config.decay_start_days:
                decay_days = days_since_access - self.config.decay_start_days
                decay_factor = self.config.decay_rate ** decay_days
                new_importance = max(
                    old_importance * decay_factor,
                    self.config.min_importance
                )

                if new_importance < old_importance:
                    # 更新Redis
                    await self._update_importance_only(user_id, memory_id, new_importance)

                    # 记录事件
                    self._log_event(AdjustmentEvent(
                        memory_id=memory_id,
                        event_type="decay",
                        old_importance=old_importance,
                        new_importance=new_importance,
                        reason=f"Time decay: {decay_days} days, factor={decay_factor:.4f}"
                    ))

                    decay_count += 1
                    memory["importance"] = new_importance

            adjusted_memories.append(memory)

        if decay_count > 0:
            logger.info(
                f"[ImportanceAdjuster] Time decay applied: "
                f"user={user_id}, decayed={decay_count}/{len(memories)} memories"
            )

        return adjusted_memories

    async def adjust_by_context(
        self,
        user_id: str,
        memories: List[Dict[str, Any]],
        current_query: str,
        keywords: Optional[List[str]] = None
    ) -> List[Dict[str, Any]]:
        """
        根据上下文调整重要度

        与当前查询相关的记忆临时提升重要度

        Args:
            user_id: 用户ID
            memories: 记忆列表
            current_query: 当前查询
            keywords: 关键词列表（可选）

        Returns:
            调整后的记忆列表（带临时提升标记）
        """
        if not keywords:
            keywords = self._extract_keywords(current_query)

        if not keywords:
            return memories

        keywords_lower = [k.lower() for k in keywords]
        adjusted_memories = []
        context_boost_count = 0

        for memory in memories:
            content = memory.get("content", "").lower()
            memory_keywords = memory.get("keywords", [])

            # 计算与当前上下文的相关性
            relevance_score = 0.0

            # 1. 内容关键词匹配
            for kw in keywords_lower:
                if kw in content:
                    relevance_score += 0.2  # 每个匹配的关键词加0.2

            # 2. 标签/关键词匹配
            for mk in memory_keywords:
                if mk.lower() in keywords_lower:
                    relevance_score += 0.3  # 标签匹配更重要

            # 如果有相关性，应用上下文提升
            if relevance_score > 0:
                context_boost = min(
                    relevance_score * self.config.context_boost,
                    self.config.context_boost  # 上限
                )

                old_importance = memory.get("importance", 0.5)
                # 临时提升（不持久化，只用于当前检索）
                memory["_context_adjusted_importance"] = min(
                    old_importance + context_boost, 1.0
                )
                memory["_context_boost"] = context_boost
                context_boost_count += 1

            adjusted_memories.append(memory)

        if context_boost_count > 0:
            logger.debug(
                f"[ImportanceAdjuster] Context adjustment: "
                f"boosted={context_boost_count}/{len(memories)} memories, "
                f"keywords={keywords[:5]}"
            )

        return adjusted_memories

    async def adjust_on_reference(
        self,
        user_id: str,
        memory_id: str,
        current_importance: float,
        reference_type: str = "implicit"
    ) -> float:
        """
        被引用时调整重要度

        当记忆被其他记忆引用或被用户明确引用时，提升重要度

        Args:
            user_id: 用户ID
            memory_id: 记忆ID
            current_importance: 当前重要度
            reference_type: 引用类型（implicit=隐式引用, explicit=显式引用）

        Returns:
            调整后的重要度
        """
        old_importance = current_importance

        if reference_type == "explicit":
            # 用户明确引用（如"根据之前提到的..."）
            boost = self.config.citation_boost
        else:
            # 隐式引用（如检索时匹配到）
            boost = self.config.reference_boost

        new_importance = min(current_importance + boost, 1.0)

        # 更新Redis
        await self._update_importance_only(user_id, memory_id, new_importance)

        # 记录事件
        self._log_event(AdjustmentEvent(
            memory_id=memory_id,
            event_type="reference",
            old_importance=old_importance,
            new_importance=new_importance,
            reason=f"Reference type={reference_type}, boost={boost:.4f}"
        ))

        logger.debug(
            f"[ImportanceAdjuster] Reference adjustment: "
            f"memory={memory_id}, {old_importance:.3f} -> {new_importance:.3f} "
            f"(type={reference_type})"
        )

        return new_importance

    async def batch_decay(
        self,
        user_id: str
    ) -> Dict[str, Any]:
        """
        批量应用时间衰减（定时任务调用）

        遍历用户所有记忆，应用时间衰减

        Args:
            user_id: 用户ID

        Returns:
            衰减统计
        """
        # 获取所有中期记忆
        medium_key = f"memory:{user_id}:medium_term"

        try:
            # 获取所有记忆及其分数
            memories_data = self.redis.zrange(medium_key, 0, -1, withscores=True)

            if not memories_data:
                return {"decayed": 0, "total": 0}

            import json
            memories = []
            for data, score in memories_data:
                try:
                    if isinstance(data, bytes):
                        data = data.decode('utf-8')
                    memory = json.loads(data)
                    memory["importance"] = score
                    memories.append(memory)
                except:
                    continue

            # 应用衰减
            adjusted = await self.apply_time_decay(user_id, memories)

            # 统计衰减数量
            decayed_count = sum(
                1 for m in adjusted
                if m.get("importance", 0) < memories[adjusted.index(m)].get("importance", 0)
            )

            return {
                "decayed": decayed_count,
                "total": len(memories),
                "user_id": user_id
            }

        except Exception as e:
            logger.error(f"[ImportanceAdjuster] Batch decay failed: {e}")
            return {"decayed": 0, "total": 0, "error": str(e)}

    def _extract_keywords(self, text: str) -> List[str]:
        """
        提取关键词（简单版本）

        Args:
            text: 文本

        Returns:
            关键词列表
        """
        import re

        # 简单分词：提取中文词汇和英文单词
        # 中文：连续汉字
        cn_words = re.findall(r'[\u4e00-\u9fff]{2,}', text)
        # 英文：连续字母
        en_words = re.findall(r'[a-zA-Z]{3,}', text.lower())

        # 去重并限制数量
        keywords = list(set(cn_words + en_words))[:20]
        return keywords

    async def _update_importance_in_redis(
        self,
        user_id: str,
        memory_id: str,
        new_importance: float,
        new_access_count: int
    ):
        """更新Redis中的重要度和访问计数"""
        import json

        # 更新中期记忆的分数
        medium_key = f"memory:{user_id}:medium_term"

        try:
            # 获取所有记忆
            memories = self.redis.zrange(medium_key, 0, -1)

            for data in memories:
                if isinstance(data, bytes):
                    data = data.decode('utf-8')

                memory = json.loads(data)
                if memory.get("id") == memory_id:
                    # 更新字段
                    memory["importance"] = new_importance
                    memory["access_count"] = new_access_count
                    memory["last_access"] = datetime.now(timezone.utc).isoformat()

                    # 删除旧记录，添加新记录
                    pipe = self.redis.pipeline()
                    pipe.zrem(medium_key, data)
                    pipe.zadd(medium_key, {json.dumps(memory, ensure_ascii=False): new_importance})
                    pipe.execute()

                    logger.debug(
                        f"[ImportanceAdjuster] Updated Redis: "
                        f"memory={memory_id}, importance={new_importance:.3f}"
                    )
                    break

        except Exception as e:
            logger.error(f"[ImportanceAdjuster] Failed to update Redis: {e}")

    async def _update_importance_only(
        self,
        user_id: str,
        memory_id: str,
        new_importance: float
    ):
        """只更新重要度"""
        await self._update_importance_in_redis(
            user_id, memory_id, new_importance, 0  # 访问计数不变
        )

    def _log_event(self, event: AdjustmentEvent):
        """记录调整事件"""
        self._event_log.append(event)

        # 保持事件日志在合理范围内
        if len(self._event_log) > 1000:
            self._event_log = self._event_log[-500:]

    def get_recent_events(
        self,
        limit: int = 50,
        event_type: Optional[str] = None
    ) -> List[AdjustmentEvent]:
        """
        获取最近的调整事件

        Args:
            limit: 最大返回数量
            event_type: 过滤事件类型

        Returns:
            事件列表
        """
        events = self._event_log

        if event_type:
            events = [e for e in events if e.event_type == event_type]

        return events[-limit:]

    def get_adjustment_stats(self) -> Dict[str, Any]:
        """
        获取调整统计

        Returns:
            统计信息
        """
        events = self._event_log

        stats = {
            "total_events": len(events),
            "by_type": {},
            "avg_boost": 0.0,
            "avg_decay": 0.0
        }

        # 按类型统计
        for event in events:
            event_type = event.event_type
            if event_type not in stats["by_type"]:
                stats["by_type"][event_type] = 0
            stats["by_type"][event_type] += 1

        # 计算平均提升和衰减
        boosts = [
            e.new_importance - e.old_importance
            for e in events
            if e.new_importance > e.old_importance
        ]
        decays = [
            e.old_importance - e.new_importance
            for e in events
            if e.new_importance < e.old_importance
        ]

        if boosts:
            stats["avg_boost"] = sum(boosts) / len(boosts)
        if decays:
            stats["avg_decay"] = sum(decays) / len(decays)

        return stats


# 全局单例
_default_adjuster: Optional[DynamicImportanceAdjuster] = None


def get_importance_adjuster(redis_client: Redis) -> DynamicImportanceAdjuster:
    """
    获取全局默认的重要度调整器实例

    Args:
        redis_client: Redis客户端

    Returns:
        DynamicImportanceAdjuster实例
    """
    global _default_adjuster
    if _default_adjuster is None:
        _default_adjuster = DynamicImportanceAdjuster(redis_client)
    return _default_adjuster
