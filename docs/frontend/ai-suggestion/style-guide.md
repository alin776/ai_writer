# 样式规范文档

本文档定义AI建议功能的样式规范和设计系统。

---

## 🎨 颜色系统

### 主题色

#### 待确认（Pending）

```css
--ai-pending-bg: linear-gradient(90deg, rgba(255, 235, 59, 0.2) 0%, rgba(255, 235, 59, 0.1) 100%);
--ai-pending-border: #FFD700;
--ai-pending-shadow: rgba(255, 215, 0, 0.4);
```

**使用场景**: 编辑器中待确认的AI内容

#### 成功（Success）

```css
--ai-success-bg: #10b981;
--ai-success-light: #f0fdf4;
--ai-success-border: #10b981;
```

**使用场景**: 接受按钮、已采纳状态、成功Toast

#### 错误（Error）

```css
--ai-error-bg: #ef4444;
--ai-error-light: #fef2f2;
--ai-error-border: #ef4444;
```

**使用场景**: 拒绝提示、错误Toast

#### 中性（Neutral）

```css
--ai-neutral-50: #f9fafb;
--ai-neutral-100: #f3f4f6;
--ai-neutral-200: #e5e7eb;
--ai-neutral-600: #6b7280;
--ai-neutral-900: #111827;
```

**使用场景**: 卡片背景、边框、文本

---

## 📏 尺寸规范

### 间距系统

```css
--spacing-xs: 4px;
--spacing-sm: 8px;
--spacing-md: 12px;
--spacing-lg: 16px;
--spacing-xl: 20px;
--spacing-2xl: 24px;
```

### 圆角

```css
--radius-sm: 4px;   /* 小元素：tag、badge */
--radius-md: 6px;   /* 按钮 */
--radius-lg: 8px;   /* 卡片 */
--radius-xl: 12px;  /* 对话框 */
--radius-full: 9999px; /* 圆形 */
```

### 阴影

```css
--shadow-sm: 0 1px 2px rgba(0, 0, 0, 0.05);
--shadow-md: 0 4px 6px rgba(0, 0, 0, 0.1);
--shadow-lg: 0 10px 15px rgba(0, 0, 0, 0.1);
--shadow-xl: 0 20px 25px rgba(0, 0, 0, 0.15);
```

---

## 🔤 字体规范

### 字号

```css
--text-xs: 10px;    /* 辅助文本 */
--text-sm: 11px;    /* 次要文本 */
--text-base: 13px;  /* 正文 */
--text-lg: 14px;    /* 标题 */
--text-xl: 16px;    /* 大标题 */
```

### 字重

```css
--font-normal: 400;
--font-medium: 500;
--font-semibold: 600;
--font-bold: 700;
```

### 行高

```css
--leading-tight: 1.25;  /* 紧凑 */
--leading-normal: 1.5;  /* 正常 */
--leading-relaxed: 1.75; /* 宽松 */
```

---

## 🎭 组件样式规范

### AISuggestionCard

```css
.ai-suggestion-card {
  /* 尺寸 */
  min-height: 50px;
  max-width: 400px;
  padding: var(--spacing-md);

  /* 颜色 */
  background: white;
  border: 1px solid var(--ai-neutral-200);

  /* 圆角阴影 */
  border-radius: var(--radius-lg);
  box-shadow: var(--shadow-md);

  /* 过渡 */
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
}

/* 生成中状态 */
.ai-suggestion-card.generating {
  background: var(--ai-neutral-50);
  min-height: 60px;
}

/* 待确认状态 */
.ai-suggestion-card.pending {
  border-color: var(--ai-pending-border);
  background: linear-gradient(135deg, #fffbeb 0%, #ffffff 100%);
}

/* 已采纳状态 */
.ai-suggestion-card.accepted {
  background: var(--ai-success-light);
  border-color: var(--ai-success-border);
}

/* 已拒绝状态 */
.ai-suggestion-card.rejected {
  background: var(--ai-error-light);
  border-color: var(--ai-error-border);
}
```

### 按钮样式

```css
.action-btn {
  /* 尺寸 */
  height: 36px;
  padding: 0 var(--spacing-lg);

  /* 字体 */
  font-size: var(--text-sm);
  font-weight: var(--font-medium);

  /* 圆角 */
  border-radius: var(--radius-md);

  /* 过渡 */
  transition: all 0.2s ease;
  cursor: pointer;
  border: none;
}

/* 接受按钮 */
.accept-btn {
  background: var(--ai-success-bg);
  color: white;
}

.accept-btn:hover {
  background: #059669;
  transform: translateY(-1px);
  box-shadow: var(--shadow-md);
}

/* 拒绝按钮 */
.reject-btn {
  background: var(--ai-neutral-100);
  color: var(--ai-neutral-600);
}

.reject-btn:hover {
  background: var(--ai-neutral-200);
  color: var(--ai-neutral-900);
}
```

### 编辑器待确认内容

```css
.ai-pending-content {
  /* 背景 */
  background: linear-gradient(
    90deg,
    rgba(255, 235, 59, 0.2) 0%,
    rgba(255, 235, 59, 0.1) 100%
  );

  /* 边框 */
  border: 2px dashed var(--ai-pending-border);
  border-radius: var(--radius-sm);

  /* 间距 */
  padding: 4px 6px;
  margin: 0 2px;

  /* 动画 */
  animation: ai-pending-pulse 2s ease-in-out infinite;
}
```

---

## 🎬 动画规范

### 时长

```css
--duration-fast: 150ms;    /* 快速交互 */
--duration-normal: 300ms;  /* 常规过渡 */
--duration-slow: 500ms;    /* 慢速动画 */
```

### 缓动函数

