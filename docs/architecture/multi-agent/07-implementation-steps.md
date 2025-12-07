# 详细实施步骤

> 文档版本: 1.0
> 创建日期: 2025-12-06
> 状态: 实施指南

---

## 概述

本文档提供 Multi-Agent 实现的详细步骤指南。

---

## 实施阶段总览

```
阶段1: 准备工作（移除ReAct）           [1天]
阶段2: 创建目录结构                    [0.5天]
阶段3: 实现核心Agent                   [2天]
阶段4: 实现执行器                      [1天]
阶段5: 集成到Planning模式              [1天]
阶段6: 测试与调优                      [2天]
────────────────────────────────────────
总计: 7-8天
```

---

## 阶段1: 准备工作（移除ReAct）

### 目标
清理无效的 ReAct 模式代码，简化架构。

### 步骤

#### 1.1 前端：移除 ReAct 选项

**文件**: `src/components/agent/ModeSelector.tsx`

```tsx
// 移除或隐藏 ReAct 选项
// 将默认模式改为 'planning'
```

**文件**: `src/components/agent/AgentChatPanel.tsx`

```tsx
// 第124行：将默认值从 'react' 改为 'planning'
const [mode, setMode] = useState<AgentMode>('planning');
```

**文件**: `src/hooks/useAgentChatStream.ts`

```tsx
// 第198行：移除 mode: 'react'
```

#### 1.2 后端：简化 API 层

**文件**: `backend/app/api/v1/agent.py`

```python
# 移除 mode 分支判断
# 统一使用 chat_with_planning
```

#### 1.3 移除 chat_stream 中的 ReAct 相关代码

**文件**: `backend/app/services/agent/langgraph_agent.py`

```python
# chat_stream() 方法可以保留，但作为内部方法
# 不再作为 ReAct 模式的入口
```

### 检查清单

- [ ] 前端默认模式改为 planning
- [ ] 移除 ModeSelector 中的 ReAct 选项
- [ ] API 层移除 mode 分支
- [ ] 更新 ChatMode 枚举（可选：移除 REACT）
- [ ] 测试 Planning 模式正常工作

---

## 阶段2: 创建目录结构

### 目标
建立 Multi-Agent 模块的目录和基础文件。

### 步骤

#### 2.1 创建目录

```bash
mkdir -p backend/app/services/agent/multi_agent/agents
mkdir -p backend/app/services/agent/multi_agent/prompts
```

#### 2.2 创建 __init__.py 文件

**文件**: `backend/app/services/agent/multi_agent/__init__.py`

```python
"""Multi-Agent 写作系统"""

from .executor import MultiAgentExecutor

__all__ = ["MultiAgentExecutor"]
```

**文件**: `backend/app/services/agent/multi_agent/agents/__init__.py`

```python
"""Multi-Agent 各角色Agent"""

from .base_agent import BaseAgent
from .outline_agent import OutlineAgent
from .writer_agent import WriterAgent
from .character_guard import CharacterGuard
from .logic_auditor import LogicAuditor
from .editor_agent import EditorAgent

__all__ = [
    "BaseAgent",
    "OutlineAgent",
    "WriterAgent",
    "CharacterGuard",
    "LogicAuditor",
    "EditorAgent",
]
```

### 检查清单

- [ ] 创建 multi_agent/ 目录
- [ ] 创建 agents/ 子目录
- [ ] 创建 prompts/ 子目录
- [ ] 创建所有 __init__.py 文件

---

## 阶段3: 实现核心 Agent

### 目标
实现 5 个核心 Agent。

### 步骤

#### 3.1 实现 BaseAgent

**文件**: `backend/app/services/agent/multi_agent/agents/base_agent.py`

