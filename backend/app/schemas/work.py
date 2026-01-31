from pydantic import BaseModel, Field, field_serializer
from typing import Optional
from datetime import datetime
from uuid import UUID
from app.models.work import WorkStatus, WorkGenre


class WorkBase(BaseModel):
    """作品基础模型"""
    title: str = Field(..., min_length=1, max_length=200)
    description: Optional[str] = None
    genre: WorkGenre = WorkGenre.OTHER
    status: WorkStatus = WorkStatus.DRAFT


class WorkCreate(WorkBase):
    """创建作品"""
    cover_image: Optional[str] = None


class WorkUpdate(BaseModel):
    """更新作品"""
    title: Optional[str] = Field(None, min_length=1, max_length=200)
    description: Optional[str] = None
    cover_image: Optional[str] = None
    genre: Optional[WorkGenre] = None
    status: Optional[WorkStatus] = None


class WorkResponse(WorkBase):
    """作品响应"""
    id: UUID
    author_id: UUID
    cover_image: Optional[str] = None
    total_words: int
    total_chapters: int
    view_count: int
    favorite_count: int = 0
    is_published: bool = False
    is_featured: bool = False
    created_at: datetime
    updated_at: datetime
    published_at: Optional[datetime] = None

    class Config:
        from_attributes = True

    @field_serializer('id', 'author_id')
    def serialize_uuid(self, value: UUID, _info) -> str:
        """将 UUID 序列化为字符串"""
        return str(value)


class WorkSummary(BaseModel):
    """作品汇总统计"""
    total_words: int = 0
    writing_count: int = 0
    weekly_new_words: int = 0


class WorkListResponse(BaseModel):
    """作品列表响应"""
    total: int
    page: int
    page_size: int
    items: list[WorkResponse]
    summary: Optional[WorkSummary] = None
