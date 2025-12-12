"""
邮件验证码服务

用于发送和验证邮箱修改验证码
"""
import random
import string
import logging
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from typing import Optional
from redis.asyncio import Redis
from app.core.config import settings

logger = logging.getLogger(__name__)

# 验证码过期时间（秒）
CODE_EXPIRE_SECONDS = 300  # 5分钟

# 验证码发送间隔（秒）
CODE_SEND_INTERVAL = 60  # 1分钟内不能重复发送

# 验证码最大尝试次数
MAX_VERIFY_ATTEMPTS = 5

# 验证失败锁定时间（秒）
VERIFY_LOCKOUT_SECONDS = 300  # 5分钟


class EmailVerificationService:
    """邮件验证码服务"""

    def __init__(self, redis: Optional[Redis] = None):
        """
        初始化服务

        Args:
            redis: Redis 连接实例
        """
        self.redis = redis

    def _generate_code(self, length: int = 6) -> str:
        """
        生成验证码

        Args:
            length: 验证码长度

        Returns:
            6位数字验证码
        """
        return ''.join(random.choices(string.digits, k=length))

    def _build_cache_key(self, user_id: str, email: str) -> str:
        """
        构建缓存键

        Args:
            user_id: 用户ID
            email: 邮箱地址

        Returns:
            Redis 键名
        """
        return f"email_verify:{user_id}:{email}"

    def _build_rate_limit_key(self, user_id: str) -> str:
        """
        构建发送频率限制键

        Args:
            user_id: 用户ID

        Returns:
            Redis 键名
        """
        return f"email_verify_rate:{user_id}"

    def _build_attempt_key(self, user_id: str, email: str) -> str:
        """
        构建验证尝试次数键

        Args:
            user_id: 用户ID
            email: 邮箱地址

        Returns:
            Redis 键名
        """
        return f"email_verify_attempts:{user_id}:{email}"

    def _build_lockout_key(self, user_id: str) -> str:
        """
        构建锁定键

        Args:
            user_id: 用户ID

        Returns:
            Redis 键名
        """
        return f"email_verify_lockout:{user_id}"

    async def send_verification_code(
        self,
        user_id: str,
        new_email: str,
        current_email: Optional[str] = None
    ) -> str:
        """
        发送验证码到新邮箱

        Args:
            user_id: 用户ID
            new_email: 新邮箱地址
            current_email: 当前邮箱地址

        Returns:
            生成的验证码（用于测试/调试）

        Raises:
            ValueError: 发送频率限制或其他错误
        """
        if not self.redis:
            raise ValueError("Redis 服务不可用，无法发送验证码")

        # 检查发送频率限制
        rate_limit_key = self._build_rate_limit_key(user_id)
        if await self.redis.exists(rate_limit_key):
            ttl = await self.redis.ttl(rate_limit_key)
            raise ValueError(f"请等待 {ttl} 秒后再发送验证码")

        # 生成验证码
        code = self._generate_code()

        # 存储验证码到 Redis
        cache_key = self._build_cache_key(user_id, new_email)
        await self.redis.setex(cache_key, CODE_EXPIRE_SECONDS, code)

        # 设置发送频率限制
        await self.redis.setex(rate_limit_key, CODE_SEND_INTERVAL, "1")

        # 发送邮件（如果配置了 SMTP）
        try:
            await self._send_email(new_email, code)
            logger.info(f"验证码已发送到 {new_email}")
        except Exception as e:
            logger.warning(f"发送邮件失败: {e}，验证码: {code}")
            # 即使邮件发送失败，验证码仍然有效（用于测试）

        return code

    async def verify_code(
        self,
        user_id: str,
        email: str,
        code: str
    ) -> bool:
        """
        验证验证码

        Args:
            user_id: 用户ID
            email: 邮箱地址
            code: 用户输入的验证码

        Returns:
            验证是否成功

        Raises:
            ValueError: 验证次数超限或被锁定
        """
        if not self.redis:
            raise ValueError("Redis 服务不可用")

        # 检查是否被锁定
        lockout_key = self._build_lockout_key(user_id)
        if await self.redis.exists(lockout_key):
            ttl = await self.redis.ttl(lockout_key)
            raise ValueError(f"验证码验证已被锁定，请 {ttl} 秒后重试")

        cache_key = self._build_cache_key(user_id, email)
        attempt_key = self._build_attempt_key(user_id, email)

        stored_code = await self.redis.get(cache_key)

        if not stored_code:
            return False

        if stored_code != code:
            # 增加失败次数
            attempts = await self.redis.incr(attempt_key)
            # 设置尝试次数键的过期时间（与验证码相同）
            await self.redis.expire(attempt_key, CODE_EXPIRE_SECONDS)

            if attempts >= MAX_VERIFY_ATTEMPTS:
                # 达到最大尝试次数，锁定用户
                await self.redis.setex(lockout_key, VERIFY_LOCKOUT_SECONDS, "1")
                # 删除验证码和尝试次数
                await self.redis.delete(cache_key)
                await self.redis.delete(attempt_key)
                raise ValueError(f"验证码错误次数过多，已被锁定 {VERIFY_LOCKOUT_SECONDS // 60} 分钟")

            remaining = MAX_VERIFY_ATTEMPTS - attempts
            raise ValueError(f"验证码错误，还剩 {remaining} 次尝试机会")

        # 验证成功后删除验证码和尝试次数
        await self.redis.delete(cache_key)
        await self.redis.delete(attempt_key)
        return True

    async def _send_email(self, to_email: str, code: str) -> None:
        """
        发送验证码邮件

        Args:
            to_email: 收件人邮箱
            code: 验证码
        """
        # 检查是否配置了 SMTP
        smtp_host = getattr(settings, 'SMTP_HOST', None)
        smtp_port = getattr(settings, 'SMTP_PORT', 587)
        smtp_user = getattr(settings, 'SMTP_USER', None)
        smtp_password = getattr(settings, 'SMTP_PASSWORD', None)

        if not all([smtp_host, smtp_user, smtp_password]):
            logger.warning("SMTP 未配置，跳过邮件发送")
            return

        # 构建邮件内容
        msg = MIMEMultipart('alternative')
        msg['Subject'] = f'【{settings.APP_NAME}】邮箱验证码'
        msg['From'] = smtp_user
        msg['To'] = to_email

        # HTML 内容
        html = f"""
        <div style="max-width: 600px; margin: 0 auto; padding: 20px; font-family: Arial, sans-serif;">
            <h2 style="color: #333;">邮箱验证码</h2>
            <p style="color: #666;">您正在修改邮箱地址，验证码为：</p>
            <div style="background: #f5f5f5; padding: 20px; text-align: center; margin: 20px 0;">
                <span style="font-size: 32px; font-weight: bold; color: #3b82f6; letter-spacing: 8px;">
                    {code}
                </span>
            </div>
            <p style="color: #999; font-size: 14px;">
                验证码有效期为 5 分钟，请勿泄露给他人。
            </p>
            <p style="color: #999; font-size: 14px;">
                如果这不是您本人的操作，请忽略此邮件。
            </p>
            <hr style="border: none; border-top: 1px solid #eee; margin: 20px 0;">
            <p style="color: #999; font-size: 12px;">
                此邮件由系统自动发送，请勿回复。
            </p>
        </div>
        """

        msg.attach(MIMEText(html, 'html', 'utf-8'))

        # 发送邮件
        try:
            with smtplib.SMTP(smtp_host, smtp_port) as server:
                server.starttls()
                server.login(smtp_user, smtp_password)
                server.send_message(msg)
        except Exception as e:
            logger.error(f"SMTP 发送失败: {e}")
            raise


# 全局服务实例
_email_verification_service: Optional[EmailVerificationService] = None


async def get_email_verification_service() -> EmailVerificationService:
    """
    获取邮件验证服务实例

    Returns:
        EmailVerificationService 实例
    """
    global _email_verification_service

    if _email_verification_service is None:
        # 创建 Redis 连接，使用配置文件中的 REDIS_URL
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
            _email_verification_service = EmailVerificationService(redis)
            logger.info("邮件验证服务初始化成功")
        except Exception as e:
            logger.warning(f"Redis 连接失败，邮件验证服务将受限: {e}")
            _email_verification_service = EmailVerificationService(None)

    return _email_verification_service
