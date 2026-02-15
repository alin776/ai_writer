# Explore 流式事件

> ✅ **实现状态（2026-01-17 更新）**
>
> `explore_round` 和 `explore_summary` 事件方法**已在 flow_events.py 中实现**。
>
> **已实现**：
> - `FlowEventBuilder.explore_round()` - 构建单轮探索事件
> - `FlowEventBuilder.explore_summary()` - 构建 AI 分析与规划事件
> - `EXPLORE_TAG_ICONS` - 工具标签类型图标映射

## 1. 设计原则

**融入现有体系**：复用 `FlowEventBuilder` 的事件格式，只新增必要的 Explore 专用事件。

## 2. 复用的现有事件

| 事件类型 | 用途 | Explore 中的使用 |
|----------|------|------------------|
| `step_start` | 步骤开始 | 每轮探索开始 |
| `knowledge_loaded` | 知识加载 | 显示搜索结果、章节、世界观 |
| `step_complete` | 步骤完成 | 工具调用完成 |
| `completion` | 任务完成 | 探索结束 |

## 3. 现有事件的使用方式

### 3.1 step_start - 轮次开始

```python
# 复用现有事件格式
FlowEventBuilder.step_start(
    step_id=1,
    title="Explore 深度探索（第1轮）"
)

# 输出
{
    "type": "step_start",
    "step_id": 1,
    "title": "Explore 深度探索（第1轮）",
    "status": "running",
    "timestamp": "2024-01-17T10:00:01Z"
}
```

### 3.2 knowledge_loaded - 搜索结果

```python
FlowEventBuilder.knowledge_loaded(
    step_id=1,
    knowledge_type="search",  # 复用现有类型
    title="搜索结果(5)",
    icon="Search",
    items=[
        {"name": "第3章·第18段", "tag": "0.92", "similarity": 0.92},
        {"name": "第5章·第25段", "tag": "0.89", "similarity": 0.89}
    ]
)

# 输出
{
    "type": "knowledge_loaded",
    "step_id": 1,
    "knowledge_type": "search",
    "title": "搜索结果(5)",
    "icon": "Search",
    "items": [...],
    "timestamp": "..."
}
```

### 3.3 knowledge_loaded - 章节加载

```python
FlowEventBuilder.knowledge_loaded(
    step_id=1,
    knowledge_type="chapters",
    title="章节已读取(3)",
    icon="FileText",
    items=[
        {"name": "第3章：一夕千悟", "tag": "3012字"},
        {"name": "第4章：家底", "tag": "2234字"},
        {"name": "第5章：太一门", "tag": "2891字"}
    ]
)
```

### 3.4 knowledge_loaded - 世界观加载

```python
FlowEventBuilder.knowledge_loaded(
    step_id=1,
    knowledge_type="worldview",
    title="世界观已加载(5)",
    icon="BookOpen",
    items=[
        {"name": "段融", "tag": "人物"},
        {"name": "赵穆", "tag": "人物"},
        {"name": "太一门", "tag": "地点"}
    ]
)
```

### 3.5 step_complete - 工具完成

```python
FlowEventBuilder.step_complete(
    step_id=1,
    description="首轮信息收集完成",
    tool_call={"icon": "Search", "name": "search_content"}
)
```

---

## 4. 新增事件：explore_round（V2 完整版）

> ✅ **实现状态：已实现（2026-01-17）**
>
> 此事件方法已在 `flow_events.py` 中实现。

> 基于 HTML 设计稿 `agent-writing-preview - 副本 (2).html` 行 957-1148

用于展示单轮探索的完整信息，包括工具调用、状态、证据等。

### 4.1 事件定义

