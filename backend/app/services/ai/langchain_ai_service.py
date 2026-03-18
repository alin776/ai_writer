"""
LangChain-based AI Service — HTTPAIService 的 drop-in 替代

使用 langchain_openai.ChatOpenAI 替代 raw httpx SSE 调用。
所有外部接口（方法签名、yield 协议）保持完全一致，业务逻辑直接复用。
"""

import json
import logging
import asyncio
import hashlib
from typing import AsyncGenerator, Optional, Any
from datetime import datetime
from langchain_openai import ChatOpenAI
from langchain_core.messages import SystemMessage, HumanMessage, AIMessage
from app.core.config import settings
from app.services.ai.prompts import get_prompts_manager
from app.services.agent.model_selector import ModelSelector, TaskType
from app.core.request_context import get_request_user_id, get_request_db
from app.utils.datetime_utils import get_utc_now

logger = logging.getLogger(__name__)

# 导入 openai 异常类型（用于精确重试判断）
try:
    from openai import (
        APITimeoutError as _APITimeoutError,
        RateLimitError as _RateLimitError,
        APIStatusError as _APIStatusError,
        APIConnectionError as _APIConnectionError,
    )
except ImportError:
    _APITimeoutError = _RateLimitError = _APIStatusError = _APIConnectionError = None


