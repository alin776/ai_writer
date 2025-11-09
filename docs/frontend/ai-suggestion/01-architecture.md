# 架构设计文档（实际实现）

## ⚠️ 重要说明

本文档已更新为反映**实际代码实现**。与最初设计方案相比，实际架构更加完善和功能丰富。

## 🏗️ 实际整体架构

### 系统分层（实际）

```
┌─────────────────────────────────────────────────────────┐
│              EditorView (src/views/EditorView.tsx)      │
├─────────────────────────────────────────────────────────┤
│                                                          │
│  ┌─────────────────────┐      ┌──────────────────────┐ │
│  │   NovelEditor       │      │  AgentChatPanel      │ │
│  │   (Tiptap 编辑器)   │      │  (智能助手面板)     │ │
│  │                     │      │                      │ │
│  │  ┌──────────────┐   │      │  ┌───────────────┐  │ │
│  │  │AIHighlight   │   │      │  │AgentMessage   │  │ │
│  │  │Extension     │   │      │  │(Markdown渲染) │  │ │
│  │  └──────────────┘   │      │  └───────────────┘  │ │
│  │  ┌──────────────┐   │      │  ┌───────────────┐  │ │
│  │  │AIAutoComplete│   │      │  │TaskListPanel  │  │ │
│  │  │Extension     │   │      │  │(Planning任务) │  │ │
│  │  └──────────────┘   │      │  └───────────────┘  │ │
│  │  ┌──────────────┐   │      │  ┌───────────────┐  │ │
│  │  │AIMenu        │   │      │  │ChatInput      │  │ │
│  │  │(操作菜单)    │   │      │  │(输入框)       │  │ │
│  │  └──────────────┘   │      │  └───────────────┘  │ │
│  └─────────┬───────────┘      └──────────┬───────────┘ │
│            │                             │             │
│       ┌────▼──────────┐         ┌────────▼──────────┐  │
│       │ useAI Hook    │         │ useAgentChat Hook │  │
│       └────┬──────────┘         └────────┬──────────┘  │
├────────────┼─────────────────────────────┼─────────────┤
│            │        服务层 (SSE)          │             │
│       ┌────▼──────────┐         ┌────────▼──────────┐  │
│       │ AIService.ts  │         │ agentApi.ts       │  │
│       │ - complete()  │         │ - chatStream()    │  │
│       │ - expand()    │         │ - chatReactStream()│ │
│       │ - polish()    │         │                   │  │
│       │ - translate() │         │                   │  │
│       └───────────────┘         └───────────────────┘  │
└─────────────────────────────────────────────────────────┘
```

## 📊 实际数据流

### 1. 编辑器 AI 续写流程（实际）

```
用户选中文本 → 右键或选中后出现 AIMenu
     ↓
点击"续写" → 打开续写配置弹窗
     ↓
配置参数（风格、情绪、字数、情节点等）
     ↓
AIMenu.handleContinueWithConfig()
     ↓
useAI.complete(config, onChunk)
     ↓
AIService.complete() → 发起 SSE 流式请求到 /api/v1/ai/complete
     ↓
SSE 实时返回 → onChunk 回调
     ↓
每个 chunk:
  1. editor.insertContent(chunk)  // 插入文本
  2. editor.setMark('aiHighlight') // 设置黄色高亮
     ↓
用户决策：
  - ✅ 同意 → editor.unsetMark('aiHighlight')，保留内容
  - ✕ 撤销 → 删除插入的内容，恢复原状
  - ⏸ 暂停 → AIService.cancel()
```

### 2. Agent 对话流程（实际）

```
用户在 AgentChatPanel 输入消息
     ↓
useAgentChat.sendMessageStream(message, scenario)
     ↓
agentApi.chatStream() → SSE 连接到 /api/v1/agent/chat_stream
     ↓
SSE 事件序列：
  start → plan → task_start → task_progress → task_done → content → done
     ↓
实时更新：
  - AgentMessage 显示消息内容（Markdown 渲染）
  - TaskListPanel 显示任务进度
  - ThinkingIndicator 显示思考状态
  - SuggestedActions 显示建议操作
     ↓
对话历史保存，conversation_id 保持连贯性
```

### 3. 自动补全流程（实际）

```
用户停止输入 → 3秒延迟（可配置）
     ↓
AIAutoCompleteExtension 触发
     ↓
从编辑器获取上下文（前N个字符）
     ↓
AIService.quickComplete(context)
     ↓
返回补全建议
     ↓
使用 ProseMirror Decoration 显示为虚拟文本（浅色）
     ↓
用户操作：
  - Tab → 接受建议，插入文本
  - Esc → 拒绝建议，清除显示
  - 继续输入 → 自动拒绝，清除显示
```

