# Quick Edit 功能详细设计

## 📋 功能概述

**Quick Edit** 是一个编辑器内浮动AI对话框，允许用户在不离开编辑器的情况下，直接在选中文字附近与AI交互，保持高度专注的写作体验。

### 核心价值
- ⚡ **极速交互：** 无需切换到侧边栏，即时弹出对话框
- 🎯 **保持专注：** 始终停留在编辑器内，减少上下文切换
- 💬 **灵活对话：** 支持自由输入提示词，完整Agent能力
- 🔄 **实时预览：** 流式显示AI响应，实时查看效果
- ✅ **一键应用：** 接受或撤销AI建议

### ⚠️ 重要说明：纯前端实现

**后端改动：** ❌ **无需任何后端代码改动**

本功能是**纯前端实现**，通过以下方式复用现有API：
- 使用现有的 `/api/v1/ai/complete` 端点（已支持自定义prompt）
- 通过新的 `AIService.quickEdit()` 方法调用
- 只需前端实现浮动UI和交互逻辑

**前置条件：** ⚠️ **必须先完成 `AIService.ts` 的修复**（详见 [04_前后端协作方案.md](./04_前后端协作方案.md)），否则无法实现自定义提示词功能

---

## 🎨 UI设计

### 视觉效果图

```
┌─────────────────────────────────────────────────┐
│  编辑器内容区域                                   │
│                                                   │
│  难道那种压迫感，其实就是杀气？                   │ ← 选中的文字
│  ▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔                       │
│                                                   │
│  ┌────────────────────────────────────────┐     │
│  │  Quick Edit                       [×]  │     │ ← 浮动对话框
│  ├────────────────────────────────────────┤     │
│  │  选中文字: "难道那种压迫感..."        │     │
│  ├────────────────────────────────────────┤     │
│  │  ┌──────────────────────────────────┐ │     │
│  │  │ 告诉AI你想做什么...              │ │     │ ← 输入框
│  │  │ 例如：改得更口语化一点            │ │     │
│  │  └──────────────────────────────────┘ │     │
│  │  [发送] [取消]                        │     │
│  ├────────────────────────────────────────┤     │
│  │  AI响应：                            │     │
│  │  "那种压迫感，该不会就是杀气吧？"    │     │ ← AI流式响应
│  │  ▓ (正在生成...)                     │     │
│  ├────────────────────────────────────────┤     │
│  │  [✓ 应用] [✗ 撤销] [↻ 重新生成]     │     │ ← 操作按钮
│  └────────────────────────────────────────┘     │
│                                                   │
│  段融听到萧宗庭的问话，才停止了思绪，回转到眼前   │
│  的场景。                                        │
└─────────────────────────────────────────────────┘
```

### 交互状态

| 状态 | 描述 | 视觉表现 |
|------|------|---------|
| **初始状态** | 浮动框刚弹出 | 显示输入框，聚焦 |
| **输入中** | 用户正在输入提示词 | 输入框高亮，发送按钮可用 |
| **等待响应** | 已发送请求，等待AI | 加载动画，输入框禁用 |
| **流式响应** | AI正在生成内容 | 逐字显示，闪烁光标 |
| **响应完成** | AI生成完毕 | 显示完整内容，操作按钮可用 |
| **错误状态** | API调用失败 | 显示错误信息，重试按钮 |

---

## 🏗️ 技术架构

### 组件层次结构

```
QuickEditPanel (Container)
│
├─ QuickEditHeader
│  ├─ Title: "Quick Edit"
│  └─ CloseButton: [×]
│
├─ QuickEditBody
│  ├─ SelectedTextPreview  (可选)
│  │  └─ "选中文字: ..."
│  │
│  ├─ QuickEditInput
│  │  ├─ Textarea: 用户输入
│  │  └─ SendButton: [发送]
│  │
│  └─ QuickEditResponse
│     ├─ AIContent: AI响应内容
│     ├─ LoadingIndicator: 加载动画
│     └─ ErrorMessage: 错误提示
│
└─ QuickEditFooter
   ├─ ApplyButton: [✓ 应用]
   ├─ RejectButton: [✗ 撤销]
   └─ RegenerateButton: [↻ 重新生成]
```

### 核心组件

#### 1. QuickEditPanel.tsx

**职责:**
- 浮动UI定位和显示
- 管理内部状态
- 处理AI请求
- 应用/撤销操作

**Props:**
```typescript
interface QuickEditPanelProps {
  editor: Editor;              // Tiptap编辑器实例
  position: { x: number; y: number };  // 浮动框位置
  selectedText: string;         // 选中的文本
  selectionRange: { from: number; to: number };  // 选中范围
  onClose: () => void;          // 关闭回调
}
```

