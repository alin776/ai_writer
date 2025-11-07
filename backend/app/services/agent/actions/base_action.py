"""
BaseAction 基类定义

ARE架构的核心组件 - Action层
负责封装具体的业务逻辑执行
"""

from abc import ABC, abstractmethod
from typing import Dict, Any, Optional
from enum import Enum
from datetime import datetime
import logging

logger = logging.getLogger(__name__)


class ActionStatus(Enum):
    """Action执行状态"""
    PENDING = "pending"          # 待执行
    IN_PROGRESS = "in_progress"  # 执行中
    COMPLETED = "completed"      # 已完成
    FAILED = "failed"            # 失败


class ActionResult:
    """
    Action执行结果

    封装Action执行后的所有信息，包括:
    - 执行状态
    - 返回数据
    - 错误信息
    - 元数据
    - 系统提示词（新架构）
    """

    def __init__(
        self,
        status: ActionStatus,
        data: Any = None,
        error: Optional[str] = None,
        metadata: Optional[Dict[str, Any]] = None,
        system_prompt: Optional[str] = None  # 新增：用于新架构的prepare()方法
    ):
        """
        初始化Action结果

        Args:
            status: 执行状态
            data: 返回数据(可以是任意类型)
            error: 错误信息(仅在失败时使用)
            metadata: 元数据(如执行时间、token用量等)
            system_prompt: 系统提示词(新架构使用，prepare()方法返回)
        """
        self.status = status
        self.data = data
        self.error = error
        self.metadata = metadata or {}
        self.system_prompt = system_prompt  # 新架构：存储准备好的prompt
        self.timestamp = datetime.now()

    def to_dict(self) -> Dict[str, Any]:
        """转换为字典格式"""
        result = {
            "status": self.status.value,
            "data": self.data,
            "error": self.error,
            "metadata": self.metadata,
            "timestamp": str(self.timestamp)
        }
        # 如果有system_prompt，也包含在字典中（新架构）
        if self.system_prompt is not None:
            result["system_prompt"] = self.system_prompt
        return result

    def is_success(self) -> bool:
        """是否执行成功（向后兼容方法）"""
        return self.status == ActionStatus.COMPLETED

    @property
    def success(self) -> bool:
        """
        是否成功（新架构简化属性）

        这是一个便捷属性，等价于 is_success()
        新架构推荐使用此属性进行判断
        """
        return self.status == ActionStatus.COMPLETED

    def __repr__(self) -> str:
        return f"ActionResult(status={self.status.value}, error={self.error})"


