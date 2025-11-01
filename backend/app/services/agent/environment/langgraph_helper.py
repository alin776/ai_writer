"""
LangGraph Environment集成助手

提供便捷的方法将MessageBus和StateManager集成到LangGraph节点中
"""

from typing import Dict, Any, Optional, Callable
from functools import wraps
import logging

from app.services.agent.environment import (
    get_message_bus,
    Message,
    MessageType,
    StateManager
)
from app.services.agent.actions import ActionStatus

logger = logging.getLogger(__name__)


class LangGraphEnvironmentHelper:
    """
    LangGraph Environment集成助手

    提供:
    1. MessageBus消息发布
    2. StateManager状态管理
    3. Action执行装饰器
    """

    def __init__(
        self,
        redis_client: Optional[Any] = None,
        enable_message_bus: bool = True,
        enable_state_manager: bool = True
    ):
        """
        初始化助手

        Args:
            redis_client: Redis客户端(可选)
            enable_message_bus: 是否启用MessageBus
            enable_state_manager: 是否启用StateManager
        """
        self.enable_message_bus = enable_message_bus
        self.enable_state_manager = enable_state_manager

        # 初始化MessageBus
        if enable_message_bus:
            self.message_bus = get_message_bus()
            logger.info("[Environment] MessageBus已启用")
        else:
            self.message_bus = None

        # 初始化StateManager
        if enable_state_manager:
            self.state_manager = StateManager(redis_client=redis_client)
            logger.info("[Environment] StateManager已启用")
        else:
            self.state_manager = None

    async def publish_action_event(
        self,
        event_type: MessageType,
        action_name: str,
        extra_data: Optional[Dict[str, Any]] = None
    ) -> None:
        """
        发布Action事件

        Args:
            event_type: 事件类型
            action_name: Action名称
            extra_data: 额外数据
        """
        if not self.enable_message_bus or not self.message_bus:
            return

        content = {
            "action": action_name,
            **(extra_data or {})
        }

        await self.message_bus.publish(Message(
            topic=event_type.value,
            sender="langgraph",
            content=content
        ))

    async def update_conversation_state(
        self,
        conversation_id: str,
        updates: Dict[str, Any],
        persist_to_redis: bool = True
    ) -> None:
        """
        更新会话状态

        Args:
            conversation_id: 会话ID
            updates: 要更新的字段
            persist_to_redis: 是否持久化到Redis
        """
        if not self.enable_state_manager or not self.state_manager:
            return

        await self.state_manager.update_state(
            conversation_id,
            updates,
            persist_to_redis=persist_to_redis
        )

    async def get_conversation_state(
        self,
        conversation_id: str
    ) -> Dict[str, Any]:
        """
        获取会话状态

        Args:
            conversation_id: 会话ID

        Returns:
            状态字典
        """
        if not self.enable_state_manager or not self.state_manager:
            return {}

        return await self.state_manager.get_state(conversation_id)

    def with_action_tracking(
        self,
        action_name: str,
        conversation_id_key: str = "conversation_id"
    ):
        """
        Action执行追踪装饰器

        自动发布Action开始/完成/失败事件

        Args:
            action_name: Action名称
            conversation_id_key: state中conversation_id的键名

        Example:
            @helper.with_action_tracking("writing")
            async def _handle_writing(self, state: AgentState) -> AgentState:
                # ... 处理逻辑
                return state
        """
        def decorator(func: Callable):
            @wraps(func)
            async def wrapper(self_or_state, *args, **kwargs):
                # 判断是否是方法调用
                if hasattr(self_or_state, '__dict__') and len(args) > 0:
                    # 类方法调用: self, state, ...
                    state = args[0]
                else:
                    # 函数调用: state, ...
                    state = self_or_state

                conversation_id = state.get(conversation_id_key, "unknown")

                # 发布开始事件
                await self.publish_action_event(
                    MessageType.ACTION_STARTED,
                    action_name,
                    {"conversation_id": conversation_id}
                )

                try:
                    # 执行原函数
                    result = await func(self_or_state, *args, **kwargs)

                    # 发布完成事件
                    await self.publish_action_event(
                        MessageType.ACTION_COMPLETED,
                        action_name,
                        {
                            "conversation_id": conversation_id,
                            "status": ActionStatus.COMPLETED.value
                        }
                    )

                    return result

                except Exception as e:
                    # 发布失败事件
                    await self.publish_action_event(
                        MessageType.ACTION_FAILED,
                        action_name,
                        {
                            "conversation_id": conversation_id,
                            "error": str(e)
                        }
                    )
                    raise

            return wrapper
        return decorator


# 全局助手实例(可选)
_global_helper: Optional[LangGraphEnvironmentHelper] = None


def get_environment_helper(
    redis_client: Optional[Any] = None,
    enable_message_bus: bool = True,
    enable_state_manager: bool = True
) -> LangGraphEnvironmentHelper:
    """
    获取全局Environment助手

    Args:
        redis_client: Redis客户端(仅首次调用有效)
        enable_message_bus: 是否启用MessageBus
        enable_state_manager: 是否启用StateManager

    Returns:
        LangGraphEnvironmentHelper实例
    """
    global _global_helper

    if _global_helper is None:
        _global_helper = LangGraphEnvironmentHelper(
            redis_client=redis_client,
            enable_message_bus=enable_message_bus,
            enable_state_manager=enable_state_manager
        )
        logger.info("[Environment] 创建全局Helper实例")

    return _global_helper


def reset_environment_helper() -> None:
    """重置全局Helper(主要用于测试)"""
    global _global_helper
    _global_helper = None
    logger.info("[Environment] 重置全局Helper实例")
