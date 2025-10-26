"""
评审功能集成测试脚本

测试内容:
1. 段落级评审 API
2. 作品级评审 API
"""

import asyncio
import json
from uuid import uuid4


# ==================== 测试数据 ====================

# 测试段落
TEST_PARAGRAPH = """
林风深吸一口气，推开木门。房间里灰尘飞舞，一把古剑静静地躺在桌上，
散发着淡淡的青光。他走近桌边，手指轻轻触碰剑身，一股冰凉的感觉瞬间传遍全身。
"""

TEST_CONTEXT = "这是主角第一次进入师父的密室，发现传说中的神剑"

# 测试作品
TEST_BOOK_TITLE = "剑仙传说"
TEST_NOVEL_ID = str(uuid4())

TEST_CHAPTERS = [
    {
        "title": "第一章 入门",
        "content": """
        东洲大陆，剑宗山门。

        林风站在山门前，仰望着高耸入云的山峰。作为一个从小村庄走出来的少年，
        他从未见过如此壮观的景象。山门两侧，巨大的石柱上刻着"剑道至尊"四个大字，
        每个字都透着凌厉的剑意。

        "新弟子，进来吧。"一个声音从山门内传来。

        林风深吸一口气，迈步走了进去。前方是一条长长的石阶，两旁站着数十名
        身穿白色道袍的弟子，个个气质不凡。他们用审视的目光打量着林风，
        眼中既有好奇，也有一丝轻视。

        "又来了一个散修，能坚持三天就不错了。"有人低声说道。

        林风装作没听见，继续向前走去。他知道，想要在剑宗立足，
        必须用实力说话。而他，正是为此而来。
        """,
        "order": 1
    },
    {
        "title": "第二章 试炼",
        "content": """
        试炼大会在第二天清晨开始。

        所有新入门的弟子聚集在演武场上，足足有三百多人。主持试炼的是一位
        长老，名叫云剑子，据说已经修炼了三百年，实力深不可测。

        "试炼规则很简单，"云剑子缓缓开口，"进入幻境，斩杀妖兽，
        获得积分。积分前一百名，可以正式成为外门弟子。"

        话音刚落，一道光幕在空中展开，形成了一个巨大的传送门。
        弟子们鱼贯而入，林风也跟着人群进入了幻境。

        眼前景象一变，他发现自己身处一片密林之中。不远处，
        传来野兽的咆哮声。林风抽出腰间的长剑，向声音的方向走去。

        第一只妖兽很快出现了，是一头三阶的铁背熊。林风眼神一凝，
        身形如电般冲了出去。剑光一闪，铁背熊应声倒地。

        "果然，实战才是最好的修炼。"林风喃喃自语。
        """,
        "order": 2
    },
    {
        "title": "第三章 突破",
        "content": """
        试炼持续了三天三夜。

        林风在幻境中斩杀了无数妖兽，积分遥遥领先。但他并不满足，
        因为他感觉到，突破的时机快要到了。

        第三天黄昏，林风遇到了一只五阶的炎魔狼。这是幻境中最强大的妖兽之一，
        寻常弟子见到都会绕道而行。但林风却主动迎了上去。

        战斗异常激烈。炎魔狼的火焰几乎要将林风吞噬，但他咬牙坚持，
        一剑又一剑地劈砍着。渐渐地，他发现自己的剑法越来越流畅，
        体内的真气也在疯狂涌动。

        "就是现在！"林风大喝一声，全身真气爆发，剑光暴涨三尺。

        一剑，将炎魔狼劈成两半。

        与此同时，林风感觉到体内一道屏障轰然破碎。他，突破到了筑基期！

        "这就是筑基的力量吗？"林风握紧拳头，感受着体内澎湃的真气，
        眼中闪过一丝兴奋。

        试炼结束，林风以第一名的成绩成为了外门弟子。但他知道，
        这只是开始。剑道之路，还很漫长。
        """,
        "order": 3
    }
]


# ==================== 测试函数 ====================

