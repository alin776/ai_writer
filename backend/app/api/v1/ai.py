"""
AI 服务 API 路由

提供 AI 相关的 RESTful API 接口，包括：
- AI 续写（流式响应）
- AI 润色（流式响应）
- AI 翻译（流式响应）
- AI 扩写（流式响应）
- AI 总结（流式响应）

所有接口均返回 Server-Sent Events (SSE) 流式响应
"""

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import StreamingResponse
from sqlalchemy.ext.asyncio import AsyncSession
from pydantic import BaseModel, Field
import logging

from app.core.database import get_db
from app.core.security import get_current_active_user
from app.models.user import User
from app.services.ai.http_ai_service import HTTPAIService

router = APIRouter()
logger = logging.getLogger(__name__)


# ==================== 请求数据模型 ====================

class AICompleteRequest(BaseModel):
    """AI 续写请求"""
    context: str = Field(..., description="上下文内容（用户已写的内容）", min_length=1)
    prompt: str = Field(default="续写", description="续写指令")
    style: str = Field(default="", description="写作风格（如：玄幻小说、现代都市等）")
    max_tokens: int = Field(default=500, ge=100, le=2000, description="最大生成token数")


class AIPolishRequest(BaseModel):
    """AI 润色请求"""
    text: str = Field(..., description="待润色的文本", min_length=1)


class AITranslateRequest(BaseModel):
    """AI 翻译请求"""
    text: str = Field(..., description="待翻译的文本", min_length=1)
    target_lang: str = Field(
        default="auto",
        description="目标语言（auto=自动识别/english=英文/chinese=中文）"
    )


class AIExpandRequest(BaseModel):
    """AI 扩写请求"""
    text: str = Field(..., description="待扩写的文本", min_length=1)


class AISummarizeRequest(BaseModel):
    """AI 总结请求"""
    text: str = Field(..., description="待总结的文本", min_length=1)


# ==================== API 路由 ====================

@router.post(
    "/complete",
    summary="AI 续写",
    description="""
    AI 续写功能，支持流式响应。
    
    **请求示例**:
    ```json
    {
      "context": "从前有座山，山里有座庙",
      "prompt": "续写",
      "style": "玄幻小说",
      "max_tokens": 500
    }
    ```
    
    **响应格式** (Server-Sent Events):
    ```
    data: 庙里
    data: 有个
    data: 老和尚
    data: ，这个
    data: 老和尚
    data: 正在
    data: ...
    data: [DONE]
    ```
    
    **错误响应**:
    ```
    data: [ERROR] 错误信息
    ```
    """,
    response_class=StreamingResponse
)
async def ai_complete(
    request: AICompleteRequest,
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db)
):
    """
    AI 续写接口（流式响应）
    
    返回 Server-Sent Events (SSE) 流，前端可以实时接收生成的文本
    """
    logger.info(
        f"[AI续写] 用户: {current_user.username}({current_user.id}), "
        f"上下文长度: {len(request.context)}, "
        f"风格: {request.style or '默认'}"
    )
    
    ai_service = HTTPAIService()
    
    async def event_generator():
        """SSE 事件生成器"""
        try:
            async for chunk in ai_service.stream_complete(
                context=request.context,
                prompt=request.prompt,
                style=request.style,
                max_tokens=request.max_tokens
            ):
                # SSE 格式: data: {content}\n\n
                yield f"data: {chunk}\n\n"
            
            # 流结束标记
            yield "data: [DONE]\n\n"
            logger.info(f"[AI续写] 用户 {current_user.username} 请求完成")
            
        except Exception as e:
            error_msg = str(e)
            logger.error(f"[AI续写] 用户 {current_user.username} 请求失败: {error_msg}")
            yield f"data: [ERROR] {error_msg}\n\n"
    
    return StreamingResponse(
        event_generator(),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
            "X-Accel-Buffering": "no",  # 禁用 Nginx 缓冲
        }
    )


@router.post(
    "/polish",
    summary="AI 润色",
    description="""
    AI 润色功能，优化文字表达，使其更加流畅生动。
    
    **请求示例**:
    ```json
    {
      "text": "他很高兴地说话"
    }
    ```
    
    **响应格式** (SSE):
    ```
    data: 他
    data: 欣喜
    data: 若狂
    data: 地
    data: 说道
    data: [DONE]
    ```
    """,
    response_class=StreamingResponse
)
async def ai_polish(
    request: AIPolishRequest,
    current_user: User = Depends(get_current_active_user)
):
    """AI 润色接口（流式响应）"""
    logger.info(
        f"[AI润色] 用户: {current_user.username}({current_user.id}), "
        f"文本长度: {len(request.text)}"
    )
    
    ai_service = HTTPAIService()
    
    async def event_generator():
        try:
            async for chunk in ai_service.stream_polish(request.text):
                yield f"data: {chunk}\n\n"
            
            yield "data: [DONE]\n\n"
            logger.info(f"[AI润色] 用户 {current_user.username} 请求完成")
            
        except Exception as e:
            error_msg = str(e)
            logger.error(f"[AI润色] 用户 {current_user.username} 请求失败: {error_msg}")
            yield f"data: [ERROR] {error_msg}\n\n"
    
    return StreamingResponse(
        event_generator(),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
        }
    )


