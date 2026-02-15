"""管理端邀请码系统API"""

from math import ceil
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from uuid import UUID

from app.core.database import get_db
from app.core.security import get_current_active_user
from app.models.user import User
from app.services.invitations.invitation_service import InvitationService
from app.schemas.admin_invitations import (
    AdminInvitationGenerateRequest,
    AdminInvitationResponse,
    AdminInvitationListResponse,
    AdminInvitationListItem,
    AdminInvitationStats,
    AdminInvitationDeleteResponse
)

router = APIRouter()


def check_admin_permission(current_user: User = Depends(get_current_active_user)) -> User:
    """检查是否为管理员"""
    if not current_user.is_admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="需要管理员权限"
        )
    return current_user


@router.post("/generate", response_model=AdminInvitationResponse)
async def generate_admin_invitation(
    request: AdminInvitationGenerateRequest,
    current_user: User = Depends(check_admin_permission),
    db: AsyncSession = Depends(get_db)
):
    """
    管理员生成邀请码

    - **custom_code**: 自定义邀请码（3-8位，可选）
    - **max_uses**: 最大使用次数（1-100）
    - **expires_days**: 有效期天数（1-365）
    - **remark**: 备注信息（可选）

    返回生成的邀请码信息
    """
    invitation_service = InvitationService(db)

    try:
        invitation = await invitation_service.generate_admin_invitation(
            admin_id=current_user.id,
            custom_code=request.custom_code,
            max_uses=request.max_uses,
            expires_days=request.expires_days,
            remark=request.remark
        )

        # 判断状态
        now = invitation.created_at
        if invitation.used_count >= invitation.max_uses:
            inv_status = "exhausted"
        elif invitation.expires_at and invitation.expires_at <= now:
            inv_status = "expired"
        else:
            inv_status = "active"

        return AdminInvitationResponse(
            id=str(invitation.id),
            code=invitation.code,
            max_uses=invitation.max_uses,
            used_count=invitation.used_count,
            activated_count=invitation.activated_count,
            total_rewards=float(invitation.total_rewards),
            expires_at=invitation.expires_at.isoformat() if invitation.expires_at else None,
            remark=invitation.remark,
            created_by=str(invitation.user_id),
            creator_username=current_user.username,
            created_at=invitation.created_at.isoformat(),
            status=inv_status
        )

    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


@router.get("/list", response_model=AdminInvitationListResponse)
async def list_admin_invitations(
    page: int = 1,
    page_size: int = 20,
    status: str = None,
    creator_id: str = None,
    search: str = None,
    current_user: User = Depends(check_admin_permission),
    db: AsyncSession = Depends(get_db)
):
    """
    管理员查询所有邀请码

    - **page**: 页码（默认1）
    - **page_size**: 每页数量（默认20，最大100）
    - **status**: 状态筛选（active/expired/exhausted/all，可选）
    - **creator_id**: 创建者ID筛选（可选）
    - **search**: 搜索关键词（邀请码或备注，可选）

    返回邀请码列表和统计信息
    """
    invitation_service = InvitationService(db)

    # 转换 creator_id
    creator_uuid = None
    if creator_id:
        try:
            creator_uuid = UUID(creator_id)
        except ValueError:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="无效的创建者ID"
            )

    # 限制每页数量
    if page_size > 100:
        page_size = 100

    items, total, stats_dict = await invitation_service.list_all_invitations(
        page=page,
        page_size=page_size,
        status=status,
        creator_id=creator_uuid,
        search=search
    )

    # 构建响应
    list_items = [AdminInvitationListItem(**item) for item in items]
    stats = AdminInvitationStats(**stats_dict)

    total_pages = ceil(total / page_size) if page_size > 0 else 0

    return AdminInvitationListResponse(
        total=total,
        page=page,
        page_size=page_size,
        total_pages=total_pages,
        items=list_items,
        stats=stats
    )


@router.delete("/{invitation_id}", response_model=AdminInvitationDeleteResponse)
async def delete_admin_invitation(
    invitation_id: str,
    current_user: User = Depends(check_admin_permission),
    db: AsyncSession = Depends(get_db)
):
    """
    删除邀请码

    仅允许删除未使用的邀请码

    - **invitation_id**: 邀请码ID

    返回删除结果
    """
    invitation_service = InvitationService(db)

    try:
        invitation_uuid = UUID(invitation_id)
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="无效的邀请码ID"
        )

    try:
        success = await invitation_service.delete_invitation(invitation_uuid)
        return AdminInvitationDeleteResponse(
            success=success,
            message="邀请码已删除"
        )
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
