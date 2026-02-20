#!/usr/bin/env python3



"""
List Validator

Analyzes entropy lists for quality metrics:
- Size (is it large enough for good entropy?)
- Duplicates (any repeated items?)
- Item length (too short = vague, too long = unwieldy)
- Variety indicators

Usage:
  deno run --allow-read validate-list.py list.json
  deno run --allow-read validate-list.py data.json list_name
  deno run --allow-read validate-list.py list.json --json
"""

import sys
import os
import json
import re
import random
from datetime import date




def validateList(items: string[], listName: string): ValidationReport {
  # Find duplicates
  seen = new Set<string>();
  duplicates: string[] = [];
  for item in items) {
    normalized = item.lower().strip();
    if (seen.has(normalized)) {
      duplicates.append(item);
    }
    seen.add(normalized);
  }

  # Calculate lengths
  lengths = items.map((i) => i.length);
  avgLength = lengths.reduce((a, b) => a + b, 0) / lengths.length;
  minLength = min(...lengths);
  maxLength = max(...lengths);

  # Find problematic items
  shortItems = items.filter((i) => i.length < 10).slice(0, 5);
  longItems = items.filter((i) => i.length > 100).slice(0, 5);

  # Specificity score (based on ideal length range 20-60)
  idealItems = items.filter((i) => i.length >= 20 and i.length <= 60).length;
  specificityScore = round((idealItems / items.length) * 100);

  # Maturity level assessment
  uniqueCount = seen.size;
  maturityLevel: MaturityLevel;
  nextLevel: MaturityLevel | None;
  itemsNeededForNext: number;

  if (uniqueCount < 30) {
    maturityLevel = "starter";
    nextLevel = "functional";
    itemsNeededForNext = 30 - uniqueCount;
  } else if (uniqueCount < 75) {
    maturityLevel = "functional";
    nextLevel = "production";
    itemsNeededForNext = 75 - uniqueCount;
  } else if (uniqueCount < 150) {
    maturityLevel = "production";
    nextLevel = "comprehensive";
    itemsNeededForNext = 150 - uniqueCount;
  } else {
    maturityLevel = "comprehensive";
    nextLevel = None;
    itemsNeededForNext = 0;
  }

  # Generate issues and suggestions
  issues: string[] = [];
  suggestions: string[] = [];

  if (duplicates.length > 0) {
    issues.append(f"{duplicates.length} duplicate(s) found");
    suggestions.append("Remove duplicate entries");
  }

  if (maturityLevel == "starter") {
    issues.append(f"Starter level ({uniqueCount} items) - not production ready");
    suggestions.append(f"Add {itemsNeededForNext} more unique items to reach Functional level");
  } else if (maturityLevel == "functional") {
    suggestions.append(f"Add {itemsNeededForNext} more items to reach Production level");
  }

  if (specificityScore < 30) {
    issues.append(f"Low specificity score ({specificityScore}%) - items may be too vague or too complex");
    suggestions.append("Target item length of 20-60 characters for optimal specificity");
  }

  if (shortItems.length > items.length * 0.2) {
    issues.append("Many items are very short (< 10 chars)");
    suggestions.append("Short items may be too vague—add specificity");
  }

  if (longItems.length > items.length * 0.1) {
    issues.append("Some items are very long (> 100 chars)");
    suggestions.append("Long items may be unwieldy—consider splitting or simplifying");
  }

  if (avgLength < 15) {
    issues.append("Average item length is short");
    suggestions.append("Items may lack specificity needed to spark ideas");
  }

  return {
    listName,
    totalItems: items.length,
    uniqueItems: seen.size,
    duplicates,
    avgLength: round(avgLength * 10) / 10,
    minLength,
    maxLength,
    shortItems,
    longItems,
    specificityScore,
    maturityLevel,
    nextLevel,
    itemsNeededForNext,
    issues,
    suggestions,
  };
}

