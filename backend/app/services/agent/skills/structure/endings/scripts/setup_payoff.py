#!/usr/bin/env python3
import sys
import os
import re
import json
from datetime import datetime

#
 # Setup-Payoff Tracker
 #
 # Tracks setups (Chekhov's guns) and payoffs across a story.
 # Helps identify unresolved setups and payoffs without setup.
 #
 # Usage:
 #   deno run --allow-read setup-payoff.ts --analyze story.txt
 #   deno run --allow-read setup-payoff.ts --setup "rusty key" --file story.txt
 #   deno run --allow-read setup-payoff.ts --list story.txt
 #


# Setup patterns - things introduced that might need payoff
SETUP_PATTERNS: { type; patterns }[] = [
 :
    type: "object",
    patterns: [
      re.compile(r"\b(noticed|saw|spotted|found|discovered|picked up|grabbed|took|carried|kept|hidden|concealed)\s+(a|an|the)\s+([a-z]+\s+)?([a-z]+)", re.I),
      re.compile(r"\b(the|a|an)\s+([a-z]+\s+)?(key|gun|knife|sword|letter|photograph|ring|necklace|book|box|bag|case|weapon|tool)\b", re.I),
    ],
 :
    type: "skill",
    patterns: [
      re.compile(r"\b(knew how to|could|was able to|trained in|learned|practiced|mastered|skilled at|expert in)\b", re.I),
      re.compile(r"\b(years of|experience with|background in|history of)\b", re.I),
    ],
 :
    type: "character",
    patterns: [
      re.compile(r"\b(had\s+a\s+(brother|sister|friend|enemy|rival|ally)|someone\s+who|a\s+person\s+from)\b", re.I),
      re.compile(r"\b(old\s+(friend|enemy|acquaintance)|former\s+(colleague|partner|lover))\b", re.I),
    ],
 :
    type: "information",
    patterns: [
      re.compile(r"\b(secret|knew\s+that|heard\s+that|remembered|recalled|once\s+told|mentioned)\b", re.I),
      re.compile(r"\b(no\s+one\s+knew|only\s+\w+\s+knew|hidden\s+truth|the\s+real\s+reason)\b", re.I),
    ],
 :
    type: "threat",
    patterns: [
      re.compile(r"\b(would\s+return|wasn't\s+over|still\s+out\s+there|waiting|watching|someday)\b", re.I),
      re.compile(r"\b(warned|threatened|promised\s+to|swore\s+to|vowed)\b", re.I),
    ],
 :
    type: "promise",
    patterns: [
      re.compile(r"\b(promised|swore|vowed|committed|pledged|gave\s+\w+\s+word)\b", re.I),
      re.compile(r"\b(would\s+never|would\s+always|one\s+day|someday)\b", re.I),
    ],
 :
    type: "foreshadow",
    patterns: [
      re.compile(r"\b(little\s+did|if\s+only|would\s+later|couldn't\s+have\s+known|foreshadow)\b", re.I),
      re.compile(r"\b(ominous|foreboding|sense\s+of|feeling\s+that|premonition)\b", re.I),
    ],
]

