from enum import Enum
from pydantic import BaseModel, Field, field_serializer
from typing import Optional
from datetime import datetime
from uuid import UUID


class ChapterStatusEnum(str, Enum):
    """章节状态枚举"""
    DRAFT = "draft"
    PUBLISHED = "published"
    ARCHIVED = "archived"


class ChapterBase(BaseModel):
    """章节基础模型"""
    title: str = Field(..., min_length=1, max_length=200)
    content: str = ""


class ChapterCreate(ChapterBase):
    """创建章节"""
    work_id: UUID
    order: Optional[int] = None
    status: ChapterStatusEnum = ChapterStatusEnum.DRAFT
    is_published: Optional[bool] = None
    # 编辑事件唯一标识，用于幂等性检查
    edit_event_id: Optional[str] = Field(None, max_length=64)


class ChapterUpdate(BaseModel):
    """更新章节"""
    title: Optional[str] = Field(None, min_length=1, max_length=200)
    content: Optional[str] = None
    summary: Optional[str] = None
    order: Optional[int] = None
    is_published: Optional[bool] = None
    status: Optional[ChapterStatusEnum] = None
    # 编辑事件唯一标识，用于幂等性检查
    edit_event_id: Optional[str] = Field(None, max_length=64)


class ChapterResponse(ChapterBase):
    """章节响应"""
    id: UUID
    work_id: UUID
    order: int
    is_published: bool
    status: ChapterStatusEnum
    word_count: int
    view_count: int
    summary: Optional[str] = None
    created_at: datetime
    updated_at: datetime
    published_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True
    
    @field_serializer('id', 'work_id')
    def serialize_uuid(self, value: UUID, _info) -> str:
        """将 UUID 序列化为字符串"""
        return str(value)


class ChapterListResponse(BaseModel):
    """章节列表响应"""
    total: int
    items: list[ChapterResponse]


class ChapterSummaryResponse(BaseModel):
    """章节概括响应"""
    summary: str = Field(..., description="章节剧情概括")