async def test_paragraph_review():
    """测试段落级评审"""
    print("\n" + "="*60)
    print("测试 1: 段落级评审")
    print("="*60)

    from app.services.review.paragraph_review_service import ParagraphReviewService

    try:
        service = ParagraphReviewService()
        result = await service.review_paragraph(
            text=TEST_PARAGRAPH,
            context=TEST_CONTEXT
        )

        print("\n[OK] 段落级评审成功!")
        print(f"\n总分: {result.get('overall_score', 0)}")
        print(f"\n维度评分:")
        for dim, score in result.get('dimension_scores', {}).items():
            print(f"  - {dim}: {score}")
        print(f"\n快速反馈: {result.get('quick_feedback', '')}")
        print(f"\n建议:")
        for i, sug in enumerate(result.get('suggestions', []), 1):
            print(f"  {i}. {sug}")

        return True

    except Exception as e:
        print(f"\n[ERROR] 段落级评审失败: {e}")
        import traceback
        traceback.print_exc()
        return False


async def test_book_review():
    """测试作品级评审"""
    print("\n" + "="*60)
    print("测试 2: 作品级评审")
    print("="*60)

    from app.services.review.book_review_service import BookReviewService
    from uuid import UUID

    try:
        service = BookReviewService()
        result = await service.review_book(
            novel_id=UUID(TEST_NOVEL_ID),
            book_title=TEST_BOOK_TITLE,
            chapters=TEST_CHAPTERS
        )

        print("\n[OK] 作品级评审成功!")
        print(f"\n书名: {result.get('book_title', '')}")
        print(f"总分: {result.get('overall_score', 0)}")
        print(f"章节数: {result.get('total_chapters', 0)}")

        print(f"\n【情节分析】")
        plot = result.get('plot_analysis', {})
        print(f"  结构类型: {plot.get('structure_type', '')}")
        print(f"  节奏评分: {plot.get('rhythm_score', 0)}")
        print(f"  高潮章节: {plot.get('climax_points', [])}")

        print(f"\n【人物分析】")
        char = result.get('character_analysis', {})
        print(f"  人物评分: {char.get('character_score', 0)}")
        print(f"  主要角色数: {len(char.get('main_characters', []))}")

        print(f"\n【世界观分析】")
        world = result.get('worldview_analysis', {})
        print(f"  独特性: {world.get('uniqueness_score', 0)}")
        print(f"  一致性: {world.get('consistency_score', 0)}")
        print(f"  深度: {world.get('depth_score', 0)}")

        print(f"\n【文风分析】")
        style = result.get('writing_style', {})
        print(f"  风格标签: {', '.join(style.get('style_tags', []))}")
        print(f"  语言评分: {style.get('language_score', 0)}")
        print(f"  对话评分: {style.get('dialogue_score', 0)}")

        print(f"\n【综合建议】")
        rec = result.get('recommendations', {})
        print(f"  核心优势: {', '.join(rec.get('core_strengths', []))}")
        print(f"  关键问题: {', '.join(rec.get('critical_issues', []))}")

        return True

    except Exception as e:
        print(f"\n[ERROR] 作品级评审失败: {e}")
        import traceback
        traceback.print_exc()
        return False


async def main():
    """主测试函数"""
    print("\n" + "="*60)
    print("[TEST] 评审功能集成测试")
    print("="*60)

    results = []

    # 测试1: 段落级评审
    result1 = await test_paragraph_review()
    results.append(("段落级评审", result1))

    # 测试2: 作品级评审
    result2 = await test_book_review()
    results.append(("作品级评审", result2))

    # 汇总结果
    print("\n" + "="*60)
    print("[SUMMARY] 测试结果汇总")
    print("="*60)

    for name, success in results:
        status = "[PASS]" if success else "[FAIL]"
        print(f"{name}: {status}")

    all_passed = all(r[1] for r in results)
    print(f"\n总体结果: {'[ALL PASS]' if all_passed else '[SOME FAIL]'}")


if __name__ == "__main__":
    asyncio.run(main())
