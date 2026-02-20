#!/usr/bin/env python3

"""
Entropy Injector

Randomly selects elements from curated lists to introduce creative entropy.
Breaks default patterns by forcing unexpected combinations.

Usage:
  python entropy.py lies              # Random character lie
  python entropy.py lies --count 3    # Three random lies
  python entropy.py --list            # Show available lists
  python entropy.py --combo           # Generate random combo
  python entropy.py --file data.json professions  # Use custom file
"""

import sys
import json
import random

# Ensure UTF-8 output on all platforms
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")
if hasattr(sys.stderr, "reconfigure"):
    sys.stderr.reconfigure(encoding="utf-8")


# Built-in lists for immediate use
BUILT_IN_LISTS: dict[str, list[str]] = {
    # Character lies (for character-arc skill)
    'lies': [
        "I'm not worthy of love",
        'Power is the only protection',
        'Trust leads to betrayal',
        'My value comes from achievement',
        'The world is fundamentally hostile',
        "I don't deserve happiness",
        'Being vulnerable is weakness',
        'I can only rely on myself',
        "If I'm perfect, I'll be loved",
        'My past defines my future',
        'Other people always leave',
        "I'm not smart/talented enough",
        'Asking for help is failure',
        'I must control everything',
        'Emotions are dangerous',
        "I'm fundamentally broken",
        'Success will make me happy',
        "I don't belong anywhere",
        'Love requires sacrifice of self',
        'The truth is too dangerous',
    ],

    # Ghost/wound types (backstory wounds that create lies)
    'ghosts': [
        'Parental abandonment',
        'Public humiliation',
        'Betrayal by trusted figure',
        'Failure at crucial moment',
        'Loss of loved one',
        'Witnessed something terrible',
        'Rejected by community',
        "Survivor's guilt",
        'Childhood neglect',
        'Broken promise with consequences',
        'Identity revelation (adopted, etc.)',
        'Forced to make impossible choice',
        'Trusted someone unworthy',
        'Lost something irreplaceable',
        'Discovered painful truth about self',
        'Was complicit in harm',
        "Couldn't save someone",
        'Was used by someone they loved',
        "Escaped while others didn't",
        'Chose wrong at fork in road',
    ],

    # Disaster types (for scene-sequencing skill)
    'disasters': [
        'Yes, but now a worse problem',
        'No, and the door is closed',
        'No, and they know you tried',
        'Yes, but it cost too much',
        'No, and time is running out',
        "Yes, but it's the wrong thing",
        "No, and you're exposed",
        'Yes, but someone else paid',
        "No, and you're trapped",
        'Yes, but trust is broken',
        "No, and help can't reach you",
        'Yes, but you became what you hate',
        'No, and the enemy adapts',
        'Yes, but innocent bystanders',
        'No, and your ally turns',
    ],

    # Dilemma structures (for scene-sequencing)
    'dilemmas': [
        'Save friend vs. complete mission',
        'Tell truth vs. protect someone',
        'Personal goal vs. group need',
        'Quick risky path vs. slow safe path',
        'Certain small win vs. possible big win',
        'Principle vs. pragmatism',
        'Trust new ally vs. go alone',
        'Reveal secret vs. maintain cover',
        'Confront now vs. gather evidence',
        'Mercy vs. justice',
        'Loyalty to past vs. necessity of present',
        'Self-preservation vs. moral obligation',
        'Love vs. duty',
        'Honesty vs. kindness',
        'Individual vs. many',
    ],

    # Unexpected professions (for character cliché-breaking)
    'professions': [
        'Elevator inspector',
        'Medical illustrator',
        'Voice actor for GPS systems',
        'Crime scene cleaner',
        'Ethical hacker',
        'Cult deprogrammer',
        'Prosthetic eye maker',
        'Patent examiner',
        'Foley artist',
        'Professional line-sitter',
        'Food stylist',
        'Escape room designer',
        'Wind turbine technician',
        'Crossword puzzle constructor',
        'Museum preparator',
        'Genealogist for hire',
        'Demolition consultant',
        'Wastewater treatment operator',
        'Cartographic surveyor',
        'Sleep study technician',
    ],

    # Unexpected locations (for setting cliché-breaking)
    'locations': [
        'Toll booth at 3 AM',
        'Hospital chapel',
        'Closed water park',
        'Grain silo',
        'Furniture warehouse clearance sale',
        'Nuclear power plant visitor center',
        'Taxidermy workshop',
        'Airport interfaith chapel',
        'Underground parking garage, level 7',
        'Botanical garden at closing time',
        'Self-storage facility at midnight',
        'Casino surveillance room',
        'Dental office waiting room',
        "Beekeeper's apiary",
        'Radio transmission tower base',
        'Recycling center sorting floor',
        'Meat processing plant',
        'Weather research station',
        'Dog show grooming area',
        'Construction site trailer',
    ],

    # Orthogonal collisions (for cliche-transcendence)
    'collisions': [
        "Their investigation accidentally overlaps with protagonist's secret",
        "They're solving a completely different case that uses same evidence",
        "Their mundane job puts them in protagonist's path repeatedly",
        "They're looking for someone else who happens to be with protagonist",
        'Their personal vendetta targets someone protagonist needs',
        "They have information they don't know is valuable",
        'They witnessed something they misinterpreted',
        'Their hobby intersects with the mystery',
        "They're enforcing a rule that blocks protagonist for boring reasons",
        'They want the same resource for completely different reasons',
        "They're cleaning up someone else's mess and protagonist is evidence",
        "They're testing equipment that detects protagonist's secret",
        "They're writing a story and researching the protagonist's situation",
        "They're a former victim of something adjacent to protagonist's problem",
        "They're running a scam that accidentally mimics the real conspiracy",
    ],

    # Scene openings (for drafting prompts)
    'openings': [
        "In the middle of an argument that's clearly been going for hours",
        "Someone arriving where they're not supposed to be",
        "Two people pretending they don't know each other",
        'The aftermath of violence, not the violence itself',
        "A routine that's about to be broken",
        'Someone working while processing bad news',
        'A forced politeness between enemies',
        'The moment before a reveal',
        'Someone doing their job badly because distracted',
        'Two conversations happening simultaneously',
        'Someone waiting and trying not to show impatience',
        'A goodbye that might be final',
        'Discovery of something that changes everything',
        'The last normal moment before disruption',
        'Someone maintaining composure while falling apart',
    ],

}


