# Explore 功能概述

## 1. 定位

Explore 是 `get_writing_context` 的**增强版**，专门用于复杂任务的多轮信息收集。

```
get_writing_context  →  一次性聚合，适合简单任务
explore_content      →  多轮探索，适合复杂任务
```

**本质**：一个 mini-agent 聚合工具，对外是单个工具调用，内部是自主循环。

## 2. 与 get_writing_context 的关系

| 特性 | get_writing_context | explore_content |
|------|---------------------|-----------------|
| 调用方式 | 一次性 | 多轮循环 |
| 信息充足判断 | 无 | AI 自主判断 |
| 精确验证 | 无 | 支持 read_paragraph 验证 |
| 适用场景 | 简单任务 | 复杂任务 |

**选择规则**（由 AI 自主决定）：
- 续写当前章节、简单改写 → `get_writing_context`
- 涉及多章节、需要深入理解人物关系 → `explore_content`

## 3. 核心价值

| 价值 | 说明 |
|------|------|
| 多轮探索 | 直到 AI 判断信息充足 |
| 精确验证 | 搜索 → 定位 → read_paragraph 验证原文 |
| 封装复杂度 | 主 Agent 只需调用一次 |
| 复用现有工具 | 调用 search_content、get_writing_context、locate_content |

## 4. 架构图

```
┌─────────────────────────────────────────────────────────┐
│  主 Agent (Planning → Execution)                        │
│                                                         │
│  AI 根据任务复杂度选择：                                │
│    - 简单任务 → get_writing_context                     │
│    - 复杂任务 → explore_content                         │
└─────────────────────────────────────────────────────────┘
                         │
           ┌─────────────┴─────────────┐
           │                           │
           ▼                           ▼
┌─────────────────────┐    ┌─────────────────────────────┐
│ get_writing_context │    │ explore_content             │
│                     │    │ (mini-agent)                │
│ 一次性返回:         │    │                             │
│ - chapters          │    │ 内部循环调用现有工具:       │
│ - worldview         │    │ - search_content            │
│ - rag_context       │    │ - get_writing_context       │
└─────────────────────┘    │ - locate_content            │
                           │ - read_paragraph (新增)     │
                           │                             │
                           │ 直到 AI 判断信息充足        │
                           └─────────────────────────────┘
```

## 5. 触发时机

**由 AI 在 Planning 阶段自主决定**，不是强制第一步。

Planning Prompt 中的描述：
```
explore_content - 深度探索工具（get_writing_context 的增强版）

适用场景：
- 任务涉及多个章节的关联分析
- 需要深入理解人物关系、情节发展
- 搜索结果需要原文验证

不适用场景：
- 简单的续写当前章节（用 get_writing_context）
- 已经知道具体位置的改写（用 locate_content + smart_rewrite）
```

## 6. 设计原则

1. **复用现有工具**：不重复实现 search、chapter、worldview 的获取
2. **精度零丢失**：内容原样传递，不压缩
3. **AI 自主决策**：每轮由 AI 决定调用哪些工具
4. **去重工具调用**：避免重复搜索相同 query
5. **融入现有架构**：事件格式与 FlowEventBuilder 兼容
