from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy import select, func, and_
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload
from typing import Optional
import logging

from app.core.database import get_db
from app.core.security import get_current_active_user
from app.models.user import User
from app.models.work import Work
from app.models.comment import Comment, CommentLike, CommentReport
from app.models.rating import WorkRating
from app.schemas.comment import (
    CommentCreate,
    CommentUpdate,
    CommentResponse,
    CommentWithRepliesResponse,
    CommentListResponse,
    UserInfo
)
from app.schemas.report import CommentReportCreate, CommentReportResponse

router = APIRouter()
logger = logging.getLogger(__name__)


@router.get("/works/{work_id}/comments", response_model=CommentListResponse)
async def get_work_comments(
    work_id: str,
    skip: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=100),
    current_user: Optional[User] = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db)
):
    """
    获取作品的评论列表(只返回顶级评论,每个评论包含其回复)

    - **work_id**: 作品ID
    - **skip**: 跳过的记录数
    - **limit**: 每页数量
    """
    # 验证作品是否存在且已发布
    work_result = await db.execute(
        select(Work).where(Work.id == work_id, Work.is_published == True)
    )
    work = work_result.scalar_one_or_none()

    if not work:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="作品不存在或未发布"
        )

    # 查询顶级评论(parent_id为空的评论)
    query = (
        select(Comment)
        .where(
            Comment.work_id == work_id,
            Comment.parent_id == None,
            Comment.is_deleted == False
        )
        .options(
            selectinload(Comment.user),
            selectinload(Comment.reply_to_user)
        )
        .order_by(Comment.created_at.desc())
    )

    # 获取总数
    count_result = await db.execute(
        select(func.count(Comment.id)).where(
            Comment.work_id == work_id,
            Comment.parent_id == None,
            Comment.is_deleted == False
        )
    )
    total = count_result.scalar() or 0

    # 分页查询
    result = await db.execute(query.offset(skip).limit(limit))
    comments = result.scalars().all()

    # 构建响应数据
    items = []
    for comment in comments:
        # 查询该评论的所有回复
        replies_result = await db.execute(
            select(Comment)
            .where(
                Comment.parent_id == comment.id,
                Comment.is_deleted == False
            )
            .options(
                selectinload(Comment.user),
                selectinload(Comment.reply_to_user)
            )
            .order_by(Comment.created_at.asc())
        )
        replies = replies_result.scalars().all()

        # 检查当前用户是否点赞了该评论
        is_liked = False
        if current_user:
            like_result = await db.execute(
                select(CommentLike).where(
                    CommentLike.comment_id == comment.id,
                    CommentLike.user_id == current_user.id
                )
            )
            is_liked = like_result.scalar_one_or_none() is not None

        # 查询评论者对该作品的评分
        rating_result = await db.execute(
            select(WorkRating.rating).where(
                WorkRating.user_id == comment.user_id,
                WorkRating.work_id == work_id
            )
        )
        user_rating = rating_result.scalar_one_or_none()

        # 构建回复列表
        reply_responses = []
        for reply in replies:
            # 检查是否点赞回复
            reply_is_liked = False
            if current_user:
                reply_like_result = await db.execute(
                    select(CommentLike).where(
                        CommentLike.comment_id == reply.id,
                        CommentLike.user_id == current_user.id
                    )
                )
                reply_is_liked = reply_like_result.scalar_one_or_none() is not None

            # 查询回复者对该作品的评分
            reply_rating_result = await db.execute(
                select(WorkRating.rating).where(
                    WorkRating.user_id == reply.user_id,
                    WorkRating.work_id == work_id
                )
            )
            reply_user_rating = reply_rating_result.scalar_one_or_none()

            reply_responses.append(CommentResponse(
                id=str(reply.id),
                work_id=str(reply.work_id),
                user_id=str(reply.user_id),
                parent_id=str(reply.parent_id) if reply.parent_id else None,
                reply_to_user_id=str(reply.reply_to_user_id) if reply.reply_to_user_id else None,
                content=reply.content,
                like_count=reply.like_count,
                is_deleted=reply.is_deleted,
                created_at=reply.created_at,
                updated_at=reply.updated_at,
                user=UserInfo(
                    id=str(reply.user.id),
                    username=reply.user.username,
                    avatar=reply.user.avatar
                ),
                reply_to_user=UserInfo(
                    id=str(reply.reply_to_user.id),
                    username=reply.reply_to_user.username,
                    avatar=reply.reply_to_user.avatar
                ) if reply.reply_to_user else None,
                is_liked=reply_is_liked,
                reply_count=0,
                user_rating=reply_user_rating
            ))

        items.append(CommentWithRepliesResponse(
            id=str(comment.id),
            work_id=str(comment.work_id),
            user_id=str(comment.user_id),
            parent_id=None,
            reply_to_user_id=None,
            content=comment.content,
            like_count=comment.like_count,
            is_deleted=comment.is_deleted,
            created_at=comment.created_at,
            updated_at=comment.updated_at,
            user=UserInfo(
                id=str(comment.user.id),
                username=comment.user.username,
                avatar=comment.user.avatar
            ),
            reply_to_user=None,
            is_liked=is_liked,
            reply_count=len(replies),
            user_rating=user_rating,
            replies=reply_responses
        ))

    page = skip // limit + 1

    return CommentListResponse(
        total=total,
        page=page,
        page_size=limit,
        items=items
    )


