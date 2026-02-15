"""
分析工具集 (Analysis Tools)

提供标准化的文本分析工具,包括:
1. analyze_content_tool - 内容分析工具
2. evaluate_quality_tool - 质量评估工具

所有工具使用 StandardTool 包装,支持强类型输入输出验证。
"""

from typing import Optional, List, Dict, Any
import json
import logging
from pydantic import Field, ConfigDict
from app.utils.json_parser import parse_ai_json

from .tool_types import ToolInput, ToolOutput, ToolCategory, StandardTool
from .writing_tools import _ensure_ai_service, _generate_text, InsufficientCreditsError
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
        analysis_types: 分析类型列表(可选)
        focus: 分析重点(可选)
        work_id: 作品ID（用于一致性检查）
        chapter_id: 章节ID（可选）
    """

    content: str = Field(
        ...,
        description="待分析的文本内容",
        min_length=10,
        max_length=200000,
        alias="text"  # 兼容 text 参数
    )

    aspects: List[str] = Field(
        default_factory=lambda: ["grammar", "logic", "style", "structure"],
        description="分析维度: grammar(语法), logic(逻辑), style(风格), structure(结构), character(人物), plot(情节)"
    )

    analysis_types: List[str] = Field(
        default_factory=lambda: ["text", "style"],
        description="分析类型: text(文本), style(风格), consistency(一致性), quality(质量)"
    )

    focus: str = Field(
        default="all",
        description="分析重点: grammar/logic/style/structure/character/plot/all",
        min_length=1,
        max_length=100
    )

    work_id: str = Field(
        default="",
        description="作品ID（用于一致性检查）"
    )

    chapter_id: str = Field(
        default="",
        description="章节ID（可选）"
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

    model_config = ConfigDict(populate_by_name=True)  # 允许同时使用 content 和 text


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


async def _run_text_analysis(
    content: str,
    aspects: List[str],
    depth: str,
    context: str,
    focus: str
) -> Dict[str, Any]:
    """执行文本分析（兼容旧版 aspects）"""
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
        for aspect in aspects
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
{content}"""

    if context:
        prompt += f"""

【上下文信息】
{context}"""

    if focus and focus != "all":
        prompt += f"""

【分析重点】
{focus}"""

    prompt += f"""

【分析要求】
- 分析深度: {depth_instructions.get(depth, depth_instructions["normal"])}
- 分析维度:
{chr(10).join(selected_aspects)}

【输出格式】
请按以下格式输出:

## 分析摘要
[用1-2段话总结整体分析结果]

## 详细分析
{chr(10).join([f"### {aspect_descriptions.get(a, a)}" + chr(10) + "[具体分析内容]" for a in aspects if a in aspect_descriptions])}

## 主要问题
1. [问题1]
2. [问题2]
...

## 改进建议
1. [建议1]
2. [建议2]
...

## 评分 (0-100)
{chr(10).join([f"- {aspect_descriptions.get(a, a)}: [分数]" for a in aspects if a in aspect_descriptions])}

请开始分析:"""

    analysis_text = await _generate_text(
        prompt=prompt,
        temperature=0.3,
        max_tokens=3000,
        task_type=TaskType.SUMMARIZATION
    )

    # 解析结果
    summary = ""
    scores = {}
    issues = []
    suggestions = []

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
                except Exception:
                    continue

    return {
        "analysis": analysis_text,
        "summary": summary or "分析完成",
        "scores": scores,
        "issues": issues,
        "suggestions": suggestions
    }


def _run_style_analysis(content: str) -> Dict[str, Any]:
    """执行风格分析（规则计算）"""
    try:
        from app.services.agent.tools.style_learning import analyze_writing_style
        features = analyze_writing_style(content)
        vocabulary_level = "basic"
        if features.vocabulary_richness >= 0.6:
            vocabulary_level = "advanced"
        elif features.vocabulary_richness >= 0.4:
            vocabulary_level = "intermediate"

        tone = "neutral"
        if getattr(features, "exclamation_usage", 0) > 0.05:
            tone = "excited"
        elif getattr(features, "ellipsis_usage", 0) > 0.05:
            tone = "hesitant"

        description_ratio = round(features.long_sentence_ratio, 2)
        action_ratio = round(features.short_sentence_ratio, 2)
        return {
            "avg_sentence_length": features.avg_sentence_length,
            "pov": features.pov,
            "long_sentence_ratio": round(features.long_sentence_ratio, 2),
            "short_sentence_ratio": round(features.short_sentence_ratio, 2),
            "vocabulary_richness": round(features.vocabulary_richness, 2),
            "common_words": features.common_words[:5],
            "dialogue_ratio": round(features.dialogue_ratio, 2),
            "avg_paragraph_length": features.avg_paragraph_length,
            "description_ratio": description_ratio,
            "action_ratio": action_ratio,
            "tone": tone,
            "vocabulary_level": vocabulary_level
        }
    except Exception as e:
        return {"error": str(e)}


