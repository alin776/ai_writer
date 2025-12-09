# 05 - 事件协议

> DeepAgent 模式的 SSE 事件协议，提供两种方案：复用 task_progress（推荐）或新增 reflection 事件

## 0. 方案选择

| 方案 | 前端改动 | 推荐场景 |
|------|----------|----------|
| **方案A: 复用 task_progress** | **0 行** | MVP、快速迭代 |
| 方案B: 新增 reflection 事件 | ~25 行 | 完整版、需要专属样式 |

**推荐方案 A**，原因：
- 前端已有 `onTaskProgress` 回调处理
- Task 接口已有 `progress_status` 字段
- TaskListPanel 已能显示进度状态
- 零改动，零风险

## 1. 事件概览

### 1.1 事件类型

| 事件类型 | 说明 | 发送时机 | MVP | 完整版 |
|---------|------|----------|-----|--------|
| `plan` | 任务列表 | 规划完成 / 重规划后 | ✅ | ✅ |
| `task_start` | 任务开始 | 执行任务前 | ✅ | ✅ |
| `task_progress` | 进度/反思 | Multi-Agent进度 / 反思后 | ✅ **发送反思** | ✅ |
| `task_done` | 任务完成 | 任务执行后 | ✅ | ✅ |
| `reflection` | 反思内容 | think_tool 执行后 | ❌ 不使用 | ✅ 可选 |
| `content` | 文本内容 | 流式输出 | ✅ | ✅ |
| `done` | 完成 | 全部结束 | ✅ | ✅ |
| `error` | 错误 | 发生错误时 | ✅ | ✅ |

### 1.2 事件传输

```
后端 (SSE Stream) ──────────────────► 前端 (useAgentChat)
                                         │
事件格式:                                 │
data: {"type": "plan", ...}              ▼
data: {"type": "task_start", ...}    TaskListPanel
data: {"type": "task_progress", ...} (progress_status 显示反思)  ← MVP复用
data: {"type": "task_done", ...}
data: {"type": "content", ...}       AgentMessage
```

---

## 2. 方案A：复用 task_progress（推荐）

### 2.1 事件格式

```json
{
  "type": "task_progress",
  "data": {
    "task_id": 1,
    "status": "💭 反思: 分析发现3个伏笔，但血神宫线索不完整，需要补充分析。"
  }
}
```

### 2.2 后端发送

```python
# deep_agent/executor.py

async def _do_reflection(self, task, result, remaining_tasks, context):
    reflection_result = await think_tool(...)

    # MVP方案：复用现有的 task_progress 事件
    if self.on_task_progress:
        await self.on_task_progress(
            task,
            f"💭 反思: {reflection_result.reflection}"
        )

    return reflection_result
```

### 2.3 前端处理（无需改动）

现有代码已支持：

```typescript
// useAgentChat.ts:327-338 - 已有代码，无需修改

onTaskProgress: (progress: any) => {
  const taskId = progress.task_id;
  const status = progress.status;
  if (taskId !== undefined && status) {
    sessionManager.updateSession(sessionId, {
      tasks: (sessionManager.getSession(sessionId)?.tasks || []).map((t) =>
        t.task_id === taskId ? { ...t, progress_status: status } : t
      )
    });
  }
}
```

```typescript
// Task 接口 - 已有字段，无需修改
interface Task {
  task_id: number;
  description: string;
  status: 'pending' | 'running' | 'completed' | 'failed';
  progress_status?: string;  // ← 自动显示反思内容
}
```

### 2.4 显示效果

```
┌─────────────────────────────────────┐
│ ● 分析前文伏笔                  1.2s │
│   💭 反思: 发现3个伏笔...           │  ← progress_status 自动显示
│                                     │
│ ◐ 生成章节大纲                 ...  │
│ ○ 撰写章节内容                      │
└─────────────────────────────────────┘
```

---

## 3. 方案B：新增 reflection 事件（可选）

> 仅在需要专属反思样式时使用

### 3.1 事件格式

