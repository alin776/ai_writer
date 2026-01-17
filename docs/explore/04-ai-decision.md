# Explore AI 决策逻辑

## 1. 决策流程

```
┌─────────────────────────────────────────────────────────┐
│ 每轮开始                                                │
│                                                         │
│  1. 构建 Prompt（目标任务 + 已收集信息 + 可用工具）     │
│                                                         │
│  2. 调用 AI → 返回决策结果                              │
│     - sufficient: 是否充足                              │
│     - reasoning: 思考过程                               │
│     - tool_calls: 本轮要调用的工具                      │
│                                                         │
│  3. 如果 sufficient=true → 退出循环                     │
│     如果 sufficient=false → 执行工具 → 下一轮           │
└─────────────────────────────────────────────────────────┘
```

## 2. AI Plan Prompt

```python
EXPLORE_PLAN_PROMPT = """
你是一个信息收集专家。你的目标是为后续任务收集足够的上下文信息。

## 目标任务
{target_task}

## 当前已收集的信息

### 搜索结果 ({evidences_count} 条)
{evidences_summary}

### 已读取的段落原文 ({paragraphs_count} 条)
{paragraphs_summary}

### 已读取的章节 ({chapters_count} 章)
{chapters_summary}

### 世界观设定 ({worldview_count} 条)
{worldview_summary}

## 可用工具

1. search_content(query: str)
   - 语义搜索，返回匹配片段 + 位置信息
   - 已搜索过的 query: {searched_queries}

2. read_paragraph(chapter_order: int, paragraph_index: int, context_before: int, context_after: int)
   - 精确读取段落原文 + 上下文
   - 已读取过的位置: {read_positions}

3. get_chapter(chapter_orders: List[int])
   - 读取完整章节原文
   - 已读取过的章节: {read_chapters}

4. get_worldview(categories: List[str])
   - 读取世界观设定
   - 可选分类: character, location, power_system, item, rule
   - 已读取过的分类: {read_categories}

## 你的任务

判断当前信息是否足够支撑目标任务。如果不够，决定本轮调用哪些工具。

注意：
- 搜索结果只是片段，如果需要确认完整上下文，使用 read_paragraph
- 优先使用精确工具（read_paragraph）验证搜索结果
- 避免重复搜索已有的 query
- 可以并行调用多个工具

## 输出格式（JSON）

{{
  "sufficient": false,
  "reasoning": "说明为什么信息不足，还需要什么",
  "tool_calls": [
    {{
      "tool": "search_content",
      "params": {{ "query": "xxx" }}
    }},
    {{
      "tool": "read_paragraph",
      "params": {{ "chapter_order": 5, "paragraph_index": 25, "context_before": 2, "context_after": 2 }}
    }}
  ]
}}

或者

{{
  "sufficient": true,
  "reasoning": "说明为什么信息已经充足",
  "tool_calls": []
}}
"""
```

## 3. Prompt 变量填充

```python
def build_plan_prompt(target_task: str, state: ExploreState) -> str:
    """构建 AI Plan Prompt"""

    # 证据摘要
    evidences_summary = "\n".join([
        f"- [{e.chapter_order}章{e.paragraph_index}段] {e.text[:100]}... (query: {e.query})"
        for e in state.evidences[:20]  # 最多显示 20 条
    ]) or "暂无"

    # 段落摘要
    paragraphs_summary = "\n".join([
        f"- [{p.chapter_order}章{p.paragraph_index}段] {p.text[:100]}..."
        for p in state.paragraphs[:10]
    ]) or "暂无"

    # 章节摘要
    chapters_summary = "\n".join([
        f"- 第{c.order}章《{c.title}》({c.word_count}字)"
        for c in state.chapters.values()
    ]) or "暂无"

    # 世界观摘要
    worldview_items = []
    for category, items in state.worldview.items():
        for item in items[:5]:  # 每个分类最多 5 条
            worldview_items.append(f"- [{category}] {item.name}: {item.description[:50]}...")
    worldview_summary = "\n".join(worldview_items) or "暂无"

    return EXPLORE_PLAN_PROMPT.format(
        target_task=target_task,
        evidences_count=len(state.evidences),
        evidences_summary=evidences_summary,
        paragraphs_count=len(state.paragraphs),
        paragraphs_summary=paragraphs_summary,
        chapters_count=len(state.chapters),
        chapters_summary=chapters_summary,
        worldview_count=sum(len(items) for items in state.worldview.values()),
        worldview_summary=worldview_summary,
        searched_queries=list(state.searched_queries) or "无",
        read_positions=list(state.read_paragraph_positions) or "无",
        read_chapters=list(state.read_chapter_orders) or "无",
        read_categories=list(state.read_worldview_categories) or "无"
    )
```

