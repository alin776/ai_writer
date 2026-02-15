"""
图书分析策略基类

定义了图书分析的策略接口和通用逻辑
"""

from abc import ABC, abstractmethod
from typing import Dict, List, Optional, Any
from dataclasses import dataclass
from enum import Enum


class DimensionType(str, Enum):
    """分析维度类型"""
    TECHNIQUE = "technique"  # 技巧 (知识库条目)
    CHARACTER_TEMPLATE = "character_template"  # 角色模板 (智能建议)
    POWER_SYSTEM = "power_system"  # 力量体系 (智能建议)
    SETTING = "setting"  # 设定 (智能建议)
    RELATIONSHIP = "relationship"  # 关系 (智能建议)
    PLOT_STRUCTURE = "plot_structure"  # 情节结构 (知识库条目)


@dataclass
class AnalysisDimension:
    """分析维度定义"""
    id: str  # 维度ID (如 core_selling_point)
    name: str  # 维度名称 (如 核心卖点)
    description: str  # 维度描述
    priority: int  # 优先级 (1-11)
    output_length: str  # 期望输出长度 (如 50-80字)
    dimension_type: DimensionType  # 维度类型
    tags: List[str]  # 标签
    sub_elements: Optional[List[Dict[str, str]]] = None  # 子元素定义

    def to_dict(self) -> Dict[str, Any]:
        """转换为字典"""
        result = {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "priority": self.priority,
            "output_length": self.output_length,
            "dimension_type": self.dimension_type.value,
            "tags": self.tags,
        }
        if self.sub_elements:
            result["sub_elements"] = self.sub_elements
        return result


class BookAnalysisStrategy(ABC):
    """
    图书分析策略抽象基类

    所有分析策略必须继承此类并实现抽象方法
    """

    @property
    @abstractmethod
    def strategy_id(self) -> str:
        """策略唯一标识"""
        pass

    @property
    @abstractmethod
    def strategy_name(self) -> str:
        """策略名称"""
        pass

    @property
    @abstractmethod
    def description(self) -> str:
        """策略描述"""
        pass

    @abstractmethod
    def get_dimensions(self) -> List[AnalysisDimension]:
        """
        获取分析维度列表

        Returns:
            分析维度列表
        """
        pass

    @abstractmethod
    def build_system_prompt(self) -> str:
        """
        构建系统提示词

        Returns:
            系统提示词内容
        """
        pass

    @abstractmethod
    def build_user_prompt(
        self,
        content: str,
        existing_settings: Optional[Dict[str, Any]] = None,
        is_incremental: bool = False,
        chapter_num: Optional[int] = None
    ) -> str:
        """
        构建用户提示词

        Args:
            content: 待分析的文本内容
            existing_settings: 已有的设定 (增量分析时使用)
            is_incremental: 是否为增量分析
            chapter_num: 当前章节号 (增量分析时使用)

        Returns:
            用户提示词内容
        """
        pass

    @abstractmethod
    def parse_ai_response(self, response: str) -> Dict[str, Any]:
        """
        解析AI返回结果

        Args:
            response: AI返回的原始文本

        Returns:
            解析后的结构化数据
        """
        pass

    def validate_result(self, result: Dict[str, Any]) -> bool:
        """
        验证分析结果是否完整

        Args:
            result: 分析结果

        Returns:
            是否有效
        """
        dimensions = self.get_dimensions()
        required_ids = {dim.id for dim in dimensions}
        result_ids = set(result.keys())

        # 检查是否包含所有必需的维度
        missing = required_ids - result_ids
        if missing:
            print(f"警告: 分析结果缺少维度: {missing}")
            return False

        return True

    def get_dimension_by_id(self, dimension_id: str) -> Optional[AnalysisDimension]:
        """
        根据ID获取维度定义

        Args:
            dimension_id: 维度ID

        Returns:
            维度定义,如果不存在则返回None
        """
        for dim in self.get_dimensions():
            if dim.id == dimension_id:
                return dim
        return None


class StrategyRegistry:
    """
    策略注册器

    管理所有可用的分析策略
    """

    def __init__(self):
        self._strategies: Dict[str, BookAnalysisStrategy] = {}

    def register(self, strategy: BookAnalysisStrategy) -> None:
        """
        注册策略

        Args:
            strategy: 策略实例
        """
        self._strategies[strategy.strategy_id] = strategy
        print(f"已注册策略: {strategy.strategy_id} - {strategy.strategy_name}")

    def get(self, strategy_id: str) -> Optional[BookAnalysisStrategy]:
        """
        获取策略

        Args:
            strategy_id: 策略ID

        Returns:
            策略实例,如果不存在则返回None
        """
        return self._strategies.get(strategy_id)

    def list_strategies(self) -> List[Dict[str, str]]:
        """
        列出所有策略

        Returns:
            策略列表 [{id, name, description}]
        """
        return [
            {
                "id": strategy.strategy_id,
                "name": strategy.strategy_name,
                "description": strategy.description,
            }
            for strategy in self._strategies.values()
        ]


# 全局策略注册器实例
strategy_registry = StrategyRegistry()
