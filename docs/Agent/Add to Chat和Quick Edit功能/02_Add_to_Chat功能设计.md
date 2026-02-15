# Add to Chat 功能详细设计

## 📋 功能概述

**Add to Chat** 是一个快速将编辑器中选中文本发送到AI助手对话框的功能，旨在建立编辑器与AI助手之间的无缝连接。

### 核心价值
- 🎯 **减少操作步骤：** 从选中文本到AI处理，仅需一键
- 🔄 **保持上下文：** 自动将文本传递到Agent
- 💡 **灵活交互：** 用户可自由输入提示词进行各种操作
- ⚡ **提升效率：** 无需手动复制粘贴

### ⚠️ 重要说明：纯前端实现

**后端改动：** ❌ **无需任何后端代码改动**

本功能是**纯前端实现**，通过以下方式复用现有API：
- 使用现有的 `/api/v1/agent/chat/stream` 端点
- Agent API已经完美支持接收自定义消息
- 只需前端进行状态传递和UI交互即可

**前置条件：** ⚠️ 需要先完成 `AIService.ts` 的修复（详见 [04_前后端协作方案.md](./04_前后端协作方案.md)）

---

## 🎨 用户交互流程

### 完整流程图

```
┌──────────────────┐
│ 1. 用户在编辑器  │
│    中选中文本     │
└────────┬─────────┘
         │
         ▼
┌──────────────────┐
│ 2. 浮动菜单出现  │  ← BubbleMenu / AIMenu
│    包含:          │
│    - Bold         │
│    - Italic       │
│    - Ask AI       │
│    - [Add to Chat]│  ← 新增按钮
└────────┬─────────┘
         │
         ▼
┌──────────────────┐
│ 3. 用户点击      │
│    "Add to Chat" │
└────────┬─────────┘
         │
         ├─────────────────────┐
         │                     │
         ▼                     ▼
┌──────────────────┐    ┌──────────────────┐
│ 4a. 自动打开     │    │ 4b. 如果侧边栏   │
│     Agent侧边栏  │    │     已打开，直接 │
│     (如果未打开) │    │     聚焦Agent面板│
└────────┬─────────┘    └────────┬─────────┘
         │                       │
         └───────────┬───────────┘
                     │
                     ▼
         ┌──────────────────┐
         │ 5. 文本传递到    │
         │    Agent面板     │
         │    (两种模式)    │
         └────────┬─────────┘
                  │
         ┌────────┴────────┐
         │                 │
         ▼                 ▼
┌──────────────────┐ ┌──────────────────┐
│ 模式A: 填充输入框│ │ 模式B: 直接发送  │
│ 用户可继续编辑  │ │ 自动触发AI响应   │
└────────┬─────────┘ └────────┬─────────┘
         │                    │
         └────────┬───────────┘
                  │
                  ▼
         ┌──────────────────┐
         │ 6. 用户在Agent   │
         │    中输入提示词  │
         │    与AI交互      │
         └──────────────────┘
```

### 交互模式选择

我们提供两种交互模式，可通过配置切换：

| 模式 | 描述 | 优点 | 缺点 | 推荐场景 |
|------|------|------|------|---------|
| **模式A: 填充输入框** | 将文本填充到输入框，等待用户输入提示词 | 灵活、可编辑、无误操作 | 需要多一步操作 | 需要精确控制提示词 |
| **模式B: 直接发送** | 自动发送文本到Agent，触发默认提示 | 快速、自动化 | 可能不是用户想要的操作 | 快速预览或分析 |

**推荐:** 默认使用 **模式A（填充输入框）**，未来可以添加设置选项让用户切换。

---

## 🏗️ 技术架构

### 架构图

