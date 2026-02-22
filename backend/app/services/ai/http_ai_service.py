"""
HTTP-based AI Service (Bypass Cloudflare blocking)

Direct httpx calls to OpenAI API, not using openai-python SDK
"""

import httpx
import json
import logging
import asyncio
import hashlib
from typing import AsyncGenerator, Optional, Any
from datetime import datetime
from app.core.config import settings
from app.services.ai.prompts import get_prompts_manager
from app.services.agent.model_selector import ModelSelector, TaskType
from ..agent.utils.llm_optimizer import get_llm_optimizer, optimized_llm_call
# ✅ 2025-12-01: 支持从请求上下文获取user_id（用于全局Agent成本追踪）
from app.core.request_context import get_request_user_id, get_request_db
from app.utils.datetime_utils import get_utc_now

logger = logging.getLogger(__name__)

# HTTP/2 is optional; gracefully disable if the h2 package is missing
try:
    import h2  # type: ignore  # noqa: F401
    _http2_supported = True
except ImportError:
    _http2_supported = False
    logger.warning("HTTP/2 support disabled: install 'h2' via `pip install httpx[http2]` to enable it.")


class HTTPAIService:
    """基于 HTTP 的 AI 服务 - 直接调用 API 绕过 Cloudflare

    成本追踪（2025-12-01更新）：
    - 使用AILogService持久化成本数据到数据库（ai_call_logs表）
    - 需要传递db和user_id参数才能启用成本追踪
    - 成本会在AI调用完成时自动记录（通过_track_api_cost方法）

    使用示例：
    ```python
    from app.core.database import create_db_session

    async with create_db_session() as db:
        ai_service = HTTPAIService(
            db=db,
            user_id=str(current_user.id)
        )
        # AI调用会自动记录成本到数据库
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
        db = None
    ):
        """Initialize HTTP client and prompts manager

        Args:
            model: 指定模型名称,如果不提供则使用默认配置
            timeout: 超时时间(秒),如果不提供则使用默认配置
            enable_model_selector: 是否启用智能模型选择 (默认True)
            enable_cost_tracking: 是否启用成本追踪 (默认True)
            user_id: 用户ID（⚠️ 成本追踪必需）
            db: 数据库会话（⚠️ 成本追踪必需，同时用于Context-Aware补全）
        """
        self.api_key = settings.OPENAI_API_KEY
        self.base_url = settings.OPENAI_BASE_URL
        self.model = model or settings.OPENAI_MODEL  # 支持自定义模型
        timeout_value = timeout or settings.OPENAI_TIMEOUT  # 支持自定义超时
        self.prompts = get_prompts_manager()
        self.db = db  # 保存数据库会话

        # Week 7: 模型选择器和成本追踪
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
            # 允许依赖请求上下文 + 临时db会话进行追踪，避免误报“不会记录”
            ctx_user = get_request_user_id()
            if ctx_user:
                logger.info("[成本追踪] 初始化未传db/user_id，将使用请求上下文按需记录成本")
            else:
                logger.info("[成本追踪] 初始化未传db/user_id，暂不创建AILogService；_track_api_cost会按需尝试")

        # 创建持久化客户端，模拟普通浏览器/应用
        # 流式场景容易超过总超时，单独放宽读超时以避免长响应被误判为超时
        self.client = httpx.AsyncClient(
            headers={
                "User-Agent": "okhttp/4.12.0",
                "Accept": "application/json",
                "Accept-Encoding": "gzip, deflate",
                "Connection": "keep-alive",
            },
            timeout=httpx.Timeout(
                connect=10.0,
                read=None,             # 流式读取不设超时，避免长生成被截断
                write=timeout_value,   # 发送请求体受配置超时限制
                pool=timeout_value     # httpx 要求四项都明确设置
            ),
            follow_redirects=True,
            http2=_http2_supported,  # 启用 HTTP/2（若缺少 h2 库则自动降级）
            limits=httpx.Limits(
                max_connections=20,           # 最大连接数
                max_keepalive_connections=10  # 保持活动连接数（支持连接复用）
            ),
        )

        logger.info(
            f"HTTP AI Service 初始化成功，Base URL: {self.base_url}, "
            f"Model: {self.model}, Timeout: {timeout_value}s, "
            f"HTTP/2: Enabled (多路复用), "
            f"ModelSelector: {enable_model_selector}, CostTracking: {enable_cost_tracking}"
        )
    
    async def close(self):
        """关闭 HTTP 客户端"""
        await self.client.aclose()
    
    async def _stream_chat(
        self,
        messages: list,
        max_tokens: int = 1000,
        temperature: float = 0.7,
        task_type: Optional[TaskType] = None,
        response_format: Optional[dict] = None,
        _allow_response_format_fallback: bool = True
    ) -> AsyncGenerator[tuple[str, dict | None], None]:
        """
        通用流式聊天方法

        Args:
            messages: 消息列表
            max_tokens: 最大token数
            temperature: 温度参数
            task_type: 任务类型 (用于模型选择和成本追踪)

        Yields:
            tuple: (文本片段, usage统计或None)
                - 文本片段: str
                - usage: 仅在最后一个块返回完整usage,其他为None
        """
        # ==================== 积分预检查 ====================
        # 在AI调用前检查用户积分余额（管理员豁免）
        user_id = self.user_id or get_request_user_id()
        if user_id and self.enable_cost_tracking:
            try:
                from app.core.database import create_db_session
                from app.services.credits.credit_service import CreditService
                from app.models.user import User
                from sqlalchemy import select
                from uuid import UUID

                async with create_db_session() as db:
                    # 查询用户信息
                    user_stmt = select(User).where(User.id == UUID(user_id))
                    user_result = await db.execute(user_stmt)
                    user = user_result.scalar_one_or_none()

                    if user and not user.is_admin:
                        # 非管理员需要检查余额
                        credit_service = CreditService(db)

                        # 粗略估算需要的积分（基于max_tokens）
                        from app.utils.cost_calculator import CostCalculator
                        # 使用当前模型的定价估算最大成本
                        estimated_cost_data = CostCalculator.calculate_cost(
                            model_name=self.model,
                            prompt_tokens=len(str(messages)) // 4,  # 粗略估算
                            completion_tokens=max_tokens  # 使用最大值
                        )
                        estimated_credits = estimated_cost_data["total_cost"] * settings.CREDITS_PER_DOLLAR  # 转换为积分

                        # 检查余额是否充足
                        is_sufficient, current_balance = await credit_service.check_sufficient(
                            user_id=UUID(user_id),
                            required_credits=estimated_credits
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
                # 如果是我们抛出的余额不足异常，直接传递
                if "积分余额不足" in str(e):
                    raise
                # 其他检查失败不影响调用（降级处理）
                logger.error(f"[积分检查] 检查失败，继续执行: {type(e).__name__}: {str(e)}")
        # ================================================

        # 🔧 监控：导入监控工具
        import time
        from app.services.agent.utils.monitoring import increment_counter, record_timer, set_gauge

        # 🔧 监控：记录LLM调用开始时间
        llm_start_time = time.time()

        # ==================== 模型选择逻辑 ====================
        # 根据task_type智能选择模型
        # ✅ 2025-12-18: 增强日志，清晰追踪模型选择过程
        if self.model_selector and task_type:
            try:
                # 使用ModelSelector智能选择
                selection = self.model_selector.select_model(
                    task_type=task_type,
                    input_tokens=len(str(messages)) // 4,  # 粗略估算
                    output_tokens=max_tokens
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
            # 使用默认模型
            model = self.model
            if not self.model_selector:
                logger.warning(
                    f"[ModelSelector] ⚠️ 未启用(model_selector=None)，使用默认模型: {model}"
                )
            elif not task_type:
                logger.warning(
                    f"[ModelSelector] ⚠️ 未传递task_type，使用默认模型: {model}"
                )
        # ======================================================

        url = f"{self.base_url}/chat/completions"
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }

        payload = {
            "model": model,  # ← 使用动态选择的模型
            "messages": messages,
            "temperature": temperature,
            "max_tokens": max_tokens,
            "stream": True
        }
        if response_format:
            payload["response_format"] = response_format

        logger.debug(
            f"开始调用 AI API: model={model}, "  # ← 记录实际模型
            f"max_tokens={max_tokens}, temp={temperature}, task_type={task_type}"
        )

        # 记录开始时间 (用于成本追踪)
        start_time = get_utc_now()

        # Week 10: 添加缓存索引键生成
        cache_key = self._generate_cache_key(messages, model, temperature, max_tokens)  # ← 使用model而不是self.model

        try:
            async with self.client.stream("POST", url, json=payload, headers=headers) as response:
                if response.status_code != 200:
                    error_text = await response.aread()
                    error_msg = error_text.decode('utf-8', errors='ignore')[:500]
                    logger.error(f"API 错误: {response.status_code}, {error_msg}")
                    if response_format and _allow_response_format_fallback and response.status_code in (400, 422):
                        lower_msg = error_msg.lower()
                        if (
                            "response_format" in lower_msg
                            or "json_schema" in lower_msg
                            or "json schema" in lower_msg
                            or "unknown field" in lower_msg
                            or "unsupported" in lower_msg
                        ):
                            logger.warning(
                                "[ResponseFormat] 服务不支持 response_format，自动降级重试"
                            )
                            async for chunk in self._stream_chat(
                                messages=messages,
                                max_tokens=max_tokens,
                                temperature=temperature,
                                task_type=task_type,
                                response_format=None,
                                _allow_response_format_fallback=False
                            ):
                                yield chunk
                            return
                    raise Exception(f"API 请求失败: {response.status_code}, {error_msg}")

                logger.debug("API 流式响应已建立，开始接收数据...")
                chunk_count = 0
                total_content = ""
                usage_info = None  # 用于存储最终的usage信息

                try:
                    async for line in response.aiter_lines():
                        line = line.strip()

                        # SSE 格式: data: {...}
                        if not line or not line.startswith("data: "):
                            continue

                        # 移除 "data: " 前缀
                        data_str = line[6:]

                        # 结束标记
                        if data_str == "[DONE]":
                            logger.debug(
                                f"API 响应完成，共接收 {chunk_count} 个数据块，总长度: {len(total_content)}"
                            )

                            # P1修复: 如果 completion_tokens=0 但有内容，使用 TokenCounter 估算
                            if usage_info and usage_info.get('completion_tokens', 0) == 0 and len(total_content) > 0:
                                from app.services.context.token_counter import count_tokens
                                # TokenCounter 策略: tiktoken精确(100%) > 中文优化(95%) > 简单估算(75%)
                                estimated_completion = count_tokens(total_content, model=model)
                                usage_info['completion_tokens'] = estimated_completion
                                usage_info['total_tokens'] = usage_info.get('prompt_tokens', 0) + estimated_completion
                                logger.warning(
                                    "[Token估算] API返回completion_tokens=0，使用TokenCounter估算: "
                                    f"{estimated_completion} tokens (内容{len(total_content)}字符)"
                                )

                            # 记录usage统计
                            if usage_info:
                                logger.debug(
                                    "流式响应Token统计: "
                                    f"{usage_info.get('total_tokens', 0)} "
                                    f"(prompt={usage_info.get('prompt_tokens', 0)}, "
                                    f"completion={usage_info.get('completion_tokens', 0)})"
                                )
                            break

                        try:
                            data = json.loads(data_str)

                            # 提取usage信息(通常在最后一个块)
                            if "usage" in data:
                                usage_info = data["usage"]

                            # 提取内容
                            if "choices" in data and len(data["choices"]) > 0:
                                choice = data["choices"][0]

                                if "delta" in choice and "content" in choice["delta"]:
                                    content = choice["delta"]["content"]

                                    # 修复: Gemini API 第一个块的 content 可能是 null
                                    if content is not None and content and not self._should_filter(content):
                                        chunk_count += 1
                                        total_content += content
                                        # ✅ 真流式输出：AI返回什么立即yield什么，不拆分不延迟
                                        # 显示节奏由前端控制，后端保持高效传输
                                        yield content, None

                        except json.JSONDecodeError as e:
                            logger.warning(f"JSON 解析错误: {e}, 数据: {data_str[:100]}")
                            continue
                except asyncio.CancelledError:
                    logger.info("[HTTPAIService] 流式请求被取消，关闭连接")
                    try:
                        await response.aclose()
                    except Exception:
                        pass
                    raise

                # Week 7: 追踪成本
                # ✅ 2025-12-01: 移除ai_log_service检查（现在使用独立db session）
                # ✅ 2025-12-15: 保存追踪结果用于空响应退款
                # ✅ 2025-12-18: 传递实际使用的模型（ModelSelector选择的）
                cost_tracking_result = None
                if self.enable_cost_tracking and usage_info:
                    cost_tracking_result = await self._track_api_cost(
                        usage_info=usage_info,
                        task_type=task_type,
                        start_time=start_time,
                        actual_model=model  # ✅ 传递 ModelSelector 动态选择的模型
                    )

                # 🔧 监控：记录Token使用
                if usage_info:
                    set_gauge("llm_token_usage_prompt", usage_info.get("prompt_tokens", 0), labels={"model": model})
                    set_gauge("llm_token_usage_completion", usage_info.get("completion_tokens", 0), labels={"model": model})
                    set_gauge("llm_token_usage_total", usage_info.get("total_tokens", 0), labels={"model": model})

                # 🔧 监控：记录响应时间和成功
                record_timer("llm_response_time", time.time() - llm_start_time, labels={"model": model})
                increment_counter("llm_calls_success", labels={"model": model})

                # 循环结束后,yield最终的usage信息
                if usage_info:
                    yield "", usage_info  # 空内容块 + 完整usage统计
                else:
                    logger.warning("流式响应未返回usage信息")

                # ==================== 空响应自动退款 ====================
                # ✅ 2025-12-15: 如果 AI 响应为空但已扣费，自动退还积分
                if chunk_count == 0:
                    logger.error(f"警告: AI 响应为空！未接收到任何内容块。")

                    # 检查是否有扣费记录且非管理员
                    if (cost_tracking_result
                        and cost_tracking_result.get("credits_deducted")
                        and not cost_tracking_result.get("is_admin")):

                        try:
                            from app.core.database import create_db_session
                            from app.services.credits.credit_service import CreditService
                            from uuid import UUID

                            credits_to_refund = cost_tracking_result["credits_deducted"]
                            refund_user_id = cost_tracking_result["user_id"]
                            ai_call_log = cost_tracking_result.get("ai_call_log")

                            async with create_db_session() as db:
                                credit_service = CreditService(db)

                                # 执行退款
                                refund_transaction = await credit_service.refund(
                                    user_id=UUID(refund_user_id),
                                    amount=credits_to_refund,
                                    description="AI响应为空，自动退还积分",
                                    related_id=ai_call_log.id if ai_call_log else None
                                )

                                logger.info(
                                    f"[自动退款] 用户 {refund_user_id}: 退还 {float(credits_to_refund)} 积分, "
                                    f"原因: AI响应为空, "
                                    f"余额: {float(refund_transaction.balance_before)} → {float(refund_transaction.balance_after)}"
                                )

                        except Exception as refund_error:
                            # ⚠️ 退款失败时记录完整信息，便于手动补偿
                            logger.error(
                                f"[自动退款] 退款失败! "
                                f"用户={refund_user_id}, "
                                f"金额={float(credits_to_refund)}, "
                                f"ai_call_log_id={ai_call_log.id if ai_call_log else 'None'}, "
                                f"错误={type(refund_error).__name__}: {str(refund_error)}"
                            )
                # ======================================================

        except httpx.HTTPError as e:
            # 🔧 监控：记录HTTP错误
            increment_counter("llm_calls_error", labels={"model": model, "error_type": "HTTPError"})
            record_timer("llm_response_time", time.time() - llm_start_time, labels={"model": model})

            logger.error(f"HTTP 请求错误: {type(e).__name__}: {str(e)}")
            raise Exception(f"网络请求失败: {str(e)}")

        except Exception as e:
            # 🔧 监控：记录其他错误
            increment_counter("llm_calls_error", labels={"model": model, "error_type": type(e).__name__})
            record_timer("llm_response_time", time.time() - llm_start_time, labels={"model": model})

            logger.error(f"AI API 调用错误: {type(e).__name__}: {str(e)}")
            raise
    
    async def stream_complete(
        self,
        context: str,
        prompt: str = "续写",
        style: str = "",
        max_tokens: int = 500,
        temperature: float = 0.7,
        # ===== Context-Aware 元数据参数 =====
        work_id: str = None,
        chapter_id: str = None,
        enable_rag: bool = False
    ) -> AsyncGenerator[tuple[str, dict | None], None]:
        """AI 续写（流式响应）

        Args:
            context: 上下文文本
            prompt: 续写提示
            style: 写作风格
            max_tokens: 最大token数
            temperature: 温度参数
            work_id: 作品ID（用于加载元数据）
            chapter_id: 章节ID（用于加载章节概要）
            enable_rag: 是否启用RAG检索

        Yields:
            tuple: (文本片段, usage统计或None)
        """
        # 区分自动补全和正式续写
        is_autocomplete = max_tokens <= 150

        if is_autocomplete:
            # ===== 使用增强的自动补全提示词 =====
            system_prompt = await self._build_enhanced_autocomplete_prompt(
                work_id, chapter_id, context, enable_rag
            )
            logger.info(f"AI自动补全请求 - 上下文长度: {len(context)}, work_id: {work_id}")
        else:
            system_prompt = self._build_complete_system_prompt(prompt, style)
            logger.info(f"AI续写请求 - 上下文长度: {len(context)}, 风格: {style or '默认'}")

        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": context}
        ]

        # P0修复: 根据任务类型选择合适的模型
        # 自动补全(短文本)用简单模型，正式续写用内容创作模型
        task_type = TaskType.SIMPLE_QA if is_autocomplete else TaskType.CONTENT_CREATION

        async for chunk, usage in self._stream_chat(messages, max_tokens, temperature, task_type=task_type):
            yield chunk, usage
    
    async def stream_polish(
        self,
        text: str,
        max_tokens: int = 1000,
        temperature: float = 0.5
    ) -> AsyncGenerator[tuple[str, dict | None], None]:
        """AI Polish (streaming response)

        Yields:
            tuple: (文本片段, usage统计或None)
        """
        system_prompt, user_prefix = self.prompts.get_polish_prompt()

        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": f"{user_prefix}{text}"}
        ]

        logger.info(f"AI Polish request - text length: {len(text)}")

        # 传递task_type以正确记录operation_type
        async for chunk, usage in self._stream_chat(
            messages,
            max_tokens,
            temperature,
            task_type=TaskType.TEXT_POLISH
        ):
            yield chunk, usage
    
    async def stream_translate(
        self,
        text: str,
        target_lang: str = "auto",
        max_tokens: int = 1000
    ) -> AsyncGenerator[tuple[str, dict | None], None]:
        """AI Translate (streaming response)

        Yields:
            tuple: (文本片段, usage统计或None)
        """
        system_prompt = self.prompts.get_translate_prompt(target_lang)

        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": text}
        ]

        logger.info(f"AI Translate request - text length: {len(text)}, target: {target_lang}")

        # 传递task_type以正确记录operation_type
        async for chunk, usage in self._stream_chat(
            messages,
            max_tokens,
            temperature=0.3,
            task_type=TaskType.TRANSLATION
        ):
            yield chunk, usage
    
    async def stream_expand(
        self,
        text: str,
        max_tokens: int = 1000,
        temperature: float = 0.7
    ) -> AsyncGenerator[tuple[str, dict | None], None]:
        """AI Expand (streaming response)

        Yields:
            tuple: (文本片段, usage统计或None)
        """
        system_prompt, user_prefix = self.prompts.get_expand_prompt()

        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": f"{user_prefix}{text}"}
        ]

        logger.info(f"AI Expand request - text length: {len(text)}")

        # 传递task_type以正确记录operation_type
        async for chunk, usage in self._stream_chat(
            messages,
            max_tokens,
            temperature,
            task_type=TaskType.TEXT_EXPANSION
        ):
            yield chunk, usage

    async def stream_summarize(
        self,
        text: str,
        max_tokens: int = 100,
        temperature: float = 0.3
    ) -> AsyncGenerator[tuple[str, dict | None], None]:
        """AI Summarize (streaming response) - 简短概括主要事件

        Yields:
            tuple: (文本片段, usage统计或None)
        """
        system_prompt, user_prefix = self.prompts.get_summarize_prompt()

        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": f"{user_prefix}{text}"}
        ]

        logger.info(f"AI Summarize request - text length: {len(text)}")

        # 传递task_type以正确记录operation_type
        async for chunk, usage in self._stream_chat(
            messages,
            max_tokens,
            temperature,
            task_type=TaskType.SUMMARIZATION
        ):
            yield chunk, usage
    
    def _extract_character_names(self, context: str, guidelines) -> list[str]:
        """从上下文中智能提取人物名

        Args:
            context: 用户输入的文本
            guidelines: AI创作规范（用于获取主角名）

        Returns:
            提取的人物名列表（最多3个）
        """
        import re
        names = []

        # 1. 优先使用主角名（从 guidelines 获取）
        if guidelines and guidelines.protagonist_name:
            # 处理 "张三/小张" 格式，取第一个名字
            protag_name = guidelines.protagonist_name.split('/')[0].strip()
            if protag_name in context:
                names.append(protag_name)
                logger.info(f"[RAG] 检测到主角: {protag_name}")

        # 2. 正则匹配人名模式（中文人名 + 动作词）
        pattern = r'([\u4e00-\u9fa5]{2,4})(?:说|道|想|看|听|笑|问|答|走|跑|站|坐|来|去|拿|放)'
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
        # 1. 对话场景
        if '"' in context or '"' in context or '「' in context:
            logger.info("[RAG] 检测到对话场景")
            return True

        # 2. 动作描写
        action_keywords = ['走进', '来到', '看到', '听到', '发现']
        if any(keyword in context[-100:] for keyword in action_keywords):
            logger.info("[RAG] 检测到动作场景")
            return True

        # 3. 力量体系
        power_keywords = ['施展', '使用', '释放', '修炼', '境界', '突破', '法术']
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
        enable_rag: bool = False
    ) -> str:
        """构建增强的自动补全提示词（Context-Aware）

        从数据库加载作品元数据，为AI提供更丰富的上下文

        Args:
            work_id: 作品ID
            chapter_id: 章节ID
            context: 用户输入的文本
            enable_rag: 是否启用RAG检索

        Returns:
            增强后的system prompt
        """
        # 基础提示词
        base_prompt = self._build_autocomplete_system_prompt()

        # 如果没有work_id或db，返回基础版本
        if not work_id or not self.db:
            return base_prompt

        enhancements = []
        guidelines = None  # 声明在外部作用域

        try:
            # ===== 1. 加载 AI Guidelines（最重要的元数据） =====
            from uuid import UUID
            from sqlalchemy import select
            from app.models.ai_guidelines import AIGuidelines
            import json

            # 尝试从 Redis 缓存获取
            cache_key = f"guidelines:{work_id}"
            try:
                from app.core.redis import get_redis
                redis = await get_redis()
                cached = await redis.get(cache_key)

                if cached:
                    # 从缓存恢复
                    cached_data = json.loads(cached)
                    # 创建一个简单对象来存储缓存数据
                    class CachedGuidelines:
                        def __init__(self, data):
                            self.is_active = True
                            for k, v in data.items():
                                setattr(self, k, v)

                    guidelines = CachedGuidelines(cached_data)
                    logger.info(f"[Cache] 从缓存加载 Guidelines")
            except Exception as cache_error:
                logger.warning(f"[Cache] Redis 缓存读取失败: {cache_error}")

            # 如果缓存未命中，从数据库查询
            if not guidelines:
                stmt = select(AIGuidelines).where(AIGuidelines.work_id == UUID(work_id))
                result = await self.db.execute(stmt)
                guidelines = result.scalar_one_or_none()

                # 写入缓存（1小时过期）
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

                        await redis.setex(cache_key, 3600, json.dumps(cache_data, ensure_ascii=False))
                        logger.info(f"[Cache] Guidelines 已缓存（1小时）")
                    except Exception as cache_error:
                        logger.warning(f"[Cache] Redis 缓存写入失败: {cache_error}")

            if guidelines and (hasattr(guidelines, 'is_active') and guidelines.is_active or isinstance(guidelines, type) and hasattr(guidelines, '__dict__')):
                metadata_parts = []

                # 文笔风格（最重要）
                if guidelines.writing_style:
                    metadata_parts.append(f"文笔风格: {guidelines.writing_style}")

                # 叙事节奏
                if guidelines.narrative_rhythm:
                    metadata_parts.append(f"叙事节奏: {guidelines.narrative_rhythm}")

                # 主角基本信息
                if guidelines.protagonist_name:
                    protag_info = f"主角: {guidelines.protagonist_name}"
                    if guidelines.protagonist_traits:
                        # 限制长度
                        traits = guidelines.protagonist_traits[:100]
                        protag_info += f"({traits})"
                    metadata_parts.append(protag_info)

                # 力量体系（如果有）
                if guidelines.power_system_name:
                    power_info = f"力量体系: {guidelines.power_system_name}"
                    if guidelines.power_levels:
                        power_info += f" ({guidelines.power_levels[:80]})"
                    metadata_parts.append(power_info)

                # 世界规则
                if guidelines.world_rules:
                    metadata_parts.append(f"世界规则: {guidelines.world_rules[:150]}")

                # 内容禁忌
                if guidelines.content_taboos:
                    metadata_parts.append(f"禁忌: {guidelines.content_taboos[:100]}")

                if metadata_parts:
                    enhancements.append("【作品设定】\n" + "\n".join(metadata_parts))
                    logger.info(f"[Context-Aware] 已加载 AI Guidelines，{len(metadata_parts)} 项元数据")

        except Exception as e:
            logger.warning(f"[Context-Aware] 加载 AI Guidelines 失败: {e}")

        # ===== 2. 加载章节概要 =====
        if chapter_id:
            try:
                from app.models.chapter import Chapter

                # 当前章节
                stmt = select(Chapter).where(Chapter.id == UUID(chapter_id))
                result = await self.db.execute(stmt)
                current_chapter = result.scalar_one_or_none()

                if current_chapter and current_chapter.summary:
                    enhancements.append(f"【本章剧情】\n{current_chapter.summary[:200]}")
                    logger.info(f"[Context-Aware] 已加载当前章节概要")

                    # 获取前一章概要（可选）
                    if current_chapter.order > 1:
                        prev_stmt = select(Chapter).where(
                            Chapter.work_id == UUID(work_id),
                            Chapter.order == current_chapter.order - 1
                        )
                        prev_result = await self.db.execute(prev_stmt)
                        previous_chapter = prev_result.scalar_one_or_none()

                        if previous_chapter and previous_chapter.summary:
                            enhancements.append(f"【上章剧情】\n{previous_chapter.summary[:150]}")
                            logger.info(f"[Context-Aware] 已加载前一章概要")

            except Exception as e:
                logger.warning(f"[Context-Aware] 加载章节概要失败: {e}")

        # ===== 3. RAG 智能检索（可选，默认关闭） =====
        if enable_rag and work_id and self._should_trigger_rag(context):
            try:
                # 提取人物名
                names = self._extract_character_names(context, guidelines)

                if names:
                    from app.services.vector_store_service import VectorStoreService
                    vector_service = VectorStoreService(self.db)

                    # 构建检索查询（人物名）
                    query = f"人物 {' '.join(names)}"
                    logger.info(f"[RAG] 检索查询: {query}")

                    # 检索相关信息
                    # P2修复: 统一阈值为0.3（原为0.6）
                    relevant_info = await vector_service.retrieve_relevant_analysis(
                        work_id=work_id,
                        query=query,
                        top_k=2,
                        similarity_threshold=0.3
                    )

                    if relevant_info:
                        rag_parts = []
                        for item in relevant_info:
                            if 'content_text' in item:
                                # 限制每条RAG结果长度
                                rag_parts.append(item['content_text'][:150])

                        if rag_parts:
                            enhancements.append("【相关设定】\n" + "\n".join(rag_parts))
                            logger.info(f"[RAG] 已检索到 {len(rag_parts)} 条相关信息")
                    else:
                        logger.info(f"[RAG] 未检索到相关信息")

            except Exception as e:
                # RAG 失败不影响主流程
                logger.warning(f"[RAG] 检索失败: {e}")

        # ===== 组装最终提示词 =====
        if not enhancements:
            logger.info(f"[Context-Aware] 未加载到元数据，使用基础提示词")
            return base_prompt

        # 限制元数据总长度（避免超过token限制）
        enhanced_context = "\n\n".join(enhancements)
        if len(enhanced_context) > 800:
            enhanced_context = enhanced_context[:800] + "..."
            logger.info(f"[Context-Aware] 元数据被截断到800字符")

        final_prompt = f"{base_prompt}\n\n{enhanced_context}"
        logger.info(f"[Context-Aware] 增强提示词构建完成，总长度: {len(final_prompt)}")

        return final_prompt

    def _build_complete_system_prompt(self, prompt: str, style: str) -> str:
        """Build complete (continuation) system prompt from config"""
        return self.prompts.get_complete_prompt(prompt, style)
    
    def _should_filter(self, content: str) -> bool:
        """判断内容是否应该被过滤"""
        if not content:
            return True

        # 检查思考标签
        filter_patterns = ['<think>', '</think>', '<thinking>', '</thinking>']

        for pattern in filter_patterns:
            if pattern in content.lower():
                return True

        return False

    async def _track_api_cost(
        self,
        usage_info: dict,
        task_type: Optional[TaskType],
        start_time: datetime,
        actual_model: Optional[str] = None,  # ✅ 2025-12-18: 实际使用的模型（ModelSelector选择的）
        db: Optional[Any] = None,  # 可选：外层数据库会话（用于事务原子性）
        auto_commit: bool = True   # 是否自动提交（传入外层db时应设为False）
    ) -> Optional[dict]:
        """追踪API调用成本（使用AILogService）

        支持三种模式：
        1. 实例模式：HTTPAIService初始化时传递了user_id（优先）
        2. 上下文模式：从请求上下文获取user_id（用于全局Agent）
        3. 外层事务模式：传入db参数，积分扣除与外层业务共享事务（推荐）

        Args:
            usage_info: usage统计信息
            task_type: 任务类型
            start_time: 调用开始时间
            actual_model: 实际使用的模型名称（由ModelSelector动态选择，如不传则使用self.model）
            db: 可选的外层数据库会话。如果传入，则使用该会话（不自动提交）
            auto_commit: 是否自动提交。传入外层db时应设为False，由外层统一提交/回滚

        Returns:
            dict: 包含追踪结果的字典，包括：
                - ai_call_log: AI调用日志对象（用于关联退款等操作）
                - credits_deducted: 扣除的积分数量（用于退款计算）
                - user_id: 用户ID（用于退款操作）
            失败时返回None

        Note:
            - 如果传入db且auto_commit=False，外层业务失败时可以回滚积分扣除
            - 如果不传入db，使用独立会话并自动提交（适用于流式响应等场景）
        """
        # ✅ 2025-12-01: 优先使用实例的user_id，如果没有则从请求上下文获取
        user_id = self.user_id or get_request_user_id()

        # 检查是否有user_id（任一来源）
        if not user_id:
            logger.debug("[成本追踪] 跳过：缺少user_id（实例和上下文均未设置）")
            return

        try:
            from app.utils.cost_calculator import CostCalculator
            from app.schemas.ai_call_log import AICallLogCreate
            from app.core.database import create_db_session
            from app.services.ai_log_service import AILogService
            from uuid import UUID

            # 记录user_id来源（用于调试）
            source = "实例" if self.user_id else "上下文"
            logger.debug(f"[成本追踪] user_id来源: {source}, user_id={user_id}")

            # ✅ 2025-12-18: 使用实际调用的模型（ModelSelector选择的），而不是默认模型
            model_to_track = actual_model or self.model
            logger.debug(f"[成本追踪] 记录模型: {model_to_track} (actual_model={actual_model}, self.model={self.model})")

            # 提取token使用情况
            prompt_tokens = usage_info.get('prompt_tokens', 0)
            completion_tokens = usage_info.get('completion_tokens', 0)

            # 使用CostCalculator计算成本（统一的定价源）
            cost_data = CostCalculator.calculate_cost(
                model_name=model_to_track,  # ✅ 使用实际模型计算成本
                prompt_tokens=prompt_tokens,
                completion_tokens=completion_tokens
            )

            # 计算响应时间
            duration_ms = int((get_utc_now() - start_time).total_seconds() * 1000)

            # 创建日志记录
            log_data = AICallLogCreate(
                user_id=UUID(user_id),
                model_name=model_to_track,  # ✅ 使用实际模型记录日志
                operation_type=task_type.value if task_type else "unknown",
                prompt_tokens=prompt_tokens,
                completion_tokens=completion_tokens,
                total_tokens=prompt_tokens + completion_tokens,
                prompt_cost=cost_data["prompt_cost"],
                completion_cost=cost_data["completion_cost"],
                total_cost=cost_data["total_cost"],
                duration_ms=duration_ms,
                is_success=True,
                extra_data={}
            )

            # ✅ 2025-12-14: 支持外层事务模式，确保积分扣除的原子性
            # - 如果传入了外层db，使用该db会话（不自动提交，由外层控制）
            # - 如果构造时传入了self.db，使用该会话（适用于非流式API）
            # - 如果都没有，创建独立会话并自动提交（适用于流式响应）
            from contextlib import asynccontextmanager

            @asynccontextmanager
            async def get_db_session():
                """获取数据库会话：传入参数 > 实例db > 独立创建

                Returns:
                    tuple: (db_session, should_auto_commit)
                    - should_auto_commit=False 表示使用外层db，由外层控制事务
                    - should_auto_commit=True 表示使用独立会话，需要自己提交
                """
                # 优先级：传入参数 > 实例db > 独立会话
                effective_db = db if db is not None else self.db

                if effective_db is not None:
                    # 使用外层/实例传入的会话（事务由外层控制）
                    logger.debug("[成本追踪] 使用外层数据库会话（事务原子性模式）")
                    yield effective_db, False  # 不自动提交，由外层控制
                else:
                    # 创建独立会话（适用于流式响应等场景）
                    logger.debug("[成本追踪] 使用独立数据库会话")
                    async with create_db_session() as new_db:
                        yield new_db, True  # 自动提交

            ai_call_log = None  # 返回值，用于关联退款等操作
            credits_deducted = None  # 记录实际扣除的积分（用于退款）
            is_admin_user = False  # 记录是否为管理员（管理员不需要退款）

            async with get_db_session() as (db_session, should_auto_commit):
                # ✅ 2025-12-14: 传递 auto_commit 参数，控制是否自动提交
                temp_log_service = AILogService(db_session)
                ai_call_log = await temp_log_service.create_log(log_data, auto_commit=should_auto_commit)

                # ==================== 积分扣除 ====================
                # ✅ 2025-12-14: 支持事务原子性
                # - 使用外层db时，积分扣除与业务逻辑在同一事务中
                # - 业务失败时，积分扣除也会被回滚
                try:
                    from app.services.credits.credit_service import CreditService
                    from app.services.credits.credit_utils import calculate_credits_from_cost
                    from app.services.credits.credit_exceptions import (
                        InsufficientCreditsError,
                        CreditsExpiredError
                    )
                    from app.models.user import User
                    from sqlalchemy import select

                    # 查询用户信息（检查是否为管理员）
                    user_stmt = select(User).where(User.id == UUID(user_id))
                    user_result = await db_session.execute(user_stmt)
                    user = user_result.scalar_one_or_none()

                    if user:
                        is_admin_user = user.is_admin
                        credit_service = CreditService(db_session)

                        # 计算需要扣除的积分
                        credits_to_deduct = calculate_credits_from_cost(cost_data["total_cost"])

                        # 扣除积分（管理员自动豁免）
                        # consume方法内部会检查余额并加锁，确保线程安全
                        # ✅ 2025-12-14: 传递 auto_commit 参数，与外层事务保持一致
                        transaction = await credit_service.consume(
                            user_id=UUID(user_id),
                            amount=credits_to_deduct,
                            description=f"AI调用: {task_type.value if task_type else 'unknown'}",
                            related_id=ai_call_log.id,
                            skip_check=user.is_admin,  # 管理员豁免
                            auto_commit=should_auto_commit  # 由外层事务控制提交
                        )

                        if transaction:  # 非管理员才有交易记录
                            credits_deducted = credits_to_deduct  # 记录扣除金额（用于退款）
                            logger.debug(
                                f"[积分扣除] 用户 {user_id}: 扣除 {float(credits_to_deduct)} 积分, "
                                f"余额: {float(transaction.balance_before)} → {float(transaction.balance_after)}"
                            )
                        else:
                            logger.debug(f"[积分扣除] 管理员 {user_id} 豁免积分扣除")

                        # 注意：邀请激活逻辑已移至注册阶段（注册即激活模式）
                        # 此处不再需要检查消费激活条件
                        # 参见: auth.py register() 函数中的 force=True 激活逻辑

                    else:
                        logger.warning(f"[积分扣除] 用户 {user_id} 不存在，跳过扣除")

                except InsufficientCreditsError as e:
                    # 余额不足时抛出HTTPException
                    logger.error(
                        f"[积分扣除] 用户 {user_id} 余额不足: "
                        f"需要 {float(e.required)} 积分，当前 {float(e.available)} 积分"
                    )
                    # 回滚DB事务
                    await db_session.rollback()
                    # 抛出HTTP异常，中断流式响应
                    from fastapi import HTTPException
                    raise HTTPException(
                        status_code=402,  # Payment Required
                        detail=f"积分余额不足：需要 {float(e.required):.2f} 积分，当前余额 {float(e.available):.2f} 积分。请先充值。"
                    )
                except CreditsExpiredError as e:
                    logger.error(f"[积分扣除] 用户 {user_id} 积分已过期: {e.expired_at}")
                    await db_session.rollback()
                    from fastapi import HTTPException
                    raise HTTPException(
                        status_code=402,
                        detail=f"积分已于 {e.expired_at} 过期，请联系管理员。"
                    )
                except ValueError as e:
                    # 积分记录不存在
                    logger.error(f"[积分扣除] {str(e)}")
                    await db_session.rollback()
                    from fastapi import HTTPException
                    raise HTTPException(
                        status_code=500,
                        detail="积分系统错误：用户积分记录不存在。"
                    )
                except Exception as e:
                    logger.error(f"[积分扣除] 扣除失败: {type(e).__name__}: {str(e)}")
                    # 其他异常不影响日志记录，但记录警告
                    logger.warning("[积分扣除] 扣除失败，但AI调用日志已记录")
                # ================================================

            logger.debug(
                f"[AILogService] API调用已记录到数据库 (来源:{source}): "
                f"tokens={prompt_tokens + completion_tokens}, "
                f"cost=${cost_data['total_cost']:.6f}, "
                f"time={duration_ms}ms"
            )

            # ✅ 2025-12-15: 返回包含追踪结果的字典（用于空响应退款）
            return {
                "ai_call_log": ai_call_log,
                "credits_deducted": credits_deducted,
                "user_id": user_id,
                "is_admin": is_admin_user
            }

        except Exception as e:
            logger.error(f"成本追踪失败: {type(e).__name__}: {str(e)}")
            # 成本追踪失败不应影响主流程
            return None

    async def call_ai(
        self,
        system_prompt: str,
        user_prompt: str,
        max_tokens: int = 2000,
        temperature: float = 0.7,
        max_retries: int = 3,
        task_type: Optional[TaskType] = None
    ) -> str:
        """
        非流式AI调用 (用于评审等需要完整响应的场景,带重试机制)

        Args:
            system_prompt: 系统提示词
            user_prompt: 用户提示词
            max_tokens: 最大token数
            temperature: 温度参数
            max_retries: 最大重试次数(默认3次)
            task_type: 任务类型 (用于成本追踪)

        Returns:
            完整的AI响应文本
        """
        url = f"{self.base_url}/chat/completions"
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }

        # ✅ 2025-12-18: 非流式调用也应使用 ModelSelector 智能选择模型
        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ]

        if self.model_selector and task_type:
            try:
                selection = self.model_selector.select_model(
                    task_type=task_type,
                    input_tokens=len(str(messages)) // 4,
                    output_tokens=max_tokens
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

        payload = {
            "model": model,  # ✅ 使用动态选择的模型
            "messages": messages,
            "temperature": temperature,
            "max_tokens": max_tokens,
            "stream": False  # 非流式
        }

        # 记录开始时间 (用于成本追踪)
        start_time = get_utc_now()

        # 重试机制
        for attempt in range(max_retries):
            try:
                if attempt > 0:
                    # 指数退避: 2秒, 4秒, 8秒
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

                response = await self.client.post(url, json=payload, headers=headers)

                if response.status_code != 200:
                    error_text = response.text
                    logger.error(f"API错误: {response.status_code}, {error_text[:500]}")

                    # 如果是服务器错误(5xx)或超时(429),可以重试
                    if response.status_code >= 500 or response.status_code == 429:
                        if attempt < max_retries - 1:
                            continue  # 重试

                    raise Exception(f"API请求失败: {response.status_code}")

                data = response.json()
                content = data['choices'][0]['message']['content']

                # Week 7: 追踪成本 (如果API返回了usage信息)
                # ✅ 2025-12-15: 保存追踪结果用于空响应退款
                # ✅ 2025-12-18: 传递实际使用的模型（ModelSelector选择的）
                cost_tracking_result = None
                if self.enable_cost_tracking and 'usage' in data:
                    cost_tracking_result = await self._track_api_cost(
                        usage_info=data['usage'],
                        task_type=task_type,
                        start_time=start_time,
                        actual_model=model  # ✅ 传递 ModelSelector 动态选择的模型
                    )

                # ✅ 2025-12-15: 空响应自动退款
                if not content or len(content.strip()) == 0:
                    logger.error(f"警告: AI 非流式响应为空！")

                    # 检查是否有扣费记录且非管理员
                    if (cost_tracking_result
                        and cost_tracking_result.get("credits_deducted")
                        and not cost_tracking_result.get("is_admin")):

                        try:
                            from app.core.database import create_db_session
                            from app.services.credits.credit_service import CreditService
                            from uuid import UUID

                            credits_to_refund = cost_tracking_result["credits_deducted"]
                            refund_user_id = cost_tracking_result["user_id"]
                            ai_call_log = cost_tracking_result.get("ai_call_log")

                            async with create_db_session() as db:
                                credit_service = CreditService(db)

                                # 执行退款
                                refund_transaction = await credit_service.refund(
                                    user_id=UUID(refund_user_id),
                                    amount=credits_to_refund,
                                    description="AI响应为空，自动退还积分",
                                    related_id=ai_call_log.id if ai_call_log else None
                                )

                                logger.info(
                                    f"[自动退款] 用户 {refund_user_id}: 退还 {float(credits_to_refund)} 积分, "
                                    f"原因: AI非流式响应为空, "
                                    f"余额: {float(refund_transaction.balance_before)} → {float(refund_transaction.balance_after)}"
                                )

                        except Exception as refund_error:
                            # ⚠️ 退款失败时记录完整信息，便于手动补偿
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

            except httpx.ReadTimeout as e:
                logger.error(
                    f"AI调用超时 (尝试 {attempt + 1}/{max_retries}): {str(e)}"
                )
                if attempt < max_retries - 1:
                    continue  # 重试
                else:
                    logger.error(f"AI调用超时,已重试{max_retries}次,全部失败")
                    raise Exception(f"网络请求超时,已重试{max_retries}次")

            except httpx.HTTPError as e:
                logger.error(
                    f"HTTP请求错误 (尝试 {attempt + 1}/{max_retries}): "
                    f"{type(e).__name__}: {str(e)}"
                )
                if attempt < max_retries - 1:
                    continue  # 重试
                else:
                    logger.error(f"HTTP请求失败,已重试{max_retries}次,全部失败")
                    raise Exception(f"网络请求失败: {str(e)}")

            except Exception as e:
                logger.error(
                    f"AI调用错误 (尝试 {attempt + 1}/{max_retries}): "
                    f"{type(e).__name__}: {str(e)}"
                )
                # 其他异常不重试
                raise

        # 理论上不会到这里
        raise Exception(f"AI调用失败,已重试{max_retries}次")

    def _generate_cache_key(
        self,
        messages: list,
        model: str,
        temperature: float,
        max_tokens: int
    ) -> str:
        """
        生成缓存键

        Args:
            messages: 消息列表
            model: 模型名称
            temperature: 温度参数
            max_tokens: 最大token数

        Returns:
            str: 缓存键
        """
        # 限制消息长度以避免内存问题
        max_message_length = 10000  # 10k字符限制
        messages_str = json.dumps(messages, sort_keys=True, ensure_ascii=False)

        if len(messages_str) > max_message_length:
            # 对过长消息进行截断并添加标记
            messages_str = messages_str[:max_message_length] + "...[TRUNCATED]"

        # 创建缓存键的组成部分，标准化温度精度
        key_components = [
            messages_str,
            model,
            f"{temperature:.3f}",  # 限制温度为3位小数
            str(max_tokens)
        ]

        # 组合并生成MD5哈希
        key_string = "|".join(key_components)
        cache_key = hashlib.md5(key_string.encode('utf-8')).hexdigest()

        logger.debug(f"Generated cache key: {cache_key}")
        return cache_key