class BaseAction(ABC):
    """
    Action基类 - ARE架构的核心组件

    职责:
    1. 封装具体的业务逻辑
    2. 提供统一的执行接口
    3. 处理执行前后的钩子
    4. 统一错误处理

    使用方法:
    ```python
    class MyAction(BaseAction):
        async def execute(self, state: Dict[str, Any]) -> ActionResult:
            # 实现具体逻辑
            return ActionResult(
                status=ActionStatus.COMPLETED,
                data={"result": "success"}
            )

    # 使用
    action = MyAction("my_action", "My Action Description")
    result = await action.run(state)
    ```
    """

    def __init__(self, name: str, description: str):
        """
        初始化Action

        Args:
            name: Action名称(用于标识和日志)
            description: Action描述(用于文档和提示)
        """
        self.name = name
        self.description = description
        self.logger = logging.getLogger(f"Action.{name}")
        self.execution_count = 0
        self.total_duration = 0.0

    async def prepare(self, state: Dict[str, Any]) -> ActionResult:
        """
        准备Action所需的参数和Prompt（新架构方法）

        这是新架构的核心方法，职责：
        1. 从state中提取业务参数
        2. 应用领域知识（如小说阶段判断）
        3. 构建场景化的system prompt
        4. 返回准备好的参数，不调用LLM

        Args:
            state: 当前AgentState,包含:
                - messages: 对话历史
                - work_id: 作品ID
                - chapter_id: 章节ID
                - intent: 用户意图
                - context: 上下文信息
                - agent_steps: 执行步骤

        Returns:
            ActionResult: 包含:
                - success: 是否准备成功
                - system_prompt: 构建好的系统提示词
                - metadata: 业务元数据（如agent_type, phase等）
                - error: 错误信息（如果失败）

        Note:
            - 此方法不应调用LLM
            - 仅负责参数准备和Prompt构建
            - 默认实现返回失败，子类应重写此方法
        """
        return ActionResult(
            status=ActionStatus.FAILED,
            error=f"{self.name}: prepare()方法未实现",
            metadata={"action_name": self.name}
        )

    async def execute(self, state: Dict[str, Any]) -> ActionResult:
        """
        执行Action的核心逻辑（已废弃，建议使用prepare()）

        ⚠️⚠️⚠️ 废弃警告 ⚠️⚠️⚠️
        此方法已被 prepare() 方法替代，将在未来版本中移除。

        新架构说明：
        - prepare()：仅准备参数和Prompt，不调用LLM（推荐）
        - execute()：旧方法，包含LLM调用逻辑（已废弃）

        迁移指南：
        1. 将LLM调用逻辑移到外部（由LangGraph框架处理）
        2. 在prepare()中只做参数提取和Prompt构建
        3. 返回ActionResult，包含system_prompt和metadata

        Args:
            state: 当前AgentState

        Returns:
            ActionResult: 默认返回失败，提示使用prepare()
        """
        logger.warning(f"[{self.name}] execute()方法已废弃，请使用prepare()方法")

        # 尝试调用prepare()作为fallback
        try:
            result = await self.prepare(state)
            if result.status != ActionStatus.FAILED:
                return result
        except Exception as e:
            logger.debug(f"[{self.name}] prepare()调用失败: {e}")

        # 返回错误提示
        return ActionResult(
            status=ActionStatus.FAILED,
            error=f"{self.name}: execute()方法已废弃，请使用prepare()方法",
            metadata={"action_name": self.name, "deprecated": True}
        )

    async def validate_input(self, state: Dict[str, Any]) -> bool:
        """
        验证输入是否有效

        Args:
            state: AgentState

        Returns:
            bool: 是否有效
        """
        # 检查state是否为None
        if state is None:
            self.logger.error(f"[{self.name}] 输入state为None")
            return False

        # 检查state是否为字典
        if not isinstance(state, dict):
            self.logger.error(f"[{self.name}] 无效的输入类型: {type(state)}, 期望dict")
            return False

        return True

    async def before_execute(self, state: Dict[str, Any]):
        """
        执行前的钩子

        可以在子类中重写此方法,实现:
        - 参数预处理
        - 日志记录
        - 性能监控开始
        """
        self.logger.info(f"[{self.name}] 准备执行")
        self.execution_count += 1

    async def after_execute(self, result: ActionResult):
        """
        执行后的钩子

        可以在子类中重写此方法,实现:
        - 结果后处理
        - 日志记录
        - 性能监控结束
        - 事件发布
        """
        self.logger.info(f"[{self.name}] 执行完成: {result.status.value}")

    async def on_error(self, error: Exception) -> ActionResult:
        """
        错误处理钩子

        Args:
            error: 捕获的异常

        Returns:
            ActionResult: 包含错误信息的结果
        """
        self.logger.error(f"[{self.name}] 执行失败: {error}", exc_info=True)
        return ActionResult(
            status=ActionStatus.FAILED,
            error=str(error),
            metadata={
                "error_type": type(error).__name__,
                "action_name": self.name
            }
        )

    async def run(self, state: Dict[str, Any]) -> ActionResult:
        """
        完整的执行流程(模板方法模式)

        执行顺序:
        1. 验证输入
        2. 执行前钩子
        3. 核心执行
        4. 执行后钩子
        5. 错误处理(如果发生异常)

        Args:
            state: AgentState

        Returns:
            ActionResult: 执行结果
        """
        import time
        start_time = time.time()

        try:
            # 1. 验证输入
            if not await self.validate_input(state):
                return ActionResult(
                    status=ActionStatus.FAILED,
                    error="输入验证失败",
                    metadata={"action_name": self.name}
                )

            # 2. 执行前钩子
            await self.before_execute(state)

            # 3. 核心执行
            result = await self.execute(state)

            # 4. 记录执行时间
            duration = time.time() - start_time
            self.total_duration += duration
            result.metadata["duration"] = duration
            result.metadata["action_name"] = self.name

            # 5. 执行后钩子
            await self.after_execute(result)

            return result

        except Exception as e:
            # 错误处理
            result = await self.on_error(e)
            result.metadata["duration"] = time.time() - start_time
            return result

    def get_stats(self) -> Dict[str, Any]:
        """
        获取Action执行统计

        Returns:
            Dict: 统计信息
        """
        return {
            "name": self.name,
            "description": self.description,
            "execution_count": self.execution_count,
            "total_duration": self.total_duration,
            "avg_duration": (
                self.total_duration / self.execution_count
                if self.execution_count > 0
                else 0
            )
        }

    def __repr__(self) -> str:
        return f"<{self.__class__.__name__}(name='{self.name}')>"


class CompositeAction(BaseAction):
    """
    组合Action - 可以包含多个子Action

    用于实现复杂的业务流程,将多个Action组合执行
    """

    def __init__(self, name: str, description: str, actions: list[BaseAction] = None):
        """
        初始化组合Action

        Args:
            name: Action名称
            description: Action描述
            actions: 子Action列表
        """
        super().__init__(name, description)
        self.actions = actions or []

    def add_action(self, action: BaseAction):
        """添加子Action"""
        self.actions.append(action)

    async def execute(self, state: Dict[str, Any]) -> ActionResult:
        """
        顺序执行所有子Action

        如果任何一个子Action失败,则停止执行并返回失败结果
        """
        results = []

        for action in self.actions:
            result = await action.run(state)
            results.append(result)

            # 如果失败,停止执行
            if not result.is_success():
                return ActionResult(
                    status=ActionStatus.FAILED,
                    error=f"子Action '{action.name}' 执行失败: {result.error}",
                    metadata={
                        "failed_action": action.name,
                        "sub_results": [r.to_dict() for r in results]
                    }
                )

            # 更新state(如果子Action返回了新数据)
            if result.data and isinstance(result.data, dict):
                state.update(result.data)

        # 所有子Action都成功
        return ActionResult(
            status=ActionStatus.COMPLETED,
            data={"sub_results": [r.to_dict() for r in results]},
            metadata={
                "action_count": len(self.actions),
                "all_succeeded": True
            }
        )


# 导出
__all__ = [
    "BaseAction",
    "ActionResult",
    "ActionStatus",
    "CompositeAction"
]
