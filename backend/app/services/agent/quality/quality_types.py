"""
质量评估相关的数据类型定义

包括评估维度、评分模型、评估上下文等
"""

from enum import Enum
from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field


class QualityDimension(Enum):
    """质量评估维度"""
    CONTENT_QUALITY = "content_quality"         # 内容质量 (权重30%)
    LENGTH_CHECK = "length_check"               # 字数检查 (权重15%)
    COHERENCE = "coherence"                     # 连贯性 (权重25%)
    STYLE_CONSISTENCY = "style_consistency"     # 风格一致性 (权重20%)
    GRAMMAR = "grammar"                         # 语法正确性 (权重10%)


# 维度权重配置
DIMENSION_WEIGHTS = {
    QualityDimension.CONTENT_QUALITY: 0.30,
    QualityDimension.LENGTH_CHECK: 0.15,
    QualityDimension.COHERENCE: 0.25,
    QualityDimension.STYLE_CONSISTENCY: 0.20,
    QualityDimension.GRAMMAR: 0.10
}


class DimensionScore(BaseModel):
    """单个维度的评分"""
    dimension: QualityDimension
    score: float = Field(ge=0.0, le=10.0, description="评分 0-10")
    feedback: str = Field(description="具体反馈")
    weight: float = Field(ge=0.0, le=1.0, description="权重")

    class Config:
        use_enum_values = False  # 保持Enum对象,不自动转换为值


class QualityEvaluation(BaseModel):
    """完整的质量评估结果"""
    overall_score: float = Field(ge=0.0, le=10.0, description="加权总分")
    dimension_scores: List[DimensionScore] = Field(description="各维度评分")
    passes: bool = Field(description="是否通过 (>=8分)")
    feedback: str = Field(description="综合反馈")
    suggestions: List[str] = Field(default_factory=list, description="改进建议")
    metadata: Dict[str, Any] = Field(default_factory=dict, description="元数据")

    def get_score_by_dimension(self, dimension: QualityDimension) -> Optional[DimensionScore]:
        """获取指定维度的评分"""
        for ds in self.dimension_scores:
            if ds.dimension == dimension:
                return ds
        return None

    def get_weak_dimensions(self, threshold: float = 7.0) -> List[DimensionScore]:
        """获取得分低于阈值的维度"""
        return [ds for ds in self.dimension_scores if ds.score < threshold]


class EvaluationContext(BaseModel):
    """评估上下文"""
    user_id: str
    novel_id: str
    chapter_id: str
    previous_content: Optional[str] = None      # 前文内容
    outline: Optional[str] = None               # 大纲
    character_settings: Optional[Dict] = None   # 人物设定
    writing_style: Optional[str] = None         # 写作风格
    target_length: int = 2000                   # 目标字数
    genre: Optional[str] = None                 # 题材类型 (如: 都市、玄幻、仙侠)

    class Config:
        arbitrary_types_allowed = True
