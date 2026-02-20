#!/usr/bin/env python3
"""
validate_list.py - List Validator

Analyzes entropy lists for quality metrics:
- Size (is it large enough for good entropy?)
- Duplicates (any repeated items?)
- Item length (too short = vague, too long = unwieldy)
- Variety indicators

Usage:
  python validate_list.py list.json
  python validate_list.py data.json list_name
  python validate_list.py list.json --json
"""

import sys
import os
import json

# Ensure UTF-8 output on all platforms
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")
if hasattr(sys.stderr, "reconfigure"):
    sys.stderr.reconfigure(encoding="utf-8")


def validate_list(items, list_name):
    """Validate a list of string items and return a report dict."""
    # Find duplicates
    seen = set()
    duplicates = []
    for item in items:
        normalized = item.lower().strip()
        if normalized in seen:
            duplicates.append(item)
        seen.add(normalized)

    # Calculate lengths
    lengths = [len(i) for i in items]
    avg_length = sum(lengths) / len(lengths) if lengths else 0
    min_length = min(lengths) if lengths else 0
    max_length = max(lengths) if lengths else 0

    # Find problematic items
    short_items = [i for i in items if len(i) < 10][:5]
    long_items = [i for i in items if len(i) > 100][:5]

    # Specificity score (based on ideal length range 20-60)
    ideal_items = len([i for i in items if 20 <= len(i) <= 60])
    specificity_score = round((ideal_items / len(items)) * 100) if items else 0

    # Maturity level assessment
    unique_count = len(seen)
    if unique_count < 30:
        maturity_level = "starter"
        next_level = "functional"
        items_needed_for_next = 30 - unique_count
    elif unique_count < 75:
        maturity_level = "functional"
        next_level = "production"
        items_needed_for_next = 75 - unique_count
    elif unique_count < 150:
        maturity_level = "production"
        next_level = "comprehensive"
        items_needed_for_next = 150 - unique_count
    else:
        maturity_level = "comprehensive"
        next_level = None
        items_needed_for_next = 0

    # Generate issues and suggestions
    issues = []
    suggestions = []

    if len(duplicates) > 0:
        issues.append(f"{len(duplicates)} duplicate(s) found")
        suggestions.append("Remove duplicate entries")

    if maturity_level == "starter":
        issues.append(f"Starter level ({unique_count} items) - not production ready")
        suggestions.append(f"Add {items_needed_for_next} more unique items to reach Functional level")
    elif maturity_level == "functional":
        suggestions.append(f"Add {items_needed_for_next} more items to reach Production level")

    if specificity_score < 30:
        issues.append(f"Low specificity score ({specificity_score}%) - items may be too vague or too complex")
        suggestions.append("Target item length of 20-60 characters for optimal specificity")

    if len(short_items) > len(items) * 0.2:
        issues.append("Many items are very short (< 10 chars)")
        suggestions.append("Short items may be too vague--add specificity")

    if len(long_items) > len(items) * 0.1:
        issues.append("Some items are very long (> 100 chars)")
        suggestions.append("Long items may be unwieldy--consider splitting or simplifying")

    if avg_length < 15:
        issues.append("Average item length is short")
        suggestions.append("Items may lack specificity needed to spark ideas")

    return {
        'listName': list_name,
        'totalItems': len(items),
        'uniqueItems': len(seen),
        'duplicates': duplicates,
        'avgLength': round(avg_length * 10) / 10,
        'minLength': min_length,
        'maxLength': max_length,
        'shortItems': short_items,
        'longItems': long_items,
        'specificityScore': specificity_score,
        'maturityLevel': maturity_level,
        'nextLevel': next_level,
        'itemsNeededForNext': items_needed_for_next,
        'issues': issues,
        'suggestions': suggestions,
    }


