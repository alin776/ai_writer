# Explore 输出格式

## 1. 设计原则

| 原则 | 说明 |
|------|------|
| 精度零丢失 | 原文内容原样传递，不压缩、不摘要 |
| 结构清晰 | 便于后续任务直接使用 |
| 可追溯 | 包含轨迹信息，便于调试和展示 |

## 2. 输出结构

```python
from dataclasses import dataclass
from typing import Dict, List, Any
from datetime import datetime

@dataclass
class ExploreResult:
    """Explore 工具的最终输出"""

    # ========== 原文内容（精度零丢失）==========

    evidences: List[Evidence]
    # 搜索到的所有证据片段，原样保留

    paragraphs: List[ParagraphRead]
    # 精确读取的段落原文 + 上下文

    chapters: Dict[int, ChapterRead]
    # 读取的完整章节原文

    worldview: Dict[str, List[WorldviewItem]]
    # 世界观设定

    # ========== AI 分析（辅助信息）==========

    analysis: str
    # AI 生成的信息总结和分析
    # 注意：这是辅助信息，不替代原文

    # ========== 统计信息 ==========

    stats: ExploreStats

    # ========== 轨迹信息（给前端展示）==========

    rounds: List[ExploreRound]
    # 每轮的执行记录

    stop_reason: str
    # 停止原因

    total_duration_ms: int
    # 总耗时

@dataclass
class ExploreStats:
    """探索统计"""
    total_evidences: int
    total_paragraphs: int
    total_chapters: int
    total_worldview_items: int
    total_rounds: int
    searched_queries: List[str]
```

## 3. 序列化格式

### 3.1 完整 JSON 格式

```json
{
  "evidences": [
    {
      "text": "段融性格坚韧，从不轻言放弃",
      "chapter_order": 2,
      "paragraph_index": 5,
      "similarity": 0.92,
      "source_type": "chapter",
      "query": "段融性格",
      "round_idx": 1
    },
    {
      "text": "炼体三层巅峰，距离四层只差一步之遥",
      "chapter_order": 5,
      "paragraph_index": 25,
      "similarity": 0.89,
      "source_type": "chapter",
      "query": "段融修炼进度",
      "round_idx": 1
    }
  ],

  "paragraphs": [
    {
      "chapter_order": 5,
      "chapter_title": "太一门",
      "paragraph_index": 25,
      "text": "炼体三层巅峰，距离四层只差一步之遥。段融睁开双眼，眼中闪过一丝精光。",
      "context_before": [
        "段融盘膝而坐，体内灵力缓缓流转...",
        "经过数日苦修，他感觉到丹田中有了微妙变化..."
      ],
      "context_after": [
        "\"再有三五日，应该就能突破了。\"他暗自思忖...",
        "正在此时，门外传来一阵脚步声..."
      ],
      "round_idx": 2
    }
  ],

  "chapters": {
    "5": {
      "order": 5,
      "title": "太一门",
      "content": "太一门坐落于青云山脉...(完整原文)...",
      "word_count": 2891,
      "round_idx": 2
    }
  },

  "worldview": {
    "character": [
      {
        "id": "char_001",
        "name": "段融",
        "category": "character",
        "description": "主角，穿越者，性格坚韧沉默",
        "attributes": {
          "age": 18,
          "cultivation": "炼体三层巅峰",
          "personality": ["坚韧", "沉默", "心思缜密"]
        }
      },
      {
        "id": "char_002",
        "name": "赵穆",
        "category": "character",
        "description": "引路人，对段融友善",
        "attributes": {
          "role": "杂役弟子",
          "relationship_to_protagonist": "友人"
        }
      }
    ]
  },

  "analysis": "经过 2 轮深度探索，收集到续写第6章所需的完整信息：\n\n1. 段融性格：坚韧、沉默、心思缜密\n2. 修炼进度：炼体三层巅峰，即将突破四层\n3. 同门关系：与赵穆友善，对其他杂役保持距离\n4. 当前状态：在太一门杂役弟子区修炼\n\n建议续写方向：可以描写段融突破四层的过程，或与赵穆一起执行任务的情节。",

  "stats": {
    "total_evidences": 8,
    "total_paragraphs": 3,
    "total_chapters": 1,
    "total_worldview_items": 5,
    "total_rounds": 2,
    "searched_queries": ["段融性格", "段融修炼进度", "段融 同门 关系"]
  },

  "rounds": [
    {
      "round_idx": 1,
      "reasoning": "首先搜索段融的性格特点和修炼进度...",
      "tool_calls": [...],
      "new_evidences_count": 5,
      "new_paragraphs_count": 0,
      "sufficient": false,
      "timestamp": "2024-01-17T10:00:01Z"
    },
    {
      "round_idx": 2,
      "reasoning": "搜索结果需要验证，读取原文确认...",
      "tool_calls": [...],
      "new_evidences_count": 3,
      "new_paragraphs_count": 3,
      "sufficient": true,
      "timestamp": "2024-01-17T10:00:10Z"
    }
  ],

  "stop_reason": "AI 判断信息充足",
  "total_duration_ms": 22000
}
```

