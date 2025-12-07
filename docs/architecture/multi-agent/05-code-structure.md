# 代码结构设计

> 文档版本: 1.1
> 创建日期: 2025-12-06
> 最后更新: 2025-12-06
> 状态: 设计方案

⚠️ **重要说明**：本文档描述的是 **目标结构**，`multi_agent/` 目录 **尚未创建**。

---

## 概述

本文档描述 Multi-Agent 实现的代码结构，以及 `langgraph_agent.py` 的拆分方案。

---

## 现有代码结构（实际状态）

> ⚠️ 以下是当前项目中**已存在**的代码结构，**不是**本文档设计的 Multi-Agent。

```
backend/app/services/agent/         # 现有结构
├── langgraph_agent.py              # 5015行，主工作流（待拆分）
│
├── agents/                          # 现有 Agent（不是5角色Multi-Agent）
│   ├── planning_agent.py           # 规划Agent - 用于任务规划和执行
│   ├── reflection_agent.py         # 反思Agent - 用于自我评估
│   └── parallel_executor.py        # 并行执行器
│
├── actions/                         # ARE架构的Action层
│   ├── base_action.py              # Action基类
│   ├── writing_action.py           # 写作Action
│   ├── planning_action.py          # 规划Action
│   ├── analysis_action.py          # 分析Action
│   ├── stuck_action.py             # 卡文Action
│   ├── general_chat_action.py      # 通用聊天Action
│   ├── action_registry.py          # Action注册表
│   └── echo_action.py              # 测试Action
│
├── environment/                     # 环境管理（可复用于Multi-Agent）
│   ├── message_bus.py              # 消息总线（发布-订阅）⭐可复用
│   ├── state_manager.py            # 状态管理（三级缓存）⭐可复用
│   └── langgraph_helper.py         # LangGraph集成助手
│
├── memory/                          # 记忆系统
│   ├── memory_manager.py           # 记忆管理器
│   ├── long_term_memory.py         # 长期记忆
│   ├── user_profile.py             # 用户画像
│   └── ... (其他模块)
│
├── tools/                           # 工具系统
│   ├── tool_registry.py            # 工具注册表 ⭐可复用
│   ├── editor_tools.py             # 编辑工具
│   ├── writing_tools.py            # 写作工具
│   └── ... (其他工具)
│
├── quality/                         # 质量评估
│   ├── quality_evaluator.py
│   └── quality_loop.py
│
├── prompts/                         # Prompt库
│   ├── novel_planning_prompts.py
│   └── content_creation_prompts.py
│
└── utils/                           # 工具函数
    ├── error_handler.py
    ├── logger.py
    └── monitoring.py
```

### 现有 Agent 与新 Multi-Agent 的关系

| 现有模块 | 职责 | 与新Multi-Agent的关系 |
|---------|------|---------------------|
| `PlanningAgent` | 任务规划和执行 | **不冲突**，用于任务调度层 |
| `ReflectionAgent` | 自我评估和迭代 | **可参考**，类似总编的评估职责 |
| `WritingAgentGraph` | LangGraph主工作流 | **集成点**，Multi-Agent嵌入此处 |

---

## 当前问题

### langgraph_agent.py 现状

```
文件行数：5015行
问题：典型的"上帝类"反模式
```

### 行数分布（估算）

```
langgraph_agent.py
├── 导入和常量           ~50行
├── AgentState + 工具定义  ~1000行
└── WritingAgentGraph类   ~3900行
    ├── 初始化            ~250行
    ├── 图构建            ~100行
    ├── 意图分类          ~130行
    ├── Agent处理器       ~1100行  ← 最大块
    ├── chat()            ~100行
    ├── chat_stream()     ~320行
    ├── chat_with_planning() ~380行
    ├── 任务执行          ~520行
    ├── 响应构建          ~250行
    └── 工具方法          ~750行
```

---

## 目标结构

### 完整目录树

