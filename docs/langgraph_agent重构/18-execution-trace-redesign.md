# Agent 执行轨迹可视化 - 重新设计方案

## 文档版本
- 日期：2025-12-25
- 状态：设计中
- 作者：Claude

---

## 一、问题分析

### 1.1 之前方案的问题

之前的实施方案存在**根本性问题**：

```
❌ 在 stream_event_handler.py 中添加 on_text/on_tool 回调
❌ 在 langgraph_agent.py 的 chat_stream 方法中传递这些回调
❌ 在前端 useAgentChat.ts 的 react 模式分支中处理这些事件
```

**问题根源**：
1. **后端强制 Planning 模式**：`agent.py:859-861` 将任何模式都回退到 `planning`
2. **执行路径不匹配**：
   - `on_text/on_tool` 只在 `chat_stream()`（ReAct 模式）中被调用
   - API 层只调用 `chat_with_planning()`
   - 这些代码**永远不会执行**

### 1.2 现有事件流分析

**Planning 模式的实际事件流**：
```
用户请求 → API /chat/stream
    ↓
chat_with_planning()
    ├─ Phase 1: 规划
    │  └─ on_plan(plan_data) → SSE: {type: 'plan', data: {...}}
    ├─ Phase 2: 执行
    │  ├─ on_task_start(task) → SSE: {type: 'task_start', data: {...}}
    │  ├─ _execute_task()
    │  └─ on_task_done(task, result) → SSE: {type: 'task_done', data: {...}}
    └─ Phase 3: 响应
       └─ on_content(chunk) → SSE: {type: 'content', data: {...}}
```

**现有事件中包含的信息**：
| 事件类型 | 数据字段 |
|---------|---------|
| `plan` | `tasks: [{task_id, description, tool, params}]` |
| `task_start` | `task_id, description` |
| `task_done` | `task_id, description, elapsed_time` |
| `content` | 文本内容 |

**关键发现**：`plan` 事件的 `tasks` 数组中**已经包含 `tool` 字段**！

---

## 二、新方案设计

### 2.1 核心思路

**利用现有数据，而非新增事件类型**：
1. 前端已有 `tasks` 数据，包含 `tool` 字段
2. 添加前端 `TOOL_DISPLAY_CONFIG` 映射表
3. 在任务列表渲染时，根据 `tool` 字段显示对应图标

### 2.2 方案对比

| 方案 | 改动范围 | 复杂度 | 风险 |
|------|---------|--------|------|
| A: 增强任务列表 | 仅前端 | 低 | 低 |
| B: 新增 text/tool 事件 | 前后端 | 高 | 高 |
| C: 启用 ReAct 模式 | 前后端 | 很高 | 很高 |

**推荐方案 A**：仅修改前端，在任务列表中显示工具图标。

### 2.3 方案 A 详细设计

#### 改动清单

| 文件 | 改动内容 | 行数 |
|------|----------|------|
| `src/components/editor/AIPanel.tsx` | 添加工具图标映射和渲染 | +50行 |
| `src/types/agent.ts` | 扩展 Task 类型定义 | +5行 |

**总计**：约 55 行代码改动

#### 2.3.1 前端工具图标映射

```typescript
// src/components/editor/AIPanel.tsx 或单独文件

import {
  FileText, Search, Pencil, BookOpen, Zap,
  Globe, MessageSquare, FolderOpen, RefreshCw, Save, Wrench
} from 'lucide-react';

const TOOL_ICONS: Record<string, { icon: React.ReactNode; title: string }> = {
  // 章节读取类
  'read_chapter_tool': { icon: <FileText size={12} />, title: '读取章节' },
  'get_chapter_by_order_tool': { icon: <FileText size={12} />, title: '获取章节' },

  // 检索类
  'search_analysis_fragments_tool': { icon: <Search size={12} />, title: '检索片段' },
  'search_memory_tool': { icon: <Search size={12} />, title: '搜索记忆' },

  // 写作类
  'continue_writing_tool': { icon: <Pencil size={12} />, title: '续写' },
  'smart_continue': { icon: <Pencil size={12} />, title: '智能续写' },

  // 编辑类
  'smart_rewrite': { icon: <RefreshCw size={12} />, title: '改写' },
  'apply_chapter_edit': { icon: <Save size={12} />, title: '保存' },

  // 分析类
  'analyze_text': { icon: <BookOpen size={12} />, title: '分析' },

  // 默认
  '_default': { icon: <Wrench size={12} />, title: '工具' }
};

const getToolDisplay = (toolName?: string) => {
  if (!toolName) return TOOL_ICONS['_default'];
  return TOOL_ICONS[toolName] || TOOL_ICONS['_default'];
};
```

