#!/usr/bin/env python3
"""
analyze_scene_batch.py - Batch Scene Structure Analyzer

Applies scene-sequencing analysis (Goal/Conflict/Disaster) to all scenes
in a segmented book. Builds on patterns from scene-sequencing skill.

Usage:
  python analyze_scene_batch.py segments.json book.txt
  python analyze_scene_batch.py segments.json book.txt --output scenes.json
"""

import sys
import os
import re
import json
from datetime import datetime

# Ensure UTF-8 output on all platforms
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")
if hasattr(sys.stderr, "reconfigure"):
    sys.stderr.reconfigure(encoding="utf-8")

# == PATTERNS (from scene-sequencing skill) ==

GOAL_PATTERNS = [
    re.compile(r"\b(want|wanted|wants|need|needed|needs|must|had to|have to|trying to|attempted to|goal|objective|mission)\b", re.I),
    re.compile(r"\b(determined to|resolved to|set out to|aimed to|intended to)\b", re.I),
    re.compile(r"\b(find|get|reach|escape|stop|save|discover|learn|prove)\b", re.I),
]

CONFLICT_PATTERNS = [
    re.compile(r"\b(but|however|although|despite|yet|still|unfortunately)\b", re.I),
    re.compile(r"\b(blocked|stopped|prevented|refused|denied|resisted|fought|struggled)\b", re.I),
    re.compile(r"\b(problem|obstacle|challenge|difficulty|trouble|threat|danger)\b", re.I),
    re.compile(r"\b(against|versus|confronted|opposed|clashed)\b", re.I),
]

DISASTER_PATTERNS = [
    re.compile(r"\b(failed|lost|fell|collapsed|shattered|ruined|destroyed)\b", re.I),
    re.compile(r"\b(worse|terrible|horrible|devastating|catastrophic)\b", re.I),
    re.compile(r"\b(trapped|caught|discovered|exposed|betrayed)\b", re.I),
    re.compile(r"\b(too late|no way|impossible|hopeless)\b", re.I),
    re.compile(r"\b(and then|but then|suddenly|without warning)\b", re.I),
]

REACTION_PATTERNS = [
    re.compile(r"\b(felt|feeling|emotion|heart|stomach|chest|tears)\b", re.I),
    re.compile(r"\b(shock|horror|despair|grief|anger|fear|relief)\b", re.I),
    re.compile(r"\b(couldn't believe|couldn't think|mind raced|thoughts)\b", re.I),
    re.compile(r"\b(sat|stood|stared|gazed|looked)\s+(there|still|frozen|numb)", re.I),
]

DILEMMA_PATTERNS = [
    re.compile(r"\b(choice|decision|option|alternative|either|or)\b", re.I),
    re.compile(r"\b(could|should|might|what if|if only)\b", re.I),
    re.compile(r"\b(on one hand|on the other|weighing|considering)\b", re.I),
    re.compile(r"\b(no good options|impossible choice|between)\b", re.I),
]

DECISION_PATTERNS = [
    re.compile(r"\b(decided|decision|chose|choice|resolved|determined)\b", re.I),
    re.compile(r"\b(would|going to|had to|must|will)\b", re.I),
    re.compile(r"\b(plan|strategy|next step|only way|one thing)\b", re.I),
    re.compile(r"\b(stood up|got up|turned|headed|set off|began)\b", re.I),
]

# Disaster type patterns
DISASTER_TYPE_PATTERNS = {
    "yes-but": [re.compile(r"\byes,?\s*but\b", re.I), re.compile(r"\bsucceeded,?\s*but\b", re.I), re.compile(r"\bgot\s+it,?\s*but\b", re.I)],
    "no": [re.compile(r"\bfailed\b", re.I), re.compile(r"\bcouldn't\b", re.I), re.compile(r"\bdidn't\b", re.I), re.compile(r"\bwasn't able\b", re.I)],
    "no-and-furthermore": [re.compile(r"\bnot only.+but also\b", re.I), re.compile(r"\bworse,?\s*\b", re.I), re.compile(r"\band then.+also\b", re.I), re.compile(r"\bon top of that\b", re.I)],
}

# == UTILITIES ==


def count_matches(text, patterns):
    matches = []
    for pattern in patterns:
        found = pattern.findall(text)
        if found:
            matches.extend(found[:3])
    return list(dict.fromkeys(matches))[:5]  # unique, max 5


def calculate_confidence(indicators, text):
    if len(indicators) == 0:
        return 0
    word_count = len(re.split(r"\s+", text))
    # More indicators relative to length = higher confidence
    density = len(indicators) / (word_count / 100) if word_count > 0 else 0
    return min(1, density * 0.3 + (0.4 if len(indicators) > 2 else 0.2))


def detect_disaster_type(text):
    for dtype, patterns in DISASTER_TYPE_PATTERNS.items():
        for pattern in patterns:
            if pattern.search(text):
                return dtype
    return "unclear"


