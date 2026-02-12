# -*- coding: utf-8 -*-
"""
四路径集成测试：验证 Explore V6 按 downstream_tool 分路获取上下文

测试场景：
  1. smart_insert  → _run_locate()  (reranker 精确定位段落)
  2. smart_rewrite → _run_locate()  (reranker 精确定位段落)
  3. smart_continue → _run_continue() (纯 DB 读章节末尾)
  4. 新建章节      → _run_create()  (LightRAG KG + 上一章末尾)

运行: cd backend && python -X utf8 tests/integration_four_paths.py
前提: PostgreSQL / LightRAG 均已启动，且数据库中已有导入的小说章节
"""

import asyncio
import json
import os
import sys
import time
from pathlib import Path

# ── 环境初始化 ──────────────────────────────────────────────
BACKEND_DIR = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(BACKEND_DIR))

# 从 backend/.env 加载环境变量
_env_file = BACKEND_DIR / ".env"
if _env_file.exists():
    for line in _env_file.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if line and not line.startswith("#") and "=" in line:
            key, _, val = line.partition("=")
            raw_val = val.strip()
            if "  #" in raw_val:
                raw_val = raw_val[:raw_val.index("  #")].strip()
            os.environ.setdefault(key.strip(), raw_val)

os.environ.setdefault("LIGHTRAG_BASE_URL", "http://127.0.0.1:9621")
os.environ.setdefault("LIGHTRAG_TIMEOUT_SECONDS", "300")


BOOK_PATH = Path(r"D:\Java\ai_writer\docs\Agent\real-book\一夕千悟，从杂役弟子开始.txt")
TEST_USER_ID = "79913e7e-d5cd-4e09-bce6-ca6639bd8456"
LIGHTRAG_WAIT_SECONDS = 90  # LightRAG 索引等待时间


def _header(title):
    print(f"\n{'='*70}")
    print(f"  {title}")
    print(f"{'='*70}")


def _step(step, msg):
    print(f"\n  [{step}] {msg}")


# ── 导入小说 ───────────────────────────────────────────────
async def import_novel() -> dict:
    """导入小说到 DB + LightRAG，返回 {work_id, chapters}"""
    _header("阶段 0：导入小说")

    if not BOOK_PATH.exists():
        raise FileNotFoundError(f"小说文件不存在: {BOOK_PATH}")

    raw_text = BOOK_PATH.read_text(encoding="utf-8")
    _step("0.1", f"读取文件: {BOOK_PATH.name} ({len(raw_text)} 字符)")

    from app.core.database import AsyncSessionLocal
    from app.services.import_service import ImportService
    from app.schemas.export import ImportOptions

    async with AsyncSessionLocal() as db:
        service = ImportService(db)
        options = ImportOptions(
            format="txt",
            create_new=True,
            include_worldview=False,
            include_guidelines=False,
        )
        _step("0.2", "调用 ImportService.import_work() ...")
        t0 = time.time()
        result, vectorize_jobs, import_context = await service.import_work(
            content=raw_text.encode("utf-8"),
            user_id=TEST_USER_ID,
            options=options,
        )
        elapsed = time.time() - t0

    work_id = str(result.work_id)
    _step("0.3", f"导入完成: work_id={work_id[:12]}..., chapters={result.chapters_created}, 耗时={elapsed:.1f}s")

    from app.services.chapter_service import ChapterService

    async with AsyncSessionLocal() as db:
        ch_service = ChapterService(db)
        ch_list = await ch_service.get_chapters_by_work(work_id)
    chapters = [
        {"id": str(ch.id), "order": ch.order, "title": ch.title or "", "word_count": ch.word_count or 0}
        for ch in (ch_list or [])
    ]

    _step("0.4", f"共 {len(chapters)} 章:")
    for ch in chapters[:6]:
        print(f"    第{ch['order']}章: {ch['title']} ({ch['word_count']}字)")
    if len(chapters) > 6:
        print(f"    ... 共 {len(chapters)} 章")

    _step("0.5", f"等待 LightRAG 后台索引 {LIGHTRAG_WAIT_SECONDS}s ...")
    await asyncio.sleep(LIGHTRAG_WAIT_SECONDS)

    return {"work_id": work_id, "chapters": chapters}

    return {"work_id": work_id, "chapters": chapters, "title": work_title}


