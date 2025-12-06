# Multi-Agent 集成细节

> 文档版本: 2.0
> 更新日期: 2025-12-06
> 状态: **已更新 - 复用 Planning 模式 UI**

---

## 概述

本文档详细说明 Multi-Agent 与现有系统的集成细节，包括依赖模块、数据流、事件格式等。

---

## 依赖模块清单

### 1. AI 服务

```python
from app.services.ai.http_ai_service import HTTPAIService

# 用途：所有 Agent 的 LLM 调用
# 获取方式：通过构造函数注入
```

### 2. 世界观服务（获取人设）

```python
from app.services.worldview_service import WorldviewService

# 用途：获取角色、地点、设定信息
# 使用示例：
async with create_db_session() as db:
    worldview_service = WorldviewService(db)
    characters = await worldview_service.get_characters_by_work(work_id)
    locations = await worldview_service.get_locations_by_work(work_id)
    settings = await worldview_service.get_settings_by_work(work_id)
```

### 3. 上下文管理

```python
from app.services.context import ContextManager, VectorMemoryStore

# 用途：
# - ContextManager: 管理对话上下文
# - VectorMemoryStore: 检索相关前文内容
```

### 4. 数据库会话

```python
from app.core.database import create_db_session

# 用途：获取数据库会话
# 注意：每个操作使用独立会话，避免连接泄漏
async with create_db_session() as db:
    # 使用 db
    pass
```

### 5. 事件格式化

```python
from app.models.chat_models import format_planning_event_to_sse

# 用途：将进度事件格式化为 SSE
# Multi-Agent 应使用 Planning 模式的事件格式
```

---

## 数据获取详细流程

### 获取人设文档

```python
async def _get_character_document(self, work_id: str) -> str:
    """获取作品的人设文档"""
    from app.core.database import create_db_session
    from app.services.worldview_service import WorldviewService

    async with create_db_session() as db:
        worldview_service = WorldviewService(db)
        characters = await worldview_service.get_characters_by_work(work_id)

        if not characters:
            return "（无角色设定）"

        # 格式化角色信息
        doc_lines = ["# 角色设定\n"]
        for char in characters:
            doc_lines.append(f"## {char.name}")
            if char.description:
                doc_lines.append(f"描述：{char.description}")
            if hasattr(char, 'personality') and char.personality:
                doc_lines.append(f"性格：{char.personality}")
            if hasattr(char, 'catchphrase') and char.catchphrase:
                doc_lines.append(f"口头禅：{char.catchphrase}")
            doc_lines.append("")

        return "\n".join(doc_lines)
```

### 获取前文摘要

```python
async def _get_previous_summary(self, work_id: str, chapter_id: str) -> str:
    """获取前文摘要"""
    from app.services.context import VectorMemoryStore, get_vector_memory_store

    # 方案1：使用向量检索
    vector_store = get_vector_memory_store()
    if vector_store:
        results = await vector_store.search(
            query=f"work:{work_id} 前文摘要",
            top_k=5
        )
        if results:
            return "\n".join([r.content for r in results])

    # 方案2：从章节服务获取
    # （如果有章节摘要服务的话）

    return "（无前文摘要）"
```

### 获取章节内容

```python
async def _get_chapter_content(self, chapter_id: str) -> str:
    """获取章节内容"""
    from app.core.database import create_db_session
    from app.services.chapter_service import ChapterService

    async with create_db_session() as db:
        chapter_service = ChapterService(db)
        chapter = await chapter_service.get_chapter_by_id(chapter_id)
        if chapter:
            return chapter.content or ""
        return ""
```

---

## 正确的集成位置

### 位置：`_execute_tasks_in_parallel` 方法内部

