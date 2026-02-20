#!/usr/bin/env python3
"""
emotional_beat_map.py - Timeline Emotional Mapping

Maps emotional peaks and valleys across a work's timeline.
Helps identify the emotional experience the work delivers.

Usage:
  python emotional_beat_map.py "Work Name" --acts 5
  python emotional_beat_map.py "Work Name" --episodes 10
  python emotional_beat_map.py --compare drama,thriller
"""

import sys
import os
import json
import re
from datetime import date

# Ensure UTF-8 output on all platforms
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")
if hasattr(sys.stderr, "reconfigure"):
    sys.stderr.reconfigure(encoding="utf-8")

# == DATA ==

GENRE_EXPECTATIONS = {
    "wonder": {
        "name": "Wonder",
        "expected_peaks": [0.1, 0.5, 0.9],
        "expected_emotions": ["awe", "curiosity", "amazement", "discovery"],
        "pacing_pattern": "Builds through revelations, peaks at major discoveries",
        "key_beats": [
            {"position": 0.1, "description": "Initial wonder hook - something fascinating"},
            {"position": 0.5, "description": "Major revelation that reframes understanding"},
            {"position": 0.9, "description": "Final perspective shift or scale revelation"}
        ]
    },
    "mystery": {
        "name": "Mystery",
        "expected_peaks": [0.25, 0.5, 0.75, 0.95],
        "expected_emotions": ["curiosity", "suspicion", "confusion", "satisfaction"],
        "pacing_pattern": "Clue distribution with rising tension toward revelation",
        "key_beats": [
            {"position": 0.1, "description": "Crime/mystery established"},
            {"position": 0.25, "description": "First major clue"},
            {"position": 0.5, "description": "Major complication or red herring"},
            {"position": 0.75, "description": "All pieces available (reader could solve)"},
            {"position": 0.95, "description": "Revelation and explanation"}
        ]
    },
    "thriller": {
        "name": "Thriller",
        "expected_peaks": [0.15, 0.4, 0.6, 0.8, 0.95],
        "expected_emotions": ["tension", "fear", "urgency", "relief"],
        "pacing_pattern": "Escalating tension with brief relief valleys",
        "key_beats": [
            {"position": 0.15, "description": "Danger established, stakes clear"},
            {"position": 0.4, "description": "First major setback"},
            {"position": 0.6, "description": "Point of no return"},
            {"position": 0.8, "description": "Darkest moment / all seems lost"},
            {"position": 0.95, "description": "Final confrontation and resolution"}
        ]
    },
    "horror": {
        "name": "Horror",
        "expected_peaks": [0.2, 0.5, 0.7, 0.9],
        "expected_emotions": ["unease", "dread", "fear", "terror", "horror"],
        "pacing_pattern": "Building dread punctuated by terror spikes",
        "key_beats": [
            {"position": 0.1, "description": "Normality before disruption"},
            {"position": 0.2, "description": "First sign something is wrong"},
            {"position": 0.5, "description": "Nature of threat becomes clear"},
            {"position": 0.7, "description": "Escape attempts fail, vulnerability maximum"},
            {"position": 0.9, "description": "Final confrontation with horror"}
        ]
    },
    "drama": {
        "name": "Drama",
        "expected_peaks": [0.25, 0.5, 0.75, 0.95],
        "expected_emotions": ["sympathy", "tension", "catharsis", "transformation"],
        "pacing_pattern": "Internal pressure building to transformation",
        "key_beats": [
            {"position": 0.1, "description": "Character's lie/flaw established"},
            {"position": 0.25, "description": "Inciting pressure on the lie"},
            {"position": 0.5, "description": "Midpoint - glimpse of truth or False victory"},
            {"position": 0.75, "description": "Dark night - lie confronted fully"},
            {"position": 0.95, "description": "Transformation or tragic fall"}
        ]
    },
    "adventure": {
        "name": "Adventure",
        "expected_peaks": [0.15, 0.35, 0.55, 0.75, 0.95],
        "expected_emotions": ["excitement", "danger", "triumph", "wonder"],
        "pacing_pattern": "Action peaks with brief recovery valleys",
        "key_beats": [
            {"position": 0.1, "description": "Call to adventure"},
            {"position": 0.25, "description": "First threshold crossed"},
            {"position": 0.5, "description": "Major challenge overcome"},
            {"position": 0.75, "description": "Supreme ordeal"},
            {"position": 0.95, "description": "Victory and return"}
        ]
    },
    "relationship": {
        "name": "Relationship",
        "expected_peaks": [0.2, 0.5, 0.8, 0.95],
        "expected_emotions": ["longing", "connection", "conflict", "resolution"],
        "pacing_pattern": "Connection-conflict cycles building to resolution",
        "key_beats": [
            {"position": 0.15, "description": "Meet cute / initial connection"},
            {"position": 0.35, "description": "Growing intimacy"},
            {"position": 0.5, "description": "Major obstacle or conflict"},
            {"position": 0.75, "description": "Dark moment / seeming end"},
            {"position": 0.95, "description": "Resolution (together or apart)"}
        ]
    },
    "humor": {
        "name": "Humor",
        "expected_peaks": [0.1, 0.3, 0.5, 0.7, 0.9],
        "expected_emotions": ["amusement", "surprise", "delight", "release"],
        "pacing_pattern": "Regular comedic peaks with escalating absurdity",
        "key_beats": [
            {"position": 0.1, "description": "Comedic premise established"},
            {"position": 0.35, "description": "Complications compound hilariously"},
            {"position": 0.6, "description": "Situation reaches absurd extreme"},
            {"position": 0.8, "description": "Darkest/most awkward moment"},
            {"position": 0.95, "description": "Resolution with final laugh"}
        ]
    }
}

