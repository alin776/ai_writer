from enum import Enum
from pydantic import BaseModel, Field, field_serializer
from typing import Optional, List, Dict, Any
from datetime import datetime
from uuid import UUID


# ==================== 枚举类型 ====================

class ReviewLevelEnum(str, Enum):
    """评审粒度枚举"""
    PARAGRAPH = "paragraph"
    CHAPTER = "chapter"
    WORK = "work"


class ReviewTypeEnum(str, Enum):
    """评审深度枚举"""
    QUICK = "quick"
    STANDARD = "standard"
    DEEP = "deep"


class TaskPriorityEnum(str, Enum):
    """任务优先级枚举"""
    P0 = "P0"
    P1 = "P1"
    P2 = "P2"


class TaskStatusEnum(str, Enum):
    """任务状态枚举"""
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    SKIPPED = "skipped"


class TaskSourceEnum(str, Enum):
    """任务来源枚举"""
    AI = "ai"
    MANUAL = "manual"


class VersionTypeEnum(str, Enum):
    """版本类型枚举"""
    SNAPSHOT = "snapshot"
    COMPRESSED = "compressed"
    ARCHIVED = "archived"


# ==================== 评审会话 Schema ====================

class ReviewSessionCreate(BaseModel):
    """创建评审会话请求"""
    review_type: ReviewTypeEnum = ReviewTypeEnum.STANDARD
    auto_generate_tasks: bool = True
    create_version: bool = True


class DimensionScores(BaseModel):
    """维度评分 (章节级8维度)"""
    literary_quality: Optional[float] = Field(None, ge=0, le=100, description="文学性")
    plot_logic: Optional[float] = Field(None, ge=0, le=100, description="情节合理性")
    character: Optional[float] = Field(None, ge=0, le=100, description="人物塑造")
    pacing: Optional[float] = Field(None, ge=0, le=100, description="节奏把控")
    scene: Optional[float] = Field(None, ge=0, le=100, description="场景描写")
    emotion: Optional[float] = Field(None, ge=0, le=100, description="情感感染力")
    foreshadowing: Optional[float] = Field(None, ge=0, le=100, description="伏笔铺垫")
    creativity: Optional[float] = Field(None, ge=0, le=100, description="创意新颖度")


class ReviewSessionResponse(BaseModel):
    """评审会话响应"""
    id: UUID
    user_id: UUID
    review_level: ReviewLevelEnum
    target_id: UUID
    overall_score: Optional[float]
    dimension_scores: Optional[Dict[str, float]]  # 改为 Dict 类型,更灵活
    highlights: Optional[List[str]]
    issues: Optional[List[str]]
    suggestions: Optional[List[str]]
    word_count: Optional[int]
    review_type: ReviewTypeEnum
    ai_model: Optional[str]
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

    @field_serializer('id', 'user_id', 'target_id')
    def serialize_uuid(self, value: UUID, _info) -> str:
        return str(value)


# ==================== 任务清单 Schema ====================

class TaskLocation(BaseModel):
    """任务定位信息"""
    paragraph_index: int = Field(..., description="段落序号")
    start_pos: int = Field(..., description="字符起始位置")
    end_pos: int = Field(..., description="字符结束位置")
    text_snippet: str = Field(..., max_length=100, description="原文片段(前50字)")


class ReviewTaskCreate(BaseModel):
    """创建任务请求"""
    chapter_id: UUID
    title: str = Field(..., min_length=1, max_length=200)
    description: str = Field(..., min_length=1)
    priority: TaskPriorityEnum = TaskPriorityEnum.P1
    category: Optional[str] = None
    location: Optional[TaskLocation] = None
    estimated_time: Optional[int] = None
    tags: Optional[List[str]] = None


class ReviewTaskUpdate(BaseModel):
    """更新任务请求"""
    title: Optional[str] = Field(None, min_length=1, max_length=200)
    description: Optional[str] = None
    priority: Optional[TaskPriorityEnum] = None
    category: Optional[str] = None
    status: Optional[TaskStatusEnum] = None
    user_notes: Optional[str] = None
    skipped_reason: Optional[str] = None
    sort_order: Optional[int] = None


class ReviewTaskStatusUpdate(BaseModel):
    """更新任务状态请求"""
    status: TaskStatusEnum
    notes: Optional[str] = None
    skipped_reason: Optional[str] = None


