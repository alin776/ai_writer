#!/usr/bin/env python3
"""orthogonality_check.py - 网文套路 vs 正交性评估工具

评估故事元素是套路化的还是具有"正交性"（独立逻辑），
帮助作者突破常见网文套路。

Usage:
  python orthogonality_check.py "元素描述"
  python orthogonality_check.py --json "元素描述"
"""

import sys
import json

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")


def generate_check(element):
    return {
        'element': element,
        'axes': {
            'form': {
                'axis': '形态',
                'question': '「{}」是什么？'.format(element),
                'cliche': '该类型的默认/标准版本',
                'orthogonal': '形态本身可以是常见的——正交性体现在其他维度',
            },
            'knowledge': {
                'axis': '认知',
                'question': '「{}」知道主线剧情吗？'.format(element),
                'cliche': '了解核心冲突，是冲突的一部分',
                'orthogonal': '有自己的关注点，与主线只是偶然相交',
            },
            'goal': {
                'axis': '目标',
                'question': '「{}」想要什么？'.format(element),
                'cliche': '目标是帮助/阻止主角完成主线任务',
                'orthogonal': '追求与主线无关的东西，但恰好产生碰撞',
            },
            'role': {
                'axis': '角色',
                'question': '「{}」在故事中扮演什么功能？'.format(element),
                'cliche': '存在的意义就是当主角的工具人/反派',
                'orthogonal': '有自己的故事线，与主角只是交叉',
            },
        },
        'key_test': '「{}」知道自己在什么类型的故事里吗？（套路化的元素知道；正交的元素以为自己在另一个故事里）'.format(element),
        'assessment': 'needs-input',
        'suggestions': [],
    }


def format_questionnaire(check):
    r = '# 正交性评估：「{}」\n\n'.format(check['element'])
    r += '## 四维分析\n\n'
    r += '对每个维度，判断你的元素更接近哪一列：\n'
    for key, axis in check['axes'].items():
        r += '\n### ' + axis['axis']
        r += '\n**问题：** ' + axis['question'] + '\n'
        r += '\n| 套路版 | 正交版 |'
        r += '\n|--------|--------|'
        r += '\n| {} | {} |'.format(axis['cliche'], axis['orthogonal'])
        r += '\n'
    r += '\n## 核心测试\n'
    r += '\n> ' + check['key_test'] + '\n'
    r += '\n- 如果是 → 这个元素可能是套路化的'
    r += '\n- 如果否 → 这个元素有自己的独立逻辑，与你的故事产生碰撞\n'
    r += '\n## 突破策略\n'
    r += '\n如果元素过于套路化，尝试旋转一个或多个维度：\n'
    el = check['element']
    r += '\n1. **改变认知**：如果「{}」完全不知道主线在发生什么？'.format(el)
    r += '\n2. **改变目标**：如果「{}」追求的东西与主线毫无关系，但恰好制造了冲突？'.format(el)
    r += '\n3. **改变角色**：如果「{}」有自己的故事，只是偶然闯入了主角的世界？'.format(el)
    r += '\n\n## 网文套路突破示例\n'
    r += '\n反派长老刁难主角（套路）：'
    r += '\n- 长老知道主角有特殊血脉，故意阻拦'
    r += '\n- 目标是为主角制造升级动力'
    r += '\n\n反派长老刁难主角（正交）：'
    r += '\n- 长老在追查二十年前的门派叛徒，主角只是恰好触发了他的疑心'
    r += '\n- 长老以为自己在一个复仇故事里，不知道这是主角的成长故事\n'
    return r


def main():
    args = sys.argv[1:]
    if '--help' in args or '-h' in args:
        print('正交性评估工具 — 检测网文元素是套路还是独立')
        print('Usage:')
        print('  python orthogonality_check.py "元素描述"')
        print('  python orthogonality_check.py --json "元素描述"')
        sys.exit(0)
    json_out = '--json' in args
    element = None
    for a in args:
        if not a.startswith('--'):
            element = a
            break
    if not element:
        print('错误: 未提供元素描述。使用 --help 查看用法。', file=sys.stderr)
        sys.exit(1)
    check = generate_check(element)
    if json_out:
        print(json.dumps(check, indent=2, ensure_ascii=False))
    else:
        print(format_questionnaire(check))


if __name__ == '__main__':
    main()
