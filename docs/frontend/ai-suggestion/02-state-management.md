# Phase 1: 状态管理系统

## 📋 任务清单

- [ ] 1.1 创建AIPendingMark扩展（Tiptap Mark）
- [ ] 1.2 创建useAISuggestion Hook（管理建议生命周期）
- [ ] 1.3 添加待确认内容的CSS样式（黄色高亮+虚线边框+脉动动画）

## 🎯 目标

构建AI建议的状态管理核心，包括：
1. Tiptap Mark扩展用于标记待确认内容
2. React Hook管理建议生命周期
3. CSS样式突出显示待确认内容

---

## 📝 Task 1.1: 创建AIPendingMark扩展

### 文件路径
```
src/components/editor/extensions/AIPendingMark.ts
```

### 实现代码

```typescript
/**
 * AIPendingMark - AI生成内容的待确认标记扩展
 * 用于在编辑器中标识待用户确认的AI生成内容
 */
import { Mark } from '@tiptap/core';

export interface AIPendingAttributes {
  suggestionId: string;
}

export const AIPendingMark = Mark.create({
  name: 'aiPending',

  // 定义Mark的属性
  addAttributes() {
    return {
      suggestionId: {
        default: null,
        parseHTML: (element) => element.getAttribute('data-suggestion-id'),
        renderHTML: (attributes) => {
          if (!attributes.suggestionId) {
            return {};
          }
          return {
            'data-suggestion-id': attributes.suggestionId,
          };
        },
      },
    };
  },

  // HTML解析规则
  parseHTML() {
    return [
      {
        tag: 'span[data-ai-pending]',
        getAttrs: (element) => {
          const suggestionId = (element as HTMLElement).getAttribute('data-suggestion-id');
          return suggestionId ? { suggestionId } : false;
        },
      },
    ];
  },

  // HTML渲染规则
  renderHTML({ HTMLAttributes }) {
    return [
      'span',
      {
        ...HTMLAttributes,
        'data-ai-pending': 'true',
        class: 'ai-pending-content',
      },
      0, // 内容插槽
    ];
  },

  // 定义为inclusive mark（会包含新输入的内容）
  // 设为false，避免用户输入时自动应用该mark
  addOptions() {
    return {
      ...this.parent?.(),
      inclusive: false,
    };
  },
});
```

### 类型定义

```typescript
// src/types/ai-suggestion.ts
export interface AISuggestion {
  id: string;                    // 建议唯一ID
  content: string;               // 生成的内容
  startPos: number;              // 起始位置
  endPos: number;                // 结束位置
  status: 'pending' | 'accepted' | 'rejected';  // 状态
  createdAt: number;             // 创建时间戳
}
```

### 测试用例

```typescript
// src/components/editor/extensions/__tests__/AIPendingMark.test.ts
import { describe, it, expect } from 'vitest';
import { createEditor } from '@tiptap/react';
import StarterKit from '@tiptap/starter-kit';
import { AIPendingMark } from '../AIPendingMark';

describe('AIPendingMark', () => {
  it('应该正确渲染带标记的内容', () => {
    const editor = createEditor({
      extensions: [StarterKit, AIPendingMark],
      content: '<p>测试内容</p>',
    });

    editor.commands.setTextSelection({ from: 1, to: 5 });
    editor.commands.setMark('aiPending', { suggestionId: 'test-123' });

    const html = editor.getHTML();
    expect(html).toContain('data-ai-pending="true"');
    expect(html).toContain('data-suggestion-id="test-123"');
  });

  it('应该正确解析HTML中的pending标记', () => {
    const html = '<p><span data-ai-pending="true" data-suggestion-id="test-456">测试</span></p>';

    const editor = createEditor({
      extensions: [StarterKit, AIPendingMark],
      content: html,
    });

    const json = editor.getJSON();
    expect(json.content[0].content[0].marks[0]).toMatchObject({
      type: 'aiPending',
      attrs: { suggestionId: 'test-456' },
    });
  });
});
```

---

## 📝 Task 1.2: 创建useAISuggestion Hook

### 文件路径
```
src/hooks/useAISuggestion.ts
```

### 实现代码

