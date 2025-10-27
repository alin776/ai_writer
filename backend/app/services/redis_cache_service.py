"""
Redis缓存服务

用于缓存AI分析结果,避免重复分析相同内容的章节
"""
import json
import hashlib
import logging
from typing import Optional, Dict, Any
from redis.asyncio import Redis
from app.core.config import settings

logger = logging.getLogger(__name__)


class RedisCacheService:
    """Redis缓存服务"""

    def __init__(self):
        """初始化Redis连接"""
        self.redis: Optional[Redis] = None
        self.enabled = True  # 缓存开关

    async def connect(self):
        """建立Redis连接"""
        try:
            self.redis = Redis(
                host="localhost",
                port=6379,
                db=0,
                decode_responses=True,  # 自动解码为字符串
                socket_timeout=5,
                socket_connect_timeout=5
            )
            # 测试连接
            await self.redis.ping()
            logger.info("✓ Redis连接成功")
        except Exception as e:
            logger.warning(f"⚠️  Redis连接失败,缓存功能将禁用: {e}")
            self.enabled = False
            self.redis = None

    async def close(self):
        """关闭Redis连接"""
        if self.redis:
            await self.redis.close()
            logger.info("Redis连接已关闭")

    def _hash_content(self, content: str) -> str:
        """
        计算内容哈希

        Args:
            content: 章节内容

        Returns:
            MD5哈希字符串
        """
        return hashlib.md5(content.encode('utf-8')).hexdigest()

    def _build_cache_key(self, content_hash: str, analysis_type: str = "micro") -> str:
        """
        构建缓存键

        Args:
            content_hash: 内容哈希
            analysis_type: 分析类型 (micro/macro)

        Returns:
            Redis键名
        """
        return f"novel_analysis:{analysis_type}:{content_hash}"

    async def get_cached_analysis(
        self,
        chapter_content: str,
        analysis_type: str = "micro"
    ) -> Optional[Dict[str, Any]]:
        """
        获取缓存的分析结果

        Args:
            chapter_content: 章节内容
            analysis_type: 分析类型

        Returns:
            缓存的分析结果,不存在则返回None
        """
        if not self.enabled or not self.redis:
            return None

        try:
            # 1. 计算内容哈希
            content_hash = self._hash_content(chapter_content)
            cache_key = self._build_cache_key(content_hash, analysis_type)

            # 2. 查询缓存
            cached_data = await self.redis.get(cache_key)

            if cached_data:
                logger.info(f"✓ 缓存命中: {cache_key[:32]}...")
                return json.loads(cached_data)

            logger.debug(f"✗ 缓存未命中: {cache_key[:32]}...")
            return None

        except Exception as e:
            logger.warning(f"查询缓存失败: {e}")
            return None

    async def cache_analysis_result(
        self,
        chapter_content: str,
        result: Dict[str, Any],
        analysis_type: str = "micro",
        ttl: int = 60 * 60 * 24 * 7  # 默认7天
    ) -> bool:
        """
        缓存分析结果

        Args:
            chapter_content: 章节内容
            result: 分析结果
            analysis_type: 分析类型
            ttl: 过期时间(秒)

        Returns:
            是否缓存成功
        """
        if not self.enabled or not self.redis:
            return False

        try:
            # 1. 计算内容哈希
            content_hash = self._hash_content(chapter_content)
            cache_key = self._build_cache_key(content_hash, analysis_type)

            # 2. 序列化结果
            cached_data = json.dumps(result, ensure_ascii=False)

            # 3. 写入缓存
            await self.redis.setex(cache_key, ttl, cached_data)

            logger.info(f"✓ 结果已缓存: {cache_key[:32]}... (TTL: {ttl}秒)")
            return True

        except Exception as e:
            logger.warning(f"写入缓存失败: {e}")
            return False

    async def get_cache_stats(self) -> Dict[str, Any]:
        """
        获取缓存统计信息

        Returns:
            统计信息字典
        """
        if not self.enabled or not self.redis:
            return {
                "enabled": False,
                "error": "Redis未连接"
            }

        try:
            info = await self.redis.info()
            return {
                "enabled": True,
                "connected_clients": info.get("connected_clients", 0),
                "used_memory_human": info.get("used_memory_human", "0B"),
                "total_keys": await self.redis.dbsize(),
            }
        except Exception as e:
            logger.error(f"获取缓存统计失败: {e}")
            return {
                "enabled": False,
                "error": str(e)
            }

    async def clear_cache(self, pattern: str = "novel_analysis:*") -> int:
        """
        清理缓存

        Args:
            pattern: 匹配模式

        Returns:
            清理的键数量
        """
        if not self.enabled or not self.redis:
            return 0

        try:
            keys = []
            async for key in self.redis.scan_iter(match=pattern):
                keys.append(key)

            if keys:
                deleted = await self.redis.delete(*keys)
                logger.info(f"✓ 清理缓存: {deleted} 个键")
                return deleted

            logger.info("✓ 没有匹配的缓存键需要清理")
            return 0

        except Exception as e:
            logger.error(f"清理缓存失败: {e}")
            return 0


# 全局缓存实例
_cache_service: Optional[RedisCacheService] = None


async def get_cache_service() -> RedisCacheService:
    """
    获取缓存服务实例(单例)

    Returns:
        RedisCacheService实例
    """
    global _cache_service

    if _cache_service is None:
        _cache_service = RedisCacheService()
        await _cache_service.connect()

    return _cache_service
