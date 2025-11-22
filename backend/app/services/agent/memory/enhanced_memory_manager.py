"""
增强的记忆管理器 (Enhanced Memory Manager)

实现三层记忆模型和智能遗忘机制的核心管理类。

架构:
    - 短期记忆: Redis List, 最近10条, TTL 1小时
    - 中期记忆: Redis Sorted Set, 最近100条, TTL 24小时
    - 长期记忆: Redis String, 压缩摘要, 永久保存

核心功能:
    1. 记忆添加与分层存储
    2. 智能遗忘策略应用
    3. 多种检索方式（最近、相关、关键词）
    4. 状态快照与恢复
"""

import uuid
import json
import logging
from datetime import datetime, timezone
from typing import List, Optional, Dict, Any
import redis
from redis import Redis

from .types import MemoryItem, MemoryLayer, MemorySnapshot, MemoryStats
from .memory_strategy import SmartForgetStrategy
from .metrics import get_metrics  # ✅ P1-5修复: 集成监控
from .long_term_store import get_long_term_store  # ✅ P1-6修复: 长期记忆持久化
from app.core.config import settings
from ..utils import robust_retry, safe_execute_async, global_error_handler, ErrorCategory, cache_result, performance_optimizer
from ..utils.redis_fallback import get_fallback_store, FallbackReason
import time  # ✅ P1-5修复: 用于性能测量

logger = logging.getLogger(__name__)

# 内存缓存将在需要时创建
_memory_index_cache = None


