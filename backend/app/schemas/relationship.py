"""
关系Schema定义
"""
from pydantic import BaseModel, Field, ConfigDict
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

    model_config = ConfigDict(from_attributes=True)
class RelationshipListResponse(BaseModel):
    """关系列表响应"""
    items: List[RelationshipResponse]
    total: int


# ==================== AI 生成关系 Schema ====================

class NodeInfo(BaseModel):
    """节点信息"""
    id: UUID
    name: str
    type: str = Field(..., pattern="^(character|location|setting)$")
    description: Optional[str] = None


class AIGenerateRelationshipRequest(BaseModel):
    """AI生成关系请求"""
    work_id: UUID
    user_input: str = Field(..., min_length=1, max_length=500, description="用户的想法")
    source: NodeInfo
    target: NodeInfo
    relationship_type: str = Field(..., description="关系类型")
    direction: str = Field(default="one-way", pattern="^(one-way|two-way)$")


class AIGenerateRelationshipResponse(BaseModel):
    """AI生成关系响应"""
    label: str = Field(..., description="生成的标签")
    description: str = Field(..., description="生成的描述")
