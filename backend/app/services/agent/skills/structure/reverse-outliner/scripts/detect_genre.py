#!/usr/bin/env python3
import sys
import os
import re
import json
from datetime import datetime

#
 # Genre Detection Script
 #
 # Identifies primary and secondary elemental genres from text patterns.
 # Maps detected genre to Key Moments framework.
 #
 # Usage:
 #   deno run --allow-read scripts/detect-genre.ts book.txt
 #   deno run --allow-read scripts/detect-genre.ts book.txt --output genre.json
 #

# == INTERFACES ==


# == GENRE PATTERNS ==

# Pattern sets for each elemental genre
GENRE_PATTERNS =:
  wonder: [
    re.compile(r"\b(awe|wonder|amazed|astonished|breathtaking|magnificent|spectacular)\b", re.I),
    re.compile(r"\b(vast|immense|infinite|boundless|cosmic|universe|stars)\b", re.I),
    re.compile(r"\b(discover|revelation|realize|understand|truth|secret)\b", re.I),
    re.compile(r"\b(impossible|unbelievable|unprecedented|never before)\b", re.I),
    re.compile(r"\b(transcend|transform|enlighten|illuminate)\b", re.I),
  ],

  mystery: [
    re.compile(r"\b(clue|evidence|investigate|detective|suspect|witness)\b", re.I),
    re.compile(r"\b(murder|crime|victim|alibi|motive)\b", re.I),
    re.compile(r"\b(puzzle|riddle|mystery|enigma|secret)\b", re.I),
    re.compile(r"\b(uncover|reveal|discover|deduce|solve)\b", re.I),
    re.compile(r"\b(who|what|why|how)\s+(?:did|was|could|would)\b", re.I),
  ],

  adventure: [
    re.compile(r"\b(journey|quest|expedition|voyage|trek|travel)\b", re.I),
    re.compile(r"\b(treasure|map|compass|destination|horizon)\b", re.I),
    re.compile(r"\b(danger|peril|risk|hazard|obstacle)\b", re.I),
    re.compile(r"\b(survive|escape|rescue|explore|discover)\b", re.I),
    re.compile(r"\b(supplies|equipment|provisions|camp|wilderness)\b", re.I),
  ],

  horror: [
    re.compile(r"\b(terror|horror|dread|fear|nightmare|scream)\b", re.I),
    re.compile(r"\b(dark|shadow|darkness|black|sinister)\b", re.I),
    re.compile(r"\b(monster|creature|beast|demon|evil)\b", re.I),
    re.compile(r"\b(dead|death|corpse|grave|blood)\b", re.I),
    re.compile(r"\b(haunted|cursed|possessed|supernatural)\b", re.I),
  ],

  thriller: [
    re.compile(r"\b(bomb|deadline|countdown|ticking|timer)\b", re.I),
    re.compile(r"\b(chase|pursue|hunt|escape|run)\b", re.I),
    re.compile(r"\b(danger|threat|risk|stakes|life|death)\b", re.I),
    re.compile(r"\b(spy|agent|mission|operation|target)\b", re.I),
    re.compile(r"\b(tension|suspense|urgent|critical|time)\b", re.I),
  ],

  relationship: [
    re.compile(r"\b(love|heart|feelings|emotion|romance)\b", re.I),
    re.compile(r"\b(kiss|embrace|touch|together|apart)\b", re.I),
    re.compile(r"\b(relationship|connection|bond|trust)\b", re.I),
    re.compile(r"\b(marry|wedding|proposal|date|romantic)\b", re.I),
    re.compile(r"\b(attraction|desire|longing|yearning)\b", re.I),
  ],

  drama: [
    re.compile(r"\b(choice|decision|dilemma|consequence|regret)\b", re.I),
    re.compile(r"\b(family|father|mother|son|daughter|brother|sister)\b", re.I),
    re.compile(r"\b(guilt|shame|pride|honor|dignity)\b", re.I),
    re.compile(r"\b(sacrifice|forgive|betray|loyalty)\b", re.I),
    re.compile(r"\b(past|memory|secret|truth|lie)\b", re.I),
  ],

  issue: [
    re.compile(r"\b(justice|injustice|rights|freedom|oppression)\b", re.I),
    re.compile(r"\b(society|system|government|power|authority)\b", re.I),
    re.compile(r"\b(debate|argue|believe|opinion|perspective)\b", re.I),
    re.compile(r"\b(moral|ethical|right|wrong|fair)\b", re.I),
    re.compile(r"\b(change|reform|revolution|protest)\b", re.I),
  ],

  ensemble: [
    re.compile(r"\b(team|group|crew|squad|party)\b", re.I),
    re.compile(r"\b(together|cooperation|unity|alliance)\b", re.I),
    re.compile(r"\b(leader|member|role|contribution)\b", re.I),
    re.compile(r"\b(trust|loyalty|betrayal|sacrifice)\b", re.I),
    re.compile(r"\b(diverse|different|unique|each)\b", re.I),
  ],

  humor: [
    re.compile(r"\b(laugh|funny|hilarious|absurd|ridiculous)\b", re.I),
    re.compile(r"\b(joke|comedy|wit|sarcasm|irony)\b", re.I),
    re.compile(r"\b(embarrass|awkward|mishap|disaster)\b", re.I),
    re.compile(r"\b(mock|tease|prank|gag)\b", re.I),
    re.compile(r"\b(silly|goofy|zany|wacky)\b", re.I),
  ],

  idea: [
    re.compile(r"\b(theory|hypothesis|concept|principle|law)\b", re.I),
    re.compile(r"\b(science|technology|experiment|research)\b", re.I),
    re.compile(r"\b(future|evolution|progress|advancement)\b", re.I),
    re.compile(r"\b(what if|imagine|suppose|consider)\b", re.I),
    re.compile(r"\b(implication|consequence|effect|impact)\b", re.I),
  ],