```json
{
  "type": "reflection",
  "data": {
    "task_id": 1,
    "reflection": "分析发现3个伏笔，但血神宫线索不完整，需要补充分析。",
    "needs_replan": true
  }
}
```

### 3.2 后端发送

```python
# deep_agent/executor.py

async def _do_reflection(self, task, result, remaining_tasks, context):
    reflection_result = await think_tool(...)

    # 完整版方案：发送独立的 reflection 事件
    if self.on_reflection:
        await self.on_reflection({
            "task_id": task.get("task_id"),
            "reflection": reflection_result.reflection,
            "needs_replan": reflection_result.needs_replan,
        })

    return reflection_result
```

### 3.3 前端处理（需要改动）

```typescript
// agentApi.ts - 新增事件解析 (+5行)

case 'reflection':
  callbacks.onReflection?.(data.data);
  break;
```

```typescript
// useAgentChat.ts - 新增回调处理 (+15行)

onReflection: (data: {
  task_id: number;
  reflection: string;
  needs_replan: boolean;
}) => {
  sessionManager.updateSession(sessionId, {
    tasks: (sessionManager.getSession(sessionId)?.tasks || []).map((t) =>
      t.task_id === data.task_id
        ? { ...t, reflection: data.reflection }
        : t
    )
  });
}
```

---

## 4. plan 更新事件（is_update）

### 4.1 初始规划格式

```json
{
  "type": "plan",
  "data": {
    "tasks": [
      {"task_id": 1, "description": "分析前文伏笔", "status": "pending"},
      {"task_id": 2, "description": "生成章节大纲", "status": "pending"},
      {"task_id": 3, "description": "撰写章节内容", "status": "pending"}
    ]
  }
}
```

### 4.2 重规划格式（新增字段）

```json
{
  "type": "plan",
  "data": {
    "tasks": [
      {"task_id": 1, "description": "分析前文伏笔", "status": "completed"},
      {"task_id": 4, "description": "深入分析血神宫线索", "status": "pending"},
      {"task_id": 2, "description": "生成章节大纲", "status": "pending"},
      {"task_id": 3, "description": "撰写章节内容", "status": "pending"}
    ],
    "is_update": true,
    "new_task_ids": [4],
    "reason": "反思发现血神宫线索不完整"
  }
}
```

### 4.3 前端处理 is_update（需要改动）

**问题**：现有前端直接替换整个任务列表，会丢失已完成任务的状态。

**修复**：

```typescript
// useAgentChat.ts - 修改 onPlan 回调 (+15行)

onPlan: (plan: any) => {
  const isUpdate = plan.is_update === true;
  const newTaskIds = new Set(plan.new_task_ids || []);

  if (isUpdate) {
    // 重规划：保留已完成任务的状态
    const existingTasks = sessionManager.getSession(sessionId)?.tasks || [];
    const existingTaskMap = new Map(existingTasks.map(t => [t.task_id, t]));

    const mergedTasks: Task[] = plan.tasks.map((t: any) => {
      const existing = existingTaskMap.get(t.task_id);
      return {
        task_id: t.task_id,
        description: t.description,
        status: existing?.status || t.status || 'pending',
        elapsed_time: existing?.elapsed_time,
        isNewFromReplan: newTaskIds.has(t.task_id),  // 标记新增任务
      };
    });

    sessionManager.updateSession(sessionId, { tasks: mergedTasks });
  } else {
    // 初始规划：替换全部
    const initialTasks: Task[] = plan.tasks.map((t: any) => ({
      task_id: t.task_id,
      description: t.description,
      status: t.status || 'pending',
    }));
    sessionManager.updateSession(sessionId, { tasks: initialTasks });
  }
}
```

---

## 5. 完整事件序列

### 5.1 MVP 方案（复用 task_progress）

