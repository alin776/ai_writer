# Phase 2: Agent卡片UI

## 📋 任务清单

- [ ] 2.1 创建AISuggestionCard组件（⚪旋转动画表示生成中）
- [ ] 2.2 实现卡片展开/收起动画（生成中收起，完成后展开）
- [ ] 2.3 添加操作按钮（✓接受 / ✗拒绝）
- [ ] 2.4 实现确认后状态显示（✅已采纳 / ❌已拒绝）

## 🎯 目标

构建右侧Agent对话框中的建议卡片组件，提供直观的视觉反馈和操作入口。

---

## 📝 Task 2.1: 创建AISuggestionCard组件

### 文件路径
```
src/components/editor/AISuggestionCard.tsx
```

### 组件状态机

```
generating → completed → (accepted | rejected)
    ⚪   →   ✓/✗   →   ✅/❌
```

### 实现代码

```typescript
/**
 * AISuggestionCard - AI建议卡片组件
 * 显示在Agent对话框中，提供确认/拒绝操作
 */
import React, { useState, useEffect } from 'react';
import { Check, X, Loader2 } from 'lucide-react';
import type { AISuggestion } from '@/types/ai-suggestion';
import './AISuggestionCard.css';

export interface AISuggestionCardProps {
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

export const AISuggestionCard: React.FC<AISuggestionCardProps> = ({
  suggestion,
  isGenerating = false,
  onAccept,
  onReject,
  className = '',
}) => {
  const [isExpanded, setIsExpanded] = useState(false);
  const [localStatus, setLocalStatus] = useState(suggestion.status);

  // 生成完成后自动展开
  useEffect(() => {
    if (!isGenerating && suggestion.content) {
      setIsExpanded(true);
    }
  }, [isGenerating, suggestion.content]);

  // 生成中状态：收起显示旋转圆圈
  if (isGenerating) {
    return (
      <div className={`ai-suggestion-card generating ${className}`}>
        <div className="card-generating">
          <Loader2 className="loading-spinner" />
          <span className="generating-text">生成中...</span>
        </div>
      </div>
    );
  }

  // 已确认状态：简洁提示
  if (localStatus === 'accepted') {
    return (
      <div className={`ai-suggestion-card accepted ${className}`}>
        <div className="card-status">
          <Check className="status-icon success" />
          <span className="status-text">已采纳</span>
        </div>
      </div>
    );
  }

  // 已拒绝状态：简洁提示
  if (localStatus === 'rejected') {
    return (
      <div className={`ai-suggestion-card rejected ${className}`}>
        <div className="card-status">
          <X className="status-icon error" />
          <span className="status-text">已拒绝</span>
        </div>
      </div>
    );
  }

  // 待确认状态：展示内容和操作按钮
  return (
    <div className={`ai-suggestion-card pending ${className} ${isExpanded ? 'expanded' : ''}`}>
      {/* 内容区域 */}
      <div className="card-content">
        <p className="suggestion-text">{suggestion.content}</p>
      </div>

      {/* 操作按钮 */}
      <div className="card-actions">
        <button
          className="action-btn accept-btn"
          onClick={() => {
            setLocalStatus('accepted');
            onAccept();
          }}
          title="接受建议 (Tab)"
        >
          <Check className="btn-icon" />
          <span>接受</span>
        </button>
        <button
          className="action-btn reject-btn"
          onClick={() => {
            setLocalStatus('rejected');
            onReject();
          }}
          title="拒绝建议 (Esc)"
        >
          <X className="btn-icon" />
          <span>拒绝</span>
        </button>
      </div>
    </div>
  );
};
```

---

## 📝 Task 2.2: 实现卡片动画

### 文件路径
```
src/components/editor/AISuggestionCard.css
```

### 实现代码

