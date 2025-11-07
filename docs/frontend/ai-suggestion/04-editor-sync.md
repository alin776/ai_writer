# Phase 3: 编辑器实时同步

## 📋 任务清单

- [ ] 3.1 修改NovelEditor，注册AIPendingMark扩展
- [ ] 3.2 实现SSE流式响应→编辑器实时插入（带pending标记）
- [ ] 3.3 添加内容插入位置计算逻辑（光标位置/末尾）

## 🎯 目标

实现AI生成内容实时同步到编辑器，带pending标记高亮显示。

---

## 📝 Task 3.1: 注册AIPendingMark扩展

### 修改NovelEditor组件

```typescript
// src/components/editor/NovelEditor.tsx
import { AIPendingMark } from './extensions/AIPendingMark';
import './ai-suggestion-styles.css'; // 引入样式

const NovelEditor: React.FC<NovelEditorProps> = ({
  content,
  onSave,
  onEditorReady, // 新增：暴露editor实例
  // ... 其他props
}) => {
  const editor = useEditor({
    extensions: [
      StarterKit,
      // ... 其他扩展
      AIPendingMark, // ✅ 注册AI Pending Mark扩展
    ],
    // ... 其他配置
  });

  // 暴露editor实例给父组件
  useEffect(() => {
    if (editor && onEditorReady) {
      onEditorReady(editor);
    }
  }, [editor, onEditorReady]);

  // ... 其他代码
};

export default NovelEditor;
```

### 更新Props类型

```typescript
interface NovelEditorProps {
  content?: string;
  onSave?: (content: string, json: any) => void;
  onEditorReady?: (editor: Editor) => void; // ✅ 新增
  placeholder?: string;
  autoSave?: boolean;
  autoSaveInterval?: number;
}
```

---

## 📝 Task 3.2: SSE流式响应绑定

### 修改useAgentChat Hook

```typescript
// src/hooks/useAgentChat.ts
import { useContext } from 'react';
import { EditorContext } from '@/views/EditorView/EditorContext';

export const useAgentChat = () => {
  const editorContext = useContext(EditorContext);

  /**
   * 发送消息并流式接收响应
   */
  const sendMessageStream = async (
    request: AgentChatRequest,
    options?: {
      onChunk?: (chunk: string) => void;
      onComplete?: () => void;
    }
  ) => {
    // 检测是否是生成内容的请求
    const isGenerateContent = detectGenerateIntent(request.message);

    let suggestionId: string | undefined;

    // 如果是生成内容，启动AI建议
    if (isGenerateContent && editorContext?.aiSuggestion) {
      suggestionId = editorContext.aiSuggestion.startSuggestion();
    }

    try {
      const response = await fetch('/api/agent/chat/stream', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(request),
      });

      const reader = response.body?.getReader();
      const decoder = new TextDecoder();

      while (true) {
        const { done, value } = await reader!.read();
        if (done) break;

        const chunk = decoder.decode(value);

        // 1. 更新消息列表（右侧显示）
        addMessageChunk(chunk);

        // 2. 同时插入到编辑器（左侧显示）
        if (suggestionId && editorContext?.aiSuggestion) {
          editorContext.aiSuggestion.streamInsert(chunk);
        }

        // 3. 调用自定义回调
        options?.onChunk?.(chunk);
      }

      options?.onComplete?.();
    } catch (error) {
      console.error('Stream error:', error);
    }
  };

  return {
    sendMessageStream,
    // ... 其他返回值
  };
};

/**
 * 检测是否是生成内容的意图
 */
function detectGenerateIntent(message: string): boolean {
  const keywords = [
    '生成', '续写', '写', '创作', '扩展',
    '补充', '接下来', '然后', '继续',
  ];

  return keywords.some(keyword => message.includes(keyword));
}
```

### 实现逻辑流程图

```
用户输入: "生成下一段情节"
    ↓
检测意图: detectGenerateIntent() → true
    ↓
启动建议: aiSuggestion.startSuggestion()
    ↓
开始SSE流式接收
    ↓
┌───────────────────────────────┐
│  每个chunk到达时:              │
│  1. addMessageChunk()          │  → 右侧Agent卡片显示
│  2. aiSuggestion.streamInsert()│  → 左侧编辑器插入（带pending）
└───────────────────────────────┘
    ↓
流完成: onComplete()
    ↓
卡片展开显示 ✓/✗ 按钮
```

---

## 📝 Task 3.3: 插入位置计算

