# Phase 2.6 Prompt缓存 - 实施计划

**实施日期**: 2025-11-10
**状态**: 准备实施
**预计耗时**: 2 小时

---

## 📊 现状分析

### Phase 2.5 的影响

在 Phase 2.5 中，我们已经大幅精简了 Prompt：
- **工具决策 Prompt**: 50+ 行 → 18 行（约 150 tokens）
- **Planning Prompt**: 120+ 行 → 32 行（约 240 tokens）

这意味着**可缓存的静态 Token 比文档预期少了很多**。

### 当前 Prompt 结构分析

#### 1. 工具决策 Prompt (langgraph_agent.py:1678-1696)

**结构**:
```
{system_prompt}            ← 未知大小，需要调查
用户: {last_user_message}  ← 动态（每次不同）
{context_info}             ← 动态（work_id, chapter_id）

[静态部分，可缓存，约 100-150 tokens:]
判断是否需要工具。可用工具:
需work_id: get_chapter_by_order, get_context, read_chapter, search_fragments
不需work_id: continue_writing, polish_text, analyze_text

返回JSON:
- 需要: {{"need_tools": true, ...}}
- 缺参数: {{"need_tools": false, ...}}
- 直接答: {{"need_tools": false, ...}}

示例:
"获取第3章" + work_id已设置 → ...
"获取第3章" + work_id未设置 → ...

处理:
```

#### 2. Planning Prompt (langgraph_agent.py:2834-2865)

**结构**:
```
AI写作助手。{history_section}  ← 动态（对话历史）
用户: {message}                  ← 动态
work_id: {work_id}               ← 动态
chapter_id: {chapter_id}         ← 动态

[静态部分，可缓存，约 200-250 tokens:]
生成任务清单JSON。

可用工具:
1. get_chapter_by_order_tool: ...
2. read_chapter_tool: ...
...

规则:
- "第X章" → ...
- UUID格式: ...
- 任务依赖用占位符: ...

示例:
用户: "分析第二章"
{...完整JSON示例...}

返回纯JSON:
```

---

## 🎯 优化策略（调整后）

### 策略 A: 简化实施（推荐）⭐

**原因**: Phase 2.5 已经大幅精简了 Prompt，可缓存的 Token 有限

**实施方案**:
1. **仅缓存工具决策和 Planning 的静态部分** (约 300-400 tokens)
2. **不拆分 Prompt 结构**，使用简单的字符串缓存
3. **预期收益**: Token 节省 15-20%（而非文档中的 50%）
4. **实施时间**: 1 小时

### 策略 B: 完整实施（文档原计划）

**实施方案**:
1. 拆分所有 Prompt 为静态+动态
2. 使用 `@cache_review` 装饰器
3. 调查并缓存 `system_prompt`
4. **预期收益**: 取决于 `system_prompt` 的大小
5. **实施时间**: 2-3 小时

---

## 📋 实施计划（策略 A - 简化实施）

### Step 1: 创建静态 Prompt 缓存函数 (30分钟)

创建两个简单的缓存函数：

```python
# backend/app/services/agent/prompt_cache.py

from app.core.cache import cache_review

@cache_review(expire=3600, key_prefix="prompt")
async def get_tool_decision_static_prompt() -> str:
    """获取工具决策的静态 Prompt 部分（可缓存）"""
    return """判断是否需要工具。可用工具:
需work_id: get_chapter_by_order, get_context, read_chapter, search_fragments
不需work_id: continue_writing, polish_text, analyze_text

返回JSON:
- 需要: {{"need_tools": true, "tool_name": "工具名", "tool_args": {{}}}}
- 缺参数: {{"need_tools": false, "direct_response": "请提供..."}}
- 直接答: {{"need_tools": false, "direct_response": "..."}}

示例:
"获取第3章" + work_id已设置 → {{"need_tools": true, "tool_name": "get_chapter_by_order_tool", "tool_args": {{"chapter_order": 3}}}}
"获取第3章" + work_id未设置 → {{"need_tools": false, "direct_response": "请先告诉我是哪部作品？"}}

处理:"""


@cache_review(expire=3600, key_prefix="prompt")
async def get_planning_static_prompt() -> str:
    """获取 Planning 的静态 Prompt 部分（可缓存）"""
    return """生成任务清单JSON。

可用工具:
1. get_chapter_by_order_tool: 按序号获取章节 (参数: chapter_order)
2. read_chapter_tool: 按ID读取章节 (参数: chapter_id, UUID格式)
3. get_context_tool: 获取作品上下文 (无参数)
4. search_analysis_fragments_tool: 搜索设定 (参数: query)
5. continue_writing_tool: 续写 (参数: context, requirements)
6. polish_text_tool: 润色 (参数: text, style)
7. analyze_text_tool: 分析 (参数: text, focus)

规则:
- "第X章" → 用 get_chapter_by_order_tool
- UUID格式: xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx (标准36字符)
- 任务依赖用占位符: $TASK_N.field$ (如 $TASK_1.content$)

示例:
用户: "分析第二章"
{{
  "user_intent": "分析第二章内容",
  "tasks": [
    {{"task_id": 1, "description": "获取第二章", "tool": "get_chapter_by_order_tool", "params": {{"chapter_order": 2}}, "estimated_time": "5秒"}},
    {{"task_id": 2, "description": "分析章节", "tool": "analyze_text_tool", "params": {{"text": "$TASK_1.content$", "focus": "情节"}}, "estimated_time": "10秒"}}
  ]
}}

返回纯JSON:"""
```

