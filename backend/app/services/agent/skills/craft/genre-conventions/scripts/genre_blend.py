#!/usr/bin/env python3
"""genre_blend.py - 网文类型融合策略工具

分析两个网文类型的兼容性，提供融合比例和策略建议。

Usage:
  python genre_blend.py <主类型> <副类型>
  python genre_blend.py --matrix
  python genre_blend.py --json xuanhuan romance
"""

import sys
import json

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

GENRES = [
    {'name': 'xuanhuan', 'display': '玄幻', 'promise': '修炼突破的爽感', 'pacing': 'fast', 'tone': 'hot', 'focus': 'external'},
    {'name': 'urban', 'display': '都市', 'promise': '现代都市的逆袭传奇', 'pacing': 'fast', 'tone': 'neutral', 'focus': 'external'},
    {'name': 'xianxia', 'display': '仙侠', 'promise': '求仙问道的旅程', 'pacing': 'moderate', 'tone': 'neutral', 'focus': 'both'},
    {'name': 'scifi', 'display': '科幻', 'promise': '未来科技的无限想象', 'pacing': 'moderate', 'tone': 'neutral', 'focus': 'external'},
    {'name': 'apocalypse', 'display': '末世', 'promise': '绝境求生的紧迫', 'pacing': 'fast', 'tone': 'dark', 'focus': 'external'},
    {'name': 'game', 'display': '游戏', 'promise': '游戏化成长的代入', 'pacing': 'fast', 'tone': 'hot', 'focus': 'external'},
    {'name': 'historical', 'display': '历史', 'promise': '权谋风云的沉浸', 'pacing': 'moderate', 'tone': 'neutral', 'focus': 'both'},
    {'name': 'romance', 'display': '言情', 'promise': '情感关系的满足', 'pacing': 'slow', 'tone': 'warm', 'focus': 'internal'},
    {'name': 'suspense', 'display': '悬疑', 'promise': '真相揭露的快感', 'pacing': 'moderate', 'tone': 'dark', 'focus': 'external'},
    {'name': 'fantasy', 'display': '奇幻', 'promise': '异世界冒险的惊奇', 'pacing': 'moderate', 'tone': 'neutral', 'focus': 'external'},
    {'name': 'wuxia', 'display': '武侠', 'promise': '江湖恩怨的快意', 'pacing': 'moderate', 'tone': 'neutral', 'focus': 'both'},
]

GENRE_MAP = {g['name']: g for g in GENRES}


def assess_compatibility(p, s):
    score = 0
    # 节奏兼容
    if p['pacing'] == s['pacing']:
        score += 2
    elif 'moderate' in (p['pacing'], s['pacing']):
        score += 1
    # 基调兼容
    if p['tone'] == s['tone']:
        score += 2
    elif 'neutral' in (p['tone'], s['tone']):
        score += 1
    elif (p['tone'] == 'hot' and s['tone'] == 'warm') or (p['tone'] == 'warm' and s['tone'] == 'hot'):
        score += 1
    elif p['tone'] != s['tone']:
        score -= 1
    # 焦点兼容
    if p['focus'] == s['focus']:
        score += 1
    elif 'both' in (p['focus'], s['focus']):
        score += 1
    if score >= 4:
        return 'excellent'
    if score >= 2:
        return 'good'
    if score >= 0:
        return 'challenging'
    return 'difficult'


