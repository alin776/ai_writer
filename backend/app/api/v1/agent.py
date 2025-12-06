"""
Agent 鏅鸿兘鍔╂墜 API 璺敱

鎻愪緵 Agent 鐩稿叧鐨?RESTful API 鎺ュ彛锛屽寘鎷細
- Agent 瀵硅瘽锛堟敮鎸佹祦寮忓搷搴旓級
- 浜烘満鍗忓悓锛圚ITL锛夋壒鍑嗙鐞?
- 鎵ц璁″垝绠＄悊
- 璁板繂绠＄悊
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
from app.models.agent_session_message import AgentSessionMessage
from app.models.chat_models import ChatMode, ChatRequest as UnifiedChatRequest, format_react_event_to_sse, format_planning_event_to_sse, format_error_event
from app.services.agent.memory import MemoryManager
from app.services.agent.agents import PlanningAgent, ReflectionAgent
from app.services.agent.tools import HITLManager
from app.services.ai.http_ai_service import HTTPAIService
from app.services.agent.langgraph_agent import WritingAgentGraph
from app.services.knowledge_service import KnowledgeService
from app.core.config import settings
# ✅ 2025-12-01: 支持Agent成本追踪（通过请求上下文传递user_id）
from app.core.request_context import set_request_context
import redis

router = APIRouter()
logger = logging.getLogger(__name__)

# 鍒涘缓鍚屾Redis杩炴帴姹狅紙鍏ㄥ眬澶嶇敤锛岄伩鍏嶆瘡娆¤姹傞兘寤虹珛鏂拌繛鎺ワ級
_redis_pool = None
SESSION_CACHE_TTL_SECONDS = 30 * 24 * 60 * 60  # 30 澶╃紦瀛?TTL锛岀敤浜庣儹鏁版嵁

def get_redis_client():
    """鑾峰彇鍚屾Redis瀹㈡埛绔紙浣跨敤杩炴帴姹狅級"""
    global _redis_pool

    # 馃敡 淇锛氫娇鐢ㄥ叏灞€杩炴帴姹狅紝閬垮厤姣忔閮藉垱寤烘柊杩炴帴
    if _redis_pool is None:
        _redis_pool = redis.ConnectionPool(
            host='localhost',
            port=6379,
            db=1,  # 浣跨敤db1锛岄伩鍏嶄笌缂撳瓨鏈嶅姟鍐茬獊
            decode_responses=False,
            max_connections=10,  # 鏈€澶ц繛鎺ユ暟
            socket_connect_timeout=5,  # 杩炴帴瓒呮椂5绉?
            socket_timeout=5,  # 鎿嶄綔瓒呮椂5绉?
        )
        logger.info("[Redis] 鍏ㄥ眬杩炴帴姹犲凡鍒涘缓")

    return redis.Redis(connection_pool=_redis_pool)

# 鍏ㄥ眬Agent瀹炰緥锛堣法璇锋眰鍏变韩锛屼繚鎸丮emorySaver鎸佷箙鍖栵級
_global_agent_graph = None

def get_agent_graph() -> WritingAgentGraph:
    """
    鑾峰彇鍏ㄥ眬鍏变韩鐨凙gent瀹炰緥

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
        # 鍒涘缓Agent瀹炰緥锛堝彧鍒涘缓涓€娆★級
        _global_agent_graph = WritingAgentGraph(ai_service, use_chatgpt=settings.AGENT_USE_CHATGPT)
        logger.info("[Global Agent] created global agent instance; MemorySaver shared across requests")
    return _global_agent_graph


# ==================== Request/response models ====================

class AgentChatRequest(BaseModel):
    """Agent chat request"""
    message: str = Field(..., description="User message", min_length=1)
    mode: Optional[str] = Field(None, description="Chat mode: planning/react (default planning)")
    work_id: Optional[str] = Field(None, description="Work ID")
    chapter_id: Optional[str] = Field(None, description="Chapter ID")
    conversation_id: Optional[str] = Field(None, description="Conversation ID for continuing session")
    context: Optional[Dict[str, Any]] = Field(default_factory=dict, description="Extra context")


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
    """鎵瑰噯鎿嶄綔璇锋眰"""
    action: str = Field(..., description="鎿嶄綔绫诲瀷: approve/reject/modify")
    modifications: Optional[Dict[str, Any]] = Field(None, description="淇敼鍐呭锛坅ction=modify鏃讹級")
    feedback: Optional[str] = Field(None, description="鍙嶉璇存槑")


class ApprovalResponse(BaseModel):
    """鎵瑰噯鍝嶅簲"""
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

# ==================== Request/response models ====================

class AgentChatRequest(BaseModel):
    """Agent chat request"""
    message: str = Field(..., description="User message", min_length=1)
    mode: Optional[str] = Field(None, description="Chat mode: planning/react (default planning)")
    work_id: Optional[str] = Field(None, description="Work ID")
    chapter_id: Optional[str] = Field(None, description="Chapter ID")
    conversation_id: Optional[str] = Field(None, description="Conversation ID for continuing session")
    context: Optional[Dict[str, Any]] = Field(default_factory=dict, description="Extra context")


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
    """鎵瑰噯鎿嶄綔璇锋眰"""
    action: str = Field(..., description="鎿嶄綔绫诲瀷: approve/reject/modify")
    modifications: Optional[Dict[str, Any]] = Field(None, description="淇敼鍐呭锛坅ction=modify鏃讹級")
    feedback: Optional[str] = Field(None, description="鍙嶉璇存槑")


class ApprovalResponse(BaseModel):
    """鎵瑰噯鍝嶅簲"""
    request_id: str
    title: str
    description: str
    proposed_action: Dict[str, Any]
    alternatives: List[Dict[str, Any]]
    status: str
    created_at: str


# ==================== 浼氳瘽绠＄悊锛堟柊澧烇級 ====================

class AgentSessionCreateRequest(BaseModel):
    title: Optional[str] = Field(None, description="浼氳瘽鏍囬")
    work_id: Optional[str] = Field(None, description="浣滃搧ID")
    chapter_id: Optional[str] = Field(None, description="绔犺妭ID")
    conversation_id: Optional[str] = Field(None, description="鍏宠仈鐨勫璇滻D锛堝彲閫夛級")
    title_locked: Optional[bool] = Field(None, description="鏄惁閿佸畾鏍囬")


class AgentSessionUpdateRequest(BaseModel):
    title: Optional[str] = Field(None, description="浼氳瘽鏍囬")
    title_locked: Optional[bool] = Field(None, description="鏄惁閿佸畾鏍囬")


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


# ==================== 渚濊禆娉ㄥ叆 ====================

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


