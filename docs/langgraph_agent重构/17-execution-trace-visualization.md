# Agent 执行轨迹可视化方案

## 文档版本
- 版本：3.0
- 日期：2025-12-24
- 类型：技术方案
- 状态：🔥 优先实施
- 更新：补充现有代码差距分析、前端事件处理、完整数据流

---

## 〇、现有代码与设计差距分析

> ⚠️ **重要**：本章节明确当前代码与设计目标的差距，确保实施时有的放矢。

### 0.1 后端差距分析

#### 0.1.1 SSE 事件类型对比

| 事件类型 | 设计要求 | 现有实现 | 差距 |
|----------|---------|----------|------|
| `text` | AI 思考说明文字 | ❌ 不存在 | 🔴 需新增 |
| `tool` | `{icon, title, description, status}` | `tool_call`: `{tool, args}` | 🔴 格式不匹配 |
| `task_update` | 任务状态更新 | ❌ 不存在 | 🔴 需新增 |
| `content` | 最终输出 | ✅ 已有 | ✅ 可复用 |
| `progress` | 执行进度 | ✅ 已有 | ⚠️ 保留兼容 |

#### 0.1.2 EventParser 现有代码分析

**文件**: `backend/app/services/agent/stream/event_parser.py`

```python
# 现有工具显示名称（需要扩展为含图标的配置）
TOOL_DISPLAY_NAMES = {
    "get_chapter_by_order_tool": "读取章节",      # 需改为 {"icon": "FileText", ...}
    "continue_writing_tool": "继续创作",          # 需改为 {"icon": "PenTool", ...}
    "search_analysis_fragments_tool": "检索设定", # 需改为 {"icon": "Search", ...}
    ...
}

# 现有方法 generate_tool_description() 返回字符串
# 需要新增 format_tool_display() 返回完整对象
```

**需要改造的方法**:

| 方法 | 现有功能 | 改造内容 |
|------|---------|----------|
| `TOOL_DISPLAY_NAMES` | 工具名→显示名 | 扩展为 `TOOL_DISPLAY_CONFIG` 含图标 |
| `generate_tool_description()` | 返回描述字符串 | 保留，供 `format_tool_display()` 调用 |
| ❌ 不存在 | - | 新增 `format_tool_display()` |

#### 0.1.3 StreamEventHandler 现有代码分析

**文件**: `backend/app/services/agent/stream/stream_event_handler.py`

```python
# 现有回调
on_progress: callable   # ✅ 保留
on_tool_call: callable  # ⚠️ 需改为 on_tool，增强数据格式
on_content: callable    # ✅ 保留

# 缺少的回调
on_text: callable       # 🔴 需新增：AI 思考文字
```

### 0.2 前端差距分析

#### 0.2.1 组件对比

| 组件 | 设计要求 | 现有实现 | 差距 |
|------|---------|----------|------|
| `ExecutionFlow` | 执行轨迹容器 | ❌ 不存在 | 🔴 需新建 |
| `TextBlock` | AI 说明文字 | ❌ 不存在 | 🔴 需新建 |
| `ToolCard` | 工具调用卡片 | ❌ 不存在 | 🔴 需新建 |
| `ContentBlock` | 内容展示 | ❌ 不存在 | 🔴 需新建 |
| `ActivityStream` | 活动流 | ✅ 已有 | ⚠️ 样式可复用 |
| 任务列表 | 底部固定 | ✅ 已有（内嵌） | ⚠️ 需调整位置 |

#### 0.2.2 agentApi.ts 现有事件处理

**文件**: `src/services/agentApi.ts`

```typescript
// 现有事件处理（252-291行）
case 'content':
  callbacks.onContent?.(content);
  break;
case 'tool_call':
  callbacks.onToolCall?.(data.data);  // 🔴 格式不匹配设计
  break;
case 'progress':
  callbacks.onProgress?.(data.data);
  break;

// 缺少的事件处理
case 'text':    // 🔴 需新增
case 'tool':    // 🔴 需新增（增强版）
```

#### 0.2.3 useAgentChat.ts 现有回调

**文件**: `src/hooks/useAgentChat.ts`

```typescript
// 现有回调处理（350-416行）
onPlan: (plan) => { ... }
onTaskStart: (task) => { ... }
onTaskDone: (taskDone) => { ... }
onProgress: (progress) => { ... }
onToolCall: (toolCall) => { ... }

// 缺少的回调
onText: (textData) => { ... }   // 🔴 需新增
onTool: (toolData) => { ... }   // 🔴 需新增（增强版）
```

#### 0.2.4 布局差距

**现有布局** (`AIPanel.tsx`):
```
┌─────────────────────────────────┐
│ 历史消息                        │
│ ActivityStream（内嵌）          │ ← 与设计不符
│ 任务列表（内嵌，非固定）        │ ← 位置不对
│ 流式输出                        │
└─────────────────────────────────┘
```

**设计要求布局**:
```
┌─────────────────────────────────┐
│ 执行轨迹（可滚动）              │ ← 需新建 ExecutionFlow
│ AI: 我先读取第3章...            │
│ [ToolCard] 读取章节             │
├─────────────────────────────────┤
│ 任务列表（底部固定）            │ ← 需调整位置
└─────────────────────────────────┘
```

### 0.3 差距总结

```
┌─────────────────────────────────────────────────────────────┐
│ 实施工作量评估                                              │
│                                                             │
│ 后端改造:                                                   │
│ ├─ event_parser.py: 新增 TOOL_DISPLAY_CONFIG + format_tool_display()
│ ├─ stream_event_handler.py: 新增 on_text 回调              │
│ └─ langgraph_agent.py: 提取 AIMessage.content 发送 text 事件
│                                                             │
│ 前端改造:                                                   │
│ ├─ 新建 4 个组件: ExecutionFlow/TextBlock/ToolCard/ContentBlock
│ ├─ agentApi.ts: 新增 text/tool 事件处理                    │
│ ├─ useAgentChat.ts: 新增 onText/onTool 回调 + flowItems 状态
│ └─ AIPanel.tsx: 布局调整（任务列表移至底部固定）           │
└─────────────────────────────────────────────────────────────┘
```

---

## 一、设计规范总览

### 0.0 与现有前端保持一致

本方案严格遵循项目现有的前端设计规范，确保 UI 风格统一：

