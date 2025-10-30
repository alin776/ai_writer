"""
自我反思与优化模块 (Reflection)

这是Agentic AI的9大核心工作流模式之一

功能:
1. Agent自我评估生成质量
2. 发现问题并改进
3. 多次迭代直到达标
4. 学习优化策略

工作流:
生成 → 自我评估 → 判断是否达标 → 未达标则改进 → 再次评估

使用场景:
- 续写章节后自动检查质量
- 生成大纲后自动优化
- 创建角色后自动完善
"""

from typing import Dict, List, Optional, Any, Callable
from datetime import datetime
from pydantic import BaseModel
from enum import Enum


class ReflectionResult(BaseModel):
    """反思结果"""
    quality_score: float  # 0-100
    is_acceptable: bool  # 是否可接受
    issues: List[str] = []  # 发现的问题
    suggestions: List[str] = []  # 改进建议
    timestamp: str


class IterationRecord(BaseModel):
    """迭代记录"""
    iteration: int  # 第几次迭代
    content: Any  # 本次内容
    reflection: ReflectionResult  # 反思结果
    improvements_made: List[str] = []  # 做了哪些改进


class ReflectionAgent:
    """自我反思Agent"""

    def __init__(
        self,
        evaluator: Callable,
        improver: Callable,
        quality_threshold: float = 80.0,
        max_iterations: int = 3
    ):
        """
        初始化反思Agent

        Args:
            evaluator: 评估函数 (content) -> ReflectionResult
            improver: 改进函数 (content, issues, suggestions) -> improved_content
            quality_threshold: 质量阈值 (0-100)
            max_iterations: 最大迭代次数
        """
        self.evaluator = evaluator
        self.improver = improver
        self.quality_threshold = quality_threshold
        self.max_iterations = max_iterations

    async def reflect_and_improve(
        self,
        initial_content: Any,
        context: Dict[str, Any] = None
    ) -> Dict[str, Any]:
        """
        反思并改进内容

        Args:
            initial_content: 初始内容
            context: 上下文信息

        Returns:
            Dict: {
                "final_content": 最终内容,
                "iterations": 迭代记录列表,
                "quality_score": 最终质量分数,
                "improved": 是否经过改进
            }
        """
        context = context or {}
        iterations = []
        current_content = initial_content

        for i in range(1, self.max_iterations + 1):
            # 评估当前内容
            reflection = await self.evaluator(current_content, context)

            # 记录迭代
            iteration_record = IterationRecord(
                iteration=i,
                content=current_content,
                reflection=reflection
            )
            iterations.append(iteration_record)

            # 检查是否达标
            if reflection.is_acceptable:
                return {
                    "final_content": current_content,
                    "iterations": iterations,
                    "quality_score": reflection.quality_score,
                    "improved": i > 1,
                    "iteration_count": i
                }

            # 未达标，进行改进
            if i < self.max_iterations:
                improved_content = await self.improver(
                    current_content,
                    reflection.issues,
                    reflection.suggestions,
                    context
                )

                # 记录改进
                iteration_record.improvements_made = [
                    f"针对问题「{issue}」进行了改进"
                    for issue in reflection.issues
                ]

                current_content = improved_content

        # 达到最大迭代次数，返回最后一次结果
        last_reflection = iterations[-1].reflection
        return {
            "final_content": current_content,
            "iterations": iterations,
            "quality_score": last_reflection.quality_score,
            "improved": True,
            "iteration_count": self.max_iterations,
            "warning": "达到最大迭代次数，质量可能未达标"
        }


# ==================== 预定义的评估器 ====================

class TextQualityEvaluator:
    """文本质量评估器"""

    def __init__(self, ai_service: Any):
        """
        初始化评估器

        Args:
            ai_service: AI服务实例（用于调用LLM评估）
        """
        self.ai_service = ai_service

    async def evaluate_writing_quality(
        self,
        content: str,
        context: Dict[str, Any]
    ) -> ReflectionResult:
        """
        评估写作质量

        Args:
            content: 文本内容
            context: 上下文

        Returns:
            ReflectionResult: 评估结果
        """
        # 调用AI进行评估
        prompt = f"""请评估以下文本的质量（1-100分），并指出问题和改进建议。

文本内容:
{content}

请以JSON格式返回评估结果:
{{
    "score": 分数(0-100),
    "issues": ["问题1", "问题2"],
    "suggestions": ["建议1", "建议2"]
}}
"""

        # 这里应该调用AI服务，简化示例
        # response = await self.ai_service.chat(prompt)
        # evaluation = json.loads(response)

        # 示例响应
        evaluation = {
            "score": 75.0,
            "issues": ["情节发展过快", "人物描写不够细腻"],
            "suggestions": ["增加过渡情节", "加强人物内心描写"]
        }

        return ReflectionResult(
            quality_score=evaluation["score"],
            is_acceptable=evaluation["score"] >= 80.0,
            issues=evaluation["issues"],
            suggestions=evaluation["suggestions"],
            timestamp=datetime.now().isoformat()
        )

    async def evaluate_outline_quality(
        self,
        outline: List[Dict],
        context: Dict[str, Any]
    ) -> ReflectionResult:
        """
        评估大纲质量

        Args:
            outline: 大纲列表
            context: 上下文

        Returns:
            ReflectionResult: 评估结果
        """
        issues = []
        suggestions = []
        score = 100.0

        # 检查章节数量
        if len(outline) < 10:
            issues.append("章节数量过少")
            suggestions.append("建议增加到15-30章")
            score -= 10

        # 检查是否有章节标题
        missing_titles = [i for i, ch in enumerate(outline) if not ch.get("title")]
        if missing_titles:
            issues.append(f"{len(missing_titles)}个章节缺少标题")
            suggestions.append("为所有章节添加标题")
            score -= 15

        # 检查是否有章节简介
        missing_summary = [i for i, ch in enumerate(outline) if not ch.get("summary")]
        if len(missing_summary) > len(outline) * 0.5:
            issues.append("超过一半的章节缺少简介")
            suggestions.append("为主要章节添加情节简介")
            score -= 20

        return ReflectionResult(
            quality_score=max(score, 0),
            is_acceptable=score >= 80.0,
            issues=issues,
            suggestions=suggestions,
            timestamp=datetime.now().isoformat()
        )


