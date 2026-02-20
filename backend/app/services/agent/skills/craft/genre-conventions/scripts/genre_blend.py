#!/usr/bin/env python3
"""genre_blend.py - Secondary genre integration strategies"""

import sys
import json


GENRES = [
    {'name': 'wonder', 'display': 'Wonder', 'promise': 'Awe and fascination', 'pacing': 'slow', 'tone': 'light', 'focus': 'external'},
    {'name': 'idea', 'display': 'Idea', 'promise': 'Intellectual fascination', 'pacing': 'slow', 'tone': 'neutral', 'focus': 'internal'},
    {'name': 'adventure', 'display': 'Adventure', 'promise': 'Excitement through challenges', 'pacing': 'fast', 'tone': 'neutral', 'focus': 'external'},
    {'name': 'horror', 'display': 'Horror', 'promise': 'Dread and fear', 'pacing': 'moderate', 'tone': 'dark', 'focus': 'both'},
    {'name': 'mystery', 'display': 'Mystery', 'promise': 'Curiosity about unknowns', 'pacing': 'moderate', 'tone': 'neutral', 'focus': 'external'},
    {'name': 'thriller', 'display': 'Thriller', 'promise': 'Tension through danger', 'pacing': 'fast', 'tone': 'dark', 'focus': 'external'},
    {'name': 'humor', 'display': 'Humor', 'promise': 'Entertainment and amusement', 'pacing': 'fast', 'tone': 'light', 'focus': 'both'},
    {'name': 'relationship', 'display': 'Relationship', 'promise': 'Investment in connections', 'pacing': 'slow', 'tone': 'neutral', 'focus': 'internal'},
    {'name': 'drama', 'display': 'Drama', 'promise': 'Internal transformation', 'pacing': 'slow', 'tone': 'neutral', 'focus': 'internal'},
    {'name': 'issue', 'display': 'Issue', 'promise': 'Exploration of questions', 'pacing': 'slow', 'tone': 'neutral', 'focus': 'both'},
    {'name': 'ensemble', 'display': 'Ensemble', 'promise': 'Group dynamics', 'pacing': 'moderate', 'tone': 'neutral', 'focus': 'both'},
]

GENRE_MAP = {g['name']: g for g in GENRES}


def assess_compatibility(p, s):
    score = 0
    if p['pacing'] == s['pacing']: score += 2
    elif 'moderate' in (p['pacing'], s['pacing']): score += 1
    if p['tone'] == s['tone']: score += 2
    elif 'neutral' in (p['tone'], s['tone']): score += 1
    elif p['tone'] != s['tone']: score -= 1
    if p['focus'] == s['focus']: score += 1
    elif 'both' in (p['focus'], s['focus']): score += 1
    if score >= 4: return 'excellent'
    if score >= 2: return 'good'
    if score >= 0: return 'challenging'
    return 'difficult'


def get_blend_strategy(primary_name, secondary_name):
    p = GENRE_MAP.get(primary_name)
    s = GENRE_MAP.get(secondary_name)
    if not p or not s:
        raise ValueError('Unknown genre: ' + (primary_name if not p else secondary_name))
    compat = assess_compatibility(p, s)
    strategies, pitfalls = [], []
    if p['pacing'] == 'fast' and s['pacing'] == 'slow':
        strategies.append('Use {} elements in setup and aftermath'.format(s['display']))
        pitfalls.append('{} elements may slow {} momentum'.format(s['display'], p['display']))
    elif p['pacing'] == 'slow' and s['pacing'] == 'fast':
        strategies.append('{} sequences can punctuate {} contemplation'.format(s['display'], p['display']))
    if p['tone'] == 'dark' and s['tone'] == 'light':
        strategies.append('Use contrast deliberately - light moments make dark moments darker')
        pitfalls.append('Tonal whiplash if transitions not managed')
    strategies.append('{} elements should serve {} promise'.format(s['display'], p['display']))
    pitfalls.append('{} overwhelming {} if proportions not maintained'.format(s['display'], p['display']))
    prop_map = {
        'excellent': '60% {} / 40% {} - integrate throughout',
        'good': '70% {} / 30% {} - secondary in specific scenes',
        'challenging': '80% {} / 20% {} - secondary as accent',
        'difficult': '85% {} / 15% {} - requires careful craft',
    }
    prop = prop_map[compat].format(p['display'], s['display'])
    return {
        'primary': p['display'], 'secondary': s['display'],
        'compatibility': compat, 'strategies': strategies,
        'pitfalls': pitfalls, 'proportion': prop,
    }


def format_blend_report(strategy):
    icons = {'excellent': '++++', 'good': '+++', 'challenging': '++', 'difficult': '+'}
    r = '# {} + {} Blend'.format(strategy['primary'], strategy['secondary']) + chr(10)
    r += chr(10) + 'Compatibility: {} {}'.format(strategy['compatibility'].upper(), icons[strategy['compatibility']])
    r += chr(10)*2 + '## Proportion Guideline'
    r += chr(10) + strategy['proportion'] + chr(10)
    r += chr(10) + '## Integration Strategies'
    for s in strategy['strategies']: r += chr(10) + '  - ' + s
    r += chr(10)*2 + '## Common Pitfalls'
    for p in strategy['pitfalls']: r += chr(10) + '  - ' + p
    r += chr(10)
    return r


def format_matrix():
    r = '# Genre Compatibility Matrix' + chr(10)*2
    header = '       ' + ' '.join(g['name'][:4].ljust(5) for g in GENRES)
    r += header + chr(10)
    for g1 in GENRES:
        row = g1['name'][:6].ljust(7)
        for g2 in GENRES:
            if g1['name'] == g2['name']:
                row += '  -  '
            else:
                c = assess_compatibility(g1, g2)
                icons = {'excellent': ' ++++ ', 'good': ' +++  ', 'challenging': ' ++   ', 'difficult': ' +    '}
                row += icons[c]
        r += row + chr(10)
    r += chr(10) + '++++ excellent | +++ good | ++ challenging | + difficult'
    return r


def main():
    args = sys.argv[1:]
    genre_names = [g['name'] for g in GENRES]
    json_out = '--json' in args
    if '--help' in args or '-h' in args:
        print('Genre Blend Helper - Secondary genre integration strategies')
        print('Usage: python genre_blend.py <primary> <secondary>')
        print('       python genre_blend.py --matrix')
        print('Genres: ' + ', '.join(genre_names))
        sys.exit(0)
    if '--matrix' in args:
        print(format_matrix())
        sys.exit(0)
    if '--secondary' in args:
        si = args.index('--secondary')
        secondaries = args[si+1].split(',') if si+1 < len(args) else []
        primary = None
        for a in args:
            if not a.startswith('--') and a in genre_names:
                primary = a
                break
        if not primary:
            print('Error: Specify a primary genre', file=sys.stderr)
            sys.exit(1)
        for s in secondaries:
            st = get_blend_strategy(primary, s.strip())
            if json_out: print(json.dumps(st, indent=2))
            else: print(format_blend_report(st))
        sys.exit(0)
    ga = [a for a in args if not a.startswith('--') and a in genre_names]
    if len(ga) < 2:
        print('Error: Specify primary and secondary genres', file=sys.stderr)
        sys.exit(1)
    st = get_blend_strategy(ga[0], ga[1])
    if json_out: print(json.dumps(st, indent=2))
    else: print(format_blend_report(st))


if __name__ == '__main__':
    main()
