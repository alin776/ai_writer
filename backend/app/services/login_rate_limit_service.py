"""
登录限流服务

防止暴力破解，限制登录失败次数
"""
import logging
from typing import Optional, Tuple
from redis.asyncio import Redis
from app.core.config import settings

logger = logging.getLogger(__name__)

# 配置常量
MAX_LOGIN_ATTEMPTS = 5  # 最大失败次数
LOCKOUT_SECONDS = 900  # 锁定时间（15分钟）
ATTEMPT_WINDOW_SECONDS = 600  # 失败计数窗口（10分钟）


class LoginRateLimitService:
    """登录限流服务"""

    def __init__(self, redis: Optional[Redis] = None):
        self.redis = redis

    def _build_attempt_key(self, identifier: str) -> str:
        """构建失败次数键（基于用户名或IP）"""
        return f"login_attempts:{identifier}"

    def _build_lockout_key(self, identifier: str) -> str:
        """构建锁定键"""
        return f"login_lockout:{identifier}"

    async def check_rate_limit(self, username: str, ip_address: str) -> Tuple[bool, str]:
        """
        检查是否被限流

        Args:
            username: 用户名
            ip_address: IP地址

        Returns:
            (是否允许登录, 错误消息)
        """
        if not self.redis:
            return True, ""

        # 检查用户名锁定
        user_lockout_key = self._build_lockout_key(username)
        if await self.redis.exists(user_lockout_key):
            ttl = await self.redis.ttl(user_lockout_key)
            minutes = ttl // 60 + 1
            return False, f"账户已被锁定，请 {minutes} 分钟后重试"

        # 检查IP锁定
        ip_lockout_key = self._build_lockout_key(ip_address)
        if await self.redis.exists(ip_lockout_key):
            ttl = await self.redis.ttl(ip_lockout_key)
            minutes = ttl // 60 + 1
            return False, f"当前IP已被锁定，请 {minutes} 分钟后重试"

        return True, ""

    async def record_failed_attempt(self, username: str, ip_address: str) -> Tuple[int, bool]:
        """
        记录登录失败

        Args:
            username: 用户名
            ip_address: IP地址

        Returns:
            (剩余尝试次数, 是否被锁定)
        """
        if not self.redis:
            return MAX_LOGIN_ATTEMPTS, False

        # 记录用户名失败次数
        user_attempt_key = self._build_attempt_key(username)
        user_attempts = await self.redis.incr(user_attempt_key)
        await self.redis.expire(user_attempt_key, ATTEMPT_WINDOW_SECONDS)

        # 记录IP失败次数
        ip_attempt_key = self._build_attempt_key(ip_address)
        ip_attempts = await self.redis.incr(ip_attempt_key)
        await self.redis.expire(ip_attempt_key, ATTEMPT_WINDOW_SECONDS)

        # 检查是否需要锁定
        max_attempts = max(user_attempts, ip_attempts)
        if max_attempts >= MAX_LOGIN_ATTEMPTS:
            # 锁定用户名和IP
            user_lockout_key = self._build_lockout_key(username)
            ip_lockout_key = self._build_lockout_key(ip_address)
            await self.redis.setex(user_lockout_key, LOCKOUT_SECONDS, "1")
            await self.redis.setex(ip_lockout_key, LOCKOUT_SECONDS, "1")
            # 清除失败计数
            await self.redis.delete(user_attempt_key)
            await self.redis.delete(ip_attempt_key)
            logger.warning(f"用户 {username} (IP: {ip_address}) 登录失败次数过多，已锁定")
            return 0, True

        remaining = MAX_LOGIN_ATTEMPTS - max_attempts
        return remaining, False

    async def clear_failed_attempts(self, username: str, ip_address: str):
        """
        登录成功后清除失败记录

        Args:
            username: 用户名
            ip_address: IP地址
        """
        if not self.redis:
            return

        user_attempt_key = self._build_attempt_key(username)
        ip_attempt_key = self._build_attempt_key(ip_address)
        await self.redis.delete(user_attempt_key)
        await self.redis.delete(ip_attempt_key)


# 全局服务实例
_login_rate_limit_service: Optional[LoginRateLimitService] = None


async def get_login_rate_limit_service() -> LoginRateLimitService:
    """获取登录限流服务实例"""
    global _login_rate_limit_service

    if _login_rate_limit_service is None:
        try:
            from urllib.parse import urlparse

            redis_url = settings.REDIS_URL
            parsed = urlparse(redis_url)

            redis = Redis(
                host=parsed.hostname or "localhost",
                port=parsed.port or 6379,
                db=int(parsed.path.lstrip('/') or 0) if parsed.path else 0,
                password=parsed.password,
                decode_responses=True,
                socket_timeout=5,
                socket_connect_timeout=3,
            )
            await redis.ping()
            _login_rate_limit_service = LoginRateLimitService(redis)
            logger.info("登录限流服务初始化成功")
        except Exception as e:
            logger.warning(f"Redis 连接失败，登录限流服务将不可用: {e}")
            _login_rate_limit_service = LoginRateLimitService(None)

    return _login_rate_limit_service
