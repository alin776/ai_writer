"""
StuckAction - 卡文处理Action

负责处理卡文相关的请求，包括:
- 创作瓶颈突破
- 情节发展建议
- 多方向创作提示
- 创意激发
"""

from typing import Dict, Any
import logging

from .base_action import BaseAction, ActionResult, ActionStatus
from .action_registry import register_action

logger = logging.getLogger(__name__)


@register_action("stuck", category="writing_assistance")
class StuckAction(BaseAction):
    """
    卡文处理Action

    功能:
    1. 诊断卡文原因
    2. 提供多个创作方向
    3. 激发创作灵感
    4. 支持RAG检索相关灵感

    示例:
    ```python
    action = StuckAction(ai_service)
    state = {
        "messages": [HumanMessage(content="我在写第五章时卡住了，不知道怎么继续")],
        "work_id": "work_123",
        "chapter_id": "chapter_456"
    }
    result = await action.run(state)
    ```
    """

    def __init__(self):
        """
        初始化StuckAction

        注意：新架构不需要ai_service参数，Action只负责准备参数
        """
        super().__init__("stuck", "处理卡文相关请求")

        # 新增：初始化 PromptManager
        from app.prompts import get_prompt_manager
        self.prompt_manager = get_prompt_manager()
        self.logger.info(f"[{self.name}] PromptManager已初始化")

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

    async def prepare(self, state: Dict[str, Any]) -> ActionResult:
        """
        准备卡文处理场景的参数和Prompt（新架构方法）

        职责：
        1. 提取上下文信息
        2. 构建系统Prompt
        3. 返回准备好的参数，不调用LLM

        Args:
            state: AgentState

        Returns:
            ActionResult: 包含system_prompt和metadata
        """
        try:
            # 1. 提取上下文
            work_id = state.get("work_id")
            chapter_id = state.get("chapter_id")
            messages = state.get("messages", [])

            self.logger.info(f"[{self.name}] work_id={work_id}, chapter_id={chapter_id}")

            # 2. 生成系统Prompt
            system_prompt = self._build_system_prompt(work_id, chapter_id)

            # 3. 返回准备好的参数
            return ActionResult(
                status=ActionStatus.COMPLETED,
                system_prompt=system_prompt,  # 新架构：使用system_prompt参数
                metadata={
                    "agent_type": "stuck",
                    "action": "stuck",
                    "work_id": work_id,
                    "chapter_id": chapter_id
                }
            )

        except Exception as e:
            self.logger.error(f"[{self.name}] prepare()失败: {e}", exc_info=True)
            return ActionResult(
                status=ActionStatus.FAILED,
                error=str(e),
                metadata={"action": "stuck"}
            )

    def _build_system_prompt(
        self,
        work_id: str = None,
        chapter_id: str = None
    ) -> str:
        """
        构建系统Prompt

        Args:
            work_id: 作品ID
            chapter_id: 章节ID

        Returns:
            str: 系统Prompt
        """
        return f"""你是专业的写作指导Agent，擅长帮助作者突破创作瓶颈。

【核心能力】
- 诊断卡文原因（情节、角色、节奏、逻辑）
- 提供多个创作方向（3-5个具体建议）
- 激发创作灵感（参考类似作品、经典桥段）
- 尝试续写示例（展示可能的发展方向）

可用工具：
- get_context_tool: 获取当前创作背景
- read_chapter_tool: 读取已写章节
- search_analysis_fragments_tool: 检索相关创作灵感和分析（RAG）
- analyze_text_tool: 分析现有内容
- continue_writing_tool: 尝试续写方向

当前信息: 作品ID={work_id}, 章节ID={chapter_id}

【工作流程】
1. 理解用户卡文的具体情况
2. 调用工具获取创作背景和已有内容
3. 分析可能的卡文原因
4. 提供3-5个具体的创作方向建议

【建议格式】
每个建议应包含：
- 方向标题（简洁明了）
- 具体做法（操作步骤）
- 预期效果（这样写的好处）
- 示例片段（可选，展示效果）

【注意事项】
- 建议要具体可执行，不要泛泛而谈
- 要基于现有内容，保持连贯性
- 考虑作品类型和风格
- 给予鼓励和信心

帮助卡文的用户突破瓶颈，提供多个创作方向建议。根据需要调用工具。"""


# 导出
__all__ = ["StuckAction"]
