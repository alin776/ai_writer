from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy import select, func, and_
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload
from typing import Optional, Dict, List
import logging
import uuid as uuid_module

from app.core.database import get_db
from app.core.security import get_current_active_user
from app.models.user import User
from app.models.work import Work
from app.models.comment import Comment, CommentLike, CommentDislike, CommentReport
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
from app.services.notification_service import NotificationService

router = APIRouter()
logger = logging.getLogger(__name__)


async def build_comment_tree(
    comment: Comment,
    all_comments_by_parent: Dict[str, List[Comment]],
    user_likes: set,
    user_dislikes: set,
    user_ratings: Dict[str, int],
    work_id: str,
    max_depth: int = 10,
    current_depth: int = 0
) -> CommentWithRepliesResponse:
    """
    递归构建评论树

    Args:
        comment: 当前评论
        all_comments_by_parent: 按 parent_id 分组的所有评论
        user_likes: 当前用户点赞的评论ID集合
        user_dislikes: 当前用户踩的评论ID集合
        user_ratings: 用户ID -> 评分的映射
        work_id: 作品ID
        max_depth: 最大递归深度
        current_depth: 当前深度
    """
    comment_id_str = str(comment.id)

    # 获取该评论的直接回复
    direct_replies = all_comments_by_parent.get(comment_id_str, [])

    # 递归构建子回复
    reply_responses = []
    if current_depth < max_depth:
        for reply in direct_replies:
            reply_response = await build_comment_tree(
                reply,
                all_comments_by_parent,
                user_likes,
                user_dislikes,
                user_ratings,
                work_id,
                max_depth,
                current_depth + 1
            )
            reply_responses.append(reply_response)

    # 计算总回复数（包括所有层级）
    def count_all_replies(parent_id: str) -> int:
        direct = all_comments_by_parent.get(parent_id, [])
        total = len(direct)
        for r in direct:
            total += count_all_replies(str(r.id))
        return total

    reply_count = count_all_replies(comment_id_str)

    return CommentWithRepliesResponse(
        id=comment_id_str,
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
        is_liked=comment_id_str in user_likes,
        is_disliked=comment_id_str in user_dislikes,
        reply_count=reply_count,
        user_rating=user_ratings.get(str(comment.user_id)),
        replies=reply_responses
    )


