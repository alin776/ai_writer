# 组件Props详解

本文档详细说明所有组件的Props配置。

---

## AISuggestionCard

AI建议卡片组件。

### Props

```typescript
interface AISuggestionCardProps {
  /** 建议对象 */
  suggestion: AISuggestion;
  /** 是否正在生成 */
  isGenerating?: boolean;
  /** 接受回调 */
  onAccept: () => void;
  /** 拒绝回调 */
  onReject: () => void;
  /** 自定义类名 */
  className?: string;
}
```

### 详细说明

#### suggestion

- **类型**: `AISuggestion`
- **必填**: ✅
- **说明**: 建议对象，包含id、content、status等信息

```typescript
{
  id: 'suggestion-1234567890',
  content: 'AI生成的内容...',
  startPos: 100,
  endPos: 150,
  status: 'pending',
  createdAt: 1234567890
}
```

#### isGenerating

- **类型**: `boolean`
- **必填**: ❌
- **默认值**: `false`
- **说明**: 控制卡片显示状态
  - `true`: 显示旋转圆圈，收起状态
  - `false`: 显示完整内容，展开状态

#### onAccept

- **类型**: `() => void`
- **必填**: ✅
- **说明**: 用户点击✓按钮时的回调
- **触发时机**: 点击接受按钮或按Tab键

```typescript
const handleAccept = () => {
  console.log('用户接受了建议');
  // 移除pending标记
  // 更新卡片状态为✅
};
```

#### onReject

- **类型**: `() => void`
- **必填**: ✅
- **说明**: 用户点击✗按钮时的回调
- **触发时机**: 点击拒绝按钮或按Esc键

```typescript
const handleReject = () => {
  console.log('用户拒绝了建议');
  // 删除编辑器内容
  // 更新卡片状态为❌
};
```

#### className

- **类型**: `string`
- **必填**: ❌
- **默认值**: `''`
- **说明**: 自定义CSS类名，用于样式覆盖

```typescript
<AISuggestionCard className="my-custom-card" />
```

### 使用示例

```typescript
// 基础使用
<AISuggestionCard
  suggestion={currentSuggestion}
  isGenerating={false}
  onAccept={() => aiSuggestion.acceptSuggestion()}
  onReject={() => aiSuggestion.rejectSuggestion()}
/>

// 生成中状态
<AISuggestionCard
  suggestion={currentSuggestion}
  isGenerating={true}
  onAccept={handleAccept}
  onReject={handleReject}
/>

// 自定义样式
<AISuggestionCard
  suggestion={currentSuggestion}
  onAccept={handleAccept}
  onReject={handleReject}
  className="custom-card-style"
/>
```

---

## NovelEditor

Novel富文本编辑器组件。

### Props

```typescript
interface NovelEditorProps {
  /** 初始内容（HTML） */
  content?: string;
  /** 保存回调 */
  onSave?: (content: string, json: any) => void;
  /** 编辑器就绪回调 */
  onEditorReady?: (editor: Editor) => void;
  /** 占位符文本 */
  placeholder?: string;
  /** 是否自动保存 */
  autoSave?: boolean;
  /** 自动保存间隔（毫秒） */
  autoSaveInterval?: number;
}
```

### 详细说明

#### content

- **类型**: `string`
- **必填**: ❌
- **默认值**: `''`
- **说明**: 编辑器初始HTML内容

```typescript
<NovelEditor content="<p>初始内容</p>" />
```

#### onSave

- **类型**: `(content: string, json: any) => void`
- **必填**: ❌
- **说明**: 内容保存时的回调
- **参数**:
  - `content`: HTML格式内容
  - `json`: ProseMirror JSON格式

```typescript
<NovelEditor
  onSave={(html, json) => {
    console.log('HTML:', html);
    console.log('JSON:', json);
    // 保存到服务器
  }}
/>
```

#### onEditorReady

- **类型**: `(editor: Editor) => void`
- **必填**: ❌
- **说明**: 编辑器初始化完成时的回调
- **用途**: 获取editor实例供外部使用

```typescript
const [editor, setEditor] = useState<Editor | null>(null);

<NovelEditor onEditorReady={setEditor} />
```

#### placeholder

- **类型**: `string`
- **必填**: ❌
- **默认值**: `'开始写作...'`
- **说明**: 编辑器为空时的占位符文本

#### autoSave

- **类型**: `boolean`
- **必填**: ❌
- **默认值**: `true`
- **说明**: 是否启用自动保存

