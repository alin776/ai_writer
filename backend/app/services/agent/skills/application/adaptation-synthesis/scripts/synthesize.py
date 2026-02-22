#!/usr/bin/env python3



"""
Synthesize

Interactive synthesis session from DNA documents.
Guides function-to-form mapping for adaptation projects.

Usage:
  python scripts/synthesize.py source.json --context "corporate dystopia"
  python scripts/synthesize.py source1.json source2.json --primary source1
  python scripts/synthesize.py --template
"""

import sys
import os
import json
import re
import random
from datetime import date


# == INTERFACES ===








# == UTILITIES ===

def formatDate(): string {
  now = new Date();
  return now.toISOString().split("T")[0];
}

def createEmptySynthesis(
  sourceName: string,
  context: string,
  genre: string
): SynthesisDocument {
  return {
    _meta: {
      type: "synthesis",
      synthesis_name: f"{sourceName} in {context}",
      target_context: context,
      primary_source: sourceName,
      secondary_sources: [],
      target_genre: genre,
      synthesis_date: formatDate()
    },
    context_mapping: {
      setting: "",
      power_structure: "",
      information_control: "",
      escape_prevention: "",
      typical_conflicts: ""
    },
    function_to_form_mapping: {},
    tone_synthesis: {
      original_tone: "",
      adapted_tone: "",
      sincerity_level: "",
      conflict_style: ""
    },
    character_synthesis: {},
    validation: {
      genre_check: "pending",
      function_coverage: "pending",
      orthogonality_check: "pending",
      context_coherence: "pending"
    },
    ready_for: "in-progress"
  };
}

def formatSynthesisWorksheet(synthesis: SynthesisDocument, source: DNADocument | None): string {
  lines: string[] = [];

  lines.append(f"# Synthesis Worksheet: {synthesis._meta.synthesis_name}");
  lines.append("");
  lines.append(f"**Primary Source:** {synthesis._meta.primary_source}");
  lines.append(f"**Target Context:** {synthesis._meta.target_context}");
  lines.append(f"**Target Genre:** {synthesis._meta.target_genre}");
  lines.append(f"**Date:** {synthesis._meta.synthesis_date}");
  lines.append("");

  lines.append("---");
  lines.append("");

  # Section 1: Context Mapping
  lines.append("## 1. Context Mapping");
  lines.append("");
  lines.append("Define what elements in your target context will serve source functions.");
  lines.append("");
  lines.append("### Setting");
  lines.append("Where does this take place? Be specific about location, time period, social milieu.");
  lines.append("");
  lines.append("**Your answer:**");
  lines.append("");

  lines.append("### Power Structure");
  lines.append("How is power organized? Who has it? How is it contested?");
  lines.append("");
  lines.append("**Your answer:**");
  lines.append("");

  lines.append("### Information Control");
  lines.append("How is information controlled, shared, hidden? What makes something secret?");
  lines.append("");
  lines.append("**Your answer:**");
  lines.append("");

  lines.append("### Escape Prevention");
  lines.append("Why can't characters just leave? What traps them in the situation?");
  lines.append("");
  lines.append("**Your answer:**");
  lines.append("");

  lines.append("### Typical Conflicts");
  lines.append("What conflicts naturally arise in this context?");
  lines.append("");
  lines.append("**Your answer:**");
  lines.append("");

  lines.append("---");
  lines.append("");

  # Section 2: Function Mapping
  lines.append("## 2. Function-to-Form Mapping");
  lines.append("");
  lines.append("For each key function from the source, define a new form in your context.");
  lines.append("");
  lines.append("**Remember the orthogonality test:** Does the new form exist for its own reasons?");
  lines.append("Would someone unfamiliar with the source find it believable?");
  lines.append("");

  # If we have source DNA, list its structural requirements
  if (source?.structural_requirements) {
    lines.append("### Source Structural Requirements");
    lines.append("");
    for req in source.structural_requirements) {
      lines.append(f"- {req}");
    }
    lines.append("");
    lines.append("### Map Each Requirement");
    lines.append("");

    for req in source.structural_requirements) {
      shortName = req.substring(0, 40) + (req.length > 40 ? "..." : "");
      lines.append(f"#### Function: \"{shortName}\"");
      lines.append("");
      lines.append("**Original form in source:** ");
      lines.append("");
      lines.append("**New form in your context:** ");
      lines.append("");
      lines.append("**Orthogonality check:** Does this form exist for its own reasons? (yes/no/needs work)");
      lines.append("");
      lines.append("**Functions served:** (list what this enables)");
      lines.append("- ");
      lines.append("");
    }
  } else {
    lines.append("### Key Functions to Map");
    lines.append("");
    lines.append("(Add functions from your source extraction)");
    lines.append("");
    lines.append("#### Function: \"[describe function]\"");
    lines.append("");
    lines.append("**Original form in source:** ");
    lines.append("");
    lines.append("**New form in your context:** ");
    lines.append("");
    lines.append("**Orthogonality check:** ");
    lines.append("");
    lines.append("**Functions served:**");
    lines.append("- ");
    lines.append("");
  }

  lines.append("---");
  lines.append("");

  # Section 3: Tone Synthesis
  lines.append("## 3. Tone Synthesis");
  lines.append("");

  if (source?.tone) {
    lines.append("### Source Tone");
    lines.append(f"- Sincerity: {source.tone.sincerity_level}");
    lines.append(f"- Conflict style: {source.tone.conflict_style}");
    lines.append(f"- Baseline: {source.tone.baseline_tone}");
    lines.append("");
  }

  lines.append("### Adapted Tone");
  lines.append("");
  lines.append("**Original tone summary:**");
  lines.append("");
  lines.append("**How will you adapt it to your context?**");
  lines.append("");
  lines.append("**Sincerity level:** (high/medium/low)");
  lines.append("");
  lines.append("**Conflict style:** (verbal sparring, cold silence, explosive, etc.)");
  lines.append("");

  lines.append("---");
  lines.append("");

  # Section 4: Character Synthesis
  lines.append("## 4. Character Synthesis");
  lines.append("");

  if (source?.characters) {
    lines.append("### Source Characters");
    lines.append("");
    for ([name, char] of Object.entries(source.characters)) {
      lines.append(f"#### {name}");
      lines.append(f"Original form: {char.form}");
      if (char.functions?.structural) {
        lines.append("Key functions: " + char.functions.structural.slice(0, 2).join("; "));
      }
      lines.append("");
    }
    lines.append("");
  }

  lines.append("### Your Adapted Characters");
  lines.append("");
  lines.append("#### Protagonist");
  lines.append("");
  lines.append("**New name:**");
  lines.append("");
  lines.append("**Based on functions from:** (source character name)");
  lines.append("");
  lines.append("**New form:** (describe who they are in your context)");
  lines.append("");
  lines.append("**Arc:** (brief transformation description)");
  lines.append("");
  lines.append("(Repeat for other key characters)");
  lines.append("");

  lines.append("---");
  lines.append("");

  # Section 5: Validation
  lines.append("## 5. Validation Checklist");
  lines.append("");
  lines.append("Before proceeding, verify:");
  lines.append("");
  lines.append("- [ ] **Genre check:** Does this deliver " + synthesis._meta.target_genre + " emotional experience?");
  lines.append("- [ ] **Function coverage:** Are all structural requirements from source addressed?");
  lines.append("- [ ] **Orthogonality check:** Do all new forms exist for their own reasons?");
  lines.append("- [ ] **Context coherence:** Do all elements fit naturally in the target context?");
  lines.append("- [ ] **Tone alignment:** Does the adapted tone serve the emotional experience?");
  lines.append("");

  lines.append("---");
  lines.append("");
  lines.append("## When Complete");
  lines.append("");
  lines.append("Run validation: f"deno run --allow-read scripts/validate-synthesis.ts your-synthesis.json"");
  lines.append("");
  lines.append("Then proceed to outline-collaborator or drafting skill.");

  return lines.join("\n");
}

