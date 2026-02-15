"""
Actions模块 - ARE架构的Action层

提供统一的Action接口和注册机制
"""

from .base_action import (
    BaseAction,
    ActionResult,
    ActionStatus,
    CompositeAction
)
from .action_registry import (
    ActionRegistry,
    register_action
)
from .echo_action import EchoAction
from .writing_action import WritingAction
from .planning_action import PlanningAction
from .analysis_action import AnalysisAction
from .stuck_action import StuckAction
from .general_chat_action import GeneralChatAction

__all__ = [
    # 基类和结果
    "BaseAction",
    "ActionResult",
    "ActionStatus",
    "CompositeAction",

    # 注册机制
    "ActionRegistry",
    "register_action",

    # 具体Action
    "EchoAction",
    "WritingAction",
    "PlanningAction",
    "AnalysisAction",
    "StuckAction",
    "GeneralChatAction",
]
