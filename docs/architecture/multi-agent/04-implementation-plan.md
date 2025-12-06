# 实现方案选择

> 文档版本: 1.0
> 创建日期: 2025-12-06
> 状态: 决策文档

---

## 概述

本文档分析 Multi-Agent 的三种实现方案，并给出最终推荐。

---

## 核心问题

**Multi-Agent 应该如何与现有 Planning 模式集成？**

### 三种方案

| 方案 | 描述 |
|------|------|
| 方案A | 单独实现 Multi-Agent，与 Planning 并行 |
| 方案B | 在 Planning 基础上扩展 |
| 方案C | 混合架构（推荐） |

---

## 方案A: 单独实现 Multi-Agent

### 架构图

```
用户 → [选择模式] → Planning模式（现有）
                   → Multi-Agent模式（新建）
```

### 代码结构

```
multi_agent/
├── __init__.py
├── multi_agent_writer.py      # 入口类
├── agents/
│   ├── outline_agent.py       # 大纲师
│   ├── writer_agent.py        # 主笔
│   ├── character_guard.py     # 角色守护
│   ├── logic_auditor.py       # 逻辑审计
│   └── editor_agent.py        # 总编
└── prompts/
    └── ...                    # 5个Agent的Prompt
```

### 优点

- ✅ 架构清晰，完全按设计文档实现
- ✅ 不影响现有 Planning 功能
- ✅ 独立迭代，风险隔离

### 缺点

- ❌ 大量代码重复（状态管理、checkpoint、工具调用）
- ❌ 维护两套系统
- ❌ 用户困惑：什么时候用哪个？
- ❌ **工作量：约2周**

---

## 方案B: 在 Planning 基础上扩展

### 架构图

```
Planning模式（扩展）
├── 阶段1: 规划（现有）           → 复用为"大纲师"
├── 阶段2: 执行（现有）           → 复用为"主笔"
├── 阶段2.5: 校验（新增）         → 角色守护 + 逻辑审计
├── 阶段2.6: 裁决（新增）         → 总编
└── 阶段3: 响应（现有）
```

### 优点

- ✅ 复用现有代码（规划、执行、checkpoint）
- ✅ 统一用户体验
- ✅ 渐进式升级，风险低
- ✅ **工作量：约1周**

### 缺点

- ❌ Planning模式变复杂
- ❌ 架构耦合度高
- ❌ **粒度不匹配**（见下文分析）

### 粒度不匹配问题

**Multi-Agent 文档的流程是章节级串行**：

```
每写一章：大纲师 → 主笔 → 角色守护 → 逻辑审计 → 总编
```

**现有 Planning 是任务级并行**：

```
用户请求 → 分解为任务1,2,3 → 并行执行 → 汇总
```

直接在 Planning 上加校验会导致：

```
规划 → 并行执行任务1,2,3 → [对谁校验？] → 响应
                           ↑ 问题在这里
```

---

## 方案C: 混合架构（推荐）

### 核心思想

- **Planning 作为任务调度层**（不大改）
- **Multi-Agent 作为内容生产的子流程**（嵌入执行层）
- **智能判断**：写作任务走 Multi-Agent，其他任务简单执行

### 架构图

```
用户请求
    ↓
Planning（任务调度层）
    ↓
识别任务类型
    ↓
┌──────────────────┬─────────────────┐
│  [写作类任务?]   │  [非写作类任务]  │
│        ↓         │        ↓        │
│  Multi-Agent流程 │    简单执行     │
│ (大纲→写→校验)   │  (直接调用工具)  │
└────────┬─────────┴────────┬────────┘
         └──────────────────┘
                  ↓
             汇总响应
```

### 代码实现

#### 1. 任务执行层判断

> **注意**：实际集成点在 `_execute_tasks_in_parallel` 方法内的 `execute_with_semaphore` 闭包中，详见 [10-integration-details.md](./10-integration-details.md)

