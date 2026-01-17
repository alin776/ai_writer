# Explore 与现有架构集成

> ✅ **实现状态说明（2026-01-17 更新）**
>
> | 组件 | 文档状态 | 实际状态 |
> |------|---------|---------|
> | `explore_tools.py` | 新增 | ✅ 已实现（~800行） |
> | `read_paragraph` | 新增 | ✅ 已实现（~130行） |
> | `flow_events.py` 事件方法 | 修改 | ✅ 已实现（~80行） |
> | `tool_executor.py` 参数处理 | 修改 | ✅ 已实现（~50行） |
> | `planning_examples.py` 示例 | 修改 | ✅ 已实现（~120行） |
> | 前端事件处理 | 修改 | ✅ 已实现（~110行） |
> | 前端 UI 组件 | 新增 | ✅ 已实现（ExploreCard.tsx ~470行） |
> | 类型定义 | 新增 | ✅ 已实现（types/agent.ts ~100行） |

## 1. 集成策略

**最小改动原则**：Explore 作为新工具加入，复用现有工具和事件体系。

| 改动类型 | 文件 | 说明 |
|----------|------|------|
| 新增 | `tools/explore_tools.py` | Explore 核心实现 |
| 修改 | `langgraph_tools.py` | 添加 `read_paragraph` 工具 |
| 修改 | `prompts/tool_descriptions.py` | 添加 `explore_content` 工具描述 |
| 修改 | `stream/flow_events.py` | 添加 `explore_analysis` 事件 |
| 修改 | `execution/tool_executor.py` | 添加工具调用支持 |
| 修改 | `utils/tool_cache.py` | 添加段落级缓存支持 |

## 2. 工具注册

### 2.1 添加 read_paragraph

```python
# langgraph_tools.py

@tool
async def read_paragraph(
    work_id: str,
    chapter_order: int,
    paragraph_index: int,
    context_before: int = 2,
    context_after: int = 2
) -> str:
    """精确读取段落原文 + 上下文"""
    # 实现见 02-tools.md
```

### 2.2 添加 explore_content

```python
# tools/explore_tools.py

@tool
async def explore_content(
    work_id: str,
    target_task: str,
    max_rounds: int = 5,
    timeout_seconds: int = 60
) -> str:
    """
    深度探索工具（get_writing_context 的增强版）

    适用场景：
    - 任务涉及多个章节的关联分析
    - 需要深入理解人物关系、情节发展
    - 搜索结果需要原文验证

    Args:
        work_id: 作品ID
        target_task: 目标任务描述
        max_rounds: 最大探索轮数
        timeout_seconds: 超时时间

    Returns:
        JSON 格式的探索结果
    """
    # 实现见 07-implementation.md
```

### 2.3 工具列表更新

```python
# langgraph_tools.py

LANGGRAPH_TOOLS = [
    # 现有工具
    search_content,
    locate_content,
    get_writing_context,
    analyze_content,
    smart_continue,
    smart_rewrite,
    smart_insert,
    apply_chapter_edit,
    create_chapter,
    update_chapter_title,
    delete_chapter,

    # 新增工具
    read_paragraph,      # 精确读取段落
    explore_content,     # 深度探索
]
```

---

## 3. Planning 集成

### 3.1 添加工具描述（在 tool_descriptions.py）

```python
# prompts/tool_descriptions.py

def _get_explore_tools_section() -> str:
    """探索工具描述"""
    return """
【探索工具 - 复杂任务使用】

- explore_content: 深度探索工具（get_writing_context 的增强版）
  参数:
    - work_id: 作品ID（必需）
    - target_task: 目标任务描述（必需）
    - max_rounds: 最大探索轮数（默认5）
  返回: {
    explore_summary,      # AI 分析
    chapters,            # 完整章节原文
    worldview,           # 世界观设定
    evidences,           # 搜索证据片段
    paragraphs           # 精确读取的段落
  }

  ✅ 使用场景:
    - 任务涉及多个章节的关联分析
    - 需要深入理解人物关系、情节发展
    - 搜索结果需要原文验证

  ⚠️ 与 get_writing_context 的对比:
    - get_writing_context: 一次性获取，适合简单任务
    - explore_content: 多轮探索，适合复杂任务

- read_paragraph: 精确读取段落原文
  参数:
    - work_id: 作品ID（必需）
    - chapter_order: 章节序号（必需）
    - paragraph_index: 段落索引（必需）
    - context_before: 向前读取段落数（默认2）
    - context_after: 向后读取段落数（默认2）
  返回: {chapter_title, paragraphs[{index, text, is_target}]}

  ✅ 使用场景:
    - 搜索结果片段太短，需要验证完整上下文
    - 需要精确读取某个段落的前后文
"""

# 更新 get_all_tools_description
def get_all_tools_description() -> str:
    return (
        _get_new_aggregated_tools_section() +
        _get_retrieval_tools_section() +
        _get_editor_tools_section() +
        _get_explore_tools_section() +  # 新增
        _get_read_tools_section() +
        _get_creative_tools_section() +
        _get_operation_tools_section() +
        _get_analysis_tools_section()
    )
```

