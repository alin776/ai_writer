"""
Redis 连接管理模块

功能：
- 异步 Redis 连接池管理
- 缓存操作封装
- 自动序列化/反序列化
"""
import json
import logging
from typing import Any, Optional, Union
from redis.asyncio import Redis, ConnectionPool
from app.core.config import settings

logger = logging.getLogger(__name__)


class RedisClient:
    """Redis 客户端单例"""
    
    _instance: Optional[Redis] = None
    _pool: Optional[ConnectionPool] = None
    
    @classmethod
    async def get_instance(cls) -> Redis:
        """获取 Redis 实例（单例模式）"""
        if cls._instance is None:
            await cls.init()
        return cls._instance
    
    @classmethod
    async def init(cls) -> None:
        """初始化 Redis 连接池"""
        if cls._instance is not None:
            logger.warning("Redis already initialized")
            return
        
        try:
            # 创建连接池
            cls._pool = ConnectionPool.from_url(
                settings.REDIS_URL,
                encoding="utf-8",
                decode_responses=True,  # 自动解码为字符串
                max_connections=10,
            )
            
            # 创建 Redis 实例
            cls._instance = Redis(connection_pool=cls._pool)
            
            # 测试连接
            await cls._instance.ping()
            logger.info(f"✅ Redis connected: {settings.REDIS_URL}")
            
        except Exception as e:
            logger.error(f"❌ Redis connection failed: {e}")
            raise
    
    @classmethod
    async def close(cls) -> None:
        """关闭 Redis 连接"""
        if cls._instance:
            await cls._instance.close()
            cls._instance = None
        
        if cls._pool:
            await cls._pool.disconnect()
            cls._pool = None
        
        logger.info("Redis connection closed")
    
    @classmethod
    async def get(cls, key: str) -> Optional[Any]:
        """
        获取缓存
        
        Args:
            key: 缓存键
            
        Returns:
            缓存值（自动反序列化 JSON）
        """
        try:
            redis = await cls.get_instance()
            value = await redis.get(key)
            
            if value is None:
                return None
            
            # 尝试解析 JSON
            try:
                return json.loads(value)
            except (json.JSONDecodeError, TypeError):
                return value
                
        except Exception as e:
            logger.error(f"Redis GET error [{key}]: {e}")
            return None
    
    @classmethod
    async def set(
        cls,
        key: str,
        value: Any,
        expire: Optional[int] = None
    ) -> bool:
        """
        设置缓存
        
        Args:
            key: 缓存键
            value: 缓存值（自动序列化为 JSON）
            expire: 过期时间（秒）
            
        Returns:
            是否设置成功
        """
        try:
            redis = await cls.get_instance()
            
            # 序列化值
            if isinstance(value, (dict, list)):
                serialized_value = json.dumps(value, ensure_ascii=False, default=str)
            else:
                serialized_value = str(value)
            
            # 设置缓存
            if expire:
                await redis.setex(key, expire, serialized_value)
            else:
                await redis.set(key, serialized_value)
            
            return True
            
        except Exception as e:
            logger.error(f"Redis SET error [{key}]: {e}")
            return False
    
    @classmethod
    async def delete(cls, key: str) -> bool:
        """
        删除缓存
        
        Args:
            key: 缓存键
            
        Returns:
            是否删除成功
        """
        try:
            redis = await cls.get_instance()
            await redis.delete(key)
            return True
            
        except Exception as e:
            logger.error(f"Redis DELETE error [{key}]: {e}")
            return False
    
    @classmethod
    async def delete_pattern(cls, pattern: str) -> int:
        """
        删除匹配模式的所有键
        
        Args:
            pattern: 键模式（支持通配符 *）
            
        Returns:
            删除的键数量
        """
        try:
            redis = await cls.get_instance()
            keys = await redis.keys(pattern)
            
            if keys:
                deleted = await redis.delete(*keys)
                logger.info(f"Deleted {deleted} keys matching pattern: {pattern}")
                return deleted
            
            return 0
            
        except Exception as e:
            logger.error(f"Redis DELETE PATTERN error [{pattern}]: {e}")
            return 0
    
    @classmethod
    async def exists(cls, key: str) -> bool:
        """
        检查键是否存在
        
        Args:
            key: 缓存键
            
        Returns:
            是否存在
        """
        try:
            redis = await cls.get_instance()
            return await redis.exists(key) > 0
            
        except Exception as e:
            logger.error(f"Redis EXISTS error [{key}]: {e}")
            return False
    
    @classmethod
    async def expire(cls, key: str, seconds: int) -> bool:
        """
        设置键的过期时间

        Args:
            key: 缓存键
            seconds: 过期时间（秒）

        Returns:
            是否设置成功
        """
        try:
            redis = await cls.get_instance()
            return await redis.expire(key, seconds)

        except Exception as e:
            logger.error(f"Redis EXPIRE error [{key}]: {e}")
            return False

    @classmethod
    async def incr(cls, key: str) -> int:
        """
        对键的值进行原子递增

        Args:
            key: 缓存键

        Returns:
            递增后的值
        """
        try:
            redis = await cls.get_instance()
            return await redis.incr(key)

        except Exception as e:
            logger.error(f"Redis INCR error [{key}]: {e}")
            raise


