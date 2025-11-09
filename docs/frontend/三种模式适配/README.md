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

### ⚠️ 重要：修复前必读

**[SAFE_FIX_GUIDE.md](./SAFE_FIX_GUIDE.md)** - 🛡️ 安全修复快速指南
- **核心原则**：绝不破坏Planning模式
- 5步快速修复流程
- 每步验收检查清单
- 紧急回滚方案
- 零风险实施策略

**[FRONTEND_MODE_ADAPTATION_ISSUES.md](./FRONTEND_MODE_ADAPTATION_ISSUES.md)** - 深度问题分析
- 14个问题的详细分析
- 安全修复方案（完整版）
- 工时估算和实施计划
- 前后端对比分析

---

### 🎨 模式命名与UI设计（新增）

**[AGENT_MODE_NAMING_RESEARCH.md](./AGENT_MODE_NAMING_RESEARCH.md)** - 模式命名调研报告
- **核心结论**：采用VS Code的Ask/Plan/Agent命名
- 业界标准分析（微软、GitHub验证）
- 用户友好命名 vs 技术命名对比
- 完整的模式映射方案
- Web搜索调研数据

**[VSCODE_UI_DESIGN_ANALYSIS.md](./VSCODE_UI_DESIGN_ANALYSIS.md)** - VS Code UI设计深度分析
- 基于真实截图的设计分析
- 极简主义设计原理（为什么只显示图标）
- 完整的技术实现要点
- 尺寸、间距、颜色规范
- 用户行为分析

**[MODE_SELECTOR_INTEGRATION_SIMPLE.md](./MODE_SELECTOR_INTEGRATION_SIMPLE.md)** - 集成实施指南
- ModeSelector组件使用方法
- AgentChatPanel集成步骤（3步完成）
- 完整代码示例
- 视觉效果展示

---

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
| `onContent` | ✅ | ✅ | 内容生成（共同）⚠️ 格式不同 |
| `onDone` | ✅ | ✅ | 对话完成（共同） |
| `onError` | ✅ | ✅ | 错误处理（共同） |

### ⚠️ 重要：content 事件数据格式差异

两种模式的 `content` 事件数据格式不同：

**Planning模式**:
```typescript
// 后端发送
{ type: 'content', data: "生成的文本内容", mode: 'planning' }

// 前端读取
onContent: (chunk) => {
  // chunk 直接是字符串
  console.log(chunk);
}
```

**React模式**:
```typescript
// 后端发送
{ type: 'content', data: { content: "生成的文本内容" }, mode: 'react' }

// 前端读取
onContent: (chunk) => {
  // 如果使用统一的chatStream()，需要根据mode处理
  if (typeof chunk === 'string') {
    console.log(chunk);  // Planning模式
  } else {
    console.log(chunk.content);  // React模式
  }
}
```

**原因**: React模式的content回调包装为对象，以便未来扩展更多字段（如token使用量、元数据等）。

**代码位置**:
- React模式: `backend/app/api/v1/agent.py:1017-1018`
- Planning模式: `backend/app/api/v1/agent.py:999-1001`

---

## 🚨 已知问题（基于代码审查）

### ❌ 问题1: 前端类型定义缺失mode参数 ✅ 已确认

**文件**: `src/types/agent.ts:7-18`

**问题**: `AgentChatRequest` 接口缺少 `mode` 字段

**实际代码**:
```typescript
export interface AgentChatRequest {
  message: string;
  work_id?: string;
  chapter_id?: string;
  conversation_id?: string;
  context?: Record<string, any>;
  // ❌ 缺少: mode?: 'planning' | 'react';
}
```

**后端已支持**:
```python
# backend/app/schemas/agent.py
class AgentChatRequest(BaseModel):
    message: str
    mode: Optional[str] = None  # ✅ 后端已有！
```

**影响**: 前端无法传递模式参数给后端

**修复优先级**: 🔴 P0 - 立即修复

---

### ❌ 问题2: ModeSelector 命名不匹配 ✅ 已确认

**文件**: `src/components/agent/ModeSelector.tsx:14-49`

**问题**: 前端使用 `ask/plan/agent`，但后端使用 `planning/react`

**实际代码**:
```typescript
// 前端
type AgentMode = 'ask' | 'plan' | 'agent'

// 后端
class ChatMode(str, Enum):
    PLANNING = "planning"
    REACT = "react"
```

**影响**: 命名不统一，开发者困惑，且 `ask` 模式后端不存在

**修复优先级**: 🔴 P0 - 立即修复

**修复方案**: 统一改为 `planning` 和 `react`

---

### ❌ 问题3: AgentChatPanel 未集成 ModeSelector ✅ 已确认

**文件**: `src/components/agent/AgentChatPanel.tsx:27-79`

**问题**: `ModeSelector` 组件已存在但从未被使用

