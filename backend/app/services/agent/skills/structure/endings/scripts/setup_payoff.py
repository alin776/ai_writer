#!/usr/bin/env python3
"""
setup_payoff.py - Setup-Payoff Tracker

Tracks setups (Chekhov's guns) and payoffs across a story.
Helps identify unresolved setups and payoffs without setup.

Usage:
  python setup_payoff.py --analyze story.txt
  python setup_payoff.py --setup "rusty key" --file story.txt
  python setup_payoff.py --list story.txt
  python setup_payoff.py --json --analyze story.txt
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
# Setup patterns - things introduced that might need payoff
# ---------------------------------------------------------------------------

SETUP_PATTERNS = [
    {
        "type": "object",
        "patterns": [
            re.compile(r"\b(noticed|saw|spotted|found|discovered|picked up|grabbed|took|carried|kept|hidden|concealed)\s+(a|an|the)\s+([a-z]+\s+)?([a-z]+)", re.I),
            re.compile(r"\b(the|a|an)\s+([a-z]+\s+)?(key|gun|knife|sword|letter|photograph|ring|necklace|book|box|bag|case|weapon|tool)\b", re.I),
        ],
    },
    {
        "type": "skill",
        "patterns": [
            re.compile(r"\b(knew how to|could|was able to|trained in|learned|practiced|mastered|skilled at|expert in)\b", re.I),
            re.compile(r"\b(years of|experience with|background in|history of)\b", re.I),
        ],
    },
    {
        "type": "character",
        "patterns": [
            re.compile(r"\b(had\s+a\s+(brother|sister|friend|enemy|rival|ally)|someone\s+who|a\s+person\s+from)\b", re.I),
            re.compile(r"\b(old\s+(friend|enemy|acquaintance)|former\s+(colleague|partner|lover))\b", re.I),
        ],
    },
    {
        "type": "information",
        "patterns": [
            re.compile(r"\b(secret|knew\s+that|heard\s+that|remembered|recalled|once\s+told|mentioned)\b", re.I),
            re.compile(r"\b(no\s+one\s+knew|only\s+\w+\s+knew|hidden\s+truth|the\s+real\s+reason)\b", re.I),
        ],
    },
    {
        "type": "threat",
        "patterns": [
            re.compile(r"\b(would\s+return|wasn't\s+over|still\s+out\s+there|waiting|watching|someday)\b", re.I),
            re.compile(r"\b(warned|threatened|promised\s+to|swore\s+to|vowed)\b", re.I),
        ],
    },
    {
        "type": "promise",
        "patterns": [
            re.compile(r"\b(promised|swore|vowed|committed|pledged|gave\s+\w+\s+word)\b", re.I),
            re.compile(r"\b(would\s+never|would\s+always|one\s+day|someday)\b", re.I),
        ],
    },
    {
        "type": "foreshadow",
        "patterns": [
            re.compile(r"\b(little\s+did|if\s+only|would\s+later|couldn't\s+have\s+known|foreshadow)\b", re.I),
            re.compile(r"\b(ominous|foreboding|sense\s+of|feeling\s+that|premonition)\b", re.I),
        ],
    },
]

# ---------------------------------------------------------------------------
# Payoff patterns - things that might be resolving setups
# ---------------------------------------------------------------------------

PAYOFF_PATTERNS = [
    {
        "type": "object",
        "patterns": [
            re.compile(r"\b(used|pulled\s+out|reached\s+for|grabbed|produced|wielded|fired|unlocked|opened\s+with)\b", re.I),
            re.compile(r"\b(the\s+(key|gun|knife|sword|letter|ring|weapon)\s+(worked|opened|saved|killed|revealed))\b", re.I),
        ],
    },
    {
        "type": "skill",
        "patterns": [
            re.compile(r"\b(finally\s+could|now\s+knew\s+how|training\s+paid\s+off|skills\s+saved|experience\s+told)\b", re.I),
            re.compile(r"\b(years\s+of\s+\w+\s+paid\s+off|remembered\s+how\s+to)\b", re.I),
        ],
    },
    {
        "type": "character",
        "patterns": [
            re.compile(r"\b(arrived|appeared|returned|showed\s+up|came\s+back|was\s+there)\b", re.I),
            re.compile(r"\b(unexpected\s+ally|old\s+friend\s+\w+|recognized)\b", re.I),
        ],
    },
    {
        "type": "information",
        "patterns": [
            re.compile(r"\b(realized|understood|finally\s+knew|the\s+truth\s+was|now\s+it\s+made\s+sense)\b", re.I),
            re.compile(r"\b(revealed|exposed|came\s+to\s+light|discovered\s+that)\b", re.I),
        ],
    },
    {
        "type": "threat",
        "patterns": [
            re.compile(r"\b(returned|came\s+back|finally\s+struck|made\s+good|carried\s+out)\b", re.I),
            re.compile(r"\b(defeated|destroyed|overcame|escaped|survived|confronted)\b", re.I),
        ],
    },
    {
        "type": "promise",
        "patterns": [
            re.compile(r"\b(kept\s+\w+\s+promise|fulfilled|honored|made\s+good|finally\s+could)\b", re.I),
            re.compile(r"\b(as\s+promised|true\s+to\s+\w+\s+word|never\s+forgot)\b", re.I),
        ],
    },
    {
        "type": "foreshadow",
        "patterns": [
            re.compile(r"\b(just\s+as|as\s+foretold|the\s+prophecy|finally|inevitable)\b", re.I),
            re.compile(r"\b(now\s+understood|saw\s+it\s+coming|knew\s+it\s+would)\b", re.I),
        ],
    },
]


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def get_line_context(text, position, window_size=50):
    """Return a snippet of text around *position* for context display."""
    start = max(0, position - window_size)
    end = min(len(text), position + window_size)
    context = text[start:end].replace("\n", " ").strip()
    if start > 0:
        context = "..." + context
    if end < len(text):
        context = context + "..."
    return context


def find_setups(text):
    """Find potential setups in the first 70 % of *text*."""
    text_length = len(text)
    setups = []

    for group in SETUP_PATTERNS:
        setup_type = group["type"]
        for pattern in group["patterns"]:
            for m in pattern.finditer(text):
                position_pct = (m.start() / text_length) * 100 if text_length else 0
                # Only consider setups in first 70% of text
                if position_pct <= 70:
                    setups.append({
                        "text": m.group(0).lower().strip(),
                        "position": m.start(),
                        "positionPercent": round(position_pct),
                        "type": setup_type,
                        "lineContext": get_line_context(text, m.start()),
                    })

    # Deduplicate by text similarity
    unique = []
    for setup in setups:
        is_dup = any(
            u["text"] == setup["text"] and abs(u["position"] - setup["position"]) < 100
            for u in unique
        )
        if not is_dup:
            unique.append(setup)

    unique.sort(key=lambda s: s["position"])
    return unique


def find_payoffs(text):
    """Find potential payoffs in the last 50 % of *text*."""
    text_length = len(text)
    payoffs = []

    for group in PAYOFF_PATTERNS:
        payoff_type = group["type"]
        for pattern in group["patterns"]:
            for m in pattern.finditer(text):
                position_pct = (m.start() / text_length) * 100 if text_length else 0
                # Only consider payoffs in last 50% of text
                if position_pct >= 50:
                    payoffs.append({
                        "text": m.group(0).lower().strip(),
                        "position": m.start(),
                        "positionPercent": round(position_pct),
                        "type": payoff_type,
                        "lineContext": get_line_context(text, m.start()),
                    })

    # Deduplicate
    unique = []
    for payoff in payoffs:
        is_dup = any(
            u["text"] == payoff["text"] and abs(u["position"] - payoff["position"]) < 100
            for u in unique
        )
        if not is_dup:
            unique.append(payoff)

    unique.sort(key=lambda p: p["position"])
    return unique


def match_setups_to_payoffs(setups, payoffs, text_length):
    """Try to pair setups with payoffs of the same type.

    Returns a dict with keys: matched, unresolved, orphaned.
    """
    matched = []
    used_setups = set()
    used_payoffs = set()

    for i, setup in enumerate(setups):
        for j, payoff in enumerate(payoffs):
            if j in used_payoffs:
                continue
            if setup["type"] == payoff["type"] and payoff["position"] > setup["position"]:
                distance = payoff["position"] - setup["position"]
                distance_pct = round((distance / text_length) * 100) if text_length else 0
                matched.append({
                    "setup": setup,
                    "payoff": payoff,
                    "distance": distance,
                    "distancePercent": distance_pct,
                })
                used_setups.add(i)
                used_payoffs.add(j)
                break

    unresolved = [s for i, s in enumerate(setups) if i not in used_setups]
    orphaned = [p for j, p in enumerate(payoffs) if j not in used_payoffs]

    return {"matched": matched, "unresolved": unresolved, "orphaned": orphaned}


def search_for_term(text, term):
    """Search for *term* throughout *text* and return occurrence locations."""
    term_lower = term.lower()
    text_lower = text.lower()
    occurrences = []

    pos = 0
    while True:
        idx = text_lower.find(term_lower, pos)
        if idx == -1:
            break
        pct = round((idx / len(text)) * 100) if len(text) else 0
        occurrences.append({
            "position": idx,
            "percent": pct,
            "context": get_line_context(text, idx, 60),
        })
        pos = idx + len(term_lower)

    return {"found": len(occurrences) > 0, "occurrences": occurrences}


# ---------------------------------------------------------------------------
# Full analysis
# ---------------------------------------------------------------------------

def analyze_setup_payoff(text, file_name="input"):
    """Run the complete setup-payoff analysis on *text*."""
    words = [w for w in re.split(r"\s+", text) if w]
    setups = find_setups(text)
    payoffs = find_payoffs(text)
    result = match_setups_to_payoffs(setups, payoffs, len(text))
    matched = result["matched"]
    unresolved = result["unresolved"]
    orphaned = result["orphaned"]

    issues = []
    recommendations = []

    # Assess health
    health = "good"

    if len(unresolved) > 3:
        health = "problems"
        issues.append(f"{len(unresolved)} potential setups without payoffs detected")
        recommendations.append("Review unresolved setups - either pay them off or remove them")
    elif len(unresolved) > 0:
        health = "issues"
        issues.append(f"{len(unresolved)} potential unresolved setup(s)")

    if len(orphaned) > 2:
        if health == "good":
            health = "issues"
        issues.append(f"{len(orphaned)} potential payoffs without clear setup (deus ex machina risk)")
        recommendations.append("Ensure late-story resolutions are established earlier")

    if len(matched) == 0 and len(setups) > 0:
        issues.append("No setup-payoff matches detected - story may lack satisfying resolution")
        recommendations.append("Track your setups and ensure they pay off by the end")

    # Check for setups too close to payoff
    quick_payoffs = [m for m in matched if m["distancePercent"] < 10]
    if quick_payoffs:
        issues.append("Some setups pay off very quickly (may reduce impact)")
        recommendations.append("Consider more distance between setup and payoff for greater impact")

    return {
        "fileName": file_name,
        "wordCount": len(words),
        "potentialSetups": setups,
        "potentialPayoffs": payoffs,
        "matchedPairs": matched,
        "unresolvedSetups": unresolved,
        "orphanedPayoffs": orphaned,
        "setupPayoffHealth": health,
        "issues": issues,
        "recommendations": recommendations,
    }


# ---------------------------------------------------------------------------
# Reporting
# ---------------------------------------------------------------------------

def format_report(analysis):
    """Return a human-readable setup-payoff report."""
    lines = []

    lines.append("# Setup-Payoff Analysis\n")
    lines.append(f"File: {analysis['fileName']}")
    lines.append(f"Words: {analysis['wordCount']}")
    lines.append(f"Health: {analysis['setupPayoffHealth'].upper()}\n")

    lines.append("## Summary\n")
    lines.append(f"  Potential setups detected: {len(analysis['potentialSetups'])}")
    lines.append(f"  Potential payoffs detected: {len(analysis['potentialPayoffs'])}")
    lines.append(f"  Matched pairs: {len(analysis['matchedPairs'])}")
    lines.append(f"  Unresolved setups: {len(analysis['unresolvedSetups'])}")
    lines.append(f"  Orphaned payoffs: {len(analysis['orphanedPayoffs'])}")
    lines.append("")

    if analysis["matchedPairs"]:
        lines.append("## Matched Setup-Payoff Pairs\n")
        for pair in analysis["matchedPairs"][:10]:
            s = pair["setup"]
            p = pair["payoff"]
            lines.append(f"  [{s['type']}] Setup at {s['positionPercent']}% -> Payoff at {p['positionPercent']}%")
            lines.append(f"    Setup: \"{s['text']}\"")
            lines.append(f"    Payoff: \"{p['text']}\"")
            lines.append("")
        if len(analysis["matchedPairs"]) > 10:
            lines.append(f"  ... and {len(analysis['matchedPairs']) - 10} more pairs\n")

    if analysis["unresolvedSetups"]:
        lines.append("## Unresolved Setups (Chekhov's Guns Unfired)\n")
        for setup in analysis["unresolvedSetups"][:10]:
            lines.append(f"  [{setup['type']}] at {setup['positionPercent']}%: \"{setup['text']}\"")
            lines.append(f"    Context: {setup['lineContext']}")
            lines.append("")

    if analysis["orphanedPayoffs"]:
        lines.append("## Orphaned Payoffs (Possible Deus Ex Machina)\n")
        for payoff in analysis["orphanedPayoffs"][:10]:
            lines.append(f"  [{payoff['type']}] at {payoff['positionPercent']}%: \"{payoff['text']}\"")
            lines.append(f"    Context: {payoff['lineContext']}")
            lines.append("")

    if analysis["issues"]:
        lines.append("## Issues\n")
        for issue in analysis["issues"]:
            lines.append(f"  - {issue}")
        lines.append("")

    if analysis["recommendations"]:
        lines.append("## Recommendations\n")
        for rec in analysis["recommendations"]:
            lines.append(f"  - {rec}")
        lines.append("")

    return "\n".join(lines)


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------

def main():
    args = sys.argv[1:]

    if "--help" in args or "-h" in args:
        print("""Setup-Payoff Tracker

