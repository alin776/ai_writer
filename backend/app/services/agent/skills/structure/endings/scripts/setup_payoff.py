#!/usr/bin/env python3
"""
setup_payoff.py - 伏笔-回收追踪器

追踪故事中的伏笔（铺垫）与回收，帮助发现未回收的伏笔以及缺少铺垫的回收。

用法:
  python setup_payoff.py --analyze story.txt
  python setup_payoff.py --setup "玉佩" --file story.txt
  python setup_payoff.py --list story.txt
  python setup_payoff.py --json --analyze story.txt
"""

import sys
import re
import json

# 确保所有平台 UTF-8 输出
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")
if hasattr(sys.stderr, "reconfigure"):
    sys.stderr.reconfigure(encoding="utf-8")

# ---------------------------------------------------------------------------
# 铺垫模式 — 引入后可能需要回收的元素
# ---------------------------------------------------------------------------

SETUP_PATTERNS = [
    {
        "type": "object",
        "patterns": [
            re.compile(r"(注意到|发现|看到|捡起|取出|藏着|隐藏|携带|收好|塞进|摸到|怀中)"),
            re.compile(r"(钥匙|剑|玉佩|令牌|丹药|秘籍|地图|信物|法器|宝物|暗器|毒药|解药|血书|骨灰)"),
        ],
    },
    {
        "type": "skill",
        "patterns": [
            re.compile(r"(会|能|擅长|精通|修炼过|学过|传承|天赋|血脉|觉醒|领悟)"),
            re.compile(r"(多年的|从小|曾经练过|一身的|精于)"),
        ],
    },
    {
        "type": "character",
        "patterns": [
            re.compile(r"(有一个|师兄|师妹|师父|故人|仇人|旧识|义兄|结拜|失散)"),
            re.compile(r"(曾经的|昔日的|幼时的|当年的|前任)"),
        ],
    },
    {
        "type": "information",
        "patterns": [
            re.compile(r"(秘密|知道|听说|记得|曾经说过|提到过|据说|传言|古籍记载|禁忌)"),
            re.compile(r"(无人知晓|只有.*知道|隐藏的真相|真正的原因)"),
        ],
    },
    {
        "type": "threat",
        "patterns": [
            re.compile(r"(还会回来|不会就此罢休|还在|有朝一日|总有一天|等着瞧|迟早)"),
            re.compile(r"(警告|威胁|发誓要|誓言|扬言)"),
        ],
    },
    {
        "type": "promise",
        "patterns": [
            re.compile(r"(答应|承诺|许下|保证|立下誓言|发过毒誓|约定|赌上.*名义)"),
            re.compile(r"(一定会|终有一天|绝不|此生必)"),
        ],
    },
    {
        "type": "foreshadow",
        "patterns": [
            re.compile(r"(殊不知|谁也没想到|日后|后来证明|彼时.*尚不知|埋下了.*种子)"),
            re.compile(r"(不祥的|隐隐|预感|冥冥之中|命运)"),
        ],
    },
]

# ---------------------------------------------------------------------------
# 回收模式 — 可能正在解决先前铺垫的元素
# ---------------------------------------------------------------------------

PAYOFF_PATTERNS = [
    {
        "type": "object",
        "patterns": [
            re.compile(r"(拿出|取出|使用|祭出|掏出|亮出|抛出|打开|解锁|终于用上)"),
            re.compile(r"(之前的.*派上了用场|关键时刻.*掏出)"),
        ],
    },
    {
        "type": "skill",
        "patterns": [
            re.compile(r"(终于派上用场|多年的.*终于|果然|修炼的.*发挥了|当年学的|幸亏.*会)"),
            re.compile(r"(功夫不负|关键时刻使出)"),
        ],
    },
    {
        "type": "character",
        "patterns": [
            re.compile(r"(出现了|回来了|找到了|赶到|现身|再次出现|突然出手|从天而降)"),
            re.compile(r"(意想不到的.*帮助|没想到.*竟然)"),
        ],
    },
    {
        "type": "information",
        "patterns": [
            re.compile(r"(真相是|原来|终于明白|恍然大悟|揭开了|真相大白|一切都说得通了)"),
            re.compile(r"(当初的.*原来|此刻才明白|难怪)"),
        ],
    },
    {
        "type": "threat",
        "patterns": [
            re.compile(r"(兑现|应验|果然来了|卷土重来|杀到|找上门|报复|清算)"),
            re.compile(r"(当初的.*终于|如期而至)"),
        ],
    },
    {
        "type": "promise",
        "patterns": [
            re.compile(r"(兑现了|践行|没有食言|信守|终于做到了|完成了.*承诺)"),
            re.compile(r"(当初的约定|实现了.*诺言)"),
        ],
    },
    {
        "type": "foreshadow",
        "patterns": [
            re.compile(r"(正如|应验了|终于|原来如此|一切都联系上了|命运的齿轮)"),
            re.compile(r"(果然如此|真如.*所说|印证了)"),
        ],
    },
]

