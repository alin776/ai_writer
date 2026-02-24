#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""genre_check.py - 网文类型检测与分析工具

分析文本中的网文类型元素，支持 11 种主流网文类型。

用法:
  python genre_check.py --text "文本内容" --genre xuanhuan
  python genre_check.py novel.txt --genre xianxia --json
  python genre_check.py novel.txt --analyze
  python genre_check.py --help
"""

import sys
import re
import json
import io

# 确保 stdout 使用 UTF-8 编码（Windows 兼容）
if hasattr(sys.stdout, 'buffer'):
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
if hasattr(sys.stderr, 'buffer'):
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')


# ── 类型定义 ──────────────────────────────────────────────────────────

GENRE_PATTERNS = {}


def _gp(name, display, promise, required, patterns):
    """注册一个网文类型及其检测模式。"""
    compiled = {}
    for cat, pats in patterns.items():
        compiled[cat] = [re.compile(p) for p in pats]
    GENRE_PATTERNS[name] = {
        'display': display,
        'promise': promise,
        'required': required,
        'patterns': compiled,
    }


# ── 1. 玄幻 ──────────────────────────────────────────────────────────

_gp('xuanhuan', '玄幻', '修炼突破的爽感',
    ['修炼体系', '战斗场面', '力量道具'], {
    'cultivation': [
        r'修炼|突破|境界|丹田|灵气|内力|功法|心法',
        r'气海|经脉|真气|灵力|修为|筑基|金丹|元婴',
    ],
    'combat': [
        r'战斗|对决|招式|剑气|拳风',
        r'杀招|绝学|爆发|碾压|秒杀|一击|对轰',
    ],
    'power_system': [
        r'灵石|灵药|法器|储物戒|阵法',
        r'丹炉|炼器|炼丹|灵脉|洞府|秘境',
    ],
})

# ── 2. 都市 ──────────────────────────────────────────────────────────

_gp('urban', '都市', '现代都市的传奇',
    ['现代生活', '社会关系', '冲突对抗'], {
    'modern_life': [
        r'公司|总裁|豪车|别墅|商场',
        r'写字楼|CBD|集团|董事|股份|合同|项目',
    ],
    'social': [
        r'面子|关系|背景|实力|圈子',
        r'人脉|家族|权势|地位|身份|资源',
    ],
    'conflict': [
        r'打脸|装逼|看不起|嘲讽|后悔',
        r'跪下|求饶|震惊|傻眼|目瞪口呆|不敢相信',
    ],
})

# ── 3. 仙侠 ──────────────────────────────────────────────────────────

_gp('xianxia', '仙侠', '求仙问道的旅程',
    ['修仙体系', '仙界设定', '法宝仙器'], {
    'cultivation': [
        r'仙人|飞升|渡劫|天劫|仙气|道心',
        r'仙路|证道|大道|天道|劫雷|仙劫|化神',
    ],
    'world': [
        r'仙界|洞天|福地|宗门|山门',
        r'灵山|仙宫|天庭|仙域|修仙界|上界|下界',
    ],
    'artifacts': [
        r'仙剑|法宝|丹药|灵植|仙器',
        r'飞剑|御剑|神通|道法|符箓|玉简',
    ],
})

# ── 4. 科幻 ──────────────────────────────────────────────────────────

_gp('scifi', '科幻', '未来科技的想象',
    ['科技元素', '太空设定', '社会形态'], {
    'tech': [
        r'飞船|星际|机甲|人工智能|基因|纳米',
        r'量子|光脑|芯片|能量盾|激光|粒子|引擎',
    ],
    'space': [
        r'星球|宇宙|银河|虫洞|超光速',
        r'空间站|太阳系|恒星|星系|跃迁|曲率|星门',
    ],
    'society': [
        r'联邦|文明|殖民|外星|异族',
        r'帝国|议会|星际联盟|母星|殖民地|舰队',
    ],
})

# ── 5. 末世 ──────────────────────────────────────────────────────────

_gp('apocalypse', '末世', '绝境求生的紧迫',
    ['灾变设定', '生存要素', '进化体系'], {
    'disaster': [
        r'丧尸|末世|灾变|变异|辐射|病毒',
        r'末日|废墟|荒芜|坍塌|污染|丧尸潮',
    ],
    'survival': [
        r'据点|物资|食物|弹药|幸存者',
        r'避难所|补给|搜刮|庇护|营地|求生',
    ],
    'evolution': [
        r'异能|进化|觉醒|变异体|晶核',
        r'能力者|超能力|觉醒者|血清|强化|适应',
    ],
})

# ── 6. 游戏 ──────────────────────────────────────────────────────────

_gp('game', '游戏', '游戏化的成长',
    ['系统面板', '游戏机制', '成长进阶'], {
    'system': [
        r'系统|面板|属性|等级|经验值|技能点',
        r'状态栏|血量|蓝量|HP|MP|数值|界面',
    ],
    'mechanics': [
        r'任务|副本|BOSS|掉落|装备',
        r'刷怪|组队|PK|竞技|公会|排行榜|奖励',
    ],
    'growth': [
        r'升级|进阶|转职|觉醒|天赋',
        r'突破|满级|称号|成就|技能树|加点',
    ],
})

# ── 7. 历史 ──────────────────────────────────────────────────────────

_gp('historical', '历史', '历史风云的沉浸',
    ['时代背景', '政治权谋', '文化礼制'], {
    'setting': [
        r'朝廷|皇帝|大臣|江湖|王朝',
        r'太子|丞相|将军|天子|京城|边关|藩王',
    ],
    'politics': [
        r'权谋|阴谋|结盟|叛乱|争位',
        r'夺嫡|党争|变法|逼宫|拥立|谋反|联姻',
    ],
    'culture': [
        r'诗词|礼仪|科举|门阀|世家',
        r'儒|道|佛|士族|寒门|书院|功名',
    ],
})

# ── 8. 言情 ──────────────────────────────────────────────────────────

_gp('romance', '言情', '情感关系的满足',
    ['情感描写', '关系发展', '情感冲突'], {
    'emotion': [
        r'心动|脸红|心跳|暧昧|甜蜜',
        r'怦然|小鹿乱撞|脸颊发烫|酥麻|悸动|温柔',
    ],
    'relationship': [
        r'喜欢|爱|告白|在一起|分手',
        r'牵手|拥抱|亲吻|约会|恋人|情侣|表白',
    ],
    'conflict': [
        r'误会|纠葛|情敌|虐心|错过',
        r'三角|背叛|隐瞒|吃醋|争吵|冷战|和好',
    ],
})

# ── 9. 悬疑 ──────────────────────────────────────────────────────────

_gp('suspense', '悬疑', '真相揭露的快感',
    ['谜团设置', '调查推理', '真相揭露'], {
    'mystery': [
        r'线索|嫌疑人|真相|秘密|谜团',
        r'蹊跷|疑点|不对劲|隐情|蛛丝马迹|疑云',
    ],
    'investigation': [
        r'调查|推理|证据|分析|破案',
        r'排查|审讯|侦查|勘察|现场|作案|动机',
    ],
    'revelation': [
        r'发现|揭露|原来|真凶|幕后',
        r'真相大白|水落石出|浮出水面|揭开|谜底',
    ],
})

# ── 10. 奇幻 ─────────────────────────────────────────────────────────

_gp('fantasy', '奇幻', '异世界的冒险',
    ['世界设定', '冒险任务', '魔法体系'], {
    'world': [
        r'大陆|王国|精灵|矮人|魔法',
        r'龙|兽人|神殿|魔族|圣域|异世界|位面',
    ],
    'quest': [
        r'冒险|任务|勇者|魔王|拯救',
        r'冒险者|公会|佣兵|探索|远征|讨伐|屠龙',
    ],
    'magic': [
        r'魔力|咒语|元素|召唤|结界',
        r'法阵|施法|禁咒|魔导|魔纹|附魔|吟唱',
    ],
})

# ── 11. 武侠 ─────────────────────────────────────────────────────────

_gp('wuxia', '武侠', '江湖恩怨的快意',
    ['武功招式', '江湖生态', '侠义精神'], {
    'martial': [
        r'武功|内力|轻功|剑法|掌法',
        r'刀法|拳法|暗器|点穴|气功|真气|武学',
    ],
    'jianghu': [
        r'江湖|门派|武林|盟主|恩怨',
        r'帮派|少林|武当|丐帮|武林大会|镖局|客栈',
    ],
    'chivalry': [
        r'侠义|恩仇|行侠|仗义|快意',
        r'侠客|大侠|义气|豪爽|报仇|除暴安良|路见不平',
    ],
})


# ── 分析引擎 ─────────────────────────────────────────────────────────

def count_matches(text, patterns):
    """统计文本中匹配指定模式的独立关键词数量。"""
    matches = []
    for pattern in patterns:
        found = pattern.findall(text)
        if found:
            matches.extend(found[:3])
    unique = list(dict.fromkeys(
        m.lower() if isinstance(m, str) else m[0].lower() for m in matches
    ))
    return {'count': len(unique), 'samples': unique[:5]}


def analyze_for_genre(text, genre_name):
    """针对单一类型分析文本，返回评分与分类明细。"""
    genre = GENRE_PATTERNS[genre_name]
    breakdown = {}
    total = 0
    for cat, patterns in genre['patterns'].items():
        result = count_matches(text, patterns)
        breakdown[cat] = result
        total += result['count']

    cat_count = len(genre['patterns'])
    max_score = cat_count * 5
    score = min(100, round((total / max_score) * 100)) if max_score else 0

    # 分类中文名映射
    cat_labels = {
        'cultivation': '修炼体系', 'combat': '战斗场面', 'power_system': '力量道具',
        'modern_life': '现代生活', 'social': '社会关系', 'conflict': '冲突对抗',
        'world': '世界设定', 'artifacts': '法宝仙器',
        'tech': '科技元素', 'space': '太空设定', 'society': '社会形态',
        'disaster': '灾变设定', 'survival': '生存要素', 'evolution': '进化体系',
        'system': '系统面板', 'mechanics': '游戏机制', 'growth': '成长进阶',
        'setting': '时代背景', 'politics': '政治权谋', 'culture': '文化礼制',
        'emotion': '情感描写', 'relationship': '关系发展',
        'mystery': '谜团设置', 'investigation': '调查推理', 'revelation': '真相揭露',
        'quest': '冒险任务', 'magic': '魔法体系',
        'martial': '武功招式', 'jianghu': '江湖生态', 'chivalry': '侠义精神',
    }

    present = [cat_labels.get(c, c) for c, r in breakdown.items() if r['count'] > 0]
    missing = [cat_labels.get(c, c) for c, r in breakdown.items() if r['count'] == 0]

    issues = []
    recs = []
    if score < 20:
        issues.append('几乎未检测到「{}」类型元素'.format(genre['display']))
        recs.append('建议补充以下核心要素：' + '、'.join(genre['required']))
    if missing:
        issues.append('缺失分类：' + '、'.join(missing))

    return {
        'genre': genre['display'],
        'score': score,
        'total_matches': total,
        'breakdown': breakdown,
        'present': present,
        'missing': missing,
        'issues': issues,
        'recommendations': recs,
    }


def analyze_multi_genre(text):
    """对文本进行全类型扫描，返回综合评分与主类型详情。"""
    scores = {}
    best_name, best_score = None, 0
    for name in GENRE_PATTERNS:
        a = analyze_for_genre(text, name)
        scores[GENRE_PATTERNS[name]['display']] = a['score']
        if a['score'] > best_score:
            best_score = a['score']
            best_name = name

    # 中文字符计数（更适合网文场景）
    char_count = len(re.findall(r'[\u4e00-\u9fff]', text))

    return {
        'char_count': char_count,
        'word_count': len([w for w in text.split() if w]),
        'likely_primary': GENRE_PATTERNS[best_name]['display'] if best_name else '未知',
        'scores': scores,
        'detailed': analyze_for_genre(text, best_name) if best_name else None,
    }


# ── 报告格式化 ────────────────────────────────────────────────────────

def format_report(a):
    """格式化单类型分析报告（中文输出）。"""
    nl = chr(10)
    r = '# 「{}」类型分析报告'.format(a['genre']) + nl * 2
    r += '## 匹配评分：{}/100'.format(a['score']) + nl * 2

    # 评分条
    bar_full = a['score'] // 5
    bar_str = '█' * bar_full + '░' * (20 - bar_full)
    r += '  [{}] {}/100'.format(bar_str, a['score']) + nl * 2

    # 评语
    if a['score'] >= 80:
        r += '> 判定：**高度符合**「{}」类型，核心承诺「{}」得到充分兑现。'.format(
            a['genre'], GENRE_PATTERNS[[k for k, v in GENRE_PATTERNS.items() if v['display'] == a['genre']][0]]['promise']
        ) + nl * 2
    elif a['score'] >= 50:
        r += '> 判定：**基本符合**「{}」类型，部分元素仍可加强。'.format(a['genre']) + nl * 2
    elif a['score'] >= 20:
        r += '> 判定：**弱匹配**「{}」类型，核心元素不足。'.format(a['genre']) + nl * 2
    else:
        r += '> 判定：**不符合**「{}」类型。'.format(a['genre']) + nl * 2

    r += '## 分类明细' + nl
    for cat, res in a['breakdown'].items():
        # 分类中文名映射（与 analyze_for_genre 保持一致）
        cat_labels = {
            'cultivation': '修炼体系', 'combat': '战斗场面', 'power_system': '力量道具',
            'modern_life': '现代生活', 'social': '社会关系', 'conflict': '冲突对抗',
            'world': '世界设定', 'artifacts': '法宝仙器',
            'tech': '科技元素', 'space': '太空设定', 'society': '社会形态',
            'disaster': '灾变设定', 'survival': '生存要素', 'evolution': '进化体系',
            'system': '系统面板', 'mechanics': '游戏机制', 'growth': '成长进阶',
            'setting': '时代背景', 'politics': '政治权谋', 'culture': '文化礼制',
            'emotion': '情感描写', 'relationship': '关系发展',
            'mystery': '谜团设置', 'investigation': '调查推理', 'revelation': '真相揭露',
            'quest': '冒险任务', 'magic': '魔法体系',
            'martial': '武功招式', 'jianghu': '江湖生态', 'chivalry': '侠义精神',
        }
        label = cat_labels.get(cat, cat)
        st = '✓' if res['count'] > 0 else '✗'
        samples = '：' + '、'.join(res['samples']) if res['samples'] else ''
        r += '  {} {} ({}){}'.format(st, label, res['count'], samples) + nl

    if a['present']:
        r += nl + '## 已覆盖：' + '、'.join(a['present']) + nl
    if a['missing']:
        r += nl + '## 待补充：' + '、'.join(a['missing']) + nl
    if a['issues']:
        r += nl + '## 问题' + nl
        for i in a['issues']:
            r += '  - ' + i + nl
    if a['recommendations']:
        r += nl + '## 建议' + nl
        for rec in a['recommendations']:
            r += '  - ' + rec + nl
    return r


def format_multi_report(a):
    """格式化多类型综合分析报告（中文输出）。"""
    nl = chr(10)
    r = '# 网文类型综合分析' + nl * 2
    r += '字数统计：{} 汉字 / {} 词'.format(a['char_count'], a['word_count']) + nl
    r += '最可能类型：**{}**'.format(a['likely_primary']) + nl * 2

    r += '## 各类型评分' + nl
    for genre, score in sorted(a['scores'].items(), key=lambda x: x[1], reverse=True):
        bar = '█' * (score // 5) + '░' * (20 - score // 5)
        r += '  {} [{}] {}'.format(genre.ljust(6, '\u3000'), bar, score) + nl

    if a['detailed']:
        r += nl + '## 主类型详细分析' + nl * 2
        r += format_report(a['detailed'])
    return r


# ── 帮助信息 ─────────────────────────────────────────────────────────

HELP_TEXT = """genre_check.py - 网文类型检测与分析工具

