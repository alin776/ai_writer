from enum import Enum
from pydantic import BaseModel, Field, field_serializer, ConfigDict
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

    model_config = ConfigDict(from_attributes=True)
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

    model_config = ConfigDict(from_attributes=True)
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

    model_config = ConfigDict(from_attributes=True)
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


# ==================== 段落级评审 Schema ====================

class ParagraphReviewRequest(BaseModel):
    """段落评审请求"""
    text: str = Field(..., min_length=50, max_length=2000, description="段落文本 (50-2000字)")
    context: Optional[str] = Field(default=None, max_length=500, description="上下文信息 (可选)")

    model_config = ConfigDict(json_schema_extra={
        "example": {
            "text": "林风深吸一口气，推开木门。房间里灰尘飞舞，一把古剑静静地躺在桌上，散发着淡淡的青光。",
            "context": "这是主角第一次进入师父的密室"
        }
    })


class ParagraphDimensionScores(BaseModel):
    """段落评审维度分数"""
    language: float = Field(..., ge=0, le=100, description="语言质量")
    vividness: float = Field(..., ge=0, le=100, description="描写生动度")
    dialogue: float = Field(..., ge=0, le=100, description="对话真实性")
    emotion: float = Field(..., ge=0, le=100, description="情感表达")


class ParagraphReviewResponse(BaseModel):
    """段落评审响应"""
    overall_score: float = Field(..., ge=0, le=100, description="总分")
    dimension_scores: ParagraphDimensionScores = Field(..., description="4维度评分")
    quick_feedback: str = Field(..., max_length=200, description="简短反馈")
    suggestions: List[str] = Field(default_factory=list, description="改进建议")

    model_config = ConfigDict(json_schema_extra={
        "example": {
            "overall_score": 82.5,
            "dimension_scores": {
                "language": 85,
                "vividness": 88,
                "dialogue": 75,
                "emotion": 82
            },
            "quick_feedback": "语言流畅，环境描写生动，但对话略显僵硬",
            "suggestions": [
                "可以加入人物的内心独白，增强情感表达",
                "对话可以更口语化，更贴近人物性格"
            ]
        }
    })


# ==================== 作品级评审 Schema ====================

class ChapterInput(BaseModel):
    """章节输入"""
    title: str = Field(..., description="章节标题")
    content: str = Field(..., description="章节内容")
    order: int = Field(..., ge=1, description="章节顺序")


class BookReviewRequest(BaseModel):
    """作品级评审请求"""
    novel_id: UUID = Field(..., description="小说ID")
    book_title: str = Field(..., min_length=1, max_length=200, description="书名")
    chapters: List[ChapterInput] = Field(..., min_items=3, description="章节列表 (至少3章)")
    author_notes: Optional[str] = Field(None, max_length=1000, description="作者备注")
    quick_mode: bool = Field(default=False, description="快速模式 (仅分析前10章)")

    model_config = ConfigDict(json_schema_extra={
        "example": {
            "novel_id": "123e4567-e89b-12d3-a456-426614174000",
            "book_title": "剑仙传说",
            "chapters": [
                {"title": "第一章 入门", "content": "林风来到剑宗山门...", "order": 1},
                {"title": "第二章 试炼", "content": "试炼大会开始了...", "order": 2},
                {"title": "第三章 突破", "content": "林风终于突破了...", "order": 3}
            ],
            "author_notes": "这是我的第一部作品",
            "quick_mode": False
        }
    })


class PlotAnalysis(BaseModel):
    """情节分析结果"""
    structure_type: str = Field(..., description="结构类型")
    acts: List[Dict[str, Any]] = Field(..., description="章节分幕")
    climax_points: List[int] = Field(..., description="高潮章节")
    rhythm_score: float = Field(..., ge=0, le=100, description="节奏评分")
    rhythm_analysis: str = Field(..., description="节奏分析")
    foreshadowing: Dict[str, Any] = Field(..., description="伏笔分析")
    issues: List[str] = Field(..., description="问题列表")
    strengths: List[str] = Field(..., description="优点列表")


class CharacterAnalysis(BaseModel):
    """人物分析结果"""
    main_characters: List[Dict[str, Any]] = Field(..., description="主要角色")
    relationships: List[Dict[str, Any]] = Field(..., description="人物关系")
    character_score: float = Field(..., ge=0, le=100, description="人物塑造评分")
    issues: List[str] = Field(..., description="问题列表")
    strengths: List[str] = Field(..., description="优点列表")


