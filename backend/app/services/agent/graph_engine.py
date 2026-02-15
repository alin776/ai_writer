# -*- coding: utf-8 -*-
"""
LangGraph StateGraph 核心引擎

真正的 LangGraph ReAct + Planning 架构：
- Planner 节点：分析意图，生成执行指引（或直接回答）
- Agent 节点：LLM + bind_tools，ReAct Think
- ToolNode：执行工具，ReAct Act
- 条件边：有 tool_calls → tools，无 → END

图结构：
  START → planner → (直接回答→END | agent ⇄ tools → END)
"""

import asyncio
import json
import logging
from typing import TypedDict, Annotated, Optional, Dict, Any, List

import httpx

from langchain_core.messages import SystemMessage, AIMessage
from langchain_openai import ChatOpenAI
from langgraph.graph import StateGraph, START, END, add_messages
from langgraph.prebuilt import ToolNode, tools_condition
from langgraph.config import get_stream_writer

from app.core.config import settings
from app.services.agent.langgraph_tools import LANGGRAPH_TOOLS
from app.services.agent.prompts.tool_descriptions import get_all_tools_description

logger = logging.getLogger(__name__)


# ==================== State 定义 ====================

class WritingAgentState(TypedDict):
    """ReAct Agent 状态"""
    # 消息历史（ReAct 核心，add_messages 自动累积）
    messages: Annotated[list, add_messages]

    # 输入上下文（由适配层填充）
    work_id: str
    chapter_id: str
    user_id: str
    conversation_id: str
    conversation_history: str       # ContextManager 构建的压缩历史
    context: Dict[str, Any]         # 结构化上下文 (tool_policy, selected_text 等)

    # 规划指引（Planner 输出）
    plan_guidance: Optional[str]    # 初始规划建议，作为系统消息指引 Agent
    downstream_tool: Optional[str]  # Planner 输出：smart_rewrite/smart_insert/smart_continue/smart_create

    # 工具结果存储（InjectedState 读取）
    tool_results: Dict[str, Any]    # tool_name → result，供后续工具读取


# ==================== LLM 工厂 ====================

def _create_llm(temperature: float = 0.7, max_tokens: int = 4096) -> ChatOpenAI:
    """创建 ChatOpenAI 实例（使用项目配置）"""
    return ChatOpenAI(
        model=settings.OPENAI_MODEL,
        api_key=settings.OPENAI_API_KEY,
        base_url=settings.OPENAI_BASE_URL,
        temperature=temperature,
        max_tokens=max_tokens,
        timeout=settings.OPENAI_TIMEOUT,
        max_retries=2,
    )


def _parse_json_from_text(text: str) -> Optional[dict]:
    """从文本中提取 JSON（兼容 markdown code fence）"""
    import re
    if not text:
        return None
    # 尝试直接解析
    try:
        return json.loads(text)
    except (json.JSONDecodeError, TypeError):
        pass
    # 尝试从 code fence 中提取
    match = re.search(r'```(?:json)?\s*\n?(.*?)\n?```', text, re.DOTALL)
    if match:
        try:
            return json.loads(match.group(1).strip())
        except (json.JSONDecodeError, TypeError):
            pass
    # 尝试查找 { ... } 块
    match = re.search(r'\{.*\}', text, re.DOTALL)
    if match:
        try:
            return json.loads(match.group(0))
        except (json.JSONDecodeError, TypeError):
            pass
    return None


# ==================== Planner 节点 ====================

