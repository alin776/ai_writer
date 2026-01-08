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
from app.services.agent.prompts.format_guidelines import get_format_guidelines

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

    def __init__(self):
        """
        初始化WritingAction

        注意：新架构不需要ai_service参数，Action只负责准备参数
        """
        super().__init__("writing", "处理写作相关请求")

        # 🔧 新增：初始化 PromptManager
        from app.prompts import get_prompt_manager
        self.prompt_manager = get_prompt_manager()
        self.logger.info(f"[{self.name}] PromptManager已初始化")

        # 🆕 双Prompt架构：从配置中读取
        from app.core.config import settings
        self.use_dual_prompt = settings.AGENT_USE_DUAL_PROMPT
        self.logger.info(f"[{self.name}] 双Prompt架构: {'启用' if self.use_dual_prompt else '禁用'}")

    async def prepare(self, state: Dict[str, Any]) -> ActionResult:
        """
        准备写作场景的参数和Prompt（新架构方法）

        职责：
        1. 识别章节号和创作阶段（业务逻辑）
        2. 构建系统Prompt（单Prompt或双Prompt架构）
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
            if self.use_dual_prompt:
                # 🆕 双Prompt架构：阶段1使用系统层Prompt（轻量级）
                system_prompt = self._build_system_layer_prompt(state)
                self.logger.info("[双Prompt] 使用系统层Prompt（专注决策逻辑）")
            else:
                # 原有单Prompt架构
                system_prompt = self._build_system_prompt(
                    phase=phase,
                    chapter_num=chapter_num,
                    work_id=work_id,
                    chapter_id=chapter_id,
                    state=state
                )
                self.logger.info("[单Prompt] 使用传统系统Prompt")

            # 4. 返回准备好的参数
            return ActionResult(
                status=ActionStatus.COMPLETED,
                system_prompt=system_prompt,
                metadata={
                    "agent_type": "writing",
                    "action": "writing",
                    "phase": phase.value if phase else None,
                    "chapter_num": chapter_num,
                    "work_id": work_id,
                    "chapter_id": chapter_id,
                    "use_dual_prompt": self.use_dual_prompt  # 🆕 标记是否使用双Prompt
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

    def _extract_context_from_messages(self, messages: list) -> str:
        """
        从消息历史中提取场景设定和上下文

        提取包含场景设定的关键消息，确保AI遵循用户的场景要求

        Args:
            messages: 消息列表

        Returns:
            str: 提取的上下文摘要
        """
        context_parts = []

        # 遍历消息历史（排除最后一条，因为是当前请求）
        for msg in messages[:-1] if len(messages) > 1 else []:
            if not hasattr(msg, 'content'):
                continue

            content = str(msg.content)

            # 检查是否包含场景设定关键词
            scene_keywords = [
                "场景", "主角", "氛围", "设定", "背景",
                "时代", "地点", "角色", "人物", "剧情",
                "世界观", "风格", "类型", "主题"
            ]

            # 如果消息包含场景设定关键词，提取该消息
            if any(keyword in content for keyword in scene_keywords):
                # 限制长度避免prompt过长
                if len(content) > 500:
                    content = content[:500] + "..."
                context_parts.append(content)
                self.logger.info(f"[{self.name}] 提取到场景设定消息（长度：{len(content)}）")

        if context_parts:
            result = "\n\n".join(context_parts)
            self.logger.info(f"[{self.name}] 共提取 {len(context_parts)} 条上下文消息")
            return result

        self.logger.warning(f"[{self.name}] 未找到场景设定消息")
        return ""

    def _build_system_layer_prompt(self, state: Dict[str, Any]) -> str:
        """
        构建系统层Prompt（双Prompt架构 - 阶段1）

        系统层专注于：
        - 意图识别
        - 工具调用决策
        - 轻量级（~500 tokens）

        Args:
            state: AgentState

        Returns:
            str: 系统层Prompt
        """
        try:
            messages = state.get("messages", [])
            user_message = messages[-1].content if messages else ""

            # 使用 system_agent_prompt.yaml 模板
            system_prompt = self.prompt_manager.render(
                "system_agent_prompt",
                user_message=user_message
            )

            self.logger.info(f"[{self.name}] 系统层Prompt生成成功 (长度: {len(system_prompt)})")
            return system_prompt

        except Exception as e:
            self.logger.error(f"[{self.name}] 系统层Prompt生成失败: {e}", exc_info=True)
            # 备用方案：返回基础系统层Prompt
            return """你是Agent的决策系统，负责理解用户意图并调用相应工具。

