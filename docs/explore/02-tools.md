# Explore 工具接口

## 1. 工具总览

Explore 内部**复用现有工具**，只新增 `read_paragraph`。

| 工具 | 来源 | 用途 |
|------|------|------|
| `search_content` | **复用现有** | 语义搜索，返回片段 + 位置 |
| `get_writing_context` | **复用现有** | 一次性获取 chapter + worldview + rag |
| `locate_content` | **复用现有** | 定位段落位置 |
| `read_paragraph` | **新增** | 精确读取段落 + 上下文原文 |

## 2. 复用的现有工具

### 2.1 search_content（现有）

**文件位置**：`langgraph_tools.py:796`

**已有功能**：
- 混合检索（向量 + 全文）
- 返回片段 + 位置信息（chapter_order, paragraph_index）
- 支持 top_k、时序窗口

**返回格式**：
```json
{
    "results": [
        {
            "chapter_order": 3,
            "chapter_title": "第三章",
            "paragraph_index": 18,
            "snippet": "段融突破至炼体三层...",
            "similarity": 0.92
        }
    ],
    "total_results": 5
}
```

**Explore 中的使用**：
```python
# 调用现有工具
result = await search_content.ainvoke({
    "work_id": work_id,
    "query": "段融修炼进度",
    "top_k": 10
})
```

---

### 2.2 get_writing_context（现有）

**文件位置**：`langgraph_tools.py:945`

**已有功能**：
- 一次性获取 chapter + worldview + rag
- 智能内容截断（控制总量）
- 支持章节序号解析（"1-5", "-3"）

**返回格式**：
```json
{
    "work_id": "...",
    "chapters": [
        {"order": 1, "title": "...", "content": "完整原文...", "word_count": 2500}
    ],
    "worldview": {
        "characters": [...],
        "locations": [...],
        "settings": [...]
    },
    "rag_context": [
        {"chapter_order": 1, "content": "相关片段...", "relevance": 0.92}
    ]
}
```

**Explore 中的使用**：
```python
# 首轮调用，获取基础信息
result = await get_writing_context.ainvoke({
    "work_id": work_id,
    "chapter_orders": "-3",  # 最近3章
    "include": "chapter,worldview"
})
```

---

### 2.3 locate_content（现有）

**文件位置**：`tools/locate_tools.py:465`

**已有功能**：
- 定位章节中的内容位置
- 返回 before_anchor, after_anchor, node_id, paragraph_index
- 支持语义查询（"主角出场的地方"）

**返回格式**：
```json
{
    "success": true,
    "chapter_id": "...",
    "paragraph_index": 5,
    "before_anchor": "前文内容...",
    "after_anchor": "后文内容...",
    "node_id": "node-uuid",
    "matched_text": "匹配的文本..."
}
```

**Explore 中的使用**：
```python
# 定位后，用 read_paragraph 获取完整原文
locate_result = await locate_content.ainvoke({
    "chapter_id": chapter_id,
    "query": "段融突破的描写"
})
```

---

## 3. 新增工具：read_paragraph

### 3.1 为什么需要这个工具？

| 现有工具 | 局限性 |
|----------|--------|
| `search_content` | 返回截断片段（max_content_length=200），丢失上下文 |
| `get_chapter_by_order` | 读取整章，信息过多 |
| `locate_content` | 只返回位置，不返回完整原文 |

**需求**：根据位置信息，读取指定段落 + 前后上下文的完整原文。

### 3.2 工具定义

```python
@tool
async def read_paragraph(
    work_id: str,
    chapter_order: int,
    paragraph_index: int,
    context_before: int = 2,
    context_after: int = 2
) -> str:
    """
    精确读取段落原文 + 上下文

    Args:
        work_id: 作品ID（UUID格式）
        chapter_order: 章节序号（1-based）
        paragraph_index: 段落索引（0-based）
        context_before: 向前读取段落数（默认2）
        context_after: 向后读取段落数（默认2）

    Returns:
        JSON 格式的段落原文
    """
```

### 3.3 返回格式

```json
{
    "success": true,
    "work_id": "627feba4-2097-4f28-a3f3-7641d10f7f40",
    "chapter_order": 5,
    "chapter_title": "太一门",
    "paragraphs": [
        {
            "index": 23,
            "text": "段融盘膝而坐，体内灵力缓缓流转...",
            "is_target": false
        },
        {
            "index": 24,
            "text": "经过数日苦修，他感觉到丹田中有了微妙变化...",
            "is_target": false
        },
        {
            "index": 25,
            "text": "炼体三层巅峰，距离四层只差一步之遥。段融睁开双眼，眼中闪过一丝精光。",
            "is_target": true
        },
        {
            "index": 26,
            "text": "\"再有三五日，应该就能突破了。\"他暗自思忖...",
            "is_target": false
        },
        {
            "index": 27,
            "text": "正在此时，门外传来一阵脚步声...",
            "is_target": false
        }
    ],
    "total_paragraphs_in_chapter": 32
}
```