#### autoSaveInterval

- **类型**: `number`
- **必填**: ❌
- **默认值**: `3000`
- **说明**: 自动保存间隔（毫秒）

---

## AIPanel

AI对话面板组件。

### Props

```typescript
interface AIPanelProps {
  /** 作品ID */
  workId: string;
  /** 章节ID（可选） */
  chapterId?: string;
  /** 自定义类名 */
  className?: string;
}
```

### 详细说明

#### workId

- **类型**: `string`
- **必填**: ✅
- **说明**: 当前作品的唯一标识

#### chapterId

- **类型**: `string`
- **必填**: ❌
- **说明**: 当前章节的唯一标识
- **用途**: 用于上下文关联

#### className

- **类型**: `string`
- **必填**: ❌
- **说明**: 自定义样式类名

---

## ToastContainer

Toast消息容器组件。

### Props

```typescript
interface ToastContainerProps {
  /** 消息列表 */
  messages: ToastMessage[];
  /** 关闭回调 */
  onClose: (id: string) => void;
}
```

### 详细说明

#### messages

- **类型**: `ToastMessage[]`
- **必填**: ✅
- **说明**: 要显示的Toast消息数组

```typescript
const messages = [
  { id: '1', type: 'success', message: '保存成功' },
  { id: '2', type: 'error', message: '删除失败' },
];
```

#### onClose

- **类型**: `(id: string) => void`
- **必填**: ✅
- **说明**: 消息关闭时的回调

---

## KeyboardShortcutHint

键盘快捷键提示组件。

### Props

```typescript
interface KeyboardShortcutHintProps {
  /** 是否隐藏 */
  hidden?: boolean;
}
```

### 详细说明

#### hidden

- **类型**: `boolean`
- **必填**: ❌
- **默认值**: `false`
- **说明**: 控制提示的显示/隐藏

```typescript
// 仅在有建议时显示
<KeyboardShortcutHint hidden={!currentSuggestion} />
```

---

## EditorProvider

编辑器上下文提供者。

### Props

```typescript
interface EditorProviderProps {
  /** 子组件 */
  children: React.ReactNode;
}
```

### 详细说明

#### children

- **类型**: `React.ReactNode`
- **必填**: ✅
- **说明**: 需要访问EditorContext的子组件

```typescript
<EditorProvider>
  <NovelEditor />
  <AIPanel />
</EditorProvider>
```

---

## 🎨 Props最佳实践

### 1. 类型安全

```typescript
// ✅ 使用TypeScript接口
interface MyComponentProps {
  required: string;
  optional?: number;
}

// ❌ 避免any类型
interface BadProps {
  data: any; // 不好
}
```

### 2. 默认值

```typescript
// ✅ 使用解构赋值设置默认值
const MyComponent: React.FC<Props> = ({
  isGenerating = false,
  placeholder = '请输入...',
}) => {
  // ...
};
```

### 3. 回调命名

```typescript
// ✅ 使用on前缀
onAccept: () => void;
onReject: () => void;
onSave: (data) => void;

// ❌ 避免模糊命名
accept: () => void; // 不好
handleAccept: () => void; // 不好
```

### 4. 文档注释

```typescript
interface Props {
  /**
   * 建议对象
   * @example { id: '123', content: 'text' }
   */
  suggestion: AISuggestion;

  /**
   * 接受回调
   * @param suggestion 被接受的建议
   */
  onAccept?: (suggestion: AISuggestion) => void;
}
```

---

## 📊 Props验证

### 运行时验证（可选）

```typescript
import PropTypes from 'prop-types';

AISuggestionCard.propTypes = {
  suggestion: PropTypes.shape({
    id: PropTypes.string.isRequired,
    content: PropTypes.string.isRequired,
    status: PropTypes.oneOf(['pending', 'accepted', 'rejected']).isRequired,
  }).isRequired,
  isGenerating: PropTypes.bool,
  onAccept: PropTypes.func.isRequired,
  onReject: PropTypes.func.isRequired,
};
```

### TypeScript编译时验证

```typescript
// ✅ TypeScript会在编译时检查
<AISuggestionCard
  suggestion={suggestion} // 类型检查
  onAccept={handleAccept} // 函数签名检查
  isGenerating={true} // 类型检查
/>
```

---

## 📚 相关文档

- [API参考](./api-reference.md)
- [使用示例](./examples.md)
- [样式规范](./style-guide.md)
