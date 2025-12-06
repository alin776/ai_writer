# Multi-Agent 前端UI设计

> 文档版本: 2.0
> 更新日期: 2025-12-06
> 状态: **已确认方案**

---

## 核心结论

**Multi-Agent 100% 复用 Planning 模式的前端 UI，无需开发新组件。**

---

## 方案说明

### 现有 Planning 模式机制

```
后端 SSE 事件              前端处理                    UI 展示
─────────────              ────────                    ──────
plan (任务列表)     →    onPlan()      →    TaskListPanel 初始化
task_start          →    onTaskStart() →    标记任务"运行中"
task_done           →    onTaskDone()  →    标记任务"已完成"
content             →    onContent()   →    流式输出内容
```

### Multi-Agent 复用方式

将 5 个 Agent 阶段映射为 5 个 Planning 任务：

| Agent 阶段 | 映射为 Task |
|-----------|-------------|
| 大纲师 | `{task_id: 1, description: "生成章节大纲", tool: "outline_agent"}` |
| 主笔 | `{task_id: 2, description: "撰写初稿", tool: "writer_agent"}` |
| 角色守护 | `{task_id: 3, description: "审核人设一致性", tool: "character_guard"}` |
| 逻辑审计 | `{task_id: 4, description: "检查剧情逻辑", tool: "logic_auditor"}` |
| 总编 | `{task_id: 5, description: "裁决修订定稿", tool: "editor_agent"}` |

---

## 前端展示效果

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

### 总编跳过时的处理

> **设计决策**：即使校验通过（无需修订），总编任务也会执行并标记完成，以保持前端 UI 的一致性。

| 场景 | 行为 | 前端显示 |
|------|------|---------|
| 需要修订 | 执行完整总编流程 | ✓ 8.5s |
| 无需修订 | 快速标记完成 | ✓ 0.1s |

**原因**：
- 前端任务列表始终显示 5 个任务
- 如果跳过总编，第 5 个任务会一直显示"待执行"状态
- 用户会困惑为什么任务没有完成

---

## 后端实现要求

### 1. 发送任务计划

Multi-Agent 启动时，发送 `plan` 事件：

```python
# multi_agent/executor.py

async def execute(self, task, work_id, chapter_id, context, on_event=None):
    """执行 Multi-Agent 流程"""

    # 1. 发送任务计划（复用 Planning 的 plan 事件）
    if on_event:
        await on_event({
            "type": "plan",
            "data": {
                "tasks": [
                    {"task_id": 1, "description": "生成章节大纲", "tool": "outline_agent"},
                    {"task_id": 2, "description": "撰写初稿", "tool": "writer_agent"},
                    {"task_id": 3, "description": "审核人设一致性", "tool": "character_guard"},
                    {"task_id": 4, "description": "检查剧情逻辑", "tool": "logic_auditor"},
                    {"task_id": 5, "description": "裁决修订定稿", "tool": "editor_agent"},
                ]
            }
        })

    # 2. 执行各阶段...
```

### 2. 发送阶段开始/完成事件

```python
# 阶段开始
async def _execute_stage(self, stage_id, stage_name, agent_func, on_event):
    # 发送 task_start（复用 Planning 事件）
    if on_event:
        await on_event({
            "type": "task_start",
            "data": {"task_id": stage_id}
        })

    start_time = time.time()

    # 执行 Agent
    result = await agent_func()

    elapsed = time.time() - start_time

    # 发送 task_done（复用 Planning 事件）
    if on_event:
        await on_event({
            "type": "task_done",
            "data": {
                "task_id": stage_id,
                "elapsed_time": elapsed
            }
        })

    return result
```

### 3. 并行审核的处理

角色守护和逻辑审计并行执行时，两个任务同时标记为"运行中"：

