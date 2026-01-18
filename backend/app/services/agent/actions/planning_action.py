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
from app.services.agent.prompts.format_guidelines import get_format_guidelines

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

    def __init__(self):
        """
        初始化PlanningAction

        注意：新架构不需要ai_service参数，Action只负责准备参数
        """
        super().__init__("planning", "处理小说规划相关请求")

        # 🔧 新增：初始化 PromptManager
        from app.prompts import get_prompt_manager
        self.prompt_manager = get_prompt_manager()
        self.logger.info(f"[{self.name}] PromptManager已初始化")

    async def prepare(self, state: Dict[str, Any]) -> ActionResult:
        """
        准备规划场景的参数和Prompt（新架构方法）

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
            chapter_id = state.get("chapter_id")  # 🆕 提取 chapter_id
            messages = state.get("messages", [])

            self.logger.info(f"[{self.name}] work_id={work_id}, chapter_id={chapter_id}")

            # 2. 生成系统Prompt（传入 chapter_id）
            system_prompt = self._build_system_prompt(work_id, chapter_id)

            # 3. 返回准备好的参数
            return ActionResult(
                status=ActionStatus.COMPLETED,
                system_prompt=system_prompt,  # 新架构：使用system_prompt参数
                metadata={
                    "agent_type": "planning",
                    "action": "planning",
                    "work_id": work_id,
                    "chapter_id": chapter_id  # 🆕 添加到 metadata
                }
            )

        except Exception as e:
            self.logger.error(f"[{self.name}] prepare()失败: {e}", exc_info=True)
            return ActionResult(
                status=ActionStatus.FAILED,
                error=str(e),
                metadata={"action": "planning"}
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

    def _build_system_prompt(self, work_id: str = None, chapter_id: str = None) -> str:
        """
        构建系统Prompt - 章节上下文感知版

        Args:
            work_id: 作品ID
            chapter_id: 章节ID（如果用户在章节聊天面板中，会自动传入）
        """

        # 🆕 关键修复：如果 chapter_id 存在，说明用户在特定章节的聊天面板中
        # 此时应该自动读取该章节内容，而不需要手动定位
        if chapter_id:
            core_instruction = f"""
你是小说创作助手。

# ✅ 当前环境：章节聊天面板
（内部参数：work_id="{work_id}", chapter_id="{chapter_id}"）

**⚠️ 重要：禁止在回复中显示 UUID**
- 在回复用户时，**绝对不要**显示 work_id 或 chapter_id 的值
- 用中文描述替代，如"当前作品"、"当前章节"、"本章"
- 工具调用时仍使用完整参数，但不要在文字回复中暴露

**重要规则**：用户正在这一章的专属聊天面板中对话，所以：
1. ⚠️ 在回答任何关于"修改/润色/分析"本章内容的问题之前，你**必须**先调用 `read_chapter_tool(work_id="{work_id}", chapter_id="{chapter_id}")` 读取本章完整内容
2. 只有在完全理解了章节的场景、情绪、角色状态、前后文逻辑之后，才能给出修改建议
3. 禁止在不读原文的情况下，凭空想象或套用模板

---

## 📖 标准工作流程

### 第一步：读取章节（必须）
当用户要求修改/润色/分析本章任何内容时：
→ **立即调用** `read_chapter_tool(work_id="{work_id}", chapter_id="{chapter_id}")`
→ 不要问用户在哪一章（因为已经在章节面板中）

### 第二步：理解上下文
读取原文后，分析：
- 这句话是谁说的？
- 当时在什么场景？（战斗/对话/死亡）
- 什么情绪？（悲伤/紧张/温馨）
- 前后文发生了什么？

### 第三步：给出建议
基于真实的上下文给出修改建议，而不是套用模板。

---

## 🔧 工具使用

**read_chapter_tool** - 读取本章内容（优先使用）
- 固定参数: `work_id="{work_id}", chapter_id="{chapter_id}"`
- 用途：每次处理修改/润色/分析请求时的第一步

**get_worldview_summary** - 查询世界观信息
- 参数: `work_id="{work_id}"`
- 用途：当用户询问"世界观里有什么"、"有哪些角色/地点/设定"时调用
- ⚠️ 必须立即调用，不要问用户想了解什么

**explore_content** - 统一信息获取工具（返回snippet）
- 用途：查询本章之外的信息（如角色设定、世界观）
- 参数: `target_task="描述任务目标"`

**get_context_tool** - 获取作品大纲/简介
- 用途：规划任务、了解整体故事结构
- 参数: `work_id="{work_id}"`

---

## 📝 输出要求：必须先输出思维链

在回答用户之前，你必须先输出 **【思维链】**，格式如下：