```
backend/app/services/agent/
│
├── langgraph_agent.py          # 精简为入口+组装（~300行）
│
├── graph/                       # 🆕 图相关
│   ├── __init__.py
│   ├── state.py                # AgentState定义（~100行）
│   ├── graph_builder.py        # _build_graph逻辑（~150行）
│   └── routing.py              # 路由逻辑（~100行）
│
├── handlers/                    # 🆕 Agent处理器
│   ├── __init__.py
│   ├── base_handler.py         # 基类（~100行）
│   ├── writing_handler.py      # _handle_writing（~200行）
│   ├── planning_handler.py     # _handle_planning（~200行）
│   ├── analysis_handler.py     # _handle_analysis（~200行）
│   ├── stuck_handler.py        # _handle_stuck（~200行）
│   └── general_handler.py      # _handle_general（~150行）
│
├── intent/                      # 🆕 意图分类
│   ├── __init__.py
│   ├── classifier.py           # 意图分类逻辑（~150行）
│   └── rules.py                # 规则匹配（~100行）
│
├── execution/                   # 🆕 执行层
│   ├── __init__.py
│   ├── task_executor.py        # 任务执行（~300行）
│   ├── parallel_executor.py    # 并行执行（~200行）
│   └── response_builder.py     # 响应构建（~250行）
│
├── stream/                      # 🆕 流式处理
│   ├── __init__.py
│   ├── chat_stream.py          # chat_stream逻辑（~350行）
│   ├── planning_stream.py      # chat_with_planning逻辑（~400行）
│   └── event_handler.py        # 事件处理（~200行）
│
├── multi_agent/                 # 🆕 Multi-Agent（核心新功能）
│   ├── __init__.py
│   ├── executor.py             # MultiAgentExecutor入口（~200行）
│   ├── agents/
│   │   ├── __init__.py
│   │   ├── base_agent.py       # Agent基类（~100行）
│   │   ├── outline_agent.py    # 大纲师（~150行）
│   │   ├── writer_agent.py     # 主笔（~150行）
│   │   ├── character_guard.py  # 角色守护（~150行）
│   │   ├── logic_auditor.py    # 逻辑审计（~150行）
│   │   └── editor_agent.py     # 总编（~200行）
│   └── prompts/
│       ├── __init__.py
│       ├── outline_prompt.py   # 大纲师Prompt
│       ├── writer_prompt.py    # 主笔Prompt
│       └── review_prompts.py   # 校验Prompt
│
└── ... (现有的其他目录保持不变)
    ├── memory/
    ├── tools/
    ├── prompts/
    ├── utils/
    └── ...
```

---

## Multi-Agent 模块详细设计

### multi_agent/executor.py

```python
"""Multi-Agent 执行器 - 入口类"""

import asyncio
import time
from typing import Dict, Any, Optional, Callable
from .agents.outline_agent import OutlineAgent
from .agents.writer_agent import WriterAgent
from .agents.character_guard import CharacterGuard
from .agents.logic_auditor import LogicAuditor
from .agents.editor_agent import EditorAgent


class MultiAgentExecutor:
    """
    写作任务的 Multi-Agent 执行器

    流程：大纲师 → 主笔 → 角色守护 → 逻辑审计 → 总编
    """

    STAGE_TASKS = [
        {"task_id": 1, "description": "生成章节大纲", "tool": "outline_agent"},
        {"task_id": 2, "description": "撰写初稿", "tool": "writer_agent"},
        {"task_id": 3, "description": "审核人设一致性", "tool": "character_guard"},
        {"task_id": 4, "description": "检查剧情逻辑", "tool": "logic_auditor"},
        {"task_id": 5, "description": "裁决修订定稿", "tool": "editor_agent"},
    ]

    STAGE_TIMEOUTS = {
        "outline": 30,
        "writing": 120,
        "character_guard": 30,
        "logic_auditor": 30,
        "editor": 60,
    }
    TOTAL_TIMEOUT = 300

    def __init__(self, ai_service, memory_manager=None):
        self.ai_service = ai_service
        self.memory_manager = memory_manager

        # 初始化各Agent
        self.outline_agent = OutlineAgent(ai_service)
        self.writer_agent = WriterAgent(ai_service)
        self.character_guard = CharacterGuard(ai_service)
        self.logic_auditor = LogicAuditor(ai_service)
        self.editor_agent = EditorAgent(ai_service)

    async def execute(
        self,
        task: Dict[str, Any],
        work_id: str,
        chapter_id: str,
        context: Dict[str, Any],
        on_event: Optional[callable] = None
    ) -> Dict[str, Any]:
        """
        执行写作任务的完整Multi-Agent流程

        Args:
            task: 任务信息
            work_id: 作品ID
            chapter_id: 章节ID
            context: 上下文（需要包含 character_document / previous_summary / total_outline）
            on_event: 事件回调（发送 plan/task_start/task_done/content，调用方可用 format_planning_event_to_sse 包装）

        Returns:
            最终内容和元数据
        """
        async def _run_with_timeout(stage_name: str, coro):
            timeout = self.STAGE_TIMEOUTS.get(stage_name, 60)
            return await asyncio.wait_for(coro, timeout=timeout)

        async def _emit_plan():
            if on_event:
                await on_event({"type": "plan", "data": {"tasks": self.STAGE_TASKS}})

        async def _execute_pipeline():
            await _emit_plan()

            # 步骤1: 大纲师
            await self._report_event(on_event, "task_start", 1)
            start = time.time()
            outline = await _run_with_timeout("outline", self.outline_agent.generate(task, context))
            await self._report_event(on_event, "task_done", 1, time.time() - start)

            # 步骤2: 主笔
            await self._report_event(on_event, "task_start", 2)
            start = time.time()
            draft = await _run_with_timeout("writing", self.writer_agent.write(outline, context))
            await self._report_event(on_event, "task_done", 2, time.time() - start)

            # 步骤3&4: 校验并行
            await self._report_event(on_event, "task_start", 3)
            await self._report_event(on_event, "task_start", 4)
            start = time.time()
            character_review, logic_review = await asyncio.gather(
                _run_with_timeout("character_guard", self.character_guard.check(draft, work_id, context)),
                _run_with_timeout("logic_auditor", self.logic_auditor.check(draft, work_id, context)),
            )
            elapsed = time.time() - start
            await self._report_event(on_event, "task_done", 3, elapsed)
            await self._report_event(on_event, "task_done", 4, elapsed)

            # 步骤5: 总编
            await self._report_event(on_event, "task_start", 5)
            start = time.time()
            if self._needs_revision(character_review, logic_review):
                final = await _run_with_timeout(
                    "editor",
                    self.editor_agent.revise(draft, character_review, logic_review, context),
                )
            else:
                final = {
                    "content": draft.get("content", ""),
                    "word_count": draft.get("word_count", 0),
                    "quality_score": 0.85,
                    "revision_summary": "无需修订",
                    "conflicts_resolved": [],
                }
            await self._report_event(on_event, "task_done", 5, time.time() - start)
            await self._report_event(on_event, "content", data=final.get("content", ""))

            return {
                "content": final.get("content", ""),
                "word_count": final.get("word_count", 0),
                "quality_score": final.get("quality_score", 0.85),
                "outline": outline,
                "draft": draft,
                "character_review": character_review,
                "logic_review": logic_review,
                "revision_summary": final.get("revision_summary"),
                "conflicts_resolved": final.get("conflicts_resolved", []),
            }

        return await asyncio.wait_for(_execute_pipeline(), timeout=self.TOTAL_TIMEOUT)

    def _needs_revision(self, char_review, logic_review) -> bool:
        """判断是否需要修订"""
        return (
            char_review.get("status") == "NEED_REVISION" or
            logic_review.get("status") == "NEED_REVISION"
        )

    async def _report_event(
        self,
        callback: Optional[Callable],
        event_type: str,
        task_id: int,
        elapsed_time: float = 0,
        data: Any = None,
    ):
        """报告事件"""
        if callback:
            if event_type == "task_start":
                await callback({"type": "task_start", "data": {"task_id": task_id}})
            elif event_type == "task_done":
                await callback({
                    "type": "task_done",
                    "data": {"task_id": task_id, "elapsed_time": elapsed_time}
                })
            elif event_type == "content":
                await callback({"type": "content", "data": data or ""})
```

