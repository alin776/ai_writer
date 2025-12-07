# 04 - 工具实现

> DeepAgent 的核心工具：think_tool（反思工具）

## 1. 概述

DeepAgent 模式在 Planning 基础上新增一个核心工具：

| 工具 | 功能 | 类型 | Phase |
|------|------|------|-------|
| `think_tool` | 反思（纯上下文工程） | 无操作 | Phase 1 |
| `task` (可选) | 动态子代理委派 | 子代理 | Phase 3 |

> **注意**：不需要 `write_todos` 工具，因为 Planning 模式已经有完整的任务规划能力。
> DeepAgent 只需在执行过程中增加反思和重规划能力。

## 2. think_tool 工具

### 2.1 设计理念

来自 Deep Agents 的核心洞见：

> think_tool 是一个 **纯上下文工程工具**，不执行任何实际操作，但迫使 Agent 在关键节点评估进度。

其价值：
- 强制 Agent **评估当前进度**
- 记录 **推理过程**
- 决定是否 **调整计划**
- 提高 **决策质量**

### 2.2 与 write_todos 的区别

| 工具 | Deep Agents 用途 | 本项目用途 |
|------|------------------|------------|
| write_todos | 动态创建任务列表 | **不需要** - Planning 模式已有 |
| think_tool | 反思和评估进度 | **需要** - 新增反思能力 |

### 2.3 接口定义

```python
# backend/app/services/agent/deep_agent/reflection.py

from dataclasses import dataclass
from typing import Dict, Any, List, Optional


@dataclass
class ReflectionResult:
    """反思结果"""
    reflection: str           # 反思内容
    needs_replan: bool        # 是否需要重规划
    suggested_tasks: Optional[List[str]] = None  # 建议的新任务


async def think_tool(
    task: Dict[str, Any],
    result: Dict[str, Any],
    remaining_tasks: List[Dict[str, Any]],
    context: Dict[str, Any],
    ai_service,  # HTTPAIService 实例，通过 WritingAgentGraph.ai_service 获取
) -> ReflectionResult:
    """反思工具

    这是一个"上下文工程"工具，不执行实际操作，
    但迫使 Agent 在关键节点评估进度。

    触发时机：
    - 任务执行失败后
    - 分析类任务完成后
    - 每 N 个任务完成后
    - 任务结果质量较低时

    Args:
        task: 刚执行完的任务
        result: 任务执行结果
        remaining_tasks: 剩余待执行的任务
        context: 上下文信息
        ai_service: AI 服务实例

    Returns:
        ReflectionResult: 反思结果，包含是否需要重规划
    """
```

### 2.4 Prompt 设计

```python
REFLECTION_PROMPT = """你是一个 AI Agent，刚刚完成了一个任务。请进行反思。

## 刚完成的任务

- 描述: {task_description}
- 状态: {task_status}
- 输出摘要: {task_output}

## 剩余任务

{remaining_tasks}

## 反思要求

请思考以下问题：
1. 任务执行结果是否达到预期？
2. 是否发现了需要补充的信息？
3. 剩余任务是否仍然合理？
4. 是否需要调整计划？

## 输出格式

请以 JSON 格式回复：
{{
    "reflection": "你的反思内容（简洁明了，不超过 200 字）",
    "needs_replan": true/false,
    "reason": "如果需要重规划，说明原因"
}}
"""
```

### 2.5 使用场景

```
用户: 帮我写第三章，要承接前面的伏笔

AI: [Planning] 生成任务列表
    1. 分析前文伏笔
    2. 生成章节大纲
    3. 撰写章节内容
    4. 校验伏笔回收

AI: [Execution] 执行任务 1: 分析前文伏笔
    结果: 发现 3 个伏笔，但血神宫线索不完整

AI: [think_tool] 反思
    💭 分析发现前文有3个主要伏笔：
       1. 神秘老者的身份（第一章埋下）
       2. 主角的特殊体质（第二章暗示）
       3. 血神宫的阴谋（多处暗线）

       问题：第3个伏笔信息不完整，需要补充分析。
       结论：建议在任务2之前增加"深入分析血神宫线索"任务。

AI: [Replan] 需要重规划 → 更新任务列表
    1. 分析前文伏笔 ✓
    2. 深入分析血神宫线索 (新增)
    3. 生成章节大纲
    4. 撰写章节内容
    5. 校验伏笔回收

AI: 继续执行...
```

### 2.6 错误处理场景

```
场景1: 反思超时
─────────────────────────────────────────────────────
用户: 帮我写第三章

AI: [Execution] 执行任务 1: 分析前文伏笔
    结果: 完成分析

AI: [think_tool] 反思中...
    (超过30秒未响应)

AI: [系统] ⚠️ 反思超时，跳过反思继续执行
    (降级处理：继续执行下一个任务，不触发重规划)

AI: [Execution] 执行任务 2: 生成章节大纲
    ...继续正常执行...
─────────────────────────────────────────────────────

场景2: 反思 JSON 解析失败
─────────────────────────────────────────────────────
AI: [think_tool] 反思
    AI返回: "我觉得分析结果还不错，可以继续了。"
    (非JSON格式)

AI: [系统] 解析反思响应...
    检测关键词: "不错" → needs_replan = False
    (降级处理：使用原始文本作为反思内容)

AI: 💭 反思: 我觉得分析结果还不错，可以继续了。
    (继续执行，不重规划)
─────────────────────────────────────────────────────

场景3: 达到反思上限
─────────────────────────────────────────────────────
AI: [Execution] 任务1 完成 → 触发反思 (1/3)
AI: [Execution] 任务2 完成 → 触发反思 (2/3)
AI: [Execution] 任务3 完成 → 触发反思 (3/3)
AI: [Execution] 任务4 完成
    (检测到需要反思，但已达上限)

AI: [系统] ⚠️ 达到最大反思次数(3)，跳过反思
    (继续执行，防止无限循环)
─────────────────────────────────────────────────────

场景4: 重规划失败
─────────────────────────────────────────────────────
AI: [think_tool] 反思
    💭 需要增加一个新任务来补充分析

AI: [Replan] 生成新任务列表中...
    (AI返回无效JSON或超时)

AI: [系统] ⚠️ 重规划失败，保持原计划继续执行
    (降级处理：不更新任务列表，继续执行剩余任务)
─────────────────────────────────────────────────────
```