**State:**
```typescript
interface QuickEditState {
  input: string;                // 用户输入的提示词
  aiResponse: string;           // AI响应内容
  isLoading: boolean;           // 加载状态
  error: string | null;         // 错误信息
  stage: 'input' | 'streaming' | 'complete' | 'error';  // 当前阶段
}
```

---

### 浮动UI定位算法

使用 **@floating-ui/dom** 实现智能定位：

```typescript
import { computePosition, flip, shift, offset, arrow } from '@floating-ui/dom';

async function updateFloatingPosition(
  referenceElement: HTMLElement,    // 参考元素（选中文本）
  floatingElement: HTMLElement,     // 浮动元素（对话框）
  arrowElement?: HTMLElement        // 箭头元素（可选）
) {
  const { x, y, placement, middlewareData } = await computePosition(
    referenceElement,
    floatingElement,
    {
      placement: 'bottom-start',    // 优先显示在下方左对齐
      middleware: [
        offset(10),                 // 距离选中文本10px
        flip(),                     // 如果下方空间不足，自动翻转到上方
        shift({ padding: 10 }),     // 横向调整，避免溢出窗口
        arrow({ element: arrowElement }),  // 箭头定位
      ],
    }
  );

  // 应用位置
  Object.assign(floatingElement.style, {
    left: `${x}px`,
    top: `${y}px`,
  });

  // 应用箭头位置
  if (arrowElement && middlewareData.arrow) {
    const { x: arrowX, y: arrowY } = middlewareData.arrow;
    Object.assign(arrowElement.style, {
      left: arrowX != null ? `${arrowX}px` : '',
      top: arrowY != null ? `${arrowY}px` : '',
    });
  }

  return { x, y, placement };
}
```

**定位策略:**
1. **首选位置:** 选中文字下方，左对齐
2. **空间不足:** 自动翻转到上方
3. **横向溢出:** 自动横向调整
4. **响应滚动:** 监听scroll事件，实时更新位置
5. **响应resize:** 监听resize事件，重新计算位置

---

## 💾 状态管理

### Zustand Store扩展

```typescript
// src/store/editorStore.ts

interface QuickEditConfig {
  open: boolean;                     // 是否打开
  position: { x: number; y: number } | null;  // 位置
  selectedText: string;              // 选中文本
  selectionRange: { from: number; to: number } | null;  // 选中范围
  timestamp: number;                 // 时间戳
}

interface EditorStore {
  // ... 现有状态

  quickEditConfig: QuickEditConfig;

  // 打开Quick Edit
  openQuickEdit: (
    position: { x: number; y: number },
    selectedText: string,
    selectionRange: { from: number; to: number }
  ) => void;

  // 关闭Quick Edit
  closeQuickEdit: () => void;
}

export const useEditorStore = create<EditorStore>((set) => ({
  // ... 现有实现

  quickEditConfig: {
    open: false,
    position: null,
    selectedText: '',
    selectionRange: null,
    timestamp: 0,
  },

  openQuickEdit: (position, selectedText, selectionRange) => {
    set({
      quickEditConfig: {
        open: true,
        position,
        selectedText,
        selectionRange,
        timestamp: Date.now(),
      },
    });
  },

  closeQuickEdit: () => {
    set({
      quickEditConfig: {
        open: false,
        position: null,
        selectedText: '',
        selectionRange: null,
        timestamp: 0,
      },
    });
  },
}));
```

---

## 🔧 组件实现

### 1. QuickEditPanel 主组件

**文件:** `src/components/editor/QuickEditPanel.tsx`