async def _build_consistency_context(input_data: "AnalyzeContentInput") -> str:
    """构建一致性检查上下文（优先使用传入 context）"""
    if input_data.context:
        return input_data.context
    if not input_data.work_id:
        return ""

    try:
        from app.services.agent.langgraph_tools import get_writing_context
        include_parts = ["worldview"]
        chapter_id = input_data.chapter_id or ""
        if chapter_id:
            include_parts.insert(0, "chapter")

        result_str = await get_writing_context.ainvoke({
            "work_id": input_data.work_id,
            "chapter_id": chapter_id,
            "include": ",".join(include_parts)
        })
        return result_str if isinstance(result_str, str) else json.dumps(result_str, ensure_ascii=False)
    except Exception as e:
        logger.warning(f"[analyze_content] 获取一致性上下文失败: {e}")
        return ""


async def _run_consistency_check(content: str, context: str, work_id: str) -> Dict[str, Any]:
    """执行一致性检查（LLM）"""
    if not context:
        return {"error": "一致性检查需要提供 context 或 work_id"}

    prompt = f"""请检查以下新内容与作品上下文的一致性：

作品上下文：
{context}

新内容：
{content}

请以 JSON 格式返回检查结果：
{{
  "score": 0-100,
  "inconsistencies": [{{"type": "类型", "description": "描述"}}],
  "warnings": [{{"type": "类型", "description": "描述"}}]
}}
"""

    report = await _generate_text(
        prompt=prompt,
        temperature=0.3,
        max_tokens=1500,
        task_type=TaskType.DEEP_ANALYSIS
    )

    report_text = report.strip() if isinstance(report, str) else str(report)
    parsed = parse_ai_json(
        report_text,
        fallback_value={"error": "解析失败", "raw_report": report_text[:500]},
        log_prefix="consistency_check"
    )

    if isinstance(parsed, dict) and not parsed.get("error"):
        parsed.setdefault("work_id", work_id)
        parsed.setdefault("raw_report", report_text)
        return parsed

    return {
        "work_id": work_id,
        "report": report_text,
        "error": parsed.get("error") if isinstance(parsed, dict) else "parse_failed"
    }


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
        def _truncate_text(text: str, max_len: int) -> tuple[str, bool]:
            if len(text) <= max_len:
                return text, False
            head_len = int(max_len * 0.7)
            tail_len = max_len - head_len
            omitted = len(text) - max_len
            return (
                f"{text[:head_len]}\n\n...[省略 {omitted} 字符]...\n\n{text[-tail_len:]}",
                True
            )

        analysis_types = [t.strip().lower() for t in (input_data.analysis_types or []) if t.strip()]
        if not analysis_types:
            analysis_types = ["text", "style"]

        original_content = input_data.content or ""
        content_length = len(original_content)
        text_content = original_content
        truncated_for_text = False
        truncated_for_llm = False

        if content_length > 50000:
            text_content, truncated_for_text = _truncate_text(original_content, 50000)

        llm_content = original_content
        if content_length > 20000:
            llm_content, truncated_for_llm = _truncate_text(original_content, 20000)

        report_sections = []
        data: Dict[str, Any] = {"analysis_types": analysis_types}
        summary = ""
        scores: Dict[str, Any] = {}
        issues: List[str] = []
        suggestions: List[str] = []

        if "text" in analysis_types:
            if content_length > 20000:
                text_report = await analyze_text_executor(
                    AnalyzeTextInput(text=text_content, focus=input_data.focus)
                )
                analysis_report = (text_report.data or {}).get("analysis_report", "")
                data["text_analysis"] = {
                    "analysis": analysis_report,
                    "summary": "分析完成",
                    "scores": {},
                    "issues": [],
                    "suggestions": []
                }
                summary = "分析完成"
                report_sections.append(f"【文本分析】\n{analysis_report}")
            else:
                text_result = await _run_text_analysis(
                    input_data.content,
                    input_data.aspects,
                    input_data.depth,
                    input_data.context,
                    input_data.focus
                )
                data["text_analysis"] = text_result
                summary = text_result.get("summary", "")
                scores = text_result.get("scores", {})
                issues = text_result.get("issues", [])
                suggestions = text_result.get("suggestions", [])
                report_sections.append(f"【文本分析】\n{text_result.get('analysis', '')}")

        if "style" in analysis_types:
            style_features = _run_style_analysis(text_content if content_length > 20000 else input_data.content)
            data["style_features"] = style_features
            report_sections.append(f"【风格特征】\n{json.dumps(style_features, ensure_ascii=False)}")

        if "consistency" in analysis_types:
            consistency_context = await _build_consistency_context(input_data)
            consistency_report = await _run_consistency_check(
                llm_content,
                consistency_context,
                input_data.work_id
            )
            data["consistency_report"] = consistency_report
            report_sections.append(f"【一致性检查】\n{json.dumps(consistency_report, ensure_ascii=False)}")

        if "quality" in analysis_types:
            quality_result = await evaluate_quality_executor(
                EvaluateQualityInput(content=llm_content)
            )
            quality_data = quality_result.data or {}
            data["quality_evaluation"] = quality_data
            report_sections.append(f"【质量评估】\n{json.dumps(quality_data, ensure_ascii=False)}")

        analysis_text = "\n\n".join([s for s in report_sections if s]) or "分析完成"
        data.setdefault("analysis", analysis_text)
        data.setdefault("summary", summary or "分析完成")
        data.setdefault("scores", scores)
        data.setdefault("issues", issues)
        data.setdefault("suggestions", suggestions)

        return AnalyzeContentOutput(
            success=True,
            message="分析完成",
            data=data,
            metadata={
                "content_length": content_length,
                "analysis_types": analysis_types,
                "aspects": input_data.aspects,
                "depth": input_data.depth,
                "issues_count": len(issues),
                "suggestions_count": len(suggestions),
                "truncated_for_text": truncated_for_text,
                "truncated_for_llm": truncated_for_llm
            }
        )

    except InsufficientCreditsError as e:
        logger.warning(f"内容分析工具积分不足: {e}")
        return AnalyzeContentOutput(
            success=False,
            message=e.message,
            data={"analysis": e.message, "summary": e.message},
            metadata={"error": "insufficient_credits"}
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
    description="多维度分析文本内容,支持 analysis_types 聚合与 aspects 兼容,提供诊断与建议",
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
        max_length=20000,
        alias="text"  # 支持 AI 传递 "text" 参数
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

    model_config = ConfigDict(populate_by_name=True)  # 允许同时使用 content 和 text


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

    except InsufficientCreditsError as e:
        logger.warning(f"质量评估工具积分不足: {e}")
        return EvaluateQualityOutput(
            success=False,
            message=e.message,
            data={"feedback": e.message},
            metadata={"error": "insufficient_credits"}
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

        # 🔧 2025-12-15: 增强的重试/降级机制
        # 通过切换 task_type 来影响模型选择：
        # - SUMMARIZATION (MEDIUM) -> 使用标准模型
        # - SIMPLE_QA (SIMPLE) -> 使用更快/更轻量的模型
        fallback_configs = [
            {"temperature": 0.3, "task_type": TaskType.SUMMARIZATION},
            {"temperature": 0.5, "task_type": TaskType.SUMMARIZATION},
            {"temperature": 0.7, "task_type": TaskType.SIMPLE_QA},  # 降级到更快的模型
        ]

        result = None
        last_error = None

        for attempt, config in enumerate(fallback_configs):
            try:
                logger.info(f"[analyze_text_tool] 尝试第 {attempt + 1} 次调用，config={config}")
                result = await _generate_text(
                    prompt=base_prompt,
                    temperature=config["temperature"],
                    max_tokens=1500,
                    task_type=config["task_type"]
                )

                # 检查是否为空响应或错误
                if result and not result.startswith("错误:") and not result.startswith("错误：") and len(result) > 20:
                    logger.info(f"[analyze_text_tool] 第 {attempt + 1} 次调用成功")
                    break
                else:
                    last_error = f"空响应或错误: {result[:100] if result else 'None'}"
                    logger.warning(f"[analyze_text_tool] 第 {attempt + 1} 次调用返回空/错误: {last_error}")
                    result = None

            except Exception as e:
                last_error = str(e)
                logger.warning(f"[analyze_text_tool] 第 {attempt + 1} 次调用异常: {e}")
                continue

        # 如果所有尝试都失败
        if not result or result.startswith("错误:") or result.startswith("错误："):
            logger.error(f"[analyze_text_tool] 所有重试均失败: {last_error}")
            return AnalyzeTextOutput(
                success=False,
                message="AI 生成内容为空，请稍后重试",
                data={"analysis_report": "分析失败：AI 服务暂时无法响应，请稍后重试。"},
                metadata={"error": "empty_ai_response", "retry_attempted": True, "attempts": len(fallback_configs)}
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

    except InsufficientCreditsError as e:
        logger.warning(f"文本分析工具积分不足: {e}")
        return AnalyzeTextOutput(
            success=False,
            message=e.message,
            data={"analysis_report": e.message},
            metadata={"error": "insufficient_credits"}
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

