"""
知识库API路由
"""
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Optional, List

from app.core.database import get_db
from app.core.security import get_current_active_user
from app.models.user import User
from app.models.knowledge_item import KnowledgeCategory
from app.schemas.knowledge import (
    KnowledgeItemCreate,
    KnowledgeItemUpdate,
    KnowledgeItemResponse,
    KnowledgeItemListResponse,
    KnowledgeSearchRequest,
    KnowledgeSearchResponse,
    KnowledgeSearchResult
)
from app.services.knowledge_service import KnowledgeService

router = APIRouter()


@router.post("", response_model=KnowledgeItemResponse, status_code=status.HTTP_201_CREATED)
async def create_knowledge_item(
    data: KnowledgeItemCreate,
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db)
):
    """
    创建知识条目

    - **title**: 标题
    - **content**: 内容
    - **category**: 分类
    - **tags**: 标签列表
    - **source_type**: 来源类型
    - **source_reference**: 来源说明
    - **work_id**: 关联作品ID（可选）
    - **chapter_id**: 关联章节ID（可选）
    """
    service = KnowledgeService(db)
    item = await service.create_item(
        user_id=str(current_user.id),
        data=data
    )
    return item


@router.get("", response_model=KnowledgeItemListResponse)
async def get_knowledge_items(
    skip: int = Query(0, ge=0, description="跳过数量"),
    limit: int = Query(20, ge=1, le=100, description="每页大小"),
    category: Optional[KnowledgeCategory] = Query(None, description="分类过滤"),
    tags: Optional[str] = Query(None, description="标签过滤(逗号分隔)"),
    work_id: Optional[str] = Query(None, description="作品ID过滤"),
    search: Optional[str] = Query(None, description="搜索关键词"),
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db)
):
    """
    获取知识条目列表

    支持分类、标签、作品、关键词过滤和分页
    """
    service = KnowledgeService(db)

    # 解析标签
    tag_list = None
    if tags:
        tag_list = [t.strip() for t in tags.split(",") if t.strip()]

    items, total = await service.get_items(
        user_id=str(current_user.id),
        skip=skip,
        limit=limit,
        category=category,
        tags=tag_list,
        work_id=work_id,
        search=search
    )

    page = skip // limit + 1

    return KnowledgeItemListResponse(
        total=total,
        page=page,
        page_size=limit,
        items=items
    )


@router.get("/{item_id}", response_model=KnowledgeItemResponse)
async def get_knowledge_item(
    item_id: str,
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db)
):
    """获取知识条目详情"""
    service = KnowledgeService(db)
    item = await service.get_item(
        item_id=item_id,
        user_id=str(current_user.id)
    )

    if not item:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Knowledge item not found or access denied"
        )

    return item


@router.put("/{item_id}", response_model=KnowledgeItemResponse)
async def update_knowledge_item(
    item_id: str,
    data: KnowledgeItemUpdate,
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db)
):
    """更新知识条目"""
    service = KnowledgeService(db)
    item = await service.update_item(
        item_id=item_id,
        user_id=str(current_user.id),
        data=data
    )

    if not item:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Knowledge item not found or access denied"
        )

    return item


@router.delete("/{item_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_knowledge_item(
    item_id: str,
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db)
):
    """删除知识条目"""
    service = KnowledgeService(db)
    success = await service.delete_item(
        item_id=item_id,
        user_id=str(current_user.id)
    )

    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Knowledge item not found or access denied"
        )


@router.post("/search", response_model=KnowledgeSearchResponse)
async def search_knowledge(
    request: KnowledgeSearchRequest,
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db)
):
    """
    语义搜索知识库

    使用RAG向量检索技术，根据语义相似度搜索相关知识条目
    """
    service = KnowledgeService(db)

    results = await service.search_by_semantic(
        user_id=str(current_user.id),
        query=request.query,
        category=request.category,
        tags=request.tags,
        work_id=str(request.work_id) if request.work_id else None,
        top_k=request.top_k
    )

    # 转换为响应格式
    search_results = [
        KnowledgeSearchResult(
            item=result['item'],
            relevance_score=result['relevance_score'],
            highlight=result['highlight']
        )
        for result in results
    ]

    return KnowledgeSearchResponse(
        query=request.query,
        total=len(search_results),
        results=search_results
    )


@router.post("/{item_id}/reference", status_code=status.HTTP_200_OK)
async def increment_reference_count(
    item_id: str,
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db)
):
    """
    增加引用次数

    当用户在编辑器中引用该知识条目时调用
    """
    service = KnowledgeService(db)
    success = await service.increment_reference_count(
        item_id=item_id,
        user_id=str(current_user.id)
    )

    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Knowledge item not found or access denied"
        )

    return {"message": "Reference count incremented"}