def infer_function(scene_index, total_scenes, analysis):
    position = scene_index / total_scenes if total_scenes > 0 else 0

    # Opening scenes
    if scene_index == 0:
        return "Opening scene - establishes status quo and character"

    # First 10% - setup
    if position < 0.10:
        return "Setup - introducing world and characters"

    # Around 12% - inciting incident
    if 0.10 <= position <= 0.15:
        if analysis["structure"]["disaster"]["detected"]:
            return "Inciting incident - story catalyst"

    # First plot point area (20-25%)
    if 0.20 <= position <= 0.25:
        if analysis["structure"]["goal"]["confidence"] > 0.6:
            return "First plot point - protagonist commits"

    # Rising action (25-45%)
    if 0.25 < position < 0.45:
        return "Rising action - escalating conflict"

    # Midpoint area (45-55%)
    if 0.45 <= position <= 0.55:
        if analysis["structure"]["conflict"]["confidence"] > 0.7:
            return "Midpoint - mirror moment or major revelation"

    # Complications (55-75%)
    if 0.55 < position < 0.75:
        return "Complications - stakes raise, options narrow"

    # Dark night (75-85%)
    if 0.75 <= position <= 0.85:
        if analysis["pacing"] == "reflective" or analysis["sequelElements"]["dilemma"]:
            return "Dark night - lowest point, crisis"

    # Climax (85-95%)
    if 0.85 <= position <= 0.95:
        if analysis["pacing"] == "action-heavy":
            return "Climax - final confrontation"

    # Resolution (95%+)
    if position > 0.95:
        return "Resolution - new equilibrium established"

    # Default based on pacing
    if analysis["pacing"] == "action-heavy":
        return "Action scene - conflict-driven"
    elif analysis["pacing"] == "reflective":
        return "Sequel scene - reaction and planning"

    return "Development scene - advancing plot/character"


def generate_summary(indicators, element_type):
    if len(indicators) == 0:
        return f"No clear {element_type} detected"
    display = ", ".join(str(ind) for ind in indicators[:3])
    return f"{element_type[0].upper() + element_type[1:]} indicators: {display}"


# == CORE LOGIC ==

def analyze_scene(scene_id, chapter_number, text, pov, scene_index, total_scenes):
    word_count = len([w for w in re.split(r"\s+", text) if len(w) > 0])

    # Detect elements
    goal_indicators = count_matches(text, GOAL_PATTERNS)
    conflict_indicators = count_matches(text, CONFLICT_PATTERNS)
    disaster_indicators = count_matches(text, DISASTER_PATTERNS)
    reaction_indicators = count_matches(text, REACTION_PATTERNS)
    dilemma_indicators = count_matches(text, DILEMMA_PATTERNS)
    decision_indicators = count_matches(text, DECISION_PATTERNS)

    # Calculate scene vs sequel ratio
    scene_score = len(goal_indicators) + len(conflict_indicators) + len(disaster_indicators)
    sequel_score = len(reaction_indicators) + len(dilemma_indicators) + len(decision_indicators)
    total_score = scene_score + sequel_score or 1
    scene_ratio = scene_score / total_score

    # Determine pacing
    if scene_ratio > 0.65:
        pacing = "action-heavy"
    elif scene_ratio < 0.35:
        pacing = "reflective"
    else:
        pacing = "balanced"

    # Build analysis
    analysis = {
        "id": scene_id,
        "chapterNumber": chapter_number,
        "pov": pov,
        "wordCount": word_count,
        "structure": {
            "goal": {
                "detected": len(goal_indicators) > 0,
                "confidence": calculate_confidence(goal_indicators, text),
                "indicators": goal_indicators,
                "summary": generate_summary(goal_indicators, "goal"),
            },
            "conflict": {
                "detected": len(conflict_indicators) > 0,
                "confidence": calculate_confidence(conflict_indicators, text),
                "indicators": conflict_indicators,
                "summary": generate_summary(conflict_indicators, "conflict"),
            },
            "disaster": {
                "detected": len(disaster_indicators) > 0,
                "confidence": calculate_confidence(disaster_indicators, text),
                "indicators": disaster_indicators,
                "summary": generate_summary(disaster_indicators, "disaster"),
                "type": detect_disaster_type(text),
            },
        },
        "sequelElements": {
            "reaction": len(reaction_indicators) > 0,
            "dilemma": len(dilemma_indicators) > 0,
            "decision": len(decision_indicators) > 0,
        },
        "sceneSequelRatio": round(scene_ratio * 100) / 100,
        "pacing": pacing,
        "function": "",  # Will be set below
        "issues": [],
    }

    # Infer function based on position and analysis
    analysis["function"] = infer_function(scene_index, total_scenes, analysis)

    # Detect issues
    if not analysis["structure"]["goal"]["detected"]:
        analysis["issues"].append("No clear goal detected in scene opening")
    if not analysis["structure"]["conflict"]["detected"]:
        analysis["issues"].append("No conflict indicators detected")
    if not analysis["structure"]["disaster"]["detected"] and scene_score > 0:
        analysis["issues"].append("Scene may end without clear disaster/outcome")
    if scene_ratio > 0.85:
        analysis["issues"].append("Very action-heavy - minimal reflection time")
    if scene_ratio < 0.15 and word_count > 500:
        analysis["issues"].append("Extended reflection without action")

    return analysis


