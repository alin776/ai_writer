"""
章节评论相关的 Pydantic schemas
"""
from pydantic import BaseModel, Field, ConfigDict
from typing import Optional, List, Dict
from datetime import datetime
from uuid import UUID


# ==================== 用户信息 ====================

class UserInfo(BaseModel):
    """用户简要信息"""
    id: UUID
    username: str
    avatar: Optional[str] = None

    model_config = ConfigDict(from_attributes=True)
# ==================== 章节评论 ====================

class ChapterCommentBase(BaseModel):
    """章节评论基础模型"""
    content: str = Field(..., min_length=1, max_length=1000, description="评论内容")


class ChapterCommentCreate(ChapterCommentBase):
    """创建章节评论"""
    location_type: str = Field(default="chapter", description="位置类型: chapter/paragraph/sentence")
    paragraph_index: Optional[int] = Field(default=None, description="段落索引")
    sentence_index: Optional[int] = Field(default=None, description="句子索引")
    quoted_text: Optional[str] = Field(default=None, max_length=500, description="引用原文")
    parent_id: Optional[UUID] = Field(default=None, description="父评论ID (回复时使用)")
    reply_to_user_id: Optional[UUID] = Field(default=None, description="回复目标用户ID")


class ChapterCommentUpdate(BaseModel):
    """更新章节评论"""
    content: str = Field(..., min_length=1, max_length=1000, description="评论内容")


class ChapterCommentResponse(ChapterCommentBase):
    """章节评论响应"""
    id: UUID
    work_id: UUID
    chapter_num: int
    user_id: UUID
    location_type: str
    paragraph_index: Optional[int] = None
    sentence_index: Optional[int] = None
    quoted_text: Optional[str] = None
    parent_id: Optional[UUID] = None
    reply_to_user_id: Optional[UUID] = None
    like_count: int = 0
    is_deleted: bool = False
    created_at: datetime
    updated_at: Optional[datetime] = None

    # 关联信息
    user: Optional[UserInfo] = None
    reply_to_user: Optional[UserInfo] = None
    is_liked: bool = False  # 当前用户是否点赞
    reply_count: int = 0    # 回复数量

    model_config = ConfigDict(from_attributes=True)
class ChapterCommentWithReplies(ChapterCommentResponse):
    """带回复列表的章节评论（两层结构：回复不再嵌套）"""
    replies: List[ChapterCommentResponse] = []


class ChapterCommentListResponse(BaseModel):
    """章节评论列表响应"""
    total: int
    page: int
    page_size: int
    items: List[ChapterCommentWithReplies]


# ==================== 评论位置统计 ====================

class CommentLocationStats(BaseModel):
    """评论位置统计"""
    chapter: int = Field(default=0, description="章节级评论数量")
    paragraphs: Dict[str, int] = Field(default_factory=dict, description="段落评论数量 {index: count}")
    sentences: Dict[str, int] = Field(default_factory=dict, description="句子评论数量 {paragraphIndex-sentenceIndex: count}")
    total: int = Field(default=0, description="总评论数量")


# ==================== 点赞 ====================

class ChapterCommentLikeResponse(BaseModel):
    """点赞响应"""
    success: bool
    like_count: int
    is_liked: bool


# ==================== 举报 ====================

class ChapterCommentReportCreate(BaseModel):
    """创建举报"""
    reason: str = Field(..., description="举报原因: spam/abuse/porn/illegal/false/other")
    description: Optional[str] = Field(default=None, max_length=500, description="详细描述")


class ChapterCommentReportResponse(BaseModel):
    """举报响应"""
    id: UUID
    comment_id: UUID
    user_id: UUID
    reason: str
    description: Optional[str] = None
    is_processed: bool = False
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)
