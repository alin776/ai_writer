# Agent 工具重构方案

## 背景

当前 Agent 有 21 个工具，存在以下问题：
1. 工具重复（如 `read_chapter_tool` 和 `get_chapter_by_order_tool`）
2. 职责不清（Search 工具返回完整内容，越界了）
3. Read 工具过多，调用链路冗长（续写需要调用 3-4 个工具）

---

## Search 和 Read 的关系

> **Search 和 Read 是「弱依赖的探索式关系」**

### Search = 索引/线索生成器

- 快速定位"哪里可能有相关内容"
- 返回：位置 + **片段(snippet)**
- 不保证上下文完整
- 成本低、速度快
- 类比：`grep / ripgrep`

### Read = 上下文获取器

- 真正"读代码/文本本身"
- 返回：**完整上下文**
- 能看到连续的、完整的内容
- 成本高、但信息完整
- 类比：`vim / less`

### 关系

```
Search（定位）
   ↓ 返回：位置 + 片段（snippet）
   ↓
（模型推理/判断）
   ↓
Read（获取上下文）
   ↓ 返回：完整上下文
```

**"grep 常常用来决定我 vim 打开哪个文件"**

---

## 重构目标

按 **Search / Read / Update** 三大类重新设计，精简到 15 个工具。

---

## 四个核心工具设计

### 1. search_content（搜索多个位置）

**为什么需要：**
- 修改伏笔时，需要找到所有相关位置（牵一发动全身）
- 用户说"找一下关于XX的内容"

**返回：**
```json
{
    "results": [
        {"chapter_id": "xxx", "chapter_order": 2, "paragraph_index": 3, "snippet": "主角拿起戒指..."},
        {"chapter_id": "yyy", "chapter_order": 5, "paragraph_index": 7, "snippet": "那枚戒指闪烁..."}
    ],
    "total": 2
}
```

**实现：**
```python
async def search_content(
    work_id: str,
    query: str,
    top_k: int = 10
) -> str:
    """
    搜索多个相关位置（返回位置 + 片段）
    基于 HybridRetriever（向量 + 全文检索）
    """
    retriever = HybridRetriever(db)
    results = await retriever.search(work_id=work_id, query=query, top_k=top_k)

    return [{
        "chapter_id": r["chapter_id"],
        "chapter_order": r["chapter_order"],
        "paragraph_index": r["paragraph_index"],
        "snippet": r["content"][:200]  # 只返回片段，不是完整内容
    } for r in results]
```

**与现有工具的关系：**
- 重命名 `search_analysis_fragments_tool` → `search_content`
- 简化返回内容，只返回片段

---

### 2. locate_content（定位单个位置）

**为什么需要：**
- 用户说"把第三段改了"
- 精确定位单个位置

**返回：**
```json
{
    "chapter_id": "xxx",
    "paragraph_index": 3,
    "snippet": "主角缓缓走进大厅...",
    "node_id": "abc123",
    "confidence": 0.95
}
```

**实现：**
- 保持现有 `locate_content` 的 7 种定位策略
- 返回位置 + 片段（不是完整段落）

**与现有工具的关系：**
- 保持现有实现，无需修改

---

### 3. get_writing_context（获取完整上下文）

**为什么需要：**
- 续写前需要完整上下文
- 合并 4 个原子工具，减少调用次数

**返回：**
```json
{
    "work_info": {"title": "...", "description": "...", "genre": "..."},
    "chapter": {"id": "...", "title": "...", "content": "完整内容..."},
    "worldview": {
        "characters": [...],
        "locations": [...],
        "settings": [...]
    },
    "style_guidance": "使用第一人称，句子较长...",
    "rag_context": [...]
}
```

**实现：**
```python
async def get_writing_context(
    work_id: str,
    chapter_id: str = "",
    user_id: str = "",
    include: List[str] = ["work", "chapter", "worldview", "style", "rag"]
) -> str:
    """
    获取创作上下文（一站式）
    合并：get_context + read_chapter + get_worldview_summary + get_style_guidance
    """
    result = {}

    if "work" in include:
        work = await work_service.get_work_by_id(work_id)
        result["work_info"] = {
            "title": work.title,
            "description": work.description,
            "genre": work.genre,
            "total_chapters": len(work.chapters)
        }

    if "chapter" in include and chapter_id:
        chapter = await chapter_service.get_chapter_by_id(chapter_id)
        result["chapter"] = {
            "id": str(chapter.id),
            "title": chapter.title,
            "order": chapter.order,
            "content": chapter.content,  # 完整内容
            "word_count": chapter.word_count
        }

    if "worldview" in include:
        result["worldview"] = {
            "characters": await worldview_service.get_characters_by_work(work_id),
            "locations": await worldview_service.get_locations_by_work(work_id),
            "settings": await worldview_service.get_settings_by_work(work_id)
        }

    if "style" in include and user_id:
        result["style_guidance"] = get_style_prompt(user_id)

    if "rag" in include:
        result["rag_context"] = await chapter_vector_service.retrieve_for_writing(
            work_id=work_id,
            current_chapter_order=chapter.order if chapter else None,
            query="作品背景、人物关系、情节发展",
            top_k=5
        )

    return json.dumps(result, ensure_ascii=False)
```

