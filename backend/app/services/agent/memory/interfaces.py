"""
记忆系统统一接口抽象 (P2-1修复)

定义记忆管理系统的统一接口，使不同实现可以互换使用。

核心接口：
- IMemoryManager: 记忆管理器基础接口
- IMemoryStore: 记忆存储接口
- IMemoryRetriever: 记忆检索接口
- IForgetStrategy: 遗忘策略接口

设计原则：
1. 接口隔离：每个接口职责单一
2. 依赖倒置：高层模块依赖抽象而非具体实现
3. 开闭原则：对扩展开放，对修改关闭

使用示例：
```python
# 注入不同的实现
manager: IMemoryManager = EnhancedMemoryManager(redis_client)
# 或
manager: IMemoryManager = SimpleMemoryManager()

# 统一的使用方式
await manager.add_memory(user_id="user_123", content="重要信息", role="user")
memories = await manager.retrieve_memories(user_id="user_123", query="设定")
```
"""

from abc import ABC, abstractmethod
from typing import List, Dict, Any, Optional, TypeVar, Generic
from datetime import datetime
from enum import Enum
from dataclasses import dataclass


class MemoryLayerType(Enum):
    """记忆层级枚举"""
    SHORT_TERM = "short_term"      # 短期记忆：最近对话
    MEDIUM_TERM = "medium_term"    # 中期记忆：重要对话
    LONG_TERM = "long_term"        # 长期记忆：永久摘要


@dataclass
class MemoryEntry:
    """
    统一的记忆条目数据结构

    所有记忆管理器实现必须使用此结构或其兼容结构
    """
    id: str                              # 唯一标识
    user_id: str                         # 用户ID
    content: str                         # 记忆内容
    role: str                            # 角色（user/assistant/system）
    importance: float                    # 重要度 (0.0-1.0)
    layer: MemoryLayerType               # 所属层级
    created_at: datetime                 # 创建时间
    updated_at: Optional[datetime]       # 更新时间
    metadata: Dict[str, Any]             # 扩展元数据
    access_count: int = 0                # 访问次数
    last_accessed: Optional[datetime] = None  # 最后访问时间


@dataclass
class RetrievalResult:
    """
    记忆检索结果

    包含检索到的记忆及其相关性得分
    """
    memory: MemoryEntry                  # 记忆条目
    score: float                         # 相关性得分 (0.0-1.0)
    source: str                          # 来源（short_term/medium_term/long_term/vector）


@dataclass
class MemoryStats:
    """
    记忆统计信息

    用于监控和展示记忆系统状态
    """
    user_id: str
    short_term_count: int
    medium_term_count: int
    long_term_size_kb: float
    total_tokens: int
    avg_importance: float
    oldest_memory: Optional[datetime]
    newest_memory: Optional[datetime]


class IMemoryStore(ABC):
    """
    记忆存储接口

    定义记忆的底层存储操作，负责数据的持久化。
    不同存储后端（Redis、PostgreSQL、文件系统）可以实现此接口。
    """

    @abstractmethod
    async def save(
        self,
        entry: MemoryEntry
    ) -> bool:
        """
        保存记忆条目

        Args:
            entry: 记忆条目

        Returns:
            是否保存成功
        """
        pass

    @abstractmethod
    async def load(
        self,
        memory_id: str
    ) -> Optional[MemoryEntry]:
        """
        加载单个记忆条目

        Args:
            memory_id: 记忆ID

        Returns:
            记忆条目，如果不存在返回None
        """
        pass

    @abstractmethod
    async def load_batch(
        self,
        user_id: str,
        layer: Optional[MemoryLayerType] = None,
        limit: int = 100
    ) -> List[MemoryEntry]:
        """
        批量加载记忆

        Args:
            user_id: 用户ID
            layer: 指定层级（可选）
            limit: 最大返回数量

        Returns:
            记忆条目列表
        """
        pass

    @abstractmethod
    async def delete(
        self,
        memory_id: str
    ) -> bool:
        """
        删除记忆条目

        Args:
            memory_id: 记忆ID

        Returns:
            是否删除成功
        """
        pass

    @abstractmethod
    async def update(
        self,
        memory_id: str,
        updates: Dict[str, Any]
    ) -> bool:
        """
        更新记忆条目

        Args:
            memory_id: 记忆ID
            updates: 要更新的字段

        Returns:
            是否更新成功
        """
        pass

    @abstractmethod
    async def clear(
        self,
        user_id: str,
        layer: Optional[MemoryLayerType] = None
    ) -> int:
        """
        清除记忆

        Args:
            user_id: 用户ID
            layer: 指定层级（可选，不指定则清除所有）

        Returns:
            清除的记忆数量
        """
        pass