```css
--ease-in: cubic-bezier(0.4, 0, 1, 1);
--ease-out: cubic-bezier(0, 0, 0.2, 1);
--ease-in-out: cubic-bezier(0.4, 0, 0.2, 1);
```

### 标准动画

#### 淡入淡出

```css
@keyframes fade-in {
  from { opacity: 0; }
  to { opacity: 1; }
}

@keyframes fade-out {
  from { opacity: 1; }
  to { opacity: 0; }
}
```

#### 滑入滑出

```css
@keyframes slide-in-up {
  from {
    opacity: 0;
    transform: translateY(10px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

@keyframes slide-out-up {
  from {
    opacity: 1;
    transform: translateY(0);
  }
  to {
    opacity: 0;
    transform: translateY(-10px);
  }
}
```

#### 缩放

```css
@keyframes scale-in {
  from {
    opacity: 0;
    transform: scale(0.95);
  }
  to {
    opacity: 1;
    transform: scale(1);
  }
}
```

#### 旋转

```css
@keyframes spin {
  from { transform: rotate(0deg); }
  to { transform: rotate(360deg); }
}
```

---

## 🌗 深色模式

### 颜色覆盖

```css
@media (prefers-color-scheme: dark) {
  :root {
    /* 中性色反转 */
    --ai-neutral-50: #1f2937;
    --ai-neutral-100: #111827;
    --ai-neutral-900: #f3f4f6;

    /* 待确认色调暗 */
    --ai-pending-bg: linear-gradient(
      90deg,
      rgba(255, 235, 59, 0.15) 0%,
      rgba(255, 235, 59, 0.08) 100%
    );
    --ai-pending-border: #F9A825;
  }

  .ai-suggestion-card {
    background: #1f2937;
    border-color: #374151;
    color: #f3f4f6;
  }

  .ai-pending-content {
    background: var(--ai-pending-bg);
    border-color: var(--ai-pending-border);
  }
}
```

---

## 📱 响应式设计

### 断点

```css
--breakpoint-sm: 640px;   /* 手机 */
--breakpoint-md: 768px;   /* 平板 */
--breakpoint-lg: 1024px;  /* 桌面 */
--breakpoint-xl: 1280px;  /* 大屏 */
```

### 移动端适配

```css
@media (max-width: 768px) {
  .ai-suggestion-card {
    padding: var(--spacing-sm);
    max-width: 100%;
  }

  .action-btn {
    height: 32px;
    padding: 0 var(--spacing-md);
    font-size: var(--text-xs);
  }

  .suggestion-text {
    font-size: var(--text-sm);
  }
}
```

---

## ♿ 无障碍规范

### 对比度

遵循WCAG 2.1 AA标准：
- **正文文本**: 最小对比度 4.5:1
- **大文本**: 最小对比度 3:1
- **UI组件**: 最小对比度 3:1

```css
/* ✅ 良好对比度 */
.good-contrast {
  background: #ffffff;
  color: #111827; /* 对比度 16:1 */
}

/* ❌ 对比度不足 */
.bad-contrast {
  background: #ffffff;
  color: #d1d5db; /* 对比度 1.8:1 */
}
```

### 焦点状态

```css
.action-btn:focus-visible {
  outline: 2px solid #3b82f6;
  outline-offset: 2px;
}

/* 移除默认outline */
.action-btn:focus {
  outline: none;
}
```

### 动画减弱

```css
@media (prefers-reduced-motion: reduce) {
  *,
  *::before,
  *::after {
    animation-duration: 0.01ms !important;
    animation-iteration-count: 1 !important;
    transition-duration: 0.01ms !important;
  }
}
```

---

## 🎯 性能优化

### GPU加速

```css
.ai-pending-content,
.loading-spinner,
.ai-suggestion-card {
  transform: translateZ(0);
  backface-visibility: hidden;
  will-change: transform, opacity;
}
```

### 避免重排

```css
/* ✅ 使用transform代替top/left */
.slide-animation {
  transform: translateY(10px);
}

/* ❌ 避免 */
.bad-animation {
  top: 10px; /* 触发重排 */
}
```

---

## 📐 布局规范

### Flexbox

```css
/* 水平居中 */
.center-h {
  display: flex;
  justify-content: center;
}

/* 垂直居中 */
.center-v {
  display: flex;
  align-items: center;
}

/* 水平垂直居中 */
.center-both {
  display: flex;
  justify-content: center;
  align-items: center;
}

/* 两端对齐 */
.space-between {
  display: flex;
  justify-content: space-between;
}
```

---

## 📝 CSS命名规范

### BEM规范

```css
/* Block（块） */
.ai-suggestion-card {}

/* Element（元素） */
.ai-suggestion-card__content {}
.ai-suggestion-card__actions {}

/* Modifier（修饰符） */
.ai-suggestion-card--pending {}
.ai-suggestion-card--accepted {}
```

### 状态类

```css
.is-active {}
.is-disabled {}
.is-loading {}
.is-hidden {}
```

---

## 🔧 工具类

### 间距

```css
.p-0 { padding: 0; }
.p-1 { padding: 4px; }
.p-2 { padding: 8px; }
.p-3 { padding: 12px; }
.p-4 { padding: 16px; }

.m-0 { margin: 0; }
.m-1 { margin: 4px; }
.m-2 { margin: 8px; }
/* ... */
```

### 文本

```css
.text-xs { font-size: 10px; }
.text-sm { font-size: 11px; }
.text-base { font-size: 13px; }

.font-normal { font-weight: 400; }
.font-medium { font-weight: 500; }
.font-semibold { font-weight: 600; }
```

---

## 📚 相关文档

- [组件Props](./component-props.md)
- [API参考](./api-reference.md)
- [使用示例](./examples.md)