class EnhancedMemoryManager:
    """
    增强的记忆管理器

    管理用户的三层记忆（短期/中期/长期），支持智能遗忘和快照恢复。
    """

    # Redis TTL 常量
    SHORT_TERM_TTL = 86400  # 24小时（修复P0-2：原1小时太短导致上下文丢失）
    MEDIUM_TERM_TTL = 86400 * 3  # 3天（修复P1-1：基础TTL，重要记忆会更长）
    SNAPSHOT_TTL = 86400 * 7  # 7天

    def __init__(self, redis_client: Redis):
        """
        初始化记忆管理器

        Args:
            redis_client: Redis客户端实例
        """
        self.redis = redis_client
        self.strategy = SmartForgetStrategy(
            forget_threshold=settings.MEMORY_FORGET_THRESHOLD
        )

        # 从配置读取容量参数
        self.short_term_size = settings.MEMORY_SHORT_TERM_SIZE
        self.medium_term_size = settings.MEMORY_MEDIUM_TERM_SIZE
        self.forget_threshold = settings.MEMORY_FORGET_THRESHOLD

        # ✅ P1-5修复: 初始化监控
        self.metrics = get_metrics()

        # ✅ P1-6修复: 初始化长期记忆持久化存储
        self.long_term_store = get_long_term_store(
            base_dir=getattr(settings, 'LONG_TERM_MEMORY_DIR', './data/long_term_memory'),
            max_size_kb=getattr(settings, 'LONG_TERM_MAX_SIZE_KB', 50),
            compression_enabled=getattr(settings, 'LONG_TERM_COMPRESSION', True)
        )

        logger.info(
            f"EnhancedMemoryManager initialized: "
            f"short={self.short_term_size}, "
            f"medium={self.medium_term_size}, "
            f"threshold={self.forget_threshold}, "
            f"long_term_backup=enabled"
        )

    # ==================== 记忆添加 ====================

    async def add_memory(
        self,
        user_id: str,
        conversation_id: str,
        role: str,
        content: str,
        importance: float = 0.5,
        metadata: Dict[str, Any] = None
    ) -> MemoryItem:
        """
        添加新记忆（自动分层存储）

        流程:
            1. 创建 MemoryItem 对象
            2. 添加到短期记忆（Redis List）
            3. 触发智能遗忘策略

        Args:
            user_id: 用户ID
            conversation_id: 会话ID
            role: 角色 (user/assistant/system/tool)
            content: 记忆内容
            importance: 初始重要度 (0.0-1.0)
            metadata: 扩展元数据

        Returns:
            MemoryItem: 创建的记忆条目

        示例:
            >>> manager.add_memory(
            ...     user_id="user_123",
            ...     conversation_id="conv_456",
            ...     role="user",
            ...     content="我想写一部玄幻小说",
            ...     importance=0.8
            ... )
        """
        # 参数验证
        if not user_id or not user_id.strip():
            raise ValueError("user_id cannot be empty")
        if not content or not content.strip():
            raise ValueError("content cannot be empty")
        if len(content) > 10000:
            raise ValueError("content too long (max 10000 chars)")

        logger.debug(f"Adding memory for user={user_id}, conv={conversation_id}")

        # ✅ P1-5修复: 开始性能监控
        start_time = time.time()

        try:
            # 1. 创建记忆条目（使用 aware datetime）
            now = datetime.now(timezone.utc)
            memory = MemoryItem(
                id=self._generate_memory_id(),
                user_id=user_id,
                conversation_id=conversation_id,
                role=role,
                content=content,
                timestamp=now,
                last_access=now,
                importance=importance,
                metadata=metadata or {}
            )

            # ✅ P1-5修复: 记录重要度分布
            self.metrics.record_importance(importance)

            # 2. 添加到短期记忆（使用重试机制）
            await self._safe_add_to_short_term(user_id, memory)
            logger.info(f"Memory {memory.id} added to short-term for user {user_id}")

            # ✅ P1-5修复: 记录写入性能
            latency_ms = (time.time() - start_time) * 1000
            self.metrics.record_write(latency_ms)

            # 3. 更新缓存索引
            self._update_cache_index(user_id, memory)

            # 4. 应用智能遗忘策略（失败不影响主流程）
            await safe_execute_async(
                self.apply_forgetting,
                user_id,
                conversation_id,
                context={"user_id": user_id, "action": "apply_forgetting"},
                fallback_result=None
            )

            return memory

        except redis.RedisError as e:
            # ✅ P1-5修复: 记录Redis错误和降级事件
            self.metrics.record_redis_error()
            self.metrics.record_fallback()

            # 使用统一的降级策略（修复P0-8）
            error_info = global_error_handler.classify_error(
                e,
                {"user_id": user_id, "conversation_id": conversation_id, "action": "add_memory"}
            )
            global_error_handler.handle_error(error_info)

            # 进入降级模式并存储到降级存储
            fallback_store = get_fallback_store()
            reason = FallbackReason.CONNECTION_ERROR if "connection" in str(e).lower() else FallbackReason.UNKNOWN
            fallback_store.enter_fallback_mode(reason)

            # 存储到降级存储
            key = f"memory:{user_id}:short_term"
            fallback_store.lpush(key, memory.model_dump_json(), ttl=self.SHORT_TERM_TTL)

            logger.warning(f"[EnhancedMemoryManager] Redis故障，使用降级存储: user={user_id}, reason={reason.value}")
            return memory

        except Exception as e:
            # 其他异常直接抛出
            error_info = global_error_handler.classify_error(
                e,
                {"user_id": user_id, "conversation_id": conversation_id, "action": "add_memory"}
            )
            global_error_handler.handle_error(error_info)
            raise

    # ==================== 记忆检索 ====================

    def get_recent_memories(
        self,
        user_id: str,
        limit: int = 10,
        layer: MemoryLayer = MemoryLayer.SHORT_TERM
    ) -> List[MemoryItem]:
        """
        获取最近的记忆

        Args:
            user_id: 用户ID
            limit: 返回数量限制
            layer: 记忆层级

        Returns:
            List[MemoryItem]: 记忆列表（按时间倒序）

        示例:
            >>> # 获取最近5条短期记忆
            >>> memories = manager.get_recent_memories("user_123", limit=5)
        """
        if layer == MemoryLayer.SHORT_TERM:
            return self._get_short_term_memories(user_id, limit)
        elif layer == MemoryLayer.MEDIUM_TERM:
            return self._get_medium_term_memories(user_id, limit)
        elif layer == MemoryLayer.LONG_TERM:
            # 长期记忆返回摘要文本（包装为MemoryItem）
            summary = self._get_long_term_summary(user_id)
            if summary:
                now = datetime.now(timezone.utc)
                return [MemoryItem(
                    id="long_term_summary",
                    user_id=user_id,
                    conversation_id="",
                    role="system",
                    content=summary,
                    timestamp=now,
                    last_access=now
                )]
            return []
        else:
            return []

    def search_memories(
        self,
        user_id: str,
        keywords: List[str],
        limit: int = 10
    ) -> List[MemoryItem]:
        """
        关键词搜索记忆

        Args:
            user_id: 用户ID
            keywords: 关键词列表
            limit: 返回数量

        Returns:
            List[MemoryItem]: 匹配的记忆列表

        示例:
            >>> memories = manager.search_memories(
            ...     user_id="user_123",
            ...     keywords=["玄幻", "主角"],
            ...     limit=5
            ... )
        """
        # 从短期和中期记忆搜索
        all_memories = []
        all_memories.extend(
            self._get_short_term_memories(user_id, self.short_term_size)
        )
        all_memories.extend(
            self._get_medium_term_memories(user_id, self.medium_term_size)
        )

        # 关键词匹配
        matched = []
        for memory in all_memories:
            content_lower = memory.content.lower()
            if any(keyword.lower() in content_lower for keyword in keywords):
                # 更新访问次数
                memory.access_count += 1
                memory.last_access = datetime.now(timezone.utc)
                matched.append(memory)

        return matched[:limit]

    def get_relevant_memories(
        self,
        user_id: str,
        query: str,
        top_k: int = 5,
        layer: MemoryLayer = None
    ) -> List[MemoryItem]:
        """
        获取相关记忆（语义相似度检索）- 优化版（修复P0-5）

        使用jieba分词提取关键词，并支持同义词扩展

        Args:
            user_id: 用户ID
            query: 查询文本
            top_k: 返回数量
            layer: 记忆层级（None表示所有层级）

        Returns:
            List[MemoryItem]: 相关记忆列表
        """
        # ✅ P1-5修复: 开始检索性能监控
        start_time = time.time()

        try:
            # 使用改进的关键词提取
            keywords = self._extract_keywords(query)

            if not keywords:
                # 如果提取不到关键词，返回最近的记忆
                results = self.get_recent_memories(user_id, limit=top_k)
            else:
                results = self.search_memories(user_id, keywords, limit=top_k)

            # ✅ P1-5修复: 记录检索性能
            latency_ms = (time.time() - start_time) * 1000
            self.metrics.record_retrieval(latency_ms, success=True)

            return results

        except Exception as e:
            # ✅ P1-5修复: 记录失败的检索
            latency_ms = (time.time() - start_time) * 1000
            self.metrics.record_retrieval(latency_ms, success=False)
            raise

    def _extract_keywords(self, text: str) -> List[str]:
        """
        从文本中提取关键词（修复P0-5：改进关键词提取）

        使用jieba分词进行中文分词，过滤停用词

        Args:
            text: 输入文本

        Returns:
            关键词列表
        """
        try:
            import jieba
            import jieba.analyse

            # 使用TF-IDF提取关键词
            keywords = jieba.analyse.extract_tags(text, topK=10, withWeight=False)

            # 如果TF-IDF没有结果，退回普通分词
            if not keywords:
                # 停用词列表
                stopwords = {
                    '的', '了', '是', '在', '我', '有', '和', '就', '不', '人', '都', '一',
                    '一个', '上', '也', '很', '到', '说', '要', '去', '你', '会', '着',
                    '没有', '看', '好', '自己', '这', '那', '什么', '怎么', '吗', '呢',
                    '啊', '吧', '把', '被', '给', '让', '从', '向', '对', '与', '能',
                    '可以', '这个', '那个', '帮我', '请', '想', '能不能', '可不可以'
                }

                # 分词
                words = jieba.cut(text)
                # 过滤停用词和短词
                keywords = [w for w in words if w not in stopwords and len(w) >= 2][:10]

            # 添加同义词扩展
            expanded = self._expand_synonyms(keywords)

            return list(set(keywords + expanded))[:15]  # 最多15个关键词

        except ImportError:
            # jieba未安装，使用简单的正则分词
            import re
            # 匹配中文词语和英文单词
            pattern = r'[\u4e00-\u9fff]{2,}|[a-zA-Z]{3,}'
            words = re.findall(pattern, text)
            return words[:10]
        except Exception as e:
            logger.warning(f"Keyword extraction failed: {e}, falling back to simple split")
            return text.split()[:5]

    def _expand_synonyms(self, keywords: List[str]) -> List[str]:
        """
        同义词扩展（修复P0-5：提高召回率）

        Args:
            keywords: 原始关键词列表

        Returns:
            扩展后的同义词列表
        """
        # 写作相关的同义词映射
        synonym_map = {
            # 角色相关
            '主角': ['主人公', '男主', '女主', '主人翁'],
            '主人公': ['主角', '男主', '女主'],
            '配角': ['次要角色', '配角人物'],
            '角色': ['人物', '角色设定'],
            '人物': ['角色', '人物设定'],
            # 创作相关
            '续写': ['继续写', '继续创作', '往下写'],
            '继续写': ['续写', '继续创作'],
            '改写': ['重写', '修改', '改动'],
            '大纲': ['提纲', '故事大纲', '情节大纲'],
            '设定': ['设定集', '背景设定', '世界设定'],
            # 情节相关
            '情节': ['剧情', '故事情节'],
            '剧情': ['情节', '故事'],
            '背景': ['世界背景', '故事背景'],
            '世界观': ['世界设定', '背景设定'],
            # 武器装备
            '武器': ['装备', '兵器', '武具'],
            '装备': ['武器', '道具'],
        }

        expanded = []
        for kw in keywords:
            if kw in synonym_map:
                expanded.extend(synonym_map[kw])

        return expanded

    # ==================== 智能遗忘 ====================

    def apply_forgetting(
        self,
        user_id: str,
        conversation_id: str
    ):
        """
        应用智能遗忘策略 - 使用分布式锁确保线程安全（修复P0-6）

        流程:
            1. 从短期记忆移动旧记忆到中期记忆
            2. 获取中期记忆并计算重要度
            3. 筛选需要遗忘的记忆
            4. 更新中期记忆（保留重要的）
            5. 压缩遗忘的记忆为摘要，存入长期记忆

        Args:
            user_id: 用户ID
            conversation_id: 会话ID
        """
        # ✅ P1-5修复: 开始遗忘性能监控
        start_time = time.time()

        # 使用Redis分布式锁确保同一用户只有一个进程执行遗忘（修复P0-6）
        lock_key = f"lock:forget:{user_id}"
        lock = self.redis.lock(lock_key, timeout=30, blocking_timeout=5)

        if not lock.acquire(blocking=False):
            # 无法获取锁，说明有其他进程正在执行，跳过本次
            logger.debug(f"Skipping apply_forgetting for user {user_id}, lock held by another process")
            return

        try:
            # 1. 检查短期记忆是否溢出，溢出的移到中期
            short_memories = self._get_short_term_memories(
                user_id,
                self.short_term_size + 10  # 多取10条检查
            )

            if len(short_memories) > self.short_term_size:
                # 将超出的记忆移到中期
                overflow = short_memories[self.short_term_size:]
                for memory in overflow:
                    self._add_to_medium_term(user_id, memory)

            # 2. 获取中期记忆
            medium_memories = self._get_medium_term_memories(
                user_id,
                self.medium_term_size
            )

            if not medium_memories:
                return

            # 3. 应用遗忘策略
            to_keep, to_forget = self.strategy.filter_memories(
                medium_memories,
                current_time=datetime.now(timezone.utc)
            )

            # 4. 更新中期记忆
            self._update_medium_term_memories(user_id, to_keep)

            # 5. 压缩遗忘的记忆到长期记忆
            if to_forget:
                summary = self.strategy.compress_to_summary(to_forget, mode="simple")
                self._append_to_long_term(user_id, summary)

            # ✅ P1-5修复: 记录遗忘性能
            latency_ms = (time.time() - start_time) * 1000
            self.metrics.record_forget(latency_ms)

        finally:
            # 确保释放锁
            try:
                lock.release()
            except redis.exceptions.LockError:
                pass  # 锁可能已经过期自动释放

    # ==================== 状态快照 ====================

    def create_snapshot(
        self,
        user_id: str,
        conversation_id: str,
        description: str = "",
        tags: List[str] = None
    ) -> str:
        """
        创建记忆状态快照

        Args:
            user_id: 用户ID
            conversation_id: 会话ID
            description: 快照描述
            tags: 快照标签

        Returns:
            str: 快照ID

        示例:
            >>> snapshot_id = manager.create_snapshot(
            ...     user_id="user_123",
            ...     conversation_id="conv_456",
            ...     description="完成第一章创作后的状态"
            ... )
        """
        snapshot = MemorySnapshot(
            snapshot_id=self._generate_snapshot_id(),
            user_id=user_id,
            conversation_id=conversation_id,
            created_at=datetime.now(timezone.utc),
            short_term_memories=self._get_short_term_memories(user_id, self.short_term_size),
            medium_term_memories=self._get_medium_term_memories(user_id, self.medium_term_size),
            long_term_summary=self._get_long_term_summary(user_id),
            description=description,
            tags=tags or []
        )

        # 保存快照到Redis（TTL 7天）
        key = f"memory:snapshot:{snapshot.snapshot_id}"
        self.redis.set(
            key,
            snapshot.model_dump_json(),  # Pydantic v2
            ex=86400 * 7  # 7天过期
        )

        return snapshot.snapshot_id

    def restore_snapshot(
        self,
        snapshot_id: str
    ) -> MemorySnapshot:
        """
        恢复记忆快照

        Args:
            snapshot_id: 快照ID

        Returns:
            MemorySnapshot: 快照对象

        Raises:
            ValueError: 快照不存在

        示例:
            >>> snapshot = manager.restore_snapshot("snap_abc123")
        """
        key = f"memory:snapshot:{snapshot_id}"
        data = self.redis.get(key)

        if not data:
            raise ValueError(f"Snapshot {snapshot_id} not found")

        # 反序列化快照
        snapshot = MemorySnapshot.model_validate_json(data)  # Pydantic v2

        # 恢复记忆状态
        self._restore_memories_from_snapshot(snapshot)

        return snapshot

    # ==================== 私有方法：Redis 操作 ====================

    def _add_to_short_term(self, user_id: str, memory: MemoryItem):
        """添加到短期记忆（Redis List）- 使用事务确保原子性"""
        key = f"memory:{user_id}:short_term"
        # 使用pipeline确保原子性（修复P0-4：竞态条件）
        pipe = self.redis.pipeline()
        # LPUSH 添加到列表头部（最新的在前）
        pipe.lpush(key, memory.model_dump_json())
        # LTRIM 保持列表大小
        pipe.ltrim(key, 0, self.short_term_size - 1)
        # 设置过期时间（修复P0-2：从1小时改为24小时）
        pipe.expire(key, self.SHORT_TERM_TTL)
        pipe.execute()

    def _get_short_term_memories(self, user_id: str, limit: int) -> List[MemoryItem]:
        """获取短期记忆"""
        key = f"memory:{user_id}:short_term"
        data_list = self.redis.lrange(key, 0, limit - 1)

        memories = []
        for data in data_list:
            try:
                memory = MemoryItem.model_validate_json(data)
                memories.append(memory)
            except Exception as e:
                # 跳过损坏的数据
                continue

        return memories

    def _add_to_medium_term(self, user_id: str, memory: MemoryItem):
        """添加到中期记忆（Redis Sorted Set）- 使用事务确保原子性"""
        key = f"memory:{user_id}:medium_term"
        # 使用初始重要度作为score
        score = memory.importance

        # 根据重要度动态设置TTL（修复P1-1）
        if memory.importance >= 0.8:
            ttl = 86400 * 7  # 重要记忆: 7天
        elif memory.importance >= 0.6:
            ttl = 86400 * 5  # 较重要记忆: 5天
        else:
            ttl = self.MEDIUM_TERM_TTL  # 普通记忆: 3天

        # 使用pipeline确保原子性（修复P0-4：竞态条件）
        pipe = self.redis.pipeline()
        pipe.zadd(key, {memory.model_dump_json(): score})
        pipe.expire(key, ttl)
        pipe.execute()

    def _get_medium_term_memories(self, user_id: str, limit: int) -> List[MemoryItem]:
        """获取中期记忆（按重要度倒序）"""
        key = f"memory:{user_id}:medium_term"
        # ZREVRANGE 按score倒序获取
        data_list = self.redis.zrevrange(key, 0, limit - 1)

        memories = []
        for data in data_list:
            try:
                memory = MemoryItem.model_validate_json(data)
                memories.append(memory)
            except Exception as e:
                continue

        return memories

    def _update_medium_term_memories(self, user_id: str, memories: List[MemoryItem]):
        """更新中期记忆 - 使用事务确保原子性（修复P0-4）"""
        key = f"memory:{user_id}:medium_term"

        # 使用pipeline确保原子性（修复P0-4：竞态条件）
        pipe = self.redis.pipeline()

        # 清空旧数据
        pipe.delete(key)

        # 重新添加
        if memories:
            mapping = {}
            max_importance = 0.0
            for memory in memories:
                # 使用metadata中的current_importance作为score
                score = memory.metadata.get('current_importance', memory.importance)
                mapping[memory.model_dump_json()] = score
                max_importance = max(max_importance, score)

            pipe.zadd(key, mapping)

            # 根据最高重要度设置TTL（修复P1-1）
            if max_importance >= 0.8:
                ttl = 86400 * 7  # 7天
            elif max_importance >= 0.6:
                ttl = 86400 * 5  # 5天
            else:
                ttl = self.MEDIUM_TERM_TTL  # 3天
            pipe.expire(key, ttl)

        pipe.execute()

    def _get_long_term_summary(self, user_id: str) -> str:
        """
        获取长期记忆摘要

        ✅ P1-6修复: 支持从磁盘恢复（Redis故障容错）
        """
        key = f"memory:{user_id}:long_term"

        try:
            summary = self.redis.get(key)

            if summary is None:
                # ✅ P1-6修复: Redis无数据时，尝试从磁盘恢复
                logger.info(f"[P1-6] Long-term memory not in Redis, attempting disk restore for user={user_id}")

                # 异步加载（在同步上下文中使用run_sync）
                import asyncio
                try:
                    loop = asyncio.get_event_loop()
                except RuntimeError:
                    loop = asyncio.new_event_loop()
                    asyncio.set_event_loop(loop)

                disk_content = loop.run_until_complete(
                    self.long_term_store.load(user_id, verify_checksum=True)
                )

                if disk_content:
                    # 恢复到Redis
                    self.redis.set(key, disk_content)
                    logger.info(f"[P1-6] Successfully restored long-term memory from disk for user={user_id}")
                    return disk_content
                else:
                    logger.warning(f"[P1-6] No disk backup found for user={user_id}")
                    return ""

            # 兼容 decode_responses=True 和 False 两种情况
            return summary.decode('utf-8') if isinstance(summary, bytes) else summary

        except redis.RedisError as e:
            # ✅ P1-6修复: Redis故障时从磁盘恢复
            logger.error(f"[P1-6] Redis error when fetching long-term memory: {e}, attempting disk restore")
            self.metrics.redis_errors.increment()

            import asyncio
            try:
                loop = asyncio.get_event_loop()
            except RuntimeError:
                loop = asyncio.new_event_loop()
                asyncio.set_event_loop(loop)

            disk_content = loop.run_until_complete(
                self.long_term_store.load(user_id, verify_checksum=True)
            )

            return disk_content or ""

    def _append_to_long_term(self, user_id: str, summary: str) -> None:
        """
        追加到长期记忆

        ✅ P1-6修复: 同步保存到磁盘，支持自动压缩和备份
        """
        key = f"memory:{user_id}:long_term"
        current = self._get_long_term_summary(user_id)

        # 追加新摘要
        new_summary = f"{current}\n{summary}" if current else summary

        try:
            # 保存到Redis
            self.redis.set(key, new_summary)
            logger.debug(f"Appended to long-term memory for user {user_id}")

            # ✅ P1-6修复: 同步保存到磁盘（异步执行）
            import asyncio
            try:
                loop = asyncio.get_event_loop()
            except RuntimeError:
                loop = asyncio.new_event_loop()
                asyncio.set_event_loop(loop)

            # 保存到磁盘（自动压缩、备份）
            backup_result = loop.run_until_complete(
                self.long_term_store.save(
                    user_id=user_id,
                    content=new_summary,
                    auto_compress=True,  # 超过50KB自动二次压缩
                    create_backup=True    # 创建历史备份
                )
            )

            if backup_result.get("success"):
                logger.info(
                    f"[P1-6] Long-term memory backed up to disk: user={user_id}, "
                    f"size={backup_result.get('content_size_kb', 0):.2f}KB, "
                    f"compressed={backup_result.get('compressed', False)}, "
                    f"secondary_compressed={backup_result.get('secondary_compressed', False)}, "
                    f"backup_version={backup_result.get('backup_version', 0)}"
                )
            else:
                logger.error(f"[P1-6] Failed to backup long-term memory to disk for user={user_id}")

        except redis.RedisError as e:
            logger.error(f"[P1-6] Redis error when appending to long-term memory: {e}")
            self.metrics.redis_errors.increment()

            # 即使Redis失败，也要保存到磁盘
            import asyncio
            try:
                loop = asyncio.get_event_loop()
            except RuntimeError:
                loop = asyncio.new_event_loop()
                asyncio.set_event_loop(loop)

            loop.run_until_complete(
                self.long_term_store.save(user_id=user_id, content=new_summary)
            )
            logger.warning(f"[P1-6] Saved to disk only (Redis unavailable) for user={user_id}")

    def _restore_memories_from_snapshot(self, snapshot: MemorySnapshot):
        """从快照恢复记忆"""
        user_id = snapshot.user_id

        # 清空当前记忆
        self.redis.delete(f"memory:{user_id}:short_term")
        self.redis.delete(f"memory:{user_id}:medium_term")

        # 恢复短期记忆
        for memory in snapshot.short_term_memories:
            self._add_to_short_term(user_id, memory)

        # 恢复中期记忆
        self._update_medium_term_memories(user_id, snapshot.medium_term_memories)

        # 恢复长期记忆
        if snapshot.long_term_summary:
            key = f"memory:{user_id}:long_term"
            self.redis.set(key, snapshot.long_term_summary)

    # ==================== 辅助方法 ====================

    def _generate_memory_id(self) -> str:
        """生成记忆ID"""
        return f"mem_{uuid.uuid4().hex[:12]}"

    def _generate_snapshot_id(self) -> str:
        """生成快照ID"""
        return f"snap_{uuid.uuid4().hex[:12]}"

    @robust_retry(max_attempts=3, delay=0.5, fallback_result=None)
    async def _safe_add_to_short_term(self, user_id: str, memory: MemoryItem):
        """安全添加到短期记忆（带重试机制）"""
        self._add_to_short_term(user_id, memory)

    @robust_retry(max_attempts=3, delay=0.5, fallback_result=None)
    async def _safe_get_short_term_memories(self, user_id: str, limit: int) -> List[MemoryItem]:
        """安全获取短期记忆（带重试机制）"""
        return self._get_short_term_memories(user_id, limit)

    @robust_retry(max_attempts=3, delay=0.5, fallback_result=[])
    async def _safe_get_medium_term_memories(self, user_id: str, limit: int) -> List[MemoryItem]:
        """安全获取中期记忆（带重试机制）"""
        return self._get_medium_term_memories(user_id, limit)

    @cache_result(ttl=300)  # 5分钟缓存
    async def get_recent_memories_safe(
        self,
        user_id: str,
        limit: int = 10,
        fallback_to_empty: bool = True
    ) -> List[MemoryItem]:
        """
        安全获取最近记忆（带降级处理）

        Args:
            user_id: 用户ID
            limit: 返回数量限制
            fallback_to_empty: Redis失败时是否返回空列表

        Returns:
            List[MemoryItem]: 记忆列表
        """
        try:
            # 首先尝试从缓存索引获取
            memory_index = self.get_user_memory_index(user_id)

            if memory_index:
                # 从索引中获取最新的记忆ID
                latest_ids = [item['id'] for item in memory_index[-limit:]]

                # 批量获取记忆条目
                memories = await self._get_memories_by_ids(user_id, latest_ids)

                if memories:
                    logger.debug(f"Retrieved {len(memories)} memories from cache index for user {user_id}")
                    return memories[:limit]

            # 缓存未命中，回退到Redis查询
            return await self._get_memories_from_redis(user_id, limit, fallback_to_empty)

        except Exception as e:
            error_info = global_error_handler.classify_error(
                e,
                {"user_id": user_id, "action": "get_recent_memories"}
            )
            global_error_handler.handle_error(error_info)

            if fallback_to_empty:
                logger.warning(f"Memory retrieval failed for user {user_id}, returning empty list")
                return []
            else:
                raise

    def _update_cache_index(self, user_id: str, memory: MemoryItem) -> None:
        """更新缓存索引"""
        try:
            global _memory_index_cache
            if _memory_index_cache is None:
                _memory_index_cache = performance_optimizer.cache

            # 为用户的记忆创建索引
            index_key = f"user_memories:{user_id}"

            # 从缓存获取现有索引
            cached_memories = _memory_index_cache.get(index_key)
            if cached_memories is None:
                cached_memories = []

            # 添加新缓存记忆ID
            cached_memories.append({
                'id': memory.id,
                'conversation_id': memory.conversation_id,
                'role': memory.role,
                'timestamp': memory.timestamp.isoformat(),
                'importance': memory.importance
            })

            # 保持索引大小合理
            if len(cached_memories) > 100:
                cached_memories = cached_memories[-100:]  # 保留最新的100条

            # 更新缓存
            _memory_index_cache.set(index_key, cached_memories, ttl=1800)  # 30分钟

        except Exception as e:
            logger.warning(f"Failed to update cache index for user {user_id}: {e}")

    @cache_result(ttl=300)  # 5分钟缓存
    def get_user_memory_index(self, user_id: str) -> List[Dict[str, Any]]:
        """获取用户的记忆索引"""
        global _memory_index_cache
        if _memory_index_cache is None:
            _memory_index_cache = performance_optimizer.cache

        index_key = f"user_memories:{user_id}"
        return _memory_index_cache.get(index_key) or []

    async def _get_memories_by_ids(self, user_id: str, memory_ids: List[str]) -> List[MemoryItem]:
        """根据ID列表获取记忆条目"""
        memories = []

        # 尝试从短期记忆获取
        short_key = f"memory:{user_id}:short_term"
        try:
            short_ids = self.redis.lrange(short_key, 0, -1)
            for mem_data in short_ids:
                try:
                    mem_dict = json.loads(mem_data.decode('utf-8'))
                    if mem_dict['id'] in memory_ids:
                        memories.append(MemoryItem(**mem_dict))
                        if len(memories) >= len(memory_ids):
                            break
                except Exception:
                    continue
        except Exception as e:
            logger.debug(f"Failed to get memories by IDs from short term: {e}")

        # 如果短期记忆不足，从中期记忆获取
        if len(memories) < len(memory_ids):
            remaining_ids = [mid for mid in memory_ids if mid not in [m.id for m in memories]]

            if remaining_ids:
                medium_key = f"memory:{user_id}:medium_term"
                try:
                    medium_ids = self.redis.zrevrange(medium_key, 0, -1)
                    for mem_data in medium_ids:
                        try:
                            mem_dict = json.loads(mem_data.decode('utf-8'))
                            if mem_dict['id'] in remaining_ids:
                                memories.append(MemoryItem(**mem_dict))
                                if len(memories) >= len(memory_ids):
                                    break
                        except Exception:
                            continue
                except Exception as e:
                    logger.debug(f"Failed to get memories by IDs from medium term: {e}")

        return memories

    async def _get_memories_from_redis(self, user_id: str, limit: int, fallback_to_empty: bool) -> List[MemoryItem]:
        """从Redis获取记忆"""
        try:
            # 尝试获取短期记忆
            short_memories = await self._safe_get_short_term_memories(user_id, limit)

            # 如果短期记忆不足，获取中期记忆
            if len(short_memories) < limit:
                medium_memories = await self._safe_get_medium_term_memories(user_id, limit - len(short_memories))
                return short_memories + medium_memories[:limit - len(short_memories)]

            return short_memories[:limit]

        except Exception as e:
            error_info = global_error_handler.classify_error(
                e,
                {"user_id": user_id, "action": "get_memories_from_redis"}
            )
            global_error_handler.handle_error(error_info)

            if fallback_to_empty:
                logger.warning(f"Redis memory retrieval failed for user {user_id}, returning empty list")
                return []
            else:
                raise

    def get_stats(self, user_id: str) -> MemoryStats:
        """
        获取记忆统计信息

        Args:
            user_id: 用户ID

        Returns:
            MemoryStats: 统计信息
        """
        short_memories = self._get_short_term_memories(user_id, self.short_term_size)
        medium_memories = self._get_medium_term_memories(user_id, self.medium_term_size)
        long_summary = self._get_long_term_summary(user_id)

        total_access = sum(m.access_count for m in short_memories + medium_memories)
        all_memories = short_memories + medium_memories
        avg_importance = (
            sum(m.importance for m in all_memories) / len(all_memories)
            if all_memories else 0
        )

        return MemoryStats(
            user_id=user_id,
            short_term_count=len(short_memories),
            medium_term_count=len(medium_memories),
            long_term_summary_length=len(long_summary),
            total_access_count=total_access,
            avg_importance=avg_importance,
            last_update=datetime.now(timezone.utc)
        )
