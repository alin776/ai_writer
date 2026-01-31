"""邀请服务"""

import secrets
from datetime import datetime, timedelta
from decimal import Decimal
from typing import List, Optional, Set, Tuple
from uuid import UUID

from sqlalchemy import select, and_, or_, func
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.user import User
from app.models.user_invitation import UserInvitation
from app.models.invitation_usage import InvitationUsage
from app.models.credit_transaction import CreditTransaction
from app.core.config import settings
from app.services.credits.credit_service import CreditService
from app.services.credits.credit_exceptions import (
    InvitationQuotaExceededError,
    InvitationCodeInvalidError,
    InvitationCodeExpiredError,
    InvitationCodeFullError,
    AntiAbuseLimitError
)
from app.utils.datetime_utils import get_utc_now


# 有效字符集：排除易混淆字符
VALID_CHARS = "ABCDEFGHJKMNPQRSTUVWXYZ23456789"


class InvitationService:
    """邀请服务"""

    def __init__(self, db: AsyncSession):
        self.db = db
        self.credit_service = CreditService(db)

    def _generate_unique_code(self, existing_codes: Set[str], length: int = 8) -> str:
        """生成唯一邀请码"""
        max_attempts = 100
        for _ in range(max_attempts):
            code = ''.join(secrets.choice(VALID_CHARS) for _ in range(length))
            if code not in existing_codes:
                return code
        raise Exception("生成唯一邀请码失败")

    async def generate_invitation_code(
        self,
        user_id: UUID,
        max_uses: int = 3,
        expires_days: int = 60
    ) -> UserInvitation:
        """
        生成邀请码

        Args:
            user_id: 用户ID
            max_uses: 最大使用次数（默认3次）
            expires_days: 有效期天数（固定60天）

        Returns:
            UserInvitation: 邀请码记录

        Raises:
            InvitationQuotaExceededError: 超过生成数量限制
        """
        # 查询用户信息
        user_stmt = select(User).where(User.id == user_id)
        user_result = await self.db.execute(user_stmt)
        user = user_result.scalar_one()

        # 查询已有邀请码数量
        count_stmt = select(func.count()).select_from(UserInvitation).where(
            UserInvitation.user_id == user_id
        )
        count_result = await self.db.execute(count_stmt)
        existing_count = count_result.scalar()

        if existing_count >= settings.USER_MAX_INVITATION_CODES:
            raise InvitationQuotaExceededError(settings.USER_MAX_INVITATION_CODES)

        # 查询现有邀请码（避免重复）
        code_stmt = select(UserInvitation.code)
        code_result = await self.db.execute(code_stmt)
        existing_codes = set(code_result.scalars().all())

        # 生成唯一邀请码
        code_str = self._generate_unique_code(existing_codes)

        # 计算过期时间（固定60天）
        expires_at = get_utc_now() + timedelta(days=expires_days)

        # 创建邀请码
        invitation = UserInvitation(
            user_id=user_id,
            code=code_str,
            max_uses=max_uses,
            expires_at=expires_at
        )
        self.db.add(invitation)
        await self.db.commit()
        await self.db.refresh(invitation)

        return invitation

    async def validate_invitation_code(
        self,
        code: str,
        ip_address: Optional[str] = None,
        device_fingerprint: Optional[str] = None
    ) -> Tuple[bool, str, Optional[UserInvitation]]:
        """
        验证邀请码

        Args:
            code: 邀请码
            ip_address: IP 地址
            device_fingerprint: 设备指纹

        Returns:
            Tuple[bool, str, Optional[UserInvitation]]:
                (是否有效, 错误信息, 邀请码记录)
        """
        # 查询邀请码
        stmt = select(UserInvitation).where(UserInvitation.code == code.upper())
        result = await self.db.execute(stmt)
        invitation = result.scalar_one_or_none()

        if not invitation:
            return False, "邀请码不存在", None

        # 检查过期
        if invitation.expires_at and invitation.expires_at < get_utc_now():
            return False, "邀请码已过期", invitation

        # 检查使用次数
        if invitation.used_count >= invitation.max_uses:
            return False, "邀请码使用次数已满", invitation

        # 防刷检查
        if ip_address:
            # IP限制：同一IP 24小时内最多注册N次
            time_24h_ago = get_utc_now() - timedelta(hours=24)
            ip_stmt = select(func.count()).select_from(InvitationUsage).where(
                and_(
                    InvitationUsage.ip_address == ip_address,
                    InvitationUsage.created_at >= time_24h_ago
                )
            )
            ip_result = await self.db.execute(ip_stmt)
            ip_count = ip_result.scalar()

            if ip_count >= settings.SAME_IP_REGISTER_LIMIT_24H:
                return False, f"该IP地址24小时内注册次数过多，请稍后再试", invitation

        if device_fingerprint:
            # 设备限制：同一设备7天内最多注册N次
            time_7d_ago = get_utc_now() - timedelta(days=7)
            device_stmt = select(func.count()).select_from(InvitationUsage).where(
                and_(
                    InvitationUsage.device_fingerprint == device_fingerprint,
                    InvitationUsage.created_at >= time_7d_ago
                )
            )
            device_result = await self.db.execute(device_stmt)
            device_count = device_result.scalar()

            if device_count >= settings.SAME_DEVICE_REGISTER_LIMIT_7D:
                return False, f"该设备7天内注册次数过多，请稍后再试", invitation

        return True, "", invitation

    async def use_invitation_code(
        self,
        code: str,
        invitee_id: UUID,
        ip_address: Optional[str] = None,
        device_fingerprint: Optional[str] = None
    ) -> InvitationUsage:
        """
        使用邀请码（注册时调用）

        Args:
            code: 邀请码
            invitee_id: 被邀请人 ID
            ip_address: IP 地址
            device_fingerprint: 设备指纹

        Returns:
            InvitationUsage: 使用记录

        Raises:
            InvitationCodeInvalidError: 邀请码无效
        """
        # 验证邀请码（包含防刷检查）
        is_valid, error_msg, _ = await self.validate_invitation_code(
            code, ip_address, device_fingerprint
        )

        if not is_valid:
            raise InvitationCodeInvalidError(error_msg)

        # ✅ High修复5: 加锁后重新检查状态（二次验证）
        # 增加使用次数（加锁）
        stmt = select(UserInvitation).where(
            UserInvitation.code == code.upper()
        ).with_for_update()
        result = await self.db.execute(stmt)
        invitation = result.scalar_one()

        # ✅ 锁内二次验证：检查过期时间
        if invitation.expires_at and invitation.expires_at < get_utc_now():
            raise InvitationCodeExpiredError(invitation.expires_at)

        # ✅ 锁内二次验证：检查使用次数
        if invitation.used_count >= invitation.max_uses:
            raise InvitationCodeFullError(invitation.max_uses)

        # 增加使用次数
        invitation.used_count += 1

        # 创建使用记录
        usage = InvitationUsage(
            invitation_id=invitation.id,
            invitee_id=invitee_id,
            ip_address=ip_address,
            device_fingerprint=device_fingerprint,
            status="pending"
        )
        self.db.add(usage)

        await self.db.flush()
        await self.db.refresh(usage)
        return usage

    async def check_activation(
        self,
        invitee_id: UUID
    ) -> Tuple[bool, Decimal, Decimal]:
        """
        检查激活条件

        Args:
            invitee_id: 被邀请人 ID

        Returns:
            Tuple[bool, Decimal, Decimal]:
                (是否满足, 已消费积分, 已充值积分)
        """
        # 查询邀请使用记录
        usage_stmt = select(InvitationUsage).where(
            InvitationUsage.invitee_id == invitee_id
        )
        usage_result = await self.db.execute(usage_stmt)
        usage = usage_result.scalar_one_or_none()

        if not usage or usage.status == "active":
            return False, Decimal("0"), Decimal("0")

        # 检查是否超过7天
        deadline = usage.created_at + timedelta(days=settings.INVITATION_ACTIVATION_DEADLINE_DAYS)
        if get_utc_now() > deadline:
            # 标记为过期
            usage.status = "expired"
            await self.db.commit()
            return False, Decimal("0"), Decimal("0")

        # 查询累计消费积分
        consume_stmt = select(func.sum(CreditTransaction.amount)).where(
            and_(
                CreditTransaction.user_id == invitee_id,
                CreditTransaction.type == "consume"
            )
        )
        consume_result = await self.db.execute(consume_stmt)
        total_consumed = abs(consume_result.scalar() or Decimal("0"))

        # 查询累计充值积分
        recharge_stmt = select(func.sum(CreditTransaction.amount)).where(
            and_(
                CreditTransaction.user_id == invitee_id,
                CreditTransaction.type == "recharge"
            )
        )
        recharge_result = await self.db.execute(recharge_stmt)
        total_recharged = recharge_result.scalar() or Decimal("0")

        # 判断是否满足激活条件
        min_consume = Decimal(str(settings.INVITATION_ACTIVATION_MIN_CONSUME))
        min_recharge = Decimal(str(settings.INVITATION_ACTIVATION_MIN_RECHARGE))

        is_activated = (total_consumed >= min_consume) or (total_recharged >= min_recharge)

        return is_activated, total_consumed, total_recharged

    async def activate_invitation(
        self,
        invitee_id: UUID,
        force: bool = False,
        commit: bool = True
    ) -> Optional[dict]:
        """
        激活邀请（奖励邀请人）

        Args:
            invitee_id: 被邀请人 ID
            force: 强制激活（注册即奖励模式，跳过消费/充值检查）
            commit: 是否在函数内部提交事务（嵌套事务时传 False）

        Returns:
            Optional[dict]: 奖励信息（如果激活成功）
        """
        # ✅ High修复4: 先加锁，然后在锁内检查激活条件，避免重复发放奖励
        # 查询邀请使用记录（加锁）
        usage_stmt = select(InvitationUsage).where(
            InvitationUsage.invitee_id == invitee_id
        ).with_for_update()
        usage_result = await self.db.execute(usage_stmt)
        usage = usage_result.scalar_one_or_none()

        # 记录不存在或已经激活，直接返回
        if not usage or usage.status == "active":
            return None

        # 如果不是强制激活，检查激活条件
        if not force:
            # 检查是否超过7天
            deadline = usage.created_at + timedelta(days=settings.INVITATION_ACTIVATION_DEADLINE_DAYS)
            if get_utc_now() > deadline:
                # 标记为过期
                usage.status = "expired"
                if commit:
                    await self.db.commit()
                else:
                    await self.db.flush()
                return None

            # 查询累计消费积分
            consume_stmt = select(func.sum(CreditTransaction.amount)).where(
                and_(
                    CreditTransaction.user_id == invitee_id,
                    CreditTransaction.type == "consume"
                )
            )
            consume_result = await self.db.execute(consume_stmt)
            total_consumed = abs(consume_result.scalar() or Decimal("0"))

            # 查询累计充值积分
            recharge_stmt = select(func.sum(CreditTransaction.amount)).where(
                and_(
                    CreditTransaction.user_id == invitee_id,
                    CreditTransaction.type == "recharge"
                )
            )
            recharge_result = await self.db.execute(recharge_stmt)
            total_recharged = recharge_result.scalar() or Decimal("0")

            # 判断是否满足激活条件
            min_consume = Decimal(str(settings.INVITATION_ACTIVATION_MIN_CONSUME))
            min_recharge = Decimal(str(settings.INVITATION_ACTIVATION_MIN_RECHARGE))

            is_activated = (total_consumed >= min_consume) or (total_recharged >= min_recharge)

            if not is_activated:
                return None

        # 查询邀请码（加锁）
        invitation_stmt = select(UserInvitation).where(
            UserInvitation.id == usage.invitation_id
        ).with_for_update()
        invitation_result = await self.db.execute(invitation_stmt)
        invitation = invitation_result.scalar_one()

        # 更新邀请使用记录
        usage.status = "active"
        usage.activated_at = get_utc_now()

        # 更新邀请码统计
        invitation.activated_count += 1

        # 初始化奖励金额
        reward_amount = Decimal("0")

        # 查询邀请码创建者，判断是否是管理员
        creator_stmt = select(User).where(User.id == invitation.user_id)
        creator_result = await self.db.execute(creator_stmt)
        creator = creator_result.scalar_one()

        # 只有普通用户创建的邀请码才发放奖励（管理员不需要积分回馈）
        if not creator.is_admin:
            reward_amount = Decimal(str(settings.INVITATION_REWARD_CREDITS))
            invitation.total_rewards += reward_amount

            # 给邀请人赠送积分
            await self.credit_service.gift(
                user_id=invitation.user_id,
                amount=reward_amount,
                description=f"邀请奖励: 邀请 {invitee_id} 激活成功",
                related_type="invitation_reward",
                commit=commit
            )

        if commit:
            await self.db.commit()
        else:
            await self.db.flush()

        return {
            "inviter_id": str(invitation.user_id),
            "invitee_id": str(invitee_id),
            "reward_credits": float(reward_amount),
            "activated_at": usage.activated_at.isoformat()
        }

    async def get_my_invitations(self, user_id: UUID) -> List[dict]:
        """
        查询我的邀请码

        Args:
            user_id: 用户ID

        Returns:
            List[dict]: 邀请码列表
        """
        # ✅ High修复6: 使用selectinload预加载关联数据，避免N+1查询
        from sqlalchemy.orm import selectinload

        stmt = select(UserInvitation).where(
            UserInvitation.user_id == user_id
        ).options(
            # 预加载邀请使用记录和被邀请人信息
            selectinload(UserInvitation.usages).selectinload(InvitationUsage.invitee)
        ).order_by(UserInvitation.created_at.desc())

        result = await self.db.execute(stmt)
        invitations = result.scalars().all()

        items = []
        for inv in invitations:
            # ✅ 直接使用预加载的关联数据，无需额外查询
            invitees = [
                {
                    "username": usage.invitee.username,
                    "status": usage.status,
                    "registered_at": usage.created_at.isoformat(),
                    "activated_at": usage.activated_at.isoformat() if usage.activated_at else None
                }
                for usage in inv.usages
            ]

            items.append({
                "id": str(inv.id),
                "code": inv.code,
                "max_uses": inv.max_uses,
                "used_count": inv.used_count,
                "activated_count": inv.activated_count,
                "total_rewards": float(inv.total_rewards),
                "expires_at": inv.expires_at.isoformat() if inv.expires_at else None,
                "created_at": inv.created_at.isoformat(),
                "invitees": invitees
            })

        return items

    async def get_invitation_stats(self, user_id: UUID) -> dict:
        """
        查询邀请统计

        Args:
            user_id: 用户ID

        Returns:
            dict: 邀请统计
        """
        # 查询邀请码数量
        count_stmt = select(func.count()).select_from(UserInvitation).where(
            UserInvitation.user_id == user_id
        )
        count_result = await self.db.execute(count_stmt)
        total_invitations = count_result.scalar()

        # 查询统计数据
        stats_stmt = select(
            func.sum(UserInvitation.used_count).label('total_used'),
            func.sum(UserInvitation.activated_count).label('total_activated'),
            func.sum(UserInvitation.total_rewards).label('total_rewards')
        ).where(UserInvitation.user_id == user_id)
        stats_result = await self.db.execute(stats_stmt)
        stats = stats_result.one()

        can_generate_more = total_invitations < settings.USER_MAX_INVITATION_CODES
        remaining_quota = settings.USER_MAX_INVITATION_CODES - total_invitations

        return {
            "total_invitations": total_invitations,
            "total_used": stats.total_used or 0,
            "total_activated": stats.total_activated or 0,
            "total_rewards": float(stats.total_rewards or Decimal("0")),
            "can_generate_more": can_generate_more,
            "remaining_quota": remaining_quota
        }

    # ==================== 管理员方法 ====================

    async def generate_admin_invitation(
        self,
        admin_id: UUID,
        custom_code: Optional[str] = None,
        max_uses: int = 1,
        expires_days: int = 90,
        remark: Optional[str] = None
    ) -> UserInvitation:
        """
        管理员生成邀请码

        Args:
            admin_id: 管理员用户ID
            custom_code: 自定义邀请码（可选）
            max_uses: 最大使用次数（1-100）
            expires_days: 有效期天数（1-365）
            remark: 备注信息

        Returns:
            UserInvitation: 邀请码记录

        Raises:
            ValueError: 自定义邀请码已存在
        """
        # 处理邀请码
        if custom_code:
            # 验证自定义邀请码是否已存在
            code_str = custom_code.upper().strip()
            check_stmt = select(UserInvitation).where(UserInvitation.code == code_str)
            check_result = await self.db.execute(check_stmt)
            if check_result.scalar_one_or_none():
                raise ValueError(f"邀请码 {code_str} 已存在")
        else:
            # 自动生成8位邀请码
            code_stmt = select(UserInvitation.code)
            code_result = await self.db.execute(code_stmt)
            existing_codes = set(code_result.scalars().all())
            code_str = self._generate_unique_code(existing_codes, length=8)

        # 计算过期时间
        expires_at = get_utc_now() + timedelta(days=expires_days)

        # 创建邀请码
        invitation = UserInvitation(
            user_id=admin_id,
            code=code_str,
            max_uses=max_uses,
            expires_at=expires_at,
            remark=remark
        )
        self.db.add(invitation)
        await self.db.commit()
        await self.db.refresh(invitation)

        return invitation

    async def list_all_invitations(
        self,
        page: int = 1,
        page_size: int = 20,
        status: Optional[str] = None,
        creator_id: Optional[UUID] = None,
        search: Optional[str] = None
    ) -> Tuple[List[dict], int, dict]:
        """
        管理员查询所有邀请码

        Args:
            page: 页码
            page_size: 每页数量
            status: 状态筛选 (active/expired/exhausted/all)
            creator_id: 创建者ID筛选
            search: 搜索关键词

        Returns:
            Tuple[List[dict], int, dict]: (邀请码列表, 总数, 统计信息)
        """
        # 构建查询条件
        conditions = []

        # 状态筛选
        now = get_utc_now()
        if status == "active":
            conditions.append(UserInvitation.used_count < UserInvitation.max_uses)
            conditions.append(
                or_(
                    UserInvitation.expires_at.is_(None),
                    UserInvitation.expires_at > now
                )
            )
        elif status == "expired":
            conditions.append(UserInvitation.expires_at <= now)
        elif status == "exhausted":
            conditions.append(UserInvitation.used_count >= UserInvitation.max_uses)

        # 创建者筛选
        if creator_id:
            conditions.append(UserInvitation.user_id == creator_id)

        # 搜索
        if search:
            search_pattern = f"%{search}%"
            conditions.append(
                or_(
                    UserInvitation.code.like(search_pattern),
                    UserInvitation.remark.like(search_pattern)
                )
            )

        # 查询总数
        count_stmt = select(func.count()).select_from(UserInvitation)
        if conditions:
            count_stmt = count_stmt.where(and_(*conditions))
        count_result = await self.db.execute(count_stmt)
        total = count_result.scalar()

        # 查询列表
        offset = (page - 1) * page_size
        stmt = (
            select(UserInvitation, User.username)
            .outerjoin(User, UserInvitation.user_id == User.id)
            .order_by(UserInvitation.created_at.desc())
            .offset(offset)
            .limit(page_size)
        )
        if conditions:
            stmt = stmt.where(and_(*conditions))

        result = await self.db.execute(stmt)
        rows = result.all()

        # 构建响应数据
        items = []
        for invitation, username in rows:
            # 判断状态
            if invitation.used_count >= invitation.max_uses:
                inv_status = "exhausted"
            elif invitation.expires_at and invitation.expires_at <= now:
                inv_status = "expired"
            else:
                inv_status = "active"

            # 计算使用率
            usage_rate = (invitation.used_count / invitation.max_uses * 100) if invitation.max_uses > 0 else 0

            items.append({
                "id": str(invitation.id),
                "code": invitation.code,
                "max_uses": invitation.max_uses,
                "used_count": invitation.used_count,
                "activated_count": invitation.activated_count,
                "total_rewards": float(invitation.total_rewards),
                "usage_rate": round(usage_rate, 2),
                "expires_at": invitation.expires_at.isoformat() if invitation.expires_at else None,
                "remark": invitation.remark,
                "creator_username": username,
                "created_at": invitation.created_at.isoformat(),
                "status": inv_status
            })

        # 查询统计信息
        stats_stmt = select(
            func.count(UserInvitation.id).label('total_codes'),
            func.sum(UserInvitation.used_count).label('total_usages'),
            func.sum(UserInvitation.activated_count).label('total_activated'),
            func.sum(UserInvitation.total_rewards).label('total_rewards')
        ).select_from(UserInvitation)

        stats_result = await self.db.execute(stats_stmt)
        stats_row = stats_result.one()

        # 统计各状态数量
        active_stmt = select(func.count()).select_from(UserInvitation).where(
            and_(
                UserInvitation.used_count < UserInvitation.max_uses,
                or_(
                    UserInvitation.expires_at.is_(None),
                    UserInvitation.expires_at > now
                )
            )
        )
        active_result = await self.db.execute(active_stmt)
        active_count = active_result.scalar()

        expired_stmt = select(func.count()).select_from(UserInvitation).where(
            UserInvitation.expires_at <= now
        )
        expired_result = await self.db.execute(expired_stmt)
        expired_count = expired_result.scalar()

        exhausted_stmt = select(func.count()).select_from(UserInvitation).where(
            UserInvitation.used_count >= UserInvitation.max_uses
        )
        exhausted_result = await self.db.execute(exhausted_stmt)
        exhausted_count = exhausted_result.scalar()

        stats = {
            "total_codes": stats_row.total_codes or 0,
            "active_codes": active_count,
            "expired_codes": expired_count,
            "exhausted_codes": exhausted_count,
            "total_usages": stats_row.total_usages or 0,
            "total_activated": stats_row.total_activated or 0,
            "total_rewards": float(stats_row.total_rewards or Decimal("0"))
        }

        return items, total, stats

    async def delete_invitation(self, invitation_id: UUID) -> bool:
        """
        删除邀请码

        Args:
            invitation_id: 邀请码ID

        Returns:
            bool: 是否成功

        Raises:
            ValueError: 邀请码不存在或已被使用
        """
        # 查询邀请码
        stmt = select(UserInvitation).where(UserInvitation.id == invitation_id)
        result = await self.db.execute(stmt)
        invitation = result.scalar_one_or_none()

        if not invitation:
            raise ValueError("邀请码不存在")

        # 检查是否已被使用
        if invitation.used_count > 0:
            raise ValueError("邀请码已被使用，无法删除")

        # 删除邀请码
        await self.db.delete(invitation)
        await self.db.commit()

        return True
