#!/usr/bin/env python3
"""
rhythm.py - Analyze prose rhythm and variety

Reports:
- Sentence length distribution
- Paragraph length variation
- Opening word variety
- Rhythm score (variety metric)

Usage:
  python rhythm.py <file>
  python rhythm.py --text "Short. Then longer. Short again."
"""

import sys
import re
import math


def split_into_paragraphs(text):
    return [p.strip() for p in re.split(r'\n\s*\n', text) if p.strip()]


def split_into_sentences(text):
    clean = text.replace('Mr.', 'Mr').replace('Mrs.', 'Mrs').replace('Dr.', 'Dr').replace('Ms.', 'Ms')
    clean = clean.replace('...', chr(8230))
    return [s.strip() for s in re.split(r'[.!?]+', clean) if s.strip()]


def count_words(text):
    return len([w for w in text.split() if w])


def get_opening_word(sentence):
    words = sentence.strip().split()
    if not words:
        return ''
    return re.sub(r'[^a-z]', '', words[0].lower())


def calculate_std_dev(values, mean):
    if len(values) < 2:
        return 0.0
    squared_diffs = [(v - mean) ** 2 for v in values]
    return math.sqrt(sum(squared_diffs) / len(values))


def analyze_sentences(sentences):
    lengths = [count_words(s) for s in sentences]
    short = sum(1 for l in lengths if l < 10)
    medium = sum(1 for l in lengths if 10 <= l <= 20)
    long_ = sum(1 for l in lengths if 21 <= l <= 35)
    very_long = sum(1 for l in lengths if l > 35)
    avg = sum(lengths) / len(lengths) if lengths else 0
    std = calculate_std_dev(lengths, avg)
    variety = min(100, (std / 10) * 100)
    return {
        'total': len(sentences), 'lengths': lengths,
        'short': short, 'medium': medium, 'long': long_, 'very_long': very_long,
        'avg_length': avg, 'std_dev': std, 'variety_score': variety,
    }


def analyze_paragraphs(paragraphs):
    lengths = [len(split_into_sentences(p)) for p in paragraphs]
    short = sum(1 for l in lengths if l <= 2)
    medium = sum(1 for l in lengths if 3 <= l <= 5)
    long_ = sum(1 for l in lengths if l >= 6)
    avg = sum(lengths) / len(lengths) if lengths else 0
    total = len(paragraphs)
    variety = 0
    if total > 0:
        cats = sum(1 for x in [short > 0, medium > 0, long_ > 0] if x)
        variety = (cats / 3) * 100
    return {
        'total': total, 'lengths': lengths,
        'short': short, 'medium': medium, 'long': long_,
        'avg_length': avg, 'variety_score': variety,
    }


def analyze_openings(sentences):
    openings = {}
    for sentence in sentences:
        opening = get_opening_word(sentence)
        if opening:
            openings[opening] = openings.get(opening, 0) + 1
    sorted_openings = sorted(openings.items(), key=lambda x: x[1], reverse=True)
    top = sorted_openings[:10]
    unique_ratio = len(openings) / len(sentences) if sentences else 0
    threshold = max(4, len(sentences) * 0.15)
    warnings = []
    for word, count in sorted_openings:
        if count >= threshold:
            warnings.append('"{}" starts {} sentences ({}%)'.format(word, count, int(count / len(sentences) * 100)))
    return {
        'openings': openings, 'unique_ratio': unique_ratio,
        'top_openings': top, 'warnings': warnings,
    }


def calculate_rhythm_score(sentences, paragraphs, openings):
    return sentences['variety_score'] * 0.4 + paragraphs['variety_score'] * 0.3 + openings['unique_ratio'] * 100 * 0.3


def get_verdict(sentences, paragraphs, openings):
    issues = []
    if sentences['variety_score'] < 30: issues.append('Low sentence length variety')
    if sentences['short'] == 0 and sentences['total'] > 5: issues.append('No short punchy sentences')
    if sentences['long'] == 0 and sentences['very_long'] == 0 and sentences['total'] > 5: issues.append('No long flowing sentences')
    if paragraphs['variety_score'] < 50: issues.append('Limited paragraph length variety')
    if openings['warnings']: issues.append('Repetitive sentence openings')
    if not issues: return 'Good rhythm variety'
    elif len(issues) <= 2: return 'Some rhythm issues: ' + '; '.join(issues)
    else: return 'Monotonous prose: ' + '; '.join(issues)


def analyze_text(text):
    paragraphs = split_into_paragraphs(text)
    sentences = split_into_sentences(text)
    s = analyze_sentences(sentences)
    p = analyze_paragraphs(paragraphs)
    o = analyze_openings(sentences)
    score = calculate_rhythm_score(s, p, o)
    verdict = get_verdict(s, p, o)
    return {'sentences': s, 'paragraphs': p, 'openings': o, 'rhythm_score': score, 'verdict': verdict}


