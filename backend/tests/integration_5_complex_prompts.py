# -*- coding: utf-8 -*-
"""
5 个复杂 Prompt 真实环境压测：验证 only_need_context + chunk→chapter 定位

运行: cd backend && python -X utf8 tests/integration_5_complex_prompts.py
"""

import asyncio
import os
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
os.environ.setdefault("LIGHTRAG_BASE_URL", "http://127.0.0.1:9621")
os.environ.setdefault("LIGHTRAG_TIMEOUT_SECONDS", "300")

WORK_ID = "e6590250-38df-4db2-aadb-de87ee3ca640"
DB_URL = "postgresql+asyncpg://novelaide:novelaide_password@localhost:5432/novelaide"

# ========== 5 个复杂 Prompt ==========

COMPLEX_PROMPTS = [
    {
        "id": 1,
        "name": "跨章节因果链 — 器灵吞噬的完整规则推演",
        "query_intent": "段融吞噬器灵的完整规则体系：吞噬条件（精神力等级）、吞噬效果（刀法经验传承）、器灵等阶与器物品质的关系（为何废刀等阶高于好刀）、以及器灵成长与岁月经历的关联",
        "must_have": ["器灵等阶", "吞噬", "精神力", "废刀"],
        "focus_terms": ["器灵等阶", "吞噬要求", "精神力", "废刀", "好刀", "岁月", "经历"],
        # 预期应命中：第1章（读取器灵数据面板）、第5章（器灵规则推演）
        "expect_keywords_in_text": ["器灵等阶", "吞噬"],
    },
    {
        "id": 2,
        "name": "多人物交叉 — 段融、赵穆、孔斌三人的能力对比与关系网",
        "query_intent": "对比段融、赵穆、孔斌三人的武功水平和关系：赵穆作为实习镖师的刀法水平和对杂役弟子的态度，孔斌作为天赋最佳弟子的表现和小团体地位，段融通过吞噬器灵获得的隐藏实力与表面上的弱者形象之间的反差",
        "must_have": ["段融", "赵穆", "孔斌"],
        "focus_terms": ["段融", "赵穆", "孔斌", "李充", "张征", "学徒", "天赋", "吞噬"],
        # 预期应命中：第1章（赵穆让段融擦刀）、第2章（赵穆教学+孔斌等三人）、第3章（李充嘲讽+孔斌制止）
        "expect_keywords_in_text": ["赵穆", "孔斌"],
    },
    {
        "id": 3,
        "name": "隐藏伏笔追踪 — 赵穆察觉刀中器灵消失的后续影响",
        "query_intent": "段融吞噬赵穆牛尾刀的器灵后，赵穆晚上练功时发现'人刀相应'的感觉消失、刀变得不顺手的具体描写，以及这个伏笔对段融身份暴露风险的暗示。同时追踪段融吞噬后'脑中被塞进东西'的迟钝状态到梦中消化经验的完整过程",
        "must_have": ["赵穆", "器灵", "人刀相应", "消失"],
        "focus_terms": ["赵穆", "牛尾刀", "人刀相应", "顺手", "器灵", "消失", "脑中", "融化", "梦境", "五虎群羊刀"],
        # 预期应命中：第2章（赵穆发现异常）、第2章（段融脑中迟钝）、第3章（梦中消化）
        "expect_keywords_in_text": ["赵穆", "牛尾刀"],
    },
    {
        "id": 4,
        "name": "世界观架构还原 — 太一门宗门体制与底层武者生存链",
        "query_intent": "还原小说的世界观架构：九州大陆由八大宗门统治，太一门掌管青州，县令是外门弟子，武功秘籍传承决定权力格局。同时追踪底层武者的生存链条：杂役弟子→学徒→实习镖师→镖师的晋升体系，以及月钱从六十文到三钱银子的经济基础",
        "must_have": ["太一门", "青州", "宗门"],
        "focus_terms": ["太一门", "九州", "宗门", "青州", "县令", "外门弟子", "杂役弟子", "学徒", "镖师", "月钱", "六十文", "三钱银子"],
        # 预期应命中：第5章（太一门+九州）、第4章（月钱+晋升体系）、第1章（杂役弟子处境）
        "expect_keywords_in_text": ["太一门", "宗门"],
    },
    {
        "id": 5,
        "name": "关键事件精确定位 — 许儒虎案件的完整情报链",
        "query_intent": "定位许儒虎事件的完整信息链：许儒虎是太一门叛徒和外门弟子身份、奸污同门的罪行、在青州四府十八郡流窜多年、重伤后藏身勾栏院被解道寒捕头发现、搏斗中重锁刺透肩胛骨关入地牢、杨震和解雷受命看守、以及宗门将派人提走处决",
        "must_have": ["许儒虎", "太一门", "解道寒"],
        "focus_terms": ["许儒虎", "太一门", "叛徒", "奸污", "通缉", "解道寒", "捕头", "杨震", "解雷", "地牢", "肩胛骨", "宗门"],
        # 预期应命中：第5章（杨震讲述许儒虎完整故事）
        "expect_keywords_in_text": ["许儒虎"],
    },
]


