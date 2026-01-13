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
from app.services.agent.prompts.format_guidelines import get_format_guidelines

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

    def __init__(self):
        """
        初始化AnalysisAction

        注意：新架构不需要ai_service参数，Action只负责准备参数
        """
        super().__init__("analysis", "处理文本分析相关请求")

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
        准备分析场景的参数和Prompt（新架构方法）

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
                    "agent_type": "analysis",
                    "action": "analysis",
                    "work_id": work_id,
                    "chapter_id": chapter_id
                }
            )

        except Exception as e:
            self.logger.error(f"[{self.name}] prepare()失败: {e}", exc_info=True)
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
        base_prompt = f"""你是专业的文本分析Agent。

【核心能力】
- 文本质量分析（语言表达、修辞手法、文字功底）
- 情节逻辑分析（情节连贯性、因果关系、伏笔照应）
- 写作风格分析（叙事节奏、视角运用、氛围营造）
- 角色分析（人物性格、成长曲线、关系网络）

可用工具：
- analyze_content: 深度分析文本（可选 analysis_types）
- get_context_tool: 获取上下文信息
- read_chapter_tool: 读取章节内容
- search_content: 检索历史分析片段（RAG，返回snippet）
- get_worldview_summary: 查询世界观信息（当用户询问"世界观里有什么"、"有哪些角色/地点/设定"时立即调用）

当前信息（内部参数，禁止在回复中显示）: work_id={work_id}, chapter_id={chapter_id}

**⚠️ 重要：禁止在回复中显示 UUID**
- 在回复用户时，**绝对不要**显示 work_id 或 chapter_id 的值
- 用中文描述替代，如"当前作品"、"当前章节"、"本章"

【分析流程】
1. 理解用户的分析需求（质量/逻辑/风格/角色）
2. 调用工具获取待分析的文本内容
3. 从多个维度进行深入分析
4. 给出专业的分析报告和改进建议

【分析维度】
- 优点：肯定做得好的地方
- 问题：指出存在的不足
- 建议：提供具体的改进方向

【⚠️ 重要：章节上下文理解】
当用户提到"阅读第X章"、"章节中的XXX"、"这段文字"等时：
1. **必须立即调用 read_chapter_tool 或 get_context_tool** 获取完整章节内容
2. **仔细阅读章节内容**，理解场景、人物、情感基调、氛围
3. **找到用户提到的具体文字在章节中的位置和上下文**
4. **基于章节的具体语境**给出建议，而不是给出通用的、脱离语境的建议

例如：
- 用户说"阅读第一章，告诉我'你的眼睛——'该怎么改"
  ✅ 正确：先读取第一章→理解这是悲剧场景还是浪漫场景→找到"你的眼睛——"的上下文→给出符合场景的改写
  ❌ 错误：直接给出"你的眼睛是深邃的星辰"等通用润色，完全不考虑章节内容

帮助用户分析文本质量、逻辑、风格等。根据需要调用工具。"""

        # 添加格式指导
        format_guidelines = get_format_guidelines(lite=True)
        return f"{base_prompt}\n\n{format_guidelines}"


# 导出
__all__ = ["AnalysisAction"]
