# 07 - Review 报告

> 深度分析 ReAct 模式问题，确定采用方案 A：基于 Planning 模式扩展

## 一、ReAct 模式问题汇总

### 1.1 严重问题（共 4 个）

#### 🔴 问题 1：前后端状态严重不一致

| 层面 | 状态 | 位置 |
|------|------|------|
| 后端 ChatMode 枚举 | ✅ 存在 `REACT` | `chat_models.py:15-26` |
| 后端 API 路由 | ✅ 支持 `mode=react` | `agent.py:1132-1183` |
| 前端 ModeSelector | ❌ **已移除 ReAct** | 注释明确写"ReAct 模式已移除" |
| 前端 AIPanel | ⚠️ 仍有 ReAct 代码 | `AIPanel.tsx:484-498` |
| 前端 useAgentChat | ⚠️ 仍有 ReAct 回调 | `useAgentChat.ts:328-416` |

**问题本质**：前端说移除了，但代码没删干净；后端完全支持，但前端不展示

#### 🔴 问题 2：双重 API 路由

```
/agent/chat/stream?mode=react     → agent.py 统一端点
/agent/chat/react-stream          → agent_react_stream.py 独立端点
```

**问题**：
- 功能重复，维护成本高
- 功能开关检查不一致
- 客户端不知道该用哪个

#### 🔴 问题 3：chat_stream 与 chat_with_planning 差异巨大

| 特性 | chat_stream (ReAct) | chat_with_planning (Planning) |
|------|---------------------|-------------------------------|
| 执行流程 | 单次 LangGraph 执行 | 两阶段：规划 + 执行 |
| 事件格式 | progress/tool_call/content | plan/task_start/task_done/content |
| 工具调用 | LangGraph 自动管理 | MultiAgentExecutor 协调 |
| 任务管理 | ❌ 无 | ✅ 完整 |
| 前端支持 | ⚠️ 不完整 | ✅ 完整 |

#### 🔴 问题 4：ReAct 缺少 DeepAgent 核心特性

| 特性 | Planning 模式 | ReAct 模式 |
|------|---------------|------------|
| 任务规划 | ✅ on_plan 事件 | ❌ 无 |
| 任务进度 | ✅ task_start/done | ❌ 只有 progress |
| 前端任务列表 | ✅ TaskListPanel | ❌ 不支持 |

### 1.2 中等问题（共 5 个）

| # | 问题 | 位置 |
|---|------|------|
| 5 | HITL 回调使用私有属性 `_approval_callback` | agent.py:1170 |
| 6 | mode 参数优先级混乱（URL vs Body） | agent.py:1000-1009 |
| 7 | 全局 Agent 实例无法追踪成本 | agent.py:89-99 |
| 8 | progressData 验证失败仍使用数据 | useAgentChatStream.ts:246-256 |
| 9 | SessionTabs 未显示 mode 信息 | SessionTabs.tsx |

## 二、方案对比

### 2.1 方案 A：基于 Planning 模式扩展 ✅ 推荐

```
优点：
✅ Planning 已有完整任务管理（on_plan/task_start/task_done）
✅ MultiAgentExecutor 可复用
✅ 事件格式已被前端完整支持
✅ 改动量最小（~150 行）
✅ 风险可控

缺点：
- 需要添加 think_tool 和反思机制
- 执行流程稍重

实现路径：
1. 在 chat_with_planning 中添加反思检查点
2. 实现 think_tool 工具
3. 添加重规划逻辑
4. 前端无需改动
```

### 2.2 方案 B：重构 ReAct 模式 ❌ 不推荐

```
优点：
- ReAct 模式更轻量
- 边思考边执行更灵活

缺点：
❌ 需要先修复前后端不一致（2-3 天）
❌ 需要添加任务管理能力（3-5 天）
❌ 需要重新设计事件格式（1-2 天）
❌ 总工作量 8-13 天

实现路径：
1. 先修复前端 ReAct 支持
2. 统一 API 路由
3. 在 chat_stream 中添加 write_todos
4. 添加 think_tool
5. 实现任务事件发送
```

### 2.3 方案 C：新建 DeepAgent 模式 ❌ 不推荐

```
优点：
- 不影响现有功能
- 可以从零设计

缺点：
❌ 代码重复
❌ 维护成本高
❌ 需要新的前端支持
```

## 三、最终决策

**采用方案 A：基于 Planning 模式扩展**

| 决策项 | 选择 |
|--------|------|
| 基础模式 | Planning 模式 |
| 扩展方式 | 在 Execution 阶段添加反思循环 |
| 核心工具 | think_tool |
| 前端改动 | MVP 零改动（复用 task_progress） |
| 事件协议 | 复用现有 task_progress 事件 |

## 四、实现清单