# ==================== Agent 瀵硅瘽鎺ュ彛 ====================

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

        # 鑾峰彇鐢ㄦ埛璁板繂涓婁笅鏂?
        # 馃敡 淇锛氫娇鐢╝wait璋冪敤async鏂规硶
        # 鉁?P0淇锛氫紶閫抴ork_id浠ラ殧绂讳笉鍚屼綔鍝佺殑璁板繂
        user_context = await memory.get_complete_context(
            user_id,
            work_id=request.work_id  # 鉁?浼犻€抴ork_id杩涜璁板繂闅旂
        )
        memory_context = memory.format_context_for_agent(
            user_id,
            mode="chat",
            work_id=request.work_id  # 鉁?淇锛氫紶閫抴ork_id閬垮厤璁板繂姹℃煋
        )

        # 鑾峰彇鍏ㄥ眬鍏变韩鐨?LangGraph Agent锛堜慨澶嶈蹇嗗姛鑳斤級
        # 浣跨敤鍏ㄥ眬鍗曚緥妯″紡锛岀‘淇滿emorySaver鍦ㄨ姹傞棿鍏变韩
        agent_graph = get_agent_graph()

        # 鍑嗗涓婁笅鏂囷紙灏嗚蹇嗕笂涓嬫枃鍔犲叆鍒拌姹備笂涓嬫枃涓級
        context = request.context or {}
        context["memory_context"] = memory_context
        context["user_context"] = user_context

        # 瀹屾垚鐭ヨ瘑鏂囨湰涓婁笅鏂囨彃鍏?鍏堝憡璇ュ寘鎷姹備腑鐭ヨ瘑ID锛屽綋鏈夎淇℃伅鏃堕€氳繃API鍙栨湰鏂囩幆澧冿紙闃叉粡AI鍑哄敖锛?
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
                        # 文档不存在或无权限访问
                        logger.warning(f"[agent_chat] Knowledge doc not found or access denied: doc_id={doc_id}, user_id={user_id}")
                except Exception as load_err:
                    logger.warning(f"[agent_chat] load knowledge item failed: {load_err}")

        # ===== 向后兼容：tags 搜索（仅在旧前端调用时触发，计划在后续版本移除）=====
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
                # 语义检索为空时，退化为按标签的数据库过滤
                if not knowledge_docs:
                    try:
                        items, _ = await knowledge_service.get_items(
                            user_id=user_id,
                            tags=tags,
                            work_id=request.work_id
                        )
                        for item in items[:3]:
                            knowledge_docs.append({
                                "id": str(item.id),
                                "title": item.title,
                                "content": item.content,
                                "tags": item.tags,
                                "source_type": getattr(item.source_type, "value", str(item.source_type)),
                            })
                    except Exception as list_err:
                        logger.warning(f"[agent_chat] fallback tag filter failed: {list_err}")

        # 标签检索为空时，降级为不带标签的语义检索（避免因无标签/标签不匹配导致0结果）
        if not knowledge_docs:
            try:
                search_results = await knowledge_service.search_by_semantic(
                    user_id=user_id,
                    query=request.message,
                    tags=None,
                    top_k=3,
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
                logger.warning(f"[agent_chat] fallback knowledge semantic search failed: {search_err}")

        if knowledge_docs:
            context["knowledge_docs"] = knowledge_docs
            logger.info(f"[agent_chat] Injected {len(knowledge_docs)} knowledge docs into context")

        # 璋冪敤 LangGraph Agent 杩涜瀵硅瘽
        result = await agent_graph.chat(
            message=request.message,
            work_id=request.work_id,
            chapter_id=request.chapter_id,
            conversation_id=conversation_id,
            context=context
        )

        # 璁板綍浜や簰鍒扮敤鎴疯蹇?
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

        # æç¤ºï¼šå°†ç”¨æˆ·/Agentæ¶ˆæ¯æŒä¹…åŒ–åˆ°ä¼šè¯ä¿å­˜ï¼ˆç¬¦åˆæ­£åœ¨ä½¿ç”¨çš„ä¼šè¯ï¼‰
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
            detail=f"Agent瀵硅瘽澶辫触: {str(e)}"
        )


@router.post("/chat/reset", response_model=ResetConversationResponse)
async def reset_conversation(
    request: ResetConversationRequest,
    current_user: User = Depends(get_current_active_user)
):
    """
    閲嶅紑Session - 娓呯┖瀵硅瘽鍘嗗彶锛屽紑濮嬪叏鏂板璇?

    鍔熻兘:
    - 娓呯┖褰撳墠浼氳瘽鐨勬墍鏈夋秷鎭巻鍙?
    - 鍒犻櫎LangGraph checkpoint鏁版嵁
    - 鐢熸垚鏂扮殑conversation_id

    Args:
        request: 閲嶇疆璇锋眰锛堝寘鍚閲嶇疆鐨刢onversation_id锛?
        current_user: 褰撳墠鐢ㄦ埛

    Returns:
        ResetConversationResponse: 鍖呭惈鏂扮殑conversation_id
    """
    try:
        user_id = str(current_user.id)
        old_conversation_id = request.conversation_id

        logger.info(f"[Reset Conversation] User: {user_id}, Old Conv ID: {old_conversation_id}")

        # 鉁?楠岃瘉浼氳瘽褰掑睘
        from app.core.redis import redis_client

        stored_user_id = await redis_client.get(
            f"conversation:{old_conversation_id}:owner"
        )
        if stored_user_id:
            # RedisClient 宸茶嚜鍔ㄨВ鐮侊紝鏃犻渶 decode()
            if isinstance(stored_user_id, bytes):
                stored_user_id = stored_user_id.decode('utf-8')
            if stored_user_id != user_id:
                # 浼氳瘽褰掑睘楠岃瘉澶辫触
                logger.warning(
                    f"[Security] 鐢ㄦ埛 {user_id} 灏濊瘯閲嶇疆鍏朵粬鐢ㄦ埛鐨勪細璇?{old_conversation_id}"
                )
                raise HTTPException(
                    status_code=403,
                    detail="Unauthorized to access this conversation"
                )

        # 鑾峰彇鍏ㄥ眬Agent瀹炰緥
        agent_graph = get_agent_graph()

        # 鍒犻櫎LangGraph checkpoint鏁版嵁
        # AsyncRedisSaver浼氳嚜鍔ㄦ竻鐞嗗搴攖hread_id鐨勬墍鏈塩heckpoint
        try:
            # 鏋勫缓config
            config = {
                "configurable": {
                    "thread_id": old_conversation_id
                }
            }

            # 浣跨敤AsyncRedisSaver鐨凙PI鍒犻櫎checkpoint
            # 娉ㄦ剰锛欰syncRedisSaver鍙兘娌℃湁鐩存帴鐨刣elete鏂规硶锛?
            # 浣嗘垜浠彲浠ラ€氳繃璁ヽheckpoint杩囨湡鏉ュ疄鐜?
            # 杩欓噷鎴戜滑鍙渶瑕佺敓鎴愭柊鐨刢onversation_id锛屾棫鐨勪細璇濅細鍥燭TL鑷姩杩囨湡

            logger.info(f"[Reset Conversation] Checkpoint灏嗚嚜鍔ㄨ繃鏈? {old_conversation_id}")

        except Exception as e:
            logger.warning(f"[Reset Conversation] 鍒犻櫎checkpoint澶辫触锛堝彲蹇界暐锛? {e}")

        # 鐢熸垚鏂扮殑conversation_id
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
            detail=f"閲嶇疆浼氳瘽澶辫触: {str(e)}"
        )