@router.post("/works/{work_id}/comments", response_model=CommentResponse, status_code=status.HTTP_201_CREATED)
async def create_comment(
    work_id: str,
    comment_data: CommentCreate,
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db)
):
    """
    发表评论

    - **work_id**: 作品ID
    - **comment_data**: 评论内容
    """
    # 验证作品是否存在且已发布
    work_result = await db.execute(
        select(Work).where(Work.id == work_id, Work.is_published == True)
    )
    work = work_result.scalar_one_or_none()

    if not work:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="作品不存在或未发布"
        )

    # 如果是回复评论,验证父评论是否存在
    if comment_data.parent_id:
        parent_result = await db.execute(
            select(Comment).where(
                Comment.id == comment_data.parent_id,
                Comment.work_id == work_id,
                Comment.is_deleted == False
            )
        )
        parent_comment = parent_result.scalar_one_or_none()

        if not parent_comment:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="父评论不存在"
            )

    # 创建评论
    comment = Comment(
        work_id=work_id,
        user_id=current_user.id,
        content=comment_data.content,
        parent_id=comment_data.parent_id,
        reply_to_user_id=comment_data.reply_to_user_id
    )

    db.add(comment)
    await db.commit()
    await db.refresh(comment)

    # 加载关联数据
    await db.execute(
        select(Comment)
        .where(Comment.id == comment.id)
        .options(
            selectinload(Comment.user),
            selectinload(Comment.reply_to_user)
        )
    )
    await db.refresh(comment)

    # 查询评论者对该作品的评分
    rating_result = await db.execute(
        select(WorkRating.rating).where(
            WorkRating.user_id == current_user.id,
            WorkRating.work_id == work_id
        )
    )
    user_rating = rating_result.scalar_one_or_none()

    return CommentResponse(
        id=str(comment.id),
        work_id=str(comment.work_id),
        user_id=str(comment.user_id),
        parent_id=str(comment.parent_id) if comment.parent_id else None,
        reply_to_user_id=str(comment.reply_to_user_id) if comment.reply_to_user_id else None,
        content=comment.content,
        like_count=comment.like_count,
        is_deleted=comment.is_deleted,
        created_at=comment.created_at,
        updated_at=comment.updated_at,
        user=UserInfo(
            id=str(comment.user.id),
            username=comment.user.username,
            avatar=comment.user.avatar
        ),
        reply_to_user=UserInfo(
            id=str(comment.reply_to_user.id),
            username=comment.reply_to_user.username,
            avatar=comment.reply_to_user.avatar
        ) if comment.reply_to_user else None,
        is_liked=False,
        reply_count=0,
        user_rating=user_rating
    )


@router.put("/comments/{comment_id}", response_model=CommentResponse)
async def update_comment(
    comment_id: str,
    comment_data: CommentUpdate,
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db)
):
    """
    更新评论

    - **comment_id**: 评论ID
    - **comment_data**: 更新内容
    """
    # 查询评论
    result = await db.execute(
        select(Comment)
        .where(Comment.id == comment_id, Comment.is_deleted == False)
        .options(
            selectinload(Comment.user),
            selectinload(Comment.reply_to_user)
        )
    )
    comment = result.scalar_one_or_none()

    if not comment:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="评论不存在"
        )

    # 检查权限
    if str(comment.user_id) != str(current_user.id):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="无权修改此评论"
        )

    # 更新内容
    comment.content = comment_data.content

    await db.commit()
    await db.refresh(comment)

    # 检查是否点赞
    like_result = await db.execute(
        select(CommentLike).where(
            CommentLike.comment_id == comment.id,
            CommentLike.user_id == current_user.id
        )
    )
    is_liked = like_result.scalar_one_or_none() is not None

    # 查询评论者对该作品的评分
    rating_result = await db.execute(
        select(WorkRating.rating).where(
            WorkRating.user_id == current_user.id,
            WorkRating.work_id == comment.work_id
        )
    )
    user_rating = rating_result.scalar_one_or_none()

    return CommentResponse(
        id=str(comment.id),
        work_id=str(comment.work_id),
        user_id=str(comment.user_id),
        parent_id=str(comment.parent_id) if comment.parent_id else None,
        reply_to_user_id=str(comment.reply_to_user_id) if comment.reply_to_user_id else None,
        content=comment.content,
        like_count=comment.like_count,
        is_deleted=comment.is_deleted,
        created_at=comment.created_at,
        updated_at=comment.updated_at,
        user=UserInfo(
            id=str(comment.user.id),
            username=comment.user.username,
            avatar=comment.user.avatar
        ),
        reply_to_user=UserInfo(
            id=str(comment.reply_to_user.id),
            username=comment.reply_to_user.username,
            avatar=comment.reply_to_user.avatar
        ) if comment.reply_to_user else None,
        is_liked=is_liked,
        reply_count=0,
        user_rating=user_rating
    )


