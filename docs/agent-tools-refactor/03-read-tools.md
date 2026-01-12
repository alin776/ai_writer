# Read 类工具设计

## 1. 概述

Read 类工具负责**获取完整内容**，进行智能预处理（选择、压缩、格式化），但不进行语义推理。

**设计理念**：类似 `vim / less`，查看完整的、连续的内容。

## 2. 工具列表

| 工具 | 功能 | 场景 |
|------|------|------|
| `get_writing_context` | 获取创作上下文（一站式） | 续写、改写前获取上下文 |

## 3. get_writing_context

### 3.1 功能描述

一站式获取创作所需的完整上下文，合并 4 个原子工具：
- `get_context_tool`
- `read_chapter_tool`
- `get_worldview_summary`
- `get_style_guidance_tool`

### 3.2 变更说明

| 项目 | 变更前 | 变更后 |
|------|--------|--------|
| 工具数量 | 4 个独立工具 | 1 个聚合工具 |
| 调用次数 | 4 次 | 1 次 |
| 参数控制 | 无 | `include` 参数控制返回内容 |

### 3.3 参数定义

```python
@dataclass
class GetWritingContextInput:
    work_id: str                    # 作品ID（必需）
    chapter_id: str = ""            # 章节ID（可选，支持 UUID）
    chapter_orders: str = ""        # 章节序号，支持批量（可选）
                                    # 格式："1" / "1,2,3" / "1-5" / "1,3-5,7"
    user_id: str = ""               # 用户ID（用于获取风格）
    include: List[str] = None       # 包含的内容类型
                                    # 可选值：work, chapter, worldview, style, rag
                                    # 默认：["work", "chapter", "worldview", "style", "rag"]
    rag_query: str = ""             # RAG 检索查询（可选，默认自动生成）
    rag_top_k: int = 5              # RAG 返回数量
    use_cache: bool = True          # 是否使用章节缓存（新增）
```

### 3.4 章节缓存机制（新增）

**问题背景**：
- Planning 阶段读取的章节内容，在 Execution 阶段会再次读取
- 导致重复的数据库查询，增加延迟和资源消耗

**解决方案**：
在 AgentState 中引入章节缓存：

```python
# agent_state.py
@dataclass
class AgentState:
    # ... 现有字段
    chapter_cache: Dict[str, Chapter] = field(default_factory=dict)
    # key: chapter_id 或 f"{work_id}:{chapter_order}"
```

**缓存逻辑**：
```python
async def _get_chapter_with_cache(
    work_id: str,
    chapter_id: str = "",
    chapter_order: int = -1,
    state: AgentState = None,
    use_cache: bool = True
) -> Optional[Chapter]:
    """带缓存的章节获取"""

    # 生成缓存 key
    if chapter_id:
        cache_key = chapter_id
    else:
        cache_key = f"{work_id}:{chapter_order}"

    # 检查缓存
    if use_cache and state and cache_key in state.chapter_cache:
        return state.chapter_cache[cache_key]

    # 从数据库获取
    if chapter_id:
        chapter = await chapter_service.get_chapter_by_id(chapter_id)
    else:
        chapter = await chapter_service.get_chapter_by_order(work_id, chapter_order)

    # 写入缓存
    if chapter and state:
        state.chapter_cache[cache_key] = chapter
        # 同时缓存另一个 key
        if chapter_id:
            state.chapter_cache[f"{work_id}:{chapter.order}"] = chapter
        else:
            state.chapter_cache[str(chapter.id)] = chapter

    return chapter
```

### 3.5 返回格式

```json
{
    "work_info": {
        "id": "xxx",
        "title": "我的小说",
        "description": "一个关于冒险的故事",
        "genre": "玄幻",
        "total_chapters": 10
    },
    "chapters": [
        {
            "id": "xxx",
            "title": "第一章 起源",
            "order": 1,
            "content": "完整章节内容...",
            "word_count": 3500
        }
    ],
    "worldview": {
        "characters": [
            {
                "name": "主角",
                "description": "一个普通少年...",
                "relationships": ["师父", "青梅竹马"]
            }
        ],
        "locations": [
            {
                "name": "青云山",
                "description": "修仙门派所在地..."
            }
        ],
        "settings": [
            {
                "name": "修炼体系",
                "description": "分为练气、筑基、金丹..."
            }
        ]
    },
    "style_guidance": "使用第一人称，句子较长，注重心理描写...",
    "rag_context": [
        {
            "chapter_order": 3,
            "chapter_title": "第三章",
            "content": "相关上下文片段...",
            "relevance": 0.85
        }
    ]
}
```

### 3.6 智能压缩策略