# 全局 Redis 实例（便于使用）
redis_client = RedisClient
get_redis = RedisClient.get_instance


# 缓存键生成器
class CacheKey:
    """缓存键命名规范"""
    
    # 作品相关
    WORK_LIST = "works:list"
    WORK_DETAIL = "works:detail:{work_id}"
    WORK_CHAPTERS = "works:{work_id}:chapters"
    
    # 章节相关
    CHAPTER_DETAIL = "chapters:detail:{chapter_id}"
    CHAPTER_SUMMARY = "chapters:{chapter_id}:summary"
    
    # 世界观相关
    WORLDVIEW_DATA = "worldview:{work_id}:data"
    CHARACTERS = "worldview:{work_id}:characters"
    LOCATIONS = "worldview:{work_id}:locations"
    SETTINGS = "worldview:{work_id}:settings"
    GUIDELINES = "worldview:{work_id}:guidelines"
    AI_GUIDELINES = "worldview:{work_id}:ai_guidelines"
    GLOSSARY = "worldview:{work_id}:glossary"
    
    # 分析相关
    ANALYSIS_STATUS = "analysis:{work_id}:status"
    ANALYSIS_RESULT = "analysis:{work_id}:result"
    
    # 管理后台相关
    ADMIN_STATISTICS = "admin:statistics"
    ADMIN_USERS = "admin:users:list"
    ADMIN_AI_MODELS = "admin:ai_models:list"
    ADMIN_COSTS = "admin:costs:metrics"
    
    @staticmethod
    def work_detail(work_id: str) -> str:
        return f"works:detail:{work_id}"
    
    @staticmethod
    def work_chapters(work_id: str) -> str:
        return f"works:{work_id}:chapters"
    
    @staticmethod
    def chapter_detail(chapter_id: str) -> str:
        return f"chapters:detail:{chapter_id}"
    
    @staticmethod
    def worldview_data(work_id: str) -> str:
        return f"worldview:{work_id}:data"
    
    @staticmethod
    def invalidate_work(work_id: str) -> list:
        """获取作品相关的所有缓存键模式"""
        return [
            f"works:detail:{work_id}",
            f"works:{work_id}:*",
            f"worldview:{work_id}:*",
            f"analysis:{work_id}:*",
        ]


# 缓存过期时间配置（秒）
class CacheExpire:
    """缓存过期时间配置"""
    
    # 静态数据（变化不频繁）
    STATIC = 10 * 60  # 10分钟
    
    # 动态数据（可能被修改）
    DYNAMIC = 5 * 60  # 5分钟
    
    # 实时数据（频繁变化）
    REALTIME = 30  # 30秒
    
    # 长期缓存
    LONG_TERM = 60 * 60  # 1小时
