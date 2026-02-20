#!/usr/bin/env python3



"""
representation-map.py - Map and analyze character representation

Analyzes character data to identify:
- Identity distribution
- Agency/centrality patterns
- Potential trope risks
- Diversity within identity groups

Usage:
  deno run --allow-read representation-map.py characters.json
  deno run --allow-read representation-map.py --interactive

Character JSON format:
[
  {
    "name": "Character Name",
    "role": "protagonist|antagonist|supporting|minor",
    "identities": {
      "race": "...",
      "gender": "...",
      "sexuality": "...",
      "disability": "...",
      "other": ["..."]
    },
    "agency": "high|medium|low",
    "arc": "positive|negative|flat|none",
    "survives": True|false,
    "notes": "..."
  }
]
"""

import sys
import os
import json
import re
import random
from datetime import date





MARGINALIZED_IDENTITIES = {
  race: ['black', 'asian', 'latino', 'latina', 'latinx', 'indigenous', 'native', 'middle eastern', 'south asian', 'pacific islander', 'mixed', 'biracial', 'multiracial'],
  gender: ['woman', 'female', 'trans', 'transgender', 'non-binary', 'nonbinary', 'genderqueer', 'agender', 'genderfluid'],
  sexuality: ['gay', 'lesbian', 'bisexual', 'pansexual', 'queer', 'asexual', 'ace'],
  disability: ['disabled', 'blind', 'deaf', 'wheelchair', 'chronic', 'neurodivergent', 'autistic', 'adhd'],
  mentalHealth: ['depression', 'anxiety', 'ptsd', 'bipolar', 'schizophrenia', 'ocd', 'eating disorder'],
};

def isMarginalized(category: string, value: string): boolean {
  categoryList = MARGINALIZED_IDENTITIES[category as keyof typeof MARGINALIZED_IDENTITIES];
  if (!categoryList) return False;
  lowerValue = value.lower();
  return categoryList.some(term => lowerValue.includes(term));
}

