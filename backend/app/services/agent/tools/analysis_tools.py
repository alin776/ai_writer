"""
分析工具集 (Analysis Tools)

提供标准化的文本分析工具,包括:
1. analyze_content_tool - 内容分析工具
2. evaluate_quality_tool - 质量评估工具

所有工具使用 StandardTool 包装,支持强类型输入输出验证。
"""

from typing import Optional, List, Dict, Any
import logging
from pydantic import Field

from .tool_types import ToolInput, ToolOutput, ToolCategory, StandardTool
from .writing_tools import _ensure_ai_service, _generate_text
from app.services.agent.model_selector import TaskType

logger = logging.getLogger(__name__)


# ==================== 1. 内容分析工具 (Analyze Content) ====================

class AnalyzeContentInput(ToolInput):
    """
    内容分析工具输入

    Attributes:
        content: 待分析的文本内容(必需)
        aspects: 分析维度列表(可选)
        depth: 分析深度(shallow/normal/deep)
        context: 额外的上下文信息(可选)
    """

    content: str = Field(
        ...,
        description="待分析的文本内容",
        min_length=10,
        max_length=20000
    )

    aspects: List[str] = Field(
        default_factory=lambda: ["grammar", "logic", "style", "structure"],
        description="分析维度: grammar(语法), logic(逻辑), style(风格), structure(结构), character(人物), plot(情节)"
    )

    depth: str = Field(
        default="normal",
        description="分析深度: shallow(浅层), normal(正常), deep(深度)",
        pattern="^(shallow|normal|deep)$"
    )

    context: str = Field(
        default="",
        description="额外的上下文信息,帮助更准确的分析"
    )


class AnalyzeContentOutput(ToolOutput):
    """
    内容分析工具输出

    在 ToolOutput.data 中包含:
    - analysis: 分析报告文本
    - summary: 分析摘要
    - scores: 各维度评分(Dict[str, int])
    - issues: 发现的问题列表
    - suggestions: 改进建议列表
    """
    pass


async def analyze_content_executor(
    input_data: AnalyzeContentInput
) -> AnalyzeContentOutput:
    """
    内容分析工具执行器

    对文本进行多维度分析,包括语法、逻辑、风格、结构等。

    Args:
        input_data: 分析输入参数

    Returns:
        分析输出结果
    """
    try:
        # 构建分析维度描述
        aspect_descriptions = {
            "grammar": "语法错误和用词不当",
            "logic": "逻辑连贯性和因果关系",
            "style": "写作风格和表达方式",
            "structure": "文章结构和段落组织",
            "character": "人物刻画和性格一致性",
            "plot": "情节发展和冲突设置"
        }

        selected_aspects = [
            f"- {aspect}: {aspect_descriptions.get(aspect, aspect)}"
            for aspect in input_data.aspects
            if aspect in aspect_descriptions
        ]

        depth_instructions = {
            "shallow": "进行基础层面的分析,指出明显问题",
            "normal": "进行中等深度的分析,包含详细的问题说明和建议",
            "deep": "进行深度分析,包含深层次的问题挖掘、详细的改进方案和最佳实践建议"
        }

        # 构建提示词
        prompt = f"""你是一位专业的文本分析专家。请对以下内容进行全面分析。

【待分析内容】
{input_data.content}"""

        if input_data.context:
            prompt += f"""

【上下文信息】
{input_data.context}"""

        prompt += f"""

【分析要求】
- 分析深度: {depth_instructions[input_data.depth]}
- 分析维度:
{chr(10).join(selected_aspects)}

【输出格式】
请按以下格式输出:

## 分析摘要
[用1-2段话总结整体分析结果]

## 详细分析
{chr(10).join([f"### {aspect_descriptions.get(a, a)}" + chr(10) + "[具体分析内容]" for a in input_data.aspects if a in aspect_descriptions])}

## 主要问题
1. [问题1]
2. [问题2]
...

## 改进建议
1. [建议1]
2. [建议2]
...

## 评分 (0-100)
{chr(10).join([f"- {aspect_descriptions.get(a, a)}: [分数]" for a in input_data.aspects if a in aspect_descriptions])}

请开始分析:"""

        # 调用 AI 生成
        # ✅ 2025-12-08: 添加 task_type，使用适合分析任务的模型
        analysis_text = await _generate_text(
            prompt=prompt,
            temperature=0.3,  # 较低温度,更客观
            max_tokens=3000,
            task_type=TaskType.SUMMARIZATION  # 分析任务属于摘要类型
        )

        # 解析结果
        analysis = analysis_text
        summary = ""
        scores = {}
        issues = []
        suggestions = []

        # 简单解析(实际项目中可以用更复杂的解析逻辑)
        if "## 分析摘要" in analysis_text:
            parts = analysis_text.split("## 详细分析")
            if len(parts) > 0:
                summary_section = parts[0].replace("## 分析摘要", "").strip()
                summary = summary_section.split("\n\n")[0] if summary_section else ""

        if "## 主要问题" in analysis_text:
            issues_section = analysis_text.split("## 主要问题")[1].split("## 改进建议")[0]
            issues = [
                line.strip()
                for line in issues_section.split("\n")
                if line.strip() and (line.strip()[0].isdigit() or line.strip().startswith("-"))
            ]

        if "## 改进建议" in analysis_text:
            suggestions_section = analysis_text.split("## 改进建议")[1].split("## 评分")[0] if "## 评分" in analysis_text else analysis_text.split("## 改进建议")[1]
            suggestions = [
                line.strip()
                for line in suggestions_section.split("\n")
                if line.strip() and (line.strip()[0].isdigit() or line.strip().startswith("-"))
            ]

        # 解析评分
        if "## 评分" in analysis_text:
            score_section = analysis_text.split("## 评分")[1]
            for line in score_section.split("\n"):
                if ":" in line:
                    try:
                        aspect_name, score_str = line.split(":")
                        aspect_name = aspect_name.strip().replace("-", "").strip()
                        score = int(''.join(filter(str.isdigit, score_str)))
                        if 0 <= score <= 100:
                            scores[aspect_name] = score
                    except:
                        continue

        return AnalyzeContentOutput(
            success=True,
            message="分析完成",
            data={
                "analysis": analysis,
                "summary": summary or "分析完成",
                "scores": scores,
                "issues": issues,
                "suggestions": suggestions
            },
            metadata={
                "content_length": len(input_data.content),
                "aspects": input_data.aspects,
                "depth": input_data.depth,
                "issues_count": len(issues),
                "suggestions_count": len(suggestions)
            }
        )

    except Exception as e:
        logger.error(f"内容分析工具执行失败: {e}")
        return AnalyzeContentOutput(
            success=False,
            message=f"分析失败: {str(e)}",
            data=None,
            metadata={"error": str(e)}
        )