用法:
  python genre_check.py --text "文本内容" --genre <类型> [--json]
  python genre_check.py <文件路径> --genre <类型> [--json]
  python genre_check.py --text "文本内容" --analyze [--json]
  python genre_check.py <文件路径> --analyze [--json]
  python genre_check.py --help

参数:
  --text "..."    直接传入待分析文本
  <文件路径>      从文件读取待分析文本（UTF-8 编码）
  --genre <类型>  指定单一类型进行分析
  --analyze       对所有 11 种类型进行综合分析
  --json          以 JSON 格式输出结果
  --help          显示此帮助信息

支持的网文类型:
  xuanhuan    玄幻    修炼突破的爽感
  urban       都市    现代都市的传奇
  xianxia     仙侠    求仙问道的旅程
  scifi       科幻    未来科技的想象
  apocalypse  末世    绝境求生的紧迫
  game        游戏    游戏化的成长
  historical  历史    历史风云的沉浸
  romance     言情    情感关系的满足
  suspense    悬疑    真相揭露的快感
  fantasy     奇幻    异世界的冒险
  wuxia       武侠    江湖恩怨的快意

示例:
  python genre_check.py --text "他盘膝而坐，丹田内灵气翻涌，突破在即" --genre xuanhuan
  python genre_check.py novel.txt --analyze --json
