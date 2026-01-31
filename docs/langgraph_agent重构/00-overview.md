# LangGraph Agent 重构概述

## 文档版本
- 版本：1.2
- 日期：2025-12-22
- 作者：AI Assistant
- 更新：API 验证确认，更新工具数量为 20 个，添加目录结构

## 目录结构

```
langgraph_agent重构/
├── 00-overview.md              # 本文档 - 重构概述
├── 01-current-analysis.md      # 现状分析 - 问题诊断
├── 02-deep-agents-concepts.md  # Deep Agents 核心概念（含 API 验证结果）
├── 03-migration-strategy.md    # 迁移策略 - 整体规划
├── 04-tools-migration.md       # 工具迁移 - 详细方案（含 StandardToolRegistry）
├── 05-memory-integration.md    # 记忆系统集成
├── 06-interrupt-resume.md      # 中断恢复机制
├── 07-implementation-plan.md   # 实施计划 - 分阶段
├── 08-risk-assessment.md       # 风险评估与回滚方案
├── 09-skills-mechanism.md      # Skills 机制 - 渐进式知识披露 ⭐新增
└── 10-phase3.5-skills-plan.md  # Phase 3.5 - Skills 实施计划 ⭐新增
```

---

## 〇、API 验证状态（2025-12-22）

> ✅ **已验证**：`deepagents==0.3.0` 库已安装测试，核心 API 可用

| API | 状态 | 说明 |
|-----|------|------|
| `create_deep_agent()` | ✅ 可用 | 主入口函数 |
| `AgentMiddleware` | ✅ 可用 | 位于 `langchain.agents.middleware.types` |
| `interrupt_on` 参数 | ✅ 支持 | HITL 配置 |
| `ToolRuntime` | ✅ 存在 | 位于 `langgraph.prebuilt.tool_node` |
| `interrupt` / `Command` | ✅ 可用 | 位于 `langgraph.types` |

---

## 一、重构背景

### 1.1 当前问题

| 问题 | 严重程度 | 描述 |
|------|----------|------|
| 代码臃肿 | 🔴 严重 | `langgraph_agent.py` 单文件 5,703 行，272KB |
| 无法实时调整 | 🔴 严重 | 任务执行后才能反思，无法中途干预 |
| 用户交互差 | 🔴 严重 | 一旦开始执行就必须完成，浪费 tokens |
| 可维护性差 | 🔴 严重 | 64 个函数挤在一个文件，职责混乱 |

### 1.2 重构目标

1. **代码可维护性**：将 5700 行代码拆分为模块化结构
2. **实时计划调整**：支持任务执行中的用户干预
3. **资源节约**：用户可随时中断，避免无效 token 消耗
4. **标准化架构**：采用 Deep Agents 框架，获得社区支持

---

## 二、技术选型

### 2.1 为什么选择 Deep Agents

| 对比项 | 手动重构 | Deep Agents |
|--------|----------|-------------|
| interrupt/resume | 需自己实现 | ✅ 内置支持 |
| 中间件架构 | 需自己设计 | ✅ 标准化 |
| 社区维护 | ❌ 无 | ✅ LangChain 官方 |
| 长期成本 | 高 | 低 |

### 2.2 保留的现有功能

| 功能 | 处理方式 |
|------|----------|
| 20 个专业写作工具 | 适配后注册到 Deep Agents（含 StandardTool 迁移） |
| 三层记忆系统 | 作为自定义 AgentMiddleware 接入 |
| ModelSelector | 覆盖默认模型配置 |
| 成本追踪 | 保持独立，通过钩子调用 |
| 上下文管理 | 集成到 Deep Agents Store |

---

## 三、架构对比

### 3.1 当前架构

```
┌─────────────────────────────────────────┐
│         langgraph_agent.py              │
│            (5,703 行)                    │
│                                         │
│  ┌─────────────────────────────────┐   │
│  │ 意图分类 + 路由 + 工具调用 +    │   │
│  │ 反思 + HITL + 流式处理 + ...   │   │
│  └─────────────────────────────────┘   │
│                                         │
└─────────────────────────────────────────┘
         ↓ 紧耦合
┌─────────────────────────────────────────┐
│  deep_agent/, tools/, memory/, ...      │
└─────────────────────────────────────────┘
```

