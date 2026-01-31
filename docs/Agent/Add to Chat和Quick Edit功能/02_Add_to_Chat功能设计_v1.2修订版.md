# Add to Chat 功能详细设计（v1.2 修订版）

## 📋 功能概述

**Add to Chat** 是一个快速将编辑器中选中文本发送到AI助手对话框的功能，通过**引用块**的方式将选中内容作为上下文传递给AI，建立编辑器与AI助手之间的无缝连接。

> **✨ v1.2 核心改进**：
> - 选中的文字不再直接填充到输入框
> - 而是变成**引用块**显示在输入框上方
> - 输入框保持干净，用户专注输入提示词
> - 类似现代聊天工具的"引用回复"功能

### 核心价值
- 🎯 **减少操作步骤：** 从选中文本到AI处理，仅需一键
- 🔄 **上下文清晰：** 引用块清晰展示参考内容
- 💡 **灵活交互：** 用户可自由输入提示词，输入框不被占用
- ⚡ **提升效率：** 无需手动复制粘贴
- ✨ **现代体验：** 类似微信/Telegram的引用回复

### ⚠️ 重要说明：纯前端实现

**后端改动：** ❌ **无需任何后端代码改动**

本功能是**纯前端实现**，通过以下方式复用现有API：
- 使用现有的 `/api/v1/agent/chat/stream` 端点
- Agent API已经完美支持接收自定义消息
- 只需前端进行状态传递和UI交互即可

**前置条件：** ✅ **无任何前置条件，可立即开始开发**

---

## 🎨 用户交互流程

### 完整流程图

```
┌──────────────────┐
│ 1. 用户在编辑器  │
│    中选中文本     │
│  "UI简化显示逻辑"│
└────────┬─────────┘
         │
         ▼
┌──────────────────┐
│ 2. 浮动菜单出现  │  ← BubbleMenu / AIMenu
│    - Bold         │
│    - Italic       │
│    - Ask AI       │
│    - [Add to Chat]│  ← 新增按钮
│    - [Quick Edit] │
└────────┬─────────┘
         │
         ▼
┌──────────────────┐
│ 3. 点击          │
│    "Add to Chat" │
└────────┬─────────┘
         │
         ▼
┌──────────────────┐
│ 4. 自动打开      │
│    Agent侧边栏   │
│   (如果未打开)   │
└────────┬─────────┘
         │
         ▼
┌─────────────────────────────────┐
│ 5. 在Agent面板中显示：           │
│                                 │
│  ┌────────────────────────────┐│
│  │ 📎 引用: filename.md       ││ ← 引用块
│  │ ─────────────────────────  ││
│  │ UI简化显示逻辑 (20分钟)    ││
│  │                  [× 移除]  ││
│  └────────────────────────────┘│
│                                 │
│  ┌────────────────────────────┐│
│  │ 在这里输入你的问题...       ││ ← 输入框（干净）
│  │ █                          ││
│  └────────────────────────────┘│
│  [发送]                         │
└─────────────────────────────────┘
         │
         ▼
┌──────────────────┐
│ 6. 用户输入      │
│    提示词:        │
│   "这个任务要    │
│    怎么实现？"   │
└────────┬─────────┘
         │
         ▼
┌──────────────────┐
│ 7. 发送给AI:     │
│                  │
│ 参考内容:        │
│ UI简化显示逻辑   │
│                  │
│ 用户问题:        │
│ 这个任务要怎么   │
│ 实现？           │
└──────────────────┘
```

---

## 🎨 UI设计详解

### 引用块展示效果

```
┌──────────────────────────────────────────┐
│  🤖 AI 助手                    [×]       │
├──────────────────────────────────────────┤
│                                          │
│  （之前的对话历史）                       │
│                                          │
├──────────────────────────────────────────┤
│  新消息输入区域：                         │
│                                          │
│  ┌────────────────────────────────────┐ │
│  │ 📎 引用自: REACT_VERIFICATION...   │ │ ← 引用块头部
│  │ ────────────────────────────────  │ │
│  │ UI简化显示逻辑 (20分钟)            │ │ ← 引用内容
│  │                                    │ │
│  │                      [× 移除引用]  │ │ ← 移除按钮
│  └────────────────────────────────────┘ │
│                                          │
│  ┌────────────────────────────────────┐ │
│  │ 在这里输入你的问题...               │ │ ← 输入框（空白）
│  │                                    │ │
│  │                                    │ │
│  └────────────────────────────────────┘ │
│  [发送] [清空]              Ctrl+Enter  │
└──────────────────────────────────────────┘
```

