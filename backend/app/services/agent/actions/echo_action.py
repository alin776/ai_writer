"""
EchoAction - 最简单的示例Action

用途:
1. 验证Action→LangGraph集成流程
2. 作为新Action开发的参考模板
3. 演示Action的最佳实践
"""

from typing import Dict, Any
from .base_action import BaseAction, ActionResult, ActionStatus
from .action_registry import register_action
from langchain_core.messages import HumanMessage


@register_action("echo", category="example")
class EchoAction(BaseAction):
    """
    回显Action - 最简单的示例

    功能: 回显用户输入的消息
    用途: 验证Action框架和集成流程

    示例:
    ```python
    action = EchoAction()
    state = {
        "messages": [HumanMessage(content="Hello")]
    }
    result = await action.run(state)
    print(result.data["echo"])  # "You said: Hello"
    ```
    """

    def __init__(self):
        """初始化EchoAction"""
        super().__init__("echo", "回显用户输入的消息")

    async def validate_input(self, state: Dict[str, Any]) -> bool:
        """
        验证输入是否有效

        要求:
        - state必须是字典
        - state必须包含messages字段
        - messages至少有一条消息
        """
        if not await super().validate_input(state):
            return False

        # 检查是否有消息
        messages = state.get("messages", [])
        if not messages:
            self.logger.error(f"[{self.name}] state中没有messages")
            return False

        return True

    async def execute(self, state: Dict[str, Any]) -> ActionResult:
        """
        执行回显逻辑

        Args:
            state: AgentState,包含messages字段

        Returns:
            ActionResult: 包含回显消息的结果
        """
        # 获取最后一条用户消息
        messages = state.get("messages", [])
        last_message = messages[-1]

        # 提取消息内容
        if hasattr(last_message, "content"):
            user_input = last_message.content
        else:
            user_input = str(last_message)

        # 构造回显消息
        echo_message = f"You said: {user_input}"

        self.logger.info(f"[{self.name}] 回显: {echo_message}")

        # 返回结果
        return ActionResult(
            status=ActionStatus.COMPLETED,
            data={
                "echo": echo_message,
                "original_input": user_input,
                "message_count": len(messages)
            },
            metadata={
                "action": "echo",
                "input_length": len(user_input)
            }
        )


# 导出
__all__ = ["EchoAction"]
