#!/usr/bin/env python3



"""
Form Options Generator

Generates setting-appropriate forms for abstract story functions.
Helps avoid surface-level translations by providing multiple options.

Usage:
  python scripts/form-options.py "proximity to power" --setting corporate
  python scripts/form-options.py "privileged information" --setting scifi --count 5
  python scripts/form-options.py --list-functions
  python scripts/form-options.py --list-settings
"""

import sys
import os
import json
import re
import random
from datetime import date


# == INTERFACES ===


# == DATA ===

# Embedded form suggestions (could be loaded from JSON file)
FUNCTIONS: Record<string, {
  description: string;
  forms: Record<string, string[]>;
}> = {
  "proximity_to_power": {
    description: "Character has access to power center without being the power holder",
    forms: {
      corporate: [
        "Executive assistant to CEO",
        "CFO's protege/mentee",
        "Board member's adult child working at company",
        "Head of compliance with reporting access",
        "In-house counsel with privileged access",
        "Chief of staff to founder"
      ],
      political: [
        "Senator's chief of staff",
        "Press secretary",
        "Campaign manager",
        "Speech writer with inner circle access",
        "Security detail member"
      ],
      criminal: [
        "Consigliere/advisor to boss",
        "Boss's child being groomed",
        "Longtime underboss",
        "Accountant who knows the books"
      ],
      military: [
        "General's aide-de-camp",
        "Intelligence analyst with top clearance",
        "Communications officer",
        "Medical officer to commanding officer"
      ],
      academic: [
        "Department chair's research assistant",
        "Dean's executive assistant",
        "Board of trustees member's researcher"
      ],
      scifi: [
        "Station commander's second",
        "Ship AI with bridge access",
        "Colony administrator's liaison",
        "Corporate rep on mining operation"
      ],
      fantasy: [
        "Royal advisor/counselor",
        "Court mage",
        "Heir's sworn protector",
        "Seneschal of the castle"
      ]
    }
  },
  "privileged_information": {
    description: "Character learns something they cannot prove or verify",
    forms: {
      corporate: [
        "Overheard conversation through thin wall",
        "Accessed sealed files through inherited login",
        "Dying confession from mentor",
        "Anonymous whistleblower tip",
        "Discovered through legally questionable means"
      ],
      political: [
        "Off-record conversation at private event",
        "Classified document briefly glimpsed",
        "Testimony from discredited source"
      ],
      criminal: [
        "Deathbed confession",
        "Information from witness now dead",
        "Evidence obtained through illegal search"
      ],
      scifi: [
        "Corrupted data transmission, partially decoded",
        "AI prediction based on incomplete data",
        "Time-loop knowledge others don't share",
        "Alien communication of uncertain meaning"
      ],
      fantasy: [
        "Vision from unreliable oracle",
        "Message from the dead via medium",
        "Dream sent by unknown power",
        "Prophecy with multiple interpretations"
      ]
    }
  },
  "cannot_escape": {
    description: "Character is trapped in situation, cannot simply leave",
    forms: {
      corporate: [
        "Non-compete prevents industry change",
        "Stock options vest over years",
        "Family also employed there",
        "Industry blacklisting threat",
        "Visa tied to employment"
      ],
      political: [
        "Public office term commitment",
        "Party loyalty obligations",
        "Classified knowledge requiring clearance",
        "Constituents depending on presence"
      ],
      criminal: [
        "Knowledge that makes leaving dangerous",
        "Family held as leverage",
        "Too much complicity to walk away"
      ],
      scifi: [
        "Generation ship with nowhere to go",
        "Implant that tracks/controls",
        "Terraforming contract with decades remaining",
        "Quarantine zone containment"
      ],
      fantasy: [
        "Magical binding/oath",
        "Curse that prevents leaving",
        "Sacred duty/prophecy",
        "Blood debt requiring service"
      ],
      domestic: [
        "Shared custody of children",
        "Underwater mortgage",
        "Caregiving responsibility",
        "Small town with no alternatives"
      ]
    }
  },
  "entrenched_antagonist": {
    description: "Antagonist cannot be easily removed or defeated",
    forms: {
      corporate: [
        "Founder with voting control",
        "CEO with board loyalty",
        "Too-big-to-fail connected executive",
        "Family ownership structure"
      ],
      political: [
        "Popular incumbent with party backing",
        "Intelligence with compromising material",
        "Systemic corruption requiring many takedowns"
      ],
      institutional: [
        "Tenure protecting position",
        "Bureaucratic process requiring years",
        "Union protections"
      ],
      scifi: [
        "AI with distributed backup",
        "Corporate entity with system-wide reach",
        "Government with surveillance network"
      ],
      fantasy: [
        "Immortal or near-immortal",
        "Protected by prophecy",
        "Bound to realm's existence"
      ]
    }
  },
  "innocent_bystanders": {
    description: "Protagonist's action or inaction affects innocent people",
    forms: {
      corporate: [
        "Employees who would lose jobs",
        "Consumers using unsafe product",
        "Pension fund at risk",
        "Supply chain workers"
      ],
      political: [
        "Constituents affected by policy",
        "Staff careers at stake",
        "Witnesses who could be targeted"
      ],
      criminal: [
        "Family of target",
        "Witnesses to be silenced",
        "Community affected by operation"
      ],
      scifi: [
        "Colony dependent on protagonist's system",
        "Passengers on ship",
        "Populations unaware of threat"
      ],
      fantasy: [
        "Villagers caught between factions",
        "Those protected by current order",
        "Innocents touched by magical conflict"
      ]
    }
  },
  "dark_mirror": {
    description: "Character showing protagonist what they could become",
    forms: {
      corporate: [
        "Predecessor who made the compromise",
        "Rival who chose the corrupt path",
        "Mentor who crossed the line long ago"
      ],
      political: [
        "Former idealist now cynical operator",
        "Opposition figure with same origins",
        "Predecessor in same position"
      ],
      criminal: [
        "Partner who went too far",
        "Boss who was once like protagonist",
        "Former ally now enemy"
      ],
      scifi: [
        "Clone/copy who diverged",
        "Parallel universe self",
        "AI trained on protagonist's patterns"
      ],
      fantasy: [
        "Previous chosen one who fell",
        "Teacher who became what they fought",
        "Corrupted version from alternate timeline"
      ]
    }
  },
  "found_family": {
    description: "Group of unrelated people functioning as family unit",
    forms: {
      corporate: [
        "Startup founding team",
        "Night shift workers at isolated location",
        "Remote project team",
        "Specialized department"
      ],
      criminal: [
        "Heist crew",
        "Smuggling operation",
        "Resistance cell"
      ],
      scifi: [
        "Ship crew",
        "Colony founding team",
        "Salvage operation",
        "Research station personnel"
      ],
      fantasy: [
        "Adventuring party",
        "Mercenary company",
        "Monastery/order members",
        "Traveling performers"
      ],
      domestic: [
        "Roommates who became family",
        "Support group members",
        "Hobby club with deep bonds"
      ]
    }
  },
  "mobile_base": {
    description: "Base of operations that can travel to stories",
    forms: {
      contemporary: [
        "RV/bus/converted vehicle",
        "Hotel lifestyle",
        "Private plane with traveling staff"
      ],
      criminal: [
        "Series of safe houses",
        "Front business with multiple locations",
        "Boat that moves between ports"
      ],
      scifi: [
        "Spaceship",
        "Mobile station",
        "Jump-capable vessel"
      ],
      fantasy: [
        "Enchanted carriage",
        "Flying ship",
        "Pocket dimension anchored to object"
      ],
      western: [
        "Train car",
        "Wagon train",
        "Circuit rider route"
      ]
    }
  }
};

