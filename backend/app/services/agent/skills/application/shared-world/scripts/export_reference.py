#!/usr/bin/env python3
"""
export_reference.py - Export world bible as a single reference document

Walks a world-bible directory and produces a portable reference document
containing all entries organized by category, with a table of contents.

Usage:
  python export_reference.py ./world-bible
  python export_reference.py ./world-bible --format txt
  python export_reference.py ./world-bible --json
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


CATEGORY_DESCRIPTIONS = {
    'characters': 'People and beings that inhabit this world.',
    'locations': 'Places in the world, from continents to individual buildings.',
    'factions': 'Organizations, governments, groups, and alliances.',
    'rules': 'How the world works - magic systems, technology, physics.',
    'culture': 'Beliefs, customs, languages, and traditions.',
    'artifacts': 'Significant objects, weapons, and items of power.',
    'species': 'Non-human beings, creatures, and races.',
}

CATEGORY_ORDER = list(CATEGORY_DESCRIPTIONS.keys())

# Compiled regex patterns
RE_HEADING = re.compile(r'^#\s+(.+)$', re.MULTILINE)
RE_STATUS = re.compile(r'\*\*Canon Status:\*\*\s*(\w+)')
RE_SUMMARY = re.compile(r'## Summary\s*\n+([^\n#]+)')
RE_DESCRIPTION = re.compile(
    r'## Description\s*\n+(.*?)(?=\n## |\Z)', re.DOTALL
)


def get_status_symbol(status):
    """Return the display symbol for a canon status."""
    lower = status.lower()
    if 'established' in lower:
        return '\u2713'
    if 'proposed' in lower:
        return '?'
    if 'deprecated' in lower:
        return '\u2717'
    if 'contradicted' in lower:
        return '\u26a0'
    if 'speculative' in lower:
        return '~'
    return '?'


def parse_entry_full(path):
    """Parse a markdown entry and extract name, status, summary, description."""
    try:
        with open(path, 'r', encoding='utf-8') as f:
            content = f.read()

        name_match = RE_HEADING.search(content)
        if not name_match:
            return None

        name = name_match.group(1).strip()

        status_match = RE_STATUS.search(content)
        status = status_match.group(1) if status_match else 'Proposed'

        summary_match = RE_SUMMARY.search(content)
        summary = summary_match.group(1).strip() if summary_match else ''
        if summary.startswith('[') or summary == '':
            summary = ''

        desc_match = RE_DESCRIPTION.search(content)
        description = desc_match.group(1).strip() if desc_match else ''
        if description.startswith('['):
            description = ''

        return {
            'name': name,
            'file': path,
            'status': status,
            'summary': summary,
            'description': description,
        }
    except Exception:
        return None


def collect_entries(bible_path):
    """Walk the world bible and collect entries grouped by category."""
    entries_by_category = {}

    for category in CATEGORY_ORDER:
        category_path = os.path.join(bible_path, category)
        if not os.path.isdir(category_path):
            continue

        entries = []
        for root, dirs, files in os.walk(category_path):
            dirs[:] = [d for d in dirs if not d.startswith('.')]
            for fname in files:
                if (fname.endswith('.md') and
                        not fname.startswith('_') and
                        fname != 'overview.md'):
                    filepath = os.path.join(root, fname)
                    entry = parse_entry_full(filepath)
                    if entry:
                        entries.append(entry)

        entries.sort(key=lambda e: e['name'].lower())
        if entries:
            entries_by_category[category] = entries

    return entries_by_category


def generate_toc(entries_by_category):
    """Generate a markdown table of contents."""
    lines = ["## Table of Contents\n"]
    total = 0
    for category in CATEGORY_ORDER:
        if category not in entries_by_category:
            continue
        entries = entries_by_category[category]
        cap = category[0].upper() + category[1:]
        lines.append(f"- **{cap}** ({len(entries)} entries)")
        for entry in entries:
            symbol = get_status_symbol(entry['status'])
            lines.append(f"  - {symbol} {entry['name']}")
        total += len(entries)
    lines.append(f"\n*Total entries: {total}*\n")
    return "\n".join(lines)


def format_markdown(entries_by_category, bible_name):
    """Format the full reference document as Markdown."""
    today = date.today().isoformat()
    parts = []

    parts.append(f"# {bible_name} \u2014 Reference Document\n")
    parts.append(f"*Generated: {today}*\n")

    # Table of contents
    parts.append(generate_toc(entries_by_category))
    parts.append("---\n")

    # Each category
    for category in CATEGORY_ORDER:
        if category not in entries_by_category:
            continue
        entries = entries_by_category[category]
        cap = category[0].upper() + category[1:]
        desc = CATEGORY_DESCRIPTIONS.get(category, '')

        parts.append(f"## {cap}\n")
        parts.append(f"*{desc}*\n")

        for entry in entries:
            symbol = get_status_symbol(entry['status'])
            parts.append(f"### {entry['name']}\n")
            parts.append(f"**Status:** {symbol} {entry['status']}\n")
            if entry['summary']:
                parts.append(f"**Summary:** {entry['summary']}\n")
            if entry['description']:
                parts.append(entry['description'] + "\n")
            parts.append("")  # blank line separator

        parts.append("---\n")

    return "\n".join(parts)


def format_text(entries_by_category, bible_name):
    """Format the full reference document as plain text."""
    today = date.today().isoformat()
    lines = []

    title = f"{bible_name} -- Reference Document"
    lines.append(title)
    lines.append("=" * len(title))
    lines.append(f"Generated: {today}\n")

    # Summary
    total = sum(len(v) for v in entries_by_category.values())
    lines.append(f"Total entries: {total}")
    lines.append(f"Categories: {len(entries_by_category)}\n")

    # Each category
    for category in CATEGORY_ORDER:
        if category not in entries_by_category:
            continue
        entries = entries_by_category[category]
        cap = category[0].upper() + category[1:]
        desc = CATEGORY_DESCRIPTIONS.get(category, '')

        lines.append(cap)
        lines.append("-" * len(cap))
        lines.append(desc + "\n")

        for entry in entries:
            symbol = get_status_symbol(entry['status'])
            lines.append(f"  {symbol} {entry['name']} [{entry['status']}]")
            if entry['summary']:
                lines.append(f"    {entry['summary']}")
            if entry['description']:
                # Indent description lines
                for dl in entry['description'].split('\n')[:3]:
                    if dl.strip():
                        lines.append(f"    {dl.strip()}")
            lines.append("")  # blank line

        lines.append("")

    return "\n".join(lines)


def show_usage():
    print("""
