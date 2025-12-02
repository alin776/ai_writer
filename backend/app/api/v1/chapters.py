from fastapi import APIRouter, Depends, HTTPException, status, Body
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List, Optional
from pydantic import Field
import logging
import json

from app.core.database import get_db
from app.core.security import get_current_active_user
from app.core.redis_client import redis_client
from app.models.user import User
from app.schemas.chapter import ChapterCreate, ChapterUpdate, ChapterResponse, ChapterListResponse, ChapterSummaryResponse
from app.services.chapter_service import ChapterService
from app.services.work_service import WorkService
from app.services.ai.http_ai_service import HTTPAIService

logger = logging.getLogger(__name__)

router = APIRouter()


def _invalidate_chapter_cache(work_id: str):
    """失效指定作品的章节列表缓存"""
    if not redis_client.is_available():
        return

    cache_key = f"chapters:work:{work_id}"
    try:
        redis_client.client.delete(cache_key)
        logger.info(f"🗑️ [Chapters] 缓存已失效: {cache_key}")
    except Exception as e:
        logger.error(f"⚠️ [Chapters] 缓存失效失败: {cache_key}, error={e}")


@router.get("/work/{work_id}", response_model=ChapterListResponse)
async def get_chapters(
    work_id: str,
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db)
):
    """获取作品的章节列表 (带Redis缓存，TTL=60秒)"""
    logger.info(f"[GET chapters] work_id={work_id}, user_id={current_user.id}")

    # 🔧 2025-12-02: P0修复 - 先验证权限，再检查缓存（防止权限绕过漏洞）
    # 1. 先验证作品权限（安全第一）
    work_service = WorkService(db)
    work = await work_service.get_work_by_id(work_id)

    if not work:
        logger.error(f"[GET chapters] Work not found: {work_id}")
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Work not found"
        )

    if str(work.author_id) != str(current_user.id):
        logger.error(f"[GET chapters] Permission denied: work.author_id={work.author_id}, user_id={current_user.id}")
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to access this work"
        )

    # 2. 权限验证通过后，检查缓存
    cache_key = f"chapters:work:{work_id}"
    if redis_client.is_available():
        cached_data = redis_client.get_json(cache_key)
        if cached_data:
            logger.info(f"✅ [GET chapters] 缓存命中: {cache_key}")
            return ChapterListResponse(**cached_data)
        logger.info(f"⚠️ [GET chapters] 缓存未命中: {cache_key}")

    # 3. 缓存未命中，查询数据库
    chapter_service = ChapterService(db)
    chapters = await chapter_service.get_chapters_by_work(work_id)

    logger.info(f"[GET chapters] Returning {len(chapters)} chapters")

    # 4. 构造响应
    response = ChapterListResponse(
        total=len(chapters),
        items=chapters
    )

    # 5. 缓存结果 (TTL=60秒)
    if redis_client.is_available():
        # 兼容 Pydantic v1 和 v2
        response_data = response.model_dump() if hasattr(response, 'model_dump') else response.dict()
        cache_success = redis_client.set_json(cache_key, response_data, expire=60)
        if cache_success:
            logger.info(f"💾 [GET chapters] 缓存已保存: {cache_key} (expire=60s)")
        else:
            logger.warning(f"⚠️ [GET chapters] 缓存保存失败: {cache_key}")

    return response


@router.get("/{chapter_id}", response_model=ChapterResponse)
async def get_chapter(
    chapter_id: str,
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db)
):
    """获取章节详情"""
    chapter_service = ChapterService(db)
    chapter = await chapter_service.get_chapter_by_id(chapter_id)
    
    if not chapter:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Chapter not found"
        )
    
    # 验证权限
    work_service = WorkService(db)
    work = await work_service.get_work_by_id(str(chapter.work_id))
    
    if not work or str(work.author_id) != str(current_user.id):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to access this chapter"
        )
    
    return chapter


@router.post("", response_model=ChapterResponse, status_code=status.HTTP_201_CREATED)
async def create_chapter(
    chapter_data: ChapterCreate,
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db)
):
    """
    创建章节
    
    - **work_id**: 作品ID
    - **title**: 章节标题
    - **content**: 章节内容
    - **order**: 排序（可选）
    """
    # 验证作品权限
    work_service = WorkService(db)
    work = await work_service.get_work_by_id(chapter_data.work_id)
    
    if not work:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Work not found"
        )
    
    if str(work.author_id) != str(current_user.id):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to create chapter for this work"
        )
    
    # 创建章节
    chapter_service = ChapterService(db)
    chapter = await chapter_service.create_chapter(chapter_data)

    # 更新作品统计
    await work_service.update_work_stats(chapter_data.work_id)

    # 🔧 2025-12-02: P0修复 - 失效缓存
    _invalidate_chapter_cache(chapter_data.work_id)

    return chapter


