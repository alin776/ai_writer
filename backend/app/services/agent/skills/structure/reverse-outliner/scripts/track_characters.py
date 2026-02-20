#!/usr/bin/env python3
import sys
import os
import re
import json
from datetime import datetime

#
 # Character Tracking Script
 #
 # Identifies protagonist and major characters, tracks their arcs.
 # Uses patterns from character-arc skill.
 #
 # Usage:
 #   deno run --allow-read scripts/track-characters.ts segments.json book.txt
 #   deno run --allow-read scripts/track-characters.ts segments.json book.txt --output characters.json
 #

# == INTERFACES ==


# == PATTERNS ==

# Patterns for detecting arc elements
LIE_PATTERNS = [
  re.compile(r"\b(always believed|never thought|everyone knew|I know that|it's just how|the world is)\b", re.I),
  re.compile(r"\b(can't trust|don't need|won't ever|could never)\b", re.I),
  re.compile(r"\b(believed that|convinced that|certain that)\b", re.I),
]

WANT_PATTERNS = [
  re.compile(r"\b(wanted nothing more|goal was|dream of|hoped to|wished for)\b", re.I),
  re.compile(r"\b(must find|must get|must have|need to)\b", re.I),
  re.compile(r"\b(desperate to|determined to|obsessed with)\b", re.I),
]

NEED_PATTERNS = [
  re.compile(r"\b(really needed|actually need|what .+ truly|deep down)\b", re.I),
  re.compile(r"\b(connection|trust|acceptance|love|forgiveness)\b", re.I),
]

GHOST_PATTERNS = [
  re.compile(r"\b(remembered|memory|flashback|years ago|back when)\b", re.I),
  re.compile(r"\b(never forgot|haunted by|couldn't forget|still remembered)\b", re.I),
  re.compile(r"\b(reminded .+ of|took .+ back to)\b", re.I),
]

TRUTH_PATTERNS = [
  re.compile(r"\b(finally understood|realized that|saw clearly|for the first time)\b", re.I),
  re.compile(r"\b(had been wrong|changed .+ mind|no longer believed)\b", re.I),
  re.compile(r"\b(truth was|saw the truth|understood now)\b", re.I),
]

TRANSFORMATION_PATTERNS = [
  re.compile(r"\b(different person|changed|transformed|no longer the same)\b", re.I),
  re.compile(r"\b(let go of|accepted that|embraced)\b", re.I),
  re.compile(r"\b(chose to|decided to|committed to)\b", re.I),
]

# POV indicators for scoring
POV_INDICATORS = [
  re.compile(r"\bthought\b", re.I),
  re.compile(r"\bfelt\b", re.I),
  re.compile(r"\bknew\b", re.I),
  re.compile(r"\bwondered\b", re.I),
  re.compile(r"\brealized\b", re.I),
]

# == UTILITIES ==

def extractSceneText(bookText, startLine, endLine):
  lines = bookText.split("\n")
  return lines.slice(startLine - 1, endLine).join("\n")

def countNameMentions(text, name):
  pattern = re.compile(f"\\b${name}\\b", "gi")
  matches = text.match(pattern)
  return matches ? len(matches) : 0

def extractProperNouns(text):
  names = new Map<string, number>()

  # Match capitalized words that look like names
  namePattern = re.compile(r"\b([A-Z][a-z]{2,})\b", 0)
  match

  while (match = namePattern.exec(text)) != None:
    name = match[1]

    # Filter out common non-name words
    nonNames = new Set([
      "The", "This", "That", "There", "These", "Those", "When", "Where",
      "What", "Which", "While", "After", "Before", "During", "Through",
      "Chapter", "Part", "One", "Two", "Three", "First", "Second", "Third",
      "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday",
      "January", "February", "March", "April", "May", "June", "July", "August",
      "September", "October", "November", "December",
    ])

    if !nonNames.has(name):
      names.set(name, (names.get(name) or 0) + 1)

  return names

def findPovScore(text, name):
  score = 0

  # Check for "Name thought/felt/knew" patterns
  for pattern in POV_INDICATORS:
    namePattern = re.compile(f"\\b${name}\\s+${pattern.source}", "gi")
    matches = text.match(namePattern)
    if matches:
      score += len(matches) * 2

  # Check for "'s thoughts/feelings" patterns
  possessivePatterns = [
    re.compile(f"\\b${name}'s\\s+(thoughts?|mind|heart|eyes|stomach)", "gi"),
    re.compile(f"\\b${name}'s\\s+(face|expression|voice)\\s+(showed|revealed|betrayed)", "gi"),
  ]

  for pattern in possessivePatterns:
    matches = text.match(pattern)
    if matches:
      score += len(matches)

  return score