# ── 通用运行函数 ────────────────────────────────────────────
async def run_explore(work_id: str, prompt: str, downstream_tool: str, chapter_scope=None) -> dict:
    """运行 ExploreV6，注入 downstream_tool"""
    from app.services.agent.tools.explore_v6 import ExploreV6

    retrieval_intent = {
        "goal": prompt,
        "entities": [],
        "downstream_tool": downstream_tool,
    }
    if chapter_scope:
        retrieval_intent["constraints"] = {"chapter_scope": chapter_scope}

    v6 = ExploreV6(
        work_id=work_id,
        target_task=prompt,
        retrieval_intent=retrieval_intent,
    )

    t0 = time.time()
    result = await v6.run()
    elapsed = time.time() - t0

    return {"result": result, "elapsed": elapsed}


def print_result_summary(result: dict, elapsed: float, label: str):
    """打印结果摘要"""
    evidences = result.get("evidences", [])
    locate_targets = result.get("locate_targets", [])
    stats = result.get("stats", {})
    stop_reason = result.get("stop_reason", "?")
    ctx = result.get("context_for_task", "")

    print(f"    耗时: {elapsed:.2f}s")
    print(f"    stop_reason: {stop_reason}")
    print(f"    evidences: {len(evidences)} 条")
    print(f"    locate_targets: {len(locate_targets)} 个")
    print(f"    context_for_task: {len(ctx)} 字符")

    if stats.get("query"):
        print(f"    query: {stats['query'][:60]}")
    if stats.get("downstream_tool"):
        print(f"    downstream_tool: {stats['downstream_tool']}")

    # 打印 evidence 摘要
    for i, ev in enumerate(evidences[:5]):
        src = ev.get("source_type", "?")
        cid = (ev.get("chapter_id") or "")[:8]
        co = ev.get("chapter_order")
        pi = ev.get("paragraph_index")
        text_preview = (ev.get("text") or "")[:80].replace("\n", " ")
        print(f"    evidence[{i}]: src={src} ch={co or '?'} para={pi} | {text_preview}...")
    if len(evidences) > 5:
        print(f"    ... 共 {len(evidences)} 条")

    # 打印 locate_targets
    for i, lt in enumerate(locate_targets[:3]):
        co = lt.get("chapter_order")
        pi = lt.get("paragraph_index")
        nid = lt.get("node_id") or ""
        text_preview = (lt.get("text") or "")[:50]
        print(f"    locate_target[{i}]: ch={co} para={pi} nid={nid[:12]} | {text_preview}...")


# ── 测试 1：smart_insert → _run_locate ────────────────────
async def test_smart_insert(work_id: str, chapters: list):
    _header("测试 1：smart_insert → _run_locate (reranker 定位)")

    # 选第1章，模拟"在段融吞噬器灵之后插入一段内心独白"
    prompt = "在第1章段融吞噬器灵成功之后插入一段他的内心独白"
    _step("1.1", f"Prompt: {prompt}")
    _step("1.2", "downstream_tool=smart_insert, chapter_scope=[1]")

    data = await run_explore(work_id, prompt, "smart_insert", chapter_scope=[1])
    result, elapsed = data["result"], data["elapsed"]

    _step("1.3", "结果:")
    print_result_summary(result, elapsed, "smart_insert")

    # 验证
    _step("1.4", "验证:")
    evidences = result.get("evidences", [])
    locate_targets = result.get("locate_targets", [])

    checks = []
    checks.append(("有 evidence", len(evidences) > 0))
    checks.append(("stop_reason 非错误", "失败" not in result.get("stop_reason", "")))

    has_locate = any(
        lt.get("paragraph_index") is not None or lt.get("node_id")
        for lt in locate_targets
    )
    checks.append(("有段落级 locate_target", has_locate))
    checks.append(("locate_targets 恰好 1 个", len(locate_targets) == 1))

    reranker_src = any(e.get("source_type") == "reranker_locate" for e in evidences)
    fallback_src = any(e.get("source_type") == "lightrag_fallback" for e in evidences)
    checks.append(("使用 reranker 或 fallback", reranker_src or fallback_src))

    for label, passed in checks:
        print(f"    {'PASS' if passed else 'FAIL'}: {label}")

    return all(p for _, p in checks)