## 🔧 实际核心模块

### 1. 编辑器 AI 状态管理（实际）

**文件**: `src/hooks/useAI.ts`

**职责**:
- 封装 AIService 的所有 AI 功能调用
- 管理加载状态和错误处理
- 提供统一的 AI 操作接口

**接口**:
```typescript
interface UseAIReturn {
  isLoading: boolean;
  error: string | null;
  complete: (config, onChunk) => Promise<string>;
  expand: (text, targetLength) => Promise<string>;
  summarize: (text) => Promise<string>;
  polish: (text) => Promise<string>;
  translate: (text, targetLang) => Promise<string>;
  cancel: () => void;
}
```

### 2. Agent 对话状态管理（实际）

**文件**: `src/hooks/useAgentChat.ts`

**职责**:
- 管理对话历史消息
- 处理流式对话的事件
- 维护任务列表状态
- 保持 conversation_id

**接口**:
```typescript
interface UseAgentChatReturn {
  messages: Message[];
  tasks: Task[];
  isLoading: boolean;
  error: string | null;
  conversationId?: string;
  suggestedActions: string[];
  sendMessage: (message) => Promise<void>;
  sendMessageStream: (message, scenario) => Promise<void>;
  clearMessages: () => void;
}
```

### 3. 编辑器扩展层（实际）

#### AIHighlightExtension
**文件**: `src/components/editor/AIHighlightExtension.ts`

**职责**:
- 定义 aiHighlight Mark 类型
- 渲染为 `<mark class="ai-highlight">` 标签
- 提供 setAIHighlight/unsetAIHighlight 命令

**Mark 特性**:
- 黄色背景高亮
- 可通过命令设置/移除
- 不影响文本内容

#### AIAutoCompleteExtension
**文件**: `src/components/editor/AIAutoCompleteExtension.tsx`

**职责**:
- 监听用户输入停止（3秒延迟）
- 获取编辑器上下文
- 使用 Decoration 显示补全建议
- 处理 Tab/Esc 快捷键

**Plugin 机制**:
- ProseMirror Plugin
- DecorationSet 虚拟文本显示
- 键盘事件拦截

### 4. UI 组件层（实际）

#### AIMenu
**文���**: `src/components/editor/AIMenu.tsx`

**功能**:
- 续写（带详细配置：风格、情绪、字数、情节点）
- 扩写
- 总结
- 润色
- 翻译

**交互**:
- 选中文本后弹出
- 模态弹窗配置参数
- 实时流式插入
- 同意/撤销/暂停按钮

#### AgentChatPanel
**文件**: `src/components/agent/AgentChatPanel.tsx`

**功能**:
- 4 种场景选择（写作/规划/分析/卡文）
- 消息列表显示（支持 Markdown）
- Planning 任务进度追踪
- 建议操作快捷按钮

**状态显示**:
- ThinkingIndicator（思考中）
- ProgressIndicator（进度条）
- Token 统计显示

### 5. 服务层（实际）

#### AIService
**文件**: `src/services/AIService.ts`

**核心方法**:
```typescript
class AIService {
  // 流式续写（SSE）
  async complete(config, onChunk): Promise<string>

  // 同步续写
  async completeSync(config): Promise<string>

  // 文本扩写
  async expand(text, targetLength): Promise<string>

  // 文本总结
  async summarize(text): Promise<string>

  // 文本润色
  async polish(text): Promise<string>

  // 文本翻译
  async translate(text, targetLang): Promise<string>

  // 取消请求
  cancel(): void
}
```

#### agentApi
**文件**: `src/services/agentApi.ts`

**核心方法**:
```typescript
// Planning + Execution 流式对话
async function chatStream(
  request: AgentChatRequest,
  onEvent: (event) => void
): Promise<void>

// ReAct 模式流式对话
async function chatReactStream(
  request: AgentChatRequest,
  onProgress: (data) => void
): Promise<void>

// 非流式对话
async function chat(
  request: AgentChatRequest
): Promise<AgentChatResponse>
```

**SSE 事件类型**:
- start: 开始生成
- plan: 计划生成
- task_start: 任务开始
- task_progress: 任务进度
- task_done: 任务完成
- content: 内容片段
- done: 完成
- error: 错误

## 📦 实际文件结构

