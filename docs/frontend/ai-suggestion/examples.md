# 使用示例

本文档提供完整的代码示例，展示如何在项目中使用AI建议功能。

---

## 🚀 快速开始

### 最小示例

```typescript
import React from 'react';
import { EditorProvider } from '@/views/EditorView/EditorContext';
import NovelEditor from '@/components/editor/NovelEditor';
import { AIPanel } from '@/components/editor/AIPanel';

export const MinimalExample = () => {
  return (
    <EditorProvider>
      <div style={{ display: 'flex', gap: '20px' }}>
        {/* 左侧：编辑器 */}
        <div style={{ flex: 1 }}>
          <NovelEditor placeholder="开始写作..." />
        </div>

        {/* 右侧：AI面板 */}
        <div style={{ width: '400px' }}>
          <AIPanel workId="work-123" chapterId="chapter-456" />
        </div>
      </div>
    </EditorProvider>
  );
};
```

---

## 📝 完整集成示例

### 1. 创建EditorView页面

```typescript
// src/views/EditorView/index.tsx

import React, { useState } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { ArrowLeft, Save, MessageSquare, X } from 'lucide-react';
import { EditorProvider, useEditorContext } from './EditorContext';
import NovelEditor from '@/components/editor/NovelEditor';
import { AIPanel } from '@/components/editor/AIPanel';
import { KeyboardShortcutHint } from '@/components/editor/KeyboardShortcutHint';
import styles from './EditorView.module.css';

const EditorViewContent: React.FC = () => {
  const { chapterId } = useParams<{ chapterId: string }>();
  const navigate = useNavigate();
  const { aiSuggestion } = useEditorContext();
  const [showAIPanel, setShowAIPanel] = useState(false);

  return (
    <div className={styles.page}>
      {/* 工具栏 */}
      <div className={styles.toolbar}>
        <button onClick={() => navigate('/works')} className={styles.backButton}>
          <ArrowLeft className="w-4 h-4" />
          <span>返回</span>
        </button>

        <div className={styles.actions}>
          <button onClick={() => setShowAIPanel(!showAIPanel)} className={styles.aiButton}>
            <MessageSquare className="w-4 h-4" />
            <span>AI助手</span>
          </button>

          <button className={styles.saveButton}>
            <Save className="w-4 h-4" />
            <span>保存</span>
          </button>
        </div>
      </div>

      {/* 主编辑区 */}
      <div className={styles.editor}>
        {/* 左侧编辑器 */}
        <div className={styles.editorMain}>
          <NovelEditor
            placeholder="开始创作你的故事..."
            autoSave={true}
            autoSaveInterval={3000}
            onSave={(html, json) => {
              console.log('保存内容:', { html, json });
              // 调用API保存
            }}
          />
        </div>

        {/* 右侧AI面板 */}
        {showAIPanel && (
          <div className={styles.sidebar}>
            <div className={styles.sidebarHeader}>
              <h3>AI智能助手</h3>
              <button onClick={() => setShowAIPanel(false)}>
                <X className="w-4 h-4" />
              </button>
            </div>

            <AIPanel workId="work-123" chapterId={chapterId} />
          </div>
        )}
      </div>

      {/* 键盘快捷键提示 */}
      {aiSuggestion.currentSuggestion && <KeyboardShortcutHint />}
    </div>
  );
};

// 包裹Provider
export const EditorView: React.FC = () => {
  return (
    <EditorProvider>
      <EditorViewContent />
    </EditorProvider>
  );
};
```

---

### 2. 自定义AIPanel集成