> 约定补充：
> - `on_event` 回调输出的是 Planning 事件（plan/task_start/task_done/content），由调用方使用 `format_planning_event_to_sse` 包装后写 SSE。
> - `context` 必须由集成层构建（推荐 `_build_multi_agent_context`，从 `WorldviewService`/`VectorMemoryStore` 获取 `character_document`、`previous_summary`、`total_outline`）。
> - 回退/重试策略沿用 10-integration-details.md（示例未展开降级逻辑，仅给出超时保护）。

---

### multi_agent/agents/base_agent.py

```python
"""Agent基类"""

from abc import ABC, abstractmethod
from typing import Dict, Any


class BaseAgent(ABC):
    """Multi-Agent基类"""

    def __init__(self, ai_service):
        self.ai_service = ai_service

    @abstractmethod
    async def execute(self, input_data: Dict[str, Any], context: Dict[str, Any]) -> Dict[str, Any]:
        """执行Agent任务"""
        pass

    async def _call_llm(self, prompt: str, temperature: float = 0.7) -> str:
        """调用LLM"""
        result = await self.ai_service.generate_text(
            prompt=prompt,
            temperature=temperature,
            max_tokens=2000
        )
        return result.get("text", "")

    def _parse_json_response(self, text: str) -> Dict[str, Any]:
        """解析JSON响应"""
        import json
        import re

        # 尝试提取JSON
        json_match = re.search(r'\{[\s\S]*\}', text)
        if json_match:
            try:
                return json.loads(json_match.group())
            except json.JSONDecodeError:
                pass
        return {}
```

---

### multi_agent/agents/character_guard.py