### 4.1 后端改动

| 文件 | 改动 | 行数 |
|------|------|------|
| `langgraph_agent.py` | 导入 + 参数 + 分支 | +6-8 行 |
| `agent.py` | 传递 enable_reflection 参数 | +3-5 行 |
| `chat_models.py` | 请求模型添加字段 | +1-2 行 |
| `deep_agent/config.py` | 配置常量 | ~20 行 |
| `deep_agent/reflection.py` | think_tool | ~80 行 |
| `deep_agent/executor.py` | DeepAgentExecutor | ~150 行 |
| **总计后端** | | **~280 行** |

### 4.2 前端改动（分层级）

| 层级 | 改动 | 行数 |
|------|------|------|
| MVP（Level 1） | 零改动，复用 task_progress | **0 行** |
| 增强版（Level 2） | is_update 处理 | +15 行 |
| 完整版（Level 3） | 反思气泡 + 新增标记 | ~100 行 |

### 4.3 无需改动

- SSE 事件协议格式
- MultiAgentExecutor（任务执行）
- TaskListPanel（MVP 复用 progress_status）
- useAgentChat 的 onTaskProgress 回调（已有）

### 4.4 需要改动（如果使用完整版）

- useAgentChat（onPlan 的 is_update 处理）
- TaskListPanel（反思气泡组件）
- agentApi（reflection 事件解析）

## 五、风险控制

### 5.1 反思次数限制

```python
MAX_REFLECTIONS = 3  # 单次请求最多反思 3 次
MAX_REPLANS = 2      # 单次请求最多重规划 2 次
```

### 5.2 超时保护

```python
REFLECTION_TIMEOUT = 30   # 反思超时 30 秒
REPLAN_TIMEOUT = 45       # 重规划超时 45 秒
TOTAL_TIMEOUT = 360       # 总超时保持 6 分钟
```

### 5.3 回退机制

- 反思失败 → 跳过反思，继续执行
- 重规划失败 → 保持原计划
- enable_reflection=False → 完全跳过反思（降级到标准 Planning）

## 六、验证清单

### 6.1 是否解决原问题？

| 目标 | 方案是否满足 |
|------|-------------|
| 动态规划（边做边想） | ✅ 反思 + 重规划 |
| 反思能力 | ✅ think_tool |
| 低侵入性 | ✅ 独立 deep_agent/ 模块 |
| 前端任务列表复用 | ✅ MVP 零改动 |

### 6.2 是否引入新问题？

| 检查项 | 结果 |
|--------|------|
| 是否破坏现有 Planning 模式？ | ❌ 不会（enable_reflection=False 时完全兼容） |
| 是否需要数据库迁移？ | ❌ 不需要 |
| 是否影响现有 API 兼容性？ | ❌ 不影响（新增可选参数） |
| 是否引入新的依赖？ | ❌ 不需要 |

## 七、实施计划

### Phase 1: MVP（预计 2 天）

- [ ] 实现 deep_agent/ 模块
- [ ] 实现 think_tool 工具
- [ ] 复用 task_progress 发送反思
- [ ] 前端零改动
- [ ] 单元测试

### Phase 2: 增强版（预计 1 天）

- [ ] 实现 plan 更新事件（is_update）
- [ ] 前端适配 is_update
- [ ] 测试重规划场景

### Phase 3: 完整版（可选，预计 2 天）

- [ ] 实现反思气泡组件
- [ ] 新增 reflection 事件
- [ ] 样式优化

### Phase 4: 子代理支持（可选，预计 3-5 天）

- [ ] 实现 task 工具
- [ ] 子代理上下文隔离
- [ ] 子代理结果整合

## 八、关键代码位置索引

### 后端

| 文件 | 关键内容 | 行号 |
|------|----------|------|
| `chat_models.py` | ChatMode 枚举 | 15-26 |
| `agent.py` | 统一流式端点 | 966-1355 |
| `agent.py` | on_task_progress 回调 | 1104-1106 |
| `langgraph_agent.py` | chat_with_planning | 3785-4175 |
| `multi_agent/executor.py` | MultiAgentExecutor | 1-494 |

### 前端

| 文件 | 关键内容 | 行号 |
|------|----------|------|
| `ModeSelector.tsx` | 模式选择器 | - |
| `TaskListPanel.tsx` | 任务列表、progress_status | 80-85 |
| `useAgentChat.ts` | onTaskProgress 处理 | 327-338 |
| `agentApi.ts` | task_progress 事件解析 | 254 |

---

*Review 完成时间：2025-12-07*
*决策：采用方案 A - 基于 Planning 模式扩展*
*MVP 改动量：~280 行（后端）+ 0 行（前端）*
*预计工作量：2-3 天（MVP）*
