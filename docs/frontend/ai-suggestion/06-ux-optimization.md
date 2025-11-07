# Phase 6: UX优化与细节完善

## 📋 任务清单

- [ ] 6.1 添加键盘快捷键（Tab=✓, Esc=✗）
- [ ] 6.2 优化动画效果（⚪旋转→卡片展开→✅/❌反馈）
- [ ] 6.3 添加Toast反馈（✅内容已采纳 / ❌内容已拒绝）

## 🎯 目标

提升用户体验，增加键盘快捷键支持，优化动画效果，添加视觉反馈。

---

## 📝 Task 6.1: 键盘快捷键

### 实现全局快捷键Hook

```typescript
// src/hooks/useKeyboardShortcuts.ts

import { useEffect, useCallback } from 'react';

export interface KeyboardShortcut {
  key: string;
  ctrl?: boolean;
  shift?: boolean;
  alt?: boolean;
  handler: (event: KeyboardEvent) => void;
  description?: string;
}

export const useKeyboardShortcuts = (shortcuts: KeyboardShortcut[]) => {
  const handleKeyDown = useCallback((event: KeyboardEvent) => {
    for (const shortcut of shortcuts) {
      const keyMatch = event.key === shortcut.key;
      const ctrlMatch = shortcut.ctrl ? event.ctrlKey || event.metaKey : !event.ctrlKey && !event.metaKey;
      const shiftMatch = shortcut.shift ? event.shiftKey : !event.shiftKey;
      const altMatch = shortcut.alt ? event.altKey : !event.altKey;

      if (keyMatch && ctrlMatch && shiftMatch && altMatch) {
        event.preventDefault();
        shortcut.handler(event);
        break;
      }
    }
  }, [shortcuts]);

  useEffect(() => {
    window.addEventListener('keydown', handleKeyDown);
    return () => window.removeEventListener('keydown', handleKeyDown);
  }, [handleKeyDown]);
};
```

### 在EditorView中使用

```typescript
// src/views/EditorView/index.tsx

import { useKeyboardShortcuts } from '@/hooks/useKeyboardShortcuts';
import { useEditorContext } from './EditorContext';

const EditorView: React.FC = () => {
  const { aiSuggestion } = useEditorContext();

  // 定义快捷键
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

  // ... 其他代码
};
```

### 显示快捷键提示

```typescript
// src/components/editor/KeyboardShortcutHint.tsx

import React from 'react';
import './KeyboardShortcutHint.css';

export const KeyboardShortcutHint: React.FC = () => {
  return (
    <div className="keyboard-hint">
      <div className="hint-item">
        <kbd>Tab</kbd>
        <span>接受</span>
      </div>
      <div className="hint-item">
        <kbd>Esc</kbd>
        <span>拒绝</span>
      </div>
    </div>
  );
};
```

### 快捷键提示样式

```css
/* src/components/editor/KeyboardShortcutHint.css */

.keyboard-hint {
  position: fixed;
  bottom: 20px;
  right: 20px;
  display: flex;
  gap: 12px;
  padding: 8px 12px;
  background: rgba(0, 0, 0, 0.8);
  border-radius: 8px;
  backdrop-filter: blur(10px);
  animation: hint-fade-in 0.3s ease-out;
  z-index: 9999;
}

.hint-item {
  display: flex;
  align-items: center;
  gap: 6px;
  color: white;
  font-size: 12px;
}

kbd {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  min-width: 24px;
  padding: 2px 6px;
  background: rgba(255, 255, 255, 0.2);
  border: 1px solid rgba(255, 255, 255, 0.3);
  border-radius: 4px;
  font-family: monospace;
  font-size: 11px;
  font-weight: 600;
  color: white;
}

@keyframes hint-fade-in {
  from {
    opacity: 0;
    transform: translateY(10px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

/* 仅在有建议时显示 */
.keyboard-hint[data-hidden="true"] {
  display: none;
}
```

### 集成到EditorView

