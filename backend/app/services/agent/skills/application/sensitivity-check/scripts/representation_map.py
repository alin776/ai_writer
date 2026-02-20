#!/usr/bin/env python3
"""
representation_map.py - Map and analyze character representation

Analyzes character data to identify:
- Identity distribution
- Agency/centrality patterns
- Potential trope risks
- Diversity within identity groups

Usage:
  python representation_map.py characters.json
  python representation_map.py --format
  python representation_map.py --json characters.json

Character JSON format:
[
  {
    "name": "Character Name",
    "role": "protagonist|antagonist|supporting|minor",
    "identities": {
      "race": "...",
      "gender": "...",
      "sexuality": "...",
      "disability": "...",
      "other": ["..."]
    },
    "agency": "high|medium|low",
    "arc": "positive|negative|flat|none",
    "survives": true|false,
    "notes": "..."
  }
]
"""

import sys
import json

# Ensure UTF-8 output on all platforms
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")
if hasattr(sys.stderr, "reconfigure"):
    sys.stderr.reconfigure(encoding="utf-8")

# ---------------------------------------------------------------------------
# Identity reference lists
# ---------------------------------------------------------------------------

MARGINALIZED_IDENTITIES = {
    "race": ["black", "asian", "latino", "latina", "latinx", "indigenous",
             "native", "middle eastern", "south asian", "pacific islander",
             "mixed", "biracial", "multiracial"],
    "gender": ["woman", "female", "trans", "transgender", "non-binary",
               "nonbinary", "genderqueer", "agender", "genderfluid"],
    "sexuality": ["gay", "lesbian", "bisexual", "pansexual", "queer",
                  "asexual", "ace"],
    "disability": ["disabled", "blind", "deaf", "wheelchair", "chronic",
                   "neurodivergent", "autistic", "adhd"],
    "mentalHealth": ["depression", "anxiety", "ptsd", "bipolar",
                     "schizophrenia", "ocd", "eating disorder"],
}

IDENTITY_CATEGORIES = ["race", "gender", "sexuality", "disability",
                       "mentalHealth", "religion"]


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def is_marginalized(category, value):
    """Return True if *value* matches any known marginalized term in *category*."""
    category_list = MARGINALIZED_IDENTITIES.get(category)
    if not category_list:
        return False
    lower_value = value.lower()
    return any(term in lower_value for term in category_list)


def _get_identity(char, category):
    """Safely retrieve an identity value from a character dict."""
    identities = char.get("identities", {})
    return identities.get(category, None)


def _identity_items(char):
    """Yield (category, value) pairs for every string identity on *char*."""
    identities = char.get("identities", {})
    for cat, val in identities.items():
        if val and isinstance(val, str):
            yield cat, val


def _has_marginalized_identity(char):
    """Return True if the character has any marginalized identity."""
    return any(
        is_marginalized(cat, val)
        for cat, val in _identity_items(char)
    )


# ---------------------------------------------------------------------------
# Core analysis
# ---------------------------------------------------------------------------

