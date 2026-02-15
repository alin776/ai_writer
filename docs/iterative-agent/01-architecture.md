# 01 - 架构设计

## 整体架构

> ⚠️ 实现载体为 **DeepAgentExecutor 增强版**，下图的 IterativeExecutor 为概念层名称。  
> 事件命名以 planning SSE 为准（`task_done` 为主，`task_complete` 仅别名）。

```
┌─────────────────────────────────────────────────────────────┐
│                      用户请求                                │
└─────────────────────────────────────────────────────────────┘
                           │
                           ▼
┌─────────────────────────────────────────────────────────────┐
│                   IterativeExecutor                          │
│  ┌─────────────────────────────────────────────────────┐   │
│  │  PlanGenerator    │  初始规划（复用）                │   │
│  ├─────────────────────────────────────────────────────┤   │
│  │  DynamicPlan      │  动态计划管理（新增）            │   │
│  ├─────────────────────────────────────────────────────┤   │
│  │  TaskRunner       │  任务执行（复用）                │   │
│  ├─────────────────────────────────────────────────────┤   │
│  │  ReflectionEngine │  反思决策（增强）                │   │
│  ├─────────────────────────────────────────────────────┤   │
│  │  ResponseBuilder  │  最终响应（复用）                │   │
│  └─────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────┘
                           │
                           ▼
┌─────────────────────────────────────────────────────────────┐
│                   StreamEventHandler                         │
│  发送事件：plan / task_start / task_done / thinking /       │
│           plan_update / final                               │
└─────────────────────────────────────────────────────────────┘
                           │
                           ▼
┌─────────────────────────────────────────────────────────────┐
│                      前端 AIPanel                            │
│  展示：任务列表 / 执行状态 / AI思考 / 最终响应              │
└─────────────────────────────────────────────────────────────┘
```

## 模块职责

### 1. IterativeExecutor（概念层，落地为 DeepAgentExecutor）

**职责**：协调整个迭代执行流程

```python
class IterativeExecutor:
    """迭代执行器 - 核心协调者"""

    def __init__(self):
        self.plan_generator = PlanGenerator()
        self.task_runner = TaskRunner()
        self.reflection_engine = ReflectionEngine()
        self.response_builder = ResponseBuilder()

    async def execute(self, request, state) -> AsyncGenerator:
        """执行入口，返回事件流"""
        pass
```

### 2. DynamicPlan（新增）

**职责**：管理可动态调整的任务计划

```python
class DynamicPlan:
    """动态计划管理"""

    def __init__(self, tasks: List[Task]):
        self.tasks = tasks

    def get_next(self) -> Optional[Task]: ...
    def insert_after_current(self, task: Task): ...
    def skip_task(self, task_id: str): ...
    def has_pending(self) -> bool: ...
```

### 3. ReflectionEngine（增强）

**职责**：任务执行后的反思决策

```python
class ReflectionEngine:
    """反思引擎 - 基于现有 think_tool 增强"""

    async def reflect(
        self,
        task: Task,
        result: TaskResult,
        remaining_tasks: List[Task],
        user_request: str
    ) -> ReflectionResult:
        """反思并决定下一步"""
        pass
```

## 数据流

```
1. 用户请求 → DeepAgentExecutor.execute_with_reflection()（概念上等同 IterativeExecutor.execute）

2. 初始规划：
   PlanGenerator.generate() → tasks[]
   → 发送 plan 事件

3. 迭代循环：
   while DynamicPlan.has_pending():
       task = DynamicPlan.get_next()
       → 发送 task_start 事件

       result = TaskRunner.execute(task)
       → 发送 task_done 事件

       decision = ReflectionEngine.reflect(task, result)
       → 发送 thinking 事件

       if decision.action == "add_task":
           DynamicPlan.insert(decision.new_task)
           → 发送 plan_update 事件

4. 最终响应：
   ResponseBuilder.build(all_results)
   → 发送 final 事件
```

## 复用关系

| 模块 | 复用方式 |
|------|----------|
| PlanGenerator | 100% 复用 |
| TaskRunner | 100% 复用 |
| ResponseBuilder | 100% 复用 |
| think_tool | 增强输出格式 |
| StreamEventHandler | 新增事件类型 |
