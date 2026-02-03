"""导入API路由"""
from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File, Form, BackgroundTasks
from sqlalchemy.ext.asyncio import AsyncSession
import logging
from typing import Optional

from app.core.database import get_db
from app.core.security import get_current_user
from app.models.user import User
from app.schemas.export import (
    ImportOptions,
    ImportPreviewResponse,
    ImportResponse
)
from app.services.import_service import ImportService

router = APIRouter()
logger = logging.getLogger(__name__)


async def _extract_worldview_from_chapters(
    work_id: str,
    user_id: str,
    scan_mode: str = "incremental",
    chapter_ids: Optional[list[str]] = None,
    preface_text: Optional[str] = None
):
    """后台任务：从导入的章节中提取世界观"""
    try:
        from app.services.worldview_sync_service import WorldviewSyncService
        from app.services.worldview_scan_progress_service import WorldviewScanProgressService
        from app.core.database import async_session_maker

        logger.info(f"[世界观提取] 开始为作品 {work_id} 提取世界观")

        async with async_session_maker() as db_session:
            sync_service = WorldviewSyncService(db_session, user_id=user_id)
            progress_service = WorldviewScanProgressService(db_session)

            # 解析章节范围
            if scan_mode == "full":
                chapters = await sync_service.get_chapters_by_work(work_id)
            else:
                chapters = await sync_service.get_chapters_by_ids(work_id, chapter_ids or [])

            chapters_total = len(chapters)
            await progress_service.start_progress(
                work_id=work_id,
                scan_mode=scan_mode,
                chapters_total=chapters_total,
                metadata={
                    "chapter_ids": chapter_ids or [],
                    "preface_included": bool(preface_text)
                }
            )

            if not chapters:
                await progress_service.mark_completed(work_id)
                logger.info(f"[世界观提取] 未找到可解析的章节")
                return

            # 扫描章节（分批）
            changes, scan_meta = await sync_service.scan_chapters_for_changes_by_ids(
                work_id=work_id,
                chapter_ids=[str(ch.id) for ch in chapters],
                preface_text=preface_text,
                progress_callback=progress_service.update_progress
            )

            scanned = changes.get("scanned_chapters", 0)
            new_chars = len(changes.get("new_characters", []))
            updated_chars = len(changes.get("updated_characters", []))
            new_locs = len(changes.get("new_locations", []))
            new_sets = len(changes.get("new_settings", []))
            rel_changes = len(changes.get("relationship_changes", []))

            logger.info(f"[世界观提取] 扫描完成: {scanned}章, 发现 {new_chars}人物, {new_locs}地点, {new_sets}设定")

            # 如果有发现，自动应用
            if new_chars > 0 or updated_chars > 0 or new_locs > 0 or new_sets > 0 or rel_changes > 0:
                stats = await sync_service.apply_changes(work_id, changes)
                await progress_service.update_results(work_id, stats)
                logger.info(f"[世界观提取] 应用完成: {stats}")
            else:
                logger.info(f"[世界观提取] 未发现新的世界观元素")
                await progress_service.update_results(work_id, {})

            await progress_service.mark_completed(work_id, extra={"scanned_chapters": scanned, **(scan_meta or {})})

    except Exception as e:
        logger.error(f"[世界观提取] 提取失败: work_id={work_id}, error={e}", exc_info=True)
        try:
            from app.services.worldview_scan_progress_service import WorldviewScanProgressService
            from app.core.database import async_session_maker
            async with async_session_maker() as db_session:
                await WorldviewScanProgressService(db_session).mark_failed(work_id, str(e))
        except Exception:
            logger.error(f"[世界观提取] 记录失败状态失败: work_id={work_id}", exc_info=True)


