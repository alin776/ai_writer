# Week 4-5: 质量循环机制实施计划

> **创建时间**: 2025-11-01
> **预计工期**: 7-10个工作日
> **目标**: 实现内容质量评估和质量循环机制,提升内容质量+15%

---

## 📊 项目背景

### 当前状态
- ✅ 阶段一已完成 (Memory系统、工具系统、版本管理)
- ✅ 基础设施已就绪
- 🎯 准备进入阶段二第一个任务

### 核心目标
1. **质量评估**: 实现多维度内容质量评估 (5个维度)
2. **质量循环**: 实现生成→评估→改进→重试的闭环
3. **质量提升**: 内容质量分数提升 +15%
4. **性能保证**: 质量循环总耗时 < 30s (3次迭代)

---

## 🎯 Week 4 详细任务 (Day 1-5)

### Day 1-2: 质量评估设计 📐

#### 任务1.1: 设计评估维度枚举
**文件**: `backend/app/services/agent/quality/quality_types.py`

```python
from enum import Enum
from typing import List, Optional, Dict
from pydantic import BaseModel, Field

class QualityDimension(Enum):
    """质量评估维度"""
    CONTENT_QUALITY = "content_quality"         # 内容质量 (权重30%)
    LENGTH_CHECK = "length_check"               # 字数检查 (权重15%)
    COHERENCE = "coherence"                     # 连贯性 (权重25%)
    STYLE_CONSISTENCY = "style_consistency"     # 风格一致性 (权重20%)
    GRAMMAR = "grammar"                         # 语法正确性 (权重10%)

# 维度权重配置
DIMENSION_WEIGHTS = {
    QualityDimension.CONTENT_QUALITY: 0.30,
    QualityDimension.LENGTH_CHECK: 0.15,
    QualityDimension.COHERENCE: 0.25,
    QualityDimension.STYLE_CONSISTENCY: 0.20,
    QualityDimension.GRAMMAR: 0.10
}
```

#### 任务1.2: 设计评分数据模型
**文件**: `backend/app/services/agent/quality/quality_types.py`

```python
class DimensionScore(BaseModel):
    """单个维度的评分"""
    dimension: QualityDimension
    score: float = Field(ge=0.0, le=10.0, description="评分 0-10")
    feedback: str = Field(description="具体反馈")
    weight: float = Field(ge=0.0, le=1.0, description="权重")

    class Config:
        use_enum_values = True

class QualityEvaluation(BaseModel):
    """完整的质量评估结果"""
    overall_score: float = Field(ge=0.0, le=10.0, description="加权总分")
    dimension_scores: List[DimensionScore] = Field(description="各维度评分")
    passes: bool = Field(description="是否通过 (>=8分)")
    feedback: str = Field(description="综合反馈")
    suggestions: List[str] = Field(default_factory=list, description="改进建议")
    metadata: Dict = Field(default_factory=dict, description="元数据")

    def get_score_by_dimension(self, dimension: QualityDimension) -> Optional[DimensionScore]:
        """获取指定维度的评分"""
        for ds in self.dimension_scores:
            if ds.dimension == dimension:
                return ds
        return None
```

#### 任务1.3: 设计评估上下文
**文件**: `backend/app/services/agent/quality/quality_types.py`

```python
class EvaluationContext(BaseModel):
    """评估上下文"""
    user_id: str
    novel_id: str
    chapter_id: str
    previous_content: Optional[str] = None  # 前文内容
    outline: Optional[str] = None           # 大纲
    character_settings: Optional[Dict] = None  # 人物设定
    writing_style: Optional[str] = None     # 写作风格
    target_length: int = 2000               # 目标字数
    genre: Optional[str] = None             # 题材类型
```

### Day 3-4: 质量评估Prompt设计 ✍️

#### 任务2.1: 创建Prompt模板文件
**文件**: `backend/app/services/agent/prompts/quality_prompts.py`

