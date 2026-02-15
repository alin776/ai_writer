# -*- coding: utf-8 -*-
"""
真实环境集成测试：LightRAG only_need_context + chunk→paragraph 定位

前置条件：
1. LightRAG 服务运行在 127.0.0.1:9621
2. PostgreSQL 数据库运行且有小说数据
3. 运行: cd backend && python -X utf8 tests/integration_lightrag_context.py
"""

import asyncio
import os
import sys
import time
from pathlib import Path

# 让 import 能找到 backend/app
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
os.environ.setdefault("LIGHTRAG_BASE_URL", "http://127.0.0.1:9621")
os.environ.setdefault("LIGHTRAG_TIMEOUT_SECONDS", "300")

WORK_ID = "e6590250-38df-4db2-aadb-de87ee3ca640"
DB_URL = "postgresql+asyncpg://novelaide:novelaide_password@localhost:5432/novelaide"


def section(title: str):
    print(f"\n{'='*60}")
    print(f"  {title}")
    print(f"{'='*60}")


async def test_1_lightrag_health():
    """测试 1: LightRAG 服务连通性"""
    section("测试 1: LightRAG 服务连通性")
    import httpx
    try:
        async with httpx.AsyncClient(timeout=5) as client:
            resp = await client.get("http://127.0.0.1:9621/health")
            print(f"  状态码: {resp.status_code}")
            assert resp.status_code == 200
            print("  ✓ 通过")
    except Exception as e:
        print(f"  ⚠ 健康检查异常（不阻断）: {e}")


async def test_2_raw_only_need_context():
    """测试 2: 直接调用 /query + only_need_context=True 并验证返回格式"""
    section("测试 2: LightRAG /query only_need_context=True")
    import httpx

    payload = {"query": "主角修炼突破过程", "mode": "mix", "top_k": 5, "only_need_context": True}
    print(f"  请求: {payload}")

    t0 = time.time()
    async with httpx.AsyncClient(timeout=30) as client:
        resp = await client.post("http://127.0.0.1:9621/query", json=payload)
    elapsed = time.time() - t0

    assert resp.status_code == 200, f"HTTP {resp.status_code}"
    data = resp.json()
    response_text = str(data.get("response") or "")

    has_dc = "Document Chunks" in response_text
    has_entity = "Knowledge Graph" in response_text
    print(f"  状态码: {resp.status_code}, 耗时: {elapsed:.2f}s, 长度: {len(response_text)}")
    print(f"  包含 Knowledge Graph: {has_entity}")
    print(f"  包含 Document Chunks: {has_dc}")

    assert len(response_text) > 100, "响应过短"
    assert has_dc, "响应中没有 Document Chunks 部分"
    print(f"  ✓ 通过 — {elapsed:.2f}s")
    return response_text


async def test_3_parse_context_chunks(response_text: str):
    """测试 3: _parse_context_chunks 解析真实返回"""
    section("测试 3: _parse_context_chunks 提取真实小说 chunks")

    from app.services.agent.retrieval.fact_retrieval_gateway import FactRetrievalGateway
    chunks = FactRetrievalGateway._parse_context_chunks(response_text)

    print(f"  提取 {len(chunks)} 个 chunks")
    for i, chunk in enumerate(chunks[:5]):
        preview = chunk[:100].replace('\n', ' ')
        print(f"  [{i}] ({len(chunk)}字): {preview}...")

    assert len(chunks) >= 1, "未提取出任何 chunk"
    # 验证提取的是小说原文而非 Knowledge Graph 实体
    has_chinese = any(any('\u4e00' <= c <= '\u9fff' for c in ch) for ch in chunks)
    assert has_chinese, "chunks 中无中文内容"
    print(f"\n  ✓ 通过 — {len(chunks)} 个 chunks，含中文小说原文")
    return chunks


