#!/usr/bin/env python3
"""
segment_book.py - Book Segmentation Script

Parses raw book text into chapters and scenes.
Detects chapters via regex patterns and scenes via break markers or POV shifts.

Usage:
  python segment_book.py book.txt
  python segment_book.py book.txt --output segments.json
  python segment_book.py book.txt --chapter-pattern "^CHAPTER"
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

# == DEFAULT PATTERNS ==

DEFAULT_CHAPTER_PATTERNS = [
    re.compile(r"^(Chapter|CHAPTER)\s+\d+", re.I),
    re.compile(r"^(Chapter|CHAPTER)\s+(One|Two|Three|Four|Five|Six|Seven|Eight|Nine|Ten|Eleven|Twelve|Thirteen|Fourteen|Fifteen|Sixteen|Seventeen|Eighteen|Nineteen|Twenty)", re.I),
    re.compile(r"^(PART|Part)\s+(ONE|TWO|THREE|I|II|III|IV|V|1|2|3|4|5)", re.I),
    re.compile(r"^\d+\s*$"),
    re.compile(r"^(PROLOGUE|EPILOGUE|Prologue|Epilogue)", re.I),
]

DEFAULT_SCENE_BREAK_PATTERNS = [
    re.compile(r"^\s*\*\s*\*\s*\*\s*$"),
    re.compile(r"^\s*#\s*$"),
    re.compile(r"^\s*---\s*$"),
    re.compile(r"^\s*\* \* \*\s*$"),
    re.compile(r"^\s*~+\s*$"),
]

# Common first names for POV detection
COMMON_NAMES = {
    "John", "Jane", "Michael", "Sarah", "David", "Emily", "James", "Emma",
    "Robert", "Anna", "William", "Maria", "Thomas", "Elizabeth", "Jack", "Kate",
    "Alex", "Sam", "Chris", "Taylor", "Jordan", "Morgan", "Casey", "Quinn",
}

# == UTILITIES ==


def count_words(text):
    return len([w for w in re.split(r"\s+", text) if len(w) > 0])


def extract_opening_text(lines, max_chars=150):
    text = ""
    for line in lines:
        trimmed = line.strip()
        if trimmed:
            text += (" " if text else "") + trimmed
            if len(text) >= max_chars:
                return text[:max_chars] + "..."
    return text


def detect_pov_candidate(text):
    # Look for proper nouns in first few sentences
    first_paragraph = re.split(r"\n\s*\n", text)[0] if text else text
    sentences = re.split(r"[.!?]+", first_paragraph)[:3]

    for sentence in sentences:
        # Look for capitalized words that might be names
        words = re.split(r"\s+", sentence)
        for word in words:
            cleaned = re.sub(r"[^a-zA-Z]", "", word)
            if len(cleaned) > 2 and re.match(r"^[A-Z][a-z]+$", cleaned):
                # Check if it's a common name
                if cleaned in COMMON_NAMES:
                    return cleaned

        # Look for "I" as first-person POV indicator
        if re.search(r"\bI\b", sentence):
            return "[First Person]"

    # Second pass: look for any capitalized word after common patterns
    pov_patterns = [
        re.compile(r"\b([A-Z][a-z]+)\s+(?:thought|felt|knew|wondered|watched|looked|stared)"),
        re.compile(r"\b([A-Z][a-z]+)'s\s+(?:eyes|heart|mind|stomach)"),
        re.compile(r"\b([A-Z][a-z]+)\s+(?:was|had been|stood|sat)"),
    ]

    for pattern in pov_patterns:
        match = pattern.search(first_paragraph)
        if match:
            return match.group(1)

    return None


def is_chapter_heading(line, patterns):
    trimmed = line.strip()
    if not trimmed:
        return False

    for pattern in patterns:
        if pattern.search(trimmed):
            return True
    return False


def is_scene_break(line, patterns):
    for pattern in patterns:
        if pattern.search(line):
            return True
    return False


def is_blank_line_cluster(lines, index, threshold=3):
    count = 0
    for i in range(index, min(len(lines), index + threshold + 2)):
        if lines[i].strip() == "":
            count += 1
        else:
            break
    return count >= threshold


# == CORE LOGIC ==

def segment_book(text, options=None):
    if options is None:
        options = {}

    chapter_patterns = options.get("chapterPatterns", DEFAULT_CHAPTER_PATTERNS)
    scene_break_patterns = options.get("sceneBreakPatterns", DEFAULT_SCENE_BREAK_PATTERNS)
    blank_line_threshold = options.get("blankLineThreshold", 3)

    lines = text.split("\n")
    chapters = []
    chapter_number = 0

    # First pass: find chapter boundaries
    chapter_boundaries = []

    for i in range(len(lines)):
        if is_chapter_heading(lines[i], chapter_patterns):
            chapter_boundaries.append({
                "line": i,
                "title": lines[i].strip(),
            })

    # If no chapters found, treat entire book as one chapter
    if len(chapter_boundaries) == 0:
        chapter_boundaries.append({
            "line": 0,
            "title": "Full Text",
        })

    # Process each chapter
    for chapter_idx in range(len(chapter_boundaries)):
        chapter_start = chapter_boundaries[chapter_idx]["line"]
        if chapter_idx < len(chapter_boundaries) - 1:
            chapter_end = chapter_boundaries[chapter_idx + 1]["line"] - 1
        else:
            chapter_end = len(lines) - 1

        chapter_number += 1
        scenes = []
        scene_start_line = chapter_start + 1  # Skip chapter heading

        # Find scene breaks within chapter
        i = scene_start_line
        while i <= chapter_end:
            is_break = is_scene_break(lines[i], scene_break_patterns) or \
                is_blank_line_cluster(lines, i, blank_line_threshold)

            if is_break or i == chapter_end:
                # End current scene
                scene_end_line = i - 1 if is_break else i

                if scene_end_line >= scene_start_line:
                    scene_lines = lines[scene_start_line:scene_end_line + 1]
                    scene_text = "\n".join(scene_lines)

                    if count_words(scene_text) > 10:  # Skip very short segments
                        scenes.append({
                            "id": f"ch{chapter_number}-s{len(scenes) + 1}",
                            "startLine": scene_start_line + 1,  # Convert to 1-based
                            "endLine": scene_end_line + 1,
                            "wordCount": count_words(scene_text),
                            "openingText": extract_opening_text(scene_lines),
                            "povCandidate": detect_pov_candidate(scene_text),
                        })

                # Start new scene after the break
                if is_break and is_blank_line_cluster(lines, i, blank_line_threshold):
                    # Skip past all blank lines
                    while i <= chapter_end and lines[i].strip() == "":
                        i += 1
                    scene_start_line = i
                    continue  # Don't increment i again
                else:
                    scene_start_line = i + 1

            i += 1

        chapter_lines = lines[chapter_start:chapter_end + 1]
        chapter_text = "\n".join(chapter_lines)

        if len(scenes) == 0:
            scenes = [{
                "id": f"ch{chapter_number}-s1",
                "startLine": chapter_start + 2,
                "endLine": chapter_end + 1,
                "wordCount": count_words(chapter_text),
                "openingText": extract_opening_text(chapter_lines[1:]),
                "povCandidate": detect_pov_candidate(chapter_text),
            }]

        chapters.append({
            "number": chapter_number,
            "title": chapter_boundaries[chapter_idx]["title"],
            "startLine": chapter_start + 1,
            "endLine": chapter_end + 1,
            "wordCount": count_words(chapter_text),
            "scenes": scenes,
        })

    total_words = sum(ch["wordCount"] for ch in chapters)
    total_scenes = sum(len(ch["scenes"]) for ch in chapters)

    return {
        "title": options.get("title", "Untitled"),
        "totalWords": total_words,
        "chapters": chapters,
        "metadata": {
            "totalChapters": len(chapters),
            "totalScenes": total_scenes,
            "avgSceneLength": round(total_words / total_scenes) if total_scenes > 0 else 0,
            "segmentedAt": datetime.now().isoformat(),
        }
    }


# == CLI ==

def print_help():
    print("""Book Segmentation Script

