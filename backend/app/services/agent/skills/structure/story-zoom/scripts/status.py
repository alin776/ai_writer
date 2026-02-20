#!/usr/bin/env python3
"""
status.py - Display change log summary for story-zoom

Reads the change log and shows what's changed since the last review.
Useful for LLM to quickly understand what needs attention.

Usage:
  python status.py [project-path]
  python status.py [project-path] --all
  python status.py [project-path] --json
"""

import sys
import os
import json
from datetime import datetime


def show_usage():
    print("""
Story-Zoom Status
=================

Shows changes since last review.

Usage:
  python status.py [project-path] [options]

Options:
  --all       Show all changes, not just since last review
  --json      Output as JSON (useful for LLM processing)
  --help, -h  Show this help

Example:
  python status.py ./my-novel
  python status.py ./my-novel --json
""")


def get_level(file_path):
    dir_name = file_path.split("/")[0]
    level_map = {
        "pitch": "L1 Pitch",
        "structure": "L2 Structure",
        "scenes": "L3 Scenes",
        "entities": "L4 Entities",
        "manuscript": "L5 Manuscript",
    }
    return level_map.get(dir_name, "Unknown")


def read_change_log(path):
    try:
        with open(path, "r", encoding="utf-8") as f:
            content = f.read().strip()
        if not content:
            return []
        lines = [line for line in content.split("\n") if line.strip()]
        return [json.loads(line) for line in lines]
    except (FileNotFoundError, json.JSONDecodeError):
        return []


def read_last_review(path):
    try:
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return None


def get_status(project_path, show_all):
    base_path = project_path.rstrip("/")
    project_name = os.path.basename(base_path) or "Unknown"

    change_log_path = f"{base_path}/story-state/change-log.jsonl"
    last_review_path = f"{base_path}/story-state/last-review.json"

    all_changes = read_change_log(change_log_path)
    last_review = read_last_review(last_review_path)

    last_review_time = last_review["timestamp"] if last_review else "1970-01-01T00:00:00.000Z"

    # Filter changes since last review
    if show_all:
        recent_changes = all_changes
    else:
        recent_changes = [c for c in all_changes if c["time"] > last_review_time]

    # Group by level
    by_level = {}
    for change in recent_changes:
        level = get_level(change["file"])
        if level not in by_level:
            by_level[level] = []
        by_level[level].append(change)

    # Count by kind
    by_kind = {"create": 0, "modify": 0, "remove": 0}
    for change in recent_changes:
        kind = change.get("kind", "modify")
        if kind in by_kind:
            by_kind[kind] += 1

    return {
        "project": project_name,
        "lastReview": last_review_time,
        "changesSinceReview": len(recent_changes),
        "totalChanges": len(all_changes),
        "byLevel": by_level,
        "byKind": by_kind,
        "recentChanges": recent_changes[-20:],
    }


def format_status(status, show_all):
    lines = []

    lines.append(f"Story-Zoom Status: {status['project']}")
    lines.append("=" * 40)
    lines.append("")

    if not show_all:
        lines.append(f"Last Review: {status['lastReview']}")
        lines.append(f"Changes Since Review: {status['changesSinceReview']}")
    else:
        lines.append(f"Total Changes Logged: {status['totalChanges']}")

    lines.append("")

    if status["changesSinceReview"] == 0 and not show_all:
        lines.append("No changes since last review.")
        return "\n".join(lines)

    # By kind
    lines.append("By Type:")
    lines.append(f"  Created: {status['byKind']['create']}")
    lines.append(f"  Modified: {status['byKind']['modify']}")
    lines.append(f"  Removed: {status['byKind']['remove']}")
    lines.append("")

    # By level
    lines.append("By Level:")
    levels = ["L1 Pitch", "L2 Structure", "L3 Scenes", "L4 Entities", "L5 Manuscript"]
    for level in levels:
        entries = status["byLevel"].get(level, [])
        count = len(entries)
        if count > 0:
            lines.append(f"  {level}: {count} changes")
            for change in entries[-5:]:
                lines.append(f"    - [{change['kind']}] {change['file']}")
    lines.append("")

    # Recent changes
    if status["recentChanges"]:
        lines.append(f"Recent Changes (last {min(20, len(status['recentChanges']))}):")
        for change in status["recentChanges"][-10:]:
            date_part = change["time"].split("T")[0]
            lines.append(f"  [{date_part}] {change['kind']}: {change['file']}")

    return "\n".join(lines)


def main():
    args = sys.argv[1:]

    if "--help" in args or "-h" in args:
        show_usage()
        sys.exit(0)

    show_all = "--all" in args
    json_output = "--json" in args

    # Find project path
    project_path = "."
    for arg in args:
        if not arg.startswith("--"):
            project_path = arg
            break

    try:
        status = get_status(project_path, show_all)

        if json_output:
            print(json.dumps(status, indent=2))
        else:
            print(format_status(status, show_all))
    except Exception as e:
        print(f"Error reading story state: {e}", file=sys.stderr)
        print("\nMake sure story-state/ exists. Run init.py first.", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
