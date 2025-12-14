from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy import select, func, or_, and_
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload
from typing import Optional
import logging

from app.core.database import get_db
from app.core.security import get_current_active_user
from app.models.user import User
from app.models.work import Work, WorkGenre, WorkStatus
from app.models.chapter import Chapter
from app.models.rating import WorkRating
from pydantic import BaseModel

router = APIRouter()
logger = logging.getLogger(__name__)


class WorksListResponse(BaseModel):
    """管理员作品列表响应"""
    total: int
    page: int
    pageSize: int
    items: list


class TogglePublishRequest(BaseModel):
    """切换发布状态请求"""
    is_published: bool


class ToggleFeaturedRequest(BaseModel):
    """切换推荐状态请求"""
    is_featured: bool


def is_admin(user: User) -> bool:
    """检查用户是否是管理员"""
    return user.is_admin


@router.get("/works", response_model=WorksListResponse)
async def get_all_works(
    skip: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=100),
    search: Optional[str] = None,
    genre: Optional[WorkGenre] = None,
    status: Optional[WorkStatus] = None,
    is_published: Optional[bool] = None,
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db)
):
    """
    获取所有作品列表（管理员）

    - **skip**: 跳过的记录数
    - **limit**: 每页数量
    - **search**: 搜索关键词（标题或作者名）
    - **genre**: 作品类型筛选
    - **status**: 作品状态筛选
    - **is_published**: 发布状态筛选
    """
    # 检查管理员权限
    if not is_admin(current_user):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="需要管理员权限"
        )

    # 构建基础查询
    query = select(Work)
    count_query = select(func.count(Work.id))

    # 类型筛选
    if genre:
        query = query.where(Work.genre == genre)
        count_query = count_query.where(Work.genre == genre)

    # 状态筛选
    if status:
        query = query.where(Work.status == status)
        count_query = count_query.where(Work.status == status)

    # 发布状态筛选
    if is_published is not None:
        query = query.where(Work.is_published == is_published)
        count_query = count_query.where(Work.is_published == is_published)

    # 搜索功能
    if search:
        from app.models.user import User as UserModel
        query = query.join(Work.author).where(
            or_(
                Work.title.ilike(f"%{search}%"),
                UserModel.username.ilike(f"%{search}%")
            )
        )
        count_query = count_query.join(Work.author).where(
            or_(
                Work.title.ilike(f"%{search}%"),
                UserModel.username.ilike(f"%{search}%")
            )
        )

    # 获取总数
    total_result = await db.execute(count_query)
    total = total_result.scalar() or 0

    # 排序：推荐作品优先，然后按更新时间倒序
    query = query.order_by(Work.is_featured.desc(), Work.updated_at.desc())

    # 分页并加载作者信息
    query = query.options(selectinload(Work.author)).offset(skip).limit(limit)
    result = await db.execute(query)
    works = result.scalars().all()

    # 构建响应数据
    items = []
    for work in works:
        # 统计已发布章节数
        published_chapter_count_result = await db.execute(
            select(func.count(Chapter.id)).where(
                Chapter.work_id == work.id,
                Chapter.is_published == True
            )
        )
        published_chapter_count = published_chapter_count_result.scalar() or 0

        # 计算平均评分
        avg_rating_result = await db.execute(
            select(func.avg(WorkRating.rating)).where(
                WorkRating.work_id == work.id
            )
        )
        average_rating = avg_rating_result.scalar() or 0.0

        items.append({
            "id": str(work.id),
            "title": work.title,
            "description": work.description,
            "coverImage": work.cover_image,
            "genre": work.genre.value,
            "status": work.status.value,
            "totalWords": work.total_words,
            "totalChapters": work.total_chapters,
            "viewCount": work.view_count,
            "favoriteCount": work.favorite_count,
            "averageRating": round(average_rating, 1) if average_rating else 0.0,
            "isPublished": work.is_published,
            "isFeatured": work.is_featured,
            "publishedAt": work.published_at.isoformat() if work.published_at else None,
            "authorName": work.author.username,
            "authorId": str(work.author_id),
            "publishedChapterCount": published_chapter_count,
            "createdAt": work.created_at.isoformat(),
            "updatedAt": work.updated_at.isoformat()
        })

    page = skip // limit + 1

    return WorksListResponse(
        total=total,
        page=page,
        pageSize=limit,
        items=items
    )


@router.put("/works/{work_id}/publish")
async def toggle_work_publish(
    work_id: str,
    request: TogglePublishRequest,
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db)
):
    """
    切换作品发布状态（管理员）

    - **work_id**: 作品ID
    - **is_published**: 发布状态
    """
    # 检查管理员权限
    if not is_admin(current_user):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="需要管理员权限"
        )

    # 查询作品
    result = await db.execute(
        select(Work).where(Work.id == work_id)
    )
    work = result.scalar_one_or_none()

    if not work:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="作品不存在"
        )

    # 更新发布状态
    work.is_published = request.is_published

    # 如果是发布，设置发布时间
    if request.is_published and not work.published_at:
        from datetime import datetime, timezone
        work.published_at = datetime.now(timezone.utc)

    await db.commit()

    return {
        "message": "发布状态已更新",
        "workId": str(work_id),
        "isPublished": work.is_published
    }


@router.put("/works/{work_id}/feature")
async def toggle_work_featured(
    work_id: str,
    request: ToggleFeaturedRequest,
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db)
):
    """
    切换作品推荐状态（管理员）

    - **work_id**: 作品ID
    - **is_featured**: 推荐状态
    """
    # 检查管理员权限
    if not is_admin(current_user):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="需要管理员权限"
        )

    # 查询作品
    result = await db.execute(
        select(Work).where(Work.id == work_id)
    )
    work = result.scalar_one_or_none()

    if not work:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="作品不存在"
        )

    # 如果要设为推荐，检查作品是否已发布
    if request.is_featured and not work.is_published:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="只能推荐已发布的作品"
        )

    # 更新推荐状态
    work.is_featured = request.is_featured

    await db.commit()

    return {
        "message": "推荐状态已更新",
        "workId": str(work_id),
        "isFeatured": work.is_featured
    }


@router.delete("/works/{work_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_work(
    work_id: str,
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db)
):
    """
    删除作品（管理员）

    - **work_id**: 作品ID
    """
    # 检查管理员权限
    if not is_admin(current_user):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="需要管理员权限"
        )

    # 查询作品
    result = await db.execute(
        select(Work).where(Work.id == work_id)
    )
    work = result.scalar_one_or_none()

    if not work:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="作品不存在"
        )

    # 删除作品（会级联删除相关的章节、评论等）
    await db.delete(work)
    await db.commit()
