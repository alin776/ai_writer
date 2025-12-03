"""用户端积分API"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.core.security import get_current_user
from app.models.user import User
from app.services.credits.credit_service import CreditService
from app.services.credits.redeem_code_service import RedeemCodeService
from app.services.credits.credit_exceptions import (
    RedeemCodeNotFoundError,
    RedeemCodeUsedError,
    RedeemCodeExpiredError
)
from app.schemas.credits import (
    BalanceResponse,
    TransactionListRequest,
    TransactionListResponse,
    RedeemRequest,
    RedeemResponse
)

router = APIRouter()


@router.get("/balance", response_model=BalanceResponse)
async def get_balance(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """
    查询积分余额

    返回当前用户的积分余额及统计信息
    """
    credit_service = CreditService(db)
    balance_info = await credit_service.get_balance(current_user.id)
    return balance_info


@router.get("/transactions", response_model=TransactionListResponse)
async def get_transactions(
    page: int = 1,
    page_size: int = 20,
    type: str = None,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """
    查询交易记录

    - **page**: 页码（从1开始）
    - **page_size**: 每页数量（1-100）
    - **type**: 筛选类型（可选：recharge/consume/gift/refund）
    """
    credit_service = CreditService(db)
    transactions = await credit_service.get_transactions(
        user_id=current_user.id,
        page=page,
        page_size=page_size,
        type=type
    )
    return transactions


@router.post("/redeem", response_model=RedeemResponse)
async def redeem_code(
    request: RedeemRequest,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """
    兑换码兑换

    - **code**: 12位兑换码

    成功兑换后会增加相应积分
    """
    redeem_service = RedeemCodeService(db)

    try:
        result = await redeem_service.redeem(
            code=request.code,
            user_id=current_user.id
        )
        return result
    except RedeemCodeNotFoundError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )
    except RedeemCodeUsedError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except RedeemCodeExpiredError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
