# -*- coding: utf-8 -*-
"""
LangGraph Agent 工作流实现

使用 LangGraph 框架实现智能写作助手，支持：
- 4个核心场景（写作/规划/分析/卡文）
- 工具调用（HTTPAIService集成）
- 记忆管理（Checkpointer）
- 人机协同（HITL）

重构说明（2025-12-09）：
- 工具函数拆分到 langgraph_tools.py
- 上下文构建拆分到 utils/context_builder.py
"""

from typing import TypedDict, Annotated, List, Dict, Any, Optional, Literal
from datetime import datetime
import os
from langgraph.graph import StateGraph, END
from langgraph.prebuilt import ToolNode
from app.services.agent.parallel_tool_node import ParallelToolNode
from langgraph.checkpoint.redis import AsyncRedisSaver
from langchain_core.messages import HumanMessage, AIMessage, SystemMessage, ToolMessage
import operator
import logging
import httpx
import uuid
import asyncio
import threading  # ✅ P0-2修复: 添加threading以支持线程锁
import redis
import json
import re

from app.services.ai.http_ai_service import HTTPAIService
from app.core.config import settings
from app.core.database import AsyncSessionLocal
from app.services.agent.prompts import NovelPhase, PhaseCharacteristics
from app.services.agent.prompt_library import get_content_prompt
from app.services.agent.model_selector import TaskType
from app.services.agent.prompt_cache import get_tool_decision_static_prompt, get_planning_static_prompt, get_planning_agent_mode_prompt, get_complexity_decision_prompt
from app.services.agent.progress_tracker import ProgressTracker
from app.services.agent.node_metadata import get_node_info
# DeepAgent 反思系统
from app.services.agent.deep_agent import DeepAgentExecutor
from app.services.agent.timeout_config import TimeoutConfig, async_timeout
from app.services.context.context_config import ContextConfig
from app.services.agent.tools.editor_tools import (
    smart_continue,
    smart_rewrite,
    smart_insert,
    apply_chapter_edit
)
# 🔧 2025-12-14: 导入 registry 用于统一工具调用
from app.services.agent.tools import registry
from app.utils.datetime_utils import get_utc_now

# ✅ 拆分模块导入
from app.services.agent.langgraph_tools import (
    # 全局服务管理
    set_global_ai_service,
    get_global_ai_service,
    # 辅助函数
    validate_uuid,
    _retry_on_failure,
    _generate_text_helper,
    # 工具列表 & 单个工具（LangGraph 节点内直接调用）
    LANGGRAPH_TOOLS,
    continue_writing_tool,
    analyze_text_tool,
    read_chapter_tool,
    get_chapter_by_order_tool,
    get_context_tool,
    search_analysis_fragments_tool,
)
from app.services.agent.utils.context_builder import (
    _compress_task_result,
    _build_summarization_context,
    _build_knowledge_system_messages,
)

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


# ==================== 工具列表（从 langgraph_tools 导入）====================

