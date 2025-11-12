# Bug修复完成总结

## 修复内容

### Bug描述
前台显示：`📚 正在读取第?章...`
期望显示：`📚 正在读取第1章...`

### 根本原因
在 `tools` 节点被处理时，`node_data["messages"]` 中已经没有AIMessage（包含tool_calls参数），只有ToolMessage（工具执行结果），导致无法获取工具调用参数。

### 修复方案
采用**参数缓存机制**：
1. 在 `writing_agent` 等节点结束时，提取并缓存 `tool_calls` 参数
2. 在 `tools` 节点处理时，优先使用缓存的参数
3. 使用后立即清除缓存

### 代码修改

#### 1. 添加缓存变量 (langgraph_agent.py:1070-1071)
```python
# 🔧 缓存工具调用参数（用于进度显示）
self._cached_tool_calls = {}
```

#### 2. 缓存工具参数 (langgraph_agent.py:2617-2628)
```python
# 🔧 缓存agent节点的工具调用参数（用于后续tools节点显示）
if node_name in ["writing_agent", "planning_agent", "analysis_agent", "stuck_agent", "general_agent"]:
    messages = node_data.get("messages", [])
    for msg in reversed(messages):
        if isinstance(msg, AIMessage) and hasattr(msg, "tool_calls") and msg.tool_calls:
            for tool_call in msg.tool_calls:
                tool_name = tool_call.get("name")
                tool_args = tool_call.get("args", {})
                if tool_name:
                    self._cached_tool_calls[tool_name] = tool_args
                    logger.debug(f"[Cache] 缓存工具参数: {tool_name} -> {tool_args}")
            break  # 只缓存最新的一条AIMessage
```

#### 3. 使用缓存参数 (langgraph_agent.py:2763-2769)
```python
# 🔧 优先使用缓存的参数（如果有）
if tool_name in self._cached_tool_calls:
    cached_args = self._cached_tool_calls[tool_name]
    logger.info(f"[Tools Node] 使用缓存参数: {tool_name} -> {cached_args}")
    tool_args = cached_args
    # 使用后清除缓存
    del self._cached_tool_calls[tool_name]
```

## 测试验证

### 测试步骤
1. 重启后端服务
2. 发送测试请求："第一章讲了什么？"
3. 观察前台进度显示和后台日志

### 预期结果

**前台显示：**
```
✅ 📚 正在读取第1章...
```

**后台日志应包含：**
```
[Cache] 缓存工具参数: get_chapter_by_order_tool -> {'chapter_order': 1, ...}
[Tools Node] 使用缓存参数: get_chapter_by_order_tool -> {'chapter_order': 1, ...}
[Tools Node] 最终使用: tool_name=get_chapter_by_order_tool, tool_args={'chapter_order': 1, ...}
```

### 验收标准
- [ ] 前台显示具体章节号（如"第1章"、"第2章"）
- [ ] 不再显示"?"
- [ ] 其他工具也能正确显示参数（如"正在检索「xxx」相关设定..."）
- [ ] 日志中能看到缓存和使用的过程

## 影响范围
- **修改文件：** `backend/app/services/agent/langgraph_agent.py`
- **修改行数：** 3处，共约15行代码
- **影响功能：** 所有工具调用的进度显示
- **风险评估：** 低风险（只影响显示，不影响功能）

## 附加优化
修复还包含了详细的调试日志，方便未来追踪类似问题。