Usage:
  python setup_payoff.py --analyze <file>
  python setup_payoff.py --setup "term" --file <file>
  python setup_payoff.py --list <file>

Modes:
  --analyze      Full setup-payoff analysis
  --setup "X"    Search for specific term throughout story
  --list         List all detected setups and payoffs

Options:
  --file <f>     Specify input file
  --text "..."   Provide text directly
  --json         Output as JSON
  --help         Show this message

Detects:
  - Objects (Chekhov's gun)
  - Skills (training/ability)
  - Characters (allies, enemies)
  - Information (secrets, knowledge)
  - Threats (warnings, foreshadowing)
  - Promises (commitments)
""")
        sys.exit(0)

    json_output = "--json" in args
    text = ""
    file_name = "input"

    # --text flag for inline text
    if "--text" in args:
        idx = args.index("--text")
        text = " ".join(args[idx + 1:])
        # strip any subsequent flags from text
        # (simple approach: take until next --)
        parts = []
        for part in args[idx + 1:]:
            if part.startswith("--"):
                break
            parts.append(part)
        text = " ".join(parts)
    else:
        # Get file via --file or positional arg
        if "--file" in args:
            file_idx = args.index("--file")
            if file_idx + 1 < len(args):
                file_name = args[file_idx + 1]
                try:
                    with open(file_name, "r", encoding="utf-8") as f:
                        text = f.read()
                except Exception as e:
                    print(f"Error reading file: {e}", file=sys.stderr)
                    sys.exit(1)
        else:
            # Try to find file as positional arg (non-flag, not the --setup value)
            setup_idx = args.index("--setup") if "--setup" in args else -1
            for a in args:
                if a.startswith("--"):
                    continue
                # skip the value after --setup
                if setup_idx >= 0 and args.index(a) == setup_idx + 1:
                    continue
                file_name = a
                try:
                    with open(a, "r", encoding="utf-8") as f:
                        text = f.read()
                except Exception as e:
                    print(f"Error reading file: {e}", file=sys.stderr)
                    sys.exit(1)
                break

    if not text.strip():
        print("No text provided. Use --file <path>, --text \"...\", or provide a file path as argument.",
              file=sys.stderr)
        sys.exit(1)

    # --- Search for specific setup ---
    if "--setup" in args:
        setup_idx = args.index("--setup")
        if setup_idx + 1 >= len(args):
            print("Error: --setup requires a search term", file=sys.stderr)
            sys.exit(1)
        term = args[setup_idx + 1]

        result = search_for_term(text, term)
        if json_output:
            print(json.dumps(result, ensure_ascii=False, indent=2))
        else:
            print(f"\n# Search for \"{term}\"\n")
            if result["found"]:
                print(f"Found {len(result['occurrences'])} occurrence(s):\n")
                for occ in result["occurrences"]:
                    print(f"  At {occ['percent']}%: {occ['context']}\n")
            else:
                print("Term not found in text.")
        sys.exit(0)

    # --- List mode ---
    if "--list" in args:
        setups = find_setups(text)
        payoffs = find_payoffs(text)

        if json_output:
            print(json.dumps({"setups": setups, "payoffs": payoffs},
                             ensure_ascii=False, indent=2))
        else:
            print("\n# Detected Setups (first 70%)\n")
            for s in setups:
                print(f"  [{s['type']}] {s['positionPercent']}%: \"{s['text']}\"")
            print("\n# Detected Payoffs (last 50%)\n")
            for p in payoffs:
                print(f"  [{p['type']}] {p['positionPercent']}%: \"{p['text']}\"")
        sys.exit(0)

    # --- Full analysis (default / --analyze) ---
    analysis = analyze_setup_payoff(text, file_name)

    if json_output:
        print(json.dumps(analysis, ensure_ascii=False, indent=2))
    else:
        print(format_report(analysis))


if __name__ == "__main__":
    main()
