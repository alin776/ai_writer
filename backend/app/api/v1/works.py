from fastapi import APIRouter, Depends, HTTPException, status, Query, File, UploadFile
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Optional
from pydantic import BaseModel

from app.core.database import get_db
from app.core.security import get_current_active_user
from app.core.config import settings
from app.models.user import User
from app.schemas.work import WorkCreate, WorkUpdate, WorkResponse, WorkListResponse
from app.services.work_service import WorkService
from app.services.cos_service import get_cos_service

router = APIRouter()


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
    
    return WorkListResponse(
        total=total,
        page=page,
        page_size=limit,
        items=works
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
    
    # 检查权限（只能查看自己的作品）
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
    
    - **title**: 作品标题
    - **description**: 作品简介
    - **genre**: 作品类型
    - **status**: 作品状态
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
    
    await work_service.delete_work(work_id)


@router.post("/{work_id}/cover", response_model=CoverUploadResponse)
async def upload_work_cover(
    work_id: str,
    file: UploadFile = File(...),
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db)
):
    """上传作品封面"""
    # 检查文件类型
    allowed_types = {"image/jpeg", "image/png", "image/webp"}
    if file.content_type not in allowed_types:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="仅支持 JPG/PNG/WebP 图片文件"
        )

    # 读取文件内容
    content = await file.read()
    max_size = settings.MAX_UPLOAD_SIZE or 10485760
    if len(content) > max_size:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="文件过大，请选择 10MB 以下的图片"
        )

    # 检查作品是否存在
    work_service = WorkService(db)
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
            detail="Not authorized to upload cover for this work"
        )

    # 上传到 COS
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
        content_type=file.content_type
    )

    # 更新作品封面
    from app.schemas.work import WorkUpdate
    work_data = WorkUpdate(cover_image=cover_url)
    await work_service.update_work(work_id, work_data)

    return CoverUploadResponse(cover_url=cover_url)