# Payoff patterns - things that might be resolving setups
PAYOFF_PATTERNS: { type; patterns }[] = [
 :
    type: "object",
    patterns: [
      re.compile(r"\b(used|pulled\s+out|reached\s+for|grabbed|produced|wielded|fired|unlocked|opened\s+with)\b", re.I),
      re.compile(r"\b(the\s+(key|gun|knife|sword|letter|ring|weapon)\s+(worked|opened|saved|killed|revealed))\b", re.I),
    ],
 :
    type: "skill",
    patterns: [
      re.compile(r"\b(finally\s+could|now\s+knew\s+how|training\s+paid\s+off|skills\s+saved|experience\s+told)\b", re.I),
      re.compile(r"\b(years\s+of\s+\w+\s+paid\s+off|remembered\s+how\s+to)\b", re.I),
    ],
 :
    type: "character",
    patterns: [
      re.compile(r"\b(arrived|appeared|returned|showed\s+up|came\s+back|was\s+there)\b", re.I),
      re.compile(r"\b(unexpected\s+ally|old\s+friend\s+\w+|recognized)\b", re.I),
    ],
 :
    type: "information",
    patterns: [
      re.compile(r"\b(realized|understood|finally\s+knew|the\s+truth\s+was|now\s+it\s+made\s+sense)\b", re.I),
      re.compile(r"\b(revealed|exposed|came\s+to\s+light|discovered\s+that)\b", re.I),
    ],
 :
    type: "threat",
    patterns: [
      re.compile(r"\b(returned|came\s+back|finally\s+struck|made\s+good|carried\s+out)\b", re.I),
      re.compile(r"\b(defeated|destroyed|overcame|escaped|survived|confronted)\b", re.I),
    ],
 :
    type: "promise",
    patterns: [
      re.compile(r"\b(kept\s+\w+\s+promise|fulfilled|honored|made\s+good|finally\s+could)\b", re.I),
      re.compile(r"\b(as\s+promised|True\s+to\s+\w+\s+word|never\s+forgot)\b", re.I),
    ],
 :
    type: "foreshadow",
    patterns: [
      re.compile(r"\b(just\s+as|as\s+foretold|the\s+prophecy|finally|inevitable)\b", re.I),
      re.compile(r"\b(now\s+understood|saw\s+it\s+coming|knew\s+it\s+would)\b", re.I),
    ],
]

def getLineContext(text, position, windowSize = 50):
  start = max(0, position - windowSize)
  end = min(len(text), position + windowSize)
  context = text.slice(start, end).replace(re.compile(r"\n", 0), " ").strip()
  if (start > 0) context = "..." + context
  if (end < len(text)) context = context + "..."
  return context

def findSetups(text):
  setups = []
  textLength = len(text)

  for (const { type, patterns } of SETUP_PATTERNS):
    for pattern in patterns:
      regex = re.compile(pattern.source, pattern.flags)
      match
      while (match = regex.exec(text)) != None:
        # Only consider setups in first 70% of text
        positionPercent = (match.index / textLength) * 100
        if positionPercent <= 70:
          setups.append({
            text: match[0].lower().strip(),
            position: match.index,
            positionPercent.round(positionPercent),
            type,
            lineContext: getLineContext(text, match.index),
          })

  # Deduplicate by text similarity
  unique = []
  for setup in setups:
    isDuplicate = unique.some(
      u => u.text == setup.text and Math.abs(u.position - setup.position) < 100
    )
    if !isDuplicate:
      unique.append(setup)

  return unique.sort((a, b) => a.position - b.position)

def findPayoffs(text):
  payoffs = []
  textLength = len(text)

  for (const { type, patterns } of PAYOFF_PATTERNS):
    for pattern in patterns:
      regex = re.compile(pattern.source, pattern.flags)
      match
      while (match = regex.exec(text)) != None:
        # Only consider payoffs in last 50% of text
        positionPercent = (match.index / textLength) * 100
        if positionPercent >= 50:
          payoffs.append({
            text: match[0].lower().strip(),
            position: match.index,
            positionPercent.round(positionPercent),
            type,
            lineContext: getLineContext(text, match.index),
          })

  # Deduplicate
  unique = []
  for payoff in payoffs:
    isDuplicate = unique.some(
      u => u.text == payoff.text and Math.abs(u.position - payoff.position) < 100
    )
    if !isDuplicate:
      unique.append(payoff)

  return unique.sort((a, b) => a.position - b.position)

function matchSetupsToPayoffs(
  setups,
  payoffs,
  textLength
): { matched; unresolved; orphaned }:
  matched = []
  usedSetups = new Set<number>()
  usedPayoffs = new Set<number>()

  # Match by type and position
  for i in range(0, len(setups)):
    setup = setups[i]
    for j in range(0, len(payoffs)):
      if (usedPayoffs.has(j)) continue

      payoff = payoffs[j]
      if setup.type == payoff.type and payoff.position > setup.position:
        matched.append({
          setup,
          payoff,
          distance: payoff.position - setup.position,
          distancePercent.round(((payoff.position - setup.position) / textLength) * 100),
        })
        usedSetups.add(i)
        usedPayoffs.add(j)
        break

  unresolved = setups.filter((_, i) => !usedSetups.has(i))
  orphaned = payoffs.filter((_, i) => !usedPayoffs.has(i))

  return { matched, unresolved, orphaned }

