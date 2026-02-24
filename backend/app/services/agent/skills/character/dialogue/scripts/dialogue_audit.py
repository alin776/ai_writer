#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
dialogue_audit.py - 对话审计工具（中文网文专用）

分析对话的功能覆盖度（情节推进、角色揭示、潜台词、关系动态）
以及常见反模式（设定倾泻、情绪旁白过多、千人一面、直白情绪）。

Usage:
  python dialogue_audit.py <file>
  python dialogue_audit.py --text "对话内容"
"""

import sys
import re
import json
import os


# ---------------------------------------------------------------------------
# 功能检测模式 — 情节推进
# ---------------------------------------------------------------------------
PLOT_PATTERNS = [
    # 意图/计划类
    re.compile(r'(?:必须|需要|打算|计划|应该|准备|决定)'),
    # 事件/动作类
    re.compile(r'(?:发生了|被杀|逃走|到达|离开|死亡|失踪|消失|出事|暴露)'),
    # 发现/信息类
    re.compile(r'(?:发现|得知|查到|探明|知道了|听说|收到消息)'),
    # 移动/方向类
    re.compile(r'(?:前往|赶往|出发|回去|撤退|转移|进攻)'),
    # 疑问推动类
    re.compile(r'(?:什么时候|在哪里|为什么|怎么回事|怎么办|谁干的|到底)'),
]

# ---------------------------------------------------------------------------
# 功能检测模式 — 角色揭示
# ---------------------------------------------------------------------------
CHARACTER_PATTERNS = [
    # 自我剖白
    re.compile(r'(?:我一直|我从不|我相信|我觉得|我想要|我需要|我讨厌|我喜欢)'),
    # 身世/回忆
    re.compile(r'(?:我父亲|我母亲|我师父|我小时候|我记得|当年我|那时候我)'),
    # 自我定义
    re.compile(r'(?:我这个人|我不是那种|这不是我|我向来|我天生|我命中注定)'),
    # 情感态度
    re.compile(r'(?:怕的是|骄傲的是|惭愧|抱歉|感激|后悔|不甘心)'),
]

# ---------------------------------------------------------------------------
# 功能检测模式 — 潜台词
# ---------------------------------------------------------------------------
SUBTEXT_INDICATORS = [
    # 反问/试探
    re.compile(r'(?:你觉得呢|是吗|不是吗|你说呢|你认为呢|你猜)'),
    # 回避/模糊
    re.compile(r'(?:也许吧|看情况|再说吧|随便|无所谓|算了|不好说|谁知道呢)'),
    # 话题转换
    re.compile(r'(?:说起来|话说回来|不过|对了|话又说回来|算了不说这个)'),
    # 言不由衷标记
    re.compile(r'(?:没什么|我没事|我很好|别担心|不用管我|与你无关)'),
]

# ---------------------------------------------------------------------------
# 功能检测模式 — 关系动态
# ---------------------------------------------------------------------------
RELATIONSHIP_PATTERNS = [
    # 指责/对比
    re.compile(r'(?:你总是|你从来不|你以前|你变了|你还是老样子)'),
    # 关系词汇
    re.compile(r'(?:我们之间|你还记得|当初我们|我们的约定|你答应过)'),
    # 信任/情感
    re.compile(r'(?:信任|原谅|理解|了解我|相信我|靠得住|辜负|背叛)'),
    # 共同/分离
    re.compile(r'(?:我们|一起|分开|之间|同行|并肩|各走各的|形同陌路)'),
]

# ---------------------------------------------------------------------------
# 设定倾泻检测模式
# ---------------------------------------------------------------------------
EXPOSITION_PATTERNS = [
    # 信息回顾话术
    re.compile(r'(?:你也知道|众所周知|传说中|据说|想必你也听说)'),
    # 定义/解释话术
    re.compile(r'所谓的.{0,10}就是'),
    re.compile(r'(?:简单来说|也就是说|换句话说|说白了)'),
    # 设定词汇密集（据、乃是、即是、所谓、便是）
    re.compile(r'(?:乃是|即是|所谓|便是|此乃|正是那)'),
]

# ---------------------------------------------------------------------------
# 对话标签 — 中性标签
# ---------------------------------------------------------------------------
NEUTRAL_TAGS = ['说', '道', '问', '答', '叫', '喊']

# ---------------------------------------------------------------------------
# 对话标签 — 过度修饰（said-bookisms 中文等价）
# ---------------------------------------------------------------------------
SAID_BOOKISMS = [
    # 声音修饰
    '娇声道', '柔声道', '冷冷道', '森然道', '戏谑道', '玩味道',
    '淡淡道', '沉声道', '低声道', '高声道', '轻声道', '厉声道',
    '阴沉道', '傲然道', '冷笑道', '嗤笑道', '讥笑道', '狞笑道',
    '大笑道', '苦笑道', '微笑道', '咬牙道', '怒声道', '喝道',
    '嘶声道', '颤声道', '哽咽道', '嘻嘻道', '嘿嘿道', '哈哈道',
    # 语气修饰
    '不屑道', '得意道', '无奈道', '感慨道', '惊呼道', '惊叫道',
    '懒洋洋道', '一本正经道', '意味深长道', '若有所思道',
]

# ---------------------------------------------------------------------------
# 直白情绪表达（对话内）
# ---------------------------------------------------------------------------
ON_THE_NOSE_EMOTIONS = [
    '我很生气', '我很伤心', '我很高兴', '我很害怕',
    '我很难过', '我很紧张', '我很激动', '我很失望',
    '我很愤怒', '我很痛苦', '我很开心', '我很担心',
    '我觉得很',
]


# ---------------------------------------------------------------------------
# 辅助函数
# ---------------------------------------------------------------------------

def count_matches(text, patterns):
    """对 patterns 列表逐一匹配，返回去重匹配项（每个 pattern 最多取 3 个）。"""
    matches = []
    for pattern in patterns:
        found = pattern.findall(text)
        if found:
            matches.extend(found[:3])
    return list(dict.fromkeys(matches))


def detect_function(text, patterns):
    """检测单项功能的存在与置信度。"""
    signals = count_matches(text, patterns)
    count = len(signals)
    if count >= 3:
        confidence = '高'
    elif count >= 1:
        confidence = '中'
    else:
        confidence = '低'
    return {
        'detected': count > 0,
        'confidence': confidence,
        'signals': signals[:5],
    }


def extract_dialogue_content(text):
    """提取中文引号内的对话内容（支持 "" 和 「」）。"""
    parts = []
    # 中文双引号 \u201c ... \u201d
    parts.extend(re.findall(r'\u201c([^\u201d]*)\u201d', text))
    # 中文单引号用作外层（偶见）\u300c ... \u300d
    parts.extend(re.findall(r'\u300c([^\u300d]*)\u300d', text))
    # 英文双引号 fallback
    parts.extend(re.findall(r'"([^"]*)"', text))
    return ''.join(parts)


def calculate_dialogue_ratio(text):
    """计算对话内容占总文本的字符比例。"""
    if not text:
        return 0.0
    quote_patterns = [
        re.compile(r'\u201c[^\u201d]*\u201d'),  # ""
        re.compile(r'\u300c[^\u300d]*\u300d'),  # 「」
        re.compile(r'"[^"]*"'),                  # ""
    ]
    quoted_chars = 0
    for pat in quote_patterns:
        for m in pat.finditer(text):
            quoted_chars += len(m.group())
    return quoted_chars / len(text)


# ---------------------------------------------------------------------------
# 对话标签分析
# ---------------------------------------------------------------------------

def analyze_dialogue_tags(text):
    """分析中文对话标签的使用情况。"""
    # 中性标签计数：引号后紧跟的 说/道/问/答
    neutral_pattern = re.compile(
        r'[\u201d\u300d"]\s*(?:\S{0,4})(' + '|'.join(NEUTRAL_TAGS) + r')'
    )
    neutral_matches = neutral_pattern.findall(text)

    # 过度修饰标签
    bookism_pattern = re.compile('(' + '|'.join(re.escape(b) for b in SAID_BOOKISMS) + ')')
    bookism_matches = bookism_pattern.findall(text)

    # 动作节拍：引号后跟动作描写
    action_beat_pattern = re.compile(
        r'[\u201d\u300d"]'
        r'[^。！？\n]{0,6}'
        r'(走|站|坐|转|看|伸手|点头|摇头|微笑|皱眉|握拳|叹息|起身|挥手|低头|抬头|拍|推|拉|挡)'
    )
    action_beats = action_beat_pattern.findall(text)

    found_bookisms = list(dict.fromkeys(bookism_matches))

    neutral_count = len(neutral_matches)
    bookism_count = len(bookism_matches)

    return {
        'neutral_count': neutral_count,
        'bookism_count': bookism_count,
        'action_beat_count': len(action_beats),
        'said_bookisms': found_bookisms[:10],
        'tag_healthy': bookism_count <= neutral_count,
    }


# ---------------------------------------------------------------------------
# 反模式检测
# ---------------------------------------------------------------------------

def detect_anti_patterns(text):
    """检测中文网文常见对话反模式。"""
    dialogue_content = extract_dialogue_content(text)
    results = []

    # ------ 1. 设定倾泻 ------
    exposition_matches = count_matches(text, EXPOSITION_PATTERNS)
    # 额外检查：对话中超长句子 + 设定词汇密集
    long_exposition = False
    dialogue_segments = re.findall(r'[\u201c\u300c]([^\u201d\u300d]{100,})[\u201d\u300d]', text)
    setting_words = re.compile(r'(?:据|乃是|即是|所谓|便是|此乃|正是)')
    for seg in dialogue_segments:
        if len(setting_words.findall(seg)) >= 2:
            long_exposition = True
            if '长段设定对话' not in exposition_matches:
                exposition_matches.append('长段设定对话')
    severity = '高' if len(exposition_matches) >= 2 or long_exposition else '中'
    results.append({
        'name': '设定倾泻',
        'detected': len(exposition_matches) > 0,
        'severity': severity,
        'evidence': exposition_matches[:5],
    })

    # ------ 2. 情绪旁白过多 ------
    # 副词 + 说话动词
    emotional_narrator_pattern = re.compile(
        r'(?:愤怒地|悲伤地|开心地|紧张地|焦急地|恐惧地|绝望地|兴奋地|痛苦地|冷冷地|狠狠地|温柔地|平静地|无奈地)'
        r'(?:说|道|问|答|喊|叫|吼)'
    )
    emotional_matches = emotional_narrator_pattern.findall(text)
    em_severity = '高' if len(emotional_matches) >= 3 else '中'
    results.append({
        'name': '情绪旁白过多',
        'detected': len(emotional_matches) > 0,
        'severity': em_severity,
        'evidence': list(dict.fromkeys(emotional_matches))[:5],
    })

    # ------ 3. 千人一面 ------
    # 结构性检测：各说话人的句子长度和模式是否过于接近
    dialogue_lines = re.findall(r'[\u201c\u300c]([^\u201d\u300d]+)[\u201d\u300d]', text)
    identical_twins_detected = False
    identical_evidence = []
    if len(dialogue_lines) >= 4:
        lengths = [len(line) for line in dialogue_lines]
        avg_len = sum(lengths) / len(lengths) if lengths else 0
        if avg_len > 0:
            variance = sum((l - avg_len) ** 2 for l in lengths) / len(lengths)
            std_dev = variance ** 0.5
            # 如果标准差相对于平均长度过小，说明句子长度高度一致
            cv = std_dev / avg_len if avg_len > 0 else 0
            if cv < 0.15:
                identical_twins_detected = True
                identical_evidence.append(
                    f'句长变异系数仅{cv:.2f}，各角色说话节奏雷同'
                )
        # 检查标点模式是否单一
        punct_patterns = set()
        for line in dialogue_lines:
            puncts = re.findall(r'[，。！？、；：]', line)
            pattern_key = ''.join(p for p in puncts[-3:]) if len(puncts) >= 3 else ''.join(puncts)
            punct_patterns.add(pattern_key)
        if len(punct_patterns) <= 2 and len(dialogue_lines) >= 4:
            identical_twins_detected = True
            identical_evidence.append(
                f'仅{len(punct_patterns)}种标点模式，语气缺乏分化'
            )
    results.append({
        'name': '千人一面',
        'detected': identical_twins_detected,
        'severity': '高' if len(identical_evidence) >= 2 else '中',
        'evidence': identical_evidence,
    })

    # ------ 4. 直白情绪 ------
    on_the_nose_matches = []
    for emotion in ON_THE_NOSE_EMOTIONS:
        if emotion in dialogue_content:
            on_the_nose_matches.append(emotion)
    on_the_nose_matches = list(dict.fromkeys(on_the_nose_matches))
    results.append({
        'name': '直白情绪',
        'detected': len(on_the_nose_matches) > 0,
        'severity': '高' if len(on_the_nose_matches) >= 2 else '中',
        'evidence': on_the_nose_matches[:5],
    })

    return results


# ---------------------------------------------------------------------------
# 核心审计函数
# ---------------------------------------------------------------------------

def audit_dialogue(text):
    """对输入文本执行完整对话审计。"""
    char_count = len(text.replace(' ', '').replace('\n', ''))
    dialogue_content = extract_dialogue_content(text)

    functions = {
        'plot_advancement': detect_function(dialogue_content, PLOT_PATTERNS),
        'character_reveal': detect_function(dialogue_content, CHARACTER_PATTERNS),
        'subtext_present': detect_function(dialogue_content, SUBTEXT_INDICATORS),
        'relationship_dynamics': detect_function(dialogue_content, RELATIONSHIP_PATTERNS),
    }

    detected_count = sum(1 for f in functions.values() if f['detected'])
    high_confidence = sum(1 for f in functions.values() if f['confidence'] == '高')
    function_score = min(100, (detected_count * 20) + (high_confidence * 10))

    tag_analysis = analyze_dialogue_tags(text)
    anti_patterns = detect_anti_patterns(text)

    issues = []
    recommendations = []

    if detected_count < 2:
        issues.append('对话可能只承担单一功能（未通过双重职责检验）')
        recommendations.append('为对话增加第二层目的：角色揭示、关系推动或潜台词暗线')

    if not functions['subtext_present']['detected']:
        issues.append('未检测到潜台词信号——对话可能过于直白')
        recommendations.append('赋予角色隐藏诉求，让他们无法直接说出真正想要的东西')

    if not tag_analysis['tag_healthy']:
        issues.append('过度修饰的对话标签比例偏高')
        recommendations.append('减少"XX道"式修饰，改用动作节拍或让对话本身传达情绪')

    for pattern in anti_patterns:
        if pattern['detected'] and pattern['severity'] != '低':
            issues.append(f"检测到反模式：{pattern['name']}")

    if any(p['name'] == '设定倾泻' and p['detected'] for p in anti_patterns):
        recommendations.append('将设定信息融入冲突场景，让角色在行动中展现世界观，而非口头解说')

    if any(p['name'] == '情绪旁白过多' and p['detected'] for p in anti_patterns):
        recommendations.append('删除说话动词前的副词修饰，用动作细节和对话内容本身传达情绪')

    if any(p['name'] == '千人一面' and p['detected'] for p in anti_patterns):
        recommendations.append('为不同角色设计差异化的语言习惯：句长、口头禅、措辞风格需有明显区分')

    if any(p['name'] == '直白情绪' and p['detected'] for p in anti_patterns):
        recommendations.append('将"我很XX"式直述改为行为展示或潜台词暗示，让读者自行感受情绪')

    return {
        'line_count': len([l for l in text.split('\n') if l.strip()]),
        'char_count': char_count,
        'dialogue_ratio': calculate_dialogue_ratio(text),
        'functions': functions,
        'function_score': function_score,
        'tag_analysis': tag_analysis,
        'anti_patterns': anti_patterns,
        'issues': issues,
        'recommendations': recommendations,
    }


# ---------------------------------------------------------------------------
# 报告格式化
# ---------------------------------------------------------------------------

def format_report(audit):
    """将审计结果格式化为中文可读报告。"""
    lines = []
    lines.append('# 对话审计报告\n')

    ratio_pct = audit['dialogue_ratio'] * 100
    lines.append(f"字数：{audit['char_count']} | 对话占比：{ratio_pct:.1f}%")
    lines.append(f"双重职责得分：{audit['function_score']}/100\n")

    # --- 功能检测 ---
    lines.append('## 功能检测（双重职责检验）\n')
    function_names = {
        'plot_advancement': '情节推进',
        'character_reveal': '角色揭示',
        'subtext_present': '潜台词',
        'relationship_dynamics': '关系动态',
    }
    for key, label in function_names.items():
        func = audit['functions'][key]
        status = '[+]' if func['detected'] else '[-]'
        conf = f"（{func['confidence']}）" if func['detected'] else ''
        signals = f"：{'、'.join(func['signals'][:3])}" if func['signals'] else ''
        lines.append(f'  {status} {label}{conf}{signals}')
    lines.append('')

    # --- 标签分析 ---
    lines.append('## 对话标签分析\n')
    ta = audit['tag_analysis']
    lines.append(f"  中性标签（说/道/问/答）：{ta['neutral_count']} 次")
    lines.append(f"  过度修饰标签：{ta['bookism_count']} 次")
    lines.append(f"  动作节拍：{ta['action_beat_count']} 次")
    if ta['said_bookisms']:
        lines.append(f"  具体修饰标签：{'、'.join(ta['said_bookisms'][:6])}")
    health_label = '健康' if ta['tag_healthy'] else '需改善'
    lines.append(f'  标签健康度：{health_label}')
    lines.append('')

    # --- 反模式 ---
    detected_patterns = [p for p in audit['anti_patterns'] if p['detected']]
    if detected_patterns:
        lines.append('## 检测到的反模式\n')
        for pattern in detected_patterns:
            lines.append(f"  - {pattern['name']}（严重度：{pattern['severity']}）")
            if pattern['evidence']:
                evidence_str = '、'.join(str(e) for e in pattern['evidence'][:3])
                lines.append(f'    证据：{evidence_str}')
        lines.append('')

    # --- 问题 ---
    if audit['issues']:
        lines.append('## 存在的问题\n')
        for issue in audit['issues']:
            lines.append(f'  - {issue}')
        lines.append('')

    # --- 建议 ---
    if audit['recommendations']:
        lines.append('## 修改建议\n')
        for rec in audit['recommendations']:
            lines.append(f'  - {rec}')
        lines.append('')

    # --- 通过时的评估 ---
    if not audit['issues']:
        lines.append('## 综合评估\n')
        lines.append('  对话通过基础检查。建议人工复核以下方面：')
        lines.append('  - 各角色是否有独特的说话风格（建议运行 voice-check）')
        lines.append('  - 潜台词是否真实存在（而非仅有指标命中）')
        lines.append('  - 对话结束后场景关系是否发生了变化')
        lines.append('')

    return '\n'.join(lines)


# ---------------------------------------------------------------------------
# CLI 入口
# ---------------------------------------------------------------------------

def main():
    args = sys.argv[1:]

    if '--help' in args or '-h' in args:
        print('对话审计工具 — 中文网文对话双重职责与反模式检测\n')
        print('用法：')
        print('  python dialogue_audit.py <文件路径>')
        print('  python dialogue_audit.py --text "对话内容"\n')
        print('选项：')
        print('  --text "..."  直接提供文本')
        print('  --json        以 JSON 格式输出')
        print('  --help        显示此帮助信息\n')
        print('检测项目：')
        print('  - 功能覆盖度（情节推进、角色揭示、潜台词、关系动态）')
        print('  - 对话标签使用（中性标签 vs 过度修饰）')
        print('  - 常见反模式（设定倾泻、情绪旁白过多、千人一面、直白情绪）')
        sys.exit(0)

    json_output = '--json' in args
    text = ''

    if '--text' in args:
        text_index = args.index('--text')
        text = args[text_index + 1] if text_index + 1 < len(args) else ''
    else:
        file_path = next((a for a in args if not a.startswith('--')), None)
        if file_path:
            file_path = os.path.normpath(file_path)
            try:
                text = open(file_path, 'r', encoding='utf-8').read()
            except Exception as e:
                print(f'读取文件失败：{e}', file=sys.stderr)
                sys.exit(1)

    if not text.strip():
        print('错误：未提供文本。请使用 --text 或提供文件路径。', file=sys.stderr)
        sys.exit(1)

    audit = audit_dialogue(text)

    if json_output:
        print(json.dumps(audit, indent=2, ensure_ascii=False))
    else:
        print(format_report(audit))


if __name__ == '__main__':
    main()