```typescript
// src/components/editor/AIPanel.tsx

import React, { useState } from 'react';
import { Send, Loader2 } from 'lucide-react';
import { useEditorContext } from '@/views/EditorView/EditorContext';
import { AISuggestionCard } from './AISuggestionCard';
import { useAgentChat } from '@/hooks/useAgentChat';
import { Input } from '@/components/ui/input';
import { Button } from '@/components/ui/button';

interface AIPanelProps {
  workId: string;
  chapterId?: string;
}

export const AIPanel: React.FC<AIPanelProps> = ({ workId, chapterId }) => {
  const { aiSuggestion } = useEditorContext();
  const { messages, sendMessageStream, isLoading } = useAgentChat();
  const [inputValue, setInputValue] = useState('');

  const handleSend = async () => {
    if (!inputValue.trim() || isLoading) return;

    const userMessage = inputValue.trim();
    setInputValue('');

    // 检测是否是生成内容的请求
    const isGenerateRequest = /生成|续写|写|创作|扩展/.test(userMessage);

    let suggestionId: string | undefined;

    // 如果是生成请求，启动AI建议
    if (isGenerateRequest) {
      suggestionId = aiSuggestion.startSuggestion({ mode: 'auto' });
    }

    try {
      // 发送消息并流式接收
      await sendMessageStream(
        {
          message: userMessage,
          work_id: workId,
          chapter_id: chapterId,
        },
        {
          onChunk: (chunk: string) => {
            // 同时插入到编辑器
            if (suggestionId && aiSuggestion.isGenerating) {
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
    <div className="ai-panel h-full flex flex-col">
      {/* 消息列表 */}
      <div className="flex-1 overflow-y-auto p-3 space-y-3">
        {messages.map((message, index) => (
          <div key={index} className={`message message-${message.role}`}>
            <p>{message.content}</p>
          </div>
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

        {/* 加载状态 */}
        {isLoading && !aiSuggestion.currentSuggestion && (
          <div className="flex items-center gap-2 text-gray-500">
            <Loader2 className="w-4 h-4 animate-spin" />
            <span>思考中...</span>
          </div>
        )}
      </div>

      {/* 输入框 */}
      <div className="p-3 border-t flex gap-2">
        <Input
          value={inputValue}
          onChange={(e) => setInputValue(e.target.value)}
          onKeyPress={(e) => e.key === 'Enter' && handleSend()}
          placeholder="输入问题或指令..."
          disabled={isLoading}
          className="flex-1"
        />
        <Button onClick={handleSend} disabled={isLoading || !inputValue.trim()}>
          {isLoading ? <Loader2 className="w-4 h-4 animate-spin" /> : <Send className="w-4 h-4" />}
        </Button>
      </div>
    </div>
  );
};
```

---

### 3. 实现EditorContext

```typescript
// src/views/EditorView/EditorContext.tsx

import React, { createContext, useState, useContext, useCallback } from 'react';
import { Editor } from '@tiptap/react';
import { useAISuggestion } from '@/hooks/useAISuggestion';
import { useToast } from '@/hooks/useToast';
import { ToastContainer } from '@/components/ui/Toast';
import type { AISuggestion } from '@/types/ai-suggestion';

interface EditorContextValue {
  editor: Editor | null;
  aiSuggestion: ReturnType<typeof useAISuggestion>;
  setEditor: (editor: Editor | null) => void;
}

const EditorContext = createContext<EditorContextValue | null>(null);

export const EditorProvider: React.FC<{ children: React.ReactNode }> = ({ children }) => {
  const [editor, setEditor] = useState<Editor | null>(null);
  const toast = useToast();

  const aiSuggestion = useAISuggestion(editor, {
    onAccept: (suggestion: AISuggestion) => {
      console.log('✅ 建议已接受:', suggestion.id);
      toast.success('✅ 内容已采纳');

      // 可选：保存到服务器
      saveSuggestionToServer(suggestion);
    },
    onReject: (suggestion: AISuggestion) => {
      console.log('❌ 建议已拒绝:', suggestion.id);
      toast.info('❌ 内容已拒绝');

      // 可选：记录拒绝原因
      logRejection(suggestion);
    },
    onStart: (suggestionId: string) => {
      console.log('🚀 开始新建议:', suggestionId);
    },
  });

  const saveSuggestionToServer = async (suggestion: AISuggestion) => {
    try {
      await fetch('/api/suggestions', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          id: suggestion.id,
          content: suggestion.content,
          status: suggestion.status,
        }),
      });
    } catch (error) {
      console.error('保存失败:', error);
    }
  };

  const logRejection = (suggestion: AISuggestion) => {
    // 记录拒绝原因，用于优化AI
    console.log('Rejection logged:', suggestion.id);
  };

  return (
    <EditorContext.Provider value={{ editor, aiSuggestion, setEditor }}>
      {children}
      <ToastContainer messages={toast.messages} onClose={toast.close} />
    </EditorContext.Provider>
  );
};

export const useEditorContext = () => {
  const context = useContext(EditorContext);
  if (!context) {
    throw new Error('useEditorContext必须在EditorProvider内部使用');
  }
  return context;
};

export { EditorContext };
```

