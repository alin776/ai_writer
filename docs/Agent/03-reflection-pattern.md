# P0-3: Reflection 反思机制

> 优先级：🔴 P0（核心功能）
>
> 工作量：2-3天
>
> 预期收益：自动质量优化、减少低质输出

---

## 📋 问题描述

当前系统一次性生成内容，没有质量评估和迭代改进机制。

---

## 🎯 解决方案：Generate → Reflect → Revise 循环

```
┌──────────────────────────────────────┐
│         Reflection Loop              │
│                                      │
│  ┌──────────┐    ┌──────────┐      │
│  │ Generate │ ──>│ Evaluate │      │
│  │ Content  │    │ Quality  │      │
│  └──────────┘    └─────┬────┘      │
│       ▲                 │           │
│       │                 ▼           │
│       │          ┌────────────┐    │
│       │          │ Score < 80?│    │
│       │          └──┬─────┬───┘    │
│       │             │ YES │ NO     │
│       │      ┌──────▼─┐   │        │
│       └──────│ Revise │   ▼        │
│              │ Content│  Done       │
│              └────────┘             │
└──────────────────────────────────────┘
```

---

## 🔧 实现步骤

### Step 1: 扩展状态

```python
class ReflectionState(TypedDict):
    """包含反思的状态"""
    # ... 原有字段
    generated_content: Optional[str]
    quality_score: Optional[float]
    quality_issues: List[str]
    revision_count: int
    max_revisions: int  # 最大迭代次数
    reflection_history: List[Dict]
```

### Step 2: 实现 Reflection Node

```python
async def reflection_node(state: ReflectionState) -> ReflectionState:
    """反思节点：评估内容质量"""

    content = state["generated_content"]

    # 使用 LLM 评估质量
    prompt = f"""
请评估以下内容的质量（0-100分），并指出问题。

内容:
{content}

评估维度:
1. 语言流畅性
2. 逻辑连贯性
3. 细节丰富度
4. 符合要求程度

返回 JSON:
{{
    "score": 分数,
    "issues": ["问题1", "问题2"],
    "suggestions": ["建议1", "建议2"]
}}
"""

    evaluation = await ai_service.generate(prompt, temperature=0.3)
    eval_data = json.loads(evaluation)

    state["quality_score"] = eval_data["score"]
    state["quality_issues"] = eval_data["issues"]
    state["reflection_history"].append(eval_data)

    return state

def should_revise(state: ReflectionState) -> Literal["revise", "accept"]:
    """决定是否需要修订"""

    score = state["quality_score"]
    revision_count = state["revision_count"]
    max_revisions = state["max_revisions"]

    if score < 80 and revision_count < max_revisions:
        return "revise"
    else:
        return "accept"

# 构建带反思的图
workflow.add_node("generate", generate_node)
workflow.add_node("reflect", reflection_node)
workflow.add_node("revise", revise_node)

workflow.add_edge("generate", "reflect")

workflow.add_conditional_edges(
    "reflect",
    should_revise,
    {
        "revise": "revise",    # 循环回去修订
        "accept": END          # 接受结果
    }
)

workflow.add_edge("revise", "reflect")  # 修订后再评估
```

### Step 3: 实现 Revise Node

```python
async def revise_node(state: ReflectionState) -> ReflectionState:
    """修订节点：根据反思改进内容"""

    content = state["generated_content"]
    issues = state["quality_issues"]

    prompt = f"""
请改进以下内容，解决这些问题：

原内容:
{content}

问题:
{chr(10).join(f'- {issue}' for issue in issues)}

要求:
1. 保持原意
2. 解决所有问题
3. 提升整体质量
"""

    improved_content = await ai_service.generate(prompt, temperature=0.7)

    state["generated_content"] = improved_content
    state["revision_count"] += 1

    return state
```

---

## 📚 参考资源

- **Reflection Pattern**：https://github.com/langchain-ai/langgraph/tree/main/examples/reflection
- **Content Writer Feedback Loop**：https://github.com/langchain-ai/content-writer

---

**下一步**：实施完成后，继续 [并行工具调用](./04-parallel-execution.md)