```
┌────────────────────────────────────────────────┐
│              Editor View (EditorView.tsx)      │
│  ┌──────────────────────────────────────────┐ │
│  │         Novel Editor (NovelEditor.tsx)   │ │
│  │  ┌────────────────────────────────────┐  │ │
│  │  │  BubbleMenu / AIMenu               │  │ │
│  │  │  ┌──────────────────────────────┐  │  │ │
│  │  │  │ [Add to Chat] 按钮           │  │  │ │
│  │  │  │  onClick: setAddToChatText() │  │  │ │
│  │  │  └──────────────────────────────┘  │  │ │
│  │  └────────────────────────────────────┘  │ │
│  └──────────────────────────────────────────┘ │
│                                                │
│  ┌──────────────────────────────────────────┐ │
│  │  Agent Sidebar (AgentChatPanel.tsx)     │ │
│  │  ┌────────────────────────────────────┐ │ │
│  │  │  useEffect: 监听 addToChatText     │ │ │
│  │  │  ↓                                  │ │ │
│  │  │  填充到输入框 / 直接发送            │ │ │
│  │  └────────────────────────────────────┘ │ │
│  └──────────────────────────────────────────┘ │
└────────────────────────────────────────────────┘
                      ↕
         ┌────────────────────────┐
         │  Zustand Store         │
         │  (useEditorStore)      │
         │  ┌──────────────────┐  │
         │  │ addToChatText    │  │
         │  │ setAddToChatText │  │
         │  │ clearAddToChatText│ │
         │  └──────────────────┘  │
         └────────────────────────┘
```

### 组件职责划分

| 组件 | 职责 | 输入 | 输出 |
|------|------|------|------|
| **BubbleMenu** | 显示浮动菜单，提供Add to Chat按钮 | 选中文本 | 触发setAddToChatText |
| **AIMenu** | 显示AI操作菜单，提供Add to Chat按钮 | 选中文本 | 触发setAddToChatText |
| **EditorView** | 监听状态变化，控制侧边栏显示 | addToChatText状态 | 打开/切换侧边栏 |
| **AgentChatPanel** | 接收文本，填充输入框或直接发送 | addToChatText状态 | 清除状态，发送消息 |
| **useEditorStore** | 全局状态管理 | set/clear操作 | 状态变化通知 |

---

## 💾 状态管理设计

### Zustand Store扩展

```typescript
// src/store/editorStore.ts

import { create } from 'zustand';

interface AddToChatConfig {
  text: string;
  mode: 'fill' | 'send';  // 模式A: fill, 模式B: send
  timestamp: number;      // 防止重复处理
}

interface EditorStore {
  // ... 现有状态

  // Add to Chat状态
  addToChatConfig: AddToChatConfig | null;

  // 设置Add to Chat配置
  setAddToChatText: (text: string, mode?: 'fill' | 'send') => void;

  // 清除Add to Chat状态
  clearAddToChatText: () => void;
}

export const useEditorStore = create<EditorStore>((set) => ({
  // ... 现有实现

  addToChatConfig: null,

  setAddToChatText: (text, mode = 'fill') => {
    set({
      addToChatConfig: {
        text,
        mode,
        timestamp: Date.now(),
      },
    });
  },

  clearAddToChatText: () => {
    set({ addToChatConfig: null });
  },
}));
```

### 状态流转时序图

```
Time    BubbleMenu          EditorStore         EditorView          AgentChatPanel
─────────────────────────────────────────────────────────────────────────────────
  │
  │ 用户点击
  │ Add to Chat
  ├──────>│
  │       │ setAddToChatText()
  │       ├──────>│
  │       │       │ 状态: addToChatConfig = { text, mode, timestamp }
  │       │       │
  │       │       ├──────>│
  │       │       │       │ useEffect监听
  │       │       │       │ 检测到addToChatConfig
  │       │       │       │
  │       │       │       │ setSidebarType('agent')
  │       │       │       ├──────>│
  │       │       │       │       │ useEffect监听
  │       │       │       │       │ 检测到addToChatConfig
  │       │       │       │       │
  │       │       │       │       │ if mode === 'fill':
  │       │       │       │       │   setInputValue(text)
  │       │       │       │       │ else:
  │       │       │       │       │   sendMessage(text)
  │       │       │       │       │
  │       │       │       │       │ clearAddToChatText()
  │       │       │       │       ├──────>│
  │       │       │       │       │       │ 状态: addToChatConfig = null
  │       │       │       │       │<──────┤
  │       │       │       │<──────┤
  │       │       │<──────┤
  │<──────┤       │
  │       │       │
```

