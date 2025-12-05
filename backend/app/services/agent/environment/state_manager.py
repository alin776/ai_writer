"""
StateManager - 状态管理中枢
提供三级缓存的状态管理: 内存 → Redis → 数据库
"""

from typing import Dict, Any, Optional
import json
import logging
from datetime import datetime
from copy import deepcopy

from ..utils import robust_retry, safe_execute_async, global_error_handler, ErrorCategory
from app.utils.datetime_utils import get_utc_now

logger = logging.getLogger(__name__)


class StateManager:
    """
    状态管理中枢

    提供三级缓存的状态管理机制:
    1. 内存缓存 (最快,进程内)
    2. Redis缓存 (快速,跨进程)
    3. 数据库 (持久化,可恢复)

    Example:
        >>> manager = StateManager(redis_client=redis_client)
        >>>
        >>> # 获取状态
        >>> state = await manager.get_state("conv_123")
        >>>
        >>> # 更新状态
        >>> await manager.update_state("conv_123", {"messages": [...]})
        >>>
        >>> # 持久化到数据库
        >>> await manager.persist_state("conv_123")
    """

    def __init__(
        self,
        redis_client: Optional[Any] = None,
        db_session: Optional[Any] = None,
        default_ttl: int = 3600
    ):
        """
        初始化StateManager

        Args:
            redis_client: Redis客户端实例(可选)
            db_session: 数据库session实例(可选)
            default_ttl: Redis缓存默认过期时间(秒),默认1小时
        """
        self.redis = redis_client
        self.db = db_session
        self.default_ttl = default_ttl

        # 一级缓存: 内存缓存
        self._memory_cache: Dict[str, Dict[str, Any]] = {}

        logger.info(
            f"[StateManager] 初始化完成 "
            f"(Redis: {redis_client is not None}, "
            f"DB: {db_session is not None})"
        )

    async def get_state(self, conversation_id: str) -> Dict[str, Any]:
        """
        获取会话状态

        查找顺序: 内存缓存 → Redis → 数据库 → 创建默认状态

        Args:
            conversation_id: 会话ID

        Returns:
            状态字典
        """
        # 1. 尝试从内存缓存读取
        if conversation_id in self._memory_cache:
            logger.debug(
                f"[StateManager] 从内存缓存读取: {conversation_id}"
            )
            return deepcopy(self._memory_cache[conversation_id])

        # 2. 尝试从Redis读取
        if self.redis:
            state = await self._get_from_redis(conversation_id)
            if state is not None:
                logger.debug(
                    f"[StateManager] 从Redis读取: {conversation_id}"
                )
                # 更新内存缓存
                self._memory_cache[conversation_id] = state
                return deepcopy(state)

        # 3. 尝试从数据库读取
        if self.db:
            state = await self._get_from_db(conversation_id)
            if state is not None:
                logger.debug(
                    f"[StateManager] 从数据库读取: {conversation_id}"
                )
                # 更新缓存
                self._memory_cache[conversation_id] = state
                if self.redis:
                    await self._save_to_redis(conversation_id, state)
                return deepcopy(state)

        # 4. 创建默认状态
        logger.debug(f"[StateManager] 创建新状态: {conversation_id}")
        state = self._create_default_state()
        self._memory_cache[conversation_id] = state
        return deepcopy(state)

    async def update_state(
        self,
        conversation_id: str,
        updates: Dict[str, Any],
        persist_to_redis: bool = True
    ) -> None:
        """
        更新状态

        Args:
            conversation_id: 会话ID
            updates: 要更新的字段
            persist_to_redis: 是否立即持久化到Redis
        """
        # 1. 获取当前状态
        state = await self.get_state(conversation_id)

        # 2. 合并更新
        state.update(updates)
        state["updated_at"] = get_utc_now().isoformat()

        # 3. 更新内存缓存
        self._memory_cache[conversation_id] = state

        # 4. 可选: 持久化到Redis
        if persist_to_redis and self.redis:
            await self._save_to_redis(conversation_id, state)

        logger.debug(
            f"[StateManager] 状态已更新: {conversation_id}, "
            f"字段: {list(updates.keys())}"
        )

    async def set_state(
        self,
        conversation_id: str,
        state: Dict[str, Any],
        persist_to_redis: bool = True
    ) -> None:
        """
        直接设置完整状态(替换,不是合并)

        Args:
            conversation_id: 会话ID
            state: 完整的状态字典
            persist_to_redis: 是否立即持久化到Redis
        """
        # 更新时间戳
        state["updated_at"] = get_utc_now().isoformat()
        if "created_at" not in state:
            state["created_at"] = state["updated_at"]

        # 更新内存缓存
        self._memory_cache[conversation_id] = state

        # 可选: 持久化到Redis
        if persist_to_redis and self.redis:
            await self._save_to_redis(conversation_id, state)

        logger.debug(f"[StateManager] 状态已设置: {conversation_id}")

    async def persist_state(self, conversation_id: str) -> bool:
        """
        持久化状态到数据库

        Args:
            conversation_id: 会话ID

        Returns:
            是否成功持久化
        """
        if not self.db:
            logger.warning("[StateManager] 数据库未配置,无法持久化")
            return False

        state = await self.get_state(conversation_id)
        success = await self._save_to_db(conversation_id, state)

        if success:
            logger.info(f"[StateManager] 状态已持久化到数据库: {conversation_id}")
        else:
            logger.error(f"[StateManager] 状态持久化失败: {conversation_id}")

        return success

    async def clear_state(
        self,
        conversation_id: str,
        clear_redis: bool = True,
        clear_db: bool = False
    ) -> None:
        """
        清除状态

        Args:
            conversation_id: 会话ID
            clear_redis: 是否清除Redis缓存
            clear_db: 是否清除数据库记录
        """
        # 清除内存缓存
        if conversation_id in self._memory_cache:
            del self._memory_cache[conversation_id]

        # 清除Redis
        if clear_redis and self.redis:
            key = self._get_redis_key(conversation_id)
            await self.redis.delete(key)

        # 清除数据库
        if clear_db and self.db:
            await self._delete_from_db(conversation_id)

        logger.info(
            f"[StateManager] 状态已清除: {conversation_id} "
            f"(Redis: {clear_redis}, DB: {clear_db})"
        )

    def clear_memory_cache(self) -> int:
        """
        清空内存缓存

        Returns:
            清除的条目数量
        """
        count = len(self._memory_cache)
        self._memory_cache.clear()
        logger.info(f"[StateManager] 内存缓存已清空: {count} 条")
        return count

    def get_memory_cache_size(self) -> int:
        """
        获取内存缓存大小

        Returns:
            缓存条目数量
        """
        return len(self._memory_cache)

    # ========== Redis相关方法 ==========

    def _get_redis_key(self, conversation_id: str) -> str:
        """生成Redis key"""
        return f"agent:state:{conversation_id}"

    @robust_retry(max_attempts=3, delay=0.5, fallback_result=None)
    async def _get_from_redis(self, conversation_id: str) -> Optional[Dict[str, Any]]:
        """从Redis读取状态（带重试机制）"""
        key = self._get_redis_key(conversation_id)
        state_json = await self.redis.get(key)

        if state_json:
            if isinstance(state_json, bytes):
                state_json = state_json.decode('utf-8')
            return json.loads(state_json)

        return None

    @robust_retry(max_attempts=3, delay=0.5, fallback_result=False)
    async def _save_to_redis(
        self,
        conversation_id: str,
        state: Dict[str, Any]
    ) -> bool:
        """保存状态到Redis（带重试机制）"""
        key = self._get_redis_key(conversation_id)
        state_json = json.dumps(state, ensure_ascii=False)

        await self.redis.set(key, state_json, ex=self.default_ttl)
        return True

    # ========== 数据库相关方法 ==========

    async def _get_from_db(self, conversation_id: str) -> Optional[Dict[str, Any]]:
        """
        从数据库读取状态

        TODO: 实现数据库读取逻辑
        """
        # 这里需要根据实际数据库结构实现
        logger.debug("[StateManager] 数据库读取未实现")
        return None

    async def _save_to_db(
        self,
        conversation_id: str,
        state: Dict[str, Any]
    ) -> bool:
        """
        保存状态到数据库

        TODO: 实现数据库保存逻辑
        """
        # 这里需要根据实际数据库结构实现
        logger.debug("[StateManager] 数据库保存未实现")
        return False

    async def _delete_from_db(self, conversation_id: str) -> bool:
        """
        从数据库删除状态

        TODO: 实现数据库删除逻辑
        """
        # 这里需要根据实际数据库结构实现
        logger.debug("[StateManager] 数据库删除未实现")
        return False

    # ========== 辅助方法 ==========

    def _create_default_state(self) -> Dict[str, Any]:
        """
        创建默认状态

        Returns:
            默认状态字典
        """
        now = get_utc_now().isoformat()
        return {
            "messages": [],
            "work_id": None,
            "chapter_id": None,
            "intent": None,
            "context": {},
            "agent_steps": [],
            "suggested_actions": [],
            "final_response": None,
            "created_at": now,
            "updated_at": now,
        }


# 全局单例(可选)
_global_state_manager: Optional[StateManager] = None


def get_state_manager(
    redis_client: Optional[Any] = None,
    db_session: Optional[Any] = None
) -> StateManager:
    """
    获取全局StateManager单例

    Args:
        redis_client: Redis客户端(仅首次调用时有效)
        db_session: 数据库session(仅首次调用时有效)

    Returns:
        StateManager实例
    """
    global _global_state_manager

    if _global_state_manager is None:
        _global_state_manager = StateManager(
            redis_client=redis_client,
            db_session=db_session
        )
        logger.info("[StateManager] 创建全局单例")

    return _global_state_manager


def reset_state_manager() -> None:
    """
    重置全局StateManager(主要用于测试)
    """
    global _global_state_manager
    _global_state_manager = None
    logger.info("[StateManager] 重置全局单例")