def get_blend_strategy(primary_name, secondary_name):
    p = GENRE_MAP.get(primary_name)
    s = GENRE_MAP.get(secondary_name)
    if not p or not s:
        raise ValueError('未知类型: ' + (primary_name if not p else secondary_name))
    compat = assess_compatibility(p, s)
    strategies, pitfalls = [], []

    if p['pacing'] == 'fast' and s['pacing'] == 'slow':
        strategies.append('在铺垫期和战后恢复期融入{}元素'.format(s['display']))
        pitfalls.append('{}元素可能拖慢{}的节奏推进'.format(s['display'], p['display']))
    elif p['pacing'] == 'slow' and s['pacing'] == 'fast':
        strategies.append('用{}高潮段落打断{}的舒缓节奏'.format(s['display'], p['display']))

    if p['tone'] == 'dark' and s['tone'] in ('hot', 'warm'):
        strategies.append('刻意使用反差——轻松时刻让黑暗时刻更有冲击力')
        pitfalls.append('基调切换过猛可能导致读者出戏')

    if p['tone'] == 'hot' and s['tone'] == 'dark':
        strategies.append('在爽文节奏中穿插危机感，增加紧迫性')
        pitfalls.append('过度黑暗可能破坏爽点体验')

    strategies.append('{}元素应服务于{}的核心爽点'.format(s['display'], p['display']))
    pitfalls.append('副类型{}比重过大可能喧宾夺主'.format(s['display']))

    prop_map = {
        'excellent': '60% {} / 40% {} — 全程深度融合',
        'good': '70% {} / 30% {} — 副类型在特定场景集中出现',
        'challenging': '80% {} / 20% {} — 副类型作为调味点缀',
        'difficult': '85% {} / 15% {} — 需要精心设计过渡',
    }
    prop = prop_map[compat].format(p['display'], s['display'])

    return {
        'primary': p['display'],
        'secondary': s['display'],
        'compatibility': compat,
        'strategies': strategies,
        'pitfalls': pitfalls,
        'proportion': prop,
    }


def format_blend_report(strategy):
    icons = {'excellent': '★★★★', 'good': '★★★', 'challenging': '★★', 'difficult': '★'}
    compat_cn = {'excellent': '极佳', 'good': '良好', 'challenging': '有挑战', 'difficult': '困难'}
    r = '# {} + {} 类型融合\n'.format(strategy['primary'], strategy['secondary'])
    r += '\n兼容性: {} {}'.format(compat_cn[strategy['compatibility']], icons[strategy['compatibility']])
    r += '\n\n## 比例建议'
    r += '\n' + strategy['proportion'] + '\n'
    r += '\n## 融合策略'
    for s in strategy['strategies']:
        r += '\n  - ' + s
    r += '\n\n## 常见陷阱'
    for p in strategy['pitfalls']:
        r += '\n  - ' + p
    r += '\n'
    return r


def format_matrix():
    r = '# 网文类型兼容性矩阵\n\n'
    header = '        ' + ' '.join(g['display'].ljust(4) for g in GENRES)
    r += header + '\n'
    compat_icons = {'excellent': ' ★★★★', 'good': ' ★★★ ', 'challenging': ' ★★  ', 'difficult': ' ★   '}
    for g1 in GENRES:
        row = g1['display'].ljust(6) + '  '
        for g2 in GENRES:
            if g1['name'] == g2['name']:
                row += '  —  '
            else:
                c = assess_compatibility(g1, g2)
                row += compat_icons[c]
        r += row + '\n'
    r += '\n★★★★ 极佳 | ★★★ 良好 | ★★ 有挑战 | ★ 困难'
    return r


def main():
    args = sys.argv[1:]
    genre_names = [g['name'] for g in GENRES]
    json_out = '--json' in args

    if '--help' in args or '-h' in args:
        print('网文类型融合策略工具')
        print('Usage: python genre_blend.py <主类型> <副类型>')
        print('       python genre_blend.py --matrix')
        print('类型: ' + ', '.join('{} ({})'.format(g['name'], g['display']) for g in GENRES))
        sys.exit(0)

    if '--matrix' in args:
        print(format_matrix())
        sys.exit(0)

    if '--secondary' in args:
        si = args.index('--secondary')
        secondaries = args[si + 1].split(',') if si + 1 < len(args) else []
        primary = None
        for a in args:
            if not a.startswith('--') and a in genre_names:
                primary = a
                break
        if not primary:
            print('错误: 请指定主类型', file=sys.stderr)
            sys.exit(1)
        for s in secondaries:
            st = get_blend_strategy(primary, s.strip())
            if json_out:
                print(json.dumps(st, indent=2, ensure_ascii=False))
            else:
                print(format_blend_report(st))
        sys.exit(0)

    ga = [a for a in args if not a.startswith('--') and a in genre_names]
    if len(ga) < 2:
        print('错误: 请指定主类型和副类型。使用 --help 查看可用类型。', file=sys.stderr)
        sys.exit(1)
    st = get_blend_strategy(ga[0], ga[1])
    if json_out:
        print(json.dumps(st, indent=2, ensure_ascii=False))
    else:
        print(format_blend_report(st))


if __name__ == '__main__':
    main()
