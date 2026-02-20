#!/usr/bin/env python3
"""
watcher.py - Simple file change logger for story-zoom

Watches story directories and logs changes to change-log.jsonl.
Does NO semantic understanding - just records what changed and when.
The LLM skill does all the thinking.

Usage:
  python watcher.py <project-path>
  python watcher.py <project-path> --log ./custom/change-log.jsonl
"""

import sys
import os
import json
import time
from datetime import datetime

WATCH_DIRS = ["pitch", "structure", "scenes", "entities", "manuscript"]
DEFAULT_LOG = "story-state/change-log.jsonl"


def show_usage():
    print("""
Story-Zoom File Watcher
=======================

Watches story directories and logs changes. Does no semantic analysis.

Usage:
  python watcher.py <project-path> [options]

Options:
  --log <path>    Custom log file location (default: story-state/change-log.jsonl)
  --help, -h      Show this help

Watched directories:
  pitch/          L1: tagline, logline, synopsis
  structure/      L2: outline, beats, acts
  scenes/         L3: scene files
  entities/       L4: characters, locations, items
  manuscript/     L5: actual prose

Example:
  python watcher.py ./my-novel
  python watcher.py ./my-novel --log ./logs/changes.jsonl
""")


def ensure_dir(path):
    dir_path = os.path.dirname(path)
    if dir_path:
        os.makedirs(dir_path, exist_ok=True)


def log_change(log_file, entry):
    ensure_dir(log_file)
    with open(log_file, "a", encoding="utf-8") as f:
        f.write(json.dumps(entry) + "\n")


def snapshot_dir(base_path, watch_paths):
    """Take a snapshot of all files with their modification times."""
    snapshot = {}
    for wp in watch_paths:
        for root, dirs, files in os.walk(wp):
            for fname in files:
                if fname.endswith(".md"):
                    full = os.path.join(root, fname)
                    try:
                        snapshot[full] = os.path.getmtime(full)
                    except OSError:
                        pass
    return snapshot


def main():
    args = sys.argv[1:]

    if "--help" in args or "-h" in args or len(args) == 0:
        show_usage()
        sys.exit(0)

    # Parse arguments
    log_index = args.index("--log") if "--log" in args else -1
    custom_log = args[log_index + 1] if log_index != -1 else None

    # Find project path (first non-flag argument)
    skip_indices = set()
    if log_index != -1:
        skip_indices.add(log_index)
        skip_indices.add(log_index + 1)

    project_path = None
    for i, arg in enumerate(args):
        if not arg.startswith("--") and i not in skip_indices:
            project_path = arg
            break

    if not project_path:
        print("Error: Project path required", file=sys.stderr)
        sys.exit(1)

    # Resolve paths
    base_path = project_path.rstrip("/")
    log_file = custom_log or f"{base_path}/{DEFAULT_LOG}"

    # Build watch paths (only directories that exist)
    watch_paths = []
    for d in WATCH_DIRS:
        full_path = f"{base_path}/{d}"
        if os.path.isdir(full_path):
            watch_paths.append(full_path)

    if not watch_paths:
        print(f"Error: No story directories found in {base_path}", file=sys.stderr)
        print(f"Expected directories: {', '.join(WATCH_DIRS)}", file=sys.stderr)
        sys.exit(1)

    short_names = [p.replace(base_path + "/", "") for p in watch_paths]
    print("Story-Zoom Watcher")
    print("==================")
    print(f"Project: {base_path}")
    print(f"Log file: {log_file}")
    print(f"Watching: {', '.join(short_names)}")
    print("\nPress Ctrl+C to stop.\n")

    # Polling-based watcher
    prev_snapshot = snapshot_dir(base_path, watch_paths)

    try:
        while True:
            time.sleep(2)
            current = snapshot_dir(base_path, watch_paths)

            # Detect creates and modifies
            for path, mtime in current.items():
                if path not in prev_snapshot:
                    kind = "create"
                elif mtime != prev_snapshot[path]:
                    kind = "modify"
                else:
                    continue

                entry = {
                    "file": path.replace(base_path + "/", "").replace("\\", "/"),
                    "time": datetime.now().isoformat(),
                    "kind": kind,
                }
                log_change(log_file, entry)
                print(f"[{entry['time']}] {entry['kind']}: {entry['file']}")

            # Detect removes
            for path in prev_snapshot:
                if path not in current:
                    entry = {
                        "file": path.replace(base_path + "/", "").replace("\\", "/"),
                        "time": datetime.now().isoformat(),
                        "kind": "remove",
                    }
                    log_change(log_file, entry)
                    print(f"[{entry['time']}] {entry['kind']}: {entry['file']}")

            prev_snapshot = current

    except KeyboardInterrupt:
        print("\nStopped.")


if __name__ == "__main__":
    main()