def searchForTerm(text, term): found; occurrences: { position; percent; context }[] }:
  termLower = term.lower()
  textLower = text.lower()
  occurrences: { position; percent; context }[] = []

  pos = 0
  while (pos = textLower.indexOf(termLower, pos)) != -1:
    occurrences.append({
      position: pos,
      percent.round((pos / len(text)) * 100),
      context: getLineContext(text, pos, 60),
    })
    pos += len(termLower)

  return { found: len(occurrences) > 0, occurrences }

def analyzeSetupPayoff(text, fileName = "input"):
  words = text.split(re.compile(r"\s+", 0)).filter(w => len(w) > 0)
  setups = findSetups(text)
  payoffs = findPayoffs(text)
  { matched, unresolved, orphaned } = matchSetupsToPayoffs(setups, payoffs, len(text))

  issues = []
  recommendations = []

  # Assess health
  health: "good" | "issues" | "problems" = "good"

  if len(unresolved) > 3:
    health = "problems"
    issues.append(f"${len(unresolved)} potential setups without payoffs detected")
    recommendations.append("Review unresolved setups - either pay them off or remove them")
  elif len(unresolved) > 0:
    health = "issues"
    issues.append(f"${len(unresolved)} potential unresolved setup(s)")

  if len(orphaned) > 2:
    health = health == "good" ? "issues" : health
    issues.append(f"${len(orphaned)} potential payoffs without clear setup (deus ex machina risk)")
    recommendations.append("Ensure late-story resolutions are established earlier")

  if len(matched) == 0 and len(setups) > 0:
    issues.append("No setup-payoff matches detected - story may lack satisfying resolution")
    recommendations.append("Track your setups and ensure they pay off by the end")

  # Check for setups too close to payoff
  quickPayoffs = matched.filter(m => m.distancePercent < 10)
  if len(quickPayoffs) > 0:
    issues.append("Some setups pay off very quickly (may reduce impact)")
    recommendations.append("Consider more distance between setup and payoff for greater impact")

  return:
    fileName,
    wordCount: len(words),
    potentialSetups: setups,
    potentialPayoffs: payoffs,
    matchedPairs: matched,
    unresolvedSetups: unresolved,
    orphanedPayoffs: orphaned,
    setupPayoffHealth: health,
    issues,
    recommendations,

def formatReport(analysis):
  lines = []

  lines.append("# Setup-Payoff Analysis\n")
  lines.append(f"File: ${analysis.fileName}")
  lines.append(f"Words: ${analysis.wordCount}")
  lines.append(f"Health: ${analysis.setupPayoffHealth.upper()}\n")

  lines.append("## Summary\n")
  lines.append(f"  Potential setups detected: ${analysis.len(potentialSetups)}")
  lines.append(f"  Potential payoffs detected: ${analysis.len(potentialPayoffs)}")
  lines.append(f"  Matched pairs: ${analysis.len(matchedPairs)}")
  lines.append(f"  Unresolved setups: ${analysis.len(unresolvedSetups)}")
  lines.append(f"  Orphaned payoffs: ${analysis.len(orphanedPayoffs)}")
  lines.append("")

  if analysis.len(matchedPairs) > 0:
    lines.append("## Matched Setup-Payoff Pairs\n")
    for pair in analysis.matchedPairs[0:10]:
      lines.append(f"  [${pair.setup.type}] Setup at ${pair.setup.positionPercent}% �� Payoff at ${pair.payoff.positionPercent}%")
      lines.append(f"    Setup: "${pair.setup.text}"")
      lines.append(f"    Payoff: "${pair.payoff.text}"")
      lines.append("")
    if analysis.len(matchedPairs) > 10:
      lines.append(f"  ... and ${analysis.len(matchedPairs) - 10} more pairs\n")

  if analysis.len(unresolvedSetups) > 0:
    lines.append("## Unresolved Setups (Chekhov's Guns Unfired)\n")
    for setup in analysis.unresolvedSetups[0:10]:
      lines.append(f"  [${setup.type}] at ${setup.positionPercent}%: "${setup.text}"")
      lines.append(f"    Context: ${setup.lineContext}")
      lines.append("")

  if analysis.len(orphanedPayoffs) > 0:
    lines.append("## Orphaned Payoffs (Possible Deus Ex Machina)\n")
    for payoff in analysis.orphanedPayoffs[0:10]:
      lines.append(f"  [${payoff.type}] at ${payoff.positionPercent}%: "${payoff.text}"")
      lines.append(f"    Context: ${payoff.lineContext}")
      lines.append("")

  if analysis.len(issues) > 0:
    lines.append("## Issues\n")
    for issue in analysis.issues:
      lines.append(f"  - ${issue}")
    lines.append("")

  if analysis.len(recommendations) > 0:
    lines.append("## Recommendations\n")
    for rec in analysis.recommendations:
      lines.append(f"  - ${rec}")
    lines.append("")

  return lines.join("\n")

