# Phase2 优化#5: Token消耗优化

**优先级**: P1（高）💰
**预期收益**: Token节省83%（1860 → 320）
**实施难度**: 🟢 低（60%代码可从Planning复用）
**预计时间**: 2小时（vs 原计划0.5天）
**当前状态**: ❌ 未开始
**代码复用度**: **60%** 🎯

---

## 🎉 ModelSelector 已100%可用！

**源文件**: `model_selector.py`

ModelSelector 已正确实施，支持根据任务类型自动选择最优模型。

**剩余工作**: 精简Prompt（40%新工作）

**Planning 模式源代码**:
- `model_selector.py` - 模型选择（100%可复用）

---

## 📋 优化概述

### 问题描述

**当前Token消耗**（BACKEND.md）:
- 意图识别: **1860 tokens** (prompt=1792, completion=68)
- Prompt过长: 1792 tokens
- 使用昂贵模型: gemini-2.5-pro而非flash-lite

**问题点**:
1. ❌ Prompt冗长（1792 tokens，可优化到300）
2. ❌ 使用pro模型（成本是flash-lite的10倍）
3. ❌ max_tokens=50过大（实际只需20）
4. ❌ 无Prompt缓存

### 影响范围

**成本影响**:
- 当前成本: $0.000046/次 × 120,000次/年 = **$552/年**
- 优化后: $0.000008/次 × 120,000次/年 = **$96/年**
- **年度节省: $456** 💰

---

## 🎯 优化目标

### 性能指标

| 指标 | 优化前 | 优化后 | 节省 |
|------|-------|--------|------|
| Prompt tokens | 1792 | 300 | **83%** |
| Completion tokens | 68 | 20 | **71%** |
| 总Token | 1860 | 320 | **83%** |
| 单次成本 | $0.000046 | $0.000008 | **83%** |

### 验收标准

- [ ] Token消耗 < 400
- [ ] 使用flash-lite模型
- [ ] 准确率下降 < 2%
- [ ] max_tokens减少到20

---

## 💡 优化方案

### 优化1: 精简Prompt

**当前Prompt** (1792 tokens):
```python
prompt = f"""分析用户意图，返回以下之一：
- writing: 续写、扩写相关
- planning: 规划、大纲、世界观相关
- analysis: 分析、评估、诊断相关
- stuck: 卡文、灵感、方向相关
- general: 一般对话

用户消息：{last_message}

只返回意图类型，不要其他内容。"""
```

**优化后Prompt** (~150 tokens):
```python
# 使用简写映射
INTENT_MAP = {
    "w": "writing", "p": "planning",
    "a": "analysis", "s": "stuck", "g": "general"
}

prompt = f"""分类[w写|p划|a析|s卡|g话]: {last_message[:200]}
JSON: {{"intent":"w","conf":0.95}}"""
```

### 优化2: 使用flash-lite模型

```python
# 当前 Bug: 代码中标注使用flash-lite但实际用的pro
task_type=TaskType.TEXT_CLASSIFICATION  # 应该映射到flash-lite

# 修复ModelSelector
class ModelSelector:
    MODEL_MAPPING = {
        TaskType.TEXT_CLASSIFICATION: "gemini-2.5-flash-lite",  # ✅
        TaskType.CONTENT_CREATION: "gemini-2.5-pro",
    }
```

### 优化3: 减少max_tokens

```python
result = await self._generate_text(
    prompt=prompt,
    max_tokens=20,  # 从50减到20
    task_type=TaskType.TEXT_CLASSIFICATION
)
```

---

## 🔧 详细实施步骤

### 上午 (2小时)

**Step 1: 精简Prompt** (30分钟)
**Step 2: 修复模型选择** (1小时)
**Step 3: 减少max_tokens** (30分钟)

### 下午 (2小时)

**Step 4: A/B测试** (1小时)
**Step 5: 性能验证** (1小时)

---

## ✅ 验收标准

- [ ] Token < 400
- [ ] 模型使用flash-lite
- [ ] 准确率 > 93%

---

## 📊 预期收益

| 指标 | 优化前 | 优化后 | 节省 |
|------|-------|--------|------|
| Token | 1860 | 320 | 83% |
| 年度成本 | $552 | $96 | **$456** 💰 |

---

**创建日期**: 2025-11-10
**负责人**: 后端开发
**状态**: ❌ 未开始

[返回README](./README.md)