async def test_4_gateway_full_pipeline():
    """测试 4: FactRetrievalGateway.query_lightrag_raw() 完整流水线"""
    section("测试 4: Gateway.query_lightrag_raw() 完整流水线")

    from app.services.agent.retrieval.fact_retrieval_gateway import FactRetrievalGateway
    gateway = FactRetrievalGateway()
    print(f"  work_id: {WORK_ID}")
    print(f"  timeout: {gateway.lightrag_timeout_seconds}s, mode: {gateway.lightrag_mode}")

    t0 = time.time()
    results = await gateway.query_lightrag_raw(
        "查找主角段融修炼突破的关键情节",
        top_k=10,
    )
    elapsed = time.time() - t0

    print(f"\n  耗时: {elapsed:.2f}s")
    print(f"  hits: {len(results)}")

    assert len(results) > 0, "无结果"

    context_count = sum(1 for r in results if r.get("retrieval_mode") == "lightrag_context")
    print(f"  lightrag_context 结果: {context_count}/{len(results)}")

    for i, r in enumerate(results[:5]):
        ch = r.get("chapter_order")
        pi = r.get("paragraph_index")
        mode = r.get("retrieval_mode")
        text_preview = str(r.get("text", ""))[:80].replace('\n', ' ')
        print(f"  [{i}] ch={ch} p={pi} mode={mode}: {text_preview}...")

    assert context_count > 0, "未走 lightrag_context 路径"
    print(f"\n  ✓ 通过 — {elapsed:.2f}s, {context_count} context chunks")
    return results


async def test_5_chunk_to_chapter_matching():
    """测试 5: chunk→chapter 子串匹配（真实 DB）"""
    section("测试 5: chunk→chapter 子串匹配")

    from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
    from sqlalchemy.orm import sessionmaker
    from sqlalchemy import text as sa_text

    engine = create_async_engine(DB_URL)
    async_session = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

    async with async_session() as session:
        sql = sa_text(
            'SELECT c."order" AS chapter_order, c.id AS chapter_id, c.title AS chapter_title, '
            "ci.plain_text "
            "FROM chapter_content_indexes ci JOIN chapters c ON ci.chapter_id = c.id "
            "WHERE c.work_id = :work_id "
            'ORDER BY c."order" LIMIT 5'
        )
        row_result = await session.execute(sql, {"work_id": WORK_ID})
        chapters = []
        for row in row_result:
            chapters.append({
                "chapter_order": row.chapter_order,
                "chapter_id": str(row.chapter_id),
                "chapter_title": str(row.chapter_title or ""),
                "plain_text": str(row.plain_text or ""),
            })
    await engine.dispose()

    print(f"  加载 {len(chapters)} 个章节")
    assert len(chapters) > 0, "无章节数据"

    for ch in chapters[:3]:
        print(f"  第{ch['chapter_order']}章 {ch['chapter_title']}: {len(ch['plain_text'])}字")

    # 模拟 chunk：取第一个章节的一段文字
    test_ch = chapters[0]
    plain = test_ch["plain_text"]
    # 从文本中段取 80 字符作为模拟 chunk
    mid = len(plain) // 3
    fake_chunk = plain[mid:mid+80].strip()
    print(f"\n  模拟 chunk（取自第{test_ch['chapter_order']}章中间）:")
    print(f"  \"{fake_chunk}\"")

    # 子串匹配
    matched = False
    for ch in chapters:
        pos = ch["plain_text"].find(fake_chunk)
        if pos >= 0:
            paras_before = ch["plain_text"][:pos].split("\n")
            est_pi = len([p for p in paras_before if p.strip()])
            print(f"\n  匹配成功: 第{ch['chapter_order']}章 \"{ch['chapter_title']}\"")
            print(f"  估算段落索引: {est_pi}")
            matched = True
            break

    assert matched, "子串匹配失败"
    print(f"  ✓ 通过")


