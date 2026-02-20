#!/usr/bin/env python3
"""
Fate Pressure Calculator

Calculates current fate pressure for entities based on:
- Power level (1-10)
- Tenure modifier (0.5x - 2.5x)
- Vulnerability score (0-10)
- Protection factor (1-10)
- Fortune buffer (0-5)
- Risk exposure accumulation

Usage:
    python fate-pressure.py --power 7 --tenure 40 --vulns 3 --prots 2 --fortune 2
    python fate-pressure.py --json
"""

import json
import sys
from datetime import date


def get_tenure_modifier(years):
    if years < 1:
        return 0.5
    if years <= 5:
        return 1.0
    if years <= 20:
        return 1.5
    if years <= 50:
        return 2.0
    return 2.5


def calculate_vulnerability_score(vulnerabilities):
    score = 0
    for v in vulnerabilities:
        lower = v.lower()
        if "secret" in lower or "hidden" in lower:
            score += 3
        elif "flaw" in lower or "weakness" in lower or "addiction" in lower:
            score += 2
        elif "conflict" in lower or "war" in lower or "feud" in lower:
            score += 1.5
        elif "enemy" in lower or "rival" in lower or "opponent" in lower:
            score += 1
        elif "depends" in lower or "relies" in lower or "needs" in lower:
            score += 1
        else:
            score += 1
    return min(score, 10)


def calculate_protection_factor(protections):
    factor = 1
    for p in protections:
        lower = p.lower()
        if "divine" in lower or "god" in lower or "blessed" in lower:
            factor += 3
        elif "magical" in lower or "enchant" in lower or "ward" in lower:
            factor += 3
        elif "fortif" in lower or "stronghold" in lower or "castle" in lower:
            factor += 2
        elif "popular" in lower or "beloved" in lower or "supported" in lower:
            factor += 2
        elif "ally" in lower or "loyal" in lower or "friend" in lower:
            factor += 1
        elif "network" in lower or "spies" in lower or "intelligence" in lower:
            factor += 1
        else:
            factor += 0.5
    return min(factor, 10)


def calculate_risk_exposure(exposure_log):
    return sum(entry["pressure"] for entry in exposure_log)


def calculate_fate_pressure(power_level, tenure_years, vulnerabilities, protections, fortune_buffer, exposure_log):
    tenure_modifier = get_tenure_modifier(tenure_years)
    vulnerability_score = calculate_vulnerability_score(vulnerabilities)
    protection_factor = calculate_protection_factor(protections)
    risk_exposure = calculate_risk_exposure(exposure_log)

    numerator = power_level * tenure_modifier * (vulnerability_score / 10)
    denominator = protection_factor * max(fortune_buffer, 0.5)
    fate_pressure = (numerator / denominator) + risk_exposure
    fate_pressure = min(max(fate_pressure, 0), 1)

    if fate_pressure < 0.2:
        state, state_desc = "F1", "Stable Ascent"
        interpretation = "This entity is relatively stable. Monitor for changes but no immediate action needed."
    elif fate_pressure < 0.35:
        state, state_desc = "F2", "Peak Power"
        interpretation = "At peak influence. Consider surfacing hidden vulnerabilities or introducing rivals."
    elif fate_pressure < 0.6:
        state, state_desc = "F3", "Overextension"
        interpretation = "High pressure. Fate-shift likely if pressure continues. Consider Tier 2 choices."
    elif fate_pressure < 0.85:
        state, state_desc = "F4", "Precarious Position"
        interpretation = "Critical pressure. Fate-offered choices should be generated. Death rolls possible."
    else:
        state, state_desc = "F5", "Fall in Progress"
        interpretation = "Terminal pressure. Focus on managing the transition and documenting the fall."

    return {
        "components": {
            "powerLevel": power_level,
            "tenureModifier": tenure_modifier,
            "vulnerabilityScore": vulnerability_score,
            "protectionFactor": protection_factor,
            "fortuneBuffer": fortune_buffer,
            "riskExposure": risk_exposure,
        },
        "fatePressure": fate_pressure,
        "state": state,
        "stateDescription": state_desc,
        "interpretation": interpretation,
    }


