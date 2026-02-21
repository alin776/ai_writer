#!/usr/bin/env python3
"""
add_entry.py - Add a new entry to the world bible

Creates a new entry from template with proper metadata.

Usage:
  python add_entry.py --bible ./world-bible --category character \
    --name "Character Name" --status proposed --contributor "Your Name"
"""

import sys
import os
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


CATEGORIES = [
    'character', 'characters',
    'location', 'locations',
    'faction', 'factions',
    'event', 'events',
    'rule', 'rules',
    'culture', 'cultures',
    'artifact', 'artifacts',
    'species',
]

CATEGORY_ALIASES = {
    'power_system': 'rule',
    'power_systems': 'rules',
    'magic_system': 'rule',
    'magic_systems': 'rules',
    'technology': 'rule',
    'item': 'artifact',
    'items': 'artifacts',
    'creature': 'species',
    'creatures': 'species',
    'organization': 'faction',
    'organizations': 'factions',
    'place': 'location',
    'places': 'locations',
}

STATUSES = ['established', 'proposed', 'deprecated', 'contradicted', 'speculative']


def get_date():
    """Return today's date as YYYY-MM-DD string."""
    return date.today().isoformat()


def slugify(name):
    """Convert a name to a filesystem-friendly slug (supports CJK characters)."""
    slug = name.lower()
    # Normalize common CJK middle dots to hyphens
    slug = slug.replace('\u00b7', '-').replace('\uff65', '-').replace('\u30fb', '-')
    # Keep word chars (letters, digits, underscore — Unicode-aware) and CJK ideographs
    slug = re.sub(r'[^\w\u4e00-\u9fff]+', '-', slug, flags=re.UNICODE)
    slug = re.sub(r'(^-|-$)', '', slug)
    # Fallback: if slug is empty after filtering, use a hash
    if not slug:
        import hashlib
        slug = hashlib.md5(name.encode('utf-8')).hexdigest()[:8]
    return slug


def normalize_category(category):
    """Normalize a category to its plural form."""
    singular = category[:-1] if category.endswith('s') else category
    plural = singular + 's'

    # Special case for species
    if singular == 'specie':
        return 'species'

    return plural


def get_status_symbol(status):
    """Return the symbol for a given canon status."""
    status_lower = status.lower()
    if status_lower == 'established':
        return '✓'
    elif status_lower == 'proposed':
        return '?'
    elif status_lower == 'deprecated':
        return '✗'
    elif status_lower == 'contradicted':
        return '⚠'
    elif status_lower == 'speculative':
        return '~'
    else:
        return '?'


def generate_entry(options):
    """Generate an entry markdown file from options dict."""
    today = get_date()
    status_cap = options['status'][0].upper() + options['status'][1:]
    category_cap = options['category'][0].upper() + options['category'][1:]

    return f"""# {options['name']}

**Canon Status:** {status_cap}
**Category:** {category_cap}
**Created:** {today}
**Last Updated:** {today}
**Contributors:** {options['contributor']}

## Summary

[1-2 sentence overview for quick reference]

## Description

[Detailed information about this entry]

## Relationships

- **Related To:** [[Related Entry]]
<!-- Add more relationships as appropriate:
- **Located In:** [[Location]]
- **Member Of:** [[Faction]]
- **Contains:** [[Sub-entry]]
- **Preceded By:** [[Earlier Entry]]
- **See Also:** [[Related Entry]]
-->

## Key Facts

- [Key fact 1]
- [Key fact 2]
- [Key fact 3]

## Notes for Writers

[Guidance for using this element in stories. What should writers know? What's flexible vs. fixed?]

## Sources

- [Source work/document] (what was established)

## History

- {today}: Created by {options['contributor']}
"""


def generate_changelog_entry(options):
    """Generate a changelog line for the new entry."""
    return f"- **Created**: New {options['category']} entry \"{options['name']}\" ({options['contributor']})"


