"""
AnalysisAction - 分析场景Action

负责处理文本分析相关的请求，包括:
- 文本质量分析
- 情节逻辑分析
- 写作风格分析
- 角色分析
"""

from typing import Dict, Any
import logging

from .base_action import BaseAction, ActionResult, ActionStatus
from .action_registry import register_action

logger = logging.getLogger(__name__)


@register_action("analysis", category="analysis")
class AnalysisAction(BaseAction):
    """
    分析场景Action

    功能:
    1. 文本质量分析（语言、风格、节奏）
    2. 情节逻辑分析（连贯性、合理性）
    3. 角色分析（性格、成长、关系）
    4. 支持RAG检索历史分析片段

    示例:
    ```python
    action = AnalysisAction(ai_service)
    state = {
        "messages": [HumanMessage(content="分析第一章的写作质量")],
        "work_id": "work_123",
        "chapter_id": "chapter_456"
    }
    result = await action.run(state)
    ```
    """

    def __init__(self, ai_service, use_chatgpt: bool = False):
        """
        初始化AnalysisAction

        Args:
            ai_service: AI服务实例(HTTPAIService或ChatOpenAI)
            use_chatgpt: 是否使用ChatGPT模式
        """
        super().__init__("analysis", "处理文本分析相关请求")
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
        执行分析逻辑

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
            chapter_id = state.get("chapter_id")
            messages = state.get("messages", [])

            self.logger.info(f"[{self.name}] work_id={work_id}, chapter_id={chapter_id}")

            # 2. 生成系统Prompt
            system_prompt = self._build_system_prompt(work_id, chapter_id)

            # 3. 返回结果
            return ActionResult(
                status=ActionStatus.COMPLETED,
                data={
                    "system_prompt": system_prompt,
                    "agent_type": "analysis"
                },
                metadata={
                    "action": "analysis",
                    "work_id": work_id,
                    "chapter_id": chapter_id
                }
            )

        except Exception as e:
            self.logger.error(f"[{self.name}] 执行失败: {e}", exc_info=True)
            return ActionResult(
                status=ActionStatus.FAILED,
                error=str(e),
                metadata={"action": "analysis"}
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
        return f"""你是专业的文本分析Agent。

【核心能力】
- 文本质量分析（语言表达、修辞手法、文字功底）
- 情节逻辑分析（情节连贯性、因果关系、伏笔照应）
- 写作风格分析（叙事节奏、视角运用、氛围营造）
- 角色分析（人物性格、成长曲线、关系网络）

可用工具：
- analyze_text_tool: 深度分析文本
- get_context_tool: 获取上下文信息
- read_chapter_tool: 读取章节内容
- search_analysis_fragments_tool: 检索历史分析片段（RAG）

当前信息: 作品ID={work_id}, 章节ID={chapter_id}

【分析流程】
1. 理解用户的分析需求（质量/逻辑/风格/角色）
2. 调用工具获取待分析的文本内容
3. 从多个维度进行深入分析
4. 给出专业的分析报告和改进建议

【分析维度】
- 优点：肯定做得好的地方
- 问题：指出存在的不足
- 建议：提供具体的改进方向

帮助用户分析文本质量、逻辑、风格等。根据需要调用工具。"""


# 导出
__all__ = ["AnalysisAction"]