当批量读取多个章节时，根据章节数量动态调整每章的内容限制：

| 章节数量 | 每章字数限制 | 总字数上限 |
|---------|-------------|-----------|
| 1-5 章 | 5000 字/章 | 25,000 字 |
| 6-15 章 | 2000 字/章 | 30,000 字 |
| 16-30 章 | 1000 字/章 | 30,000 字 |
| 31-50 章 | 500 字/章 | 25,000 字 |
| 51+ 章 | 300 字/章 | 动态 |

```python
def _get_content_limit(chapter_count: int) -> int:
    """根据章节数量获取每章内容限制"""
    if chapter_count <= 5:
        return 5000
    elif chapter_count <= 15:
        return 2000
    elif chapter_count <= 30:
        return 1000
    elif chapter_count <= 50:
        return 500
    else:
        return 300
```

### 3.7 实现代码

```python
async def get_writing_context(
    work_id: str,
    chapter_id: str = "",
    chapter_orders: str = "",
    user_id: str = "",
    include: List[str] = None,
    rag_query: str = "",
    rag_top_k: int = 5
) -> str:
    """
    获取创作上下文（一站式）

    Args:
        work_id: 作品ID
        chapter_id: 章节ID（单章节）
        chapter_orders: 章节序号（支持批量："1" / "1,2,3" / "1-5"）
        user_id: 用户ID（用于获取风格指导）
        include: 包含的内容类型
        rag_query: RAG 检索查询
        rag_top_k: RAG 返回数量

    Returns:
        JSON 格式的创作上下文
    """
    if include is None:
        include = ["work", "chapter", "worldview", "style", "rag"]

    result = {}

    # 1. 获取作品信息
    if "work" in include:
        work = await work_service.get_work_by_id(work_id)
        result["work_info"] = {
            "id": str(work.id),
            "title": work.title,
            "description": work.description,
            "genre": work.genre,
            "total_chapters": len(work.chapters)
        }

    # 2. 获取章节内容
    if "chapter" in include:
        chapters = await _get_chapters(work_id, chapter_id, chapter_orders)
        content_limit = _get_content_limit(len(chapters))

        result["chapters"] = []
        for chapter in chapters:
            content = chapter.content
            if len(content) > content_limit:
                content = content[:content_limit] + f"\n\n[内容已截断，完整内容共 {len(chapter.content)} 字]"

            result["chapters"].append({
                "id": str(chapter.id),
                "title": chapter.title,
                "order": chapter.order,
                "content": content,
                "word_count": chapter.word_count
            })

    # 3. 获取世界观
    if "worldview" in include:
        result["worldview"] = {
            "characters": await worldview_service.get_characters_by_work(work_id),
            "locations": await worldview_service.get_locations_by_work(work_id),
            "settings": await worldview_service.get_settings_by_work(work_id)
        }

    # 4. 获取风格指导
    if "style" in include and user_id:
        result["style_guidance"] = get_style_prompt(user_id)

    # 5. RAG 检索
    if "rag" in include:
        # 确定当前章节序号
        current_order = None
        if result.get("chapters"):
            current_order = result["chapters"][-1]["order"]

        # 自动生成查询（如果未指定）
        if not rag_query:
            rag_query = "作品背景、人物关系、情节发展"

        rag_results = await chapter_vector_service.retrieve_for_writing(
            work_id=work_id,
            current_chapter_order=current_order,
            query=rag_query,
            top_k=rag_top_k
        )

        result["rag_context"] = [
            {
                "chapter_order": r["chapter_order"],
                "chapter_title": r.get("chapter_title", ""),
                "content": r["content"],
                "relevance": round(r["similarity"], 2)
            }
            for r in rag_results
        ]

    return json.dumps(result, ensure_ascii=False)


async def _get_chapters(
    work_id: str,
    chapter_id: str,
    chapter_orders: str
) -> List[Chapter]:
    """
    获取章节列表

    支持三种方式：
    1. chapter_id: 单个章节 UUID
    2. chapter_orders: "1" / "1,2,3" / "1-5"
    3. 都为空: 返回空列表
    """
    chapters = []

    if chapter_id:
        # 单个章节 UUID
        chapter = await chapter_service.get_chapter_by_id(chapter_id)
        if chapter:
            chapters.append(chapter)

    elif chapter_orders:
        # 解析章节序号
        orders = _parse_chapter_orders(chapter_orders)
        for order in orders:
            chapter = await chapter_service.get_chapter_by_order(work_id, order)
            if chapter:
                chapters.append(chapter)

    return chapters


def _parse_chapter_orders(chapter_orders: str) -> List[int]:
    """
    解析章节序号

    支持格式：
    - "1" -> [1]
    - "1,2,3" -> [1, 2, 3]
    - "1-5" -> [1, 2, 3, 4, 5]
    - "1,3-5,7" -> [1, 3, 4, 5, 7]
    """
    orders = []
    parts = chapter_orders.split(",")

    for part in parts:
        part = part.strip()
        if "-" in part:
            # 范围格式
            start, end = part.split("-")
            orders.extend(range(int(start), int(end) + 1))
        else:
            # 单个数字
            orders.append(int(part))

    return sorted(set(orders))
```

