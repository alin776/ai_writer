#!/usr/bin/env python3
"""
Word Generator

Generates words from a phoneme inventory using syllable templates.
Can use output from phonology.py or custom phoneme sets.

Usage:
    python words.py --count 20
    python words.py --inventory inventory.json --count 10
    python words.py --syllables 2-3 --seed 12345
"""

import json
import math
import os
import random as random_mod
import sys


class SeededRandom:
    def __init__(self, seed):
        self.seed = seed

    def next(self):
        self.seed = (self.seed * 1103515245 + 12345) & 0x7FFFFFFF
        return self.seed / 0x7FFFFFFF

    def pick(self, array):
        return array[int(self.next() * len(array))]

    def range(self, min_val, max_val):
        return int(self.next() * (max_val - min_val + 1)) + min_val


DEFAULT_INVENTORY = {
    "consonants": ["p", "t", "k", "m", "n", "s", "l", "r", "w", "j", "h"],
    "vowels": ["a", "e", "i", "o", "u"],
    "syllableTemplates": ["CV", "CVC", "V", "VC"],
}


def load_syllable_data():
    try:
        script_dir = os.path.dirname(os.path.abspath(__file__))
        data_dir = os.path.join(script_dir, "..", "data")
        syllables_path = os.path.join(data_dir, "syllable-templates.json")
        with open(syllables_path, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return None


def parse_inventory(inventory_path=None):
    if inventory_path:
        with open(inventory_path, "r", encoding="utf-8") as f:
            return json.load(f)
    # Check for piped input
    if not sys.stdin.isatty():
        content = sys.stdin.read().strip()
        if content:
            return json.loads(content)
    return DEFAULT_INVENTORY


def generate_syllable(template, consonants, vowels, rng):
    syllable = ""
    structure = ""
    for char in template:
        if char == "C":
            syllable += rng.pick(consonants)
            structure += "C"
        elif char == "V":
            syllable += rng.pick(vowels)
            structure += "V"
        elif char == "n":
            syllable += "n"
            structure += "n"
    return syllable, structure


def generate_word(inventory, templates, syllable_count, rng):
    syllables = []
    structures = []
    for _ in range(syllable_count):
        template = rng.pick(templates)
        syllable, structure = generate_syllable(
            template, inventory["consonants"], inventory["vowels"], rng)
        syllables.append(syllable)
        structures.append(structure)
    return {
        "word": "".join(syllables),
        "syllables": syllables,
        "structure": "-".join(structures),
    }


def generate_words(inventory, options):
    rng = SeededRandom(options["seed"])
    templates = (options.get("templates") or
                 inventory.get("syllableTemplates") or
                 DEFAULT_INVENTORY["syllableTemplates"])
    words = []
    for _ in range(options["count"]):
        syllable_count = rng.range(options["syllableRange"][0], options["syllableRange"][1])
        words.append(generate_word(inventory, templates, syllable_count, rng))
    return {
        "words": words,
        "inventory": {
            "consonants": inventory["consonants"],
            "vowels": inventory["vowels"],
            "templates": templates,
        },
        "metadata": {
            "count": options["count"],
            "seed": options["seed"],
            "syllableRange": options["syllableRange"],
        },
    }


def format_output(result, show_details):
    lines = []
    lines.append("# Generated Words")
    lines.append("")
    lines.append("**Seed:** {}".format(result["metadata"]["seed"]))
    lines.append("**Syllables:** {}-{}".format(result["metadata"]["syllableRange"][0], result["metadata"]["syllableRange"][1]))
    lines.append("**Count:** {}".format(result["metadata"]["count"]))
    lines.append("")
    lines.append("## Words")
    lines.append("")
    if show_details:
        for word in result["words"]:
            lines.append("- **{}** [{}] ({})".format(word["word"], "-".join(word["syllables"]), word["structure"]))
    else:
        for word in result["words"]:
            lines.append("- {}".format(word["word"]))
    lines.append("")
    lines.append("## Inventory Used")
    lines.append("")
    lines.append("Consonants: {}".format(" ".join(result["inventory"]["consonants"])))
    lines.append("Vowels: {}".format(" ".join(result["inventory"]["vowels"])))
    lines.append("Templates: {}".format(", ".join(result["inventory"]["templates"])))
    return chr(10).join(lines)


def generate_categories(inventory, templates, seed):
    rng = SeededRandom(seed)
    categories = {
        "Short (1-2 syllables)": {"syllables": (1, 2), "count": 5},
        "Medium (2-3 syllables)": {"syllables": (2, 3), "count": 5},
        "Long (3-4 syllables)": {"syllables": (3, 4), "count": 5},
        "Names (2-3 syllables)": {"syllables": (2, 3), "count": 10},
        "Places (2-4 syllables)": {"syllables": (2, 4), "count": 5},
    }
    result = {}
    for category, config in categories.items():
        words = []
        for _ in range(config["count"]):
            count = rng.range(config["syllables"][0], config["syllables"][1])
            word = generate_word(inventory, templates, count, rng)
            words.append(word["word"])
        result[category] = words
    return result


def main():
    args = sys.argv[1:]
    if "--help" in args or "-h" in args:
        print("Word Generator")
        print()
        print("Usage:")
        print("  python words.py [options]")
        print()
        print("Options:")
        print("  --inventory <file>  Path to inventory JSON (from phonology.py --json)")
        print("  --count <number>    Number of words to generate (default: 20)")
        print("  --syllables <range> Syllable count range, e.g., 2-3 (default: 1-3)")
        print("  --seed <number>     Seed for reproducible generation (default: random)")
        print("  --details           Show syllable breakdown and structure")
        print("  --categories        Generate words in categories (names, places, etc.)")
        print("  --json              Output as JSON")
        print()
        print("Input:")
        print("  Can read inventory from stdin: phonology.py --json | python words.py --count 10")
        print()
        print("Examples:")
        print("  python words.py --count 20")
        print("  python words.py --inventory my-language.json --count 10")
        print("  python words.py --syllables 2-4 --seed 42 --details")
        print("  python words.py --categories")
        sys.exit(0)
    inventory_path = None
    count = 20
    seed = None
    syllable_range = (1, 3)
    show_details = "--details" in args
    show_categories = "--categories" in args
    json_output = "--json" in args
    for i, arg in enumerate(args):
        if arg == "--inventory" and i + 1 < len(args):
            inventory_path = args[i + 1]
        elif arg == "--count" and i + 1 < len(args):
            count = int(args[i + 1])
        elif arg == "--syllables" and i + 1 < len(args):
            parts = args[i + 1].split("-")
            if len(parts) == 2:
                try:
                    syllable_range = (int(parts[0]), int(parts[1]))
                except ValueError:
                    pass
        elif arg == "--seed" and i + 1 < len(args):
            seed = int(args[i + 1])
    if seed is None:
        seed = random_mod.randint(0, 999999)
    try:
        inventory = parse_inventory(inventory_path)
        syllable_data = load_syllable_data()
        templates = (inventory.get("syllableTemplates") or
                     (syllable_data or {}).get("complexity_levels", {}).get("moderate", {}).get("templates") or
                     DEFAULT_INVENTORY["syllableTemplates"])
        if show_categories:
            categories = generate_categories(inventory, templates, seed)
            if json_output:
                print(json.dumps({"categories": categories, "seed": seed}, indent=2))
            else:
                print("# Word Categories")
                print()
                print("**Seed:** {}".format(seed))
                print()
                for category, words in categories.items():
                    print("## {}".format(category))
                    print()
                    print(", ".join(words))
                    print()
        else:
            result = generate_words(inventory, {
                "count": count,
                "seed": seed,
                "syllableRange": syllable_range,
                "templates": templates,
            })
            if json_output:
                print(json.dumps(result, indent=2))
            else:
                print(format_output(result, show_details))
    except Exception as e:
        print("Error: {}".format(e), file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
