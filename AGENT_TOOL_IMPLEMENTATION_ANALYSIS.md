# Backend Agent 工具实现深度分析

## 执行摘要

本分析深入探索了后端Agent工具系统的实现,重点关注 `read_chapter_tool` 的完整实现、工具Schema定义和ID来源问题。

**核心发现:**
1. `read_chapter_tool` 是一个 **LangChain @tool 装饰器** 实现的工具
2. **工具Schema** 通过 **@tool装饰器自动生成**,基于函数签名和docstring
3. **ID来源问题**: LLM生成的简化ID(如`ch_1`,`ch_2`)是**因为提示词示例不规范**,而非工具Schema问题
4. **RAG检索** 会返回真实UUID,但RAG结果不直接用于工具参数,而是作为上下文提供

---

## 1. read_chapter_tool 完整实现

文件: `D:\Java\ai_writer\backend\app\services\agent\langgraph_agent.py` (第348-415行)

工具特点:
- **装饰器**: @tool (LangChain原生)
- **参数**: work_id (Optional[str]), chapter_id (str = "")
- **返回**: JSON字符串格式的章节信息
- **异步**: ✅ 完全异步实现
- **错误处理**: ✅ 友好的错误提示

关键功能:
1. 验证work_id和chapter_id
2. 使用ChapterService从数据库查询章节
3. 返回章节标题、内容(5000字符限制)、字数等信息
4. 如果缺少参数,返回JSON错误提示(不抛异常)

---

## 2. 工具Schema定义机制

Schema自动生成来源:
1. **函数签名** → 参数名、参数类型
2. **Docstring** → 工具描述、参数说明

推断的Schema结构:
{
  "name": "read_chapter_tool",
  "description": "读取指定章节工具：从数据库读取章节内容",
  "parameters": {
    "type": "object",
    "properties": {
      "work_id": {
        "type": "string",
        "description": "作品ID（可选，但强烈推荐提供）",
        "nullable": true
      },
      "chapter_id": {
        "type": "string",
        "description": "章节ID",
        "default": ""
      }
    },
    "required": ["chapter_id"]
  }
}

**问题发现**: Schema只标记chapter_id为"string",没有UUID格式约束!

---

## 3. ID来源问题分析 (核心问题)

### 问题现象
LLM生成工具参数时出现简化ID: ch_1, ch_2 而非真实UUID

### 根本原因: 提示词示例

在langgraph_agent.py第2766行:
  "示例：{{\"tool\": \"read_chapter_tool\", \"params\": {{\"chapter_id\": \"abc-123-def\"}}}}"
                                                                          ^^^^^^^^^^^^^^
                                                        这个简化示例导致LLM学习简化格式!

在langgraph_agent.py第1535-1538行:
  用户："帮我获取第3章"
  决策：{{"need_tools": true, "tool_name": "get_chapter_by_order_tool", "tool_args": {{"chapter_order": 3}}}}

### 为什么不用真实UUID?

设计上鼓励使用 get_chapter_by_order_tool (按序号获取) 而不是直接提供UUID:
- 用户通常说"第3章",不说"UUID xxx的章节"
- get_chapter_by_order_tool接收整数chapter_order,更容易生成
- read_chapter_tool是fallback,在已知UUID时才用

### RAG检索中的真实UUID

langgraph_agent.py第663行,RAG返回真实UUID:
  "chapter_id": r['chapter_id'],  // ← 真实的UUID

但这个ID只作为**上下文信息**返回,不直接用于后续工具调用参数!

---

## 4. 工具参数流处理

流程:
1. 用户输入 → AI决策(HTTPAIService)
2. AI决策输出: {need_tools, tool_name, tool_args}
   (可能包含简化ID ← 在这里出现问题)
3. 参数标准化: _normalize_tool_params()
4. 工具执行: read_chapter_tool.ainvoke(params)
5. 返回结果: JSON章节信息