## 4. 传递给后续任务

### 4.1 构建上下文字符串

```python
def build_context_for_task(result: ExploreResult) -> str:
    """
    将 ExploreResult 转换为后续任务可用的上下文字符串

    注意：原文内容原样传递，不压缩
    """
    sections = []

    # 1. 世界观设定
    if result.worldview:
        sections.append("## 世界观设定\n")
        for category, items in result.worldview.items():
            sections.append(f"### {category}\n")
            for item in items:
                sections.append(f"- **{item.name}**: {item.description}\n")
                if item.attributes:
                    for key, value in item.attributes.items():
                        sections.append(f"  - {key}: {value}\n")

    # 2. 章节原文
    if result.chapters:
        sections.append("\n## 已读取的章节原文\n")
        for order, chapter in sorted(result.chapters.items()):
            sections.append(f"### 第{chapter.order}章：{chapter.title}\n")
            sections.append(f"{chapter.content}\n")

    # 3. 精确读取的段落（如果没有读取整章）
    if result.paragraphs:
        # 过滤掉已经在 chapters 中的段落
        read_chapter_orders = set(result.chapters.keys())
        paragraphs_to_show = [
            p for p in result.paragraphs
            if p.chapter_order not in read_chapter_orders
        ]
        if paragraphs_to_show:
            sections.append("\n## 精确读取的段落\n")
            for p in paragraphs_to_show:
                sections.append(f"### 第{p.chapter_order}章《{p.chapter_title}》第{p.paragraph_index}段\n")
                if p.context_before:
                    sections.append("【前文】\n" + "\n".join(p.context_before) + "\n")
                sections.append(f"【目标段落】\n{p.text}\n")
                if p.context_after:
                    sections.append("【后文】\n" + "\n".join(p.context_after) + "\n")

    # 4. 搜索证据（作为补充）
    if result.evidences:
        # 过滤掉已经在 paragraphs 或 chapters 中出现的证据
        shown_positions = set()
        for p in result.paragraphs:
            shown_positions.add((p.chapter_order, p.paragraph_index))
        for order in result.chapters.keys():
            # 如果整章都读取了，该章的所有证据都不需要单独显示
            pass  # 这里简化处理

        evidences_to_show = [
            e for e in result.evidences
            if (e.chapter_order, e.paragraph_index) not in shown_positions
        ]

        if evidences_to_show:
            sections.append("\n## 相关片段\n")
            for e in evidences_to_show[:10]:  # 最多显示 10 条
                sections.append(f"- [{e.chapter_order}章{e.paragraph_index}段] {e.text}\n")

    # 5. AI 分析
    if result.analysis:
        sections.append(f"\n## AI 分析\n{result.analysis}\n")

    return "".join(sections)
```

### 4.2 使用示例（修正版）

**重要**：smart_continue 没有 context 参数！需要通过 TaskRunner 传递。

