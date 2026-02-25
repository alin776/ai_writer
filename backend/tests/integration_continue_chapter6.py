# -*- coding: utf-8 -*-
"""
集成测试：续写第6章完整 Agent 链路

验证 WritingAgentGraph.chat_with_planning() 从 Plan → Explore → SmartContinue → Response
的完整链路是否工作正常。

运行: cd backend && python -X utf8 tests/integration_continue_chapter6.py
前提: PostgreSQL / Redis / LightRAG 均已启动
"""

import asyncio
import json
import os
import re
import sys
import time
import traceback
from pathlib import Path

# ── 环境初始化 ──────────────────────────────────────────────
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
os.environ.setdefault("LIGHTRAG_BASE_URL", "http://127.0.0.1:9621")
os.environ.setdefault("LIGHTRAG_TIMEOUT_SECONDS", "300")

WORK_ID = "e6590250-38df-4db2-aadb-de87ee3ca640"
DB_URL = "postgresql+asyncpg://novelaide:novelaide_password@localhost:5432/novelaide"

USER_PROMPT = (
    '续写第6章开头，需要衔接以下所有线索：'
    '段融已经通过吞噬赵穆牛尾刀器灵获得了入门级五虎群羊刀经验，'
    '并在梦中完成了\u201c一夕千悟\u201d的消化过程；'
    '但他的身体素质仍然羸弱，右臂肌肉差点拉伤；'
    '他正在尝试通过站桩捕捉内息但始终摸不到门道；'
    '同时赵穆已经发现自己的刀\u201c人刀相应\u201d感觉消失了却不知原因；'
    '考核还有半个月就要开始了。'
)

# 预期关键词——续写内容中至少应命中其中若干
EXPECT_KEYWORDS = ["段融", "器灵", "赵穆", "站桩", "考核"]


# ── 查询最后一章（第5章）的 chapter_id ──────────────────────
async def get_last_chapter_id() -> tuple:
    """返回 (chapter_id, chapter_order) — 取最新章节作为续写起点"""
    from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
    from sqlalchemy.orm import sessionmaker
    from sqlalchemy import text as sa_text

    engine = create_async_engine(DB_URL)
    async_session = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

    async with async_session() as session:
        sql = sa_text(
            'SELECT c.id, c."order" FROM chapters c '
            'WHERE c.work_id = :work_id '
            'ORDER BY c."order" DESC LIMIT 1'
        )
        row = (await session.execute(sql, {"work_id": WORK_ID})).first()

    await engine.dispose()

    if row is None:
        raise RuntimeError("数据库中无任何章节，请检查 work_id 和章节数据")
    return str(row.id), row.order


# ── 事件收集器 ──────────────────────────────────────────────
class EventCollector:
    """收集 chat_with_planning 回调事件"""

    def __init__(self):
        self.plan_data = None
        self.task_starts = []
        self.task_progresses = []
        self.task_dones = []
        self.contents = []
        self.flow_events = []

    async def on_plan(self, plan_data):
        self.plan_data = plan_data
        tasks = plan_data.get("tasks", []) if isinstance(plan_data, dict) else []
        print(f"  [plan] 收到规划，共 {len(tasks)} 个任务")
        for i, t in enumerate(tasks):
            title = t.get("title", t.get("tool", "?"))
            print(f"    task[{i}]: {title}")

    async def on_task_start(self, task):
        self.task_starts.append(task)
        title = task.get("title", task.get("tool", "?")) if isinstance(task, dict) else str(task)
        print(f"  [task_start] {title}")

    async def on_task_progress(self, task, progress):
        self.task_progresses.append({"task": task, "progress": progress})

    async def on_task_done(self, task, result):
        self.task_dones.append({"task": task, "result": result})
        title = task.get("title", task.get("tool", "?")) if isinstance(task, dict) else str(task)
        # 摘要打印 result
        if isinstance(result, dict):
            keys = list(result.keys())[:8]
            print(f"  [task_done] {title} → keys={keys}")
        elif isinstance(result, str):
            print(f"  [task_done] {title} → str(len={len(result)}) preview={result[:80]}...")
        else:
            print(f"  [task_done] {title} → type={type(result).__name__}")

    async def on_content(self, data):
        self.contents.append(data)

    async def on_flow_event(self, event):
        self.flow_events.append(event)
        etype = event.get("type", "?") if isinstance(event, dict) else "?"
        if etype in ("step_start", "step_complete", "knowledge_loaded", "output_ready"):
            desc = ""
            if isinstance(event, dict):
                desc = event.get("data", {}).get("title", "") or event.get("data", {}).get("description", "")
            print(f"  [flow] {etype}: {desc[:60]}")


