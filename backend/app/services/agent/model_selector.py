"""
模型选择器 - Week 7

智能选择合适的模型以优化成本和质量平衡
参考: novel-ai-agent-Chinese 的模型分级策略

核心功能:
1. 根据任务复杂度自动选择模型
2. 成本估算和追踪
3. 模型性能监控
4. 降级和回退策略
"""

from enum import Enum
from typing import Optional, Dict, Any, List
from pydantic import BaseModel, Field, ConfigDict
import logging

logger = logging.getLogger(__name__)


# ==================== 任务复杂度定义 ====================

class TaskComplexity(str, Enum):
    """任务复杂度等级

    根据任务类型、上下文长度、质量要求等因素综合判断
    """
    SIMPLE = "simple"      # 简单任务: 评估、分类、简单问答
    MEDIUM = "medium"      # 中等任务: 润色、扩写、摘要
    COMPLEX = "complex"    # 复杂任务: 创作、规划、深度分析


class TaskType(str, Enum):
    """任务类型枚举"""
    # 简单任务
    QUALITY_EVALUATION = "quality_evaluation"    # 质量评估
    TEXT_CLASSIFICATION = "text_classification"  # 文本分类
    SIMPLE_QA = "simple_qa"                     # 简单问答
    KEYWORD_EXTRACTION = "keyword_extraction"    # 关键词提取

    # 中等任务
    TEXT_POLISH = "text_polish"                 # 文本润色
    TEXT_EXPANSION = "text_expansion"           # 文本扩写
    SUMMARIZATION = "summarization"             # 摘要生成
    TRANSLATION = "translation"                 # 翻译

    # 复杂任务
    CONTENT_CREATION = "content_creation"       # 内容创作
    STORY_PLANNING = "story_planning"           # 故事规划
    CHARACTER_DESIGN = "character_design"       # 角色设计
    WORLD_BUILDING = "world_building"           # 世界观构建
    DEEP_ANALYSIS = "deep_analysis"             # 深度分析


# ==================== 模型配置 ====================

class ModelTier(BaseModel):
    """模型层级配置

    定义不同层级模型的性能和成本特征
    """
    name: str = Field(..., description="模型名称")
    provider: str = Field(..., description="模型提供商 (openai/deepseek/qwen/gemini)")
    model_id: str = Field(..., description="模型ID")

    # 成本配置 (单位: USD per 1M tokens)
    cost_per_1m_input: float = Field(..., description="输入成本 (每百万token)")
    cost_per_1m_output: float = Field(..., description="输出成本 (每百万token)")

    # 性能配置
    max_tokens: int = Field(default=4096, description="最大token数")
    speed: str = Field(default="medium", description="速度等级 (fast/medium/slow)")
    quality_score: float = Field(default=7.0, ge=0, le=10, description="质量评分 (0-10)")

    # 适用场景
    recommended_for: List[TaskComplexity] = Field(
        default_factory=list,
        description="推荐使用的任务复杂度"
    )

    model_config = ConfigDict(json_schema_extra={
        "example": {
            "name": "DeepSeek Chat",
            "provider": "deepseek",
            "model_id": "deepseek-chat",
            "cost_per_1m_input": 0.14,
            "cost_per_1m_output": 0.28,
            "max_tokens": 4096,
            "speed": "fast",
            "quality_score": 7.5,
            "recommended_for": ["simple", "medium"]
        }
    })


# ==================== 预定义模型配置 ====================

# 参考价格 (单位: USD per 1M tokens)
# GPT-5.2 (当前使用):
# - gpt-5.2: 统一模型，用于所有任务
#
# 其他模型参考:
# - GPT-3.5 Turbo: $0.50 input / $1.50 output
# - GPT-4 Turbo: $10.00 input / $30.00 output
# - DeepSeek: $0.14 input / $0.28 output

# 注意: 当前统一使用 gpt-5.2 模型

MODEL_TIERS: Dict[TaskComplexity, ModelTier] = {
    # 简单任务
    TaskComplexity.SIMPLE: ModelTier(
        name="GPT-5.2",
        provider="openai",
        model_id="gpt-5.2",
        cost_per_1m_input=1.0,
        cost_per_1m_output=2.0,
        max_tokens=4096,
        speed="fast",
        quality_score=8.0,
        recommended_for=[TaskComplexity.SIMPLE]
    ),

    # 中等任务
    TaskComplexity.MEDIUM: ModelTier(
        name="GPT-5.2",
        provider="openai",
        model_id="gpt-5.2",
        cost_per_1m_input=1.0,
        cost_per_1m_output=2.0,
        max_tokens=8192,
        speed="fast",
        quality_score=8.0,
        recommended_for=[TaskComplexity.MEDIUM]
    ),

    # 复杂任务
    TaskComplexity.COMPLEX: ModelTier(
        name="GPT-5.2",
        provider="openai",
        model_id="gpt-5.2",
        cost_per_1m_input=1.0,
        cost_per_1m_output=2.0,
        max_tokens=8192,
        speed="medium",
        quality_score=9.0,
        recommended_for=[TaskComplexity.COMPLEX]
    )
}

