"""
章节评论 API 路由
支持章节级、段落级、句子级评论
"""
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func, and_, or_
from sqlalchemy.orm import selectinload
from typing import Optional, List
from uuid import UUID
import logging

from app.core.database import get_db
from app.core.security import get_current_active_user
from app.models.user import User
from app.models.chapter import Chapter
from app.models.chapter_comment import (
    ChapterComment,
    ChapterCommentLike,
    ChapterCommentReport,
)
from app.schemas.chapter_comment import (
    ChapterCommentCreate,
    ChapterCommentUpdate,
    ChapterCommentResponse,
    ChapterCommentWithReplies,
    ChapterCommentListResponse,
    CommentLocationStats,
    ChapterCommentLikeResponse,
    ChapterCommentReportCreate,
    ChapterCommentReportResponse,
    UserInfo,
)

router = APIRouter(prefix="/chapter-comments", tags=["章节评论"])
logger = logging.getLogger(__name__)


# ==================== 辅助函数 ====================

def build_comment_response(
    comment: ChapterComment,
    current_user_id: UUID,
    liked_comment_ids: set = None,
    reply_counts: dict = None
) -> ChapterCommentResponse:
    """构建评论响应对象"""
    if liked_comment_ids is None:
        liked_comment_ids = set()
    if reply_counts is None:
        reply_counts = {}

    return ChapterCommentResponse(
        id=comment.id,
        chapter_id=comment.chapter_id,
        user_id=comment.user_id,
        content=comment.content,
        location_type=comment.location_type,
        paragraph_index=comment.paragraph_index,
        sentence_index=comment.sentence_index,
        quoted_text=comment.quoted_text,
        parent_id=comment.parent_id,
        reply_to_user_id=comment.reply_to_user_id,
        like_count=comment.like_count,
        is_deleted=comment.is_deleted,
        created_at=comment.created_at,
        updated_at=comment.updated_at,
        user=UserInfo(
            id=comment.user.id,
            username=comment.user.username,
            avatar=comment.user.avatar
        ) if comment.user else None,
        reply_to_user=UserInfo(
            id=comment.reply_to_user.id,
            username=comment.reply_to_user.username,
            avatar=comment.reply_to_user.avatar
        ) if comment.reply_to_user else None,
        is_liked=comment.id in liked_comment_ids,
        reply_count=reply_counts.get(str(comment.id), 0)
    )


# ==================== 获取章节评论列表 ====================

@router.get("/chapters/{chapter_id}/comments", response_model=ChapterCommentListResponse)
async def get_chapter_comments(
    chapter_id: UUID,
    skip: int = Query(default=0, ge=0),
    limit: int = Query(default=20, ge=1, le=100),
    location_type: Optional[str] = Query(default=None, description="筛选位置类型"),
    paragraph_index: Optional[int] = Query(default=None, description="筛选段落索引"),
    sentence_index: Optional[int] = Query(default=None, description="筛选句子索引"),
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """获取章节评论列表"""
    # 验证章节存在
    chapter = await db.get(Chapter, chapter_id)
    if not chapter:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="章节不存在"
        )

    # 构建查询条件
    conditions = [
        ChapterComment.chapter_id == chapter_id,
        ChapterComment.is_deleted == False,
        ChapterComment.parent_id == None  # 只查询顶级评论
    ]

    if location_type:
        conditions.append(ChapterComment.location_type == location_type)
    if paragraph_index is not None:
        conditions.append(ChapterComment.paragraph_index == paragraph_index)
    if sentence_index is not None:
        conditions.append(ChapterComment.sentence_index == sentence_index)

    # 查询总数
    count_query = select(func.count(ChapterComment.id)).where(and_(*conditions))
    total_result = await db.execute(count_query)
    total = total_result.scalar()

    # 查询评论列表
    query = (
        select(ChapterComment)
        .options(
            selectinload(ChapterComment.user),
            selectinload(ChapterComment.reply_to_user),
            selectinload(ChapterComment.replies).selectinload(ChapterComment.user),
            selectinload(ChapterComment.replies).selectinload(ChapterComment.reply_to_user)
        )
        .where(and_(*conditions))
        .order_by(ChapterComment.created_at.desc())
        .offset(skip)
        .limit(limit)
    )
    result = await db.execute(query)
    comments = result.scalars().unique().all()

    # 获取当前用户点赞的评论
    all_comment_ids = set()
    for comment in comments:
        all_comment_ids.add(comment.id)
        for reply in comment.replies:
            all_comment_ids.add(reply.id)

    liked_query = select(ChapterCommentLike.comment_id).where(
        and_(
            ChapterCommentLike.user_id == current_user.id,
            ChapterCommentLike.comment_id.in_(all_comment_ids)
        )
    )
    liked_result = await db.execute(liked_query)
    liked_comment_ids = set(r[0] for r in liked_result.fetchall())

    # 统计回复数量
    reply_count_query = (
        select(
            ChapterComment.parent_id,
            func.count(ChapterComment.id).label('count')
        )
        .where(
            and_(
                ChapterComment.parent_id.in_([c.id for c in comments]),
                ChapterComment.is_deleted == False
            )
        )
        .group_by(ChapterComment.parent_id)
    )
    reply_count_result = await db.execute(reply_count_query)
    reply_counts = {str(r[0]): r[1] for r in reply_count_result.fetchall()}

    # 构建响应
    items = []
    for comment in comments:
        comment_response = build_comment_response(comment, current_user.id, liked_comment_ids, reply_counts)

        # 添加回复
        replies = []
        for reply in sorted(comment.replies, key=lambda x: x.created_at):
            if not reply.is_deleted:
                replies.append(build_comment_response(reply, current_user.id, liked_comment_ids, {}))

        items.append(ChapterCommentWithReplies(
            **comment_response.model_dump(),
            replies=replies
        ))

    return ChapterCommentListResponse(
        total=total,
        page=skip // limit + 1,
        page_size=limit,
        items=items
    )


