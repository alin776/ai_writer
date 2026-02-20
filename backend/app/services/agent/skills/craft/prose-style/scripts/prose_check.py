#!/usr/bin/env python3
"""
prose_check.py - Analyze prose for common issues

Detects:
- Passive voice percentage
- Weak verb frequency
- Adverb density
- Filter word usage
- Adjective stacking

Usage:
  python prose_check.py <file>
  python prose_check.py --text "Text to analyze..."
"""

import sys
import re


PASSIVE_PATTERNS = [
    re.compile(r'\b(is|are|was|were|be|been|being)\s+(\w+ed|written|done|made|taken|given|seen|shown|known|found)\b', re.IGNORECASE),
    re.compile(r'\b(has|have|had)\s+been\s+\w+', re.IGNORECASE),
    re.compile(r'\bget(s|ting)?\s+\w+ed\b', re.IGNORECASE),
]

WEAK_VERBS = [
    'is',
    'are',
    'was',
    'were',
    'be',
    'been',
    'being',
    'has',
    'have',
    'had',
    'do',
    'does',
    'did',
    'get',
    'gets',
    'got',
    'gotten',
    'make',
    'makes',
    'made',
    'seem',
    'seems',
    'seemed',
    'appear',
    'appears',
    'appeared',
    'become',
    'becomes',
    'became',
]

FILTER_WORDS = [
    'saw',
    'see',
    'sees',
    'seen',
    'heard',
    'hear',
    'hears',
    'felt',
    'feel',
    'feels',
    'noticed',
    'notice',
    'notices',
    'realized',
    'realize',
    'realizes',
    'thought',
    'think',
    'thinks',
    'knew',
    'know',
    'knows',
    'watched',
    'watch',
    'watches',
    'wondered',
    'wonder',
    'wonders',
    'decided',
    'decide',
    'decides',
]

ADVERB_PATTERN = re.compile(r'\b\w+ly\b', re.IGNORECASE)
DIALOGUE_ADVERBS = [
    'quickly',
    'slowly',
    'softly',
    'loudly',
    'quietly',
    'angrily',
    'sadly',
    'happily',
    'nervously',
    'anxiously',
    'suddenly',
    'immediately',
    'finally',
    'really',
    'very',
    'actually',
    'basically',
    'literally',
    'definitely',
    'certainly',
]


def split_into_sentences(text):
    return [s.strip() for s in re.split(r'[.!?]+', text) if s.strip()]


def count_words(text):
    return len([w for w in text.split() if w])


def find_passive_voice(text):
    examples = []
    count = 0
    sentences = split_into_sentences(text)
    for sentence in sentences:
        for pattern in PASSIVE_PATTERNS:
            matches = pattern.findall(sentence)
            if matches:
                count += len(matches)
                if len(examples) < 5:
                    preview = sentence.strip()[:80] + ('...' if len(sentence) > 80 else '')
                    examples.append(preview)
    return count, list(dict.fromkeys(examples))


def count_weak_verbs(text):
    words = text.lower().split()
    return sum(1 for w in words if re.sub(r'[^a-z]', '', w) in WEAK_VERBS)


def find_adverbs(text):
    matches = ADVERB_PATTERN.findall(text)
    examples = [m for m in matches if m.lower() in DIALOGUE_ADVERBS][:10]
    return len(matches), examples


def find_filter_words(text):
    words = text.lower().split()
    found = [w for w in words if re.sub(r'[^a-z]', '', w) in FILTER_WORDS]
    return len(found), list(dict.fromkeys(found))[:10]


def find_adjective_stacks(text):
    pattern = re.compile(
        r'\b((\w+,?\s+){2,})(man|woman|person|thing|place|room|house|building|sky|day|night|face|eyes|voice|hand|way|time|door|wall|street|car|sun|moon|tree|water)\b',
        re.IGNORECASE,
    )
    matches = pattern.findall(text)
    comma_pattern = re.compile(r'\b\w+,\s+\w+,\s+\w+\s+(and\s+)?\w+\b', re.IGNORECASE)
    comma_matches = comma_pattern.findall(text)
    examples = [m[0] if isinstance(m, tuple) else m for m in matches][:5]
    comma_examples = [m if isinstance(m, str) else m[0] for m in comma_matches][:5]
    all_examples = (examples + comma_examples)[:5]
    return len(matches) + len(comma_matches), all_examples