```typescript
import React, { useState, useRef, useEffect } from 'react';
import { Editor } from '@tiptap/core';
import { X, Loader2, Check, RotateCw } from 'lucide-react';
import { computePosition, flip, shift, offset } from '@floating-ui/dom';
import AIService from '@/services/AIService';
import { useToast } from '@/hooks/useToast';

interface QuickEditPanelProps {
  editor: Editor;
  position: { x: number; y: number };
  selectedText: string;
  selectionRange: { from: number; to: number };
  onClose: () => void;
}

type Stage = 'input' | 'streaming' | 'complete' | 'error';

export const QuickEditPanel: React.FC<QuickEditPanelProps> = ({
  editor,
  position,
  selectedText,
  selectionRange,
  onClose,
}) => {
  const [input, setInput] = useState('');
  const [aiResponse, setAIResponse] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [stage, setStage] = useState<Stage>('input');

  const panelRef = useRef<HTMLDivElement>(null);
  const inputRef = useRef<HTMLTextAreaElement>(null);
  const toast = useToast();

  // 自动聚焦输入框
  useEffect(() => {
    setTimeout(() => {
      inputRef.current?.focus();
    }, 100);
  }, []);

  // 处理提交
  const handleSubmit = async () => {
    if (!input.trim()) {
      toast.warning('请输入提示词');
      return;
    }

    setIsLoading(true);
    setStage('streaming');
    setError(null);
    setAIResponse('');

    try {
      // ✅ 使用新的 quickEdit 方法（需要先修复 AIService.ts）
      await AIService.quickEdit(
        selectedText,    // 选中的文本
        input,          // 用户输入的提示词
        (chunk) => {
          setAIResponse((prev) => prev + chunk);
        }
      );

      setStage('complete');
    } catch (err) {
      console.error('Quick Edit AI请求失败:', err);
      setError((err as Error).message || '生成失败');
      setStage('error');
      toast.error('生成失败', (err as Error).message);
    } finally {
      setIsLoading(false);
    }
  };

  // 应用AI响应到编辑器
  const handleApply = () => {
    if (!aiResponse) return;

    const { from, to } = selectionRange;
    editor
      .chain()
      .focus()
      .deleteRange({ from, to })
      .insertContent(aiResponse)
      .run();

    toast.success('已应用AI建议');
    onClose();
  };

  // 撤销（不应用，直接关闭）
  const handleReject = () => {
    onClose();
  };

  // 重新生成
  const handleRegenerate = () => {
    setAIResponse('');
    setStage('input');
    setError(null);
    inputRef.current?.focus();
  };

  // 快捷键
  useEffect(() => {
    const handleKeyDown = (e: KeyboardEvent) => {
      // Esc: 关闭
      if (e.key === 'Escape') {
        onClose();
      }
      // Ctrl+Enter: 提交
      if (e.key === 'Enter' && (e.ctrlKey || e.metaKey)) {
        e.preventDefault();
        handleSubmit();
      }
      // Ctrl+Shift+Enter: 应用
      if (e.key === 'Enter' && (e.ctrlKey || e.metaKey) && e.shiftKey) {
        e.preventDefault();
        handleApply();
      }
    };

    window.addEventListener('keydown', handleKeyDown);
    return () => window.removeEventListener('keydown', handleKeyDown);
  }, [input, aiResponse, onClose]);

  return (
    <div
      ref={panelRef}
      className="quick-edit-panel"
      style={{
        position: 'fixed',
        left: `${position.x}px`,
        top: `${position.y}px`,
        zIndex: 9999,
      }}
    >
      {/* Header */}
      <div className="quick-edit-header">
        <h3 className="quick-edit-title">Quick Edit</h3>
        <button onClick={onClose} className="quick-edit-close">
          <X className="w-4 h-4" />
        </button>
      </div>

      {/* Body */}
      <div className="quick-edit-body">
        {/* 选中文字预览 */}
        <div className="quick-edit-selected-text">
          <span className="text-xs text-gray-500">选中文字:</span>
          <p className="text-sm text-gray-700 line-clamp-2">{selectedText}</p>
        </div>

        {/* 输入区 */}
        {(stage === 'input' || stage === 'streaming') && (
          <div className="quick-edit-input-container">
            <textarea
              ref={inputRef}
              value={input}
              onChange={(e) => setInput(e.target.value)}
              placeholder="告诉AI你想做什么... (Ctrl+Enter发送)"
              className="quick-edit-input"
              rows={3}
              disabled={isLoading}
            />
            <button
              onClick={handleSubmit}
              disabled={isLoading || !input.trim()}
              className="quick-edit-submit"
            >
              {isLoading ? (
                <Loader2 className="w-4 h-4 animate-spin" />
              ) : (
                '发送'
              )}
            </button>
          </div>
        )}

        {/* AI响应区 */}
        {(stage === 'streaming' || stage === 'complete') && (
          <div className="quick-edit-response">
            <span className="text-xs text-gray-500">AI响应:</span>
            <div className="quick-edit-response-content">
              {aiResponse}
              {stage === 'streaming' && (
                <span className="quick-edit-cursor">▓</span>
              )}
            </div>
          </div>
        )}

        {/* 错误提示 */}
        {stage === 'error' && error && (
          <div className="quick-edit-error">
            <p>{error}</p>
            <button onClick={handleRegenerate} className="quick-edit-retry">
              <RotateCw className="w-4 h-4" />
              重试
            </button>
          </div>
        )}
      </div>

      {/* Footer */}
      {stage === 'complete' && (
        <div className="quick-edit-footer">
          <button onClick={handleApply} className="quick-edit-apply">
            <Check className="w-4 h-4" />
            应用 (Ctrl+Shift+Enter)
          </button>
          <button onClick={handleReject} className="quick-edit-reject">
            <X className="w-4 h-4" />
            撤销 (Esc)
          </button>
          <button onClick={handleRegenerate} className="quick-edit-regenerate">
            <RotateCw className="w-4 h-4" />
            重新生成
          </button>
        </div>
      )}
    </div>
  );
};
```