可用工具：
- read_chapter_tool: 读取章节内容
- smart_rewrite: 生成改写版本（3个版本供用户选择）
- apply_chapter_edit: 直接应用修改到章节
- smart_continue: 追加内容到章节末尾（不生成内容，需要先有content）
- get_worldview_summary: 查询世界观信息（当用户询问"世界观里有什么"时立即调用）

请分析用户意图，决定调用哪些工具。"""

    def _build_creative_layer_prompt(
        self,
        state: Dict[str, Any],
        task_type: str = "rewrite",
        **kwargs
    ) -> str:
        """
        构建创作层Prompt（双Prompt架构 - 阶段2）

        创作层专注于：
        - 高质量内容生成
        - Few-Shot示例
        - 风格参考和上下文
        - 重量级（~800 tokens）

        Args:
            state: AgentState
            task_type: 任务类型 (rewrite/continue)
            **kwargs: 动态参数（original_text, user_requirement, base_version等）

        Returns:
            str: 创作层Prompt
        """
        try:
            # 1. 提取风格参考（从章节中取前500字）
            style_reference = kwargs.get("style_reference", "")
            if not style_reference:
                # 尝试从state中提取
                chapter_content = kwargs.get("chapter_content", "")
                if chapter_content:
                    style_reference = self._extract_style_reference(chapter_content)

            # 2. 提取当前剧情状态
            current_plot = state.get("context", {}).get("plot_state", "")

            # 3. 提取角色信息
            character_context = state.get("context", {}).get("characters", "")

            # 4. 渲染创作层Prompt
            creative_prompt = self.prompt_manager.render(
                "creative_writing_prompt",
                task_type=task_type,
                style_reference=style_reference,
                current_plot=current_plot,
                character_context=character_context,
                **kwargs  # 包含original_text, user_requirement, base_version等
            )

            self.logger.info(
                f"[{self.name}] 创作层Prompt生成成功 "
                f"(长度: {len(creative_prompt)}, 任务类型: {task_type})"
            )
            return creative_prompt

        except Exception as e:
            self.logger.error(f"[{self.name}] 创作层Prompt生成失败: {e}", exc_info=True)
            # 备用方案：返回基础创作层Prompt
            return f"""你是资深网文作家，专注于高质量内容创作。

任务类型：{task_type}

