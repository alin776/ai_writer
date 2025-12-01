"""
AI 成本计算工具

根据不同模型的定价计算 Token 成本
"""

from typing import Dict, Tuple


class CostCalculator:
    """AI成本计算器"""

    # 模型定价 (单位: 美元/百万token)
    # 格式: {model_name: (input_price, output_price)}
    # 项目统一使用 Google Gemini 2.5 系列模型
    PRICING: Dict[str, Tuple[float, float]] = {
        # Google Gemini 2.5 系列（2025年官方定价）
        "gemini-2.5-pro": (1.25, 10.0),          # 复杂任务 - 输入$1.25, 输出$10.00/M
        "gemini-2.5-flash": (0.30, 2.50),        # 中等任务 - 输入$0.30, 输出$2.50/M
        "gemini-2.5-flash-lite": (0.10, 0.40),   # 简单任务 - 输入$0.10, 输出$0.40/M

        # 默认定价（未知模型）
        "default": (1.0, 2.0),
    }

    @classmethod
    def calculate_cost(
        cls,
        model_name: str,
        prompt_tokens: int,
        completion_tokens: int
    ) -> Dict[str, float]:
        """
        计算AI调用成本

        Args:
            model_name: 模型名称
            prompt_tokens: 输入token数
            completion_tokens: 输出token数

        Returns:
            Dict[str, float]: 包含 prompt_cost, completion_cost, total_cost
        """
        # 获取定价，如果模型不存在则使用默认定价
        pricing = cls.PRICING.get(model_name, cls.PRICING["default"])
        input_price, output_price = pricing

        # 计算成本（价格是每百万token的美元数）
        prompt_cost = (prompt_tokens / 1_000_000) * input_price
        completion_cost = (completion_tokens / 1_000_000) * output_price
        total_cost = prompt_cost + completion_cost

        return {
            "prompt_cost": prompt_cost,
            "completion_cost": completion_cost,
            "total_cost": total_cost
        }

    @classmethod
    def get_model_pricing(cls, model_name: str) -> Tuple[float, float]:
        """
        获取模型定价

        Args:
            model_name: 模型名称

        Returns:
            Tuple[float, float]: (输入价格, 输出价格) 每百万token的美元数
        """
        return cls.PRICING.get(model_name, cls.PRICING["default"])

    @classmethod
    def add_model_pricing(
        cls,
        model_name: str,
        input_price: float,
        output_price: float
    ) -> None:
        """
        添加新模型定价

        Args:
            model_name: 模型名称
            input_price: 输入价格（美元/百万token）
            output_price: 输出价格（美元/百万token）
        """
        cls.PRICING[model_name] = (input_price, output_price)
