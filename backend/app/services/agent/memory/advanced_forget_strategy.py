"""
高级遗忘策略 (P2-5修复)

实现更智能的遗忘机制：
1. 多维度评分：综合考虑时间、重要度、访问频率、关联性
2. 保护机制：关键记忆不被遗忘
3. 渐进遗忘：从降权到真正删除的多阶段过程
4. 上下文感知：根据当前任务动态调整

核心思想：
- 艾宾浩斯遗忘曲线：记忆强度随时间指数衰减
- 间隔重复：频繁复习的记忆保留更久
- 情感权重：情感强烈的记忆更难遗忘
- 关联网络：与其他记忆关联多的更重要

使用示例：
```python
strategy = AdvancedForgetStrategy(config)

# 计算遗忘分数
score = await strategy.calculate_forget_score(memory)

# 选择要遗忘的记忆
to_forget = await strategy.select_memories_to_forget(memories, target=10)

# 应用渐进遗忘
await strategy.apply_gradual_forgetting(memories)
```
"""

import math
import logging
from datetime import datetime, timezone, timedelta
from typing import List, Dict, Any, Optional, Set, Tuple
from dataclasses import dataclass, field
from enum import Enum

from .memory_config import MemoryConfig

logger = logging.getLogger(__name__)


class ForgetStage(Enum):
    """遗忘阶段"""
    ACTIVE = "active"          # 活跃：正常使用
    FADING = "fading"          # 褪色：开始遗忘
    DORMANT = "dormant"        # 休眠：很少使用
    ARCHIVED = "archived"      # 归档：准备删除
    FORGOTTEN = "forgotten"    # 遗忘：可以删除


class ProtectionLevel(Enum):
    """保护级别"""
    NONE = 0                   # 无保护
    LOW = 1                    # 低保护
    MEDIUM = 2                 # 中等保护
    HIGH = 3                   # 高保护
    PERMANENT = 4              # 永久保护


@dataclass
class ForgetConfig:
    """
    遗忘策略配置

    可根据不同场景调整参数
    默认值统一从 MemoryConfig 读取
    """
    # === 时间衰减参数 ===
    decay_half_life_days: float = MemoryConfig.DECAY_HALF_LIFE_DAYS
    max_retention_days: int = MemoryConfig.MAX_RETENTION_DAYS

    # === 重要度阈值 ===
    critical_importance: float = MemoryConfig.CRITICAL_IMPORTANCE
    high_importance: float = MemoryConfig.HIGH_IMPORTANCE
    medium_importance: float = MemoryConfig.MEDIUM_IMPORTANCE

    # === 访问频率参数 ===
    access_boost_factor: float = MemoryConfig.ACCESS_BOOST_FACTOR
    max_access_boost: float = MemoryConfig.MAX_ACCESS_BOOST

    # === 关联性参数 ===
    link_protection_factor: float = MemoryConfig.LINK_PROTECTION_FACTOR
    max_link_protection: float = MemoryConfig.MAX_LINK_PROTECTION

    # === 遗忘阶段阈值 ===
    fading_threshold: float = MemoryConfig.FADING_THRESHOLD
    dormant_threshold: float = MemoryConfig.DORMANT_THRESHOLD
    archived_threshold: float = MemoryConfig.ARCHIVED_THRESHOLD
    forgotten_threshold: float = MemoryConfig.FORGOTTEN_THRESHOLD

    # === 批量遗忘参数 ===
    min_retention_count: int = MemoryConfig.MIN_RETENTION_COUNT
    max_forget_per_batch: int = MemoryConfig.MAX_FORGET_PER_BATCH


@dataclass
class ForgetDecision:
    """
    遗忘决策

    包含是否遗忘及原因
    """
    memory_id: str
    should_forget: bool
    forget_score: float
    stage: ForgetStage
    reason: str
    protection_level: ProtectionLevel
    factors: Dict[str, float] = field(default_factory=dict)


