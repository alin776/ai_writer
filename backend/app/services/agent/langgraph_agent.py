"""
LangGraph Agent 工作流实现

使用 LangGraph 框架实现智能写作助手，支持：
- 4个核心场景（写作/规划/分析/卡文）
- 工具调用（HTTPAIService集成）
- 记忆管理（Checkpointer）
- 人机协同（HITL）
"""

from typing import TypedDict, Annotated, List, Dict, Any, Optional, Literal
from datetime import datetime
from langgraph.graph import StateGraph, END
from langgraph.prebuilt import ToolNode
from langgraph.checkpoint.memory import MemorySaver
from langchain_core.messages import HumanMessage, AIMessage, SystemMessage, ToolMessage
from langchain_core.tools import tool
from langchain_openai import ChatOpenAI
import operator
import logging

from app.services.ai.http_ai_service import HTTPAIService
from app.core.config import settings
from app.services.agent.prompts import NovelPhase, PhaseCharacteristics
from app.services.agent.prompt_library import get_content_prompt

logger = logging.getLogger(__name__)


# ==================== State 定义 ====================

class AgentState(TypedDict):
    """Agent 状态定义"""
    messages: Annotated[List[Any], operator.add]  # 对话历史
    work_id: Optional[str]  # 作品ID
    chapter_id: Optional[str]  # 章节ID
    intent: Optional[str]  # 用户意图
    context: Dict[str, Any]  # 上下文信息
    agent_steps: List[Dict[str, Any]]  # Agent执行步骤
    suggested_actions: List[str]  # 建议操作
    final_response: Optional[str]  # 最终响应


# ==================== 工具定义 ====================

# 全局 AI Service 实例（用于工具调用）
_global_ai_service: Optional[HTTPAIService] = None

def set_global_ai_service(ai_service: HTTPAIService):
    """设置全局 AI Service"""
    global _global_ai_service
    _global_ai_service = ai_service


async def _retry_on_failure(func, *args, max_retries=3, **kwargs):
    """通用重试包装器：用于数据库操作等可能失败的操作

    Args:
        func: 要执行的异步函数
        max_retries: 最大重试次数
        *args, **kwargs: 传递给func的参数

    Returns:
        函数执行结果
    """
    import asyncio
    retry_count = 0

    while retry_count < max_retries:
        try:
            result = await func(*args, **kwargs)
            return result
        except Exception as e:
            retry_count += 1
            logger.error(f"[Retry] {func.__name__} 失败 (尝试 {retry_count}/{max_retries}): {e}")

            if retry_count >= max_retries:
                raise  # 重试次数用尽，抛出异常

            # 指数退避
            await asyncio.sleep(2 ** retry_count)

    raise Exception(f"{func.__name__} 失败，已重试{max_retries}次")


async def _generate_text_helper(prompt: str, temperature: float = 0.7, max_tokens: int = 1000) -> str:
    """辅助函数：使用 HTTPAIService 生成文本（带重试机制）"""
    if not _global_ai_service:
        return "错误：AI服务未初始化"

    messages = [{"role": "user", "content": prompt}]
    generated_text = ""
    max_retries = 3
    retry_count = 0

    while retry_count < max_retries:
        try:
            async for chunk, _ in _global_ai_service._stream_chat(
                messages=messages,
                max_tokens=max_tokens,
                temperature=temperature
            ):
                if chunk:
                    generated_text += chunk

            # 成功生成内容，退出循环
            if generated_text:
                return generated_text

            # 如果没有生成内容，重试
            retry_count += 1
            logger.warning(f"[_generate_text_helper] 生成文本为空，重试 {retry_count}/{max_retries}")

        except Exception as e:
            retry_count += 1
            logger.error(f"[_generate_text_helper] 生成失败 (尝试 {retry_count}/{max_retries}): {e}")

            if retry_count >= max_retries:
                return f"错误：AI服务调用失败，已重试{max_retries}次。错误信息：{str(e)}"

            # 等待后重试（指数退避）
            import asyncio
            await asyncio.sleep(2 ** retry_count)

    return generated_text or "错误：生成内容为空"


@tool
async def continue_writing_tool(context: str, requirements: str = "") -> str:
    """续写工具：根据上下文续写内容

    Args:
        context: 已有的文本上下文
        requirements: 续写要求（可选）

    Returns:
        续写后的文本
    """
    prompt = f"""你是专业的小说续写助手。请直接续写小说内容，不要给建议或提问！

上下文：
{context}

续写要求：{requirements if requirements else '保持原有风格，情节自然连贯，字数500-800字'}

重要：请直接输出续写的小说正文，不要输出任何说明文字、建议或问题。立即开始续写："""

    return await _generate_text_helper(prompt, temperature=0.8, max_tokens=2000)


@tool
async def polish_text_tool(text: str, style: str = "professional") -> str:
    """润色工具：优化文本质量

    Args:
        text: 待润色的文本
        style: 润色风格（professional/creative/concise）

    Returns:
        润色后的文本
    """
    prompt = f"""请润色以下文本，风格：{style}

原文：
{text}

请提供润色后的版本："""

    return await _generate_text_helper(prompt, temperature=0.7, max_tokens=2000)


@tool
async def analyze_text_tool(text: str, focus: str = "all") -> str:
    """分析工具：分析文本问题

    Args:
        text: 待分析的文本
        focus: 分析重点（all/grammar/logic/style）

    Returns:
        分析报告
    """
    prompt = f"""请分析以下文本，重点关注：{focus}

文本：
{text}

请提供详细的分析报告："""

    return await _generate_text_helper(prompt, temperature=0.3, max_tokens=1500)