def _build_planner_prompt(state: WritingAgentState) -> str:
    """构建 Planner 的系统 prompt

    复用现有 tool_descriptions 作为工具知识，
    但不再要求输出 JSON 任务列表——改为自然语言指引。
    """
    tool_desc = get_all_tools_description()
    conversation_history = state.get("conversation_history") or ""
    ctx = state.get("context") or {}

    history_section = ""
    if conversation_history:
        history_section = f"\n【对话历史】\n{conversation_history}\n"

    selected_text_section = ""
    if ctx.get("selected_text"):
        selected_text_section = f"\n【用户选中文本】\n{ctx['selected_text']}\n"

    knowledge_section = ""
    knowledge_docs = ctx.get("knowledge_docs")
    if isinstance(knowledge_docs, list) and knowledge_docs:
        titles = [d.get("title", "未命名") for d in knowledge_docs[:5] if isinstance(d, dict)]
        knowledge_section = f"\n【引用知识库】\n" + ", ".join(titles) + "\n"

    return f"""你是任务规划分析器。分析用户请求，判断执行策略。
{history_section}{selected_text_section}{knowledge_section}
【内部参数】
work_id: {state.get('work_id', '')}
chapter_id: {state.get('chapter_id', '')}

【可用工具】
{tool_desc}

【你的职责】
1. 分析用户意图
2. 判断是否需要工具：
   - 如果是闲聊/简单问答/不需要工具 → 设置 needs_tools=false，提供 direct_answer
   - 如果需要工具 → 设置 needs_tools=true，提供执行策略建议
3. 执行策略应包含：推荐的工具调用顺序、关键参数提示、注意事项

返回 JSON：
{{
  "needs_tools": true/false,
  "downstream_tool": "smart_rewrite 或 smart_insert 或 smart_continue 或 smart_create 或 null",
  "direct_answer": "不需要工具时的直接回答（needs_tools=false 时必填）",
  "guidance": "执行策略建议（needs_tools=true 时必填）",
  "intent_summary": "用户意图一句话概括"
}}

downstream_tool 取值说明（needs_tools=true 时必填）：
- smart_continue — 续写/接着写
- smart_create — 新建章节/写新章
- smart_rewrite — 改写/润色/扩写/缩写
- smart_insert — 在某位置插入内容
- null — 不确定/纯分析/不涉及内容创作

仅返回 JSON，禁止多余文字。"""


async def planner_node(state: WritingAgentState) -> dict:
    """Planner 节点 — 分析用户意图，生成执行指引或直接回答

    - 直接回答短路：闲聊/简单问答 → 返回 AIMessage（无 tool_calls）→ 直接到 END
    - 工具指引：复杂任务 → 返回 plan_guidance 系统消息 → Agent 节点基于指引做 ReAct
    """
    writer = get_stream_writer()

    # 调 LLM 分析意图
    llm = _create_llm(temperature=0.3, max_tokens=2000)
    planner_prompt = _build_planner_prompt(state)
    user_msg = state["messages"][-1]  # 最后一条用户消息

    response = await llm.ainvoke([
        SystemMessage(content=planner_prompt),
        user_msg,
    ])

    # 解析响应
    plan_data = _parse_json_from_text(response.content)

    if not plan_data:
        # JSON 解析失败，默认走工具路径
        logger.warning(f"[Planner] JSON 解析失败，默认需要工具: {response.content[:200]}")
        return {"plan_guidance": response.content}

    needs_tools = plan_data.get("needs_tools", True)
    intent_summary = plan_data.get("intent_summary", "")

    if intent_summary:
        logger.info(f"[Planner] 意图: {intent_summary}, needs_tools={needs_tools}")

    # 直接回答短路
    if not needs_tools:
        direct_answer = plan_data.get("direct_answer", "")
        if direct_answer:
            logger.info(f"[Planner] 直接回答短路 ({len(direct_answer)}字)")
            # 发送 output_ready 事件
            from app.services.agent.stream.flow_events import FlowEventBuilder
            writer(FlowEventBuilder.output_ready("回复内容", "", is_applicable=False))
            # 通过 stream_writer 发送内容（适配层捕获后调 on_content）
            writer({"type": "direct_answer", "content": direct_answer})
            # 返回 AIMessage → 条件边路由到 END（不经过 agent_node）
            return {
                "messages": [AIMessage(content=direct_answer)],
                "plan_guidance": None,
            }

    # 需要工具 → 返回执行指引
    guidance = plan_data.get("guidance", "")
    downstream_tool = plan_data.get("downstream_tool")
    # 过滤无效值：LLM 可能输出 "null" 字符串而非 JSON null
    if downstream_tool and downstream_tool not in ("smart_rewrite", "smart_insert", "smart_continue", "smart_create"):
        downstream_tool = None
    logger.info(f"[Planner] 生成执行指引 ({len(guidance)}字), downstream_tool={downstream_tool}")

    return {
        "plan_guidance": guidance,
        "downstream_tool": downstream_tool,
    }


