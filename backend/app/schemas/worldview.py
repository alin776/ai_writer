"""
世界观相关 schemas
包括：Character（人物）、Location（地点）、Setting（设定）、WorkGuidelines（作品规范）、AIGuidelines（AI创作规范）
"""
from pydantic import BaseModel, Field, field_serializer, ConfigDict
from typing import Optional, List, Any, Dict
from datetime import datetime
from uuid import UUID
from app.models.worldview_change import WorldviewChangeStatus


# ==================== Character（人物） ====================

class EvidenceItem(BaseModel):
    """证据条目"""
    chapter_id: Optional[str] = None
    chapter_number: Optional[int] = None
    excerpt: Optional[str] = None
    source_type: Optional[str] = None
    confidence: Optional[float] = None


class CharacterBase(BaseModel):
    """人物基础模型"""
    name: str = Field(..., min_length=1, max_length=200)
    description: str
    avatar: Optional[str] = None
    role: Optional[str] = None
    status: Optional[str] = None
    voice: Optional[str] = None
    tags: Optional[List[str]] = None
    aliases: Optional[List[str]] = None
    relationships: Optional[List[Any]] = None
    constraints: Optional[List[str]] = None
    evidence: Optional[List[EvidenceItem]] = None


class CharacterCreate(CharacterBase):
    """创建人物"""
    work_id: str


class CharacterUpdate(BaseModel):
    """更新人物"""
    name: Optional[str] = Field(None, min_length=1, max_length=200)
    description: Optional[str] = None
    avatar: Optional[str] = None
    role: Optional[str] = None
    status: Optional[str] = None
    voice: Optional[str] = None
    tags: Optional[List[str]] = None
    aliases: Optional[List[str]] = None
    relationships: Optional[List[Any]] = None
    constraints: Optional[List[str]] = None
    evidence: Optional[List[EvidenceItem]] = None


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
    status: Optional[str] = None
    voice: Optional[str] = None
    tags: Optional[List[str]] = None
    related_locations: Optional[List[str]] = None
    aliases: Optional[List[str]] = None
    relations: Optional[List[Any]] = None
    constraints: Optional[List[str]] = None
    evidence: Optional[List[EvidenceItem]] = None


class LocationCreate(LocationBase):
    """创建地点"""
    work_id: str


class LocationUpdate(BaseModel):
    """更新地点"""
    name: Optional[str] = Field(None, min_length=1, max_length=200)
    description: Optional[str] = None
    image: Optional[str] = None
    type: Optional[str] = None
    status: Optional[str] = None
    voice: Optional[str] = None
    tags: Optional[List[str]] = None
    related_locations: Optional[List[str]] = None
    aliases: Optional[List[str]] = None
    relations: Optional[List[Any]] = None
    constraints: Optional[List[str]] = None
    evidence: Optional[List[EvidenceItem]] = None


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
    status: Optional[str] = None
    voice: Optional[str] = None
    tags: Optional[List[str]] = None
    related_items: Optional[List[Any]] = None
    aliases: Optional[List[str]] = None
    relations: Optional[List[Any]] = None
    constraints: Optional[List[str]] = None
    evidence: Optional[List[EvidenceItem]] = None


class SettingCreate(SettingBase):
    """创建设定"""
    work_id: str


class SettingUpdate(BaseModel):
    """更新设定"""
    title: Optional[str] = Field(None, min_length=1, max_length=200)
    category: Optional[str] = None
    content: Optional[str] = None
    status: Optional[str] = None
    voice: Optional[str] = None
    tags: Optional[List[str]] = None
    related_items: Optional[List[Any]] = None
    aliases: Optional[List[str]] = None
    relations: Optional[List[Any]] = None
    constraints: Optional[List[str]] = None
    evidence: Optional[List[EvidenceItem]] = None


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


# ==================== Glossary（术语表） ====================

class GlossaryTermBase(BaseModel):
    """术语表基础模型"""
    term: str = Field(..., min_length=1, max_length=200)
    definition: str
    aliases: Optional[List[str]] = None
    tags: Optional[List[str]] = None
    evidence: Optional[List[EvidenceItem]] = None


class GlossaryTermCreate(GlossaryTermBase):
    """创建术语"""
    work_id: str


class GlossaryTermUpdate(BaseModel):
    """更新术语"""
    term: Optional[str] = Field(None, min_length=1, max_length=200)
    definition: Optional[str] = None
    aliases: Optional[List[str]] = None
    tags: Optional[List[str]] = None
    evidence: Optional[List[EvidenceItem]] = None