@router.post("/branches", response_model=BranchResponse)
async def create_branch(
    request: CreateBranchRequest,
    current_user: User = Depends(get_current_active_user)
):
    """
    鍒涘缓瀵硅瘽鍒嗘敮 - 鍦ㄤ换鎰忔秷鎭偣鍒嗗弶锛屼繚鐣欐墍鏈夊巻鍙?

    鍔熻兘:
    - 鍦ㄦ寚瀹氭秷鎭偣鍒涘缓鏂板垎鏀?
    - 澶嶅埗鍒嗗弶鐐逛箣鍓嶇殑鎵€鏈夋秷鎭埌鏂板垎鏀?
    - 淇濈暀鍘熷垎鏀暟鎹紙鏁版嵁涓嶄涪澶憋級
    - 鏀寔澶氭潯瀵硅瘽璺緞骞跺瓨

    鍒嗗弶鐐硅鏄?
    - fork_point_message_index 鏄敤鎴风湅鍒扮殑娑堟伅绱㈠紩锛堜粠0寮€濮嬶級
    - 褰撳墠瀹炵幇锛氭寜checkpoint鏁伴噺鏄犲皠锛堢畝鍖栧疄鐜帮級
    - 鏈潵浼樺寲锛氳В鏋恈heckpoint涓殑瀹為檯娑堟伅鏁伴噺

    绀轰緥:
    - index=0: 鍦ㄧ1鏉℃秷鎭悗鍒嗗弶
    - index=2: 鍦ㄧ3鏉℃秷鎭悗鍒嗗弶

    Args:
        request: 鍒涘缓鍒嗘敮璇锋眰
        current_user: 褰撳墠鐢ㄦ埛

    Returns:
        BranchResponse: 鏂板垎鏀俊鎭?
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

        # 1. 楠岃瘉鐖跺垎鏀潈闄愶紙濡傛灉鐖跺垎鏀湁鍏冩暟鎹級
        parent_branch_key = f"branch:{parent_branch_id}"
        parent_data_str = redis_client.get(parent_branch_key)

        if parent_data_str:
            # 鐖跺垎鏀瓨鍦ㄥ厓鏁版嵁锛岄獙璇佹潈闄?
            parent_metadata = json.loads(parent_data_str)
            if parent_metadata.get("user_id") != user_id:
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail="Forbidden to access parent branch data"
                )
            logger.info(f"[Create Branch] 鐖跺垎鏀潈闄愰獙璇侀€氳繃")
        else:
            # 鐖跺垎鏀槸鍘熷浼氳瘽锛堟病鏈夊厓鏁版嵁锛夛紝鍏佽缁х画
            logger.info(f"[Create Branch] 鐖跺垎鏀槸鍘熷浼氳瘽锛堟棤鍏冩暟鎹級")

        # 2. 鑾峰彇鍏ㄥ眬Agent瀹炰緥
        agent_graph = get_agent_graph()
        checkpointer = agent_graph.checkpointer

        # 3. 鑾峰彇鐖跺垎鏀殑鎵€鏈塩heckpoint
        parent_config = {
            "configurable": {
                "thread_id": parent_branch_id
            }
        }

        checkpoints_list = []
        async for checkpoint_tuple in checkpointer.alist(parent_config):
            checkpoints_list.append(checkpoint_tuple)

        logger.info(f"[Create Branch] 鐖跺垎鏀叡鏈?{len(checkpoints_list)} 涓猚heckpoint")

        if len(checkpoints_list) == 0:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"鐖跺垎鏀笉瀛樺湪鎴栨棤娑堟伅鍘嗗彶: {parent_branch_id}"
            )

        # 4. 楠岃瘉鍒嗗弶鐐圭储寮?
        # checkpoint鏄€掑簭鐨勶紙鏈€鏂扮殑鍦ㄥ墠锛夛紝鎴戜滑闇€瑕佹壘鍒板搴旂殑checkpoint
        # fork_point_index=0琛ㄧず绗竴鏉℃秷鎭紝瀵瑰簲鏈€鍚庝竴涓猚heckpoint
        if fork_point_index >= len(checkpoints_list):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Fork index {fork_point_index} out of range. Max allowed {len(checkpoints_list) - 1}"
            )

        # 5. 鍒涘缓鏂扮殑branch_id
        branch_id = str(uuid.uuid4())
        branch_name = request.branch_name or f"分支-{get_utc_now().strftime('%m%d-%H%M')}"

        # 6. 鍏堜繚瀛樺垎鏀厓鏁版嵁鍒癛edis锛堜紭鍏堜繚瀛樺厓鏁版嵁锛屼究浜庡け璐ュ洖婊氾級
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

        # 淇濆瓨鍒嗘敮鍏冩暟鎹?
        branch_key = f"branch:{branch_id}"
        redis_client.set(
            branch_key,
            json.dumps(branch_metadata, ensure_ascii=False),
            ex=7 * 24 * 60 * 60  # 7澶╄繃鏈?
        )

        # 鏇存柊浼氳瘽鐨刡ranches鍒楄〃
        conversation_branches_key = f"conversation:{parent_branch_id}:branches"
        redis_client.sadd(conversation_branches_key, branch_id)
        redis_client.expire(conversation_branches_key, 7 * 24 * 60 * 60)

        logger.info(f"[Create Branch] 鍏冩暟鎹凡淇濆瓨: {branch_id}")

        # 7. 澶嶅埗鍒嗗弶鐐逛箣鍓嶇殑checkpoint鍒版柊鍒嗘敮
        # checkpoints_list鏄€掑簭鐨勶紝鎴戜滑闇€瑕佸鍒朵粠鏈€鑰佸埌鍒嗗弶鐐圭殑鎵€鏈塩heckpoint
        # fork_point_index=0 -> 澶嶅埗鏈€鍚?涓猚heckpoint锛堟渶鏃╃殑娑堟伅锛?
        # fork_point_index=1 -> 澶嶅埗鏈€鍚?涓猚heckpoint
        # ...
        checkpoints_to_copy = list(reversed(checkpoints_list))[: fork_point_index + 1]

        logger.info(f"[Create Branch] 澶嶅埗 {len(checkpoints_to_copy)} 涓猚heckpoint鍒版柊鍒嗘敮")

        # 澶嶅埗checkpoint鍒版柊鍒嗘敮
        for idx, checkpoint_tuple in enumerate(checkpoints_to_copy):
            checkpoint_data = checkpoint_tuple.checkpoint
            metadata = checkpoint_tuple.metadata

            # 浠巆heckpoint_tuple涓幏鍙栧師濮媍onfig锛堝寘鍚玞heckpoint_ns绛夛級
            original_config = checkpoint_tuple.config if hasattr(checkpoint_tuple, 'config') else {}

            # 鍒涘缓鏂扮殑config锛屼繚鐣檆heckpoint_ns浣嗘洿鏂皌hread_id
            new_branch_config = {
                "configurable": {
                    "thread_id": branch_id
                }
            }

            # 濡傛灉鍘焎onfig鏈塩heckpoint_ns锛屾坊鍔犲埌鏂癱onfig
            if "configurable" in original_config and "checkpoint_ns" in original_config["configurable"]:
                new_branch_config["configurable"]["checkpoint_ns"] = original_config["configurable"]["checkpoint_ns"]

            # 鑾峰彇checkpoint鐨刢hannel_versions浠ヤ繚鎸佺増鏈竴鑷存€?
            channel_versions = checkpoint_data.get("channel_versions", {})

            # 淇濆瓨鍒版柊鍒嗘敮锛堜娇鐢ㄤ綅缃弬鏁帮紝涓巐anggraph_agent.py淇濇寔涓€鑷达級
            await checkpointer.aput(
                new_branch_config,
                checkpoint_data,
                metadata,
                channel_versions  # 浣跨敤姝ｇ‘鐨勭増鏈俊鎭?
            )

            logger.debug(f"[Create Branch] 澶嶅埗checkpoint {idx + 1}/{len(checkpoints_to_copy)}")

        # 8. 鏇存柊鍒嗘敮鍏冩暟鎹腑鐨勫疄闄呮秷鎭暟
        branch_metadata["message_count"] = len(checkpoints_to_copy)
        redis_client.set(
            branch_key,
            json.dumps(branch_metadata, ensure_ascii=False),
            ex=7 * 24 * 60 * 60
        )

        logger.info(
            f"[Create Branch] 鍒涘缓鎴愬姛 - Branch ID: {branch_id}, "
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
            detail=f"鍒涘缓鍒嗘敮澶辫触: {str(e)}"
        )


@router.post("/branches/{branch_id}/switch", response_model=SwitchBranchResponse)
async def switch_branch(
    branch_id: str,
    current_user: User = Depends(get_current_active_user)
):
    """
    鍒囨崲鍒版寚瀹氬垎鏀?- 鍔犺浇鍒嗘敮鐨勬秷鎭巻鍙?

    鍔熻兘:
    - 楠岃瘉鍒嗘敮瀛樺湪鎬?
    - 鍔犺浇鍒嗘敮鐨勬墍鏈夋秷鎭巻鍙?
    - 鏇存柊娲昏穬鍒嗘敮鏍囪
    - 杩斿洖鍒嗘敮娑堟伅鍒楄〃

    Args:
        branch_id: 瑕佸垏鎹㈠埌鐨勫垎鏀疘D
        current_user: 褰撳墠鐢ㄦ埛

    Returns:
        SwitchBranchResponse: 鍒嗘敮淇℃伅鍜屾秷鎭巻鍙?
    """
    try:
        user_id = str(current_user.id)

        logger.info(f"[Switch Branch] User: {user_id}, Branch: {branch_id}")

        # 1. 浠嶳edis鑾峰彇鍒嗘敮鍏冩暟鎹?
        redis_client = get_redis_client()
        branch_key = f"branch:{branch_id}"
        branch_data_str = redis_client.get(branch_key)

        if not branch_data_str:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"鍒嗘敮涓嶅瓨鍦? {branch_id}"
            )

        branch_metadata = json.loads(branch_data_str)

        # 楠岃瘉鐢ㄦ埛鏉冮檺
        if branch_metadata.get("user_id") != user_id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Forbidden to access this branch"
            )

        # 2. 鑾峰彇鍒嗘敮鐨勬墍鏈塩heckpoint
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

        logger.info(f"[Switch Branch] 鍒嗘敮鍏辨湁 {len(checkpoints_list)} 涓猚heckpoint")

        # 3. 瑙ｆ瀽checkpoint鑾峰彇娑堟伅鍘嗗彶
        # checkpoint鏄€掑簭鐨勶紙鏈€鏂扮殑鍦ㄥ墠锛夛紝闇€瑕佸弽杞?
        messages = []
        for checkpoint_tuple in reversed(checkpoints_list):
            checkpoint_data = checkpoint_tuple.checkpoint

            # 浠巆heckpoint涓彁鍙栨秷鎭?
            # LangGraph鐨刢heckpoint鍖呭惈channel_values锛屽叾涓湁messages
            channel_values = checkpoint_data.get("channel_values", {})
            if "messages" in channel_values:
                # messages鏄竴涓垪琛紝姣忎釜鍏冪礌鏄竴鏉℃秷鎭?
                for msg in channel_values["messages"]:
                    # 鍏煎dict鍜屽璞′袱绉嶆牸寮?
                    if isinstance(msg, dict):
                        message_dict = {
                            "type": msg.get("type", "unknown"),
                            "content": msg.get("content", ""),
                            "name": msg.get("name"),
                            "id": msg.get("id")
                        }
                    else:
                        # 瀵硅薄鏍煎紡锛堜娇鐢╣etattr锛?
                        message_dict = {
                            "type": getattr(msg, "type", "unknown"),
                            "content": getattr(msg, "content", ""),
                            "name": getattr(msg, "name", None),
                            "id": getattr(msg, "id", None)
                        }
                    messages.append(message_dict)

        # 鍘婚噸锛坈heckpoint鍙兘鏈夐噸澶嶇殑娑堟伅锛?
        seen_ids = set()
        seen_content_hashes = set()  # 鐢ㄤ簬娌℃湁ID鐨勬秷鎭?
        unique_messages = []

        for msg in messages:
            msg_id = msg.get("id")

            if msg_id:
                # 鏈塈D鐨勬秷鎭細鍩轰簬ID鍘婚噸
                if msg_id not in seen_ids:
                    seen_ids.add(msg_id)
                    unique_messages.append(msg)
            else:
                # 娌℃湁ID鐨勬秷鎭細鍩轰簬鍐呭hash鍘婚噸
                content_hash = hash((
                    msg.get("type"),
                    msg.get("content"),
                    msg.get("name")
                ))
                if content_hash not in seen_content_hashes:
                    seen_content_hashes.add(content_hash)
                    unique_messages.append(msg)

        # 4. 鏇存柊鍒嗘敮鐨刬sActive鏍囪锛堝彲閫夛紝鐢ㄤ簬UI鏄剧ず锛?
        branch_metadata["is_active"] = True
        branch_metadata["last_accessed"] = get_utc_now().isoformat()
        redis_client.set(
            branch_key,
            json.dumps(branch_metadata, ensure_ascii=False),
            ex=7 * 24 * 60 * 60
        )

        logger.info(
            f"[Switch Branch] 鍒囨崲鎴愬姛 - Branch: {branch_id}, "
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
            detail=f"鍒囨崲鍒嗘敮澶辫触: {str(e)}"
        )


@router.get("/conversations/{conversation_id}/branches", response_model=GetBranchesResponse)
async def get_conversation_branches(
    conversation_id: str,
    current_user: User = Depends(get_current_active_user)
):
    """
    鑾峰彇浼氳瘽鐨勬墍鏈夊垎鏀垪琛?

    鍔熻兘:
    - 鑾峰彇浼氳瘽鐨勬墍鏈夊垎鏀?
    - 杩斿洖鍒嗘敮鍏冩暟鎹紙鎵佸钩鍒楄〃锛?
    - 鍓嶇鍙互鏍规嵁parent_branch_id鏋勫缓鏍戝舰缁撴瀯

    Args:
        conversation_id: 浼氳瘽ID锛堟牴鍒嗘敮ID锛?
        current_user: 褰撳墠鐢ㄦ埛

    Returns:
        GetBranchesResponse: 鍒嗘敮鍒楄〃
    """
    try:
        user_id = str(current_user.id)

        logger.info(f"[Get Branches] User: {user_id}, Conversation: {conversation_id}")

        redis_client = get_redis_client()

        # 1. 鑾峰彇浼氳瘽鐨勬墍鏈夊垎鏀疘D
        conversation_branches_key = f"conversation:{conversation_id}:branches"
        branch_ids = redis_client.smembers(conversation_branches_key)

        # 灏哹ytes杞负str
        if branch_ids:
            branch_ids = [bid.decode('utf-8') if isinstance(bid, bytes) else bid for bid in branch_ids]
        else:
            branch_ids = []

        logger.info(f"[Get Branches] found {len(branch_ids)} branches")

        # 2. 鎵归噺鑾峰彇鍒嗘敮鍏冩暟鎹紙浣跨敤Pipeline浼樺寲锛?
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

                    # 楠岃瘉鐢ㄦ埛鏉冮檺
                    if branch_metadata.get("user_id") == user_id:
                        branches_data.append(branch_metadata)
                else:
                    logger.warning(f"[Get Branches] 鍒嗘敮鍏冩暟鎹己澶? {branch_id}")

        # 3. 鏋勫缓杩斿洖鏁版嵁锛堟墎骞冲垪琛紝鍓嶇鑷繁鏋勫缓鏍戯級
        branch_nodes = []
        for branch_metadata in branches_data:
            node = BranchTreeNode(
                branch_id=branch_metadata["branch_id"],
                parent_branch_id=branch_metadata.get("parent_branch_id"),
                branch_name=branch_metadata["branch_name"],
                message_count=branch_metadata.get("message_count", 0),
                is_active=branch_metadata.get("is_active", False),
                created_at=branch_metadata["created_at"],
                children=[]  # 鎵佸钩鍒楄〃锛屽墠绔瀯寤烘爲
            )
            branch_nodes.append(node)

        # 4. 娣诲姞鏍瑰垎鏀紙涓诲垎鏀級淇℃伅锛堝鏋滆繕娌℃湁锛?
        # 涓诲垎鏀氨鏄痗onversation_id鏈韩
        root_exists = any(b.branch_id == conversation_id for b in branch_nodes)
        if not root_exists:
            # 鍒涘缓铏氭嫙鐨勬牴鍒嗘敮鑺傜偣
            root_node = BranchTreeNode(
                branch_id=conversation_id,
                parent_branch_id=None,
                branch_name="涓荤嚎",
                message_count=0,  # 鍙互閫氳繃checkpoint璁＄畻锛岃繖閲岀畝鍖?
                is_active=True,
                created_at=get_utc_now().isoformat(),
                children=[]
            )
            branch_nodes.insert(0, root_node)

        logger.info(
            f"[Get Branches] 杩斿洖 {len(branch_nodes)} 涓垎鏀?"
            f"(鍖呮嫭鏍瑰垎鏀? {conversation_id})"
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
            detail=f"鑾峰彇鍒嗘敮鍒楄〃澶辫触: {str(e)}"
        )


@router.post("/chat/stream")
async def agent_chat_stream(
    request: AgentChatRequest,
    current_user: User = Depends(get_current_active_user),
    memory: MemoryManager = Depends(get_memory_manager),
    ai_service: HTTPAIService = Depends(get_ai_service),
    # 鉁?淇锛氱Щ闄b渚濊禆锛岄伩鍏嶇敓鍛藉懆鏈熶笉鍖归厤
    mode: Optional[str] = None  # 鏂板锛氭敮鎸乵ode鍙傛暟锛堥€氳繃鏌ヨ鍙傛暟鎴朆ody锛?
):
    """
    Agent 鏅鸿兘瀵硅瘽 - 缁熶竴娴佸紡鍝嶅簲锛圫SE锛?

    鏀寔涓ょ妯″紡锛?
    - Planning妯″紡锛堥粯璁わ級锛氬厛瑙勫垝鍐嶆墽琛?
    - React妯″紡锛氳竟鎬濊€冭竟鎵ц

    浣跨敤鏂瑰紡锛?
    1. Planning妯″紡锛堥粯璁わ級: 涓嶄紶mode鎴杕ode="planning"
    2. React妯″紡: mode="react"

    Args:
        request: 瀵硅瘽璇锋眰
        current_user: 褰撳墠鐢ㄦ埛
        memory: 璁板繂绠＄悊鍣?
        ai_service: AI鏈嶅姟
        db: 鏁版嵁搴撲細璇?
        mode: 鑱婂ぉ妯″紡锛坧lanning/react锛岄粯璁lanning锛?

    Returns:
        StreamingResponse: SSE娴佸紡鍝嶅簲
    """
    import asyncio

    # 纭畾浣跨敤鐨勬ā寮?
    # 浼樺厛绾э細URL鏌ヨ鍙傛暟 > Body鍙傛暟 > 榛樿planning
    actual_mode = mode or request.mode or ChatMode.PLANNING

    # 瀛楃涓茶浆鏋氫妇
    if isinstance(actual_mode, str):
        try:
            actual_mode = ChatMode(actual_mode.lower())
        except (ValueError, AttributeError):
            logger.warning(f"[Chat Stream] 鏃犳晥鐨刴ode鍊? {actual_mode}, 浣跨敤榛樿planning")
            actual_mode = ChatMode.PLANNING

    logger.info(f"[Chat Stream] Mode: {actual_mode}")

    async def event_generator():
        # 鉁?淇锛氱敓鎴愬櫒鍐呭垱寤虹嫭绔媎b浼氳瘽锛屽畬鍏ㄦ帶鍒剁敓鍛藉懆鏈?
        from app.core.database import create_db_session

        async with create_db_session() as db:
            # 浣跨敤闃熷垪瀹炵幇瀹炴椂浜嬩欢鍙戦€?
            import time  # 鉁?鍦ㄨ繖閲屽鍏ワ紝鏁翠釜鍑芥暟鍐呴兘鍙互浣跨敤
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
                    # 楠岃瘉鐜版湁浼氳瘽鐨勫綊灞?
                    stored_user_id = await redis_client.get(
                        f"conversation:{request.conversation_id}:owner"
                    )
                    if stored_user_id:
                        # RedisClient 宸茶缃?decode_responses=True锛岃繑鍥炲瓧绗︿覆
                        # 浣嗗鏋滆繑鍥炵殑鏄瓧鑺傦紝闇€瑕佽В鐮?
                        if isinstance(stored_user_id, bytes):
                            stored_user_id = stored_user_id.decode('utf-8')
                        if stored_user_id != user_id:
                            # 浼氳瘽褰掑睘楠岃瘉澶辫触
                            error_event = {
                                'type': 'error',
                                'message': 'Unauthorized to access this conversation',
                                'code': 'UNAUTHORIZED_CONVERSATION'
                            }
                            yield f"data: {json.dumps(error_event, ensure_ascii=False)}\n\n"
                            logger.warning(
                                f"[Security] 鐢ㄦ埛 {user_id} 灏濊瘯璁块棶鍏朵粬鐢ㄦ埛鐨勪細璇?{request.conversation_id}"
                            )
                            return
                else:
                    # 鏂颁細璇濓細瀛樺偍褰掑睘鍏崇郴
                    await redis_client.set(
                        f"conversation:{conversation_id}:owner",
                        user_id,
                        expire=86400 * 30  # 30澶╄繃鏈燂紙淇锛歟x -> expire锛?
                    )
                    logger.info(f"[Session] 鍒涘缓鏂颁細璇濆綊灞? {conversation_id} -> {user_id}")

                logger.info(f"[LangGraph Agent Stream] 鈴憋笍 璇锋眰寮€濮?- User: {user_id}, Mode: {actual_mode}, Message: {request.message[:50]}...")

                # 鍙戦€佸紑濮嬩簨浠讹紙鍖呭惈mode淇℃伅锛?
                start_event = {'type': 'start', 'conversation_id': conversation_id, 'mode': str(actual_mode)}
                yield f"data: {json.dumps(start_event, ensure_ascii=False)}\n\n"

                # 鉁?淇锛氬垹闄ゅ浣欑殑 MemoryManager 璋冪敤
                # WritingAgentGraph 鍐呴儴宸叉湁 ContextManager锛堜娇鐢?VectorStore 鐨勮涔夋悳绱級
                # 涓嶅啀闇€瑕佷粠 Redis 鑾峰彇绌虹殑浼氳瘽鍒楄〃
                # 娉ㄩ噴鍘熷洜锛?
                # 1. MemoryManager.get_complete_context() 浠?Redis 鏌ヨ浼氳瘽鍒楄〃 鈫?杩斿洖0鏉★紙Redis閲屾病鏁版嵁锛?
                # 2. WritingAgentGraph 宸茬粡鏈?ContextManager 鈫?浠?ChromaDB 妫€绱紙鏈夋暟鎹級
                # 3. 瀵艰嚧閲嶅妫€绱笖浣跨敤浜嗛敊璇殑鏁版嵁婧?

                # 鑾峰彇鍏ㄥ眬鍏变韩鐨?LangGraph Agent
                agent_graph = get_agent_graph()

                # 鍑嗗涓婁笅鏂囷紙鍒涘缓鏂癲ict閬垮厤淇敼鍘焤equest锛?
                context = dict(request.context) if request.context else {}
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
                                # 文档不存在或无权限访问
                                logger.warning(f"[agent_chat_stream] Knowledge doc not found or access denied: doc_id={doc_id}, user_id={user_id}")
                        except Exception as load_err:
                            logger.warning(f"[agent_chat_stream] load knowledge item failed: {load_err}")

                # ===== 向后兼容：tags 搜索（仅在旧前端调用时触发，计划在后续版本移除）=====
                if not knowledge_docs:
                    tags = context.get("knowledge_tags") if isinstance(context.get("knowledge_tags"), list) else []
                    if tags:
                        logger.info(f"[agent_chat_stream] Using legacy knowledge_tags search (deprecated): tags={tags}")
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
                            logger.warning(f"[agent_chat_stream] knowledge semantic search failed: {search_err}")
                        # 语义检索为空时，退化为按标签的数据库过滤
                        if not knowledge_docs:
                            try:
                                items, _ = await knowledge_service.get_items(
                                    user_id=user_id,
                                    tags=tags,
                                    work_id=request.work_id
                                )
                                for item in items[:3]:
                                    knowledge_docs.append({
                                        "id": str(item.id),
                                        "title": item.title,
                                        "content": item.content,
                                        "tags": item.tags,
                                        "source_type": getattr(item.source_type, "value", str(item.source_type)),
                                    })
                            except Exception as list_err:
                                logger.warning(f"[agent_chat_stream] fallback tag filter failed: {list_err}")

                # 标签检索为空时，降级为不带标签的语义检索
                if not knowledge_docs:
                    try:
                        search_results = await knowledge_service.search_by_semantic(
                            user_id=user_id,
                            query=request.message,
                            tags=None,
                            top_k=3,
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
                        logger.warning(f"[agent_chat_stream] fallback knowledge semantic search failed: {search_err}")

                if knowledge_docs:
                    context["knowledge_docs"] = knowledge_docs
                    logger.info(f"[agent_chat_stream] Injected {len(knowledge_docs)} knowledge docs into context")

                # 鉁?杩借釜娲诲姩鐘舵€侊紙鐢ㄤ簬鍙戦€?activity_complete 浜嬩欢锛?
                last_activity_step = {'step': None, 'start_time': None}
                # 鉁?杩借釜鍐呭鏄惁宸查€氳繃娴佸紡鍙戦€侊紙閬垮厤閲嶅鍙戦€侊級
                content_sent = {'value': False}

                # 瀹氫箟鍥炶皟鍑芥暟 - 瀹炴椂鏀惧叆闃熷垪
                async def on_plan(plan_data):
                    """Handle plan event."""
                    await event_queue.put(('plan', plan_data))
                    logger.info(f"[Stream] Plan tasks: {len(plan_data.get('tasks', []))} items")

                async def on_task_start(task):
                    """Handle task start event."""
                    await event_queue.put(('task_start', task))
                    logger.info(f"[Stream] Task started: {task.get('description')}")

                async def on_task_progress(task, status):
                    """浠诲姟杩涘害鍥炶皟"""
                    await event_queue.put(('task_progress', {'task_id': task.get('task_id'), 'status': status}))

                async def on_task_done(task, result_data):
                    """浠诲姟瀹屾垚鍥炶皟"""
                    elapsed_time = task.get('elapsed_time', 0)
                    await event_queue.put(('task_done', {
                        'task_id': task.get('task_id'),
                        'description': task.get('description'),
                        'elapsed_time': elapsed_time
                    }))
                    logger.info(f"[Stream] 浠诲姟瀹屾垚: {task.get('description')} ({elapsed_time:.1f}s)")

                async def on_content(chunk):
                    """鍐呭鐢熸垚鍥炶皟"""
                    content_sent['value'] = True  # 鉁?鏍囪鍐呭宸插彂閫?
                    if isinstance(chunk, dict) and "content" in chunk:
                        assistant_chunks.append(str(chunk.get("content", "")))
                    elif chunk is not None:
                        assistant_chunks.append(str(chunk))
                    await event_queue.put(('content', chunk))

                # 鍦ㄥ悗鍙拌繍琛?Agent
                async def run_agent():
                    nonlocal result
                    try:
                        # 鏍规嵁妯″紡璋冪敤涓嶅悓鐨勬柟娉?
                        if actual_mode == ChatMode.REACT:
                            # React妯″紡锛氫娇鐢╟hat_stream()
                            # 瀹氫箟React妯″紡鐨勫洖璋?
                            async def on_progress_react(event):
                                """杩涘害鍥炶皟 - 娣诲姞activity_complete閫昏緫"""
                                current_step = event.get('step')

                                # 鉁?濡傛灉娲诲姩绫诲瀷鏀瑰彉锛屽彂閫佸墠涓€涓椿鍔ㄧ殑瀹屾垚浜嬩欢
                                if last_activity_step['step'] is not None and last_activity_step['step'] != current_step:
                                    elapsed_time = time.time() - last_activity_step['start_time'] if last_activity_step['start_time'] else 0
                                    await event_queue.put(('activity_complete', {
                                        'step': last_activity_step['step'],
                                        'elapsed_time': elapsed_time
                                    }))
                                    logger.info(f"[Stream] Activity瀹屾垚: {last_activity_step['step']} ({elapsed_time:.1f}s)")

                                # 鏇存柊褰撳墠娲诲姩
                                last_activity_step['step'] = current_step
                                last_activity_step['start_time'] = time.time()

                                # 鍙戦€乸rogress浜嬩欢
                                await event_queue.put(('progress', event))

                            async def on_tool_call_react(tool_name: str, tool_args: dict):
                                await event_queue.put(('tool_call', {'tool': tool_name, 'args': tool_args}))

                            async def on_content_react(content: str):
                                content_sent['value'] = True  # 鉁?鏍囪鍐呭宸插彂閫?
                                assistant_chunks.append(str(content) if content is not None else "")
                                await event_queue.put(('content', {'content': content}))

                            # 鉁?P0-6淇锛氬畾涔塇ITL纭璇锋眰鍥炶皟锛堝瓨鍌ㄤ负瀹炰緥鍙橀噺锛岄伩鍏嶅簭鍒楀寲锛?
                            async def on_approval_request(request_data: dict):
                                """Handle approval request stream event."""
                                logger.info(f"[Stream] Approval request: {request_data.get('request_id')}")
                                await event_queue.put(('approval_request', request_data))

                            # 鉁?P0-6淇锛氬皢鍥炶皟璁剧疆涓哄疄渚嬪彉閲忥紝鑰岄潪娣诲姞鍒癱ontext锛堥伩鍏峈edis搴忓垪鍖栭敊璇級
                            agent_graph._approval_callback = on_approval_request

                            result = await agent_graph.chat_stream(
                                message=request.message,
                                user_id=user_id,  # 鏂板锛氫紶鍏ョ敤鎴稩D
                                work_id=request.work_id,
                                chapter_id=request.chapter_id,
                                conversation_id=conversation_id,
                                context=context,
                                on_progress=on_progress_react,
                                on_tool_call=on_tool_call_react,
                                on_content=on_content_react,
                                db=db  # 鉁?淇锛氫紶鍏ョ敓鎴愬櫒鐨勭嫭绔媎b浼氳瘽
                            )
                        else:
                            # Planning妯″紡锛氫娇鐢╟hat_with_planning()
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
                        # 鉁?鍙戦€佹渶鍚庝竴涓椿鍔ㄧ殑瀹屾垚浜嬩欢
                        if last_activity_step['step'] is not None:
                            elapsed_time = time.time() - last_activity_step['start_time'] if last_activity_step['start_time'] else 0
                            await event_queue.put(('activity_complete', {
                                'step': last_activity_step['step'],
                                'elapsed_time': elapsed_time
                            }))
                            logger.info(f"[Stream] 鏈€鍚庢椿鍔ㄥ畬鎴? {last_activity_step['step']} ({elapsed_time:.1f}s)")

                        # Agent 瀹屾垚鍚庢斁鍏ョ粨鏉熸爣璁?
                        await event_queue.put(('__done__', None))
                    except Exception as e:
                        # Agent鎵ц寮傚父锛岄€氳繃闃熷垪鍙戦€侀敊璇?
                        logger.error(f"[Stream] Agent鎵ц澶辫触: {str(e)}", exc_info=True)
                        await event_queue.put(('__error__', {
                            'error': str(e),
                            'error_type': type(e).__name__
                        }))

                # 鍚姩 Agent 浠诲姟
                agent_task = asyncio.create_task(run_agent())

                # 瀹炴椂浠庨槦鍒椾腑鍙栧嚭浜嬩欢骞跺彂閫?
                while True:
                    event_type, event_data = await event_queue.get()

                    if event_type == '__done__':
                        # Agent 鎵ц瀹屾垚
                        break

                    if event_type == '__error__':
                        # Agent鎵ц澶辫触
                        error_event = {
                            'type': 'error',
                            'data': event_data,
                            'mode': str(actual_mode)
                        }
                        yield f"data: {json.dumps(error_event, ensure_ascii=False)}\n\n"
                        # 缁撴潫娴佸紡鍝嶅簲
                        return

                    # 瀹炴椂鍙戦€佷簨浠讹紙娣诲姞mode鏍囪瘑锛?
                    event_payload = {
                        'type': event_type,
                        'data': event_data,
                        'mode': str(actual_mode)
                    }
                    # 娣诲姞璋冭瘯鏃ュ織
                    if event_type == 'progress':
                        logger.info(f"[SSE] 鍙戦€?progress 浜嬩欢: step={event_data.get('step')}, desc={event_data.get('description')}")
                    elif event_type == 'activity_complete':
                        logger.info(f"[SSE] 鍙戦€?activity_complete 浜嬩欢: step={event_data.get('step')}, elapsed={event_data.get('elapsed_time'):.1f}s")
                    yield f"data: {json.dumps(event_payload, ensure_ascii=False)}\n\n"

                # 绛夊緟 Agent 浠诲姟瀹屾垚
                await agent_task

                # 妫€鏌esult鏄惁鏈夋晥
                if result is None:
                    logger.error(f"[LangGraph Agent Stream] Result is None, Agent鍙兘鎵ц澶辫触")
                    error_event = {
                        'type': 'error',
                        'error': 'Agent鎵ц澶辫触锛屾湭杩斿洖缁撴灉',
                        'mode': str(actual_mode)
                    }
                    yield f"data: {json.dumps(error_event, ensure_ascii=False)}\n\n"
                    return

                # 鉁?淇锛氬彧鏈夊綋鍐呭鏈€氳繃娴佸紡鍙戦€佹椂锛屾墠鍦ㄥ畬鎴愬墠鍙戦€乫inal_response
                final_response = result.get("response")
                if final_response and not content_sent['value']:
                    logger.info(f"[Stream] 鍙戦€佹渶缁堝搷搴旓紙鍐呭鏈祦寮忓彂閫侊級: {final_response[:100]}...")
                    content_event = {
                        'type': 'content',
                        'data': final_response,
                        'mode': str(actual_mode)
                    }
                    yield f"data: {json.dumps(content_event, ensure_ascii=False)}\n\n"
                elif final_response:
                    logger.info(f"[Stream] 璺宠繃鏈€缁堝搷搴旓紙鍐呭宸叉祦寮忓彂閫侊級")

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

                # 璁板綍浜や簰
                memory.record_user_interaction(
                    user_id,
                    "agent_chat",
                    {
                        "message": request.message,
                        "intent": result.get("metadata", {}).get("intent"),
                        "conversation_id": conversation_id,
                        "mode": str(actual_mode)  # 璁板綍浣跨敤鐨勬ā寮?
                    }
                )

                # 鍙戦€佸畬鎴愪簨浠?
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
                # 鍙戦€侀敊璇簨浠讹紙鍖呭惈mode鏍囪瘑锛?
                error_event = {
                    'type': 'error',
                    'error': str(e),
                    'error_type': type(e).__name__,
                    'mode': str(actual_mode)
                }
                yield f"data: {json.dumps(error_event, ensure_ascii=False)}\n\n"
                # 鍙栨秷 Agent 浠诲姟
                if agent_task and not agent_task.done():
                    agent_task.cancel()

    return StreamingResponse(
        event_generator(),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
            "X-Accel-Buffering": "no"  # 绂佺敤 nginx 缂撳啿
        }
    )


# ==================== 鎵ц璁″垝绠＄悊 ====================

@router.post("/plans", response_model=PlanResponse)
async def create_plan(
    request: PlanCreationRequest,
    current_user: User = Depends(get_current_active_user),
    planner: PlanningAgent = Depends(get_planning_agent)
):
    """
    鍒涘缓鎵ц璁″垝

    鏍规嵁鐢ㄦ埛鐩爣鑷姩鐢熸垚鎵ц璁″垝锛屾敮鎸侊細
    - 灏忚鍒涗綔瑙勫垝
    - 浣滃搧鏀硅繘瑙勫垝
    - 鑷畾涔夎鍒?

    Args:
        request: 璁″垝鍒涘缓璇锋眰
        current_user: 褰撳墠鐢ㄦ埛
        planner: 瑙勫垝Agent

    Returns:
        PlanResponse: 鎵ц璁″垝
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
            detail=f"鍒涘缓璁″垝澶辫触: {str(e)}"
        )


