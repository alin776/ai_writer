"""
Agent 智能助手 API 路由

提供 Agent 相关的 RESTful API 接口，包括：
- Agent 对话（支持流式响应）
- 人机协同（HITL）批准管理
- 执行计划管理
- 记忆管理
"""

from fastapi import APIRouter, Depends, HTTPException, status, Query
from fastapi.responses import StreamingResponse
from sqlalchemy.ext.asyncio import AsyncSession
from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any
import logging
import json
import uuid
from datetime import datetime

from app.core.database import get_db
from app.core.security import get_current_active_user
from app.models.user import User
from app.models.chat_models import ChatMode, ChatRequest as UnifiedChatRequest, format_react_event_to_sse, format_planning_event_to_sse, format_error_event
from app.services.agent.memory import MemoryManager
from app.services.agent.agents import PlanningAgent, ReflectionAgent
from app.services.agent.tools import HITLManager
from app.services.ai.http_ai_service import HTTPAIService
from app.services.agent.langgraph_agent import WritingAgentGraph
from app.core.config import settings
# ✅ 2025-12-01: 支持Agent成本追踪（通过请求上下文传递user_id）
from app.core.request_context import set_request_context
import redis

router = APIRouter()
logger = logging.getLogger(__name__)

# 创建同步Redis连接池（全局复用，避免每次请求都建立新连接）
_redis_pool = None

def get_redis_client():
    """获取同步Redis客户端（使用连接池）"""
    global _redis_pool

    # 🔧 修复：使用全局连接池，避免每次都创建新连接
    if _redis_pool is None:
        _redis_pool = redis.ConnectionPool(
            host='localhost',
            port=6379,
            db=1,  # 使用db1，避免与缓存服务冲突
            decode_responses=False,
            max_connections=10,  # 最大连接数
            socket_connect_timeout=5,  # 连接超时5秒
            socket_timeout=5,  # 操作超时5秒
        )
        logger.info("[Redis] 全局连接池已创建")

    return redis.Redis(connection_pool=_redis_pool)

# 全局Agent实例（跨请求共享，保持MemorySaver持久化）
_global_agent_graph = None

def get_agent_graph() -> WritingAgentGraph:
    """
    获取全局共享的Agent实例

    使用全局单例模式，确保MemorySaver在请求间共享，
    从而实现对话历史的持久化

    TODO (2025-12-01): 成本追踪限制
    ----------------------------------------
    当前全局单例的HTTPAIService不包含db和user_id，导致Agent内部的AI调用无法追踪成本。
    这是一个架构限制，需要深度重构才能解决：

    解决方案选项：
    1. 移除全局单例，使用外部存储（Redis）保持MemorySaver的持久化
    2. 修改WritingAgentGraph支持运行时动态设置ai_service
    3. 在Agent内部使用事件系统，将AI调用委托给请求级别的ai_service

    优先级：P2（中期优化）
    预计工作量：6-8小时
    ----------------------------------------
    """
    global _global_agent_graph
    if _global_agent_graph is None:
        # 创建AI服务（使用配置中的MODEL_SELECTION_ENABLED）
        # 注意：此ai_service不包含db/user_id，Agent的AI调用成本暂时无法追踪
        ai_service = HTTPAIService(
            enable_model_selector=settings.MODEL_SELECTION_ENABLED
        )
        # 创建Agent实例（只创建一次）
        _global_agent_graph = WritingAgentGraph(ai_service, use_chatgpt=settings.AGENT_USE_CHATGPT)
        logger.info("[Global Agent] 创建全局Agent实例，MemorySaver将在请求间共享")
    return _global_agent_graph


# ==================== 请求/响应数据模型 ====================

class AgentChatRequest(BaseModel):
    """Agent 对话请求"""
    message: str = Field(..., description="用户消息", min_length=1)
    mode: Optional[str] = Field(None, description="聊天模式：planning/react（默认planning）")
    work_id: Optional[str] = Field(None, description="作品ID")
    chapter_id: Optional[str] = Field(None, description="章节ID")
    conversation_id: Optional[str] = Field(None, description="会话ID（用于继续对话）")
    context: Optional[Dict[str, Any]] = Field(default_factory=dict, description="额外上下文")


class AgentChatResponse(BaseModel):
    """Agent 对话响应"""
    response: str = Field(..., description="Agent回复")
    conversation_id: str = Field(..., description="会话ID")
    agent_steps: List[Dict[str, Any]] = Field(default_factory=list, description="Agent执行步骤")
    suggested_actions: List[str] = Field(default_factory=list, description="建议的后续操作")
    metadata: Dict[str, Any] = Field(default_factory=dict, description="元数据")


class PlanCreationRequest(BaseModel):
    """创建执行计划请求"""
    goal: str = Field(..., description="目标描述", min_length=1)
    genre: Optional[str] = Field(None, description="小说类型")
    work_id: Optional[str] = Field(None, description="作品ID")
    context: Optional[Dict[str, Any]] = Field(default_factory=dict, description="上下文")


class PlanResponse(BaseModel):
    """执行计划响应"""
    plan_id: str = Field(..., description="计划ID")
    goal: str = Field(..., description="目标")
    tasks: List[Dict[str, Any]] = Field(..., description="任务列表")
    status: str = Field(..., description="计划状态")
    progress: float = Field(..., description="进度 0-1")


class ApprovalActionRequest(BaseModel):
    """批准操作请求"""
    action: str = Field(..., description="操作类型: approve/reject/modify")
    modifications: Optional[Dict[str, Any]] = Field(None, description="修改内容（action=modify时）")
    feedback: Optional[str] = Field(None, description="反馈说明")


class ApprovalResponse(BaseModel):
    """批准响应"""
    request_id: str
    title: str
    description: str
    proposed_action: Dict[str, Any]
    alternatives: List[Dict[str, Any]]
    status: str
    created_at: str


class ResetConversationRequest(BaseModel):
    """重置会话请求"""
    conversation_id: str = Field(..., description="要重置的会话ID")


class ResetConversationResponse(BaseModel):
    """重置会话响应"""
    new_conversation_id: str = Field(..., description="新的会话ID")
    message: str = Field(default="会话已重置", description="提示消息")


