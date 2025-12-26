# Agent 执行轨迹可视化方案

## 文档版本
- 版本：5.0 (完整版)
- 日期：2025-12-25
- 类型：技术方案
- 状态：✅ 基于实际架构设计，支持"AI 说明 + 工具卡片交织"效果

---

## 〇、方案概述

### 0.1 目标效果

达到 `preview-execution-trace.html` 预览的 UI 效果：

```
┌─────────────────────────────────────────────────────────────┐
│  AI: 我先读取第3章的内容，了解当前的剧情进展                    │
│  ┌─ 工具卡片 ────────────────────────────────────────────┐  │
│  │ [FileText] 读取章节  ·  第3章                    ✓    │  │
│  └───────────────────────────────────────────────────────┘  │
│  AI: 好的，接下来让我检索一下相关的角色设定                     │
│  ┌─ 工具卡片 ────────────────────────────────────────────┐  │
│  │ [Search] 检索设定    ·  主角性格                 ✓    │  │
│  └───────────────────────────────────────────────────────┘  │
│  AI: 现在开始续写后续内容                                     │
│  ┌─ 工具卡片 ────────────────────────────────────────────┐  │
│  │ [PenTool] 续写内容   ·  约500字                 ⟳    │  │
│  └───────────────────────────────────────────────────────┘  │
│  流式输出: 林风深吸一口气，眼中闪过一丝决然...                  │
├─────────────────────────────────────────────────────────────┤
│  任务列表（底部固定）                                 2/3    │
│  ● 读取第3章内容                                    1.2s    │
│  ● 检索角色设定                                     0.8s    │
│  ○ 续写战斗场景                                            │
└─────────────────────────────────────────────────────────────┘
```

### 0.2 改动量估算

| 层级 | 文件 | 改动行数 | 说明 |
|------|------|---------|------|
| **后端** | `agent.py` | +30行 | 增强 `task_start` 事件，添加 `explanation` 字段 |
| **前端** | `agentApi.ts` | +5行 | 无需修改（已有 `onTaskStart`） |
| **前端** | `useAgentChat.ts` | +40行 | 添加 `flowItems` 状态管理 |
| **前端** | `ExecutionFlow/` | +120行 | 新建组件目录 |
| **前端** | `AIPanel.tsx` | +20行 | 使用 ExecutionFlow 替换现有渲染 |
| **总计** | 5 文件 | **~215行** | |

---

## 一、核心问题：AI 说明文字从哪来？

### 1.1 现有 Planning 数据结构

```python
# plan_data 结构
{
    "thinking": {
        "step1_output": "用户期望的输出形式",
        "step2_material": "需要的原料",
        "step3_process": "处理方式"
    },
    "user_intent": "概括第三章内容",
    "tasks": [
        {
            "task_id": 1,
            "description": "获取第三章",           # ✅ 已有友好描述
            "tool": "get_chapter_by_order_tool",
            "params": {"chapter_order": 3}
        },
        {
            "task_id": 2,
            "description": "概括内容",
            "tool": "analyze_text_tool",
            "params": {"text": "$TASK_1.content$", "focus": "概括主要内容"}
        }
    ]
}
```

### 1.2 解决方案：利用 description 生成 explanation

**核心思路**：`task.description` 已经是友好的描述，后端添加自然语言前缀即可

```python
# 后端生成 explanation
def generate_explanation(task_index: int, task: dict) -> str:
    """根据任务位置和内容生成自然语言说明"""
    desc = task.get("description", "")
    tool = task.get("tool", "")

    # 首个任务
    if task_index == 0:
        prefixes = ["我先", "首先让我", "让我先"]
    # 后续任务
    else:
        prefixes = ["接下来", "然后", "好的，现在"]

    prefix = prefixes[task_index % len(prefixes)]

    # 工具特定的后缀
    if "read" in tool or "get_chapter" in tool:
        suffix = "，了解当前内容"
    elif "search" in tool:
        suffix = "，查找相关信息"
    elif "continue_writing" in tool:
        suffix = ""
    elif "analyze" in tool:
        suffix = ""
    else:
        suffix = ""

    return f"{prefix}{desc}{suffix}"
```

**示例输出**：

