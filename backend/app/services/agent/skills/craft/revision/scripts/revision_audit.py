#!/usr/bin/env python3
"""revision_audit.py - 修订清单与场景审计工具

提供分阶段的修订清单（结构→场景→角色→对话→文笔→润色），
以及场景级别的审计功能。

Usage:
  python revision_audit.py --scenes <file>
  python revision_audit.py --pass <阶段名>
  python revision_audit.py --checklist
"""

import sys
import re

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")


PASS_CHECKLISTS = {
    'structural': {
        'name': '结构审查',
        'items': [
            '故事是否有清晰的核心戏剧问题？',
            '主角的目标是否从一开始就明确？',
            '主角是否驱动了结局的解决？（而非被动接受外部解决）',
            '每个场景是否都推进了情节或角色发展？',
            '是否存在逻辑漏洞或设定矛盾？',
            '节奏是否合适？（不过慢、不过赶）',
            '张力是否逐步升级直到高潮？',
            '高潮是否是全书最紧张的时刻？',
            '结局是否令人满意且源自故事本身？',
            '所有主要角色弧线是否都有收束？',
            '黄金三章是否足够吸引人？',
            '爽点分布是否均匀？（每2-3章至少一个小爽点）',
        ],
    },
    'scene': {
        'name': '场景审查',
        'items': [
            '每个场景是否有清晰的 POV 角色目标？',
            '每个场景是否有阻碍目标的冲突？',
            '每个场景是否以灾难或转折结尾？',
            '场景开头是否足够快？（没有过多铺垫）',
            '场景结尾是否干脆？（没有拖沓收尾）',
            '场景-续篇节奏是否良好交替？',
            '是否有可以删掉的冗余场景？',
            '是否有可以合并的相似场景？',
            '场景之间的过渡是否清晰？',
            '章节末尾是否有足够的悬念/钩子？',
        ],
    },
    'character': {
        'name': '角色审查',
        'items': [
            '主角开头是否有明确的错误信念/弱点？',
            '主角结尾是否获得了成长或领悟？',
            '关键转变时刻是否可见？',
            '每个主要角色的声音是否一致且有辨识度？',
            '角色做出重大行动时动机是否清晰？',
            '动机是否与已建立的角色性格一致？',
            '不看对话标签能否分辨说话者？',
            '角色弧线的进展是否通过选择和行为体现？',
            '配角是否有独立动机？（不只是工具人）',
        ],
    },
    'dialogue': {
        'name': '对话审查',
        'items': [
            '对话是否有潜台词？（表面之下的真实含义）',
            '角色是否避免直接说出自己的想法？',
            '对话双方之间是否有张力？',
            '每段对话是否至少完成两个功能？（推进情节/揭示角色/建立关系）',
            '每个角色的说话方式是否有辨识度？',
            '语言习惯是否在全书中保持一致？',
            '对话中是否没有设定倾泻？',
            '对话标签是否简洁不抢戏？（少用"冷笑道""森然道"）',
            '角色之间的对话是否推动了关系变化？',
        ],
    },
    'prose': {
        'name': '文笔审查',
        'items': [
            '是否避免了 AI 味用语？（"值得注意的是""需要指出的是"）',
            '虚词密度是否合理？（的了着过不过度堆砌）',
            '是否避免了四字格滥用？（连续3+个四字成语）',
            '感官过滤词是否精简？（看到、感觉到、意识到→直接描写）',
            '代词指代是否清晰？',
            '段落长短是否有变化？',
            '句子长短和结构是否有变化？',
            '描写是否与动作融合？（而非静态堆砌）',
            '是否使用了具体细节而非笼统描述？',
            '朗读时是否通顺？',
        ],
    },
    'polish': {
        'name': '润色审查',
        'items': [
            '是否有错别字？（特别是角色名）',
            '标点符号是否正确一致？（中文标点、引号格式）',
            '格式是否统一？（章节标题、分割线）',
            '角色名字是否全书一致？（没有同一角色两种写法）',
            '地名是否全书一致？',
            '时间线是否内部自洽？（白天/黑夜、距离/速度）',
            '外貌描写是否前后一致？（发色、瞳色、身高）',
            '修炼等级/实力是否连贯？（不会莫名其妙变强/变弱）',
            '是否做过完整的通读？',
        ],
    },
}

SCENE_BREAK_PATTERNS = [
    re.compile(r'^#{1,3}\s+', re.MULTILINE),
    re.compile(r'^\*{3,}$', re.MULTILINE),
    re.compile(r'^-{3,}$', re.MULTILINE),
    re.compile(r'^~{3,}$', re.MULTILINE),
    re.compile(r'^\s*\*\s*\*\s*\*\s*$', re.MULTILINE),
    re.compile(r'^第[一二三四五六七八九十百千\d]+章', re.MULTILINE),
    re.compile(r'^Chapter\s+\d+', re.MULTILINE | re.IGNORECASE),
]