async def agent_node(state: WritingAgentState) -> dict:
    """Agent 节点 — LLM + bind_tools，ReAct Think

    LLM 基于消息历史决定下一步：调用工具或生成最终回答。
    每次被调用都会重新评估 state，实现 Replanning。
    """
    llm = _create_llm()
    llm_with_tools = llm.bind_tools(LANGGRAPH_TOOLS)

    tool_desc = get_all_tools_description()

    # 构建系统 prompt
    system_parts = [
        "你是专业的小说写作AI助手（文枢AI）。",
        "根据用户请求、执行指引和已有工具结果，选择最合适的下一步行动。",
        "如果所有必要信息已收集完毕，直接生成最终回答。",
        "",
        "【重要】当所有工具调用完成后，你必须生成一段中文总结回复告知用户执行结果，"
        "包括完成了什么操作、生成/修改了什么内容。禁止在最终回复中只返回工具调用而不附带文字说明。",
        "",
        "【重要】每次只调用一个工具。当一个工具的输出是另一个工具的输入时（例如先 smart_continue 生成内容，再 operate_apply 写入），"
        "必须分开两轮调用：先调第一个工具，等拿到结果后再调第二个。禁止在同一轮中并行调用有依赖关系的工具。",
        "",
        "【重要】调用任何工具时，必须填写 step_reasoning 参数：用一句连贯的中文（约30字）描述你当前的思考。"
        "第一步格式为「用户要求XX + 我先做什么」，后续步骤格式为「上一步结果 + 当前要做什么」。"
        "示例：「用户要求续写第5章，先获取前文内容以保持风格一致」"
        "「已获取第4章完整内容，现在基于前文风格续写战斗场景」"
        "「续写内容已生成，现在将其追加到章节末尾」。"
        "要求语句连贯自然，每次调用都必须填写，不可省略。",
        "",
        f"【可用工具说明】\n{tool_desc}",
    ]

    # 内部参数
    work_id = state.get("work_id", "")
    chapter_id = state.get("chapter_id", "")
    if work_id or chapter_id:
        system_parts.append(
            f"\n【内部参数 — 调用工具时请直接使用这些值】\n"
            f"work_id: {work_id}\n"
            f"chapter_id: {chapter_id}\n"
            f"⚠️ 调用 explore_content、smart_continue、smart_create 等工具时，"
            f"请将上述 work_id/chapter_id 作为对应参数传入。"
        )

    # 对话历史上下文
    if state.get("conversation_history"):
        system_parts.append(f"\n【对话历史】\n{state['conversation_history']}")

    # 规划指引
    if state.get("plan_guidance"):
        system_parts.append(f"\n【执行指引】\n{state['plan_guidance']}")

    # 上下文信息
    ctx = state.get("context") or {}
    if ctx.get("selected_text"):
        system_parts.append(f"\n【用户选中文本】\n{ctx['selected_text']}")

    system_msg = SystemMessage(content="\n".join(system_parts))

    # 系统消息 + 所有历史消息（含 tool calls/results）
    messages = [system_msg] + state["messages"]

    # 网络级错误重试（SDK 内置重试只覆盖 HTTP 状态码，不覆盖连接中断）
    _RETRYABLE = (httpx.RemoteProtocolError, httpx.ReadError, httpx.ConnectError)
    for attempt in range(3):
        try:
            response = await llm_with_tools.ainvoke(messages)
            break
        except _RETRYABLE as e:
            if attempt == 2:
                raise
            wait = 2 ** attempt  # 1s, 2s
            logger.warning(f"[agent_node] 网络错误，{wait}s 后重试 ({attempt+1}/2): {e}")
            await asyncio.sleep(wait)

    return {"messages": [response]}


# ==================== 工具执行节点（带流式事件） ====================