```python
"""Agent基类"""

from abc import ABC, abstractmethod
from typing import Dict, Any, Optional
import json
import re
import logging

logger = logging.getLogger(__name__)


class BaseAgent(ABC):
    """Multi-Agent基类"""

    def __init__(self, ai_service):
        self.ai_service = ai_service

    @property
    @abstractmethod
    def name(self) -> str:
        """Agent名称"""
        pass

    @abstractmethod
    async def execute(
        self,
        input_data: Dict[str, Any],
        context: Dict[str, Any]
    ) -> Dict[str, Any]:
        """执行Agent任务"""
        pass

    async def _call_llm(
        self,
        prompt: str,
        temperature: float = 0.7,
        max_tokens: int = 2000
    ) -> str:
        """调用LLM"""
        try:
            result = await self.ai_service.generate_text(
                prompt=prompt,
                temperature=temperature,
                max_tokens=max_tokens
            )
            return result.get("text", "")
        except Exception as e:
            logger.error(f"[{self.name}] LLM调用失败: {e}")
            raise

    def _parse_json_response(self, text: str) -> Dict[str, Any]:
        """解析JSON响应"""
        # 尝试提取JSON块
        json_match = re.search(r'```json\s*([\s\S]*?)\s*```', text)
        if json_match:
            try:
                return json.loads(json_match.group(1))
            except json.JSONDecodeError:
                pass

        # 尝试直接解析
        json_match = re.search(r'\{[\s\S]*\}', text)
        if json_match:
            try:
                return json.loads(json_match.group())
            except json.JSONDecodeError:
                pass

        logger.warning(f"[{self.name}] 无法解析JSON响应")
        return {}
```

#### 3.2 实现 OutlineAgent

**文件**: `backend/app/services/agent/multi_agent/agents/outline_agent.py`

```python
"""大纲师Agent"""

from typing import Dict, Any
from .base_agent import BaseAgent
from ..prompts.outline_prompt import OUTLINE_PROMPT


class OutlineAgent(BaseAgent):
    """
    大纲师Agent

    职责：生成章节大纲（冲突/角色/情绪曲线）
    """

    @property
    def name(self) -> str:
        return "outline_agent"

    async def execute(
        self,
        input_data: Dict[str, Any],
        context: Dict[str, Any]
    ) -> Dict[str, Any]:
        return await self.generate(input_data, context)

    async def generate(
        self,
        task: Dict[str, Any],
        context: Dict[str, Any]
    ) -> Dict[str, Any]:
        """生成章节大纲"""
        prompt = OUTLINE_PROMPT.format(
            task_description=task.get("description", ""),
            total_outline=context.get("total_outline", ""),
            character_document=context.get("character_document", ""),
            previous_summary=context.get("previous_summary", ""),
            chapter_id=task.get("chapter_id", "unknown")
        )

        response = await self._call_llm(prompt, temperature=0.5)
        result = self._parse_json_response(response)

        return {
            "chapter_id": result.get("chapter_id", task.get("chapter_id")),
            "title": result.get("title", ""),
            "core_conflict": result.get("core_conflict", ""),
            "characters": result.get("characters", []),
            "emotion_curve": result.get("emotion_curve", {}),
            "foreshadowing": result.get("foreshadowing", ""),
            "connection_to_previous": result.get("connection_to_previous", "")
        }
```

#### 3.3 实现其他 Agent

按照相同模式实现：
- `writer_agent.py` - 主笔
- `character_guard.py` - 角色守护
- `logic_auditor.py` - 逻辑审计
- `editor_agent.py` - 总编

### 检查清单

- [ ] 实现 BaseAgent
- [ ] 实现 OutlineAgent
- [ ] 实现 WriterAgent
- [ ] 实现 CharacterGuard
- [ ] 实现 LogicAuditor
- [ ] 实现 EditorAgent
- [ ] 单元测试各Agent

---

## 阶段4: 实现执行器

### 目标
实现 MultiAgentExecutor，串联所有 Agent。

### 步骤

#### 4.1 实现 MultiAgentExecutor

**文件**: `backend/app/services/agent/multi_agent/executor.py`

> 下方为结构化示例，完整事件/超时/回退细节请遵循 05-code-structure.md 与 10-integration-details.md。

