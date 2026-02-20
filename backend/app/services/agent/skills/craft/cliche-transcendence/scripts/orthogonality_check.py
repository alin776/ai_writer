#!/usr/bin/env python3
"""orthogonality_check.py - Evaluate if a story element is cliched or orthogonal"""

import sys
import json


def generate_check(element):
    return {
        'element': element,
        'axes': {
            'form': {
                'axis': 'Form',
                'question': 'What is the "{}"?'.format(element),
                'cliche': 'The expected/default version of this element',
                'orthogonal': 'Same form is fine - orthogonality is in other axes',
            },
            'knowledge': {
                'axis': 'Knowledge',
                'question': 'What does "{}" know about the central plot/mystery?'.format(element),
                'cliche': 'Knows about the main conflict; part of it',
                'orthogonal': 'Has own concerns; intersects with plot accidentally',
            },
            'goal': {
                'axis': 'Goal',
                'question': 'What does "{}" want?'.format(element),
                'cliche': 'Wants to help/stop protagonist regarding main plot',
                'orthogonal': 'Wants something unrelated that happens to collide',
            },
            'role': {
                'axis': 'Role',
                'question': 'What function does "{}" serve in the story?'.format(element),
                'cliche': 'Exists to be obstacle/ally for protagonist',
                "orthogonal": "Has own story that intersects with protagonist's",
            },
        },
        'key_test': 'Does "{}" know what story it\'s in? (Cliche elements know; orthogonal elements think they\'re in a different story)'.format(element),
        'assessment': 'needs-input',
        'suggestions': [],
    }


def format_questionnaire(check):
    r = '# Orthogonality Check: "{}"'.format(check['element']) + chr(10)*2
    r += '## The Four Axes' + chr(10)*2
    r += 'For each axis, consider which answer better describes your element:' + chr(10)
    for key, axis in check['axes'].items():
        r += chr(10) + '### ' + axis['axis']
        r += chr(10) + '**Question:** ' + axis['question'] + chr(10)
        r += chr(10) + '| Cliche Version | Orthogonal Version |'
        r += chr(10) + '|----------------|-------------------|'
        r += chr(10) + '| {} | {} |'.format(axis['cliche'], axis['orthogonal'])
        r += chr(10)
    r += chr(10) + '## The Key Test' + chr(10)
    r += chr(10) + '> ' + check['key_test'] + chr(10)
    r += chr(10) + '- If YES -> The element is likely cliched'
    r += chr(10) + '- If NO -> The element has its own logic that collides with your story' + chr(10)
    r += chr(10) + '## Transformation Strategies' + chr(10)
    r += chr(10) + 'If the element is cliched, try rotating on one or more axes:' + chr(10)
    el = check['element']
    r += chr(10) + '1. **Change Knowledge**: What if "{}" doesn\'t know about the central plot?'.format(el)
    r += chr(10) + '2. **Change Goal**: What if "{}" wants something unrelated that creates conflict?'.format(el)
    r += chr(10) + '3. **Change Role**: What if "{}" has their own story that intersects accidentally?'.format(el)
    r += chr(10)*2 + '## Example Transformation' + chr(10)
    r += chr(10) + 'FBI agents investigating UFO (cliche):'
    r += chr(10) + '- Know about aliens, part of cover-up'
    r += chr(10) + chr(10) + 'FBI agents investigating UFO (orthogonal):'
    r += chr(10) + '- Working a missing persons case, not aliens'
    r += chr(10) + '- They think they\'re in a crime drama, not a UFO story' + chr(10)
    return r


def main():
    args = sys.argv[1:]
    if '--help' in args or '-h' in args:
        print('Orthogonality Check Tool')
        print('Usage:')
        print('  python orthogonality_check.py "element description"')
        print('  python orthogonality_check.py --json "element"')
        sys.exit(0)
    json_out = '--json' in args
    element = None
    for a in args:
        if not a.startswith('--'):
            element = a
            break
    if not element:
        print('Error: No element provided. Use --help for usage.', file=sys.stderr)
        sys.exit(1)
    check = generate_check(element)
    if json_out:
        print(json.dumps(check, indent=2))
    else:
        print(format_questionnaire(check))


if __name__ == '__main__':
    main()
