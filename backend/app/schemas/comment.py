from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime
from uuid import UUID


class CommentBase(BaseModel):
    """评论基础模型"""
    content: str = Field(..., min_length=1, max_length=1000)


class CommentCreate(CommentBase):
    """创建评论"""
    parent_id: Optional[str] = None
    reply_to_user_id: Optional[str] = None


class CommentUpdate(BaseModel):
    """更新评论"""
    content: str = Field(..., min_length=1, max_length=1000)


class UserInfo(BaseModel):
    """用户信息"""
    id: str
    username: str
    avatar: Optional[str] = None

    class Config:
        from_attributes = True


class CommentResponse(CommentBase):
    """评论响应"""
    id: str
    work_id: str
    user_id: str
    parent_id: Optional[str] = None
    reply_to_user_id: Optional[str] = None
    like_count: int
    is_deleted: bool
    created_at: datetime
    updated_at: datetime
    user: UserInfo
    reply_to_user: Optional[UserInfo] = None
    is_liked: bool = False  # 当前用户是否点赞
    is_disliked: bool = False  # 当前用户是否踩
    reply_count: int = 0  # 回复数量
    user_rating: Optional[int] = None  # 评论者对该作品的评分(1-5星)

    class Config:
        from_attributes = True


class CommentWithRepliesResponse(CommentResponse):
    """带回复的评论响应（支持无限层级嵌套）"""
    replies: List["CommentWithRepliesResponse"] = []


# 更新前向引用，支持递归嵌套
CommentWithRepliesResponse.model_rebuild()


class CommentListResponse(BaseModel):
    """评论列表响应"""
    total: int
    page: int
    page_size: int
    items: List[CommentWithRepliesResponse]