```css
/**
 * AISuggestionCard 样式
 */

/* 基础卡片样式 */
.ai-suggestion-card {
  background: #ffffff;
  border: 1px solid #e5e7eb;
  border-radius: 8px;
  padding: 12px;
  margin-bottom: 12px;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
}

/* ==================== 生成中状态 ==================== */
.ai-suggestion-card.generating {
  min-height: 60px;
  display: flex;
  align-items: center;
  justify-content: center;
  background: #f9fafb;
  animation: card-pulse 2s ease-in-out infinite;
}

.card-generating {
  display: flex;
  align-items: center;
  gap: 8px;
  color: #6b7280;
}

.loading-spinner {
  width: 20px;
  height: 20px;
  animation: spin 1s linear infinite;
}

.generating-text {
  font-size: 13px;
  font-weight: 500;
}

/* 旋转动画 */
@keyframes spin {
  from {
    transform: rotate(0deg);
  }
  to {
    transform: rotate(360deg);
  }
}

/* 脉动动画 */
@keyframes card-pulse {
  0%, 100% {
    opacity: 1;
  }
  50% {
    opacity: 0.8;
  }
}

/* ==================== 待确认状态 ==================== */
.ai-suggestion-card.pending {
  border-color: #fbbf24;
  background: linear-gradient(
    135deg,
    #fffbeb 0%,
    #ffffff 100%
  );
  max-height: 80px;
  overflow: hidden;
}

.ai-suggestion-card.pending.expanded {
  max-height: 500px;
  animation: expand-card 0.3s ease-out;
}

@keyframes expand-card {
  from {
    max-height: 80px;
    opacity: 0.8;
  }
  to {
    max-height: 500px;
    opacity: 1;
  }
}

/* 内容区域 */
.card-content {
  margin-bottom: 12px;
}

.suggestion-text {
  font-size: 13px;
  line-height: 1.6;
  color: #374151;
  margin: 0;
  word-wrap: break-word;
}

/* 操作按钮区域 */
.card-actions {
  display: flex;
  gap: 8px;
  padding-top: 8px;
  border-top: 1px solid #e5e7eb;
}

.action-btn {
  flex: 1;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 6px;
  padding: 8px 16px;
  font-size: 13px;
  font-weight: 500;
  border: none;
  border-radius: 6px;
  cursor: pointer;
  transition: all 0.2s ease;
}

.action-btn:hover {
  transform: translateY(-1px);
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.action-btn:active {
  transform: translateY(0);
}

.btn-icon {
  width: 16px;
  height: 16px;
}

/* 接受按钮 */
.accept-btn {
  background: #10b981;
  color: white;
}

.accept-btn:hover {
  background: #059669;
}

/* 拒绝按钮 */
.reject-btn {
  background: #f3f4f6;
  color: #6b7280;
}

.reject-btn:hover {
  background: #e5e7eb;
  color: #374151;
}

/* ==================== 已确认/已拒绝状态 ==================== */
.ai-suggestion-card.accepted,
.ai-suggestion-card.rejected {
  min-height: 50px;
  display: flex;
  align-items: center;
  justify-content: center;
  animation: fade-in 0.3s ease-out;
}

.ai-suggestion-card.accepted {
  background: #f0fdf4;
  border-color: #10b981;
}

.ai-suggestion-card.rejected {
  background: #fef2f2;
  border-color: #ef4444;
}

.card-status {
  display: flex;
  align-items: center;
  gap: 8px;
}

.status-icon {
  width: 20px;
  height: 20px;
}

.status-icon.success {
  color: #10b981;
}

.status-icon.error {
  color: #ef4444;
}

.status-text {
  font-size: 13px;
  font-weight: 600;
}

@keyframes fade-in {
  from {
    opacity: 0;
    transform: scale(0.95);
  }
  to {
    opacity: 1;
    transform: scale(1);
  }
}

/* ==================== 深色模式 ==================== */
@media (prefers-color-scheme: dark) {
  .ai-suggestion-card {
    background: #1f2937;
    border-color: #374151;
  }

  .ai-suggestion-card.generating {
    background: #111827;
  }

  .card-generating {
    color: #9ca3af;
  }

  .ai-suggestion-card.pending {
    border-color: #f59e0b;
    background: linear-gradient(
      135deg,
      #1f2937 0%,
      #111827 100%
    );
  }

  .suggestion-text {
    color: #d1d5db;
  }

  .card-actions {
    border-top-color: #374151;
  }

  .reject-btn {
    background: #374151;
    color: #d1d5db;
  }

  .reject-btn:hover {
    background: #4b5563;
  }

  .ai-suggestion-card.accepted {
    background: #064e3b;
    border-color: #10b981;
  }

  .ai-suggestion-card.rejected {
    background: #7f1d1d;
    border-color: #ef4444;
  }
}

/* ==================== 响应式 ==================== */
@media (max-width: 768px) {
  .ai-suggestion-card {
    padding: 10px;
  }

  .action-btn {
    padding: 6px 12px;
    font-size: 12px;
  }

  .btn-icon {
    width: 14px;
    height: 14px;
  }
}
```