# Key Moments templates by genre
KEY_MOMENTS[]> =:
  wonder: [
    { type: "Initial Encounter", expectedPosition: 0.15, emotionalExperience: "Surprise and awe", storyFunction: "Establishes the spectacular" },
    { type: "Scale Revelation", expectedPosition: 0.35, emotionalExperience: "Humbling realization", storyFunction: "Contextualizes protagonist's place" },
    { type: "Wonder Escalation", expectedPosition: 0.60, emotionalExperience: "Intensification of awe", storyFunction: "Raises stakes and deepens engagement" },
    { type: "Perspective Shift", expectedPosition: 0.75, emotionalExperience: "Paradigm change", storyFunction: "Forces reevaluation" },
    { type: "Transcendent Integration", expectedPosition: 0.90, emotionalExperience: "Meaning-making", storyFunction: "Provides thematic resolution" },
  ],

  mystery: [
    { type: "Question Inception", expectedPosition: 0.10, emotionalExperience: "Curiosity activation", storyFunction: "Establishes the puzzle" },
    { type: "Pattern Recognition", expectedPosition: 0.35, emotionalExperience: "Satisfaction of connection", storyFunction: "Provides momentum" },
    { type: "False Resolution", expectedPosition: 0.55, emotionalExperience: "Surprise from misdirection", storyFunction: "Creates complexity" },
    { type: "Progressive Revelation", expectedPosition: 0.75, emotionalExperience: "Deepening understanding", storyFunction: "Builds toward solution" },
    { type: "Solution Crystallization", expectedPosition: 0.90, emotionalExperience: "Illumination and closure", storyFunction: "Completes emotional journey" },
  ],

  adventure: [
    { type: "Threshold Crossing", expectedPosition: 0.15, emotionalExperience: "Excitement of departure", storyFunction: "Transitions to adventure world" },
    { type: "Capability Test", expectedPosition: 0.30, emotionalExperience: "Confidence from competence", storyFunction: "Establishes abilities" },
    { type: "Resource Depletion", expectedPosition: 0.50, emotionalExperience: "Vulnerability from loss", storyFunction: "Forces adaptation" },
    { type: "Ultimate Challenge", expectedPosition: 0.80, emotionalExperience: "Fear and determination", storyFunction: "Tests protagonist's limits" },
    { type: "Return Transformation", expectedPosition: 0.95, emotionalExperience: "Pride and perspective", storyFunction: "Demonstrates growth" },
  ],

  horror: [
    { type: "Wrongness Glimpse", expectedPosition: 0.10, emotionalExperience: "Unease from dissonance", storyFunction: "Establishes threat potential" },
    { type: "Safety Violation", expectedPosition: 0.30, emotionalExperience: "Shock from boundary breach", storyFunction: "Demonstrates vulnerability" },
    { type: "Threat Escalation", expectedPosition: 0.50, emotionalExperience: "Escalating dread", storyFunction: "Raises stakes" },
    { type: "Failed Solution", expectedPosition: 0.70, emotionalExperience: "Despair from ineffectuality", storyFunction: "Deepens hopelessness" },
    { type: "Confrontation", expectedPosition: 0.90, emotionalExperience: "Terror meets courage", storyFunction: "Provides climactic moment" },
  ],

  thriller: [
    { type: "Stakes Establishment", expectedPosition: 0.15, emotionalExperience: "Concern for outcome", storyFunction: "Sets up tension framework" },
    { type: "Deadline Imposition", expectedPosition: 0.25, emotionalExperience: "Anxiety from time pressure", storyFunction: "Creates urgency" },
    { type: "Near Miss", expectedPosition: 0.50, emotionalExperience: "Relief with lingering tension", storyFunction: "Maintains engagement" },
    { type: "Option Elimination", expectedPosition: 0.75, emotionalExperience: "Mounting pressure", storyFunction: "Forces harder choices" },
    { type: "Decision Under Duress", expectedPosition: 0.90, emotionalExperience: "Catharsis through action", storyFunction: "Provides climactic release" },
  ],

  relationship: [
    { type: "Significant Connection", expectedPosition: 0.10, emotionalExperience: "Recognition of potential", storyFunction: "Establishes relationship basis" },
    { type: "Intimacy Deepening", expectedPosition: 0.35, emotionalExperience: "Warmth from vulnerability", storyFunction: "Develops investment" },
    { type: "Value Conflict", expectedPosition: 0.55, emotionalExperience: "Frustration from differences", storyFunction: "Creates meaningful obstacles" },
    { type: "Relationship Crisis", expectedPosition: 0.75, emotionalExperience: "Heartbreak or betrayal", storyFunction: "Tests connection's resilience" },
    { type: "Reconciliation/Resolution", expectedPosition: 0.90, emotionalExperience: "Emotional closure", storyFunction: "Completes relationship arc" },
  ],

  drama: [
    { type: "Internal Conflict Revelation", expectedPosition: 0.15, emotionalExperience: "Recognition of contradiction", storyFunction: "Establishes character struggle" },
    { type: "External Pressure Point", expectedPosition: 0.35, emotionalExperience: "Stress from circumstances", storyFunction: "Forces character choices" },
    { type: "Failure Moment", expectedPosition: 0.55, emotionalExperience: "Shame from inadequacy", storyFunction: "Deepens character journey" },
    { type: "Truth Confrontation", expectedPosition: 0.75, emotionalExperience: "Painful self-awareness", storyFunction: "Catalyzes change" },
    { type: "Character Evolution", expectedPosition: 0.90, emotionalExperience: "Self-actualization", storyFunction: "Demonstrates growth" },
  ],

  issue: [
    { type: "Perspective Challenge", expectedPosition: 0.15, emotionalExperience: "Intellectual discomfort", storyFunction: "Establishes complexity" },
    { type: "Stake Personalization", expectedPosition: 0.30, emotionalExperience: "Emotional investment", storyFunction: "Makes abstract concrete" },
    { type: "Complexity Recognition", expectedPosition: 0.50, emotionalExperience: "Cognitive expansion", storyFunction: "Prevents simplistic resolution" },
    { type: "Position Testing", expectedPosition: 0.70, emotionalExperience: "Value examination", storyFunction: "Forces intellectual honesty" },
    { type: "Perspective Integration", expectedPosition: 0.90, emotionalExperience: "Nuanced understanding", storyFunction: "Provides thematic resolution" },
  ],

  ensemble: [
    { type: "Group Formation", expectedPosition: 0.15, emotionalExperience: "Belonging potential", storyFunction: "Establishes the collective" },
    { type: "Role Establishment", expectedPosition: 0.30, emotionalExperience: "Identity within community", storyFunction: "Defines character functions" },
    { type: "Group Fracture", expectedPosition: 0.55, emotionalExperience: "Loyalty testing", storyFunction: "Creates internal conflict" },
    { type: "Collective Challenge", expectedPosition: 0.75, emotionalExperience: "Shared adversity", storyFunction: "Forces cooperation" },
    { type: "Synergy Moment", expectedPosition: 0.90, emotionalExperience: "Strength through unity", storyFunction: "Demonstrates group value" },
  ],

  humor: [
    { type: "Setup Establishment", expectedPosition: 0.10, emotionalExperience: "Anticipation", storyFunction: "Creates comedic potential" },
    { type: "Incongruity Introduction", expectedPosition: 0.25, emotionalExperience: "Surprise amusement", storyFunction: "Establishes comedic logic" },
    { type: "Escalation Sequence", expectedPosition: 0.50, emotionalExperience: "Mounting absurdity", storyFunction: "Builds comedic momentum" },
    { type: "Subversion Peak", expectedPosition: 0.75, emotionalExperience: "Maximum comedic release", storyFunction: "Delivers primary payoff" },
    { type: "Resolution Callback", expectedPosition: 0.90, emotionalExperience: "Satisfying closure", storyFunction: "Ties comedic threads" },
  ],

  idea: [
    { type: "Concept Introduction", expectedPosition: 0.10, emotionalExperience: "Intellectual curiosity", storyFunction: "Establishes central idea" },
    { type: "Implication Exploration", expectedPosition: 0.30, emotionalExperience: "Fascination with consequences", storyFunction: "Expands idea's scope" },
    { type: "Edge Case Discovery", expectedPosition: 0.50, emotionalExperience: "Surprise from complexity", storyFunction: "Deepens understanding" },
    { type: "Idea Testing", expectedPosition: 0.70, emotionalExperience: "Tension from stakes", storyFunction: "Makes abstract personal" },
    { type: "Synthesis Resolution", expectedPosition: 0.90, emotionalExperience: "Intellectual satisfaction", storyFunction: "Completes thought experiment" },
  ],

