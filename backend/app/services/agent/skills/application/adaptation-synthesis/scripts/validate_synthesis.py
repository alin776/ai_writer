#!/usr/bin/env python3
"""
validate_synthesis.py - Synthesis Validation Tool

Checks synthesis documents for completeness, function coverage,
and alignment with source DNA and target genre.

Usage:
  python validate_synthesis.py synthesis.json
  python validate_synthesis.py synthesis.json --against source.json
  python validate_synthesis.py synthesis.json --genre drama
  python validate_synthesis.py synthesis.json --full
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

# == VALIDATION LOGIC ==


def validate_completeness(synthesis):
    notes = []
    score = 0
    max_score = 10

    meta = synthesis.get("_meta", {})

    # Check meta fields
    if meta.get("synthesis_name"):
        score += 1
    else:
        notes.append("Missing synthesis name")

    if meta.get("target_context"):
        score += 1
    else:
        notes.append("Missing target context")

    if meta.get("primary_source"):
        score += 1
    else:
        notes.append("Missing primary source reference")

    if meta.get("target_genre"):
        score += 1
    else:
        notes.append("Missing target genre")

    # Check context mapping
    context_mapping = synthesis.get("context_mapping", {})
    if context_mapping and len(context_mapping) > 0:
        score += 2
        if len(context_mapping) >= 4:
            score += 1
        else:
            notes.append("Context mapping could be more detailed")
    else:
        notes.append("Missing context mapping")

    # Check function mappings
    func_mapping = synthesis.get("function_to_form_mapping", {})
    if func_mapping and len(func_mapping) > 0:
        score += 2
        mapping_count = len(func_mapping)
        if mapping_count >= 5:
            score += 1
        else:
            notes.append(f"Only {mapping_count} function mappings - consider adding more")
    else:
        notes.append("Missing function-to-form mappings")

    # Check character synthesis
    char_synthesis = synthesis.get("character_synthesis", {})
    if not char_synthesis or len(char_synthesis) == 0:
        notes.append("Missing character synthesis")

    status = "pass" if score >= 8 else ("warn" if score >= 5 else "fail")
    return {
        "status": status,
        "score": score,
        "max_score": max_score,
        "notes": notes
    }


def validate_orthogonality(synthesis):
    notes = []
    score = 0
    max_score = 10

    func_mapping = synthesis.get("function_to_form_mapping")
    if not func_mapping:
        return {
            "status": "fail",
            "score": 0,
            "max_score": max_score,
            "notes": ["No function mappings to check for orthogonality"]
        }

    mappings = list(func_mapping.items())
    passed_checks = 0
    explicitly_marked = 0

    for func, mapping in mappings:
        # Check if orthogonality was explicitly evaluated
        orth_check = mapping.get("orthogonality_check", "")
        if orth_check:
            explicitly_marked += 1
            if "pass" in orth_check.lower():
                passed_checks += 1
            elif "fail" in orth_check.lower():
                notes.append(f"Orthogonality FAILED for: {func}")
            else:
                notes.append(f"Unclear orthogonality status for: {func}")

        # Heuristic checks for surface translation
        new_form = mapping.get("new_form", "")
        original_form = mapping.get("original_form", "")
        if new_form and original_form:
            original_lower = original_form.lower()
            new_lower = new_form.lower()

            # Check for obvious 1:1 translations
            surface_indicators = ["space ", "cyber", "future ", "sci-fi ", "fantasy "]
            for indicator in surface_indicators:
                if indicator in new_lower and indicator not in original_lower:
                    notes.append(f'Possible surface translation: "{new_form}" - just adding setting prefix?')
                    break

    # Score based on explicit checks
    if len(mappings) > 0:
        if explicitly_marked == len(mappings):
            score += 4
        elif explicitly_marked > 0:
            score += 2
            notes.append(f"Only {explicitly_marked}/{len(mappings)} mappings have explicit orthogonality check")
        else:
            notes.append("No explicit orthogonality checks recorded")

        pass_rate = passed_checks / len(mappings) if len(mappings) > 0 else 0
        score += round(pass_rate * 6)

    status = "pass" if score >= 8 else ("warn" if score >= 5 else "fail")
    return {
        "status": status,
        "score": score,
        "max_score": max_score,
        "notes": notes
    }


def validate_function_coverage(synthesis, source):
    notes = []
    score = 0
    max_score = 10

    func_mapping = synthesis.get("function_to_form_mapping")
    if not func_mapping:
        return {
            "status": "fail",
            "score": 0,
            "max_score": max_score,
            "notes": ["No function mappings present"]
        }

    mapped_functions = list(func_mapping.keys())

    # Basic: has some mappings
    if len(mapped_functions) > 0:
        score += 2

    # Check that mappings have functions_served
    functions_served = 0
    for mapping in func_mapping.values():
        fs = mapping.get("functions_served", [])
        if fs and len(fs) > 0:
            functions_served += len(fs)

    if functions_served >= 10:
        score += 3
    elif functions_served >= 5:
        score += 2
        notes.append("Consider documenting more functions served by each mapping")
    else:
        score += 1
        notes.append("Few functions documented - synthesis may have gaps")

    # If we have source DNA, check coverage
    if source and source.get("structural_requirements"):
        requirements = source["structural_requirements"]
        covered = 0

        for req in requirements:
            # Check if any mapping mentions this requirement
            req_words = req.lower().split()
            found = False

            for mapping in func_mapping.values():
                mapping_text = json.dumps(mapping).lower()
                if any(len(word) > 4 and word in mapping_text for word in req_words):
                    found = True
                    break

            if found:
                covered += 1

        coverage_rate = covered / len(requirements) if len(requirements) > 0 else 0
        score += round(coverage_rate * 5)

        if coverage_rate < 1:
            notes.append(f"{len(requirements) - covered}/{len(requirements)} structural requirements may not be covered")
    else:
        # No source to check against - assume reasonable coverage
        score += 3
        notes.append("No source DNA provided - cannot verify full function coverage")

    status = "pass" if score >= 8 else ("warn" if score >= 5 else "fail")
    return {
        "status": status,
        "score": score,
        "max_score": max_score,
        "notes": notes
    }


def validate_context_coherence(synthesis):
    notes = []
    score = 0
    max_score = 10

    # Check context mapping exists and is substantive
    context_mapping = synthesis.get("context_mapping", {})
    if not context_mapping or len(context_mapping) == 0:
        return {
            "status": "fail",
            "score": 0,
            "max_score": max_score,
            "notes": ["No context mapping present"]
        }

    context_fields = list(context_mapping.keys())
    context_values = list(context_mapping.values())

    # Basic: has context mapping
    score += 2

    # Check for key context elements
    desired_fields = ["setting", "power_structure", "information_control", "escape_prevention"]
    fields_present = 0
    for field in desired_fields:
        if any(field.replace("_", "") in f.lower() for f in context_fields):
            fields_present += 1
    score += min(4, fields_present)
    if fields_present < len(desired_fields):
        missing = [f for f in desired_fields if not any(f.replace("_", "") in cf.lower() for cf in context_fields)]
        notes.append(f"Consider adding context for: {', '.join(missing)}")

    # Check that context values are substantive (not just placeholders)
    substantive_values = [v for v in context_values if v and len(str(v)) > 10]
    if len(substantive_values) == len(context_values):
        score += 2
    else:
        notes.append("Some context values seem like placeholders")
        score += 1

    # Check function mappings fit context
    func_mapping = synthesis.get("function_to_form_mapping")
    if func_mapping:
        context_text = json.dumps(context_mapping).lower()
        coherent = 0
        mappings = list(func_mapping.values())

        for mapping in mappings:
            # Basic heuristic: new form should use words from context
            new_form = mapping.get("new_form", "")
            if new_form:
                form_words = new_form.lower().split()
                if any(len(w) > 4 and w in context_text for w in form_words):
                    coherent += 1

        if len(mappings) > 0:
            coherence_rate = coherent / len(mappings)
            score += round(coherence_rate * 2)
            if coherence_rate < 0.5:
                notes.append("Some new forms may not fit the defined context")

    status = "pass" if score >= 8 else ("warn" if score >= 5 else "fail")
    return {
        "status": status,
        "score": score,
        "max_score": max_score,
        "notes": notes
    }


def validate_genre_alignment(synthesis, target_genre, source):
    notes = []
    score = 0
    max_score = 10

    genre = target_genre or synthesis.get("_meta", {}).get("target_genre")

    if not genre:
        return {
            "status": "warn",
            "score": 5,
            "max_score": max_score,
            "notes": ["No target genre specified - cannot validate alignment"]
        }

    # Has explicit genre
    score += 2

    # Check if source genre matches (if available)
    source_genre = ""
    if source:
        source_genre = source.get("emotional_core", {}).get("primary_genre", "")
    if source_genre:
        if source_genre.lower() == genre.lower():
            score += 3
            notes.append("Target genre matches source primary genre")
        else:
            notes.append(f"Source genre ({source_genre}) differs from target ({genre}) - intentional shift?")
            score += 1
    else:
        score += 2

    # Check tone synthesis for genre appropriateness
    tone_synthesis = synthesis.get("tone_synthesis")
    if tone_synthesis:
        score += 2
        tone = json.dumps(tone_synthesis).lower()
        genre_lower = genre.lower()

        if genre_lower == "horror" and "dread" not in tone and "fear" not in tone and "unease" not in tone:
            notes.append("Horror genre but tone doesn't mention dread/fear/unease")
        if genre_lower == "humor" and "comic" not in tone and "funny" not in tone and "wit" not in tone:
            notes.append("Humor genre but tone doesn't mention comedy elements")
        if genre_lower == "drama" and "light" in tone and "comedy" in tone:
            notes.append("Drama genre but tone seems light - intentional dramedy?")
    else:
        notes.append("No tone synthesis - harder to verify genre alignment")

    # Check for explicit genre validation in document
    validation = synthesis.get("validation", {})
    genre_check = validation.get("genre_check", "")
    if genre_check and "pass" in genre_check.lower():
        score += 3
    elif genre_check:
        score += 1
        notes.append("Genre check in document doesn't indicate clear pass")

    status = "pass" if score >= 8 else ("warn" if score >= 5 else "fail")
    return {
        "status": status,
        "score": score,
        "max_score": max_score,
        "notes": notes
    }


def run_validation(synthesis, source, target_genre):
    completeness = validate_completeness(synthesis)
    orthogonality = validate_orthogonality(synthesis)
    function_coverage = validate_function_coverage(synthesis, source)
    context_coherence = validate_context_coherence(synthesis)
    genre_alignment = validate_genre_alignment(synthesis, target_genre, source)

    checks = {
        "function_coverage": function_coverage,
        "orthogonality": orthogonality,
        "context_coherence": context_coherence,
        "genre_alignment": genre_alignment,
        "completeness": completeness
    }

    # Aggregate issues and warnings
    issues = []
    warnings = []

    for name, check in checks.items():
        if check["status"] == "fail":
            issues.append(f"{name}: FAILED ({check['score']}/{check['max_score']})")
            for n in check["notes"]:
                issues.append(f"  - {n}")
        elif check["status"] == "warn":
            warnings.append(f"{name}: WARNING ({check['score']}/{check['max_score']})")
            for n in check["notes"]:
                warnings.append(f"  - {n}")

    # Determine overall status
    fail_count = sum(1 for c in checks.values() if c["status"] == "fail")
    warn_count = sum(1 for c in checks.values() if c["status"] == "warn")

    if fail_count > 0:
        overall_status = "fail"
    elif warn_count > 1:
        overall_status = "warn"
    else:
        overall_status = "pass"

    # Determine readiness
    ready_for = []
    if overall_status == "pass":
        ready_for.extend(["outline-collaborator", "drafting"])
    elif overall_status == "warn":
        ready_for.append("review and refinement")
    else:
        ready_for.append("address issues before proceeding")

    return {
        "synthesis_name": synthesis.get("_meta", {}).get("synthesis_name", "Unknown"),
        "overall_status": overall_status,
        "checks": checks,
        "issues": issues,
        "warnings": warnings,
        "ready_for": ready_for
    }


# == FORMATTING ==


def format_validation_result(result):
    lines = []

    if result["overall_status"] == "pass":
        status_label = "[PASS]"
    elif result["overall_status"] == "warn":
        status_label = "[WARN]"
    else:
        status_label = "[FAIL]"

    lines.append(f"# Validation Result: {result['synthesis_name']}")
    lines.append("")
    lines.append(f"## Overall Status: {status_label} {result['overall_status'].upper()}")
    lines.append("")

    lines.append("## Check Results")
    lines.append("")
    lines.append("| Check | Status | Score |")
    lines.append("|-------|--------|-------|")

    for name, check in result["checks"].items():
        if check["status"] == "pass":
            emoji = "PASS"
        elif check["status"] == "warn":
            emoji = "WARN"
        else:
            emoji = "FAIL"
        lines.append(f"| {name.replace('_', ' ')} | {emoji} | {check['score']}/{check['max_score']} |")
    lines.append("")

    if len(result["issues"]) > 0:
        lines.append("## Issues (Must Fix)")
        lines.append("")
        for issue in result["issues"]:
            lines.append(issue)
        lines.append("")

    if len(result["warnings"]) > 0:
        lines.append("## Warnings (Consider)")
        lines.append("")
        for warning in result["warnings"]:
            lines.append(warning)
        lines.append("")

    lines.append("## Ready For")
    lines.append("")
    for ready in result["ready_for"]:
        lines.append(f"- {ready}")
    lines.append("")

    # Detailed notes per check
    lines.append("## Detailed Notes")
    lines.append("")
    for name, check in result["checks"].items():
        if len(check["notes"]) > 0:
            lines.append(f"### {name.replace('_', ' ')}")
            for note in check["notes"]:
                lines.append(f"- {note}")
            lines.append("")

    return "\n".join(lines)


# == MAIN ==

def main():
    args = sys.argv[1:]

    # Help
    if "--help" in args or "-h" in args:
        print("""Validate Synthesis