---

## 🔧 组件实现细节

### 1. BubbleMenu 扩展

**文件:** `src/components/editor/BubbleMenu.tsx`

```typescript
import React, { useState } from 'react';
import { BubbleMenu as TiptapBubbleMenu } from '@tiptap/react/menus';
import { Editor } from '@tiptap/core';
import {
  Bold,
  Italic,
  Sparkles,
  MessageSquarePlus,  // ← 新增图标
} from 'lucide-react';
import AIAutoComplete from './AIAutoComplete';
import { useEditorStore } from '@/store/editorStore';  // ← 新增

interface BubbleMenuProps {
  editor: Editor;
}

const BubbleMenu: React.FC<BubbleMenuProps> = ({ editor }) => {
  const [openAI, setOpenAI] = useState(false);
  const setAddToChatText = useEditorStore(state => state.setAddToChatText);  // ← 新增

  if (!editor) {
    return null;
  }

  // ← 新增: Add to Chat处理函数
  const handleAddToChat = () => {
    const { from, to } = editor.state.selection;
    const selectedText = editor.state.doc.textBetween(from, to, ' ');

    if (selectedText.trim()) {
      setAddToChatText(selectedText, 'fill');  // 默认使用填充模式
    }
  };

  // 当 AI 面板打开时...
  if (openAI) {
    return (
      <TiptapBubbleMenu editor={editor} className="bubble-menu-container ai-mode">
        <AIAutoComplete editor={editor} onOpenChange={setOpenAI} />
      </TiptapBubbleMenu>
    );
  }

  return (
    <TiptapBubbleMenu editor={editor} className="bubble-menu-container">
      {/* Ask AI 按钮 */}
      <button
        onClick={() => setOpenAI(true)}
        className="bubble-menu-button ai-button"
        title="Ask AI"
        type="button"
      >
        <Sparkles className="w-4 h-4 text-purple-500" />
        <span className="ml-1 text-sm text-purple-500 font-medium">Ask AI</span>
      </button>

      {/* ← 新增: Add to Chat 按钮 */}
      <button
        onClick={handleAddToChat}
        className="bubble-menu-button add-to-chat-button"
        title="Add to Chat (Ctrl+Shift+A)"
        type="button"
      >
        <MessageSquarePlus className="w-4 h-4 text-blue-500" />
        <span className="ml-1 text-sm text-blue-500 font-medium">Add to Chat</span>
      </button>

      {/* 分隔符 */}
      <div className="bubble-menu-separator" />

      {/* 文本样式 */}
      <div className="bubble-menu-group">
        <button
          onClick={() => editor.chain().focus().toggleBold().run()}
          className={`bubble-menu-button ${editor.isActive('bold') ? 'active' : ''}`}
          title="粗体 (Ctrl+B)"
        >
          <Bold className="w-4 h-4" />
        </button>

        <button
          onClick={() => editor.chain().focus().toggleItalic().run()}
          className={`bubble-menu-button ${editor.isActive('italic') ? 'active' : ''}`}
          title="斜体 (Ctrl+I)"
        >
          <Italic className="w-4 h-4" />
        </button>

        {/* ... 其他按钮 */}
      </div>
    </TiptapBubbleMenu>
  );
};

export default BubbleMenu;
```

---

### 2. AIMenu 扩展

**文件:** `src/components/editor/AIMenu.tsx`

