#!/usr/bin/env python3



"""
Validate Synthesis

Checks synthesis documents for completeness, function coverage,
and alignment with source DNA and target genre.

Usage:
  python scripts/validate-synthesis.py synthesis.json
  python scripts/validate-synthesis.py synthesis.json --against source.json
  python scripts/validate-synthesis.py synthesis.json --genre drama
  python scripts/validate-synthesis.py synthesis.json --full
"""

import sys
import os
import json
import re
import random
from datetime import date


# == INTERFACES ===





# == VALIDATION LOGIC ===

def validateCompleteness(synthesis: SynthesisDocument): CheckResult {
  notes: string[] = [];
  score = 0;
  maxScore = 10;

  # Check meta fields
  if (synthesis._meta?.synthesis_name) {
    score += 1;
  } else {
    notes.append("Missing synthesis name");
  }

  if (synthesis._meta?.target_context) {
    score += 1;
  } else {
    notes.append("Missing target context");
  }

  if (synthesis._meta?.primary_source) {
    score += 1;
  } else {
    notes.append("Missing primary source reference");
  }

  if (synthesis._meta?.target_genre) {
    score += 1;
  } else {
    notes.append("Missing target genre");
  }

  # Check context mapping
  if (synthesis.context_mapping and Object.keys(synthesis.context_mapping).length > 0) {
    score += 2;
    if (Object.keys(synthesis.context_mapping).length >= 4) {
      score += 1;
    } else {
      notes.append("Context mapping could be more detailed");
    }
  } else {
    notes.append("Missing context mapping");
  }

  # Check function mappings
  if (synthesis.function_to_form_mapping and Object.keys(synthesis.function_to_form_mapping).length > 0) {
    score += 2;
    mappingCount = Object.keys(synthesis.function_to_form_mapping).length;
    if (mappingCount >= 5) {
      score += 1;
    } else {
      notes.append(f"Only {mappingCount} function mappings - consider adding more");
    }
  } else {
    notes.append("Missing function-to-form mappings");
  }

  # Check character synthesis
  if (synthesis.character_synthesis and Object.keys(synthesis.character_synthesis).length > 0) {
    # Score already at max if everything above passes
  } else {
    notes.append("Missing character synthesis");
  }

  return {
    status: score >= 8 ? "pass" : score >= 5 ? "warn" : "fail",
    score,
    max_score: maxScore,
    notes
  };
}

def validateOrthogonality(synthesis: SynthesisDocument): CheckResult {
  notes: string[] = [];
  score = 0;
  maxScore = 10;

  if (!synthesis.function_to_form_mapping) {
    return {
      status: "fail",
      score: 0,
      max_score: maxScore,
      notes: ["No function mappings to check for orthogonality"]
    };
  }

  mappings = Object.entries(synthesis.function_to_form_mapping);
  passedChecks = 0;
  explicitlyMarked = 0;

  for func, mapping in mappings) {
    # Check if orthogonality was explicitly evaluated
    if (mapping.orthogonality_check) {
      explicitlyMarked++;
      if (mapping.orthogonality_check.lower().includes("pass")) {
        passedChecks++;
      } else if (mapping.orthogonality_check.lower().includes("fail")) {
        notes.append(f"Orthogonality FAILED for: {func}");
      } else {
        notes.append(f"Unclear orthogonality status for: {func}");
      }
    }

    # Heuristic checks for surface translation
    if (mapping.new_form and mapping.original_form) {
      original = mapping.original_form.lower();
      newForm = mapping.new_form.lower();

      # Check for obvious 1:1 translations
      surfaceIndicators = ["space ", "cyber", "future ", "sci-fi ", "fantasy "];
      for indicator in surfaceIndicators) {
        if (newForm.includes(indicator) and !original.includes(indicator)) {
          notes.append(f"Possible surface translation: \"{mapping.new_form}\" - just adding setting prefix?");
          break;
        }
      }
    }
  }

  # Score based on explicit checks
  if (mappings.length > 0) {
    if (explicitlyMarked == mappings.length) {
      score += 4;
    } else if (explicitlyMarked > 0) {
      score += 2;
      notes.append(f"Only {explicitlyMarked}/{mappings.length} mappings have explicit orthogonality check");
    } else {
      notes.append("No explicit orthogonality checks recorded");
    }

    passRate = passedChecks / mappings.length;
    score += round(passRate * 6);
  }

  return {
    status: score >= 8 ? "pass" : score >= 5 ? "warn" : "fail",
    score,
    max_score: maxScore,
    notes
  };
}

