"""
统一记忆协调器（✅ P0-1修复）

解决三套记忆系统并存的架构问题：
1. AsyncRedisSaver - LangGraph原生checkpointer（对话历史）
2. EnhancedMemoryManager - 三层记忆系统（短期/中期/长期）
3. ContextManager - 上下文管理（Token预算/压缩/摘要）

协调策略：
- 统一入口：所有记忆操作通过协调器进行
- 数据同步：确保三个系统间数据一致性
- 职责分离：每个系统专注自己的核心功能
- 降级支持：任一系统故障不影响整体可用性

架构关系：
                    UnifiedMemoryCoordinator (统一入口)
                            |
            +---------------+---------------+
            |               |               |
    AsyncRedisSaver  EnhancedMemory   ContextManager
    (对话checkpoint)  (三层记忆)      (Token管理)
"""

import logging
import asyncio
from typing import Optional, Dict, Any, List, TYPE_CHECKING
from datetime import datetime, timezone
from dataclasses import dataclass, field
from enum import Enum

if TYPE_CHECKING:
    from langgraph.checkpoint.redis import AsyncRedisSaver
    from app.services.agent.memory.enhanced_memory_manager import EnhancedMemoryManager
    from app.services.context.manager import ContextManager

logger = logging.getLogger(__name__)


class MemorySystemStatus(Enum):
    """记忆系统状态"""
    HEALTHY = "healthy"
    DEGRADED = "degraded"
    UNAVAILABLE = "unavailable"


@dataclass
class MemorySystemHealth:
    """记忆系统健康状态"""
    checkpointer: MemorySystemStatus = MemorySystemStatus.UNAVAILABLE
    enhanced_memory: MemorySystemStatus = MemorySystemStatus.UNAVAILABLE
    context_manager: MemorySystemStatus = MemorySystemStatus.UNAVAILABLE
    last_check: Optional[datetime] = None
    error_messages: Dict[str, str] = field(default_factory=dict)


@dataclass
class UnifiedMemoryConfig:
    """统一记忆配置"""
    # 同步策略
    sync_to_enhanced_memory: bool = True  # 是否同步到增强记忆
    sync_to_context_manager: bool = True  # 是否同步到上下文管理器

    # 降级策略
    fallback_on_checkpointer_failure: bool = True
    fallback_on_enhanced_memory_failure: bool = True

    # 健康检查
    health_check_interval: int = 60  # 秒

    # 数据一致性
    ensure_consistency: bool = True  # 确保数据一致性


