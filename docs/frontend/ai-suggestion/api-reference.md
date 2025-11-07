# API参考文档

本文档详细说明所有对外API接口。

---

## 📦 核心Exports

### useAISuggestion Hook

AI建议状态管理Hook。

#### 导入

```typescript
import { useAISuggestion } from '@/hooks/useAISuggestion';
```

#### 类型定义

```typescript
interface UseAISuggestionOptions {
  onAccept?: (suggestion: AISuggestion) => void;
  onReject?: (suggestion: AISuggestion) => void;
  onStart?: (suggestionId: string) => void;
}

interface UseAISuggestionReturn {
  currentSuggestion: AISuggestion | null;
  isGenerating: boolean;
  startSuggestion: (options?: StartOptions) => string;
  streamInsert: (chunk: string) => void;
  acceptSuggestion: () => Promise<void>;
  rejectSuggestion: () => Promise<void>;
  getSuggestionById: (id: string) => AISuggestion | undefined;
}

type StartOptions = {
  mode?: 'cursor' | 'end' | 'auto';
  position?: number;
};
```

#### 参数

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| editor | `Editor \| null` | ✅ | Tiptap编辑器实例 |
| options | `UseAISuggestionOptions` | ❌ | 回调配置 |

#### 返回值

| 属性 | 类型 | 说明 |
|------|------|------|
| currentSuggestion | `AISuggestion \| null` | 当前活动的建议 |
| isGenerating | `boolean` | 是否正在生成 |
| startSuggestion | `(options?) => string` | 开始新建议 |
| streamInsert | `(chunk) => void` | 流式插入内容 |
| acceptSuggestion | `() => Promise<void>` | 接受建议 |
| rejectSuggestion | `() => Promise<void>` | 拒绝建议 |
| getSuggestionById | `(id) => AISuggestion \| undefined` | 根据ID获取建议 |

#### 示例

```typescript
const MyEditor = () => {
  const [editor, setEditor] = useState<Editor | null>(null);

  const aiSuggestion = useAISuggestion(editor, {
    onAccept: (suggestion) => {
      console.log('已接受:', suggestion.id);
    },
    onReject: (suggestion) => {
      console.log('已拒绝:', suggestion.id);
    },
  });

  const handleGenerate = () => {
    const id = aiSuggestion.startSuggestion({ mode: 'auto' });
    // 开始流式插入...
  };

  return (
    <div>
      <button onClick={handleGenerate}>生成</button>
      {aiSuggestion.currentSuggestion && (
        <>
          <button onClick={aiSuggestion.acceptSuggestion}>接受</button>
          <button onClick={aiSuggestion.rejectSuggestion}>拒绝</button>
        </>
      )}
    </div>
  );
};
```

---

### AIPendingMark Extension

Tiptap Mark扩展，用于标记待确认内容。

#### 导入

```typescript
import { AIPendingMark } from '@/components/editor/extensions/AIPendingMark';
```

#### 注册

```typescript
const editor = useEditor({
  extensions: [
    StarterKit,
    AIPendingMark,
    // ... 其他扩展
  ],
});
```

#### Mark属性

| 属性 | 类型 | 说明 |
|------|------|------|
| suggestionId | `string` | 建议唯一标识 |

#### 命令

```typescript
// 应用pending标记
editor.commands.setMark('aiPending', { suggestionId: 'xxx' });

// 移除pending标记
editor.commands.unsetMark('aiPending');
```

#### HTML输出

```html
<span data-ai-pending="true" data-suggestion-id="xxx" class="ai-pending-content">
  待确认的内容
</span>
```

---

### AISuggestionCard Component

AI建议卡片组件。

#### 导入

```typescript
import { AISuggestionCard } from '@/components/editor/AISuggestionCard';
```

#### Props

```typescript
interface AISuggestionCardProps {
  suggestion: AISuggestion;
  isGenerating?: boolean;
  onAccept: () => void;
  onReject: () => void;
  className?: string;
}
```

| Prop | 类型 | 必填 | 默认值 | 说明 |
|------|------|------|--------|------|
| suggestion | `AISuggestion` | ✅ | - | 建议对象 |
| isGenerating | `boolean` | ❌ | `false` | 是否生成中 |
| onAccept | `() => void` | ✅ | - | 接受回调 |
| onReject | `() => void` | ✅ | - | 拒绝回调 |
| className | `string` | ❌ | `''` | 自定义类名 |

#### 示例

```typescript
<AISuggestionCard
  suggestion={currentSuggestion}
  isGenerating={isGenerating}
  onAccept={() => console.log('Accept')}
  onReject={() => console.log('Reject')}
  className="my-custom-card"
/>
```

---

### EditorContext

共享编辑器实例和AI状态的Context。

#### 导入

```typescript
import { EditorContext, EditorProvider, useEditorContext } from '@/views/EditorView/EditorContext';
```

#### Provider

```typescript
<EditorProvider>
  <YourComponents />
</EditorProvider>
```

#### Hook使用

```typescript
const MyComponent = () => {
  const { editor, aiSuggestion, setEditor } = useEditorContext();

  return <div>{/* 使用editor和aiSuggestion */}</div>;
};
```