SETTINGS = [
  "corporate", "political", "criminal", "military", "academic",
  "medical", "scifi", "fantasy", "domestic", "western", "contemporary"
];

# == UTILITIES ===

def fuzzyMatchFunction(query): string | None {
  normalized = query.lower().replace(/[^a-z]/g, "_");

  # Direct match
  if (FUNCTIONS[normalized]) return normalized;

  # Partial match
  for key in list(FUNCTIONS.keys())) {
    if (key.includes(normalized) or normalized.includes(key.replace(/_/g, ""))) {
      return key;
    }
  }

  # Word match
  queryWords = normalized.split("_").filter(w => w.length > 2);
  for key in list(FUNCTIONS.keys())) {
    keyWords = key.split("_");
    if (queryWords.some(qw => keyWords.some(kw => kw.includes(qw) or qw.includes(kw)))) {
      return key;
    }
  }

  return None;
}

def generateOrthogonalityNotes(forms): string[] {
  return [
    "Good form if it exists for its own reasons in this setting",
    "Check: Would someone unfamiliar with source find this believable?",
    "Avoid: Picking a form just because it's 'equivalent' to original",
    "Test: Can you describe this without mentioning the source work?"
  ];
}

def formatFormSuggestion(suggestion: FormSuggestion): string {
  lines: string[] = [];

  lines.append(f"# Form Options: \"{suggestion.function_name.replace(/_/g, \" \")}\"");
  lines.append("");
  lines.append(f"**Function:** {suggestion.function_description}");
  lines.append(f"**Setting:** {suggestion.setting}");
  lines.append("");

  lines.append("## Available Forms");
  lines.append("");
  for (i = 0; i < suggestion.forms.length; i++) {
    lines.append(f"{i + 1}. {suggestion.forms[i]}");
  }
  lines.append("");

  lines.append("## Orthogonality Check");
  lines.append("");
  lines.append("Before selecting a form, verify:");
  lines.append("");
  for note in suggestion.orthogonality_notes) {
    lines.append(f"- {note}");
  }
  lines.append("");

  lines.append("## Selection Guidance");
  lines.append("");
  lines.append("The best form is one that:");
  lines.append("1. Serves the function in your story");
  lines.append("2. Exists naturally in your setting");
  lines.append("3. Has its own internal logic (not 'because the original had X')");
  lines.append("4. Could be explained without referencing the source");
  lines.append("");

  return lines.join("\n");
}