Export World Bible Reference
=============================

Generates a single-file reference document from a world bible.

Usage:
  python export_reference.py <world-bible-path>
  python export_reference.py <world-bible-path> --format txt
  python export_reference.py <world-bible-path> --json

Options:
  --format, -f    Output format: md (default) or txt
  --json          Output structured JSON instead of document
  --help, -h      Show this help

Example:
  python export_reference.py ./world-bible
  python export_reference.py ./world-bible --format txt
""")


def main():
    args = sys.argv[1:]

    if len(args) == 0 or '--help' in args or '-h' in args:
        show_usage()
        sys.exit(0)

    json_output = '--json' in args

    # Parse --format flag
    fmt = 'md'
    for i, a in enumerate(args):
        if a in ('--format', '-f') and i + 1 < len(args):
            fmt = args[i + 1].lower()
            break

    if fmt not in ('md', 'txt'):
        print(f"Error: Unknown format '{fmt}'. Use 'md' or 'txt'.", file=sys.stderr)
        sys.exit(1)

    # Find the bible path (first non-flag arg)
    bible_path = None
    skip_next = False
    for a in args:
        if skip_next:
            skip_next = False
            continue
        if a in ('--format', '-f'):
            skip_next = True
            continue
        if not a.startswith('--'):
            bible_path = a
            break

    if not bible_path:
        print("Error: No world bible path specified", file=sys.stderr)
        sys.exit(1)

    if not os.path.exists(bible_path):
        print(f"Error: Path not found: {bible_path}", file=sys.stderr)
        sys.exit(1)

    # Derive bible name from directory name
    bible_name = os.path.basename(os.path.abspath(bible_path))
    bible_name = bible_name.replace('-', ' ').replace('_', ' ').title()

    entries_by_category = collect_entries(bible_path)

    if json_output:
        total = sum(len(v) for v in entries_by_category.values())
        output = {
            'bibleName': bible_name,
            'generatedDate': date.today().isoformat(),
            'totalEntries': total,
            'categories': {},
        }
        for cat, entries in entries_by_category.items():
            output['categories'][cat] = {
                'description': CATEGORY_DESCRIPTIONS.get(cat, ''),
                'count': len(entries),
                'entries': entries,
            }
        print(json.dumps(output, indent=2, ensure_ascii=False))
    else:
        if fmt == 'txt':
            print(format_text(entries_by_category, bible_name))
        else:
            print(format_markdown(entries_by_category, bible_name))


if __name__ == '__main__':
    main()