class CreateBranchRequest(BaseModel):
    """创建分支请求"""
    conversation_id: str = Field(..., description="当前会话ID（父分支）")
    fork_point_message_index: int = Field(
        ...,
        ge=0,
        description=(
            "分叉点消息索引（从0开始）\n"
            "注意：这是用户看到的消息索引，不是内部checkpoint索引\n"
            "例如：index=0表示在第1条消息后分叉，index=2表示在第3条消息后分叉"
        )
    )
    branch_name: Optional[str] = Field(None, description="分支名称（可选，自动生成格式: 分支-MMDD-HHMM）")


class BranchResponse(BaseModel):
    """分支响应"""
    branch_id: str = Field(..., description="分支ID（新的thread_id）")
    parent_branch_id: str = Field(..., description="父分支ID")
    branch_name: str = Field(..., description="分支名称")
    fork_point_index: int = Field(..., description="分叉点索引")
    message_count: int = Field(0, description="分支中的消息数")
    created_at: str = Field(..., description="创建时间（ISO格式）")


class SwitchBranchRequest(BaseModel):
    """切换分支请求"""
    branch_id: str = Field(..., description="要切换到的分支ID")


class SwitchBranchResponse(BaseModel):
    """切换分支响应"""
    branch_id: str = Field(..., description="分支ID")
    branch_name: str = Field(..., description="分支名称")
    message_count: int = Field(..., description="分支中的消息数")
    messages: List[Dict[str, Any]] = Field(default_factory=list, description="分支的消息历史")


class BranchTreeNode(BaseModel):
    """分支树节点"""
    branch_id: str = Field(..., description="分支ID")
    parent_branch_id: Optional[str] = Field(None, description="父分支ID")
    branch_name: str = Field(..., description="分支名称")
    message_count: int = Field(0, description="消息数")
    is_active: bool = Field(False, description="是否活跃")
    created_at: str = Field(..., description="创建时间")
    children: List["BranchTreeNode"] = Field(default_factory=list, description="子分支")


class GetBranchesResponse(BaseModel):
    """获取分支列表响应"""
    conversation_id: str = Field(..., description="会话ID")
    total_branches: int = Field(..., description="总分支数")
    branches: List[BranchTreeNode] = Field(default_factory=list, description="分支树（扁平列表）")


# ==================== 依赖注入 ====================

async def get_memory_manager(
    db: AsyncSession = Depends(get_db)
) -> MemoryManager:
    """获取记忆管理器"""
    redis_client = get_redis_client()
    manager = MemoryManager(redis_client)
    return manager


async def get_planning_agent() -> PlanningAgent:
    """获取规划Agent"""
    return PlanningAgent()


async def get_hitl_manager() -> HITLManager:
    """获取HITL管理器"""
    redis_client = get_redis_client()
    return HITLManager(redis_client)


async def get_ai_service(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
) -> HTTPAIService:
    """获取AI服务实例"""
    # 2025-12-01: 传递db和user_id以启用成本追踪
    return HTTPAIService(db=db, user_id=str(current_user.id))


# ==================== Agent 对话接口 ====================

@router.post("/chat", response_model=AgentChatResponse)
async def agent_chat(
    request: AgentChatRequest,
    current_user: User = Depends(get_current_active_user),
    memory: MemoryManager = Depends(get_memory_manager),
    ai_service: HTTPAIService = Depends(get_ai_service),
    db: AsyncSession = Depends(get_db)
):
    """
    Agent 智能对话（基于 LangGraph 框架）- 非流式响应

    支持的场景：
    - "帮我写第三章" (writing)
    - "我想写玄幻小说" (planning)
    - "分析这段文字哪里不好" (analysis)
    - "我卡文了" (stuck)

    Args:
        request: 对话请求
        current_user: 当前用户
        memory: 记忆管理器
        ai_service: AI服务
        db: 数据库会话

    Returns:
        AgentChatResponse: Agent响应
    """
    try:
        user_id = str(current_user.id)
        conversation_id = request.conversation_id or str(uuid.uuid4())

        # ✅ 2025-12-01: 设置请求上下文，让全局Agent的HTTPAIService能追踪成本
        set_request_context(db, user_id)

        logger.info(f"[LangGraph Agent] User: {user_id}, Message: {request.message[:50]}...")

        # 获取用户记忆上下文
        # 🔧 修复：使用await调用async方法
        # ✅ P0修复：传递work_id以隔离不同作品的记忆
        user_context = await memory.get_complete_context(
            user_id,
            work_id=request.work_id  # ✅ 传递work_id进行记忆隔离
        )
        memory_context = memory.format_context_for_agent(
            user_id,
            mode="chat",
            work_id=request.work_id  # ✅ 修复：传递work_id避免记忆污染
        )

        # 获取全局共享的 LangGraph Agent（修复记忆功能）
        # 使用全局单例模式，确保MemorySaver在请求间共享
        agent_graph = get_agent_graph()

        # 准备上下文（将记忆上下文加入到请求上下文中）
        context = request.context or {}
        context["memory_context"] = memory_context
        context["user_context"] = user_context

        # 调用 LangGraph Agent 进行对话
        result = await agent_graph.chat(
            message=request.message,
            work_id=request.work_id,
            chapter_id=request.chapter_id,
            conversation_id=conversation_id,
            context=context
        )

        # 记录交互到用户记忆
        memory.record_user_interaction(
            user_id,
            "agent_chat",
            {
                "message": request.message,
                "intent": result["metadata"].get("intent"),
                "conversation_id": conversation_id
            }
        )

        logger.info(
            f"[LangGraph Agent] User {user_id} - Intent: {result['metadata'].get('intent')}, "
            f"Steps: {len(result['agent_steps'])}"
        )

        return AgentChatResponse(
            response=result["response"],
            conversation_id=result["conversation_id"],
            agent_steps=result["agent_steps"],
            suggested_actions=result["suggested_actions"],
            metadata={
                **result["metadata"],
                "memory_quality": user_context.get("user_context", {}).get("memory_quality", "low"),
                "framework": "langgraph"
            }
        )

    except Exception as e:
        logger.error(f"[LangGraph Agent] Error: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Agent对话失败: {str(e)}"
        )


