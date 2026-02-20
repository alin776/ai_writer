#!/usr/bin/env python3
"""
generate_outline.py - Outline Generation Script

Synthesizes all analysis JSON files into a structured markdown outline.

Usage:
  python generate_outline.py --segments segments.json --scenes scenes.json --genre genre.json --characters characters.json
  python generate_outline.py --segments s.json --scenes sc.json --genre g.json --characters c.json --output outline.md
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

# == UTILITIES ==


def format_confidence(confidence):
    pct = round(confidence * 100)
    if pct >= 70:
        return f"{pct}% (high)"
    if pct >= 40:
        return f"{pct}% (medium)"
    return f"{pct}% (low)"


def format_pacing(pacing):
    if pacing == "action-heavy":
        return "Action-heavy (more scene than sequel)"
    elif pacing == "reflective":
        return "Reflective (more sequel than scene)"
    else:
        return "Balanced"


# == GENERATION ==

def generate_outline(segments, scenes, genre, characters, depth="standard"):
    lines = []
    today = datetime.now().isoformat().split("T")[0]

    # == HEADER ==
    lines.append(f"# Reverse Outline: {segments.get('title', 'Untitled')}")
    lines.append("")
    lines.append(f"**Generated:** {today}")
    lines.append(f"**Analysis Depth:** {depth}")
    lines.append("")
    lines.append("---")
    lines.append("")

    # == OVERVIEW ==
    lines.append("## Overview")
    lines.append("")
    lines.append(f"**Genre:** {genre.get('primaryGenre', 'unknown')} ({round(genre.get('primaryConfidence', 0) * 100)}% confidence)")
    secondary_genres = genre.get("secondaryGenres", [])
    if len(secondary_genres) > 0:
        lines.append(f"**Secondary Genres:** {', '.join(secondary_genres)}")
    lines.append(f"**Total Words:** {segments.get('totalWords', 0)}")
    metadata = segments.get("metadata", {})
    lines.append(f"**Chapters:** {metadata.get('totalChapters', 0)}")
    lines.append(f"**Scenes:** {metadata.get('totalScenes', 0)}")
    lines.append(f"**Avg Scene Length:** {metadata.get('avgSceneLength', 0)} words")
    lines.append("")

    # Pacing distribution
    summary = scenes.get("summary", {})
    pacing = summary.get("pacingDistribution", {})
    total_scenes_count = summary.get("totalScenes", 1) or 1
    lines.append("**Pacing Distribution:**")
    ah = pacing.get("actionHeavy", 0)
    bal = pacing.get("balanced", 0)
    ref = pacing.get("reflective", 0)
    lines.append(f"- Action-heavy scenes: {ah} ({round(ah / total_scenes_count * 100)}%)")
    lines.append(f"- Balanced scenes: {bal} ({round(bal / total_scenes_count * 100)}%)")
    lines.append(f"- Reflective scenes: {ref} ({round(ref / total_scenes_count * 100)}%)")
    lines.append("")

    # == KEY MOMENTS MAP ==
    lines.append("## Key Moments Map")
    lines.append("")
    lines.append(f"Framework: {genre.get('keyMomentsFramework', 'unknown')}")
    lines.append("")
    lines.append("| Key Moment | Expected Position | Emotional Experience | Story Function |")
    lines.append("|------------|-------------------|---------------------|----------------|")

    for km in genre.get("expectedKeyMoments", []):
        expected_pct = round(km.get("expectedPosition", 0) * 100)
        lines.append(f"| {km.get('type', '')} | {expected_pct}% | {km.get('emotionalExperience', '')} | {km.get('storyFunction', '')} |")
    lines.append("")

    # == CHARACTER ARCS ==
    lines.append("## Character Arcs")
    lines.append("")

    protagonist = characters.get("protagonist")
    if protagonist:
        p = protagonist
        lines.append(f"### Protagonist: {p.get('name', 'Unknown')}")
        lines.append("")
        lines.append(f"**Arc Type:** {p.get('arcType', 'unknown')}")
        lines.append(f"**POV Scenes:** {p.get('povScenes', 0)}")
        lines.append(f"**First Appearance:** {p.get('firstAppearance', 'unknown')}")
        lines.append("")

        arc = p.get("arcComponents", {})
        if arc.get("lie"):
            lines.append(f"**Lie:** {arc['lie']}")
        if arc.get("want"):
            lines.append(f"**Want:** {arc['want']}")
        if arc.get("need"):
            lines.append(f"**Need:** {arc['need']}")
        if arc.get("ghost"):
            lines.append(f"**Ghost/Backstory:** {arc['ghost']}")
        if arc.get("truthAcceptance"):
            lines.append(f"**Truth Acceptance:** {arc['truthAcceptance']}")
        if arc.get("transformation"):
            lines.append(f"**Transformation:** {arc['transformation']}")

        key_scenes = p.get("keyScenes", [])
        if len(key_scenes) > 0:
            lines.append(f"**Key Scenes:** {', '.join(key_scenes)}")
        lines.append("")

    secondary_chars = characters.get("secondaryCharacters", [])
    if len(secondary_chars) > 0:
        lines.append("### Secondary Characters")
        lines.append("")

        for c in secondary_chars:
            lines.append(f"#### {c.get('name', 'Unknown')}")
            lines.append(f"- **Role:** {c.get('role', 'unknown')}")
            lines.append(f"- **Arc Type:** {c.get('arcType', 'unknown')}")
            lines.append(f"- **POV Scenes:** {c.get('povScenes', 0)}")
            c_key_scenes = c.get("keyScenes", [])
            if len(c_key_scenes) > 0:
                lines.append(f"- **Key Scenes:** {', '.join(c_key_scenes)}")
            lines.append("")

    lines.append("---")
    lines.append("")

    # == CHAPTER-BY-CHAPTER BREAKDOWN ==
    lines.append("## Chapter-by-Chapter Breakdown")
    lines.append("")

    # Build scene lookup
    scene_map = {}
    for scene in scenes.get("scenes", []):
        scene_map[scene["id"]] = scene

    for chapter in segments.get("chapters", []):
        lines.append(f"### Chapter {chapter.get('number', '')}: {chapter.get('title', '')}")
        lines.append("")
        lines.append(f"**Word Count:** {chapter.get('wordCount', 0)}")
        lines.append(f"**Scenes:** {len(chapter.get('scenes', []))}")
        lines.append("")

        for seg_scene in chapter.get("scenes", []):
            analysis = scene_map.get(seg_scene["id"])

            lines.append(f"#### Scene {seg_scene['id']} | POV: {seg_scene.get('povCandidate') or 'Unknown'}")
            lines.append("")

            if analysis:
                lines.append(f"**Function:** {analysis.get('function', 'Unknown')}")
                lines.append("")

                if depth in ("detailed", "standard"):
                    lines.append("| Element | Analysis |")
                    lines.append("|---------|----------|")
                    goal = analysis["structure"]["goal"]
                    conflict = analysis["structure"]["conflict"]
                    disaster = analysis["structure"]["disaster"]
                    lines.append(f"| Goal | {goal['summary'] if goal['detected'] else 'Not detected'} |")
                    lines.append(f"| Conflict | {conflict['summary'] if conflict['detected'] else 'Not detected'} |")
                    disaster_text = f"{disaster['type']}: {disaster['summary']}" if disaster["detected"] else "Not detected"
                    lines.append(f"| Disaster | {disaster_text} |")

                    sequel_parts = []
                    sequel = analysis.get("sequelElements", {})
                    if sequel.get("reaction"):
                        sequel_parts.append("Reaction")
                    if sequel.get("dilemma"):
                        sequel_parts.append("Dilemma")
                    if sequel.get("decision"):
                        sequel_parts.append("Decision")
                    lines.append(f"| Sequel | {', '.join(sequel_parts) if sequel_parts else 'None detected'} |")
                    lines.append("")

                lines.append(f"**Pacing:** {format_pacing(analysis.get('pacing', 'balanced'))}")
                lines.append(f"**Words:** {analysis.get('wordCount', 0)}")

                if depth == "detailed" and len(analysis.get("issues", [])) > 0:
                    lines.append("")
                    lines.append("**Issues:**")
                    for issue in analysis["issues"]:
                        lines.append(f"- {issue}")
            else:
                lines.append(f"**Opening:** {seg_scene.get('openingText', '')}")
                lines.append(f"**Words:** {seg_scene.get('wordCount', 0)}")

            lines.append("")
            lines.append("---")
            lines.append("")

    # == APPENDIX A: INDEX BY FUNCTION ==
    lines.append("## Appendix A: Index by Function")
    lines.append("")

    # Group scenes by structural function
    function_groups = {}
    for scene in scenes.get("scenes", []):
        func_key = scene.get("function", "Unknown").split(" - ")[0]
        if func_key not in function_groups:
            function_groups[func_key] = []
        function_groups[func_key].append(scene["id"])

    lines.append("| Function | Scenes |")
    lines.append("|----------|--------|")

    function_order = [
        "Opening scene",
        "Setup",
        "Inciting incident",
        "First plot point",
        "Rising action",
        "Midpoint",
        "Complications",
        "Dark night",
        "Climax",
        "Resolution",
    ]

    listed_keys = set()
    for func in function_order:
        for key, scene_ids in function_groups.items():
            if func.lower() in key.lower():
                lines.append(f"| {key} | {', '.join(scene_ids)} |")
                listed_keys.add(key)

    # Add any functions not in the standard order
    for func_key, scene_ids in function_groups.items():
        if func_key not in listed_keys:
            lines.append(f"| {func_key} | {', '.join(scene_ids)} |")
    lines.append("")

    # == APPENDIX B: SCENE TRACKER ==
    lines.append("## Appendix B: Scene Tracker")
    lines.append("")
    lines.append("| Character | POV Scenes | Arc Type | Key Scenes |")
    lines.append("|-----------|------------|----------|------------|")

    if protagonist:
        p = protagonist
        p_key = ", ".join(p.get("keyScenes", [])[:5])
        lines.append(f"| **{p.get('name', '')}** (protagonist) | {p.get('povScenes', 0)} | {p.get('arcType', '')} | {p_key} |")

    for c in secondary_chars:
        c_key = ", ".join(c.get("keyScenes", [])[:3])
        lines.append(f"| {c.get('name', '')} | {c.get('povScenes', 0)} | {c.get('arcType', '')} | {c_key} |")
    lines.append("")

    # == APPENDIX C: ANALYSIS ==
    if depth == "detailed":
        lines.append("## Appendix C: Analysis")
        lines.append("")
        lines.append("Scene-by-scene pacing showing scene/sequel ratio:")
        lines.append("")

        for scene in scenes.get("scenes", []):
            ratio = scene.get("sceneSequelRatio", 0)
            bar_len = round(ratio * 20)
            bar = "=" * bar_len
            space = " " * (20 - bar_len)
            lines.append(f"{scene['id']}: [{bar}{space}] {round(ratio * 100)}% scene")
        lines.append("")

    # == FOOTER ==
    lines.append("---")
    lines.append("")
    lines.append("*Generated by reverse-outliner skill*")

    return "\n".join(lines)


# == CLI ==

def print_help():
    print("""Outline Generation Script