```python
# 内容质量评估Prompt
CONTENT_QUALITY_PROMPT = """你是一位专业的网文编辑,请评估以下内容的质量。

评估内容:
{content}

评估标准:
1. 情节是否吸引人 (是否有冲突、爽点、悬念)
2. 人物刻画是否生动 (对话、动作、心理描写)
3. 场景描写是否细腻 (环境、氛围营造)
4. 节奏是否合理 (不拖沓、不突兀)

请给出0-10分的评分,并说明理由。

输出格式:
分数: [0-10的数字]
理由: [具体的评价,100字以内]
"""

# 连贯性评估Prompt
COHERENCE_PROMPT = """你是一位专业的网文编辑,请评估内容的连贯性。

前文内容:
{previous_content}

当前内容:
{current_content}

评估标准:
1. 与前文是否自然衔接 (时间、地点、人物)
2. 情节发展是否合理 (逻辑自洽)
3. 人物行为是否符合设定 (性格一致)
4. 没有明显的断层或跳跃

请给出0-10分的评分,并说明理由。

输出格式:
分数: [0-10的数字]
理由: [具体的评价,100字以内]
"""

# 风格一致性评估Prompt
STYLE_CONSISTENCY_PROMPT = """你是一位专业的网文编辑,请评估写作风格的一致性。

参考风格:
{reference_style}

当前内容:
{content}

评估标准:
1. 叙述语气是否一致 (第一人称/第三人称)
2. 用词风格是否一致 (现代/古风/幽默等)
3. 句式长短是否协调
4. 整体氛围是否统一

请给出0-10分的评分,并说明理由。

输出格式:
分数: [0-10的数字]
理由: [具体的评价,100字以内]
"""

# 语法正确性评估Prompt
GRAMMAR_PROMPT = """你是一位专业的文字编辑,请检查以下内容的语法和错别字。

内容:
{content}

评估标准:
1. 没有错别字
2. 没有语法错误 (主谓宾、标点)
3. 没有逻辑矛盾
4. 表达清晰准确

请给出0-10分的评分,并列出发现的问题。

输出格式:
分数: [0-10的数字]
问题列表: [发现的问题,每个问题一行。如果没有问题,写"无"]
"""
```

#### 任务2.2: 创建Prompt工具类
**文件**: `backend/app/services/agent/prompts/quality_prompts.py`

```python
class QualityPrompts:
    """质量评估Prompt管理类"""

    @staticmethod
    def get_content_quality_prompt(content: str) -> str:
        return CONTENT_QUALITY_PROMPT.format(content=content)

    @staticmethod
    def get_coherence_prompt(current_content: str, previous_content: str) -> str:
        return COHERENCE_PROMPT.format(
            current_content=current_content,
            previous_content=previous_content[:1000]  # 只取前1000字避免token过多
        )

    @staticmethod
    def get_style_prompt(content: str, reference_style: str) -> str:
        return STYLE_CONSISTENCY_PROMPT.format(
            content=content,
            reference_style=reference_style
        )

    @staticmethod
    def get_grammar_prompt(content: str) -> str:
        return GRAMMAR_PROMPT.format(content=content)
```

### Day 5: 实现QualityEvaluatorService 🔧

#### 任务3.1: 创建评估服务核心类
**文件**: `backend/app/services/agent/quality/quality_evaluator.py`