| task_index | description | explanation |
|------------|-------------|-------------|
| 0 | "获取第三章" | "我先获取第三章，了解当前内容" |
| 1 | "检索角色设定" | "接下来检索角色设定，查找相关信息" |
| 2 | "续写内容" | "好的，现在续写内容" |

---

## 二、后端改动方案

### 2.1 修改 agent.py：增强 task_start 事件

**位置**：`backend/app/api/v1/agent.py:1107-1143`

```python
# 现有代码
async def on_task_start(task):
    await event_queue.put(('task_start', task))

# 修改为
async def on_task_start(task):
    # 获取任务索引（从 plan_data 中）
    task_index = next(
        (i for i, t in enumerate(plan_data.get("tasks", []))
         if t.get("task_id") == task.get("task_id")),
        0
    )

    # 生成自然语言说明
    explanation = generate_explanation(task_index, task)

    # 增强事件数据
    enhanced_task = {
        **task,
        "explanation": explanation,
        "icon": get_tool_icon(task.get("tool")),
        "tool_title": get_tool_title(task.get("tool")),
        "tool_description": build_tool_description(task)
    }

    await event_queue.put(('task_start', enhanced_task))
```

### 2.2 添加辅助函数

```python
# 工具图标映射（Lucide 图标名）
TOOL_ICONS = {
    "get_chapter_by_order_tool": "FileText",
    "read_chapter_tool": "FileText",
    "get_context_tool": "BookOpen",
    "search_analysis_fragments_tool": "Search",
    "search_memory_tool": "Search",
    "continue_writing_tool": "PenTool",
    "smart_continue": "PenTool",
    "smart_rewrite": "Edit3",
    "smart_insert": "Plus",
    "analyze_text_tool": "BarChart2",
    "apply_chapter_edit": "Check",
    "_default": "Wrench"
}

TOOL_TITLES = {
    "get_chapter_by_order_tool": "读取章节",
    "read_chapter_tool": "读取章节",
    "get_context_tool": "获取上下文",
    "search_analysis_fragments_tool": "检索设定",
    "search_memory_tool": "搜索记忆",
    "continue_writing_tool": "续写内容",
    "smart_continue": "智能续写",
    "smart_rewrite": "智能改写",
    "smart_insert": "智能插入",
    "analyze_text_tool": "分析文本",
    "apply_chapter_edit": "应用修改",
    "_default": "工具调用"
}

def get_tool_icon(tool_name: str) -> str:
    return TOOL_ICONS.get(tool_name, TOOL_ICONS["_default"])

def get_tool_title(tool_name: str) -> str:
    return TOOL_TITLES.get(tool_name, TOOL_TITLES["_default"])

def build_tool_description(task: dict) -> str:
    """构建工具调用的简短描述"""
    tool = task.get("tool", "")
    params = task.get("params", {})

    if tool in ["get_chapter_by_order_tool", "read_chapter_tool"]:
        chapter = params.get("chapter_order") or params.get("chapter_id", "")
        return f"第{chapter}章" if chapter else ""

    if tool == "search_analysis_fragments_tool":
        query = params.get("query", "")
        return query[:20] if query else "检索中..."

    if tool == "continue_writing_tool":
        words = params.get("target_words", 500)
        return f"约{words}字"

    if tool == "analyze_text_tool":
        focus = params.get("focus", "")
        return focus[:15] if focus else "分析中..."

    return ""

def generate_explanation(task_index: int, task: dict) -> str:
    """生成任务说明"""
    desc = task.get("description", "")
    tool = task.get("tool", "")

    if task_index == 0:
        prefix = "我先"
    elif task_index == 1:
        prefix = "接下来"
    else:
        prefix = "然后"

    # 工具特定后缀
    if "read" in tool or "get_chapter" in tool:
        suffix = "，了解当前内容："
    elif "search" in tool:
        suffix = "："
    else:
        suffix = "："

    return f"{prefix}{desc}{suffix}"
```

### 2.3 增强后的 task_start 事件格式

```json
{
    "type": "task_start",
    "data": {
        "task_id": 1,
        "description": "获取第三章",
        "tool": "get_chapter_by_order_tool",
        "params": {"chapter_order": 3},

        // 新增字段
        "explanation": "我先获取第三章，了解当前内容：",
        "icon": "FileText",
        "tool_title": "读取章节",
        "tool_description": "第3章"
    }
}
```

