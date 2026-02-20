#!/usr/bin/env python3

"""
Function-Form Generator

Works with abstract story functions and setting-specific forms.
Select a function for story role, then instantiate with setting-appropriate form.

Usage:
  python functions.py                    # Random function + form
  python functions.py --setting scifi    # Random function, scifi form
  python functions.py healer             # Specific function, random setting
  python functions.py healer --setting fantasy  # Specific both
  python functions.py --list             # List all functions
  python functions.py --list-settings    # List all settings
  python functions.py --count 3          # Multiple random results
"""

import sys
import os
import json
import random


# Ensure UTF-8 output on all platforms
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")
if hasattr(sys.stderr, "reconfigure"):
    sys.stderr.reconfigure(encoding="utf-8")


def random_from(arr: list, count: int = 1) -> list:
    shuffled = arr[:]
    random.shuffle(shuffled)
    return shuffled[:min(count, len(arr))]


def generate_result(data: dict, function_name: str | None, setting: str | None) -> dict:
    func_names = list(data["functions"].keys())
    selected_func = function_name or random_from(func_names, 1)[0]
    func_data = data["functions"].get(selected_func)

    if not func_data:
        raise ValueError(f"Unknown function: {selected_func}")

    selected_setting = setting or random_from(data["settings"], 1)[0]

    if selected_setting not in data["settings"]:
        raise ValueError(f"Unknown setting: {selected_setting}")

    forms = func_data["forms"].get(selected_setting, [])
    if not forms:
        raise ValueError(f"No forms for {selected_func} in {selected_setting}")

    selected_form = random_from(forms, 1)[0]

    return {
        "function": selected_func,
        "description": func_data["description"],
        "story_access": func_data["story_access"],
        "setting": selected_setting,
        "form": selected_form,
    }


def format_result(result: dict) -> str:
    lines = []
    lines.append(f"## {result['form']}")
    lines.append(f"Function: {result['function']} ({result['setting']})")
    lines.append(f"Role: {result['description']}")
    sa = ", ".join(result["story_access"])
    lines.append(f"Story access: {sa}")
    return '\n'.join(lines)


def format_brief(result: dict) -> str:
    return f"{result['form']} [{result['function']}/{result['setting']}]"


def main() -> None:
    args = sys.argv[1:]

    if "--help" in args or "-h" in args:
        print("""Function-Form Generator

Works with abstract story functions and setting-specific forms.

Usage:
  python functions.py                    # Random function + form
  python functions.py --setting scifi    # Random function, scifi form
  python functions.py healer             # Specific function
  python functions.py healer --setting fantasy
  python functions.py --list             # List all functions
  python functions.py --list-settings    # List all settings
  python functions.py --count 3          # Multiple results
  python functions.py --brief            # Short output format

Options:
  --setting S    Use specific setting (contemporary, historical, fantasy, scifi, postapoc)
  --count N      Generate N results
  --brief        Short output (just form and tags)
  --json         Output as JSON
  --list         List all available functions
  --list-settings List all settings""")
        sys.exit(0)

    # Load data
    script_dir = os.path.dirname(os.path.abspath(__file__))
    data_path = os.path.join(script_dir, "..", "data", "functions-forms.json")

    try:
        with open(data_path, "r", encoding="utf-8") as f:
            data = json.load(f)
    except Exception as e:
        print(f"Error loading data: {e}", file=sys.stderr)
        sys.exit(1)

    # List modes
    if "--list" in args:
        print("Available functions:\n")
        for name, func in data["functions"].items():
            print(f"  {name:<20} {func['description']}")
        sys.exit(0)

    if "--list-settings" in args:
        print("Available settings:\n")
        for setting in data["settings"]:
            print(f"  {setting}")
        sys.exit(0)

    # Parse options
    json_output = "--json" in args
    brief_output = "--brief" in args

    setting_index = args.index("--setting") if "--setting" in args else -1
    setting = args[setting_index + 1] if setting_index != -1 else None

    count_index = args.index("--count") if "--count" in args else -1
    count = 1
    if count_index != -1 and count_index + 1 < len(args):
        try:
            count = int(args[count_index + 1])
        except ValueError:
            count = 1

    # Find function name (first arg that is not a flag or flag value)
    skip_indices: set[int] = set()
    if setting_index != -1:
        skip_indices.add(setting_index)
        skip_indices.add(setting_index + 1)
    if count_index != -1:
        skip_indices.add(count_index)
        skip_indices.add(count_index + 1)

    function_name: str | None = None
    for i in range(len(args)):
        if not args[i].startswith("--") and i not in skip_indices:
            function_name = args[i]
            break

    # Generate results
    results: list[dict] = []
    try:
        for i in range(count):
            results.append(generate_result(data, function_name, setting))
    except ValueError as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)

    # Output
    if json_output:
        print(json.dumps(results, indent=2))
    elif brief_output:
        for result in results:
            print(format_brief(result))
    else:
        for idx, result in enumerate(results):
            print(format_result(result))
            if len(results) > 1 and idx < len(results) - 1:
                print()


if __name__ == "__main__":
    main()
