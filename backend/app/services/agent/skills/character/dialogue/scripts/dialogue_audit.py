#!/usr/bin/env python3
"""
dialogue_audit.py - Double-Duty and Anti-Pattern Checker

Analyzes dialogue for function coverage (plot, character, subtext, relationship)
and common anti-patterns (exposition dump, identical twins, etc.).

Usage:
  python dialogue_audit.py <file>
  python dialogue_audit.py --text "dialogue here"
"""

import sys
import re
import json


PLOT_PATTERNS = [
    re.compile(r'\b(must|need to|have to|going to|will|plan|decide|discover|find out|learn that)\b', re.IGNORECASE),
    re.compile(r'\b(happened|killed|stole|escaped|arrived|left|died|born|married|divorced)\b', re.IGNORECASE),
    re.compile(r'\b(where is|when did|who did|what happened|how did|why did)\b', re.IGNORECASE),
    re.compile(r'\b(tomorrow|tonight|next|before|after|deadline|time)\b', re.IGNORECASE),
]

CHARACTER_PATTERNS = [
    re.compile(r'\b(I always|I never|I believe|I think|I feel|I want|I need|I hate|I love)\b', re.IGNORECASE),
    re.compile(r'\b(my father|my mother|my family|when I was|I remember|I grew up)\b', re.IGNORECASE),
    re.compile(r"\b(I'm the kind of|I'm not the type|that's not who I am|that's just how I)\b", re.IGNORECASE),
    re.compile(r'\b(afraid of|proud of|ashamed of|sorry for|grateful for)\b', re.IGNORECASE),
]

SUBTEXT_INDICATORS = [
    re.compile(r"\b(don't you think|wouldn't you say|isn't it|aren't you)\b", re.IGNORECASE),
    re.compile(r"\b(I don't know|maybe|perhaps|we'll see|it depends|that's one way)\b", re.IGNORECASE),
    re.compile(r'\b(interesting|fine|whatever|sure|if you say so|I suppose)\b', re.IGNORECASE),
    re.compile(r'\b(anyway|but what about|speaking of|by the way|never mind)\b', re.IGNORECASE),
]

RELATIONSHIP_PATTERNS = [
    re.compile(r'\b(you always|you never|you used to|remember when we|between us)\b', re.IGNORECASE),
    re.compile(r"\b(trust|believe|forgive|understand|know me|don't know me)\b", re.IGNORECASE),
    re.compile(r'\b(we|us|our|together|apart|between|relationship)\b', re.IGNORECASE),
    re.compile(r'\b(like you|love you|hate you|miss you|need you|want you)\b', re.IGNORECASE),
]

EXPOSITION_PATTERNS = [
    re.compile(r"\b(as you know|as I'm sure you're aware|you remember|of course you know)\b", re.IGNORECASE),
    re.compile(r"\b(let me explain|I'll tell you|you see|the thing is|basically)\b", re.IGNORECASE),
    re.compile(r'\b(founded in|established in|years ago when|the history of)\b', re.IGNORECASE),
]

SAID_BOOKISMS = [
    "exclaimed", "declared", "announced", "proclaimed", "stated",
    "uttered", "articulated", "vocalized", "verbalized", "intoned",
    "opined", "remarked", "observed", "noted", "commented",
    "retorted", "countered", "snapped", "barked", "growled",
    "hissed", "snarled", "spat", "thundered", "boomed",
    "cooed", "purred", "breathed", "sighed", "moaned",
    "whimpered", "sobbed", "wailed", "shrieked", "screamed",
    "chuckled", "giggled", "laughed", "snickered", "guffawed",
]


def count_matches(text, patterns):
    matches = []
    for pattern in patterns:
        found = pattern.findall(text)
        if found:
            matches.extend(found[:3])
    return list(dict.fromkeys(matches))


def detect_function(text, patterns):
    signals = count_matches(text, patterns)
    count = len(signals)
    if count >= 3:
        confidence = "high"
    elif count >= 1:
        confidence = "medium"
    else:
        confidence = "low"
    return {
        'detected': count > 0,
        'confidence': confidence,
        'signals': signals[:5],
    }


def analyze_dialogue_tags(text):
    said_matches = re.findall(r'\bsaid\b', text, re.IGNORECASE)
    bookism_pattern = re.compile(r'\b(' + '|'.join(SAID_BOOKISMS) + r')\b', re.IGNORECASE)
    bookism_matches = bookism_pattern.findall(text)
    action_beat_pattern = re.compile(
        r'"\s+[A-Z][a-z]+\s+(walked|stood|sat|turned|looked|crossed|nodded|shook|smiled|frowned|leaned|moved|stepped|grabbed|picked|put|set|ran|jumped)',
        re.IGNORECASE,
    )
    action_beats = action_beat_pattern.findall(text)
    found_bookisms = list(dict.fromkeys(m.lower() for m in bookism_matches))
    return {
        'said_count': len(said_matches),
        'other_tag_count': len(bookism_matches),
        'action_beat_count': len(action_beats),
        'said_bookisms': found_bookisms,
        'tag_healthy': len(bookism_matches) <= len(said_matches),
    }


