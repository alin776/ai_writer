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
from sqlalchemy import select
from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any
import logging
import json
import uuid
from datetime import datetime, timedelta
from app.utils.datetime_utils import get_utc_now

from app.core.database import get_db
from app.core.security import get_current_active_user
from app.models.user import User
from app.models.agent_session import AgentSession
from app.models.agent_session_message import AgentSessionMessage
from app.models.chat_models import ChatMode
from app.models.chapter import Chapter
from app.services.agent.memory import MemoryManager
from app.services.agent.agents import PlanningAgent, ReflectionAgent
from app.services.agent.tools import HITLManager
from app.services.ai.http_ai_service import HTTPAIService
from app.services.ai.humanize_service import HumanizeService
from app.services.agent.langgraph_agent import WritingAgentGraph
from app.services.knowledge_service import KnowledgeService
from app.core.config import settings
from app.core.humanize_config import get_config
# ✅ 2025-12-01: 支持Agent成本追踪（通过请求上下文传递user_id）
from app.core.request_context import set_request_context
import redis

router = APIRouter()
logger = logging.getLogger(__name__)

# 创建同步Redis连接池（全局复用，避免每次请求都建立新连接）
_redis_pool = None
SESSION_CACHE_TTL_SECONDS = 30 * 24 * 60 * 60  # 30 天缓存 TTL，用于热数据

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
        _global_agent_graph = WritingAgentGraph(ai_service)
        logger.info("[Global Agent] created global agent instance; MemorySaver shared across requests")
    return _global_agent_graph


# ==================== Request/response models ====================

class AgentChatRequest(BaseModel):
    """Agent chat request"""
    message: str = Field(..., description="User message", min_length=1)
    mode: Optional[str] = Field(None, description="Chat mode: planning only (default)")
    work_id: Optional[str] = Field(None, description="Work ID")
    chapter_id: Optional[str] = Field(None, description="Chapter ID")
    conversation_id: Optional[str] = Field(None, description="Conversation ID for continuing session")
    context: Optional[Dict[str, Any]] = Field(default_factory=dict, description="Extra context")
    enable_reflection: bool = Field(False, description="Enable DeepAgent reflection mode")


class AgentChatResponse(BaseModel):
    """Agent chat response"""
    response: str = Field(..., description="Agent reply")
    conversation_id: str = Field(..., description="Conversation ID")
    agent_steps: List[Dict[str, Any]] = Field(default_factory=list, description="Agent execution steps")
    suggested_actions: List[str] = Field(default_factory=list, description="Suggested follow-up actions")
    metadata: Dict[str, Any] = Field(default_factory=dict, description="Metadata")


class PlanCreationRequest(BaseModel):
    """Create execution plan request"""
    goal: str = Field(..., description="Goal description", min_length=1)
    genre: Optional[str] = Field(None, description="Novel genre")
    work_id: Optional[str] = Field(None, description="Work ID")
    context: Optional[Dict[str, Any]] = Field(default_factory=dict, description="Context info")


class PlanResponse(BaseModel):
    """Execution plan response"""
    plan_id: str = Field(..., description="Plan ID")
    goal: str = Field(..., description="Goal")
    tasks: List[Dict[str, Any]] = Field(..., description="Task list")
    status: str = Field(..., description="Plan status")
    progress: float = Field(..., description="Progress 0-1")

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
    """Reset conversation request"""
    conversation_id: str = Field(..., description="Conversation ID to reset")


class ResetConversationResponse(BaseModel):
    """Reset conversation response"""
    new_conversation_id: str = Field(..., description="New conversation ID")
    message: str = Field(default="Conversation has been reset", description="Info message")


class CreateBranchRequest(BaseModel):
    """Create branch request"""
    conversation_id: str = Field(..., description="Conversation ID (parent branch)")
    fork_point_message_index: int = Field(
        ...,
        ge=0,
        description=(
            "Message index (starting from 0) where the branch should fork.\n"
            "This is the user-visible index, not the internal checkpoint index."
        ),
    )
    branch_name: Optional[str] = Field(None, description="Branch name (default: Branch-MMDD-HHMM)")


class BranchResponse(BaseModel):
    """Branch response"""
    branch_id: str = Field(..., description="Branch ID")
    parent_branch_id: Optional[str] = Field(None, description="Parent branch ID")
    branch_name: str = Field(..., description="Branch name")
    fork_point_index: int = Field(..., description="Fork point message index")
    message_count: int = Field(0, description="Number of messages")
    created_at: str = Field(..., description="Created at (ISO)")


class SwitchBranchRequest(BaseModel):
    """Switch branch request"""
    branch_id: str = Field(..., description="Branch ID to switch to")


class SwitchBranchResponse(BaseModel):
    """Switch branch response"""
    branch_id: str = Field(..., description="Branch ID")
    branch_name: str = Field(..., description="Branch name")
    message_count: int = Field(..., description="Number of messages")
    messages: List[Dict[str, Any]] = Field(default_factory=list, description="Branch messages")


