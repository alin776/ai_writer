# 修复 LangGraph KeyError: 'step' 问题

## 📋 问题分析

### 错误信息
```
KeyError: 'step'
位置: langgraph\pregel\_loop.py:1262
代码: self.step = self.checkpoint_metadata["step"] + 1
```

### 错误原因
- **根本原因**: LangGraph 在执行 `astream()` 时，尝试从 `checkpoint_metadata` 中获取 'step' 键，但该键不存在
- **触发场景**: 首次创建 checkpoint 或 checkpoint 初始化不完整时
- **影响范围**: 所有使用流式对话的功能都会失败

### 相关代码
- `backend/app/services/agent/langgraph_agent.py:998` - MemorySaver 降级方案
- `backend/app/services/agent/langgraph_agent.py:1135` - 编译 graph 时传入 checkpointer
- `backend/app/services/agent/langgraph_agent.py:2344-2349` - config 配置
- `backend/app/services/agent/langgraph_agent.py:2360` - astream 调用失败点

### 当前 LangGraph 版本
- **版本**: 1.0.1
- **问题**: 该版本在首次使用 checkpoint 时可能缺少 metadata 初始化

## ✅ 待办任务

- [ ] 1. 搜索 LangGraph 1.0.1 相关文档和 issue，了解 checkpoint metadata 初始化要求
- [ ] 2. 修改 config 配置，确保 checkpoint 正确初始化
- [ ] 3. 添加异常处理，捕获 checkpoint 相关错误
- [ ] 4. 测试修复效果

## 🔧 解决方案

### 方案 1：修改 config 配置（推荐）⭐
**描述**: 在 config 中添加 checkpoint_id 或提供初始 metadata

**修改点**:
```python
# 当前代码 (Line 2344-2349)
config = {
    "configurable": {
        "thread_id": conversation_id or "default",
        "checkpoint_ns": ""
    }
}

# 修改为
config = {
    "configurable": {
        "thread_id": conversation_id or "default"
    }
}
```

**优点**:
- 简单快速，修改量小
- 不影响现有功能
- 符合 LangGraph 最佳实践

**缺点**:
- 需要验证是否彻底解决问题

**预计工时**: 30 分钟

---

### 方案 2：添加异常处理和重试机制
**描述**: 在 astream 调用前后添加异常处理，如果 checkpoint 初始化失败则重试

**修改点**:
- 在 `chat_stream` 方法中添加 try-except
- 捕获 KeyError，重新初始化 checkpoint

**优点**:
- 健壮性高，能应对各种异常
- 提供降级方案

**缺点**:
- 代码复杂度增加
- 可能掩盖真正的问题

**预计工时**: 1 小时

---

### 方案 3：升级 LangGraph 版本
**描述**: 升级到最新的 LangGraph 版本，可能已修复此问题

**修改点**:
- 更新 `requirements.txt` 中的 langgraph 版本
- 测试兼容性

**优点**:
- 可能彻底解决问题
- 获得最新功能和修复

**缺点**:
- 可能引入新的兼容性问题
- 需要全面测试

**预计工时**: 2 小时

---

## 📝 实施计划

### 第一步：快速修复（方案 1）
1. 删除 config 中的 `checkpoint_ns: ""`
2. 测试是否解决问题
3. 如果解决，继续；如果未解决，进入第二步

### 第二步：深入调查（如果方案 1 失败）
1. 查看 LangGraph 文档和源码
2. 搜索相关 GitHub issues
3. 确定正确的 config 格式

### 第三步：添加异常处理（备用方案）
1. 实施方案 2
2. 提供详细的错误日志
3. 确保系统稳定性

---

## 📊 Review

### 修复总结

**实施的方案**: 方案 2A - 分离式修复（删除 chat/chat_stream 的 checkpoint_ns，保留 Planning）

**修改的文件**:
- `backend/app/services/agent/langgraph_agent.py`

**代码变更**:
1. ✅ Line 2143: chat() 方法 - 删除 checkpoint_ns
2. ✅ Line 2344-2348: chat_stream() 方法 - 删除 checkpoint_ns
3. ✅ Line 2778, 3092: chat_with_planning() 方法 - **保留** checkpoint_ns

**测试结果**: 待测试

**遗留问题**:
- 需要测试 chat_stream() 是否不再出现 KeyError: 'step'
- 需要验证 Planning 模式对话历史功能是否正常

### 预期效果
- [ ] LangGraph 流式对话正常工作（chat_stream 不报错）
- [ ] 不再出现 KeyError: 'step'
- [ ] Planning 模式对话历史功能正常
- [ ] checkpoint 正常保存和恢复

### 修复详情

#### 修改 1: chat() 方法
```python
# 修改前
config = {"configurable": {"thread_id": conversation_id or "default", "checkpoint_ns": ""}}

# 修改后
config = {"configurable": {"thread_id": conversation_id or "default"}}
```

#### 修改 2: chat_stream() 方法
```python
# 修改前
config = {
    "configurable": {
        "thread_id": conversation_id or "default",
        "checkpoint_ns": ""
    }
}

# 修改后
config = {
    "configurable": {
        "thread_id": conversation_id or "default"
    }
}
```

#### 保持不变: chat_with_planning() 方法
```python
# Line 2778 - 保持不变
config = {"configurable": {"thread_id": conversation_id, "checkpoint_ns": ""}}

# Line 3092 - 保持不变
config = {"configurable": {"thread_id": conversation_id, "checkpoint_ns": ""}}
```

**原因**: Planning 模式手动管理 checkpoint，需要 checkpoint_ns 参数来定位和保存数据。

---

**修复完成时间**: 2025-11-09 23:40
**实际工时**: 约 15 分钟
**修复策略**: 分离式修复，最小化风险

---

## 📝 相关报告

- **FINAL_DIAGNOSIS_REPORT.md** - LangGraph KeyError: 'step' 深度诊断报告
- **PLANNING_CHECKPOINT_ANALYSIS.md** - Planning 模式 checkpoint_ns 使用深度分析报告

---

**创建时间**: 2025-11-09 23:25
**预计总工时**: 30分钟 - 2小时（取决于方案选择）
