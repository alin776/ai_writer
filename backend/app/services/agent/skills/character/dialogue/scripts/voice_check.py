#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
voice_check.py - 对话声音辨识度分析器

分析对话文本，衡量每位角色说话风格的独特性。
比较词汇、句式、语气词等特征，判断角色声音是否足够区分。

Usage:
  python voice_check.py <file>
  python voice_check.py --text "对话内容"
"""

import sys
import re
import json
import os


# ── 中文停用词 ──────────────────────────────────────────────────────
STOP_WORDS = {
    "的", "了", "是", "在", "我", "他", "她", "你", "不", "有",
    "这", "那", "就", "都", "也", "人", "来", "到", "说", "要",
    "会", "能", "对", "着", "和", "而", "被", "把", "让", "给",
    "从", "向", "于", "与", "但", "却", "又", "还", "很", "最",
    "已", "才", "只", "将", "去", "过", "吗", "吧", "呢", "啊",
    "么", "个", "们", "地", "得", "里", "上", "下", "中", "大",
    "小", "为", "之", "其", "所", "以", "如", "此", "些", "时",
}

# ── 语气词集合 ──────────────────────────────────────────────────────
MOOD_PARTICLES = {"啊", "呀", "嘛", "呢", "吧", "哦", "哟", "嗯", "哼",
                  "嘿", "喂", "唉", "哎", "噢", "嘻", "呵", "嗷", "哇",
                  "诶", "呐", "咦", "哈", "嘁", "嘘", "喔", "咳", "噫"}

# ── 言说动词（按长度降序排列，确保正则优先匹配更长的动词）────────
SPEECH_VERBS = (
    "说", "道", "喊", "叫", "问", "答",
    "笑道", "冷笑道", "淡淡道", "沉声道", "低声道",
    "怒道", "叹道", "嘀咕道", "嗤笑道", "冷哼道",
    "问道", "答道", "哼道", "喝道", "嘟囔道",
    "轻声道", "厉声道", "柔声道", "急道", "缓缓道",
    "冷声道", "嘶声道", "朗声道", "笑着说", "哭着说",
    "吼道", "嚷道", "喃喃道", "自语道", "插嘴道",
)

_VERB_PATTERN = "|".join(sorted(SPEECH_VERBS, key=len, reverse=True))

# ── 常见修饰词（出现在角色名与言说动词之间的描述性词语）─────────
_MODIFIERS = (
    "惊讶", "惊喜", "惊呼", "点头", "摇头", "冷冷", "淡淡",
    "微微", "缓缓", "轻轻", "狠狠", "慢慢", "默默", "忽然",
    "突然", "赶紧", "连忙", "急忙", "立刻", "马上", "终于",
    "无奈", "尴尬", "得意", "不满", "不屑", "愤怒", "生气",
    "高兴", "开心", "伤心", "难过", "激动", "兴奋", "紧张",
    "担心", "好奇", "疑惑", "迟疑", "犹豫", "认真", "严肃",
    "温柔", "冰冷", "平静", "坦然", "苦笑", "微笑", "大笑",
    "哈哈", "嘿嘿", "呵呵", "嗤笑", "冷哼", "皱眉", "蹙眉",
    "低头", "抬头", "转头", "回头", "侧头", "歪头", "叹气",
    "咬牙", "哽咽", "颤声", "厉声", "沉声", "低声", "朗声",
)
_MOD_PATTERN = "|".join(sorted(_MODIFIERS, key=len, reverse=True))


# ═══════════════════════════════════════════════════════════════════
# 对话提取
# ═══════════════════════════════════════════════════════════════════

def _extract_name(raw):
    """从正则捕获的原始字符串中提取角色名（去除修饰词后缀）。"""
    # 尝试从尾部去除已知修饰词
    cleaned = re.sub(r'(?:' + _MOD_PATTERN + r')+$', '', raw)
    if 2 <= len(cleaned) <= 4:
        return cleaned
    # 原始串本身长度合适就直接用
    if 2 <= len(raw) <= 4:
        return raw
    # 最后兜底：取前 2~3 个字
    return raw[:min(3, len(raw))]


def extract_dialogue(text):
    """
    从中文小说文本中提取角色对话。

    支持的格式:
      - "对话内容，"角色名道。
      - "对话内容。"角色名说。
      - 角色名说："对话内容。"
      - 角色名道："对话内容"
      - 「对话内容」角色名道。
      - 角色名说：「对话内容」
    """
    speakers = {}

    def _add(speaker, dialogue):
        speaker = speaker.strip()
        dialogue = dialogue.strip()
        if not speaker or not dialogue:
            return
        # 过滤明显不是人名的匹配（纯标点或数字）
        if re.fullmatch(r'[\d\s\W]+', speaker):
            return
        if speaker not in speakers:
            speakers[speaker] = []
        speakers[speaker].append(dialogue)

    # ── 模式1: "对话"角色名(+修饰词)+言说动词  ─────────────────
    #   例: "你怎么来了？"林小雨惊讶道。
    #   引号对话 → 2~8字(角色名+可能的修饰) → 言说动词
    #   使用 lazy 量词让名字尽量短，动词尽量长
    p1 = re.compile(
        r'["\u201c\u300c]([^\u201d"\u300d]+)["\u201d\u300d]\s*'
        r'([\u4e00-\u9fff]{2,8}?)'
        r'(?:' + _VERB_PATTERN + r')',
    )

    # ── 模式2: 角色名(+修饰词)+言说动词+：+"对话"  ───────────────
    #   例: 张大勇沉声道："城外发现了魔兽。"
    p2 = re.compile(
        r'([\u4e00-\u9fff]{2,8}?)'
        r'(?:' + _VERB_PATTERN + r')'
        r'\s*[：:]\s*'
        r'["\u201c\u300c]([^\u201d"\u300d]+)["\u201d\u300d]',
    )

    # ── 模式3: 角色名+言说动词+，+"对话"（逗号引出变体）──────────
    #   例: 林小雨急道，"什么事？"
    p3 = re.compile(
        r'([\u4e00-\u9fff]{2,8}?)'
        r'(?:' + _VERB_PATTERN + r')'
        r'\s*[，,]\s*'
        r'["\u201c\u300c]([^\u201d"\u300d]+)["\u201d\u300d]',
    )

    matched_spans = set()

    for m in p1.finditer(text):
        name = _extract_name(m.group(2))
        _add(name, m.group(1))
        matched_spans.add(m.span())

    for m in p2.finditer(text):
        if m.span() not in matched_spans:
            name = _extract_name(m.group(1))
            _add(name, m.group(2))
            matched_spans.add(m.span())

    for m in p3.finditer(text):
        if m.span() not in matched_spans:
            name = _extract_name(m.group(1))
            _add(name, m.group(2))
            matched_spans.add(m.span())

    # ── 兜底: 纯引号对话（无法识别说话人时按序编号）──────────────
    if not speakers:
        bare = re.compile(
            r'["\u201c\u300c]([\u4e00-\u9fff\w，。！？、；：…—\s]+)["\u201d\u300d]'
        )
        idx = 0
        for m in bare.finditer(text):
            idx += 1
            _add(f"角色{idx}", m.group(1))

    return speakers


# ═══════════════════════════════════════════════════════════════════
# 中文分词 / 词汇分析
# ═══════════════════════════════════════════════════════════════════

def _split_sentences(dialogue):
    """将一段对话按标点拆分为子句列表。"""
    parts = re.split(r'[。！？；…\n]+', dialogue)
    return [p.strip() for p in parts if p.strip()]


def _extract_bigrams(text):
    """从纯中文文本中提取双字词（bigram）。"""
    chars = re.findall(r'[\u4e00-\u9fff]', text)
    bigrams = []
    for i in range(len(chars) - 1):
        bg = chars[i] + chars[i + 1]
        # 排除双字停用词组合
        if chars[i] not in STOP_WORDS or chars[i + 1] not in STOP_WORDS:
            bigrams.append(bg)
    return bigrams


def analyze_vocabulary(lines):
    """分析词汇：统计双字词频率和独特词集合。"""
    bigram_counts = {}
    unique = set()
    for line in lines:
        bigrams = _extract_bigrams(line)
        for bg in bigrams:
            unique.add(bg)
            bigram_counts[bg] = bigram_counts.get(bg, 0) + 1
    sorted_bigrams = sorted(bigram_counts.items(), key=lambda x: x[1], reverse=True)
    return unique, sorted_bigrams[:10]


# ═══════════════════════════════════════════════════════════════════
# 语音特征指标
# ═══════════════════════════════════════════════════════════════════

def count_mood_particles(lines):
    """语气词使用率：语气词字数 / 总字数。"""
    total_chars = 0
    mood_count = 0
    for line in lines:
        chars = re.findall(r'[\u4e00-\u9fff]', line)
        total_chars += len(chars)
        for c in chars:
            if c in MOOD_PARTICLES:
                mood_count += 1
    return mood_count / total_chars if total_chars > 0 else 0


def count_short_sentences(lines):
    """短句率：长度 < 10 字的子句占比。"""
    total = 0
    short = 0
    for line in lines:
        sents = _split_sentences(line)
        for s in sents:
            char_len = len(re.findall(r'[\u4e00-\u9fff]', s))
            total += 1
            if char_len < 10:
                short += 1
    return short / total if total > 0 else 0


def count_questions(lines):
    """疑问句比率：以？结尾的子句占比。"""
    total = 0
    questions = 0
    for line in lines:
        sents = _split_sentences(line)
        total += max(len(sents), 1)
        questions += line.count("\uff1f") + line.count("?")
    return questions / total if total > 0 else 0


def count_exclamations(lines):
    """感叹句比率：以！结尾的子句占比。"""
    total = 0
    exclamations = 0
    for line in lines:
        sents = _split_sentences(line)
        total += max(len(sents), 1)
        exclamations += line.count("\uff01") + line.count("!")
    return exclamations / total if total > 0 else 0


def avg_sentence_length(lines):
    """平均子句长度（字数）。"""
    total_chars = 0
    total_sents = 0
    for line in lines:
        sents = _split_sentences(line)
        for s in sents:
            char_len = len(re.findall(r'[\u4e00-\u9fff]', s))
            total_chars += char_len
            total_sents += 1
    return total_chars / total_sents if total_sents > 0 else 0


# ═══════════════════════════════════════════════════════════════════
# 角色分析
# ═══════════════════════════════════════════════════════════════════

def analyze_speaker(name, lines):
    """对单个角色的所有对话进行综合分析。"""
    unique_bigrams, top_bigrams = analyze_vocabulary(lines)
    total_chars = sum(len(re.findall(r'[\u4e00-\u9fff]', l)) for l in lines)
    return {
        'name': name,
        'line_count': len(lines),
        'char_count': total_chars,
        'avg_chars_per_line': total_chars / len(lines) if lines else 0,
        'avg_sentence_length': avg_sentence_length(lines),
        'vocabulary_size': len(unique_bigrams),
        'mood_particle_rate': count_mood_particles(lines),
        'question_rate': count_questions(lines),
        'exclamation_rate': count_exclamations(lines),
        'short_sentence_rate': count_short_sentences(lines),
        'unique_bigrams': unique_bigrams,
        'top_bigrams': top_bigrams,
    }


# ═══════════════════════════════════════════════════════════════════
# 综合对比
# ═══════════════════════════════════════════════════════════════════

def calculate_variance(values):
    """计算方差。"""
    if len(values) < 2:
        return 0
    mean = sum(values) / len(values)
    squared_diffs = [(v - mean) ** 2 for v in values]
    return sum(squared_diffs) / len(squared_diffs)


def calculate_overlap(speaker_stats):
    """计算角色间词汇重叠度（Jaccard 相似系数均值）。"""
    all_sets = [stats['unique_bigrams'] for stats in speaker_stats.values()]
    if len(all_sets) < 2:
        return 0
    total_overlap = 0
    pairs = 0
    for i in range(len(all_sets)):
        for j in range(i + 1, len(all_sets)):
            intersection = all_sets[i] & all_sets[j]
            union = all_sets[i] | all_sets[j]
            if union:
                total_overlap += len(intersection) / len(union)
            pairs += 1
    return total_overlap / pairs if pairs > 0 else 0


def analyze_voices(speaker_data):
    """对所有角色进行声音辨识度分析。"""
    speaker_stats = {}
    for name, lines in speaker_data.items():
        speaker_stats[name] = analyze_speaker(name, lines)

    patterns = []
    speaker_names = list(speaker_stats.keys())

    if len(speaker_names) >= 2:
        metrics = [
            ('avg_chars_per_line', '每句平均字数'),
            ('avg_sentence_length', '子句平均长度'),
            ('mood_particle_rate', '语气词使用率'),
            ('question_rate', '疑问句频率'),
            ('exclamation_rate', '感叹句频率'),
            ('short_sentence_rate', '短句率'),
        ]
        for metric_key, metric_label in metrics:
            values = {}
            nums = []
            for name in speaker_names:
                val = speaker_stats[name][metric_key]
                values[name] = val
                nums.append(val)
            variance = calculate_variance(nums)
            patterns.append({
                'metric': metric_label,
                'values': values,
                'variance': variance,
                'distinct': variance > 0.01,
            })

    vocabulary_overlap = calculate_overlap(speaker_stats)

    distinct_patterns = sum(1 for p in patterns if p['distinct'])
    pattern_score = (distinct_patterns / max(len(patterns), 1)) * 50
    overlap_score = (1 - vocabulary_overlap) * 50
    overall_distinctiveness = round(pattern_score + overlap_score)

    issues = []
    recommendations = []

    if vocabulary_overlap > 0.6:
        issues.append("角色间词汇重叠度过高")
        recommendations.append("为每个角色设计专属用语、口头禅或特定领域词汇")

    if sum(1 for p in patterns if not p['distinct']) > len(patterns) / 2:
        issues.append("角色语言模式过于相似")
        recommendations.append("调整不同角色的句式长短、语气轻重、正式程度")

    low_mood = [s for s in speaker_stats.values() if s['mood_particle_rate'] < 0.02]
    if len(low_mood) == len(speaker_stats) and len(speaker_stats) > 0:
        issues.append("所有角色语气词使用率偏低——对话可能显得生硬")
        recommendations.append("适当加入语气词（啊、嘛、呢、吧、哦等）使对话更自然")

    all_questions = [s for s in speaker_stats.values() if s['question_rate'] > 0.5]
    if len(all_questions) > len(speaker_stats) / 2:
        issues.append("大部分角色疑问句过多——可能存在\"问答式灌水\"倾向")
        recommendations.append("减少不必要的疑问，用陈述或动作描写推进对话")

    high_short = [s for s in speaker_stats.values() if s['short_sentence_rate'] > 0.8]
    if len(high_short) == len(speaker_stats) and len(speaker_stats) > 0:
        issues.append("所有角色短句率均偏高——对话可能缺乏节奏变化")
        recommendations.append("混合使用长短句，为不同角色设计不同的句式节奏")

    if len(speaker_stats) < 2:
        issues.append("需要至少两个角色才能进行声音辨识度对比")

    return {
        'speakers': speaker_stats,
        'overall_distinctiveness': overall_distinctiveness,
        'vocabulary_overlap': vocabulary_overlap,
        'patterns_comparison': patterns,
        'issues': issues,
        'recommendations': recommendations,
    }


# ═══════════════════════════════════════════════════════════════════
# 报告输出
# ═══════════════════════════════════════════════════════════════════

def format_report(analysis):
    """生成中文 Markdown 格式的分析报告。"""
    lines = []

    score = analysis['overall_distinctiveness']
    if score >= 80:
        verdict = "优秀——角色声音高度区分"
    elif score >= 60:
        verdict = "良好——角色有一定辨识度"
    elif score >= 40:
        verdict = "一般——角色声音区分不够明显"
    else:
        verdict = "较差——角色声音趋于同质化"

    lines.append("# 对话声音辨识度分析\n")
    lines.append(f"总体辨识度评分: {score}/100 （{verdict}）")
    lines.append(f"词汇重叠度: {analysis['vocabulary_overlap'] * 100:.1f}%\n")

    lines.append("## 角色画像\n")
    for name, stats in analysis['speakers'].items():
        lines.append(f"### {name}")
        lines.append(f"  对话条数: {stats['line_count']} | 总字数: {stats['char_count']}")
        lines.append(f"  每条平均字数: {stats['avg_chars_per_line']:.1f}")
        lines.append(f"  子句平均长度: {stats['avg_sentence_length']:.1f} 字")
        lines.append(f"  语气词使用率: {stats['mood_particle_rate'] * 100:.1f}%")
        lines.append(f"  疑问句比率: {stats['question_rate'] * 100:.1f}%")
        lines.append(f"  感叹句比率: {stats['exclamation_rate'] * 100:.1f}%")
        lines.append(f"  短句率(<10字): {stats['short_sentence_rate'] * 100:.1f}%")
        lines.append(f"  词汇丰富度(双字词): {stats['vocabulary_size']}")
        if stats['top_bigrams']:
            top = "、".join(w for w, _ in stats['top_bigrams'][:5])
            lines.append(f"  高频用词: {top}")
        lines.append("")

    if analysis['patterns_comparison']:
        lines.append("## 模式对比\n")
        for pattern in analysis['patterns_comparison']:
            status = "[+] 有区分" if pattern['distinct'] else "[-] 趋同"
            values = "、".join(
                f"{name}: {val:.2f}" for name, val in pattern['values'].items()
            )
            lines.append(f"  [{status}] {pattern['metric']}: {values}")
        lines.append("")

    if analysis['issues']:
        lines.append("## 发现的问题\n")
        for issue in analysis['issues']:
            lines.append(f"  - {issue}")
        lines.append("")

    if analysis['recommendations']:
        lines.append("## 改进建议\n")
        for rec in analysis['recommendations']:
            lines.append(f"  - {rec}")
        lines.append("")

    return "\n".join(lines)


# ═══════════════════════════════════════════════════════════════════
# CLI 入口
# ═══════════════════════════════════════════════════════════════════

def main():
    args = sys.argv[1:]

    if '--help' in args or '-h' in args:
        print("voice_check - 对话声音辨识度分析器\n")
        print("用法:")
        print("  python voice_check.py <文件路径>")
        print('  python voice_check.py --text "对话内容"\n')
        print("选项:")
        print('  --text "..."  直接输入对话文本')
        print("  --json        以 JSON 格式输出")
        print("  --help        显示帮助信息\n")
        print("支持的对话格式:")
        print('  - \u201c对话内容，\u201d角色名道。')
        print('  - \u201c对话内容。\u201d角色名说。')
        print('  - 角色名说：\u201c对话内容。\u201d')
        print('  - 角色名道：\u201c对话内容\u201d')
        print('  - 「对话内容」角色名道。\n')
        print("本工具通过对比词汇、句式、语气词等特征，")
        print("衡量不同角色对话声音的独特性与区分度。")
        sys.exit(0)

    json_output = '--json' in args
    text = ""

    if '--text' in args:
        text_index = args.index('--text')
        text = args[text_index + 1] if text_index + 1 < len(args) else ""
    else:
        file_path = next((a for a in args if not a.startswith('--')), None)
        if file_path:
            file_path = os.path.normpath(file_path)
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    text = f.read()
            except Exception as e:
                print(f"读取文件出错: {e}", file=sys.stderr)
                sys.exit(1)

    if not text.strip():
        print("错误: 未提供文本。请使用 --text 或指定文件路径。", file=sys.stderr)
        sys.exit(1)

    speaker_data = extract_dialogue(text)

    if not speaker_data:
        print("错误: 无法提取对话。请检查格式（使用 --help 查看支持的格式）。", file=sys.stderr)
        sys.exit(1)

    analysis = analyze_voices(speaker_data)

    if json_output:
        json_safe = dict(analysis)
        json_safe['speakers'] = {
            k: {
                kk: (list(vv) if isinstance(vv, set) else vv)
                for kk, vv in v.items()
            }
            for k, v in analysis['speakers'].items()
        }
        print(json.dumps(json_safe, indent=2, ensure_ascii=False))
    else:
        print(format_report(analysis))


if __name__ == '__main__':
    main()