# 工具图标映射（与 flow_events.py 保持一致）
_TOOL_ICONS = {
    "explore_content": "Search",
    "load_explore_artifact": "Search",
    "analyze_content": "FileSearch",
    "smart_continue": "PenTool",
    "smart_create": "PenTool",
    "smart_rewrite": "Edit3",
    "smart_insert": "Plus",
    "operate_apply": "Check",
    "delete_chapter": "Trash2",
    "update_chapter_content": "Save",
}

# 工具中文标题
_TOOL_TITLES = {
    "explore_content": "探索上下文",
    "load_explore_artifact": "读取探索结果",
    "analyze_content": "内容分析",
    "smart_continue": "智能续写",
    "smart_create": "新建章节",
    "smart_rewrite": "智能改写",
    "smart_insert": "智能插入",
    "operate_apply": "应用修改",
    "delete_chapter": "删除章节",
    "update_chapter_content": "更新内容",
}


# ToolNode 单例（避免每次 ReAct 循环重复初始化）
_INNER_TOOL_NODE = ToolNode(LANGGRAPH_TOOLS)


def _build_step_description(tool_name: str, msg_content: str) -> str:
    """从工具结果生成动态步骤描述（step_complete 用）"""
    fallback = _TOOL_TITLES.get(tool_name, "完成")
    try:
        data = json.loads(msg_content) if isinstance(msg_content, str) else msg_content
        if not isinstance(data, dict):
            return fallback
    except (json.JSONDecodeError, TypeError):
        return fallback

    if tool_name == "explore_content":
        evidences = data.get("evidences", [])
        chapters = data.get("chapters", [])
        return f"找到 {len(evidences)} 条证据，涉及 {len(chapters)} 个章节"

    if tool_name == "operate_apply":
        desc = data.get("description")
        if desc:
            return desc
        op = data.get("operation", "应用")
        title = data.get("chapter_title", "")
        content_len = data.get("content_length")
        if title and content_len:
            return f"{op} · {title}（约{content_len}字）"
        if title:
            return f"{op} · {title}"
        return fallback

    if tool_name in ("smart_continue", "smart_create", "smart_rewrite", "smart_insert"):
        title = data.get("chapter_title", "")
        content = data.get("content") or ""
        content_len = len(content) if content else 0
        parts = [fallback]
        if title:
            parts.append(title)
        if content_len:
            parts.append(f"约{content_len}字")
        return " · ".join(parts)

    return fallback


def _build_step_start_description(tool_name: str, args: dict) -> str:
    """从工具调用参数生成 step_start 描述（AI 要做什么）"""
    def _clip(text: str, max_len: int = 40) -> str:
        if not text:
            return ""
        text = text.strip().replace("\n", " ")
        return text[:max_len] + "…" if len(text) > max_len else text

    if tool_name == "explore_content":
        target = _clip(args.get("target_task", ""))
        return target or "探索相关上下文"

    if tool_name == "smart_continue":
        req = _clip(args.get("user_requirement", ""))
        wc = args.get("word_count", "")
        parts = []
        if req:
            parts.append(req)
        if wc:
            parts.append(f"约{wc}字")
        return " · ".join(parts) if parts else "续写章节内容"

    if tool_name == "smart_create":
        title = _clip(args.get("title", ""))
        wc = args.get("word_count", "")
        parts = []
        if title:
            parts.append(title)
        if wc:
            parts.append(f"约{wc}字")
        return " · ".join(parts) if parts else "创建新章节"

    if tool_name == "smart_rewrite":
        req = _clip(args.get("user_requirement", ""))
        return req or "改写选中内容"

    if tool_name == "smart_insert":
        intent = _clip(args.get("user_intent", ""))
        wc = args.get("word_count", "")
        parts = []
        if intent:
            parts.append(intent)
        if wc:
            parts.append(f"约{wc}字")
        return " · ".join(parts) if parts else "插入新内容"

    if tool_name == "operate_apply":
        op_map = {"append": "追加续写内容", "replace": "替换段落", "insert": "插入内容",
                  "content": "替换整章内容", "create": "创建新章节", "title": "修改标题"}
        op = args.get("operation", "")
        op_label = op_map.get(op, op)
        desc = _clip(args.get("target_description", ""))
        title = _clip(args.get("title", ""), 20)
        parts = [op_label] if op_label else []
        if title:
            parts.append(title)
        elif desc:
            parts.append(desc)
        return " · ".join(parts) if parts else "应用修改到章节"

    if tool_name == "load_explore_artifact":
        mode = args.get("mode", "full")
        mode_map = {"full": "加载完整结果", "summary": "加载摘要", "metadata": "加载元数据"}
        return mode_map.get(mode, "加载探索结果")

    if tool_name == "analyze_content":
        focus = _clip(args.get("focus", ""), 30)
        return focus or "分析内容质量"

    return ""


