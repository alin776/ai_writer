# ReAct 模式问题 Review

> 文档版本: 1.0
> 创建日期: 2025-12-06
> 状态: 已确认问题

---

## 概述

本文档记录对现有 ReAct 模式实现的深度 Review 结果。

---

## 问题1: 模式标识不起作用

### 验证结果: ✅ 确认问题存在

### 代码位置

`backend/app/services/agent/langgraph_agent.py:3048-3056`

### 问题描述

- `chat_stream()` 方法（ReAct模式调用）**硬编码**使用 `"writing_agent"` 系统提示
- 没有任何"思考-行动"分步逻辑
- 与 `chat_with_planning()` 的主要区别仅在于回调结构不同，而非思维模式不同

### 问题代码

```python
# 第3048-3056行 - 硬编码writing_agent模板
system_prompt = self.prompt_manager.render(
    "writing_agent",  # ❌ 无论mode=react还是其他，都用这个模板
    user_message=message,
    context_summary="",
    user_preferences={},
    writing_constraints=[],
    examples=[]
)
```

### 影响

ReAct模式名存实亡，实际行为与普通写作模式无异。

---

## 问题2: 进度/权重配置缺失

### 验证结果: ✅ 确认问题存在

### 代码位置

`backend/app/services/agent/node_metadata.py:194-208`

### 问题描述

`get_scenario_nodes()` 函数只定义了以下场景:
- `writing`, `planning`, `analysis`, `stuck`, `general`
- `writing_with_tools`, `planning_with_tools`, `analysis_with_tools`

**没有 `react` 场景分支**

### 问题代码

```python
scenarios = {
    "writing": ["intent_classifier", "writing_agent"],
    "planning": ["intent_classifier", "planning_agent"],
    "analysis": ["intent_classifier", "analysis_agent"],
    "stuck": ["intent_classifier", "stuck_agent"],
    "general": ["intent_classifier", "general_chat"],
    # ❌ 缺失: "react": [...]
}
```

### 矛盾发现

在第243行的测试代码中，竟然试图计算 `"react"` 场景的权重，但这会返回空列表。

### 影响

前端进度条完全失真，只能显示 `intent_classifier` 的进度。

---

## 问题3: 会话隔离缺失模式维度

### 验证结果: ✅ 确认问题存在

### 代码位置

- `langgraph_agent.py:3092-3101` (chat_stream的thread_id)
- `langgraph_agent.py:3836-3843` (chat_with_planning的thread_id)
- `agent.py:1132-1199` (模式切换逻辑)

### 问题描述

两个方法使用完全相同的 thread_id 构建逻辑:

```python
# chat_stream (ReAct模式)
if work_id and conversation_id:
    thread_id = f"{work_id}:{conversation_id}"

# chat_with_planning (Planning模式)
if work_id and conversation_id:
    isolated_thread_id = f"{work_id}:{conversation_id}"
```

### thread_id 结构问题

- 当前格式: `{work_id}:{conversation_id}`
- 缺少 `mode` 维度
- 切换模式时会复用同一 checkpoint

### 影响

1. Planning模式的规划步骤、工具调用历史会污染到ReAct对话
2. 模式切换后，AI可能会引用不相关的上下文
3. 用户体验混乱

---

## 总结

| 问题 | 严重程度 | 确认状态 | 修复难度 |
|------|---------|---------|---------|
| 模式标识不起作用 | 🔴 严重 | ✅ 确认 | 中等 |
| 进度权重配置缺失 | 🟡 中等 | ✅ 确认 | 简单 |
| 会话隔离缺失模式维度 | 🔴 严重 | ✅ 确认 | 简单 |

---

## 建议

基于以上问题，建议**移除 ReAct 模式**，改为实现更适合写作场景的 **Multi-Agent 模式**。

详见: [02-mode-comparison.md](./02-mode-comparison.md)
