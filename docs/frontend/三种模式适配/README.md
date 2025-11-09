# Agent API 三种模式适配文档

## 📋 文档概述

本文档目录专注于前端如何适配后端 Agent API 的调用模式：
- `chat()` - 非流式对话
- `chat_stream()` - 统一流式对话（支持 planning/react 模式）
- 通过 `mode` 参数区分：Planning（先规划再执行）和 React（边思考边执行）

## 🎯 文档范围

本目录**仅关注**：
- 后端 Agent API 的调用方式
- Planning 模式 vs React 模式的差异
- SSE 事件处理和回调函数
- API 请求参数和响应格式

**不包含**：
- 编辑器 UI 交互（参见 `../ai-suggestion/`）
- Tiptap 扩展实现
- 编辑器内容的高亮和确认机制

---

## 📚 文档导航

### 核心文档

1. **[AGENT_API_EXAMPLES.md](./AGENT_API_EXAMPLES.md)** - 推荐阅读
   - Agent API 的正确使用方法
   - Planning 模式和 React 模式的完整示例
   - React Hook 集成示例
   - 回调函数对比表

2. **[API_QUICK_FIX.md](./API_QUICK_FIX.md)** - 问题修复
   - 当前前端实现的问题说明
   - 快速修复步骤
   - 使用指南速查

3. **[API_ADAPTATION_ANALYSIS.md](./API_ADAPTATION_ANALYSIS.md)** - 深度分析
   - 前后端 API 适配的完整分析
   - 问题根因分析
   - 修复方案详解
   - 测试验证用例

---

## 🔍 后端 API 架构

### 统一流式接口设计

后端提供了**一个统一的流式接口**：

```
POST /api/v1/agent/chat/stream
```

通过 `mode` 参数区分两种模式：
- `mode: 'planning'`（默认）- 先规划再执行
- `mode: 'react'` - 边思考边执行

### 路由列表

| 路由 | 方法 | 功能 | 代码位置 |
|------|------|------|---------|
| `/api/v1/agent/chat` | POST | 非流式对话 | backend/app/api/v1/agent.py:232 |
| `/api/v1/agent/chat/stream` | POST | 统一流式对话 | backend/app/api/v1/agent.py:865 |

⚠️ **重要**：后端**不存在** `/api/v1/agent/chat/react-stream` 路由

---

## ✅ 正确的使用方式

⚠️ **重要前提**：使用前需要先修改类型定义！

### Step 0: 修改类型定义（必须）

修改 `src/types/agent.ts`:

```typescript
export interface AgentChatRequest {
  message: string;
  mode?: 'planning' | 'react';  // ✅ 添加此行
  work_id?: string;
  chapter_id?: string;
  conversation_id?: string;
  context?: Record<string, any>;
}
```

### Planning 模式（默认）

```typescript
import { agentApi } from '@/services/agentApi';

await agentApi.chatStream(
  {
    message: '帮我写第三章',
    mode: 'planning',  // 可选，默认就是 planning
    work_id: 'work-123',
  },
  {
    onPlan: (plan) => console.log('规划:', plan),
    onTaskStart: (task) => console.log('任务开始:', task),
    onTaskDone: (task) => console.log('任务完成:', task),
    onContent: (chunk) => console.log('内容:', chunk),
    onDone: (result) => console.log('完成:', result),
  }
);
```

### React 模式

⚠️ **当前问题**：`chatStream()` 缺少 React 模式的事件处理（`progress`, `tool_call`），需要先扩展该函数。

```typescript
await agentApi.chatStream(
  {
    message: '分析第30章',
    mode: 'react',  // 指定 react 模式
    work_id: 'work-123',
  },
  {
    onProgress: (progress) => console.log('进度:', progress),
    onToolCall: (toolCall) => console.log('工具调用:', toolCall),
    onContent: (chunk) => console.log('内容:', chunk),
    onDone: (result) => console.log('完成:', result),
  }
);
```

---

## 🔄 回调函数差异

| 回调函数 | Planning 模式 | React 模式 | 说明 |
|---------|-------------|-----------|------|
| `onStart` | ✅ | ✅ | 对话开始 |
| `onPlan` | ✅ | ❌ | 规划生成（Planning 独有） |
| `onTaskStart` | ✅ | ❌ | 任务开始（Planning 独有） |
| `onTaskProgress` | ✅ | ❌ | 任务进度（Planning 独有） |
| `onTaskDone` | ✅ | ❌ | 任务完成（Planning 独有） |
| `onProgress` | ❌ | ✅ | 进度更新（React 独有） |
| `onToolCall` | ❌ | ✅ | 工具调用（React 独有） |
| `onContent` | ✅ | ✅ | 内容生成（共同） |
| `onDone` | ✅ | ✅ | 对话完成（共同） |
| `onError` | ✅ | ✅ | 错误处理（共同） |

---

## 🚨 已知问题

### ❌ 前端实现错误

**问题**：`src/services/agentApi.ts` 中的 `chatReactStream()` 函数调用了不存在的路由

```typescript
// ❌ 错误：这个路由不存在
const url = `${API_BASE_URL}/api/v1/agent/chat/react-stream`;
```

**状态**：已识别，待修复

**修复优先级**：🔴 P0 - 立即修复

**详细说明**：参见 [API_QUICK_FIX.md](./API_QUICK_FIX.md)

---

## 📖 使用场景建议

### 何时使用 Planning 模式？

- ✅ 复杂的多步骤任务（如：写作一整章）
- ✅ 需要详细任务进度显示
- ✅ 需要任务可追溯性
- ✅ 用户需要了解 AI 的执行计划

**示例**：
```typescript
// 写作场景
sendMessage('帮我写第三章，主角遇到了挑战', { mode: 'planning' });

// 润色场景
sendMessage('润色第五章，提升文学性', { mode: 'planning' });
```

### 何时使用 React 模式？

- ✅ 简单的查询或分析任务
- ✅ 需要实时显示推理过程
- ✅ 需要查看工具调用详情
- ✅ 快速响应的交互场景

**示例**：
```typescript
// 分析场景
sendMessage('分析第30章的人物关系', { mode: 'react' });

// 查询场景
sendMessage('查询主角在第10-15章的行动轨迹', { mode: 'react' });
```

---

## 🔧 快速开始

### 1. 阅读核心文档
从 [AGENT_API_EXAMPLES.md](./AGENT_API_EXAMPLES.md) 开始

### 2. 修复当前问题
参考 [API_QUICK_FIX.md](./API_QUICK_FIX.md) 修复 `chatReactStream()` 错误

### 3. 深入理解
阅读 [API_ADAPTATION_ANALYSIS.md](./API_ADAPTATION_ANALYSIS.md) 了解完整架构

---

## 🔗 相关文档

- **编辑器交互文档**: `../ai-suggestion/` - 编辑器内的 AI 建议 UI 实现
- **后端 API 文档**: `../../backend/` - 后端 Agent API 接口定义

---

## 📝 更新记录

- **2025-11-09**: 创建文档目录，整理 Agent API 适配文档
- **2025-11-09**: 移入 AGENT_API_EXAMPLES.md、API_QUICK_FIX.md、API_ADAPTATION_ANALYSIS.md

---

**文档维护者**：前端开发团队
**最后更新**：2025-11-09
