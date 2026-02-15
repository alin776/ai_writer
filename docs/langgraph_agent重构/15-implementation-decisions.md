# 实施决策记录 (ADR)

## 文档版本
- 版本：1.0
- 日期：2025-12-23
- 类型：架构决策记录

---

## ADR-001: 不引入 deepagents 库

### 状态
**已决定** - 2025-12-23

### 背景
原重构方案（`07-implementation-plan.md`）规划引入 `deepagents` 库（0.3.0 版本）来实现 interrupt/resume 机制。

### 决策
**不引入 deepagents 库**，直接使用 LangGraph 原生的 `interrupt()` 和 `Command`。

### 理由
1. **依赖来源相同**: `interrupt` 和 `Command` 实际来自 `langgraph.types`，不是 deepagents 独有
2. **减少依赖**: 项目已依赖 langgraph，无需额外引入 deepagents
3. **降低风险**: deepagents 0.3.0 相对较新，稳定性未知

### 代码示例
```python
# 正确做法
from langgraph.types import interrupt, Command

# 不需要
# from deepagents import ...
```

### 影响
- 节省依赖管理成本
- 避免版本兼容问题
- 功能完全不受影响

---

## ADR-002: 增强 PromptManager 而非新建 Skills 系统

### 状态
**已决定** - 2025-12-23

### 背景
原方案（`09-skills-mechanism.md`）规划新建完整的 Skills 文件系统：
- `skills/` 目录
- 每个 skill 包含 `SKILL.md` + 附加资源
- 三级渐进式加载（元数据 → 核心指令 → 附加资源）

### 决策
**修改现有 PromptManager**，添加渐进式加载功能，而非新建系统。

### 理由
1. **避免重复建设**: 项目已有完善的 PromptManager + YAML 模板系统
2. **简化维护**: 一套系统比两套系统更容易维护
3. **工期更短**: 0.5 天 vs 1.5 天
4. **够用原则**: 两级加载（摘要 + 详细模板）对于 5-6 个技能足够

### 对比
| 方案 | 工期 | 新文件 | 复杂度 |
|------|------|--------|--------|
| 新建 Skills | 1.5 天 | 15+ | 高 |
| 增强 PromptManager | 0.5 天 | 0 | 低 |

### 影响
- YAML 模板需添加 `triggers` 和 `summary` 字段
- PromptManager 新增 3 个方法（~50 行代码）
- 三级加载简化为两级

---

## ADR-003: 使用原生 interrupt 而非 Redis 轮询

### 状态
**已决定** - 2025-12-23

### 背景
现有 HITL 实现（`tools/hitl.py`）使用 Redis 轮询：
```python
async def wait_for_approval(self, request_id, check_interval=5):
    while True:
        await asyncio.sleep(check_interval)  # 5秒轮询
```

### 决策
**使用 LangGraph 原生 interrupt** 替换轮询机制。

### 理由
| 对比项 | Redis 轮询 | LangGraph interrupt |
|--------|-----------|---------------------|
| 延迟 | 2-5 秒 | < 100ms |
| 实现复杂度 | 高（需管理状态） | 低（框架内置） |
| 资源消耗 | 持续轮询 | 事件驱动 |

### 代码示例
```python
# 替换前
while True:
    result = await redis.get(key)
    if result:
        break
    await asyncio.sleep(5)

# 替换后
from langgraph.types import interrupt, Command
response = interrupt({"type": "confirmation", "message": "确认执行？"})
```

### 影响
- 用户体验显著提升
- 需要修改 API 端点支持 resume
- 前端需适配新的事件格式

---

## ADR-004: 在 DeepAgentExecutor 添加任务确认中断点

### 状态
**已决定** - 2025-12-23

### 背景
现有 `DeepAgentExecutor.execute_with_reflection()` 只能在任务全部完成后进行反思，无法在执行过程中让用户确认或调整。

### 决策
在任务循环中添加 interrupt 中断点，实现**每个任务执行前可确认**。

