# LangGraph Agent 重构文档

**日期**: 2025-12-09
**版本**: alin3.0
**作者**: Claude Code

---

## 1. 重构背景

### 1.1 原始问题

`langgraph_agent.py` 文件过于庞大（6156 行），包含了：
- LangChain @tool 装饰器工具函数
- 上下文构建辅助函数
- Agent 状态管理
- 工作流节点定义
- 主 Agent 类

这导致：
- 代码难以维护
- 单元测试困难
- 循环导入风险
- 代码复用性差

### 1.2 重构目标
## 2. 文件变更概览

| 文件 | 变更类型 | 行数变化 |
|------|----------|----------|
| `langgraph_agent.py` | 修改 | 6156 → 4966 行 |
| `langgraph_tools.py` | 新建 | 712 行 |
| `utils/context_builder.py` | 新建 | 211 行 |
| `tools/editor_tools.py` | 修复 | 571 行 |

---

## 3. 新建模块详情

### 3.1 langgraph_tools.py

**路径**: `backend/app/services/agent/langgraph_tools.py`

**职责**: 集中管理所有 LangChain @tool 装饰器工具

**导出内容**:

```python
# 全局服务管理
set_global_ai_service(ai_service: HTTPAIService)
get_global_ai_service() -> Optional[HTTPAIService]

# 辅助函数
validate_uuid(value: str, field_name: str) -> Optional[str]
_retry_on_failure(func, *args, max_retries=3, **kwargs)
_generate_text_helper(prompt, temperature, max_tokens, task_type) -> str

# 写作工具 (3个)
continue_writing_tool(context: str, requirements: str) -> str
polish_text_tool(text: str, style: str) -> str
analyze_text_tool(text: str, focus: str) -> str

# 章节工具 (4个)
read_chapter_tool(work_id: str, chapter_id: str) -> str
get_chapter_by_order_tool(work_id: str, chapter_order: int) -> str
search_analysis_fragments_tool(work_id: str, query: str, top_k: int) -> str
get_context_tool(work_id: str, chapter_id: str) -> str

# 工具列表
LANGGRAPH_TOOLS: List[StructuredTool]  # 包含 11 个工具（本文件 7 个，编辑类 4 个来自 editor_tools）
（编辑类工具 smart_continue / smart_rewrite / smart_insert / apply_chapter_edit 定义在 `backend/app/services/agent/tools/editor_tools.py`，通过导入汇总进 LANGGRAPH_TOOLS）
```

**特性**:
- 线程安全的全局 AI Service 管理
- UUID 格式验证
- 带重试机制的辅助函数
- 返回格式：写作类工具返回纯文本，编辑类工具返回 JSON 字符串

### 3.2 utils/context_builder.py

**路径**: `backend/app/services/agent/utils/context_builder.py`

**职责**: 上下文构建和压缩

**导出内容**:

```python
def _compress_task_result(
    task_id: int,
    task_description: str,
    task_result: str,
    max_length: int = 2000
) -> str:
    """智能压缩任务结果"""

def _build_summarization_context(
    user_message: str,
    task_results: List[Dict[str, Any]],
    max_context_length: int = 3000
) -> str:
    """构建 Summarization 的压缩上下文"""

def _build_knowledge_system_messages(
    context: Optional[Dict[str, Any]],
    max_docs: int = 3,
    max_snippet_chars: int = 800,
    max_total_chars: int = 2400
) -> List[SystemMessage]:
    """将 knowledge_docs 构造成系统提示"""
```

**特性**:
- 智能识别内容类型（章节、RAG结果等）
- 自动截断超长内容
- 保留关键信息摘要

---

## 4. Bug 修复详情

### 4.1 editor_tools.py @tool 装饰器缺失

**问题描述**:

`editor_tools.py` 中的函数只使用了自定义的 `@register_as_tool` 装饰器，但 `langgraph_agent.py` 中使用 `.ainvoke()` 方法调用这些工具。

```python
# 问题代码 - 只有自定义装饰器
@register_as_tool("smart_rewrite", "editor", "...")
async def smart_rewrite(...) -> Dict[str, Any]:
    return {"success": True, ...}

# 调用方式 - 需要 LangChain 工具
result = await smart_rewrite.ainvoke({...})  # AttributeError!
```

**问题原因**:

- `@register_as_tool` 只是将函数注册到自定义工具注册表
- 普通函数没有 `.ainvoke()` 方法
- `.ainvoke()` 是 LangChain `Runnable` 接口的方法

