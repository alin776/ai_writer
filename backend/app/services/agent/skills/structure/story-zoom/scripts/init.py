#!/usr/bin/env python3
"""
init.py - Initialize story-state directory for a story project

Creates the story-state/ directory structure and initial files.
Also creates the standard story directory structure if it doesn't exist.

Usage:
  python init.py [project-path]
"""

import sys
import os
import json
from datetime import datetime

STORY_DIRS = ["pitch", "structure", "scenes", "entities", "manuscript"]


def show_usage():
    print("""
Story-Zoom Initializer
======================

Creates story-state/ directory and optionally the standard story structure.

Usage:
  python init.py [project-path]

If no path provided, initializes in current directory.

Creates:
  story-state/
    change-log.jsonl    Append-only change record
    state.md            LLM-maintained dashboard
    last-review.json    Timestamp of last LLM review

Optionally creates (if missing):
  pitch/                L1: tagline, logline, synopsis
  structure/            L2: outline, beats, acts
  scenes/               L3: scene files
  entities/             L4: characters, locations, items
  manuscript/           L5: actual prose

Example:
  python init.py ./my-novel
""")


def dir_exists(path):
    return os.path.isdir(path)


def init_project(project_path):
    base_path = project_path.rstrip("/")
    project_name = os.path.basename(base_path) or "Untitled Project"

    info = {
        "name": project_name,
        "path": base_path,
        "existing_dirs": [],
        "created_dirs": [],
    }

    # Create base directory if needed
    os.makedirs(base_path, exist_ok=True)

    # Check which story directories exist
    for d in STORY_DIRS:
        full_path = f"{base_path}/{d}"
        if dir_exists(full_path):
            info["existing_dirs"].append(d)

    # Create story-state directory
    story_state_path = f"{base_path}/story-state"
    os.makedirs(story_state_path, exist_ok=True)
    info["created_dirs"].append("story-state")

    # Create initial change-log.jsonl (empty)
    change_log_path = f"{story_state_path}/change-log.jsonl"
    if not os.path.exists(change_log_path):
        with open(change_log_path, "w", encoding="utf-8") as f:
            f.write("")

    # Create initial last-review.json
    last_review_path = f"{story_state_path}/last-review.json"
    if not os.path.exists(last_review_path):
        last_review = {
            "timestamp": datetime.now().isoformat(),
            "note": "Initial setup - baseline established",
        }
        with open(last_review_path, "w", encoding="utf-8") as f:
            json.dump(last_review, f, indent=2)

    # Create initial state.md
    state_path = f"{story_state_path}/state.md"
    if not os.path.exists(state_path):
        now_iso = datetime.now().isoformat()
        today = now_iso.split("T")[0]
        existing = info["existing_dirs"]

        state_content = f"""# Story State: {project_name}

**Last Review:** {now_iso}
**Health:** Green (newly initialized)

## Level Summary

| Level | Directory | Files | Status | Notes |
|-------|-----------|-------|--------|-------|
| L1 Pitch | pitch/ | - | - | {"Exists" if "pitch" in existing else "Not created"} |
| L2 Structure | structure/ | - | - | {"Exists" if "structure" in existing else "Not created"} |
| L3 Scenes | scenes/ | - | - | {"Exists" if "scenes" in existing else "Not created"} |
| L4 Entities | entities/ | - | - | {"Exists" if "entities" in existing else "Not created"} |
| L5 Manuscript | manuscript/ | - | - | {"Exists" if "manuscript" in existing else "Not created"} |

## Active Concerns

None - freshly initialized.

## Recent Resolutions

- [{today}] Initialized story-state tracking

## Next Steps

1. Start the watcher daemon: `python scripts/watcher.py {base_path}`
2. Create story files in the appropriate directories
3. Run `/story-zoom review` periodically to check for drift
"""
        with open(state_path, "w", encoding="utf-8") as f:
            f.write(state_content)

    return info


def main():
    args = sys.argv[1:]

    if "--help" in args or "-h" in args:
        show_usage()
        sys.exit(0)

    project_path = args[0] if args else "."

    print("Story-Zoom Initializer")
    print("======================\n")

    info = init_project(project_path)

    print(f"Project: {info['name']}")
    print(f"Path: {info['path']}")
    print("\nCreated:")
    print("  story-state/change-log.jsonl")
    print("  story-state/last-review.json")
    print("  story-state/state.md")

    if info["existing_dirs"]:
        print("\nExisting story directories:")
        for d in info["existing_dirs"]:
            print(f"  {d}/")

    missing_dirs = [d for d in STORY_DIRS if d not in info["existing_dirs"]]
    if missing_dirs:
        print("\nMissing story directories (create as needed):")
        for d in missing_dirs:
            print(f"  {d}/")

    print("\nNext steps:")
    print("  1. Create story directories as needed")
    print(f"  2. Start watcher: python scripts/watcher.py {info['path']}")
    print("  3. Use /story-zoom review to check synchronization")


if __name__ == "__main__":
    main()
