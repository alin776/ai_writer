# Explore 核心循环实现

## 0. 设计更新说明

**基于 Review 报告的修正**：
- 复用现有工具（search_content、get_writing_context、locate_content）
- 只新增 read_paragraph 工具
- 融入现有 FlowEventBuilder 事件体系
- 使用 `.ainvoke()` 调用现有 @tool 装饰的工具

## 1. 整体流程

```
┌─────────────────────────────────────────────────────────┐
│                    ContentExplorer                       │
│                                                         │
│  1. 初始化                                              │
│     - 创建 ExploreState                                 │
│     - 创建 EventEmitter                                 │
│                                                         │
│  2. 主循环                                              │
│     ┌─────────────────────────────────────────────┐    │
│     │ while round_idx < max_rounds:               │    │
│     │                                             │    │
│     │   a. AI Plan - 决定本轮工具调用             │    │
│     │                                             │    │
│     │   b. 检查停止条件                           │    │
│     │      - sufficient?                          │    │
│     │      - converged?                           │    │
│     │      - timeout?                             │    │
│     │                                             │    │
│     │   c. 并行执行工具                           │    │
│     │                                             │    │
│     │   d. 更新状态                               │    │
│     │                                             │    │
│     │   e. 记录轮次                               │    │
│     └─────────────────────────────────────────────┘    │
│                                                         │
│  3. 生成 AI 分析                                        │
│                                                         │
│  4. 构建输出                                            │
└─────────────────────────────────────────────────────────┘
```

## 2. 核心类实现

```python
import asyncio
from dataclasses import dataclass
from typing import Optional, Callable, List, Dict, Any
from datetime import datetime

@dataclass
class ExploreConfig:
    """Explore 配置"""
    max_rounds: int = 5
    timeout_seconds: int = 60
    convergence_window: int = 2
    plan_model: str = "gpt-4o-mini"
    analysis_model: str = "gpt-4o"

class ContentExplorer:
    """
    AI 自主决策的内容探索器 - mini-agent

    封装复杂的多轮探索逻辑，对外表现为单个工具调用
    """

    def __init__(
        self,
        work_id: str,
        target_task: str,
        config: ExploreConfig = None,
        event_callback: Callable[[ExploreEvent], None] = None
    ):
        self.work_id = work_id
        self.target_task = target_task
        self.config = config or ExploreConfig()

        self.state = ExploreState()
        self.emitter = ExploreEventEmitter(callback=event_callback)
        self.start_time: Optional[datetime] = None

    async def execute(self) -> ExploreResult:
        """
        执行探索

        Returns:
            ExploreResult: 包含所有收集到的信息
        """
        self.start_time = datetime.now()

        # 1. 发送开始事件
        self.emitter.emit(ExploreEventType.EXPLORE_START, {
            "target_task": self.target_task,
            "max_rounds": self.config.max_rounds,
            "timeout_seconds": self.config.timeout_seconds
        })

        # 2. 主循环
        round_idx = 0
        stop_reason = ""

        while round_idx < self.config.max_rounds:
            round_idx += 1

            # 2a. 发送轮次开始事件
            self.emitter.emit(ExploreEventType.ROUND_START, {
                "round_idx": round_idx,
                "current_stats": self.state.get_stats()
            })

            # 2b. AI 规划本轮工具调用
            decision = await self._ai_plan(round_idx)

            # 2c. 发送规划事件
            self.emitter.emit(ExploreEventType.ROUND_PLAN, {
                "round_idx": round_idx,
                "reasoning": decision.reasoning,
                "tool_calls": [
                    {"tool": tc.tool, "params": tc.params}
                    for tc in decision.tool_calls
                ],
                "sufficient": decision.sufficient
            })

            # 2d. 检查停止条件
            should_stop, stop_reason = self._should_stop(decision, round_idx)
            if should_stop:
                # 发送充足性检查事件
                self.emitter.emit(ExploreEventType.SUFFICIENT_CHECK, {
                    "round_idx": round_idx,
                    "sufficient": decision.sufficient,
                    "reasoning": decision.reasoning,
                    "stats": self.state.get_stats()
                })
                break

            # 2e. 并行执行工具
            tool_results = await self._execute_tools_parallel(
                decision.tool_calls,
                round_idx
            )

            # 2f. 记录轮次
            explore_round = ExploreRound(
                round_idx=round_idx,
                reasoning=decision.reasoning,
                tool_calls=tool_results,
                new_evidences_count=self._count_new_evidences(round_idx),
                new_paragraphs_count=self._count_new_paragraphs(round_idx),
                sufficient=decision.sufficient,
                timestamp=datetime.now()
            )
            self.state.rounds.append(explore_round)

            # 2g. 发送轮次结束事件
            self.emitter.emit(ExploreEventType.ROUND_END, {
                "round_idx": round_idx,
                "new_evidences": explore_round.new_evidences_count,
                "new_paragraphs": explore_round.new_paragraphs_count,
                "duration_ms": self._calculate_round_duration(round_idx),
                "continue_to_next": True,
                "stop_reason": ""
            })

        # 3. 生成 AI 分析
        analysis = await self._generate_analysis()

        # 4. 计算总耗时
        total_duration_ms = int(
            (datetime.now() - self.start_time).total_seconds() * 1000
        )

        # 5. 发送结束事件
        self.emitter.emit(ExploreEventType.EXPLORE_END, {
            "total_rounds": len(self.state.rounds),
            "total_duration_ms": total_duration_ms,
            "stop_reason": stop_reason,
            "final_stats": self.state.get_stats(),
            "analysis": analysis
        })

        # 6. 构建输出
        return ExploreResult(
            evidences=self.state.evidences,
            paragraphs=self.state.paragraphs,
            chapters=self.state.chapters,
            worldview=self.state.worldview,
            analysis=analysis,
            stats=ExploreStats(
                total_evidences=len(self.state.evidences),
                total_paragraphs=len(self.state.paragraphs),
                total_chapters=len(self.state.chapters),
                total_worldview_items=sum(
                    len(items) for items in self.state.worldview.values()
                ),
                total_rounds=len(self.state.rounds),
                searched_queries=list(self.state.searched_queries)
            ),
            rounds=self.state.rounds,
            stop_reason=stop_reason,
            total_duration_ms=total_duration_ms
        )
```

