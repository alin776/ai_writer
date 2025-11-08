"""
自适应Token预算 - 根据任务类型动态分配Token

根据不同的对话场景（创作、分析、问答、闲聊），智能调整各部分的Token预算比例，
提升Token利用效率和用户体验。

核心思想：
- 创作类任务：增加短期对话和长期记忆的比例，保持创作连贯性
- 分析类任务：增加系统提示和工具结果，提供更多指导和数据支持
- 问答类任务：平衡配置，适用于通用场景
- 闲聊类任务：大幅增加短期对话，保持对话流畅

设计原则：
- 所有比例总和必须为1.0
- 预留5%作为安全缓冲
- 向后兼容现有TokenBudget
"""

from enum import Enum
from dataclasses import dataclass
from typing import Dict, Optional
import logging

logger = logging.getLogger(__name__)


class TaskType(Enum):
    """
    任务类型枚举

    根据对话的主要目的分类，用于选择最优的Token预算分配策略
    """
    CREATIVE = "creative"       # 创作类：小说续写、文章创作、剧本编写
    ANALYTICAL = "analytical"   # 分析类：大纲分析、内容总结、质量评估
    QA = "qa"                   # 问答类：知识查询、设定询问、功能咨询
    CHAT = "chat"               # 闲聊类：日常对话、情感交流、轻松聊天


