#!/usr/bin/env python3
"""
ending_check.py - 结局结构分析工具

分析小说结局的结构和类型，识别常见问题模式。
适配中文网文文本（中文标点、分段、对话标记）。

Usage:
  python ending_check.py --analyze final-chapter.txt
  python ending_check.py --text "故事结局文本..."
  python ending_check.py --json --analyze final-chapter.txt
"""

import sys
import re
import json

# Ensure UTF-8 output on all platforms
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")
if hasattr(sys.stderr, "reconfigure"):
    sys.stderr.reconfigure(encoding="utf-8")

# ---------------------------------------------------------------------------
# 中文分句工具
# ---------------------------------------------------------------------------

_SENT_SPLIT = re.compile(r'[。！？…；\n]+')
_PARA_SPLIT = re.compile(r'\n\s*\n')


def split_sentences(text):
    """按中文标点分句，过滤空句。"""
    parts = _SENT_SPLIT.split(text)
    return [s.strip() for s in parts if s.strip()]


def split_paragraphs(text):
    """按空行分段，过滤空段。"""
    parts = _PARA_SPLIT.split(text)
    return [p.strip() for p in parts if p.strip()]


# ---------------------------------------------------------------------------
# 结局类型检测模式（中文关键词）
# ---------------------------------------------------------------------------

ENDING_TYPE_PATTERNS = {
    "封闭式": {
        "description": "所有主要问题都得到回答",
        "patterns": [
            re.compile(r'(终于|最终|结局|圆满|大结局|完结|从此|此后再也没有)'),
            re.compile(r'(一切.*尘埃落定|画上.*句号|落下.*帷幕|告一段落)'),
            re.compile(r'(真相大白|水落石出|各得其所|皆大欢喜)'),
        ],
    },
    "开放式": {
        "description": "部分问题未得到回答",
        "patterns": [
            re.compile(r'(也许|或许|谁知道|未来.*会|等待着|故事.*还没.*结束)'),
            re.compile(r'(远方|新的.*旅程|新的.*开始|路还很长|一切才刚刚开始)'),
            re.compile(r'(消失在|渐行渐远|不知.*去向|没人知道)'),
        ],
    },
    "反转式": {
        "description": "最终揭示重新定义整个故事",
        "patterns": [
            re.compile(r'(原来|竟然|没想到|万万没想到|真相.*竟是|一切都是)'),
            re.compile(r'(恍然大悟|如梦初醒|细思极恐|不寒而栗)'),
            re.compile(r'(这一刻.*才.*明白|所有.*谜团.*解开|隐藏.*真相)'),
        ],
    },
    "环形": {
        "description": "回到起点，但带有变化",
        "patterns": [
            re.compile(r'(又回到|再次.*站在|一切.*回到.*原点|轮回|重新)'),
            re.compile(r'(和.*一样|同样的|熟悉的|似曾相识|物是人非)'),
            re.compile(r'(不同的是|但这一次|只是这次|已经不再是)'),
        ],
    },
    "模糊式": {
        "description": "刻意留下模糊的解读空间",
        "patterns": [
            re.compile(r'(是真是假|亦真亦幻|虚实难辨|无人知晓)'),
            re.compile(r'(也许.*也许|或者.*或者|究竟.*还是)'),
            re.compile(r'(到底|梦境|幻觉|真实.*虚幻)'),
        ],
    },
}

# ---------------------------------------------------------------------------
# 解决 vs 扩散模式检测
# ---------------------------------------------------------------------------

RESOLUTION_PATTERNS = [
    re.compile(r'(解决|化解|平息|消除|挽回|重归|和解|回归)'),
    re.compile(r'(终于.*成功|问题.*解决|危机.*化解|冲突.*平息)'),
    re.compile(r'(尘埃落定|盖棺定论|水到渠成|功德圆满)'),
]

DIVERGENCE_PATTERNS = [
    re.compile(r'(新的.*问题|更大的.*危机|意想不到|突然.*出现|新的.*敌人)'),
    re.compile(r'(但是.*没有.*结束|然而.*才刚刚.*开始|另一个.*谜团)'),
    re.compile(r'(伏笔|暗流涌动|山雨欲来|隐患|潜在.*威胁)'),
]