def analyze_characters(characters):
    """Analyze a list of character dicts and return a comprehensive result."""
    result = {
        "characterCount": len(characters),
        "roleDistribution": {},
        "identityDistribution": {},
        "agencyAnalysis": {"byIdentity": {}, "concerns": []},
        "survivalAnalysis": {"byIdentity": {}, "concerns": []},
        "tropeRisks": [],
        "diversityNotes": [],
    }

    # --- Role distribution ---
    for char in characters:
        role = char.get("role", "unknown")
        result["roleDistribution"][role] = result["roleDistribution"].get(role, 0) + 1

    # --- Identity distribution ---
    for category in IDENTITY_CATEGORIES:
        result["identityDistribution"][category] = {}

    for char in characters:
        for category in IDENTITY_CATEGORIES:
            value = _get_identity(char, category)
            if value and isinstance(value, str):
                bucket = result["identityDistribution"][category]
                bucket[value] = bucket.get(value, 0) + 1

    # --- Agency analysis by identity ---
    agency_by_id = result["agencyAnalysis"]["byIdentity"]
    for char in characters:
        agency = char.get("agency", "medium")
        for cat, val in _identity_items(char):
            key = f"{cat}:{val}"
            if key not in agency_by_id:
                agency_by_id[key] = {"high": 0, "medium": 0, "low": 0}
            if agency in agency_by_id[key]:
                agency_by_id[key][agency] += 1

    # Agency concerns
    for identity, counts in agency_by_id.items():
        total = counts["high"] + counts["medium"] + counts["low"]
        if total >= 2:
            low_pct = (counts["low"] / total) * 100
            if low_pct > 50:
                cat, val = identity.split(":", 1)
                if is_marginalized(cat, val):
                    result["agencyAnalysis"]["concerns"].append(
                        f"{identity}: {low_pct:.0f}% low agency "
                        f"({counts['low']}/{total} characters)"
                    )

    # --- Survival analysis ---
    survival_by_id = result["survivalAnalysis"]["byIdentity"]
    for char in characters:
        for cat, val in _identity_items(char):
            key = f"{cat}:{val}"
            if key not in survival_by_id:
                survival_by_id[key] = {"survives": 0, "dies": 0}
            if char.get("survives", True):
                survival_by_id[key]["survives"] += 1
            else:
                survival_by_id[key]["dies"] += 1

    # Survival concerns
    for identity, counts in survival_by_id.items():
        total = counts["survives"] + counts["dies"]
        if counts["dies"] > 0:
            death_pct = (counts["dies"] / total) * 100
            cat, val = identity.split(":", 1)
            if is_marginalized(cat, val):
                if death_pct > 50 or (cat == "sexuality" and counts["dies"] > 0):
                    result["survivalAnalysis"]["concerns"].append(
                        f"{identity}: {counts['dies']}/{total} characters die "
                        f"({death_pct:.0f}%)"
                    )

    # --- Trope risk detection ---

    # Bury Your Gays
    lgbtq_chars = [
        c for c in characters
        if is_marginalized("sexuality", _get_identity(c, "sexuality") or "")
        or (
            _get_identity(c, "gender")
            and is_marginalized("gender", _get_identity(c, "gender"))
            and "trans" in (_get_identity(c, "gender") or "").lower()
        )
    ]
    lgbtq_deaths = [c for c in lgbtq_chars if not c.get("survives", True)]
    if lgbtq_deaths:
        names = ", ".join(c.get("name", "?") for c in lgbtq_deaths)
        result["tropeRisks"].append(
            f"BURY YOUR GAYS RISK: {len(lgbtq_deaths)} LGBTQ+ character(s) die: {names}"
        )

    # Magical minority detection
    marginalized_supporting_high = [
        c for c in characters
        if c.get("role") == "supporting"
        and c.get("agency") == "high"
        and _has_marginalized_identity(c)
    ]
    protagonists = [c for c in characters if c.get("role") == "protagonist"]
    default_protagonists = [
        c for c in protagonists
        if not _has_marginalized_identity(c)
    ]

    if marginalized_supporting_high and default_protagonists:
        names = ", ".join(c.get("name", "?") for c in marginalized_supporting_high)
        result["tropeRisks"].append(
            f"MAGICAL MINORITY RISK: Marginalized supporting characters with "
            f"high agency serving default protagonist(s). Check: {names}"
        )

    # Mental health + antagonist
    mh_antagonists = [
        c for c in characters
        if c.get("role") == "antagonist" and _get_identity(c, "mentalHealth")
    ]
    if mh_antagonists:
        details = ", ".join(
            f"{c.get('name', '?')} ({_get_identity(c, 'mentalHealth')})"
            for c in mh_antagonists
        )
        result["tropeRisks"].append(
            f"MENTAL ILLNESS = VILLAIN RISK: Antagonist(s) with mental health "
            f"conditions: {details}"
        )

    # --- Diversity / tokenism notes ---
    identity_counts = {}
    for char in characters:
        for cat, val in _identity_items(char):
            key = f"{cat}:{val}"
            identity_counts[key] = identity_counts.get(key, 0) + 1

    for identity, count in identity_counts.items():
        if count == 1:
            cat, val = identity.split(":", 1)
            if is_marginalized(cat, val):
                result["diversityNotes"].append(
                    f"Only one {val} character - consider if tokenism risk"
                )

    return result


# ---------------------------------------------------------------------------
# Reporting
# ---------------------------------------------------------------------------

def format_report(result):
    """Return a human-readable representation report."""
    report = (
        "\nREPRESENTATION MAP\n"
        "==================\n"
        "\n"
        f"Characters analyzed: {result['characterCount']}\n"
        "\n"
        "ROLE DISTRIBUTION\n"
    )
    for role, count in result["roleDistribution"].items():
        report += f"  {role}: {count}\n"

    report += "\nIDENTITY DISTRIBUTION\n"
    for category, values in result["identityDistribution"].items():
        if values:
            report += f"\n  {category}:\n"
            for value, count in values.items():
                report += f"    {value}: {count}\n"

    if result["agencyAnalysis"]["concerns"]:
        report += "\nAGENCY CONCERNS\n"
        for concern in result["agencyAnalysis"]["concerns"]:
            report += f"  ! {concern}\n"

    if result["survivalAnalysis"]["concerns"]:
        report += "\nSURVIVAL CONCERNS\n"
        for concern in result["survivalAnalysis"]["concerns"]:
            report += f"  ! {concern}\n"

    if result["tropeRisks"]:
        report += "\nTROPE RISKS\n"
        for risk in result["tropeRisks"]:
            report += f"  !! {risk}\n"

    if result["diversityNotes"]:
        report += "\nDIVERSITY NOTES\n"
        for note in result["diversityNotes"]:
            report += f"  * {note}\n"

    report += (
        "\nRECOMMENDATIONS\n"
        "\n"
        "1. Review any flagged trope risks carefully\n"
        "2. Consider agency distribution across identities\n"
        "3. If only one character of an identity, consider tokenism\n"
        "4. Ensure marginalized characters have their own stories/arcs\n"
        "5. Engage sensitivity readers for identities represented\n"
        "\n"
        "This analysis is based on data provided and cannot assess:\n"
        "  - Quality of representation within the narrative\n"
        "  - Stereotyping through characterization\n"
        "  - Authentic voice and experience\n"
        "  - Reception by affected communities\n"
    )

    return report