def analyzeCharacters(characters: Character[]): AnalysisResult {
  result: AnalysisResult = {
    characterCount: characters.length,
    roleDistribution: {},
    identityDistribution: {},
    agencyAnalysis: { byIdentity: {}, concerns: [] },
    survivalAnalysis: { byIdentity: {}, concerns: [] },
    tropeRisks: [],
    diversityNotes: [],
  };

  # Role distribution
  for char in characters) {
    result.roleDistribution[char.role] = (result.roleDistribution[char.role] or 0) + 1;
  }

  # Identity distribution
  identityCategories = ['race', 'gender', 'sexuality', 'disability', 'mentalHealth', 'religion'];
  for category in identityCategories) {
    result.identityDistribution[category] = {};
  }

  for char in characters) {
    for category in identityCategories) {
      value = char.identities[category as keyof CharacterIdentities];
      if (value and typeof value == 'string') {
        result.identityDistribution[category][value] =
          (result.identityDistribution[category][value] or 0) + 1;
      }
    }
  }

  # Agency analysis by identity
  for char in characters) {
    for ([category, value] of Object.entries(char.identities)) {
      if (value and typeof value == 'string') {
        key = f"{category}:{value}";
        if (!result.agencyAnalysis.byIdentity[key]) {
          result.agencyAnalysis.byIdentity[key] = { high: 0, medium: 0, low: 0 };
        }
        result.agencyAnalysis.byIdentity[key][char.agency]++;
      }
    }
  }

  # Agency concerns
  for ([identity, counts] of Object.entries(result.agencyAnalysis.byIdentity)) {
    total = counts.high + counts.medium + counts.low;
    if (total >= 2) {
      lowPercentage = (counts.low / total) * 100;
      if (lowPercentage > 50) {
        [category, value] = identity.split(':');
        if (isMarginalized(category, value)) {
          result.agencyAnalysis.concerns.append(
            f"{identity}: {lowPercentage.toFixed(0)}% low agency ({counts.low}/{total} characters)"
          );
        }
      }
    }
  }

  # Survival analysis
  for char in characters) {
    for ([category, value] of Object.entries(char.identities)) {
      if (value and typeof value == 'string') {
        key = f"{category}:{value}";
        if (!result.survivalAnalysis.byIdentity[key]) {
          result.survivalAnalysis.byIdentity[key] = { survives: 0, dies: 0 };
        }
        if (char.survives) {
          result.survivalAnalysis.byIdentity[key].survives++;
        } else {
          result.survivalAnalysis.byIdentity[key].dies++;
        }
      }
    }
  }

  # Survival concerns
  for ([identity, counts] of Object.entries(result.survivalAnalysis.byIdentity)) {
    total = counts.survives + counts.dies;
    if (counts.dies > 0) {
      deathPercentage = (counts.dies / total) * 100;
      [category, value] = identity.split(':');
      if (isMarginalized(category, value)) {
        if (deathPercentage > 50 or (category == 'sexuality' and counts.dies > 0)) {
          result.survivalAnalysis.concerns.append(
            f"{identity}: {counts.dies}/{total} characters die ({deathPercentage.toFixed(0)}%)"
          );
        }
      }
    }
  }

  # Trope risk detection
  lgbtqChars = characters.filter(c =>
    isMarginalized('sexuality', c.identities.sexuality or '') ||
    (c.identities.gender and isMarginalized('gender', c.identities.gender) and c.identities.gender.lower().includes('trans'))
  );
  lgbtqDeaths = lgbtqChars.filter(c => !c.survives);
  if (lgbtqDeaths.length > 0) {
    result.tropeRisks.append(
      f"BURY YOUR GAYS RISK: {lgbtqDeaths.length} LGBTQ+ character(s) die: {lgbtqDeaths.map(c => c.name).join(', ')}"
    );
  }

  # Magical minority detection
  marginalizedSupportingWithHighAgency = characters.filter(c =>
    c.role == 'supporting' &&
    c.agency == 'high' &&
    Object.entries(c.identities).some(([cat, val]) =>
      val and typeof val == 'string' and isMarginalized(cat, val)
    )
  );
  protagonists = characters.filter(c => c.role == 'protagonist');
  defaultProtagonists = protagonists.filter(c =>
    !Object.entries(c.identities).some(([cat, val]) =>
      val and typeof val == 'string' and isMarginalized(cat, val)
    )
  );

  if (marginalizedSupportingWithHighAgency.length > 0 and defaultProtagonists.length > 0) {
    result.tropeRisks.append(
      f"MAGICAL MINORITY RISK: Marginalized supporting characters with high agency serving default protagonist(s). Check: {marginalizedSupportingWithHighAgency.map(c => c.name).join(', ')}"
    );
  }

  # Mental health + antagonist
  mentalHealthAntagonists = characters.filter(c =>
    c.role == 'antagonist' and c.identities.mentalHealth
  );
  if (mentalHealthAntagonists.length > 0) {
    result.tropeRisks.append(
      f"MENTAL ILLNESS = VILLAIN RISK: Antagonist(s) with mental health conditions: ${mentalHealthAntagonists.map(c => "${c.name} (${c.identities.mentalHealth})f").join(', ')}"
    );
  }

  # Diversity notes
  identityCounts: Record<string, number> = {};
  for char in characters) {
    for ([category, value] of Object.entries(char.identities)) {
      if (value and typeof value == 'string') {
        key = f"{category}:{value}";
        identityCounts[key] = (identityCounts[key] or 0) + 1;
      }
    }
  }

  for ([identity, count] of identityCounts.items()) {
    if (count == 1) {
      [category, value] = identity.split(':');
      if (isMarginalized(category, value)) {
        result.diversityNotes.append(
          f"Only one {value} character - consider if tokenism risk"
        );
      }
    }
  }

  return result;
}

def formatReport(result: AnalysisResult): string {
  report = f"
REPRESENTATION MAP
==================

Characters analyzed: {result.characterCount}

ROLE DISTRIBUTION
";
  for ([role, count] of Object.entries(result.roleDistribution)) {
    report += f"  {role}: {count}\n";
  }

  report += f"
IDENTITY DISTRIBUTION
";
  for ([category, values] of Object.entries(result.identityDistribution)) {
    if (list(values.keys()).length > 0) {
      report += f"\n  {category}:\n";
      for ([value, count] of values.items()) {
        report += f"    {value}: {count}\n";
      }
    }
  }

  if (result.agencyAnalysis.concerns.length > 0) {
    report += f"
AGENCY CONCERNS
";
    for concern in result.agencyAnalysis.concerns) {
      report += f"  ! {concern}\n";
    }
  }

  if (result.survivalAnalysis.concerns.length > 0) {
    report += f"
SURVIVAL CONCERNS
";
    for concern in result.survivalAnalysis.concerns) {
      report += f"  ! {concern}\n";
    }
  }

  if (result.tropeRisks.length > 0) {
    report += f"
TROPE RISKS
";
    for risk in result.tropeRisks) {
      report += f"  !! {risk}\n";
    }
  }

  if (result.diversityNotes.length > 0) {
    report += f"
DIVERSITY NOTES
";
    for note in result.diversityNotes) {
      report += f"  * {note}\n";
    }
  }

  report += f"
