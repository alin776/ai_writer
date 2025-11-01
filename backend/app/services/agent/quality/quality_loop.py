"""
质量循环管理器

实现 生成 → 评估 → 改进 → 重试 的质量循环机制
"""

import logging
from typing import Callable, Dict, Any, Optional, List
from app.services.agent.quality.quality_types import (
    QualityEvaluation,
    EvaluationContext
)
from app.services.agent.quality.quality_evaluator import QualityEvaluatorService

logger = logging.getLogger(__name__)


class QualityLoopResult:
    """质量循环结果"""

    def __init__(
        self,
        content: str,
        evaluation: QualityEvaluation,
        iterations: int,
        iteration_history: List[Dict[str, Any]]
    ):
        self.content = content
        self.evaluation = evaluation
        self.iterations = iterations
        self.iteration_history = iteration_history

    @property
    def overall_score(self) -> float:
        """总分"""
        return self.evaluation.overall_score

    @property
    def passes(self) -> bool:
        """是否通过"""
        return self.evaluation.passes

    def to_dict(self) -> Dict[str, Any]:
        """转换为字典"""
        return {
            "content": self.content,
            "evaluation": self.evaluation.dict(),
            "iterations": self.iterations,
            "iteration_history": self.iteration_history
        }


class QualityLoopManager:
    """质量循环管理器"""

    def __init__(self, evaluator: QualityEvaluatorService):
        """
        初始化质量循环管理器

        Args:
            evaluator: 质量评估服务
        """
        self.evaluator = evaluator
        self.max_iterations = 3  # 默认最大迭代次数
        self.target_score = 8.0  # 目标分数

    async def run_quality_loop(
        self,
        generator: Callable,
        generator_kwargs: Dict[str, Any],
        context: EvaluationContext,
        max_iterations: Optional[int] = None,
        target_score: Optional[float] = None
    ) -> QualityLoopResult:
        """
        运行质量循环

        流程:
        1. 调用generator生成内容
        2. 评估内容质量
        3. 如果分数 >= target_score 或达到最大迭代次数,返回最佳结果
        4. 否则根据评估反馈优化参数,重新生成

        Args:
            generator: 内容生成函数 (async callable)
            generator_kwargs: 生成函数的参数
            context: 评估上下文
            max_iterations: 最大迭代次数
            target_score: 目标分数

        Returns:
            QualityLoopResult: 包含最终内容、评估结果、迭代历史
        """
        max_iter = max_iterations or self.max_iterations
        target = target_score or self.target_score

        logger.info(f"开始质量循环,最大迭代:{max_iter}, 目标分数:{target}")

        iteration_history = []
        best_content = None
        best_evaluation = None
        best_score = 0.0

        for iteration in range(max_iter):
            logger.info(f"质量循环第 {iteration + 1}/{max_iter} 次迭代")

            try:
                # 1. 生成内容
                content = await self._call_generator(generator, generator_kwargs)

                if not content:
                    logger.warning(f"第{iteration+1}次生成内容为空,跳过")
                    continue

                # 2. 评估内容
                evaluation = await self.evaluator.evaluate(content, context)

                # 3. 记录历史
                iteration_data = {
                    "iteration": iteration + 1,
                    "content_length": len(content),
                    "score": evaluation.overall_score,
                    "passes": evaluation.passes,
                    "feedback": evaluation.feedback,
                    "suggestions": evaluation.suggestions
                }
                iteration_history.append(iteration_data)

                logger.info(
                    f"第{iteration+1}次评估完成: "
                    f"分数={evaluation.overall_score:.1f}, "
                    f"通过={evaluation.passes}"
                )

                # 4. 更新最佳结果
                if evaluation.overall_score > best_score:
                    best_content = content
                    best_evaluation = evaluation
                    best_score = evaluation.overall_score
                    logger.info(f"更新最佳结果: 分数={best_score:.1f}")

                # 5. 如果达到目标分数,提前结束
                if evaluation.overall_score >= target:
                    logger.info(f"达到目标分数{target},提前结束循环")
                    break

                # 6. 如果不是最后一次迭代,优化参数
                if iteration < max_iter - 1:
                    generator_kwargs = self._optimize_params(
                        generator_kwargs,
                        evaluation
                    )
                    logger.debug("已优化生成参数,准备下一次迭代")

            except Exception as e:
                logger.error(f"第{iteration+1}次迭代失败: {e}", exc_info=True)
                iteration_history.append({
                    "iteration": iteration + 1,
                    "error": str(e)
                })
                continue

        # 返回最佳结果
        if best_content is None:
            logger.error("质量循环未能生成任何有效内容")
            raise RuntimeError("质量循环失败: 未能生成有效内容")

        logger.info(
            f"质量循环完成: "
            f"总迭代={len(iteration_history)}, "
            f"最佳分数={best_score:.1f}, "
            f"通过={best_evaluation.passes}"
        )

        return QualityLoopResult(
            content=best_content,
            evaluation=best_evaluation,
            iterations=len(iteration_history),
            iteration_history=iteration_history
        )

    async def _call_generator(
        self,
        generator: Callable,
        kwargs: Dict[str, Any]
    ) -> str:
        """
        调用生成器函数

        支持同步和异步生成器
        """
        import asyncio
        import inspect

        if inspect.iscoroutinefunction(generator):
            # 异步生成器
            result = await generator(**kwargs)
        else:
            # 同步生成器
            result = generator(**kwargs)

        return result if isinstance(result, str) else str(result)

    def _optimize_params(
        self,
        params: Dict[str, Any],
        evaluation: QualityEvaluation
    ) -> Dict[str, Any]:
        """
        根据评估结果优化生成参数

        优化策略:
        1. 在prompt中添加改进建议
        2. 调整temperature (质量低 -> 降低随机性)
        3. 调整max_tokens (内容过短 -> 增加token)
        """
        new_params = params.copy()

        # 策略1: 在prompt中添加改进建议
        if "prompt" in new_params and evaluation.suggestions:
            improvement_text = self._format_improvement_suggestions(
                evaluation.suggestions
            )
            new_params["prompt"] = f"{new_params['prompt']}\n\n{improvement_text}"
            logger.debug(f"已添加改进建议到prompt")

        # 策略2: 调整temperature
        if "temperature" in new_params:
            # 分数越低,temperature降低越多
            if evaluation.overall_score < 6.0:
                new_params["temperature"] = max(0.3, new_params["temperature"] * 0.6)
            elif evaluation.overall_score < 7.0:
                new_params["temperature"] = max(0.3, new_params["temperature"] * 0.8)
            logger.debug(f"调整temperature: {new_params['temperature']:.2f}")

        # 策略3: 调整max_tokens (如果内容过短)
        if "max_tokens" in new_params:
            content_length = evaluation.metadata.get("content_length", 0)
            target_length = evaluation.metadata.get("target_length", 2000)

            if content_length < target_length * 0.8:
                # 内容过短,增加max_tokens
                new_params["max_tokens"] = int(new_params["max_tokens"] * 1.2)
                logger.debug(f"调整max_tokens: {new_params['max_tokens']}")

        return new_params

    def _format_improvement_suggestions(self, suggestions: List[str]) -> str:
        """格式化改进建议"""
        if not suggestions:
            return ""

        formatted = "请重点改进以下方面:\n"
        for i, suggestion in enumerate(suggestions, 1):
            formatted += f"{i}. {suggestion}\n"

        return formatted.strip()


class SimpleQualityLoop:
    """简化版质量循环 (用于快速测试)"""

    def __init__(self, evaluator: QualityEvaluatorService):
        self.evaluator = evaluator

    async def run(
        self,
        content: str,
        context: EvaluationContext
    ) -> QualityEvaluation:
        """
        简单评估,不进行循环

        Args:
            content: 要评估的内容
            context: 评估上下文

        Returns:
            QualityEvaluation: 评估结果
        """
        return await self.evaluator.evaluate(content, context)
