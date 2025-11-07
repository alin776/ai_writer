# 架构设计文档

## 🏗️ 整体架构

### 系统分层

```
┌─────────────────────────────────────────────────────────┐
│                     EditorView (容器层)                  │
├─────────────────────────────────────────────────────────┤
│                  EditorContext (状态层)                  │
│  - editor instance (Tiptap编辑器实例)                    │
│  - aiSuggestion state (AI建议状态)                       │
├──────────────────────┬──────────────────────────────────┤
│   NovelEditor (左)   │   AgentChatPanel (右)            │
│   ┌────────────────┐ │   ┌────────────────┐             │
│   │ AIPendingMark  │◄┼───┤ AISuggestionCard│             │
│   │    扩展        │ │   │                │             │
│   └────────────────┘ │   │  ⚪ → ✓/✗ → ✅/❌│             │
│   ┌────────────────┐ │   └────────────────┘             │
│   │ 高亮待确认内容  │ │                                  │
│   └────────────────┘ │                                  │
└──────────────────────┴──────────────────────────────────┘
```

## 📊 数据流

### 1. 生成流程

```
用户输入 → AIPanel → SSE Stream
                         ↓
            ┌───────────────────────┐
            ↓                       ↓
     Editor实时插入            Agent卡片展示
     (带pending标记)             (⚪旋转)
            ↓                       ↓
     黄色高亮显示              生成完成展开
     (脉动动画)                (显示✓/✗)
```

### 2. 确认流程

```
用户点击 ✓
    ↓
useAISuggestion.acceptSuggestion()
    ↓
Editor移除pending标记 (保留内容)
    ↓
卡片状态更新为 ✅
    ↓
Toast提示 "✅ 内容已采纳"
```

### 3. 拒绝流程

```
用户点击 ✗
    ↓
useAISuggestion.rejectSuggestion()
    ↓
Editor删除内容和标记
    ↓
卡片状态更新为 ❌
    ↓
Toast提示 "❌ 内容已拒绝"
```

## 🔧 核心模块

### 1. 状态管理层

**文件**: `src/hooks/useAISuggestion.ts`

**职责**:
- 管理AI建议生命周期
- 提供accept/reject方法
- 维护当前建议状态

**接口**:
```typescript
interface UseAISuggestion {
  currentSuggestion: AISuggestion | null;
  startSuggestion: () => string;
  streamInsert: (chunk: string) => void;
  acceptSuggestion: () => void;
  rejectSuggestion: () => void;
}
```

### 2. 编辑器扩展层

**文件**: `src/components/editor/extensions/AIPendingMark.ts`

**职责**:
- 定义pending状态的Mark类型
- 提供DOM渲染规则
- 应用CSS样式类

**Mark属性**:
```typescript
{
  suggestionId: string;  // 建议唯一标识
}
```

### 3. UI组件层

#### AISuggestionCard

**文件**: `src/components/editor/AISuggestionCard.tsx`

**状态机**:
```
pending → generating → completed → (accepted | rejected)
```

**Props**:
```typescript
interface AISuggestionCardProps {
  suggestion: AISuggestion;
  onAccept: () => void;
  onReject: () => void;
}
```

### 4. 上下文层

**文件**: `src/views/EditorView/EditorContext.tsx`

**提供**:
- 编辑器实例
- AI建议状态
- 操作方法

## 🔄 状态同步机制

### 双向绑定

```typescript
// Editor → Card
editor.state.doc.content → card显示✓/✗按钮

// Card → Editor
card点击✓/✗ → editor内容更新
```

### 事件流

```
1. SSE chunk到达
   ↓
2. useAISuggestion.streamInsert(chunk)
   ↓
3. Editor.commands.insertContent(marked_chunk)
   ↓
4. DOM更新 + CSS高亮
   ↓
5. AISuggestionCard同步更新进度
```

## 📦 文件结构

```
src/
├── hooks/
│   └── useAISuggestion.ts          # 状态管理Hook
├── components/
│   └── editor/
│       ├── extensions/
│       │   └── AIPendingMark.ts    # Tiptap扩展
│       ├── AISuggestionCard.tsx    # Agent卡片组件
│       └── NovelEditor.tsx         # 编辑器组件
└── views/
    └── EditorView/
        ├── index.tsx               # 容器组件
        └── EditorContext.tsx       # Context定义
```

## 🎯 设计原则

### 1. 单一职责
- Hook只管状态
- 组件只管UI
- 扩展只管标记

### 2. 数据单向流动
```
State → UI → User Action → State Update
```

### 3. 最小化重渲染
- 使用Context避免prop drilling
- memo优化子组件
- 只订阅需要的状态

### 4. 类型安全
- 所有接口定义TypeScript类型
- 严格模式编译
- 避免any类型

## 🔌 扩展点

### 1. 自定义样式
通过CSS变量覆盖默认样式：
```css
.ai-pending-content {
  --ai-bg-color: rgba(255, 235, 59, 0.2);
  --ai-border-color: #FFD700;
}
```

### 2. 自定义Mark行为
继承AIPendingMark扩展：
```typescript
const CustomPendingMark = AIPendingMark.extend({
  // 自定义逻辑
});
```

### 3. 自定义卡片UI
通过Props传递自定义渲染：
```typescript
<AISuggestionCard
  renderActions={(onAccept, onReject) => (
    <CustomButtons />
  )}
/>
```

## 📈 性能考虑

### 1. 流式插入优化
- 使用requestAnimationFrame批处理
- 避免频繁DOM操作
- 合并连续的小chunk

### 2. 大文档性能
- 虚拟化长文档
- 懒加载历史建议
- 限制同时pending的建议数量

### 3. 内存管理
- 及时清理已完成的建议
- 限制历史记录数量
- 使用WeakMap存储临时数据

## 🔍 下一步

- [状态管理详细设计](./02-state-management.md)
- [Agent卡片UI实现](./03-agent-card.md)
- [编辑器同步机制](./04-editor-sync.md)