```typescript
/**
 * useAISuggestion - AI建议状态管理Hook
 * 负责管理AI建议的完整生命周期
 */
import { useState, useCallback, useRef } from 'react';
import { Editor } from '@tiptap/react';
import type { AISuggestion } from '@/types/ai-suggestion';

export interface UseAISuggestionReturn {
  currentSuggestion: AISuggestion | null;
  isGenerating: boolean;
  startSuggestion: (insertPosition?: number) => string;
  streamInsert: (chunk: string) => void;
  acceptSuggestion: () => void;
  rejectSuggestion: () => void;
  getSuggestionById: (id: string) => AISuggestion | undefined;
}

export const useAISuggestion = (editor: Editor | null): UseAISuggestionReturn => {
  const [currentSuggestion, setCurrentSuggestion] = useState<AISuggestion | null>(null);
  const [isGenerating, setIsGenerating] = useState(false);
  const historyRef = useRef<Map<string, AISuggestion>>(new Map());

  // 历史记录最大数量（防止内存泄漏）
  const MAX_HISTORY = 50;

  /**
   * 添加到历史记录（自动清理）
   */
  const addToHistory = useCallback((suggestion: AISuggestion) => {
    historyRef.current.set(suggestion.id, suggestion);

    // 超过最大数量时，删除最旧的记录
    if (historyRef.current.size > MAX_HISTORY) {
      const firstKey = historyRef.current.keys().next().value;
      if (firstKey) {
        historyRef.current.delete(firstKey);
        console.log('[useAISuggestion] 清理旧记录:', firstKey);
      }
    }
  }, []);

  /**
   * 开始新的建议
   * @param insertPosition 插入位置，不传则使用光标位置
   * @returns 建议ID
   */
  const startSuggestion = useCallback((insertPosition?: number) => {
    // 1. 检查编辑器是否初始化
    if (!editor) {
      console.error('[useAISuggestion] Editor未初始化');
      throw new Error('Editor not initialized');
    }

    // 2. 检查是否已有进行中的建议（防止并发）
    if (currentSuggestion && isGenerating) {
      console.warn('[useAISuggestion] 已有进行中的建议，返回现有ID');
      return currentSuggestion.id;
    }

    // 3. 创建新建议
    const suggestionId = `suggestion-${Date.now()}`;
    const startPos = insertPosition ?? editor.state.selection.to;

    const newSuggestion: AISuggestion = {
      id: suggestionId,
      content: '',
      startPos,
      endPos: startPos,
      status: 'pending',
      createdAt: Date.now(),
    };

    // 4. 更新状态
    setCurrentSuggestion(newSuggestion);
    setIsGenerating(true);
    historyRef.current.set(suggestionId, newSuggestion);

    console.log('[useAISuggestion] 开始新建议:', suggestionId);
    return suggestionId;
  }, [editor, currentSuggestion, isGenerating]);

  /**
   * 流式插入内容
   * @param chunk 内容片段
   */
  const streamInsert = useCallback((chunk: string) => {
    if (!editor || !currentSuggestion) {
      console.warn('[useAISuggestion] 无法插入：editor或suggestion未初始化');
      return;
    }

    // 插入内容并应用pending标记
    editor
      .chain()
      .focus()
      .insertContentAt(currentSuggestion.endPos, {
        type: 'text',
        text: chunk,
        marks: [
          {
            type: 'aiPending',
            attrs: { suggestionId: currentSuggestion.id },
          },
        ],
      })
      .run();

    // 更新建议状态
    const updatedSuggestion = {
      ...currentSuggestion,
      content: currentSuggestion.content + chunk,
      endPos: currentSuggestion.endPos + chunk.length,
    };

    setCurrentSuggestion(updatedSuggestion);
    historyRef.current.set(currentSuggestion.id, updatedSuggestion);
  }, [editor, currentSuggestion]);

  /**
   * 接受建议（移除pending标记，保留内容）
   */
  const acceptSuggestion = useCallback(() => {
    if (!editor || !currentSuggestion) {
      console.warn('[useAISuggestion] 无法接受：editor或suggestion未初始化');
      return;
    }

    const { doc, tr } = editor.state;
    const { startPos, endPos, id } = currentSuggestion;

    // 遍历文档，找到所有匹配的pending标记并移除
    doc.nodesBetween(startPos, endPos, (node, pos) => {
      if (node.isText) {
        const mark = node.marks.find(
          (m) => m.type.name === 'aiPending' && m.attrs.suggestionId === id
        );
        if (mark) {
          const from = pos;
          const to = pos + node.nodeSize;
          tr.removeMark(from, to, mark);
        }
      }
    });

    // 应用事务
    editor.view.dispatch(tr);

    // 更新状态
    const acceptedSuggestion = { ...currentSuggestion, status: 'accepted' as const };
    historyRef.current.set(id, acceptedSuggestion);
    setCurrentSuggestion(null);
    setIsGenerating(false);

    console.log('[useAISuggestion] 已接受建议:', id);
  }, [editor, currentSuggestion]);

  /**
   * 拒绝建议（删除内容和标记）
   */
  const rejectSuggestion = useCallback(() => {
    if (!editor || !currentSuggestion) {
      console.warn('[useAISuggestion] 无法拒绝：editor或suggestion未初始化');
      return;
    }

    const { startPos, endPos, id } = currentSuggestion;

    // 删除整个范围的内容
    editor
      .chain()
      .focus()
      .deleteRange({ from: startPos, to: endPos })
      .run();

    // 更新状态
    const rejectedSuggestion = { ...currentSuggestion, status: 'rejected' as const };
    historyRef.current.set(id, rejectedSuggestion);
    setCurrentSuggestion(null);
    setIsGenerating(false);

    console.log('[useAISuggestion] 已拒绝建议:', id);
  }, [editor, currentSuggestion]);

  /**
   * 根据ID获取建议
   */
  const getSuggestionById = useCallback((id: string) => {
    return historyRef.current.get(id);
  }, []);

  return {
    currentSuggestion,
    isGenerating,
    startSuggestion,
    streamInsert,
    acceptSuggestion,
    rejectSuggestion,
    getSuggestionById,
  };
};
```