## 3. AI 规划方法

```python
async def _ai_plan(self, round_idx: int) -> AIDecision:
    """
    调用 AI 决定本轮工具调用

    Args:
        round_idx: 当前轮次

    Returns:
        AIDecision: AI 的决策结果
    """
    # 构建 Prompt
    prompt = build_plan_prompt(self.target_task, self.state)

    # 调用 AI
    response = await call_llm(
        model=self.config.plan_model,
        messages=[{"role": "user", "content": prompt}],
        temperature=0.3  # 低温度，更稳定的决策
    )

    # 解析决策
    decision = parse_ai_decision(response)

    # 过滤已执行的工具调用（去重）
    decision.tool_calls = self._filter_duplicate_calls(decision.tool_calls)

    return decision

def _filter_duplicate_calls(
    self,
    tool_calls: List[ToolCallPlan]
) -> List[ToolCallPlan]:
    """过滤已执行的工具调用"""
    filtered = []

    for tc in tool_calls:
        if tc.tool == "search_content":
            query = tc.params.get("query", "")
            if self.state.should_search(query):
                filtered.append(tc)

        elif tc.tool == "read_paragraph":
            chapter = tc.params.get("chapter_order")
            para = tc.params.get("paragraph_index")
            if self.state.should_read_paragraph(chapter, para):
                filtered.append(tc)

        elif tc.tool == "get_chapter":
            orders = tc.params.get("chapter_orders", [])
            new_orders = [o for o in orders if self.state.should_read_chapter(o)]
            if new_orders:
                tc.params["chapter_orders"] = new_orders
                filtered.append(tc)

        elif tc.tool == "get_worldview":
            categories = tc.params.get("categories", [])
            new_categories = [
                c for c in categories
                if self.state.should_read_worldview(c)
            ]
            if new_categories:
                tc.params["categories"] = new_categories
                filtered.append(tc)

    return filtered
```

