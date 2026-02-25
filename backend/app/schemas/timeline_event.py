"""
时间线事件Schema定义
"""
from pydantic import BaseModel, Field, ConfigDict, field_serializer
from typing import Optional, List
from datetime import datetime
from uuid import UUID


class TimelineEventBase(BaseModel):
    """时间线事件基础Schema"""
    entity_id: str  # 兼容 UUID 字符串和 FS 章节编号
    entity_type: str = Field(..., pattern="^(character|location|setting|relationship)$")
    event_type: str = Field(..., pattern="^(milestone|change|created|removed)$")
    title: str = Field(..., min_length=1, max_length=200)
    description: Optional[str] = None
    icon: Optional[str] = None
    chapter_id: Optional[str] = None  # 兼容 UUID 字符串和 FS 章节编号
    chapter_number: Optional[int] = None
    timestamp: Optional[int] = None
    color: Optional[str] = None


class TimelineEventCreate(TimelineEventBase):
    """创建时间线事件Schema"""
    work_id: UUID


class TimelineEventUpdate(BaseModel):
    """更新时间线事件Schema"""
    entity_id: Optional[str] = None
    entity_type: Optional[str] = Field(None, pattern="^(character|location|setting|relationship)$")
    event_type: Optional[str] = Field(None, pattern="^(milestone|change|created|removed)$")
    title: Optional[str] = Field(None, min_length=1, max_length=200)
    description: Optional[str] = None
    icon: Optional[str] = None
    chapter_id: Optional[str] = None
    chapter_number: Optional[int] = None
    timestamp: Optional[int] = None
    color: Optional[str] = None


class TimelineEventResponse(TimelineEventBase):
    """时间线事件响应Schema"""
    id: UUID
    work_id: UUID
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)

    @field_serializer('id', 'work_id')
    def serialize_uuid(self, value: UUID, _info) -> str:
        return str(value)


class TimelineEventListResponse(BaseModel):
    """时间线事件列表响应"""
    items: List[TimelineEventResponse]
    total: int


class ChapterAnchor(BaseModel):
    """章节锚点"""
    id: str
    chapter_id: str
    chapter_title: str
    chapter_number: int
    timestamp: int  # 在时间线上的位置


class TimelineTrack(BaseModel):
    """时间线轨道"""
    entity_id: str
    entity_type: str
    entity_label: str
    events: List[TimelineEventResponse]