def formatSynthesisTemplate(): string {
  return json.dumps({
    _meta: {
      type: "synthesis",
      synthesis_name: "Your Synthesis Name",
      target_context: "describe target context",
      primary_source: "source-dna.json",
      secondary_sources: [],
      target_genre: "drama",
      synthesis_date: formatDate()
    },
    context_mapping: {
      setting: "Where and when",
      power_structure: "How power is organized",
      information_control: "How secrets work",
      escape_prevention: "Why characters can't leave",
      typical_conflicts: "What conflicts arise naturally"
    },
    function_to_form_mapping: {
      "function_name": {
        original_form: "what it was in source",
        new_form: "what it is in your version",
        orthogonality_check: "pass/fail/needs work",
        functions_served: ["list", "of", "functions"]
      }
    },
    tone_synthesis: {
      original_tone: "describe source tone",
      adapted_tone: "describe your tone",
      sincerity_level: "high/medium/low",
      conflict_style: "how characters fight"
    },
    character_synthesis: {
      protagonist: {
        new_name: "Character Name",
        original_functions_from: "source character",
        new_form: "who they are in your context",
        arc: "their transformation"
      }
    },
    validation: {
      genre_check: "pending",
      function_coverage: "pending",
      orthogonality_check: "pending",
      context_coherence: "pending"
    },
    ready_for: "in-progress"
  }, None, 2);
}

