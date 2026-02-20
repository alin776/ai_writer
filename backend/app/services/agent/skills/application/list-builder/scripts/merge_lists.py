#!/usr/bin/env python3
"""
merge_lists.py - Merge multiple JSON list files

Combines multiple JSON list sources, deduplicates case-insensitively
(keeping the first occurrence's casing), sorts alphabetically, and
outputs the merged result.

Usage:
  python merge_lists.py source1.json source2.json
  python merge_lists.py source1.json source2.json --output combined.json
  python merge_lists.py source1.json source2.json --json
"""

import sys
import os
import json

# Ensure UTF-8 output on all platforms
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")
if hasattr(sys.stderr, "reconfigure"):
    sys.stderr.reconfigure(encoding="utf-8")


def load_list_file(file_path):
    """Load a JSON file and extract list items.

    Supports:
      - JSON array: returns all items directly
      - JSON object: concatenates all array values

    Returns:
        (items, source_info) or (None, error_message)
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.loads(f.read())
    except Exception as e:
        return None, f"Error reading {file_path}: {e}"

    items = []
    if isinstance(data, list):
        items = [str(item) for item in data]
    elif isinstance(data, dict):
        for key, value in data.items():
            if isinstance(value, list):
                items.extend(str(item) for item in value)
    else:
        return None, f"Error: {file_path} must contain a JSON array or object"

    return items, None


def merge_items(all_items):
    """Merge and deduplicate items case-insensitively.

    Keeps the first occurrence's casing. Sorts alphabetically.

    Args:
        all_items: list of (source_file, items_list) tuples

    Returns:
        (merged_list, stats_dict)
    """
    seen = {}  # normalized -> original casing
    total_input = 0
    source_stats = []

    for source, items in all_items:
        count = len(items)
        total_input += count
        source_stats.append({'file': source, 'items': count})

        for item in items:
            normalized = item.lower().strip()
            if normalized and normalized not in seen:
                seen[normalized] = item.strip()

    merged = sorted(seen.values(), key=lambda x: x.lower())
    duplicates_removed = total_input - len(merged)

    stats = {
        'sources': source_stats,
        'totalInput': total_input,
        'uniqueItems': len(merged),
        'duplicatesRemoved': duplicates_removed,
    }

    return merged, stats


def format_report(merged, stats):
    """Format merge results as a human-readable report."""
    lines = []

    lines.append("LIST MERGE REPORT")
    lines.append("=" * 40)
    lines.append("")

    # Sources
    lines.append("SOURCES")
    lines.append("-" * 40)
    for src in stats['sources']:
        lines.append(f"  {src['file']}: {src['items']} items")
    lines.append("")

    # Stats
    lines.append("MERGE RESULTS")
    lines.append("-" * 40)
    lines.append(f"  Total input items:    {stats['totalInput']}")
    lines.append(f"  Duplicates removed:   {stats['duplicatesRemoved']}")
    lines.append(f"  Final unique items:   {stats['uniqueItems']}")
    lines.append("")

    # Preview
    if merged:
        preview_count = min(10, len(merged))
        lines.append(f"PREVIEW (first {preview_count} of {len(merged)})")
        lines.append("-" * 40)
        for item in merged[:preview_count]:
            lines.append(f"  - {item}")
        if len(merged) > preview_count:
            lines.append(f"  ... and {len(merged) - preview_count} more")
        lines.append("")

    return "\n".join(lines)


def show_usage():
    print("""
List Merger
============

Combines multiple JSON list files, deduplicates, and sorts.

Usage:
  python merge_lists.py <file1.json> [file2.json ...]
  python merge_lists.py <file1.json> [file2.json ...] --output combined.json
  python merge_lists.py <file1.json> [file2.json ...] --json

Input formats:
  - JSON array:  ["item1", "item2", ...]
  - JSON object: {"list1": [...], "list2": [...]}
    (all array values are concatenated)

Options:
  --output, -o   Write merged list to file (as JSON array)
  --json         Output full result as JSON to stdout
  --help, -h     Show this help

Deduplication is case-insensitive (keeps first occurrence's casing).

Example:
  python merge_lists.py professions-v1.json professions-v2.json --output professions.json
""")


def main():
    args = sys.argv[1:]

    if len(args) == 0 or '--help' in args or '-h' in args:
        show_usage()
        sys.exit(0)

    json_output = '--json' in args

    # Parse --output flag
    output_file = None
    for i, a in enumerate(args):
        if a in ('--output', '-o') and i + 1 < len(args):
            output_file = args[i + 1]
            break

    # Collect JSON file arguments (positional, non-flag)
    json_files = []
    skip_next = False
    for a in args:
        if skip_next:
            skip_next = False
            continue
        if a in ('--output', '-o'):
            skip_next = True
            continue
        if a.startswith('--'):
            continue
        if a.endswith('.json'):
            json_files.append(a)

    if not json_files:
        print("Error: No JSON files specified", file=sys.stderr)
        sys.exit(1)

    # Load all source files
    all_items = []
    for fpath in json_files:
        if not os.path.exists(fpath):
            print(f"Error: File not found: {fpath}", file=sys.stderr)
            sys.exit(1)
        items, error = load_list_file(fpath)
        if error:
            print(error, file=sys.stderr)
            sys.exit(1)
        all_items.append((fpath, items))

    # Merge
    merged, stats = merge_items(all_items)

    # Output
    if output_file:
        # Write merged list to file
        outdir = os.path.dirname(output_file)
        if outdir:
            os.makedirs(outdir, exist_ok=True)
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(merged, f, indent=2, ensure_ascii=False)
        print(f"Merged {stats['totalInput']} items -> {stats['uniqueItems']} unique items")
        print(f"Written to: {output_file}")
    elif json_output:
        output = {
            'merged': merged,
            'stats': stats,
        }
        print(json.dumps(output, indent=2, ensure_ascii=False))
    else:
        print(format_report(merged, stats))


if __name__ == '__main__':
    main()
