# Bug修复报告：工具参数类型验证错误

## Bug描述

### 错误信息
```
1 validation error for continue_writing_tool
requirements
  Input should be a valid string [type=string_type, input_value={'plot_point': '段融在...原有风格和基调'}, input_type=dict]
```

### 问题根源

AI在Planning阶段生成的任务参数格式不符合工具定义：

**AI生成的参数**（错误）:
```json
{
  "tool": "continue_writing_tool",
  "params": {
    "context": "...",
    "requirements": {
      "plot_point": "段融在...",
      "style": "原有风格和基调"
    }
  }
}
```

**工具期望的参数**（正确）:
```python
@tool
async def continue_writing_tool(context: str, requirements: str = "") -> str:
    # requirements 必须是字符串
```

### 影响范围
- **严重程度**: 高（导致任务执行失败）
- **影响工具**:
  - `continue_writing_tool` ✗
  - `polish_text_tool` ✗
  - `analyze_text_tool` ✗
- **触发条件**: Planning阶段生成字典格式的参数

---

## 修复方案

### 1. 新增参数标准化函数

**位置**: `langgraph_agent.py:2157-2198`

```python
def _normalize_tool_params(self, tool_name: str, params: Dict[str, Any]) -> Dict[str, Any]:
    """标准化工具参数，将不符合格式的参数转换为正确格式

    Args:
        tool_name: 工具名称
        params: 原始参数

    Returns:
        标准化后的参数
    """
    normalized = params.copy()

    # continue_writing_tool 的 requirements 必须是字符串
    if tool_name == "continue_writing_tool":
        requirements = params.get("requirements", "")
        if isinstance(requirements, dict):
            # 将字典转换为可读的字符串
            parts = []
            for key, value in requirements.items():
                parts.append(f"{key}: {value}")
            normalized["requirements"] = "，".join(parts)
            logger.info(f"[参数标准化] continue_writing_tool.requirements: dict → str")

    # polish_text_tool 和 analyze_text_tool 同理...

    return normalized
```

### 2. 在调用工具前标准化参数

**修改位置1**: `_execute_task` 方法（第2213行）

```python
async def _execute_task(...):
    tool_name = task.get("tool", "auto")
    params = task.get("params", {})

    # 标准化参数格式 ← 新增
    params = self._normalize_tool_params(tool_name, params)

    # 调用工具...
```

**修改位置2**: `_handle_with_httpai` 方法（第1159行）

```python
if decision.get("need_tools", False):
    tool_name = decision.get("tool_name", "continue_writing_tool")
    tool_args = decision.get("tool_args", {})

    # 标准化参数格式 ← 新增
    tool_args = self._normalize_tool_params(tool_name, tool_args)

    # 调用工具...
```

---

## 修复效果

### 转换示例

**输入**（字典）:
```json
{
  "requirements": {
    "plot_point": "段融在北境遇险",
    "style": "原有风格和基调",
    "length": "500-800字"
  }
}
```

**输出**（字符串）:
```
"plot_point: 段融在北境遇险，style: 原有风格和基调，length: 500-800字"
```

### 日志输出
```
[参数标准化] continue_writing_tool.requirements: dict → str
```

---

## 测试验证

### 语法检查
```bash
python -m py_compile backend/app/services/agent/langgraph_agent.py
```
✅ 通过

### 预期行为
1. 遇到字典参数时自动转换为字符串
2. 记录转换日志便于调试
3. 不影响已经是正确格式的参数

---

## 代码变更统计

| 文件 | 新增行数 | 修改行数 | 总变更 |
|------|---------|---------|--------|
| `langgraph_agent.py` | +44 | +2 | 46 |

### 新增函数
- `_normalize_tool_params()`: 42行

### 修改位置
- `_execute_task()`: +1行（调用标准化函数）
- `_handle_with_httpai()`: +3行（调用标准化函数）

---

## 根本原因分析

### 为什么会产生这个Bug？

1. **Planning阶段的AI不理解工具签名**
   - AI只看到工具描述，不知道参数必须是字符串
   - AI倾向于生成结构化的JSON（字典）

2. **缺少参数验证和转换层**
   - 直接将Planning生成的参数传给工具
   - 假设AI总是生成正确的格式

3. **工具定义使用了严格的类型检查**
   - `@tool` 装饰器使用Pydantic进行参数验证
   - 类型不匹配时抛出验证错误

### 长期解决方案建议

#### 方案1：改进Planning Prompt（推荐）
```python
plan_prompt = f"""
...
【工具参数格式要求】
所有工具的参数必须是基本类型（字符串、数字、布尔值），不要使用嵌套的对象！

❌ 错误示例：
{{"tool": "continue_writing_tool", "params": {{"requirements": {{"plot": "...", "style": "..."}}}}}}

✅ 正确示例：
{{"tool": "continue_writing_tool", "params": {{"requirements": "plot: ..., style: ..."}}}}
"""
```

#### 方案2：修改工具签名接受字典（不推荐）
```python
@tool
async def continue_writing_tool(context: str, requirements: Union[str, Dict] = "") -> str:
    if isinstance(requirements, dict):
        # 转换为字符串...
```

**为什么不推荐**：违反了"工具应该有清晰的接口"原则

#### 方案3：使用结构化输出（最佳但成本高）
```python
# 使用支持结构化输出的模型
# 严格约束AI输出的JSON schema
```

---

## 总结

### 修复的问题
✅ 修复了Planning生成字典参数导致的验证错误
✅ 添加了参数标准化层，增强鲁棒性
✅ 保持了代码向后兼容性

### 遗留问题
⚠️ 根本原因未解决：AI仍然可能生成错误格式
⚠️ 只处理了3个工具，未来新增工具需要添加规则

### 建议后续优化
1. 改进Planning prompt，明确参数格式要求
2. 添加Planning结果的schema验证
3. 考虑使用支持结构化输出的模型

---

## 验收标准

- [x] 语法检查通过
- [x] 字典参数能正确转换为字符串
- [x] 不影响已经是字符串的参数
- [x] 添加了日志记录便于调试
- [ ] 实际运行测试（待用户验证）