**修复方案**:

```python
# 修复后 - 添加 @tool 装饰器
from langchain_core.tools import tool
import json

@tool  # 添加 LangChain 装饰器
@register_as_tool("smart_rewrite", "editor", "...")
async def smart_rewrite(...) -> str:  # 返回类型改为 str
    return json.dumps({"success": True, ...}, ensure_ascii=False)
```

**修改的函数** (4个):

| 函数名 | 功能 |
|--------|------|
| `apply_chapter_edit` | 执行章节编辑操作 |
| `smart_continue` | 智能续写 |
| `smart_rewrite` | 智能改写 |
| `smart_insert` | 智能插入 |

**关键变更**:

1. 添加 `from langchain_core.tools import tool` 导入
2. 每个函数添加 `@tool` 装饰器（放在 `@register_as_tool` 之前）
3. 返回类型从 `Dict[str, Any]` 改为 `str`
4. 所有 `return {...}` 改为 `return json.dumps({...}, ensure_ascii=False)`

---

## 5. langgraph_agent.py 变更

### 5.1 新增导入

```python
# 从新模块导入工具
from app.services.agent.langgraph_tools import (
    set_global_ai_service,
    get_global_ai_service,
    validate_uuid,
    _retry_on_failure,
    _generate_text_helper,
    LANGGRAPH_TOOLS,
)

# 从新模块导入上下文构建函数
from app.services.agent.utils.context_builder import (
    _compress_task_result,
    _build_summarization_context,
    _build_knowledge_system_messages,
)
```

### 5.2 删除的代码

删除了约 1089 行代码，包括：
- 全局 AI Service 管理函数
- UUID 验证函数
- 重试包装器函数
- 文本生成辅助函数
- 7 个 @tool 装饰器工具函数
- 3 个上下文构建函数

### 5.3 兼容性处理

```python
# 保持向后兼容
WRITING_TOOLS = LANGGRAPH_TOOLS
```

---

## 6. 验证结果

### 6.1 模块导入测试

```
✅ editor_tools.py - 4 个 StructuredTool
✅ langgraph_tools.py - 11 个工具
✅ context_builder.py - 3 个函数
✅ langgraph_agent.py - WritingAgentGraph, AgentState
```

### 6.2 工具类型验证

```python
# 修复前
type(smart_rewrite)  # <class 'function'>
hasattr(smart_rewrite, 'ainvoke')  # False

# 修复后
type(smart_rewrite)  # <class 'langchain_core.tools.structured.StructuredTool'>
hasattr(smart_rewrite, 'ainvoke')  # True
```

### 6.3 LANGGRAPH_TOOLS 完整列表

```
1. continue_writing_tool (写作)
2. polish_text_tool (写作)
3. analyze_text_tool (写作)
4. get_context_tool (章节)
5. read_chapter_tool (章节)
6. get_chapter_by_order_tool (章节)
7. search_analysis_fragments_tool (检索)
8. smart_continue (编辑器)
9. smart_rewrite (编辑器)
10. smart_insert (编辑器)
11. apply_chapter_edit (编辑器)
```
其中 8-11 由 `backend/app/services/agent/tools/editor_tools.py` 提供，前 7 个定义在本文件。

---

## 7. 文件结构

```
backend/app/services/agent/
|-- langgraph_agent.py          # 主 Agent 文件 (4966行)
|-- langgraph_tools.py          # 工具函数 (712行) [新建]
|-- utils/
|   `-- context_builder.py      # 上下文构建 (211行) [新建]
`-- tools/
    `-- editor_tools.py         # 编辑器工具 (571行) [修复]
```

---

## 8. 后续建议

1. **继续拆分**: `langgraph_agent.py` 仍有约 5000 行，可考虑进一步拆分工作流节点
2. **添加测试**: 为新模块添加单元测试
3. **文档更新**: 更新 API 文档，说明工具使用方式
4. **性能监控**: 监控重构后的性能表现

---

## 9. 回滚方案

如需回滚，执行：

```bash
git checkout HEAD~1 -- backend/app/services/agent/langgraph_agent.py
git checkout HEAD~1 -- backend/app/services/agent/tools/editor_tools.py
rm backend/app/services/agent/langgraph_tools.py
rm backend/app/services/agent/utils/context_builder.py
```

---

**文档结束**