```python
"""Multi-Agent 执行器"""

import asyncio
import logging
from typing import Dict, Any, Optional, Callable, Awaitable

from .agents import (
    OutlineAgent,
    WriterAgent,
    CharacterGuard,
    LogicAuditor,
    EditorAgent
)

logger = logging.getLogger(__name__)


class MultiAgentExecutor:
    """
    写作任务的 Multi-Agent 执行器

    流程：大纲师 → 主笔 → 角色守护 → 逻辑审计 → 总编
    """

    # 写作类任务类型
    WRITING_TASK_TYPES = {
        "write_chapter",
        "continue_writing",
        "expand_content",
        "rewrite_content",
        "write_content",
    }

    def __init__(self, ai_service, memory_manager=None):
        self.ai_service = ai_service
        self.memory_manager = memory_manager

        # 初始化各Agent
        self.outline_agent = OutlineAgent(ai_service)
        self.writer_agent = WriterAgent(ai_service)
        self.character_guard = CharacterGuard(ai_service)
        self.logic_auditor = LogicAuditor(ai_service)
        self.editor_agent = EditorAgent(ai_service)

    def is_writing_task(self, task: Dict[str, Any]) -> bool:
        """判断是否是写作类任务"""
        task_type = task.get("type", "").lower()
        task_tool = task.get("tool", "").lower()

        # 检查任务类型
        if task_type in self.WRITING_TASK_TYPES:
            return True

        # 检查工具名称
        if any(keyword in task_tool for keyword in ["write", "content", "chapter"]):
            return True

        # 检查描述中的关键词
        description = task.get("description", "").lower()
        writing_keywords = ["写", "续写", "扩写", "重写", "创作", "生成内容"]
        if any(kw in description for kw in writing_keywords):
            return True

        return False

    async def execute(
        self,
        task: Dict[str, Any],
        work_id: str,
        chapter_id: str,
        context: Dict[str, Any],
        on_event: Optional[Callable[[Dict], Awaitable[None]]] = None
    ) -> Dict[str, Any]:
        """执行写作任务的完整Multi-Agent流程"""
        logger.info(f"[MultiAgent] 开始执行写作任务: {task.get('description', '')[:50]}")

        try:
            # 步骤1: 大纲师
            await self._report_event(on_event, "task_start", 1)
            outline = await self.outline_agent.generate(task, context)
            logger.info(f"[MultiAgent] 大纲生成完成: {outline.get('title', '')}")

            # 步骤2: 主笔
            await self._report_event(on_event, "task_done", 1)
            await self._report_event(on_event, "task_start", 2)
            draft = await self.writer_agent.write(outline, context)
            logger.info(f"[MultiAgent] 初稿完成: {draft.get('word_count', 0)}字")

            # 步骤3&4: 角色守护 + 逻辑审计（并行）
            await self._report_event(on_event, "task_done", 2)
            await self._report_event(on_event, "task_start", 3)
            await self._report_event(on_event, "task_start", 4)
            character_review, logic_review = await asyncio.gather(
                self.character_guard.check(draft, work_id, context),
                self.logic_auditor.check(draft, work_id, context)
            )
            logger.info(
                f"[MultiAgent] 校验完成: "
                f"角色={character_review.get('status')}, "
                f"逻辑={logic_review.get('status')}"
            )

            # 步骤5: 总编裁决（如需要）
            await self._report_event(on_event, "task_done", 3)
            await self._report_event(on_event, "task_done", 4)
            await self._report_event(on_event, "task_start", 5)
            if self._needs_revision(character_review, logic_review):
                final = await self.editor_agent.revise(
                    draft, character_review, logic_review, context
                )
                logger.info(f"[MultiAgent] 总编修订完成")
            else:
                final = {
                    "content": draft.get("content", ""),
                    "word_count": draft.get("word_count", 0),
                    "quality_score": 0.85,
                    "revision_summary": "无需修订",
                    "conflicts_resolved": []
                }

            await self._report_event(on_event, "task_done", 5)

            return {
                "content": final.get("content", ""),
                "word_count": final.get("word_count", 0),
                "quality_score": final.get("quality_score", 0.85),
                "outline": outline,
                "draft": draft,
                "character_review": character_review,
                "logic_review": logic_review,
                "revision_summary": final.get("revision_summary"),
                "conflicts_resolved": final.get("conflicts_resolved", [])
            }

        except Exception as e:
            logger.error(f"[MultiAgent] 执行失败: {e}", exc_info=True)
            raise

    def _needs_revision(self, char_review: Dict, logic_review: Dict) -> bool:
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
        elapsed_time: float = 0
    ):
        """报告事件"""
        if callback:
            if event_type == "task_start":
                await callback({"type": "task_start", "data": {"task_id": task_id}})
            elif event_type == "task_done":
                await callback({"type": "task_done", "data": {"task_id": task_id, "elapsed_time": elapsed_time}})
```

