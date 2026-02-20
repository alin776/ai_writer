#!/usr/bin/env python3
"""
build_index.py - Rebuild index files from entries

Scans all entries in a category and regenerates the _index.md file.

Usage:
  python build_index.py ./world-bible
  python build_index.py ./world-bible --category characters
  python build_index.py ./world-bible --json
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


def _wt(p, ct):
    """Write text to a file, creating parent directories as needed."""
    d = os.path.dirname(p)
    if d:
        os.makedirs(d, exist_ok=True)
    with open(p, 'w', encoding='utf-8') as fh:
        fh.write(ct)


CATEGORY_DESCRIPTIONS = {
    'characters': 'People and beings that inhabit this world.',
    'locations': 'Places in the world, from continents to individual buildings.',
    'factions': 'Organizations, governments, groups, and alliances.',
    'rules': 'How the world works - magic systems, technology, physics.',
    'culture': 'Beliefs, customs, languages, and traditions.',
    'artifacts': 'Significant objects, weapons, and items of power.',
    'species': 'Non-human beings, creatures, and races.',
}

# Compiled regex patterns
RE_HEADING = re.compile(r'^#\s+(.+)$', re.MULTILINE)
RE_STATUS = re.compile(r'\*\*Canon Status:\*\*\s*(\w+)')
RE_SUMMARY = re.compile(r'## Summary\s*\n+([^\n#]+)')


def get_status_symbol(status):
    """Return the display symbol for a canon status."""
    lower = status.lower()
    if 'established' in lower:
        return '✓'
    if 'proposed' in lower:
        return '?'
    if 'deprecated' in lower:
        return '✗'
    if 'contradicted' in lower:
        return '⚠'
    if 'speculative' in lower:
        return '~'
    return '?'


def get_date():
    """Return today's date as YYYY-MM-DD string."""
    return date.today().isoformat()


def parse_entry(path):
    """Parse a markdown entry file and extract name, status, and summary."""
    try:
        with open(path, 'r', encoding='utf-8') as f:
            content = f.read()

        # Extract name from first heading
        name_match = RE_HEADING.search(content)
        if not name_match:
            return None

        name = name_match.group(1).strip()

        # Extract status
        status_match = RE_STATUS.search(content)
        status = status_match.group(1) if status_match else 'Proposed'

        # Extract summary (first line after ## Summary)
        summary_match = RE_SUMMARY.search(content)
        summary = summary_match.group(1).strip() if summary_match else ''

        # Clean up placeholder text
        if summary.startswith('[') or summary == '':
            summary = '[Add summary]'

        # Truncate long summaries
        if len(summary) > 60:
            summary = summary[:57] + '...'

        return {
            'name': name,
            'file': path,
            'status': status,
            'summary': summary,
        }
    except Exception:
        return None


def build_category_index(bible_path, category):
    """Build the _index.md for a single category. Returns the entry count."""
    category_path = os.path.join(bible_path, category)
    index_path = os.path.join(category_path, '_index.md')

    # Check if category directory exists
    if not os.path.isdir(category_path):
        return 0

    # Collect all entries
    entries = []
    for fname in os.listdir(category_path):
        if (fname.endswith('.md') and
                not fname.startswith('_') and
                fname != 'overview.md'):
            filepath = os.path.join(category_path, fname)
            if os.path.isfile(filepath):
                entry = parse_entry(filepath)
                if entry:
                    entries.append(entry)

    # Sort alphabetically
    entries.sort(key=lambda e: e['name'].lower())

    # Generate index content
    description = CATEGORY_DESCRIPTIONS.get(category, f"Entries in the {category} category.")
    singular = category[:-1] if category.endswith('s') else category
    cap_category = category[0].upper() + category[1:]
    today = get_date()

    content = f"""# {cap_category}

{description}

## Entries

| Name | Status | Summary |
|------|--------|---------|
"""

    if len(entries) == 0:
        content += "| *No entries yet* | | |\n"
    else:
        for entry in entries:
            symbol = get_status_symbol(entry['status'])
            content += f"| [[{entry['name']}]] | {symbol} | {entry['summary']} |\n"

    content += f"""
## Adding New {cap_category}

1. Create file in this directory: "{singular}-name.md"
2. Use the entry template
3. Set category to "{cap_category}"
4. Add relationships to existing entries
5. Update this index
6. Note in [changelog](../meta/changelog.md)

---

*Last updated: {today}*
*Entries: {len(entries)}*
"""

    _wt(index_path, content)
    return len(entries)


def build_all_indexes(bible_path):
    """Build indexes for all categories. Returns dict of category -> count."""
    categories = list(CATEGORY_DESCRIPTIONS.keys())
    total_entries = 0
    results = {}

    print(f"Building indexes for {bible_path}...\n")

    for category in categories:
        count = build_category_index(bible_path, category)
        print(f"  {category}/_index.md: {count} entries")
        total_entries += count
        results[category] = count

    print(f"\nTotal entries indexed: {total_entries}")
    return results


def show_usage():
    print("""
Build World Bible Indexes
=========================

Regenerates _index.md files from entries.

Usage:
  python build_index.py <world-bible-path>
  python build_index.py <world-bible-path> --category <name>
  python build_index.py <world-bible-path> --json

Options:
  --category, -c    Only rebuild specific category index
  --json            Output results as JSON

Categories:
  characters, locations, factions, rules, culture, artifacts, species

Example:
  python build_index.py ./world-bible
  python build_index.py ./world-bible -c characters
""")


def main():
    args = sys.argv[1:]

    if len(args) == 0 or '--help' in args or '-h' in args:
        show_usage()
        sys.exit(0)

    json_output = '--json' in args

    # Find the bible path (first arg that isn't a flag)
    bible_path = None
    for a in args:
        if not a.startswith('--') and not a.startswith('-'):
            bible_path = a
            break

    if not bible_path:
        print("Error: No world bible path specified", file=sys.stderr)
        sys.exit(1)

    # Check if path exists
    if not os.path.exists(bible_path):
        print(f"Error: Path not found: {bible_path}", file=sys.stderr)
        sys.exit(1)

    # Check for specific category
    category = None
    for i, a in enumerate(args):
        if a in ('--category', '-c') and i + 1 < len(args):
            category = args[i + 1]
            break

    if category:
        print(f"Building index for {category}...")
        count = build_category_index(bible_path, category)
        if json_output:
            print(json.dumps({'category': category, 'entries': count}, indent=2))
        else:
            print(f"{category}/_index.md: {count} entries")
    else:
        results = build_all_indexes(bible_path)
        if json_output:
            print(json.dumps(results, indent=2))


if __name__ == '__main__':
    main()
