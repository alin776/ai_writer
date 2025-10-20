from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, or_, func
from typing import Optional

from app.core.database import get_db
from app.core.security import get_current_active_user
from app.models.user import User
from app.models.work import Work
from app.models.chapter import Chapter
from app.models.character import Character
from app.models.location import Location
from app.models.setting import Setting
from app.schemas.search import (
    SearchResponse,
    WorkSearchResult,
    ChapterSearchResult,
    CharacterSearchResult,
    LocationSearchResult,
    SettingSearchResult
)

router = APIRouter()


def highlight_snippet(text: str, query: str, max_length: int = 150) -> str:
    """
    提取包含关键词的文本片段，并高亮显示
    """
    if not text:
        return ""
    
    # 查找关键词位置
    query_lower = query.lower()
    text_lower = text.lower()
    pos = text_lower.find(query_lower)
    
    if pos == -1:
        # 未找到，返回开头
        return text[:max_length] + ("..." if len(text) > max_length else "")
    
    # 计算片段范围（关键词前后各取一半）
    half_length = max_length // 2
    start = max(0, pos - half_length)
    end = min(len(text), pos + len(query) + half_length)
    
    snippet = text[start:end]
    
    # 添加省略号
    if start > 0:
        snippet = "..." + snippet
    if end < len(text):
        snippet = snippet + "..."
    
    return snippet


@router.get("", response_model=SearchResponse)
async def global_search(
    q: str = Query(..., min_length=1, description="搜索关键词"),
    type: Optional[str] = Query(None, description="搜索类型: works/chapters/characters/locations/settings，不填则搜索全部"),
    work_id: Optional[str] = Query(None, description="限定在某个作品内搜索"),
    limit: int = Query(10, ge=1, le=50, description="每个类型返回的最大结果数"),
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db)
):
    """
    全局搜索
    
    支持搜索：
    - 作品（标题、简介）
    - 章节（标题、内容）
    - 角色（名称、描述）
    - 地点（名称、描述）
    - 设定（标题、内容）
    """
    search_pattern = f"%{q}%"
    results = SearchResponse(
        query=q,
        total=0,
        works=[],
        chapters=[],
        characters=[],
        locations=[],
        settings=[]
    )
    
    # 1. 搜索作品（当前用户的作品）
    if not type or type == "works":
        works_query = (
            select(Work)
            .where(Work.author_id == current_user.id)
            .where(
                or_(
                    Work.title.ilike(search_pattern),
                    Work.description.ilike(search_pattern)
                )
            )
            .limit(limit)
        )
        
        if work_id:
            from uuid import UUID
            works_query = works_query.where(Work.id == UUID(work_id))
        
        works_result = await db.execute(works_query)
        works = works_result.scalars().all()
        
        results.works = [
            WorkSearchResult(
                id=work.id,
                title=work.title,
                description=work.description,
                genre=work.genre,
                word_count=work.word_count,
                chapter_count=work.chapter_count,
                updated_at=work.updated_at
            )
            for work in works
        ]
        results.total += len(results.works)
    
    # 2. 搜索章节（标题和内容）
    if not type or type == "chapters":
        # 构建章节查询，JOIN作品表获取作品标题
        chapters_query = (
            select(Chapter, Work.title.label('work_title'))
            .join(Work, Chapter.work_id == Work.id)
            .where(Work.author_id == current_user.id)
            .where(
                or_(
                    Chapter.title.ilike(search_pattern),
                    Chapter.content.ilike(search_pattern)
                )
            )
            .limit(limit)
        )
        
        if work_id:
            from uuid import UUID
            chapters_query = chapters_query.where(Chapter.work_id == UUID(work_id))
        
        chapters_result = await db.execute(chapters_query)
        chapters_data = chapters_result.all()
        
        results.chapters = [
            ChapterSearchResult(
                id=chapter.id,
                work_id=chapter.work_id,
                work_title=work_title,
                title=chapter.title,
                content_snippet=highlight_snippet(chapter.content or "", q, 200),
                word_count=chapter.word_count,
                updated_at=chapter.updated_at
            )
            for chapter, work_title in chapters_data
        ]
        results.total += len(results.chapters)
    
    # 3. 搜索角色
    if not type or type == "characters":
        characters_query = (
            select(Character, Work.title.label('work_title'))
            .join(Work, Character.work_id == Work.id)
            .where(Work.author_id == current_user.id)
            .where(
                or_(
                    Character.name.ilike(search_pattern),
                    Character.description.ilike(search_pattern)
                )
            )
            .limit(limit)
        )
        
        if work_id:
            from uuid import UUID
            characters_query = characters_query.where(Character.work_id == UUID(work_id))
        
        characters_result = await db.execute(characters_query)
        characters_data = characters_result.all()
        
        results.characters = [
            CharacterSearchResult(
                id=char.id,
                work_id=char.work_id,
                work_title=work_title,
                name=char.name,
                role=char.role,
                description=char.description
            )
            for char, work_title in characters_data
        ]
        results.total += len(results.characters)
    
    # 4. 搜索地点
    if not type or type == "locations":
        locations_query = (
            select(Location, Work.title.label('work_title'))
            .join(Work, Location.work_id == Work.id)
            .where(Work.author_id == current_user.id)
            .where(
                or_(
                    Location.name.ilike(search_pattern),
                    Location.description.ilike(search_pattern)
                )
            )
            .limit(limit)
        )
        
        if work_id:
            from uuid import UUID
            locations_query = locations_query.where(Location.work_id == UUID(work_id))
        
        locations_result = await db.execute(locations_query)
        locations_data = locations_result.all()
        
        results.locations = [
            LocationSearchResult(
                id=loc.id,
                work_id=loc.work_id,
                work_title=work_title,
                name=loc.name,
                type=loc.type,
                description=loc.description
            )
            for loc, work_title in locations_data
        ]
        results.total += len(results.locations)
    
    # 5. 搜索设定
    if not type or type == "settings":
        settings_query = (
            select(Setting, Work.title.label('work_title'))
            .join(Work, Setting.work_id == Work.id)
            .where(Work.author_id == current_user.id)
            .where(
                or_(
                    Setting.title.ilike(search_pattern),
                    Setting.content.ilike(search_pattern)
                )
            )
            .limit(limit)
        )
        
        if work_id:
            from uuid import UUID
            settings_query = settings_query.where(Setting.work_id == UUID(work_id))
        
        settings_result = await db.execute(settings_query)
        settings_data = settings_result.all()
        
        results.settings = [
            SettingSearchResult(
                id=setting.id,
                work_id=setting.work_id,
                work_title=work_title,
                title=setting.title,
                category=setting.category,
                content=setting.content
            )
            for setting, work_title in settings_data
        ]
        results.total += len(results.settings)
    
    return results
