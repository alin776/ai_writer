# API 适配问题快速参考

**问题**：前端 React 模式流式对话无法工作

**原因**：`agentApi.chatReactStream()` 调用了不存在的后端路由 `/api/v1/agent/chat/react-stream`

---

## 🚨 核心问题

❌ **错误调用**：
```typescript
// src/services/agentApi.ts:110
const url = `${API_BASE_URL}/api/v1/agent/chat/react-stream`;  // 路由不存在！
```

✅ **后端实际路由**：
```python
# 后端只有一个统一的流式接口
POST /api/v1/agent/chat/stream

# 支持两种模式（通过 mode 参数区分）：
# - mode='planning' (默认)
# - mode='react'
```

---

## ✅ 完整修复步骤

### Step 0: 修改类型定义（必须）

修改 `src/types/agent.ts`:

```typescript
export interface AgentChatRequest {
  message: string;
  mode?: 'planning' | 'react';  // ✅ 新增此字段
  work_id?: string;
  chapter_id?: string;
  conversation_id?: string;
  context?: Record<string, any>;
}
```

### Step 1: 扩展 chatStream() 支持 React 模式

修改 `src/services/agentApi.ts`:

**1.1 添加回调参数类型**（第194行附近）：

```typescript
async chatStream(
  request: AgentChatRequest,
  callbacks: {
    onStart?: (conversationId: string) => void;
    // Planning 模式回调
    onPlan?: (plan: any) => void;
    onTaskStart?: (task: any) => void;
    onTaskProgress?: (progress: any) => void;
    onTaskDone?: (taskDone: any) => void;
    // ✅ 新增：React 模式回调
    onProgress?: (progress: any) => void;
    onToolCall?: (toolCall: any) => void;
    // 共同回调
    onContent?: (chunk: string) => void;
    onStep?: (step: any) => void;
    onDone?: (metadata: any, suggestedActions: string[]) => void;
    onError?: (error: string) => void;
  }
): Promise<void>
```

**1.2 添加事件处理**（第254-283行的switch语句中）：

```typescript
switch (data.type) {
  case 'start':
    callbacks.onStart?.(data.conversation_id);
    break;
  // Planning 模式事件
  case 'plan':
    callbacks.onPlan?.(data.data);
    break;
  case 'task_start':
    callbacks.onTaskStart?.(data.data);
    break;
  case 'task_progress':
    callbacks.onTaskProgress?.(data.data);
    break;
  case 'task_done':
    callbacks.onTaskDone?.(data.data);
    break;
  // ✅ 新增：React 模式事件
  case 'progress':
    callbacks.onProgress?.(data.data);
    break;
  case 'tool_call':
    callbacks.onToolCall?.(data.data);
    break;
  // 共同事件
  case 'content':
    callbacks.onContent?.(data.data);
    break;
  case 'step':
    callbacks.onStep?.(data.data);
    break;
  case 'done':
    callbacks.onDone?.(data.metadata, data.suggested_actions);
    break;
  case 'error':
    callbacks.onError?.(data.error);
    break;
}
```

### Step 2: 删除错误函数

删除 `src/services/agentApi.ts` 中的 `chatReactStream()` 函数（第97-186行）

### Step 3: 修改 Hook

修改 `src/hooks/useAgentChatStream.ts:136`：

```typescript
// ❌ 错误
await agentApi.chatReactStream(request, { ... });

// ✅ 正确
const request: AgentChatRequest = {
  message,
  mode: 'react',  // 添加 mode 参数
  conversation_id: conversationId || undefined,
  ...requestOptions,
};

await agentApi.chatStream(request, {
  onProgress: ...,
  onToolCall: ...,
  onContent: ...,
  onDone: ...,
  onError: ...,
});
```

---

## 📋 使用指南

### Planning 模式（默认）

```typescript
await agentApi.chatStream(
  { message: '帮我写第三章', mode: 'planning' },  // 或不传 mode
  {
    onPlan: (plan) => console.log('规划:', plan),
    onTaskStart: (task) => console.log('任务开始:', task),
    onTaskDone: (task) => console.log('任务完成:', task),
    onContent: (chunk) => console.log('内容:', chunk),
    onDone: (metadata) => console.log('完成:', metadata),
    onError: (error) => console.error('错误:', error),
  }
);
```

### React 模式

```typescript
await agentApi.chatStream(
  { message: '分析第30章', mode: 'react' },  // 传递 mode: 'react'
  {
    onProgress: (event) => console.log('进度:', event),
    onToolCall: (tool) => console.log('工具调用:', tool),
    onContent: (chunk) => console.log('内容:', chunk),
    onDone: (result) => console.log('完成:', result),
    onError: (error) => console.error('错误:', error),
  }
);
```

---

## 📊 回调差异对照表

| 回调函数 | Planning 模式 | React 模式 | 说明 |
|---------|-------------|-----------|------|
| `onStart` | ✅ | ✅ | 对话开始 |
| `onPlan` | ✅ | ❌ | 规划生成 |
| `onTaskStart` | ✅ | ❌ | 任务开始 |
| `onTaskProgress` | ✅ | ❌ | 任务进度 |
| `onTaskDone` | ✅ | ❌ | 任务完成 |
| `onProgress` | ❌ | ✅ | 进度更新 |
| `onToolCall` | ❌ | ✅ | 工具调用 |
| `onContent` | ✅ | ✅ | 内容生成 |
| `onDone` | ✅ | ✅ | 对话完成 |
| `onError` | ✅ | ✅ | 错误处理 |

---

## 🔗 完整分析

详见：[API_ADAPTATION_ANALYSIS.md](./API_ADAPTATION_ANALYSIS.md)

**修复优先级**：🔴 P0 - 立即修复

**预估工时**：1.5 小时

详细工时：
- Step 0 (类型定义)：5分钟
- Step 1 (扩展chatStream)：40分钟
- Step 2 (删除函数)：5分钟
- Step 3 (修改Hook)：10分钟
- 测试验证：20分钟
