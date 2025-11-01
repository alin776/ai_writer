"""
Week 7: ModelSelector 单元测试

测试模型选择器的核心功能
"""

import pytest
from app.services.agent.model_selector import (
    ModelSelector,
    TaskType,
    TaskComplexity,
    ModelTier,
    ModelSelectionResult,
    select_model_for_task,
    MODEL_TIERS
)


class TestModelSelector:
    """测试 ModelSelector 类"""

    def setup_method(self):
        """每个测试前初始化"""
        self.selector = ModelSelector(enable_cost_optimization=True)

    def test_init(self):
        """测试初始化"""
        assert self.selector.enable_cost_optimization is True
        assert self.selector.model_tiers == MODEL_TIERS
        assert len(self.selector.model_tiers) == 3  # SIMPLE, MEDIUM, COMPLEX

    def test_select_model_by_task_type_simple(self):
        """测试通过任务类型选择模型 - SIMPLE任务"""
        result = self.selector.select_model(
            task_type=TaskType.QUALITY_EVALUATION,
            input_tokens=1000,
            output_tokens=500
        )

        assert isinstance(result, ModelSelectionResult)
        assert result.complexity == TaskComplexity.SIMPLE
        assert result.model.model_id == "gemini-2.5-flash-lite"
        assert result.estimated_cost is not None
        assert result.estimated_cost > 0

    def test_select_model_by_task_type_medium(self):
        """测试通过任务类型选择模型 - MEDIUM任务"""
        result = self.selector.select_model(
            task_type=TaskType.TEXT_POLISH,
            input_tokens=1000,
            output_tokens=500
        )

        assert result.complexity == TaskComplexity.MEDIUM
        assert result.model.model_id == "gemini-2.5-flash"

    def test_select_model_by_task_type_complex(self):
        """测试通过任务类型选择模型 - COMPLEX任务"""
        result = self.selector.select_model(
            task_type=TaskType.CONTENT_CREATION,
            input_tokens=3000,
            output_tokens=2000
        )

        assert result.complexity == TaskComplexity.COMPLEX
        assert result.model.model_id == "gemini-2.5-pro"

    def test_select_model_by_explicit_complexity(self):
        """测试显式指定复杂度"""
        result = self.selector.select_model(
            complexity=TaskComplexity.MEDIUM,
            input_tokens=1000,
            output_tokens=500
        )

        assert result.complexity == TaskComplexity.MEDIUM
        assert result.model.model_id == "gemini-2.5-flash"

    def test_select_model_by_context_length(self):
        """测试根据上下文长度推断复杂度"""
        # 短上下文 -> SIMPLE
        result1 = self.selector.select_model(
            context_length=300,
            input_tokens=300,
            output_tokens=200
        )
        assert result1.complexity == TaskComplexity.SIMPLE

        # 中等上下文 -> MEDIUM
        result2 = self.selector.select_model(
            context_length=1000,
            input_tokens=1000,
            output_tokens=500
        )
        assert result2.complexity == TaskComplexity.MEDIUM

        # 长上下文 -> COMPLEX
        result3 = self.selector.select_model(
            context_length=3000,
            input_tokens=3000,
            output_tokens=2000
        )
        assert result3.complexity == TaskComplexity.COMPLEX

    def test_select_model_by_quality_requirement(self):
        """测试根据质量要求选择模型"""
        # 低质量要求 -> SIMPLE
        result1 = self.selector.select_model(
            quality_requirement="low",
            input_tokens=1000,
            output_tokens=500
        )
        assert result1.complexity == TaskComplexity.SIMPLE

        # 中等质量要求 -> MEDIUM
        result2 = self.selector.select_model(
            quality_requirement="medium",
            input_tokens=1000,
            output_tokens=500
        )
        assert result2.complexity == TaskComplexity.MEDIUM

        # 高质量要求 -> COMPLEX
        result3 = self.selector.select_model(
            quality_requirement="high",
            input_tokens=1000,
            output_tokens=500
        )
        assert result3.complexity == TaskComplexity.COMPLEX

    def test_cost_estimation(self):
        """测试成本估算"""
        result = self.selector.select_model(
            task_type=TaskType.QUALITY_EVALUATION,
            input_tokens=1000,
            output_tokens=500
        )

        # Gemini 2.5 Flash Lite: $0.03 input / $0.12 output per 1M tokens
        expected_cost = (1000 / 1_000_000) * 0.03 + (500 / 1_000_000) * 0.12
        assert abs(result.estimated_cost - expected_cost) < 0.000001

    def test_cost_constraint_downgrade(self):
        """测试成本约束自动降级"""
        # 设置很低的成本限制,应该触发降级
        result = self.selector.select_model(
            task_type=TaskType.CONTENT_CREATION,  # 默认COMPLEX
            input_tokens=3000,
            output_tokens=2000,
            max_cost=0.001  # 非常低的预算
        )

        # 应该降级到更便宜的模型
        assert result.model.model_id != "gemini-2.5-pro"
        # 可能降级到MEDIUM或SIMPLE
        assert result.model.model_id in ["gemini-2.5-flash", "gemini-2.5-flash-lite"]

    def test_estimate_cost_method(self):
        """测试 estimate_cost 方法"""
        model = MODEL_TIERS[TaskComplexity.SIMPLE]

        cost = self.selector.estimate_cost(
            model=model,
            input_tokens=1000,
            output_tokens=500
        )

        expected = (1000 / 1_000_000) * 0.03 + (500 / 1_000_000) * 0.12
        assert abs(cost - expected) < 0.000001

    def test_get_recommended_params_evaluation_task(self):
        """测试获取推荐参数 - 评估类任务"""
        model = MODEL_TIERS[TaskComplexity.SIMPLE]

        params = self.selector.get_recommended_params(
            model=model,
            task_type=TaskType.QUALITY_EVALUATION
        )

        assert params["model"] == "gemini-2.5-flash-lite"
        assert params["temperature"] == 0.3  # 评估类任务低温度
        assert params["max_tokens"] == 4096

    def test_get_recommended_params_creation_task(self):
        """测试获取推荐参数 - 创作类任务"""
        model = MODEL_TIERS[TaskComplexity.COMPLEX]

        params = self.selector.get_recommended_params(
            model=model,
            task_type=TaskType.CONTENT_CREATION
        )

        assert params["model"] == "gemini-2.5-pro"
        assert params["temperature"] == 0.8  # 创作类任务高温度
        assert params["max_tokens"] == 8192

    def test_select_model_default_behavior(self):
        """测试默认行为 (无任何参数)"""
        result = self.selector.select_model()

        # 应该使用默认的MEDIUM复杂度
        assert result.complexity == TaskComplexity.MEDIUM
        assert result.model.model_id == "gemini-2.5-flash"

    def test_selection_reason_generated(self):
        """测试选择原因生成"""
        result = self.selector.select_model(
            task_type=TaskType.CONTENT_CREATION,
            quality_requirement="high"
        )

        assert result.reason is not None
        assert len(result.reason) > 0
        assert "complex" in result.reason.lower()