@tool
async def read_chapter_tool(work_id: str, chapter_id: str) -> str:
    """读取指定章节工具：从数据库读取章节内容

    Args:
        work_id: 作品ID
        chapter_id: 章节ID

    Returns:
        章节信息（包含标题和内容）
    """
    try:
        from app.core.database import AsyncSessionLocal
        from app.services.chapter_service import ChapterService
        import json

        # 创建数据库会话
        async with AsyncSessionLocal() as db:
            chapter_service = ChapterService(db)

            # 查询章节
            chapter = await chapter_service.get_chapter_by_id(chapter_id)

            if not chapter:
                return json.dumps({
                    "error": f"未找到章节 {chapter_id}",
                    "work_id": work_id
                }, ensure_ascii=False, indent=2)

            # 返回章节信息
            chapter_info = {
                "chapter_id": str(chapter.id),
                "title": chapter.title,
                "order": chapter.order,
                "content": chapter.content[:2000] if chapter.content else "",  # 限制长度避免token溢出
                "content_length": len(chapter.content) if chapter.content else 0,
                "word_count": chapter.word_count,
                "status": chapter.status.value if hasattr(chapter, 'status') else "unknown"
            }

            logger.info(f"[read_chapter_tool] 读取章节成功: {chapter.title}")
            return json.dumps(chapter_info, ensure_ascii=False, indent=2)

    except Exception as e:
        logger.error(f"[read_chapter_tool] 读取章节失败: {e}", exc_info=True)
        return json.dumps({
            "error": f"读取章节失败: {str(e)}",
            "work_id": work_id,
            "chapter_id": chapter_id
        }, ensure_ascii=False, indent=2)


@tool
async def get_chapter_by_order_tool(work_id: str, chapter_order: int) -> str:
    """通过章节序号获取章节ID和内容

    Args:
        work_id: 作品ID
        chapter_order: 章节序号（第1章=1，第2章=2，...）

    Returns:
        章节信息（包含ID、标题和内容）
    """
    try:
        from app.core.database import AsyncSessionLocal
        from app.services.work_service import WorkService
        import json

        async with AsyncSessionLocal() as db:
            work_service = WorkService(db)

            # 获取作品及其章节
            work = await work_service.get_work_by_id(work_id, use_cache=False)

            if not work or not work.chapters:
                return json.dumps({
                    "error": f"未找到作品或作品没有章节",
                    "work_id": work_id
                }, ensure_ascii=False, indent=2)

            # 查找对应序号的章节
            target_chapter = None
            for chapter in work.chapters:
                if chapter.order == chapter_order:
                    target_chapter = chapter
                    break

            if not target_chapter:
                return json.dumps({
                    "error": f"未找到第{chapter_order}章",
                    "work_id": work_id,
                    "total_chapters": len(work.chapters)
                }, ensure_ascii=False, indent=2)

            # 返回章节信息
            chapter_info = {
                "chapter_id": str(target_chapter.id),
                "title": target_chapter.title,
                "order": target_chapter.order,
                "content": target_chapter.content[:2000] if target_chapter.content else "",
                "content_length": len(target_chapter.content) if target_chapter.content else 0,
                "word_count": target_chapter.word_count,
                "status": target_chapter.status.value if hasattr(target_chapter, 'status') else "unknown"
            }

            logger.info(f"[get_chapter_by_order_tool] 找到第{chapter_order}章: {target_chapter.title}")
            return json.dumps(chapter_info, ensure_ascii=False, indent=2)

    except Exception as e:
        logger.error(f"[get_chapter_by_order_tool] 查询失败: {e}", exc_info=True)
        return json.dumps({
            "error": f"查询失败: {str(e)}",
            "work_id": work_id,
            "chapter_order": chapter_order
        }, ensure_ascii=False, indent=2)


@tool
async def search_analysis_fragments_tool(work_id: str, query: str, top_k: int = 5) -> str:
    """检索分析碎片工具：从向量数据库检索相关的小说分析片段（RAG）

    Args:
        work_id: 作品ID
        query: 查询文本（用户的问题或需求）
        top_k: 返回前K个最相关结果（默认5个）

    Returns:
        相关的分析片段列表（JSON格式）
    """
    try:
        from app.core.database import AsyncSessionLocal
        from app.services.vector_store_service import VectorStoreService
        import json

        # 创建数据库会话
        async with AsyncSessionLocal() as db:
            vector_service = VectorStoreService(db)

            # RAG检索
            results = await vector_service.retrieve_relevant_analysis(
                work_id=work_id,
                query=query,
                top_k=top_k,
                similarity_threshold=0.3  # 降低阈值以获取更多结果
            )

            if not results:
                return json.dumps({
                    "message": "未找到相关的分析片段",
                    "work_id": work_id,
                    "query": query,
                    "results": []
                }, ensure_ascii=False, indent=2)

            # 格式化结果
            formatted_results = []
            for i, result in enumerate(results):
                formatted_results.append({
                    "rank": i + 1,
                    "similarity": result['similarity'],
                    "chapter_id": result['chapter_id'],
                    "content": result['content_text'][:500],  # 限制长度
                    "micro_data_summary": {
                        "theme": result['micro_data'].get('chapter_theme', 'N/A') if result['micro_data'] else 'N/A'
                    }
                })

            logger.info(f"[search_analysis_fragments_tool] RAG检索成功: 找到{len(results)}个相关片段")

            return json.dumps({
                "work_id": work_id,
                "query": query,
                "total_results": len(results),
                "results": formatted_results
            }, ensure_ascii=False, indent=2)

    except Exception as e:
        logger.error(f"[search_analysis_fragments_tool] RAG检索失败: {e}", exc_info=True)
        return json.dumps({
            "error": f"检索失败: {str(e)}",
            "work_id": work_id,
            "query": query
        }, ensure_ascii=False, indent=2)


