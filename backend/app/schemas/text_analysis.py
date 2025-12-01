"""文本分析相关的数据模型"""
from pydantic import BaseModel, Field
from typing import List, Literal, Optional
from enum import Enum


class IssueSeverity(str, Enum):
    """问题严重程度"""
    LOW = "low"          # 轻微
    MEDIUM = "medium"    # 中等
    HIGH = "high"        # 严重
    CRITICAL = "critical"  # 极严重


class IssueType(str, Enum):
    """问题类型"""
    TOO_SIMPLE = "too_simple"                    # 描写过于简单
    LACK_EMOTION = "lack_emotion"                # 缺少情感渲染
    WEAK_DETAILS = "weak_details"                # 细节不足
    REPETITIVE = "repetitive"                    # 重复啰嗦
    UNCLEAR_LOGIC = "unclear_logic"              # 逻辑不清
    POOR_RHYTHM = "poor_rhythm"                  # 节奏感差
    WEAK_CHARACTER = "weak_character"            # 人物形象单薄
    INCONSISTENT_STYLE = "inconsistent_style"    # 风格不统一
    GRAMMAR_ERROR = "grammar_error"              # 语法错误
    OTHER = "other"                              # 其他


class RewriteMode(str, Enum):
    """改写模式"""
    OPTIMIZE = "optimize"      # 优化提升（默认）
    EXPAND = "expand"          # 扩写丰富
    COMPRESS = "compress"      # 精简压缩
    CUSTOM = "custom"          # 自定义要求


class TextIssue(BaseModel):
    """文本问题"""
    type: IssueType = Field(..., description="问题类型")
    severity: IssueSeverity = Field(..., description="严重程度")
    description: str = Field(..., description="问题描述")

    class Config:
        json_schema_extra = {
            "example": {
                "type": "too_simple",
                "severity": "high",
                "description": "描写过于简单，缺少画面感"
            }
        }


class TextAnalysisResult(BaseModel):
    """文本分析结果"""
    quality_score: int = Field(..., ge=0, le=100, description="质量评分（0-100）")
    issues: List[TextIssue] = Field(default_factory=list, description="检测到的问题列表")
    recommended_mode: RewriteMode = Field(..., description="推荐的改写模式")
    reason: str = Field(..., description="推荐理由")

    class Config:
        json_schema_extra = {
            "example": {
                "quality_score": 45,
                "issues": [
                    {
                        "type": "too_simple",
                        "severity": "high",
                        "description": "描写过于简单"
                    },
                    {
                        "type": "lack_emotion",
                        "severity": "medium",
                        "description": "缺少情感渲染"
                    }
                ],
                "recommended_mode": "expand",
                "reason": "建议增加细节和情感描写，使画面更生动"
            }
        }


class TextAnalysisRequest(BaseModel):
    """文本分析请求"""
    text: str = Field(..., min_length=1, max_length=5000, description="待分析的文本")
    context_before: Optional[str] = Field(None, max_length=3000, description="前文上下文")
    context_after: Optional[str] = Field(None, max_length=3000, description="后文上下文")

    class Config:
        json_schema_extra = {
            "example": {
                "text": "主角走进房间，看到了桌子上的剑。",
                "context_before": "经过三天的跋涉，主角终于来到了目的地...",
                "context_after": "他拿起剑，准备离开..."
            }
        }


class RewriteRequest(BaseModel):
    """改写请求"""
    text: str = Field(..., min_length=1, max_length=5000, description="待改写的文本")
    mode: RewriteMode = Field(RewriteMode.OPTIMIZE, description="改写模式")
    custom_requirement: Optional[str] = Field(None, max_length=500, description="自定义要求（仅当mode=custom时）")
    context_before: Optional[str] = Field(None, max_length=3000, description="前文上下文")
    context_after: Optional[str] = Field(None, max_length=3000, description="后文上下文")
    model_names: Optional[List[str]] = Field(None, description="指定使用的模型列表，不指定则使用默认模型")

    class Config:
        json_schema_extra = {
            "example": {
                "text": "主角走进房间，看到了桌子上的剑。",
                "mode": "expand",
                "context_before": "经过三天的跋涉...",
                "context_after": "他拿起剑...",
                "model_names": ["gemini-2.5-pro"]
            }
        }


class ModelResult(BaseModel):
    """单个模型的改写结果"""
    model_name: str = Field(..., description="模型名称")
    rewritten_text: str = Field(..., description="改写后的文本")
    word_count: int = Field(..., description="字数")
    elapsed_time: float = Field(..., description="耗时（秒）")
    error: Optional[str] = Field(None, description="错误信息（如果失败）")

    class Config:
        json_schema_extra = {
            "example": {
                "model_name": "gemini-2.5-pro",
                "rewritten_text": "主角推开那扇厚重的木门，昏暗的房间中唯有一柄长剑泛着幽冷的寒光...",
                "word_count": 156,
                "elapsed_time": 2.3,
                "error": None
            }
        }


class RewriteResponse(BaseModel):
    """改写响应"""
    original_text: str = Field(..., description="原文")
    mode: RewriteMode = Field(..., description="改写模式")
    results: List[ModelResult] = Field(..., description="各模型的改写结果")

    class Config:
        json_schema_extra = {
            "example": {
                "original_text": "主角走进房间，看到了桌子上的剑。",
                "mode": "expand",
                "results": [
                    {
                        "model_name": "gemini-2.5-pro",
                        "rewritten_text": "主角推开那扇厚重的木门...",
                        "word_count": 156,
                        "elapsed_time": 2.3,
                        "error": None
                    }
                ]
            }
        }
