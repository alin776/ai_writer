"""积分服务"""

from datetime import datetime, timedelta
from decimal import Decimal
from typing import Optional, Tuple
from uuid import UUID

from sqlalchemy import select, and_, func
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.user_credits import UserCredits
from app.models.credit_transaction import CreditTransaction
from app.models.ai_call_log import AICallLog
from app.core.config import settings
from app.services.credits.credit_exceptions import (
    InsufficientCreditsError,
    CreditsExpiredError
)
from app.utils.datetime_utils import get_utc_now


class CreditService:
    """积分服务"""

    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_or_create_credits(
        self,
        user_id: UUID,
        gift_credits: Optional[Decimal] = None,
        commit: bool = True
    ) -> UserCredits:
        """
        获取或创建用户积分记录

        Args:
            user_id: 用户ID
            gift_credits: 新用户赠送积分（可选，默认使用配置值）
            commit: 是否立即提交（默认 True；在外层控制事务时传 False）

        Returns:
            UserCredits: 用户积分记录
        """
        # 查询是否已存在
        stmt = select(UserCredits).where(UserCredits.user_id == user_id)
        result = await self.db.execute(stmt)
        credits = result.scalar_one_or_none()

        if credits:
            return credits

        # 创建新记录
        gift_amount = gift_credits if gift_credits is not None else Decimal(str(settings.NEW_USER_GIFT_CREDITS))

        # 计算过期时间
        expires_at = None
        if settings.CREDITS_EXPIRE_DAYS > 0:
            expires_at = get_utc_now() + timedelta(days=settings.CREDITS_EXPIRE_DAYS)

        credits = UserCredits(
            user_id=user_id,
            balance=gift_amount,
            total_gifted=gift_amount,
            expires_at=expires_at
        )
        self.db.add(credits)

        # 如果有赠送积分，创建交易记录
        if gift_amount > 0:
            transaction = CreditTransaction(
                user_id=user_id,
                type="gift",
                amount=gift_amount,
                balance_before=Decimal("0.00"),
                balance_after=gift_amount,
                description="新用户注册赠送",
                related_type="new_user"
            )
            self.db.add(transaction)

        if commit:
            await self.db.commit()
        else:
            await self.db.flush()
        await self.db.refresh(credits)
        return credits

    async def get_balance(self, user_id: UUID) -> dict:
        """
        查询用户余额

        Args:
            user_id: 用户ID

        Returns:
            dict: 余额信息
        """
        credits = await self.get_or_create_credits(user_id, commit=True)

        # 检查是否过期
        is_expired = False
        if credits.expires_at and credits.expires_at < get_utc_now():
            is_expired = True

        return {
            "balance": float(credits.balance),
            "total_recharged": float(credits.total_recharged),
            "total_consumed": float(credits.total_consumed),
            "total_gifted": float(credits.total_gifted),
            "expires_at": credits.expires_at.isoformat() if credits.expires_at else None,
            "is_expired": is_expired
        }

    async def check_sufficient(
        self,
        user_id: UUID,
        required_credits: Decimal
    ) -> Tuple[bool, Decimal]:
        """
        检查余额是否充足

        Args:
            user_id: 用户ID
            required_credits: 需要的积分数量

        Returns:
            Tuple[bool, Decimal]: (是否充足, 当前余额)
        """
        credits = await self.get_or_create_credits(user_id, commit=True)

        # 检查是否过期
        if credits.expires_at and credits.expires_at < get_utc_now():
            return False, credits.balance

        # 检查余额
        is_sufficient = credits.balance >= required_credits
        return is_sufficient, credits.balance

    async def consume(
        self,
        user_id: UUID,
        amount: Decimal,
        description: str,
        related_id: Optional[UUID] = None,
        skip_check: bool = False,
        auto_commit: bool = True  # ✅ 2025-12-14: 支持外层事务控制
    ) -> Optional[CreditTransaction]:
        """
        消费积分（AI调用扣费）

        Args:
            user_id: 用户ID
            amount: 消费数量（正数）
            description: 描述
            related_id: 关联的 ai_call_log ID
            skip_check: 跳过检查（管理员豁免）
            auto_commit: 是否自动提交（默认True）。设为False时由外层控制事务

        Returns:
            CreditTransaction: 交易记录（管理员豁免时返回 None）

        Raises:
            InsufficientCreditsError: 余额不足
            CreditsExpiredError: 积分已过期
            ValueError: 积分记录不存在
        """
        # 管理员豁免
        if skip_check:
            return None

        # ✅ Critical修复2: 获取用户积分记录（加锁）
        stmt = select(UserCredits).where(
            UserCredits.user_id == user_id
        ).with_for_update()
        result = await self.db.execute(stmt)
        credits = result.scalar_one_or_none()

        # ❌ 删除自动创建逻辑，避免竞态条件
        # 积分记录应该在用户注册时创建，不应该在扣费时创建
        if not credits:
            raise ValueError(
                f"用户 {user_id} 的积分记录不存在。"
                "积分记录应该在用户注册时创建，请检查注册流程。"
            )

        # 检查是否过期
        if credits.expires_at and credits.expires_at < get_utc_now():
            raise CreditsExpiredError(credits.expires_at)

        # 检查余额是否充足
        if credits.balance < amount:
            raise InsufficientCreditsError(amount, credits.balance)

        # 扣减余额
        balance_before = credits.balance
        credits.balance -= amount
        credits.total_consumed += amount
        balance_after = credits.balance

        # 创建交易记录
        transaction = CreditTransaction(
            user_id=user_id,
            type="consume",
            amount=-amount,  # 负数表示消费
            balance_before=balance_before,
            balance_after=balance_after,
            description=description,
            related_type="ai_call",
            related_id=related_id
        )
        self.db.add(transaction)

        # ✅ 2025-12-14: 支持外层事务控制
        if auto_commit:
            await self.db.commit()
            await self.db.refresh(transaction)
        else:
            # 仅 flush 获取 ID，不提交事务
            await self.db.flush()

        return transaction

    async def recharge(
        self,
        user_id: UUID,
        amount: Decimal,
        description: str,
        related_id: UUID
    ) -> CreditTransaction:
        """
        充值积分（兑换码兑换）

        Args:
            user_id: 用户ID
            amount: 充值数量
            description: 描述
            related_id: 关联的 redeem_code ID

        Returns:
            CreditTransaction: 交易记录
        """
        # 获取或创建用户积分记录
        credits = await self.get_or_create_credits(user_id)

        # 增加余额
        balance_before = credits.balance
        credits.balance += amount
        credits.total_recharged += amount
        balance_after = credits.balance

        # 延长过期时间（如果配置了有效期）
        if settings.CREDITS_EXPIRE_DAYS > 0:
            new_expires = get_utc_now() + timedelta(days=settings.CREDITS_EXPIRE_DAYS)
            if not credits.expires_at or new_expires > credits.expires_at:
                credits.expires_at = new_expires

        # 创建交易记录
        transaction = CreditTransaction(
            user_id=user_id,
            type="recharge",
            amount=amount,
            balance_before=balance_before,
            balance_after=balance_after,
            description=description,
            related_type="redeem_code",
            related_id=related_id
        )
        self.db.add(transaction)

        await self.db.commit()
        await self.db.refresh(transaction)
        return transaction

    async def gift(
        self,
        user_id: UUID,
        amount: Decimal,
        description: str,
        related_type: str = "admin_gift",
        commit: bool = True
    ) -> CreditTransaction:
        """
        赠送积分（管理员/邀请奖励）

        Args:
            user_id: 用户ID
            amount: 赠送数量
            description: 描述
            related_type: 关联类型 (admin_gift / invitation_reward)

        Returns:
            CreditTransaction: 交易记录
        """
        # 获取或创建用户积分记录
        credits = await self.get_or_create_credits(user_id)

        # 增加余额
        balance_before = credits.balance
        credits.balance += amount
        credits.total_gifted += amount
        balance_after = credits.balance

        # 创建交易记录
        transaction = CreditTransaction(
            user_id=user_id,
            type="gift",
            amount=amount,
            balance_before=balance_before,
            balance_after=balance_after,
            description=description,
            related_type=related_type
        )
        self.db.add(transaction)

        if commit:
            await self.db.commit()
        else:
            await self.db.flush()

        await self.db.refresh(transaction)
        return transaction

    async def refund(
        self,
        user_id: UUID,
        amount: Decimal,
        description: str,
        related_id: Optional[UUID] = None
    ) -> CreditTransaction:
        """
        退还积分（AI调用失败时）

        Args:
            user_id: 用户ID
            amount: 退还数量
            description: 描述
            related_id: 关联的 ai_call_log ID

        Returns:
            CreditTransaction: 交易记录
        """
        credits = await self.get_or_create_credits(user_id)

        # 增加余额
        balance_before = credits.balance
        credits.balance += amount
        # 注意：退还不减少 total_consumed，因为已经消费过了
        balance_after = credits.balance

        # 创建交易记录
        transaction = CreditTransaction(
            user_id=user_id,
            type="refund",
            amount=amount,
            balance_before=balance_before,
            balance_after=balance_after,
            description=description,
            related_type="ai_call",
            related_id=related_id
        )
        self.db.add(transaction)

        await self.db.commit()
        await self.db.refresh(transaction)
        return transaction

    async def get_transactions(
        self,
        user_id: UUID,
        page: int = 1,
        page_size: int = 20,
        type: Optional[str] = None,
        start_date: Optional[datetime] = None,
        end_date: Optional[datetime] = None
    ) -> dict:
        """
        查询交易记录

        Args:
            user_id: 用户ID
            page: 页码
            page_size: 每页数量
            type: 筛选类型
            start_date: 开始日期
            end_date: 结束日期

        Returns:
            dict: 分页结果
        """
        # 构建查询条件
        conditions = [CreditTransaction.user_id == user_id]

        if type:
            conditions.append(CreditTransaction.type == type)

        if start_date:
            conditions.append(CreditTransaction.created_at >= start_date)

        if end_date:
            conditions.append(CreditTransaction.created_at <= end_date)

        # 查询总数
        count_stmt = select(func.count()).select_from(CreditTransaction).where(and_(*conditions))
        total_result = await self.db.execute(count_stmt)
        total = total_result.scalar()

        # 查询分页数据
        offset = (page - 1) * page_size
        stmt = select(CreditTransaction).where(
            and_(*conditions)
        ).order_by(
            CreditTransaction.created_at.desc()
        ).offset(offset).limit(page_size)

        result = await self.db.execute(stmt)
        transactions = result.scalars().all()

        # 批量查询关联的 AICallLog（一条 SQL，非 N+1）
        ai_call_ids = [
            t.related_id for t in transactions
            if t.related_type == "ai_call" and t.related_id
        ]
        token_details_map: dict = {}
        if ai_call_ids:
            logs_result = await self.db.execute(
                select(AICallLog).where(AICallLog.id.in_(ai_call_ids))
            )
            for log in logs_result.scalars():
                token_details_map[str(log.id)] = {
                    "model_name": log.model_name,
                    "prompt_tokens": log.prompt_tokens,
                    "completion_tokens": log.completion_tokens,
                    "total_tokens": log.total_tokens,
                    "cache_read_tokens": log.cache_read_tokens,
                    "cache_creation_tokens": log.cache_creation_tokens,
                    "reasoning_tokens": log.reasoning_tokens,
                    "prompt_cost": log.prompt_cost,
                    "completion_cost": log.completion_cost,
                    "total_cost": log.total_cost,
                }

        # 从 DB 读取定价元数据（get_model_pricing 已保证返回含 default 键的有效数据）
        from app.services.system_config_service import SystemConfigService
        model_pricing = await SystemConfigService.get_model_pricing(self.db)
        credits_per_dollar = await SystemConfigService.get_credits_per_dollar(self.db)

        return {
            "items": [
                {
                    "id": str(t.id),
                    "type": t.type,
                    "amount": float(t.amount),
                    "balance_before": float(t.balance_before),
                    "balance_after": float(t.balance_after),
                    "description": t.description,
                    "related_type": t.related_type,
                    "related_id": str(t.related_id) if t.related_id else None,
                    "created_at": t.created_at.isoformat(),
                    "token_details": token_details_map.get(str(t.related_id)) if t.related_type == "ai_call" else None,
                }
                for t in transactions
            ],
            "total": total,
            "page": page,
            "page_size": page_size,
            "total_pages": (total + page_size - 1) // page_size,
            "pricing_info": {
                "credits_per_dollar": credits_per_dollar,
                "model_pricing": model_pricing,
            },
        }
