# 文档 Review 补充 - 发现的问题与更新

> 文档版本: 1.0
> 创建日期: 2025-12-06
> 状态: Review 结果

---

## 深度 Review 发现的问题

通过对项目代码的深入探索，发现以下文档遗漏和需要更正的问题。

---

## 问题1: 集成点描述不准确

### 原文档描述（04/05/07）

```python
# 文档说在 _execute_single_task 中集成
async def _execute_single_task(self, task, ...):
    if self._is_writing_task(task):
        return await self._execute_with_multi_agent(...)
```

### 实际代码情况

**实际上不存在 `_execute_single_task` 方法**，任务执行逻辑在 `_execute_tasks_in_parallel` 中。

```python
# 实际代码结构 (langgraph_agent.py:4161)
async def _execute_tasks_in_parallel(self, tasks, ...):
    # 分组任务
    for task in tasks:
        if tool_name in PARALLEL_SAFE_TOOLS:
            parallel_tasks.append(task)
        else:
            sequential_tasks.append(task)

    # 并行执行 (使用 execute_with_semaphore 闭包)
    async def execute_with_semaphore(task):
        # 这里是实际执行单个任务的地方
        ...
```

### 更正方案

Multi-Agent 应该集成到 `execute_with_semaphore` 闭包内部，或者在任务分组时将写作任务单独处理。

---

## 问题2: 人设文档获取方式未说明

### 原文档描述

```python
context = {
    "character_document": "人设文档...",  # 哪里获取？
    "previous_summary": "前文摘要...",    # 哪里获取？
}
```

### 实际代码中的数据源

**发现了以下现有服务可用**：

1. **WorldviewService** (`langgraph_agent.py:881-898`)
   ```python
   from app.services.worldview_service import WorldviewService
   worldview_service = WorldviewService(db)

   characters = await worldview_service.get_characters_by_work(work_id)
   locations = await worldview_service.get_locations_by_work(work_id)
   settings = await worldview_service.get_settings_by_work(work_id)
   ```

2. **get_context_tool** (`langgraph_agent.py:938`)
   - 已有工具可获取作品上下文（包含角色、地点、设定）

3. **VectorMemoryStore** (`context/__init__.py:25`)
   - 向量存储，可用于检索相关内容

### 更正方案

文档需要补充说明：
- 使用 `WorldviewService` 获取角色设定
- 使用 `get_context_tool` 的逻辑作为参考
- 使用 `VectorMemoryStore` 检索相关前文

---

## 问题3: 进度事件格式与现有系统不兼容

### 原文档设计

```python
# 文档中的进度事件
{
    "step": "outline" | "writing" | "review" | "editing" | "complete",
    "status": "running" | "done" | "error"
}
```

### 实际前端期望的事件

**Planning 模式事件** (`chat_models.py:83-105`, `agentApi.ts:250-268`):
```javascript
// 前端处理的事件类型
case 'plan':       // 规划完成
case 'task_start': // 任务开始
case 'task_progress': // 任务进度
case 'task_done':  // 任务完成
case 'content':    // 内容生成
```

### 更正方案

Multi-Agent 的进度应该映射到现有的 Planning 模式事件：

| Multi-Agent 阶段 | 映射到 Planning 事件 |
|-----------------|---------------------|
| outline | task_start (大纲任务) |
| writing | task_start (写作任务) |
| review | task_start (校验任务) |
| editing | task_start (修订任务) |
| complete | task_done |

---

## 问题4: 缺少对现有模块的依赖说明

### 需要依赖的现有模块

| 模块 | 用途 | 位置 |
|------|------|------|
| `WorldviewService` | 获取角色、地点、设定 | `app.services.worldview_service` |
| `ContextManager` | 上下文管理 | `app.services.context` |
| `VectorMemoryStore` | 向量检索 | `app.services.context.vector_memory_store` |
| `HTTPAIService` | AI调用 | `app.services.ai.http_ai_service` |
| `ParameterResolver` | 参数解析 | `app.services.agent.parameter_resolver` |
| `format_planning_event_to_sse` | 事件格式化 | `app.models.chat_models` |

### 需要复用的现有工具

| 工具 | 用途 |
|------|------|
| `get_context_tool` | 获取作品上下文 |
| `read_chapter_tool` | 读取章节内容 |
| `search_analysis_fragments_tool` | 搜索分析片段 |

---

## 问题5: 数据库会话管理未说明

### 现有代码的数据库会话模式

```python
# langgraph_agent.py 中的模式
from app.core.database import create_db_session

async with create_db_session() as db:
    # 使用 db
    worldview_service = WorldviewService(db)
```

### Multi-Agent 需要注意

- 每个 Agent 方法需要获取独立的 db 会话
- 避免跨 Agent 共享 db 会话
- 需要正确处理事务和连接关闭

---

## 问题6: 并行安全工具列表需要更新

### 现有并行安全工具 (`langgraph_agent.py:4205-4211`)

```python
PARALLEL_SAFE_TOOLS = {
    "get_context_tool",
    "read_chapter_tool",
    "get_chapter_by_order_tool",
    "search_analysis_fragments_tool",
    "analyze_text_tool"
}
```

### Multi-Agent 需要考虑

写作任务**不应该**被标记为并行安全，因为 Multi-Agent 流程是**串行**的（大纲 → 写作 → 校验 → 裁决）。

---

## 问题7: 缺少错误处理和重试机制设计

### 现有代码的重试机制 (`langgraph_agent.py:4265-4323`)

```python
max_retries = 2
for retry_count in range(max_retries + 1):
    try:
        # 执行任务
    except Exception as e:
        is_retryable = any(keyword in str(e).lower() for keyword in [
            "timeout", "connection", "network"
        ])
        if is_retryable and retry_count < max_retries:
            wait_time = 2 ** (retry_count + 1)  # 指数退避
            await asyncio.sleep(wait_time)
```

### Multi-Agent 需要补充

文档中缺少各 Agent 的错误处理和重试策略设计。

---

## 更新清单

| 文档 | 需要更新的内容 |
|------|---------------|
| **05-code-structure.md** | 更正集成点说明 |
| **06-api-design.md** | 添加依赖模块说明 |
| **07-implementation-steps.md** | 更正集成代码示例 |
| **08-prompt-templates.md** | 无需更改 |
| **新增 09-integration-details.md** | 详细集成说明 |

---

## 下一步行动

1. 更新 05/06/07 文档中的错误描述
2. 创建新文档 `09-integration-details.md` 详细说明集成细节
3. 补充错误处理和重试机制设计
