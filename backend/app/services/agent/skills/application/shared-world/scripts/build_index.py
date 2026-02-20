#!/usr/bin/env python3



"""
build-index.py - Rebuild index files from entries

Scans all entries in a category and regenerates the _index.md file.

Usage:
  deno run --allow-read --allow-write build-index.py ./world-bible
  deno run --allow-read --allow-write build-index.py ./world-bible --category characters
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




CATEGORY_DESCRIPTIONS: Record<string, string> = {
  characters: 'People and beings that inhabit this world.',
  locations: 'Places in the world, from continents to individual buildings.',
  factions: 'Organizations, governments, groups, and alliances.',
  rules: 'How the world works - magic systems, technology, physics.',
  culture: 'Beliefs, customs, languages, and traditions.',
  artifacts: 'Significant objects, weapons, and items of power.',
  species: 'Non-human beings, creatures, and races.',
};

def getStatusSymbol(status: string): string {
  lower = status.lower();
  if (lower.includes('established')) return '✓';
  if (lower.includes('proposed')) return '?';
  if (lower.includes('deprecated')) return '✗';
  if (lower.includes('contradicted')) return '⚠';
  if (lower.includes('speculative')) return '~';
  return '?';
}

def getDate(): string {
  return new Date().toISOString().split('T')[0];
}

def parseEntry(path: string): Promise<EntryInfo | None> {
  try {
    content = open(path, "r", encoding="utf-8").read();

    # Extract name from first heading
    nameMatch = content.match(/^#\s+(.+)$/m);
    if (!nameMatch) return None;

    name = nameMatch[1].strip();

    # Extract status
    statusMatch = content.match(/\*\*Canon Status:\*\*\s*(\w+)/);
    status = statusMatch ? statusMatch[1] : 'Proposed';

    # Extract summary (first line after ## Summary)
    summaryMatch = content.match(/## Summary\s*\n+([^\n#]+)/);
    summary = summaryMatch ? summaryMatch[1].strip() : '';

    # Clean up placeholder text
    if (summary.startswith('[') or summary == '') {
      summary = '[Add summary]';
    }

    # Truncate long summaries
    if (summary.length > 60) {
      summary = summary.slice(0, 57) + '...';
    }

    return {
      name,
      file: path,
      status,
      summary,
    };
  } catch {
    return None;
  }
}

def buildCategoryIndex(biblePath: string, category: string): Promise<number> {
  categoryPath = f"{biblePath}/{category}";
  indexPath = f"{categoryPath}/_index.md";

  # Check if category directory exists
  try {
    os.stat(categoryPath);
  } catch {
    return 0;
  }

  # Collect all entries
  entries: EntryInfo[] = [];

  for await (file of walk(categoryPath, {
    maxDepth: 1,
    exts: ['.md'],
  })) {
    if (file.isFile and !file.name.startswith('_') and file.name != 'overview.md') {
      entry = await parseEntry(file.path);
      if (entry) {
        entries.append(entry);
      }
    }
  }

  # Sort alphabetically
  entries.sort((a, b) => a.name.localeCompare(b.name));

  # Generate index content
  description = CATEGORY_DESCRIPTIONS[category] or f"Entries in the {category} category.";
  singular = category.endswith('s') ? category.slice(0, -1) : category;

  content = f"# {category.charAt(0).upper() + category.slice(1)}

{description}

## Entries

| Name | Status | Summary |
|------|--------|---------|
";

  if (entries.length == 0) {
    content += f"| *No entries yet* | | |\n";
  } else {
    for entry in entries) {
      symbol = getStatusSymbol(entry.status);
      content += f"| [[{entry.name}]] | {symbol} | {entry.summary} |\n";
    }
  }

  content += f"
## Adding New {category.charAt(0).upper() + category.slice(1)}

1. Create file in this directory: \"${singular}-name.md\f"
2. Use the entry template
3. Set category to \"{category.charAt(0).upper() + category.slice(1)}\"
4. Add relationships to existing entries
5. Update this index
6. Note in [changelog](../meta/changelog.md)

---

*Last updated: {getDate()}*
*Entries: {entries.length}*
";

  _wt(indexPath, content);
  return entries.length;
}

def buildAllIndexes(biblePath: string): Promise<void> {
  categories = list(CATEGORY_DESCRIPTIONS.keys());
  totalEntries = 0;

  print(f"Building indexes for {biblePath}...\n");

  for category in categories) {
    count = await buildCategoryIndex(biblePath, category);
    print(f"  {category}/_index.md: {count} entries");
    totalEntries += count;
  }

  print(f"\nTotal entries indexed: {totalEntries}");
}

function showUsage() {
  print(f"
Build World Bible Indexes
=========================

Regenerates _index.md files from entries.

Usage:
  deno run --allow-read --allow-write build-index.ts <world-bible-path>
  deno run --allow-read --allow-write build-index.ts <world-bible-path> --category <name>

Options:
  --category, -c    Only rebuild specific category index

Categories:
  characters, locations, factions, rules, culture, artifacts, species

Example:
  deno run --allow-read --allow-write build-index.ts ./world-bible
  deno run --allow-read --allow-write build-index.ts ./world-bible -c characters
");
}

async function main() {
  args = sys.argv[1:];

  if (args.length == 0 or args.includes('--help') or args.includes('-h')) {
    showUsage();
    sys.exit(0);
  }

  biblePath = args[0];

  # Check if path exists
  try {
    os.stat(biblePath);
  } catch {
    print(f"Error: Path not found: {biblePath}");
    sys.exit(1);
  }

  # Check for specific category
  categoryIndex = args.indexOf('--category');
  categoryIndexShort = args.indexOf('-c');
  catIdx = categoryIndex > -1 ? categoryIndex : categoryIndexShort;

  if (catIdx > -1 and args[catIdx + 1]) {
    category = args[catIdx + 1];
    print(f"Building index for {category}...");
    count = await buildCategoryIndex(biblePath, category);
    print(f"{category}/_index.md: {count} entries");
  } else {
    await buildAllIndexes(biblePath);
  }
}

main();
