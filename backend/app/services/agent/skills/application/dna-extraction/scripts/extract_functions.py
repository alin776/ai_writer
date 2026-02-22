#!/usr/bin/env python3



"""
Extract Functions

Interactive questionnaire for DNA extraction from existing works.
Guides through six-axis function analysis at configurable depth.

Usage:
  python scripts/extract-functions.py "Work Name"
  python scripts/extract-functions.py "Work Name" --depth quick
  python scripts/extract-functions.py --element "The Ghost"
  python scripts/extract-functions.py --validate extraction.json
  python scripts/extract-functions.py --template
"""

import sys
import os
import json
import re
import random
from datetime import date


# == INTERFACES ===















# == DATA ===

EXTRACTION_QUESTIONS = {
  structural: [
    "What would break in the plot if we removed this?",
    "What information does this control or reveal?",
    "What does this force to happen?",
    "What does this prevent from happening prematurely?"
  ],
  character: [
    "What does this reveal about any character?",
    "How does this challenge or change a character?",
    "What choice does this force?",
    "Who does this illuminate through contrast?"
  ],
  emotional: [
    "What should the audience feel here?",
    "How does this serve the genre promise?",
    "Is this a peak, valley, or sustain moment?",
    "What would be lost emotionally without this?"
  ],
  thematic: [
    "What question does this raise or address?",
    "What value does this test?",
    "What does this symbolize?",
    "How does this complicate or reinforce the theme?"
  ],
  relational: [
    "What connection does this create or strengthen?",
    "What tension does this generate between characters?",
    "How does this change the relationship web?",
    "What contrast does this establish?"
  ]
};

GENRE_OPTIONS = [
  "wonder", "idea", "adventure", "horror", "mystery",
  "thriller", "humor", "relationship", "drama", "issue", "ensemble"
];

SINCERITY_OPTIONS = [
  "high (earnest, characters mean what they say)",
  "medium (mix of sincere and ironic)",
  "low (ironic, detached, subtext-heavy)"
];

HUMOR_MODES = [
  "banter/quips", "deadpan", "physical/slapstick", "dark/gallows",
  "absurdist", "satirical", "minimal/serious"
];

CONFLICT_STYLES = [
  "verbal sparring", "cold silence", "explosive outbursts",
  "passive aggression", "physical violence", "avoidant/deflecting"
];

# == UTILITIES ===

def formatDate(): string {
  now = new Date();
  return now.toISOString().split("T")[0];
}

def createEmptyExtraction(workName: string, depth: Depth): WorkExtraction {
  return {
    _meta: {
      type: "work-extraction",
      source_work: workName,
      source_author: "",
      source_medium: "",
      extraction_date: formatDate(),
      extraction_depth: depth,
      clusters: []
    },
    emotional_core: {
      primary_genre: "",
      secondary_genres: [],
      emotional_experience: "",
      emotional_beats: []
    },
    tone: {
      sincerity_level: "",
      humor_mode: "",
      emotional_expression: "",
      dialogue_density: "",
      conflict_style: "",
      baseline_tone: "",
      tonal_shifts: []
    },
    characters: {},
    plot_structures: {},
    relationships: {},
    structural_requirements: [],
    adaptable_without_breaking: [],
    links: {
      clusters: [],
      similar_works: [],
      derived_syntheses: []
    }
  };
}

def createEmptyElement(name: string, type: ElementExtraction["element_type"]): ElementExtraction {
  return {
    element_name: name,
    element_type: type,
    form: "",
    functions: {
      structural: [],
      character: [],
      emotional: [],
      thematic: [],
      relational: []
    },
    structural_necessity: "medium",
    adaptable_elements: []
  };
}

