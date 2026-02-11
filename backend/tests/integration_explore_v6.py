# -*- coding: utf-8 -*-
"""
Explore V6 集成测试：5 个复杂 Prompt 对比 V6 与 V5

运行: cd backend && python -X utf8 tests/integration_explore_v6.py
前提: LightRAG 服务运行于 127.0.0.1:9621, 数据库可用

对比指标: 结果数、定位率、覆盖率、耗时、LLM 调用次数
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

# ========== 5 个复杂 Prompt ==========

COMPLEX_PROMPTS = [
    {
        "id": 1,
        "name": "跨章节因果链 — 器灵吞噬规则推演",
        "target_task": "段融吞噬器灵的完整规则体系：吞噬条件、吞噬效果、器灵等阶与器物品质的关系、以及器灵成长与岁月经历的关联",
        "must_have": ["器灵等阶", "吞噬", "精神力", "废刀"],
        "entities": ["段融", "器灵", "废刀"],
        "expect_keywords": ["器灵", "吞噬"],
    },
    {
        "id": 2,
        "name": "多人物交叉 — 段融、赵穆、孔斌关系网",
        "target_task": "对比段融、赵穆、孔斌三人的武功水平和关系：赵穆的刀法水平，孔斌的天赋表现，段融的隐藏实力与弱者形象的反差",
        "must_have": ["段融", "赵穆", "孔斌"],
        "entities": ["段融", "赵穆", "孔斌"],
        "expect_keywords": ["赵穆", "孔斌"],
    },
    {
        "id": 3,
        "name": "隐藏伏笔追踪 — 赵穆察觉器灵消失",
        "target_task": "段融吞噬赵穆牛尾刀器灵后，赵穆发现人刀相应感觉消失的描写，以及段融消化经验的完整过程",
        "must_have": ["赵穆", "器灵", "人刀相应", "消失"],
        "entities": ["赵穆", "牛尾刀", "段融"],
        "expect_keywords": ["赵穆", "牛尾刀"],
    },
    {
        "id": 4,
        "name": "世界观架构还原 — 太一门宗门体制",
        "target_task": "还原小说世界观架构：九州大陆八大宗门、太一门掌管青州、底层武者晋升体系、月钱经济基础",
        "must_have": ["太一门", "青州", "宗门"],
        "entities": ["太一门", "青州"],
        "expect_keywords": ["太一门", "宗门"],
    },
    {
        "id": 5,
        "name": "关键事件精确定位 — 许儒虎案件情报链",
        "target_task": "定位许儒虎事件的完整信息链：许儒虎身份、罪行、被捕过程、关押看守",
        "must_have": ["许儒虎", "太一门", "解道寒"],
        "entities": ["许儒虎", "解道寒", "杨震"],
        "expect_keywords": ["许儒虎"],
    },
]


async def run_v6_test(prompt_cfg):
    """运行单个 V6 测试"""
    from app.services.agent.tools.explore_v6 import ExploreV6

    pid = prompt_cfg["id"]
    name = prompt_cfg["name"]
    print(f"\n{'─'*60}")
    print(f"  Prompt {pid}: {name}")
    print(f"{'─'*60}")

    v6 = ExploreV6(
        work_id=WORK_ID,
        target_task=prompt_cfg["target_task"],
        retrieval_intent={
            "goal": prompt_cfg["target_task"],
            "must_have": prompt_cfg["must_have"],
            "entities": prompt_cfg.get("entities", []),
        },
    )

    t0 = time.time()
    result = await v6.run()
    elapsed = time.time() - t0

    evidences = result.get("evidences", [])
    stats = result.get("stats", {})
    stop_reason = result.get("stop_reason", "")

    # 统计
    total = len(evidences)
    located = sum(1 for e in evidences if isinstance(e.get("chapter_order"), int))
    chapters_hit = sorted(set(
        e["chapter_order"] for e in evidences if isinstance(e.get("chapter_order"), int)
    ))
    coverage = stats.get("coverage", 0)
    queries = stats.get("queries", [])
    supplement_rounds = stats.get("supplement_rounds", 0)

    # 关键词命中
    all_text = " ".join(str(e.get("text", "")) for e in evidences)
    expect_kws = prompt_cfg.get("expect_keywords", [])
    kw_hits = {kw: kw in all_text for kw in expect_kws}

    print(f"  耗时: {elapsed:.2f}s")
    print(f"  查询数: {len(queries)} | 补充轮数: {supplement_rounds}")
    print(f"  结果数: {total} | 定位: {located}/{total} | 章节: {chapters_hit}")
    print(f"  覆盖率: {coverage:.2%}")
    print(f"  关键词: {kw_hits}")
    print(f"  停止原因: {stop_reason}")

    if queries:
        print(f"  生成的查询:")
        for i, q in enumerate(queries):
            print(f"    [{i+1}] {q}")

    # 结果明细（前 5 条）
    print(f"  前 5 条 evidence:")
    for i, e in enumerate(evidences[:5]):
        ch = e.get("chapter_order")
        pi = e.get("paragraph_index")
        text_preview = str(e.get("text", ""))[:60].replace('\n', ' ')
        loc = f"第{ch}章第{pi}段" if ch is not None else "未定位"
        print(f"    [{i}] {loc}: {text_preview}...")

    # 判定
    errors = []
    if not result.get("success"):
        errors.append("检索失败")
    if total == 0:
        errors.append("无结果")
    if located == 0 and total > 0:
        errors.append("全部未定位")
    for kw, hit in kw_hits.items():
        if not hit:
            errors.append(f"关键词 '{kw}' 未命中")

    if errors:
        print(f"\n  ✗ 问题: {'; '.join(errors)}")
        return False, elapsed
    else:
        print(f"\n  ✓ 通过")
        return True, elapsed


async def main():
    print("=" * 60)
    print("  Explore V6 集成测试 — 5 个复杂 Prompt")
    print(f"  work_id: {WORK_ID}")
    print("=" * 60)

    passed = 0
    failed = 0
    total_time = 0

    for prompt_cfg in COMPLEX_PROMPTS:
        try:
            ok, elapsed = await run_v6_test(prompt_cfg)
            total_time += elapsed
            if ok:
                passed += 1
            else:
                failed += 1
        except Exception as e:
            print(f"\n  ✗ 异常: {e}")
            import traceback
            traceback.print_exc()
            failed += 1

    print(f"\n{'='*60}")
    print(f"  V6 总结: {passed} 通过, {failed} 失败, 总耗时 {total_time:.1f}s")
    print(f"{'='*60}")
    if failed:
        sys.exit(1)
    print("  全部通过!")


if __name__ == "__main__":
    asyncio.run(main())