class GlossaryTermResponse(GlossaryTermBase):
    """术语响应"""
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
    constraints: Optional[str] = None
    taboo: Optional[str] = None
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
    glossary: Optional[List[GlossaryTermResponse]] = None


# ==================== 世界观 Schema v1（按需加载） ====================

class WorldviewProfile(BaseModel):
    """世界观摘要统计（轻量）"""
    total_characters: int = 0
    total_locations: int = 0
    total_settings: int = 0
    total_glossary: int = 0
    has_guidelines: bool = False
    top_characters: List[str] = []
    top_locations: List[str] = []
    top_settings: List[str] = []
    top_glossary: List[str] = []


class WorldviewPack(BaseModel):
    """世界观按需小包（只返回当前任务必要条目）"""
    characters: List[Dict[str, Any]] = []
    locations: List[Dict[str, Any]] = []
    settings: List[Dict[str, Any]] = []
    guidelines: Optional[Dict[str, Any]] = None
    world_rules: Optional[List[str]] = None
    constraints: Optional[List[str]] = None
    taboo: Optional[List[str]] = None
    timeline: Optional[List[Dict[str, Any]]] = None
    glossary: Optional[List[Dict[str, Any]]] = None
    keywords: Optional[List[str]] = None


class WorldviewSchemaV1(BaseModel):
    """统一世界观数据结构（预留扩展）"""
    characters: List[Dict[str, Any]] = []
    locations: List[Dict[str, Any]] = []
    settings: List[Dict[str, Any]] = []
    guidelines: Optional[Dict[str, Any]] = None
    world_rules: Optional[List[str]] = None
    constraints: Optional[List[str]] = None
    taboo: Optional[List[str]] = None
    timeline: Optional[List[Dict[str, Any]]] = None
    glossary: Optional[List[Dict[str, Any]]] = None


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


class KnowledgeToWorldviewSyncRequest(BaseModel):
    """从知识文件同步到世界观卡片的请求"""
    touched_paths: Optional[List[str]] = None
    sync_mode: Optional[str] = "upsert"


class KnowledgeToWorldviewSyncResponse(BaseModel):
    """从知识文件同步到世界观卡片的响应"""
    status: str = "ok"
    created: Dict[str, int] = Field(default_factory=dict)
    updated: Dict[str, int] = Field(default_factory=dict)
    deleted: Dict[str, int] = Field(default_factory=dict)
    mirrored_files: List[str] = Field(default_factory=list)
    has_db_changes: bool = False
    parsed_counts: Dict[str, int] = Field(default_factory=dict)
    checked_files: List[str] = Field(default_factory=list)
    missing_files: List[str] = Field(default_factory=list)
    sync_mode: str = "upsert"


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


# ==================== 世界观回写闭环 Schema ====================

class WorldviewChangeCreateRequest(BaseModel):
    """创建 pending 世界观变更"""
    changes: WorldviewChangesResponse
    source: Optional[str] = Field("manual", description="来源：extract/scan/consistency/manual/other")
    selected_items: Optional[Dict[str, List[str]]] = None
    evidence: Optional[Dict[str, Any]] = None
    user_notes: Optional[str] = None


class WorldviewChangeApplyRequest(BaseModel):
    """应用世界观变更"""
    selected_items: Optional[Dict[str, List[str]]] = None
    user_notes: Optional[str] = None


class WorldviewChangeRejectRequest(BaseModel):
    """拒绝世界观变更"""
    user_notes: Optional[str] = None


class WorldviewChangeResponse(BaseModel):
    """世界观变更响应"""
    id: UUID
    work_id: UUID
    user_id: UUID
    applied_by: Optional[UUID] = None
    status: WorldviewChangeStatus
    source: Optional[str] = None
    changes: Dict[str, Any]
    selected_items: Optional[Dict[str, Any]] = None
    evidence: Optional[Dict[str, Any]] = None
    user_notes: Optional[str] = None
    version_before: Optional[int] = None
    version_after: Optional[int] = None
    apply_stats: Optional[Dict[str, Any]] = None
    created_at: datetime
    updated_at: datetime
    applied_at: Optional[datetime] = None

    model_config = ConfigDict(from_attributes=True)

    @field_serializer('id', 'work_id', 'user_id', 'applied_by')
    def serialize_uuid(self, value: Optional[UUID], _info) -> Optional[str]:
        return str(value) if value else None


class WorldviewChangeListResponse(BaseModel):
    """世界观变更列表响应"""
    total: int
    items: List[WorldviewChangeResponse]