class WorldviewAnalysis(BaseModel):
    """世界观分析结果"""
    setting: Dict[str, Any] = Field(..., description="背景设定")
    rules: List[str] = Field(..., description="规则列表")
    uniqueness_score: float = Field(..., ge=0, le=100, description="独特性评分")
    consistency_score: float = Field(..., ge=0, le=100, description="一致性评分")
    depth_score: float = Field(..., ge=0, le=100, description="深度评分")
    issues: List[str] = Field(..., description="问题列表")
    strengths: List[str] = Field(..., description="优点列表")


class WritingStyleAnalysis(BaseModel):
    """文风分析结果"""
    style_tags: List[str] = Field(..., description="风格标签")
    language_score: float = Field(..., ge=0, le=100, description="语言评分")
    description_score: float = Field(..., ge=0, le=100, description="描写评分")
    dialogue_score: float = Field(..., ge=0, le=100, description="对话评分")
    readability_score: float = Field(..., ge=0, le=100, description="可读性评分")
    analysis: str = Field(..., description="整体分析")
    issues: List[str] = Field(..., description="问题列表")
    strengths: List[str] = Field(..., description="优点列表")


class Recommendations(BaseModel):
    """综合建议"""
    core_strengths: List[str] = Field(..., description="核心优势")
    critical_issues: List[str] = Field(..., description="关键问题")
    priority_actions: List[Dict[str, Any]] = Field(..., description="优先修改建议")
    next_steps: str = Field(..., description="下一步建议")


class BookReviewResponse(BaseModel):
    """作品级评审响应"""
    book_title: str = Field(..., description="书名")
    novel_id: str = Field(..., description="小说ID")
    total_chapters: int = Field(..., description="章节总数")
    analysis_date: str = Field(..., description="分析日期")
    overall_score: float = Field(..., ge=0, le=100, description="综合评分")
    plot_analysis: PlotAnalysis = Field(..., description="情节分析")
    character_analysis: CharacterAnalysis = Field(..., description="人物分析")
    worldview_analysis: WorldviewAnalysis = Field(..., description="世界观分析")
    writing_style: WritingStyleAnalysis = Field(..., description="文风分析")
    recommendations: Recommendations = Field(..., description="综合建议")
    is_quick_review: Optional[bool] = Field(default=False, description="是否快速评审")
    sampled_chapters: Optional[int] = Field(default=None, description="采样章节数")

    model_config = ConfigDict(json_schema_extra={
        "example": {
            "book_title": "剑仙传说",
            "novel_id": "123e4567-e89b-12d3-a456-426614174000",
            "total_chapters": 20,
            "analysis_date": "2025-10-26T21:30:00",
            "overall_score": 82.5,
            "plot_analysis": {
                "structure_type": "三幕式结构",
                "acts": [
                    {"act": 1, "chapters": [1, 5], "summary": "世界观建立"},
                    {"act": 2, "chapters": [6, 15], "summary": "冲突升级"}
                ],
                "climax_points": [5, 10, 18],
                "rhythm_score": 85,
                "rhythm_analysis": "节奏控制良好，高潮分布合理",
                "foreshadowing": {"count": 5, "examples": []},
                "issues": ["中期节奏略显拖沓"],
                "strengths": ["开局吸引人", "高潮设计合理"]
            },
            "character_analysis": {
                "main_characters": [
                    {"name": "林风", "role": "主角", "traits": ["坚韧", "聪明"]}
                ],
                "relationships": [],
                "character_score": 80,
                "issues": ["配角塑造不足"],
                "strengths": ["主角性格鲜明"]
            },
            "worldview_analysis": {
                "setting": {"era": "修仙时代", "location": "东洲大陆"},
                "rules": ["修炼体系", "宗门制度"],
                "uniqueness_score": 75,
                "consistency_score": 90,
                "depth_score": 80,
                "issues": [],
                "strengths": ["世界观逻辑严谨"]
            },
            "writing_style": {
                "style_tags": ["简洁", "流畅"],
                "language_score": 85,
                "description_score": 80,
                "dialogue_score": 88,
                "readability_score": 90,
                "analysis": "文风简洁流畅，适合网文阅读",
                "issues": [],
                "strengths": ["语言精练"]
            },
            "recommendations": {
                "core_strengths": ["情节紧凑", "人物鲜明"],
                "critical_issues": ["配角需要加强"],
                "priority_actions": [
                    {"priority": 1, "action": "丰富配角", "reason": "增强故事层次"}
                ],
                "next_steps": "继续保持节奏，加强配角塑造"
            },
            "is_quick_review": False
        }
    })
