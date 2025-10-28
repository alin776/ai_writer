"""
Redis缓存服务

用于缓存AI分析结果,避免重复分析相同内容的章节
"""
import json
import hashlib
import logging
from typing import Optional, Dict, Any, List
from redis.asyncio import Redis
from app.core.config import settings

logger = logging.getLogger(__name__)


class RedisCacheService:
    """Redis缓存服务"""

    def __init__(self):
        """初始化Redis连接"""
        self.redis: Optional[Redis] = None
        self.enabled = True  # 缓存开关

        # 缓存统计
        self.stats = {
            "hits": 0,
            "misses": 0,
            "errors": 0,
            "total_time_saved": 0.0  # 节省的总时间(秒)
        }

    async def connect(self):
        """建立Redis连接"""
        try:
            self.redis = Redis(
                host="localhost",
                port=6379,
                db=0,
                decode_responses=True,  # 自动解码为字符串
                socket_timeout=10,  # 增加到10秒
                socket_connect_timeout=5,
                retry_on_timeout=True,  # 超时自动重试
                health_check_interval=30,  # 健康检查间隔
                max_connections=50  # 连接池大小
            )
            # 测试连接
            await self.redis.ping()
            logger.info("✓ Redis连接成功 (timeout=10s, retry=enabled, pool=50)")
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
            analysis_type: 分析类型 (micro/macro/vector/suggestions/chapters)

        Returns:
            Redis键名
        """
        # 添加版本号v2,方便后续升级
        return f"novel_analysis:v2:{analysis_type}:{content_hash}"

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

        # 重试逻辑
        max_retries = 2
        for attempt in range(max_retries):
            try:
                # 1. 计算内容哈希
                content_hash = self._hash_content(chapter_content)
                cache_key = self._build_cache_key(content_hash, analysis_type)

                # 2. 查询缓存
                cached_data = await self.redis.get(cache_key)

                if cached_data:
                    self.stats["hits"] += 1
                    logger.info(f"✓ 缓存命中: {cache_key[:32]}...")
                    return json.loads(cached_data)

                self.stats["misses"] += 1
                logger.debug(f"✗ 缓存未命中: {cache_key[:32]}...")
                return None

            except Exception as e:
                self.stats["errors"] += 1
                if attempt < max_retries - 1:
                    logger.warning(f"查询缓存失败 (重试 {attempt + 1}/{max_retries}): {e}")
                    continue
                else:
                    logger.warning(f"查询缓存最终失败: {e}")
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

        # 重试逻辑
        max_retries = 2
        for attempt in range(max_retries):
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
                if attempt < max_retries - 1:
                    logger.warning(f"写入缓存失败 (重试 {attempt + 1}/{max_retries}): {e}")
                    continue
                else:
                    logger.warning(f"写入缓存最终失败: {e}")
                    return False

    async def get_cached_vectors(
        self,
        texts: List[str]
    ) -> Optional[List[Optional[List[float]]]]:
        """
        获取缓存的向量化结果 (支持部分命中)

        Args:
            texts: 文本列表

        Returns:
            向量列表,每个元素可能是向量或None(未命中)
            如果完全未命中返回None
        """
        if not self.enabled or not self.redis:
            return None

        try:
            # 为每个文本计算哈希并查询缓存
            embeddings = []
            hit_count = 0
            miss_count = 0

            for text in texts:
                text_hash = self._hash_content(text)
                cache_key = self._build_cache_key(text_hash, "vector")

                cached_data = await self.redis.get(cache_key)

                if cached_data:
                    embeddings.append(json.loads(cached_data))
                    hit_count += 1
                else:
                    embeddings.append(None)  # 占位,表示需要计算
                    miss_count += 1

            # 更新统计
            self.stats["hits"] += hit_count
            self.stats["misses"] += miss_count

            # 如果有部分命中,返回部分结果
            if hit_count > 0:
                logger.info(f"✓ 向量缓存部分命中: {hit_count}/{len(texts)} 个向量")
                return embeddings

            # 完全未命中
            logger.debug(f"✗ 向量缓存完全未命中: {len(texts)} 个向量")
            return None

        except Exception as e:
            self.stats["errors"] += 1
            logger.warning(f"查询向量缓存失败: {e}")
            return None

    async def cache_vectors(
        self,
        texts: List[str],
        embeddings: List[List[float]],
        ttl: int = 60 * 60 * 24 * 7  # 7天
    ) -> bool:
        """
        缓存向量化结果

        Args:
            texts: 文本列表
            embeddings: 对应的向量列表
            ttl: 过期时间(秒)

        Returns:
            是否缓存成功
        """
        if not self.enabled or not self.redis:
            return False

        try:
            cached_count = 0

            for text, embedding in zip(texts, embeddings):
                text_hash = self._hash_content(text)
                cache_key = self._build_cache_key(text_hash, "vector")

                # 序列化向量
                cached_data = json.dumps(embedding, ensure_ascii=False)

                # 写入缓存
                await self.redis.setex(cache_key, ttl, cached_data)
                cached_count += 1

            logger.info(f"✓ 向量缓存成功: {cached_count} 个向量 (TTL: {ttl}秒)")
            return True

        except Exception as e:
            logger.warning(f"缓存向量失败: {e}")
            return False

    async def get_cached_chapters(
        self,
        file_content: str
    ) -> Optional[List[Dict[str, Any]]]:
        """
        获取缓存的章节解析结果

        Args:
            file_content: 文件内容

        Returns:
            章节列表,未命中返回None
        """
        if not self.enabled or not self.redis:
            return None

        try:
            content_hash = self._hash_content(file_content)
            cache_key = self._build_cache_key(content_hash, "chapters")

            cached_data = await self.redis.get(cache_key)

            if cached_data:
                logger.info(f"✓ 章节解析缓存命中: {cache_key[:32]}...")
                return json.loads(cached_data)

            return None

        except Exception as e:
            logger.warning(f"查询章节缓存失败: {e}")
            return None

    async def cache_chapters(
        self,
        file_content: str,
        chapters: List[Dict[str, Any]],
        ttl: int = 60 * 60 * 24 * 7  # 7天
    ) -> bool:
        """
        缓存章节解析结果

        Args:
            file_content: 文件内容
            chapters: 章节列表
            ttl: 过期时间(秒)

        Returns:
            是否缓存成功
        """
        if not self.enabled or not self.redis:
            return False

        try:
            content_hash = self._hash_content(file_content)
            cache_key = self._build_cache_key(content_hash, "chapters")

            # 序列化
            cached_data = json.dumps(chapters, ensure_ascii=False)

            # 写入缓存
            await self.redis.setex(cache_key, ttl, cached_data)

            logger.info(f"✓ 章节解析已缓存: {len(chapters)} 个章节 (TTL: {ttl}秒)")
            return True

        except Exception as e:
            logger.warning(f"缓存章节失败: {e}")
            return False

    def get_local_stats(self) -> Dict[str, Any]:
        """
        获取本地缓存统计信息

        Returns:
            统计信息字典
        """
        total_requests = self.stats["hits"] + self.stats["misses"]
        hit_rate = (self.stats["hits"] / total_requests * 100) if total_requests > 0 else 0

        return {
            "enabled": self.enabled,
            "hits": self.stats["hits"],
            "misses": self.stats["misses"],
            "errors": self.stats["errors"],
            "total_requests": total_requests,
            "hit_rate": f"{hit_rate:.1f}%",
            "time_saved": f"{self.stats['total_time_saved']:.1f}秒"
        }

    def log_cache_stats(self):
        """输出缓存统计到日志"""
        stats = self.get_local_stats()
        if stats["total_requests"] > 0:
            logger.info(f"""
📊 缓存统计:
  - 总请求: {stats['total_requests']}
  - 命中: {stats['hits']}
  - 未命中: {stats['misses']}
  - 错误: {stats['errors']}
  - 命中率: {stats['hit_rate']}
  - 节省时间: {stats['time_saved']}
""")

    def reset_stats(self):
        """重置统计信息"""
        self.stats = {
            "hits": 0,
            "misses": 0,
            "errors": 0,
            "total_time_saved": 0.0
        }
        logger.info("✓ 缓存统计已重置")

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
