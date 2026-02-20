#!/usr/bin/env python3
"""genre_elements.py - Random genre-specific element generator"""

import sys
import os
import json
import random


def load_data():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    data_path = os.path.join(script_dir, '..', 'data', 'genre-elements.json')
    with open(data_path, 'r', encoding='utf-8') as f:
        return json.load(f)


def get_genres(data):
    return data['_meta']['genres']


def get_genre_data(data, genre):
    gd = data.get(genre)
    if gd and 'categories' in gd:
        return gd
    return None


def get_all_elements(genre_data):
    all_items = []
    for items in genre_data['categories'].values():
        all_items.extend(items)
    return all_items


def random_from(arr, count=1):
    shuffled = arr[:]
    random.shuffle(shuffled)
    return shuffled[:min(count, len(arr))]


def main():
    args = sys.argv[1:]
    if '--help' in args or '-h' in args:
        print('Genre Elements Generator')
        print('Usage:')
        print('  python genre_elements.py <genre>           # Random element')
        print('  python genre_elements.py <genre> --count N # N elements')
        print('  python genre_elements.py --list             # Show genres')
        print('  python genre_elements.py --combo g1,g2     # One from each')
        sys.exit(0)
    data = load_data()
    genres = get_genres(data)
    json_out = '--json' in args
    if '--list' in args:
        li = args.index('--list')
        specific = args[li+1] if li+1 < len(args) and args[li+1] in genres else None
        if specific:
            gd = get_genre_data(data, specific)
            if gd:
                print(chr(10) + 'Categories for ' + specific + ':' + chr(10))
                for cat, items in gd['categories'].items():
                    print('  {} ({} items)'.format(cat.ljust(25), len(items)))
        else:
            print(chr(10) + 'Available elemental genres:' + chr(10))
            for genre in genres:
                gd = get_genre_data(data, genre)
                if gd:
                    total = sum(len(v) for v in gd['categories'].values())
                    print('  {} - {}... ({} items)'.format(genre.ljust(15), gd['core_promise'][:50], total))
        sys.exit(0)

    if '--info' in args:
        ii = args.index('--info')
        genre = args[ii+1] if ii+1 < len(args) else None
        if not genre or genre not in genres:
            print('Error: Specify a valid genre', file=sys.stderr)
            sys.exit(1)
        gd = get_genre_data(data, genre)
        if gd:
            print(chr(10) + '## ' + genre.capitalize())
            print('Core promise: ' + gd['core_promise'])
            print('Required: ' + ', '.join(gd['required_elements']))
            print('Categories:')
            for cat in gd['categories']: print('  - ' + cat)
        sys.exit(0)

    if '--combo' in args:
        ci = args.index('--combo')
        combo_genres = args[ci+1].split(',') if ci+1 < len(args) else []
        result = {}
        for g in combo_genres:
            g = g.strip()
            gd = get_genre_data(data, g)
            if gd:
                result[g] = random_from(get_all_elements(gd), 1)[0]
        if json_out:
            print(json.dumps(result, indent=2))
        else:
            print(chr(10) + 'Genre combo:' + chr(10))
            for g, e in result.items(): print('  {}: {}'.format(g, e))
        sys.exit(0)

    # Parse count and category
    count = int(args[args.index('--count') + 1]) if '--count' in args else 1
    category = args[args.index('--category') + 1] if '--category' in args else None
    # Find genre
    skip = set()
    for flag in ['--count', '--category', '--json']:
        if flag in args:
            idx = args.index(flag)
            skip.add(idx)
            if flag != '--json': skip.add(idx + 1)
    genre = None
    for i, a in enumerate(args):
        if i not in skip and not a.startswith('--'):
            genre = a
            break
    if not genre or genre not in genres:
        print('Error: Specify a valid genre. Use --list to see options.', file=sys.stderr)
        sys.exit(1)
    gd = get_genre_data(data, genre)
    if not gd:
        print('Error: Could not load data for genre', file=sys.stderr)
        sys.exit(1)
    if category:
        if category not in gd['categories']:
            print('Error: Unknown category. Available: ' + ', '.join(gd['categories'].keys()), file=sys.stderr)
            sys.exit(1)
        pool = gd['categories'][category]
    else:
        pool = get_all_elements(gd)
    selected = random_from(pool, count)
    if json_out:
        print(json.dumps(selected, indent=2))
    elif count == 1:
        print(selected[0])
    else:
        for item in selected: print('- ' + item)


if __name__ == '__main__':
    main()