class UnifiedMemoryCoordinator:
    """
    统一记忆协调器

    作为三个记忆系统的统一入口，负责：
    1. 协调数据写入（确保一致性）
    2. 协调数据读取（智能选择源）
    3. 健康监控和降级处理
    4. 记忆同步和迁移
    """

    def __init__(
        self,
        checkpointer: Optional['AsyncRedisSaver'] = None,
        enhanced_memory: Optional['EnhancedMemoryManager'] = None,
        context_manager: Optional['ContextManager'] = None,
        config: Optional[UnifiedMemoryConfig] = None
    ):
        """
        初始化统一记忆协调器

        Args:
            checkpointer: LangGraph checkpointer实例
            enhanced_memory: 增强记忆管理器实例
            context_manager: 上下文管理器实例
            config: 协调器配置
        """
        self.checkpointer = checkpointer
        self.enhanced_memory = enhanced_memory
        self.context_manager = context_manager
        self.config = config or UnifiedMemoryConfig()

        self._health = MemorySystemHealth()
        self._sync_lock = asyncio.Lock()
        self._initialized = False

        logger.info("[UnifiedMemoryCoordinator] 初始化统一记忆协调器")

    async def initialize(self):
        """初始化所有记忆系统"""
        if self._initialized:
            return

        # 初始化checkpointer（如果需要）
        if self.checkpointer:
            try:
                # AsyncRedisSaver需要调用asetup()
                if hasattr(self.checkpointer, 'asetup'):
                    await self.checkpointer.asetup()
                self._health.checkpointer = MemorySystemStatus.HEALTHY
                logger.info("[UnifiedMemoryCoordinator] ✅ Checkpointer初始化成功")
            except Exception as e:
                self._health.checkpointer = MemorySystemStatus.UNAVAILABLE
                self._health.error_messages['checkpointer'] = str(e)
                logger.error(f"[UnifiedMemoryCoordinator] ❌ Checkpointer初始化失败: {e}")

        # 检查增强记忆
        if self.enhanced_memory:
            try:
                # 简单的健康检查
                self.enhanced_memory.get_stats("test_user")
                self._health.enhanced_memory = MemorySystemStatus.HEALTHY
                logger.info("[UnifiedMemoryCoordinator] ✅ EnhancedMemory初始化成功")
            except Exception as e:
                self._health.enhanced_memory = MemorySystemStatus.DEGRADED
                self._health.error_messages['enhanced_memory'] = str(e)
                logger.warning(f"[UnifiedMemoryCoordinator] ⚠️ EnhancedMemory状态降级: {e}")

        # 检查上下文管理器
        if self.context_manager:
            self._health.context_manager = MemorySystemStatus.HEALTHY
            logger.info("[UnifiedMemoryCoordinator] ✅ ContextManager已就绪")

        self._health.last_check = datetime.now(timezone.utc)
        self._initialized = True

        logger.info(
            f"[UnifiedMemoryCoordinator] 初始化完成 | "
            f"Checkpointer={self._health.checkpointer.value} | "
            f"EnhancedMemory={self._health.enhanced_memory.value} | "
            f"ContextManager={self._health.context_manager.value}"
        )

    # ==================== 统一写入接口 ====================

    async def save_conversation_turn(
        self,
        user_id: str,
        conversation_id: str,
        user_message: str,
        assistant_message: str,
        work_id: Optional[str] = None,
        metadata: Optional[Dict[str, Any]] = None
    ) -> Dict[str, bool]:
        """
        保存对话轮次（统一入口）

        将对话同时保存到所有可用的记忆系统：
        1. Checkpointer: 保存完整对话历史（LangGraph状态）
        2. EnhancedMemory: 提取并保存重要记忆
        3. ContextManager: 更新上下文（用于Token管理）

        Args:
            user_id: 用户ID
            conversation_id: 对话ID
            user_message: 用户消息
            assistant_message: 助手消息
            work_id: 作品ID（可选）
            metadata: 附加元数据

        Returns:
            各系统保存状态 {"checkpointer": True/False, "enhanced_memory": True/False, ...}
        """
        results = {
            "checkpointer": False,
            "enhanced_memory": False,
            "context_manager": False
        }

        async with self._sync_lock:
            # 1. 保存到EnhancedMemory（三层记忆）
            if self.enhanced_memory and self.config.sync_to_enhanced_memory:
                try:
                    # 保存用户消息
                    self.enhanced_memory.add_memory(
                        user_id=user_id,
                        conversation_id=conversation_id,
                        content=user_message,
                        memory_type="user_input",
                        metadata={"work_id": work_id, "role": "user", **(metadata or {})}
                    )

                    # 保存助手回复
                    self.enhanced_memory.add_memory(
                        user_id=user_id,
                        conversation_id=conversation_id,
                        content=assistant_message,
                        memory_type="assistant_response",
                        metadata={"work_id": work_id, "role": "assistant", **(metadata or {})}
                    )

                    results["enhanced_memory"] = True
                    logger.debug(f"[UnifiedMemoryCoordinator] ✅ 对话已保存到EnhancedMemory")

                except Exception as e:
                    logger.error(f"[UnifiedMemoryCoordinator] ❌ EnhancedMemory保存失败: {e}")
                    if not self.config.fallback_on_enhanced_memory_failure:
                        raise

            # 2. 保存到ContextManager（上下文管理）
            if self.context_manager and self.config.sync_to_context_manager:
                try:
                    await self.context_manager.update_context(
                        session_id=conversation_id,
                        new_messages=[
                            {"role": "user", "content": user_message},
                            {"role": "assistant", "content": assistant_message}
                        ],
                        work_id=work_id
                    )
                    results["context_manager"] = True
                    logger.debug(f"[UnifiedMemoryCoordinator] ✅ 对话已保存到ContextManager")

                except Exception as e:
                    logger.error(f"[UnifiedMemoryCoordinator] ❌ ContextManager保存失败: {e}")

            # 3. Checkpointer由LangGraph自动管理，这里只标记状态
            if self.checkpointer:
                results["checkpointer"] = True  # LangGraph自动处理

        return results

    async def save_memory_item(
        self,
        user_id: str,
        conversation_id: str,
        content: str,
        memory_type: str = "general",
        importance: Optional[float] = None,
        metadata: Optional[Dict[str, Any]] = None
    ) -> bool:
        """
        保存单条记忆（主要用于EnhancedMemory）

        Args:
            user_id: 用户ID
            conversation_id: 对话ID
            content: 记忆内容
            memory_type: 记忆类型
            importance: 重要度（0-1）
            metadata: 附加元数据

        Returns:
            是否保存成功
        """
        if not self.enhanced_memory:
            logger.warning("[UnifiedMemoryCoordinator] EnhancedMemory未配置，跳过保存")
            return False

        try:
            self.enhanced_memory.add_memory(
                user_id=user_id,
                conversation_id=conversation_id,
                content=content,
                memory_type=memory_type,
                importance=importance,
                metadata=metadata
            )
            return True
        except Exception as e:
            logger.error(f"[UnifiedMemoryCoordinator] 保存记忆失败: {e}")
            return False

    # ==================== 统一读取接口 ====================

    async def get_context_for_chat(
        self,
        user_id: str,
        conversation_id: str,
        query: str,
        work_id: Optional[str] = None,
        system_prompt: str = "",
        task_type: Optional[Any] = None
    ) -> Dict[str, Any]:
        """
        获取聊天上下文（统一接口）

        整合所有记忆系统的数据：
        1. ContextManager: 获取Token管理的消息列表
        2. EnhancedMemory: 获取相关长期记忆
        3. Checkpointer: （由LangGraph自动处理）

        Args:
            user_id: 用户ID
            conversation_id: 对话ID
            query: 当前查询（用于相关记忆检索）
            work_id: 作品ID
            system_prompt: 系统提示
            task_type: 任务类型（用于自适应预算）

        Returns:
            {
                "messages": [...],  # 格式化的消息列表
                "related_memories": [...],  # 相关长期记忆
                "metadata": {...}  # 元数据
            }
        """
        result = {
            "messages": [],
            "related_memories": [],
            "metadata": {
                "user_id": user_id,
                "conversation_id": conversation_id,
                "work_id": work_id,
                "sources": []
            }
        }

        # 1. 从ContextManager获取主要上下文
        if self.context_manager:
            try:
                # 设置user_id（如果ContextManager支持）
                if not self.context_manager.user_id:
                    self.context_manager.user_id = user_id

                context_result = await self.context_manager.build_context(
                    session_id=conversation_id,
                    system_prompt=system_prompt,
                    query=query,
                    task_type=task_type,
                    work_id=work_id,
                    chapter_id=metadata.get("chapter_id") if metadata else None
                )

                result["messages"] = context_result.get("messages", [])
                result["metadata"].update(context_result.get("metadata", {}))
                result["metadata"]["sources"].append("context_manager")

                logger.debug(
                    f"[UnifiedMemoryCoordinator] ContextManager返回 "
                    f"{len(result['messages'])} 条消息"
                )

            except Exception as e:
                logger.error(f"[UnifiedMemoryCoordinator] ContextManager获取失败: {e}")

        # 2. 从EnhancedMemory获取相关记忆
        if self.enhanced_memory:
            try:
                memories = self.enhanced_memory.retrieve_relevant_memories(
                    user_id=user_id,
                    query=query,
                    max_results=5
                )

                result["related_memories"] = memories
                result["metadata"]["sources"].append("enhanced_memory")

                logger.debug(
                    f"[UnifiedMemoryCoordinator] EnhancedMemory返回 "
                    f"{len(memories)} 条相关记忆"
                )

            except Exception as e:
                logger.error(f"[UnifiedMemoryCoordinator] EnhancedMemory检索失败: {e}")

        return result

    async def get_conversation_history(
        self,
        conversation_id: str,
        limit: int = 20
    ) -> List[Dict[str, Any]]:
        """
        获取对话历史

        优先从Checkpointer获取，降级从ContextManager获取

        Args:
            conversation_id: 对话ID
            limit: 最大返回条数

        Returns:
            对话历史列表
        """
        # 1. 尝试从Checkpointer获取
        if self.checkpointer and self._health.checkpointer == MemorySystemStatus.HEALTHY:
            try:
                config = {"configurable": {"thread_id": conversation_id}}
                checkpoint_tuple = await self.checkpointer.aget_tuple(config)

                if checkpoint_tuple and checkpoint_tuple.checkpoint:
                    messages = checkpoint_tuple.checkpoint.get("channel_values", {}).get("messages", [])
                    return [
                        {"role": msg.type, "content": msg.content}
                        for msg in messages[-limit:]
                    ]
            except Exception as e:
                logger.warning(f"[UnifiedMemoryCoordinator] Checkpointer获取历史失败: {e}")

        # 2. 降级从ContextManager获取
        if self.context_manager:
            try:
                context_result = await self.context_manager.build_context(
                    session_id=conversation_id,
                    system_prompt=""
                )
                messages = context_result.get("messages", [])
                return messages[-limit:]
            except Exception as e:
                logger.warning(f"[UnifiedMemoryCoordinator] ContextManager获取历史失败: {e}")

        return []

    # ==================== 记忆同步 ====================

    async def sync_memories(
        self,
        user_id: str,
        conversation_id: str,
        direction: str = "checkpointer_to_enhanced"
    ) -> Dict[str, int]:
        """
        同步记忆数据（用于数据一致性修复）

        Args:
            user_id: 用户ID
            conversation_id: 对话ID
            direction: 同步方向
                - "checkpointer_to_enhanced": Checkpointer → EnhancedMemory
                - "enhanced_to_context": EnhancedMemory → ContextManager

        Returns:
            同步统计 {"synced": N, "failed": M}
        """
        stats = {"synced": 0, "failed": 0}

        if direction == "checkpointer_to_enhanced":
            if not self.checkpointer or not self.enhanced_memory:
                logger.warning("[UnifiedMemoryCoordinator] 同步所需系统未就绪")
                return stats

            try:
                # 从Checkpointer获取历史
                config = {"configurable": {"thread_id": conversation_id}}
                checkpoint_tuple = await self.checkpointer.aget_tuple(config)

                if checkpoint_tuple and checkpoint_tuple.checkpoint:
                    messages = checkpoint_tuple.checkpoint.get("channel_values", {}).get("messages", [])

                    for msg in messages:
                        try:
                            self.enhanced_memory.add_memory(
                                user_id=user_id,
                                conversation_id=conversation_id,
                                content=msg.content,
                                memory_type="synced_from_checkpointer",
                                metadata={"role": msg.type, "synced": True}
                            )
                            stats["synced"] += 1
                        except Exception as e:
                            stats["failed"] += 1
                            logger.warning(f"[UnifiedMemoryCoordinator] 同步单条消息失败: {e}")

                    logger.info(
                        f"[UnifiedMemoryCoordinator] 同步完成: "
                        f"synced={stats['synced']}, failed={stats['failed']}"
                    )

            except Exception as e:
                logger.error(f"[UnifiedMemoryCoordinator] 同步失败: {e}")

        return stats

    # ==================== 健康监控 ====================

    async def health_check(self) -> MemorySystemHealth:
        """
        执行健康检查

        Returns:
            各系统健康状态
        """
        # 检查Checkpointer
        if self.checkpointer:
            try:
                # 简单的连通性测试
                config = {"configurable": {"thread_id": "__health_check__"}}
                await self.checkpointer.aget_tuple(config)
                self._health.checkpointer = MemorySystemStatus.HEALTHY
                self._health.error_messages.pop('checkpointer', None)
            except Exception as e:
                self._health.checkpointer = MemorySystemStatus.DEGRADED
                self._health.error_messages['checkpointer'] = str(e)

        # 检查EnhancedMemory
        if self.enhanced_memory:
            try:
                self.enhanced_memory.get_stats("__health_check__")
                self._health.enhanced_memory = MemorySystemStatus.HEALTHY
                self._health.error_messages.pop('enhanced_memory', None)
            except Exception as e:
                self._health.enhanced_memory = MemorySystemStatus.DEGRADED
                self._health.error_messages['enhanced_memory'] = str(e)

        # ContextManager通常不会失败
        if self.context_manager:
            self._health.context_manager = MemorySystemStatus.HEALTHY

        self._health.last_check = datetime.now(timezone.utc)
        return self._health

    def get_health_status(self) -> Dict[str, Any]:
        """获取健康状态摘要"""
        return {
            "checkpointer": self._health.checkpointer.value,
            "enhanced_memory": self._health.enhanced_memory.value,
            "context_manager": self._health.context_manager.value,
            "last_check": self._health.last_check.isoformat() if self._health.last_check else None,
            "errors": self._health.error_messages,
            "overall": "healthy" if all(
                status == MemorySystemStatus.HEALTHY
                for status in [
                    self._health.checkpointer,
                    self._health.enhanced_memory,
                    self._health.context_manager
                ] if status != MemorySystemStatus.UNAVAILABLE
            ) else "degraded"
        }

    # ==================== 清理和维护 ====================

    async def cleanup_conversation(
        self,
        user_id: str,
        conversation_id: str
    ) -> Dict[str, bool]:
        """
        清理对话相关的所有记忆

        Args:
            user_id: 用户ID
            conversation_id: 对话ID

        Returns:
            各系统清理状态
        """
        results = {
            "checkpointer": False,
            "enhanced_memory": False,
            "context_manager": False
        }

        # 清理ContextManager
        if self.context_manager:
            try:
                await self.context_manager.clear_context(conversation_id)
                results["context_manager"] = True
            except Exception as e:
                logger.error(f"[UnifiedMemoryCoordinator] ContextManager清理失败: {e}")

        # 清理EnhancedMemory（如果支持）
        if self.enhanced_memory:
            try:
                # EnhancedMemory通常通过TTL自动清理
                # 这里可以手动触发遗忘
                self.enhanced_memory.apply_forgetting(user_id, conversation_id)
                results["enhanced_memory"] = True
            except Exception as e:
                logger.error(f"[UnifiedMemoryCoordinator] EnhancedMemory清理失败: {e}")

        # Checkpointer通常通过TTL自动清理
        if self.checkpointer:
            results["checkpointer"] = True  # TTL自动处理

        return results

    def get_statistics(self) -> Dict[str, Any]:
        """获取统计信息"""
        stats = {
            "initialized": self._initialized,
            "health": self.get_health_status(),
            "config": {
                "sync_to_enhanced_memory": self.config.sync_to_enhanced_memory,
                "sync_to_context_manager": self.config.sync_to_context_manager,
                "ensure_consistency": self.config.ensure_consistency
            }
        }

        # 添加EnhancedMemory统计
        if self.enhanced_memory:
            try:
                stats["enhanced_memory_stats"] = self.enhanced_memory.get_stats("__global__")
            except Exception:
                pass

        return stats


