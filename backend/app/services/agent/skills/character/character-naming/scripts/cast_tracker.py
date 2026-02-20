#!/usr/bin/env python3
"""
cast_tracker.py - Manage cast tracking for collision detection

Manages cast tracking for collision detection and cultural distribution analysis.
Helps maintain variety and avoid confusing similar names.

Usage:
  python cast_tracker.py init "Novel Title"
  python cast_tracker.py add "Sarah Chen" --role protagonist
  python cast_tracker.py check "Marcus"
  python cast_tracker.py distribution
"""

import sys
import re
import json
import os
from datetime import date


def count_syllables(name):
    vowels = re.findall(r'[aeiouy]+', name.lower())
    return len(vowels) if vowels else 1


def get_consonants(name):
    consonants = re.findall(r'[bcdfghjklmnpqrstvwxz]', name.lower())
    return list(dict.fromkeys(consonants))


def get_vowel_pattern(name):
    return re.sub(r'[^aeiouy]', '', name.lower())


def analyze_sound_profile(name):
    parts = name.split()
    first_name = parts[0].lower()
    return {
        'startsWith': first_name[0],
        'syllables': count_syllables(first_name),
        'endsWith': first_name[-1],
        'consonants': get_consonants(first_name),
        'vowelPattern': get_vowel_pattern(first_name),
    }


def levenshtein_distance(a, b):
    matrix = [[0] * (len(a) + 1) for _ in range(len(b) + 1)]
    for i in range(len(b) + 1):
        matrix[i][0] = i
    for j in range(len(a) + 1):
        matrix[0][j] = j
    for i in range(1, len(b) + 1):
        for j in range(1, len(a) + 1):
            if b[i - 1] == a[j - 1]:
                matrix[i][j] = matrix[i - 1][j - 1]
            else:
                matrix[i][j] = min(
                    matrix[i - 1][j - 1] + 1,
                    matrix[i][j - 1] + 1,
                    matrix[i - 1][j] + 1,
                )
    return matrix[len(b)][len(a)]


def check_collision(name, cast):
    result = {
        'has_collision': False,
        'severity': "none",
        'issues': [],
        'similar_to': [],
    }
    profile = analyze_sound_profile(name)
    name_lower = name.lower()
    name_parts = name_lower.split()
    first_name = name_parts[0]
    last_name = name_parts[-1] if len(name_parts) > 1 else None
    for character in cast['characters']:
        char_lower = character['name'].lower()
        char_parts = char_lower.split()
        char_first = char_parts[0]
        char_last = char_parts[-1] if len(char_parts) > 1 else None
        if name_lower == char_lower:
            result['has_collision'] = True
            result['severity'] = "high"
            result['issues'].append("Exact match with existing character")
            result['similar_to'].append(character['name'])
            continue
        char_profile = character.get('soundProfile', {})
        char_starts_with = char_profile.get('startsWith', '')
        if profile['startsWith'] == char_starts_with:
            char_syllables = char_profile.get('syllables', 0)
            if abs(profile['syllables'] - char_syllables) <= 1:
                result['has_collision'] = True
                if result['severity'] != "high":
                    result['severity'] = "warning"
                result['issues'].append(
                    f"Same first initial '{profile['startsWith'].upper()}' with similar syllable count"
                )
                result['similar_to'].append(character['name'])
        if last_name and char_last and last_name == char_last:
            result['has_collision'] = True
            result['severity'] = "high"
            result['issues'].append(f"Same surname '{last_name}'")
            if character['name'] not in result['similar_to']:
                result['similar_to'].append(character['name'])
        if levenshtein_distance(first_name, char_first) <= 2 and first_name != char_first:
            result['has_collision'] = True
            if result['severity'] != "high":
                result['severity'] = "warning"
            result['issues'].append(f"Very similar to '{char_first}' (small edit distance)")
            if character['name'] not in result['similar_to']:
                result['similar_to'].append(character['name'])
        char_ends_with = char_profile.get('endsWith', '')
        if (
            profile['startsWith'] == char_starts_with
            and profile['endsWith'] == char_ends_with
            and character['name'] not in result['similar_to']
        ):
            result['has_collision'] = True
            if result['severity'] != "high":
                result['severity'] = "warning"
            result['issues'].append("Same start and end sounds")
            result['similar_to'].append(character['name'])
    result['issues'] = list(dict.fromkeys(result['issues']))
    result['similar_to'] = list(dict.fromkeys(result['similar_to']))
    return result


def get_default_cast_path():
    return "cast-tracker.json"