def validateFunctionCoverage(synthesis: SynthesisDocument, source: DNADocument | None): CheckResult {
  notes: string[] = [];
  score = 0;
  maxScore = 10;

  if (!synthesis.function_to_form_mapping) {
    return {
      status: "fail",
      score: 0,
      max_score: maxScore,
      notes: ["No function mappings present"]
    };
  }

  mappedFunctions = Object.keys(synthesis.function_to_form_mapping);

  # Basic: has some mappings
  if (mappedFunctions.length > 0) {
    score += 2;
  }

  # Check that mappings have functions_served
  functionsServed = 0;
  for mapping in Object.values(synthesis.function_to_form_mapping)) {
    if (mapping.functions_served and mapping.functions_served.length > 0) {
      functionsServed += mapping.functions_served.length;
    }
  }

  if (functionsServed >= 10) {
    score += 3;
  } else if (functionsServed >= 5) {
    score += 2;
    notes.append("Consider documenting more functions served by each mapping");
  } else {
    score += 1;
    notes.append("Few functions documented - synthesis may have gaps");
  }

  # If we have source DNA, check coverage
  if (source and source.structural_requirements) {
    requirements = source.structural_requirements;
    covered = 0;

    for req in requirements) {
      # Check if any mapping mentions this requirement
      reqWords = req.lower().split(/\s+/);
      found = False;

      for mapping in Object.values(synthesis.function_to_form_mapping)) {
        mappingText = json.dumps(mapping).lower();
        if (reqWords.some(word => word.length > 4 and mappingText.includes(word))) {
          found = True;
          break;
        }
      }

      if (found) covered++;
    }

    coverageRate = covered / requirements.length;
    score += round(coverageRate * 5);

    if (coverageRate < 1) {
      notes.append(f"{requirements.length - covered}/{requirements.length} structural requirements may not be covered");
    }
  } else {
    # No source to check against - assume reasonable coverage
    score += 3;
    notes.append("No source DNA provided - cannot verify full function coverage");
  }

  return {
    status: score >= 8 ? "pass" : score >= 5 ? "warn" : "fail",
    score,
    max_score: maxScore,
    notes
  };
}

