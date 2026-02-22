#!/usr/bin/env python3
import sys
import os
import re
import json
from datetime import datetime

#
 # Outline Generation Script
 #
 # Synthesizes all analysis JSON files into a structured markdown outline.
 #
 # Usage:
 #   deno run --allow-read --allow-write scripts/generate-outline.ts [options]
 #

# == INTERFACES ==

# From segment-book.ts


# From analyze-scene-batch.ts


# From detect-genre.ts


# From track-characters.ts


# == UTILITIES ==

def formatConfidence(confidence):
  pct = round(confidence * 100)
  if (pct >= 70) return f"${pct}% (high)"
  if (pct >= 40) return f"${pct}% (medium)"
  return f"${pct}% (low)"

def formatPacing(pacing):
  switch (pacing):
    case "action-heavy":
      return "Action-heavy (more scene than sequel)"
    case "reflective":
      return "Reflective (more sequel than scene)"
    default:
      return "Balanced"

# == GENERATION ==

function generateOutline(
  segments,
  scenes,
  genre,
  characters,
  depth: "summary" | "standard" | "detailed" = "standard"
):
  lines = []
  today = datetime.now().isoformat().split("T")[0]

  # == HEADER ==
  lines.append(f"# Reverse Outline: ${segments.title}")
  lines.append("")
  lines.append(f"**Generated:** ${today}")
  lines.append(f"**Analysis Depth:** ${depth}")
  lines.append("")
  lines.append("---")
  lines.append("")

  # == OVERVIEW ==
  lines.append("## Overview")
  lines.append("")
  lines.append(f"**Genre:** ${genre.primaryGenre} (${round(genre.primaryConfidence * 100)}% confidence)")
  if genre.len(secondaryGenres) > 0:
    lines.append(f"**Secondary Genres:** ${genre.secondaryGenres.join(", ")}")
  lines.append(f"**Total Words:** ${segments.totalWords}")
  lines.append(f"**Chapters:** ${segments.metadata.totalChapters}")
  lines.append(f"**Scenes:** ${segments.metadata.totalScenes}")
  lines.append(f"**Avg Scene Length:** ${segments.metadata.avgSceneLength} words")
  lines.append("")

  # Pacing distribution
  pacing = scenes.summary.pacingDistribution
  lines.append("**Pacing Distribution:**")
  lines.append(f"- Action-heavy scenes: ${pacing.actionHeavy} (${round(pacing.actionHeavy / scenes.summary.totalScenes * 100)}%)")
  lines.append(f"- Balanced scenes: ${pacing.balanced} (${round(pacing.balanced / scenes.summary.totalScenes * 100)}%)")
  lines.append(f"- Reflective scenes: ${pacing.reflective} (${round(pacing.reflective / scenes.summary.totalScenes * 100)}%)")
  lines.append("")

  # == KEY MOMENTS MAP ==
  lines.append("## Key Moments Map")
  lines.append("")
  lines.append(f"Framework: ${genre.keyMomentsFramework}")
  lines.append("")
  lines.append("| Key Moment | Expected Position | Emotional Experience | Story Function |")
  lines.append("|------------|-------------------|---------------------|----------------|")

  for km in genre.expectedKeyMoments:
    expectedPct = round(km.expectedPosition * 100)
    lines.append(f"| ${km.type} | ${expectedPct}% | ${km.emotionalExperience} | ${km.storyFunction} |")
  lines.append("")

  # == CHARACTER ARCS ==
  lines.append("## Character Arcs")
  lines.append("")

  if characters.protagonist:
    p = characters.protagonist
    lines.append(f"### Protagonist: ${p.name}")
    lines.append("")
    lines.append(f"**Arc Type:** ${p.arcType}")
    lines.append(f"**POV Scenes:** ${p.povScenes}")
    lines.append(f"**First Appearance:** ${p.firstAppearance}")
    lines.append("")

    if p.arcComponents.lie:
      lines.append(f"**Lie:** ${p.arcComponents.lie}")
    if p.arcComponents.want:
      lines.append(f"**Want:** ${p.arcComponents.want}")
    if p.arcComponents.need:
      lines.append(f"**Need:** ${p.arcComponents.need}")
    if p.arcComponents.ghost:
      lines.append(f"**Ghost/Backstory:** ${p.arcComponents.ghost}")
    if p.arcComponents.truthAcceptance:
      lines.append(f"**Truth Acceptance:** ${p.arcComponents.truthAcceptance}")
    if p.arcComponents.transformation:
      lines.append(f"**Transformation:** ${p.arcComponents.transformation}")

    if p.len(keyScenes) > 0:
      lines.append(f"**Key Scenes:** ${p.keyScenes.join(", ")}")
    lines.append("")

  if characters.len(secondaryCharacters) > 0:
    lines.append("### Secondary Characters")
    lines.append("")

    for c in characters.secondaryCharacters:
      lines.append(f"#### ${c.name}")
      lines.append(f"- **Role:** ${c.role}")
      lines.append(f"- **Arc Type:** ${c.arcType}")
      lines.append(f"- **POV Scenes:** ${c.povScenes}")
      if c.len(keyScenes) > 0:
        lines.append(f"- **Key Scenes:** ${c.keyScenes.join(", ")}")
      lines.append("")

  lines.append("---")
  lines.append("")

  # == CHAPTER-BY-CHAPTER BREAKDOWN ==
  lines.append("## Chapter-by-Chapter Breakdown")
  lines.append("")

  # Build scene lookup
  sceneMap = new Map<string, SceneAnalysis>()
  for scene in scenes.scenes:
    sceneMap.set(scene.id, scene)

  for chapter in segments.chapters:
    lines.append(f"### Chapter ${chapter.number}: ${chapter.title}")
    lines.append("")
    lines.append(f"**Word Count:** ${chapter.wordCount}")
    lines.append(f"**Scenes:** ${chapter.len(scenes)}")
    lines.append("")

    for segScene in chapter.scenes:
      analysis = sceneMap.get(segScene.id)

      lines.append(f"#### Scene ${segScene.id} | POV: ${segScene.povCandidate or "Unknown"}")
      lines.append("")

      if analysis:
        lines.append(f"**Function:** ${analysis.function}")
        lines.append("")

        if depth == "detailed" or depth == "standard":
          lines.append("| Element | Analysis |")
          lines.append("|---------|----------|")
          lines.append(f"| Goal | ${analysis.structure.goal.detected ? analysis.structure.goal.summary : "Not detected"} |")
          lines.append(f"| Conflict | ${analysis.structure.conflict.detected ? analysis.structure.conflict.summary : "Not detected"} |")
          lines.append("| Disaster | ${analysis.structure.disaster.detected ? "${analysis.structure.disaster.type}: ${analysis.structure.disaster.summary}" : "Not detected"} |")

          sequelParts = []
          if (analysis.sequelElements.reaction) sequelParts.append("Reaction")
          if (analysis.sequelElements.dilemma) sequelParts.append("Dilemma")
          if (analysis.sequelElements.decision) sequelParts.append("Decision")
          lines.append(f"| Sequel | ${len(sequelParts) > 0 ? sequelParts.join(", ") : "None detected"} |")
          lines.append("")

        lines.append(f"**Pacing:** ${formatPacing(analysis.pacing)}")
        lines.append(f"**Words:** ${analysis.wordCount}")

        if depth == "detailed" and analysis.len(issues) > 0:
          lines.append("")
          lines.append("**Issues:**")
          for issue in analysis.issues:
            lines.append(f"- ${issue}")
      else:
        lines.append(f"**Opening:** ${segScene.openingText}")
        lines.append(f"**Words:** ${segScene.wordCount}")

      lines.append("")
      lines.append("---")
      lines.append("")

  # == APPENDIX A INDEX BY FUNCTION ==
  lines.append("## Appendix A Index by Function")
  lines.append("")

  # Group scenes by structural function
  functionGroups = new Map<string, string[]>()
  for scene in scenes.scenes:
    funcKey = scene.function.split(" - ")[0];  # Get main function
    if !functionGroups.has(funcKey):
      functionGroups.set(funcKey, [])
    functionGroups.get(funcKey)!.append(scene.id)

  lines.append("| Function | Scenes |")
  lines.append("|----------|--------|")

  functionOrder = [
    "Opening scene",
    "Setup",
    "Inciting incident",
    "First plot point",
    "Rising action",
    "Midpoint",
    "Complications",
    "Dark night",
    "Climax",
    "Resolution",
  ]

  for func in functionOrder:
    matching = Array.from(functionGroups.entries())
      .filter(([key]) => key.lower().includes(func.lower()))
    for (const [key, sceneIds] of matching):
      lines.append(f"| ${key} | ${sceneIds.join(", ")} |")

  # Add any functions not in the standard order
  for (const [func, sceneIds] of functionGroups.entries()):
    isStandard = functionOrder.some(f => func.lower().includes(f.lower()))
    if !isStandard:
      lines.append(f"| ${func} | ${sceneIds.join(", ")} |")
  lines.append("")

  # == APPENDIX B SCENE TRACKER ==
  lines.append("## Appendix B Scene Tracker")
  lines.append("")
  lines.append("| Character | POV Scenes | Arc Type | Key Scenes |")
  lines.append("|-----------|------------|----------|------------|")

  if characters.protagonist:
    p = characters.protagonist
    lines.append(f"| **${p.name}** (protagonist) | ${p.povScenes} | ${p.arcType} | ${p.keyScenes[0:5].join(", ")} |")

  for c in characters.secondaryCharacters:
    lines.append(f"| ${c.name} | ${c.povScenes} | ${c.arcType} | ${c.keyScenes[0:3].join(", ")} |")
  lines.append("")

  # == APPENDIX C ANALYSIS ==
  if depth == "detailed":
    lines.append("## Appendix C Analysis")
    lines.append("")
    lines.append("Scene-by-scene pacing showing scene/sequel ratio:")
    lines.append("")

    for scene in scenes.scenes:
      bar = "=".repeat(round(scene.sceneSequelRatio * 20))
      space = " ".repeat(20 - len(bar))
      lines.append(f"${scene.id}: [${bar}${space}] ${round(scene.sceneSequelRatio * 100)}% scene")
    lines.append("")

  # == FOOTER ==
  lines.append("---")
  lines.append("")
  lines.append("*Generated by reverse-outliner skill*")

  return lines.join("\n")

