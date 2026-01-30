from fastapi import APIRouter, Depends, HTTPException, status, Body, BackgroundTasks, Query
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
from app.schemas.chapter_revision import ChapterRevisionResponse
from app.services.chapter_service import ChapterService
from app.services.chapter_revision_service import ChapterRevisionService
from app.services.work_service import WorkService
from app.services.task_service import TaskService
from app.services.ai.http_ai_service import HTTPAIService
from app.services.chapter_comment_service import cleanup_invalid_comments, delete_all_chapter_comments

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


@router.get("/{chapter_id}/revisions", response_model=List[ChapterRevisionResponse])
async def get_chapter_revisions(
    chapter_id: str,
    status_filter: str = Query("pending", alias="status"),
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db)
):
    """获取章节待处理修订"""
    chapter_service = ChapterService(db)
    chapter = await chapter_service.get_chapter_by_id(chapter_id)

    if not chapter:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Chapter not found"
        )

    work_service = WorkService(db)
    work = await work_service.get_work_by_id(str(chapter.work_id))

    if not work or str(work.author_id) != str(current_user.id):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to access this chapter"
        )

    if status_filter != "pending":
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Only pending revisions are supported"
        )

    revision_service = ChapterRevisionService(db)
    revisions = await revision_service.get_pending_revisions_by_chapter(chapter_id)
    return revisions


@router.post("", response_model=ChapterResponse, status_code=status.HTTP_201_CREATED)
async def create_chapter(
    chapter_data: ChapterCreate,
    background_tasks: BackgroundTasks,
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

    # 如果有内容，触发每日写作任务检查
    if chapter.content:
        word_count = len(chapter.content)
        if word_count > 0:
            await TaskService.check_daily_writing_task(db, current_user.id, word_count)

    # 🔧 2025-12-02: P0修复 - 失效缓存
    _invalidate_chapter_cache(chapter_data.work_id)

    return chapter


@router.put("/{chapter_id}", response_model=ChapterResponse)
async def update_chapter(
    chapter_id: str,
    chapter_data: ChapterUpdate,
    background_tasks: BackgroundTasks,
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

    # 保存旧内容用于评论清理
    old_content = chapter.content

    # 计算内容变化的字数
    old_word_count = len(chapter.content) if chapter.content else 0
    new_word_count = len(chapter_data.content) if chapter_data.content else 0
    word_count_diff = new_word_count - old_word_count

    updated_chapter = await chapter_service.update_chapter(chapter_id, chapter_data)

    # 🆕 2025-12-24: 清理因内容变化而失效的章节评论
    if chapter_data.content and chapter_data.content != old_content:
        try:
            from uuid import UUID as UUIDType
            deleted_comments = await cleanup_invalid_comments(
                db,
                UUIDType(chapter_id),
                chapter_data.content,
                old_content
            )
            if deleted_comments > 0:
                logger.info(f"[Chapters] 章节 {chapter_id} 更新后清理了 {deleted_comments} 条失效评论")
        except Exception as e:
            logger.error(f"[Chapters] 清理失效评论失败: {e}")

    # 更新作品统计
    work_id = str(chapter.work_id)
    await work_service.update_work_stats(work_id)

    # 如果增加了字数，触发每日写作任务检查
    if word_count_diff > 0:
        await TaskService.check_daily_writing_task(db, current_user.id, word_count_diff)

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

    # 🆕 2025-12-24: 删除章节的所有评论
    try:
        from uuid import UUID as UUIDType
        deleted_comments = await delete_all_chapter_comments(db, UUIDType(chapter_id))
        if deleted_comments > 0:
            logger.info(f"[Chapters] 章节 {chapter_id} 删除，清理了 {deleted_comments} 条评论")
    except Exception as e:
        logger.error(f"[Chapters] 清理章节评论失败: {e}")

    await chapter_service.delete_chapter(chapter_id)

    # 更新作品统计
    await work_service.update_work_stats(work_id)

    # 🔧 2025-12-02: P0修复 - 失效缓存
    _invalidate_chapter_cache(work_id)

    # 🆕 删除章节向量
    try:
        from app.services.chapter_vector_service import ChapterVectorService
        vector_service = ChapterVectorService(db)
        await vector_service.delete_chapter_vectors(chapter_id)
    except Exception as e:
        logger.warning(f"[Chapters] 删除章节向量失败（不阻断删除）: {e}")


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
        # ✅ 2025-12-14: 添加事务回滚，确保积分扣除被回滚
        await db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to generate chapter summary: {str(e)}"
        )


async def _vectorize_chapter_content(
    work_id: str,
    chapter_id: str,
    chapter_order: int,
    chapter_title: str,
    content: str
):
    """
    后台任务：章节内容向量化

    Args:
        work_id: 作品ID
        chapter_id: 章节ID
        chapter_order: 章节顺序
        chapter_title: 章节标题
        content: 章节内容
    """
    try:
        from app.services.chapter_vector_service import ChapterVectorService

        # 创建新的数据库会话（后台任务需要独立会话）
        from app.core.database import async_session_maker
        async with async_session_maker() as db:
            service = ChapterVectorService(db)
            await service.store_chapter_vector(
                work_id=work_id,
                chapter_id=chapter_id,
                chapter_order=chapter_order,
                chapter_title=chapter_title,
                content=content
            )

    except Exception as e:
        logger.error(f"章节向量化后台任务失败: {e}", exc_info=True)
        # 不影响用户的保存操作，只记录日志
