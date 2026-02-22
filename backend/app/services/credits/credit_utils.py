"""积分计算工具函数"""

from decimal import Decimal
from typing import Optional

from app.core.config import settings


def calculate_credits_from_cost(
    cost_usd: float,
    credits_per_dollar: Optional[int] = None,
) -> Decimal:
    """
    将美元成本转换为积分

    Args:
        cost_usd: 美元成本
        credits_per_dollar: 美元兑积分比例（可选，默认用 settings 硬编码值）

    Returns:
        Decimal: 积分数量（两位小数）
    """
    rate = credits_per_dollar if credits_per_dollar is not None else settings.CREDITS_PER_DOLLAR
    credits = Decimal(str(cost_usd)) * Decimal(str(rate))
    return credits.quantize(Decimal("0.01"))
