#!/usr/bin/env python3
"""
Exposure Log - Track Risk Events

Logs risk exposure events that increase fate pressure.
Categorizes events and suggests pressure increments.

Usage:
    python exposure-log.py --event "Survived assassination attempt"
    python exposure-log.py --event "Secret revealed publicly" --pressure 0.20
    python exposure-log.py --list
"""

import json
import sys
from datetime import date


EXPOSURE_CATEGORIES = {
    "combat": {
        "base": 0.10,
        "description": "Active combat, violence, or physical danger",
        "keywords": ["combat", "battle", "fight", "wound", "attack", "assassination", "duel"],
    },
    "intrigue": {
        "base": 0.05,
        "description": "Political maneuvering, subtle threats",
        "keywords": ["intrigue", "politics", "scheme", "plot", "manipulat", "negotiat"],
    },
    "betrayal": {
        "base": 0.15,
        "description": "Trust violated, ally turns against",
        "keywords": ["betray", "turned", "abandon", "traitor", "double-cross"],
    },
    "revelation": {
        "base": 0.20,
        "description": "Secret exposed, truth revealed",
        "keywords": ["secret", "reveal", "exposed", "discover", "truth", "uncover"],
    },
    "overreach": {
        "base": 0.10,
        "description": "Hubris, overconfident action",
        "keywords": ["hubris", "overconfident", "reckless", "arrogant", "foolish"],
    },
    "loss": {
        "base": 0.08,
        "description": "Resource, ally, or territory lost",
        "keywords": ["lost", "death of", "defeat", "lose", "fallen"],
    },
    "challenge": {
        "base": 0.12,
        "description": "Direct challenge to power or status",
        "keywords": ["challenge", "rival", "contest", "dispute", "claim"],
    },
    "narrow_escape": {
        "base": 0.05,
        "description": "Survived dangerous situation",
        "keywords": ["narrow", "escape", "surviv", "barely", "close call"],
    },
}


def categorize_event(event_description):
    lower = event_description.lower()
    for category, data in EXPOSURE_CATEGORIES.items():
        for keyword in data["keywords"]:
            if keyword in lower:
                return category, data["base"], data
    return "intrigue", 0.05, EXPOSURE_CATEGORIES["intrigue"]


def format_exposure_entry(event, category, pressure, name=None):
    today = str(date.today())
    lines = []
    lines.append("EXPOSURE EVENT LOGGED")
    lines.append("=" * 50)
    lines.append("")
    if name:
        lines.append("Entity: {}".format(name))
    lines.append("Date: {}".format(today))
    lines.append("Event: {}".format(event))
    lines.append("Category: {}".format(category))
    lines.append("Pressure Increment: +{:.1f}%".format(pressure * 100))
    lines.append("")
    lines.append("WORLD BIBLE ENTRY FORMAT")
    lines.append("-" * 50)
    lines.append("Add to entity's Risk Exposure Log section:")
    lines.append("")
    lines.append("- {}: {} (+{}% pressure)".format(today, event, int(pressure * 100)))
    lines.append("")
    lines.append("CUMULATIVE EFFECT")
    lines.append("-" * 50)
    lines.append("This event adds to the entity's total fate pressure.")
    lines.append("Run fate-pressure.py to see current total.")
    return chr(10).join(lines)


def main():
    args = sys.argv[1:]
    if "--help" in args or "-h" in args:
        print("Exposure Log - Track Risk Events")
        print()
        print("Usage:")
        print("  python exposure-log.py [options]")
        print()
        print("Required:")
        print("  --event <text>    Description of the exposure event")
        print()
        print("Optional:")
        print("  --pressure <n>    Override suggested pressure increment (0.01-0.30)")
        print("  --name <name>     Entity name for context")
        print("  --json            Output as JSON for programmatic use")
        print()
        print("Information:")
        print("  --list            List all exposure categories and base pressures")
        sys.exit(0)

    if "--list" in args:
        print("Exposure Categories")
        print("=" * 50)
        print()
        for category, data in EXPOSURE_CATEGORIES.items():
            print(category.upper())
            print("  Base pressure: +{}%".format(int(data["base"] * 100)))
            print("  Description: {}".format(data["description"]))
            print("  Keywords: {}".format(", ".join(data["keywords"])))
            print()
        sys.exit(0)

    event = ""
    custom_pressure = None
    name = ""
    json_output = "--json" in args

    i = 0
    while i < len(args):
        if args[i] == "--event" and i + 1 < len(args):
            i += 1; event = args[i]
        elif args[i] == "--pressure" and i + 1 < len(args):
            i += 1
            try: custom_pressure = float(args[i])
            except ValueError: pass
        elif args[i] == "--name" and i + 1 < len(args):
            i += 1; name = args[i]
        i += 1

    if not event:
        print("Error: --event required", file=sys.stderr)
        print('Example: --event "Survived assassination attempt"', file=sys.stderr)
        sys.exit(1)

    category, suggested_pressure, category_data = categorize_event(event)
    pressure = custom_pressure if custom_pressure is not None else suggested_pressure
    pressure = min(max(pressure, 0.01), 0.30)

    if json_output:
        print(json.dumps({
            "date": str(date.today()),
            "entity": name or None,
            "event": event,
            "category": category,
            "pressure": pressure,
            "categoryDescription": category_data["description"],
        }, indent=2))
    else:
        print(format_exposure_entry(event, category, pressure, name or None))


if __name__ == "__main__":
    main()
