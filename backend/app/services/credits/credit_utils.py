"""积分计算工具函数"""

from decimal import Decimal
from app.core.config import settings


def calculate_credits_from_cost(cost_usd: float) -> Decimal:
    """
    将美元成本转换为积分

    Args:
        cost_usd: 美元成本

    Returns:
        Decimal: 积分数量（两��小数）
    """
    credits = Decimal(str(cost_usd)) * Decimal(str(settings.CREDITS_PER_DOLLAR))
    return credits.quantize(Decimal("0.01"))


def calculate_credits_for_ai_call(
    model_name: str,
    prompt_tokens: int,
    completion_tokens: int
) -> Decimal:
    """
    计算 AI 调用消耗的积分

    Args:
        model_name: 模型名称
        prompt_tokens: 输入 token 数
        completion_tokens: 输出 token 数

    Returns:
        Decimal: 消耗积分
    """
    # 导入 CostCalculator (延迟导入避免循环依赖)
    from app.utils.cost_calculator import CostCalculator

    cost_data = CostCalculator.calculate_cost(
        model_name=model_name,
        prompt_tokens=prompt_tokens,
        completion_tokens=completion_tokens
    )
    return calculate_credits_from_cost(cost_data["total_cost"])
