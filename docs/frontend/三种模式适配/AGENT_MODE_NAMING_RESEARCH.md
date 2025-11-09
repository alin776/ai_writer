# Agent模式命名方案调研报告

**调研日期**: 2025-11-09
**调研目的**: 确定前端Agent模式的最佳命名和UI设计方案
**结论**: ✅ 采用VS Code Copilot的 Ask/Plan/Agent 命名方案

---

## 📋 问题背景

### 当前技术命名（后端）

后端提供了三种API调用模式：

| 后端模式 | API方法 | 特性 | 技术描述 |
|---------|---------|------|---------|
| `chat` | `/api/v1/agent/chat` | 非流式 | 简单对话，快速响应 |
| `planning` | `/api/v1/agent/chat/stream?mode=planning` | 流式 | 先规划任务，再执行 |
| `react` | `/api/v1/agent/chat/stream?mode=react` | 流式 | 边思考边执行，工具调用 |

**问题**：这些是**技术术语**，对普通用户不友好。

### 用户需求

用户需要：
- ❌ 不用理解"planning"、"react"是什么
- ✅ 看名字就知道这个模式做什么
- ✅ 符合使用场景的心智模型

---

## 🔍 业界调研

### 调研方法

通过GitHub和Web搜索，调研了以下关键词：
- "AI agent chat mode selector UI design"
- "chatbot mode switcher interface plan ask agent"
- "LangChain agent mode selector UI"

### 调研发现

#### 1. **VS Code Copilot** - 微软官方实现 ⭐⭐⭐⭐⭐

