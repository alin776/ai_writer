# 06 - 前端实现

> 提供两种实现方案：MVP（零改动）和完整版（反思气泡）

## 0. 方案选择

| 方案 | 改动量 | 效果 | 推荐场景 |
|------|--------|------|----------|
| **MVP** | **0 行** | progress_status 显示反思 | 快速验证、初期迭代 |
| 完整版 | ~100 行 | 专属反思气泡 + 新增标记 | 产品化、用户体验优化 |

---

## 1. MVP 方案（零改动）

### 1.1 原理

- 后端通过 `task_progress` 事件发送反思内容
- 前端已有 `onTaskProgress` 回调处理
- Task 接口已有 `progress_status` 字段
- TaskListPanel 已能显示进度状态

### 1.2 效果

```
┌───────────────────────────────────────────────────────────────┐
│ 执行计划                                                  2/5 │
├───────────────────────────────────────────────────────────────┤
│                                                               │
│  ● 分析前文伏笔                                         1.2s  │
│    💭 反思: 发现3个伏笔，但血神宫线索不完整...                │ ← progress_status
│                                                               │
│  ◐ 生成章节大纲                                         ...  │
│  ○ 撰写章节内容                                              │
│  ○ 校验伏笔回收                                              │
│                                                               │
└───────────────────────────────────────────────────────────────┘
```

### 1.3 已有代码（无需修改）

```typescript
// useAgentChat.ts:327-338 - 已有代码

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
// TaskListPanel.tsx - 已有代码

{task.progress_status && task.status === 'running' && (
  <div className={styles.progressStatus}>
    {task.progress_status}
  </div>
)}
```

---

## 2. 完整版方案（~100 行改动）

### 2.1 UI 效果图

```
┌───────────────────────────────────────────────────────────────┐
│ 执行计划                                                  2/5 │
├───────────────────────────────────────────────────────────────┤
│                                                               │
│  ● 分析前文伏笔                                         1.2s  │
│    ┌─────────────────────────────────────────────────────┐   │
│    │ ○ 发现3个伏笔，但血神宫线索不完整，需要补充分析     │   │  ← 反思气泡
│    └─────────────────────────────────────────────────────┘   │
│                                                               │
│  ◐ 深入分析血神宫线索                               新增 ...  │  ← 新增标记
│                                                               │
│  ○ 生成章节大纲                                              │
│  ○ 撰写章节内容                                              │
│  ○ 校验伏笔回收                                              │
│                                                               │
├───────────────────────────────────────────────────────────────┤
│ ████████████░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░  40% │
└───────────────────────────────────────────────────────────────┘
```

### 2.2 改动清单

| 文件 | 改动类型 | 行数 |
|------|----------|------|
| `TaskListPanel.tsx` | 修改 | +35 行 |
| `TaskListPanel.module.css` | 修改 | +40 行 |
| `useAgentChat.ts` | 修改 | +15 行 |
| `agentApi.ts` | 修改 | +10 行 |
| **总计** | | **~100 行** |

### 2.2.1 类型定义文件修改

完整版需要扩展 `src/types/agent.ts` 中的类型定义：

```typescript
// src/types/agent.ts - 需要添加的类型

/** 扩展 Task 接口 */
export interface Task {
  task_id: number;
  description: string;
  tool?: string;
  estimated_time?: string;
  status: 'pending' | 'running' | 'completed' | 'failed';
  elapsed_time?: number;
  progress_status?: string;

  // === DeepAgent 完整版新增 ===
  reflection?: string;           // 反思内容
  isNewFromReplan?: boolean;     // 是否是重规划新增的任务
}

/** 反思事件数据（如使用独立 reflection 事件） */
export interface ReflectionEventData {
  task_id: number;
  reflection: string;
  needs_replan: boolean;
}

/** 扩展 AgentStreamCallbacks */
export interface AgentStreamCallbacks {
  // ... 现有回调 ...
  onReflection?: (data: ReflectionEventData) => void;  // 新增
}
```

**文件改动清单**：

| 文件 | 改动类型 | 说明 |
|------|----------|------|
| `src/types/agent.ts` | 修改 | 扩展 Task 接口，新增 ReflectionEventData |
| `src/hooks/useAgentChat.ts` | 修改 | 导入新类型，实现 onReflection |
| `src/services/agentApi.ts` | 修改 | 解析 reflection 事件 |

### 2.3 数据结构扩展

```typescript
// src/hooks/useAgentChat.ts

interface Task {
  task_id: number;
  description: string;
  tool?: string;
  estimated_time?: string;
  status: 'pending' | 'running' | 'completed' | 'failed';
  elapsed_time?: number;
  progress_status?: string;       // 现有：Multi-Agent 进度

  // === 完整版新增字段 ===
  reflection?: string;            // 反思内容（独立字段）
  isNewFromReplan?: boolean;      // 是否是重规划新增的任务
}
```

### 2.4 useAgentChat.ts 改动

