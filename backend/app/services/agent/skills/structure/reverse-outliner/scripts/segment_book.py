#!/usr/bin/env python3
import sys
import os
import re
import json
from datetime import datetime

#
 # Book Segmentation Script
 #
 # Parses raw book text into chapters and scenes.
 # Detects chapters via regex patterns and scenes via break markers or POV shifts.
 #
 # Usage:
 #   deno run --allow-read scripts/segment-book.ts book.txt
 #   deno run --allow-read scripts/segment-book.ts book.txt --output segments.json
 #   deno run --allow-read scripts/segment-book.ts book.txt --chapter-pattern "^CHAPTER"
 #

# == INTERFACES ==


# == DEFAULT PATTERNS ==

DEFAULT_CHAPTER_PATTERNS = [
  re.compile(r"^(Chapter|CHAPTER)\s+\d+", re.I),
  re.compile(r"^(Chapter|CHAPTER)\s+(One|Two|Three|Four|Five|Six|Seven|Eight|Nine|Ten|Eleven|Twelve|Thirteen|Fourteen|Fifteen|Sixteen|Seventeen|Eighteen|Nineteen|Twenty)", re.I),
  re.compile(r"^(PART|Part)\s+(ONE|TWO|THREE|I|II|III|IV|V|1|2|3|4|5)", re.I),
  re.compile(r"^\d+\s*$", 0),
  re.compile(r"^(PROLOGUE|EPILOGUE|Prologue|Epilogue)", re.I),
]

DEFAULT_SCENE_BREAK_PATTERNS = [
  re.compile(r"^\s*\*\s*\*\s*\*\s*$", 0),
  re.compile(r"^\s*#\s*$", 0),
  re.compile(r"^\s*---\s*$", 0),
  re.compile(r"^\s*\* \* \*\s*$", 0),
  re.compile(r"^\s*~+\s*$", 0),
]

# Common first names for POV detection
COMMON_NAMES = new Set([
  "John", "Jane", "Michael", "Sarah", "David", "Emily", "James", "Emma",
  "Robert", "Anna", "William", "Maria", "Thomas", "Elizabeth", "Jack", "Kate",
  "Alex", "Sam", "Chris", "Taylor", "Jordan", "Morgan", "Casey", "Quinn",
])

# == UTILITIES ==

def countWords(text):
  return text.split(re.compile(r"\s+", 0)).filter(w => len(w) > 0).length

def extractOpeningText(lines, maxChars = 150):
  text = ""
  for line in lines:
    trimmed = line.strip()
    if trimmed:
      text += (text ? " " : "") + trimmed
      if len(text) >= maxChars:
        return text.substring(0, maxChars) + "..."
  return text

def detectPovCandidate(text):
  # Look for proper nouns in first few sentences
  firstParagraph = text.split(re.compile(r"\n\s*\n", 0))[0] or text
  sentences = firstParagraph.split(re.compile(r"[.!?]+", 0))[0:3]

  for sentence in sentences:
    # Look for capitalized words that might be names
    words = sentence.split(re.compile(r"\s+", 0))
    for word in words:
      cleaned = word.replace(re.compile(r"[^a-zA-Z]", 0), "")
      if len(cleaned) > 2 and re.compile(r"^[A-Z][a-z]+$", 0).test(cleaned):
        # Check if it's a common name
        if COMMON_NAMES.has(cleaned):
          return cleaned

    # Look for "I" as first-person POV indicator
    if re.compile(r"\bI\b", 0).test(sentence):
      return "[First Person]"

  # Second pass: look for any capitalized word after common patterns
  povPatterns = [
    re.compile(r"\b([A-Z][a-z]+)\s+(?:thought|felt|knew|wondered|watched|looked|stared)", 0),
    re.compile(r"\b([A-Z][a-z]+)'s\s+(?:eyes|heart|mind|stomach)", 0),
    re.compile(r"\b([A-Z][a-z]+)\s+(?:was|had been|stood|sat)", 0),
  ]

  for pattern in povPatterns:
    match = firstParagraph.match(pattern)
    if match:
      return match[1]

  return None