---

## 📝 Task 2.3 & 2.4: 集成到AIPanel

### 修改AIPanel组件

```typescript
// src/components/editor/AIPanel.tsx
import { AISuggestionCard } from './AISuggestionCard';
import { useContext } from 'react';
import { EditorContext } from '@/views/EditorView/EditorContext';

export function AIPanel({ workId, chapterId }: AIPanelProps) {
  const { editor, aiSuggestion } = useContext(EditorContext);

  return (
    <div className="ai-panel">
      {/* 其他消息... */}

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
  );
}
```

---

## ✅ 验收标准

### 2.1 组件创建
- [ ] 组件正确渲染三种状态（生成中/待确认/已确认）
- [ ] TypeScript类型定义完整
- [ ] Props传递正确

### 2.2 动画效果
- [ ] ⚪旋转动画流畅
- [ ] 卡片展开动画自然
- [ ] 状态切换有过渡效果

### 2.3 操作按钮
- [ ] ✓按钮点击触发onAccept
- [ ] ✗按钮点击触发onReject
- [ ] 按钮有悬停效果
- [ ] 按钮title提示正确

### 2.4 状态显示
- [ ] ✅状态正确显示
- [ ] ❌状态正确显示
- [ ] 状态切换无闪烁

---

## 🎨 设计规范

### 颜色系统

| 状态 | 背景色 | 边框色 | 文字色 |
|------|--------|--------|--------|
| 生成中 | `#f9fafb` | `#e5e7eb` | `#6b7280` |
| 待确认 | `#fffbeb` | `#fbbf24` | `#374151` |
| 已采纳 | `#f0fdf4` | `#10b981` | `#10b981` |
| 已拒绝 | `#fef2f2` | `#ef4444` | `#ef4444` |

### 尺寸规范

- 卡片最小高度：50px
- 卡片最大高度：500px
- 圆角：8px
- 内边距：12px
- 按钮高度：36px
- 图标尺寸：16px-20px

### 动画时长

- 展开动画：0.3s
- 旋转动画：1s
- 脉动动画：2s
- 淡入动画：0.3s

---

## 🐛 常见问题

### Q1: 卡片没有自动展开？
**A**: 检查useEffect依赖：
```typescript
useEffect(() => {
  if (!isGenerating && suggestion.content) {
    setIsExpanded(true);
  }
}, [isGenerating, suggestion.content]); // 确保依赖完整
```

### Q2: 按钮点击无反应？
**A**: 检查Props是否正确传递：
```typescript
<AISuggestionCard
  onAccept={() => console.log('Accept clicked')} // 调试
  onReject={() => console.log('Reject clicked')}
/>
```

### Q3: 深色模式样式异常？
**A**: 确保媒体查询正确：
```css
@media (prefers-color-scheme: dark) {
  /* 深色样式 */
}
```

---

## 📚 相关文档

- [状态管理](./02-state-management.md)
- [编辑器同步](./04-editor-sync.md)
- [样式规范](./style-guide.md)
