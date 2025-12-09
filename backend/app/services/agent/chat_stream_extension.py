"""
chat_stream扩展方法

将此文件中的方法添加到WritingAgentGraph类中
添加位置：在chat()方法之后（约Line 1643之后）
"""

from typing import Optional, Callable, Dict, Any
from datetime import datetime
import logging
import uuid

from langchain_core.messages import AIMessage, ToolMessage
from langgraph.checkpoint.redis import AsyncRedisSaver

from app.services.context.context_config import ContextConfig
from app.utils.datetime_utils import get_utc_now

logger = logging.getLogger(__name__)


# ==================== 添加到WritingAgentGraph类的方法 ====================

async def chat_stream(
    self,
    message: str,
    work_id: Optional[str] = None,
    chapter_id: Optional[str] = None,
    conversation_id: Optional[str] = None,
    context: Optional[dict] = None,
    on_progress: Optional[Callable] = None,
    on_tool_call: Optional[Callable] = None,
    on_content: Optional[Callable] = None,
    user_id: Optional[str] = None  # 补充用户隔离信息（向后兼容，默认可为空）
) -> Dict[str, Any]:
    """
    流式执行chat()，提供实时进度反馈

    Args:
        message: 用户消息
        work_id: 作品ID
        chapter_id: 章节ID
        conversation_id: 会话ID
        context: 额外上下文
        on_progress: 进度回调 async def on_progress(event: dict)
        on_tool_call: 工具调用回调 async def on_tool_call(tool_name: str, tool_args: dict)
        on_content: 内容生成回调 async def on_content(content: str)

    Returns:
        Dict: Agent响应（同chat()方法）
    """

    logger.info(f"[LangGraph Stream] 开始流式执行: {message[:50]}...")

    # 懒加载AsyncRedisSaver索引
    if isinstance(self.checkpointer, AsyncRedisSaver) and not self._checkpointer_setup_done:
        try:
            await self.checkpointer.asetup()
            self._checkpointer_setup_done = True
            logger.info(f"[LangGraph] AsyncRedisSaver索引创建成功")
        except Exception as setup_error:
            logger.error(f"[LangGraph] AsyncRedisSaver索引创建失败: {setup_error}")
            raise

    # 兜底 conversation_id，防止落入默认共享线程
    if not conversation_id:
        conversation_id = str(uuid.uuid4())
        logger.warning(f"[LangGraph Stream] 未提供 conversation_id，自动生成: {conversation_id}")

    # 提示缺失 work_id 可能导致跨作品污染
    if not work_id:
        logger.warning("[LangGraph Stream] work_id 缺失，将退化为用户/会话级隔离，请尽快在前端补充 work_id")

    # 构建初始状态（与chat()相同）
    from langchain_core.messages import HumanMessage
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

    # 构建隔离 thread_id（与主流程对齐）
    user_prefix = f"{user_id}:" if user_id else ""
    if work_id and conversation_id:
        thread_id = f"{user_prefix}{work_id}:{conversation_id}"
    elif work_id:
        thread_id = f"{user_prefix}{work_id}:default"
    elif conversation_id:
        thread_id = f"{user_prefix}{conversation_id}"
    else:
        thread_id = f"{user_prefix}anonymous:{uuid.uuid4()}" if user_prefix else f"{user_prefix}anonymous:{uuid.uuid4()}"

    max_len = ContextConfig.MAX_THREAD_ID_LENGTH
    if len(thread_id) > max_len:
        import hashlib as _hashlib
        hash_suffix = _hashlib.sha1(thread_id.encode("utf-8")).hexdigest()[:10]
        prefix_budget = max_len - len(hash_suffix) - 1
        thread_id = f"{thread_id[:prefix_budget]}:{hash_suffix}"
        logger.warning(f"[LangGraph Stream] thread_id 过长，已压缩为: {thread_id}")

    logger.info(f"[LangGraph Stream] 使用隔离的thread_id: {thread_id} (user_id={user_id}, work_id={work_id}, conversation_id={conversation_id})")

    # 配置
    config = {
        "configurable": {
            "thread_id": thread_id,
            "checkpoint_ns": ""
        }
    }

    try:
        # 使用astream()流式执行
        event_count = 0

        async for event in self.graph.astream(initial_state, config):
            event_count += 1

            # 处理事件并触发回调
            await self._handle_stream_event(
                event,
                on_progress=on_progress,
                on_tool_call=on_tool_call,
                on_content=on_content
            )

        logger.info(f"[LangGraph Stream] 流式执行完成，共{event_count}个事件")

        # 获取最终状态
        final_state = await self.graph.aget_state(config)

        # 构建返回结果（与chat()相同的格式）
        if final_state and final_state.values:
            result = final_state.values
            return {
                "response": result.get("final_response"),
                "conversation_id": conversation_id,
                "messages": result.get("messages", []),
                "agent_steps": result.get("agent_steps", []),
                "suggested_actions": result.get("suggested_actions", []),
                "metadata": {
                    "intent": result.get("intent"),
                    "timestamp": str(get_utc_now()),
                    "stream_events": event_count
                }
            }
        else:
            logger.error("[LangGraph Stream] 无法获取最终状态")
            return {
                "response": "执行完成，但无法获取结果",
                "conversation_id": conversation_id,
                "agent_steps": [],
                "suggested_actions": [],
                "metadata": {"error": "No final state"}
            }

    except Exception as e:
        import traceback
        error_msg = str(e) or repr(e)
        error_trace = traceback.format_exc()
        logger.error(f"[LangGraph Stream] 执行失败: {error_msg}")
        logger.error(f"[LangGraph Stream] 错误堆栈:\n{error_trace}")
        return {
            "response": f"抱歉，处理您的请求时出错了：{error_msg}",
            "conversation_id": conversation_id,
            "agent_steps": [],
            "suggested_actions": [],
            "metadata": {"error": error_msg, "traceback": error_trace}
        }