# ---------------------------------------------------------------------------
# 类型中文名称映射
# ---------------------------------------------------------------------------

TYPE_LABELS = {
    "object": "物品",
    "skill": "技能",
    "character": "角色",
    "information": "信息",
    "threat": "威胁",
    "promise": "承诺",
    "foreshadow": "伏笔/预示",
}


# ---------------------------------------------------------------------------
# 辅助函数
# ---------------------------------------------------------------------------

def get_line_context(text, position, window_size=50):
    """返回 *position* 周围的文本片段用于上下文展示。"""
    start = max(0, position - window_size)
    end = min(len(text), position + window_size)
    context = text[start:end].replace("\n", " ").strip()
    if start > 0:
        context = "..." + context
    if end < len(text):
        context = context + "..."
    return context


def find_setups(text):
    """在 *text* 前 70% 中查找潜在的铺垫。"""
    text_length = len(text)
    setups = []

    for group in SETUP_PATTERNS:
        setup_type = group["type"]
        for pattern in group["patterns"]:
            for m in pattern.finditer(text):
                position_pct = (m.start() / text_length) * 100 if text_length else 0
                # 仅考虑前 70% 的铺垫
                if position_pct <= 70:
                    setups.append({
                        "text": m.group(0).strip(),
                        "position": m.start(),
                        "positionPercent": round(position_pct),
                        "type": setup_type,
                        "lineContext": get_line_context(text, m.start()),
                    })

    # 按文本相似性去重
    unique = []
    for setup in setups:
        is_dup = any(
            u["text"] == setup["text"] and abs(u["position"] - setup["position"]) < 100
            for u in unique
        )
        if not is_dup:
            unique.append(setup)

    unique.sort(key=lambda s: s["position"])
    return unique


def find_payoffs(text):
    """在 *text* 后 50% 中查找潜在的回收。"""
    text_length = len(text)
    payoffs = []

    for group in PAYOFF_PATTERNS:
        payoff_type = group["type"]
        for pattern in group["patterns"]:
            for m in pattern.finditer(text):
                position_pct = (m.start() / text_length) * 100 if text_length else 0
                # 仅考虑后 50% 的回收
                if position_pct >= 50:
                    payoffs.append({
                        "text": m.group(0).strip(),
                        "position": m.start(),
                        "positionPercent": round(position_pct),
                        "type": payoff_type,
                        "lineContext": get_line_context(text, m.start()),
                    })

    # 去重
    unique = []
    for payoff in payoffs:
        is_dup = any(
            u["text"] == payoff["text"] and abs(u["position"] - payoff["position"]) < 100
            for u in unique
        )
        if not is_dup:
            unique.append(payoff)

    unique.sort(key=lambda p: p["position"])
    return unique


def match_setups_to_payoffs(setups, payoffs, text_length):
    """尝试将相同类型的铺垫与回收配对。

    返回包含 matched、unresolved、orphaned 的字典。
    """
    matched = []
    used_setups = set()
    used_payoffs = set()

    for i, setup in enumerate(setups):
        for j, payoff in enumerate(payoffs):
            if j in used_payoffs:
                continue
            if setup["type"] == payoff["type"] and payoff["position"] > setup["position"]:
                distance = payoff["position"] - setup["position"]
                distance_pct = round((distance / text_length) * 100) if text_length else 0
                matched.append({
                    "setup": setup,
                    "payoff": payoff,
                    "distance": distance,
                    "distancePercent": distance_pct,
                })
                used_setups.add(i)
                used_payoffs.add(j)
                break

    unresolved = [s for i, s in enumerate(setups) if i not in used_setups]
    orphaned = [p for j, p in enumerate(payoffs) if j not in used_payoffs]

    return {"matched": matched, "unresolved": unresolved, "orphaned": orphaned}


def search_for_term(text, term):
    """在整个 *text* 中搜索 *term*，返回出现位置。"""
    occurrences = []

    pos = 0
    while True:
        idx = text.find(term, pos)
        if idx == -1:
            break
        pct = round((idx / len(text)) * 100) if len(text) else 0
        occurrences.append({
            "position": idx,
            "percent": pct,
            "context": get_line_context(text, idx, 60),
        })
        pos = idx + len(term)

    return {"found": len(occurrences) > 0, "occurrences": occurrences}


# ---------------------------------------------------------------------------
# 完整分析
# ---------------------------------------------------------------------------