EMOTION_VOCABULARY = {
    "positive": [
        "joy", "triumph", "relief", "hope", "love", "awe", "wonder",
        "satisfaction", "connection", "excitement", "delight", "peace"
    ],
    "negative": [
        "fear", "dread", "horror", "grief", "anger", "despair", "tension",
        "anxiety", "disgust", "shame", "loneliness", "betrayal"
    ],
    "complex": [
        "bittersweet", "melancholy", "anticipation", "unease", "catharsis",
        "ambivalence", "longing", "resignation", "defiance", "transformation"
    ]
}

# == UTILITIES ==


def create_empty_beat_map(work_name, structure_type, unit_count):
    return {
        "work_name": work_name,
        "structure_type": structure_type,
        "unit_count": unit_count,
        "primary_genre": "",
        "beats": [],
        "analysis": {
            "peaks": [],
            "valleys": [],
            "dominant_emotions": [],
            "pacing_notes": ""
        }
    }


def format_beat_map(beat_map):
    lines = []

    lines.append(f"# Emotional Beat Map: {beat_map['work_name']}")
    lines.append("")
    lines.append(f"**Structure:** {beat_map['unit_count']} {beat_map['structure_type']}")
    lines.append(f"**Primary Genre:** {beat_map['primary_genre'] or '(not set)'}")
    lines.append("")

    # Visual timeline
    lines.append("## Timeline")
    lines.append("")
    lines.append("```")
    lines.append("Position  0%   25%   50%   75%   100%")
    lines.append("          |-----|-----|-----|-----|")

    if len(beat_map["beats"]) > 0:
        sorted_beats = sorted(beat_map["beats"], key=lambda b: b["position"])
        for beat in sorted_beats:
            pos = round(beat["position"] * 100)
            if beat["beat_type"] == "peak":
                marker = "^"
            elif beat["beat_type"] == "valley":
                marker = "v"
            else:
                marker = "-"
            spacer = " " * max(0, int(pos / 5))
            lines.append(f"{str(pos).rjust(3)}%{spacer}{marker} {beat['emotion']} ({beat['element']})")
    else:
        lines.append("(No beats mapped yet)")

    lines.append("```")
    lines.append("")

    # Beat details
    if len(beat_map["beats"]) > 0:
        lines.append("## Beat Details")
        lines.append("")
        lines.append("| Position | Type | Emotion | Intensity | Element |")
        lines.append("|----------|------|---------|-----------|---------|")
        for beat in sorted(beat_map["beats"], key=lambda b: b["position"]):
            pos = f"{round(beat['position'] * 100)}%"
            lines.append(f"| {pos} | {beat['beat_type']} | {beat['emotion']} | {beat['intensity']}/10 | {beat['element']} |")
        lines.append("")

    # Analysis
    if beat_map["analysis"]["pacing_notes"]:
        lines.append("## Analysis")
        lines.append("")
        lines.append(beat_map["analysis"]["pacing_notes"])
        lines.append("")

    return "\n".join(lines)


