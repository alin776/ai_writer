"""
小说分析相关 schemas
包括：NovelAnalysis（小说分析）、微观分析、宏观分析报告
"""
from pydantic import BaseModel, Field, field_serializer, ConfigDict
from typing import Optional, List, Dict, Any
from datetime import datetime
from uuid import UUID
from enum import Enum


# ==================== Enums ====================

class AnalysisStatusEnum(str, Enum):
    """分析状态"""
    PENDING = "pending"
    ANALYZING = "analyzing"
    COMPLETED = "completed"
    FAILED = "failed"


class AnalysisStageEnum(str, Enum):
    """分析阶段"""
    MICRO_ANALYSIS = "micro_analysis"
    MACRO_ANALYSIS = "macro_analysis"
    COMPLETED = "completed"


# ==================== 微观分析结构 ====================

class EntityInvolved(BaseModel):
    """事件中涉及的实体"""
    type: str = Field(..., description="实体类型: Character | Location | Artifact")
    name: str = Field(..., description="实体名称")
    description: str = Field(..., description="本章节中的核心描述、初次登场状态或重要行为")


class DetailedEvent(BaseModel):
    """详细事件"""
    time_context: str = Field(..., description="事件发生的时间点或时间描述")
    action_summary: str = Field(..., description="事件的核心行为或转折点的简洁概括")
    entities_involved: List[EntityInvolved] = Field(default_factory=list, description="涉及的实体列表")


class MicroAnalysisChunk(BaseModel):
    """微观分析块（单个章节的分析结果）"""
    chapter_id: str = Field(..., description="章节ID")
    scene_id: Optional[str] = Field(None, description="场景ID（如章节被切分）")
    analysis_type: str = Field(default="Micro_Detail_Extraction", description="分析类型")
    detailed_events: List[DetailedEvent] = Field(default_factory=list, description="详细事件列表")
    chapter_theme: Optional[str] = Field(None, description="章节情感基调或核心主题")


# ==================== 宏观分析报告 ====================

class CharacterArcReport(BaseModel):
    """人物成长轨迹报告"""
    protagonist_name: Optional[str] = Field(None, description="主角名称")
    early_stage: Optional[str] = Field(None, description="故事初期的心理状态")
    middle_stage: Optional[str] = Field(None, description="故事中期的转变")
    late_stage: Optional[str] = Field(None, description="故事末期的状态")
    key_relationships: Optional[str] = Field(None, description="主要人物关系演变")


class WorldTimelineReport(BaseModel):
    """世界观图谱与时间线报告"""
    key_events: Optional[List[str]] = Field(None, description="五大关键历史事件或主要情节转折")
    major_locations: Optional[Dict[str, str]] = Field(None, description="主要地点及其功能关联")


class ConflictEvolutionReport(BaseModel):
    """核心矛盾演变报告"""
    early_conflict: Optional[str] = Field(None, description="初期核心矛盾")
    middle_conflict: Optional[str] = Field(None, description="中期核心矛盾")
    late_conflict: Optional[str] = Field(None, description="末期核心矛盾")


class MacroAnalysisReport(BaseModel):
    """宏观分析报告（三大报告）"""
    character_arc: Optional[CharacterArcReport] = Field(None, description="人物成长轨迹报告")
    world_timeline: Optional[WorldTimelineReport] = Field(None, description="世界观图谱与时间线报告")
    conflict_evolution: Optional[ConflictEvolutionReport] = Field(None, description="核心矛盾演变报告")
    raw_text: Optional[str] = Field(None, description="原始AI生成的完整报告文本")


# ==================== NovelAnalysis CRUD ====================

class NovelAnalysisCreate(BaseModel):
    """创建小说分析请求"""
    work_id: str = Field(..., description="作品ID")


class NovelAnalysisUpdate(BaseModel):
    """更新小说分析状态"""
    status: Optional[AnalysisStatusEnum] = None
    current_stage: Optional[AnalysisStageEnum] = None
    analyzed_chapters: Optional[int] = None
    micro_results: Optional[List[MicroAnalysisChunk]] = None
    macro_results: Optional[str] = None
    error_message: Optional[str] = None


class AnalysisProgress(BaseModel):
    """分析进度信息"""
    status: AnalysisStatusEnum
    current_stage: AnalysisStageEnum
    total_chapters: int
    analyzed_chapters: int
    progress_percentage: float = Field(..., description="进度百分比 0-100")
    error_message: Optional[str] = None


class NovelAnalysisResponse(BaseModel):
    """小说分析响应"""
    id: UUID
    work_id: UUID
    status: AnalysisStatusEnum
    current_stage: AnalysisStageEnum
    total_chapters: int
    analyzed_chapters: int
    progress_percentage: float
    micro_results: Optional[List[Dict[str, Any]]] = Field(None, description="微观分析JSON结果")
    macro_results: Optional[str] = Field(None, description="宏观分析报告文本")
    error_message: Optional[str] = None
    started_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None
    created_at: datetime
    updated_at: datetime
    
    model_config = ConfigDict(from_attributes=True, populate_by_name=True)
    @field_serializer('id', 'work_id')
    def serialize_uuid(self, value: UUID, _info) -> str:
        return str(value)


# ==================== 简化的分析结果 ====================

class NovelAnalysisSimple(BaseModel):
    """简化的分析结果（只返回状态和进度）"""
    id: UUID
    work_id: UUID
    status: AnalysisStatusEnum
    current_stage: AnalysisStageEnum
    progress_percentage: float
    error_message: Optional[str] = None
    
    model_config = ConfigDict(from_attributes=True, populate_by_name=True)
    @field_serializer('id', 'work_id')
    def serialize_uuid(self, value: UUID, _info) -> str:
        return str(value)