@router.get("/plans/{plan_id}", response_model=PlanResponse)
async def get_plan(
    plan_id: str,
    current_user: User = Depends(get_current_active_user)
):
    """鑾峰彇鎵ц璁″垝璇︽儏"""
    # TODO: 浠庡瓨鍌ㄤ腑鑾峰彇璁″垝
    raise HTTPException(
        status_code=status.HTTP_501_NOT_IMPLEMENTED,
        detail="鍔熻兘寮€鍙戜腑"
    )


# ==================== HITL 鎵瑰噯绠＄悊 ====================

@router.get("/approvals/pending", response_model=List[ApprovalResponse])
async def get_pending_approvals(
    current_user: User = Depends(get_current_active_user),
    hitl: HITLManager = Depends(get_hitl_manager)
):
    """
    鑾峰彇寰呮壒鍑嗗垪琛?

    杩斿洖褰撳墠鐢ㄦ埛鎵€鏈夊緟澶勭悊鐨勬壒鍑嗚姹?

    Args:
        current_user: 褰撳墠鐢ㄦ埛
        hitl: HITL绠＄悊鍣?

    Returns:
        List[ApprovalResponse]: 寰呮壒鍑嗗垪琛?
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
            detail=f"鑾峰彇寰呮壒鍑嗗垪琛ㄥけ璐? {str(e)}"
        )


@router.post("/approvals/{request_id}/action")
async def handle_approval(
    request_id: str,
    action_request: ApprovalActionRequest,
    current_user: User = Depends(get_current_active_user),
    hitl: HITLManager = Depends(get_hitl_manager)
):
    """
    澶勭悊鎵瑰噯璇锋眰

    鏀寔鐨勬搷浣滐細
    - approve: 鎵瑰噯
    - reject: 鎷掔粷
    - modify: 淇敼鍚庢壒鍑?

    Args:
        request_id: 璇锋眰ID
        action_request: 鎿嶄綔璇锋眰
        current_user: 褰撳墠鐢ㄦ埛
        hitl: HITL绠＄悊鍣?

    Returns:
        鎿嶄綔缁撴灉
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
                    detail="淇敼鎿嶄綔闇€瑕佹彁渚沵odifications"
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
                detail=f"涓嶆敮鎸佺殑鎿嶄綔: {action_request.action}"
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
            detail=f"澶勭悊鎵瑰噯璇锋眰澶辫触: {str(e)}"
        )


