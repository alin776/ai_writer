"""
质量评估服务

提供内容质量的多维度评估功能
"""

import re
import logging
from typing import List, Optional, Dict, Any
from app.services.agent.quality.quality_types import (
    QualityDimension,
    DimensionScore,
    QualityEvaluation,
    EvaluationContext,
    DIMENSION_WEIGHTS
)
from app.services.agent.prompts.quality_prompts import QualityPrompts

logger = logging.getLogger(__name__)


class QualityEvaluatorService:
    """质量评估服务"""

    def __init__(self, ai_service):
        """
        初始化质量评估服务

        Args:
            ai_service: AI服务实例 (HTTPAIService)
        """
        self.ai_service = ai_service
        self.prompts = QualityPrompts()

    async def evaluate(
        self,
        content: str,
        context: EvaluationContext,
        dimensions: Optional[List[QualityDimension]] = None,
        parallel: bool = True
    ) -> QualityEvaluation:
        """
        评估内容质量

        Args:
            content: 要评估的内容
            context: 评估上下文
            dimensions: 要评估的维度列表,None表示评估所有维度
            parallel: 是否并行评估多个维度(默认True)

        Returns:
            QualityEvaluation: 评估结果
        """
        if dimensions is None:
            dimensions = list(QualityDimension)

        logger.info(f"开始质量评估,内容长度: {len(content)}, 评估维度: {[d.value for d in dimensions]}, 并行: {parallel}")

        # 评估各个维度
        if parallel:
            # 并行评估(使用asyncio.gather)
            import asyncio
            tasks = [
                self._evaluate_dimension_safe(content, dimension, context)
                for dimension in dimensions
            ]
            dimension_scores = await asyncio.gather(*tasks)
        else:
            # 串行评估
            dimension_scores = []
            for dimension in dimensions:
                try:
                    score = await self._evaluate_dimension(content, dimension, context)
                    dimension_scores.append(score)
                    logger.debug(f"维度 {dimension.value} 评分: {score.score}")
                except Exception as e:
                    logger.error(f"评估维度 {dimension.value} 失败: {e}")
                    # 失败时给中等分数
                    dimension_scores.append(DimensionScore(
                        dimension=dimension,
                        score=5.0,
                        feedback=f"评估失败: {str(e)}",
                        weight=DIMENSION_WEIGHTS[dimension]
                    ))

        # 计算加权总分
        overall_score = self._calculate_overall_score(dimension_scores)

        # 生成综合反馈
        feedback = self._generate_feedback(dimension_scores, overall_score)

        # 生成改进建议
        suggestions = self._generate_suggestions(dimension_scores)

        evaluation = QualityEvaluation(
            overall_score=overall_score,
            dimension_scores=dimension_scores,
            passes=overall_score >= 8.0,
            feedback=feedback,
            suggestions=suggestions,
            metadata={
                "content_length": len(content),
                "target_length": context.target_length,
                "evaluated_dimensions": [d.value for d in dimensions],
                "parallel_evaluation": parallel
            }
        )

        logger.info(f"质量评估完成,总分: {overall_score:.1f}, 通过: {evaluation.passes}")
        return evaluation

    async def _evaluate_dimension_safe(
        self,
        content: str,
        dimension: QualityDimension,
        context: EvaluationContext
    ) -> DimensionScore:
        """
        安全地评估单个维度(带异常处理)

        用于并行评估时避免单个维度失败导致整体失败
        """
        try:
            return await self._evaluate_dimension(content, dimension, context)
        except Exception as e:
            logger.error(f"评估维度 {dimension.value} 失败: {e}")
            return DimensionScore(
                dimension=dimension,
                score=5.0,
                feedback=f"评估失败: {str(e)}",
                weight=DIMENSION_WEIGHTS[dimension]
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
        try:
            response = await self._call_llm_for_evaluation(prompt)
            score, feedback = self._parse_llm_response(response, dimension)
        except Exception as e:
            logger.error(f"LLM调用失败: {e}")
            score, feedback = 5.0, f"评估失败: {str(e)}"

        return DimensionScore(
            dimension=dimension,
            score=score,
            feedback=feedback,
            weight=DIMENSION_WEIGHTS[dimension]
        )

    def _evaluate_length(self, content: str, target_length: int) -> DimensionScore:
        """
        评估字数是否符合要求

        评分逻辑:
        - 90%-110% = 10分
        - 80%-120% = 8分
        - 其他按比例递减
        """
        actual_length = len(content)
        ratio = actual_length / target_length if target_length > 0 else 0

        if 0.9 <= ratio <= 1.1:
            score = 10.0
            feedback = f"字数{actual_length}字,符合目标{target_length}字"
        elif 0.8 <= ratio <= 1.2:
            score = 8.0
            feedback = f"字数{actual_length}字,基本符合目标{target_length}字"
        elif ratio < 0.8:
            score = max(0, 8.0 - (0.8 - ratio) * 20)
            feedback = f"字数{actual_length}字,少于目标{target_length}字 ({ratio*100:.0f}%)"
        else:
            score = max(0, 8.0 - (ratio - 1.2) * 10)
            feedback = f"字数{actual_length}字,超过目标{target_length}字 ({ratio*100:.0f}%)"

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
                context.previous_content
            )

        elif dimension == QualityDimension.STYLE_CONSISTENCY:
            return self.prompts.get_style_prompt(
                content,
                context.writing_style
            )

        elif dimension == QualityDimension.GRAMMAR:
            return self.prompts.get_grammar_prompt(content)

        else:
            raise ValueError(f"Unknown dimension: {dimension}")

    async def _call_llm_for_evaluation(self, prompt: str) -> str:
        """
        调用LLM进行评估

        使用HTTPAIService的流式聊天接口
        使用低温度(0.1)保证评估稳定性
        """
        try:
            messages = [{"role": "user", "content": prompt}]

            # 收集完整响应
            full_response = ""

            # 使用HTTPAIService的_stream_chat方法
            async for chunk, usage in self.ai_service._stream_chat(
                messages=messages,
                max_tokens=350,  # 增加token数量避免反馈截断(从200→350)
                temperature=0.1  # 低温度保证稳定性和一致性
            ):
                full_response += chunk

            logger.debug(f"LLM评估响应: {full_response[:100]}...")
            return full_response

        except Exception as e:
            logger.error(f"调用LLM失败: {e}", exc_info=True)
            # 返回默认响应而不是抛出异常,提高容错性
            return "分数: 7.0\n理由: 评估服务暂时不可用,给出默认评分"

    def _parse_llm_response(self, response: str, dimension: QualityDimension) -> tuple:
        """
        解析LLM返回的评分和反馈

        Returns:
            (score, feedback): 评分和反馈文本
        """
        # 提取分数 (匹配 "分数: 8" 或 "分数:8" 或 "分数: 8.5" 等格式)
        score_match = re.search(r'分数\s*[:：]\s*(\d+(?:\.\d+)?)', response)
        score = float(score_match.group(1)) if score_match else 7.0

        # 提取理由或问题列表
        if dimension == QualityDimension.GRAMMAR:
            # 语法维度提取问题列表
            problems_match = re.search(r'问题列表\s*[:：]\s*(.+)', response, re.DOTALL)
            feedback = problems_match.group(1).strip() if problems_match else response
        else:
            # 其他维度提取理由
            feedback_match = re.search(r'理由\s*[:：]\s*(.+)', response, re.DOTALL)
            feedback = feedback_match.group(1).strip() if feedback_match else response

        # 限制分数范围
        score = max(0.0, min(10.0, score))

        # 截断过长的反馈
        if len(feedback) > 300:
            feedback = feedback[:297] + "..."

        return score, feedback

    def _calculate_overall_score(self, dimension_scores: List[DimensionScore]) -> float:
        """
        计算加权总分

        加权公式: overall = Σ(score_i * weight_i) / Σ(weight_i)
        """
        total_score = 0.0
        total_weight = 0.0

        for ds in dimension_scores:
            total_score += ds.score * ds.weight
            total_weight += ds.weight

        return round(total_score / total_weight, 2) if total_weight > 0 else 0.0

    def _generate_feedback(
        self,
        dimension_scores: List[DimensionScore],
        overall_score: float
    ) -> str:
        """生成综合反馈"""
        # 根据总分确定等级
        if overall_score >= 9.0:
            level = "优秀"
        elif overall_score >= 8.0:
            level = "良好"
        elif overall_score >= 7.0:
            level = "中等"
        elif overall_score >= 6.0:
            level = "及格"
        else:
            level = "需要改进"

        feedback = f"总体质量{level}(评分{overall_score:.1f}/10)。"

        # 找出得分最低的维度
        if dimension_scores:
            worst_dimension = min(dimension_scores, key=lambda x: x.score)

            if worst_dimension.score < 7.0:
                dim_name = self._get_dimension_name_cn(worst_dimension.dimension)
                feedback += f"主要问题在{dim_name}方面({worst_dimension.score:.1f}分): {worst_dimension.feedback[:50]}"
            elif overall_score >= 8.0:
                feedback += "各维度表现均衡,继续保持。"

        return feedback

    def _generate_suggestions(self, dimension_scores: List[DimensionScore]) -> List[str]:
        """生成改进建议"""
        suggestions = []

        # 按分数排序,优先改进得分最低的维度
        sorted_scores = sorted(dimension_scores, key=lambda x: x.score)

        for ds in sorted_scores:
            if ds.score < 8.0:
                suggestion = self._get_suggestion_for_dimension(ds)
                if suggestion:
                    suggestions.append(suggestion)

        # 最多返回3条建议
        return suggestions[:3]

    def _get_suggestion_for_dimension(self, dimension_score: DimensionScore) -> Optional[str]:
        """根据维度生成具体建议"""
        dimension = dimension_score.dimension
        score = dimension_score.score

        if dimension == QualityDimension.CONTENT_QUALITY:
            if score < 6.0:
                return "大幅增强情节冲突和爽点,加强人物刻画和场景描写"
            else:
                return "适当增加情节冲突,让内容更吸引人"

        elif dimension == QualityDimension.LENGTH_CHECK:
            return f"调整内容长度: {dimension_score.feedback}"

        elif dimension == QualityDimension.COHERENCE:
            if score < 6.0:
                return "重新检查与前文的衔接,确保情节发展合理且逻辑自洽"
            else:
                return "加强与前文的自然衔接,注意情节逻辑"

        elif dimension == QualityDimension.STYLE_CONSISTENCY:
            if score < 6.0:
                return "统一叙述语气和用词风格,保持整体氛围一致"
            else:
                return "微调写作风格,保持与前文一致"

        elif dimension == QualityDimension.GRAMMAR:
            return "仔细检查错别字和语法错误,确保表达准确"

        return None

    def _get_dimension_name_cn(self, dimension: QualityDimension) -> str:
        """获取维度的中文名称"""
        name_map = {
            QualityDimension.CONTENT_QUALITY: "内容质量",
            QualityDimension.LENGTH_CHECK: "字数",
            QualityDimension.COHERENCE: "连贯性",
            QualityDimension.STYLE_CONSISTENCY: "风格一致性",
            QualityDimension.GRAMMAR: "语法"
        }
        return name_map.get(dimension, dimension.value)
