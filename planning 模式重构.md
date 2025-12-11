# Planning 模式重构

## 一、问题分析（原始讨论保留）

### 三层架构的问题

```
原设计：Planning → DeepAgent → MultiAgent（三层嵌套，职责重叠）
```

**职责重叠点**：
1. 任务执行循环 - 三层各有自己的 `for task in tasks`
2. 失败处理和重试 - 三层都有自己的逻辑
3. 动态任务生成 - Planning 和 DeepAgent 都能生成/修改任务
4. 事件发送 - 三层都往前端发事件，命名空间冲突
5. 上下文管理 - 三层各自维护 context，数据重复传递

**根本原因**：三层是在不同时期、为了不同目的独立开发的，没有统一设计。

---

## 二、重构方案演进

### 最初方案（2025-12-10 讨论）

```
目标：Planning（内置反思 + 简化写作）（一层，职责清晰）

计划：
1. 删除 DeepAgent 层，反思内置到 Planning
2. 删除 MultiAgent（已完成 ✅）
3. 统一事件系统
```

### 实际执行中的调整（2025-12-11）

**发现的问题**：
- `langgraph_agent.py` 已有 **4764 行**
- `deep_agent/` 目录有 **1166 行**
- 如果内联，文件将接近 6000 行，不利于维护

**另一个重要发现**：
- `PlanningAgent` 类（`agents/planning_agent.py`）从未被实际使用
- 它有 bug：`get_planning_agent()` 返回 `PlanningAgent()` 缺少必需的 `task_executors` 参数
- 真正在用的是 `langgraph_agent.py` 中的 `planning_agent` 节点（LangGraph 工作流节点）

---

## 三、最终实施方案

### 选择：简化版方向 B

```
最终架构：
langgraph_agent.py (4764行)  ←→  deep_agent/ (1166行)
      主流程                        反思模块
```

### 已完成的操作

#### 1. 删除 `PlanningAgent` 类（从未被使用的死代码）

**删除的文件**：
- `backend/app/services/agent/agents/planning_agent.py`

**修改的文件**：
- `backend/app/services/agent/agents/__init__.py` - 移除 PlanningAgent 导出
- `backend/app/api/v1/agent.py` - 移除：
  - `from app.services.agent.agents import PlanningAgent`
  - `get_planning_agent()` 依赖函数
  - `PlanCreationRequest`、`PlanResponse` 模型类
  - `POST /plans`、`GET /plans/{plan_id}` 两个 API 端点

#### 2. 保留 `deep_agent/` 目录

**原因**：避免让 langgraph_agent.py 变成 6000 行的巨型文件

**保留的文件**：
```
backend/app/services/agent/deep_agent/
├── __init__.py      (29行)
├── config.py        (52行)
├── executor.py      (462行)  # DeepAgentExecutor
├── reflection.py    (262行)  # 反思逻辑
└── task_enricher.py (361行)  # 任务增强
```

#### 3. 保留的相关配置（名字相同但用途不同）

| 名称 | 类型 | 状态 | 说明 |
|------|------|------|------|
| `PlanningAgent` 类 | Python 类 | ❌ 已删除 | 从未被使用 |
| `planning_agent` 节点 | LangGraph 工作流节点 | ✅ 保留 | 正在使用 |
| `planning_agent.yaml` | Prompt 模板 | ✅ 保留 | 给节点用 |
| `deep_agent/` | 反思模块 | ✅ 保留 | 正在使用 |

---

## 四、验证结果

### 测试时间：2025-12-11

### 测试内容
使用小说《一夕千悟，从杂役弟子开始》的设定，测试 Planning 模式的完整流程。

### 测试结果

```
✅ Planning 模式正常启动
✅ planning_agent 模板加载成功 (版本 2.0.0)
✅ 规划生成成功，共 2 个任务
✅ DeepAgent 反思模式启用
✅ 任务执行完成
✅ 反思触发正常 (反思=2次, 重规划=0次)
✅ 响应生成成功
```

### 执行流程（实际日志）

