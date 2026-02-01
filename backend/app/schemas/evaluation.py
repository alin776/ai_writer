"""
AI评价功能的Pydantic Schema
"""

from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field, ConfigDict
from datetime import datetime
from uuid import UUID


# ===== 维度评分模型 =====
class DimensionScores(BaseModel):
    """5维度评分模型"""
    literary_quality: float = Field(..., ge=0, le=100, description="文学性评分 (0-100)")
    coherence: float = Field(..., ge=0, le=100, description="连贯性评分 (0-100)")
    creativity: float = Field(..., ge=0, le=100, description="创意性评分 (0-100)")
    emotional_impact: float = Field(..., ge=0, le=100, description="情感感染力评分 (0-100)")
    pacing: float = Field(..., ge=0, le=100, description="节奏把控评分 (0-100)")

    model_config = ConfigDict(json_schema_extra={
        "example": {
            "literary_quality": 85.0,
            "coherence": 80.0,
            "creativity": 75.0,
            "emotional_impact": 88.0,
            "pacing": 82.0
        }
    })


# ===== 评价上下文信息 =====
class EvaluationContext(BaseModel):
    """评价上下文信息"""
    work_id: Optional[UUID] = Field(None, description="作品ID")
    chapter_id: Optional[UUID] = Field(None, description="章节ID")
    work_title: Optional[str] = Field(None, description="作品标题")
    chapter_title: Optional[str] = Field(None, description="章节标题")
    previous_text: Optional[str] = Field(None, max_length=1000, description="前文片段(最多1000字)")

    model_config = ConfigDict(json_schema_extra={
        "example": {
            "work_id": "550e8400-e29b-41d4-a716-446655440000",
            "chapter_id": "660e8400-e29b-41d4-a716-446655440000",
            "work_title": "我的小说",
            "chapter_title": "第一章",
            "previous_text": "这是前文片段..."
        }
    })


# ===== 评价请求 =====
class EvaluationRequest(BaseModel):
    """评价请求"""
    text: str = Field(..., min_length=10, max_length=10000, description="待评价的AI生成内容")
    operation_type: str = Field(..., description="操作类型 (continue/polish/expand/translate/summarize)")
    context: Optional[EvaluationContext] = Field(None, description="上下文信息")

    model_config = ConfigDict(json_schema_extra={
        "example": {
            "text": "这是AI生成的一段小说内容...",
            "operation_type": "continue",
            "context": {
                "work_title": "我的小说",
                "chapter_title": "第一章",
                "previous_text": "前文片段..."
            }
        }
    })


# ===== 评价响应 =====
class EvaluationResponse(BaseModel):
    """评价响应"""
    overall_score: float = Field(..., ge=0, le=100, description="总分 (0-100)")
    dimensions: DimensionScores = Field(..., description="5维度评分")
    highlights: List[str] = Field(default_factory=list, description="优点列表")
    issues: List[str] = Field(default_factory=list, description="问题列表")
    suggestions: List[str] = Field(default_factory=list, description="改进建议列表")

    # 元数据
    evaluation_id: Optional[UUID] = Field(None, description="评价记录ID")
    created_at: Optional[datetime] = Field(None, description="评价时间")

    model_config = ConfigDict(json_schema_extra={
        "example": {
            "overall_score": 82.0,
            "dimensions": {
                "literary_quality": 85.0,
                "coherence": 80.0,
                "creativity": 75.0,
                "emotional_impact": 88.0,
                "pacing": 82.0
            },
            "highlights": [
                "语言流畅,文字优美",
                "情感表达细腻,有感染力",
                "节奏把控得当,张弛有度"
            ],
            "issues": [
                "部分描写过于抽象,缺乏具体细节",
                "某些情节转折略显生硬"
            ],
            "suggestions": [
                "增加感官描写,让场景更生动",
                "在情节转折处增加铺垫"
            ],
            "evaluation_id": "770e8400-e29b-41d4-a716-446655440000",
            "created_at": "2025-10-26T14:12:00Z"
        }
    })


# ===== 评价记录(数据库) =====
class EvaluationRecordInDB(BaseModel):
    """数据库中的评价记录"""
    id: UUID
    user_id: UUID
    work_id: Optional[UUID]
    chapter_id: Optional[UUID]
    operation_type: str
    overall_score: float
    dimensions: Dict[str, float]
    evaluation_details: Dict[str, Any]
    ai_call_log_id: Optional[UUID]
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)
