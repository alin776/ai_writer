"""
写作工具集 (Writing Tools)

提供标准化的写作相关工具,包括:
1. continue_writing_tool - 续写工具
2. polish_text_tool - 润色工具
3. expand_text_tool - 扩写工具

所有工具使用 StandardTool 包装,支持强类型输入输出验证。
"""

from typing import Optional
import logging
from pydantic import Field

from .tool_types import ToolInput, ToolOutput, ToolCategory, StandardTool
from app.services.ai.http_ai_service import HTTPAIService

logger = logging.getLogger(__name__)


# ==================== 全局 AI Service ====================

# 全局 HTTPAIService 实例(需要在初始化时设置)
_ai_service: Optional[HTTPAIService] = None


def set_ai_service(ai_service: HTTPAIService):
    """
    设置全局 AI Service

    Args:
        ai_service: HTTPAIService 实例
    """
    global _ai_service
    _ai_service = ai_service
    logger.info("Writing tools AI service initialized")


def _ensure_ai_service() -> HTTPAIService:
    """确保 AI Service 已初始化"""
    if _ai_service is None:
        raise RuntimeError(
            "AI Service 未初始化。请先调用 set_ai_service() 设置 AI Service 实例。"
        )
    return _ai_service


# ==================== 辅助函数 ====================

async def _generate_text(
    prompt: str,
    temperature: float = 0.7,
    max_tokens: int = 2000
) -> str:
    """
    使用 HTTPAIService 生成文本的辅助函数

    Args:
        prompt: 提示词
        temperature: 温度参数(0.0-1.0)
        max_tokens: 最大token数

    Returns:
        生成的文本
    """
    ai_service = _ensure_ai_service()

    messages = [{"role": "user", "content": prompt}]

    try:
        # 流式生成
        generated_text = ""
        async for chunk, _ in ai_service._stream_chat(
            messages=messages,
            max_tokens=max_tokens,
            temperature=temperature
        ):
            generated_text += chunk

        if not generated_text:
            return "错误: AI 生成内容为空"

        return generated_text.strip()

    except Exception as e:
        logger.error(f"文本生成失败: {e}")
        return f"错误: 文本生成失败 - {str(e)}"


# ==================== 1. 续写工具 (Continue Writing) ====================

class ContinueWritingInput(ToolInput):
    """
    续写工具输入

    Attributes:
        context: 已有的文本上下文(必需)
        requirements: 续写要求(可选)
        target_length: 目标长度,单位:字符(可选)
        style: 写作风格(可选)
    """

    context: str = Field(
        ...,
        description="已有的文本上下文,用于续写",
        min_length=10,
        max_length=10000
    )

    requirements: str = Field(
        default="",
        description="续写的具体要求(如情节发展、人物行为等)"
    )

    target_length: int = Field(
        default=500,
        description="期望续写的长度(字符数)",
        ge=100,
        le=5000
    )

    style: str = Field(
        default="",
        description="写作风格(如:悬疑、温馨、激烈等)"
    )


class ContinueWritingOutput(ToolOutput):
    """
    续写工具输出

    在 ToolOutput.data 中包含:
    - generated_text: 生成的续写文本
    - word_count: 生成的字数
    - actual_length: 实际长度(字符数)
    """
    pass


async def continue_writing_executor(
    input_data: ContinueWritingInput
) -> ContinueWritingOutput:
    """
    续写工具执行器

    根据已有上下文和要求,生成续写内容。

    Args:
        input_data: 续写输入参数

    Returns:
        续写输出结果
    """
    try:
        # 构建提示词
        prompt = f"""你是一位专业的小说续写助手。请根据以下上下文续写内容。

【上下文】
{input_data.context}

【续写要求】
- 目标长度: 约 {input_data.target_length} 字符"""

        if input_data.requirements:
            prompt += f"\n- 具体要求: {input_data.requirements}"

        if input_data.style:
            prompt += f"\n- 写作风格: {input_data.style}"

        prompt += """

【重要】
1. 直接输出续写的小说正文,不要输出任何说明文字、建议或问题
2. 保持与上下文的风格一致
3. 情节合理自然,符合人物性格
4. 立即开始续写:"""

        # 调用 AI 生成
        generated_text = await _generate_text(
            prompt=prompt,
            temperature=0.8,
            max_tokens=min(input_data.target_length * 2, 4000)
        )

        # 计算字数
        word_count = len(generated_text)

        return ContinueWritingOutput(
            success=True,
            message="续写成功",
            data={
                "generated_text": generated_text,
                "word_count": word_count,
                "actual_length": len(generated_text)
            },
            metadata={
                "context_length": len(input_data.context),
                "target_length": input_data.target_length,
                "style": input_data.style or "default"
            }
        )

    except Exception as e:
        logger.error(f"续写工具执行失败: {e}")
        return ContinueWritingOutput(
            success=False,
            message=f"续写失败: {str(e)}",
            data=None,
            metadata={"error": str(e)}
        )