```
Planning (20s)
    ↓
Task 1: 获取上下文 (0.1s) → 反思检查点 ✓
    ↓
Task 2: 设计情节 (103s) → 兜底反思 ✓
    ↓
生成响应 (16s)
    ↓
完成 (总耗时 ~154s)
```

---

## 五、对比总结

| 维度 | 重构前 | 重构后 |
|------|--------|--------|
| 架构层数 | 3 层（Planning → DeepAgent → MultiAgent） | 2 层（langgraph + deep_agent） |
| 死代码 | PlanningAgent 类存在但未使用 | 已清理 |
| 反思功能 | ✅ 正常 | ✅ 正常 |
| 代码分离 | 混乱 | 清晰（主流程 vs 反思模块） |
| 可维护性 | 低 | 提高 |

---

## 六、Deep Review：Planning + DeepAgent 协调性问题

### 讨论日期：2025-12-11

### 用户意愿

> 给 planning 模式加上 deep_agent 的目的是：**当任务无法执行完成或不达预期时，能够实时调整任务，继续执行，最终生成符合用户需求的内容。**

### 🔴 核心问题：User Intent 断链

#### 问题描述

反思和重规划时，**不知道用户最初想要什么**，导致无法准确判断"是否达到预期"。

#### 数据流断链图示

```
┌─────────────────────────────────────────────────────────────┐
│  Planning 阶段                                               │
│  ✅ user_intent = "续写第五章，保持悬疑风格"                   │
│  ✅ tasks = [{读取第四章}, {续写第五章}]                       │
└─────────────────────────────────────────────────────────────┘
                          ↓
┌─────────────────────────────────────────────────────────────┐
│  Execution 阶段 (DeepAgentExecutor)                         │
│  ❌ user_intent 没有被提取和传递！                            │
│  只传了：tasks, context(无 user_intent)                      │
└─────────────────────────────────────────────────────────────┘
                          ↓
┌─────────────────────────────────────────────────────────────┐
│  Reflection 阶段 (think_tool)                               │
│  ❌ 反思 prompt 中没有 user_intent                           │
│  AI 只能问：「结果是否达到预期？」                             │
│  但 AI 不知道「预期是什么」！                                 │
└─────────────────────────────────────────────────────────────┘
                          ↓
┌─────────────────────────────────────────────────────────────┐
│  Replan 阶段 (_do_replan)                                   │
│  ❌ 重规划 prompt 中也没有 user_intent                        │
│  AI 只能根据反思内容猜测要调整什么                             │
└─────────────────────────────────────────────────────────────┘
```

#### 具体代码问题

**问题1：executor.py - user_intent 被忽视**

```python
# executor.py 第 48-61 行
async def execute_with_reflection(
    self,
    plan: Dict[str, Any],      # ✅ plan 里有 user_intent
    context: Dict[str, Any],
    execute_task_func: Callable,
) -> Dict[str, Any]:

    tasks = list(plan.get("tasks", []))
    # ❌ plan.get("user_intent") 从未被使用！
```

**问题2：reflection.py - 反思时不知道"预期是什么"**

```python
# reflection.py 第 111-138 行
def _build_reflection_prompt(task, result, remaining_tasks):
    return f"""
    ## 请思考
    1. 结果是否达到预期？  ← 预期是什么？没说！
    2. 是否发现需要补充的信息？
    3. 剩余任务是否仍然合理？
    """
```

**问题3：executor.py - 重规划时无法追溯初衷**

```python
# executor.py 第 280-299 行
prompt = f"""基于反思结果，请调整后续任务计划。

## 反思内容
{reflection}

## 已完成任务
{completed_str}  # 只有最近 3 个

## 原剩余任务
{remaining_str}

# ❌ 没有 user_intent！AI 不知道用户最初想要什么
"""
```

#### 问题影响示例

**用户说**：「为这个故事设计5个关键转折点」