## 4. AI 输出解析

```python
from dataclasses import dataclass
from typing import List, Dict, Any
import json

@dataclass
class ToolCallPlan:
    tool: str
    params: Dict[str, Any]

@dataclass
class AIDecision:
    sufficient: bool
    reasoning: str
    tool_calls: List[ToolCallPlan]

def parse_ai_decision(response: str) -> AIDecision:
    """解析 AI 返回的决策 JSON"""
    try:
        # 提取 JSON（可能包含在 markdown code block 中）
        json_str = response
        if "```json" in response:
            json_str = response.split("```json")[1].split("```")[0]
        elif "```" in response:
            json_str = response.split("```")[1].split("```")[0]

        data = json.loads(json_str.strip())

        return AIDecision(
            sufficient=data.get("sufficient", False),
            reasoning=data.get("reasoning", ""),
            tool_calls=[
                ToolCallPlan(tool=tc["tool"], params=tc["params"])
                for tc in data.get("tool_calls", [])
            ]
        )
    except Exception as e:
        # 解析失败，返回默认决策（继续探索）
        return AIDecision(
            sufficient=False,
            reasoning=f"AI 输出解析失败: {e}",
            tool_calls=[]
        )
```

## 5. 停止条件判断

```python
def should_stop(
    decision: AIDecision,
    state: ExploreState,
    round_idx: int,
    max_rounds: int,
    start_time: datetime,
    timeout_seconds: int
) -> Tuple[bool, str]:
    """
    判断是否应该停止探索

    Returns:
        (should_stop, reason)
    """
    # 优先级 1: AI 判断信息充足
    if decision.sufficient:
        return True, "AI 判断信息充足"

    # 优先级 2: 收敛检测
    if state.check_convergence(window=2):
        return True, "连续 2 轮没有新增信息，已收敛"

    # 优先级 3: 轮数上限
    if round_idx >= max_rounds:
        return True, f"达到最大轮数 {max_rounds}"

    # 优先级 4: 超时
    elapsed = (datetime.now() - start_time).total_seconds()
    if elapsed > timeout_seconds:
        return True, f"超时 {timeout_seconds}s"

    # 优先级 5: 没有更多工具可调用
    if not decision.tool_calls:
        return True, "没有更多工具可调用"

    return False, ""
```

## 6. 模型选择

| 场景 | 推荐模型 | 理由 |
|------|----------|------|
| AI Plan 决策 | gpt-4o-mini / claude-3-haiku | 速度快，决策简单 |
| 最终分析生成 | gpt-4o / claude-3-sonnet | 需要更好的理解和总结能力 |

```python
EXPLORE_PLAN_MODEL = "gpt-4o-mini"  # 或 "claude-3-haiku"
EXPLORE_ANALYSIS_MODEL = "gpt-4o"   # 或 "claude-3-sonnet"
```

## 7. 决策示例

### 示例 1: 信息不足

```json
{
  "sufficient": false,
  "reasoning": "搜索到段融修炼进度的片段，但片段太短，需要读取原文确认当前境界。同时缺少段融与同门的关系信息。",
  "tool_calls": [
    {
      "tool": "read_paragraph",
      "params": { "chapter_order": 5, "paragraph_index": 25, "context_before": 2, "context_after": 2 }
    },
    {
      "tool": "search_content",
      "params": { "query": "段融 同门 关系" }
    }
  ]
}
```

### 示例 2: 信息充足

```json
{
  "sufficient": true,
  "reasoning": "已收集到：1) 段融性格特点（坚韧、沉默、心思缜密）2) 修炼进度（炼体三层巅峰，即将突破四层）3) 与赵穆的友善关系 4) 第5章完整原文作为上下文。信息足够支撑续写第6章。",
  "tool_calls": []
}
```