# ==================== 璁板繂绠＄悊 ====================

@router.get("/memory/context")
async def get_memory_context(
    work_id: Optional[str] = Query(None, description="浣滃搧ID锛岀敤浜庤幏鍙栫壒瀹氫綔鍝佺殑璁板繂"),
    current_user: User = Depends(get_current_active_user),
    memory: MemoryManager = Depends(get_memory_manager)
):
    """
    鑾峰彇鐢ㄦ埛璁板繂涓婁笅鏂?

    杩斿洖鐢ㄦ埛鐨勫畬鏁磋蹇嗕俊鎭紝鍖呮嫭锛?
    - 鐢ㄦ埛鍋忓ソ
    - 鍐欎綔椋庢牸
    - 鐢ㄦ埛鐢诲儚

    鍙€夊弬鏁帮細
    - work_id: 浣滃搧ID锛屽鏋滄彁渚涘垯鍙繑鍥炶浣滃搧鐨勫璇濊蹇?

    Args:
        work_id: 浣滃搧ID锛堝彲閫夛紝鐢ㄤ簬闅旂涓嶅悓浣滃搧鐨勮蹇嗭級
        current_user: 褰撳墠鐢ㄦ埛
        memory: 璁板繂绠＄悊鍣?

    Returns:
        鐢ㄦ埛璁板繂涓婁笅鏂?
    """
    try:
        user_id = str(current_user.id)
        # 鉁?淇锛氭坊鍔爓ork_id鍙傛暟鏀寔
        context = await memory.get_complete_context(user_id, work_id=work_id)

        return {
            "success": True,
            "data": context
        }

    except Exception as e:
        logger.error(f"Get memory context error: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"鑾峰彇璁板繂涓婁笅鏂囧け璐? {str(e)}"
        )