@router.post(
    "/translate",
    summary="AI 翻译",
    description="""
    AI 翻译功能，支持中英互译。
    
    **请求示例**:
    ```json
    {
      "text": "你好世界",
      "target_lang": "auto"
    }
    ```
    
    **支持的目标语言**:
    - `auto`: 自动识别（中译英或英译中）
    - `english`: 翻译成英文
    - `chinese`: 翻译成中文
    """,
    response_class=StreamingResponse
)
async def ai_translate(
    request: AITranslateRequest,
    current_user: User = Depends(get_current_active_user)
):
    """AI 翻译接口（流式响应）"""
    logger.info(
        f"[AI翻译] 用户: {current_user.username}({current_user.id}), "
        f"文本长度: {len(request.text)}, "
        f"目标语言: {request.target_lang}"
    )
    
    ai_service = HTTPAIService()
    
    async def event_generator():
        try:
            async for chunk in ai_service.stream_translate(
                request.text,
                request.target_lang
            ):
                yield f"data: {chunk}\n\n"
            
            yield "data: [DONE]\n\n"
            logger.info(f"[AI翻译] 用户 {current_user.username} 请求完成")
            
        except Exception as e:
            error_msg = str(e)
            logger.error(f"[AI翻译] 用户 {current_user.username} 请求失败: {error_msg}")
            yield f"data: [ERROR] {error_msg}\n\n"
    
    return StreamingResponse(
        event_generator(),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
        }
    )


@router.post(
    "/expand",
    summary="AI 扩写",
    description="""
    AI 扩写功能，在保持原意的基础上增加细节描写。
    
    **请求示例**:
    ```json
    {
      "text": "他走进了房间"
    }
    ```
    """,
    response_class=StreamingResponse
)
async def ai_expand(
    request: AIExpandRequest,
    current_user: User = Depends(get_current_active_user)
):
    """AI 扩写接口（流式响应）"""
    logger.info(
        f"[AI扩写] 用户: {current_user.username}({current_user.id}), "
        f"文本长度: {len(request.text)}"
    )
    
    ai_service = HTTPAIService()
    
    async def event_generator():
        try:
            async for chunk in ai_service.stream_expand(request.text):
                yield f"data: {chunk}\n\n"
            
            yield "data: [DONE]\n\n"
            logger.info(f"[AI扩写] 用户 {current_user.username} 请求完成")
            
        except Exception as e:
            error_msg = str(e)
            logger.error(f"[AI扩写] 用户 {current_user.username} 请求失败: {error_msg}")
            yield f"data: [ERROR] {error_msg}\n\n"
    
    return StreamingResponse(
        event_generator(),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
        }
    )


@router.post(
    "/summarize",
    summary="AI 总结",
    description="""
    AI 总结功能，提取核心信息，生成简洁摘要。
    
    **请求示例**:
    ```json
    {
      "text": "很长的一段文本..."
    }
    ```
    """,
    response_class=StreamingResponse
)
async def ai_summarize(
    request: AISummarizeRequest,
    current_user: User = Depends(get_current_active_user)
):
    """AI 总结接口（流式响应）"""
    logger.info(
        f"[AI总结] 用户: {current_user.username}({current_user.id}), "
        f"文本长度: {len(request.text)}"
    )
    
    ai_service = HTTPAIService()
    
    async def event_generator():
        try:
            async for chunk in ai_service.stream_summarize(request.text):
                yield f"data: {chunk}\n\n"
            
            yield "data: [DONE]\n\n"
            logger.info(f"[AI总结] 用户 {current_user.username} 请求完成")
            
        except Exception as e:
            error_msg = str(e)
            logger.error(f"[AI总结] 用户 {current_user.username} 请求失败: {error_msg}")
            yield f"data: [ERROR] {error_msg}\n\n"
    
    return StreamingResponse(
        event_generator(),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
        }
    )


@router.get(
    "/health",
    summary="AI 服务健康检查",
    description="检查 AI 服务是否正常运行"
)
async def ai_health_check():
    """AI 服务健康检查"""
    try:
        ai_service = HTTPAIService()
        return {
            "status": "healthy",
            "service": "OpenAI (HTTP)",
            "base_url": ai_service.base_url,
            "model": ai_service.model
        }
    except Exception as e:
        logger.error(f"AI 服务健康检查失败: {e}")
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail=f"AI 服务不可用: {str(e)}"
        )