```python
# langgraph_agent.py

async def _execute_tasks_in_parallel(
    self,
    tasks: List[Dict[str, Any]],
    work_id: str,
    chapter_id: str,
    context: Dict[str, Any],
    on_task_start: Optional[callable] = None,
    on_task_progress: Optional[callable] = None,
    on_task_done: Optional[callable] = None,
) -> List[Dict[str, Any]]:

    # 🆕 初始化 Multi-Agent 执行器
    from app.services.agent.multi_agent import MultiAgentExecutor
    multi_agent = MultiAgentExecutor(self.ai_service)

    # ... 现有的任务分组逻辑 ...

    async def execute_with_semaphore(task):
        async with semaphore:
            task_id = task["task_id"]
            tool_name = task.get("tool", "unknown")

            # 🆕 判断是否是写作类任务
            if multi_agent.is_writing_task(task):
                logger.info(f"[MultiAgent] 任务{task_id}使用Multi-Agent流程")

                # 构建上下文
                ma_context = await self._build_multi_agent_context(work_id, chapter_id)

                # 进度回调适配：Multi-Agent 发出的 plan/task_start/task_done/content
                # 事件需格式化为 Planning SSE，前端才能复用 TaskListPanel
                async def on_ma_event(event: Dict[str, Any]):
                    if on_task_progress:
                        from app.models.chat_models import format_planning_event_to_sse
                        await on_task_progress(task, format_planning_event_to_sse(event))

                # 执行 Multi-Agent 流程
                result = await multi_agent.execute(
                    task=task,
                    work_id=work_id,
                    chapter_id=chapter_id,
                    context=ma_context,
                    on_event=on_ma_event,
                )

                return {
                    "task_id": task_id,
                    "description": task.get("description"),
                    "tool": "multi_agent",
                    "result": result["content"],
                    "status": "completed",
                    "metadata": {
                        "word_count": result.get("word_count"),
                        "quality_score": result.get("quality_score")
                    }
                }
            else:
                # 🔄 原有的简单执行逻辑
                # ...
```

### 辅助方法：构建 Multi-Agent 上下文

```python
async def _build_multi_agent_context(
    self,
    work_id: str,
    chapter_id: str,
) -> Dict[str, Any]:
    """构建 Multi-Agent 所需的上下文"""
    context: Dict[str, Any] = {}

    # 获取人设文档
    try:
        context["character_document"] = await self._get_character_document(work_id)
    except Exception as e:
        logger.warning(f"获取人设文档失败: {e}")
        context["character_document"] = ""

    # 获取前文摘要
    try:
        context["previous_summary"] = await self._get_previous_summary(work_id, chapter_id)
    except Exception as e:
        logger.warning(f"获取前文摘要失败: {e}")
        context["previous_summary"] = ""

    # 获取总纲（如果有）
    try:
        context["total_outline"] = await self._get_work_outline(work_id)
    except AttributeError:
        logger.info("未实现 _get_work_outline，返回空总纲")
        context["total_outline"] = ""
    except Exception as e:
        logger.warning(f"获取总纲失败: {e}")
        context["total_outline"] = ""

    return context
```

---

## 进度事件格式（复用 Planning 模式）

### 核心原则

**Multi-Agent 直接复用 Planning 模式的 SSE 事件格式，前端无需任何改动。**

### 事件类型

| 事件类型 | 用途 | 发送时机 |
|---------|------|---------|
| `plan` | 初始化任务列表 | Multi-Agent 启动时 |
| `task_start` | 标记任务开始 | 每个 Agent 阶段开始时 |
| `task_done` | 标记任务完成 | 每个 Agent 阶段完成时 |
| `content` | 输出最终内容 | 总编完成后 |

### 事件发送示例

```python
# multi_agent/executor.py

class MultiAgentExecutor:
    """Multi-Agent 执行器"""

    # 任务定义
    STAGE_TASKS = [
        {"task_id": 1, "description": "生成章节大纲", "tool": "outline_agent"},
        {"task_id": 2, "description": "撰写初稿", "tool": "writer_agent"},
        {"task_id": 3, "description": "审核人设一致性", "tool": "character_guard"},
        {"task_id": 4, "description": "检查剧情逻辑", "tool": "logic_auditor"},
        {"task_id": 5, "description": "裁决修订定稿", "tool": "editor_agent"},
    ]

    async def execute(self, task, work_id, chapter_id, context, on_event=None):
        """执行 Multi-Agent 流程"""

        # 1. 发送任务计划
        if on_event:
            await on_event({
                "type": "plan",
                "data": {"tasks": self.STAGE_TASKS}
            })

        # 2. 大纲师
        await self._emit_task_start(on_event, 1)
        start = time.time()
        outline = await self.outline_agent.generate(task, context)
        await self._emit_task_done(on_event, 1, time.time() - start)

        # 3. 主笔
        await self._emit_task_start(on_event, 2)
        start = time.time()
        draft = await self.writer_agent.write(outline, context)
        await self._emit_task_done(on_event, 2, time.time() - start)

        # 4. 并行审核
        await self._emit_task_start(on_event, 3)
        await self._emit_task_start(on_event, 4)
        start = time.time()
        char_review, logic_review = await asyncio.gather(
            self.character_guard.check(draft, work_id, context),
            self.logic_auditor.check(draft, work_id, context)
        )
        elapsed = time.time() - start
        await self._emit_task_done(on_event, 3, elapsed)
        await self._emit_task_done(on_event, 4, elapsed)

        # 5. 总编
        await self._emit_task_start(on_event, 5)
        start = time.time()
        final = await self.editor_agent.revise(draft, char_review, logic_review, context)
        await self._emit_task_done(on_event, 5, time.time() - start)

        # 6. 发送最终内容
        if on_event:
            await on_event({
                "type": "content",
                "data": final.get("content", "")
            })

        return final

    async def _emit_task_start(self, on_event, task_id):
        if on_event:
            await on_event({"type": "task_start", "data": {"task_id": task_id}})

    async def _emit_task_done(self, on_event, task_id, elapsed_time):
        if on_event:
            await on_event({
                "type": "task_done",
                "data": {"task_id": task_id, "elapsed_time": elapsed_time}
            })
```