def format_genre_comparison(genres):
    lines = []

    lines.append("# Genre Emotional Expectations Comparison")
    lines.append("")

    for genre in genres:
        expectations = GENRE_EXPECTATIONS.get(genre.lower())
        if not expectations:
            lines.append(f"## {genre}")
            lines.append("(Unknown genre - no expectations defined)")
            lines.append("")
            continue

        lines.append(f"## {expectations['name']}")
        lines.append("")
        lines.append(f"**Pacing Pattern:** {expectations['pacing_pattern']}")
        lines.append("")
        lines.append(f"**Expected Emotions:** {', '.join(expectations['expected_emotions'])}")
        lines.append("")
        lines.append("**Key Beats:**")
        for beat in expectations["key_beats"]:
            lines.append(f"- {round(beat['position'] * 100)}%: {beat['description']}")
        lines.append("")

    # Side-by-side if multiple genres
    if len(genres) > 1:
        lines.append("## Comparison Grid")
        lines.append("")
        header_names = []
        for g in genres:
            exp = GENRE_EXPECTATIONS.get(g.lower())
            header_names.append(exp["name"] if exp else g)
        lines.append("| Position | " + " | ".join(header_names) + " |")
        lines.append("|----------|" + "|".join(["---"] * len(genres)) + "|")

        positions = [0.1, 0.25, 0.35, 0.5, 0.6, 0.75, 0.8, 0.9, 0.95]
        for pos in positions:
            cells = []
            for g in genres:
                exp = GENRE_EXPECTATIONS.get(g.lower())
                if not exp:
                    cells.append("-")
                    continue
                beat = next((b for b in exp["key_beats"] if abs(b["position"] - pos) < 0.05), None)
                cells.append(beat["description"][:30] if beat else "-")
            lines.append(f"| {round(pos * 100)}% | {' | '.join(cells)} |")
        lines.append("")

    return "\n".join(lines)


def format_template(work_name, structure_type, unit_count):
    lines = []

    lines.append(f"# Emotional Beat Map Template: {work_name}")
    lines.append("")
    lines.append(f"Structure: {unit_count} {structure_type}")
    lines.append("")
    lines.append("## Instructions")
    lines.append("")
    lines.append("For each significant emotional moment, record:")
    lines.append("- Position (0.0 - 1.0)")
    lines.append("- Emotion (what audience should feel)")
    lines.append("- Intensity (1-10)")
    lines.append("- Element (what causes this emotion)")
    lines.append("- Type: peak (high intensity), valley (low/recovery), sustain, shift")
    lines.append("")

    lines.append("## Emotion Vocabulary")
    lines.append("")
    lines.append("**Positive:** " + ", ".join(EMOTION_VOCABULARY["positive"]))
    lines.append("")
    lines.append("**Negative:** " + ", ".join(EMOTION_VOCABULARY["negative"]))
    lines.append("")
    lines.append("**Complex:** " + ", ".join(EMOTION_VOCABULARY["complex"]))
    lines.append("")

    lines.append("## Beat Recording Template")
    lines.append("")

    # Generate position markers based on structure
    increment = 1 / unit_count
    for i in range(unit_count + 1):
        pos = i * increment
        if structure_type == "acts":
            label = f"Act {i + 1} start"
        elif structure_type == "episodes":
            label = f"Episode {i + 1}"
        else:
            label = f"Chapter {i + 1}"
        lines.append(f"### {round(pos * 100)}% - {label}")
        lines.append("")
        lines.append("| Emotion | Intensity | Element | Type |")
        lines.append("|---------|-----------|---------|------|")
        lines.append("|         |           |         |      |")
        lines.append("")

    return "\n".join(lines)


