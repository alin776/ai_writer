"""
HTTP-based AI Service (Bypass Cloudflare blocking)

Direct httpx calls to OpenAI API, not using openai-python SDK
"""

import httpx
import json
import logging
import asyncio
import hashlib
from typing import AsyncGenerator, Optional
from datetime import datetime
from app.core.config import settings
from app.services.ai.prompts import get_prompts_manager
from app.services.agent.model_selector import ModelSelector, TaskType
# ❌ DEPRECATED - 2025-12-01: 注释掉CostTracker，改用AILogService
# from app.services.agent.cost_tracker import get_cost_tracker
from ..agent.utils.llm_optimizer import get_llm_optimizer, optimized_llm_call
# ✅ 2025-12-01: 支持从请求上下文获取user_id（用于全局Agent成本追踪）
from app.core.request_context import get_request_user_id, get_request_db

logger = logging.getLogger(__name__)


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

        # ❌ DEPRECATED - 2025-12-01: 注释掉CostTracker
        # if enable_cost_tracking:
        #     self.cost_tracker = get_cost_tracker()
        #     logger.info("CostTracker 已启用")
        # else:
        #     self.cost_tracker = None

        # ✅ 新增：使用AILogService替代CostTracker
        if enable_cost_tracking and db and user_id:
            from app.services.ai_log_service import AILogService
            self.ai_log_service = AILogService(db)
            logger.info("AILogService 已启用 (用于成本追踪)")
        else:
            self.ai_log_service = None
            if enable_cost_tracking:
                logger.warning(
                    "成本追踪已启用，但未提供db或user_id，"
                    "成本数据将不会被记录！请检查HTTPAIService初始化参数。"
                )

        # 创建持久化客户端，模拟普通浏览器/应用
        self.client = httpx.AsyncClient(
            headers={
                "User-Agent": "okhttp/4.12.0",
                "Accept": "application/json",
                "Accept-Encoding": "gzip, deflate",
                "Connection": "keep-alive",
            },
            timeout=httpx.Timeout(
                timeout_value,  # 使用可配置的超时
                connect=10.0
            ),
            follow_redirects=True,
            http2=True,  # 启用 HTTP/2 - 支持多路复用和头部压缩
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
        task_type: Optional[TaskType] = None
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
        # 🔧 监控：导入监控工具
        import time
        from app.services.agent.utils.monitoring import increment_counter, record_timer, set_gauge

        # 🔧 监控：记录LLM调用开始时间
        llm_start_time = time.time()

        # ==================== 模型选择逻辑 ====================
        # 根据task_type智能选择模型
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
                    f"[ModelSelector] 任务={task_type.value}, "
                    f"模型={model}, 原因={selection.reason}"
                )
            except Exception as e:
                logger.warning(f"[ModelSelector] 选择失败: {e}, 使用默认模型")
                model = self.model
        else:
            # 使用默认模型
            model = self.model
            if task_type and not self.model_selector:
                logger.debug(f"[ModelSelector] 未启用，使用默认模型: {model}")
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

        logger.info(
            f"开始调用 AI API: model={model}, "  # ← 记录实际模型
            f"max_tokens={max_tokens}, temp={temperature}, task_type={task_type}"
        )

        # 记录开始时间 (用于成本追踪)
        start_time = datetime.now()

        # Week 10: 添加缓存索引键生成
        cache_key = self._generate_cache_key(messages, model, temperature, max_tokens)  # ← 使用model而不是self.model

        try:
            async with self.client.stream("POST", url, json=payload, headers=headers) as response:
                if response.status_code != 200:
                    error_text = await response.aread()
                    error_msg = error_text.decode('utf-8', errors='ignore')[:500]
                    logger.error(f"API 错误: {response.status_code}, {error_msg}")
                    raise Exception(f"API 请求失败: {response.status_code}")

                logger.info("API 流式响应已建立，开始接收数据...")
                chunk_count = 0
                total_content = ""
                usage_info = None  # 用于存储最终的usage信息

                async for line in response.aiter_lines():
                    line = line.strip()

                    # SSE 格式: data: {...}
                    if not line or not line.startswith("data: "):
                        continue

                    # 移除 "data: " 前缀
                    data_str = line[6:]

                    # 结束标记
                    if data_str == "[DONE]":
                        logger.info(
                            f"API 响应完成，共接收 {chunk_count} 个数据块，总长度: {len(total_content)}"
                        )
                        # 记录usage统计
                        if usage_info:
                            logger.info(
                                f"流式响应Token统计: {usage_info.get('total_tokens', 0)} "
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
                                    yield content, None  # 中间块不返回usage

                    except json.JSONDecodeError as e:
                        logger.warning(f"JSON 解析错误: {e}, 数据: {data_str[:100]}")
                        continue

                # Week 7: 追踪成本
                # ✅ 2025-12-01: 移除ai_log_service检查（现在使用独立db session）
                if self.enable_cost_tracking and usage_info:
                    await self._track_api_cost(
                        usage_info=usage_info,
                        task_type=task_type,
                        start_time=start_time
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

                # 如果没有接收到任何内容，记录警告
                if chunk_count == 0:
                    logger.error(f"警告: AI 响应为空！未接收到任何内容块。")

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

        async for chunk, usage in self._stream_chat(messages, max_tokens, temperature):
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
        max_tokens: int = 500,
        temperature: float = 0.3
    ) -> AsyncGenerator[tuple[str, dict | None], None]:
        """AI Summarize (streaming response)

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
                    relevant_info = await vector_service.retrieve_relevant_analysis(
                        work_id=work_id,
                        query=query,
                        top_k=2,
                        similarity_threshold=0.6
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
        start_time: datetime
    ):
        """追踪API调用成本（使用AILogService）

        支持两种模式：
        1. 实例模式：HTTPAIService初始化时传递了user_id（优先）
        2. 上下文模式：从请求上下文获取user_id（用于全局Agent）

        Args:
            usage_info: usage统计信息
            task_type: 任务类型
            start_time: 调用开始时间
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

            # 提取token使用情况
            prompt_tokens = usage_info.get('prompt_tokens', 0)
            completion_tokens = usage_info.get('completion_tokens', 0)

            # 使用CostCalculator计算成本（统一的定价源）
            cost_data = CostCalculator.calculate_cost(
                model_name=self.model,
                prompt_tokens=prompt_tokens,
                completion_tokens=completion_tokens
            )

            # 计算响应时间
            duration_ms = int((datetime.now() - start_time).total_seconds() * 1000)

            # 创建日志记录
            log_data = AICallLogCreate(
                user_id=UUID(user_id),
                model_name=self.model,
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

            # ✅ 使用独立db会话持久化（解决StreamingResponse会话生命周期问题）
            async with create_db_session() as db:
                temp_log_service = AILogService(db)
                await temp_log_service.create_log(log_data)

            logger.info(
                f"[AILogService] API调用已记录到数据库 (来源:{source}): "
                f"tokens={prompt_tokens + completion_tokens}, "
                f"cost=${cost_data['total_cost']:.6f}, "
                f"time={duration_ms}ms"
            )

        except Exception as e:
            logger.error(f"成本追踪失败: {type(e).__name__}: {str(e)}")
            # 成本追踪失败不应影响主流程

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

        payload = {
            "model": self.model,
            "messages": [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            "temperature": temperature,
            "max_tokens": max_tokens,
            "stream": False  # 非流式
        }

        # 记录开始时间 (用于成本追踪)
        start_time = datetime.now()

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

                logger.info(
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
                if self.enable_cost_tracking and 'usage' in data:
                    await self._track_api_cost(
                        usage_info=data['usage'],
                        task_type=task_type,
                        start_time=start_time
                    )

                logger.info(
                    f"AI响应成功, 长度={len(content)}, "
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