```
Planning:
  user_intent = "设计5个关键转折点"
  tasks = [
    {task_id: 1, description: "读取故事大纲"},
    {task_id: 2, description: "分析故事结构"},
    {task_id: 3, description: "设计转折点", checkpoint: true}
  ]

Execution:
  task_1 完成 → 读到了大纲
  task_2 完成 → 分析了结构
  task_3 完成 → 生成了 3 个转折点（不是5个！）

Reflection (当前实现):
  AI 看到：task_3 有输出，有内容
  AI 不知道：用户要的是「5个」
  AI 判断：「有输出，看起来没问题」→ needs_replan = false

结果：返回 3 个转折点，不符合用户需求 ❌
```

### 🟢 修复方向

#### 核心修复：让 user_intent 贯穿全流程

**修复1：executor.py - 提取并传递 user_intent**

```python
async def execute_with_reflection(self, plan, context, execute_task_func):
    tasks = list(plan.get("tasks", []))
    user_intent = plan.get("user_intent", "")  # ← 提取 user_intent

    # ... 执行循环中
    if should_reflect(...):
        reflection_result = await think_tool(
            task=task,
            result=result,
            remaining_tasks=remaining,
            user_intent=user_intent,  # ← 传递给反思
            ...
        )

        if reflection_result.needs_replan:
            new_tasks = await self._do_replan(
                reflection=...,
                user_intent=user_intent,  # ← 传递给重规划
                ...
            )
```

**修复2：reflection.py - 反思 prompt 注入 user_intent**

```python
def _build_reflection_prompt(task, result, remaining_tasks, user_intent):
    return f"""
    ## 用户的原始意图
    {user_intent}  # ← 新增：作为判断基准

    ## 刚完成的任务
    ...

    ## 请思考
    1. 结果是否符合用户的原始意图？  # ← 改进：明确对比标准
    2. 是否还需要补充什么才能满足用户需求？
    """
```

**修复3：executor.py - 重规划 prompt 注入 user_intent**

```python
prompt = f"""基于反思结果，请调整后续任务计划。

## 用户的原始意图
{user_intent}  # ← 新增

## 反思内容
{reflection}

## 已完成任务
{completed_str}

## 原剩余任务
{remaining_str}
"""
```

### 📊 问题优先级

| 优先级 | 问题 | 文件位置 | 影响 |
|-------|------|---------|------|
| **P0** | user_intent 未传递到反思阶段 | `executor.py:48-61` | 无法判断"是否达到预期" |
| **P0** | user_intent 未传递到重规划阶段 | `executor.py:245-299` | 重规划可能偏离原始需求 |
| **P1** | 反思 prompt 判断标准模糊 | `reflection.py:111-138` | 只检查"缺数据"，不检查"是否满足需求" |
| **P2** | 已完成任务只保留 3 个 | `executor.py:270-273` | 长流程丢失上下文 |

### 附：Checkpoint 规则讨论

#### 当前 Checkpoint 触发机制

```
触发优先级：
1. AI 主动标记  →  task.checkpoint == true
2. 首任务补偿   →  completed_count == 0
3. 间隔补偿     →  每 3 个任务触发一次
4. 失败补偿     →  result.status == "failed"

全局限制: MAX_REFLECTIONS=3, MAX_REPLANS=2
```

#### 是否需要更强制的 Checkpoint 规则？

**当前问题**：
- AI 标记 checkpoint 依赖 prompt 质量，不可靠
- 间隔补偿过于机械（固定每 3 个任务）
- 没有基于工具类型的强制规则

**可选方案**：

| 方案 | 描述 | 优点 | 缺点 |
|------|------|------|------|
| A | 基于工具类型强制 checkpoint（如 write_chapter_tool 后必须反思） | 可靠性高 | 可能过度反思 |
| B | 保持 AI 标记 + 增强补偿机制 | 保持灵活性 | 逻辑更复杂 |
| C | 混合策略：写入操作强制 + AI 标记 + 智能补偿 | 平衡可靠性和灵活性 | 需要更多开发 |

**结论**：先解决 P0 级的 user_intent 断链问题，checkpoint 规则可后续优化。

---

## 七、后续优化方向（可选）

