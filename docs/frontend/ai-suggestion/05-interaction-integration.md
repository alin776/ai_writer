# Phase 4 & 5: 交互实现与集成测试

## 📋 任务清单

### Phase 4: ✓/✗交互
- [ ] 4.1 实现acceptSuggestion（移除pending标记，保留内容）
- [ ] 4.2 实现rejectSuggestion（删除编辑器内容+标记）
- [ ] 4.3 添加状态同步（卡片✓/✗ ↔ 编辑器内容变化）

### Phase 5: 集成测试
- [ ] 5.1 创建EditorContext共享编辑器实例和AI状态
- [ ] 5.2 修改AIPanel集成新的卡片组件
- [ ] 5.3 测试完整交互流程（生成→展示→✓/✗）

---

## 📝 Phase 4.1: 实现acceptSuggestion

### 实现逻辑

```typescript
// src/hooks/useAISuggestion.ts

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

  console.log('[useAISuggestion] 开始接受建议:', {
    id,
    startPos,
    endPos,
    content: currentSuggestion.content,
  });

  // 遍历建议范围内的所有节点
  doc.nodesBetween(startPos, endPos, (node, pos) => {
    if (!node.isText) return;

    // 查找匹配的pending标记
    const pendingMark = node.marks.find(
      (m) => m.type.name === 'aiPending' && m.attrs.suggestionId === id
    );

    if (pendingMark) {
      const from = pos;
      const to = pos + node.nodeSize;

      // 移除pending标记
      tr.removeMark(from, to, pendingMark);

      console.log('[useAISuggestion] 移除标记:', { from, to });
    }
  });

  // 应用事务
  if (tr.steps.length > 0) {
    editor.view.dispatch(tr);
  }

  // 更新状态
  const acceptedSuggestion: AISuggestion = {
    ...currentSuggestion,
    status: 'accepted',
  };

  historyRef.current.set(id, acceptedSuggestion);
  setCurrentSuggestion(null);
  setIsGenerating(false);

  console.log('[useAISuggestion] ✅ 建议已接受:', id);

  // 触发回调
  onAcceptCallback?.(acceptedSuggestion);
}, [editor, currentSuggestion, onAcceptCallback]);
```

### 优化版本：带动画效果

```typescript
const acceptSuggestion = useCallback(async () => {
  if (!editor || !currentSuggestion) return;

  // 1. 添加"接受中"动画
  const suggestionElements = document.querySelectorAll(
    `[data-suggestion-id="${currentSuggestion.id}"]`
  );

  suggestionElements.forEach((el) => {
    el.classList.add('ai-pending-accepting');
  });

  // 2. 等待动画完成
  await new Promise((resolve) => setTimeout(resolve, 300));

  // 3. 移除pending标记
  const { doc, tr } = editor.state;
  const { startPos, endPos, id } = currentSuggestion;

  doc.nodesBetween(startPos, endPos, (node, pos) => {
    if (node.isText) {
      const mark = node.marks.find(
        (m) => m.type.name === 'aiPending' && m.attrs.suggestionId === id
      );
      if (mark) {
        tr.removeMark(pos, pos + node.nodeSize, mark);
      }
    }
  });

  editor.view.dispatch(tr);

  // 4. 更新状态
  const acceptedSuggestion = { ...currentSuggestion, status: 'accepted' as const };
  historyRef.current.set(id, acceptedSuggestion);
  setCurrentSuggestion(null);
  setIsGenerating(false);

  // 5. 触发回调
  onAcceptCallback?.(acceptedSuggestion);
}, [editor, currentSuggestion, onAcceptCallback]);
```

### 接受动画CSS

```css
/* src/components/editor/ai-suggestion-styles.css */

/* 接受中动画 */
.ai-pending-accepting {
  animation: accept-flash 0.3s ease-out;
}

@keyframes accept-flash {
  0% {
    background: rgba(16, 185, 129, 0.3);
    border-color: #10b981;
  }
  100% {
    background: transparent;
    border-color: transparent;
  }
}
```

---

## 📝 Phase 4.2: 实现rejectSuggestion

### 实现逻辑

