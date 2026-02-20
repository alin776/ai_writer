#!/usr/bin/env python3
"""
sensitivity_audit.py - Pattern scanner for potential representation concerns

IMPORTANT: This tool flags patterns for HUMAN REVIEW. It cannot determine
context, intent, or whether a pattern is actually problematic. Every flag
requires human evaluation.

Detects:
- Potential stereotyping language patterns
- Uneven physical description patterns
- Common harmful trope markers
- Agency/voice distribution indicators

Usage:
  python sensitivity_audit.py manuscript.txt
  python sensitivity_audit.py --text "Sample passage..."
  python sensitivity_audit.py --json manuscript.txt
"""

import sys
import re
import json

# Ensure UTF-8 output on all platforms
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")
if hasattr(sys.stderr, "reconfigure"):
    sys.stderr.reconfigure(encoding="utf-8")

# ---------------------------------------------------------------------------
# Pattern definitions
# Each entry: (compiled_regex, note_string)
# ---------------------------------------------------------------------------

# Physical description patterns that may indicate gendered gaze
PHYSICAL_DESCRIPTION_PATTERNS = [
    (re.compile(r"\b(her|she|woman's|girl's)\s+(body|figure|curves|breasts|legs|hips|waist|lips|skin)\b", re.I), "Physical description of female body - check for male gaze"),
    (re.compile(r"\b(beautiful|gorgeous|stunning|sexy|attractive)\s+(woman|girl|she|her)\b", re.I), "Appearance-focused female description - check balance with male characters"),
    (re.compile(r"\bher\s+(ample|full|heaving|soft)\s+", re.I), "Potentially objectifying description - review context"),
]

# Stereotyping language patterns (require context review)
STEREOTYPE_PATTERNS = [
    # General
    (re.compile(r"\b(exotic|oriental)\b", re.I), "Potentially othering language - review context"),
    (re.compile(r"\b(tribe|tribal)\b", re.I), "May be appropriate or stereotyping - review context"),
    (re.compile(r"\bbroken\s+english\b", re.I), "Dialect representation - check if respectful or mocking"),
    # Agency markers
    (re.compile(r"\bsaved\s+(her|him|them)\s+from\b", re.I), "Savior dynamic - check who saves whom"),
    (re.compile(r"\bteach\s+(her|him|them)\s+(about|how)\b", re.I), "Teaching dynamic - check power dynamics"),
    (re.compile(r"\bexplain(ed|ing)?\s+(to|for)\s+(her|him|them)\b", re.I), "Explaining dynamic - check condescension"),
]

# Trope markers (require context review)
TROPE_PATTERNS = [
    # Death/suffering
    (re.compile(r"\b(died|killed|death)\b.*\b(gay|lesbian|bisexual|trans|queer)\b", re.I), "LGBTQ+ character death - check for Bury Your Gays pattern"),
    (re.compile(r"\b(gay|lesbian|bisexual|trans|queer)\b.*\b(died|killed|death)\b", re.I), "LGBTQ+ character death - check for Bury Your Gays pattern"),
    # Magical/mystical minority
    (re.compile(r"\b(wise|wisdom|ancient|mystical|spiritual)\s+(elder|grandmother|grandfather|old\s+(man|woman))\b", re.I), "Wisdom figure - check for Magical Minority trope"),
    # Mental health
    (re.compile(r"\b(crazy|insane|psycho|lunatic|mental)\s+(killer|murderer|villain)\b", re.I), "Mental illness = violence pattern - review carefully"),
    (re.compile(r"\b(schizophren|bipolar|psychotic)\b.*\b(dangerous|violent|killer)\b", re.I), "Specific diagnosis linked to violence - major concern"),
]

