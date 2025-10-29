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

async def _generate_text_helper(prompt: str, temperature: float = 0.7, max_tokens: int = 1000) -> str:
    """辅助函数：使用 HTTPAIService 生成文本"""
    if not _global_ai_service:
        return "错误：AI服务未初始化"

    messages = [{"role": "user", "content": prompt}]
    generated_text = ""

    async for chunk, _ in _global_ai_service._stream_chat(
        messages=messages,
        max_tokens=max_tokens,
        temperature=temperature
    ):
        if chunk:
            generated_text += chunk

    return generated_text


@tool
async def continue_writing_tool(context: str, requirements: str = "") -> str:
    """续写工具：根据上下文续写内容

    Args:
        context: 已有的文本上下文
        requirements: 续写要求（可选）

    Returns:
        续写后的文本
    """
    prompt = f"""作为专业写作助手，请根据以下上下文续写内容。

上下文：
{context}

要求：{requirements if requirements else '保持风格一致，情节连贯'}

请续写："""

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
async def get_context_tool(work_id: str, chapter_id: str = "") -> str:
    """获取上下文工具：检索章节和世界观信息

    Args:
        work_id: 作品ID
        chapter_id: 章节ID（可选）

    Returns:
        上下文信息（JSON格式字符串）
    """
    # TODO: 调用数据库获取真实上下文
    import json
    context_info = {
        "work_id": work_id,
        "chapter_id": chapter_id or "N/A",
        "world_setting": "这里是世界观设定信息",
        "characters": ["主角", "配角A", "配角B"],
        "plot_summary": "这里是剧情概要"
    }
    return json.dumps(context_info, ensure_ascii=False, indent=2)


# 工具列表
WRITING_TOOLS = [
    continue_writing_tool,
    polish_text_tool,
    analyze_text_tool,
    get_context_tool
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

            # 使用 HTTPAIService 基于工具结果生成最终响应
            tool_result = messages[-1].content
            final_prompt = f"""{system_prompt}

工具执行结果：
{tool_result}

请基于工具结果，生成对用户友好的最终回复。"""

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

        # 提取 JSON
        json_match = re.search(r'\{[^}]+\}', decision_text)
        if json_match:
            try:
                decision = json.loads(json_match.group())
            except:
                decision = {"need_tools": False, "direct_response": decision_text}
        else:
            decision = {"need_tools": False, "direct_response": decision_text}

        logger.info(f"[LangGraph] {agent_type} 决策 (HTTPAIService): {decision.get('need_tools', False)}")

        if decision.get("need_tools", False):
            # 需要工具：手动调用
            tool_name = decision.get("tool_name", "continue_writing_tool")
            tool_args = decision.get("tool_args", {})

            # 调用工具
            tool_result = ""
            if tool_name == "continue_writing_tool":
                tool_result = await continue_writing_tool(
                    context=tool_args.get("context", last_user_message),
                    requirements=tool_args.get("requirements", "")
                )
            elif tool_name == "polish_text_tool":
                tool_result = await polish_text_tool(
                    text=tool_args.get("text", last_user_message),
                    style=tool_args.get("style", "professional")
                )
            elif tool_name == "analyze_text_tool":
                tool_result = await analyze_text_tool(
                    text=tool_args.get("text", last_user_message),
                    focus=tool_args.get("focus", "all")
                )
            elif tool_name == "get_context_tool":
                tool_result = await get_context_tool(
                    work_id=state.get("work_id", ""),
                    chapter_id=state.get("chapter_id", "")
                )

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
        """处理写作场景"""
        work_id = state.get("work_id")
        chapter_id = state.get("chapter_id")
        context_info = state.get("context", {})

        system_prompt = f"""你是专业的写作助手Agent。

可用工具：
- get_context_tool: 获取作品/章节上下文
- continue_writing_tool: 续写内容
- polish_text_tool: 润色文本

当前信息：作品ID={work_id}, 章节ID={chapter_id}

根据用户需求，决定是否调用工具来帮助用户。"""

        return await self._handle_agent_with_tools(state, "writing", system_prompt)

    async def _handle_planning(self, state: AgentState) -> AgentState:
        """处理规划场景"""
        system_prompt = """你是专业的规划助手Agent。

可用工具：
- get_context_tool: 获取作品信息
- analyze_text_tool: 分析现有内容

帮助用户规划小说创作，包括世界观、角色、大纲等。根据需要调用工具。"""

        return await self._handle_agent_with_tools(state, "planning", system_prompt)

    async def _handle_analysis(self, state: AgentState) -> AgentState:
        """处理分析场景"""
        system_prompt = """你是专业的文本分析Agent。

可用工具：
- analyze_text_tool: 深度分析文本
- get_context_tool: 获取上下文信息

帮助用户分析文本质量、逻辑、风格等。根据需要调用工具。"""

        return await self._handle_agent_with_tools(state, "analysis", system_prompt)

    async def _handle_stuck(self, state: AgentState) -> AgentState:
        """处理卡文场景"""
        system_prompt = """你是专业的写作指导Agent。

可用工具：
- get_context_tool: 获取当前创作背景
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


# ==================== 导出 ====================

__all__ = ["WritingAgentGraph", "AgentState"]
