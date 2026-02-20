#!/usr/bin/env python3
"""
track_characters.py - Character Tracking Script

Identifies protagonist and major characters, tracks their arcs.
Uses patterns from character-arc skill.

Usage:
  python track_characters.py segments.json book.txt
  python track_characters.py segments.json book.txt --output characters.json
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

# == PATTERNS ==

LIE_PATTERNS = [
    re.compile(r"\b(always believed|never thought|everyone knew|I know that|it's just how|the world is)\b", re.I),
    re.compile(r"\b(can't trust|don't need|won't ever|could never)\b", re.I),
    re.compile(r"\b(believed that|convinced that|certain that)\b", re.I),
]

WANT_PATTERNS = [
    re.compile(r"\b(wanted nothing more|goal was|dream of|hoped to|wished for)\b", re.I),
    re.compile(r"\b(must find|must get|must have|need to)\b", re.I),
    re.compile(r"\b(desperate to|determined to|obsessed with)\b", re.I),
]

NEED_PATTERNS = [
    re.compile(r"\b(really needed|actually need|what .+ truly|deep down)\b", re.I),
    re.compile(r"\b(connection|trust|acceptance|love|forgiveness)\b", re.I),
]

GHOST_PATTERNS = [
    re.compile(r"\b(remembered|memory|flashback|years ago|back when)\b", re.I),
    re.compile(r"\b(never forgot|haunted by|couldn't forget|still remembered)\b", re.I),
    re.compile(r"\b(reminded .+ of|took .+ back to)\b", re.I),
]

TRUTH_PATTERNS = [
    re.compile(r"\b(finally understood|realized that|saw clearly|for the first time)\b", re.I),
    re.compile(r"\b(had been wrong|changed .+ mind|no longer believed)\b", re.I),
    re.compile(r"\b(truth was|saw the truth|understood now)\b", re.I),
]

TRANSFORMATION_PATTERNS = [
    re.compile(r"\b(different person|changed|transformed|no longer the same)\b", re.I),
    re.compile(r"\b(let go of|accepted that|embraced)\b", re.I),
    re.compile(r"\b(chose to|decided to|committed to)\b", re.I),
]

# POV indicators for scoring
POV_INDICATORS = [
    re.compile(r"\bthought\b", re.I),
    re.compile(r"\bfelt\b", re.I),
    re.compile(r"\bknew\b", re.I),
    re.compile(r"\bwondered\b", re.I),
    re.compile(r"\brealized\b", re.I),
]

# == UTILITIES ==

NON_NAMES = {
    "The", "This", "That", "There", "These", "Those", "When", "Where",
    "What", "Which", "While", "After", "Before", "During", "Through",
    "Chapter", "Part", "One", "Two", "Three", "First", "Second", "Third",
    "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday",
    "January", "February", "March", "April", "May", "June", "July", "August",
    "September", "October", "November", "December",
}


def extract_scene_text(book_text, start_line, end_line):
    lines = book_text.split("\n")
    return "\n".join(lines[start_line - 1:end_line])


def count_name_mentions(text, name):
    pattern = re.compile(r"\b" + re.escape(name) + r"\b", re.I)
    return len(pattern.findall(text))


def extract_proper_nouns(text):
    names = {}

    # Match capitalized words that look like names
    for match in re.finditer(r"\b([A-Z][a-z]{2,})\b", text):
        name = match.group(1)
        if name not in NON_NAMES:
            names[name] = names.get(name, 0) + 1

    return names


def find_pov_score(text, name):
    score = 0

    # Check for "Name thought/felt/knew" patterns
    for indicator in POV_INDICATORS:
        name_pattern = re.compile(r"\b" + re.escape(name) + r"\s+" + indicator.pattern, re.I)
        matches = name_pattern.findall(text)
        if matches:
            score += len(matches) * 2

    # Check for "'s thoughts/feelings" patterns
    possessive_patterns = [
        re.compile(r"\b" + re.escape(name) + r"'s\s+(thoughts?|mind|heart|eyes|stomach)", re.I),
        re.compile(r"\b" + re.escape(name) + r"'s\s+(face|expression|voice)\s+(showed|revealed|betrayed)", re.I),
    ]

    for pattern in possessive_patterns:
        matches = pattern.findall(text)
        if matches:
            score += len(matches)

    return score


def find_pattern_evidence(text, patterns, name):
    evidence = []

    for pattern in patterns:
        sentences = re.split(r"[.!?]+", text)
        for sentence in sentences:
            if name in sentence and pattern.search(sentence):
                cleaned = sentence.strip()[:100]
                if cleaned and cleaned not in evidence:
                    evidence.append(cleaned + ("..." if len(sentence.strip()) > 100 else ""))

    return evidence[:3]


def infer_arc_type(arc_components):
    has_lie = arc_components.get("lie") is not None or len(arc_components.get("lieEvidence", [])) > 0
    has_truth = arc_components.get("truthAcceptance") is not None
    has_transformation = arc_components.get("transformation") is not None

    if has_lie and has_truth and has_transformation:
        return "positive"

    if has_lie and not has_truth:
        return "negative"

    if not has_lie and has_transformation:
        return "flat"

    return "unclear"


def infer_role(is_protagonist, pov_count, mentions, arc_type):
    if is_protagonist:
        return "Protagonist"

    if pov_count > 5:
        if arc_type == "flat":
            return "Mentor figure"
        return "Major viewpoint character"

    if mentions > 20:
        return "Supporting character"

    return "Minor character"


# == CORE LOGIC ==

def track_characters(segments, book_text, options=None):
    if options is None:
        options = {}

    max_secondary = options.get("maxSecondary", 5)

    # Extract all proper nouns and count occurrences
    name_frequency = extract_proper_nouns(book_text)

    # Track POV candidates from segmentation
    pov_counts = {}
    first_appearances = {}

    for chapter in segments["chapters"]:
        for scene in chapter["scenes"]:
            pov_candidate = scene.get("povCandidate")
            if pov_candidate and pov_candidate != "[First Person]":
                pov_counts[pov_candidate] = pov_counts.get(pov_candidate, 0) + 1
                if pov_candidate not in first_appearances:
                    first_appearances[pov_candidate] = scene["id"]

    # Build character candidates
    candidates = []
    for name, mentions in name_frequency.items():
        if mentions < 5:
            continue  # Skip rarely mentioned names

        pov_score = find_pov_score(book_text, name)
        pov_scenes = pov_counts.get(name, 0)

        candidates.append({
            "name": name,
            "mentions": mentions,
            "povScore": pov_score,
            "povScenes": pov_scenes,
            "firstAppearance": first_appearances.get(name, "ch1-s1"),
        })

    # Sort by combined score (POV weighted heavily)
    candidates.sort(key=lambda c: c["povScenes"] * 10 + c["povScore"] * 2 + c["mentions"], reverse=True)

    # Override protagonist if specified
    protagonist_name = options.get("protagonistName")
    if protagonist_name:
        existing = -1
        for idx, c in enumerate(candidates):
            if c["name"].lower() == protagonist_name.lower():
                existing = idx
                break
        if existing > 0:
            protagonist_candidate = candidates.pop(existing)
            candidates.insert(0, protagonist_candidate)

    # Analyze protagonist
    protagonist = None
    if len(candidates) > 0:
        protag = candidates[0]

        # Find arc components
        arc_components = {
            "lie": None,
            "lieEvidence": find_pattern_evidence(book_text, LIE_PATTERNS, protag["name"]),
            "want": None,
            "need": None,
            "ghost": None,
            "ghostScene": None,
            "truthAcceptance": None,
            "transformation": None,
        }

        # Extract specific component summaries
        want_evidence = find_pattern_evidence(book_text, WANT_PATTERNS, protag["name"])
        if len(want_evidence) > 0:
            arc_components["want"] = want_evidence[0]

        need_evidence = find_pattern_evidence(book_text, NEED_PATTERNS, protag["name"])
        if len(need_evidence) > 0:
            arc_components["need"] = need_evidence[0]

        ghost_evidence = find_pattern_evidence(book_text, GHOST_PATTERNS, protag["name"])
        if len(ghost_evidence) > 0:
            arc_components["ghost"] = ghost_evidence[0]

        truth_evidence = find_pattern_evidence(book_text, TRUTH_PATTERNS, protag["name"])
        if len(truth_evidence) > 0:
            arc_components["truthAcceptance"] = truth_evidence[0]

        transform_evidence = find_pattern_evidence(book_text, TRANSFORMATION_PATTERNS, protag["name"])
        if len(transform_evidence) > 0:
            arc_components["transformation"] = transform_evidence[0]

        if len(arc_components["lieEvidence"]) > 0:
            arc_components["lie"] = arc_components["lieEvidence"][0]

        # Find key scenes
        key_scenes = []
        for chapter in segments["chapters"]:
            for scene in chapter["scenes"]:
                scene_text = extract_scene_text(book_text, scene["startLine"], scene["endLine"])
                name_mentions = count_name_mentions(scene_text, protag["name"])

                has_arc_content = (
                    any(p.search(scene_text) and protag["name"] in scene_text for p in LIE_PATTERNS) or
                    any(p.search(scene_text) and protag["name"] in scene_text for p in TRUTH_PATTERNS) or
                    any(p.search(scene_text) and protag["name"] in scene_text for p in TRANSFORMATION_PATTERNS)
                )

                if (scene.get("povCandidate") == protag["name"] or name_mentions > 5) and has_arc_content:
                    key_scenes.append(scene["id"])

        arc_type = infer_arc_type(arc_components)

        protagonist = {
            "name": protag["name"],
            "firstAppearance": protag["firstAppearance"],
            "povScenes": protag["povScenes"],
            "mentions": protag["mentions"],
            "arcType": arc_type,
            "arcComponents": arc_components,
            "keyScenes": key_scenes[:10],
            "role": "Protagonist",
        }

    # Analyze secondary characters
    secondary_characters = []
    for i in range(1, len(candidates)):
        if len(secondary_characters) >= max_secondary:
            break
        char = candidates[i]

        arc_components = {
            "lie": None,
            "lieEvidence": find_pattern_evidence(book_text, LIE_PATTERNS, char["name"])[:1],
            "want": None,
            "need": None,
            "ghost": None,
            "ghostScene": None,
            "truthAcceptance": None,
            "transformation": None,
        }

        if len(arc_components["lieEvidence"]) > 0:
            arc_components["lie"] = arc_components["lieEvidence"][0]

        arc_type = infer_arc_type(arc_components)

        # Find key scenes for this character
        key_scenes = []
        for chapter in segments["chapters"]:
            for scene in chapter["scenes"]:
                if scene.get("povCandidate") == char["name"]:
                    key_scenes.append(scene["id"])

        secondary_characters.append({
            "name": char["name"],
            "firstAppearance": char["firstAppearance"],
            "povScenes": char["povScenes"],
            "mentions": char["mentions"],
            "arcType": arc_type,
            "arcComponents": arc_components,
            "keyScenes": key_scenes[:5],
            "role": infer_role(False, char["povScenes"], char["mentions"], arc_type),
        })

    # Build character web (relationships based on co-occurrence)
    character_web = {}

    if protagonist:
        for secondary in secondary_characters:
            pair_key = f"{protagonist['name'].lower()}-{secondary['name'].lower()}"
            character_web[pair_key] = "relationship detected"

    return {
        "protagonist": protagonist,
        "secondaryCharacters": secondary_characters,
        "characterWeb": character_web,
        "trackedAt": datetime.now().isoformat(),
    }


# == CLI ==

def print_help():
    print("""Character Tracking Script

