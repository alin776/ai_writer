#!/usr/bin/env python3
"""
structural_stylistic.py - Structural vs Stylistic Classification

Helps classify story elements as structural (must keep for story to work)
or stylistic (can be adapted without breaking the story).

Usage:
  python structural_stylistic.py "royal court setting"
  python structural_stylistic.py --batch elements.json
  python structural_stylistic.py --examples
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

CLASSIFICATION_QUESTIONS = [
    {
        "question": "If you removed this completely, would the plot still be possible?",
        "structural_answer": "No - the plot depends on this element existing",
        "stylistic_answer": "Yes - the plot could work without it or with a substitute",
        "weight": 3
    },
    {
        "question": "Could a different form serve the same story function?",
        "structural_answer": "No - this specific form is required",
        "stylistic_answer": "Yes - many different forms could serve the same function",
        "weight": 3
    },
    {
        "question": "Is this element specific to the time/place/culture, or universal?",
        "structural_answer": "It embodies a universal that MUST be present",
        "stylistic_answer": "It's a specific expression of something that could be expressed differently",
        "weight": 2
    },
    {
        "question": "Would changing this require changing the character arcs?",
        "structural_answer": "Yes - character transformations depend on this",
        "stylistic_answer": "No - characters could transform the same way with a different version",
        "weight": 2
    },
    {
        "question": "Does the emotional experience of the story require this specific element?",
        "structural_answer": "Yes - the genre promise depends on this",
        "stylistic_answer": "No - the emotional experience could be achieved differently",
        "weight": 2
    },
    {
        "question": "Is this element what audiences remember and love, or is it incidental?",
        "structural_answer": "This IS what they love - it defines the work",
        "stylistic_answer": "They love what this enables, not this specifically",
        "weight": 1
    },
    {
        "question": "Would the theme/meaning change if this element changed?",
        "structural_answer": "Yes - the theme is embodied in this specific element",
        "stylistic_answer": "No - the theme could be explored through different elements",
        "weight": 2
    }
]

EXAMPLES = {
    "clearly_structural": [
        {
            "element": "Hamlet's uncertainty about the ghost's truthfulness",
            "reasoning": "The entire plot hinges on Hamlet's inability to act due to uncertainty. Remove this, and you remove the central dramatic engine.",
            "functions": ["Creates the central conflict", "Enables the delay that defines the character", "Generates the play-within-a-play"]
        },
        {
            "element": "The mystery structure in a detective story",
            "reasoning": "A mystery without a puzzle to solve isn't a mystery. The structure IS the genre promise.",
            "functions": ["Delivers the genre promise", "Creates reader engagement through problem-solving", "Provides satisfaction of revelation"]
        },
        {
            "element": "Romeo and Juliet's families being enemies",
            "reasoning": "The tragedy requires the love to be forbidden. Without opposing families (or equivalent), there's no star-crossed element.",
            "functions": ["Creates the central obstacle", "Makes the romance tragic rather than simple", "Forces the fatal decisions"]
        }
    ],
    "clearly_stylistic": [
        {
            "element": "The specific time period (Renaissance Denmark in Hamlet)",
            "reasoning": "Hamlet has been successfully set in modern times, corporate settings, etc. The period is characteristic but not essential.",
            "alternatives": ["Corporate boardroom", "Political dynasty", "Mafia family", "Any power structure with succession"]
        },
        {
            "element": "Shakespeare's iambic pentameter",
            "reasoning": "The language style is beautiful but adaptations in prose, modern English, or other languages preserve the story.",
            "alternatives": ["Modern English", "Film dialogue", "Any language that can express the ideas"]
        },
        {
            "element": "The specific occupations in a romance",
            "reasoning": "Whether characters are doctors, lawyers, or baristas usually doesn't affect the romantic arc.",
            "alternatives": ["Any occupation that provides the needed access/conflict/status"]
        }
    ],
    "requires_analysis": [
        {
            "element": "Hamlet being a prince",
            "analysis": "This seems stylistic (could be any insider-to-power) but the specific functions require examination: proximity to power, obligation through birth, inability to simply leave. These functions could be served by other forms.",
            "likely_classification": "stylistic",
            "functions_to_preserve": ["Proximity to power center", "Inherited obligation", "Cannot easily escape situation"]
        },
        {
            "element": "The ghost in Hamlet",
            "analysis": "The supernatural element seems essential but the FUNCTION (delivering unverifiable privileged information that creates obligation) could be served by: dying message, discovered evidence, testimony from unreliable source.",
            "likely_classification": "stylistic (the specific form), structural (the function)",
            "functions_to_preserve": ["Provides information protagonist cannot verify", "Creates moral obligation not chosen", "Introduces uncertainty about truth"]
        },
        {
            "element": "The ship in bounty hunter sci-fi",
            "analysis": "Mobile base that enables case-of-the-week structure. Could be other mobile platforms (RV, train, etc.) but the 'crew lives together in mobile home' function is structural to the subgenre.",
            "likely_classification": "function is structural, specific form is stylistic",
            "functions_to_preserve": ["Mobile base for travel", "Crew living quarters for relationship development", "Home that travels to stories"]
        }
    ]
}

# == UTILITIES ==


def format_questionnaire(element):
    lines = []

    lines.append(f'# Structural vs Stylistic Classification: "{element}"')
    lines.append("")
    lines.append("Answer each question to determine if this element is structural (must keep)")
    lines.append("or stylistic (can adapt to a different form).")
    lines.append("")
    lines.append("---")
    lines.append("")

    for i in range(len(CLASSIFICATION_QUESTIONS)):
        q = CLASSIFICATION_QUESTIONS[i]
        lines.append(f"## Question {i + 1} (Weight: {q['weight']})")
        lines.append("")
        lines.append(f"**{q['question']}**")
        lines.append("")
        lines.append(f"- [ ] **Structural:** {q['structural_answer']}")
        lines.append(f"- [ ] **Stylistic:** {q['stylistic_answer']}")
        lines.append("")

    lines.append("---")
    lines.append("")
    lines.append("## Additional Analysis")
    lines.append("")
    lines.append("### Functions this element serves:")
    lines.append("(List what this element DOES in the story)")
    lines.append("")
    lines.append("1. ")
    lines.append("2. ")
    lines.append("3. ")
    lines.append("")
    lines.append("### Alternative forms that could serve these functions:")
    lines.append("(If stylistic, what else could work?)")
    lines.append("")
    lines.append("1. ")
    lines.append("2. ")
    lines.append("3. ")
    lines.append("")
    lines.append("### Final Classification:")
    lines.append("")
    lines.append("- [ ] **Structural** - Cannot be changed without breaking the story")
    lines.append("- [ ] **Stylistic** - Can be adapted to different forms")
    lines.append("- [ ] **Mixed** - Function is structural, specific form is stylistic")
    lines.append("")

    return "\n".join(lines)


def format_examples():
    lines = []

    lines.append("# Structural vs Stylistic: Examples")
    lines.append("")
    lines.append("Understanding the difference between what MUST stay and what CAN change.")
    lines.append("")

    lines.append("## Clearly Structural Elements")
    lines.append("")
    lines.append("These cannot be changed without breaking the story:")
    lines.append("")

    for ex in EXAMPLES["clearly_structural"]:
        lines.append(f'### "{ex["element"]}"')
        lines.append("")
        lines.append(f"**Why structural:** {ex['reasoning']}")
        lines.append("")
        lines.append("**Functions served:**")
        for f in ex["functions"]:
            lines.append(f"- {f}")
        lines.append("")

    lines.append("## Clearly Stylistic Elements")
    lines.append("")
    lines.append("These can change form while preserving the story:")
    lines.append("")

    for ex in EXAMPLES["clearly_stylistic"]:
        lines.append(f'### "{ex["element"]}"')
        lines.append("")
        lines.append(f"**Why stylistic:** {ex['reasoning']}")
        lines.append("")
        lines.append("**Alternative forms:**")
        for a in ex["alternatives"]:
            lines.append(f"- {a}")
        lines.append("")

    lines.append("## Elements Requiring Analysis")
    lines.append("")
    lines.append("These need careful function extraction to classify:")
    lines.append("")

    for ex in EXAMPLES["requires_analysis"]:
        lines.append(f'### "{ex["element"]}"')
        lines.append("")
        lines.append(f"**Analysis:** {ex['analysis']}")
        lines.append("")
        lines.append(f"**Likely classification:** {ex['likely_classification']}")
        lines.append("")
        lines.append("**Functions to preserve:**")
        for f in ex["functions_to_preserve"]:
            lines.append(f"- {f}")
        lines.append("")

    lines.append("## The Key Insight")
    lines.append("")
    lines.append("**Form is almost always stylistic. Function is almost always structural.**")
    lines.append("")
    lines.append("When analyzing an element:")
    lines.append("1. Identify what FUNCTION it serves")
    lines.append("2. Ask: Could a different FORM serve that function?")
    lines.append("3. If yes: the form is stylistic, the function is structural")
    lines.append("4. The adaptation must preserve functions, not forms")
    lines.append("")

    return "\n".join(lines)


def format_batch_template():
    return json.dumps({
        "elements": [
            {
                "name": "Element 1",
                "type": "character|setting|plot|relationship|device",
                "initial_impression": "structural|stylistic|unclear"
            }
        ],
        "instructions": "List elements to classify. Run with --batch filename.json"
    }, indent=2, ensure_ascii=False)


def create_empty_result(element):
    return {
        "element": element,
        "classification": "unclear",
        "confidence": "low",
        "reasoning": [],
        "questions_to_resolve": [
            "What specific functions does this element serve?",
            "Could those functions be served by a different form?",
            "Would the story break without this, or just feel different?"
        ],
        "functions_served": [],
        "alternative_forms": []
    }


# == MAIN ==

def main():
    args = sys.argv[1:]

    # Help
    if "--help" in args or "-h" in args:
        print("""Structural vs Stylistic Classification