```typescript
const EditorView: React.FC = () => {
  const { aiSuggestion } = useEditorContext();

  return (
    <div className={styles.page}>
      {/* ... 其他内容 */}

      {/* 快捷键提示 */}
      {aiSuggestion.currentSuggestion && <KeyboardShortcutHint />}
    </div>
  );
};
```

---

## 📝 Task 6.2: 优化动画效果

### 完整动画CSS

```css
/* src/components/editor/ai-suggestion-animations.css */

/**
 * AI建议动画效果集合
 */

/* ==================== 生成中动画 ==================== */

/* 旋转圆圈 */
@keyframes spin {
  0% {
    transform: rotate(0deg);
  }
  100% {
    transform: rotate(360deg);
  }
}

.loading-spinner {
  animation: spin 1s linear infinite;
}

/* 脉动效果 */
@keyframes pulse {
  0%, 100% {
    opacity: 1;
    transform: scale(1);
  }
  50% {
    opacity: 0.8;
    transform: scale(0.98);
  }
}

.ai-suggestion-card.generating {
  animation: pulse 2s ease-in-out infinite;
}

/* ==================== 卡片展开动画 ==================== */

@keyframes expand-height {
  from {
    max-height: 80px;
    opacity: 0.8;
  }
  to {
    max-height: 500px;
    opacity: 1;
  }
}

@keyframes expand-fade {
  from {
    opacity: 0;
    transform: translateY(-10px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.ai-suggestion-card.pending.expanded {
  animation: expand-height 0.4s cubic-bezier(0.4, 0, 0.2, 1);
}

.ai-suggestion-card.pending.expanded .card-content {
  animation: expand-fade 0.3s ease-out 0.1s both;
}

.ai-suggestion-card.pending.expanded .card-actions {
  animation: expand-fade 0.3s ease-out 0.2s both;
}

/* ==================== 接受动画 ==================== */

/* 编辑器中的接受闪烁 */
@keyframes accept-flash {
  0% {
    background: rgba(16, 185, 129, 0.4);
    border-color: #10b981;
    box-shadow: 0 0 20px rgba(16, 185, 129, 0.5);
  }
  100% {
    background: transparent;
    border-color: transparent;
    box-shadow: none;
  }
}

.ai-pending-accepting {
  animation: accept-flash 0.4s ease-out forwards;
}

/* 卡片接受动画 */
@keyframes card-accept {
  0% {
    opacity: 1;
    transform: scale(1);
  }
  50% {
    opacity: 0.8;
    transform: scale(1.05);
  }
  100% {
    opacity: 1;
    transform: scale(1);
  }
}

.ai-suggestion-card.accepted {
  animation: card-accept 0.5s ease-out;
}

/* ==================== 拒绝动画 ==================== */

/* 编辑器中的拒绝淡出 */
@keyframes reject-fade {
  0% {
    opacity: 1;
    background: rgba(239, 68, 68, 0.2);
    border-color: #ef4444;
    transform: scale(1);
  }
  50% {
    background: rgba(239, 68, 68, 0.3);
    transform: scale(0.98);
  }
  100% {
    opacity: 0;
    background: rgba(239, 68, 68, 0);
    border-color: transparent;
    transform: scale(0.95);
  }
}

.ai-pending-rejecting {
  animation: reject-fade 0.4s ease-out forwards;
}

/* 卡片拒绝动画 */
@keyframes card-reject {
  0% {
    opacity: 1;
    transform: translateX(0) rotate(0deg);
  }
  50% {
    opacity: 0.5;
    transform: translateX(-10px) rotate(-2deg);
  }
  100% {
    opacity: 1;
    transform: translateX(0) rotate(0deg);
  }
}

.ai-suggestion-card.rejected {
  animation: card-reject 0.5s ease-out;
}

/* ==================== 悬停动画 ==================== */

.action-btn {
  transition: all 0.2s cubic-bezier(0.4, 0, 0.2, 1);
}

.action-btn:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
}

.action-btn:active {
  transform: translateY(0);
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

/* ==================== 按钮波纹效果 ==================== */

@keyframes ripple {
  0% {
    transform: scale(0);
    opacity: 0.8;
  }
  100% {
    transform: scale(2);
    opacity: 0;
  }
}

.action-btn::after {
  content: '';
  position: absolute;
  top: 50%;
  left: 50%;
  width: 100%;
  height: 100%;
  background: rgba(255, 255, 255, 0.5);
  border-radius: 50%;
  transform: translate(-50%, -50%) scale(0);
  pointer-events: none;
}

.action-btn:active::after {
  animation: ripple 0.6s ease-out;
}

/* ==================== Toast动画 ==================== */

@keyframes toast-slide-in {
  from {
    opacity: 0;
    transform: translateY(-20px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

@keyframes toast-slide-out {
  from {
    opacity: 1;
    transform: translateY(0);
  }
  to {
    opacity: 0;
    transform: translateY(-20px);
  }
}

.toast-message {
  animation: toast-slide-in 0.3s ease-out;
}

.toast-message.exiting {
  animation: toast-slide-out 0.3s ease-in;
}

/* ==================== 性能优化 ==================== */

/* 使用will-change提示浏览器优化 */
.ai-suggestion-card,
.action-btn,
.ai-pending-content {
  will-change: transform, opacity;
}

/* 使用GPU加速 */
.loading-spinner,
.ai-pending-accepting,
.ai-pending-rejecting {
  transform: translateZ(0);
  backface-visibility: hidden;
}
```