def formatExtraction(extraction: WorkExtraction): string {
  lines: string[] = [];

  lines.append("# DNA Extraction: " + extraction._meta.source_work);
  lines.append("");
  lines.append(f"**Author:** {extraction._meta.source_author or \"(not specified)\"}");
  lines.append(f"**Medium:** {extraction._meta.source_medium or \"(not specified)\"}");
  lines.append(f"**Extraction Depth:** {extraction._meta.extraction_depth}");
  lines.append(f"**Date:** {extraction._meta.extraction_date}");
  lines.append("");

  # Emotional Core
  lines.append("## Emotional Core");
  lines.append("");
  lines.append(f"**Primary Genre:** {extraction.emotional_core.primary_genre or \"(not identified)\"}");
  if (extraction.emotional_core.secondary_genres.length > 0) {
    lines.append(f"**Secondary Genres:** {extraction.emotional_core.secondary_genres.join(\", \")}");
  }
  lines.append("");
  lines.append(f"**Emotional Experience:** {extraction.emotional_core.emotional_experience or \"(not described)\"}");
  lines.append("");

  if (extraction.emotional_core.emotional_beats.length > 0) {
    lines.append("### Emotional Beats");
    for beat in extraction.emotional_core.emotional_beats) {
      lines.append(f"- **{round(beat.position * 100)}%:** {beat.emotion} ({beat.element})");
    }
    lines.append("");
  }

  # Tone
  if (extraction.tone.baseline_tone) {
    lines.append("## Tone Profile");
    lines.append("");
    lines.append(f"**Baseline:** {extraction.tone.baseline_tone}");
    lines.append(f"**Sincerity:** {extraction.tone.sincerity_level}");
    lines.append(f"**Humor Mode:** {extraction.tone.humor_mode}");
    lines.append(f"**Emotional Expression:** {extraction.tone.emotional_expression}");
    lines.append(f"**Dialogue Density:** {extraction.tone.dialogue_density}");
    lines.append(f"**Conflict Style:** {extraction.tone.conflict_style}");
    lines.append("");
  }

  # Characters
  charNames = Object.keys(extraction.characters);
  if (charNames.length > 0) {
    lines.append("## Characters");
    lines.append("");
    for name in charNames) {
      char = extraction.characters[name];
      lines.append(f"### {name}");
      lines.append(f"**Form:** {char.form}");
      lines.append(f"**Necessity:** {char.structural_necessity}");
      lines.append("");

      if (char.functions.structural.length > 0) {
        lines.append("**Structural Functions:**");
        for f in char.functions.structural) {
          lines.append(f"- {f}");
        }
      }
      if (char.functions.character.length > 0) {
        lines.append("**Character Functions:**");
        for f in char.functions.character) {
          lines.append(f"- {f}");
        }
      }
      if (char.functions.emotional.length > 0) {
        lines.append("**Emotional Functions:**");
        for f in char.functions.emotional) {
          lines.append(f"- {f}");
        }
      }
      if (char.functions.relational.length > 0) {
        lines.append("**Relational Functions:**");
        for f in char.functions.relational) {
          lines.append(f"- {f}");
        }
      }
      if (char.adaptable_elements.length > 0) {
        lines.append(f"**Adaptable:** {char.adaptable_elements.join(\", \")}");
      }
      lines.append("");
    }
  }

  # Structural Requirements
  if (extraction.structural_requirements.length > 0) {
    lines.append("## Structural Requirements");
    lines.append("");
    for req in extraction.structural_requirements) {
      lines.append(f"- {req}");
    }
    lines.append("");
  }

  # Adaptable Elements
  if (extraction.adaptable_without_breaking.length > 0) {
    lines.append("## Adaptable Without Breaking");
    lines.append("");
    for elem in extraction.adaptable_without_breaking) {
      lines.append(f"- {elem}");
    }
    lines.append("");
  }

  # Clusters
  if (extraction._meta.clusters.length > 0) {
    lines.append("## Cluster Memberships");
    lines.append("");
    for cluster in extraction._meta.clusters) {
      lines.append(f"- {cluster}");
    }
    lines.append("");
  }

  return lines.join("\n");
}