Usage:
  python structural_stylistic.py "element name"
  python structural_stylistic.py --examples
  python structural_stylistic.py --batch-template
  python structural_stylistic.py --questions

Options:
  --examples        Show classification examples
  --questions       List all classification questions
  --batch-template  Output batch classification template
  --json            Output as JSON

The Structural/Stylistic Distinction:
  Structural = The story BREAKS without this (or its function)
  Stylistic = The story WORKS with a different form of this

Key Insight:
  Form is usually stylistic. Function is usually structural.
  Ask: "What does this DO?" then "Could something else DO that?"
""")
        sys.exit(0)

    is_json = "--json" in args

    # Handle --examples
    if "--examples" in args:
        if is_json:
            print(json.dumps(EXAMPLES, indent=2, ensure_ascii=False))
        else:
            print(format_examples())
        return

    # Handle --questions
    if "--questions" in args:
        if is_json:
            print(json.dumps(CLASSIFICATION_QUESTIONS, indent=2, ensure_ascii=False))
        else:
            print("# Classification Questions\n")
            for i in range(len(CLASSIFICATION_QUESTIONS)):
                q = CLASSIFICATION_QUESTIONS[i]
                print(f"## {i + 1}. {q['question']} (Weight: {q['weight']})")
                print(f"   Structural: {q['structural_answer']}")
                print(f"   Stylistic: {q['stylistic_answer']}")
                print("")
        return

    # Handle --batch-template
    if "--batch-template" in args:
        print(format_batch_template())
        return

    # Find element name (positional argument)
    element = None
    for i in range(len(args)):
        if not args[i].startswith("--"):
            element = args[i]
            break

    if not element:
        print("Error: Please provide an element to classify", file=sys.stderr)
        print('Usage: python structural_stylistic.py "royal court setting"', file=sys.stderr)
        print("       python structural_stylistic.py --examples", file=sys.stderr)
        sys.exit(1)

    # Generate questionnaire for the element
    if is_json:
        result = create_empty_result(element)
        print(json.dumps(result, indent=2, ensure_ascii=False))
    else:
        print(format_questionnaire(element))


if __name__ == "__main__":
    main()
