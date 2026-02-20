#!/usr/bin/env python3
"""
extract_functions.py - DNA Extraction Tool

Interactive questionnaire for DNA extraction from existing works.
Guides through six-axis function analysis at configurable depth.

Usage:
  python extract_functions.py "Work Name"
  python extract_functions.py "Work Name" --depth quick
  python extract_functions.py --element "The Ghost"
  python extract_functions.py --validate extraction.json
  python extract_functions.py --template
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

EXTRACTION_QUESTIONS = {
    "structural": [
        "What would break in the plot if we removed this?",
        "What information does this control or reveal?",
        "What does this force to happen?",
        "What does this prevent from happening prematurely?"
    ],
    "character": [
        "What does this reveal about any character?",
        "How does this challenge or change a character?",
        "What choice does this force?",
        "Who does this illuminate through contrast?"
    ],
    "emotional": [
        "What should the audience feel here?",
        "How does this serve the genre promise?",
        "Is this a peak, valley, or sustain moment?",
        "What would be lost emotionally without this?"
    ],
    "thematic": [
        "What question does this raise or address?",
        "What value does this test?",
        "What does this symbolize?",
        "How does this complicate or reinforce the theme?"
    ],
    "relational": [
        "What connection does this create or strengthen?",
        "What tension does this generate between characters?",
        "How does this change the relationship web?",
        "What contrast does this establish?"
    ]
}

GENRE_OPTIONS = [
    "wonder", "idea", "adventure", "horror", "mystery",
    "thriller", "humor", "relationship", "drama", "issue", "ensemble"
]

SINCERITY_OPTIONS = [
    "high (earnest, characters mean what they say)",
    "medium (mix of sincere and ironic)",
    "low (ironic, detached, subtext-heavy)"
]

HUMOR_MODES = [
    "banter/quips", "deadpan", "physical/slapstick", "dark/gallows",
    "absurdist", "satirical", "minimal/serious"
]

CONFLICT_STYLES = [
    "verbal sparring", "cold silence", "explosive outbursts",
    "passive aggression", "physical violence", "avoidant/deflecting"
]

# == UTILITIES ==


def format_date():
    return date.today().isoformat()


def create_empty_extraction(work_name, depth):
    return {
        "_meta": {
            "type": "work-extraction",
            "source_work": work_name,
            "source_author": "",
            "source_medium": "",
            "extraction_date": format_date(),
            "extraction_depth": depth,
            "clusters": []
        },
        "emotional_core": {
            "primary_genre": "",
            "secondary_genres": [],
            "emotional_experience": "",
            "emotional_beats": []
        },
        "tone": {
            "sincerity_level": "",
            "humor_mode": "",
            "emotional_expression": "",
            "dialogue_density": "",
            "conflict_style": "",
            "baseline_tone": "",
            "tonal_shifts": []
        },
        "characters": {},
        "plot_structures": {},
        "relationships": {},
        "structural_requirements": [],
        "adaptable_without_breaking": [],
        "links": {
            "clusters": [],
            "similar_works": [],
            "derived_syntheses": []
        }
    }


def create_empty_element(name, element_type):
    return {
        "element_name": name,
        "element_type": element_type,
        "form": "",
        "functions": {
            "structural": [],
            "character": [],
            "emotional": [],
            "thematic": [],
            "relational": []
        },
        "structural_necessity": "medium",
        "adaptable_elements": []
    }


def format_extraction(extraction):
    lines = []

    lines.append("# DNA Extraction: " + extraction["_meta"]["source_work"])
    lines.append("")
    lines.append(f"**Author:** {extraction['_meta']['source_author'] or '(not specified)'}")
    lines.append(f"**Medium:** {extraction['_meta']['source_medium'] or '(not specified)'}")
    lines.append(f"**Extraction Depth:** {extraction['_meta']['extraction_depth']}")
    lines.append(f"**Date:** {extraction['_meta']['extraction_date']}")
    lines.append("")

    # Emotional Core
    lines.append("## Emotional Core")
    lines.append("")
    lines.append(f"**Primary Genre:** {extraction['emotional_core']['primary_genre'] or '(not identified)'}")
    if len(extraction["emotional_core"]["secondary_genres"]) > 0:
        lines.append(f"**Secondary Genres:** {', '.join(extraction['emotional_core']['secondary_genres'])}")
    lines.append("")
    lines.append(f"**Emotional Experience:** {extraction['emotional_core']['emotional_experience'] or '(not described)'}")
    lines.append("")

    if len(extraction["emotional_core"]["emotional_beats"]) > 0:
        lines.append("### Emotional Beats")
        for beat in extraction["emotional_core"]["emotional_beats"]:
            lines.append(f"- **{round(beat['position'] * 100)}%:** {beat['emotion']} ({beat['element']})")
        lines.append("")

    # Tone
    if extraction["tone"]["baseline_tone"]:
        lines.append("## Tone Profile")
        lines.append("")
        lines.append(f"**Baseline:** {extraction['tone']['baseline_tone']}")
        lines.append(f"**Sincerity:** {extraction['tone']['sincerity_level']}")
        lines.append(f"**Humor Mode:** {extraction['tone']['humor_mode']}")
        lines.append(f"**Emotional Expression:** {extraction['tone']['emotional_expression']}")
        lines.append(f"**Dialogue Density:** {extraction['tone']['dialogue_density']}")
        lines.append(f"**Conflict Style:** {extraction['tone']['conflict_style']}")
        lines.append("")

    # Characters
    char_names = list(extraction["characters"].keys())
    if len(char_names) > 0:
        lines.append("## Characters")
        lines.append("")
        for name in char_names:
            char = extraction["characters"][name]
            lines.append(f"### {name}")
            lines.append(f"**Form:** {char['form']}")
            lines.append(f"**Necessity:** {char['structural_necessity']}")
            lines.append("")

            if len(char["functions"]["structural"]) > 0:
                lines.append("**Structural Functions:**")
                for f in char["functions"]["structural"]:
                    lines.append(f"- {f}")
            if len(char["functions"]["character"]) > 0:
                lines.append("**Character Functions:**")
                for f in char["functions"]["character"]:
                    lines.append(f"- {f}")
            if len(char["functions"]["emotional"]) > 0:
                lines.append("**Emotional Functions:**")
                for f in char["functions"]["emotional"]:
                    lines.append(f"- {f}")
            if len(char["functions"]["relational"]) > 0:
                lines.append("**Relational Functions:**")
                for f in char["functions"]["relational"]:
                    lines.append(f"- {f}")
            if len(char["adaptable_elements"]) > 0:
                lines.append(f"**Adaptable:** {', '.join(char['adaptable_elements'])}")
            lines.append("")

    # Structural Requirements
    if len(extraction["structural_requirements"]) > 0:
        lines.append("## Structural Requirements")
        lines.append("")
        for req in extraction["structural_requirements"]:
            lines.append(f"- {req}")
        lines.append("")

    # Adaptable Elements
    if len(extraction["adaptable_without_breaking"]) > 0:
        lines.append("## Adaptable Without Breaking")
        lines.append("")
        for elem in extraction["adaptable_without_breaking"]:
            lines.append(f"- {elem}")
        lines.append("")

    # Clusters
    if len(extraction["_meta"]["clusters"]) > 0:
        lines.append("## Cluster Memberships")
        lines.append("")
        for cluster in extraction["_meta"]["clusters"]:
            lines.append(f"- {cluster}")
        lines.append("")

    return "\n".join(lines)


def format_element_extraction(element):
    lines = []

    lines.append(f"# Element Extraction: {element['element_name']}")
    lines.append("")
    lines.append(f"**Type:** {element['element_type']}")
    lines.append(f"**Form:** {element['form']}")
    lines.append(f"**Structural Necessity:** {element['structural_necessity']}")
    lines.append("")

    axes = ["structural", "character", "emotional", "thematic", "relational"]
    for axis in axes:
        funcs = element["functions"][axis]
        if len(funcs) > 0:
            lines.append(f"## {axis[0].upper() + axis[1:]} Functions")
            for f in funcs:
                lines.append(f"- {f}")
            lines.append("")

    if len(element["adaptable_elements"]) > 0:
        lines.append("## Adaptable Elements")
        for elem in element["adaptable_elements"]:
            lines.append(f"- {elem}")

    return "\n".join(lines)


def format_questionnaire(work_name, depth):
    lines = []

    lines.append(f"# DNA Extraction Questionnaire: {work_name}")
    lines.append(f"**Depth:** {depth}")
    lines.append("")
    lines.append("---")
    lines.append("")

    # Emotional Core Questions
    lines.append("## 1. Emotional Core")
    lines.append("")
    lines.append("### Primary Genre")
    lines.append("What emotional experience does this work primarily deliver?")
    lines.append(f"Options: {', '.join(GENRE_OPTIONS)}")
    lines.append("")
    lines.append("**Your answer:**")
    lines.append("")

    lines.append("### Secondary Genres (if any)")
    lines.append("What other emotional experiences does it layer in?")
    lines.append("")
    lines.append("**Your answer:**")
    lines.append("")

    lines.append("### Emotional Experience")
    lines.append("In one sentence, what does someone who LOVES this work love about it?")
    lines.append("")
    lines.append("**Your answer:**")
    lines.append("")

    if depth != "quick":
        lines.append("### Emotional Beats")
        lines.append("List 5-10 key emotional moments with approximate position (0.0-1.0):")
        lines.append("Format: position | emotion | element")
        lines.append("")
        lines.append("**Your answer:**")
        lines.append("")

    # Tone Questions (standard+)
    if depth != "quick":
        lines.append("---")
        lines.append("")
        lines.append("## 2. Tone Profile")
        lines.append("")

        lines.append("### Sincerity Level")
        lines.append("How earnest vs. ironic is the work?")
        for opt in SINCERITY_OPTIONS:
            lines.append(f"- {opt}")
        lines.append("")
        lines.append("**Your answer:**")
        lines.append("")

        lines.append("### Humor Mode")
        lines.append("When humor appears, what form does it take?")
        lines.append(f"Options: {', '.join(HUMOR_MODES)}")
        lines.append("")
        lines.append("**Your answer:**")
        lines.append("")

        lines.append("### Emotional Expression")
        lines.append("How do characters show/hide their feelings?")
        lines.append("(direct statement, subtext-heavy, action-reveals-feeling, denial/deflection)")
        lines.append("")
        lines.append("**Your answer:**")
        lines.append("")

        lines.append("### Dialogue Density")
        lines.append("Talk-to-action ratio? (quippy/rapid-fire, balanced, sparse/weighted silence)")
        lines.append("")
        lines.append("**Your answer:**")
        lines.append("")

        lines.append("### Conflict Style")
        lines.append("How do characters fight?")
        lines.append(f"Options: {', '.join(CONFLICT_STYLES)}")
        lines.append("")
        lines.append("**Your answer:**")
        lines.append("")

        lines.append("### Baseline Tone")
        lines.append("Describe the default emotional register in a phrase:")
        lines.append("")
        lines.append("**Your answer:**")
        lines.append("")

    # Character Questions
    lines.append("---")
    lines.append("")
    char_label = "3-5 main" if depth == "quick" else "all significant"
    lines.append(f"## 3. Characters ({char_label})")
    lines.append("")
    lines.append("For each character, answer:")
    lines.append("")
    lines.append("### Character: [NAME]")
    lines.append("")
    lines.append("**Form:** What are they on the surface?")
    lines.append("")

    for axis, questions in EXTRACTION_QUESTIONS.items():
        lines.append(f"**{axis[0].upper() + axis[1:]} Function:**")
        for q in questions:
            lines.append(f"- {q}")
        lines.append("")

    lines.append("**Structural Necessity:** high/medium/low")
    lines.append("**Adaptable Elements:** What about them could change?")
    lines.append("")
    lines.append("(Repeat for each character)")
    lines.append("")

    # Structural Requirements
    lines.append("---")
    lines.append("")
    lines.append("## 4. Structural Requirements")
    lines.append("")
    lines.append("What MUST be present for the story to work? (Not forms, but functions)")
    lines.append("Example: 'Protagonist must have privileged information others lack'")
    lines.append("")
    lines.append("**Your answer:**")
    lines.append("")

    # Adaptable Elements
    lines.append("---")
    lines.append("")
    lines.append("## 5. Adaptable Without Breaking")
    lines.append("")
    lines.append("What could change completely without breaking what makes this work?")
    lines.append("Example: 'Royal setting', 'Time period', 'Character genders'")
    lines.append("")
    lines.append("**Your answer:**")
    lines.append("")

    # Cluster Membership
    lines.append("---")
    lines.append("")
    lines.append("## 6. Cluster Membership")
    lines.append("")
    lines.append("What trope patterns does this belong to?")
    lines.append("Example: 'revenge-tragedy', 'found-family', 'bounty-hunter-scifi'")
    lines.append("")
    lines.append("**Your answer:**")
    lines.append("")

    return "\n".join(lines)


def validate_extraction(extraction):
    issues = []

    # Check required fields
    if not extraction.get("_meta", {}).get("source_work"):
        issues.append("Missing source work name")

    if not extraction.get("emotional_core", {}).get("primary_genre"):
        issues.append("Missing primary genre - emotional core not identified")

    if not extraction.get("emotional_core", {}).get("emotional_experience"):
        issues.append("Missing emotional experience description")

    # Check for characters
    characters = extraction.get("characters", {})
    char_count = len(characters)
    if char_count == 0:
        issues.append("No characters extracted")
    else:
        # Check each character
        for name, char in characters.items():
            all_functions = (
                char.get("functions", {}).get("structural", []) +
                char.get("functions", {}).get("character", []) +
                char.get("functions", {}).get("emotional", []) +
                char.get("functions", {}).get("thematic", []) +
                char.get("functions", {}).get("relational", [])
            )
            if len(all_functions) == 0:
                issues.append(f"Character '{name}' has no functions extracted")
            if not char.get("structural_necessity"):
                issues.append(f"Character '{name}' missing structural necessity rating")

    # Check structural requirements
    if len(extraction.get("structural_requirements", [])) == 0:
        issues.append("No structural requirements identified")

    # Check adaptable elements
    if len(extraction.get("adaptable_without_breaking", [])) == 0:
        issues.append("No adaptable elements identified - likely over-restricting")

    # Depth-specific checks
    if extraction.get("_meta", {}).get("extraction_depth") != "quick":
        if not extraction.get("tone", {}).get("baseline_tone"):
            issues.append("Standard/detailed extraction missing tone profile")
        if len(extraction.get("emotional_core", {}).get("emotional_beats", [])) == 0:
            issues.append("Standard/detailed extraction missing emotional beats")

    return {
        "valid": len(issues) == 0,
        "issues": issues
    }


# == MAIN ==

def main():
    args = sys.argv[1:]

    # Help
    if "--help" in args or "-h" in args:
        print("""Extract Functions - DNA Extraction Tool

