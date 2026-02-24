"""
时间线事件Schema定义
"""
from pydantic import BaseModel, Field, ConfigDict
from typing import Optional, List
from datetime import datetime
from uuid import UUID


class TimelineEventBase(BaseModel):
    """时间线事件基础Schema"""
    entity_id: UUID
    entity_type: str = Field(..., pattern="^(character|location|setting|relationship)$")
    event_type: str = Field(..., pattern="^(milestone|change|created|removed)$")
    title: str = Field(..., min_length=1, max_length=200)
    description: Optional[str] = None
    icon: Optional[str] = None
    chapter_id: Optional[UUID] = None
    chapter_number: Optional[int] = None
    timestamp: Optional[int] = None
    color: Optional[str] = None


class TimelineEventCreate(TimelineEventBase):
    """创建时间线事件Schema"""
    work_id: UUID


class TimelineEventUpdate(BaseModel):
    """更新时间线事件Schema"""
    entity_id: Optional[UUID] = None
    entity_type: Optional[str] = Field(None, pattern="^(character|location|setting|relationship)$")
    event_type: Optional[str] = Field(None, pattern="^(milestone|change|created|removed)$")
    title: Optional[str] = Field(None, min_length=1, max_length=200)
    description: Optional[str] = None
    icon: Optional[str] = None
    chapter_id: Optional[UUID] = None
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
    entity_id: UUID
    entity_type: str
    entity_label: str
    events: List[TimelineEventResponse]
