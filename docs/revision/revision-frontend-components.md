# 修订编辑器章节 - 前端组件实现

> 最后更新: 2026-01-08

## 1. 现有 UI 风格分析

### 1.1 设计规范（基于现有组件）

| 属性 | 规范 | 示例 |
|------|------|------|
| 框架 | Tailwind CSS | 不使用自定义 CSS 类 |
| 背景色 | 白色/深色 | `bg-white dark:bg-slate-800` |
| 边框 | 灰色细边框 | `border border-gray-200 dark:border-slate-700` |
| 圆角 | 胶囊/卡片 | `rounded-full` / `rounded-xl` / `rounded-[10px]` |
| 文字颜色 | 灰色层级 | `text-gray-500` / `text-gray-900 dark:text-white` |
| 字体大小 | 13-14px | `text-[13px]` / `text-[14px]` |
| 图标大小 | 12-14px | `size={12}` / `size={14}` |
| 间距 | 紧凑 | `gap-1.5` / `gap-2` / `px-2.5 py-1` |

### 1.2 现有组件参考

| 组件 | 文件 | 特点 |
|------|------|------|
| StepCard | `StepCard.tsx` | 可折叠步骤，状态图标 |
| OutputCard | `OutputCard.tsx` | 白色卡片，标题栏+内容区 |
| KnowledgeContainer | `KnowledgeContainer.tsx` | 胶囊样式，可展开 |
| CompletionStatus | `CompletionStatus.tsx` | 简单状态显示 |

---

## 2. 组件结构

```
src/components/agent/ExecutionFlow/
├── index.tsx              # 执行轨迹入口 (需修改)
├── RevisionCard.tsx       # 修订胶囊组件 (新增)
├── StepCard.tsx           # 步骤卡片 (已有)
├── KnowledgeContainer.tsx # 知识容器 (已有)
├── OutputCard.tsx         # 输出卡片 (已有)
└── ...
```

---

## 3. RevisionCard 组件设计

### 3.1 组件接口

```typescript
// src/types/agent.ts 新增类型

export type RevisionType = 'append' | 'replace' | 'insert' | 'create' | 'rename';
export type RevisionStatus = 'pending' | 'accepted' | 'discarded';

export interface RevisionFlowData {
  revisionType: RevisionType;
  status: RevisionStatus;
  chapterId?: string;
  chapterTitle?: string;
  contentPreview?: string;      // 内容预览（前50字）
  oldTitle?: string;            // 原标题（rename 类型）
  newTitle?: string;            // 新标题（rename 类型）
  versions?: RewriteVersion[];  // 改写版本（replace 类型）
}

interface RewriteVersion {
  style_name: string;
  reason: string;
  content: string;
}
```

### 3.2 组件实现（Tailwind CSS 风格）

