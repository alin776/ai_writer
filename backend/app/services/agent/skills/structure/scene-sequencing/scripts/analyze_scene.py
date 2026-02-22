#!/usr/bin/env python3
"""analyze_scene.py - 场景结构分析器

基于场景-续篇（Scene-Sequel）模式分析中文小说场景结构：
场景段：目标(Goal) → 冲突(Conflict) → 灾难(Disaster)
续篇段：反应(Reaction) → 困境(Dilemma) → 决定(Decision)

Usage:
  python analyze_scene.py <file>
  python analyze_scene.py --text "场景文本..."
  python analyze_scene.py --json <file>
"""

import sys
import re
import json

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

# ---------------------------------------------------------------------------
# 中文场景结构模式
# ---------------------------------------------------------------------------

GOAL_PATTERNS = [
    re.compile(r'(想要|需要|必须|一定要|打算|决心|目标|任务|使命)'),
    re.compile(r'(下定决心|立志|发誓|暗暗决定|计划着)'),
    re.compile(r'(寻找|获取|到达|逃离|阻止|拯救|夺回|保护|破解|攻克)'),
]
CONFLICT_PATTERNS = [
    re.compile(r'(但是|然而|可是|不料|偏偏|却|岂料|谁知|无奈)'),
    re.compile(r'(阻拦|阻止|拦住|挡住|抵抗|反击|对峙|抗拒)'),
    re.compile(r'(困难|障碍|危险|威胁|敌人|麻烦|问题|陷阱|困境)'),
    re.compile(r'(交手|厮杀|对决|缠斗|对抗|碰撞|冲突)'),
]
DISASTER_PATTERNS = [
    re.compile(r'(失败|落败|败下阵来|功亏一篑|前功尽弃|溃败)'),
    re.compile(r'(更糟|雪上加霜|屋漏偏逢|祸不单行|急转直下)'),
    re.compile(r'(被困|被抓|被发现|暴露|中计|中招|受伤|倒下)'),
    re.compile(r'(来不及|无法|不可能|绝望|走投无路)'),
    re.compile(r'(突然|忽然|骤然|猛然|陡然|刹那间)'),
]
REACTION_PATTERNS = [
    re.compile(r'(感到|感觉|心中|心里|内心|胸口|心头)'),
    re.compile(r'(震惊|恐惧|绝望|悲痛|愤怒|害怕|惊恐|不安)'),
    re.compile(r'(不敢相信|脑中一片空白|思绪万千|心乱如麻)'),
    re.compile(r'(呆立|愣住|怔住|僵在|瘫坐|跌坐)'),
]
DILEMMA_PATTERNS = [
    re.compile(r'(选择|抉择|两难|要么.*要么|是.*还是)'),
    re.compile(r'(可以|应该|或许|如果|假如|万一)'),
    re.compile(r'(一方面.*另一方面|进退两难|左右为难|权衡)'),
    re.compile(r'(没有好的选择|两个都.*不好|无论.*都)'),
]
DECISION_PATTERNS = [
    re.compile(r'(决定|下定决心|做出.*决定|选择了|拿定主意)'),
    re.compile(r'(要|必须|一定|非.*不可|唯一.*办法)'),
    re.compile(r'(计划|策略|下一步|唯一.*出路|只有一个办法)'),
    re.compile(r'(站起|起身|转身|迈步|出发|动身|行动)'),
]


def count_matches(text, patterns):
    matches = []
    for p in patterns:
        found = p.findall(text)
        if found:
            matches.extend(found[:3])
    return list(set(matches))[:5]


def calc_dialogue(text):
    # 中文引号对话
    quotes = re.findall(r'[""「][^""」]+[""」]', text)
    return sum(len(q) for q in quotes) / len(text) if text else 0


