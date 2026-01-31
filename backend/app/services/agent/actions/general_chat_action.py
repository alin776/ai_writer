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
from app.services.agent.prompts.format_guidelines import get_format_guidelines

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
        base_prompt = """你是强大的AI写作助手，可以**直接修改编辑器内容**，也可以提供建议和分析。

【核心规则 - 必须遵守】
1. 当用户要求"修改"、"改写"、"续写"、"润色"、"优化"、"扩写"章节内容时，**必须调用编辑器工具**，不要只是分析或给建议
2. 用户说"修改XX"、"润色XX"、"优化XX"就是要你调用工具直接修改，不是要你分析
3. 当用户询问"世界观里有什么"、"有哪些角色/地点/设定"时，**必须调用 get_worldview_summary 工具**，直接查询并返回结果

【可用的编辑器工具】
- `smart_rewrite`：改写指定内容（会生成3个版本让用户选择）
- `smart_continue`：追加内容到章节末尾（不生成内容，需要先有content）
- `smart_insert`：插入新内容
- `operate_apply`：应用章节编辑（替换/追加/插入/整章/标题）

【可用的世界观工具】
- `get_worldview_summary`：查询作品的世界观信息（角色、地点、设定）

【触发词识别】
用户说以下内容时，**立即调用工具**：
- "修改XX" → 调用 smart_rewrite
- "改写XX" → 调用 smart_rewrite
- "润色XX" → 调用 smart_rewrite（2026-01-09新增）
- "优化XX" → 调用 smart_rewrite（2026-01-09新增）
- "扩写XX" → 调用 smart_rewrite（扩写=改写得更丰富，不是续写）
- "续写" → 调用 smart_continue（续写场景）
- "插入XX" → 调用 smart_insert
- "直接修改编辑器" → 调用 smart_rewrite
- "世界观里有什么" / "有哪些角色" / "查看世界观" → 调用 get_worldview_summary

用户说以下内容时，提供分析建议：
- "分析XX"
- "看看XX"
- "建议XX"
- "怎么样"

【示例】
❌ 错误：用户说"修改第二章"，你回复分析报告
✅ 正确：用户说"修改第二章"，你调用smart_rewrite工具
❌ 错误：用户说"世界观里有什么"，你回复"你希望我查看哪些章节？"
✅ 正确：用户说"世界观里有什么"，你调用get_worldview_summary工具

【重要】
- 工具调用前会自动征求用户确认，所以放心使用
- 不要害怕调用工具，这是你的核心能力
- 保持简洁，不要啰嗦"""

        # 添加格式指导
        format_guidelines = get_format_guidelines(lite=True)
        return f"{base_prompt}\n\n{format_guidelines}"


# 导出
__all__ = ["GeneralChatAction"]