# == UTILITIES ==

def countPatternMatches(text, patterns): count; indicators }:
  indicators = []
  totalCount = 0

  for pattern in patterns:
    matches = text.match(pattern)
    if matches:
      totalCount += len(matches)
      indicators.append(...matches[0:3])

  return:
    count: totalCount,
    indicators: [...set(indicators)][0:10],

def sampleText(text, sampleSize = 10):
  paragraphs = text.split(re.compile(r"\n\s*\n", 0)).filter(p => p.strip().length > 100)

  if len(paragraphs) <= sampleSize:
    return paragraphs

  # Sample from beginning, middle, and end
  samples = []
  thirdSize = int(sampleSize / 3)

  # Beginning
  for i in range(0, thirdSize and i < len(paragraphs)):
    samples.append(paragraphs[i])

  # Middle
  middleStart = int(len(paragraphs) / 2) - int(thirdSize / 2)
  for (let i = middleStart; i < middleStart + thirdSize and i < len(paragraphs); i++):
    if !samples.includes(paragraphs[i]):
      samples.append(paragraphs[i])

  # End
  endStart = len(paragraphs) - thirdSize
  for (let i = endStart; i < len(paragraphs); i++):
    if !samples.includes(paragraphs[i]):
      samples.append(paragraphs[i])

  return samples