def formatElementExtraction(element: ElementExtraction): string {
  lines: string[] = [];

  lines.append(f"# Element Extraction: {element.element_name}");
  lines.append("");
  lines.append(f"**Type:** {element.element_type}");
  lines.append(f"**Form:** {element.form}");
  lines.append(f"**Structural Necessity:** {element.structural_necessity}");
  lines.append("");

  axes = ["structural", "character", "emotional", "thematic", "relational"] as const;
  for axis in axes) {
    funcs = element.functions[axis];
    if (funcs.length > 0) {
      lines.append(f"## {axis.charAt(0).upper() + axis.slice(1)} Functions");
      for f in funcs) {
        lines.append(f"- {f}");
      }
      lines.append("");
    }
  }

  if (element.adaptable_elements.length > 0) {
    lines.append("## Adaptable Elements");
    for elem in element.adaptable_elements) {
      lines.append(f"- {elem}");
    }
  }

  return lines.join("\n");
}

def formatQuestionnaire(workName: string, depth: Depth): string {
  lines: string[] = [];

  lines.append(f"# DNA Extraction Questionnaire: {workName}");
  lines.append(f"**Depth:** {depth}");
  lines.append("");
  lines.append("---");
  lines.append("");

  # Emotional Core Questions
  lines.append("## 1. Emotional Core");
  lines.append("");
  lines.append("### Primary Genre");
  lines.append("What emotional experience does this work primarily deliver?");
  lines.append(f"Options: {GENRE_OPTIONS.join(\", \")}");
  lines.append("");
  lines.append("**Your answer:**");
  lines.append("");

  lines.append("### Secondary Genres (if any)");
  lines.append("What other emotional experiences does it layer in?");
  lines.append("");
  lines.append("**Your answer:**");
  lines.append("");

  lines.append("### Emotional Experience");
  lines.append("In one sentence, what does someone who LOVES this work love about it?");
  lines.append("");
  lines.append("**Your answer:**");
  lines.append("");

  if (depth != "quick") {
    lines.append("### Emotional Beats");
    lines.append("List 5-10 key emotional moments with approximate position (0.0-1.0):");
    lines.append("Format: position | emotion | element");
    lines.append("");
    lines.append("**Your answer:**");
    lines.append("");
  }

  # Tone Questions (standard+)
  if (depth != "quick") {
    lines.append("---");
    lines.append("");
    lines.append("## 2. Tone Profile");
    lines.append("");

    lines.append("### Sincerity Level");
    lines.append("How earnest vs. ironic is the work?");
    for opt in SINCERITY_OPTIONS) {
      lines.append(f"- {opt}");
    }
    lines.append("");
    lines.append("**Your answer:**");
    lines.append("");

    lines.append("### Humor Mode");
    lines.append("When humor appears, what form does it take?");
    lines.append(f"Options: {HUMOR_MODES.join(\", \")}");
    lines.append("");
    lines.append("**Your answer:**");
    lines.append("");

    lines.append("### Emotional Expression");
    lines.append("How do characters show/hide their feelings?");
    lines.append("(direct statement, subtext-heavy, action-reveals-feeling, denial/deflection)");
    lines.append("");
    lines.append("**Your answer:**");
    lines.append("");

    lines.append("### Dialogue Density");
    lines.append("Talk-to-action ratio? (quippy/rapid-fire, balanced, sparse/weighted silence)");
    lines.append("");
    lines.append("**Your answer:**");
    lines.append("");

    lines.append("### Conflict Style");
    lines.append("How do characters fight?");
    lines.append(f"Options: {CONFLICT_STYLES.join(\", \")}");
    lines.append("");
    lines.append("**Your answer:**");
    lines.append("");

    lines.append("### Baseline Tone");
    lines.append("Describe the default emotional register in a phrase:");
    lines.append("");
    lines.append("**Your answer:**");
    lines.append("");
  }

  # Character Questions
  lines.append("---");
  lines.append("");
  lines.append(f"## 3. Characters ({depth == \"quick\" ? \"3-5 main\" : \"all significant\"})");
  lines.append("");
  lines.append("For each character, answer:");
  lines.append("");
  lines.append("### Character: [NAME]");
  lines.append("");
  lines.append("**Form:** What are they on the surface?");
  lines.append("");

  for ([axis, questions] of EXTRACTION_QUESTIONS.items()) {
    lines.append(f"**{axis.charAt(0).upper() + axis.slice(1)} Function:**");
    for q in questions) {
      lines.append(f"- {q}");
    }
    lines.append("");
  }

  lines.append("**Structural Necessity:** high/medium/low");
  lines.append("**Adaptable Elements:** What about them could change?");
  lines.append("");
  lines.append("(Repeat for each character)");
  lines.append("");

  # Structural Requirements
  lines.append("---");
  lines.append("");
  lines.append("## 4. Structural Requirements");
  lines.append("");
  lines.append("What MUST be present for the story to work? (Not forms, but functions)");
  lines.append("Example: 'Protagonist must have privileged information others lack'");
  lines.append("");
  lines.append("**Your answer:**");
  lines.append("");

  # Adaptable Elements
  lines.append("---");
  lines.append("");
  lines.append("## 5. Adaptable Without Breaking");
  lines.append("");
  lines.append("What could change completely without breaking what makes this work?");
  lines.append("Example: 'Royal setting', 'Time period', 'Character genders'");
  lines.append("");
  lines.append("**Your answer:**");
  lines.append("");

  # Cluster Membership
  lines.append("---");
  lines.append("");
  lines.append("## 6. Cluster Membership");
  lines.append("");
  lines.append("What trope patterns does this belong to?");
  lines.append("Example: 'revenge-tragedy', 'found-family', 'bounty-hunter-scifi'");
  lines.append("");
  lines.append("**Your answer:**");
  lines.append("");

  return lines.join("\n");
}