Usage:
  python extract_functions.py "Work Name"
  python extract_functions.py "Work Name" --depth quick
  python extract_functions.py --element "The Ghost"
  python extract_functions.py --validate extraction.json
  python extract_functions.py --template

Options:
  --depth <level>    Extraction depth: quick, standard, detailed (default: standard)
  --element <name>   Extract single element instead of full work
  --validate <file>  Validate existing extraction file
  --template         Output blank extraction template
  --json             Output as JSON instead of markdown
  --questionnaire    Output questionnaire format for manual completion

Depth Levels:
  quick     - 15-30 min: Core functions, primary genre, 3-5 characters
  standard  - 1-3 hours: Full extraction with tone and relationships
  detailed  - 4-8 hours: Scene-level, episode structures, voice patterns

Examples:
  # Generate questionnaire for Hamlet
  python extract_functions.py "Hamlet" --questionnaire

  # Quick extraction template
  python extract_functions.py "Killjoys" --depth quick --template

  # Validate completed extraction
  python extract_functions.py --validate hamlet.json
""")
        sys.exit(0)

    # Parse arguments
    depth_index = args.index("--depth") if "--depth" in args else -1
    depth = args[depth_index + 1] if depth_index != -1 and depth_index + 1 < len(args) else "standard"

    element_index = args.index("--element") if "--element" in args else -1
    element_name = args[element_index + 1] if element_index != -1 and element_index + 1 < len(args) else None

    validate_index = args.index("--validate") if "--validate" in args else -1
    validate_file = args[validate_index + 1] if validate_index != -1 and validate_index + 1 < len(args) else None

    is_template = "--template" in args
    is_json = "--json" in args
    is_questionnaire = "--questionnaire" in args

    # Track consumed indices for positional arg detection
    skip_indices = set()
    if depth_index != -1:
        skip_indices.add(depth_index)
        skip_indices.add(depth_index + 1)
    if element_index != -1:
        skip_indices.add(element_index)
        skip_indices.add(element_index + 1)
    if validate_index != -1:
        skip_indices.add(validate_index)
        skip_indices.add(validate_index + 1)

    # Find positional argument (work name)
    work_name = None
    for i in range(len(args)):
        if not args[i].startswith("--") and i not in skip_indices:
            work_name = args[i]
            break

    # Handle validation mode
    if validate_file:
        try:
            content = open(validate_file, "r", encoding="utf-8").read()
            extraction = json.loads(content)
            result = validate_extraction(extraction)

            if is_json:
                print(json.dumps(result, indent=2, ensure_ascii=False))
            else:
                print(f"\nValidation Result: {'PASS' if result['valid'] else 'FAIL'}\n")
                if len(result["issues"]) > 0:
                    print("Issues found:")
                    for issue in result["issues"]:
                        print(f"  - {issue}")
                else:
                    print("Extraction is complete and ready for synthesis.")
        except Exception as e:
            print(f"Error reading/parsing {validate_file}: {e}", file=sys.stderr)
            sys.exit(1)
        return

    # Handle element extraction mode
    if element_name:
        element = create_empty_element(element_name, "other")

        if is_json:
            print(json.dumps(element, indent=2, ensure_ascii=False))
        else:
            print(format_element_extraction(element))
            print("\n---\n")
            print("## Extraction Questions\n")
            for axis, questions in EXTRACTION_QUESTIONS.items():
                print(f"### {axis[0].upper() + axis[1:]}")
                for q in questions:
                    print(f"- {q}")
                print("")
        return

    # Need work name for remaining modes
    if not work_name:
        print("Error: Please provide a work name or use --validate/--element flags", file=sys.stderr)
        print('Usage: python extract_functions.py "Work Name"', file=sys.stderr)
        sys.exit(1)

    # Handle questionnaire mode
    if is_questionnaire:
        print(format_questionnaire(work_name, depth))
        return

    # Handle template mode
    extraction = create_empty_extraction(work_name, depth)

    if is_json:
        print(json.dumps(extraction, indent=2, ensure_ascii=False))
    elif is_template:
        print(json.dumps(extraction, indent=2, ensure_ascii=False))
    else:
        # Default: output formatted markdown template with guidance
        print(format_extraction(extraction))
        print("\n---\n")
        print("## Next Steps\n")
        print("1. Use --questionnaire flag for guided extraction")
        print("2. Fill in extraction fields")
        print("3. Use --validate to check completeness")
        print(f'\nExample: python extract_functions.py "{work_name}" --questionnaire')


if __name__ == "__main__":
    main()