### Step 2: 修改工具决策 Prompt (15分钟)

```python
# langgraph_agent.py 行 1678-1696

async def _handle_with_httpai(self, state, agent_type, system_prompt):
    # ... 第二次进入的逻辑 ...

    # 第一次进入：使用 HTTPAIService 决定是否需要工具
    last_user_message = messages[-1].content

    # ... 格式化 context_info ...

    # ✅ Phase 2.6: 使用缓存的静态 Prompt
    from app.services.agent.prompt_cache import get_tool_decision_static_prompt

    static_prompt = await get_tool_decision_static_prompt()

    decision_prompt = f"""{system_prompt}

用户: {last_user_message}
{context_info}

{static_prompt}"""

    # ... 其余逻辑不变 ...
```

### Step 3: 修改 Planning Prompt (15分钟)

```python
# langgraph_agent.py 行 2834-2865

async def _handle_planning_mode(self, state):
    # ... 历史记录逻辑 ...

    # ✅ Phase 2.6: 使用缓存的静态 Prompt
    from app.services.agent.prompt_cache import get_planning_static_prompt

    static_prompt = await get_planning_static_prompt()

    plan_prompt = f"""AI写作助手。{history_section}
用户: {message}
work_id: {work_id}
chapter_id: {chapter_id}

{static_prompt}"""

    # ... 其余逻辑不变 ...
```

---

## ✅ 验收标准

- [ ] 缓存功能正常工作
- [ ] 静态 Prompt 被正确缓存到 Redis
- [ ] 缓存命中时不重复构建 Prompt
- [ ] 功能无回归（所有测试通过）
- [ ] 缓存命中率 > 80%（第二次请求开始命中）
- [ ] 内存增长 < 10MB

---

## 📊 预期收益（调整后）

### Token 节省估算

| 场景 | 静态 Tokens | 缓存节省 | 说明 |
|------|------------|---------|------|
| 工具决策 | ~150 | 100% | 第2次请求开始节省 |
| Planning | ~250 | 100% | 第2次请求开始节省 |
| **总计** | ~400 | **15-20%** | 相对于总 Prompt |

### 成本节省估算

**假设**:
- 每月 10,000 次调用
- 每次调用平均 2000 tokens (输入)
- 缓存命中率 70%
- 模型: gemini-2.5-flash-lite ($0.03 per 1M tokens)

**计算**:
```
节省 tokens = 10,000 * 0.7 * 400 = 2,800,000 tokens/月
月度节省 = 2,800,000 * $0.03 / 1,000,000 = $0.084
年度节省 = $0.084 * 12 = $1.008 (约 $1)
```

**结论**: 由于 Phase 2.5 已经大幅精简了 Prompt，**缓存的收益较小**（年度节省约 $1）。

---

## 💡 建议

### 建议 1: 简化实施，降低预期 ⭐ 推荐

**原因**:
- Phase 2.5 已经精简了 Prompt，可缓存的 Token 有限
- 成本收益比较低（年度节省约 $1 vs 2小时开发）
- 缓存增加了系统复杂度

**实施**:
- 只做简单的缓存（1小时）
- 为未来更大的 Prompt 优化打下基础

### 建议 2: 跳过 Phase 2.6，优先其他优化

**原因**:
- ROI 很低（$1/年 vs 2小时）
- 可以优先实施 Phase 3（并行、错误处理等）

---

## 🚀 下一步

**请确认实施策略**:
- **策略 A**: 简化实施（1小时，年度节省 ~$1）
- **策略 B**: 完整实施（2-3小时，需要调查 system_prompt）
- **策略 C**: 跳过 Phase 2.6，优先 Phase 3

---

**创建时间**: 2025-11-10