def analyze_text(text):
    sentences = split_into_sentences(text)
    total_words = count_words(text)
    passive_count, passive_examples = find_passive_voice(text)
    weak_verb_count = count_weak_verbs(text)
    adverb_count, adverb_examples = find_adverbs(text)
    filter_count, filter_examples = find_filter_words(text)
    stack_count, stack_examples = find_adjective_stacks(text)
    return {
        'total_sentences': len(sentences),
        'total_words': total_words,
        'passive_count': passive_count,
        'passive_percentage': (passive_count / len(sentences) * 100) if sentences else 0,
        'passive_examples': passive_examples,
        'weak_verb_count': weak_verb_count,
        'weak_verb_percentage': (weak_verb_count / total_words * 100) if total_words else 0,
        'adverb_count': adverb_count,
        'adverb_density': (adverb_count / total_words * 100) if total_words else 0,
        'adverb_examples': adverb_examples,
        'filter_word_count': filter_count,
        'filter_examples': filter_examples,
        'adjective_stack_count': stack_count,
        'stack_examples': stack_examples,
    }


def get_verdict(result):
    issues = []
    if result['passive_percentage'] > 20:
        issues.append('High passive voice usage (>20%)')
    if result['weak_verb_percentage'] > 15:
        issues.append('High weak verb frequency (>15%)')
    if result['adverb_density'] > 4:
        issues.append('High adverb density (>4%)')
    if result['filter_word_count'] > result['total_sentences'] * 0.1:
        issues.append('Frequent filter words')
    if result['adjective_stack_count'] > 3:
        issues.append('Multiple adjective stacks detected')
    if not issues:
        return 'Prose patterns look healthy'
    elif len(issues) <= 2:
        return 'Minor issues: ' + '; '.join(issues)
    else:
        return 'Multiple issues detected: ' + '; '.join(issues)


def format_report(result):
    r = ''
    r += '\nPROSE ANALYSIS'
    r += '\n==============' + '\n'
    r += '\nOverview:'
    r += '\n  Sentences: ' + str(result['total_sentences'])
    r += '\n  Words: ' + str(result['total_words'])
    r += '\n\nPASSIVE VOICE'
    r += '\n  Count: ' + str(result['passive_count'])
    r += '\n  Percentage: {:.1f}% of sentences'.format(result['passive_percentage'])
    r += '\n  Target: <20%'
    if result['passive_examples']:
        r += '\n  Examples:'
        for e in result['passive_examples']:
            r += '\n    - "' + e + '"'
    r += '\n\nWEAK VERBS (is/was/had/got/made/seemed)'
    r += '\n  Count: ' + str(result['weak_verb_count'])
    r += '\n  Percentage: {:.1f}% of words'.format(result['weak_verb_percentage'])
    r += '\n  Target: <15%'
    r += '\n\nADVERBS'
    r += '\n  Count: ' + str(result['adverb_count'])
    r += '\n  Density: {:.1f}% of words'.format(result['adverb_density'])
    r += '\n  Target: <4%'
    if result['adverb_examples']:
        r += '\n  Flagged: ' + ', '.join(result['adverb_examples'])
    r += '\n\nFILTER WORDS (saw/felt/noticed/realized/etc.)'
    r += '\n  Count: ' + str(result['filter_word_count'])
    if result['filter_examples']:
        r += '\n  Found: ' + ', '.join(result['filter_examples'])
    r += '\n\nADJECTIVE STACKING'
    r += '\n  Count: ' + str(result['adjective_stack_count'])
    if result['stack_examples']:
        r += '\n  Examples:'
        for e in result['stack_examples']:
            r += '\n    - "' + str(e) + '"'
    r += '\n\nVERDICT'
    r += '\n  ' + get_verdict(result)
    r += '\n\nRECOMMENDATIONS:'
    r += '\n  - Passive voice: Use intentionally for emphasis or unknown agents'
    r += '\n  - Weak verbs: Replace with specific, active verbs where possible'
    r += '\n  - Adverbs: Cut or replace with stronger verbs'
    r += '\n  - Filter words: Remove to bring reader closer to experience'
    r += '\n  - Adjective stacks: Choose one precise adjective over many vague ones'
    r += '\n'
    return r


def main():
    args = sys.argv[1:]
    if '--text' in args:
        text_index = args.index('--text')
        text = ' '.join(args[text_index + 1:])
    elif args:
        filename = args[0]
        try:
            with open(filename, 'r', encoding='utf-8') as f:
                text = f.read()
        except Exception as e:
            print('Error reading file: ' + filename, file=sys.stderr)
            print(e, file=sys.stderr)
            sys.exit(1)
    else:
        print('Usage:')
        print('  python prose_check.py <file>')
        print('  python prose_check.py --text "Text to analyze..."')
        print('Analyzes prose for:')
        print('  - Passive voice percentage')
        print('  - Weak verb frequency')
        print('  - Adverb density')
        print('  - Filter word usage')
        print('  - Adjective stacking')
        sys.exit(0)
    result = analyze_text(text)
    print(format_report(result))


if __name__ == '__main__':
    main()