def analyze_setup_payoff(text, file_name="input"):
    """对 *text* 执行完整的伏笔-回收分析。"""
    char_count = len(re.sub(r"\s+", "", text))
    setups = find_setups(text)
    payoffs = find_payoffs(text)
    result = match_setups_to_payoffs(setups, payoffs, len(text))
    matched = result["matched"]
    unresolved = result["unresolved"]
    orphaned = result["orphaned"]

    issues = []
    recommendations = []

    # 评估健康度
    health = "健康"

    if len(unresolved) > 3:
        health = "严重问题"
        issues.append(f"检测到 {len(unresolved)} 处潜在铺垫未被回收")
        recommendations.append("审查未回收的铺垫——要么补充回收，要么删除铺垫")
    elif len(unresolved) > 0:
        health = "轻微问题"
        issues.append(f"检测到 {len(unresolved)} 处潜在的未回收铺垫")

    if len(orphaned) > 2:
        if health == "健康":
            health = "轻微问题"
        issues.append(f"检测到 {len(orphaned)} 处缺少铺垫的回收（天降神兵风险）")
        recommendations.append("确保后期的解决方案在前期有充分铺垫")

    if len(matched) == 0 and len(setups) > 0:
        issues.append("未检测到伏笔-回收匹配——故事可能缺乏令人满意的呼应")
        recommendations.append("追踪你的伏笔，确保在结尾前得到回收")

    # 检查铺垫与回收距离过近
    quick_payoffs = [m for m in matched if m["distancePercent"] < 10]
    if quick_payoffs:
        issues.append("部分铺垫回收过快（可能降低效果）")
        recommendations.append("建议拉大铺垫与回收之间的距离以增强冲击力")

    return {
        "fileName": file_name,
        "charCount": char_count,
        "potentialSetups": setups,
        "potentialPayoffs": payoffs,
        "matchedPairs": matched,
        "unresolvedSetups": unresolved,
        "orphanedPayoffs": orphaned,
        "setupPayoffHealth": health,
        "issues": issues,
        "recommendations": recommendations,
    }


# ---------------------------------------------------------------------------
# 报告输出
# ---------------------------------------------------------------------------

def format_report(analysis):
    """返回可读的伏笔-回收分析报告。"""
    lines = []

    lines.append("# 伏笔-回收分析\n")
    lines.append(f"文件: {analysis['fileName']}")
    lines.append(f"字数: {analysis['charCount']}")
    lines.append(f"健康度: {analysis['setupPayoffHealth']}\n")

    lines.append("## 总览\n")
    lines.append(f"  检测到潜在铺垫: {len(analysis['potentialSetups'])} 处")
    lines.append(f"  检测到潜在回收: {len(analysis['potentialPayoffs'])} 处")
    lines.append(f"  已匹配的伏笔对: {len(analysis['matchedPairs'])} 对")
    lines.append(f"  未回收的伏笔: {len(analysis['unresolvedSetups'])} 处")
    lines.append(f"  缺少铺垫的回收: {len(analysis['orphanedPayoffs'])} 处")
    lines.append("")

    if analysis["matchedPairs"]:
        lines.append("## 已匹配的伏笔-回收对\n")
        for pair in analysis["matchedPairs"][:10]:
            s = pair["setup"]
            p = pair["payoff"]
            s_label = TYPE_LABELS.get(s["type"], s["type"])
            p_label = TYPE_LABELS.get(p["type"], p["type"])
            lines.append(f"  [{s_label}] 铺垫于 {s['positionPercent']}% -> 回收于 {p['positionPercent']}%")
            lines.append(f"    铺垫: \"{s['text']}\"")
            lines.append(f"    回收: \"{p['text']}\"")
            lines.append("")
        if len(analysis["matchedPairs"]) > 10:
            lines.append(f"  ... 以及其他 {len(analysis['matchedPairs']) - 10} 对\n")

    if analysis["unresolvedSetups"]:
        lines.append("## 未回收的伏笔\n")
        for setup in analysis["unresolvedSetups"][:10]:
            label = TYPE_LABELS.get(setup["type"], setup["type"])
            lines.append(f"  [{label}] 位于 {setup['positionPercent']}%: \"{setup['text']}\"")
            lines.append(f"    上下文: {setup['lineContext']}")
            lines.append("")

    if analysis["orphanedPayoffs"]:
        lines.append("## 缺少铺垫的回收（天降神兵风险）\n")
        for payoff in analysis["orphanedPayoffs"][:10]:
            label = TYPE_LABELS.get(payoff["type"], payoff["type"])
            lines.append(f"  [{label}] 位于 {payoff['positionPercent']}%: \"{payoff['text']}\"")
            lines.append(f"    上下文: {payoff['lineContext']}")
            lines.append("")

    if analysis["issues"]:
        lines.append("## 问题\n")
        for issue in analysis["issues"]:
            lines.append(f"  - {issue}")
        lines.append("")

    if analysis["recommendations"]:
        lines.append("## 建议\n")
        for rec in analysis["recommendations"]:
            lines.append(f"  - {rec}")
        lines.append("")

    return "\n".join(lines)


