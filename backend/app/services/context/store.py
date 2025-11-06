"""
上下文管理 - 存储层

提供上下文的持久化存储，支持：
- Redis存储（生产环境）
- 内存存储（测试环境）
"""

from abc import ABC, abstractmethod
from typing import Optional, Dict
import json
import redis.asyncio as redis
import logging

from app.services.context.models import Context, Message, ShortMemory, SummaryMemory, LongTermMemory

logger = logging.getLogger(__name__)


class ContextStore(ABC):
    """上下文存储接口"""

    @abstractmethod
    async def load(self, session_id: str) -> Optional[Context]:
        """加载上下文"""
        pass

    @abstractmethod
    async def save(self, context: Context):
        """保存上下文"""
        pass

    @abstractmethod
    async def delete(self, session_id: str):
        """删除上下文"""
        pass


class RedisContextStore(ContextStore):
    """Redis实现的上下文存储"""

    def __init__(self, redis_url: str = "redis://localhost:6379/0"):
        self.redis_url = redis_url
        self.redis_client: Optional[redis.Redis] = None
        self.key_prefix = "context:"
        self.default_ttl = 86400  # 24小时

    async def connect(self):
        """连接Redis"""
        if not self.redis_client:
            try:
                self.redis_client = await redis.from_url(
                    self.redis_url,
                    encoding="utf-8",
                    decode_responses=True
                )
                logger.info("[ContextStore] Redis连接成功")
            except Exception as e:
                logger.error(f"[ContextStore] Redis连接失败: {str(e)}")
                raise

    async def load(self, session_id: str) -> Optional[Context]:
        """从Redis加载上下文"""
        await self.connect()

        key = f"{self.key_prefix}{session_id}"
        try:
            data = await self.redis_client.get(key)

            if not data:
                logger.debug(f"[ContextStore] 未找到上下文: {session_id}")
                return None

            context_dict = json.loads(data)
            context = self._deserialize_context(context_dict, session_id)
            logger.info(f"[ContextStore] 加载上下文: {session_id}, {len(context.short_memory.messages)}条消息")
            return context

        except Exception as e:
            logger.error(f"[ContextStore] 加载失败: {str(e)}")
            return None

    async def save(self, context: Context):
        """保存上下文到Redis"""
        await self.connect()

        key = f"{self.key_prefix}{context.session_id}"
        try:
            data = json.dumps(self._serialize_context(context), ensure_ascii=False)

            # 设置过期时间24小时
            await self.redis_client.setex(key, self.default_ttl, data)
            logger.info(f"[ContextStore] 保存上下文: {context.session_id}, token={context.get_total_tokens()}")

        except Exception as e:
            logger.error(f"[ContextStore] 保存失败: {str(e)}")
            raise

    async def delete(self, session_id: str):
        """删除上下文"""
        await self.connect()

        key = f"{self.key_prefix}{session_id}"
        try:
            await self.redis_client.delete(key)
            logger.info(f"[ContextStore] 删除上下文: {session_id}")
        except Exception as e:
            logger.error(f"[ContextStore] 删除失败: {str(e)}")
            raise

    def _serialize_context(self, context: Context) -> Dict:
        """序列化上下文为字典"""
        return {
            "session_id": context.session_id,
            "short_memory": {
                "messages": [
                    {
                        "role": msg.role,
                        "content": msg.content,
                        "timestamp": msg.timestamp,
                        "metadata": msg.metadata
                    }
                    for msg in context.short_memory.messages
                ],
                "max_turns": context.short_memory.max_turns
            },
            "summary_memory": {
                "summary": context.summary_memory.summary,
                "last_updated": context.summary_memory.last_updated,
                "important_facts": context.summary_memory.important_facts
            },
            "system_prompt": context.system_prompt
        }

    def _deserialize_context(self, data: Dict, session_id: str) -> Context:
        """从字典反序列化上下文"""
        # 重建短期记忆
        short_memory = ShortMemory(
            max_turns=data.get("short_memory", {}).get("max_turns", 6)
        )
        for msg_data in data.get("short_memory", {}).get("messages", []):
            short_memory.add_message(Message(
                role=msg_data["role"],
                content=msg_data["content"],
                timestamp=msg_data["timestamp"],
                metadata=msg_data.get("metadata", {})
            ))

        # 重建摘要记忆
        summary_data = data.get("summary_memory", {})
        summary_memory = SummaryMemory(
            summary=summary_data.get("summary", ""),
            last_updated=summary_data.get("last_updated", 0),
            important_facts=summary_data.get("important_facts", [])
        )

        # 重建长期记忆（当前未启用）
        long_term_memory = LongTermMemory(enabled=False)

        return Context(
            session_id=session_id,
            short_memory=short_memory,
            summary_memory=summary_memory,
            long_term_memory=long_term_memory,
            system_prompt=data.get("system_prompt", "")
        )


class MemoryContextStore(ContextStore):
    """内存实现的上下文存储（用于测试）"""

    def __init__(self):
        self.store: Dict[str, Context] = {}
        logger.info("[ContextStore] 使用内存存储")

    async def load(self, session_id: str) -> Optional[Context]:
        """从内存加载上下文"""
        context = self.store.get(session_id)
        if context:
            logger.debug(f"[ContextStore] 加载上下文: {session_id}")
        return context

    async def save(self, context: Context):
        """保存上下文到内存"""
        self.store[context.session_id] = context
        logger.debug(f"[ContextStore] 保存上下文: {context.session_id}")

    async def delete(self, session_id: str):
        """从内存删除上下文"""
        if session_id in self.store:
            del self.store[session_id]
            logger.debug(f"[ContextStore] 删除上下文: {session_id}")
