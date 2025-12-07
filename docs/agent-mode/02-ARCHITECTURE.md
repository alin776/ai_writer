# 02 - 架构设计

> 在 Planning 模式基础上增加反思循环，实现 DeepAgent 能力

## 0. 模块化设计原则

**核心原则**：`langgraph_agent.py` 已有 5000+ 行，**不再往里添加大量代码**。

DeepAgent 逻辑独立到新模块，同时需要在 API 层传递参数：

```
backend/app/services/agent/
├── langgraph_agent.py           # +6-8 行（导入 + 参数 + 分支）
│
├── deep_agent/                  # 新增目录
│   ├── __init__.py
│   ├── executor.py              # DeepAgentExecutor (~150 行)
│   ├── reflection.py            # think_tool + 反思逻辑 (~80 行)
│   └── config.py                # 配置常量 (~20 行)

backend/app/api/v1/
└── agent.py                     # +3-5 行（传递 enable_reflection 参数）

backend/app/models/
└── chat_models.py               # +1-2 行（请求模型添加字段）
```

**改动量评估**：

| 文件 | 改动 | 说明 |
|------|------|------|
| `langgraph_agent.py` | +6-8 行 | 导入 + 参数 + if 分支 |
| `agent.py` | +3-5 行 | 传递 enable_reflection 参数 |
| `chat_models.py` | +1-2 行 | AgentChatRequest 添加字段 |
| `deep_agent/executor.py` | 新建 ~150 行 | DeepAgentExecutor |
| `deep_agent/reflection.py` | 新建 ~80 行 | think_tool |
| `deep_agent/config.py` | 新建 ~20 行 | 配置常量 |
| **总计后端** | **~280 行** | |

## 1. 整体架构

```
┌─────────────────────────────────────────────────────────────────────┐
│                           前端层                                     │
├─────────────────────────────────────────────────────────────────────┤
│                                                                     │
│   AgentChatPanel ──────► useAgentChat ──────► TaskListPanel         │
│   (无需改动)              (MVP无需改动)        (MVP无需改动)          │
│                                                                     │
│                              │                                      │
│                              ▼                                      │
│                    事件处理 (已支持):                                 │
│                    • onPlan → 显示任务列表                           │
│                    • onTaskStart → 更新任务状态                      │
│                    • onTaskProgress → 显示反思内容（MVP复用此事件）   │
│                    • onTaskDone → 标记完成                           │
│                    • onContent → 流式内容                            │
│                                                                     │
└─────────────────────────────────────────────────────────────────────┘
                               │
                               │ SSE Stream (复用现有事件协议)
                               ▼
┌─────────────────────────────────────────────────────────────────────┐
│                           后端层                                     │
├─────────────────────────────────────────────────────────────────────┤
│                                                                     │
│   agent.py:agent_chat_stream()                                      │
│       │                                                             │
│       ▼ mode == ChatMode.PLANNING (默认)                            │
│                                                                     │
│   langgraph_agent.py:chat_with_planning()                           │
│   ┌─────────────────────────────────────────────────────────┐      │
│   │                                                          │      │
│   │  ┌──────────────────────────────────────────────────┐   │      │
│   │  │              Planning 阶段（现有）                │   │      │
│   │  │  • 分析用户请求                                   │   │      │
│   │  │  • 生成任务列表                                   │   │      │
│   │  │  • 发送 plan 事件                                 │   │      │
│   │  └──────────────────────────────────────────────────┘   │      │
│   │                          │                               │      │
│   │                          ▼                               │      │
│   │  ┌──────────────────────────────────────────────────┐   │      │
│   │  │              Execution 阶段（增强）               │   │      │
│   │  │                                                  │   │      │
│   │  │  ┌────────────────────────────────────────────┐ │   │      │
│   │  │  │ 反思循环 (新增)                             │ │   │      │
│   │  │  │                                            │ │   │      │
│   │  │  │  for task in tasks:                        │ │   │      │
│   │  │  │      执行任务 (MultiAgentExecutor)          │ │   │      │
│   │  │  │      │                                     │ │   │      │
│   │  │  │      ▼                                     │ │   │      │
│   │  │  │      if 需要反思:                          │ │   │      │
│   │  │  │          think_tool() → 发送反思内容        │ │   │      │
│   │  │  │          │                                 │ │   │      │
│   │  │  │          ▼                                 │ │   │      │
│   │  │  │          if 需要重规划:                    │ │   │      │
│   │  │  │              更新任务列表                   │ │   │      │
│   │  │  │              发送新的 plan 事件             │ │   │      │
│   │  │  └────────────────────────────────────────────┘ │   │      │
│   │  │                                                  │   │      │
│   │  └──────────────────────────────────────────────────┘   │      │
│   │                          │                               │      │
│   │                          ▼                               │      │
│   │  ┌──────────────────────────────────────────────────┐   │      │
│   │  │           Summarization 阶段（现有）              │   │      │
│   │  │  • 整合执行结果                                   │   │      │
│   │  │  • 发送 content 事件                              │   │      │
│   │  │  • 发送 done 事件                                 │   │      │
│   │  └──────────────────────────────────────────────────┘   │      │
│   │                                                          │      │
│   └─────────────────────────────────────────────────────────┘      │
│                                                                     │
│   复用组件 (无需修改):                                               │
│   ├── MultiAgentExecutor - 多 Agent 执行                            │
│   ├── DynamicToolRegistry - 工具注册                                │
│   ├── HTTPAIService - AI 服务                                       │
│   └── ProgressTracker - 进度追踪                                    │
│                                                                     │
└─────────────────────────────────────────────────────────────────────┘
```

