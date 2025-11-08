"""
Agent React Stream 端点

提供基于LangGraph ReAct模式的流式响应，支持实时进度显示

特点：
- 使用 chat_stream() 方法（基于astream）
- 实时显示节点执行进度
- 工具调用可见
- 完全不影响现有端点
"""

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import StreamingResponse
from typing import Optional
import logging
import json
import uuid
from datetime import datetime

from app.core.security import get_current_active_user
from app.core.features import is_react_stream_enabled
from app.models.user import User
from app.services.agent.memory import MemoryManager
from app.api.v1.agent import (
    AgentChatRequest,
    get_memory_manager,
    get_agent_graph
)

router = APIRouter()
logger = logging.getLogger(__name__)


@router.post("/chat/react-stream")
async def agent_react_stream(
    request: AgentChatRequest,
    current_user: User = Depends(get_current_active_user),
    memory: MemoryManager = Depends(get_memory_manager)
):
    """
    Agent 智能对话 - ReAct流式响应（SSE）

    使用 LangGraph ReAct 模式 + astream()：
    1. 实时显示节点执行进度（intent_classifier, agent, tools）
    2. 工具调用可见
    3. Agent思考过程透明
    4. 性能零开销

    与 /chat/stream 的区别：
    - /chat/stream: Planning模式（规划->执行->汇总）
    - /chat/react-stream: ReAct模式（自动决策->工具调用->响应）

    Args:
        request: 对话请求
        current_user: 当前用户
        memory: 记忆管理器
        ai_service: AI服务
        db: 数据库会话

    Returns:
        StreamingResponse: SSE流式响应

    SSE事件格式：
    - type: "start" - 开始执行
    - type: "progress" - 进度更新
    - type: "tool_call" - 工具调用
    - type: "content" - 内容生成
    - type: "done" - 执行完成
    - type: "error" - 执行错误
    """

    # 功能开关检查
    if not is_react_stream_enabled():
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="ReAct流式模式当前未启用"
        )

    async def event_generator():
        import asyncio

        try:
            user_id = str(current_user.id)
            conversation_id = request.conversation_id or str(uuid.uuid4())

            logger.info(
                f"[React Stream] 开始 - User: {user_id}, "
                f"Message: {request.message[:50]}..."
            )

            # 发送开始事件
            yield f"data: {json.dumps({
                'type': 'start',
                'conversation_id': conversation_id,
                'timestamp': datetime.now().isoformat()
            }, ensure_ascii=False)}\n\n"

            # 获取记忆上下文
            user_context = await memory.get_complete_context(user_id)
            memory_context = memory.format_context_for_agent(user_id, mode="chat")

            # 获取全局共享的 LangGraph Agent
            agent_graph = get_agent_graph()

            # 准备上下文
            context = request.context or {}
            context["memory_context"] = memory_context
            context["user_context"] = user_context

            # 使用队列实现回调事件传递
            event_queue = asyncio.Queue()
            agent_task = None
            result = None

            # 定义回调函数 - 将事件放入队列
            async def on_progress(event: dict):
                """进度回调 - 节点执行进度"""
                logger.debug(f"[React Stream] Progress: {event.get('description')}")
                await event_queue.put(('progress', event))

            async def on_tool_call(tool_name: str, tool_args: dict):
                """工具调用回调"""
                logger.info(f"[React Stream] Tool call: {tool_name}")
                await event_queue.put(('tool_call', {
                    'tool': tool_name,
                    'args': tool_args,
                    'timestamp': datetime.now().isoformat()
                }))

            async def on_content(content: str):
                """内容生成回调"""
                logger.debug(f"[React Stream] Content: {content[:50]}...")
                await event_queue.put(('content', {'content': content}))

            # 在后台运行 chat_stream
            async def run_agent():
                nonlocal result
                try:
                    result = await agent_graph.chat_stream(
                        message=request.message,
                        user_id=user_id,  # 新增：传入用户ID
                        work_id=request.work_id,
                        chapter_id=request.chapter_id,
                        conversation_id=conversation_id,
                        context=context,
                        on_progress=on_progress,
                        on_tool_call=on_tool_call,
                        on_content=on_content
                    )
                    # 放入完成标记
                    await event_queue.put(('__done__', None))
                except Exception as e:
                    logger.error(f"[React Stream] run_agent failed: {str(e)}", exc_info=True)
                    # 放入错误标记
                    await event_queue.put(('__error__', str(e)))

            # 启动后台任务
            agent_task = asyncio.create_task(run_agent())

            # 实时从队列中取事件并发送
            while True:
                event_type, event_data = await event_queue.get()

                if event_type == '__done__':
                    break

                if event_type == '__error__':
                    # 处理后台任务的错误
                    yield f"data: {json.dumps({
                        'type': 'error',
                        'error': str(event_data),
                        'timestamp': datetime.now().isoformat()
                    }, ensure_ascii=False)}\n\n"
                    return  # 提前结束

                # 发送SSE事件
                yield f"data: {json.dumps({
                    'type': event_type,
                    'data': event_data
                }, ensure_ascii=False)}\n\n"

            # 等待agent任务完成（带异常处理）
            try:
                await agent_task
            except Exception as e:
                # 异常已通过队列发送，这里只记录日志
                logger.error(f"[React Stream] Agent task error: {str(e)}", exc_info=True)
                return

            # 检查result是否有效
            if result is None:
                logger.error("[React Stream] Result is None after agent task completed")
                yield f"data: {json.dumps({
                    'type': 'error',
                    'error': 'Agent执行失败，未返回结果',
                    'timestamp': datetime.now().isoformat()
                }, ensure_ascii=False)}\n\n"
                return

            # 记录交互到用户记忆
            memory.record_user_interaction(
                user_id,
                "agent_react_chat",
                {
                    "message": request.message,
                    "intent": result.get("metadata", {}).get("intent"),
                    "conversation_id": conversation_id,
                    "mode": "react_stream"
                }
            )

            # 发送完成事件
            yield f"data: {json.dumps({
                'type': 'done',
                'data': {
                    'response': result.get('response', ''),
                    'metadata': result.get('metadata', {}),
                    'suggested_actions': result.get('suggested_actions', []),
                    'agent_steps': result.get('agent_steps', [])
                }
            }, ensure_ascii=False)}\n\n"

            logger.info(
                f"[React Stream] 完成 - User: {user_id}, "
                f"Intent: {result.get('metadata', {}).get('intent')}, "
                f"Events: {result.get('metadata', {}).get('stream_events', 0)}"
            )

        except Exception as e:
            logger.error(f"[React Stream] Error: {str(e)}", exc_info=True)
            yield f"data: {json.dumps({
                'type': 'error',
                'error': str(e),
                'timestamp': datetime.now().isoformat()
            }, ensure_ascii=False)}\n\n"

    return StreamingResponse(
        event_generator(),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
            "X-Accel-Buffering": "no"  # 禁用nginx缓冲
        }
    )