# ── 验证逻辑 ────────────────────────────────────────────────
def run_checks(collector: EventCollector, agent_result: dict) -> list:
    """返回错误列表（空 = 全部通过）"""
    errors = []

    # 1. Plan 包含 explore + continue 任务
    plan = collector.plan_data
    if plan is None:
        errors.append("未收到 plan 事件")
    else:
        tasks = plan.get("tasks", []) if isinstance(plan, dict) else []
        tool_names = [t.get("tool", "") for t in tasks if isinstance(t, dict)]
        has_explore = any("explore" in n.lower() for n in tool_names)
        has_continue = any("continue" in n.lower() or "smart" in n.lower() or "write" in n.lower()
                          for n in tool_names)
        if not has_explore:
            errors.append(f"Plan 中缺少 explore 任务 (tools={tool_names})")
        if not has_continue:
            errors.append(f"Plan 中缺少 continue/write 任务 (tools={tool_names})")
        if len(tasks) < 2:
            errors.append(f"Plan 任务数不足 ({len(tasks)} < 2)")

    # 2. 检查 task_results 中 explore 的 raw_result
    #    on_task_done 回调传的是 result_text（字符串），
    #    但 agent_result["task_results"] 含有 raw_result（结构化数据）。
    explore_result = None
    task_results = agent_result.get("task_results", [])
    for tr in task_results:
        if not isinstance(tr, dict):
            continue
        tool_name = tr.get("tool", "")
        raw = tr.get("raw_result")
        if "explore" in tool_name.lower() and isinstance(raw, dict):
            explore_result = raw
            break

    # 如果 task_results 中没找到，也尝试在 task_done 回调中查找
    if explore_result is None:
        for td in collector.task_dones:
            task = td.get("task", {})
            result = td.get("result", {})
            tool_name = task.get("tool", "") if isinstance(task, dict) else ""
            if "explore" in tool_name.lower() and isinstance(result, dict):
                explore_result = result
                break

    if explore_result is None:
        # 降级检查: explore 任务至少执行了且产出了文本
        explore_ran = any(
            "explore" in (td.get("task", {}).get("tool", "") if isinstance(td.get("task"), dict) else "").lower()
            for td in collector.task_dones
        )
        if explore_ran:
            print("  [check] explore 任务已执行，但 raw_result 不可用（结构化检查跳过）")
        else:
            errors.append("未找到 explore 任务结果")
    else:
        # evidences 非空
        evidences = explore_result.get("evidences", [])
        if len(evidences) == 0:
            errors.append("ExploreV6 evidences 为空")
        else:
            print(f"  [check] evidences 数量: {len(evidences)}")

        # chapters 是 list（非 dict）
        chapters = explore_result.get("chapters")
        if chapters is not None:
            if not isinstance(chapters, list):
                errors.append(f"ExploreV6 chapters 不是 list，而是 {type(chapters).__name__}")
            else:
                print(f"  [check] chapters 格式正确 (list, len={len(chapters)})")

        # locate_targets 是 list
        locate_targets = explore_result.get("locate_targets")
        if locate_targets is not None:
            if not isinstance(locate_targets, list):
                errors.append(f"ExploreV6 locate_targets 不是 list，而是 {type(locate_targets).__name__}")
            elif len(locate_targets) == 0:
                errors.append("ExploreV6 locate_targets 为空")
            else:
                print(f"  [check] locate_targets 数量: {len(locate_targets)}")

    # 3. 最终 Agent 响应非空且包含中文
    response_text = agent_result.get("response", "")
    if not response_text or len(response_text.strip()) == 0:
        errors.append("Agent 最终响应为空")
    else:
        has_chinese = bool(re.search(r'[\u4e00-\u9fff]', response_text))
        if not has_chinese:
            errors.append("Agent 最终响应不包含中文")
        else:
            print(f"  [check] 响应长度: {len(response_text)} 字符")

    # 4. 关键词命中检查（在响应 + 所有 content 事件中查找）
    all_text = response_text
    for c in collector.contents:
        if isinstance(c, str):
            all_text += c
        elif isinstance(c, dict):
            all_text += str(c.get("content", "")) + str(c.get("text", ""))

    kw_hits = {kw: kw in all_text for kw in EXPECT_KEYWORDS}
    hit_count = sum(1 for v in kw_hits.values() if v)
    print(f"  [check] 关键词命中: {kw_hits} ({hit_count}/{len(EXPECT_KEYWORDS)})")
    if hit_count == 0:
        errors.append(f"无任何关键词命中: {kw_hits}")

    return errors


