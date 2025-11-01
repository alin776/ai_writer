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

    def __init__(self, ai_service):
        """
        初始化GeneralChatAction

        Args:
            ai_service: AI服务实例(HTTPAIService)
        """
        super().__init__("general_chat", "处理一般对话请求")
        self.ai_service = ai_service

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

    async def execute(self, state: Dict[str, Any]) -> ActionResult:
        """
        执行一般对话逻辑

        主要流程:
        1. 提取用户消息
        2. 构建对话Prompt
        3. 调用AI服务生成回复
        4. 返回结果

        Args:
            state: AgentState

        Returns:
            ActionResult: 执行结果
        """
        try:
            # 1. 提取用户消息
            messages = state.get("messages", [])
            last_message = messages[-1].content if messages else ""

            self.logger.info(f"[{self.name}] 处理一般对话: {last_message[:50]}...")

            # 2. 构建Prompt
            system_prompt = self._build_system_prompt()
            prompt = f"""{system_prompt}

用户消息：{last_message}

请回复："""

            # 3. 调用AI服务生成回复
            response_text = ""
            async for chunk, _ in self.ai_service._stream_chat(
                messages=[{"role": "user", "content": prompt}],
                max_tokens=500,
                temperature=0.7
            ):
                if chunk:
                    response_text += chunk

            self.logger.info(f"[{self.name}] 生成回复: {response_text[:50]}...")

            # 4. 构造AI消息
            ai_message = AIMessage(content=response_text)

            # 5. 返回结果
            return ActionResult(
                status=ActionStatus.COMPLETED,
                data={
                    "messages": [ai_message],
                    "final_response": response_text
                },
                metadata={
                    "action": "general_chat",
                    "input_length": len(last_message),
                    "output_length": len(response_text)
                }
            )

        except Exception as e:
            self.logger.error(f"[{self.name}] 执行失败: {e}", exc_info=True)
            return ActionResult(
                status=ActionStatus.FAILED,
                error=str(e),
                metadata={"action": "general_chat"}
            )

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