class AdvancedForgetStrategy:
    """
    高级遗忘策略

    实现多维度、渐进式的智能遗忘机制
    """

    def __init__(self, config: Optional[ForgetConfig] = None):
        """
        初始化遗忘策略

        Args:
            config: 遗忘配置
        """
        self.config = config or ForgetConfig()
        self._protection_rules: List[Dict[str, Any]] = []

        # 初始化默认保护规则
        self._init_default_protection_rules()

        logger.info(
            f"[AdvancedForget] Initialized: "
            f"half_life={self.config.decay_half_life_days}d, "
            f"max_retention={self.config.max_retention_days}d"
        )

    def _init_default_protection_rules(self):
        """初始化默认保护规则"""
        # 规则格式：{"condition": func, "level": ProtectionLevel, "reason": str}
        self._protection_rules = [
            # 1. 关键设定不遗忘
            {
                "name": "critical_settings",
                "keywords": ["大纲", "设定", "角色", "世界观", "主角", "配角"],
                "level": ProtectionLevel.PERMANENT,
                "reason": "包含关键设定信息"
            },
            # 2. 用户明确要求保留
            {
                "name": "user_marked",
                "metadata_key": "pinned",
                "level": ProtectionLevel.PERMANENT,
                "reason": "用户标记为重要"
            },
            # 3. 高重要度记忆保护
            {
                "name": "high_importance",
                "min_importance": 0.9,
                "level": ProtectionLevel.HIGH,
                "reason": "高重要度记忆"
            },
            # 4. 最近访问过的记忆
            {
                "name": "recently_accessed",
                "max_access_age_hours": 24,
                "level": ProtectionLevel.MEDIUM,
                "reason": "最近被访问过"
            },
            # 5. 有多个关联的记忆
            {
                "name": "highly_linked",
                "min_links": 5,
                "level": ProtectionLevel.LOW,
                "reason": "关联多个其他记忆"
            }
        ]

    def add_protection_rule(self, rule: Dict[str, Any]):
        """添加自定义保护规则"""
        self._protection_rules.append(rule)

    async def calculate_forget_score(
        self,
        memory: Dict[str, Any],
        current_context: Optional[str] = None
    ) -> Tuple[float, Dict[str, float]]:
        """
        计算记忆的遗忘分数

        分数越高越可能被遗忘 (0.0 = 保留, 1.0 = 遗忘)

        Args:
            memory: 记忆数据
            current_context: 当前上下文（用于相关性计算）

        Returns:
            (遗忘分数, 各因素得分)
        """
        factors = {}

        # === 1. 时间衰减因子 ===
        time_factor = self._calculate_time_decay(memory)
        factors["time_decay"] = time_factor

        # === 2. 重要度因子（反向）===
        importance = memory.get("importance", 0.5)
        importance_factor = 1.0 - importance
        factors["importance"] = importance_factor

        # === 3. 访问频率因子（反向）===
        access_factor = self._calculate_access_factor(memory)
        factors["access_frequency"] = access_factor

        # === 4. 关联性因子（反向）===
        link_factor = self._calculate_link_factor(memory)
        factors["links"] = link_factor

        # === 5. 上下文相关性因子（反向）===
        if current_context:
            context_factor = self._calculate_context_relevance(memory, current_context)
            factors["context_relevance"] = context_factor
        else:
            factors["context_relevance"] = 0.5

        # === 6. 内容长度因子（长内容可能更重要）===
        content = memory.get("content", "")
        length_factor = 1.0 - min(len(content) / 2000, 0.5)  # 长内容保护
        factors["content_length"] = length_factor

        # === 综合计算 ===
        # 权重分配
        weights = {
            "time_decay": 0.35,         # 时间衰减权重最高
            "importance": 0.25,         # 重要度次之
            "access_frequency": 0.15,   # 访问频率
            "links": 0.10,              # 关联性
            "context_relevance": 0.10,  # 上下文相关性
            "content_length": 0.05      # 内容长度
        }

        forget_score = sum(
            factors[key] * weights[key]
            for key in weights
        )

        # 应用保护
        protection = self._check_protection(memory)
        if protection.level == ProtectionLevel.PERMANENT:
            forget_score = 0.0
        elif protection.level == ProtectionLevel.HIGH:
            forget_score *= 0.3
        elif protection.level == ProtectionLevel.MEDIUM:
            forget_score *= 0.6
        elif protection.level == ProtectionLevel.LOW:
            forget_score *= 0.8

        factors["final_protection"] = protection.level.value / 4.0

        return min(forget_score, 1.0), factors

    def _calculate_time_decay(self, memory: Dict[str, Any]) -> float:
        """
        计算时间衰减因子

        使用指数衰减模型：R = e^(-t/τ)
        其中 τ = half_life / ln(2)
        """
        # 获取最后访问时间或创建时间
        last_access = memory.get("last_access") or memory.get("created_at")

        if isinstance(last_access, str):
            try:
                last_access = datetime.fromisoformat(last_access.replace("Z", "+00:00"))
            except:
                return 0.5  # 默认中等衰减

        if not last_access:
            return 0.5

        # 计算经过的天数
        now = datetime.now(timezone.utc)
        days_elapsed = (now - last_access).total_seconds() / 86400

        # 指数衰减
        tau = self.config.decay_half_life_days / math.log(2)
        decay = 1.0 - math.exp(-days_elapsed / tau)

        # 超过最大保留天数，强制遗忘
        if days_elapsed > self.config.max_retention_days:
            decay = 1.0

        return min(decay, 1.0)

    def _calculate_access_factor(self, memory: Dict[str, Any]) -> float:
        """
        计算访问频率因子

        访问越多，遗忘分数越低
        """
        access_count = memory.get("access_count", 0)

        # 使用对数增长
        if access_count == 0:
            return 1.0  # 从未访问

        # 访问次数越多，因子越低
        # 使用 1 / (1 + log(1 + count)) 的形式
        factor = 1.0 - min(
            math.log(1 + access_count) * self.config.access_boost_factor,
            self.config.max_access_boost
        )

        return max(factor, 0.0)

    def _calculate_link_factor(self, memory: Dict[str, Any]) -> float:
        """
        计算关联性因子

        关联越多，遗忘分数越低
        """
        links = memory.get("links", [])
        link_count = len(links) if isinstance(links, list) else 0

        # 关联数越多，因子越低
        factor = 1.0 - min(
            link_count * self.config.link_protection_factor,
            self.config.max_link_protection
        )

        return max(factor, 0.0)

    def _calculate_context_relevance(
        self,
        memory: Dict[str, Any],
        current_context: str
    ) -> float:
        """
        计算上下文相关性因子

        与当前上下文越相关，遗忘分数越低
        """
        content = memory.get("content", "").lower()
        context_lower = current_context.lower()

        # 简单的关键词匹配
        context_words = set(context_lower.split())
        content_words = set(content.split())

        if not context_words or not content_words:
            return 0.5

        # Jaccard相似度
        intersection = len(context_words & content_words)
        union = len(context_words | content_words)

        similarity = intersection / union if union > 0 else 0

        # 相似度越高，遗忘因子越低
        return 1.0 - min(similarity * 2, 1.0)

    def _check_protection(self, memory: Dict[str, Any]) -> ForgetDecision:
        """
        检查记忆的保护状态

        Args:
            memory: 记忆数据

        Returns:
            保护决策
        """
        content = memory.get("content", "").lower()
        metadata = memory.get("metadata", {})

        highest_protection = ProtectionLevel.NONE
        protection_reason = ""

        for rule in self._protection_rules:
            # 关键词检查
            if "keywords" in rule:
                if any(kw in content for kw in rule["keywords"]):
                    if rule["level"].value > highest_protection.value:
                        highest_protection = rule["level"]
                        protection_reason = rule["reason"]

            # 元数据检查
            if "metadata_key" in rule:
                if metadata.get(rule["metadata_key"]):
                    if rule["level"].value > highest_protection.value:
                        highest_protection = rule["level"]
                        protection_reason = rule["reason"]

            # 重要度检查
            if "min_importance" in rule:
                if memory.get("importance", 0) >= rule["min_importance"]:
                    if rule["level"].value > highest_protection.value:
                        highest_protection = rule["level"]
                        protection_reason = rule["reason"]

            # 访问时间检查
            if "max_access_age_hours" in rule:
                last_access = memory.get("last_access")
                if last_access:
                    if isinstance(last_access, str):
                        try:
                            last_access = datetime.fromisoformat(last_access.replace("Z", "+00:00"))
                        except:
                            continue

                    hours_ago = (datetime.now(timezone.utc) - last_access).total_seconds() / 3600
                    if hours_ago <= rule["max_access_age_hours"]:
                        if rule["level"].value > highest_protection.value:
                            highest_protection = rule["level"]
                            protection_reason = rule["reason"]

            # 关联数检查
            if "min_links" in rule:
                links = memory.get("links", [])
                if len(links) >= rule["min_links"]:
                    if rule["level"].value > highest_protection.value:
                        highest_protection = rule["level"]
                        protection_reason = rule["reason"]

        return ForgetDecision(
            memory_id=memory.get("id", ""),
            should_forget=highest_protection == ProtectionLevel.NONE,
            forget_score=0.0,  # 稍后计算
            stage=ForgetStage.ACTIVE,
            reason=protection_reason or "无保护",
            protection_level=highest_protection
        )

    def determine_stage(self, forget_score: float) -> ForgetStage:
        """
        根据遗忘分数确定记忆阶段

        Args:
            forget_score: 遗忘分数

        Returns:
            记忆阶段
        """
        if forget_score >= self.config.forgotten_threshold:
            return ForgetStage.FORGOTTEN
        elif forget_score >= self.config.archived_threshold:
            return ForgetStage.ARCHIVED
        elif forget_score >= self.config.dormant_threshold:
            return ForgetStage.DORMANT
        elif forget_score >= self.config.fading_threshold:
            return ForgetStage.FADING
        else:
            return ForgetStage.ACTIVE

    async def select_memories_to_forget(
        self,
        memories: List[Dict[str, Any]],
        target_count: int,
        current_context: Optional[str] = None
    ) -> List[ForgetDecision]:
        """
        选择要遗忘的记忆

        Args:
            memories: 候选记忆列表
            target_count: 目标遗忘数量
            current_context: 当前上下文

        Returns:
            遗忘决策列表
        """
        decisions = []

        # 计算每个记忆的遗忘分数
        for memory in memories:
            score, factors = await self.calculate_forget_score(memory, current_context)
            protection = self._check_protection(memory)
            stage = self.determine_stage(score)

            decision = ForgetDecision(
                memory_id=memory.get("id", ""),
                should_forget=score >= self.config.forgotten_threshold and protection.level == ProtectionLevel.NONE,
                forget_score=score,
                stage=stage,
                reason=protection.reason if protection.level != ProtectionLevel.NONE else f"遗忘分数: {score:.3f}",
                protection_level=protection.level,
                factors=factors
            )
            decisions.append(decision)

        # 按遗忘分数排序
        decisions.sort(key=lambda d: d.forget_score, reverse=True)

        # 选择要遗忘的记忆
        to_forget = []
        for decision in decisions:
            if decision.should_forget:
                to_forget.append(decision)
                if len(to_forget) >= min(target_count, self.config.max_forget_per_batch):
                    break

        # 确保至少保留min_retention_count个记忆
        total_remaining = len(memories) - len(to_forget)
        if total_remaining < self.config.min_retention_count:
            # 减少遗忘数量
            keep_count = len(memories) - self.config.min_retention_count
            to_forget = to_forget[:max(0, keep_count)]

        logger.info(
            f"[AdvancedForget] Selected {len(to_forget)}/{len(memories)} memories to forget, "
            f"target={target_count}"
        )

        return to_forget

    async def apply_gradual_forgetting(
        self,
        memories: List[Dict[str, Any]],
        current_context: Optional[str] = None
    ) -> Dict[str, List[Dict[str, Any]]]:
        """
        应用渐进遗忘

        将记忆分类到不同的遗忘阶段

        Args:
            memories: 记忆列表
            current_context: 当前上下文

        Returns:
            按阶段分类的记忆
        """
        staged = {
            ForgetStage.ACTIVE: [],
            ForgetStage.FADING: [],
            ForgetStage.DORMANT: [],
            ForgetStage.ARCHIVED: [],
            ForgetStage.FORGOTTEN: []
        }

        for memory in memories:
            score, factors = await self.calculate_forget_score(memory, current_context)
            stage = self.determine_stage(score)

            memory["_forget_score"] = score
            memory["_forget_stage"] = stage.value
            memory["_forget_factors"] = factors

            staged[stage].append(memory)

        # 记录统计
        logger.info(
            f"[AdvancedForget] Gradual forgetting: "
            f"active={len(staged[ForgetStage.ACTIVE])}, "
            f"fading={len(staged[ForgetStage.FADING])}, "
            f"dormant={len(staged[ForgetStage.DORMANT])}, "
            f"archived={len(staged[ForgetStage.ARCHIVED])}, "
            f"forgotten={len(staged[ForgetStage.FORGOTTEN])}"
        )

        return {stage.value: memories for stage, memories in staged.items()}

    def get_config(self) -> ForgetConfig:
        """获取当前配置"""
        return self.config

    def update_config(self, **kwargs):
        """更新配置"""
        for key, value in kwargs.items():
            if hasattr(self.config, key):
                setattr(self.config, key, value)
                logger.info(f"[AdvancedForget] Updated config: {key}={value}")