---

## 三、前端改动方案

### 3.1 数据流设计

```
┌─────────────────────────────────────────────────────────────┐
│                       完整数据流                              │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  SSE 事件流                                                  │
│  ├─ task_start → {explanation, icon, tool_title, ...}       │
│  ├─ task_done  → {task_id, elapsed_time}                    │
│  └─ content    → "流式文本..."                               │
│                                                             │
│  useAgentChat.ts                                            │
│  ├─ onTaskStart → flowItems.push({type: 'text', ...})       │
│  │             → flowItems.push({type: 'tool', ...})        │
│  ├─ onTaskDone  → 更新 tool 项的 status                      │
│  └─ onContent   → flowItems.push/update({type: 'content'})  │
│                                                             │
│  AIPanel.tsx                                                │
│  ├─ <ExecutionFlow items={flowItems} />  // 上方可滚动      │
│  └─ <TaskList tasks={tasks} />           // 底部固定        │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

### 3.2 FlowItem 类型定义

```typescript
// src/types/agent.ts 新增

interface FlowItem {
  id: string;
  type: 'text' | 'tool' | 'content';
  data: TextData | ToolData | ContentData;
  timestamp: string;
}

interface TextData {
  content: string;  // AI 说明文字
}

interface ToolData {
  taskId: number;
  icon: string;           // Lucide 图标名
  title: string;          // 工具标题
  description: string;    // 工具描述
  status: 'running' | 'done' | 'error';
}

interface ContentData {
  content: string;  // 流式内容
}
```

### 3.3 useAgentChat.ts 改动

```typescript
// 新增状态
const [flowItems, setFlowItems] = useState<FlowItem[]>([]);
const flowItemsRef = useRef<FlowItem[]>([]);

// 修改 onTaskStart 回调
onTaskStart: (task: any) => {
  // 1. 添加 AI 说明文字
  if (task.explanation) {
    const textItem: FlowItem = {
      id: `text_${task.task_id}_${Date.now()}`,
      type: 'text',
      data: { content: task.explanation },
      timestamp: new Date().toISOString()
    };
    flowItemsRef.current = [...flowItemsRef.current, textItem];
  }

  // 2. 添加工具卡片
  const toolItem: FlowItem = {
    id: `tool_${task.task_id}`,
    type: 'tool',
    data: {
      taskId: task.task_id,
      icon: task.icon || 'Wrench',
      title: task.tool_title || '工具调用',
      description: task.tool_description || '',
      status: 'running'
    },
    timestamp: new Date().toISOString()
  };
  flowItemsRef.current = [...flowItemsRef.current, toolItem];

  // 更新状态
  setFlowItems([...flowItemsRef.current]);

  // 保持现有逻辑
  // ... tasks 状态更新
},

// 修改 onTaskDone 回调
onTaskDone: (taskDone: any) => {
  // 更新工具卡片状态
  flowItemsRef.current = flowItemsRef.current.map(item => {
    if (item.type === 'tool' && (item.data as ToolData).taskId === taskDone.task_id) {
      return {
        ...item,
        data: { ...(item.data as ToolData), status: 'done' }
      };
    }
    return item;
  });
  setFlowItems([...flowItemsRef.current]);

  // 保持现有逻辑
  // ... tasks 状态更新
},

// 修改 onContent 回调
onContent: (chunk: string) => {
  // 更新或创建 content 项
  const existingContent = flowItemsRef.current.find(item => item.type === 'content');

  if (existingContent) {
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
    const contentItem: FlowItem = {
      id: `content_${Date.now()}`,
      type: 'content',
      data: { content: chunk },
      timestamp: new Date().toISOString()
    };
    flowItemsRef.current = [...flowItemsRef.current, contentItem];
  }

  setFlowItems([...flowItemsRef.current]);

  // 保持现有打字机效果逻辑
  // ...
},

// 清空 flowItems（开始新对话时）
onStart: (conversationId: string) => {
  flowItemsRef.current = [];
  setFlowItems([]);
  // ...
},