# ---------------------------------------------------------------------------
# 反模式检测（结局常见问题）
# ---------------------------------------------------------------------------

ANTI_PATTERN_CHECKS = {
    "天降神兵": {
        "description": "外部力量突然解决问题",
        "patterns": [
            re.compile(r'(突然.*出现.*解救|从天而降|凭空.*出现|恰好.*赶到)'),
            re.compile(r'(神秘.*力量|不知.*从哪|意外.*获得|天意)'),
        ],
    },
    "主题演讲": {
        "description": "角色明确说出故事意义",
        "patterns": [
            re.compile(r'[""「」].*(?:人生.*就是|我.*明白了|原来.*道理|这就是.*意义|所谓.*就是).*[""」」]'),
            re.compile(r'(感慨地说|语重心长|意味深长地|沉声道.*人生)'),
        ],
    },
    "信息倾泻": {
        "description": "结尾冗长解释所有人命运",
        "patterns": [
            re.compile(r'(后来|多年后|数年之后|几年过去).*[，,].*(?:后来|多年后|数年之后)'),
            re.compile(r'(至于.*最终|而.*则是|另外.*后来)'),
        ],
    },
    "仓促收束": {
        "description": "高潮后立即结束，缺乏过渡",
        # 通过节奏指标间接检测，不使用正则
        "patterns": [],
    },
}

# ---------------------------------------------------------------------------
# 节奏分析
# ---------------------------------------------------------------------------

def analyze_pacing(text, sentences):
    """分析结局部分的节奏指标。"""
    total_len = len(text)
    total_sents = len(sentences)

    if total_sents < 3:
        return {
            "totalSentences": total_sents,
            "avgSentenceLength": total_len // max(total_sents, 1),
            "pacing": "insufficient_data",
            "pacingNote": "文本过短，无法判断节奏",
        }

    # 将文本分成前半（高潮区）和后半（收束区）
    mid = total_len // 2
    first_half_sents = [s for s in sentences if text.find(s) < mid]
    second_half_sents = [s for s in sentences if text.find(s) >= mid]

    avg_first = sum(len(s) for s in first_half_sents) / max(len(first_half_sents), 1)
    avg_second = sum(len(s) for s in second_half_sents) / max(len(second_half_sents), 1)

    # 段落分析
    paragraphs = split_paragraphs(text)
    total_paras = len(paragraphs)
    if total_paras >= 2:
        last_para_ratio = len(paragraphs[-1]) / (total_len / total_paras)
    else:
        last_para_ratio = 1.0

    # 节奏判断
    if total_sents <= 5 and total_len > 500:
        pacing = "rushed"
        note = "句子数量少但篇幅不短，可能缺乏过渡和消化空间"
    elif len(second_half_sents) > len(first_half_sents) * 2:
        pacing = "dragging"
        note = "后半部分句子密度远大于前半，收束可能过长"
    elif avg_second > avg_first * 1.5:
        pacing = "expanding"
        note = "后半段句子变长，可能在解释而非收束"
    elif avg_second < avg_first * 0.5 and len(second_half_sents) < 3:
        pacing = "abrupt"
        note = "后半段极短，可能缺乏下降动作"
    else:
        pacing = "balanced"
        note = "节奏较为均衡"

    return {
        "totalSentences": total_sents,
        "totalParagraphs": total_paras,
        "avgSentenceLengthFirst": round(avg_first),
        "avgSentenceLengthSecond": round(avg_second),
        "lastParagraphRatio": round(last_para_ratio, 2),
        "pacing": pacing,
        "pacingNote": note,
    }


# ---------------------------------------------------------------------------
# 结局类型得分
# ---------------------------------------------------------------------------

