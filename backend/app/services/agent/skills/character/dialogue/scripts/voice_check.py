#!/usr/bin/env python3
"""
voice_check.py - Dialogue Voice Distinctiveness Analyzer

Analyzes dialogue to measure how distinct each speaker's voice is.
Compares vocabulary, sentence patterns, and speech characteristics.

Usage:
  python voice_check.py <file>
  python voice_check.py --text "dialogue here"
"""

import sys
import re
import json


STOP_WORDS = {
    "the", "a", "an", "and", "or", "but", "in", "on", "at", "to", "for",
    "of", "with", "by", "from", "as", "is", "was", "are", "were", "been",
    "be", "have", "has", "had", "do", "does", "did", "will", "would",
    "could", "should", "may", "might", "must", "shall", "can", "need",
    "it", "its", "this", "that", "these", "those", "i", "you", "he",
    "she", "we", "they", "me", "him", "her", "us", "them", "my", "your",
    "his", "our", "their", "mine", "yours", "hers", "ours", "theirs",
    "what", "which", "who", "whom", "whose", "where", "when", "why", "how",
    "all", "each", "every", "both", "few", "more", "most", "other", "some",
    "such", "no", "nor", "not", "only", "own", "same", "so", "than", "too",
    "very", "just", "also", "now", "here", "there", "then", "once",
}


def extract_dialogue(text):
    speakers = {}
    patterns = [
        re.compile(
            r'"([^"]+)"\s*(?:said|asked|replied|answered|whispered|shouted|muttered|called|cried|exclaimed|declared|announced|continued|added|interrupted|began|finished|concluded)\s+([A-Z][a-z]+)',
            re.IGNORECASE,
        ),
        re.compile(
            r'"([^"]+)"\s+([A-Z][a-z]+)\s+(?:said|asked|replied|answered|whispered|shouted|muttered|called|cried|exclaimed|declared|announced|continued|added|interrupted|began|finished|concluded)',
            re.IGNORECASE,
        ),
        re.compile(
            r'([A-Z][a-z]+)\s+(?:said|asked|replied|answered|whispered|shouted|muttered|called|cried|exclaimed|declared|announced|continued|added|interrupted|began|finished|concluded),?\s+"([^"]+)"',
            re.IGNORECASE,
        ),
    ]
    for pattern in patterns:
        for match in pattern.finditer(text):
            if match.group(0).startswith('"'):
                dialogue = match.group(1)
                speaker = match.group(2)
            else:
                speaker = match.group(1)
                dialogue = match.group(2)
            speaker = speaker.strip()
            dialogue = dialogue.strip()
            if speaker not in speakers:
                speakers[speaker] = []
            speakers[speaker].append(dialogue)
    if not speakers:
        colon_pattern = re.compile(r'^([A-Z][A-Za-z]+):\s*"?([^"\n]+)"?', re.MULTILINE)
        for match in colon_pattern.finditer(text):
            speaker = match.group(1).strip()
            dialogue = match.group(2).strip()
            if speaker not in speakers:
                speakers[speaker] = []
            speakers[speaker].append(dialogue)
    return speakers


def analyze_vocabulary(lines):
    word_counts = {}
    unique = set()
    for line in lines:
        words = re.sub(r"[^\w\s']", "", line.lower()).split()
        for word in words:
            if len(word) > 1 and word not in STOP_WORDS:
                unique.add(word)
                word_counts[word] = word_counts.get(word, 0) + 1
    sorted_words = sorted(word_counts.items(), key=lambda x: x[1], reverse=True)
    return unique, sorted_words[:10]


def count_contractions(lines):
    total = 0
    contractions = 0
    contraction_pattern = re.compile(r"\b\w+'\w+\b")
    for line in lines:
        words = line.split()
        total += len(words)
        matches = contraction_pattern.findall(line)
        contractions += len(matches)
    return contractions / total if total > 0 else 0


def count_questions(lines):
    questions = sum(1 for l in lines if l.strip().endswith("?"))
    return questions / len(lines) if lines else 0


def count_exclamations(lines):
    exclamations = sum(1 for l in lines if l.strip().endswith("!"))
    return exclamations / len(lines) if lines else 0