# 备选模型配置 (统一使用 Gemini 系列，无需备选)
ALTERNATIVE_MODELS: Dict[str, ModelTier] = {}


# ==================== 任务类型到复杂度的映射 ====================

TASK_TYPE_TO_COMPLEXITY: Dict[TaskType, TaskComplexity] = {
    # 简单任务
    TaskType.QUALITY_EVALUATION: TaskComplexity.SIMPLE,
    TaskType.TEXT_CLASSIFICATION: TaskComplexity.SIMPLE,
    TaskType.SIMPLE_QA: TaskComplexity.SIMPLE,
    TaskType.KEYWORD_EXTRACTION: TaskComplexity.SIMPLE,

    # 中等任务
    TaskType.TEXT_POLISH: TaskComplexity.MEDIUM,
    TaskType.TEXT_EXPANSION: TaskComplexity.MEDIUM,
    TaskType.SUMMARIZATION: TaskComplexity.MEDIUM,
    TaskType.TRANSLATION: TaskComplexity.MEDIUM,

    # 复杂任务
    TaskType.CONTENT_CREATION: TaskComplexity.COMPLEX,
    TaskType.STORY_PLANNING: TaskComplexity.COMPLEX,
    TaskType.CHARACTER_DESIGN: TaskComplexity.COMPLEX,
    TaskType.WORLD_BUILDING: TaskComplexity.COMPLEX,
    TaskType.DEEP_ANALYSIS: TaskComplexity.COMPLEX
}


# ==================== 模型选择结果 ====================

class ModelSelectionResult(BaseModel):
    """模型选择结果"""
    model: ModelTier = Field(..., description="选中的模型")
    complexity: TaskComplexity = Field(..., description="任务复杂度")
    reason: str = Field(..., description="选择原因")
    estimated_cost: Optional[float] = Field(None, description="预估成本 (USD)")
    alternative_models: List[ModelTier] = Field(
        default_factory=list,
        description="备选模型列表"
    )


# ==================== 模型选择器 ====================

