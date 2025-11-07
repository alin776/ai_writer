"""
WritingAction - 写作场景Action

负责处理写作相关的所有请求，包括:
- 章节续写
- 内容润色
- 写作指导
- 阶段性写作优化
"""

from typing import Dict, Any, Optional
import re
import logging
from langchain_core.messages import AIMessage, SystemMessage

from .base_action import BaseAction, ActionResult, ActionStatus
from .action_registry import register_action
from app.services.agent.prompts import PhaseCharacteristics, NovelPhase
from app.services.agent.prompt_library import get_content_prompt

logger = logging.getLogger(__name__)


@register_action("writing", category="content_creation")
class WritingAction(BaseAction):
    """
    写作场景Action

    功能:
    1. 识别章节号和创作阶段
    2. 使用阶段性Prompt优化
    3. 集成AI服务生成内容
    4. 支持工具调用(通过LangGraph)

    示例:
    ```python
    action = WritingAction(ai_service, prompt_library)
    state = {
        "messages": [HumanMessage(content="续写第一章")],
        "work_id": "work_123",
        "chapter_id": "chapter_456"
    }
    result = await action.run(state)
    ```
    """

    def __init__(self, ai_service=None, use_chatgpt: bool = False):
        """
        初始化WritingAction

        Args:
            ai_service: AI服务实例(HTTPAIService或ChatOpenAI) - 可选，新架构不需要
            use_chatgpt: 是否使用ChatGPT模式（已废弃，保留兼容）
        """
        super().__init__("writing", "处理写作相关请求")
        self.ai_service = ai_service  # 向后兼容，新架构不使用
        self.use_chatgpt = use_chatgpt  # 向后兼容

        # 🔧 新增：初始化 PromptManager
        from app.prompts import get_prompt_manager
        self.prompt_manager = get_prompt_manager()
        logger.info("[WritingAction] PromptManager已初始化")

    async def prepare(self, state: Dict[str, Any]) -> ActionResult:
        """
        准备写作场景的参数和Prompt（新架构方法）

        职责：
        1. 识别章节号和创作阶段（业务逻辑）
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

            # 2. 识别章节和阶段（核心业务逻辑）
            last_message = messages[-1].content if messages else ""
            phase, chapter_num = self._detect_phase(last_message)

            self.logger.info(
                f"[{self.name}] work_id={work_id}, chapter_id={chapter_id}, "
                f"phase={phase.value if phase else None}, chapter_num={chapter_num}"
            )

            # 3. 生成系统Prompt
            system_prompt = self._build_system_prompt(
                phase=phase,
                chapter_num=chapter_num,
                work_id=work_id,
                chapter_id=chapter_id
            )

            # 4. 返回准备好的参数
            return ActionResult(
                status=ActionStatus.COMPLETED,
                system_prompt=system_prompt,  # 新架构：使用system_prompt参数
                metadata={
                    "agent_type": "writing",
                    "action": "writing",
                    "phase": phase.value if phase else None,
                    "chapter_num": chapter_num,
                    "work_id": work_id,
                    "chapter_id": chapter_id
                }
            )

        except Exception as e:
            self.logger.error(f"[{self.name}] prepare()失败: {e}", exc_info=True)
            return ActionResult(
                status=ActionStatus.FAILED,
                error=str(e),
                metadata={"action": "writing"}
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
        执行写作逻辑（旧架构方法）

        ⚠️ TODO: 迁移到prepare()后删除此方法

        这是旧架构的execute()方法，虽然不直接调用LLM，但会被run()包装。
        新架构使用prepare()方法替代，语义更清晰。

        保留此方法仅为向后兼容，待所有Action迁移完成后删除。

        主要流程:
        1. 提取上下文信息(work_id, chapter_id)
        2. 识别章节号和创作阶段
        3. 生成系统Prompt(使用阶段优化)
        4. 返回结果

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

            # 2. 识别章节和阶段
            last_message = messages[-1].content if messages else ""
            phase, chapter_num = self._detect_phase(last_message)

            self.logger.info(
                f"[{self.name}] work_id={work_id}, chapter_id={chapter_id}, "
                f"phase={phase.value if phase else None}, chapter_num={chapter_num}"
            )

            # 3. 生成系统Prompt
            system_prompt = self._build_system_prompt(
                phase=phase,
                chapter_num=chapter_num,
                work_id=work_id,
                chapter_id=chapter_id
            )

            # 4. 生成响应
            # 注意: 这里只生成Prompt和AIMessage
            # 实际的工具调用由LangGraph的_handle_agent_with_tools处理
            response_message = AIMessage(
                content="",  # 内容为空，表示需要LangGraph处理工具调用
                additional_kwargs={
                    "system_prompt": system_prompt,
                    "agent_type": "writing"
                }
            )

            # 5. 返回结果
            return ActionResult(
                status=ActionStatus.COMPLETED,
                data={
                    "system_prompt": system_prompt,
                    "agent_type": "writing",
                    "phase": phase.value if phase else None,
                    "chapter_num": chapter_num
                },
                metadata={
                    "action": "writing",
                    "work_id": work_id,
                    "chapter_id": chapter_id,
                    "phase": phase.value if phase else None,
                    "chapter_num": chapter_num
                }
            )

        except Exception as e:
            self.logger.error(f"[{self.name}] 执行失败: {e}", exc_info=True)
            return ActionResult(
                status=ActionStatus.FAILED,
                error=str(e),
                metadata={"action": "writing"}
            )

    def _detect_phase(self, message: str | int) -> tuple[Optional[NovelPhase], Optional[int]]:
        """
        检测章节阶段

        从用户消息中提取章节号，并根据章节号判断创作阶段

        Args:
            message: 用户消息(字符串)或章节号(整数)

        Returns:
            (phase, chapter_num): 阶段和章节号
        """
        chapter_num = None

        # 处理整数输入(直接传入章节号)
        if isinstance(message, int):
            chapter_num = message
            self.logger.info(f"[{self.name}] 直接输入章节号: {chapter_num}")
        # 处理字符串输入(从消息中提取章节号)
        elif isinstance(message, str):
            chapter_match = re.search(r'第(\d+)章|chapter\s*(\d+)', message, re.IGNORECASE)
            if chapter_match:
                chapter_num = int(chapter_match.group(1) or chapter_match.group(2))
                self.logger.info(f"[{self.name}] 从消息中识别到章节号: {chapter_num}")

        # 根据章节号判断阶段
        if chapter_num is not None:
            phase = PhaseCharacteristics.get_phase_by_chapter(chapter_num)
            self.logger.info(f"[{self.name}] 章节 {chapter_num} 属于阶段: {phase.value}")
            return phase, chapter_num

        return None, None

    def _build_system_prompt(
        self,
        phase: Optional[NovelPhase],
        chapter_num: Optional[int],
        work_id: Optional[str],
        chapter_id: Optional[str]
    ) -> str:
        """
        构建系统Prompt

        根据阶段和上下文生成完整的系统Prompt

        Args:
            phase: 创作阶段
            chapter_num: 章节号
            work_id: 作品ID
            chapter_id: 章节ID

        Returns:
            str: 系统Prompt
        """
        # 基础Prompt
        if phase:
            # 使用阶段优化的Prompt（保留原有逻辑）
            base_prompt = get_content_prompt(
                phase=phase,
                scene_type=None,
                context={
                    'current_chapter': chapter_num,
                    'total_chapters': 50  # 默认50章，可配置
                }
            )
        else:
            # 🔧 使用 PromptManager 渲染默认 Prompt
            try:
                base_prompt = self.prompt_manager.render(
                    "writing_agent",
                    user_message="",  # 此处不需要具体消息
                    context_summary="",
                    user_preferences={},
                    writing_constraints=[],
                    examples=[]
                )
                # ✅ 清理空的"当前任务"部分，保持Prompt结构清晰
                base_prompt = re.sub(
                    r'# 当前任务\s*\n\s*用户需求：\s*\n+.*?现在请开始创作网络小说内容：\s*\n*',
                    '',
                    base_prompt,
                    flags=re.DOTALL
                )
            except Exception as e:
                logger.warning(f"[WritingAction] PromptManager渲染失败，使用备用Prompt: {e}")
                # 备用方案：使用原有的硬编码 Prompt
                base_prompt = """你是专业的网络小说写作助手Agent，专注于创作网文故事。

