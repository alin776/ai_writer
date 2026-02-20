#!/usr/bin/env python3

"""
npc_generator.py - Generate NPCs on demand for game sessions

Creates NPCs with name, motivation, trait, voice, and story hook.

Usage:
  python scripts/npc_generator.py
  python scripts/npc_generator.py --tone dark-fantasy
  python scripts/npc_generator.py --role merchant --trait suspicious
"""

import random
import sys

TONES = {
    "dark-fantasy": {
        "names": ["Grimwald", "Sera", "Thorne", "Ashlyn", "Mordecai", "Lilith", "Cain", "Isolde", "Raven", "Dusk"],
        "flavor": "grim, desperate, haunted",
    },
    "high-fantasy": {
        "names": ["Aldric", "Elara", "Thorin", "Lyanna", "Galen", "Seraphina", "Bram", "Mira", "Cedric", "Faye"],
        "flavor": "noble, questing, legendary",
    },
    "urban-fantasy": {
        "names": ["Jack", "Maya", "Dante", "Zara", "Marcus", "Luna", "Ash", "Vera", "Cole", "Iris"],
        "flavor": "street-smart, hidden, dual-life",
    },
    "sci-fi": {
        "names": ["Kira", "Dex", "Nova", "Zane", "Echo", "Ryn", "Jax", "Vera", "Orion", "Cass"],
        "flavor": "pragmatic, augmented, frontier",
    },
    "historical": {
        "names": ["Edmund", "Catherine", "William", "Elizabeth", "Thomas", "Margaret", "John", "Anne", "Henry", "Mary"],
        "flavor": "formal, hierarchical, tradition-bound",
    },
    "modern": {
        "names": ["Sam", "Alex", "Jordan", "Casey", "Morgan", "Riley", "Taylor", "Jamie", "Quinn", "Blake"],
        "flavor": "contemporary, relatable, grounded",
    },
}

ROLES = [
    "merchant", "guard", "innkeeper", "scholar", "priest", "criminal", "noble",
    "peasant", "artisan", "soldier", "healer", "entertainer", "messenger",
    "hunter", "sailor", "servant", "beggar", "traveler", "official", "mystic",
]

WANTS = [
    "money to pay a debt", "information about someone", "protection from a threat",
    "revenge for a wrong", "escape from this place", "to find a missing person",
    "to keep a secret hidden", "to expose a secret", "power over others",
    "to be left alone", "recognition for their work", "to help someone they love",
    "to destroy something", "to preserve something", "to prove themselves",
    "to atone for past actions", "to acquire a specific item",
    "to prevent a coming disaster", "to complete a dying wish", "to sabotage a rival",
]

METHODS = [
    "manipulation and lies", "direct confrontation", "bargaining and deals",
    "pleading and sympathy", "threats and intimidation", "seduction and charm",
    "deception and disguise", "patience and observation", "bribery and corruption",
    "violence as last resort", "gathering allies", "undermining rivals",
    "leveraging connections", "exploiting weaknesses", "offering genuine help",
]

TRAITS = [
    "nervous, fidgeting constantly", "overly friendly, too eager to please",
    "suspicious, watches everyone", "exhausted, barely holding on",
    "arrogant, dismissive of others", "grieving, heavy with loss",
    "cheerful despite circumstances", "bitter about past failures",
    "devoutly religious", "secretly terrified", "calculating every angle",
    "genuinely kind-hearted", "barely concealed anger",
    "mysterious, speaks in riddles", "blunt to the point of rudeness",
    "drunk or intoxicated", "physically distinctive (scar, limp)",
    "clearly lying about something", "desperately hiding something",
    "nostalgic for better times",
]

VOICE_PATTERNS = [
    "speaks in short, clipped sentences", "rambles and loses track of thoughts",
    "formal and overly polite", "casual, uses slang and curses",
    "whispers conspiratorially", "loud and commanding",
    "hesitant, lots of pauses", "rapid-fire, barely pauses for breath",
    "asks too many questions", "never quite answers directly",
    "uses elaborate vocabulary", "speaks in platitudes and sayings",
    "nervous laughter between phrases", "sighs heavily before speaking",
    "interrupts constantly",
]

HOOKS = [
    "knows something about a player's background",
    "has an item the players need",
    "is being hunted by the same enemy",
    "witnessed something the players need to know",
    "owes a debt to someone the players know",
    "recognizes a player from somewhere",
    "is pretending to be someone else",
    "has a job that needs doing",
    "is dying and needs one last thing",
    "is working for the opposition secretly",
    "can provide access to a restricted area",
    "has a missing family member to find",
    "carries a curse that affects others",
    "knows the location of something valuable",
    "is the last survivor of something significant",
]


def generate_npc(tone=None, role=None, trait=None):
    t = tone if tone and tone in TONES else random.choice(list(TONES.keys()))
    tone_data = TONES[t]
    return {
        "name": random.choice(tone_data["names"]),
        "role": role or random.choice(ROLES),
        "want": random.choice(WANTS),
        "method": random.choice(METHODS),
        "trait": trait or random.choice(TRAITS),
        "voice": random.choice(VOICE_PATTERNS),
        "hook": random.choice(HOOKS),
    }


def format_npc(npc):
    return """
NPC GENERATED
=============

Name: {name}
Role: {role}

MOTIVATION
  Want: {want}
  Method: {method}

PORTRAYAL
  Trait: {trait}
  Voice: {voice}

STORY HOOK
  {hook}

QUICK REFERENCE
  "{name} the {role} wants {want}
   and will use {method} to get it."

NOTES FOR PLAY
  - Play the want actively - they're always pursuing it
  - The trait is visible; the want may be hidden
  - The hook creates connection - use when the moment is right
""".format(**npc)


def main():
    args = sys.argv[1:]

    if "--help" in args or "-h" in args:
        print("NPC Generator\n")
        print("Usage: python scripts/npc_generator.py [options]\n")
        print("Options:")
        print("  --tone <tone>     Set the tone/setting")
        print("  --role <role>     Specify role/occupation")
        print("  --trait <trait>   Specify personality trait")
        print("  --count <n>      Generate multiple NPCs")
        print("\nTones:", ", ".join(TONES.keys()))
        sys.exit(0)

    opts = {}
    count = 1
    i = 0
    while i < len(args):
        if args[i] == "--tone" and i + 1 < len(args):
            i += 1; opts["tone"] = args[i]
        elif args[i] == "--role" and i + 1 < len(args):
            i += 1; opts["role"] = args[i]
        elif args[i] == "--trait" and i + 1 < len(args):
            i += 1; opts["trait"] = args[i]
        elif args[i] == "--count" and i + 1 < len(args):
            i += 1; count = int(args[i])
        i += 1

    for j in range(count):
        npc = generate_npc(**opts)
        print(format_npc(npc))
        if j < count - 1:
            print("\n" + "-" * 50 + "\n")


if __name__ == "__main__":
    main()
