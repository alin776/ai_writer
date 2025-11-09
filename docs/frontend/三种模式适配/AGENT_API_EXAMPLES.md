# Agent API 前端使用示例

本文档提供 Agent API 在前端的正确使用方法和示例代码。

---

## ⚠️ 重要前提

在使用以下示例前，**必须先修改类型定义**：

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

---

## 📋 API 概览

### 后端提供的路由

```
POST /api/v1/agent/chat              # 非流式对话
POST /api/v1/agent/chat/stream       # 统一流式对话（支持 planning/react 模式）
```

⚠️ **重要**：后端只有一个流式接口，通过 `mode` 参数区分模式

---

## ✅ Planning 模式（默认）

### 特点
- 先规划任务，再逐步执行
- 适合复杂的多步骤任务
- 提供详细的任务进度反馈

### 使用示例

```typescript
import { agentApi } from '@/services/agentApi';

// Planning 模式示例
async function planningModeExample() {
  await agentApi.chatStream(
    {
      message: '帮我写第三章，主角遇到了挑战',
      mode: 'planning',  // 可选，默认就是 planning
      work_id: 'work-123',
      chapter_id: 'chapter-3',
      conversation_id: undefined,  // 新对话
    },
    {
      // 开始回调
      onStart: (conversationId) => {
        console.log('对话开始:', conversationId);
      },

      // 规划生成回调
      onPlan: (plan) => {
        console.log('规划生成:', plan);
        // plan 结构：
        // {
        //   tasks: [
        //     { task_id: '1', description: '分析上文情节', tool: 'analyze' },
        //     { task_id: '2', description: '生成新内容', tool: 'write' }
        //   ]
        // }
      },

      // 任务开始回调
      onTaskStart: (task) => {
        console.log('任务开始:', task);
        // task 结构：
        // {
        //   task_id: '1',
        //   description: '分析上文情节'
        // }
      },

      // 任务进度回调
      onTaskProgress: (progress) => {
        console.log('任务进度:', progress);
        // progress 结构：
        // {
        //   task_id: '1',
        //   status: 'running'
        // }
      },

      // 任务完成回调
      onTaskDone: (taskDone) => {
        console.log('任务完成:', taskDone);
        // taskDone 结构：
        // {
        //   task_id: '1',
        //   description: '分析上文情节',
        //   elapsed_time: 2.5  // 秒
        // }
      },

      // 内容生成回调（流式）
      onContent: (chunk) => {
        console.log('内容块:', chunk);
        // chunk 是字符串片段，需要累积
      },

      // 完成回调
      onDone: (metadata, suggestedActions) => {
        console.log('对话完成:', metadata, suggestedActions);
        // metadata: { intent: 'writing', ... }
        // suggestedActions: ['继续写作', '修改润色']
      },

      // 错误回调
      onError: (error) => {
        console.error('错误:', error);
      },
    }
  );
}
```

### React Hook 集成

```typescript
import { useAgentChat } from '@/hooks/useAgentChat';

function PlanningModeComponent() {
  const {
    messages,
    isLoading,
    error,
    tasks,
    currentTaskId,
    streamingContent,
    sendMessage,
  } = useAgentChat({
    mode: 'planning',
    onComplete: (result) => {
      console.log('对话完成:', result);
    },
  });

  const handleSend = () => {
    sendMessage('帮我写第三章');
  };

  return (
    <div>
      {/* 任务列表 */}
      <TaskListPanel tasks={tasks} currentTaskId={currentTaskId} />

      {/* 流式内容 */}
      <div>{streamingContent}</div>

      {/* 发送按钮 */}
      <button onClick={handleSend} disabled={isLoading}>
        发送
      </button>
    </div>
  );
}
```

---

## ✅ React 模式

⚠️ **当前限制**：`chatStream()` 需要先扩展支持 `progress` 和 `tool_call` 事件，参见 [API_QUICK_FIX.md](./API_QUICK_FIX.md)

### 特点
- 边思考边执行（ReAct）
- 实时显示推理步骤
- 提供工具调用详情

### 使用示例