```python
import re
from typing import List, Optional
from backend.app.services.agent.quality.quality_types import (
    QualityDimension, DimensionScore, QualityEvaluation,
    EvaluationContext, DIMENSION_WEIGHTS
)
from backend.app.services.agent.prompts.quality_prompts import QualityPrompts
from backend.app.services.http_ai_service import HTTPAIService

class QualityEvaluatorService:
    """质量评估服务"""

    def __init__(self, ai_service: HTTPAIService):
        self.ai_service = ai_service
        self.prompts = QualityPrompts()

    async def evaluate(
        self,
        content: str,
        context: EvaluationContext,
        dimensions: Optional[List[QualityDimension]] = None
    ) -> QualityEvaluation:
        """
        评估内容质量

        Args:
            content: 要评估的内容
            context: 评估上下文
            dimensions: 要评估的维度列表,None表示评估所有维度

        Returns:
            QualityEvaluation: 评估结果
        """
        if dimensions is None:
            dimensions = list(QualityDimension)

        # 并行评估各个维度
        dimension_scores = []
        for dimension in dimensions:
            score = await self._evaluate_dimension(content, dimension, context)
            dimension_scores.append(score)

        # 计算加权总分
        overall_score = self._calculate_overall_score(dimension_scores)

        # 生成综合反馈
        feedback = self._generate_feedback(dimension_scores, overall_score)

        # 生成改进建议
        suggestions = self._generate_suggestions(dimension_scores)

        return QualityEvaluation(
            overall_score=overall_score,
            dimension_scores=dimension_scores,
            passes=overall_score >= 8.0,
            feedback=feedback,
            suggestions=suggestions,
            metadata={
                "content_length": len(content),
                "target_length": context.target_length,
                "evaluated_dimensions": [d.value for d in dimensions]
            }
        )

    async def _evaluate_dimension(
        self,
        content: str,
        dimension: QualityDimension,
        context: EvaluationContext
    ) -> DimensionScore:
        """评估单个维度"""

        # 字数检查维度直接计算,不调用LLM
        if dimension == QualityDimension.LENGTH_CHECK:
            return self._evaluate_length(content, context.target_length)

        # 其他维度调用LLM评估
        prompt = self._get_dimension_prompt(dimension, content, context)

        # 调用LLM (使用低成本模型)
        response = await self.ai_service.call_llm(
            prompt=prompt,
            model="deepseek-chat",  # 使用低成本模型
            temperature=0.1,  # 低温度保证稳定性
            max_tokens=200
        )

        # 解析LLM返回的评分
        score, feedback = self._parse_llm_response(response)

        return DimensionScore(
            dimension=dimension,
            score=score,
            feedback=feedback,
            weight=DIMENSION_WEIGHTS[dimension]
        )

    def _evaluate_length(self, content: str, target_length: int) -> DimensionScore:
        """评估字数是否符合要求"""
        actual_length = len(content)
        ratio = actual_length / target_length if target_length > 0 else 0

        # 评分逻辑: 90%-110% = 10分, 80%-120% = 8分, 其他递减
        if 0.9 <= ratio <= 1.1:
            score = 10.0
            feedback = f"字数{actual_length}字,符合目标{target_length}字"
        elif 0.8 <= ratio <= 1.2:
            score = 8.0
            feedback = f"字数{actual_length}字,基本符合目标{target_length}字"
        elif ratio < 0.8:
            score = max(0, 8.0 - (0.8 - ratio) * 20)
            feedback = f"字数{actual_length}字,少于目标{target_length}字"
        else:
            score = max(0, 8.0 - (ratio - 1.2) * 10)
            feedback = f"字数{actual_length}字,超过目标{target_length}字"

        return DimensionScore(
            dimension=QualityDimension.LENGTH_CHECK,
            score=score,
            feedback=feedback,
            weight=DIMENSION_WEIGHTS[QualityDimension.LENGTH_CHECK]
        )

    def _get_dimension_prompt(
        self,
        dimension: QualityDimension,
        content: str,
        context: EvaluationContext
    ) -> str:
        """获取维度对应的评估Prompt"""
        if dimension == QualityDimension.CONTENT_QUALITY:
            return self.prompts.get_content_quality_prompt(content)
        elif dimension == QualityDimension.COHERENCE:
            return self.prompts.get_coherence_prompt(
                content,
                context.previous_content or ""
            )
        elif dimension == QualityDimension.STYLE_CONSISTENCY:
            return self.prompts.get_style_prompt(
                content,
                context.writing_style or "现代都市网文风格"
            )
        elif dimension == QualityDimension.GRAMMAR:
            return self.prompts.get_grammar_prompt(content)
        else:
            raise ValueError(f"Unknown dimension: {dimension}")

    def _parse_llm_response(self, response: str) -> tuple[float, str]:
        """解析LLM返回的评分和反馈"""
        # 提取分数 (匹配 "分数: 8" 或 "分数:8" 等格式)
        score_match = re.search(r'分数\s*[:：]\s*(\d+(?:\.\d+)?)', response)
        score = float(score_match.group(1)) if score_match else 5.0

        # 提取理由
        feedback_match = re.search(r'理由\s*[:：]\s*(.+)', response, re.DOTALL)
        feedback = feedback_match.group(1).strip() if feedback_match else response

        # 限制分数范围
        score = max(0.0, min(10.0, score))

        return score, feedback

    def _calculate_overall_score(self, dimension_scores: List[DimensionScore]) -> float:
        """计算加权总分"""
        total_score = 0.0
        total_weight = 0.0

        for ds in dimension_scores:
            total_score += ds.score * ds.weight
            total_weight += ds.weight

        return total_score / total_weight if total_weight > 0 else 0.0

    def _generate_feedback(
        self,
        dimension_scores: List[DimensionScore],
        overall_score: float
    ) -> str:
        """生成综合反馈"""
        if overall_score >= 9.0:
            level = "优秀"
        elif overall_score >= 8.0:
            level = "良好"
        elif overall_score >= 7.0:
            level = "中等"
        else:
            level = "需要改进"

        # 找出得分最低的维度
        worst_dimension = min(dimension_scores, key=lambda x: x.score)

        feedback = f"总体质量{level}(评分{overall_score:.1f}/10)。"
        if worst_dimension.score < 7.0:
            feedback += f"主要问题在{worst_dimension.dimension.value}方面({worst_dimension.score:.1f}分): {worst_dimension.feedback}"

        return feedback

    def _generate_suggestions(self, dimension_scores: List[DimensionScore]) -> List[str]:
        """生成改进建议"""
        suggestions = []

        for ds in dimension_scores:
            if ds.score < 8.0:
                # 根据维度给出具体建议
                if ds.dimension == QualityDimension.CONTENT_QUALITY:
                    suggestions.append("增加情节冲突和爽点,让内容更吸引人")
                elif ds.dimension == QualityDimension.LENGTH_CHECK:
                    suggestions.append(f"调整内容长度: {ds.feedback}")
                elif ds.dimension == QualityDimension.COHERENCE:
                    suggestions.append("加强与前文的衔接,确保情节发展合理")
                elif ds.dimension == QualityDimension.STYLE_CONSISTENCY:
                    suggestions.append("保持写作风格一致,统一叙述语气")
                elif ds.dimension == QualityDimension.GRAMMAR:
                    suggestions.append("检查错别字和语法错误")

        return suggestions
```

