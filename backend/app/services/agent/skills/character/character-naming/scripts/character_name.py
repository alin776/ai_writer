#!/usr/bin/env python3
"""
character_name.py - Character Name Generator

Generates character names from curated lists or phoneme patterns.
Breaks LLM statistical defaults by using external entropy.

Usage:
  python character_name.py --culture chinese --gender female
  python character_name.py --pool contemporary-american --count 5
  python character_name.py --fantasy elvish-like --count 10
  python character_name.py --culture anglo --cast cast.json
"""

import sys
import os
import re
import json


class SeededRandom:

    def __init__(self, seed=None):
        import random as _random
        self._seed = seed if seed is not None else _random.randint(0, 1000000)

    def next(self):
        self._seed = (self._seed * 1103515245 + 12345) & 0x7FFFFFFF
        return self._seed / 0x7FFFFFFF

    def pick(self, array):
        return array[int(self.next() * len(array))]

    def shuffle(self, array):
        result = list(array)
        for i in range(len(result) - 1, 0, -1):
            j = int(self.next() * (i + 1))
            result[i], result[j] = result[j], result[i]
        return result

    def range(self, min_val, max_val):
        return int(self.next() * (max_val - min_val + 1)) + min_val

    def get_seed(self):
        return self._seed


def get_data_dir():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(script_dir, "..", "data")


def load_name_list(culture, list_type):
    data_dir = get_data_dir()
    possible_paths = [
        os.path.join(data_dir, "cultures", f"{culture}-{list_type}.json"),
        os.path.join(data_dir, "cultures", culture, f"{list_type}.json"),
        os.path.join(data_dir, "cultures", f"{culture}.json"),
    ]
    for path in possible_paths:
        try:
            with open(path, 'r', encoding='utf-8') as f:
                return json.loads(f.read())
        except Exception:
            continue
    return None


def load_mixed_pool(pool_name):
    data_dir = get_data_dir()
    path = os.path.join(data_dir, "mixed-pools", f"{pool_name}.json")
    try:
        with open(path, 'r', encoding='utf-8') as f:
            return json.loads(f.read())
    except Exception:
        return None


def load_phoneme_preset(preset_name):
    data_dir = get_data_dir()
    path = os.path.join(data_dir, "phoneme-presets", f"{preset_name}.json")
    try:
        with open(path, 'r', encoding='utf-8') as f:
            return json.loads(f.read())
    except Exception:
        return None


def load_cast_file(cast_path):
    try:
        with open(cast_path, 'r', encoding='utf-8') as f:
            return json.loads(f.read())
    except Exception:
        return None


def list_available_cultures():
    data_dir = get_data_dir()
    cultures_dir = os.path.join(data_dir, "cultures")
    cultures = set()
    try:
        for entry in os.listdir(cultures_dir):
            if entry.endswith(".json"):
                match = re.match(r'^([a-z-]+?)(?:-(surnames|given|given-male|given-female))?\.json$', entry)
                if match:
                    cultures.add(match.group(1))
    except Exception:
        pass
    return sorted(cultures)


def list_available_pools():
    data_dir = get_data_dir()
    pools_dir = os.path.join(data_dir, "mixed-pools")
    pools = []
    try:
        for entry in os.listdir(pools_dir):
            if entry.endswith(".json"):
                pools.append(entry.replace(".json", ""))
    except Exception:
        pass
    return sorted(pools)


def list_available_presets():
    data_dir = get_data_dir()
    presets_dir = os.path.join(data_dir, "phoneme-presets")
    presets = []
    try:
        for entry in os.listdir(presets_dir):
            if entry.endswith(".json"):
                presets.append(entry.replace(".json", ""))
    except Exception:
        pass
    return sorted(presets)


def generate_from_list(name_list, count, rng):
    shuffled = rng.shuffle(name_list['names'])
    return shuffled[:min(count, len(shuffled))]


def generate_syllable(preset, template, rng):
    syllable = ""
    for char in template:
        if char == "C":
            syllable += rng.pick(preset['consonants'])
        elif char == "V":
            syllable += rng.pick(preset['vowels'])
    return syllable


def generate_fantasy_name(preset, syllable_count, rng):
    syllables = []
    for _ in range(syllable_count):
        template = rng.pick(preset['syllableTemplates'])
        syllables.append(generate_syllable(preset, template, rng))
    name = "".join(syllables)
    return name[0].upper() + name[1:]


def check_collision(name, cast):
    name_lower = name.lower()
    name_first = name_lower[0]
    name_parts = name_lower.split()
    for character in cast['characters']:
        char_lower = character['name'].lower()
        char_first = char_lower[0]
        char_parts = char_lower.split()
        if name_lower == char_lower:
            return {'collision': True, 'collision_with': character['name']}
        if name_first == char_first and len(name_parts[0]) <= 5 and len(char_parts[0]) <= 5:
            similarity = calculate_similarity(name_parts[0], char_parts[0])
            if similarity > 0.6:
                return {'collision': True, 'collision_with': character['name']}
        if len(name_parts) > 1 and len(char_parts) > 1:
            if name_parts[-1] == char_parts[-1]:
                return {'collision': True, 'collision_with': f"{character['name']} (same surname)"}
    return {'collision': False}


def calculate_similarity(a, b):
    if a == b:
        return 1
    if not a or not b:
        return 0
    a_chars = set(a)
    b_chars = set(b)
    shared = len(a_chars & b_chars)
    return shared / max(len(a_chars), len(b_chars))


def format_names(names, json_output):
    if json_output:
        print(json.dumps(names, indent=2))
    else:
        for item in names:
            if item.get('collision'):
                print(f"- {item['name']} [COLLISION with {item.get('collision_with', '?')}]")
            else:
                print(f"- {item['name']}")


