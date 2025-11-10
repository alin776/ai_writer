# Phase3 优化#8: 消息清理策略优化

**优先级**: P2（中）📝
**预期收益**: 多轮对话质量+30%
**实施难度**: 🟢 低（70%代码可从Planning复用）
**预计时间**: 3小时（vs 原计划1天）
**当前状态**: ❌ 未开始
**代码复用度**: **70%** 🎯

---

## 🎉 Planning 已实现任务结果压缩逻辑！

**源文件**: `langgraph_agent.py:2858-2894`（40行，70%可复用）

Planning 模式的任务结果压缩算法可直接适配为消息压缩，原理相同。

**复用方案**（3小时 vs 原计划1天）:
- 复用压缩算法（70%）
- 添加消息分类逻辑（30%）

**Planning 模式源代码**:
- `langgraph_agent.py:2858-2894` - 任务结果压缩
- `context/manager.py` - AI智能压缩（参考）

---

## 📋 优化概述

### 问题描述

**当前策略**: 固定保留最近4条消息（2轮对话）

**问题点**:
- ❌ 阈值过低，过早清理
- ❌ 固定策略，不够灵活
- ❌ 可能破坏上下文连贯性

---

## 🎯 优化目标

### 改进对比

| 策略 | 阈值 | 保留用户消息 | 保留交互对 |
|------|------|------------|----------|
| 优化前 | 8条 | 2（固定） | 2（固定） |
| 优化后 | 15条 | 2-4（动态） | 3-5（动态） |

### 验收标准

- [ ] 多轮对话不丢失关键上下文
- [ ] 用户满意度 > 90%

---

## 💡 优化方案

### 核心实现

```python
class ContextManager:
    def __init__(self, ...):
        self.cleanup_thresholds = {
            "small": {"threshold": 20, "keep_user": 2, "keep_pairs": 3},
            "medium": {"threshold": 30, "keep_user": 3, "keep_pairs": 4},
            "large": {"threshold": float("inf"), "keep_user": 4, "keep_pairs": 5}
        }
        self.min_messages_before_cleanup = 15  # 🟢 从8提高到15

    async def compress_context(self, context):
        """压缩上下文 - 动态策略"""
        total_messages = len(context.short_memory.messages)

        # 🟢 动态选择策略
        if total_messages < self.min_messages_before_cleanup:
            return

        if total_messages < 20:
            strategy = self.cleanup_thresholds["small"]
        elif total_messages < 30:
            strategy = self.cleanup_thresholds["medium"]
        else:
            strategy = self.cleanup_thresholds["large"]

        # 🟢 智能成对保留
        keep_count = strategy["keep_pairs"] * 2
        messages_to_keep = messages[-keep_count:]
        messages_to_summarize = messages[:-keep_count]

        # 生成摘要
        summary = await self._generate_summary(messages_to_summarize)
        context.summary_memory.summary = summary
```

---

## 🔧 详细实施步骤

### Day 1: 实现动态策略

**上午**: 修改清理逻辑
**下午**: 测试验证

---

## ✅ 验收标准

- [ ] 多轮对话质量不下降

---

## 📊 预期收益

- 多轮对话质量 +30%
- 上下文连贯性提升

---

**创建日期**: 2025-11-10
**负责人**: 后端开发
**状态**: ❌ 未开始

[返回README](./README.md)
