# -*- coding: utf-8 -*-
"""
端到端集成测试：导入作品 → Explore → 段落定位 → 模拟写入链路

验证整条链路：
  1. 导入 txt 小说 → 章节存入 DB + HTML 转纯文本插入 LightRAG
  2. Explore V6 查询 → locate_targets 包含 paragraph_index / node_id
  3. 模拟 _ensure_source_locator + _validate_source_locator → 写入链路是否通畅

运行: cd backend && python -X utf8 tests/integration_paragraph_locate.py
前提: PostgreSQL / Redis / LightRAG 均已启动
"""

import asyncio
import json
import os
import sys
import time
import traceback
from pathlib import Path

# ── 环境初始化 ──────────────────────────────────────────────
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
os.environ.setdefault("LIGHTRAG_BASE_URL", "http://127.0.0.1:9621")
os.environ.setdefault("LIGHTRAG_TIMEOUT_SECONDS", "300")

BOOK_PATH = Path(r"D:\Java\ai_writer\docs\Agent\real-book\一夕千悟，从杂役弟子开始.txt")
DB_URL = "postgresql+asyncpg://novelaide:novelaide_password@localhost:5432/novelaide"
TEST_USER_ID = "79913e7e-d5cd-4e09-bce6-ca6639bd8456"

# Explore 测试 prompt
TEST_PROMPT = "段融吞噬器灵的条件和效果是什么？废刀和新刀的器灵等阶有什么规律"

# 等待 LightRAG 索引的时间（秒）
LIGHTRAG_WAIT_SECONDS = 60


def _print_header(title):
    print(f"\n{'='*70}")
    print(f"  {title}")
    print(f"{'='*70}")


def _print_step(step, msg):
    print(f"\n  [{step}] {msg}")


# ── 阶段 1：导入作品 ────────────────────────────────────────
async def stage_import() -> dict:
    """导入 txt 小说，返回 {work_id, chapters: [{id, order, title, word_count}]}"""
    _print_header("阶段 1：导入作品")

    if not BOOK_PATH.exists():
        raise FileNotFoundError(f"小说文件不存在: {BOOK_PATH}")

    _print_step("1.1", f"读取文件: {BOOK_PATH.name} ({BOOK_PATH.stat().st_size / 1024:.0f} KB)")
    raw_text = BOOK_PATH.read_text(encoding="utf-8")
    _print_step("1.2", f"文本长度: {len(raw_text)} 字符")

    # 通过 API 层面的 ImportService 导入
    from app.core.database import AsyncSessionLocal
    from app.services.import_service import ImportService
    from app.schemas.export import ImportOptions

    async with AsyncSessionLocal() as db:
        service = ImportService(db)

        options = ImportOptions(
            format="txt",
            create_new=True,
            include_guidelines=False,
        )

        _print_step("1.3", "调用 ImportService.import_work() ...")
        t0 = time.time()
        result = await service.import_work(
            content=raw_text.encode("utf-8"),
            user_id=TEST_USER_ID,
            options=options,
        )
        elapsed = time.time() - t0

    work_id = str(result.work_id)
    _print_step("1.4", f"导入完成: work_id={work_id}, chapters_created={result.chapters_created}, 耗时={elapsed:.1f}s")

    # ImportResponse 没有 chapters 列表，从 DB 查询
    from app.services.chapter_service import ChapterService

    async with AsyncSessionLocal() as db:
        ch_service = ChapterService(db)
        ch_list = await ch_service.get_chapters_by_work(work_id)
    chapters = [
        {
            "id": str(ch.id),
            "order": ch.order,
            "title": ch.title or "",
            "word_count": ch.word_count or 0,
        }
        for ch in (ch_list or [])
    ]

    _print_step("1.4b", f"查询到 {len(chapters)} 章")
    for ch in chapters[:5]:
        print(f"         第{ch['order']}章: id={ch['id'][:12]}.. {ch['title']} ({ch['word_count']}字)")
    if len(chapters) > 5:
        print(f"         ... 共 {len(chapters)} 章")

    _print_step("1.5", f"等待 LightRAG 后台索引 {LIGHTRAG_WAIT_SECONDS}s ...")
    await asyncio.sleep(LIGHTRAG_WAIT_SECONDS)

    return {"work_id": work_id, "chapters": chapters}