# ── 测试 2：smart_rewrite → _run_locate ──────────────────
async def test_smart_rewrite(work_id: str, chapters: list):
    _header("测试 2：smart_rewrite → _run_locate (reranker 定位)")

    prompt = "改写第2章中赵穆教授羚羊献食的段落，让描写更生动"
    _step("2.1", f"Prompt: {prompt}")
    _step("2.2", "downstream_tool=smart_rewrite, chapter_scope=[2]")

    data = await run_explore(work_id, prompt, "smart_rewrite", chapter_scope=[2])
    result, elapsed = data["result"], data["elapsed"]

    _step("2.3", "结果:")
    print_result_summary(result, elapsed, "smart_rewrite")

    _step("2.4", "验证:")
    evidences = result.get("evidences", [])
    locate_targets = result.get("locate_targets", [])

    checks = []
    checks.append(("有 evidence", len(evidences) > 0))
    checks.append(("stop_reason 非错误", "失败" not in result.get("stop_reason", "")))

    has_locate = any(
        lt.get("paragraph_index") is not None or lt.get("node_id")
        for lt in locate_targets
    )
    checks.append(("有段落级 locate_target", has_locate))
    checks.append(("locate_targets ≤ 1 个（不触发 ambiguous）", len(locate_targets) <= 1))

    for label, passed in checks:
        print(f"    {'PASS' if passed else 'FAIL'}: {label}")

    return all(p for _, p in checks)


# ── 测试 3：smart_continue → _run_continue ───────────────
async def test_smart_continue(work_id: str, chapters: list):
    _header("测试 3：smart_continue → _run_continue (纯 DB 读取)")

    # 选第2章续写
    target_order = min(3, len(chapters))
    prompt = f"续写第{target_order}章的内容"
    _step("3.1", f"Prompt: {prompt}")
    _step("3.2", f"downstream_tool=smart_continue, chapter_scope=[{target_order}]")

    data = await run_explore(work_id, prompt, "smart_continue", chapter_scope=[target_order])
    result, elapsed = data["result"], data["elapsed"]

    _step("3.3", "结果:")
    print_result_summary(result, elapsed, "smart_continue")

    _step("3.4", "验证:")
    evidences = result.get("evidences", [])
    locate_targets = result.get("locate_targets", [])
    stats = result.get("stats", {})

    checks = []
    checks.append(("有 evidence", len(evidences) > 0))
    checks.append(("stop_reason='续写上下文就绪'", result.get("stop_reason") == "续写上下文就绪"))

    # 续写路径不需要 locate_targets
    checks.append(("locate_targets 为空（续写不需要段落定位）", len(locate_targets) == 0))

    # 检查是否有 db_chapter_tail 类型
    has_tail = any(e.get("source_type") == "db_chapter_tail" for e in evidences)
    checks.append(("有当前章末尾内容 (db_chapter_tail)", has_tail))

    # 应该有 context_for_task 且内容较长
    ctx_len = len(result.get("context_for_task", ""))
    checks.append((f"context_for_task 内容充分 ({ctx_len}字符)", ctx_len > 100))

    # 不应该有 query（不调用 LLM 生成查询）
    has_query = bool(stats.get("query"))
    checks.append(("未调用 LLM 生成查询（纯 DB）", not has_query))

    # 耗时应该很短（纯 DB 读取）
    checks.append((f"耗时 < 5s（纯 DB 读取应很快）({elapsed:.2f}s)", elapsed < 5.0))

    for label, passed in checks:
        print(f"    {'PASS' if passed else 'FAIL'}: {label}")

    return all(p for _, p in checks)