def detect_anti_patterns(text):
    patterns = []
    exposition_matches = count_matches(text, EXPOSITION_PATTERNS)
    patterns.append({
        'name': "Exposition Dump",
        'detected': len(exposition_matches) > 0,
        'severity': "high" if len(exposition_matches) >= 2 else "medium",
        'evidence': exposition_matches,
    })
    emotional_tag_pattern = re.compile(
        r'said\s+(angrily|sadly|happily|nervously|anxiously|fearfully|hopefully|desperately|quietly|loudly|softly|firmly|gently|harshly)',
        re.IGNORECASE,
    )
    emotional_matches = emotional_tag_pattern.findall(text)
    patterns.append({
        'name': "Emotional Narrator",
        'detected': len(emotional_matches) > 0,
        'severity': "high" if len(emotional_matches) >= 3 else "medium",
        'evidence': list(dict.fromkeys(emotional_matches))[:3],
    })
    philosopher_pattern = re.compile(
        r"\b(the moral is|what this means|the lesson here|you see|the truth is|life is about|that's what .* is really about)\b",
        re.IGNORECASE,
    )
    philosopher_matches = philosopher_pattern.findall(text)
    patterns.append({
        'name': "The Philosopher",
        'detected': len(philosopher_matches) > 0,
        'severity': "medium",
        'evidence': list(dict.fromkeys(philosopher_matches))[:3],
    })
    filler_pattern = re.compile(r'\b(um|uh|er|ah|well,|so,|like,|you know,|I mean,)\b', re.IGNORECASE)
    filler_matches = filler_pattern.findall(text)
    word_count = len(text.split()) or 1
    filler_density = len(filler_matches) / word_count
    patterns.append({
        'name': "Court Reporter",
        'detected': filler_density > 0.05,
        'severity': "high" if filler_density > 0.1 else "low",
        'evidence': list(dict.fromkeys(filler_matches))[:5],
    })
    on_the_nose_pattern = re.compile(chr(34) + r'[^' + chr(34) + r']*\b(' + "I'm angry|I'm sad|I'm happy|I'm scared|I'm worried|I feel angry|I feel sad|I feel happy" + r')\b[^' + chr(34) + r']*' + chr(34), re.IGNORECASE)
    on_the_nose_matches = on_the_nose_pattern.findall(text)
    patterns.append({
        'name': "On-The-Nose Emotions",
        'detected': len(on_the_nose_matches) > 0,
        'severity': "high" if len(on_the_nose_matches) >= 2 else "medium",
        'evidence': [m[:50] + ("..." if len(m) > 50 else "") for m in on_the_nose_matches],
    })
    return patterns


def calculate_dialogue_ratio(text):
    quotes = re.findall(r'"[^"]+"', text)
    quoted_chars = sum(len(q) for q in quotes)
    return quoted_chars / len(text) if text else 0


def audit_dialogue(text):
    words = [w for w in text.split() if w]
    dialogue_content = " ".join(re.findall(r'"([^"]+)"', text))
    functions = {
        'plot_advancement': detect_function(dialogue_content, PLOT_PATTERNS),
        'character_reveal': detect_function(dialogue_content, CHARACTER_PATTERNS),
        'subtext_present': detect_function(dialogue_content, SUBTEXT_INDICATORS),
        'relationship_dynamics': detect_function(dialogue_content, RELATIONSHIP_PATTERNS),
    }
    detected_count = sum(1 for f in functions.values() if f['detected'])
    high_confidence = sum(1 for f in functions.values() if f['confidence'] == "high")
    function_score = min(100, (detected_count * 20) + (high_confidence * 10))
    tag_analysis = analyze_dialogue_tags(text)
    anti_patterns = detect_anti_patterns(text)
    issues = []
    recommendations = []
    if detected_count < 2:
        issues.append("Dialogue may be single-function (fails Double-Duty Test)")
        recommendations.append("Add a second purpose: character revelation, relationship shift, or subtext")
    if not functions['subtext_present']['detected']:
        issues.append("No subtext indicators detected - dialogue may be too on-the-nose")
        recommendations.append("Give characters hidden agendas; make them want things they can't ask for directly")
    if not tag_analysis['tag_healthy']:
        issues.append("Too many said-bookisms relative to 'said'")
        recommendations.append("Replace descriptive tags with action beats or let dialogue carry emotion")
    for pattern in anti_patterns:
        if pattern['detected'] and pattern['severity'] != "low":
            issues.append(f"Anti-pattern detected: {pattern['name']}")
    if any(p['name'] == "Exposition Dump" and p['detected'] for p in anti_patterns):
        recommendations.append("Find conflict in the information or have characters discover it on-page")
    if any(p['name'] == "Emotional Narrator" and p['detected'] for p in anti_patterns):
        recommendations.append("Remove adverbs from tags; let words and action beats carry emotion")
    if any(p['name'] == "On-The-Nose Emotions" and p['detected'] for p in anti_patterns):
        recommendations.append("Convert direct emotional statements to shown behavior or subtext")
    return {
        'line_count': len([l for l in text.split("\n") if l.strip()]),
        'word_count': len(words),
        'dialogue_ratio': calculate_dialogue_ratio(text),
        'functions': functions,
        'function_score': function_score,
        'tag_analysis': tag_analysis,
        'anti_patterns': anti_patterns,
        'issues': issues,
        'recommendations': recommendations,
    }