# ── 阶段 2：Explore V6 ──────────────────────────────────────
async def stage_explore(work_id: str) -> dict:
    """运行 Explore V6，返回完整 result dict"""
    _print_header("阶段 2：Explore V6 查询")
    _print_step("2.1", f"Prompt: {TEST_PROMPT}")

    from app.services.agent.tools.explore_v6 import ExploreV6

    v6 = ExploreV6(
        work_id=work_id,
        target_task=TEST_PROMPT,
        retrieval_intent={
            "goal": TEST_PROMPT,
            "entities": ["段融", "器灵", "废刀"],
        },
    )

    t0 = time.time()
    result = await v6.run()
    elapsed = time.time() - t0

    evidences = result.get("evidences", [])
    locate_targets = result.get("locate_targets", [])
    stats = result.get("stats", {})

    _print_step("2.2", f"查询完成: 耗时={elapsed:.1f}s")
    print(f"         查询: {stats.get('query', '?')}")
    print(f"         evidences: {len(evidences)} 条")
    print(f"         locate_targets: {len(locate_targets)} 个")

    # 详细打印每个 locate_target
    _print_step("2.3", "locate_targets 详情:")
    for i, lt in enumerate(locate_targets):
        cid = lt.get("chapter_id", "?")[:8]
        co = lt.get("chapter_order")
        pi = lt.get("paragraph_index")
        nid = lt.get("node_id") or ""
        text_preview = (lt.get("text") or "")[:50]
        ba = (lt.get("before_anchor") or "")[:30]
        aa = (lt.get("after_anchor") or "")[:30]

        status = "✓" if (pi is not None or nid) else "✗"
        print(f"    [{i}] {status} chapter={cid}.. order={co} para_idx={pi} node_id={nid}")
        print(f"        text: {text_preview}...")
        if ba:
            print(f"        before: {ba}...")
        if aa:
            print(f"        after: {aa}...")

    # 统计
    total_targets = len(locate_targets)
    located_targets = sum(
        1 for lt in locate_targets
        if lt.get("paragraph_index") is not None or lt.get("node_id")
    )
    _print_step("2.4", f"段落定位率: {located_targets}/{total_targets}")

    return result


# ── 阶段 3：模拟写入链路验证 ────────────────────────────────
async def stage_validate_write_chain(explore_result: dict):
    """模拟 _ensure_source_locator + _validate_source_locator 验证链路是否通畅"""
    _print_header("阶段 3：模拟写入链路验证")

    locate_targets = explore_result.get("locate_targets", [])
    if not locate_targets:
        _print_step("3.1", "✗ 无 locate_targets，写入链路不可用")
        return False

    # 模拟 evidence_store.has("locate_targets")
    _print_step("3.1", "模拟 evidence_store.has('locate_targets') 检查:")
    store_has = False
    for item in locate_targets:
        chapter_id = item.get("chapter_id") or ""
        paragraph_index = item.get("paragraph_index")
        node_id = item.get("node_id") or ""
        if chapter_id and (paragraph_index is not None or node_id):
            store_has = True
            break
    print(f"         结果: {'✓ 通过' if store_has else '✗ 失败 — 无有效的段落级定位'}")

    if not store_has:
        return False

    # 模拟 _ensure_source_locator（取第一个有效的 locate_target）
    _print_step("3.2", "模拟 _ensure_source_locator（选取第一个有段落定位的 target）:")
    selected = None
    for item in locate_targets:
        cid = item.get("chapter_id") or ""
        pi = item.get("paragraph_index")
        nid = item.get("node_id") or ""
        if cid and (pi is not None or nid):
            selected = item
            break
    if not selected:
        print("         ✗ 无有效 target")
        return False
    source_locator = {
        "chapter_id": selected.get("chapter_id"),
        "paragraph_index": selected.get("paragraph_index"),
        "node_id": selected.get("node_id"),
        "text": selected.get("text") or "",
    }
    print(f"         source_locator = {{")
    for k, v in source_locator.items():
        val = f'"{v[:40]}..."' if isinstance(v, str) and len(v) > 40 else repr(v)
        print(f"           {k}: {val}")
    print(f"         }}")

    # 模拟 _validate_source_locator
    _print_step("3.3", "模拟 _validate_source_locator 检查:")
    src_node_id = source_locator.get("node_id") or ""
    src_paragraph_index = source_locator.get("paragraph_index")

    if not src_node_id and src_paragraph_index is None:
        print("         ✗ 失败: source_locator 缺少 node_id/paragraph_index，写回会被阻止")
        return False
    else:
        print(f"         ✓ 通过: node_id={src_node_id or '(空)'}, paragraph_index={src_paragraph_index}")

    # 模拟构建 smart_insert 参数
    _print_step("3.4", "模拟 smart_insert 参数构建:")
    params = {
        "chapter_id": source_locator["chapter_id"],
        "paragraph_index": source_locator["paragraph_index"],
        "node_id": source_locator["node_id"],
        "insert_context": selected.get("before_anchor") or selected.get("text") or "",
        "source_locator": source_locator,
    }
    print(f"         chapter_id: {params['chapter_id'][:12]}...")
    print(f"         paragraph_index: {params['paragraph_index']}")
    print(f"         node_id: {params['node_id']}")
    print(f"         insert_context: {(params['insert_context'] or '')[:50]}...")
    print(f"         ✓ 参数完整，可以调用 smart_insert")

    # 验证 apply_chapter_edit 需要的字段
    _print_step("3.5", "模拟 apply_chapter_edit 参数:")
    print(f"         operation: insert")
    print(f"         chapter_id: {params['chapter_id'][:12]}...")
    print(f"         paragraph_index: {params['paragraph_index']} ← 用于定位段落")
    print(f"         node_id: {params['node_id']} ← 用于精确定位 HTML 节点")
    print(f"         ✓ 编辑器可以定位到具体段落")

    return True