### 检查清单

- [ ] 实现 MultiAgentExecutor
- [ ] 实现 is_writing_task 判断逻辑
- [ ] 实现进度回调
- [ ] 集成测试

---

## 阶段5: 集成到 Planning 模式

### 目标
将 MultiAgentExecutor 集成到现有的任务执行流程中。

### 步骤

#### 5.1 修改任务执行逻辑

**文件**: `backend/app/services/agent/langgraph_agent.py`

> **重要**：实际集成点在 `_execute_tasks_in_parallel` 方法内的 `execute_with_semaphore` 闭包中，**不存在** `_execute_single_task` 方法。详见 [10-integration-details.md](./10-integration-details.md)

```python
from app.services.agent.multi_agent import MultiAgentExecutor

# 在 _execute_tasks_in_parallel 方法内部
async def _execute_tasks_in_parallel(self, tasks, work_id, chapter_id, context, ...):
    # 初始化 Multi-Agent 执行器
    multi_agent = MultiAgentExecutor(self.ai_service)

    async def execute_with_semaphore(task):
	        async with semaphore:
	            # 判断是否是写作类任务
	            if multi_agent.is_writing_task(task):
	                # 写作任务走Multi-Agent
	                ma_context = await self._build_multi_agent_context(work_id, chapter_id)

                async def on_ma_event(event: Dict[str, Any]):
                    if on_task_progress:
                        from app.models.chat_models import format_planning_event_to_sse
                        await on_task_progress(task, format_planning_event_to_sse(event))

                result = await multi_agent.execute(
                    task=task,
                    work_id=work_id,
                    chapter_id=chapter_id,
                    context=ma_context,
                    on_event=on_ma_event,  # 发送 plan/task_start/task_done/content
                )
	                return {
	                    "task_id": task.get("task_id"),
	                    "result": result["content"],
	                    "metadata": {
	                        "word_count": result["word_count"],
	                        "quality_score": result["quality_score"]
	                    }
	                }
	            else:
	                # 其他任务简单执行（原有逻辑）
	                return await self._execute_tool_call(task, work_id, chapter_id, context)
```

> 集成要求：MultiAgentExecutor 需按 05/10 文档的流程发送 `plan/task_start/task_done/content`，并带阶段耗时；`_build_multi_agent_context` 必须从 WorldviewService/VectorMemoryStore 拉取人设和前文。

### 检查清单

- [ ] 在 langgraph_agent.py 中导入 MultiAgentExecutor
- [ ] 在初始化中创建实例
- [ ] 在任务执行中添加判断逻辑
- [ ] 端到端测试

---

## 阶段6: 测试与调优

### 目标
确保系统稳定运行，优化性能。

### 测试用例

#### 6.1 单元测试