### 3.2 AI 选择规则（现有逻辑不变）

AI 根据任务复杂度自主选择：

```
用户请求: "续写第6章"
├─ 简单情况（前5章内容已知）
│   → get_writing_context + smart_continue
│
└─ 复杂情况（需要深入理解人物关系）
    → explore_content + smart_continue
```

**不需要强制**"Planning 第一步永远是 explore_content"。

---

## 4. Execution 集成

### 4.1 Tool Executor 更新

```python
# execution/tool_executor.py

# 在 call_tool 方法中添加支持

async def call_tool(self, tool_name: str, tool_args: dict, state: dict) -> str:
    # ...现有逻辑...

    if tool_name == "explore_content":
        # 注入事件回调
        event_callback = state.get("flow_event_callback")
        tool_args["event_callback"] = event_callback
        return await explore_content.ainvoke(tool_args)

    if tool_name == "read_paragraph":
        return await read_paragraph.ainvoke(tool_args)

    # ...其他工具...
```

### 4.2 结果传递

Explore 的输出自动传递给后续任务：

```python
# 在 TaskRunner 中

async def execute_task(self, task: Task, context: dict) -> Any:
    if task.tool == "explore_content":
        result = await self.tool_executor.call_tool(
            "explore_content", task.params, context
        )
        # 保存结果，供后续任务使用
        context["explore_result"] = json.loads(result)
        return result

    elif task.tool in ["smart_continue", "smart_rewrite"]:
        # 如果有 Explore 结果，注入上下文
        if "explore_result" in context:
            task.params["context"] = self._build_context(context["explore_result"])
        return await self.tool_executor.call_tool(task.tool, task.params, context)
```

---

## 5. 事件集成

### 5.1 添加 explore_analysis 事件

```python
# stream/flow_events.py

class FlowEventBuilder:
    # ...现有方法...

    @staticmethod
    def explore_analysis(
        step_id: int,
        round_idx: int,
        reasoning: str,
        stats: Dict[str, int],
        sufficient: bool,
        next_actions: Optional[List[str]] = None
    ) -> dict:
        """构建 Explore AI 分析事件"""
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

### 5.2 工具图标映射

```python
# stream/flow_events.py

TOOL_ICONS = {
    # ...现有映射...

    "explore_content": "Scan",
    "read_paragraph": "FileText",
}
```

---

## 6. 文件结构

```
backend/app/services/agent/
├── tools/
│   ├── __init__.py
│   ├── analysis_tools.py       # 现有
│   ├── writing_tools.py        # 现有
│   ├── locate_tools.py         # 现有
│   └── explore_tools.py        # 新增：Explore 核心实现
│       ├── ContentExplorer     # 核心类
│       ├── ExploreState        # 状态管理
│       └── explore_content()   # 工具入口
│
├── langgraph_tools.py          # 修改：添加 read_paragraph
│
├── execution/
│   └── tool_executor.py        # 修改：添加工具调用支持
│
├── prompts/
│   └── planning_prompts.py     # 修改：添加工具描述
│
└── stream/
    └── flow_events.py          # 修改：添加 explore_analysis 事件
```

---

## 7. 数据流图

```
用户请求: "续写第6章，深入描写段融的性格变化"
    │
    ▼