# 使用 LANGGRAPH_TOOLS 替代原 WRITING_TOOLS
WRITING_TOOLS = LANGGRAPH_TOOLS


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

        # 构建图
        self.graph = self._build_graph()

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

    def _build_graph(self) -> StateGraph:
        """
        构建 LangGraph 工作流

        完整工作流结构：
        START
          ↓
        intent_classifier (分类意图)
          ↓
        [条件路由]
          ├─> writing_agent (生成AIMessage + tool_calls)
          ├─> planning_agent (生成AIMessage + tool_calls)
          ├─> analysis_agent (生成AIMessage + tool_calls)
          ├─> stuck_agent (生成AIMessage + tool_calls)
          └─> general_chat (直接响应)
          ↓
        [条件判断: 是否需要工具?]
          ├─> YES → tools (ToolNode执行工具)
          └─> NO  → END
          ↓
        [工具执行后返回Agent]
          ↓
        Agent节点 (处理工具结果，生成最终响应)
          ↓
        END
        """

        # ✅ 回滚开关：支持快速禁用 CoT 快速路径
        enable_quick_path = os.getenv("ENABLE_QUICK_PATH", "true").lower() == "true"

        # 创建图
        workflow = StateGraph(AgentState)

        # 添加节点
        if enable_quick_path:
            # ✅ CoT 快速路径：使用增强版意图识别
            workflow.add_node("intent_classifier", self._classify_intent_with_cot)
            # ✅ 新增快速执行节点
            workflow.add_node("quick_tool_execute", self._quick_tool_execute)
            workflow.add_node("direct_response", self._direct_response)
        else:
            # 回滚模式：使用原有意图分类
            logger.warning("[LangGraph] CoT 快速路径已禁用，使用原有流程")
            workflow.add_node("intent_classifier", self._classify_intent)
        # 原有 Agent 节点
        workflow.add_node("writing_agent", self._handle_writing)
        workflow.add_node("planning_agent", self._handle_planning)
        workflow.add_node("analysis_agent", self._handle_analysis)
        workflow.add_node("stuck_agent", self._handle_stuck)
        workflow.add_node("general_chat", self._handle_general)
        # 🟢 Phase 3.7: 使用ParallelToolNode替代标准ToolNode，支持并行执行
        workflow.add_node("tools", ParallelToolNode(
            WRITING_TOOLS,
            max_concurrent=5  # 最大并发数（基于数据库连接池大小）
        ))

        # 设置入口点
        workflow.set_entry_point("intent_classifier")

        # 添加条件边：根据意图/CoT 结果路由到不同节点
        if enable_quick_path:
            # ✅ CoT 模式：支持快速路径
            workflow.add_conditional_edges(
                "intent_classifier",
                self._route_after_intent_cot,
                {
                    # 新增快速路径
                    "quick_tool_execute": "quick_tool_execute",
                    "direct_response": "direct_response",
                    # 原有路径
                    "writing_agent": "writing_agent",
                    "planning_agent": "planning_agent",
                    "analysis_agent": "analysis_agent",
                    "stuck_agent": "stuck_agent",
                    "general_chat": "general_chat"
                }
            )

            # ✅ 快速路径直接结束
            workflow.add_edge("quick_tool_execute", END)
            workflow.add_edge("direct_response", END)
        else:
            # 回滚模式：使用原有路由
            workflow.add_conditional_edges(
                "intent_classifier",
                self._route_intent,
                {
                    "writing": "writing_agent",
                    "planning": "planning_agent",
                    "analysis": "analysis_agent",
                    "stuck": "stuck_agent",
                    "general": "general_chat"
                }
            )

        # 各Agent节点添加条件边：判断是否需要调用工具
        for agent_node in ["writing_agent", "planning_agent", "analysis_agent", "stuck_agent"]:
            workflow.add_conditional_edges(
                agent_node,
                self._should_continue,
                {
                    "continue": "tools",  # 需要工具 → 执行工具
                    "end": END  # 不需要工具 → 结束
                }
            )

        # 工具执行后，根据意图返回对应的Agent节点（让Agent处理工具结果）
        workflow.add_conditional_edges(
            "tools",
            self._route_after_tools,
            {
                "writing": "writing_agent",
                "planning": "planning_agent",
                "analysis": "analysis_agent",
                "stuck": "stuck_agent"
            }
        )

        # 一般对话直接结束
        workflow.add_edge("general_chat", END)

        # 编译图
        return workflow.compile(checkpointer=self.checkpointer)

    def _should_continue(self, state: AgentState) -> Literal["continue", "end"]:
        """判断是否需要继续执行工具"""
        messages = state["messages"]
        last_message = messages[-1]

        # 如果最后一条消息是 AIMessage 且包含 tool_calls，则继续执行工具
        if isinstance(last_message, AIMessage) and last_message.tool_calls:
            logger.info(f"[LangGraph] 检测到工具调用: {len(last_message.tool_calls)} 个工具")
            return "continue"

        # 否则结束
        logger.info("[LangGraph] 无需工具调用，结束流程")
        return "end"

    def _route_after_tools(self, state: AgentState) -> str:
        """工具执行后路由回对应的Agent"""
        intent = state.get("intent", "general")
        logger.info(f"[LangGraph] 工具执行完毕，路由回: {intent}_agent")
        return intent

    # ==================== 2025-12-14: 统一工具调用接口 ====================

    async def _call_tool_via_registry(
        self,
        tool_name: str,
        tool_args: dict,
        state: dict
    ) -> str:
        """通过 registry 统一调用工具（StandardTool 优先，@tool 兜底）

        Args:
            tool_name: 工具名称
            tool_args: 工具参数
            state: Agent 状态

        Returns:
            str: 工具执行结果（字符串格式）
        """
        # 工具名称映射（@tool 名称 → StandardTool 名称）
        TOOL_NAME_MAPPING = {
            "continue_writing_tool": "continue_writing",
            "analyze_text_tool": "analyze_text",
            "smart_rewrite": "smart_rewrite",
            "smart_continue": "smart_continue",
            "smart_insert": "smart_insert",
            "apply_chapter_edit": "apply_chapter_edit",
            # 章节工具（2025-12-14: 新增）
            "get_context_tool": "get_context",
            "read_chapter_tool": "read_chapter",
            "get_chapter_by_order_tool": "get_chapter_by_order",
            "search_analysis_fragments_tool": "search_analysis_fragments",
            # 分析工具（2025-12-15: 新增 evaluate_quality 别名支持）
            "evaluate_quality_tool": "evaluate_quality",
            "analyze_content_tool": "analyze_content",
        }

        # 规范化工具名称
        normalized_name = TOOL_NAME_MAPPING.get(tool_name, tool_name)

        try:
            # 准备参数
            params = self._prepare_tool_params(normalized_name, tool_args, state)

            # 调用 StandardTool
            result = await registry.call_tool(normalized_name, params)

            # 提取返回值
            if isinstance(result, dict) and result.get("success"):
                tool_result = self._extract_tool_result(normalized_name, result)
                logger.info(f"[StandardTool] {normalized_name} 执行成功")
                return tool_result
            else:
                error_msg = result.get("message", "执行失败") if isinstance(result, dict) else "未知错误"
                logger.error(f"[StandardTool] {normalized_name} 执行失败: {error_msg}")
                return json.dumps({"error": "tool_failed", "message": error_msg}, ensure_ascii=False)

        except ValueError as e:
            # StandardTool 不存在，降级到 @tool
            logger.warning(f"[StandardTool] '{normalized_name}' 不存在，降级到 @tool: {e}")
            return await self._fallback_to_legacy_tool(tool_name, tool_args, state)

        except Exception as e:
            # 其他错误，也尝试降级
            logger.error(f"[StandardTool] 调用失败: {e}")
            return await self._fallback_to_legacy_tool(tool_name, tool_args, state)

    def _prepare_tool_params(
        self,
        tool_name: str,
        tool_args: dict,
        state: dict
    ) -> dict:
        """准备工具参数（处理特殊情况）"""
        params = dict(tool_args)
        last_user_message = state.get("last_user_message", "")

        # 工具特定的参数处理
        if tool_name == "continue_writing":
            params.setdefault("context", last_user_message)
            params.setdefault("requirements", "")
            params.setdefault("target_length", 500)
            params.setdefault("style", "")

        elif tool_name == "analyze_text":
            params.setdefault("text", last_user_message)
            params.setdefault("focus", "all")

        elif tool_name == "smart_rewrite":
            # 编辑器工具：智能改写
            params.setdefault("chapter_id", state.get("chapter_id", ""))
            params.setdefault("text_to_rewrite", None)
            params.setdefault("chapter_content", None)
            params.setdefault("user_requirement", None)
            params.setdefault("base_version", None)
            params.setdefault("user_id", state.get("user_id"))

        elif tool_name == "smart_continue":
            # 编辑器工具：智能续写
            params.setdefault("chapter_id", state.get("chapter_id", ""))
            params.setdefault("user_id", state.get("user_id"))

        elif tool_name == "smart_insert":
            # 编辑器工具：智能插入
            params.setdefault("chapter_id", state.get("chapter_id", ""))
            params.setdefault("chapter_content", None)
            params.setdefault("context", None)
            params.setdefault("user_id", state.get("user_id"))

        elif tool_name == "apply_chapter_edit":
            # 章节编辑工具
            params.setdefault("chapter_id", state.get("chapter_id", ""))
            params.setdefault("operation", "append")
            params.setdefault("position", None)
            params.setdefault("user_id", state.get("user_id"))
            params.setdefault("description", None)

        # 章节工具（2025-12-14: 新增）
        elif tool_name == "get_context":
            params.setdefault("work_id", state.get("work_id", ""))
            params.setdefault("chapter_id", state.get("chapter_id", ""))

        elif tool_name == "read_chapter":
            params.setdefault("work_id", state.get("work_id", ""))
            params.setdefault("chapter_id", state.get("chapter_id", ""))

        elif tool_name == "get_chapter_by_order":
            params.setdefault("work_id", state.get("work_id", ""))
            params.setdefault("chapter_order", 1)

        elif tool_name == "search_analysis_fragments":
            params.setdefault("work_id", state.get("work_id", ""))
            params.setdefault("query", last_user_message)
            params.setdefault("top_k", 5)
            params.setdefault("chapter_id", state.get("chapter_id", ""))
            params.setdefault("include_current", True)
            params.setdefault("look_ahead", 2)

        # 🔧 2025-12-15: 新增 evaluate_quality 参数处理
        elif tool_name == "evaluate_quality":
            # 参数别名映射：text -> content（兼容规划器生成的参数）
            if "text" in params and "content" not in params:
                params["content"] = params.pop("text")
            params.setdefault("content", last_user_message)
            params.setdefault("context", "novel")
            params.setdefault("criteria", ["readability", "creativity", "coherence", "engagement"])
            params.setdefault("reference", "")

        # 🔧 2025-12-15: 新增 analyze_content 参数处理
        elif tool_name == "analyze_content":
            params.setdefault("content", last_user_message)
            params.setdefault("aspects", ["grammar", "logic", "style", "structure"])
            params.setdefault("depth", "normal")
            params.setdefault("context", "")

        return params

    def _extract_tool_result(self, tool_name: str, result: dict) -> str:
        """从 StandardTool 返回值中提取实际结果"""
        data = result.get("data", {})

        # 根据不同工具提取不同字段
        if tool_name == "continue_writing":
            return data.get("generated_text", "")

        elif tool_name == "analyze_text":
            return data.get("analysis_report", "")

        elif tool_name in ["smart_rewrite", "smart_continue", "smart_insert", "apply_chapter_edit"]:
            # 编辑器工具返回完整的 data（包含版本、确认请求等）
            return json.dumps(data, ensure_ascii=False)

        # 章节工具（2025-12-14: 新增）
        elif tool_name == "get_context":
            return data.get("context", "")

        elif tool_name == "read_chapter":
            return data.get("chapter_info", "")

        elif tool_name == "get_chapter_by_order":
            return data.get("chapter_info", "")

        elif tool_name == "search_analysis_fragments":
            return data.get("fragments", "")

        # 🔧 2025-12-15: 新增分析工具结果提取
        elif tool_name == "evaluate_quality":
            # 返回格式化的评估报告
            feedback = data.get("feedback", "")
            overall_score = data.get("overall_score", 0)
            grade = data.get("grade", "B")
            return f"评分: {overall_score}/100 (等级: {grade})\n\n{feedback}"

        elif tool_name == "analyze_content":
            # 返回分析报告
            return data.get("analysis", data.get("summary", ""))

        # 默认返回整个 data（JSON 字符串）
        return json.dumps(data, ensure_ascii=False)

    async def _fallback_to_legacy_tool(
        self,
        tool_name: str,
        tool_args: dict,
        state: dict
    ) -> str:
        """降级到 @tool 版本（向后兼容）"""
        from app.services.agent.langgraph_tools import (
            continue_writing_tool,
            analyze_text_tool,
        )
        from app.services.agent.tools.editor_tools import (
            smart_rewrite,
            smart_continue,
            smart_insert,
            apply_chapter_edit,
        )

        last_user_message = state.get("last_user_message", "")

        LEGACY_TOOLS = {
            "continue_writing_tool": continue_writing_tool,
            "analyze_text_tool": analyze_text_tool,
            "smart_rewrite": smart_rewrite,
            "smart_continue": smart_continue,
            "smart_insert": smart_insert,
            "apply_chapter_edit": apply_chapter_edit,
        }

        legacy_tool = LEGACY_TOOLS.get(tool_name)
        if legacy_tool:
            logger.info(f"[LegacyTool] 使用 @tool 版本: {tool_name}")
            try:
                # 准备参数（与原有逻辑一致）
                if tool_name == "continue_writing_tool":
                    params = {
                        "context": tool_args.get("context", last_user_message),
                        "requirements": tool_args.get("requirements", "")
                    }
                elif tool_name == "analyze_text_tool":
                    params = {
                        "text": tool_args.get("text", last_user_message),
                        "focus": tool_args.get("focus", "all")
                    }
                else:
                    # 编辑器工具直接使用 tool_args
                    params = tool_args

                return await legacy_tool.ainvoke(params)
            except Exception as e:
                logger.error(f"[LegacyTool] 调用失败: {e}")
                return json.dumps({"error": "legacy_tool_failed", "message": str(e)}, ensure_ascii=False)

        # 工具完全不存在
        logger.error(f"[ToolCall] 未知工具: {tool_name}")
        return json.dumps({"error": "unknown_tool", "message": f"未知工具: {tool_name}"}, ensure_ascii=False)

    # ==================== 原有方法继续 ====================

    async def _generate_text(
        self,
        prompt: Optional[str] = None,
        messages: Optional[List] = None,  # ✅ 新增：支持消息列表（修复记忆问题）
        temperature: float = 0.7,
        max_tokens: int = 1000,
        task_type: Optional[TaskType] = None
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
                    task_type=task_type  # ← 传递task_type
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

    def _classify_intent_by_rules(self, message: str) -> tuple[str, float]:
        """基于规则的快速意图识别（<1ms）

        Args:
            message: 用户消息内容

        Returns:
            tuple[str, float]: (intent类型, 置信度)
        """
        msg = message.lower().strip()

        # ========== 极简快速通道（只处理极端情况）==========
        # 这里只处理明显不需要AI判断的情况，其他全部交给AI

        # 1. 空消息或纯空白
        if not msg or len(msg.strip()) == 0:
            logger.info("[Intent] 空消息，判定为 general")
            return "general", 0.99

        # 2. 纯标点/表情（长度<=3且无中文字母数字）
        if len(msg) <= 3 and not re.search(r'[\u4e00-\u9fa5a-zA-Z0-9]', msg):
            logger.info(f"[Intent] 纯标点/表情: {msg}，判定为 general")
            return "general", 0.99

        # 3. 章节模式强匹配（这是明确的写作意图，可以快速判断）
        chapter_pattern = r'第[一二三四五六七八九十\d]+章|chapter\s*\d+'
        if re.search(chapter_pattern, msg, re.IGNORECASE):
            logger.info(f"[Intent] 匹配章节模式: {re.findall(chapter_pattern, msg, re.IGNORECASE)}")
            return "writing", 0.98

        # ========== 其他情况交给AI判断 ==========
        # 不再使用硬编码关键词列表，让AI做语义理解
        logger.info("[Intent] 交给AI进行语义分类")
        return "unknown", 0.3  # 低置信度，强制触发AI判断

    async def _ai_classify_intent(self, message: str) -> tuple[str, float]:
        """使用AI进行意图分类（兜底方案）

        当规则匹配置信度不足时，调用轻量级LLM判断意图

        Args:
            message: 用户消息

        Returns:
            tuple[str, float]: (intent类型, 置信度)
        """
        prompt = f"""你是意图分类器。根据用户消息判断其意图类型。

用户消息: "{message}"

可选意图类型:
- writing: 用户明确要求修改、改写、续写、创作内容（必须有明确的写作指令词）
- planning: 用户想要规划大纲、设计角色、构建世界观
- analysis: 用户想要分析、评估、诊断文本质量
- stuck: 用户写作卡住了、需要灵感或建议
- general: 普通对话、闲聊、问答、不确定的情况

判断规则:
1. 只有明确包含写作指令（如"帮我改"、"续写"、"修改第X章"）才判定为 writing
2. 简短的问候、寒暄、疑问句应判定为 general
3. 如果消息含义模糊或不确定，优先判定为 general
4. 不要过度解读用户意图，除非用户明确表达了写作需求

只返回一个单词（writing/planning/analysis/stuck/general），不要解释:"""

        try:
            # 使用快速模型进行意图分类
            from app.services.agent.model_selector import TaskType

            result = await self.ai_service.call_ai(
                system_prompt="你是精确的意图分类器，只返回一个意图类型单词。",
                user_prompt=prompt,
                max_tokens=20,  # 只需要一个单词
                temperature=0.1,  # 低温度，确保稳定输出
                task_type=TaskType.TEXT_CLASSIFICATION
            )

            # 解析结果
            intent = result.strip().lower()
            valid_intents = ["writing", "planning", "analysis", "stuck", "general"]

            if intent in valid_intents:
                logger.info(f"[Intent] AI识别结果: {intent}")
                return intent, 0.90
            else:
                # 尝试从返回中提取有效意图
                for valid in valid_intents:
                    if valid in intent:
                        logger.info(f"[Intent] AI识别结果（提取）: {valid}")
                        return valid, 0.85

                logger.warning(f"[Intent] AI返回无效意图: {intent}，降级为general")
                return "general", 0.70

        except Exception as e:
            logger.error(f"[Intent] AI意图分类失败: {e}，降级为general")
            return "general", 0.60

    async def _classify_intent(self, state: AgentState) -> AgentState:
        """意图分类节点 - AI优先，极简规则快速通道

        🆕 支持 selected_text: 当检测到编辑器选中文字时，自动判定为 writing 意图
        """
        logger.info("[LangGraph] 意图分类（AI优先架构）")

        last_message = state["messages"][-1].content
        context = state.get("context", {})

        # 🔍 调试日志：检查 context 内容
        logger.info(f"[Intent] 📥 state.context 字段:")
        logger.info(f"  - context keys: {list(context.keys()) if context else '空'}")
        logger.info(f"  - selected_text: {context.get('selected_text', 'N/A')[:50] + '...' if context.get('selected_text') else 'N/A'}")
        logger.info(f"  - selection_position: {context.get('selection_position', 'N/A')}")

        # 🆕 检测选中文字 - 如果有选中文字，强制判定为 writing
        selected_text = context.get("selected_text", "")
        if selected_text and len(selected_text.strip()) > 0:
            logger.info(f"[Intent] 检测到 selected_text ({len(selected_text)} 字符)，强制判定为 writing")
            return {
                "intent": "writing",
                "agent_steps": [{
                    "step": "intent_classification",
                    "result": "识别意图: writing (编辑器选中文字模式)",
                    "usage": {}
                }]
            }

        # 1. 极简规则快速通道（只处理极端情况）
        intent, confidence = self._classify_intent_by_rules(last_message)
        classification_method = "快速通道"

        # 2. 非极端情况（confidence < 0.9）全部使用AI判断
        if confidence < 0.9:
            logger.info(f"[Intent] 触发AI语义分类（规则置信度={confidence:.2f}）")
            ai_intent, ai_confidence = await self._ai_classify_intent(last_message)
            intent = ai_intent
            confidence = ai_confidence
            classification_method = "AI语义分类"
            logger.info(f"[Intent] AI分类结果: {intent} ({confidence:.2f})")

        logger.info(
            f"[Intent] 最终结果: {intent}, 置信度: {confidence:.2f}, 方法: {classification_method}"
        )

        # ✅ 只返回节点新增/修改的字段，避免 operator.add 重复添加
        return {
            "intent": intent,
            "agent_steps": [{
                "step": "intent_classification",
                "result": f"识别意图: {intent} ({classification_method})",
                "usage": {}  # Token消耗在AI调用中已记录
            }]
        }

    def _route_intent(self, state: AgentState) -> str:
        """路由决策函数"""
        intent = state.get("intent", "general")
        logger.info(f"[LangGraph] 路由到: {intent}")
        return intent

    # ==================== CoT 快速路径（新增）====================

    async def _classify_intent_with_cot(self, state: AgentState) -> AgentState:
        """增强版意图识别 - 在现有分类基础上增加复杂度判断

        流程：
        1. 调用现有的意图分类逻辑（复用 _classify_intent_by_rules + _ai_classify_intent）
        2. 新增：判断复杂度（simple/complex）
        3. 新增：如果 simple，确定执行方案

        🆕 支持 selected_text: 当检测到编辑器选中文字时，自动判定为 writing 意图

        Returns:
            AgentState: 包含 intent, intent_decision, agent_steps
        """
        message = state["messages"][-1].content
        context = state.get("context", {})
        logger.info(f"[Intent-CoT] 开始分析: {message[:50]}...")

        # 🆕 检测选中文字 - 如果有选中文字，强制判定为 writing/complex
        selected_text = context.get("selected_text", "")
        if selected_text and len(selected_text.strip()) > 0:
            logger.info(f"[Intent-CoT] 检测到 selected_text ({len(selected_text)} 字符)，强制判定为 writing/complex")
            return {
                "intent": "writing",
                "intent_decision": {"complexity": "complex", "action": {}},
                "agent_steps": [{
                    "step": "intent_cot",
                    "result": "writing/complex (编辑器选中文字模式)",
                }]
            }

        # ========== 步骤1: 复用现有意图分类 ==========
        intent, confidence = self._classify_intent_by_rules(message)
        classification_method = "快速通道"

        if confidence < 0.9:
            intent, confidence = await self._ai_classify_intent(message)
            classification_method = "AI语义分类"

        logger.info(f"[Intent-CoT] 意图: {intent} ({classification_method})")

        # ========== 步骤2: 复杂度判断 ==========
        # writing/planning/analysis/stuck 意图默认为 complex
        if intent in ("writing", "planning", "analysis", "stuck"):
            logger.info(f"[Intent-CoT] {intent} 意图默认为 complex")
            return {
                "intent": intent,
                "intent_decision": {"complexity": "complex", "action": {}},
                "agent_steps": [{
                    "step": "intent_cot",
                    "result": f"{intent}/complex (默认)",
                }]
            }

        # general 意图需要进一步判断复杂度
        complexity_decision = await self._judge_complexity(message, intent)

        logger.info(
            f"[Intent-CoT] 决策: intent={intent}, "
            f"complexity={complexity_decision.get('complexity', 'complex')}"
        )

        return {
            "intent": intent,
            "intent_decision": complexity_decision,
            "agent_steps": [{
                "step": "intent_cot",
                "result": f"{intent}/{complexity_decision.get('complexity', 'complex')}",
            }]
        }

    async def _judge_complexity(self, message: str, intent: str) -> Dict:
        """判断请求复杂度并确定执行方案

        Args:
            message: 用户消息
            intent: 已识别的意图类型

        Returns:
            Dict: {"complexity": "simple|complex", "action": {...}}
        """
        prompt_template = await get_complexity_decision_prompt()
        prompt = prompt_template.format(intent=intent, message=message)

        try:
            result = await self.ai_service.call_ai(
                system_prompt="你是执行路径决策器，返回严格的JSON格式。",
                user_prompt=prompt,
                max_tokens=300,
                temperature=0.1,
                task_type=TaskType.TEXT_CLASSIFICATION
            )

            decision = self._extract_json_from_text(result)
            if decision and decision.get("complexity"):
                return decision

        except Exception as e:
            logger.warning(f"[Intent-CoT] 复杂度判断失败: {e}，降级为 complex")

        # 降级：默认为 complex
        return {"complexity": "complex", "action": {}}

    def _route_after_intent_cot(self, state: AgentState) -> str:
        """根据 CoT 结果路由到对应节点

        路由规则：
        - simple + direct_answer → direct_response 节点（新增）
        - simple + tool_name → quick_tool_execute 节点（新增）
        - complex → 原有 Agent 节点（按意图路由）

        Returns:
            str: 目标节点名称
        """
        decision = state.get("intent_decision", {})
        complexity = decision.get("complexity", "complex")
        action = decision.get("action", {})
        intent = state.get("intent", "general")

        # ========== 快速路径（新增）==========
        if complexity == "simple":
            if action.get("direct_answer"):
                logger.info("[Route-CoT] → direct_response (直接回答)")
                return "direct_response"
            elif action.get("tool_name"):
                logger.info(f"[Route-CoT] → quick_tool_execute ({action['tool_name']})")
                return "quick_tool_execute"

        # ========== 原有路径（保持不变）==========
        # 复杂请求走原有的 Agent 节点
        route_map = {
            "writing": "writing_agent",
            "planning": "planning_agent",
            "analysis": "analysis_agent",
            "stuck": "stuck_agent",
            "general": "general_chat",
        }
        target = route_map.get(intent, "general_chat")
        logger.info(f"[Route-CoT] → {target} (complex)")
        return target

    async def _quick_tool_execute(self, state: AgentState) -> AgentState:
        """快速执行单工具（新增节点，跳过完整 Agent 流程）

        用于 simple + tool 场景，直接调用工具并格式化返回。

        Returns:
            AgentState: 包含 final_response, agent_steps
        """
        decision = state.get("intent_decision", {})
        action = decision.get("action", {})

        tool_name = action.get("tool_name")
        tool_args = action.get("tool_args", {})
        response_hint = action.get("response_hint")

        logger.info(f"[QuickExecute] 执行工具: {tool_name}, 参数: {tool_args}")

        # 1. 获取工具函数
        tool_func = self._get_tool_by_name(tool_name)
        if not tool_func:
            return {
                "final_response": f"抱歉，无法执行该操作（未知工具: {tool_name}）",
                "agent_steps": [{"step": "quick_tool_execute", "result": "工具不存在"}]
            }

        # 2. 执行工具
        try:
            # 添加 work_id 参数（如果工具需要）
            work_id = state.get("work_id")

            # ✅ 检查 work_id 是否存在（某些工具需要）
            tools_need_work_id = {"get_chapter_by_order_tool", "get_context_tool", "read_chapter_tool"}
            if tool_name in tools_need_work_id and not work_id:
                return {
                    "final_response": "需要先选择一部作品才能执行此操作。请告诉我您要查看哪部作品？",
                    "agent_steps": [{"step": "quick_tool_execute", "result": "缺少 work_id"}]
                }

            if work_id and "work_id" not in tool_args:
                tool_args["work_id"] = work_id

            result = await tool_func.ainvoke(tool_args)
        except Exception as e:
            logger.error(f"[QuickExecute] 工具执行失败: {e}")
            return {
                "final_response": f"工具执行失败: {str(e)}",
                "agent_steps": [{"step": "quick_tool_execute", "result": f"错误: {e}"}]
            }

        # 3. 根据 hint 格式化响应
        response = self._format_tool_response(result, tool_args, response_hint)

        return {
            "final_response": response,
            "agent_steps": [{
                "step": "quick_tool_execute",
                "result": f"执行 {tool_name}",
            }]
        }

    async def _direct_response(self, state: AgentState) -> AgentState:
        """直接返回答案（新增节点，无需工具）

        用于 simple + direct_answer 场景。

        Returns:
            AgentState: 包含 final_response, agent_steps
        """
        decision = state.get("intent_decision", {})
        action = decision.get("action", {})
        answer = action.get("direct_answer", "")

        logger.info(f"[DirectResponse] 返回预设答案")

        return {
            "final_response": answer,
            "agent_steps": [{
                "step": "direct_response",
                "result": "直接回答"
            }]
        }

    def _get_tool_by_name(self, tool_name: str):
        """根据名称获取工具函数

        维护一个工具名到函数的映射表。
        """
        # 从全局工具列表中查找
        for tool in WRITING_TOOLS:
            if tool.name == tool_name:
                return tool
        return None

    def _format_tool_response(
        self,
        result: Any,
        tool_args: Dict,
        response_hint: Optional[str]
    ) -> str:
        """格式化工具响应

        根据 response_hint 提取特定字段并格式化为用户友好的响应。
        """
        # 解析 result（可能是 JSON 字符串）
        if isinstance(result, str):
            try:
                result = json.loads(result)
            except json.JSONDecodeError:
                return result

        if not response_hint or not isinstance(result, dict):
            return str(result)

        chapter_order = tool_args.get("chapter_order", "")

        if response_hint == "title":
            title = result.get("title", "未知")
            return f"第{chapter_order}章的标题是：**{title}**"

        elif response_hint == "word_count":
            word_count = result.get("word_count", 0)
            return f"第{chapter_order}章共 **{word_count}** 字"

        elif response_hint == "content":
            return result.get("content", "")

        elif response_hint == "title_and_word_count":
            title = result.get("title", "未知")
            word_count = result.get("word_count", 0)
            return f"第{chapter_order}章「{title}」共 **{word_count}** 字"

        else:
            return str(result)

    # ==================== Planning 模式快速路径（新增）====================

    async def _try_quick_path_for_planning(
        self,
        message: str,
        work_id: Optional[str],
        on_plan: Optional[callable] = None,
        on_task_start: Optional[callable] = None,
        on_task_done: Optional[callable] = None,
        on_content: Optional[callable] = None
    ) -> Optional[Dict[str, Any]]:
        """Planning 模式的快速路径判断

        在规划生成前判断是否可以走快速路径，适用于简单查询：
        - 获取章节标题
        - 获取章节字数
        - 简单问候

        Args:
            message: 用户消息
            work_id: 作品 ID
            on_plan: 规划回调
            on_task_start: 任务开始回调
            on_task_done: 任务完成回调
            on_content: 内容回调

        Returns:
            Optional[Dict]: 如果命中快速路径返回结果，否则返回 None
        """
        import time

        # 1. 规则快速判断（不调用 AI）
        quick_action = self._detect_quick_action(message)

        if not quick_action:
            return None

        action_type = quick_action.get("type")
        logger.info(f"[QuickPath-Planning] 命中快速路径: {action_type}")

        # 2. 执行快速路径
        start_time = time.time()

        try:
            if action_type == "get_chapter_info":
                # 获取章节信息
                chapter_order = quick_action.get("chapter_order", 1)
                field = quick_action.get("field", "title")  # title, word_count, content

                if not work_id:
                    return {
                        "response": "需要先选择一部作品才能查看章节信息。",
                        "agent_steps": [{"step": "quick_path", "result": "缺少 work_id"}]
                    }

                # 发送简化的计划
                if on_plan:
                    await on_plan([{
                        "task_id": 1,
                        "description": f"获取第{chapter_order}章信息"
                    }])

                if on_task_start:
                    await on_task_start({"task_id": 1, "description": f"获取第{chapter_order}章信息"})

                # 直接调用工具
                result = await get_chapter_by_order_tool.ainvoke({
                    "work_id": work_id,
                    "chapter_order": chapter_order
                })

                elapsed = time.time() - start_time
                if on_task_done:
                    await on_task_done({
                        "task_id": 1,
                        "description": f"获取第{chapter_order}章信息",
                        "elapsed_time": elapsed
                    })

                # 解析结果
                try:
                    if isinstance(result, dict):
                        data = result  # 已经是 dict
                    elif isinstance(result, list):
                        # 如果是 list，取第一个元素或转换
                        data = result[0] if result and isinstance(result[0], dict) else {"content": str(result)}
                    else:
                        data = json.loads(result)
                except (json.JSONDecodeError, TypeError, IndexError) as e:
                    logger.warning(f"[QuickPath-Planning] 解析结果失败: {e}, result type: {type(result)}")
                    data = {"error": str(result)}

                # 格式化响应
                if data.get("error"):
                    response = f"获取章节信息失败：{data.get('error')}"
                elif field == "title":
                    response = f"第{chapter_order}章的标题是：**{data.get('title', '未知')}**"
                elif field == "word_count":
                    response = f"第{chapter_order}章共 **{data.get('word_count', 0)}** 字"
                else:
                    title = data.get('title', '未知')
                    word_count = data.get('word_count', 0)
                    response = f"第{chapter_order}章「{title}」共 **{word_count}** 字"

                if on_content:
                    await on_content({"content": response})

                logger.info(f"[QuickPath-Planning] 完成，耗时: {elapsed:.2f}s")

                return {
                    "response": response,
                    "agent_steps": [{
                        "step": "quick_path",
                        "action": action_type,
                        "elapsed": elapsed
                    }]
                }

            elif action_type == "greeting":
                # 问候直接回复
                response = quick_action.get("response", "你好！我是 AI 写作助手，有什么可以帮你的吗？")

                if on_content:
                    await on_content({"content": response})

                return {
                    "response": response,
                    "agent_steps": [{"step": "quick_path", "action": "greeting"}]
                }

        except Exception as e:
            logger.warning(f"[QuickPath-Planning] 执行失败: {e}，降级到规划模式")
            return None

        return None

    def _detect_quick_action(self, message: str) -> Optional[Dict]:
        """规则检测是否可以走快速路径（不调用 AI）

        Returns:
            Dict: {"type": "get_chapter_info", "chapter_order": 5, "field": "title"}
            或 None
        """
        import re

        message = message.strip()

        # 1. 问候检测
        greetings = ["你好", "您好", "在吗", "hello", "hi", "嗨"]
        if any(message.lower().startswith(g) for g in greetings) and len(message) < 10:
            return {
                "type": "greeting",
                "response": "你好！我是 AI 写作助手，有什么可以帮你的吗？"
            }

        # 2. 章节标题查询
        # 匹配："第五章的标题是什么"、"第5章标题"、"第三章叫什么"
        title_patterns = [
            r'第([一二三四五六七八九十百千\d]+)章.{0,2}(?:的)?(?:标题|题目|名字|叫什么)',
            r'(?:标题|题目|名字).{0,2}第([一二三四五六七八九十百千\d]+)章',
        ]
        for pattern in title_patterns:
            match = re.search(pattern, message)
            if match:
                chapter_str = match.group(1)
                chapter_order = self._chinese_to_number(chapter_str)
                return {
                    "type": "get_chapter_info",
                    "chapter_order": chapter_order,
                    "field": "title"
                }

        # 3. 章节字数查询
        # 匹配："第三章有多少字"、"第5章字数"
        word_count_patterns = [
            r'第([一二三四五六七八九十百千\d]+)章.{0,3}(?:有)?(?:多少|几)(?:个)?字',
            r'第([一二三四五六七八九十百千\d]+)章.{0,2}(?:的)?字数',
        ]
        for pattern in word_count_patterns:
            match = re.search(pattern, message)
            if match:
                chapter_str = match.group(1)
                chapter_order = self._chinese_to_number(chapter_str)
                return {
                    "type": "get_chapter_info",
                    "chapter_order": chapter_order,
                    "field": "word_count"
                }

        # 4. 不符合快速路径条件
        return None

    def _chinese_to_number(self, s: str) -> int:
        """中文数字转阿拉伯数字"""
        chinese_map = {
            '零': 0, '一': 1, '二': 2, '三': 3, '四': 4,
            '五': 5, '六': 6, '七': 7, '八': 8, '九': 9,
            '十': 10, '百': 100, '千': 1000
        }

        # 纯数字
        if s.isdigit():
            return int(s)

        # 简单中文数字（1-99）
        if len(s) == 1 and s in chinese_map:
            return chinese_map[s]

        # "十"、"十一"、"二十"、"二十三" 等
        result = 0
        if '十' in s:
            parts = s.split('十')
            tens = chinese_map.get(parts[0], 1) if parts[0] else 1
            ones = chinese_map.get(parts[1], 0) if len(parts) > 1 and parts[1] else 0
            result = tens * 10 + ones
        else:
            # 单个字符
            result = chinese_map.get(s, 1)

        return result if result > 0 else 1

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

    async def _handle_agent_with_tools(self, state: AgentState, agent_type: str, system_prompt: str) -> AgentState:
        """
        通用的Agent处理逻辑 - 使用HTTPAIService手动工具调用
        """
        logger.info(f"[LangGraph] 处理{agent_type}场景")
        return await self._handle_with_httpai(state, agent_type, system_prompt)

    async def _handle_with_httpai(self, state: AgentState, agent_type: str, system_prompt: str, recursion_depth: int = 0) -> AgentState:
        """HTTPAIService 模式 - 手动工具调用（绕过 Cloudflare）

        Args:
            state: Agent状态
            agent_type: Agent类型
            system_prompt: 系统提示词
            recursion_depth: 递归深度（默认0）✅ P0-3修复
        """
        # ✅ P0-3修复：检查递归深度，防止无限递归
        MAX_RECURSION_DEPTH = 5  # 最多允许5层递归（原始调用 + 4次工具调用）
        if recursion_depth > MAX_RECURSION_DEPTH:
            logger.error(
                f"[LangGraph] ❌ 递归深度超限: {recursion_depth} > {MAX_RECURSION_DEPTH}，"
                f"可能存在工具循环调用，强制终止"
            )
            return {
                "messages": [AIMessage(content="抱歉，处理您的请求时遇到了问题（递归深度超限），请简化您的需求后重试。")],
                "final_response": "递归深度超限，已强制终止",
                "agent_steps": [{
                    "step": f"{agent_type}_recursion_limit",
                    "result": f"递归深度{recursion_depth}超过限制{MAX_RECURSION_DEPTH}"
                }]
            }

        messages = state["messages"]

        # 检查是否已经有工具结果（第二次进入）
        if messages and isinstance(messages[-1], ToolMessage):
            logger.info(f"[LangGraph] {agent_type} - 处理工具执行结果 (HTTPAIService)")

            # 获取用户原始请求（第一条HumanMessage）
            user_message = ""
            for msg in messages:
                if isinstance(msg, HumanMessage):
                    user_message = msg.content
                    break

            # 使用 HTTPAIService 基于工具结果生成最终响应
            tool_result = messages[-1].content

            logger.info(f"[LangGraph] 🔍 工具返回内容长度: {len(tool_result)} 字符")
            logger.info(f"[LangGraph] 🔍 工具返回内容预览:\n{tool_result[:500]}")

            # ✅ 新增：检查是否需要二次工具调用（特别是编辑器工具）
            # 场景：用户说"修改第2章"，AI先调get_chapter_by_order_tool获取chapter_id，
            # 然后应该调用smart_rewrite进行实际修改
            modify_keywords = ["修改", "改写", "重写", "续写", "插入", "帮我改", "你来改",
                             "来帮我改", "改一下", "太平淡", "帮改", "改改"]
            needs_second_tool = any(kw in user_message for kw in modify_keywords)

            # 检查是否已经执行过二次工具调用(避免无限递归)
            already_did_second_call = state.get("_second_tool_called", False)

            if needs_second_tool and agent_type == "writing" and not already_did_second_call:
                logger.info(f"[LangGraph] 🔄 检测到编辑意图，尝试二次工具调用")

                # 提取工具返回的chapter_id（如果有）
                import json
                import re
                chapter_id_from_tool = None
                try:
                    tool_data = json.loads(tool_result)
                    # 尝试从多个可能的路径提取chapter_id
                    chapter_id_from_tool = (
                        tool_data.get("chapter_id") or
                        (tool_data.get("current_chapter") or {}).get("id") or
                        (tool_data.get("chapter") or {}).get("id")
                    )
                except:
                    pass

                if chapter_id_from_tool:
                    logger.info(f"[LangGraph] ✅ 提取到chapter_id: {chapter_id_from_tool[:20]}...")

                    # 更新state中的chapter_id（供后续使用）
                    state["chapter_id"] = chapter_id_from_tool

                    # 构建二次工具决策prompt
                    second_decision_prompt = f"""用户原始请求：{user_message}

第一次工具调用已获取章节信息，chapter_id: {chapter_id_from_tool}

现在判断是否需要第二次工具调用来完成用户的实际编辑需求。

可用的编辑器工具：
- smart_rewrite: 改写/修改章节内容 (参数: chapter_id, instructions)
- smart_continue: 续写章节 (参数: chapter_id, context)
- smart_insert: 插入内容 (参数: chapter_id, position, content)

⚠️ 重要规则：
1. 用户说"修改"、"改写"、"重写" → 使用 smart_rewrite
2. 用户说"续写"、"继续写" → 使用 smart_continue
3. 用户说"插入" → 使用 smart_insert
4. 必须严格返回JSON格式！

返回JSON:
{{"need_tools": true, "tool_name": "工具名", "tool_args": {{"chapter_id": "{chapter_id_from_tool}", "instructions": "根据用户要求..."}}}}

或者如果不需要工具：
{{"need_tools": false, "direct_response": "..."}}

请返回JSON:"""

                    # 调用AI做二次工具决策
                    second_result = await self._generate_text(
                        messages=[{
                            "role": "system",
                            "content": system_prompt
                        }, {
                            "role": "user",
                            "content": second_decision_prompt
                        }],
                        max_tokens=200,
                        temperature=0.3,
                        task_type=TaskType.SIMPLE_QA
                    )
                    second_decision_text = second_result.get("text", "")
                    logger.info(f"[LangGraph] 🔄 二次工具决策原文: {second_decision_text}")

                    # 解析二次决策
                    second_decision = None
                    try:
                        second_decision = json.loads(second_decision_text.strip())
                    except:
                        # 尝试正则提取
                        json_matches = re.finditer(r'\{(?:[^{}]|(?:\{[^}]*\}))*\}', second_decision_text)
                        for match in json_matches:
                            try:
                                candidate = json.loads(match.group())
                                if "need_tools" in candidate:
                                    second_decision = candidate
                                    break
                            except:
                                continue

                    # 如果需要调用第二个工具
                    if second_decision and second_decision.get("need_tools", False):
                        tool_name = second_decision.get("tool_name", "")
                        tool_args = second_decision.get("tool_args", {})

                        logger.info(f"[LangGraph] 🚀 准备二次工具调用: {tool_name}, args={tool_args}")

                        # 直接调用编辑器工具
                        second_tool_result = ""
                        try:
                            if tool_name == "smart_rewrite":
                                # ✅ 智能版本引用
                                base_version = tool_args.get("base_version", "")
                                last_versions = state.get("context", {}).get("last_rewrite_versions", {})
                                if base_version and last_versions:
                                    resolved = self._resolve_version_reference(base_version, last_versions)
                                    if resolved:
                                        logger.info(f"[LangGraph] 🔄 二次调用智能版本解析: '{base_version}' → 完整内容({len(resolved)}字)")
                                        base_version = resolved

                                logger.info(f"[LangGraph] 🚀 二次调用 smart_rewrite, chapter_id={tool_args.get('chapter_id')}, user_requirement={tool_args.get('user_requirement', '')[:30]}")
                                # 🔧 2025-12-14: 统一使用 registry
                                try:
                                    result = await registry.call_tool("smart_rewrite", {
                                        "chapter_id": tool_args.get("chapter_id", ""),
                                        "text_to_rewrite": tool_args.get("text_to_rewrite", ""),
                                        "chapter_content": None,
                                        "user_requirement": tool_args.get("user_requirement", ""),
                                        "base_version": base_version,
                                        "user_id": state.get("user_id")
                                    })
                                    if isinstance(result, dict) and result.get("success"):
                                        second_tool_result = json.dumps(result.get("data", {}), ensure_ascii=False)
                                    else:
                                        second_tool_result = json.dumps(result, ensure_ascii=False)
                                except Exception as e:
                                    logger.warning(f"[StandardTool] 二次调用 smart_rewrite 失败，降级: {e}")
                                    second_tool_result = await smart_rewrite.ainvoke({
                                        "chapter_id": tool_args.get("chapter_id", ""),
                                        "text_to_rewrite": tool_args.get("text_to_rewrite", ""),
                                        "chapter_content": None,  # 🔧 补充
                                        "user_requirement": tool_args.get("user_requirement", ""),
                                        "base_version": base_version,
                                        "user_id": state.get("user_id")  # 🔧 补充 user_id
                                    })
                            elif tool_name == "smart_continue":
                                logger.info(f"[LangGraph] 🚀 二次调用 smart_continue, chapter_id={tool_args.get('chapter_id')}")
                                # 🔧 2025-12-14: 统一使用 registry
                                try:
                                    result = await registry.call_tool("smart_continue", {
                                        "chapter_id": tool_args.get("chapter_id", ""),
                                        "content": tool_args.get("context", ""),
                                        "user_id": state.get("user_id")
                                    })
                                    if isinstance(result, dict) and result.get("success"):
                                        second_tool_result = json.dumps(result.get("data", {}), ensure_ascii=False)
                                    else:
                                        second_tool_result = json.dumps(result, ensure_ascii=False)
                                except Exception as e:
                                    logger.warning(f"[StandardTool] 二次调用 smart_continue 失败，降级: {e}")
                                    second_tool_result = await smart_continue.ainvoke({
                                        "chapter_id": tool_args.get("chapter_id", ""),
                                        "content": tool_args.get("context", ""),  # 🔧 参数名修正
                                        "user_id": state.get("user_id")
                                    })
                            elif tool_name == "smart_insert":
                                logger.info(f"[LangGraph] 🚀 二次调用 smart_insert, chapter_id={tool_args.get('chapter_id')}")
                                # 🔧 2025-12-14: 统一使用 registry
                                try:
                                    result = await registry.call_tool("smart_insert", {
                                        "chapter_id": tool_args.get("chapter_id", ""),
                                        "content": tool_args.get("content", ""),
                                        "user_intent": tool_args.get("position", "end"),
                                        "chapter_content": None,
                                        "context": None,
                                        "user_id": state.get("user_id")
                                    })
                                    if isinstance(result, dict) and result.get("success"):
                                        second_tool_result = json.dumps(result.get("data", {}), ensure_ascii=False)
                                    else:
                                        second_tool_result = json.dumps(result, ensure_ascii=False)
                                except Exception as e:
                                    logger.warning(f"[StandardTool] 二次调用 smart_insert 失败，降级: {e}")
                                    second_tool_result = await smart_insert.ainvoke({
                                        "chapter_id": tool_args.get("chapter_id", ""),
                                        "content": tool_args.get("content", ""),
                                        "user_intent": tool_args.get("position", "end"),  # 🔧 参数名映射
                                        "chapter_content": None,  # 🔧 补充
                                        "context": None,  # 🔧 补充
                                        "user_id": state.get("user_id")  # 🔧 补充 user_id
                                    })
                            elif tool_name == "apply_chapter_edit":
                                logger.info(f"[LangGraph] 🚀 二次调用 apply_chapter_edit, chapter_id={tool_args.get('chapter_id')}")
                                # 🔧 2025-12-14: 统一使用 registry
                                try:
                                    result = await registry.call_tool("apply_chapter_edit", {
                                        "chapter_id": tool_args.get("chapter_id", ""),
                                        "content": tool_args.get("content", ""),
                                        "operation": tool_args.get("operation", "replace"),
                                        "position": None,
                                        "user_id": state.get("user_id"),
                                        "description": None
                                    })
                                    if isinstance(result, dict) and result.get("success"):
                                        second_tool_result = json.dumps(result.get("data", {}), ensure_ascii=False)
                                    else:
                                        second_tool_result = json.dumps(result, ensure_ascii=False)
                                except Exception as e:
                                    logger.warning(f"[StandardTool] 二次调用 apply_chapter_edit 失败，降级: {e}")
                                    second_tool_result = await apply_chapter_edit.ainvoke({
                                        "chapter_id": tool_args.get("chapter_id", ""),
                                        "content": tool_args.get("content", ""),
                                        "operation": tool_args.get("operation", "replace"),
                                        "position": None,  # 🔧 补充
                                        "user_id": state.get("user_id"),  # 🔧 补充 user_id
                                        "description": None  # 🔧 补充
                                    })
                            else:
                                logger.warning(f"[LangGraph] 未知的二次工具调用: {tool_name}")

                            if second_tool_result:
                                logger.info(f"[LangGraph] ✅ 二次工具调用成功，返回结果长度: {len(second_tool_result)} 字符")

                                # 编辑器工具返回的是 HITL 审批请求
                                # 创建工具消息并添加到消息历史,让流程继续处理
                                from langchain_core.messages import AIMessage
                                ai_msg = AIMessage(content=f"我需要使用 {tool_name} 工具来帮助你。")
                                tool_msg = ToolMessage(content=second_tool_result, tool_call_id="manual_call_2")

                                # 更新state,添加第二次工具调用的消息
                                updated_state = state.copy()
                                updated_state["messages"] = state["messages"] + [ai_msg, tool_msg]
                                updated_state["agent_steps"] = state.get("agent_steps", []) + [{
                                    "step": f"{agent_type}_second_tool_call",
                                    "result": f"二次调用编辑器工具: {tool_name}",
                                    "tool_result_length": len(second_tool_result)
                                }]
                                # 🔒 标记已经执行过二次工具调用
                                updated_state["_second_tool_called"] = True

                                # 🔄 继续递归处理,让它生成最终响应
                                # 这次传入的messages最后一条是ToolMessage,会进入"处理工具结果"分支
                                logger.info(f"[LangGraph] 🔄 继续处理第二次工具结果 (depth={recursion_depth + 1})")
                                return await self._handle_with_httpai(
                                    updated_state,
                                    agent_type,
                                    system_prompt,
                                    recursion_depth=recursion_depth + 1
                                )
                        except Exception as e:
                            logger.error(f"[LangGraph] 二次工具调用失败: {e}", exc_info=True)
                else:
                    logger.info(f"[LangGraph] ⚠️ 未能从工具结果中提取chapter_id，继续正常流程")

            # 判断用户意图：是想「查看/读取」内容，还是想「创作/续写」内容
            read_keywords = ["读", "看", "查看", "显示", "展示", "告诉我", "第几章", "内容是什么"]
            write_keywords = ["写", "续写", "创作", "生成", "继续", "扩写", "补充"]

            is_read_request = any(keyword in user_message for keyword in read_keywords)
            is_write_request = any(keyword in user_message for keyword in write_keywords)

            # 构建任务指令（不包含 system_prompt，因为会单独添加）
            if agent_type == "writing":
                # 如果用户明确想「读取/查看」内容
                if is_read_request and not is_write_request:
                    task_instruction = f"""用户请求：{user_message}

工具返回的真实数据（JSON格式）：
{tool_result}

【重要指令】
上面是从数据库读取的真实数据，包含作品信息、章节内容、分析片段等。

请按照以下格式清晰地展示给用户：

**作品信息**
- 标题：[从 work_info.title 获取]
- 描述：[从 work_info.description 获取]
- 章节总数：[从 work_info.total_chapters 获取]

**章节信息**
- 章节标题：[从 current_chapter.title 获取]
- 章节序号：第 [从 current_chapter.order 获取] 章
- 字数：[从 current_chapter.word_count 获取]

**章节内容**
[从 current_chapter.content_preview 或完整 content 获取，保持原文格式]

注意：
1. 所有信息必须来自上述JSON数据，不要编造
2. 如果某个字段为空或不存在，标注为"暂无"
3. 用清晰的markdown格式展示
4. 不要添加任何评论、分析或续写"""

                # 如果用户明确想「创作/续写」内容
                else:
                    task_instruction = f"""用户请求：{user_message}

工具提供的真实上下文数据（JSON格式）：
{tool_result}

【重要指令】
1. 上面的工具返回数据是从数据库读取的真实内容，包含：
   - 作品的真实标题、描述、类型
   - 章节的真实标题、序号、已有内容
   - 从向量数据库检索到的世界观、角色设定等分析片段

2. 你必须仔细阅读上述JSON数据，特别是：
   - current_chapter.content_preview（当前章节已有内容）
   - related_analysis（相关世界观和角色设定）
   - work_info（作品整体信息）

3. 创作续写时，必须：
   - 基于 current_chapter.content_preview 中的真实内容进行续写
   - 保持与已有内容的风格、人物、情节连贯
   - 参考 related_analysis 中的世界观和角色设定
   - 不要编造与上述数据矛盾的信息

4. 如果上述数据中某些字段为空或缺失，说明数据库中确实没有相关内容，此时可以合理发挥创作。

请直接开始续写内容（至少500字），不要重复说明你看到了什么数据。"""

            elif agent_type == "stuck":
                task_instruction = f"""用户遇到的问题：{user_message}

当前创作背景：
{tool_result}

请基于背景信息，给用户3-5个具体的创作方向建议，每个建议包含：
1. 方向概述
2. 可以这样写的理由
3. 示例开头（50字左右）"""

            elif agent_type == "planning":
                task_instruction = f"""用户需求：{user_message}

当前信息：
{tool_result}

请基于现有信息，提供详细的规划方案。"""

            else:  # analysis 或其他
                # 如果用户明确想「读取/查看」内容
                if is_read_request and not is_write_request:
                    task_instruction = f"""用户请求：{user_message}

工具返回的数据：
{tool_result}

请注意：用户想要「查看/读取」内容！
请直接整理并呈现工具返回的数据内容，用清晰易读的格式展示给用户。"""
                else:
                    task_instruction = f"""用户请求：{user_message}

分析材料：
{tool_result}

请基于材料，生成详细的分析报告。"""

            # ✅ 记忆修复：构建包含历史消息的完整对话上下文
            response_messages = []

            # 1. 添加系统提示
            response_messages.append({
                "role": "system",
                "content": system_prompt
            })

            # 2. 添加历史对话消息（排除工具调用相关消息）
            # ✅ 优化：限制历史消息数量，避免 token 无限增长
            MAX_HISTORY_MESSAGES = 20  # 最多保留最近10轮对话（20条消息）

            history_messages = []
            for msg in messages[:-1]:  # 排除最后一条 ToolMessage
                if isinstance(msg, HumanMessage):
                    history_messages.append({"role": "user", "content": msg.content})
                elif isinstance(msg, AIMessage):
                    # 跳过工具调用相关的AI消息
                    if not msg.content.startswith("我需要使用"):
                        history_messages.append({"role": "assistant", "content": msg.content})
                # SystemMessage 和 ToolMessage 不添加到历史

            # ✅ 如果历史消息过多，只保留最近的 N 条
            if len(history_messages) > MAX_HISTORY_MESSAGES:
                history_messages = history_messages[-MAX_HISTORY_MESSAGES:]
                logger.info(f"[LangGraph] ⚠️ 工具响应阶段：历史消息过多，截断为最近 {MAX_HISTORY_MESSAGES} 条")

            # 添加到响应消息列表
            response_messages.extend(history_messages)

            # 3. 添加当前的任务指令（包含工具结果）
            response_messages.append({
                "role": "user",
                "content": task_instruction
            })

            logger.info(f"[LangGraph] 🧠 工具响应阶段：传递 {len(response_messages)} 条消息给AI（包含历史对话）")

            # 根据 agent_type 和用户意图智能选择 task_type
            if agent_type == "writing":
                # 写作场景：根据用户意图区分
                if is_read_request and not is_write_request:
                    selected_task_type = TaskType.SUMMARIZATION  # 展示数据
                else:
                    selected_task_type = TaskType.CONTENT_CREATION  # 续写创作
            elif agent_type == "stuck":
                selected_task_type = TaskType.SIMPLE_QA  # 提供建议
            elif agent_type == "planning":
                selected_task_type = TaskType.STORY_PLANNING  # 规划方案
            elif agent_type == "analysis":
                # 分析场景：根据复杂度区分
                if is_read_request and not is_write_request:
                    selected_task_type = TaskType.SUMMARIZATION  # 展示数据
                else:
                    selected_task_type = TaskType.DEEP_ANALYSIS  # 深度分析
            else:
                # 其他场景：默认摘要
                selected_task_type = TaskType.SUMMARIZATION

            logger.info(f"[LangGraph] {agent_type} 最终响应使用模型: task_type={selected_task_type.value}")

            # ✅ 使用 _generate_text 传递完整历史
            result = await self._generate_text(
                messages=response_messages,  # ✅ 传递包含历史的消息列表
                max_tokens=1500,
                temperature=0.7,
                task_type=selected_task_type  # 智能选择的task_type
            )
            final_text = result.get("text", "")

            response = AIMessage(content=final_text)
            # ✅ 只返回新消息，避免 operator.add 重复添加
            return {
                "messages": [response],
                "final_response": final_text,
                "agent_steps": [{
                    "step": f"{agent_type}_final_response",
                    "result": "基于工具结果生成最终响应 (HTTPAIService)"
                }]
            }

        # 第一次进入：使用 HTTPAIService 决定是否需要工具
        last_user_message = messages[-1].content

        # ✅ P0修复：改进AI决策Prompt，明确当前上下文
        current_work_id = state.get("work_id")
        current_chapter_id = state.get("chapter_id")

        # ✅ P2修复：显示实际的ID值（安全截断）
        def _format_id(value: Optional[str], max_len: int = 20) -> str:
            """格式化ID值，安全截断过长ID"""
            if not value:
                return "未设置"
            if len(value) <= max_len:
                return f"{value}"
            return f"{value[:max_len]}..."

        context_info = f"""
当前上下文：
- 作品ID (work_id): {_format_id(current_work_id)}
- 章节ID (chapter_id): {_format_id(current_chapter_id)}
"""

        # Version memory: add previous versions to context if available
        last_versions = state.get("context", {}).get("last_rewrite_versions", {})
        if last_versions:
            version_info = "\n[Previous rewrite versions (use when user says 'based on version X')]"
            if last_versions.get("version_a"):
                version_info += f"\n- Version A: {last_versions['version_a'][:100]}..."
            if last_versions.get("version_b"):
                version_info += f"\n- Version B: {last_versions['version_b'][:100]}..."
            if last_versions.get("version_c"):
                version_info += f"\n- Version C: {last_versions['version_c'][:100]}..."
            context_info += version_info
            logger.info(f"[LangGraph] Added version memory to context")

        # ✅ Phase 2.6: 使用缓存的静态 Prompt（节省构建时间和 Token）
        static_prompt = await get_tool_decision_static_prompt()

        # 🆕 Phase 2.7: 动态添加章节上下文提示（如果存在 chapter_id）
        chapter_context_hint = ""
        if state.get("chapter_id"):
            work_id = state.get("work_id", "未知")
            chapter_id = state.get("chapter_id")
            chapter_context_hint = f"""

⚠️ 【章节上下文提示】：
- 当前用户在章节聊天面板中（work_id={work_id}, chapter_id={chapter_id}）
- 如果用户要求修改/润色/分析本章内容，**必须先调用 read_chapter_tool(work_id="{work_id}", chapter_id="{chapter_id}")** 读取章节原文
- 正确流程：read_chapter_tool → 理解上下文 → smart_rewrite 或其他工具
"""

        # ✅ 记忆修复：构建包含历史消息的完整对话上下文
        chat_messages = []

        # 1. 添加系统提示作为第一条消息
        chat_messages.append({
            "role": "system",
            "content": f"""{system_prompt}

{context_info}

{static_prompt}{chapter_context_hint}"""
        })

        # 2. 添加历史对话消息（保留上下文）
        # ✅ 优化：限制历史消息数量，避免 token 无限增长
        MAX_HISTORY_MESSAGES = 10  # 最多保留最近5轮对话（10条消息）

        history_messages = []
        for msg in messages:
            if isinstance(msg, HumanMessage):
                history_messages.append({"role": "user", "content": msg.content})
            elif isinstance(msg, AIMessage):
                # 跳过工具调用相关的AI消息（避免混淆）
                if not msg.content.startswith("我需要使用"):
                    history_messages.append({"role": "assistant", "content": msg.content})
            # SystemMessage 和 ToolMessage 不添加到历史（已在系统提示中或不需要）

        # ✅ 如果历史消息过多，只保留最近的 N 条
        if len(history_messages) > MAX_HISTORY_MESSAGES:
            history_messages = history_messages[-MAX_HISTORY_MESSAGES:]
            logger.info(f"[LangGraph] ⚠️ 历史消息过多，截断为最近 {MAX_HISTORY_MESSAGES} 条")

        # 添加到聊天消息列表
        chat_messages.extend(history_messages)

        logger.info(f"[LangGraph] 🧠 记忆修复：传递 {len(chat_messages)} 条消息给AI（包含历史对话）")

        # ✅ 使用 _generate_text 调用HTTPAIService
        result = await self._generate_text(
            messages=chat_messages,  # ✅ 传递完整消息历史
            max_tokens=200,  # ✅ Phase 2.5: 优化从500→200 (JSON响应通常<100 tokens)
            temperature=0.3,
            task_type=TaskType.SIMPLE_QA  # 工具决策任务
        )
        decision_text = result.get("text", "")

        # 解析决策
        import json
        import re

        logger.info(f"[LangGraph] AI 决策原文: {decision_text}")

        # 方法 1: 尝试直接解析整个文本（如果 AI 只返回 JSON）
        decision = None
        try:
            decision = json.loads(decision_text.strip())
            logger.info(f"[LangGraph] 方法1成功: 直接解析整个文本")
        except:
            pass

        # 方法 2: 使用正则提取 JSON（支持嵌套，贪婪匹配）
        if not decision:
            # 匹配 { ... } 包括嵌套的 JSON
            json_matches = re.finditer(r'\{(?:[^{}]|(?:\{[^}]*\}))*\}', decision_text)
            for match in json_matches:
                try:
                    candidate = json.loads(match.group())
                    # 验证是否包含必需字段
                    if "need_tools" in candidate:
                        decision = candidate
                        logger.info(f"[LangGraph] 方法2成功: 正则提取 JSON")
                        break
                except:
                    continue

        # 方法 3: 如果都失败，使用AI的原始回答
        if not decision:
            logger.warning(f"[LangGraph] 无法解析JSON决策，使用原始回答，原文前200字符: {decision_text[:200]}")
            decision = {
                "need_tools": False,
                "direct_response": decision_text.strip()  # ✅ 使用AI的原始回答，而不是默认错误消息
            }

        logger.info(f"[LangGraph] 最终决策: {decision}")

        logger.info(f"[LangGraph] {agent_type} 决策 (HTTPAIService): {decision.get('need_tools', False)}")

        if decision.get("need_tools", False):
            # 需要工具：手动调用
            tool_name = decision.get("tool_name", "continue_writing_tool")
            tool_args = decision.get("tool_args", {})

            # 标准化参数格式
            tool_args = self._normalize_tool_params(tool_name, tool_args)

            # 调用工具（使用 .ainvoke() 方法，因为 @tool 装饰器返回的是 StructuredTool 对象）
            tool_result = ""
            if tool_name == "continue_writing_tool":
                # 🔧 2025-12-14: 迁移到 StandardTool 系统
                try:
                    result = await registry.call_tool("continue_writing", {
                        "context": tool_args.get("context", last_user_message),
                        "requirements": tool_args.get("requirements", ""),
                        "target_length": tool_args.get("target_length", 500),
                        "style": tool_args.get("style", "")
                    })

                    # StandardTool 返回 dict 格式，提取 generated_text
                    if isinstance(result, dict) and result.get("success"):
                        tool_result = result.get("data", {}).get("generated_text", "")
                        logger.info(f"[StandardTool] continue_writing 执行成功，字数: {len(tool_result)}")
                    else:
                        error_msg = result.get("message", "执行失败") if isinstance(result, dict) else "未知错误"
                        tool_result = json.dumps({"error": "tool_failed", "message": error_msg}, ensure_ascii=False)
                        logger.error(f"[StandardTool] continue_writing 执行失败: {error_msg}")

                except Exception as e:
                    # 降级到 @tool 版本（兜底）
                    logger.warning(f"[StandardTool] 调用失败，降级到 @tool 版本: {e}")
                    tool_result = await continue_writing_tool.ainvoke({
                        "context": tool_args.get("context", last_user_message),
                        "requirements": tool_args.get("requirements", "")
                    })
            elif tool_name == "analyze_text_tool":
                # 🔧 2025-12-14: 迁移到 StandardTool 系统
                try:
                    result = await registry.call_tool("analyze_text", {
                        "text": tool_args.get("text", last_user_message),
                        "focus": tool_args.get("focus", "all")
                    })

                    # StandardTool 返回 dict 格式，提取 analysis_report
                    if isinstance(result, dict) and result.get("success"):
                        tool_result = result.get("data", {}).get("analysis_report", "")
                        logger.info(f"[StandardTool] analyze_text 执行成功，结果长度: {len(tool_result)}")
                    else:
                        error_msg = result.get("message", "执行失败") if isinstance(result, dict) else "未知错误"
                        tool_result = json.dumps({"error": "tool_failed", "message": error_msg}, ensure_ascii=False)
                        logger.error(f"[StandardTool] analyze_text 执行失败: {error_msg}")

                except Exception as e:
                    # 降级到 @tool 版本（兜底）
                    logger.warning(f"[StandardTool] 调用失败，降级到 @tool 版本: {e}")
                    tool_result = await analyze_text_tool.ainvoke({
                        "text": tool_args.get("text", last_user_message),
                        "focus": tool_args.get("focus", "all")
                    })
            elif tool_name == "get_context_tool":
                # ✅ P0修复：添加参数完整性检查
                work_id_value = state.get("work_id")
                if not work_id_value:
                    logger.warning(f"[LangGraph] ⚠️ get_context_tool 缺少必需参数 work_id")
                    tool_result = json.dumps({
                        "error": "missing_work_id",
                        "message": "需要提供作品ID才能获取上下文",
                        "user_prompt": "请先告诉我您要操作哪部作品？"
                    }, ensure_ascii=False)
                else:
                    # 🔧 2025-12-14: 统一使用 registry 调用 StandardTool
                    logger.info(f"[LangGraph] 🚀 准备调用 get_context_tool, work_id={work_id_value}, chapter_id={state.get('chapter_id')}")
                    try:
                        result = await registry.call_tool("get_context", {
                            "work_id": work_id_value,
                            "chapter_id": state.get("chapter_id", "")
                        })

                        # StandardTool 返回 dict 格式，提取 context
                        if isinstance(result, dict) and result.get("success"):
                            tool_result = result.get("data", {}).get("context", "")
                            logger.info(f"[StandardTool] get_context 执行成功，长度: {len(tool_result)} 字符")
                        else:
                            error_msg = result.get("message", "执行失败") if isinstance(result, dict) else "未知错误"
                            tool_result = json.dumps({"error": "tool_failed", "message": error_msg}, ensure_ascii=False)
                            logger.error(f"[StandardTool] get_context 执行失败: {error_msg}")

                    except Exception as e:
                        # 降级到 @tool 版本
                        logger.warning(f"[StandardTool] get_context 调用失败，降级到 @tool: {e}")
                        tool_result = await get_context_tool.ainvoke({
                            "work_id": work_id_value,
                            "chapter_id": state.get("chapter_id", "")
                        })

                    logger.info(f"[LangGraph] ✅ get_context_tool 返回结果长度: {len(tool_result)} 字符")
                    logger.info(f"[LangGraph] ✅ get_context_tool 返回内容预览: {tool_result[:200]}")
            elif tool_name == "read_chapter_tool":
                # ✅ P0修复：添加参数完整性检查
                work_id_value = state.get("work_id")
                if not work_id_value:
                    logger.warning(f"[LangGraph] ⚠️ read_chapter_tool 缺少必需参数 work_id")
                    tool_result = json.dumps({
                        "error": "missing_work_id",
                        "message": "需要提供作品ID才能读取章节",
                        "user_prompt": "请先告诉我您要读取哪部作品的章节？"
                    }, ensure_ascii=False)
                else:
                    # 🔧 2025-12-14: 统一使用 registry 调用 StandardTool
                    try:
                        result = await registry.call_tool("read_chapter", {
                            "work_id": work_id_value,
                            "chapter_id": tool_args.get("chapter_id") or state.get("chapter_id") or ""
                        })

                        # StandardTool 返回 dict 格式，提取 chapter_info
                        if isinstance(result, dict) and result.get("success"):
                            tool_result = result.get("data", {}).get("chapter_info", "")
                            logger.info(f"[StandardTool] read_chapter 执行成功")
                        else:
                            error_msg = result.get("message", "执行失败") if isinstance(result, dict) else "未知错误"
                            tool_result = json.dumps({"error": "tool_failed", "message": error_msg}, ensure_ascii=False)
                            logger.error(f"[StandardTool] read_chapter 执行失败: {error_msg}")

                    except Exception as e:
                        # 降级到 @tool 版本
                        logger.warning(f"[StandardTool] read_chapter 调用失败，降级到 @tool: {e}")
                        tool_result = await read_chapter_tool.ainvoke({
                            "work_id": work_id_value,
                            "chapter_id": tool_args.get("chapter_id") or state.get("chapter_id") or ""
                        })
            elif tool_name == "get_chapter_by_order_tool":
                # ✅ P0修复：添加参数完整性检查
                work_id_value = state.get("work_id")
                if not work_id_value:
                    logger.warning(f"[LangGraph] ⚠️ get_chapter_by_order_tool 缺少必需参数 work_id")
                    tool_result = json.dumps({
                        "error": "missing_work_id",
                        "message": "需要提供作品ID才能查询章节",
                        "user_prompt": "请先告诉我您要查看哪部作品的章节？您可以说：\n- 「我想看《作品名》的第X章」\n- 或者先创建一部新作品"
                    }, ensure_ascii=False)
                else:
                    # 🔧 2025-12-14: 统一使用 registry 调用 StandardTool
                    logger.info(f"[LangGraph] 🚀 准备调用 get_chapter_by_order_tool, work_id={work_id_value}, chapter_order={tool_args.get('chapter_order')}")
                    try:
                        result = await registry.call_tool("get_chapter_by_order", {
                            "work_id": work_id_value,
                            "chapter_order": tool_args.get("chapter_order", 1)
                        })

                        # StandardTool 返回 dict 格式，提取 chapter_info
                        if isinstance(result, dict) and result.get("success"):
                            tool_result = result.get("data", {}).get("chapter_info", "")
                            logger.info(f"[StandardTool] get_chapter_by_order 执行成功")
                        else:
                            error_msg = result.get("message", "执行失败") if isinstance(result, dict) else "未知错误"
                            tool_result = json.dumps({"error": "tool_failed", "message": error_msg}, ensure_ascii=False)
                            logger.error(f"[StandardTool] get_chapter_by_order 执行失败: {error_msg}")

                    except Exception as e:
                        # 降级到 @tool 版本
                        logger.warning(f"[StandardTool] get_chapter_by_order 调用失败，降级到 @tool: {e}")
                        tool_result = await get_chapter_by_order_tool.ainvoke({
                            "work_id": work_id_value,
                            "chapter_order": tool_args.get("chapter_order", 1)
                        })

                    logger.info(f"[LangGraph] ✅ get_chapter_by_order_tool 返回结果长度: {len(tool_result)} 字符")
            elif tool_name == "search_analysis_fragments_tool":
                # ✅ P0修复：添加参数完整性检查
                work_id_value = state.get("work_id")
                if not work_id_value:
                    logger.warning(f"[LangGraph] ⚠️ search_analysis_fragments_tool 缺少必需参数 work_id")
                    tool_result = json.dumps({
                        "error": "missing_work_id",
                        "message": "需要提供作品ID才能搜索分析片段",
                        "user_prompt": "请先告诉我您要搜索哪部作品的分析片段？"
                    }, ensure_ascii=False)
                else:
                    # 🔧 2025-12-14: 统一使用 registry 调用 StandardTool
                    try:
                        result = await registry.call_tool("search_analysis_fragments", {
                            "work_id": work_id_value,
                            "query": tool_args.get("query", last_user_message),
                            "top_k": tool_args.get("top_k", 5),
                            "chapter_id": state.get("chapter_id", ""),  # ✅ P0修复：传递 chapter_id 支持时序限制
                            "include_current": tool_args.get("include_current", True),
                            "look_ahead": tool_args.get("look_ahead", 2)
                        })

                        # StandardTool 返回 dict 格式，提取 fragments
                        if isinstance(result, dict) and result.get("success"):
                            tool_result = result.get("data", {}).get("fragments", "")
                            logger.info(f"[StandardTool] search_analysis_fragments 执行成功")
                        else:
                            error_msg = result.get("message", "执行失败") if isinstance(result, dict) else "未知错误"
                            tool_result = json.dumps({"error": "tool_failed", "message": error_msg}, ensure_ascii=False)
                            logger.error(f"[StandardTool] search_analysis_fragments 执行失败: {error_msg}")

                    except Exception as e:
                        # 降级到 @tool 版本
                        logger.warning(f"[StandardTool] search_analysis_fragments 调用失败，降级到 @tool: {e}")
                        tool_result = await search_analysis_fragments_tool.ainvoke({
                            "work_id": work_id_value,
                            "query": tool_args.get("query", last_user_message),
                            "top_k": tool_args.get("top_k", 5),
                            "chapter_id": state.get("chapter_id", ""),  # ✅ P0修复：传递 chapter_id 支持时序限制
                            "include_current": tool_args.get("include_current", True),
                            "look_ahead": tool_args.get("look_ahead", 2),
                        })
            # ✅ 编辑器工具：smart_rewrite（改写章节）
            elif tool_name == "smart_rewrite":
                # ✅ P0-6修复：使用正确的参数名，包含 user_requirement 和 base_version
                text_to_rewrite = tool_args.get("text_to_rewrite") or tool_args.get("content", "")
                chapter_content = tool_args.get("chapter_content", "")
                user_requirement = tool_args.get("user_requirement", "")
                base_version = tool_args.get("base_version", "")

                # 🆕 InlineAI 支持：优先使用 context 中的 selected_text
                context = state.get("context", {})
                selected_text = context.get("selected_text", "")
                selection_position = context.get("selection_position", None)

                # 🔑 关键修复：如果有 selected_text，强制使用它（覆盖 LLM 传入的 text_to_rewrite）
                # 这是因为用户在编辑器中选中的文本才是他们真正想要修改的内容
                if selected_text:
                    logger.info(f"[LangGraph] 📝 强制使用 InlineAI selected_text 作为 text_to_rewrite ({len(selected_text)} 字符)")
                    logger.info(f"[LangGraph] 📝 原 text_to_rewrite: {text_to_rewrite[:50] if text_to_rewrite else 'None'}...")
                    text_to_rewrite = selected_text

                # ✅ 智能版本引用：语义匹配用户的版本表达
                last_versions = state.get("context", {}).get("last_rewrite_versions", {})
                if base_version and last_versions:
                    resolved_version = self._resolve_version_reference(base_version, last_versions)
                    if resolved_version:
                        logger.info(f"[LangGraph] 🔄 智能版本解析: '{base_version}' → 完整内容({len(resolved_version)}字)")
                        base_version = resolved_version

                logger.info(f"[LangGraph] 🚀 准备调用 smart_rewrite, chapter_id={tool_args.get('chapter_id')}, text_to_rewrite长度={len(text_to_rewrite)}, user_requirement={user_requirement[:50] if user_requirement else 'None'}")

                # 🔧 2025-12-14: 统一使用 registry 调用 StandardTool
                try:
                    result = await registry.call_tool("smart_rewrite", {
                        "chapter_id": tool_args.get("chapter_id", ""),
                        "text_to_rewrite": text_to_rewrite,
                        "chapter_content": chapter_content,
                        "user_requirement": user_requirement,
                        "base_version": base_version,
                        "user_id": state.get("user_id")
                    })

                    # StandardTool 返回 dict 格式，提取 data
                    if isinstance(result, dict) and result.get("success"):
                        tool_result = json.dumps(result.get("data", {}), ensure_ascii=False)
                        logger.info(f"[StandardTool] smart_rewrite 执行成功")
                    else:
                        error_msg = result.get("message", "执行失败") if isinstance(result, dict) else "未知错误"
                        tool_result = json.dumps({"error": "tool_failed", "message": error_msg}, ensure_ascii=False)
                        logger.error(f"[StandardTool] smart_rewrite 执行失败: {error_msg}")

                except Exception as e:
                    # 降级到 @tool 版本
                    logger.warning(f"[StandardTool] smart_rewrite 调用失败，降级到 @tool: {e}")
                    tool_result = await smart_rewrite.ainvoke({
                        "chapter_id": tool_args.get("chapter_id", ""),
                        "text_to_rewrite": text_to_rewrite,
                        "chapter_content": chapter_content,
                        "user_requirement": user_requirement,
                        "base_version": base_version,
                        "user_id": state.get("user_id")  # 🔧 补充 user_id
                    })

                logger.info(f"[LangGraph] ✅ smart_rewrite 返回结果长度: {len(str(tool_result))} 字符")

                # ✅ 版本记忆：保存生成的版本到 context，供后续"在第X版基础上改"使用
                try:
                    if isinstance(tool_result, str):
                        result_obj = json.loads(tool_result)
                    else:
                        result_obj = tool_result

                    if result_obj.get("success") and result_obj.get("versions"):
                        versions = result_obj["versions"]
                        state["context"] = state.get("context", {})
                        state["context"]["last_rewrite_versions"] = {
                            "version_a": versions[0].get("content", "") if len(versions) > 0 else "",
                            "version_b": versions[1].get("content", "") if len(versions) > 1 else "",
                            "version_c": versions[2].get("content", "") if len(versions) > 2 else ""
                        }
                        logger.info(f"[LangGraph] 💾 已保存 {len(versions)} 个改写版本到 context")

                        # 🆕 InlineAI: 添加 editor_action 字段
                        if selected_text and selection_position:
                            result_obj["editor_action"] = {
                                "type": "modify",
                                "original_text": text_to_rewrite,
                                "position": selection_position,
                                "requires_confirmation": True
                            }
                            # 更新 tool_result
                            tool_result = json.dumps(result_obj, ensure_ascii=False) if isinstance(tool_result, str) else result_obj
                            logger.info(f"[LangGraph] 📝 添加 editor_action (modify) 到 smart_rewrite 结果")
                except Exception as e:
                    logger.warning(f"[LangGraph] 保存版本记忆失败: {e}")
            # ✅ 编辑器工具：smart_continue（续写章节）
            elif tool_name == "smart_continue":
                logger.info(f"[LangGraph] 🚀 准备调用 smart_continue, chapter_id={tool_args.get('chapter_id')}")

                # 🆕 InlineAI 支持：获取 selection_position
                context = state.get("context", {})
                selected_text = context.get("selected_text", "")
                selection_position = context.get("selection_position", None)

                # 🔧 2025-12-14: 统一使用 registry 调用 StandardTool
                try:
                    result = await registry.call_tool("smart_continue", {
                        "chapter_id": tool_args.get("chapter_id", ""),
                        "content": tool_args.get("context", ""),
                        "user_id": state.get("user_id")
                    })

                    # StandardTool 返回 dict 格式，提取 data
                    if isinstance(result, dict) and result.get("success"):
                        tool_result = json.dumps(result.get("data", {}), ensure_ascii=False)
                        logger.info(f"[StandardTool] smart_continue 执行成功")
                    else:
                        error_msg = result.get("message", "执行失败") if isinstance(result, dict) else "未知错误"
                        tool_result = json.dumps({"error": "tool_failed", "message": error_msg}, ensure_ascii=False)
                        logger.error(f"[StandardTool] smart_continue 执行失败: {error_msg}")

                except Exception as e:
                    # 降级到 @tool 版本
                    logger.warning(f"[StandardTool] smart_continue 调用失败，降级到 @tool: {e}")
                    tool_result = await smart_continue.ainvoke({
                        "chapter_id": tool_args.get("chapter_id", ""),
                        "content": tool_args.get("context", ""),  # 🔧 参数名修正：@tool 版本期望 "content"
                        "user_id": state.get("user_id")
                    })

                logger.info(f"[LangGraph] ✅ smart_continue 返回结果长度: {len(tool_result)} 字符")

                # 🆕 InlineAI: 添加 editor_action 字段 (type=continue)
                if selected_text and selection_position:
                    try:
                        if isinstance(tool_result, str):
                            result_obj = json.loads(tool_result)
                        else:
                            result_obj = tool_result

                        result_obj["editor_action"] = {
                            "type": "continue",
                            "position": selection_position,
                            "requires_confirmation": True
                        }
                        tool_result = json.dumps(result_obj, ensure_ascii=False) if isinstance(tool_result, str) else result_obj
                        logger.info(f"[LangGraph] 📝 添加 editor_action (continue) 到 smart_continue 结果")
                    except Exception as e:
                        logger.warning(f"[LangGraph] 添加 editor_action 失败: {e}")
            # ✅ 编辑器工具：smart_insert（插入内容）
            elif tool_name == "smart_insert":
                logger.info(f"[LangGraph] 🚀 准备调用 smart_insert, chapter_id={tool_args.get('chapter_id')}")

                # 🔧 2025-12-14: 统一使用 registry 调用 StandardTool
                try:
                    result = await registry.call_tool("smart_insert", {
                        "chapter_id": tool_args.get("chapter_id", ""),
                        "content": tool_args.get("content", ""),
                        "user_intent": tool_args.get("position", "end"),  # position 映射到 user_intent
                        "chapter_content": None,
                        "context": None,
                        "user_id": state.get("user_id")
                    })

                    # StandardTool 返回 dict 格式，提取 data
                    if isinstance(result, dict) and result.get("success"):
                        tool_result = json.dumps(result.get("data", {}), ensure_ascii=False)
                        logger.info(f"[StandardTool] smart_insert 执行成功")
                    else:
                        error_msg = result.get("message", "执行失败") if isinstance(result, dict) else "未知错误"
                        tool_result = json.dumps({"error": "tool_failed", "message": error_msg}, ensure_ascii=False)
                        logger.error(f"[StandardTool] smart_insert 执行失败: {error_msg}")

                except Exception as e:
                    # 降级到 @tool 版本
                    logger.warning(f"[StandardTool] smart_insert 调用失败，降级到 @tool: {e}")
                    tool_result = await smart_insert.ainvoke({
                        "chapter_id": tool_args.get("chapter_id", ""),
                        "content": tool_args.get("content", ""),
                        "user_intent": tool_args.get("position", "end"),  # 🔧 参数名映射
                        "chapter_content": None,  # 🔧 补充
                        "context": None,  # 🔧 补充
                        "user_id": state.get("user_id")  # 🔧 补充 user_id
                    })

                logger.info(f"[LangGraph] ✅ smart_insert 返回结果长度: {len(tool_result)} 字符")

            # ✅ 编辑器工具：apply_chapter_edit（应用章节编辑）
            elif tool_name == "apply_chapter_edit":
                logger.info(f"[LangGraph] 🚀 准备调用 apply_chapter_edit, chapter_id={tool_args.get('chapter_id')}")

                # 🔧 2025-12-14: 统一使用 registry 调用 StandardTool
                try:
                    result = await registry.call_tool("apply_chapter_edit", {
                        "chapter_id": tool_args.get("chapter_id", ""),
                        "content": tool_args.get("content", ""),
                        "operation": tool_args.get("operation", "replace"),
                        "position": None,
                        "user_id": state.get("user_id"),
                        "description": None
                    })

                    # StandardTool 返回 dict 格式，提取 data
                    if isinstance(result, dict) and result.get("success"):
                        tool_result = json.dumps(result.get("data", {}), ensure_ascii=False)
                        logger.info(f"[StandardTool] apply_chapter_edit 执行成功")
                    else:
                        error_msg = result.get("message", "执行失败") if isinstance(result, dict) else "未知错误"
                        tool_result = json.dumps({"error": "tool_failed", "message": error_msg}, ensure_ascii=False)
                        logger.error(f"[StandardTool] apply_chapter_edit 执行失败: {error_msg}")

                except Exception as e:
                    # 降级到 @tool 版本
                    logger.warning(f"[StandardTool] apply_chapter_edit 调用失败，降级到 @tool: {e}")
                    tool_result = await apply_chapter_edit.ainvoke({
                        "chapter_id": tool_args.get("chapter_id", ""),
                        "content": tool_args.get("content", ""),
                        "operation": tool_args.get("operation", "replace"),
                        "position": None,  # 🔧 补充
                        "user_id": state.get("user_id"),  # 🔧 补充 user_id
                        "description": None  # 🔧 补充
                    })

                logger.info(f"[LangGraph] ✅ apply_chapter_edit 返回结果长度: {len(tool_result)} 字符")
            else:
                # 🔧 2025-12-14: 使用统一接口调用未明确处理的工具
                logger.info(f"[LangGraph] 使用统一接口调用工具: {tool_name}")
                try:
                    tool_result = await self._call_tool_via_registry(
                        tool_name=tool_name,
                        tool_args=tool_args,
                        state=state
                    )
                    logger.info(f"[LangGraph] ✅ 统一接口调用成功: {tool_name}")
                except Exception as e:
                    # 统一接口调用失败
                    logger.error(f"[LangGraph] 统一接口调用失败: {tool_name}, 错误: {e}")
                    tool_result = json.dumps({
                        "error": "tool_call_failed",
                        "message": f"工具调用失败: {str(e)}",
                        "user_prompt": "抱歉，我在处理您的请求时遇到了问题。能否换个方式描述？"
                    }, ensure_ascii=False)

            # ✅ 创建新消息（不直接修改 state，避免重复）
            ai_decision = AIMessage(content=f"我需要使用 {tool_name} 工具来帮助你。")
            tool_message = ToolMessage(content=tool_result, tool_call_id="manual_call")

            new_step = {
                "step": f"{agent_type}_tool_call",
                "result": f"调用工具 (HTTPAIService): {tool_name}",
                "tool_result_length": len(tool_result)
            }

            # ✅ 创建更新后的 state（不修改原 state）
            updated_state = state.copy()
            updated_state["messages"] = state["messages"] + [ai_decision, tool_message]
            updated_state["agent_steps"] = state["agent_steps"] + [new_step]

            # ✅ P0修复：检查工具是否返回错误，如果是错误则直接返回友好提示
            try:
                tool_result_obj = json.loads(tool_result)
                error_type = tool_result_obj.get("error")
                if error_type in ["missing_work_id", "unknown_tool"]:
                    logger.info(f"[LangGraph] 🎯 检测到工具错误({error_type})，直接返回友好提示")
                    direct_response = tool_result_obj.get("user_prompt", "请先告诉我您要操作哪部作品？")
                    return {
                        "messages": [AIMessage(content=direct_response)],
                        "final_response": direct_response,
                        "agent_steps": [{
                            "step": f"{agent_type}_{error_type}",
                            "result": f"检测到错误: {error_type}"
                        }]
                    }
            except json.JSONDecodeError:
                # 正常的工具返回结果，继续处理
                pass
            except Exception as e:
                logger.warning(f"[LangGraph] 解析工具结果异常: {e}")
                # 继续处理，不返回错误

            # ✅ P1修复：智能清理累积的消息，防止上下文无限增长
            current_messages = updated_state["messages"]
            message_count = len(current_messages)

            # 智能清理策略：根据消息数量动态调整
            if message_count > 8:  # 降低阈值，更早触发清理
                # 分类消息
                system_messages = []
                user_messages = []
                ai_messages = []
                tool_messages = []

                for msg in current_messages:
                    if isinstance(msg, SystemMessage):
                        system_messages.append(msg)
                    elif isinstance(msg, HumanMessage):
                        user_messages.append(msg)
                    elif isinstance(msg, AIMessage):
                        ai_messages.append(msg)
                    elif isinstance(msg, ToolMessage):
                        tool_messages.append(msg)

                # 智能保留策略：
                # 1. 保留所有系统消息（通常只有1条）
                # 2. 保留最近的1条用户消息（当前请求）
                # 3. 保留最近的2对AI-Tool交互（最多4条）
                # 总共最多保留: 1(system) + 1(user) + 4(ai+tool) = 6条

                cleaned_messages = system_messages.copy()

                # 保留最近的用户消息
                if user_messages:
                    cleaned_messages.append(user_messages[-1])

                # ✅ P2修复：智能成对保留最近的AI-Tool交互
                # 确保AI消息和Tool消息成对保留，避免破坏对话连贯性
                recent_pairs = []
                ai_idx = len(ai_messages) - 1
                tool_idx = len(tool_messages) - 1

                # 从最新的开始，成对保留最多2对交互（4条消息）
                pairs_count = 0
                while pairs_count < 2 and ai_idx >= 0 and tool_idx >= 0:
                    # 成对添加（先AI后Tool）
                    recent_pairs.insert(0, tool_messages[tool_idx])
                    recent_pairs.insert(0, ai_messages[ai_idx])
                    ai_idx -= 1
                    tool_idx -= 1
                    pairs_count += 1

                # 按原始顺序重组
                for msg in current_messages:
                    if msg in recent_pairs and msg not in cleaned_messages:
                        cleaned_messages.append(msg)

                updated_state["messages"] = cleaned_messages
                logger.info(f"[LangGraph] 🧹 智能清理累积消息：{message_count}条 -> 保留{len(cleaned_messages)}条（压缩率{100 - len(cleaned_messages) * 100 // message_count}%）")
            else:
                logger.debug(f"[LangGraph] 消息数量{message_count}条，无需清理")

            # ✅ P0-3修复：递归处理工具结果，传递递归深度
            logger.debug(f"[LangGraph] 递归处理工具结果，当前深度={recursion_depth}")
            result = await self._handle_with_httpai(updated_state, agent_type, system_prompt, recursion_depth + 1)

            # ✅ 返回所有新增的消息（工具调用消息 + 递归结果）
            # 注意：updated_state是局部变量，不会影响外部state
            # 所以需要在返回时包含ai_decision和tool_message
            return {
                "messages": [ai_decision, tool_message] + result.get("messages", []),
                "final_response": result.get("final_response"),
                "agent_steps": [new_step] + result.get("agent_steps", [])
            }

        else:
            # 不需要工具：直接响应
            direct_response = decision.get("direct_response", "抱歉，我无法处理您的请求。")
            response = AIMessage(content=direct_response)
            # ✅ 只返回新消息，避免 operator.add 重复添加
            return {
                "messages": [response],
                "final_response": direct_response,
                "agent_steps": [{
                    "step": f"{agent_type}_direct_response",
                    "result": "直接响应用户 (HTTPAIService)"
                }]
            }

    async def _handle_writing(self, state: AgentState) -> AgentState:
        """
        处理写作场景 - 使用新架构

        新架构流程：
        1. 使用WritingAction.prepare()准备参数
        2. 调用_handle_agent_with_tools统一处理（触发监控）
        """
        from app.services.agent.actions import WritingAction

        logger.info("[LangGraph] 处理写作请求（新架构）")

        # 1. 使用Action准备参数（业务逻辑）
        writing_action = WritingAction()  # 新架构不需要ai_service
        prep_result = await writing_action.prepare(state)

        # 2. 检查准备结果
        if not prep_result.success:
            logger.error(f"[LangGraph] WritingAction.prepare()失败: {prep_result.error}")
            from langchain_core.messages import AIMessage
            error_msg = AIMessage(content=f"抱歉，写作请求处理失败: {prep_result.error}")
            return {
                "messages": [error_msg],
                "final_response": error_msg.content,
                "agent_steps": [{
                    "step": "writing_error",
                    "result": f"准备失败: {prep_result.error}"
                }]
            }

        # 3. 记录业务信息
        logger.info(
            f"[LangGraph] WritingAction准备完成: "
            f"phase={prep_result.metadata.get('phase')}, "
            f"chapter_num={prep_result.metadata.get('chapter_num')}"
        )

        # 4. 统一使用框架调用LLM（触发监控）
        return await self._handle_agent_with_tools(
            state,
            agent_type=prep_result.metadata.get("agent_type", "writing"),
            system_prompt=prep_result.system_prompt
        )

    async def _handle_planning(self, state: AgentState) -> AgentState:
        """
        处理规划场景 - 使用新架构

        新架构流程：
        1. 使用PlanningAction.prepare()准备参数
        2. 调用_handle_agent_with_tools统一处理（触发监控）
        """
        from app.services.agent.actions import PlanningAction

        logger.info("[LangGraph] 处理规划请求（新架构）")

        # 1. 使用Action准备参数（业务逻辑）
        planning_action = PlanningAction()  # 新架构不需要ai_service
        prep_result = await planning_action.prepare(state)

        # 2. 检查准备结果
        if not prep_result.success:
            logger.error(f"[LangGraph] PlanningAction.prepare()失败: {prep_result.error}")
            from langchain_core.messages import AIMessage
            error_msg = AIMessage(content=f"抱歉，规划请求处理失败: {prep_result.error}")
            return {
                "messages": [error_msg],
                "final_response": error_msg.content,
                "agent_steps": [{
                    "step": "planning_error",
                    "result": f"准备失败: {prep_result.error}"
                }]
            }

        # 3. 统一使用框架调用LLM（触发监控）
        return await self._handle_agent_with_tools(
            state,
            agent_type=prep_result.metadata.get("agent_type", "planning"),
            system_prompt=prep_result.system_prompt
        )

    async def _handle_analysis(self, state: AgentState) -> AgentState:
        """
        处理分析场景 - 使用新架构

        新架构流程：
        1. 使用AnalysisAction.prepare()准备参数
        2. 调用_handle_agent_with_tools统一处理（触发监控）
        """
        from app.services.agent.actions import AnalysisAction

        logger.info("[LangGraph] 处理分析请求（新架构）")

        # 1. 使用Action准备参数（业务逻辑）
        analysis_action = AnalysisAction()  # 新架构不需要ai_service
        prep_result = await analysis_action.prepare(state)

        # 2. 检查准备结果
        if not prep_result.success:
            logger.error(f"[LangGraph] AnalysisAction.prepare()失败: {prep_result.error}")
            from langchain_core.messages import AIMessage
            error_msg = AIMessage(content=f"抱歉，分析请求处理失败: {prep_result.error}")
            return {
                "messages": [error_msg],
                "final_response": error_msg.content,
                "agent_steps": [{
                    "step": "analysis_error",
                    "result": f"准备失败: {prep_result.error}"
                }]
            }

        # 3. 记录业务信息
        logger.info(
            f"[LangGraph] AnalysisAction准备完成: "
            f"work_id={prep_result.metadata.get('work_id')}, "
            f"chapter_id={prep_result.metadata.get('chapter_id')}"
        )

        # 4. 统一使用框架调用LLM（触发监控）
        return await self._handle_agent_with_tools(
            state,
            agent_type=prep_result.metadata.get("agent_type", "analysis"),
            system_prompt=prep_result.system_prompt
        )

    async def _handle_stuck(self, state: AgentState) -> AgentState:
        """
        处理卡文场景 - 使用新架构

        新架构流程：
        1. 使用StuckAction.prepare()准备参数
        2. 调用_handle_agent_with_tools统一处理（触发监控）
        """
        from app.services.agent.actions import StuckAction

        logger.info("[LangGraph] 处理卡文请求（新架构）")

        # 1. 使用Action准备参数（业务逻辑）
        stuck_action = StuckAction()  # 新架构不需要ai_service
        prep_result = await stuck_action.prepare(state)

        # 2. 检查准备结果
        if not prep_result.success:
            logger.error(f"[LangGraph] StuckAction.prepare()失败: {prep_result.error}")
            from langchain_core.messages import AIMessage
            error_msg = AIMessage(content=f"抱歉，卡文请求处理失败: {prep_result.error}")
            return {
                "messages": [error_msg],
                "final_response": error_msg.content,
                "agent_steps": [{
                    "step": "stuck_error",
                    "result": f"准备失败: {prep_result.error}"
                }]
            }

        # 3. 记录业务信息
        logger.info(
            f"[LangGraph] StuckAction准备完成: "
            f"work_id={prep_result.metadata.get('work_id')}, "
            f"chapter_id={prep_result.metadata.get('chapter_id')}"
        )

        # 4. 统一使用框架调用LLM（触发监控）
        return await self._handle_agent_with_tools(
            state,
            agent_type=prep_result.metadata.get("agent_type", "stuck"),
            system_prompt=prep_result.system_prompt
        )

    async def _handle_general(self, state: AgentState) -> AgentState:
        """
        处理一般对话 - 直接对话模式（不走工具决策）

        ✅ 修复：general意图直接生成响应，跳过工具决策流程
        这样"你好"等简单问候就不会被误判为需要续写工具

        流程：
        1. 使用GeneralChatAction.prepare()准备参数
        2. 直接调用_generate_text生成响应（不经过工具决策）
        """
        from app.services.agent.actions import GeneralChatAction
        from app.services.agent.model_selector import TaskType

        logger.info("[LangGraph] 处理一般对话（直接对话模式，跳过工具决策）")

        # 1. 使用Action准备参数（业务逻辑）
        general_action = GeneralChatAction()
        prep_result = await general_action.prepare(state)

        # 2. 检查准备结果
        if not prep_result.success:
            logger.error(f"[LangGraph] GeneralChatAction.prepare()失败: {prep_result.error}")
            error_msg = AIMessage(content=f"抱歉，无法处理您的请求: {prep_result.error}")
            return {
                "messages": [error_msg],
                "final_response": error_msg.content,
                "agent_steps": [{
                    "step": "general_chat_error",
                    "result": f"准备失败: {prep_result.error}"
                }]
            }

        # 3. ✅ 直接生成响应，不走工具决策流程
        messages = state["messages"]
        user_message = messages[-1].content if messages else ""

        # 构建对话消息（包含历史）
        chat_messages = [{
            "role": "system",
            "content": prep_result.system_prompt
        }]

        # 添加历史消息（最多保留10条）
        history_count = 0
        for msg in messages[:-1]:  # 排除当前消息
            if isinstance(msg, HumanMessage):
                chat_messages.append({"role": "user", "content": msg.content})
                history_count += 1
            elif isinstance(msg, AIMessage) and msg.content:
                chat_messages.append({"role": "assistant", "content": msg.content})
                history_count += 1
            if history_count >= 10:
                break

        # 添加当前用户消息
        chat_messages.append({"role": "user", "content": user_message})

        logger.info(f"[LangGraph] General直接对话: {len(chat_messages)}条消息")

        # 直接调用LLM生成响应
        result = await self._generate_text(
            messages=chat_messages,
            max_tokens=500,  # 闲聊不需要太长
            temperature=0.7,
            task_type=TaskType.SIMPLE_QA  # 使用轻量模型
        )

        response_text = result.get("text", "您好！有什么可以帮您的？")

        response = AIMessage(content=response_text)
        return {
            "messages": [response],
            "final_response": response_text,
            "agent_steps": [{
                "step": "general_direct_response",
                "result": "直接对话响应（跳过工具决策）"
            }]
        }

    async def chat_stream(
        self,
        message: str,
        user_id: Optional[str] = None,  # 新增：用户ID（用于长期记忆隔离）
        work_id: Optional[str] = None,
        chapter_id: Optional[str] = None,
        conversation_id: Optional[str] = None,
        context: Optional[dict] = None,
        on_progress: Optional[callable] = None,
        on_tool_call: Optional[callable] = None,
        on_content: Optional[callable] = None,
        db: Optional[Any] = None  # 新增：数据库会话（用于token记录）
    ) -> dict:
        """
        流式执行chat()，提供实时进度反馈（已集成上下文管理）

        Args:
            message: 用户消息
            user_id: 用户ID（用于长期记忆隔离）
            work_id: 作品ID
            chapter_id: 章节ID
            conversation_id: 会话ID
            context: 额外上下文
            on_progress: 进度回调 async def on_progress(event: dict)
            on_tool_call: 工具调用回调 async def on_tool_call(tool_name: str, tool_args: dict)
            on_content: 内容生成回调 async def on_content(content: str)
            db: 数据库会话（用于token记录到AICallLog）

        Returns:
            Dict: Agent响应（同chat()方法）
        """

        # 🔧 监控：导入监控工具
        import time
        from app.services.agent.utils.monitoring import increment_counter, record_timer

        # 🔧 监控：记录总体开始时间
        overall_start = time.time()

        logger.info(f"[LangGraph Stream] 开始流式执行: {message[:50]}...")

        # ✅ 前端兜底：若未传 conversation_id，则生成随机ID并返回给前端
        if not conversation_id:
            conversation_id = str(uuid.uuid4())
            logger.warning(f"[LangGraph Stream] 未提供 conversation_id，自动生成: {conversation_id}")

        # ✅ 前端兜底：提示缺失 work_id 可能导致跨作品污染
        if not work_id:
            logger.warning("[LangGraph Stream] work_id 缺失，将退化为用户/会话级隔离，请尽快在前端补充 work_id 以防跨作品污染")

        # 懒加载AsyncRedisSaver索引
        if isinstance(self.checkpointer, AsyncRedisSaver) and not self._checkpointer_setup_done:
            try:
                await self.checkpointer.asetup()
                self._checkpointer_setup_done = True
                logger.info(f"[LangGraph] AsyncRedisSaver索引创建成功")
            except Exception as setup_error:
                logger.error(f"[LangGraph] AsyncRedisSaver索引创建失败: {setup_error}")
                raise

        # 🔧 新增：构建上下文（加载历史对话）
        session_id = conversation_id

        # 动态设置user_id（用于长期记忆隔离）
        if user_id:
            self.context_manager.user_id = user_id
            logger.info(f"[Context] 设置用户ID: {user_id}")

        # ✅ 优化：移除重复的意图识别
        # LangGraph的intent_classifier节点会自动完成意图识别
        # 这里不再预先识别,避免重复调用

        # 🔧 监控：上下文构建计时
        context_start = time.time()

        # 使用默认的writing_agent模板（LangGraph会根据实际意图动态切换）
        system_prompt = self.prompt_manager.render(
            "writing_agent",
            user_message=message,
            context_summary="",
            user_preferences={},
            writing_constraints=[],
            examples=[]
        )

        context_bundle = await self.context_manager.build_context(
            session_id=session_id,
            system_prompt=system_prompt,
            query=message,  # 新增：触发长期记忆检索
            work_id=work_id  # ✅ P0-2修复：传递work_id隔离向量记忆
        )

        # 🔧 监控：记录上下文构建耗时
        record_timer("context_build_duration", time.time() - context_start)

        logger.info(f"[Context] 加载上下文: {context_bundle['metadata']}")

        # 🔧 新增：将历史消息转换为LangGraph消息格式
        history_messages = []
        for msg in context_bundle["messages"]:
            if msg["role"] == "system":
                history_messages.append(SystemMessage(content=msg["content"]))
            elif msg["role"] == "user":
                history_messages.append(HumanMessage(content=msg["content"]))
            elif msg["role"] == "assistant":
                history_messages.append(AIMessage(content=msg["content"]))

        # 构建初始状态（不预设intent,由LangGraph的intent_classifier节点识别）
        knowledge_messages = _build_knowledge_system_messages(context)

        initial_state = {
            "messages": knowledge_messages + history_messages + [HumanMessage(content=message)],  # 知识上下文 + 历史消息 + 当前消息
            "work_id": work_id,
            "chapter_id": chapter_id,
            "intent": None,  # ✅ 优化：由LangGraph的intent_classifier节点自动识别
            "context": context or {},
            "agent_steps": [],
            "suggested_actions": [],
            "final_response": None
        }

        # ✅ P0-3修复：构建隔离的thread_id（包含user_id和work_id）
        # 三层隔离：user_id > work_id > conversation_id，避免跨用户/跨作品污染
        user_prefix = f"{user_id}:" if user_id else ""

        if work_id and conversation_id:
            thread_id = f"{user_prefix}{work_id}:{conversation_id}"
        elif work_id:
            thread_id = f"{user_prefix}{work_id}:default"
        elif conversation_id:
            thread_id = f"{user_prefix}{conversation_id}"
        else:
            # 兜底：无user_id时使用随机UUID，确保不会全局共享
            thread_id = f"{user_prefix}anonymous:{uuid.uuid4()}" if not user_prefix else f"{user_prefix}default"

        # ✅ P2防护：thread_id长度验证
        max_thread_id_length = ContextConfig.MAX_THREAD_ID_LENGTH
        if len(thread_id) > max_thread_id_length:
            import hashlib as _hashlib
            logger.warning(
                f"[LangGraph] thread_id过长({len(thread_id)}字符), "
                f"使用哈希缩短"
            )
            hash_suffix = _hashlib.sha1(thread_id.encode("utf-8")).hexdigest()[:10]
            prefix_budget = max_thread_id_length - len(hash_suffix) - 1
            thread_id = f"{thread_id[:prefix_budget]}:{hash_suffix}"

        logger.info(f"[LangGraph] 使用隔离的thread_id: {thread_id} (user_id={user_id}, work_id={work_id}, conversation_id={conversation_id})")

        # 配置
        config = {
            "configurable": {
                "thread_id": thread_id  # ✅ 使用work_id隔离的thread_id
            }
        }

        # ✅ 初始化ProgressTracker（不预设expected_nodes，完全动态追踪）
        progress_tracker = None
        try:
            # 不传expected_nodes/scenario，让ProgressTracker根据实际执行的节点动态计算进度
            # 这样可以自适应任何intent（general/writing/planning/analysis/stuck）
            # ProgressTracker内部有平滑处理机制，避免进度倒退
            progress_tracker = ProgressTracker()
            logger.info("[ProgressTracker] 初始化完成，使用动态节点追踪模式")
        except Exception as e:
            logger.error(f"[ProgressTracker] 初始化失败: {e}，将继续执行但不提供进度信息")
            progress_tracker = None  # 降级：不使用ProgressTracker

        try:
            # 🔧 监控：LangGraph执行计时
            graph_start = time.time()

            # 使用astream()流式执行
            event_count = 0

            # ✅ 添加超时保护（使用统一配置）
            async with async_timeout(TimeoutConfig.LANGGRAPH_STREAM):
                async for event in self.graph.astream_events(initial_state, config, version="v2"):
                    event_count += 1

                    # 提取事件类型和数据
                    event_type = event.get("event")
                    event_name = event.get("name")
                    event_data = event.get("data", {})

                    # ✅ 处理节点开始事件
                    if event_type == "on_chain_start" and event_name:
                        if progress_tracker:
                            progress_tracker.start_node(event_name)
                            logger.debug(f"[ProgressTracker] 节点开始: {event_name}")

                    # ✅ 处理节点结束事件
                    elif event_type == "on_chain_end" and event_name:
                        # ✅ P0-6调试：打印tools节点的事件数据
                        if event_name == "tools":
                            logger.info(f"[HITL Debug] tools节点on_chain_end事件: event_data keys={list(event_data.keys())}")
                            output_data_preview = event_data.get("output")
                            if output_data_preview:
                                logger.info(f"[HITL Debug] output keys={list(output_data_preview.keys()) if isinstance(output_data_preview, dict) else type(output_data_preview)}")
                                if isinstance(output_data_preview, dict) and "messages" in output_data_preview:
                                    logger.info(f"[HITL Debug] messages数量={len(output_data_preview['messages'])}")
                                    for i, msg in enumerate(output_data_preview["messages"]):
                                        logger.info(f"[HITL Debug] message[{i}]: type={type(msg).__name__}, name={getattr(msg, 'name', 'N/A')}")

                        # 构造原格式的event用于现有逻辑，添加降级处理
                        output_data = event_data.get("output")
                        if output_data is None:
                            output_data = event_data  # 降级：使用完整event_data
                        formatted_event = {event_name: output_data}

                        # 处理事件并触发回调
                        await self._handle_stream_event(
                            formatted_event,
                            on_progress=on_progress,
                            on_tool_call=on_tool_call,
                            on_content=on_content,
                            progress_tracker=progress_tracker,  # ✅ 传递ProgressTracker
                            context=context  # ✅ P0-6修复：传递context用于HITL回调
                        )

                    # ✅ 处理节点错误事件
                    elif event_type == "on_chain_error" and event_name:
                        if progress_tracker:
                            progress_tracker.end_node(event_name)  # 标记节点完成（即使失败）
                            logger.error(f"[ProgressTracker] 节点失败: {event_name}")

            # 🔧 监控：记录LangGraph执行耗时
            record_timer("graph_execution_duration", time.time() - graph_start)

            logger.info(f"[LangGraph Stream] 流式执行完成，共{event_count}个事件")

            # 获取最终状态
            final_state = await self.graph.aget_state(config)

            # 构建返回结果（与chat()相同的格式）
            if final_state and final_state.values:
                result = final_state.values
                final_response = result.get("final_response")

                # 🔧 新增：更新上下文（保存本轮对话）
                # ✅ P0-2补充修复：传递work_id以正确保存向量记忆
                await self.context_manager.update_context(
                    session_id=session_id,
                    new_messages=[
                        {"role": "user", "content": message},
                        {"role": "assistant", "content": final_response or ""}
                    ],
                    context=context_bundle.get("context"),
                    work_id=work_id  # ✅ 新增：传递work_id
                )
                logger.info(f"[Context] 上下文已更新: {session_id} (work_id={work_id})")

                # 🔧 监控：记录成功
                increment_counter("chat_stream_success")
                record_timer("chat_stream_total_duration", time.time() - overall_start)

                return {
                    "response": final_response,
                    "conversation_id": conversation_id,
                    "messages": result.get("messages", []),
                    "agent_steps": result.get("agent_steps", []),
                    "suggested_actions": result.get("suggested_actions", []),
                    "metadata": {
                        "intent": result.get("intent"),
                        "timestamp": str(get_utc_now()),
                        "stream_events": event_count,
                        "context_token_count": context_bundle["metadata"]["token_count"]
                    }
                }
            else:
                logger.error("[LangGraph Stream] 无法获取最终状态")

                # 🔧 监控：记录失败（无最终状态）
                increment_counter("chat_stream_error", labels={"error_type": "NoFinalState"})
                record_timer("chat_stream_total_duration", time.time() - overall_start)

                return {
                    "response": "执行完成，但无法获取结果",
                    "conversation_id": conversation_id,
                    "agent_steps": [],
                    "suggested_actions": [],
                    "metadata": {"error": "No final state"}
                }

        except asyncio.TimeoutError:
            # ✅ 超时异常的特殊处理
            logger.error(f"[LangGraph Stream] 执行超时（{TimeoutConfig.LANGGRAPH_STREAM}秒）")

            # 🔧 监控：记录超时
            increment_counter("chat_stream_error", labels={"error_type": "TimeoutError"})
            record_timer("chat_stream_total_duration", time.time() - overall_start)

            return {
                "response": "抱歉，请求处理超时（超过5分钟）。请尝试简化您的问题或稍后再试。",
                "conversation_id": conversation_id,
                "agent_steps": [],
                "suggested_actions": ["简化问题", "稍后重试"],
                "metadata": {"error": f"Request timeout after {TimeoutConfig.LANGGRAPH_STREAM} seconds", "timeout": TimeoutConfig.LANGGRAPH_STREAM}
            }

        except Exception as e:
            import traceback
            error_msg = str(e) or repr(e)
            error_trace = traceback.format_exc()

            # 🔧 监控：记录异常
            increment_counter("chat_stream_error", labels={"error_type": type(e).__name__})
            record_timer("chat_stream_total_duration", time.time() - overall_start)

            logger.error(f"[LangGraph Stream] 执行失败: {error_msg}")
            logger.error(f"[LangGraph Stream] 错误堆栈:\n{error_trace}")
            return {
                "response": f"抱歉，处理您的请求时出错了：{error_msg}",
                "conversation_id": conversation_id,
                "agent_steps": [],
                "suggested_actions": [],
                "metadata": {"error": error_msg, "traceback": error_trace}
            }

        finally:
            # ✅ 新增：清理ProgressTracker（P1任务7）
            if progress_tracker:
                try:
                    # 重置tracker状态，释放资源
                    progress_tracker.reset()
                    del progress_tracker
                    logger.debug("[ProgressTracker] 已清理")
                except Exception as e:
                    logger.warning(f"[ProgressTracker] 清理失败: {e}")

    async def _handle_stream_event(
        self,
        event: dict,
        on_progress: Optional[callable] = None,
        on_tool_call: Optional[callable] = None,
        on_content: Optional[callable] = None,
        progress_tracker: Optional[ProgressTracker] = None,  # ✅ 新增参数
        context: Optional[dict] = None  # ✅ P0-5修复：接收context用于HITL回调
    ):
        """处理astream事件，转换为用户友好的进度信息并触发回调"""

        if not event:
            return

        # 提取节点名和数据
        node_name = list(event.keys())[0]
        node_data = event[node_name]

        logger.info(f"[Stream Event] 节点: {node_name}")  # 改为info级别

        # ✅ 追踪节点完成
        if progress_tracker:
            progress_tracker.end_node(node_name)
            logger.debug(f"[ProgressTracker] 节点完成: {node_name}")

        # 🔧 缓存agent节点的工具调用参数（用于后续tools节点显示）
        if node_name in ["writing_agent", "planning_agent", "analysis_agent", "stuck_agent", "general_agent"]:
            messages = node_data.get("messages", [])
            for msg in reversed(messages):
                if isinstance(msg, AIMessage) and hasattr(msg, "tool_calls") and msg.tool_calls:
                    for tool_call in msg.tool_calls:
                        tool_name = tool_call.get("name")
                        tool_args = tool_call.get("args", {})
                        if tool_name:
                            self._cached_tool_calls[tool_name] = tool_args
                            logger.debug(f"[Cache] 缓存工具参数: {tool_name} -> {tool_args}")
                    break  # 只缓存最新的一条AIMessage

        # 1. 解析进度事件并触发on_progress
        if on_progress:
            progress_event = self._parse_node_event(node_name, node_data, progress_tracker)  # ✅ 传递tracker
            if progress_event:
                logger.info(f"[Stream Event] progress_event = {progress_event}")  # 添加日志
                try:
                    await on_progress(progress_event)
                    logger.info(f"[Stream Event] on_progress 回调已调用")  # 添加日志
                except Exception as e:
                    logger.error(f"[Stream] 进度回调失败: {e}")

        # 2. 检测工具调用并触发on_tool_call + HITL确认请求
        if node_name == "tools":
            # 2a. 触发工具调用回调
            if on_tool_call:
                tool_calls = self._extract_tool_calls(node_data)
                for tool_name, tool_args in tool_calls:
                    try:
                        await on_tool_call(tool_name, tool_args)
                    except Exception as e:
                        logger.error(f"[Stream] 工具回调失败: {e}")

            # 2b. ✅ P0-6修复：检测HITL确认请求（使用实例变量，避免序列化）
            if self._approval_callback:
                messages = node_data.get("messages", [])

                # 遍历ToolMessage，检查是否需要确认
                for msg in messages:
                    if isinstance(msg, ToolMessage):
                        try:
                            import json
                            # 尝试解析工具返回结果
                            content_length = len(msg.content) if msg.content else 0
                            logger.info(f"[HITL] 检查工具消息: {msg.name}, content长度={content_length}, 前100字符: {msg.content[:100]}")
                            tool_result = json.loads(msg.content)

                            # ✅ P0-6调试：打印完整解析结果
                            logger.info(f"[HITL] 解析成功，requires_confirmation={tool_result.get('requires_confirmation')}, keys={list(tool_result.keys())}")
                            logger.info(f"[HITL] 完整tool_result: {tool_result}")

                            # 检查是否需要用户确认
                            if tool_result.get("requires_confirmation"):
                                logger.info(f"[HITL] 检测到确认请求: {tool_result.get('action_type')}")

                                # ✅ P0-6调试：检查回调是否存在
                                if not self._approval_callback:
                                    logger.error(f"[HITL] ❌ _approval_callback 未设置！")
                                    continue

                                # ✅ P0-6修复：使用实例变量而非context中的回调
                                # ✅ 更新：versions现在包含实际改写内容
                                versions = tool_result.get("versions") or tool_result.get("recommendations")
                                approval_data = {
                                    "request_id": f"{msg.name}_{msg.tool_call_id}",  # 生成唯一ID
                                    "action_type": tool_result.get("action_type", "edit"),
                                    "operation": tool_result.get("operation"),
                                    "original_content": tool_result.get("original_text"),
                                    "new_content": tool_result.get("content"),
                                    "description": tool_result.get("description"),
                                    "versions": versions,  # smart_rewrite的改写版本（包含content）
                                    "chapter_id": tool_result.get("chapter_id"),
                                    # 🆕 InlineAI: 包含 editor_action 信息
                                    "editor_action": tool_result.get("editor_action")
                                }
                                logger.info(f"[HITL] 准备调用回调: request_id={approval_data['request_id']}, versions数量={len(versions) if versions else 0}, editor_action={approval_data.get('editor_action')}")
                                await self._approval_callback(approval_data)
                                logger.info(f"[HITL] ✅ 回调执行成功")

                        except json.JSONDecodeError as e:
                            logger.warning(f"[HITL] JSON解析失败: {msg.name}, error={e}, content前200字符={msg.content[:200]}")
                        except Exception as e:
                            logger.error(f"[HITL] 处理确认请求失败: {msg.name}, error={e}", exc_info=True)

        # 3. 检测内容生成并触发on_content
        if on_content:
            content = self._extract_content(node_name, node_data)
            if content:
                try:
                    await on_content(content)
                except Exception as e:
                    logger.error(f"[Stream] 内容回调失败: {e}")

    def _parse_node_event(
        self,
        node_name: str,
        node_data: dict,
        progress_tracker: Optional[ProgressTracker] = None  # ✅ 新增参数
    ) -> Optional[dict]:
        """将LangGraph节点事件转换为用户友好的进度信息"""

        # 节点映射表
        node_mapping = {
            "intent_classifier": {
                "step": "intent_analysis",
                "description": "正在分析您的需求..."
            },
            "writing_agent": {
                "step": "thinking",
                "description": "正在思考如何帮助您..."
            },
            "planning_agent": {
                "step": "thinking",
                "description": "正在规划方案..."
            },
            "analysis_agent": {
                "step": "thinking",
                "description": "正在分析内容..."
            },
            "stuck_agent": {
                "step": "thinking",
                "description": "正在寻找解决方案..."
            },
            "general_chat": {
                "step": "thinking",
                "description": "正在思考回复..."
            },
            "tools": {
                "step": "tool_execution",
                "description": "正在调用工具..."
            }
        }

        mapping = node_mapping.get(node_name)
        if not mapping:
            return None

        # 提取额外信息
        details = {}

        if node_name == "intent_classifier":
            # 提取识别的意图
            intent = node_data.get("intent")
            if intent:
                details["intent"] = intent
                # 更新描述
                intent_names = {
                    "writing": "写作任务",
                    "planning": "规划任务",
                    "analysis": "分析任务",
                    "stuck": "卡文求助",
                    "general": "一般对话"
                }
                intent_display = intent_names.get(intent, intent)
                mapping["description"] = f"识别为：{intent_display}"

        elif node_name == "tools":
            # ✅ 从AIMessage提取tool_calls参数
            messages = node_data.get("messages", [])
            tool_info = None

            # 🔍 DEBUG: 输出消息列表
            logger.debug(f"[Tools Node] messages数量: {len(messages)}")

            # 寻找AIMessage中的tool_calls（倒序查找最新的）
            for msg in reversed(messages):
                if isinstance(msg, AIMessage) and hasattr(msg, "tool_calls") and msg.tool_calls:
                    # 🔍 DEBUG: 输出tool_calls结构
                    logger.info(f"[Tools Node] 找到AIMessage with tool_calls: {msg.tool_calls}")

                    # 取第一个tool_call
                    tool_call = msg.tool_calls[0]

                    # 🔍 DEBUG: 输出tool_call详情
                    logger.info(f"[Tools Node] tool_call详情: name={tool_call.get('name')}, args={tool_call.get('args')}")

                    tool_info = {
                        "name": tool_call.get("name"),
                        "args": tool_call.get("args", {})
                    }
                    break

            # 如果没找到AIMessage的tool_calls，尝试从ToolMessage提取（向后兼容）
            if not tool_info:
                logger.warning("[Tools Node] 未找到AIMessage的tool_calls，尝试从ToolMessage提取")
                for msg in messages:
                    if hasattr(msg, "name"):
                        tool_info = {
                            "name": msg.name,
                            "args": {}
                        }
                        break

            if tool_info:
                tool_name = tool_info["name"]
                tool_args = tool_info["args"]

                # 🔧 优先使用缓存的参数（如果有）
                if tool_name in self._cached_tool_calls:
                    cached_args = self._cached_tool_calls[tool_name]
                    logger.info(f"[Tools Node] 使用缓存参数: {tool_name} -> {cached_args}")
                    tool_args = cached_args
                    # 使用后清除缓存
                    del self._cached_tool_calls[tool_name]

                # 🔍 DEBUG: 输出最终使用的参数
                logger.info(f"[Tools Node] 最终使用: tool_name={tool_name}, tool_args={tool_args}")

                details["tools"] = [tool_name]
                details["tool_args"] = tool_args

                # ✅ 根据工具和参数生成具体描述
                mapping["description"] = self._generate_tool_description(tool_name, tool_args)

        # ✅ 从ProgressTracker获取进度信息
        progress_data = {}
        if progress_tracker:
            try:
                progress_event = progress_tracker.get_progress_event()
                progress_data = {
                    "progress": progress_event.get("progress"),
                    "eta": progress_event.get("eta"),
                    "eta_display": progress_event.get("eta_display"),
                    "eta_confidence": progress_event.get("eta_confidence"),
                    "current_step": progress_event.get("current_step"),
                    "total_steps": progress_event.get("total_steps"),
                    "step_description": progress_event.get("step_description"),
                    "elapsed": progress_event.get("elapsed")
                }
                logger.debug(
                    f"[ProgressTracker] 进度: {progress_data['progress']}%, "
                    f"ETA: {progress_data['eta_display']}"
                )
            except Exception as e:
                logger.error(
                    f"[ProgressTracker] 获取进度失败: {e}, "
                    f"类型: {type(e).__name__}, "
                    f"当前节点: {progress_tracker.current_node if hasattr(progress_tracker, 'current_node') else 'unknown'}, "
                    f"已完成: {len(progress_tracker.completed_nodes) if hasattr(progress_tracker, 'completed_nodes') else 0}个节点",
                    exc_info=True  # 包含完整堆栈跟踪
                )
                # 失败时使用空数据，不影响主流程
                progress_data = {}

        # ✅ 合并所有信息
        return {
            "type": "progress",
            "step": mapping["step"],
            "description": mapping["description"],
            "node": node_name,
            "details": details,
            "timestamp": get_utc_now().isoformat(),
            **progress_data  # ✅ 包含进度信息
        }

    def _extract_tool_calls(self, node_data: dict) -> list:
        """提取工具调用信息"""
        tool_calls = []
        messages = node_data.get("messages", [])

        for msg in messages:
            if isinstance(msg, ToolMessage) and hasattr(msg, "name"):
                tool_name = msg.name
                tool_args = {}
                tool_calls.append((tool_name, tool_args))

        return tool_calls

    def _generate_tool_description(self, tool_name: str, tool_args: dict) -> str:
        """根据工具名称和参数生成具体描述

        Args:
            tool_name: 工具名称
            tool_args: 工具参数字典

        Returns:
            str: 具体的描述文本
        """
        # get_chapter_by_order_tool - 读取章节
        if tool_name == "get_chapter_by_order_tool":
            chapter_order = tool_args.get("chapter_order", "?")
            return f"📚 正在读取第{chapter_order}章..."

        # continue_writing_tool - 续写内容
        elif tool_name == "continue_writing_tool":
            target_words = tool_args.get("target_words")
            if target_words:
                return f"✍️ 正在创作内容（目标{target_words}字）..."
            return "✍️ 正在创作内容..."

        # search_analysis_fragments_tool - 检索设定
        elif tool_name == "search_analysis_fragments_tool":
            query = tool_args.get("query", "")
            if query and len(query) <= 20:  # 只显示较短的查询
                return f"🔍 正在检索「{query}」相关设定..."
            return "🔍 正在检索设定..."

        # search_memory_tool - 搜索记忆
        elif tool_name == "search_memory_tool":
            query = tool_args.get("query", "")
            if query and len(query) <= 20:
                return f"💭 正在搜索「{query}」相关记忆..."
            return "💭 正在搜索记忆..."

        # analyze_text_tool - 分析文本
        elif tool_name == "analyze_text_tool":
            return "🔍 正在分析文本..."

        # add_todo_tool - 添加待办
        elif tool_name == "add_todo_tool":
            return "📝 正在添加待办事项..."

        # get_work_details_tool - 获取作品信息
        elif tool_name == "get_work_details_tool":
            return "📖 正在获取作品信息..."

        # update_work_metadata_tool - 更新元数据
        elif tool_name == "update_work_metadata_tool":
            return "💾 正在更新作品元数据..."

        # 默认描述（向后兼容）
        tool_display_names = {
            "get_chapter_by_order_tool": "读取章节",
            "continue_writing_tool": "继续创作",
            "search_analysis_fragments_tool": "检索设定",
            "search_memory_tool": "搜索记忆",
            "add_todo_tool": "添加待办",
            "get_work_details_tool": "获取作品信息",
            "update_work_metadata_tool": "更新元数据",
            "analyze_text_tool": "分析文本"
        }
        display_name = tool_display_names.get(tool_name, tool_name)
        return f"正在{display_name}..."

    def _extract_content(self, node_name: str, node_data: dict) -> Optional[str]:
        """提取生成的内容"""
        # 只处理agent节点
        if not node_name.endswith("_agent") and node_name != "general_chat":
            return None

        messages = node_data.get("messages", [])
        if not messages:
            return None

        last_message = messages[-1]
        if isinstance(last_message, AIMessage) and last_message.content:
            # 避免返回工具调用指令
            if not hasattr(last_message, "tool_calls") or not last_message.tool_calls:
                return last_message.content

        return None

    def _extract_json_from_text(self, text: str) -> Optional[dict]:
        """从文本中提取JSON对象

        支持：
        1. 纯JSON
        2. Markdown代码块包裹的JSON
        3. 混合文本中的JSON
        """
        import json
        import re

        text = text.strip()

        if not text:
            logger.error("[JSON解析] 输入文本为空")
            return None

        # 方法1: 尝试直接解析（最快）
        try:
            result = json.loads(text)
            logger.info("[JSON解析] 方法1成功: 直接解析")
            return result
        except json.JSONDecodeError as e:
            logger.debug(f"[JSON解析] 方法1失败: {e}")

        # 方法2: 尝试去除Markdown代码块 ```json ... ```
        if "```json" in text:
            # 使用贪婪匹配，确保捕获完整JSON
            match = re.search(r'```json\s*\n(.*?)```', text, re.DOTALL)
            if match:
                json_str = match.group(1).strip()
                try:
                    result = json.loads(json_str)
                    logger.info("[JSON解析] 方法2成功: 从```json块提取")
                    return result
                except json.JSONDecodeError as e:
                    logger.warning(f"[JSON解析] 方法2失败: {e}, JSON字符串: {json_str[:200]}")

        # 方法3: 尝试去除普通代码块 ``` ... ```
        if "```" in text:
            match = re.search(r'```\s*\n(.*?)```', text, re.DOTALL)
            if match:
                json_str = match.group(1).strip()
                try:
                    result = json.loads(json_str)
                    logger.info("[JSON解析] 方法3成功: 从```块提取")
                    return result
                except json.JSONDecodeError as e:
                    logger.warning(f"[JSON解析] 方法3失败: {e}, JSON字符串: {json_str[:200]}")

        # 方法4: 使用正则查找第一个完整的JSON对象 { ... }
        # 注意：要处理字符串中的大括号（在字符串中的大括号不算）
        match = re.search(r'\{[^{}]*(?:\{[^{}]*\}[^{}]*)*\}', text, re.DOTALL)
        if match:
            json_str = match.group(0)
            try:
                result = json.loads(json_str)
                logger.info("[JSON解析] 方法4成功: 正则匹配JSON对象")
                return result
            except json.JSONDecodeError as e:
                logger.warning(f"[JSON解析] 方法4失败: {e}, JSON字符串: {json_str[:200]}")

        # 方法5: 逐字符扫描，手动匹配大括号（最后的手段）
        in_string = False
        escape = False
        brace_count = 0
        start_idx = -1

        for i, char in enumerate(text):
            if escape:
                escape = False
                continue

            if char == '\\':
                escape = True
                continue

            if char == '"' and not escape:
                in_string = not in_string
                continue

            if not in_string:
                if char == '{':
                    if brace_count == 0:
                        start_idx = i
                    brace_count += 1
                elif char == '}':
                    brace_count -= 1
                    if brace_count == 0 and start_idx != -1:
                        # 找到完整的JSON对象
                        json_str = text[start_idx:i+1]
                        try:
                            result = json.loads(json_str)
                            logger.info("[JSON解析] 方法5成功: 手动扫描大括号")
                            return result
                        except json.JSONDecodeError as e:
                            logger.warning(f"[JSON解析] 方法5失败: {e}, JSON字符串: {json_str[:200]}")
                            # 继续查找下一个
                            start_idx = -1

        logger.error(f"[JSON解析] 所有方法均失败，原始文本: {text[:500]}")
        return None

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
        db: Optional[Any] = None,
        enable_reflection: bool = False  # DeepAgent 反思模式
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
            db: 数据库会话（用于token记录）
            enable_reflection: 是否启用DeepAgent反思模式

        Returns:
            Dict: Agent响应
        """
        # ✅ P0-2: 添加360秒总体超时保护（6分钟）
        try:
            import time
            from app.services.agent.utils.monitoring import increment_counter, record_timer
            start_time = time.time()

            # ✅ P0修复：构建隔离的thread_id（包含user_id和work_id）
            # 三层隔离：user_id > work_id > conversation_id，避免跨用户/跨作品污染
            user_prefix = f"{user_id}:" if user_id else ""

            if work_id and conversation_id:
                isolated_thread_id = f"{user_prefix}{work_id}:{conversation_id}"
            elif work_id:
                isolated_thread_id = f"{user_prefix}{work_id}:default"
            elif conversation_id:
                isolated_thread_id = f"{user_prefix}{conversation_id}"
            else:
                # 兜底：无user_id时使用随机UUID，确保不会全局共享
                import uuid as uuid_module
                isolated_thread_id = f"{user_prefix}anonymous:{uuid_module.uuid4()}" if not user_prefix else f"{user_prefix}default"

            # ✅ P2防护：thread_id长度验证
            max_thread_id_length = ContextConfig.MAX_THREAD_ID_LENGTH
            if len(isolated_thread_id) > max_thread_id_length:
                import hashlib as _hashlib
                logger.warning(
                    f"[Planning] thread_id过长({len(isolated_thread_id)}字符), "
                    f"使用哈希缩短"
                )
                hash_suffix = _hashlib.sha1(isolated_thread_id.encode("utf-8")).hexdigest()[:10]
                prefix_budget = max_thread_id_length - len(hash_suffix) - 1
                isolated_thread_id = f"{isolated_thread_id[:prefix_budget]}:{hash_suffix}"

            logger.info(
                f"[Planning] 使用隔离的thread_id: {isolated_thread_id} "
                f"(user_id={user_id}, work_id={work_id}, conversation_id={conversation_id})"
            )

            # 设置总体超时（使用统一配置）
            async with async_timeout(TimeoutConfig.TASK_EXECUTION):
                # ========== 加载对话历史（使用 ContextManager 压缩） ==========
                conversation_history = ""
                context_bundle = None  # 保存上下文包，用于后续更新

                # 动态设置 user_id（用于长期记忆隔离）
                if user_id:
                    self.context_manager.user_id = user_id

                try:
                    # 使用 ContextManager 构建上下文（自动压缩）
                    context_bundle = await self.context_manager.build_context(
                        session_id=isolated_thread_id,
                        system_prompt="",  # Planning 阶段不需要系统提示
                        query=message,
                        work_id=work_id
                    )

                    # 从压缩后的上下文中提取历史消息
                    messages = context_bundle.get("messages", [])
                    if messages:
                        logger.info(
                            f"[Planning] 从 ContextManager 加载了 {len(messages)} 条历史消息 "
                            f"(token: {context_bundle['metadata'].get('token_count', 0)})"
                        )
                        # 格式化历史消息（保持原有格式兼容）
                        history_lines = []
                        for msg in messages:
                            role = msg.get("role", "")
                            content = msg.get("content", "")
                            if role == "user":
                                history_lines.append(f"用户: {content}")
                            elif role == "assistant":
                                history_lines.append(f"助手: {content}")
                        if history_lines:
                            conversation_history = "\n".join(history_lines)
                except Exception as e:
                    logger.warning(f"[Planning] ContextManager 加载历史失败: {e}", exc_info=True)

                # ========== 快速路径判断（新增）==========
                # 在规划生成前判断是否可以走快速路径
                enable_quick_path = os.getenv("ENABLE_QUICK_PATH", "true").lower() == "true"

                if enable_quick_path:
                    quick_result = await self._try_quick_path_for_planning(
                        message=message,
                        work_id=work_id,
                        on_plan=on_plan,
                        on_task_start=on_task_start,
                        on_task_done=on_task_done,
                        on_content=on_content
                    )
                    if quick_result:
                        logger.info(f"[Planning] 快速路径命中，跳过规划流程")
                        # ✅ 修复：快速路径也需要保存对话到 ContextManager
                        try:
                            await self.context_manager.update_context(
                                session_id=isolated_thread_id,
                                new_messages=[
                                    {"role": "user", "content": message},
                                    {"role": "assistant", "content": quick_result.get("response", "")}
                                ],
                                context=context_bundle.get("context") if context_bundle else None,
                                work_id=work_id
                            )
                            logger.info(f"[Planning] 快速路径对话已保存到 ContextManager")
                        except Exception as e:
                            logger.warning(f"[Planning] 快速路径保存对话失败: {e}")
                        return quick_result

                # ========== 阶段1: 规划（Planning） ==========
                # ✅ P1-7: 添加监控记录
                planning_start = time.time()
                logger.info(f"[Planning] 开始规划: {message[:50]}...")
                increment_counter("planning_phase_start")

                # 构建规划prompt（包含历史）
                history_section = ""
                if conversation_history:
                    history_section = f"""
【对话历史】
{conversation_history}

"""

                # ✅ Phase 2.6: 使用缓存的静态 Prompt（节省构建时间和 Token）
                # ✅ 2025-12-08: Agent 模式使用增强版 Prompt（支持 checkpoint 标记）
                if enable_reflection:
                    static_prompt = await get_planning_agent_mode_prompt()
                else:
                    static_prompt = await get_planning_static_prompt()

                # ✅ P0修复: 注入知识库文档到Planning prompt
                knowledge_section = ""
                knowledge_docs = context.get("knowledge_docs") if context else []
                if knowledge_docs:
                    logger.info(f"[Planning] 注入 {len(knowledge_docs)} 个知识库文档到prompt")
                    knowledge_parts = []
                    for doc in knowledge_docs[:3]:  # 最多3个文档
                        title = doc.get("title") or "未命名文档"
                        tags = doc.get("tags") or []
                        source = doc.get("source_type") or "unknown"
                        content = doc.get("content") or ""
                        # 截取摘要，避免prompt过长
                        snippet = content.strip()[:800] if content else ""
                        if snippet:
                            # ✅ P0修复: 更明确地标注文档元数据，避免AI混淆
                            tags_str = ', '.join(tags) if tags else '无'
                            knowledge_parts.append(
                                f"=== 知识库文档 ===\n"
                                f"文档标题: {title}\n"
                                f"文档来源: {source}\n"
                                f"文档标签: {tags_str}\n"
                                f"文档正文内容:\n{snippet}\n"
                                f"=== 文档结束 ==="
                            )
                    if knowledge_parts:
                        knowledge_section = "\n\n【用户引用的知识库文档】\n请参考以下文档内容回答用户问题：\n\n" + "\n\n".join(knowledge_parts) + "\n\n"

                # ✅ 2025-12-08 修复: 注入用户选中的文本到 Planning prompt
                selected_text_section = ""
                if context:
                    selected_text = context.get("selected_text") or ""
                    instruction_context = context.get("instruction_context") or ""
                    selection_position = context.get("selection_position")

                    if selected_text:
                        logger.info(f"[Planning] 注入选中文本到prompt: {selected_text[:50]}...")
                        selected_text_section = f"""

【用户选中的文本】
以下是用户在编辑器中选中的文本，请针对这段文本执行用户的指令：
---
{selected_text}
---
选区位置: from={selection_position.get('from') if selection_position else 'N/A'}, to={selection_position.get('to') if selection_position else 'N/A'}

"""
                    elif instruction_context:
                        # 如果没有 selected_text 但有 instruction_context，也注入
                        logger.info(f"[Planning] 注入指令上下文到prompt")
                        selected_text_section = f"""

【用户指令上下文】
{instruction_context}

"""

                # 🆕 动态添加章节上下文提示（如果存在 chapter_id）
                chapter_planning_hint = ""
                if chapter_id:
                    chapter_planning_hint = f"""

⚠️ 【章节上下文提示】：
- 当前用户在章节聊天面板中（chapter_id={chapter_id}）
- 用户要求修改/润色本章内容时，必须使用以下流程：
  1. 任务1: 调用 read_chapter_tool(work_id="{work_id}", chapter_id="{chapter_id}") 读取章节完整内容
  2. 任务2: 调用 analyze_text_tool 分析原文中该句话的场景、情绪、角色状态
  3. 任务3: 基于分析结果，给出符合场景的多个修改建议（用 analyze_text_tool 输出）
- ✅ 正确示例：read_chapter_tool → analyze_text_tool(focus="分析'微光如露落雪'在原文中的场景和情绪，给出符合语境的改写建议")
"""

                plan_prompt = f"""AI写作助手。{history_section}{knowledge_section}{selected_text_section}
用户: {message}
work_id: {work_id}
chapter_id: {chapter_id}

{static_prompt}{chapter_planning_hint}"""

                try:
                    # 2025-12-15: P0修复 - 添加重试机制，解决 AI 响应为空问题
                    max_planning_retries = 2
                    plan_text = ""
                    plan_data = None

                    for retry_attempt in range(max_planning_retries):
                        plan_result = await self._generate_text(
                            prompt=plan_prompt,  # ✅ 修复：使用关键字参数
                            temperature=0.3 + (retry_attempt * 0.1),  # 重试时稍微提高温度
                            max_tokens=2000,  # ✅ 2025-12-14: 增加到2000，防止复杂场景JSON被截断
                            task_type=TaskType.SIMPLE_QA  # ← Planning阶段用轻量模型快速生成任务列表
                        )
                        plan_text = plan_result.get("text", "").strip()

                        # 检查是否有有效内容
                        if plan_text:
                            # 解析规划JSON
                            plan_data = self._extract_json_from_text(plan_text)
                            if plan_data and plan_data.get("tasks"):
                                # 成功获取有效规划，退出重试循环
                                if retry_attempt > 0:
                                    logger.info(f"[Planning] 第{retry_attempt + 1}次重试成功")
                                break
                            else:
                                logger.warning(f"[Planning] 第{retry_attempt + 1}次尝试: JSON解析失败或无任务")
                        else:
                            logger.warning(f"[Planning] 第{retry_attempt + 1}次尝试: AI返回空响应")

                        # 如果还有重试机会，等待一小段时间
                        if retry_attempt < max_planning_retries - 1:
                            await asyncio.sleep(1)

                    # ✅ 2025-12-07: 记录 thinking 字段用于调试
                    if plan_data and "thinking" in plan_data:
                        thinking = plan_data["thinking"]
                        logger.info(
                            f"[Planning] 思维链: "
                            f"输出={thinking.get('step1_output', '?')[:30]}, "
                            f"原料={thinking.get('step2_material', '?')[:20]}, "
                            f"处理={thinking.get('step3_process', '?')[:20]}"
                        )

                except Exception as e:
                    logger.error(f"[Planning Agent] 执行失败: {e}", exc_info=True)

                    # 定义网络相关异常类型
                    network_related_errors = (
                    httpx.ConnectTimeout,
                    httpx.ReadTimeout,
                    httpx.NetworkError,
                    httpx.HTTPError,
                    ConnectionError,
                    TimeoutError,
                    # 移除过于宽泛的 OSError，只保留特定的网络错误
                    )

                    # 检查是否是网络相关错误
                    is_network_error = (
                    isinstance(e, network_related_errors) or
                    any(keyword in str(e).lower() for keyword in ["网络", "连接", "超时", "timeout", "connection", "network"])
                    )

                    if is_network_error:
                        logger.warning(f"[Planning] 检测到网络错误，使用简化规划流程")
                        # 使用简化的规划，避免再次调用AI
                        plan_data = {
                        "user_intent": "执行用户请求",
                        "tasks": [
                            {
                                "task_id": 1,
                                "description": "直接执行用户请求",
                                "tool": "get_context_tool",
                                "estimated_time": "5秒"
                            }
                        ]
                        }
                    else:
                        # 其他错误，返回错误响应
                        return {
                        "response": f"抱歉，规划阶段出现问题：{str(e)}。请稍后重试。",
                        "conversation_id": conversation_id or "default",
                        "agent_steps": [],
                        "suggested_actions": [],
                        "metadata": {"error": str(e), "stage": "planning", "error_type": type(e).__name__}
                        }

                if not plan_data:
                    logger.warning(f"[Planning] 无法解析规划JSON，AI返回: {plan_text[:500]}")

                if not plan_data or "tasks" not in plan_data:
                    # 默认规划 - 当 AI 规划失败时的兜底方案
                    # 🔧 2025-12-14: 修复 tool:"auto" 无效问题，改用 analyze_text_tool
                    plan_data = {
                        "user_intent": "执行用户请求",
                        "tasks": [
                            {
                                "task_id": 1,
                                "description": "理解用户意图并获取相关上下文",
                                "tool": "get_context_tool",
                                "estimated_time": "5秒"
                            },
                            {
                                "task_id": 2,
                                "description": "基于上下文响应用户请求",
                                "tool": "analyze_text_tool",
                                "params": {
                                    "text": "$TASK_1$",
                                    "focus": "根据用户请求进行分析或回答"
                                },
                                "estimated_time": "10秒"
                            }
                        ]
                    }

                # === 规划后处理：补充验收与 checkpoint，降低兜底反思频率 ===
                def _quick_acceptance_from_text(text: str):
                    """快速提取验收标准

                    🔧 2025-12-13: 致命BUG修复 - 正则表达式从\d{1,3}改为\d{1,5}
                    原正则只匹配1-3位数字，导致"2000字"被错误匹配为"000字"
                    """
                    import re
                    # 🔧 修复: \d{1,3} → \d{1,5} 支持最大99999的数字
                    m = re.search(r"(\d{1,5})\s*(个|条|点|段|篇|章节|章|转折点|要点|场景|角色|人物|种|类|组|步|项|处|部分|方面|建议|方案|问题|观点|字)", text or "")
                    if m:
                        return {"expected_count": int(m.group(1)), "requirement": m.group(0)}
                    return None

                acceptance_hint = _quick_acceptance_from_text(plan_data.get("user_intent") or message)
                tasks = plan_data.get("tasks") or []
                for idx, t in enumerate(tasks):
                    if acceptance_hint and not t.get("acceptance"):
                        t["acceptance"] = acceptance_hint
                    # 保证至少首个任务打 checkpoint，便于早期反思校验
                    if "checkpoint" not in t:
                        t["checkpoint"] = (idx == 0)
                plan_data["tasks"] = tasks

                # ✅ P1-7: 记录Planning阶段完成
                planning_duration = time.time() - planning_start

                logger.info(f"[Planning] 规划生成成功，共{len(plan_data['tasks'])}个任务，耗时: {planning_duration:.2f}s")
                increment_counter("planning_phase_completed")
                record_timer("planning_phase_duration", planning_duration)

                # 回调：发送规划
                if on_plan:
                    await on_plan(plan_data)

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

                # 使用新的并行执行方法
                # ✅ 为任务执行添加超时保护（使用统一配置）
                try:
                    async with async_timeout(TimeoutConfig.TASK_EXECUTION):
                        # ════════════════════════════════════════════
                        # DeepAgent 反思模式分支
                        # ════════════════════════════════════════════
                        if enable_reflection:
                            logger.info("[DeepAgent] 启用反思模式")
                            deep_executor = DeepAgentExecutor(
                                agent_graph=self,
                                on_plan=on_plan,
                                on_task_start=on_task_start,
                                on_task_progress=on_task_progress,
                                on_task_done=on_task_done,
                                on_content=on_content,
                            )

                            # ✅ 创建参数解析器（与 Plan 模式保持一致）
                            from app.services.agent.parameter_resolver import ParameterResolver
                            deep_resolver = ParameterResolver(strict_mode=False)
                            logger.info("[DeepAgent] ParameterResolver 已启用")

                            # 定义任务执行函数（传递给 DeepAgentExecutor）
                            async def execute_single_task(task, context, on_task_progress):
                                import time as time_module  # ✅ 添加计时支持
                                start_time = time_module.time()

                                # ✅ 解析任务参数中的占位符（修复 $TASK_N.content$ 未解析问题）
                                resolved_task = task.copy()
                                task_id = task.get("task_id", 0)
                                if "params" in resolved_task:
                                    resolved_task["params"] = await deep_resolver.resolve_params(
                                        resolved_task["params"],
                                        current_task_id=task_id
                                    )
                                    logger.debug(f"[DeepAgent] 任务{task_id}参数已解析")

                                result_str = await self._execute_task(
                                    task=resolved_task,  # ✅ 使用解析后的任务
                                    work_id=work_id,
                                    chapter_id=chapter_id,
                                    context=context.get("context_str", initial_context),
                                    on_progress=on_task_progress,
                                )

                                # ✅ 注册任务结果到参数解析器（供后续任务使用）
                                await deep_resolver.register_result(task_id, result_str)
                                logger.debug(f"[DeepAgent] 任务{task_id}结果已注册")

                                # ✅ 计算耗时（与 Plan 模式保持一致）
                                elapsed_time = time_module.time() - start_time

                                return {"status": "completed", "content": result_str, "elapsed_time": elapsed_time}

                            deep_result = await deep_executor.execute_with_reflection(
                                plan=plan_data,
                                context={"context_str": initial_context, "work_id": work_id, "chapter_id": chapter_id},
                                execute_task_func=execute_single_task,
                            )

                            # 如果发生重规划，使用最新的任务列表覆盖原规划，确保后续返回/缓存一致
                            if deep_result.get("replan_count", 0) > 0:
                                plan_data["tasks"] = deep_result.get("tasks", plan_data.get("tasks", []))

                            # 转换结果格式
                            task_results = []
                            # ✅ 构建任务ID到任务的映射（用于获取 tool 字段）
                            task_map = {t.get("task_id", i+1): t for i, t in enumerate(deep_result.get("tasks", []))}
                            for task_id, result in deep_result.get("results", {}).items():
                                task_info = task_map.get(task_id, {})
                                task_results.append({
                                    "task_id": task_id,
                                    "result": result.get("content", result.get("result", str(result))),
                                    "status": result.get("status", "completed"),
                                    "tool": task_info.get("tool", ""),  # ✅ 添加 tool 字段，用于任务分类
                                    "description": task_info.get("description", ""),  # ✅ 添加描述
                                    "elapsed_time": result.get("elapsed_time", 0),  # ✅ 添加耗时字段
                                })

                            logger.info(
                                f"[DeepAgent] 执行完成: 反思={deep_result.get('reflection_count', 0)}次, "
                                f"重规划={deep_result.get('replan_count', 0)}次"
                            )
                        else:
                            # 标准模式：使用原有并行执行
                            task_results = await self._execute_tasks_in_parallel(
                                tasks=plan_data["tasks"],
                                work_id=work_id,
                                chapter_id=chapter_id,
                                context=initial_context,
                                on_task_start=on_task_start,
                                on_task_progress=on_task_progress,
                                on_task_done=on_task_done
                            )
                        # ════════════════════════════════════════════
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

                # 使用新的智能判断方法
                # ✅ 传递 response_hint 用于元数据查询的精准返回
                final_content = await self._build_final_response(
                    task_results=task_results,
                    message=message,
                    on_content=on_content,
                    response_hint=plan_data.get("response_hint"),
                    knowledge_docs=knowledge_docs_for_response  # ✅ P0修复: 传递知识库文档
                )

                # ========== 保存对话到 ContextManager ==========
                try:
                    await self.context_manager.update_context(
                        session_id=isolated_thread_id,
                        new_messages=[
                            {"role": "user", "content": message},
                            {"role": "assistant", "content": final_content}
                        ],
                        context=context_bundle.get("context") if context_bundle else None,
                        work_id=work_id
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
            logger.error(f"[Planning] 总体超时（{elapsed:.1f}秒，限制360秒）")
            increment_counter("chat_with_planning_error", labels={"error_type": "TimeoutError"})

            return {
                "response": f"抱歉，请求处理超时（超过6分钟）。您的请求可能过于复杂，建议：\n1. 简化请求内容\n2. 分步骤进行操作\n3. 稍后重试",
                "conversation_id": conversation_id or "default",
                "agent_steps": [],
                "suggested_actions": ["简化请求", "分步操作", "稍后重试"],
                "metadata": {
                    "error": "Overall timeout",
                    "timeout_seconds": 360,
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
        on_task_start: Optional[callable] = None,
        on_task_progress: Optional[callable] = None,
        on_task_done: Optional[callable] = None
    ) -> List[Dict[str, Any]]:
        """智能并行执行任务

        Args:
            tasks: 任务列表
            work_id: 作品ID
            chapter_id: 章节ID
            context: 上下文
            on_task_start: 任务开始回调
            on_task_progress: 任务进度回调
            on_task_done: 任务完成回调

        Returns:
            任务结果列表
        """
        # ✅ 创建参数解析器
        from app.services.agent.parameter_resolver import ParameterResolver

        resolver = ParameterResolver(strict_mode=False)  # 使用非严格模式，兼容性更好
        logger.info("[ParameterResolver] 参数解析器已启用")

        # ✅ 【修复-问题3】辅助函数：检查参数中是否包含占位符
        def _has_placeholder_dependency(params: Dict[str, Any]) -> bool:
            """检查参数中是否包含占位符（表示依赖其他任务）"""
            import json
            try:
                params_str = json.dumps(params, ensure_ascii=False)
                return bool(ParameterResolver.PLACEHOLDER_PATTERN.search(params_str))
            except Exception as e:
                logger.warning(f"[参数依赖检测] 序列化参数失败: {e}")
                return False  # 序列化失败，保守处理：假设无依赖

        # 定义可以并行执行的独立数据获取工具
        # ✅ P1-2修复: 添加 analyze_text_tool，当分析不同章节时可以并行
        # 注意: 参数依赖检测(_has_placeholder_dependency)会确保有依赖的任务仍然串行
        PARALLEL_SAFE_TOOLS = {
            "get_context_tool",
            "read_chapter_tool",
            "get_chapter_by_order_tool",
            "search_analysis_fragments_tool",
            "analyze_text_tool"  # ✅ 允许并行（无参数依赖时）
        }

        # ✅ 改进：三层分组策略
        # 第一层：完全独立的任务（可立即并行）
        # 第二层：只依赖第一层任务的分析任务（第一层完成后可并行）
        # 第三层：有复杂依赖链的任务（必须串行）
        parallel_tasks = []
        parallel_dependent_tasks = []  # 新增：第二层并行任务
        sequential_tasks = []

        # 收集第一层任务的 ID
        first_layer_ids = set()

        # 第一遍：识别第一层任务
        for task in tasks:
            tool_name = task.get("tool", "auto")
            has_dependency = _has_placeholder_dependency(task.get("params", {}))

            if tool_name in PARALLEL_SAFE_TOOLS and not has_dependency:
                parallel_tasks.append(task)
                first_layer_ids.add(task["task_id"])
                logger.debug(f"[任务分组] 任务{task['task_id']}({tool_name}) → 第一层并行")

        # 第二遍：识别第二层任务（只依赖第一层的分析任务）
        for task in tasks:
            if task in parallel_tasks:
                continue

            tool_name = task.get("tool", "auto")
            params = task.get("params", {})
            has_dependency = _has_placeholder_dependency(params)

            if has_dependency:
                # 检查是否只依赖第一层任务
                deps = self._extract_task_dependencies(params)
                only_depends_on_first_layer = all(
                    dep_id in first_layer_ids for dep_id in deps
                )

                # 如果是分析工具且只依赖第一层，可以在第一层完成后并行
                if only_depends_on_first_layer and tool_name in {"analyze_text_tool", "summarization"}:
                    parallel_dependent_tasks.append(task)
                    logger.debug(f"[任务分组] 任务{task['task_id']}({tool_name}) → 第二层并行")
                else:
                    sequential_tasks.append(task)
                    logger.debug(f"[任务分组] 任务{task['task_id']}({tool_name}) → 串行（复杂依赖）")
            else:
                # 无依赖但工具不支持并行
                sequential_tasks.append(task)
                logger.debug(f"[任务分组] 任务{task['task_id']}({tool_name}) → 串行（工具不支持）")

        logger.info(
            f"[ParallelExecution] 任务分组: "
            f"第一层并行={len(parallel_tasks)}, "
            f"第二层并行={len(parallel_dependent_tasks)}, "
            f"串行={len(sequential_tasks)}"
        )

        task_results = []
        all_context = context

        # ✅ 在所有批次之前定义 semaphore（避免作用域问题）
        semaphore = asyncio.Semaphore(5)

        # 第1批：并行执行独立的数据获取任务
        if parallel_tasks:
            logger.info(f"[ParallelExecution] 开始并行执行{len(parallel_tasks)}个任务")

            async def execute_with_semaphore(task):
                async with semaphore:
                    import time
                    start_time = time.time()  # ✅ P1-1修复: 记录开始时间

                    task_id = task["task_id"]
                    description = task["description"]
                    tool_name = task.get("tool", "unknown")  # 获取工具名称

                    logger.info(f"[ParallelExecution] 并行任务{task_id}开始: {description}")

                    if on_task_start:
                        await on_task_start(task)

                    # ✅ P1-5: 添加重试机制（最多3次尝试）
                    max_retries = 2
                    last_error = None

                    for retry_count in range(max_retries + 1):
                        try:
                            # ✅ 解析任务参数中的占位符
                            resolved_task = task.copy()
                            if "params" in resolved_task:
                                resolved_task["params"] = await resolver.resolve_params(
                                    resolved_task["params"],
                                    current_task_id=task_id
                                )
                                logger.debug(
                                    f"[ParameterResolver] 任务{task_id}参数已解析: "
                                    f"{resolved_task['params']}"
                                )

                            result = await self._execute_task(
                                task=resolved_task,  # ✅ 使用解析后的任务
                                work_id=work_id,
                                chapter_id=chapter_id,
                                context=all_context,
                                on_progress=on_task_progress
                            )

                            logger.info(f"[ParallelExecution] 并行任务{task_id}完成" + (f"（重试{retry_count}次后成功）" if retry_count > 0 else ""))

                            # ✅ 注册任务结果到参数解析器
                            await resolver.register_result(task_id, result)
                            logger.debug(f"[ParameterResolver] 任务{task_id}结果已注册")

                            # ✅ P1-1修复: 计算耗时
                            elapsed_time = time.time() - start_time
                            task_with_time = {**task, "elapsed_time": elapsed_time}

                            if on_task_done:
                                await on_task_done(task_with_time, result)

                            return {
                                "task_id": task_id,
                                "description": description,
                                "tool": tool_name,
                                "result": result,
                                "status": "completed",
                                "elapsed_time": elapsed_time  # ✅ P1-1修复: 添加耗时字段
                            }

                        except Exception as e:
                            last_error = e

                            # 判断是否为可重试的错误（网络相关）
                            is_retryable = any(keyword in str(e).lower() for keyword in [
                                "timeout", "connection", "network", "网络", "连接", "超时"
                            ])

                            if is_retryable and retry_count < max_retries:
                                wait_time = 2 ** (retry_count + 1)  # 指数退避：2, 4, 8秒
                                logger.warning(f"[ParallelExecution] 任务{task_id}失败（{e}），{wait_time}秒后重试（{retry_count + 1}/{max_retries}）")
                                await asyncio.sleep(wait_time)
                            else:
                                # 不可重试或已达最大次数
                                logger.error(f"[ParallelExecution] 并行任务{task_id}最终失败: {last_error}")

                                # ✅ 【修复-问题2】注册失败结果到参数解析器
                                error_result = f"错误: {str(last_error)}"
                                await resolver.register_result(task_id, error_result)
                                logger.debug(f"[ParameterResolver] 任务{task_id}失败结果已注册")

                                return {
                                    "task_id": task_id,
                                    "description": description,
                                    "tool": tool_name,
                                    "result": error_result,
                                    "status": "failed"
                                }

                    # 如果所有重试都失败
                    # ✅ 【修复-问题2】注册重试失败结果到参数解析器
                    error_result = f"错误: {str(last_error)}（已重试{max_retries}次）"
                    await resolver.register_result(task_id, error_result)
                    logger.debug(f"[ParameterResolver] 任务{task_id}重试失败结果已注册")

                    return {
                        "task_id": task_id,
                        "description": description,
                        "tool": tool_name,
                        "result": error_result,
                        "status": "failed"
                    }

            # 并行执行所有独立任务
            # ✅ P0-4: 修复 return_exceptions=True，避免一个任务失败导致所有任务取消
            parallel_results = await asyncio.gather(
                *[execute_with_semaphore(task) for task in parallel_tasks],
                return_exceptions=True
            )

            # ✅ P0-4: 处理可能的异常结果（因为 return_exceptions=True）
            for i, result in enumerate(parallel_results):
                if isinstance(result, Exception):
                    # 异常结果 - 创建失败的任务记录
                    logger.error(f"[ParallelExecution] 并行任务失败: {result}")
                    failed_task = {
                        "task_id": parallel_tasks[i]["task_id"] if i < len(parallel_tasks) else "unknown",
                        "result": f"任务执行失败: {str(result)}",
                        "status": "failed",
                        "error": str(result)
                    }
                    task_results.append(failed_task)
                    all_context += f"\n任务{failed_task['task_id']}失败：{str(result)}\n"
                else:
                    # 正常结果
                    # 注意：任务结果已在execute_with_semaphore内部注册到resolver
                    task_results.append(result)
                    all_context += f"\n任务{result['task_id']}结果：\n{result['result']}\n"

        # 第2批：并行执行只依赖第一层的分析任务（新增）
        if parallel_dependent_tasks:
            logger.info(f"[ParallelExecution] 开始第二层并行执行{len(parallel_dependent_tasks)}个分析任务")

            async def execute_dependent_task(task):
                async with semaphore:
                    import time
                    start_time = time.time()

                    task_id = task["task_id"]
                    description = task["description"]
                    tool_name = task.get("tool", "unknown")

                    logger.info(f"[ParallelExecution] 第二层并行任务{task_id}开始: {description}")

                    if on_task_start:
                        await on_task_start(task)

                    max_retries = 2
                    last_error = None

                    for retry_count in range(max_retries + 1):
                        try:
                            resolved_task = task.copy()
                            if "params" in resolved_task:
                                resolved_task["params"] = await resolver.resolve_params(
                                    resolved_task["params"],
                                    current_task_id=task_id
                                )

                            result = await self._execute_task(
                                task=resolved_task,
                                work_id=work_id,
                                chapter_id=chapter_id,
                                context=all_context,
                                on_progress=on_task_progress
                            )

                            elapsed = time.time() - start_time
                            if on_task_done:
                                await on_task_done({
                                    **task,
                                    "elapsed_time": elapsed
                                }, result)

                            logger.info(f"[ParallelExecution] 第二层并行任务{task_id}完成")

                            await resolver.register_result(task_id, result)  # ✅ 添加 await
                            return {
                                "task_id": task_id,
                                "tool": tool_name,  # ✅ 添加 tool 字段
                                "description": description,
                                "result": result,
                                "status": "success"
                            }

                        except Exception as e:
                            last_error = e
                            if retry_count < max_retries:
                                logger.warning(f"[ParallelExecution] 第二层任务{task_id}失败，重试...")
                                await asyncio.sleep(1)
                            else:
                                logger.error(f"[ParallelExecution] 第二层任务{task_id}最终失败: {e}")

                    elapsed = time.time() - start_time
                    error_result = f"任务失败: {str(last_error)}"
                    if on_task_done:
                        await on_task_done({**task, "elapsed_time": elapsed}, error_result)

                    return {
                        "task_id": task_id,
                        "tool": tool_name,  # ✅ 添加 tool 字段
                        "description": description,
                        "result": error_result,
                        "status": "failed"
                    }

            # 并行执行第二层任务
            dependent_results = await asyncio.gather(
                *[execute_dependent_task(task) for task in parallel_dependent_tasks],
                return_exceptions=True
            )

            for i, result in enumerate(dependent_results):
                if isinstance(result, Exception):
                    task = parallel_dependent_tasks[i]
                    failed_task = {
                        "task_id": task["task_id"],
                        "tool": task.get("tool", "unknown"),  # ✅ 添加 tool 字段
                        "description": task.get("description", ""),
                        "result": f"任务执行失败: {str(result)}",
                        "status": "failed"
                    }
                    task_results.append(failed_task)
                    all_context += f"\n任务{failed_task['task_id']}失败：{str(result)}\n"
                else:
                    task_results.append(result)
                    all_context += f"\n任务{result['task_id']}结果：\n{result['result']}\n"

        # 第3批：串行执行有复杂依赖的任务
        if sequential_tasks:
            logger.info(f"[ParallelExecution] 开始串行执行{len(sequential_tasks)}个任务")

            for task in sequential_tasks:
                import time
                start_time = time.time()  # ✅ P1-1修复: 记录开始时间

                task_id = task["task_id"]
                description = task["description"]
                tool_name = task.get("tool", "unknown")  # 获取工具名称

                logger.info(f"[ParallelExecution] 串行任务{task_id}开始: {description}")

                if on_task_start:
                    await on_task_start(task)

                # ✅ P1-5: 为串行任务也添加重试机制
                max_retries = 2
                last_error = None
                task_succeeded = False

                for retry_count in range(max_retries + 1):
                    try:
                        # ✅ 解析任务参数中的占位符
                        resolved_task = task.copy()
                        if "params" in resolved_task:
                            resolved_task["params"] = await resolver.resolve_params(
                                resolved_task["params"],
                                current_task_id=task_id
                            )
                            logger.debug(
                                f"[ParameterResolver] 任务{task_id}参数已解析: "
                                f"{resolved_task['params']}"
                            )

                        result = await self._execute_task(
                            task=resolved_task,  # ✅ 使用解析后的任务
                            work_id=work_id,
                            chapter_id=chapter_id,
                            context=all_context,
                            on_progress=on_task_progress
                        )

                        # ✅ 注册任务结果到参数解析器
                        await resolver.register_result(task_id, result)
                        logger.debug(f"[ParameterResolver] 任务{task_id}结果已注册")

                        # ✅ P1-1修复: 计算耗时
                        elapsed_time = time.time() - start_time

                        task_results.append({
                            "task_id": task_id,
                            "description": description,
                            "tool": tool_name,
                            "result": result,
                            "status": "completed",
                            "elapsed_time": elapsed_time  # ✅ P1-1修复: 添加耗时字段
                        })

                        all_context += f"\n任务{task_id}结果：\n{result}\n"

                        logger.info(f"[ParallelExecution] 串行任务{task_id}完成" + (f"（重试{retry_count}次后成功）" if retry_count > 0 else ""))

                        # ✅ P1-1修复: 传递带耗时的task
                        task_with_time = {**task, "elapsed_time": elapsed_time}
                        if on_task_done:
                            await on_task_done(task_with_time, result)

                        task_succeeded = True
                        break  # 成功，退出重试循环

                    except Exception as e:
                        last_error = e

                        # 判断是否为可重试的错误（网络相关）
                        is_retryable = any(keyword in str(e).lower() for keyword in [
                            "timeout", "connection", "network", "网络", "连接", "超时"
                        ])

                        if is_retryable and retry_count < max_retries:
                            wait_time = 2 ** (retry_count + 1)
                            logger.warning(f"[ParallelExecution] 串行任务{task_id}失败（{e}），{wait_time}秒后重试（{retry_count + 1}/{max_retries}）")
                            await asyncio.sleep(wait_time)
                        else:
                            # 不可重试或已达最大次数
                            break

                # 如果所有重试都失败
                if not task_succeeded:
                    logger.error(f"[ParallelExecution] 串行任务{task_id}最终失败: {last_error}")

                    # ✅ 【修复-问题2】注册失败结果到参数解析器
                    error_result = f"错误: {str(last_error)}"
                    await resolver.register_result(task_id, error_result)
                    logger.debug(f"[ParameterResolver] 任务{task_id}失败结果已注册")

                    task_results.append({
                        "task_id": task_id,
                        "description": description,
                        "tool": tool_name,
                        "result": error_result,
                        "status": "failed"
                    })

        # 按task_id排序，保持原始顺序
        task_results.sort(key=lambda x: x["task_id"])

        return task_results

    def _classify_tasks(self, task_results: List[Dict]) -> Dict[str, List]:
        """分类任务：输入型 vs 输出型 vs 展示型

        Args:
            task_results: 任务结果列表

        Returns:
            分类后的任务字典，包含 input_tasks, output_tasks, display_tasks
        """
        # 定义输入型工具（只是获取数据，不产生最终输出）
        INPUT_TOOLS = {
            "get_context_tool",
            "search_analysis_fragments_tool"
        }

        # ✅ P2-1修复: 定义展示型工具（用户只想查看数据，可直接格式化返回）
        DISPLAY_TOOLS = {
            "get_chapter_by_order_tool",  # 获取章节内容
            "read_chapter_tool"            # 读取章节
        }

        # 定义输出型工具（产生用户需要的最终内容）
        OUTPUT_TOOLS = {
            "continue_writing_tool",   # 续写
            "analyze_text_tool"        # 分析
        }

        input_tasks = []
        output_tasks = []
        display_tasks = []  # ✅ P2-1修复: 新增展示型任务

        for task in task_results:
            tool = task.get("tool", "")
            if tool in DISPLAY_TOOLS:
                display_tasks.append(task)
            elif tool in INPUT_TOOLS:
                input_tasks.append(task)
            elif tool in OUTPUT_TOOLS:
                output_tasks.append(task)
            else:
                # 未分类的工具，保守起见归为输出型
                output_tasks.append(task)

        logger.info(
            f"[TaskClassify] 任务分类: 输入型={len(input_tasks)}, "
            f"输出型={len(output_tasks)}, 展示型={len(display_tasks)}"
        )

        return {
            "input_tasks": input_tasks,
            "output_tasks": output_tasks,
            "display_tasks": display_tasks  # ✅ P2-1修复: 返回展示型任务
        }

    async def _build_final_response(
        self,
        task_results: List[Dict],
        message: str,
        on_content: Optional[callable] = None,
        response_hint: Optional[str] = None,
        knowledge_docs: Optional[List[Dict]] = None  # ✅ P0修复: 添加知识库文档参数
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
            logger.warning("[Response] 没有明确输出任务，使用AI整合")
            return await self._ai_summarization(task_results, message, on_content, knowledge_docs)

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
                return await self._ai_summarization(task_results, message, on_content, knowledge_docs)

            # 创作类任务，且输出充分 → 直接返回
            if tool_name in ["continue_writing_tool"]:
                if len(result) > 500:
                    logger.info(
                        f"[Response] 单个创作任务({tool_name})，"
                        f"输出{len(result)}字符，直接返回（跳过AI调用）"
                    )

                    # ✅ 方案B修复：真流式输出，直接发送整个内容
                    # 由于内容已经生成完毕，直接一次性发送比分块发送更快
                    if on_content:
                        await on_content(result)

                    return result

            # 分析类任务，可能需要格式化
            logger.info(f"[Response] 单个分析任务({tool_name})，使用AI格式化")
            return await self._ai_summarization(task_results, message, on_content, knowledge_docs)

        # 情况3：多个输出任务（约15%）
        else:
            # ✅ 方案B修复：使用@知识库时，走AI整合路径（真流式）
            if knowledge_docs:
                logger.info(
                    f"[Response] 检测到知识库文档({len(knowledge_docs)}个)，"
                    f"{len(output_tasks)}个输出任务，使用AI整合（确保流式输出）"
                )
                return await self._ai_summarization(task_results, message, on_content, knowledge_docs)

            # ✅ 方案B优化：检查是否全是分析/摘要类任务
            analysis_like_tools = {"analyze_text_tool", "summarization", "analyze_content"}
            all_analyze = all(
                task.get("tool") in analysis_like_tools
                for task in output_tasks
            )
            has_writing = any(
                task.get("tool") == "continue_writing_tool"
                for task in output_tasks
            )

            # 多个分析/摘要任务 → AI整合（避免冗余拼接）
            if all_analyze and not has_writing:
                logger.info(f"[Response] {len(output_tasks)}个分析类任务，使用AI整合（避免冗余）")
                return await self._ai_summarization(task_results, message, on_content, knowledge_docs)

            # 包含续写任务 → 简单拼接（保持创作内容完整）
            logger.info(f"[Response] {len(output_tasks)}个输出任务，简单拼接")

            parts = []
            for task in output_tasks:
                tool_name = task.get("tool", "unknown")  # ✅ 安全访问
                result = task.get("result", "") or ""  # 处理None的情况

                # 添加标题
                if tool_name == "analyze_text_tool":
                    parts.append(f"## 分析结果\n\n{result}")
                elif tool_name == "continue_writing_tool":
                    parts.append(f"## 续写内容\n\n{result}")
                else:
                    parts.append(result)

            final_content = "\n\n".join(parts)

            # ✅ 方案B修复：直接发送整个内容（比分块发送更快）
            if on_content:
                await on_content(final_content)

            return final_content

    async def _format_display_response(
        self,
        display_tasks: List[Dict],
        response_hint: Optional[str] = None,
        on_content: Optional[callable] = None
    ) -> str:
        """
        ✅ P2-1修复: 格式化展示型任务的响应

        当用户只是查看数据（如查看章节内容）时，直接格式化返回，
        不需要调用AI进行整合，节省成本。

        Args:
            display_tasks: 展示型任务列表
            response_hint: Planning 阶段提供的响应提示（如 "title", "word_count", "content"）
            on_content: 内容回调函数

        Returns:
            格式化后的响应内容
        """
        response_parts = []

        for task in display_tasks:
            description = task.get("description", "")
            result = task.get("result", "")

            # 尝试解析JSON格式的结果
            try:
                result_json = json.loads(result)

                # 提取章节信息
                if isinstance(result_json, dict):
                    # ✅ 先检查是否是错误响应
                    if "error" in result_json:
                        error_msg = result_json.get("error", "未知错误")
                        total_chapters = result_json.get("total_chapters")
                        if total_chapters:
                            response_parts.append(f"❌ {error_msg}（该作品共有 {total_chapters} 章）")
                        else:
                            response_parts.append(f"❌ {error_msg}")
                        continue

                    title = result_json.get("title", "")
                    content = result_json.get("content", "")
                    word_count = result_json.get("word_count", 0)
                    # ✅ 修复: 工具返回的是 "order" 字段，不是 "chapter_order"
                    chapter_order = result_json.get("order") or result_json.get("chapter_order", "")

                    # ✅ 根据 response_hint 智能返回（由 Planning 阶段提供）
                    # 如果 Planning 没有返回 hint，尝试从 task description 推断
                    effective_hint = response_hint
                    if not effective_hint:
                        desc_lower = description.lower()
                        if "标题" in desc_lower or "题目" in desc_lower or "章名" in desc_lower:
                            effective_hint = "title"
                        elif "字数" in desc_lower or "多少字" in desc_lower:
                            effective_hint = "word_count"

                    if effective_hint == "title":
                        response_parts.append(f"第{chapter_order}章的标题是：**{title}**")
                    elif effective_hint == "word_count":
                        response_parts.append(f"第{chapter_order}章《{title}》共 **{word_count}** 字")
                    elif effective_hint == "title_and_word_count":
                        response_parts.append(f"第{chapter_order}章《**{title}**》，共 **{word_count}** 字")
                    elif title and content:
                        # 默认：返回标题+内容
                        chapter_header = f"**第{chapter_order}章: {title}**" if chapter_order else f"**{title}**"
                        # 截取内容摘要（避免响应过长）
                        content_preview = content[:1500] + "..." if len(content) > 1500 else content
                        response_parts.append(f"{chapter_header}\n\n{content_preview}")
                    else:
                        response_parts.append(result)
                else:
                    response_parts.append(result)

            except (json.JSONDecodeError, TypeError):
                # 非JSON格式，直接使用
                response_parts.append(result)

        # 组合响应
        final_response = "\n\n---\n\n".join(response_parts)

        # ✅ 方案B修复：直接发送整个内容（比分块发送更快）
        if on_content and final_response:
            await on_content(final_response)

        return final_response

    async def _ai_summarization(
        self,
        task_results: List[Dict],
        message: str,
        on_content: Optional[callable] = None,
        knowledge_docs: Optional[List[Dict]] = None  # ✅ P0修复: 添加知识库文档参数
    ) -> str:
        """AI整合（保留原有的Summarization逻辑）

        Args:
            task_results: 任务结果列表
            message: 用户原始消息
            on_content: 内容回调函数
            knowledge_docs: 用户引用的知识库文档列表（可选）

        Returns:
            AI整合后的最终响应
        """
        from app.services.agent.utils.monitoring import increment_counter

        logger.info("[Summarization] 使用AI整合任务结果")

        # ✅ P0修复: 构建知识库文档上下文
        knowledge_section = ""
        if knowledge_docs:
            logger.info(f"[Summarization] 注入 {len(knowledge_docs)} 个知识库文档到总结prompt")
            knowledge_parts = []
            for doc in knowledge_docs[:3]:  # 最多3个文档
                title = doc.get("title") or "未命名文档"
                tags = doc.get("tags") or []
                source = doc.get("source_type") or "unknown"
                content = doc.get("content") or ""
                # 截取摘要，避免prompt过长
                snippet = content.strip()[:1200] if content else ""
                if snippet:
                    # ✅ P0修复: 更明确地标注文档元数据，避免AI混淆
                    tags_str = ', '.join(tags) if tags else '无'
                    knowledge_parts.append(
                        f"=== 知识库文档 ===\n"
                        f"文档标题: {title}\n"
                        f"文档来源: {source}\n"
                        f"文档标签: {tags_str}\n"
                        f"文档正文内容:\n{snippet}\n"
                        f"=== 文档结束 ==="
                    )
            if knowledge_parts:
                knowledge_section = "\n\n【用户引用的知识库文档】\n请优先参考以下文档内容回答用户问题：\n\n" + "\n\n".join(knowledge_parts) + "\n\n"

        # 构建完整上下文
        all_context = f"用户请求：{message}\n\n"
        for result in task_results:
            all_context += f"\n任务{result['task_id']}结果：\n{result['result']}\n"

        # 上下文压缩
        compressed_context = _build_summarization_context(
            user_message=message,
            task_results=task_results,
            max_context_length=6000  # 减少到6000字符，提高响应速度，避免超时
        )

        logger.info(
            f"[Summarization] 上下文处理: "
            f"原始={len(all_context)}字符, "
            f"处理后={len(compressed_context)}字符"
        )

        # ✅ P0修复: 将知识库文档注入到总结prompt中
        summary_prompt = f"""基于以下任务执行结果，生成最终的响应给用户。
{knowledge_section}
{compressed_context}

⚠️ 重要规则（必须遵守）：
1. 【数据忠实性】必须使用工具返回的真实数据，禁止编造或猜测！
   - 章节标题 = 工具返回的 title 字段值
   - 章节内容 = 工具返回的 content 字段值
   - 章节序号 = 工具返回的 order 字段值
2. 综合所有任务结果，用清晰、友好的语言呈现
3. 如果是创作内容，直接输出创作结果
4. 如果是分析/规划，给出详细说明
5. 如果用户询问事实性问题（如标题、内容等），直接引用工具返回的数据
6. 如果用户引用了知识库文档，优先基于文档内容回答

请生成最终响应："""

        # ✅ 使用流式生成，实现真正的同步流式输出
        logger.info("[Summarization] 使用流式生成（_generate_text_stream）")

        # 定义流式回调：直接将每个 chunk 传递给 on_content
        async def stream_callback(chunk: str):
            if on_content and chunk:
                await on_content(chunk)

        # 调用流式生成方法（内部已有超时和异常处理）
        result = await self._generate_text_stream(
            prompt=summary_prompt,
            on_chunk=stream_callback,
            max_tokens=2000,
            temperature=0.7,
            task_type=TaskType.SUMMARIZATION,
            buffer_size=1  # ✅ 逐字输出：每1个字符发送一次
        )

        # 检查是否有错误
        if "error" in result and not result.get("partial"):
            error_msg = result.get('error', '')
            logger.warning(f"[Summarization] _generate_text_stream 失败: {error_msg}")
            increment_counter("ai_summarization_error", labels={"error_type": error_msg[:50] if error_msg else 'unknown'})

            # 检测积分不足错误，显示友好提示
            if "积分" in error_msg and ("不足" in error_msg or "余额" in error_msg):
                fallback_content = "积分余额不足，请先充值后再使用此功能。"
                if on_content:
                    await on_content(fallback_content)
                return fallback_content

            # 返回简单的任务结果拼接作为 fallback
            fallback_content = "抱歉，AI整合失败。以下是任务结果摘要：\n\n"
            for task_result in task_results:
                fallback_content += f"- 任务{task_result['task_id']}: {task_result.get('description', 'N/A')}\n"
                if task_result.get('status') == 'completed':
                    result_text = str(task_result.get('result', ''))[:200]
                    fallback_content += f"  结果: {result_text}...\n"
            # 发送 fallback 内容
            if on_content:
                await on_content(fallback_content)
            return fallback_content

        # 如果是部分内容（超时但有内容），记录日志
        if result.get("partial"):
            logger.warning(f"[Summarization] 流式生成超时，返回部分内容（{len(result.get('text', ''))}字符）")

        final_content = result.get("text", "")
        # 注意：内容已通过 stream_callback 流式发送，这里不再重复发送

        return final_content

    def _resolve_version_reference(self, reference: str, versions: Dict[str, str]) -> Optional[str]:
        """智能解析版本引用，支持多种表达方式

        Args:
            reference: 用户的版本引用表达（如"第二版"、"版本B"、"$VERSION_B$"、"2"等）
            versions: 版本内容字典 {"version_a": "...", "version_b": "...", "version_c": "..."}

        Returns:
            匹配到的版本内容，如果没有匹配返回None
        """
        if not reference or not versions:
            return None

        ref = reference.lower().strip()

        # 版本A的各种表达方式
        version_a_patterns = [
            "版本a", "version_a", "version a", "$version_a$",
            "第一版", "第1版", "一版", "1版", "a版", "a",
            "第一个", "第1个", "1", "一"
        ]

        # 版本B的各种表达方式
        version_b_patterns = [
            "版本b", "version_b", "version b", "$version_b$",
            "第二版", "第2版", "二版", "2版", "b版", "b",
            "第二个", "第2个", "2", "二"
        ]

        # 版本C的各种表达方式
        version_c_patterns = [
            "版本c", "version_c", "version c", "$version_c$",
            "第三版", "第3版", "三版", "3版", "c版", "c",
            "第三个", "第3个", "3", "三"
        ]

        # 检查是否匹配版本A
        if any(p in ref or ref == p for p in version_a_patterns):
            content = versions.get("version_a", "")
            if content:
                return content

        # 检查是否匹配版本B
        if any(p in ref or ref == p for p in version_b_patterns):
            content = versions.get("version_b", "")
            if content:
                return content

        # 检查是否匹配版本C
        if any(p in ref or ref == p for p in version_c_patterns):
            content = versions.get("version_c", "")
            if content:
                return content

        # 如果reference本身就是版本内容（长度>50），直接返回
        if len(reference) > 50:
            return reference

        logger.warning(f"[LangGraph] 无法解析版本引用: '{reference}'")
        return None

    def _normalize_tool_params(self, tool_name: str, params: Dict[str, Any]) -> Dict[str, Any]:
        """标准化工具参数，将不符合格式的参数转换为正确格式

        Args:
            tool_name: 工具名称
            params: 原始参数

        Returns:
            标准化后的参数
        """
        import json

        normalized = params.copy()

        # continue_writing_tool 的 requirements 必须是字符串
        if tool_name == "continue_writing_tool":
            requirements = params.get("requirements", "")
            if isinstance(requirements, dict):
                # 将字典转换为可读的字符串
                parts = []
                for key, value in requirements.items():
                    parts.append(f"{key}: {value}")
                normalized["requirements"] = "，".join(parts)
                logger.info(f"[参数标准化] continue_writing_tool.requirements: dict → str")

        # 🔧 2025-12-14: analyze_content → analyze_text 参数转换
        # analyze_content 使用 content 参数，analyze_text 使用 text 参数
        elif tool_name in ("analyze_content", "analyze_content_tool", "analyze_text_tool", "analyze_text"):
            # 如果有 content 但没有 text，转换参数名
            if "content" in params and "text" not in params:
                normalized["text"] = params["content"]
                del normalized["content"]
                logger.info(f"[参数标准化] {tool_name}.content → text")
            if "text" in normalized and not isinstance(normalized["text"], str):
                normalized["text"] = str(normalized["text"])
                logger.info(f"[参数标准化] {tool_name}.text: {type(params.get('text', params.get('content'))).__name__} → str")
            if "focus" in params and not isinstance(params["focus"], str):
                normalized["focus"] = str(params["focus"])

        return normalized

    async def _execute_task(
        self,
        task: Dict[str, Any],
        work_id: str,
        chapter_id: str,
        context: str,
        on_progress: Optional[callable] = None
    ) -> str:
        """执行单个任务（DeepAgent 模式使用）

        🔧 2025-12-14: 统一使用 registry.call_tool() 调用 StandardTool
        """
        tool_name = task.get("tool", "analyze_text")  # 🔧 2025-12-14: 默认改为 analyze_text
        # 🔧 2025-12-14: 处理 auto 工具名
        if tool_name == "auto":
            tool_name = "analyze_text"
        task_type = task.get("type", "")  # ✅ 新增：检测任务类型
        params = task.get("params", {})

        # 标准化参数格式
        params = self._normalize_tool_params(tool_name, params)

        if on_progress:
            await on_progress(task, "正在执行...")

        # 🔧 2025-12-14: 统一使用 registry 调用所有工具
        try:
            # 工具名称映射
            # 🔧 2025-12-14: 添加 analyze_content → analyze_text 映射，避免 AI 混淆
            TOOL_NAME_MAPPING = {
                "continue_writing_tool": "continue_writing",
                "analyze_text_tool": "analyze_text",
                "analyze_content_tool": "analyze_text",  # 🔧 兼容：统一使用 analyze_text
                "analyze_content": "analyze_text",       # 🔧 兼容：统一使用 analyze_text
                "get_context_tool": "get_context",
                "read_chapter_tool": "read_chapter",
                "get_chapter_by_order_tool": "get_chapter_by_order",
                "search_analysis_fragments_tool": "search_analysis_fragments",
            }

            normalized_name = TOOL_NAME_MAPPING.get(tool_name, tool_name)

            # 准备工具参数（DeepAgent 特有逻辑）
            if tool_name == "get_chapter_by_order_tool":
                tool_params = {
                    "work_id": work_id,
                    "chapter_order": params.get("chapter_order", 1)
                }
            elif tool_name == "get_context_tool":
                tool_params = {
                    "work_id": work_id,
                    "chapter_id": chapter_id or ""
                }
            elif tool_name == "read_chapter_tool":
                if "chapter_id" not in params or not params["chapter_id"]:
                    logger.warning(
                        f"[_execute_task] read_chapter_tool 缺少 chapter_id 参数，"
                        f"将使用当前章节ID: {chapter_id}。"
                        f"任务描述: {task.get('description', 'N/A')}"
                    )
                tool_params = {
                    "work_id": work_id,
                    "chapter_id": params.get("chapter_id") or chapter_id or ""
                }
            elif tool_name == "search_analysis_fragments_tool":
                if not work_id:
                    logger.warning(
                        f"[_execute_task] search_analysis_fragments_tool 需要 work_id 参数，"
                        f"但当前 work_id 为空。任务描述: {task.get('description', 'N/A')}"
                    )
                    return json.dumps({
                        "error": "需要指定作品ID才能检索分析片段",
                        "message": "请在聊天时指定作品ID，或在作品详情页使用此功能",
                        "tool": "search_analysis_fragments_tool"
                    }, ensure_ascii=False, indent=2)
                tool_params = {
                    "work_id": work_id,
                    "query": params.get("query", "相关内容"),
                    "top_k": params.get("top_k", 5),
                    "chapter_id": chapter_id or "",
                    "include_current": params.get("include_current", True),
                    "look_ahead": params.get("look_ahead", 2),
                }
            elif tool_name == "continue_writing_tool":
                # ✅ 2025-12-17: 优先使用选中文本作为续写上下文
                context_param = params.get("context", "").strip()
                if not context_param or "$TASK_" in context_param:
                    selected_text_extracted = None
                    if "用户选中的文本：" in context:
                        match = re.search(r'用户选中的文本：\n---\n(.*?)\n---', context, re.DOTALL)
                        if match:
                            selected_text_extracted = match.group(1).strip()

                    # 使用较低阈值(5字符)，避免忽略有效的短文本如"优化这句"
                    if selected_text_extracted and len(selected_text_extracted) >= 5:
                        logger.info(f"[_execute_task] continue_writing_tool 优先使用选中文本（{len(selected_text_extracted)}字符）")
                        context_param = selected_text_extracted
                    else:
                        context_param = context

                tool_params = {
                    "context": context_param,
                    "requirements": params.get("requirements", ""),
                    "target_length": params.get("target_length", 500),
                    "style": params.get("style", "")
                }
            elif tool_name == "analyze_text_tool":
                # 🔧 2025-12-14: 防御性编程 - 使用 context 兜底
                text_param = params.get("text", "").strip()

                # 处理空值和占位符 - 优先使用选中文本
                if not text_param or "$TASK_" in text_param:
                    # ✅ 2025-12-17: 优先从 context 提取选中文本，避免使用被任务结果污染的整个 context
                    selected_text_extracted = None
                    if "用户选中的文本：" in context:
                        match = re.search(r'用户选中的文本：\n---\n(.*?)\n---', context, re.DOTALL)
                        if match:
                            selected_text_extracted = match.group(1).strip()

                    # 使用较低阈值(5字符)，避免忽略有效的短文本如"优化这句"
                    if selected_text_extracted and len(selected_text_extracted) >= 5:
                        logger.info(f"[_execute_task] analyze_text_tool 优先使用选中文本（{len(selected_text_extracted)}字符）")
                        text_param = selected_text_extracted
                    else:
                        logger.info(f"[_execute_task] analyze_text_tool 的 text 参数为空或含占位符，使用 context 兜底（{len(context)}字符）")
                        text_param = context[:50000]  # 限制长度以符合 max_length=50000

                # 🔧 2025-12-14: focus 参数支持任意字符串
                # 模板 analyze_text.yaml 会根据 focus 内容决定输出模式：
                # - focus="all" 或包含"全面/完整" → 详细模式（完整报告）
                # - 其他任意字符串 → 简洁模式（200-500字聚焦分析）
                focus_param = params.get("focus", "all")

                # 只对空值或占位符做兜底，其他情况保留原始 focus
                if not focus_param or "$TASK_" in str(focus_param):
                    focus_param = "all"
                    logger.info(f"[_execute_task] analyze_text_tool 的 focus 参数为空/占位符，使用默认值 'all'")
                else:
                    logger.info(f"[_execute_task] analyze_text_tool 使用 focus: '{str(focus_param)[:80]}...'")

                tool_params = {
                    "text": text_param,
                    "focus": focus_param  # ✅ 支持任意 focus 字符串触发简洁模式
                }
            else:
                # 未知工具，尝试使用统一接口
                logger.info(f"[_execute_task] 使用统一接口调用未知工具: {tool_name}")
                result = await self._call_tool_via_registry(
                    tool_name=tool_name,
                    tool_args=params,
                    state={"work_id": work_id, "chapter_id": chapter_id, "last_user_message": context}
                )
                if on_progress:
                    await on_progress(task, "完成")
                return result

            # 调用 StandardTool
            logger.info(f"[_execute_task] 调用 registry.call_tool({normalized_name})")
            result_data = await registry.call_tool(normalized_name, tool_params)

            # 提取结果
            if isinstance(result_data, dict) and result_data.get("success"):
                result = self._extract_tool_result(normalized_name, result_data)
                logger.info(f"[StandardTool] {normalized_name} 执行成功（DeepAgent模式）")
            else:
                error_msg = result_data.get("message", "执行失败") if isinstance(result_data, dict) else "未知错误"
                result = json.dumps({"error": "tool_failed", "message": error_msg}, ensure_ascii=False)
                logger.error(f"[StandardTool] {normalized_name} 执行失败（DeepAgent模式）: {error_msg}")

        except ValueError as e:
            # 🔧 2025-12-14: 改进错误分类，区分验证错误和工具不存在
            error_msg = str(e)

            if "validation error" in error_msg.lower():
                # Pydantic 参数验证失败
                logger.error(f"[_execute_task] {tool_name} 参数验证失败: {error_msg}")
                logger.error(f"[_execute_task] 传入的参数: {tool_params}")
            else:
                # StandardTool 不存在
                logger.warning(f"[_execute_task] StandardTool '{tool_name}' 不存在，降级到 @tool: {e}")

            # 无论如何都降级
            result = await self._fallback_legacy_execute(tool_name, params, work_id, chapter_id, context)

        except Exception as e:
            # 其他异常，也尝试降级
            logger.error(f"[_execute_task] StandardTool 调用失败: {tool_name}, 错误: {e}")
            result = await self._fallback_legacy_execute(tool_name, params, work_id, chapter_id, context)

        if on_progress:
            await on_progress(task, "完成")

        return result

    async def _fallback_legacy_execute(
        self,
        tool_name: str,
        params: dict,
        work_id: str,
        chapter_id: str,
        context: str
    ) -> str:
        """DeepAgent 模式的降级执行（使用 @tool）"""
        # 根据工具名称调用对应工具
        if tool_name == "get_chapter_by_order_tool":
            return await get_chapter_by_order_tool.ainvoke({
                "work_id": work_id,
                "chapter_order": params.get("chapter_order", 1)
            })
        elif tool_name == "get_context_tool":
            return await get_context_tool.ainvoke({
                "work_id": work_id,
                "chapter_id": chapter_id or ""
            })
        elif tool_name == "read_chapter_tool":
            return await read_chapter_tool.ainvoke({
                "work_id": work_id,
                "chapter_id": params.get("chapter_id") or chapter_id or ""
            })
        elif tool_name == "search_analysis_fragments_tool":
            return await search_analysis_fragments_tool.ainvoke({
                "work_id": work_id,
                "query": params.get("query", "相关内容"),
                "top_k": params.get("top_k", 5),
                "chapter_id": chapter_id or "",
                "include_current": params.get("include_current", True),
                "look_ahead": params.get("look_ahead", 2),
            })
        elif tool_name == "continue_writing_tool":
            return await continue_writing_tool.ainvoke({
                "context": params.get("context", context),
                "requirements": params.get("requirements", "")
            })
        elif tool_name == "analyze_text_tool":
            return await analyze_text_tool.ainvoke({
                "text": params.get("text", ""),
                "focus": params.get("focus", "all")
            })
        else:
            # 自动选择工具
            return f"任务 {tool_name} 需要手动处理"


# ==================== 导出 ====================

__all__ = ["WritingAgentGraph", "AgentState"]
 
