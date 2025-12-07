# DeepAgent 模式实现文档

> 基于 Deep Agents 设计理念，在 Planning 模式基础上增强动态反思和重新规划能力

## 重要说明

经过深度 Review，确定采用 **方案 A：基于 Planning 模式扩展**：

| 决策 | 说明 |
|------|------|
| **不基于 ReAct 模式** | ReAct 模式前后端状态不一致，需要大量改造 |
| **基于 Planning 模式** | 已有完整的任务管理、事件系统、前端支持 |
| **模块化设计** | 独立 `deep_agent/` 目录，最小化对现有代码的侵入 |
| **复用现有事件** | 优先复用 `task_progress` 事件，MVP 可实现前端零改动 |

详见 [07-Review报告](./07-REVIEW.md)

## 文档索引

| 序号 | 文档 | 内容 |
|------|------|------|
| 01 | [概述](./01-OVERVIEW.md) | 设计背景、目标、为什么选择扩展 Planning |
| 02 | [架构设计](./02-ARCHITECTURE.md) | 整体架构、模块化设计、扩展点 |
| 03 | [后端实现](./03-BACKEND.md) | deep_agent/ 模块、DeepAgentExecutor、API 层改动 |
| 04 | [工具实现](./04-TOOLS.md) | think_tool 设计、触发条件、错误处理 |
| 05 | [事件协议](./05-EVENTS.md) | 复用 task_progress 事件（推荐）或新增 reflection 事件 |
| 06 | [前端实现](./06-FRONTEND.md) | MVP 零改动方案 / 完整版反思气泡方案 |
| **07** | **[Review报告](./07-REVIEW.md)** | **ReAct 问题分析、方案决策过程** |

## 快速导航

### 我想了解...

- **为什么不基于 ReAct？** → [07-Review报告](./07-REVIEW.md#一react-模式问题汇总)
- **DeepAgent 有什么能力？** → [01-概述](./01-OVERVIEW.md)
- **模块化设计原则** → [02-架构设计](./02-ARCHITECTURE.md#0-模块化设计原则)
- **后端怎么实现？** → [03-后端实现](./03-BACKEND.md)
- **think_tool 怎么设计？** → [04-工具实现](./04-TOOLS.md)
- **事件方案选择** → [05-事件协议](./05-EVENTS.md)
- **前端实现方案** → [06-前端实现](./06-FRONTEND.md)

## 核心设计

### 模块化架构

```
backend/app/services/agent/
├── langgraph_agent.py           # +6-8 行（导入 + 参数 + 分支）
│
└── deep_agent/                  # 新增目录（~260 行）
    ├── __init__.py              # 导出接口
    ├── config.py                # 配置常量 (~20 行)
    ├── reflection.py            # think_tool + 反思逻辑 (~80 行)
    └── executor.py              # DeepAgentExecutor (~150 行)

backend/app/api/v1/
└── agent.py                     # +3-5 行（传递 enable_reflection 参数）

backend/app/models/
└── chat_models.py               # +1-2 行（请求模型添加字段）
```

### 前端改动（分层级）

**Level 1: MVP（零改动）**
- 复用现有 `task_progress` 事件
- 反思内容自动显示在 `progress_status` 中

**Level 2: 完整版（~100 行）**
```
src/
├── components/agent/
│   ├── TaskListPanel.tsx        # +35 行（反思气泡、新增标记）
│   └── TaskListPanel.module.css # +40 行（样式）
├── hooks/
│   └── useAgentChat.ts          # +15 行（is_update 处理）
└── services/
    └── agentApi.ts              # +10 行（reflection 事件解析）
```

## 改动量统计

### MVP 方案（推荐）

| 层面 | 文件 | 改动量 |
|------|------|--------|
| 后端 | langgraph_agent.py | +6-8 行 |
| 后端 | agent.py | +3-5 行 |
| 后端 | chat_models.py | +1-2 行 |
| 后端 | deep_agent/ (新建) | ~260 行 |
| 前端 | - | **0 行** |
| **总计** | | **~280 行** |

### 完整方案

| 层面 | 文件 | 改动量 |
|------|------|--------|
| 后端 | （同上） | ~280 行 |
| 前端 | TaskListPanel | +75 行 |
| 前端 | useAgentChat | +15 行 |
| 前端 | agentApi | +10 行 |
| **总计** | | **~380 行** |

## 实现状态

- [ ] Phase 1: MVP（2天）
  - [ ] deep_agent/ 模块
  - [ ] think_tool + 动态重规划
  - [ ] 复用 task_progress 发送反思
  - [ ] 前端零改动
- [ ] Phase 2: 增强版（1天）
  - [ ] plan 更新事件（is_update）
  - [ ] 前端适配 is_update
  - [ ] 测试重规划场景
- [ ] Phase 3: 完整版（可选，2天）
  - [ ] 前端反思气泡组件
  - [ ] 新增 reflection 事件
  - [ ] 样式优化
- [ ] Phase 4: 子代理支持
  - [ ] task 工具

## 核心设计决策

| 原方案（已放弃） | 现方案（采用） | 原因 |
|-----------------|---------------|------|
| 基于 ReAct 模式 | 基于 Planning 模式 | ReAct 前后端不一致，改造工作量大 |
| 代码写入 langgraph_agent.py | 独立 deep_agent/ 模块 | 原文件已 5000+ 行 |
| 新增 reflection 事件 | **优先复用 task_progress** | 前端零改动，最小风险 |
| 前端必须改动 | MVP 前端零改动 | 渐进式增强，降低风险 |
| 仅改 langgraph_agent.py | 需要同步改 API 层 | 完整的参数传递链路 |

## 参考资料

- [Deep Agents GitHub](https://github.com/langchain-ai/deepagents)
- [Deep Agents Quickstarts](https://github.com/langchain-ai/deepagents-quickstarts)
- [LangChain Blog: Deep Agents](https://blog.langchain.com/deep-agents/)