---

## 🎯 Week 5 详细任务 (Day 1-5)

### Day 1-3: 实现QualityLoopManager 🔄

#### 任务4.1: 创建质量循环管理器
**文件**: `backend/app/services/agent/quality/quality_loop.py`

```python
from typing import Callable, Dict, Any, Optional
from backend.app.services.agent.quality.quality_types import (
    QualityEvaluation, EvaluationContext
)
from backend.app.services.agent.quality.quality_evaluator import QualityEvaluatorService

class QualityLoopManager:
    """质量循环管理器"""

    def __init__(self, evaluator: QualityEvaluatorService):
        self.evaluator = evaluator
        self.max_iterations = 3
        self.target_score = 8.0

    async def run_quality_loop(
        self,
        generator: Callable,
        generator_kwargs: Dict[str, Any],
        context: EvaluationContext,
        max_iterations: Optional[int] = None
    ) -> Dict[str, Any]:
        """
        运行质量循环

        Args:
            generator: 内容生成函数
            generator_kwargs: 生成函数的参数
            context: 评估上下文
            max_iterations: 最大迭代次数

        Returns:
            包含最终内容、评估结果、迭代历史的字典
        """
        max_iter = max_iterations or self.max_iterations
        iteration_history = []

        best_content = None
        best_evaluation = None
        best_score = 0.0

        for iteration in range(max_iter):
            # 生成内容
            content = await generator(**generator_kwargs)

            # 评估内容
            evaluation = await self.evaluator.evaluate(content, context)

            # 记录历史
            iteration_history.append({
                "iteration": iteration + 1,
                "content": content,
                "evaluation": evaluation,
                "score": evaluation.overall_score
            })

            # 更新最佳结果
            if evaluation.overall_score > best_score:
                best_content = content
                best_evaluation = evaluation
                best_score = evaluation.overall_score

            # 如果达到目标分数,提前结束
            if evaluation.overall_score >= self.target_score:
                break

            # 如果不是最后一次迭代,优化参数
            if iteration < max_iter - 1:
                generator_kwargs = self._optimize_params(
                    generator_kwargs,
                    evaluation
                )

        return {
            "content": best_content,
            "evaluation": best_evaluation,
            "iterations": len(iteration_history),
            "iteration_history": iteration_history
        }

    def _optimize_params(
        self,
        params: Dict[str, Any],
        evaluation: QualityEvaluation
    ) -> Dict[str, Any]:
        """
        根据评估结果优化生成参数

        优化策略:
        1. 在prompt中添加改进建议
        2. 调整temperature (质量低->降低随机性)
        """
        new_params = params.copy()

        # 在prompt中添加改进建议
        if "prompt" in new_params and evaluation.suggestions:
            improvement_text = "\n".join([
                "请改进以下方面:",
                *[f"- {s}" for s in evaluation.suggestions]
            ])
            new_params["prompt"] = f"{new_params['prompt']}\n\n{improvement_text}"

        # 降低temperature提高稳定性
        if "temperature" in new_params:
            new_params["temperature"] = max(0.3, new_params["temperature"] * 0.8)

        return new_params
```

