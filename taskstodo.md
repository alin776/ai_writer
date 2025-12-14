# AI 输出冗余问题 - 深度设计 Review

## 问题描述

**用户请求**：`先分析第一章和第二章的情节发展，然后续写第四章的开头300字`

**预期输出**：情节发展分析（200-500字）+ 续写（300字）

**实际输出**：4000+ 字完整报告（人物、主题、情节、亮点全都有）

## 待办事项

- [x] 1. 分析 focus 参数的设计不一致问题
- [x] 2. 修复工具定义中的正则限制
- [x] 3. 更新 taskstodo.md 记录完整分析

## 深度 Review：设计存在 4 层不一致

### 一、问题全貌

`analyze_text_tool` 的 `focus` 参数在 4 个层次上定义**互相矛盾**：

| 层次 | 文件 | focus 定义 | 状态 |
|-----|------|-----------|------|
| **规划提示词** | `prompt_cache.py` | 任意描述字符串，示例："分析情节"、"概括"、"给出润色建议" | ✅ 灵活设计 |
| **工具定义** | `analysis_tools.py:537` | `pattern="^(all\|grammar\|logic\|style\|structure)$"` | ❌ 过于严格 |
| **模板** | `analyze_text.yaml` | 任意字符串，自动切换简洁/详细模式 | ✅ 灵活设计 |
| **执行代码** | `langgraph_agent.py:5356` | 白名单验证 `["all","grammar","logic","style","structure"]` | ❌ 过于严格 |

### 二、矛盾详解

#### 规划提示词（告诉 AI focus 可以是任意字符串）

```python
# prompt_cache.py 中的示例
focus 参数示例："给出润色建议"、"分析问题并改写"、"使其更有画面感"
- "更丰富" → focus="分析并给出更丰富的改写建议"
- "概括内容" → focus="概括这一章的主要内容：核心事件、涉及人物、情节发展"
```

#### 工具定义（用正则限制 focus 只能是 5 个值）

```python
# analysis_tools.py:534-538
focus: str = Field(
    default="all",
    pattern="^(all|grammar|logic|style|structure)$"  # ← 正则限制！
)
```

#### 模板（支持任意 focus 字符串）

```yaml
# analyze_text.yaml:44,73
{% if focus == "all" or "全面" in focus or "完整" in focus %}
# 详细模式 - 完整报告
{% else %}
# 简洁模式 - 只输出与「{{ focus }}」相关的内容，200-500字
{% endif %}
```

#### 执行代码（白名单验证）

```python
# langgraph_agent.py:5356-5360
valid_focus_values = ["all", "grammar", "logic", "style", "structure"]
if focus_param not in valid_focus_values:
    focus_param = "all"  # ← 强制回退到 all！
```

### 三、问题链

```
用户: "分析第一章和第二章的情节发展"
    ↓
规划阶段: AI 按提示词示例生成 focus="分析情节发展：关键事件、人物关系..."
    ↓
工具定义: Pydantic 验证失败（不匹配正则）→ 但代码绕过了 Pydantic
    ↓
执行代码: 白名单验证失败 → 回退到 focus="all"
    ↓
模板渲染: focus="all" → 触发详细模式
    ↓
输出: 4000+ 字冗余报告
```

## 修复方案

### 修复 1：执行代码（已完成）

**文件**: `langgraph_agent.py:5354-5370`

移除白名单验证，保留 AI 生成的 focus 字符串：

```python
# 修改后
focus_param = params.get("focus", "all")
if not focus_param or "$TASK_" in str(focus_param):
    focus_param = "all"
# 不再强制回退到 "all"
```

### 修复 2：工具定义（已完成）

**文件**: `analysis_tools.py:534-539`

移除正则限制，支持任意字符串：

```python
# 修改前
focus: str = Field(
    default="all",
    pattern="^(all|grammar|logic|style|structure)$"  # ← 删除这行
)

# 修改后
focus: str = Field(
    default="all",
    description="分析重点: 可以是预定义值或任意描述性字符串。当focus='all'或包含'全面/完整'时输出完整报告，否则输出简洁聚焦分析(200-500字)",
    min_length=1,
    max_length=500
)
```

### 不需要修改

- **规划提示词** (`prompt_cache.py`)：设计正确，已经引导 AI 生成描述性 focus
- **模板** (`analyze_text.yaml`)：设计正确，已经支持简洁/详细模式切换

## 修复效果

修复后的流程：

```
用户: "分析第一章和第二章的情节发展"
    ↓
规划阶段: AI 生成 focus="分析情节发展"
    ↓
工具定义: Pydantic 验证通过（无正则限制）
    ↓
执行代码: 不再强制回退，保留 focus="分析情节发展"
    ↓
模板渲染: focus!="all" 且不含"全面/完整" → 触发简洁模式
    ↓
输出: 200-500 字聚焦分析（只包含情节发展相关内容）
```

## Review 总结

| 项目 | 说明 |
|-----|------|
| 问题类型 | **设计一致性问题** - 4 层定义互相矛盾 |
| 根本原因 | 工具定义的正则限制与规划提示词/模板的设计不一致 |
| 影响范围 | 所有使用 `analyze_text_tool` 且 focus 非预定义值的任务 |
| 修复文件 | `langgraph_agent.py`, `analysis_tools.py` |
| 修复方式 | 统一设计：focus 支持任意字符串，由模板决定输出模式 |

## 经验教训

1. **设计一致性**：同一个参数在不同层次（提示词、工具定义、模板、执行代码）的定义必须一致
2. **过早限制**：Pydantic 正则验证虽然严格，但会限制灵活性，需要权衡
3. **模板驱动**：让模板根据参数内容决定行为，比硬编码白名单更灵活
