# API 接口设计

> 文档版本: 1.0
> 创建日期: 2025-12-06
> 状态: 设计方案

---

## 概述

本文档描述 Multi-Agent 模块的内部 API 接口设计。

### 类型定义说明

> **设计决策**：本文档使用 `dataclass` 定义数据结构以提供清晰的类型约束和文档化。
>
> **实际实现**：可以根据需要使用 `Dict[str, Any]` 替代，以获得更高的灵活性。两种方式等效：
>
> ```python
> # dataclass 方式（类型安全）
> @dataclass
> class ReviewResult:
>     status: str
>     issues: List[ReviewIssue]
>
> # Dict 方式（灵活）
> result: Dict[str, Any] = {
>     "status": "PASS",
>     "issues": []
> }
> ```

---

## 核心类接口

### MultiAgentExecutor

```python
class MultiAgentExecutor:
    """Multi-Agent 执行器"""

    def __init__(
        self,
        ai_service: HTTPAIService,
        memory_manager: Optional[MemoryManager] = None
    ):
        """
        初始化执行器

        Args:
            ai_service: AI服务实例
            memory_manager: 记忆管理器（可选，用于获取人设、前文等）
        """
        pass

    async def execute(
        self,
        task: Dict[str, Any],
        work_id: str,
        chapter_id: str,
        context: Dict[str, Any],
        on_event: Optional[Callable[[Dict], Awaitable[None]]] = None
    ) -> MultiAgentResult:
        """
        执行写作任务

        Args:
            task: 任务信息
                {
                    "type": "write_chapter",
                    "description": "写第三章",
                    "parameters": {...}
                }
            work_id: 作品ID
            chapter_id: 章节ID
            context: 上下文信息
                {
                    "character_document": "人设文档...",
                    "previous_summary": "前文摘要...",
                    "outline": "大纲..."
                }
            on_event: 事件回调（发送 plan/task_start/task_done 等事件）

        Returns:
            MultiAgentResult
        """
        pass

    def is_writing_task(self, task: Dict[str, Any]) -> bool:
        """
        判断是否是写作类任务

        写作类任务类型：
        - write_chapter: 写章节
        - continue_writing: 续写
        - expand_content: 扩写
        - rewrite_content: 重写

        非写作类任务（不走Multi-Agent）：
        - search_content: 搜索内容
        - analyze_content: 分析内容
        - get_context: 获取上下文
        """
        pass
```

---

### MultiAgentResult

```python
from dataclasses import dataclass
from typing import List, Dict, Any, Optional


@dataclass
class ReviewIssue:
    """校验问题"""
    type: str              # 问题类型：性格偏离/逻辑矛盾/时间线错误等
    location: str          # 问题位置
    description: str       # 问题描述
    suggestion: str        # 修改建议
    reference: Optional[str] = None  # 参考章节（逻辑审计用）


@dataclass
class ReviewResult:
    """校验结果"""
    status: str            # PASS / NEED_REVISION
    issues: List[ReviewIssue]
    confidence: float      # 置信度 0-1


@dataclass
class MultiAgentResult:
    """Multi-Agent 执行结果"""
    content: str           # 最终内容
    word_count: int        # 字数
    quality_score: float   # 质量评分 0-1

    # 中间产物
    outline: Dict[str, Any]        # 大纲
    draft: Dict[str, Any]          # 初稿
    character_review: ReviewResult # 角色守护结果
    logic_review: ReviewResult     # 逻辑审计结果

    # 元数据
    revision_summary: Optional[str] = None  # 修订摘要（如果有修订）
    conflicts_resolved: List[Dict] = None   # 解决的冲突（如果有）
```

---

## Agent 接口

### BaseAgent（基类）

```python
from abc import ABC, abstractmethod


class BaseAgent(ABC):
    """Agent基类"""

    def __init__(self, ai_service: HTTPAIService):
        self.ai_service = ai_service

    @abstractmethod
    async def execute(
        self,
        input_data: Dict[str, Any],
        context: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        执行Agent任务

        Args:
            input_data: 输入数据
            context: 上下文

        Returns:
            输出结果
        """
        pass

    @property
    @abstractmethod
    def name(self) -> str:
        """Agent名称"""
        pass
```

---

### OutlineAgent（大纲师）

```python
class OutlineAgent(BaseAgent):
    """大纲师"""

    @property
    def name(self) -> str:
        return "outline_agent"

    async def generate(
        self,
        task: Dict[str, Any],
        context: Dict[str, Any]
    ) -> OutlineResult:
        """
        生成章节大纲

        Args:
            task: 任务信息
            context: 包含总纲、人设摘要、前文摘要等

        Returns:
            OutlineResult
        """
        pass


@dataclass
class OutlineResult:
    """大纲结果"""
    chapter_id: str
    title: str
    core_conflict: str
    characters: List[str]
    emotion_curve: Dict[str, str]  # {start, mid, end}
    foreshadowing: str
    connection_to_previous: str
```

