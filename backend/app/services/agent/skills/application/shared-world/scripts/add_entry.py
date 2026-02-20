#!/usr/bin/env python3



"""
add-entry.py - Add a new entry to the world bible

Creates a new entry from template with proper metadata.

Usage:
  deno run --allow-read --allow-write add-entry.py \
    --bible ./world-bible \
    --category character \
    --name "Character Name" \
    --status proposed \
    --contributor "Your Name"
"""

import sys
import os
import json
import re
import random
from datetime import date
def _wt(p, ct):
    d=os.path.dirname(p)
    if d: os.makedirs(d,exist_ok=True)
    with open(p,'w',encoding='utf-8') as fh: fh.write(ct)



CATEGORIES = [
  'character', 'characters',
  'location', 'locations',
  'faction', 'factions',
  'event', 'events',
  'rule', 'rules',
  'culture', 'cultures',
  'artifact', 'artifacts',
  'species',
];

STATUSES = ['established', 'proposed', 'deprecated', 'contradicted', 'speculative'];


def getDate(): string {
  return new Date().toISOString().split('T')[0];
}

def slugify(name: string): string {
  return name.lower().replace(/[^a-z0-9]+/g, '-').replace(/(^-|-$)/g, '');
}

def normalizeCategory(category: string): string {
  singular = category.endswith('s') ? category.slice(0, -1) : category;
  plural = singular + 's';

  # Special case for species
  if (singular == 'specie') return 'species';

  return plural;
}

def getStatusSymbol(status: string): string {
  switch (status.lower()) {
    case 'established': return '✓';
    case 'proposed': return '?';
    case 'deprecated': return '✗';
    case 'contradicted': return '⚠';
    case 'speculative': return '~';
    default: return '?';
  }
}

def generateEntry(options: EntryOptions): string {
  date = getDate();
  statusCapitalized = options.status.charAt(0).upper() + options.status.slice(1);
  categoryCapitalized = options.category.charAt(0).upper() + options.category.slice(1);

  return f"# {options.name}

**Canon Status:** {statusCapitalized}
**Category:** {categoryCapitalized}
**Created:** {date}
**Last Updated:** {date}
**Contributors:** {options.contributor}

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

- {date}: Created by {options.contributor}
";
}

def generateChangelogEntry(options: EntryOptions): string {
  date = getDate();
  return f"- **Created**: New {options.category} entry \"{options.name}\" ({options.contributor})";
}

async function addEntry(options: EntryOptions) {
  category = normalizeCategory(options.category);
  slug = slugify(options.name);
  entryPath = f"{options.bible}/{category}/{slug}.md";
  changelogPath = f"{options.bible}/meta/changelog.md";
  indexPath = f"{options.bible}/{category}/_index.md";

  # Check if entry already exists
  try {
    os.stat(entryPath);
    print(f"Error: Entry already exists at {entryPath}");
    sys.exit(1);
  } catch {
    # File doesn't exist, which is what we want
  }

  # Create the entry
  entryContent = generateEntry(options);
  _wt(entryPath, entryContent);
  print(f"Created: {entryPath}");

  # Update changelog
  try {
    changelog = open(changelogPath, "r", encoding="utf-8").read();
    date = getDate();
    changelogEntry = generateChangelogEntry(options);

    # Find today's date section or create it
    if (changelog.includes(f"## {date}")) {
      # Add under existing date
      changelog = changelog.replace(
        f"## {date}\n",
        f"## {date}\n\n{changelogEntry}\n"
      );
    } else {
      # Add new date section after the header
      headerEnd = changelog.indexOf('\n## ');
      if (headerEnd > -1) {
        changelog = changelog.slice(0, headerEnd) +
          f"\n## {date}\n\n{changelogEntry}\n" +
          changelog.slice(headerEnd);
      }
    }

    _wt(changelogPath, changelog);
    print(f"Updated: {changelogPath}");
  } catch (e) {
    print(f"Warning: Could not update changelog: {e}");
  }

  # Update index
  try {
    index = open(indexPath, "r", encoding="utf-8").read();
    statusSymbol = getStatusSymbol(options.status);
    newRow = f"| [[{options.name}]] | {statusSymbol} | [Add summary] |";

    # Replace "no entries" row or add to table
    if (index.includes('*No entries yet*')) {
      index = index.replace('| *No entries yet* | | |', newRow);
    } else {
      # Add before the last empty line of the table
      tableEnd = index.lastIndexOf('\n\n## Adding');
      if (tableEnd > -1) {
        index = index.slice(0, tableEnd) + '\n' + newRow + index.slice(tableEnd);
      }
    }

    _wt(indexPath, index);
    print(f"Updated: {indexPath}");
  } catch (e) {
    print(f"Warning: Could not update index: {e}");
  }

  print(f"
Entry created successfully!

Next steps:
1. Edit {entryPath} to fill in details
2. Add wiki-links to related entries
3. Update the summary in {indexPath}
");
}

def parseArgs(args: string[]): EntryOptions | None {
  options: Partial<EntryOptions> = {
    bible: './world-bible',
    status: 'proposed',
    contributor: 'Unknown',
  };

  for (i = 0; i < args.length; i++) {
    switch (args[i]) {
      case '--bible':
      case '-b':
        options.bible = args[++i];
        break;
      case '--category':
      case '-c':
        options.category = args[++i];
        break;
      case '--name':
      case '-n':
        options.name = args[++i];
        break;
      case '--status':
      case '-s':
        options.status = args[++i];
        break;
      case '--contributor':
      case '--author':
      case '-a':
        options.contributor = args[++i];
        break;
    }
  }

  if (!options.category or !options.name) {
    return None;
  }

  if (!CATEGORIES.includes(options.category.lower())) {
    print(f"Invalid category: {options.category}");
    print(f"Valid categories: {CATEGORIES.filter(c => !c.endswith('s')).join(', ')}");
    return None;
  }

  if (!STATUSES.includes(options.status!.lower())) {
    print(f"Invalid status: {options.status}");
    print(f"Valid statuses: {STATUSES.join(', ')}");
    return None;
  }

  return options as EntryOptions;
}

function showUsage() {
  print(f"
Add Entry to World Bible
========================

Creates a new entry from template.

Usage:
  deno run --allow-read --allow-write add-entry.ts [options]

Options:
  --bible, -b       Path to world bible (default: ./world-bible)
  --category, -c    Entry category (required)
  --name, -n        Entry name (required)
  --status, -s      Canon status (default: proposed)
  --contributor, -a Contributor name (default: Unknown)

Categories:
  character, location, faction, event, rule, culture, artifact, species

Statuses:
  established, proposed, deprecated, contradicted, speculative

Example:
  deno run --allow-read --allow-write add-entry.ts \\
    --bible ./my-world \\
    --category character \\
    --name \"Elena Blackwood\" \\
    --status proposed \\
    --contributor \"jsmith\"
");
}

async function main() {
  args = sys.argv[1:];

  if (args.length == 0 or args.includes('--help') or args.includes('-h')) {
    showUsage();
    sys.exit(0);
  }

  options = parseArgs(args);
  if (!options) {
    showUsage();
    sys.exit(1);
  }

  try {
    await addEntry(options);
  } catch (e) {
    print('Error adding entry:', e);
    sys.exit(1);
  }
}

main();
