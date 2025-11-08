"""
GeneralChatAction - 一般对话Action

负责处理一般对话请求，包括:
- 普通问答
- 闲聊对话
- 使用说明
- 功能介绍
"""

from typing import Dict, Any
import logging
from langchain_core.messages import AIMessage

from .base_action import BaseAction, ActionResult, ActionStatus
from .action_registry import register_action

logger = logging.getLogger(__name__)


@register_action("general_chat", category="conversation")
class GeneralChatAction(BaseAction):
    """
    一般对话Action

    功能:
    1. 处理普通对话请求
    2. 友好、简洁的回复
    3. 提供功能引导
    4. 无需工具调用

    示例:
    ```python
    action = GeneralChatAction(ai_service)
    state = {
        "messages": [HumanMessage(content="你好")]
    }
    result = await action.run(state)
    ```
    """

    def __init__(self):
        """
        初始化GeneralChatAction

        注意：新架构不需要ai_service参数，Action只负责准备参数
        """
        super().__init__("general_chat", "处理一般对话请求")

    async def prepare(self, state: Dict[str, Any]) -> ActionResult:
        """
        准备一般对话的参数和Prompt（新架构方法）

        职责：
        1. 验证输入（检查messages）
        2. 构建系统提示词
        3. 返回准备好的参数，不调用LLM

        Args:
            state: AgentState，至少包含messages字段

        Returns:
            ActionResult: 包含system_prompt和metadata
        """
        try:
            # 1. 验证输入
            messages = state.get("messages", [])
            if not messages:
                return ActionResult(
                    status=ActionStatus.FAILED,
                    error="state中没有messages",
                    metadata={"action": "general_chat"}
                )

            self.logger.info(f"[{self.name}] 准备一般对话，历史消息数: {len(messages)}")

            # 2. 构建系统提示词
            system_prompt = self._build_system_prompt()

            # 3. 返回准备好的参数
            return ActionResult(
                status=ActionStatus.COMPLETED,
                system_prompt=system_prompt,
                metadata={
                    "agent_type": "general",
                    "action": "general_chat",
                    "message_count": len(messages)
                }
            )

        except Exception as e:
            self.logger.error(f"[{self.name}] prepare()失败: {e}", exc_info=True)
            return ActionResult(
                status=ActionStatus.FAILED,
                error=str(e),
                metadata={"action": "general_chat"}
            )

    async def validate_input(self, state: Dict[str, Any]) -> bool:
        """
        验证输入是否有效

        要求:
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

    def _build_system_prompt(self) -> str:
        """
        构建系统Prompt

        Returns:
            str: 系统Prompt
        """
        return """你是友好的AI写作助手，以专业、简洁的方式回复用户。

【你的特点】
- 友好、专业、有耐心
- 简洁明了，避免冗长
- 善于引导用户使用功能

【你能做什么】
- 写作：帮助用户续写、创作小说内容
- 规划：协助规划世界观、角色、大纲
- 分析：分析文本质量、逻辑、风格
- 卡文：提供创作方向和灵感

【回复原则】
- 如果用户在闲聊，友好回应
- 如果用户询问功能，简洁介绍
- 如果用户需要帮助，引导到具体功能
- 保持简洁，不要过于啰嗦"""


# 导出
__all__ = ["GeneralChatAction"]