def show_example_format():
    """Return a string showing the expected JSON character format."""
    return (
        "\nCHARACTER JSON FORMAT\n"
        "=====================\n"
        "\n"
        "Create a JSON file with this structure:\n"
        "\n"
        "[\n"
        "  {\n"
        '    "name": "Maya Chen",\n'
        '    "role": "protagonist",\n'
        '    "identities": {\n'
        '      "race": "Chinese-American",\n'
        '      "gender": "woman",\n'
        '      "sexuality": "bisexual",\n'
        '      "disability": null,\n'
        '      "mentalHealth": null,\n'
        '      "religion": null\n'
        "    },\n"
        '    "agency": "high",\n'
        '    "arc": "positive",\n'
        '    "survives": true,\n'
        '    "notes": "Main character, drives the plot"\n'
        "  },\n"
        "  {\n"
        '    "name": "James Wright",\n'
        '    "role": "supporting",\n'
        '    "identities": {\n'
        '      "race": "white",\n'
        '      "gender": "man",\n'
        '      "sexuality": "straight"\n'
        "    },\n"
        '    "agency": "medium",\n'
        '    "arc": "flat",\n'
        '    "survives": true\n'
        "  },\n"
        "  {\n"
        '    "name": "Dr. Amara Okonkwo",\n'
        '    "role": "supporting",\n'
        '    "identities": {\n'
        '      "race": "Nigerian",\n'
        '      "gender": "woman",\n'
        '      "sexuality": "lesbian"\n'
        "    },\n"
        '    "agency": "high",\n'
        '    "arc": "positive",\n'
        '    "survives": false,\n'
        '    "notes": "Dies in chapter 15"\n'
        "  }\n"
        "]\n"
        "\n"
        "FIELDS:\n"
        "  name: Character name\n"
        "  role: protagonist | antagonist | supporting | minor\n"
        "  identities: Object with identity categories\n"
        "    - race: ethnic/racial identity\n"
        "    - gender: gender identity\n"
        "    - sexuality: sexual orientation\n"
        "    - disability: any disability\n"
        "    - mentalHealth: any mental health condition\n"
        "    - religion: religious identity\n"
        "    - class: socioeconomic class\n"
        "  agency: high | medium | low (how much they drive events)\n"
        "  arc: positive | negative | flat | none\n"
        "  survives: true | false (do they survive the story?)\n"
        "  notes: optional additional context\n"
    )


def show_usage():
    print(
        "\nRepresentation Map Tool\n"
        "=======================\n"
        "\n"
        "Analyzes character data to identify representation patterns.\n"
        "\n"
        "Usage:\n"
        "  python representation_map.py <characters.json>\n"
        "  python representation_map.py --format\n"
        "  python representation_map.py --json <characters.json>\n"
        "\n"
        "Options:\n"
        "  --format    Show the expected JSON format for character data\n"
        "  --json      Output results as JSON\n"
        "\n"
        "Detects:\n"
        "  - Identity distribution across characters\n"
        "  - Agency imbalances by identity\n"
        "  - Survival disparities (Bury Your Gays, etc.)\n"
        "  - Trope risks (Magical Minority, etc.)\n"
        "  - Tokenism indicators\n"
        "\n"
        "See --format for character JSON structure.\n"
    )


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------

def main():
    args = sys.argv[1:]

    if "--help" in args or "-h" in args:
        show_usage()
        sys.exit(0)

    if "--format" in args:
        print(show_example_format())
        sys.exit(0)

    use_json = "--json" in args

    if len(args) == 0 or args[0].startswith("--"):
        # Try to find a non-flag argument
        filename = None
        for a in args:
            if not a.startswith("--"):
                filename = a
                break
        if filename is None:
            show_usage()
            sys.exit(0)
    else:
        filename = args[0]

    try:
        with open(filename, "r", encoding="utf-8") as f:
            text = f.read()
        characters = json.loads(text)

        if not isinstance(characters, list):
            print("Error: JSON must be an array of character objects",
                  file=sys.stderr)
            sys.exit(1)

        result = analyze_characters(characters)

        if use_json:
            print(json.dumps(result, ensure_ascii=False, indent=2))
        else:
            print(format_report(result))

    except json.JSONDecodeError as e:
        print("Error: Invalid JSON format", file=sys.stderr)
        print(str(e), file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"Error reading file: {filename}", file=sys.stderr)
        print(str(e), file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