---

### 2. BubbleMenu / AIMenu 集成

```typescript
// src/components/editor/BubbleMenu.tsx

import { Sparkles } from 'lucide-react';
import { useEditorStore } from '@/store/editorStore';

const BubbleMenu: React.FC<BubbleMenuProps> = ({ editor }) => {
  const openQuickEdit = useEditorStore((state) => state.openQuickEdit);

  const handleQuickEdit = () => {
    const { from, to } = editor.state.selection;
    const selectedText = editor.state.doc.textBetween(from, to, ' ');

    if (!selectedText.trim()) {
      return;
    }

    // 获取选中文本的DOM位置
    const { view } = editor;
    const start = view.coordsAtPos(from);
    const end = view.coordsAtPos(to);

    // 计算浮动框位置（选中文字下方居中）
    const position = {
      x: (start.left + end.left) / 2,
      y: end.bottom + 10,  // 距离选中文字下方10px
    };

    openQuickEdit(position, selectedText, { from, to });
  };

  return (
    <TiptapBubbleMenu editor={editor}>
      {/* 新增: Quick Edit按钮 */}
      <button
        onClick={handleQuickEdit}
        className="bubble-menu-button quick-edit-button"
        title="Quick Edit (Ctrl+E)"
      >
        <Sparkles className="w-4 h-4 text-purple-500" />
        <span>Quick Edit</span>
      </button>

      {/* 其他按钮... */}
    </TiptapBubbleMenu>
  );
};
```

---

### 3. NovelEditor 集成

```typescript
// src/components/editor/NovelEditor.tsx

import { QuickEditPanel } from './QuickEditPanel';
import { useEditorStore } from '@/store/editorStore';

const NovelEditor: React.FC<NovelEditorProps> = ({ ... }) => {
  const editor = useEditor({ ... });
  const quickEditConfig = useEditorStore((state) => state.quickEditConfig);
  const closeQuickEdit = useEditorStore((state) => state.closeQuickEdit);

  if (!editor) {
    return <div>加载中...</div>;
  }

  return (
    <div className="novel-editor">
      {/* 编辑器内容 */}
      <EditorContent editor={editor} />

      {/* 浮动Quick Edit面板 */}
      {quickEditConfig.open && quickEditConfig.position && (
        <QuickEditPanel
          editor={editor}
          position={quickEditConfig.position}
          selectedText={quickEditConfig.selectedText}
          selectionRange={quickEditConfig.selectionRange!}
          onClose={closeQuickEdit}
        />
      )}
    </div>
  );
};
```

---

## 🎨 样式设计

