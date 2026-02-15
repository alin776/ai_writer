from pydantic import BaseModel, Field, field_serializer, ConfigDict
from typing import Optional, List
from datetime import datetime
from uuid import UUID
from app.models.knowledge_item import KnowledgeCategory, KnowledgeSource


class KnowledgeItemBase(BaseModel):
    """知识条目基础模型"""
    title: str = Field(..., min_length=1, max_length=200, description="标题")
    content: str = Field(..., min_length=1, description="内容")
    category: KnowledgeCategory = Field(..., description="分类")
    tags: List[str] = Field(default_factory=list, description="标签列表")


class KnowledgeItemCreate(KnowledgeItemBase):
    """创建知识条目"""
    summary: Optional[str] = Field(None, description="摘要(可选)")
    source_type: KnowledgeSource = Field(default=KnowledgeSource.MANUAL, description="来源类型")
    source_reference: Optional[str] = Field(None, max_length=500, description="来源说明(书名/网址等)")
    work_id: Optional[UUID] = Field(None, description="关联作品ID(可选)")
    chapter_id: Optional[UUID] = Field(None, description="关联章节ID(可选)")
    extra_data: dict = Field(default_factory=dict, description="扩展数据")


class KnowledgeItemUpdate(BaseModel):
    """更新知识条目"""
    title: Optional[str] = Field(None, min_length=1, max_length=200, description="标题")
    content: Optional[str] = Field(None, min_length=1, description="内容")
    summary: Optional[str] = Field(None, description="摘要")
    category: Optional[KnowledgeCategory] = Field(None, description="分类")
    tags: Optional[List[str]] = Field(None, description="标签列表")
    source_reference: Optional[str] = Field(None, max_length=500, description="来源说明")
    work_id: Optional[UUID] = Field(None, description="关联作品ID")
    chapter_id: Optional[UUID] = Field(None, description="关联章节ID")
    extra_data: Optional[dict] = Field(None, description="扩展数据")


class KnowledgeItemResponse(KnowledgeItemBase):
    """知识条目响应"""
    id: UUID
    user_id: UUID
    summary: Optional[str] = None
    source_type: KnowledgeSource
    source_id: Optional[UUID] = None
    source_reference: Optional[str] = None
    work_id: Optional[UUID] = None
    chapter_id: Optional[UUID] = None
    extra_data: dict
    view_count: int
    reference_count: int
    created_at: datetime
    updated_at: datetime
    last_accessed_at: Optional[datetime] = None

    model_config = ConfigDict(from_attributes=True)
    @field_serializer('id', 'user_id', 'source_id', 'work_id', 'chapter_id')
    def serialize_uuid(self, value: Optional[UUID], _info) -> Optional[str]:
        """将 UUID 序列化为字符串"""
        return str(value) if value else None


class KnowledgeItemListResponse(BaseModel):
    """知识条目列表响应"""
    total: int = Field(..., description="总数")
    page: int = Field(..., description="当前页码")
    page_size: int = Field(..., description="每页大小")
    items: List[KnowledgeItemResponse] = Field(..., description="知识条目列表")


class KnowledgeSearchRequest(BaseModel):
    """知识搜索请求"""
    query: str = Field(..., min_length=1, description="搜索查询")
    category: Optional[KnowledgeCategory] = Field(None, description="分类过滤(可选)")
    tags: Optional[List[str]] = Field(None, description="标签过滤(可选)")
    work_id: Optional[UUID] = Field(None, description="作品ID过滤(可选)")
    top_k: int = Field(default=10, ge=1, le=50, description="返回结果数量(1-50)")


class KnowledgeSearchResult(BaseModel):
    """单个搜索结果"""
    item: KnowledgeItemResponse = Field(..., description="知识条目")
    relevance_score: float = Field(..., ge=0.0, le=1.0, description="相关性评分(0-1)")
    highlight: str = Field(..., description="高亮片段")


class KnowledgeSearchResponse(BaseModel):
    """知识搜索响应"""
    query: str = Field(..., description="搜索查询")
    total: int = Field(..., description="结果总数")
    results: List[KnowledgeSearchResult] = Field(..., description="搜索结果列表")