---

### 4. 添加键盘快捷键

```typescript
// src/views/EditorView/index.tsx

import { useKeyboardShortcuts } from '@/hooks/useKeyboardShortcuts';

const EditorViewContent: React.FC = () => {
  const { aiSuggestion } = useEditorContext();

  // 注册快捷键
  useKeyboardShortcuts([
    {
      key: 'Tab',
      handler: (e) => {
        if (aiSuggestion.currentSuggestion) {
          e.preventDefault();
          aiSuggestion.acceptSuggestion();
        }
      },
      description: '接受AI建议',
    },
    {
      key: 'Escape',
      handler: (e) => {
        if (aiSuggestion.currentSuggestion) {
          e.preventDefault();
          aiSuggestion.rejectSuggestion();
        }
      },
      description: '拒绝AI建议',
    },
    {
      key: 's',
      ctrl: true,
      handler: (e) => {
        e.preventDefault();
        handleSave();
      },
      description: '保存',
    },
  ]);

  // ... rest of component
};
```

---

## 🎨 自定义样式示例

### 覆盖默认样式

```css
/* CustomEditor.css */

/* 自定义待确认内容样式 */
.my-custom-editor .ai-pending-content {
  background: linear-gradient(90deg, rgba(59, 130, 246, 0.2) 0%, rgba(59, 130, 246, 0.1) 100%);
  border: 2px solid #3b82f6;
  border-radius: 8px;
  padding: 6px 10px;
}

/* 自定义卡片样式 */
.my-custom-card {
  border-radius: 12px;
  box-shadow: 0 8px 16px rgba(0, 0, 0, 0.1);
}

.my-custom-card .accept-btn {
  background: linear-gradient(135deg, #10b981 0%, #059669 100%);
}

.my-custom-card .reject-btn {
  background: linear-gradient(135deg, #ef4444 0%, #dc2626 100%);
  color: white;
}
```

---

## 🧪 测试示例

### 单元测试

```typescript
// useAISuggestion.test.ts

import { renderHook, act } from '@testing-library/react';
import { useAISuggestion } from '@/hooks/useAISuggestion';
import { createEditor } from '@tiptap/react';
import StarterKit from '@tiptap/starter-kit';
import { AIPendingMark } from '@/components/editor/extensions/AIPendingMark';

describe('useAISuggestion', () => {
  let editor: Editor;

  beforeEach(() => {
    editor = createEditor({
      extensions: [StarterKit, AIPendingMark],
      content: '<p>Initial content</p>',
    });
  });

  it('应该正确启动建议', () => {
    const { result } = renderHook(() => useAISuggestion(editor));

    act(() => {
      const suggestionId = result.current.startSuggestion();
      expect(suggestionId).toBeTruthy();
      expect(result.current.currentSuggestion).not.toBeNull();
      expect(result.current.isGenerating).toBe(true);
    });
  });

  it('应该正确插入内容', () => {
    const { result } = renderHook(() => useAISuggestion(editor));

    act(() => {
      result.current.startSuggestion();
      result.current.streamInsert('测试内容');
    });

    expect(result.current.currentSuggestion?.content).toBe('测试内容');
    expect(editor.getHTML()).toContain('测试内容');
  });

  it('应该正确接受建议', async () => {
    const onAccept = vi.fn();
    const { result } = renderHook(() => useAISuggestion(editor, { onAccept }));

    act(() => {
      result.current.startSuggestion();
      result.current.streamInsert('测试内容');
    });

    await act(async () => {
      await result.current.acceptSuggestion();
    });

    expect(onAccept).toHaveBeenCalled();
    expect(result.current.currentSuggestion).toBeNull();
    // 检查pending标记已移除
    expect(editor.getHTML()).not.toContain('data-ai-pending');
  });
});
```