**实际代码**:
```typescript
export default function AgentChatPanel({...}) {
  const [useStreaming] = useState(true);  // 只是开关，不是模式选择
  // ❌ 没有导入 ModeSelector
  // ❌ 没有 mode 状态管理
}
```

**影响**: 用户无法在 UI 中选择执行模式

**修复优先级**: 🔴 P0 - 立即修复

---

### ❌ 问题4: useAgentChat Hook 硬编码模式 ✅ 已确认

**文件**: `src/hooks/useAgentChat.ts:148-270`

**问题**: `sendMessageStream()` 总是调用 Planning 模式，无法切换

**实际代码**:
```typescript
const sendMessageStream = useCallback(
  async (request: AgentChatRequest) => {
    // ❌ 无法指定 mode，总是 Planning
    await agentApi.chatStream(request, {
      onPlan: ...,
      onTaskStart: ...,
      // 没有 React 模式的回调
    })
  }
)
```

**影响**: Hook 层面无法支持 React 模式

**修复优先级**: 🟡 P1 - 本周修复

---

### ❌ 问题5: chatStream() 不支持 React 模式事件 ✅ 已确认

**文件**: `src/services/agentApi.ts:194-294`

**问题**: `chatStream()` 函数缺少 React 模式的事件处理（`progress`, `tool_call`）

**实际代码**:
```typescript
async chatStream(
  request: AgentChatRequest,  // 没有 mode 参数
  callbacks: {
    // 只有 Planning 模式的回调
    onPlan?: (plan: any) => void;
    onTaskStart?: (task: any) => void;
    // ❌ 缺少: onProgress, onToolCall
  }
)
```

**影响**: 使用统一接口时无法接收 React 模式的特定事件

**修复优先级**: 🟡 P1 - 本周修复

**修复步骤**:

1. **扩展回调函数类型**（第196-206行）:
```typescript
async chatStream(
  request: AgentChatRequest,  // 确保包含mode参数
  callbacks: {
    // Planning模式回调
    onPlan?: (plan: any) => void;
    onTaskStart?: (task: any) => void;
    onTaskProgress?: (progress: any) => void;
    onTaskDone?: (taskDone: any) => void;
    // React模式回调
    onProgress?: (progress: any) => void;
    onToolCall?: (toolCall: any) => void;
    // 共同回调
    onStart?: (conversationId: string) => void;
    onContent?: (chunk: string | any) => void;  // 注意：支持两种格式
    onDone?: (result: any) => void;
    onError?: (error: string) => void;
  }
): Promise<void>
```

2. **在switch中添加React事件处理**（第254行后）:
```typescript
switch (data.type) {
  case 'start':
    callbacks.onStart?.(data.conversation_id);
    break;
  // Planning模式事件
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
  // React模式事件（新增）
  case 'progress':
    callbacks.onProgress?.(data.data);
    break;
  case 'tool_call':
    callbacks.onToolCall?.(data.data);
    break;
  // 共同事件
  case 'content':
    // 处理两种格式的content
    const content = typeof data.data === 'string'
      ? data.data
      : data.data?.content || data.data;
    callbacks.onContent?.(content);
    break;
  case 'done':
    callbacks.onDone?.(data.data);
    break;
  case 'error':
    callbacks.onError?.(data.error || data.message);
    break;
}
```

**预计修复时间**: 约15分钟

---

### 📋 修复总结（基于代码审查）

| 问题 | 优先级 | 文件 | 行号 | 工时 | 状态 |
|------|--------|------|------|------|------|
| 类型定义缺失mode | 🔴 P0 | src/types/agent.ts | 7-18 | 5分钟 | ⏳ 待修复 |
| ModeSelector命名混乱 | 🔴 P0 | src/components/agent/ModeSelector.tsx | 14-49 | 30分钟 | ⏳ 待修复 |
| AgentChatPanel未集成 | 🔴 P0 | src/components/agent/AgentChatPanel.tsx | 27-79 | 45分钟 | ⏳ 待修复 |
| useAgentChat硬编码 | 🟡 P1 | src/hooks/useAgentChat.ts | 148-270 | 30分钟 | ⏳ 待修复 |
| chatStream不支持React | 🟡 P1 | src/services/agentApi.ts | 194-294 | 45分钟 | ⏳ 待修复 |
| 删除冗余后端文件 | 🟡 P1 | backend/app/api/v1/agent_react_stream.py | 全文件 | 2分钟 | ⏳ 待修复 |

**P0 总计**: 约1.5小时（必须修复）
**P1 总计**: 约1.5小时（建议修复）
**总计**: 约3小时

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
- **2025-11-09**: 添加content事件格式差异说明，详细化修复步骤和优先级

---

**文档维护者**：前端开发团队
**最后更新**：2025-11-09
