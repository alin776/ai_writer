# -*- coding: utf-8 -*-
"""
Explore V6 真实环境验证：5 个复杂 Prompt

运行: cd backend && python -X utf8 tests/integration_explore_v6_live.py
"""

import asyncio
import os
import sys
import time
from pathlib import Path

BACKEND_DIR = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(BACKEND_DIR))

# 从 backend/.env 加载环境变量
_env_file = BACKEND_DIR / ".env"
if _env_file.exists():
    for line in _env_file.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if line and not line.startswith("#") and "=" in line:
            key, _, val = line.partition("=")
            # 去掉行内注释（# 后面的部分），但保留 URL 中的 #
            raw_val = val.strip()
            if "  #" in raw_val:
                raw_val = raw_val[:raw_val.index("  #")].strip()
            os.environ.setdefault(key.strip(), raw_val)

os.environ.setdefault("LIGHTRAG_BASE_URL", "http://127.0.0.1:9621")
os.environ.setdefault("LIGHTRAG_TIMEOUT_SECONDS", "300")

WORK_ID = "e6590250-38df-4db2-aadb-de87ee3ca640"

# ========== 5 个复杂 Prompt ==========

COMPLEX_PROMPTS = [
    {
        "id": 1,
        "name": "跨章节因果推演 — 器灵等阶规则体系",
        "target_task": (
            "段融吞噬器灵的完整规则体系：为什么废刀的器灵等阶（二阶、三阶）反而高于赵穆好刀（未入阶）？"
            "器灵等阶由什么决定——器物经历的岁月、使用者数量、还是武功浸润时间？"
            "吞噬条件（精神力等级）与吞噬效果（刀法经验传承）之间的关系是什么？"
            "段融吞噬后脑中'被塞进东西'的迟钝状态到梦中消化的完整过程是怎样的？"
        ),
        "must_have": ["器灵等阶", "废刀", "吞噬", "精神力", "岁月"],
        "entities": ["段融", "器灵", "废刀", "赵穆"],
        "expect_keywords": ["器灵", "废刀", "吞噬"],
    },
    {
        "id": 2,
        "name": "多人物三角关系网 — 段融/赵穆/孔斌的隐性博弈",
        "target_task": (
            "全面分析段融、赵穆、孔斌三人之间的关系动态和实力对比："
            "赵穆作为实习镖师对杂役弟子的态度（让段融擦刀、只重点指导三人），"
            "孔斌作为天赋最佳弟子的领袖地位（制止李充挑衅、三人小团体核心），"
            "段融通过吞噬器灵获得入门级五虎群羊刀后的隐藏实力（标准桩功让孔斌讶异），"
            "以及赵穆发现人刀相应感消失但尚未意识到原因的伏笔。"
        ),
        "must_have": ["段融", "赵穆", "孔斌", "李充", "五虎群羊刀"],
        "entities": ["段融", "赵穆", "孔斌", "李充", "张征"],
        "expect_keywords": ["赵穆", "孔斌", "段融"],
    },
    {
        "id": 3,
        "name": "隐藏伏笔双线追踪 — 器灵消失 + 梦中经验消化",
        "target_task": (
            "追踪两条平行伏笔线："
            "线索A：段融吞噬赵穆牛尾刀器灵后，赵穆晚上练功发现'人刀相应'感觉消失、"
            "刀变得不顺手'倒像攥了一把新刀'的具体描写，以及这对段融身份暴露的风险暗示。"
            "线索B：段融吞噬后脑中'被塞进一团东西'的迟钝状态，到夜里梦境中看到壮硕人影练刀、"
            "感知内息流转、最终午夜醒来一夕千悟将五虎群羊刀打出来的完整过程。"
            "两条线的时间线如何交错？"
        ),
        "must_have": ["人刀相应", "消失", "梦", "一夕千悟", "内息"],
        "entities": ["段融", "赵穆", "牛尾刀"],
        "expect_keywords": ["人刀相应", "一夕千悟"],
    },
    {
        "id": 4,
        "name": "世界观纵深还原 — 宗门体制 + 底层经济 + 权力结构",
        "target_task": (
            "还原小说的完整世界观架构："
            "宏观层：九州大陆由八大宗门统治，太一门掌管青州，县令是外门弟子，武功秘籍传承决定权力格局。"
            "中观层：源顺镖局的组织结构——杂役弟子→学徒→实习镖师→镖师的晋升链条，"
            "总教习萧宗庭负责考核选拔，镖头管理日常。"
            "微观层：底层武者的经济基础——杂役月钱六十文vs学徒三钱银子（五倍），"
            "段融全部家底一两多银子，两个窝头一碗粥的伙食标准，"
            "杨震二叔在生药铺做账房的人脉资源。"
        ),
        "must_have": ["太一门", "青州", "宗门", "月钱", "学徒"],
        "entities": ["太一门", "源顺镖局", "萧宗庭", "杨震"],
        "expect_keywords": ["太一门", "宗门"],
    },
    {
        "id": 5,
        "name": "关键事件全链路 — 许儒虎案的情报网络",
        "target_task": (
            "完整还原许儒虎事件的情报链，按时间线组织："
            "1）许儒虎身份：太一门外门弟子→因奸污同门被全境通缉→"
            "在青州四府十八郡流窜多年。"
            "2）被捕过程：重伤藏身勾栏院→被解道寒捕头偶然认出→"
            "搏斗中即使重伤仍打得解道寒吐血→最终被擒，重锁刺透肩胛骨关入地牢。"
            "3）后续安排：杨震和解雷（解道寒侄儿）受命看守→"
            "县衙发急递→宗门回复将派人提走处决。"
            "4）信息来源：杨震在酒楼向段融炫耀此事的社交动机分析。"
        ),
        "must_have": ["许儒虎", "太一门", "解道寒", "杨震", "地牢"],
        "entities": ["许儒虎", "解道寒", "杨震", "解雷"],
        "expect_keywords": ["许儒虎", "解道寒"],
    },
]