class TestTaskTypeMapping:
    """测试任务类型映射"""

    def test_simple_task_types(self):
        """测试简单任务类型"""
        selector = ModelSelector()

        simple_tasks = [
            TaskType.QUALITY_EVALUATION,
            TaskType.TEXT_CLASSIFICATION,
            TaskType.SIMPLE_QA,
            TaskType.KEYWORD_EXTRACTION
        ]

        for task_type in simple_tasks:
            result = selector.select_model(task_type=task_type)
            assert result.complexity == TaskComplexity.SIMPLE

    def test_medium_task_types(self):
        """测试中等任务类型"""
        selector = ModelSelector()

        medium_tasks = [
            TaskType.TEXT_POLISH,
            TaskType.TEXT_EXPANSION,
            TaskType.SUMMARIZATION,
            TaskType.TRANSLATION
        ]

        for task_type in medium_tasks:
            result = selector.select_model(task_type=task_type)
            assert result.complexity == TaskComplexity.MEDIUM

    def test_complex_task_types(self):
        """测试复杂任务类型"""
        selector = ModelSelector()

        complex_tasks = [
            TaskType.CONTENT_CREATION,
            TaskType.STORY_PLANNING,
            TaskType.CHARACTER_DESIGN,
            TaskType.WORLD_BUILDING,
            TaskType.DEEP_ANALYSIS
        ]

        for task_type in complex_tasks:
            result = selector.select_model(task_type=task_type)
            assert result.complexity == TaskComplexity.COMPLEX


class TestConvenienceFunction:
    """测试便捷函数"""

    def test_select_model_for_task(self):
        """测试 select_model_for_task 便捷函数"""
        result = select_model_for_task(
            task_type=TaskType.TEXT_POLISH,
            input_tokens=1000,
            output_tokens=500
        )

        assert isinstance(result, ModelSelectionResult)
        assert result.complexity == TaskComplexity.MEDIUM
        assert result.estimated_cost is not None


class TestModelTiers:
    """测试模型配置"""

    def test_model_tiers_structure(self):
        """测试模型配置结构"""
        assert len(MODEL_TIERS) == 3

        # 检查每个层级都存在
        assert TaskComplexity.SIMPLE in MODEL_TIERS
        assert TaskComplexity.MEDIUM in MODEL_TIERS
        assert TaskComplexity.COMPLEX in MODEL_TIERS

    def test_model_tier_properties(self):
        """测试模型配置属性"""
        for complexity, model in MODEL_TIERS.items():
            assert isinstance(model, ModelTier)
            assert model.name is not None
            assert model.provider == "gemini"
            assert model.cost_per_1m_input > 0
            assert model.cost_per_1m_output > 0
            assert model.max_tokens > 0
            assert 0 <= model.quality_score <= 10

    def test_cost_progression(self):
        """测试成本递增规律"""
        simple_model = MODEL_TIERS[TaskComplexity.SIMPLE]
        medium_model = MODEL_TIERS[TaskComplexity.MEDIUM]
        complex_model = MODEL_TIERS[TaskComplexity.COMPLEX]

        # 成本应该递增
        assert simple_model.cost_per_1m_input < medium_model.cost_per_1m_input
        assert medium_model.cost_per_1m_input < complex_model.cost_per_1m_input

        assert simple_model.cost_per_1m_output < medium_model.cost_per_1m_output
        assert medium_model.cost_per_1m_output < complex_model.cost_per_1m_output

    def test_quality_progression(self):
        """测试质量评分递增"""
        simple_model = MODEL_TIERS[TaskComplexity.SIMPLE]
        medium_model = MODEL_TIERS[TaskComplexity.MEDIUM]
        complex_model = MODEL_TIERS[TaskComplexity.COMPLEX]

        # 质量应该递增
        assert simple_model.quality_score <= medium_model.quality_score
        assert medium_model.quality_score <= complex_model.quality_score


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