async def test_6_end_to_end():
    """测试 6: 端到端 — Gateway query_lightrag_raw + chunk locate"""
    section("测试 6: 端到端 Gateway + chunk→chapter 定位")

    from app.services.agent.retrieval.fact_retrieval_gateway import FactRetrievalGateway
    from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
    from sqlalchemy.orm import sessionmaker
    from sqlalchemy import text as sa_text

    # 第一步：Gateway 检索
    gateway = FactRetrievalGateway()
    t0 = time.time()
    results = await gateway.query_lightrag_raw(
        "段融吞噬器灵的关键场景",
        top_k=10,
    )
    retrieve_elapsed = time.time() - t0

    unlocated = [r for r in results if r.get("chapter_order") is None]
    print(f"  Gateway 检索: {retrieve_elapsed:.2f}s, {len(results)} 条结果, {len(unlocated)} 条未定位")

    if not unlocated:
        print("  所有结果已有定位，跳过 locate")
        print(f"  ✓ 通过")
        return

    # 第二步：加载章节数据并子串匹配
    engine = create_async_engine(DB_URL)
    async_session = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

    t1 = time.time()
    async with async_session() as session:
        sql = sa_text(
            'SELECT c."order" AS chapter_order, c.id AS chapter_id, c.title AS chapter_title, '
            "ci.plain_text "
            "FROM chapter_content_indexes ci JOIN chapters c ON ci.chapter_id = c.id "
            "WHERE c.work_id = :work_id "
            'ORDER BY c."order"'
        )
        row_result = await session.execute(sql, {"work_id": WORK_ID})
        chapter_cache = []
        for row in row_result:
            plain = str(row.plain_text or "")
            if plain:
                chapter_cache.append({
                    "chapter_order": row.chapter_order,
                    "chapter_id": str(row.chapter_id),
                    "chapter_title": str(row.chapter_title or ""),
                    "plain_text": plain,
                })
    await engine.dispose()
    db_elapsed = time.time() - t1

    print(f"  DB 加载: {db_elapsed:.2f}s, {len(chapter_cache)} 个章节")

    # 子串匹配（规范化全角空格 + 跳过乱码首字符）
    located = 0
    for item in unlocated:
        chunk_text = str(item.get("text") or "")
        # 跳过开头乱码字符
        clean_start = 0
        for ci, c in enumerate(chunk_text[:20]):
            if '\u4e00' <= c <= '\u9fff' or c in '，。！？、；：""''（）《》' or c.isascii():
                clean_start = ci
                break
        search_key = chunk_text[clean_start:clean_start + 80].strip()
        search_key_norm = search_key.replace('\u3000', '').replace('\t', '')
        if len(search_key_norm) < 6:
            continue
        for ch in chapter_cache:
            pos = ch["plain_text"].find(search_key_norm)
            if pos >= 0:
                item["chapter_order"] = ch["chapter_order"]
                item["chapter_id"] = ch["chapter_id"]
                item["chapter_title"] = ch["chapter_title"]
                paras_before = ch["plain_text"][:pos].split("\n")
                item["paragraph_index"] = len([p for p in paras_before if p.strip()])
                located += 1
                break

    total_elapsed = retrieve_elapsed + db_elapsed
    print(f"\n  定位结果: {located}/{len(unlocated)} 成功")
    print(f"  总耗时: {total_elapsed:.2f}s")

    print(f"\n  最终结果（前 5 条）:")
    for i, r in enumerate(results[:5]):
        ch = r.get("chapter_order")
        pi = r.get("paragraph_index")
        title = r.get("chapter_title", "")
        loc = f"第{ch}章{title} 第{pi}段" if ch is not None else "⚠未定位"
        text_preview = str(r.get("text", ""))[:60].replace('\n', ' ')
        print(f"  [{i}] {loc}: {text_preview}...")

    assert located > 0, f"所有 {len(unlocated)} 个 chunk 均匹配失败"
    print(f"\n  ✓ 通过 — 总耗时 {total_elapsed:.2f}s, 定位 {located}/{len(unlocated)}")


async def main():
    print("=" * 60)
    print("  LightRAG only_need_context 真实环境集成测试")
    print(f"  work_id: {WORK_ID}")
    print("=" * 60)

    passed = 0
    failed = 0
    tests = [
        ("test_1", test_1_lightrag_health, []),
        ("test_2", test_2_raw_only_need_context, []),
        ("test_3", None, []),  # depends on test_2
        ("test_4", test_4_gateway_full_pipeline, []),
        ("test_5", test_5_chunk_to_chapter_matching, []),
        ("test_6", test_6_end_to_end, []),
    ]

    # 1
    try:
        await test_1_lightrag_health()
        passed += 1
    except Exception as e:
        print(f"  ✗ 失败: {e}")
        failed += 1

    # 2
    response_text = None
    try:
        response_text = await test_2_raw_only_need_context()
        passed += 1
    except Exception as e:
        print(f"  ✗ 失败: {e}")
        failed += 1

    # 3
    if response_text:
        try:
            await test_3_parse_context_chunks(response_text)
            passed += 1
        except Exception as e:
            print(f"  ✗ 失败: {e}")
            failed += 1
    else:
        print("\n  跳过测试 3（依赖测试 2）")

    # 4
    try:
        await test_4_gateway_full_pipeline()
        passed += 1
    except Exception as e:
        print(f"  ✗ 失败: {e}")
        failed += 1

    # 5
    try:
        await test_5_chunk_to_chapter_matching()
        passed += 1
    except Exception as e:
        print(f"  ✗ 失败: {e}")
        failed += 1

    # 6
    try:
        await test_6_end_to_end()
        passed += 1
    except Exception as e:
        print(f"  ✗ 失败: {e}")
        failed += 1

    section(f"结果: {passed} 通过, {failed} 失败")
    if failed:
        sys.exit(1)
    print("  全部通过!")


if __name__ == "__main__":
    asyncio.run(main())