#### 2.4.1 is_update 处理（重要）

**问题**：现有 `onPlan` 回调直接替换任务列表，重规划时会丢失已完成任务的状态。

**修复**：

```typescript
// useAgentChat.ts - 修改 onPlan 回调

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
        tool: t.tool,
        estimated_time: t.estimated_time,
        status: existing?.status || t.status || 'pending',
        elapsed_time: existing?.elapsed_time,
        reflection: existing?.reflection,  // 保留反思内容
        isNewFromReplan: newTaskIds.has(t.task_id),
      };
    });

    sessionManager.updateSession(sessionId, { tasks: mergedTasks });
  } else {
    // 初始规划：替换全部
    const initialTasks: Task[] = plan.tasks.map((t: any) => ({
      task_id: t.task_id,
      description: t.description,
      tool: t.tool,
      estimated_time: t.estimated_time,
      status: t.status || 'pending',
    }));
    sessionManager.updateSession(sessionId, { tasks: initialTasks });
  }
}
```

#### 2.4.2 onReflection 回调（可选）

如果使用独立的 `reflection` 事件：

```typescript
// useAgentChat.ts - 新增回调

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

### 2.5 agentApi.ts 改动

```typescript
// agentApi.ts - 新增事件解析

case 'reflection':
  callbacks.onReflection?.(data.data);
  break;
```

### 2.6 TaskListPanel.tsx 改动

```typescript
// TaskListPanel.tsx - 新增反思气泡和新增标记

{/* 任务项 */}
<div
  key={task.task_id}
  className={`
    ${styles.taskItem}
    ${isActive ? styles.active : ''}
    ${task.status === 'completed' ? styles.completed : ''}
    ${task.isNewFromReplan ? styles.newTask : ''}
  `}
>
  {/* 状态图标 */}
  <div className={styles.taskIcon}>
    {getStatusIcon(task.status, isActive)}
  </div>

  <div className={styles.taskContent}>
    <div className={styles.taskDescription}>
      {task.description}
    </div>

    <div className={styles.taskMeta}>
      {/* 新增任务标记 */}
      {task.isNewFromReplan && (
        <span className={styles.newBadge}>新增</span>
      )}

      {task.tool && (
        <span className={styles.toolName}>
          {task.tool.replace('_tool', '')}
        </span>
      )}

      {task.elapsed_time !== undefined && (
        <span className={styles.elapsedTime}>
          {task.elapsed_time.toFixed(1)}s
        </span>
      )}
    </div>

    {/* 反思气泡 */}
    {task.reflection && (
      <div className={styles.reflectionBubble}>
        <span className={styles.thinkDot}></span>
        <span className={styles.reflectionText}>
          {task.reflection}
        </span>
      </div>
    )}
  </div>
</div>
```

### 2.7 CSS 样式

```css
/* TaskListPanel.module.css - 新增样式 */

/* 新增任务高亮 */
.taskItem.newTask {
  border-color: #c4b5fd;
  background: #f5f3ff;
  animation: fadeIn 0.3s ease-out;
}

@keyframes fadeIn {
  from { opacity: 0; transform: translateY(-4px); }
  to { opacity: 1; transform: translateY(0); }
}

/* 新增标记 */
.newBadge {
  padding: 2px 6px;
  background: #ede9fe;
  color: #7c3aed;
  border-radius: 999px;
  font-size: 10px;
  font-weight: 600;
}

/* 反思气泡 */
.reflectionBubble {
  display: flex;
  align-items: flex-start;
  gap: 6px;
  margin-top: 8px;
  padding: 8px;
  background: #fefce8;
  border-radius: 8px;
  font-size: 12px;
  color: #374151;
}

.thinkDot {
  width: 6px;
  height: 6px;
  background: #eab308;
  border-radius: 50%;
  animation: pulse 1.4s ease-in-out infinite;
}

@keyframes pulse {
  0%, 100% { opacity: 1; }
  50% { opacity: 0.45; }
}

.reflectionText {
  flex: 1;
  line-height: 1.4;
}
```

---

## 3. 实现路径建议

```
Phase 1（MVP）:
  └─ 使用方案A，前端零改动
     └─ 反思内容通过 progress_status 显示

Phase 2（增强版）:
  └─ 实现 is_update 处理
     └─ 保留已完成任务状态
     └─ 新增任务紫色高亮

Phase 3（完整版）:
  └─ 添加反思气泡组件
     └─ 独立 reflection 字段
     └─ 专属样式
```

---

## 4. 测试清单

### MVP

- [ ] task_progress 事件正确显示在 progress_status
- [ ] 反思内容前缀有 💭 图标
- [ ] 任务完成后 progress_status 清空

### 完整版

- [ ] 反思气泡正确显示在对应任务下方
- [ ] 新增任务有紫色高亮和 "新增" 标记
- [ ] 重规划后已完成任务状态保留
- [ ] 动画流畅，无闪烁
