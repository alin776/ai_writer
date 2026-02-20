#!/usr/bin/env python3

"""
Scene Scoring Calculator for Chapter-Drafter Orchestrator

Calculates composite scores from pass evaluations.
Used to determine ACCEPT/REVISE/REWRITE/REJECT outcomes.

Usage:
  python scripts/score_scene.py --example
  python scripts/score_scene.py --json '{...}'
"""

import copy
import json
import sys

PASS_WEIGHTS = {
    "scene-sequencing": 0.35,
    "character-arc": 0.25,
    "cliche-transcendence": 0.15,
    "dialogue": 0.15,
    "prose-style": 0.1,
}

RATING_SCORES = {"PASS": 100, "WARN": 85, "FAIL": 60}

THRESHOLDS = {"ACCEPT": 80, "REVISE": 60, "REWRITE": 40}


def calculate_pass_score(criteria):
    """Calculate score for a single pass based on its criteria."""
    if not criteria:
        return 0
    total = sum(RATING_SCORES[c["rating"]] for c in criteria)
    return round(total / len(criteria))


def calculate_composite_score(passes):
    """Calculate composite score from all passes."""
    weighted_sum = 0
    total_weight = 0
    for p in passes:
        weight = PASS_WEIGHTS.get(p["pass"], 0)
        score = p.get("score") if p.get("score") is not None else calculate_pass_score(p["criteria"])
        weighted_sum += score * weight
        total_weight += weight
    return round(weighted_sum / total_weight) if total_weight > 0 else 0


def determine_decision(composite, passes):
    """Determine decision based on composite score."""
    seq = next((p for p in passes if p["pass"] == "scene-sequencing"), None)
    if seq and any(c["rating"] == "FAIL" for c in seq["criteria"]):
        return "REWRITE"
    if composite >= THRESHOLDS["ACCEPT"]:
        return "ACCEPT"
    if composite >= THRESHOLDS["REVISE"]:
        return "REVISE"
    if composite >= THRESHOLDS["REWRITE"]:
        return "REWRITE"
    return "REJECT"


def find_lowest_scoring_pass(passes):
    """Find the lowest-scoring pass for targeted revision."""
    lowest = None
    lowest_score = float("inf")
    for p in passes:
        score = p.get("score") if p.get("score") is not None else calculate_pass_score(p["criteria"])
        if score < lowest_score:
            lowest_score = score
            lowest = p
    return lowest["pass"] if lowest else None


def get_failing_criteria(passes):
    """Get all failing criteria across all passes."""
    failing = []
    for p in passes:
        for criterion in p["criteria"]:
            if criterion["rating"] == "FAIL":
                failing.append({"pass": p["pass"], "criterion": criterion})
    return failing


def evaluate_scene(evaluation):
    """Process a complete scene evaluation."""
    for p in evaluation["passes"]:
        p["score"] = calculate_pass_score(p["criteria"])
    evaluation["composite"] = calculate_composite_score(evaluation["passes"])
    evaluation["decision"] = determine_decision(evaluation["composite"], evaluation["passes"])
    return evaluation


def generate_report(evaluation):
    """Generate a summary report."""
    lines = []
    lines.append("# Scene Evaluation: {}".format(evaluation["scene"]))
    lines.append("")
    lines.append("## Pass Scores")
    lines.append("")
    lines.append("| Pass | Score | Weight | Weighted |")
    lines.append("|------|-------|--------|----------|")
    for p in evaluation["passes"]:
        weight = PASS_WEIGHTS.get(p["pass"], 0)
        weighted = round(p.get("score", 0) * weight)
        lines.append("| {} | {} | {}% | {} |".format(
            p["pass"], p.get("score", 0), int(weight * 100), weighted))
    lines.append("")
    lines.append("**Composite Score:** {}".format(evaluation.get("composite", "")))
    lines.append("**Decision:** {}".format(evaluation.get("decision", "")))
    lines.append("")
    failing = get_failing_criteria(evaluation["passes"])
    if failing:
        lines.append("## Failing Criteria")
        lines.append("")
        for f in failing:
            notes = " - " + f["criterion"]["notes"] if f["criterion"].get("notes") else ""
            lines.append("- **{}**: {}{}".format(f["pass"], f["criterion"]["name"], notes))
        lines.append("")
    if evaluation.get("decision") == "REVISE":
        lp = find_lowest_scoring_pass(evaluation["passes"])
        lines.append("## Revision Guidance")
        lines.append("")
        lines.append("Target lowest-scoring pass: **{}**".format(lp))
        lines.append("")
    return "\n".join(lines)