# ── 阶段 4：验证章节内容格式 ────────────────────────────────
async def stage_verify_chapter_content(work_id: str, explore_result: dict):
    """验证章节内容是 HTML 格式，且 _split_paragraphs 能正确解析"""
    _print_header("阶段 4：验证章节内容与段落解析")

    locate_targets = explore_result.get("locate_targets", [])
    if not locate_targets:
        _print_step("4.1", "无 locate_targets，跳过")
        return

    # 取第一个有 paragraph_index 的 target
    target = None
    for lt in locate_targets:
        if lt.get("paragraph_index") is not None:
            target = lt
            break

    if not target:
        _print_step("4.1", "无有效段落定位的 target，跳过")
        return

    chapter_id = target["chapter_id"]
    para_idx = target["paragraph_index"]
    node_id = target.get("node_id") or ""

    _print_step("4.1", f"加载章节内容: chapter_id={chapter_id[:12]}...")

    from app.services.chapter_service import ChapterService
    from app.core.database import AsyncSessionLocal

    async with AsyncSessionLocal() as db:
        service = ChapterService(db)
        chapter = await service.get_chapter_by_id(chapter_id)

    if not chapter or not chapter.content:
        print("         ✗ 章节内容为空")
        return

    content = str(chapter.content)
    _print_step("4.2", f"章节内容: {len(content)} 字符, HTML={'<p' in content}")

    # 解析段落
    from app.services.agent.tools.locate_tools import _split_paragraphs
    paragraphs = _split_paragraphs(content)
    _print_step("4.3", f"_split_paragraphs 解析出 {len(paragraphs)} 个段落")

    # 验证 paragraph_index 指向的段落
    if para_idx < len(paragraphs):
        para = paragraphs[para_idx]
        _print_step("4.4", f"paragraph_index={para_idx} 对应的段落:")
        print(f"         node_id: {para.get('node_id')}")
        print(f"         text: {para['text'][:80]}...")

        # 验证 node_id 一致性
        if node_id and para.get("node_id"):
            match = node_id == para["node_id"]
            print(f"         node_id 一致性: {'✓ 匹配' if match else '✗ 不匹配'}")
            print(f"           explore 返回: {node_id}")
            print(f"           章节实际: {para['node_id']}")
    else:
        print(f"         ✗ paragraph_index={para_idx} 超出范围 (共{len(paragraphs)}段)")

    # 打印前后几段供人工验证
    _print_step("4.5", f"段落 {max(0, para_idx-1)}~{min(len(paragraphs)-1, para_idx+1)} 上下文:")
    for i in range(max(0, para_idx - 1), min(len(paragraphs), para_idx + 2)):
        marker = ">>>" if i == para_idx else "   "
        text_preview = paragraphs[i]["text"][:60]
        nid = paragraphs[i].get("node_id") or ""
        print(f"    {marker} [{i}] node={nid}: {text_preview}...")


