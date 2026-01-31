from pydantic import BaseModel
from typing import List, Optional
from uuid import UUID
from datetime import datetime


class WorkSearchResult(BaseModel):
    """作品搜索结果"""
    id: UUID
    title: str
    description: Optional[str] = None
    genre: Optional[str] = None
    word_count: int = 0
    chapter_count: int = 0
    updated_at: datetime
    
    class Config:
        from_attributes = True


class ChapterSearchResult(BaseModel):
    """章节搜索结果"""
    id: UUID
    work_id: UUID
    work_title: str
    title: str
    content_snippet: str  # 匹配的内容片段（带高亮）
    word_count: int = 0
    updated_at: datetime
    
    class Config:
        from_attributes = True


class CharacterSearchResult(BaseModel):
    """角色搜索结果"""
    id: UUID
    work_id: UUID
    work_title: str
    name: str
    role: Optional[str] = None
    description: Optional[str] = None
    
    class Config:
        from_attributes = True


class LocationSearchResult(BaseModel):
    """地点搜索结果"""
    id: UUID
    work_id: UUID
    work_title: str
    name: str
    type: Optional[str] = None
    description: Optional[str] = None
    
    class Config:
        from_attributes = True


class SettingSearchResult(BaseModel):
    """设定搜索结果"""
    id: UUID
    work_id: UUID
    work_title: str
    title: str
    category: Optional[str] = None
    content: Optional[str] = None
    
    class Config:
        from_attributes = True


class SearchResponse(BaseModel):
    """搜索响应"""
    query: str
    total: int
    works: List[WorkSearchResult] = []
    chapters: List[ChapterSearchResult] = []
    characters: List[CharacterSearchResult] = []
    locations: List[LocationSearchResult] = []
    settings: List[SettingSearchResult] = []