EXAMPLE_EVALUATION = {
    "scene": "Chapter 1, Scene 3",
    "passes": [
        {"pass": "scene-sequencing", "criteria": [
            {"name": "Goal clarity", "rating": "PASS"},
            {"name": "Conflict escalation", "rating": "PASS"},
            {"name": "Disaster quality", "rating": "WARN", "notes": "Simple No ending"},
            {"name": "Sequel presence", "rating": "PASS"},
            {"name": "Scene-sequel ratio", "rating": "PASS"},
        ]},
        {"pass": "character-arc", "criteria": [
            {"name": "Lie visibility", "rating": "PASS"},
            {"name": "Want/Need gap", "rating": "PASS"},
            {"name": "Arc progress", "rating": "WARN", "notes": "Arc static this scene"},
            {"name": "Transformation markers", "rating": "PASS"},
        ]},
        {"pass": "cliche-transcendence", "criteria": [
            {"name": "Form axis", "rating": "PASS"},
            {"name": "Knowledge axis", "rating": "WARN", "notes": "Mentor too plot-aware"},
            {"name": "Goal axis", "rating": "PASS"},
            {"name": "Role axis", "rating": "PASS"},
        ]},
        {"pass": "dialogue", "criteria": [
            {"name": "Voice distinctiveness", "rating": "PASS"},
            {"name": "Subtext presence", "rating": "WARN", "notes": "Some on-the-nose lines"},
            {"name": "Double-duty test", "rating": "PASS"},
            {"name": "Naturalness", "rating": "PASS"},
            {"name": "Exposition handling", "rating": "PASS"},
        ]},
        {"pass": "prose-style", "criteria": [
            {"name": "Sentence variety", "rating": "PASS"},
            {"name": "Clarity", "rating": "PASS"},
            {"name": "Voice consistency", "rating": "PASS"},
            {"name": "Economy", "rating": "PASS"},
            {"name": "Active voice", "rating": "PASS"},
        ]},
    ],
}


def main():
    args = sys.argv[1:]

    if "--help" in args or "-h" in args:
        print("Scene Scoring Calculator for Chapter-Drafter")
        print("")
        print("Usage:")
        print("  score_scene.py --example          Run with example evaluation")
        print("  score_scene.py --json '<json>'    Evaluate JSON input")
        print("")
        print("Pass Weights:")
        print("  scene-sequencing:     35%")
        print("  character-arc:        25%")
        print("  cliche-transcendence: 15%")
        print("  dialogue:             15%")
        print("  prose-style:          10%")
        print("")
        print("Decision Thresholds:")
        print("  ACCEPT:  >= 80")
        print("  REVISE:  60-79")
        print("  REWRITE: 40-59")
        print("  REJECT:  < 40")
        sys.exit(0)

    if "--example" in args:
        result = evaluate_scene(copy.deepcopy(EXAMPLE_EVALUATION))
        print(generate_report(result))
        print("\n---\n")
        print("JSON Output:")
        print(json.dumps(result, indent=2))
        sys.exit(0)

    if "--json" in args:
        idx = args.index("--json")
        if idx + 1 < len(args):
            try:
                data = json.loads(args[idx + 1])
                result = evaluate_scene(data)
                print(generate_report(result))
            except Exception as e:
                print("Error parsing JSON: {}".format(e), file=sys.stderr)
                sys.exit(1)
            sys.exit(0)

    print("Run with --example to see sample evaluation")
    print("Run with --help for usage information")


if __name__ == "__main__":
    main()