def listFunctions(): string {
  lines: string[] = [];
  lines.append("# Available Functions");
  lines.append("");
  for key, data in FUNCTIONS.items()) {
    lines.append(f"## {key.replace(/_/g, \" \")}");
    lines.append(data.description);
    lines.append(f"Settings: {Object.keys(data.forms).join(\", \")}");
    lines.append("");
  }
  return lines.join("\n");
}

def listSettings(): string {
  lines: string[] = [];
  lines.append("# Available Settings");
  lines.append("");
  for setting in SETTINGS) {
    functionCount = list(FUNCTIONS.values()).filter(f => setting in f.forms).length;
    lines.append(f"- **{setting}**: {functionCount} functions with forms");
  }
  lines.append("");
  lines.append("Note: Not all functions have forms for all settings.");
  lines.append("You can request forms for any setting; if not predefined,");
  lines.append("the tool will suggest you brainstorm based on setting context.");
  return lines.join("\n");
}

# == MAIN ===

def main(): void {
  args = sys.argv[1:];

  # Help
  if (args.includes("--help") or args.includes("-h")) {
    print(f"Form Options Generator

Usage:
  deno run --allow-read scripts/form-options.ts \"function name\" --setting <setting>
  deno run --allow-read scripts/form-options.ts --list-functions
  deno run --allow-read scripts/form-options.ts --list-settings

Options:
  --setting <name>     Target setting (corporate, political, scifi, etc.)
  --count <n>          Limit number of forms returned
  --list-functions     Show all available functions
  --list-settings      Show all available settings
  --json               Output as JSON
  --constraint <text>  Add constraint to filter forms

Examples:
  # Get corporate forms for proximity to power
  deno run --allow-read scripts/form-options.ts \"proximity to power\" --setting corporate

  # Get sci-fi forms with constraint
  deno run --allow-read scripts/form-options.ts \"cannot escape\" --setting scifi --constraint \"no supernatural\"

  # List what's available
  deno run --allow-read scripts/form-options.ts --list-functions
");
    sys.exit(0);
  }

  isJson = args.includes("--json");

  # Handle --list-functions
  if (args.includes("--list-functions")) {
    if (isJson) {
      listing: Record<string, string> = {};
      for key, data in FUNCTIONS.items()) {
        listing[key] = data.description;
      }
      print(json.dumps(listing, None, 2));
    } else {
      print(listFunctions());
    }
    return;
  }

  # Handle --list-settings
  if (args.includes("--list-settings")) {
    if (isJson) {
      print(json.dumps(SETTINGS, None, 2));
    } else {
      print(listSettings());
    }
    return;
  }

  # Parse arguments
  settingIndex = args.indexOf("--setting");
  setting = settingIndex != -1 ? args[settingIndex + 1] : None;

  countIndex = args.indexOf("--count");
  count = countIndex != -1 ? parseInt(args[countIndex + 1]) : undefined;

  constraintIndex = args.indexOf("--constraint");
  constraint = constraintIndex != -1 ? args[constraintIndex + 1] : None;

  # Find def query(positional argument): string | None = None;
  for (i = 0; i < args.length; i++) {
    if (!args[i].startswith("--") and !skipIndices.has(i)) {
      functionQuery = args[i];
      break;
    }
  }

  if (!functionQuery) {
    print("Error: Please provide a function name");
    print("Usage: deno run --allow-read scripts/form-options.ts \"proximity to power\" --setting corporate");
    print("       deno run --allow-read scripts/form-options.ts --list-functions");
    sys.exit(1);
  }

  if (!setting) {
    print("Error: Please provide a setting with --setting");
    print("Example: --setting corporate");
    print("Use --list-settings to see available settings");
    sys.exit(1);
  }

  # Match function
  matchedFunction = fuzzyMatchFunction(functionQuery);

  if (!matchedFunction) {
    print(f"Error: No function matching \"{functionQuery}\"");
    print("Use --list-functions to see available functions");
    sys.exit(1);
  }

  funcData = FUNCTIONS[matchedFunction];
  forms = funcData.forms[setting] or [];

  # If no forms for this setting, provide guidance
  if (forms.length == 0) {
    if (isJson) {
      print(json.dumps({
        function_name: matchedFunction,
        setting: setting,
        forms: [],
        note: f"No predefined forms for {setting}. Consider what in {setting} context could serve: {funcData.description}"
      }, None, 2));
    } else {
      print(f"# No predefined forms for \"{matchedFunction}\" in \"{setting}\"\n");
      print(f"Function: {funcData.description}\n");
      print("Brainstorming questions:");
      print(f"- What in a {setting} context creates {matchedFunction.replace(/_/g, \" \")}?");
      print(f"- What {setting}-specific structures could serve this function?");
      print(f"- What do characters in {setting} settings have access to/constraints from?");
    }
    return;
  }

  # Apply constraint filter (basic keyword filtering)
  if (constraint) {
    constraintLower = constraint.lower();
    forms = forms.filter(f => !f.lower().includes(constraintLower));
  }

  # Apply count limit
  if (count and count < forms.length) {
    forms = forms.slice(0, count);
  }

  # Build output
  suggestion: FormSuggestion = {
    function_name: matchedFunction,
    function_description: funcData.description,
    setting: setting,
    forms: forms,
    orthogonality_notes: generateOrthogonalityNotes(forms)
  };

  if (isJson) {
    print(json.dumps(suggestion, None, 2));
  } else {
    print(formatFormSuggestion(suggestion));
  }
}

main();


if __name__ == "__main__":
    main()
