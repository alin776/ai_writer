"""导入API路由"""
from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File, Form
from sqlalchemy.ext.asyncio import AsyncSession
import logging

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
        
        if len(content) > 50 * 1024 * 1024:  # 50MB限制
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="文件过大（最大50MB）"
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
    """
    try:
        # 读取文件内容
        content = await file.read()
        
        if len(content) == 0:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="文件为空"
            )
        
        if len(content) > 50 * 1024 * 1024:  # 50MB限制
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="文件过大（最大50MB）"
            )
        
        logger.info(f"用户 {current_user.id} 导入文件: {file.filename}, 格式: {format}")
        
        # 构建导入选项
        options = ImportOptions(
            format=format,
            create_new=create_new,
            work_id=None,
            include_worldview=include_worldview,
            include_guidelines=include_guidelines
        )
        
        # 创建导入服务
        import_service = ImportService(db)
        
        # 执行导入
        result = await import_service.import_work(
            content=content,
            user_id=current_user.id,
            options=options
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