```typescript
import { agentApi } from '@/services/agentApi';

// React 模式示例
async function reactModeExample() {
  await agentApi.chatStream(
    {
      message: '分析第30章的主要情节',
      mode: 'react',  // ✅ 关键：指定 react 模式
      work_id: 'work-123',
      conversation_id: undefined,
    },
    {
      // 开始回调
      onStart: (conversationId) => {
        console.log('对话开始:', conversationId);
      },

      // 进度更新回调（⚠️ 需要先在chatStream中添加）
      onProgress: (progress) => {
        console.log('进度更新:', progress);
        // progress 结构：
        // {
        //   step: 'thinking',  // 'intent_analysis' | 'thinking' | 'tool_execution'
        //   description: '正在分析意图...',
        //   node: 'intent_classifier',
        //   details: { intent: 'analysis' },
        //   timestamp: '2025-11-09T12:00:00'
        // }
      },

      // 工具调用回调
      onToolCall: (toolCall) => {
        console.log('工具调用:', toolCall);
        // toolCall 结构：
        // {
        //   tool: 'get_chapter_content',
        //   args: { chapter_id: 'chapter-30' },
        //   timestamp: '2025-11-09T12:00:00'
        // }
      },

      // 内容生成回调（流式）
      onContent: (chunk) => {
        console.log('内容块:', chunk);
      },

      // 完成回调
      onDone: (result) => {
        console.log('对话完成:', result);
      },

      // 错误回调
      onError: (error) => {
        console.error('错误:', error);
      },
    }
  );
}
```

### React Hook 集成

```typescript
import { useAgentChatStream } from '@/hooks/useAgentChatStream';

function ReactModeComponent() {
  const {
    loading,
    error,
    currentProgress,
    progressHistory,
    toolCalls,
    content,
    sendMessage,
  } = useAgentChatStream({
    onProgress: (progress) => {
      console.log('进度:', progress);
    },
    onToolCall: (toolCall) => {
      console.log('工具调用:', toolCall);
    },
  });

  const handleSend = () => {
    sendMessage('分析第30章', { mode: 'react' });
  };

  return (
    <div>
      {/* 进度指示器 */}
      <ProgressIndicator
        currentProgress={currentProgress}
        toolCalls={toolCalls}
      />

      {/* 生成的内容 */}
      <div>{content}</div>

      {/* 发送按钮 */}
      <button onClick={handleSend} disabled={loading}>
        发送
      </button>
    </div>
  );
}
```

---

## 🔄 模式切换

### 场景一：根据用户输入动态切换

```typescript
function SmartAgentComponent() {
  const [mode, setMode] = useState<'planning' | 'react'>('planning');

  const handleSend = async (message: string) => {
    // 根据消息内容智能选择模式
    const selectedMode = message.includes('分析') || message.includes('查询')
      ? 'react'      // 分析/查询用 React 模式
      : 'planning';  // 写作/创作用 Planning 模式

    setMode(selectedMode);

    await agentApi.chatStream(
      { message, mode: selectedMode },
      {
        onPlan: mode === 'planning' ? handlePlan : undefined,
        onProgress: mode === 'react' ? handleProgress : undefined,
        onToolCall: mode === 'react' ? handleToolCall : undefined,
        onContent: handleContent,
        onDone: handleDone,
      }
    );
  };

  return <div>...</div>;
}
```

### 场景二：用户手动选择模式

```typescript
function ManualModeSelector() {
  const [selectedMode, setSelectedMode] = useState<'planning' | 'react'>('planning');

  return (
    <div>
      {/* 模式选择器 */}
      <select
        value={selectedMode}
        onChange={(e) => setSelectedMode(e.target.value as any)}
      >
        <option value="planning">Planning 模式（先规划再执行）</option>
        <option value="react">React 模式（边思考边执行）</option>
      </select>

      {/* 根据模式渲染不同的UI */}
      {selectedMode === 'planning' ? (
        <PlanningModeUI />
      ) : (
        <ReactModeUI />
      )}
    </div>
  );
}
```

---

## 🎯 完整示例：统一的 Agent 容器