def formatReport(report: ValidationReport): string {
  lines: string[] = [];

  lines.append(f"# List Validation: {report.listName}\n");

  # Maturity level section
  maturityEmoji = {
    comprehensive: "★",
    production: "✓",
    functional: "~",
    starter: "⚠",
  }[report.maturityLevel];

  maturityDesc = {
    comprehensive: "Reference quality (150+)",
    production: "Production ready (75-150)",
    functional: "Usable but limited (30-75)",
    starter: "Quick example only (< 30)",
  }[report.maturityLevel];

  lines.append("## Maturity Level");
  lines.append(f"{maturityEmoji} **{report.maturityLevel.upper()}** - {maturityDesc}");
  lines.append(f"   {report.uniqueItems} unique items");
  if (report.nextLevel) {
    lines.append(f"   → {report.itemsNeededForNext} more items needed for {report.nextLevel}");
  }
  if (report.duplicates.length > 0) {
    lines.append(f"   ⚠ {report.duplicates.length} duplicates found");
  }
  lines.append("");

  # Specificity section
  specEmoji = report.specificityScore >= 50 ? "✓" : report.specificityScore >= 30 ? "~" : "⚠";
  lines.append("## Specificity");
  lines.append(f"{specEmoji} Score: {report.specificityScore}% (items in ideal 20-60 char range)");
  lines.append(f"   Average length: {report.avgLength} chars (range: {report.minLength}-{report.maxLength})");

  if (report.shortItems.length > 0) {
    lines.append(f"   Short items (< 10 chars): {report.shortItems.slice(0, 3).join(\", \")}{report.shortItems.length > 3 ? \"...\" : \"\"}");
  }
  if (report.longItems.length > 0) {
    lines.append(f"   Long items (> 100 chars): {report.longItems.length} found");
  }
  lines.append("");

  # Issues
  if (report.issues.length > 0) {
    lines.append("## Issues");
    for issue in report.issues) {
      lines.append(f"- ⚠ {issue}");
    }
    lines.append("");
  }

  # Suggestions
  if (report.suggestions.length > 0) {
    lines.append("## Suggestions");
    for suggestion in report.suggestions) {
      lines.append(f"- {suggestion}");
    }
    lines.append("");
  }

  # Summary
  if (report.issues.length == 0) {
    lines.append("## Assessment");
    lines.append("✓ List passes validation checks\n");
  }

  return lines.join("\n");
}

def main(): Promise<void> {
  args = sys.argv[1:];

  if (args.includes("--help") or args.includes("-h")) {
    print(f"List Validator - Check entropy list quality

Usage:
  deno run --allow-read validate-list.ts <file.json>
  deno run --allow-read validate-list.ts <file.json> <list_name>
  deno run --allow-read validate-list.ts <file.json> --json

If file contains a single array, validates that array.
If file contains an object with multiple lists, specify list_name or validate all.

Options:
  --json    Output as JSON
  --all     Validate all lists in file (default if no list_name given)
  --help    Show this help
");
    sys.exit(0);
  }

  jsonOutput = args.includes("--json");
  file = args.find((a) => a.endswith(".json"));
  listName = args.find((a) => !a.startswith("--") and !a.endswith(".json"));

  if (!file) {
    print("Error: No JSON file specified");
    sys.exit(1);
  }

  data: unknown;
  try {
    text = open(file, "r", encoding="utf-8").read();
    data = json.loads(text);
  } catch (e) {
    print(f"Error reading {file}: {e}");
    sys.exit(1);
  }

  reports: ValidationReport[] = [];

  if (Array.isArray(data)) {
    # Single array
    reports.append(validateList(data as string[], file));
  } else if (typeof data == "object" and data != None) {
    # Object with multiple lists
    obj = data as Record<string, string[]>;

    if (listName) {
      if (!obj[listName]) {
        print(f"Error: List \"{listName}\" not found in {file}");
        print(f"Available: {list(obj.keys()).join(\", \")}");
        sys.exit(1);
      }
      reports.append(validateList(obj[listName], listName));
    } else {
      # Validate all
      for ([name, items] of obj.items()) {
        if (Array.isArray(items)) {
          reports.append(validateList(items, name));
        }
      }
    }
  } else {
    print("Error: File must contain a JSON array or object");
    sys.exit(1);
  }

  if (jsonOutput) {
    print(json.dumps(reports, None, 2));
  } else {
    for report in reports) {
      print(formatReport(report));
      if (reports.length > 1) {
        print("---\n");
      }
    }
  }
}

main();


if __name__ == '__main__':
    main()
