#!/usr/bin/env python3
"""
check_conflicts.py - Scan world bible for potential conflicts

Identifies:
- Entries marked as contradicted
- Broken wiki-links
- Duplicate entry names
- Entries without sources

Usage:
  python check_conflicts.py ./world-bible
  python check_conflicts.py ./world-bible --json
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

# Compiled regex patterns
RE_HEADING = re.compile(r'^#\s+(.+)$', re.MULTILINE)
RE_WIKI_LINK = re.compile(r'\[\[([^\]|]+)(?:\|[^\]]+)?\]\]')
RE_EMPTY_SOURCES = re.compile(r'## Sources\s*\n\s*\n')


def scan_file(path, result):
    """Scan a single markdown file for issues."""
    try:
        with open(path, 'r', encoding='utf-8') as f:
            content = f.read()
    except Exception:
        return

    # Extract entry name from first heading
    name_match = RE_HEADING.search(content)
    if name_match:
        name = name_match.group(1).strip()
        if name not in result['entries']:
            result['entries'][name] = []
        result['entries'][name].append(path)

    # Check for contradicted status
    if ('**Canon Status:** Contradicted' in content or
            'Status:** \u26a0' in content):
        result['issues'].append({
            'type': 'contradiction',
            'file': path,
            'description': 'Entry is marked as contradicted - needs resolution',
            'severity': 'error',
        })

    # Extract wiki-links
    for match in RE_WIKI_LINK.finditer(content):
        result['links'].add(match.group(1).strip())

    # Check for missing sources
    if ('## Sources' in content and
            ('[Source work/document]' in content or
             RE_EMPTY_SOURCES.search(content))):
        result['issues'].append({
            'type': 'missing-source',
            'file': path,
            'description': 'Entry has no sources documented',
            'severity': 'warning',
        })

    # Check for unfilled template markers
    if ('[1-2 sentence overview' in content or
            '[Detailed information about' in content or
            '[Key fact' in content):
        result['issues'].append({
            'type': 'orphan',
            'file': path,
            'description': 'Entry has unfilled template sections',
            'severity': 'info',
        })

    result['files'] += 1


def walk_markdown_files(bible_path):
    """Walk directory tree and yield .md file paths, skipping _ prefixed files."""
    for root, dirs, files in os.walk(bible_path):
        # Skip hidden directories and node_modules
        dirs[:] = [d for d in dirs if not d.startswith('.') and d != 'node_modules']
        for fname in files:
            if fname.endswith('.md') and not fname.startswith('_'):
                yield os.path.join(root, fname)


def scan_world_bible(bible_path):
    """Scan the entire world bible for conflicts and issues."""
    result = {
        'files': 0,
        'entries': {},  # name -> list of file paths
        'links': set(),
        'issues': [],
    }

    for filepath in walk_markdown_files(bible_path):
        scan_file(filepath, result)

    # Check for duplicates
    for name, files in result['entries'].items():
        if len(files) > 1:
            result['issues'].append({
                'type': 'duplicate',
                'file': ', '.join(files),
                'description': f'Duplicate entry name "{name}" in multiple files',
                'severity': 'error',
            })

    # Check for broken links
    for link in result['links']:
        # Skip section links
        if '#' in link:
            continue

        # Check if link target exists
        if link not in result['entries']:
            result['issues'].append({
                'type': 'broken-link',
                'file': 'Multiple files',
                'description': f'Broken link: [[{link}]] - no entry with this name',
                'severity': 'warning',
            })

    return result


def format_report(result):
    """Format scan results as a human-readable report."""
    report = f"""
WORLD BIBLE CONFLICT CHECK
==========================

Files scanned: {result['files']}
Unique entries: {len(result['entries'])}
Wiki-links found: {len(result['links'])}

"""

    errors = [i for i in result['issues'] if i['severity'] == 'error']
    warnings = [i for i in result['issues'] if i['severity'] == 'warning']
    infos = [i for i in result['issues'] if i['severity'] == 'info']

    if len(errors) > 0:
        report += f"ERRORS ({len(errors)})\n{'=' * 40}\n\n"
        for issue in errors:
            report += f"[{issue['type'].upper()}] {issue['description']}\n"
            report += f"  File: {issue['file']}\n\n"

    if len(warnings) > 0:
        report += f"WARNINGS ({len(warnings)})\n{'=' * 40}\n\n"
        for issue in warnings:
            report += f"[{issue['type'].upper()}] {issue['description']}\n"
            report += f"  File: {issue['file']}\n\n"

    if len(infos) > 0:
        report += f"INFO ({len(infos)})\n{'=' * 40}\n\n"
        for issue in infos:
            report += f"[{issue['type'].upper()}] {issue['description']}\n"
            report += f"  File: {issue['file']}\n\n"

    if len(result['issues']) == 0:
        report += "No issues found.\n"
    else:
        report += f"""
SUMMARY
=======
Errors: {len(errors)}
Warnings: {len(warnings)}
Info: {len(infos)}
Total: {len(result['issues'])}
"""

    return report


def format_json(result):
    """Format scan results as JSON (converting set to list for serialization)."""
    output = {
        'files': result['files'],
        'uniqueEntries': len(result['entries']),
        'wikiLinks': len(result['links']),
        'issues': result['issues'],
    }
    return json.dumps(output, indent=2, ensure_ascii=False)


def show_usage():
    print("""
World Bible Conflict Check
==========================

Scans for potential conflicts and issues.

Usage:
  python check_conflicts.py <world-bible-path>
  python check_conflicts.py <world-bible-path> --json

Options:
  --json    Output results as JSON

Checks for:
  - Entries marked as contradicted
  - Broken wiki-links ([[Name]] with no matching entry)
  - Duplicate entry names
  - Missing source documentation
  - Unfilled template sections

Example:
  python check_conflicts.py ./world-bible
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
        if not a.startswith('--'):
            bible_path = a
            break

    if not bible_path:
        print("Error: No world bible path specified", file=sys.stderr)
        sys.exit(1)

    if not os.path.exists(bible_path):
        print(f"Error: Path not found: {bible_path}", file=sys.stderr)
        sys.exit(1)

    result = scan_world_bible(bible_path)

    if json_output:
        print(format_json(result))
    else:
        print(format_report(result))

    # Exit with error code if errors found
    error_count = len([i for i in result['issues'] if i['severity'] == 'error'])
    if error_count > 0:
        sys.exit(1)


if __name__ == '__main__':
    main()