# 创建内容分析工具实例
analyze_content_tool = StandardTool(
    name="analyze_content",
    description="多维度分析文本内容,包括语法、逻辑、风格、结构等,提供详细的问题诊断和改进建议",
    category=ToolCategory.ANALYSIS,
    input_schema=AnalyzeContentInput,
    output_schema=AnalyzeContentOutput,
    executor=analyze_content_executor,
    tags=["analysis", "quality", "diagnosis"],
    version="1.0.0"
)


# ==================== 2. 质量评估工具 (Evaluate Quality) ====================

class EvaluateQualityInput(ToolInput):
    """
    质量评估工具输入

    Attributes:
        content: 待评估的文本内容(必需)
        context: 评估上下文(novel/article/report等)
        criteria: 评估标准列表(可选)
        reference: 参考标准或示例(可选)
    """

    content: str = Field(
        ...,
        description="待评估的文本内容",
        min_length=10,
        max_length=20000
    )

    context: str = Field(
        default="novel",
        description="评估上下文类型: novel(小说), article(文章), report(报告), creative(创意写作)",
        pattern="^(novel|article|report|creative)$"
    )

    criteria: List[str] = Field(
        default_factory=lambda: ["readability", "creativity", "coherence", "engagement"],
        description="评估标准: readability(可读性), creativity(创意性), coherence(连贯性), engagement(吸引力), accuracy(准确性)"
    )

    reference: str = Field(
        default="",
        description="参考标准或示例文本,用于对比评估"
    )


class EvaluateQualityOutput(ToolOutput):
    """
    质量评估工具输出

    在 ToolOutput.data 中包含:
    - overall_score: 总体评分(0-100)
    - dimension_scores: 各维度评分(Dict[str, int])
    - strengths: 优势列表
    - weaknesses: 不足列表
    - feedback: 详细反馈
    - grade: 等级评定(A+/A/B+/B/C+/C/D)
    """
    pass