Usage:
  python segment_book.py <book.txt> [options]

Options:
  --output <file>         Write output to JSON file (default: stdout)
  --chapter-pattern <rx>  Custom chapter detection regex
  --scene-break <marker>  Custom scene break marker (e.g., "***")
  --blank-threshold <n>   Number of blank lines to treat as scene break (default: 3)
  --title <title>         Book title for output metadata
  --help, -h              Show this help message

Examples:
  python segment_book.py novel.txt
  python segment_book.py novel.txt --output segments.json
  python segment_book.py novel.txt --chapter-pattern "^CHAPTER"
""")


def main():
    args = sys.argv[1:]

    if "--help" in args or "-h" in args or len(args) == 0:
        print_help()
        sys.exit(0)

    # Parse arguments
    input_file = ""
    output_file = ""
    custom_chapter_pattern = None
    custom_scene_break = ""
    blank_threshold = 3
    title = ""

    skip_indices = set()

    for i in range(len(args)):
        if i in skip_indices:
            continue

        if args[i] == "--output" and i + 1 < len(args):
            output_file = args[i + 1]
            skip_indices.add(i + 1)
        elif args[i] == "--chapter-pattern" and i + 1 < len(args):
            custom_chapter_pattern = re.compile(args[i + 1], re.I)
            skip_indices.add(i + 1)
        elif args[i] == "--scene-break" and i + 1 < len(args):
            custom_scene_break = args[i + 1]
            skip_indices.add(i + 1)
        elif args[i] == "--blank-threshold" and i + 1 < len(args):
            try:
                blank_threshold = int(args[i + 1])
            except ValueError:
                blank_threshold = 3
            skip_indices.add(i + 1)
        elif args[i] == "--title" and i + 1 < len(args):
            title = args[i + 1]
            skip_indices.add(i + 1)
        elif not args[i].startswith("--") and not input_file:
            input_file = args[i]

    if not input_file:
        print("Error: no input file provided", file=sys.stderr)
        sys.exit(1)

    # Read input file
    try:
        text = open(input_file, "r", encoding="utf-8").read()
    except Exception as e:
        print(f"Error reading file: {e}", file=sys.stderr)
        sys.exit(1)

    # Infer title from filename if not provided
    if not title:
        basename = os.path.basename(input_file)
        title = re.sub(r"\.[^.]+$", "", basename) or "Untitled"

    # Build options
    options = {
        "title": title,
        "blankLineThreshold": blank_threshold,
    }

    if custom_chapter_pattern:
        options["chapterPatterns"] = [custom_chapter_pattern] + DEFAULT_CHAPTER_PATTERNS

    if custom_scene_break:
        escaped_break = re.escape(custom_scene_break)
        options["sceneBreakPatterns"] = [
            re.compile(f"^\\s*{escaped_break}\\s*$"),
        ] + DEFAULT_SCENE_BREAK_PATTERNS

    # Segment the book
    result = segment_book(text, options)

    # Output
    json_output = json.dumps(result, indent=2, ensure_ascii=False)

    if output_file:
        with open(output_file, "w", encoding="utf-8") as f:
            f.write(json_output)
        print(f"Segmentation complete: {result['metadata']['totalChapters']} chapters, {result['metadata']['totalScenes']} scenes")
        print(f"Output written to: {output_file}")
    else:
        print(json_output)


if __name__ == "__main__":
    main()
