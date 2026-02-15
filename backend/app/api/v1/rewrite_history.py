"""
改写历史 API 路由

提供改写历史记录的管理接口
"""

from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, and_, desc, func
from pydantic import BaseModel, Field, ConfigDict
from typing import List, Optional
from datetime import datetime
from uuid import UUID
import logging

from app.core.database import get_db
from app.core.security import get_current_active_user
from app.models.user import User
from app.models.rewrite_history import RewriteSession, RewriteResult

router = APIRouter()
logger = logging.getLogger(__name__)


# ==================== 请求/响应数据模型 ====================

class RewriteResultCreate(BaseModel):
    """创建改写结果"""
    model_name: str = Field(..., description="模型名称")
    rewritten_text: str = Field(..., description="改写后的文本")
    word_count: int = Field(..., description="字数")
    elapsed_time: float = Field(..., description="耗时（秒）")
    error: Optional[str] = Field(None, description="错误信息")
    is_selected: bool = Field(False, description="是否被选中")


class RewriteSessionCreate(BaseModel):
    """创建改写会话"""
    original_text: str = Field(..., description="原文")
    context_before: Optional[str] = Field(None, description="前文上下文")
    context_after: Optional[str] = Field(None, description="后文上下文")
    mode: str = Field(..., description="改写模式")
    custom_requirement: Optional[str] = Field(None, description="自定义要求")
    results: List[RewriteResultCreate] = Field(..., description="改写结果列表")


class RewriteResultResponse(BaseModel):
    """改写结果响应"""
    id: str
    model_name: str
    rewritten_text: str
    word_count: int
    elapsed_time: float
    error: Optional[str]
    is_selected: bool
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)
class RewriteSessionResponse(BaseModel):
    """改写会话响应"""
    id: str
    user_id: str
    original_text: str
    context_before: Optional[str]
    context_after: Optional[str]
    mode: str
    custom_requirement: Optional[str]
    created_at: datetime
    results: List[RewriteResultResponse]

    model_config = ConfigDict(from_attributes=True)
class RewriteSessionListItem(BaseModel):
    """改写会话列表项（简化版）"""
    id: str
    original_text: str  # 原文（可能截断）
    mode: str
    result_count: int  # 结果数量
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)
class RewriteSessionListResponse(BaseModel):
    """改写会话列表响应"""
    sessions: List[RewriteSessionListItem]
    total: int
    page: int
    page_size: int


# ==================== API 路由 ====================