```css
/* src/components/editor/quick-edit-styles.css */

.quick-edit-panel {
  width: 450px;
  max-width: 90vw;
  background: white;
  border-radius: 12px;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.15);
  border: 1px solid #e5e7eb;
  overflow: hidden;
  animation: quickEditFadeIn 0.2s ease-out;
}

@keyframes quickEditFadeIn {
  from {
    opacity: 0;
    transform: translateY(-10px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.quick-edit-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 12px 16px;
  border-bottom: 1px solid #e5e7eb;
  background: linear-gradient(to right, #f9fafb, #f3f4f6);
}

.quick-edit-title {
  font-size: 14px;
  font-weight: 600;
  color: #374151;
}

.quick-edit-close {
  padding: 4px;
  background: transparent;
  border: none;
  cursor: pointer;
  border-radius: 4px;
  transition: background 0.2s;
}

.quick-edit-close:hover {
  background: #e5e7eb;
}

.quick-edit-body {
  padding: 16px;
  max-height: 400px;
  overflow-y: auto;
}

.quick-edit-selected-text {
  margin-bottom: 12px;
  padding: 8px;
  background: #f9fafb;
  border-radius: 6px;
  border: 1px solid #e5e7eb;
}

.quick-edit-input-container {
  display: flex;
  gap: 8px;
  margin-bottom: 12px;
}

.quick-edit-input {
  flex: 1;
  padding: 10px;
  border: 1px solid #d1d5db;
  border-radius: 6px;
  font-size: 14px;
  resize: none;
  transition: border-color 0.2s;
}

.quick-edit-input:focus {
  outline: none;
  border-color: #8b5cf6;
  box-shadow: 0 0 0 3px rgba(139, 92, 246, 0.1);
}

.quick-edit-submit {
  padding: 10px 16px;
  background: #8b5cf6;
  color: white;
  border: none;
  border-radius: 6px;
  font-size: 14px;
  font-weight: 500;
  cursor: pointer;
  transition: background 0.2s;
}

.quick-edit-submit:hover:not(:disabled) {
  background: #7c3aed;
}

.quick-edit-submit:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.quick-edit-response {
  margin-top: 12px;
  padding: 12px;
  background: #f9fafb;
  border-radius: 6px;
  border: 1px solid #e5e7eb;
}

.quick-edit-response-content {
  margin-top: 8px;
  font-size: 14px;
  line-height: 1.6;
  color: #374151;
  white-space: pre-wrap;
}

.quick-edit-cursor {
  animation: blink 1s infinite;
}

@keyframes blink {
  0%, 49% { opacity: 1; }
  50%, 100% { opacity: 0; }
}

.quick-edit-footer {
  display: flex;
  gap: 8px;
  padding: 12px 16px;
  border-top: 1px solid #e5e7eb;
  background: #f9fafb;
}

.quick-edit-apply {
  flex: 1;
  padding: 8px 12px;
  background: #10b981;
  color: white;
  border: none;
  border-radius: 6px;
  font-size: 13px;
  font-weight: 500;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 6px;
  transition: background 0.2s;
}

.quick-edit-apply:hover {
  background: #059669;
}

.quick-edit-reject {
  padding: 8px 12px;
  background: #ef4444;
  color: white;
  border: none;
  border-radius: 6px;
  font-size: 13px;
  font-weight: 500;
  cursor: pointer;
  display: flex;
  align-items: center;
  gap: 6px;
  transition: background 0.2s;
}

.quick-edit-reject:hover {
  background: #dc2626;
}

.quick-edit-regenerate {
  padding: 8px 12px;
  background: white;
  color: #6b7280;
  border: 1px solid #d1d5db;
  border-radius: 6px;
  font-size: 13px;
  cursor: pointer;
  display: flex;
  align-items: center;
  gap: 6px;
  transition: all 0.2s;
}

.quick-edit-regenerate:hover {
  background: #f9fafb;
  border-color: #9ca3af;
}
```

---

## ⌨️ 快捷键支持

| 快捷键 | 功能 | 状态 |
|--------|------|------|
| `Ctrl/Cmd + E` | 打开Quick Edit | 任何时候 |
| `Esc` | 关闭Quick Edit | Quick Edit打开时 |
| `Ctrl/Cmd + Enter` | 发送提示词 | 输入中 |
| `Ctrl/Cmd + Shift + Enter` | 应用AI建议 | 响应完成时 |
| `Ctrl/Cmd + R` | 重新生成 | 响应完成时 |

---

## 🧪 测试计划

### 功能测试

| 测试场景 | 预期结果 | 优先级 |
|---------|---------|--------|
| 基础打开关闭 | 点击Quick Edit正确弹出/关闭 | P0 |
| 输入提交 | 输入提示词后正确调用AI | P0 |
| 流式响应 | 逐字显示AI内容 | P0 |
| 应用建议 | 正确替换选中文本 | P0 |
| 撤销操作 | 关闭面板，不修改文本 | P0 |
| 重新生成 | 清空响应，重新输入 | P1 |
| 边界溢出 | 浮动框自动翻转和调整 | P1 |
| 长文本 | 支持长选中文本和AI响应 | P1 |
| 错误处理 | API失败时显示错误 | P1 |

---

## 🚀 实施计划

### 第一周：核心组件开发
- [ ] QuickEditPanel组件框架
- [ ] 浮动UI定位逻辑（@floating-ui）
- [ ] 基础样式
- [ ] 状态管理扩展

### 第二周：AI集成与优化
- [ ] AI流式响应集成
- [ ] 应用/撤销逻辑
- [ ] 错误处理
- [ ] 快捷键支持

### 第三周：测试与完善
- [ ] 功能测试
- [ ] 边界情况处理
- [ ] 性能优化
- [ ] 用户体验优化

---

**版本:** v1.0
**日期:** 2025-01-08
**作者:** Claude & 开发团队