def load_cast(path):
    try:
        with open(path, 'r', encoding='utf-8') as f:
            return json.loads(f.read())
    except Exception:
        return None


def save_cast(path, cast):
    cast['_meta']['updated'] = date.today().isoformat()
    with open(path, 'w', encoding='utf-8') as f:
        f.write(json.dumps(cast, indent=2))


def create_new_cast(project_name):
    today = date.today().isoformat()
    return {
        '_meta': {
            'project': project_name,
            'created': today,
            'updated': today,
            'version': '1.0',
        },
        'characters': [],
        'usedSurnames': [],
        'usedGivenNames': [],
        'culturalDistribution': {},
    }


def cmd_init(project_name, cast_path):
    existing = load_cast(cast_path)
    if existing:
        print(f"Error: Cast file already exists at {cast_path}", file=sys.stderr)
        print("Delete it first or use a different path with --file", file=sys.stderr)
        sys.exit(1)
    cast = create_new_cast(project_name)
    save_cast(cast_path, cast)
    print(f'Created cast tracker for "{project_name}" at {cast_path}')


def cmd_add(name, cast_path, role=None, culture=None, notes=None):
    cast = load_cast(cast_path)
    if not cast:
        print(f"Error: Cast file not found at {cast_path}", file=sys.stderr)
        print('Run \'cast_tracker.py init "Project Name"\' first', file=sys.stderr)
        sys.exit(1)
    collision = check_collision(name, cast)
    if collision['severity'] == "high":
        print("Error: High collision risk with existing characters:", file=sys.stderr)
        for issue in collision['issues']:
            print(f"  - {issue}", file=sys.stderr)
        print(f"  Similar to: {', '.join(collision['similar_to'])}", file=sys.stderr)
        print("\nUse --force to add anyway, or choose a different name.", file=sys.stderr)
        sys.exit(1)
    if collision['severity'] == "warning":
        print("Warning: Potential collision with existing characters:")
        for issue in collision['issues']:
            print(f"  - {issue}")
        print(f"  Similar to: {', '.join(collision['similar_to'])}")
        print("")
    profile = analyze_sound_profile(name)
    character = {
        'name': name,
        'role': role,
        'culture': culture,
        'soundProfile': profile,
        'addedAt': date.today().isoformat(),
        'notes': notes,
    }
    cast['characters'].append(character)
    name_parts = name.split()
    if len(name_parts) > 1:
        cast['usedSurnames'].append(name_parts[-1])
    cast['usedGivenNames'].append(name_parts[0])
    if culture:
        cast['culturalDistribution'][culture] = cast['culturalDistribution'].get(culture, 0) + 1
    save_cast(cast_path, cast)
    print(f'Added "{name}" to cast')
    if role:
        print(f"  Role: {role}")
    if culture:
        print(f"  Culture: {culture}")


def cmd_check(name, cast_path):
    cast = load_cast(cast_path)
    if not cast:
        print(f"Error: Cast file not found at {cast_path}", file=sys.stderr)
        sys.exit(1)
    collision = check_collision(name, cast)
    if collision['severity'] == "none":
        print(f'"{name}" has no collisions with existing cast.')
    elif collision['severity'] == "warning":
        print(f'"{name}" has potential collisions (warning):')
        for issue in collision['issues']:
            print(f"  - {issue}")
        print(f"  Similar to: {', '.join(collision['similar_to'])}")
    else:
        print(f'"{name}" has HIGH collision risk:')
        for issue in collision['issues']:
            print(f"  - {issue}")
        print(f"  Similar to: {', '.join(collision['similar_to'])}")


def cmd_distribution(cast_path):
    cast = load_cast(cast_path)
    if not cast:
        print(f"Error: Cast file not found at {cast_path}", file=sys.stderr)
        sys.exit(1)
    print(f'Cast Distribution for "{cast["_meta"]["project"]}"')
    print(f"Total characters: {len(cast['characters'])}")
    print("")
    if not cast['culturalDistribution']:
        print("Cultural distribution: (no cultures recorded)")
        print("Use --culture when adding characters to track distribution.")
    else:
        print("Cultural distribution:")
        sorted_dist = sorted(cast['culturalDistribution'].items(), key=lambda x: x[1], reverse=True)
        for culture, count in sorted_dist:
            pct = round(count / len(cast['characters']) * 100)
            print(f"  {culture}: {count} ({pct}%)")
    print("")
    print("First initial usage:")
    initials = {}
    for char in cast['characters']:
        profile = char.get('soundProfile', {})
        initial = profile.get('startsWith', '?').upper()
        initials[initial] = initials.get(initial, 0) + 1
    sorted_initials = sorted(initials.items(), key=lambda x: x[1], reverse=True)
    for initial, count in sorted_initials:
        if count > 1:
            print(f"  {initial}: {count} characters (collision risk)")
        else:
            print(f"  {initial}: {count} character")