def main():
  args = sys.argv[1:]

  if args.includes("--help") or args.includes("-h"):
    console.log("""Setup-Payoff Tracker

Usage:
  deno run --allow-read setup-payoff.ts --analyze <file>
  deno run --allow-read setup-payoff.ts --setup "term" --file <file>
  deno run --allow-read setup-payoff.ts --list <file>

Modes:
  --analyze      Full setup-payoff analysis
  --setup "X"    Search for specific term throughout story
  --list         List all detected setups and payoffs

Options:
  --file <f>     Specify input file
  --json         Output as JSON
  --help         Show this message

Detects:
  - Objects (Chekhov's gun)
  - Skills (training/ability)
  - Characters (allies, enemies)
  - Information (secrets, knowledge)
  - Threats (warnings, foreshadowing)
  - Promises (commitments)
""");
    sys.exit(0)

  jsonOutput = args.includes("--json")
  text = ""
  fileName = "input"

  # Get file
  fileIndex = args.indexOf("--file")
  if fileIndex != -1 and args[fileIndex + 1]:
    fileName = args[fileIndex + 1]
    try:
      text = open(fileName, 'r', encoding='utf-8').read()
    except Exception as e:
      print(f"Error reading file: ${e}")
      sys.exit(1)
  else:
    # Try to find file as positional arg
    file = args.find(a => !a.startswith("--") and a != args[args.indexOf("--setup") + 1])
    if file:
      fileName = file
      try:
        text = open(file, 'r', encoding='utf-8').read()
      except Exception as e:
        print(f"Error reading file: ${e}")
        sys.exit(1)

  if !text.strip():
    print("Error file provided. Use --file <path> or provide path as argument.")
    sys.exit(1)

  # Search for specific setup
  if args.includes("--setup"):
    setupIndex = args.indexOf("--setup")
    term = args[setupIndex + 1]
    if !term:
      print("Error: --setup requires a search term")
      sys.exit(1)

    result = searchForTerm(text, term)
    if jsonOutput:
      print(json.dumps(result, None, 2))
    else:
      print(f"\n# Search for "${term}"\n")
      if result.found:
        print(f"Found ${result.len(occurrences)} occurrence(s):\n")
        for occ in result.occurrences:
          print(f"  At ${occ.percent}%: ${occ.context}\n")
      else:
        print("Term not found in text.")
    sys.exit(0)

  # List mode
  if args.includes("--list"):
    setups = findSetups(text)
    payoffs = findPayoffs(text)

    if jsonOutput:
      print(json.dumps({ setups, payoffs }, None, 2))
    else:
      print("\n# Detected Setups (first 70%)\n")
      for s in setups:
        print(f"  [${s.type}] ${s.positionPercent}%: "${s.text}"")
      print("\n# Detected Payoffs (last 50%)\n")
      for p in payoffs:
        print(f"  [${p.type}] ${p.positionPercent}%: "${p.text}"")
    sys.exit(0)

  # Full analysis
  analysis = analyzeSetupPayoff(text, fileName)

  if jsonOutput:
    print(json.dumps(analysis, None, 2))
  else:
    print(formatReport(analysis))

main()