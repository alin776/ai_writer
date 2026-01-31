"""
AI评价服务

提供AI生成内容的质量评价功能
"""

import json
import logging
from typing import Optional, Dict, Any
from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.models.evaluation_record import EvaluationRecord
from app.models.work import Work
from app.models.chapter import Chapter
from app.schemas.evaluation import (
    EvaluationRequest,
    EvaluationResponse,
    DimensionScores,
    EvaluationContext
)
from app.services.ai.http_ai_service import HTTPAIService
from app.services.ai.evaluation_prompts import (
    get_evaluation_prompt,
    EVALUATION_SYSTEM_PROMPT
)
from app.services.ai.ai_log_middleware import AILogMiddleware
from app.services.agent.model_selector import TaskType  # ✅ 新增：用于成本追踪

logger = logging.getLogger(__name__)


class EvaluationService:
    """AI评价服务"""

    def __init__(self, db: AsyncSession, user_id: UUID):
        """
        初始化评价服务

        Args:
            db: 数据库会话
            user_id: 用户ID
        """
        self.db = db
        self.user_id = user_id

    async def evaluate_text(
        self,
        request: EvaluationRequest,
        model_name: str = "gemini-2.5-flash"
    ) -> EvaluationResponse:
        """
        评价AI生成的文本

        Args:
            request: 评价请求
            model_name: 使用的模型名称

        Returns:
            EvaluationResponse: 评价结果
        """
        logger.info(
            f"开始评价文本, user_id={self.user_id}, "
            f"operation_type={request.operation_type}, "
            f"text_length={len(request.text)}"
        )

        # 1. 创建指定模型的 AI 服务
        # ✅ 2025-12-02: 不传db和user_id，因为本服务使用AILogMiddleware手动追踪
        # 如果传递db和user_id会导致重复记录（HTTPAIService自动追踪 + AILogMiddleware手动追踪）
        http_ai = HTTPAIService(model=model_name, db=None, user_id=None)

        try:
            # 2. 获取上下文信息
            context = await self._get_context(request.context)

            # 3. 生成评价Prompt
            prompt = get_evaluation_prompt(
                text=request.text,
                work_title=context.get("work_title"),
                chapter_title=context.get("chapter_title"),
                previous_text=context.get("previous_text"),
                operation_type=request.operation_type
            )

            # 4. 调用AI进行评价 (使用日志中间件)
            log_middleware = AILogMiddleware(
                db=self.db,
                user_id=self.user_id,
                model_name=model_name
            )

            ai_call_log_id = None
            evaluation_result = None

            async with log_middleware.log_call(
                operation_type="evaluate",
                work_id=context.get("work_id"),
                chapter_id=context.get("chapter_id"),
                extra_data={"operation_type": request.operation_type}
            ) as token_counter:
                # 构造消息
                messages = [
                    {"role": "system", "content": EVALUATION_SYSTEM_PROMPT},
                    {"role": "user", "content": prompt}
                ]

                # 调用AI (非流式)
                result_text = await self._call_ai_non_stream(http_ai, messages)

                # 估算token数 (用于成本计算)
                token_counter.estimate_tokens(
                    prompt_text=EVALUATION_SYSTEM_PROMPT + prompt,
                    completion_text=result_text
                )

                # 解析AI返回的JSON
                evaluation_result = self._parse_evaluation_result(result_text)

            # 获取AI调用日志ID
            ai_call_log_id = token_counter.log_id

        finally:
            # 5. 确保关闭 HTTP 客户端,防止资源泄漏
            await http_ai.close()

        # 6. 保存评价记录
        evaluation_record = await self._save_evaluation_record(
            request=request,
            evaluation_result=evaluation_result,
            context=context,
            ai_call_log_id=ai_call_log_id
        )

        # 7. 构造响应
        response = EvaluationResponse(
            overall_score=evaluation_result["overall_score"],
            dimensions=DimensionScores(**evaluation_result["dimensions"]),
            highlights=evaluation_result.get("highlights", []),
            issues=evaluation_result.get("issues", []),
            suggestions=evaluation_result.get("suggestions", []),
            evaluation_id=evaluation_record.id,
            created_at=evaluation_record.created_at
        )

        logger.info(
            f"评价完成, evaluation_id={evaluation_record.id}, "
            f"overall_score={response.overall_score}"
        )

        return response

    async def _get_context(
        self,
        context: Optional[EvaluationContext]
    ) -> Dict[str, Any]:
        """
        获取评价上下文信息

        Args:
            context: 上下文对象

        Returns:
            包含完整上下文信息的字典
        """
        result = {}

        if not context:
            return result

        # 获取作品信息
        if context.work_id:
            work = await self.db.get(Work, context.work_id)
            if work:
                result["work_id"] = context.work_id
                result["work_title"] = work.title

        # 获取章节信息
        if context.chapter_id:
            chapter = await self.db.get(Chapter, context.chapter_id)
            if chapter:
                result["chapter_id"] = context.chapter_id
                result["chapter_title"] = chapter.title

        # 使用提供的信息覆盖
        if context.work_title:
            result["work_title"] = context.work_title
        if context.chapter_title:
            result["chapter_title"] = context.chapter_title
        if context.previous_text:
            result["previous_text"] = context.previous_text

        return result

    async def _call_ai_non_stream(self, http_ai: HTTPAIService, messages: list) -> str:
        """
        调用AI (非流式)

        Args:
            http_ai: HTTP AI Service 实例
            messages: 消息列表

        Returns:
            AI返回的完整文本
        """
        logger.info("🔄 开始调用AI进行评价...")
        logger.debug(f"📝 消息数量: {len(messages)}, max_tokens: 3500")

        chunks = []
        chunk_count = 0

        async for chunk in http_ai._stream_chat(
            messages=messages,
            max_tokens=3500,  # 增加到3500,确保JSON完整
            temperature=0.3,  # 评价任务用较低温度,保证一致性
            task_type=TaskType.TEXT_CLASSIFICATION  # ✅ 新增：评价是分类任务
        ):
            chunk_count += 1
            # chunk 是 tuple (文本片段, usage统计)
            text_chunk, usage = chunk
            chunks.append(text_chunk)
            logger.debug(f"📦 接收第 {chunk_count} 个数据块, 长度: {len(text_chunk)}")

        result = "".join(chunks)
        logger.info(f"✅ AI调用完成, 共接收 {chunk_count} 个数据块, 总长度: {len(result)} 字符")
        logger.debug(f"📄 AI返回内容前200字符: {result[:200]}")
        logger.debug(f"📄 AI返回内容后200字符: {result[-200:]}")

        return result

    def _parse_evaluation_result(self, result_text: str) -> Dict[str, Any]:
        """
        解析AI返回的评价结果

        Args:
            result_text: AI返回的文本

        Returns:
            解析后的评价结果字典
        """
        logger.info(f"🔍 开始解析AI评价结果, 文本长度: {len(result_text)} 字符")

        # 检测JSON截断
        self._check_json_truncation(result_text)

        try:
            # 尝试直接解析JSON
            logger.debug("📝 尝试直接解析JSON...")
            result = json.loads(result_text)
            logger.info("✅ JSON解析成功 (方法: 直接解析)")

            # 验证必需字段
            required_fields = ["overall_score", "dimensions"]
            for field in required_fields:
                if field not in result:
                    logger.error(f"❌ 缺少必需字段: {field}")
                    raise ValueError(f"缺少必需字段: {field}")

            # 验证维度评分
            required_dimensions = [
                "literary_quality",
                "coherence",
                "creativity",
                "emotional_impact",
                "pacing"
            ]
            for dim in required_dimensions:
                if dim not in result["dimensions"]:
                    logger.error(f"❌ 缺少维度评分: {dim}")
                    raise ValueError(f"缺少维度评分: {dim}")

            logger.info(f"✅ JSON验证通过, overall_score={result['overall_score']}")
            return result

        except json.JSONDecodeError as e:
            logger.warning(f"⚠️ JSON直接解析失败: {e}")
            logger.warning(f"📄 错误位置: line {e.lineno}, column {e.colno}")
            logger.debug(f"📄 原文前500字符:\n{result_text[:500]}")
            logger.debug(f"📄 原文后500字符:\n{result_text[-500:]}")

            # 尝试提取JSON部分
            try:
                logger.info("🔄 尝试提取JSON代码块...")
                # 查找JSON代码块
                if "```json" in result_text:
                    logger.debug("发现 ```json 标记")
                    start = result_text.index("```json") + 7
                    end = result_text.index("```", start)
                    json_text = result_text[start:end].strip()
                    logger.debug(f"提取的JSON长度: {len(json_text)} 字符")
                    result = json.loads(json_text)
                    logger.info("✅ JSON解析成功 (方法: markdown代码块提取)")
                    return result
                elif "{" in result_text and "}" in result_text:
                    logger.debug("发现 { } 标记,尝试提取")
                    start = result_text.index("{")
                    end = result_text.rindex("}") + 1
                    json_text = result_text[start:end]
                    logger.debug(f"提取的JSON长度: {len(json_text)} 字符")
                    logger.debug(f"提取的JSON前100字符: {json_text[:100]}")
                    logger.debug(f"提取的JSON后100字符: {json_text[-100:]}")
                    result = json.loads(json_text)
                    logger.info("✅ JSON解析成功 (方法: 大括号提取)")
                    return result
                else:
                    logger.error("❌ 未找到JSON标记")
            except json.JSONDecodeError as e2:
                logger.error(f"❌ JSON提取后解析失败: {e2}")
                logger.error(f"错误位置: line {e2.lineno}, column {e2.colno}")
            except Exception as e2:
                logger.error(f"❌ JSON提取过程异常: {e2}")

            # 返回默认评价
            logger.warning("⚠️ 使用默认评价结果")
            return self._get_default_evaluation()

        except Exception as e:
            logger.error(f"❌ 评价结果解析异常: {e}")
            logger.exception("详细错误信息:")
            return self._get_default_evaluation()

    def _check_json_truncation(self, text: str) -> None:
        """检查JSON是否可能被截断"""
        if not text:
            logger.error("⚠️ AI返回内容为空!")
            return

        # 检查是否有起始大括号
        if "{" not in text:
            logger.error("⚠️ 未发现JSON起始符号 '{'")
            return

        # 检查是否有结束大括号
        if "}" not in text:
            logger.error("⚠️ 未发现JSON结束符号 '}' - 可能被截断!")
            return

        # 统计大括号数量
        open_braces = text.count("{")
        close_braces = text.count("}")

        if open_braces != close_braces:
            logger.warning(f"⚠️ 大括号不匹配! 开括号: {open_braces}, 闭括号: {close_braces} - JSON可能不完整")

        # 检查是否有未完成的数组
        open_brackets = text.count("[")
        close_brackets = text.count("]")

        if open_brackets != close_brackets:
            logger.warning(f"⚠️ 方括号不匹配! 开括号: {open_brackets}, 闭括号: {close_brackets} - 数组可能不完整")

    def _get_default_evaluation(self) -> Dict[str, Any]:
        """
        获取默认评价结果 (解析失败时使用)

        Returns:
            默认评价结果
        """
        return {
            "overall_score": 70.0,
            "dimensions": {
                "literary_quality": 70.0,
                "coherence": 70.0,
                "creativity": 70.0,
                "emotional_impact": 70.0,
                "pacing": 70.0
            },
            "highlights": ["AI评价解析失败,使用默认评分"],
            "issues": ["无法获取详细评价"],
            "suggestions": ["请重试评价功能"]
        }

    async def _save_evaluation_record(
        self,
        request: EvaluationRequest,
        evaluation_result: Dict[str, Any],
        context: Dict[str, Any],
        ai_call_log_id: Optional[UUID]
    ) -> EvaluationRecord:
        """
        保存评价记录到数据库

        Args:
            request: 评价请求
            evaluation_result: 评价结果
            context: 上下文信息
            ai_call_log_id: AI调用日志ID

        Returns:
            评价记录对象
        """
        # 构造评价详情
        evaluation_details = {
            "highlights": evaluation_result.get("highlights", []),
            "issues": evaluation_result.get("issues", []),
            "suggestions": evaluation_result.get("suggestions", [])
        }

        # 创建评价记录
        record = EvaluationRecord(
            user_id=self.user_id,
            work_id=context.get("work_id"),
            chapter_id=context.get("chapter_id"),
            operation_type=request.operation_type,
            overall_score=evaluation_result["overall_score"],
            dimensions=evaluation_result["dimensions"],
            evaluation_details=evaluation_details,
            ai_call_log_id=ai_call_log_id
        )

        self.db.add(record)
        await self.db.commit()
        await self.db.refresh(record)

        logger.info(f"评价记录已保存: {record.id}")

        return record