def analyze_scene(text):
    chars = len(text.replace(' ', '').replace('\n', ''))
    paras = [p for p in re.split(r'\n\s*\n', text) if p.strip()]
    sents = [s.strip() for s in re.split(r'[。！？…]+', text) if s.strip()]

    gi = count_matches(text, GOAL_PATTERNS)
    ci = count_matches(text, CONFLICT_PATTERNS)
    di = count_matches(text, DISASTER_PATTERNS)
    ri = count_matches(text, REACTION_PATTERNS)
    dli = count_matches(text, DILEMMA_PATTERNS)
    dci = count_matches(text, DECISION_PATTERNS)

    ss = len(gi) + len(ci) + len(di)  # 场景段信号
    sq = len(ri) + len(dli) + len(dci)  # 续篇段信号
    ratio = ss / (ss + sq) if (ss + sq) > 0 else 0.5

    if ratio > 0.65:
        pacing = "动作密集"
    elif ratio < 0.35:
        pacing = "反思为主"
    else:
        pacing = "均衡"

    issues, recs = [], []
    if not gi:
        issues.append("未检测到明确的目标/动机")
        recs.append("在场景开头建立 POV 角色的具体目标")
    if not ci:
        issues.append("未检测到冲突指标")
        recs.append("加入阻碍角色达成目标的对抗力量")
    if not di and ss > 0:
        issues.append("场景可能结束得太顺利")
        recs.append("考虑让结果比预期更糟——灾难推动故事前进")
    if ratio > 0.8:
        issues.append("严重偏向动作，缺少情感消化")
        recs.append("在高潮后加入续篇段（反应→困境→决定）")
    if ratio < 0.2 and chars > 500:
        issues.append("过长的内心反思，缺少外在行动")
        recs.append("推动角色走向决定和行动")
    if ri and not dci:
        issues.append("有情绪反应但没有做出决定")
        recs.append("让角色在反思后做出承诺并付诸行动")

    return {
        "charCount": chars,
        "sentenceCount": len(sents),
        "paragraphCount": len(paras),
        "dialogueRatio": round(calc_dialogue(text), 3),
        "goalIndicators": gi,
        "conflictIndicators": ci,
        "disasterIndicators": di,
        "reactionIndicators": ri,
        "dilemmaIndicators": dli,
        "decisionIndicators": dci,
        "sceneSequelRatio": round(ratio, 2),
        "pacingAssessment": pacing,
        "issues": issues,
        "recommendations": recs,
    }


def format_report(r):
    out = ["# 场景结构分析"]
    out.append("字数: {}  句数: {}  段落: {}".format(
        r["charCount"], r["sentenceCount"], r["paragraphCount"]))
    out.append("对话比: {:.1f}%  节奏: {}  场景段比: {:.0f}%".format(
        r["dialogueRatio"] * 100, r["pacingAssessment"], r["sceneSequelRatio"] * 100))
    out.append("")

    labels = [
        ("goalIndicators", "目标(G)"),
        ("conflictIndicators", "冲突(C)"),
        ("disasterIndicators", "灾难(D)"),
        ("reactionIndicators", "反应(R)"),
        ("dilemmaIndicators", "困境(D)"),
        ("decisionIndicators", "决定(D)"),
    ]
    for key, label in labels:
        v = r[key]
        out.append("  {}: {}".format(label, "、".join(v) if v else "未检测到"))

    if r["issues"]:
        out.append("\n发现的问题:")
        for i in r["issues"]:
            out.append("  - " + i)
    if r["recommendations"]:
        out.append("\n改进建议:")
        for i in r["recommendations"]:
            out.append("  - " + i)
    return "\n".join(out)


def main():
    args = sys.argv[1:]
    if "--help" in args or "-h" in args:
        print("场景结构分析器 (analyze_scene.py)")
        print("Usage: python analyze_scene.py <file> [--json] [--text TEXT]")
        print("分析场景的目标-冲突-灾难-反应-困境-决定结构")
        sys.exit(0)
    json_out = "--json" in args
    text = ""
    if "--text" in args:
        idx = args.index("--text")
        parts = []
        for part in args[idx + 1:]:
            if part.startswith("--"):
                break
            parts.append(part)
        text = " ".join(parts)
    else:
        farg = next((x for x in args if not x.startswith("--")), None)
        if farg:
            try:
                with open(farg, "r", encoding="utf-8") as f:
                    text = f.read()
            except Exception as e:
                print("读取文件错误: %s" % e, file=sys.stderr)
                sys.exit(1)
        else:
            print("错误: 未提供输入。使用 --help 查看用法。", file=sys.stderr)
            sys.exit(1)
    if not text.strip():
        print("错误: 输入为空", file=sys.stderr)
        sys.exit(1)
    result = analyze_scene(text)
    print(json.dumps(result, indent=2, ensure_ascii=False) if json_out else format_report(result))


if __name__ == "__main__":
    main()
