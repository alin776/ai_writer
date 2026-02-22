#!/usr/bin/env python3



"""
Emotional Beat Map

Maps emotional peaks and valleys across a work's timeline.
Helps identify the emotional experience the work delivers.

Usage:
  python scripts/emotional-beat-map.py "Work Name" --acts 5
  python scripts/emotional-beat-map.py "Work Name" --episodes 10
  python scripts/emotional-beat-map.py --compare drama,thriller
"""

import sys
import os
import json
import re
import random
from datetime import date


# == INTERFACES ===




# == DATA ===

GENRE_EXPECTATIONS: Record<string, GenreExpectations> = {
  wonder: {
    name: "Wonder",
    expected_peaks: [0.1, 0.5, 0.9],
    expected_emotions: ["awe", "curiosity", "amazement", "discovery"],
    pacing_pattern: "Builds through revelations, peaks at major discoveries",
    key_beats: [
      { position: 0.1, description: "Initial wonder hook - something fascinating" },
      { position: 0.5, description: "Major revelation that reframes understanding" },
      { position: 0.9, description: "Final perspective shift or scale revelation" }
    ]
  },
  mystery: {
    name: "Mystery",
    expected_peaks: [0.25, 0.5, 0.75, 0.95],
    expected_emotions: ["curiosity", "suspicion", "confusion", "satisfaction"],
    pacing_pattern: "Clue distribution with rising tension toward revelation",
    key_beats: [
      { position: 0.1, description: "Crime/mystery established" },
      { position: 0.25, description: "First major clue" },
      { position: 0.5, description: "Major complication or red herring" },
      { position: 0.75, description: "All pieces available (reader could solve)" },
      { position: 0.95, description: "Revelation and explanation" }
    ]
  },
  thriller: {
    name: "Thriller",
    expected_peaks: [0.15, 0.4, 0.6, 0.8, 0.95],
    expected_emotions: ["tension", "fear", "urgency", "relief"],
    pacing_pattern: "Escalating tension with brief relief valleys",
    key_beats: [
      { position: 0.15, description: "Danger established, stakes clear" },
      { position: 0.4, description: "First major setback" },
      { position: 0.6, description: "Point of no return" },
      { position: 0.8, description: "Darkest moment / all seems lost" },
      { position: 0.95, description: "Final confrontation and resolution" }
    ]
  },
  horror: {
    name: "Horror",
    expected_peaks: [0.2, 0.5, 0.7, 0.9],
    expected_emotions: ["unease", "dread", "fear", "terror", "horror"],
    pacing_pattern: "Building dread punctuated by terror spikes",
    key_beats: [
      { position: 0.1, description: "Normality before disruption" },
      { position: 0.2, description: "First sign something is wrong" },
      { position: 0.5, description: "Nature of threat becomes clear" },
      { position: 0.7, description: "Escape attempts fail, vulnerability maximum" },
      { position: 0.9, description: "Final confrontation with horror" }
    ]
  },
  drama: {
    name: "Drama",
    expected_peaks: [0.25, 0.5, 0.75, 0.95],
    expected_emotions: ["sympathy", "tension", "catharsis", "transformation"],
    pacing_pattern: "Internal pressure building to transformation",
    key_beats: [
      { position: 0.1, description: "Character's lie/flaw established" },
      { position: 0.25, description: "Inciting pressure on the lie" },
      { position: 0.5, description: "Midpoint - glimpse of truth or False victory" },
      { position: 0.75, description: "Dark night - lie confronted fully" },
      { position: 0.95, description: "Transformation or tragic fall" }
    ]
  },
  adventure: {
    name: "Adventure",
    expected_peaks: [0.15, 0.35, 0.55, 0.75, 0.95],
    expected_emotions: ["excitement", "danger", "triumph", "wonder"],
    pacing_pattern: "Action peaks with brief recovery valleys",
    key_beats: [
      { position: 0.1, description: "Call to adventure" },
      { position: 0.25, description: "First threshold crossed" },
      { position: 0.5, description: "Major challenge overcome" },
      { position: 0.75, description: "Supreme ordeal" },
      { position: 0.95, description: "Victory and return" }
    ]
  },
  relationship: {
    name: "Relationship",
    expected_peaks: [0.2, 0.5, 0.8, 0.95],
    expected_emotions: ["longing", "connection", "conflict", "resolution"],
    pacing_pattern: "Connection-conflict cycles building to resolution",
    key_beats: [
      { position: 0.15, description: "Meet cute / initial connection" },
      { position: 0.35, description: "Growing intimacy" },
      { position: 0.5, description: "Major obstacle or conflict" },
      { position: 0.75, description: "Dark moment / seeming end" },
      { position: 0.95, description: "Resolution (together or apart)" }
    ]
  },
  humor: {
    name: "Humor",
    expected_peaks: [0.1, 0.3, 0.5, 0.7, 0.9],
    expected_emotions: ["amusement", "surprise", "delight", "release"],
    pacing_pattern: "Regular comedic peaks with escalating absurdity",
    key_beats: [
      { position: 0.1, description: "Comedic premise established" },
      { position: 0.35, description: "Complications compound hilariously" },
      { position: 0.6, description: "Situation reaches absurd extreme" },
      { position: 0.8, description: "Darkest/most awkward moment" },
      { position: 0.95, description: "Resolution with final laugh" }
    ]
  }
};