def formatCombinationGuidance(primary: string, secondary: string[]): string {
  lines: string[] = [];

  lines.append("# Combining Multiple Sources");
  lines.append("");
  lines.append(f"**Primary source:** {primary}");
  lines.append(f"**Secondary sources:** {secondary.join(\", \")}");
  lines.append("");

  lines.append("## Combination Rules");
  lines.append("");
  lines.append("1. **Primary source functions take precedence** when sources conflict");
  lines.append("2. **Secondary sources add flavor**, not structure");
  lines.append("3. **Identify conflicts early** - where do sources want different things?");
  lines.append("");

  lines.append("## Conflict Resolution Options");
  lines.append("");
  lines.append("When functions conflict, choose one approach:");
  lines.append("");
  lines.append("- **Primary wins:** Keep primary's version, drop secondary's");
  lines.append("- **Blend:** Find middle ground that partially serves both");
  lines.append("- **Alternate:** Different parts of work serve different sources");
  lines.append("- **Transform:** Conflict becomes a feature (tension between approaches)");
  lines.append("");

  lines.append("## Process");
  lines.append("");
  lines.append("1. List all functions from primary source");
  lines.append("2. List functions from secondary sources");
  lines.append("3. Identify overlaps (complementary)");
  lines.append("4. Identify conflicts (incompatible)");
  lines.append("5. Resolve each conflict using options above");
  lines.append("6. Proceed with combined function list");
  lines.append("");

  return lines.join("\n");
}

# == MAIN ===

def main(): void {
  args = sys.argv[1:];

  # Help
  if (args.includes("--help") or args.includes("-h")) {
    print(f"Synthesize - DNA Synthesis Tool

Usage:
  deno run --allow-read scripts/synthesize.ts source.json --context \"corporate dystopia\"
  deno run --allow-read scripts/synthesize.ts source1.json source2.json --primary source1.json
  deno run --allow-read scripts/synthesize.ts --template
  deno run --allow-read scripts/synthesize.ts --function \"proximity to power\" --context scifi

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
  deno run --allow-read scripts/synthesize.ts hamlet.json --context \"corporate dystopia\" --worksheet

  # Get blank template
  deno run --allow-read scripts/synthesize.ts --template

  # Combine two sources
  deno run --allow-read scripts/synthesize.ts hamlet.json killjoys.json --primary hamlet.json --context scifi
");
    sys.exit(0);
  }

  isJson = args.includes("--json");
  isWorksheet = args.includes("--worksheet");
  isTemplate = args.includes("--template");

  # Handle --template
  if (isTemplate) {
    print(formatSynthesisTemplate());
    return;
  }

  # Parse arguments
  contextIndex = args.indexOf("--context");
  context = contextIndex != -1 ? args[contextIndex + 1] : None;

  genreIndex = args.indexOf("--genre");
  genre = genreIndex != -1 ? args[genreIndex + 1] : None;

  primaryIndex = args.indexOf("--primary");
  primaryFile = primaryIndex != -1 ? args[primaryIndex + 1] : None;

  # Find source files (positional arguments)
  skipIndices = new Set<number>();
  for idx in [contextIndex, genreIndex, primaryIndex]) {
    if (idx != -1) {
      skipIndices.add(idx);
      skipIndices.add(idx + 1);
    }
  }

  sourceFiles: string[] = [];
  for (i = 0; i < args.length; i++) {
    if (!args[i].startswith("--") and !skipIndices.has(i) and args[i].endswith(".json")) {
      sourceFiles.append(args[i]);
    }
  }

  if (sourceFiles.length == 0) {
    print("Error: Please provide at least one source DNA file");
    print("Usage: deno run --allow-read scripts/synthesize.ts source.json --context \"corporate\"");
    print("       deno run --allow-read scripts/synthesize.ts --template");
    sys.exit(1);
  }

  if (!context) {
    print("Error: Please provide target context with --context");
    print("Example: --context \"corporate dystopia\"");
    sys.exit(1);
  }

  # Load primary source
  primarySource = primaryFile or sourceFiles[0];
  source: DNADocument | None = None;

  try {
    content = open(primarySource, "r", encoding="utf-8").read();
    source = json.loads(content);
  } catch (e) {
    print(f"Error reading source file {primarySource}: {e}");
    sys.exit(1);
  }

  # Determine genre
  targetGenre = genre or source?.emotional_core?.primary_genre or "drama";

  # Create synthesis document
  sourceName = source?._meta?.source_work or primarySource.replace(".json", "");
  synthesis = createEmptySynthesis(sourceName, context, targetGenre);

  # Add secondary sources if multiple files
  if (sourceFiles.length > 1) {
    synthesis._meta.secondary_sources = sourceFiles.filter(f => f != primarySource);
  }

  # Output
  if (sourceFiles.length > 1 and !isWorksheet and !isJson) {
    # Show combination guidance first
    print(formatCombinationGuidance(primarySource, synthesis._meta.secondary_sources));
    print("\n---\n");
  }

  if (isJson) {
    print(json.dumps(synthesis, None, 2));
  } else if (isWorksheet or True) {
    # Default to worksheet
    print(formatSynthesisWorksheet(synthesis, source));
  }
}

main();


if __name__ == '__main__':
    main()