def findPatternEvidence(text, patterns, name):
  evidence = []

  for pattern in patterns:
    # Look for pattern near character name
    sentences = text.split(re.compile(r"[.!?]+", 0))
    for sentence in sentences:
      if sentence.includes(name) and pattern.test(sentence):
        cleaned = sentence.strip().substring(0, 100)
        if cleaned and !evidence.includes(cleaned):
          evidence.append(cleaned + (len(sentence) > 100 ? "..." : ""))

  return evidence[0:3]

def inferArcType(arcComponents):
  hasLie = arcComponents.lie != None or arcComponents.len(lieEvidence) > 0
  hasTruth = arcComponents.truthAcceptance != None
  hasTransformation = arcComponents.transformation != None

  if hasLie and hasTruth and hasTransformation:
    return "positive"

  if hasLie and !hasTruth:
    # Could be negative or ongoing
    return "negative"

  if !hasLie and hasTransformation:
    return "flat"

  return "unclear"

function inferRole(
  isProtagonist,
  povCount,
  mentions,
  arcType
):
  if isProtagonist:
    return "Protagonist"

  if povCount > 5:
    if arcType == "flat":
      return "Mentor figure"
    return "Major viewpoint character"

  if mentions > 20:
    return "Supporting character"

  return "Minor character"

# == CORE LOGIC ==

function trackCharacters(
  segments,
  bookText,
  options::
    protagonistName?
    maxSecondary?
  } = {}
):
  maxSecondary = options.maxSecondary or 5

  # Extract all proper nouns and count occurrences
  nameFrequency = extractProperNouns(bookText)

  # Build character candidates with POV scoring
  candidates::
    name
    mentions
    povScore
    povScenes
    firstAppearance
    scenes
  }[] = []

  # Track POV candidates from segmentation
  povCounts = new Map<string, number>()
  firstAppearances = new Map<string, string>()

  for chapter in segments.chapters:
    for scene in chapter.scenes:
      if scene.povCandidate and scene.povCandidate != "[First Person]":
        povCounts.set(scene.povCandidate, (povCounts.get(scene.povCandidate) or 0) + 1)
        if !firstAppearances.has(scene.povCandidate):
          firstAppearances.set(scene.povCandidate, scene.id)

  # Combine frequency data with POV data
  for (const [name, mentions] of nameFrequency.entries()):
    if (mentions < 5) continue;  # Skip rarely mentioned names

    povScore = findPovScore(bookText, name)
    povScenes = povCounts.get(name) or 0

    candidates.append({
      name,
      mentions,
      povScore,
      povScenes,
      firstAppearance: firstAppearances.get(name) or "ch1-s1",
      scenes: new Set<string>(),
    })

  # Sort by combined score (POV weighted heavily)
  candidates.sort((a, b) =>:
    scoreA = a.povScenes * 10 + a.povScore * 2 + a.mentions
    scoreB = b.povScenes * 10 + b.povScore * 2 + b.mentions
    return scoreB - scoreA
  })

  # Override protagonist if specified
  if options.protagonistName:
    existing = candidates.findIndex(c =>
      c.name.lower() == options.protagonistName!.lower()
    )
    if existing > 0:
      [protagonist] = candidates.splice(existing, 1)
      candidates.unshift(protagonist)

  # Analyze protagonist
  protagonist = None
  if len(candidates) > 0:
    protag = candidates[0]

    # Find arc components
    arcComponents =:
      lie: None,
      lieEvidence: findPatternEvidence(bookText, LIE_PATTERNS, protag.name),
      want: None,
      need: None,
      ghost: None,
      ghostScene: None,
      truthAcceptance: None,
      transformation: None,

    # Extract specific component summaries
    wantEvidence = findPatternEvidence(bookText, WANT_PATTERNS, protag.name)
    if len(wantEvidence) > 0:
      arcComponents.want = wantEvidence[0]

    needEvidence = findPatternEvidence(bookText, NEED_PATTERNS, protag.name)
    if len(needEvidence) > 0:
      arcComponents.need = needEvidence[0]

    ghostEvidence = findPatternEvidence(bookText, GHOST_PATTERNS, protag.name)
    if len(ghostEvidence) > 0:
      arcComponents.ghost = ghostEvidence[0]

    truthEvidence = findPatternEvidence(bookText, TRUTH_PATTERNS, protag.name)
    if len(truthEvidence) > 0:
      arcComponents.truthAcceptance = truthEvidence[0]

    transformEvidence = findPatternEvidence(bookText, TRANSFORMATION_PATTERNS, protag.name)
    if len(transformEvidence) > 0:
      arcComponents.transformation = transformEvidence[0]

    if arcComponents.len(lieEvidence) > 0:
      arcComponents.lie = arcComponents.lieEvidence[0]

    # Find key scenes (scenes with significant arc moments)
    keyScenes = []
    for chapter in segments.chapters:
      for scene in chapter.scenes:
        sceneText = extractSceneText(bookText, scene.startLine, scene.endLine)
        nameMentions = countNameMentions(sceneText, protag.name)

        # Check if scene has arc-relevant content
        hasArcContent =
          LIE_PATTERNS.some(p => p.test(sceneText) and sceneText.includes(protag.name)) ||
          TRUTH_PATTERNS.some(p => p.test(sceneText) and sceneText.includes(protag.name)) ||
          TRANSFORMATION_PATTERNS.some(p => p.test(sceneText) and sceneText.includes(protag.name))

        if (scene.povCandidate == protag.name or nameMentions > 5) and hasArcContent:
          keyScenes.append(scene.id)

    arcType = inferArcType(arcComponents)

    protagonist =:
      name: protag.name,
      firstAppearance: protag.firstAppearance,
      povScenes: protag.povScenes,
      mentions: protag.mentions,
      arcType,
      arcComponents,
      keyScenes: keyScenes[0:10],
      role: "Protagonist",

  # Analyze secondary characters
  secondaryCharacters = []
  for i in range(1, len(candidates) and len(secondaryCharacters) < maxSecondary):
    char = candidates[i]

    arcComponents =:
      lie: None,
      lieEvidence: findPatternEvidence(bookText, LIE_PATTERNS, char.name)[0:1],
      want: None,
      need: None,
      ghost: None,
      ghostScene: None,
      truthAcceptance: None,
      transformation: None,

    if arcComponents.len(lieEvidence) > 0:
      arcComponents.lie = arcComponents.lieEvidence[0]

    arcType = inferArcType(arcComponents)

    # Find key scenes for this character
    keyScenes = []
    for chapter in segments.chapters:
      for scene in chapter.scenes:
        if scene.povCandidate == char.name:
          keyScenes.append(scene.id)

    secondaryCharacters.append({
      name: char.name,
      firstAppearance: char.firstAppearance,
      povScenes: char.povScenes,
      mentions: char.mentions,
      arcType,
      arcComponents,
      keyScenes: keyScenes[0:5],
      role: inferRole(False, char.povScenes, char.mentions, arcType),
    })

  # Build character web (relationships based on co-occurrence)
  characterWeb = {}

  if protagonist:
    for secondary in secondaryCharacters:
      # Simple relationship inference based on context
      pairKey = f"${protagonist.name.lower()}-${secondary.name.lower()}"
      characterWeb[pairKey] = "relationship detected";  # Would need more sophisticated analysis for actual relationship types

  return:
    protagonist,
    secondaryCharacters,
    characterWeb,
    trackedAt: datetime.now().isoformat(),