#### Context值

```typescript
interface EditorContextValue {
  editor: Editor | null;
  aiSuggestion: ReturnType<typeof useAISuggestion>;
  setEditor: (editor: Editor | null) => void;
}
```

---

### useKeyboardShortcuts Hook

全局键盘快捷键Hook。

#### 导入

```typescript
import { useKeyboardShortcuts } from '@/hooks/useKeyboardShortcuts';
```

#### 类型定义

```typescript
interface KeyboardShortcut {
  key: string;
  ctrl?: boolean;
  shift?: boolean;
  alt?: boolean;
  handler: (event: KeyboardEvent) => void;
  description?: string;
}
```

#### 示例

```typescript
useKeyboardShortcuts([
  {
    key: 'Tab',
    handler: (e) => {
      e.preventDefault();
      handleAccept();
    },
    description: '接受建议',
  },
  {
    key: 'Escape',
    handler: handleReject,
    description: '拒绝建议',
  },
  {
    key: 's',
    ctrl: true,
    handler: handleSave,
    description: '保存',
  },
]);
```

---

### useToast Hook

Toast消息管理Hook。

#### 导入

```typescript
import { useToast } from '@/hooks/useToast';
```

#### 返回值

```typescript
interface UseToastReturn {
  messages: ToastMessage[];
  show: (type: ToastType, message: string, duration?: number) => void;
  close: (id: string) => void;
  success: (message: string, duration?: number) => void;
  error: (message: string, duration?: number) => void;
  info: (message: string, duration?: number) => void;
  warning: (message: string, duration?: number) => void;
}
```

#### 示例

```typescript
const MyComponent = () => {
  const toast = useToast();

  const handleClick = () => {
    toast.success('操作成功！');
    toast.error('操作失败！', 5000); // 5秒后消失
    toast.info('提示信息');
    toast.warning('警告信息');
  };

  return (
    <>
      <button onClick={handleClick}>显示Toast</button>
      <ToastContainer messages={toast.messages} onClose={toast.close} />
    </>
  );
};
```

---

## 📊 数据类型

### AISuggestion

```typescript
interface AISuggestion {
  id: string;
  content: string;
  startPos: number;
  endPos: number;
  status: 'pending' | 'accepted' | 'rejected';
  createdAt: number;
}
```

| 字段 | 类型 | 说明 |
|------|------|------|
| id | `string` | 唯一标识符 |
| content | `string` | 生成的文本内容 |
| startPos | `number` | ProseMirror起始位置 |
| endPos | `number` | ProseMirror结束位置 |
| status | `'pending' \| 'accepted' \| 'rejected'` | 状态 |
| createdAt | `number` | 创建时间戳 |

### ToastMessage

```typescript
interface ToastMessage {
  id: string;
  type: 'success' | 'error' | 'info' | 'warning';
  message: string;
  duration?: number;
}
```

---

## 🎛️ 配置选项

### AIPendingMark配置

```typescript
AIPendingMark.configure({
  HTMLAttributes: {
    class: 'custom-pending-class',
  },
})
```

### useAISuggestion配置

```typescript
useAISuggestion(editor, {
  onAccept: (suggestion) => {
    // 自定义接受逻辑
  },
  onReject: (suggestion) => {
    // 自定义拒绝逻辑
  },
  onStart: (suggestionId) => {
    // 开始时的回调
  },
})
```

---

## 🔧 工具函数

### calculateInsertPosition

计算最佳插入位置（内部使用）。

```typescript
const pos = calculateInsertPosition('auto'); // 'cursor' | 'end' | 'auto'
```

### detectGenerateIntent

检测用户意图是否为生成内容。

```typescript
const isGenerate = detectGenerateIntent('生成下一段');
// → true
```

---

## 📝 命名规范

### 状态命名

- `currentSuggestion` - 当前建议
- `isGenerating` - 生成中标志
- `messages` - 消息列表

### 方法命名

- `startSuggestion` - 开始建议
- `streamInsert` - 流式插入
- `acceptSuggestion` - 接受建议
- `rejectSuggestion` - 拒绝建议

### 回调命名

- `onAccept` - 接受回调
- `onReject` - 拒绝回调
- `onStart` - 开始回调
- `onComplete` - 完成回调

---

## 🚨 错误处理

### 常见错误

```typescript
// ❌ Editor未初始化
useAISuggestion(null); // 会输出warning但不会crash

// ❌ Context外使用
useEditorContext(); // 抛出错误: "必须在EditorProvider内部使用"

// ❌ 无效的建议ID
getSuggestionById('invalid-id'); // 返回undefined
```

### 最佳实践

```typescript
// ✅ 检查editor是否存在
if (editor) {
  aiSuggestion.startSuggestion();
}

// ✅ 检查当前建议
if (aiSuggestion.currentSuggestion) {
  aiSuggestion.acceptSuggestion();
}

// ✅ 错误边界包裹
<ErrorBoundary>
  <EditorProvider>
    <YourApp />
  </EditorProvider>
</ErrorBoundary>
```

---

## 📚 相关文档

- [状态管理](./02-state-management.md)
- [组件Props](./component-props.md)
- [使用示例](./examples.md)