def extract_scene_text(book_text, start_line, end_line):
    lines = book_text.split("\n")
    # Convert 1-based line numbers to 0-based indices
    return "\n".join(lines[start_line - 1:end_line])


def analyze_all_scenes(segments, book_text):
    scenes = []

    # Count total scenes for position calculation
    total_scenes = 0
    for chapter in segments["chapters"]:
        total_scenes += len(chapter["scenes"])

    scene_index = 0

    for chapter in segments["chapters"]:
        for scene in chapter["scenes"]:
            scene_text = extract_scene_text(book_text, scene["startLine"], scene["endLine"])
            analysis = analyze_scene(
                scene["id"],
                chapter["number"],
                scene_text,
                scene.get("povCandidate"),
                scene_index,
                total_scenes
            )
            scenes.append(analysis)
            scene_index += 1

    # Calculate summary statistics
    if len(scenes) > 0:
        avg_confidence = sum(
            (s["structure"]["goal"]["confidence"] + s["structure"]["conflict"]["confidence"] + s["structure"]["disaster"]["confidence"]) / 3
            for s in scenes
        ) / len(scenes)
    else:
        avg_confidence = 0

    pacing_distribution = {
        "actionHeavy": sum(1 for s in scenes if s["pacing"] == "action-heavy"),
        "balanced": sum(1 for s in scenes if s["pacing"] == "balanced"),
        "reflective": sum(1 for s in scenes if s["pacing"] == "reflective"),
    }

    issues_count = sum(len(s["issues"]) for s in scenes)

    return {
        "title": segments.get("title", "Untitled"),
        "analyzedAt": datetime.now().isoformat(),
        "scenes": scenes,
        "summary": {
            "totalScenes": len(scenes),
            "avgConfidence": round(avg_confidence * 100) / 100,
            "pacingDistribution": pacing_distribution,
            "issuesCount": issues_count,
        }
    }


# == CLI ==

def print_help():
    print("""Batch Scene Structure Analyzer

Usage:
  python analyze_scene_batch.py <segments.json> <book.txt> [options]

Arguments:
  segments.json    Output from segment_book.py
  book.txt         Original book text file

Options:
  --output <file>  Write output to JSON file (default: stdout)
  --depth <level>  Analysis depth: quick, standard, detailed (default: standard)
  --help, -h       Show this help message

Examples:
  python analyze_scene_batch.py segments.json novel.txt
  python analyze_scene_batch.py segments.json novel.txt --output scenes.json
""")


def main():
    args = sys.argv[1:]

    if "--help" in args or "-h" in args or len(args) < 2:
        print_help()
        sys.exit(0)

    # Parse arguments
    segments_file = ""
    book_file = ""
    output_file = ""

    skip_indices = set()

    for i in range(len(args)):
        if i in skip_indices:
            continue

        if args[i] == "--output" and i + 1 < len(args):
            output_file = args[i + 1]
            skip_indices.add(i + 1)
        elif args[i] == "--depth" and i + 1 < len(args):
            # depth is captured but not used differently in this version
            skip_indices.add(i + 1)
        elif not args[i].startswith("--"):
            if not segments_file:
                segments_file = args[i]
            elif not book_file:
                book_file = args[i]

    if not segments_file or not book_file:
        print("Error: segments.json and book.txt are required", file=sys.stderr)
        sys.exit(1)

    # Read files
    try:
        segments_json = open(segments_file, "r", encoding="utf-8").read()
        segments = json.loads(segments_json)
    except Exception as e:
        print(f"Error reading segments file: {e}", file=sys.stderr)
        sys.exit(1)

    try:
        book_text = open(book_file, "r", encoding="utf-8").read()
    except Exception as e:
        print(f"Error reading book file: {e}", file=sys.stderr)
        sys.exit(1)

    # Analyze all scenes
    result = analyze_all_scenes(segments, book_text)

    # Output
    json_output = json.dumps(result, indent=2, ensure_ascii=False)

    if output_file:
        with open(output_file, "w", encoding="utf-8") as f:
            f.write(json_output)
        print(f"Analysis complete: {result['summary']['totalScenes']} scenes analyzed")
        print(f"Average confidence: {result['summary']['avgConfidence']}")
        pd = result["summary"]["pacingDistribution"]
        print(f"Pacing: {pd['actionHeavy']} action-heavy, {pd['balanced']} balanced, {pd['reflective']} reflective")
        print(f"Output written to: {output_file}")
    else:
        print(json_output)


if __name__ == "__main__":
    main()