// 返回 flowItems
return {
  // ... 现有返回值
  flowItems,
};
```

### 3.4 ExecutionFlow 组件

**目录结构**：
```
src/components/agent/ExecutionFlow/
├── index.tsx
├── ExecutionFlow.module.css
├── TextBlock.tsx
├── ToolCard.tsx
└── ContentBlock.tsx
```

#### index.tsx

```tsx
import { FlowItem } from '@/types/agent';
import { TextBlock } from './TextBlock';
import { ToolCard } from './ToolCard';
import { ContentBlock } from './ContentBlock';
import styles from './ExecutionFlow.module.css';

interface ExecutionFlowProps {
  items: FlowItem[];
}

export function ExecutionFlow({ items }: ExecutionFlowProps) {
  return (
    <div className={styles.container}>
      {items.map((item) => {
        switch (item.type) {
          case 'text':
            return <TextBlock key={item.id} content={item.data.content} />;
          case 'tool':
            return <ToolCard key={item.id} {...item.data} />;
          case 'content':
            return <ContentBlock key={item.id} content={item.data.content} />;
          default:
            return null;
        }
      })}
    </div>
  );
}
```

#### TextBlock.tsx

```tsx
import styles from './ExecutionFlow.module.css';

interface TextBlockProps {
  content: string;
}

export function TextBlock({ content }: TextBlockProps) {
  return (
    <p className={styles.textBlock}>{content}</p>
  );
}
```

#### ToolCard.tsx

```tsx
import {
  FileText, Search, PenTool, Edit3, Plus, Check,
  BarChart2, BookOpen, RefreshCw, Wrench, Loader2, CheckCircle
} from 'lucide-react';
import styles from './ExecutionFlow.module.css';

const ICON_MAP: Record<string, React.ComponentType<any>> = {
  FileText, Search, PenTool, Edit3, Plus, Check,
  BarChart2, BookOpen, RefreshCw, Wrench
};

interface ToolCardProps {
  taskId: number;
  icon: string;
  title: string;
  description: string;
  status: 'running' | 'done' | 'error';
}

export function ToolCard({ icon, title, description, status }: ToolCardProps) {
  const IconComponent = ICON_MAP[icon] || Wrench;

  return (
    <div className={`${styles.toolCard} ${styles[status]}`}>
      <div className={`${styles.toolIcon} ${styles[status]}`}>
        <IconComponent size={14} />
      </div>

      <div className={styles.toolContent}>
        <div className={styles.toolTitle}>{title}</div>
        {description && (
          <div className={styles.toolMeta}>
            <span className={styles.toolTag}>{description}</span>
          </div>
        )}
      </div>

      <div className={styles.toolStatus}>
        {status === 'running' && <Loader2 size={14} className={styles.spin} />}
        {status === 'done' && <CheckCircle size={14} className={styles.check} />}
      </div>
    </div>
  );
}
```

#### ContentBlock.tsx

```tsx
import styles from './ExecutionFlow.module.css';

interface ContentBlockProps {
  content: string;
}

export function ContentBlock({ content }: ContentBlockProps) {
  return (
    <div className={styles.contentBlock}>
      <div className={styles.contentText}>{content}</div>
    </div>
  );
}
```

#### ExecutionFlow.module.css

```css
.container {
  padding: 16px;
}

/* AI 说明文字 */
.textBlock {
  font-size: 13px;
  color: var(--slate-600);
  line-height: 1.6;
  margin: 10px 0;
}

/* 工具卡片 */
.toolCard {
  display: flex;
  gap: 10px;
  padding: 10px;
  border-radius: 10px;
  border: 1px solid var(--slate-200);
  background: var(--slate-50);
  margin: 10px 0;
}

.toolCard.running {
  border-color: var(--blue-200);
  background: var(--blue-50);
}

.toolCard.done {
  border-color: var(--emerald-100);
  background: var(--emerald-50);
}

.toolIcon {
  width: 28px;
  height: 28px;
  border-radius: 999px;
  background: #eef2ff;
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
}

.toolIcon.running svg {
  color: var(--blue-600);
}

.toolIcon.done svg {
  color: var(--emerald-500);
}

.toolContent {
  flex: 1;
  min-width: 0;
}

