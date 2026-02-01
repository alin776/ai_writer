"""导出/导入相关的Schema定义"""
from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any
from datetime import datetime
from uuid import UUID


# ============= 导出相关 =============

class ExportOptions(BaseModel):
    """导出选项"""
    format: str = Field(..., description="导出格式: json/markdown/docx")
    include_chapters: bool = Field(True, description="是否包含章节")
    include_worldview: bool = Field(True, description="是否包含世界观")
    include_guidelines: bool = Field(True, description="是否包含规范")
    include_analysis: bool = Field(False, description="是否包含分析报告")
    chapter_ids: Optional[List[UUID]] = Field(None, description="指定导出的章节ID列表")


class ExportResponse(BaseModel):
    """导出响应"""
    download_url: str = Field(..., description="下载链接")
    file_name: str = Field(..., description="文件名")
    file_size: int = Field(..., description="文件大小(字节)")
    expires_at: datetime = Field(..., description="链接过期时间")


# ============= 导入相关 =============

class ImportOptions(BaseModel):
    """导入选项"""
    format: str = Field(..., description="导入格式: json/markdown/txt")
    create_new: bool = Field(True, description="是否创建新作品")
    work_id: Optional[UUID] = Field(None, description="导入到现有作品的ID")
    include_worldview: bool = Field(True, description="是否导入世界观")
    include_guidelines: bool = Field(True, description="是否导入规范")


class ImportPreviewWork(BaseModel):
    """导入预览 - 作品信息"""
    title: str
    description: Optional[str] = None
    genre: Optional[str] = None
    total_words: int = 0
    total_chapters: int = 0


class ImportPreviewChapter(BaseModel):
    """导入预览 - 章节信息"""
    title: str
    word_count: int
    order: int


class ImportPreviewResponse(BaseModel):
    """导入预览响应"""
    work: ImportPreviewWork
    chapters: List[ImportPreviewChapter]
    characters_count: int = 0
    locations_count: int = 0
    settings_count: int = 0
    warnings: List[str] = Field(default_factory=list, description="警告信息")


class ImportResponse(BaseModel):
    """导入响应"""
    work_id: UUID
    chapters_created: int
    characters_created: int = 0
    locations_created: int = 0
    settings_created: int = 0
    message: str = "导入成功"


# ============= 导出数据结构 =============

class ExportWork(BaseModel):
    """导出的作品数据"""
    id: UUID
    title: str
    description: Optional[str] = None
    genre: str
    status: str
    total_words: int
    total_chapters: int
    created_at: datetime
    updated_at: datetime


class ExportChapter(BaseModel):
    """导出的章节数据"""
    id: UUID
    title: str
    content: str
    summary: Optional[str] = None
    order: int
    word_count: int
    is_published: bool
    created_at: datetime
    updated_at: datetime


class ExportCharacter(BaseModel):
    """导出的人物数据"""
    id: UUID
    name: str
    role: Optional[str] = None
    description: str
    tags: List[str] = Field(default_factory=list)
    relationships: List[Dict[str, Any]] = Field(default_factory=list)


class ExportLocation(BaseModel):
    """导出的地点数据"""
    id: UUID
    name: str
    type: Optional[str] = None
    description: str
    tags: List[str] = Field(default_factory=list)
    related_locations: List[str] = Field(default_factory=list)


class ExportSetting(BaseModel):
    """导出的设定数据"""
    id: UUID
    title: str
    category: Optional[str] = None
    content: Optional[str] = None
    tags: List[str] = Field(default_factory=list)


class ExportWorldview(BaseModel):
    """导出的世界观数据"""
    characters: List[ExportCharacter] = Field(default_factory=list)
    locations: List[ExportLocation] = Field(default_factory=list)
    settings: List[ExportSetting] = Field(default_factory=list)


class ExportGuidelines(BaseModel):
    """导出的规范数据"""
    work_guidelines: Optional[Dict[str, Any]] = None
    ai_guidelines: Optional[Dict[str, Any]] = None


class ExportData(BaseModel):
    """完整导出数据"""
    version: str = "1.0"
    exported_at: datetime
    work: ExportWork
    chapters: List[ExportChapter] = Field(default_factory=list)
    worldview: Optional[ExportWorldview] = None
    guidelines: Optional[ExportGuidelines] = None
    analysis: Optional[Dict[str, Any]] = None
