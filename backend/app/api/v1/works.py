from fastapi import APIRouter, Depends, HTTPException, status, Query, File, UploadFile
from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Optional
from datetime import datetime, timedelta, timezone
import logging
from pydantic import BaseModel

from app.core.database import get_db
from app.core.security import get_current_active_user
from app.core.config import settings
from app.models.user import User
from app.models.work import Work, WorkStatus
from app.schemas.work import WorkCreate, WorkUpdate, WorkResponse, WorkListResponse, WorkSummary
from app.services.work_service import WorkService
from app.services.cos_service import get_cos_service
from app.services.chapter_word_stat_service import ChapterWordStatService

router = APIRouter()
logger = logging.getLogger(__name__)

async def _calculate_weekly_new_words(db: AsyncSession, author_id: str) -> int:
    """计算本周新增字数：自然周（周一00:00 ~ 周日23:59，中国时区），只计正增量"""
    stat_service = ChapterWordStatService(db)
    return await stat_service.sum_positive_delta_for_author_this_week(author_id)


class CoverUploadResponse(BaseModel):
    """封面上传响应"""
    cover_url: str


@router.get("", response_model=WorkListResponse)
async def get_works(
    skip: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=100),
    search: Optional[str] = None,
    author_id: Optional[str] = None,
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db)
):
    """
    获取作品列表

    - **skip**: 跳过的记录数
    - **limit**: 每页数量
    - **search**: 搜索关键词
    - **author_id**: 作者ID（可选，不填则获取当前用户的作品）
    """
    work_service = WorkService(db)

    # 如果没有指定作者ID，默认获取当前用户的作品
    if author_id is None:
        author_id = str(current_user.id)

    works, total = await work_service.get_works(
        author_id=author_id,
        skip=skip,
        limit=limit,
        search=search
    )

    page = skip // limit + 1

    # 统计汇总数据（全量计算，不受分页影响）
    total_words = await db.scalar(
        select(func.coalesce(func.sum(Work.total_words), 0)).where(Work.author_id == author_id)
    ) or 0
    writing_count = await db.scalar(
        select(func.count(Work.id)).where(
            Work.author_id == author_id,
            Work.status == WorkStatus.WRITING
        )
    ) or 0
    weekly_new_words = await _calculate_weekly_new_words(db, author_id)

    return WorkListResponse(
        total=total,
        page=page,
        page_size=limit,
        items=works,
        summary=WorkSummary(
            total_words=total_words,
            writing_count=writing_count,
            weekly_new_words=weekly_new_words
        )
    )


@router.get("/{work_id}", response_model=WorkResponse)
async def get_work(
    work_id: str,
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db)
):
    """获取作品详情"""
    work_service = WorkService(db)
    work = await work_service.get_work_by_id(work_id)

    if not work:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Work not found"
        )

    # 只能查看自己的作品
    if str(work.author_id) != str(current_user.id):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to access this work"
        )

    return work


@router.post("", response_model=WorkResponse, status_code=status.HTTP_201_CREATED)
async def create_work(
    work_data: WorkCreate,
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db)
):
    """
    创建作品
    """
    work_service = WorkService(db)
    work = await work_service.create_work(str(current_user.id), work_data)
    return work


@router.put("/{work_id}", response_model=WorkResponse)
async def update_work(
    work_id: str,
    work_data: WorkUpdate,
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db)
):
    """更新作品"""
    work_service = WorkService(db)

    # 检查作品是否存在
    work = await work_service.get_work_by_id(work_id)
    if not work:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Work not found"
        )

    # 检查权限
    if str(work.author_id) != str(current_user.id):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to update this work"
        )

    updated_work = await work_service.update_work(work_id, work_data)
    return updated_work


@router.delete("/{work_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_work(
    work_id: str,
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db)
):
    """删除作品"""
    work_service = WorkService(db)

    # 检查作品是否存在
    work = await work_service.get_work_by_id(work_id)
    if not work:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Work not found"
        )

    # 检查权限
    if str(work.author_id) != str(current_user.id):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to delete this work"
        )

    # 删除作品
    await work_service.delete_work(work_id)

    # 失效相关缓存（缓存失效失败不影响删除）
    try:
        from app.api.v1.chapters import _invalidate_chapter_cache
        from app.api.v1.worldview import _invalidate_worldview_cache

        _invalidate_chapter_cache(work_id)
        _invalidate_worldview_cache(work_id, [
            "characters",
            "locations",
            "settings",
            "guidelines",
            "worlddata",
            "ai-guidelines",
        ])
        logger.info(f"[Works] 作品及相关缓存已删除: work_id={work_id}")
    except Exception as exc:  # pragma: no cover - 缓存失效失败不阻断流程
        logger.warning(f"[Works] 缓存失效失败（不影响删除）: work_id={work_id}, error={exc}")


@router.post("/{work_id}/cover", response_model=CoverUploadResponse)
async def upload_work_cover(
    work_id: str,
    file: UploadFile = File(...),
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db)
):
    """上传作品封面"""
    allowed_types = {"image/jpeg", "image/png", "image/webp"}
    if file.content_type not in allowed_types:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="仅支持 JPG/PNG/WebP 图片文件"
        )

    content = await file.read()
    max_size = settings.MAX_UPLOAD_SIZE or 10 * 1024 * 1024
    if len(content) > max_size:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="文件过大，请选择 10MB 以下的图片"
        )

    work_service = WorkService(db)
    work = await work_service.get_work_by_id(work_id)
    if not work:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Work not found"
        )

    if str(work.author_id) != str(current_user.id):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to upload cover for this work"
        )

    try:
        cos_service = get_cos_service()
    except RuntimeError as exc:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(exc)
        )

    cover_url = await cos_service.upload_avatar(
        user_id=str(current_user.id),
        filename=file.filename,
        content=content,
        content_type=file.content_type,
    )

    # 更新作品封面
    work_data = WorkUpdate(cover_image=cover_url)
    await work_service.update_work(work_id, work_data)

    return CoverUploadResponse(cover_url=cover_url)