class IMemoryRetriever(ABC):
    """
    记忆检索接口

    定义记忆的检索操作，支持多种检索方式。
    """

    @abstractmethod
    async def retrieve_by_recency(
        self,
        user_id: str,
        limit: int = 10,
        layer: Optional[MemoryLayerType] = None
    ) -> List[RetrievalResult]:
        """
        按时间检索最近的记忆

        Args:
            user_id: 用户ID
            limit: 最大返回数量
            layer: 指定层级

        Returns:
            检索结果列表
        """
        pass

    @abstractmethod
    async def retrieve_by_relevance(
        self,
        user_id: str,
        query: str,
        limit: int = 10,
        layer: Optional[MemoryLayerType] = None
    ) -> List[RetrievalResult]:
        """
        按相关性检索记忆

        Args:
            user_id: 用户ID
            query: 查询文本
            limit: 最大返回数量
            layer: 指定层级

        Returns:
            检索结果列表（按相关性排序）
        """
        pass

    @abstractmethod
    async def retrieve_by_importance(
        self,
        user_id: str,
        min_importance: float = 0.5,
        limit: int = 10,
        layer: Optional[MemoryLayerType] = None
    ) -> List[RetrievalResult]:
        """
        按重要度检索记忆

        Args:
            user_id: 用户ID
            min_importance: 最小重要度阈值
            limit: 最大返回数量
            layer: 指定层级

        Returns:
            检索结果列表（按重要度排序）
        """
        pass


class IForgetStrategy(ABC):
    """
    遗忘策略接口

    定义记忆的遗忘逻辑，可以实现不同的遗忘算法。
    """

    @abstractmethod
    async def should_forget(
        self,
        memory: MemoryEntry
    ) -> bool:
        """
        判断记忆是否应该被遗忘

        Args:
            memory: 记忆条目

        Returns:
            是否应该遗忘
        """
        pass

    @abstractmethod
    async def calculate_forget_score(
        self,
        memory: MemoryEntry
    ) -> float:
        """
        计算遗忘分数

        分数越高越可能被遗忘

        Args:
            memory: 记忆条目

        Returns:
            遗忘分数 (0.0-1.0)
        """
        pass

    @abstractmethod
    async def select_for_forget(
        self,
        memories: List[MemoryEntry],
        target_count: int
    ) -> List[MemoryEntry]:
        """
        选择要遗忘的记忆

        Args:
            memories: 候选记忆列表
            target_count: 目标遗忘数量

        Returns:
            选中的要遗忘的记忆列表
        """
        pass


class IImportanceEvaluator(ABC):
    """
    重要度评估接口

    定义记忆重要度的评估逻辑
    """

    @abstractmethod
    async def evaluate(
        self,
        content: str,
        role: str,
        context: Optional[Dict[str, Any]] = None
    ) -> float:
        """
        评估内容的重要度

        Args:
            content: 文本内容
            role: 角色（user/assistant/system）
            context: 上下文信息（可选）

        Returns:
            重要度分数 (0.0-1.0)
        """
        pass

    @abstractmethod
    async def adjust_importance(
        self,
        memory: MemoryEntry,
        event: str,
        context: Optional[Dict[str, Any]] = None
    ) -> float:
        """
        根据事件调整重要度

        Args:
            memory: 记忆条目
            event: 触发事件（access/reference/time_decay）
            context: 上下文信息

        Returns:
            调整后的重要度
        """
        pass


