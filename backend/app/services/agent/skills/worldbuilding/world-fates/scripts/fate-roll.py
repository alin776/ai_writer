#!/usr/bin/env python3
"""
Fate Roll - The Wheel of Fortune

Rolls against fate pressure to determine if a fate-shift occurs.
Uses weighted probability based on accumulated pressure.

Usage:
    python fate-roll.py --pressure 0.65
    python fate-roll.py --pressure 0.75 --danger --fortune 0
    python fate-roll.py --pressure 0.80 --danger --fortune 0 --name "Kaira the Bold"
    python fate-roll.py --seed 12345 --pressure 0.65
"""

import json
import math
import sys
import time


class SeededRandom:
    def __init__(self, seed):
        self.seed = seed

    def next(self):
        self.seed = (self.seed * 1103515245 + 12345) & 0x7FFFFFFF
        return self.seed / 0x7FFFFFFF

    def d100(self):
        return int(self.next() * 100) + 1


def roll_fate(fate_pressure, in_danger, fortune_buffer, rng):
    roll = rng.d100()
    threshold = fate_pressure * 100
    shift_triggered = roll < threshold

    severity = "none"
    if shift_triggered:
        if roll < threshold * 0.25:
            severity = "catastrophic"
        elif roll < threshold * 0.50:
            severity = "major"
        elif roll < threshold * 0.75:
            severity = "moderate"
        else:
            severity = "minor"

    death_eligible = in_danger and fate_pressure > 0.5 and fortune_buffer < 1
    death_roll = None
    death_threshold = None
    death_occurs = None
    fortune_decrement = None

    if death_eligible and shift_triggered:
        death_roll = rng.next()
        death_threshold = (fate_pressure - 0.5) * 2 * (1 - fortune_buffer / 5)
        death_occurs = death_roll < death_threshold
        if not death_occurs:
            fortune_decrement = True

    return {
        "roll": roll,
        "threshold": threshold,
        "shiftTriggered": shift_triggered,
        "severity": severity,
        "deathEligible": death_eligible,
        "deathRoll": death_roll,
        "deathThreshold": death_threshold,
        "deathOccurs": death_occurs,
        "fortuneDecrement": fortune_decrement,
    }


def format_roll_result(result, entity_name=None):
    lines = []
    lines.append("FATE ROLL{}".format(": " + entity_name if entity_name else ""))
    lines.append("=" * 50)
    lines.append("")
    lines.append("Roll: {} vs Threshold {}".format(result["roll"], int(result["threshold"])))
    lines.append("")

    if result["shiftTriggered"]:
        lines.append("THE WHEEL TURNS")
        lines.append("-" * 50)
        lines.append("Fate-shift triggered. Severity: {}".format(result["severity"].upper()))
        lines.append("")
        if result["severity"] == "catastrophic":
            lines.append("The wheel turns heavily. A catastrophic fate-shift is warranted.")
            lines.append("Consider: death, complete fall, total collapse, destruction.")
        elif result["severity"] == "major":
            lines.append("A major turn of the wheel. Significant consequences follow.")
            lines.append("Consider: serious wound, major loss, significant decline, defeat.")
        elif result["severity"] == "moderate":
            lines.append("The wheel moves. A moderate setback occurs.")
            lines.append("Consider: vulnerability exposed, resource lost, ally turns.")
        elif result["severity"] == "minor":
            lines.append("A warning from fate. Minor consequences manifest.")
            lines.append("Consider: reputation damage, small loss, omen of worse to come.")

        if result["deathEligible"]:
            lines.append("")
            lines.append("DEATH ROLL")
            lines.append("-" * 50)
            lines.append("Death eligibility: YES (in danger, pressure > 50%, fortune depleted)")
            lines.append("Death roll: {:.1f}% vs threshold {:.1f}%".format(
                result["deathRoll"] * 100, result["deathThreshold"] * 100))
            if result["deathOccurs"]:
                lines.append("")
                lines.append("*** DEATH OCCURS ***")
                lines.append("The wheel of fate turns completely. The entity meets their end.")
                lines.append("")
                lines.append("Next steps:")
                lines.append("  1. Run propose-shift.py to generate death proposal")
                lines.append("  2. Determine narrative hook for the death")
                lines.append("  3. Submit for human approval")
            else:
                lines.append("")
                lines.append("Death avoided. Fate grants a reprieve this time.")
                if result["fortuneDecrement"]:
                    lines.append("Fortune buffer should decrease by 1 (narrow escape).")
    else:
        lines.append("THE WHEEL HOLDS")
        lines.append("-" * 50)
        lines.append("No fate-shift triggered. The entity continues.")
        lines.append("")
        lines.append("Pressure continues to accumulate unless addressed.")
        lines.append("Re-roll at next trigger point (session end, arc completion, etc.).")

    lines.append("")
    lines.append("NEXT STEPS")
    lines.append("-" * 50)
    if result["shiftTriggered"]:
        lines.append("1. Determine appropriate shift type based on severity")
        lines.append("2. Consider running fate-choice.py for Tier 2 choice")
        lines.append("3. Run propose-shift.py to generate formal proposal")
        lines.append("4. Submit for human approval before applying")
    else:
        lines.append("1. Continue tracking exposure events")
        lines.append("2. Update vulnerability/protection if changed")
        lines.append("3. Re-roll at next trigger point")
    return chr(10).join(lines)


def main():
    args = sys.argv[1:]
    if "--help" in args or "-h" in args:
        print("Fate Roll - The Wheel of Fortune")
        print()
        print("Usage:")
        print("  python fate-roll.py [options]")
        print()
        print("Options:")
        print("  --pressure <0-1>  Fate pressure (required)")
        print("  --danger          Entity is in active danger (enables death roll)")
        print("  --fortune <0-5>   Fortune buffer (default: 3)")
        print("  --name <name>     Entity name for output")
        print("  --seed <n>        Random seed for reproducibility")
        print("  --json            Output as JSON")
        sys.exit(0)

    pressure = -1.0
    danger = "--danger" in args
    fortune = 3.0
    name = ""
    seed = int(time.time() * 1000) % (2**31)
    json_output = "--json" in args

    i = 0
    while i < len(args):
        if args[i] == "--pressure" and i + 1 < len(args):
            i += 1
            try: pressure = float(args[i])
            except ValueError: pressure = -1.0
        elif args[i] == "--fortune" and i + 1 < len(args):
            i += 1
            try: fortune = float(args[i])
            except ValueError: fortune = 3.0
        elif args[i] == "--name" and i + 1 < len(args):
            i += 1; name = args[i]
        elif args[i] == "--seed" and i + 1 < len(args):
            i += 1
            try: seed = int(args[i])
            except ValueError: pass
        i += 1

    if pressure < 0 or pressure > 1:
        print("Error: --pressure required (value between 0 and 1)", file=sys.stderr)
        print("Example: --pressure 0.65", file=sys.stderr)
        sys.exit(1)

    fortune = min(max(fortune, 0), 5)
    rng = SeededRandom(seed)
    result = roll_fate(pressure, danger, fortune, rng)

    if json_output:
        output = {
            "name": name or None,
            "fatePressure": pressure,
            "inDanger": danger,
            "fortuneBuffer": fortune,
            "seed": seed,
        }
        output.update(result)
        print(json.dumps(output, indent=2))
    else:
        print(format_roll_result(result, name or None))


if __name__ == "__main__":
    main()