### Day 4-5: 集成测试和优化 ✅

#### 任务5.1: 创建测试文件
**文件**: `backend/tests/test_quality/test_quality_evaluator.py`

```python
import pytest
from backend.app.services.agent.quality.quality_evaluator import QualityEvaluatorService
from backend.app.services.agent.quality.quality_types import (
    QualityDimension, EvaluationContext
)

@pytest.fixture
def quality_evaluator(mock_ai_service):
    return QualityEvaluatorService(mock_ai_service)

@pytest.mark.asyncio
async def test_evaluate_length():
    """测试字数评估"""
    # TODO: 实现测试

@pytest.mark.asyncio
async def test_evaluate_content_quality():
    """测试内容质量评估"""
    # TODO: 实现测试

@pytest.mark.asyncio
async def test_full_evaluation():
    """测试完整评估流程"""
    # TODO: 实现测试
```

#### 任务5.2: 性能测试
**文件**: `backend/tests/test_quality/test_quality_performance.py`

```python
import pytest
import time

@pytest.mark.asyncio
async def test_evaluation_speed():
    """测试评估速度 (应该 < 10s)"""
    # TODO: 实现测试

@pytest.mark.asyncio
async def test_quality_loop_speed():
    """测试质量循环速度 (3次迭代应该 < 30s)"""
    # TODO: 实现测试
```

---

## 📊 验收标准

### 功能验收
- [ ] QualityEvaluatorService实现完成
- [ ] 支持5个维度评估
- [ ] QualityLoopManager实现完成
- [ ] 支持参数自动优化

### 性能验收
- [ ] 单次评估速度 < 10s
- [ ] 质量循环(3次)耗时 < 30s
- [ ] 评估准确率 > 80%

### 质量验收
- [ ] 所有单元测试通过
- [ ] 代码类型安全(Pydantic)
- [ ] 完整的文档注释

---

## 📦 交付物清单

### 核心代码
```
backend/app/services/agent/
├── quality/
│   ├── __init__.py
│   ├── quality_types.py (~150行)
│   ├── quality_evaluator.py (~300行)
│   └── quality_loop.py (~150行)
└── prompts/
    └── quality_prompts.py (~200行)
```

### 测试代码
```
backend/tests/test_quality/
├── conftest.py
├── test_quality_evaluator.py
├── test_quality_loop.py
└── test_quality_performance.py
```

### 文档
- Week4-5完成总结.md
- 质量评估API文档
- A/B测试报告

---

## 🎯 下一步行动

### 立即开始
1. 创建目录结构和文件
2. 实现quality_types.py数据模型
3. 实现quality_prompts.py评估Prompt

### 分阶段验证
- Day 2: 验证数据模型设计
- Day 4: 验证评估Prompt效果
- Day 5: 验证完整评估流程

---

## 📞 注意事项

1. **成本控制**: 评估时使用低成本模型(DeepSeek)
2. **性能优化**: 可以并行评估多个维度
3. **错误处理**: LLM调用失败时的降级策略
4. **缓存机制**: 相同内容不重复评估

---

**准备就绪,等待确认开始开发!** 🚀
