"""
ActionRegistry - Action注册表

ARE架构的核心组件之一
负责管理和注册所有可用的Action
"""

from typing import Dict, Optional, Type, Any
from .base_action import BaseAction
import logging
from app.utils.datetime_utils import get_utc_now

logger = logging.getLogger(__name__)


class ActionRegistry:
    """
    Action注册表 - 管理所有可用的Action

    使用场景:
    1. 自动注册Action(通过装饰器)
    2. 按名称查找Action
    3. 创建Action实例
    4. 列出所有可用Action

    示例:
    ```python
    # 方式1: 使用装饰器自动注册
    @register_action("writing")
    class WritingAction(BaseAction):
        pass

    # 方式2: 手动注册
    ActionRegistry.register(WritingAction, "writing")

    # 使用
    action_class = ActionRegistry.get_action("writing")
    action = ActionRegistry.create_action("writing", ai_service, prompt_library)
    ```
    """

    # 类变量: 存储所有注册的Action
    _actions: Dict[str, Type[BaseAction]] = {}
    _action_metadata: Dict[str, Dict[str, Any]] = {}

    @classmethod
    def register(
        cls,
        action_class: Type[BaseAction],
        name: Optional[str] = None,
        category: Optional[str] = None,
        metadata: Optional[Dict[str, Any]] = None
    ):
        """
        注册一个Action

        Args:
            action_class: Action类(必须继承自BaseAction)
            name: Action名称(如果不提供,使用类名)
            category: Action分类(如: writing, planning, analysis等)
            metadata: 额外的元数据

        Raises:
            TypeError: 如果action_class不是BaseAction的子类
        """
        # 验证类型
        if not issubclass(action_class, BaseAction):
            raise TypeError(
                f"Action类必须继承自BaseAction, 但得到: {action_class.__name__}"
            )

        # 确定名称
        action_name = name or action_class.__name__

        # 注册Action
        cls._actions[action_name] = action_class

        # 保存元数据
        cls._action_metadata[action_name] = {
            "class_name": action_class.__name__,
            "category": category,
            "metadata": metadata or {},
            "registered_at": str(__import__("datetime").get_utc_now())
        }

        logger.info(
            f"[ActionRegistry] 注册Action: {action_name} "
            f"(class={action_class.__name__}, category={category})"
        )

    @classmethod
    def unregister(cls, name: str) -> bool:
        """
        注销一个Action

        Args:
            name: Action名称

        Returns:
            bool: 是否成功注销
        """
        if name in cls._actions:
            del cls._actions[name]
            if name in cls._action_metadata:
                del cls._action_metadata[name]
            logger.info(f"[ActionRegistry] 注销Action: {name}")
            return True
        return False

    @classmethod
    def get_action(cls, name: str) -> Optional[Type[BaseAction]]:
        """
        获取Action类

        Args:
            name: Action名称

        Returns:
            Type[BaseAction] | None: Action类,如果不存在返回None
        """
        return cls._actions.get(name)

    @classmethod
    def has_action(cls, name: str) -> bool:
        """
        检查Action是否已注册

        Args:
            name: Action名称

        Returns:
            bool: 是否存在
        """
        return name in cls._actions

    @classmethod
    def list_actions(cls, category: Optional[str] = None) -> Dict[str, Type[BaseAction]]:
        """
        列出所有Action

        Args:
            category: 可选的分类过滤

        Returns:
            Dict[str, Type[BaseAction]]: Action字典
        """
        if category is None:
            return cls._actions.copy()

        # 按分类过滤
        filtered = {}
        for name, action_class in cls._actions.items():
            if cls._action_metadata.get(name, {}).get("category") == category:
                filtered[name] = action_class
        return filtered

    @classmethod
    def get_metadata(cls, name: str) -> Optional[Dict[str, Any]]:
        """
        获取Action的元数据

        Args:
            name: Action名称

        Returns:
            Dict | None: 元数据
        """
        return cls._action_metadata.get(name)

    @classmethod
    def list_categories(cls) -> list[str]:
        """
        列出所有分类

        Returns:
            list[str]: 分类列表
        """
        categories = set()
        for metadata in cls._action_metadata.values():
            if metadata.get("category"):
                categories.add(metadata["category"])
        return sorted(list(categories))

    @classmethod
    def create_action(cls, name: str, *args, **kwargs) -> Optional[BaseAction]:
        """
        创建Action实例

        Args:
            name: Action名称
            *args: 传递给Action构造函数的位置参数
            **kwargs: 传递给Action构造函数的关键字参数

        Returns:
            BaseAction | None: Action实例,如果Action不存在返回None
        """
        action_class = cls.get_action(name)
        if action_class is None:
            logger.warning(f"[ActionRegistry] Action未找到: {name}")
            return None

        try:
            instance = action_class(*args, **kwargs)
            logger.debug(f"[ActionRegistry] 创建Action实例: {name}")
            return instance
        except Exception as e:
            logger.error(f"[ActionRegistry] 创建Action失败 {name}: {e}", exc_info=True)
            return None

    @classmethod
    def get_registry_info(cls) -> Dict[str, Any]:
        """
        获取注册表信息

        Returns:
            Dict: 包含所有Action的信息
        """
        return {
            "total_actions": len(cls._actions),
            "categories": cls.list_categories(),
            "actions": {
                name: {
                    "class_name": action_class.__name__,
                    "metadata": cls._action_metadata.get(name, {})
                }
                for name, action_class in cls._actions.items()
            }
        }

    @classmethod
    def clear(cls):
        """清空注册表(主要用于测试)"""
        cls._actions.clear()
        cls._action_metadata.clear()
        logger.warning("[ActionRegistry] 注册表已清空")


def register_action(
    name: Optional[str] = None,
    category: Optional[str] = None,
    **metadata
):
    """
    装饰器: 自动注册Action到注册表

    使用方法:
    ```python
    @register_action("writing", category="content_creation")
    class WritingAction(BaseAction):
        def __init__(self, ai_service):
            super().__init__("writing", "处理写作请求")
            self.ai_service = ai_service

        async def execute(self, state):
            # 实现逻辑
            pass
    ```

    Args:
        name: Action名称(可选,默认使用类名)
        category: Action分类(可选)
        **metadata: 额外的元数据

    Returns:
        装饰器函数
    """
    def decorator(action_class: Type[BaseAction]):
        # 注册Action
        ActionRegistry.register(
            action_class=action_class,
            name=name,
            category=category,
            metadata=metadata
        )
        return action_class

    return decorator


# 导出
__all__ = [
    "ActionRegistry",
    "register_action"
]