@router.post("/chat/reset", response_model=ResetConversationResponse)
async def reset_conversation(
    request: ResetConversationRequest,
    current_user: User = Depends(get_current_active_user)
):
    """
    重开Session - 清空对话历史，开始全新对话

    功能:
    - 清空当前会话的所有消息历史
    - 删除LangGraph checkpoint数据
    - 生成新的conversation_id

    Args:
        request: 重置请求（包含要重置的conversation_id）
        current_user: 当前用户

    Returns:
        ResetConversationResponse: 包含新的conversation_id
    """
    try:
        user_id = str(current_user.id)
        old_conversation_id = request.conversation_id

        logger.info(f"[Reset Conversation] User: {user_id}, Old Conv ID: {old_conversation_id}")

        # ✅ 验证会话归属
        from app.core.redis import redis_client

        stored_user_id = await redis_client.get(
            f"conversation:{old_conversation_id}:owner"
        )
        if stored_user_id:
            # RedisClient 已自动解码，无需 decode()
            if isinstance(stored_user_id, bytes):
                stored_user_id = stored_user_id.decode('utf-8')
            if stored_user_id != user_id:
                # 会话归属验证失败
                logger.warning(
                    f"[Security] 用户 {user_id} 尝试重置其他用户的会话 {old_conversation_id}"
                )
                raise HTTPException(
                    status_code=403,
                    detail="无权访问此会话"
                )

        # 获取全局Agent实例
        agent_graph = get_agent_graph()

        # 删除LangGraph checkpoint数据
        # AsyncRedisSaver会自动清理对应thread_id的所有checkpoint
        try:
            # 构建config
            config = {
                "configurable": {
                    "thread_id": old_conversation_id
                }
            }

            # 使用AsyncRedisSaver的API删除checkpoint
            # 注意：AsyncRedisSaver可能没有直接的delete方法，
            # 但我们可以通过让checkpoint过期来实现
            # 这里我们只需要生成新的conversation_id，旧的会话会因TTL自动过期

            logger.info(f"[Reset Conversation] Checkpoint将自动过期: {old_conversation_id}")

        except Exception as e:
            logger.warning(f"[Reset Conversation] 删除checkpoint失败（可忽略）: {e}")

        # 生成新的conversation_id
        new_conversation_id = str(uuid.uuid4())

        logger.info(
            f"[Reset Conversation] User {user_id} - "
            f"Old: {old_conversation_id}, New: {new_conversation_id}"
        )

        return ResetConversationResponse(
            new_conversation_id=new_conversation_id,
            message="会话已重置"
        )

    except Exception as e:
        logger.error(f"[Reset Conversation] Error: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"重置会话失败: {str(e)}"
        )


@router.post("/branches", response_model=BranchResponse)
async def create_branch(
    request: CreateBranchRequest,
    current_user: User = Depends(get_current_active_user)
):
    """
    创建对话分支 - 在任意消息点分叉，保留所有历史

    功能:
    - 在指定消息点创建新分支
    - 复制分叉点之前的所有消息到新分支
    - 保留原分支数据（数据不丢失）
    - 支持多条对话路径并存

    分叉点说明:
    - fork_point_message_index 是用户看到的消息索引（从0开始）
    - 当前实现：按checkpoint数量映射（简化实现）
    - 未来优化：解析checkpoint中的实际消息数量

    示例:
    - index=0: 在第1条消息后分叉
    - index=2: 在第3条消息后分叉

    Args:
        request: 创建分支请求
        current_user: 当前用户

    Returns:
        BranchResponse: 新分支信息
    """
    try:
        user_id = str(current_user.id)
        parent_branch_id = request.conversation_id
        fork_point_index = request.fork_point_message_index

        logger.info(
            f"[Create Branch] User: {user_id}, Parent: {parent_branch_id}, "
            f"Fork Point: {fork_point_index}"
        )

        redis_client = get_redis_client()

        # 1. 验证父分支权限（如果父分支有元数据）
        parent_branch_key = f"branch:{parent_branch_id}"
        parent_data_str = redis_client.get(parent_branch_key)

        if parent_data_str:
            # 父分支存在元数据，验证权限
            parent_metadata = json.loads(parent_data_str)
            if parent_metadata.get("user_id") != user_id:
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail="无权访问父分支"
                )
            logger.info(f"[Create Branch] 父分支权限验证通过")
        else:
            # 父分支是原始会话（没有元数据），允许继续
            logger.info(f"[Create Branch] 父分支是原始会话（无元数据）")

        # 2. 获取全局Agent实例
        agent_graph = get_agent_graph()
        checkpointer = agent_graph.checkpointer

        # 3. 获取父分支的所有checkpoint
        parent_config = {
            "configurable": {
                "thread_id": parent_branch_id
            }
        }

        checkpoints_list = []
        async for checkpoint_tuple in checkpointer.alist(parent_config):
            checkpoints_list.append(checkpoint_tuple)

        logger.info(f"[Create Branch] 父分支共有 {len(checkpoints_list)} 个checkpoint")

        if len(checkpoints_list) == 0:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"父分支不存在或无消息历史: {parent_branch_id}"
            )

        # 4. 验证分叉点索引
        # checkpoint是倒序的（最新的在前），我们需要找到对应的checkpoint
        # fork_point_index=0表示第一条消息，对应最后一个checkpoint
        if fork_point_index >= len(checkpoints_list):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"分叉点索引 {fork_point_index} 超出范围（最大: {len(checkpoints_list) - 1}）"
            )

        # 5. 创建新的branch_id
        branch_id = str(uuid.uuid4())
        branch_name = request.branch_name or f"分支-{datetime.now().strftime('%m%d-%H%M')}"

        # 6. 先保存分支元数据到Redis（优先保存元数据，便于失败回滚）
        branch_metadata = {
            "branch_id": branch_id,
            "parent_branch_id": parent_branch_id,
            "branch_name": branch_name,
            "fork_point_index": fork_point_index,
            "message_count": fork_point_index + 1,  # 暂时估算
            "created_at": datetime.now().isoformat(),
            "is_active": False,
            "user_id": user_id
        }

        # 保存分支元数据
        branch_key = f"branch:{branch_id}"
        redis_client.set(
            branch_key,
            json.dumps(branch_metadata, ensure_ascii=False),
            ex=7 * 24 * 60 * 60  # 7天过期
        )

        # 更新会话的branches列表
        conversation_branches_key = f"conversation:{parent_branch_id}:branches"
        redis_client.sadd(conversation_branches_key, branch_id)
        redis_client.expire(conversation_branches_key, 7 * 24 * 60 * 60)

        logger.info(f"[Create Branch] 元数据已保存: {branch_id}")

        # 7. 复制分叉点之前的checkpoint到新分支
        # checkpoints_list是倒序的，我们需要复制从最老到分叉点的所有checkpoint
        # fork_point_index=0 -> 复制最后1个checkpoint（最早的消息）
        # fork_point_index=1 -> 复制最后2个checkpoint
        # ...
        checkpoints_to_copy = list(reversed(checkpoints_list))[: fork_point_index + 1]

        logger.info(f"[Create Branch] 复制 {len(checkpoints_to_copy)} 个checkpoint到新分支")

        # 复制checkpoint到新分支
        for idx, checkpoint_tuple in enumerate(checkpoints_to_copy):
            checkpoint_data = checkpoint_tuple.checkpoint
            metadata = checkpoint_tuple.metadata

            # 从checkpoint_tuple中获取原始config（包含checkpoint_ns等）
            original_config = checkpoint_tuple.config if hasattr(checkpoint_tuple, 'config') else {}

            # 创建新的config，保留checkpoint_ns但更新thread_id
            new_branch_config = {
                "configurable": {
                    "thread_id": branch_id
                }
            }

            # 如果原config有checkpoint_ns，添加到新config
            if "configurable" in original_config and "checkpoint_ns" in original_config["configurable"]:
                new_branch_config["configurable"]["checkpoint_ns"] = original_config["configurable"]["checkpoint_ns"]

            # 获取checkpoint的channel_versions以保持版本一致性
            channel_versions = checkpoint_data.get("channel_versions", {})

            # 保存到新分支（使用位置参数，与langgraph_agent.py保持一致）
            await checkpointer.aput(
                new_branch_config,
                checkpoint_data,
                metadata,
                channel_versions  # 使用正确的版本信息
            )

            logger.debug(f"[Create Branch] 复制checkpoint {idx + 1}/{len(checkpoints_to_copy)}")

        # 8. 更新分支元数据中的实际消息数
        branch_metadata["message_count"] = len(checkpoints_to_copy)
        redis_client.set(
            branch_key,
            json.dumps(branch_metadata, ensure_ascii=False),
            ex=7 * 24 * 60 * 60
        )

        logger.info(
            f"[Create Branch] 创建成功 - Branch ID: {branch_id}, "
            f"Name: {branch_name}, Messages: {len(checkpoints_to_copy)}"
        )

        return BranchResponse(
            branch_id=branch_id,
            parent_branch_id=parent_branch_id,
            branch_name=branch_name,
            fork_point_index=fork_point_index,
            message_count=len(checkpoints_to_copy),
            created_at=branch_metadata["created_at"]
        )

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"[Create Branch] Error: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"创建分支失败: {str(e)}"
        )


