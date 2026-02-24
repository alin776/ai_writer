---
name: subagent-strategy
description: "子 Agent 委派策略。定义何时必须使用 task 工具将阅读和分析任务委派给子 Agent，避免主线程 context window 被大量章节内容撑爆。本策略始终生效。"
license: MIT
metadata:
  author: ai-writer
  version: "1.0"
  type: system
  mode: always-active
  domain: meta
allowed-tools: task
---

# 子 Agent 使用策略（必须遵守）

子 Agent 用于隔离上下文密集的只读操作，避免主线程被大量文件内容撑爆。

## 硬性规则
- 需要阅读超过 3 个章节文件时，**禁止**在主线程逐个调用 read_file，**必须**使用 task 工具委派子 Agent 批量阅读
- 需要在超过 5 个文件中搜索/追踪某个元素时，**必须**使用 task 工具委派
- 多维度分析任务（如同时分析爽点 + 升级 + 角色），**应该**为每个维度启动独立的 task

## 委派方式
- 按每 5-10 章分组，每组启动一个子 Agent
- 多组可并行启动
- 子 Agent 仅做只读操作（read_file / glob / grep / semantic_search），不得修改文件
- 所有写作和编辑操作必须在主线程完成

<example>
user: "分析前20章的爽点分布"
assistant: 这需要通读20章内容，我会分两组委派子Agent分析。
assistant: *使用 task 工具并行启动两个子 Agent*
  - 子 Agent 1: "阅读第 1-10 章，分析每章的爽点类型、位置和密度，以表格形式返回"
  - 子 Agent 2: "阅读第 11-20 章，分析每章的爽点类型、位置和密度，以表格形式返回"
assistant: *收到两个子 Agent 的分析结果，在主线程汇总并输出完整报告*
<commentary>
20 章内容量巨大，在主线程逐个 read_file 会消耗大量 context window，导致后续推理空间不足。
使用 task 工具将阅读和初步分析委派给子 Agent，主线程只接收精简的分析结果，保持高效。
禁止在主线程连续调用 read_file 超过 3 次来读取章节。
</commentary>
</example>

<example>
user: "帮我追踪萧凌的实力变化"
assistant: 需要全书追踪角色信息，我用子 Agent 来检索。
assistant: *使用 task 工具启动子 Agent: "在所有章节中搜索萧凌的修为、境界、技能变化，按章节顺序整理为时间线返回"*
assistant: *收到子 Agent 返回的实力时间线，向用户展示结果*
<commentary>
跨全书的角色追踪是典型的 context-heavy 只读任务，子 Agent 负责检索和整理，主线程负责展示和解读。
</commentary>
</example>

<example>
user: "修改第5章，让战斗更紧凑"
assistant: *直接 read_file 读取第5章，然后 edit_file 修改*
<commentary>
只涉及 1 个章节的阅读和编辑，这是简单任务，直接在主线程完成即可，不需要使用 task 工具。
</commentary>
</example>
