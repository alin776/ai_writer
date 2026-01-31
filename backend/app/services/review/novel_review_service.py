"""
章节评审服务
负责章节级别的评审功能
"""

import json
import re
import logging
from typing import Optional, Dict, Any
from uuid import UUID
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.models.chapter import Chapter
from app.models.review_session import ReviewSession, ReviewLevel, ReviewType
from app.models.ai_call_log import AICallLog
from app.schemas.review import (
    ReviewSessionCreate,
    ReviewSessionResponse,
    DimensionScores
)
from app.prompts.review_prompts import ReviewPromptTemplates
from app.services.ai.http_ai_service import HTTPAIService
from app.services.ai_log_service import AILogService
# 导入 TaskType 用于智能模型选择
from app.services.agent.model_selector import TaskType
from app.services.chapter_content_provider import ChapterContentProvider

logger = logging.getLogger(__name__)


def extract_json_from_response(text: str) -> Dict[str, Any]:
    """
    从 AI 响应中提取 JSON 对象

    使用统一的JSON解析工具,支持多种格式和容错策略。

    Args:
        text: AI 返回的原始文本

    Returns:
        Dict: 解析后的 JSON 对象

    Raises:
        ValueError: 无法提取或解析 JSON
    """
    from app.utils.json_parser import parse_ai_json

    result = parse_ai_json(
        response=text,
        log_prefix="NovelReviewService"
    )

    # 检查是否解析失败
    if "error" in result and result["error"] == "解析失败":
        logger.error(f"JSON解析失败")
        raise ValueError(f"无法解析AI响应为JSON: {result.get('raw_response', '')[:200]}")

    return result


