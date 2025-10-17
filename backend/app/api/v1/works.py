from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Optional

from app.core.database import get_db
from app.core.security import get_current_active_user
from app.models.user import User
from app.schemas.work import WorkCreate, WorkUpdate, WorkResponse, WorkListResponse
from app.services.work_service import WorkService

router = APIRouter()


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