### 实现智能位置计算

```typescript
// src/hooks/useAISuggestion.ts

export const useAISuggestion = (editor: Editor | null) => {
  /**
   * 计算最佳插入位置
   * @param mode 插入模式
   * @returns 插入位置（ProseMirror position）
   */
  const calculateInsertPosition = useCallback((
    mode: 'cursor' | 'end' | 'auto' = 'auto'
  ): number => {
    if (!editor) return 0;

    const { selection, doc } = editor.state;

    switch (mode) {
      case 'cursor':
        // 光标当前位置
        return selection.to;

      case 'end':
        // 文档末尾
        return doc.content.size;

      case 'auto':
        // 自动判断
        const cursorPos = selection.to;
        const docSize = doc.content.size;

        // 如果光标在文档最后20%区域，使用光标位置
        // 否则使用文档末尾
        const threshold = docSize * 0.8;

        return cursorPos > threshold ? cursorPos : docSize;

      default:
        return selection.to;
    }
  }, [editor]);

  /**
   * 开始新的建议（支持指定位置模式）
   */
  const startSuggestion = useCallback((
    options?: {
      mode?: 'cursor' | 'end' | 'auto';
      position?: number;
    }
  ) => {
    if (!editor) return '';

    const suggestionId = `suggestion-${Date.now()}`;

    // 计算插入位置
    const startPos = options?.position !== undefined
      ? options.position
      : calculateInsertPosition(options?.mode);

    // 滚动到插入位置
    scrollToPosition(startPos);

    const newSuggestion: AISuggestion = {
      id: suggestionId,
      content: '',
      startPos,
      endPos: startPos,
      status: 'pending',
      createdAt: Date.now(),
    };

    setCurrentSuggestion(newSuggestion);
    setIsGenerating(true);
    historyRef.current.set(suggestionId, newSuggestion);

    return suggestionId;
  }, [editor, calculateInsertPosition]);

  /**
   * 滚动到指定位置
   */
  const scrollToPosition = useCallback((pos: number) => {
    if (!editor) return;

    editor.commands.focus();
    editor.commands.setTextSelection(pos);

    // 确保位置可见
    const { node } = editor.view.domAtPos(pos);
    node.scrollIntoView({
      behavior: 'smooth',
      block: 'center',
    });
  }, [editor]);

  return {
    // ... 其他返回值
    calculateInsertPosition,
    startSuggestion,
  };
};
```

### 使用示例

```typescript
// 在AIPanel中使用
const handleGenerate = async (prompt: string) => {
  // 方式1: 自动判断位置
  const suggestionId = aiSuggestion.startSuggestion({ mode: 'auto' });

  // 方式2: 固定光标位置
  const suggestionId = aiSuggestion.startSuggestion({ mode: 'cursor' });

  // 方式3: 固定文档末尾
  const suggestionId = aiSuggestion.startSuggestion({ mode: 'end' });

  // 方式4: 指定精确位置
  const suggestionId = aiSuggestion.startSuggestion({ position: 100 });

  // 开始流式生成...
  await sendMessageStream({
    message: prompt,
    work_id: workId,
  });
};
```

### 位置计算策略

#### 策略1: 智能auto模式
```typescript
// 光标在后20%区域 → 使用光标位置
// 光标在前80%区域 → 使用文档末尾

if (cursorPos > docSize * 0.8) {
  return cursorPos; // 用户可能想在当前位置插入
} else {
  return docSize;   // 用户可能想续写到末尾
}
```

#### 策略2: 根据上下文判断
```typescript
// 检查光标前后是否有内容
const beforeCursor = doc.textBetween(0, cursorPos);
const afterCursor = doc.textBetween(cursorPos, doc.content.size);

if (afterCursor.trim().length === 0) {
  // 光标后无内容，说明在末尾
  return cursorPos;
} else {
  // 光标后有内容，插入到末尾更安全
  return doc.content.size;
}
```

#### 策略3: 尊重用户选择
```typescript
// 如果用户有选中内容，在选区后插入
if (selection.from !== selection.to) {
  return selection.to;
}

// 否则使用光标位置
return selection.to;
```

---

## ✅ 验收标准

### 3.1 扩展注册
- [ ] AIPendingMark在editor.extensions中
- [ ] editor实例正确传递给父组件
- [ ] CSS样式正确加载

### 3.2 流式同步
- [ ] SSE流到达时实时插入编辑器
- [ ] 插入内容带pending标记
- [ ] 右侧卡片和左侧编辑器同步更新
- [ ] 检测生成意图准确