@router.post("/works/import/preview", response_model=ImportPreviewResponse)
async def preview_import(
    file: UploadFile = File(...),
    format: str = Form(...),
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """预览导入数据
    
    上传文件并返回将要导入的数据概览
    
    支持格式：
    - json: 完整导入（作品+章节+世界观+规范）
    - markdown: 文本导入（自动分割章节）
    - txt: 文本导入（自动分割章节）
    """
    try:
        # 读取文件内容
        content = await file.read()
        
        if len(content) == 0:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="文件为空"
            )
        
        max_size = 50 * 1024 * 1024
        if format in ["markdown", "txt"]:
            max_size = 10 * 1024 * 1024  # 降低文本导入上限，避免超大文本占用

        if len(content) > max_size:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"文件过大（{format} 最大 {max_size // (1024 * 1024)}MB）"
            )
        
        logger.info(f"用户 {current_user.id} 预览导入文件: {file.filename}, 格式: {format}")
        
        # 创建导入服务
        import_service = ImportService(db)
        
        # 预览数据
        preview = await import_service.preview_import(content, format)
        
        logger.info(f"预览成功: 作品={preview.work.title}, 章节数={len(preview.chapters)}")
        
        return preview
        
    except ValueError as e:
        logger.warning(f"预览导入失败: {e}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except Exception as e:
        logger.error(f"预览导入时发生错误: {e}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="预览失败，请检查文件格式"
        )


@router.post("/works/import", response_model=ImportResponse)
async def import_work(
    file: UploadFile = File(...),
    format: str = Form(...),
    create_new: bool = Form(True),
    include_worldview: bool = Form(True),
    include_guidelines: bool = Form(True),
    auto_extract_worldview: bool = Form(False),
    worldview_scan_mode: str = Form("incremental"),
    work_id: Optional[str] = Form(None),
    background_tasks: BackgroundTasks = None,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """导入作品

    从文件中导入作品数据

    参数：
    - file: 上传的文件
    - format: 文件格式（json/markdown/txt）
    - create_new: 是否创建新作品（目前只支持创建新作品）
    - include_worldview: 是否导入世界观数据（仅JSON格式）
    - include_guidelines: 是否导入规范数据（仅JSON格式）
    - auto_extract_worldview: 是否自动从内容提取世界观（仅markdown/txt格式）
    - work_id: 追加导入的目标作品ID（仅文本/markdown格式）
    """
    try:
        # 读取文件内容
        content = await file.read()
        
        if len(content) == 0:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="文件为空"
            )
        
        max_size = 50 * 1024 * 1024
        if format in ["markdown", "txt"]:
            max_size = 10 * 1024 * 1024
        if len(content) > max_size:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"文件过大（{format} 最大 {max_size // (1024 * 1024)}MB）"
            )
        
        logger.info(f"用户 {current_user.id} 导入文件: {file.filename}, 格式: {format}")
        if worldview_scan_mode not in ["incremental", "full"]:
            worldview_scan_mode = "incremental"
        logger.info(f"[导入参数] auto_extract_worldview={auto_extract_worldview}, scan_mode={worldview_scan_mode}, format={format}, background_tasks={background_tasks is not None}")
        
        # 构建导入选项
        options = ImportOptions(
            format=format,
            create_new=create_new,
            work_id=work_id,
            include_worldview=include_worldview,
            include_guidelines=include_guidelines,
            worldview_scan_mode=worldview_scan_mode
        )
        
        # 创建导入服务
        import_service = ImportService(db)
        
        # 执行导入
        result, vectorize_jobs, import_context = await import_service.import_work(
            content=content,
            user_id=current_user.id,
            options=options
        )

        if vectorize_jobs and background_tasks is not None:
            for job in vectorize_jobs:
                background_tasks.add_task(_vectorize_import_chapter_content, **job)
            # 在响应中提示已排队
            result.message = "导入成功，向量化已排队"

        # 如果是文本导入且启用了自动提取世界观
        if auto_extract_worldview and format in ["markdown", "txt"] and background_tasks is not None:
            background_tasks.add_task(
                _extract_worldview_from_chapters,
                work_id=str(result.work_id),
                user_id=str(current_user.id),
                scan_mode=worldview_scan_mode or "incremental",
                chapter_ids=import_context.get("chapter_ids") if import_context else None,
                preface_text=import_context.get("preface_text") if import_context else None
            )
            result.message = (result.message or "导入成功") + "，世界观提取已排队"
            logger.info(f"[世界观提取] 已为作品 {result.work_id} 排队世界观提取任务")

        # 回填导入上下文给前端（不包含前言全文）
        if import_context:
            result.import_context = {
                "chapter_ids": import_context.get("chapter_ids", []),
                "chapter_order_start": import_context.get("chapter_order_start"),
                "chapter_order_end": import_context.get("chapter_order_end"),
                "scan_mode": worldview_scan_mode or "incremental"
            }
        
        logger.info(
            f"导入成功: 作品ID={result.work_id}, "
            f"章节={result.chapters_created}, "
            f"人物={result.characters_created}"
        )
        
        return result
        
    except ValueError as e:
        logger.warning(f"导入失败: {e}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except Exception as e:
        logger.error(f"导入作品时发生错误: {e}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="导入失败，请稍后重试"
        )


async def _vectorize_import_chapter_content(
    work_id: str,
    chapter_id: str,
    chapter_order: int,
    chapter_title: str,
    content: str
):
    """后台任务：异步向量化导入章节"""
    try:
        from app.services.chapter_vector_service import ChapterVectorService
        from app.core.database import async_session_maker

        async with async_session_maker() as db_session:
            service = ChapterVectorService(db_session)
            await service.store_chapter_vector(
                work_id=work_id,
                chapter_id=chapter_id,
                chapter_order=chapter_order,
                chapter_title=chapter_title,
                content=content
            )
    except Exception as e:
        logger.error(f"导入章节向量化失败（后台任务）: work_id={work_id}, chapter_id={chapter_id}, error={e}", exc_info=True)