### 引用块的组成部分

```typescript
┌──────────────────────────────────────┐
│ 📎 引用自: filename.md        [×]    │ ← Header（来源文件 + 移除按钮）
│ ──────────────────────────────────── │ ← 分隔线
│ 选中的文本内容                        │ ← Content（引用的文字）
│ 可能有多行...                        │
│                                      │
│ 字数: 128字                          │ ← Footer（元信息，可选）
└──────────────────────────────────────┘
```

---

## 💾 数据结构设计

### Reference类型定义

```typescript
// src/types/agent.ts

/**
 * 引用（Reference）- 从编辑器传递到AI助手的上下文
 */
export interface Reference {
  /** 引用内容 */
  content: string;

  /** 来源文件名 */
  source?: string;

  /** 创建时间戳 */
  timestamp: number;

  /** 唯一ID（用于删除） */
  id: string;
}

/**
 * Add to Chat 配置
 */
export interface AddToChatConfig {
  /** 引用对象 */
  reference: Reference;

  /** 创建时间戳（用于防止重复处理） */
  timestamp: number;
}
```

### Zustand Store扩展

```typescript
// src/store/editorStore.ts

import { create } from 'zustand';
import type { Reference, AddToChatConfig } from '@/types/agent';

interface EditorStore {
  // ... 现有状态

  // ✨ Add to Chat状态
  addToChatConfig: AddToChatConfig | null;

  // ✨ 设置Add to Chat配置
  setAddToChatReference: (text: string, source?: string) => void;

  // ✨ 清除Add to Chat状态
  clearAddToChatConfig: () => void;
}

export const useEditorStore = create<EditorStore>((set) => ({
  // ... 现有实现

  addToChatConfig: null,

  setAddToChatReference: (text, source) => {
    const reference: Reference = {
      id: `ref_${Date.now()}_${Math.random().toString(36).substr(2, 9)}`,
      content: text,
      source: source || '未命名文档',
      timestamp: Date.now(),
    };

    set({
      addToChatConfig: {
        reference,
        timestamp: Date.now(),
      },
    });
  },

  clearAddToChatConfig: () => {
    set({ addToChatConfig: null });
  },
}));
```

---

## 🔧 组件实现详情

### 1. BubbleMenu扩展

**文件:** `src/components/editor/BubbleMenu.tsx`

```typescript
import { MessageSquarePlus } from 'lucide-react';
import { useEditorStore } from '@/store/editorStore';

const BubbleMenu: React.FC<BubbleMenuProps> = ({ editor }) => {
  const setAddToChatReference = useEditorStore(state => state.setAddToChatReference);

  const handleAddToChat = () => {
    const { from, to } = editor.state.selection;
    const selectedText = editor.state.doc.textBetween(from, to, ' ');

    if (selectedText.trim()) {
      // 获取当前文件名（如果可用）
      const currentFileName = getCurrentFileName(); // 实现获取文件名的逻辑

      setAddToChatReference(selectedText, currentFileName);
    }
  };

  return (
    <TiptapBubbleMenu editor={editor} className="bubble-menu-container">
      {/* Add to Chat 按钮 */}
      <button
        onClick={handleAddToChat}
        className="bubble-menu-button add-to-chat-button"
        title="Add to Chat (Ctrl+Shift+A)"
        type="button"
      >
        <MessageSquarePlus className="w-4 h-4 text-blue-500" />
        <span className="ml-1 text-sm text-blue-500 font-medium">Add to Chat</span>
      </button>

      {/* 其他按钮... */}
    </TiptapBubbleMenu>
  );
};
```

---

### 2. ReferenceBlock组件（新增）

**文件:** `src/components/agent/ReferenceBlock.tsx`