以下是原方案中提到的优化点，可以作为后续迭代参考：

### 1. AI 自我评估机制
让 AI 执行任务时同时输出自我评估，由 AI 自己决定是否需要反思。

### 2. 统一事件系统
- 使用命名空间前缀：`plan:`, `exec:`, `refl:`
- 全局唯一 event_id（UUID）

### 3. 统一上下文 Schema
定义 `TaskContext` dataclass，替代不定形的 dict。

### 4. 护栏机制
- `max_reflections = 3`（单次执行最大反思次数）
- `max_retries_per_task = 2`（单任务最大重试次数）
- `max_total_ai_calls = 20`（总 AI 调用上限）

### 5. 并行执行优化
- 任务通过 `dependencies` 字段声明依赖
- 构建依赖图，拓扑排序分层
- 同层任务使用 `asyncio.gather` 并行执行

---

## 七、结论

本次重构采用**最小改动原则**：

1. **删除死代码** - `PlanningAgent` 类从未被使用，删除它不影响任何功能
2. **保留有效模块** - `deep_agent/` 正在被使用且反思功能正常
3. **不过度重构** - 避免一次性大改，保持系统稳定

重构后系统测试通过，Planning 模式和反思功能均正常工作。

---

*初始讨论：2025-12-10*
*实际执行：2025-12-11*
*验证通过：2025-12-11*
*Deep Review（协调性问题分析）：2025-12-11*

---

## 八、协调性深度 Review（2025-12-11 续）

### 用户意愿回顾

> 当任务无法执行完成或无法达到预期时，能够实时调整任务，继续执行，最终生成符合用户需求的内容。

### 当前实现状态

| 机制 | 状态 | 位置 |
|------|------|------|
| user_intent 贯穿 | ✅ 已实现 | executor.py:78,159,170 |
| 反思触发（checkpoint） | ✅ 已实现 | reflection.py:201-313 |
| 重规划（替换剩余任务） | ✅ 已实现 | executor.py:582-698 |
| 末尾校验与补救 | ✅ 已实现 | executor.py:392-510 |

### 待优化问题

#### 🟡 P1：重规划只能替换"剩余任务"

**现状**：
```python
# executor.py:176
tasks = tasks[:i + 1] + new_tasks  # 只替换 tasks[i+1:]
```

**问题场景**：
- 用户要求"5个转折点"，任务3只生成了2个
- 重规划只能在任务4之后补充，无法直接补充任务3的输出

**建议**：允许插入"补充任务"
```python
if reflection_result.issue_type == "insufficient_output":
    supplement_task = {
        "description": f"补充上一任务：{reflection_result.reflection}",
        "tool": current_task.get("tool"),
        "is_supplement": True,
    }
    tasks.insert(i + 1, supplement_task)
```

#### 🟡 P2：反思判断精度不足

**现状**：反思 prompt 只说"判断是否符合预期"，没有传入验收标准

**建议**：增强反思 prompt
```python
prompt = f"""
## 验收标准
- 期望数量: {task.get("acceptance", {}).get("expected_count", "未知")}
- 要求: {task.get("acceptance", {}).get("requirement", "未知")}

## 请对照验收标准判断...
"""
```

#### 🟡 P2：反思触发时机不够智能

**现状**：依赖 AI 标记 checkpoint + 间隔补偿

**建议**：增加写入型操作的强制反思
```python
WRITE_TOOLS = {"write_chapter_tool", "generate_content_tool"}

if task.get("tool") in WRITE_TOOLS:
    return True  # 写入操作后必须反思
```

### 改进优先级

| 优先级 | 问题 | 工作量 |
|-------|------|--------|
| P1 | 实时补充机制（插入补充任务） | 中 |
| P2 | 增强反思判断精度 | 低 |
| P2 | 优化反思触发时机 | 低 |

### 待确认事项

1. **补充任务的定位**：是作为独立任务还是与原任务合并？
2. **issue_type 分类**：如何让 AI 准确判断是"输出不足"还是"方向错误"？
3. **前端展示**：补充任务需要特殊标记吗？