# == CORE LOGIC ==

def detectGenre(text, sampleSize = 10):
  # Sample text to analyze
  samples = sampleText(text, sampleSize)
  sampledText = samples.join("\n\n")

  # Count matches for each genre
  evidence = {}
  scores: { genre; score }[] = []

  for (const [genre, patterns] of GENRE_PATTERNS.items()):
    result = countPatternMatches(sampledText, patterns)
    evidence[genre] =:
      count: result.count,
      indicators: result.indicators,
    scores.append({ genre, score: result.count })

  # Sort by score
  scores.sort((a, b) => b.score - a.score)

  # Calculate confidence based on how much higher primary is than others
  totalScore = scores.reduce((sum, s) => sum + s.score, 0) or 1
  primaryScore = scores[0]?.score or 0
  primaryConfidence = min(1, (primaryScore / totalScore) + (primaryScore > 10 ? 0.2 : 0))

  # Get secondary genres (those with > 30% of primary's score)
  secondaryGenres = scores
    [1:4]
    .filter(s => s.score > primaryScore * 0.3)
    .map(s => s.genre)

  # Get Key Moments for primary genre
  primaryGenre = scores[0]?.genre or "drama";  # Default to drama if unclear
  keyMomentTemplates = KEY_MOMENTS[primaryGenre] or KEY_MOMENTS.drama

  expectedKeyMoments = keyMomentTemplates.map(km => ({
    ...km,
    foundAt: None,
    foundScene: None,
  }))

  return:
    primaryGenre,
    primaryConfidence.round(primaryConfidence * 100) / 100,
    secondaryGenres,
    evidence,
    keyMomentsFramework: primaryGenre,
    expectedKeyMoments,
    detectedAt: datetime.now().isoformat(),