# ==================== 获取评论位置统计 ====================

@router.get("/chapters/{chapter_id}/comments/stats", response_model=CommentLocationStats)
async def get_comment_stats(
    chapter_id: UUID,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """获取章节评论位置统计"""
    # 验证章节存在
    chapter = await db.get(Chapter, chapter_id)
    if not chapter:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="章节不存在"
        )

    # 查询所有未删除的评论
    query = select(ChapterComment).where(
        and_(
            ChapterComment.chapter_id == chapter_id,
            ChapterComment.is_deleted == False
        )
    )
    result = await db.execute(query)
    comments = result.scalars().all()

    # 统计各位置的评论数量
    chapter_count = 0
    paragraphs = {}
    sentences = {}

    for comment in comments:
        if comment.location_type == 'chapter':
            chapter_count += 1
        elif comment.location_type == 'paragraph' and comment.paragraph_index is not None:
            key = str(comment.paragraph_index)
            paragraphs[key] = paragraphs.get(key, 0) + 1
        elif comment.location_type == 'sentence' and comment.paragraph_index is not None and comment.sentence_index is not None:
            key = f"{comment.paragraph_index}-{comment.sentence_index}"
            sentences[key] = sentences.get(key, 0) + 1

    return CommentLocationStats(
        chapter=chapter_count,
        paragraphs=paragraphs,
        sentences=sentences,
        total=len(comments)
    )


# ==================== 创建评论 ====================

@router.post("/chapters/{chapter_id}/comments", response_model=ChapterCommentResponse, status_code=status.HTTP_201_CREATED)
async def create_chapter_comment(
    chapter_id: UUID,
    comment_data: ChapterCommentCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """创建章节评论"""
    # 验证章节存在
    chapter = await db.get(Chapter, chapter_id)
    if not chapter:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="章节不存在"
        )

    # 验证位置类型
    if comment_data.location_type not in ['chapter', 'paragraph', 'sentence']:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="无效的位置类型"
        )

    # 验证段落/句子索引
    if comment_data.location_type == 'paragraph' and comment_data.paragraph_index is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="段落级评论必须指定段落索引"
        )
    if comment_data.location_type == 'sentence':
        if comment_data.paragraph_index is None or comment_data.sentence_index is None:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="句子级评论必须指定段落和句子索引"
            )

    # 验证父评论存在（如果是回复）
    if comment_data.parent_id:
        parent_comment = await db.get(ChapterComment, comment_data.parent_id)
        if not parent_comment or parent_comment.is_deleted:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="父评论不存在"
            )
        if parent_comment.chapter_id != chapter_id:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="父评论不属于当前章节"
            )

    # 创建评论
    comment = ChapterComment(
        chapter_id=chapter_id,
        user_id=current_user.id,
        content=comment_data.content,
        location_type=comment_data.location_type,
        paragraph_index=comment_data.paragraph_index,
        sentence_index=comment_data.sentence_index,
        quoted_text=comment_data.quoted_text,
        parent_id=comment_data.parent_id,
        reply_to_user_id=comment_data.reply_to_user_id
    )

    db.add(comment)
    await db.commit()
    await db.refresh(comment)

    # 加载关联数据
    query = (
        select(ChapterComment)
        .options(
            selectinload(ChapterComment.user),
            selectinload(ChapterComment.reply_to_user)
        )
        .where(ChapterComment.id == comment.id)
    )
    result = await db.execute(query)
    comment = result.scalar_one()

    logger.info(f"用户 {current_user.username} 在章节 {chapter_id} 创建了评论")

    return build_comment_response(comment, current_user.id)


# ==================== 更新评论 ====================