### E2E测试

```typescript
// EditorView.e2e.test.tsx

import { render, screen, fireEvent, waitFor } from '@testing-library/react';
import { EditorView } from '@/views/EditorView';
import { BrowserRouter } from 'react-router-dom';

describe('EditorView E2E', () => {
  it('应该完成完整的AI建议流程', async () => {
    render(
      <BrowserRouter>
        <EditorView />
      </BrowserRouter>
    );

    // 1. 打开AI面板
    const aiButton = screen.getByText('AI助手');
    fireEvent.click(aiButton);

    // 2. 输入生成请求
    const input = screen.getByPlaceholderText('输入问题或指令...');
    fireEvent.change(input, { target: { value: '生成下一段情节' } });

    // 3. 发送
    const sendButton = screen.getByRole('button', { name: /send/i });
    fireEvent.click(sendButton);

    // 4. 等待生成中状态
    await waitFor(() => {
      expect(screen.getByText('生成中...')).toBeInTheDocument();
    });

    // 5. 等待生成完成
    await waitFor(() => {
      expect(screen.getByText('接受')).toBeInTheDocument();
    }, { timeout: 5000 });

    // 6. 检查编辑器中的pending内容
    const pendingContent = document.querySelector('.ai-pending-content');
    expect(pendingContent).toBeInTheDocument();

    // 7. 点击接受
    const acceptButton = screen.getByText('接受');
    fireEvent.click(acceptButton);

    // 8. 检查状态更新
    await waitFor(() => {
      expect(screen.getByText('✅ 内容已采纳')).toBeInTheDocument();
    });

    // 9. 检查pending标记已移除
    await waitFor(() => {
      expect(document.querySelector('.ai-pending-content')).not.toBeInTheDocument();
    });
  });
});
```

---

## 🔧 高级用法

### 自定义插入位置策略

```typescript
const CustomEditorView = () => {
  const { aiSuggestion } = useEditorContext();

  const handleGenerateAtCursor = () => {
    // 强制在光标位置插入
    aiSuggestion.startSuggestion({ mode: 'cursor' });
  };

  const handleGenerateAtEnd = () => {
    // 强制在末尾插入
    aiSuggestion.startSuggestion({ mode: 'end' });
  };

  const handleGenerateAtPosition = () => {
    // 在指定位置插入
    aiSuggestion.startSuggestion({ position: 500 });
  };

  return (
    <div>
      <button onClick={handleGenerateAtCursor}>在光标处生成</button>
      <button onClick={handleGenerateAtEnd}>在末尾生成</button>
      <button onClick={handleGenerateAtPosition}>在位置500生成</button>
    </div>
  );
};
```

### 批量建议管理

```typescript
const BatchSuggestionManager = () => {
  const { editor } = useEditorContext();
  const [suggestions, setSuggestions] = useState<AISuggestion[]>([]);

  const generateMultiple = async () => {
    const prompts = ['生成开头', '生成发展', '生成高潮', '生成结局'];

    for (const prompt of prompts) {
      const id = aiSuggestion.startSuggestion({ mode: 'end' });
      // 生成内容...
      await generateContent(prompt);
    }
  };

  const acceptAll = async () => {
    for (const suggestion of suggestions) {
      await aiSuggestion.acceptSuggestion();
    }
  };

  return (
    <div>
      <button onClick={generateMultiple}>批量生成</button>
      <button onClick={acceptAll}>全部接受</button>
    </div>
  );
};
```

---

## 📚 相关文档

- [API参考](./api-reference.md)
- [组件Props](./component-props.md)
- [样式规范](./style-guide.md)