```
[思维链]
1. 用户意图：[提取用户想做什么]
2. 当前章节：本章（不要显示 UUID）
3. 行动决策：先调用 read_chapter_tool 读取本章内容
4. 预期目标：理解场景、情绪、角色状态后给出建议
[结束思维链]
```

然后调用工具和给出最终回复。

---

## 回答质量标准

**拒绝陈词滥调**：
- ❌ "星辰大海"、"深邃的眼眸"、"浩瀚宇宙"
- ✅ 有画面感、有情绪、符合当前场景

**Show, Don't Tell**：
- ❌ "他很悲伤"
- ✅ "他的手在颤抖，嘴角的笑僵硬得像块石头"

**必须符合语境**：
- 悲剧场景 → 不要写浪漫
- 战斗场景 → 不要写抒情
- 温馨场景 → 不要写惊悚

---

记住：**在章节聊天面板中 = 先读章节内容！**
"""
        else:
            # 原有的逻辑死锁修复版本（非章节面板场景）
            core_instruction = f"""
你是小说创作助手。（内部参数：work_id="{work_id}"）

**⚠️ 重要：禁止在回复中显示 UUID**
- 在回复用户时，**绝对不要**显示 work_id 或 chapter_id 的值
- 用中文描述替代，如"当前作品"、"当前章节"、"本章"

# 🚨 核心故障排除：你经常犯的错误

**错误行为**：用户给了一句原文让你改，因为你不知道这句话在第几章，你就直接开始瞎编。
**从现在起，禁止这种行为！**

---

## 工作流程：【定位 → 获取 → 处理】

当用户要求"修改/润色/分析"某段具体文字时，你必须执行以下流程：

### 第一步：定位 (Locate)
**问自己：我知道这是第几章吗？**

- **情况A：知道章节号** (用户说了"第X章" 或 对话历史中正在讨论某章)
  → 进入第二步

- **情况B：不知道章节号** (用户只给了句子，没说在哪)
  → **禁止直接回答！**
  → 你必须先调用 `explore_content` 搜索这句话，找到它在第几章
  → 如果搜不到，你必须反问用户："这句话是在哪一章？我需要看上下文才能给出合适的修改建议。"

### 第二步：获取 (Retrieve)
拿到章节号后，**必须调用** `read_chapter_tool(chapter_number=X)`

**为什么必须读原文？**
- 这句话是谁说的？
- 当时在什么场景？（战斗/对话/死亡）
- 什么情绪？（悲伤/紧张/温馨）
- 前后文发生了什么？

### 第三步：处理 (Process)
根据上下文语境进行修改。

---

## 🔧 工具操作指南

1. **read_chapter_tool** - 读取章节原文
   - 必填参数: `chapter_number=X`
   - ⚠️ 如果你不知道 chapter_number，不要瞎填！回到第一步执行"定位"流程！

2. **get_worldview_summary** - 查询世界观信息
   - 参数: `work_id={work_id}`
   - 用途：当用户询问"世界观里有什么"、"有哪些角色/地点/设定"时调用
   - ⚠️ 必须立即调用，不要问用户想了解什么

3. **explore_content** - 统一信息获取
   - 用途1：当你不知道某句话在哪一章时，用这个搜关键词
   - 用途2：查询旧设定、旧角色
   - 示例: `target_task="查找微光如露落雪相关内容"`

4. **get_context_tool** - 获取作品大纲/简介
   - 规划任务开始时使用
   - 参数: `work_id={work_id}`

---

## 📝 输出要求：必须先输出思维链

在回答用户之前，你必须先输出 **【思维链】**，格式如下：

```
[思维链]
1. 用户意图：修改"微光如露落雪"
2. 定位检查：我知道这是第几章吗？ -> [是/否]
3. 行动决策：
   - 如果是 -> 调用 read_chapter_tool(chapter_number=X)
   - 如果否 -> 调用 explore_content(target_task="查找微光如露落雪相关内容") 或 询问用户
4. 预期目标：获取上下文，判断场景类型和情绪
[结束思维链]
```

然后再调用工具和给出最终回复。

---

## 回答质量标准

**拒绝陈词滥调**：
- ❌ "星辰大海"、"深邃的眼眸"、"浩瀚宇宙"
- ✅ 有画面感、有情绪、符合当前场景

**Show, Don't Tell**：
- ❌ "他很悲伤"
- ✅ "他的手在颤抖，嘴角的笑僵硬得像块石头"

**必须符合语境**：
- 悲剧场景 → 不要写浪漫
- 战斗场景 → 不要写抒情
- 温馨场景 → 不要写惊悚

---

记住：**不知道章节号 = 禁止直接改 = 先定位！**
"""

        # 添加格式指导
        format_guidelines = get_format_guidelines(lite=True)
        return f"{core_instruction}\n\n{format_guidelines}"


# 导出
__all__ = ["PlanningAction"]