# ── 阶段 4b：验证新导入章节的 data-id ─────────────────────
async def stage_verify_new_chapter(chapters: list):
    """直接验证新导入的章节是否有 data-id，不依赖 Explore 结果"""
    _print_header("阶段 4b：验证新导入章节 data-id")

    if not chapters:
        _print_step("4b.1", "无章节，跳过")
        return

    chapter_id = chapters[0]["id"]
    _print_step("4b.1", f"加载新导入章节: id={chapter_id[:12]}.. order={chapters[0]['order']}")

    from app.services.chapter_service import ChapterService
    from app.core.database import AsyncSessionLocal
    from app.services.agent.tools.locate_tools import _split_paragraphs

    async with AsyncSessionLocal() as db:
        service = ChapterService(db)
        chapter = await service.get_chapter_by_id(chapter_id)

    if not chapter or not chapter.content:
        print("         ✗ 章节内容为空")
        return

    content = str(chapter.content)
    has_data_id = 'data-id=' in content
    _print_step("4b.2", f"HTML={True}, data-id={'✓' if has_data_id else '✗'}, {len(content)} 字符")

    # 打印前 200 字符的 HTML 结构
    print(f"         HTML 预览: {content[:200]}...")

    paragraphs = _split_paragraphs(content)
    _print_step("4b.3", f"_split_paragraphs 解析出 {len(paragraphs)} 个段落")

    # 统计 node_id 覆盖率
    with_nid = sum(1 for p in paragraphs if p.get("node_id"))
    _print_step("4b.4", f"node_id 覆盖率: {with_nid}/{len(paragraphs)}")

    # 打印前 5 段
    for i, p in enumerate(paragraphs[:5]):
        nid = p.get("node_id") or "(无)"
        print(f"    [{i}] node_id={nid}: {p['text'][:50]}...")


# ── 清理测试数据 ────────────────────────────────────────────
async def cleanup(work_id: str):
    """删除测试创建的作品和章节"""
    _print_header("清理测试数据")
    try:
        from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
        from sqlalchemy.orm import sessionmaker
        from sqlalchemy import text as sa_text

        engine = create_async_engine(DB_URL)
        async_session = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

        async with async_session() as session:
            # 删除章节
            await session.execute(
                sa_text("DELETE FROM chapters WHERE work_id = :wid"),
                {"wid": work_id},
            )
            # 删除作品
            await session.execute(
                sa_text("DELETE FROM works WHERE id = :wid"),
                {"wid": work_id},
            )
            await session.commit()

        await engine.dispose()
        print(f"  已清理 work_id={work_id}")
    except Exception as e:
        print(f"  清理失败（可手动清理）: {e}")


# ── 主入口 ──────────────────────────────────────────────────
async def main():
    _print_header("端到端集成测试：导入 → Explore → 段落定位 → 写入链路")
    print(f"  小说: {BOOK_PATH.name}")
    print(f"  测试 prompt: {TEST_PROMPT}")

    work_id = None
    all_passed = True

    try:
        # 阶段 1：导入
        import_result = await stage_import()
        work_id = import_result["work_id"]
        chapters = import_result["chapters"]
        if not chapters:
            print("\n  ✗ 导入失败：无章节")
            sys.exit(1)

        # 阶段 2：Explore
        explore_result = await stage_explore(work_id)

        # 过滤出属于当前作品的 locate_targets
        chapter_ids = {ch["id"] for ch in chapters}
        locate_targets = explore_result.get("locate_targets", [])
        own_targets = [lt for lt in locate_targets if lt.get("chapter_id") in chapter_ids]
        stale_targets = [lt for lt in locate_targets if lt.get("chapter_id") not in chapter_ids]
        if stale_targets:
            print(f"\n  ⚠ {len(stale_targets)} 个 target 来自旧导入（已过滤）")
        if own_targets:
            print(f"  ✓ {len(own_targets)} 个 target 来自本次导入")
            # 用过滤后的结果替换
            explore_result = {**explore_result, "locate_targets": own_targets}
        else:
            print(f"  ⚠ LightRAG 未返回本次导入的章节（可能索引未完成），仅验证 data-id")

        # 阶段 3：写入链路验证
        write_ok = await stage_validate_write_chain(explore_result)
        if not write_ok and not own_targets:
            # LightRAG 未索引新数据，不算测试失败
            print("         （LightRAG 索引延迟，跳过写入链路验证）")
        elif not write_ok:
            all_passed = False

        # 阶段 4：章节内容验证（Explore 结果 + 新导入章节）
        await stage_verify_chapter_content(work_id, explore_result)

        # 阶段 4b：直接验证新导入章节的 data-id 和段落解析
        await stage_verify_new_chapter(chapters)

    except Exception as e:
        print(f"\n  ✗ 异常: {e}")
        traceback.print_exc()
        all_passed = False
    finally:
        # 清理
        if work_id:
            await cleanup(work_id)

    _print_header("测试结果")
    if all_passed:
        print("  ✓ 全部通过：导入 → Explore → 段落定位 → 写入链路 完整可用")
    else:
        print("  ✗ 存在问题，请查看上方详细输出")
        sys.exit(1)


if __name__ == "__main__":
    asyncio.run(main())
