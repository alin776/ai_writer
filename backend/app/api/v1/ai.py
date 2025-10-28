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
from app.services.ai.ai_log_middleware import AILogMiddleware
from app.services.ai.evaluation_service import EvaluationService
from app.services.ai.text_analyzer import TextAnalyzer
from app.services.ai.rewrite_arena_service import get_arena_service
from app.core.config import settings
from app.schemas.evaluation import EvaluationRequest, EvaluationResponse
from app.schemas.text_analysis import (
    TextAnalysisRequest,
    TextAnalysisResult,
    RewriteRequest,
    RewriteResponse,
    ModelResult
)

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


class AISummarizeResponse(BaseModel):
    """AI 总结响应"""
    summary: str = Field(..., description="剧情概括内容")


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
    logger.info(f"[AI续写] context内容: '{request.context[:200]}'")
    logger.info(f"[AI续写] prompt: '{request.prompt}', max_tokens: {request.max_tokens}")

    ai_service = HTTPAIService()

    # 创建日志中间件
    log_middleware = AILogMiddleware(
        db=db,
        user_id=current_user.id,
        model_name=settings.OPENAI_MODEL
    )

    async def event_generator():
        """SSE 事件生成器"""
        accumulated_text = ""
        try:
            # 使用日志中间件记录 AI 调用
            async with log_middleware.log_call(
                operation_type="continue",
                extra_data={
                    "style": request.style,
                    "prompt": request.prompt,
                    "max_tokens": request.max_tokens,
                    "context_length": len(request.context)
                }
            ) as token_counter:
                async for chunk in ai_service.stream_complete(
                    context=request.context,
                    prompt=request.prompt,
                    style=request.style,
                    max_tokens=request.max_tokens
                ):
                    accumulated_text += chunk
                    # SSE 格式: data: {content}\n\n
                    yield f"data: {chunk}\n\n"

                # 估算 token 数量
                token_counter.estimate_tokens(
                    prompt_text=request.context,
                    completion_text=accumulated_text
                )

            # 流结束标记
            yield "data: [DONE]\n\n"
            logger.info(f"[AI续写] 用户 {current_user.username} 请求完成，生成字数: {len(accumulated_text)}")

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
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db)
):
    """AI 润色接口（流式响应）"""
    logger.info(
        f"[AI润色] 用户: {current_user.username}({current_user.id}), "
        f"文本长度: {len(request.text)}"
    )

    ai_service = HTTPAIService()

    # 创建日志中间件
    log_middleware = AILogMiddleware(
        db=db,
        user_id=current_user.id,
        model_name=settings.OPENAI_MODEL
    )

    async def event_generator():
        accumulated_text = ""
        try:
            async with log_middleware.log_call(
                operation_type="polish",
                extra_data={
                    "text_length": len(request.text)
                }
            ) as token_counter:
                async for chunk, usage in ai_service.stream_polish(request.text):
                    # 只处理内容块,忽略最后的usage块(chunk为空字符串)
                    if chunk:
                        accumulated_text += chunk
                        yield f"data: {chunk}\n\n"

                # 估算 token 数量
                token_counter.estimate_tokens(
                    prompt_text=request.text,
                    completion_text=accumulated_text
                )

            yield "data: [DONE]\n\n"
            logger.info(f"[AI润色] 用户 {current_user.username} 请求完成，生成字数: {len(accumulated_text)}")

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
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db)
):
    """AI 翻译接口（流式响应）"""
    logger.info(
        f"[AI翻译] 用户: {current_user.username}({current_user.id}), "
        f"文本长度: {len(request.text)}, "
        f"目标语言: {request.target_lang}"
    )

    ai_service = HTTPAIService()

    # 创建日志中间件
    log_middleware = AILogMiddleware(
        db=db,
        user_id=current_user.id,
        model_name=settings.OPENAI_MODEL
    )

    async def event_generator():
        accumulated_text = ""
        try:
            async with log_middleware.log_call(
                operation_type="translate",
                extra_data={
                    "text_length": len(request.text),
                    "target_lang": request.target_lang
                }
            ) as token_counter:
                async for chunk, usage in ai_service.stream_translate(
                    request.text,
                    request.target_lang
                ):
                    # 只处理内容块,忽略最后的usage块
                    if chunk:
                        accumulated_text += chunk
                        yield f"data: {chunk}\n\n"

                # 估算 token 数量
                token_counter.estimate_tokens(
                    prompt_text=request.text,
                    completion_text=accumulated_text
                )

            yield "data: [DONE]\n\n"
            logger.info(f"[AI翻译] 用户 {current_user.username} 请求完成，生成字数: {len(accumulated_text)}")

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
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db)
):
    """AI 扩写接口（流式响应）"""
    logger.info(
        f"[AI扩写] 用户: {current_user.username}({current_user.id}), "
        f"文本长度: {len(request.text)}"
    )

    ai_service = HTTPAIService()

    # 创建日志中间件
    log_middleware = AILogMiddleware(
        db=db,
        user_id=current_user.id,
        model_name=settings.OPENAI_MODEL
    )

    async def event_generator():
        accumulated_text = ""
        try:
            async with log_middleware.log_call(
                operation_type="expand",
                extra_data={
                    "text_length": len(request.text)
                }
            ) as token_counter:
                async for chunk, usage in ai_service.stream_expand(request.text):
                    # 只处理内容块,忽略最后的usage块
                    if chunk:
                        accumulated_text += chunk
                        yield f"data: {chunk}\n\n"

                # 估算 token 数量
                token_counter.estimate_tokens(
                    prompt_text=request.text,
                    completion_text=accumulated_text
                )

            yield "data: [DONE]\n\n"
            logger.info(f"[AI扩写] 用户 {current_user.username} 请求完成，生成字数: {len(accumulated_text)}")

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
    summary="AI 剧情概括",
    response_model=AISummarizeResponse,
    description="""
    AI 剧情概括功能，提炼章节核心剧情和事件发展。
    
    **请求示例**:
    ```json
    {
      "text": "章节内容..."
    }
    ```
    
    **返回示例**:
    ```json
    {
      "summary": "本章剧情概括内容..."
    }
    ```
    """
)
async def ai_summarize(
    request: AISummarizeRequest,
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db)
) -> AISummarizeResponse:
    """AI 剧情概括接口（返回JSON对象）"""
    logger.info(
        f"[AI剧情概括] 用户: {current_user.username}({current_user.id}), "
        f"文本长度: {len(request.text)}"
    )

    try:
        ai_service = HTTPAIService()

        # 创建日志中间件
        log_middleware = AILogMiddleware(
            db=db,
            user_id=current_user.id,
            model_name=settings.OPENAI_MODEL
        )

        # 调用非流式总结
        summary_text = ""
        async with log_middleware.log_call(
            operation_type="summarize",
            extra_data={
                "text_length": len(request.text)
            }
        ) as token_counter:
            async for chunk, usage in ai_service.stream_summarize(request.text):
                # 只处理内容块,忽略最后的usage块
                if chunk:
                    summary_text += chunk

            # 估算 token 数量
            token_counter.estimate_tokens(
                prompt_text=request.text,
                completion_text=summary_text
            )

        logger.info(f"[AI剧情概括] 用户 {current_user.username} 请求完成，概括长度: {len(summary_text)}")

        return AISummarizeResponse(summary=summary_text)

    except Exception as e:
        error_msg = str(e)
        logger.error(f"[AI剧情概括] 用户 {current_user.username} 请求失败: {error_msg}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"生成剧情概括失败: {error_msg}"
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


# ==================== AI 改写助手路由 ====================

@router.get(
    "/rewrite-arena/models",
    summary="获取可用模型列表",
    description="""
    获取改写助手的可用模型列表。

    **返回示例**:
    ```json
    {
      "models": [
        {
          "id": "gemini-2.5-pro",
          "name": "Gemini 2.5 Pro",
          "description": "擅长创意和细节描写",
          "enabled": true
        },
        {
          "id": "gpt-5",
          "name": "GPT-5",
          "description": "平衡全能，表现稳定",
          "enabled": true
        }
      ],
      "default_models": ["gemini-2.5-pro", "gpt-5"],
      "max_models": 4
    }
    ```
    """
)
async def get_rewrite_models(
    current_user: User = Depends(get_current_active_user)
):
    """获取可用模型列表"""
    logger.info(f"[获取模型列表] 用户: {current_user.username}({current_user.id})")

    # 从配置中获取模型列表
    models = [
        {
            "id": model_id,
            "name": model_info["name"],
            "description": model_info["description"],
            "enabled": model_info["enabled"]
        }
        for model_id, model_info in settings.REWRITE_MODELS.items()
    ]

    return {
        "models": models,
        "default_models": settings.REWRITE_DEFAULT_MODELS,
        "max_models": settings.REWRITE_MAX_MODELS
    }


@router.post(
    "/rewrite-arena/analyze",
    summary="智能分析文本",
    response_model=TextAnalysisResult,
    description="""
    智能分析文本质量，检测问题，给出改写建议。

    **请求示例**:
    ```json
    {
      "text": "主角走进房间，看到了桌子上的剑。",
      "context_before": "经过三天的跋涉，主角终于来到了目的地...",
      "context_after": "他拿起剑，准备离开..."
    }
    ```

    **返回示例**:
    ```json
    {
      "quality_score": 45,
      "issues": [
        {
          "type": "too_simple",
          "severity": "high",
          "description": "描写过于简单"
        }
      ],
      "recommended_mode": "expand",
      "reason": "建议增加细节和情感描写，使画面更生动"
    }
    ```
    """
)
async def analyze_text(
    request: TextAnalysisRequest,
    current_user: User = Depends(get_current_active_user)
) -> TextAnalysisResult:
    """智能分析文本接口"""
    logger.info(
        f"[文本分析] 用户: {current_user.username}({current_user.id}), "
        f"文本长度: {len(request.text)}"
    )

    try:
        analyzer = TextAnalyzer()

        result = await analyzer.analyze_text(
            text=request.text,
            context_before=request.context_before,
            context_after=request.context_after
        )

        await analyzer.close()

        logger.info(
            f"[文本分析] 用户 {current_user.username} 分析完成，"
            f"评分: {result.quality_score}, 推荐模式: {result.recommended_mode}"
        )

        return result

    except Exception as e:
        error_msg = str(e)
        logger.error(f"[文本分析] 用户 {current_user.username} 分析失败: {error_msg}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"文本分析失败: {error_msg}"
        )


@router.post(
    "/rewrite-arena/rewrite",
    summary="多模型改写",
    response_model=RewriteResponse,
    description="""
    使用多个模型并发改写文本，对比不同模型的效果。

    **请求示例**:
    ```json
    {
      "text": "主角走进房间，看到了桌子上的剑。",
      "mode": "expand",
      "context_before": "经过三天的跋涉...",
      "context_after": "他拿起剑...",
      "model_names": ["gemini-2.5-pro", "gpt-5"]
    }
    ```

    **返回示例**:
    ```json
    {
      "original_text": "主角走进房间，看到了桌子上的剑。",
      "mode": "expand",
      "results": [
        {
          "model_name": "gemini-2.5-pro",
          "rewritten_text": "主角推开那扇厚重的木门...",
          "word_count": 156,
          "elapsed_time": 2.3,
          "error": null
        }
      ]
    }
    ```
    """
)
async def rewrite_text(
    request: RewriteRequest,
    current_user: User = Depends(get_current_active_user)
) -> RewriteResponse:
    """多模型改写接口"""
    logger.info(
        f"[多模型改写] 用户: {current_user.username}({current_user.id}), "
        f"文本长度: {len(request.text)}, 模式: {request.mode}"
    )

    try:
        # 获取要使用的模型列表
        if request.model_names:
            # 验证模型数量
            if len(request.model_names) > settings.REWRITE_MAX_MODELS:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"最多只能选择 {settings.REWRITE_MAX_MODELS} 个模型"
                )

            # 验证模型是否启用
            for model_name in request.model_names:
                if model_name not in settings.REWRITE_MODELS:
                    raise HTTPException(
                        status_code=status.HTTP_400_BAD_REQUEST,
                        detail=f"模型 {model_name} 不存在"
                    )
                if not settings.REWRITE_MODELS[model_name]["enabled"]:
                    raise HTTPException(
                        status_code=status.HTTP_400_BAD_REQUEST,
                        detail=f"模型 {model_name} 未启用"
                    )

            model_names = request.model_names
        else:
            # 使用默认模型
            model_names = settings.REWRITE_DEFAULT_MODELS

        logger.info(f"[多模型改写] 使用模型: {model_names}")

        # 获取改写服务
        arena_service = get_arena_service()

        # 并发改写
        results = await arena_service.rewrite_with_multiple_models(
            model_names=model_names,
            text=request.text,
            mode=request.mode,
            custom_requirement=request.custom_requirement,
            context_before=request.context_before,
            context_after=request.context_after
        )

        success_count = sum(1 for r in results if not r.error)
        logger.info(
            f"[多模型改写] 用户 {current_user.username} 改写完成，"
            f"成功: {success_count}/{len(results)}"
        )

        return RewriteResponse(
            original_text=request.text,
            mode=request.mode,
            results=results
        )

    except HTTPException:
        raise
    except Exception as e:
        error_msg = str(e)
        logger.error(f"[多模型改写] 用户 {current_user.username} 改写失败: {error_msg}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"改写失败: {error_msg}"
        )