```python
"""角色守护Agent"""

from typing import Dict, Any
from .base_agent import BaseAgent
from ..prompts.review_prompts import CHARACTER_GUARD_PROMPT


class CharacterGuard(BaseAgent):
    """
    角色守护Agent

    职责：校验人设一致性（名字/性格/能力）
    """

    async def check(
        self,
        draft: Dict[str, Any],
        work_id: str,
        context: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        校验草稿的人设一致性

        Args:
            draft: 主笔输出的草稿
            work_id: 作品ID
            context: 包含人设文档等

        Returns:
            校验结果 {status, issues, confidence}
        """
        # 获取人设文档
        character_doc = context.get("character_document", "")

        # 构建Prompt
        prompt = CHARACTER_GUARD_PROMPT.format(
            content=draft["content"],
            character_document=character_doc,
            chapter_id=draft.get("chapter_id", "unknown")
        )

        # 调用LLM
        response = await self._call_llm(prompt, temperature=0.3)

        # 解析结果
        result = self._parse_json_response(response)

        # 确保返回格式正确
        return {
            "chapter_id": draft.get("chapter_id"),
            "status": result.get("status", "PASS"),
            "issues": result.get("issues", []),
            "confidence": result.get("confidence", 0.8)
        }

    async def execute(self, input_data: Dict[str, Any], context: Dict[str, Any]) -> Dict[str, Any]:
        """BaseAgent接口实现"""
        return await self.check(input_data, context.get("work_id", ""), context)
```

---

## 精简后的 langgraph_agent.py

```python
"""
LangGraph Agent 入口
精简版：~300行
"""

from app.services.agent.graph.state import AgentState
from app.services.agent.graph.graph_builder import build_agent_graph
from app.services.agent.handlers import (
    WritingHandler, PlanningHandler, AnalysisHandler,
    StuckHandler, GeneralHandler
)
from app.services.agent.intent.classifier import IntentClassifier
from app.services.agent.stream.chat_stream import ChatStreamMixin
from app.services.agent.stream.planning_stream import PlanningStreamMixin
from app.services.agent.execution.task_executor import TaskExecutor


class WritingAgentGraph(ChatStreamMixin, PlanningStreamMixin):
    """
    智能写作Agent - 组装各模块

    职责：
    1. 初始化和组装各模块
    2. 提供统一的chat/chat_stream/chat_with_planning入口
    3. 管理checkpointer和状态
    """

    _checkpointer = None  # 类级别共享

    def __init__(self, ai_service, use_chatgpt: bool = False):
        self.ai_service = ai_service
        self.use_chatgpt = use_chatgpt

        # 初始化各组件
        self.intent_classifier = IntentClassifier(ai_service)
        self.task_executor = TaskExecutor(ai_service)

        # 初始化处理器
        self.handlers = {
            "writing": WritingHandler(ai_service, use_chatgpt),
            "planning": PlanningHandler(ai_service, use_chatgpt),
            "analysis": AnalysisHandler(ai_service, use_chatgpt),
            "stuck": StuckHandler(ai_service, use_chatgpt),
            "general": GeneralHandler(ai_service, use_chatgpt),
        }

        # 构建LangGraph图
        self.graph = build_agent_graph(
            handlers=self.handlers,
            intent_classifier=self.intent_classifier,
            checkpointer=self._checkpointer
        )

    async def chat(self, message: str, **kwargs) -> Dict[str, Any]:
        """
        基础聊天入口

        Args:
            message: 用户消息
            **kwargs: work_id, chapter_id, conversation_id等

        Returns:
            Agent响应
        """
        # 构建初始状态
        initial_state = self._build_initial_state(message, kwargs)

        # 运行图
        config = {"configurable": {"thread_id": kwargs.get("conversation_id", "default")}}
        result = await self.graph.ainvoke(initial_state, config)

        return self._format_response(result)

    # chat_stream 和 chat_with_planning 通过 Mixin 继承
    # 详见 stream/chat_stream.py 和 stream/planning_stream.py
```

---

## 拆分优先级

| 优先级 | 任务 | 工作量 | 风险 |
|--------|------|--------|------|
| **P0** | 新建 `multi_agent/` 目录（新功能） | 3天 | 无 |
| **P1** | 拆分 `handlers/`（5个处理器） | 1天 | 低 |
| **P2** | 拆分 `stream/`（流式处理） | 1天 | 中 |
| **P3** | 拆分 `intent/`（意图分类） | 0.5天 | 低 |
| **P4** | 拆分 `execution/`（任务执行） | 1天 | 中 |
| **P5** | 精简 `langgraph_agent.py` | 0.5天 | 低 |

### 推荐路径

```
阶段1: 新建 multi_agent/ 实现新功能     [P0, 不动现有代码]
阶段2: 拆分 handlers/                  [P1, 风险最低的重构]
阶段3: 拆分 stream/                    [P2, 逐步减小主文件]
阶段4: 最终精简 langgraph_agent.py      [P3-P5, 收尾]
```

---

## 相关文档

- [04-implementation-plan.md](./04-implementation-plan.md) - 实现方案选择
- [06-api-design.md](./06-api-design.md) - API接口设计
- [07-implementation-steps.md](./07-implementation-steps.md) - 详细实施步骤
