# 集成指南 - 如何将AI建议功能集成到现有项目

本文档说明如何将AI建议功能集成到现有的AI Writer项目中。

---

## 📋 前置条件检查

### 当前项目状态
- ✅ 已有`NovelEditor.tsx`（基于Tiptap）
- ✅ 已有`AIPanel.tsx`（AI对话面板）
- ✅ 已有`useAgentChat.ts`（Agent聊天Hook）
- ⚠️ 缺少`useAISuggestion.ts`（需要创建）
- ⚠️ 缺少`AIPendingMark.ts`（需要创建）
- ⚠️ 缺少`EditorContext.tsx`（需要创建）

### 需要安装的依赖

```bash
# 检查是否已安装
npm list @tiptap/react @tiptap/core lucide-react use-debounce

# 如未安装，执行
npm install @tiptap/react@^2.1.0 @tiptap/core@^2.1.0
npm install lucide-react@^0.294.0 use-debounce@^10.0.0
```

---

## 🚀 分阶段集成计划

### Phase 0: 准备工作（30分钟）

#### 0.1 创建类型定义文件

```bash
# 创建types目录（如不存在）
mkdir -p src/types

# 创建ai-suggestion.ts
touch src/types/ai-suggestion.ts
```

```typescript
// src/types/ai-suggestion.ts
export interface AISuggestion {
  id: string;
  content: string;
  startPos: number;
  endPos: number;
  status: 'pending' | 'accepted' | 'rejected';
  createdAt: number;
}

export interface UseAISuggestionOptions {
  onAccept?: (suggestion: AISuggestion) => void;
  onReject?: (suggestion: AISuggestion) => void;
  onStart?: (suggestionId: string) => void;
}

// ... 其他类型定义见 types-definition.md
```

#### 0.2 准备CSS文件

```bash
# 在editor组件目录创建样式文件
touch src/components/editor/ai-suggestion-styles.css
```

参考[样式规范文档](./style-guide.md)中的CSS代码。

---

### Phase 1: 创建核心Hook（1-2小时）

#### 1.1 创建useAISuggestion Hook

```bash
touch src/hooks/useAISuggestion.ts
```

完整代码参考[状态管理文档](./02-state-management.md)，关键点：

```typescript
// src/hooks/useAISuggestion.ts
import { useState, useCallback, useRef } from 'react';
import { Editor } from '@tiptap/react';
import type { AISuggestion, UseAISuggestionOptions } from '@/types/ai-suggestion';

export const useAISuggestion = (
  editor: Editor | null,
  options?: UseAISuggestionOptions
) => {
  // 实现代码...

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

#### 1.2 创建AIPendingMark扩展

```bash
mkdir -p src/components/editor/extensions
touch src/components/editor/extensions/AIPendingMark.ts
```

完整代码参考[状态管理文档](./02-state-management.md#task-11)。

---

### Phase 2: 创建UI组件（1-2小时）

#### 2.1 创建AISuggestionCard组件

```bash
touch src/components/editor/AISuggestionCard.tsx
touch src/components/editor/AISuggestionCard.css
```

完整代码参考[Agent卡片文档](./03-agent-card.md)。

**注意事项**:
- 使用项目中已有的`lucide-react`图标
- CSS类名避免与现有样式冲突
- 确保深色模式适配

---

### Phase 3: 集成到NovelEditor（30分钟）

#### 3.1 修改NovelEditor.tsx

```typescript
// src/components/editor/NovelEditor.tsx

// 1. 导入新扩展和样式
import { AIPendingMark } from './extensions/AIPendingMark';
import './ai-suggestion-styles.css';

// 2. 在editor配置中注册扩展
const editor = useEditor({
  extensions: [
    StarterKit,
    // ... 其他扩展
    AIPendingMark, // ← 添加这行
  ],
  // ... 其他配置
});

// 3. 暴露editor实例（如果还没有）
useEffect(() => {
  if (editor && onEditorReady) {
    onEditorReady(editor);
  }
}, [editor, onEditorReady]);
```

#### 3.2 更新Props类型

```typescript
interface NovelEditorProps {
  content?: string;
  onSave?: (content: string, json: any) => void;
  onEditorReady?: (editor: Editor) => void; // ← 添加这个
  placeholder?: string;
  autoSave?: boolean;
  autoSaveInterval?: number;
}
```

---

### Phase 4: 集成到EditorView（1-2小时）

#### 4.1 创建EditorContext

```bash
mkdir -p src/views/EditorView
touch src/views/EditorView/EditorContext.tsx
```

```typescript
// src/views/EditorView/EditorContext.tsx