## 4. 并行执行工具

```python
async def _execute_tools_parallel(
    self,
    tool_calls: List[ToolCallPlan],
    round_idx: int
) -> List[ToolCall]:
    """
    并行执行工具调用

    Args:
        tool_calls: 要执行的工具列表
        round_idx: 当前轮次

    Returns:
        List[ToolCall]: 执行结果
    """
    async def execute_single(tc: ToolCallPlan) -> ToolCall:
        start = datetime.now()

        # 发送工具开始事件
        self.emitter.emit(ExploreEventType.TOOL_START, {
            "round_idx": round_idx,
            "tool_name": tc.tool,
            "params": tc.params
        })

        try:
            result = await self._call_tool(tc.tool, tc.params, round_idx)
            success = True
            result_summary = self._summarize_result(tc.tool, result)
        except Exception as e:
            result = {"error": str(e)}
            success = False
            result_summary = f"执行失败: {e}"

        duration_ms = int((datetime.now() - start).total_seconds() * 1000)

        # 发送工具结束事件
        self.emitter.emit(ExploreEventType.TOOL_END, {
            "round_idx": round_idx,
            "tool_name": tc.tool,
            "params": tc.params,
            "duration_ms": duration_ms,
            "success": success,
            "result_summary": result_summary
        })

        return ToolCall(
            tool_name=tc.tool,
            params=tc.params,
            result=result,
            duration_ms=duration_ms
        )

    # 并行执行所有工具
    results = await asyncio.gather(*[
        execute_single(tc) for tc in tool_calls
    ])

    return list(results)
```

## 5. 工具调用实现

```python
async def _call_tool(
    self,
    tool_name: str,
    params: Dict[str, Any],
    round_idx: int
) -> Any:
    """
    调用具体工具并更新状态

    Args:
        tool_name: 工具名称
        params: 工具参数
        round_idx: 当前轮次

    Returns:
        工具返回结果
    """
    if tool_name == "search_content":
        query = params["query"]
        limit = params.get("limit", 10)

        # 调用实际的搜索工具
        result = await search_analysis_fragments_tool(
            work_id=self.work_id,
            query=query,
            limit=limit
        )

        # 记录已搜索的 query
        self.state.record_search(query)

        # 存储搜索结果
        for item in result.results:
            self.state.add_evidence(item, query, round_idx)

            # 发送发现证据事件
            self.emitter.emit(ExploreEventType.EVIDENCE_FOUND, {
                "round_idx": round_idx,
                "evidence": {
                    "text": item.text,
                    "chapter_order": item.chapter_order,
                    "paragraph_index": item.paragraph_index,
                    "similarity": item.similarity,
                    "query": query
                }
            })

        return result

    elif tool_name == "read_paragraph":
        chapter_order = params["chapter_order"]
        paragraph_index = params["paragraph_index"]
        context_before = params.get("context_before", 2)
        context_after = params.get("context_after", 2)

        # 调用实际的读取工具
        result = await read_paragraph_tool(
            work_id=self.work_id,
            chapter_order=chapter_order,
            paragraph_index=paragraph_index,
            context_before=context_before,
            context_after=context_after
        )

        # 记录已读取的位置
        self.state.record_paragraph_read(chapter_order, paragraph_index)

        # 存储段落
        self.state.add_paragraph(result, round_idx)

        # 发送段落读取事件
        self.emitter.emit(ExploreEventType.PARAGRAPH_READ, {
            "round_idx": round_idx,
            "chapter_order": chapter_order,
            "chapter_title": result.chapter_title,
            "paragraph_index": paragraph_index,
            "text": result.paragraphs[0].text if result.paragraphs else "",
            "context_paragraphs": len(result.paragraphs)
        })

        return result

    elif tool_name == "get_chapter":
        chapter_orders = params["chapter_orders"]

        # 调用实际的读取工具
        result = await get_chapter_by_order_tool(
            work_id=self.work_id,
            chapter_orders=chapter_orders
        )

        # 记录并存储
        for chapter in result.chapters:
            self.state.record_chapter_read(chapter.order)
            self.state.add_chapter(chapter, round_idx)

            # 发送章节读取事件
            self.emitter.emit(ExploreEventType.CHAPTER_READ, {
                "round_idx": round_idx,
                "chapter_order": chapter.order,
                "chapter_title": chapter.title,
                "word_count": chapter.word_count
            })

        return result

    elif tool_name == "get_worldview":
        categories = params.get("categories")

        # 调用实际的读取工具
        result = await get_worldview_summary(
            work_id=self.work_id,
            categories=categories
        )

        # 记录并存储
        for category in (categories or ["all"]):
            self.state.record_worldview_read(category)

        for item in result.items:
            self.state.add_worldview_items([item], item.category)

        # 发送世界观加载事件
        self.emitter.emit(ExploreEventType.WORLDVIEW_LOADED, {
            "round_idx": round_idx,
            "category": categories[0] if categories else "all",
            "items_count": len(result.items),
            "items": [
                {"name": i.name, "description": i.description[:50]}
                for i in result.items[:5]
            ]
        })

        return result

    else:
        raise ValueError(f"Unknown tool: {tool_name}")
```