```typescript
// 在AIMenu中也添加Add to Chat按钮
import { MessageSquarePlus } from 'lucide-react';
import { useEditorStore } from '@/store/editorStore';

const AIMenu: React.FC<AIMenuProps> = ({ editor }) => {
  const setAddToChatText = useEditorStore(state => state.setAddToChatText);

  const handleAddToChat = () => {
    const { from, to } = editor.state.selection;
    const selectedText = editor.state.doc.textBetween(from, to, ' ');

    if (selectedText.trim()) {
      setAddToChatText(selectedText, 'fill');
    }
  };

  return (
    <TiptapBubbleMenu editor={editor} shouldShow={shouldShow} className="ai-menu-container">
      {isProcessing ? (
        <div className="ai-menu-loading">
          <Loader2 className="w-4 h-4 animate-spin" />
          <span>AI 处理中...</span>
        </div>
      ) : (
        <>
          {/* 新增: Add to Chat按钮 */}
          <button
            onClick={handleAddToChat}
            className="ai-menu-button"
            title="发送到 AI 助手"
            type="button"
          >
            <MessageSquarePlus className="w-4 h-4" />
            <span className="ai-menu-label">发送到助手</span>
          </button>

          {/* 分隔线 */}
          <div className="ai-menu-separator" />

          {/* 现有按钮: 续写、扩写、总结等 */}
          <button onClick={() => setShowContinueDialog(true)}>
            <Wand2 /> 续写
          </button>
          {/* ... */}
        </>
      )}
    </TiptapBubbleMenu>
  );
};
```

---

### 3. EditorView 监听与侧边栏控制

**文件:** `src/views/EditorView/index.tsx`

```typescript
import React, { useState, useEffect } from 'react';
import { useEditorStore } from '@/store/editorStore';

const EditorView: React.FC = () => {
  const [sidebarType, setSidebarType] = useState<SidebarType>(null);

  // ← 新增: 监听Add to Chat状态
  const addToChatConfig = useEditorStore(state => state.addToChatConfig);

  // ← 新增: 当检测到Add to Chat时，自动打开Agent侧边栏
  useEffect(() => {
    if (addToChatConfig) {
      // 自动切换到Agent侧边栏
      setSidebarType('agent');

      // 记录日志
      console.log('[EditorView] Add to Chat triggered:', {
        textLength: addToChatConfig.text.length,
        mode: addToChatConfig.mode,
        timestamp: addToChatConfig.timestamp,
      });
    }
  }, [addToChatConfig]);

  return (
    <div className={styles.page}>
      {/* ... 现有内容 */}

      {/* Agent对话侧边栏 */}
      {sidebarType === 'agent' && chapter && (
        <div className={styles.sidebar}>
          <div className={styles.sidebarHeader}>
            <h3>AI智能助手</h3>
            <button onClick={() => setSidebarType(null)}>
              <X />
            </button>
          </div>
          <div className={styles.sidebarContent}>
            <AgentChatPanel
              workId={chapter.workId}
              chapterId={chapter.id}
              className="h-full"
              // ← 不需要额外传递props，组件内部自己监听store
            />
          </div>
        </div>
      )}
    </div>
  );
};
```

---

### 4. AgentChatPanel 接收与处理

**文件:** `src/components/agent/AgentChatPanel.tsx`