RECOMMENDATIONS

1. Review any flagged trope risks carefully
2. Consider agency distribution across identities
3. If only one character of an identity, consider tokenism
4. Ensure marginalized characters have their own stories/arcs
5. Engage sensitivity readers for identities represented

This analysis is based on data provided and cannot assess:
  - Quality of representation within the narrative
  - Stereotyping through characterization
  - Authentic voice and experience
  - Reception by affected communities
";

  return report;
}

def showExampleFormat(): string {
  return f"
CHARACTER JSON FORMAT
=====================

Create a JSON file with this structure:

[
  {
    \"name\": \"Maya Chen\",
    \"role\": \"protagonist\",
    \"identities\": {
      \"race\": \"Chinese-American\",
      \"gender\": \"woman\",
      \"sexuality\": \"bisexual\",
      \"disability\": None,
      \"mentalHealth\": None,
      \"religion\": None
    },
    \"agency\": \"high\",
    \"arc\": \"positive\",
    \"survives\": True,
    \"notes\": \"Main character, drives the plot\"
  },
  {
    \"name\": \"James Wright\",
    \"role\": \"supporting\",
    \"identities\": {
      \"race\": \"white\",
      \"gender\": \"man\",
      \"sexuality\": \"straight\"
    },
    \"agency\": \"medium\",
    \"arc\": \"flat\",
    \"survives\": True
  },
  {
    \"name\": \"Dr. Amara Okonkwo\",
    \"role\": \"supporting\",
    \"identities\": {
      \"race\": \"Nigerian\",
      \"gender\": \"woman\",
      \"sexuality\": \"lesbian\"
    },
    \"agency\": \"high\",
    \"arc\": \"positive\",
    \"survives\": False,
    \"notes\": \"Dies in chapter 15\"
  }
]

FIELDS:
  name: Character name
  role: protagonist | antagonist | supporting | minor
  identities: Object with identity categories
    - race: ethnic/racial identity
    - gender: gender identity
    - sexuality: sexual orientation
    - disability: any disability
    - mentalHealth: any mental health condition
    - religion: religious identity
    - class: socioeconomic class
  agency: high | medium | low (how much they drive events)
  arc: positive | negative | flat | none
  survives: True | False (do they survive the story?)
  notes: optional additional context
";
}

def showUsage(): void {
  print(f"
Representation Map Tool
=======================

Analyzes character data to identify representation patterns.

Usage:
  deno run --allow-read representation-map.ts <characters.json>
  deno run --allow-read representation-map.ts --format

Options:
  --format    Show the expected JSON format for character data

Detects:
  - Identity distribution across characters
  - Agency imbalances by identity
  - Survival disparities (Bury Your Gays, etc.)
  - Trope risks (Magical Minority, etc.)
  - Tokenism indicators

See --format for character JSON structure.
");
}

async function main() {
  args = sys.argv[1:];

  if (args.includes('--format')) {
    print(showExampleFormat());
    sys.exit(0);
  }

  if (args.length == 0 or args[0].startswith('--')) {
    showUsage();
    sys.exit(0);
  }

  filename = args[0];
  try {
    text = open(filename, "r", encoding="utf-8").read();
    characters: Character[] = json.loads(text);

    if (!Array.isArray(characters)) {
      print('Error: JSON must be an array of character objects');
      sys.exit(1);
    }

    result = analyzeCharacters(characters);
    print(formatReport(result));
  } catch (e) {
    if (e instanceof SyntaxError) {
      print('Error: Invalid JSON format');
      print(e.message);
    } else {
      print(f"Error reading file: {filename}");
      print(e);
    }
    sys.exit(1);
  }
}

main();
