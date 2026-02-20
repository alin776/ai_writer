#!/usr/bin/env python3
"""
link_validator.py - Validate wiki-links in a world bible

Checks that all [[wiki-links]] resolve to real entries. Reports broken
links with their source files, orphaned entries (nothing links to them),
and a link graph summary.

Usage:
  python link_validator.py ./world-bible
  python link_validator.py ./world-bible --json
"""

import sys
import os
import json
import re

# Ensure UTF-8 output on all platforms
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")
if hasattr(sys.stderr, "reconfigure"):
    sys.stderr.reconfigure(encoding="utf-8")


# Compiled regex patterns
RE_HEADING = re.compile(r'^#\s+(.+)$', re.MULTILINE)
RE_WIKI_LINK = re.compile(r'\[\[([^\]|]+)(?:\|[^\]]+)?\]\]')


def walk_markdown_files(bible_path):
    """Walk directory tree and yield .md file paths, skipping _ prefixed files."""
    for root, dirs, files in os.walk(bible_path):
        dirs[:] = [d for d in dirs if not d.startswith('.') and d != 'node_modules']
        for fname in files:
            if fname.endswith('.md') and not fname.startswith('_'):
                yield os.path.join(root, fname)


def scan_entries(bible_path):
    """Scan all markdown files to extract entry names and wiki-links.

    Returns:
        {
            'entries': {name: filepath},
            'links': [(source_file, target_name)],
            'files_scanned': int,
        }
    """
    entries = {}
    links = []
    files_scanned = 0

    for filepath in walk_markdown_files(bible_path):
        files_scanned += 1
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read()
        except Exception:
            continue

        # Extract entry name from first heading
        name_match = RE_HEADING.search(content)
        if name_match:
            name = name_match.group(1).strip()
            entries[name] = filepath

        # Extract wiki-links with source
        for match in RE_WIKI_LINK.finditer(content):
            target = match.group(1).strip()
            # Skip section-only links (e.g., [[#section]])
            if target.startswith('#'):
                continue
            # Strip section part (e.g., "Entry Name#section" -> "Entry Name")
            base_target = target.split('#')[0].strip()
            if base_target:
                links.append((filepath, base_target))

    return {
        'entries': entries,
        'links': links,
        'files_scanned': files_scanned,
    }


def validate_links(scan_result):
    """Validate all links and compute graph statistics.

    Returns:
        {
            'valid_links': [(source, target)],
            'broken_links': [(source, target)],
            'orphaned_entries': [name],
            'stats': {...},
            'link_graph': {name: {'inbound': int, 'outbound': int}},
        }
    """
    entries = scan_result['entries']
    links = scan_result['links']

    valid_links = []
    broken_links = []

    # Build link graph
    link_graph = {}
    for name in entries:
        link_graph[name] = {'inbound': 0, 'outbound': 0}

    # Track outbound per source file -> entry name mapping
    file_to_entry = {}
    for name, fpath in entries.items():
        file_to_entry[fpath] = name

    for source_file, target in links:
        if target in entries:
            valid_links.append((source_file, target))
            link_graph[target]['inbound'] += 1
            source_entry = file_to_entry.get(source_file)
            if source_entry and source_entry in link_graph:
                link_graph[source_entry]['outbound'] += 1
        else:
            broken_links.append((source_file, target))

    # Orphaned entries: entries with zero inbound links
    orphaned = [name for name, graph in link_graph.items()
                if graph['inbound'] == 0]
    orphaned.sort(key=str.lower)

    stats = {
        'files_scanned': scan_result['files_scanned'],
        'entry_count': len(entries),
        'total_links': len(links),
        'valid_count': len(valid_links),
        'broken_count': len(broken_links),
        'orphaned_count': len(orphaned),
    }

    return {
        'valid_links': valid_links,
        'broken_links': broken_links,
        'orphaned_entries': orphaned,
        'stats': stats,
        'link_graph': link_graph,
    }