#### 2.3.2 任务列表增强渲染

```tsx
// AIPanel.tsx 任务列表渲染部分修改

{tasks.map((task) => {
  const toolDisplay = getToolDisplay(task.tool);

  return (
    <div key={task.task_id} className="flex items-start gap-2.5">
      {/* 工具图标 */}
      <div className={`flex-shrink-0 mt-1 ${
        task.status === 'running' ? 'text-blue-500 animate-pulse' :
        task.status === 'completed' ? 'text-green-500' : 'text-zinc-400'
      }`}>
        {toolDisplay.icon}
      </div>

      {/* 任务描述 */}
      <div className="flex-1 min-w-0">
        <p className={`text-[11px] ${
          task.status === 'running' ? 'text-zinc-700' : 'text-zinc-400'
        }`}>
          {task.description}
        </p>
      </div>

      {/* 耗时 */}
      {task.status === 'completed' && task.elapsed_time && (
        <span className="text-[10px] text-zinc-300 font-mono">
          {task.elapsed_time.toFixed(1)}s
        </span>
      )}
    </div>
  );
})}
```

---

## 三、实施步骤

### Day 1: 前端增强（约2小时）

#### [ ] Step 1: 添加工具图标映射
- 位置：`src/components/editor/AIPanel.tsx`
- 添加 `TOOL_ICONS` 常量和 `getToolDisplay` 函数

#### [ ] Step 2: 修改任务列表渲染
- 替换现有的小圆点指示器为工具图标
- 添加状态颜色和动画

#### [ ] Step 3: 测试验证
- 发送消息，确认图标正确显示
- 确认动画效果（running 时脉冲）
- 确认完成状态（绿色 + 耗时）

### Day 2: 可选增强

#### [ ] Step 4: 抽取为独立组件
- 创建 `TaskList.tsx` 组件
- 复用 ActivityStream 的样式

---

## 四、与之前方案的对比

| 维度 | 之前方案 | 新方案 |
|------|---------|--------|
| 后端改动 | 需要修改 3 个文件 | **不需要** |
| 新事件类型 | text, tool | **不需要** |
| 执行路径 | 需要启用 ReAct 模式 | **利用现有 Planning 模式** |
| 风险 | 高（可能破坏现有功能） | **低** |
| 工作量 | 约 180 行 | **约 55 行** |

---

## 五、回滚建议

之前添加的代码可以选择：
1. **保留**：为未来启用 ReAct 模式做准备
2. **回滚**：避免死代码，保持代码库整洁

如果选择回滚，需要还原以下文件：
- `backend/app/services/agent/stream/stream_event_handler.py`
- `backend/app/services/agent/langgraph_agent.py`
- `src/services/agentApi.ts`
- `src/hooks/useAgentChat.ts`
- `src/components/agent/ActivityStream.tsx`

---

## 六、总结

新方案的核心优势：
1. **简单**：只改前端，约 55 行代码
2. **安全**：利用现有数据流，不影响后端
3. **即时生效**：现有 plan 事件已包含 tool 字段
4. **可扩展**：后续可继续增强

---

**下一步行动**：
1. 确认是否采用新方案
2. 决定是否回滚之前的修改
3. 开始实施 Day 1 的步骤