```python
# ⚠️ 错误的方式（context 参数不存在）
# await smart_continue(context=context)

# ✅ 正确的方式：通过 TaskRunner 的任务链传递

# 1. Planning 阶段：AI 规划任务依赖
tasks = [
    {
        "task_id": 1,
        "tool": "explore_content",
        "params": {
            "work_id": "work_123",
            "target_task": "续写第6章，分析段融性格"
        }
    },
    {
        "task_id": 2,
        "tool": "smart_continue",
        "params": {
            "chapter_id": "chapter_6_id",
            # 通过 $ref 引用 explore_content 的结果
            "chapter_content": {"$ref": {"task_id": 1, "path": ""}}
        },
        "depends_on": [1]
    }
]

# 2. Execution 阶段：TaskRunner 处理
# - 执行 task 1 (explore_content)
# - 将结果保存到 state["explore_result"]
# - 调用 build_context_for_task() 转换为字符串
# - 执行 task 2 时，将转换后的上下文注入 chapter_content
```

### 4.3 TaskRunner 集成（补充）

```python
# execution/task_runner.py 需要添加的逻辑

async def execute_task(self, task, work_id, chapter_id, context,
                       context_payload=None, state=None, ...):
    tool_name = task.get("tool")

    # explore_content 特殊处理
    if tool_name == "explore_content":
        result = await self._call_tool_via_registry(
            tool_name=tool_name,
            tool_args=params,
            state=tool_state
        )

        # 保存到 state 供后续任务使用
        try:
            explore_result = json.loads(result)
            if state is not None:
                state["explore_result"] = explore_result
                # 预构建上下文字符串
                from app.services.agent.tools.explore_tools import build_context_for_task
                state["explore_context"] = build_context_for_task(explore_result)
        except Exception as e:
            logger.warning(f"[TaskRunner] 解析 explore_result 失败: {e}")

        return result

    # smart_continue 使用 explore 结果
    elif tool_name == "smart_continue":
        # 如果有 explore_context，优先使用
        if state and state.get("explore_context"):
            params["chapter_content"] = state["explore_context"]
        else:
            context_param = self._extract_context_param(params, context)
            params["chapter_content"] = context_param

        return await self._call_tool_via_registry(
            tool_name=tool_name,
            tool_args=params,
            state=tool_state
        )
```

## 5. 前端展示数据（V2 完整版）

> 基于 HTML 设计稿 `agent-writing-preview - 副本 (2).html`

### 5.1 to_frontend_display 函数（V2 更新）