import React, { createContext, useState, useContext } from 'react';
import { Editor } from '@tiptap/react';
import { useAISuggestion } from '@/hooks/useAISuggestion';
import { useToast } from '@/hooks/useToast';
import { ToastContainer } from '@/components/ui/Toast';

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
    onAccept: (suggestion) => {
      toast.success('✅ 内容已采纳');
      console.log('[EditorContext] 建议已接受:', suggestion.id);
    },
    onReject: (suggestion) => {
      toast.info('❌ 内容已拒绝');
      console.log('[EditorContext] 建议已拒绝:', suggestion.id);
    },
  });

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

#### 4.2 修改EditorView/index.tsx

```typescript
// src/views/EditorView/index.tsx

import { EditorProvider, useEditorContext } from './EditorContext';

// 1. 将原有组件包裹在Provider中
const EditorView: React.FC = () => {
  return (
    <EditorProvider>
      <EditorViewContent />
    </EditorProvider>
  );
};

// 2. 将原有的EditorView逻辑移到EditorViewContent
const EditorViewContent: React.FC = () => {
  const { editor, setEditor, aiSuggestion } = useEditorContext();

  return (
    <div className={styles.page}>
      {/* 工具栏 */}
      <div className={styles.toolbar}>
        {/* ... */}
      </div>

      {/* 主编辑区 */}
      <div className={styles.editor}>
        {/* 左侧编辑器 */}
        <div className={styles.editorMain}>
          <NovelEditor
            onEditorReady={setEditor} // ← 暴露editor实例
            // ... 其他props
          />
        </div>

        {/* 右侧AI面板 */}
        {showAIPanel && (
          <div className={styles.sidebar}>
            <AIPanel workId={workId} chapterId={chapterId} />
          </div>
        )}
      </div>
    </div>
  );
};

export default EditorView;
```

---

### Phase 5: 修改AIPanel（1小时）

#### 5.1 修改AIPanel.tsx

```typescript
// src/components/editor/AIPanel.tsx

import { useEditorContext } from '@/views/EditorView/EditorContext';
import { AISuggestionCard } from './AISuggestionCard';

export const AIPanel: React.FC<AIPanelProps> = ({ workId, chapterId }) => {
  const { aiSuggestion } = useEditorContext(); // ← 获取aiSuggestion
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
      try {
        suggestionId = aiSuggestion.startSuggestion({ mode: 'auto' });
      } catch (error) {
        console.error('启动建议失败:', error);
        // 继续发送消息，但不创建建议
      }
    }

    try {
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
      // 清理失败的建议
      if (suggestionId) {
        aiSuggestion.rejectSuggestion();
      }
    }
  };

  return (
    <div className="ai-panel h-full flex flex-col">
      {/* 消息列表 */}
      <div className="flex-1 overflow-y-auto p-3 space-y-3">
        {messages.map((message, index) => (
          <div key={index} className={`message message-${message.role}`}>
            <MarkdownContent content={message.content} />
          </div>
        ))}

        {/* AI建议卡片 - 在消息列表底部显示 */}
        {aiSuggestion.currentSuggestion && (
          <AISuggestionCard
            suggestion={aiSuggestion.currentSuggestion}
            isGenerating={aiSuggestion.isGenerating}
            onAccept={aiSuggestion.acceptSuggestion}
            onReject={aiSuggestion.rejectSuggestion}
          />
        )}

        {/* 原有的加载状态 */}
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

### Phase 6: 添加键盘快捷键（可选，30分钟）

#### 6.1 创建useKeyboardShortcuts Hook

```bash
touch src/hooks/useKeyboardShortcuts.ts
```

参考[UX优化文档](./06-ux-optimization.md#task-61)。

#### 6.2 在EditorView中使用

```typescript
// src/views/EditorView/index.tsx (EditorViewContent)

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
  ]);

  // ... rest of component
};
```

---

## ✅ 验证清单

### 功能验证

- [ ] **编辑器初始化**: NovelEditor正常加载，AIPendingMark扩展已注册
- [ ] **开始建议**: 在AIPanel输入"生成下一段"，能正确启动建议
- [ ] **流式插入**: 内容实时插入到编辑器，带黄色高亮
- [ ] **卡片显示**: AIPanel中显示AISuggestionCard，有✓/✗按钮
- [ ] **接受建议**: 点击✓，编辑器中高亮消失，内容保留
- [ ] **拒绝建议**: 点击✗，编辑器中内容删除
- [ ] **Toast提示**: 接受/拒绝后显示Toast消息
- [ ] **键盘快捷键**: Tab接受，Esc拒绝（如已实现）

### 错误处理验证

- [ ] **editor未初始化**: startSuggestion抛出错误
- [ ] **并发建议**: 快速点击2次，第2次返回现有ID
- [ ] **网络错误**: 流式请求失败，正确清理状态
- [ ] **无效位置**: 插入到无效位置，catch错误

### 性能验证

- [ ] **流式插入流畅**: 快速输入时无卡顿
- [ ] **内存无泄漏**: 生成50+建议后，内存稳定
- [ ] **动画流畅**: 卡片展开/收起动画60fps

---

## 🐛 常见问题排查

### 问题1: 编辑器中看不到高亮

**可能原因**:
1. AIPendingMark扩展未注册
2. CSS文件未引入
3. suggestionId不匹配

**解决方案**:
```typescript
// 检查extensions数组
console.log('扩展列表:', editor?.extensionManager.extensions.map(e => e.name));

