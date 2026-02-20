#!/usr/bin/env python3
"""revision_audit.py - Track revision pass progress and scene decisions"""

import sys
import re


PASS_CHECKLISTS = {
    'structural': {
        'name': 'Structural Pass',
        'items': [
            'Does the story have a clear dramatic question?',
            "Is the protagonist's goal clear from the start?",
            'Does the protagonist drive the resolution?',
            'Does each scene advance plot or character?',
            'Are there plot holes or logic failures?',
            'Is pacing appropriate (not too slow, not too rushed)?',
            'Does tension escalate toward climax?',
            'Is the climax the highest tension point?',
            'Does the ending satisfy and emerge from the story?',
            'Do all major character arcs complete?',
        ],
    },
    'scene': {
        'name': 'Scene Pass',
        'items': [
            'Does each scene have a clear POV character goal?',
            'Does each scene have conflict preventing the goal?',
            'Does each scene end with disaster or outcome?',
            'Do scenes start late enough (no excessive setup)?',
            'Do scenes end early enough (no wrap-up drag)?',
            'Are scene-sequel rhythms creating good pacing?',
            'Could any scenes be cut without loss?',
            'Could any scenes be combined for efficiency?',
            'Are transitions between scenes clear?',
        ],
    },
    'character': {
        'name': 'Character Pass',
        'items': [
            'Does protagonist have clear lie/false belief at start?',
            'Does protagonist learn truth by end?',
            'Are key transformation moments visible?',
            'Does each major character have consistent voice?',
            'Are character motivations clear for major actions?',
            'Is motivation consistent with established character?',
            "Can you identify who's speaking without tags?",
            'Is character arc progress visible in choices/behavior?',
        ],
    },
    'dialogue': {
        'name': 'Dialogue Pass',
        'items': [
            'Does dialogue have subtext (meaning beneath surface)?',
            'Do characters avoid saying exactly what they mean?',
            'Is there tension between speakers?',
            'Does each exchange advance plot, reveal character, or build dynamics?',
            'Does each character sound distinct?',
            'Are speech patterns consistent per character?',
            'Is dialogue free of exposition dumps?',
            'Are dialogue tags unobtrusive?',
        ],
    },
    'prose': {
        'name': 'Prose Pass',
        'items': [
            'Is passive voice used intentionally, not by default?',
            'Are weak verbs (is, was, had, got) minimized?',
            'Are filter words (saw, felt, noticed) minimized?',
            'Are adverbs used sparingly?',
            'Are pronoun references clear?',
            'Do paragraphs vary in length?',
            'Do sentences vary in length and structure?',
            'Is description integrated with action?',
            'Are specific details used rather than generic?',
            'Does prose read well aloud?',
        ],
    },
    'polish': {
        'name': 'Polish Pass',
        'items': [
            'Is spelling correct (especially names)?',
            'Is grammar correct throughout?',
            'Is punctuation consistent and correct?',
            'Is formatting consistent (chapters, breaks)?',
            'Are character name spellings consistent?',
            'Are place name spellings consistent?',
            'Is timeline internally consistent?',
            'Are physical descriptions consistent?',
            'Have you done a final read-aloud?',
        ],
    },
}

