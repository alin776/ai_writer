#!/usr/bin/env python3
"""
init_world.py - Initialize a new world bible structure

Creates the full directory structure with template files
for a wiki-style world bible.

Usage:
  python init_world.py "World Name" [output-dir]

Example:
  python init_world.py "The Shattered Realms"
  python init_world.py "My World" ./worlds/my-world
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


DIRECTORIES = [
    'characters',
    'locations',
    'history',
    'history/eras',
    'history/events',
    'factions',
    'rules',
    'culture',
    'artifacts',
    'species',
    'meta',
]


def get_date():
    """Return today's date as YYYY-MM-DD string."""
    return date.today().isoformat()


def slugify(name):
    """Convert a name to a URL-friendly slug."""
    slug = name.lower()
    slug = re.sub(r'[^a-z0-9]+', '-', slug)
    slug = re.sub(r'(^-|-$)', '', slug)
    return slug


def generate_discovery(world_name):
    today = get_date()
    return f"""# {world_name} World Bible

Welcome to the canonical reference for {world_name}. This world bible contains all established facts, proposed additions, and organizational structure for our shared world.

## Quick Start

1. **New here?** Start with [Style Guide](meta/style-guide.md) for conventions
2. **Looking for something?** Check the category indexes below
3. **Adding content?** Use [Add Entry](#adding-entries) workflow
4. **Found a conflict?** Report in [Conflicts](meta/conflicts.md)

## Canon Status Guide

| Symbol | Status | Meaning |
|--------|--------|---------|
| ✓ | Established | Confirmed canon - treat as fact |
| ? | Proposed | Suggested - available but may change |
| ✗ | Deprecated | Superseded - don't use in new work |
| ⚠ | Contradicted | Conflicts exist - needs resolution |
| ~ | Speculative | Extrapolated - use cautiously |

See [Canon Status](canon-status.md) for current overview.

## Categories

### [Characters](characters/_index.md)
People and beings in the world.

### [Locations](locations/_index.md)
Places, from continents to rooms.

### [History](history/timeline.md)
Timeline, eras, and significant events.

### [Factions](factions/_index.md)
Organizations, governments, and groups.

### [Rules](rules/_index.md)
How the world works - magic, technology, physics.

### [Culture](culture/_index.md)
Beliefs, customs, languages, traditions.

### [Artifacts](artifacts/_index.md)
Significant objects.

### [Species](species/_index.md)
Non-human beings and creatures.

## Adding Entries

1. Create entry using appropriate template
2. Set status to **Proposed**
3. Add relationships (wiki-links)
4. Update relevant index
5. Note in [Changelog](meta/changelog.md)

Proposed entries become Established after review by canon authority.

## Recent Changes

See [Changelog](meta/changelog.md) for recent updates.

## Conflicts

See [Conflicts](meta/conflicts.md) for unresolved contradictions.

## Contributors

See [Contributors](meta/contributors.md) for who maintains what.

---

*Created: {today}*
"""


def generate_canon_status(world_name):
    today = get_date()
    return f"""# {world_name} Canon Status

Overview of canonical state across all categories.

## Status Summary

| Category | Established | Proposed | Deprecated | Contradicted |
|----------|-------------|----------|------------|--------------|
| Characters | 0 | 0 | 0 | 0 |
| Locations | 0 | 0 | 0 | 0 |
| History | 0 | 0 | 0 | 0 |
| Factions | 0 | 0 | 0 | 0 |
| Rules | 0 | 0 | 0 | 0 |
| Culture | 0 | 0 | 0 | 0 |
| Artifacts | 0 | 0 | 0 | 0 |
| Species | 0 | 0 | 0 | 0 |

## Recent Status Changes

*No changes yet.*

## Pending Review

Proposed entries awaiting establishment:

*None yet.*

---

*Last updated: {today}*
"""


def generate_index(category, description):
    singular = category[:-1] if category.endswith('s') else category
    cap_category = category[0].upper() + category[1:]
    today = get_date()
    return f"""# {cap_category}

{description}

## Entries

| Name | Status | Summary |
|------|--------|---------|
| *No entries yet* | | |

## Adding New {cap_category}

1. Create file in this directory: "{singular}-name.md"
2. Use the entry template
3. Set category to "{cap_category}"
4. Add relationships to existing entries
5. Update this index
6. Note in [changelog](../meta/changelog.md)

---

*Last updated: {today}*
"""


def generate_timeline():
    today = get_date()
    return f"""# Timeline

Chronological overview of the world's history.

## Eras

| Era | Period | Description |
|-----|--------|-------------|
| *Define eras as needed* | | |

## Major Events

See [events/](events/) for detailed event entries.

## Adding to Timeline

1. Create event entry in "events/" directory
2. Add to appropriate era section above
3. Update [changelog](../meta/changelog.md)

---

*Last updated: {today}*
"""


def generate_style_guide(world_name):
    today = get_date()
    return f"""# {world_name} Style Guide

Guidelines for contributing to this shared world.

## Naming Conventions

### Characters
- [Describe naming patterns, cultural influences]
- [Examples of good names]

### Places
- [Describe place naming conventions]
- [Linguistic patterns]

### Organizations
- [How factions/groups are named]

## Tone and Voice

### World Tone
[Describe the overall feel - dark, hopeful, gritty, whimsical, etc.]

### What Fits
- [Elements that belong]
- [Themes that work]

### What Doesn't Fit
- [Elements to avoid]
- [Tone mismatches]

## Content Boundaries

### Acceptable Content
- [What can be depicted]
- [How to handle sensitive topics]

### Requires Care
- [Topics needing sensitivity]
- [How to approach them]

### Off-Limits
- [Topics not allowed]
- [Hard boundaries]

## Formatting Standards

### Dates
- In-world calendar: [describe]
- Out-of-world: YYYY-MM-DD

### Measurements
- [Units used in-world]
- [Conversion notes if helpful]

### Capitalization
- [What gets capitalized]
- [Title conventions]

## Common Terms

| Term | Meaning | Usage |
|------|---------|-------|
| [Term] | [Definition] | [How to use] |

## Canon Authority

Primary canon authority: [Name/Role]

Decisions logged in: [conflicts.md](conflicts.md)

---

*Established: {today}*
"""