@router.put("/{comment_id}", response_model=ChapterCommentResponse)
async def update_chapter_comment(
    comment_id: UUID,
    comment_data: ChapterCommentUpdate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """更新章节评论"""
    query = (
        select(ChapterComment)
        .options(
            selectinload(ChapterComment.user),
            selectinload(ChapterComment.reply_to_user)
        )
        .where(ChapterComment.id == comment_id)
    )
    result = await db.execute(query)
    comment = result.scalar_one_or_none()

    if not comment:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="评论不存在"
        )

    if comment.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="无权修改此评论"
        )

    if comment.is_deleted:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="评论已删除"
        )

    comment.content = comment_data.content
    await db.commit()
    await db.refresh(comment)

    return build_comment_response(comment, current_user.id)


# ==================== 删除评论 ====================

@router.delete("/{comment_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_chapter_comment(
    comment_id: UUID,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """删除章节评论"""
    comment = await db.get(ChapterComment, comment_id)

    if not comment:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="评论不存在"
        )

    # 检查权限：评论者本人或管理员
    if comment.user_id != current_user.id and current_user.role != 'admin':
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="无权删除此评论"
        )

    # 软删除
    comment.is_deleted = True
    await db.commit()

    logger.info(f"用户 {current_user.username} 删除了评论 {comment_id}")


# ==================== 点赞评论 ====================

@router.post("/{comment_id}/like", response_model=ChapterCommentLikeResponse)
async def like_chapter_comment(
    comment_id: UUID,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """点赞章节评论"""
    comment = await db.get(ChapterComment, comment_id)

    if not comment:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="评论不存在"
        )

    if comment.is_deleted:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="评论已删除"
        )

    # 检查是否已点赞
    existing_like = await db.execute(
        select(ChapterCommentLike).where(
            and_(
                ChapterCommentLike.comment_id == comment_id,
                ChapterCommentLike.user_id == current_user.id
            )
        )
    )
    if existing_like.scalar_one_or_none():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="已经点赞过了"
        )

    # 创建点赞
    like = ChapterCommentLike(
        comment_id=comment_id,
        user_id=current_user.id
    )
    db.add(like)

    # 更新点赞数
    comment.like_count = (comment.like_count or 0) + 1

    await db.commit()

    return ChapterCommentLikeResponse(
        success=True,
        like_count=comment.like_count,
        is_liked=True
    )


# ==================== 取消点赞 ====================

@router.delete("/{comment_id}/like", response_model=ChapterCommentLikeResponse)
async def unlike_chapter_comment(
    comment_id: UUID,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """取消点赞章节评论"""
    comment = await db.get(ChapterComment, comment_id)

    if not comment:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="评论不存在"
        )

    # 查找点赞记录
    like_result = await db.execute(
        select(ChapterCommentLike).where(
            and_(
                ChapterCommentLike.comment_id == comment_id,
                ChapterCommentLike.user_id == current_user.id
            )
        )
    )
    like = like_result.scalar_one_or_none()

    if not like:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="未点赞"
        )

    # 删除点赞
    await db.delete(like)

    # 更新点赞数
    comment.like_count = max(0, (comment.like_count or 0) - 1)

    await db.commit()

    return ChapterCommentLikeResponse(
        success=True,
        like_count=comment.like_count,
        is_liked=False
    )


# ==================== 举报评论 ====================

@router.post("/{comment_id}/report", response_model=ChapterCommentReportResponse, status_code=status.HTTP_201_CREATED)
async def report_chapter_comment(
    comment_id: UUID,
    report_data: ChapterCommentReportCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """举报章节评论"""
    comment = await db.get(ChapterComment, comment_id)

    if not comment:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="评论不存在"
        )

    if comment.user_id == current_user.id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="不能举报自己的评论"
        )

    # 检查是否已举报
    existing_report = await db.execute(
        select(ChapterCommentReport).where(
            and_(
                ChapterCommentReport.comment_id == comment_id,
                ChapterCommentReport.user_id == current_user.id
            )
        )
    )
    if existing_report.scalar_one_or_none():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="已经举报过了"
        )

    # 验证举报原因
    valid_reasons = ['spam', 'abuse', 'porn', 'illegal', 'false', 'other']
    if report_data.reason not in valid_reasons:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="无效的举报原因"
        )

    # 创建举报
    report = ChapterCommentReport(
        comment_id=comment_id,
        user_id=current_user.id,
        reason=report_data.reason,
        description=report_data.description
    )
    db.add(report)
    await db.commit()
    await db.refresh(report)

    logger.info(f"用户 {current_user.username} 举报了评论 {comment_id}，原因: {report_data.reason}")

    return ChapterCommentReportResponse(
        id=report.id,
        comment_id=report.comment_id,
        user_id=report.user_id,
        reason=report.reason,
        description=report.description,
        is_processed=report.is_processed,
        created_at=report.created_at
    )
