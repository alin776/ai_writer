"""
密码重置服务

用于发送和验证密码重置验证码
"""
import random
import string
import logging
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.utils import formataddr
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


class PasswordResetService:
    """密码重置服务"""

    def __init__(self, redis: Optional[Redis] = None):
        self.redis = redis

    def _generate_code(self, length: int = 6) -> str:
        """生成验证码"""
        return ''.join(random.choices(string.digits, k=length))

    def _build_cache_key(self, email: str) -> str:
        """构建缓存键"""
        return f"password_reset:{email}"

    def _build_rate_limit_key(self, email: str) -> str:
        """构建发送频率限制键"""
        return f"password_reset_rate:{email}"

    def _build_attempt_key(self, email: str) -> str:
        """构建验证尝试次数键"""
        return f"password_reset_attempts:{email}"

    def _build_lockout_key(self, email: str) -> str:
        """构建锁定键"""
        return f"password_reset_lockout:{email}"

    async def send_reset_code(self, email: str) -> str:
        """
        发送密码重置验证码

        Args:
            email: 邮箱地址

        Returns:
            生成的验证码

        Raises:
            ValueError: 发送频率限制
        """
        if not self.redis:
            raise ValueError("Redis 服务不可用，无法发送验证码")

        # 检查发送频率限制
        rate_limit_key = self._build_rate_limit_key(email)
        if await self.redis.exists(rate_limit_key):
            ttl = await self.redis.ttl(rate_limit_key)
            raise ValueError(f"请等待 {ttl} 秒后再发送验证码")

        # 生成验证码
        code = self._generate_code()

        # 存储验证码到 Redis
        cache_key = self._build_cache_key(email)
        await self.redis.setex(cache_key, CODE_EXPIRE_SECONDS, code)

        # 设置发送频率限制
        await self.redis.setex(rate_limit_key, CODE_SEND_INTERVAL, "1")

        # 发送邮件
        try:
            await self._send_email(email, code)
            logger.info(f"密码重置验证码已发送到 {email}")
        except Exception as e:
            logger.warning(f"发送邮件失败: {e}，验证码: {code}")

        return code

    async def verify_code(self, email: str, code: str) -> bool:
        """
        验证验证码

        Args:
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
        lockout_key = self._build_lockout_key(email)
        if await self.redis.exists(lockout_key):
            ttl = await self.redis.ttl(lockout_key)
            raise ValueError(f"验证码验证已被锁定，请 {ttl} 秒后重试")

        cache_key = self._build_cache_key(email)
        attempt_key = self._build_attempt_key(email)

        stored_code = await self.redis.get(cache_key)

        if not stored_code:
            return False

        if stored_code != code:
            # 增加失败次数
            attempts = await self.redis.incr(attempt_key)
            await self.redis.expire(attempt_key, CODE_EXPIRE_SECONDS)

            if attempts >= MAX_VERIFY_ATTEMPTS:
                # 达到最大尝试次数，锁定
                await self.redis.setex(lockout_key, VERIFY_LOCKOUT_SECONDS, "1")
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
        """发送密码重置邮件"""
        smtp_host = getattr(settings, 'SMTP_HOST', None)
        smtp_port = getattr(settings, 'SMTP_PORT', 587)
        smtp_user = getattr(settings, 'SMTP_USER', None)
        smtp_password = getattr(settings, 'SMTP_PASSWORD', None)
        smtp_from_name = getattr(settings, 'SMTP_FROM_NAME', None) or settings.APP_NAME  # 发件人名称

        if not all([smtp_host, smtp_user, smtp_password]):
            logger.warning("SMTP 未配置，跳过邮件发送")
            return

        msg = MIMEMultipart('alternative')
        msg['Subject'] = f'【{settings.APP_NAME}】密码重置验证码'
        # 使用 formataddr 格式化带名称的发件人
        msg['From'] = formataddr((smtp_from_name, smtp_user))
        msg['To'] = to_email

        html = f"""
        <div style="max-width: 600px; margin: 0 auto; padding: 20px; font-family: Arial, sans-serif;">
            <h2 style="color: #333;">密码重置验证码</h2>
            <p style="color: #666;">您正在重置密码，验证码为：</p>
            <div style="background: #f5f5f5; padding: 20px; text-align: center; margin: 20px 0;">
                <span style="font-size: 32px; font-weight: bold; color: #e53e3e; letter-spacing: 8px;">
                    {code}
                </span>
            </div>
            <p style="color: #999; font-size: 14px;">
                验证码有效期为 5 分钟，请勿泄露给他人。
            </p>
            <p style="color: #999; font-size: 14px;">
                如果这不是您本人的操作，请忽略此邮件并确保您的账户安全。
            </p>
            <hr style="border: none; border-top: 1px solid #eee; margin: 20px 0;">
            <p style="color: #999; font-size: 12px;">
                此邮件由系统自动发送，请勿回复。
            </p>
        </div>
        """

        msg.attach(MIMEText(html, 'html', 'utf-8'))

        try:
            # 根据端口选择连接方式：465用SSL，其他用STARTTLS
            if smtp_port == 465:
                server = smtplib.SMTP_SSL(smtp_host, smtp_port)
                try:
                    server.login(smtp_user, smtp_password)
                    server.send_message(msg)
                finally:
                    server.quit()
            else:
                with smtplib.SMTP(smtp_host, smtp_port) as server:
                    server.starttls()
                    server.login(smtp_user, smtp_password)
                    server.send_message(msg)
        except Exception as e:
            logger.error(f"SMTP 发送失败: {e}")
            raise


# 全局服务实例
_password_reset_service: Optional[PasswordResetService] = None


async def get_password_reset_service() -> PasswordResetService:
    """获取密码重置服务实例"""
    global _password_reset_service

    if _password_reset_service is None:
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
            _password_reset_service = PasswordResetService(redis)
            logger.info("密码重置服务初始化成功")
        except Exception as e:
            logger.warning(f"Redis 连接失败，密码重置服务将受限: {e}")
            _password_reset_service = PasswordResetService(None)

    return _password_reset_service
