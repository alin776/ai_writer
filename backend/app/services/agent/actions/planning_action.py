"""
PlanningAction - 规划场景Action

负责处理小说规划相关的请求，包括:
- 大纲规划
- 世界观设定
- 角色设定
- 情节设计
"""

from typing import Dict, Any
import logging

from .base_action import BaseAction, ActionResult, ActionStatus
from .action_registry import register_action

logger = logging.getLogger(__name__)


@register_action("planning", category="planning")
class PlanningAction(BaseAction):
    """
    规划场景Action

    功能:
    1. 处理小说规划请求
    2. 支持大纲、世界观、角色设定等规划
    3. 集成RAG检索相关分析片段
    4. 支持工具调用

    示例:
    ```python
    action = PlanningAction(ai_service)
    state = {
        "messages": [HumanMessage(content="帮我规划一个玄幻小说的世界观")],
        "work_id": "work_123"
    }
    result = await action.run(state)
    ```
    """

    def __init__(self, ai_service, use_chatgpt: bool = False):
        """
        初始化PlanningAction

        Args:
            ai_service: AI服务实例(HTTPAIService或ChatOpenAI)
            use_chatgpt: 是否使用ChatGPT模式
        """
        super().__init__("planning", "处理小说规划相关请求")
        self.ai_service = ai_service
        self.use_chatgpt = use_chatgpt

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
        执行规划逻辑

        主要流程:
        1. 提取上下文信息
        2. 生成系统Prompt
        3. 返回结果(实际工具调用由LangGraph处理)

        Args:
            state: AgentState

        Returns:
            ActionResult: 执行结果
        """
        try:
            # 1. 提取上下文
            work_id = state.get("work_id")
            messages = state.get("messages", [])

            self.logger.info(f"[{self.name}] work_id={work_id}")

            # 2. 生成系统Prompt
            system_prompt = self._build_system_prompt(work_id)

            # 3. 返回结果
            return ActionResult(
                status=ActionStatus.COMPLETED,
                data={
                    "system_prompt": system_prompt,
                    "agent_type": "planning"
                },
                metadata={
                    "action": "planning",
                    "work_id": work_id
                }
            )

        except Exception as e:
            self.logger.error(f"[{self.name}] 执行失败: {e}", exc_info=True)
            return ActionResult(
                status=ActionStatus.FAILED,
                error=str(e),
                metadata={"action": "planning"}
            )

    def _build_system_prompt(self, work_id: str = None) -> str:
        """
        构建系统Prompt

        Args:
            work_id: 作品ID

        Returns:
            str: 系统Prompt
        """
        return f"""你是专业的规划助手Agent。

【核心能力】
- 小说大纲规划（章节结构、情节走向）
- 世界观设定（体系、规则、背景）
- 角色设定（主角、配角、反派）
- 情节设计（冲突、转折、高潮）

可用工具：
- get_context_tool: 获取作品信息
- read_chapter_tool: 读取已有章节内容
- search_analysis_fragments_tool: 检索相关分析片段（RAG）
- analyze_text_tool: 分析现有内容

当前作品ID: {work_id}

【工作流程】
1. 理解用户的规划需求（大纲/世界观/角色/情节）
2. 调用工具获取必要的上下文信息
3. 基于现有信息提供专业的规划建议
4. 确保规划的逻辑性和可执行性

帮助用户规划小说创作，包括世界观、角色、大纲等。根据需要调用工具。"""


# 导出
__all__ = ["PlanningAction"]