def format_report(audit):
    lines = []
    lines.append("# Dialogue Audit\n")
    lines.append(f"Words: {audit['word_count']} | Dialogue ratio: {audit['dialogue_ratio'] * 100:.1f}%")
    lines.append(f"Double-Duty Score: {audit['function_score']}/100\n")
    lines.append("## Function Detection (Double-Duty Test)\n")
    function_names = {
        'plot_advancement': "Plot Advancement",
        'character_reveal': "Character Revelation",
        'subtext_present': "Subtext Present",
        'relationship_dynamics': "Relationship Dynamics",
    }
    for key, label in function_names.items():
        func = audit['functions'][key]
        status = "+" if func['detected'] else "-"
        conf = f" ({func['confidence']})" if func['detected'] else ""
        signals = f": {', '.join(func['signals'][:3])}" if func['signals'] else ""
        lines.append(f"  {status} {label}{conf}{signals}")
    lines.append("")
    lines.append("## Tag Analysis\n")
    ta = audit['tag_analysis']
    lines.append(f"  'said' count: {ta['said_count']}")
    lines.append(f"  Other tags: {ta['other_tag_count']}")
    lines.append(f"  Action beats: {ta['action_beat_count']}")
    if ta['said_bookisms']:
        lines.append(f"  Said-bookisms found: {', '.join(ta['said_bookisms'])}")
    lines.append(f"  Tag health: {'Good' if ta['tag_healthy'] else 'Needs work'}")
    lines.append("")
    detected_patterns = [p for p in audit['anti_patterns'] if p['detected']]
    if detected_patterns:
        lines.append("## Anti-Patterns Detected\n")
        for pattern in detected_patterns:
            lines.append(f"  - {pattern['name']} ({pattern['severity']})")
            if pattern['evidence']:
                lines.append(f"    Evidence: {', '.join(str(e) for e in pattern['evidence'][:2])}")
        lines.append("")
    if audit['issues']:
        lines.append("## Issues\n")
        for issue in audit['issues']:
            lines.append(f"  - {issue}")
        lines.append("")
    if audit['recommendations']:
        lines.append("## Recommendations\n")
        for rec in audit['recommendations']:
            lines.append(f"  - {rec}")
        lines.append("")
    if not audit['issues']:
        lines.append("## Assessment\n")
        lines.append("  Dialogue passes basic checks. Verify manually that:")
        lines.append("  - Characters sound distinct (run voice-check)")
        lines.append("  - Subtext is actually present (not just indicators)")
        lines.append("  - Conversation changes something by the end")
        lines.append("")
    return "\n".join(lines)


def main():
    args = sys.argv[1:]
    if '--help' in args or '-h' in args:
        print("Dialogue Audit - Double-Duty and Anti-Pattern Checker\n")
        print("Usage:")
        print("  python dialogue_audit.py <file>")
        print('  python dialogue_audit.py --text "dialogue here"\n')
        print("Options:")
        print('  --text "..."  Provide text inline')
        print("  --json        Output as JSON")
        print("  --help        Show this message\n")
        print("Checks for:")
        print("  - Function coverage (plot, character, subtext, relationship)")
        print("  - Tag usage (said vs. said-bookisms)")
        print("  - Common anti-patterns (exposition dump, emotional narrator, etc.)")
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
    audit = audit_dialogue(text)
    if json_output:
        print(json.dumps(audit, indent=2))
    else:
        print(format_report(audit))


if __name__ == '__main__':
    main()