Usage:
  python generate_outline.py [options]

Required Options:
  --segments <file>    Segments JSON from segment_book.py
  --scenes <file>      Scene analysis JSON from analyze_scene_batch.py
  --genre <file>       Genre detection JSON from detect_genre.py
  --characters <file>  Character tracking JSON from track_characters.py

Other Options:
  --output <file>      Output markdown file (default: stdout)
  --depth <level>      Output depth: summary, standard, detailed (default: standard)
  --help, -h           Show this help message

Examples:
  python generate_outline.py \\
    --segments analysis/segments.json \\
    --scenes analysis/scenes.json \\
    --genre analysis/genre.json \\
    --characters analysis/characters.json \\
    --output outline.md
""")


def main():
    args = sys.argv[1:]

    if "--help" in args or "-h" in args:
        print_help()
        sys.exit(0)

    # Parse arguments
    segments_file = ""
    scenes_file = ""
    genre_file = ""
    characters_file = ""
    output_file = ""
    depth = "standard"

    skip_indices = set()

    for i in range(len(args)):
        if i in skip_indices:
            continue

        if args[i] == "--segments" and i + 1 < len(args):
            segments_file = args[i + 1]
            skip_indices.add(i + 1)
        elif args[i] == "--scenes" and i + 1 < len(args):
            scenes_file = args[i + 1]
            skip_indices.add(i + 1)
        elif args[i] == "--genre" and i + 1 < len(args):
            genre_file = args[i + 1]
            skip_indices.add(i + 1)
        elif args[i] == "--characters" and i + 1 < len(args):
            characters_file = args[i + 1]
            skip_indices.add(i + 1)
        elif args[i] == "--output" and i + 1 < len(args):
            output_file = args[i + 1]
            skip_indices.add(i + 1)
        elif args[i] == "--depth" and i + 1 < len(args):
            d = args[i + 1]
            if d in ("summary", "standard", "detailed"):
                depth = d
            skip_indices.add(i + 1)

    # Validate required files
    if not segments_file or not scenes_file or not genre_file or not characters_file:
        print("Error: four input files are required (--segments, --scenes, --genre, --characters)", file=sys.stderr)
        print_help()
        sys.exit(1)

    # Read all input files
    try:
        segments = json.loads(open(segments_file, "r", encoding="utf-8").read())
        scenes = json.loads(open(scenes_file, "r", encoding="utf-8").read())
        genre = json.loads(open(genre_file, "r", encoding="utf-8").read())
        characters = json.loads(open(characters_file, "r", encoding="utf-8").read())
    except Exception as e:
        print(f"Error reading input files: {e}", file=sys.stderr)
        sys.exit(1)

    # Generate outline
    outline = generate_outline(segments, scenes, genre, characters, depth)

    # Output
    if output_file:
        with open(output_file, "w", encoding="utf-8") as f:
            f.write(outline)
        print(f"Outline generated: {output_file}")
        print(f"Title: {segments.get('title', 'Untitled')}")
        print(f"Depth: {depth}")
    else:
        print(outline)


if __name__ == "__main__":
    main()