```python
# langgraph_agent.py - _execute_tasks_in_parallel 内部
async def execute_with_semaphore(task):
    """执行单个任务（在 semaphore 控制下）"""

    # 初始化 Multi-Agent 执行器
    from app.services.agent.multi_agent import MultiAgentExecutor
    multi_agent = MultiAgentExecutor(self.ai_service)

    # 判断是否是写作类任务
    if multi_agent.is_writing_task(task):
        # 使用Multi-Agent流程
        result = await multi_agent.execute(task, work_id, chapter_id, context)
        return {"task_id": task["task_id"], "result": result["content"]}
    else:
        # 简单执行（原有逻辑）
        return await self._simple_execute(task, work_id, chapter_id, context)
```

#### 2. Multi-Agent 作为内部模块

```python
# multi_agent/executor.py
class MultiAgentExecutor:
    """写作任务的Multi-Agent执行器"""

    async def execute(self, task, work_id, chapter_id, context):
        # 步骤1: 大纲（如果task已有大纲则跳过）
        outline = await self._generate_outline(task, context)

        # 步骤2: 主笔写作
        draft = await self._write_draft(outline, context)

        # 步骤3: 角色守护校验
        character_review = await self._check_character(draft, work_id)

        # 步骤4: 逻辑审计校验
        logic_review = await self._check_logic(draft, work_id)

        # 步骤5: 总编裁决
        if character_review["status"] == "NEED_REVISION" or \
           logic_review["status"] == "NEED_REVISION":
            final = await self._editor_revise(draft, character_review, logic_review)
        else:
            final = draft

        return final
```

### 优点

- ✅ 复用现有代码（规划、执行、checkpoint）
- ✅ 粒度正确：Multi-Agent 处理单个写作任务
- ✅ 简单任务不过度处理
- ✅ 架构清晰，职责分离
- ✅ **工作量：约1周**

### 缺点

- ⚠️ 需要准确判断"写作类任务"

---

## 方案对比总结

| 维度 | 方案A（独立实现） | 方案B（扩展Planning） | 方案C（混合架构） |
|------|-----------------|---------------------|-----------------|
| 代码复用 | ❌ 低 | ✅ 高 | ✅ 高 |
| 架构清晰度 | ✅ 高 | ⚠️ 中 | ✅ 高 |
| 粒度匹配 | ✅ 正确 | ❌ 不匹配 | ✅ 正确 |
| 简单任务处理 | ✅ 不影响 | ⚠️ 过度处理 | ✅ 智能判断 |
| 工作量 | 2周 | 1周 | 1周 |
| 维护成本 | ❌ 高 | ⚠️ 中 | ✅ 低 |
| **推荐度** | ⭐⭐⭐ | ⭐⭐ | ⭐⭐⭐⭐⭐ |

---

## 最终决策

### 推荐：方案C（混合架构）

### 理由

1. **粒度正确**：Multi-Agent 处理单个写作任务，不影响 Planning 的任务调度
2. **代码复用**：复用现有的规划、执行、checkpoint 等基础设施
3. **智能判断**：非写作任务不会被过度处理
4. **渐进实现**：可以先实现核心功能，再逐步完善

### 实施路径

```
第1步：移除 ReAct 模式（清理代码）           [1天]
第2步：创建 multi_agent/ 目录结构            [0.5天]
第3步：实现 MultiAgentExecutor 核心类        [2天]
第4步：实现 5 个 Agent 的 Prompt 模板        [1天]
第5步：在 task_executor 中集成              [1天]
第6步：测试与调优                           [2天]
─────────────────────────────────────────
总计：约 7-8 天
```

---

## 相关文档

- [03-multi-agent-design.md](./03-multi-agent-design.md) - Multi-Agent架构设计
- [05-code-structure.md](./05-code-structure.md) - 代码结构设计
- [07-implementation-steps.md](./07-implementation-steps.md) - 详细实施步骤