```python
# 在 flow_events.py 中新增

@staticmethod
def explore_round(
    step_id: int,
    round_idx: int,
    title: str,
    tool_calls: List[Dict[str, Any]],
    hit_count: int,
    missing_items: List[str],
    status_text: str,                    # 新增：状态文本
    evidences: List[Dict[str, Any]],
    review_status: str,
    status: str = "done"
) -> dict:
    """构建 Explore 轮次事件（完整版）

    Args:
        step_id: 步骤ID
        round_idx: 轮次索引（从1开始）
        title: 轮次标题（如"初次检索与定位"）
        tool_calls: 工具调用列表
        hit_count: 命中条数
        missing_items: 缺失项列表（黄色警告）
        status_text: 状态文本（灰色，如"补漏完成"/"覆盖度达标"）
        evidences: 证据片段列表
        review_status: 审查状态（"覆盖不足"/"补齐要点"/"通过"）
        status: 轮次状态（"running"/"done"）
    """
    return {
        "type": "explore_round",
        "step_id": step_id,
        "round_idx": round_idx,
        "title": title,
        "tool_calls": tool_calls,
        "hit_count": hit_count,
        "missing_items": missing_items,
        "status_text": status_text,      # 新增
        "evidences": evidences,
        "review_status": review_status,
        "status": status,
        "timestamp": get_utc_now().isoformat()
    }
```

### 4.2 前端字段命名转换

> **重要**：后端使用 snake_case，前端转换为 camelCase

| 后端字段 | 前端字段 |
|----------|----------|
| `step_id` | `stepId` |
| `round_idx` | `roundIdx` |
| `tool_calls` | `toolCalls` |
| `hit_count` | `hitCount` |
| `missing_items` | `missingItems` |
| `status_text` | `statusText` |
| `review_status` | `reviewStatus` |

### 4.3 agentApi.ts 处理代码

```typescript
// 在 agentApi.ts 的 switch 中添加
case 'explore_round':
  callbacks.onFlowEvent?.({
    type: 'explore_round',
    stepId: data.step_id,
    roundIdx: data.round_idx,
    title: data.title,
    toolCalls: data.tool_calls,
    hitCount: data.hit_count,
    missingItems: data.missing_items,
    statusText: data.status_text,
    evidences: data.evidences,
    reviewStatus: data.review_status,
    status: data.status,
    timestamp: data.timestamp
  });
  break;

case 'explore_summary':
  callbacks.onFlowEvent?.({
    type: 'explore_summary',
    stepId: data.step_id,
    totalRounds: data.total_rounds,
    summary: data.summary,
    nextAction: data.next_action,
    nextTool: data.next_tool,
    stats: data.stats,
    timestamp: data.timestamp
  });
  break;
```

### 4.4 tool_calls 字段格式

```python
tool_calls = [
    {
        "type": "Search",           # 工具类型
        "value": "吞噬器灵 羚羊献食", # 显示值
        "highlight": "吞噬器灵 羚羊献食"  # 高亮部分（仅 Search 类型）
    },
    {
        "type": "Locate",
        "value": "第5章 · 第7段"
    },
    {
        "type": "ReadRaw",
        "value": "第5章"
    },
    {
        "type": "Review",
        "value": "覆盖不足"          # 状态值
    }
]
```

### 4.3 工具类型与图标映射

| type | 前端图标 | 标签前缀 | 说明 |
|------|----------|----------|------|
| `Search` | `search` | `Search:` | 搜索关键词，高亮显示 |
| `Locate` | `crosshair` | `Locate:` | 定位位置 |
| `ReadRaw` | `file-text` | `ReadRaw:` | 读取原文 |
| `Review` | `check-circle` | `Review:` | 审查状态 |

### 4.4 evidences 字段格式

```python
evidences = [
    {
        "chapter": 5,               # 章节序号
        "paragraph": 7,             # 段落索引
        "text": "赵穆的那柄刀，只有他一个人用过，吞噬效果也只有一条……"
    },
    {
        "chapter": 5,
        "paragraph": 9,
        "text": "器灵吞噬后，刀身泛起一道寒芒……"
    }
]
```

### 4.5 使用示例