```tsx
// src/components/agent/ExecutionFlow/RevisionCard.tsx

import { useState } from 'react';
import { FilePen, Check, X, ChevronDown, ChevronUp, Loader2 } from 'lucide-react';
import type { RevisionFlowData } from '@/types/agent';

interface RevisionCardProps extends RevisionFlowData {
  onAccept: (selectedVersion?: number) => void;
  onDiscard: () => void;
}

export function RevisionCard({
  revisionType,
  status,
  chapterTitle,
  contentPreview,
  oldTitle,
  newTitle,
  versions,
  onAccept,
  onDiscard
}: RevisionCardProps) {
  const [expanded, setExpanded] = useState(true);
  const [selectedVersion, setSelectedVersion] = useState(0);

  // 获取修订类型的显示文本
  const getRevisionTitle = () => {
    const titles: Record<string, string> = {
      append: '章节续写',
      replace: '文本改写',
      insert: '内容插入',
      create: '新建章节',
      rename: '修改标题'
    };
    return titles[revisionType] || '章节修订';
  };

  // 状态标签样式
  const statusStyles: Record<string, string> = {
    pending: 'bg-amber-100 dark:bg-amber-900/30 text-amber-600 dark:text-amber-400',
    accepted: 'bg-emerald-100 dark:bg-emerald-900/30 text-emerald-600 dark:text-emerald-400',
    discarded: 'bg-gray-100 dark:bg-slate-700 text-gray-500 dark:text-slate-400'
  };

  const statusText: Record<string, string> = {
    pending: '待确认',
    accepted: '已采纳',
    discarded: '已弃用'
  };

  return (
    <div className={`inline-block bg-white dark:bg-slate-800 border border-gray-200 dark:border-slate-700 mb-3 ${
      expanded ? 'rounded-xl px-3 py-2' : 'rounded-full px-2.5 py-1'
    }`}>
      {/* 头部 */}
      <div
        className="flex items-center gap-1.5 cursor-pointer select-none"
        onClick={() => setExpanded(!expanded)}
      >
        <span className="text-gray-500">
          <FilePen size={12} />
        </span>
        <span className="text-[13px] text-gray-500">{getRevisionTitle()}</span>
        <span className="text-gray-400 dark:text-gray-600 text-[9px] ml-0.5">
          {expanded ? <ChevronUp size={10} /> : <ChevronDown size={10} />}
        </span>
        <span className={`text-[10px] px-1.5 py-0.5 rounded-full ml-auto ${statusStyles[status]}`}>
          {statusText[status]}
        </span>
      </div>

      {/* 内容区域 */}
      {expanded && (
        <div className="pt-2">
          {/* 章节信息 */}
          {chapterTitle && (
            <div className="mb-2">
              <span className="text-[13px] text-blue-500 dark:text-[#5c9eff] underline underline-offset-2 cursor-pointer hover:text-blue-600">
                {chapterTitle}
              </span>
            </div>
          )}

          {/* 根据类型显示不同内容 */}
          {revisionType === 'rename' ? (
            // 修改标题
            <div className="space-y-1 mb-3">
              <div className="flex items-center gap-2 text-[13px]">
                <span className="text-gray-500 min-w-[50px]">原标题</span>
                <span className="text-gray-400 line-through">{oldTitle}</span>
              </div>
              <div className="flex items-center gap-2 text-[13px]">
                <span className="text-gray-500 min-w-[50px]">新标题</span>
                <span className="text-emerald-600 dark:text-emerald-400">{newTitle}</span>
              </div>
            </div>
          ) : revisionType === 'replace' && versions ? (
            // 改写 - 多版本选择
            <div className="space-y-1.5 mb-3">
              {versions.map((v, idx) => (
                <label
                  key={idx}
                  className={`flex items-center gap-2 p-2 rounded-lg cursor-pointer transition-colors ${
                    selectedVersion === idx
                      ? 'bg-blue-50 dark:bg-blue-900/20 border border-blue-200 dark:border-blue-800'
                      : 'bg-gray-50 dark:bg-slate-700/50 border border-transparent hover:bg-gray-100 dark:hover:bg-slate-700'
                  }`}
                >
                  <input
                    type="radio"
                    name="version"
                    checked={selectedVersion === idx}
                    onChange={() => setSelectedVersion(idx)}
                    className="w-3.5 h-3.5 text-blue-500"
                  />
                  <span className="text-[13px] text-gray-900 dark:text-white font-medium">{v.style_name}</span>
                  <span className="text-[12px] text-gray-500 dark:text-slate-400">{v.reason}</span>
                </label>
              ))}
            </div>
          ) : (
            // 其他类型 - 内容预览
            contentPreview && (
              <div className="bg-gray-50 dark:bg-slate-700/50 rounded-lg p-2.5 mb-3">
                <div className="text-[11px] text-gray-400 dark:text-slate-500 mb-1">
                  {revisionType === 'create' ? '章节内容预览' : '新增内容预览'}
                </div>
                <div className="text-[13px] text-gray-600 dark:text-slate-300 leading-[1.6] line-clamp-2">
                  "{contentPreview}..."
                </div>
              </div>
            )
          )}

          {/* 操作按钮 */}
          {status === 'pending' ? (
            <div className="flex gap-2">
              <button
                onClick={onDiscard}
                className="flex items-center gap-1 px-2.5 py-1 text-[12px] text-gray-500 dark:text-slate-400 bg-gray-100 dark:bg-slate-700 rounded-full hover:bg-gray-200 dark:hover:bg-slate-600 transition-colors"
              >
                <X size={12} />
                弃用
              </button>
              <button
                onClick={() => onAccept(versions ? selectedVersion : undefined)}
                className="flex items-center gap-1 px-2.5 py-1 text-[12px] text-white bg-blue-500 rounded-full hover:bg-blue-600 transition-colors"
              >
                <Check size={12} />
                采纳
              </button>
            </div>
          ) : (
            <div className={`flex items-center gap-1 text-[12px] ${
              status === 'accepted' ? 'text-emerald-600 dark:text-emerald-400' : 'text-gray-500'
            }`}>
              {status === 'accepted' ? <Check size={12} /> : <X size={12} />}
              {status === 'accepted' ? '修订已采纳' : '修订已弃用'}
            </div>
          )}
        </div>
      )}
    </div>
  );
}
```

