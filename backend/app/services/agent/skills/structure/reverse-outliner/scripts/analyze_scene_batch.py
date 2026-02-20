#!/usr/bin/env python3
import sys
import os
import re
import json
from datetime import datetime

#
 # Batch Scene Structure Analyzer
 #
 # Applies scene-sequencing analysis (Goal/Conflict/Disaster) to all scenes
 # in a segmented book. Builds on patterns from scene-sequencing skill.
 #
 # Usage:
 #   deno run --allow-read scripts/analyze-scene-batch.ts segments.json book.txt
 #   deno run --allow-read scripts/analyze-scene-batch.ts segments.json book.txt --output scenes.json
 #

# == INTERFACES ==


# == PATTERNS (from scene-sequencing skill) ==

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

# Disaster type patterns
DISASTER_TYPE_PATTERNS =:
  "yes-but": [re.compile(r"\byes,?\s*but\b", re.I), re.compile(r"\bsucceeded,?\s*but\b", re.I), re.compile(r"\bgot\s+it,?\s*but\b", re.I)],
  "no": [re.compile(r"\bfailed\b", re.I), re.compile(r"\bcouldn't\b", re.I), re.compile(r"\bdidn't\b", re.I), re.compile(r"\bwasn't able\b", re.I)],
  "no-and-furthermore": [re.compile(r"\bnot only.+but also\b", re.I), re.compile(r"\bworse,?\s*\b", re.I), re.compile(r"\band then.+also\b", re.I), re.compile(r"\bon top of that\b", re.I)],

# == UTILITIES ==

def countMatches(text, patterns):
  matches = []
  for pattern in patterns:
    found = text.match(pattern)
    if found:
      matches.append(...found[0:3])
  return [...set(matches)][0:5]

def calculateConfidence(indicators, text):
  if (len(indicators) == 0) return 0
  wordCount = text.split(re.compile(r"\s+", 0)).length
  # More indicators relative to length = higher confidence
  density = len(indicators) / (wordCount / 100)
  return min(1, density * 0.3 + (len(indicators) > 2 ? 0.4 : 0.2))

def detectDisasterType(text):
  for (const [type, patterns] of DISASTER_TYPE_PATTERNS.items()):
    for pattern in patterns:
      if pattern.test(text):
        return type
  return "unclear"

function inferFunction(
  sceneIndex,
  totalScenes,
  analysis
):
  position = sceneIndex / totalScenes

  # Opening scenes
  if sceneIndex == 0:
    return "Opening scene - establishes status quo and character"

  # First 10% - setup
  if position < 0.10:
    return "Setup - introducing world and characters"

  # Around 12% - inciting incident
  if position >= 0.10 and position <= 0.15:
    if analysis.structure.disaster.detected:
      return "Inciting incident - story catalyst"

  # First plot point area (20-25%)
  if position >= 0.20 and position <= 0.25:
    if analysis.structure.goal.confidence > 0.6:
      return "First plot point - protagonist commits"

  # Rising action (25-45%)
  if position > 0.25 and position < 0.45:
    return "Rising action - escalating conflict"

  # Midpoint area (45-55%)
  if position >= 0.45 and position <= 0.55:
    if analysis.structure.conflict.confidence > 0.7:
      return "Midpoint - mirror moment or major revelation"

  # Complications (55-75%)
  if position > 0.55 and position < 0.75:
    return "Complications - stakes raise, options narrow"

  # Dark night (75-85%)
  if position >= 0.75 and position <= 0.85:
    if analysis.pacing == "reflective" or analysis.sequelElements.dilemma:
      return "Dark night - lowest point, crisis"

  # Climax (85-95%)
  if position >= 0.85 and position <= 0.95:
    if analysis.pacing == "action-heavy":
      return "Climax - final confrontation"

  # Resolution (95%+)
  if position > 0.95:
    return "Resolution - new equilibrium established"

  # Default based on pacing
  if analysis.pacing == "action-heavy":
    return "Action scene - conflict-driven"
  elif analysis.pacing == "reflective":
    return "Sequel scene - reaction and planning"

  return "Development scene - advancing plot/character"