async def tool_executor_node(state: WritingAgentState) -> dict:
    """自定义工具执行节点 — 包装 ToolNode，添加 step_start/step_complete 流式事件"""
    from app.services.agent.stream.flow_events import FlowEventBuilder

    writer = get_stream_writer()

    # 从最后一条 AIMessage 获取 tool_calls
    last_msg = state["messages"][-1]
    tool_calls = getattr(last_msg, "tool_calls", []) or []

    # 基于已执行的工具数量计算 step_id 偏移（ReAct 每轮重入，避免 step_id 碰撞）
    existing_results = state.get("tool_results") or {}
    base_step_id = len(existing_results)

    # 为每个 tool_call 发送 step_start
    step_ids = {}
    step_reasonings = {}
    for i, tc in enumerate(tool_calls):
        tool_name = tc.get("name", "unknown")
        step_id = base_step_id + i + 1
        tc_id = tc.get("id", "")
        step_ids[tc_id] = step_id
        title = _TOOL_TITLES.get(tool_name, tool_name)
        args = tc.get("args", {})
        reasoning = args.get("step_reasoning") or ""
        if reasoning:
            step_reasonings[tc_id] = reasoning
        desc = reasoning or _build_step_start_description(tool_name, args)
        writer(FlowEventBuilder.step_start(step_id, title, description=desc))

    # 执行工具（ToolNode 自动处理 tool_calls → ToolMessages）
    result = await _INNER_TOOL_NODE.ainvoke(state)

    # 为每个完成的工具发送 step_complete
    result_messages = result.get("messages", [])
    for msg in result_messages:
        tool_call_id = getattr(msg, "tool_call_id", "")
        tool_name = getattr(msg, "name", "")
        step_id = step_ids.get(tool_call_id, 0)
        if step_id:
            icon = _TOOL_ICONS.get(tool_name, "Wrench")
            tool_call_data = {"icon": icon, "name": tool_name}
            # 优先沿用 AI step_reasoning，fallback 到模板摘要
            description = step_reasonings.get(tool_call_id) or _build_step_description(tool_name, getattr(msg, "content", ""))
            writer(FlowEventBuilder.step_complete(step_id, description, tool_call_data))

    # ========== 写作工具完成：发送 output_ready 事件 ==========
    _WRITING_TOOLS = {"smart_continue", "smart_create", "smart_rewrite", "smart_insert"}
    for msg in result_messages:
        tool_name = getattr(msg, "name", "")
        if tool_name not in _WRITING_TOOLS:
            continue
        output_title = _TOOL_TITLES.get(tool_name, "生成内容")
        content_str = getattr(msg, "content", "")
        if content_str:
            try:
                data = json.loads(content_str) if isinstance(content_str, str) else content_str
                if isinstance(data, dict) and data.get("chapter_title"):
                    output_title = data["chapter_title"]
            except (json.JSONDecodeError, TypeError):
                pass
        writer(FlowEventBuilder.output_ready(output_title, "", is_applicable=True))
        break

    # 存储工具结果到 state（供后续工具通过 InjectedState 读取）
    tool_results = dict(state.get("tool_results") or {})
    for msg in result_messages:
        name = getattr(msg, "name", "")
        if name and hasattr(msg, "content"):
            try:
                tool_results[name] = json.loads(msg.content)
            except (json.JSONDecodeError, TypeError):
                tool_results[name] = msg.content

    result["tool_results"] = tool_results

    # ========== 非阻塞修订：发送 revision 事件（不中断 AI 流程） ==========
    # requires_confirmation 属于"打补丁"模式：AI 跑完全程，内容实时推到编辑器，
    # 用户最后自行决定采纳/撤销。不需要 interrupt() 暂停 AI。
    for msg in result_messages:
        name = getattr(msg, "name", "")
        content_str = getattr(msg, "content", "")
        if not content_str:
            continue
        try:
            tool_result_data = json.loads(content_str) if isinstance(content_str, str) else content_str
        except (json.JSONDecodeError, TypeError):
            continue
        if not (isinstance(tool_result_data, dict) and tool_result_data.get("requires_confirmation")):
            continue

        request_id = tool_result_data.get("request_id") or f"{name}_{getattr(msg, 'tool_call_id', 'unknown')}"
        logger.info(f"[Revision] 检测到 requires_confirmation, request_id={request_id}, tool={name}")

        # 通过 stream_writer 发送 revision 事件（前端编辑器展示预览）
        from app.services.agent.stream.flow_events import FlowEventBuilder as _FEB
        operation = tool_result_data.get("operation", "replace")
        revision_type_map = {"append": "append", "insert": "insert", "replace": "replace", "replace_all": "replace"}
        revision_type = revision_type_map.get(operation, "replace")
        new_content = tool_result_data.get("content") or tool_result_data.get("new_content") or tool_result_data.get("new_title")
        original_content = tool_result_data.get("original_text") or tool_result_data.get("original_content")
        content_preview = new_content[:50] if new_content and len(new_content) > 50 else new_content
        writer(_FEB.revision(
            revision_type=revision_type,
            request_id=request_id,
            chapter_id=tool_result_data.get("chapter_id"),
            chapter_title=tool_result_data.get("chapter_title"),
            content=new_content,
            content_preview=content_preview,
            original_content=original_content,
            position=tool_result_data.get("position"),
            operation=operation,
            editor_action=tool_result_data.get("editor_action"),
            old_title=tool_result_data.get("old_title"),
            new_title=tool_result_data.get("new_title"),
            versions=tool_result_data.get("versions") or tool_result_data.get("recommendations"),
        ))
        # 注意：不写入 _hitl_pending！AI 继续运行，用户之后通过 /chat/approval-response 采纳/撤销
        break

    return result


