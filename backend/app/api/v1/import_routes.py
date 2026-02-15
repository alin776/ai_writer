"""导入API路由"""
from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File, Form
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
)
from app.services.import_service import ImportService

router = APIRouter()
logger = logging.getLogger(__name__)


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

        logger.info(f"用户 {current_user.id} 预览导入文件: {file.filename}, 格式: {format}")

        import_service = ImportService(db)
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
    include_guidelines: bool = Form(True),
    genre: Optional[str] = Form(None),
    work_id: Optional[str] = Form(None),
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """导入作品

    从文件中导入作品数据

    参数：
    - file: 上传的文件
    - format: 文件格式（json/markdown/txt）
    - create_new: 是否创建新作品
    - include_guidelines: 是否导入规范数据（仅JSON格式）
    - genre: 作品类型（新建时可指定）
    - work_id: 追加导入的目标作品ID（仅文本/markdown格式）
    """
    try:
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

        options = ImportOptions(
            format=format,
            create_new=create_new,
            work_id=work_id,
            include_guidelines=include_guidelines,
            genre=genre,
        )

        import_service = ImportService(db)
        result = await import_service.import_work(
            content=content,
            user_id=current_user.id,
            options=options
        )

        logger.info(f"导入成功: 作品ID={result.work_id}, 章节={result.chapters_created}")
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
