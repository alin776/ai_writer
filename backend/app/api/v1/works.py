from fastapi import APIRouter, Depends, HTTPException, status, Query, File, UploadFile
from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Optional, List
from datetime import datetime, timedelta, timezone
import logging
from pydantic import BaseModel

from app.core.database import get_db
from app.core.security import get_current_active_user
from app.core.config import settings
from app.models.user import User
from app.models.work import Work, WorkStatus
from app.models.channel import Channel
from app.models.channel_member import ChannelMember
from app.schemas.work import WorkCreate, WorkUpdate, WorkResponse, WorkListResponse, WorkSummary
from app.services.work_service import WorkService
from app.services.cos_service import get_cos_service
from app.services.chapter_word_stat_service import ChapterWordStatService
from app.schemas.worldview import WorldviewScanProgressResponse

router = APIRouter()
logger = logging.getLogger(__name__)

async def _calculate_weekly_new_words(db: AsyncSession, author_id: str) -> int:
    """计算本周新增字数：自然周（周一00:00 ~ 周日23:59，中国时区），只计正增量"""
    stat_service = ChapterWordStatService(db)
    return await stat_service.sum_positive_delta_for_author_this_week(author_id)


class CoverUploadResponse(BaseModel):
    """封面上传响应"""
    cover_url: str


class PublishWorkRequest(BaseModel):
    """发布作品请求"""
    chapter_ids: List[str]


class PublishWorkResponse(BaseModel):
    """发布作品响应"""
    message: str
    work_id: str
    is_published: bool


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


@router.get("/{work_id}/worldview/scan-progress", response_model=WorldviewScanProgressResponse)
async def get_worldview_scan_progress_for_work(
    work_id: str,
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db)
):
    """获取世界观扫描进度（导入解析）"""
    from app.services.worldview_scan_progress_service import WorldviewScanProgressService

    work_service = WorkService(db)
    work = await work_service.get_work_by_id(work_id)
    if not work:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Work not found")
    if str(work.author_id) != str(current_user.id):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized")

    progress_service = WorldviewScanProgressService(db)
    progress = await progress_service.get_progress(work_id)
    if not progress:
        return WorldviewScanProgressResponse(work_id=work_id, status="idle")

    data = progress.to_dict()
    return WorldviewScanProgressResponse(
        work_id=data.get("work_id", work_id),
        status=data.get("status", "idle"),
        scan_mode=data.get("scan_mode"),
        chapters_total=data.get("chapters_total", 0),
        chapters_processed=data.get("chapters_processed", 0),
        batches_total=data.get("batches_total", 0),
        batches_completed=data.get("batches_completed", 0),
        progress_percentage=data.get("progress_percentage", 0.0),
        results=data.get("results"),
        last_error=data.get("last_error"),
        updated_at=progress.updated_at
    )


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

    # V2：初始化作品工作目录（Agent + 文件系统 API 共用）
    from app.services.agent.deep_agent import DATA_ROOT
    work_dir = DATA_ROOT / str(current_user.id) / "works" / str(work.id)
    work_dir.mkdir(parents=True, exist_ok=True)

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

    # 在删除作品前，锁定对应的书友圈频道
    channel_result = await db.execute(
        select(Channel).where(Channel.work_id == work.id)
    )
    channel = channel_result.scalar_one_or_none()
    if channel:
        channel.status = 'locked'
        channel.locked_at = func.now()
        channel.work_id = None  # 作品已删除，清除关联
        await db.commit()
        logger.info(f"Locked and unlinked work channel {channel.id} for deleted work {work.id}")

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


@router.post("/{work_id}/publish", response_model=PublishWorkResponse)
async def publish_work(
    work_id: str,
    request: PublishWorkRequest,
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db)
):
    """
    发布作品到小说广场

    - **work_id**: 作品ID
    - **chapter_ids**: 要发布的章节ID列表
    """
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
            detail="Not authorized to publish this work"
        )

    # 验证章节ID
    if not request.chapter_ids:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="请至少选择一个章节"
        )

    # 发布作品
    updated_work = await work_service.publish_work(work_id, request.chapter_ids)
    if not updated_work:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="发布失败"
        )

    # 检查是否已有书友圈频道，没有则创建
    existing_channel = await db.execute(
        select(Channel).where(Channel.work_id == updated_work.id)
    )
    channel = existing_channel.scalar_one_or_none()

    if not channel:
        # 创建书友圈频道
        channel_name = f"《{updated_work.title}》书友圈"
        channel = Channel(
            name=channel_name,
            description=f"{updated_work.title} 的读者交流群",
            type='work',
            status='active',
            creator_id=current_user.id,
            work_id=updated_work.id,
            is_permanent=False,
            member_count=1,  # 作者
            cover_image=updated_work.cover_image,  # 使用作品封面作为频道头像
        )
        db.add(channel)
        await db.flush()  # 获取 channel.id

        # 作者成为频道 owner
        owner_member = ChannelMember(
            channel_id=channel.id,
            user_id=current_user.id,
            role='owner',
            custom_title='作者',
            title_color='#FF6B6B'
        )
        db.add(owner_member)
        await db.commit()
        logger.info(f"Created work channel: {channel_name} for work {updated_work.id}")
    elif channel.status == 'locked':
        # 重新发布时，解锁已锁定的频道
        channel.status = 'active'
        channel.locked_at = None
        await db.commit()
        logger.info(f"Unlocked work channel {channel.id} for republished work {updated_work.id}")

    return PublishWorkResponse(
        message=f"《{updated_work.title}》已发布到小说广场",
        work_id=str(updated_work.id),
        is_published=True
    )


@router.post("/{work_id}/unpublish", response_model=PublishWorkResponse)
async def unpublish_work(
    work_id: str,
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db)
):
    """
    取消发布作品

    - **work_id**: 作品ID
    """
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
            detail="Not authorized to unpublish this work"
        )

    # 取消发布作品
    updated_work = await work_service.unpublish_work(work_id)
    if not updated_work:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="取消发布失败"
        )

    # 锁定对应的书友圈频道
    channel_result = await db.execute(
        select(Channel).where(Channel.work_id == updated_work.id)
    )
    channel = channel_result.scalar_one_or_none()
    if channel:
        channel.status = 'locked'
        channel.locked_at = func.now()
        await db.commit()
        logger.info(f"Locked work channel {channel.id} for unpublished work {updated_work.id}")

    return PublishWorkResponse(
        message=f"《{updated_work.title}》已取消发布",
        work_id=str(updated_work.id),
        is_published=False
    )
