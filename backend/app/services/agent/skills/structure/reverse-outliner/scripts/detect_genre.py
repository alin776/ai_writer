#!/usr/bin/env python3
"""
detect_genre.py - Genre Detection Script

Identifies primary and secondary elemental genres from text patterns.
Maps detected genre to Key Moments framework.

Usage:
  python detect_genre.py book.txt
  python detect_genre.py book.txt --output genre.json
"""

import sys
import os
import re
import json
from datetime import datetime

# Ensure UTF-8 output on all platforms
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")
if hasattr(sys.stderr, "reconfigure"):
    sys.stderr.reconfigure(encoding="utf-8")

# == GENRE PATTERNS ==

GENRE_PATTERNS = {
    "wonder": [
        re.compile(r"\b(awe|wonder|amazed|astonished|breathtaking|magnificent|spectacular)\b", re.I),
        re.compile(r"\b(vast|immense|infinite|boundless|cosmic|universe|stars)\b", re.I),
        re.compile(r"\b(discover|revelation|realize|understand|truth|secret)\b", re.I),
        re.compile(r"\b(impossible|unbelievable|unprecedented|never before)\b", re.I),
        re.compile(r"\b(transcend|transform|enlighten|illuminate)\b", re.I),
    ],
    "mystery": [
        re.compile(r"\b(clue|evidence|investigate|detective|suspect|witness)\b", re.I),
        re.compile(r"\b(murder|crime|victim|alibi|motive)\b", re.I),
        re.compile(r"\b(puzzle|riddle|mystery|enigma|secret)\b", re.I),
        re.compile(r"\b(uncover|reveal|discover|deduce|solve)\b", re.I),
        re.compile(r"\b(who|what|why|how)\s+(?:did|was|could|would)\b", re.I),
    ],
    "adventure": [
        re.compile(r"\b(journey|quest|expedition|voyage|trek|travel)\b", re.I),
        re.compile(r"\b(treasure|map|compass|destination|horizon)\b", re.I),
        re.compile(r"\b(danger|peril|risk|hazard|obstacle)\b", re.I),
        re.compile(r"\b(survive|escape|rescue|explore|discover)\b", re.I),
        re.compile(r"\b(supplies|equipment|provisions|camp|wilderness)\b", re.I),
    ],
    "horror": [
        re.compile(r"\b(terror|horror|dread|fear|nightmare|scream)\b", re.I),
        re.compile(r"\b(dark|shadow|darkness|black|sinister)\b", re.I),
        re.compile(r"\b(monster|creature|beast|demon|evil)\b", re.I),
        re.compile(r"\b(dead|death|corpse|grave|blood)\b", re.I),
        re.compile(r"\b(haunted|cursed|possessed|supernatural)\b", re.I),
    ],
    "thriller": [
        re.compile(r"\b(bomb|deadline|countdown|ticking|timer)\b", re.I),
        re.compile(r"\b(chase|pursue|hunt|escape|run)\b", re.I),
        re.compile(r"\b(danger|threat|risk|stakes|life|death)\b", re.I),
        re.compile(r"\b(spy|agent|mission|operation|target)\b", re.I),
        re.compile(r"\b(tension|suspense|urgent|critical|time)\b", re.I),
    ],
    "relationship": [
        re.compile(r"\b(love|heart|feelings|emotion|romance)\b", re.I),
        re.compile(r"\b(kiss|embrace|touch|together|apart)\b", re.I),
        re.compile(r"\b(relationship|connection|bond|trust)\b", re.I),
        re.compile(r"\b(marry|wedding|proposal|date|romantic)\b", re.I),
        re.compile(r"\b(attraction|desire|longing|yearning)\b", re.I),
    ],
    "drama": [
        re.compile(r"\b(choice|decision|dilemma|consequence|regret)\b", re.I),
        re.compile(r"\b(family|father|mother|son|daughter|brother|sister)\b", re.I),
        re.compile(r"\b(guilt|shame|pride|honor|dignity)\b", re.I),
        re.compile(r"\b(sacrifice|forgive|betray|loyalty)\b", re.I),
        re.compile(r"\b(past|memory|secret|truth|lie)\b", re.I),
    ],
    "issue": [
        re.compile(r"\b(justice|injustice|rights|freedom|oppression)\b", re.I),
        re.compile(r"\b(society|system|government|power|authority)\b", re.I),
        re.compile(r"\b(debate|argue|believe|opinion|perspective)\b", re.I),
        re.compile(r"\b(moral|ethical|right|wrong|fair)\b", re.I),
        re.compile(r"\b(change|reform|revolution|protest)\b", re.I),
    ],
    "ensemble": [
        re.compile(r"\b(team|group|crew|squad|party)\b", re.I),
        re.compile(r"\b(together|cooperation|unity|alliance)\b", re.I),
        re.compile(r"\b(leader|member|role|contribution)\b", re.I),
        re.compile(r"\b(trust|loyalty|betrayal|sacrifice)\b", re.I),
        re.compile(r"\b(diverse|different|unique|each)\b", re.I),
    ],
    "humor": [
        re.compile(r"\b(laugh|funny|hilarious|absurd|ridiculous)\b", re.I),
        re.compile(r"\b(joke|comedy|wit|sarcasm|irony)\b", re.I),
        re.compile(r"\b(embarrass|awkward|mishap|disaster)\b", re.I),
        re.compile(r"\b(mock|tease|prank|gag)\b", re.I),
        re.compile(r"\b(silly|goofy|zany|wacky)\b", re.I),
    ],
    "idea": [
        re.compile(r"\b(theory|hypothesis|concept|principle|law)\b", re.I),
        re.compile(r"\b(science|technology|experiment|research)\b", re.I),
        re.compile(r"\b(future|evolution|progress|advancement)\b", re.I),
        re.compile(r"\b(what if|imagine|suppose|consider)\b", re.I),
        re.compile(r"\b(implication|consequence|effect|impact)\b", re.I),
    ],
}

