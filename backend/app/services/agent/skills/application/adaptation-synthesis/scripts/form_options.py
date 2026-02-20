#!/usr/bin/env python3
"""
form_options.py - Form Options Generator

Generates setting-appropriate forms for abstract story functions.
Helps avoid surface-level translations by providing multiple options.

Usage:
  python form_options.py "proximity to power" --setting corporate
  python form_options.py "privileged information" --setting scifi --count 5
  python form_options.py --list-functions
  python form_options.py --list-settings
"""

import sys
import os
import json
import re
from datetime import date

# Ensure UTF-8 output on all platforms
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")
if hasattr(sys.stderr, "reconfigure"):
    sys.stderr.reconfigure(encoding="utf-8")

# == DATA ==

FUNCTIONS = {
    "proximity_to_power": {
        "description": "Character has access to power center without being the power holder",
        "forms": {
            "corporate": [
                "Executive assistant to CEO",
                "CFO's protege/mentee",
                "Board member's adult child working at company",
                "Head of compliance with reporting access",
                "In-house counsel with privileged access",
                "Chief of staff to founder"
            ],
            "political": [
                "Senator's chief of staff",
                "Press secretary",
                "Campaign manager",
                "Speech writer with inner circle access",
                "Security detail member"
            ],
            "criminal": [
                "Consigliere/advisor to boss",
                "Boss's child being groomed",
                "Longtime underboss",
                "Accountant who knows the books"
            ],
            "military": [
                "General's aide-de-camp",
                "Intelligence analyst with top clearance",
                "Communications officer",
                "Medical officer to commanding officer"
            ],
            "academic": [
                "Department chair's research assistant",
                "Dean's executive assistant",
                "Board of trustees member's researcher"
            ],
            "scifi": [
                "Station commander's second",
                "Ship AI with bridge access",
                "Colony administrator's liaison",
                "Corporate rep on mining operation"
            ],
            "fantasy": [
                "Royal advisor/counselor",
                "Court mage",
                "Heir's sworn protector",
                "Seneschal of the castle"
            ]
        }
    },
    "privileged_information": {
        "description": "Character learns something they cannot prove or verify",
        "forms": {
            "corporate": [
                "Overheard conversation through thin wall",
                "Accessed sealed files through inherited login",
                "Dying confession from mentor",
                "Anonymous whistleblower tip",
                "Discovered through legally questionable means"
            ],
            "political": [
                "Off-record conversation at private event",
                "Classified document briefly glimpsed",
                "Testimony from discredited source"
            ],
            "criminal": [
                "Deathbed confession",
                "Information from witness now dead",
                "Evidence obtained through illegal search"
            ],
            "scifi": [
                "Corrupted data transmission, partially decoded",
                "AI prediction based on incomplete data",
                "Time-loop knowledge others don't share",
                "Alien communication of uncertain meaning"
            ],
            "fantasy": [
                "Vision from unreliable oracle",
                "Message from the dead via medium",
                "Dream sent by unknown power",
                "Prophecy with multiple interpretations"
            ]
        }
    },
    "cannot_escape": {
        "description": "Character is trapped in situation, cannot simply leave",
        "forms": {
            "corporate": [
                "Non-compete prevents industry change",
                "Stock options vest over years",
                "Family also employed there",
                "Industry blacklisting threat",
                "Visa tied to employment"
            ],
            "political": [
                "Public office term commitment",
                "Party loyalty obligations",
                "Classified knowledge requiring clearance",
                "Constituents depending on presence"
            ],
            "criminal": [
                "Knowledge that makes leaving dangerous",
                "Family held as leverage",
                "Too much complicity to walk away"
            ],
            "scifi": [
                "Generation ship with nowhere to go",
                "Implant that tracks/controls",
                "Terraforming contract with decades remaining",
                "Quarantine zone containment"
            ],
            "fantasy": [
                "Magical binding/oath",
                "Curse that prevents leaving",
                "Sacred duty/prophecy",
                "Blood debt requiring service"
            ],
            "domestic": [
                "Shared custody of children",
                "Underwater mortgage",
                "Caregiving responsibility",
                "Small town with no alternatives"
            ]
        }
    },
    "entrenched_antagonist": {
        "description": "Antagonist cannot be easily removed or defeated",
        "forms": {
            "corporate": [
                "Founder with voting control",
                "CEO with board loyalty",
                "Too-big-to-fail connected executive",
                "Family ownership structure"
            ],
            "political": [
                "Popular incumbent with party backing",
                "Intelligence with compromising material",
                "Systemic corruption requiring many takedowns"
            ],
            "institutional": [
                "Tenure protecting position",
                "Bureaucratic process requiring years",
                "Union protections"
            ],
            "scifi": [
                "AI with distributed backup",
                "Corporate entity with system-wide reach",
                "Government with surveillance network"
            ],
            "fantasy": [
                "Immortal or near-immortal",
                "Protected by prophecy",
                "Bound to realm's existence"
            ]
        }
    },
    "innocent_bystanders": {
        "description": "Protagonist's action or inaction affects innocent people",
        "forms": {
            "corporate": [
                "Employees who would lose jobs",
                "Consumers using unsafe product",
                "Pension fund at risk",
                "Supply chain workers"
            ],
            "political": [
                "Constituents affected by policy",
                "Staff careers at stake",
                "Witnesses who could be targeted"
            ],
            "criminal": [
                "Family of target",
                "Witnesses to be silenced",
                "Community affected by operation"
            ],
            "scifi": [
                "Colony dependent on protagonist's system",
                "Passengers on ship",
                "Populations unaware of threat"
            ],
            "fantasy": [
                "Villagers caught between factions",
                "Those protected by current order",
                "Innocents touched by magical conflict"
            ]
        }
    },
    "dark_mirror": {
        "description": "Character showing protagonist what they could become",
        "forms": {
            "corporate": [
                "Predecessor who made the compromise",
                "Rival who chose the corrupt path",
                "Mentor who crossed the line long ago"
            ],
            "political": [
                "Former idealist now cynical operator",
                "Opposition figure with same origins",
                "Predecessor in same position"
            ],
            "criminal": [
                "Partner who went too far",
                "Boss who was once like protagonist",
                "Former ally now enemy"
            ],
            "scifi": [
                "Clone/copy who diverged",
                "Parallel universe self",
                "AI trained on protagonist's patterns"
            ],
            "fantasy": [
                "Previous chosen one who fell",
                "Teacher who became what they fought",
                "Corrupted version from alternate timeline"
            ]
        }
    },
    "found_family": {
        "description": "Group of unrelated people functioning as family unit",
        "forms": {
            "corporate": [
                "Startup founding team",
                "Night shift workers at isolated location",
                "Remote project team",
                "Specialized department"
            ],
            "criminal": [
                "Heist crew",
                "Smuggling operation",
                "Resistance cell"
            ],
            "scifi": [
                "Ship crew",
                "Colony founding team",
                "Salvage operation",
                "Research station personnel"
            ],
            "fantasy": [
                "Adventuring party",
                "Mercenary company",
                "Monastery/order members",
                "Traveling performers"
            ],
            "domestic": [
                "Roommates who became family",
                "Support group members",
                "Hobby club with deep bonds"
            ]
        }
    },
    "mobile_base": {
        "description": "Base of operations that can travel to stories",
        "forms": {
            "contemporary": [
                "RV/bus/converted vehicle",
                "Hotel lifestyle",
                "Private plane with traveling staff"
            ],
            "criminal": [
                "Series of safe houses",
                "Front business with multiple locations",
                "Boat that moves between ports"
            ],
            "scifi": [
                "Spaceship",
                "Mobile station",
                "Jump-capable vessel"
            ],
            "fantasy": [
                "Enchanted carriage",
                "Flying ship",
                "Pocket dimension anchored to object"
            ],
            "western": [
                "Train car",
                "Wagon train",
                "Circuit rider route"
            ]
        }
    }
}

