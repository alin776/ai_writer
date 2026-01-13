# 07 - 实现步骤

## ⚠️ 重要更新（2026-01-12）

经验证，现有代码已有 `DeepAgentExecutor` 实现了迭代执行 + 反思循环。

**调整方案**：增强现有代码而非新建 `IterativeExecutor`

详见 [08-validation-report.md](./08-validation-report.md)

---

## 实施前置决策（必须先确认）

### 1) 事件契约与链路选择

**结论**：优先沿用 **planning SSE**（`plan/task_start/task_progress/task_done`），新增事件需保持向后兼容。

- 任务完成事件：以 `task_done` 为主，`task_complete` 仅作为别名（必要时双发）。
- 计划更新事件：优先复用 `plan` + `is_update/new_task_ids`；如新增 `plan_update`，需保证与 `plan` 同语义并兼容前端状态保留逻辑。
- 思考事件：可新增 `thinking`，同时保留 `task_progress` 作为回退渠道。

> 关键点：若新增事件类型，必须同步更新 `backend/app/api/v1/agent.py` → `src/services/agentApi.ts` → `src/hooks/useAgentChat.ts`。

### 2) 任务模型统一

**结论**：统一为数值型 `task_id`（用于参数解析器与排序），状态枚举以 UI 为准。

- `task_id`: **int**（动态任务使用递增整数）
- `status`: `pending/running/completed/failed/skipped`
- 必备字段：`description/tool/params`，需保留 `checkpoint/acceptance/is_remedy`（DeepAgentExecutor 依赖）
- 可选字段：`title/is_dynamic`（仅展示用）

### 3) 文档路线对齐

**结论**：所有文档以“增强 `DeepAgentExecutor`”为唯一实施路线，`IterativeExecutor` 仅保留概念性描述。

---

## 实现顺序（调整后）

```
Phase 0: 契约与模型对齐（事件/任务模型/文档）
    ↓
Phase 1: 后端增强（基于现有 DeepAgentExecutor）
    ↓
Phase 2: 流式事件（新增 thinking/plan_update 事件）
    ↓
Phase 3: 前端适配（适配新事件类型）
    ↓
Phase 4: 集成测试
```

## Phase 0: 契约与模型对齐

- 明确最终事件表（含别名与回退策略）
- 统一任务模型字段与状态枚举
- 修正文档不一致处（IterativeExecutor / thinking 展示）

## Phase 1: 后端增强

### Step 1.1: 创建 DynamicPlan 类

**文件**: `backend/app/services/agent/execution/dynamic_plan.py`

**内容**: 见 [03-dynamic-plan.md](./03-dynamic-plan.md)

**说明**: 封装现有 `DeepAgentExecutor` 中的任务列表操作，提高代码可读性

---

### Step 1.2: 增强 DeepAgentConfig

**文件**: `backend/app/services/agent/deep_agent/config.py`

**新增配置**:
```python
class DeepAgentConfig:
    # 现有配置...

    # 新增：迭代模式配置
    REFLECT_EVERY_TASK: bool = False  # 是否每个任务后都反思
    EMIT_THINKING_EVENT: bool = True  # 是否发送专门的 thinking 事件
```

---

### Step 1.3: 增强反思机制

**文件**: `backend/app/services/agent/deep_agent/reflection.py`

**改动**:
1. 新增 `IterativeReflectionResult` 数据类
2. 新增 `iterative_reflect()` 函数（可选，用于更丰富的反思输出）

**内容**: 见 [04-reflection-enhance.md](./04-reflection-enhance.md)

---

### Step 1.4: 增强 DeepAgentExecutor

**文件**: `backend/app/services/agent/deep_agent/executor.py`

**改动**:
1. 使用 `DynamicPlan` 类替代直接操作任务列表
2. 根据 `REFLECT_EVERY_TASK` 配置决定反思频率（必要时放宽 `MAX_REFLECTIONS`）
3. 思考事件：优先新增 `thinking`，同时保留 `task_progress` 兼容
4. 计划更新：优先复用 `on_plan` 的 `is_update/new_task_ids`

## Phase 2: 流式事件

### Step 2.1: 扩展 StreamEventHandler

**文件**: `backend/app/services/agent/stream/stream_event_handler.py`

**改动**:
1. 新增 `emit_thinking()` 方法
2. 新增 `emit_plan_update()` 方法

**内容**: 见 [05-stream-events.md](./05-stream-events.md)

---

### Step 2.2: 在 DeepAgentExecutor 中调用新事件

**文件**: `backend/app/services/agent/deep_agent/executor.py`

**改动**:
1. 在反思后调用 `emit_thinking()`
2. 在计划更新后调用 `emit_plan_update()` 或 `on_plan(is_update)`

---

## Phase 3: 前端适配

### Step 3.1: 适配新事件类型

**文件**: `src/components/editor/AIPanel.tsx`

**改动**:
1. 监听 `thinking` 事件，更新 AI 思考展示
2. 监听 `plan_update` 事件，更新任务列表

**说明**: 现有 `TaskList` 和 `ExecutionFlow` 组件可复用，仅需适配新事件类型

---

## Phase 4: 集成测试

### 测试场景

| 场景 | 预期行为 |
|------|----------|
| 简单查询 | 1个任务，直接完成 |
| 续写章节 | 多个任务，顺序执行 |
| 缺少信息 | 动态添加任务 |
| 任务失败 | 显示错误，继续或终止 |
| 事件兼容 | 旧事件与新事件均可驱动前端 |
| 任务模型 | 动态任务不破坏参数解析与状态保留 |

---

## 检查清单（调整后）

### Phase 0 完成标准
- [ ] 事件契约与别名方案确定
- [ ] 任务模型字段与状态枚举统一
- [ ] 文档路线对齐（DeepAgentExecutor 为唯一实施路线）

### Phase 1 完成标准
- [ ] DynamicPlan 类创建并测试通过
- [ ] DeepAgentConfig 新增配置项
- [ ] DeepAgentExecutor 使用 DynamicPlan

### Phase 2 完成标准
- [ ] emit_thinking() 方法实现
- [ ] emit_plan_update() 方法实现
- [ ] DeepAgentExecutor 调用新事件方法

### Phase 3 完成标准
- [ ] 前端监听 thinking 事件
- [ ] 前端监听 plan_update 事件
- [ ] AI 思考正确显示（普通文本）

### Phase 4 完成标准
- [ ] 所有测试场景通过
- [ ] 无明显性能问题
- [ ] 用户体验流畅
