# Bug修复方案：章节号显示问题

## 问题根本原因

**核心问题：时序错误**

当 `tools` 节点被处理时：
1. `node_data["messages"]` 只包含 **ToolMessage**（工具执行结果）
2. 不包含之前的 **AIMessage**（包含tool_calls参数）
3. 代码退化到向后兼容逻辑，从ToolMessage提取工具名
4. 但ToolMessage没有参数，导致 `tool_args={}`

## 修复方案

### 方案1：在agent节点缓存工具调用参数 ⭐ 推荐

**思路：** 在 `writing_agent` 节点结束时提取并缓存tool_calls，在 `tools` 节点时复用

**优点：**
- 简单直接
- 不改变现有架构
- 性能好

**实现：**
```python
# 在 LangGraphAgent 类中添加实例变量
self._cached_tool_calls = {}

# 在 _handle_stream_event 中
async def _handle_stream_event(...):
    # 如果是agent节点，缓存tool_calls
    if node_name in ["writing_agent", "planning_agent", "analysis_agent", "stuck_agent"]:
        messages = node_data.get("messages", [])
        for msg in reversed(messages):
            if isinstance(msg, AIMessage) and msg.tool_calls:
                # 缓存工具调用
                for tool_call in msg.tool_calls:
                    self._cached_tool_calls[tool_call["name"]] = tool_call["args"]

    # 在tools节点使用缓存
    elif node_name == "tools":
        # 先尝试从缓存获取
        if tool_name in self._cached_tool_calls:
            tool_args = self._cached_tool_calls[tool_name]
            # 使用后清除缓存
            del self._cached_tool_calls[tool_name]
```

### 方案2：从完整的messages历史中查找

**思路：** 修改 `_parse_node_event`，从完整的state.messages中查找AIMessage

**优点：**
- 更彻底，总能找到AIMessage
- 不需要缓存

**缺点：**
- 需要传递完整state
- 性能稍差（需要遍历所有消息）

**实现：**
```python
# 修改 _handle_stream_event 签名
async def _handle_stream_event(
    self,
    event,
    state: Optional[AgentState] = None,  # 新增
    ...
):
    # 传递完整state给_parse_node_event
    progress_event = self._parse_node_event(
        node_name,
        node_data,
        progress_tracker,
        state=state  # 新增
    )

# 修改 _parse_node_event
def _parse_node_event(
    self,
    node_name: str,
    node_data: dict,
    progress_tracker: Optional[ProgressTracker] = None,
    state: Optional[AgentState] = None  # 新增
):
    if node_name == "tools":
        # 优先从完整state中查找
        messages = state.get("messages", []) if state else node_data.get("messages", [])
        # ... 现有逻辑
```

### 方案3：修改事件处理逻辑

**思路：** 在 `writing_agent` 节点结束时就生成工具描述，不等到 `tools` 节点

**优点：**
- 参数一定能拿到
- 用户能更早看到进度

**缺点：**
- 改动较大
- 可能和现有进度显示逻辑冲突

## 推荐实施方案1

**理由：**
- 最小改动
- 性能好
- 易于理解和维护

**实施步骤：**
1. 在 `LangGraphAgent.__init__` 中添加 `self._cached_tool_calls = {}`
2. 在 `_handle_stream_event` 的agent节点处理中添加缓存逻辑
3. 在 `_parse_node_event` 的tools节点处理中优先使用缓存
4. 测试验证

## 预期效果

修复后：
```
✅ 📚 正在读取第1章...
✅ 🔍 正在检索「世界观」相关设定...
✅ ✍️ 正在创作内容（目标2000字）...
```

而不是：
```
❌ 📚 正在读取第?章...
```