```
plan ──────────────────────────────►  (初始规划)
     task_start(1)
     task_done(1)
task_progress ─────────────────────►  (💭 反思: ...)
plan ──────────────────────────────►  (重规划, is_update=true)
     task_start(4)                     (新增任务)
     task_done(4)
     task_start(2)
     task_done(2)
task_progress ─────────────────────►  (💭 反思: ...)
     task_start(3)
     task_done(3)
content ──────────────────────────►  (最终结果)
done
```

### 5.2 完整方案（独立 reflection 事件）

```
plan ──────────────────────────────►  (初始规划)
     task_start(1)
     task_done(1)
reflection ────────────────────────►  (反思)
plan ──────────────────────────────►  (重规划, is_update=true)
     task_start(4)
     task_done(4)
     task_start(2)
     task_done(2)
reflection ────────────────────────►  (反思)
     task_start(3)
     task_done(3)
content ──────────────────────────►  (最终结果)
done
```

---

## 6. 总结

| 方面 | 方案A (task_progress) | 方案B (reflection) |
|------|----------------------|-------------------|
| 前端改动 | **0 行** | ~25 行 |
| 事件类型 | 复用现有 | 新增类型 |
| 显示位置 | progress_status | 专属反思字段 |
| 样式定制 | 有限 | 可完全自定义 |
| 实现难度 | **低** | 中 |
| 推荐程度 | **⭐⭐⭐⭐⭐** | ⭐⭐⭐ |

**MVP 阶段建议使用方案 A**，后续根据产品需求再决定是否升级到方案 B。

---

## 7. API 调用示例

### 7.1 启用反思的请求

```bash
# cURL 示例
curl -X POST "http://localhost:8000/api/v1/agent/chat/stream" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer <token>" \
  -d '{
    "message": "帮我写第三章，要承接前面的伏笔",
    "work_id": "uuid-work-id",
    "chapter_id": "uuid-chapter-id",
    "mode": "planning",
    "enable_reflection": true
  }'
```

### 7.2 前端 TypeScript 调用

```typescript
// 使用 agentApi.ts 调用
import { streamChat } from '@/services/agentApi';

const response = await streamChat({
  message: "帮我写第三章，要承接前面的伏笔",
  work_id: workId,
  chapter_id: chapterId,
  mode: 'planning',
  enable_reflection: true,  // 启用反思
}, {
  onPlan: (plan) => {
    console.log('收到计划:', plan);
    // plan.is_update === true 表示重规划
  },
  onTaskStart: (task) => {
    console.log('任务开始:', task);
  },
  onTaskProgress: (progress) => {
    // MVP方案：反思内容通过此回调接收
    // progress.status 包含 "💭 反思: ..." 格式的内容
    console.log('任务进度:', progress);
  },
  onTaskDone: (task) => {
    console.log('任务完成:', task);
  },
  onContent: (content) => {
    console.log('内容:', content);
  },
  onDone: (result) => {
    console.log('完成:', result);
  },
});
```

### 7.3 请求参数说明

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `message` | string | ✅ | 用户消息 |
| `work_id` | string | ❌ | 作品 ID（写作任务需要） |
| `chapter_id` | string | ❌ | 章节 ID |
| `mode` | string | ❌ | 模式：`planning`（默认）或 `react` |
| `enable_reflection` | boolean | ❌ | 是否启用反思，默认 `false` |
| `context` | object | ❌ | 额外上下文信息 |

### 7.4 响应事件示例

```json
// 1. 初始计划
data: {"type": "plan", "data": {"tasks": [...]}}

// 2. 任务执行
data: {"type": "task_start", "data": {"task_id": 1, "description": "分析伏笔"}}
data: {"type": "task_done", "data": {"task_id": 1, "elapsed_time": 2.1}}

// 3. 反思（MVP方案通过 task_progress）
data: {"type": "task_progress", "data": {"task_id": 1, "status": "💭 反思: 发现3个伏笔..."}}

// 4. 重规划（如需要）
data: {"type": "plan", "data": {"tasks": [...], "is_update": true, "new_task_ids": [4]}}

// 5. 最终内容
data: {"type": "content", "data": "第三章：..."}
data: {"type": "done", "data": {}}
```