### 前端自动展示

发送上述事件后，前端 `TaskListPanel` 自动展示：

```
┌─────────────────────────────────────────┐
│ 执行计划                        3/5     │
├─────────────────────────────────────────┤
│ ● 生成章节大纲              ✓ 2.1s      │
│ ● 撰写初稿                  ✓ 8.3s      │
│ ◉ 审核人设一致性            运行中       │
│ ◉ 检查剧情逻辑              运行中       │
│ ○ 裁决修订定稿              待执行       │
├─────────────────────────────────────────┤
│ ████████████░░░░░░░░  60%              │
└─────────────────────────────────────────┘
```

---

## 错误处理策略

### 各 Agent 的错误处理

```python
class MultiAgentExecutor:

    async def execute(self, task, work_id, chapter_id, context, on_event=None):
        try:
            # 步骤1: 大纲师
            outline = await self._safe_execute_agent(
                self.outline_agent.generate,
                task, context,
                fallback=self._default_outline(task)
            )

            # 步骤2: 主笔
            draft = await self._safe_execute_agent(
                self.writer_agent.write,
                outline, context,
                fallback=None  # 主笔失败则整体失败
            )

            # 步骤3&4: 校验（失败不影响主流程）
            character_review = await self._safe_execute_agent(
                self.character_guard.check,
                draft, work_id, context,
                fallback={"status": "PASS", "issues": []}
            )

            # ...

        except Exception as e:
            logger.error(f"[MultiAgent] 执行失败: {e}")
            raise

    async def _safe_execute_agent(self, func, *args, fallback=None):
        """安全执行 Agent，支持降级"""
        try:
            return await func(*args)
        except Exception as e:
            logger.warning(f"[MultiAgent] Agent执行失败: {e}")
            if fallback is not None:
                return fallback
            raise
```

### 重试策略

```python
async def _execute_with_retry(self, func, *args, max_retries=2):
    """带重试的执行"""
    last_error = None

    for retry in range(max_retries + 1):
        try:
            return await func(*args)
        except Exception as e:
            last_error = e

            # 判断是否可重试
            is_retryable = any(kw in str(e).lower() for kw in [
                "timeout", "connection", "network", "rate_limit"
            ])

            if is_retryable and retry < max_retries:
                wait_time = 2 ** (retry + 1)
                logger.warning(f"[MultiAgent] 重试 {retry+1}/{max_retries}，等待 {wait_time}s")
                await asyncio.sleep(wait_time)
            else:
                break

    raise last_error
```

---

## 超时配置

### 各阶段超时时间

| 阶段 | 默认超时 | 说明 |
|------|---------|------|
| 大纲师 | 30s | 结构化输出，较快 |
| 主笔 | 120s | 生成长文本，需要较长时间 |
| 角色守护 | 30s | 校验任务，较快 |
| 逻辑审计 | 30s | 校验任务，较快 |
| 总编 | 60s | 可能需要修改内容 |
| **整体超时** | 300s | 整个 Multi-Agent 流程 |

### 超时实现

```python
import asyncio

class MultiAgentExecutor:
    # 超时配置
    STAGE_TIMEOUTS = {
        "outline": 30,
        "writing": 120,
        "character_guard": 30,
        "logic_auditor": 30,
        "editor": 60,
    }
    TOTAL_TIMEOUT = 300

    async def execute(self, task, work_id, chapter_id, context, on_event=None):
        """执行 Multi-Agent 流程（带超时）"""
        try:
            return await asyncio.wait_for(
                self._execute_internal(task, work_id, chapter_id, context, on_event),
                timeout=self.TOTAL_TIMEOUT
            )
        except asyncio.TimeoutError:
            logger.error("[MultiAgent] 整体执行超时")
            raise TimeoutError("Multi-Agent 执行超时，请稍后重试")

    async def _execute_stage_with_timeout(self, stage_name, coro):
        """带超时的阶段执行"""
        timeout = self.STAGE_TIMEOUTS.get(stage_name, 60)
        try:
            return await asyncio.wait_for(coro, timeout=timeout)
        except asyncio.TimeoutError:
            logger.error(f"[MultiAgent] {stage_name} 阶段超时")
            raise TimeoutError(f"{stage_name} 执行超时")
```

