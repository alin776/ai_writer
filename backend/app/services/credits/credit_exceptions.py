"""积分系统异常类"""

from datetime import datetime
from decimal import Decimal


class CreditError(Exception):
    """积分异常基类"""
    pass


class InsufficientCreditsError(CreditError):
    """余额不足

    🔧 2025-12-15: 改善错误提示，增加充值建议
    """
    def __init__(self, required: Decimal, available: Decimal, operation: str = "操作"):
        self.required = required
        self.available = available
        self.operation = operation
        self.shortfall = required - available  # 差额

        # 构建友好的错误消息
        message = (
            f"积分余额不足\n"
            f"- 当前余额：{float(available):.2f} 积分\n"
            f"- 预计需要：{float(required):.2f} 积分\n"
            f"- 差额：{float(self.shortfall):.2f} 积分\n"
            f"建议：请先充值至少 {float(self.shortfall):.0f} 积分后再试。"
        )
        super().__init__(message)

    def to_dict(self) -> dict:
        """转换为字典（用于 API 响应）"""
        return {
            "error": "insufficient_credits",
            "required": float(self.required),
            "available": float(self.available),
            "shortfall": float(self.shortfall),
            "operation": self.operation,
            "message": str(self),
            "suggestion": f"请充值至少 {float(self.shortfall):.0f} 积分"
        }


class CreditsExpiredError(CreditError):
    """积分已过期"""
    def __init__(self, expired_at: datetime):
        self.expired_at = expired_at
        super().__init__(f"积分已于 {expired_at} 过期")


class RedeemCodeNotFoundError(CreditError):
    """兑换码不存在"""
    pass


class RedeemCodeUsedError(CreditError):
    """兑换码已使用"""
    def __init__(self, used_at: datetime, used_by: str):
        self.used_at = used_at
        self.used_by = used_by
        super().__init__(f"兑换码已于 {used_at} 被 {used_by} 使用")


class RedeemCodeExpiredError(CreditError):
    """兑换码已过期"""
    def __init__(self, expired_at: datetime):
        self.expired_at = expired_at
        super().__init__(f"兑换码已于 {expired_at} 过期")


# ============ 邀请系统异常 ============


class InvitationError(Exception):
    """邀请系统异常基类"""
    pass


class InvitationQuotaExceededError(InvitationError):
    """超过邀请码生成数量限制"""
    def __init__(self, max_count: int = 3):
        self.max_count = max_count
        super().__init__(f"每位用户最多生成 {max_count} 个邀请码")


class NewUserCooldownError(InvitationError):
    """新用户冷却期未过"""
    def __init__(self, remaining_hours: int):
        self.remaining_hours = remaining_hours
        super().__init__(f"新用户需等待 {remaining_hours} 小时后才能生成邀请码")


class InvitationCodeInvalidError(InvitationError):
    """邀请码无效"""
    pass


class InvitationCodeExpiredError(InvitationError):
    """邀请码已过期"""
    def __init__(self, expired_at: datetime):
        self.expired_at = expired_at
        super().__init__(f"邀请码已于 {expired_at} 过期")


class InvitationCodeFullError(InvitationError):
    """邀请码使用次数已满"""
    def __init__(self, max_uses: int):
        self.max_uses = max_uses
        super().__init__(f"邀请码已达到最大使用次数 {max_uses}")


class AntiAbuseLimitError(InvitationError):
    """触发防刷限制"""
    def __init__(self, limit_type: str, message: str):
        self.limit_type = limit_type  # "ip" or "device"
        super().__init__(message)