def main():
    args = sys.argv[1:]

    if '--help' in args or '-h' in args:
        print("Character Name Generator\n")
        print("Usage:")
        print("  python character_name.py [options]\n")
        print("Options:")
        print("  --culture <name>    Use specific cultural pool")
        print("  --pool <name>       Use mixed pool")
        print("  --fantasy <preset>  Generate from phoneme preset")
        print("  --gender <m|f>      Filter for gendered lists")
        print("  --count <n>         Number of names to generate (default: 5)")
        print("  --syllables <range> Syllable range for fantasy names (e.g., 2-3)")
        print("  --full-name         Generate given + surname combination")
        print("  --cast <file>       Path to cast tracker JSON for collision checking")
        print("  --seed <n>          Seed for reproducible generation")
        print("  --json              Output as JSON")
        print("  --list              Show available cultures, pools, and presets")
        sys.exit(0)

    if '--list' in args:
        cultures = list_available_cultures()
        pools = list_available_pools()
        presets = list_available_presets()
        print("Available cultures:")
        if not cultures:
            print("  (none yet - add JSON files to data/cultures/)")
        else:
            for c in cultures:
                print(f"  - {c}")
        print("\nAvailable pools:")
        if not pools:
            print("  (none yet - add JSON files to data/mixed-pools/)")
        else:
            for p in pools:
                print(f"  - {p}")
        print("\nAvailable fantasy presets:")
        if not presets:
            print("  (none yet - add JSON files to data/phoneme-presets/)")
        else:
            for p in presets:
                print(f"  - {p}")
        sys.exit(0)

    def get_arg(flag):
        if flag in args:
            idx = args.index(flag)
            if idx + 1 < len(args):
                return args[idx + 1]
        return None

    culture = get_arg('--culture')
    pool = get_arg('--pool')
    fantasy = get_arg('--fantasy')
    gender = get_arg('--gender')
    count_str = get_arg('--count')
    count = int(count_str) if count_str else 5
    syllables_str = get_arg('--syllables')
    cast_path = get_arg('--cast')
    seed_str = get_arg('--seed')
    seed = int(seed_str) if seed_str else None
    full_name = '--full-name' in args
    json_output = '--json' in args

    syllable_range = (2, 3)
    if syllables_str:
        parts = syllables_str.split('-')
        if len(parts) == 2:
            try:
                syllable_range = (int(parts[0]), int(parts[1]))
            except ValueError:
                pass

    rng = SeededRandom(seed)

    cast = None
    if cast_path:
        cast = load_cast_file(cast_path)
        if not cast:
            print(f"Warning: Could not load cast file: {cast_path}", file=sys.stderr)

    generated_names = []

    if fantasy:
        preset = load_phoneme_preset(fantasy)
        if not preset:
            print(f'Error: Fantasy preset "{fantasy}" not found. Use --list to see available presets.', file=sys.stderr)
            sys.exit(1)
        for _ in range(count):
            syllable_count = rng.range(syllable_range[0], syllable_range[1])
            name = generate_fantasy_name(preset, syllable_count, rng)
            generated = {'name': name, 'source': f"fantasy:{fantasy}"}
            if cast:
                coll = check_collision(name, cast)
                generated['collision'] = coll['collision']
                if coll.get('collision_with'):
                    generated['collision_with'] = coll['collision_with']
            generated_names.append(generated)

    elif pool:
        pool_data = load_mixed_pool(pool)
        if not pool_data:
            print(f'Error: Pool "{pool}" not found. Use --list to see available pools.', file=sys.stderr)
            sys.exit(1)
        names = generate_from_list(pool_data, count, rng)
        for name in names:
            generated = {'name': name, 'source': f"pool:{pool}"}
            if cast:
                coll = check_collision(name, cast)
                generated['collision'] = coll['collision']
                if coll.get('collision_with'):
                    generated['collision_with'] = coll['collision_with']
            generated_names.append(generated)

    elif culture:
        if full_name:
            surname_list = load_name_list(culture, "surnames")
            given_type = "given-female" if gender == "f" else "given-male" if gender == "m" else "given"
            given_list = load_name_list(culture, given_type) or load_name_list(culture, "given")
            if not surname_list or not given_list:
                print(f'Error: Could not load name lists for culture "{culture}". Use --list.', file=sys.stderr)
                sys.exit(1)
            surnames = generate_from_list(surname_list, count, rng)
            given_names = generate_from_list(given_list, count, rng)
            for i in range(count):
                name = f"{given_names[i]} {surnames[i]}"
                generated = {'name': name, 'source': f"culture:{culture}"}
                if cast:
                    coll = check_collision(name, cast)
                    generated['collision'] = coll['collision']
                    if coll.get('collision_with'):
                        generated['collision_with'] = coll['collision_with']
                generated_names.append(generated)
        else:
            list_type = "given-female" if gender == "f" else "given-male" if gender == "m" else "surnames"
            name_list = load_name_list(culture, list_type) or load_name_list(culture, "given")
            if not name_list:
                print(f'Error: Could not load name list for culture "{culture}". Use --list.', file=sys.stderr)
                sys.exit(1)
            names = generate_from_list(name_list, count, rng)
            for name in names:
                generated = {'name': name, 'source': f"culture:{culture}:{list_type}"}
                if cast:
                    coll = check_collision(name, cast)
                    generated['collision'] = coll['collision']
                    if coll.get('collision_with'):
                        generated['collision_with'] = coll['collision_with']
                generated_names.append(generated)
    else:
        print("Error: Specify --culture, --pool, or --fantasy. Use --help for usage.", file=sys.stderr)
        sys.exit(1)

    format_names(generated_names, json_output)


if __name__ == '__main__':
    main()