def count_fragments(lines):
    verb_pattern = re.compile(
        r'\b(is|are|was|were|am|be|been|being|have|has|had|do|does|did|will|would|could|should|can|may|might|must|shall|go|goes|went|gone|going|come|comes|came|coming|get|gets|got|getting|make|makes|made|making|know|knows|knew|knowing|think|thinks|thought|thinking|take|takes|took|taking|see|sees|saw|seeing|want|wants|wanted|wanting|say|says|said|saying|tell|tells|told|telling|ask|asks|asked|asking|need|needs|needed|needing|feel|feels|felt|feeling|try|tries|tried|trying|leave|leaves|left|leaving|call|calls|called|calling|keep|keeps|kept|keeping|let|lets|letting|begin|begins|began|begun|beginning|seem|seems|seemed|seeming|help|helps|helped|helping|show|shows|showed|showing|hear|hears|heard|hearing|play|plays|played|playing|run|runs|ran|running|move|moves|moved|moving|live|lives|lived|living|believe|believes|believed|believing|hold|holds|held|holding|bring|brings|brought|bringing|write|writes|wrote|writing|stand|stands|stood|standing|lose|loses|lost|losing|pay|pays|paid|paying|meet|meets|met|meeting|include|includes|included|including|continue|continues|continued|continuing|set|sets|setting|learn|learns|learned|learning|change|changes|changed|changing|lead|leads|led|leading|understand|understands|understood|understanding|watch|watches|watched|watching|follow|follows|followed|following|stop|stops|stopped|stopping|create|creates|created|creating|speak|speaks|spoke|speaking|read|reads|reading|allow|allows|allowed|allowing|add|adds|added|adding|spend|spends|spent|spending|grow|grows|grew|growing|open|opens|opened|opening|walk|walks|walked|walking|win|wins|won|winning|offer|offers|offered|offering|remember|remembers|remembered|remembering|love|loves|loved|loving|consider|considers|considered|considering|appear|appears|appeared|appearing|buy|buys|bought|buying|wait|waits|waited|waiting|serve|serves|served|serving|die|dies|died|dying|send|sends|sent|sending|expect|expects|expected|expecting|build|builds|built|building|stay|stays|stayed|staying|fall|falls|fell|fallen|falling|cut|cuts|cutting|reach|reaches|reached|reaching|kill|kills|killed|killing|remain|remains|remained|remaining)\b',
        re.IGNORECASE,
    )
    fragments = 0
    for line in lines:
        word_count = len(line.split())
        if word_count <= 3 or not verb_pattern.search(line):
            fragments += 1
    return fragments / len(lines) if lines else 0


def calculate_sentence_length(lines):
    total_words = 0
    total_sentences = 0
    for line in lines:
        words = [w for w in line.split() if w]
        total_words += len(words)
        sentences = len(re.findall(r'[.!?]+', line))
        if sentences == 0:
            sentences = 1
        total_sentences += sentences
    return total_words / total_sentences if total_sentences > 0 else 0


def analyze_speaker(name, lines):
    unique_words, top_words = analyze_vocabulary(lines)
    word_count = sum(len(l.split()) for l in lines)
    return {
        'name': name,
        'line_count': len(lines),
        'word_count': word_count,
        'avg_words_per_line': word_count / len(lines) if lines else 0,
        'avg_sentence_length': calculate_sentence_length(lines),
        'vocabulary_size': len(unique_words),
        'contraction_rate': count_contractions(lines),
        'question_rate': count_questions(lines),
        'exclamation_rate': count_exclamations(lines),
        'fragment_rate': count_fragments(lines),
        'unique_words': unique_words,
        'top_words': top_words,
    }


def calculate_variance(values):
    if len(values) < 2:
        return 0
    mean = sum(values) / len(values)
    squared_diffs = [(v - mean) ** 2 for v in values]
    return sum(squared_diffs) / len(squared_diffs)


def calculate_overlap(speaker_stats):
    all_words_list = [stats['unique_words'] for stats in speaker_stats.values()]
    if len(all_words_list) < 2:
        return 0
    total_overlap = 0
    pairs = 0
    for i in range(len(all_words_list)):
        for j in range(i + 1, len(all_words_list)):
            intersection = all_words_list[i] & all_words_list[j]
            union = all_words_list[i] | all_words_list[j]
            if union:
                total_overlap += len(intersection) / len(union)
            pairs += 1
    return total_overlap / pairs if pairs > 0 else 0


def analyze_voices(speaker_data):
    speaker_stats = {}
    for name, lines in speaker_data.items():
        speaker_stats[name] = analyze_speaker(name, lines)
    patterns = []
    speaker_names = list(speaker_stats.keys())
    if len(speaker_names) >= 2:
        metrics = [
            ('avg_words_per_line', 'Words per line'),
            ('avg_sentence_length', 'Sentence length'),
            ('contraction_rate', 'Contraction usage'),
            ('question_rate', 'Question frequency'),
            ('exclamation_rate', 'Exclamation frequency'),
            ('fragment_rate', 'Fragment frequency'),
        ]
        for metric_key, metric_label in metrics:
            values = {}
            nums = []
            for name in speaker_names:
                val = speaker_stats[name][metric_key]
                values[name] = val
                nums.append(val)
            variance = calculate_variance(nums)
            patterns.append({
                'metric': metric_label,
                'values': values,
                'variance': variance,
                'distinct': variance > 0.01,
            })
    vocabulary_overlap = calculate_overlap(speaker_stats)
    distinct_patterns = sum(1 for p in patterns if p['distinct'])
    pattern_score = (distinct_patterns / max(len(patterns), 1)) * 50
    overlap_score = (1 - vocabulary_overlap) * 50
    overall_distinctiveness = round(pattern_score + overlap_score)
    issues = []
    recommendations = []
    if vocabulary_overlap > 0.6:
        issues.append("High vocabulary overlap between speakers")
        recommendations.append("Give each character domain-specific vocabulary or verbal tics")
    if sum(1 for p in patterns if not p['distinct']) > len(patterns) / 2:
        issues.append("Speech patterns too similar across speakers")
        recommendations.append("Vary sentence length, directness, or formality between characters")
    low_contraction = [s for s in speaker_stats.values() if s['contraction_rate'] < 0.05]
    if len(low_contraction) == len(speaker_stats) and len(speaker_stats) > 0:
        issues.append("No speakers use contractions - may feel formal/wooden")
        recommendations.append("Add contractions for more natural speech patterns")
    all_questions = [s for s in speaker_stats.values() if s['question_rate'] > 0.5]
    if len(all_questions) > len(speaker_stats) / 2:
        issues.append("Most speakers ask many questions - may indicate exposition dump pattern")
    if len(speaker_stats) < 2:
        issues.append("Need at least two speakers to compare voice distinctiveness")
    return {
        'speakers': speaker_stats,
        'overall_distinctiveness': overall_distinctiveness,
        'vocabulary_overlap': vocabulary_overlap,
        'patterns_comparison': patterns,
        'issues': issues,
        'recommendations': recommendations,
    }