SETTINGS = [
    "corporate", "political", "criminal", "military", "academic",
    "medical", "scifi", "fantasy", "domestic", "western", "contemporary"
]

# == UTILITIES ==


def fuzzy_match_function(query):
    normalized = re.sub(r"[^a-z]", "_", query.lower())

    # Direct match
    if normalized in FUNCTIONS:
        return normalized

    # Partial match
    for key in FUNCTIONS.keys():
        if normalized in key or key.replace("_", "") in normalized.replace("_", ""):
            return key

    # Word match
    query_words = [w for w in normalized.split("_") if len(w) > 2]
    for key in FUNCTIONS.keys():
        key_words = key.split("_")
        if any(any(kw in qw or qw in kw for kw in key_words) for qw in query_words):
            return key

    return None


def generate_orthogonality_notes(forms):
    return [
        "Good form if it exists for its own reasons in this setting",
        "Check: Would someone unfamiliar with source find this believable?",
        "Avoid: Picking a form just because it's 'equivalent' to original",
        "Test: Can you describe this without mentioning the source work?"
    ]


def format_form_suggestion(suggestion):
    lines = []

    lines.append(f"# Form Options: \"{suggestion['function_name'].replace('_', ' ')}\"")
    lines.append("")
    lines.append(f"**Function:** {suggestion['function_description']}")
    lines.append(f"**Setting:** {suggestion['setting']}")
    lines.append("")

    lines.append("## Available Forms")
    lines.append("")
    for i in range(len(suggestion["forms"])):
        lines.append(f"{i + 1}. {suggestion['forms'][i]}")
    lines.append("")

    lines.append("## Orthogonality Check")
    lines.append("")
    lines.append("Before selecting a form, verify:")
    lines.append("")
    for note in suggestion["orthogonality_notes"]:
        lines.append(f"- {note}")
    lines.append("")

    lines.append("## Selection Guidance")
    lines.append("")
    lines.append("The best form is one that:")
    lines.append("1. Serves the function in your story")
    lines.append("2. Exists naturally in your setting")
    lines.append("3. Has its own internal logic (not 'because the original had X')")
    lines.append("4. Could be explained without referencing the source")
    lines.append("")

    return "\n".join(lines)


