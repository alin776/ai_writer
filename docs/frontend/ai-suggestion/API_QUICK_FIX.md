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

## ✅ 快速修复

### 1. 删除错误函数

删除 `src/services/agentApi.ts` 中的 `chatReactStream()` 函数（第97-186行）

### 2. 修改 Hook

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
  ...
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

**预估工时**：2-3 小时