## 2. 扩展点设计

### 2.1 在 chat_with_planning 中的扩展位置

```python
# langgraph_agent.py:chat_with_planning() 现有流程

async def chat_with_planning(
    self,
    message: str,
    context: dict,
    on_plan: Callable,
    on_task_start: Callable,
    on_task_done: Callable,
    on_content: Callable,
    ...
):
    # 阶段 1: Planning（现有）
    plan = await self._generate_plan(message, context)
    await on_plan(plan)

    # 阶段 2: Execution（增强点）
    for task in plan.tasks:
        await on_task_start(task)
        result = await self._execute_task(task)
        await on_task_done(task, result)

        # ════════════════════════════════════════════
        # 新增：反思检查点
        # ════════════════════════════════════════════
        if self._should_reflect(task, result):
            reflection = await self._think_tool(task, result)
            await on_content(f"💭 {reflection}")

            if self._should_replan(reflection):
                new_tasks = await self._replan(reflection, remaining_tasks)
                await on_plan({"tasks": new_tasks, "is_update": True})
        # ════════════════════════════════════════════

    # 阶段 3: Summarization（现有）
    summary = await self._summarize(results)
    await on_content(summary)
```

### 2.2 反思触发条件

```python
def _should_reflect(self, task: Task, result: TaskResult) -> bool:
    """判断是否需要触发反思"""

    # 条件 1: 任务失败
    if result.status == "failed":
        return True

    # 条件 2: 任务结果质量低
    if result.quality_score < 0.6:
        return True

    # 条件 3: 执行了关键任务（如分析类）
    if task.type in ["analysis", "planning"]:
        return True

    # 条件 4: 达到反思检查点（每 N 个任务）
    if self.state.completed_tasks % 3 == 0:
        return True

    return False
```

### 2.3 重规划判断

```python
def _should_replan(self, reflection: str) -> bool:
    """判断是否需要重新规划"""

    # 条件 1: 反思中明确提到需要新任务
    if "需要" in reflection and ("新增" in reflection or "补充" in reflection):
        return True

    # 条件 2: 反思中提到信息不足
    if "不足" in reflection or "缺少" in reflection:
        return True

    # 条件 3: 反思中提到调整计划
    if "调整" in reflection or "修改计划" in reflection:
        return True

    return False
```

## 3. 数据流

### 3.1 标准 Planning 模式数据流（现有）