def format_result(result, entity_name=None):
    lines = []
    lines.append("FATE PRESSURE{}".format(": " + entity_name if entity_name else ""))
    lines.append("=" * 50)
    lines.append("")
    lines.append("Current State: {} - {}".format(result["state"], result["stateDescription"]))
    lines.append("Fate Pressure: {:.1f}%".format(result["fatePressure"] * 100))
    lines.append("")
    lines.append("COMPONENT BREAKDOWN")
    lines.append("-" * 50)
    lines.append("  Power Level:        {}/10".format(result["components"]["powerLevel"]))
    lines.append("  Tenure Modifier:    {}x".format(result["components"]["tenureModifier"]))
    lines.append("  Vulnerability Score: {:.1f}/10".format(result["components"]["vulnerabilityScore"]))
    lines.append("  Protection Factor:   {:.1f}/10".format(result["components"]["protectionFactor"]))
    lines.append("  Fortune Buffer:      {}/5".format(result["components"]["fortuneBuffer"]))
    lines.append("  Risk Exposure:       +{:.1f}%".format(result["components"]["riskExposure"] * 100))
    lines.append("")
    lines.append("INTERPRETATION")
    lines.append("-" * 50)
    lines.append("  {}".format(result["interpretation"]))
    lines.append("")
    lines.append("RECOMMENDATIONS")
    lines.append("-" * 50)
    fp = result["fatePressure"]
    if fp < 0.3:
        lines.append("  - Log exposure events as they occur")
        lines.append("  - Re-assess after significant events")
    elif fp < 0.6:
        lines.append("  - Consider fate-choice.py for dramatic moments")
        lines.append("  - Track vulnerabilities carefully")
        lines.append("  - Fate-shifts at Moderate or Minor severity possible")
    elif fp < 0.85:
        lines.append("  - Run fate-choice.py to generate Tier 2 choice")
        lines.append("  - Death/fall rolls active if in danger")
        lines.append("  - Consider voluntary NPC transition option")
    else:
        lines.append("  - Fall is in progress or imminent")
        lines.append("  - Run propose-shift.py to document the end")
        lines.append("  - Focus on managing consequences for world")
    return chr(10).join(lines)


def main():
    args = sys.argv[1:]
    if "--help" in args or "-h" in args:
        print("Fate Pressure Calculator")
        print()
        print("Usage:")
        print("  python fate-pressure.py [options]")
        print()
        print("Options:")
        print("  --power <n>       Power level (1-10, default: 5)")
        print("  --tenure <years>  Years in power (default: 5)")
        print("  --vulns <n>       Number of vulnerabilities (default: 0)")
        print("  --prots <n>       Number of protections (default: 0)")
        print("  --fortune <n>     Fortune buffer (0-5, default: 3)")
        print("  --exposure <n>    Accumulated exposure (0-1, default: 0)")
        print("  --name <name>     Entity name for output")
        print("  --json            Output as JSON")
        sys.exit(0)

    power = 5
    tenure = 5
    vuln_count = 0
    prot_count = 0
    fortune = 3
    exposure = 0.0
    name = ""
    json_output = "--json" in args

    i = 0
    while i < len(args):
        if args[i] == "--power" and i + 1 < len(args):
            i += 1; power = int(args[i])
        elif args[i] == "--tenure" and i + 1 < len(args):
            i += 1; tenure = int(args[i])
        elif args[i] == "--vulns" and i + 1 < len(args):
            i += 1; vuln_count = int(args[i])
        elif args[i] == "--prots" and i + 1 < len(args):
            i += 1; prot_count = int(args[i])
        elif args[i] == "--fortune" and i + 1 < len(args):
            i += 1; fortune = float(args[i])
        elif args[i] == "--exposure" and i + 1 < len(args):
            i += 1; exposure = float(args[i])
        elif args[i] == "--name" and i + 1 < len(args):
            i += 1; name = args[i]
        i += 1

    power = min(max(power, 1), 10)
    fortune = min(max(fortune, 0), 5)
    exposure = min(max(exposure, 0), 1)

    vulnerabilities = ["vulnerability_{}".format(j + 1) for j in range(vuln_count)]
    protections = ["protection_{}".format(j + 1) for j in range(prot_count)]
    exposure_log = []
    if exposure > 0:
        exposure_log.append({
            "date": str(date.today()),
            "event": "Accumulated exposure",
            "pressure": exposure,
        })

    result = calculate_fate_pressure(power, tenure, vulnerabilities, protections, fortune, exposure_log)

    if json_output:
        output = {"name": name or None}
        output.update(result)
        print(json.dumps(output, indent=2))
    else:
        print(format_result(result, name or None))


if __name__ == "__main__":
    main()
