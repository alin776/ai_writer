# -*- coding: utf-8 -*-
"""
Agent 执行链路实现（Planning 主链路）

当前实际运行链路为：
- /chat/stream → chat_with_planning → PlanGenerator → 执行 → 汇总输出

保留：
- Checkpointer（对话分支/回溯）
- Planning 执行与工具调度
"""

from typing import TypedDict, Annotated, List, Dict, Any, Optional
from datetime import datetime
import os
from langgraph.checkpoint.redis import AsyncRedisSaver
import operator
import logging
import uuid
import asyncio
import redis
import json
import re

from app.services.ai.http_ai_service import HTTPAIService
from app.core.config import settings
from app.services.agent.model_selector import TaskType
from app.services.agent.timeout_config import TimeoutConfig, async_timeout
from app.services.context.context_config import ContextConfig
# 🔧 2025-12-14: 导入 registry 用于统一工具调用
from app.utils.datetime_utils import get_utc_now

# ✅ 拆分模块导入
from app.services.agent.langgraph_tools import (
    # 全局服务管理
    set_global_ai_service,
)

# ✅ 2025-12-23: 解耦重构 - 导入拆分模块
from app.services.agent.intent import IntentClassifier
from app.services.agent.execution import ToolExecutor, ParallelExecutor, TaskRunner
from app.services.agent.stream import EventParser, StreamEventHandler
from app.services.agent.planning import ResponseBuilder, classify_tasks, PlanGenerator, QuickPathHandler

logger = logging.getLogger(__name__)


# ==================== State 定义 ====================

class AgentState(TypedDict):
    """Agent 状态定义"""
    messages: Annotated[List[Any], operator.add]  # 对话历史
    work_id: Optional[str]  # 作品ID
    chapter_id: Optional[str]  # 章节ID
    intent: Optional[str]  # 用户意图
    intent_decision: Optional[Dict[str, Any]]  # CoT 复杂度决策 {complexity, action}
    context: Dict[str, Any]  # 上下文信息
    agent_steps: Annotated[List[Dict[str, Any]], operator.add]  # Agent执行步骤
    suggested_actions: Annotated[List[str], operator.add]  # 建议操作
    final_response: Optional[str]  # 最终响应


# ==================== Agent 节点定义 ====================

