#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
prose_check.py - 中文散文/网文文风分析工具

检测项目:
- AI味检测（公式化句式、空洞修饰、滥用语气词）
- 虚词密度（的地得了着过等功能词占比）
- 四字格滥用检测（连续成语/四字短语堆砌）
- 感官过滤词（看到、听到、感觉到等拉远读者距离的词）
- 冗余修饰（多重形容词堆叠、"地"字短语堆砌）

用法:
  python prose_check.py <file>
  python prose_check.py --text "要分析的文本..."
  python prose_check.py --text "要分析的文本..." --json
  python prose_check.py --help
"""

import sys
import re
import json
import os

if sys.stdout and hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
if sys.stderr and hasattr(sys.stderr, 'reconfigure'):
    sys.stderr.reconfigure(encoding='utf-8')

# ============================================================
# 1. AI味检测 — 公式化句式 / 空洞修饰 / 语气词滥用
# ============================================================

# 语气助词（句末高频虚化词）
AI_PARTICLE_CHARS = list('的了吗呢地得')

# 公式化句式 —— 典型 AI / 机翻腔
FORMULAIC_PATTERNS = [
    (re.compile(r'这是一个.{1,10}的.{1,6}'), '「这是一个…的…」句式'),
    (re.compile(r'值得注意的是'), '「值得注意的是」'),
    (re.compile(r'需要指出的是'), '「需要指出的是」'),
    (re.compile(r'众所周知'), '「众所周知」'),
    (re.compile(r'不可否认'), '「不可否认」'),
    (re.compile(r'毋庸置疑'), '「毋庸置疑」'),
    (re.compile(r'在这个.{1,8}的时代'), '「在这个…的时代」'),
    (re.compile(r'作为一[个名位].{1,10}[，,]'), '「作为一个…，」句式'),
    (re.compile(r'总而言之'), '「总而言之」'),
    (re.compile(r'综上所述'), '「综上所述」'),
    (re.compile(r'换言之'), '「换言之」'),
    (re.compile(r'由此可见'), '「由此可见」'),
    (re.compile(r'不得不说'), '「不得不说」'),
    (re.compile(r'一言以蔽之'), '「一言以蔽之」'),
]

# 空洞程度副词 + 形容词 模式
HOLLOW_MODIFIER_ADVERBS = ['非常', '十分', '极其', '格外', '相当', '特别',
                           '无比', '异常', '万分', '尤为', '颇为', '甚为']
HOLLOW_MODIFIER_PATTERN = re.compile(
    r'(?:' + '|'.join(re.escape(a) for a in HOLLOW_MODIFIER_ADVERBS) + r')[\u4e00-\u9fff]{1,4}'
)

# 排比句检测：三个或以上结构相似的分句（以顿号/逗号/分号分隔，且长度相近）
def detect_parallelism_overuse(text):
    """检测过度排比：在一个句子内出现 3+ 长度相近、结构重复的分句。"""
    sentences = split_into_sentences(text)
    hits = []
    for sent in sentences:
        # 用顿号、逗号、分号拆分
        clauses = re.split(r'[、，,；;]', sent)
        clauses = [c.strip() for c in clauses if len(c.strip()) >= 2]
        if len(clauses) < 3:
            continue
        # 滑动窗口，检测连续 3 个长度相近的分句
        for i in range(len(clauses) - 2):
            triple = clauses[i:i + 3]
            lengths = [len(c) for c in triple]
            avg_len = sum(lengths) / 3
            if avg_len < 3:
                continue
            # 长度偏差在 30% 以内视为结构相近
            if all(abs(l - avg_len) / avg_len <= 0.3 for l in lengths):
                preview = '、'.join(triple)
                if len(preview) > 60:
                    preview = preview[:60] + '…'
                hits.append(preview)
                break  # 每个句子只报告一次
    return hits


def detect_ai_flavor(text):
    """AI味综合检测，返回 (总命中数, 分类详情字典, 示例列表)。"""
    details = {
        '语气词过度使用': 0,
        '公式化句式': [],
        '空洞修饰': [],
        '排比堆砌': [],
    }
    examples = []

    # --- 语气词密度（在句子粒度检测） ---
    chars_only = re.sub(r'\s+', '', text)
    total_chars = len(chars_only)
    particle_count = sum(chars_only.count(p) for p in AI_PARTICLE_CHARS)
    if total_chars > 0:
        details['语气词过度使用'] = particle_count

    # --- 公式化句式 ---
    for pattern, label in FORMULAIC_PATTERNS:
        found = pattern.findall(text)
        for f in found:
            match_text = f if isinstance(f, str) else f[0]
            preview = match_text.strip()[:40]
            details['公式化句式'].append(label)
            if len(examples) < 5:
                examples.append(f'[公式化] {preview}')

    # --- 空洞修饰 ---
    hollow_matches = HOLLOW_MODIFIER_PATTERN.findall(text)
    for m in hollow_matches:
        details['空洞修饰'].append(m)
        if len(examples) < 8:
            examples.append(f'[空洞修饰] {m}')

    # --- 排比堆砌 ---
    parallel_hits = detect_parallelism_overuse(text)
    details['排比堆砌'] = parallel_hits
    for p in parallel_hits[:3]:
        if len(examples) < 10:
            examples.append(f'[排比] {p}')

    total_hits = (
        len(details['公式化句式'])
        + len(details['空洞修饰'])
        + len(details['排比堆砌'])
    )
    # 语气词单独算比率，不计入 total_hits（在报告中独立展示）
    return total_hits, details, examples


# ============================================================
# 2. 虚词密度
# ============================================================

FUNCTION_WORDS = list('的地得了着过是在把被将由')


def calc_function_word_density(text):
    """计算虚词密度，返回 (虚词数, 总字符数, 百分比, 各虚词计数)。"""
    chars_only = re.sub(r'[^\u4e00-\u9fff]', '', text)
    total = len(chars_only)
    counts = {}
    fw_total = 0
    for w in FUNCTION_WORDS:
        c = chars_only.count(w)
        if c > 0:
            counts[w] = c
            fw_total += c
    pct = (fw_total / total * 100) if total > 0 else 0.0
    return fw_total, total, pct, counts


# ============================================================
# 3. 四字格滥用检测
# ============================================================

# 匹配连续四个汉字（简单近似四字格）
FOUR_CHAR_PATTERN = re.compile(r'[\u4e00-\u9fff]{4}')


def detect_four_char_abuse(text):
    """
    检测四字格滥用：在 50 字窗口内出现 3 个及以上四字短语。
    返回 (命中区域数, 示例列表)。
    """
    matches = list(FOUR_CHAR_PATTERN.finditer(text))
    if len(matches) < 3:
        return 0, []

    hits = []
    reported_ranges = set()

    for i in range(len(matches) - 2):
        # 检查连续三个四字格是否在 50 字符窗口内
        start_pos = matches[i].start()
        end_pos = matches[i + 2].end()
        span = end_pos - start_pos
        if span <= 50:
            # 避免重复报告重叠区域
            range_key = (start_pos // 30)
            if range_key in reported_ranges:
                continue
            reported_ranges.add(range_key)
            # 提取上下文
            ctx_start = max(0, start_pos - 5)
            ctx_end = min(len(text), end_pos + 5)
            snippet = text[ctx_start:ctx_end].replace('\n', ' ').strip()
            if len(snippet) > 50:
                snippet = snippet[:50] + '…'
            hits.append(snippet)

    return len(hits), hits[:5]


# ============================================================
# 4. 感官过滤词
# ============================================================

SENSORY_FILTER_WORDS = [
    '看到', '听到', '感觉到', '感到', '意识到', '注意到',
    '发现', '觉得', '认为', '想到', '望见', '瞧见',
    '听见', '嗅到', '闻到', '察觉到', '体会到', '领悟到',
]


def find_sensory_filters(text):
    """检测感官过滤词，返回 (总数, 各词计数, 示例上下文)。"""
    total = 0
    word_counts = {}
    examples = []
    for fw in SENSORY_FILTER_WORDS:
        positions = [m.start() for m in re.finditer(re.escape(fw), text)]
        if positions:
            word_counts[fw] = len(positions)
            total += len(positions)
            # 取第一次出现作为示例
            if len(examples) < 5:
                pos = positions[0]
                ctx_start = max(0, pos - 8)
                ctx_end = min(len(text), pos + len(fw) + 8)
                snippet = text[ctx_start:ctx_end].replace('\n', ' ').strip()
                examples.append(f'…{snippet}…')
    return total, word_counts, examples


# ============================================================
# 5. 冗余修饰检测
# ============================================================

# 模式 A：多个"…的"修饰同一名词 => "美丽的、善良的、温柔的女孩"
REDUNDANT_DE_PATTERN = re.compile(
    r'([\u4e00-\u9fff]{1,4}的[、，,]\s*){2,}[\u4e00-\u9fff]{1,4}的[\u4e00-\u9fff]{1,4}'
)

# 模式 B：多个"…地"修饰同一动词 => "快速地、轻柔地、小心翼翼地走过去"
REDUNDANT_DI_PATTERN = re.compile(
    r'([\u4e00-\u9fff]{1,6}地[、，,]\s*){2,}[\u4e00-\u9fff]{1,6}地[\u4e00-\u9fff]{1,6}'
)

# 模式 C：连续两个以上"很/太/好+形容词"
REDUNDANT_DEGREE_PATTERN = re.compile(
    r'(?:(?:很|太|好|真|最)[\u4e00-\u9fff]{1,3}[、，,]\s*){2,}(?:很|太|好|真|最)[\u4e00-\u9fff]{1,3}'
)


def detect_redundant_modifiers(text):
    """检测冗余修饰，返回 (命中数, 示例列表)。"""
    hits = []

    for pattern, label in [
        (REDUNDANT_DE_PATTERN, '多重"的"字修饰'),
        (REDUNDANT_DI_PATTERN, '多重"地"字修饰'),
        (REDUNDANT_DEGREE_PATTERN, '程度词堆叠'),
    ]:
        for m in pattern.finditer(text):
            snippet = m.group()
            if len(snippet) > 40:
                snippet = snippet[:40] + '…'
            hits.append(f'[{label}] {snippet}')

    return len(hits), hits[:5]


# ============================================================
# 辅助工具
# ============================================================

def split_into_sentences(text):
    """按中文句号、问号、感叹号、省略号拆句。"""
    parts = re.split(r'[。！？!?\u2026]+', text)
    return [s.strip() for s in parts if s.strip()]


def count_chinese_chars(text):
    """统计汉字数量（不含标点和空格）。"""
    return len(re.findall(r'[\u4e00-\u9fff]', text))


# ============================================================
# 综合分析
# ============================================================

def analyze_text(text):
    sentences = split_into_sentences(text)
    total_chars = count_chinese_chars(text)

    # 1) AI味检测
    ai_hits, ai_details, ai_examples = detect_ai_flavor(text)
    particle_count = ai_details['语气词过度使用']
    particle_pct = (particle_count / total_chars * 100) if total_chars > 0 else 0.0

    # 2) 虚词密度
    fw_count, fw_total_chars, fw_pct, fw_breakdown = calc_function_word_density(text)

    # 3) 四字格滥用
    four_char_hits, four_char_examples = detect_four_char_abuse(text)

    # 4) 感官过滤词
    filter_count, filter_breakdown, filter_examples = find_sensory_filters(text)

    # 5) 冗余修饰
    redundant_count, redundant_examples = detect_redundant_modifiers(text)

    return {
        'total_sentences': len(sentences),
        'total_chars': total_chars,
        # AI味
        'ai_hits': ai_hits,
        'ai_details': ai_details,
        'ai_examples': ai_examples,
        'particle_count': particle_count,
        'particle_pct': particle_pct,
        # 虚词
        'fw_count': fw_count,
        'fw_pct': fw_pct,
        'fw_breakdown': fw_breakdown,
        # 四字格
        'four_char_hits': four_char_hits,
        'four_char_examples': four_char_examples,
        # 感官过滤词
        'filter_count': filter_count,
        'filter_breakdown': filter_breakdown,
        'filter_examples': filter_examples,
        # 冗余修饰
        'redundant_count': redundant_count,
        'redundant_examples': redundant_examples,
    }


# ============================================================
# 评语
# ============================================================

def get_verdict(result):
    issues = []

    if result['particle_pct'] > 12:
        issues.append('语气词密度偏高（>{:.1f}%，建议 <12%）'.format(result['particle_pct']))
    if result['ai_hits'] > 3:
        issues.append('公式化/空洞表达较多（{}处）'.format(result['ai_hits']))
    if result['fw_pct'] > 18:
        issues.append('虚词密度偏高（{:.1f}%，建议 <18%）'.format(result['fw_pct']))
    if result['four_char_hits'] > 2:
        issues.append('四字格堆砌（{}处密集区）'.format(result['four_char_hits']))
    if result['filter_count'] > max(3, result['total_sentences'] * 0.1):
        issues.append('感官过滤词过多（{}处）'.format(result['filter_count']))
    if result['redundant_count'] > 2:
        issues.append('冗余修饰（{}处）'.format(result['redundant_count']))

    if not issues:
        return '散文模式健康', issues
    elif len(issues) <= 2:
        return '轻微问题', issues
    else:
        return '多项问题', issues


# ============================================================
# 报告格式化
# ============================================================

def format_report(result):
    verdict_label, issue_list = get_verdict(result)

    r = ''
    r += '\n文风分析报告'
    r += '\n============\n'
    r += '\n【概览】'
    r += '\n  句子数: {}'.format(result['total_sentences'])
    r += '\n  汉字数: {}'.format(result['total_chars'])

    # ---- AI味 ----
    r += '\n\n【AI味检测】'
    r += '\n  语气词(的了吗呢地得)数量: {}'.format(result['particle_count'])
    r += '\n  语气词占比: {:.1f}%'.format(result['particle_pct'])
    r += '\n  建议: <12%'
    r += '\n  公式化句式命中: {}处'.format(len(result['ai_details']['公式化句式']))
    r += '\n  空洞修饰命中: {}处'.format(len(result['ai_details']['空洞修饰']))
    r += '\n  排比堆砌命中: {}处'.format(len(result['ai_details']['排比堆砌']))
    if result['ai_examples']:
        r += '\n  示例:'
        for e in result['ai_examples'][:5]:
            r += '\n    - {}'.format(e)

    # ---- 虚词密度 ----
    r += '\n\n【虚词密度】(的地得了着过是在把被将由)'
    r += '\n  虚词总数: {}'.format(result['fw_count'])
    r += '\n  虚词密度: {:.1f}%'.format(result['fw_pct'])
    r += '\n  建议: <18%'
    if result['fw_breakdown']:
        top_fw = sorted(result['fw_breakdown'].items(), key=lambda x: -x[1])[:6]
        breakdown_str = '、'.join(f'「{w}」{c}次' for w, c in top_fw)
        r += '\n  分布: {}'.format(breakdown_str)

    # ---- 四字格 ----
    r += '\n\n【四字格滥用检测】'
    r += '\n  密集区域: {}处'.format(result['four_char_hits'])
    r += '\n  判定标准: 50字内出现3个及以上四字短语'
    if result['four_char_examples']:
        r += '\n  示例:'
        for e in result['four_char_examples']:
            r += '\n    - "{}..."'.format(e)

    # ---- 感官过滤词 ----
    r += '\n\n【感官过滤词】(看到/听到/感觉到/觉得/意识到 等)'
    r += '\n  总数: {}'.format(result['filter_count'])
    if result['filter_breakdown']:
        top_filters = sorted(result['filter_breakdown'].items(), key=lambda x: -x[1])[:6]
        r += '\n  分布: {}'.format('、'.join(f'「{w}」{c}次' for w, c in top_filters))
    if result['filter_examples']:
        r += '\n  示例:'
        for e in result['filter_examples']:
            r += '\n    - {}'.format(e)

    # ---- 冗余修饰 ----
    r += '\n\n【冗余修饰】'
    r += '\n  命中: {}处'.format(result['redundant_count'])
    if result['redundant_examples']:
        r += '\n  示例:'
        for e in result['redundant_examples']:
            r += '\n    - {}'.format(e)

    # ---- 评语 ----
    r += '\n\n【评语】'
    r += '\n  {}'.format(verdict_label)
    if issue_list:
        for iss in issue_list:
            r += '\n  - {}'.format(iss)

    # ---- 建议 ----
    r += '\n\n【优化建议】'
    r += '\n  - AI味: 减少公式化开头（"这是一个…"），用具体细节替代空洞修饰（"非常美丽"→写出美在哪里）'
    r += '\n  - 虚词: 削减不必要的"的""了"，尝试把"…地+动词"改为更精准的单个动词'
    r += '\n  - 四字格: 避免连续堆砌成语，穿插白话短句增加节奏变化'
    r += '\n  - 过滤词: 删掉"他看到…""她感觉到…"，直接描写场景让读者自行感受'
    r += '\n  - 冗余修饰: 从三个形容词中选最精准的一个，删掉其余'
    r += '\n'
    return r


def format_json(result):
    verdict_label, issue_list = get_verdict(result)
    output = {
        '概览': {
            '句子数': result['total_sentences'],
            '汉字数': result['total_chars'],
        },
        'AI味检测': {
            '语气词数量': result['particle_count'],
            '语气词占比': round(result['particle_pct'], 1),
            '公式化句式': len(result['ai_details']['公式化句式']),
            '空洞修饰': len(result['ai_details']['空洞修饰']),
            '排比堆砌': len(result['ai_details']['排比堆砌']),
            '示例': result['ai_examples'][:5],
        },
        '虚词密度': {
            '虚词总数': result['fw_count'],
            '密度百分比': round(result['fw_pct'], 1),
            '分布': result['fw_breakdown'],
        },
        '四字格滥用': {
            '密集区域数': result['four_char_hits'],
            '示例': result['four_char_examples'],
        },
        '感官过滤词': {
            '总数': result['filter_count'],
            '分布': result['filter_breakdown'],
            '示例': result['filter_examples'],
        },
        '冗余修饰': {
            '命中数': result['redundant_count'],
            '示例': result['redundant_examples'],
        },
        '评语': verdict_label,
        '问题列表': issue_list,
    }
    return json.dumps(output, ensure_ascii=False, indent=2)


# ============================================================
# CLI 入口
# ============================================================

def print_help():
    print('用法:')
    print('  python prose_check.py <文件路径>')
    print('  python prose_check.py --text "要分析的文本..."')
    print('  python prose_check.py --text "要分析的文本..." --json')
    print('  python prose_check.py --help')
    print()
    print('中文文风分析工具，检测以下问题:')
    print('  - AI味检测（公式化句式、空洞修饰、语气词滥用）')
    print('  - 虚词密度（的地得了着过等功能词占比）')
    print('  - 四字格滥用（连续成语/四字短语堆砌）')
    print('  - 感官过滤词（看到、听到、感觉到等拉远距离的词）')
    print('  - 冗余修饰（多重形容词堆叠）')


def main():
    args = sys.argv[1:]
    use_json = '--json' in args
    if use_json:
        args = [a for a in args if a != '--json']

    if '--help' in args or '-h' in args:
        print_help()
        sys.exit(0)

    text = None

    if '--text' in args:
        text_index = args.index('--text')
        remaining = args[text_index + 1:]
        if not remaining:
            print('错误: --text 后面需要提供文本内容', file=sys.stderr)
            sys.exit(1)
        text = ' '.join(remaining)
    elif args:
        filename = args[0]
        if not os.path.isfile(filename):
            print('错误: 找不到文件 - ' + filename, file=sys.stderr)
            sys.exit(1)
        try:
            with open(filename, 'r', encoding='utf-8') as f:
                text = f.read()
        except Exception as e:
            print('错误: 读取文件失败 - ' + filename, file=sys.stderr)
            print(str(e), file=sys.stderr)
            sys.exit(1)
    else:
        print_help()
        sys.exit(0)

    if not text or not text.strip():
        print('错误: 输入文本为空', file=sys.stderr)
        sys.exit(1)

    result = analyze_text(text)

    if use_json:
        print(format_json(result))
    else:
        print(format_report(result))


if __name__ == '__main__':
    main()
