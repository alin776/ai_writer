#!/usr/bin/env python3
"""
Propose Fate-Shift

Generates a proposal document for human review before applying
changes to the world bible.

Usage:
    python propose-shift.py --name "Character Name" --type fall --severity major
    python propose-shift.py --name "Character Name" --type death --pressure 0.82 --roll 15 --output proposal.md
"""

import json
import os
import sys
import time
from datetime import date


class SeededRandom:
    def __init__(self, seed):
        self.seed = seed

    def next(self):
        self.seed = (self.seed * 1103515245 + 12345) & 0x7FFFFFFF
        return self.seed / 0x7FFFFFFF

    def pick(self, array):
        return array[int(self.next() * len(array))]


def load_shift_types():
    try:
        script_dir = os.path.dirname(os.path.abspath(__file__))
        data_path = os.path.join(script_dir, "..", "data", "shift-types.json")
        with open(data_path, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return None


def get_lesser_severity(severity):
    order = ["minor", "moderate", "major", "catastrophic"]
    index = order.index(severity) if severity in order else 0
    return order[index - 1] if index > 0 else "warning sign"


def get_alternative_type(shift_type, category):
    alternatives = {
        "character": {
            "death": ["fall", "exile"],
            "fall": ["diminishment", "exile"],
            "corruption": ["transformation", "fall"],
            "exile": ["fall", "diminishment"],
            "transformation": ["corruption", "diminishment"],
            "diminishment": ["fall", "transformation"],
        },
        "faction": {
            "collapse": ["schism", "decline"],
            "schism": ["decline", "reformation"],
            "absorption": ["decline", "defeat"],
            "decline": ["defeat", "schism"],
            "reformation": ["schism", "decline"],
            "defeat": ["decline", "absorption"],
        },
        "location": {
            "destruction": ["disaster", "conquest"],
            "conquest": ["decline", "isolation"],
            "disaster": ["decline", "destruction"],
            "decline": ["isolation", "disaster"],
            "transformation": ["decline", "isolation"],
            "isolation": ["decline", "transformation"],
        },
    }
    category_alts = alternatives.get(category, {})
    type_alts = category_alts.get(shift_type, [])
    return type_alts[0] if type_alts else "different fate"


def generate_proposal(name, category, shift_type, severity, pressure, roll, trigger, vulnerabilities, shift_data, rng):
    today = str(date.today())
    threshold = pressure * 100
    narrative_hook = rng.pick(shift_data["narrativeHooks"])
    severity_desc = shift_data.get("severities", {}).get(severity, "Consequences to be determined.")

    lines = []
    lines.append("# Fate-Shift Proposal: {}".format(name))
    lines.append("")
    lines.append("**Date Generated:** {}".format(today))
    lines.append("**Trigger:** {}".format(trigger))
    lines.append("**Fate Pressure at Assessment:** {:.1f}%".format(pressure * 100))
    lines.append("")

    lines.append("## Current State Summary")
    lines.append("")
    lines.append("{} is a {} currently under significant fate pressure.".format(name, category))
    lines.append("The wheel of fortune has turned against them.")
    lines.append("")

    lines.append("## Vulnerability Analysis")
    lines.append("")
    if vulnerabilities:
        lines.append("The following vulnerabilities contributed to this fate-shift:")
        for v in vulnerabilities:
            lines.append("- {}".format(v))
    else:
        lines.append("Vulnerabilities should be documented from the entity's world bible entry.")
    lines.append("")

    lines.append("## The Fate Roll")
    lines.append("")
    if roll is not None:
        lines.append("- **Roll:** {}".format(roll))
        lines.append("- **Threshold:** {}".format(int(threshold)))
    else:
        lines.append("- **Roll:** [Not recorded - manual proposal]")
        lines.append("- **Threshold:** {} (based on pressure)".format(int(threshold)))
    lines.append("- **Severity:** {}".format(severity.upper()))
    lines.append("")

    lines.append("## Proposed Fate-Shift")
    lines.append("")
    lines.append("{} experiences a {} {}.".format(name, severity, shift_type))
    lines.append("")
    lines.append("**{}**".format(shift_data["description"]))
    lines.append("")
    lines.append(severity_desc)
    lines.append("")

    lines.append("### Type")
    lines.append("")
    lines.append(shift_type)
    lines.append("")

    lines.append("### Narrative Hook")
    lines.append("")
    lines.append(narrative_hook)
    lines.append("")

    lines.append("### Consequences")
    lines.append("")
    lines.append("- **For {}:** {}".format(name, severity_desc))
    if category == "character":
        lines.append("- **For the world:** Power vacuum in {}'s sphere of influence. Allies and enemies respond.".format(name))
        lines.append("- **For campaigns:** Review active campaigns involving this character for impact.")
    elif category == "faction":
        lines.append("- **For the world:** {}'s {} creates opportunities for rivals and instability for allies.".format(name, shift_type))
        lines.append("- **For campaigns:** Review campaigns with faction involvement for necessary adjustments.")
    else:
        lines.append("- **For the world:** The {} of {} ripples outward, affecting connected locations.".format(shift_type, name))
        lines.append("- **For campaigns:** Review campaigns set in or connected to this location.")
    lines.append("")

    lines.append("## Alternative Options")
    lines.append("")
    lines.append("1. Reduce severity to {} with slower progression".format(get_lesser_severity(severity)))
    lines.append("2. Change type to {} with equivalent severity".format(get_alternative_type(shift_type, category)))
    lines.append("3. Defer decision and increase pressure by 0.1 for next assessment")
    lines.append("")

    lines.append("## Approval Required")
    lines.append("")
    lines.append("- [ ] Approve as proposed")
    lines.append("- [ ] Approve with modifications: _______________")
    lines.append("- [ ] Reject and explain: _______________")
    lines.append("- [ ] Defer decision to later")
    lines.append("")

    lines.append("---")
    lines.append("")
    lines.append("*Generated by world-fates skill on {}*".format(today))

    return chr(10).join(lines)


DEFAULT_SHIFT_DATA = {
    "description": "A fate-shift affecting the entity",
    "severities": {
        "minor": "Minor consequences",
        "moderate": "Moderate consequences",
        "major": "Major consequences",
        "catastrophic": "Catastrophic consequences",
    },
    "narrativeHooks": ["The circumstances unfold through play"],
}


def main():
    args = sys.argv[1:]
    if "--help" in args or "-h" in args:
        print("Propose Fate-Shift")
        print()
        print("Generates a fate-shift proposal for human review.")
        print()
        print("Usage:")
        print("  python propose-shift.py [options]")
        print()
        print("Required:")
        print("  --name <name>         Entity name")
        print("  --type <type>         Shift type (death, fall, corruption, etc.)")
        print("  --severity <level>    Severity (minor, moderate, major, catastrophic)")
        print()
        print("Optional:")
        print("  --category <cat>      Entity category (character, faction, location; default: character)")
        print("  --pressure <0-1>      Fate pressure (default: 0.65)")
        print("  --roll <1-100>        The roll that triggered this")
        print("  --trigger <text>      What triggered assessment (default: Manual assessment)")
        print("  --vulns <csv>         Comma-separated vulnerabilities")
        print("  --output <file>       Output file path")
        print("  --seed <n>            Random seed")
        sys.exit(0)

    shift_types_data = load_shift_types()

    name = ""
    category = "character"
    shift_type = ""
    severity = ""
    pressure = 0.65
    roll = None
    trigger = "Manual assessment"
    vulns_str = ""
    output = ""
    seed = int(time.time() * 1000) % (2**31)

    i = 0
    while i < len(args):
        if args[i] == "--name" and i + 1 < len(args):
            i += 1; name = args[i]
        elif args[i] == "--category" and i + 1 < len(args):
            i += 1; category = args[i]
        elif args[i] == "--type" and i + 1 < len(args):
            i += 1; shift_type = args[i]
        elif args[i] == "--severity" and i + 1 < len(args):
            i += 1; severity = args[i]
        elif args[i] == "--pressure" and i + 1 < len(args):
            i += 1
            try: pressure = float(args[i])
            except ValueError: pass
        elif args[i] == "--roll" and i + 1 < len(args):
            i += 1
            try: roll = int(args[i])
            except ValueError: pass
        elif args[i] == "--trigger" and i + 1 < len(args):
            i += 1; trigger = args[i]
        elif args[i] == "--vulns" and i + 1 < len(args):
            i += 1; vulns_str = args[i]
        elif args[i] == "--output" and i + 1 < len(args):
            i += 1; output = args[i]
        elif args[i] == "--seed" and i + 1 < len(args):
            i += 1
            try: seed = int(args[i])
            except ValueError: pass
        i += 1

    if not name:
        print("Error: --name required", file=sys.stderr)
        sys.exit(1)
    if not shift_type:
        print("Error: --type required", file=sys.stderr)
        sys.exit(1)
    if not severity:
        print("Error: --severity required", file=sys.stderr)
        sys.exit(1)

    vulnerabilities = [v.strip() for v in vulns_str.split(",")] if vulns_str else []
    rng = SeededRandom(seed)

    if shift_types_data and category in shift_types_data and shift_type in shift_types_data[category]:
        shift_data = shift_types_data[category][shift_type]
    else:
        shift_data = dict(DEFAULT_SHIFT_DATA)
        shift_data["description"] = "A {} affecting {}".format(shift_type, category)

    proposal = generate_proposal(
        name, category, shift_type, severity, pressure, roll,
        trigger, vulnerabilities, shift_data, rng)

    if output:
        with open(output, "w", encoding="utf-8") as out_f:
            out_f.write(proposal)
        print("Proposal written to: {}".format(output))
    else:
        print(proposal)


if __name__ == "__main__":
    main()