def format_histogram(lengths, bucket_size=5):
    buckets = {}
    for l in lengths:
        b = (l // bucket_size) * bucket_size
        buckets[b] = buckets.get(b, 0) + 1
    sorted_b = sorted(buckets.items())
    if not sorted_b: return ''
    mx = max(c for _, c in sorted_b)
    scale = min(30, mx)
    h = ''
    for bk, cnt in sorted_b:
        bl = round((cnt / mx) * scale)
        h += '    {}-{}: {} ({})\n'.format(str(bk).rjust(2), str(bk + bucket_size - 1).ljust(2), '=' * bl, cnt)
    return h


def pct(n, total):
    return int(n / total * 100) if total > 0 else 0


def format_report(a):
    s, p, o = a['sentences'], a['paragraphs'], a['openings']
    sc, v = a['rhythm_score'], a['verdict']
    r = '' + chr(10) + 'RHYTHM ANALYSIS' + chr(10) + '===============' + chr(10)
    r += chr(10) + 'OVERALL RHYTHM SCORE: {:.0f}/100'.format(sc)
    r += chr(10) + v
    r += chr(10)*2 + 'SENTENCE LENGTH'
    r += chr(10) + '  Total sentences: ' + str(s['total'])
    r += chr(10) + '  Average length: {:.1f} words'.format(s['avg_length'])
    r += chr(10) + '  Standard deviation: {:.1f}'.format(s['std_dev'])
    r += chr(10) + '  Variety score: {:.0f}/100'.format(s['variety_score'])
    r += chr(10)*2 + '  Distribution:'
    r += chr(10) + '    Short (<10):    {} ({}%)'.format(s['short'], pct(s['short'], s['total']))
    r += chr(10) + '    Medium (10-20): {} ({}%)'.format(s['medium'], pct(s['medium'], s['total']))
    r += chr(10) + '    Long (21-35):   {} ({}%)'.format(s['long'], pct(s['long'], s['total']))
    r += chr(10) + '    Very long (>35):  {} ({}%)'.format(s['very_long'], pct(s['very_long'], s['total']))
    r += chr(10)*2 + '  Histogram (words per sentence):' + chr(10)
    r += format_histogram(s['lengths'], 5)
    r += chr(10) + 'PARAGRAPH LENGTH'
    r += chr(10) + '  Total: ' + str(p['total'])
    r += chr(10) + '  Average: {:.1f} sentences'.format(p['avg_length'])
    r += chr(10) + '  Variety: {:.0f}/100'.format(p['variety_score'])
    r += chr(10)*2 + '  Distribution:'
    r += chr(10) + '    Short (1-2):  {} ({}%)'.format(p['short'], pct(p['short'], p['total']))
    r += chr(10) + '    Medium (3-5): {} ({}%)'.format(p['medium'], pct(p['medium'], p['total']))
    r += chr(10) + '    Long (6+):    {} ({}%)'.format(p['long'], pct(p['long'], p['total']))
    r += chr(10)*2 + 'SENTENCE OPENINGS'
    u = int(o['unique_ratio']*100)
    r += chr(10) + '  Unique ratio: {}% ({} unique / {} total)'.format(u, len(o['openings']), s['total'])
    r += chr(10)*2 + '  Most common:'
    for w, c in o['top_openings']:
        r += chr(10) + '    "{}": {} ({}%)'.format(w, c, pct(c, s['total']))
    if o['warnings']:
        r += chr(10)*2 + '  WARNINGS:'
        for w in o['warnings']: r += chr(10) + '    ! ' + w
    r += chr(10)*2 + 'RECOMMENDATIONS:'
    r += chr(10) + '  - Vary sentence lengths consciously'
    r += chr(10) + '  - Short sentences punch, long sentences flow'
    r += chr(10) + '  - Use single-sentence paragraphs for emphasis'
    r += chr(10) + '  - Vary sentence openings'
    r += chr(10) + '  - Mix simple, compound, and complex sentences' + chr(10)
    return r


def main():
    args = sys.argv[1:]
    if '--text' in args:
        idx = args.index('--text')
        text = ' '.join(args[idx + 1:])
    elif args:
        try:
            with open(args[0], 'r', encoding='utf-8') as fh:
                text = fh.read()
        except Exception as e:
            print('Error reading file: ' + args[0], file=sys.stderr)
            print(e, file=sys.stderr)
            sys.exit(1)
    else:
        print('Usage:')
        print('  python rhythm.py <file>')
        print('  python rhythm.py --text "Short. Then longer."')
        sys.exit(0)
    print(format_report(analyze_text(text)))


if __name__ == '__main__':
    main()