```python
def to_frontend_display(result: ExploreResult) -> dict:
    """转换为前端展示格式（V2 完整版）

    与 HTML 设计稿的 Explore 轨迹板块完全对应
    """
    return {
        # 轨迹展示（对应 explore-panel）
        "rounds": [
            {
                "round_idx": r.round_idx,
                "title": _get_round_title(r.round_idx, r),  # 轮次标题
                "tool_calls": _format_tool_calls(r),        # 工具标签
                "hit_count": r.new_evidences_count,         # 命中数
                "missing_items": r.missing_items or [],     # 缺失项（黄色）
                "status_text": _get_status_text(r),         # 状态文本（灰色）
                "evidences": [                              # 证据片段
                    {
                        "chapter": e.chapter_order,
                        "paragraph": e.paragraph_index,
                        "text": e.text[:100] + "..." if len(e.text) > 100 else e.text
                    }
                    for e in r.evidences
                ],
                "review_status": _get_review_status(r),     # 审查状态
                "status": "done"
            }
            for r in result.rounds
        ],

        # AI 分析与规划（对应 AI 分析与规划卡片）
        "ai_analysis": {
            "summary": result.analysis,
            "next_action": _generate_next_action(result),
            "next_tool": _get_next_tool(result),
            "stats": {
                "worldview": result.stats.total_worldview_items,
                "chapters": _format_chapters_range(result.chapters),
                "evidences": result.stats.total_evidences,
                "coverage": _calculate_coverage(result)
            }
        },

        # 步骤描述
        "step_description": "多轮检索-定位-原文读取，逐轮 review 覆盖度，补漏后输出完整证据链。",

        # 工具调用标签
        "tool_operation": {
            "icon": "Scan",
            "name": f"explore_content (max_rounds: {result.stats.total_rounds})"
        },

        # 完成状态
        "status": "completed",
        "stop_reason": result.stop_reason,
        "duration_ms": result.total_duration_ms
    }


def _get_round_title(round_idx: int, round_data) -> str:
    """生成轮次标题"""
    titles = {
        1: "初次检索与定位",
        2: "补漏检索与二次定位",
        3: "交叉验证与收敛",
    }
    return titles.get(round_idx, f"深度探索（第{round_idx}轮）")


def _format_tool_calls(round_data) -> List[dict]:
    """格式化工具调用为标签格式"""
    tags = []

    # 从 round_data.tool_calls 提取信息
    for tc in round_data.tool_calls:
        if tc.tool_name == "search_content":
            query = tc.params.get("query", "")
            tags.append({
                "type": "Search",
                "value": query,
                "highlight": query
            })
        elif tc.tool_name == "locate_content":
            chapter = tc.params.get("chapter_order", "?")
            para = tc.result.get("paragraph_index", "?") if tc.result else "?"
            tags.append({
                "type": "Locate",
                "value": f"第{chapter}章 · 第{para}段"
            })
        elif tc.tool_name in ["read_paragraph", "get_chapter_by_order_tool"]:
            chapter = tc.params.get("chapter_order", "?")
            tags.append({
                "type": "ReadRaw",
                "value": f"第{chapter}章"
            })

    # 添加 Review 标签
    tags.append({
        "type": "Review",
        "value": _get_review_status(round_data)
    })

    return tags


def _get_review_status(round_data) -> str:
    """获取审查状态"""
    if round_data.sufficient:
        return "通过"
    elif round_data.missing_items:
        return "覆盖不足"
    else:
        return "补齐要点"


def _get_status_text(round_data) -> str:
    """获取状态文本（灰色显示）

    仅在 missing_items 为空时显示
    """
    if round_data.missing_items:
        return ""  # 有缺失项时不显示状态文本
    elif round_data.sufficient:
        return "覆盖度达标"
    else:
        return "补漏完成"


def _format_chapters_range(chapters: Dict[int, ChapterRead]) -> str:
    """格式化章节范围"""
    if not chapters:
        return "-"
    orders = sorted(chapters.keys())
    if len(orders) == 1:
        return str(orders[0])
    return f"{orders[0]}-{orders[-1]}"


def _calculate_coverage(result: ExploreResult) -> str:
    """计算覆盖度"""
    # 基于轮次结果计算
    if not result.rounds:
        return "0%"

    last_round = result.rounds[-1]
    if last_round.sufficient:
        return "95%"
    elif last_round.new_evidences_count > 0:
        return "70%"
    else:
        return "50%"


def _generate_next_action(result: ExploreResult) -> str:
    """生成下一步行动描述"""
    return f"基于这些背景信息，我将执行续写，重点描写收集到的关键情节要素。"


def _get_next_tool(result: ExploreResult) -> str:
    """获取下一步工具名"""
    return "smart_continue"
```

### 5.2 完整输出示例（JSON）