def list_functions():
    lines = []
    lines.append("# Available Functions")
    lines.append("")
    for key, data in FUNCTIONS.items():
        lines.append(f"## {key.replace('_', ' ')}")
        lines.append(data["description"])
        lines.append(f"Settings: {', '.join(data['forms'].keys())}")
        lines.append("")
    return "\n".join(lines)


def list_settings():
    lines = []
    lines.append("# Available Settings")
    lines.append("")
    for setting in SETTINGS:
        function_count = sum(1 for f in FUNCTIONS.values() if setting in f["forms"])
        lines.append(f"- **{setting}**: {function_count} functions with forms")
    lines.append("")
    lines.append("Note: Not all functions have forms for all settings.")
    lines.append("You can request forms for any setting; if not predefined,")
    lines.append("the tool will suggest you brainstorm based on setting context.")
    return "\n".join(lines)


# == MAIN ==

def main():
    args = sys.argv[1:]

    # Help
    if "--help" in args or "-h" in args:
        print("""Form Options Generator

Usage:
  python form_options.py "function name" --setting <setting>
  python form_options.py --list-functions
  python form_options.py --list-settings

Options:
  --setting <name>     Target setting (corporate, political, scifi, etc.)
  --count <n>          Limit number of forms returned
  --list-functions     Show all available functions
  --list-settings      Show all available settings
  --json               Output as JSON
  --constraint <text>  Add constraint to filter forms

Examples:
  # Get corporate forms for proximity to power
  python form_options.py "proximity to power" --setting corporate

  # Get sci-fi forms with constraint
  python form_options.py "cannot escape" --setting scifi --constraint "no supernatural"

  # List what's available
  python form_options.py --list-functions
""")
        sys.exit(0)

    is_json = "--json" in args

    # Handle --list-functions
    if "--list-functions" in args:
        if is_json:
            listing = {}
            for key, data in FUNCTIONS.items():
                listing[key] = data["description"]
            print(json.dumps(listing, indent=2, ensure_ascii=False))
        else:
            print(list_functions())
        return

    # Handle --list-settings
    if "--list-settings" in args:
        if is_json:
            print(json.dumps(SETTINGS, indent=2, ensure_ascii=False))
        else:
            print(list_settings())
        return

    # Parse arguments
    setting_index = args.index("--setting") if "--setting" in args else -1
    setting = args[setting_index + 1] if setting_index != -1 and setting_index + 1 < len(args) else None

    count_index = args.index("--count") if "--count" in args else -1
    count = int(args[count_index + 1]) if count_index != -1 and count_index + 1 < len(args) else None

    constraint_index = args.index("--constraint") if "--constraint" in args else -1
    constraint = args[constraint_index + 1] if constraint_index != -1 and constraint_index + 1 < len(args) else None

    # Track skip indices for positional arg detection
    skip_indices = set()
    for idx in [setting_index, count_index, constraint_index]:
        if idx != -1:
            skip_indices.add(idx)
            skip_indices.add(idx + 1)

    # Find function query (positional argument)
    function_query = None
    for i in range(len(args)):
        if not args[i].startswith("--") and i not in skip_indices:
            function_query = args[i]
            break

    if not function_query:
        print("Error: Please provide a function name", file=sys.stderr)
        print('Usage: python form_options.py "proximity to power" --setting corporate', file=sys.stderr)
        print("       python form_options.py --list-functions", file=sys.stderr)
        sys.exit(1)

    if not setting:
        print("Error: Please provide a setting with --setting", file=sys.stderr)
        print("Example: --setting corporate", file=sys.stderr)
        print("Use --list-settings to see available settings", file=sys.stderr)
        sys.exit(1)

    # Match function
    matched_function = fuzzy_match_function(function_query)

    if not matched_function:
        print(f'Error: No function matching "{function_query}"', file=sys.stderr)
        print("Use --list-functions to see available functions", file=sys.stderr)
        sys.exit(1)

    func_data = FUNCTIONS[matched_function]
    forms = list(func_data["forms"].get(setting, []))

    # If no forms for this setting, provide guidance
    if len(forms) == 0:
        if is_json:
            print(json.dumps({
                "function_name": matched_function,
                "setting": setting,
                "forms": [],
                "note": f"No predefined forms for {setting}. Consider what in {setting} context could serve: {func_data['description']}"
            }, indent=2, ensure_ascii=False))
        else:
            print(f'# No predefined forms for "{matched_function}" in "{setting}"\n')
            print(f"Function: {func_data['description']}\n")
            print("Brainstorming questions:")
            print(f"- What in a {setting} context creates {matched_function.replace('_', ' ')}?")
            print(f"- What {setting}-specific structures could serve this function?")
            print(f"- What do characters in {setting} settings have access to/constraints from?")
        return

    # Apply constraint filter (basic keyword filtering)
    if constraint:
        constraint_lower = constraint.lower()
        forms = [f for f in forms if constraint_lower not in f.lower()]

    # Apply count limit
    if count and count < len(forms):
        forms = forms[:count]

    # Build output
    suggestion = {
        "function_name": matched_function,
        "function_description": func_data["description"],
        "setting": setting,
        "forms": forms,
        "orthogonality_notes": generate_orthogonality_notes(forms)
    }

    if is_json:
        print(json.dumps(suggestion, indent=2, ensure_ascii=False))
    else:
        print(format_form_suggestion(suggestion))


if __name__ == "__main__":
    main()