def detect_ending_types(text):
    """检测文本中各结局类型的匹配度。"""
    results = []
    for etype, config in ENDING_TYPE_PATTERNS.items():
        hits = 0
        evidence = []
        for pat in config["patterns"]:
            matches = pat.findall(text)
            if matches:
                hits += len(matches)
                for m in matches[:3]:  # 每类型最多3条证据
                    matched_text = m if isinstance(m, str) else m[0] if isinstance(m, tuple) else str(m)
                    if matched_text not in [e["text"] for e in evidence]:
                        # 找到匹配位置以获取上下文
                        pos = text.find(matched_text)
                        evidence.append({
                            "text": matched_text,
                            "context": get_context(text, pos) if pos >= 0 else "",
                        })
        if hits > 0:
            results.append({
                "type": etype,
                "description": config["description"],
                "hits": hits,
                "confidence": min(hits / 3.0, 1.0),
                "evidence": evidence[:3],
            })

    results.sort(key=lambda r: r["hits"], reverse=True)
    return results


# ---------------------------------------------------------------------------
# 解决/扩散比率
# ---------------------------------------------------------------------------

def detect_resolution_divergence(text):
    """检测解决模式与扩散模式的比率。"""
    resolution_hits = 0
    divergence_hits = 0
    resolution_evidence = []
    divergence_evidence = []

    for pat in RESOLUTION_PATTERNS:
        matches = pat.findall(text)
        resolution_hits += len(matches)
        for m in matches[:2]:
            matched = m if isinstance(m, str) else m[0]
            resolution_evidence.append(matched)

    for pat in DIVERGENCE_PATTERNS:
        matches = pat.findall(text)
        divergence_hits += len(matches)
        for m in matches[:2]:
            matched = m if isinstance(m, str) else m[0]
            divergence_evidence.append(matched)

    total = resolution_hits + divergence_hits
    if total == 0:
        pattern = "neutral"
        note = "未检测到明显的解决或扩散信号"
    elif resolution_hits > divergence_hits * 2:
        pattern = "resolution"
        note = "文本以解决/收束为主，结局倾向封闭"
    elif divergence_hits > resolution_hits * 2:
        pattern = "divergence"
        note = "文本出现较多扩散信号，可能是开放式结局或E4（扩散的结局）"
    elif divergence_hits > resolution_hits:
        pattern = "leaning_divergence"
        note = "扩散信号略多于解决信号"
    else:
        pattern = "leaning_resolution"
        note = "解决信号略多于扩散信号"

    return {
        "resolutionHits": resolution_hits,
        "divergenceHits": divergence_hits,
        "pattern": pattern,
        "note": note,
        "resolutionEvidence": resolution_evidence[:3],
        "divergenceEvidence": divergence_evidence[:3],
    }


# ---------------------------------------------------------------------------
# 反模式检测
# ---------------------------------------------------------------------------

def detect_anti_patterns(text, pacing_result):
    """检测结局中的常见反模式。"""
    found = []
    for name, config in ANTI_PATTERN_CHECKS.items():
        if name == "仓促收束":
            # 通过节奏指标检测
            if pacing_result.get("pacing") in ("rushed", "abrupt"):
                found.append({
                    "name": name,
                    "description": config["description"],
                    "evidence": pacing_result.get("pacingNote", ""),
                    "severity": "warning",
                })
            continue

        hits = 0
        evidence = []
        for pat in config["patterns"]:
            matches = pat.findall(text)
            hits += len(matches)
            for m in matches[:2]:
                matched = m if isinstance(m, str) else m[0]
                evidence.append(matched)

        if hits > 0:
            found.append({
                "name": name,
                "description": config["description"],
                "evidence": "、".join(evidence[:3]),
                "severity": "warning" if hits <= 2 else "problem",
            })

    return found


# ---------------------------------------------------------------------------
# 辅助函数
# ---------------------------------------------------------------------------

def get_context(text, position, window=30):
    """获取位置周围的上下文片段。"""
    start = max(0, position - window)
    end = min(len(text), position + window)
    ctx = text[start:end].replace("\n", " ").strip()
    if start > 0:
        ctx = "…" + ctx
    if end < len(text):
        ctx = ctx + "…"
    return ctx


# ---------------------------------------------------------------------------
# 综合分析
# ---------------------------------------------------------------------------

