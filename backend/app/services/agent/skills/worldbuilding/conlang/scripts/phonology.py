#!/usr/bin/env python3
"""
Phoneme Inventory Generator

Generates linguistically plausible phoneme inventories for constructed languages.
Uses PHOIBLE-derived frequency data to select phonemes based on cross-linguistic patterns.

Usage:
    python phonology.py --complexity flavor
    python phonology.py --complexity naming --seed 12345
    python phonology.py --preset elvish_like
    python phonology.py --family romance --features aspirated
"""

import json
import os
import random as random_mod
import sys


class SeededRandom:
    def __init__(self, seed):
        self.seed = seed

    def next(self):
        self.seed = (self.seed * 1103515245 + 12345) & 0x7FFFFFFF
        return self.seed / 0x7FFFFFFF

    def shuffle(self, array):
        result = list(array)
        for i in range(len(result) - 1, 0, -1):
            j = int(self.next() * (i + 1))
            result[i], result[j] = result[j], result[i]
        return result

    def pick(self, array, count):
        return self.shuffle(array)[:count]

    def pick_weighted(self, items, count):
        selected = []
        remaining = list(items)
        while len(selected) < count and len(remaining) > 0:
            total = sum(w for _, w in remaining)
            r = self.next() * total
            for i, (item, weight) in enumerate(remaining):
                r -= weight
                if r <= 0:
                    selected.append(item)
                    remaining.pop(i)
                    break
        return selected


def load_data():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    data_dir = os.path.join(script_dir, "..", "data")
    phonemes_path = os.path.join(data_dir, "phoneme-frequencies.json")
    syllables_path = os.path.join(data_dir, "syllable-templates.json")
    with open(phonemes_path, "r", encoding="utf-8") as f:
        phonemes = json.load(f)
    with open(syllables_path, "r", encoding="utf-8") as f:
        syllables = json.load(f)
    return phonemes, syllables


def extract_consonants(data):
    consonants = []
    for cat, sub in [("stops", "voiceless"), ("stops", "voiced"), ("fricatives", "voiceless"), ("fricatives", "voiced")]:
        section = data.get("consonants", {}).get(cat, {}).get(sub, {}) or {}
        for phoneme, info in section.items():
            consonants.append({"phoneme": phoneme, "weight": info["frequency"], "tier": info["tier"]})
    for cat in ("nasals", "liquids", "glides"):
        section = data.get("consonants", {}).get(cat, {}) or {}
        for phoneme, info in section.items():
            if phoneme == "description":
                continue
            consonants.append({"phoneme": phoneme, "weight": info["frequency"], "tier": info["tier"]})
    affricates = data.get("consonants", {}).get("affricates", {})
    if affricates:
        for sub in ("voiceless", "voiced"):
            section = affricates.get(sub, {}) or {}
            for phoneme, info in section.items():
                consonants.append({"phoneme": phoneme, "weight": info["frequency"], "tier": info["tier"]})
    return consonants


def generate_inventory(phonemes, syllables, options):
    rng = SeededRandom(options["seed"])
    complexity_preset = phonemes.get("complexity_presets", {}).get(
        options["complexity"], phonemes.get("complexity_presets", {}).get("naming", {}))
    target_consonants = complexity_preset["consonants"]["target"]
    target_vowels = complexity_preset["vowels"]["target"]
    syllable_complexity = {"flavor": "simple", "naming": "moderate"}.get(options["complexity"], "complex")
    syllable_preset = syllables["complexity_levels"][syllable_complexity]
    if options.get("preset") and options["preset"] in syllables.get("presets", {}):
        syllable_preset = syllables["presets"][options["preset"]]
    all_consonants = extract_consonants(phonemes)
    tier_filter_map = {
        "flavor": ["universal", "common"],
        "naming": ["universal", "common", "less_common"],
    }
    tier_filter = tier_filter_map.get(options["complexity"], ["universal", "common", "less_common", "rare"])
    eligible = [c for c in all_consonants if c["tier"] in tier_filter]
    selected_consonants = rng.pick_weighted(
        [(c["phoneme"], c["weight"]) for c in eligible], target_consonants)
    vowel_pool = list(phonemes["vowels"]["universal"]["phonemes"])
    if target_vowels > 3:
        vowel_pool.extend(phonemes["vowels"]["common"]["phonemes"])
    if target_vowels > 5:
        vowel_pool.extend(phonemes["vowels"]["extended"]["phonemes"])
    if target_vowels > 8:
        vowel_pool.extend(phonemes["vowels"]["less_common"]["phonemes"])
    selected_vowels = rng.pick(vowel_pool, target_vowels)
    features = list(options.get("features") or [])
    return {
        "consonants": sorted(selected_consonants),
        "vowels": sorted(selected_vowels),
        "syllableTemplates": syllable_preset["templates"],
        "features": features,
        "metadata": {
            "complexity": options["complexity"],
            "seed": options["seed"],
            "consonantCount": len(selected_consonants),
            "vowelCount": len(selected_vowels),
            "preset": options.get("preset"),
            "family": options.get("family"),
        },
    }