```typescript
import React from 'react';
import { X, FileText } from 'lucide-react';
import type { Reference } from '@/types/agent';

interface ReferenceBlockProps {
  reference: Reference;
  onRemove: () => void;
}

export const ReferenceBlock: React.FC<ReferenceBlockProps> = ({
  reference,
  onRemove,
}) => {
  // 限制显示长度
  const displayContent = reference.content.length > 200
    ? reference.content.slice(0, 200) + '...'
    : reference.content;

  return (
    <div className="reference-block">
      {/* Header */}
      <div className="reference-header">
        <div className="reference-source">
          <FileText className="w-4 h-4 text-gray-500" />
          <span className="text-sm text-gray-600">引用自: {reference.source}</span>
        </div>
        <button
          onClick={onRemove}
          className="reference-remove-btn"
          title="移除引用"
          type="button"
        >
          <X className="w-4 h-4" />
        </button>
      </div>

      {/* Divider */}
      <div className="reference-divider" />

      {/* Content */}
      <div className="reference-content">
        <p className="text-sm text-gray-700 whitespace-pre-wrap">
          {displayContent}
        </p>
      </div>

      {/* Footer (optional) */}
      {reference.content.length > 200 && (
        <div className="reference-footer">
          <span className="text-xs text-gray-500">
            {reference.content.length} 字 （已截取前200字）
          </span>
        </div>
      )}
    </div>
  );
};
```

**样式：** `src/components/agent/ReferenceBlock.module.css`

```css
.reference-block {
  background-color: #f8fafc; /* slate-50 */
  border: 1px solid #e2e8f0; /* slate-200 */
  border-radius: 0.5rem;
  padding: 0.75rem;
  margin-bottom: 0.75rem;
}

.reference-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 0.5rem;
}

.reference-source {
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.reference-remove-btn {
  padding: 0.25rem;
  color: #64748b; /* slate-500 */
  background: transparent;
  border: none;
  border-radius: 0.25rem;
  cursor: pointer;
  transition: all 0.2s;
}

.reference-remove-btn:hover {
  background-color: #f1f5f9; /* slate-100 */
  color: #ef4444; /* red-500 */
}

.reference-divider {
  height: 1px;
  background-color: #e2e8f0; /* slate-200 */
  margin-bottom: 0.5rem;
}

.reference-content {
  max-height: 8rem;
  overflow-y: auto;
  padding: 0.5rem;
  background-color: white;
  border-radius: 0.375rem;
}

.reference-footer {
  margin-top: 0.5rem;
  text-align: right;
}
```

---

### 3. AgentChatPanel集成引用块

**文件:** `src/components/agent/AgentChatPanel.tsx`

```typescript
import React, { useState, useEffect } from 'react';
import { useAgentChat } from '@/hooks/useAgentChat';
import { useEditorStore } from '@/store/editorStore';
import { ReferenceBlock } from './ReferenceBlock';
import type { Reference } from '@/types/agent';

export default function AgentChatPanel({ workId, chapterId, className = '' }) {
  const { sendMessageStream, isLoading } = useAgentChat();
  const [inputValue, setInputValue] = useState('');

  // ✨ 当前引用（可能有多个，支持扩展）
  const [currentReference, setCurrentReference] = useState<Reference | null>(null);

  // ✨ 监听Add to Chat状态
  const addToChatConfig = useEditorStore(state => state.addToChatConfig);
  const clearAddToChatConfig = useEditorStore(state => state.clearAddToChatConfig);

  // ✨ 处理Add to Chat
  useEffect(() => {
    if (addToChatConfig) {
      const { reference } = addToChatConfig;

      console.log('[AgentChatPanel] 收到引用:', {
        source: reference.source,
        contentLength: reference.content.length,
      });

      // 设置引用
      setCurrentReference(reference);

      // 聚焦到输入框
      setTimeout(() => {
        const input = document.querySelector('.chat-input') as HTMLInputElement;
        input?.focus();
      }, 100);

      // 清除状态（避免重复处理）
      clearAddToChatConfig();
    }
  }, [addToChatConfig, clearAddToChatConfig]);

  // ✨ 移除引用
  const handleRemoveReference = () => {
    setCurrentReference(null);
  };

  // ✨ 发送消息
  const handleSendMessage = async () => {
    if (!inputValue.trim()) {
      return;
    }

    // 构建完整消息
    let message = inputValue;

    if (currentReference) {
      // 将引用内容作为上下文
      message = `参考内容：
${currentReference.content}

用户问题：
${inputValue}`;
    }

    const request = {
      message,
      work_id: workId,
      chapter_id: chapterId,
    };

    await sendMessageStream(request);

    // 发送后清空输入框和引用
    setInputValue('');
    setCurrentReference(null);
  };

  return (
    <div className={`agent-chat-panel ${className}`}>
      {/* 消息列表 */}
      <div className="messages">
        {messages.map((msg, index) => (
          <AgentMessage key={index} message={msg} />
        ))}
      </div>

      {/* 输入区域 */}
      <div className="chat-input-container">
        {/* ✨ 引用块（如果存在） */}
        {currentReference && (
          <ReferenceBlock
            reference={currentReference}
            onRemove={handleRemoveReference}
          />
        )}

        {/* 输入框 */}
        <ChatInput
          value={inputValue}
          onChange={setInputValue}
          onSend={handleSendMessage}
          disabled={isLoading}
          placeholder={
            currentReference
              ? '输入你的问题...'
              : '输入消息或提示词...'
          }
        />
      </div>
    </div>
  );
}
```

