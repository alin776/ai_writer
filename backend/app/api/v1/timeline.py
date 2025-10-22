"""
时间线事件API
"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, and_
from typing import List
from uuid import UUID

from app.core.database import get_db
from app.core.security import get_current_user
from app.models.user import User
from app.models.work import Work
from app.models.timeline_event import TimelineEvent
from app.models.chapter import Chapter
from app.schemas.timeline_event import (
    TimelineEventCreate,
    TimelineEventUpdate,
    TimelineEventResponse,
    TimelineEventListResponse,
    ChapterAnchor
)

router = APIRouter()


async def verify_work_owner(work_id: UUID, user_id: UUID, db: AsyncSession):
    """验证作品所有权"""
    result = await db.execute(
        select(Work).where(and_(Work.id == work_id, Work.author_id == user_id))
    )
    work = result.scalar_one_or_none()
    if not work:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Work not found or you don't have permission"
        )
    return work


@router.post("/", response_model=TimelineEventResponse, status_code=status.HTTP_201_CREATED)
async def create_timeline_event(
    event: TimelineEventCreate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """创建时间线事件"""
    # 验证作品所有权
    await verify_work_owner(event.work_id, current_user.id, db)
    
    # 创建事件
    db_event = TimelineEvent(**event.dict())
    db.add(db_event)
    await db.commit()
    await db.refresh(db_event)
    
    return db_event


@router.get("/{event_id}", response_model=TimelineEventResponse)
async def get_timeline_event(
    event_id: UUID,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """获取单个时间线事件详情"""
    result = await db.execute(
        select(TimelineEvent).where(TimelineEvent.id == event_id)
    )
    event = result.scalar_one_or_none()
    
    if not event:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Timeline event not found"
        )
    
    # 验证作品所有权
    await verify_work_owner(event.work_id, current_user.id, db)
    
    return event


@router.get("/work/{work_id}", response_model=TimelineEventListResponse)
async def get_work_timeline_events(
    work_id: UUID,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """获取作品的所有时间线事件"""
    # 验证作品所有权
    await verify_work_owner(work_id, current_user.id, db)
    
    # 查询事件
    result = await db.execute(
        select(TimelineEvent)
        .where(TimelineEvent.work_id == work_id)
        .order_by(TimelineEvent.timestamp.asc())
    )
    events = result.scalars().all()
    
    return {
        "items": events,
        "total": len(events)
    }


@router.put("/{event_id}", response_model=TimelineEventResponse)
async def update_timeline_event(
    event_id: UUID,
    event_update: TimelineEventUpdate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """更新时间线事件"""
    # 查询事件
    result = await db.execute(
        select(TimelineEvent).where(TimelineEvent.id == event_id)
    )
    db_event = result.scalar_one_or_none()
    
    if not db_event:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Timeline event not found"
        )
    
    # 验证作品所有权
    await verify_work_owner(db_event.work_id, current_user.id, db)
    
    # 更新字段
    update_data = event_update.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_event, field, value)
    
    await db.commit()
    await db.refresh(db_event)
    
    return db_event


@router.delete("/{event_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_timeline_event(
    event_id: UUID,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """删除时间线事件"""
    # 查询事件
    result = await db.execute(
        select(TimelineEvent).where(TimelineEvent.id == event_id)
    )
    db_event = result.scalar_one_or_none()
    
    if not db_event:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Timeline event not found"
        )
    
    # 验证作品所有权
    await verify_work_owner(db_event.work_id, current_user.id, db)
    
    # 删除事件
    await db.delete(db_event)
    await db.commit()
    
    return None


@router.get("/work/{work_id}/chapter-anchors", response_model=List[ChapterAnchor])
async def get_chapter_anchors(
    work_id: UUID,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """获取作品的章节锚点列表"""
    # 验证作品所有权
    await verify_work_owner(work_id, current_user.id, db)
    
    # 查询所有章节
    result = await db.execute(
        select(Chapter)
        .where(Chapter.work_id == work_id)
        .order_by(Chapter.order.asc())
    )
    chapters = result.scalars().all()
    
    # 转换为章节锚点
    anchors = []
    for i, chapter in enumerate(chapters):
        anchors.append({
            "id": chapter.id,
            "chapter_id": chapter.id,
            "chapter_title": chapter.title,
            "chapter_number": chapter.order,
            "timestamp": i * 100  # 简单的时间戳计算，每章间隔100
        })
    
    return anchors