# Disability language patterns
DISABILITY_PATTERNS = [
    (re.compile(r"\b(wheelchair\s*bound|confined\s+to\s+(a\s+)?wheelchair)\b", re.I), "Outdated disability language - prefer 'uses a wheelchair'"),
    (re.compile(r"\b(suffer(s|ed|ing)?\s+from|afflicted\s+(with|by))\b", re.I), "Suffering framing - may be othering; review context"),
    (re.compile(r"\b(despite\s+(his|her|their)\s+disability)\b", re.I), "Inspiration porn marker - review for 'overcoming' narrative"),
    (re.compile(r"\b(special\s+needs)\b", re.I), "Euphemism - consider if 'disabled' is more direct and preferred"),
    (re.compile(r"\bthe\s+(blind|deaf|disabled|crippled|handicapped)\b", re.I), "Group-noun usage - prefer person-first or identity-first per community"),
]

# Body size patterns
BODY_PATTERNS = [
    (re.compile(r"\b(fat|obese|overweight)\s+(and|but)\s+(lazy|slovenly|gross|disgusting)\b", re.I), "Weight + negative trait - check for fatphobic stereotyping"),
    (re.compile(r"\blet\s+(herself|himself|themselves)\s+go\b", re.I), "Weight judgment - review for moralizing body size"),
    (re.compile(r"\b(thin|slim|slender)\s+(and|but)\s+(beautiful|attractive|healthy)\b", re.I), "Thin = positive pattern - review for anti-fat bias"),
]

# Dialogue patterns that might indicate same-voice issues across identities
DIALOGUE_PATTERNS = [
    (re.compile(r"\b(yes,?\s+massa|yessir|lawdy|chile)\b", re.I), "Dialect representation - verify authenticity, check for minstrelsy"),
    (re.compile(r"\bme\s+(love|want|no\s+understand)\b", re.I), "Broken speech pattern - check for mocking vs. authentic ESL"),
]


# ---------------------------------------------------------------------------
# Core logic
# ---------------------------------------------------------------------------

def match_patterns(text, patterns, category):
    """Scan *text* line-by-line against a list of (regex, note) tuples.

    Returns a list of dicts with keys:
        category, pattern, line, text, note
    """
    lines = text.split("\n")
    matches = []

    for i, line in enumerate(lines):
        for regex, note in patterns:
            for m in regex.finditer(line):
                context = line.strip()[:100] + ("..." if len(line.strip()) > 100 else "")
                matches.append({
                    "category": category,
                    "pattern": m.group(0),
                    "line": i + 1,
                    "text": context,
                    "note": note,
                })

    return matches


def analyze_text(text):
    """Run all pattern categories against *text* and return an audit result dict."""
    flags = []

    flags.extend(match_patterns(text, PHYSICAL_DESCRIPTION_PATTERNS, "Physical Description"))
    flags.extend(match_patterns(text, STEREOTYPE_PATTERNS, "Stereotyping Language"))
    flags.extend(match_patterns(text, TROPE_PATTERNS, "Harmful Tropes"))
    flags.extend(match_patterns(text, DISABILITY_PATTERNS, "Disability Language"))
    flags.extend(match_patterns(text, BODY_PATTERNS, "Body Size"))
    flags.extend(match_patterns(text, DIALOGUE_PATTERNS, "Dialogue Patterns"))

    # Sort by line number
    flags.sort(key=lambda f: f["line"])

    # Summarize by category
    summary = {}
    for flag in flags:
        cat = flag["category"]
        summary[cat] = summary.get(cat, 0) + 1

    lines = text.split("\n")
    return {
        "totalLines": len(lines),
        "flags": flags,
        "summary": summary,
    }