class IMemoryManager(ABC):
    """
    记忆管理器核心接口

    整合存储、检索、遗忘等功能的统一入口。
    这是最常用的接口，大多数业务代码应该依赖此接口。
    """

    @abstractmethod
    async def add_memory(
        self,
        user_id: str,
        content: str,
        role: str,
        importance: Optional[float] = None,
        metadata: Optional[Dict[str, Any]] = None
    ) -> str:
        """
        添加新记忆

        Args:
            user_id: 用户ID
            content: 记忆内容
            role: 角色（user/assistant/system）
            importance: 重要度（可选，不提供则自动评估）
            metadata: 扩展元数据

        Returns:
            新创建的记忆ID
        """
        pass

    @abstractmethod
    async def retrieve_memories(
        self,
        user_id: str,
        query: Optional[str] = None,
        limit: int = 10,
        layer: Optional[MemoryLayerType] = None,
        min_importance: float = 0.0
    ) -> List[RetrievalResult]:
        """
        检索记忆

        Args:
            user_id: 用户ID
            query: 查询文本（可选，不提供则按时间检索）
            limit: 最大返回数量
            layer: 指定层级
            min_importance: 最小重要度阈值

        Returns:
            检索结果列表
        """
        pass

    @abstractmethod
    async def update_memory(
        self,
        memory_id: str,
        updates: Dict[str, Any]
    ) -> bool:
        """
        更新记忆

        Args:
            memory_id: 记忆ID
            updates: 要更新的字段

        Returns:
            是否更新成功
        """
        pass

    @abstractmethod
    async def delete_memory(
        self,
        memory_id: str
    ) -> bool:
        """
        删除记忆

        Args:
            memory_id: 记忆ID

        Returns:
            是否删除成功
        """
        pass

    @abstractmethod
    async def apply_forgetting(
        self,
        user_id: str,
        force: bool = False
    ) -> int:
        """
        应用遗忘策略

        Args:
            user_id: 用户ID
            force: 是否强制执行（忽略阈值）

        Returns:
            遗忘的记忆数量
        """
        pass

    @abstractmethod
    async def get_stats(
        self,
        user_id: str
    ) -> MemoryStats:
        """
        获取记忆统计信息

        Args:
            user_id: 用户ID

        Returns:
            统计信息
        """
        pass

    @abstractmethod
    async def create_snapshot(
        self,
        user_id: str,
        description: str = ""
    ) -> str:
        """
        创建记忆快照

        Args:
            user_id: 用户ID
            description: 快照描述

        Returns:
            快照ID
        """
        pass

    @abstractmethod
    async def restore_snapshot(
        self,
        user_id: str,
        snapshot_id: str
    ) -> bool:
        """
        从快照恢复记忆

        Args:
            user_id: 用户ID
            snapshot_id: 快照ID

        Returns:
            是否恢复成功
        """
        pass


class IContextBuilder(ABC):
    """
    上下文构建器接口

    负责将记忆组装成LLM可用的上下文
    """

    @abstractmethod
    async def build_context(
        self,
        user_id: str,
        session_id: str,
        query: str,
        max_tokens: int = 8000
    ) -> Dict[str, Any]:
        """
        构建对话上下文

        Args:
            user_id: 用户ID
            session_id: 会话ID
            query: 当前查询
            max_tokens: 最大Token数

        Returns:
            包含messages和metadata的字典
        """
        pass

    @abstractmethod
    async def update_context(
        self,
        user_id: str,
        session_id: str,
        user_message: str,
        assistant_message: str
    ) -> bool:
        """
        更新上下文（添加新的对话轮次）

        Args:
            user_id: 用户ID
            session_id: 会话ID
            user_message: 用户消息
            assistant_message: 助手回复

        Returns:
            是否更新成功
        """
        pass


# ==================== 工厂模式支持 ====================

class MemoryManagerFactory:
    """
    记忆管理器工厂

    用于创建和管理不同类型的记忆管理器实例
    """

    _registry: Dict[str, type] = {}

    @classmethod
    def register(cls, name: str, manager_class: type):
        """注册记忆管理器类型"""
        if not issubclass(manager_class, IMemoryManager):
            raise TypeError(f"{manager_class.__name__} must implement IMemoryManager")
        cls._registry[name] = manager_class

    @classmethod
    def create(cls, name: str, **kwargs) -> IMemoryManager:
        """创建记忆管理器实例"""
        if name not in cls._registry:
            raise ValueError(f"Unknown memory manager type: {name}")
        return cls._registry[name](**kwargs)

    @classmethod
    def list_types(cls) -> List[str]:
        """列出所有注册的管理器类型"""
        return list(cls._registry.keys())


# ==================== 装饰器支持 ====================

def memory_operation(operation_name: str):
    """
    记忆操作装饰器

    用于统一记录操作日志和性能指标

    Usage:
        @memory_operation("add_memory")
        async def add_memory(self, ...):
            ...
    """
    def decorator(func):
        async def wrapper(self, *args, **kwargs):
            import time
            import logging
            logger = logging.getLogger(__name__)

            start_time = time.time()
            try:
                result = await func(self, *args, **kwargs)
                elapsed = (time.time() - start_time) * 1000
                logger.debug(
                    f"[MemoryOp] {operation_name} completed in {elapsed:.2f}ms"
                )
                return result
            except Exception as e:
                elapsed = (time.time() - start_time) * 1000
                logger.error(
                    f"[MemoryOp] {operation_name} failed after {elapsed:.2f}ms: {e}"
                )
                raise

        return wrapper
    return decorator