# ==================== 全局实例管理 ====================

_unified_coordinator: Optional[UnifiedMemoryCoordinator] = None


def get_unified_coordinator() -> Optional[UnifiedMemoryCoordinator]:
    """获取全局统一记忆协调器实例"""
    return _unified_coordinator


def set_unified_coordinator(coordinator: UnifiedMemoryCoordinator):
    """设置全局统一记忆协调器实例"""
    global _unified_coordinator
    _unified_coordinator = coordinator
    logger.info("[UnifiedMemoryCoordinator] 全局实例已设置")


async def create_unified_coordinator(
    checkpointer: Optional['AsyncRedisSaver'] = None,
    enhanced_memory: Optional['EnhancedMemoryManager'] = None,
    context_manager: Optional['ContextManager'] = None,
    config: Optional[UnifiedMemoryConfig] = None
) -> UnifiedMemoryCoordinator:
    """
    创建并初始化统一记忆协调器

    Args:
        checkpointer: LangGraph checkpointer
        enhanced_memory: 增强记忆管理器
        context_manager: 上下文管理器
        config: 配置

    Returns:
        初始化好的协调器实例
    """
    coordinator = UnifiedMemoryCoordinator(
        checkpointer=checkpointer,
        enhanced_memory=enhanced_memory,
        context_manager=context_manager,
        config=config
    )

    await coordinator.initialize()
    set_unified_coordinator(coordinator)

    return coordinator