## 3. 反思触发条件

### 3.1 配置项

```python
class DeepAgentConfig:
    # 反思限制
    MAX_REFLECTIONS = 3       # 单次请求最多反思次数
    MAX_REPLANS = 2           # 单次请求最多重规划次数

    # 触发条件
    REFLECT_ON_FAILURE = True           # 任务失败时反思
    REFLECT_ON_LOW_QUALITY = True       # 低质量结果时反思
    QUALITY_THRESHOLD = 0.6             # 质量阈值
    REFLECT_ON_ANALYSIS = True          # 分析类任务后反思
    REFLECT_EVERY_N_TASKS = 3           # 每 N 个任务反思一次
```

### 3.2 触发逻辑

```python
def _should_reflect(task, result, completed_count, state):
    """判断是否需要触发反思"""

    # 达到上限则不反思
    if state["reflection_count"] >= MAX_REFLECTIONS:
        return False

    # 条件 1: 任务失败
    if result.status == "failed":
        return True

    # 条件 2: 低质量结果
    if result.quality_score < QUALITY_THRESHOLD:
        return True

    # 条件 3: 分析类任务
    if "分析" in task.description:
        return True

    # 条件 4: 定期反思
    if completed_count % REFLECT_EVERY_N_TASKS == 0:
        return True

    return False
```

## 4. 重规划逻辑

### 4.1 判断是否需要重规划

```python
def _should_replan(reflection: str) -> bool:
    """根据反思内容判断是否需要重规划"""

    keywords = ["需要", "补充", "调整", "新增", "不足", "缺少", "修改计划"]

    for kw in keywords:
        if kw in reflection:
            return True

    return False
```

### 4.2 生成新任务

```python
REPLAN_PROMPT = """基于以下反思，请调整后续任务计划：

反思内容：
{reflection}

原剩余任务：
{remaining_tasks}

请输出调整后的任务列表（JSON 格式），可以：
1. 在开头插入新任务
2. 调整现有任务的描述
3. 删除不必要的任务

输出格式：
{{"tasks": [
    {{"task_id": 1, "description": "任务描述"}},
    ...
]}}
"""
```

## 5. 事件发送

### 5.1 反思内容作为 content 事件

```python
# 反思内容通过 on_content 回调发送
await on_content(f"\n💭 **反思**: {reflection.reflection}\n")
```

前端会在消息流中显示：

```
💭 **反思**: 分析发现前文有3个主要伏笔...
```

### 5.2 重规划作为 plan 事件（更新）

```python
# 重规划后发送更新的 plan 事件
await on_plan({
    "tasks": new_tasks,
    "is_update": True,  # 标记为更新
    "reason": reflection[:100]  # 更新原因
})
```

前端 TaskListPanel 会自动更新任务列表。

## 6. 与现有系统的集成

### 6.1 复用 Planning 的任务管理

```
Planning 模式已有:
├── 任务规划 (_generate_plan)
├── 任务执行 (MultiAgentExecutor)
├── 任务状态 (task_start/task_done)
└── 结果汇总 (_summarize_results)

DeepAgent 新增:
├── 反思检查点 (_should_reflect)
├── 反思执行 (think_tool)
├── 重规划判断 (_should_replan)
└── 任务更新 (_do_replan)
```

### 6.2 事件兼容性

| 事件 | Planning 模式 | DeepAgent 模式 |
|------|--------------|----------------|
| plan | 开始时发送一次 | 开始 + 重规划时更新 |
| task_start | ✅ 复用 | ✅ 复用 |
| task_done | ✅ 复用 | ✅ 复用 |
| content | 最终结果 | 反思 + 最终结果 |
| done | ✅ 复用 | ✅ 复用 |

## 7. task 工具（Phase 3）

### 7.1 设计概念

```python
@tool
def task(
    task_description: str,
    agent_name: str = "default",
    tools: List[str] = None,
    context: Dict[str, Any] = None
) -> str:
    """委派任务给子代理

    创建一个隔离的子代理来执行特定任务。
    子代理有独立的上下文，完成后返回结果摘要。

    适用场景:
    - 需要专业化处理的子任务
    - 可能产生大量中间结果的任务
    - 需要上下文隔离的任务
    """
```

### 7.2 暂不实现原因

1. **复杂度高**：需要设计子代理的生命周期管理
2. **现有能力足够**：MultiAgentExecutor 已能处理多 Agent 协作
3. **优先级低**：Phase 1 的 think_tool 已能满足核心需求

## 8. 总结

| 方面 | 说明 |
|------|------|
| **核心工具** | think_tool（反思） |
| **设计理念** | 纯上下文工程，不执行实际操作 |
| **触发时机** | 任务失败、分析完成、定期检查 |
| **输出** | 反思内容 + 是否需要重规划 |
| **集成方式** | 在 chat_with_planning 的 Execution 阶段插入 |
| **前端影响** | 无需修改，复用现有事件处理 |