def format_report(result):
    """Return a human-readable audit report string."""
    report = (
        "\nSENSITIVITY AUDIT\n"
        "=================\n"
        "\n"
        "IMPORTANT: This tool flags patterns for HUMAN REVIEW.\n"
        "It cannot determine context, intent, or actual harm.\n"
        "Every flag requires thoughtful human evaluation.\n"
        "\n"
        f"Lines scanned: {result['totalLines']}\n"
        f"Patterns flagged: {len(result['flags'])}\n"
        "\n"
    )

    if result["summary"]:
        report += "SUMMARY BY CATEGORY\n"
        for category, count in result["summary"].items():
            report += f"  {category}: {count} flag(s)\n"
        report += "\n"

    if len(result["flags"]) == 0:
        report += (
            "No patterns flagged. This does NOT mean the text is free of concerns.\n"
            "Pattern matching cannot catch:\n"
            "  - Stereotyping through characterization (not language)\n"
            "  - Agency imbalances in plot structure\n"
            "  - Tropes enacted through events rather than words\n"
            "  - Subtle or contextual issues\n"
            "\n"
            "Consider full human sensitivity reading for thorough evaluation.\n"
        )
    else:
        report += "FLAGGED PATTERNS\n"
        report += "=" * 50 + "\n\n"

        current_category = ""
        for flag in result["flags"]:
            if flag["category"] != current_category:
                current_category = flag["category"]
                report += f"\n## {current_category}\n\n"

            report += f"Line {flag['line']}: \"{flag['pattern']}\"\n"
            report += f"  Context: {flag['text']}\n"
            report += f"  Note: {flag['note']}\n\n"

        report += (
            "\n" + "=" * 50 + "\n"
            "\n"
            "NEXT STEPS\n"
            "\n"
            "1. Review each flag in context - many may be appropriate\n"
            "2. For concerning patterns, consider:\n"
            "   - Is this character/scene necessary?\n"
            "   - Could this be written differently?\n"
            "   - What might affected readers experience?\n"
            "3. Consider engaging sensitivity readers for identities represented\n"
            "4. Pattern absence doesn't mean concern absence - structural issues\n"
            "   (plot, character agency, tropes) require human analysis\n"
            "\n"
            "This tool supplements but does NOT replace human sensitivity reading.\n"
        )

    return report


def show_usage():
    print(
        "\nSensitivity Audit Tool\n"
        "======================\n"
        "\n"
        "Scans text for patterns that may indicate representation concerns.\n"
        "Flags for HUMAN REVIEW - cannot determine actual harm.\n"
        "\n"
        "Usage:\n"
        "  python sensitivity_audit.py <file>\n"
        "  python sensitivity_audit.py --text \"Text to analyze...\"\n"
        "\n"
        "Pattern Categories:\n"
        "  - Physical Description: Gendered gaze, objectification\n"
        "  - Stereotyping Language: Othering, power dynamics\n"
        "  - Harmful Tropes: Known problematic patterns\n"
        "  - Disability Language: Outdated or othering terms\n"
        "  - Body Size: Fatphobic patterns\n"
        "  - Dialogue Patterns: Accent/dialect representation\n"
        "\n"
        "IMPORTANT: This tool cannot catch:\n"
        "  - Characterization-based stereotyping\n"
        "  - Plot-level agency imbalances\n"
        "  - Tropes enacted through events\n"
        "  - Contextual or subtle issues\n"
        "\n"
        "Always engage human sensitivity readers for thorough evaluation.\n"
    )


def main():
    args = sys.argv[1:]

    if "--help" in args or "-h" in args:
        show_usage()
        sys.exit(0)

    text = None
    use_json = "--json" in args

    if "--text" in args:
        idx = args.index("--text")
        text = " ".join(args[idx + 1:])
    elif len(args) > 0 and not args[0].startswith("--"):
        filename = args[0]
        try:
            with open(filename, "r", encoding="utf-8") as f:
                text = f.read()
        except Exception as e:
            print(f"Error reading file: {filename}", file=sys.stderr)
            print(str(e), file=sys.stderr)
            sys.exit(1)
    else:
        show_usage()
        sys.exit(0)

    if text is None:
        show_usage()
        sys.exit(0)

    result = analyze_text(text)

    if use_json:
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        print(format_report(result))


if __name__ == "__main__":
    main()