// 检查mark是否应用
console.log('当前marks:', editor?.state.doc.content.toJSON());
```

### 问题2: 卡片不显示

**可能原因**:
1. useEditorContext在Provider外使用
2. currentSuggestion为null

**解决方案**:
```typescript
// 检查Context
const EditorViewContent = () => {
  try {
    const { aiSuggestion } = useEditorContext();
    console.log('Current suggestion:', aiSuggestion.currentSuggestion);
  } catch (error) {
    console.error('Context错误:', error);
  }
};
```

### 问题3: 键盘快捷键不工作

**可能原因**:
1. 事件被其他组件捕获
2. currentSuggestion为null

**解决方案**:
```typescript
// 添加调试日志
useKeyboardShortcuts([
  {
    key: 'Tab',
    handler: (e) => {
      console.log('Tab pressed, suggestion:', aiSuggestion.currentSuggestion);
      if (aiSuggestion.currentSuggestion) {
        e.preventDefault();
        aiSuggestion.acceptSuggestion();
      }
    },
  },
]);
```

---

## 📊 集成进度追踪

| Phase | 任务 | 预计时间 | 状态 |
|-------|------|----------|------|
| 0 | 准备工作 | 30分钟 | ⏳ |
| 1 | 创建核心Hook | 1-2小时 | ⏳ |
| 2 | 创建UI组件 | 1-2小时 | ⏳ |
| 3 | 集成NovelEditor | 30分钟 | ⏳ |
| 4 | 集成EditorView | 1-2小时 | ⏳ |
| 5 | 修改AIPanel | 1小时 | ⏳ |
| 6 | 键盘快捷键（可选） | 30分钟 | ⏳ |
| **总计** | | **5-7小时** | ⏳ |

---

## 📚 相关文档

- [快速开始](./quick-start.md) - 5分钟快速体验
- [状态管理](./02-state-management.md) - Hook详细实现
- [Agent卡片](./03-agent-card.md) - UI组件实现
- [编辑器同步](./04-editor-sync.md) - 流式同步机制
- [API参考](./api-reference.md) - 完整API说明
- [使用示例](./examples.md) - 代码示例

---

## 💡 最佳实践

1. **分阶段集成**: 按Phase顺序逐步实现，每个Phase都要测试
2. **保留现有功能**: 不要破坏现有的编辑器和AIPanel功能
3. **渐进式增强**: 先实现最小可用版本，再逐步添加功能
4. **充分测试**: 每个Phase完成后都要测试所有场景
5. **代码Review**: 完成后请其他开发者Review代码

---

**创建时间**: 2025-01-07
**预计集成时间**: 5-7小时
**难度等级**: ⭐⭐⭐☆☆ (中等)

🤖 Generated with [Claude Code](https://claude.com/claude-code)