---

## ⌨️ 快捷键支持

### 快捷键配置

| 快捷键 | 功能 | 备注 |
|--------|------|------|
| `Ctrl/Cmd + Shift + A` | 将选中文字添加为引用 | 全局快捷键 |
| `Esc` | 移除当前引用 | 在输入框聚焦时 |

### 实现方式

```typescript
// src/components/editor/NovelEditor.tsx

import { Extension } from '@tiptap/core';
import { useEditorStore } from '@/store/editorStore';

const AddToChatKeymap = Extension.create({
  name: 'addToChatKeymap',

  addKeyboardShortcuts() {
    return {
      // Ctrl/Cmd + Shift + A: 添加引用
      'Mod-Shift-a': () => {
        const { from, to } = this.editor.state.selection;
        const text = this.editor.state.doc.textBetween(from, to, ' ');

        if (text.trim()) {
          const fileName = getCurrentFileName(); // 实现获取文件名
          useEditorStore.getState().setAddToChatReference(text, fileName);
          return true;
        }
        return false;
      },
    };
  },
});
```

---

## 🧪 测试计划

### 功能测试

| 测试场景 | 操作步骤 | 预期结果 | 优先级 |
|---------|---------|---------|--------|
| **基础功能** | 选中文本 → 点击Add to Chat | 侧边栏打开，显示引用块，输入框空白 | P0 |
| **引用显示** | 添加引用 | 引用块正确显示文件名和内容 | P0 |
| **移除引用** | 点击引用块的[×]按钮 | 引用块消失 | P0 |
| **发送消息** | 有引用时发送消息 | 引用内容作为上下文一起发送 | P0 |
| **长文本引用** | 选中5000字+ | 引用块正确截断显示，完整内容正确发送 | P1 |
| **快捷键** | Ctrl+Shift+A | 同点击按钮效果 | P1 |
| **空文本** | 不选中文本 → Add to Chat | 无反应或提示 | P1 |

---

## 📊 与v1.0/v1.1的对比

### 主要改进

| 对比项 | v1.0/v1.1（旧） | v1.2（新） |
|-------|---------------|----------|
| **文字去向** | 直接填充到输入框 | 显示为引用块 |
| **输入框状态** | 被选中文字占用 | 保持干净 |
| **用户体验** | 需要手动删除或编辑选中文字 | 直接输入提示词 |
| **上下文展示** | 不明显 | 引用块清晰展示 |
| **现代感** | 一般 | 类似主流聊天工具 |

### 数据结构变化

```typescript
// v1.0/v1.1（旧）
interface AddToChatConfig {
  text: string;
  mode: 'fill' | 'send';
  timestamp: number;
}

// v1.2（新）
interface AddToChatConfig {
  reference: Reference;  // ✨ 改为引用对象
  timestamp: number;
}

interface Reference {
  id: string;
  content: string;
  source?: string;
  timestamp: number;
}
```

---

## ✅ 验收标准

### 功能完整性
- ✅ 选中文字后点击Add to Chat，引用块正确显示
- ✅ 引用块包含文件名、内容、移除按钮
- ✅ 输入框保持空白状态
- ✅ 可以移除引用
- ✅ 发送消息时，引用内容作为上下文一起发送
- ✅ 发送后自动清空引用和输入框

### 用户体验
- ✅ 响应速度 < 500ms
- ✅ 引用块样式美观
- ✅ 长文本自动截断显示
- ✅ 支持快捷键
- ✅ 提示清晰

---

## 📝 版本记录

| 版本 | 日期 | 主要变更 |
|------|------|---------|
| v1.0 | 2025-01-08 | 初始版本（填充输入框模式） |
| v1.2 | 2025-01-10 | **引用块模式**（重大改进） |

---

## 🚀 下一步

1. ✅ **开始开发:** 按照v1.2设计实现引用块功能
2. 📖 **参考:** 现代聊天工具（微信、Telegram）的引用回复功能
3. 🔧 **集成:** 开发完成后集成到主分支

---

**版本:** v1.2
**日期:** 2025-01-10
**作者:** Claude & 开发团队