def validateExtraction(extraction: WorkExtraction): { valid: boolean; issues: string[] } {
  issues: string[] = [];

  # Check required fields
  if (!extraction._meta.source_work) {
    issues.append("Missing source work name");
  }

  if (!extraction.emotional_core.primary_genre) {
    issues.append("Missing primary genre - emotional core not identified");
  }

  if (!extraction.emotional_core.emotional_experience) {
    issues.append("Missing emotional experience description");
  }

  # Check for characters
  charCount = Object.keys(extraction.characters).length;
  if (charCount == 0) {
    issues.append("No characters extracted");
  } else {
    # Check each character
    for ([name, char] of Object.entries(extraction.characters)) {
      allFunctions = [
        ...char.functions.structural,
        ...char.functions.character,
        ...char.functions.emotional,
        ...char.functions.thematic,
        ...char.functions.relational
      ];
      if (allFunctions.length == 0) {
        issues.append(f"Character '{name}' has no functions extracted");
      }
      if (!char.structural_necessity) {
        issues.append(f"Character '{name}' missing structural necessity rating");
      }
    }
  }

  # Check structural requirements
  if (extraction.structural_requirements.length == 0) {
    issues.append("No structural requirements identified");
  }

  # Check adaptable elements
  if (extraction.adaptable_without_breaking.length == 0) {
    issues.append("No adaptable elements identified - likely over-restricting");
  }

  # Depth-specific checks
  if (extraction._meta.extraction_depth != "quick") {
    if (!extraction.tone.baseline_tone) {
      issues.append("Standard/detailed extraction missing tone profile");
    }
    if (extraction.emotional_core.emotional_beats.length == 0) {
      issues.append("Standard/detailed extraction missing emotional beats");
    }
  }

  return {
    valid: issues.length == 0,
    issues
  };
}

# == MAIN ===

