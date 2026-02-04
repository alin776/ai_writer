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
    ImportResponse,
    ImportContext
)
from app.services.import_service import ImportService
from app.services.worldview_extraction_runner import run_worldview_extraction
from app.services.vectorize_runner import run_vectorize_chapter
from app.services.worldview_scan_progress_service import WorldviewScanProgressService
from app.core.config import settings
from app.core.celery_app import celery_app
from app.tasks.tasks import extract_worldview_task, vectorize_chapter_task

router = APIRouter()
logger = logging.getLogger(__name__)


def _celery_worker_available() -> bool:
    if not settings.ENABLE_CELERY_IMPORT_TASKS:
        return False
    try:
        insp = celery_app.control.inspect(timeout=1)
        resp = insp.ping()
        return bool(resp)
    except Exception as exc:
        logger.warning(f"[导入任务] Celery 不可用，回退 BackgroundTasks: {exc}")
        return False


async def _extract_worldview_from_chapters(
    work_id: str,
    user_id: str,
    scan_mode: str = "incremental",
    chapter_ids: Optional[list[str]] = None,
    preface_text: Optional[str] = None
):
    """后台任务：从导入的章节中提取世界观"""
    await run_worldview_extraction(
        work_id=work_id,
        user_id=user_id,
        scan_mode=scan_mode,
        chapter_ids=chapter_ids,
        preface_text=preface_text
    )


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

        celery_available = _celery_worker_available()

        queued_worldview = False
        queued_vectorize = False

        # 如果是文本导入且启用了自动提取世界观（先写入排队中进度）
        if auto_extract_worldview and format in ["markdown", "txt"]:
            try:
                progress_service = WorldviewScanProgressService(db)
                await progress_service.start_progress(
                    work_id=str(result.work_id),
                    scan_mode=worldview_scan_mode or "incremental",
                    chapters_total=len(import_context.get("chapter_ids", [])) if import_context else 0,
                    batches_total=0,
                    status="pending",
                    metadata={
                        "chapter_ids": import_context.get("chapter_ids", []) if import_context else [],
                        "preface_included": bool(import_context.get("preface_text")) if import_context else False
                    }
                )
            except Exception as exc:
                logger.warning(f"[世界观提取] 初始化进度失败: {exc}")

            if celery_available:
                extract_worldview_task.apply_async(
                    args=[
                        str(result.work_id),
                        str(current_user.id),
                        worldview_scan_mode or "incremental",
                        import_context.get("chapter_ids") if import_context else None,
                        import_context.get("preface_text") if import_context else None
                    ],
                    queue="worldview",
                    priority=9
                )
            elif background_tasks is not None:
                background_tasks.add_task(
                    _extract_worldview_from_chapters,
                    work_id=str(result.work_id),
                    user_id=str(current_user.id),
                    scan_mode=worldview_scan_mode or "incremental",
                    chapter_ids=import_context.get("chapter_ids") if import_context else None,
                    preface_text=import_context.get("preface_text") if import_context else None
                )
            queued_worldview = True
            logger.info(f"[世界观提取] 已为作品 {result.work_id} 排队世界观提取任务")

        if vectorize_jobs:
            if celery_available:
                for job in vectorize_jobs:
                    vectorize_chapter_task.apply_async(
                        args=[
                            job["work_id"],
                            job["chapter_id"],
                            job["chapter_order"],
                            job["chapter_title"],
                            job["content"]
                        ],
                        queue="vectorize",
                        priority=1
                    )
            elif background_tasks is not None:
                for job in vectorize_jobs:
                    background_tasks.add_task(_vectorize_import_chapter_content, **job)
            queued_vectorize = True

        # 在响应中提示排队状态
        if queued_worldview or queued_vectorize:
            message_parts = ["导入成功"]
            if queued_worldview:
                message_parts.append("世界观提取已排队")
            if queued_vectorize:
                message_parts.append("向量化已排队")
            result.message = "，".join(message_parts)

        # 回填导入上下文给前端（不包含前言全文）
        if import_context:
            result.import_context = ImportContext(
                chapter_ids=import_context.get("chapter_ids", []),
                chapter_order_start=import_context.get("chapter_order_start"),
                chapter_order_end=import_context.get("chapter_order_end"),
                scan_mode=worldview_scan_mode or "incremental"
            )
        
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
    await run_vectorize_chapter(
        work_id=work_id,
        chapter_id=chapter_id,
        chapter_order=chapter_order,
        chapter_title=chapter_title,
        content=content
    )