# == CLI ==

def printHelp():
  console.log("""Character Tracking Script

Usage:
  deno run --allow-read scripts/track-characters.ts <segments.json> <book.txt> [options]

Arguments:
  segments.json      Output from segment-book.ts
  book.txt           Original book text file

Options:
  --output <file>      Write output to JSON file (default: stdout)
  --protagonist <name> Specify protagonist name (overrides detection)
  --max-secondary <n>  Maximum secondary characters to track (default: 5)
  --help, -h           Show this help message

Examples:
  deno run --allow-read track-characters.ts segments.json novel.txt
  deno run --allow-read track-characters.ts segments.json novel.txt --output characters.json
  deno run --allow-read track-characters.ts segments.json novel.txt --protagonist "Sarah Chen"
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
  protagonistName = ""
  maxSecondary = 5

  skipIndices = new Set<number>()

  for i in range(0, len(args)):
    if (skipIndices.has(i)) continue

    if args[i] == "--output" and args[i + 1]:
      outputFile = args[i + 1]
      skipIndices.add(i + 1)
    elif args[i] == "--protagonist" and args[i + 1]:
      protagonistName = args[i + 1]
      skipIndices.add(i + 1)
    elif args[i] == "--max-secondary" and args[i + 1]:
      maxSecondary = parseInt(args[i + 1], 10) or 5
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

  # Track characters
  result = trackCharacters(segments, bookText,:
    protagonistName: protagonistName or undefined,
    maxSecondary,
  })

  # Output
  jsonOutput = json.dumps(result, None, 2)

  if outputFile:
    open(outputFile, 'w', encoding='utf-8').write(jsonOutput)
    print("Character tracking complete")
    if result.protagonist:
      print(f"Protagonist: ${result.protagonist.name} (${result.protagonist.arcType} arc, ${result.protagonist.povScenes} POV scenes)")
    print(f"Secondary characters: ${result.secondaryCharacters.map(c => c.name).join(", ")}")
    print(f"Output written to: ${outputFile}")
  else:
    print(jsonOutput)

main()
