"""
关系管理API
"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, and_
from typing import List
from uuid import UUID

from app.core.database import get_db
from app.core.security import get_current_user
from app.models.user import User
from app.models.relationship import EntityRelationship
from app.models.work import Work
from app.schemas.relationship import (
    RelationshipCreate,
    RelationshipUpdate,
    RelationshipResponse,
    RelationshipListResponse
)

router = APIRouter()


async def verify_work_owner(work_id: UUID, user_id: UUID, db: AsyncSession):
    """验证作品所有权"""
    result = await db.execute(
        select(Work).where(and_(Work.id == work_id, Work.author_id == user_id))
    )
    work = result.scalar_one_or_none()
    if not work:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Work not found or you don't have permission"
        )
    return work


@router.post("/", response_model=RelationshipResponse, status_code=status.HTTP_201_CREATED)
async def create_relationship(
    relationship: RelationshipCreate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """创建关系"""
    import logging
    logger = logging.getLogger(__name__)

    try:
        logger.info(f"Creating relationship: {relationship.dict()}")

        # 验证作品所有权
        await verify_work_owner(relationship.work_id, current_user.id, db)

        # 创建关系
        relationship_data = relationship.dict()
        logger.info(f"Relationship data for DB: {relationship_data}")

        db_relationship = EntityRelationship(**relationship_data)
        db.add(db_relationship)
        await db.commit()
        await db.refresh(db_relationship)

        logger.info(f"Relationship created successfully: {db_relationship.id}")
        return db_relationship
    except Exception as e:
        logger.error(f"Error creating relationship: {type(e).__name__}: {str(e)}")
        import traceback
        logger.error(f"Traceback: {traceback.format_exc()}")
        raise


@router.get("/{relationship_id}", response_model=RelationshipResponse)
async def get_relationship(
    relationship_id: UUID,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """获取单个关系详情"""
    result = await db.execute(
        select(EntityRelationship).where(EntityRelationship.id == relationship_id)
    )
    relationship = result.scalar_one_or_none()
    
    if not relationship:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Relationship not found"
        )
    
    # 验证作品所有权
    await verify_work_owner(relationship.work_id, current_user.id, db)
    
    return relationship


@router.get("/work/{work_id}", response_model=RelationshipListResponse)
async def get_work_relationships(
    work_id: UUID,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """获取作品的所有关系"""
    # 验证作品所有权
    await verify_work_owner(work_id, current_user.id, db)
    
    # 查询关系
    result = await db.execute(
        select(EntityRelationship)
        .where(EntityRelationship.work_id == work_id)
        .order_by(EntityRelationship.created_at.desc())
    )
    relationships = result.scalars().all()
    
    return {
        "items": relationships,
        "total": len(relationships)
    }


@router.put("/{relationship_id}", response_model=RelationshipResponse)
async def update_relationship(
    relationship_id: UUID,
    relationship_update: RelationshipUpdate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """更新关系"""
    # 查询关系
    result = await db.execute(
        select(EntityRelationship).where(EntityRelationship.id == relationship_id)
    )
    db_relationship = result.scalar_one_or_none()
    
    if not db_relationship:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Relationship not found"
        )
    
    # 验证作品所有权
    await verify_work_owner(db_relationship.work_id, current_user.id, db)
    
    # 更新字段
    update_data = relationship_update.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_relationship, field, value)
    
    await db.commit()
    await db.refresh(db_relationship)
    
    return db_relationship


@router.delete("/{relationship_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_relationship(
    relationship_id: UUID,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """删除关系"""
    # 查询关系
    result = await db.execute(
        select(EntityRelationship).where(EntityRelationship.id == relationship_id)
    )
    db_relationship = result.scalar_one_or_none()
    
    if not db_relationship:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Relationship not found"
        )
    
    # 验证作品所有权
    await verify_work_owner(db_relationship.work_id, current_user.id, db)
    
    # 删除关系
    await db.delete(db_relationship)
    await db.commit()
    
    return None