---

## 回退机制

### 回退策略

当 Multi-Agent 流程失败时，系统应该能够优雅降级：

| 场景 | 回退行为 |
|------|---------|
| 大纲师失败 | 使用简单大纲模板 |
| 主笔失败 | **终止流程**（核心步骤不可跳过） |
| 角色守护失败 | 跳过校验，继续流程 |
| 逻辑审计失败 | 跳过校验，继续流程 |
| 总编失败 | 直接使用初稿 |

### 回退实现

```python
class MultiAgentExecutor:

    async def execute(self, task, work_id, chapter_id, context, on_event=None):
        """带回退的 Multi-Agent 流程"""

        # 1. 大纲师（可回退）
        try:
            outline = await self.outline_agent.generate(task, context)
        except Exception as e:
            logger.warning(f"[MultiAgent] 大纲生成失败，使用默认大纲: {e}")
            outline = self._default_outline(task)

        # 2. 主笔（不可回退）
        draft = await self.writer_agent.write(outline, context)

        # 3&4. 校验（可回退）
        try:
            character_review, logic_review = await asyncio.gather(
                self.character_guard.check(draft, work_id, context),
                self.logic_auditor.check(draft, work_id, context),
                return_exceptions=True  # 允许部分失败
            )
            # 处理异常结果
            if isinstance(character_review, Exception):
                logger.warning(f"[MultiAgent] 角色校验失败: {character_review}")
                character_review = {"status": "PASS", "issues": []}
            if isinstance(logic_review, Exception):
                logger.warning(f"[MultiAgent] 逻辑校验失败: {logic_review}")
                logic_review = {"status": "PASS", "issues": []}
        except Exception as e:
            logger.warning(f"[MultiAgent] 校验阶段失败: {e}")
            character_review = {"status": "PASS", "issues": []}
            logic_review = {"status": "PASS", "issues": []}

        # 5. 总编（可回退）
        if self._needs_revision(character_review, logic_review):
            try:
                final = await self.editor_agent.revise(draft, character_review, logic_review, context)
            except Exception as e:
                logger.warning(f"[MultiAgent] 总编修订失败，使用初稿: {e}")
                final = draft
        else:
            final = draft

        return final

    def _default_outline(self, task) -> Dict[str, Any]:
        """默认大纲模板（回退用）"""
        return {
            "chapter_id": task.get("chapter_id", "unknown"),
            "title": task.get("description", "未命名章节"),
            "core_conflict": "待定",
            "characters": [],
            "emotion_curve": {"start": "平静", "mid": "高潮", "end": "收尾"},
            "foreshadowing": "",
            "connection_to_previous": ""
        }
```

---

## 测试要点

### 单元测试

```python
# tests/test_multi_agent.py

@pytest.mark.asyncio
async def test_is_writing_task():
    """测试写作任务判断"""
    executor = MultiAgentExecutor(mock_ai_service)

    # 应该识别为写作任务
    assert executor.is_writing_task({"type": "write_chapter"})
    assert executor.is_writing_task({"description": "帮我写第三章"})
    assert executor.is_writing_task({"tool": "continue_writing_tool"})

    # 不应该识别为写作任务
    assert not executor.is_writing_task({"type": "search"})
    assert not executor.is_writing_task({"tool": "get_context_tool"})


@pytest.mark.asyncio
async def test_execute_flow_with_mock():
    """测试完整流程（使用 mock）"""
    # Mock AI 服务
    mock_ai = MockAIService()
    executor = MultiAgentExecutor(mock_ai)

    task = {"task_id": "1", "description": "写第三章"}
    context = {"character_document": "角色A...", "previous_summary": "..."}

    result = await executor.execute(task, "work_1", "chapter_3", context)

    assert "content" in result
    assert result["word_count"] > 0
```

### 集成测试

```python
@pytest.mark.asyncio
async def test_integration_with_planning():
    """测试与 Planning 模式的集成"""
    # 需要真实的数据库和 AI 服务
    pass
```

---

## 相关文档

- [05-code-structure.md](./05-code-structure.md) - 代码结构
- [07-implementation-steps.md](./07-implementation-steps.md) - 实施步骤
- [09-review-findings.md](./09-review-findings.md) - Review 发现