# ── 测试 4：新建章节 → _run_create ────────────────────────
async def test_create_chapter(work_id: str, chapters: list):
    _header("测试 4：新建章节 → _run_create (LightRAG KG + 上一章末尾)")

    prompt = "新建下一章，段融在武功初成后首次外出走镖的情节"
    _step("4.1", f"Prompt: {prompt}")
    _step("4.2", "downstream_tool=(空), 走默认 _run_create 路径")

    data = await run_explore(work_id, prompt, "", chapter_scope=None)
    result, elapsed = data["result"], data["elapsed"]

    _step("4.3", "结果:")
    print_result_summary(result, elapsed, "create_chapter")

    _step("4.4", "验证:")
    evidences = result.get("evidences", [])
    locate_targets = result.get("locate_targets", [])
    stats = result.get("stats", {})

    checks = []
    checks.append(("有 evidence", len(evidences) > 0))
    checks.append(("stop_reason='新建章节上下文就绪'", result.get("stop_reason") == "新建章节上下文就绪"))

    # 应该有上一章末尾内容
    has_prev_tail = any(e.get("source_type") == "db_prev_chapter_tail" for e in evidences)
    checks.append(("有上一章末尾内容 (db_prev_chapter_tail)", has_prev_tail))

    # 应该有 LightRAG KG 内容
    has_kg = any(e.get("source_type") == "lightrag_kg" for e in evidences)
    checks.append(("有 LightRAG KG 内容 (lightrag_kg)", has_kg))

    # 应该生成了查询
    has_query = bool(stats.get("query"))
    checks.append(("生成了 LightRAG 查询", has_query))

    # context_for_task 应该有内容
    ctx_len = len(result.get("context_for_task", ""))
    checks.append((f"context_for_task 内容充分 ({ctx_len}字符)", ctx_len > 100))

    for label, passed in checks:
        print(f"    {'PASS' if passed else 'FAIL'}: {label}")

    return all(p for _, p in checks)


# ── 评估总结 ────────────────────────────────────────────────
def print_evaluation(results: dict):
    _header("评估总结")

    all_pass = True
    for name, passed in results.items():
        status = "PASS" if passed else "FAIL"
        print(f"  [{status}] {name}")
        if not passed:
            all_pass = False

    print()
    if all_pass:
        print("  所有场景测试通过")
    else:
        failed = [n for n, p in results.items() if not p]
        print(f"  {len(failed)} 个场景未通过: {', '.join(failed)}")


# ── 主函数 ──────────────────────────────────────────────────
async def main():
    _header("四路径集成测试：Explore V6 按 downstream_tool 分路")

    # 导入小说
    work_info = await import_novel()
    work_id = work_info["work_id"]
    chapters = work_info["chapters"]

    if len(chapters) < 2:
        print("  作品章节数不足 2 章，无法完成所有测试")
        return

    # 运行四个测试
    results = {}

    try:
        results["smart_insert → _run_locate"] = await test_smart_insert(work_id, chapters)
    except Exception as exc:
        print(f"  ERROR: {exc}")
        import traceback; traceback.print_exc()
        results["smart_insert → _run_locate"] = False

    try:
        results["smart_rewrite → _run_locate"] = await test_smart_rewrite(work_id, chapters)
    except Exception as exc:
        print(f"  ERROR: {exc}")
        import traceback; traceback.print_exc()
        results["smart_rewrite → _run_locate"] = False

    try:
        results["smart_continue → _run_continue"] = await test_smart_continue(work_id, chapters)
    except Exception as exc:
        print(f"  ERROR: {exc}")
        import traceback; traceback.print_exc()
        results["smart_continue → _run_continue"] = False

    try:
        results["新建章节 → _run_create"] = await test_create_chapter(work_id, chapters)
    except Exception as exc:
        print(f"  ERROR: {exc}")
        import traceback; traceback.print_exc()
        results["新建章节 → _run_create"] = False

    # 评估总结
    print_evaluation(results)


if __name__ == "__main__":
    asyncio.run(main())
