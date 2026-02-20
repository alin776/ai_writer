#!/usr/bin/env python3
"""
Fate Choice Generator - Tier 2 Dramatic Choices

Generates dramatic choices when fate pressure is high.
One path leads to NPC-hood, one path faces the roll,
optional third path offers different trade-off.

Usage:
    python fate-choice.py --name "Kaira the Bold" --pressure 0.72
    python fate-choice.py --name "Kaira" --pressure 0.72 --antagonist "The Dark Queen"
    python fate-choice.py --name "Kaira" --pressure 0.72 --pattern dark_bargain
"""

import json
import os
import re
import sys
import time


class SeededRandom:
    def __init__(self, seed):
        self.seed = seed

    def next(self):
        self.seed = (self.seed * 1103515245 + 12345) & 0x7FFFFFFF
        return self.seed / 0x7FFFFFFF

    def pick(self, array):
        return array[int(self.next() * len(array))]


def load_choice_data():
    try:
        script_dir = os.path.dirname(os.path.abspath(__file__))
        data_path = os.path.join(script_dir, "..", "data", "fate-choices.json")
        with open(data_path, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return None


def calculate_death_odds(pressure, fortune):
    if pressure <= 0.5 or fortune >= 1:
        return 0
    return (pressure - 0.5) * 2 * (1 - fortune / 5) * 100


def generate_choice(name, pressure, fortune, pattern, antagonist, rng):
    lines = []
    death_odds = calculate_death_odds(pressure, fortune)

    lines.append("FATE CHOICE: {}".format(name))
    lines.append("=" * 50)
    lines.append("")
    lines.append("The wheel turns. Fate pressure is {}%.".format(int(pressure * 100)))
    lines.append("A choice presents itself:")
    lines.append("")

    situation = rng.pick(pattern["examples"])
    if antagonist:
        situation = re.sub(
            r"The Queen of Shadows|the demon|The emperor|the enemy",
            antagonist, situation, flags=re.IGNORECASE)
    lines.append('"{}"'.format(situation))
    lines.append("")

    path_keys = list(pattern["paths"].keys())
    path_labels = ["A", "B", "C"]

    for i, key in enumerate(path_keys):
        path = pattern["paths"][key]
        label = path_labels[i] if i < len(path_labels) else str(i + 1)
        lines.append("{}) {}".format(label, key.upper().replace("_", " ")))
        lines.append("   {}".format(path["description"]))
        for consequence in path["consequences"]:
            display = consequence
            if "current odds" in consequence:
                display = consequence.replace("current odds", "{}% death chance".format(int(death_odds)))
            lines.append("   -> {}".format(display))
        lines.append("")

    lines.append("-" * 50)
    lines.append("MECHANICS")
    lines.append("-" * 50)
    lines.append("  Fate Pressure: {}%".format(int(pressure * 100)))
    lines.append("  Fortune Buffer: {}/5".format(fortune))
    if death_odds > 0:
        lines.append("  Death Odds (if roll path): {}%".format(int(death_odds)))
    else:
        lines.append("  Death: Not eligible (fortune > 0 or pressure <= 50%)")
    lines.append("")
    lines.append("NOTES FOR FACILITATOR")
    lines.append("-" * 50)
    lines.append("  - Present this choice at a dramatic moment")
    lines.append("  - The NPC path should feel like a real cost, not escape")
    lines.append("  - If they choose to roll, use fate-roll.py with --danger flag")
    lines.append("  - Honor their choice -- this IS the climax")

    return chr(10).join(lines)


DEFAULT_PATTERN = {
    "description": "A powerful entity offers safety at the cost of service",
    "triggers": ["high_pressure"],
    "paths": {
        "accept": {
            "outcome": "npc_transition",
            "description": "Accept the bargain. Survive, but serve.",
            "consequences": [
                "Character becomes NPC in antagonist's service",
                "May appear as ally, enemy, or neutral figure later",
                "Player loses control but character persists",
            ],
        },
        "refuse": {
            "outcome": "fate_roll",
            "description": "Refuse. Face what comes.",
            "consequences": [
                "Roll death/fall check at current odds",
                "If survived: fortune buffer decreases",
                "If failed: death or major fall",
            ],
        },
        "counter": {
            "outcome": "complication",
            "description": "Make a counter-offer. Change the terms.",
            "consequences": [
                "Temporary reprieve",
                "New obligation or debt",
                "Fate pressure temporarily reduced but will return",
            ],
        },
    },
    "examples": [
        "The Dark One offers sanctuary -- serve them, lose yourself",
        "Your enemy offers pardon in exchange for eternal loyalty",
        "The power offers itself -- take it and be changed forever",
    ],
}


def main():
    args = sys.argv[1:]
    if "--help" in args or "-h" in args:
        print("Fate Choice Generator")
        print()
        print("Generates Tier 2 dramatic choices for high-pressure situations.")
        print()
        print("Usage:")
        print("  python fate-choice.py [options]")
        print()
        print("Required:")
        print("  --name <name>        Entity name")
        print("  --pressure <0-1>     Fate pressure (should be > 0.6)")
        print()
        print("Optional:")
        print("  --fortune <0-5>      Fortune buffer (default: 0)")
        print("  --antagonist <name>  Name to use for tempter/threat")
        print("  --pattern <type>     Specific pattern to use")
        print("  --seed <n>           Random seed for reproducibility")
        print("  --list               List available patterns")
        sys.exit(0)

    choice_data = load_choice_data()
    if not choice_data:
        print("Warning: Could not load fate-choices.json, using defaults", file=sys.stderr)

    name = ""
    pressure = -1.0
    fortune = 0
    antagonist = None
    pattern_name = None
    seed = int(time.time() * 1000) % (2**31)

    i = 0
    while i < len(args):
        if args[i] == "--name" and i + 1 < len(args):
            i += 1
            name = args[i]
        elif args[i] == "--pressure" and i + 1 < len(args):
            i += 1
            try:
                pressure = float(args[i])
            except ValueError:
                pressure = -1.0
        elif args[i] == "--fortune" and i + 1 < len(args):
            i += 1
            try:
                fortune = float(args[i])
            except ValueError:
                fortune = 0
        elif args[i] == "--antagonist" and i + 1 < len(args):
            i += 1
            antagonist = args[i]
        elif args[i] == "--pattern" and i + 1 < len(args):
            i += 1
            pattern_name = args[i]
        elif args[i] == "--seed" and i + 1 < len(args):
            i += 1
            try:
                seed = int(args[i])
            except ValueError:
                pass
        elif args[i] == "--list":
            if choice_data:
                print("Available patterns:")
                for key, pat in choice_data.get("choice_patterns", {}).items():
                    print("  {}: {}".format(key, pat["description"]))
            sys.exit(0)
        i += 1

    if not name:
        print("Error: --name required", file=sys.stderr)
        sys.exit(1)
    if pressure < 0 or pressure > 1:
        print("Error: --pressure required (value between 0 and 1)", file=sys.stderr)
        sys.exit(1)
    if pressure < 0.5:
        print("Warning: Fate pressure < 50%. Tier 2 choices typically trigger at > 60%.", file=sys.stderr)

    fortune = min(max(fortune, 0), 5)
    rng = SeededRandom(seed)

    if choice_data and pattern_name and pattern_name in choice_data.get("choice_patterns", {}):
        pattern = choice_data["choice_patterns"][pattern_name]
    elif choice_data:
        patterns = list(choice_data.get("choice_patterns", {}).values())
        pattern = rng.pick(patterns) if patterns else DEFAULT_PATTERN
    else:
        pattern = DEFAULT_PATTERN

    print(generate_choice(name, pressure, fortune, pattern, antagonist, rng))


if __name__ == "__main__":
    main()