def main(): void {
  args = sys.argv[1:];

  # Help
  if (args.includes("--help") or args.includes("-h")) {
    print(f"Extract Functions - DNA Extraction Tool

Usage:
  deno run --allow-read --allow-write scripts/extract-functions.ts \"Work Name\"
  deno run --allow-read --allow-write scripts/extract-functions.ts \"Work Name\" --depth quick
  deno run --allow-read --allow-write scripts/extract-functions.ts --element \"The Ghost\"
  deno run --allow-read --allow-write scripts/extract-functions.ts --validate extraction.json
  deno run --allow-read --allow-write scripts/extract-functions.ts --template

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
  deno run --allow-read scripts/extract-functions.ts \"Hamlet\" --questionnaire

  # Quick extraction template
  deno run --allow-read scripts/extract-functions.ts \"Killjoys\" --depth quick --template

  # Validate completed extraction
  deno run --allow-read scripts/extract-functions.ts --validate hamlet.json
");
    sys.exit(0);
  }

  # Parse arguments
  depthIndex = args.indexOf("--depth");
  depth: Depth = depthIndex != -1 and args[depthIndex + 1]
    ? args[depthIndex + 1] as Depth
    : "standard";

  elementIndex = args.indexOf("--element");
  elementName = elementIndex != -1 ? args[elementIndex + 1] : None;

  validateIndex = args.indexOf("--validate");
  validateFile = validateIndex != -1 ? args[validateIndex + 1] : None;

  isTemplate = args.includes("--template");
  isJson = args.includes("--json");
  isQuestionnaire = args.includes("--questionnaire");

  # Track consumed indices for positional arg detection
  skipIndices = new Set<number>();
  if (depthIndex != -1) {
    skipIndices.add(depthIndex);
    skipIndices.add(depthIndex + 1);
  }
  if (elementIndex != -1) {
    skipIndices.add(elementIndex);
    skipIndices.add(elementIndex + 1);
  }
  if (validateIndex != -1) {
    skipIndices.add(validateIndex);
    skipIndices.add(validateIndex + 1);
  }

  # Find positional argument (work name)
  workName: string | None = None;
  for (i = 0; i < args.length; i++) {
    if (!args[i].startswith("--") and !skipIndices.has(i)) {
      workName = args[i];
      break;
    }
  }

  # Handle validation mode
  if (validateFile) {
    try {
      content = open(validateFile, "r", encoding="utf-8").read();
      extraction = json.loads(content) as WorkExtraction;
      result = validateExtraction(extraction);

      if (isJson) {
        print(json.dumps(result, None, 2));
      } else {
        print(f"\nValidation Result: {result.valid ? \"PASS\" : \"FAIL\"}\n");
        if (result.issues.length > 0) {
          print("Issues found:");
          for issue in result.issues) {
            print(f"  - {issue}");
          }
        } else {
          print("Extraction is complete and ready for synthesis.");
        }
      }
    } catch (e) {
      print(f"Error reading/parsing {validateFile}: {e}");
      sys.exit(1);
    }
    return;
  }

  # Handle element extraction mode
  if (elementName) {
    element = createEmptyElement(elementName, "other");

    if (isJson) {
      print(json.dumps(element, None, 2));
    } else {
      print(formatElementExtraction(element));
      print("\n---\n");
      print("## Extraction Questions\n");
      for ([axis, questions] of EXTRACTION_QUESTIONS.items()) {
        print(f"### {axis.charAt(0).upper() + axis.slice(1)}");
        for q in questions) {
          print(f"- {q}");
        }
        print("");
      }
    }
    return;
  }

  # Need work name for remaining modes
  if (!workName) {
    print("Error: Please provide a work name or use --validate/--element flags");
    print("Usage: deno run --allow-read scripts/extract-functions.ts \"Work Name\"");
    sys.exit(1);
  }

  # Handle questionnaire mode
  if (isQuestionnaire) {
    print(formatQuestionnaire(workName, depth));
    return;
  }

  # Handle template mode
  extraction = createEmptyExtraction(workName, depth);

  if (isJson) {
    print(json.dumps(extraction, None, 2));
  } else if (isTemplate) {
    print(json.dumps(extraction, None, 2));
  } else {
    # Default: output formatted markdown template with guidance
    print(formatExtraction(extraction));
    print("\n---\n");
    print("## Next Steps\n");
    print("1. Use --questionnaire flag for guided extraction");
    print("2. Fill in extraction fields");
    print("3. Use --validate to check completeness");
    print(f"\nExample: deno run --allow-read scripts/extract-functions.ts \"{workName}\" --questionnaire");
  }
}

main();


if __name__ == '__main__':
    main()