# ---------------------------------------------------------------------------
# 入口
# ---------------------------------------------------------------------------

def main():
    args = sys.argv[1:]

    if "--help" in args or "-h" in args:
        print("""伏笔-回收追踪器

用法:
  python setup_payoff.py --analyze <文件>
  python setup_payoff.py --setup "关键词" --file <文件>
  python setup_payoff.py --list <文件>

模式:
  --analyze      完整伏笔-回收分析
  --setup "X"    在故事中搜索特定关键词
  --list         列出所有检测到的铺垫与回收

选项:
  --file <f>     指定输入文件
  --text "..."   直接提供文本
  --json         以 JSON 格式输出
  --help         显示此帮助信息

检测类型:
  - 物品铺垫（契诃夫之枪）
  - 技能铺垫（修炼/能力）
  - 角色铺垫（盟友、仇敌）
  - 信息铺垫（秘密、知识）
  - 威胁铺垫（警告、预示）
  - 承诺铺垫（誓言、约定）
  - 伏笔/预示（命运暗示）
""")
        sys.exit(0)

    json_output = "--json" in args
    text = ""
    file_name = "input"

    # --text 标志用于内联文本
    if "--text" in args:
        idx = args.index("--text")
        text = " ".join(args[idx + 1:])
        # 截取到下一个 -- 标志为止
        parts = []
        for part in args[idx + 1:]:
            if part.startswith("--"):
                break
            parts.append(part)
        text = " ".join(parts)
    else:
        # 通过 --file 或位置参数获取文件
        if "--file" in args:
            file_idx = args.index("--file")
            if file_idx + 1 < len(args):
                file_name = args[file_idx + 1]
                try:
                    with open(file_name, "r", encoding="utf-8") as f:
                        text = f.read()
                except Exception as e:
                    print(f"读取文件出错: {e}", file=sys.stderr)
                    sys.exit(1)
        else:
            # 尝试将位置参数作为文件路径（非标志参数，且非 --setup 的值）
            setup_idx = args.index("--setup") if "--setup" in args else -1
            for a in args:
                if a.startswith("--"):
                    continue
                # 跳过 --setup 后面的值
                if setup_idx >= 0 and args.index(a) == setup_idx + 1:
                    continue
                file_name = a
                try:
                    with open(a, "r", encoding="utf-8") as f:
                        text = f.read()
                except Exception as e:
                    print(f"读取文件出错: {e}", file=sys.stderr)
                    sys.exit(1)
                break

    if not text.strip():
        print("未提供文本。请使用 --file <路径>、--text \"...\" 或直接提供文件路径作为参数。",
              file=sys.stderr)
        sys.exit(1)

    # --- 搜索特定铺垫 ---
    if "--setup" in args:
        setup_idx = args.index("--setup")
        if setup_idx + 1 >= len(args):
            print("错误: --setup 需要一个搜索关键词", file=sys.stderr)
            sys.exit(1)
        term = args[setup_idx + 1]

        result = search_for_term(text, term)
        if json_output:
            print(json.dumps(result, ensure_ascii=False, indent=2))
        else:
            print(f"\n# 搜索 \"{term}\"\n")
            if result["found"]:
                print(f"找到 {len(result['occurrences'])} 处:\n")
                for occ in result["occurrences"]:
                    print(f"  位于 {occ['percent']}%: {occ['context']}\n")
            else:
                print("在文本中未找到该关键词。")
        sys.exit(0)

    # --- 列表模式 ---
    if "--list" in args:
        setups = find_setups(text)
        payoffs = find_payoffs(text)

        if json_output:
            print(json.dumps({"setups": setups, "payoffs": payoffs},
                             ensure_ascii=False, indent=2))
        else:
            print("\n# 检测到的铺垫（前 70%）\n")
            for s in setups:
                label = TYPE_LABELS.get(s["type"], s["type"])
                print(f"  [{label}] {s['positionPercent']}%: \"{s['text']}\"")
            print("\n# 检测到的回收（后 50%）\n")
            for p in payoffs:
                label = TYPE_LABELS.get(p["type"], p["type"])
                print(f"  [{label}] {p['positionPercent']}%: \"{p['text']}\"")
        sys.exit(0)

    # --- 完整分析（默认 / --analyze） ---
    analysis = analyze_setup_payoff(text, file_name)

    if json_output:
        print(json.dumps(analysis, ensure_ascii=False, indent=2))
    else:
        print(format_report(analysis))


if __name__ == "__main__":
    main()
