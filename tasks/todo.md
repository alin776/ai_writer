# 修复 increment_counter 未定义错误

## 问题分析

在 `backend/app/services/agent/langgraph_agent.py` 文件中：
- `chat_with_planning()` 方法在第 2607 行使用了 `increment_counter` 函数
- 但该函数没有在该方法内部导入
- `increment_counter` 只在 `chat()` 方法内部（第 2018 行）导入
- 导致运行时抛出 `NameError: name 'increment_counter' is not defined`

错误日志：
```
NameError: name 'increment_counter' is not defined
at line 2607: increment_counter("planning_phase_start")
```

## 待办任务

- [x] 在 `chat_with_planning()` 方法开始处添加监控工具导入
  - 导入 `increment_counter` 和 `record_timer`
  - 位置：第 2571 行（`import time` 之后）

## Review

### 修复内容
在 `backend/app/services/agent/langgraph_agent.py:2571` 添加了一行代码：
```python
from app.services.agent.utils.monitoring import increment_counter, record_timer
```

### 修复影响
- **文件**：`langgraph_agent.py`
- **改动**：仅添加1行导入语句
- **影响范围**：`chat_with_planning()` 方法现在可以正常使用监控工具
- **风险**：无，这是一个纯粹的缺失导入修复

### 测试建议
重新测试 planning 模式的对话功能，确认：
1. 不再出现 `NameError: name 'increment_counter' is not defined` 错误
2. 监控指标正常记录（planning_phase_start、planning_phase_completed 等）

**修复时间**：2025-11-07
**状态**：✅ 已完成
