# Bug分析报告：章节显示为"?"问题

## 问题描述

前台显示：`📚 正在读取第?章...`
期望显示：`📚 正在读取第1章...`

## 问题日志

从 INFO.md 第42行：
```
'description': '📚 正在读取第?章...',
'tool_args': {}
```

关键线索：
- 第23行：`chapter_num=None` （初次创建WritingAction时）
- 第28行：检测到工具调用 `get_chapter_by_order_tool`
- 第42行：显示 `'📚 正在读取第?章...'` ，`tool_args` 为**空字典**
- 第49行：`从消息中识别到章节号: 1` （工具执行后）

## 问题定位

### 1. 工具定义（✅ 正常）

`backend/app/services/agent/langgraph_agent.py:500`
```python
async def get_chapter_by_order_tool(
    work_id: Optional[str] = None,
    chapter_order: int = 1  # ✅ 参数名: chapter_order
) -> str:
```

### 2. 进度描述生成（✅ 正常）

`backend/app/services/agent/langgraph_agent.py:2805-2808`
```python
if tool_name == "get_chapter_by_order_tool":
    chapter_order = tool_args.get("chapter_order", "?")  # ✅ 正确获取参数
    return f"📚 正在读取第{chapter_order}章..."
```

### 3. 参数提取逻辑（🔍 需要调查）

`backend/app/services/agent/langgraph_agent.py:2707-2739`
```python
# ✅ 从AIMessage提取tool_calls参数
messages = node_data.get("messages", [])
tool_info = None

# 寻找AIMessage中的tool_calls（倒序查找最新的）
for msg in reversed(messages):
    if isinstance(msg, AIMessage) and hasattr(msg, "tool_calls") and msg.tool_calls:
        # 取第一个tool_call
        tool_call = msg.tool_calls[0]
        tool_info = {
            "name": tool_call.get("name"),
            "args": tool_call.get("args", {})  # 🔍 应该能拿到args
        }
        break
```

## 问题根本原因（待验证）

**可能原因1：LLM没有传递参数**
- LLM在调用 `get_chapter_by_order_tool` 时，没有传递 `chapter_order` 参数
- 导致 `tool_call["args"]` 为空字典 `{}`

**可能原因2：参数提取时机错误**
- 在 `tools` 节点被处理时，AIMessage 还没有正确加入 `messages` 列表
- 或者 `node_data.get("messages")` 返回的不是预期的消息列表

**可能原因3：参数名不匹配**
- LLM使用了其他参数名（如 `order`, `chapter_num`）而不是 `chapter_order`
- 但工具定义的参数名是 `chapter_order`

## 需要验证的点

1. ✅ 查看LLM实际调用时的 `tool_calls` 结构和参数
2. ⬜ 确认 `node_data["messages"]` 中是否包含正确的AIMessage
3. ⬜ 确认 `tool_call["args"]` 的实际内容
4. ⬜ 检查是否是LLM的prompt问题，没有指示传递参数

## 下一步

1. 添加详细日志，输出 `tool_call` 的完整结构
2. 验证 LLM 是否正确传递了 `chapter_order` 参数
3. 如果LLM没传参数，检查prompt是否需要优化
4. 如果是参数名问题，考虑支持多种参数名（`chapter_order`, `order`, `chapter_num`）