class WritingAgentGraph:
    """
    LangGraph 写作 Agent

    使用 HTTPAIService + 手动工具调用
    """

    @classmethod
    async def setup_checkpointer(cls):
        """
        预创建AsyncRedisSaver索引（应用启动时调用）

        优化点: 避免首次请求时的21秒索引创建延迟
        """
        try:
            from app.core.config import settings
            redis_url = settings.REDIS_URL

            # 创建临时checkpointer实例用于预初始化
            ttl_config = {
                "default_ttl": 10080,  # 7天
                "refresh_on_read": True  # 启用自动续期，活跃对话自动续期到7天
            }

            # ✅ P0-5修复：测试Redis连接（防止NameError）
            test_client = None
            try:
                test_client = redis.Redis.from_url(redis_url, decode_responses=False)
                test_client.ping()
                logger.info("[LangGraph] ✅ setup_checkpointer Redis连接验证成功")
            except Exception as test_error:
                logger.error(f"[LangGraph] ❌ setup_checkpointer Redis连接测试失败: {test_error}")
                raise
            finally:
                if test_client:
                    try:
                        test_client.close()
                    except Exception as close_error:
                        logger.warning(f"[LangGraph] setup_checkpointer关闭Redis测试连接时出错: {close_error}")

            # 创建并初始化checkpointer
            checkpointer = AsyncRedisSaver(redis_url=redis_url, ttl=ttl_config)
            await checkpointer.asetup()  # 预创建索引
            logger.info("[LangGraph] ✅ AsyncRedisSaver索引预创建成功")
        except Exception as e:
            logger.warning(f"[LangGraph] ⚠️ AsyncRedisSaver索引预创建失败: {e}")
            logger.warning("[LangGraph] 将在首次使用时自动创建索引")

    def __init__(self, ai_service: HTTPAIService):
        """
        初始化 Agent

        Args:
            ai_service: HTTPAIService 实例
        """
        self.ai_service = ai_service

        # ✅ P0-6修复：HITL确认请求回调（存储为实例变量，避免序列化到Redis）
        self._approval_callback: Optional[callable] = None

        # 🔧 缓存工具调用参数（用于进度显示）
        self._cached_tool_calls = {}

        # 设置全局 AI Service（供工具使用）
        set_global_ai_service(ai_service)

        # 🔧 2025-12-14: 同时设置 writing_tools 的 AI Service（用于 StandardTool）
        from app.services.agent.tools import set_ai_service
        set_ai_service(ai_service)
        logger.info("[LangGraph] ✅ AI Service 已同时设置到 langgraph_tools 和 writing_tools")

        # 初始化上下文管理器（用于chat_stream的长对话管理）
        from app.services.context import ContextManager
        from app.services.context.adaptive_budget import get_adaptive_budget

        # ✅ 启用自适应预算：根据任务类型智能分配Token，总预算提升到16000
        adaptive_budget = get_adaptive_budget(total=16000)

        self.context_manager = ContextManager(
            ai_service=self.ai_service,  # 传入AI服务（用于LLM摘要）
            enable_long_term_memory=True,  # 启用长期记忆
            enable_adaptive_budget=True,  # ✅ 启用自适应预算
            adaptive_budget=adaptive_budget  # ✅ 传入自适应预算实例（16000 tokens）
        )
        logger.info("[LangGraph] ✅ ContextManager已初始化（长期记忆已启用，自适应预算已启用，总预算=16000 tokens）")

        # 初始化Prompt管理器（用于统一管理各类Agent的Prompt模板）
        from app.prompts import get_prompt_manager
        self.prompt_manager = get_prompt_manager()
        logger.info("[LangGraph] ✅ PromptManager已初始化")

        # 创建 Checkpointer（记忆系统）
        # 使用 AsyncRedisSaver 替代 MemorySaver，解决内存泄漏和数据持久化问题
        try:
            # AsyncRedisSaver必须使用db0（RediSearch索引限制）
            # 使用checkpoint:前缀避免与缓存key冲突
            redis_url = settings.REDIS_URL  # 使用db0

            # ✅ P0-5修复：完善Redis连接验证
            test_client = None  # ✅ 防止NameError
            try:
                test_client = redis.Redis.from_url(redis_url, decode_responses=False)
                test_client.ping()
                logger.info("[LangGraph] ✅ Redis连接验证成功")
            except Exception as test_error:
                logger.error(f"[LangGraph] ❌ Redis连接测试失败: {test_error}")
                raise  # 重新抛出异常，触发降级
            finally:
                # ✅ P0-5修复：确保test_client正确关闭
                if test_client:  # ✅ 检查是否已初始化
                    try:
                        test_client.close()
                    except Exception as close_error:
                        logger.warning(f"[LangGraph] 关闭Redis测试连接时出错: {close_error}")

            # AsyncRedisSaver支持异步操作，直接传递URL字符串
            # 配置TTL：7天自动清理不活跃对话
            ttl_config = {
                "default_ttl": 10080,  # 7天 = 7 * 24 * 60分钟
                "refresh_on_read": True  # 启用自动续期，活跃对话自动续期到7天
            }
            self.checkpointer = AsyncRedisSaver(redis_url=redis_url, ttl=ttl_config)
            self._checkpointer_setup_done = False  # 标记是否已初始化索引
            logger.info(f"[LangGraph] OK 使用 AsyncRedisSaver（{redis_url}，TTL=7天）")
        except Exception as e:
            logger.warning(f"[LangGraph] 警告 Redis连接失败，降级使用MemorySaver: {e}")
            # 降级方案：如果Redis不可用，使用MemorySaver
            from langgraph.checkpoint.memory import MemorySaver
            self.checkpointer = MemorySaver()
            self._checkpointer_setup_done = True  # MemorySaver不需要setup

        # ✅ P0-1修复: 初始化统一记忆协调器
        self._init_unified_memory_coordinator()

        # ✅ 2025-12-23: 解耦重构 - 初始化拆分模块
        self.intent_classifier = IntentClassifier(ai_service)
        self.tool_executor = ToolExecutor()
        self.event_parser = EventParser(self._cached_tool_calls)
        # ✅ Phase 4.3: ResponseBuilder 需要延迟设置 stream generator
        self.response_builder = ResponseBuilder(ai_service)
        # ✅ Phase 2.2: 初始化 ParallelExecutor
        self.parallel_executor = ParallelExecutor(self)
        # ✅ Phase 2.3: 初始化 PlanGenerator
        self.plan_generator = PlanGenerator(self)
        # ✅ Phase 2.4: 初始化 QuickPathHandler
        self.quick_path_handler = QuickPathHandler(self)
        # ✅ Phase 3.2: 初始化 StreamEventHandler
        self.stream_event_handler = StreamEventHandler(
            event_parser=self.event_parser,
            cached_tool_calls=self._cached_tool_calls,
            approval_callback=self._approval_callback
        )
        # ✅ Phase 4.4: 初始化 TaskRunner（单任务执行）
        self.task_runner = TaskRunner(
            call_tool_via_registry_func=self._call_tool_via_registry,
            extract_tool_result_func=self._extract_tool_result
        )
        # ✅ Phase 4.3: 延迟设置 ResponseBuilder 的流式生成函数
        self.response_builder.set_stream_generator(self._generate_text_stream)
        # ✅ Phase 4.4: 设置 ResponseBuilder 的流式事件处理器（用于 Summarization 事件）
        self.response_builder.set_stream_event_handler(self.stream_event_handler)
        logger.info("[LangGraph] ✅ 解耦模块已初始化 (IntentClassifier, ToolExecutor, EventParser, ResponseBuilder, ParallelExecutor, PlanGenerator, QuickPathHandler, StreamEventHandler, TaskRunner)")

    def _init_unified_memory_coordinator(self):
        """
        初始化统一记忆协调器（✅ P0-1修复）

        协调三个记忆系统：
        1. AsyncRedisSaver (checkpointer) - 对话历史
        2. EnhancedMemoryManager - 三层记忆
        3. ContextManager - 上下文管理

        这是一个同步初始化方法，异步setup会在首次使用时完成
        """
        try:
            from app.services.agent.memory import (
                UnifiedMemoryCoordinator,
                UnifiedMemoryConfig,
                set_unified_coordinator
            )
            from app.services.agent.memory.enhanced_memory_manager import EnhancedMemoryManager
            from app.core.config import settings

            # 创建EnhancedMemoryManager实例
            try:
                # 🔧 2025-12-02: P2修复 - 创建redis_client传入EnhancedMemoryManager
                enhanced_redis_client = redis.Redis.from_url(
                    settings.REDIS_URL,
                    decode_responses=True
                )
                enhanced_memory = EnhancedMemoryManager(redis_client=enhanced_redis_client)
                logger.info("[LangGraph] ✅ EnhancedMemoryManager已创建")
            except Exception as e:
                logger.warning(f"[LangGraph] ⚠️ EnhancedMemoryManager创建失败，将在协调器中降级: {e}")
                enhanced_memory = None

            # 配置协调器
            config = UnifiedMemoryConfig(
                sync_to_enhanced_memory=True,
                sync_to_context_manager=True,
                fallback_on_checkpointer_failure=True,
                fallback_on_enhanced_memory_failure=True,
                ensure_consistency=True
            )

            # 创建统一记忆协调器
            self.memory_coordinator = UnifiedMemoryCoordinator(
                checkpointer=self.checkpointer,
                enhanced_memory=enhanced_memory,
                context_manager=self.context_manager,
                config=config
            )

            # 设置为全局实例
            set_unified_coordinator(self.memory_coordinator)

            logger.info(
                "[LangGraph] ✅ UnifiedMemoryCoordinator已初始化 | "
                f"checkpointer={type(self.checkpointer).__name__} | "
                f"enhanced_memory={'yes' if enhanced_memory else 'no'} | "
                f"context_manager=yes"
            )

        except Exception as e:
            logger.error(f"[LangGraph] ❌ UnifiedMemoryCoordinator初始化失败: {e}")
            self.memory_coordinator = None

    async def _ensure_memory_coordinator_ready(self):
        """确保记忆协调器已完成异步初始化"""
        if self.memory_coordinator and not self.memory_coordinator._initialized:
            await self.memory_coordinator.initialize()

    # ==================== 工具执行（委托到 ToolExecutor）====================

    async def _call_tool_via_registry(self, tool_name: str, tool_args: dict, state: dict) -> str:
        """通过 registry 统一调用工具 - 委托到 ToolExecutor"""
        return await self.tool_executor.call_tool(tool_name, tool_args, state)

    def _prepare_tool_params(self, tool_name: str, tool_args: dict, state: dict) -> dict:
        """准备工具参数 - 委托到 ToolExecutor"""
        return self.tool_executor.prepare_params(tool_name, tool_args, state)

    def _extract_tool_result(self, tool_name: str, result: dict) -> str:
        """提取工具结果 - 委托到 ToolExecutor"""
        return self.tool_executor.extract_result(tool_name, result)

    async def _fallback_to_legacy_tool(self, tool_name: str, tool_args: dict, state: dict) -> str:
        """降级到旧版工具 - 委托到 ToolExecutor"""
        return await self.tool_executor.fallback_to_legacy(tool_name, tool_args, state)

    # ==================== 原有方法继续 ====================

    async def _generate_text(
        self,
        prompt: Optional[str] = None,
        messages: Optional[List] = None,  # ✅ 新增：支持消息列表（修复记忆问题）
        temperature: float = 0.7,
        max_tokens: int = 1000,
        task_type: Optional[TaskType] = None,
        response_format: Optional[dict] = None
    ) -> dict:
        """生成文本的辅助方法（使用HTTPAIService）

        Args:
            prompt: 提示词（可选，与messages二选一）
            messages: 消息列表（可选，与prompt二选一，格式：[{"role": "user", "content": "..."}]）
            temperature: 温度参数
            max_tokens: 最大token数
            task_type: 任务类型（用于模型选择）

        Returns:
            dict: {"text": str, "usage": dict}
        """
        # ✅ 参数验证
        if prompt is None and messages is None:
            raise ValueError("prompt 和 messages 必须至少提供一个")
        if prompt is not None and messages is not None:
            raise ValueError("prompt 和 messages 不能同时提供")
        from app.services.agent.utils.monitoring import increment_counter

        # ✅ P0-1: 添加超时保护（使用统一配置）
        try:
            async with async_timeout(TimeoutConfig.LLM_CALL):
                # 使用HTTPAIService
                # ✅ 构建消息列表
                if messages is not None:
                    # 使用提供的消息列表
                    http_messages = messages
                else:
                    # 使用单个prompt（向后兼容）
                    http_messages = [{"role": "user", "content": prompt}]

                generated_text = ""
                usage = None

                async for chunk, chunk_usage in self.ai_service._stream_chat(
                    messages=http_messages,
                    max_tokens=max_tokens,
                    temperature=temperature,
                    task_type=task_type,  # ← 传递task_type
                    response_format=response_format
                ):
                    if chunk:
                        generated_text += chunk
                    if chunk_usage:
                        usage = chunk_usage

                logger.info(f"[_generate_text] 使用HTTPAIService生成文本，tokens={usage.get('total_tokens', 0) if usage else 0}")

                return {
                    "text": generated_text,
                    "usage": usage or {}
                }

        except asyncio.TimeoutError:
            # 超时处理
            logger.error(f"[_generate_text] HTTPAIService LLM调用超时（{TimeoutConfig.LLM_CALL}秒）")
            increment_counter("generate_text_error", labels={"error_type": "TimeoutError"})

            # 返回错误结果
            return {
                "text": f"抱歉，AI响应超时（超过{TimeoutConfig.LLM_CALL}秒）。请稍后重试。",
                "usage": {},
                "error": "timeout"
            }

        except Exception as e:
            error_str = str(e)
            # 其他异常处理
            logger.error(f"[_generate_text] HTTPAIService LLM调用失败: {error_str}", exc_info=True)
            increment_counter("generate_text_error", labels={"error_type": type(e).__name__})

            # 检测积分不足错误，返回友好提示
            if "积分" in error_str and ("不足" in error_str or "余额" in error_str):
                return {
                    "text": "积分余额不足，请先充值后再使用此功能。",
                    "usage": {},
                    "error": "insufficient_credits"
                }

            # 返回错误结果
            return {
                "text": f"抱歉，AI服务调用失败：{error_str}",
                "usage": {},
                "error": error_str
            }

    async def _generate_text_stream(
        self,
        prompt: str,
        on_chunk: callable,
        temperature: float = 0.7,
        max_tokens: int = 2000,
        task_type: Optional[TaskType] = None,
        buffer_size: int = 1  # ✅ 默认逐字输出
    ) -> dict:
        """流式生成文本，带缓冲区平滑输出

        真正的流式输出：每累积 buffer_size 个字符就立即回调，
        而不是等待完整响应后再发送。

        Args:
            prompt: 提示词
            on_chunk: 每个缓冲区满时的回调函数 (async callable)
            temperature: 温度参数
            max_tokens: 最大token数
            task_type: 任务类型（用于模型选择）
            buffer_size: 缓冲区大小（字符数），默认1个字符（逐字输出）

        Returns:
            dict: {"text": str, "usage": dict, "partial": bool(可选)}
        """
        from app.services.agent.utils.monitoring import increment_counter

        full_text = ""
        usage = None
        buffer = ""

        logger.info(f"[_generate_text_stream] 开始流式生成，buffer_size={buffer_size}")

        try:
            async with async_timeout(TimeoutConfig.LLM_CALL):
                async for chunk, chunk_usage in self.ai_service._stream_chat(
                    messages=[{"role": "user", "content": prompt}],
                    max_tokens=max_tokens,
                    temperature=temperature,
                    task_type=task_type
                ):
                    if chunk:
                        full_text += chunk
                        buffer += chunk

                        # 缓冲区满了才发送（平滑显示）
                        if len(buffer) >= buffer_size:
                            await on_chunk(buffer)
                            buffer = ""

                    if chunk_usage:
                        usage = chunk_usage

                # 发送剩余缓冲区内容
                if buffer:
                    await on_chunk(buffer)

                logger.info(f"[_generate_text_stream] 流式生成完成，总长度={len(full_text)}")

        except asyncio.TimeoutError:
            logger.warning(f"[_generate_text_stream] 超时({TimeoutConfig.LLM_CALL}s)，返回已生成内容")
            increment_counter("generate_text_stream_error", labels={"error_type": "TimeoutError"})

            # 超时降级：发送剩余缓冲区，返回已生成的部分内容
            if buffer:
                await on_chunk(buffer)

            if full_text:
                return {"text": full_text, "usage": usage or {}, "partial": True}
            return {"text": "", "usage": {}, "error": "timeout"}

        except Exception as e:
            error_str = str(e)
            logger.error(f"[_generate_text_stream] 流式生成失败: {error_str}", exc_info=True)
            increment_counter("generate_text_stream_error", labels={"error_type": type(e).__name__})

            # 检测积分不足错误，直接返回错误（不降级）
            if "积分" in error_str and ("不足" in error_str or "余额" in error_str):
                return {"text": "", "usage": {}, "error": error_str}

            # 异常降级：发送剩余缓冲区，返回已生成的部分内容
            if buffer:
                try:
                    await on_chunk(buffer)
                except Exception:
                    pass

            if full_text:
                return {"text": full_text, "usage": usage or {}, "partial": True, "error": error_str}
            return {"text": "", "usage": {}, "error": error_str}

        return {"text": full_text, "usage": usage or {}}

    # ==================== Thread ID 构建（公共方法）====================

    def _build_thread_id(
        self,
        user_id: Optional[str],
        work_id: Optional[str],
        conversation_id: Optional[str],
        log_prefix: str = "LangGraph"
    ) -> str:
        """构建隔离的 thread_id（三层隔离：user_id > work_id > conversation_id）

        Args:
            user_id: 用户ID
            work_id: 作品ID
            conversation_id: 会话ID
            log_prefix: 日志前缀

        Returns:
            str: 构建好的 thread_id
        """
        import hashlib as _hashlib

        user_prefix = f"{user_id}:" if user_id else ""

        if work_id and conversation_id:
            thread_id = f"{user_prefix}{work_id}:{conversation_id}"
        elif work_id:
            thread_id = f"{user_prefix}{work_id}:default"
        elif conversation_id:
            thread_id = f"{user_prefix}{conversation_id}"
        else:
            thread_id = f"{user_prefix}anonymous:{uuid.uuid4()}" if not user_prefix else f"{user_prefix}default"

        # P2防护：thread_id长度验证
        max_thread_id_length = ContextConfig.MAX_THREAD_ID_LENGTH
        if len(thread_id) > max_thread_id_length:
            logger.warning(
                f"[{log_prefix}] thread_id过长({len(thread_id)}字符), 使用哈希缩短"
            )
            hash_suffix = _hashlib.sha1(thread_id.encode("utf-8")).hexdigest()[:10]
            prefix_budget = max_thread_id_length - len(hash_suffix) - 1
            thread_id = f"{thread_id[:prefix_budget]}:{hash_suffix}"

        logger.info(
            f"[{log_prefix}] 使用隔离的thread_id: {thread_id} "
            f"(user_id={user_id}, work_id={work_id}, conversation_id={conversation_id})"
        )

        return thread_id

    async def _infer_tool_policy_from_context(
        self,
        message: str,
        conversation_history: str,
        context: Optional[Dict[str, Any]],
        metadata: Optional[Dict[str, Any]] = None
    ) -> Optional[str]:
        """基于现有上下文判断是否需要调用工具（AI判定）"""
        history = (conversation_history or "").strip()
        context_payload = context if isinstance(context, dict) else {}

        has_known_context = bool(
            history
            or context_payload.get("knowledge_docs")
            or context_payload.get("worldview_data")
            or context_payload.get("selected_text")
            or context_payload.get("current_content")
            or context_payload.get("text")
        )
        if not has_known_context:
            return None

        max_history_chars = 2200
        if len(history) > max_history_chars:
            head_len = 1600
            tail_len = 400
            history = f"{history[:head_len]}\n\n...[省略部分历史]...\n\n{history[-tail_len:]}"

        knowledge_docs = context_payload.get("knowledge_docs") if isinstance(context_payload.get("knowledge_docs"), list) else []
        knowledge_titles = [doc.get("title") for doc in knowledge_docs if isinstance(doc, dict) and doc.get("title")]
        knowledge_titles = knowledge_titles[:5]

        worldview_data = context_payload.get("worldview_data") if isinstance(context_payload.get("worldview_data"), dict) else {}
        worldview_profile = {
            "characters": len(worldview_data.get("characters", []) or []),
            "locations": len(worldview_data.get("locations", []) or []),
            "settings": len(worldview_data.get("settings", []) or []),
            "glossary": len(worldview_data.get("glossary", []) or []),
            "has_guidelines": bool(worldview_data.get("guidelines"))
        }

        context_keys = [
            key for key in context_payload.keys()
            if key not in {"knowledge_docs", "worldview_data"}
        ]
        context_keys = sorted(context_keys)[:20]

        context_profile = {
            "context_keys": context_keys,
            "has_selected_text": bool(context_payload.get("selected_text") or context_payload.get("selection")),
            "has_current_content": bool(context_payload.get("current_content") or context_payload.get("text")),
            "knowledge_docs": len(knowledge_docs),
            "knowledge_titles": knowledge_titles,
            "worldview": worldview_profile,
            "has_memorypack": "memorypack" in history.lower()
        }

        if metadata:
            context_profile["context_tokens"] = metadata.get("token_count", 0)
            context_profile["has_summary"] = bool(metadata.get("has_summary"))

        prompt = (
            "你是工具策略判定器。根据用户请求和可用上下文判断是否需要调用工具。\n"
            "可选策略:\n"
            "- no_tool: 仅用现有上下文即可准确回答，不需要再读取/检索/分析工具\n"
            "- cache_only: 可能需要工具结果，但应仅允许使用缓存；若缓存未命中，不调用真实工具\n"
            "- auto: 需要调用工具获取新信息\n\n"
            "要求:\n"
            "1) 仅依据提供的上下文判断，不臆造。\n"
            "2) 如果上下文明显足够，选 no_tool。\n"
            "3) 如果上下文部分相关但不确定，优先选 auto；只有明显依赖历史工具结果才选 cache_only。\n"
            "4) 如果已有 MemoryPack 且能覆盖问题关键信息，选 no_tool。\n"
            "5) 只返回严格JSON，不要包含多余文字。\n\n"
            f"用户请求:\n{message}\n\n"
            f"可用上下文摘要:\n{history or '无'}\n\n"
            f"上下文概览(JSON):\n{json.dumps(context_profile, ensure_ascii=False)}\n"
        )

        try:
            result = await self.ai_service.call_ai(
                system_prompt="你是精确的策略判定器，只返回JSON。",
                user_prompt=prompt,
                max_tokens=200,
                temperature=0.1,
                task_type=TaskType.TEXT_CLASSIFICATION
            )
            decision = self._extract_json_from_text(result) or {}
            policy = str(decision.get("policy", "")).strip().lower()
            if policy in {"auto", "no_tool", "cache_only"}:
                reason = str(decision.get("reason", "")).strip()
                if reason:
                    logger.info(f"[ToolPolicy] 自动判定: {policy} ({reason})")
                else:
                    logger.info(f"[ToolPolicy] 自动判定: {policy}")
                return policy
        except Exception as e:
            logger.warning(f"[ToolPolicy] 自动判定失败: {e}")

        return None

    def _extract_task_dependencies(self, params: Dict[str, Any]) -> set:
        """从参数中提取依赖的任务 ID

        查找 $task_X_result 形式的占位符，返回依赖的任务 ID 集合
        """
        import re
        import json

        deps = set()
        try:
            params_str = json.dumps(params, ensure_ascii=False)
            # 匹配 $task_1_result, $task_2_result 等
            matches = re.findall(r'\$task_(\d+)_result', params_str)
            for m in matches:
                deps.add(int(m))
        except Exception as e:
            logger.warning(f"[依赖提取] 解析参数失败: {e}")

        return deps

    def _extract_json_from_text(self, text: str) -> Optional[dict]:
        """从文本提取JSON - 委托到 EventParser"""
        return EventParser.extract_json_from_text(text)

    async def chat_with_planning(
        self,
        message: str,
        user_id: Optional[str] = None,
        work_id: Optional[str] = None,
        chapter_id: Optional[str] = None,
        conversation_id: Optional[str] = None,
        context: Optional[Dict[str, Any]] = None,
        on_plan: Optional[callable] = None,
        on_task_start: Optional[callable] = None,
        on_task_progress: Optional[callable] = None,
        on_task_done: Optional[callable] = None,
        on_content: Optional[callable] = None,
        on_flow_event: Optional[callable] = None,  # v6.0: 执行轨迹事件回调
        db: Optional[Any] = None,
    ) -> Dict[str, Any]:
        """
        与 Agent 对话 - Planning + Execution 模式

        Args:
            message: 用户消息
            user_id: 用户ID（用于token记录）
            work_id: 作品ID
            chapter_id: 章节ID
            conversation_id: 会话ID
            context: 额外上下文
            on_plan: 规划生成回调
            on_task_start: 任务开始回调
            on_task_progress: 任务进度回调
            on_task_done: 任务完成回调
            on_content: 内容生成回调
            on_flow_event: 执行轨迹事件回调 (v6.0)
            db: 数据库会话（用于token记录）

        Returns:
            Dict: Agent响应
        """
        # ✅ P0-2: 添加3600秒总体超时保护（60分钟）
        try:
            import time
            from app.services.agent.utils.monitoring import increment_counter, record_timer
            start_time = time.time()

            # v7.0: 提前设置flow事件回调，确保执行阶段可发送revision事件
            if on_flow_event:
                self.stream_event_handler.set_flow_event_callback(on_flow_event)

            # ✅ P0修复：构建隔离的thread_id - 委托到公共方法
            isolated_thread_id = self._build_thread_id(user_id, work_id, conversation_id, "Planning")

            # 设置总体超时（使用统一配置）
            async with async_timeout(TimeoutConfig.TASK_EXECUTION):
                # ========== 加载对话历史（使用 ContextManager 压缩） ==========
                conversation_history = ""
                context_bundle = None  # 保存上下文包，用于后续更新
                metadata: Dict[str, Any] = {}

                # 动态设置 user_id（用于长期记忆隔离）
                if user_id:
                    self.context_manager.user_id = user_id

                try:
                    # 使用 ContextManager 构建上下文（自动压缩）
                    context_bundle = await self.context_manager.build_context(
                        session_id=isolated_thread_id,
                        system_prompt="",  # Planning 阶段不需要系统提示
                        query=message,
                        work_id=work_id,
                        chapter_id=chapter_id
                    )

                    # 从压缩后的上下文中提取历史消息
                    messages = context_bundle.get("messages", [])
                    context_obj = context_bundle.get("context")
                    metadata = context_bundle.get("metadata", {})
                    memory_pack_text = context_bundle.get("memory_pack_text")

                    if messages:
                        logger.info(
                            f"[Planning] 从 ContextManager 加载了 {len(messages)} 条历史消息 "
                            f"(token: {metadata.get('token_count', 0)}, "
                            f"has_summary: {metadata.get('has_summary', False)})"
                        )

                        history_parts = []
                        if memory_pack_text:
                            history_parts.append(memory_pack_text)

                        # ✅ 修复：提取并使用摘要信息（如果有）
                        if context_obj and context_obj.summary_memory.summary:
                            summary = context_obj.summary_memory.summary
                            history_parts.append(f"【历史对话摘要】\n{summary}")
                            logger.info(f"[Planning] 使用对话摘要: {len(summary)}字符")

                            # 添加重要事实（如果有）
                            if context_obj.summary_memory.important_facts:
                                facts = "\n".join(f"- {fact}" for fact in context_obj.summary_memory.important_facts)
                                history_parts.append(f"【重要信息】\n{facts}")

                        # 格式化近期对话消息（只取 user/assistant）
                        recent_lines = []
                        for msg in messages:
                            role = msg.get("role", "")
                            content = msg.get("content", "")
                            if role == "user":
                                recent_lines.append(f"用户: {content}")
                            elif role == "assistant":
                                recent_lines.append(f"助手: {content}")

                        if recent_lines:
                            history_parts.append("【近期对话】\n" + "\n".join(recent_lines))

                        # 注入会话级 Explore Artifact 指针（Redis 会话状态）
                        if conversation_id:
                            try:
                                from app.services.agent.utils.explore_artifact import get_session_artifacts
                                artifacts = await get_session_artifacts(conversation_id)
                                if artifacts:
                                    artifact_lines = [
                                        f"- {item.get('artifact_id')} (work_id={item.get('work_id')}) {item.get('preview', '')}"
                                        for item in artifacts
                                    ]
                                    history_parts.append("【可用探索结果】\n" + "\n".join(artifact_lines))
                                    if not isinstance(context, dict):
                                        context = {}
                                    context["session_artifacts"] = artifacts
                            except Exception as exc:
                                logger.debug(f"[Planning] 读取会话 artifact 失败: {exc}")

                        if history_parts:
                            conversation_history = "\n\n".join(history_parts)
                except Exception as e:
                    logger.warning(f"[Planning] ContextManager 加载历史失败: {e}", exc_info=True)

                tool_policy = "auto"
                forced_no_tool = False
                if metadata and metadata.get("memory_pack"):
                    memory_pack_text = context_bundle.get("memory_pack_text")
                    if memory_pack_text:
                        forced_no_tool = True
                        tool_policy = "no_tool"
                        if not isinstance(context, dict):
                            context = {}
                        context["tool_policy"] = tool_policy
                        logger.info("[Planning] MemoryPack 命中，强制 tool_policy=no_tool")

                if not forced_no_tool and context and isinstance(context.get("tool_policy"), str):
                    candidate_policy = context.get("tool_policy", "").strip().lower()
                    if candidate_policy in {"auto", "no_tool", "cache_only"}:
                        tool_policy = candidate_policy
                    else:
                        logger.warning(f"[Planning] 无效 tool_policy={candidate_policy}，已回退为 auto")

                if tool_policy == "auto":
                    inferred_policy = await self._infer_tool_policy_from_context(
                        message=message,
                        conversation_history=conversation_history,
                        context=context,
                        metadata=metadata
                    )
                    if inferred_policy in {"no_tool", "cache_only"}:
                        tool_policy = inferred_policy
                        if not isinstance(context, dict):
                            context = {}
                        context["tool_policy"] = tool_policy
                        logger.info(f"[Planning] 自动判定 tool_policy={tool_policy}，优先使用上下文/缓存")

                # ========== 快速路径判断 - 委托到 QuickPathHandler ==========
                # 在规划生成前判断是否可以走快速路径
                enable_quick_path = os.getenv("ENABLE_QUICK_PATH", "true").lower() == "true"

                if enable_quick_path and tool_policy == "auto":
                    quick_result = await self.quick_path_handler.try_quick_path(
                        message=message,
                        work_id=work_id,
                        on_plan=on_plan,
                        on_task_start=on_task_start,
                        on_task_done=on_task_done,
                        on_content=on_content,
                        on_flow_event=on_flow_event  # v6.2: 传递flow事件回调
                    )
                    if quick_result:
                        logger.info(f"[Planning] 快速路径命中，跳过规划流程")

                        # v6.2: agent_header 已在 quick_path 中发送

                        # ✅ 修复：快速路径也需要保存对话到 ContextManager
                        try:
                            await self.context_manager.update_context(
                                session_id=isolated_thread_id,
                                new_messages=[
                                    {"role": "user", "content": message},
                                    {"role": "assistant", "content": quick_result.get("response", "")}
                                ],
                                context=context_bundle.get("context") if context_bundle else None,
                                work_id=work_id,
                                chapter_id=chapter_id
                            )
                            logger.info(f"[Planning] 快速路径对话已保存到 ContextManager")
                        except Exception as e:
                            logger.warning(f"[Planning] 快速路径保存对话失败: {e}")
                        return quick_result
                elif enable_quick_path:
                    logger.info(f"[Planning] tool_policy={tool_policy}，跳过快速路径")

                # ========== 🆕 AI 意图分类（复用 IntentClassifier）==========
                # 在规划前判断：如果是普通对话，直接响应，不进入规划流程
                from app.services.agent.model_selector import TaskType

                intent, confidence = await self.intent_classifier.classify_by_ai(message)
                logger.info(f"[Planning] AI意图分类: {intent} (置信度: {confidence:.2f})")

                # ✅ 2025-12-30: 移除 general 快速路径，统一走 LangGraph 工具调用流程
                # 原因：快速路径跳过工具决策，导致无法查询世界观、读取章节等
                # 现在所有意图（包括 general）都通过 LangGraph 处理，支持工具调用
                if intent == "general" and confidence >= 0.85:
                    logger.info(f"[Planning] 识别为 general 意图，但仍走 LangGraph 流程（支持工具调用）")
                    # 不再直接响应，继续执行下面的规划流程

                # ========== 阶段1: 规划（Planning） - 委托到 PlanGenerator ==========
                planning_start = time.time()

                try:
                    plan_data = await self.plan_generator.generate_plan(
                        message=message,
                        work_id=work_id,
                        chapter_id=chapter_id,
                        context=context,
                        conversation_history=conversation_history
                    )
                except Exception as e:
                    logger.error(f"[Planning Agent] 执行失败: {e}", exc_info=True)
                    return {
                        "response": f"抱歉，规划阶段出现问题：{str(e)}。请稍后重试。",
                        "conversation_id": conversation_id or "default",
                        "agent_steps": [],
                        "suggested_actions": [],
                        "metadata": {"error": str(e), "stage": "planning", "error_type": type(e).__name__}
                    }

                # ✅ P1-7: 记录Planning阶段完成
                planning_duration = time.time() - planning_start
                logger.info(f"[Planning] 规划完成，共{len(plan_data['tasks'])}个任务，耗时: {planning_duration:.2f}s")
                record_timer("planning_phase_duration", planning_duration)

                # 回调：发送规划
                if on_plan:
                    await on_plan(plan_data)

                # v6.2: agent_header 移到 wrapped_on_task_start 中发送，确保有实际内容时才显示

                # ========== 🆕 直接回答模式：检查 direct_answer ==========
                raw_direct_answer = plan_data.get("direct_answer")
                tasks = plan_data.get("tasks", [])

                # 🔧 严格空值检查：排除空字符串和空白字符串
                has_valid_direct_answer = (
                    raw_direct_answer is not None
                    and isinstance(raw_direct_answer, str)
                    and raw_direct_answer.strip()
                )
                has_tasks = tasks and len(tasks) > 0

                # 🔧 协议违反警告：AI 同时返回 direct_answer 和 tasks
                if has_valid_direct_answer and has_tasks:
                    logger.warning(
                        f"[Planning-Alert] AI 违反协议：同时返回 direct_answer({len(raw_direct_answer)}字) "
                        f"和 {len(tasks)} 个 tasks，将执行 tasks 而忽略 direct_answer"
                    )

                # 只有当有 direct_answer 且没有 tasks 时才直接返回
                if has_valid_direct_answer and not has_tasks:
                    direct_answer = raw_direct_answer.strip()
                    logger.info(f"[Planning] 检测到 direct_answer({len(direct_answer)}字)，直接返回答案，跳过任务执行")

                    # v6.3: 先发送 output_ready（带空内容），再发送内容
                    if on_flow_event:
                        from app.services.agent.stream.flow_events import FlowEventBuilder
                        await on_flow_event(FlowEventBuilder.agent_header())
                        # 使用 AI 生成的 output_title，降级为默认值
                        output_title = plan_data.get("output_title") or "回复内容"
                        await on_flow_event(FlowEventBuilder.output_ready(output_title, "", is_applicable=False))

                    # 通过回调发送内容
                    if on_content:
                        await on_content({"content": direct_answer})

                    # 保存对话到 ContextManager
                    try:
                        await self.context_manager.update_context(
                            session_id=isolated_thread_id,
                            new_messages=[
                                {"role": "user", "content": message},
                                {"role": "assistant", "content": direct_answer}
                            ],
                            context=context_bundle.get("context") if context_bundle else None,
                            work_id=work_id,
                            chapter_id=chapter_id
                        )
                        logger.info(f"[Planning] direct_answer 对话已保存到 ContextManager")
                    except Exception as e:
                        logger.warning(f"[Planning] direct_answer 对话保存失败: {e}")

                    return {
                        "response": direct_answer,
                        "conversation_id": conversation_id or "default",
                        "agent_steps": [{
                            "step": "direct_answer",
                            "result": f"规划阶段直接回答（无需工具）",
                            "user_intent": plan_data.get("user_intent", "")
                        }],
                        "suggested_actions": [],
                        "metadata": {
                            "path": "planning_direct_answer",
                            "planning_duration": planning_duration
                        }
                    }

                # ========== 阶段2: 执行（Execution）- 智能并行执行 ==========
                # ✅ P1-7: 添加Execution阶段监控
                execution_start = time.time()
                logger.info("[Execution] 开始智能并行执行任务")
                increment_counter("execution_phase_start")

                # ✅ 2025-12-08 修复: 在执行阶段也包含 selected_text
                initial_context = f"用户请求：{message}\n\n"
                if context:
                    exec_selected_text = context.get("selected_text") or ""
                    if exec_selected_text:
                        initial_context += f"用户选中的文本：\n---\n{exec_selected_text}\n---\n\n"

                # v6.0: 包装回调以发送flow事件
                step_counter = [0]  # 使用列表以便在闭包中修改
                task_step_map = {}  # v6.1: 记录每个任务的 step_id
                agent_header_sent = [False]  # v6.2: 跟踪是否已发送agent_header

                # v6.3: 辅助函数 - 发送knowledge_loaded事件
                async def _emit_knowledge_loaded(on_flow_event, step_id, tool_name, result_data):
                    """根据工具类型解析结果并发送knowledge_loaded事件"""
                    from app.services.agent.stream.flow_events import FlowEventBuilder
                    import json as json_module
                    try:
                        # 获取结果内容
                        result_str = result_data.get("content", "") if isinstance(result_data, dict) else str(result_data)
                        if not result_str:
                            return

                        # 世界观工具
                        if tool_name in ["get_worldview_summary", "get_worldview_tool"]:
                            data = json_module.loads(result_str) if isinstance(result_str, str) else result_str
                            if "error" in data:
                                return
                            items = []
                            # 角色
                            for char in data.get("characters", []):
                                items.append({"name": f"{char.get('name', '')} - {char.get('role', '')}", "tag": "人物"})
                            # 地点
                            for loc in data.get("locations", []):
                                items.append({"name": loc.get("name", ""), "tag": "地点"})
                            # 设定
                            for setting in data.get("settings", []):
                                items.append({"name": setting.get("title", ""), "tag": "设定"})
                            if items:
                                total = len(items)
                                await on_flow_event(FlowEventBuilder.knowledge_loaded(
                                    step_id, "worldview", f"世界观已加载({total})", "BookOpen", items
                                ))

                        # 章节读取工具
                        elif tool_name in ["read_chapter_tool", "get_chapter_by_order_tool"]:
                            data = json_module.loads(result_str) if isinstance(result_str, str) else result_str
                            if "error" in data:
                                return
                            items = []
                            # 多章节格式
                            if data.get("type") == "multi_chapter":
                                for ch in data.get("chapters", [])[:5]:
                                    items.append({"name": f"{ch.get('title', '章节')} ({ch.get('word_count', 0)}字)", "tag": "章节"})
                            # 单章节格式
                            else:
                                title = data.get("title", "章节")
                                word_count = data.get("word_count", 0)
                                items = [{"name": f"{title} ({word_count}字)", "tag": "章节"}]
                            if items:
                                await on_flow_event(FlowEventBuilder.knowledge_loaded(
                                    step_id, "chapters", f"章节已读取({len(items)})", "FileText", items
                                ))

                        # 上下文获取工具
                        elif tool_name == "get_context_tool":
                            data = json_module.loads(result_str) if isinstance(result_str, str) else result_str
                            if "error" in data:
                                return
                            items = []
                            # 当前章节
                            if data.get("current_chapter") and data["current_chapter"].get("title"):
                                items.append({"name": data["current_chapter"].get("title", "当前章节"), "tag": "章节"})
                            # 相关上下文 (related_context 是实际字段名)
                            for ctx in data.get("related_context", [])[:3]:
                                items.append({"name": ctx.get("chapter_title", ""), "tag": "前文"})
                            if items:
                                await on_flow_event(FlowEventBuilder.knowledge_loaded(
                                    step_id, "chapters", f"上下文已加载({len(items)})", "FileText", items
                                ))

                        # 检索工具
                        elif tool_name == "search_analysis_fragments_tool":
                            data = json_module.loads(result_str) if isinstance(result_str, str) else result_str
                            items = []
                            # 实际返回格式是 results 字段
                            results = data.get("results", []) if isinstance(data, dict) else data if isinstance(data, list) else []
                            for f in results[:5]:
                                content = f.get("snippet") or f.get("content", "")
                                content = content[:30]
                                items.append({"name": f"{content}...", "tag": "片段", "similarity": f.get("similarity")})
                            if items:
                                await on_flow_event(FlowEventBuilder.knowledge_loaded(
                                    step_id, "search", f"检索结果({len(items)})", "Search", items
                                ))
                    except Exception as e:
                        logger.debug(f"[FlowEvent] knowledge_loaded解析失败: {e}")

                async def wrapped_on_task_start(task):
                    """包装任务开始回调，同时发送step_start事件"""
                    step_counter[0] += 1
                    current_step_id = step_counter[0]
                    # v6.1: 保存任务ID到step_id的映射
                    task_step_map[task.get("task_id")] = current_step_id
                    if on_flow_event:
                        from app.services.agent.stream.flow_events import FlowEventBuilder
                        # v6.2: 在第一个step_start之前发送agent_header
                        if not agent_header_sent[0]:
                            await on_flow_event(FlowEventBuilder.agent_header())
                            agent_header_sent[0] = True
                        # v6.1: 优先使用 title（简洁标题），回退到 description
                        step_title = task.get("title") or task.get("description", "执行任务")
                        # 同时发送 description，让前端可以立即显示（与 step_complete 保持一致的回退逻辑）
                        step_description = task.get("description") or task.get("title", "任务完成")
                        if step_description and step_title and step_description.strip() == step_title.strip():
                            step_description = None
                        await on_flow_event(FlowEventBuilder.step_start(current_step_id, step_title, step_description))
                    if on_task_start:
                        await on_task_start(task)

                async def wrapped_on_task_done(task, result_data):
                    """包装任务完成回调，同时发送step_complete事件"""
                    # v6.1: 使用保存的 step_id，而不是当前的 step_counter
                    task_id = task.get("task_id")
                    current_step_id = task_step_map.get(task_id, step_counter[0])
                    if on_flow_event:
                        from app.services.agent.stream.flow_events import FlowEventBuilder, get_tool_icon
                        tool_name = task.get("tool", "")

                        # v6.3: 发送knowledge_loaded事件（在step_complete之前）
                        await _emit_knowledge_loaded(
                            on_flow_event, current_step_id, tool_name, result_data
                        )

                        tool_call = {"icon": get_tool_icon(tool_name), "name": tool_name} if tool_name else None
                        # v6.1: step_complete 的 description 可以保持详细，用于日志
                        await on_flow_event(FlowEventBuilder.step_complete(
                            current_step_id,
                            task.get("description") or task.get("title", "任务完成"),
                            tool_call
                        ))
                    if on_task_done:
                        await on_task_done(task, result_data)

                # 使用新的并行执行方法
                # ✅ 为任务执行添加超时保护（使用统一配置）
                try:
                    async with async_timeout(TimeoutConfig.TASK_EXECUTION):
                        shared_state = {
                            "work_id": work_id,
                            "chapter_id": chapter_id,
                            "context": context if isinstance(context, dict) else {},
                            "tool_policy": tool_policy,
                            "task_step_map": task_step_map,
                        }
                        task_results = await self._execute_tasks_in_parallel(
                            tasks=plan_data["tasks"],
                            work_id=work_id,
                            chapter_id=chapter_id,
                            context=initial_context,
                            context_payload=context,
                            on_task_start=wrapped_on_task_start,  # v6.0: 使用包装回调
                            on_task_progress=on_task_progress,
                            on_task_done=wrapped_on_task_done,  # v6.0: 使用包装回调
                            conversation_id=conversation_id,  # v8.0: 传递 conversation_id 用于操作日志
                            state=shared_state
                        )
                except asyncio.TimeoutError:
                    logger.error(f"[Execution] 任务执行超时（{TimeoutConfig.TASK_EXECUTION}秒）")
                    return {
                        "response": "抱歉，任务执行超时。请尝试简化您的请求。",
                        "conversation_id": conversation_id or "default",
                        "plan": plan_data,
                        "task_results": [],
                        "agent_steps": [],
                        "suggested_actions": ["简化请求", "稍后重试"],
                        "metadata": {"error": "Task execution timeout", "timeout": TimeoutConfig.TASK_EXECUTION}
                    }

                # 构建完整上下文用于后续总结
                all_context = initial_context
                for result in task_results:
                    all_context += f"\n任务{result['task_id']}结果：\n{result['result']}\n"

                # ✅ P1-7: 记录Execution阶段完成
                execution_duration = time.time() - execution_start
                logger.info(f"[Execution] 所有任务执行完成，共{len(task_results)}个任务，耗时: {execution_duration:.2f}s")
                increment_counter("execution_phase_completed")
                record_timer("execution_phase_duration", execution_duration)

                # ========== 阶段3: 智能返回（Response） ==========
                logger.info("[Response] 生成最终响应")

                # ✅ P0修复: 从context中获取知识库文档，传递给_build_final_response
                knowledge_docs_for_response = context.get("knowledge_docs") if context else None

                # v6.3: 判断 is_applicable
                CONTENT_GENERATION_TOOLS = {'smart_continue', 'smart_create', 'smart_rewrite', 'smart_insert'}
                is_applicable = False

                for result in task_results:
                    tool_name = result.get('tool', '')
                    if tool_name in CONTENT_GENERATION_TOOLS:
                        is_applicable = True
                    try:
                        result_data = result.get('result')
                        if isinstance(result_data, str):
                            parsed = json.loads(result_data)
                            if parsed.get('requires_confirmation'):
                                is_applicable = True
                    except (json.JSONDecodeError, TypeError):
                        pass

                # v6.3: 使用 AI 生成的 output_title，降级为默认值
                output_title = plan_data.get("output_title") or "生成内容"

                # v6.5: 设置 stream_event_handler 的回调，用于 Summarization 和 output_ready 事件
                if on_flow_event:
                    self.stream_event_handler.set_flow_event_callback(on_flow_event)

                # 使用新的智能判断方法
                # ✅ 传递 response_hint 用于元数据查询的精准返回
                # v6.5: 传递 output_title 和 is_applicable，在 summarization_complete 后发送 output_ready
                final_content = await self._build_final_response(
                    task_results=task_results,
                    message=message,
                    on_content=on_content,
                    response_hint=plan_data.get("response_hint"),
                    knowledge_docs=knowledge_docs_for_response,  # ✅ P0修复: 传递知识库文档
                    direct_answer=plan_data.get("direct_answer"),  # ✅ 分阶段执行：传递 direct_answer
                    output_title=output_title,  # v6.5: 传递 output_title
                    is_applicable=is_applicable  # v6.5: 传递 is_applicable
                )

                # v6.3: 内容生成完成后，更新 output_ready 的 title（可选）
                # 注意：内容已通过 on_content 流式发送，这里只更新元数据

                # v6.0: completion事件移到API层发送，确保在所有内容输出完成后才显示
                # 原因：此处发送completion时，on_content的内容可能还在队列中未发送到前端

                # ========== 保存对话到 ContextManager ==========
                try:
                    await self.context_manager.update_context(
                        session_id=isolated_thread_id,
                        new_messages=[
                            {"role": "user", "content": message},
                            {"role": "assistant", "content": final_content}
                        ],
                        context=context_bundle.get("context") if context_bundle else None,
                        work_id=work_id,
                        chapter_id=chapter_id
                    )
                    logger.info(f"[Planning] 已保存对话到 ContextManager (session={isolated_thread_id})")
                except Exception as e:
                    logger.warning(f"[Planning] 保存对话到 ContextManager 失败: {e}")

                return {
                    "response": final_content,
                    "conversation_id": conversation_id or "default",
                    "plan": plan_data,
                    "task_results": task_results,
                    "agent_steps": [
                        {"step": "planning", "result": f"生成了{len(plan_data['tasks'])}个任务"},
                        {"step": "execution", "result": f"完成了{len(task_results)}个任务"},
                        {"step": "summarization", "result": "生成最终响应"}
                    ],
                    "suggested_actions": [],
                    "metadata": {
                        "intent": plan_data.get("user_intent"),
                        "total_tasks": len(plan_data["tasks"]),
                        "completed_tasks": len([t for t in task_results if t["status"] == "completed"]),
                        "timestamp": str(get_utc_now())
                    }
                }

        except asyncio.TimeoutError:
            # 总体超时处理
            elapsed = time.time() - start_time
            timeout_seconds = TimeoutConfig.TASK_EXECUTION
            timeout_minutes = max(1, int(timeout_seconds / 60))
            logger.error(f"[Planning] 总体超时（{elapsed:.1f}秒，限制{timeout_seconds}秒）")
            increment_counter("chat_with_planning_error", labels={"error_type": "TimeoutError"})

            return {
                "response": f"抱歉，请求处理超时（超过{timeout_minutes}分钟）。您的请求可能过于复杂，建议：\n1. 简化请求内容\n2. 分步骤进行操作\n3. 稍后重试",
                "conversation_id": conversation_id or "default",
                "agent_steps": [],
                "suggested_actions": ["简化请求", "分步操作", "稍后重试"],
                "metadata": {
                    "error": "Overall timeout",
                    "timeout_seconds": timeout_seconds,
                    "elapsed_seconds": elapsed
                }
            }

        except Exception as e:
            logger.error(f"[Planning Agent] 执行失败: {e}", exc_info=True)
            return {
                "response": f"抱歉，处理您的请求时出错了：{str(e)}",
                "conversation_id": conversation_id or "default",
                "agent_steps": [],
                "suggested_actions": [],
                "metadata": {"error": str(e)}
            }

    async def _execute_tasks_in_parallel(
        self,
        tasks: List[Dict[str, Any]],
        work_id: str,
        chapter_id: str,
        context: str,
        context_payload: Optional[Dict[str, Any]] = None,
        on_task_start: Optional[callable] = None,
        on_task_progress: Optional[callable] = None,
        on_task_done: Optional[callable] = None,
        conversation_id: Optional[str] = None,  # v8.0: 添加 conversation_id 用于操作日志
        state: Optional[Dict[str, Any]] = None  # 🆕 2026-01-12: 添加 state 用于章节缓存
    ) -> List[Dict[str, Any]]:
        """智能并行执行任务 - 委托到 ParallelExecutor

        Args:
            tasks: 任务列表
            work_id: 作品ID
            chapter_id: 章节ID
            context: 上下文
            context_payload: 结构化上下文（原始 request.context）
            on_task_start: 任务开始回调
            on_task_progress: 任务进度回调
            on_task_done: 任务完成回调
            conversation_id: 会话ID（用于操作日志记录）
            state: Agent 状态（用于章节缓存）

        Returns:
            任务结果列表
        """
        return await self.parallel_executor.execute_tasks(
            tasks=tasks,
            work_id=work_id,
            chapter_id=chapter_id,
            context=context,
            context_payload=context_payload,
            on_task_start=on_task_start,
            on_task_progress=on_task_progress,
            on_task_done=on_task_done,
            conversation_id=conversation_id,
            state=state  # 🆕 传递 state 用于章节缓存
        )

    # ==================== 规划响应（委托到 ResponseBuilder）====================

    def _classify_tasks(self, task_results: List[Dict]) -> Dict[str, List]:
        """分类任务 - 委托到 planning 模块"""
        return classify_tasks(task_results)

    async def _build_final_response(
        self,
        task_results: List[Dict],
        message: str,
        on_content: Optional[callable] = None,
        response_hint: Optional[str] = None,
        knowledge_docs: Optional[List[Dict]] = None,  # ✅ P0修复: 添加知识库文档参数
        direct_answer: Optional[str] = None,  # ✅ 分阶段执行：传递 direct_answer
        output_title: Optional[str] = None,  # v6.5: 输出标题
        is_applicable: bool = False  # v6.5: 是否可应用
    ) -> str:
        """智能构建最终响应

        根据任务类型智能判断是否需要AI整合：
        - 缺失前置条件 → 直接返回友好提示（优先级最高）
        - 单个创作任务 → 直接返回（节省AI调用）
        - 多个输出任务 → 简单拼接（节省AI调用）
        - 其他情况 → AI整合

        Args:
            task_results: 任务结果列表
            message: 用户原始消息
            on_content: 内容回调函数
            response_hint: 响应提示（如 "title", "word_count"），用于元数据查询
            knowledge_docs: 用户引用的知识库文档列表（可选）

        Returns:
            最终响应内容
        """
        # ✅ 优先检查：是否有缺失前置条件或积分不足的情况
        # 如果有工具返回了特殊状态，直接返回友好提示，跳过AI整合
        for result in task_results:
            try:
                result_str = result.get('result', '')
                if not result_str:
                    continue

                # 尝试解析为JSON
                result_json = json.loads(result_str)

                # 检查是否为missing_prerequisite状态
                if result_json.get('status') == 'missing_prerequisite':
                    suggested = result_json.get('suggested_response', '')

                    if suggested:
                        logger.info(
                            f"[Response] 检测到missing_prerequisite "
                            f"(缺失: {result_json.get('missing', 'unknown')}), "
                            f"直接返回友好提示，跳过AI整合"
                        )

                        # ✅ 方案B修复：直接发送整个内容（比分块发送更快）
                        if on_content:
                            await on_content(suggested)

                        return suggested

                # ✅ 检查是否为积分不足错误（tool_failed + 积分相关消息）
                if result_json.get('error') == 'tool_failed':
                    error_msg = result_json.get('message', '')
                    if "积分" in error_msg and ("不足" in error_msg or "余额" in error_msg):
                        friendly_msg = "积分余额不足，请先充值后再使用此功能。"
                        logger.info(
                            f"[Response] 检测到积分不足错误，"
                            f"直接返回友好提示，跳过AI整合"
                        )

                        if on_content:
                            await on_content(friendly_msg)

                        return friendly_msg

            except (json.JSONDecodeError, TypeError, KeyError):
                # 不是JSON或格式不对，继续下一个
                continue

        # 分类任务
        classified = self._classify_tasks(task_results)
        output_tasks = classified["output_tasks"]
        display_tasks = classified["display_tasks"]  # ✅ P2-1修复

        # ✅ P2-1修复: 情况0 - 纯展示型任务（用户只是查看数据）
        # 当所有任务都是展示型任务时，直接格式化返回，不需要AI整合
        if len(output_tasks) == 0 and len(display_tasks) > 0:
            logger.info(
                f"[Response] 纯展示型任务({len(display_tasks)}个)，"
                f"直接格式化返回（跳过AI整合，节省成本）"
            )
            return await self._format_display_response(display_tasks, response_hint, on_content)

        # 情况1：没有输出任务（极少见）
        if len(output_tasks) == 0:
            # ✅ 分阶段执行：如果有 direct_answer，说明是创作请求的第一阶段
            # 调用AI整合，基于获取的信息（如世界观）生成询问
            if direct_answer:
                logger.info("[Response] 分阶段执行第一阶段，基于任务结果生成询问")
                # 使用AI整合，会基于世界观内容生成针对性的询问
                return await self._ai_summarization(task_results, message, on_content, knowledge_docs, output_title, is_applicable)

            logger.warning("[Response] 没有明确输出任务，使用AI整合")
            return await self._ai_summarization(task_results, message, on_content, knowledge_docs, output_title, is_applicable)

        # 情况2：单个输出任务（主要场景，约85%）
        elif len(output_tasks) == 1:
            task = output_tasks[0]
            tool_name = task.get("tool", "unknown")  # ✅ 安全访问
            result = task.get("result", "") or ""  # 处理None的情况

            # ✅ 方案B修复：使用@知识库时，走AI整合路径（真流式）
            # 当有知识库文档时，需要AI基于文档内容生成响应，确保流式输出
            if knowledge_docs:
                logger.info(
                    f"[Response] 检测到知识库文档({len(knowledge_docs)}个)，"
                    f"使用AI整合（确保流式输出）"
                )
                return await self._ai_summarization(task_results, message, on_content, knowledge_docs, output_title, is_applicable)

            # v6.4: 所有单个输出任务都走AI整合路径（确保Summarization事件）
            logger.info(f"[Response] 单个输出任务({tool_name})，使用AI整合")
            return await self._ai_summarization(task_results, message, on_content, knowledge_docs, output_title, is_applicable)

        # 情况3：多个输出任务（约15%）
        else:
            # ✅ 方案B修复：使用@知识库时，走AI整合路径（真流式）
            if knowledge_docs:
                logger.info(
                    f"[Response] 检测到知识库文档({len(knowledge_docs)}个)，"
                    f"{len(output_tasks)}个输出任务，使用AI整合（确保流式输出）"
                )
                return await self._ai_summarization(task_results, message, on_content, knowledge_docs, output_title, is_applicable)

            # ✅ 方案B优化：检查是否全是分析/摘要类任务
            analysis_like_tools = {"analyze_text_tool", "summarization", "analyze_content"}
            all_analyze = all(
                task.get("tool") in analysis_like_tools
                for task in output_tasks
            )
            has_writing = any(
                task.get("tool") in {"smart_continue", "smart_create", "smart_rewrite", "smart_insert"}
                for task in output_tasks
            )

            # 多个分析/摘要任务 → AI整合（避免冗余拼接）
            if all_analyze and not has_writing:
                logger.info(f"[Response] {len(output_tasks)}个分析类任务，使用AI整合（避免冗余）")
                return await self._ai_summarization(task_results, message, on_content, knowledge_docs, output_title, is_applicable)

            # v6.4: 多个输出任务（包含续写）→ 也使用AI整合（确保Summarization事件）
            logger.info(f"[Response] {len(output_tasks)}个输出任务（含续写），使用AI整合")
            return await self._ai_summarization(task_results, message, on_content, knowledge_docs, output_title, is_applicable)

    async def _format_display_response(
        self,
        display_tasks: List[Dict],
        response_hint: Optional[str] = None,
        on_content: Optional[callable] = None
    ) -> str:
        """格式化展示型任务的响应 - 委托到 ResponseBuilder"""
        return await self.response_builder.format_display_response(
            display_tasks=display_tasks,
            response_hint=response_hint,
            on_content=on_content
        )

    async def _ai_summarization(
        self,
        task_results: List[Dict],
        message: str,
        on_content: Optional[callable] = None,
        knowledge_docs: Optional[List[Dict]] = None,
        output_title: Optional[str] = None,  # v6.5: 输出标题
        is_applicable: bool = False  # v6.5: 是否可应用
    ) -> str:
        """AI整合 - 委托到 ResponseBuilder"""
        return await self.response_builder.ai_summarization(
            task_results=task_results,
            message=message,
            on_content=on_content,
            knowledge_docs=knowledge_docs,
            output_title=output_title,
            is_applicable=is_applicable
        )

    async def _execute_task(
        self,
        task: Dict[str, Any],
        work_id: str,
        chapter_id: str,
        context: str,
        context_payload: Optional[Dict[str, Any]] = None,
        on_progress: Optional[callable] = None,
        conversation_id: Optional[str] = None,  # v8.0: 添加 conversation_id 用于操作日志
        state: Optional[Dict[str, Any]] = None  # 🆕 2026-01-12: 添加 state 用于章节缓存
    ) -> str:
        """执行单个任务 - 委托到 TaskRunner

        Args:
            task: 任务配置
            work_id: 作品ID
            chapter_id: 章节ID
            context: 上下文
            context_payload: 结构化上下文（原始 request.context）
            on_progress: 进度回调
            conversation_id: 会话ID（用于操作日志记录）
            state: Agent 状态（用于章节缓存）

        Returns:
            任务执行结果
        """
        result = await self.task_runner.execute_task(
            task=task,
            work_id=work_id,
            chapter_id=chapter_id,
            context=context,
            context_payload=context_payload,
            on_progress=on_progress,
            conversation_id=conversation_id,
            state=state  # 🆕 传递 state 用于章节缓存
        )
        # v7.0: 检测HITL确认请求并发送审批/修订事件
        await self._handle_hitl_tool_result(task, result, work_id=work_id, chapter_id=chapter_id)
        return result

    async def _handle_hitl_tool_result(
        self,
        task: Dict[str, Any],
        tool_result: Any,
        work_id: Optional[str] = None,
        chapter_id: Optional[str] = None
    ) -> None:
        """处理工具结果中的HITL确认请求（Planning路径）"""
        if not tool_result:
            return
        tool_name = task.get("tool", "")
        params = task.get("params", {}) or {}

        result_obj = None
        if isinstance(tool_result, dict):
            result_obj = tool_result
        elif isinstance(tool_result, str):
            try:
                result_obj = json.loads(tool_result)
            except Exception:
                result_obj = None

        if not (isinstance(result_obj, dict) and result_obj.get("requires_confirmation")):
            # 🔧 2026-01-10: 严格分离 - CREATIVE 工具只返回内容，不触发编辑器操作
            # 移除了 smart_continue 的自动转换逻辑
            # 只有 OPERATION 工具（返回 requires_confirmation=True）才会触发修订请求
            return

        # 构建审批数据
        original_content = (
            result_obj.get("original_text")
            or result_obj.get("original_content")
            or result_obj.get("old_title")
        )
        # v8.1: 智能解析 new_content - 如果是 JSON 字符串，提取其中的 content 字段
        new_content = (
            result_obj.get("content")
            or result_obj.get("new_content")
            or result_obj.get("new_title")
        )
        if isinstance(new_content, str) and new_content.strip().startswith('{'):
            try:
                parsed = json.loads(new_content)
                if isinstance(parsed, dict) and 'content' in parsed:
                    new_content = parsed['content']
                    logger.info(f"[HITL] 从 JSON 中提取 content 字段")
            except json.JSONDecodeError:
                pass

        request_id = result_obj.get("request_id") or f"{tool_name}_{uuid.uuid4().hex}"
        approval_data = {
            "request_id": request_id,
            "action_type": result_obj.get("action_type", "edit"),
            "operation": result_obj.get("operation"),
            "original_content": original_content,
            "new_content": new_content,
            "description": result_obj.get("description"),
            "versions": result_obj.get("versions") or result_obj.get("recommendations"),
            "chapter_id": result_obj.get("chapter_id"),
            "chapter_title": result_obj.get("chapter_title"),
            "work_id": result_obj.get("work_id"),
            "old_title": result_obj.get("old_title"),
            "new_title": result_obj.get("new_title"),
            "editor_action": result_obj.get("editor_action"),
            "position": result_obj.get("position")  # v7.5: 添加 position 字段
        }

        # v8.1: Ensure editor_action exists and carries location data when available.
        editor_action = result_obj.get("editor_action")
        if not isinstance(editor_action, dict):
            editor_action = {}

        operation = approval_data.get("operation")
        position_value = result_obj.get("position")

        # Build position payload from tool result if present.
        if position_value is not None:
            if isinstance(position_value, dict) and "from" in position_value:
                position_payload = position_value
            else:
                position_payload = {"from": position_value, "to": position_value}
        else:
            position_payload = None

        inferred_type = "modify"
        if operation == "append":
            inferred_type = "continue"
        elif operation == "insert":
            inferred_type = "insert"
        elif operation == "replace":
            inferred_type = "modify"

        if "type" not in editor_action:
            editor_action["type"] = inferred_type
        if "position" not in editor_action:
            editor_action["position"] = position_payload
        if "requires_confirmation" not in editor_action:
            editor_action["requires_confirmation"] = True

        # 🔧 2026-01-11: 复制定位字段，并确保 paragraph_index 是整数类型
        for key in ("before_anchor", "after_anchor", "node_id", "paragraph_index", "original_text"):
            if key not in editor_action:
                value = result_obj.get(key)
                if value is not None:
                    # 确保 paragraph_index 是整数
                    if key == "paragraph_index":
                        try:
                            value = int(value)
                        except (ValueError, TypeError):
                            logger.warning(f"[HITL] paragraph_index 类型转换失败: {value}")
                            continue
                    editor_action[key] = value

        approval_data["editor_action"] = editor_action

        # 调用审批回调（用于前端通知）
        callback_result = None
        if self._approval_callback:
            try:
                callback_result = await self._approval_callback(approval_data)
            except Exception as e:
                logger.warning(f"[HITL] 审批回调执行失败: {e}")

        if isinstance(callback_result, dict) and callback_result.get("request_id"):
            request_id = callback_result.get("request_id")
        elif isinstance(callback_result, str):
            request_id = callback_result

        # 构建 revision 事件
        action_type = approval_data.get("action_type", "edit")
        operation = approval_data.get("operation")
        revision_type_map = {
            "rewrite": "replace",
            "edit": "replace",
            "continue": "append",
            "insert": "insert",
            "create": "create",
            "rename": "rename"
        }
        revision_type = revision_type_map.get(action_type, "replace")
        if operation == "append":
            revision_type = "append"
        elif operation == "insert":
            revision_type = "insert"

        content_preview = None
        if new_content:
            content_preview = new_content[:50] if len(new_content) > 50 else new_content

        await self.stream_event_handler.emit_revision(
            revision_type=revision_type,
            request_id=request_id,
            chapter_id=approval_data.get("chapter_id"),
            chapter_title=approval_data.get("chapter_title"),
            content=new_content,
            content_preview=content_preview,
            original_content=original_content,
            position=approval_data.get("position"),
            operation=operation,
            editor_action=approval_data.get("editor_action"),
            old_title=approval_data.get("old_title"),
            new_title=approval_data.get("new_title"),
            versions=approval_data.get("versions")
        )

    # 🔧 2026-01-10: 已移除 _should_promote_continue_task 方法
    # CREATIVE 工具严格分离，不再自动转换为修订请求

    async def _fallback_legacy_execute(
        self,
        tool_name: str,
        params: dict,
        work_id: str,
        chapter_id: str,
        context: str
    ) -> str:
        """降级执行 - 委托到 TaskRunner"""
        return await self.task_runner._fallback_legacy_execute(
            tool_name=tool_name,
            params=params,
            work_id=work_id,
            chapter_id=chapter_id,
            context=context
        )


# ==================== 导出 ====================

__all__ = ["WritingAgentGraph", "AgentState"]
 