async def run_v6_test(prompt_cfg):
    """运行单个 V6 真实测试"""
    from app.services.agent.tools.explore_v6 import ExploreV6

    pid = prompt_cfg["id"]
    name = prompt_cfg["name"]
    print(f"\n{'━'*70}")
    print(f"  Prompt {pid}: {name}")
    print(f"{'━'*70}")

    v6 = ExploreV6(
        work_id=WORK_ID,
        target_task=prompt_cfg["target_task"],
        retrieval_intent={
            "goal": prompt_cfg["target_task"][:200],
            "must_have": prompt_cfg["must_have"],
            "entities": prompt_cfg.get("entities", []),
        },
    )

    t0 = time.time()
    try:
        result = await v6.run()
    except Exception as e:
        elapsed = time.time() - t0
        print(f"  ✗ V6 执行异常: {e}")
        import traceback
        traceback.print_exc()
        return False, elapsed

    elapsed = time.time() - t0

    evidences = result.get("evidences", [])
    stats = result.get("stats", {})
    stop_reason = result.get("stop_reason", "")
    worldview = result.get("worldview", {})

    # 统计
    total = len(evidences)
    located = sum(1 for e in evidences if isinstance(e.get("chapter_order"), int))
    chapters_hit = sorted(set(
        e["chapter_order"] for e in evidences if isinstance(e.get("chapter_order"), int)
    ))
    coverage = stats.get("coverage", 0)
    queries = stats.get("queries", [])
    supplement_rounds = stats.get("supplement_rounds", 0)
    wv_cats = list(worldview.keys()) if worldview else []

    # 关键词命中
    all_text = " ".join(str(e.get("text", "")) for e in evidences)
    expect_kws = prompt_cfg.get("expect_keywords", [])
    kw_hits = {kw: kw in all_text for kw in expect_kws}

    print(f"  ⏱  耗时: {elapsed:.2f}s")
    print(f"  📊 查询数: {len(queries)} | 补充轮: {supplement_rounds} | 覆盖率: {coverage:.0%}")
    print(f"  📦 结果数: {total} | 定位: {located}/{total} | 章节: {chapters_hit}")
    print(f"  🌍 世界观: {wv_cats}")
    print(f"  🔑 关键词: {kw_hits}")
    print(f"  🏁 停止原因: {stop_reason}")

    if queries:
        print(f"\n  生成的查询:")
        for i, q in enumerate(queries):
            print(f"    [{i+1}] {q}")

    # 前 5 条 evidence 明细
    print(f"\n  前 5 条 evidence:")
    for i, e in enumerate(evidences[:5]):
        ch = e.get("chapter_order")
        pi = e.get("paragraph_index")
        text_preview = str(e.get("text", ""))[:80].replace('\n', ' ')
        loc = f"第{ch}章·第{pi}段" if ch is not None else "⚠未定位"
        print(f"    [{i}] {loc}")
        print(f"        {text_preview}...")

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
        print(f"\n  ✓ 通过 — {elapsed:.2f}s, {located}/{total} 定位, 章节 {chapters_hit}")
        return True, elapsed


async def main():
    print("=" * 70)
    print("  Explore V6 真实环境验证 — 5 个复杂 Prompt")
    print(f"  work_id: {WORK_ID}")
    print(f"  LightRAG: {os.environ.get('LIGHTRAG_BASE_URL')}")
    print("=" * 70)

    passed = 0
    failed = 0
    total_time = 0
    results = []

    for prompt_cfg in COMPLEX_PROMPTS:
        try:
            ok, elapsed = await run_v6_test(prompt_cfg)
            total_time += elapsed
            results.append((prompt_cfg["id"], prompt_cfg["name"][:20], ok, elapsed))
            if ok:
                passed += 1
            else:
                failed += 1
        except Exception as e:
            print(f"\n  ✗ 异常: {e}")
            import traceback
            traceback.print_exc()
            results.append((prompt_cfg["id"], prompt_cfg["name"][:20], False, 0))
            failed += 1

    # 汇总
    print(f"\n{'='*70}")
    print(f"  V6 验证总结")
    print(f"{'='*70}")
    for pid, name, ok, elapsed in results:
        status = "✓" if ok else "✗"
        print(f"  {status} Prompt {pid}: {name}... ({elapsed:.1f}s)")
    print(f"\n  通过: {passed}/5 | 失败: {failed}/5 | 总耗时: {total_time:.1f}s")
    if total_time > 0:
        print(f"  平均每个: {total_time/5:.1f}s")
    print(f"{'='*70}")

    if failed:
        sys.exit(1)
    print("  全部通过!")


if __name__ == "__main__":
    asyncio.run(main())
