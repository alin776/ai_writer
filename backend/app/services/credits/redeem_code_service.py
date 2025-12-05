"""兑换码服务"""

import secrets
from datetime import datetime, timedelta
from decimal import Decimal
from typing import List, Optional, Set
from uuid import UUID

from sqlalchemy import select, and_, or_, func, Integer
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.redeem_code import RedeemCode
from app.core.config import settings
from app.services.credits.credit_service import CreditService
from app.services.credits.credit_exceptions import (
    RedeemCodeNotFoundError,
    RedeemCodeUsedError,
    RedeemCodeExpiredError
)
from app.utils.datetime_utils import get_utc_now


# 有效字符集：排除易混淆字符 O, 0, I, 1, L
VALID_CHARS = "ABCDEFGHJKMNPQRSTUVWXYZ23456789"


class RedeemCodeService:
    """兑换码服务"""

    def __init__(self, db: AsyncSession):
        self.db = db
        self.credit_service = CreditService(db)

    def _generate_unique_code(self, existing_codes: Set[str], length: int = 12) -> str:
        """
        生成唯一兑换码

        Args:
            existing_codes: 已存在的兑换码集合
            length: 兑换码长度

        Returns:
            str: 唯一兑换码
        """
        max_attempts = 100
        for _ in range(max_attempts):
            code = ''.join(secrets.choice(VALID_CHARS) for _ in range(length))
            if code not in existing_codes:
                return code
        raise Exception("生成唯一兑换码失败")

    async def generate_codes(
        self,
        count: int,
        credits: Decimal,
        expires_days: Optional[int] = None,
        remark: Optional[str] = None,
        created_by: Optional[UUID] = None
    ) -> List[RedeemCode]:
        """
        批量生成兑换码

        Args:
            count: 生成数量（1-100）
            credits: 每个兑换码的积分数量
            expires_days: 有效期天数（默认使用配置值）
            remark: 备注
            created_by: 创建者（管理员）ID

        Returns:
            List[RedeemCode]: 生成的兑换码列表
        """
        if count < 1 or count > 100:
            raise ValueError("生成数量必须在 1-100 之间")

        # 计算过期时间
        expires_at = None
        days = expires_days if expires_days is not None else settings.REDEEM_CODE_EXPIRE_DAYS
        if days > 0:
            expires_at = get_utc_now() + timedelta(days=days)

        # 查询现有兑换码（避免重复）
        stmt = select(RedeemCode.code)
        result = await self.db.execute(stmt)
        existing_codes = set(result.scalars().all())

        # 批量生成
        codes = []
        for _ in range(count):
            code_str = self._generate_unique_code(existing_codes)
            existing_codes.add(code_str)

            code = RedeemCode(
                code=code_str,
                credits=credits,
                expires_at=expires_at,
                created_by=created_by,
                remark=remark
            )
            codes.append(code)
            self.db.add(code)

        await self.db.commit()

        # 刷新所有对象
        for code in codes:
            await self.db.refresh(code)

        return codes

    async def redeem(
        self,
        code: str,
        user_id: UUID
    ) -> dict:
        """
        兑换码兑换

        Args:
            code: 兑换码
            user_id: 用户ID

        Returns:
            dict: 兑换结果

        Raises:
            RedeemCodeNotFoundError: 兑换码不存在
            RedeemCodeUsedError: 兑换码已使用
            RedeemCodeExpiredError: 兑换码已过期
        """
        # 查询兑换码（加锁防止重复兑换）
        stmt = select(RedeemCode).where(
            RedeemCode.code == code.upper()
        ).with_for_update()
        result = await self.db.execute(stmt)
        redeem_code = result.scalar_one_or_none()

        # 验证兑换码
        if not redeem_code:
            raise RedeemCodeNotFoundError("兑换码不存在")

        if redeem_code.is_used:
            raise RedeemCodeUsedError(
                redeem_code.used_at,
                redeem_code.used_by
            )

        if redeem_code.expires_at and redeem_code.expires_at < get_utc_now():
            raise RedeemCodeExpiredError(redeem_code.expires_at)

        # 充值积分
        balance_info = await self.credit_service.get_balance(user_id)
        balance_before = Decimal(str(balance_info["balance"]))

        await self.credit_service.recharge(
            user_id=user_id,
            amount=redeem_code.credits,
            description=f"兑换码充值: {code}",
            related_id=redeem_code.id
        )

        balance_after = balance_before + redeem_code.credits

        # 更新兑换码状态
        redeem_code.is_used = True
        redeem_code.used_by = user_id
        redeem_code.used_at = get_utc_now()

        await self.db.commit()

        return {
            "credits": float(redeem_code.credits),
            "balance_before": float(balance_before),
            "balance_after": float(balance_after)
        }

    async def get_code(self, code_id: UUID) -> Optional[dict]:
        """
        查询单个兑换码

        Args:
            code_id: 兑换码ID

        Returns:
            dict: 兑换码信息
        """
        stmt = select(RedeemCode).where(RedeemCode.id == code_id)
        result = await self.db.execute(stmt)
        code = result.scalar_one_or_none()

        if not code:
            return None

        # 检查是否过期
        is_expired = False
        if code.expires_at and code.expires_at < get_utc_now():
            is_expired = True

        return {
            "id": str(code.id),
            "code": code.code,
            "credits": float(code.credits),
            "is_used": code.is_used,
            "used_by": str(code.used_by) if code.used_by else None,
            "used_at": code.used_at.isoformat() if code.used_at else None,
            "expires_at": code.expires_at.isoformat() if code.expires_at else None,
            "is_expired": is_expired,
            "created_by": str(code.created_by) if code.created_by else None,
            "remark": code.remark,
            "created_at": code.created_at.isoformat()
        }

    async def list_codes(
        self,
        page: int = 1,
        page_size: int = 20,
        is_used: Optional[bool] = None,
        is_expired: Optional[bool] = None,
        created_by: Optional[UUID] = None
    ) -> dict:
        """
        查询兑换码列表（管理员）

        Args:
            page: 页码
            page_size: 每页数量
            is_used: 筛选已使用/未使用
            is_expired: 筛选已过期/未过期
            created_by: 筛选创建者

        Returns:
            dict: 分页结果
        """
        # 构建查询条件
        conditions = []

        if is_used is not None:
            conditions.append(RedeemCode.is_used == is_used)

        if created_by is not None:
            conditions.append(RedeemCode.created_by == created_by)

        if is_expired is not None:
            if is_expired:
                conditions.append(RedeemCode.expires_at < get_utc_now())
            else:
                conditions.append(
                    or_(
                        RedeemCode.expires_at.is_(None),
                        RedeemCode.expires_at >= get_utc_now()
                    )
                )

        # 查询总数
        count_stmt = select(func.count()).select_from(RedeemCode)
        if conditions:
            count_stmt = count_stmt.where(and_(*conditions))
        total_result = await self.db.execute(count_stmt)
        total = total_result.scalar()

        # 查询分页数据
        offset = (page - 1) * page_size
        stmt = select(RedeemCode)
        if conditions:
            stmt = stmt.where(and_(*conditions))
        stmt = stmt.order_by(RedeemCode.created_at.desc()).offset(offset).limit(page_size)

        result = await self.db.execute(stmt)
        codes = result.scalars().all()

        # 统计数据
        stats_stmt = select(
            func.count().label('total_codes'),
            func.sum(func.cast(RedeemCode.is_used, Integer)).label('used_codes')
        ).select_from(RedeemCode)
        stats_result = await self.db.execute(stats_stmt)
        stats = stats_result.one()

        return {
            "items": [
                {
                    "id": str(c.id),
                    "code": c.code,
                    "credits": float(c.credits),
                    "is_used": c.is_used,
                    "used_at": c.used_at.isoformat() if c.used_at else None,
                    "expires_at": c.expires_at.isoformat() if c.expires_at else None,
                    "is_expired": c.expires_at < get_utc_now() if c.expires_at else False,
                    "remark": c.remark,
                    "created_at": c.created_at.isoformat()
                }
                for c in codes
            ],
            "total": total,
            "page": page,
            "page_size": page_size,
            "total_pages": (total + page_size - 1) // page_size,
            "stats": {
                "total_codes": stats.total_codes or 0,
                "used_codes": stats.used_codes or 0,
                "unused_codes": (stats.total_codes or 0) - (stats.used_codes or 0)
            }
        }