class ModelSelector:
    """智能模型选择器

    根据任务特征自动选择最合适的模型，优化成本和质量平衡

    使用示例:
    ```python
    selector = ModelSelector()

    # 方式1: 通过任务类型选择
    result = selector.select_model(task_type=TaskType.CONTENT_CREATION)

    # 方式2: 通过复杂度选择
    result = selector.select_model(complexity=TaskComplexity.SIMPLE)

    # 方式3: 自动判断复杂度
    result = selector.select_model(
        context_length=5000,
        quality_requirement="high"
    )

    print(f"选中模型: {result.model.name}")
    print(f"预估成本: ${result.estimated_cost:.4f}")
    ```
    """

    def __init__(
        self,
        enable_cost_optimization: bool = True,
        custom_model_tiers: Optional[Dict[TaskComplexity, ModelTier]] = None
    ):
        """初始化模型选择器

        Args:
            enable_cost_optimization: 是否启用成本优化 (默认True)
            custom_model_tiers: 自定义模型配置 (可选)
        """
        self.enable_cost_optimization = enable_cost_optimization
        self.model_tiers = custom_model_tiers or MODEL_TIERS
        logger.info(
            f"ModelSelector 初始化完成, "
            f"成本优化: {enable_cost_optimization}, "
            f"模型层级: {len(self.model_tiers)}"
        )

    def select_model(
        self,
        task_type: Optional[TaskType] = None,
        complexity: Optional[TaskComplexity] = None,
        context_length: Optional[int] = None,
        quality_requirement: Optional[str] = None,
        max_cost: Optional[float] = None,
        input_tokens: Optional[int] = None,
        output_tokens: Optional[int] = None
    ) -> ModelSelectionResult:
        """选择合适的模型

        Args:
            task_type: 任务类型 (可选, 优先级最高)
            complexity: 任务复杂度 (可选)
            context_length: 上下文长度 (可选, 用于自动判断复杂度)
            quality_requirement: 质量要求 (low/medium/high)
            max_cost: 最大成本限制 (USD)
            input_tokens: 预估输入token数 (用于成本计算)
            output_tokens: 预估输出token数 (用于成本计算)

        Returns:
            ModelSelectionResult: 模型选择结果
        """
        # 1. 确定任务复杂度
        determined_complexity = self._determine_complexity(
            task_type=task_type,
            complexity=complexity,
            context_length=context_length,
            quality_requirement=quality_requirement
        )

        logger.info(f"[ModelSelector] 任务复杂度: {determined_complexity.value}")

        # 2. 选择模型
        selected_model = self.model_tiers.get(determined_complexity)

        if not selected_model:
            logger.warning(
                f"未找到复杂度 {determined_complexity} 对应的模型, "
                f"使用默认模型"
            )
            selected_model = self.model_tiers[TaskComplexity.MEDIUM]

        # 3. 检查成本限制 (如果启用成本优化)
        if self.enable_cost_optimization and max_cost is not None:
            selected_model = self._apply_cost_constraint(
                selected_model,
                determined_complexity,
                max_cost,
                input_tokens,
                output_tokens
            )

        # 4. 估算成本
        estimated_cost = None
        if input_tokens and output_tokens:
            estimated_cost = self.estimate_cost(
                selected_model,
                input_tokens,
                output_tokens
            )

        # 5. 获取备选模型
        alternatives = self._get_alternative_models(
            determined_complexity,
            exclude_model=selected_model.model_id
        )

        # 6. 生成选择原因
        reason = self._generate_selection_reason(
            determined_complexity,
            selected_model,
            task_type,
            quality_requirement
        )

        return ModelSelectionResult(
            model=selected_model,
            complexity=determined_complexity,
            reason=reason,
            estimated_cost=estimated_cost,
            alternative_models=alternatives
        )

    def _determine_complexity(
        self,
        task_type: Optional[TaskType],
        complexity: Optional[TaskComplexity],
        context_length: Optional[int],
        quality_requirement: Optional[str]
    ) -> TaskComplexity:
        """确定任务复杂度

        优先级:
        1. 显式指定的 complexity
        2. task_type 映射
        3. 根据 context_length 和 quality_requirement 推断
        """
        # 优先级1: 显式指定
        if complexity:
            return complexity

        # 优先级2: 任务类型映射
        if task_type:
            return TASK_TYPE_TO_COMPLEXITY.get(
                task_type,
                TaskComplexity.MEDIUM  # 默认
            )

        # 优先级3: 根据上下文和质量要求推断
        if context_length or quality_requirement:
            return self._infer_complexity(context_length, quality_requirement)

        # 默认: 中等复杂度
        logger.warning("无法确定任务复杂度, 使用默认值: MEDIUM")
        return TaskComplexity.MEDIUM

    def _infer_complexity(
        self,
        context_length: Optional[int],
        quality_requirement: Optional[str]
    ) -> TaskComplexity:
        """根据上下文长度和质量要求推断复杂度"""
        # 质量要求优先
        if quality_requirement:
            quality_map = {
                "low": TaskComplexity.SIMPLE,
                "medium": TaskComplexity.MEDIUM,
                "high": TaskComplexity.COMPLEX
            }
            if quality_requirement.lower() in quality_map:
                return quality_map[quality_requirement.lower()]

        # 根据上下文长度判断
        if context_length:
            if context_length < 500:
                return TaskComplexity.SIMPLE
            elif context_length < 2000:
                return TaskComplexity.MEDIUM
            else:
                return TaskComplexity.COMPLEX

        return TaskComplexity.MEDIUM

    def _apply_cost_constraint(
        self,
        model: ModelTier,
        complexity: TaskComplexity,
        max_cost: float,
        input_tokens: Optional[int],
        output_tokens: Optional[int]
    ) -> ModelTier:
        """应用成本约束，如果超预算则降级模型"""
        if not input_tokens or not output_tokens:
            return model

        estimated_cost = self.estimate_cost(model, input_tokens, output_tokens)

        if estimated_cost <= max_cost:
            return model

        logger.warning(
            f"预估成本 ${estimated_cost:.4f} 超过预算 ${max_cost:.4f}, "
            f"尝试降级模型"
        )

        # 尝试降级到更便宜的模型
        if complexity == TaskComplexity.COMPLEX:
            downgrade_model = self.model_tiers.get(TaskComplexity.MEDIUM)
            if downgrade_model:
                downgrade_cost = self.estimate_cost(
                    downgrade_model,
                    input_tokens,
                    output_tokens
                )
                if downgrade_cost <= max_cost:
                    logger.info(f"降级到: {downgrade_model.name}")
                    return downgrade_model

        if complexity in [TaskComplexity.COMPLEX, TaskComplexity.MEDIUM]:
            downgrade_model = self.model_tiers.get(TaskComplexity.SIMPLE)
            if downgrade_model:
                downgrade_cost = self.estimate_cost(
                    downgrade_model,
                    input_tokens,
                    output_tokens
                )
                if downgrade_cost <= max_cost:
                    logger.info(f"降级到: {downgrade_model.name}")
                    return downgrade_model

        logger.warning("无法满足成本约束，使用原模型")
        return model

    def estimate_cost(
        self,
        model: ModelTier,
        input_tokens: int,
        output_tokens: int
    ) -> float:
        """估算成本 (USD)

        Args:
            model: 模型配置
            input_tokens: 输入token数
            output_tokens: 输出token数

        Returns:
            float: 预估成本 (USD)
        """
        input_cost = (input_tokens / 1_000_000) * model.cost_per_1m_input
        output_cost = (output_tokens / 1_000_000) * model.cost_per_1m_output
        total_cost = input_cost + output_cost

        logger.debug(
            f"成本估算: {model.name} - "
            f"输入 {input_tokens} tokens (${input_cost:.6f}) + "
            f"输出 {output_tokens} tokens (${output_cost:.6f}) = "
            f"${total_cost:.6f}"
        )

        return total_cost

    def _get_alternative_models(
        self,
        complexity: TaskComplexity,
        exclude_model: Optional[str] = None,
        max_alternatives: int = 3
    ) -> List[ModelTier]:
        """获取备选模型列表"""
        alternatives = []

        # 从 ALTERNATIVE_MODELS 中筛选适合的模型
        for model_id, model in ALTERNATIVE_MODELS.items():
            if model_id == exclude_model:
                continue

            if complexity in model.recommended_for:
                alternatives.append(model)

        # 按成本排序 (从低到高)
        alternatives.sort(
            key=lambda m: m.cost_per_1m_input + m.cost_per_1m_output
        )

        return alternatives[:max_alternatives]

    def _generate_selection_reason(
        self,
        complexity: TaskComplexity,
        model: ModelTier,
        task_type: Optional[TaskType],
        quality_requirement: Optional[str]
    ) -> str:
        """生成模型选择原因"""
        reasons = []

        reasons.append(f"任务复杂度为 {complexity.value}")

        if task_type:
            reasons.append(f"任务类型: {task_type.value}")

        if quality_requirement:
            reasons.append(f"质量要求: {quality_requirement}")

        reasons.append(
            f"选择 {model.name} (质量评分: {model.quality_score}/10, "
            f"成本: ${model.cost_per_1m_input}/${model.cost_per_1m_output} per 1M tokens)"
        )

        return "; ".join(reasons)

    def get_recommended_params(
        self,
        model: ModelTier,
        task_type: Optional[TaskType] = None
    ) -> Dict[str, Any]:
        """获取推荐的生成参数

        Args:
            model: 模型配置
            task_type: 任务类型

        Returns:
            Dict: 推荐参数 (temperature, max_tokens等)
        """
        # 基础参数
        params = {
            "model": model.model_id,
            "max_tokens": model.max_tokens
        }

        # 根据任务类型调整temperature
        if task_type in [
            TaskType.QUALITY_EVALUATION,
            TaskType.TEXT_CLASSIFICATION,
            TaskType.KEYWORD_EXTRACTION
        ]:
            # 评估类任务: 低temperature,提高稳定性
            params["temperature"] = 0.3
        elif task_type in [
            TaskType.CONTENT_CREATION,
            TaskType.STORY_PLANNING,
            TaskType.CHARACTER_DESIGN,
            TaskType.WORLD_BUILDING
        ]:
            # 创作类任务: 高temperature,提高创造性
            params["temperature"] = 0.8
        else:
            # 其他任务: 中等temperature
            params["temperature"] = 0.7

        return params


# ==================== 便捷函数 ====================

def select_model_for_task(
    task_type: TaskType,
    input_tokens: Optional[int] = None,
    output_tokens: Optional[int] = None,
    **kwargs
) -> ModelSelectionResult:
    """便捷函数: 为任务选择模型

    Args:
        task_type: 任务类型
        input_tokens: 预估输入token数
        output_tokens: 预估输出token数
        **kwargs: 其他参数传递给 ModelSelector.select_model()

    Returns:
        ModelSelectionResult: 模型选择结果
    """
    selector = ModelSelector()
    return selector.select_model(
        task_type=task_type,
        input_tokens=input_tokens,
        output_tokens=output_tokens,
        **kwargs
    )


# ==================== 导出 ====================

__all__ = [
    "TaskComplexity",
    "TaskType",
    "ModelTier",
    "ModelSelectionResult",
    "ModelSelector",
    "MODEL_TIERS",
    "ALTERNATIVE_MODELS",
    "select_model_for_task"
]