def split_into_scenes(text):
    for pattern in SCENE_BREAK_PATTERNS:
        if pattern.search(text):
            scenes = [s.strip() for s in pattern.split(text) if s.strip()]
            if len(scenes) > 1:
                return scenes
    paragraphs = [p.strip() for p in re.split(r'\n\s*\n', text) if p.strip()]
    if len(paragraphs) > 20:
        scenes, gs = [], 7
        for i in range(0, len(paragraphs), gs):
            scenes.append('\n'.join(paragraphs[i:i + gs]))
        return scenes
    return [text]


def count_chars(text):
    return len(text.replace(' ', '').replace('\n', ''))


def analyze_scenes(text):
    scenes = split_into_scenes(text)
    result = []
    for i, scene in enumerate(scenes):
        cc = count_chars(scene)
        pv = scene.strip()[:80].replace('\n', ' ')
        if len(scene) > 80:
            pv += '...'
        result.append({
            'number': i + 1,
            'char_count': cc,
            'preview': pv,
            'decision': '待定',
        })
    return result


def format_scene_report(scenes):
    tc = sum(s['char_count'] for s in scenes)
    avg = tc // len(scenes) if scenes else 0
    r = '\n场景审计\n========\n'
    r += '\n概况:'
    r += '\n  总场景数: ' + str(len(scenes))
    r += '\n  总字数: {:,}'.format(tc)
    r += '\n  平均场景长度: {:,} 字'.format(avg)
    r += '\n\n场景列表:'
    for s in scenes:
        r += '\n\n  场景 {}: {:,} 字'.format(s['number'], s['char_count'])
        r += '\n    "{}"'.format(s['preview'])
        r += '\n    处理决定: ' + s['decision']
    r += '\n\n场景处理指南'
    r += '\n------------'
    r += '\n对每个场景，问自己：'
    r += '\n  1. POV 角色的目标是什么？'
    r += '\n  2. 什么冲突阻碍了目标？'
    r += '\n  3. 灾难/结果是什么？'
    r += '\n  4. 这个场景推进了情节还是角色？'
    r += '\n  5. 删掉它故事能活吗？'
    r += '\n\n处理选项：'
    r += '\n  保留 — 必要且运作良好'
    r += '\n  删除 — 不推进任何必要内容'
    r += '\n  合并 — 与另一场景合并'
    r += '\n  修改 — 必要但需要返工\n'
    return r


def format_pass_checklist(pass_name):
    key = pass_name.lower()
    if key not in PASS_CHECKLISTS:
        avail = '、'.join(PASS_CHECKLISTS.keys())
        return '未知阶段: ' + pass_name + '\n\n可用阶段: ' + avail
    cl = PASS_CHECKLISTS[key]
    r = '\n' + cl['name'] + ' 清单'
    r += '\n' + '=' * (len(cl['name'].encode('utf-8')) + 10) + '\n'
    for i, item in enumerate(cl['items'], 1):
        r += '\n  {}. [ ] {}'.format(i, item)
    r += '\n\n使用方法：'
    r += '\n  - 打印此清单'
    r += '\n  - 对照你的稿件逐条检查'
    r += '\n  - 完成后打勾\n'
    return r


def format_full_checklist():
    order = ['structural', 'scene', 'character', 'dialogue', 'prose', 'polish']
    r = '\n完整修订清单\n============\n'
    for p in order:
        cl = PASS_CHECKLISTS[p]
        r += '\n## ' + cl['name']
        for item in cl['items']:
            r += '\n  [ ] ' + item
    r += '\n\n修订原则'
    r += '\n- 从大到小：先结构后文笔'
    r += '\n- 一次只做一轮：完成一个阶段再开始下一个'
    r += '\n- 不要给可能删掉的场景打磨文笔'
    r += '\n- 结构审查和文笔审查后分别征求外部反馈\n'
    return r


def main():
    args = sys.argv[1:]
    if '--help' in args or '-h' in args:
        print('修订审计工具 (revision_audit.py)')
        print('Usage:')
        print('  python revision_audit.py --scenes <file>    场景审计')
        print('  python revision_audit.py --pass <阶段名>    单阶段清单')
        print('  python revision_audit.py --checklist        完整清单')
        print('阶段: structural, scene, character, dialogue, prose, polish')
        sys.exit(0)
    if '--scenes' in args:
        idx = args.index('--scenes') + 1
        if idx >= len(args):
            print('错误: --scenes 需要文件名', file=sys.stderr)
            sys.exit(1)
        try:
            with open(args[idx], 'r', encoding='utf-8') as fh:
                text = fh.read()
            print(format_scene_report(analyze_scenes(text)))
        except Exception as e:
            print('错误: ' + str(e), file=sys.stderr)
            sys.exit(1)
    elif '--pass' in args:
        idx = args.index('--pass') + 1
        if idx >= len(args):
            print('错误: --pass 需要阶段名', file=sys.stderr)
            sys.exit(1)
        print(format_pass_checklist(args[idx]))
    elif '--checklist' in args:
        print(format_full_checklist())
    else:
        print('Usage:')
        print('  python revision_audit.py --scenes <file>')
        print('  python revision_audit.py --pass <阶段名>')
        print('  python revision_audit.py --checklist')


if __name__ == '__main__':
    main()
