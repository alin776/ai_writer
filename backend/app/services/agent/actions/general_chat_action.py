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

    def __init__(self, ai_service=None):
        """
        初始化GeneralChatAction

        Args:
            ai_service: AI服务实例(HTTPAIService) - 可选，新架构中不再需要
        """
        super().__init__("general_chat", "处理一般对话请求")
        self.ai_service = ai_service  # 向后兼容，新架构不使用

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

    async def execute(self, state: Dict[str, Any]) -> ActionResult:
        """
        执行一般对话逻辑（旧架构方法）

        ⚠️ TODO: 迁移到prepare()后删除此方法

        这是旧架构的execute()方法，会直接调用LLM。
        新架构使用prepare()方法替代，仅准备参数不调用LLM。

        保留此方法仅为向后兼容，待所有Action迁移完成后删除。

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
            # 1. 提取所有消息历史
            messages = state.get("messages", [])

            self.logger.info(f"[{self.name}] 处理一般对话，历史消息数: {len(messages)}")

            # 2. 转换消息格式：LangChain消息 -> AI服务消息
            from langchain_core.messages import HumanMessage, AIMessage

            chat_messages = []

            # 先添加系统提示
            system_prompt = self._build_system_prompt()
            chat_messages.append({"role": "system", "content": system_prompt})

            # 转换历史消息
            for msg in messages:
                if isinstance(msg, HumanMessage):
                    chat_messages.append({"role": "user", "content": msg.content})
                elif isinstance(msg, AIMessage):
                    chat_messages.append({"role": "assistant", "content": msg.content})

            self.logger.info(f"[{self.name}] 传入AI的消息数: {len(chat_messages)} (含system)")

            # 3. 调用AI服务生成回复
            from app.services.agent.model_selector import TaskType
            response_text = ""
            async for chunk, _ in self.ai_service._stream_chat(
                messages=chat_messages,  # ✅ 传入完整历史
                max_tokens=500,
                temperature=0.7,
                task_type=TaskType.SIMPLE_QA  # 一般对话任务，使用flash
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
                    "input_length": len(messages[-1].content) if messages else 0,
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
