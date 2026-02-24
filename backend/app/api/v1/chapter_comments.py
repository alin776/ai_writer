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
from app.models.work import Work
from app.services.notification_service import NotificationService
from app.services.chapter_fs_helpers import get_chapters_dir, resolve_chapter_path
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

async def _validate_chapter_exists(db: AsyncSession, work_id: UUID, chapter_num: int):
    """验证作品存在且章节文件存在，返回 Work 对象"""
    work = await db.get(Work, work_id)
    if not work:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="作品不存在"
        )
    chapters_dir = get_chapters_dir(str(work.author_id), str(work_id))
    if resolve_chapter_path(chapters_dir, chapter_num) is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="章节不存在"
        )
    return work


def build_comment_tree(
    all_comments: list,
    current_user_id: UUID,
    liked_comment_ids: set,
    parent_id: UUID = None
) -> list:
    """构建两层评论结构（一级评论 + 平铺的回复）"""
    result = []
    for comment in all_comments:
        if comment.parent_id == parent_id:
            # 构建当前评论响应
            comment_response = ChapterCommentResponse(
                id=comment.id,
                work_id=comment.work_id,
                chapter_num=comment.chapter_num,
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
                reply_count=sum(1 for c in all_comments if c.parent_id == comment.id and not c.is_deleted)
            )

            # 两层结构：只获取直接回复，不递归
            # 所有 parent_id 指向当前评论的都是它的回复（已经是扁平化的）
            child_replies = []
            if parent_id is None:  # 只有一级评论才需要获取回复
                for reply in all_comments:
                    if reply.parent_id == comment.id and not reply.is_deleted:
                        reply_response = ChapterCommentResponse(
                            id=reply.id,
                            work_id=reply.work_id,
                            chapter_num=reply.chapter_num,
                            user_id=reply.user_id,
                            content=reply.content,
                            location_type=reply.location_type,
                            paragraph_index=reply.paragraph_index,
                            sentence_index=reply.sentence_index,
                            quoted_text=reply.quoted_text,
                            parent_id=reply.parent_id,
                            reply_to_user_id=reply.reply_to_user_id,
                            like_count=reply.like_count,
                            is_deleted=reply.is_deleted,
                            created_at=reply.created_at,
                            updated_at=reply.updated_at,
                            user=UserInfo(
                                id=reply.user.id,
                                username=reply.user.username,
                                avatar=reply.user.avatar
                            ) if reply.user else None,
                            reply_to_user=UserInfo(
                                id=reply.reply_to_user.id,
                                username=reply.reply_to_user.username,
                                avatar=reply.reply_to_user.avatar
                            ) if reply.reply_to_user else None,
                            is_liked=reply.id in liked_comment_ids,
                            reply_count=0  # 二级评论不再有子回复
                        )
                        child_replies.append(reply_response)
                # 按创建时间排序回复
                child_replies.sort(key=lambda x: x.created_at)

            result.append(ChapterCommentWithReplies(
                **comment_response.model_dump(),
                replies=child_replies
            ))

    # 按创建时间排序
    result.sort(key=lambda x: x.created_at)
    return result


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
        work_id=comment.work_id,
        chapter_num=comment.chapter_num,
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