@router.post("/branches/{branch_id}/switch", response_model=SwitchBranchResponse)
async def switch_branch(
    branch_id: str,
    current_user: User = Depends(get_current_active_user)
):
    """
    切换到指定分支 - 加载分支的消息历史

    功能:
    - 验证分支存在性
    - 加载分支的所有消息历史
    - 更新活跃分支标记
    - 返回分支消息列表

    Args:
        branch_id: 要切换到的分支ID
        current_user: 当前用户

    Returns:
        SwitchBranchResponse: 分支信息和消息历史
    """
    try:
        user_id = str(current_user.id)

        logger.info(f"[Switch Branch] User: {user_id}, Branch: {branch_id}")

        # 1. 从Redis获取分支元数据
        redis_client = get_redis_client()
        branch_key = f"branch:{branch_id}"
        branch_data_str = redis_client.get(branch_key)

        if not branch_data_str:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"分支不存在: {branch_id}"
            )

        branch_metadata = json.loads(branch_data_str)

        # 验证用户权限
        if branch_metadata.get("user_id") != user_id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="无权访问此分支"
            )

        # 2. 获取分支的所有checkpoint
        agent_graph = get_agent_graph()
        checkpointer = agent_graph.checkpointer

        branch_config = {
            "configurable": {
                "thread_id": branch_id
            }
        }

        checkpoints_list = []
        async for checkpoint_tuple in checkpointer.alist(branch_config):
            checkpoints_list.append(checkpoint_tuple)

        logger.info(f"[Switch Branch] 分支共有 {len(checkpoints_list)} 个checkpoint")

        # 3. 解析checkpoint获取消息历史
        # checkpoint是倒序的（最新的在前），需要反转
        messages = []
        for checkpoint_tuple in reversed(checkpoints_list):
            checkpoint_data = checkpoint_tuple.checkpoint

            # 从checkpoint中提取消息
            # LangGraph的checkpoint包含channel_values，其中有messages
            channel_values = checkpoint_data.get("channel_values", {})
            if "messages" in channel_values:
                # messages是一个列表，每个元素是一条消息
                for msg in channel_values["messages"]:
                    # 兼容dict和对象两种格式
                    if isinstance(msg, dict):
                        message_dict = {
                            "type": msg.get("type", "unknown"),
                            "content": msg.get("content", ""),
                            "name": msg.get("name"),
                            "id": msg.get("id")
                        }
                    else:
                        # 对象格式（使用getattr）
                        message_dict = {
                            "type": getattr(msg, "type", "unknown"),
                            "content": getattr(msg, "content", ""),
                            "name": getattr(msg, "name", None),
                            "id": getattr(msg, "id", None)
                        }
                    messages.append(message_dict)

        # 去重（checkpoint可能有重复的消息）
        seen_ids = set()
        seen_content_hashes = set()  # 用于没有ID的消息
        unique_messages = []

        for msg in messages:
            msg_id = msg.get("id")

            if msg_id:
                # 有ID的消息：基于ID去重
                if msg_id not in seen_ids:
                    seen_ids.add(msg_id)
                    unique_messages.append(msg)
            else:
                # 没有ID的消息：基于内容hash去重
                content_hash = hash((
                    msg.get("type"),
                    msg.get("content"),
                    msg.get("name")
                ))
                if content_hash not in seen_content_hashes:
                    seen_content_hashes.add(content_hash)
                    unique_messages.append(msg)

        # 4. 更新分支的isActive标记（可选，用于UI显示）
        branch_metadata["is_active"] = True
        branch_metadata["last_accessed"] = datetime.now().isoformat()
        redis_client.set(
            branch_key,
            json.dumps(branch_metadata, ensure_ascii=False),
            ex=7 * 24 * 60 * 60
        )

        logger.info(
            f"[Switch Branch] 切换成功 - Branch: {branch_id}, "
            f"Name: {branch_metadata['branch_name']}, Messages: {len(unique_messages)}"
        )

        return SwitchBranchResponse(
            branch_id=branch_id,
            branch_name=branch_metadata["branch_name"],
            message_count=len(unique_messages),
            messages=unique_messages
        )

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"[Switch Branch] Error: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"切换分支失败: {str(e)}"
        )