---

## 4. ExecutionFlow 集成

### 4.1 修改 FlowItemType

```typescript
// src/types/agent.ts

export type FlowItemType =
  | 'text'
  | 'tool'
  | 'content'
  | 'step'
  | 'output'
  | 'agent_header'
  | 'completion'
  | 'summarization'
  | 'revision';  // 新增
```

### 4.2 修改 index.tsx

```tsx
// src/components/agent/ExecutionFlow/index.tsx

import { RevisionCard } from './RevisionCard';
import type { RevisionFlowData } from '@/types/agent';

export function ExecutionFlow({ items, onApplyContent, onAcceptRevision, onDiscardRevision }: ExecutionFlowProps) {
  return (
    <div>
      {items.map((item) => {
        switch (item.type) {
          // ... 现有 case ...

          case 'revision':
            return (
              <RevisionCard
                key={item.id}
                {...(item.data as RevisionFlowData)}
                onAccept={(selectedVersion) => onAcceptRevision?.(item.id, selectedVersion)}
                onDiscard={() => onDiscardRevision?.(item.id)}
              />
            );

          default:
            return null;
        }
      })}
    </div>
  );
}
```

---

## 5. 编辑器 insert 类型支持

### 5.1 问题描述

当前 `NovelEditor.tsx` 的 `handleShowRevision` 只支持 `modify` 和 `continue` 类型。

**现有代码** (`NovelEditor.tsx:503-628`):
```typescript
const handleShowRevision = (event: Event) => {
  const customEvent = event as CustomEvent<{
    type: 'modify' | 'continue';  // ❌ 缺少 'insert'
    // ...
  }>;

  if (type === 'modify' && position) {
    // ✅ 处理修改
  } else if (type === 'continue') {
    // ✅ 处理续写
  }
  // ❌ 缺少 insert 类型处理
};
```

### 5.2 修复方案

```typescript
// 1. 更新类型定义
const customEvent = event as CustomEvent<{
  type: 'modify' | 'continue' | 'insert';  // 新增 insert
  // ...
}>;

// 2. 在 handleShowRevision 中添加 insert 分支（约 620 行后）
} else if (type === 'insert' && position) {
  // 插入模式：在指定位置插入内容，显示绿色高亮
  console.log('[NovelEditor] 应用插入模式修订标记');

  const insertPos = position.from;

  // 1. 在指定位置插入新内容
  editor.chain()
    .focus()
    .setTextSelection(insertPos)
    .insertContent(replacement || '')
    .run();

  // 2. 对插入的内容应用 aiInserted 标记
  const endPos = insertPos + (replacement?.length || 0);
  editor.chain()
    .setTextSelection({ from: insertPos, to: endPos })
    .setMark('aiInserted')
    .run();

  // 3. 计算操作栏位置
  const { view } = editor;
  const coords = view.coordsAtPos(insertPos);
  setRevisionBarPosition({
    top: coords.bottom + 8,
    left: coords.left
  });

  // 4. 设置活跃修订
  setActiveRevision({
    id: rid,
    type: 'insert',
    position,
    replacement,
    originalMessage,
    context
  });
}
```

### 5.3 修改位置

- 文件: `src/components/editor/NovelEditor.tsx`
- 位置: 约 620 行，在 `else if (type === 'continue')` 分支后添加
