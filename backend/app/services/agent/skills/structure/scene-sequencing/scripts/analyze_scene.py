#!/usr/bin/env python3
"""Scene Structure Analyzer."""
import sys, re, json

GOAL_PATTERNS = [
    re.compile(r"\b(want|wanted|wants|need|needed|needs|must|had to|have to|trying to|attempted to|goal|objective|mission)\b", re.I),
    re.compile(r"\b(determined to|resolved to|set out to|aimed to|intended to)\b", re.I),
    re.compile(r"\b(find|get|reach|escape|stop|save|discover|learn|prove)\b", re.I),
]
CONFLICT_PATTERNS = [
    re.compile(r"\b(but|however|although|despite|yet|still|unfortunately)\b", re.I),
    re.compile(r"\b(blocked|stopped|prevented|refused|denied|resisted|fought|struggled)\b", re.I),
    re.compile(r"\b(problem|obstacle|challenge|difficulty|trouble|threat|danger)\b", re.I),
    re.compile(r"\b(against|versus|confronted|opposed|clashed)\b", re.I),
]
DISASTER_PATTERNS = [
    re.compile(r"\b(failed|lost|fell|collapsed|shattered|ruined|destroyed)\b", re.I),
    re.compile(r"\b(worse|terrible|horrible|devastating|catastrophic)\b", re.I),
    re.compile(r"\b(trapped|caught|discovered|exposed|betrayed)\b", re.I),
    re.compile(r"\b(too late|no way|impossible|hopeless)\b", re.I),
    re.compile(r"\b(and then|but then|suddenly|without warning)\b", re.I),
]
REACTION_PATTERNS = [
    re.compile(r"\b(felt|feeling|emotion|heart|stomach|chest|tears)\b", re.I),
    re.compile(r"\b(shock|horror|despair|grief|anger|fear|relief)\b", re.I),
    re.compile(r"\b(couldn't believe|couldn't think|mind raced|thoughts)\b", re.I),
    re.compile(r"\b(sat|stood|stared|gazed|looked)\s+(there|still|frozen|numb)", re.I),
]
DILEMMA_PATTERNS = [
    re.compile(r"\b(choice|decision|option|alternative|either|or)\b", re.I),
    re.compile(r"\b(could|should|might|what if|if only)\b", re.I),
    re.compile(r"\b(on one hand|on the other|weighing|considering)\b", re.I),
    re.compile(r"\b(no good options|impossible choice|between)\b", re.I),
]
DECISION_PATTERNS = [
    re.compile(r"\b(decided|decision|chose|choice|resolved|determined)\b", re.I),
    re.compile(r"\b(would|going to|had to|must|will)\b", re.I),
    re.compile(r"\b(plan|strategy|next step|only way|one thing)\b", re.I),
    re.compile(r"\b(stood up|got up|turned|headed|set off|began)\b", re.I),
]

def count_matches(text, patterns):
    matches = []
    for p in patterns:
        found = p.findall(text)
        if found: matches.extend(found[:3])
    return list(set(matches))[:5]

def calc_dialogue(text):
    quotes = re.findall(r'"[^"]+"', text)
    return sum(len(q) for q in quotes) / len(text) if text else 0

def analyze_scene(text):
    words = [w for w in re.split(r"\s+", text) if w]
    paras = [p for p in re.split(r"\n\s*\n", text) if p.strip()]
    gi = count_matches(text, GOAL_PATTERNS)
    ci = count_matches(text, CONFLICT_PATTERNS)
    di = count_matches(text, DISASTER_PATTERNS)
    ri = count_matches(text, REACTION_PATTERNS)
    dli = count_matches(text, DILEMMA_PATTERNS)
    dci = count_matches(text, DECISION_PATTERNS)
    ss = len(gi) + len(ci) + len(di)
    sq = len(ri) + len(dli) + len(dci)
    ratio = ss / (ss + sq) if (ss + sq) > 0 else 0.5
    pacing = "action-heavy" if ratio > 0.65 else ("reflective" if ratio < 0.35 else "balanced")
    issues, recs = [], []
    if not gi: issues.append("No clear goal detected"); recs.append("Establish POV character wants")
    if not ci: issues.append("No conflict indicators"); recs.append("Add opposition")
    if not di and ss > 0: issues.append("Scene may end too cleanly"); recs.append("Consider worse outcome")
    if ratio > 0.8: issues.append("Very action-heavy"); recs.append("Add sequel beats")
    if ratio < 0.2 and len(words) > 500: issues.append("Extended reflection"); recs.append("Move toward decision")
    if ri and not dci: issues.append("Reaction without decision"); recs.append("End with commitment to action")
    return {"wordCount": len(words), "paragraphCount": len(paras),
        "dialogueRatio": calc_dialogue(text),
        "goalIndicators": gi, "conflictIndicators": ci, "disasterIndicators": di,
        "reactionIndicators": ri, "dilemmaIndicators": dli, "decisionIndicators": dci,
        "estimatedSceneRatio": ratio, "pacingAssessment": pacing,
        "issues": issues, "recommendations": recs}

def format_report(r):
    out = ["# Scene Structure Analysis"]
    out.append("Words: %d, Paragraphs: %d" % (r["wordCount"], r["paragraphCount"]))
    out.append("Dialogue: %.1f%%, Pacing: %s, Scene ratio: %.0f%%" % (r["dialogueRatio"]*100, r["pacingAssessment"], r["estimatedSceneRatio"]*100))
    out.append("")
    for key, label in [("goalIndicators","Goal"),("conflictIndicators","Conflict"),("disasterIndicators","Disaster"),("reactionIndicators","Reaction"),("dilemmaIndicators","Dilemma"),("decisionIndicators","Decision")]:
        v = r[key]
        out.append("  %s: %s" % (label, ", ".join(v) if v else "None detected"))
    if r["issues"]:
        out.append("\nIssues:")
        for i in r["issues"]: out.append("  - " + i)
    if r["recommendations"]:
        out.append("\nRecommendations:")
        for i in r["recommendations"]: out.append("  - " + i)
    return "\n".join(out)

def main():
    args = sys.argv[1:]
    if "--help" in args or "-h" in args:
        print("Usage: python analyze_scene.py <file> [--json] [--text TEXT]"); sys.exit(0)
    json_out = "--json" in args
    text = ""
    if "--text" in args:
        idx = args.index("--text")
        text = args[idx + 1] if idx + 1 < len(args) else ""
    else:
        farg = next((x for x in args if not x.startswith("--")), None)
        if farg:
            try:
                with open(farg, "r", encoding="utf-8") as f: text = f.read()
            except Exception as e: print("Error: %s" % e, file=sys.stderr); sys.exit(1)
        else: print("Error: No input.", file=sys.stderr); sys.exit(1)
    if not text.strip(): print("Error: Empty input", file=sys.stderr); sys.exit(1)
    result = analyze_scene(text)
    print(json.dumps(result, indent=2) if json_out else format_report(result))

if __name__ == "__main__": main()