@router.get("/conversations/{conversation_id}/branches", response_model=GetBranchesResponse)
async def get_conversation_branches(
    conversation_id: str,
    current_user: User = Depends(get_current_active_user)
):
    """
    获取会话的所有分支列表

    功能:
    - 获取会话的所有分支
    - 返回分支元数据（扁平列表）
    - 前端可以根据parent_branch_id构建树形结构

    Args:
        conversation_id: 会话ID（根分支ID）
        current_user: 当前用户

    Returns:
        GetBranchesResponse: 分支列表
    """
    try:
        user_id = str(current_user.id)

        logger.info(f"[Get Branches] User: {user_id}, Conversation: {conversation_id}")

        redis_client = get_redis_client()

        # 1. 获取会话的所有分支ID
        conversation_branches_key = f"conversation:{conversation_id}:branches"
        branch_ids = redis_client.smembers(conversation_branches_key)

        # 将bytes转为str
        if branch_ids:
            branch_ids = [bid.decode('utf-8') if isinstance(bid, bytes) else bid for bid in branch_ids]
        else:
            branch_ids = []

        logger.info(f"[Get Branches] 找到 {len(branch_ids)} 个分支")

        # 2. 批量获取分支元数据（使用Pipeline优化）
        branches_data = []

        if len(branch_ids) > 0:
            pipeline = redis_client.pipeline()
            for branch_id in branch_ids:
                branch_key = f"branch:{branch_id}"
                pipeline.get(branch_key)

            results = pipeline.execute()

            for branch_id, branch_data_str in zip(branch_ids, results):
                if branch_data_str:
                    branch_metadata = json.loads(branch_data_str)

                    # 验证用户权限
                    if branch_metadata.get("user_id") == user_id:
                        branches_data.append(branch_metadata)
                else:
                    logger.warning(f"[Get Branches] 分支元数据缺失: {branch_id}")

        # 3. 构建返回数据（扁平列表，前端自己构建树）
        branch_nodes = []
        for branch_metadata in branches_data:
            node = BranchTreeNode(
                branch_id=branch_metadata["branch_id"],
                parent_branch_id=branch_metadata.get("parent_branch_id"),
                branch_name=branch_metadata["branch_name"],
                message_count=branch_metadata.get("message_count", 0),
                is_active=branch_metadata.get("is_active", False),
                created_at=branch_metadata["created_at"],
                children=[]  # 扁平列表，前端构建树
            )
            branch_nodes.append(node)

        # 4. 添加根分支（主分支）信息（如果还没有）
        # 主分支就是conversation_id本身
        root_exists = any(b.branch_id == conversation_id for b in branch_nodes)
        if not root_exists:
            # 创建虚拟的根分支节点
            root_node = BranchTreeNode(
                branch_id=conversation_id,
                parent_branch_id=None,
                branch_name="主线",
                message_count=0,  # 可以通过checkpoint计算，这里简化
                is_active=True,
                created_at=datetime.now().isoformat(),
                children=[]
            )
            branch_nodes.insert(0, root_node)

        logger.info(
            f"[Get Branches] 返回 {len(branch_nodes)} 个分支 "
            f"(包括根分支: {conversation_id})"
        )

        return GetBranchesResponse(
            conversation_id=conversation_id,
            total_branches=len(branch_nodes),
            branches=branch_nodes
        )

    except Exception as e:
        logger.error(f"[Get Branches] Error: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"获取分支列表失败: {str(e)}"
        )


