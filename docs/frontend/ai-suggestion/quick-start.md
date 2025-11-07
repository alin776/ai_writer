# 快速开始 - 5分钟体验AI建议功能

本文档提供最小化实现，让你快速体验AI建议功能的核心交互。

---

## 🚀 最小化实现（MVP）

### 前置条件

- 已有Tiptap编辑器
- 已安装`@tiptap/react`、`@tiptap/core`
- 5分钟时间

---

##步骤1: 创建Mark扩展（2分钟）

```typescript
// src/components/editor/extensions/AIPendingMark.ts
import { Mark } from '@tiptap/core';

export const AIPendingMark = Mark.create({
  name: 'aiPending',

  addAttributes() {
    return {
      suggestionId: {
        default: null,
        parseHTML: (element) => element.getAttribute('data-suggestion-id'),
        renderHTML: (attributes) => ({
          'data-suggestion-id': attributes.suggestionId,
        }),
      },
    };
  },

  parseHTML() {
    return [{ tag: 'span[data-ai-pending]' }];
  },

  renderHTML({ HTMLAttributes }) {
    return [
      'span',
      {
        ...HTMLAttributes,
        'data-ai-pending': 'true',
        class: 'ai-pending-content',
      },
      0,
    ];
  },
});
```

---

## 步骤2: 添加CSS样式（1分钟）

```css
/* src/components/editor/ai-suggestion-styles.css */
.ai-pending-content {
  background: rgba(255, 235, 59, 0.2);
  border: 2px dashed #FFD700;
  border-radius: 4px;
  padding: 4px 6px;
  margin: 0 2px;
}
```

---

## 步骤3: 注册扩展（1分钟）

```typescript
// src/components/editor/NovelEditor.tsx
import { AIPendingMark } from './extensions/AIPendingMark';
import './ai-suggestion-styles.css';

const editor = useEditor({
  extensions: [
    StarterKit,
    AIPendingMark, // ← 添加这行
    // ... 其他扩展
  ],
});
```

---

## 步骤4: 测试插入（1分钟）

在浏览器控制台测试：

```javascript
// 获取editor实例（假设已暴露到window）
const editor = window.editor;

// 插入带pending标记的内容
editor.chain()
  .focus()
  .insertContent({
    type: 'text',
    text: '这是AI生成的内容',
    marks: [{
      type: 'aiPending',
      attrs: { suggestionId: 'test-123' }
    }]
  })
  .run();

// 应该看到黄色高亮的文本
```

---

## 🎉 完成！

你应该看到：
- ✅ 文本有黄色背景
- ✅ 有金色虚线边框
- ✅ 有`data-ai-pending="true"`属性

---

## 📝 下一步

### 实现完整功能

1. **创建useAISuggestion Hook**
   - 参考 [状态管理文档](./02-state-management.md)
   - 实现accept/reject方法

2. **创建AISuggestionCard组件**
   - 参考 [Agent卡片文档](./03-agent-card.md)
   - 添加✓/✗按钮

3. **集成到项目**
   - 参考 [集成指南](./integration-guide.md)
   - 完整集成到EditorView

### 完整实现示例