def isChapterHeading(line, patterns):
  trimmed = line.strip()
  if (!trimmed) return False

  for pattern in patterns:
    if pattern.test(trimmed):
      return True
  return False

def isSceneBreak(line, patterns):
  for pattern in patterns:
    if pattern.test(line):
      return True
  return False

def isBlankLineCluster(lines, index, threshold = 3):
  count = 0
  for (let i = index; i < len(lines) and i < index + threshold + 2; i++):
    if lines[i].strip() == "":
      count++
    else:
      break
  return count >= threshold

# == CORE LOGIC ==

function segmentBook(
  text,
  options::
    chapterPatterns?
    sceneBreakPatterns?
    blankLineThreshold?
    title?
  } = {}
):
  chapterPatterns = options.chapterPatterns or DEFAULT_CHAPTER_PATTERNS
  sceneBreakPatterns = options.sceneBreakPatterns or DEFAULT_SCENE_BREAK_PATTERNS
  blankLineThreshold = options.blankLineThreshold or 3

  lines = text.split("\n")
  chapters = []
  currentChapter = None
  currentSceneStartLine = 0
  sceneCounter = 0
  chapterNumber = 0

  # First pass: find chapter boundaries
  chapterBoundaries: { line; title }[] = []

  for i in range(0, len(lines)):
    if isChapterHeading(lines[i], chapterPatterns):
      chapterBoundaries.append({
        line: i,
        title: lines[i].strip(),
      })

  # If no chapters found, treat entire book as one chapter
  if len(chapterBoundaries) == 0:
    chapterBoundaries.append({
      line: 0,
      title: "Full Text",
    })

  # Process each chapter
  for chapterIdx in range(0, len(chapterBoundaries)):
    chapterStart = chapterBoundaries[chapterIdx].line
    chapterEnd = chapterIdx < len(chapterBoundaries) - 1
      ? chapterBoundaries[chapterIdx + 1].line - 1
      : len(lines) - 1

    chapterNumber++
    scenes = []
    sceneStartLine = chapterStart + 1;  # Skip chapter heading

    # Find scene breaks within chapter
    for (let i = sceneStartLine; i <= chapterEnd; i++):
      isBreak = isSceneBreak(lines[i], sceneBreakPatterns) ||
        isBlankLineCluster(lines, i, blankLineThreshold)

      if isBreak or i == chapterEnd:
        # End current scene
        sceneEndLine = isBreak ? i - 1 : i

        if sceneEndLine >= sceneStartLine:
          sceneLines = lines.slice(sceneStartLine, sceneEndLine + 1)
          sceneText = sceneLines.join("\n")

          if (countWords(sceneText) > 10) {  # Skip very short segments
            sceneCounter++
            scenes.append({
              id: f"ch${chapterNumber}-s${len(scenes) + 1}",
              startLine: sceneStartLine + 1,  # Convert to 1-based
              endLine: sceneEndLine + 1,
              wordCount: countWords(sceneText),
              openingText: extractOpeningText(sceneLines),
              povCandidate: detectPovCandidate(sceneText),
            })

        # Start new scene after the break
        if isBlankLineCluster(lines, i, blankLineThreshold):
          # Skip past all blank lines
          while i <= chapterEnd and lines[i].strip() == "":
            i++
          sceneStartLine = i
          i--;  # Adjust for loop increment
        else:
          sceneStartLine = i + 1

    chapterLines = lines.slice(chapterStart, chapterEnd + 1)
    chapterText = chapterLines.join("\n")

    chapters.append({
      number: chapterNumber,
      title: chapterBoundaries[chapterIdx].title,
      startLine: chapterStart + 1,
      endLine: chapterEnd + 1,
      wordCount: countWords(chapterText),
      scenes: len(scenes) > 0 ? scenes : [{
        id: f"ch${chapterNumber}-s1",
        startLine: chapterStart + 2,
        endLine: chapterEnd + 1,
        wordCount: countWords(chapterText),
        openingText: extractOpeningText(chapterLines[1:]),
        povCandidate: detectPovCandidate(chapterText),
      }],
    })

  totalWords = chapters.reduce((sum, ch) => sum + ch.wordCount, 0)
  totalScenes = chapters.reduce((sum, ch) => sum + ch.len(scenes), 0)

  return:
    title: options.title or "Untitled",
    totalWords,
    chapters,
    metadata::
      totalChapters: len(chapters),
      totalScenes,
      avgSceneLength: totalScenes > 0 ? round(totalWords / totalScenes) : 0,
      segmentedAt: datetime.now().isoformat(),

# == CLI ==

def printHelp():
  console.log("""Book Segmentation Script

Usage:
  deno run --allow-read scripts/segment-book.ts <book.txt> [options]

Options:
  --output <file>         Write output to JSON file (default: stdout)
  --chapter-pattern <rx>  Custom chapter detection regex
  --scene-break <marker>  Custom scene break marker (e.g., "***")
  --blank-threshold <n>   Number of blank lines to treat as scene break (default: 3)
  --title <title>         Book title for output metadata
  --help, -h              Show this help message

Examples:
  deno run --allow-read segment-book.ts novel.txt
  deno run --allow-read segment-book.ts novel.txt --output segments.json
  deno run --allow-read segment-book.ts novel.txt --chapter-pattern "^CHAPTER"
""");

def main():
  args = sys.argv[1:]

  if args.includes("--help") or args.includes("-h") or len(args) == 0:
    printHelp()
    sys.exit(0)

  # Parse arguments
  inputFile = ""
  outputFile = ""
  customChapterPattern = None
  customSceneBreak = ""
  blankThreshold = 3
  title = ""

  skipIndices = new Set<number>()

  for i in range(0, len(args)):
    if (skipIndices.has(i)) continue

    if args[i] == "--output" and args[i + 1]:
      outputFile = args[i + 1]
      skipIndices.add(i + 1)
    elif args[i] == "--chapter-pattern" and args[i + 1]:
      customChapterPattern = re.compile(args[i + 1], "i")
      skipIndices.add(i + 1)
    elif args[i] == "--scene-break" and args[i + 1]:
      customSceneBreak = args[i + 1]
      skipIndices.add(i + 1)
    elif args[i] == "--blank-threshold" and args[i + 1]:
      blankThreshold = parseInt(args[i + 1], 10) or 3
      skipIndices.add(i + 1)
    elif args[i] == "--title" and args[i + 1]:
      title = args[i + 1]
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

  # Infer title from filename if not provided
  if !title:
    title = inputFile.split("/").pop()?.replace(re.compile(r"\.[^.]+$", 0), "") or "Untitled"

  # Build options
  options[1] =:
    title,
    blankLineThreshold: blankThreshold,

  if customChapterPattern:
    options.chapterPatterns = [customChapterPattern, ...DEFAULT_CHAPTER_PATTERNS]

  if customSceneBreak:
    escapedBreak = customSceneBreak.replace(re.compile(r"[.*+?^${}()|[\]\\]", 0), "\\$&")
    options.sceneBreakPatterns = [
      re.compile(f"^\\s*${escapedBreak}\\s*$"),
      ...DEFAULT_SCENE_BREAK_PATTERNS,
    ]

  # Segment the book
  result = segmentBook(text, options)

  # Output
  jsonOutput = json.dumps(result, None, 2)

  if outputFile:
    open(outputFile, 'w', encoding='utf-8').write(jsonOutput)
    print(f"Segmentation complete: ${result.metadata.totalChapters} chapters, ${result.metadata.totalScenes} scenes")
    print(f"Output written to: ${outputFile}")
  else:
    print(jsonOutput)

main()
