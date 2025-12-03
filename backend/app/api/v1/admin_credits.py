"""管理端积分系统API"""

from decimal import Decimal
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from uuid import UUID

from app.core.database import get_db
from app.core.security import get_current_active_user
from app.models.user import User
from app.models.user_credits import UserCredits
from app.models.credit_transaction import CreditTransaction
from app.services.credits.credit_service import CreditService
from app.services.credits.redeem_code_service import RedeemCodeService
from app.schemas.admin_credits import (
    AdminRedeemCodeGenerateRequest,
    AdminRedeemCodeListRequest,
    AdminRedeemCodeListResponse,
    AdminGiftCreditsRequest,
    AdminGiftCreditsResponse,
    AdminCreditsStatsResponse
)

router = APIRouter()


def check_admin_permission(current_user: User = Depends(get_current_active_user)) -> User:
    """检查是否为管理员"""
    if not current_user.is_admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Admin permission required"
        )
    return current_user


@router.post("/codes/generate")
async def generate_redeem_codes(
    request: AdminRedeemCodeGenerateRequest,
    current_user: User = Depends(check_admin_permission),
    db: AsyncSession = Depends(get_db)
):
    """
    批量生成兑换码（管理员）

    - **count**: 生成数量（1-100）
    - **credits**: 每个兑换码的积分数
    - **expires_days**: 有效期天数（可选）
    - **remark**: 备注信息（可选）

    返回生成的兑换码列表
    """
    redeem_service = RedeemCodeService(db)

    codes = await redeem_service.generate_codes(
        count=request.count,
        credits=Decimal(str(request.credits)),
        expires_days=request.expires_days,
        remark=request.remark,
        created_by=current_user.id
    )

    return {
        "codes": [
            {
                "id": str(c.id),
                "code": c.code,
                "credits": float(c.credits),
                "expires_at": c.expires_at.isoformat() if c.expires_at else None,
                "remark": c.remark,
                "created_at": c.created_at.isoformat()
            }
            for c in codes
        ],
        "count": len(codes)
    }


@router.get("/codes", response_model=AdminRedeemCodeListResponse)
async def list_redeem_codes(
    page: int = 1,
    page_size: int = 20,
    is_used: bool = None,
    is_expired: bool = None,
    current_user: User = Depends(check_admin_permission),
    db: AsyncSession = Depends(get_db)
):
    """
    查询兑换码列表（管理员）

    - **page**: 页码
    - **page_size**: 每页数量
    - **is_used**: 筛选已使用/未使用
    - **is_expired**: 筛选已过期/未过期
    """
    redeem_service = RedeemCodeService(db)

    result = await redeem_service.list_codes(
        page=page,
        page_size=page_size,
        is_used=is_used,
        is_expired=is_expired
    )

    return result


@router.post("/gift", response_model=AdminGiftCreditsResponse)
async def gift_credits(
    request: AdminGiftCreditsRequest,
    current_user: User = Depends(check_admin_permission),
    db: AsyncSession = Depends(get_db)
):
    """
    赠送积分（管理员）

    - **user_id**: 用户ID
    - **amount**: 赠送数量
    - **description**: 赠送原因

    向指定用户赠送积分
    """
    credit_service = CreditService(db)

    # 验证用户是否存在
    user_stmt = select(User).where(User.id == UUID(request.user_id))
    user_result = await db.execute(user_stmt)
    user = user_result.scalar_one_or_none()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )

    # 赠送积分
    transaction = await credit_service.gift(
        user_id=UUID(request.user_id),
        amount=Decimal(str(request.amount)),
        description=request.description,
        related_type="admin_gift"
    )

    return {
        "user_id": str(transaction.user_id),
        "amount": float(transaction.amount),
        "balance_before": float(transaction.balance_before),
        "balance_after": float(transaction.balance_after),
        "description": transaction.description,
        "created_at": transaction.created_at.isoformat()
    }


@router.get("/stats", response_model=AdminCreditsStatsResponse)
async def get_credits_stats(
    current_user: User = Depends(check_admin_permission),
    db: AsyncSession = Depends(get_db)
):
    """
    查询积分统计（管理员）

    返回系统积分统计信息：
    - 总用户数
    - 总余额
    - 总充值
    - 总消费
    - 总赠送
    - 总交易数
    """
    # 统计用户数
    total_users = await db.scalar(select(func.count(UserCredits.id)))

    # 统计总余额
    total_balance = await db.scalar(select(func.sum(UserCredits.balance))) or Decimal("0")

    # 统计总充值
    total_recharged = await db.scalar(select(func.sum(UserCredits.total_recharged))) or Decimal("0")

    # 统计总消费
    total_consumed = await db.scalar(select(func.sum(UserCredits.total_consumed))) or Decimal("0")

    # 统计总赠送
    total_gifted = await db.scalar(select(func.sum(UserCredits.total_gifted))) or Decimal("0")

    # 统计总交易数
    total_transactions = await db.scalar(select(func.count(CreditTransaction.id)))

    return {
        "total_users": total_users or 0,
        "total_balance": float(total_balance),
        "total_recharged": float(total_recharged),
        "total_consumed": float(total_consumed),
        "total_gifted": float(total_gifted),
        "total_transactions": total_transactions or 0
    }
