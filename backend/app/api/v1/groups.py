"""
实体分组API路由
提供分组的CRUD操作和成员管理
"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, and_
from sqlalchemy.orm import selectinload
from typing import List
from uuid import UUID

from app.core.database import get_db
from app.schemas.entity_group import (
    EntityGroupCreate,
    EntityGroupUpdate,
    EntityGroupResponse,
    GroupMemberCreate,
    GroupMemberResponse,
    BatchAddMembersRequest,
    BatchRemoveMembersRequest,
)
from app.models.entity_group import EntityGroup, GroupMember

router = APIRouter()


@router.post("/", response_model=EntityGroupResponse, status_code=status.HTTP_201_CREATED)
async def create_group(
    group_data: EntityGroupCreate,
    db: AsyncSession = Depends(get_db)
):
    """
    创建实体分组
    
    参数:
    - name: 分组名称（必填）
    - description: 分组描述
    - group_type: 分组类型（manual/auto）
    - auto_rule: 自动分组规则（JSON）
    - color: 分组颜色（HEX格式）
    - icon: 分组图标
    - parent_group_id: 父分组ID
    - order_index: 排序索引
    """
    db_group = EntityGroup(**group_data.model_dump())
    db.add(db_group)
    await db.commit()
    await db.refresh(db_group, attribute_names=['members'])
    return db_group


@router.get("/{group_id}", response_model=EntityGroupResponse)
async def get_group(
    group_id: UUID,
    db: AsyncSession = Depends(get_db)
):
    """
    获取分组详情
    
    包含分组的所有成员信息
    """
    result = await db.execute(
        select(EntityGroup)
        .options(selectinload(EntityGroup.members))
        .where(EntityGroup.id == group_id)
    )
    db_group = result.scalar_one_or_none()
    if not db_group:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Group with id {group_id} not found"
        )
    return db_group


@router.put("/{group_id}", response_model=EntityGroupResponse)
async def update_group(
    group_id: UUID,
    group_data: EntityGroupUpdate,
    db: AsyncSession = Depends(get_db)
):
    """
    更新分组信息
    
    可更新的字段：
    - name: 分组名称
    - description: 分组描述
    - auto_rule: 自动分组规则
    - color: 分组颜色
    - icon: 分组图标
    - parent_group_id: 父分组ID
    - order_index: 排序索引
    """
    result = await db.execute(
        select(EntityGroup)
        .options(selectinload(EntityGroup.members))
        .where(EntityGroup.id == group_id)
    )
    db_group = result.scalar_one_or_none()
    if not db_group:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Group with id {group_id} not found"
        )
    
    # 更新非空字段
    update_data = group_data.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_group, field, value)
    
    await db.commit()
    await db.refresh(db_group, attribute_names=['members'])
    return db_group


@router.delete("/{group_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_group(
    group_id: UUID,
    db: AsyncSession = Depends(get_db)
):
    """
    删除分组
    
    会级联删除所有分组成员关联
    """
    result = await db.execute(
        select(EntityGroup)
        .options(selectinload(EntityGroup.members))
        .where(EntityGroup.id == group_id)
    )
    db_group = result.scalar_one_or_none()
    if not db_group:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Group with id {group_id} not found"
        )
    
    await db.delete(db_group)
    await db.commit()
    return None


@router.get("/work/{work_id}", response_model=List[EntityGroupResponse])
async def get_work_groups(
    work_id: UUID,
    db: AsyncSession = Depends(get_db)
):
    """
    获取作品的所有分组
    
    返回该作品下的所有分组列表，包含成员信息
    """
    result = await db.execute(
        select(EntityGroup)
        .options(selectinload(EntityGroup.members))
        .where(EntityGroup.work_id == work_id)
        .order_by(EntityGroup.order_index)
    )
    groups = result.scalars().all()
    return groups


# ============ 分组成员管理 ============

@router.post("/{group_id}/members", response_model=List[GroupMemberResponse], status_code=status.HTTP_201_CREATED)
async def add_group_members(
    group_id: UUID,
    request: BatchAddMembersRequest,
    db: AsyncSession = Depends(get_db)
):
    """
    添加分组成员（支持批量）
    
    参数:
    - members: 成员列表
      - entity_id: 实体ID
      - entity_type: 实体类型（character/location/setting）
      - order_index: 排序索引
    """
    # 验证分组是否存在
    result = await db.execute(select(EntityGroup).where(EntityGroup.id == group_id))
    db_group = result.scalar_one_or_none()
    if not db_group:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Group with id {group_id} not found"
        )
    
    # 批量创建成员
    created_members = []
    for member_data in request.members:
        # 检查是否已存在
        check_result = await db.execute(
            select(GroupMember).where(
                and_(
                    GroupMember.group_id == group_id,
                    GroupMember.entity_id == member_data.entity_id
                )
            )
        )
        existing = check_result.scalar_one_or_none()
        
        if not existing:
            db_member = GroupMember(
                group_id=group_id,
                **member_data.model_dump()
            )
            db.add(db_member)
            created_members.append(db_member)
    
    await db.commit()
    
    # 刷新所有新创建的成员
    for member in created_members:
        await db.refresh(member)
    
    return created_members


@router.delete("/{group_id}/members/{member_id}", status_code=status.HTTP_204_NO_CONTENT)
async def remove_group_member(
    group_id: UUID,
    member_id: UUID,
    db: AsyncSession = Depends(get_db)
):
    """
    移除分组成员
    
    从指定分组中移除一个成员
    """
    result = await db.execute(
        select(GroupMember).where(
            and_(
                GroupMember.id == member_id,
                GroupMember.group_id == group_id
            )
        )
    )
    db_member = result.scalar_one_or_none()
    
    if not db_member:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Member with id {member_id} not found in group {group_id}"
        )
    
    await db.delete(db_member)
    await db.commit()
    return None


@router.post("/{group_id}/members/batch-remove", status_code=status.HTTP_204_NO_CONTENT)
async def batch_remove_members(
    group_id: UUID,
    request: BatchRemoveMembersRequest,
    db: AsyncSession = Depends(get_db)
):
    """
    批量移除分组成员
    
    参数:
    - member_ids: 要移除的成员ID列表
    """
    result = await db.execute(
        select(GroupMember).where(
            and_(
                GroupMember.group_id == group_id,
                GroupMember.id.in_(request.member_ids)
            )
        )
    )
    members_to_delete = result.scalars().all()
    
    for member in members_to_delete:
        await db.delete(member)
    
    await db.commit()
    return None