```
用户消息
    │
    ▼
┌─────────────┐
│  Planning   │ ──────► plan 事件
│   阶段      │         {tasks: [...]}
└─────────────┘
    │
    ▼
┌─────────────┐
│  Execution  │ ──────► task_start 事件
│    阶段     │         task_done 事件
└─────────────┘
    │
    ▼
┌─────────────┐
│Summarization│ ──────► content 事件
│    阶段     │         done 事件
└─────────────┘
```

### 3.2 DeepAgent 模式数据流（增强）

```
用户消息
    │
    ▼
┌─────────────┐
│  Planning   │ ──────► plan 事件
│   阶段      │         {tasks: [...]}
└─────────────┘
    │
    ▼
┌──────────────────────────────────────────────────┐
│              Execution 阶段（增强）                │
│                                                  │
│  ┌─────────────┐                                 │
│  │  执行任务 1  │ ──────► task_start 事件         │
│  └─────────────┘         task_done 事件          │
│         │                                        │
│         ▼                                        │
│  ┌─────────────┐                                 │
│  │  反思检查   │ ──────► content 事件             │
│  │ (think_tool)│         "💭 反思内容..."        │
│  └─────────────┘                                 │
│         │                                        │
│         ▼                                        │
│  ┌─────────────┐                                 │
│  │ 需要重规划？ │                                 │
│  └─────────────┘                                 │
│      │      │                                    │
│      是     否                                   │
│      │      │                                    │
│      ▼      │                                    │
│  ┌──────────┐│                                   │
│  │ 生成新   ││──────► plan 事件 (更新)            │
│  │ 任务列表 ││        {tasks: [...], update: true}│
│  └──────────┘│                                   │
│      │       │                                   │
│      └───────┼──────► 继续执行下一个任务          │
│              │                                   │
│  ┌─────────────┐                                 │
│  │  执行任务 2  │                                 │
│  └─────────────┘                                 │
│         │                                        │
│        ...                                       │
│                                                  │
└──────────────────────────────────────────────────┘
    │
    ▼
┌─────────────┐
│Summarization│ ──────► content 事件
│    阶段     │         done 事件
└─────────────┘
```

### 3.3 事件序列示例

```
用户: 帮我写第三章，要承接前面的伏笔

事件序列:
1. plan         {tasks: [分析伏笔, 生成大纲, 撰写内容, 校验伏笔]}
2. task_start   {task_id: 1, description: "分析伏笔"}
3. task_done    {task_id: 1, status: "completed"}
4. content      "💭 分析发现3个伏笔，但血神宫线索不完整..."  ← 反思
5. plan         {tasks: [..., 深入分析血神宫], update: true}  ← 重规划
6. task_start   {task_id: 5, description: "深入分析血神宫"}   ← 新任务
7. task_done    {task_id: 5}
8. task_start   {task_id: 2, description: "生成大纲"}
9. ...
10. content     "第三章：血海深仇..."  ← 最终内容
11. done        {}
```

## 4. 状态管理

### 4.1 扩展后的状态

```python
# 现有状态
class PlanningState:
    tasks: List[Task]           # 任务列表
    current_task: Optional[Task] # 当前任务
    results: Dict[int, Any]     # 任务结果

# 扩展状态
class DeepAgentState(PlanningState):
    # 反思相关
    reflections: List[str]      # 反思历史
    reflection_count: int       # 反思次数
    max_reflections: int = 3    # 最大反思次数

    # 重规划相关
    replan_count: int           # 重规划次数
    max_replans: int = 2        # 最大重规划次数
    original_tasks: List[Task]  # 原始任务（用于对比）
```

### 4.2 状态转换

```
初始状态
    │
    ▼
┌─────────────────────────────────────────────────────┐
│  tasks: [task1, task2, task3]                       │
│  current_task: None                                 │
│  reflections: []                                    │
│  replan_count: 0                                    │
└─────────────────────────────────────────────────────┘
    │
    │  执行 task1，触发反思
    ▼
┌─────────────────────────────────────────────────────┐
│  tasks: [task1✓, task2, task3]                      │
│  current_task: None                                 │
│  reflections: ["分析发现伏笔信息不完整..."]           │
│  replan_count: 0                                    │
└─────────────────────────────────────────────────────┘
    │
    │  判断需要重规划
    ▼
┌─────────────────────────────────────────────────────┐
│  tasks: [task1✓, task1.5, task2, task3]  ← 插入新任务│
│  current_task: task1.5                              │
│  reflections: [...]                                 │
│  replan_count: 1                                    │
└─────────────────────────────────────────────────────┘
    │
    │  继续执行...
    ▼
┌─────────────────────────────────────────────────────┐
│  tasks: [task1✓, task1.5✓, task2✓, task3✓]         │
│  current_task: None                                 │
│  reflections: [...]                                 │
│  replan_count: 1                                    │
└─────────────────────────────────────────────────────┘
```