def add_entry(options):
    """Add a new entry to the world bible."""
    category = normalize_category(options['category'])
    slug = slugify(options['name'])
    entry_path = os.path.join(options['bible'], category, f"{slug}.md")
    changelog_path = os.path.join(options['bible'], 'meta', 'changelog.md')
    index_path = os.path.join(options['bible'], category, '_index.md')

    # Check if entry already exists
    if os.path.exists(entry_path):
        print(f"Error: Entry already exists at {entry_path}", file=sys.stderr)
        sys.exit(1)

    # Create the entry
    entry_content = generate_entry(options)
    _wt(entry_path, entry_content)
    print(f"Created: {entry_path}")

    # Update changelog
    try:
        with open(changelog_path, 'r', encoding='utf-8') as f:
            changelog = f.read()
        today = get_date()
        changelog_entry = generate_changelog_entry(options)

        # Find today's date section or create it
        date_header = f"## {today}"
        if date_header in changelog:
            # Add under existing date
            changelog = changelog.replace(
                f"## {today}\n",
                f"## {today}\n\n{changelog_entry}\n"
            )
        else:
            # Add new date section after the header
            header_end = changelog.find('\n## ')
            if header_end > -1:
                changelog = (
                    changelog[:header_end]
                    + f"\n## {today}\n\n{changelog_entry}\n"
                    + changelog[header_end:]
                )

        _wt(changelog_path, changelog)
        print(f"Updated: {changelog_path}")
    except Exception as e:
        print(f"Warning: Could not update changelog: {e}", file=sys.stderr)

    # Update index
    try:
        with open(index_path, 'r', encoding='utf-8') as f:
            index = f.read()
        status_symbol = get_status_symbol(options['status'])
        new_row = f"| [[{options['name']}]] | {status_symbol} | [Add summary] |"

        # Replace "no entries" row or add to table
        if '*No entries yet*' in index:
            index = index.replace('| *No entries yet* | | |', new_row)
        else:
            # Add before the "Adding New" section
            table_end = index.rfind('\n\n## Adding')
            if table_end > -1:
                index = index[:table_end] + '\n' + new_row + index[table_end:]

        _wt(index_path, index)
        print(f"Updated: {index_path}")
    except Exception as e:
        print(f"Warning: Could not update index: {e}", file=sys.stderr)

    print(f"""
Entry created successfully!

Next steps:
1. Edit {entry_path} to fill in details
2. Add wiki-links to related entries
3. Update the summary in {index_path}
""")


def parse_args(args):
    """Parse command-line arguments into an options dict. Returns None on failure."""
    options = {
        'bible': './world-bible',
        'status': 'proposed',
        'contributor': 'Unknown',
        'category': None,
        'name': None,
    }

    i = 0
    while i < len(args):
        arg = args[i]
        if arg in ('--bible', '-b') and i + 1 < len(args):
            i += 1
            options['bible'] = args[i]
        elif arg in ('--category', '-c') and i + 1 < len(args):
            i += 1
            options['category'] = args[i]
        elif arg in ('--name', '-n') and i + 1 < len(args):
            i += 1
            options['name'] = args[i]
        elif arg in ('--status', '-s') and i + 1 < len(args):
            i += 1
            options['status'] = args[i]
        elif arg in ('--contributor', '--author', '-a') and i + 1 < len(args):
            i += 1
            options['contributor'] = args[i]
        i += 1

    if not options['category'] or not options['name']:
        return None

    cat = options['category'].lower()
    cat = CATEGORY_ALIASES.get(cat, cat)
    options['category'] = cat
    if cat not in CATEGORIES:
        print(f"Invalid category: {options['category']}", file=sys.stderr)
        valid = [c for c in CATEGORIES if not c.endswith('s')]
        print(f"Valid categories: {', '.join(valid)}", file=sys.stderr)
        print(f"Aliases also accepted: {', '.join(sorted(CATEGORY_ALIASES.keys()))}", file=sys.stderr)
        return None

    if options['status'].lower() not in STATUSES:
        print(f"Invalid status: {options['status']}", file=sys.stderr)
        print(f"Valid statuses: {', '.join(STATUSES)}", file=sys.stderr)
        return None

    return options


def show_usage():
    print("""
Add Entry to World Bible
========================

Creates a new entry from template.

Usage:
  python add_entry.py [options]

Options:
  --bible, -b       Path to world bible (default: ./world-bible)
  --category, -c    Entry category (required)
  --name, -n        Entry name (required)
  --status, -s      Canon status (default: proposed)
  --contributor, -a Contributor name (default: Unknown)

Categories:
  character, location, faction, event, rule, culture, artifact, species
  Aliases: power_system→rule, magic_system→rule, technology→rule,
           item→artifact, creature→species, organization→faction, place→location

Statuses:
  established, proposed, deprecated, contradicted, speculative

Example:
  python add_entry.py \\
    --bible ./my-world \\
    --category character \\
    --name "Elena Blackwood" \\
    --status proposed \\
    --contributor "jsmith"
""")


def main():
    args = sys.argv[1:]

    if len(args) == 0 or '--help' in args or '-h' in args:
        show_usage()
        sys.exit(0)

    options = parse_args(args)
    if not options:
        show_usage()
        sys.exit(1)

    try:
        add_entry(options)
    except Exception as e:
        print(f"Error adding entry: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == '__main__':
    main()
