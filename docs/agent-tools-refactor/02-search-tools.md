# Search 类工具设计

## 1. 概述

Search 类工具负责**定位内容位置**，返回位置信息和内容片段（snippet），不返回完整内容。

**设计理念**：类似 `grep / ripgrep`，快速定位"哪里可能有相关内容"。

## 2. 工具列表

| 工具 | 功能 | 场景 |
|------|------|------|
| `search_content` | 搜索多个相关位置 | "找一下关于XX的内容" |
| `locate_content` | 定位单个位置 | "把第三段改了" |

## 3. search_content

### 3.1 功能描述

搜索作品中与查询相关的多个位置，基于混合检索（向量 + 全文）。

### 3.2 变更说明

| 项目 | 变更前 | 变更后 |
|------|--------|--------|
| 工具名 | `search_analysis_fragments_tool` | `search_content` |
| 返回内容 | 完整 content | 片段 snippet（200字） |

### 3.3 参数定义

```python
@dataclass
class SearchContentInput:
    work_id: str           # 作品ID（必需）
    query: str             # 查询文本（必需）
    top_k: int = 10        # 返回前K个结果
    chapter_id: str = ""   # 当前章节ID（可选，用于时序窗口）
    look_ahead: int = 0    # 允许向后看的章节数（0=不限制）
```

### 3.4 返回格式

```json
{
    "work_id": "xxx",
    "query": "主角戒指",
    "total_results": 2,
    "results": [
        {
            "rank": 1,
            "chapter_id": "xxx",
            "chapter_order": 2,
            "chapter_title": "第二章 初遇",
            "paragraph_index": 3,
            "snippet": "主角拿起戒指，感受到一股温热...",
            "similarity": 0.85,
            "source": "hybrid"
        },
        {
            "rank": 2,
            "chapter_id": "yyy",
            "chapter_order": 5,
            "chapter_title": "第五章 觉醒",
            "paragraph_index": 7,
            "snippet": "那枚戒指闪烁着奇异的光芒...",
            "similarity": 0.72,
            "source": "vector"
        }
    ]
}
```

### 3.5 实现代码

```python
async def search_content(
    work_id: str,
    query: str,
    top_k: int = 10,
    chapter_id: str = "",
    look_ahead: int = 0
) -> str:
    """
    搜索多个相关位置（返回位置 + 片段）

    Args:
        work_id: 作品ID
        query: 查询文本
        top_k: 返回前K个结果
        chapter_id: 当前章节ID（用于时序窗口控制）
        look_ahead: 允许向后看的章节数（0=不限制）

    Returns:
        JSON 格式的搜索结果
    """
    # 获取当前章节序号（用于时序窗口）
    current_order = None
    if chapter_id:
        chapter = await chapter_service.get_chapter_by_id(chapter_id)
        current_order = chapter.order if chapter else None

    # 混合检索
    retriever = HybridRetriever(db)
    results = await retriever.search(
        work_id=work_id,
        query=query,
        top_k=top_k,
        current_order=current_order,
        look_ahead=look_ahead
    )

    # 格式化返回（只返回片段）
    formatted_results = []
    for i, r in enumerate(results):
        formatted_results.append({
            "rank": i + 1,
            "chapter_id": r["chapter_id"],
            "chapter_order": r["chapter_order"],
            "chapter_title": r.get("chapter_title", ""),
            "paragraph_index": r["paragraph_index"],
            "snippet": r["content"][:200] + "..." if len(r["content"]) > 200 else r["content"],
            "similarity": round(r["similarity"], 2),
            "source": r.get("source", "hybrid")
        })

    return json.dumps({
        "work_id": work_id,
        "query": query,
        "total_results": len(formatted_results),
        "results": formatted_results
    }, ensure_ascii=False)
```

### 3.6 使用场景

```
用户：找一下主角第一次使用魔法的地方
Agent：调用 search_content(query="主角第一次使用魔法")
返回：[{chapter_order: 3, paragraph_index: 5, snippet: "主角举起手，一道火焰..."}]
```

---

## 4. locate_content

### 4.1 功能描述

精确定位章节中的单个位置，支持多种定位策略。

