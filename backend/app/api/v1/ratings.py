from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Optional
import logging

from app.core.database import get_db
from app.core.security import get_current_active_user
from app.models.user import User
from app.models.work import Work
from app.models.rating import WorkRating
from app.schemas.rating import RatingCreate, RatingUpdate, RatingResponse, WorkRatingStats

router = APIRouter()
logger = logging.getLogger(__name__)


@router.post("/works/{work_id}/rating", response_model=RatingResponse, status_code=status.HTTP_201_CREATED)
async def rate_work(
    work_id: str,
    rating_data: RatingCreate,
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db)
):
    """
    为作品评分(如果已评分则更新)
    """
    # 检查作品是否存在
    work_result = await db.execute(select(Work).where(Work.id == work_id))
    work = work_result.scalar_one_or_none()
    if not work:
        raise HTTPException(status_code=404, detail="作品不存在")

    # 检查是否已评分
    existing_rating_result = await db.execute(
        select(WorkRating).where(
            WorkRating.user_id == current_user.id,
            WorkRating.work_id == work_id
        )
    )
    existing_rating = existing_rating_result.scalar_one_or_none()

    if existing_rating:
        # 更新评分
        existing_rating.rating = rating_data.rating
        await db.commit()
        await db.refresh(existing_rating)
        return existing_rating
    else:
        # 创建新评分
        new_rating = WorkRating(
            user_id=current_user.id,
            work_id=work_id,
            rating=rating_data.rating
        )
        db.add(new_rating)
        await db.commit()
        await db.refresh(new_rating)
        return new_rating


@router.get("/works/{work_id}/rating/stats", response_model=WorkRatingStats)
async def get_work_rating_stats(
    work_id: str,
    current_user: Optional[User] = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db)
):
    """
    获取作品评分统计
    """
    # 检查作品是否存在
    work_result = await db.execute(select(Work).where(Work.id == work_id))
    work = work_result.scalar_one_or_none()
    if not work:
        raise HTTPException(status_code=404, detail="作品不存在")

    # 获取平均评分和评分人数
    stats_result = await db.execute(
        select(
            func.avg(WorkRating.rating).label('average'),
            func.count(WorkRating.id).label('count')
        ).where(WorkRating.work_id == work_id)
    )
    stats = stats_result.first()
    average_rating = float(stats.average) if stats.average else 0.0
    rating_count = stats.count

    # 获取评分分布
    distribution_result = await db.execute(
        select(
            WorkRating.rating,
            func.count(WorkRating.id).label('count')
        ).where(WorkRating.work_id == work_id)
        .group_by(WorkRating.rating)
    )
    distribution_data = distribution_result.all()
    rating_distribution = {i: 0 for i in range(1, 6)}  # 初始化1-5星
    for row in distribution_data:
        rating_distribution[row.rating] = row.count

    # 获取当前用户的评分
    user_rating = None
    if current_user:
        user_rating_result = await db.execute(
            select(WorkRating.rating).where(
                WorkRating.user_id == current_user.id,
                WorkRating.work_id == work_id
            )
        )
        user_rating_row = user_rating_result.first()
        if user_rating_row:
            user_rating = user_rating_row.rating

    return WorkRatingStats(
        average_rating=round(average_rating, 1),
        rating_count=rating_count,
        rating_distribution=rating_distribution,
        user_rating=user_rating
    )


@router.delete("/works/{work_id}/rating", status_code=status.HTTP_204_NO_CONTENT)
async def delete_work_rating(
    work_id: str,
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db)
):
    """
    删除作品评分
    """
    # 查找用户的评分
    rating_result = await db.execute(
        select(WorkRating).where(
            WorkRating.user_id == current_user.id,
            WorkRating.work_id == work_id
        )
    )
    rating = rating_result.scalar_one_or_none()

    if not rating:
        raise HTTPException(status_code=404, detail="评分不存在")

    await db.delete(rating)
    await db.commit()