.toolTitle {
  font-size: 13px;
  font-weight: 500;
  color: var(--slate-800);
}

.toolMeta {
  margin-top: 4px;
}

.toolTag {
  font-size: 11px;
  padding: 2px 6px;
  border-radius: 999px;
  background: var(--sky-100);
  color: var(--sky-700);
}

.toolStatus {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 20px;
}

.spin {
  animation: spin 1s linear infinite;
  color: var(--blue-500);
}

.check {
  color: var(--emerald-500);
}

@keyframes spin {
  to { transform: rotate(360deg); }
}

/* 内容块 */
.contentBlock {
  margin: 12px 0;
}

.contentText {
  font-size: 13px;
  color: var(--slate-500);
  line-height: 1.7;
  white-space: pre-wrap;
}

/* 深色模式 */
@media (prefers-color-scheme: dark) {
  .textBlock { color: var(--slate-300); }

  .toolCard {
    background: var(--slate-800);
    border-color: var(--slate-700);
  }

  .toolCard.running {
    background: rgba(59, 130, 246, 0.1);
    border-color: rgba(59, 130, 246, 0.3);
  }

  .toolCard.done {
    background: rgba(16, 185, 129, 0.1);
    border-color: rgba(16, 185, 129, 0.3);
  }

  .toolIcon { background: var(--slate-700); }
  .toolTitle { color: var(--slate-200); }
  .contentText { color: var(--slate-300); }
}
```

### 3.5 AIPanel.tsx 改动

```tsx
// 导入 ExecutionFlow
import { ExecutionFlow } from '@/components/agent/ExecutionFlow';

// 在组件中获取 flowItems
const { flowItems, tasks, isLoading, ... } = useAgentChat();

// 渲染布局
return (
  <div className="flex flex-col h-full">
    {/* 上方：可滚动区域 */}
    <div className="flex-1 overflow-y-auto p-4">
      {/* 历史消息 */}
      {messages.map(msg => (
        <MessageItem key={msg.id} message={msg} />
      ))}

      {/* 执行轨迹（替换原有 ActivityStream） */}
      {isLoading && flowItems.length > 0 && (
        <ExecutionFlow items={flowItems} />
      )}
    </div>

    {/* 底部固定：任务列表 */}
    {isLoading && tasks.length > 0 && (
      <div className="border-t border-slate-200 dark:border-slate-700
                      p-3 bg-slate-50 dark:bg-slate-900 flex-shrink-0">
        {/* 复用现有任务列表代码（1010-1069行） */}
        <TaskList tasks={tasks} />
      </div>
    )}

    {/* 输入区域 */}
    <div className="border-t ...">
      <ChatInput ... />
    </div>
  </div>
);
```

---

## 四、完整事件流示例

```
用户发送: "帮我概括第三章的内容"

后端流程:
1. [规划阶段] PlanGenerator 生成规划
   → SSE: plan 事件

2. [执行阶段] task_start (task_id=1)
   → SSE: {
       "type": "task_start",
       "data": {
         "task_id": 1,
         "description": "获取第三章",
         "tool": "get_chapter_by_order_tool",
         "explanation": "我先获取第三章，了解当前内容：",
         "icon": "FileText",
         "tool_title": "读取章节",
         "tool_description": "第3章"
       }
     }

3. [执行完成] task_done (task_id=1)
   → SSE: {"type": "task_done", "data": {"task_id": 1, "elapsed_time": 1.2}}

4. [执行阶段] task_start (task_id=2)
   → SSE: {
       "type": "task_start",
       "data": {
         "task_id": 2,
         "description": "概括内容",
         "tool": "analyze_text_tool",
         "explanation": "接下来概括内容：",
         "icon": "BarChart2",
         "tool_title": "分析文本",
         "tool_description": "概括主要内容"
       }
     }

5. [内容生成] content 事件流
   → SSE: {"type": "content", "data": "第三章主要讲述了..."}
   → SSE: {"type": "content", "data": "主角林风在..."}

6. [执行完成] task_done (task_id=2)
   → SSE: {"type": "task_done", "data": {"task_id": 2, "elapsed_time": 3.5}}