### 改造方案
```python
# 改造前
async def execute_with_reflection(self, tasks):
    for task in tasks:
        await self._execute_task(task)
    reflection = await self._reflect_on_results()  # 只能事后反思

# 改造后
async def execute_with_confirmation(self, tasks):
    remaining = tasks.copy()
    while remaining:
        task = remaining[0]

        # 中断点
        response = interrupt({
            "type": "task_confirmation",
            "current_task": task,
            "remaining_tasks": remaining,
            "options": ["执行", "跳过", "修改列表", "停止"]
        })

        if response == "跳过":
            remaining.pop(0)
            continue
        elif response == "修改列表":
            remaining = response.get("new_tasks", remaining)
            continue
        elif response == "停止":
            break

        await self._execute_task(task)
        remaining.pop(0)
```

### 影响
- 用户获得实时控制能力
- 任务执行可中途调整
- 需要前端配合显示任务列表和确认对话框

---

## ADR-005: 简化中断类型

### 状态
**已决定** - 2025-12-23

### 背景
原方案（`06-interrupt-resume.md`）规划了 5 种中断类型：
1. 确认型 (confirmation)
2. 选择型 (select)
3. 版本选择型 (select_version)
4. 输入型 (text_input)
5. 进度控制型 (progress_control)

### 决策
**第一阶段只实现 2 种核心类型**，其余按需后续添加。

### 保留类型
1. **confirmation** - 简单确认（执行/跳过/停止）
2. **task_confirmation** - 任务确认（含任务列表展示）

### 延后类型
- select_version（改写多版本选择） - 复杂度高，暂不需要
- text_input（用户输入） - 可用 confirmation + 后续消息替代
- progress_control（进度控制） - task_confirmation 已覆盖

### 理由
- MVP 原则：先实现最小可用版本
- 降低前端工作量
- 后续按需扩展更灵活

### 影响
- 第一阶段功能聚焦
- 减少测试用例
- 前端只需实现 2 种对话框

---

## ADR-006: 前端使用 SSE 事件处理中断

### 状态
**已决定** - 2025-12-23

### 背景
需要确定前后端如何通信传递中断信息。

### 决策
**复用现有 SSE 流**，添加 interrupt 事件类型。

### 事件格式
```typescript
// 中断事件
{
  type: "interrupt",
  data: {
    interrupt_id: string,
    interrupt_type: "confirmation" | "task_confirmation",
    message: string,
    options: string[],
    tasks?: Task[]  // task_confirmation 专用
  }
}

// 内容事件（原有）
{
  type: "content",
  data: { ... }
}
```

### 恢复请求
```typescript
POST /api/v1/agent/resume
{
  thread_id: string,
  interrupt_id: string,
  response: string | { new_tasks: Task[] }
}
```

### 理由
- 复用现有基础设施
- 保持 API 一致性
- 无需新建 WebSocket 连接

### 影响
- 前端 SSE 处理逻辑需扩展
- 需新增 `/resume` 端点

---

## ADR-007: 工期控制在 4 天

### 状态
**已决定** - 2025-12-23

### 背景
原方案规划 15 天完成完整 Deep Agents 迁移。

### 决策
**简化方案，控制在 4 天内完成**。

### 工期分配
| 日期 | 内容 | 时间 |
|------|------|------|
| Day 1 | PromptManager 增强 + interrupt 基础 | 1 天 |
| Day 2 | 集成到执行流程 | 1 天 |
| Day 3 | 前端适配 | 1 天 |
| Day 4 | 测试和修复 | 1 天 |

### 裁剪内容
- ❌ 分层工具调用
- ❌ 完整 Sub-Agents 架构
- ❌ 上下文自动压缩
- ❌ File System 抽象
- ❌ 复杂中断类型（5 种 → 2 种）
- ❌ 新建 Skills 文件系统

### 理由
- ROI 最大化
- 快速验证核心功能
- 降低失败风险

### 影响
- 部分高级功能延后
- 核心需求（HITL + 任务调整 + 渐进加载）完整实现

---

## 决策总结

| ADR | 决策 | 状态 |
|-----|------|------|
| 001 | 不引入 deepagents 库 | ✅ 已决定 |
| 002 | 增强 PromptManager | ✅ 已决定 |
| 003 | 使用原生 interrupt | ✅ 已决定 |
| 004 | 添加任务确认中断点 | ✅ 已决定 |
| 005 | 简化中断类型（2种） | ✅ 已决定 |
| 006 | SSE 事件处理中断 | ✅ 已决定 |
| 007 | 工期控制 4 天 | ✅ 已决定 |

---

**文档结束**