# Key Moments templates by genre
KEY_MOMENTS = {
    "wonder": [
        {"type": "Initial Encounter", "expectedPosition": 0.15, "emotionalExperience": "Surprise and awe", "storyFunction": "Establishes the spectacular"},
        {"type": "Scale Revelation", "expectedPosition": 0.35, "emotionalExperience": "Humbling realization", "storyFunction": "Contextualizes protagonist's place"},
        {"type": "Wonder Escalation", "expectedPosition": 0.60, "emotionalExperience": "Intensification of awe", "storyFunction": "Raises stakes and deepens engagement"},
        {"type": "Perspective Shift", "expectedPosition": 0.75, "emotionalExperience": "Paradigm change", "storyFunction": "Forces reevaluation"},
        {"type": "Transcendent Integration", "expectedPosition": 0.90, "emotionalExperience": "Meaning-making", "storyFunction": "Provides thematic resolution"},
    ],
    "mystery": [
        {"type": "Question Inception", "expectedPosition": 0.10, "emotionalExperience": "Curiosity activation", "storyFunction": "Establishes the puzzle"},
        {"type": "Pattern Recognition", "expectedPosition": 0.35, "emotionalExperience": "Satisfaction of connection", "storyFunction": "Provides momentum"},
        {"type": "False Resolution", "expectedPosition": 0.55, "emotionalExperience": "Surprise from misdirection", "storyFunction": "Creates complexity"},
        {"type": "Progressive Revelation", "expectedPosition": 0.75, "emotionalExperience": "Deepening understanding", "storyFunction": "Builds toward solution"},
        {"type": "Solution Crystallization", "expectedPosition": 0.90, "emotionalExperience": "Illumination and closure", "storyFunction": "Completes emotional journey"},
    ],
    "adventure": [
        {"type": "Threshold Crossing", "expectedPosition": 0.15, "emotionalExperience": "Excitement of departure", "storyFunction": "Transitions to adventure world"},
        {"type": "Capability Test", "expectedPosition": 0.30, "emotionalExperience": "Confidence from competence", "storyFunction": "Establishes abilities"},
        {"type": "Resource Depletion", "expectedPosition": 0.50, "emotionalExperience": "Vulnerability from loss", "storyFunction": "Forces adaptation"},
        {"type": "Ultimate Challenge", "expectedPosition": 0.80, "emotionalExperience": "Fear and determination", "storyFunction": "Tests protagonist's limits"},
        {"type": "Return Transformation", "expectedPosition": 0.95, "emotionalExperience": "Pride and perspective", "storyFunction": "Demonstrates growth"},
    ],
    "horror": [
        {"type": "Wrongness Glimpse", "expectedPosition": 0.10, "emotionalExperience": "Unease from dissonance", "storyFunction": "Establishes threat potential"},
        {"type": "Safety Violation", "expectedPosition": 0.30, "emotionalExperience": "Shock from boundary breach", "storyFunction": "Demonstrates vulnerability"},
        {"type": "Threat Escalation", "expectedPosition": 0.50, "emotionalExperience": "Escalating dread", "storyFunction": "Raises stakes"},
        {"type": "Failed Solution", "expectedPosition": 0.70, "emotionalExperience": "Despair from ineffectuality", "storyFunction": "Deepens hopelessness"},
        {"type": "Confrontation", "expectedPosition": 0.90, "emotionalExperience": "Terror meets courage", "storyFunction": "Provides climactic moment"},
    ],
    "thriller": [
        {"type": "Stakes Establishment", "expectedPosition": 0.15, "emotionalExperience": "Concern for outcome", "storyFunction": "Sets up tension framework"},
        {"type": "Deadline Imposition", "expectedPosition": 0.25, "emotionalExperience": "Anxiety from time pressure", "storyFunction": "Creates urgency"},
        {"type": "Near Miss", "expectedPosition": 0.50, "emotionalExperience": "Relief with lingering tension", "storyFunction": "Maintains engagement"},
        {"type": "Option Elimination", "expectedPosition": 0.75, "emotionalExperience": "Mounting pressure", "storyFunction": "Forces harder choices"},
        {"type": "Decision Under Duress", "expectedPosition": 0.90, "emotionalExperience": "Catharsis through action", "storyFunction": "Provides climactic release"},
    ],
    "relationship": [
        {"type": "Significant Connection", "expectedPosition": 0.10, "emotionalExperience": "Recognition of potential", "storyFunction": "Establishes relationship basis"},
        {"type": "Intimacy Deepening", "expectedPosition": 0.35, "emotionalExperience": "Warmth from vulnerability", "storyFunction": "Develops investment"},
        {"type": "Value Conflict", "expectedPosition": 0.55, "emotionalExperience": "Frustration from differences", "storyFunction": "Creates meaningful obstacles"},
        {"type": "Relationship Crisis", "expectedPosition": 0.75, "emotionalExperience": "Heartbreak or betrayal", "storyFunction": "Tests connection's resilience"},
        {"type": "Reconciliation/Resolution", "expectedPosition": 0.90, "emotionalExperience": "Emotional closure", "storyFunction": "Completes relationship arc"},
    ],
    "drama": [
        {"type": "Internal Conflict Revelation", "expectedPosition": 0.15, "emotionalExperience": "Recognition of contradiction", "storyFunction": "Establishes character struggle"},
        {"type": "External Pressure Point", "expectedPosition": 0.35, "emotionalExperience": "Stress from circumstances", "storyFunction": "Forces character choices"},
        {"type": "Failure Moment", "expectedPosition": 0.55, "emotionalExperience": "Shame from inadequacy", "storyFunction": "Deepens character journey"},
        {"type": "Truth Confrontation", "expectedPosition": 0.75, "emotionalExperience": "Painful self-awareness", "storyFunction": "Catalyzes change"},
        {"type": "Character Evolution", "expectedPosition": 0.90, "emotionalExperience": "Self-actualization", "storyFunction": "Demonstrates growth"},
    ],
    "issue": [
        {"type": "Perspective Challenge", "expectedPosition": 0.15, "emotionalExperience": "Intellectual discomfort", "storyFunction": "Establishes complexity"},
        {"type": "Stake Personalization", "expectedPosition": 0.30, "emotionalExperience": "Emotional investment", "storyFunction": "Makes abstract concrete"},
        {"type": "Complexity Recognition", "expectedPosition": 0.50, "emotionalExperience": "Cognitive expansion", "storyFunction": "Prevents simplistic resolution"},
        {"type": "Position Testing", "expectedPosition": 0.70, "emotionalExperience": "Value examination", "storyFunction": "Forces intellectual honesty"},
        {"type": "Perspective Integration", "expectedPosition": 0.90, "emotionalExperience": "Nuanced understanding", "storyFunction": "Provides thematic resolution"},
    ],
    "ensemble": [
        {"type": "Group Formation", "expectedPosition": 0.15, "emotionalExperience": "Belonging potential", "storyFunction": "Establishes the collective"},
        {"type": "Role Establishment", "expectedPosition": 0.30, "emotionalExperience": "Identity within community", "storyFunction": "Defines character functions"},
        {"type": "Group Fracture", "expectedPosition": 0.55, "emotionalExperience": "Loyalty testing", "storyFunction": "Creates internal conflict"},
        {"type": "Collective Challenge", "expectedPosition": 0.75, "emotionalExperience": "Shared adversity", "storyFunction": "Forces cooperation"},
        {"type": "Synergy Moment", "expectedPosition": 0.90, "emotionalExperience": "Strength through unity", "storyFunction": "Demonstrates group value"},
    ],
    "humor": [
        {"type": "Setup Establishment", "expectedPosition": 0.10, "emotionalExperience": "Anticipation", "storyFunction": "Creates comedic potential"},
        {"type": "Incongruity Introduction", "expectedPosition": 0.25, "emotionalExperience": "Surprise amusement", "storyFunction": "Establishes comedic logic"},
        {"type": "Escalation Sequence", "expectedPosition": 0.50, "emotionalExperience": "Mounting absurdity", "storyFunction": "Builds comedic momentum"},
        {"type": "Subversion Peak", "expectedPosition": 0.75, "emotionalExperience": "Maximum comedic release", "storyFunction": "Delivers primary payoff"},
        {"type": "Resolution Callback", "expectedPosition": 0.90, "emotionalExperience": "Satisfying closure", "storyFunction": "Ties comedic threads"},
    ],
    "idea": [
        {"type": "Concept Introduction", "expectedPosition": 0.10, "emotionalExperience": "Intellectual curiosity", "storyFunction": "Establishes central idea"},
        {"type": "Implication Exploration", "expectedPosition": 0.30, "emotionalExperience": "Fascination with consequences", "storyFunction": "Expands idea's scope"},
        {"type": "Edge Case Discovery", "expectedPosition": 0.50, "emotionalExperience": "Surprise from complexity", "storyFunction": "Deepens understanding"},
        {"type": "Idea Testing", "expectedPosition": 0.70, "emotionalExperience": "Tension from stakes", "storyFunction": "Makes abstract personal"},
        {"type": "Synthesis Resolution", "expectedPosition": 0.90, "emotionalExperience": "Intellectual satisfaction", "storyFunction": "Completes thought experiment"},
    ],
}