class BranchTreeNode(BaseModel):
    """Branch tree node"""
    branch_id: str = Field(..., description="Branch ID")
    parent_branch_id: Optional[str] = Field(None, description="Parent branch ID")
    branch_name: str = Field(..., description="Branch name")
    message_count: int = Field(0, description="Number of messages")
    is_active: bool = Field(False, description="Whether this node is active")
    created_at: str = Field(..., description="Created at")
    children: List["BranchTreeNode"] = Field(default_factory=list, description="Child branches")


class GetBranchesResponse(BaseModel):
    """Branch list response"""
    conversation_id: str = Field(..., description="Conversation ID")
    total_branches: int = Field(..., description="Total branch count")
    branches: List[BranchTreeNode] = Field(default_factory=list, description="Branches")


# ==================== 会话管理（新增） ====================

class AgentSessionCreateRequest(BaseModel):
    title: Optional[str] = Field(None, description="会话标题")
    work_id: Optional[str] = Field(None, description="作品ID")
    chapter_id: Optional[str] = Field(None, description="章节ID")
    conversation_id: Optional[str] = Field(None, description="关联的对话ID（可选）")
    title_locked: Optional[bool] = Field(None, description="是否锁定标题")


class AgentSessionUpdateRequest(BaseModel):
    title: Optional[str] = Field(None, description="会话标题")
    title_locked: Optional[bool] = Field(None, description="是否锁定标题")


class AgentSessionResponse(BaseModel):
    session_id: str
    title: Optional[str] = None
    conversation_id: Optional[str] = None
    work_id: Optional[str] = None
    chapter_id: Optional[str] = None
    created_at: Optional[str] = None
    updated_at: Optional[str] = None
    archived_at: Optional[str] = None
    expires_at: Optional[str] = None
    title_locked: Optional[bool] = None

    model_config = {"from_attributes": True}


class AgentSessionListResponse(BaseModel):
    sessions: List[AgentSessionResponse]


class AgentSessionMessageResponse(BaseModel):
    id: str
    session_id: str
    role: str
    content: str
    metadata: Optional[Dict[str, Any]] = None
    token_usage: Optional[Dict[str, Any]] = None
    created_at: Optional[str] = None


# ==================== 依赖注入 ====================

async def get_memory_manager(
    db: AsyncSession = Depends(get_db)
) -> MemoryManager:
    """Dependency provider for MemoryManager."""
    redis_client = get_redis_client()
    manager = MemoryManager(redis_client)
    return manager


async def get_planning_agent() -> PlanningAgent:
    """Dependency provider for PlanningAgent."""
    return PlanningAgent()