```typescript
import React, { useState, useRef, useEffect } from 'react';
import { useAgentChat } from '@/hooks/useAgentChat';
import { useEditorStore } from '@/store/editorStore';

export default function AgentChatPanel({ workId, chapterId, className = '' }) {
  const { messages, sendMessage, sendMessageStream, isLoading } = useAgentChat();
  const [inputValue, setInputValue] = useState('');

  // ← 新增: 监听Add to Chat状态
  const addToChatConfig = useEditorStore(state => state.addToChatConfig);
  const clearAddToChatText = useEditorStore(state => state.clearAddToChatText);

  // ← 新增: 处理Add to Chat
  useEffect(() => {
    if (addToChatConfig) {
      const { text, mode, timestamp } = addToChatConfig;

      console.log('[AgentChatPanel] Received Add to Chat:', {
        textLength: text.length,
        mode,
        timestamp,
      });

      if (mode === 'fill') {
        // 模式A: 填充到输入框
        setInputValue(text);

        // 聚焦到输入框
        setTimeout(() => {
          const input = document.querySelector('.chat-input') as HTMLInputElement;
          input?.focus();
        }, 100);
      } else if (mode === 'send') {
        // 模式B: 直接发送
        const request = {
          message: text,
          work_id: workId,
          chapter_id: chapterId,
        };

        sendMessageStream(request);
      }

      // 清除状态（避免重复处理）
      clearAddToChatText();
    }
  }, [addToChatConfig, workId, chapterId, sendMessageStream, clearAddToChatText]);

  const handleSendMessage = async (message: string) => {
    const request = {
      message,
      work_id: workId,
      chapter_id: chapterId,
    };

    await sendMessageStream(request);
    setInputValue('');  // 清空输入框
  };

  return (
    <div className={`agent-chat-panel ${className}`}>
      {/* 消息列表 */}
      <div className="messages">
        {messages.map((msg, index) => (
          <AgentMessage key={index} message={msg} />
        ))}
      </div>

      {/* 输入框 */}
      <div className="chat-input-container">
        <ChatInput
          value={inputValue}
          onChange={setInputValue}
          onSend={() => handleSendMessage(inputValue)}
          disabled={isLoading}
          placeholder="输入消息或提示词..."
        />
      </div>
    </div>
  );
}
```

---

## 🎨 样式设计

### Add to Chat按钮样式

```css
/* src/components/editor/editor-styles.css */

.add-to-chat-button {
  display: inline-flex;
  align-items: center;
  gap: 0.25rem;
  padding: 0.375rem 0.75rem;
  font-size: 0.875rem;
  font-weight: 500;
  color: #3b82f6; /* blue-500 */
  background-color: transparent;
  border: none;
  border-radius: 0.375rem;
  cursor: pointer;
  transition: all 0.2s;
}

.add-to-chat-button:hover {
  background-color: #eff6ff; /* blue-50 */
  color: #2563eb; /* blue-600 */
}

.add-to-chat-button:active {
  transform: scale(0.95);
}

/* 分隔线样式 */
.ai-menu-separator {
  width: 1px;
  height: 1.5rem;
  background-color: #e5e7eb; /* gray-200 */
  margin: 0 0.5rem;
}
```

---

## ⌨️ 快捷键支持

### 快捷键配置

| 快捷键 | 功能 | 备注 |
|--------|------|------|
| `Ctrl/Cmd + Shift + A` | 触发Add to Chat（填充模式） | 全局快捷键 |
| `Ctrl/Cmd + Shift + S` | 触发Add to Chat（发送模式） | 可选 |

### 实现方式

```typescript
// src/components/editor/NovelEditor.tsx

import { Extension } from '@tiptap/core';

const AddToChatKeymap = Extension.create({
  name: 'addToChatKeymap',

  addKeyboardShortcuts() {
    return {
      // Ctrl/Cmd + Shift + A: 填充模式
      'Mod-Shift-a': () => {
        const { from, to } = this.editor.state.selection;
        const text = this.editor.state.doc.textBetween(from, to, ' ');

        if (text.trim()) {
          useEditorStore.getState().setAddToChatText(text, 'fill');
          return true;
        }
        return false;
      },

      // Ctrl/Cmd + Shift + S: 发送模式
      'Mod-Shift-s': () => {
        const { from, to } = this.editor.state.selection;
        const text = this.editor.state.doc.textBetween(from, to, ' ');

        if (text.trim()) {
          useEditorStore.getState().setAddToChatText(text, 'send');
          return true;
        }
        return false;
      },
    };
  },
});

// 在NovelEditor中添加扩展
const editor = useEditor({
  extensions: [
    // ... 现有扩展
    AddToChatKeymap,
  ],
});
```

---

## 🧪 测试计划

### 功能测试