@router.get("/works/{work_id}/chapters/{chapter_num}/comments", response_model=ChapterCommentListResponse)
async def get_chapter_comments(
    work_id: UUID,
    chapter_num: int,
    skip: int = Query(default=0, ge=0),
    limit: int = Query(default=20, ge=1, le=100),
    location_type: Optional[str] = Query(default=None, description="筛选位置类型"),
    paragraph_index: Optional[int] = Query(default=None, description="筛选段落索引"),
    sentence_index: Optional[int] = Query(default=None, description="筛选句子索引"),
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """获取章节评论列表（两层结构：一级评论 + 平铺回复）"""
    await _validate_chapter_exists(db, work_id, chapter_num)

    # 构建顶级评论查询条件
    top_level_conditions = [
        ChapterComment.work_id == work_id,
        ChapterComment.chapter_num == chapter_num,
        ChapterComment.is_deleted == False,
        ChapterComment.parent_id == None  # 只查询顶级评论用于分页
    ]

    if location_type:
        top_level_conditions.append(ChapterComment.location_type == location_type)
    if paragraph_index is not None:
        top_level_conditions.append(ChapterComment.paragraph_index == paragraph_index)
    if sentence_index is not None:
        top_level_conditions.append(ChapterComment.sentence_index == sentence_index)

    # 查询顶级评论总数
    count_query = select(func.count(ChapterComment.id)).where(and_(*top_level_conditions))
    total_result = await db.execute(count_query)
    total = total_result.scalar()

    # 查询顶级评论ID（用于分页）
    top_level_query = (
        select(ChapterComment.id)
        .where(and_(*top_level_conditions))
        .order_by(ChapterComment.created_at.desc())
        .offset(skip)
        .limit(limit)
    )
    top_level_result = await db.execute(top_level_query)
    top_level_ids = [r[0] for r in top_level_result.fetchall()]

    if not top_level_ids:
        return ChapterCommentListResponse(
            total=total,
            page=skip // limit + 1,
            page_size=limit,
            items=[]
        )

    # 两层结构：只获取一级评论的直接回复（不递归）
    reply_query = select(ChapterComment.id).where(
        and_(
            ChapterComment.parent_id.in_(top_level_ids),
            ChapterComment.is_deleted == False
        )
    )
    reply_result = await db.execute(reply_query)
    reply_ids = [r[0] for r in reply_result.fetchall()]

    # 合并所有需要查询的评论ID
    all_comment_ids = set(top_level_ids) | set(reply_ids)

    # 查询所有相关评论
    all_comments_query = (
        select(ChapterComment)
        .options(
            selectinload(ChapterComment.user),
            selectinload(ChapterComment.reply_to_user)
        )
        .where(ChapterComment.id.in_(all_comment_ids))
    )
    all_comments_result = await db.execute(all_comments_query)
    all_comments = list(all_comments_result.scalars().unique().all())

    # 获取当前用户点赞的评论
    liked_query = select(ChapterCommentLike.comment_id).where(
        and_(
            ChapterCommentLike.user_id == current_user.id,
            ChapterCommentLike.comment_id.in_(all_comment_ids)
        )
    )
    liked_result = await db.execute(liked_query)
    liked_comment_ids = set(r[0] for r in liked_result.fetchall())

    # 构建两层评论结构
    items = build_comment_tree(all_comments, current_user.id, liked_comment_ids, None)

    # 按创建时间倒序排列顶级评论
    items.sort(key=lambda x: x.created_at, reverse=True)

    return ChapterCommentListResponse(
        total=total,
        page=skip // limit + 1,
        page_size=limit,
        items=items
    )


# ==================== 获取评论位置统计 ====================

@router.get("/works/{work_id}/chapters/{chapter_num}/comments/stats", response_model=CommentLocationStats)
async def get_comment_stats(
    work_id: UUID,
    chapter_num: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """获取章节评论位置统计"""
    await _validate_chapter_exists(db, work_id, chapter_num)

    # 查询所有未删除的评论
    query = select(ChapterComment).where(
        and_(
            ChapterComment.work_id == work_id,
            ChapterComment.chapter_num == chapter_num,
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

@router.post("/works/{work_id}/chapters/{chapter_num}/comments", response_model=ChapterCommentResponse, status_code=status.HTTP_201_CREATED)
async def create_chapter_comment(
    work_id: UUID,
    chapter_num: int,
    comment_data: ChapterCommentCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """创建章节评论"""
    work = await _validate_chapter_exists(db, work_id, chapter_num)

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
    # 两层结构：所有回复的 parent_id 都指向一级评论（根评论）
    root_parent_id = None
    if comment_data.parent_id:
        parent_comment = await db.get(ChapterComment, comment_data.parent_id)
        if not parent_comment or parent_comment.is_deleted:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="父评论不存在"
            )
        if parent_comment.work_id != work_id or parent_comment.chapter_num != chapter_num:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="父评论不属于当前章节"
            )

        # 如果父评论本身有 parent_id，说明它是二级评论，需要找到根评论
        if parent_comment.parent_id:
            root_parent_id = parent_comment.parent_id
        else:
            # 父评论是一级评论，直接使用它的ID
            root_parent_id = comment_data.parent_id

    # 创建评论
    comment = ChapterComment(
        work_id=work_id,
        chapter_num=chapter_num,
        user_id=current_user.id,
        content=comment_data.content,
        location_type=comment_data.location_type,
        paragraph_index=comment_data.paragraph_index,
        sentence_index=comment_data.sentence_index,
        quoted_text=comment_data.quoted_text,
        parent_id=root_parent_id,  # 使用根评论ID，确保两层结构
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

    logger.info(f"用户 {current_user.username} 在作品 {work_id} 章节 {chapter_num} 创建了评论")

    # 如果是回复评论，发送通知给被回复者
    try:
        notify_user_id = None
        if comment_data.reply_to_user_id:
            notify_user_id = comment_data.reply_to_user_id
        elif comment_data.parent_id:
            # 查询父评论作者
            parent_comment = await db.get(ChapterComment, comment_data.parent_id)
            if parent_comment:
                notify_user_id = parent_comment.user_id

        # 如果有需要通知的用户，且不是自己
        if notify_user_id and notify_user_id != current_user.id:
            work_title = work.title if work else "未知作品"

            notification_service = NotificationService(db)
            comment_preview = comment_data.content[:50] + "..." if len(comment_data.content) > 50 else comment_data.content

            await notification_service.create_comment_reply_notification(
                recipient_user_id=notify_user_id,
                replier_name=current_user.username,
                replier_id=current_user.id,
                replier_avatar=current_user.avatar,
                comment_preview=comment_preview,
                work_id=str(work_id),
                work_title=work_title,
                comment_id=str(comment.id),
                parent_comment_id=str(comment_data.parent_id) if comment_data.parent_id else None,
                action_url=f"/library/novel-square?openNovel={work_id}&chapter={chapter_num}&chapterComment={comment.id}"
            )
            logger.info(f"已发送章节评论回复通知给用户 {notify_user_id}")
    except Exception as e:
        # 通知发送失败不影响评论创建
        logger.warning(f"发送章节评论回复通知失败: {e}")

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
