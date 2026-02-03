"""
世界观相关 schemas
包括：Character（人物）、Location（地点）、Setting（设定）、WorkGuidelines（作品规范）、AIGuidelines（AI创作规范）
"""
from pydantic import BaseModel, Field, field_serializer, ConfigDict
from typing import Optional, List, Any, Dict
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
    
    model_config = ConfigDict(from_attributes=True, populate_by_name=True)
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
    
    model_config = ConfigDict(from_attributes=True, populate_by_name=True)
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
    
    model_config = ConfigDict(from_attributes=True, populate_by_name=True)
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
    
    model_config = ConfigDict(from_attributes=True, populate_by_name=True)
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


# ==================== 世界观同步相关 Schema ====================

class NewCharacterItem(BaseModel):
    """新增人物项"""
    name: str
    role: Optional[str] = "配角"
    description: Optional[str] = ""
    first_appearance: Optional[str] = None
    importance: Optional[str] = "中"
    tags: Optional[List[str]] = None


class UpdatedCharacterItem(BaseModel):
    """更新人物项"""
    name: str
    changes: str


class NewLocationItem(BaseModel):
    """新增地点项"""
    name: str
    type: Optional[str] = "场景"
    description: Optional[str] = ""
    importance: Optional[str] = "中"
    tags: Optional[List[str]] = None


class NewSettingItem(BaseModel):
    """新增设定项"""
    title: str
    category: Optional[str] = "剧情设定"
    content: Optional[str] = ""
    tags: Optional[List[str]] = None


class RelationshipChangeItem(BaseModel):
    """人物关系变化项"""
    from_character: str = Field(..., alias="from")
    to_character: str = Field(..., alias="to")
    old_relation: Optional[str] = None
    new_relation: str
    reason: Optional[str] = None

    model_config = ConfigDict(populate_by_name=True)
class WorldviewChangesResponse(BaseModel):
    """世界观变化响应"""
    new_characters: List[NewCharacterItem] = []
    updated_characters: List[UpdatedCharacterItem] = []
    new_locations: List[NewLocationItem] = []
    new_settings: List[NewSettingItem] = []
    relationship_changes: List[RelationshipChangeItem] = []
    scanned_chapters: Optional[int] = None  # 批量扫描时返回


class ExtractChangesRequest(BaseModel):
    """从单章提取变化的请求"""
    chapter_id: str
    chapter_content: Optional[str] = None  # 可选，如果不传则从数据库读取


class ScanChangesRequest(BaseModel):
    """批量扫描章节的请求"""
    start_chapter: int = 1
    end_chapter: Optional[int] = None
    limit: int = 10


class ApplyChangesRequest(BaseModel):
    """应用变化的请求"""
    changes: WorldviewChangesResponse
    selected_items: Optional[dict] = None  # 选择性应用


class ApplyChangesResponse(BaseModel):
    """应用变化的响应"""
    characters_created: int = 0
    characters_updated: int = 0
    locations_created: int = 0
    settings_created: int = 0
    relationships_created: int = 0


class WorldviewScanProgressResponse(BaseModel):
    """世界观扫描进度响应"""
    work_id: str
    status: str = "idle"
    scan_mode: Optional[str] = None
    chapters_total: int = 0
    chapters_processed: int = 0
    batches_total: int = 0
    batches_completed: int = 0
    progress_percentage: float = 0.0
    results: Optional[Dict[str, int]] = None
    last_error: Optional[str] = None
    updated_at: Optional[datetime] = None