```python
# tests/test_multi_agent.py

import pytest
from unittest.mock import AsyncMock, MagicMock
from app.services.agent.multi_agent import MultiAgentExecutor


class TestMultiAgentExecutor:
    @pytest.fixture
    def mock_ai_service(self):
        """创建 mock AI 服务"""
        service = MagicMock()
        service.generate_text = AsyncMock(return_value={"text": '{"status": "PASS"}'})
        return service

    def test_is_writing_task(self, mock_ai_service):
        executor = MultiAgentExecutor(mock_ai_service)

        # 应该识别为写作任务
        assert executor.is_writing_task({"type": "write_chapter"})
        assert executor.is_writing_task({"description": "帮我写第三章"})
        assert executor.is_writing_task({"tool": "continue_writing_tool"})

        # 应该识别为非写作任务
        assert not executor.is_writing_task({"type": "search_content"})
        assert not executor.is_writing_task({"description": "查找角色信息"})
        assert not executor.is_writing_task({"tool": "get_context_tool"})

    @pytest.mark.asyncio
    async def test_execute_flow(self, mock_ai_service):
        """测试完整执行流程"""
        executor = MultiAgentExecutor(mock_ai_service)

        # 准备测试数据
        task = {"task_id": "1", "description": "写第三章", "chapter_id": "ch3"}
        context = {
            "character_document": "角色A: 性格开朗...",
            "previous_summary": "第二章摘要..."
        }

        # Mock 各 Agent 的响应
        executor.outline_agent.generate = AsyncMock(return_value={
            "chapter_id": "ch3",
            "title": "测试章节",
            "core_conflict": "测试冲突"
        })
        executor.writer_agent.write = AsyncMock(return_value={
            "content": "测试内容...",
            "word_count": 1500
        })
        executor.character_guard.check = AsyncMock(return_value={
            "status": "PASS", "issues": []
        })
        executor.logic_auditor.check = AsyncMock(return_value={
            "status": "PASS", "issues": []
        })

        # 执行
        result = await executor.execute(task, "work_1", "ch3", context)

        # 验证
        assert "content" in result
        assert result["word_count"] > 0
        executor.outline_agent.generate.assert_called_once()
        executor.writer_agent.write.assert_called_once()

    @pytest.mark.asyncio
    async def test_execute_with_revision(self, mock_ai_service):
        """测试需要修订的情况"""
        executor = MultiAgentExecutor(mock_ai_service)

        # Mock 返回需要修订
        executor.outline_agent.generate = AsyncMock(return_value={"chapter_id": "ch3"})
        executor.writer_agent.write = AsyncMock(return_value={"content": "初稿", "word_count": 1000})
        executor.character_guard.check = AsyncMock(return_value={
            "status": "NEED_REVISION",
            "issues": [{"type": "性格偏离", "description": "测试问题"}]
        })
        executor.logic_auditor.check = AsyncMock(return_value={"status": "PASS", "issues": []})
        executor.editor_agent.revise = AsyncMock(return_value={
            "content": "修订后内容",
            "word_count": 1100
        })

        result = await executor.execute({}, "work_1", "ch3", {})

        # 验证总编被调用
        executor.editor_agent.revise.assert_called_once()
```

#### 6.2 集成测试

- 测试 Planning → Multi-Agent 完整链路
- 测试错误处理
- 测试进度回调

### 调优方向

1. **Prompt 调优**：根据实际输出调整各 Agent 的 Prompt
2. **并行优化**：优化角色守护和逻辑审计的并行执行
3. **缓存优化**：缓存人设文档、前文摘要等
4. **超时处理**：添加各阶段的超时保护

### 检查清单

- [ ] 编写单元测试
- [ ] 编写集成测试
- [ ] 性能测试
- [ ] Prompt 调优
- [ ] 文档更新

---

## 完成标准

| 项目 | 标准 |
|------|------|
| 代码完成 | 所有 Agent 实现并通过测试 |
| 集成完成 | Multi-Agent 成功集成到 Planning 模式 |
| 测试覆盖 | 核心逻辑测试覆盖率 > 80% |
| 文档完成 | API 文档和使用说明完成 |

---

## 相关文档

- [03-multi-agent-design.md](./03-multi-agent-design.md) - 架构设计
- [05-code-structure.md](./05-code-structure.md) - 代码结构
- [06-api-design.md](./06-api-design.md) - API设计