# ==================== AI 评价功能路由 ====================

@router.post(
    "/evaluate",
    summary="评价AI生成内容",
    response_model=EvaluationResponse,
    description="""
    对AI生成的内容进行专业评价,返回5维度评分和改进建议。

    **评价维度**:
    1. **文学性** (literary_quality) - 语言质量、修辞手法、文字美感
    2. **连贯性** (coherence) - 与前文衔接、逻辑流畅度
    3. **创意性** (creativity) - 新颖度、想象力、打破常规
    4. **情感感染力** (emotional_impact) - 情感表达、读者共鸣度
    5. **节奏把控** (pacing) - 快慢适度、张弛有度

    **请求示例**:
    ```json
    {
      "text": "这是AI生成的一段小说内容...",
      "operation_type": "continue",
      "context": {
        "work_title": "我的小说",
        "chapter_title": "第一章",
        "previous_text": "前文片段..."
      }
    }
    ```

    **返回示例**:
    ```json
    {
      "overall_score": 82.0,
      "dimensions": {
        "literary_quality": 85.0,
        "coherence": 80.0,
        "creativity": 75.0,
        "emotional_impact": 88.0,
        "pacing": 82.0
      },
      "highlights": [
        "语言流畅,文字优美",
        "情感表达细腻,有感染力"
      ],
      "issues": [
        "部分描写过于抽象,缺乏具体细节"
      ],
      "suggestions": [
        "增加感官描写,让场景更生动"
      ],
      "evaluation_id": "770e8400-e29b-41d4-a716-446655440000",
      "created_at": "2025-10-26T14:12:00Z"
    }
    ```
    """
)
async def evaluate_generated_content(
    request: EvaluationRequest,
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db)
) -> EvaluationResponse:
    """评价AI生成内容接口"""
    logger.info(
        f"[AI评价] 用户: {current_user.username}({current_user.id}), "
        f"操作类型: {request.operation_type}, "
        f"文本长度: {len(request.text)}"
    )

    try:
        # 创建评价服务
        evaluation_service = EvaluationService(
            db=db,
            user_id=current_user.id
        )

        # 执行评价 (使用 gemini-2.5-flash - 成本低,速度快)
        result = await evaluation_service.evaluate_text(
            request=request,
            model_name="gemini-2.5-flash"
        )

        logger.info(
            f"[AI评价] 用户 {current_user.username} 评价完成, "
            f"总分: {result.overall_score}, "
            f"评价ID: {result.evaluation_id}"
        )

        return result

    except Exception as e:
        error_msg = str(e)
        logger.error(f"[AI评价] 用户 {current_user.username} 评价失败: {error_msg}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"评价失败: {error_msg}"
        )

