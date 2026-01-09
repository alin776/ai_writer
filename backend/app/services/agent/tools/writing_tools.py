"""
写作工具集 (Writing Tools)

提供标准化的写作相关工具,包括:
1. expand_text_tool - 扩写工具

所有工具使用 StandardTool 包装,支持强类型输入输出验证。
"""

from typing import Optional
import logging
from pydantic import Field

from .tool_types import ToolInput, ToolOutput, ToolCategory, StandardTool
from app.services.ai.http_ai_service import HTTPAIService
from app.services.agent.model_selector import TaskType

logger = logging.getLogger(__name__)


# ==================== 自定义异常 ====================

class InsufficientCreditsError(Exception):
    """积分不足异常"""
    def __init__(self, message: str = "积分余额不足，请先充值后再使用此功能。"):
        self.message = message
        super().__init__(self.message)


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
    max_tokens: int = 2000,
    task_type: Optional[TaskType] = None  # ← 新增参数
) -> str:
    """
    使用 HTTPAIService 生成文本的辅助函数

    Args:
        prompt: 提示词
        temperature: 温度参数(0.0-1.0)
        max_tokens: 最大token数
        task_type: 任务类型（用于模型选择）

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
            temperature=temperature,
            task_type=task_type  # ← 传递task_type
        ):
            generated_text += chunk

        if not generated_text:
            return "错误: AI 生成内容为空"

        return generated_text.strip()

    except Exception as e:
        error_str = str(e)
        logger.error(f"文本生成失败: {error_str}")

        # 检测积分不足错误，抛出特定异常
        if "积分" in error_str and ("不足" in error_str or "余额" in error_str):
            raise InsufficientCreditsError("积分余额不足，请先充值后再使用此功能。")

        return f"错误: 文本生成失败 - {error_str}"


# ==================== 1. 扩写工具 (Expand Text) ====================

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
            max_tokens=min(input_data.target_length * 2, 5000),
            task_type=TaskType.CONTENT_CREATION  # ← 新增：指定为创作任务
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

    except InsufficientCreditsError as e:
        logger.warning(f"扩写工具积分不足: {e}")
        return ExpandTextOutput(
            success=False,
            message=e.message,
            data={"expanded_text": e.message},
            metadata={"error": "insufficient_credits"}
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
    # 异常
    "InsufficientCreditsError",
    # 输入输出模型
    "ExpandTextInput",
    "ExpandTextOutput",
    # 工具实例
    "expand_text_tool",
]
