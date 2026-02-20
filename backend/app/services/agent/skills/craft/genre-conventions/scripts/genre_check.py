#!/usr/bin/env python3
"""genre_check.py - Analyze text for genre-specific elements"""

import sys
import re
import json


GENRE_PATTERNS = {}

def _gp(name, display, promise, required, patterns):
    compiled = {}
    for cat, pats in patterns.items():
        compiled[cat] = [re.compile(p, re.IGNORECASE) for p in pats]
    GENRE_PATTERNS[name] = {'display': display, 'promise': promise, 'required': required, 'patterns': compiled}

_gp('wonder', 'Wonder', 'Awe and fascination', ['scale/scope', 'discovery', 'perspective shifts'], {
    'scale_scope': [r'\b(vast|immense|infinite|endless|boundless|cosmic)\b', r'\b(horizon|expanse|beyond|stretching)\b'],
    'discovery': [r'\b(discover|discovered|revelation|reveal|revealed)\b', r'\b(first time|never before|unprecedented)\b'],
    'awe': [r'\b(awe|wonder|amazement|marvel)\b', r'\b(breathtaking|magnificent|spectacular)\b'],
})

_gp('mystery', 'Mystery', 'Curiosity about unknown facts', ['clues', 'investigation', 'revelation'], {
    'clues': [r'\b(clue|evidence|proof|trace|sign)\b', r'\b(strange|odd|unusual|suspicious)\b'],
    'investigation': [r'\b(investigate|examine|inspect|analyze)\b', r'\b(question|interview|interrogate)\b'],
    'revelation': [r'\b(truth|answer|solution|revelation)\b', r'\b(realize|understand|figure out)\b'],
})

_gp('thriller', 'Thriller', 'Tension through danger', ['time pressure', 'high stakes', 'power shifts'], {
    'time_pressure': [r'\b(deadline|timer|countdown|clock|hours|minutes)\b', r'\b(hurry|rush|quickly|fast|immediately)\b'],
    'stakes': [r'\b(life|death|lives|die|kill|survive|save)\b', r'\b(hostage|bomb|attack|threat|danger)\b'],
    'tension': [r'\b(chase|pursue|hunt|flee|escape|run)\b', r'\b(heart|pulse|breath|sweat|adrenaline)\b'],
})

_gp('horror', 'Horror', 'Dread and confrontation', ['vulnerability', 'dread building', 'rules'], {
    'dread': [r'\b(dread|terror|horror|fear|panic)\b', r'\b(creeping|lurking|watching|stalking)\b'],
    'vulnerability': [r'\b(alone|isolated|trapped|helpless)\b', r'\b(dark|darkness|shadow|shadows|night)\b'],
    'threat': [r'\b(creature|monster|entity)\b', r'\b(scream|blood|death|die|kill)\b'],
})

_gp('adventure', 'Adventure', 'Excitement through challenges', ['journey', 'obstacles', 'resources'], {
    'journey': [r'\b(journey|quest|expedition|voyage|trek)\b', r'\b(destination|goal|objective|mission)\b'],
    'obstacles': [r'\b(obstacle|challenge|barrier|block)\b', r'\b(dangerous|treacherous|difficult|deadly)\b'],
    'resources': [r'\b(supplies|provisions|equipment|gear)\b', r'\b(running low|depleted|exhausted|scarce)\b'],
})

_gp('humor', 'Humor', 'Entertainment through comedy', ['incongruity', 'subversion', 'timing'], {
    'incongruity': [r'\b(absurd|ridiculous|ludicrous)\b', r'\b(unexpected|surprising|ironic)\b'],
    'subversion': [r'\b(actually|instead|but|however|turns out)\b'],
    'reaction': [r'\b(laugh|laughed|chuckle|giggle)\b', r'\b(smile|grin|smirk|amused|funny)\b'],
})

_gp('relationship', 'Relationship', 'Investment in connections', ['obstacle', 'connection', 'resolution'], {
    'connection': [r'\b(love|loved|heart|soul|feeling)\b', r'\b(together|between|us|we|our)\b'],
    'obstacle': [r'\b(forbidden|impossible|secret|hide)\b'],
    'progression': [r'\b(closer|deeper|growing|falling)\b', r'\b(finally|at last|admitted|confessed)\b'],
})

_gp('drama', 'Drama', 'Internal transformation', ['value under pressure', 'difficult choice', 'transformation'], {
    'internal_conflict': [r'\b(torn|conflicted|struggled|wrestling)\b', r'\b(should|must|have to|need to)\b'],
    'values': [r'\b(believe|principle|value|honor|integrity)\b', r'\b(sacrifice|cost|price|give up)\b'],
    'transformation': [r'\b(change|changed|different|become|became)\b'],
})

_gp('idea', 'Idea', 'Intellectual fascination', ['central concept', 'implication exploration'], {
    'concepts': [r'\b(what if|imagine if|suppose|hypothesis)\b', r'\b(theory|concept|principle|paradigm)\b'],
    'exploration': [r'\b(therefore|thus|hence|consequently)\b'],
    'questioning': [r'\b(paradox|contradiction|dilemma|puzzle)\b'],
})

_gp('issue', 'Issue', 'Exploration of complex questions', ['multiple perspectives', 'complexity'], {
    'perspectives': [r'\b(side|perspective|view|viewpoint)\b', r'\b(but|however|although|yet|still)\b'],
    'complexity': [r'\b(complicated|complex|nuanced|layered)\b'],
    'stakes': [r'\b(rights|justice|freedom|equality)\b', r'\b(society|community|people|everyone)\b'],
})

