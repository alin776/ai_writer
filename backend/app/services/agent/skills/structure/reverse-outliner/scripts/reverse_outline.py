#!/usr/bin/env python3
"""
Reverse Outline Orchestrator

Runs the full pipeline from book.txt to outline.md:
  book.txt -> segment -> analyze -> detect genre -> track characters -> generate outline

Usage:
  python reverse_outline.py book.txt
  python reverse_outline.py book.txt --output ./outlines/
"""

import sys
import os
import subprocess
import re


def run_script(script_name, args, description):
    print(f"\n[{description}]")
    script_dir = os.path.dirname(os.path.abspath(__file__))
    script_path = os.path.join(script_dir, script_name)

    result = subprocess.run(
        [sys.executable, script_path] + args,
        stdout=sys.stdout,
        stderr=sys.stderr,
    )

    if result.returncode != 0:
        raise RuntimeError(f"Script {script_name} failed with code {result.returncode}")


def infer_book_name(input_path):
    base = os.path.basename(input_path)
    name = re.sub(r"\.[^.]+$", "", base)
    name = re.sub(r"[^a-zA-Z0-9\-_]", "-", name)
    return name


def main():
    args = sys.argv[1:]

    if "--help" in args or "-h" in args or len(args) == 0:
        print("""Reverse Outline Orchestrator

Runs the complete reverse-outline pipeline:
  1. Segment book into chapters and scenes
  2. Analyze scene structure (Goal/Conflict/Disaster)
  3. Detect genre and map Key Moments
  4. Track character arcs
  5. Generate markdown outline

Usage:
  python reverse_outline.py <book.txt> [options]

Options:
  --output <dir>         Output directory (default: ./reverse-outlines/{book-name}/)
  --depth <level>        Analysis depth: quick, standard, detailed (default: standard)
  --protagonist <name>   Specify protagonist name (overrides detection)
  --genre <type>         Override genre detection
  --help, -h             Show this help message

Examples:
  python reverse_outline.py novel.txt
  python reverse_outline.py novel.txt --output ./outlines/
  python reverse_outline.py novel.txt --protagonist "Sarah"
""")
        sys.exit(0)

    # Parse arguments
    input_file = ""
    output_dir = ""
    depth = "standard"
    protagonist_name = ""
    genre_override = ""

    skip_indices = set()

    for i in range(len(args)):
        if i in skip_indices:
            continue
        if args[i] == "--output" and i + 1 < len(args):
            output_dir = args[i + 1]
            skip_indices.add(i + 1)
        elif args[i] == "--depth" and i + 1 < len(args):
            depth = args[i + 1]
            skip_indices.add(i + 1)
        elif args[i] == "--protagonist" and i + 1 < len(args):
            protagonist_name = args[i + 1]
            skip_indices.add(i + 1)
        elif args[i] == "--genre" and i + 1 < len(args):
            genre_override = args[i + 1]
            skip_indices.add(i + 1)
        elif not args[i].startswith("--") and not input_file:
            input_file = args[i]

    if not input_file:
        print("Error: No input file provided", file=sys.stderr)
        sys.exit(1)

    # Verify input file exists
    if not os.path.exists(input_file):
        print(f"Error: Input file not found: {input_file}", file=sys.stderr)
        sys.exit(1)

    # Set up output directory
    book_name = infer_book_name(input_file)
    if not output_dir:
        output_dir = f"./reverse-outlines/{book_name}"

    analysis_dir = os.path.join(output_dir, "analysis")
    os.makedirs(analysis_dir, exist_ok=True)

    print("=" * 60)
    print(f"Reverse Outline: {book_name}")
    print("=" * 60)
    print(f"Input: {input_file}")
    print(f"Output: {output_dir}")
    print(f"Depth: {depth}")

    # File paths
    segments_file = os.path.join(analysis_dir, "segments.json")
    scenes_file = os.path.join(analysis_dir, "scenes.json")
    genre_file = os.path.join(analysis_dir, "genre.json")
    characters_file = os.path.join(analysis_dir, "characters.json")
    outline_file = os.path.join(output_dir, "outline.md")

    try:
        # Step 1: Segment book
        run_script("segment_book.py", [
            input_file,
            "--output", segments_file,
            "--title", book_name,
        ], "Step 1/5: Segmenting book into chapters and scenes")

        # Step 2: Analyze scenes
        run_script("analyze_scene_batch.py", [
            segments_file,
            input_file,
            "--output", scenes_file,
            "--depth", depth,
        ], "Step 2/5: Analyzing scene structure (Goal/Conflict/Disaster)")

        # Step 3: Detect genre
        run_script("detect_genre.py", [
            input_file,
            "--output", genre_file,
        ], "Step 3/5: Detecting genre and mapping Key Moments")

        # Step 4: Track characters
        character_args = [
            segments_file,
            input_file,
            "--output", characters_file,
        ]
        if protagonist_name:
            character_args.extend(["--protagonist", protagonist_name])
        run_script("track_characters.py", character_args,
                   "Step 4/5: Tracking character arcs")

        # Step 5: Generate outline
        run_script("generate_outline.py", [
            "--segments", segments_file,
            "--scenes", scenes_file,
            "--genre", genre_file,
            "--characters", characters_file,
            "--output", outline_file,
            "--depth", depth,
        ], "Step 5/5: Generating markdown outline")

        print("\n" + "=" * 60)
        print("COMPLETE")
        print("=" * 60)
        print(f"\nOutput files:")
        print(f"  Outline:    {outline_file}")
        print(f"  Segments:   {segments_file}")
        print(f"  Scenes:     {scenes_file}")
        print(f"  Genre:      {genre_file}")
        print(f"  Characters: {characters_file}")
        print("")

    except RuntimeError as e:
        print(f"\nPipeline failed: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
