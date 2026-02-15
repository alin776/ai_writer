"""
速率限制服务 - 防止Agent操作滥用
"""
from app.core.redis import redis_client
import logging

logger = logging.getLogger(__name__)


class RateLimiter:
    """基于Redis的速率限制器"""

    def __init__(self, key_prefix: str, limit: int, window: int):
        """
        Args:
            key_prefix: Redis key前缀
            limit: 时间窗口内最大请求数
            window: 时间窗口（秒）
        """
        self.key_prefix = key_prefix
        self.limit = limit
        self.window = window

    async def check(self, identifier: str) -> tuple[bool, int]:
        """
        检查是否超过速率限制

        Args:
            identifier: 唯一标识符（如用户ID）

        Returns:
            (is_allowed, remaining) - 是否允许操作，剩余配额
        """
        key = f"{self.key_prefix}:{identifier}"

        try:
            # 使用Redis INCR + EXPIRE实现滑动窗口
            current = await redis_client.incr(key)
            if current == 1:
                await redis_client.expire(key, self.window)

            remaining = max(0, self.limit - current)
            is_allowed = current <= self.limit

            if not is_allowed:
                logger.warning(f"Rate limit exceeded for {identifier}: {current}/{self.limit}")

            return (is_allowed, remaining)

        except Exception as e:
            logger.error(f"Rate limiter error: {e}")
            # 出错时允许操作，避免影响正常使用
            return (True, self.limit)

    async def reset(self, identifier: str) -> bool:
        """重置指定标识符的计数"""
        key = f"{self.key_prefix}:{identifier}"
        try:
            await redis_client.delete(key)
            return True
        except Exception as e:
            logger.error(f"Rate limiter reset error: {e}")
            return False

    async def get_remaining(self, identifier: str) -> int:
        """获取剩余配额"""
        key = f"{self.key_prefix}:{identifier}"
        try:
            current = await redis_client.get(key)
            if current is None:
                return self.limit
            return max(0, self.limit - int(current))
        except Exception as e:
            logger.error(f"Rate limiter get_remaining error: {e}")
            return self.limit


# 预定义的限制器实例

# Agent编辑速率限制器：每分钟最多10次
agent_edit_limiter = RateLimiter(
    key_prefix="agent_edit",
    limit=10,
    window=60
)

# AI生成速率限制器：每分钟最多20次
ai_generation_limiter = RateLimiter(
    key_prefix="ai_generation",
    limit=20,
    window=60
)