@router.put("/{chapter_id}", response_model=ChapterResponse)
async def update_chapter(
    chapter_id: str,
    chapter_data: ChapterUpdate,
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db)
):
    """更新章节"""
    chapter_service = ChapterService(db)
    chapter = await chapter_service.get_chapter_by_id(chapter_id)
    
    if not chapter:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Chapter not found"
        )
    
    # 验证权限
    work_service = WorkService(db)
    work = await work_service.get_work_by_id(str(chapter.work_id))
    
    if not work or str(work.author_id) != str(current_user.id):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to update this chapter"
        )
    
    updated_chapter = await chapter_service.update_chapter(chapter_id, chapter_data)

    # 更新作品统计
    work_id = str(chapter.work_id)
    await work_service.update_work_stats(work_id)

    # 🔧 2025-12-02: P0修复 - 失效缓存
    _invalidate_chapter_cache(work_id)

    return updated_chapter


@router.delete("/{chapter_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_chapter(
    chapter_id: str,
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db)
):
    """删除章节"""
    chapter_service = ChapterService(db)
    chapter = await chapter_service.get_chapter_by_id(chapter_id)
    
    if not chapter:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Chapter not found"
        )
    
    # 验证权限
    work_service = WorkService(db)
    work = await work_service.get_work_by_id(str(chapter.work_id))
    
    if not work or str(work.author_id) != str(current_user.id):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to delete this chapter"
        )
    
    work_id = str(chapter.work_id)
    await chapter_service.delete_chapter(chapter_id)

    # 更新作品统计
    await work_service.update_work_stats(work_id)

    # 🔧 2025-12-02: P0修复 - 失效缓存
    _invalidate_chapter_cache(work_id)


@router.post("/reorder", status_code=status.HTTP_200_OK)
async def reorder_chapters(
    work_id: str = Body(...),
    chapter_ids: List[str] = Body(..., min_items=1, max_items=1000),
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db)
):
    """
    重新排序章节

    - **work_id**: 作品ID
    - **chapter_ids**: 章节ID列表（按新顺序），1-1000个章节
    """
    # 验证作品权限
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
            detail="Not authorized to reorder chapters for this work"
        )
    
    # 重新排序
    chapter_service = ChapterService(db)
    await chapter_service.reorder_chapters(work_id, chapter_ids)

    # 🔧 2025-12-02: Review修复 - 章节顺序改变后失效缓存
    _invalidate_chapter_cache(work_id)

    return {"message": "Chapters reordered successfully"}


@router.post("/{chapter_id}/summary", response_model=ChapterSummaryResponse)
async def generate_chapter_summary(
    chapter_id: str,
    regenerate: bool = False,
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db)
):
    """
    生成章节剧情概括
    
    - **chapter_id**: 章节ID
    - **regenerate**: 是否强制重新生成（默认false，如果已有概括则直接返回）
    
    如果章节已有概括且 regenerate=false，直接返回已有概括
    否则调用 AI 生成新的概括并保存到数据库
    """
    chapter_service = ChapterService(db)
    chapter = await chapter_service.get_chapter_by_id(chapter_id)
    
    if not chapter:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Chapter not found"
        )
    
    # 验证权限
    work_service = WorkService(db)
    work = await work_service.get_work_by_id(str(chapter.work_id))
    
    if not work or str(work.author_id) != str(current_user.id):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to access this chapter"
        )
    
    # 如果已有概括且不需要重新生成，直接返回
    if chapter.summary and not regenerate:
        logger.info(f"[章节概括] 返回已有概括: chapter_id={chapter_id}")
        return ChapterSummaryResponse(summary=chapter.summary)
    
    # 检查章节内容
    if not chapter.content or len(chapter.content.strip()) == 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Chapter content is empty"
        )
    
    try:
        logger.info(f"[章节概括] 开始生成: chapter_id={chapter_id}, content_length={len(chapter.content)}")

        # 调用 AI 生成概括
        # 2025-12-01: 传递db和user_id以启用成本追踪
        ai_service = HTTPAIService(db=db, user_id=str(current_user.id))
        summary_text = ""
        async for chunk, usage in ai_service.stream_summarize(chapter.content):
            # 只处理内容块,忽略最后的usage块
            if chunk:
                summary_text += chunk

        logger.info(f"[章节概括] 生成完成: chapter_id={chapter_id}, summary_length={len(summary_text)}")
        
        # 保存概括到数据库
        from app.schemas.chapter import ChapterUpdate
        update_data = ChapterUpdate(summary=summary_text)
        await chapter_service.update_chapter(chapter_id, update_data)

        logger.info(f"[章节概括] 已保存到数据库: chapter_id={chapter_id}")

        # 🔧 2025-12-02: Review修复 - 章节summary更新后失效缓存
        _invalidate_chapter_cache(str(chapter.work_id))

        return ChapterSummaryResponse(summary=summary_text)
        
    except Exception as e:
        logger.error(f"[章节概括] 生成失败: chapter_id={chapter_id}, error={str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to generate chapter summary: {str(e)}"
        )