```typescript
/**
 * 拒绝建议（删除编辑器内容+标记）
 */
const rejectSuggestion = useCallback(async () => {
  if (!editor || !currentSuggestion) {
    console.warn('[useAISuggestion] 无法拒绝：editor或suggestion未初始化');
    return;
  }

  const { startPos, endPos, id } = currentSuggestion;

  console.log('[useAISuggestion] 开始拒绝建议:', {
    id,
    startPos,
    endPos,
  });

  // 1. 添加"拒绝中"动画
  const suggestionElements = document.querySelectorAll(
    `[data-suggestion-id="${id}"]`
  );

  suggestionElements.forEach((el) => {
    el.classList.add('ai-pending-rejecting');
  });

  // 2. 等待动画完成
  await new Promise((resolve) => setTimeout(resolve, 300));

  // 3. 删除内容范围
  editor
    .chain()
    .focus()
    .deleteRange({ from: startPos, to: endPos })
    .run();

  // 4. 更新状态
  const rejectedSuggestion: AISuggestion = {
    ...currentSuggestion,
    status: 'rejected',
  };

  historyRef.current.set(id, rejectedSuggestion);
  setCurrentSuggestion(null);
  setIsGenerating(false);

  console.log('[useAISuggestion] ❌ 建议已拒绝:', id);

  // 5. 触发回调
  onRejectCallback?.(rejectedSuggestion);
}, [editor, currentSuggestion, onRejectCallback]);
```

### 拒绝动画CSS

```css
/* 拒绝中动画 */
.ai-pending-rejecting {
  animation: reject-fade 0.3s ease-out forwards;
}

@keyframes reject-fade {
  0% {
    opacity: 1;
    background: rgba(239, 68, 68, 0.2);
    border-color: #ef4444;
    transform: scale(1);
  }
  100% {
    opacity: 0;
    background: rgba(239, 68, 68, 0);
    border-color: transparent;
    transform: scale(0.95);
  }
}
```

---

## 📝 Phase 4.3: 状态同步

### 实现双向绑定

```typescript
// src/views/EditorView/EditorContext.tsx

import React, { createContext, useState, useCallback } from 'react';
import { Editor } from '@tiptap/react';
import { useAISuggestion } from '@/hooks/useAISuggestion';

export interface EditorContextValue {
  editor: Editor | null;
  aiSuggestion: ReturnType<typeof useAISuggestion>;
  setEditor: (editor: Editor | null) => void;
}

export const EditorContext = createContext<EditorContextValue | null>(null);

export const EditorProvider: React.FC<{ children: React.ReactNode }> = ({ children }) => {
  const [editor, setEditor] = useState<Editor | null>(null);

  // 创建AI建议Hook（带回调）
  const aiSuggestion = useAISuggestion(editor, {
    onAccept: (suggestion) => {
      console.log('[EditorContext] 建议已接受:', suggestion.id);
      // 可以在这里触发其他副作用
      // 例如：保存到服务器、更新统计等
    },
    onReject: (suggestion) => {
      console.log('[EditorContext] 建议已拒绝:', suggestion.id);
    },
  });

  const contextValue: EditorContextValue = {
    editor,
    aiSuggestion,
    setEditor,
  };

  return (
    <EditorContext.Provider value={contextValue}>
      {children}
    </EditorContext.Provider>
  );
};
```

### 修改useAISuggestion支持回调

```typescript
// src/hooks/useAISuggestion.ts

export interface UseAISuggestionOptions {
  onAccept?: (suggestion: AISuggestion) => void;
  onReject?: (suggestion: AISuggestion) => void;
  onStart?: (suggestionId: string) => void;
}

export const useAISuggestion = (
  editor: Editor | null,
  options?: UseAISuggestionOptions
) => {
  // ... 其他代码

  const acceptSuggestion = useCallback(async () => {
    // ... 接受逻辑

    // 触发回调
    options?.onAccept?.(acceptedSuggestion);
  }, [editor, currentSuggestion, options]);

  const rejectSuggestion = useCallback(async () => {
    // ... 拒绝逻辑

    // 触发回调
    options?.onReject?.(rejectedSuggestion);
  }, [editor, currentSuggestion, options]);

  // ... 返回值
};
```

