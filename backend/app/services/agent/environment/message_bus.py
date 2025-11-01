"""
MessageBus - 消息总线
用于Agent系统内部组件间的解耦通信
"""

from typing import Callable, Dict, List, Any, Optional
from pydantic import BaseModel, Field
from datetime import datetime
from enum import Enum
import asyncio
import logging

logger = logging.getLogger(__name__)


class MessageType(str, Enum):
    """消息类型枚举"""
    ACTION_STARTED = "action_started"
    ACTION_COMPLETED = "action_completed"
    ACTION_FAILED = "action_failed"
    STATE_UPDATED = "state_updated"
    TOOL_CALLED = "tool_called"
    AGENT_THINKING = "agent_thinking"
    CUSTOM = "custom"


class Message(BaseModel):
    """
    消息对象

    Attributes:
        topic: 消息主题/类型
        sender: 发送者标识
        content: 消息内容
        timestamp: 时间戳
        metadata: 附加元数据
    """
    topic: str = Field(..., description="消息主题")
    sender: str = Field(..., description="发送者标识")
    content: Dict[str, Any] = Field(default_factory=dict, description="消息内容")
    timestamp: datetime = Field(default_factory=datetime.now, description="时间戳")
    metadata: Dict[str, Any] = Field(default_factory=dict, description="附加元数据")

    class Config:
        json_encoders = {
            datetime: lambda v: v.isoformat()
        }


class MessageBus:
    """
    消息总线 - 用于组件间通信

    实现发布-订阅模式,支持:
    1. 异步消息发布
    2. 主题订阅/取消订阅
    3. 消息历史记录
    4. 同步/异步handler支持

    Example:
        >>> bus = MessageBus()
        >>>
        >>> # 订阅消息
        >>> async def handler(msg: Message):
        ...     print(f"收到消息: {msg.content}")
        >>>
        >>> bus.subscribe("action_started", handler)
        >>>
        >>> # 发布消息
        >>> await bus.publish(Message(
        ...     topic="action_started",
        ...     sender="agent",
        ...     content={"action": "writing"}
        ... ))
    """

    def __init__(self, max_history: int = 1000):
        """
        初始化消息总线

        Args:
            max_history: 最大历史消息数量
        """
        self._subscribers: Dict[str, List[Callable]] = {}
        self._message_history: List[Message] = []
        self._max_history = max_history
        logger.info("[MessageBus] 初始化完成")

    async def publish(self, message: Message) -> None:
        """
        发布消息

        Args:
            message: 要发布的消息
        """
        logger.debug(
            f"[MessageBus] 发布消息: topic={message.topic}, sender={message.sender}"
        )

        # 记录到历史
        self._add_to_history(message)

        # 通知订阅者
        if message.topic in self._subscribers:
            handlers = self._subscribers[message.topic]
            logger.debug(f"[MessageBus] 通知 {len(handlers)} 个订阅者")

            # 并发执行所有handler
            tasks = [
                self._call_handler(handler, message)
                for handler in handlers
            ]

            # gather with return_exceptions=True 确保一个handler失败不影响其他
            results = await asyncio.gather(*tasks, return_exceptions=True)

            # 记录失败的handler
            for i, result in enumerate(results):
                if isinstance(result, Exception):
                    logger.error(
                        f"[MessageBus] Handler {i} 执行失败: {result}"
                    )

    async def _call_handler(self, handler: Callable, message: Message) -> None:
        """
        调用handler(支持同步和异步)

        Args:
            handler: 消息处理函数
            message: 消息对象
        """
        try:
            if asyncio.iscoroutinefunction(handler):
                await handler(message)
            else:
                # 同步函数在线程池中执行,避免阻塞
                loop = asyncio.get_event_loop()
                await loop.run_in_executor(None, handler, message)
        except Exception as e:
            logger.error(f"[MessageBus] Handler执行失败: {e}", exc_info=True)
            raise  # 重新抛出,由gather捕获

    def subscribe(self, topic: str, handler: Callable) -> None:
        """
        订阅主题

        Args:
            topic: 主题名称
            handler: 消息处理函数 (可以是同步或异步函数)
        """
        if topic not in self._subscribers:
            self._subscribers[topic] = []

        self._subscribers[topic].append(handler)
        logger.info(
            f"[MessageBus] 订阅成功: topic={topic}, "
            f"总订阅者={len(self._subscribers[topic])}"
        )

    def unsubscribe(self, topic: str, handler: Callable) -> bool:
        """
        取消订阅

        Args:
            topic: 主题名称
            handler: 要移除的处理函数

        Returns:
            是否成功取消订阅
        """
        if topic in self._subscribers and handler in self._subscribers[topic]:
            self._subscribers[topic].remove(handler)
            logger.info(f"[MessageBus] 取消订阅: topic={topic}")

            # 如果没有订阅者了,删除主题
            if not self._subscribers[topic]:
                del self._subscribers[topic]

            return True

        return False

    def get_subscribers_count(self, topic: Optional[str] = None) -> int:
        """
        获取订阅者数量

        Args:
            topic: 主题名称,None表示所有主题

        Returns:
            订阅者数量
        """
        if topic:
            return len(self._subscribers.get(topic, []))

        return sum(len(handlers) for handlers in self._subscribers.values())

    def get_history(
        self,
        topic: Optional[str] = None,
        limit: int = 100,
        sender: Optional[str] = None
    ) -> List[Message]:
        """
        获取消息历史

        Args:
            topic: 主题过滤,None表示所有主题
            limit: 返回最多消息数量
            sender: 发送者过滤,None表示所有发送者

        Returns:
            消息列表
        """
        messages = self._message_history

        # 过滤主题
        if topic:
            messages = [m for m in messages if m.topic == topic]

        # 过滤发送者
        if sender:
            messages = [m for m in messages if m.sender == sender]

        # 返回最后N条
        return messages[-limit:]

    def clear_history(self) -> None:
        """清空消息历史"""
        count = len(self._message_history)
        self._message_history.clear()
        logger.info(f"[MessageBus] 清空历史消息: {count} 条")

    def _add_to_history(self, message: Message) -> None:
        """
        添加消息到历史

        Args:
            message: 消息对象
        """
        self._message_history.append(message)

        # 超过最大数量时,删除最老的消息
        if len(self._message_history) > self._max_history:
            overflow = len(self._message_history) - self._max_history
            self._message_history = self._message_history[overflow:]

    def get_stats(self) -> Dict[str, Any]:
        """
        获取统计信息

        Returns:
            统计信息字典
        """
        return {
            "total_topics": len(self._subscribers),
            "total_subscribers": self.get_subscribers_count(),
            "history_count": len(self._message_history),
            "max_history": self._max_history,
            "topics": {
                topic: len(handlers)
                for topic, handlers in self._subscribers.items()
            }
        }


# 全局单例
_global_message_bus: Optional[MessageBus] = None


def get_message_bus() -> MessageBus:
    """
    获取全局消息总线单例

    Returns:
        MessageBus实例
    """
    global _global_message_bus

    if _global_message_bus is None:
        _global_message_bus = MessageBus()
        logger.info("[MessageBus] 创建全局单例")

    return _global_message_bus


def reset_message_bus() -> None:
    """
    重置全局消息总线(主要用于测试)
    """
    global _global_message_bus
    _global_message_bus = None
    logger.info("[MessageBus] 重置全局单例")