```typescript
// 完整的useAISuggestion Hook简化版
export const useAISuggestion = (editor: Editor | null) => {
  const [currentSuggestion, setCurrentSuggestion] = useState<any>(null);

  const startSuggestion = () => {
    if (!editor) return '';
    const id = `suggestion-${Date.now()}`;
    setCurrentSuggestion({
      id,
      content: '',
      startPos: editor.state.selection.to,
      endPos: editor.state.selection.to,
    });
    return id;
  };

  const streamInsert = (chunk: string) => {
    if (!editor || !currentSuggestion) return;

    editor.chain()
      .focus()
      .insertContentAt(currentSuggestion.endPos, {
        type: 'text',
        text: chunk,
        marks: [{
          type: 'aiPending',
          attrs: { suggestionId: currentSuggestion.id }
        }]
      })
      .run();

    setCurrentSuggestion(prev => ({
      ...prev,
      content: prev.content + chunk,
      endPos: prev.endPos + chunk.length,
    }));
  };

  const acceptSuggestion = () => {
    if (!editor || !currentSuggestion) return;

    const { doc, tr } = editor.state;
    const { startPos, endPos, id } = currentSuggestion;

    doc.nodesBetween(startPos, endPos, (node, pos) => {
      if (node.isText) {
        const mark = node.marks.find(
          m => m.type.name === 'aiPending' && m.attrs.suggestionId === id
        );
        if (mark) {
          tr.removeMark(pos, pos + node.nodeSize, mark);
        }
      }
    });

    if (tr.steps.length > 0) {
      editor.view.dispatch(tr);
    }

    setCurrentSuggestion(null);
  };

  const rejectSuggestion = () => {
    if (!editor || !currentSuggestion) return;

    editor.chain()
      .focus()
      .deleteRange({
        from: currentSuggestion.startPos,
        to: currentSuggestion.endPos
      })
      .run();

    setCurrentSuggestion(null);
  };

  return {
    currentSuggestion,
    startSuggestion,
    streamInsert,
    acceptSuggestion,
    rejectSuggestion,
  };
};
```

### 在组件中使用

```typescript
const MyEditor = () => {
  const [editor, setEditor] = useState<Editor | null>(null);
  const aiSuggestion = useAISuggestion(editor);

  const handleGenerate = async () => {
    const id = aiSuggestion.startSuggestion();

    // 模拟流式生成
    const text = "这是AI生成的内容...";
    for (const char of text) {
      aiSuggestion.streamInsert(char);
      await new Promise(resolve => setTimeout(resolve, 50));
    }
  };

  return (
    <div>
      <EditorContent editor={editor} />

      <button onClick={handleGenerate}>生成</button>

      {aiSuggestion.currentSuggestion && (
        <div>
          <button onClick={aiSuggestion.acceptSuggestion}>✓ 接受</button>
          <button onClick={aiSuggestion.rejectSuggestion}>✗ 拒绝</button>
        </div>
      )}
    </div>
  );
};
```

---

## 🎓 学习路径

1. **理解Mark机制** (10分钟)
   - Tiptap Mark如何工作
   - 如何应用和移除Mark

2. **理解状态管理** (20分钟)
   - React Hook设计模式
   - 编辑器状态同步

3. **理解流式插入** (20分钟)
   - SSE流式传输
   - 实时UI更新

4. **完整功能集成** (2-3小时)
   - Context设计
   - 组件集成
   - 错误处理

---

## 🐛 调试技巧

### 检查Mark是否应用

```javascript
// 在浏览器控制台
const editor = window.editor;
const json = editor.getJSON();
console.log(JSON.stringify(json, null, 2));

// 查找包含aiPending mark的文本节点
```

### 检查DOM结构

```javascript
// 查找所有pending内容
document.querySelectorAll('[data-ai-pending="true"]').forEach(el => {
  console.log('Pending content:', el.textContent);
  console.log('Suggestion ID:', el.getAttribute('data-suggestion-id'));
});
```

### 检查CSS是否生效

```javascript
// 检查computed style
const el = document.querySelector('.ai-pending-content');
if (el) {
  const styles = window.getComputedStyle(el);
  console.log('Background:', styles.background);
  console.log('Border:', styles.border);
}
```

---

## 📚 相关文档

- [集成指南](./integration-guide.md) - 完整集成步骤
- [状态管理](./02-state-management.md) - Hook详细实现
- [Agent卡片](./03-agent-card.md) - UI组件实现
- [使用示例](./examples.md) - 更多代码示例

---

## 💡 提示

- 如果遇到问题，先检查浏览器控制台的错误信息
- 使用React DevTools查看Hook状态
- 使用元素检查工具查看DOM结构和CSS
- 参考[REVIEW-REPORT.md](./REVIEW-REPORT.md)了解常见问题

---

**预计时间**: 5分钟（最小实现）
**难度**: ⭐☆☆☆☆ (入门)

🤖 Generated with [Claude Code](https://claude.com/claude-code)