_gp('ensemble', 'Ensemble', 'Group dynamics', ['diverse skills', 'group challenges'], {
    'group': [r'\b(team|group|crew|squad|party)\b', r'\b(together|everyone|each|we)\b'],
    'diversity': [r'\b(different|unique|special|each)\b', r'\b(skill|ability|talent|expertise)\b'],
    'cooperation': [r'\b(work together|combine|coordinate)\b', r'\b(trust|rely|depend|count on)\b'],
})


def count_matches(text, patterns):
    matches = []
    for pattern in patterns:
        found = pattern.findall(text)
        if found:
            matches.extend(found[:3])
    unique = list(dict.fromkeys(m.lower() if isinstance(m, str) else m[0].lower() for m in matches))
    return {'count': len(unique), 'samples': unique[:5]}


def analyze_for_genre(text, genre_name):
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
    present = [c.replace('_', ' ') for c, r in breakdown.items() if r['count'] > 0]
    missing = [c.replace('_', ' ') for c, r in breakdown.items() if r['count'] == 0]
    issues, recs = [], []
    if score < 20:
        issues.append('Very few {} elements detected'.format(genre['display']))
        recs.append('Consider adding ' + ', '.join(genre['required']))
    if missing:
        issues.append('Missing categories: ' + ', '.join(missing))
    return {
        'genre': genre['display'], 'score': score, 'total_matches': total,
        'breakdown': breakdown, 'present': present, 'missing': missing,
        'issues': issues, 'recommendations': recs,
    }


def analyze_multi_genre(text):
    scores = {}
    best_name, best_score = None, 0
    for name in GENRE_PATTERNS:
        a = analyze_for_genre(text, name)
        scores[GENRE_PATTERNS[name]['display']] = a['score']
        if a['score'] > best_score:
            best_score = a['score']
            best_name = name
    return {
        'word_count': len([w for w in text.split() if w]),
        'likely_primary': GENRE_PATTERNS[best_name]['display'] if best_name else 'Unknown',
        'scores': scores,
        'detailed': analyze_for_genre(text, best_name) if best_name else None,
    }


def format_report(a):
    r = '# {} Genre Analysis'.format(a['genre']) + chr(10)*2
    r += '## Match Score: {}/100'.format(a['score']) + chr(10)*2
    r += '## Category Breakdown' + chr(10)
    for cat, res in a['breakdown'].items():
        st = '+' if res['count'] > 0 else '-'
        samples = ': ' + ', '.join(res['samples']) if res['samples'] else ''
        r += '  {} {} ({}){}' .format(st, cat.replace('_', ' '), res['count'], samples) + chr(10)
    if a['present']:
        r += chr(10) + '## Present: ' + ', '.join(a['present']) + chr(10)
    if a['missing']:
        r += chr(10) + '## Missing: ' + ', '.join(a['missing']) + chr(10)
    if a['issues']:
        r += chr(10) + '## Issues' + chr(10)
        for i in a['issues']: r += '  - ' + i + chr(10)
    if a['recommendations']:
        r += chr(10) + '## Recommendations' + chr(10)
        for rec in a['recommendations']: r += '  - ' + rec + chr(10)
    return r


def format_multi_report(a):
    r = '# Multi-Genre Analysis' + chr(10)*2
    r += 'Word count: {}'.format(a['word_count']) + chr(10)
    r += 'Likely primary: **{}**'.format(a['likely_primary']) + chr(10)*2
    r += '## Genre Scores' + chr(10)
    for genre, score in sorted(a['scores'].items(), key=lambda x: x[1], reverse=True):
        bar = '=' * (score // 5)
        r += '  {} {} {}'.format(genre.ljust(15), bar, score) + chr(10)
    if a['detailed']:
        r += chr(10) + '## Primary Genre Details' + chr(10)*2
        r += format_report(a['detailed'])
    return r


def main():
    args = sys.argv[1:]
    json_out = '--json' in args
    text = ''
    if '--text' in args:
        idx = args.index('--text')
        text = args[idx+1] if idx+1 < len(args) else ''
    else:
        for i, a in enumerate(args):
            if not a.startswith('--') and a not in list(GENRE_PATTERNS.keys()):
                try:
                    with open(a, 'r', encoding='utf-8') as fh: text = fh.read()
                    break
                except Exception:
                    pass
    if not text.strip():
        print('Error: No text provided. Use --text or provide a file.', file=sys.stderr)
        sys.exit(1)
    if '--analyze' in args:
        a = analyze_multi_genre(text)
        print(json.dumps(a, indent=2) if json_out else format_multi_report(a))
        sys.exit(0)
    if '--genre' in args:
        gi = args.index('--genre')
        gn = args[gi+1].lower() if gi+1 < len(args) else None
        if gn not in GENRE_PATTERNS:
            print('Error: Unknown genre. Available: ' + ', '.join(GENRE_PATTERNS.keys()), file=sys.stderr)
            sys.exit(1)
        a = analyze_for_genre(text, gn)
        print(json.dumps(a, indent=2, default=str) if json_out else format_report(a))
        sys.exit(0)
    print('Error: Specify --genre <genre> or --analyze', file=sys.stderr)
    sys.exit(1)


if __name__ == '__main__':
    main()