```json
{
  "rounds": [
    {
      "round_idx": 1,
      "title": "初次检索与定位",
      "tool_calls": [
        {"type": "Search", "value": "吞噬器灵 羚羊献食", "highlight": "吞噬器灵 羚羊献食"},
        {"type": "Locate", "value": "第5章 · 第7段"},
        {"type": "ReadRaw", "value": "第5章"},
        {"type": "Review", "value": "覆盖不足"}
      ],
      "hit_count": 4,
      "missing_items": ["浑圆桩训练"],
      "evidences": [
        {"chapter": 5, "paragraph": 7, "text": "赵穆的那柄刀，只有他一个人用过，吞噬效果也只有一条……"},
        {"chapter": 5, "paragraph": 9, "text": "器灵吞噬后，刀身泛起一道寒芒……"}
      ],
      "review_status": "覆盖不足",
      "status": "done"
    },
    {
      "round_idx": 2,
      "title": "补漏检索与二次定位",
      "tool_calls": [
        {"type": "Search", "value": "浑圆桩 训练", "highlight": "浑圆桩 训练"},
        {"type": "Locate", "value": "第2章 · 第12段"},
        {"type": "ReadRaw", "value": "第2章"},
        {"type": "Review", "value": "补齐要点"}
      ],
      "hit_count": 5,
      "missing_items": [],
      "evidences": [
        {"chapter": 2, "paragraph": 12, "text": "他每日指导这些杂役弟子练功的时间，也不过只有半柱香而已……"},
        {"chapter": 2, "paragraph": 15, "text": "浑圆桩要稳，腰胯不可松散……"}
      ],
      "review_status": "补齐要点",
      "status": "done"
    },
    {
      "round_idx": 3,
      "title": "交叉验证与收敛",
      "tool_calls": [
        {"type": "Search", "value": "五虎群羊刀", "highlight": "五虎群羊刀"},
        {"type": "Locate", "value": "第5章 · 第8段"},
        {"type": "ReadRaw", "value": "第5章"},
        {"type": "Review", "value": "通过"}
      ],
      "hit_count": 3,
      "missing_items": [],
      "evidences": [
        {"chapter": 5, "paragraph": 8, "text": "入门级的五虎群羊刀刀法，刀势凌厉而克制……"}
      ],
      "review_status": "通过",
      "status": "done"
    }
  ],
  "ai_analysis": {
    "summary": "经过3轮深度探索，我收集到续写第5章所需的完整背景信息。主角林逸刚通过灵根测试（下品灵根），被分配到青云宗外门弟子区。了解到外门弟子每月可领取一枚聚灵丹，需完成任务获取更多资源。发现下月即将举行外门大比，前十名可进入灵泉池修炼。",
    "next_action": "基于这些背景信息，我将执行续写第5章，重点描写：林逸初到外门的感受和环境、了解修炼规则和资源制度的过程、得知外门大比后决心参加以弥补资质不足。",
    "next_tool": "smart_continue",
    "stats": {
      "worldview": 5,
      "chapters": "1-4",
      "evidences": 13,
      "coverage": "95%"
    }
  },
  "step_description": "多轮检索-定位-原文读取，逐轮 review 覆盖度，补漏后输出完整证据链。",
  "tool_operation": {
    "icon": "Scan",
    "name": "explore_content (max_rounds: 3)"
  },
  "status": "completed",
  "stop_reason": "AI 判断信息充足",
  "duration_ms": 22000
}
```

### 5.3 前端组件字段映射

| JSON 字段 | 前端组件 | 说明 |
|-----------|----------|------|
| `rounds[].title` | `.explore-round-title` | 轮次标题 |
| `rounds[].tool_calls` | `.explore-tags` | 工具标签列表 |
| `rounds[].hit_count` | `.explore-status .hit` | 绿色命中数 |
| `rounds[].missing_items` | `.explore-status .warn` | 黄色缺失项 |
| `rounds[].evidences` | `.explore-evidence .explore-items` | 证据片段 |
| `rounds[].review_status` | `tool_calls[Review].value` | 审查状态 |
| `ai_analysis.summary` | "探索总结" 内容 | AI 分析 |
| `ai_analysis.next_action` | "下一步行动" 内容 | 下一步描述 |
| `ai_analysis.next_tool` | 高亮工具名 | 蓝色高亮 |
| `ai_analysis.stats.worldview` | 世界观标签值 | 蓝色 |
| `ai_analysis.stats.chapters` | 章节标签值 | 蓝色 |
| `ai_analysis.stats.evidences` | 证据标签值 | 蓝色 |
| `ai_analysis.stats.coverage` | 覆盖度标签值 | 绿色 |
| `step_description` | `.step-description` | 步骤描述 |
| `tool_operation` | `.tool-operation` | 工具调用标签 |