7. [结束] done 事件
   → SSE: {"type": "done", ...}

前端 flowItems 状态变化:
初始: []
→ [{type: 'text', data: {content: '我先获取第三章...'}}]
→ [..., {type: 'tool', data: {icon: 'FileText', status: 'running', ...}}]
→ [..., (tool status → 'done')]
→ [..., {type: 'text', data: {content: '接下来概括内容：'}}]
→ [..., {type: 'tool', data: {icon: 'BarChart2', status: 'running', ...}}]
→ [..., {type: 'content', data: {content: '第三章主要讲述了...'}}]
→ [..., (content 追加), (tool status → 'done')]
```

---

## 五、实施计划

### 5.1 任务分解

```
Day 1: 后端改动（2小时）
├─ [1] 在 agent.py 添加辅助函数（TOOL_ICONS, generate_explanation 等）
├─ [2] 修改 on_task_start 回调，增强事件数据
└─ [3] 测试 SSE 事件输出

Day 2: 前端核心（3小时）
├─ [1] 在 types/agent.ts 添加 FlowItem 类型
├─ [2] 修改 useAgentChat.ts，添加 flowItems 状态管理
├─ [3] 创建 ExecutionFlow 组件目录和文件
└─ [4] 修改 AIPanel.tsx 布局

Day 3: 联调优化（2小时）
├─ [1] 端到端测试
├─ [2] 样式微调
├─ [3] 深色模式验证
└─ [4] 边缘情况处理
```

### 5.2 验收标准

- [ ] 每个任务开始时显示 AI 说明文字
- [ ] 工具卡片显示图标、标题、描述
- [ ] 工具卡片状态随执行变化（running → done）
- [ ] 流式内容在工具卡片后实时显示
- [ ] 任务列表固定在底部
- [ ] 深色模式正常显示

---

## 六、文件变更清单

| 文件 | 变更类型 | 行数 | 说明 |
|------|----------|------|------|
| `backend/app/api/v1/agent.py` | 修改 | +30 | 增强 task_start 事件 |
| `src/types/agent.ts` | 修改 | +15 | 添加 FlowItem 类型 |
| `src/hooks/useAgentChat.ts` | 修改 | +40 | 添加 flowItems 状态 |
| `src/components/agent/ExecutionFlow/index.tsx` | 新增 | +30 | 主容器组件 |
| `src/components/agent/ExecutionFlow/TextBlock.tsx` | 新增 | +15 | AI 说明文字 |
| `src/components/agent/ExecutionFlow/ToolCard.tsx` | 新增 | +50 | 工具卡片 |
| `src/components/agent/ExecutionFlow/ContentBlock.tsx` | 新增 | +15 | 内容块 |
| `src/components/agent/ExecutionFlow/ExecutionFlow.module.css` | 新增 | +100 | 样式 |
| `src/components/editor/AIPanel.tsx` | 修改 | +20 | 使用 ExecutionFlow |

**总计**：9 个文件，约 315 行代码

---

## 七、与 v4.0 简化版的对比

| 对比项 | v4.0 简化版 | v5.0 完整版 |
|--------|-------------|-------------|
| 后端改动 | 0 | +30行 |
| 前端改动 | ~50行 | ~285行 |
| AI 说明文字 | ❌ 无 | ✅ 有 |
| 工具卡片 | ❌ 只有图标 | ✅ 完整卡片 |
| 交织布局 | ❌ 只有任务列表 | ✅ 说明 + 卡片交织 |
| UI 效果 | 简单 | 达到 preview 效果 |

---

## 八、回滚方案

```typescript
// AIPanel.tsx
const ENABLE_EXECUTION_FLOW = true;  // 开关

{ENABLE_EXECUTION_FLOW && isLoading && flowItems.length > 0 ? (
  <ExecutionFlow items={flowItems} />
) : (
  // 原有渲染逻辑
)}
```

---

**文档结束**

> 📝 本文档基于 2025-12-25 对项目代码的深度探索，设计完整版方案。
>
> 关键发现：
> - `task.description` 已是友好描述，可直接用于生成 explanation
> - 现有 `task_start` 事件只需增强，无需新增事件类型
> - 前端只需添加 `flowItems` 状态，复用现有事件处理
