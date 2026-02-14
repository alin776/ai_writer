"""
写作工具集 (Writing Tools)

提供写作相关的基础设施：
- InsufficientCreditsError 异常
- AI Service 全局实例管理
- _generate_text 辅助函数
"""

from typing import Optional
import logging

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


# ==================== 导出 ====================

__all__ = [
    "set_ai_service",
    "InsufficientCreditsError",
    "_ensure_ai_service",
    "_generate_text",
]