---

### WriterAgent（主笔）

```python
class WriterAgent(BaseAgent):
    """主笔"""

    @property
    def name(self) -> str:
        return "writer_agent"

    async def write(
        self,
        outline: OutlineResult,
        context: Dict[str, Any]
    ) -> DraftResult:
        """
        根据大纲写初稿

        Args:
            outline: 大纲
            context: 包含人设文档、前文等

        Returns:
            DraftResult
        """
        pass


@dataclass
class DraftResult:
    """初稿结果"""
    chapter_id: str
    content: str
    word_count: int
    dialogue_ratio: str  # 如 "45%"
    pending_review: List[str]  # 待校验项
```

---

### CharacterGuard（角色守护）

```python
class CharacterGuard(BaseAgent):
    """角色守护"""

    @property
    def name(self) -> str:
        return "character_guard"

    async def check(
        self,
        draft: DraftResult,
        work_id: str,
        context: Dict[str, Any]
    ) -> ReviewResult:
        """
        校验人设一致性

        检查项：
        1. 角色名字是否正确
        2. 角色性格是否符合设定
        3. 角色口头禅是否正确使用
        4. 角色能力边界是否被突破
        5. 角色关系是否符合当前剧情进度

        Args:
            draft: 初稿
            work_id: 作品ID
            context: 包含人设文档

        Returns:
            ReviewResult
        """
        pass
```

---

### LogicAuditor（逻辑审计）

```python
class LogicAuditor(BaseAgent):
    """逻辑审计"""

    @property
    def name(self) -> str:
        return "logic_auditor"

    async def check(
        self,
        draft: DraftResult,
        work_id: str,
        context: Dict[str, Any]
    ) -> ReviewResult:
        """
        检查剧情逻辑

        检查项：
        1. 时间线是否矛盾
        2. 空间逻辑是否合理
        3. 因果关系是否成立
        4. 前文伏笔是否被遗忘/矛盾
        5. 角色已知信息是否被误用

        Args:
            draft: 初稿
            work_id: 作品ID
            context: 包含前文摘要、章节索引等

        Returns:
            ReviewResult
        """
        pass
```

---

### EditorAgent（总编）

```python
class EditorAgent(BaseAgent):
    """总编"""

    @property
    def name(self) -> str:
        return "editor_agent"

    async def revise(
        self,
        draft: DraftResult,
        character_review: ReviewResult,
        logic_review: ReviewResult,
        context: Dict[str, Any]
    ) -> FinalResult:
        """
        汇总裁决并修订

        裁决优先级：
        1. 逻辑自洽
        2. 人设一致
        3. 风格一致

        Args:
            draft: 初稿
            character_review: 角色守护结果
            logic_review: 逻辑审计结果
            context: 上下文

        Returns:
            FinalResult
        """
        pass


@dataclass
class FinalResult:
    """最终结果"""
    chapter_id: str
    content: str
    word_count: int
    quality_score: float
    revision_summary: str
    conflicts_resolved: List[Dict[str, str]]
```

---

## 进度回调接口

```python
# 进度事件类型
ProgressEvent = Dict[str, Any]

# 事件格式
{
    "step": "outline" | "writing" | "review" | "editing" | "complete",
    "status": "running" | "done" | "error",
    "agent": "outline_agent" | "writer_agent" | "character_guard" | "logic_auditor" | "editor_agent",
    "progress": 0.0 - 1.0,  # 可选
    "message": "正在生成大纲..."  # 可选
}

# 回调函数签名
async def on_event(event: ProgressEvent) -> None:
    pass
```

---

## 与 Planning 模式的集成点

### TaskExecutor 集成

```python
# execution/task_executor.py

class TaskExecutor:
    def __init__(self, ai_service):
        self.ai_service = ai_service
        self.multi_agent = MultiAgentExecutor(ai_service)

    async def execute_task(
        self,
        task: Dict[str, Any],
        work_id: str,
        chapter_id: str,
        context: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        执行单个任务

        根据任务类型选择执行方式：
        - 写作类任务 → Multi-Agent流程
        - 其他任务 → 简单执行
        """
        if self.multi_agent.is_writing_task(task):
            result = await self.multi_agent.execute(
                task, work_id, chapter_id, context
            )
            return {
                "task_id": task.get("task_id"),
                "result": result.content,
                "metadata": {
                    "word_count": result.word_count,
                    "quality_score": result.quality_score,
                    "reviews": {
                        "character": result.character_review,
                        "logic": result.logic_review
                    }
                }
            }
        else:
            return await self._simple_execute(task, work_id, chapter_id, context)
```

---

## 相关文档

- [05-code-structure.md](./05-code-structure.md) - 代码结构设计
- [07-implementation-steps.md](./07-implementation-steps.md) - 详细实施步骤