@router.post("/chat/stream")
async def agent_chat_stream(
    request: AgentChatRequest,
    current_user: User = Depends(get_current_active_user),
    memory: MemoryManager = Depends(get_memory_manager),
    ai_service: HTTPAIService = Depends(get_ai_service),
    # ✅ 修复：移除db依赖，避免生命周期不匹配
    mode: Optional[str] = None  # 新增：支持mode参数（通过查询参数或Body）
):
    """
    Agent 智能对话 - 统一流式响应（SSE）

    支持两种模式：
    - Planning模式（默认）：先规划再执行
    - React模式：边思考边执行

    使用方式：
    1. Planning模式（默认）: 不传mode或mode="planning"
    2. React模式: mode="react"

    Args:
        request: 对话请求
        current_user: 当前用户
        memory: 记忆管理器
        ai_service: AI服务
        db: 数据库会话
        mode: 聊天模式（planning/react，默认planning）

    Returns:
        StreamingResponse: SSE流式响应
    """
    import asyncio

    # 确定使用的模式
    # 优先级：URL查询参数 > Body参数 > 默认planning
    actual_mode = mode or request.mode or ChatMode.PLANNING

    # 字符串转枚举
    if isinstance(actual_mode, str):
        try:
            actual_mode = ChatMode(actual_mode.lower())
        except (ValueError, AttributeError):
            logger.warning(f"[Chat Stream] 无效的mode值: {actual_mode}, 使用默认planning")
            actual_mode = ChatMode.PLANNING

    logger.info(f"[Chat Stream] Mode: {actual_mode}")

    async def event_generator():
        # ✅ 修复：生成器内创建独立db会话，完全控制生命周期
        from app.core.database import create_db_session

        async with create_db_session() as db:
            # 使用队列实现实时事件发送
            import time  # ✅ 在这里导入，整个函数内都可以使用
            event_queue = asyncio.Queue()
            agent_task = None
            result = None

            try:
                user_id = str(current_user.id)
                conversation_id = request.conversation_id or str(uuid.uuid4())

                # ✅ 2025-12-01: 设置请求上下文，让全局Agent的HTTPAIService能追踪成本
                set_request_context(db, user_id)

                # ✅ 会话归属验证（简化版Redis方案）
                from app.core.redis import redis_client

                if request.conversation_id:
                    # 验证现有会话的归属
                    stored_user_id = await redis_client.get(
                        f"conversation:{request.conversation_id}:owner"
                    )
                    if stored_user_id:
                        # RedisClient 已设置 decode_responses=True，返回字符串
                        # 但如果返回的是字节，需要解码
                        if isinstance(stored_user_id, bytes):
                            stored_user_id = stored_user_id.decode('utf-8')
                        if stored_user_id != user_id:
                            # 会话归属验证失败
                            error_event = {
                                'type': 'error',
                                'message': '无权访问此会话',
                                'code': 'UNAUTHORIZED_CONVERSATION'
                            }
                            yield f"data: {json.dumps(error_event, ensure_ascii=False)}\n\n"
                            logger.warning(
                                f"[Security] 用户 {user_id} 尝试访问其他用户的会话 {request.conversation_id}"
                            )
                            return
                else:
                    # 新会话：存储归属关系
                    await redis_client.set(
                        f"conversation:{conversation_id}:owner",
                        user_id,
                        expire=86400 * 30  # 30天过期（修复：ex -> expire）
                    )
                    logger.info(f"[Session] 创建新会话归属: {conversation_id} -> {user_id}")

                logger.info(f"[LangGraph Agent Stream] ⏱️ 请求开始 - User: {user_id}, Mode: {actual_mode}, Message: {request.message[:50]}...")

                # 发送开始事件（包含mode信息）
                start_event = {'type': 'start', 'conversation_id': conversation_id, 'mode': str(actual_mode)}
                yield f"data: {json.dumps(start_event, ensure_ascii=False)}\n\n"

                # ✅ 修复：删除多余的 MemoryManager 调用
                # WritingAgentGraph 内部已有 ContextManager（使用 VectorStore 的语义搜索）
                # 不再需要从 Redis 获取空的会话列表
                # 注释原因：
                # 1. MemoryManager.get_complete_context() 从 Redis 查询会话列表 → 返回0条（Redis里没数据）
                # 2. WritingAgentGraph 已经有 ContextManager → 从 ChromaDB 检索（有数据）
                # 3. 导致重复检索且使用了错误的数据源

                # 获取全局共享的 LangGraph Agent
                agent_graph = get_agent_graph()

                # 准备上下文（创建新dict避免修改原request）
                context = dict(request.context) if request.context else {}

                # ✅ 追踪活动状态（用于发送 activity_complete 事件）
                last_activity_step = {'step': None, 'start_time': None}
                # ✅ 追踪内容是否已通过流式发送（避免重复发送）
                content_sent = {'value': False}

                # 定义回调函数 - 实时放入队列
                async def on_plan(plan_data):
                    """规划生成回调"""
                    await event_queue.put(('plan', plan_data))
                    logger.info(f"[Stream] 规划生成: {len(plan_data.get('tasks', []))} 个任务")

                async def on_task_start(task):
                    """任务开始回调"""
                    await event_queue.put(('task_start', task))
                    logger.info(f"[Stream] 任务开始: {task.get('description')}")

                async def on_task_progress(task, status):
                    """任务进度回调"""
                    await event_queue.put(('task_progress', {'task_id': task.get('task_id'), 'status': status}))

                async def on_task_done(task, result_data):
                    """任务完成回调"""
                    elapsed_time = task.get('elapsed_time', 0)
                    await event_queue.put(('task_done', {
                        'task_id': task.get('task_id'),
                        'description': task.get('description'),
                        'elapsed_time': elapsed_time
                    }))
                    logger.info(f"[Stream] 任务完成: {task.get('description')} ({elapsed_time:.1f}s)")

                async def on_content(chunk):
                    """内容生成回调"""
                    content_sent['value'] = True  # ✅ 标记内容已发送
                    await event_queue.put(('content', chunk))

                # 在后台运行 Agent
                async def run_agent():
                    nonlocal result
                    try:
                        # 根据模式调用不同的方法
                        if actual_mode == ChatMode.REACT:
                            # React模式：使用chat_stream()
                            # 定义React模式的回调
                            async def on_progress_react(event):
                                """进度回调 - 添加activity_complete逻辑"""
                                current_step = event.get('step')

                                # ✅ 如果活动类型改变，发送前一个活动的完成事件
                                if last_activity_step['step'] is not None and last_activity_step['step'] != current_step:
                                    elapsed_time = time.time() - last_activity_step['start_time'] if last_activity_step['start_time'] else 0
                                    await event_queue.put(('activity_complete', {
                                        'step': last_activity_step['step'],
                                        'elapsed_time': elapsed_time
                                    }))
                                    logger.info(f"[Stream] Activity完成: {last_activity_step['step']} ({elapsed_time:.1f}s)")

                                # 更新当前活动
                                last_activity_step['step'] = current_step
                                last_activity_step['start_time'] = time.time()

                                # 发送progress事件
                                await event_queue.put(('progress', event))

                            async def on_tool_call_react(tool_name: str, tool_args: dict):
                                await event_queue.put(('tool_call', {'tool': tool_name, 'args': tool_args}))

                            async def on_content_react(content: str):
                                content_sent['value'] = True  # ✅ 标记内容已发送
                                await event_queue.put(('content', {'content': content}))

                            # ✅ P0-6修复：定义HITL确认请求回调（存储为实例变量，避免序列化）
                            async def on_approval_request(request_data: dict):
                                """确认请求回调 - 编辑器工具需要用户确认"""
                                logger.info(f"[Stream] Approval request: {request_data.get('request_id')}")
                                await event_queue.put(('approval_request', request_data))

                            # ✅ P0-6修复：将回调设置为实例变量，而非添加到context（避免Redis序列化错误）
                            agent_graph._approval_callback = on_approval_request

                            result = await agent_graph.chat_stream(
                                message=request.message,
                                user_id=user_id,  # 新增：传入用户ID
                                work_id=request.work_id,
                                chapter_id=request.chapter_id,
                                conversation_id=conversation_id,
                                context=context,
                                on_progress=on_progress_react,
                                on_tool_call=on_tool_call_react,
                                on_content=on_content_react,
                                db=db  # ✅ 修复：传入生成器的独立db会话
                            )
                        else:
                            # Planning模式：使用chat_with_planning()
                            result = await agent_graph.chat_with_planning(
                                message=request.message,
                                user_id=user_id,
                                work_id=request.work_id,
                                chapter_id=request.chapter_id,
                                conversation_id=conversation_id,
                                context=context,
                                on_plan=on_plan,
                                on_task_start=on_task_start,
                                on_task_progress=on_task_progress,
                                on_task_done=on_task_done,
                                on_content=on_content,
                                db=db
                            )
                        # ✅ 发送最后一个活动的完成事件
                        if last_activity_step['step'] is not None:
                            elapsed_time = time.time() - last_activity_step['start_time'] if last_activity_step['start_time'] else 0
                            await event_queue.put(('activity_complete', {
                                'step': last_activity_step['step'],
                                'elapsed_time': elapsed_time
                            }))
                            logger.info(f"[Stream] 最后活动完成: {last_activity_step['step']} ({elapsed_time:.1f}s)")

                        # Agent 完成后放入结束标记
                        await event_queue.put(('__done__', None))
                    except Exception as e:
                        # Agent执行异常，通过队列发送错误
                        logger.error(f"[Stream] Agent执行失败: {str(e)}", exc_info=True)
                        await event_queue.put(('__error__', {
                            'error': str(e),
                            'error_type': type(e).__name__
                        }))

                # 启动 Agent 任务
                agent_task = asyncio.create_task(run_agent())

                # 实时从队列中取出事件并发送
                while True:
                    event_type, event_data = await event_queue.get()

                    if event_type == '__done__':
                        # Agent 执行完成
                        break

                    if event_type == '__error__':
                        # Agent执行失败
                        error_event = {
                            'type': 'error',
                            'data': event_data,
                            'mode': str(actual_mode)
                        }
                        yield f"data: {json.dumps(error_event, ensure_ascii=False)}\n\n"
                        # 结束流式响应
                        return

                    # 实时发送事件（添加mode标识）
                    event_payload = {
                        'type': event_type,
                        'data': event_data,
                        'mode': str(actual_mode)
                    }
                    # 添加调试日志
                    if event_type == 'progress':
                        logger.info(f"[SSE] 发送 progress 事件: step={event_data.get('step')}, desc={event_data.get('description')}")
                    elif event_type == 'activity_complete':
                        logger.info(f"[SSE] 发送 activity_complete 事件: step={event_data.get('step')}, elapsed={event_data.get('elapsed_time'):.1f}s")
                    yield f"data: {json.dumps(event_payload, ensure_ascii=False)}\n\n"

                # 等待 Agent 任务完成
                await agent_task

                # 检查result是否有效
                if result is None:
                    logger.error(f"[LangGraph Agent Stream] Result is None, Agent可能执行失败")
                    error_event = {
                        'type': 'error',
                        'error': 'Agent执行失败，未返回结果',
                        'mode': str(actual_mode)
                    }
                    yield f"data: {json.dumps(error_event, ensure_ascii=False)}\n\n"
                    return

                # ✅ 修复：只有当内容未通过流式发送时，才在完成前发送final_response
                final_response = result.get("response")
                if final_response and not content_sent['value']:
                    logger.info(f"[Stream] 发送最终响应（内容未流式发送）: {final_response[:100]}...")
                    content_event = {
                        'type': 'content',
                        'data': final_response,
                        'mode': str(actual_mode)
                    }
                    yield f"data: {json.dumps(content_event, ensure_ascii=False)}\n\n"
                elif final_response:
                    logger.info(f"[Stream] 跳过最终响应（内容已流式发送）")

                # 记录交互
                memory.record_user_interaction(
                    user_id,
                    "agent_chat",
                    {
                        "message": request.message,
                        "intent": result.get("metadata", {}).get("intent"),
                        "conversation_id": conversation_id,
                        "mode": str(actual_mode)  # 记录使用的模式
                    }
                )

                # 发送完成事件
                done_event = {
                    'type': 'done',
                    'mode': str(actual_mode),
                    'metadata': result.get('metadata', {}),
                    'suggested_actions': result.get('suggested_actions', [])
                }
                yield f"data: {json.dumps(done_event, ensure_ascii=False)}\n\n"

                logger.info(f"[LangGraph Agent Stream] User {user_id} - Mode: {actual_mode}, Stream completed")

            except Exception as e:
                logger.error(f"[LangGraph Agent Stream] Error: {str(e)}", exc_info=True)
                # 发送错误事件（包含mode标识）
                error_event = {
                    'type': 'error',
                    'error': str(e),
                    'error_type': type(e).__name__,
                    'mode': str(actual_mode)
                }
                yield f"data: {json.dumps(error_event, ensure_ascii=False)}\n\n"
                # 取消 Agent 任务
                if agent_task and not agent_task.done():
                    agent_task.cancel()

    return StreamingResponse(
        event_generator(),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
            "X-Accel-Buffering": "no"  # 禁用 nginx 缓冲
        }
    )