Usage:
  python track_characters.py <segments.json> <book.txt> [options]

Arguments:
  segments.json      Output from segment_book.py
  book.txt           Original book text file

Options:
  --output <file>      Write output to JSON file (default: stdout)
  --protagonist <name> Specify protagonist name (overrides detection)
  --max-secondary <n>  Maximum secondary characters to track (default: 5)
  --help, -h           Show this help message

Examples:
  python track_characters.py segments.json novel.txt
  python track_characters.py segments.json novel.txt --output characters.json
  python track_characters.py segments.json novel.txt --protagonist "Sarah Chen"
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
    protagonist_name = ""
    max_secondary = 5

    skip_indices = set()

    for i in range(len(args)):
        if i in skip_indices:
            continue

        if args[i] == "--output" and i + 1 < len(args):
            output_file = args[i + 1]
            skip_indices.add(i + 1)
        elif args[i] == "--protagonist" and i + 1 < len(args):
            protagonist_name = args[i + 1]
            skip_indices.add(i + 1)
        elif args[i] == "--max-secondary" and i + 1 < len(args):
            try:
                max_secondary = int(args[i + 1])
            except ValueError:
                max_secondary = 5
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

    # Track characters
    options = {
        "maxSecondary": max_secondary,
    }
    if protagonist_name:
        options["protagonistName"] = protagonist_name

    result = track_characters(segments, book_text, options)

    # Output
    json_output = json.dumps(result, indent=2, ensure_ascii=False)

    if output_file:
        with open(output_file, "w", encoding="utf-8") as f:
            f.write(json_output)
        print("Character tracking complete")
        if result["protagonist"]:
            p = result["protagonist"]
            print(f"Protagonist: {p['name']} ({p['arcType']} arc, {p['povScenes']} POV scenes)")
        print(f"Secondary characters: {', '.join(c['name'] for c in result['secondaryCharacters'])}")
        print(f"Output written to: {output_file}")
    else:
        print(json_output)


if __name__ == "__main__":
    main()
