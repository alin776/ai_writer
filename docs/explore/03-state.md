# Explore 状态管理

## 1. 设计原则

| 原则 | 说明 |
|------|------|
| 精度零丢失 | 所有收集到的内容原样保留，不压缩、不摘要 |
| 去重工具调用 | 避免重复调用相同参数的工具，减少冗余 |
| 内容不去重 | 搜索结果即使重复，也原样保留（可能来自不同视角） |

## 2. 状态结构

```python
from dataclasses import dataclass, field
from typing import Dict, List, Set, Tuple, Any
from datetime import datetime

@dataclass
class Evidence:
    """搜索到的证据片段"""
    text: str                    # 原文片段
    chapter_order: int           # 章节序号
    paragraph_index: int         # 段落索引
    similarity: float            # 相似度
    source_type: str             # 来源类型
    query: str                   # 触发此结果的搜索词
    round_idx: int               # 第几轮搜索到的

@dataclass
class ParagraphRead:
    """读取的段落原文"""
    chapter_order: int
    chapter_title: str
    paragraph_index: int
    text: str                    # 目标段落原文
    context_before: List[str]    # 前文段落
    context_after: List[str]     # 后文段落
    round_idx: int               # 第几轮读取的

@dataclass
class ChapterRead:
    """读取的章节原文"""
    order: int
    title: str
    content: str                 # 完整原文
    word_count: int
    round_idx: int               # 第几轮读取的

@dataclass
class WorldviewItem:
    """世界观条目"""
    id: str
    name: str
    category: str
    description: str
    attributes: Dict[str, Any]

@dataclass
class ExploreState:
    """Explore 内部状态"""

    # ========== 收集到的内容（原样保留，不压缩）==========

    evidences: List[Evidence] = field(default_factory=list)
    # 搜索到的所有证据片段

    paragraphs: List[ParagraphRead] = field(default_factory=list)
    # 精确读取的段落原文

    chapters: Dict[int, ChapterRead] = field(default_factory=dict)
    # 读取的完整章节，key = chapter_order

    worldview: Dict[str, List[WorldviewItem]] = field(default_factory=dict)
    # 世界观条目，key = category

    # ========== 去重记录（仅用于判断是否重复调用）==========

    searched_queries: Set[str] = field(default_factory=set)
    # 已搜索过的 query

    read_paragraph_positions: Set[Tuple[int, int]] = field(default_factory=set)
    # 已读取的段落位置 (chapter_order, paragraph_index)

    read_chapter_orders: Set[int] = field(default_factory=set)
    # 已读取完整原文的章节序号

    read_worldview_categories: Set[str] = field(default_factory=set)
    # 已读取的世界观分类

    # ========== 轮次记录（给前端展示）==========

    rounds: List['ExploreRound'] = field(default_factory=list)
    # 每轮的执行记录

@dataclass
class ToolCall:
    """单次工具调用"""
    tool_name: str
    params: Dict[str, Any]
    result: Any
    duration_ms: int

@dataclass
class ExploreRound:
    """单轮探索记录"""
    round_idx: int
    reasoning: str               # AI 的思考过程
    tool_calls: List[ToolCall]   # 本轮执行的工具
    new_evidences_count: int     # 本轮新增证据数
    new_paragraphs_count: int    # 本轮新增段落数
    sufficient: bool             # AI 判断是否充足
    timestamp: datetime
```

## 3. 去重逻辑

### 3.1 搜索去重

```python
def should_search(self, query: str) -> bool:
    """判断是否应该执行搜索"""
    # 完全相同的 query 跳过
    if query in self.searched_queries:
        return False

    # 可选：语义相似的 query 也跳过（需要额外计算）
    # for existing_query in self.searched_queries:
    #     if semantic_similarity(query, existing_query) > 0.9:
    #         return False

    return True

def record_search(self, query: str):
    """记录已搜索的 query"""
    self.searched_queries.add(query)
```

### 3.2 段落读取去重

```python
def should_read_paragraph(self, chapter_order: int, paragraph_index: int) -> bool:
    """判断是否应该读取段落"""
    position = (chapter_order, paragraph_index)
    return position not in self.read_paragraph_positions

def record_paragraph_read(self, chapter_order: int, paragraph_index: int):
    """记录已读取的段落"""
    self.read_paragraph_positions.add((chapter_order, paragraph_index))
```

### 3.3 章节读取去重

```python
def should_read_chapter(self, chapter_order: int) -> bool:
    """判断是否应该读取章节"""
    return chapter_order not in self.read_chapter_orders

def record_chapter_read(self, chapter_order: int):
    """记录已读取的章节"""
    self.read_chapter_orders.add(chapter_order)
```

### 3.4 世界观读取去重

```python
def should_read_worldview(self, category: str) -> bool:
    """判断是否应该读取世界观分类"""
    return category not in self.read_worldview_categories

def record_worldview_read(self, category: str):
    """记录已读取的世界观分类"""
    self.read_worldview_categories.add(category)
```

## 4. 内容存储逻辑

### 4.1 存储搜索结果

```python
def add_evidence(self, result: SearchResult, query: str, round_idx: int):
    """添加搜索结果（不去重，原样保留）"""
    evidence = Evidence(
        text=result.text,
        chapter_order=result.chapter_order,
        paragraph_index=result.paragraph_index,
        similarity=result.similarity,
        source_type=result.source_type,
        query=query,
        round_idx=round_idx
    )
    self.evidences.append(evidence)
```

### 4.2 存储段落原文

```python
def add_paragraph(self, data: ReadParagraphOutput, round_idx: int):
    """添加段落原文"""
    target_para = next(p for p in data.paragraphs if p.is_target)

    paragraph_read = ParagraphRead(
        chapter_order=data.chapter_order,
        chapter_title=data.chapter_title,
        paragraph_index=target_para.index,
        text=target_para.text,
        context_before=[p.text for p in data.paragraphs if p.index < target_para.index],
        context_after=[p.text for p in data.paragraphs if p.index > target_para.index],
        round_idx=round_idx
    )
    self.paragraphs.append(paragraph_read)
```

### 4.3 存储章节原文

```python
def add_chapter(self, chapter: ChapterContent, round_idx: int):
    """添加章节原文（覆盖式，同一章节只保留一份）"""
    self.chapters[chapter.order] = ChapterRead(
        order=chapter.order,
        title=chapter.title,
        content=chapter.content,
        word_count=chapter.word_count,
        round_idx=round_idx
    )
```

### 4.4 存储世界观

```python
def add_worldview_items(self, items: List[WorldviewItem], category: str):
    """添加世界观条目"""
    if category not in self.worldview:
        self.worldview[category] = []
    self.worldview[category].extend(items)
```

## 5. 收敛检测

```python
def check_convergence(self, window: int = 2) -> bool:
    """
    检测是否收敛（连续 N 轮没有新增信息）

    Args:
        window: 检测窗口大小，默认 2 轮

    Returns:
        True 表示已收敛，应该停止
    """
    if len(self.rounds) < window:
        return False

    recent_rounds = self.rounds[-window:]

    for round in recent_rounds:
        if round.new_evidences_count > 0 or round.new_paragraphs_count > 0:
            return False

    return True
```

## 6. 统计信息

```python
def get_stats(self) -> Dict[str, Any]:
    """获取当前状态统计"""
    return {
        "total_evidences": len(self.evidences),
        "total_paragraphs": len(self.paragraphs),
        "total_chapters": len(self.chapters),
        "total_worldview_items": sum(len(items) for items in self.worldview.values()),
        "searched_queries_count": len(self.searched_queries),
        "rounds_count": len(self.rounds)
    }
```
