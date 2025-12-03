"""
智能遗忘策略 (Smart Forget Strategy)

实现基于重要度计算的智能遗忘机制，避免简单的FIFO策略导致重要信息丢失。

核心算法:
    重要度 = 初始重要度 × 时间衰减 × 访问频率加权

时间衰减采用指数衰减函数（艾宾浩斯遗忘曲线）:
    时间衰减 = e^(-decay_rate × 时间差(小时))

访问频率加权:
    访问加权 = 1 + log(1 + access_count)
"""

import math
from datetime import datetime
from typing import List, Dict, Any, Tuple
from .types import MemoryItem, ForgetDecision
from app.utils.datetime_utils import get_utc_now


class SmartForgetStrategy:
    """
    智能遗忘策略

    根据记忆的重要度、时间衰减、访问频率等因素，
    智能决定哪些记忆应该被遗忘（降级到长期记忆）。
    """

    def __init__(self, forget_threshold: float = 0.1):
        """
        初始化遗忘策略

        Args:
            forget_threshold: 遗忘阈值，重要度低于此值的记忆将被遗忘
                             默认0.1，可通过环境变量配置
        """
        self.forget_threshold = forget_threshold

    # ==================== 重要度计算 ====================

    def calculate_importance(
        self,
        memory: MemoryItem,
        current_time: datetime
    ) -> float:
        """
        计算记忆的当前重要度

        公式: 重要度 = 初始重要度 × 时间衰减 × 访问频率加权

        Args:
            memory: 记忆条目
            current_time: 当前时间

        Returns:
            float: 当前重要度值 (0.0-∞，通常 < 3.0)

        示例:
            记忆A: importance=0.8, 2小时前, 访问3次
              时间衰减 = e^(-0.1 × 2) ≈ 0.82
              访问加权 = 1 + log(1 + 3) ≈ 2.39
              重要度 = 0.8 × 0.82 × 2.39 ≈ 1.57

            记忆B: importance=0.5, 10小时前, 访问0次
              时间衰减 = e^(-0.1 × 10) ≈ 0.37
              访问加权 = 1
              重要度 = 0.5 × 0.37 × 1 ≈ 0.19 → 应该遗忘
        """
        # 1. 计算时间差（小时）
        time_delta_seconds = (current_time - memory.timestamp).total_seconds()
        time_delta_hours = time_delta_seconds / 3600

        # 2. 时间衰减（指数衰减）
        # e^(-decay_rate × 时间差)
        time_decay = math.exp(-memory.decay_rate * time_delta_hours)

        # 3. 访问频率加权
        # 1 + log(1 + access_count)，常访问的记忆更重要
        access_weight = 1 + math.log(1 + memory.access_count)

        # 4. 综合重要度
        current_importance = memory.importance * time_decay * access_weight

        return current_importance

    # ==================== 遗忘决策 ====================

    def should_forget(
        self,
        memory: MemoryItem,
        current_time: datetime = None
    ) -> ForgetDecision:
        """
        判断记忆是否应该被遗忘

        Args:
            memory: 记忆条目
            current_time: 当前时间，默认为当前系统时间

        Returns:
            ForgetDecision: 遗忘决策结果
        """
        if current_time is None:
            current_time = get_utc_now()

        # 计算当前重要度
        current_importance = self.calculate_importance(memory, current_time)

        # 判断是否应该遗忘
        should_forget = current_importance < self.forget_threshold

        # 确定遗忘原因
        reason = self._get_forget_reason(memory, current_importance, current_time)

        return ForgetDecision(
            memory_id=memory.id,
            should_forget=should_forget,
            current_importance=current_importance,
            reason=reason
        )

    def _get_forget_reason(
        self,
        memory: MemoryItem,
        current_importance: float,
        current_time: datetime
    ) -> str:
        """
        分析遗忘原因

        Args:
            memory: 记忆条目
            current_importance: 当前重要度
            current_time: 当前时间

        Returns:
            str: 遗忘原因描述
        """
        if current_importance >= self.forget_threshold:
            return "保留（重要度足够）"

        # 分析具体原因
        time_delta_hours = (current_time - memory.timestamp).total_seconds() / 3600

        reasons = []

        # 初始重要度低
        if memory.importance < 0.3:
            reasons.append("初始重要度低")

        # 时间过长
        if time_delta_hours > 24:
            reasons.append(f"时间过长({time_delta_hours:.1f}小时)")

        # 访问频率低
        if memory.access_count == 0:
            reasons.append("从未被访问")

        return " + ".join(reasons) if reasons else "综合重要度低"

    # ==================== 批量处理 ====================

    def filter_memories(
        self,
        memories: List[MemoryItem],
        current_time: datetime = None
    ) -> Tuple[List[MemoryItem], List[MemoryItem]]:
        """
        批量筛选记忆，分为保留和遗忘两组

        Args:
            memories: 记忆列表
            current_time: 当前时间

        Returns:
            tuple: (应该保留的记忆列表, 应该遗忘的记忆列表)
        """
        if current_time is None:
            current_time = get_utc_now()

        to_keep = []
        to_forget = []

        for memory in memories:
            decision = self.should_forget(memory, current_time)

            # 更新metadata中的当前重要度
            memory.metadata['current_importance'] = decision.current_importance
            memory.metadata['forget_reason'] = decision.reason

            if decision.should_forget:
                to_forget.append(memory)
            else:
                to_keep.append(memory)

        return to_keep, to_forget

    # ==================== 摘要生成 ====================

    def compress_to_summary(
        self,
        memories: List[MemoryItem],
        mode: str = "simple"
    ) -> str:
        """
        将多条记忆压缩为摘要

        Args:
            memories: 待压缩的记忆列表
            mode: 压缩模式
                  - "simple": 简单规则提取（Phase 1）
                  - "llm": 使用LLM生成摘要（Phase 2，未实现）

        Returns:
            str: 摘要文本

        示例输出:
            - 用户想写一部玄幻小说...
            - 讨论了主角的人物设定...
            - 确定了故事背景为修仙世界...
        """
        if not memories:
            return ""

        if mode == "simple":
            return self._simple_compress(memories)
        elif mode == "llm":
            # TODO: Phase 2 - 集成LLM生成摘要
            return self._simple_compress(memories)
        else:
            raise ValueError(f"Unknown compression mode: {mode}")

    def _simple_compress(self, memories: List[MemoryItem]) -> str:
        """
        简单压缩：提取前50字作为摘要

        Args:
            memories: 记忆列表

        Returns:
            str: 摘要文本
        """
        summaries = []

        for memory in memories:
            # 提取前50字作为摘要
            content = memory.content.strip()
            if len(content) > 50:
                summary = content[:50] + "..."
            else:
                summary = content

            # 添加角色标记
            role_mark = {
                "user": "👤",
                "assistant": "🤖",
                "system": "⚙️",
                "tool": "🔧"
            }.get(memory.role, "")

            summaries.append(f"{role_mark} {summary}")

        return "\n".join(summaries)

    # ==================== 统计分析 ====================

    def analyze_importance_distribution(
        self,
        memories: List[MemoryItem],
        current_time: datetime = None
    ) -> Dict[str, Any]:
        """
        分析记忆重要度分布

        Args:
            memories: 记忆列表
            current_time: 当前时间

        Returns:
            Dict: 统计信息
        """
        if current_time is None:
            current_time = get_utc_now()

        if not memories:
            return {
                "total": 0,
                "avg_importance": 0,
                "should_forget_count": 0,
                "should_keep_count": 0
            }

        importances = [
            self.calculate_importance(memory, current_time)
            for memory in memories
        ]

        should_forget_count = sum(1 for imp in importances if imp < self.forget_threshold)

        return {
            "total": len(memories),
            "avg_importance": sum(importances) / len(importances),
            "min_importance": min(importances),
            "max_importance": max(importances),
            "should_forget_count": should_forget_count,
            "should_keep_count": len(memories) - should_forget_count,
            "forget_threshold": self.forget_threshold
        }