```python
# 第1轮：初次检索
FlowEventBuilder.explore_round(
    step_id=1,
    round_idx=1,
    title="初次检索与定位",
    tool_calls=[
        {"type": "Search", "value": "吞噬器灵 羚羊献食", "highlight": "吞噬器灵 羚羊献食"},
        {"type": "Locate", "value": "第5章 · 第7段"},
        {"type": "ReadRaw", "value": "第5章"},
        {"type": "Review", "value": "覆盖不足"}
    ],
    hit_count=4,
    missing_items=["浑圆桩训练"],
    evidences=[
        {"chapter": 5, "paragraph": 7, "text": "赵穆的那柄刀，只有他一个人用过..."},
        {"chapter": 5, "paragraph": 9, "text": "器灵吞噬后，刀身泛起一道寒芒..."}
    ],
    review_status="覆盖不足",
    status="done"
)

# 输出
{
    "type": "explore_round",
    "step_id": 1,
    "round_idx": 1,
    "title": "初次检索与定位",
    "tool_calls": [...],
    "hit_count": 4,
    "missing_items": ["浑圆桩训练"],
    "evidences": [...],
    "review_status": "覆盖不足",
    "status": "done",
    "timestamp": "2024-01-17T10:00:01Z"
}
```

```python
# 第2轮：补漏检索
FlowEventBuilder.explore_round(
    step_id=2,
    round_idx=2,
    title="补漏检索与二次定位",
    tool_calls=[
        {"type": "Search", "value": "浑圆桩 训练", "highlight": "浑圆桩 训练"},
        {"type": "Locate", "value": "第2章 · 第12段"},
        {"type": "ReadRaw", "value": "第2章"},
        {"type": "Review", "value": "补齐要点"}
    ],
    hit_count=5,
    missing_items=[],  # 补漏完成
    evidences=[
        {"chapter": 2, "paragraph": 12, "text": "他每日指导这些杂役弟子练功的时间..."},
        {"chapter": 2, "paragraph": 15, "text": "浑圆桩要稳，腰胯不可松散..."}
    ],
    review_status="补齐要点",
    status="done"
)
```

```python
# 第3轮：交叉验证
FlowEventBuilder.explore_round(
    step_id=3,
    round_idx=3,
    title="交叉验证与收敛",
    tool_calls=[
        {"type": "Search", "value": "五虎群羊刀", "highlight": "五虎群羊刀"},
        {"type": "Locate", "value": "第5章 · 第8段"},
        {"type": "ReadRaw", "value": "第5章"},
        {"type": "Review", "value": "通过"}
    ],
    hit_count=3,
    missing_items=[],
    evidences=[
        {"chapter": 5, "paragraph": 8, "text": "入门级的五虎群羊刀刀法，刀势凌厉而克制..."}
    ],
    review_status="通过",
    status="done"
)
```

---

## 5. 新增事件：explore_summary（AI 分析与规划）

> ✅ **实现状态：已实现（2026-01-17）**
>
> 此事件方法已在 `flow_events.py` 中实现。

用于展示探索结束后的 AI 分析和下一步行动。

### 5.1 事件定义

```python
@staticmethod
def explore_summary(
    step_id: int,
    total_rounds: int,
    summary: str,
    next_action: str,
    next_tool: Optional[str],
    stats: Dict[str, Any]
) -> dict:
    """构建 Explore AI 分析与规划事件

    Args:
        step_id: 步骤ID
        total_rounds: 总轮次数
        summary: 探索总结
        next_action: 下一步行动描述
        next_tool: 下一步要调用的工具名（如 "smart_continue"）
        stats: 统计信息
    """
    return {
        "type": "explore_summary",
        "step_id": step_id,
        "total_rounds": total_rounds,
        "summary": summary,
        "next_action": next_action,
        "next_tool": next_tool,
        "stats": stats,
        "timestamp": get_utc_now().isoformat()
    }
```

### 5.2 stats 字段格式

```python
stats = {
    "worldview": 5,         # 世界观条目数
    "chapters": "1-4",      # 章节范围
    "evidences": 13,        # 证据片段数
    "coverage": "95%"       # 覆盖度
}
```

### 5.3 使用示例