def generateSummary(indicators, elementType):
  if len(indicators) == 0:
    return f"No clear ${elementType} detected"
  return f"${elementType.charAt(0).upper() + elementType[1:]} indicators: ${indicators[0:3].join(", ")}"

# == CORE LOGIC ==

function analyzeScene(
  sceneId,
  chapterNumber,
  text,
  pov,
  sceneIndex,
  totalScenes
):
  wordCount = text.split(re.compile(r"\s+", 0)).filter(w => len(w) > 0).length

  # Detect elements
  goalIndicators = countMatches(text, GOAL_PATTERNS)
  conflictIndicators = countMatches(text, CONFLICT_PATTERNS)
  disasterIndicators = countMatches(text, DISASTER_PATTERNS)
  reactionIndicators = countMatches(text, REACTION_PATTERNS)
  dilemmaIndicators = countMatches(text, DILEMMA_PATTERNS)
  decisionIndicators = countMatches(text, DECISION_PATTERNS)

  # Calculate scene vs sequel ratio
  sceneScore = len(goalIndicators) + len(conflictIndicators) + len(disasterIndicators)
  sequelScore = len(reactionIndicators) + len(dilemmaIndicators) + len(decisionIndicators)
  totalScore = sceneScore + sequelScore or 1
  sceneRatio = sceneScore / totalScore

  # Determine pacing
  pacing: "action-heavy" | "balanced" | "reflective"
  if sceneRatio > 0.65:
    pacing = "action-heavy"
  elif sceneRatio < 0.35:
    pacing = "reflective"
  else:
    pacing = "balanced"

  # Build analysis
  analysis =:
    id: sceneId,
    chapterNumber,
    pov,
    wordCount,
    structure::
      goal::
        detected: len(goalIndicators) > 0,
        confidence: calculateConfidence(goalIndicators, text),
        indicators: goalIndicators,
        summary: generateSummary(goalIndicators, "goal"),
      conflict::
        detected: len(conflictIndicators) > 0,
        confidence: calculateConfidence(conflictIndicators, text),
        indicators: conflictIndicators,
        summary: generateSummary(conflictIndicators, "conflict"),
      disaster::
        detected: len(disasterIndicators) > 0,
        confidence: calculateConfidence(disasterIndicators, text),
        indicators: disasterIndicators,
        summary: generateSummary(disasterIndicators, "disaster"),
        type: detectDisasterType(text),
    sequelElements::
      reaction: len(reactionIndicators) > 0,
      dilemma: len(dilemmaIndicators) > 0,
      decision: len(decisionIndicators) > 0,
    sceneSequelRatio.round(sceneRatio * 100) / 100,
    pacing,
    function: "",  # Will be set below
    issues: [],

  # Infer function based on position and analysis
  analysis.function = inferFunction(sceneIndex, totalScenes, analysis)

  # Detect issues
  if !analysis.structure.goal.detected:
    analysis.issues.append("No clear goal detected in scene opening")
  if !analysis.structure.conflict.detected:
    analysis.issues.append("No conflict indicators detected")
  if !analysis.structure.disaster.detected and sceneScore > 0:
    analysis.issues.append("Scene may end without clear disaster/outcome")
  if sceneRatio > 0.85:
    analysis.issues.append("Very action-heavy - minimal reflection time")
  if sceneRatio < 0.15 and wordCount > 500:
    analysis.issues.append("Extended reflection without action")

  return analysis

function extractSceneText(
  bookText,
  startLine,
  endLine
):
  lines = bookText.split("\n")
  # Convert 1-based line numbers to 0-based indices
  return lines.slice(startLine - 1, endLine).join("\n")