# 创建续写工具实例
continue_writing_tool = StandardTool(
    name="continue_writing",
    description="根据上下文续写小说内容,支持自定义续写要求和风格",
    category=ToolCategory.WRITING,
    input_schema=ContinueWritingInput,
    output_schema=ContinueWritingOutput,
    executor=continue_writing_executor,
    tags=["writing", "generation", "novel"],
    version="1.0.0"
)


# ==================== 2. 润色工具 (Polish Text) ====================

class PolishTextInput(ToolInput):
    """
    润色工具输入

    Attributes:
        content: 待润色的文本内容(必需)
        aspect: 润色重点(可选: grammar/style/flow/all)
        style: 目标风格(可选: professional/creative/concise)
        preserve_meaning: 是否保持原意(默认True)
    """

    content: str = Field(
        ...,
        description="待润色的文本内容",
        min_length=10,
        max_length=10000
    )

    aspect: str = Field(
        default="all",
        description="润色重点: grammar(语法), style(风格), flow(流畅度), all(全面)",
        pattern="^(grammar|style|flow|all)$"
    )

    style: str = Field(
        default="professional",
        description="目标风格: professional(专业), creative(创意), concise(简洁)",
        pattern="^(professional|creative|concise)$"
    )

    preserve_meaning: bool = Field(
        default=True,
        description="是否严格保持原意"
    )


class PolishTextOutput(ToolOutput):
    """
    润色工具输出

    在 ToolOutput.data 中包含:
    - polished_text: 润色后的文本
    - changes: 主要修改说明列表
    - improvement_score: 改进评分(0-100)
    """
    pass


async def polish_text_executor(
    input_data: PolishTextInput
) -> PolishTextOutput:
    """
    润色工具执行器

    对文本进行润色,改善语法、风格和流畅度。

    Args:
        input_data: 润色输入参数

    Returns:
        润色输出结果
    """
    try:
        # 构建提示词
        aspect_desc = {
            "grammar": "重点改善语法错误和用词不当",
            "style": "重点优化写作风格和表达方式",
            "flow": "重点提升文本流畅度和连贯性",
            "all": "全面优化语法、风格和流畅度"
        }

        style_desc = {
            "professional": "专业、正式的表达",
            "creative": "富有创意、生动的描写",
            "concise": "简洁明了、精炼的叙述"
        }

        prompt = f"""你是一位专业的文本润色专家。请对以下文本进行润色优化。

【原文】
{input_data.content}

【润色要求】
- 润色重点: {aspect_desc[input_data.aspect]}
- 目标风格: {style_desc[input_data.style]}
- 保持原意: {'是(严格保持原文意思)' if input_data.preserve_meaning else '否(可适度改写)'}

【输出格式】
请按以下格式输出:

润色后文本:
[这里输出润色后的完整文本]

主要修改:
1. [修改点1]
2. [修改点2]
...(列出主要修改)

请开始润色:"""

        # 调用 AI 生成
        result_text = await _generate_text(
            prompt=prompt,
            temperature=0.7,
            max_tokens=3000
        )

        # 解析结果
        polished_text = ""
        changes = []

        if "润色后文本:" in result_text:
            parts = result_text.split("主要修改:")
            polished_text = parts[0].replace("润色后文本:", "").strip()

            if len(parts) > 1:
                changes_text = parts[1].strip()
                changes = [
                    line.strip()
                    for line in changes_text.split("\n")
                    if line.strip() and (line.strip()[0].isdigit() or line.strip().startswith("-"))
                ]
        else:
            polished_text = result_text

        return PolishTextOutput(
            success=True,
            message="润色成功",
            data={
                "polished_text": polished_text,
                "changes": changes,
                "improvement_score": 85  # 简化版,实际可用AI评分
            },
            metadata={
                "original_length": len(input_data.content),
                "polished_length": len(polished_text),
                "aspect": input_data.aspect,
                "style": input_data.style
            }
        )

    except Exception as e:
        logger.error(f"润色工具执行失败: {e}")
        return PolishTextOutput(
            success=False,
            message=f"润色失败: {str(e)}",
            data=None,
            metadata={"error": str(e)}
        )


# 创建润色工具实例
polish_text_tool = StandardTool(
    name="polish_text",
    description="润色优化文本内容,改善语法、风格和流畅度",
    category=ToolCategory.WRITING,
    input_schema=PolishTextInput,
    output_schema=PolishTextOutput,
    executor=polish_text_executor,
    tags=["writing", "editing", "polish"],
    version="1.0.0"
)