```
src/
├── components/
│   ├── editor/
│   │   ├── NovelEditor.tsx                  # Tiptap 编辑器主组件
│   │   ├── AIMenu.tsx                       # AI 操作菜单
│   │   ├── AIHighlightExtension.ts          # AI 高亮标记扩展
│   │   ├── AIAutoCompleteExtension.tsx      # 自动补全扩展
│   │   ├── AIAutoComplete.tsx               # 补全 UI 组件
│   │   ├── AICompletionCommands.tsx         # 补全命令组件
│   │   ├── BubbleMenu.tsx                   # 气泡菜单
│   │   └── SlashCommandExtension.tsx        # 斜杠命令扩展
│   └── agent/
│       ├── AgentChatPanel.tsx               # Agent 对话面板
│       ├── AgentMessage.tsx                 # 消息组件
│       ├── ChatInput.tsx                    # 输入框组件
│       ├── TaskListPanel.tsx                # 任务列表面板
│       ├── ThinkingIndicator.tsx            # 思考指示器
│       ├── ProgressIndicator.tsx            # 进度指示器
│       └── SuggestedActions.tsx             # 建议操作按钮
├── hooks/
│   ├── useAI.ts                             # AI 功能 Hook
│   ├── useAgentChat.ts                      # Agent 对话 Hook
│   └── useAgentChatStream.ts                # Agent 流式对话 Hook
├── services/
│   ├── AIService.ts                         # AI 服务（SSE 流式）
│   └── agentApi.ts                          # Agent API（SSE 流式）
├── types/
│   ├── agent.ts                             # Agent 类型定义
│   └── index.ts                             # 通用类型定义
└── views/
    └── EditorView.tsx                       # 编辑器视图容器
```

## 🎯 实际设计原则

### 1. 功能分离
- AI 编辑功能（AIService + useAI）独立于 Agent 对话（agentApi + useAgentChat）
- 编辑器扩展（Extension）与 UI 组件分离
- 服务层统一处理 SSE 流式传输

### 2. 双 SSE 架构
```
编辑器 AI 流:
  AIMenu → useAI → AIService → /api/v1/ai/complete (SSE)

Agent 对话流:
  AgentChatPanel → useAgentChat → agentApi → /api/v1/agent/chat_stream (SSE)
```

### 3. 实时反馈优化
- 使用 onChunk 回调实时插入文本
- 使用 Decoration 显示虚拟补全
- 使用 ThinkingIndicator/ProgressIndicator 显示进度

### 4. 类型安全
- 所有接口定义 TypeScript 类型
- Agent 类型在 `src/types/agent.ts` 中统一定义
- 严格模式编译

## 🔌 实际扩展点

### 1. 自定义 AI 高亮样式
通过 CSS 覆盖：
```css
.ai-highlight {
  background-color: rgba(255, 235, 59, 0.3);
  border-bottom: 2px dashed #FFD700;
}
```

### 2. 自定义补全延迟
修改 AIAutoCompleteExtension 配置：
```typescript
AIAutoCompleteExtension.configure({
  delay: 5000,  // 修改为 5 秒
})
```

### 3. 自定义 Agent 场景
在 AgentChatPanel 中添加新场景：
```typescript
const scenarios = [
  { id: 'writing', label: '写作助手', icon: '✍️' },
  { id: 'custom', label: '自定义场景', icon: '🔧' },
  // 添加更多...
];
```

### 4. 自定义 SSE 事件处理
在 useAgentChat 中扩展事件处理：
```typescript
onEvent: (event) => {
  switch (event.type) {
    case 'custom_event':
      // 处理自定义事件
      break;
  }
}
```

## 📈 性能优化（已实现）

### 1. 流式插入优化
- SSE 实时流式传输，避免长时间等待
- 使用 AbortController 支持取消请求
- 缓冲区处理不完整的数据行

### 2. 编辑器性能
- Tiptap 基于 ProseMirror，高性能虚拟 DOM
- Decoration 用于虚拟文本显示，不修改文档结构
- 防抖输入处理（自动补全延迟触发）

### 3. 内存管理
- 对话历史限制最大数量
- SSE 连接完成后自动清理
- 组件卸载时清理订阅和定时器

## 🔍 与设计文档的主要差异

| 设计文档 | 实际实现 | 说明 |
|---------|---------|------|
| AIPendingMark | AIHighlightExtension | 名称不同，功能相似 |
| AISuggestionCard | AIMenu + AgentMessage | 拆分为编辑器菜单和Agent消息 |
| useAISuggestion | useAI + useAgentChat | 拆分为两个独立的Hook |
| 单一流式接口 | 双SSE架构 | 编辑器AI和Agent分别使用独立SSE |
| EditorContext | 直接使用 Hook | 简化状态管理，无需Context |

**总结**：实际实现比设计文档更加完善，功能更丰富，架构更清晰。