class LangChainAIService:
    """基于 LangChain ChatOpenAI 的 AI 服务 — HTTPAIService 的 drop-in 替代

    成本追踪（2025-12-01更新）：
    - 使用AILogService持久化成本数据到数据库（ai_call_logs表）
    - 需要传递db和user_id参数才能启用成本追踪
    - 成本会在AI调用完成时自动记录（通过_track_api_cost方法）

    使用示例：
    ```python
    from app.core.database import create_db_session

    async with create_db_session() as db:
        ai_service = LangChainAIService(
            db=db,
            user_id=str(current_user.id)
        )
        async for chunk, usage in ai_service.stream_complete(...):
            yield chunk
    ```
    """

    _warned_non_streaming_no_selector = False
    _warned_non_streaming_no_task_type = False

    def __init__(
        self,
        model: str = None,
        timeout: int = None,
        enable_model_selector: bool = True,
        enable_cost_tracking: bool = True,
        user_id: Optional[str] = None,
        db=None,
    ):
        self.api_key = settings.OPENAI_API_KEY
        self.base_url = settings.OPENAI_BASE_URL
        self.model = model or settings.OPENAI_MODEL
        self.timeout_value = timeout or settings.OPENAI_TIMEOUT
        self.prompts = get_prompts_manager()
        self.db = db

        # 模型选择器和成本追踪
        self.enable_model_selector = enable_model_selector
        self.enable_cost_tracking = enable_cost_tracking
        self.user_id = user_id

        if enable_model_selector:
            self.model_selector = ModelSelector(enable_cost_optimization=True)
            logger.info("ModelSelector 已启用")
        else:
            self.model_selector = None

        # 使用AILogService进行成本追踪
        self.ai_log_service = None
        if enable_cost_tracking and db and user_id:
            from app.services.ai_log_service import AILogService
            self.ai_log_service = AILogService(db)
            logger.info("AILogService 已启用 (用于成本追踪)")
        elif enable_cost_tracking:
            ctx_user = get_request_user_id()
            if ctx_user:
                logger.info("[成本追踪] 初始化未传db/user_id，将使用请求上下文按需记录成本")
            else:
                logger.info("[成本追踪] 初始化未传db/user_id，暂不创建AILogService；_track_api_cost会按需尝试")

        logger.info(
            f"LangChain AI Service 初始化成功，Base URL: {self.base_url}, "
            f"Model: {self.model}, Timeout: {self.timeout_value}s, "
            f"ModelSelector: {enable_model_selector}, CostTracking: {enable_cost_tracking}"
        )

    async def close(self):
        """No-op — ChatOpenAI 自管理连接池"""
        pass

    # ------------------------------------------------------------------ #
    #  辅助方法
    # ------------------------------------------------------------------ #

    @staticmethod
    def _to_langchain_messages(messages: list):
        """dict messages → LangChain message 对象"""
        lc = []
        for m in messages:
            role, content = m["role"], m["content"]
            if role == "system":
                lc.append(SystemMessage(content=content))
            elif role == "user":
                lc.append(HumanMessage(content=content))
            elif role == "assistant":
                lc.append(AIMessage(content=content))
        return lc

    @staticmethod
    def _extract_usage(usage_metadata: dict) -> dict:
        """LangChain usage_metadata → OpenAI 风格 usage dict（含 cache/reasoning 细分）"""
        in_details = usage_metadata.get("input_token_details") or {}
        out_details = usage_metadata.get("output_token_details") or {}
        return {
            "prompt_tokens": usage_metadata.get("input_tokens", 0),
            "completion_tokens": usage_metadata.get("output_tokens", 0),
            "total_tokens": usage_metadata.get("total_tokens", 0),
            "cache_read": in_details.get("cache_read", 0) or 0,
            "cache_creation": in_details.get("cache_creation", 0) or 0,
            "reasoning": out_details.get("reasoning", 0) or 0,
        }

    # ------------------------------------------------------------------ #
    #  核心流式调用（ChatOpenAI.astream 替代 httpx SSE）
    # ------------------------------------------------------------------ #

    async def _stream_chat(
        self,
        messages: list,
        max_tokens: int = 1000,
        temperature: float = 0.7,
        task_type: Optional[TaskType] = None,
        response_format: Optional[dict] = None,
        _allow_response_format_fallback: bool = True,
    ) -> AsyncGenerator[tuple[str, dict | None], None]:
        """
        通用流式聊天方法

        Yields:
            tuple: (文本片段, usage统计或None)
                - 文本片段: str
                - usage: 仅在最后一个块返回完整usage,其他为None
        """
        # ==================== 积分预检查 ====================
        user_id = self.user_id or get_request_user_id()
        from app.core.billing_context import get_billing_context as _get_billing_ctx
        if user_id and self.enable_cost_tracking and not _get_billing_ctx():
            try:
                from app.core.database import create_db_session
                from app.services.credits.credit_service import CreditService
                from app.models.user import User
                from sqlalchemy import select
                from uuid import UUID

                async with create_db_session() as db:
                    user_stmt = select(User).where(User.id == UUID(user_id))
                    user_result = await db.execute(user_stmt)
                    user = user_result.scalar_one_or_none()

                    if user and not user.is_admin:
                        credit_service = CreditService(db)
                        from app.utils.cost_calculator import CostCalculator
                        from app.services.system_config_service import SystemConfigService
                        _precheck_pricing = await SystemConfigService.get_model_pricing(db)
                        estimated_cost_data = CostCalculator.calculate_cost(
                            model_name=self.model,
                            prompt_tokens=len(str(messages)) // 4,
                            completion_tokens=max_tokens,
                            model_pricing=_precheck_pricing,
                        )
                        estimated_credits = estimated_cost_data["total_cost"] * settings.CREDITS_PER_DOLLAR

                        is_sufficient, current_balance = await credit_service.check_sufficient(
                            user_id=UUID(user_id),
                            required_credits=estimated_credits,
                        )

                        if not is_sufficient:
                            logger.warning(
                                f"[积分检查] 用户 {user_id} 余额不足: "
                                f"需要约 {float(estimated_credits):.2f} 积分，当前 {float(current_balance):.2f} 积分"
                            )
                            raise Exception(
                                f"积分余额不足：当前余额 {float(current_balance):.2f}，"
                                f"预计需要 {float(estimated_credits):.2f} 积分。请先充值。"
                            )

                        logger.debug(
                            f"[积分检查] 用户 {user_id} 余额充足: "
                            f"当前 {float(current_balance):.2f} 积分，预计消耗 {float(estimated_credits):.2f} 积分"
                        )

            except Exception as e:
                if "积分余额不足" in str(e):
                    raise
                logger.error(f"[积分检查] 检查失败，继续执行: {type(e).__name__}: {str(e)}")
        # ================================================

        import time
        from app.services.agent.utils.monitoring import increment_counter, record_timer, set_gauge

        llm_start_time = time.time()

        # ==================== 模型选择逻辑 ====================
        if self.model_selector and task_type:
            try:
                selection = self.model_selector.select_model(
                    task_type=task_type,
                    input_tokens=len(str(messages)) // 4,
                    output_tokens=max_tokens,
                )
                model = selection.model.model_id
                logger.info(
                    f"[ModelSelector] ✅ 智能选择成功: "
                    f"task_type={task_type.value}, "
                    f"complexity={selection.complexity.value}, "
                    f"selected_model={model}, "
                    f"default_model={self.model}, "
                    f"reason={selection.reason}"
                )
            except Exception as e:
                logger.warning(
                    f"[ModelSelector] ⚠️ 选择失败，回退到默认模型: "
                    f"error={e}, default_model={self.model}"
                )
                model = self.model
        else:
            model = self.model
            if not self.model_selector:
                logger.warning(f"[ModelSelector] ⚠️ 未启用(model_selector=None)，使用默认模型: {model}")
            elif not task_type:
                logger.warning(f"[ModelSelector] ⚠️ 未传递task_type，使用默认模型: {model}")
        # ======================================================

        # 构建 ChatOpenAI 实例
        llm_kwargs = dict(
            model=model,
            api_key=self.api_key,
            base_url=self.base_url,
            temperature=temperature,
            max_tokens=max_tokens,
            stream_usage=True,
            timeout=self.timeout_value,
        )
        if response_format:
            llm_kwargs["model_kwargs"] = {"response_format": response_format}

        llm = ChatOpenAI(**llm_kwargs)
        lc_messages = self._to_langchain_messages(messages)

        logger.debug(
            f"开始调用 AI API: model={model}, "
            f"max_tokens={max_tokens}, temp={temperature}, task_type={task_type}"
        )

        start_time = get_utc_now()
        cache_key = self._generate_cache_key(messages, model, temperature, max_tokens)

        try:
            chunk_count = 0
            total_content = ""
            usage_info = None

            async for chunk in llm.astream(lc_messages):
                # 提取 usage 信息（通常在最后一个块）
                if chunk.usage_metadata:
                    usage_info = self._extract_usage(chunk.usage_metadata)

                # 提取内容
                content = chunk.content
                if content and not self._should_filter(content):
                    chunk_count += 1
                    total_content += content
                    yield content, None

            logger.debug(
                f"API 响应完成，共接收 {chunk_count} 个数据块，总长度: {len(total_content)}"
            )

            # P1修复: 如果 completion_tokens=0 但有内容，使用 TokenCounter 估算
            if usage_info and usage_info.get("completion_tokens", 0) == 0 and len(total_content) > 0:
                from app.services.context.token_counter import count_tokens

                estimated_completion = count_tokens(total_content, model=model)
                usage_info["completion_tokens"] = estimated_completion
                usage_info["total_tokens"] = usage_info.get("prompt_tokens", 0) + estimated_completion
                logger.warning(
                    "[Token估算] API返回completion_tokens=0，使用TokenCounter估算: "
                    f"{estimated_completion} tokens (内容{len(total_content)}字符)"
                )

            if usage_info:
                logger.debug(
                    "流式响应Token统计: "
                    f"{usage_info.get('total_tokens', 0)} "
                    f"(prompt={usage_info.get('prompt_tokens', 0)}, "
                    f"completion={usage_info.get('completion_tokens', 0)})"
                )

            # 成本追踪
            cost_tracking_result = None
            if self.enable_cost_tracking and usage_info:
                cost_tracking_result = await self._track_api_cost(
                    usage_info=usage_info,
                    task_type=task_type,
                    start_time=start_time,
                    actual_model=model,
                )

            # 监控指标
            if usage_info:
                set_gauge("llm_token_usage_prompt", usage_info.get("prompt_tokens", 0), labels={"model": model})
                set_gauge("llm_token_usage_completion", usage_info.get("completion_tokens", 0), labels={"model": model})
                set_gauge("llm_token_usage_total", usage_info.get("total_tokens", 0), labels={"model": model})

            record_timer("llm_response_time", time.time() - llm_start_time, labels={"model": model})
            increment_counter("llm_calls_success", labels={"model": model})

            # yield 最终的 usage 信息
            if usage_info:
                yield "", usage_info
            else:
                logger.warning("流式响应未返回usage信息")

            # ==================== 空响应自动退款 ====================
            if chunk_count == 0:
                logger.error("警告: AI 响应为空！未接收到任何内容块。")

                if (
                    cost_tracking_result
                    and cost_tracking_result.get("credits_deducted")
                    and not cost_tracking_result.get("is_admin")
                ):
                    try:
                        from app.core.database import create_db_session
                        from app.services.credits.credit_service import CreditService
                        from uuid import UUID

                        credits_to_refund = cost_tracking_result["credits_deducted"]
                        refund_user_id = cost_tracking_result["user_id"]
                        ai_call_log = cost_tracking_result.get("ai_call_log")

                        async with create_db_session() as db:
                            credit_service = CreditService(db)
                            refund_transaction = await credit_service.refund(
                                user_id=UUID(refund_user_id),
                                amount=credits_to_refund,
                                description="AI响应为空，自动退还积分",
                                related_id=ai_call_log.id if ai_call_log else None,
                            )
                            logger.info(
                                f"[自动退款] 用户 {refund_user_id}: 退还 {float(credits_to_refund)} 积分, "
                                f"原因: AI响应为空, "
                                f"余额: {float(refund_transaction.balance_before)} → {float(refund_transaction.balance_after)}"
                            )
                    except Exception as refund_error:
                        logger.error(
                            f"[自动退款] 退款失败! "
                            f"用户={refund_user_id}, "
                            f"金额={float(credits_to_refund)}, "
                            f"ai_call_log_id={ai_call_log.id if ai_call_log else 'None'}, "
                            f"错误={type(refund_error).__name__}: {str(refund_error)}"
                        )
            # ======================================================

        except asyncio.CancelledError:
            logger.info("[LangChainAIService] 流式请求被取消")
            raise

        except Exception as e:
            # response_format 降级重试
            if response_format and _allow_response_format_fallback:
                lower_msg = str(e).lower()
                if any(
                    kw in lower_msg
                    for kw in ["response_format", "json_schema", "json schema", "unknown field", "unsupported"]
                ):
                    logger.warning("[ResponseFormat] 服务不支持 response_format，自动降级重试")
                    async for chunk in self._stream_chat(
                        messages=messages,
                        max_tokens=max_tokens,
                        temperature=temperature,
                        task_type=task_type,
                        response_format=None,
                        _allow_response_format_fallback=False,
                    ):
                        yield chunk
                    return

            increment_counter("llm_calls_error", labels={"model": model, "error_type": type(e).__name__})
            record_timer("llm_response_time", time.time() - llm_start_time, labels={"model": model})
            logger.error(f"AI API 调用错误: {type(e).__name__}: {str(e)}")
            raise

    # ------------------------------------------------------------------ #
    #  业务方法（与 HTTPAIService 完全一致）
    # ------------------------------------------------------------------ #

    async def stream_complete(
        self,
        context: str,
        prompt: str = "续写",
        style: str = "",
        max_tokens: int = 500,
        temperature: float = 0.7,
        work_id: str = None,
        chapter_id: str = None,
        enable_rag: bool = False,
    ) -> AsyncGenerator[tuple[str, dict | None], None]:
        """AI 续写（流式响应）"""
        is_autocomplete = max_tokens <= 150

        if is_autocomplete:
            system_prompt = await self._build_enhanced_autocomplete_prompt(
                work_id, chapter_id, context, enable_rag
            )
            logger.info(f"AI自动补全请求 - 上下文长度: {len(context)}, work_id: {work_id}")
        else:
            system_prompt = self._build_complete_system_prompt(prompt, style)
            logger.info(f"AI续写请求 - 上下文长度: {len(context)}, 风格: {style or '默认'}")

        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": context},
        ]

        task_type = TaskType.SIMPLE_QA if is_autocomplete else TaskType.CONTENT_CREATION

        async for chunk, usage in self._stream_chat(messages, max_tokens, temperature, task_type=task_type):
            yield chunk, usage

    async def stream_polish(
        self,
        text: str,
        max_tokens: int = 1000,
        temperature: float = 0.5,
    ) -> AsyncGenerator[tuple[str, dict | None], None]:
        """AI 润色（流式响应）"""
        system_prompt, user_prefix = self.prompts.get_polish_prompt()

        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": f"{user_prefix}{text}"},
        ]

        logger.info(f"AI Polish request - text length: {len(text)}")

        async for chunk, usage in self._stream_chat(messages, max_tokens, temperature, task_type=TaskType.TEXT_POLISH):
            yield chunk, usage

    async def stream_translate(
        self,
        text: str,
        target_lang: str = "auto",
        max_tokens: int = 1000,
    ) -> AsyncGenerator[tuple[str, dict | None], None]:
        """AI 翻译（流式响应）"""
        system_prompt = self.prompts.get_translate_prompt(target_lang)

        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": text},
        ]

        logger.info(f"AI Translate request - text length: {len(text)}, target: {target_lang}")

        async for chunk, usage in self._stream_chat(messages, max_tokens, temperature=0.3, task_type=TaskType.TRANSLATION):
            yield chunk, usage

    async def stream_expand(
        self,
        text: str,
        max_tokens: int = 1000,
        temperature: float = 0.7,
    ) -> AsyncGenerator[tuple[str, dict | None], None]:
        """AI 扩写（流式响应）"""
        system_prompt, user_prefix = self.prompts.get_expand_prompt()

        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": f"{user_prefix}{text}"},
        ]

        logger.info(f"AI Expand request - text length: {len(text)}")

        async for chunk, usage in self._stream_chat(messages, max_tokens, temperature, task_type=TaskType.TEXT_EXPANSION):
            yield chunk, usage

    async def stream_summarize(
        self,
        text: str,
        max_tokens: int = 100,
        temperature: float = 0.3,
    ) -> AsyncGenerator[tuple[str, dict | None], None]:
        """AI 摘要（流式响应）"""
        system_prompt, user_prefix = self.prompts.get_summarize_prompt()

        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": f"{user_prefix}{text}"},
        ]

        logger.info(f"AI Summarize request - text length: {len(text)}")

        async for chunk, usage in self._stream_chat(messages, max_tokens, temperature, task_type=TaskType.SUMMARIZATION):
            yield chunk, usage

    # ------------------------------------------------------------------ #
    #  非流式调用（ChatOpenAI.ainvoke 替代 httpx POST）
    # ------------------------------------------------------------------ #

    async def call_ai(
        self,
        system_prompt: str,
        user_prompt: str,
        max_tokens: int = 2000,
        temperature: float = 0.7,
        max_retries: int = 3,
        task_type: Optional[TaskType] = None,
    ) -> str:
        """非流式AI调用（用于评审等需要完整响应的场景,带重试机制）"""
        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt},
        ]

        # ==================== 模型选择逻辑 ====================
        if self.model_selector and task_type:
            try:
                selection = self.model_selector.select_model(
                    task_type=task_type,
                    input_tokens=len(str(messages)) // 4,
                    output_tokens=max_tokens,
                )
                model = selection.model.model_id
                logger.info(
                    f"[ModelSelector] ✅ 非流式调用智能选择: "
                    f"task_type={task_type.value}, "
                    f"selected_model={model}, "
                    f"default_model={self.model}"
                )
            except Exception as e:
                logger.warning(
                    f"[ModelSelector] ⚠️ 非流式调用选择失败: error={e}, "
                    f"使用默认模型={self.model}"
                )
                model = self.model
        else:
            model = self.model
            if not self.model_selector:
                if not self.__class__._warned_non_streaming_no_selector:
                    logger.warning(f"[ModelSelector] ⚠️ 非流式调用未启用，使用默认模型: {model}")
                    self.__class__._warned_non_streaming_no_selector = True
                else:
                    logger.debug(f"[ModelSelector] 非流式调用未启用，使用默认模型: {model}")
            elif not task_type:
                if not self.__class__._warned_non_streaming_no_task_type:
                    logger.warning(f"[ModelSelector] ⚠️ 非流式调用未传递task_type，使用默认模型: {model}")
                    self.__class__._warned_non_streaming_no_task_type = True
                else:
                    logger.debug(f"[ModelSelector] 非流式调用未传递task_type，使用默认模型: {model}")
        # ======================================================

        llm = ChatOpenAI(
            model=model,
            api_key=self.api_key,
            base_url=self.base_url,
            temperature=temperature,
            max_tokens=max_tokens,
            timeout=self.timeout_value,
        )
        lc_messages = self._to_langchain_messages(messages)

        start_time = get_utc_now()

        for attempt in range(max_retries):
            try:
                if attempt > 0:
                    wait_time = 2 ** attempt
                    logger.warning(
                        f"AI调用失败,进行第{attempt}次重试 (共{max_retries - 1}次重试机会), "
                        f"等待 {wait_time}秒后重试..."
                    )
                    await asyncio.sleep(wait_time)

                logger.debug(
                    f"开始非流式AI调用: max_tokens={max_tokens}, temp={temperature}, "
                    f"尝试={attempt + 1}/{max_retries}, task_type={task_type}"
                )

                response = await llm.ainvoke(lc_messages)
                content = response.content

                # 提取 usage
                usage_info = None
                if response.usage_metadata:
                    usage_info = self._extract_usage(response.usage_metadata)

                # 成本追踪
                cost_tracking_result = None
                if self.enable_cost_tracking and usage_info:
                    cost_tracking_result = await self._track_api_cost(
                        usage_info=usage_info,
                        task_type=task_type,
                        start_time=start_time,
                        actual_model=model,
                    )

                # 空响应自动退款
                if not content or len(content.strip()) == 0:
                    logger.error("警告: AI 非流式响应为空！")

                    if (
                        cost_tracking_result
                        and cost_tracking_result.get("credits_deducted")
                        and not cost_tracking_result.get("is_admin")
                    ):
                        try:
                            from app.core.database import create_db_session
                            from app.services.credits.credit_service import CreditService
                            from uuid import UUID

                            credits_to_refund = cost_tracking_result["credits_deducted"]
                            refund_user_id = cost_tracking_result["user_id"]
                            ai_call_log = cost_tracking_result.get("ai_call_log")

                            async with create_db_session() as db:
                                credit_service = CreditService(db)
                                refund_transaction = await credit_service.refund(
                                    user_id=UUID(refund_user_id),
                                    amount=credits_to_refund,
                                    description="AI响应为空，自动退还积分",
                                    related_id=ai_call_log.id if ai_call_log else None,
                                )
                                logger.info(
                                    f"[自动退款] 用户 {refund_user_id}: 退还 {float(credits_to_refund)} 积分, "
                                    f"原因: AI非流式响应为空, "
                                    f"余额: {float(refund_transaction.balance_before)} → {float(refund_transaction.balance_after)}"
                                )
                        except Exception as refund_error:
                            logger.error(
                                f"[自动退款] 退款失败! "
                                f"用户={refund_user_id}, "
                                f"金额={float(credits_to_refund)}, "
                                f"ai_call_log_id={ai_call_log.id if ai_call_log else 'None'}, "
                                f"错误={type(refund_error).__name__}: {str(refund_error)}"
                            )

                logger.debug(
                    f"AI响应成功, 长度={len(content) if content else 0}, "
                    f"尝试次数={attempt + 1}"
                )
                return content

            except Exception as e:
                # 判断是否可重试
                is_retryable = False
                if _APITimeoutError and isinstance(e, _APITimeoutError):
                    is_retryable = True
                elif _RateLimitError and isinstance(e, _RateLimitError):
                    is_retryable = True
                elif _APIStatusError and isinstance(e, _APIStatusError):
                    is_retryable = e.status_code >= 500 or e.status_code == 429
                elif _APIConnectionError and isinstance(e, _APIConnectionError):
                    is_retryable = True
                elif isinstance(e, (asyncio.TimeoutError, TimeoutError)):
                    is_retryable = True

                if is_retryable and attempt < max_retries - 1:
                    logger.error(
                        f"AI调用错误 (尝试 {attempt + 1}/{max_retries}): "
                        f"{type(e).__name__}: {str(e)}"
                    )
                    continue

                # 不可重试或已用完重试次数
                if is_retryable:
                    logger.error(f"AI调用失败,已重试{max_retries}次,全部失败")
                    raise Exception(f"网络请求失败,已重试{max_retries}次: {str(e)}")
                raise

        raise Exception(f"AI调用失败,已重试{max_retries}次")

    # ------------------------------------------------------------------ #
    #  工具方法（直接复用 HTTPAIService 逻辑）
    # ------------------------------------------------------------------ #

    def _should_filter(self, content: str) -> bool:
        """判断内容是否应该被过滤"""
        if not content:
            return True
        filter_patterns = ["<think>", "</think>", "<thinking>", "</thinking>"]
        for pattern in filter_patterns:
            if pattern in content.lower():
                return True
        return False

    def _generate_cache_key(
        self,
        messages: list,
        model: str,
        temperature: float,
        max_tokens: int,
    ) -> str:
        """生成缓存键"""
        max_message_length = 10000
        messages_str = json.dumps(messages, sort_keys=True, ensure_ascii=False)

        if len(messages_str) > max_message_length:
            messages_str = messages_str[:max_message_length] + "...[TRUNCATED]"

        key_components = [
            messages_str,
            model,
            f"{temperature:.3f}",
            str(max_tokens),
        ]

        key_string = "|".join(key_components)
        cache_key = hashlib.md5(key_string.encode("utf-8")).hexdigest()
        logger.debug(f"Generated cache key: {cache_key}")
        return cache_key

    # ------------------------------------------------------------------ #
    #  提示词构建方法（直接复用）
    # ------------------------------------------------------------------ #

    def _extract_character_names(self, context: str, guidelines) -> list[str]:
        """从上下文中智能提取人物名"""
        import re

        names = []

        if guidelines and guidelines.protagonist_name:
            protag_name = guidelines.protagonist_name.split("/")[0].strip()
            if protag_name in context:
                names.append(protag_name)
                logger.info(f"[RAG] 检测到主角: {protag_name}")

        pattern = r"([\u4e00-\u9fa5]{2,4})(?:说|道|想|看|听|笑|问|答|走|跑|站|坐|来|去|拿|放)"
        matches = re.findall(pattern, context)

        for match in matches:
            if match not in names:
                names.append(match)
                if len(names) >= 3:
                    break

        logger.info(f"[RAG] 提取到人物名: {names}")
        return names[:3]

    def _should_trigger_rag(self, context: str) -> bool:
        """判断是否需要触发RAG检索"""
        if "\u201c" in context or "\u201d" in context or "\u300c" in context:
            logger.info("[RAG] 检测到对话场景")
            return True

        action_keywords = ["走进", "来到", "看到", "听到", "发现"]
        if any(keyword in context[-100:] for keyword in action_keywords):
            logger.info("[RAG] 检测到动作场景")
            return True

        power_keywords = ["施展", "使用", "释放", "修炼", "境界", "突破", "法术"]
        if any(keyword in context for keyword in power_keywords):
            logger.info("[RAG] 检测到力量体系场景")
            return True

        return False

    def _build_autocomplete_system_prompt(self) -> str:
        """Build autocomplete system prompt from config"""
        return self.prompts.get_autocomplete_prompt()

    async def _build_enhanced_autocomplete_prompt(
        self,
        work_id: str,
        chapter_id: str,
        context: str,
        enable_rag: bool = False,
    ) -> str:
        """构建增强的自动补全提示词（Context-Aware）"""
        base_prompt = self._build_autocomplete_system_prompt()

        if not work_id or not self.db:
            return base_prompt

        enhancements = []
        guidelines = None

        try:
            from uuid import UUID
            from sqlalchemy import select
            from app.models.ai_guidelines import AIGuidelines
            import json as _json

            cache_key = f"guidelines:{work_id}"
            try:
                from app.core.redis import get_redis

                redis = await get_redis()
                cached = await redis.get(cache_key)

                if cached:
                    cached_data = _json.loads(cached)

                    class CachedGuidelines:
                        def __init__(self, data):
                            self.is_active = True
                            for k, v in data.items():
                                setattr(self, k, v)

                    guidelines = CachedGuidelines(cached_data)
                    logger.info("[Cache] 从缓存加载 Guidelines")
            except Exception as cache_error:
                logger.warning(f"[Cache] Redis 缓存读取失败: {cache_error}")

            if not guidelines:
                stmt = select(AIGuidelines).where(AIGuidelines.work_id == UUID(work_id))
                result = await self.db.execute(stmt)
                guidelines = result.scalar_one_or_none()

                if guidelines and guidelines.is_active:
                    try:
                        from app.core.redis import get_redis

                        redis = await get_redis()
                        cache_data = {
                            "writing_style": guidelines.writing_style,
                            "narrative_rhythm": guidelines.narrative_rhythm,
                            "protagonist_name": guidelines.protagonist_name,
                            "protagonist_traits": guidelines.protagonist_traits,
                            "power_system_name": guidelines.power_system_name,
                            "power_levels": guidelines.power_levels,
                            "world_rules": guidelines.world_rules,
                            "content_taboos": guidelines.content_taboos,
                        }
                        await redis.setex(cache_key, 3600, _json.dumps(cache_data, ensure_ascii=False))
                        logger.info("[Cache] Guidelines 已缓存（1小时）")
                    except Exception as cache_error:
                        logger.warning(f"[Cache] Redis 缓存写入失败: {cache_error}")

            if guidelines and (
                hasattr(guidelines, "is_active")
                and guidelines.is_active
                or isinstance(guidelines, type)
                and hasattr(guidelines, "__dict__")
            ):
                metadata_parts = []

                if guidelines.writing_style:
                    metadata_parts.append(f"文笔风格: {guidelines.writing_style}")
                if guidelines.narrative_rhythm:
                    metadata_parts.append(f"叙事节奏: {guidelines.narrative_rhythm}")
                if guidelines.protagonist_name:
                    protag_info = f"主角: {guidelines.protagonist_name}"
                    if guidelines.protagonist_traits:
                        traits = guidelines.protagonist_traits[:100]
                        protag_info += f"({traits})"
                    metadata_parts.append(protag_info)
                if guidelines.power_system_name:
                    power_info = f"力量体系: {guidelines.power_system_name}"
                    if guidelines.power_levels:
                        power_info += f" ({guidelines.power_levels[:80]})"
                    metadata_parts.append(power_info)
                if guidelines.world_rules:
                    metadata_parts.append(f"世界规则: {guidelines.world_rules[:150]}")
                if guidelines.content_taboos:
                    metadata_parts.append(f"禁忌: {guidelines.content_taboos[:100]}")

                if metadata_parts:
                    enhancements.append("【作品设定】\n" + "\n".join(metadata_parts))
                    logger.info(f"[Context-Aware] 已加载 AI Guidelines，{len(metadata_parts)} 项元数据")

        except Exception as e:
            logger.warning(f"[Context-Aware] 加载 AI Guidelines 失败: {e}")

        # 加载章节概要
        if chapter_id:
            try:
                from app.models.chapter import Chapter

                stmt = select(Chapter).where(Chapter.id == UUID(chapter_id))
                result = await self.db.execute(stmt)
                current_chapter = result.scalar_one_or_none()

                if current_chapter and current_chapter.summary:
                    enhancements.append(f"【本章剧情】\n{current_chapter.summary[:200]}")
                    logger.info("[Context-Aware] 已加载当前章节概要")

                    if current_chapter.order > 1:
                        prev_stmt = select(Chapter).where(
                            Chapter.work_id == UUID(work_id),
                            Chapter.order == current_chapter.order - 1,
                        )
                        prev_result = await self.db.execute(prev_stmt)
                        previous_chapter = prev_result.scalar_one_or_none()

                        if previous_chapter and previous_chapter.summary:
                            enhancements.append(f"【上章剧情】\n{previous_chapter.summary[:150]}")
                            logger.info("[Context-Aware] 已加载前一章概要")

            except Exception as e:
                logger.warning(f"[Context-Aware] 加载章节概要失败: {e}")

        # RAG 智能检索
        if enable_rag and work_id and self._should_trigger_rag(context):
            try:
                names = self._extract_character_names(context, guidelines)

                if names:
                    from app.services.vector_store_service import VectorStoreService

                    vector_service = VectorStoreService(self.db)
                    query = f"人物 {' '.join(names)}"
                    logger.info(f"[RAG] 检索查询: {query}")

                    relevant_info = await vector_service.retrieve_relevant_analysis(
                        work_id=work_id,
                        query=query,
                        top_k=2,
                        similarity_threshold=0.3,
                    )

                    if relevant_info:
                        rag_parts = []
                        for item in relevant_info:
                            if "content_text" in item:
                                rag_parts.append(item["content_text"][:150])

                        if rag_parts:
                            enhancements.append("【相关设定】\n" + "\n".join(rag_parts))
                            logger.info(f"[RAG] 已检索到 {len(rag_parts)} 条相关信息")
                    else:
                        logger.info("[RAG] 未检索到相关信息")

            except Exception as e:
                logger.warning(f"[RAG] 检索失败: {e}")

        # 组装最终提示词
        if not enhancements:
            logger.info("[Context-Aware] 未加载到元数据，使用基础提示词")
            return base_prompt

        enhanced_context = "\n\n".join(enhancements)
        if len(enhanced_context) > 800:
            enhanced_context = enhanced_context[:800] + "..."
            logger.info("[Context-Aware] 元数据被截断到800字符")

        final_prompt = f"{base_prompt}\n\n{enhanced_context}"
        logger.info(f"[Context-Aware] 增强提示词构建完成，总长度: {len(final_prompt)}")
        return final_prompt

    def _build_complete_system_prompt(self, prompt: str, style: str) -> str:
        """Build complete (continuation) system prompt from config"""
        return self.prompts.get_complete_prompt(prompt, style)

    # ------------------------------------------------------------------ #
    #  成本追踪（直接复用 HTTPAIService 逻辑）
    # ------------------------------------------------------------------ #

    async def _track_api_cost(
        self,
        usage_info: dict,
        task_type: Optional[TaskType],
        start_time: datetime,
        actual_model: Optional[str] = None,
        db: Optional[Any] = None,
        auto_commit: bool = True,
    ) -> Optional[dict]:
        """追踪API调用成本（使用AILogService）"""
        user_id = self.user_id or get_request_user_id()

        if not user_id:
            logger.debug("[成本追踪] 跳过：缺少user_id（实例和上下文均未设置）")
            return None

        try:
            from app.utils.cost_calculator import CostCalculator
            from app.schemas.ai_call_log import AICallLogCreate
            from app.core.database import create_db_session
            from app.services.ai_log_service import AILogService
            from uuid import UUID

            source = "实例" if self.user_id else "上下文"
            logger.debug(f"[成本追踪] user_id来源: {source}, user_id={user_id}")

            model_to_track = actual_model or self.model
            logger.debug(f"[成本追踪] 记录模型: {model_to_track} (actual_model={actual_model}, self.model={self.model})")

            prompt_tokens = usage_info.get("prompt_tokens", 0)
            completion_tokens = usage_info.get("completion_tokens", 0)
            cache_read = usage_info.get("cache_read", 0)
            cache_creation = usage_info.get("cache_creation", 0)
            reasoning = usage_info.get("reasoning", 0)

            # 从 DB 获取模型定价（带内存缓存）
            from app.services.system_config_service import SystemConfigService
            from app.core.database import create_db_session as _create_pricing_session
            async with _create_pricing_session() as pricing_db:
                model_pricing = await SystemConfigService.get_model_pricing(pricing_db)

            cost_data = CostCalculator.calculate_cost(
                model_name=model_to_track,
                prompt_tokens=prompt_tokens,
                completion_tokens=completion_tokens,
                cache_read=cache_read,
                cache_creation=cache_creation,
                reasoning=reasoning,
                model_pricing=model_pricing,
            )

            duration_ms = int((get_utc_now() - start_time).total_seconds() * 1000)

            log_data = AICallLogCreate(
                user_id=UUID(user_id),
                model_name=model_to_track,
                operation_type=task_type.value if task_type else "unknown",
                prompt_tokens=prompt_tokens,
                completion_tokens=completion_tokens,
                total_tokens=prompt_tokens + completion_tokens,
                cache_read_tokens=cache_read,
                cache_creation_tokens=cache_creation,
                reasoning_tokens=reasoning,
                prompt_cost=cost_data["prompt_cost"],
                completion_cost=cost_data["completion_cost"],
                total_cost=cost_data["total_cost"],
                duration_ms=duration_ms,
                is_success=True,
                extra_data={},
            )

            from contextlib import asynccontextmanager

            @asynccontextmanager
            async def get_db_session():
                effective_db = db if db is not None else self.db
                if effective_db is not None:
                    logger.debug("[成本追踪] 使用外层数据库会话（事务原子性模式）")
                    yield effective_db, False
                else:
                    logger.debug("[成本追踪] 使用独立数据库会话")
                    async with create_db_session() as new_db:
                        yield new_db, True

            ai_call_log = None
            credits_deducted = None
            is_admin_user = False

            async with get_db_session() as (db_session, should_auto_commit):
                temp_log_service = AILogService(db_session)
                ai_call_log = await temp_log_service.create_log(log_data, auto_commit=should_auto_commit)

                # ==================== 聚合计费检查 ====================
                from app.core.billing_context import get_billing_context, record_to_billing_context

                billing_ctx = get_billing_context()
                if billing_ctx is not None:
                    # 批量模式：只记录日志，不扣费，累积到上下文
                    await record_to_billing_context(
                        log_id=str(ai_call_log.id),
                        cost_data=cost_data,
                        usage_info=usage_info,
                        model_name=model_to_track,
                    )
                    logger.debug(
                        f"[成本追踪] 聚合模式：日志已记录，费用累积到 BillingContext "
                        f"(call #{billing_ctx.call_count})"
                    )
                    return {
                        "ai_call_log": ai_call_log,
                        "credits_deducted": None,
                        "user_id": user_id,
                        "is_admin": billing_ctx.is_admin,
                    }

                # ==================== 积分扣除 ====================
                try:
                    from app.services.credits.credit_service import CreditService
                    from app.services.credits.credit_utils import calculate_credits_from_cost
                    from app.services.credits.credit_exceptions import (
                        InsufficientCreditsError,
                        CreditsExpiredError,
                    )
                    from app.models.user import User
                    from sqlalchemy import select

                    user_stmt = select(User).where(User.id == UUID(user_id))
                    user_result = await db_session.execute(user_stmt)
                    user = user_result.scalar_one_or_none()

                    if user:
                        is_admin_user = user.is_admin
                        credit_service = CreditService(db_session)
                        credits_to_deduct = calculate_credits_from_cost(cost_data["total_cost"])

                        transaction = await credit_service.consume(
                            user_id=UUID(user_id),
                            amount=credits_to_deduct,
                            description=f"AI调用: {task_type.value if task_type else 'unknown'}",
                            related_id=ai_call_log.id,
                            skip_check=user.is_admin,
                            auto_commit=should_auto_commit,
                        )

                        if transaction:
                            credits_deducted = credits_to_deduct
                            logger.debug(
                                f"[积分扣除] 用户 {user_id}: 扣除 {float(credits_to_deduct)} 积分, "
                                f"余额: {float(transaction.balance_before)} → {float(transaction.balance_after)}"
                            )
                        else:
                            logger.debug(f"[积分扣除] 管理员 {user_id} 豁免积分扣除")
                    else:
                        logger.warning(f"[积分扣除] 用户 {user_id} 不存在，跳过扣除")

                except InsufficientCreditsError as e:
                    logger.error(
                        f"[积分扣除] 用户 {user_id} 余额不足: "
                        f"需要 {float(e.required)} 积分，当前 {float(e.available)} 积分"
                    )
                    await db_session.rollback()
                    from fastapi import HTTPException

                    raise HTTPException(
                        status_code=402,
                        detail=f"积分余额不足：需要 {float(e.required):.2f} 积分，当前余额 {float(e.available):.2f} 积分。请先充值。",
                    )
                except CreditsExpiredError as e:
                    logger.error(f"[积分扣除] 用户 {user_id} 积分已过期: {e.expired_at}")
                    await db_session.rollback()
                    from fastapi import HTTPException

                    raise HTTPException(
                        status_code=402,
                        detail=f"积分已于 {e.expired_at} 过期，请联系管理员。",
                    )
                except ValueError as e:
                    logger.error(f"[积分扣除] {str(e)}")
                    await db_session.rollback()
                    from fastapi import HTTPException

                    raise HTTPException(
                        status_code=500,
                        detail="积分系统错误：用户积分记录不存在。",
                    )
                except Exception as e:
                    logger.error(f"[积分扣除] 扣除失败: {type(e).__name__}: {str(e)}")
                    logger.warning("[积分扣除] 扣除失败，但AI调用日志已记录")
                # ================================================

            logger.debug(
                f"[AILogService] API调用已记录到数据库 (来源:{source}): "
                f"tokens={prompt_tokens + completion_tokens}, "
                f"cost=${cost_data['total_cost']:.6f}, "
                f"time={duration_ms}ms"
            )

            return {
                "ai_call_log": ai_call_log,
                "credits_deducted": credits_deducted,
                "user_id": user_id,
                "is_admin": is_admin_user,
            }

        except Exception as e:
            logger.error(f"成本追踪失败: {type(e).__name__}: {str(e)}")
            return None