# ==================== 3. 扩写工具 (Expand Text) ====================

class ExpandTextInput(ToolInput):
    """
    扩写工具输入

    Attributes:
        content: 待扩写的文本内容(必需)
        target_length: 目标长度,单位:字符(必需)
        direction: 扩写方向(before/after/both)
        focus: 扩写重点(detail/dialogue/description/action)
    """

    content: str = Field(
        ...,
        description="待扩写的文本内容",
        min_length=10,
        max_length=10000
    )

    target_length: int = Field(
        ...,
        description="目标总长度(字符数)",
        ge=100,
        le=10000
    )

    direction: str = Field(
        default="after",
        description="扩写方向: before(在前面扩写), after(在后面扩写), both(前后都扩写)",
        pattern="^(before|after|both)$"
    )

    focus: str = Field(
        default="detail",
        description="扩写重点: detail(细节描写), dialogue(对话), description(环境描写), action(动作描写)",
        pattern="^(detail|dialogue|description|action)$"
    )


class ExpandTextOutput(ToolOutput):
    """
    扩写工具输出

    在 ToolOutput.data 中包含:
    - expanded_text: 扩写后的完整文本
    - added_length: 增加的字符数
    - expansion_ratio: 扩写倍数
    """
    pass


async def expand_text_executor(
    input_data: ExpandTextInput
) -> ExpandTextOutput:
    """
    扩写工具执行器

    对文本进行扩写,增加细节、对话或描写。

    Args:
        input_data: 扩写输入参数

    Returns:
        扩写输出结果
    """
    try:
        # 计算需要扩写的长度
        original_length = len(input_data.content)
        target_expansion = input_data.target_length - original_length

        if target_expansion <= 0:
            return ExpandTextOutput(
                success=False,
                message=f"目标长度({input_data.target_length})应大于原文长度({original_length})",
                data=None
            )

        # 构建提示词
        direction_desc = {
            "before": "在原文之前扩写",
            "after": "在原文之后扩写",
            "both": "在原文前后都进行扩写"
        }

        focus_desc = {
            "detail": "增加细节描写,丰富场景和情感",
            "dialogue": "增加人物对话,推动情节发展",
            "description": "增加环境氛围描写,营造画面感",
            "action": "增加动作描写,使叙述更加生动"
        }

        prompt = f"""你是一位专业的小说扩写专家。请对以下文本进行扩写。

【原文】
{input_data.content}

【扩写要求】
- 原文长度: {original_length} 字符
- 目标长度: {input_data.target_length} 字符
- 需要增加: 约 {target_expansion} 字符
- 扩写方向: {direction_desc[input_data.direction]}
- 扩写重点: {focus_desc[input_data.focus]}

【重要】
1. 保持与原文的风格和语气一致
2. 扩写的内容要自然融入,不生硬
3. 直接输出扩写后的完整文本,不要输出说明文字

请开始扩写:"""

        # 调用 AI 生成
        expanded_text = await _generate_text(
            prompt=prompt,
            temperature=0.75,
            max_tokens=min(input_data.target_length * 2, 5000)
        )

        # 计算扩写统计
        final_length = len(expanded_text)
        added_length = final_length - original_length
        expansion_ratio = final_length / original_length if original_length > 0 else 1.0

        return ExpandTextOutput(
            success=True,
            message="扩写成功",
            data={
                "expanded_text": expanded_text,
                "added_length": added_length,
                "expansion_ratio": round(expansion_ratio, 2)
            },
            metadata={
                "original_length": original_length,
                "target_length": input_data.target_length,
                "final_length": final_length,
                "direction": input_data.direction,
                "focus": input_data.focus
            }
        )

    except Exception as e:
        logger.error(f"扩写工具执行失败: {e}")
        return ExpandTextOutput(
            success=False,
            message=f"扩写失败: {str(e)}",
            data=None,
            metadata={"error": str(e)}
        )


# 创建扩写工具实例
expand_text_tool = StandardTool(
    name="expand_text",
    description="扩写文本内容,增加细节、对话或描写,使内容更加丰富",
    category=ToolCategory.WRITING,
    input_schema=ExpandTextInput,
    output_schema=ExpandTextOutput,
    executor=expand_text_executor,
    tags=["writing", "expansion", "detail"],
    version="1.0.0"
)


# ==================== 导出 ====================

__all__ = [
    # AI Service
    "set_ai_service",
    # 输入输出模型
    "ContinueWritingInput",
    "ContinueWritingOutput",
    "PolishTextInput",
    "PolishTextOutput",
    "ExpandTextInput",
    "ExpandTextOutput",
    # 工具实例
    "continue_writing_tool",
    "polish_text_tool",
    "expand_text_tool",
]