class TextImprover:
    """文本改进器"""

    def __init__(self, ai_service: Any):
        """
        初始化改进器

        Args:
            ai_service: AI服务实例
        """
        self.ai_service = ai_service

    async def improve_writing(
        self,
        content: str,
        issues: List[str],
        suggestions: List[str],
        context: Dict[str, Any]
    ) -> str:
        """
        改进写作

        Args:
            content: 原始内容
            issues: 问题列表
            suggestions: 建议列表
            context: 上下文

        Returns:
            str: 改进后的内容
        """
        prompt = f"""请根据以下问题和建议，改进这段文本。

原文:
{content}

存在的问题:
{chr(10).join(f"- {issue}" for issue in issues)}

改进建议:
{chr(10).join(f"- {sug}" for sug in suggestions)}

请输出改进后的文本。
"""

        # 这里应该调用AI服务
        # improved = await self.ai_service.chat(prompt)

        # 示例
        improved = content + "\n\n[已根据建议进行改进]"

        return improved

    async def improve_outline(
        self,
        outline: List[Dict],
        issues: List[str],
        suggestions: List[str],
        context: Dict[str, Any]
    ) -> List[Dict]:
        """
        改进大纲

        Args:
            outline: 原始大纲
            issues: 问题列表
            suggestions: 建议列表
            context: 上下文

        Returns:
            List[Dict]: 改进后的大纲
        """
        improved_outline = outline.copy()

        # 根据问题进行改进
        for issue in issues:
            if "章节数量过少" in issue:
                # 增加章节
                while len(improved_outline) < 15:
                    improved_outline.append({
                        "chapter": len(improved_outline) + 1,
                        "title": f"第{len(improved_outline) + 1}章",
                        "summary": "待完善"
                    })

            elif "缺少标题" in issue:
                # 为缺少标题的章节添加标题
                for i, ch in enumerate(improved_outline):
                    if not ch.get("title"):
                        ch["title"] = f"第{i+1}章"

            elif "缺少简介" in issue:
                # 为缺少简介的章节添加简介
                for ch in improved_outline:
                    if not ch.get("summary"):
                        ch["summary"] = "情节待补充"

        return improved_outline


# ==================== 便捷函数 ====================

async def reflect_on_chapter_writing(
    content: str,
    ai_service: Any,
    context: Dict[str, Any] = None,
    max_iterations: int = 3
) -> Dict[str, Any]:
    """
    对章节写作进行反思和改进

    Args:
        content: 章节内容
        ai_service: AI服务
        context: 上下文
        max_iterations: 最大迭代次数

    Returns:
        Dict: 改进结果
    """
    evaluator = TextQualityEvaluator(ai_service)
    improver = TextImprover(ai_service)

    agent = ReflectionAgent(
        evaluator=evaluator.evaluate_writing_quality,
        improver=improver.improve_writing,
        quality_threshold=80.0,
        max_iterations=max_iterations
    )

    return await agent.reflect_and_improve(content, context)


async def reflect_on_outline(
    outline: List[Dict],
    ai_service: Any,
    context: Dict[str, Any] = None,
    max_iterations: int = 3
) -> Dict[str, Any]:
    """
    对大纲进行反思和改进

    Args:
        outline: 大纲列表
        ai_service: AI服务
        context: 上下文
        max_iterations: 最大迭代次数

    Returns:
        Dict: 改进结果
    """
    evaluator = TextQualityEvaluator(ai_service)
    improver = TextImprover(ai_service)

    agent = ReflectionAgent(
        evaluator=evaluator.evaluate_outline_quality,
        improver=improver.improve_outline,
        quality_threshold=80.0,
        max_iterations=max_iterations
    )

    return await agent.reflect_and_improve(outline, context)