@tool
async def get_context_tool(work_id: str, chapter_id: str = "") -> str:
    """获取上下文工具：检索作品、章节和世界观信息（真实数据）

    Args:
        work_id: 作品ID
        chapter_id: 章节ID（可选）

    Returns:
        上下文信息（JSON格式字符串）
    """
    try:
        from app.core.database import AsyncSessionLocal
        from app.services.work_service import WorkService
        from app.services.chapter_service import ChapterService
        from app.services.vector_store_service import VectorStoreService
        import json

        logger.info(f"[get_context_tool] 🔥 新版本工具被调用！work_id={work_id}, chapter_id={chapter_id}")

        # 创建数据库会话
        async with AsyncSessionLocal() as db:
            work_service = WorkService(db)
            chapter_service = ChapterService(db)
            vector_service = VectorStoreService(db)

            context_info = {
                "work_id": work_id,
                "work_info": {},
                "current_chapter": {},
                "related_analysis": []
            }

            # 1. 获取作品信息
            work = await work_service.get_work_by_id(work_id, use_cache=False)
            if work:
                context_info["work_info"] = {
                    "title": work.title,
                    "description": work.description[:200] if work.description else "",
                    "genre": work.genre if hasattr(work, 'genre') else "未知",
                    "total_chapters": len(work.chapters) if work.chapters else 0
                }
            else:
                context_info["work_info"] = {"error": "作品未找到"}

            # 2. 获取当前章节（如果提供了chapter_id）
            if chapter_id:
                chapter = await chapter_service.get_chapter_by_id(chapter_id)
                if chapter:
                    context_info["current_chapter"] = {
                        "chapter_id": str(chapter.id),
                        "title": chapter.title,
                        "order": chapter.order,
                        "content_preview": chapter.content[:500] if chapter.content else "",
                        "word_count": chapter.word_count
                    }
                else:
                    context_info["current_chapter"] = {"error": "章节未找到"}

            # 3. RAG检索相关分析（如果有）
            try:
                query = f"作品背景和设定"
                analysis_results = await vector_service.retrieve_relevant_analysis(
                    work_id=work_id,
                    query=query,
                    top_k=3,
                    similarity_threshold=0.4
                )

                if analysis_results:
                    context_info["related_analysis"] = [
                        {
                            "chapter_id": r['chapter_id'],
                            "similarity": r['similarity'],
                            "summary": r['content_text'][:200]
                        }
                        for r in analysis_results
                    ]
            except Exception as rag_error:
                logger.warning(f"RAG检索失败（非致命）: {rag_error}")
                context_info["related_analysis"] = []

            logger.info(f"[get_context_tool] 获取上下文成功: work={work.title if work else 'N/A'}")
            return json.dumps(context_info, ensure_ascii=False, indent=2)

    except Exception as e:
        logger.error(f"[get_context_tool] 获取上下文失败: {e}", exc_info=True)
        return json.dumps({
            "error": f"获取上下文失败: {str(e)}",
            "work_id": work_id
        }, ensure_ascii=False, indent=2)


# 工具列表
WRITING_TOOLS = [
    continue_writing_tool,
    polish_text_tool,
    analyze_text_tool,
    get_context_tool,
    read_chapter_tool,
    get_chapter_by_order_tool,  # 新增：通过章节序号获取章节
    search_analysis_fragments_tool
]


# ==================== Agent 节点定义 ====================