# == UTILITIES ==


def count_pattern_matches(text, patterns):
    indicators = []
    total_count = 0

    for pattern in patterns:
        matches = pattern.findall(text)
        if matches:
            total_count += len(matches)
            indicators.extend(matches[:3])

    return {
        "count": total_count,
        "indicators": list(dict.fromkeys(indicators))[:10],
    }


def sample_text(text, sample_size=10):
    paragraphs = [p for p in re.split(r"\n\s*\n", text) if len(p.strip()) > 100]

    if len(paragraphs) <= sample_size:
        return paragraphs

    # Sample from beginning, middle, and end
    samples = []
    third_size = sample_size // 3

    # Beginning
    for i in range(min(third_size, len(paragraphs))):
        samples.append(paragraphs[i])

    # Middle
    middle_start = len(paragraphs) // 2 - third_size // 2
    for i in range(middle_start, min(middle_start + third_size, len(paragraphs))):
        if paragraphs[i] not in samples:
            samples.append(paragraphs[i])

    # End
    end_start = len(paragraphs) - third_size
    for i in range(max(0, end_start), len(paragraphs)):
        if paragraphs[i] not in samples:
            samples.append(paragraphs[i])

    return samples


# == CORE LOGIC ==

def detect_genre(text, sample_size=10):
    # Sample text to analyze
    samples = sample_text(text, sample_size)
    sampled_text = "\n\n".join(samples)

    # Count matches for each genre
    evidence = {}
    scores = []

    for genre, patterns in GENRE_PATTERNS.items():
        result = count_pattern_matches(sampled_text, patterns)
        evidence[genre] = {
            "count": result["count"],
            "indicators": result["indicators"],
        }
        scores.append({"genre": genre, "score": result["count"]})

    # Sort by score
    scores.sort(key=lambda s: s["score"], reverse=True)

    # Calculate confidence based on how much higher primary is than others
    total_score = sum(s["score"] for s in scores) or 1
    primary_score = scores[0]["score"] if scores else 0
    primary_confidence = min(1, (primary_score / total_score) + (0.2 if primary_score > 10 else 0))

    # Get secondary genres (those with > 30% of primary's score)
    secondary_genres = [
        s["genre"] for s in scores[1:4]
        if s["score"] > primary_score * 0.3
    ]

    # Get Key Moments for primary genre
    primary_genre = scores[0]["genre"] if scores else "drama"
    key_moment_templates = KEY_MOMENTS.get(primary_genre, KEY_MOMENTS["drama"])

    expected_key_moments = []
    for km in key_moment_templates:
        moment = dict(km)
        moment["foundAt"] = None
        moment["foundScene"] = None
        expected_key_moments.append(moment)

    return {
        "primaryGenre": primary_genre,
        "primaryConfidence": round(primary_confidence * 100) / 100,
        "secondaryGenres": secondary_genres,
        "evidence": evidence,
        "keyMomentsFramework": primary_genre,
        "expectedKeyMoments": expected_key_moments,
        "detectedAt": datetime.now().isoformat(),
    }