### 4.2 变更说明

**无变更**，保持现有实现。

### 4.3 参数定义

```python
@dataclass
class LocateContentInput:
    chapter_id: str        # 章节ID（必需）
    query: str             # 定位描述（必需）
    chapter_content: str = ""  # 章节内容（可选，避免重复查询）
```

### 4.4 定位策略（按优先级）

| 优先级 | 策略 | 触发条件 | 示例 |
|--------|------|---------|------|
| 1 | node_id 结构化定位 | query 包含 node_id | `node_id:abc123` |
| 2 | 段落索引定位 | query 匹配"第N段" | `第3段` |
| 3 | 特殊位置 | query 匹配"开头/结尾" | `开头`、`结尾` |
| 4 | 精确文本匹配 | query 是原文片段 | `主角缓缓走进大厅` |
| 5 | 模糊匹配 | 相似度 >= 0.7 | `主角走进大厅的那段` |
| 6 | LLM 辅助定位 | 模糊匹配置信度 < 0.7 | `主角出场的地方` |
| 7 | 全局降级 | 章节内定位失败 | 在整个作品中搜索 |
| 8 | 返回段落列表 | 全局降级失败 | 让用户选择 |

### 4.5 返回格式

```json
{
    "success": true,
    "locate_method": "fuzzy_match",
    "paragraph_index": 5,
    "text_preview": "主角缓缓走进大厅，四周的目光...",
    "text": "完整段落文本...",
    "node_id": "abc123",
    "before_anchor": "上一段的最后几个字",
    "after_anchor": "下一段的开头几个字",
    "confidence": 0.85
}
```

### 4.6 LLM 辅助定位

当模糊匹配置信度 < 0.7 时，调用 LLM 辅助定位：

```python
async def _llm_assisted_locate(
    query: str,
    candidates: List[Dict],
    chapter_content: str
) -> Dict:
    """
    LLM 辅助定位

    Args:
        query: 用户的定位描述
        candidates: 候选段落列表（按相似度排序）
        chapter_content: 章节完整内容

    Returns:
        定位结果
    """
    # 构建 prompt
    prompt = f"""
    用户想要定位的内容：{query}

    候选段落：
    {format_candidates(candidates)}

    请选择最符合用户意图的段落编号（1-{len(candidates)}），只返回数字。
    """

    # 调用轻量模型
    result = await ai_service.generate(
        prompt=prompt,
        task_type=TaskType.SIMPLE_QA  # 使用 gemini-2.5-flash-lite
    )

    selected_index = int(result.strip()) - 1
    return candidates[selected_index]
```

### 4.7 使用场景

```
用户：把第三段改成更生动的描述
Agent：
  1. 调用 locate_content(query="第三段")
  2. 返回：{paragraph_index: 2, text: "原文内容..."}
  3. 调用 smart_rewrite(text_to_rewrite="原文内容...", user_requirement="更生动的描述")
```

---

## 5. 与其他类工具的关系

### 5.1 Search → Read 链路

```
search_content(query="主角戒指")
   ↓ 返回多个位置
   ↓
Agent 判断需要看第2章完整内容
   ↓
get_writing_context(chapter_id="xxx")
   ↓ 返回完整上下文
```

### 5.2 Search → Update 链路

```
locate_content(query="第三段")
   ↓ 返回单个位置
   ↓
smart_rewrite(text_to_rewrite="...", user_requirement="...")
   ↓ 返回改写结果
```

---

## 6. 迁移计划

### 6.1 代码变更

| 文件 | 变更 |
|------|------|
| `langgraph_tools.py` | 重命名函数 `search_analysis_fragments_tool` → `search_content` |
| `langgraph_tools.py` | 修改返回格式，只返回 snippet |
| `tool_executor.py` | 添加别名映射 `search_analysis_fragments_tool` → `search_content` |
| `planning_examples.py` | 更新工具描述 |

### 6.2 向后兼容

```python
# tool_executor.py
TOOL_NAME_MAPPING = {
    # ... 现有映射
    "search_analysis_fragments_tool": "search_content",
    "search_analysis_fragments": "search_content",
}
```