```python
FlowEventBuilder.explore_summary(
    step_id=4,
    total_rounds=3,
    summary="经过3轮深度探索，我收集到续写第5章所需的完整背景信息。主角林逸刚通过灵根测试（下品灵根），被分配到青云宗外门弟子区。了解到外门弟子每月可领取一枚聚灵丹，需完成任务获取更多资源。发现下月即将举行外门大比，前十名可进入灵泉池修炼。",
    next_action="基于这些背景信息，我将执行续写第5章，重点描写：林逸初到外门的感受和环境、了解修炼规则和资源制度的过程、得知外门大比后决心参加以弥补资质不足。",
    next_tool="smart_continue",
    stats={
        "worldview": 5,
        "chapters": "1-4",
        "evidences": 13,
        "coverage": "95%"
    }
)

# 输出
{
    "type": "explore_summary",
    "step_id": 4,
    "total_rounds": 3,
    "summary": "经过3轮深度探索...",
    "next_action": "基于这些背景信息...",
    "next_tool": "smart_continue",
    "stats": {
        "worldview": 5,
        "chapters": "1-4",
        "evidences": 13,
        "coverage": "95%"
    },
    "timestamp": "2024-01-17T10:00:30Z"
}
```

---

## 6. 旧版事件：explore_analysis（保留兼容）

> 注意：推荐使用新版 `explore_round` + `explore_summary`，此事件保留向后兼容。

```python
@staticmethod
def explore_analysis(
    step_id: int,
    round_idx: int,
    reasoning: str,
    stats: Dict[str, int],
    sufficient: bool,
    next_actions: Optional[List[str]] = None
) -> dict:
    """构建 Explore AI 分析事件（旧版，保留兼容）"""
    return {
        "type": "explore_analysis",
        "step_id": step_id,
        "round_idx": round_idx,
        "reasoning": reasoning,
        "stats": stats,
        "sufficient": sufficient,
        "next_actions": next_actions or [],
        "timestamp": get_utc_now().isoformat()
    }
```

---

## 7. 事件序列示例（V2 完整版）

### 7.1 完整的 Explore 事件流

```
1. step_start(step_id=1, title="Explore 轨迹（3 轮）")

2. explore_round(
     step_id=1, round_idx=1,
     title="初次检索与定位",
     tool_calls=[Search, Locate, ReadRaw, Review],
     hit_count=4,
     missing_items=["浑圆桩训练"],
     evidences=[...],
     review_status="覆盖不足"
   )

3. explore_round(
     step_id=1, round_idx=2,
     title="补漏检索与二次定位",
     tool_calls=[Search, Locate, ReadRaw, Review],
     hit_count=5,
     missing_items=[],
     evidences=[...],
     review_status="补齐要点"
   )

4. explore_round(
     step_id=1, round_idx=3,
     title="交叉验证与收敛",
     tool_calls=[Search, Locate, ReadRaw, Review],
     hit_count=3,
     missing_items=[],
     evidences=[...],
     review_status="通过"
   )

5. step_complete(
     step_id=1,
     description="多轮检索-定位-原文读取，逐轮 review 覆盖度，补漏后输出完整证据链。",
     tool_call={"icon": "Scan", "name": "explore_content (max_rounds: 3)"}
   )

6. explore_summary(
     step_id=1,
     total_rounds=3,
     summary="经过3轮深度探索...",
     next_action="基于这些背景信息，我将执行...",
     next_tool="smart_continue",
     stats={"worldview": 5, "chapters": "1-4", "evidences": 13, "coverage": "95%"}
   )
```

---

## 8. 与前端组件的映射（V2 更新）

| 事件 | 前端组件/操作 |
|------|---------------|
| `step_start` | 创建 execution-step 容器 |
| `explore_round` | 在 explore-panel 中添加 explore-round 胶囊 |
| `step_complete` | 显示 step-description 和 tool-operation |
| `explore_summary` | 显示 AI 分析与规划卡片 |
| `completion` | 显示完成状态 |

### 8.1 explore_round → 前端组件映射

| 事件字段 | 前端组件 |
|----------|----------|
| `title` | `.explore-round-title` |
| `tool_calls` | `.explore-tags` 中的 `.explore-tag` |
| `hit_count` | `.explore-status .hit` |
| `missing_items` | `.explore-status .warn` |
| `evidences` | `.explore-evidence .explore-items` |
| `review_status` | `.explore-tag[Review]` 的值 |

### 8.2 explore_summary → 前端组件映射