### 3.4 实现逻辑

**关键发现**：
1. 复用现有 `locate_tools.py:_split_paragraphs()` 函数
2. 使用 `WorkService.get_work_by_id()` 获取章节（非 ChapterRepository）

```python
from app.services.agent.tools.locate_tools import _split_paragraphs
from app.services.work_service import WorkService
from app.database.session import AsyncSessionLocal

@tool
async def read_paragraph(
    work_id: str,
    chapter_order: int,
    paragraph_index: int,
    context_before: int = 2,
    context_after: int = 2
) -> str:
    """精确读取段落原文 + 上下文"""

    # 大章节保护
    MAX_CHAPTER_SIZE = 200_000  # 200K 字符

    # 1. 获取章节内容（使用 WorkService，与现有代码一致）
    async with AsyncSessionLocal() as db:
        work_service = WorkService(db)
        work = await work_service.get_work_by_id(work_id, use_cache=True)

        if not work:
            return json.dumps({
                "success": False,
                "error": f"作品 {work_id} 不存在"
            }, ensure_ascii=False)

        if not work.chapters:
            return json.dumps({
                "success": False,
                "error": "作品没有章节"
            }, ensure_ascii=False)

        # 按序号查找章节（与 get_writing_context 一致）
        chapter_map = {ch.order: ch for ch in work.chapters}
        chapter = chapter_map.get(chapter_order)

        if not chapter:
            return json.dumps({
                "success": False,
                "error": f"章节 {chapter_order} 不存在"
            }, ensure_ascii=False)

    content = chapter.content or ""

    # 2. 大章节分块处理
    if len(content) > MAX_CHAPTER_SIZE:
        # 估算目标位置，只解析附近 10K 字符
        avg_para_len = 500
        start_pos = max(0, paragraph_index * avg_para_len - 5000)
        end_pos = min(len(content), paragraph_index * avg_para_len + 5000)
        content = content[start_pos:end_pos]
        # 调整索引
        paragraph_index = min(paragraph_index, 10)

    # 3. 复用现有段落解析（支持 HTML 和纯文本）
    paragraphs = _split_paragraphs(content)

    if paragraph_index >= len(paragraphs):
        return json.dumps({
            "success": False,
            "error": f"段落索引 {paragraph_index} 超出范围（共 {len(paragraphs)} 段）"
        }, ensure_ascii=False)

    # 4. 计算范围
    start_idx = max(0, paragraph_index - context_before)
    end_idx = min(len(paragraphs), paragraph_index + context_after + 1)

    # 5. 构建结果
    result_paragraphs = []
    for i in range(start_idx, end_idx):
        result_paragraphs.append({
            "index": i,
            "text": paragraphs[i]["text"],
            "is_target": i == paragraph_index
        })

    return json.dumps({
        "success": True,
        "work_id": work_id,
        "chapter_order": chapter_order,
        "chapter_title": chapter.title,
        "paragraphs": result_paragraphs,
        "total_paragraphs_in_chapter": len(paragraphs)
    }, ensure_ascii=False)
```

### 3.5 复用的现有函数

```python
# locate_tools.py:39-78（现有代码，无需修改）
def _split_paragraphs(content: str) -> List[Dict[str, Any]]:
    """
    智能段落分割

    支持：
    - HTML 块级元素（<p>, <h1-6>, <blockquote> 等）
    - 纯文本模式（\n\n 或 \n 分割）

    返回：[{index, text, preview}]
    """
    # ... 现有实现 ...
```

---

## 4. 工具调用规则

### 4.1 AI 自主选择

AI 根据当前信息缺口决定调用哪些工具：

```
信息需求                         → 推荐工具
───────────────────────────────────────────────
不知道信息在哪                   → search_content
需要完整章节 + 世界观            → get_writing_context
知道位置，需要验证原文           → read_paragraph
需要精确定位                     → locate_content
```

### 4.2 典型调用序列

```
Round 1:
  - get_writing_context(chapter_orders="-3", include="chapter,worldview")
  - search_content(query="段融性格")

Round 2:
  - read_paragraph(chapter_order=3, paragraph_index=18)  # 验证搜索结果
  - search_content(query="段融 同门关系")

Round 3:
  AI 判断信息充足，退出
```

### 4.3 并行执行

同一轮内，多个工具调用可以并行：

```python
results = await asyncio.gather(
    search_content.ainvoke({"work_id": work_id, "query": "段融性格"}),
    search_content.ainvoke({"work_id": work_id, "query": "段融修炼"}),
    get_writing_context.ainvoke({"work_id": work_id, "include": "worldview"})
)
```