# == CLI ==

def printHelp():
  console.log("""Genre Detection Script

Usage:
  deno run --allow-read scripts/detect-genre.ts <book.txt> [options]

Options:
  --output <file>       Write output to JSON file (default: stdout)
  --sample-size <n>     Number of text samples to analyze (default: 10)
  --help, -h            Show this help message

Examples:
  deno run --allow-read detect-genre.ts novel.txt
  deno run --allow-read detect-genre.ts novel.txt --output genre.json
  deno run --allow-read detect-genre.ts novel.txt --sample-size 20
""");

def main():
  args = sys.argv[1:]

  if args.includes("--help") or args.includes("-h") or len(args) == 0:
    printHelp()
    sys.exit(0)

  # Parse arguments
  inputFile = ""
  outputFile = ""
  sampleSize = 10

  skipIndices = new Set<number>()

  for i in range(0, len(args)):
    if (skipIndices.has(i)) continue

    if args[i] == "--output" and args[i + 1]:
      outputFile = args[i + 1]
      skipIndices.add(i + 1)
    elif args[i] == "--sample-size" and args[i + 1]:
      sampleSize = parseInt(args[i + 1], 10) or 10
      skipIndices.add(i + 1)
    elif !args[i].startswith("--") and !inputFile:
      inputFile = args[i]

  if !inputFile:
    print("Error input file provided")
    sys.exit(1)

  # Read input file
  text
  try:
    text = open(inputFile, 'r', encoding='utf-8').read()
  except Exception as e:
    print(f"Error reading file: ${e instanceof Error ? e.message : e}")
    sys.exit(1)

  # Detect genre
  result = detectGenre(text, sampleSize)

  # Output
  jsonOutput = json.dumps(result, None, 2)

  if outputFile:
    open(outputFile, 'w', encoding='utf-8').write(jsonOutput)
    print("Genre detection complete")
    print(f"Primary: ${result.primaryGenre} (${round(result.primaryConfidence * 100)}% confidence)")
    if result.len(secondaryGenres) > 0:
      print(f"Secondary: ${result.secondaryGenres.join(", ")}")
    print(f"Output written to: ${outputFile}")
  else:
    print(jsonOutput)

main()