async def _handle_stream_event(
    self,
    event: dict,
    on_progress: Optional[Callable] = None,
    on_tool_call: Optional[Callable] = None,
    on_content: Optional[Callable] = None
):
    """
    处理astream事件，转换为用户友好的进度信息并触发回调

    event结构（基于LangGraph）：
    {
        "node_name": {
            "messages": [...],
            "intent": "...",
            "work_id": "...",
            ...
        }
    }
    """

    if not event:
        return

    # 提取节点名和数据
    node_name = list(event.keys())[0]
    node_data = event[node_name]

    logger.debug(f"[Stream Event] 节点: {node_name}")

    # 1. 解析进度事件并触发on_progress
    if on_progress:
        progress_event = self._parse_node_event(node_name, node_data)
        if progress_event:
            try:
                await on_progress(progress_event)
            except Exception as e:
                logger.error(f"[Stream] 进度回调失败: {e}")

    # 2. 检测工具调用并触发on_tool_call
    if on_tool_call and node_name == "tools":
        tool_calls = self._extract_tool_calls(node_data)
        for tool_name, tool_args in tool_calls:
            try:
                await on_tool_call(tool_name, tool_args)
            except Exception as e:
                logger.error(f"[Stream] 工具回调失败: {e}")

    # 3. 检测内容生成并触发on_content
    if on_content:
        content = self._extract_content(node_name, node_data)
        if content:
            try:
                await on_content(content)
            except Exception as e:
                logger.error(f"[Stream] 内容回调失败: {e}")


def _parse_node_event(self, node_name: str, node_data: dict) -> Optional[dict]:
    """
    将LangGraph节点事件转换为用户友好的进度信息

    返回格式：
    {
        "type": "progress",
        "step": "intent_analysis" | "thinking" | "tool_execution" | "generating",
        "description": "正在分析您的需求...",
        "node": "intent_classifier",
        "details": {...},
        "timestamp": "2025-01-06T10:30:00Z"
    }
    """

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
        # 提取工具名称
        messages = node_data.get("messages", [])
        tool_names = []
        for msg in messages:
            if hasattr(msg, "name"):
                tool_names.append(msg.name)

        if tool_names:
            details["tools"] = tool_names
            # 更新描述（显示工具名）
            tool_display_names = {
                "get_chapter_by_order_tool": "读取章节",
                "continue_writing_tool": "继续创作",
                "search_analysis_fragments_tool": "检索设定",
                "search_memory_tool": "搜索记忆",
                "add_todo_tool": "添加待办",
                "get_work_details_tool": "获取作品信息",
                "update_work_metadata_tool": "更新元数据"
            }
            display_names = [tool_display_names.get(t, t) for t in tool_names]
            mapping["description"] = f"正在{', '.join(display_names[:2])}..."

    return {
        "type": "progress",
        "step": mapping["step"],
        "description": mapping["description"],
        "node": node_name,
        "details": details,
        "timestamp": get_utc_now().isoformat()
    }


def _extract_tool_calls(self, node_data: dict) -> list:
    """
    提取工具调用信息

    Returns:
        List[Tuple[str, dict]]: [(tool_name, tool_args), ...]
    """
    tool_calls = []
    messages = node_data.get("messages", [])

    for msg in messages:
        if isinstance(msg, ToolMessage) and hasattr(msg, "name"):
            tool_name = msg.name
            # 工具参数通常在调用时存储，这里简化处理
            tool_args = {}
            tool_calls.append((tool_name, tool_args))

    return tool_calls


def _extract_content(self, node_name: str, node_data: dict) -> Optional[str]:
    """
    提取生成的内容

    只有agent节点可能生成用户可见的内容
    """
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


# ==================== 集成说明 ====================

"""
将上述方法添加到WritingAgentGraph类的步骤：

1. 打开 backend/app/services/agent/langgraph_agent.py

2. 找到chat()方法的结束位置（约Line 1642）

3. 在chat()方法之后，添加以下4个方法：
   - chat_stream()
   - _handle_stream_event()
   - _parse_node_event()
   - _extract_tool_calls()
   - _extract_content()

4. 确保缩进正确（这些方法都是WritingAgentGraph类的成员方法）

5. 保存文件

6. 运行测试验证：
   python tests/test_chat_stream.py

完整代码见上方，直接复制粘贴即可。
"""