# == MAIN ==

def main():
    args = sys.argv[1:]

    # Help
    if "--help" in args or "-h" in args:
        print("""Emotional Beat Map - Timeline Emotional Mapping

Usage:
  python emotional_beat_map.py "Work Name" --acts 5
  python emotional_beat_map.py "Work Name" --episodes 10
  python emotional_beat_map.py "Work Name" --chapters 20
  python emotional_beat_map.py --compare drama,thriller
  python emotional_beat_map.py --genres

Options:
  --acts <n>        Structure as n acts (default for plays)
  --episodes <n>    Structure as n episodes (default for TV)
  --chapters <n>    Structure as n chapters (default for novels)
  --compare <list>  Compare genre expectations (comma-separated)
  --genres          List available genres with expectations
  --json            Output as JSON

Examples:
  # Five-act play template
  python emotional_beat_map.py "Hamlet" --acts 5

  # TV season template
  python emotional_beat_map.py "Killjoys S1" --episodes 10

  # Compare drama and thriller expectations
  python emotional_beat_map.py --compare drama,thriller
""")
        sys.exit(0)

    is_json = "--json" in args

    # Handle --genres flag
    if "--genres" in args:
        genres = list(GENRE_EXPECTATIONS.keys())
        if is_json:
            print(json.dumps(GENRE_EXPECTATIONS, indent=2, ensure_ascii=False))
        else:
            print("Available genres with expectations:")
            for genre in genres:
                exp = GENRE_EXPECTATIONS[genre]
                print(f"  {exp['name']}: {exp['pacing_pattern']}")
        return

    # Handle --compare flag
    compare_index = args.index("--compare") if "--compare" in args else -1
    if compare_index != -1:
        if compare_index + 1 >= len(args):
            print("Error: --compare requires comma-separated genre list", file=sys.stderr)
            sys.exit(1)
        genre_list = args[compare_index + 1]
        genres = [g.strip() for g in genre_list.split(",")]

        if is_json:
            comparison = {}
            for g in genres:
                comparison[g] = GENRE_EXPECTATIONS.get(g.lower())
            print(json.dumps(comparison, indent=2, ensure_ascii=False))
        else:
            print(format_genre_comparison(genres))
        return

    # Parse structure flags
    acts_index = args.index("--acts") if "--acts" in args else -1
    episodes_index = args.index("--episodes") if "--episodes" in args else -1
    chapters_index = args.index("--chapters") if "--chapters" in args else -1

    structure_type = "acts"
    unit_count = 5

    if acts_index != -1 and acts_index + 1 < len(args):
        structure_type = "acts"
        unit_count = int(args[acts_index + 1])
    elif episodes_index != -1 and episodes_index + 1 < len(args):
        structure_type = "episodes"
        unit_count = int(args[episodes_index + 1])
    elif chapters_index != -1 and chapters_index + 1 < len(args):
        structure_type = "chapters"
        unit_count = int(args[chapters_index + 1])

    # Find work name (positional argument)
    skip_indices = set()
    for idx in [acts_index, episodes_index, chapters_index, compare_index]:
        if idx != -1:
            skip_indices.add(idx)
            skip_indices.add(idx + 1)

    work_name = None
    for i in range(len(args)):
        if not args[i].startswith("--") and i not in skip_indices:
            work_name = args[i]
            break

    if not work_name:
        print("Error: Please provide a work name", file=sys.stderr)
        print('Usage: python emotional_beat_map.py "Work Name" --acts 5', file=sys.stderr)
        sys.exit(1)

    # Generate template
    if is_json:
        beat_map = create_empty_beat_map(work_name, structure_type, unit_count)
        print(json.dumps(beat_map, indent=2, ensure_ascii=False))
    else:
        print(format_template(work_name, structure_type, unit_count))


if __name__ == "__main__":
    main()