def validateContextCoherence(synthesis: SynthesisDocument): CheckResult {
  notes: string[] = [];
  score = 0;
  maxScore = 10;

  # Check context mapping exists and is substantive
  if (!synthesis.context_mapping or Object.keys(synthesis.context_mapping).length == 0) {
    return {
      status: "fail",
      score: 0,
      max_score: maxScore,
      notes: ["No context mapping present"]
    };
  }

  contextFields = Object.keys(synthesis.context_mapping);
  contextValues = Object.values(synthesis.context_mapping);

  # Basic: has context mapping
  score += 2;

  # Check for key context elements
  desiredFields = ["setting", "power_structure", "information_control", "escape_prevention"];
  fieldsPresent = 0;
  for field in desiredFields) {
    if (contextFields.some(f => f.lower().includes(field.replace("_", "")))) {
      fieldsPresent++;
    }
  }
  score += min(4, fieldsPresent);
  if (fieldsPresent < desiredFields.length) {
    notes.append(f"Consider adding context for: {desiredFields.filter(f =>
      !contextFields.some(cf => cf.lower().includes(f.replace(\"_\", \"\")))
    ).join(\", \")}");
  }

  # Check that context values are substantive (not just placeholders)
  substantiveValues = contextValues.filter(v => v and v.length > 10);
  if (substantiveValues.length == contextValues.length) {
    score += 2;
  } else {
    notes.append("Some context values seem like placeholders");
    score += 1;
  }

  # Check function mappings fit context
  if (synthesis.function_to_form_mapping) {
    contextText = json.dumps(synthesis.context_mapping).lower();
    coherent = 0;
    mappings = Object.values(synthesis.function_to_form_mapping);

    for mapping in mappings) {
      # Basic heuristic: new form should use words from context
      if (mapping.new_form) {
        formWords = mapping.new_form.lower().split(/\s+/);
        if (formWords.some(w => w.length > 4 and contextText.includes(w))) {
          coherent++;
        }
      }
    }

    if (mappings.length > 0) {
      coherenceRate = coherent / mappings.length;
      score += round(coherenceRate * 2);
      if (coherenceRate < 0.5) {
        notes.append("Some new forms may not fit the defined context");
      }
    }
  }

  return {
    status: score >= 8 ? "pass" : score >= 5 ? "warn" : "fail",
    score,
    max_score: maxScore,
    notes
  };
}

def validateGenreAlignment(synthesis: SynthesisDocument, targetGenre: string | None, source: DNADocument | None): CheckResult {
  notes: string[] = [];
  score = 0;
  maxScore = 10;

  genre = targetGenre or synthesis._meta?.target_genre;

  if (!genre) {
    return {
      status: "warn",
      score: 5,
      max_score: maxScore,
      notes: ["No target genre specified - cannot validate alignment"]
    };
  }

  # Has explicit genre
  score += 2;

  # Check if source genre matches (if available)
  if (source?.emotional_core?.primary_genre) {
    if (source.emotional_core.primary_genre.lower() == genre.lower()) {
      score += 3;
      notes.append("Target genre matches source primary genre");
    } else {
      notes.append(f"Source genre ({source.emotional_core.primary_genre}) differs from target ({genre}) - intentional shift?");
      score += 1; # Not inherently wrong, but flag it
    }
  } else {
    score += 2; # No source to compare
  }

  # Check tone synthesis for genre appropriateness
  if (synthesis.tone_synthesis) {
    score += 2;
    # Basic genre-tone heuristics
    tone = json.dumps(synthesis.tone_synthesis).lower();
    genreLower = genre.lower();

    if (genreLower == "horror" and !tone.includes("dread") and !tone.includes("fear") and !tone.includes("unease")) {
      notes.append("Horror genre but tone doesn't mention dread/fear/unease");
    }
    if (genreLower == "humor" and !tone.includes("comic") and !tone.includes("funny") and !tone.includes("wit")) {
      notes.append("Humor genre but tone doesn't mention comedy elements");
    }
    if (genreLower == "drama" and tone.includes("light") and tone.includes("comedy")) {
      notes.append("Drama genre but tone seems light - intentional dramedy?");
    }
  } else {
    notes.append("No tone synthesis - harder to verify genre alignment");
  }

  # Check for explicit genre validation in document
  if (synthesis.validation?.genre_check?.lower().includes("pass")) {
    score += 3;
  } else if (synthesis.validation?.genre_check) {
    score += 1;
    notes.append("Genre check in document doesn't indicate clear pass");
  }

  return {
    status: score >= 8 ? "pass" : score >= 5 ? "warn" : "fail",
    score,
    max_score: maxScore,
    notes
  };
}

def runValidation(synthesis: SynthesisDocument, source: DNADocument | None, targetGenre: string | None): ValidationResult {
  completeness = validateCompleteness(synthesis);
  orthogonality = validateOrthogonality(synthesis);
  functionCoverage = validateFunctionCoverage(synthesis, source);
  contextCoherence = validateContextCoherence(synthesis);
  genreAlignment = validateGenreAlignment(synthesis, targetGenre, source);

  checks = {
    function_coverage: functionCoverage,
    orthogonality: orthogonality,
    context_coherence: contextCoherence,
    genre_alignment: genreAlignment,
    completeness: completeness
  };

  # Aggregate issues and warnings
  issues: string[] = [];
  warnings: string[] = [];

  for name, check in checks.items()) {
    if (check.status == "fail") {
      issues.append(f"{name}: FAILED ({check.score}/{check.max_score})");
      issues.append(...check.notes.map(n => f"  - {n}"));
    } else if (check.status == "warn") {
      warnings.append(f"{name}: WARNING ({check.score}/{check.max_score})");
      warnings.append(...check.notes.map(n => f"  - {n}"));
    }
  }

  # Determine overall status
  failCount = Object.values(checks).filter(c => c.status == "fail").length;
  warnCount = Object.values(checks).filter(c => c.status == "warn").length;

  overallStatus: "pass" | "warn" | "fail";
  if (failCount > 0) {
    overallStatus = "fail";
  } else if (warnCount > 1) {
    overallStatus = "warn";
  } else {
    overallStatus = "pass";
  }

  # Determine readiness
  readyFor: string[] = [];
  if (overallStatus == "pass") {
    readyFor.append("outline-collaborator", "drafting");
  } else if (overallStatus == "warn") {
    readyFor.append("review and refinement");
  } else {
    readyFor.append("address issues before proceeding");
  }

  return {
    synthesis_name: synthesis._meta?.synthesis_name or "Unknown",
    overall_status: overallStatus,
    checks,
    issues,
    warnings,
    ready_for: readyFor
  };
}

# == FORMATTING ===