@router.delete("/comments/{comment_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_comment(
    comment_id: str,
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db)
):
    """
    删除评论(硬删除,直接从数据库删除)

    - **comment_id**: 评论ID
    """
    # 查询评论
    result = await db.execute(
        select(Comment).where(Comment.id == comment_id, Comment.is_deleted == False)
    )
    comment = result.scalar_one_or_none()

    if not comment:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="评论不存在"
        )

    # 检查权限
    if str(comment.user_id) != str(current_user.id):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="无权删除此评论"
        )

    # 硬删除 - 直接从数据库删除
    await db.delete(comment)
    await db.commit()


@router.post("/comments/{comment_id}/like", response_model=dict)
async def like_comment(
    comment_id: str,
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db)
):
    """
    点赞评论

    - **comment_id**: 评论ID
    """
    # 查询评论
    result = await db.execute(
        select(Comment).where(Comment.id == comment_id, Comment.is_deleted == False)
    )
    comment = result.scalar_one_or_none()

    if not comment:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="评论不存在"
        )

    # 检查是否已经点赞
    like_result = await db.execute(
        select(CommentLike).where(
            CommentLike.comment_id == comment_id,
            CommentLike.user_id == current_user.id
        )
    )
    existing_like = like_result.scalar_one_or_none()

    if existing_like:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="已经点赞过该评论"
        )

    # 创建点赞记录
    like = CommentLike(
        comment_id=comment_id,
        user_id=current_user.id
    )
    db.add(like)

    # 增加点赞数
    comment.like_count += 1

    await db.commit()

    return {
        "message": "点赞成功",
        "like_count": comment.like_count
    }


@router.delete("/comments/{comment_id}/like", response_model=dict)
async def unlike_comment(
    comment_id: str,
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db)
):
    """
    取消点赞评论

    - **comment_id**: 评论ID
    """
    # 查询评论
    result = await db.execute(
        select(Comment).where(Comment.id == comment_id, Comment.is_deleted == False)
    )
    comment = result.scalar_one_or_none()

    if not comment:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="评论不存在"
        )

    # 查询点赞记录
    like_result = await db.execute(
        select(CommentLike).where(
            CommentLike.comment_id == comment_id,
            CommentLike.user_id == current_user.id
        )
    )
    like = like_result.scalar_one_or_none()

    if not like:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="未点赞该评论"
        )

    # 删除点赞记录
    await db.delete(like)

    # 减少点赞数
    comment.like_count = max(0, comment.like_count - 1)

    await db.commit()

    return {
        "message": "取消点赞成功",
        "like_count": comment.like_count
    }


@router.post("/comments/{comment_id}/report", response_model=CommentReportResponse, status_code=status.HTTP_201_CREATED)
async def report_comment(
    comment_id: str,
    report_data: CommentReportCreate,
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db)
):
    """
    举报评论

    - **comment_id**: 评论ID
    - **reason**: 举报原因
    - **description**: 详细描述(可选)
    """
    # 验证评论是否存在
    comment_result = await db.execute(
        select(Comment).where(Comment.id == comment_id, Comment.is_deleted == False)
    )
    comment = comment_result.scalar_one_or_none()

    if not comment:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="评论不存在或已被删除"
        )

    # 检查是否已经举报过
    existing_report_result = await db.execute(
        select(CommentReport).where(
            CommentReport.comment_id == comment_id,
            CommentReport.user_id == current_user.id
        )
    )
    existing_report = existing_report_result.scalar_one_or_none()

    if existing_report:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="您已举报过此评论"
        )

    # 创建举报记录
    report = CommentReport(
        comment_id=comment_id,
        user_id=current_user.id,
        reason=report_data.reason,
        description=report_data.description
    )

    db.add(report)
    await db.commit()
    await db.refresh(report)

    return report