# == CLI ==

def printHelp():
  console.log("""Outline Generation Script

Usage:
  deno run --allow-read --allow-write scripts/generate-outline.ts [options]

Required Options:
  --segments <file>    Segments JSON from segment-book.ts
  --scenes <file>      Scene analysis JSON from analyze-scene-batch.ts
  --genre <file>       Genre detection JSON from detect-genre.ts
  --characters <file>  Character tracking JSON from track-characters.ts

Other Options:
  --output <file>      Output markdown file (default: stdout)
  --depth <level>      Output depth: summary, standard, detailed (default: standard)
  --help, -h           Show this help message

Examples:
  deno run --allow-read --allow-write generate-outline.ts \\
    --segments analysis/segments.json \\
    --scenes analysis/scenes.json \\
    --genre analysis/genre.json \\
    --characters analysis/characters.json \\
    --output outline.md
""");

def main():
  args = sys.argv[1:]

  if args.includes("--help") or args.includes("-h"):
    printHelp()
    sys.exit(0)

  # Parse arguments
  segmentsFile = ""
  scenesFile = ""
  genreFile = ""
  charactersFile = ""
  outputFile = ""
  depth: "summary" | "standard" | "detailed" = "standard"

  skipIndices = new Set<number>()

  for i in range(0, len(args)):
    if (skipIndices.has(i)) continue

    if args[i] == "--segments" and args[i + 1]:
      segmentsFile = args[i + 1]
      skipIndices.add(i + 1)
    elif args[i] == "--scenes" and args[i + 1]:
      scenesFile = args[i + 1]
      skipIndices.add(i + 1)
    elif args[i] == "--genre" and args[i + 1]:
      genreFile = args[i + 1]
      skipIndices.add(i + 1)
    elif args[i] == "--characters" and args[i + 1]:
      charactersFile = args[i + 1]
      skipIndices.add(i + 1)
    elif args[i] == "--output" and args[i + 1]:
      outputFile = args[i + 1]
      skipIndices.add(i + 1)
    elif args[i] == "--depth" and args[i + 1]:
      d = args[i + 1]
      if d == "summary" or d == "standard" or d == "detailed":
        depth = d
      skipIndices.add(i + 1)

  # Validate required files
  if !segmentsFile or !scenesFile or !genreFile or !charactersFile:
    print("Error four input files are required (--segments, --scenes, --genre, --characters)")
    printHelp()
    sys.exit(1)

  # Read all input files
  segments
  scenes
  genre
  characters

  try:
    segments = json.loads(open(segmentsFile, 'r', encoding='utf-8').read())
    scenes = json.loads(open(scenesFile, 'r', encoding='utf-8').read())
    genre = json.loads(open(genreFile, 'r', encoding='utf-8').read())
    characters = json.loads(open(charactersFile, 'r', encoding='utf-8').read())
  except Exception as e:
    print(f"Error reading input files: ${e instanceof Error ? e.message : e}")
    sys.exit(1)

  # Generate outline
  outline = generateOutline(segments, scenes, genre, characters, depth)

  # Output
  if outputFile:
    open(outputFile, 'w', encoding='utf-8').write(outline)
    print(f"Outline generated: ${outputFile}")
    print(f"Title: ${segments.title}")
    print(f"Depth: ${depth}")
  else:
    print(outline)

main()