**与现有工具的关系：**
- 新建聚合工具
- 删除 4 个原子工具：`get_context_tool`, `read_chapter_tool`, `get_worldview_summary`, `get_style_guidance_tool`

**优化效果：**
```
Before: get_context → read_chapter → get_worldview → get_style → smart_continue
After:  get_writing_context → smart_continue
```

---

### 4. analyze_content（分析内容）

**为什么需要：**
- 创作后需要分析质量
- 合并 3 个分析工具

**返回：**
```json
{
    "text_analysis": {
        "issues": ["第3段有语病", "第5段逻辑不通"],
        "suggestions": [...]
    },
    "style_features": {
        "avg_sentence_length": 25,
        "pov": "first_person",
        "dialogue_ratio": 0.3
    },
    "consistency_report": {
        "score": 85,
        "inconsistencies": [...]
    }
}
```

**实现：**
```python
async def analyze_content(
    text: str,
    work_id: str = "",
    analysis_types: List[str] = ["text", "style", "consistency"]
) -> str:
    """
    分析内容质量（一站式）
    合并：analyze_text + analyze_style + check_story_consistency
    """
    result = {}

    if "text" in analysis_types:
        result["text_analysis"] = await _analyze_text_with_llm(text)

    if "style" in analysis_types:
        features = analyze_writing_style(text)
        result["style_features"] = {
            "avg_sentence_length": features.avg_sentence_length,
            "pov": features.pov,
            "dialogue_ratio": features.dialogue_ratio
        }

    if "consistency" in analysis_types and work_id:
        report = await check_story_consistency(work_id, ...)
        result["consistency_report"] = {
            "score": report.consistency_score,
            "inconsistencies": report.inconsistencies
        }

    return json.dumps(result, ensure_ascii=False)
```

**与现有工具的关系：**
- 新建聚合工具
- 删除 3 个原子工具：`analyze_text_tool`, `analyze_style_tool`, `check_story_consistency_tool`

---

## 工具分类总览

### Search（搜索/定位）- 2 个

| 工具 | 功能 | 返回 |
|------|------|------|
| `search_content` | 搜索多个相关位置 | 位置 + 片段（多个） |
| `locate_content` | 定位单个位置 | 位置 + 片段（单个） |

### Read（读取/分析）- 2 个

| 工具 | 功能 | 返回 |
|------|------|------|
| `get_writing_context` | 获取创作上下文 | 完整上下文 |
| `analyze_content` | 分析内容质量 | 分析报告 |

### Update（创建/修改/删除）- 11 个

| 工具 | 功能 | 类型 |
|------|------|------|
| `smart_continue` | 智能续写 | 创作 |
| `smart_rewrite` | 智能重写 | 创作 |
| `smart_insert` | 智能插入 | 创作 |
| `show_emotion_tool` | 展示情感 | 增强 |
| `enhance_scene_tool` | 增强场景 | 增强 |
| `learn_style_tool` | 学习风格 | 增强 |
| `apply_chapter_edit` | 应用编辑 | 操作 |
| `create_chapter` | 创建章节 | 操作 |
| `update_chapter_title` | 更新标题 | 操作 |
| `update_chapter_content` | 更新内容 | 操作 |
| `delete_chapter` | 删除章节 | 操作 |

---

## 删除的工具

| 工具 | 删除原因 |
|------|----------|
| `get_chapter_by_order_tool` | 与 `read_chapter_tool` 重复 |
| `search_analysis_fragments_tool` | 重命名为 `search_content` |
| `get_context_tool` | 合并到 `get_writing_context` |
| `read_chapter_tool` | 合并到 `get_writing_context` |
| `get_worldview_summary` | 合并到 `get_writing_context` |
| `get_style_guidance_tool` | 合并到 `get_writing_context` |
| `analyze_text_tool` | 合并到 `analyze_content` |
| `analyze_style_tool` | 合并到 `analyze_content` |
| `check_story_consistency_tool` | 合并到 `analyze_content` |

---

## 实现步骤

1. 创建 `get_writing_context` 聚合工具
2. 创建 `analyze_content` 聚合工具
3. 重命名 `search_analysis_fragments_tool` 为 `search_content`
4. 删除冗余的原子工具
5. 更新 `LANGGRAPH_TOOLS` 列表
6. 更新工具描述文档

---

## 设计原则

1. **Search 返回片段，Read 返回完整上下文**
2. **参数控制返回内容**，而不是创建多个工具
3. **减少工具数量**，降低 Agent 决策负担
4. **一站式调用**，常见场景一次搞定

---

## 效果

| 指标 | Before | After |
|------|--------|-------|
| 工具总数 | 21 | 15 |
| 续写调用次数 | 4-5 次 | 2 次 |
| Agent 决策复杂度 | 高 | 低 |