class WritingAgentGraph:
    """
    LangGraph 写作 Agent - 支持双模式

    模式 1 (use_chatgpt=True): 使用 ChatOpenAI + 原生工具调用
    模式 2 (use_chatgpt=False): 使用 HTTPAIService + 手动工具调用（绕过 Cloudflare）
    """

    def __init__(self, ai_service: HTTPAIService, use_chatgpt: bool = False):
        """
        初始化 Agent

        Args:
            ai_service: HTTPAIService 实例
            use_chatgpt: 是否使用 ChatOpenAI（True=原生工具调用，False=手动工具调用）
        """
        self.ai_service = ai_service
        self.use_chatgpt = use_chatgpt  # 模式开关

        # 设置全局 AI Service（供工具使用）
        set_global_ai_service(ai_service)

        # 根据模式初始化
        if use_chatgpt:
            logger.info("[LangGraph] 使用 ChatOpenAI 模式（原生工具调用）")
            self._init_chatgpt_mode()
        else:
            logger.info("[LangGraph] 使用 HTTPAIService 模式（手动工具调用，绕过 Cloudflare）")
            self.llm = None
            self.llm_with_tools = None

        # 创建 Checkpointer（记忆系统）
        self.checkpointer = MemorySaver()

        # 构建图
        self.graph = self._build_graph()

    def _init_chatgpt_mode(self):
        """初始化 ChatOpenAI 模式"""
        import httpx

        # 创建自定义 httpx 客户端（尝试绕过 Cloudflare）
        sync_http_client = httpx.Client(
            headers={
                "User-Agent": "okhttp/4.12.0",
                "Accept": "application/json",
                "Accept-Encoding": "gzip, deflate",
                "Connection": "keep-alive",
            },
            timeout=httpx.Timeout(120.0, connect=10.0),
            follow_redirects=True,
            http2=False,
        )

        async_http_client = httpx.AsyncClient(
            headers={
                "User-Agent": "okhttp/4.12.0",
                "Accept": "application/json",
                "Accept-Encoding": "gzip, deflate",
                "Connection": "keep-alive",
            },
            timeout=httpx.Timeout(120.0, connect=10.0),
            follow_redirects=True,
            http2=False,
        )

        # 创建 LLM
        self.llm = ChatOpenAI(
            model=settings.OPENAI_MODEL,
            api_key=settings.OPENAI_API_KEY,
            base_url=settings.OPENAI_BASE_URL,
            temperature=0.7,
            http_client=sync_http_client,
            http_async_client=async_http_client
        )

        # 绑定工具
        self.llm_with_tools = self.llm.bind_tools(WRITING_TOOLS)

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

        # 创建图
        workflow = StateGraph(AgentState)

        # 添加节点
        workflow.add_node("intent_classifier", self._classify_intent)
        workflow.add_node("writing_agent", self._handle_writing)
        workflow.add_node("planning_agent", self._handle_planning)
        workflow.add_node("analysis_agent", self._handle_analysis)
        workflow.add_node("stuck_agent", self._handle_stuck)
        workflow.add_node("general_chat", self._handle_general)
        workflow.add_node("tools", ToolNode(WRITING_TOOLS))

        # 设置入口点
        workflow.set_entry_point("intent_classifier")

        # 添加条件边：根据意图路由到不同Agent
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

    async def _generate_text(self, prompt: str, temperature: float = 0.7, max_tokens: int = 1000) -> dict:
        """使用 HTTPAIService 生成文本的辅助方法"""
        messages = [{"role": "user", "content": prompt}]

        generated_text = ""
        usage = None

        async for chunk, chunk_usage in self.ai_service._stream_chat(
            messages=messages,
            max_tokens=max_tokens,
            temperature=temperature
        ):
            if chunk:
                generated_text += chunk
            if chunk_usage:
                usage = chunk_usage

        return {
            "text": generated_text,
            "usage": usage or {}
        }

    async def _classify_intent(self, state: AgentState) -> AgentState:
        """意图分类节点"""
        logger.info("[LangGraph] 意图分类")

        last_message = state["messages"][-1].content

        # 使用 LLM 分类意图
        prompt = f"""分析用户意图，返回以下之一：
- writing: 续写、扩写相关
- planning: 规划、大纲、世界观相关
- analysis: 分析、评估、诊断相关
- stuck: 卡文、灵感、方向相关
- general: 一般对话

用户消息：{last_message}

只返回意图类型，不要其他内容。"""

        result = await self._generate_text(prompt=prompt, temperature=0.3, max_tokens=50)
        intent = result.get("text", "general").strip().lower()

        state["intent"] = intent
        state["agent_steps"].append({
            "step": "intent_classification",
            "result": f"识别意图: {intent}",
            "usage": result.get("usage", {})
        })

        return state

    def _route_intent(self, state: AgentState) -> str:
        """路由决策函数"""
        intent = state.get("intent", "general")
        logger.info(f"[LangGraph] 路由到: {intent}")
        return intent

    async def _handle_agent_with_tools(self, state: AgentState, agent_type: str, system_prompt: str) -> AgentState:
        """
        通用的Agent处理逻辑 - 支持双模式

        模式 1: ChatOpenAI 原生工具调用
        模式 2: HTTPAIService 手动工具调用
        """
        logger.info(f"[LangGraph] 处理{agent_type}场景 (use_chatgpt={self.use_chatgpt})")

        if self.use_chatgpt:
            # 模式 1: 使用 ChatOpenAI 原生工具调用
            return await self._handle_with_chatgpt(state, agent_type, system_prompt)
        else:
            # 模式 2: 使用 HTTPAIService 手动工具调用
            return await self._handle_with_httpai(state, agent_type, system_prompt)

    async def _handle_with_chatgpt(self, state: AgentState, agent_type: str, system_prompt: str) -> AgentState:
        """ChatOpenAI 模式 - 原生工具调用"""
        messages = state["messages"]

        # 检查是否已经有工具结果（第二次进入）
        if messages and isinstance(messages[-1], ToolMessage):
            logger.info(f"[LangGraph] {agent_type} - 处理工具执行结果 (ChatOpenAI)")
            response = await self.llm.ainvoke(messages)
            state["messages"].append(response)
            state["final_response"] = response.content
            state["agent_steps"].append({
                "step": f"{agent_type}_final_response",
                "result": "基于工具结果生成最终响应 (ChatOpenAI)"
            })
            return state

        # 第一次进入：让 LLM 决定是否需要工具
        messages_with_system = [SystemMessage(content=system_prompt)] + messages
        response = await self.llm_with_tools.ainvoke(messages_with_system)

        state["messages"].append(response)
        state["agent_steps"].append({
            "step": f"{agent_type}_decision",
            "result": f"LLM决策 (ChatOpenAI): {'调用工具' if response.tool_calls else '直接响应'}",
            "tool_calls": len(response.tool_calls) if response.tool_calls else 0
        })

        if not response.tool_calls:
            state["final_response"] = response.content

        return state

    async def _handle_with_httpai(self, state: AgentState, agent_type: str, system_prompt: str) -> AgentState:
        """HTTPAIService 模式 - 手动工具调用（绕过 Cloudflare）"""
        messages = state["messages"]

        # 检查是否已经有工具结果（第二次进入）
        if messages and isinstance(messages[-1], ToolMessage):
            logger.info(f"[LangGraph] {agent_type} - 处理工具执行结果 (HTTPAIService)")

            # 获取用户原始请求
            user_message = ""
            for msg in messages:
                if isinstance(msg, HumanMessage):
                    user_message = msg.content
                    break

            # 使用 HTTPAIService 基于工具结果生成最终响应
            tool_result = messages[-1].content

            logger.info(f"[LangGraph] 🔍 工具返回内容长度: {len(tool_result)} 字符")
            logger.info(f"[LangGraph] 🔍 工具返回内容预览:\n{tool_result[:500]}")

            # 判断用户意图：是想「查看/读取」内容，还是想「创作/续写」内容
            read_keywords = ["读", "看", "查看", "显示", "展示", "告诉我", "第几章", "内容是什么"]
            write_keywords = ["写", "续写", "创作", "生成", "继续", "扩写", "补充"]

            is_read_request = any(keyword in user_message for keyword in read_keywords)
            is_write_request = any(keyword in user_message for keyword in write_keywords)

            # 根据 agent_type 和用户实际意图定制响应方式
            if agent_type == "writing":
                # 如果用户明确想「读取/查看」内容
                if is_read_request and not is_write_request:
                    final_prompt = f"""{system_prompt}

用户请求：{user_message}

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
                    final_prompt = f"""{system_prompt}

