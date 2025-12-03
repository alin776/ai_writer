"""用户端邀请API"""

from fastapi import APIRouter, Depends, HTTPException, status, Request
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.core.security import get_current_user
from app.models.user import User
from app.services.invitations.invitation_service import InvitationService
from app.services.credits.credit_exceptions import (
    InvitationQuotaExceededError,
    NewUserCooldownError,
    InvitationCodeInvalidError
)
from app.schemas.invitations import (
    InvitationGenerateRequest,
    InvitationResponse,
    InvitationValidateRequest,
    InvitationValidateResponse,
    InvitationStatsResponse
)
from app.utils.device_parser import get_client_ip
from typing import List

router = APIRouter()


@router.post("/generate", response_model=InvitationResponse, status_code=status.HTTP_201_CREATED)
async def generate_invitation(
    request: InvitationGenerateRequest,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """
    生成邀请码

    - **max_uses**: 最大使用次数（固定1次）
    - **expires_days**: 有效期天数（固定60天）

    **限制**:
    - 每位用户最多生成3个邀请码
    - 新用户需等待72小时后才能生成
    - 每个邀请码只能使用1次
    - 有效期固定为60天（2个月）
    """
    invitation_service = InvitationService(db)

    try:
        invitation = await invitation_service.generate_invitation_code(
            user_id=current_user.id,
            max_uses=request.max_uses,
            expires_days=request.expires_days
        )

        # 查询被邀请人信息（新生成的码暂无）
        invitations = await invitation_service.get_my_invitations(current_user.id)
        matching_inv = next((inv for inv in invitations if inv["id"] == str(invitation.id)), None)

        return matching_inv if matching_inv else {
            "id": str(invitation.id),
            "code": invitation.code,
            "max_uses": invitation.max_uses,
            "used_count": invitation.used_count,
            "activated_count": invitation.activated_count,
            "total_rewards": float(invitation.total_rewards),
            "expires_at": invitation.expires_at.isoformat() if invitation.expires_at else None,
            "created_at": invitation.created_at.isoformat(),
            "invitees": []
        }
    except InvitationQuotaExceededError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except NewUserCooldownError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


@router.get("/my-codes", response_model=List[InvitationResponse])
async def get_my_invitations(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """
    查询我的邀请码

    返回当前用户创建的所有邀请码及使用情况
    """
    invitation_service = InvitationService(db)
    invitations = await invitation_service.get_my_invitations(current_user.id)
    return invitations


@router.get("/stats", response_model=InvitationStatsResponse)
async def get_invitation_stats(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """
    查询邀请统计

    返回邀请码总数、使用次数、激活次数、总奖励等统计信息
    """
    invitation_service = InvitationService(db)
    stats = await invitation_service.get_invitation_stats(current_user.id)
    return stats


@router.post("/validate", response_model=InvitationValidateResponse)
async def validate_invitation(
    request: InvitationValidateRequest,
    http_request: Request,
    db: AsyncSession = Depends(get_db)
):
    """
    验证邀请码（公开接口，无需登录）

    - **code**: 8位邀请码
    - **ip_address**: IP地址（可选，用于防刷检测）
    - **device_fingerprint**: 设备指纹（可选，用于防刷检测）

    返回邀请码是否有效及错误信息
    """
    invitation_service = InvitationService(db)

    # 获取IP地址
    ip_address = request.ip_address or get_client_ip(http_request)

    is_valid, error_msg, _ = await invitation_service.validate_invitation_code(
        code=request.code,
        ip_address=ip_address,
        device_fingerprint=request.device_fingerprint
    )

    return {
        "valid": is_valid,
        "message": error_msg if not is_valid else "邀请码有效"
    }
