"""
世界观相关 schemas
包括：Character（人物）、Location（地点）、Setting（设定）、WorkGuidelines（作品规范）、AIGuidelines（AI创作规范）
"""
from pydantic import BaseModel, Field, field_serializer
from typing import Optional, List, Any
from datetime import datetime
from uuid import UUID


# ==================== Character（人物） ====================

class CharacterBase(BaseModel):
    """人物基础模型"""
    name: str = Field(..., min_length=1, max_length=200)
    description: str
    avatar: Optional[str] = None
    role: Optional[str] = None
    tags: Optional[List[str]] = None
    relationships: Optional[List[Any]] = None


class CharacterCreate(CharacterBase):
    """创建人物"""
    work_id: str


class CharacterUpdate(BaseModel):
    """更新人物"""
    name: Optional[str] = Field(None, min_length=1, max_length=200)
    description: Optional[str] = None
    avatar: Optional[str] = None
    role: Optional[str] = None
    tags: Optional[List[str]] = None
    relationships: Optional[List[Any]] = None


class CharacterResponse(CharacterBase):
    """人物响应"""
    id: UUID
    work_id: UUID
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True
        populate_by_name = True
    
    @field_serializer('id', 'work_id')
    def serialize_uuid(self, value: UUID, _info) -> str:
        return str(value)


# ==================== Location（地点） ====================

class LocationBase(BaseModel):
    """地点基础模型"""
    name: str = Field(..., min_length=1, max_length=200)
    description: str
    image: Optional[str] = None
    type: Optional[str] = None
    tags: Optional[List[str]] = None
    related_locations: Optional[List[str]] = None


class LocationCreate(LocationBase):
    """创建地点"""
    work_id: str


class LocationUpdate(BaseModel):
    """更新地点"""
    name: Optional[str] = Field(None, min_length=1, max_length=200)
    description: Optional[str] = None
    image: Optional[str] = None
    type: Optional[str] = None
    tags: Optional[List[str]] = None
    related_locations: Optional[List[str]] = None


class LocationResponse(LocationBase):
    """地点响应"""
    id: UUID
    work_id: UUID
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True
        populate_by_name = True
    
    @field_serializer('id', 'work_id')
    def serialize_uuid(self, value: UUID, _info) -> str:
        return str(value)


# ==================== Setting（设定） ====================

class SettingBase(BaseModel):
    """设定基础模型"""
    title: str = Field(..., min_length=1, max_length=200)
    category: Optional[str] = None
    content: Optional[str] = None
    tags: Optional[List[str]] = None
    related_items: Optional[List[Any]] = None


class SettingCreate(SettingBase):
    """创建设定"""
    work_id: str


class SettingUpdate(BaseModel):
    """更新设定"""
    title: Optional[str] = Field(None, min_length=1, max_length=200)
    category: Optional[str] = None
    content: Optional[str] = None
    tags: Optional[List[str]] = None
    related_items: Optional[List[Any]] = None


class SettingResponse(SettingBase):
    """设定响应"""
    id: UUID
    work_id: UUID
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True
        populate_by_name = True
    
    @field_serializer('id', 'work_id')
    def serialize_uuid(self, value: UUID, _info) -> str:
        return str(value)


# ==================== WorkGuidelines（作品规范） ====================

class WorkGuidelinesBase(BaseModel):
    """作品规范基础模型"""
    outline: Optional[str] = None
    style: Optional[str] = None
    tone: Optional[str] = None
    words_per_chapter: Optional[int] = None
    update_frequency: Optional[str] = None
    power_system: Optional[str] = None
    world_rules: Optional[str] = None
    target_audience: Optional[str] = None
    main_theme: Optional[str] = None
    plot_direction: Optional[str] = None
    notes: Optional[str] = None


class WorkGuidelinesCreate(WorkGuidelinesBase):
    """创建作品规范"""
    work_id: str


class WorkGuidelinesUpdate(WorkGuidelinesBase):
    """更新作品规范"""
    pass


class WorkGuidelinesResponse(WorkGuidelinesBase):
    """作品规范响应"""
    id: UUID
    work_id: UUID
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True
        populate_by_name = True
    
    @field_serializer('id', 'work_id')
    def serialize_uuid(self, value: UUID, _info) -> str:
        return str(value)


# ==================== 世界观数据聚合响应 ====================

class WorldDataResponse(BaseModel):
    """世界观数据响应"""
    characters: List[CharacterResponse]
    locations: List[LocationResponse]
    settings: List[SettingResponse]
    guidelines: Optional[WorkGuidelinesResponse] = None
    ai_guidelines: Optional[Any] = None  # AIGuidelinesResponse