# ==================== 执行计划管理 ====================

@router.post("/plans", response_model=PlanResponse)
async def create_plan(
    request: PlanCreationRequest,
    current_user: User = Depends(get_current_active_user),
    planner: PlanningAgent = Depends(get_planning_agent)
):
    """
    创建执行计划

    根据用户目标自动生成执行计划，支持：
    - 小说创作规划
    - 作品改进规划
    - 自定义规划

    Args:
        request: 计划创建请求
        current_user: 当前用户
        planner: 规划Agent

    Returns:
        PlanResponse: 执行计划
    """
    try:
        logger.info(f"Creating plan - User: {current_user.id}, Goal: {request.goal}")

        # 创建计划
        if "写" in request.goal or "创作" in request.goal:
            plan = planner.create_plan_for_novel_writing(
                user_goal=request.goal,
                genre=request.genre,
                context=request.context
            )
        else:
            # 其他类型的计划
            plan = planner.create_plan_for_novel_writing(
                user_goal=request.goal,
                context=request.context
            )

        return PlanResponse(
            plan_id=plan.plan_id,
            goal=plan.goal,
            tasks=[
                {
                    "task_id": task.task_id,
                    "type": task.task_type.value,
                    "description": task.description,
                    "status": task.status.value,
                    "dependencies": task.dependencies,
                    "priority": task.priority
                }
                for task in plan.tasks
            ],
            status=plan.status,
            progress=plan.progress
        )

    except Exception as e:
        logger.error(f"Create plan error: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"创建计划失败: {str(e)}"
        )