def cmd_list(cast_path):
    cast = load_cast(cast_path)
    if not cast:
        print(f"Error: Cast file not found at {cast_path}", file=sys.stderr)
        sys.exit(1)
    print(f'Cast for "{cast["_meta"]["project"]}"')
    print("")
    if not cast['characters']:
        print("(no characters yet)")
    else:
        for char in cast['characters']:
            line = f"- {char['name']}"
            if char.get('role'):
                line += f" [{char['role']}]"
            if char.get('culture'):
                line += f" ({char['culture']})"
            print(line)


def cmd_suggest(cast_path):
    cast = load_cast(cast_path)
    if not cast:
        print(f"Error: Cast file not found at {cast_path}", file=sys.stderr)
        sys.exit(1)
    print("Suggestions for avoiding collision:\n")
    initials = {}
    for char in cast['characters']:
        profile = char.get('soundProfile', {})
        initial = profile.get('startsWith', '?').upper()
        initials[initial] = initials.get(initial, 0) + 1
    overused = [initial for initial, count in initials.items() if count > 1]
    if overused:
        print(f"Avoid first initials: {', '.join(overused)}")
    all_initials = list("ABCDEFGHIJKLMNOPQRSTUVWXYZ")
    unused = [i for i in all_initials if i not in initials]
    print(f"Available first initials: {', '.join(unused)}")
    if cast['culturalDistribution']:
        print("")
        total = len(cast['characters'])
        underrepresented = [
            culture for culture, count in cast['culturalDistribution'].items()
            if count / total < 0.2
        ]
        if underrepresented:
            print(f"Consider adding more: {', '.join(underrepresented)}")


def main():
    args = sys.argv[1:]
    if '--help' in args or '-h' in args or not args:
        print("Cast Tracker - Manage character name collision detection\n")
        print("Usage:")
        print("  python cast_tracker.py <command> [options]\n")
        print("Commands:")
        print("  init <project>     Create new cast tracker file")
        print("  add <name>         Add character to cast")
        print("  check <name>       Check if name collides with existing cast")
        print("  list               List all characters in cast")
        print("  distribution       Show cultural and initial distribution")
        print("  suggest            Get suggestions for avoiding collisions\n")
        print("Options:")
        print("  --file <path>      Path to cast file (default: cast-tracker.json)")
        print("  --role <role>      Character role (for 'add' command)")
        print("  --culture <name>   Cultural background (for 'add' command)")
        print("  --notes <text>     Additional notes (for 'add' command)")
        print("  --force            Add despite collision warnings")
        sys.exit(0)
    file_index = args.index('--file') if '--file' in args else -1
    cast_path = args[file_index + 1] if file_index != -1 else get_default_cast_path()
    command = args[0]
    if command == "init":
        project_name = args[1] if len(args) > 1 and not args[1].startswith('--') else None
        if not project_name:
            print('Error: Project name required.', file=sys.stderr)
            sys.exit(1)
        cmd_init(project_name, cast_path)
    elif command == "add":
        name = args[1] if len(args) > 1 and not args[1].startswith('--') else None
        if not name:
            print('Error: Character name required.', file=sys.stderr)
            sys.exit(1)
        role_index = args.index('--role') if '--role' in args else -1
        culture_index = args.index('--culture') if '--culture' in args else -1
        notes_index = args.index('--notes') if '--notes' in args else -1
        cmd_add(
            name,
            cast_path,
            role=args[role_index + 1] if role_index != -1 else None,
            culture=args[culture_index + 1] if culture_index != -1 else None,
            notes=args[notes_index + 1] if notes_index != -1 else None,
        )
    elif command == "check":
        name = args[1] if len(args) > 1 and not args[1].startswith('--') else None
        if not name:
            print('Error: Name required.', file=sys.stderr)
            sys.exit(1)
        cmd_check(name, cast_path)
    elif command == "list":
        cmd_list(cast_path)
    elif command == "distribution":
        cmd_distribution(cast_path)
    elif command == "suggest":
        cmd_suggest(cast_path)
    else:
        print(f"Unknown command: {command}", file=sys.stderr)
        print("Use --help to see available commands", file=sys.stderr)
        sys.exit(1)


if __name__ == '__main__':
    main()
