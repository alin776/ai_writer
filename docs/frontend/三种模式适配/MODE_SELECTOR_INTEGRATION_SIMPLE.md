# ModeSelector 集成示例（简洁版）

## 修改 AgentChatPanel.tsx

### Step 1: 添加 import

```typescript
import ModeSelector, { AgentMode, MODE_CONFIG } from './ModeSelector';
```

### Step 2: 添加 mode 状态

```typescript
const [mode, setMode] = useState<AgentMode>('plan'); // 默认Plan模式
```

### Step 3: 修改输入框区域（行179-185）

**原代码**：
```typescript
{/* 输入框 */}
<div className="px-4 py-3 border-t border-gray-200">
  <ChatInput
    onSend={handleSendMessage}
    disabled={isLoading}
    placeholder="试试：帮我写第三章..."
  />
</div>
```

**修改为**：
```typescript
{/* 输入框 */}
<div className="px-4 py-3 border-t border-gray-200">
  <div className="flex items-end gap-2">
    {/* 左下角：模式选择器 */}
    <div className="flex-shrink-0 pb-[1px]">
      <ModeSelector
        mode={mode}
        onModeChange={setMode}
        disabled={isLoading}
      />
    </div>

    {/* 右侧：输入框 */}
    <div className="flex-1">
      <ChatInput
        onSend={handleSendMessage}
        disabled={isLoading}
        placeholder="试试：帮我写第三章..."
      />
    </div>
  </div>
</div>
```

### Step 4: 根据 mode 调用不同 API（可选）

```typescript
const handleSendMessage = async (message: string, context?: any) => {
  const request = {
    message,
    work_id: workId,
    chapter_id: chapterId,
    conversation_id: conversationId,
    context
  };

  // 根据模式选择不同的调用方式
  const config = MODE_CONFIG[mode];

  if (mode === 'ask') {
    // Ask模式 - 使用非流式API
    const response = await sendMessage(request);
    if (response?.conversation_id) {
      setConversationId(response.conversation_id);
    }
  } else {
    // Plan/Agent模式 - 使用流式API
    await sendMessageStream(request);
  }
};
```

---

## 完整修改示例

```typescript
import React, { useState, useRef, useEffect } from 'react';
import { useAgentChat } from '@/hooks/useAgentChat';
import AgentMessage from './AgentMessage';
import ChatInput from './ChatInput';
import SuggestedActions from './SuggestedActions';
import ThinkingIndicator from './ThinkingIndicator';
import TaskListPanel from './TaskListPanel';
import ModeSelector, { AgentMode, MODE_CONFIG } from './ModeSelector'; // ← 新增

interface AgentChatPanelProps {
  workId?: string;
  chapterId?: string;
  initialMessage?: string;
  className?: string;
}

export default function AgentChatPanel({
  workId,
  chapterId,
  initialMessage,
  className = ''
}: AgentChatPanelProps) {
  const {
    messages,
    sendMessage,
    sendMessageStream,
    isLoading,
    suggestedActions,
    tasks,
    currentTaskId,
    clearMessages
  } = useAgentChat();

  const [conversationId, setConversationId] = useState<string | null>(null);
  const [mode, setMode] = useState<AgentMode>('plan'); // ← 新增：默认Plan模式
  const messagesEndRef = useRef<HTMLDivElement>(null);

  // ... 其他代码保持不变 ...

  return (
    <div className={`agent-chat-panel flex flex-col h-full bg-white rounded-lg shadow-lg ${className}`}>
      {/* 头部 */}
      <div className="chat-header px-4 py-3 border-b border-gray-200 bg-gradient-to-r from-blue-50 to-indigo-50">
        {/* ... 保持不变 ... */}
      </div>

      {/* 消息列表 */}
      <div className="messages flex-1 overflow-y-auto px-4 py-3 space-y-4">
        {/* ... 保持不变 ... */}
      </div>

      {/* 建议操作 */}
      {suggestedActions.length > 0 && !isLoading && (
        <div className="px-4 py-2 border-t border-gray-100 bg-gray-50">
          <SuggestedActions
            actions={suggestedActions}
            onActionClick={handleSendMessage}
          />
        </div>
      )}

      {/* 输入框 - 修改这里 ↓ */}
      <div className="px-4 py-3 border-t border-gray-200">
        <div className="flex items-end gap-2">
          {/* 左下角：模式选择器 */}
          <div className="flex-shrink-0 pb-[1px]">
            <ModeSelector
              mode={mode}
              onModeChange={setMode}
              disabled={isLoading}
            />
          </div>

          {/* 右侧：输入框 */}
          <div className="flex-1">
            <ChatInput
              onSend={handleSendMessage}
              disabled={isLoading}
              placeholder="试试：帮我写第三章..."
            />
          </div>
        </div>
      </div>

      {/* 快捷操作按钮 */}
      {messages.length === 0 && (
        <div className="px-4 pb-3 pt-1">
          {/* ... 保持不变 ... */}
        </div>
      )}
    </div>
  );
}
```

---

## 视觉效果

### 关闭状态
```
┌──────────────────────────────────────┐
│ [∞▼]  ┌────────────────┐  [📎][发送] │
│       │ 输入框...      │             │
│       └────────────────┘             │
└──────────────────────────────────────┘
```

### 打开状态
```
       ┌───────────────┐
       │ 💬 Ask        │
       │ 📋 Plan  ✏️ ✓ │  ← 深色主题
       │ 🤖 Agent      │
       └───────────────┘
┌──────────────────────────────────────┐
│ [∞▲]  ┌────────────────┐  [📎][发送] │
│       │ 输入框...      │             │
│       └────────────────┘             │
└──────────────────────────────────────┘
```

---

## 核心优势

1. ✅ **极简设计** - 按钮只显示图标
2. ✅ **信息清晰** - 菜单里显示所有必要信息
3. ✅ **空间高效** - 不占用输入框空间
4. ✅ **符合VS Code** - 业界成熟实践
5. ✅ **深色主题** - 现代化视觉

---

## 下一步

你可以直接使用这个集成方案，只需：
1. 在 AgentChatPanel.tsx 添加 mode 状态
2. 修改输入框区域布局
3. 根据 mode 调用不同的 API（可选）

完全不需要修改其他文件，保持简洁！🎯
