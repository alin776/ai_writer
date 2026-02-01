from pydantic import BaseModel, Field, field_validator, ConfigDict
from typing import Optional, Literal, Dict, List, Any
from datetime import datetime
from uuid import UUID


# ========== AI特征检测相关 ==========

class DimensionScore(BaseModel):
    """单维度评分"""
    score: float = Field(..., ge=0, le=100, description="分数 (0-100)")
    description: str = Field(..., description="维度说明")
    issues: List[str] = Field(default_factory=list, description="检测到的问题列表")


class AIDetectionResult(BaseModel):
    """AI特征检测结果"""
    overall_score: float = Field(..., ge=0, le=100, description="总体AI特征分数 (0-100)")

    # 七维度评分（V2优化版）
    dimensions: Dict[str, DimensionScore] = Field(
        ...,
        description="七维度评分详情",
        example={
            "pattern_repetition": {"score": 75, "description": "模式重复", "issues": []},
            "word_choice": {"score": 80, "description": "词汇选择", "issues": []},
            "sentence_structure": {"score": 65, "description": "句式结构", "issues": []},
            "tone_style": {"score": 70, "description": "语气风格", "issues": []},
            "formatting": {"score": 60, "description": "格式规范", "issues": []},
            "emotional_expression": {"score": 75, "description": "情感表达", "issues": []},
            "coherence_flow": {"score": 80, "description": "连贯性", "issues": []}
        }
    )

    detected_patterns: List[str] = Field(
        default_factory=list,
        description="检测到的AI痕迹列表"
    )

    needs_humanization: bool = Field(..., description="是否需要去痕迹")


# ========== 去痕迹请求/响应 ==========

class HumanizeRequest(BaseModel):
    """去痕迹请求"""
    text: str = Field(..., min_length=10, max_length=5000, description="待去痕迹的文本（最大5000字符）")
    intensity: Literal["light", "medium", "strong"] = Field(
        default="medium",
        description="去痕迹强度: light(5%改动), medium(15-20%改动), strong(30-40%改动)"
    )
    ai_function: Optional[str] = Field(
        default="rewrite",
        description="AI功能类型: complete/polish/expand/translate/summarize/rewrite"
    )


class HumanizeVerification(BaseModel):
    """去痕迹验证结果"""
    score_before: float = Field(..., ge=0, le=100, description="去痕迹前AI特征分数")
    score_after: float = Field(..., ge=0, le=100, description="去痕迹后AI特征分数")
    improvement: float = Field(..., description="改进幅度 (分数降低值)")
    success: bool = Field(..., description="是否成功降低AI痕迹")
    improvements: List[str] = Field(default_factory=list, description="改进项列表")
    remaining_issues: List[str] = Field(default_factory=list, description="遗留问题列表")


# ========== 会话记录相关 ==========

class HumanizeSessionBase(BaseModel):
    """去痕迹会话基础模型"""
    ai_function: str = Field(..., description="AI功能类型")
    score_before: float = Field(..., ge=0, le=100)
    score_after: float = Field(..., ge=0, le=100)
    improvement: float = Field(..., description="改进幅度")
    intensity: Literal["light", "medium", "strong"] = Field(default="medium")
    processing_time: float = Field(..., description="处理耗时(秒)")
    tokens_used: int = Field(..., description="消耗token数")
    cost: float = Field(..., description="成本(美元)")


class HumanizeSessionCreate(HumanizeSessionBase):
    """创建去痕迹会话"""
    user_id: UUID


class HumanizeSessionResponse(HumanizeSessionBase):
    """去痕迹会话响应"""
    id: Optional[UUID] = None  # 跳过时为None
    user_id: UUID
    user_accepted: Optional[bool] = None
    created_at: datetime

    # 详情数据 (可能为空,如果已过期)
    detail: Optional["HumanizeSessionDetailResponse"] = None

    # 跳过标记 (检测分低于阈值时为True)
    skipped: bool = Field(default=False, description="是否跳过改写（检测分低于阈值）")

    model_config = ConfigDict(from_attributes=True)
class HumanizeSessionDetailResponse(BaseModel):
    """去痕迹会话详情响应"""
    dimensions_before: Dict[str, Any] = Field(default_factory=dict)
    dimensions_after: Dict[str, Any] = Field(default_factory=dict)
    detected_patterns: List[str] = Field(default_factory=list)
    original_preview: Optional[str] = None
    humanized_preview: Optional[str] = None
    original_full: Optional[str] = None
    humanized_full: Optional[str] = None
    expires_at: datetime

    model_config = ConfigDict(from_attributes=True)
class HumanizeHistoryResponse(BaseModel):
    """去痕迹历史记录响应 (分页)"""
    total: int = Field(..., description="总记录数")
    items: List[HumanizeSessionResponse] = Field(..., description="会话列表")
    page: int = Field(..., description="当前页码")
    page_size: int = Field(..., description="每页数量")


class HumanizeStatsResponse(BaseModel):
    """去痕迹统计响应"""
    total_uses: int = Field(..., description="总使用次数")
    avg_improvement: float = Field(..., description="平均改进幅度")
    accept_rate: float = Field(..., description="接受率")
    total_tokens: int = Field(..., description="总token消耗")
    total_cost: float = Field(..., description="总成本")
    most_used_function: Optional[str] = Field(None, description="最常用功能")


# ========== 用户画像相关 ==========

class UserProfileBase(BaseModel):
    """用户画像基础模型"""
    humanize_enabled_global: bool = Field(default=True, description="全局开关")
    humanize_enabled_by_function: Dict[str, bool] = Field(
        default_factory=lambda: {
            "complete": True,
            "polish": True,
            "expand": True,
            "translate": False,
            "summarize": False,
            "rewrite": True
        },
        description="分功能开关"
    )
    preferred_intensity: Optional[Literal["light", "medium", "strong"]] = None


class UserProfileUpdateRequest(UserProfileBase):
    """更新用户画像请求"""
    pass


class UserProfileResponse(UserProfileBase):
    """用户画像响应"""
    id: UUID
    user_id: UUID

    # 统计数据
    total_uses: int = Field(default=0)
    avg_text_length: Optional[int] = None
    most_used_function: Optional[str] = None

    # 偏好设置
    preferred_speed_over_quality: bool = Field(default=False)
    is_novel_writer: bool = Field(default=False)

    # 反馈统计
    total_accepted: int = Field(default=0)
    total_rejected: int = Field(default=0)
    accept_rate: float = Field(default=0.0)

    # 显示模式
    display_mode: Literal["detailed", "simplified", "silent"] = Field(
        default="detailed",
        description="显示模式: detailed(详细对比), simplified(简化对比), silent(静默模式)"
    )

    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)
# ========== 用户反馈相关 ==========

class UserFeedbackRequest(BaseModel):
    """用户反馈请求"""
    session_id: UUID = Field(..., description="会话ID")
    accepted: bool = Field(..., description="是否接受结果")