def format_report(analysis):
    lines = []
    lines.append("# Voice Distinctiveness Analysis\n")
    lines.append(f"Overall distinctiveness: {analysis['overall_distinctiveness']}/100")
    lines.append(f"Vocabulary overlap: {analysis['vocabulary_overlap'] * 100:.1f}%\n")
    lines.append("## Speaker Profiles\n")
    for name, stats in analysis['speakers'].items():
        lines.append(f"### {name}")
        lines.append(f"  Lines: {stats['line_count']} | Words: {stats['word_count']}")
        lines.append(f"  Avg words/line: {stats['avg_words_per_line']:.1f}")
        lines.append(f"  Contractions: {stats['contraction_rate'] * 100:.1f}%")
        lines.append(f"  Questions: {stats['question_rate'] * 100:.1f}%")
        lines.append(f"  Fragments: {stats['fragment_rate'] * 100:.1f}%")
        if stats['top_words']:
            top = ", ".join(w for w, _ in stats['top_words'][:5])
            lines.append(f"  Top words: {top}")
        lines.append("")
    if analysis['patterns_comparison']:
        lines.append("## Pattern Comparison\n")
        for pattern in analysis['patterns_comparison']:
            status = "+" if pattern['distinct'] else "-"
            values = ", ".join(
                f"{name}: {val:.2f}" for name, val in pattern['values'].items()
            )
            lines.append(f"  {status} {pattern['metric']}: {values}")
        lines.append("")
    if analysis['issues']:
        lines.append("## Issues\n")
        for issue in analysis['issues']:
            lines.append(f"  - {issue}")
        lines.append("")
    if analysis['recommendations']:
        lines.append("## Recommendations\n")
        for rec in analysis['recommendations']:
            lines.append(f"  - {rec}")
        lines.append("")
    return "\n".join(lines)


def main():
    args = sys.argv[1:]
    if '--help' in args or '-h' in args:
        print("Voice Check - Dialogue Voice Distinctiveness Analyzer\n")
        print("Usage:")
        print("  python voice_check.py <file>")
        print('  python voice_check.py --text "dialogue here"\n')
        print("Options:")
        print('  --text "..."  Provide dialogue inline')
        print("  --json        Output as JSON")
        print("  --help        Show this message\n")
        print("Expected formats:")
        print('  - "Dialogue," said Speaker.')
        print('  - "Dialogue," Speaker said.')
        print('  - Speaker said, "Dialogue."')
        print("  - SPEAKER: Dialogue\n")
        print("The tool compares vocabulary, sentence patterns, and speech")
        print("characteristics to measure how distinct each speaker's voice is.")
        sys.exit(0)
    json_output = '--json' in args
    text = ""
    if '--text' in args:
        text_index = args.index('--text')
        text = args[text_index + 1] if text_index + 1 < len(args) else ""
    else:
        file_path = next((a for a in args if not a.startswith('--')), None)
        if file_path:
            try:
                text = open(file_path, 'r', encoding='utf-8').read()
            except Exception as e:
                print(f"Error reading file: {e}", file=sys.stderr)
                sys.exit(1)
    if not text.strip():
        print("Error: No text provided. Use --text or provide a file path.", file=sys.stderr)
        sys.exit(1)
    speaker_data = extract_dialogue(text)
    if not speaker_data:
        print("Error: Could not extract dialogue. Check format (see --help).", file=sys.stderr)
        sys.exit(1)
    analysis = analyze_voices(speaker_data)
    if json_output:
        json_safe = dict(analysis)
        json_safe['speakers'] = {
            k: {kk: (list(vv) if isinstance(vv, set) else vv) for kk, vv in v.items()}
            for k, v in analysis['speakers'].items()
        }
        print(json.dumps(json_safe, indent=2))
    else:
        print(format_report(analysis))


if __name__ == '__main__':
    main()