### 3.3 位置计算
- [ ] auto模式智能判断位置
- [ ] cursor模式使用光标位置
- [ ] end模式使用文档末尾
- [ ] 插入后自动滚动到可见区域

---

## 🎯 性能优化

### 1. 批处理chunk插入（优化版）

```typescript
// 使用useRef避免闭包问题
const pendingChunksRef = useRef<string[]>([]);
const rafIdRef = useRef<number | null>(null);

const streamInsert = useCallback((chunk: string) => {
  if (!editor || !currentSuggestion) {
    console.warn('[useAISuggestion] 无法插入：editor或suggestion未初始化');
    return;
  }

  // 添加到待处理队列
  pendingChunksRef.current.push(chunk);

  // 如果还没有调度RAF，则调度一个
  if (rafIdRef.current === null) {
    rafIdRef.current = requestAnimationFrame(() => {
      const combined = pendingChunksRef.current.join('');
      pendingChunksRef.current = [];
      rafIdRef.current = null;

      // 一次性插入合并后的内容
      try {
        editor
          .chain()
          .focus()
          .insertContentAt(currentSuggestion.endPos, {
            type: 'text',
            text: combined,
            marks: [{
              type: 'aiPending',
              attrs: { suggestionId: currentSuggestion.id }
            }]
          })
          .run();

        // 更新建议状态
        setCurrentSuggestion(prev => {
          if (!prev) return null;
          return {
            ...prev,
            content: prev.content + combined,
            endPos: prev.endPos + combined.length,
          };
        });
      } catch (error) {
        console.error('[useAISuggestion] 插入错误:', error);
      }
    });
  }
}, [editor, currentSuggestion]);

// 清理RAF
useEffect(() => {
  return () => {
    if (rafIdRef.current !== null) {
      cancelAnimationFrame(rafIdRef.current);
      rafIdRef.current = null;
    }
  };
}, []);
```

**改进点**:
1. ✅ 使用useRef避免闭包问题
2. ✅ 添加清理逻辑防止内存泄漏
3. ✅ 添加try-catch错误处理
4. ✅ 使用函数式setState避免竞态条件

### 2. 防抖滚动

```typescript
import { useDebouncedCallback } from 'use-debounce';

const debouncedScroll = useDebouncedCallback((pos: number) => {
  const { node } = editor.view.domAtPos(pos);
  node.scrollIntoView({ behavior: 'smooth', block: 'center' });
}, 300);
```

### 3. 限流更新

```typescript
import { throttle } from 'lodash-es';

const throttledInsert = throttle((chunk: string) => {
  // 插入逻辑
}, 100); // 每100ms最多执行一次
```

---

## 🐛 常见问题

### Q1: 插入位置不对？
**A**: 检查ProseMirror position计算：
```typescript
// 打印调试信息
console.log('Doc size:', editor.state.doc.content.size);
console.log('Selection:', editor.state.selection.to);
console.log('Insert pos:', startPos);
```

### Q2: 滚动不平滑？
**A**: 使用平滑滚动API：
```typescript
node.scrollIntoView({
  behavior: 'smooth',  // 平滑滚动
  block: 'center',     // 垂直居中
  inline: 'nearest',   // 水平最近
});
```

### Q3: 流式插入卡顿？
**A**: 使用批处理（见性能优化1）

### Q4: Pending标记丢失？
**A**: 确保Mark配置正确：
```typescript
editor.chain()
  .focus()
  .insertContentAt(pos, {
    type: 'text',
    text: chunk,
    marks: [{
      type: 'aiPending',  // ✅ 正确的Mark名称
      attrs: { suggestionId: id }
    }]
  })
  .run();
```

---

## 📊 数据流图

```
SSE Event Stream
    ↓
┌───────────────┐
│ onChunk(chunk)│
└───────┬───────┘
        ↓
  ┌─────┴─────┐
  ↓           ↓
Agent卡片   Editor
显示内容   streamInsert()
  │           ↓
  │      insertContentAt()
  │       (with pending mark)
  │           ↓
  │      DOM Update
  │           ↓
  │      CSS高亮显示
  │           ↓
  └─────→ 视觉同步 ←────┘
```

---

## 📚 相关文档

- [状态管理](./02-state-management.md)
- [Agent卡片](./03-agent-card.md)
- [交互实现](./05-interaction.md)
- [API参考](./api-reference.md)
