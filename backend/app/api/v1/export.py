"""导出API路由"""
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import FileResponse, Response
from sqlalchemy.ext.asyncio import AsyncSession
from uuid import UUID
import logging

from app.core.database import get_db
from app.core.security import get_current_user
from app.models.user import User
from app.schemas.export import ExportOptions, ExportResponse
from app.services.export_service import ExportService
from app.utils.file_storage import temp_storage

router = APIRouter()
logger = logging.getLogger(__name__)


@router.post("/works/{work_id}/export", response_model=ExportResponse)
async def export_work(
    work_id: UUID,
    options: ExportOptions,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """导出作品
    
    支持格式：
    - json: 完整数据备份（包含所有关系和元数据）
    - markdown: 可读格式（正文+世界观附录）
    - docx: 出版格式（TODO）
    
    返回临时下载链接，链接24小时后失效
    """
    try:
        logger.info(f"用户 {current_user.id} 请求导出作品 {work_id}, 格式: {options.format}")
        
        # 创建导出服务
        export_service = ExportService(db)
        
        # 导出作品
        content, filename = await export_service.export_work(
            work_id=work_id,
            user_id=current_user.id,
            options=options
        )
        
        # 保存到临时存储
        file_id, file_path, file_size = temp_storage.save_file(content, filename)
        
        # 生成下载URL
        download_url = f"/api/v1/downloads/{file_id}"
        expires_at = temp_storage.get_expiry_time(hours=24)
        
        logger.info(f"导出成功: {filename} ({file_size} bytes), 下载链接: {download_url}")
        
        return ExportResponse(
            download_url=download_url,
            file_name=filename,
            file_size=file_size,
            expires_at=expires_at
        )
        
    except ValueError as e:
        logger.warning(f"导出失败: {e}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except Exception as e:
        logger.error(f"导出作品时发生错误: {e}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="导出失败，请稍后重试"
        )


@router.get("/downloads/{file_id}")
async def download_file(file_id: str):
    """下载导出的文件
    
    临时下载链接，文件24小时后自动清理
    """
    try:
        # 获取文件路径
        file_path = temp_storage.get_file_path(file_id)
        if not file_path or not file_path.exists():
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="文件不存在或已过期"
            )
        
        # 获取原始文件名
        filename = temp_storage.get_original_filename(file_id) or "export.json"
        
        logger.info(f"下载文件: {file_id} -> {filename}")
        
        # 返回文件
        return FileResponse(
            path=str(file_path),
            filename=filename,
            media_type='application/octet-stream'
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"下载文件时发生错误: {e}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="下载失败"
        )


@router.delete("/downloads/{file_id}")
async def delete_export_file(
    file_id: str,
    current_user: User = Depends(get_current_user)
):
    """删除导出的临时文件"""
    try:
        success = temp_storage.delete_file(file_id)
        
        if success:
            return {"message": "文件已删除"}
        else:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="文件不存在"
            )
            
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"删除文件时发生错误: {e}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="删除失败"
        )
