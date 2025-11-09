# API 适配问题快速参考（已验证）

## 📊 审查结果概览

**审查日期**: 2025-11-09
**审查范围**: 前端 3,100+ 行，后端 1,600+ 行
**发现问题**: 5个（3个P0，2个P1）

---

## 🚨 核心问题（已确认）

### ✅ 后端已正确实现

**后端统一流式接口**（backend/app/api/v1/agent.py:865-910）：
```python
@router.post("/chat/stream")
async def agent_chat_stream(
    request: AgentChatRequest,
    mode: Optional[str] = None  # ✅ 已支持 mode 参数
):
    actual_mode = mode or request.mode or ChatMode.PLANNING

    if actual_mode == ChatMode.REACT:
        result = await agent_graph.chat_stream(...)        # ReAct 模式
    else:
        result = await agent_graph.chat_with_planning(...) # Planning 模式
```

✅ 路由: `POST /api/v1/agent/chat/stream`
✅ 支持模式: `planning` (默认) / `react`
✅ 自动分发到正确的处理函数

---

### ❌ 前端问题列表

#### 问题1: 类型定义缺失 mode 参数
**文件**: `src/types/agent.ts:7-18`
**当前代码**:
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

#### 问题2: ModeSelector 命名不匹配
**文件**: `src/components/agent/ModeSelector.tsx:14-49`
**当前代码**:
```typescript
type AgentMode = 'ask' | 'plan' | 'agent'  // ❌ 与后端不匹配
```

#### 问题3: AgentChatPanel 未集成
**文件**: `src/components/agent/AgentChatPanel.tsx:27-79`
**当前代码**:
```typescript
// ❌ 没有导入和使用 ModeSelector
const [useStreaming] = useState(true);  // 只是开关
```

#### 问题4: useAgentChat 硬编码
**文件**: `src/hooks/useAgentChat.ts:148-270`
**当前代码**:
```typescript
// ❌ 总是调用 Planning 模式
await agentApi.chatStream(request, {
  onPlan: ...,
  onTaskStart: ...,
  // 没有 React 模式回调
})
```

#### 问题5: chatStream 不支持 React
**文件**: `src/services/agentApi.ts:194-294`
**当前代码**:
```typescript
async chatStream(
  request: AgentChatRequest,  // ❌ 无 mode 参数
  callbacks: {
    // ❌ 只有 Planning 回调
    onPlan?: ...,
    onTaskStart?: ...,
  }
)
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

### Step 2: 修改 ModeSelector 组件

修改 `src/components/agent/ModeSelector.tsx:14-49`：

```typescript
// ❌ 错误
type AgentMode = 'ask' | 'plan' | 'agent'

// ✅ 正确（与后端对齐）
type AgentMode = 'planning' | 'react'

const modes: Array<{
  id: AgentMode;
  label: string;
  icon: React.ReactNode;
  description: string;
}> = [
  {
    id: 'planning',
    label: 'Planning',
    icon: <ListChecks className="w-4 h-4" />,
    description: '先规划再执行，适合复杂任务'
  },
  {
    id: 'react',
    label: 'ReAct',
    icon: <Zap className="w-4 h-4" />,
    description: '边思考边执行，适合快速交互'
  }
];
```

### Step 3: 集成 ModeSelector 到 AgentChatPanel

修改 `src/components/agent/AgentChatPanel.tsx`：

```typescript
import { ModeSelector } from './ModeSelector';

export default function AgentChatPanel({...}) {
  // ✅ 添加 mode 状态
  const [mode, setMode] = useState<'planning' | 'react'>('planning');

  // ✅ 在 UI 中添加 ModeSelector
  return (
    <div>
      <ModeSelector
        selectedMode={mode}
        onModeChange={setMode}
      />
      {/* 其他组件 */}
    </div>
  );
}
```

### Step 4: 修改 useAgentChat Hook

修改 `src/hooks/useAgentChat.ts:148-270`：

```typescript
const sendMessageStream = useCallback(
  async (request: AgentChatRequest) => {
    // ✅ 根据 mode 调用不同的回调
    if (request.mode === 'react') {
      await agentApi.chatStream(request, {
        onProgress: ...,
        onToolCall: ...,
        onContent: ...,
        onDone: ...,
        onError: ...,
      });
    } else {
      await agentApi.chatStream(request, {
        onPlan: ...,
        onTaskStart: ...,
        onTaskDone: ...,
        onContent: ...,
        onDone: ...,
        onError: ...,
      });
    }
  }
);
```

### Step 5: 删除冗余代码

**前端**: 如果存在 `chatReactStream()` 函数，删除它
**后端**: 删除 `backend/app/api/v1/agent_react_stream.py`（246 行，已被统一接口取代）

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

**修复优先级**：

| 步骤 | 优先级 | 预估工时 |
|------|--------|----------|
| Step 0 (类型定义) | 🔴 P0 | 5分钟 |
| Step 1 (扩展chatStream) | 🟡 P1 | 45分钟 |
| Step 2 (修改ModeSelector) | 🔴 P0 | 30分钟 |
| Step 3 (集成到AgentChatPanel) | 🔴 P0 | 45分钟 |
| Step 4 (修改useAgentChat) | 🟡 P1 | 30分钟 |
| Step 5 (删除冗余代码) | 🟡 P1 | 2分钟 |
| 测试验证 | - | 30分钟 |

**P0 总计**: 约1.5小时（必须修复，否则功能不可用）
**P1 总计**: 约1.5小时（建议修复，提升功能完整性）
**总计**: 约3小时

---

## 🎯 验收标准

修复完成后，应满足以下标准：

1. ✅ 用户可以在 UI 中选择 Planning 或 ReAct 模式
2. ✅ 类型系统正确（无 TypeScript 错误）
3. ✅ Planning 模式正常工作（显示任务列表）
4. ✅ ReAct 模式正常工作（显示思考过程）
5. ✅ 无冗余代码和文件
6. ✅ 前后端命名完全一致