关键工具调用代码(langgraph_agent.py:1642-1656):
```
elif tool_name == "read_chapter_tool":
    work_id_value = state.get("work_id")
    if not work_id_value:
        // 返回友好错误
    else:
        tool_result = await read_chapter_tool.ainvoke({
            "work_id": work_id_value,
            "chapter_id": tool_args.get("chapter_id") or state.get("chapter_id") or ""
        })
```

**Fallback机制**: 如果LLM提供的chapter_id错误,使用state中的当前chapter_id

---

## 5. 工具绑定到LLM

工具列表(langgraph_agent.py:684-693):
WRITING_TOOLS = [
    continue_writing_tool,
    polish_text_tool,
    analyze_text_tool,
    get_context_tool,
    read_chapter_tool,  ← 目标工具
    get_chapter_by_order_tool,
    search_analysis_fragments_tool
]

绑定到LLM(langgraph_agent.py:984):
self.llm_with_tools = self.llm.bind_tools(WRITING_TOOLS)

执行工具(langgraph_agent.py:1023):
workflow.add_node("tools", ToolNode(WRITING_TOOLS))

---

## 6. 关键发现总结

### 工具Schema
- ✅ 通过@tool装饰器自动生成
- ✅ 基于函数签名和docstring
- ❌ 不包含ID格式约束(缺少UUID pattern)
- ❌ 只标记为"string",无格式说明

### ID来源问题
- ❌ **不是** 工具Schema问题(虽然Schema可以改进)
- ❌ **不是** RAG问题(RAG返回真实UUID)
- ✅ **是** 提示词示例格式问题(abc-123-def示例)
- ✅ 设计上优先使用get_chapter_by_order_tool

### 参数处理
- ✅ Fallback机制(state中的current chapter_id)
- ✅ 参数完整性检查(缺少work_id时处理)
- ✅ 参数标准化(_normalize_tool_params)
- ✅ 友好的错误提示

### RAG与工具的关系
- ✅ RAG返回真实UUID
- ✅ 作为**上下文信息**返回
- ✅ **不直接用于**工具参数

---

## 7. 改进建议

### 提示词改进
将示例改为真实UUID格式:
  "示例：{{\"tool\": \"read_chapter_tool\", \"params\": {{\"chapter_id\": \"550e8400-e29b-41d4-a716-446655440000\"}}}}"

### Schema改进
在工具docstring中明确ID格式:
```
Args:
    work_id: 作品ID（UUID格式,可选但推荐）
        格式: xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx
        例如: 550e8400-e29b-41d4-a716-446655440000
    chapter_id: 章节ID（UUID格式,必需）
        格式: xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx
        例如: 550e8400-e29b-41d4-a716-446655440000
```

### 提示词中的工具使用说明改进
明确告诉LLM ID格式:
```
【重要ID格式说明】
- work_id: UUID格式, 例如 550e8400-e29b-41d4-a716-446655440000
- chapter_id: UUID格式, 例如 550e8400-e29b-41d4-a716-446655440000
- 如果不知道章节UUID, 请使用 get_chapter_by_order_tool(按序号获取)
```

---

## 8. 文件位置总结

| 组件 | 文件 | 行号 |
|-----|------|------|
| read_chapter_tool完整实现 | langgraph_agent.py | 348-415 |
| 工具列表(WRITING_TOOLS) | langgraph_agent.py | 684-693 |
| 工具绑定LLM | langgraph_agent.py | 984 |
| ToolNode设置 | langgraph_agent.py | 1023 |
| 工具调用代码 | langgraph_agent.py | 1642-1656 |
| 决策Prompt模板 | langgraph_agent.py | 1495-1547 |
| 任务规划Prompt | langgraph_agent.py | 2756-2790 |
| 参数标准化 | langgraph_agent.py | 3665-3700+ |
| get_context_tool(含RAG) | langgraph_agent.py | 583-680 |

