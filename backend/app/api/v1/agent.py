"""
Agent 智能助手 API 路由

提供 Agent 相关的 RESTful API 接口，包括：
- Agent 对话（支持流式响应）
- 人机协同（HITL）批准管理
- 执行计划管理
- 记忆管理
"""

from fastapi import APIRouter, Depends, HTTPException, status
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
from app.services.agent.memory import MemoryManager
from app.services.agent.agents import PlanningAgent, ReflectionAgent
from app.services.agent.tools import HITLManager
from app.services.ai.http_ai_service import HTTPAIService
from app.services.agent.langgraph_agent import WritingAgentGraph
from app.core.config import settings
import redis

router = APIRouter()
logger = logging.getLogger(__name__)

# 创建同步Redis客户端（用于Agent系统）
def get_redis_client():
    """获取同步Redis客户端"""
    return redis.Redis(
        host='localhost',
        port=6379,
        db=1,  # 使用db1，避免与缓存服务冲突
        decode_responses=False
    )


# ==================== 请求/响应数据模型 ====================

class AgentChatRequest(BaseModel):
    """Agent 对话请求"""
    message: str = Field(..., description="用户消息", min_length=1)
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


# ==================== 依赖注入 ====================

async def get_memory_manager(
    db: AsyncSession = Depends(get_db)
) -> MemoryManager:
    """获取记忆管理器"""
    redis_client = get_redis_client()
    return MemoryManager(redis_client)


async def get_planning_agent() -> PlanningAgent:
    """获取规划Agent"""
    return PlanningAgent()


async def get_hitl_manager() -> HITLManager:
    """获取HITL管理器"""
    redis_client = get_redis_client()
    return HITLManager(redis_client)


async def get_ai_service() -> HTTPAIService:
    """获取AI服务实例"""
    return HTTPAIService()


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
    Agent 智能对话（基于 LangGraph 框架）

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

        logger.info(f"[LangGraph Agent] User: {user_id}, Message: {request.message[:50]}...")

        # 获取用户记忆上下文
        user_context = memory.get_complete_context(user_id)
        memory_context = memory.format_context_for_agent(user_id, mode="chat")

        # 创建 LangGraph Agent（使用配置中的模式）
        agent_graph = WritingAgentGraph(ai_service, use_chatgpt=settings.AGENT_USE_CHATGPT)

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
    current_user: User = Depends(get_current_active_user),
    memory: MemoryManager = Depends(get_memory_manager)
):
    """
    获取用户记忆上下文

    返回用户的完整记忆信息，包括：
    - 用户偏好
    - 写作风格
    - 用户画像

    Args:
        current_user: 当前用户
        memory: 记忆管理器

    Returns:
        用户记忆上下文
    """
    try:
        user_id = str(current_user.id)
        context = memory.get_complete_context(user_id)

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