async def evaluate_quality_executor(
    input_data: EvaluateQualityInput
) -> EvaluateQualityOutput:
    """
    质量评估工具执行器

    对文本进行全面的质量评估,给出评分和详细反馈。

    Args:
        input_data: 评估输入参数

    Returns:
        评估输出结果
    """
    try:
        # 构建评估标准描述
        criteria_descriptions = {
            "readability": "可读性 - 文字流畅度、易理解程度",
            "creativity": "创意性 - 新颖性、独特性",
            "coherence": "连贯性 - 逻辑连贯、前后呼应",
            "engagement": "吸引力 - 读者参与度、情感共鸣",
            "accuracy": "准确性 - 事实准确、表达精确"
        }

        context_descriptions = {
            "novel": "小说创作",
            "article": "文章写作",
            "report": "报告撰写",
            "creative": "创意写作"
        }

        selected_criteria = [
            f"- {criteria_descriptions.get(c, c)}"
            for c in input_data.criteria
            if c in criteria_descriptions
        ]

        # 构建提示词
        prompt = f"""你是一位专业的文本质量评估专家。请对以下{context_descriptions.get(input_data.context, '文本')}进行全面的质量评估。

【待评估内容】
{input_data.content}"""

        if input_data.reference:
            prompt += f"""

【参考标准】
{input_data.reference}"""

        prompt += f"""

【评估标准】
{chr(10).join(selected_criteria)}

【输出格式】
请按以下格式输出:

## 总体评分
[0-100分的总分及简要说明]

## 各维度评分
{chr(10).join([f"- {criteria_descriptions.get(c, c)}: [0-100分]" for c in input_data.criteria if c in criteria_descriptions])}

## 优势
1. [优势1]
2. [优势2]
...

## 不足
1. [不足1]
2. [不足2]
...

## 详细反馈
[提供详细的评估反馈,包括具体的例证和改进方向]

## 等级评定
[A+/A/A-/B+/B/B-/C+/C/C-/D]

请开始评估:"""

        # 调用 AI 生成
        # ✅ 2025-12-08: 添加 task_type，使用适合评估任务的模型
        evaluation_text = await _generate_text(
            prompt=prompt,
            temperature=0.3,
            max_tokens=2500,
            task_type=TaskType.QUALITY_EVALUATION  # 质量评估任务
        )

        # 解析结果
        overall_score = 0
        dimension_scores = {}
        strengths = []
        weaknesses = []
        feedback = ""
        grade = "B"

        # 解析总体评分
        if "## 总体评分" in evaluation_text:
            score_section = evaluation_text.split("## 总体评分")[1].split("##")[0]
            try:
                overall_score = int(''.join(filter(str.isdigit, score_section.split("\n")[0])))
                if overall_score > 100:
                    overall_score = 85  # 默认值
            except:
                overall_score = 85

        # 解析各维度评分
        if "## 各维度评分" in evaluation_text:
            dimension_section = evaluation_text.split("## 各维度评分")[1].split("##")[0]
            for line in dimension_section.split("\n"):
                if ":" in line:
                    try:
                        criterion, score_str = line.split(":")
                        criterion = criterion.strip().replace("-", "").strip()
                        score = int(''.join(filter(str.isdigit, score_str)))
                        if 0 <= score <= 100:
                            dimension_scores[criterion] = score
                    except:
                        continue

        # 解析优势
        if "## 优势" in evaluation_text:
            strengths_section = evaluation_text.split("## 优势")[1].split("##")[0]
            strengths = [
                line.strip()
                for line in strengths_section.split("\n")
                if line.strip() and (line.strip()[0].isdigit() or line.strip().startswith("-"))
            ]

        # 解析不足
        if "## 不足" in evaluation_text:
            weaknesses_section = evaluation_text.split("## 不足")[1].split("##")[0]
            weaknesses = [
                line.strip()
                for line in weaknesses_section.split("\n")
                if line.strip() and (line.strip()[0].isdigit() or line.strip().startswith("-"))
            ]

        # 解析详细反馈
        if "## 详细反馈" in evaluation_text:
            feedback = evaluation_text.split("## 详细反馈")[1].split("##")[0].strip()

        # 解析等级
        if "## 等级评定" in evaluation_text:
            grade_section = evaluation_text.split("## 等级评定")[1].strip()
            grade_line = grade_section.split("\n")[0].strip()
            # 提取等级(A+, A, B+等)
            import re
            grade_match = re.search(r'[A-D][+-]?', grade_line)
            if grade_match:
                grade = grade_match.group()

        return EvaluateQualityOutput(
            success=True,
            message="评估完成",
            data={
                "overall_score": overall_score,
                "dimension_scores": dimension_scores,
                "strengths": strengths,
                "weaknesses": weaknesses,
                "feedback": feedback,
                "grade": grade
            },
            metadata={
                "content_length": len(input_data.content),
                "context": input_data.context,
                "criteria": input_data.criteria,
                "strengths_count": len(strengths),
                "weaknesses_count": len(weaknesses)
            }
        )

    except Exception as e:
        logger.error(f"质量评估工具执行失败: {e}")
        return EvaluateQualityOutput(
            success=False,
            message=f"评估失败: {str(e)}",
            data=None,
            metadata={"error": str(e)}
        )