| 事件字段 | 前端组件 |
|----------|----------|
| `summary` | "探索总结" 区块内容 |
| `next_action` | "下一步行动" 区块内容 |
| `next_tool` | 高亮的工具名（`<span style="color:#5c9eff">`） |
| `stats.worldview` | 世界观统计标签 |
| `stats.chapters` | 章节统计标签 |
| `stats.evidences` | 证据统计标签 |
| `stats.coverage` | 覆盖度统计标签（绿色） |

---

## 9. 实现：事件发射器（V2 更新）

```python
class ExploreEventEmitter:
    """Explore 事件发射器（V2 完整版）"""

    def __init__(self, emit_callback: Callable[[dict], None]):
        self.emit = emit_callback
        self.step_id = 0
        self.rounds_data: List[dict] = []  # 收集轮次数据

    def start_explore(self, max_rounds: int):
        """探索开始"""
        self.step_id += 1
        event = FlowEventBuilder.step_start(
            step_id=self.step_id,
            title=f"Explore 轨迹（{max_rounds} 轮）"
        )
        self.emit(event)
        return self.step_id

    def emit_round(
        self,
        round_idx: int,
        title: str,
        tool_calls: List[Dict],
        hit_count: int,
        missing_items: List[str],
        evidences: List[Dict],
        review_status: str
    ):
        """发射轮次事件"""
        event = FlowEventBuilder.explore_round(
            step_id=self.step_id,
            round_idx=round_idx,
            title=title,
            tool_calls=tool_calls,
            hit_count=hit_count,
            missing_items=missing_items,
            evidences=evidences,
            review_status=review_status,
            status="done"
        )
        self.emit(event)
        self.rounds_data.append(event)

    def complete_explore(self, description: str, total_rounds: int):
        """探索步骤完成"""
        event = FlowEventBuilder.step_complete(
            step_id=self.step_id,
            description=description,
            tool_call={
                "icon": "Scan",
                "name": f"explore_content (max_rounds: {total_rounds})"
            }
        )
        self.emit(event)

    def emit_summary(
        self,
        summary: str,
        next_action: str,
        next_tool: Optional[str],
        stats: Dict[str, Any]
    ):
        """发射 AI 分析与规划事件"""
        event = FlowEventBuilder.explore_summary(
            step_id=self.step_id,
            total_rounds=len(self.rounds_data),
            summary=summary,
            next_action=next_action,
            next_tool=next_tool,
            stats=stats
        )
        self.emit(event)
```

### 9.1 使用示例

```python
emitter = ExploreEventEmitter(emit_callback=send_sse_event)

# 1. 开始探索
emitter.start_explore(max_rounds=3)

# 2. 发射轮次事件
emitter.emit_round(
    round_idx=1,
    title="初次检索与定位",
    tool_calls=[
        {"type": "Search", "value": "吞噬器灵", "highlight": "吞噬器灵"},
        {"type": "Locate", "value": "第5章 · 第7段"},
        {"type": "ReadRaw", "value": "第5章"},
        {"type": "Review", "value": "覆盖不足"}
    ],
    hit_count=4,
    missing_items=["浑圆桩训练"],
    evidences=[{"chapter": 5, "paragraph": 7, "text": "..."}],
    review_status="覆盖不足"
)

# ... 第2轮、第3轮 ...

# 3. 完成探索步骤
emitter.complete_explore(
    description="多轮检索-定位-原文读取，逐轮 review 覆盖度，补漏后输出完整证据链。",
    total_rounds=3
)

# 4. 发射 AI 分析
emitter.emit_summary(
    summary="经过3轮深度探索...",
    next_action="基于这些背景信息，我将执行...",
    next_tool="smart_continue",
    stats={"worldview": 5, "chapters": "1-4", "evidences": 13, "coverage": "95%"}
)
```

---

## 10. 工具图标映射（V2 更新）

```python
# 在 flow_events.py 的 TOOL_ICONS 中添加

TOOL_ICONS = {
    # ... 现有映射 ...

    # Explore 相关
    "explore_content": "Scan",
    "read_paragraph": "FileText",
}

# Explore 工具标签类型图标映射
EXPLORE_TAG_ICONS = {
    "Search": "search",
    "Locate": "crosshair",
    "ReadRaw": "file-text",
    "Review": "check-circle",
}
```