class ReviewTaskResponse(BaseModel):
    """任务响应"""
    id: UUID
    review_session_id: Optional[UUID]
    chapter_id: UUID
    user_id: UUID
    title: str
    description: str
    source: TaskSourceEnum
    location: Optional[Dict[str, Any]]
    priority: TaskPriorityEnum
    category: Optional[str]
    status: TaskStatusEnum
    related_score: Optional[str]
    current_score: Optional[int]
    estimated_time: Optional[int]
    tags: Optional[List[str]]
    depends_on: Optional[List[str]]
    blocks: Optional[List[str]]
    user_notes: Optional[str]
    completed_at: Optional[datetime]
    skipped_reason: Optional[str]
    sort_order: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

    @field_serializer('id', 'chapter_id', 'user_id')
    def serialize_uuid(self, value: UUID, _info) -> str:
        return str(value)

    @field_serializer('review_session_id')
    def serialize_optional_uuid(self, value: Optional[UUID], _info) -> Optional[str]:
        return str(value) if value else None


class ReviewTaskListResponse(BaseModel):
    """任务列表响应"""
    total: int
    items: List[ReviewTaskResponse]


class TaskStatsResponse(BaseModel):
    """任务统计响应"""
    total: int
    by_status: Dict[str, int] = Field(default_factory=dict, description="按状态统计")
    by_priority: Dict[str, int] = Field(default_factory=dict, description="按优先级统计")
    estimated_total_time: int = Field(default=0, description="总预估时间(分钟)")
    completion_rate: float = Field(default=0.0, ge=0, le=1, description="完成率")


class BatchOperationRequest(BaseModel):
    """批量操作请求"""
    action: str = Field(..., description="操作类型: complete/skip/delete/update_priority/reorder")
    task_ids: List[UUID]
    notes: Optional[str] = None
    reason: Optional[str] = None
    new_priority: Optional[TaskPriorityEnum] = None
    task_orders: Optional[List[Dict[str, Any]]] = None


# ==================== 版本管理 Schema ====================

class ChapterVersionCreate(BaseModel):
    """创建版本请求"""
    is_milestone: bool = False
    version_tag: Optional[str] = None
    change_summary: Optional[str] = None


class ChapterVersionResponse(BaseModel):
    """版本响应"""
    id: UUID
    chapter_id: UUID
    user_id: UUID
    version_number: int
    version_type: VersionTypeEnum
    is_milestone: bool
    version_tag: Optional[str]
    change_summary: Optional[str]
    review_session_id: Optional[UUID]
    overall_score: Optional[float]
    dimension_scores: Optional[Dict[str, float]]
    completed_tasks_count: int
    task_completion_rate: Optional[float]
    word_count: Optional[int]
    created_at: datetime
    archived_at: Optional[datetime]

    class Config:
        from_attributes = True

    @field_serializer('id', 'chapter_id', 'user_id')
    def serialize_uuid(self, value: UUID, _info) -> str:
        return str(value)

    @field_serializer('review_session_id')
    def serialize_optional_uuid(self, value: Optional[UUID], _info) -> Optional[str]:
        return str(value) if value else None


class ChapterVersionDetailResponse(ChapterVersionResponse):
    """版本详情响应 (包含内容)"""
    content: Optional[str] = None


class ChapterVersionListResponse(BaseModel):
    """版本列表响应"""
    total: int
    versions: List[ChapterVersionResponse]


class VersionCompareRequest(BaseModel):
    """版本对比请求"""
    version1_id: UUID
    version2_id: UUID


class ScoreDiff(BaseModel):
    """评分差异"""
    old: float
    new: float
    change: float


class VersionCompareResponse(BaseModel):
    """版本对比响应"""
    score_diff: Dict[str, ScoreDiff]
    text_diff: Dict[str, Any]
    completed_tasks: List[ReviewTaskResponse]


class VersionMilestoneUpdate(BaseModel):
    """更新里程碑请求"""
    is_milestone: bool
    version_tag: Optional[str] = None


# ==================== 章节评审完整响应 ====================

class ChapterReviewResponse(BaseModel):
    """章节评审完整响应"""
    session: ReviewSessionResponse
    generated_tasks: List[ReviewTaskResponse]
    version: Optional[ChapterVersionResponse] = None
