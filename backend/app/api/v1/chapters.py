from fastapi import APIRouter, Depends, HTTPException, status, Body
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from pydantic import Field
import logging

from app.core.database import get_db
from app.core.security import get_current_active_user
from app.models.user import User
from app.schemas.chapter import ChapterCreate, ChapterUpdate, ChapterResponse, ChapterListResponse, ChapterSummaryResponse
from app.services.chapter_service import ChapterService
from app.services.work_service import WorkService
from app.services.ai.http_ai_service import HTTPAIService

logger = logging.getLogger(__name__)

router = APIRouter()


@router.get("/work/{work_id}", response_model=ChapterListResponse)
async def get_chapters(
    work_id: str,
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db)
):
    """获取作品的章节列表"""
    logger.info(f"[GET chapters] work_id={work_id}, user_id={current_user.id}")
    
    # 验证作品权限
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
    
    # 获取章节列表
    chapter_service = ChapterService(db)
    chapters = await chapter_service.get_chapters_by_work(work_id)
    
    logger.info(f"[GET chapters] Returning {len(chapters)} chapters")
    
    return ChapterListResponse(
        total=len(chapters),
        items=chapters
    )


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
    await work_service.update_work_stats(str(chapter.work_id))
    
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
        ai_service = HTTPAIService()
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
        
        return ChapterSummaryResponse(summary=summary_text)
        
    except Exception as e:
        logger.error(f"[章节概括] 生成失败: chapter_id={chapter_id}, error={str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to generate chapter summary: {str(e)}"
        )
