"""
Redis客户端配置

功能:
- 缓存评审结果
- Celery消息队列
- 会话存储
"""

from redis import Redis
from typing import Optional
import json
import logging
from datetime import timedelta
from app.core.config import settings

logger = logging.getLogger(__name__)


class RedisClient:
    """Redis客户端封装"""

    def __init__(self):
        """初始化Redis客户端"""
        # 从 REDIS_URL 解析连接参数
        # 格式: redis://localhost:6379/0
        redis_url = settings.REDIS_URL

        try:
            self.client = Redis.from_url(
                redis_url,
                decode_responses=True,
                socket_connect_timeout=5,
                socket_timeout=5
            )
            # 测试连接
            self.client.ping()
            logger.info(f"✅ Redis连接成功: {redis_url}")
        except Exception as e:
            logger.error(f"❌ Redis连接失败: {e}")
            logger.warning("⚠️ Redis不可用,缓存功能将被禁用")
            self.client = None

    def get(self, key: str) -> Optional[str]:
        """获取缓存"""
        if not self.client:
            return None

        try:
            return self.client.get(key)
        except Exception as e:
            logger.error(f"Redis GET错误: {e}")
            return None

    def set(self, key: str, value: str, expire: int = 3600) -> bool:
        """
        设置缓存

        Args:
            key: 缓存键
            value: 缓存值
            expire: 过期时间(秒) - 默认1小时

        Returns:
            是否设置成功
        """
        if not self.client:
            return False

        try:
            self.client.setex(key, expire, value)
            return True
        except Exception as e:
            logger.error(f"Redis SET错误: {e}")
            return False

    def delete(self, key: str) -> bool:
        """删除缓存"""
        if not self.client:
            return False

        try:
            self.client.delete(key)
            return True
        except Exception as e:
            logger.error(f"Redis DELETE错误: {e}")
            return False

    def exists(self, key: str) -> bool:
        """检查key是否存在"""
        if not self.client:
            return False

        try:
            return self.client.exists(key) > 0
        except Exception as e:
            logger.error(f"Redis EXISTS错误: {e}")
            return False

    def get_json(self, key: str) -> Optional[dict]:
        """获取JSON格式缓存"""
        value = self.get(key)
        if value:
            try:
                return json.loads(value)
            except json.JSONDecodeError:
                logger.error(f"JSON解析错误: {key}")
                return None
        return None

    def set_json(self, key: str, value: dict, expire: int = 3600) -> bool:
        """设置JSON格式缓存"""
        try:
            json_str = json.dumps(value, ensure_ascii=False)
            return self.set(key, json_str, expire)
        except Exception as e:
            logger.error(f"JSON序列化错误: {e}")
            return False

    def is_available(self) -> bool:
        """检查Redis是否可用"""
        return self.client is not None


# 全局实例
redis_client = RedisClient()
