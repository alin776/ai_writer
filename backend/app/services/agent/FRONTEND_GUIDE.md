# Agent智能助手 - 前端开发指南

> **更新时间**: 2025-10-29
> **后端集成**: ✅ 完成
> **预计开发时间**: 3-5天

---

## 📋 目录

1. [API接口文档](#api接口文档)
2. [前端架构设计](#前端架构设计)
3. [核心组件开发](#核心组件开发)
4. [API调用示例](#api调用示例)
5. [UI设计建议](#ui设计建议)

---

## 🚀 API接口文档

### 基础URL

```
http://localhost:8000/api/v1/agent
```

### 认证

所有请求需要在Header中携带JWT Token:
```
Authorization: Bearer <your_jwt_token>
```

---

### 1. Agent对话接口

**POST** `/chat`

与Agent进行智能对话，支持4个核心场景。

#### 请求参数

```typescript
interface AgentChatRequest {
  message: string;              // 用户消息（必填）
  work_id?: string;            // 作品ID（可选）
  chapter_id?: string;         // 章节ID（可选）
  conversation_id?: string;    // 会话ID（可选，用于继续对话）
  context?: {                  // 额外上下文（可选）
    chapter_context?: string;   // 章节内容
    text?: string;             // 待分析文本
    current_content?: string;  // 当前创作内容
  };
}
```

#### 响应数据

```typescript
interface AgentChatResponse {
  response: string;              // Agent回复
  conversation_id: string;       // 会话ID
  agent_steps: Array<{          // Agent执行步骤
    step: string;
    result: string;
    usage?: {                   // Token使用统计（最后一步才有）
      prompt_tokens: number;
      completion_tokens: number;
      total_tokens: number;
    };
  }>;
  suggested_actions: string[];   // 建议的后续操作
  metadata: {                   // 元数据
    intent: string;             // 检测到的意图
    memory_quality: string;     // 记忆质量
    timestamp: string;          // 时间戳
  };
}
```

#### 示例 - 场景A: 帮我写第三章

```bash
curl -X POST "http://localhost:8000/api/v1/agent/chat" \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "message": "帮我写第三章，主角需要突破境界",
    "work_id": "work-uuid",
    "chapter_id": "chapter-uuid",
    "context": {
      "chapter_context": "前文内容..."
    }
  }'
```

#### 示例 - 场景B: 我想写玄幻小说

```bash
curl -X POST "http://localhost:8000/api/v1/agent/chat" \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "message": "我想写一部玄幻小说，主角是一个废柴逆袭的故事"
  }'
```

#### 示例 - 场景C: 分析这段文字

```bash
curl -X POST "http://localhost:8000/api/v1/agent/chat" \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "message": "分析这段文字哪里不好",
    "context": {
      "text": "他很生气，非常生气..."
    }
  }'
```

#### 示例 - 场景D: 我卡文了

```bash
curl -X POST "http://localhost:8000/api/v1/agent/chat" \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "message": "我卡文了，不知道该怎么继续写下去",
    "context": {
      "current_content": "当前写到..."
    }
  }'
```

---

### 2. 创建执行计划

**POST** `/plans`

创建一个长期执行计划（如从零开始写小说）。

#### 请求参数

```typescript
interface PlanCreationRequest {
  goal: string;              // 目标描述（必填）
  genre?: string;           // 小说类型（可选）
  work_id?: string;         // 作品ID（可选）
  context?: object;         // 上下文（可选）
}
```

#### 响应数据

```typescript
interface PlanResponse {
  plan_id: string;          // 计划ID
  goal: string;             // 目标
  tasks: Array<{            // 任务列表
    task_id: string;
    description: string;
    status: string;         // pending/in_progress/completed
    depends_on: string[];   // 依赖任务ID
  }>;
  status: string;           // 计划状态
  progress: number;         // 进度 0-1
}
```

#### 示例

```bash
curl -X POST "http://localhost:8000/api/v1/agent/plans" \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "goal": "创作一部完整的玄幻小说",
    "genre": "玄幻"
  }'
```

---

### 3. 查询计划状态

**GET** `/plans/{plan_id}`

查询执行计划的当前状态。

#### 响应数据

同 `PlanResponse`

---

### 4. 获取待批准请求

**GET** `/approvals/pending`

获取所有等待用户批准的请求（HITL功能）。

#### 响应数据

```typescript
interface ApprovalResponse {
  request_id: string;
  title: string;
  description: string;
  proposed_action: object;      // 建议的操作
  alternatives: object[];       // 替代方案
  status: string;               // pending/approved/rejected
  created_at: string;
}
```

---

### 5. 批准/拒绝请求

**POST** `/approvals/{request_id}/approve`
**POST** `/approvals/{request_id}/reject`

批准或拒绝Agent的操作请求。

#### 请求参数

```typescript
interface ApprovalActionRequest {
  action: string;              // approve/reject/modify
  modifications?: object;      // 修改内容（action=modify时）
  feedback?: string;          // 反馈说明
}
```

---

### 6. 获取用户记忆上下文

**GET** `/memory/context`

获取当前用户的完整记忆信息。

#### 响应数据

```typescript
interface MemoryContext {
  success: boolean;
  data: {
    user_preferences: {         // 用户偏好
      preferred_genres: string[];
      writing_style: string;
      tone_preference: string;
    };
    user_profile: {             // 用户画像
      skill_level: string;
      total_sessions: number;
      favorite_operations: string[];
    };
  };
}
```

---

### 7. 更新用户偏好

**PUT** `/memory/context`

更新用户的偏好设置。

#### 请求参数

```typescript
interface UpdatePreferencesRequest {
  preferred_genres?: string[];
  writing_style?: string;
  tone_preference?: string;
  // ... 其他偏好字段
}
```

---

## 🎨 前端架构设计

### 推荐技术栈

- **React 18+** / Vue 3+ / Next.js
- **TypeScript** - 类型安全
- **TailwindCSS** - 样式框架
- **Zustand** / Pinia - 状态管理
- **React Query** / VueQuery - 数据请求
- **Markdown渲染**: react-markdown / marked
- **代码高亮**: prism.js / highlight.js

### 目录结构建议

```
src/
├── components/
│   └── agent/
│       ├── AgentChatPanel.tsx        # 主对话面板
│       ├── AgentMessage.tsx          # 消息组件
│       ├── AgentThinking.tsx         # 思考过程展示
│       ├── ApprovalDialog.tsx        # 批准对话框
│       ├── SuggestedActions.tsx      # 建议操作
│       └── ChatInput.tsx             # 输入框
├── hooks/
│   └── useAgentChat.ts               # Agent对话Hook
├── services/
│   └── agentApi.ts                   # API调用封装
├── types/
│   └── agent.ts                      # TypeScript类型定义
└── stores/
    └── agentStore.ts                 # Agent状态管理
```

---

## 🧩 核心组件开发

### 1. AgentChatPanel - 主对话面板

```typescript
// src/components/agent/AgentChatPanel.tsx

import React, { useState } from 'react';
import { useAgentChat } from '@/hooks/useAgentChat';
import AgentMessage from './AgentMessage';
import ChatInput from './ChatInput';
import SuggestedActions from './SuggestedActions';

interface AgentChatPanelProps {
  workId?: string;
  chapterId?: string;
}

export default function AgentChatPanel({ workId, chapterId }: AgentChatPanelProps) {
  const { messages, sendMessage, isLoading, suggestedActions } = useAgentChat();
  const [conversationId, setConversationId] = useState<string | null>(null);

  const handleSendMessage = async (message: string, context?: object) => {
    const response = await sendMessage({
      message,
      work_id: workId,
      chapter_id: chapterId,
      conversation_id: conversationId,
      context
    });

    if (response?.conversation_id) {
      setConversationId(response.conversation_id);
    }
  };

  return (
    <div className="agent-chat-panel flex flex-col h-full">
      {/* 头部 */}
      <div className="chat-header px-4 py-3 border-b">
        <h2 className="text-lg font-semibold">AI写作助手</h2>
        <p className="text-sm text-gray-500">智能规划 · 写作辅助 · 文本分析</p>
      </div>

      {/* 消息列表 */}
      <div className="messages flex-1 overflow-y-auto px-4 py-4 space-y-4">
        {messages.map((msg, index) => (
          <AgentMessage
            key={index}
            message={msg}
          />
        ))}

        {isLoading && (
          <div className="text-center text-gray-500">
            <span className="animate-pulse">AI正在思考...</span>
          </div>
        )}
      </div>

      {/* 建议操作 */}
      {suggestedActions.length > 0 && (
        <SuggestedActions
          actions={suggestedActions}
          onActionClick={handleSendMessage}
        />
      )}

      {/* 输入框 */}
      <ChatInput
        onSend={handleSendMessage}
        disabled={isLoading}
        placeholder="试试：帮我写第三章..."
      />
    </div>
  );
}
```

---

### 2. useAgentChat - 数据Hook

```typescript
// src/hooks/useAgentChat.ts

import { useState } from 'react';
import { agentApi } from '@/services/agentApi';
import type { AgentChatRequest, AgentChatResponse } from '@/types/agent';

interface Message {
  role: 'user' | 'agent';
  content: string;
  agentSteps?: any[];
  metadata?: any;
  timestamp: string;
}

export function useAgentChat() {
  const [messages, setMessages] = useState<Message[]>([]);
  const [isLoading, setIsLoading] = useState(false);
  const [suggestedActions, setSuggestedActions] = useState<string[]>([]);

  const sendMessage = async (request: AgentChatRequest): Promise<AgentChatResponse | null> => {
    try {
      setIsLoading(true);

      // 添加用户消息
      setMessages(prev => [...prev, {
        role: 'user',
        content: request.message,
        timestamp: new Date().toISOString()
      }]);

      // 调用API
      const response = await agentApi.chat(request);

      // 添加Agent回复
      setMessages(prev => [...prev, {
        role: 'agent',
        content: response.response,
        agentSteps: response.agent_steps,
        metadata: response.metadata,
        timestamp: new Date().toISOString()
      }]);

      // 更新建议操作
      setSuggestedActions(response.suggested_actions);

      return response;
    } catch (error) {
      console.error('Agent chat error:', error);

      // 添加错误消息
      setMessages(prev => [...prev, {
        role: 'agent',
        content: '抱歉，我遇到了一些问题。请稍后再试。',
        timestamp: new Date().toISOString()
      }]);

      return null;
    } finally {
      setIsLoading(false);
    }
  };

  const clearMessages = () => {
    setMessages([]);
    setSuggestedActions([]);
  };

  return {
    messages,
    isLoading,
    suggestedActions,
    sendMessage,
    clearMessages
  };
}
```

---

### 3. agentApi - API服务封装

```typescript
// src/services/agentApi.ts

import axios from 'axios';
import type {
  AgentChatRequest,
  AgentChatResponse,
  PlanCreationRequest,
  PlanResponse,
  ApprovalResponse
} from '@/types/agent';

const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';

// 创建axios实例
const client = axios.create({
  baseURL: `${API_BASE_URL}/api/v1/agent`,
  headers: {
    'Content-Type': 'application/json'
  }
});

// 请求拦截器 - 添加Token
client.interceptors.request.use((config) => {
  const token = localStorage.getItem('access_token');
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

export const agentApi = {
  // Agent对话
  chat: async (request: AgentChatRequest): Promise<AgentChatResponse> => {
    const response = await client.post('/chat', request);
    return response.data;
  },

  // 创建计划
  createPlan: async (request: PlanCreationRequest): Promise<PlanResponse> => {
    const response = await client.post('/plans', request);
    return response.data;
  },

  // 查询计划
  getPlan: async (planId: string): Promise<PlanResponse> => {
    const response = await client.get(`/plans/${planId}`);
    return response.data;
  },

  // 获取待批准请求
  getPendingApprovals: async (): Promise<ApprovalResponse[]> => {
    const response = await client.get('/approvals/pending');
    return response.data;
  },

  // 批准请求
  approveRequest: async (requestId: string, feedback?: string) => {
    const response = await client.post(`/approvals/${requestId}/approve`, {
      action: 'approve',
      feedback
    });
    return response.data;
  },

  // 拒绝请求
  rejectRequest: async (requestId: string, feedback?: string) => {
    const response = await client.post(`/approvals/${requestId}/reject`, {
      action: 'reject',
      feedback
    });
    return response.data;
  },

  // 获取记忆上下文
  getMemoryContext: async () => {
    const response = await client.get('/memory/context');
    return response.data;
  },

  // 更新用户偏好
  updatePreferences: async (preferences: object) => {
    const response = await client.put('/memory/context', preferences);
    return response.data;
  }
};
```

---

### 4. TypeScript类型定义

```typescript
// src/types/agent.ts

export interface AgentChatRequest {
  message: string;
  work_id?: string;
  chapter_id?: string;
  conversation_id?: string;
  context?: {
    chapter_context?: string;
    text?: string;
    current_content?: string;
    [key: string]: any;
  };
}

export interface AgentChatResponse {
  response: string;
  conversation_id: string;
  agent_steps: AgentStep[];
  suggested_actions: string[];
  metadata: {
    intent: string;
    memory_quality: string;
    timestamp: string;
  };
}

export interface AgentStep {
  step: string;
  result: string;
  usage?: {
    prompt_tokens: number;
    completion_tokens: number;
    total_tokens: number;
  };
}

export interface PlanCreationRequest {
  goal: string;
  genre?: string;
  work_id?: string;
  context?: object;
}

export interface PlanResponse {
  plan_id: string;
  goal: string;
  tasks: PlanTask[];
  status: string;
  progress: number;
}

export interface PlanTask {
  task_id: string;
  description: string;
  status: string;
  depends_on: string[];
}

export interface ApprovalResponse {
  request_id: string;
  title: string;
  description: string;
  proposed_action: any;
  alternatives: any[];
  status: string;
  created_at: string;
}
```

---

## 🎯 UI设计建议

### 对话面板布局

```
┌─────────────────────────────────────────┐
│  AI写作助手                              │
│  智能规划 · 写作辅助 · 文本分析          │
├─────────────────────────────────────────┤
│                                         │
│  👤 用户: 帮我写第三章                   │
│                                         │
│  🤖 Agent: 好的，让我来帮你...          │
│     [展开思考过程 ▼]                    │
│                                         │
│  📊 建议操作:                            │
│  [生成大纲] [续写内容] [检查一致性]     │
│                                         │
├─────────────────────────────────────────┤
│  💬 试试：帮我写第三章...  [发送]       │
└─────────────────────────────────────────┘
```

### 颜色方案建议

- **用户消息**: 蓝色背景 `bg-blue-100`
- **Agent消息**: 灰色背景 `bg-gray-100`
- **思考过程**: 淡黄色背景 `bg-yellow-50`
- **建议操作**: 边框按钮 `border-gray-300 hover:bg-gray-50`

### 交互细节

1. **流式响应**: Agent回复时逐字显示，增加真实感
2. **思考过程**: 默认折叠，点击展开显示详细步骤
3. **建议操作**: 点击直接发送对应消息
4. **历史记录**: 支持查看历史对话
5. **快捷指令**: 提供常用场景的快捷按钮

---

## 📝 开发检查清单

### Phase 1 - 基础功能 (Day 1-2)

- [ ] 搭建项目结构
- [ ] 创建API服务封装
- [ ] 实现基础对话组件
- [ ] 测试API连接

### Phase 2 - 核心功能 (Day 3-4)

- [ ] 实现4个核心场景UI
- [ ] 添加思考过程展示
- [ ] 实现建议操作
- [ ] 添加Markdown渲染

### Phase 3 - 高级功能 (Day 5)

- [ ] 实现批准管理界面
- [ ] 添加历史记录功能
- [ ] 优化交互动画
- [ ] 响应式适配

---

## 🔗 相关文档

- [Agent系统架构](./README.md)
- [API集成文档](./INTEGRATION.md)
- [快速开始指南](./QUICKSTART.md)

---

**最后更新**: 2025-10-29
**维护者**: NovelAIde 开发团队
