"""
关系Schema定义
"""
from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime
from uuid import UUID


class RelationshipBase(BaseModel):
    """关系基础Schema"""
    source_id: UUID
    source_type: str = Field(..., pattern="^(character|location|setting)$")
    target_id: UUID
    target_type: str = Field(..., pattern="^(character|location|setting)$")
    relationship_type: str
    label: str
    description: Optional[str] = None
    strength: int = Field(default=5, ge=1, le=10)
    direction: str = Field(default="one-way", pattern="^(one-way|two-way)$")
    start_chapter_id: Optional[UUID] = None
    end_chapter_id: Optional[UUID] = None
    color: Optional[str] = None
    line_style: str = Field(default="solid", pattern="^(solid|dashed|dotted)$")
    tags: Optional[List[str]] = None
    category: Optional[str] = None


class RelationshipCreate(RelationshipBase):
    """创建关系Schema"""
    work_id: UUID


class RelationshipUpdate(BaseModel):
    """更新关系Schema"""
    relationship_type: Optional[str] = None
    label: Optional[str] = None
    description: Optional[str] = None
    strength: Optional[int] = Field(default=None, ge=1, le=10)
    direction: Optional[str] = Field(default=None, pattern="^(one-way|two-way)$")
    start_chapter_id: Optional[UUID] = None
    end_chapter_id: Optional[UUID] = None
    color: Optional[str] = None
    line_style: Optional[str] = Field(default=None, pattern="^(solid|dashed|dotted)$")
    tags: Optional[List[str]] = None
    category: Optional[str] = None


class RelationshipResponse(RelationshipBase):
    """关系响应Schema"""
    id: UUID
    work_id: UUID
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class RelationshipListResponse(BaseModel):
    """关系列表响应"""
    items: List[RelationshipResponse]
    total: int
