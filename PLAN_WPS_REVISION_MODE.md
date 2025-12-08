# WPS风格修订模式实现计划

## 用户需求
1. **修改模式**: 原文字显示删除线 + AI新内容显示在后面
2. **续写模式**: 新内容追加在选中文字后面
3. **操作按钮**: 重新生成、弃用、采纳

## 现有基础设施

### 后端 (langgraph_agent.py)
- ✅ `context.selected_text` - 编辑器选中的文字
- ✅ `context.selection_position` - 选中位置 {from, to}
- ✅ `editor_action` 返回结构:
  ```python
  {
    "type": "modify" | "continue",
    "original_text": "原文",
    "position": {"from": 10, "to": 50},
    "requires_confirmation": True
  }
  ```

### 前端已有组件
- ✅ `AIRevisionMark.ts` - TipTap 扩展 (AIDeleted, AIInserted)
- ✅ `editor-styles.css` - 修订标记样式 (.ai-deleted, .ai-inserted)
- ✅ `useAgentChat.ts` - 触发 `agent-replace-text` / `agent-append-text` 事件
- ✅ `NovelEditor.tsx` - 监听事件，但直接替换而非显示修订标记

## 实现步骤

### 步骤1: 修改 NovelEditor 事件处理 (NovelEditor.tsx)

**当前逻辑**: 直接替换/追加文本
**目标逻辑**: 使用修订标记显示，等待用户确认

```tsx
// handleAgentReplace 修改为:
const handleAgentReplace = (event: CustomEvent) => {
  const { original, replacement, position, action_type, revisionId } = event.detail;

  if (action_type === 'modify' && position) {
    // 生成唯一修订ID
    const rid = revisionId || `rev-${Date.now()}`;

    // 1. 在原位置应用 AIDeleted 标记（显示删除线）
    editor.chain()
      .focus()
      .setTextSelection({ from: position.from, to: position.to })
      .setAIDeleted()
      .run();

    // 2. 在原文后插入新内容，应用 AIInserted 标记
    editor.chain()
      .setTextSelection(position.to)
      .insertContent(`<ins class="ai-inserted" data-revision-id="${rid}">${replacement}</ins>`)
      .run();

    // 3. 设置当前活跃修订，显示操作栏
    setActiveRevision({
      id: rid,
      type: 'modify',
      position,
      original,
      replacement
    });
  }
};
```

### 步骤2: 创建 AIRevisionBar 组件

新建 `src/components/editor/AIRevisionBar.tsx`:

```tsx
interface AIRevisionBarProps {
  revision: {
    id: string;
    type: 'modify' | 'continue';
    position: { from: number; to: number };
    original?: string;
    replacement: string;
  };
  position: { top: number; left: number };
  onRegenerate: () => void;
  onDiscard: () => void;
  onAccept: () => void;
}

const AIRevisionBar: React.FC<AIRevisionBarProps> = ({
  revision,
  position,
  onRegenerate,
  onDiscard,
  onAccept
}) => {
  return (
    <div
      className="ai-revision-bar"
      style={{ top: position.top, left: position.left }}
    >
      <button onClick={onRegenerate} title="重新生成">
        <RefreshIcon /> 刷新
      </button>
      <button onClick={onDiscard} title="弃用">
        <XIcon /> 弃用
      </button>
      <button onClick={onAccept} title="采纳">
        <CheckIcon /> 采纳
      </button>
    </div>
  );
};
```

### 步骤3: 添加修订状态管理

在 `NovelEditor.tsx` 中添加:

```tsx
// 活跃修订状态
const [activeRevision, setActiveRevision] = useState<{
  id: string;
  type: 'modify' | 'continue';
  position: { from: number; to: number };
  original?: string;
  replacement: string;
} | null>(null);

// 操作栏位置
const [revisionBarPosition, setRevisionBarPosition] = useState<{ top: number; left: number } | null>(null);
```

### 步骤4: 实现三个操作