def format_report(result):
    """Format validation results as a human-readable report."""
    stats = result['stats']
    lines = []

    lines.append("WIKI-LINK VALIDATION REPORT")
    lines.append("=" * 40)
    lines.append("")
    lines.append(f"Files scanned:    {stats['files_scanned']}")
    lines.append(f"Entries found:    {stats['entry_count']}")
    lines.append(f"Wiki-links found: {stats['total_links']}")
    lines.append(f"Valid links:      {stats['valid_count']}")
    lines.append(f"Broken links:     {stats['broken_count']}")
    lines.append(f"Orphaned entries: {stats['orphaned_count']}")
    lines.append("")

    # Broken links grouped by source file
    if result['broken_links']:
        lines.append("BROKEN LINKS")
        lines.append("-" * 40)
        # Group by source file
        by_source = {}
        for source, target in result['broken_links']:
            by_source.setdefault(source, []).append(target)
        for source in sorted(by_source.keys()):
            lines.append(f"\n  File: {source}")
            for target in sorted(by_source[source]):
                lines.append(f"    \u2717 [[{target}]] \u2014 no matching entry")
        lines.append("")

    # Orphaned entries
    if result['orphaned_entries']:
        lines.append("\nORPHANED ENTRIES (nothing links to these)")
        lines.append("-" * 40)
        for name in result['orphaned_entries']:
            lines.append(f"  \u26a0 {name}")
        lines.append("")

    # Link graph: top entries by inbound links
    graph = result['link_graph']
    if graph:
        ranked = sorted(graph.items(), key=lambda x: x[1]['inbound'], reverse=True)
        top = [r for r in ranked if r[1]['inbound'] > 0][:10]
        if top:
            lines.append("\nMOST REFERENCED ENTRIES")
            lines.append("-" * 40)
            for name, counts in top:
                lines.append(
                    f"  {name}: {counts['inbound']} inbound, "
                    f"{counts['outbound']} outbound"
                )
            lines.append("")

    # Overall status
    lines.append("\n" + "=" * 40)
    if stats['broken_count'] == 0:
        lines.append("\u2713 PASS \u2014 All wiki-links resolve correctly.")
    else:
        lines.append(
            f"\u2717 FAIL \u2014 {stats['broken_count']} broken link(s) found."
        )

    return "\n".join(lines)


def format_json_output(result):
    """Format validation results as JSON."""
    output = {
        'stats': result['stats'],
        'brokenLinks': [
            {'source': s, 'target': t}
            for s, t in result['broken_links']
        ],
        'orphanedEntries': result['orphaned_entries'],
        'linkGraph': result['link_graph'],
    }
    return json.dumps(output, indent=2, ensure_ascii=False)


def show_usage():
    print("""
Wiki-Link Validator
====================

Checks that all [[wiki-links]] in a world bible resolve to real entries.

Usage:
  python link_validator.py <world-bible-path>
  python link_validator.py <world-bible-path> --json

Options:
  --json    Output results as JSON
  --help    Show this help

Reports:
  - Broken links (grouped by source file)
  - Orphaned entries (entries nothing links to)
  - Link graph summary (most referenced entries)

Example:
  python link_validator.py ./world-bible
""")


def main():
    args = sys.argv[1:]

    if len(args) == 0 or '--help' in args or '-h' in args:
        show_usage()
        sys.exit(0)

    json_output = '--json' in args

    # Find the bible path (first non-flag arg)
    bible_path = None
    for a in args:
        if not a.startswith('--'):
            bible_path = a
            break

    if not bible_path:
        print("Error: No world bible path specified", file=sys.stderr)
        sys.exit(1)

    if not os.path.exists(bible_path):
        print(f"Error: Path not found: {bible_path}", file=sys.stderr)
        sys.exit(1)

    scan_result = scan_entries(bible_path)
    result = validate_links(scan_result)

    if json_output:
        print(format_json_output(result))
    else:
        print(format_report(result))

    # Exit with error code if broken links found
    if result['stats']['broken_count'] > 0:
        sys.exit(1)


if __name__ == '__main__':
    main()