# ==================== 条件路由 ====================

def _planner_route(state: WritingAgentState) -> str:
    """Planner 后条件路由

    - 直接回答（messages 末尾是 AIMessage 且 plan_guidance=None） → END
    - 需要工具 → agent
    """
    messages = state.get("messages", [])
    if messages and isinstance(messages[-1], AIMessage) and state.get("plan_guidance") is None:
        return END
    return "agent"


# ==================== 图构建 ====================

def build_graph(checkpointer=None):
    """构建并编译 StateGraph

    图结构：START → planner → (直接回答→END | agent ⇄ tools → END)

    Args:
        checkpointer: 可选的 checkpointer（AsyncRedisSaver）

    Returns:
        编译后的 CompiledGraph
    """
    # 构建图
    workflow = StateGraph(WritingAgentState)

    # 添加节点
    workflow.add_node("planner", planner_node)
    workflow.add_node("agent", agent_node)
    workflow.add_node("tools", tool_executor_node)  # 自定义工具节点（带流式事件）

    # 添加边
    workflow.add_edge(START, "planner")
    workflow.add_conditional_edges("planner", _planner_route)  # 直接回答→END, 需工具→agent
    workflow.add_conditional_edges("agent", tools_condition)    # tool_calls→tools, else→END
    workflow.add_edge("tools", "agent")   # 工具执行后 → 回到 agent（ReAct 循环）

    # 编译
    compile_kwargs = {}
    if checkpointer:
        compile_kwargs["checkpointer"] = checkpointer

    graph = workflow.compile(**compile_kwargs)

    logger.info("[GraphEngine] ✅ StateGraph 编译完成: START → planner → (END | agent ⇄ tools → agent → END)")
    return graph


# ==================== 导出 ====================

__all__ = [
    "WritingAgentState",
    "build_graph",
    "planner_node",
    "agent_node",
]
