from pydantic import BaseModel, Field, ConfigDict
from typing import Optional
from datetime import datetime
from uuid import UUID


class RatingCreate(BaseModel):
    """创建评分"""
    rating: int = Field(..., ge=1, le=5, description="评分(1-5)")


class RatingUpdate(BaseModel):
    """更新评分"""
    rating: int = Field(..., ge=1, le=5, description="评分(1-5)")


class RatingResponse(BaseModel):
    """评分响应"""
    id: UUID
    user_id: UUID
    work_id: UUID
    rating: int
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)
class WorkRatingStats(BaseModel):
    """作品评分统计"""
    average_rating: float = Field(..., description="平均评分")
    rating_count: int = Field(..., description="评分人数")
    rating_distribution: dict = Field(..., description="评分分布 {1: 10, 2: 5, 3: 20, 4: 30, 5: 35}")
    user_rating: Optional[int] = Field(None, description="当前用户的评分")