Usage:
  python validate_synthesis.py synthesis.json
  python validate_synthesis.py synthesis.json --against source.json
  python validate_synthesis.py synthesis.json --genre drama
  python validate_synthesis.py synthesis.json --full

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
""")
        sys.exit(0)

    is_json = "--json" in args
    is_full = "--full" in args

    # Parse arguments
    against_index = args.index("--against") if "--against" in args else -1
    against_file = args[against_index + 1] if against_index != -1 and against_index + 1 < len(args) else None

    genre_index = args.index("--genre") if "--genre" in args else -1
    genre = args[genre_index + 1] if genre_index != -1 and genre_index + 1 < len(args) else None

    # Find synthesis file (first positional argument)
    skip_indices = set()
    if against_index != -1:
        skip_indices.add(against_index)
        skip_indices.add(against_index + 1)
    if genre_index != -1:
        skip_indices.add(genre_index)
        skip_indices.add(genre_index + 1)

    synthesis_file = None
    for i in range(len(args)):
        if not args[i].startswith("--") and i not in skip_indices:
            synthesis_file = args[i]
            break

    if not synthesis_file:
        print("Error: Please provide a synthesis file to validate", file=sys.stderr)
        print("Usage: python validate_synthesis.py synthesis.json", file=sys.stderr)
        sys.exit(1)

    # Load synthesis document
    synthesis = None
    try:
        content = open(synthesis_file, "r", encoding="utf-8").read()
        synthesis = json.loads(content)
    except Exception as e:
        print(f"Error reading synthesis file: {e}", file=sys.stderr)
        sys.exit(1)

    # Load source DNA if provided
    source = None
    if against_file:
        try:
            content = open(against_file, "r", encoding="utf-8").read()
            source = json.loads(content)
        except Exception as e:
            print(f"Error reading source DNA file: {e}", file=sys.stderr)
            sys.exit(1)

    # Run validation
    result = run_validation(synthesis, source, genre)

    # Output
    if is_json:
        print(json.dumps(result, indent=2, ensure_ascii=False))
    else:
        print(format_validation_result(result))


if __name__ == "__main__":
    main()
