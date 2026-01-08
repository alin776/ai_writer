# 修订编辑器章节 - 前端组件实现

## 1. 组件结构

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

## 2. RevisionCard 组件设计

### 2.1 组件接口

```typescript
// RevisionCard.tsx

interface RevisionCardProps {
  revisionType: RevisionType;  // append | replace | insert | create | rename
  status: RevisionStatus;      // pending | accepted | discarded
  chapterId?: string;
  chapterTitle?: string;
  contentPreview?: string;
  oldTitle?: string;
  newTitle?: string;
  versions?: RewriteVersion[];
  onAccept: (selectedVersion?: number) => void;
  onDiscard: () => void;
}

type RevisionType = 'append' | 'replace' | 'insert' | 'create' | 'rename';
type RevisionStatus = 'pending' | 'accepted' | 'discarded';

interface RewriteVersion {
  style_name: string;
  reason: string;
  content: string;
}
```

### 2.2 组件实现

```tsx
import { useState } from 'react';
import { FilePen, Check, X, ChevronDown, ChevronUp } from 'lucide-react';

export function RevisionCard({
  revisionType,
  status,
  chapterId,
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
    switch (revisionType) {
      case 'append': return '章节续写';
      case 'replace': return '文本改写';
      case 'insert': return '内容插入';
      case 'create': return '新建章节';
      case 'rename': return '修改标题';
      default: return '章节修订';
    }
  };

  // 获取状态标签样式
  const getStatusBadge = () => {
    switch (status) {
      case 'pending':
        return <span className="revision-badge pending">待确认</span>;
      case 'accepted':
        return <span className="revision-badge accepted">已采纳</span>;
      case 'discarded':
        return <span className="revision-badge discarded">已弃用</span>;
    }
  };

  return (
    <div className="revision-capsule">
      {/* 头部 */}
      <div className="revision-header" onClick={() => setExpanded(!expanded)}>
        <span className="revision-icon">
          <FilePen size={12} />
        </span>
        <span className="revision-title">{getRevisionTitle()}</span>
        <span className="revision-toggle">
          {expanded ? <ChevronUp size={9} /> : <ChevronDown size={9} />}
        </span>
        {getStatusBadge()}
      </div>

      {/* 内容区域 */}
      {expanded && (
        <div className="revision-content">
          {/* 章节信息 */}
          {chapterTitle && (
            <div className="revision-target">
              <span className="target-name">{chapterTitle}</span>
            </div>
          )}

          {/* 根据类型显示不同内容 */}
          {revisionType === 'rename' ? (
            // 修改标题
            <div className="revision-rename">
              <div className="rename-row">
                <span className="rename-label">原标题:</span>
                <span className="rename-value old">{oldTitle}</span>
              </div>
              <div className="rename-row">
                <span className="rename-label">新标题:</span>
                <span className="rename-value new">{newTitle}</span>
              </div>
            </div>
          ) : revisionType === 'replace' && versions ? (
            // 改写 - 多版本选择
            <div className="revision-versions">
              {versions.map((v, idx) => (
                <label key={idx} className="version-option">
                  <input
                    type="radio"
                    name="version"
                    checked={selectedVersion === idx}
                    onChange={() => setSelectedVersion(idx)}
                  />
                  <span className="version-name">{v.style_name}</span>
                  <span className="version-reason">{v.reason}</span>
                </label>
              ))}
            </div>
          ) : (
            // 其他类型 - 内容预览
            <div className="revision-preview">
              <div className="preview-label">
                {revisionType === 'create' ? '章节内容预览：' : '新增内容预览：'}
              </div>
              <div className="preview-text">
                {contentPreview ? `"${contentPreview}..."` : '(无内容)'}
              </div>
            </div>
          )}

          {/* 操作按钮 */}
          {status === 'pending' ? (
            <div className="revision-actions">
              <button className="revision-btn discard" onClick={onDiscard}>
                <X size={12} />
                弃用
              </button>
              <button
                className="revision-btn accept"
                onClick={() => onAccept(versions ? selectedVersion : undefined)}
              >
                <Check size={12} />
                采纳
              </button>
            </div>
          ) : (
            <div className="revision-result">
              {status === 'accepted' ? (
                <>
                  <Check size={12} />
                  修订已采纳
                </>
              ) : (
                <>
                  <X size={12} />
                  修订已弃用
                </>
              )}
            </div>
          )}
        </div>
      )}
    </div>
  );
}
```

---

## 3. 样式定义