# 创建质量评估工具实例
evaluate_quality_tool = StandardTool(
    name="evaluate_quality",
    description="全面评估文本质量,包括可读性、创意性、连贯性等多个维度,提供评分和改进反馈",
    category=ToolCategory.QUALITY,
    input_schema=EvaluateQualityInput,
    output_schema=EvaluateQualityOutput,
    executor=evaluate_quality_executor,
    tags=["evaluation", "quality", "scoring"],
    version="1.0.0"
)


# ==================== 导出 ====================

__all__ = [
    # 内容分析工具
    "AnalyzeContentInput",
    "AnalyzeContentOutput",
    "analyze_content_tool",
    # 质量评估工具
    "EvaluateQualityInput",
    "EvaluateQualityOutput",
    "evaluate_quality_tool",
    # 文本分析工具（兼容 @tool 版本）
    "AnalyzeTextInput",
    "AnalyzeTextOutput",
    "analyze_text_tool",
]


# ==================== 3. 文本分析工具 (Analyze Text) - 兼容 @tool 版本 ====================
# 🔧 2025-12-14: 新增 analyze_text_tool，参数与 @tool 版本兼容

class AnalyzeTextInput(ToolInput):
    """
    文本分析工具输入（兼容 @tool 版本）

    Attributes:
        text: 待分析的文本
        focus: 分析重点（all/grammar/logic/style）
    """

    text: str = Field(
        ...,
        description="待分析的文本",
        min_length=1,
        max_length=50000
    )

    focus: str = Field(
        default="all",
        description="分析重点: 可以是预定义值(all/grammar/logic/style/structure)或任意描述性字符串(如'分析情节发展'、'概括主要内容')。当focus='all'或包含'全面/完整'时输出完整报告，否则输出简洁聚焦分析(200-500字)",
        min_length=1,
        max_length=500  # 限制长度，避免过长的 focus 描述
    )


class AnalyzeTextOutput(ToolOutput):
    """
    文本分析工具输出

    在 ToolOutput.data 中包含:
    - analysis_report: 分析报告文本
    """
    pass


async def analyze_text_executor(
    input_data: AnalyzeTextInput
) -> AnalyzeTextOutput:
    """
    文本分析工具执行器（兼容 @tool 版本）

    Args:
        input_data: 分析输入参数

    Returns:
        分析输出结果
    """
    try:
        # 检查占位符
        if "$TASK_" in input_data.text and "$" in input_data.text[input_data.text.find("$TASK_")+1:]:
            logger.warning(f"[analyze_text_tool] 检测到未解析的占位符")
            return AnalyzeTextOutput(
                success=False,
                message="文本参数中包含未解析的占位符",
                data={"analysis_report": f"错误：文本参数中包含未解析的占位符。原始参数: {input_data.text[:200]}"},
                metadata={"error": "unresolved_placeholder"}
            )

        # 尝试使用 prompt_manager 渲染模板
        try:
            from app.prompts import get_prompt_manager
            prompt_manager = get_prompt_manager()
            base_prompt = prompt_manager.render("analyze_text", text=input_data.text, focus=input_data.focus)
        except Exception as e:
            logger.warning(f"[analyze_text_tool] 约束提示词系统失败，使用降级方案: {e}")
            # 降级 prompt
            base_prompt = f"""请分析以下文本，重点关注：{input_data.focus}

文本：
{input_data.text}

请提供详细的分析报告："""

        # 调用 AI 生成
        result = await _generate_text(
            prompt=base_prompt,
            temperature=0.3,
            max_tokens=1500,
            task_type=TaskType.SUMMARIZATION
        )

        logger.info(f"[analyze_text_tool] 分析完成，结果长度: {len(result)}")

        return AnalyzeTextOutput(
            success=True,
            message="分析完成",
            data={
                "analysis_report": result
            },
            metadata={
                "text_length": len(input_data.text),
                "focus": input_data.focus
            }
        )

    except Exception as e:
        logger.error(f"文本分析工具执行失败: {e}")
        return AnalyzeTextOutput(
            success=False,
            message=f"分析失败: {str(e)}",
            data=None,
            metadata={"error": str(e)}
        )


# 创建文本分析工具实例
analyze_text_tool = StandardTool(
    name="analyze_text",
    description="分析文本问题，重点关注语法、逻辑、风格等方面",
    category=ToolCategory.ANALYSIS,
    input_schema=AnalyzeTextInput,
    output_schema=AnalyzeTextOutput,
    executor=analyze_text_executor,
    tags=["analysis", "text", "diagnosis"],
    version="1.0.0"
)