```python
# 并行执行审核
async def _execute_parallel_review(self, draft, work_id, context, on_event):
    # 同时发送两个 task_start
    if on_event:
        await on_event({"type": "task_start", "data": {"task_id": 3}})
        await on_event({"type": "task_start", "data": {"task_id": 4}})

    start_time = time.time()

    # 并行执行
    character_review, logic_review = await asyncio.gather(
        self.character_guard.check(draft, work_id, context),
        self.logic_auditor.check(draft, work_id, context)
    )

    elapsed = time.time() - start_time

    # 同时发送两个 task_done
    if on_event:
        await on_event({"type": "task_done", "data": {"task_id": 3, "elapsed_time": elapsed}})
        await on_event({"type": "task_done", "data": {"task_id": 4, "elapsed_time": elapsed}})

    return character_review, logic_review
```

---

## 完整执行流程

```python
async def execute(self, task, work_id, chapter_id, context, on_event=None):
    """Multi-Agent 完整执行流程"""

    # 1. 发送任务计划
    await self._send_plan(on_event)

    # 2. 大纲师
    outline = await self._execute_stage(
        stage_id=1,
        stage_name="outline",
        agent_func=lambda: self.outline_agent.generate(task, context),
        on_event=on_event
    )

    # 3. 主笔
    draft = await self._execute_stage(
        stage_id=2,
        stage_name="writing",
        agent_func=lambda: self.writer_agent.write(outline, context),
        on_event=on_event
    )

    # 4. 并行审核（角色守护 + 逻辑审计）
    character_review, logic_review = await self._execute_parallel_review(
        draft, work_id, context, on_event
    )

    # 5. 总编（即使不需要修订也要执行，保持 UI 一致性）
    if self._needs_revision(character_review, logic_review):
        # 需要修订：执行完整总编流程
        final = await self._execute_stage(
            stage_id=5,
            stage_name="editor",
            agent_func=lambda: self.editor_agent.revise(
                draft, character_review, logic_review, context
            ),
            on_event=on_event
        )
    else:
        # 无需修订：快速完成总编任务（直接使用初稿）
        await self._emit_task_start(on_event, 5)
        final = {"content": draft["content"], "word_count": draft["word_count"]}
        await self._emit_task_done(on_event, 5, 0.1)  # 快速标记完成

    # 6. 发送最终内容
    if on_event:
        await on_event({
            "type": "content",
            "data": final.get("content", "")
        })

    return final
```

---

## 改动清单

| 模块 | 需要改动？ | 说明 |
|------|-----------|------|
| **前端 TaskListPanel** | ❌ 不需要 | 直接复用 |
| **前端 useAgentChat** | ❌ 不需要 | 直接复用 |
| **前端 agentApi** | ❌ 不需要 | 直接复用 |
| **前端 AgentChatPanel** | ❌ 不需要 | 直接复用 |
| **后端 MultiAgentExecutor** | ✅ 需要 | 发送 plan/task_start/task_done 事件 |
| **后端 langgraph_agent** | ✅ 需要 | 集成 MultiAgentExecutor |

---

## 事件格式参考

### plan 事件

```json
{
  "type": "plan",
  "data": {
    "tasks": [
      {
        "task_id": 1,
        "description": "生成章节大纲",
        "tool": "outline_agent",
        "estimated_time": "2-3s"
      }
    ]
  }
}
```

### task_start 事件

```json
{
  "type": "task_start",
  "data": {
    "task_id": 1
  }
}
```

### task_done 事件

```json
{
  "type": "task_done",
  "data": {
    "task_id": 1,
    "elapsed_time": 2.1
  }
}
```

### content 事件

```json
{
  "type": "content",
  "data": "最终生成的章节内容..."
}
```

---

## 相关文件

| 文件 | 用途 |
|------|------|
| `src/components/agent/TaskListPanel.tsx` | 任务列表UI组件（复用） |
| `src/hooks/useAgentChat.ts` | 处理SSE事件（复用） |
| `src/services/agentApi.ts` | API调用（复用） |
| `backend/app/services/agent/multi_agent/executor.py` | Multi-Agent执行器（新增） |

---

## 相关文档

- [07-implementation-steps.md](./07-implementation-steps.md) - 实施步骤
- [10-integration-details.md](./10-integration-details.md) - 集成细节