class NovelReviewService:
    """小说评审服务"""

    def __init__(self, db: AsyncSession):
        self.db = db
        # ❌ DEPRECATED - 2025-12-01: 注释掉旧的HTTPAIService初始化
        # self.ai_service = HTTPAIService()

        # ✅ 新增：传递db给HTTPAIService，但user_id需要在调用时传入
        self.ai_service = HTTPAIService(
            db=db,
            user_id=None  # ⚠️ TODO: 需要在review_chapter调用时传入实际user_id
        )
        self.ai_log_service = AILogService(db)
        self.prompts = ReviewPromptTemplates()
        self.content_provider = ChapterContentProvider()

    async def review_chapter(
        self,
        chapter_id: UUID,
        user_id: UUID,
        request: ReviewSessionCreate
    ) -> ReviewSessionResponse:
        """
        评审章节

        Args:
            chapter_id: 章节ID
            user_id: 用户ID
            request: 评审请求

        Returns:
            ReviewSessionResponse: 评审结果
        """
        # 1. 获取章节信息
        chapter = await self._get_chapter(chapter_id)
        if not chapter:
            raise ValueError(f"章节不存在: {chapter_id}")

        logger.info(
            f"[NovelReviewService] 开始评审章节: chapter_id={chapter_id}, "
            f"user_id={user_id}, review_type={request.review_type}"
        )

        # 2. 生成评审提示词
        system_prompt, user_prompt = self.prompts.get_chapter_review_prompt(
            title=chapter.title,
            content=chapter.content
        )

        # 3. 调用 AI 进行评审
        try:
            review_result = await self._call_ai_review(
                system_prompt=system_prompt,
                user_prompt=user_prompt,
                review_type=request.review_type,
                user_id=user_id
            )
        except Exception as e:
            logger.error(f"[NovelReviewService] AI 评审失败: {str(e)}")
            raise

        # 4. 保存评审会话
        session = await self._save_review_session(
            user_id=user_id,
            target_id=chapter_id,
            review_level=ReviewLevel.CHAPTER,
            review_type=request.review_type,
            review_result=review_result,
            word_count=chapter.word_count,
            ai_call_log_id=review_result.get("ai_call_log_id")
        )

        logger.info(
            f"[NovelReviewService] 章节评审完成: session_id={session.id}, "
            f"overall_score={session.overall_score}"
        )

        return ReviewSessionResponse.model_validate(session)

    async def _get_chapter(self, chapter_id: UUID) -> Optional[Chapter]:
        """获取章节"""
        result = await self.db.execute(
            select(Chapter).where(Chapter.id == chapter_id)
        )
        chapter = result.scalar_one_or_none()
        if chapter:
            self.content_provider.hydrate_chapter(chapter)
        return chapter

    async def _call_ai_review(
        self,
        system_prompt: str,
        user_prompt: str,
        review_type: ReviewType,
        user_id: UUID
    ) -> Dict[str, Any]:
        """
        调用 AI 进行评审

        Returns:
            包含评审结果和 ai_call_log_id 的字典
        """
        # 根据评审类型调整参数
        max_tokens = {
            ReviewType.QUICK: 1500,
            ReviewType.STANDARD: 3000,
            ReviewType.DEEP: 5000
        }.get(review_type, 3000)

        temperature = {
            ReviewType.QUICK: 0.5,
            ReviewType.STANDARD: 0.7,
            ReviewType.DEEP: 0.7
        }.get(review_type, 0.7)

        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ]

        # 记录 AI 调用日志 (开始)
        ai_log_id = await self.ai_log_service.log_ai_call_start(
            user_id=user_id,
            operation="chapter_review",
            prompt_text=user_prompt,
            model_name=self.ai_service.model
        )

        try:
            # 调用 AI (非流式)
            full_response = ""
            last_usage = None  # 保存最后的 usage 数据
            async for chunk in self.ai_service._stream_chat(
                messages=messages,
                max_tokens=max_tokens,
                temperature=temperature,
                task_type=TaskType.DEEP_ANALYSIS  # 启用智能模型选择
            ):
                # chunk 是 tuple (文本片段, usage统计)
                text_chunk, usage = chunk
                full_response += text_chunk
                # 保存 usage（最后一个块包含完整的 usage 数据）
                if usage is not None:
                    last_usage = usage

            logger.info(f"[NovelReviewService] AI 响应长度: {len(full_response)} 字符")
            logger.debug(f"[NovelReviewService] AI 响应前200字符: {full_response[:200]}")

            # 使用智能提取函数解析 JSON 响应
            review_data = extract_json_from_response(full_response)

            logger.info(f"[NovelReviewService] JSON 解析成功,总分: {review_data.get('overall_score')}")

            # 提取真实的 token 数据
            prompt_tokens = last_usage.get("prompt_tokens", 0) if last_usage else 0
            completion_tokens = last_usage.get("completion_tokens", 0) if last_usage else 0

            # 记录成功的调用
            await self.ai_log_service.log_ai_call_success(
                log_id=ai_log_id,
                response_text=full_response,
                prompt_tokens=prompt_tokens,
                completion_tokens=completion_tokens
            )

            # 返回结果
            return {
                **review_data,
                "ai_call_log_id": ai_log_id
            }

        except (json.JSONDecodeError, ValueError) as e:
            logger.error(f"[NovelReviewService] JSON 解析失败: {str(e)}")
            logger.error(f"[NovelReviewService] 原始响应: {full_response[:500]}")
            await self.ai_log_service.log_ai_call_error(
                log_id=ai_log_id,
                error_message=f"JSON解析失败: {str(e)}"
            )
            raise ValueError(f"AI 返回的评审结果格式错误: {str(e)}")

        except Exception as e:
            logger.error(f"[NovelReviewService] AI 调用失败: {str(e)}")
            await self.ai_log_service.log_ai_call_error(
                log_id=ai_log_id,
                error_message=str(e)
            )
            raise

    async def _save_review_session(
        self,
        user_id: UUID,
        target_id: UUID,
        review_level: ReviewLevel,
        review_type: ReviewType,
        review_result: Dict[str, Any],
        word_count: int,
        ai_call_log_id: Optional[UUID] = None
    ) -> ReviewSession:
        """保存评审会话"""

        # 提取评审结果
        overall_score = review_result.get("overall_score")
        dimension_scores = review_result.get("dimension_scores", {})
        highlights = review_result.get("highlights", [])
        issues = review_result.get("issues", [])
        suggestions = review_result.get("suggestions", [])

        # 创建会话
        session = ReviewSession(
            user_id=user_id,
            review_level=review_level,
            target_id=target_id,
            overall_score=overall_score,
            dimension_scores=dimension_scores,
            highlights=highlights,
            issues=issues,
            suggestions=suggestions,
            word_count=word_count,
            review_type=review_type,
            ai_model=self.ai_service.model,
            ai_call_log_id=ai_call_log_id
        )

        self.db.add(session)
        await self.db.commit()
        await self.db.refresh(session)

        return session

    async def get_review_session(self, session_id: UUID) -> Optional[ReviewSession]:
        """获取评审会话"""
        result = await self.db.execute(
            select(ReviewSession).where(ReviewSession.id == session_id)
        )
        return result.scalar_one_or_none()

    async def get_chapter_review_history(
        self,
        chapter_id: UUID,
        skip: int = 0,
        limit: int = 10
    ) -> list[ReviewSession]:
        """获取章节的评审历史"""
        result = await self.db.execute(
            select(ReviewSession)
            .where(
                ReviewSession.review_level == ReviewLevel.CHAPTER,
                ReviewSession.target_id == chapter_id
            )
            .order_by(ReviewSession.created_at.desc())
            .offset(skip)
            .limit(limit)
        )
        return list(result.scalars().all())