def formatValidationResult(result: ValidationResult): string {
  lines: string[] = [];

  statusEmoji = result.overall_status == "pass" ? "[PASS]" :
                      result.overall_status == "warn" ? "[WARN]" : "[FAIL]";

  lines.append(f"# Validation Result: {result.synthesis_name}");
  lines.append("");
  lines.append(f"## Overall Status: {statusEmoji} {result.overall_status.upper()}");
  lines.append("");

  lines.append("## Check Results");
  lines.append("");
  lines.append("| Check | Status | Score |");
  lines.append("|-------|--------|-------|");

  for name, check in Object.entries(result.checks)) {
    emoji = check.status == "pass" ? "PASS" : check.status == "warn" ? "WARN" : "FAIL";
    lines.append(f"| {name.replace(/_/g, \" \")} | {emoji} | {check.score}/{check.max_score} |");
  }
  lines.append("");

  if (result.issues.length > 0) {
    lines.append("## Issues (Must Fix)");
    lines.append("");
    for issue in result.issues) {
      lines.append(issue);
    }
    lines.append("");
  }

  if (result.warnings.length > 0) {
    lines.append("## Warnings (Consider)");
    lines.append("");
    for warning in result.warnings) {
      lines.append(warning);
    }
    lines.append("");
  }

  lines.append("## Ready For");
  lines.append("");
  for ready in result.ready_for) {
    lines.append(f"- {ready}");
  }
  lines.append("");

  # Detailed notes per check
  lines.append("## Detailed Notes");
  lines.append("");
  for name, check in Object.entries(result.checks)) {
    if (check.notes.length > 0) {
      lines.append(f"### {name.replace(/_/g, \" \")}");
      for note in check.notes) {
        lines.append(f"- {note}");
      }
      lines.append("");
    }
  }

  return lines.join("\n");
}

# == MAIN ===

def main(): void {
  args = sys.argv[1:];

  # Help
  if (args.includes("--help") or args.includes("-h")) {
    print(f"Validate Synthesis

Usage:
  deno run --allow-read scripts/validate-synthesis.ts synthesis.json
  deno run --allow-read scripts/validate-synthesis.ts synthesis.json --against source.json
  deno run --allow-read scripts/validate-synthesis.ts synthesis.json --genre drama
  deno run --allow-read scripts/validate-synthesis.ts synthesis.json --full

Options:
  --against <file>   Source DNA to validate coverage against
  --genre <name>     Target genre to check alignment
  --full             Run all checks with verbose output
  --json             Output as JSON

Checks Performed:
  - Completeness: Are all required sections present?
  - Orthogonality: Do new forms avoid surface translation?
  - Function Coverage: Are source functions served?
  - Context Coherence: Do forms fit the target context?
  - Genre Alignment: Does synthesis deliver intended emotional experience?
");
    sys.exit(0);
  }

  isJson = args.includes("--json");
  isFull = args.includes("--full");

  # Parse arguments
  againstIndex = args.indexOf("--against");
  againstFile = againstIndex != -1 ? args[againstIndex + 1] : None;

  genreIndex = args.indexOf("--genre");
  genre = genreIndex != -1 ? args[genreIndex + 1] : None;

  # Find synthesis file (first positional argument)
  skipIndices = new Set<number>();
  if (againstIndex != -1) {
    skipIndices.add(againstIndex);
    skipIndices.add(againstIndex + 1);
  }
  if (genreIndex != -1) {
    skipIndices.add(genreIndex);
    skipIndices.add(genreIndex + 1);
  }

  synthesisFile: string | None = None;
  for (i = 0; i < args.length; i++) {
    if (!args[i].startswith("--") and !skipIndices.has(i)) {
      synthesisFile = args[i];
      break;
    }
  }

  if (!synthesisFile) {
    print("Error: Please provide a synthesis file to validate");
    print("Usage: deno run --allow-read scripts/validate-synthesis.ts synthesis.json");
    sys.exit(1);
  }

  # Load synthesis document
  synthesis: SynthesisDocument;
  try {
    content = open(synthesisFile, "r", encoding="utf-8").read();
    synthesis = json.loads(content);
  } catch (e) {
    print(f"Error reading synthesis file: {e}");
    sys.exit(1);
  }

  # Load source DNA if provided
  source: DNADocument | None = None;
  if (againstFile) {
    try {
      content = open(againstFile, "r", encoding="utf-8").read();
      source = json.loads(content);
    } catch (e) {
      print(f"Error reading source DNA file: {e}");
      sys.exit(1);
    }
  }

  # Run validation
  result = runValidation(synthesis, source, genre);

  # Output
  if (isJson) {
    print(json.dumps(result, None, 2));
  } else {
    print(formatValidationResult(result));
  }
}

main();


if __name__ == "__main__":
    main()