```tsx
// 采纳：移除标记，保留新内容
const handleAcceptRevision = useCallback(() => {
  if (!activeRevision || !editor) return;

  const { id, type, position, original, replacement } = activeRevision;

  if (type === 'modify') {
    // 删除原文（带删除线的部分）
    editor.chain()
      .setTextSelection({ from: position.from, to: position.to })
      .deleteSelection()
      .run();

    // 移除插入内容的标记，保留文本
    // 找到 data-revision-id 匹配的 ins 元素，替换为纯文本
    editor.chain()
      .unsetAIInserted()
      .run();
  }

  setActiveRevision(null);
  toast.success('已采纳修改');
}, [activeRevision, editor, toast]);

// 弃用：移除新内容，恢复原文
const handleDiscardRevision = useCallback(() => {
  if (!activeRevision || !editor) return;

  // 删除插入的新内容
  // 移除原文的删除线标记
  editor.chain()
    .unsetAIDeleted()
    .run();

  // 删除 ins 元素
  // ...

  setActiveRevision(null);
  toast.info('已弃用修改');
}, [activeRevision, editor, toast]);

// 重新生成：重新发送请求
const handleRegenerateRevision = useCallback(() => {
  if (!activeRevision) return;

  // 先弃用当前修订
  handleDiscardRevision();

  // 重新发送 InlineAI 请求
  // 使用原来的 selected_text 和 context
  // ...

}, [activeRevision, handleDiscardRevision]);
```

### 步骤5: 更新 CSS 样式

在 `editor-styles.css` 中添加:

```css
/* AI 修订操作栏 */
.ai-revision-bar {
  position: fixed;
  z-index: 1000;
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 6px 12px;
  background: white;
  border: 1px solid #e5e7eb;
  border-radius: 8px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
}

.ai-revision-bar button {
  display: flex;
  align-items: center;
  gap: 4px;
  padding: 4px 10px;
  border: none;
  border-radius: 4px;
  font-size: 12px;
  cursor: pointer;
  transition: all 0.15s;
}

.ai-revision-bar button:nth-child(1) {
  background: #f3f4f6;
  color: #4b5563;
}

.ai-revision-bar button:nth-child(2) {
  background: #fee2e2;
  color: #dc2626;
}

.ai-revision-bar button:nth-child(3) {
  background: #dcfce7;
  color: #16a34a;
}
```

### 步骤6: 修改数据流

修改 `useAgentChat.ts` 中的 `submitApproval`:

```tsx
// 不再直接触发替换，而是触发"显示修订"
if (approved && pending.action_type === 'rewrite' && selectedVersion !== undefined) {
  const selectedContent = versions[selectedVersion].content;

  window.dispatchEvent(
    new CustomEvent('agent-show-revision', {
      detail: {
        type: 'modify',
        original: originalContent,
        replacement: selectedContent,
        position: editorAction?.position,
        revisionId: `rev-${Date.now()}`
      }
    })
  );
}
```

## 文件修改清单

| 文件 | 修改内容 |
|------|---------|
| `NovelEditor.tsx` | 修改事件处理，添加修订状态管理 |
| `AIRevisionBar.tsx` | 新建组件 |
| `editor-styles.css` | 添加操作栏样式 |
| `useAgentChat.ts` | 修改 submitApproval 逻辑 |
| `AIRevisionMark.ts` | 可能需要添加更多命令 |

## 注意事项

1. **位置计算**: 操作栏需要跟随修订内容的位置
2. **多修订管理**: 如果用户在确认前又触发新修订，需要处理冲突
3. **撤销支持**: 操作应支持 Ctrl+Z 撤销
4. **滚动同步**: 滚动时操作栏位置需要更新

## 测试用例

1. 选中文字 → 发送"改写"指令 → 显示删除线+新内容 → 点击采纳
2. 选中文字 → 发送"续写"指令 → 显示新内容 → 点击弃用
3. 选中文字 → 发送指令 → 点击重新生成 → 显示新结果