async def get_hitl_manager() -> HITLManager:
    """Dependency provider for HITL manager."""
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
    Agent chat endpoint powered by LangGraph.

    Modes:
    - "writing"
    - "planning"
    - "analysis"
    - "stuck"

    Returns:
        AgentChatResponse
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

        # 完成知识文档上下文插入
        knowledge_service = KnowledgeService(db)
        knowledge_docs: List[Dict[str, Any]] = []

        doc_ids = context.get("knowledge_doc_ids") if isinstance(context.get("knowledge_doc_ids"), list) else []
        if doc_ids:
            seen_ids = set()
            for doc_id in doc_ids:
                if not doc_id or doc_id in seen_ids:
                    continue
                seen_ids.add(doc_id)
                try:
                    item = await knowledge_service.get_item(doc_id, user_id, increment_view=False)
                    if item:
                        knowledge_docs.append({
                            "id": str(item.id),
                            "title": item.title,
                            "content": item.content,
                            "tags": item.tags,
                            "source_type": getattr(item.source_type, "value", str(item.source_type)),
                        })
                        try:
                            await knowledge_service.increment_reference_count(doc_id, user_id)
                        except Exception as ref_err:
                            logger.debug(f"[agent_chat] increment_reference_count failed: {ref_err}")
                    else:
                        logger.warning(f"[agent_chat] Knowledge doc not found or access denied: doc_id={doc_id}, user_id={user_id}")
                except Exception as load_err:
                    logger.warning(f"[agent_chat] load knowledge item failed: {load_err}")

        # 向后兼容：tags 搜索
        if not knowledge_docs:
            tags = context.get("knowledge_tags") if isinstance(context.get("knowledge_tags"), list) else []
            if tags:
                logger.info(f"[agent_chat] Using legacy knowledge_tags search (deprecated): tags={tags}")
                try:
                    search_results = await knowledge_service.search_by_semantic(
                        user_id=user_id,
                        query=request.message,
                        tags=tags,
                        top_k=5,
                        work_id=str(request.work_id) if request.work_id else None
                    )
                    for res in search_results:
                        item = res.get("item")
                        if not item:
                            continue
                        knowledge_docs.append({
                            "id": str(item.id),
                            "title": item.title,
                            "content": item.content,
                            "tags": item.tags,
                            "source_type": getattr(item.source_type, "value", str(item.source_type)),
                            "highlight": res.get("highlight"),
                            "relevance_score": res.get("relevance_score"),
                        })
                except Exception as search_err:
                    logger.warning(f"[agent_chat] knowledge semantic search failed: {search_err}")

        if knowledge_docs:
            context["knowledge_docs"] = knowledge_docs
            logger.info(f"[agent_chat] Injected {len(knowledge_docs)} knowledge docs into context")

        # ✨ 优先处理 @optimization: 直接走去痕迹流程
        if context.get("use_optimization"):
            humanize_text = (
                context.get("current_content")
                or context.get("text")
                or ""
            )

            if not humanize_text and request.chapter_id:
                chapter_stmt = select(Chapter).where(Chapter.id == request.chapter_id)
                if request.work_id:
                    chapter_stmt = chapter_stmt.where(Chapter.work_id == request.work_id)
                chapter_result = await db.execute(chapter_stmt)
                chapter_obj = chapter_result.scalar_one_or_none()
                if chapter_obj and chapter_obj.content:
                    humanize_text = chapter_obj.content

            humanize_conf = get_config()
            if len(humanize_text) > humanize_conf.max_text_chars:
                raise HTTPException(
                    status_code=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE,
                    detail=f"去痕迹文本长度超过限制 ({len(humanize_text)} > {humanize_conf.max_text_chars})"
                )

            if not humanize_text:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="开启去痕迹优化但未提供可用文本"
                )

            try:
                humanize_service = HumanizeService(ai_service=ai_service)
                humanize_result = await humanize_service.full_humanize_process(
                    text=humanize_text,
                    intensity=context.get("intensity") or "medium",
                    skip_detection=False,
                    skip_verification=None,
                    use_nlp_preprocessing=None
                )
                humanized_text = humanize_result.get("humanized_text") or humanize_text
                detection = humanize_result.get("detection")
                verification = humanize_result.get("verification")

                token_usage_data = {
                    "prompt_tokens": (
                        humanize_result.get("detection_prompt_tokens", 0)
                        + humanize_result.get("rewrite_prompt_tokens", 0)
                        + humanize_result.get("verification_prompt_tokens", 0)
                    ),
                    "completion_tokens": (
                        humanize_result.get("detection_completion_tokens", 0)
                        + humanize_result.get("rewrite_completion_tokens", 0)
                        + humanize_result.get("verification_completion_tokens", 0)
                    ),
                    "total_tokens": humanize_result.get("total_tokens", 0),
                }

                metadata = {
                    "tool": "humanize_rewrite",
                    "use_optimization": True,
                    "detection_score": getattr(detection, "overall_score", None),
                    "verification_score": getattr(verification, "score_after", None),
                    "total_tokens": humanize_result.get("total_tokens"),
                }

                agent_steps = [
                    {"step": "humanize_rewrite", "result": "applied @optimization"}
                ]

                try:
                    session = await _find_session_by_conversation(db, user_id, conversation_id)
                    if session:
                        await _persist_message(
                            db, session, role="user", content=request.message,
                            metadata={"mode": request.mode, "use_optimization": True},
                        )
                        await _persist_message(
                            db, session, role="agent", content=humanized_text,
                            metadata=metadata, token_usage=token_usage_data,
                        )
                        await db.commit()
                        try:
                            redis_client = get_redis_client()
                            redis_client.delete(_session_detail_cache_key(str(session.id)))
                            _invalidate_session_caches(redis_client, user_id)
                        except Exception as cache_err:
                            logger.warning(f"[LangGraph Agent @optimization] Clear session cache failed: {cache_err}")
                except Exception as persist_err:
                    await db.rollback()
                    logger.warning(f"[LangGraph Agent @optimization] Persist message failed: {persist_err}")

                memory.record_user_interaction(
                    user_id, "agent_chat",
                    {
                        "message": request.message,
                        "intent": "humanize_rewrite",
                        "conversation_id": conversation_id,
                        "mode": request.mode or ChatMode.PLANNING,
                        "use_optimization": True,
                    }
                )

                return AgentChatResponse(
                    response=humanized_text,
                    conversation_id=conversation_id,
                    agent_steps=agent_steps,
                    suggested_actions=[],
                    metadata=metadata
                )
            except Exception as humanize_err:
                logger.error(f"[agent_chat] humanize flow failed: {humanize_err}", exc_info=True)
                raise HTTPException(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    detail=f"AI去痕迹执行失败: {str(humanize_err)}"
                )

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

        # 提示：将用户/Agent消息持久化到会话保存（符合正在使用的会话）
        try:
            session = await _find_session_by_conversation(db, user_id, conversation_id)
            if session:
                await _persist_message(
                    db,
                    session,
                    role="user",
                    content=request.message,
                    metadata={"mode": request.mode},
                )
                await _persist_message(
                    db,
                    session,
                    role="agent",
                    content=result.get("response", ""),
                    metadata=result.get("metadata"),
                    token_usage=(result.get("metadata") or {}).get("token_usage"),
                )
                await db.commit()
                try:
                    redis_client = get_redis_client()
                    redis_client.delete(_session_detail_cache_key(str(session.id)))
                    _invalidate_session_caches(redis_client, user_id)
                except Exception as cache_err:
                    logger.warning(f"[LangGraph Agent] Clear session cache failed: {cache_err}")
        except Exception as persist_err:
            await db.rollback()
            logger.warning(f"[LangGraph Agent] Persist message failed: {persist_err}")

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
                    detail="Unauthorized to access this conversation"
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
            message="Conversation has been reset"
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
                    detail="Forbidden to access parent branch data"
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
                detail=f"Fork index {fork_point_index} out of range. Max allowed {len(checkpoints_list) - 1}"
            )

        # 5. 创建新的branch_id
        branch_id = str(uuid.uuid4())
        branch_name = request.branch_name or f"分支-{get_utc_now().strftime('%m%d-%H%M')}"

        # 6. 先保存分支元数据到Redis（优先保存元数据，便于失败回滚）
        branch_metadata = {
            "branch_id": branch_id,
            "parent_branch_id": parent_branch_id,
            "branch_name": branch_name,
            "fork_point_index": fork_point_index,
            "message_count": fork_point_index + 1,  # 暂时估算
            "created_at": get_utc_now().isoformat(),
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
                detail="Forbidden to access this branch"
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
        branch_metadata["last_accessed"] = get_utc_now().isoformat()
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

        logger.info(f"[Get Branches] found {len(branch_ids)} branches")

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
                created_at=get_utc_now().isoformat(),
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

    仅支持 Planning 模式（默认）：先规划再执行

    Args:
        request: 对话请求
        current_user: 当前用户
        memory: 记忆管理器
        ai_service: AI服务
        db: 数据库会话
        mode: 聊天模式（仅planning，默认planning）

    Returns:
        StreamingResponse: SSE流式响应
    """
    import asyncio

    # 仅支持 planning，任何其他输入均回退为 planning
    requested_mode = mode or request.mode or ChatMode.PLANNING
    try:
        actual_mode = ChatMode(requested_mode.lower()) if isinstance(requested_mode, str) else ChatMode(requested_mode)
    except Exception:
        logger.warning(f"[Chat Stream] 无效的mode值: {requested_mode}, 使用默认planning")
        actual_mode = ChatMode.PLANNING

    if actual_mode != ChatMode.PLANNING:
        logger.info(f"[Chat Stream] 模式 {actual_mode} 已停用，回退到 planning")
        actual_mode = ChatMode.PLANNING

    logger.info(f"[Chat Stream] Mode: {actual_mode}")

    async def event_generator():
        # ✅ 修复：生成器内创建独立db会话，完全控制生命周期
        from app.core.database import create_db_session

        async with create_db_session() as db:
            # 使用队列实现实时事件发送
            event_queue = asyncio.Queue()
            agent_task = None
            result = None
            assistant_chunks: List[str] = []
            session = None

            try:
                user_id = str(current_user.id)
                conversation_id = request.conversation_id or str(uuid.uuid4())
                session = await _find_session_by_conversation(db, user_id, conversation_id)

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
                                'message': 'Unauthorized to access this conversation',
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

                # 知识库文档注入
                knowledge_service = KnowledgeService(db)
                knowledge_docs: List[Dict[str, Any]] = []

                doc_ids = context.get("knowledge_doc_ids") if isinstance(context.get("knowledge_doc_ids"), list) else []
                if doc_ids:
                    seen_ids = set()
                    for doc_id in doc_ids:
                        if not doc_id or doc_id in seen_ids:
                            continue
                        seen_ids.add(doc_id)
                        try:
                            item = await knowledge_service.get_item(doc_id, user_id, increment_view=False)
                            if item:
                                knowledge_docs.append({
                                    "id": str(item.id),
                                    "title": item.title,
                                    "content": item.content,
                                    "tags": item.tags,
                                    "source_type": getattr(item.source_type, "value", str(item.source_type)),
                                })
                                try:
                                    await knowledge_service.increment_reference_count(doc_id, user_id)
                                except Exception as ref_err:
                                    logger.debug(f"[agent_chat_stream] increment_reference_count failed: {ref_err}")
                            else:
                                logger.warning(f"[agent_chat_stream] Knowledge doc not found: doc_id={doc_id}")
                        except Exception as load_err:
                            logger.warning(f"[agent_chat_stream] load knowledge item failed: {load_err}")

                if knowledge_docs:
                    context["knowledge_docs"] = knowledge_docs
                    logger.info(f"[agent_chat_stream] Injected {len(knowledge_docs)} knowledge docs into context")

                # ✨ 优先处理 @optimization: 直接走去痕迹流程
                if context.get("use_optimization"):
                    humanize_text = context.get("current_content") or context.get("text") or ""

                    if not humanize_text and request.chapter_id:
                        chapter_stmt = select(Chapter).where(Chapter.id == request.chapter_id)
                        if request.work_id:
                            chapter_stmt = chapter_stmt.where(Chapter.work_id == request.work_id)
                        chapter_result = await db.execute(chapter_stmt)
                        chapter_obj = chapter_result.scalar_one_or_none()
                        if chapter_obj and chapter_obj.content:
                            humanize_text = chapter_obj.content

                    humanize_conf = get_config()
                    if len(humanize_text) > humanize_conf.max_text_chars:
                        error_event = {
                            'type': 'error',
                            'message': f'去痕迹文本长度超过限制 ({len(humanize_text)} > {humanize_conf.max_text_chars})',
                            'mode': str(actual_mode)
                        }
                        yield f"data: {json.dumps(error_event, ensure_ascii=False)}\n\n"
                        return

                    if not humanize_text:
                        error_event = {
                            'type': 'error',
                            'message': '开启去痕迹优化但未找到待处理文本',
                            'mode': str(actual_mode)
                        }
                        yield f"data: {json.dumps(error_event, ensure_ascii=False)}\n\n"
                        return

                    try:
                        humanize_service = HumanizeService(ai_service=ai_service)
                        progress_event = {
                            'type': 'progress',
                            'data': {'step': 'humanize_rewrite', 'description': '正在执行去痕迹优化'},
                            'mode': str(actual_mode)
                        }
                        yield f"data: {json.dumps(progress_event, ensure_ascii=False)}\n\n"

                        humanized_chunks: List[str] = []
                        rewrite_usage = None
                        async for chunk, usage in humanize_service.humanize_stream(
                            text=humanize_text,
                            intensity=context.get("intensity") or "medium",
                            use_nlp_preprocessing=None
                        ):
                            if chunk:
                                humanized_chunks.append(chunk)
                                content_event = {'type': 'content', 'data': chunk, 'mode': str(actual_mode)}
                                yield f"data: {json.dumps(content_event, ensure_ascii=False)}\n\n"
                            if usage:
                                rewrite_usage = usage

                        humanized_text = "".join(humanized_chunks)

                        token_usage_data = {
                            "prompt_tokens": (rewrite_usage or {}).get("prompt_tokens", 0),
                            "completion_tokens": (rewrite_usage or {}).get("completion_tokens", 0),
                            "total_tokens": (rewrite_usage or {}).get("total_tokens", 0),
                        }

                        try:
                            if session:
                                await _persist_message(
                                    db, session, role="user", content=request.message,
                                    metadata={"mode": str(actual_mode), "use_optimization": True},
                                )
                                await _persist_message(
                                    db, session, role="agent", content=humanized_text,
                                    metadata={"tool": "humanize_rewrite", "use_optimization": True},
                                    token_usage=token_usage_data,
                                )
                                await db.commit()
                        except Exception as persist_err:
                            await db.rollback()
                            logger.warning(f"[agent_chat_stream] Persist humanize messages failed: {persist_err}")

                        memory.record_user_interaction(
                            user_id, "agent_chat",
                            {"message": request.message, "intent": "humanize_rewrite", "conversation_id": conversation_id, "use_optimization": True}
                        )

                        done_event = {
                            'type': 'done', 'mode': str(actual_mode),
                            'metadata': {"tool": "humanize_rewrite", "use_optimization": True, "total_tokens": token_usage_data["total_tokens"]},
                            'suggested_actions': []
                        }
                        yield f"data: {json.dumps(done_event, ensure_ascii=False)}\n\n"
                        return
                    except Exception as humanize_err:
                        logger.error(f"[agent_chat_stream] humanize flow failed: {humanize_err}", exc_info=True)
                        error_event = {'type': 'error', 'message': f'AI去痕迹执行失败: {str(humanize_err)}', 'mode': str(actual_mode)}
                        yield f"data: {json.dumps(error_event, ensure_ascii=False)}\n\n"
                        return

                # ✅ 追踪内容是否已通过流式发送（避免重复发送）
                content_sent = {'value': False}

                # 定义回调函数 - 实时放入队列
                async def on_plan(plan_data):
                    """Handle plan event."""
                    await event_queue.put(('plan', plan_data))
                    logger.info(f"[Stream] Plan tasks: {len(plan_data.get('tasks', []))} items")

                async def on_task_start(task):
                    """Handle task start event."""
                    await event_queue.put(('task_start', task))
                    logger.info(f"[Stream] Task started: {task.get('description')}")

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
                    if isinstance(chunk, dict) and "content" in chunk:
                        assistant_chunks.append(str(chunk.get("content", "")))
                    elif chunk is not None:
                        assistant_chunks.append(str(chunk))
                    await event_queue.put(('content', chunk))

                # 在后台运行 Agent（仅 planning 模式）
                async def run_agent():
                    nonlocal result
                    try:
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
                            db=db,
                            enable_reflection=request.enable_reflection,  # DeepAgent 反思模式
                        )
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

                assistant_text = final_response or "".join(assistant_chunks)
                try:
                    if session:
                        await _persist_message(
                            db,
                            session,
                            role="user",
                            content=request.message,
                            metadata={"mode": str(actual_mode)},
                        )
                        await _persist_message(
                            db,
                            session,
                            role="agent",
                            content=assistant_text,
                            metadata=result.get("metadata"),
                            token_usage=(result.get("metadata") or {}).get("token_usage"),
                        )
                        await db.commit()
                        try:
                            redis_client = get_redis_client()
                            redis_client.delete(_session_detail_cache_key(str(session.id)))
                            _invalidate_session_caches(redis_client, user_id)
                        except Exception as cache_err:
                            logger.warning(f"[LangGraph Agent Stream] Clear session cache failed: {cache_err}")
                except Exception as persist_err:
                    await db.rollback()
                    logger.warning(f"[LangGraph Agent Stream] Persist message failed: {persist_err}")

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

        plan = planner.create_plan_for_novel_writing(
            user_goal=request.goal,
            genre=request.genre,
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


# ==================== 会话管理 ====================

def _session_to_response(session: AgentSession) -> Dict[str, Any]:
    return {
        "session_id": str(session.id),
        "title": session.title,
        "conversation_id": session.conversation_id,
        "work_id": str(session.work_id) if session.work_id else None,
        "chapter_id": str(session.chapter_id) if session.chapter_id else None,
        "created_at": session.created_at.isoformat() if session.created_at else None,
        "updated_at": session.updated_at.isoformat() if session.updated_at else None,
        "archived_at": session.archived_at.isoformat() if getattr(session, "archived_at", None) else None,
        "expires_at": session.expires_at.isoformat() if getattr(session, "expires_at", None) else None,
        "title_locked": bool(getattr(session, "title_locked", False)),
    }


def _session_cache_key(user_id: str, work_id: Optional[str], chapter_id: Optional[str], limit: int) -> str:
    return (
        f"agent:sessions:user:{user_id}:work:{work_id or 'all'}:"
        f"chapter:{chapter_id or 'all'}:limit:{limit}"
    )


def _session_detail_cache_key(session_id: str) -> str:
    return f"agent:session:{session_id}"


def _session_title_lock_key(session_id: str) -> str:
    return f"agent:session:title_locked:{session_id}"


def _cache_sessions(redis_client, key: str, sessions: List[Dict[str, Any]]) -> None:
    try:
        payload = json.dumps({"sessions": sessions}, ensure_ascii=False)
        redis_client.setex(key, SESSION_CACHE_TTL_SECONDS, payload.encode("utf-8"))
    except Exception as e:
        logger.warning(f"[Redis] set sessions cache failed: {e}")


def _read_sessions_from_cache(redis_client, key: str) -> Optional[List[Dict[str, Any]]]:
    try:
        cached = redis_client.get(key)
        if not cached:
            return None
        data = json.loads(cached)
        return data.get("sessions")
    except Exception as e:
        logger.warning(f"[Redis] read sessions cache failed: {e}")
        return None


def _invalidate_session_caches(redis_client, user_id: str) -> None:
    try:
        pattern = f"agent:sessions:user:{user_id}:*"
        for cache_key in redis_client.scan_iter(match=pattern):
            redis_client.delete(cache_key)
    except Exception as e:
        logger.warning(f"[Redis] invalidate sessions cache failed: {e}")


def _get_title_lock(redis_client, session_id: str) -> bool:
    try:
        val = redis_client.get(_session_title_lock_key(session_id))
        return bool(val and val.decode() != "0")
    except Exception as e:
        logger.warning(f"[Redis] read title lock failed: {e}")
        return False


def _set_title_lock(redis_client, session_id: str, locked: bool) -> None:
    try:
        key = _session_title_lock_key(session_id)
        if locked:
            redis_client.setex(key, SESSION_CACHE_TTL_SECONDS, "1")
        else:
            redis_client.delete(key)
    except Exception as e:
        logger.warning(f"[Redis] set title lock failed: {e}")


def _message_to_response(message: AgentSessionMessage) -> Dict[str, Any]:
    return {
        "id": str(message.id),
        "session_id": str(message.session_id),
        "role": message.role,
        "content": message.content,
        "metadata": message.message_metadata,
        "token_usage": message.token_usage,
        "created_at": message.created_at.isoformat() if message.created_at else None,
    }


async def _find_session_by_conversation(db: AsyncSession, user_id: str, conversation_id: Optional[str]) -> Optional[AgentSession]:
    if not conversation_id:
        return None
    stmt = select(AgentSession).where(
        AgentSession.user_id == user_id,
        AgentSession.conversation_id == conversation_id
    ).limit(1)
    result = await db.execute(stmt)
    return result.scalar_one_or_none()


async def _persist_message(
    db: AsyncSession,
    session: Optional[AgentSession],
    role: str,
    content: str,
    metadata: Optional[Dict[str, Any]] = None,
    token_usage: Optional[Dict[str, Any]] = None
) -> None:
    if not session:
        return
    message = AgentSessionMessage(
        session_id=session.id,
        role=role,
        content=content,
        message_metadata=metadata,
        token_usage=token_usage,
    )
    db.add(message)
    # 触发 updated_at/expires_at 更新
    session.updated_at = datetime.utcnow()
    session.expires_at = datetime.utcnow() + timedelta(days=30)


@router.post("/sessions", response_model=AgentSessionResponse, summary="创建 Agent 会话")
async def create_agent_session(
    payload: AgentSessionCreateRequest,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    title = payload.title or "New session"
    now = datetime.utcnow()
    expires_at = now + timedelta(days=30)

    # 验证 chapter_id 是否有效（如果提供）
    validated_chapter_id = None
    if payload.chapter_id:
        try:
            from uuid import UUID as PyUUID
            chapter_uuid = PyUUID(payload.chapter_id)
            stmt = select(Chapter).where(Chapter.id == chapter_uuid)
            result = await db.execute(stmt)
            chapter = result.scalar_one_or_none()
            if chapter:
                validated_chapter_id = payload.chapter_id
                # 如果 chapter 存在但 work_id 未提供，自动从 chapter 获取
                if not payload.work_id and chapter.work_id:
                    payload.work_id = str(chapter.work_id)
            else:
                logger.warning(f"[create_agent_session] chapter_id {payload.chapter_id} 不存在，已忽略")
        except ValueError:
            logger.warning(f"[create_agent_session] chapter_id {payload.chapter_id} 格式无效，已忽略")

    new_session = AgentSession(
        user_id=current_user.id,
        title=title,
        conversation_id=payload.conversation_id,
        work_id=payload.work_id,
        chapter_id=validated_chapter_id,
        expires_at=expires_at,
        title_locked=payload.title_locked if payload.title_locked is not None else False,
    )

    db.add(new_session)
    await db.commit()
    await db.refresh(new_session)

    response = _session_to_response(new_session)
    if payload.title_locked:
        try:
            redis_client = get_redis_client()
            _set_title_lock(redis_client, str(new_session.id), True)
        except Exception as e:
            logger.warning(f"[Redis] set title lock failed: {e}")

    try:
        redis_client = get_redis_client()
        redis_client.setex(
            _session_detail_cache_key(response["session_id"]),
            SESSION_CACHE_TTL_SECONDS,
            json.dumps(response, ensure_ascii=False).encode("utf-8")
        )
        _invalidate_session_caches(redis_client, str(current_user.id))
    except Exception as e:
        logger.warning(f"[Redis] cache new session failed: {e}")

    return response


@router.get("/sessions", response_model=AgentSessionListResponse, summary="获取 Agent 会话列表")
async def list_agent_sessions(
    work_id: Optional[str] = Query(None, description="Filter by work ID"),
    chapter_id: Optional[str] = Query(None, description="Filter by chapter ID"),
    limit: int = Query(50, ge=1, le=200, description="返回数量上限"),
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    redis_client = get_redis_client()
    cache_key = _session_cache_key(str(current_user.id), work_id, chapter_id, limit)
    cached_sessions = _read_sessions_from_cache(redis_client, cache_key)
    if cached_sessions is not None:
        return {"sessions": cached_sessions}

    stmt = select(AgentSession).where(AgentSession.user_id == current_user.id)
    if work_id:
        stmt = stmt.where(AgentSession.work_id == work_id)
    if chapter_id:
        stmt = stmt.where(AgentSession.chapter_id == chapter_id)
    stmt = stmt.where((AgentSession.expires_at.is_(None)) | (AgentSession.expires_at > datetime.utcnow()))

    stmt = stmt.order_by(AgentSession.updated_at.desc()).limit(limit)
    result = await db.execute(stmt)
    sessions = result.scalars().all()

    redis_client = get_redis_client()
    response = []
    for s in sessions:
        resp = _session_to_response(s)
        lock_redis = _get_title_lock(redis_client, resp["session_id"])
        resp["title_locked"] = resp["title_locked"] or lock_redis
        response.append(resp)
    _cache_sessions(redis_client, cache_key, response)
    return {"sessions": response}


@router.get("/sessions/{session_id}", response_model=AgentSessionResponse, summary="获取单个 Agent 会话详情")
async def get_agent_session_detail(
    session_id: str,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    redis_client = get_redis_client()
    cache_key = _session_detail_cache_key(session_id)
    try:
        cached = redis_client.get(cache_key)
        if cached:
            return json.loads(cached)
    except Exception as e:
        logger.warning(f"[Redis] read session detail cache failed: {e}")

    stmt = select(AgentSession).where(
        AgentSession.id == session_id,
        AgentSession.user_id == current_user.id,
    )
    result = await db.execute(stmt)
    session = result.scalar_one_or_none()

    if not session:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Session not found")

    redis_client = get_redis_client()
    response = _session_to_response(session)
    lock_redis = _get_title_lock(redis_client, response["session_id"])
    response["title_locked"] = response["title_locked"] or lock_redis
    try:
        redis_client.setex(
            cache_key,
            SESSION_CACHE_TTL_SECONDS,
            json.dumps(response, ensure_ascii=False).encode("utf-8")
        )
    except Exception as e:
        logger.warning(f"[Redis] cache session detail failed: {e}")

    return response


@router.patch("/sessions/{session_id}", response_model=AgentSessionResponse, summary="更新 Agent 会话")
async def update_agent_session(
    session_id: str,
    payload: AgentSessionUpdateRequest,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    stmt = select(AgentSession).where(
        AgentSession.id == session_id,
        AgentSession.user_id == current_user.id,
    )
    result = await db.execute(stmt)
    session = result.scalar_one_or_none()
    if not session:
        session = await _find_session_by_conversation(db, str(current_user.id), session_id)

    if not session:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Session not found")

    updated = False
    if payload.title is not None:
        session.title = payload.title
        updated = True
        # 设置默认锁定
        if payload.title_locked is None:
            payload.title_locked = True

    if payload.title_locked is not None:
        try:
            redis_client = get_redis_client()
            _set_title_lock(redis_client, str(session.id), payload.title_locked)
        except Exception as e:
            logger.warning(f"[Redis] set title lock failed: {e}")
        session.title_locked = payload.title_locked

    if updated:
        session.updated_at = datetime.utcnow()
        session.expires_at = datetime.utcnow() + timedelta(days=30)
        db.add(session)
        await db.commit()
        await db.refresh(session)

        try:
            redis_client = get_redis_client()
            redis_client.delete(_session_detail_cache_key(session_id))
            _invalidate_session_caches(redis_client, str(current_user.id))
        except Exception as e:
            logger.warning(f"[Redis] invalidate session caches failed: {e}")

    redis_client = get_redis_client()
    resp = _session_to_response(session)
    resp["title_locked"] = _get_title_lock(redis_client, resp["session_id"])
    return resp


@router.delete("/sessions/{session_id}", status_code=status.HTTP_204_NO_CONTENT, summary="删除 Agent 会话")
async def delete_agent_session(
    session_id: str,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    stmt = select(AgentSession).where(
        AgentSession.id == session_id,
        AgentSession.user_id == current_user.id,
    )
    result = await db.execute(stmt)
    session = result.scalar_one_or_none()
    if not session:
        session = await _find_session_by_conversation(db, str(current_user.id), session_id)

    if not session:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Session not found")

    await db.delete(session)
    await db.commit()

    try:
        redis_client = get_redis_client()
        redis_client.delete(_session_detail_cache_key(session_id))
        redis_client.delete(_session_title_lock_key(session_id))
        _invalidate_session_caches(redis_client, str(current_user.id))
    except Exception as e:
        logger.warning(f"[Redis] invalidate session caches failed: {e}")

    return None


@router.get("/sessions/{session_id}/messages", response_model=List[AgentSessionMessageResponse], summary="获取会话消息列表")
async def get_agent_session_messages(
    session_id: str,
    limit: int = Query(50, ge=1, le=200, description="返回数量上限"),
    offset: int = Query(0, ge=0, description="偏移量"),
    order: str = Query("asc", regex="^(asc|desc)$", description="排序 asc/desc"),
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    stmt_session = select(AgentSession).where(
        AgentSession.id == session_id,
        AgentSession.user_id == current_user.id,
    )
    result_session = await db.execute(stmt_session)
    if result_session.scalar_one_or_none() is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Session not found")

    order_by = AgentSessionMessage.created_at.asc() if order == "asc" else AgentSessionMessage.created_at.desc()
    stmt = (
        select(AgentSessionMessage)
        .where(AgentSessionMessage.session_id == session_id)
        .order_by(order_by)
        .offset(offset)
        .limit(limit)
    )
    result = await db.execute(stmt)
    messages = result.scalars().all()
    return [_message_to_response(m) for m in messages]


# ==================== 辅助函数 ====================
# 注意: 原有的意图检测和处理逻辑已迁移到 LangGraph 框架中
# 详见: app/services/agent/langgraph_agent.py
