"""
图书分析相关的Schema定义
"""

from datetime import datetime
from typing import Optional, List, Dict, Any
from uuid import UUID
from pydantic import BaseModel, Field

from app.models.book_analysis import JobStatus
from app.models.worldview_suggestion import SuggestionType, SuggestionAction, SuggestionStatus


# ========== 图书分析任务 ==========

class BookAnalysisJobCreate(BaseModel):
    """创建图书分析任务请求"""
    book_title: Optional[str] = Field(None, description="图书标题 (可选,默认使用文件名)")
    strategy_id: str = Field("web_novel_11d", description="分析策略ID")
    work_id: Optional[UUID] = Field(None, description="关联作品ID (可选)")


class BookAnalysisJobResponse(BaseModel):
    """图书分析任务响应"""
    id: UUID
    user_id: UUID
    book_title: str
    original_filename: str
    file_format: str
    file_size_bytes: int
    strategy_id: str
    status: JobStatus
    progress: int
    current_step: Optional[str]
    total_chapters: Optional[int]
    analyzed_chapters: int
    extracted_items_count: int
    suggestions_count: int
    error_message: Optional[str]
    created_at: datetime
    started_at: Optional[datetime]
    completed_at: Optional[datetime]

    class Config:
        from_attributes = True


class BookAnalysisJobListResponse(BaseModel):
    """图书分析任务列表响应"""
    jobs: List[BookAnalysisJobResponse]
    total: int


class BookAnalysisJobStatusResponse(BaseModel):
    """图书分析任务状态响应 (轻量级)"""
    id: UUID
    status: JobStatus
    progress: int
    current_step: Optional[str]
    error_message: Optional[str]


class CostEstimateResponse(BaseModel):
    """成本估算响应"""
    total_chapters: int
    analyzed_chapters: int
    deep_analysis_chapters: int
    estimated_input_tokens: int
    estimated_output_tokens: int
    estimated_total_tokens: int
    estimated_cost_usd: float


# ========== 智能建议 ==========

class WorldviewSuggestionResponse(BaseModel):
    """智能建议响应"""
    id: UUID
    job_id: UUID
    work_id: Optional[UUID]
    suggestion_type: SuggestionType
    action: SuggestionAction
    suggested_data: Dict[str, Any]
    confidence_score: float
    reason: str
    status: SuggestionStatus
    adopted_at: Optional[datetime]
    adopted_as_id: Optional[UUID]
    created_at: datetime

    class Config:
        from_attributes = True


class WorldviewSuggestionListResponse(BaseModel):
    """智能建议列表响应"""
    suggestions: List[WorldviewSuggestionResponse]
    total: int
    by_type: Dict[str, int]  # 按类型统计
    by_status: Dict[str, int]  # 按状态统计


class AdoptSuggestionRequest(BaseModel):
    """采纳建议请求"""
    suggestion_ids: List[UUID] = Field(..., description="要采纳的建议ID列表")
    work_id: Optional[UUID] = Field(None, description="目标作品ID (如果为空则使用建议中的work_id)")
    user_notes: Optional[str] = Field(None, description="用户备注")


class AdoptSuggestionResponse(BaseModel):
    """采纳建议响应"""
    success: bool
    adopted_count: int
    failed_count: int
    created_elements: List[Dict[str, Any]]  # 创建的元素列表
    errors: List[str]  # 错误信息列表


class UpdateSuggestionRequest(BaseModel):
    """更新建议请求"""
    suggested_data: Optional[Dict[str, Any]] = Field(None, description="修改后的建议数据")
    status: Optional[SuggestionStatus] = Field(None, description="状态")
    user_notes: Optional[str] = Field(None, description="用户备注")


# ========== 分析结果 ==========

class AnalysisResultResponse(BaseModel):
    """分析结果响应"""
    job_id: UUID
    dimensions: List[Dict[str, Any]]  # 11维度分析结果
    knowledge_items_count: int  # 创建的知识条目数
    suggestions_count: int  # 生成的智能建议数