### 3.8 使用场景

#### 场景 1：续写前获取上下文

```
用户：继续写第五章
Agent：
  1. 调用 get_writing_context(
       work_id="xxx",
       chapter_orders="5",
       include=["work", "chapter", "worldview", "rag"]
     )
  2. 返回：完整上下文
  3. 调用 smart_continue(...)
```

#### 场景 2：批量阅读多章

```
用户：给我看第1到第5章
Agent：
  1. 调用 get_writing_context(
       work_id="xxx",
       chapter_orders="1-5",
       include=["chapter"]
     )
  2. 返回：5 章内容（每章最多 5000 字）
```

#### 场景 3：只获取世界观

```
用户：这个作品有哪些角色？
Agent：
  1. 调用 get_writing_context(
       work_id="xxx",
       include=["worldview"]
     )
  2. 返回：角色、地点、设定列表
```

---

## 4. 删除的工具

| 工具 | 删除原因 | 功能去向 |
|------|---------|---------|
| `get_context_tool` | 合并 | `get_writing_context` 的 `include=["work", "rag"]` |
| `read_chapter_tool` | 合并 | `get_writing_context` 的 `include=["chapter"]` |
| `get_chapter_by_order_tool` | 合并 | `get_writing_context` 的 `chapter_orders` 参数 |
| `get_worldview_summary` | 合并 | `get_writing_context` 的 `include=["worldview"]` |
| `get_style_guidance_tool` | 合并 | `get_writing_context` 的 `include=["style"]` |

---

## 5. 与其他类工具的关系

### 5.1 Search → Read 链路

```
search_content(query="主角戒指")
   ↓ 返回：[{chapter_order: 2, snippet: "..."}]
   ↓
Agent 判断需要看第2章完整内容
   ↓
get_writing_context(chapter_orders="2", include=["chapter"])
   ↓ 返回：第2章完整内容
```

### 5.2 Read → Update 链路

```
get_writing_context(chapter_orders="5", include=["chapter", "worldview", "rag"])
   ↓ 返回：完整上下文
   ↓
smart_continue(chapter_id="xxx", chapter_content="...", user_requirement="...")
   ↓ 返回：续写内容
```

---

## 6. 迁移计划

### 6.1 代码变更

| 文件 | 变更 |
|------|------|
| `langgraph_tools.py` | 新增 `get_writing_context` 函数 |
| `langgraph_tools.py` | 标记旧工具为 deprecated |
| `tool_executor.py` | 添加别名映射 |
| `planning_examples.py` | 更新工具描述 |

### 6.2 向后兼容

```python
# tool_executor.py
TOOL_NAME_MAPPING = {
    # ... 现有映射
    "get_context_tool": "get_writing_context",
    "get_context": "get_writing_context",
    "read_chapter_tool": "get_writing_context",
    "read_chapter": "get_writing_context",
    "get_chapter_by_order_tool": "get_writing_context",
    "get_chapter_by_order": "get_writing_context",
    "get_worldview_summary": "get_writing_context",
    "get_style_guidance_tool": "get_writing_context",
    "get_style_guidance": "get_writing_context",
}
```

### 6.3 参数转换

当使用旧工具名调用时，自动转换参数：

```python
def _convert_legacy_params(tool_name: str, params: dict) -> dict:
    """将旧工具参数转换为 get_writing_context 参数"""

    if tool_name in ["read_chapter_tool", "read_chapter"]:
        return {
            "work_id": params.get("work_id", ""),
            "chapter_id": params.get("chapter_id", ""),
            "include": ["chapter"]
        }

    if tool_name in ["get_chapter_by_order_tool", "get_chapter_by_order"]:
        return {
            "work_id": params.get("work_id", ""),
            "chapter_orders": params.get("chapter_order", ""),
            "include": ["chapter"]
        }

    if tool_name == "get_worldview_summary":
        return {
            "work_id": params.get("work_id", ""),
            "include": ["worldview"]
        }

    if tool_name in ["get_style_guidance_tool", "get_style_guidance"]:
        return {
            "work_id": params.get("work_id", ""),
            "user_id": params.get("user_id", ""),
            "include": ["style"]
        }

    return params
```