async def load_chapter_cache():
    """加载章节数据用于子串匹配"""
    from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
    from sqlalchemy.orm import sessionmaker
    from sqlalchemy import text as sa_text

    engine = create_async_engine(DB_URL)
    async_session = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)
    chapter_cache = []
    async with async_session() as session:
        sql = sa_text(
            'SELECT c."order" AS chapter_order, c.id AS chapter_id, c.title AS chapter_title, '
            "ci.plain_text "
            "FROM chapter_content_indexes ci JOIN chapters c ON ci.chapter_id = c.id "
            "WHERE c.work_id = :work_id "
            'ORDER BY c."order"'
        )
        rows = await session.execute(sql, {"work_id": WORK_ID})
        for row in rows:
            plain = str(row.plain_text or "")
            if plain:
                chapter_cache.append({
                    "chapter_order": row.chapter_order,
                    "chapter_id": str(row.chapter_id),
                    "chapter_title": str(row.chapter_title or ""),
                    "plain_text": plain,
                })
    await engine.dispose()
    return chapter_cache


def locate_chunks(results, chapter_cache):
    """对未定位 chunks 做子串匹配"""
    located = 0
    for item in results:
        if item.get("chapter_order") is not None:
            continue
        chunk_text = str(item.get("text") or "")
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
                paras = ch["plain_text"][:pos].split("\n")
                item["paragraph_index"] = len([p for p in paras if p.strip()])
                located += 1
                break
    return located


async def run_single_prompt(prompt_cfg, gateway, chapter_cache):
    """运行单个复杂 prompt 测试"""
    pid = prompt_cfg["id"]
    name = prompt_cfg["name"]
    print(f"\n{'─'*60}")
    print(f"  Prompt {pid}: {name}")
    print(f"{'─'*60}")

    t0 = time.time()
    results = await gateway.query_lightrag_raw(
        prompt_cfg["query_intent"],
        top_k=15,
    )
    retrieve_elapsed = time.time() - t0

    success = len(results) > 0

    # 子串匹配定位
    t1 = time.time()
    located = locate_chunks(results, chapter_cache)
    locate_elapsed = time.time() - t1
    total_elapsed = retrieve_elapsed + locate_elapsed

    # 统计
    total = len(results)
    context_count = sum(1 for r in results if r.get("retrieval_mode") == "lightrag_context")
    located_count = sum(1 for r in results if r.get("chapter_order") is not None)
    chapters_hit = sorted(set(
        r.get("chapter_order") for r in results if isinstance(r.get("chapter_order"), int)
    ))

    # 关键词命中检查
    expect_kws = prompt_cfg.get("expect_keywords_in_text", [])
    all_text = " ".join(str(r.get("text", "")) for r in results)
    kw_hits = {kw: kw in all_text for kw in expect_kws}

    # 输出
    print(f"  检索耗时: {retrieve_elapsed:.2f}s | 定位耗时: {locate_elapsed:.2f}s | 总计: {total_elapsed:.2f}s")
    print(f"  success={success} | 结果数={total} | context模式={context_count} | 定位成功={located_count}")
    print(f"  命中章节: {chapters_hit if chapters_hit else '无'}")
    print(f"  关键词命中: {kw_hits}")

    print(f"\n  结果明细:")
    for i, r in enumerate(results[:8]):
        ch = r.get("chapter_order")
        pi = r.get("paragraph_index")
        mode = r.get("retrieval_mode", "?")
        matched = r.get("matched_keywords", [])
        text_preview = str(r.get("text", ""))[:70].replace('\n', ' ')
        if ch is not None:
            loc = f"第{ch}章第{pi}段"
        else:
            loc = "⚠未定位"
        print(f"  [{i}] {loc} [{mode}] kw={matched}")
        print(f"       {text_preview}...")

    # 判定
    errors = []
    if not success:
        errors.append("检索失败")
    if total == 0:
        errors.append("无结果")
    if context_count == 0:
        errors.append("未走 context 模式")
    if located_count == 0 and total > 0:
        errors.append("全部未定位")
    for kw, hit in kw_hits.items():
        if not hit:
            errors.append(f"关键词 '{kw}' 未命中")

    if errors:
        print(f"\n  ✗ 问题: {'; '.join(errors)}")
        return False
    else:
        print(f"\n  ✓ 通过 — {total_elapsed:.2f}s, {located_count}/{total} 定位, 章节 {chapters_hit}")
        return True


async def main():
    print("=" * 60)
    print("  5 个复杂 Prompt 压力测试")
    print(f"  work_id: {WORK_ID}")
    print("=" * 60)

    from app.services.agent.retrieval.fact_retrieval_gateway import FactRetrievalGateway
    gateway = FactRetrievalGateway()

    # 预加载章节数据
    chapter_cache = await load_chapter_cache()
    print(f"\n  预加载 {len(chapter_cache)} 个章节")

    passed = 0
    failed = 0
    total_time = 0

    for prompt_cfg in COMPLEX_PROMPTS:
        t0 = time.time()
        try:
            ok = await run_single_prompt(prompt_cfg, gateway, chapter_cache)
            if ok:
                passed += 1
            else:
                failed += 1
        except Exception as e:
            print(f"\n  ✗ 异常: {e}")
            failed += 1
        total_time += time.time() - t0

    # 汇总
    print(f"\n{'='*60}")
    print(f"  总结: {passed} 通过, {failed} 失败, 总耗时 {total_time:.1f}s")
    print(f"{'='*60}")
    if failed:
        sys.exit(1)
    print("  全部通过!")


if __name__ == "__main__":
    asyncio.run(main())
