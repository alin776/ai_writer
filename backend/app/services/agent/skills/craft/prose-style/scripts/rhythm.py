#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
rhythm.py - 中文散文节奏分析工具

分析内容:
- 句子长度分布（按字符数）
- 段落长度变化
- 首词多样性
- 节奏评分（多样性指标）

用法:
  python rhythm.py <file>
  python rhythm.py --text "他站在窗前。外面的雨已经下了三天三夜，丝毫没有停歇的意思。"
  python rhythm.py --json <file>
  python rhythm.py --help
"""

import sys
import re
import json
import math
import os


# ---------------------------------------------------------------------------
# 中文标点集合
# ---------------------------------------------------------------------------
# 用于断句的终止标点
_SENTENCE_TERMINATORS = set('。！？')
# 省略号和破折号需要特殊处理
_ELLIPSIS = '……'
_EM_DASH = '——'
# 所有中文标点（用于从字符计数中剔除）
_ALL_PUNCTUATION = set(
    '。，、；：！？''""（）【】《》〈〉「」『』〔〕'
    '——……·–—―‐‑‒．﹏~～♪'
    ',.;:!?\'\"()[]{}/<>@#$%^&*-_+=|\\`'
)


def split_into_paragraphs(text):
    """按空行拆分段落。"""
    return [p.strip() for p in re.split(r'\n\s*\n', text) if p.strip()]


def split_into_sentences(text):
    """
    按中文终止标点拆分句子。

    处理规则:
    - 。！？ 作为句子终止符
    - …… (中文省略号) 作为句子终止符，不拆成两个 …
    - —— (中文破折号) 作为句子终止符
    - 连续标点只算一次断句（如 ！！！ 或 ？！）
    - ；(分号) 也作为断句符，因为网文中分号常分隔独立语义
    """
    # 先将 …… 和 —— 替换为占位符，避免被逐字符处理干扰
    processed = text.replace(_ELLIPSIS, '\x00')
    processed = processed.replace(_EM_DASH, '\x01')

    # 用正则按终止标点或占位符断句
    # 终止符: 。！？；以及占位符 \x00 \x01
    parts = re.split(r'[\x00\x01。！？；]+', processed)
    sentences = []
    for part in parts:
        s = part.strip()
        # 去掉段落间残留换行
        s = re.sub(r'\s+', '', s)
        if s:
            sentences.append(s)
    return sentences


def count_chinese_chars(text):
    """
    统计有效中文字符数（排除标点和空白）。

    这里的"字符"包括:
    - CJK 统一汉字
    - 字母和数字（混排场景）
    不包括:
    - 标点符号
    - 空白字符
    """
    count = 0
    for ch in text:
        if ch in _ALL_PUNCTUATION:
            continue
        if ch.isspace():
            continue
        count += 1
    return count


def get_opening_chars(sentence, n=2):
    """
    提取句子的首 n 个有效字符（跳过标点和空白）。

    网文中常见问题是大量句子以 他/她/我/那/这 开头，
    提取前两个字可以更精准地检测重复模式（如 "他的"、"她的"）。
    """
    chars = []
    for ch in sentence:
        if ch in _ALL_PUNCTUATION or ch.isspace():
            continue
        chars.append(ch)
        if len(chars) >= n:
            break
    return ''.join(chars)


def calculate_std_dev(values, mean):
    """计算标准差。"""
    if len(values) < 2:
        return 0.0
    squared_diffs = [(v - mean) ** 2 for v in values]
    return math.sqrt(sum(squared_diffs) / len(values))


def analyze_sentences(sentences):
    """
    分析句子长度分布。

    长度类别（按字符数）:
    - 短句: < 15 字
    - 中句: 15-30 字
    - 长句: 31-50 字
    - 超长句: > 50 字
    """
    lengths = [count_chinese_chars(s) for s in sentences]
    # 过滤掉长度为 0 的（理论上 split 已排除，保险起见）
    lengths = [l for l in lengths if l > 0]

    short = sum(1 for l in lengths if l < 15)
    medium = sum(1 for l in lengths if 15 <= l <= 30)
    long_ = sum(1 for l in lengths if 31 <= l <= 50)
    very_long = sum(1 for l in lengths if l > 50)
    total = len(lengths)
    avg = sum(lengths) / total if total else 0
    std = calculate_std_dev(lengths, avg)
    # 多样性评分：标准差越大越好，以 8 个字符的标准差为满分基准
    variety = min(100, (std / 8) * 100) if total > 0 else 0
    return {
        'total': total, 'lengths': lengths,
        'short': short, 'medium': medium, 'long': long_, 'very_long': very_long,
        'avg_length': avg, 'std_dev': std, 'variety_score': variety,
    }


def analyze_paragraphs(paragraphs):
    """
    分析段落长度分布（以段落内句子数衡量）。

    类别:
    - 短段: 1-2 句
    - 中段: 3-5 句
    - 长段: 6 句及以上
    """
    lengths = [len(split_into_sentences(p)) for p in paragraphs]
    short = sum(1 for l in lengths if l <= 2)
    medium = sum(1 for l in lengths if 3 <= l <= 5)
    long_ = sum(1 for l in lengths if l >= 6)
    avg = sum(lengths) / len(lengths) if lengths else 0
    total = len(paragraphs)
    variety = 0
    if total > 0:
        cats = sum(1 for x in [short > 0, medium > 0, long_ > 0] if x)
        variety = (cats / 3) * 100
    return {
        'total': total, 'lengths': lengths,
        'short': short, 'medium': medium, 'long': long_,
        'avg_length': avg, 'variety_score': variety,
    }


def analyze_openings(sentences):
    """
    分析句子首词（前两个字符）的多样性。

    网文常见问题：大量句子以 他、她、我、这、那 等代词开头，
    如果某个首词占比超过 15%，发出警告。
    """
    openings = {}
    for sentence in sentences:
        opening = get_opening_chars(sentence, 2)
        if opening:
            openings[opening] = openings.get(opening, 0) + 1

    sorted_openings = sorted(openings.items(), key=lambda x: x[1], reverse=True)
    top = sorted_openings[:10]
    total = len(sentences)
    unique_ratio = len(openings) / total if total else 0

    # 警告阈值：至少出现 3 次，且占比超过 15%
    threshold_count = max(3, int(total * 0.15))
    warnings = []
    for word, count in sorted_openings:
        if count >= threshold_count:
            pct_val = int(count / total * 100) if total else 0
            warnings.append(
                '「{}」开头出现 {} 次（占 {}%），建议变换句式'.format(word, count, pct_val)
            )

    return {
        'openings': openings, 'unique_ratio': unique_ratio,
        'top_openings': top, 'warnings': warnings,
    }


def calculate_rhythm_score(sentences, paragraphs, openings):
    """
    综合节奏评分。

    权重:
    - 句子长度多样性: 40%
    - 段落长度多样性: 30%
    - 首词多样性: 30%
    """
    return (
        sentences['variety_score'] * 0.4
        + paragraphs['variety_score'] * 0.3
        + openings['unique_ratio'] * 100 * 0.3
    )


def get_verdict(sentences, paragraphs, openings):
    """生成诊断结论。"""
    issues = []
    if sentences['variety_score'] < 30:
        issues.append('句子长度变化不足')
    if sentences['short'] == 0 and sentences['total'] > 5:
        issues.append('缺少短句（短句能制造紧张感和节奏感）')
    if sentences['long'] == 0 and sentences['very_long'] == 0 and sentences['total'] > 5:
        issues.append('缺少长句（长句能营造铺陈和沉浸感）')
    if paragraphs['variety_score'] < 50:
        issues.append('段落长度缺少变化')
    if openings['warnings']:
        issues.append('句子开头重复')

    if not issues:
        return '节奏丰富'
    elif len(issues) <= 2:
        return '部分节奏问题：' + '；'.join(issues)
    else:
        return '节奏单调：' + '；'.join(issues)


def analyze_text(text):
    """主分析入口，返回完整分析结果字典。"""
    paragraphs = split_into_paragraphs(text)
    sentences = split_into_sentences(text)

    if not sentences:
        return {
            'sentences': {
                'total': 0, 'lengths': [], 'short': 0, 'medium': 0,
                'long': 0, 'very_long': 0, 'avg_length': 0,
                'std_dev': 0, 'variety_score': 0,
            },
            'paragraphs': {
                'total': 0, 'lengths': [], 'short': 0, 'medium': 0,
                'long': 0, 'avg_length': 0, 'variety_score': 0,
            },
            'openings': {
                'openings': {}, 'unique_ratio': 0,
                'top_openings': [], 'warnings': [],
            },
            'rhythm_score': 0,
            'verdict': '文本为空，无法分析',
        }

    s = analyze_sentences(sentences)
    p = analyze_paragraphs(paragraphs)
    o = analyze_openings(sentences)
    score = calculate_rhythm_score(s, p, o)
    verdict = get_verdict(s, p, o)
    return {
        'sentences': s, 'paragraphs': p, 'openings': o,
        'rhythm_score': score, 'verdict': verdict,
    }


def format_histogram(lengths, bucket_size=5):
    """生成字符长度分布的 ASCII 直方图。"""
    if not lengths:
        return ''
    buckets = {}
    for l in lengths:
        b = (l // bucket_size) * bucket_size
        buckets[b] = buckets.get(b, 0) + 1
    sorted_b = sorted(buckets.items())
    if not sorted_b:
        return ''
    mx = max(c for _, c in sorted_b)
    scale = min(30, mx)
    lines = []
    for bk, cnt in sorted_b:
        bar_len = round((cnt / mx) * scale) if mx > 0 else 0
        label = '{}-{}'.format(str(bk).rjust(2), str(bk + bucket_size - 1).ljust(2))
        lines.append('    {}: {} ({})'.format(label, '=' * bar_len, cnt))
    return '\n'.join(lines) + '\n'


def pct(n, total):
    """计算百分比（整数）。"""
    return int(n / total * 100) if total > 0 else 0


def format_report(a):
    """格式化分析报告（中文输出）。"""
    s = a['sentences']
    p = a['paragraphs']
    o = a['openings']
    sc = a['rhythm_score']
    v = a['verdict']

    lines = []
    lines.append('')
    lines.append('节奏分析报告')
    lines.append('============')
    lines.append('')
    lines.append('综合节奏评分: {:.0f}/100'.format(sc))
    lines.append('诊断结论: {}'.format(v))

    # ---- 句子长度 ----
    lines.append('')
    lines.append('【句子长度分析】')
    lines.append('  句子总数: {}'.format(s['total']))
    lines.append('  平均长度: {:.1f} 字'.format(s['avg_length']))
    lines.append('  标准差: {:.1f}'.format(s['std_dev']))
    lines.append('  多样性评分: {:.0f}/100'.format(s['variety_score']))
    lines.append('')
    lines.append('  长度分布:')
    lines.append('    短句（<15字）:   {} （{}%）'.format(
        s['short'], pct(s['short'], s['total'])))
    lines.append('    中句（15-30字）: {} （{}%）'.format(
        s['medium'], pct(s['medium'], s['total'])))
    lines.append('    长句（31-50字）: {} （{}%）'.format(
        s['long'], pct(s['long'], s['total'])))
    lines.append('    超长句（>50字）: {} （{}%）'.format(
        s['very_long'], pct(s['very_long'], s['total'])))
    lines.append('')
    lines.append('  字数分布直方图:')
    lines.append(format_histogram(s['lengths'], 5))

    # ---- 段落长度 ----
    lines.append('【段落长度分析】')
    lines.append('  段落总数: {}'.format(p['total']))
    lines.append('  平均长度: {:.1f} 句'.format(p['avg_length']))
    lines.append('  多样性评分: {:.0f}/100'.format(p['variety_score']))
    lines.append('')
    lines.append('  长度分布:')
    lines.append('    短段（1-2句）: {} （{}%）'.format(
        p['short'], pct(p['short'], p['total'])))
    lines.append('    中段（3-5句）: {} （{}%）'.format(
        p['medium'], pct(p['medium'], p['total'])))
    lines.append('    长段（6句+）:  {} （{}%）'.format(
        p['long'], pct(p['long'], p['total'])))

    # ---- 首词分析 ----
    lines.append('')
    lines.append('【首词多样性分析】')
    u = int(o['unique_ratio'] * 100)
    lines.append('  首词独特率: {}%（{} 种不同首词 / {} 个句子）'.format(
        u, len(o['openings']), s['total']))
    lines.append('')
    lines.append('  最常见首词（前两字）:')
    for w, c in o['top_openings']:
        lines.append('    「{}」: {} 次（{}%）'.format(w, c, pct(c, s['total'])))
    if o['warnings']:
        lines.append('')
        lines.append('  ⚠ 警告:')
        for w in o['warnings']:
            lines.append('    · {}'.format(w))

    # ---- 建议 ----
    lines.append('')
    lines.append('【写作建议】')
    lines.append('  · 有意识地交替使用长短句，制造节奏起伏')
    lines.append('  · 短句适合动作、转折、情绪爆发；长句适合描写、铺陈、内心独白')
    lines.append('  · 适当使用单句段落来强调关键信息或制造停顿感')
    lines.append('  · 避免连续多个句子以相同的字词开头')
    lines.append('  · 尝试用倒装句、省略句、对话等手法来打破单一句式')
    lines.append('')

    return '\n'.join(lines)


def format_json(a):
    """将分析结果格式化为 JSON 字符串。"""
    # 将 tuple 列表转为更友好的格式
    output = {
        'rhythm_score': round(a['rhythm_score'], 1),
        'verdict': a['verdict'],
        'sentences': {
            'total': a['sentences']['total'],
            'avg_length': round(a['sentences']['avg_length'], 1),
            'std_dev': round(a['sentences']['std_dev'], 1),
            'variety_score': round(a['sentences']['variety_score'], 1),
            'distribution': {
                'short_lt15': a['sentences']['short'],
                'medium_15_30': a['sentences']['medium'],
                'long_31_50': a['sentences']['long'],
                'very_long_gt50': a['sentences']['very_long'],
            },
            'lengths': a['sentences']['lengths'],
        },
        'paragraphs': {
            'total': a['paragraphs']['total'],
            'avg_length': round(a['paragraphs']['avg_length'], 1),
            'variety_score': round(a['paragraphs']['variety_score'], 1),
            'distribution': {
                'short_1_2': a['paragraphs']['short'],
                'medium_3_5': a['paragraphs']['medium'],
                'long_6_plus': a['paragraphs']['long'],
            },
            'lengths': a['paragraphs']['lengths'],
        },
        'openings': {
            'unique_ratio': round(a['openings']['unique_ratio'], 3),
            'top_openings': [
                {'chars': w, 'count': c} for w, c in a['openings']['top_openings']
            ],
            'warnings': a['openings']['warnings'],
        },
    }
    return json.dumps(output, ensure_ascii=False, indent=2)


def main():
    args = sys.argv[1:]

    # --help
    if '--help' in args or '-h' in args:
        print(__doc__.strip())
        sys.exit(0)

    use_json = '--json' in args
    if use_json:
        args = [a for a in args if a != '--json']

    # --text "..."
    if '--text' in args:
        idx = args.index('--text')
        if idx + 1 >= len(args):
            print('错误: --text 后面需要提供文本内容', file=sys.stderr)
            sys.exit(1)
        text = ' '.join(args[idx + 1:])
    elif args:
        filepath = os.path.normpath(args[0])
        try:
            with open(filepath, 'r', encoding='utf-8') as fh:
                text = fh.read()
        except Exception as e:
            print('读取文件失败: {}'.format(filepath), file=sys.stderr)
            print(str(e), file=sys.stderr)
            sys.exit(1)
    else:
        print('用法:')
        print('  python rhythm.py <文件路径>')
        print('  python rhythm.py --text "他站在窗前。外面的雨已经下了三天三夜。"')
        print('  python rhythm.py --json <文件路径>')
        print('  python rhythm.py --help')
        sys.exit(0)

    result = analyze_text(text)

    if use_json:
        print(format_json(result))
    else:
        print(format_report(result))


if __name__ == '__main__':
    main()