### 使用示例

```typescript
// 在EditorView中使用
const MyEditor = () => {
  const [editor, setEditor] = useState<Editor | null>(null);
  const aiSuggestion = useAISuggestion(editor);

  const handleGenerate = async () => {
    // 1. 开始建议
    const suggestionId = aiSuggestion.startSuggestion();

    // 2. 模拟流式插入
    const text = "这是AI生成的内容...";
    for (const char of text) {
      aiSuggestion.streamInsert(char);
      await new Promise(resolve => setTimeout(resolve, 50));
    }
  };

  return (
    <div>
      <button onClick={handleGenerate}>生成</button>
      {aiSuggestion.currentSuggestion && (
        <>
          <button onClick={aiSuggestion.acceptSuggestion}>✓</button>
          <button onClick={aiSuggestion.rejectSuggestion}>✗</button>
        </>
      )}
    </div>
  );
};
```

---

## 📝 Task 1.3: 添加CSS样式

### 文件路径
```
src/components/editor/ai-suggestion-styles.css
```

### 实现代码

```css
/**
 * AI建议待确认内容样式
 */

/* 基础样式 */
.ai-pending-content {
  /* 黄色渐变背景 */
  background: linear-gradient(
    90deg,
    rgba(255, 235, 59, 0.2) 0%,
    rgba(255, 235, 59, 0.1) 100%
  );

  /* 虚线边框 */
  border: 2px dashed #FFD700;
  border-radius: 4px;

  /* 内边距 */
  padding: 4px 6px;
  margin: 0 2px;

  /* 脉动动画 */
  animation: ai-pending-pulse 2s ease-in-out infinite;

  /* 过渡效果 */
  transition: all 0.3s ease;
}

/* 悬停效果 */
.ai-pending-content:hover {
  background: rgba(255, 235, 59, 0.3);
  border-color: #FFC107;
}

/* 脉动动画 */
@keyframes ai-pending-pulse {
  0%, 100% {
    opacity: 1;
    box-shadow: 0 0 0 rgba(255, 215, 0, 0.4);
  }
  50% {
    opacity: 0.85;
    box-shadow: 0 0 8px rgba(255, 215, 0, 0.6);
  }
}

/* 深色模式适配 */
@media (prefers-color-scheme: dark) {
  .ai-pending-content {
    background: linear-gradient(
      90deg,
      rgba(255, 235, 59, 0.15) 0%,
      rgba(255, 235, 59, 0.08) 100%
    );
    border-color: #F9A825;
  }

  .ai-pending-content:hover {
    background: rgba(255, 235, 59, 0.25);
    border-color: #FFD700;
  }
}

/* 打印时隐藏边框 */
@media print {
  .ai-pending-content {
    border: none;
    background: none;
    padding: 0;
    margin: 0;
  }
}

/* 禁用状态 */
.ai-pending-content[data-disabled="true"] {
  opacity: 0.5;
  pointer-events: none;
  animation: none;
}
```

### 在NovelEditor中引入

```typescript
// src/components/editor/NovelEditor.tsx
import './ai-suggestion-styles.css';
```

---

## ✅ 验收标准

### 1.1 AIPendingMark扩展
- [ ] Mark能够正确应用到文本
- [ ] HTML渲染包含 `data-ai-pending="true"` 属性
- [ ] suggestionId属性正确传递
- [ ] 不影响其他编辑器功能

### 1.2 useAISuggestion Hook
- [ ] `startSuggestion()` 返回有效的ID
- [ ] `streamInsert()` 能够逐步插入内容
- [ ] `acceptSuggestion()` 正确移除标记
- [ ] `rejectSuggestion()` 正确删除内容
- [ ] 状态管理无内存泄漏

### 1.3 CSS样式
- [ ] 待确认内容有明显的黄色背景
- [ ] 虚线边框清晰可见
- [ ] 脉动动画流畅自然
- [ ] 深色模式显示正常
- [ ] 打印时样式正确

---

## 🐛 常见问题

### Q1: Mark标记没有生效？
**A**: 检查是否正确注册了AIPendingMark扩展：
```typescript
const editor = useEditor({
  extensions: [
    // ...其他扩展
    AIPendingMark,
  ],
});
```

### Q2: 流式插入卡顿？
**A**: 使用requestAnimationFrame批处理：
```typescript
let pendingChunks: string[] = [];
let rafId: number | null = null;

const streamInsert = (chunk: string) => {
  pendingChunks.push(chunk);

  if (!rafId) {
    rafId = requestAnimationFrame(() => {
      const combined = pendingChunks.join('');
      pendingChunks = [];
      rafId = null;
      // 实际插入逻辑
    });
  }
};
```

### Q3: 删除建议后编辑器光标位置不对？
**A**: 在删除后重新设置光标：
```typescript
editor.commands.deleteRange({ from: startPos, to: endPos });
editor.commands.setTextSelection(startPos);
```

---

## 📚 相关文档

- [架构设计](./01-architecture.md)
- [Agent卡片UI](./03-agent-card.md)
- [API参考](./api-reference.md)