@router.post("/memory/preferences")
async def update_preferences(
    preferences: Dict[str, Any],
    current_user: User = Depends(get_current_active_user),
    memory: MemoryManager = Depends(get_memory_manager)
):
    """
    鏇存柊鐢ㄦ埛鍋忓ソ

    Args:
        preferences: 鍋忓ソ鏁版嵁
        current_user: 褰撳墠鐢ㄦ埛
        memory: 璁板繂绠＄悊鍣?

    Returns:
        鏇存柊缁撴灉
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
            detail=f"鏇存柊鍋忓ソ澶辫触: {str(e)}"
        )


# ==================== 浼氳瘽绠＄悊 ====================

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


@router.post("/sessions", response_model=AgentSessionResponse, summary="鍒涘缓 Agent 浼氳瘽")
async def create_agent_session(
    payload: AgentSessionCreateRequest,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    title = payload.title or "New session"
    now = datetime.utcnow()
    expires_at = now + timedelta(days=30)

    new_session = AgentSession(
        user_id=current_user.id,
        title=title,
        conversation_id=payload.conversation_id,
        work_id=payload.work_id,
        chapter_id=payload.chapter_id,
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


@router.get("/sessions", response_model=AgentSessionListResponse, summary="鑾峰彇 Agent 浼氳瘽鍒楄〃")
async def list_agent_sessions(
    work_id: Optional[str] = Query(None, description="Filter by work ID"),
    chapter_id: Optional[str] = Query(None, description="Filter by chapter ID"),
    limit: int = Query(50, ge=1, le=200, description="杩斿洖鏁伴噺涓婇檺"),
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


@router.get("/sessions/{session_id}", response_model=AgentSessionResponse, summary="鑾峰彇鍗曚釜 Agent 浼氳瘽璇︽儏")
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


@router.patch("/sessions/{session_id}", response_model=AgentSessionResponse, summary="鏇存柊 Agent 浼氳瘽")
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


@router.delete("/sessions/{session_id}", status_code=status.HTTP_204_NO_CONTENT, summary="鍒犻櫎 Agent 浼氳瘽")
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


# ==================== 杈呭姪鍑芥暟 ====================
# 娉ㄦ剰: 鍘熸湁鐨勬剰鍥炬娴嬪拰澶勭悊閫昏緫宸茶縼绉诲埌 LangGraph 妗嗘灦涓?
# 璇﹁: app/services/agent/langgraph_agent.py