```typescript
// src/components/agent/AgentContainer.tsx

import { useState } from 'react';
import { agentApi } from '@/services/agentApi';
import type { AgentChatRequest } from '@/types/agent';

export type AgentMode = 'planning' | 'react';

interface AgentContainerProps {
  mode?: AgentMode;
  workId?: string;
  chapterId?: string;
  onComplete?: (result: any) => void;
}

export function AgentContainer({
  mode = 'planning',
  workId,
  chapterId,
  onComplete,
}: AgentContainerProps) {
  const [conversationId, setConversationId] = useState<string | null>(null);
  const [loading, setLoading] = useState(false);
  const [content, setContent] = useState('');

  // Planning 模式的状态
  const [tasks, setTasks] = useState<any[]>([]);
  const [currentTaskId, setCurrentTaskId] = useState<string | null>(null);

  // React 模式的状态
  const [progressHistory, setProgressHistory] = useState<any[]>([]);
  const [toolCalls, setToolCalls] = useState<any[]>([]);

  const handleSend = async (message: string) => {
    setLoading(true);
    setContent('');

    const request: AgentChatRequest = {
      message,
      mode,
      work_id: workId,
      chapter_id: chapterId,
      conversation_id: conversationId || undefined,
    };

    await agentApi.chatStream(request, {
      onStart: (convId) => {
        setConversationId(convId);
      },

      // Planning 模式回调
      onPlan: mode === 'planning' ? (plan) => {
        setTasks(plan.tasks || []);
      } : undefined,

      onTaskStart: mode === 'planning' ? (task) => {
        setCurrentTaskId(task.task_id);
      } : undefined,

      onTaskDone: mode === 'planning' ? (taskDone) => {
        // 更新任务状态
      } : undefined,

      // React 模式回调
      onProgress: mode === 'react' ? (progress) => {
        setProgressHistory((prev) => [...prev, progress]);
      } : undefined,

      onToolCall: mode === 'react' ? (toolCall) => {
        setToolCalls((prev) => [...prev, toolCall]);
      } : undefined,

      // 共同回调
      onContent: (chunk) => {
        setContent((prev) => prev + chunk);
      },

      onDone: (result) => {
        setLoading(false);
        onComplete?.(result);
      },

      onError: (error) => {
        console.error('Agent错误:', error);
        setLoading(false);
      },
    });
  };

  return (
    <div className="agent-container">
      {/* Planning 模式 UI */}
      {mode === 'planning' && (
        <div>
          <TaskListPanel tasks={tasks} currentTaskId={currentTaskId} />
        </div>
      )}

      {/* React 模式 UI */}
      {mode === 'react' && (
        <div>
          <ProgressIndicator
            progressHistory={progressHistory}
            toolCalls={toolCalls}
          />
        </div>
      )}

      {/* 共同 UI */}
      <div className="content">{content}</div>
      <MessageInput onSend={handleSend} disabled={loading} />
    </div>
  );
}
```

---

## 📊 回调对比表

| 回调函数 | Planning | React | 数据结构 |
|---------|---------|-------|---------|
| `onStart` | ✅ | ✅ | `(conversationId: string) => void` |
| `onPlan` | ✅ | ❌ | `(plan: { tasks: Task[] }) => void` |
| `onTaskStart` | ✅ | ❌ | `(task: { task_id, description }) => void` |
| `onTaskProgress` | ✅ | ❌ | `(progress: { task_id, status }) => void` |
| `onTaskDone` | ✅ | ❌ | `(done: { task_id, elapsed_time }) => void` |
| `onProgress` | ❌ | ✅ | `(event: ProgressEvent) => void` |
| `onToolCall` | ❌ | ✅ | `(call: ToolCallEvent) => void` |
| `onContent` | ✅ | ✅ | `(chunk: string) => void` |
| `onDone` | ✅ | ✅ | `(result: any) => void` |
| `onError` | ✅ | ✅ | `(error: string) => void` |

---

## 🚨 常见错误

### ❌ 错误：调用不存在的路由

```typescript
// ❌ 错误：这个路由不存在！
await agentApi.chatReactStream(request, callbacks);
```

### ✅ 正确：使用统一接口

```typescript
// ✅ 正确：使用 chatStream() + mode 参数
await agentApi.chatStream(
  { ...request, mode: 'react' },
  callbacks
);
```

---

## 📚 相关文档

- [API_QUICK_FIX.md](./API_QUICK_FIX.md) - 问题快速修复
- [API_ADAPTATION_ANALYSIS.md](./API_ADAPTATION_ANALYSIS.md) - 深度分析报告
- [api-reference.md](./api-reference.md) - API 完整参考

---

**更新时间**：2025-11-09
**状态**：✅ 已验证