def analyze_ending(text, file_name="input"):
    """对文本执行完整的结局分析。"""
    sentences = split_sentences(text)
    char_count = len(text)
    word_count = len(text.replace(" ", "").replace("\n", ""))

    # 各维度分析
    ending_types = detect_ending_types(text)
    res_div = detect_resolution_divergence(text)
    pacing = analyze_pacing(text, sentences)
    anti_patterns = detect_anti_patterns(text, pacing)

    # 综合健康度评估
    issues = []
    recommendations = []

    # 基于结局类型
    if not ending_types:
        issues.append("未检测到明显的结局类型信号——文本可能不是结局部分")
    elif ending_types[0]["confidence"] < 0.3:
        issues.append("结局类型信号较弱，结局可能缺乏明确的收束感")

    # 基于解决/扩散
    if res_div["pattern"] == "divergence":
        issues.append("扩散信号远多于解决信号，可能存在E4（扩散的结局）问题")
        recommendations.append("检查是否在结局部分引入了新的问题或谜团，考虑将其移至更早位置")
    elif res_div["pattern"] == "neutral":
        issues.append("未检测到明显的解决或扩散信号")

    # 基于节奏
    if pacing["pacing"] == "rushed" or pacing["pacing"] == "abrupt":
        issues.append(f"节奏问题：{pacing['pacingNote']}")
        recommendations.append("考虑增加下降动作（高潮后的过渡），让读者有消化情感的空间")
    elif pacing["pacing"] == "dragging":
        issues.append(f"节奏问题：{pacing['pacingNote']}")
        recommendations.append("考虑精简后半段，在核心解决之后尽快结束")
    elif pacing["pacing"] == "expanding":
        issues.append(f"节奏问题：{pacing['pacingNote']}")
        recommendations.append("检查后半段是否有过多解释性内容，考虑以画面/行动结束")

    # 基于反模式
    for ap in anti_patterns:
        issues.append(f"反模式「{ap['name']}」：{ap['description']}")
        if ap["name"] == "天降神兵":
            recommendations.append("确保结局由主角的选择和行动驱动，避免外部力量凭空介入")
        elif ap["name"] == "主题演讲":
            recommendations.append("删掉角色直接说出主题的台词，改为通过行动和画面展示")
        elif ap["name"] == "信息倾泻":
            recommendations.append("精简尾声，不必交代每个人的结局——信任读者的想象力")

    # 健康度评级
    problem_count = len([a for a in anti_patterns if a["severity"] == "problem"])
    if problem_count > 0 or len(issues) > 3:
        health = "problems"
    elif len(issues) > 1:
        health = "issues"
    elif len(issues) == 1:
        health = "minor"
    else:
        health = "good"

    return {
        "fileName": file_name,
        "charCount": char_count,
        "wordCount": word_count,
        "sentenceCount": len(sentences),
        "endingTypes": ending_types,
        "resolutionDivergence": res_div,
        "pacing": pacing,
        "antiPatterns": anti_patterns,
        "health": health,
        "issues": issues,
        "recommendations": recommendations,
    }


# ---------------------------------------------------------------------------
# 报告格式化
# ---------------------------------------------------------------------------