## 6. 停止条件检查

```python
def _should_stop(
    self,
    decision: AIDecision,
    round_idx: int
) -> tuple[bool, str]:
    """
    判断是否应该停止探索

    Returns:
        (should_stop, reason)
    """
    # 优先级 1: AI 判断信息充足
    if decision.sufficient:
        return True, "AI 判断信息充足"

    # 优先级 2: 没有更多工具可调用
    if not decision.tool_calls:
        return True, "没有更多工具可调用"

    # 优先级 3: 收敛检测
    if self.state.check_convergence(window=self.config.convergence_window):
        return True, f"连续 {self.config.convergence_window} 轮没有新增信息"

    # 优先级 4: 轮数上限
    if round_idx >= self.config.max_rounds:
        return True, f"达到最大轮数 {self.config.max_rounds}"

    # 优先级 5: 超时
    elapsed = (datetime.now() - self.start_time).total_seconds()
    if elapsed > self.config.timeout_seconds:
        return True, f"超时 {self.config.timeout_seconds}s"

    return False, ""
```

## 7. 生成 AI 分析

```python
async def _generate_analysis(self) -> str:
    """
    生成最终的 AI 分析总结

    Returns:
        分析文本
    """
    prompt = f"""
基于以下收集到的信息，为目标任务生成简洁的分析总结。

## 目标任务
{self.target_task}

## 收集到的信息

### 搜索证据 ({len(self.state.evidences)} 条)
{self._format_evidences_for_analysis()}

### 精确读取的段落 ({len(self.state.paragraphs)} 条)
{self._format_paragraphs_for_analysis()}

### 章节原文 ({len(self.state.chapters)} 章)
{self._format_chapters_for_analysis()}

### 世界观设定
{self._format_worldview_for_analysis()}

## 要求
1. 总结收集到的关键信息
2. 说明这些信息如何支撑目标任务
3. 如果有建议，简要提出
4. 保持简洁，不超过 300 字
"""

    response = await call_llm(
        model=self.config.analysis_model,
        messages=[{"role": "user", "content": prompt}],
        temperature=0.5
    )

    return response
```

## 8. 工具入口函数

```python
async def explore_content(
    work_id: str,
    target_task: str,
    max_rounds: int = 5,
    timeout_seconds: int = 60,
    event_callback: Callable[[ExploreEvent], None] = None
) -> ExploreResult:
    """
    Explore 工具入口函数

    Args:
        work_id: 作品 ID
        target_task: 目标任务描述
        max_rounds: 最大探索轮数
        timeout_seconds: 超时时间
        event_callback: 事件回调（用于流式推送）

    Returns:
        ExploreResult: 探索结果
    """
    config = ExploreConfig(
        max_rounds=max_rounds,
        timeout_seconds=timeout_seconds
    )

    explorer = ContentExplorer(
        work_id=work_id,
        target_task=target_task,
        config=config,
        event_callback=event_callback
    )

    return await explorer.execute()
```
