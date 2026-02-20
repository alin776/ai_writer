#!/usr/bin/env python3
"""
synthesize.py - DNA Synthesis Tool

Interactive synthesis session from DNA documents.
Guides function-to-form mapping for adaptation projects.

Usage:
  python synthesize.py source.json --context "corporate dystopia"
  python synthesize.py source1.json source2.json --primary source1
  python synthesize.py --template
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

# == UTILITIES ==


def format_date():
    return date.today().isoformat()


def create_empty_synthesis(source_name, context, genre):
    return {
        "_meta": {
            "type": "synthesis",
            "synthesis_name": f"{source_name} in {context}",
            "target_context": context,
            "primary_source": source_name,
            "secondary_sources": [],
            "target_genre": genre,
            "synthesis_date": format_date()
        },
        "context_mapping": {
            "setting": "",
            "power_structure": "",
            "information_control": "",
            "escape_prevention": "",
            "typical_conflicts": ""
        },
        "function_to_form_mapping": {},
        "tone_synthesis": {
            "original_tone": "",
            "adapted_tone": "",
            "sincerity_level": "",
            "conflict_style": ""
        },
        "character_synthesis": {},
        "validation": {
            "genre_check": "pending",
            "function_coverage": "pending",
            "orthogonality_check": "pending",
            "context_coherence": "pending"
        },
        "ready_for": "in-progress"
    }


def format_synthesis_worksheet(synthesis, source):
    lines = []

    lines.append(f"# Synthesis Worksheet: {synthesis['_meta']['synthesis_name']}")
    lines.append("")
    lines.append(f"**Primary Source:** {synthesis['_meta']['primary_source']}")
    lines.append(f"**Target Context:** {synthesis['_meta']['target_context']}")
    lines.append(f"**Target Genre:** {synthesis['_meta']['target_genre']}")
    lines.append(f"**Date:** {synthesis['_meta']['synthesis_date']}")
    lines.append("")

    lines.append("---")
    lines.append("")

    # Section 1: Context Mapping
    lines.append("## 1. Context Mapping")
    lines.append("")
    lines.append("Define what elements in your target context will serve source functions.")
    lines.append("")
    lines.append("### Setting")
    lines.append("Where does this take place? Be specific about location, time period, social milieu.")
    lines.append("")
    lines.append("**Your answer:**")
    lines.append("")

    lines.append("### Power Structure")
    lines.append("How is power organized? Who has it? How is it contested?")
    lines.append("")
    lines.append("**Your answer:**")
    lines.append("")

    lines.append("### Information Control")
    lines.append("How is information controlled, shared, hidden? What makes something secret?")
    lines.append("")
    lines.append("**Your answer:**")
    lines.append("")

    lines.append("### Escape Prevention")
    lines.append("Why can't characters just leave? What traps them in the situation?")
    lines.append("")
    lines.append("**Your answer:**")
    lines.append("")

    lines.append("### Typical Conflicts")
    lines.append("What conflicts naturally arise in this context?")
    lines.append("")
    lines.append("**Your answer:**")
    lines.append("")

    lines.append("---")
    lines.append("")

    # Section 2: Function Mapping
    lines.append("## 2. Function-to-Form Mapping")
    lines.append("")
    lines.append("For each key function from the source, define a new form in your context.")
    lines.append("")
    lines.append("**Remember the orthogonality test:** Does the new form exist for its own reasons?")
    lines.append("Would someone unfamiliar with the source find it believable?")
    lines.append("")

    # If we have source DNA, list its structural requirements
    structural_reqs = source.get("structural_requirements") if source else None
    if structural_reqs:
        lines.append("### Source Structural Requirements")
        lines.append("")
        for req in structural_reqs:
            lines.append(f"- {req}")
        lines.append("")
        lines.append("### Map Each Requirement")
        lines.append("")

        for req in structural_reqs:
            short_name = req[:40] + ("..." if len(req) > 40 else "")
            lines.append(f'#### Function: "{short_name}"')
            lines.append("")
            lines.append("**Original form in source:** ")
            lines.append("")
            lines.append("**New form in your context:** ")
            lines.append("")
            lines.append("**Orthogonality check:** Does this form exist for its own reasons? (yes/no/needs work)")
            lines.append("")
            lines.append("**Functions served:** (list what this enables)")
            lines.append("- ")
            lines.append("")
    else:
        lines.append("### Key Functions to Map")
        lines.append("")
        lines.append("(Add functions from your source extraction)")
        lines.append("")
        lines.append('#### Function: "[describe function]"')
        lines.append("")
        lines.append("**Original form in source:** ")
        lines.append("")
        lines.append("**New form in your context:** ")
        lines.append("")
        lines.append("**Orthogonality check:** ")
        lines.append("")
        lines.append("**Functions served:**")
        lines.append("- ")
        lines.append("")

    lines.append("---")
    lines.append("")

    # Section 3: Tone Synthesis
    lines.append("## 3. Tone Synthesis")
    lines.append("")

    source_tone = source.get("tone") if source else None
    if source_tone:
        lines.append("### Source Tone")
        lines.append(f"- Sincerity: {source_tone.get('sincerity_level', '')}")
        lines.append(f"- Conflict style: {source_tone.get('conflict_style', '')}")
        lines.append(f"- Baseline: {source_tone.get('baseline_tone', '')}")
        lines.append("")

    lines.append("### Adapted Tone")
    lines.append("")
    lines.append("**Original tone summary:**")
    lines.append("")
    lines.append("**How will you adapt it to your context?**")
    lines.append("")
    lines.append("**Sincerity level:** (high/medium/low)")
    lines.append("")
    lines.append("**Conflict style:** (verbal sparring, cold silence, explosive, etc.)")
    lines.append("")

    lines.append("---")
    lines.append("")

    # Section 4: Character Synthesis
    lines.append("## 4. Character Synthesis")
    lines.append("")

    source_chars = source.get("characters") if source else None
    if source_chars:
        lines.append("### Source Characters")
        lines.append("")
        for name, char in source_chars.items():
            lines.append(f"#### {name}")
            lines.append(f"Original form: {char.get('form', '')}")
            char_funcs = char.get("functions", {})
            structural_funcs = char_funcs.get("structural", [])
            if structural_funcs:
                lines.append("Key functions: " + "; ".join(structural_funcs[:2]))
            lines.append("")
        lines.append("")

    lines.append("### Your Adapted Characters")
    lines.append("")
    lines.append("#### Protagonist")
    lines.append("")
    lines.append("**New name:**")
    lines.append("")
    lines.append("**Based on functions from:** (source character name)")
    lines.append("")
    lines.append("**New form:** (describe who they are in your context)")
    lines.append("")
    lines.append("**Arc:** (brief transformation description)")
    lines.append("")
    lines.append("(Repeat for other key characters)")
    lines.append("")

    lines.append("---")
    lines.append("")

    # Section 5: Validation
    lines.append("## 5. Validation Checklist")
    lines.append("")
    lines.append("Before proceeding, verify:")
    lines.append("")
    lines.append("- [ ] **Genre check:** Does this deliver " + synthesis["_meta"]["target_genre"] + " emotional experience?")
    lines.append("- [ ] **Function coverage:** Are all structural requirements from source addressed?")
    lines.append("- [ ] **Orthogonality check:** Do all new forms exist for their own reasons?")
    lines.append("- [ ] **Context coherence:** Do all elements fit naturally in the target context?")
    lines.append("- [ ] **Tone alignment:** Does the adapted tone serve the emotional experience?")
    lines.append("")

    lines.append("---")
    lines.append("")
    lines.append("## When Complete")
    lines.append("")
    lines.append("Run validation: python validate_synthesis.py your-synthesis.json")
    lines.append("")
    lines.append("Then proceed to outline-collaborator or drafting skill.")

    return "\n".join(lines)


def format_synthesis_template():
    return json.dumps({
        "_meta": {
            "type": "synthesis",
            "synthesis_name": "Your Synthesis Name",
            "target_context": "describe target context",
            "primary_source": "source-dna.json",
            "secondary_sources": [],
            "target_genre": "drama",
            "synthesis_date": format_date()
        },
        "context_mapping": {
            "setting": "Where and when",
            "power_structure": "How power is organized",
            "information_control": "How secrets work",
            "escape_prevention": "Why characters can't leave",
            "typical_conflicts": "What conflicts arise naturally"
        },
        "function_to_form_mapping": {
            "function_name": {
                "original_form": "what it was in source",
                "new_form": "what it is in your version",
                "orthogonality_check": "pass/fail/needs work",
                "functions_served": ["list", "of", "functions"]
            }
        },
        "tone_synthesis": {
            "original_tone": "describe source tone",
            "adapted_tone": "describe your tone",
            "sincerity_level": "high/medium/low",
            "conflict_style": "how characters fight"
        },
        "character_synthesis": {
            "protagonist": {
                "new_name": "Character Name",
                "original_functions_from": "source character",
                "new_form": "who they are in your context",
                "arc": "their transformation"
            }
        },
        "validation": {
            "genre_check": "pending",
            "function_coverage": "pending",
            "orthogonality_check": "pending",
            "context_coherence": "pending"
        },
        "ready_for": "in-progress"
    }, indent=2, ensure_ascii=False)


def format_combination_guidance(primary, secondary):
    lines = []

    lines.append("# Combining Multiple Sources")
    lines.append("")
    lines.append(f"**Primary source:** {primary}")
    lines.append(f"**Secondary sources:** {', '.join(secondary)}")
    lines.append("")

    lines.append("## Combination Rules")
    lines.append("")
    lines.append("1. **Primary source functions take precedence** when sources conflict")
    lines.append("2. **Secondary sources add flavor**, not structure")
    lines.append("3. **Identify conflicts early** - where do sources want different things?")
    lines.append("")

    lines.append("## Conflict Resolution Options")
    lines.append("")
    lines.append("When functions conflict, choose one approach:")
    lines.append("")
    lines.append("- **Primary wins:** Keep primary's version, drop secondary's")
    lines.append("- **Blend:** Find middle ground that partially serves both")
    lines.append("- **Alternate:** Different parts of work serve different sources")
    lines.append("- **Transform:** Conflict becomes a feature (tension between approaches)")
    lines.append("")

    lines.append("## Process")
    lines.append("")
    lines.append("1. List all functions from primary source")
    lines.append("2. List functions from secondary sources")
    lines.append("3. Identify overlaps (complementary)")
    lines.append("4. Identify conflicts (incompatible)")
    lines.append("5. Resolve each conflict using options above")
    lines.append("6. Proceed with combined function list")
    lines.append("")

    return "\n".join(lines)


# == MAIN ==

def main():
    args = sys.argv[1:]

    # Help
    if "--help" in args or "-h" in args:
        print("""Synthesize - DNA Synthesis Tool