@router.post(
    "/sessions",
    summary="保存改写记录",
    response_model=RewriteSessionResponse,
    description="""
    保存一次改写会话及其所有模型的改写结果。

    **请求示例**:
    ```json
    {
      "original_text": "主角走进房间，看到了桌子上的剑。",
      "mode": "expand",
      "context_before": "经过三天的跋涉...",
      "results": [
        {
          "model_name": "gemini-2.5-pro",
          "rewritten_text": "主角推开那扇厚重的木门...",
          "word_count": 156,
          "elapsed_time": 2.3,
          "error": null,
          "is_selected": true
        }
      ]
    }
    ```
    """
)
async def create_rewrite_session(
    request: RewriteSessionCreate,
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db)
) -> RewriteSessionResponse:
    """创建改写会话"""
    # 提前提取用户信息，避免后续访问关系属性
    user_id = current_user.id
    username = getattr(current_user, 'username', str(user_id))

    logger.info(
        f"[保存改写记录] 用户: {username}({user_id}), "
        f"模式: {request.mode}, 结果数: {len(request.results)}"
    )

    try:
        # 创建会话记录
        session = RewriteSession(
            user_id=user_id,
            original_text=request.original_text,
            context_before=request.context_before,
            context_after=request.context_after,
            mode=request.mode,
            custom_requirement=request.custom_requirement
        )

        db.add(session)
        await db.flush()  # 获取 session.id

        # 创建结果记录
        for result_data in request.results:
            result = RewriteResult(
                session_id=session.id,
                model_name=result_data.model_name,
                rewritten_text=result_data.rewritten_text,
                word_count=result_data.word_count,
                elapsed_time=result_data.elapsed_time,
                error=result_data.error,
                is_selected=result_data.is_selected
            )
            db.add(result)

        await db.commit()
        await db.refresh(session)

        # 查询结果列表（不要手动设置关系属性）
        stmt = select(RewriteResult).where(RewriteResult.session_id == session.id).order_by(RewriteResult.created_at)
        result = await db.execute(stmt)
        results_list = result.scalars().all()

        logger.info(f"[保存改写记录] 用户 {username} 保存成功，会话ID: {session.id}")

        # 转换为响应模型（直接使用查询到的 results_list）
        return RewriteSessionResponse(
            id=str(session.id),
            user_id=str(session.user_id),
            original_text=session.original_text,
            context_before=session.context_before,
            context_after=session.context_after,
            mode=session.mode,
            custom_requirement=session.custom_requirement,
            created_at=session.created_at,
            results=[
                RewriteResultResponse(
                    id=str(r.id),
                    model_name=r.model_name,
                    rewritten_text=r.rewritten_text,
                    word_count=r.word_count,
                    elapsed_time=r.elapsed_time,
                    error=r.error,
                    is_selected=r.is_selected,
                    created_at=r.created_at
                )
                for r in results_list  # 使用查询到的列表，而不是 session.results
            ]
        )

    except Exception as e:
        await db.rollback()
        error_msg = str(e)
        logger.error(f"[保存改写记录] 用户ID: {user_id} 保存失败: {error_msg}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"保存记录失败: {error_msg}"
        )


@router.get(
    "/sessions",
    summary="获取改写历史列表",
    response_model=RewriteSessionListResponse,
    description="""
    获取当前用户的改写历史记录列表。

    **查询参数**:
    - page: 页码（从1开始）
    - page_size: 每页数量
    """
)
async def get_rewrite_sessions(
    page: int = Query(1, ge=1, description="页码"),
    page_size: int = Query(20, ge=1, le=100, description="每页数量"),
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db)
) -> RewriteSessionListResponse:
    """获取改写历史列表"""
    # 提前提取用户信息
    user_id = current_user.id
    username = getattr(current_user, 'username', str(user_id))

    logger.info(
        f"[获取改写历史] 用户: {username}({user_id}), "
        f"页码: {page}, 每页: {page_size}"
    )

    try:
        # 查询总数（优化：使用数据库层面的count）
        count_stmt = select(func.count()).select_from(RewriteSession).where(
            RewriteSession.user_id == user_id
        )
        count_result = await db.execute(count_stmt)
        total = count_result.scalar()

        # 查询会话列表
        offset = (page - 1) * page_size

        # 创建子查询统计每个会话的结果数量（优化：避免N+1查询）
        result_count_subq = (
            select(
                RewriteResult.session_id,
                func.count(RewriteResult.id).label('result_count')
            )
            .group_by(RewriteResult.session_id)
            .subquery()
        )

        # 主查询 LEFT JOIN 子查询
        stmt = (
            select(RewriteSession, result_count_subq.c.result_count)
            .outerjoin(result_count_subq, RewriteSession.id == result_count_subq.c.session_id)
            .where(RewriteSession.user_id == user_id)
            .order_by(desc(RewriteSession.created_at))
            .offset(offset)
            .limit(page_size)
        )

        result = await db.execute(stmt)
        rows = result.all()

        # 构建响应
        session_items = []
        for session, result_count in rows:
            # 截断原文（最多100字）
            original_text = session.original_text
            if len(original_text) > 100:
                original_text = original_text[:100] + "..."

            session_items.append(
                RewriteSessionListItem(
                    id=str(session.id),
                    original_text=original_text,
                    mode=session.mode,
                    result_count=result_count or 0,
                    created_at=session.created_at
                )
            )

        logger.info(
            f"[获取改写历史] 用户 {username} 查询成功，"
            f"总数: {total}, 当前页: {len(session_items)}"
        )

        return RewriteSessionListResponse(
            sessions=session_items,
            total=total,
            page=page,
            page_size=page_size
        )

    except Exception as e:
        error_msg = str(e)
        logger.error(f"[获取改写历史] 用户ID: {user_id} 查询失败: {error_msg}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"获取历史记录失败: {error_msg}"
        )


