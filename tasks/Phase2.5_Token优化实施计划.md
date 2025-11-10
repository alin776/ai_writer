# Phase 2.5 Token消耗优化 - 实施计划

**日期**: 2025-11-10
**状态**: 待确认

---

## 📊 当前情况分析

### 已完成的优化 ✅

1. **Phase 2.4 已完成**: 意图识别从 LLM 改为规则识别
   - Token 消耗: 1860 → 0 (100%节省)
   - 耗时: 16秒 → <1ms (99.99%提升)

2. **ModelSelector 已100%可用**:
   - ✅ 已实现并集成到 HTTPAIService
   - ✅ 默认启用 (`MODEL_SELECTION_ENABLED=True`)
   - ✅ 所有 4 个 LLM 调用都传递了正确的 `task_type`
   - ✅ 自动根据任务类型选择模型（SIMPLE→flash-lite, MEDIUM→flash, COMPLEX→pro）

### 当前的 LLM 调用点

| 位置 | 用途 | max_tokens | task_type | 模型选择 |
|------|------|------------|-----------|----------|
| 行 1637 | 最终响应生成 | 1500 | 智能选择 | ✅ 已优化 |
| 行 1733 | 工具决策 | 500 | SIMPLE_QA | ✅ flash-lite |
| 行 2993 | Planning规划 | 1000 | SIMPLE_QA | ✅ flash-lite |
| 行 3770 | 最终摘要 | 2000 | SUMMARIZATION | ✅ flash |

---

## 🎯 待优化项目

### 优化 #1: 精简工具决策 Prompt (行 1678-1730)

**当前长度**: 约 400+ tokens（不含 system_prompt）

**问题点**:
- 过多的说明文字
- 重复的示例
- 冗长的格式说明

**优化目标**: 减少到 150-200 tokens (节省50%)

**优化方案**:
```python
# 精简后的 Prompt
decision_prompt = f"""你是小说创作助手。判断是否需要工具。

用户: {last_user_message}
上下文: work_id={_format_id(current_work_id)}, chapter_id={_format_id(current_chapter_id)}

工具列表:
需work_id: get_chapter_by_order, get_context, read_chapter, search_fragments
不需work_id: continue_writing, polish_text, analyze_text

返回JSON:
- 需要工具: {{"need_tools": true, "tool_name": "工具名", "tool_args": {{}}}}
- 缺参数: {{"need_tools": false, "direct_response": "请提供..."}}
- 直接回答: {{"need_tools": false, "direct_response": "..."}}

示例:
用户: "获取第3章" + work_id已设置 → {{"need_tools": true, "tool_name": "get_chapter_by_order_tool", "tool_args": {{"chapter_order": 3}}}}
用户: "获取第3章" + work_id未设置 → {{"need_tools": false, "direct_response": "请先告诉我是哪部作品？"}}

现在处理:"""
```

**预期收益**:
- Token: 400+ → 150 (节省62%)
- 年度节省: 约 $150 (假设每月 10,000 次调用)

---

### 优化 #2: 优化 max_tokens 设置

**当前设置**:
- 工具决策: 500 → 建议改为 **200** (JSON 响应通常 <100 tokens)
- Planning规划: 1000 → 建议改为 **600** (JSON 任务列表)
- 最终摘要: 2000 → **保持** (需要详细响应)
- 最终响应: 1500 → **保持** (需要详细响应)

**预期收益**:
- 减少输出 Token 消耗约 30%
- 年度节省: 约 $100

---

### 优化 #3: 精简 Planning Prompt (行 2950-2990)

**当前问题**: Prompt 包含过多说明

**优化方案**: 简化任务列表格式说明，移除冗余示例

**预期收益**: Token 节省约 20%

---

## 📝 实施步骤

### Step 1: 精简工具决策 Prompt (30分钟)

1. 修改 `langgraph_agent.py` 行 1678-1730
2. 移除冗余说明和示例
3. 保持功能不变

### Step 2: 优化 max_tokens (10分钟)

1. 修改工具决策: 500 → 200
2. 修改 Planning: 1000 → 600

### Step 3: 精简 Planning Prompt (20分钟)

1. 修改 `langgraph_agent.py` 行 2950-2990
2. 简化格式说明

### Step 4: 测试验证 (30分钟)

1. 运行集成测试
2. 对比优化前后的 Token 消耗
3. 确认功能正常

---

## ✅ 验收标准

- [ ] 工具决策 Prompt < 200 tokens
- [ ] 所有测试通过，功能正常
- [ ] Token 消耗减少至少 30%
- [ ] max_tokens 设置合理
- [ ] 生成优化报告

---

## 📊 预期收益

| 指标 | 优化前 | 优化后 | 节省 |
|------|-------|--------|------|
| 工具决策 Token | 400+ | 150 | 62% |
| Planning Token | 1000 | 600 | 40% |
| max_tokens (决策) | 500 | 200 | 60% |
| max_tokens (规划) | 1000 | 600 | 40% |
| **年度成本节省** | - | - | **$250+** 💰 |

---

## 🚀 下一步

请确认此计划，我将开始实施优化。

**预计完成时间**: 1.5 小时