| 规范项 | 标准 | 来源 |
|--------|------|------|
| **图标库** | Lucide React | ActivityStream.tsx |
| **颜色系统** | Tailwind Slate 色系 | 全局主题 |
| **状态色-活跃** | blue-500 (#3b82f6) | ActivityStream.module.css |
| **状态色-完成** | emerald-500 (#10b981) | ActivityStream.module.css |
| **图标容器** | 28px 圆形 | ActivityStream 样式 |
| **卡片圆角** | 10px (rounded-[10px]) | ActivityStream 样式 |
| **字体大小** | 13px 正文 / 11px 次要 | 现有组件 |

### 0.0.1 Lucide 图标映射表

| 工具操作 | Lucide 图标 | 说明 |
|----------|-------------|------|
| 读取章节 | `FileText` | 文件类操作 |
| 检索设定 | `Search` | 搜索类操作 |
| 续写内容 | `PenTool` | 写作类操作 |
| 智能改写 | `Edit3` | 编辑类操作 |
| 智能插入 | `Plus` | 插入类操作 |
| 分析文本 | `BarChart2` | 分析类操作 |
| 应用修改 | `Check` | 确认类操作 |
| 默认工具 | `Wrench` | 通用工具 |
| 加载中 | `Loader2` | 旋转动画 |
| 完成状态 | `CheckCircle` | 带圆圈的勾 |
| 待执行 | `Circle` | 空心圆 |

### 0.0.2 颜色变量（Slate 色系）

```css
/* 基础灰度 */
--slate-50: #f8fafc;   /* 最浅背景 */
--slate-100: #f1f5f9;  /* 次浅背景 */
--slate-200: #e2e8f0;  /* 边框色 */
--slate-300: #cbd5e1;  /* 禁用色 */
--slate-400: #94a3b8;  /* 次要文字 */
--slate-500: #64748b;  /* 辅助文字 */
--slate-600: #475569;  /* 正文 */
--slate-700: #334155;  /* 强调文字 */
--slate-800: #1e293b;  /* 标题 */
--slate-900: #0f172a;  /* 深色背景 */
--slate-950: #020617;  /* 最深背景（暗色模式） */

/* 状态色-蓝色（活跃/执行中） */
--blue-50: #eff6ff;    /* 背景 */
--blue-200: #bfdbfe;   /* 边框 */
--blue-500: #3b82f6;   /* 图标/文字 */
--blue-600: #2563eb;   /* 悬停 */

/* 状态色-绿色（完成） */
--emerald-50: #ecfdf5; /* 背景 */
--emerald-100: #d1fae5;/* 边框 */
--emerald-500: #10b981;/* 图标/文字 */
```

---

## 一、与现有代码对接分析

### 1.1 现有 stream/ 模块结构

项目已有完善的流式处理模块：

```
backend/app/services/agent/stream/
├── __init__.py
├── event_parser.py           # EventParser 类（285 行）
└── stream_event_handler.py   # StreamEventHandler 类（220 行）
```

**EventParser 现有功能**:
```python
class EventParser:
    NODE_MAPPING = {
        "intent_classifier": "正在分析您的需求...",
        "writing_agent": "正在思考如何帮助您...",
        "planning_agent": "正在规划任务...",
        # ...
    }

    def parse_node_event(self, event) -> dict      # 节点事件解析
    def extract_tool_calls(self, node_data) -> list # 工具调用提取
```

**StreamEventHandler 现有功能**:
```python
class StreamEventHandler:
    def handle_event(self, event, callbacks)       # 事件分发
    # - 进度追踪
    # - 工具调用缓存
    # - HITL 确认请求
```

### 1.2 对接策略

**方案**: 扩展现有模块，而非重建

| 现有功能 | 新增功能 | 对接方式 |
|----------|----------|----------|
| `NODE_MAPPING` | 保持 | 复用节点名称映射 |
| `parse_node_event()` | 扩展 | 增加 text/tool 事件类型 |
| `extract_tool_calls()` | 扩展 | 增加 `format_tool_display()` |
| `handle_event()` | 扩展 | 增加新事件类型分发 |

### 1.3 SSE 事件格式迁移

**现有格式**:
```python
{
    "type": "progress",
    "data": {"node": "writing_agent", "message": "..."}
}
{
    "type": "tool_call",
    "data": {"tool": "read_chapter", "args": {...}}
}
{
    "type": "content",
    "data": {"text": "..."}
}
```

**新增格式**:
```python
# 新增 'text' 类型（AI 思考说明）
{
    "type": "text",
    "data": {"content": "我先读取第3章，了解当前进展..."}
}

# 增强 'tool' 类型（带显示信息，使用 Lucide 图标名）
{
    "type": "tool",
    "data": {
        "icon": "FileText",       # Lucide 图标名
        "title": "读取章节",
        "description": "第3章 · 2000字",
        "status": "running"
    }
}

# 新增 'task_update' 类型
{
    "type": "task_update",
    "data": {"task_id": "xxx", "status": "done"}
}
```

**兼容性**: 新旧格式可以共存，前端按 type 分别处理

---

## 二、背景

### 2.1 问题描述

当前 Agent 执行任务时，用户只能看到：
- 任务列表闪烁（表示正在执行）
- 最终生成的结果

用户**看不到**：
- AI 正在思考什么
- 为什么调用某个工具
- 执行的具体过程

### 2.2 专业术语

| 术语 | 英文 | 说明 |
|------|------|------|
| Agent 执行轨迹 | Agent Execution Trace | Agent 每一步的决策、工具调用、状态变化 |
| 逐步执行可视化 | Step-by-step Execution | 一步一步展示执行过程 |
| Agent 行为时间线 | Agent Action Timeline | 按时间顺序展示 Agent 行为 |

### 2.3 参考案例

**Cursor 风格**：AI 说明 + 工具卡片交织，对话流形式

```
AI: 我先读取第3章内容，了解当前进展。
┌─────────────────────────────────────┐
│ 📄 summary.py        +150 -0       │
└─────────────────────────────────────┘

AI: 接下来，我将规范化交互标签...
┌─────────────────────────────────────┐
│ 📄 segmentation.py   +94 -0        │
└─────────────────────────────────────┘

AI: 全部完成！我们现在跟踪焦点份额...
```

---

## 三、核心设计原则

### 3.1 职责分离

| 角色 | 职责 | 不负责 |
|------|------|--------|
| **AI** | 决定说什么、做什么 | 怎么画 |
| **后端** | 组装数据、格式化显示文案 | UI 样式 |
| **前端** | 渲染 UI、画出来 | 决定内容 |

### 3.2 前端是"哑巴渲染器"

```
后端返回什么 → 前端显示什么
```

**正确做法**：
```typescript
// 后端返回完整的显示信息（使用 Lucide 图标名）
{
  type: 'tool',
  icon: 'FileText',              // Lucide 图标名
  title: '读取章节',
  description: '第3章 · 2000字'  // 后端决定怎么描述
}

// 前端根据图标名渲染对应组件
<ToolCard icon={data.icon} title={data.title} desc={data.description} />
```

**错误做法**：
```typescript
// ❌ 前端写死模板
<ToolCard>
  读取章节 第{args.chapter}章
</ToolCard>
```

### 3.3 AI 输出风格

- **自然语言**：AI 自己决定说什么
- **Prompt 轻引导**：只引导风格，不强制格式
- **灵活表达**：不限制详细程度

```python
# Prompt 引导（轻量）
"""
当你需要调用工具时，先简短说明你要做什么。
"""

# 不要这样（过度限制）
"""
你必须先说"我需要..."，然后说"因为..."
"""
```

---

## 四、UI 布局设计

### 4.1 整体布局

```
┌─────────────────────────────────────────────────────┐
│                                                     │
│  执行轨迹（上方，可滚动）                            │
│                          ↑ 内容往上走               │
│                                                     │
│  AI: 我先读取第3章内容...                           │
│  ┌─────────────────────────────────────────────────┐│
│  │ [FileText] 读取章节  第3章                      ││
│  └─────────────────────────────────────────────────┘│
│                                                     │
│  AI: 好的，接下来检索设定...                        │
│  ┌─────────────────────────────────────────────────┐│
│  │ [Search] 检索设定  角色设定                     ││
│  └─────────────────────────────────────────────────┘│
│                                                     │
│  [流式输出的内容...]                                │
│                                                     │
├─────────────────────────────────────────────────────┤
│  任务列表（底部固定）                                │
│  ├─ ✓ 读取章节内容              ← 已完成，划掉     │
│  ├─ ✓ 检索角色设定              ← 已完成，划掉     │
│  └─ ○ 续写内容                  ← 当前执行         │
└─────────────────────────────────────────────────────┘
```

### 4.2 布局特点

| 区域 | 位置 | 行为 |
|------|------|------|
| **执行轨迹** | 上方 | 内容向上滚动，交织显示 |
| **任务列表** | 底部固定 | 完成一个划掉一个 |

### 4.3 任务列表样式

```
✓ 已完成任务（删除线 + 灰色 + CheckCircle 图标）
○ 待执行任务（正常显示 + Circle 图标）
◎ 执行中任务（蓝色高亮 + Loader2 旋转图标）
```

---

## 五、数据结构设计

### 5.1 SSE 事件类型

后端发送的 SSE 事件：

```typescript
// 1. 执行步骤（可选，小圆点列表）
{
  type: 'step',
  action: '思考',
  target: '',
  duration: '3秒'
}

// 2. AI 说明文字
{
  type: 'text',
  content: '我先读取第3章，了解当前的剧情进展：'
}

// 3. 工具调用卡片（使用 Lucide 图标名）
{
  type: 'tool',
  icon: 'FileText',              // Lucide 图标名：FileText/Search/PenTool/Edit3 等
  title: '读取章节',
  description: '第3章 · 约2000字',
  status: 'running' | 'done' | 'error'
}

// 4. 最终内容
{
  type: 'content',
  content: '...'
}

// 5. 任务状态更新
{
  type: 'task_update',
  task_id: 'xxx',
  status: 'done'  // pending | running | done
}
```

### 5.2 前端数据结构

```typescript
// 执行轨迹项
interface FlowItem {
  id: string;
  type: 'step' | 'text' | 'tool' | 'content';
  data: StepData | TextData | ToolData | ContentData;
  timestamp: string;
}

// 步骤数据（小圆点）
interface StepData {
  action: string;      // "思考"、"读取"、"检索"
  target?: string;     // "第3章"、"角色设定"
  duration?: string;   // "3秒"
}

// 文字数据（AI 说明）
interface TextData {
  content: string;
}

// 工具数据（卡片）
interface ToolData {
  icon: string;
  title: string;
  description: string;
  status: 'running' | 'done' | 'error';
}

// 内容数据（最终输出）
interface ContentData {
  content: string;
}

// 任务项
interface TaskItem {
  id: string;
  description: string;
  status: 'pending' | 'running' | 'done';
}
```

---

## 六、组件设计

### 6.1 设计原则

**复用现有组件和样式**：
- 复用 `ActivityStream.module.css` 的样式变量
- 使用 Lucide React 图标库（与现有一致）
- 遵循现有的颜色系统（蓝色 active、绿色 completed）

### 6.2 图标映射（Lucide React）

```typescript
// 工具图标映射
const TOOL_ICONS: Record<string, LucideIcon> = {
  // 文件操作
  FileText: FileText,      // 读取章节
  Search: Search,          // 检索

  // 写作操作
  PenTool: PenTool,        // 续写
  Edit3: Edit3,            // 改写
  Plus: Plus,              // 插入

  // 分析
  BarChart2: BarChart2,    // 分析

  // 状态
  Wrench: Wrench,          // 默认工具
  Check: Check,            // 完成
  Loader2: Loader2,        // 加载中
};
```

### 6.3 组件结构

```
ExecutionFlow/
├── index.tsx              # 主容器（执行轨迹）
├── ExecutionFlow.module.css
├── components/
│   ├── TextBlock.tsx      # AI 说明文字
│   ├── ToolCard.tsx       # 工具调用卡片（复用 ActivityStream 样式）
│   └── ContentBlock.tsx   # 最终内容
└── types.ts

# 任务列表：复用现有 AIPanel.tsx 中的实现，无需新增组件
```

### 6.4 ToolCard 组件（核心）

**复用 ActivityStream 样式模式**：

```tsx
import { FileText, Search, PenTool, Edit3, Loader2, Check } from 'lucide-react';
import styles from '../ActivityStream.module.css';

interface ToolCardProps {
  icon: string;           // Lucide 图标名
  title: string;
  description: string;
  status: 'running' | 'done' | 'error';
}

const ICON_MAP: Record<string, React.ComponentType<any>> = {
  FileText, Search, PenTool, Edit3, Wrench, BarChart2, Plus, Check
};

export function ToolCard({ icon, title, description, status }: ToolCardProps) {
  const IconComponent = ICON_MAP[icon] || Wrench;

  return (
    <div className={`
      ${styles.activityItem}
      ${status === 'running' ? styles.active : ''}
      ${status === 'done' ? styles.completed : ''}
      ${status === 'error' ? styles.failed : ''}
    `}>
      {/* 图标容器 - 28px 圆形 */}
      <div className={styles.activityIcon}>
        <IconComponent
          size={14}
          className={`
            ${status === 'running' ? styles.iconActive : styles.iconCompleted}
            ${status === 'running' ? styles.spin : ''}
          `}
        />
      </div>

      {/* 内容区域 */}
      <div className={styles.activityContent}>
        <div className={styles.activityDescription}>{title}</div>
        {description && (
          <div className={styles.activityMeta}>
            <span className={styles.toolName}>{description}</span>
          </div>
        )}
      </div>

      {/* 状态指示器 */}
      <div className={styles.activityStatus}>
        {status === 'running' && <Loader2 size={12} className={styles.spin} />}
        {status === 'done' && <Check size={12} className={styles.checkIcon} />}
      </div>
    </div>
  );
}
```

### 6.5 TextBlock 组件

```tsx
// AI 说明文字 - 简洁风格
export function TextBlock({ content }: { content: string }) {
  return (
    <p className="text-sm text-slate-600 dark:text-slate-300 my-2 leading-relaxed">
      {content}
    </p>
  );
}
```

### 6.6 ContentBlock 组件

```tsx
// 最终输出内容 - 纯文本，与现有 AIPanel 一致
export function ContentBlock({ content }: { content: string }) {
  return (
    <div className="my-3">
      <div className="text-sm text-slate-500 dark:text-slate-300 leading-relaxed whitespace-pre-wrap">
        {content}
      </div>
    </div>
  );
}
```

### 6.7 任务列表（复用现有实现）

**现有实现位置**：`AIPanel.tsx:1010-1069`

现有任务列表已具备完整功能，无需重新开发：

```typescript
// 现有 Task 接口（useAgentChat.ts:17-25）
interface Task {
  task_id: number;
  description: string;
  tool?: string;
  status: 'pending' | 'running' | 'completed' | 'failed';
  elapsed_time?: number;
  progress_status?: string;
}
```

**复用方案**：只需调整布局位置（从消息流内嵌 → 固定底部）

```tsx
// AIPanel.tsx 布局调整
<div className="flex flex-col h-full">
  {/* 上方：执行轨迹 + 消息流 */}
  <div className="flex-1 overflow-y-auto">
    {/* 现有消息内容 */}
  </div>

  {/* 底部固定：复用现有任务列表代码 */}
  {tasks.length > 0 && (
    <div className="border-t border-slate-200 dark:border-slate-700 p-3 bg-slate-50 dark:bg-slate-900">
      {/* 将现有任务列表代码（1010-1069行）移到这里 */}
    </div>
  )}
</div>
```

**现有功能清单**：
- ✅ 进度显示（完成数/总数）
- ✅ 状态指示器（圆点 + 动画）
- ✅ 任务描述 + 耗时
- ✅ 进度条
- ✅ SSE 事件对接（onTaskListUpdate/onTaskStart/onTaskDone）

### 6.8 整体布局

```tsx
// ExecutionFlow/index.tsx
import { ScrollArea } from '@/components/ui/scroll-area';

export function ExecutionFlow({ items }: Props) {
  // 注意：任务列表复用现有实现，不在此组件中
  return (
    <ScrollArea className="flex-1 p-4">
      {items.map((item) => {
        switch (item.type) {
          case 'text':
            return <TextBlock key={item.id} content={item.data.content} />;
          case 'tool':
            return <ToolCard key={item.id} {...item.data} />;
          case 'content':
            return <ContentBlock key={item.id} content={item.data.content} />;
        }
      })}
    </ScrollArea>
  );
}
```

---

## 七、后端改动

### 7.1 扩展 EventParser（stream/event_parser.py）

在现有 `EventParser` 类中添加方法：

```python
# stream/event_parser.py
# 使用 Lucide 图标名称（前端使用）

class EventParser:
    # 现有代码保持不变...

    # 🆕 新增：工具显示格式化（使用 Lucide 图标名）
    # ⚠️ 重要：工具名必须与实际代码中的工具名完全一致（含 _tool 后缀）
    TOOL_DISPLAY_CONFIG = {
        # ========== 章节读取类 ==========
        "get_chapter_by_order_tool": {"icon": "FileText", "title": "读取章节"},
        "read_chapter_tool": {"icon": "FileText", "title": "读取章节"},
        "get_context_tool": {"icon": "BookOpen", "title": "获取上下文"},

        # ========== 检索类 ==========
        "search_analysis_fragments_tool": {"icon": "Search", "title": "检索设定"},
        "search_memory_tool": {"icon": "Search", "title": "搜索记忆"},
        "search_knowledge_advanced": {"icon": "Search", "title": "高级知识检索"},

        # ========== 写作类 ==========
        "continue_writing_tool": {"icon": "PenTool", "title": "继续创作"},
        "smart_continue": {"icon": "ArrowRight", "title": "智能续写"},
        "expand_text": {"icon": "Maximize2", "title": "扩写内容"},

        # ========== 编辑类 ==========
        "smart_rewrite": {"icon": "Edit3", "title": "智能改写"},
        "smart_insert": {"icon": "Plus", "title": "智能插入"},
        "apply_chapter_edit": {"icon": "Check", "title": "应用修改"},
        "deai_rewrite": {"icon": "RefreshCw", "title": "去AI改写"},

        # ========== 分析类 ==========
        "analyze_text_tool": {"icon": "BarChart2", "title": "分析文本"},
        "analyze_content": {"icon": "FileSearch", "title": "内容分析"},
        "book_analysis": {"icon": "BarChart2", "title": "书籍分析"},
        "novel_review": {"icon": "MessageSquare", "title": "小说评审"},
        "ai_evaluation": {"icon": "Sparkles", "title": "AI评估"},
        "evaluate_quality": {"icon": "Star", "title": "质量评估"},

        # ========== 管理类 ==========
        "add_todo_tool": {"icon": "ListTodo", "title": "添加待办"},
        "get_work_details_tool": {"icon": "BookOpen", "title": "获取作品信息"},
        "update_work_metadata_tool": {"icon": "Save", "title": "更新元数据"},

        # ========== 默认 ==========
        "_default": {"icon": "Wrench", "title": "工具调用"}
    }

    def format_tool_display(self, tool_call: dict) -> dict:
        """格式化工具调用为前端显示格式"""
        tool_name = tool_call.get("name", "unknown")
        args = tool_call.get("args", {})

        config = self.TOOL_DISPLAY_CONFIG.get(
            tool_name,
            self.TOOL_DISPLAY_CONFIG["_default"]
        )

        description = self._build_tool_description(tool_name, args)

        return {
            "type": "tool",
            "data": {
                "icon": config["icon"],  # Lucide 图标名
                "title": config["title"],
                "description": description,
                "status": "running"
            }
        }

    def _build_tool_description(self, tool_name: str, args: dict) -> str:
        """根据工具类型构建描述"""
        # 章节读取类
        if tool_name in ["read_chapter_tool", "get_chapter_by_order_tool"]:
            chapter = args.get("chapter_order") or args.get("chapter_id", "")
            if chapter:
                return f"第{chapter}章"
            return ""

        # 检索类
        elif tool_name == "search_analysis_fragments_tool":
            query = args.get("query", "")
            return query[:30] if query else "检索中..."
        elif tool_name == "search_memory_tool":
            query = args.get("query", "")
            return query[:30] if query else "搜索中..."
        elif tool_name == "search_knowledge_advanced":
            query = args.get("query", "")
            return query[:30] if query else "检索中..."

        # 写作类
        elif tool_name == "continue_writing_tool":
            words = args.get("target_words") or args.get("word_count", 500)
            return f"目标{words}字"
        elif tool_name == "smart_continue":
            words = args.get("target_words", 500)
            return f"约{words}字"
        elif tool_name == "expand_text":
            return "扩写中..."

        # 编辑类
        elif tool_name == "smart_rewrite":
            style = args.get("style", "润色优化")
            return style[:20]
        elif tool_name == "smart_insert":
            return "插入中..."
        elif tool_name == "apply_chapter_edit":
            return "保存中..."
        elif tool_name == "deai_rewrite":
            return "改写中..."

        # 分析类
        elif tool_name == "analyze_text_tool":
            focus = args.get("focus", "综合分析")
            return focus[:20]
        elif tool_name in ["analyze_content", "book_analysis"]:
            return "分析中..."
        elif tool_name == "novel_review":
            return "评审中..."
        elif tool_name == "ai_evaluation":
            return "评估中..."
        elif tool_name == "evaluate_quality":
            return "评估中..."

        # 管理类
        elif tool_name == "get_context_tool":
            return "加载上下文..."
        elif tool_name == "add_todo_tool":
            return "添加中..."
        elif tool_name == "get_work_details_tool":
            return "获取中..."
        elif tool_name == "update_work_metadata_tool":
            return "更新中..."

        return ""
```

### 7.2 扩展 StreamEventHandler

在现有 `StreamEventHandler` 类中添加处理逻辑：

```python
# stream/stream_event_handler.py

class StreamEventHandler:
    def __init__(self, event_parser: EventParser = None):
        self.event_parser = event_parser or EventParser()

    def handle_event(self, event, callbacks):
        # 现有逻辑保持...

        # 🆕 新增：处理 AIMessage.content（思考文字）
        if self._is_ai_message_with_content(event):
            content = self._extract_ai_content(event)
            if content:
                callbacks.on_text({"type": "text", "data": {"content": content}})

        # 🆕 新增：处理工具调用（增强格式）
        if self._has_tool_calls(event):
            for tool_call in self._extract_tool_calls(event):
                display_event = self.event_parser.format_tool_display(tool_call)
                callbacks.on_tool(display_event)
```

### 7.3 Prompt 轻引导

**位置**：System Prompt

```python
"""
当你需要调用工具时，先简短说明你要做什么。

示例：
- "我先读取第3章，了解当前进展。"
- "让我检索一下角色设定。"
- "现在开始续写..."
"""
```

### 7.4 SSE 事件生成

**位置**：`chat_stream()` 或 `event_generator()`

```python
async def process_agent_message(ai_message: AIMessage):
    # 1. 发送思考文字（如果有）
    if ai_message.content:
        yield {
            "type": "text",
            "content": ai_message.content
        }

    # 2. 发送工具调用（如果有）
    if ai_message.tool_calls:
        for tool_call in ai_message.tool_calls:
            # 后端决定显示内容
            display_info = format_tool_display(tool_call)
            yield {
                "type": "tool",
                "icon": display_info["icon"],
                "title": display_info["title"],
                "description": display_info["description"],
                "status": "running"
            }
```

### 7.5 工具显示格式化

```python
def format_tool_display(tool_call: dict) -> dict:
    """后端决定工具卡片显示什么（使用 Lucide 图标名）"""
    tool_name = tool_call["name"]
    args = tool_call["args"]

    # 根据工具类型格式化显示（返回 Lucide 图标名）
    if tool_name == "read_chapter":
        return {
            "icon": "FileText",        # Lucide 图标名
            "title": "读取章节",
            "description": f"第{args.get('chapter')}章"
        }
    elif tool_name == "search_settings":
        return {
            "icon": "Search",          # Lucide 图标名
            "title": "检索设定",
            "description": args.get("query", "")
        }
    elif tool_name == "continue_writing":
        return {
            "icon": "PenTool",         # Lucide 图标名
            "title": "续写内容",
            "description": f"约{args.get('word_count', 500)}字"
        }
    elif tool_name == "smart_rewrite":
        return {
            "icon": "Edit3",           # Lucide 图标名
            "title": "智能改写",
            "description": args.get("style", "润色优化")
        }
    else:
        return {
            "icon": "Wrench",          # 默认图标
            "title": "工具调用",
            "description": tool_name
        }
```

---

## 八、前端改动详细方案

> ⚠️ **重要**：本章节详细描述前端 SSE 事件处理、状态管理和数据流的具体改动。

### 8.1 agentApi.ts 改动

**文件**: `src/services/agentApi.ts`

**新增事件处理**（在现有 switch 语句中添加）：

```typescript
// ==================== 新增事件类型 ====================

case 'text':
  // AI 思考说明文字
  callbacks.onText?.({
    type: 'text',
    content: data.data?.content || data.data
  });
  break;

case 'tool':
  // 增强版工具调用（含图标和格式化信息）
  callbacks.onTool?.({
    type: 'tool',
    icon: data.data?.icon || 'Wrench',
    title: data.data?.title || '工具调用',
    description: data.data?.description || '',
    status: data.data?.status || 'running'
  });
  break;

case 'tool_done':
  // 工具完成状态更新
  callbacks.onToolDone?.({
    toolId: data.data?.tool_id,
    status: 'done'
  });
  break;
```

**新增回调接口**：

```typescript
interface StreamCallbacks {
  // ==================== 现有回调（保持不变）====================
  onStart?: (conversationId: string) => void;
  onContent?: (chunk: string) => void;
  onDone?: (metadata: any, suggestedActions?: any[]) => void;
  onError?: (error: string) => void;
  onPlan?: (plan: any) => void;
  onTaskStart?: (task: any) => void;
  onTaskDone?: (taskDone: any) => void;
  onProgress?: (progress: any) => void;
  onToolCall?: (toolCall: any) => void;  // 保留兼容

  // ==================== 新增回调 ====================
  onText?: (textData: TextEventData) => void;      // 🆕 AI 思考文字
  onTool?: (toolData: ToolEventData) => void;      // 🆕 增强版工具调用
  onToolDone?: (toolDone: ToolDoneData) => void;   // 🆕 工具完成
}

// 新增类型定义
interface TextEventData {
  type: 'text';
  content: string;
}

interface ToolEventData {
  type: 'tool';
  icon: string;        // Lucide 图标名
  title: string;
  description: string;
  status: 'running' | 'done' | 'error';
}

interface ToolDoneData {
  toolId: string;
  status: 'done' | 'error';
}
```

### 8.2 useAgentChat.ts 改动

**文件**: `src/hooks/useAgentChat.ts`

#### 8.2.1 新增 FlowItem 状态

```typescript
// ==================== 新增状态定义 ====================

interface FlowItem {
  id: string;
  type: 'text' | 'tool' | 'content';
  data: TextData | ToolData | ContentData;
  timestamp: string;
}

interface TextData {
  content: string;
}

interface ToolData {
  icon: string;
  title: string;
  description: string;
  status: 'running' | 'done' | 'error';
}

interface ContentData {
  content: string;
}

// 在 SessionState 中新增
interface SessionState {
  // ... 现有字段保持不变
  messages: Message[];
  tasks: Task[];
  activities: ActivityItem[];
  progressData: ProgressData;

  // 🆕 新增：执行轨迹项
  flowItems: FlowItem[];
}
```

#### 8.2.2 新增回调处理

```typescript
// ==================== 在 chatStream 回调中新增 ====================

const flowItemsRef = useRef<FlowItem[]>([]);

// 🆕 处理 AI 思考文字
onText: (textData: TextEventData) => {
  const flowItem: FlowItem = {
    id: `text_${Date.now()}`,
    type: 'text',
    data: { content: textData.content },
    timestamp: new Date().toISOString()
  };

  flowItemsRef.current = [...flowItemsRef.current, flowItem];

  sessionManager.updateSession(sessionId, {
    flowItems: flowItemsRef.current
  });
},

// 🆕 处理增强版工具调用
onTool: (toolData: ToolEventData) => {
  const flowItem: FlowItem = {
    id: `tool_${Date.now()}`,
    type: 'tool',
    data: {
      icon: toolData.icon,
      title: toolData.title,
      description: toolData.description,
      status: toolData.status
    },
    timestamp: new Date().toISOString()
  };

  flowItemsRef.current = [...flowItemsRef.current, flowItem];

  sessionManager.updateSession(sessionId, {
    flowItems: flowItemsRef.current
  });
},

// 🆕 处理工具完成
onToolDone: (toolDone: ToolDoneData) => {
  // 更新对应工具的状态为 done
  flowItemsRef.current = flowItemsRef.current.map(item => {
    if (item.type === 'tool' && item.id === toolDone.toolId) {
      return {
        ...item,
        data: { ...(item.data as ToolData), status: 'done' }
      };
    }
    return item;
  });

  sessionManager.updateSession(sessionId, {
    flowItems: flowItemsRef.current
  });
},

// 🆕 处理流式内容（添加到 flowItems）
onContent: (chunk: string) => {
  // 保持现有打字机效果逻辑...

  // 同时更新 flowItems 中的 content 项
  const existingContentItem = flowItemsRef.current.find(
    item => item.type === 'content'
  );

  if (existingContentItem) {
    // 追加内容
    flowItemsRef.current = flowItemsRef.current.map(item => {
      if (item.type === 'content') {
        return {
          ...item,
          data: { content: (item.data as ContentData).content + chunk }
        };
      }
      return item;
    });
  } else {
    // 创建新的 content 项
    const contentItem: FlowItem = {
      id: `content_${Date.now()}`,
      type: 'content',
      data: { content: chunk },
      timestamp: new Date().toISOString()
    };
    flowItemsRef.current = [...flowItemsRef.current, contentItem];
  }

  sessionManager.updateSession(sessionId, {
    flowItems: flowItemsRef.current
  });
},
```

#### 8.2.3 会话重置时清空 flowItems

```typescript
// 在开始新对话时
onStart: (conversationId: string) => {
  // 清空执行轨迹
  flowItemsRef.current = [];

  sessionManager.updateSession(sessionId, {
    flowItems: [],
    // ... 其他重置
  });
},
```

### 8.3 完整数据流

```
┌─────────────────────────────────────────────────────────────────────────┐
│                           完整数据流                                      │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                         │
│  后端 LangGraph Agent                                                   │
│  ├─ AIMessage.content (思考文字)                                        │
│  │     ↓                                                                │
│  │   emit_event("text", {content: "我先读取第3章..."})                  │
│  │                                                                      │
│  ├─ AIMessage.tool_calls                                                │
│  │     ↓                                                                │
│  │   EventParser.format_tool_display(tool_call)                         │
│  │     ↓                                                                │
│  │   emit_event("tool", {icon: "FileText", title: "读取章节", ...})     │
│  │                                                                      │
│  └─ ToolMessage.content (工具返回)                                      │
│        ↓                                                                │
│      emit_event("tool_done", {tool_id: "xxx", status: "done"})          │
│                                                                         │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                         │
│  SSE HTTP Stream                                                        │
│  data: {"type": "text", "data": {"content": "..."}}                     │
│  data: {"type": "tool", "data": {"icon": "FileText", ...}}              │
│  data: {"type": "tool_done", "data": {"tool_id": "...", "status": ...}} │
│  data: {"type": "content", "data": "生成的内容..."}                     │
│                                                                         │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                         │
│  前端 agentApi.ts                                                       │
│  ├─ case 'text'  → callbacks.onText(data)                               │
│  ├─ case 'tool'  → callbacks.onTool(data)                               │
│  ├─ case 'tool_done' → callbacks.onToolDone(data)                       │
│  └─ case 'content' → callbacks.onContent(data)                          │
│                                                                         │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                         │
│  前端 useAgentChat.ts                                                   │
│  ├─ onText  → flowItemsRef.current.push({type: 'text', ...})            │
│  ├─ onTool  → flowItemsRef.current.push({type: 'tool', ...})            │
│  ├─ onToolDone → 更新对应 tool 的 status                                │
│  └─ onContent → 更新或创建 content 项                                   │
│        ↓                                                                │
│      sessionManager.updateSession({flowItems: [...]})                   │
│                                                                         │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                         │
│  前端 AIPanel.tsx                                                       │
│  ├─ const { flowItems, tasks } = useAgentChat()                         │
│  │                                                                      │
│  └─ 渲染:                                                               │
│      <div className="flex flex-col h-full">                             │
│        {/* 上方：执行轨迹（可滚动）*/}                                   │
│        <div className="flex-1 overflow-y-auto">                         │
│          <ExecutionFlow items={flowItems} />                            │
│        </div>                                                           │
│                                                                         │
│        {/* 底部固定：任务列表 */}                                        │
│        <div className="border-t ...">                                   │
│          <TaskList tasks={tasks} />                                     │
│        </div>                                                           │
│      </div>                                                             │
│                                                                         │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                         │
│  ExecutionFlow 组件                                                     │
│  flowItems.map(item => {                                                │
│    switch (item.type) {                                                 │
│      case 'text':    return <TextBlock content={item.data.content} />   │
│      case 'tool':    return <ToolCard {...item.data} />                 │
│      case 'content': return <ContentBlock content={item.data.content} />│
│    }                                                                    │
│  })                                                                     │
│                                                                         │
└─────────────────────────────────────────────────────────────────────────┘
```

### 8.4 工具名映射表（完整版）

> ⚠️ 注意：工具名必须与 `event_parser.py` 中实际使用的工具名完全一致

#### 8.4.1 现有 TOOL_DISPLAY_NAMES（需废弃）

```python
# 旧版映射（仅8个工具，待废弃）
TOOL_DISPLAY_NAMES = {
    "get_chapter_by_order_tool": "读取章节",
    "continue_writing_tool": "继续创作",
    "search_analysis_fragments_tool": "检索设定",
    "search_memory_tool": "搜索记忆",
    "add_todo_tool": "添加待办",
    "get_work_details_tool": "获取作品信息",
    "update_work_metadata_tool": "更新元数据",
    "analyze_text_tool": "分析文本"
}
```

#### 8.4.2 新版 TOOL_DISPLAY_CONFIG（完整22个工具）

```python
# backend/app/services/agent/stream/event_parser.py

TOOL_DISPLAY_CONFIG = {
    # ========== 章节读取类（3个）==========
    "get_chapter_by_order_tool": {"icon": "FileText", "title": "读取章节"},
    "read_chapter_tool": {"icon": "FileText", "title": "读取章节"},
    "get_context_tool": {"icon": "BookOpen", "title": "获取上下文"},

    # ========== 检索类（3个）==========
    "search_analysis_fragments_tool": {"icon": "Search", "title": "检索设定"},
    "search_memory_tool": {"icon": "Search", "title": "搜索记忆"},
    "search_knowledge_advanced": {"icon": "Search", "title": "高级知识检索"},

    # ========== 写作类（3个）==========
    "continue_writing_tool": {"icon": "PenTool", "title": "继续创作"},
    "smart_continue": {"icon": "ArrowRight", "title": "智能续写"},
    "expand_text": {"icon": "Maximize2", "title": "扩写内容"},

    # ========== 编辑类（4个）==========
    "smart_rewrite": {"icon": "Edit3", "title": "智能改写"},
    "smart_insert": {"icon": "Plus", "title": "智能插入"},
    "apply_chapter_edit": {"icon": "Check", "title": "应用修改"},
    "deai_rewrite": {"icon": "RefreshCw", "title": "去AI改写"},

    # ========== 分析类（6个）==========
    "analyze_text_tool": {"icon": "BarChart2", "title": "分析文本"},
    "analyze_content": {"icon": "FileSearch", "title": "内容分析"},
    "book_analysis": {"icon": "BarChart2", "title": "书籍分析"},
    "novel_review": {"icon": "MessageSquare", "title": "小说评审"},
    "ai_evaluation": {"icon": "Sparkles", "title": "AI评估"},
    "evaluate_quality": {"icon": "Star", "title": "质量评估"},

    # ========== 管理类（3个）==========
    "add_todo_tool": {"icon": "ListTodo", "title": "添加待办"},
    "get_work_details_tool": {"icon": "BookOpen", "title": "获取作品信息"},
    "update_work_metadata_tool": {"icon": "Save", "title": "更新元数据"},

    # ========== 默认 ==========
    "_default": {"icon": "Wrench", "title": "工具调用"}
}
```

#### 8.4.3 Lucide 图标速查表

| 图标名 | 用途 | 工具示例 |
|--------|------|----------|
| `FileText` | 文件/章节读取 | read_chapter_tool |
| `BookOpen` | 作品/上下文 | get_context_tool, get_work_details_tool |
| `Search` | 检索/搜索 | search_analysis_fragments_tool |
| `PenTool` | 创作/写作 | continue_writing_tool |
| `ArrowRight` | 续写 | smart_continue |
| `Maximize2` | 扩展/扩写 | expand_text |
| `Edit3` | 编辑/改写 | smart_rewrite |
| `Plus` | 插入/添加 | smart_insert |
| `Check` | 确认/应用 | apply_chapter_edit |
| `RefreshCw` | 重写/刷新 | deai_rewrite |
| `BarChart2` | 分析/统计 | analyze_text_tool, book_analysis |
| `FileSearch` | 内容分析 | analyze_content |
| `MessageSquare` | 评审/评论 | novel_review |
| `Sparkles` | AI评估 | ai_evaluation |
| `Star` | 质量评估 | evaluate_quality |
| `ListTodo` | 待办事项 | add_todo_tool |
| `Save` | 保存/更新 | update_work_metadata_tool |
| `Wrench` | 默认工具 | 未知工具 |
| `Loader2` | 加载中 | 状态指示 |
| `CheckCircle` | 完成 | 状态指示 |

#### 8.4.4 工具来源清单

> 📋 确保所有工具都已覆盖，按文件分类

| 来源文件 | 工具名 | 是否映射 |
|----------|--------|----------|
| **langgraph_tools.py** | | |
| | `continue_writing_tool` | ✅ |
| | `analyze_text_tool` | ✅ |
| | `read_chapter_tool` | ✅ |
| | `get_chapter_by_order_tool` | ✅ |
| | `search_analysis_fragments_tool` | ✅ |
| | `get_context_tool` | ✅ |
| **tools/editor_tools.py** | | |
| | `smart_continue` | ✅ |
| | `smart_rewrite` | ✅ |
| | `smart_insert` | ✅ |
| | `apply_chapter_edit` | ✅ |
| **tools/advanced_tools.py** | | |
| | `book_analysis` | ✅ |
| | `novel_review` | ✅ |
| | `ai_evaluation` | ✅ |
| | `deai_rewrite` | ✅ |
| | `search_knowledge_advanced` | ✅ |
| **tools/writing_tools.py** | | |
| | `expand_text` | ✅ |
| **tools/analysis_tools.py** | | |
| | `analyze_content` | ✅ |
| | `evaluate_quality` | ✅ |
| **现有映射（待确认来源）** | | |
| | `search_memory_tool` | ✅ |
| | `add_todo_tool` | ✅ |
| | `get_work_details_tool` | ✅ |
| | `update_work_metadata_tool` | ✅ |

**总计**: 22 个工具 + 1 个默认

#### 8.4.5 实施差异分析

> 📊 对比现有代码与文档规划的差异

**现有代码** (`stream/event_parser.py`):

```python
# 当前状态：仅 8 个工具，使用 emoji 图标
TOOL_DISPLAY_NAMES = {
    "get_chapter_by_order_tool": "读取章节",
    "continue_writing_tool": "继续创作",
    # ... 共 8 个
}

def generate_tool_description(self, tool_name, tool_args):
    # 使用 emoji 作为图标（📚, ✍️, 🔍...）
    if tool_name == "get_chapter_by_order_tool":
        return f"📚 正在读取第{chapter_order}章..."
```

**规划状态**:

| 对比项 | 现有代码 | 文档规划 | 差距 |
|--------|----------|----------|------|
| 工具数量 | 8 个 | 22 个 | +14 个 |
| 映射结构 | `TOOL_DISPLAY_NAMES` (str) | `TOOL_DISPLAY_CONFIG` (dict含icon) | 需重构 |
| 图标方案 | emoji (📚✍️🔍) | Lucide (FileText, PenTool) | 需替换 |
| 描述生成 | `generate_tool_description` | `_build_tool_description` | 需扩展 |
| 缺失的工具 | - | read_chapter_tool, get_context_tool, smart_*, book_analysis 等 | 需添加 |

**实施步骤**:

1. ✅ 在 `EventParser` 中添加 `TOOL_DISPLAY_CONFIG`（保留旧的 `TOOL_DISPLAY_NAMES` 兼容）
2. ✅ 添加 `format_tool_display()` 方法
3. ✅ 扩展 `_build_tool_description()` 覆盖所有 22 个工具
4. ⏳ 前端使用 Lucide 图标渲染

### 8.5 AIPanel.tsx 布局调整

**文件**: `src/components/editor/AIPanel.tsx`

```tsx
// ==================== 布局调整 ====================

export function AIPanel({ ... }) {
  const { flowItems, tasks, isLoading, ... } = useAgentChat();

  return (
    <div className="flex flex-col h-full">
      {/* ==================== 上方：执行轨迹（可滚动）==================== */}
      <div className="flex-1 overflow-y-auto p-4">
        {/* 历史消息 */}
        {messages.map(msg => (
          <MessageItem key={msg.id} message={msg} />
        ))}

        {/* 🆕 执行轨迹（替换原有 ActivityStream 位置）*/}
        {isLoading && flowItems.length > 0 && (
          <ExecutionFlow items={flowItems} />
        )}

        {/* 流式输出内容（如果不在 flowItems 中单独显示）*/}
        {streamingContent && (
          <div className="text-sm text-slate-600 dark:text-slate-300">
            {streamingContent}
          </div>
        )}
      </div>

      {/* ==================== 底部固定：任务列表 ==================== */}
      {isLoading && tasks.length > 0 && (
        <div className="border-t border-slate-200 dark:border-slate-700
                        p-3 bg-slate-50 dark:bg-slate-900 flex-shrink-0">
          {/* 复用现有任务列表代码（1010-1069行）*/}
          <TaskList tasks={tasks} />
        </div>
      )}

      {/* 输入区域 */}
      <div className="border-t ...">
        <ChatInput ... />
      </div>
    </div>
  );
}
```

---

## 九、现有组件处理

### 9.1 ActivityStream 处理方案

**方案**：渐进式替换

```
Phase 1: 新增 ExecutionFlow（不动 ActivityStream）
├─ 通过开关切换显示哪个
└─ 两个可以共存，方便对比

Phase 2: 验证稳定后
├─ 默认使用新的 ExecutionFlow
└─ 移除 ActivityStream
```

### 9.2 功能开关

```tsx
// AIPanel.tsx
const ENABLE_EXECUTION_FLOW = true;

{ENABLE_EXECUTION_FLOW ? (
  <ExecutionFlow items={flowItems} />
) : (
  <ActivityStream activities={activities} />
)}
```

---

## 十、实施计划

### 10.1 任务分解

```
Phase 1: 执行轨迹可视化（3天）

Day 1: 后端准备
├─ [ ] Prompt 添加"先说再做"引导
├─ [ ] 实现 format_tool_display 函数
├─ [ ] SSE 事件增加 text/tool 类型
└─ [ ] 测试后端事件流

Day 2: 前端核心
├─ [ ] 创建 ExecutionFlow 组件
├─ [ ] 创建 TextBlock/ToolCard/ContentBlock 组件
├─ [ ] 调整 AIPanel 布局（任务列表移至底部固定）
├─ [ ] 修改 SSE 事件处理逻辑
└─ [ ] 实现布局（上滚动 + 下固定）

Day 3: 联调优化
├─ [ ] 端到端测试
├─ [ ] 样式调整
├─ [ ] 错误处理
└─ [ ] Bug 修复
```

### 10.2 验收标准

- [ ] 执行轨迹在上方，内容向上滚动
- [ ] 任务列表固定在底部（复用现有实现）
- [ ] AI 说明文字实时显示
- [ ] 工具调用显示为卡片样式（Lucide 图标 + Slate 配色）
- [ ] 完成的任务显示进度和耗时
- [ ] 思考、工具、内容按时间顺序交织显示
- [ ] 深色模式正确适配

---

## 十一、文件变更清单

### 11.1 后端

| 文件 | 变更类型 | 说明 |
|------|----------|------|
| `prompts/templates/*.yaml` | 修改 | 添加"先说再做"引导 |
| `services/agent/langgraph_agent.py` | 修改 | 提取 content 并发送 text 事件 |
| `api/v1/agent.py` | 修改 | 增加 format_tool_display 逻辑 |

### 11.2 前端

| 文件 | 变更类型 | 说明 |
|------|----------|------|
| `components/agent/ExecutionFlow.tsx` | 新增 | 执行轨迹容器组件 |
| `components/agent/TextBlock.tsx` | 新增 | AI 说明文字组件 |
| `components/agent/ToolCard.tsx` | 新增 | 工具调用卡片组件 |
| `components/agent/ContentBlock.tsx` | 新增 | 生成内容展示组件 |
| `components/editor/AIPanel.tsx` | 修改 | 调整布局：任务列表移至底部固定 |

> **注意**：任务列表复用现有实现（AIPanel.tsx:1010-1069），无需新增组件

---

## 十二、风险与回滚

### 12.1 风险

| 风险 | 概率 | 影响 | 缓解措施 |
|------|------|------|----------|
| AI 不输出思考文字 | 中 | 中 | Prompt 多轮调优 |
| SSE 连接不稳定 | 低 | 高 | 添加重连机制 |
| 布局兼容性问题 | 低 | 中 | 充分测试不同屏幕 |

### 12.2 回滚方案

```typescript
const ENABLE_EXECUTION_FLOW = false;  // 关闭开关即可回滚
```

---

## 十三、后续计划

Phase 1 完成后，进入 Phase 2：

```
Phase 2: interrupt 人机交互（2-3天）
├─ [ ] 后端 DeepAgentExecutor 添加中断点
├─ [ ] 前端 InterruptDialog 组件
├─ [ ] /resume API 端点
└─ [ ] 任务确认/跳过/修改流程
```

---

## 十四、参考

### 14.1 Cursor 风格特点

- AI 说明文字 → 普通文本，自然表达
- 工具调用 → 卡片样式，深灰背景
- 文件操作 → 显示文件名 + 行数变化（`+150 -0`）
- 按执行顺序从上到下

### 14.2 相关文档

- [11-discussion-summary.md](./11-discussion-summary.md) - 讨论总结索引
- [06-interrupt-resume.md](./06-interrupt-resume.md) - interrupt 机制设计

---

## 十五、深度 Review 问题记录

> 📅 Review 日期：2025-12-25
> 🔍 对比实际代码与文档规划的差异

### 15.1 🔴 严重问题（必须修复）

#### 问题 1：SSE 事件类型不匹配

| 对比项 | 文档规划 | 现有代码 | 差异 |
|--------|----------|----------|------|
| 事件类型 | `text`, `tool` | `progress`, `tool_call`, `content` | ❌ 不一致 |
| 事件位置 | `langgraph_agent.py` | `stream/stream_event_handler.py` | ⚠️ 文档未更新 |

**现有代码事件结构**:
```python
# stream/stream_event_handler.py
progress_event = {
    "type": "progress",
    "step": "tool_execution",  # intent_analysis/thinking/tool_execution/generating
    "description": "📚 正在读取第3章...",
    "node": "tools",
    "details": {...}
}
```

**建议**：文档应基于现有 `progress` 事件扩展，而非新增 `text`/`tool` 类型。

---

#### 问题 2：前端组件命名冲突

| 对比项 | 文档规划 | 现有代码 | 状态 |
|--------|----------|----------|------|
| 主组件 | `ExecutionFlow` | `ActivityStream` | ❌ 需明确替换策略 |
| hook 返回 | `flowItems` | `activities: ActivityItem[]` | ❌ 接口不一致 |
| 活动类型 | 未明确 | `intent_analysis/thinking/tool_execution/generating` | ⚠️ 文档未说明 |

**现有代码路径**:
- `src/components/agent/ActivityStream.tsx` ✅ 存在
- `src/hooks/useAgentChat.ts` → 返回 `activities` ✅
- `src/hooks/useAgentChatStream.ts` → 返回 `activities` ✅

**建议**：文档需明确是复用 `ActivityStream` 还是新建 `ExecutionFlow`。

---

### 15.2 🟡 中等问题（需要注意）

#### 问题 3：工具名称后缀不一致

| 来源文件 | 工具名称格式 | 示例 |
|----------|-------------|------|
| `langgraph_tools.py` | 带 `_tool` 后缀 | `continue_writing_tool` |
| `editor_tools.py` | 无后缀（`@tool` 装饰器） | `smart_continue` |
| `advanced_tools.py` | 无后缀（async def） | `book_analysis` |

**影响**：`TOOL_DISPLAY_CONFIG` 中的工具名必须与实际工具函数名一致。

**当前配置问题**:
```python
# 文档中的配置
"smart_continue": {...}  # ✅ 正确（editor_tools.py 中无后缀）
"continue_writing_tool": {...}  # ✅ 正确（langgraph_tools.py 中有后缀）
```

---

#### 问题 4：图标方案差异

| 对比项 | 文档规划 | 现有代码 |
|--------|----------|----------|
| 图标类型 | Lucide 名称（`FileText`） | emoji（📚✍️🔍） |
| 图标位置 | 后端返回 | 前端 `ActivityStream` 内部映射 |

**现有代码** (`ActivityStream.tsx`):
```tsx
const getActivityIcon = (type: AgentActivityType, status: ActivityStatus) => {
  switch (type) {
    case 'intent_analysis': return <Brain />;
    case 'thinking': return <Sparkles />;
    case 'tool_execution': return <Wrench />;
    case 'generating': return <Loader2 />;
  }
};
```

**建议**：保持前端图标映射（已用 Lucide），后端只需提供工具名和描述。

---

### 15.3 🟢 轻微问题（可选修复）

#### 问题 5：API 接口文档缺失

文档提到 `/resume` 端点，但未提供完整 API 规格：

```
待补充：
- POST /api/v1/agent/resume
- 请求体格式
- 响应格式
- 错误码
```

#### 问题 6：ActivityItem 类型文档

现有类型定义（`src/types/agent.ts:276-286`）未在文档中说明：

```typescript
interface ActivityItem {
  id: string;
  type: AgentActivityType;  // 'intent_analysis' | 'thinking' | 'tool_execution' | 'generating'
  description: string;
  timestamp: string;
  status: ActivityStatus;   // 'active' | 'completed' | 'failed'
  node?: string;
  tool?: string;
  details?: Record<string, any>;
  elapsedTime?: number;
}
```

---

### 15.4 修正建议汇总

| 优先级 | 问题 | 建议修正 |
|--------|------|----------|
| P0 | SSE 事件类型 | 基于现有 `progress` 事件扩展，添加 `icon` 字段 |
| P0 | 组件策略 | 明确：增强 `ActivityStream` 还是新建 `ExecutionFlow` |
| P1 | 工具名后缀 | 在文档中说明命名规则差异 |
| P1 | 图标方案 | 保持前端映射，后端只传工具名 |
| P2 | API 规格 | 补充 `/resume` 端点详细设计 |
| P2 | 类型文档 | 添加 `ActivityItem` 类型说明 |

---

**文档结束**