## 5. 复用分析

### 5.1 MVP 完全复用（0 改动）

| 组件 | 文件 | 说明 |
|------|------|------|
| TaskListPanel | `src/components/agent/TaskListPanel.tsx` | 已支持 progress_status 显示 |
| useAgentChat | `src/hooks/useAgentChat.ts` | 已有 onTaskProgress 处理 |
| AgentChatPanel | `src/components/agent/AgentChatPanel.tsx` | 布局无需改动 |
| agentApi | `src/services/agentApi.ts` | 已有 task_progress 事件解析 |
| MultiAgentExecutor | `backend/.../executor.py` | 任务执行逻辑复用 |
| HTTPAIService | `backend/.../ai_service.py` | AI 调用复用 |
| 事件协议 | SSE 格式 | task_progress 事件完全兼容 |

### 5.2 需要修改（后端）

| 组件 | 文件 | 改动量 | 改动内容 |
|------|------|--------|----------|
| chat_with_planning | `langgraph_agent.py` | +6-8 行 | 添加 enable_reflection 参数和分支 |
| agent_chat_stream | `agent.py` | +3-5 行 | 传递 enable_reflection 参数 |
| AgentChatRequest | `chat_models.py` | +1-2 行 | 添加 enable_reflection 字段 |
| deep_agent 模块 | 新建 | ~260 行 | 完整的反思逻辑 |

### 5.3 完整版改动（前端可选）

| 组件 | 文件 | 改动量 | 改动内容 |
|------|------|--------|----------|
| TaskListPanel | `TaskListPanel.tsx` | +35 行 | 反思气泡、新增任务标记 |
| useAgentChat | `useAgentChat.ts` | +15 行 | is_update 处理逻辑 |
| agentApi | `agentApi.ts` | +10 行 | reflection 事件解析 |

## 6. 目录结构

### 6.1 现有结构（不变）

```
backend/app/services/agent/
├── langgraph_agent.py          # 主入口
├── multi_agent/
│   └── executor.py             # Multi-Agent 执行器
├── tools/
│   ├── writing_tools.py        # 写作工具
│   └── analysis_tools.py       # 分析工具
└── actions/
    └── ...
```

### 6.2 新增/修改文件

```
backend/app/services/agent/
├── langgraph_agent.py          # 修改: +6-8 行（参数 + 分支）
│
└── deep_agent/                 # 新增目录
    ├── __init__.py
    ├── config.py               # 配置常量
    ├── reflection.py           # think_tool
    └── executor.py             # DeepAgentExecutor

backend/app/api/v1/
└── agent.py                    # 修改: +3-5 行（传递参数）

backend/app/models/
└── chat_models.py              # 修改: +1-2 行（请求字段）
```

## 7. 风险控制

### 7.1 反思次数限制

```python
MAX_REFLECTIONS = 3  # 单次请求最多反思 3 次
MAX_REPLANS = 2      # 单次请求最多重规划 2 次
```

### 7.2 超时保护

```python
REFLECTION_TIMEOUT = 30   # 反思超时 30 秒
REPLAN_TIMEOUT = 45       # 重规划超时 45 秒
TOTAL_TIMEOUT = 360       # 总超时保持 6 分钟
```

### 7.3 回退机制

```python
try:
    reflection = await self._think_tool(task, result)
except TimeoutError:
    # 超时：跳过反思，继续执行
    logger.warning("反思超时，跳过")
    continue
except Exception as e:
    # 异常：记录错误，继续执行
    logger.error(f"反思失败: {e}")
    continue
```