【重要】你的写作风格：
- 你是网文作家，不是程序员或技术文档作者
- 写作类型：玄幻、都市、言情、武侠、仙侠等网络小说
- 绝对禁止写编程、代码、技术相关的内容
- 必须写人物、情节、对话、情感、动作、场景描写
- 保持网文的节奏感和代入感"""

        # 工具使用说明（保持原有逻辑不变）
        tools_instruction = f"""

---

【工具使用】
可用工具：
- get_context_tool: 获取作品/章节上下文（包含作品信息、章节内容、相关分析）
- read_chapter_tool: 读取指定章节的完整内容（需要chapter_id）
- get_chapter_by_order_tool: 通过章节序号获取章节（用户说"第X章"时用这个）
- search_analysis_fragments_tool: 从向量数据库检索相关的小说分析片段（RAG）
- continue_writing_tool: 续写内容
- polish_text_tool: 润色文本

当前信息：作品ID={work_id}, 当前页面章节ID={chapter_id}

【重要】章节处理流程：
1. 用户说"续写第X章"或"读第X章"时：
   - 先调用 get_chapter_by_order_tool 获取第X章的 chapter_id 和内容
   - 例如：用户说"续写第二章"，你应该调用 get_chapter_by_order_tool(chapter_order=2)

2. 用户说"续写"但没指定章节时：
   - 使用当前页面的 chapter_id 调用 read_chapter_tool

3. 续写要求：
   - 必须先读取章节的真实内容
   - 续写必须紧接章节结尾，不要重新开头
   - 保持原文的写作风格、人物性格、情节发展
   - 写网络小说故事，不是技术文档或编程内容
   - 可调用 search_analysis_fragments_tool 获取世界观、角色设定

根据用户需求，决定调用合适的工具。"""

        return base_prompt + tools_instruction


# 导出
__all__ = ["WritingAction"]