用户请求：{user_message}

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
                final_prompt = f"""{system_prompt}

用户遇到的问题：{user_message}

当前创作背景：
{tool_result}

请基于背景信息，给用户3-5个具体的创作方向建议，每个建议包含：
1. 方向概述
2. 可以这样写的理由
3. 示例开头（50字左右）"""

            elif agent_type == "planning":
                final_prompt = f"""{system_prompt}

用户需求：{user_message}

当前信息：
{tool_result}

请基于现有信息，提供详细的规划方案。"""

            else:  # analysis 或其他
                # 如果用户明确想「读取/查看」内容
                if is_read_request and not is_write_request:
                    final_prompt = f"""{system_prompt}

用户请求：{user_message}

工具返回的数据：
{tool_result}

请注意：用户想要「查看/读取」内容！
请直接整理并呈现工具返回的数据内容，用清晰易读的格式展示给用户。"""
                else:
                    final_prompt = f"""{system_prompt}

用户请求：{user_message}

分析材料：
{tool_result}

请基于材料，生成详细的分析报告。"""

            final_text = ""
            async for chunk, _ in self.ai_service._stream_chat(
                messages=[{"role": "user", "content": final_prompt}],
                max_tokens=1500,
                temperature=0.7
            ):
                if chunk:
                    final_text += chunk

            response = AIMessage(content=final_text)
            state["messages"].append(response)
            state["final_response"] = final_text
            state["agent_steps"].append({
                "step": f"{agent_type}_final_response",
                "result": "基于工具结果生成最终响应 (HTTPAIService)"
            })
            return state

        # 第一次进入：使用 HTTPAIService 决定是否需要工具
        last_user_message = messages[-1].content

        decision_prompt = f"""{system_prompt}

用户消息：{last_user_message}

请判断是否需要调用工具来帮助用户。

如果需要工具，请返回 JSON 格式：
{{"need_tools": true, "tool_name": "工具名", "tool_args": {{"参数": "值"}}}}

如果不需要工具，请返回 JSON 格式：
{{"need_tools": false, "direct_response": "直接回复用户的内容"}}"""

        decision_text = ""
        async for chunk, _ in self.ai_service._stream_chat(
            messages=[{"role": "user", "content": decision_prompt}],
            max_tokens=500,
            temperature=0.3
        ):
            if chunk:
                decision_text += chunk

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

        # 方法 3: 如果都失败，返回默认决策
        if not decision:
            logger.error(f"[LangGraph] 无法解析决策，原文: {decision_text[:200]}")
            decision = {
                "need_tools": False,
                "direct_response": "抱歉，我在理解您的请求时遇到了问题。能否更详细地描述一下？"
            }

        logger.info(f"[LangGraph] 最终决策: {decision}")

        logger.info(f"[LangGraph] {agent_type} 决策 (HTTPAIService): {decision.get('need_tools', False)}")

        if decision.get("need_tools", False):
            # 需要工具：手动调用
            tool_name = decision.get("tool_name", "continue_writing_tool")
            tool_args = decision.get("tool_args", {})

            # 调用工具（使用 .ainvoke() 方法，因为 @tool 装饰器返回的是 StructuredTool 对象）
            tool_result = ""
            if tool_name == "continue_writing_tool":
                tool_result = await continue_writing_tool.ainvoke({
                    "context": tool_args.get("context", last_user_message),
                    "requirements": tool_args.get("requirements", "")
                })
            elif tool_name == "polish_text_tool":
                tool_result = await polish_text_tool.ainvoke({
                    "text": tool_args.get("text", last_user_message),
                    "style": tool_args.get("style", "professional")
                })
            elif tool_name == "analyze_text_tool":
                tool_result = await analyze_text_tool.ainvoke({
                    "text": tool_args.get("text", last_user_message),
                    "focus": tool_args.get("focus", "all")
                })
            elif tool_name == "get_context_tool":
                logger.info(f"[LangGraph] 🚀 准备调用 get_context_tool, work_id={state.get('work_id')}, chapter_id={state.get('chapter_id')}")
                tool_result = await get_context_tool.ainvoke({
                    "work_id": state.get("work_id", ""),
                    "chapter_id": state.get("chapter_id", "")
                })
                logger.info(f"[LangGraph] ✅ get_context_tool 返回结果长度: {len(tool_result)} 字符")
                logger.info(f"[LangGraph] ✅ get_context_tool 返回内容预览: {tool_result[:200]}")
            elif tool_name == "read_chapter_tool":
                tool_result = await read_chapter_tool.ainvoke({
                    "work_id": state.get("work_id", ""),
                    "chapter_id": tool_args.get("chapter_id", state.get("chapter_id", ""))
                })
            elif tool_name == "get_chapter_by_order_tool":
                logger.info(f"[LangGraph] 🚀 准备调用 get_chapter_by_order_tool, work_id={state.get('work_id')}, chapter_order={tool_args.get('chapter_order')}")
                tool_result = await get_chapter_by_order_tool.ainvoke({
                    "work_id": state.get("work_id", ""),
                    "chapter_order": tool_args.get("chapter_order", 1)
                })
                logger.info(f"[LangGraph] ✅ get_chapter_by_order_tool 返回结果长度: {len(tool_result)} 字符")
            elif tool_name == "search_analysis_fragments_tool":
                tool_result = await search_analysis_fragments_tool.ainvoke({
                    "work_id": state.get("work_id", ""),
                    "query": tool_args.get("query", last_user_message),
                    "top_k": tool_args.get("top_k", 5)
                })
            else:
                tool_result = f"未知工具: {tool_name}"
                logger.warning(f"[LangGraph] 尝试调用未知工具: {tool_name}")

            # 添加消息
            ai_decision = AIMessage(content=f"我需要使用 {tool_name} 工具来帮助你。")
            state["messages"].append(ai_decision)

            tool_message = ToolMessage(content=tool_result, tool_call_id="manual_call")
            state["messages"].append(tool_message)

            state["agent_steps"].append({
                "step": f"{agent_type}_tool_call",
                "result": f"调用工具 (HTTPAIService): {tool_name}",
                "tool_result_length": len(tool_result)
            })

            # 递归处理工具结果
            return await self._handle_with_httpai(state, agent_type, system_prompt)

        else:
            # 不需要工具：直接响应
            direct_response = decision.get("direct_response", "抱歉，我无法处理您的请求。")
            response = AIMessage(content=direct_response)
            state["messages"].append(response)
            state["final_response"] = direct_response
            state["agent_steps"].append({
                "step": f"{agent_type}_direct_response",
                "result": "直接响应用户 (HTTPAIService)"
            })

        return state

    async def _handle_writing(self, state: AgentState) -> AgentState:
        """处理写作场景 - 使用 Prompt 库优化"""
        work_id = state.get("work_id")
        chapter_id = state.get("chapter_id")
        context_info = state.get("context", {})

        # 尝试识别章节号,确定创作阶段
        phase = None
        chapter_num = None

        # 从用户消息中提取章节号
        last_message = state["messages"][-1].content if state["messages"] else ""
        import re
        chapter_match = re.search(r'第(\d+)章|chapter\s*(\d+)', last_message, re.IGNORECASE)
        if chapter_match:
            chapter_num = int(chapter_match.group(1) or chapter_match.group(2))
            phase = PhaseCharacteristics.get_phase_by_chapter(chapter_num)
            logger.info(f"[Writing] 识别到章节号: {chapter_num}, 阶段: {phase.value}")

        # 使用 Prompt 库生成系统 Prompt
        if phase:
            # 使用阶段 Prompt (包含爽感优化)
            base_system_prompt = get_content_prompt(
                phase=phase,
                scene_type=None,  # 可以根据需要添加场景识别
                context={
                    'current_chapter': chapter_num,
                    'total_chapters': 50  # 默认50章,可配置
                }
            )

            # 添加工具使用说明
            tools_instruction = f"""

---

【工具使用】
可用工具：
- get_context_tool: 获取作品/章节上下文（包含作品信息、章节内容、相关分析）
- read_chapter_tool: 读取指定章节的完整内容（需要chapter_id）
- get_chapter_by_order_tool: 通过章节序号获取章节（用户说"第X章"时用这个）
- search_analysis_fragments_tool: 从向量数据库检索相关的小说分析片段（RAG）
- continue_writing_tool: 续写内容
- polish_text_tool: 润色文本

当前信息：作品ID={work_id}, 当前页面章节ID={chapter_id}

【重要】章节处理流程：
1. 用户说"续写第X章"或"读第X章"时：
   - 先调用 get_chapter_by_order_tool 获取第X章的 chapter_id 和内容
   - 例如：用户说"续写第二章"，你应该调用 get_chapter_by_order_tool(chapter_order=2)

2. 用户说"续写"但没指定章节时：
   - 使用当前页面的 chapter_id 调用 read_chapter_tool

3. 续写要求：
   - 必须先读取章节的真实内容
   - 续写必须紧接章节结尾，不要重新开头
   - 保持原文的写作风格、人物性格、情节发展
   - 写网络小说故事，不是技术文档或编程内容
   - 可调用 search_analysis_fragments_tool 获取世界观、角色设定

根据用户需求，决定调用合适的工具。"""

            system_prompt = base_system_prompt + tools_instruction
        else:
            # 没有识别到章节,使用默认 Prompt
            system_prompt = f"""你是专业的网络小说写作助手Agent，专注于创作网文故事。

【重要】你的写作风格：
- 你是网文作家，不是程序员或技术文档作者
- 写作类型：玄幻、都市、言情、武侠、仙侠等网络小说
- 绝对禁止写编程、代码、技术相关的内容
- 必须写人物、情节、对话、情感、动作、场景描写
- 保持网文的节奏感和代入感

可用工具：
- get_context_tool: 获取作品/章节上下文（包含作品信息、章节内容、相关分析）
- read_chapter_tool: 读取指定章节的完整内容（需要chapter_id）
- get_chapter_by_order_tool: 通过章节序号获取章节（用户说"第X章"时用这个）
- search_analysis_fragments_tool: 从向量数据库检索相关的小说分析片段（RAG）
- continue_writing_tool: 续写内容
- polish_text_tool: 润色文本

当前信息：作品ID={work_id}, 当前页面章节ID={chapter_id}

【重要】章节处理流程：
1. 用户说"续写第X章"或"读第X章"时：
   - 先调用 get_chapter_by_order_tool 获取第X章的 chapter_id 和内容
   - 例如：用户说"续写第二章"，你应该调用 get_chapter_by_order_tool(chapter_order=2)

2. 用户说"续写"但没指定章节时：
   - 使用当前页面的 chapter_id 调用 read_chapter_tool

3. 续写要求：
   - 必须先读取章节的真实内容
   - 续写必须紧接章节结尾，不要重新开头
   - 保持原文的写作风格、人物性格、情节发展
   - 写网络小说故事，不是技术文档或编程内容
   - 可调用 search_analysis_fragments_tool 获取世界观、角色设定

根据用户需求，决定调用合适的工具。"""

        return await self._handle_agent_with_tools(state, "writing", system_prompt)

    async def _handle_planning(self, state: AgentState) -> AgentState:
        """处理规划场景"""
        system_prompt = """你是专业的规划助手Agent。

可用工具：
- get_context_tool: 获取作品信息
- read_chapter_tool: 读取已有章节内容
- search_analysis_fragments_tool: 检索相关分析片段（RAG）
- analyze_text_tool: 分析现有内容

帮助用户规划小说创作，包括世界观、角色、大纲等。根据需要调用工具。"""

        return await self._handle_agent_with_tools(state, "planning", system_prompt)

    async def _handle_analysis(self, state: AgentState) -> AgentState:
        """处理分析场景"""
        system_prompt = """你是专业的文本分析Agent。

可用工具：
- analyze_text_tool: 深度分析文本
- get_context_tool: 获取上下文信息
- read_chapter_tool: 读取章节内容
- search_analysis_fragments_tool: 检索历史分析片段（RAG）

帮助用户分析文本质量、逻辑、风格等。根据需要调用工具。"""

        return await self._handle_agent_with_tools(state, "analysis", system_prompt)

    async def _handle_stuck(self, state: AgentState) -> AgentState:
        """处理卡文场景"""
        system_prompt = """你是专业的写作指导Agent。

可用工具：
- get_context_tool: 获取当前创作背景
- read_chapter_tool: 读取已写章节
- search_analysis_fragments_tool: 检索相关创作灵感和分析（RAG）
- analyze_text_tool: 分析现有内容
- continue_writing_tool: 尝试续写方向

帮助卡文的用户突破瓶颈，提供多个创作方向建议。根据需要调用工具。"""

        return await self._handle_agent_with_tools(state, "stuck", system_prompt)

    async def _handle_general(self, state: AgentState) -> AgentState:
        """处理一般对话 - 使用 HTTPAIService"""
        logger.info("[LangGraph] 处理一般对话")

        messages = state["messages"]
        last_message = messages[-1].content
        system_prompt = "你是友好的AI写作助手，以专业、简洁的方式回复用户。"

        prompt = f"""{system_prompt}

用户消息：{last_message}

请回复："""

        response_text = ""
        async for chunk, _ in self.ai_service._stream_chat(
            messages=[{"role": "user", "content": prompt}],
            max_tokens=500,
            temperature=0.7
        ):
            if chunk:
                response_text += chunk

        response = AIMessage(content=response_text)
        state["messages"].append(response)
        state["final_response"] = response_text
        state["agent_steps"].append({
            "step": "general_chat",
            "result": "一般对话响应"
        })

        return state

    async def chat(
        self,
        message: str,
        work_id: Optional[str] = None,
        chapter_id: Optional[str] = None,
        conversation_id: Optional[str] = None,
        context: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        与 Agent 对话

        Args:
            message: 用户消息
            work_id: 作品ID
            chapter_id: 章节ID
            conversation_id: 会话ID（用于记忆）
            context: 额外上下文

        Returns:
            Dict: Agent响应
        """

        # 构建初始状态
        initial_state = {
            "messages": [HumanMessage(content=message)],
            "work_id": work_id,
            "chapter_id": chapter_id,
            "intent": None,
            "context": context or {},
            "agent_steps": [],
            "suggested_actions": [],
            "final_response": None
        }

        # 运行图
        config = {"configurable": {"thread_id": conversation_id or "default"}}

        try:
            result = await self.graph.ainvoke(initial_state, config)

            return {
                "response": result["final_response"],
                "conversation_id": conversation_id or "default",
                "agent_steps": result["agent_steps"],
                "suggested_actions": result["suggested_actions"],
                "metadata": {
                    "intent": result.get("intent"),
                    "timestamp": str(datetime.now())
                }
            }

        except Exception as e:
            logger.error(f"[LangGraph] Agent执行失败: {e}")
            return {
                "response": f"抱歉，处理您的请求时出错了：{str(e)}",
                "conversation_id": conversation_id or "default",
                "agent_steps": [],
                "suggested_actions": [],
                "metadata": {"error": str(e)}
            }

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
        work_id: Optional[str] = None,
        chapter_id: Optional[str] = None,
        conversation_id: Optional[str] = None,
        context: Optional[Dict[str, Any]] = None,
        on_plan: Optional[callable] = None,
        on_task_start: Optional[callable] = None,
        on_task_progress: Optional[callable] = None,
        on_task_done: Optional[callable] = None,
        on_content: Optional[callable] = None
    ) -> Dict[str, Any]:
        """
        与 Agent 对话 - Planning + Execution 模式

        Args:
            message: 用户消息
            work_id: 作品ID
            chapter_id: 章节ID
            conversation_id: 会话ID
            context: 额外上下文
            on_plan: 规划生成回调
            on_task_start: 任务开始回调
            on_task_progress: 任务进度回调
            on_task_done: 任务完成回调
            on_content: 内容生成回调

        Returns:
            Dict: Agent响应
        """
        try:
            # ========== 阶段1: 规划（Planning） ==========
            logger.info(f"[Planning] 开始规划: {message[:50]}...")

            plan_prompt = f"""你是专业的AI写作助手。用户请求如下：

用户请求：{message}
作品ID：{work_id}
当前页面章节ID：{chapter_id}

请分析这个请求，生成一个详细的To-Do List（任务清单），列出完成这个请求需要执行的步骤。

【重要】你必须只返回纯JSON，不要有任何其他文字、解释、或Markdown格式。

可用工具说明：
1. get_chapter_by_order_tool: 通过章节序号获取章节
   - 使用场景：用户说"第1章"、"第2章"、"第N章"等按序号指定章节
   - 参数：chapter_order (整数，例如 1, 2, 3...)
   - 示例：{{"tool": "get_chapter_by_order_tool", "params": {{"chapter_order": 2}}}}

2. read_chapter_tool: 通过章节ID读取章节内容
   - 使用场景：已知具体的chapter_id时使用
   - 参数：chapter_id (字符串UUID)
   - 注意：如果不知道具体的chapter_id，不要使用这个工具！应该用get_chapter_by_order_tool
   - 示例：{{"tool": "read_chapter_tool", "params": {{"chapter_id": "abc-123-def"}}}}

3. get_context_tool: 获取作品和章节的整体上下文
   - 使用场景：需要了解作品背景、描述、章节列表等
   - 参数：无需额外参数

4. search_analysis_fragments_tool: 从向量数据库检索相关分析片段
   - 使用场景：查找世界观、角色设定、情节分析等
   - 参数：query (搜索关键词)

5. continue_writing_tool: 续写内容
   - 使用场景：在已有内容基础上继续创作
   - 参数：context (已有内容), requirements (续写要求)

6. polish_text_tool: 润色文本
   - 参数：text, style

7. analyze_text_tool: 分析文本
   - 参数：text, focus

【工具选择规则】
- 用户说"第X章" → 必须用 get_chapter_by_order_tool
- 用户说"当前章节"或没指定章节 → 用 read_chapter_tool 配合当前chapter_id
- 用户说"读取/查看章节" + 章节序号 → 用 get_chapter_by_order_tool

示例1：用户说"续写第二章"
{{
  "user_intent": "续写第二章",
  "tasks": [
    {{
      "task_id": 1,
      "description": "读取第二章的现有内容",
      "tool": "get_chapter_by_order_tool",
      "params": {{"chapter_order": 2}},
      "estimated_time": "5秒"
    }},
    {{
      "task_id": 2,
      "description": "检索相关世界观和角色设定",
      "tool": "search_analysis_fragments_tool",
      "params": {{"query": "世界观和角色"}},
      "estimated_time": "3秒"
    }},
    {{
      "task_id": 3,
      "description": "基于上下文生成续写内容",
      "tool": "continue_writing_tool",
      "params": {{"context": "章节内容"}},
      "estimated_time": "10秒"
    }}
  ]
}}

现在直接返回JSON，不要任何解释："""

            plan_result = await self._generate_text(plan_prompt, temperature=0.3, max_tokens=1000)
            plan_text = plan_result.get("text", "").strip()

            # 解析规划JSON
            plan_data = self._extract_json_from_text(plan_text)

            if not plan_data:
                logger.warning(f"[Planning] 无法解析规划JSON，AI返回: {plan_text[:500]}")

            if not plan_data or "tasks" not in plan_data:
                # 默认规划
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
                            "description": "执行用户请求",
                            "tool": "auto",
                            "estimated_time": "10秒"
                        }
                    ]
                }

            logger.info(f"[Planning] 规划生成成功，共{len(plan_data['tasks'])}个任务")

            # 回调：发送规划
            if on_plan:
                await on_plan(plan_data)

            # ========== 阶段2: 执行（Execution） ==========
            task_results = []
            all_context = f"用户请求：{message}\n\n"

            for task in plan_data["tasks"]:
                task_id = task["task_id"]
                description = task["description"]
                tool_name = task.get("tool", "auto")

                logger.info(f"[Execution] 开始任务{task_id}: {description}")

                # 回调：任务开始
                if on_task_start:
                    await on_task_start(task)

                try:
                    # 执行任务
                    task_result = await self._execute_task(
                        task=task,
                        work_id=work_id,
                        chapter_id=chapter_id,
                        context=all_context,
                        on_progress=on_task_progress
                    )

                    task_results.append({
                        "task_id": task_id,
                        "description": description,
                        "result": task_result,
                        "status": "completed"
                    })

                    all_context += f"\n任务{task_id}结果：\n{task_result}\n"

                    logger.info(f"[Execution] 任务{task_id}完成")

                    # 回调：任务完成
                    if on_task_done:
                        await on_task_done(task, task_result)

                except Exception as e:
                    logger.error(f"[Execution] 任务{task_id}失败: {e}")
                    task_results.append({
                        "task_id": task_id,
                        "description": description,
                        "result": f"错误: {str(e)}",
                        "status": "failed"
                    })

            # ========== 阶段3: 总结（Summarization） ==========
            logger.info("[Summarization] 生成最终响应")

            summary_prompt = f"""基于以下任务执行结果，生成最终的响应给用户。

{all_context}

要求：
1. 综合所有任务结果
2. 用清晰、友好的语言呈现
3. 如果是创作内容，直接输出创作结果
4. 如果是分析/规划，给出详细说明

请生成最终响应："""

            final_content = ""
            async for chunk, _ in self.ai_service._stream_chat(
                messages=[{"role": "user", "content": summary_prompt}],
                max_tokens=2000,
                temperature=0.7
            ):
                if chunk:
                    final_content += chunk
                    # 回调：内容生成
                    if on_content:
                        await on_content(chunk)

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
                    "timestamp": str(datetime.now())
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

    async def _execute_task(
        self,
        task: Dict[str, Any],
        work_id: str,
        chapter_id: str,
        context: str,
        on_progress: Optional[callable] = None
    ) -> str:
        """执行单个任务"""
        tool_name = task.get("tool", "auto")
        params = task.get("params", {})

        if on_progress:
            await on_progress(task, "正在执行...")

        # 根据工具名称调用对应工具
        if tool_name == "get_chapter_by_order_tool":
            result = await get_chapter_by_order_tool.ainvoke({
                "work_id": work_id,
                "chapter_order": params.get("chapter_order", 1)
            })
        elif tool_name == "get_context_tool":
            result = await get_context_tool.ainvoke({
                "work_id": work_id,
                "chapter_id": chapter_id
            })
        elif tool_name == "read_chapter_tool":
            # 检查是否提供了 chapter_id 参数
            if "chapter_id" not in params or not params["chapter_id"]:
                logger.warning(
                    f"[_execute_task] read_chapter_tool 缺少 chapter_id 参数，"
                    f"将使用当前章节ID: {chapter_id}。"
                    f"任务描述: {task.get('description', 'N/A')}"
                )

            result = await read_chapter_tool.ainvoke({
                "work_id": work_id,
                "chapter_id": params.get("chapter_id", chapter_id)
            })
        elif tool_name == "search_analysis_fragments_tool":
            result = await search_analysis_fragments_tool.ainvoke({
                "work_id": work_id,
                "query": params.get("query", "相关内容"),
                "top_k": params.get("top_k", 5)
            })
        elif tool_name == "continue_writing_tool":
            result = await continue_writing_tool.ainvoke({
                "context": params.get("context", context),
                "requirements": params.get("requirements", "")
            })
        elif tool_name == "polish_text_tool":
            result = await polish_text_tool.ainvoke({
                "text": params.get("text", ""),
                "style": params.get("style", "professional")
            })
        elif tool_name == "analyze_text_tool":
            result = await analyze_text_tool.ainvoke({
                "text": params.get("text", ""),
                "focus": params.get("focus", "all")
            })
        else:
            # 自动选择工具
            result = f"任务 {task['description']} 需要手动处理"

        if on_progress:
            await on_progress(task, "完成")

        return result


# ==================== 导出 ====================

__all__ = ["WritingAgentGraph", "AgentState"]
 