---

## 📝 Phase 5.1: 创建EditorContext

### 完整Context实现

```typescript
// src/views/EditorView/EditorContext.tsx

import React, { createContext, useState, useCallback, useContext } from 'react';
import { Editor } from '@tiptap/react';
import { useAISuggestion } from '@/hooks/useAISuggestion';
import { useToast } from '@/hooks/useToast';
import type { AISuggestion } from '@/types/ai-suggestion';

export interface EditorContextValue {
  editor: Editor | null;
  aiSuggestion: ReturnType<typeof useAISuggestion>;
  setEditor: (editor: Editor | null) => void;
}

export const EditorContext = createContext<EditorContextValue | null>(null);

export const EditorProvider: React.FC<{ children: React.ReactNode }> = ({ children }) => {
  const [editor, setEditor] = useState<Editor | null>(null);
  const toast = useToast();

  const aiSuggestion = useAISuggestion(editor, {
    onAccept: (suggestion: AISuggestion) => {
      console.log('[EditorContext] ✅ 建议已接受:', suggestion.id);
      toast.show('success', '✅ 内容已采纳');
    },
    onReject: (suggestion: AISuggestion) => {
      console.log('[EditorContext] ❌ 建议已拒绝:', suggestion.id);
      toast.show('info', '❌ 内容已拒绝');
    },
    onStart: (suggestionId: string) => {
      console.log('[EditorContext] 🚀 开始新建议:', suggestionId);
    },
  });

  const contextValue: EditorContextValue = {
    editor,
    aiSuggestion,
    setEditor,
  };

  return (
    <EditorContext.Provider value={contextValue}>
      {children}
    </EditorContext.Provider>
  );
};

/**
 * 使用EditorContext的Hook
 */
export const useEditorContext = () => {
  const context = useContext(EditorContext);
  if (!context) {
    throw new Error('useEditorContext必须在EditorProvider内部使用');
  }
  return context;
};
```

---

## 📝 Phase 5.2: 集成AIPanel

### 修改EditorView

```typescript
// src/views/EditorView/index.tsx

import { EditorProvider } from './EditorContext';

const EditorView: React.FC = () => {
  return (
    <EditorProvider>
      <div className={styles.page}>
        {/* 工具栏 */}
        <div className={styles.toolbar}>
          {/* ... */}
        </div>

        {/* 编辑器主体 */}
        <div className={styles.editor}>
          {/* 左侧编辑器 */}
          <div className={styles.editorMain}>
            <NovelEditor />
          </div>

          {/* 右侧Agent面板 */}
          {sidebarType === 'agent' && (
            <div className={styles.sidebar}>
              <AIPanel workId={workId} chapterId={chapterId} />
            </div>
          )}
        </div>
      </div>
    </EditorProvider>
  );
};
```

### 修改NovelEditor

```typescript
// src/components/editor/NovelEditor.tsx

import { useEditorContext } from '@/views/EditorView/EditorContext';

const NovelEditor: React.FC<NovelEditorProps> = (props) => {
  const { setEditor } = useEditorContext();

  const editor = useEditor({
    extensions: [
      StarterKit,
      AIPendingMark, // ✅ 注册扩展
      // ... 其他扩展
    ],
    content: props.content,
    // ... 其他配置
  });

  // 暴露editor实例
  useEffect(() => {
    if (editor) {
      setEditor(editor);
    }
    return () => setEditor(null);
  }, [editor, setEditor]);

  // ... 其他代码
};
```

### 修改AIPanel