# == CLI ==

def print_help():
    print("""Genre Detection Script

Usage:
  python detect_genre.py <book.txt> [options]

Options:
  --output <file>       Write output to JSON file (default: stdout)
  --sample-size <n>     Number of text samples to analyze (default: 10)
  --help, -h            Show this help message

Examples:
  python detect_genre.py novel.txt
  python detect_genre.py novel.txt --output genre.json
  python detect_genre.py novel.txt --sample-size 20
""")


def main():
    args = sys.argv[1:]

    if "--help" in args or "-h" in args or len(args) == 0:
        print_help()
        sys.exit(0)

    # Parse arguments
    input_file = ""
    output_file = ""
    sample_size = 10

    skip_indices = set()

    for i in range(len(args)):
        if i in skip_indices:
            continue

        if args[i] == "--output" and i + 1 < len(args):
            output_file = args[i + 1]
            skip_indices.add(i + 1)
        elif args[i] == "--sample-size" and i + 1 < len(args):
            try:
                sample_size = int(args[i + 1])
            except ValueError:
                sample_size = 10
            skip_indices.add(i + 1)
        elif not args[i].startswith("--") and not input_file:
            input_file = args[i]

    if not input_file:
        print("Error: no input file provided", file=sys.stderr)
        sys.exit(1)

    # Read input file
    try:
        text = open(input_file, "r", encoding="utf-8").read()
    except Exception as e:
        print(f"Error reading file: {e}", file=sys.stderr)
        sys.exit(1)

    # Detect genre
    result = detect_genre(text, sample_size)

    # Output
    json_output = json.dumps(result, indent=2, ensure_ascii=False)

    if output_file:
        with open(output_file, "w", encoding="utf-8") as f:
            f.write(json_output)
        print("Genre detection complete")
        print(f"Primary: {result['primaryGenre']} ({round(result['primaryConfidence'] * 100)}% confidence)")
        if len(result["secondaryGenres"]) > 0:
            print(f"Secondary: {', '.join(result['secondaryGenres'])}")
        print(f"Output written to: {output_file}")
    else:
        print(json_output)


if __name__ == "__main__":
    main()