"""


# ── 主入口 ───────────────────────────────────────────────────────────

def main():
    args = sys.argv[1:]

    # 帮助
    if '--help' in args or '-h' in args or not args:
        print(HELP_TEXT)
        sys.exit(0)

    json_out = '--json' in args

    # 获取文本
    text = ''
    if '--text' in args:
        idx = args.index('--text')
        text = args[idx + 1] if idx + 1 < len(args) else ''
    else:
        # 跳过已知 flag 及其参数值
        flag_with_value = {'--genre', '--text'}
        skip_next = False
        for a in args:
            if skip_next:
                skip_next = False
                continue
            if a in flag_with_value:
                skip_next = True
                continue
            if a.startswith('--'):
                continue
            if a in list(GENRE_PATTERNS.keys()):
                continue
            # 先尝试当文件路径打开，失败则视为内联文本
            try:
                with open(a, 'r', encoding='utf-8') as fh:
                    text = fh.read()
                break
            except Exception:
                text = a
                break

    if not text.strip():
        print('错误：未提供文本。请使用 --text 或传入文件路径。', file=sys.stderr)
        sys.exit(1)

    # 综合分析模式
    if '--analyze' in args:
        a = analyze_multi_genre(text)
        print(json.dumps(a, indent=2, ensure_ascii=False) if json_out else format_multi_report(a))
        sys.exit(0)

    # 单类型分析模式
    if '--genre' in args:
        gi = args.index('--genre')
        gn = args[gi + 1].lower() if gi + 1 < len(args) else None
        if gn not in GENRE_PATTERNS:
            available = ', '.join(
                '{} ({})'.format(k, v['display']) for k, v in GENRE_PATTERNS.items()
            )
            print('错误：未知类型「{}」。可用类型：{}'.format(gn, available), file=sys.stderr)
            sys.exit(1)
        a = analyze_for_genre(text, gn)
        print(json.dumps(a, indent=2, ensure_ascii=False, default=str) if json_out else format_report(a))
        sys.exit(0)

    print('错误：请指定 --genre <类型> 或 --analyze 进行分析。', file=sys.stderr)
    sys.exit(1)


if __name__ == '__main__':
    main()