def format_report(report):
    """Format a validation report as human-readable text."""
    lines = []

    lines.append(f"# List Validation: {report['listName']}\n")

    # Maturity level section
    maturity_emoji = {
        'comprehensive': '\u2605',
        'production': '\u2713',
        'functional': '~',
        'starter': '\u26a0',
    }.get(report['maturityLevel'], '?')

    maturity_desc = {
        'comprehensive': 'Reference quality (150+)',
        'production': 'Production ready (75-150)',
        'functional': 'Usable but limited (30-75)',
        'starter': 'Quick example only (< 30)',
    }.get(report['maturityLevel'], 'Unknown')

    lines.append("## Maturity Level")
    lines.append(f"{maturity_emoji} **{report['maturityLevel'].upper()}** - {maturity_desc}")
    lines.append(f"   {report['uniqueItems']} unique items")
    if report['nextLevel']:
        lines.append(f"   -> {report['itemsNeededForNext']} more items needed for {report['nextLevel']}")
    if len(report['duplicates']) > 0:
        lines.append(f"   \u26a0 {len(report['duplicates'])} duplicates found")
    lines.append("")

    # Specificity section
    if report['specificityScore'] >= 50:
        spec_emoji = '\u2713'
    elif report['specificityScore'] >= 30:
        spec_emoji = '~'
    else:
        spec_emoji = '\u26a0'

    lines.append("## Specificity")
    lines.append(f"{spec_emoji} Score: {report['specificityScore']}% (items in ideal 20-60 char range)")
    lines.append(f"   Average length: {report['avgLength']} chars (range: {report['minLength']}-{report['maxLength']})")

    if len(report['shortItems']) > 0:
        preview = report['shortItems'][:3]
        suffix = "..." if len(report['shortItems']) > 3 else ""
        lines.append(f"   Short items (< 10 chars): {', '.join(preview)}{suffix}")
    if len(report['longItems']) > 0:
        lines.append(f"   Long items (> 100 chars): {len(report['longItems'])} found")
    lines.append("")

    # Issues
    if len(report['issues']) > 0:
        lines.append("## Issues")
        for issue in report['issues']:
            lines.append(f"- \u26a0 {issue}")
        lines.append("")

    # Suggestions
    if len(report['suggestions']) > 0:
        lines.append("## Suggestions")
        for suggestion in report['suggestions']:
            lines.append(f"- {suggestion}")
        lines.append("")

    # Summary
    if len(report['issues']) == 0:
        lines.append("## Assessment")
        lines.append("\u2713 List passes validation checks\n")

    return "\n".join(lines)


def main():
    args = sys.argv[1:]

    if '--help' in args or '-h' in args:
        print("""List Validator - Check entropy list quality

Usage:
  python validate_list.py <file.json>
  python validate_list.py <file.json> <list_name>
  python validate_list.py <file.json> --json

If file contains a single array, validates that array.
If file contains an object with multiple lists, specify list_name or validate all.

Options:
  --json    Output as JSON
  --all     Validate all lists in file (default if no list_name given)
  --help    Show this help
""")
        sys.exit(0)

    json_output = '--json' in args

    # Find the .json file argument
    file_path = None
    for a in args:
        if a.endswith('.json'):
            file_path = a
            break

    # Find list name argument (non-flag, non-json-file)
    list_name = None
    for a in args:
        if not a.startswith('--') and not a.endswith('.json'):
            list_name = a
            break

    if not file_path:
        print("Error: No JSON file specified", file=sys.stderr)
        sys.exit(1)

    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.loads(f.read())
    except Exception as e:
        print(f"Error reading {file_path}: {e}", file=sys.stderr)
        sys.exit(1)

    reports = []

    if isinstance(data, list):
        # Single array
        reports.append(validate_list(data, file_path))
    elif isinstance(data, dict):
        # Object with multiple lists
        if list_name:
            if list_name not in data:
                print(f'Error: List "{list_name}" not found in {file_path}', file=sys.stderr)
                print(f"Available: {', '.join(data.keys())}", file=sys.stderr)
                sys.exit(1)
            reports.append(validate_list(data[list_name], list_name))
        else:
            # Validate all
            for name, items in data.items():
                if isinstance(items, list):
                    reports.append(validate_list(items, name))
    else:
        print("Error: File must contain a JSON array or object", file=sys.stderr)
        sys.exit(1)

    if json_output:
        print(json.dumps(reports, indent=2, ensure_ascii=False))
    else:
        for i, report in enumerate(reports):
            print(format_report(report))
            if len(reports) > 1 and i < len(reports) - 1:
                print("---\n")


if __name__ == '__main__':
    main()