Usage:
  python synthesize.py source.json --context "corporate dystopia"
  python synthesize.py source1.json source2.json --primary source1.json
  python synthesize.py --template
  python synthesize.py --function "proximity to power" --context scifi

Options:
  --context <desc>   Target context/setting for synthesis
  --genre <name>     Target genre (default: from source)
  --primary <file>   When combining sources, which is primary
  --template         Output blank synthesis template (JSON)
  --worksheet        Output guided worksheet (markdown)
  --json             Output as JSON instead of markdown
  --function <name>  Generate form options for specific function (uses form-options)

Examples:
  # Start synthesis worksheet from Hamlet extraction
  python synthesize.py hamlet.json --context "corporate dystopia" --worksheet

  # Get blank template
  python synthesize.py --template

  # Combine two sources
  python synthesize.py hamlet.json killjoys.json --primary hamlet.json --context scifi
""")
        sys.exit(0)

    is_json = "--json" in args
    is_worksheet = "--worksheet" in args
    is_template = "--template" in args

    # Handle --template
    if is_template:
        print(format_synthesis_template())
        return

    # Parse arguments
    context_index = args.index("--context") if "--context" in args else -1
    context = args[context_index + 1] if context_index != -1 and context_index + 1 < len(args) else None

    genre_index = args.index("--genre") if "--genre" in args else -1
    genre = args[genre_index + 1] if genre_index != -1 and genre_index + 1 < len(args) else None

    primary_index = args.index("--primary") if "--primary" in args else -1
    primary_file = args[primary_index + 1] if primary_index != -1 and primary_index + 1 < len(args) else None

    # Find source files (positional arguments)
    skip_indices = set()
    for idx in [context_index, genre_index, primary_index]:
        if idx != -1:
            skip_indices.add(idx)
            skip_indices.add(idx + 1)

    source_files = []
    for i in range(len(args)):
        if not args[i].startswith("--") and i not in skip_indices and args[i].endswith(".json"):
            source_files.append(args[i])

    if len(source_files) == 0:
        print("Error: Please provide at least one source DNA file", file=sys.stderr)
        print('Usage: python synthesize.py source.json --context "corporate"', file=sys.stderr)
        print("       python synthesize.py --template", file=sys.stderr)
        sys.exit(1)

    if not context:
        print("Error: Please provide target context with --context", file=sys.stderr)
        print('Example: --context "corporate dystopia"', file=sys.stderr)
        sys.exit(1)

    # Load primary source
    primary_source = primary_file or source_files[0]
    source = None

    try:
        content = open(primary_source, "r", encoding="utf-8").read()
        source = json.loads(content)
    except Exception as e:
        print(f"Error reading source file {primary_source}: {e}", file=sys.stderr)
        sys.exit(1)

    # Determine genre
    target_genre = genre
    if not target_genre and source:
        target_genre = source.get("emotional_core", {}).get("primary_genre", "")
    if not target_genre:
        target_genre = "drama"

    # Create synthesis document
    source_name = ""
    if source:
        source_name = source.get("_meta", {}).get("source_work", "")
    if not source_name:
        source_name = primary_source.replace(".json", "")
    synthesis = create_empty_synthesis(source_name, context, target_genre)

    # Add secondary sources if multiple files
    if len(source_files) > 1:
        synthesis["_meta"]["secondary_sources"] = [f for f in source_files if f != primary_source]

    # Output
    if len(source_files) > 1 and not is_worksheet and not is_json:
        # Show combination guidance first
        print(format_combination_guidance(primary_source, synthesis["_meta"]["secondary_sources"]))
        print("\n---\n")

    if is_json:
        print(json.dumps(synthesis, indent=2, ensure_ascii=False))
    else:
        # Default to worksheet
        print(format_synthesis_worksheet(synthesis, source))


if __name__ == "__main__":
    main()