---

## 📝 Task 6.3: Toast反馈

### 创建Toast组件

```typescript
// src/components/ui/Toast.tsx

import React, { useEffect, useState } from 'react';
import { Check, X, Info, AlertTriangle } from 'lucide-react';
import './Toast.css';

export type ToastType = 'success' | 'error' | 'info' | 'warning';

export interface ToastMessage {
  id: string;
  type: ToastType;
  message: string;
  duration?: number;
}

interface ToastProps {
  message: ToastMessage;
  onClose: (id: string) => void;
}

const iconMap = {
  success: Check,
  error: X,
  info: Info,
  warning: AlertTriangle,
};

export const Toast: React.FC<ToastProps> = ({ message, onClose }) => {
  const [isExiting, setIsExiting] = useState(false);
  const Icon = iconMap[message.type];

  useEffect(() => {
    const timer = setTimeout(() => {
      setIsExiting(true);
      setTimeout(() => onClose(message.id), 300); // 等待退出动画
    }, message.duration || 3000);

    return () => clearTimeout(timer);
  }, [message, onClose]);

  return (
    <div className={`toast-message toast-${message.type} ${isExiting ? 'exiting' : ''}`}>
      <Icon className="toast-icon" />
      <span className="toast-text">{message.message}</span>
    </div>
  );
};

export const ToastContainer: React.FC<{ messages: ToastMessage[]; onClose: (id: string) => void }> = ({
  messages,
  onClose,
}) => {
  return (
    <div className="toast-container">
      {messages.map((message) => (
        <Toast key={message.id} message={message} onClose={onClose} />
      ))}
    </div>
  );
};
```

### Toast样式

```css
/* src/components/ui/Toast.css */

.toast-container {
  position: fixed;
  top: 20px;
  right: 20px;
  display: flex;
  flex-direction: column;
  gap: 12px;
  z-index: 10000;
  pointer-events: none;
}

.toast-message {
  display: flex;
  align-items: center;
  gap: 10px;
  padding: 12px 16px;
  background: white;
  border-radius: 8px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
  border-left: 4px solid;
  min-width: 250px;
  max-width: 400px;
  pointer-events: auto;
  animation: toast-slide-in 0.3s ease-out;
}

.toast-message.exiting {
  animation: toast-slide-out 0.3s ease-in;
}

.toast-icon {
  width: 20px;
  height: 20px;
  flex-shrink: 0;
}

.toast-text {
  flex: 1;
  font-size: 14px;
  font-weight: 500;
  line-height: 1.4;
}

/* Success */
.toast-success {
  border-left-color: #10b981;
}

.toast-success .toast-icon {
  color: #10b981;
}

/* Error */
.toast-error {
  border-left-color: #ef4444;
}

.toast-error .toast-icon {
  color: #ef4444;
}

/* Info */
.toast-info {
  border-left-color: #3b82f6;
}

.toast-info .toast-icon {
  color: #3b82f6;
}

/* Warning */
.toast-warning {
  border-left-color: #f59e0b;
}

.toast-warning .toast-icon {
  color: #f59e0b;
}

/* 深色模式 */
@media (prefers-color-scheme: dark) {
  .toast-message {
    background: #1f2937;
    color: #f3f4f6;
  }
}
```