# ── 主流程 ──────────────────────────────────────────────────
async def main():
    print("=" * 60)
    print("  集成测试：续写第6章完整 Agent 链路")
    print(f"  work_id: {WORK_ID}")
    print("=" * 60)

    # 1. 查询最后一章 chapter_id（续写起点）
    print("\n[1/4] 查询最后一章 chapter_id ...")
    chapter_id, chapter_order = await get_last_chapter_id()
    print(f"  最后一章: 第{chapter_order}章, chapter_id = {chapter_id}")
    print(f"  续写目标: 第{chapter_order + 1}章")

    # 2. 创建 Agent 实例
    print("\n[2/4] 创建 Agent 实例 ...")
    from app.services.ai.langchain_ai_service import LangChainAIService
    from app.services.agent.langgraph_agent import WritingAgentGraph

    ai_service = LangChainAIService(enable_model_selector=True)
    agent = WritingAgentGraph(ai_service)
    print("  Agent 创建成功")

    # 3. 调用 chat_with_planning
    #    使用唯一 conversation_id 避免复用上次对话历史
    import uuid
    conversation_id = f"test_{uuid.uuid4().hex[:12]}"
    print(f"\n[3/4] 调用 chat_with_planning ...")
    print(f"  conversation_id: {conversation_id}")
    print(f"  Prompt: {USER_PROMPT[:60]}...")
    collector = EventCollector()

    t0 = time.time()
    try:
        result = await agent.chat_with_planning(
            message=USER_PROMPT,
            work_id=WORK_ID,
            chapter_id=chapter_id,
            conversation_id=conversation_id,
            context={"tool_policy": "auto"},
            on_plan=collector.on_plan,
            on_task_start=collector.on_task_start,
            on_task_progress=collector.on_task_progress,
            on_task_done=collector.on_task_done,
            on_content=collector.on_content,
            on_flow_event=collector.on_flow_event,
        )
    except Exception as e:
        elapsed = time.time() - t0
        print(f"\n  ✗ Agent 执行异常 ({elapsed:.1f}s): {e}")
        traceback.print_exc()
        sys.exit(1)

    elapsed = time.time() - t0
    print(f"\n  Agent 执行完成，耗时 {elapsed:.1f}s")

    # 打印响应摘要
    response_text = result.get("response", "")
    print(f"  响应长度: {len(response_text)} 字符")
    if response_text:
        preview = response_text[:200].replace('\n', ' ')
        print(f"  响应前200字: {preview}...")

    # 4. 验证
    print(f"\n[4/4] 验证结果 ...")
    print(f"  事件统计: plan={'有' if collector.plan_data else '无'}, "
          f"task_start={len(collector.task_starts)}, "
          f"task_done={len(collector.task_dones)}, "
          f"content={len(collector.contents)}, "
          f"flow_event={len(collector.flow_events)}")

    # 打印 task_results 结构摘要（用于诊断）
    task_results = result.get("task_results", [])
    print(f"  task_results 数量: {len(task_results)}")
    for i, tr in enumerate(task_results):
        if isinstance(tr, dict):
            tool = tr.get("tool", "?")
            status = tr.get("status", "?")
            has_raw = "raw_result" in tr
            raw_type = type(tr.get("raw_result")).__name__ if has_raw else "N/A"
            print(f"    [{i}] tool={tool} status={status} has_raw={has_raw} raw_type={raw_type}")

    errors = run_checks(collector, result)

    # ── 汇总 ────────────────────────────────────────────────
    print(f"\n{'='*60}")
    if errors:
        print(f"  ✗ 失败 — 共 {len(errors)} 个问题:")
        for i, err in enumerate(errors):
            print(f"    {i+1}. {err}")
        print(f"{'='*60}")
        sys.exit(1)
    else:
        print(f"  ✓ 全部通过 — 耗时 {elapsed:.1f}s")
        print(f"{'='*60}")


if __name__ == "__main__":
    asyncio.run(main())