def format_inventory(inventory):
    lines = []
    lines.append("# Phoneme Inventory")
    lines.append("")
    lines.append("**Complexity:** {}".format(inventory["metadata"]["complexity"]))
    lines.append("**Seed:** {} (use this seed to regenerate)".format(inventory["metadata"]["seed"]))
    if inventory["metadata"].get("preset"):
        lines.append("**Preset:** {}".format(inventory["metadata"]["preset"]))
    lines.append("")
    lines.append("## Consonants ({})".format(inventory["metadata"]["consonantCount"]))
    lines.append("")
    lines.append("  ".join(inventory["consonants"]))
    lines.append("")
    lines.append("## Vowels ({})".format(inventory["metadata"]["vowelCount"]))
    lines.append("")
    lines.append("  ".join(inventory["vowels"]))
    lines.append("")
    lines.append("## Syllable Structure")
    lines.append("")
    lines.append("Templates: {}".format(", ".join(inventory["syllableTemplates"])))
    lines.append("")
    if inventory["features"]:
        lines.append("## Special Features")
        lines.append("")
        lines.append(", ".join(inventory["features"]))
        lines.append("")
    lines.append("## Usage Tips")
    lines.append("")
    lines.append("- Use the consonants and vowels to create names following the syllable templates")
    lines.append("- CV = consonant + vowel, CVC = consonant + vowel + consonant, etc.")
    lines.append("- For consistency, stick to these phonemes for all names in this culture/species")
    lines.append("- Save this seed to regenerate the same inventory later")
    return chr(10).join(lines)


def main():
    args = sys.argv[1:]
    if "--help" in args or "-h" in args:
        print("Phoneme Inventory Generator")
        print()
        print("Usage:")
        print("  python phonology.py [options]")
        print()
        print("Options:")
        print("  --complexity <level>  Complexity level: flavor, naming, full (default: naming)")
        print("  --seed <number>       Seed for reproducible generation (default: random)")
        print("  --preset <name>       Use a preset style: japanese_like, hawaiian_like, latin_like,")
        print("                        arabic_like, english_like, elvish_like, harsh_fantasy")
        print("  --family <name>       Base on language family: romance, germanic, slavic, semitic,")
        print("                        sino_tibetan, polynesian, japanese")
        print("  --features <list>     Comma-separated optional features: aspirated, ejectives, tones")
        print("  --json                Output as JSON")
        print()
        print("Complexity Levels:")
        print("  flavor  - Minimal (10-15 consonants, 3-5 vowels) for quick names/phrases")
        print("  naming  - Standard (15-22 consonants, 5-7 vowels) for consistent naming")
        print("  full    - Complete (20-35 consonants, 7-12 vowels) for developed language")
        print()
        print("Examples:")
        print("  python phonology.py --complexity flavor")
        print("  python phonology.py --preset elvish_like --seed 42")
        print("  python phonology.py --complexity full --features aspirated,tones")
        sys.exit(0)
    complexity = "naming"
    seed = None
    preset = None
    family = None
    features = None
    json_output = "--json" in args
    for i, arg in enumerate(args):
        if arg == "--complexity" and i + 1 < len(args):
            complexity = args[i + 1]
        elif arg == "--seed" and i + 1 < len(args):
            seed = int(args[i + 1])
        elif arg == "--preset" and i + 1 < len(args):
            preset = args[i + 1]
        elif arg == "--family" and i + 1 < len(args):
            family = args[i + 1]
        elif arg == "--features" and i + 1 < len(args):
            features = args[i + 1].split(",")
    if seed is None:
        seed = random_mod.randint(0, 999999)
    if complexity not in ("flavor", "naming", "full"):
        print("Error: Unknown complexity level", file=sys.stderr)
        print("Available: flavor, naming, full", file=sys.stderr)
        sys.exit(1)
    try:
        phonemes, syllable_data = load_data()
        inventory = generate_inventory(phonemes, syllable_data, {
            "complexity": complexity, "seed": seed, "preset": preset,
            "family": family, "features": features,
        })
        if json_output:
            print(json.dumps(inventory, indent=2, ensure_ascii=False))
        else:
            print(format_inventory(inventory))
    except Exception as e:
        print("Error: {}".format(e), file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