### 3.2 目标架构

```
┌─────────────────────────────────────────┐
│           Deep Agents Core              │
│        (create_deep_agent)              │
└─────────────────────────────────────────┘
         ↓ 中间件模式
┌─────────────┬─────────────┬─────────────┐
│  TodoList   │ Filesystem  │  SubAgent   │
│ AgentMiddle │ AgentMiddle │ AgentMiddle │
└─────────────┴─────────────┴─────────────┘
         ↓ 自定义扩展
┌─────────────┬─────────────┬─────────────┐
│   Memory    │   Model     │    Cost     │
│ AgentMiddle │  Selector   │  Tracker    │
│  (自定义)    │  (自定义)   │  (自定义)   │
└─────────────┴─────────────┴─────────────┘
         ↓ 工具注册
┌─────────────────────────────────────────┐
│         专业写作工具 (20)               │
│  continue_writing, smart_rewrite, ...   │
│  (含 @tool 和 StandardTool 迁移)        │
└─────────────────────────────────────────┘
```

---

## 四、核心改进

### 4.1 中断/恢复机制

**Before (当前):**
```python
# 轮询等待用户响应
async def wait_for_approval(request_id):
    while True:
        await asyncio.sleep(5)  # 每5秒检查一次
        # ...
```

**After (Deep Agents):**
```python
# 原生中断机制
response = interrupt({
    "type": "confirm_task",
    "task": current_task,
    "options": ["继续", "修改", "跳过"]
})
# 自动暂停，等待用户响应后恢复
```

### 4.2 实时计划调整

**Before (当前):**
```python
# 任务完成后才反思
if should_reflect(task, result):
    reflection = await do_reflection(task, result)
    if reflection.needs_replan:
        # 重新规划所有剩余任务
```

**After (Deep Agents):**
```python
# 任务执行前/中/后都可干预
@task
async def execute_step(step, runtime):
    # 执行前确认
    if step.needs_confirmation:
        response = interrupt({"question": f"即将执行: {step.description}"})

    result = await do_work(step)

    # 执行后可调整
    if not satisfactory(result):
        adjustment = interrupt({"question": "如何处理？"})
```

---

## 五、预期收益

| 维度 | 改进 |
|------|------|
| **代码量** | 5,703 行 → ~1,500 行核心代码 |
| **可维护性** | 单体 → 模块化 AgentMiddleware |
| **用户体验** | 被动等待 → 主动控制 |
| **资源消耗** | 必须完成 → 随时中断 |
| **扩展性** | 改代码 → 加 AgentMiddleware |

---

## 六、文档阅读顺序

1. **了解现状**：阅读 `01-current-analysis.md`
2. **学习框架**：阅读 `02-deep-agents-concepts.md`
3. **理解策略**：阅读 `03-migration-strategy.md`
4. **具体实施**：
   - `04-tools-migration.md` - 工具迁移
   - `05-memory-integration.md` - 记忆集成
   - `06-interrupt-resume.md` - 中断机制
5. **执行计划**：阅读 `07-implementation-plan.md`
6. **风险控制**：阅读 `08-risk-assessment.md`

---

## 七、决策记录

| 日期 | 决策 | 原因 |
|------|------|------|
| 2025-12-19 | 采用 Deep Agents 重构 | 解决 interrupt/resume 问题，降低维护成本 |
| 2025-12-19 | 保留专业写作工具 | 业务核心功能，Deep Agents 通用工具不适用 |
| 2025-12-19 | 保留三层记忆系统 | 远超 Deep Agents 基础能力 |
| 2025-12-19 | 保留 ModelSelector | 多模型选择是成本优化关键 |
| 2025-12-21 | 新增 Skills 机制 | 实现渐进式知识披露，优化 Token 消耗 |
| 2025-12-22 | API 验证通过 | 确认 deepagents 0.3.0 可用，核心 API 存在 |