### 创建useToast Hook

```typescript
// src/hooks/useToast.ts

import { useState, useCallback } from 'react';
import type { ToastMessage, ToastType } from '@/components/ui/Toast';

export const useToast = () => {
  const [messages, setMessages] = useState<ToastMessage[]>([]);

  const show = useCallback((type: ToastType, message: string, duration?: number) => {
    const id = `toast-${Date.now()}`;
    const newMessage: ToastMessage = {
      id,
      type,
      message,
      duration,
    };

    setMessages((prev) => [...prev, newMessage]);
  }, []);

  const close = useCallback((id: string) => {
    setMessages((prev) => prev.filter((msg) => msg.id !== id));
  }, []);

  return {
    messages,
    show,
    close,
    success: (message: string, duration?: number) => show('success', message, duration),
    error: (message: string, duration?: number) => show('error', message, duration),
    info: (message: string, duration?: number) => show('info', message, duration),
    warning: (message: string, duration?: number) => show('warning', message, duration),
  };
};
```

### 集成Toast到EditorContext

```typescript
// src/views/EditorView/EditorContext.tsx

import { useToast } from '@/hooks/useToast';
import { ToastContainer } from '@/components/ui/Toast';

export const EditorProvider: React.FC<{ children: React.ReactNode }> = ({ children }) => {
  const [editor, setEditor] = useState<Editor | null>(null);
  const toast = useToast();

  const aiSuggestion = useAISuggestion(editor, {
    onAccept: () => {
      toast.success('✅ 内容已采纳');
    },
    onReject: () => {
      toast.info('❌ 内容已拒绝');
    },
  });

  return (
    <EditorContext.Provider value={{ editor, aiSuggestion, setEditor }}>
      {children}
      <ToastContainer messages={toast.messages} onClose={toast.close} />
    </EditorContext.Provider>
  );
};
```

---

## ✅ 验收标准

### 6.1 键盘快捷键
- [ ] Tab键正确触发接受
- [ ] Esc键正确触发拒绝
- [ ] 无建议时快捷键不生效
- [ ] 快捷键提示显示正确

### 6.2 动画效果
- [ ] 旋转动画流畅
- [ ] 卡片展开自然
- [ ] 接受/拒绝动画顺滑
- [ ] 无卡顿和闪烁

### 6.3 Toast反馈
- [ ] Toast正确显示
- [ ] 自动消失
- [ ] 支持多条堆叠
- [ ] 动画流畅

---

## 🎨 UX细节清单

### 视觉反馈
- [x] 生成中显示旋转圆圈
- [x] 卡片展开有过渡动画
- [x] 接受时绿色闪烁
- [x] 拒绝时红色淡出
- [x] Toast提示及时

### 交互反馈
- [x] 按钮悬停效果
- [x] 按钮点击反馈
- [x] 键盘快捷键支持
- [x] 快捷键提示显示

### 性能优化
- [x] 使用GPU加速
- [x] will-change优化
- [x] 避免layout thrashing
- [x] 批处理DOM操作

---

## 📚 相关文档

- [交互实现](./05-interaction-integration.md)
- [样式规范](./style-guide.md)
- [API参考](./api-reference.md)