@dataclass
class AdaptiveBudget:
    """
    自适应Token预算管理器

    根据任务类型动态提供最优的Token预算分配方案。

    预算分类：
    - system_prompt: 系统提示词（角色设定、任务指导）
    - long_term_memory: 长期记忆（跨会话的重要信息）
    - summary: 摘要上下文（压缩的历史对话）
    - short_memory: 近期对话（最近的几轮交互）
    - tools: 工具结果（Agent工具调用的输出）
    - reserved: 预留缓冲（应对突发情况）

    使用示例：
    ```python
    budget_manager = AdaptiveBudget(total=8000)

    # 获取创作任务的预算配置
    creative_budget = budget_manager.get_budget(TaskType.CREATIVE)
    system_tokens = creative_budget.get_budget("system_prompt")  # 返回1200 (15%)
    ```
    """

    total: int = 8000  # 总Token预算（适配常见模型：GPT-3.5/4, Claude等）

    # 预算模板：为每种任务类型预定义最优的比例分配
    BUDGETS: Dict[TaskType, Dict[str, float]] = None

    def __post_init__(self):
        """初始化预算模板"""
        if self.BUDGETS is None:
            self.BUDGETS = {
                # 创作类任务：强调对话历史和记忆
                TaskType.CREATIVE: {
                    "system_prompt": 0.15,      # ↓ 减少系统提示（创作不需要太多指导）
                    "long_term_memory": 0.20,   # ↑ 增加长期记忆（角色、世界观设定）
                    "summary": 0.15,            # ↓ 减少摘要（创作更注重近期细节）
                    "short_memory": 0.40,       # ↑↑ 大幅增加短期对话（保持创作连贯）
                    "tools": 0.05,              # ↓↓ 减少工具（创作较少使用工具）
                    "reserved": 0.05            # 预留
                },

                # 分析类任务：强调系统指导和工具支持
                TaskType.ANALYTICAL: {
                    "system_prompt": 0.30,      # ↑↑ 大幅增加系统提示（提供分析指导）
                    "long_term_memory": 0.10,   # ↓ 减少长期记忆（分析主要看当前内容）
                    "summary": 0.20,            # 平衡摘要
                    "short_memory": 0.20,       # ↓ 减少短期对话（分析不需要太多历史）
                    "tools": 0.15,              # ↑ 增加工具结果（数据、报告等）
                    "reserved": 0.05            # 预留
                },

                # 问答类任务：平衡配置（默认选项）
                TaskType.QA: {
                    "system_prompt": 0.20,      # 标准系统提示
                    "long_term_memory": 0.15,   # 标准长期记忆
                    "summary": 0.25,            # 标准摘要
                    "short_memory": 0.30,       # 标准短期对话
                    "tools": 0.05,              # 标准工具
                    "reserved": 0.05            # 预留
                },

                # 闲聊类任务：强调对话流畅性
                TaskType.CHAT: {
                    "system_prompt": 0.10,      # ↓↓ 大幅减少系统提示（闲聊不需要太多指导）
                    "long_term_memory": 0.10,   # ↓ 减少长期记忆（闲聊主要关注当前）
                    "summary": 0.10,            # ↓↓ 大幅减少摘要（闲聊不需要太多历史）
                    "short_memory": 0.60,       # ↑↑↑ 最大化短期对话（保持对话自然流畅）
                    "tools": 0.05,              # ↓ 减少工具
                    "reserved": 0.05            # 预留
                }
            }

            # 验证所有预算配置的合法性
            self._validate_budgets()

    def _validate_budgets(self):
        """
        验证预算配置的合法性

        检查：
        1. 所有比例总和 = 1.0
        2. 所有比例 >= 0
        3. 所有类别都有定义
        """
        required_categories = {
            "system_prompt", "long_term_memory", "summary",
            "short_memory", "tools", "reserved"
        }

        for task_type, budget in self.BUDGETS.items():
            # 检查类别完整性
            if set(budget.keys()) != required_categories:
                raise ValueError(
                    f"预算配置 {task_type.value} 缺少必需的类别。"
                    f"需要: {required_categories}, 实际: {set(budget.keys())}"
                )

            # 检查总和
            total_ratio = sum(budget.values())
            if abs(total_ratio - 1.0) > 0.001:  # 允许浮点误差
                raise ValueError(
                    f"预算配置 {task_type.value} 的比例总和不等于1.0: {total_ratio}"
                )

            # 检查非负
            for category, ratio in budget.items():
                if ratio < 0:
                    raise ValueError(
                        f"预算配置 {task_type.value} 的类别 {category} 比例为负: {ratio}"
                    )

        logger.info("✅ 所有预算配置验证通过")

    def get_budget(
        self,
        task_type: TaskType,
        category: Optional[str] = None
    ) -> Dict[str, float]:
        """
        获取指定任务类型的预算配置

        Args:
            task_type: 任务类型（CREATIVE, ANALYTICAL, QA, CHAT）
            category: 可选，如果指定则返回该类别的Token数量而非比例

        Returns:
            如果category为None: 返回完整的比例配置字典
            如果category指定: 返回该类别的实际Token数量

        Examples:
            # 获取完整配置
            >>> budget = manager.get_budget(TaskType.CREATIVE)
            >>> budget
            {"system_prompt": 0.15, "long_term_memory": 0.20, ...}

            # 获取特定类别的Token数量
            >>> tokens = manager.get_budget(TaskType.CREATIVE, "system_prompt")
            >>> tokens
            1200  # 8000 * 0.15
        """
        # 获取预算配置，如果类型不存在则使用默认QA配置
        budget_ratios = self.BUDGETS.get(task_type, self.BUDGETS[TaskType.QA])

        # 如果指定了category，返回实际Token数量
        if category:
            if category not in budget_ratios:
                logger.warning(f"未知的预算类别: {category}，返回0")
                return 0
            return int(self.total * budget_ratios[category])

        # 否则返回完整的比例配置
        return budget_ratios

    def get_budget_breakdown(self, task_type: TaskType) -> Dict[str, int]:
        """
        获取指定任务类型的Token预算详细分解（实际Token数量）

        Args:
            task_type: 任务类型

        Returns:
            各类别的实际Token数量字典

        Example:
            >>> breakdown = manager.get_budget_breakdown(TaskType.CREATIVE)
            >>> breakdown
            {
                "system_prompt": 1200,
                "long_term_memory": 1600,
                "summary": 1200,
                "short_memory": 3200,
                "tools": 400,
                "reserved": 400
            }
        """
        ratios = self.get_budget(task_type)
        return {
            category: int(self.total * ratio)
            for category, ratio in ratios.items()
        }

    def compare_budgets(self) -> str:
        """
        生成所有任务类型的预算对比表格（用于分析和调试）

        Returns:
            格式化的对比表格字符串
        """
        lines = [
            "=" * 80,
            "自适应Token预算对比表",
            f"总预算: {self.total} tokens",
            "=" * 80,
            ""
        ]

        # 表头
        header = f"{'类别':<20} | {'创作':<10} | {'分析':<10} | {'问答':<10} | {'闲聊':<10}"
        lines.append(header)
        lines.append("-" * 80)

        # 数据行
        categories = [
            "system_prompt", "long_term_memory", "summary",
            "short_memory", "tools", "reserved"
        ]

        for category in categories:
            row = f"{category:<20} |"
            for task_type in TaskType:
                ratio = self.BUDGETS[task_type][category]
                tokens = int(self.total * ratio)
                row += f" {ratio:>5.1%} ({tokens:>4}) |"
            lines.append(row)

        lines.append("=" * 80)
        return "\n".join(lines)

    def to_token_budget(self, task_type: TaskType):
        """
        将自适应预算转换为标准TokenBudget对象（向后兼容）

        Args:
            task_type: 任务类型

        Returns:
            TokenBudget实例

        Note:
            这个方法用于与现有系统兼容，逐步迁移时使用
        """
        from app.services.context.models import TokenBudget

        ratios = self.get_budget(task_type)

        return TokenBudget(
            total=self.total,
            system_prompt=ratios["system_prompt"],
            summary=ratios["summary"],
            short_memory=ratios["short_memory"],
            tools=ratios["tools"],
            reserved=ratios["reserved"]
        )

    @classmethod
    def from_custom_ratios(
        cls,
        total: int,
        custom_ratios: Dict[str, float]
    ) -> 'AdaptiveBudget':
        """
        从自定义比例创建AdaptiveBudget（高级用法）

        Args:
            total: 总Token预算
            custom_ratios: 自定义比例字典

        Returns:
            AdaptiveBudget实例

        Example:
            >>> custom = {
            ...     "system_prompt": 0.25,
            ...     "long_term_memory": 0.20,
            ...     "summary": 0.20,
            ...     "short_memory": 0.25,
            ...     "tools": 0.05,
            ...     "reserved": 0.05
            ... }
            >>> budget = AdaptiveBudget.from_custom_ratios(8000, custom)
        """
        instance = cls(total=total)

        # 添加自定义配置作为新的任务类型
        # 这里使用QA作为基础，然后覆盖
        instance.BUDGETS[TaskType.QA] = custom_ratios

        # 验证自定义配置
        instance._validate_budgets()

        return instance


# 全局单例（可选）
_default_adaptive_budget: Optional[AdaptiveBudget] = None


def get_adaptive_budget(total: int = 8000) -> AdaptiveBudget:
    """
    获取全局默认的AdaptiveBudget实例（单例模式）

    Args:
        total: Token总预算

    Returns:
        AdaptiveBudget实例
    """
    global _default_adaptive_budget
    if _default_adaptive_budget is None or _default_adaptive_budget.total != total:
        _default_adaptive_budget = AdaptiveBudget(total=total)
    return _default_adaptive_budget