def random_from(arr: list, count: int = 1) -> list:
    shuffled = arr[:]
    random.shuffle(shuffled)
    return shuffled[:min(count, len(arr))]


def generate_combo(lists: dict[str, list[str]]) -> dict[str, str]:
    combo: dict[str, str] = {}
    for name, items in lists.items():
        combo[name] = random_from(items, 1)[0]
    return combo


def load_external_lists(filepath: str) -> dict[str, list[str]]:
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception as e:
        print(f'Error loading {filepath}: {e}', file=sys.stderr)
        sys.exit(1)


def main() -> None:
    args = sys.argv[1:]

    if '--help' in args or '-h' in args:
        print("""
Entropy Injector - Random elements for creative work

Usage:
  python entropy.py <list-name>           # Random element
  python entropy.py <list-name> --count N # N random elements
  python entropy.py --list                # Show available lists
  python entropy.py --combo               # One from each list
  python entropy.py --combo-small         # Subset combo
  python entropy.py --file custom.json <list>  # Custom lists

Built-in lists:
  lies        - Character false beliefs (for arcs)
  ghosts      - Backstory wounds
  disasters   - Scene endings
  dilemmas    - Choice structures
  professions - Unexpected jobs
  locations   - Unusual places
  collisions  - Orthogonal intersections
  openings    - Scene start prompts

Options:
  --count N   Return N random items
  --json      Output as JSON
  --list      Show all available lists
  --combo     Generate one item from each list
  --file F    Load additional lists from JSON file
""")
        sys.exit(0)

    lists = {**BUILT_IN_LISTS}

    # Load external file if specified
    file_index = args.index('--file') if '--file' in args else -1
    if file_index != -1 and file_index + 1 < len(args):
        external = load_external_lists(args[file_index + 1])
        lists = {**lists, **external}

    json_output = '--json' in args

    # Show available lists
    if '--list' in args:
        print('Available lists:' + '\n')
        for name, items in lists.items():
            print(f'  {name:<15} ({len(items)} items)')
        sys.exit(0)

    # Generate combo from all or subset of lists
    if '--combo' in args:
        combo = generate_combo(lists)
        if json_output:
            print(json.dumps(combo, indent=2))
        else:
            print('Random combination:' + '\n')
            for name, value in combo.items():
                print(f'  {name}: {value}')
        sys.exit(0)

    if '--combo-small' in args:
        small = {
            'lies': lists['lies'],
            'disasters': lists['disasters'],
            'locations': lists['locations'],
        }
        combo = generate_combo(small)
        if json_output:
            print(json.dumps(combo, indent=2))
        else:
            print('Random seed:' + '\n')
            for name, value in combo.items():
                print(f'  {name}: {value}')
        sys.exit(0)

    # Get count
    count_index = args.index('--count') if '--count' in args else -1
    count = 1
    if count_index != -1 and count_index + 1 < len(args):
        try:
            count = int(args[count_index + 1])
        except ValueError:
            count = 1

    # Build set of arg indices to skip
    skip_indices: set[int] = set()
    if file_index != -1:
        skip_indices.add(file_index)
        skip_indices.add(file_index + 1)
    if count_index != -1:
        skip_indices.add(count_index)
        skip_indices.add(count_index + 1)

    # Get specific list name
    list_name = None
    for i in range(len(args)):
        if not args[i].startswith('--') and i not in skip_indices:
            list_name = args[i]
            break

    if not list_name:
        print('Error: No list specified. Use --list to see options.', file=sys.stderr)
        sys.exit(1)

    if list_name not in lists:
        print(f'Error: Unknown list "{list_name}". Use --list to see options.', file=sys.stderr)
        sys.exit(1)

    selected = random_from(lists[list_name], count)

    if json_output:
        print(json.dumps(selected, indent=2))
    else:
        if count == 1:
            print(selected[0])
        else:
            for item in selected:
                print(f'• {item}')


if __name__ == '__main__':
    main()