| 测试场景 | 操作步骤 | 预期结果 | 优先级 |
|---------|---------|---------|--------|
| **基础功能** | 选中文本 → 点击Add to Chat | 侧边栏打开，文本填充到输入框 | P0 |
| **空文本处理** | 不选中文本 → 点击Add to Chat | 按钮禁用或无反应 | P1 |
| **长文本处理** | 选中5000字+ → 点击Add to Chat | 正常传递，无性能问题 | P1 |
| **快捷键** | 选中文本 → Ctrl+Shift+A | 同点击按钮效果 | P1 |
| **重复点击** | 连续快速点击2次Add to Chat | 不重复处理，状态正确 | P2 |
| **侧边栏已打开** | 侧边栏已打开 → Add to Chat | 直接填充，不关闭再打开 | P1 |
| **多段落文本** | 选中包含多个段落的文本 | 保留换行，正确传递 | P2 |

### 性能测试

| 测试项 | 指标 | 目标值 |
|--------|------|--------|
| **状态更新时间** | 从点击到状态更新 | < 50ms |
| **侧边栏打开时间** | 从状态更新到侧边栏显示 | < 200ms |
| **输入框填充时间** | 从侧边栏打开到输入框填充 | < 100ms |
| **总耗时** | 从点击到完成 | < 500ms |

### 边界情况测试

- ⚠️ 选中文本包含特殊字符（表情、符号）
- ⚠️ 选中文本包含HTML标签
- ⚠️ 选中文本为空格或换行
- ⚠️ 编辑器失焦状态下触发
- ⚠️ 快速切换选中区域

---

## 📊 性能优化

### 防抖处理

```typescript
// 防止用户快速连续点击
import { useDebouncedCallback } from 'use-debounce';

const handleAddToChat = useDebouncedCallback(() => {
  const { from, to } = editor.state.selection;
  const selectedText = editor.state.doc.textBetween(from, to, ' ');

  if (selectedText.trim()) {
    setAddToChatText(selectedText, 'fill');
  }
}, 300);  // 300ms防抖
```

### 长文本优化

```typescript
// 限制文本长度，避免传递过长文本
const MAX_TEXT_LENGTH = 10000;  // 最多10000字

const handleAddToChat = () => {
  let selectedText = editor.state.doc.textBetween(from, to, ' ');

  if (selectedText.length > MAX_TEXT_LENGTH) {
    // 截断并提示
    selectedText = selectedText.slice(0, MAX_TEXT_LENGTH);
    toast.warning('文本过长', `已截取前${MAX_TEXT_LENGTH}字`);
  }

  setAddToChatText(selectedText, 'fill');
};
```

---

## 🚀 实施计划

### 第一周：基础功能开发

**Day 1-2: 状态管理**
- [ ] 扩展useEditorStore
- [ ] 添加addToChatConfig状态
- [ ] 实现set/clear方法
- [ ] 单元测试

**Day 3-4: UI组件**
- [ ] 在BubbleMenu中添加按钮
- [ ] 在AIMenu中添加按钮
- [ ] 样式调整
- [ ] 图标和文案

**Day 5-7: 集成与测试**
- [ ] EditorView监听逻辑
- [ ] AgentChatPanel接收逻辑
- [ ] 快捷键支持
- [ ] 功能测试
- [ ] Bug修复

---

## ✅ 验收标准

### 功能完整性
- ✅ 用户可以通过点击按钮将选中文本发送到Agent
- ✅ 支持快捷键触发
- ✅ 侧边栏自动打开（如果未打开）
- ✅ 文本正确填充到输入框
- ✅ 清空状态后不重复处理

### 用户体验
- ✅ 响应速度 < 500ms
- ✅ 无闪烁或跳动
- ✅ 提示清晰（Toast）
- ✅ 支持长文本
- ✅ 边界情况处理得当

### 代码质量
- ✅ TypeScript类型完整
- ✅ 组件职责清晰
- ✅ 无内存泄漏
- ✅ 代码注释充分
- ✅ 符合项目规范

---

## 📝 下一步

1. ✅ **开始开发:** 按照实施计划进行开发
2. 📖 **阅读:** [03_Quick_Edit功能设计.md](./03_Quick_Edit功能设计.md)
3. 🔧 **集成:** 开发完成后集成到主分支

---

**版本:** v1.0
**日期:** 2025-01-08
**作者:** Claude & 开发团队