@router.get("/plans/{plan_id}", response_model=PlanResponse)
async def get_plan(
    plan_id: str,
    current_user: User = Depends(get_current_active_user)
):
    """获取执行计划详情"""
    # TODO: 从存储中获取计划
    raise HTTPException(
        status_code=status.HTTP_501_NOT_IMPLEMENTED,
        detail="功能开发中"
    )


# ==================== HITL 批准管理 ====================

@router.get("/approvals/pending", response_model=List[ApprovalResponse])
async def get_pending_approvals(
    current_user: User = Depends(get_current_active_user),
    hitl: HITLManager = Depends(get_hitl_manager)
):
    """
    获取待批准列表

    返回当前用户所有待处理的批准请求

    Args:
        current_user: 当前用户
        hitl: HITL管理器

    Returns:
        List[ApprovalResponse]: 待批准列表
    """
    try:
        user_id = str(current_user.id)
        pending_requests = hitl.get_pending_requests(user_id)

        return [
            ApprovalResponse(
                request_id=req.request_id,
                title=req.title,
                description=req.description,
                proposed_action=req.proposed_action,
                alternatives=req.alternatives,
                status=req.status.value,
                created_at=req.created_at
            )
            for req in pending_requests
        ]

    except Exception as e:
        logger.error(f"Get pending approvals error: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"获取待批准列表失败: {str(e)}"
        )


@router.post("/approvals/{request_id}/action")
async def handle_approval(
    request_id: str,
    action_request: ApprovalActionRequest,
    current_user: User = Depends(get_current_active_user),
    hitl: HITLManager = Depends(get_hitl_manager)
):
    """
    处理批准请求

    支持的操作：
    - approve: 批准
    - reject: 拒绝
    - modify: 修改后批准

    Args:
        request_id: 请求ID
        action_request: 操作请求
        current_user: 当前用户
        hitl: HITL管理器

    Returns:
        操作结果
    """
    try:
        user_id = str(current_user.id)

        if action_request.action == "approve":
            response = hitl.approve_request(
                request_id,
                user_id,
                modifications=action_request.modifications,
                feedback=action_request.feedback
            )
        elif action_request.action == "reject":
            response = hitl.reject_request(
                request_id,
                user_id,
                reason=action_request.feedback
            )
        elif action_request.action == "modify":
            if not action_request.modifications:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="修改操作需要提供modifications"
                )
            response = hitl.modify_and_approve(
                request_id,
                user_id,
                modified_action=action_request.modifications,
                feedback=action_request.feedback
            )
        else:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"不支持的操作: {action_request.action}"
            )

        return {
            "success": True,
            "request_id": request_id,
            "action": action_request.action,
            "status": response.status.value,
            "timestamp": response.timestamp
        }

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Handle approval error: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"处理批准请求失败: {str(e)}"
        )


# ==================== 记忆管理 ====================

@router.get("/memory/context")
async def get_memory_context(
    work_id: Optional[str] = Query(None, description="作品ID，用于获取特定作品的记忆"),
    current_user: User = Depends(get_current_active_user),
    memory: MemoryManager = Depends(get_memory_manager)
):
    """
    获取用户记忆上下文

    返回用户的完整记忆信息，包括：
    - 用户偏好
    - 写作风格
    - 用户画像

    可选参数：
    - work_id: 作品ID，如果提供则只返回该作品的对话记忆

    Args:
        work_id: 作品ID（可选，用于隔离不同作品的记忆）
        current_user: 当前用户
        memory: 记忆管理器

    Returns:
        用户记忆上下文
    """
    try:
        user_id = str(current_user.id)
        # ✅ 修复：添加work_id参数支持
        context = await memory.get_complete_context(user_id, work_id=work_id)

        return {
            "success": True,
            "data": context
        }

    except Exception as e:
        logger.error(f"Get memory context error: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"获取记忆上下文失败: {str(e)}"
        )


@router.post("/memory/preferences")
async def update_preferences(
    preferences: Dict[str, Any],
    current_user: User = Depends(get_current_active_user),
    memory: MemoryManager = Depends(get_memory_manager)
):
    """
    更新用户偏好

    Args:
        preferences: 偏好数据
        current_user: 当前用户
        memory: 记忆管理器

    Returns:
        更新结果
    """
    try:
        user_id = str(current_user.id)

        updated = memory.long_term_memory.update_user_preferences(
            user_id,
            preferences
        )

        return {
            "success": True,
            "data": updated.dict()
        }

    except Exception as e:
        logger.error(f"Update preferences error: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"更新偏好失败: {str(e)}"
        )


# ==================== 辅助函数 ====================
# 注意: 原有的意图检测和处理逻辑已迁移到 LangGraph 框架中
# 详见: app/services/agent/langgraph_agent.py