```typescript
// src/components/editor/AIPanel.tsx

import { useEditorContext } from '@/views/EditorView/EditorContext';
import { AISuggestionCard } from './AISuggestionCard';

export function AIPanel({ workId, chapterId }: AIPanelProps) {
  const { editor, aiSuggestion } = useEditorContext();
  const { sendMessageStream } = useAgentChat();

  const handleSend = async () => {
    if (!inputValue.trim()) return;

    // 1. 检测是否是生成内容的请求
    const isGenerate = inputValue.includes('生成') || inputValue.includes('续写');

    let suggestionId: string | undefined;

    // 2. 如果是生成请求，启动建议
    if (isGenerate) {
      suggestionId = aiSuggestion.startSuggestion({ mode: 'auto' });
    }

    // 3. 发送消息并流式接收
    try {
      await sendMessageStream(
        {
          message: inputValue,
          work_id: workId,
          chapter_id: chapterId,
        },
        {
          onChunk: (chunk) => {
            // 同时插入到编辑器
            if (suggestionId) {
              aiSuggestion.streamInsert(chunk);
            }
          },
          onComplete: () => {
            console.log('生成完成');
          },
        }
      );
    } catch (error) {
      console.error('发送失败:', error);
    }
  };

  return (
    <div className="ai-panel">
      {/* 消息列表 */}
      <div className="messages">
        {messages.map((message, index) => (
          <div key={index}>{/* 消息内容 */}</div>
        ))}

        {/* AI建议卡片 */}
        {aiSuggestion.currentSuggestion && (
          <AISuggestionCard
            suggestion={aiSuggestion.currentSuggestion}
            isGenerating={aiSuggestion.isGenerating}
            onAccept={aiSuggestion.acceptSuggestion}
            onReject={aiSuggestion.rejectSuggestion}
          />
        )}
      </div>

      {/* 输入框 */}
      <Input
        value={inputValue}
        onChange={(e) => setInputValue(e.target.value)}
        onKeyPress={(e) => e.key === 'Enter' && handleSend()}
      />
    </div>
  );
}
```

---

## 📝 Phase 5.3: 完整测试流程

### 测试用例

```typescript
// src/views/EditorView/__tests__/AISuggestion.e2e.test.tsx

import { describe, it, expect, vi } from 'vitest';
import { render, screen, fireEvent, waitFor } from '@testing-library/react';
import { EditorView } from '../index';

describe('AI建议完整流程', () => {
  it('应该完成完整的生成→展示→接受流程', async () => {
    // 1. 渲染组件
    render(<EditorView />);

    // 2. 打开Agent面板
    const agentButton = screen.getByTitle('AI智能助手');
    fireEvent.click(agentButton);

    // 3. 输入生成请求
    const input = screen.getByPlaceholderText('输入问题或指令...');
    fireEvent.change(input, { target: { value: '生成下一段情节' } });
    fireEvent.keyPress(input, { key: 'Enter' });

    // 4. 等待生成中状态
    await waitFor(() => {
      expect(screen.getByText('生成中...')).toBeInTheDocument();
    });

    // 5. 等待生成完成
    await waitFor(() => {
      expect(screen.getByText('接受')).toBeInTheDocument();
      expect(screen.getByText('拒绝')).toBeInTheDocument();
    });

    // 6. 检查编辑器中的pending内容
    const pendingContent = document.querySelector('.ai-pending-content');
    expect(pendingContent).toBeInTheDocument();

    // 7. 点击接受按钮
    const acceptButton = screen.getByText('接受');
    fireEvent.click(acceptButton);

    // 8. 等待状态更新
    await waitFor(() => {
      expect(screen.getByText('已采纳')).toBeInTheDocument();
    });

    // 9. 检查pending标记已移除
    await waitFor(() => {
      const pendingContent = document.querySelector('.ai-pending-content');
      expect(pendingContent).not.toBeInTheDocument();
    });

    // 10. 检查Toast提示
    expect(screen.getByText('✅ 内容已采纳')).toBeInTheDocument();
  });

  it('应该完成拒绝流程', async () => {
    // ... 类似的测试流程，但点击拒绝按钮
  });
});
```

---

## ✅ 验收标准

### Phase 4: 交互实现
- [ ] 接受功能正确移除pending标记
- [ ] 拒绝功能正确删除内容
- [ ] 状态同步无延迟
- [ ] 动画流畅自然

### Phase 5: 集成测试
- [ ] EditorContext正确提供数据
- [ ] AIPanel正确消费Context
- [ ] 完整流程无报错
- [ ] Toast提示正确显示

---

## 📚 相关文档

- [状态管理](./02-state-management.md)
- [Agent卡片](./03-agent-card.md)
- [编辑器同步](./04-editor-sync.md)
- [UX优化](./07-ux-optimization.md)
