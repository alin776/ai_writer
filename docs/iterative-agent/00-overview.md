# 迭代式 Agent 执行模式 - 总览

## 目标

实现类似 Claude Code 的执行模式：**有计划 + 单步执行 + 动态调整**

## ⚠️ 重要发现（2026-01-12 验证）

**现有代码已有 `DeepAgentExecutor`**，实现了迭代执行 + 反思循环！

详见 [08-validation-report.md](./08-validation-report.md)

**建议方案**：增强现有 `DeepAgentExecutor` 而非新建 `IterativeExecutor`

## 核心特性

1. **初始规划**：生成完整任务列表，展示给用户
2. **迭代执行**：每次只执行一个任务
3. **反思决策**：每个任务执行后，AI 总结 + 决定下一步
4. **动态调整**：可以增删改任务
5. **阶段反馈**：每一步都输出给前端展示

## 与当前模式对比

| 特性 | 当前模式（DeepAgentExecutor） | 增强后模式 |
|------|------------------------------|------------|
| 规划方式 | 一次性生成所有任务 | 一次性生成，但可动态调整 |
| 执行方式 | 逐个执行 ✅ | 逐个执行 |
| 中间反馈 | task_progress 事件 | 专门的 thinking 事件 |
| 计划调整 | 仅 checkpoint 可调整 | 每步都可调整（可配置） |
| 反思触发 | 仅 checkpoint 任务 | 每个任务（可配置） |

## 文档结构

| 文档 | 内容 |
|------|------|
| [01-architecture.md](./01-architecture.md) | 架构设计 |
| [02-iterative-executor.md](./02-iterative-executor.md) | 迭代执行器设计 |
| [03-dynamic-plan.md](./03-dynamic-plan.md) | 动态计划管理 |
| [04-reflection-enhance.md](./04-reflection-enhance.md) | 反思机制增强 |
| [05-stream-events.md](./05-stream-events.md) | 流式事件设计 |
| [06-frontend-display.md](./06-frontend-display.md) | 前端展示设计 |
| [07-implementation-steps.md](./07-implementation-steps.md) | 实现步骤 |
| [08-validation-report.md](./08-validation-report.md) | **验证报告（重要）** |

## 改动范围（调整后）

```
backend/app/services/agent/
├── deep_agent/
│   ├── executor.py           # 增强（添加配置项）
│   ├── reflection.py         # 增强（添加 iterative_reflect）
│   └── config.py             # 增强（添加新配置）
├── execution/
│   └── dynamic_plan.py       # 新增（封装任务列表操作）
└── stream/
    └── stream_event_handler.py # 增强（添加 thinking/plan_update 事件）

frontend/src/components/editor/
└── AIPanel.tsx               # 小幅改造（适配新事件）
```

## 预估工作量（调整后）

| 原估算 | 调整后 | 说明 |
|--------|--------|------|
| 后端 280 行 | 约 100 行 | 复用现有 DeepAgentExecutor |
| 前端 100 行 | 约 50 行 | 复用现有 TaskList/ExecutionFlow |
| 测试 2-3 小时 | 1-2 小时 | 现有测试可复用 |