SCENE_BREAK_PATTERNS = [
    re.compile(r'^#{1,3}\s+', re.MULTILINE),
    re.compile(r'^\*{3,}$', re.MULTILINE),
    re.compile(r'^-{3,}$', re.MULTILINE),
    re.compile(r'^~{3,}$', re.MULTILINE),
    re.compile(r'^\s*\*\s*\*\s*\*\s*$', re.MULTILINE),
    re.compile(r'^Chapter\s+\d+', re.MULTILINE | re.IGNORECASE),
    re.compile(r'^CHAPTER\s+', re.MULTILINE),
    re.compile(r'^\[Scene\s+\d+\]', re.MULTILINE | re.IGNORECASE),
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
            scenes.append(chr(10).join(paragraphs[i:i+gs]))
        return scenes
    return [text]


def count_words(text):
    return len([w for w in text.split() if w])


def analyze_scenes(text):
    scenes = split_into_scenes(text)
    result = []
    for i, scene in enumerate(scenes):
        wc = count_words(scene)
        pv = scene.strip()[:100].replace(chr(10), ' ')
        if len(scene) > 100: pv += '...'
        result.append({'number': i+1, 'word_count': wc, 'preview': pv, 'decision': 'pending'})
    return result


def format_scene_report(scenes):
    tw = sum(s['word_count'] for s in scenes)
    avg = tw // len(scenes) if scenes else 0
    r = chr(10) + 'SCENE AUDIT' + chr(10) + '===========' + chr(10)
    r += chr(10) + 'Summary:'
    r += chr(10) + '  Total scenes: ' + str(len(scenes))
    r += chr(10) + '  Total words: {:,}'.format(tw)
    r += chr(10) + '  Average scene length: {:,} words'.format(avg)
    r += chr(10)*2 + 'Scenes:'
    for s in scenes:
        r += chr(10)*2 + '  Scene {}: {:,} words'.format(s['number'], s['word_count'])
        r += chr(10) + '    "{}"'.format(s['preview'])
        r += chr(10) + '    Decision: ' + s['decision']
    r += chr(10)*2 + 'SCENE DECISION GUIDE'
    r += chr(10) + '--------------------'
    r += chr(10) + 'For each scene, ask:'
    r += chr(10) + "  1. What is the POV character's goal?"
    r += chr(10) + '  2. What conflict prevents it?'
    r += chr(10) + '  3. What is the disaster/outcome?'
    r += chr(10) + '  4. Does this advance plot or character?'
    r += chr(10) + '  5. Could the story survive without it?'
    r += chr(10)*2 + 'Decisions:'
    r += chr(10) + '  KEEP - Essential, working well'
    r += chr(10) + '  CUT - Adds nothing essential'
    r += chr(10) + '  COMBINE - Merge with another scene'
    r += chr(10) + '  REVISE - Needed but not working' + chr(10)
    return r


def format_pass_checklist(pass_name):
    key = pass_name.lower()
    if key not in PASS_CHECKLISTS:
        avail = ', '.join(PASS_CHECKLISTS.keys())
        return 'Unknown pass: ' + pass_name + chr(10)*2 + 'Available: ' + avail
    cl = PASS_CHECKLISTS[key]
    r = chr(10) + cl['name'].upper() + ' CHECKLIST'
    r += chr(10) + '=' * (len(cl['name']) + 10) + chr(10)
    for i, item in enumerate(cl['items'], 1):
        r += chr(10) + '  {}. [ ] {}'.format(i, item)
    r += chr(10)*2 + 'Instructions:'
    r += chr(10) + '  - Print this checklist'
    r += chr(10) + '  - Work through your manuscript with these questions'
    r += chr(10) + '  - Check off each item when addressed' + chr(10)
    return r


def format_full_checklist():
    order = ['structural', 'scene', 'character', 'dialogue', 'prose', 'polish']
    r = chr(10) + 'FULL REVISION CHECKLIST' + chr(10) + '=======================' + chr(10)
    for p in order:
        cl = PASS_CHECKLISTS[p]
        r += chr(10) + '## ' + cl['name']
        for item in cl['items']:
            r += chr(10) + '  [ ] ' + item
    r += chr(10)*2 + 'REVISION PRINCIPLES'
    r += chr(10) + '- Work from large to small'
    r += chr(10) + '- Complete one pass before starting the next'
    r += chr(10) + "- Don't polish prose in scenes you might cut"
    r += chr(10) + '- Get external feedback after structural and prose passes' + chr(10)
    return r


def main():
    args = sys.argv[1:]
    if '--scenes' in args:
        idx = args.index('--scenes') + 1
        if idx >= len(args):
            print('Error: --scenes requires a filename', file=sys.stderr)
            sys.exit(1)
        try:
            with open(args[idx], 'r', encoding='utf-8') as fh:
                text = fh.read()
            print(format_scene_report(analyze_scenes(text)))
        except Exception as e:
            print('Error: ' + str(e), file=sys.stderr)
            sys.exit(1)
    elif '--pass' in args:
        idx = args.index('--pass') + 1
        if idx >= len(args):
            print('Error: --pass requires a pass name', file=sys.stderr)
            sys.exit(1)
        print(format_pass_checklist(args[idx]))
    elif '--checklist' in args:
        print(format_full_checklist())
    else:
        print('Usage:')
        print('  python revision_audit.py --scenes <file>')
        print('  python revision_audit.py --pass <passname>')
        print('  python revision_audit.py --checklist')


if __name__ == '__main__':
    main()