┌─────────────────────────────────────────────────────────────────┐
│ Planning Agent                                                  │
│                                                                 │
│ AI 判断：涉及人物性格分析，需要深度探索                        │
│                                                                 │
│ → Task 1: explore_content(target="续写第6章，分析段融性格...")  │
│ → Task 2: smart_continue(chapter=6) [depends: 1]                │
└───────────────────────────────┬─────────────────────────────────┘
                                │
                                ▼
┌─────────────────────────────────────────────────────────────────┐
│ Execution - Task 1: explore_content                             │
│                                                                 │
│ ┌─────────────────────────────────────────────────────────┐    │
│ │ Explore Mini-Agent（复用现有工具）                       │    │
│ │                                                          │    │
│ │ Round 1:                                                 │    │
│ │   - get_writing_context(chapters="-3", worldview)        │    │
│ │   - search_content("段融性格")                           │    │
│ │                                                          │    │
│ │ AI 分析: 片段太短，需要验证                              │    │
│ │                                                          │    │
│ │ Round 2:                                                 │    │
│ │   - read_paragraph(chapter=3, para=18)                   │    │
│ │   - search_content("段融 同门")                          │    │
│ │                                                          │    │
│ │ AI 分析: 信息充足                                        │    │
│ └─────────────────────────────────────────────────────────┘    │
│                                                                 │
│ 输出: explore_result (保存到 context)                           │
└───────────────────────────────┬─────────────────────────────────┘
                                │
                                ▼
┌─────────────────────────────────────────────────────────────────┐
│ Execution - Task 2: smart_continue                              │
│                                                                 │
│ 从 context 注入 explore_result                                  │
│                                                                 │
│ smart_continue(chapter=6, context=explore_result)               │
│ → 生成续写内容                                                  │
└─────────────────────────────────────────────────────────────────┘
```

---

## 8. 改动清单总结

> ✅ **实际实现情况（2026-01-17 更新）**

### 后端（已实现）

| 文件 | 改动 | 代码量 | 状态 |
|------|------|--------|------|
| `tools/explore_tools.py` | 新增 | ~800行 | ✅ 已实现 |
| `langgraph_tools.py` | 添加 read_paragraph + explore_content 导入 | ~135行 | ✅ 已实现 |
| `prompts/tool_descriptions.py` | 添加工具描述 | ~50行 | ✅ 已实现 |
| `prompts/planning_prompts.py` | 添加 explore_content 使用指导 | ~15行 | ✅ 已实现 |
| `prompts/planning_examples.py` | 添加 explore_content 规划示例 | ~120行 | ✅ 已实现 |
| `execution/task_runner.py` | 添加 explore 结果处理 | ~40行 | ✅ 已实现 |
| `execution/tool_executor.py` | 添加 work_id 参数注入 + 降级支持 | ~50行 | ✅ 已实现 |
| `stream/flow_events.py` | 添加事件 + 图标 | ~80行 | ✅ 已实现 |
| `utils/tool_cache.py` | 段落级缓存 | ~80行 | ✅ 已实现 |

**后端实际完成**：~1370行（核心类 + 工具 + 事件 + 缓存 + 提示词 + 执行器）

### 前端（已实现）

| 文件 | 改动 | 代码量估计 | 状态 |
|------|------|------------|------|
| `src/services/agentApi.ts` | 添加 explore_round/explore_summary | ~30行 | ✅ 已实现 |
| `src/hooks/useAgentChat.ts` | 添加事件处理 | ~40行 | ✅ 已实现 |
| `src/hooks/useAgentChatStream.ts` | 添加事件处理 | ~40行 | ✅ 已实现 |
| `src/types/agent.ts` | 添加 Explore 类型定义 | ~100行 | ✅ 已实现 |
| `src/components/agent/ExecutionFlow/ExploreCard.tsx` | 添加流事件组件 | ~270行 | ✅ 已实现 |
| `src/components/agent/ExecutionFlow/index.tsx` | 添加 explore 渲染 | ~15行 | ✅ 已实现 |

**前端状态**：✅ 全部完成

### 实际代码量

| 类型 | 文档预估 | 实际情况 |
|------|---------|---------|
| 后端 | ~530行 | ~1370行（核心类 + 工具 + 事件 + 缓存 + 提示词 + 执行器） |
| 前端 | ~55行 | ~495行（事件处理 + UI 组件 + 类型定义） |
| 总计 | ~585行 | ~1865行 |

**实现状态**：✅ 全部完成（2026-01-17）