function analyzeAllScenes(
  segments,
  bookText
):
  scenes = []

  # Count total scenes for position calculation
  totalScenes = 0
  for chapter in segments.chapters:
    totalScenes += chapter.len(scenes)

  sceneIndex = 0

  for chapter in segments.chapters:
    for scene in chapter.scenes:
      sceneText = extractSceneText(bookText, scene.startLine, scene.endLine)
      analysis = analyzeScene(
        scene.id,
        chapter.number,
        sceneText,
        scene.povCandidate,
        sceneIndex,
        totalScenes
      )
      scenes.append(analysis)
      sceneIndex++

  # Calculate summary statistics
  avgConfidence = scenes.reduce((sum, s) =>
    sum + (s.structure.goal.confidence + s.structure.conflict.confidence + s.structure.disaster.confidence) / 3,
    0
  ) / len(scenes)

  pacingDistribution =:
    actionHeavy: scenes.filter(s => s.pacing == "action-heavy").length,
    balanced: scenes.filter(s => s.pacing == "balanced").length,
    reflective: scenes.filter(s => s.pacing == "reflective").length,

  issuesCount = scenes.reduce((sum, s) => sum + s.len(issues), 0)

  return:
    title: segments.title,
    analyzedAt: datetime.now().isoformat(),
    scenes,
    summary::
      totalScenes: len(scenes),
      avgConfidence.round(avgConfidence * 100) / 100,
      pacingDistribution,
      issuesCount,

# == CLI ==

def printHelp():
  console.log("""Batch Scene Structure Analyzer

Usage:
  deno run --allow-read scripts/analyze-scene-batch.ts <segments.json> <book.txt> [options]

Arguments:
  segments.json    Output from segment-book.ts
  book.txt         Original book text file

Options:
  --output <file>  Write output to JSON file (default: stdout)
  --depth <level>  Analysis depth: quick, standard, detailed (default: standard)
  --help, -h       Show this help message

Examples:
  deno run --allow-read analyze-scene-batch.ts segments.json novel.txt
  deno run --allow-read analyze-scene-batch.ts segments.json novel.txt --output scenes.json
""");

def main():
  args = sys.argv[1:]

  if args.includes("--help") or args.includes("-h") or len(args) < 2:
    printHelp()
    sys.exit(0)

  # Parse arguments
  segmentsFile = ""
  bookFile = ""
  outputFile = ""

  skipIndices = new Set<number>()

  for i in range(0, len(args)):
    if (skipIndices.has(i)) continue

    if args[i] == "--output" and args[i + 1]:
      outputFile = args[i + 1]
      skipIndices.add(i + 1)
    elif args[i] == "--depth" and args[i + 1]:
      # depth is captured but not used differently in this version
      skipIndices.add(i + 1)
    elif !args[i].startswith("--"):
      if !segmentsFile:
        segmentsFile = args[i]
      elif !bookFile:
        bookFile = args[i]

  if !segmentsFile or !bookFile:
    print("Error segments.json and book.txt are required")
    sys.exit(1)

  # Read files
  segments
  bookText

  try:
    segmentsJson = open(segmentsFile, 'r', encoding='utf-8').read()
    segments = json.loads(segmentsJson)
  except Exception as e:
    print(f"Error reading segments file: ${e instanceof Error ? e.message : e}")
    sys.exit(1)

  try:
    bookText = open(bookFile, 'r', encoding='utf-8').read()
  except Exception as e:
    print(f"Error reading book file: ${e instanceof Error ? e.message : e}")
    sys.exit(1)

  # Analyze all scenes
  result = analyzeAllScenes(segments, bookText)

  # Output
  jsonOutput = json.dumps(result, None, 2)

  if outputFile:
    open(outputFile, 'w', encoding='utf-8').write(jsonOutput)
    print(f"Analysis complete: ${result.summary.totalScenes} scenes analyzed")
    print(f"Average confidence: ${result.summary.avgConfidence}")
    print(f"Pacing: ${result.summary.pacingDistribution.actionHeavy} action-heavy, ${result.summary.pacingDistribution.balanced} balanced, ${result.summary.pacingDistribution.reflective} reflective")
    print(f"Output written to: ${outputFile}")
  else:
    print(jsonOutput)

main()