@router.get(
    "/sessions/{session_id}",
    summary="获取改写会话详情",
    response_model=RewriteSessionResponse,
    description="获取指定改写会话的完整详情，包括所有模型的改写结果。"
)
async def get_rewrite_session(
    session_id: UUID,
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db)
) -> RewriteSessionResponse:
    """获取改写会话详情"""
    # 提前提取用户信息
    user_id = current_user.id
    username = getattr(current_user, 'username', str(user_id))

    logger.info(
        f"[获取会话详情] 用户: {username}({user_id}), "
        f"会话ID: {session_id}"
    )

    try:
        # 查询会话
        stmt = select(RewriteSession).where(
            and_(
                RewriteSession.id == session_id,
                RewriteSession.user_id == user_id
            )
        )
        result = await db.execute(stmt)
        session = result.scalar_one_or_none()

        if not session:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="改写会话不存在或无权访问"
            )

        # 查询结果
        results_stmt = select(RewriteResult).where(
            RewriteResult.session_id == session.id
        ).order_by(RewriteResult.created_at)
        results_result = await db.execute(results_stmt)
        results = results_result.scalars().all()

        logger.info(f"[获取会话详情] 用户 {username} 查询成功")

        return RewriteSessionResponse(
            id=str(session.id),
            user_id=str(session.user_id),
            original_text=session.original_text,
            context_before=session.context_before,
            context_after=session.context_after,
            mode=session.mode,
            custom_requirement=session.custom_requirement,
            created_at=session.created_at,
            results=[
                RewriteResultResponse(
                    id=str(r.id),
                    model_name=r.model_name,
                    rewritten_text=r.rewritten_text,
                    word_count=r.word_count,
                    elapsed_time=r.elapsed_time,
                    error=r.error,
                    is_selected=r.is_selected,
                    created_at=r.created_at
                )
                for r in results
            ]
        )

    except HTTPException:
        raise
    except Exception as e:
        error_msg = str(e)
        logger.error(f"[获取会话详情] 用户ID: {user_id} 查询失败: {error_msg}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"获取会话详情失败: {error_msg}"
        )


@router.delete(
    "/sessions/{session_id}",
    summary="删除改写会话",
    description="删除指定的改写会话及其所有结果。"
)
async def delete_rewrite_session(
    session_id: UUID,
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db)
):
    """删除改写会话"""
    # 提前提取用户信息
    user_id = current_user.id
    username = getattr(current_user, 'username', str(user_id))

    logger.info(
        f"[删除改写会话] 用户: {username}({user_id}), "
        f"会话ID: {session_id}"
    )

    try:
        # 查询会话
        stmt = select(RewriteSession).where(
            and_(
                RewriteSession.id == session_id,
                RewriteSession.user_id == user_id
            )
        )
        result = await db.execute(stmt)
        session = result.scalar_one_or_none()

        if not session:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="改写会话不存在或无权访问"
            )

        # 删除会话（级联删除结果）
        await db.delete(session)
        await db.commit()

        logger.info(f"[删除改写会话] 用户 {username} 删除成功")

        return {"detail": "删除成功"}

    except HTTPException:
        raise
    except Exception as e:
        await db.rollback()
        error_msg = str(e)
        logger.error(f"[删除改写会话] 用户ID: {user_id} 删除失败: {error_msg}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"删除会话失败: {error_msg}"
        )