@router.get("/works/{work_id}/comments", response_model=CommentListResponse)
async def get_work_comments(
    work_id: str,
    skip: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=100),
    sort_by: str = Query("newest", regex="^(newest|most_liked)$"),
    current_user: Optional[User] = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db)
):
    """
    获取作品的评论列表(返回树形结构，支持无限层级嵌套)

    - **work_id**: 作品ID
    - **skip**: 跳过的记录数
    - **limit**: 每页数量
    - **sort_by**: 排序方式 (newest=最新, most_liked=最热)
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

    # 获取顶级评论总数（用于分页）
    count_result = await db.execute(
        select(func.count(Comment.id)).where(
            Comment.work_id == work_id,
            Comment.parent_id == None,
            Comment.is_deleted == False
        )
    )
    total = count_result.scalar() or 0

    # 根据排序方式设置排序条件
    if sort_by == "most_liked":
        order_clause = Comment.like_count.desc()
    else:  # newest
        order_clause = Comment.created_at.desc()

    # 查询顶级评论（分页）
    top_comments_result = await db.execute(
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
        .order_by(order_clause)
        .offset(skip)
        .limit(limit)
    )
    top_comments = top_comments_result.scalars().all()

    if not top_comments:
        return CommentListResponse(
            total=total,
            page=skip // limit + 1,
            page_size=limit,
            items=[]
        )

    # 一次性获取该作品的所有评论（用于构建树）
    all_comments_result = await db.execute(
        select(Comment)
        .where(
            Comment.work_id == work_id,
            Comment.is_deleted == False
        )
        .options(
            selectinload(Comment.user),
            selectinload(Comment.reply_to_user)
        )
    )
    all_comments = all_comments_result.scalars().all()

    # 按 parent_id 分组
    all_comments_by_parent: Dict[str, List[Comment]] = {}
    for c in all_comments:
        parent_key = str(c.parent_id) if c.parent_id else "root"
        if parent_key not in all_comments_by_parent:
            all_comments_by_parent[parent_key] = []
        all_comments_by_parent[parent_key].append(c)

    # 对每个分组按时间排序
    for key in all_comments_by_parent:
        all_comments_by_parent[key].sort(key=lambda x: x.created_at)

    # 获取当前用户的点赞/踩记录
    user_likes: set = set()
    user_dislikes: set = set()
    if current_user:
        likes_result = await db.execute(
            select(CommentLike.comment_id).where(
                CommentLike.user_id == current_user.id
            )
        )
        user_likes = {str(row[0]) for row in likes_result.fetchall()}

        dislikes_result = await db.execute(
            select(CommentDislike.comment_id).where(
                CommentDislike.user_id == current_user.id
            )
        )
        user_dislikes = {str(row[0]) for row in dislikes_result.fetchall()}

    # 获取所有评论者的评分
    commenter_ids = list({str(c.user_id) for c in all_comments})
    user_ratings: Dict[str, int] = {}
    if commenter_ids:
        ratings_result = await db.execute(
            select(WorkRating.user_id, WorkRating.rating).where(
                WorkRating.work_id == work_id,
                WorkRating.user_id.in_(commenter_ids)
            )
        )
        for row in ratings_result.fetchall():
            user_ratings[str(row[0])] = row[1]

    # 构建树形结构
    items = []
    for comment in top_comments:
        tree = await build_comment_tree(
            comment,
            all_comments_by_parent,
            user_likes,
            user_dislikes,
            user_ratings,
            work_id
        )
        items.append(tree)

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

    # 重新查询以加载关联数据
    result = await db.execute(
        select(Comment)
        .where(Comment.id == comment.id)
        .options(
            selectinload(Comment.user),
            selectinload(Comment.reply_to_user)
        )
    )
    comment = result.scalar_one()
    # 如果是回复评论，发送通知给被回复者
    try:
        # 确定需要通知的用户ID（优先使用 reply_to_user_id，否则使用父评论作者）
        notify_user_id = None
        if comment_data.reply_to_user_id:
            notify_user_id = comment_data.reply_to_user_id
        elif comment_data.parent_id:
            # 查询父评论作者
            parent_result = await db.execute(
                select(Comment.user_id).where(Comment.id == comment_data.parent_id)
            )
            parent_user_id = parent_result.scalar_one_or_none()
            if parent_user_id:
                notify_user_id = parent_user_id

        # 如果有需要通知的用户，且不是自己，发送通知
        if notify_user_id and str(notify_user_id) != str(current_user.id):
            notification_service = NotificationService(db)
            comment_preview = comment_data.content[:50] + "..." if len(comment_data.content) > 50 else comment_data.content
            # 确保 recipient_user_id 是 UUID 类型
            recipient_uuid = uuid_module.UUID(str(notify_user_id)) if isinstance(notify_user_id, str) else notify_user_id
            await notification_service.create_comment_reply_notification(
                recipient_user_id=recipient_uuid,
                replier_name=current_user.username,
                replier_id=current_user.id,
                replier_avatar=current_user.avatar,
                comment_preview=comment_preview,
                work_id=work_id,
                work_title=work.title,
                comment_id=str(comment.id),
                parent_comment_id=comment_data.parent_id,
                action_url=f"/library/novel-square?openNovel={work_id}&comment={comment.id}"
            )
    except Exception as e:
        # 通知发送失败不影响评论创建
        logger.warning(f"发送评论回复通知失败: {e}")

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
        is_disliked=False,
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

    # 检查是否踩
    dislike_result = await db.execute(
        select(CommentDislike).where(
            CommentDislike.comment_id == comment.id,
            CommentDislike.user_id == current_user.id
        )
    )
    is_disliked = dislike_result.scalar_one_or_none() is not None

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
        is_disliked=is_disliked,
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

    # 如果已经踩过，先取消踩（点赞和踩互斥）
    dislike_result = await db.execute(
        select(CommentDislike).where(
            CommentDislike.comment_id == comment_id,
            CommentDislike.user_id == current_user.id
        )
    )
    existing_dislike = dislike_result.scalar_one_or_none()
    if existing_dislike:
        await db.delete(existing_dislike)
        comment.dislike_count = max(0, comment.dislike_count - 1)

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


@router.post("/comments/{comment_id}/dislike", response_model=dict)
async def dislike_comment(
    comment_id: str,
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db)
):
    """
    踩评论

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

    # 检查是否已经踩过
    dislike_result = await db.execute(
        select(CommentDislike).where(
            CommentDislike.comment_id == comment_id,
            CommentDislike.user_id == current_user.id
        )
    )
    existing_dislike = dislike_result.scalar_one_or_none()

    if existing_dislike:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="已经踩过该评论"
        )

    # 如果已经点赞过，先取消点赞（点赞和踩互斥）
    like_result = await db.execute(
        select(CommentLike).where(
            CommentLike.comment_id == comment_id,
            CommentLike.user_id == current_user.id
        )
    )
    existing_like = like_result.scalar_one_or_none()
    if existing_like:
        await db.delete(existing_like)
        comment.like_count = max(0, comment.like_count - 1)

    # 创建踩记录
    dislike = CommentDislike(
        comment_id=comment_id,
        user_id=current_user.id
    )
    db.add(dislike)

    # 增加踩数
    comment.dislike_count += 1

    await db.commit()

    return {
        "message": "踩成功",
        "dislike_count": comment.dislike_count
    }


@router.delete("/comments/{comment_id}/dislike", response_model=dict)
async def undislike_comment(
    comment_id: str,
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db)
):
    """
    取消踩评论

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

    # 查询踩记录
    dislike_result = await db.execute(
        select(CommentDislike).where(
            CommentDislike.comment_id == comment_id,
            CommentDislike.user_id == current_user.id
        )
    )
    dislike = dislike_result.scalar_one_or_none()

    if not dislike:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="未踩该评论"
        )

    # 删除踩记录
    await db.delete(dislike)

    # 减少踩数
    comment.dislike_count = max(0, comment.dislike_count - 1)

    await db.commit()

    return {
        "message": "取消踩成功",
        "dislike_count": comment.dislike_count
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