def generate_changelog(world_name):
    today = get_date()
    return f"""# {world_name} Changelog

Recent changes to the world bible.

## {today}

- **Created**: World bible initialized

---

## Adding to Changelog

When you make changes:
1. Add entry under today's date (or create new date header)
2. Use format: "- **Action**: Description (contributor)"
3. Actions: Created, Updated, Deprecated, Established, Resolved

Example:
```
- **Created**: New character entry for Elena (jsmith)
- **Updated**: Expanded magic system rules (kdoe)
- **Established**: Proposed faction "The Order" now canon (admin)
```
"""


def generate_conflicts():
    return """# Canon Conflicts

Unresolved contradictions requiring attention.

## Active Conflicts

*No conflicts currently.*

## Resolved Conflicts

*No resolutions yet.*

---

## Reporting Conflicts

When you find contradicting information:

1. Add to Active Conflicts section below
2. Include:
   - Both entries involved (with links)
   - Nature of contradiction
   - Source references
   - Date discovered

### Template:

```
### [Brief Description]
**Discovered:** [Date]
**Entries:** [[Entry 1]] vs [[Entry 2]]
**Conflict:** [Description of contradiction]
**Sources:**
- Entry 1: [source]
- Entry 2: [source]
**Status:** Awaiting resolution
```

## Resolving Conflicts

Canon authority resolves by:
1. Determining which source has priority
2. Either reconciling both or deprecating one
3. Moving to Resolved section with decision documented
"""


def generate_contributors():
    today = get_date()
    return f"""# Contributors

Who maintains what in this world bible.

## Canon Authority

- **Primary:** [Name] - final decisions on canon status

## Active Contributors

| Name | Areas | Since |
|------|-------|-------|
| [Name] | [Categories/areas] | {today} |

## Contribution History

See [changelog](changelog.md) for detailed contribution history.

---

## Becoming a Contributor

1. Read the [Style Guide](style-guide.md)
2. Familiarize yourself with existing canon
3. Start with Proposed entries in your area of interest
4. Contact canon authority for questions
"""


INDEX_DESCRIPTIONS = {
    'characters': 'People and beings that inhabit this world.',
    'locations': 'Places in the world, from continents to individual buildings.',
    'factions': 'Organizations, governments, groups, and alliances.',
    'rules': 'How the world works - magic systems, technology, physics.',
    'culture': 'Beliefs, customs, languages, and traditions.',
    'artifacts': 'Significant objects, weapons, and items of power.',
    'species': 'Non-human beings, creatures, and races.',
}


def init_world(world_name, output_dir):
    print(f'Initializing world bible for "{world_name}"...')
    print(f"Output directory: {output_dir}")

    # Create directories
    os.makedirs(output_dir, exist_ok=True)
    for d in DIRECTORIES:
        os.makedirs(os.path.join(output_dir, d), exist_ok=True)
        print(f"  Created: {d}/")

    # Create main files
    _wt(os.path.join(output_dir, "discovery.md"), generate_discovery(world_name))
    print("  Created: discovery.md")

    _wt(os.path.join(output_dir, "canon-status.md"), generate_canon_status(world_name))
    print("  Created: canon-status.md")

    # Create index files
    for category, description in INDEX_DESCRIPTIONS.items():
        _wt(
            os.path.join(output_dir, category, "_index.md"),
            generate_index(category, description),
        )
        print(f"  Created: {category}/_index.md")

    # Create history timeline
    _wt(os.path.join(output_dir, "history", "timeline.md"), generate_timeline())
    print("  Created: history/timeline.md")

    # Create meta files
    _wt(os.path.join(output_dir, "meta", "style-guide.md"), generate_style_guide(world_name))
    print("  Created: meta/style-guide.md")

    _wt(os.path.join(output_dir, "meta", "changelog.md"), generate_changelog(world_name))
    print("  Created: meta/changelog.md")

    _wt(os.path.join(output_dir, "meta", "conflicts.md"), generate_conflicts())
    print("  Created: meta/conflicts.md")

    _wt(os.path.join(output_dir, "meta", "contributors.md"), generate_contributors())
    print("  Created: meta/contributors.md")

    print("""
World bible initialized!

Next steps:
1. Edit meta/style-guide.md with your world's conventions
2. Add yourself to meta/contributors.md
3. Start adding entries to populate the bible
4. Use discovery.md as your navigation hub
""")


def show_usage():
    print("""
Initialize World Bible
======================

Creates a complete world bible directory structure.

Usage:
  python init_world.py "World Name" [output-dir]

Arguments:
  World Name    Name of your world (required)
  output-dir    Where to create the bible (default: ./world-bible)

Examples:
  python init_world.py "The Shattered Realms"
  python init_world.py "My World" ./worlds/my-world
""")


def main():
    args = sys.argv[1:]

    if len(args) == 0 or args[0] == '--help' or args[0] == '-h':
        show_usage()
        sys.exit(0)

    world_name = args[0]
    output_dir = args[1] if len(args) > 1 else './world-bible'

    try:
        init_world(world_name, output_dir)
    except Exception as e:
        print(f"Error initializing world bible: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == '__main__':
    main()