```css
/* RevisionCard.css 或在全局样式中 */

.revision-capsule {
  background: #2a2a2a;
  border: 1px solid #3a3a3a;
  border-radius: 16px;
  padding: 4px 10px;
  display: inline-block;
  margin: 8px 0;
}

.revision-header {
  display: flex;
  align-items: center;
  gap: 6px;
  cursor: pointer;
  user-select: none;
}

.revision-icon {
  color: #888;
  display: flex;
  align-items: center;
}

.revision-title {
  font-size: 13px;
  color: #888;
}

.revision-toggle {
  color: #666;
  font-size: 9px;
  margin-left: 2px;
}

.revision-badge {
  font-size: 10px;
  padding: 2px 8px;
  border-radius: 10px;
  margin-left: auto;
}

.revision-badge.pending {
  background: #3a3a3a;
  color: #888;
}

.revision-badge.accepted {
  background: #3a3a3a;
  color: #10b981;
}

.revision-badge.discarded {
  background: #3a3a3a;
  color: #888;
}

.revision-content {
  padding-top: 6px;
}

.revision-target {
  margin-bottom: 6px;
}

.target-name {
  font-size: 13px;
  color: #5c9eff;
  text-decoration: underline;
  cursor: pointer;
}

.revision-preview {
  background: #222;
  border-radius: 8px;
  padding: 8px 10px;
  margin-bottom: 8px;
}

.preview-label {
  font-size: 10px;
  color: #666;
  margin-bottom: 3px;
}

.preview-text {
  font-size: 12px;
  color: #888;
  line-height: 1.5;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

.revision-actions {
  display: flex;
  gap: 6px;
}

.revision-btn {
  display: flex;
  align-items: center;
  gap: 4px;
  padding: 4px 10px;
  border: none;
  border-radius: 12px;
  font-size: 11px;
  cursor: pointer;
  transition: all 0.15s;
}

.revision-btn.discard {
  background: #3a3a3a;
  color: #ccc;
}

.revision-btn.accept {
  background: #3a3a3a;
  color: #ccc;
}

.revision-btn:hover {
  background: #4a4a4a;
}

.revision-result {
  font-size: 11px;
  padding: 4px 0;
  display: flex;
  align-items: center;
  gap: 4px;
  color: #888;
}

/* 改写版本选择 */
.revision-versions {
  margin-bottom: 8px;
}

.version-option {
  display: flex;
  align-items: center;
  gap: 6px;
  padding: 4px 0;
  cursor: pointer;
}

.version-name {
  font-size: 12px;
  color: #ccc;
}

.version-reason {
  font-size: 11px;
  color: #666;
}

/* 修改标题 */
.revision-rename {
  margin-bottom: 8px;
}

.rename-row {
  display: flex;
  gap: 8px;
  padding: 2px 0;
}

.rename-label {
  font-size: 11px;
  color: #666;
  min-width: 50px;
}

.rename-value {
  font-size: 12px;
}

.rename-value.old {
  color: #888;
  text-decoration: line-through;
}

.rename-value.new {
  color: #10b981;
}
```

---

## 4. ExecutionFlow 集成

### 4.1 修改 index.tsx

```tsx
// src/components/agent/ExecutionFlow/index.tsx

import { RevisionCard } from './RevisionCard';
import type { RevisionFlowData } from '@/types/agent';

export function ExecutionFlow({ items, onApplyContent }: ExecutionFlowProps) {
  // ... 现有代码 ...

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
                onAccept={(selectedVersion) => {
                  // 调用 submitApproval
                }}
                onDiscard={() => {
                  // 调用 submitApproval(false)
                }}
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

## 5. 与 useAgentChat 集成

```tsx
// 在 ExecutionFlow 中使用

import { useAgentChat } from '@/hooks/useAgentChat';

function ExecutionFlowContainer() {
  const { flowItems, pendingApproval, submitApproval } = useAgentChat();

  const handleAccept = async (selectedVersion?: number) => {
    await submitApproval(true, selectedVersion);
  };

  const handleDiscard = async () => {
    await submitApproval(false);
  };

  return (
    <ExecutionFlow
      items={flowItems}
      onAccept={handleAccept}
      onDiscard={handleDiscard}
    />
  );
}
```

---

## 6. 修订状态管理

```typescript
// 在 useAgentChat 中管理修订状态

interface RevisionState {
  id: string;
  status: 'pending' | 'accepted' | 'discarded';
  data: RevisionFlowData;
}

// 更新修订状态
const updateRevisionStatus = (id: string, status: RevisionStatus) => {
  setFlowItems(prev =>
    prev.map(item =>
      item.id === id && item.type === 'revision'
        ? { ...item, data: { ...item.data, status } }
        : item
    )
  );
};
```

---

## 7. 编辑器 insert 类型支持 (待补充)

### 7.1 问题描述

当前 `NovelEditor.tsx` 的 `handleShowRevision` 只支持 `modify` 和 `continue` 类型，缺少 `insert` 类型处理。

**现有代码** (`NovelEditor.tsx:503-628`):
```typescript
const handleShowRevision = (event: Event) => {
  const { type, ... } = customEvent.detail;

  if (type === 'modify' && position) {
    // ✅ 处理修改
  } else if (type === 'continue') {
    // ✅ 处理续写
  }
  // ❌ 缺少 insert 类型处理
};
```

### 7.2 需要补充的代码

```typescript
// 在 handleShowRevision 中添加 insert 分支

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

### 7.3 修改位置

文件: `src/components/editor/NovelEditor.tsx`
位置: 约 620 行，在 `else if (type === 'continue')` 分支后添加