**来源**: [VS Code Copilot Chat文档](https://code.visualstudio.com/docs/copilot/chat/copilot-chat)

**模式设计**：

| 模式名称 | 图标 | 用途描述 | 对应我们的技术模式 |
|---------|------|---------|-------------------|
| **Ask** | 💬 | 快速问答、简单咨询 | `chat` (非流式) |
| **Plan** | 📋 | 创建结构化实现计划，分步骤执行 | `planning` (流式) |
| **Agent** | 🤖 | 复杂任务，自主操作，运行工具 | `react` (流式) |
| Edit | ✏️ | 直接编辑代码 | (我们暂不需要) |

**UI实现**：
```
┌─────────────────────────────────────┐
│        编辑器区域                    │
├─────────────────────────────────────┤
│ [∞ ▼] [       输入框      ] [工具]  │
│   ↑                                 │
│   └─ 左下角模式选择器                │
└─────────────────────────────────────┘

点击后向上弹出菜单：
  ┌──────────────┐
  │ ∞ Agent  ✓  │
  │ 📋 Plan   ✏️  │
  │ 💬 Ask       │
  └──────────────┘
```

**设计特点**：
- ✅ **简洁图标** - 按钮只显示 `∞` 符号
- ✅ **向上弹出** - 因为在底部
- ✅ **深色主题** - 现代化视觉
- ✅ **清晰标记** - ✓ 表示当前模式

**引用原文**（来自搜索结果）：
> "VS Code provides four built-in chat modes: Agent, Plan, Ask, and Edit. Users can select the desired mode from the chat mode dropdown list and switch between chat modes at any time during a chat session."

> "Agent Mode: Optimized for complex coding tasks based on high-level requirements that might require running terminal commands and tools, with the AI operating autonomously."

> "Plan Mode: Optimized for creating a structured implementation plan for a coding task, useful when you want to break down a complex feature or change into smaller, manageable steps."

---

#### 2. **GitHub Copilot** - GitHub官方实现 ⭐⭐⭐⭐⭐

**来源**: [GitHub Blog - Introducing Agent HQ](https://github.blog/news-insights/company-news/welcome-home-agents/)

**引用原文**：
> "GitHub introduced Plan Mode, which works with Copilot and asks clarifying questions along the way to help build a step-by-step approach for tasks. Once you approve, your plan goes to Copilot to start implementing."

**关键特性**：
- Plan模式会主动提问，明确需求
- 生成步骤化的实施计划
- 用户确认后开始执行

---

#### 3. **LangChain agent-chat-ui** - 开源项目 ⭐⭐⭐

**来源**: [langchain-ai/agent-chat-ui](https://github.com/langchain-ai/agent-chat-ui)

**特点**：
- React UI for LangGraph agents
- 支持流式输出和工具调用
- 使用hooks管理状态（`useArtifact`, `useStreamContext`）

**参考价值**：
- 提供了React组件的实现参考
- 流式数据处理的最佳实践

---

#### 4. **CopilotKit** - React AI框架 ⭐⭐⭐⭐

**来源**: [CopilotKit/CopilotKit](https://github.com/CopilotKit/CopilotKit)

**特点**：
- React UI + AI Copilots基础设施
- 支持LangGraph.js和LangGraph Python
- 中间状态流式输出

**参考价值**：
- 提供了完整的React集成方案
- 支持多种Agent框架

---

#### 5. **assistant-ui** - 热门React库 ⭐⭐⭐⭐

**来源**: [assistant-ui/assistant-ui](https://github.com/assistant-ui/assistant-ui)

**数据**：
- 400k+ 月下载量
- TypeScript/React库
- 支持流式、生成式UI、人机交互

**设计理念**：
- Radix风格的可组合primitives
- 不是monolithic组件

---

## 📊 调研结论

### 行业标准命名

经过调研，**Ask/Plan/Agent** 是行业标准命名：

| 命名来源 | 市场地位 | 用户量 | 可信度 |
|---------|---------|--------|--------|
| VS Code Copilot | 微软官方IDE | 百万级 | ⭐⭐⭐⭐⭐ |
| GitHub Copilot | GitHub官方 | 百万级 | ⭐⭐⭐⭐⭐ |
| assistant-ui | 开源热门库 | 400k+月下载 | ⭐⭐⭐⭐ |

### 命名方案对比

#### 方案A：技术命名（当前）

```typescript
❌ 用户视角不友好
- chat()       // 用户：这是普通聊天吗？
- planning     // 用户：什么是planning？
- react        // 用户：React框架？？
```

**问题**：
- 技术术语，用户不理解
- 需要阅读文档才能知道用途
- 容易混淆（react vs React.js）

#### 方案B：用户友好命名（推荐）✅

```typescript
✅ 用户一看就懂
- Ask    💬  // 我想问个问题
- Plan   📋  // 我需要完成一个任务
- Agent  🤖  // 帮我自主完成复杂工作
```

**优势**：
- ✅ 符合用户心智模型
- ✅ 清晰的使用场景
- ✅ 业界标准，用户熟悉
- ✅ 易于理解，无需文档

---

## 🎯 最终方案

### 模式映射关系

| 前端显示 | 图标 | 后端mode参数 | API方法 | 流式 | 用户场景 |
|---------|------|-------------|---------|------|---------|
| **Ask** | 💬 | `chat` | `/chat` | ❌ | "帮我看看这段文字" |
| **Plan** | 📋 | `planning` | `/chat/stream` | ✅ | "帮我写第三章" |
| **Agent** | 🤖 | `react` | `/chat/stream` | ✅ | "帮我分析并优化整个作品" |

### TypeScript类型定义

```typescript
// src/types/agent.ts

/**
 * Agent模式 - 用户友好命名
 *
 * @see https://code.visualstudio.com/docs/copilot/chat/copilot-chat
 */
export type AgentMode = 'ask' | 'plan' | 'agent';

/**
 * 后端技术模式 - 内部使用
 */
type BackendMode = 'chat' | 'planning' | 'react';

/**
 * 模式配置
 */
interface ModeConfig {
  backendMode: BackendMode;  // 映射到后端参数
  streaming: boolean;         // 是否流式
  label: string;              // 显示名称
  icon: string;               // 图标
  description: string;        // 描述
}

/**
 * 模式配置表
 */
export const MODE_CONFIG: Record<AgentMode, ModeConfig> = {
  'ask': {
    backendMode: 'chat',
    streaming: false,
    label: 'Ask',
    icon: '💬',
    description: '快速问答，简单咨询'
  },
  'plan': {
    backendMode: 'planning',
    streaming: true,
    label: 'Plan',
    icon: '📋',
    description: '先规划再执行，任务分解'
  },
  'agent': {
    backendMode: 'react',
    streaming: true,
    label: 'Agent',
    icon: '🤖',
    description: '复杂任务，自主操作'
  }
};
```

### API调用示例

```typescript
// src/services/agentApi.ts

/**
 * 统一的Agent调用接口
 *
 * @param mode - 用户选择的模式（Ask/Plan/Agent）
 * @param request - 请求参数
 */
async chatWithMode(
  mode: AgentMode,
  request: AgentChatRequest
): Promise<void> {
  const config = MODE_CONFIG[mode];

  // 映射到后端mode参数
  const backendRequest = {
    ...request,
    mode: config.backendMode  // 'chat' | 'planning' | 'react'
  };

  if (config.streaming) {
    return this.chatStream(backendRequest);
  } else {
    return this.chatBasic(backendRequest);
  }
}
```

---

## 🎨 UI设计方案

### 参考VS Code的简洁设计

**核心理念**：
- 按钮极简（只显示图标）
- 菜单详细（显示所有信息）
- 用户点击后立即了解所有选项

**布局位置**：
```
┌─────────────────────────────────────┐
│           消息列表                   │
├─────────────────────────────────────┤
│ [∞▼] ┌──────────────┐ [📎] [发送]  │
│  ↑   │ 输入框...    │              │
│  └─ 左下角                          │
└─────────────────────────────────────┘
```

**交互流程**：
```
1. 默认状态：[∞▼]
   - 只显示图标和下拉箭头
   - 保持简洁

2. 点击后：向上弹出菜单
   ┌───────────────┐
   │ 💬 Ask        │
   │ 📋 Plan  ✏️ ✓ │  ← 当前选中
   │ 🤖 Agent      │
   └───────────────┘

3. 选择模式：菜单关闭，开始使用
```

---

## ✅ 采用建议

### 推荐方案：Ask/Plan/Agent

**理由**：

1. **业界标准** ⭐⭐⭐⭐⭐
   - VS Code Copilot（微软）
   - GitHub Copilot（GitHub）
   - 百万级用户验证

2. **用户友好** ⭐⭐⭐⭐⭐
   - 符合用户心智模型
   - 无需阅读文档
   - 场景清晰明确

3. **技术优雅** ⭐⭐⭐⭐
   - 前端用户化命名
   - 后端技术化命名
   - 通过配置映射解耦

4. **易于扩展** ⭐⭐⭐⭐
   - 未来可以添加新模式
   - 配置化管理
   - 不影响现有代码

### 实施优先级

1. **P0（立即）**: 采用Ask/Plan/Agent命名
2. **P0（立即）**: 实现ModeSelector组件
3. **P1（本周）**: 集成到AgentChatPanel
4. **P1（本周）**: 根据mode调用不同API
5. **P2（下周）**: 完善不同模式的UI差异

---

## 📚 参考资料

### 官方文档

1. **VS Code Copilot Chat**
   - https://code.visualstudio.com/docs/copilot/chat/copilot-chat
   - 4种模式的官方文档

2. **GitHub Blog - Agent HQ**
   - https://github.blog/news-insights/company-news/welcome-home-agents/
   - Plan Mode介绍

### GitHub项目

1. **langchain-ai/agent-chat-ui**
   - https://github.com/langchain-ai/agent-chat-ui
   - LangGraph Agent的React UI

2. **CopilotKit/CopilotKit**
   - https://github.com/CopilotKit/CopilotKit
   - React UI for AI Copilots

3. **assistant-ui/assistant-ui**
   - https://github.com/assistant-ui/assistant-ui
   - 400k+月下载的React库

### 技术文章

1. **Plan Mode vs Agent Mode: Understanding GitHub's Revolutionary Coding Workflows**
   - https://skywork.ai/blog/agent/plan-mode-vs-agent-mode-understanding-githubs-revolutionary-coding-workflows/

2. **Build stateful conversational AI agents with LangGraph and assistant-ui**
   - https://blog.langchain.com/assistant-ui/

---

## 📝 附录：调研数据

### Web搜索结果统计

| 搜索词 | 结果数 | 相关度 | 关键发现 |
|-------|--------|--------|---------|
| AI agent mode selector | 10 | 高 | VS Code Copilot为主流方案 |
| chatbot plan ask agent | 10 | 高 | GitHub采用相同命名 |
| LangChain agent UI | 10 | 中 | 提供React实现参考 |

### 项目受欢迎程度

| 项目 | GitHub Stars | NPM下载量 | 最后更新 |
|------|-------------|-----------|---------|
| assistant-ui | 未提供 | 400k+/月 | 2024 |
| CopilotKit | 未提供 | 未提供 | 2024 |
| agent-chat-ui | 未提供 | 未提供 | 2024 |

---

**报告生成时间**: 2025-11-09
**下一步**: 实施ModeSelector组件，采用Ask/Plan/Agent命名方案
**预计完成**: 1个工作日

