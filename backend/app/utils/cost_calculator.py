"""
AI 成本计算工具

支持 5 分类 token 差异化定价：
  new_input / cache_read / cache_creation / output / reasoning
定价数据由调用方从 SystemConfigService 注入。
"""

from typing import Dict, Optional


# 硬编码兜底（无 DB 时 fallback）
_FALLBACK_PRICING = {
    "input": 1.0,
    "cached_input": 0.5,
    "output": 2.0,
    "reasoning": 2.0,
    "cache_creation": 1.0,
}


class CostCalculator:
    """AI 成本计算器（分类计费）"""

    @classmethod
    def calculate_cost(
        cls,
        model_name: str,
        prompt_tokens: int,
        completion_tokens: int,
        cache_read: int = 0,
        cache_creation: int = 0,
        reasoning: int = 0,
        model_pricing: Optional[Dict] = None,
    ) -> Dict[str, float]:
        """
        计算 AI 调用成本（5 分类计费）

        Args:
            model_name: 模型名称
            prompt_tokens: 总输入 token 数
            completion_tokens: 总输出 token 数
            cache_read: 缓存命中的输入 token
            cache_creation: 创建缓存的 token
            reasoning: 推理 token
            model_pricing: 从 SystemConfigService.get_model_pricing() 获取的定价字典

        Returns:
            Dict 包含 prompt_cost, completion_cost, total_cost
        """
        model_pricing = model_pricing or {}
        pricing = model_pricing.get(
            model_name,
            model_pricing.get("default", _FALLBACK_PRICING),
        )

        # 拆分 token 类别
        new_input = max(prompt_tokens - cache_read - cache_creation, 0)
        new_output = max(completion_tokens - reasoning, 0)

        # 分类计费
        prompt_cost = (new_input / 1_000_000) * pricing.get("input", 1.0)
        cache_read_cost = (cache_read / 1_000_000) * pricing.get("cached_input", 0.5)
        cache_create_cost = (cache_creation / 1_000_000) * pricing.get("cache_creation", 1.0)
        output_cost = (new_output / 1_000_000) * pricing.get("output", 2.0)
        reasoning_cost = (reasoning / 1_000_000) * pricing.get("reasoning", 2.0)

        total_cost = prompt_cost + cache_read_cost + cache_create_cost + output_cost + reasoning_cost

        return {
            "prompt_cost": prompt_cost + cache_read_cost + cache_create_cost,  # 兼容旧字段
            "completion_cost": output_cost + reasoning_cost,                    # 兼容旧字段
            "total_cost": total_cost,
        }