请生成高质量的网文内容。"""

    def _extract_style_reference(self, chapter_content: str) -> str:
        """
        从章节中提取风格参考（前500字）

        Args:
            chapter_content: 章节内容

        Returns:
            str: 风格参考文本
        """
        if not chapter_content:
            return ""

        # 去除HTML标签
        import re
        text = re.sub(r'<[^>]+>', '', chapter_content)

        # 取前500字
        style_ref = text[:500]

        self.logger.info(f"[{self.name}] 提取风格参考 (长度: {len(style_ref)})")
        return style_ref

    def _build_system_prompt(
        self,
        phase: Optional[NovelPhase],
        chapter_num: Optional[int],
        work_id: Optional[str],
        chapter_id: Optional[str],
        state: Dict[str, Any]
    ) -> str:
        """
        构建系统Prompt

        根据阶段和上下文生成完整的系统Prompt

        Args:
            phase: 创作阶段
            chapter_num: 章节号
            work_id: 作品ID
            chapter_id: 章节ID
            state: AgentState（用于提取消息历史）

        Returns:
            str: 系统Prompt
        """
        # ✅ 从消息历史中提取场景设定上下文
        messages = state.get("messages", [])
        context_summary = self._extract_context_from_messages(messages)

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
                # ✅ 修复：传递真实的上下文摘要，而不是空字符串
                base_prompt = self.prompt_manager.render(
                    "writing_agent",
                    user_message="",  # 此处不需要具体消息
                    context_summary=context_summary,  # ✅ 使用提取的场景设定
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

## 📖 读取工具
- get_context_tool: 获取作品/章节上下文（包含作品信息、章节内容、相关分析）
- read_chapter_tool: 读取指定章节的完整内容（需要chapter_id）
- get_chapter_by_order_tool: 通过章节序号获取章节（⭐用户说"第X章"时用这个）
- search_analysis_fragments_tool: 从向量数据库检索相关的小说分析片段（RAG）
- get_worldview_summary: 查询世界观信息（当用户询问"世界观里有什么"、"有哪些角色/地点/设定"时立即调用）

## ✍️ 编辑器工具（直接修改编辑器内容 - 优先使用）
- smart_rewrite: 改写/修改章节内容（会生成3个版本供用户选择）
  - 参数: chapter_id, text_to_rewrite, user_requirement
  - 用于: 用户说"修改"、"改写"、"重写"、"润色"、"优化"、"扩写"章节时
  - ⚠️ "扩写"= 把现有内容写得更丰富，属于改写场景，不是续写！
- smart_continue: 追加内容到章节末尾（不生成内容，需要先有content）
  - 参数: chapter_id, content
  - 用于: 系统内部调用，将已生成的内容追加到章节
  - ⚠️ 续写场景请用 continue_writing_tool + apply_to_editor=true
- smart_insert: 插入内容到章节
  - 参数: chapter_id, position, content
  - 用于: 用户说"插入"内容时
- apply_chapter_edit: 应用章节编辑
  - 参数: chapter_id, operation, content
  - 用于: 替换/追加/插入操作

## 📝 普通写作工具
- continue_writing_tool: 续写内容（加 apply_to_editor=true 可写入编辑器）

当前信息（内部参数，禁止在回复中显示）：work_id={work_id}, chapter_id={chapter_id}

**⚠️ 重要：禁止在回复中显示 UUID**
- 在回复用户时，**绝对不要**显示 work_id 或 chapter_id 的值
- 用中文描述替代，如"当前作品"、"当前章节"、"本章"

【⚠️ 重要】修改/续写章节的正确流程：

1️⃣ 用户说"修改第X章"/"改写第X章"时：
   第一步：调用 get_chapter_by_order_tool 获取第X章的 chapter_id
   第二步：**必须**调用 smart_rewrite(chapter_id=xxx, instructions="根据用户要求修改")
   ❌ 错误：直接返回修改建议文本
   ✅ 正确：调用smart_rewrite工具

2️⃣ 用户说"续写第X章"时：
   第一步：调用 get_chapter_by_order_tool 获取第X章的 chapter_id
   第二步：调用 continue_writing_tool，参数加 apply_to_editor=true, operation="append"
   ✅ 正确：使用 continue_writing_tool + apply_to_editor=true
   ❌ 错误：直接调用 smart_continue（它不生成内容）

3️⃣ 用户说"插入XX到第X章"时：
   第一步：调用 get_chapter_by_order_tool 获取第X章的 chapter_id
   第二步：**必须**调用 smart_insert(chapter_id=xxx, position="end", content="...")

📌 关键规则：
- 当用户要求"修改"、"改写"、"续写"、"插入"、"润色"、"优化"、"扩写"章节内容时，**必须调用编辑器工具**
- 编辑器工具会自动征求用户确认，所以放心使用
- 不要只是分析或给建议，要实际调用工具去修改
- 工具会返回HITL确认请求，前端会显示确认对话框
- ⚠️ "扩写"、"润色"、"优化" → smart_rewrite（改写场景）
- ⚠️ "续写" → continue_writing_tool + apply_to_editor=true（续写场景）

根据用户需求，决定调用合适的工具。"""

        # 添加格式指导
        format_guidelines = get_format_guidelines(lite=True)
        return f"{base_prompt}{tools_instruction}\n\n{format_guidelines}"


# 导出
__all__ = ["WritingAction"]