EMOTION_VOCABULARY = {
  positive: [
    "joy", "triumph", "relief", "hope", "love", "awe", "wonder",
    "satisfaction", "connection", "excitement", "delight", "peace"
  ],
  negative: [
    "fear", "dread", "horror", "grief", "anger", "despair", "tension",
    "anxiety", "disgust", "shame", "loneliness", "betrayal"
  ],
  complex: [
    "bittersweet", "melancholy", "anticipation", "unease", "catharsis",
    "ambivalence", "longing", "resignation", "defiance", "transformation"
  ]
};

# == UTILITIES ===

def createEmptyBeatMap(workName: string, structureType: "acts" | "episodes" | "chapters", unitCount: number): BeatMap {
  return {
    work_name: workName,
    structure_type: structureType,
    unit_count: unitCount,
    primary_genre: "",
    beats: [],
    analysis: {
      peaks: [],
      valleys: [],
      dominant_emotions: [],
      pacing_notes: ""
    }
  };
}

def formatBeatMap(map: BeatMap): string {
  lines: string[] = [];

  lines.append(f"# Emotional Beat Map: {map.work_name}");
  lines.append("");
  lines.append(f"**Structure:** {map.unit_count} {map.structure_type}");
  lines.append(f"**Primary Genre:** {map.primary_genre or \"(not set)\"}");
  lines.append("");

  # Visual timeline
  lines.append("## Timeline");
  lines.append("");
  lines.append("f""f"\");
  lines.append(\"Position  0%   25%   50%   75%   100%\");
  lines.append(\"          |-----|-----|-----|-----|\");

  if (map.beats.length > 0) {
    # Sort beats by position
    sorted = [...map.beats].sort((a, b) => a.position - b.position);
    for beat in sorted) {
      pos = round(beat.position * 100);
      marker = beat.beat_type == \"peak\" ? \"^\" : beat.beat_type == \"valley\" ? \"v\" : \"-\";
      spacer = \" \".repeat(max(0, int(pos / 5)));
      lines.append("${pos.toString().padStart(3)}%${spacer}${marker} ${beat.emotion} (${beat.element})f");
    }
  } else {
    lines.append(\"(No beats mapped yet)\");
  }

  lines.append(\""f""");
  lines.append("");

  # Beat details
  if (map.beats.length > 0) {
    lines.append("## Beat Details");
    lines.append("");
    lines.append("| Position | Type | Emotion | Intensity | Element |");
    lines.append("|----------|------|---------|-----------|---------|");
    for beat in map.beats.sort((a, b) => a.position - b.position)) {
      pos = f"{round(beat.position * 100)}%";
      lines.append(f"| {pos} | {beat.beat_type} | {beat.emotion} | {beat.intensity}/10 | {beat.element} |");
    }
    lines.append("");
  }

  # Analysis
  if (map.analysis.pacing_notes) {
    lines.append("## Analysis");
    lines.append("");
    lines.append(map.analysis.pacing_notes);
    lines.append("");
  }

  return lines.join("\n");
}

def formatGenreComparison(genres: string[]): string {
  lines: string[] = [];

  lines.append("# Genre Emotional Expectations Comparison");
  lines.append("");

  for genre in genres) {
    expectations = GENRE_EXPECTATIONS[genre.lower()];
    if (!expectations) {
      lines.append(f"## {genre}");
      lines.append("(Unknown genre - no expectations defined)");
      lines.append("");
      continue;
    }

    lines.append(f"## {expectations.name}");
    lines.append("");
    lines.append(f"**Pacing Pattern:** {expectations.pacing_pattern}");
    lines.append("");
    lines.append(f"**Expected Emotions:** {expectations.expected_emotions.join(\", \")}");
    lines.append("");
    lines.append("**Key Beats:**");
    for beat in expectations.key_beats) {
      lines.append(f"- {round(beat.position * 100)}%: {beat.description}");
    }
    lines.append("");
  }

  # Side-by-side if multiple genres
  if (genres.length > 1) {
    lines.append("## Comparison Grid");
    lines.append("");
    lines.append("| Position | " + genres.map(g => GENRE_EXPECTATIONS[g.lower()]?.name or g).join(" | ") + " |");
    lines.append("|----------|" + genres.map(() => "---").join("|") + "|");

    positions = [0.1, 0.25, 0.35, 0.5, 0.6, 0.75, 0.8, 0.9, 0.95];
    for pos in positions) {
      cells = genres.map(g => {
        exp = GENRE_EXPECTATIONS[g.lower()];
        if (!exp) return "-";
        beat = exp.key_beats.find(b => Math.abs(b.position - pos) < 0.05);
        return beat ? beat.description.substring(0, 30) : "-";
      });
      lines.append(f"| {round(pos * 100)}% | {cells.join(\" | \")} |");
    }
    lines.append("");
  }

  return lines.join("\n");
}

def formatTemplate(workName: string, structureType: "acts" | "episodes" | "chapters", unitCount: number): string {
  lines: string[] = [];

  lines.append(f"# Emotional Beat Map Template: {workName}");
  lines.append("");
  lines.append(f"Structure: {unitCount} {structureType}");
  lines.append("");
  lines.append("## Instructions");
  lines.append("");
  lines.append("For each significant emotional moment, record:");
  lines.append("- Position (0.0 - 1.0)");
  lines.append("- Emotion (what audience should feel)");
  lines.append("- Intensity (1-10)");
  lines.append("- Element (what causes this emotion)");
  lines.append("- Type: peak (high intensity), valley (low/recovery), sustain, shift");
  lines.append("");

  lines.append("## Emotion Vocabulary");
  lines.append("");
  lines.append("**Positive:** " + EMOTION_VOCABULARY.positive.join(", "));
  lines.append("");
  lines.append("**Negative:** " + EMOTION_VOCABULARY.negative.join(", "));
  lines.append("");
  lines.append("**Complex:** " + EMOTION_VOCABULARY.complex.join(", "));
  lines.append("");

  lines.append("## Beat Recording Template");
  lines.append("");

  # Generate position markers based on structure
  increment = 1 / unitCount;
  for (i = 0; i <= unitCount; i++) {
    pos = i * increment;
    label = structureType == "acts" ? f"Act {i + 1} start" :
                  structureType == "episodes" ? f"Episode {i + 1}" :
                  f"Chapter {i + 1}";
    lines.append(f"### {round(pos * 100)}% - {label}");
    lines.append("");
    lines.append("| Emotion | Intensity | Element | Type |");
    lines.append("|---------|-----------|---------|------|");
    lines.append("|         |           |         |      |");
    lines.append("");
  }

  return lines.join("\n");
}

# == MAIN ===

def main(): void {
  args = sys.argv[1:];

  # Help
  if (args.includes("--help") or args.includes("-h")) {
    print(f"Emotional Beat Map - Timeline Emotional Mapping

Usage:
  deno run --allow-read scripts/emotional-beat-map.ts \"Work Name\" --acts 5
  deno run --allow-read scripts/emotional-beat-map.ts \"Work Name\" --episodes 10
  deno run --allow-read scripts/emotional-beat-map.ts \"Work Name\" --chapters 20
  deno run --allow-read scripts/emotional-beat-map.ts --compare drama,thriller
  deno run --allow-read scripts/emotional-beat-map.ts --genres

Options:
  --acts <n>        Structure as n acts (default for plays)
  --episodes <n>    Structure as n episodes (default for TV)
  --chapters <n>    Structure as n chapters (default for novels)
  --compare <list>  Compare genre expectations (comma-separated)
  --genres          List available genres with expectations
  --json            Output as JSON

Examples:
  # Five-act play template
  deno run --allow-read scripts/emotional-beat-map.ts \"Hamlet\" --acts 5

  # TV season template
  deno run --allow-read scripts/emotional-beat-map.ts \"Killjoys S1\" --episodes 10

  # Compare drama and thriller expectations
  deno run --allow-read scripts/emotional-beat-map.ts --compare drama,thriller
");
    sys.exit(0);
  }

  isJson = args.includes("--json");

  # Handle --genres flag
  if (args.includes("--genres")) {
    genres = list(GENRE_EXPECTATIONS.keys());
    if (isJson) {
      print(json.dumps(GENRE_EXPECTATIONS, None, 2));
    } else {
      print("Available genres with expectations:");
      for genre in genres) {
        exp = GENRE_EXPECTATIONS[genre];
        print(f"  {exp.name}: {exp.pacing_pattern}");
      }
    }
    return;
  }

  # Handle --compare flag
  compareIndex = args.indexOf("--compare");
  if (compareIndex != -1) {
    genreList = args[compareIndex + 1];
    if (!genreList) {
      print("Error: --compare requires comma-separated genre list");
      sys.exit(1);
    }
    genres = genreList.split(",").map(g => g.strip());

    if (isJson) {
      comparison: Record<string, GenreExpectations | None> = {};
      for g in genres) {
        comparison[g] = GENRE_EXPECTATIONS[g.lower()] or None;
      }
      print(json.dumps(comparison, None, 2));
    } else {
      print(formatGenreComparison(genres));
    }
    return;
  }

  # Parse structure flags
  actsIndex = args.indexOf("--acts");
  episodesIndex = args.indexOf("--episodes");
  chaptersIndex = args.indexOf("--chapters");

  structureType: "acts" | "episodes" | "chapters" = "acts";
  unitCount = 5;

  if (actsIndex != -1 and args[actsIndex + 1]) {
    structureType = "acts";
    unitCount = parseInt(args[actsIndex + 1]);
  } else if (episodesIndex != -1 and args[episodesIndex + 1]) {
    structureType = "episodes";
    unitCount = parseInt(args[episodesIndex + 1]);
  } else if (chaptersIndex != -1 and args[chaptersIndex + 1]) {
    structureType = "chapters";
    unitCount = parseInt(args[chaptersIndex + 1]);
  }

  # Find work name (positional argument)
  skipIndices = new Set<number>();
  for idx in [actsIndex, episodesIndex, chaptersIndex, compareIndex]) {
    if (idx != -1) {
      skipIndices.add(idx);
      skipIndices.add(idx + 1);
    }
  }

  workName: string | None = None;
  for (i = 0; i < args.length; i++) {
    if (!args[i].startswith("--") and !skipIndices.has(i)) {
      workName = args[i];
      break;
    }
  }

  if (!workName) {
    print("Error: Please provide a work name");
    print("Usage: deno run --allow-read scripts/emotional-beat-map.ts \"Work Name\" --acts 5");
    sys.exit(1);
  }

  # Generate template
  if (isJson) {
    map = createEmptyBeatMap(workName, structureType, unitCount);
    print(json.dumps(map, None, 2));
  } else {
    print(formatTemplate(workName, structureType, unitCount));
  }
}

main();


if __name__ == '__main__':
    main()