def format_report(analysis):
    """生成人类可读的结局分析报告。"""
    lines = []

    lines.append("# 结局结构分析报告\n")
    lines.append(f"文件: {analysis['fileName']}")
    lines.append(f"字数: {analysis['charCount']}（含标点）")
    lines.append(f"句数: {analysis['sentenceCount']}")
    lines.append(f"健康度: {analysis['health'].upper()}\n")

    # 结局类型
    lines.append("## 结局类型检测\n")
    if analysis["endingTypes"]:
        for et in analysis["endingTypes"]:
            conf_bar = "●" * int(et["confidence"] * 5) + "○" * (5 - int(et["confidence"] * 5))
            lines.append(f"  [{conf_bar}] {et['type']}（{et['description']}）- {et['hits']} 处匹配")
            for ev in et["evidence"]:
                lines.append(f"    → \"{ev['text']}\" {ev['context']}")
            lines.append("")
    else:
        lines.append("  未检测到明确的结局类型信号\n")

    # 解决/扩散
    lines.append("## 解决 vs 扩散\n")
    rd = analysis["resolutionDivergence"]
    lines.append(f"  解决信号: {rd['resolutionHits']}  |  扩散信号: {rd['divergenceHits']}")
    lines.append(f"  模式: {rd['pattern']}")
    lines.append(f"  判断: {rd['note']}\n")

    # 节奏
    lines.append("## 节奏分析\n")
    p = analysis["pacing"]
    lines.append(f"  节奏评估: {p['pacing']}")
    lines.append(f"  说明: {p['pacingNote']}")
    if "avgSentenceLengthFirst" in p:
        lines.append(f"  前半段平均句长: {p['avgSentenceLengthFirst']} 字")
        lines.append(f"  后半段平均句长: {p['avgSentenceLengthSecond']} 字")
    lines.append("")

    # 反模式
    if analysis["antiPatterns"]:
        lines.append("## 检测到的反模式\n")
        for ap in analysis["antiPatterns"]:
            icon = "⚠️" if ap["severity"] == "warning" else "❌"
            lines.append(f"  {icon} {ap['name']}：{ap['description']}")
            if ap["evidence"]:
                lines.append(f"    证据: {ap['evidence']}")
            lines.append("")

    # 问题和建议
    if analysis["issues"]:
        lines.append("## 发现的问题\n")
        for issue in analysis["issues"]:
            lines.append(f"  - {issue}")
        lines.append("")

    if analysis["recommendations"]:
        lines.append("## 改进建议\n")
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
        print("""结局结构分析工具 (ending_check.py)

Usage:
  python ending_check.py --analyze <file>
  python ending_check.py --text "结局文本..."

Modes:
  --analyze      完整结局分析（默认模式）
  --types        仅检测结局类型

Options:
  --file <f>     指定输入文件
  --text "..."   直接提供文本
  --json         输出 JSON 格式
  --help         显示此帮助信息

检测内容:
  - 结局类型（封闭式/开放式/反转式/环形/模糊式）
  - 解决 vs 扩散模式
  - 节奏指标（仓促/冗长/均衡）
  - 反模式（天降神兵/主题演讲/信息倾泻/仓促收束）
""")
        sys.exit(0)

    json_output = "--json" in args
    text = ""
    file_name = "input"

    # --text flag for inline text
    if "--text" in args:
        idx = args.index("--text")
        parts = []
        for part in args[idx + 1:]:
            if part.startswith("--"):
                break
            parts.append(part)
        text = " ".join(parts)
    else:
        # Get file via --file or positional arg
        if "--file" in args:
            file_idx = args.index("--file")
            if file_idx + 1 < len(args):
                file_name = args[file_idx + 1]
                try:
                    with open(file_name, "r", encoding="utf-8") as f:
                        text = f.read()
                except Exception as e:
                    print(f"读取文件错误: {e}", file=sys.stderr)
                    sys.exit(1)
        else:
            # Try positional arg
            for a in args:
                if a.startswith("--"):
                    continue
                file_name = a
                try:
                    with open(a, "r", encoding="utf-8") as f:
                        text = f.read()
                except Exception as e:
                    print(f"读取文件错误: {e}", file=sys.stderr)
                    sys.exit(1)
                break

    if not text.strip():
        print("未提供文本。使用 --file <路径>、--text \"...\" 或直接提供文件路径。",
              file=sys.stderr)
        sys.exit(1)

    # --- Types only mode ---
    if "--types" in args:
        types = detect_ending_types(text)
        if json_output:
            print(json.dumps(types, ensure_ascii=False, indent=2))
        else:
            print("\n# 结局类型检测\n")
            if types:
                for t in types:
                    print(f"  {t['type']}（{t['description']}）- {t['hits']} 处匹配")
            else:
                print("  未检测到明确的结局类型信号")
        sys.exit(0)

    # --- Full analysis (default / --analyze) ---
    analysis = analyze_ending(text, file_name)

    if json_output:
        print(json.dumps(analysis, ensure_ascii=False, indent=2))
    else:
        print(format_report(analysis))


if __name__ == "__main__":
    main()
