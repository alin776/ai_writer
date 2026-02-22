#!/usr/bin/env python3

"""
functions.py - 角色功能-形态生成器

双层随机化：先选定抽象角色功能（治疗者、执法者…），
再根据网文设定（玄幻/都市/历史/末世/游戏）实例化为具体形态。

Usage:
  python functions.py                    # 随机功能 + 形态
  python functions.py --setting xuanhuan # 随机功能，玄幻设定
  python functions.py healer             # 指定功能，随机设定
  python functions.py healer --setting xuanhuan  # 都指定
  python functions.py --list             # 列出所有功能
  python functions.py --list-settings    # 列出所有设定
  python functions.py --count 3          # 生成多个结果
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

SETTING_DISPLAY = {
    "xuanhuan": "玄幻",
    "urban": "都市",
    "historical": "历史",
    "apocalypse": "末世",
    "game": "游戏",
}


def random_from(arr: list, count: int = 1) -> list:
    shuffled = arr[:]
    random.shuffle(shuffled)
    return shuffled[:min(count, len(arr))]


def generate_result(data: dict, function_name: str | None, setting: str | None) -> dict:
    func_names = list(data["functions"].keys())
    selected_func = function_name or random_from(func_names, 1)[0]
    func_data = data["functions"].get(selected_func)

    if not func_data:
        raise ValueError("未知功能: " + selected_func)

    selected_setting = setting or random_from(data["settings"], 1)[0]

    if selected_setting not in data["settings"]:
        raise ValueError("未知设定: " + selected_setting)

    forms = func_data["forms"].get(selected_setting, [])
    if not forms:
        raise ValueError("{}在{}设定下没有可用形态".format(selected_func, selected_setting))

    selected_form = random_from(forms, 1)[0]

    return {
        "function": selected_func,
        "description": func_data["description"],
        "story_access": func_data["story_access"],
        "setting": selected_setting,
        "form": selected_form,
    }


def format_result(result: dict) -> str:
    setting_cn = SETTING_DISPLAY.get(result['setting'], result['setting'])
    lines = []
    lines.append("## " + result['form'])
    lines.append("功能: {} （{}）".format(result['function'], setting_cn))
    lines.append("角色: " + result['description'])
    sa = "、".join(result["story_access"])
    lines.append("故事切入点: " + sa)
    return '\n'.join(lines)


def format_brief(result: dict) -> str:
    setting_cn = SETTING_DISPLAY.get(result['setting'], result['setting'])
    return "{} [{}/{}]".format(result['form'], result['function'], setting_cn)


def main() -> None:
    args = sys.argv[1:]

    if "--help" in args or "-h" in args:
        print("角色功能-形态生成器")
        print()
        print("双层随机化：先选抽象功能，再根据设定实例化为具体形态。")
        print()
        print("用法:")
        print("  python functions.py                    # 随机功能 + 形态")
        print("  python functions.py --setting xuanhuan  # 随机功能，玄幻设定")
        print("  python functions.py healer              # 指定功能")
        print("  python functions.py healer --setting urban")
        print("  python functions.py --list              # 列出所有功能")
        print("  python functions.py --list-settings     # 列出所有设定")
        print("  python functions.py --count 3           # 生成多个结果")
        print("  python functions.py --brief             # 简短输出")
        print()
        print("选项:")
        print("  --setting S    指定设定 (xuanhuan/urban/historical/apocalypse/game)")
        print("  --count N      生成 N 个结果")
        print("  --brief        简短输出（仅形态和标签）")
        print("  --json         JSON 格式输出")
        print("  --list         列出所有可用功能")
        print("  --list-settings 列出所有设定")
        sys.exit(0)

    # Load data
    script_dir = os.path.dirname(os.path.abspath(__file__))
    data_path = os.path.join(script_dir, "..", "data", "functions-forms.json")

    try:
        with open(data_path, "r", encoding="utf-8") as f:
            data = json.load(f)
    except Exception as e:
        print("加载数据失败: " + str(e), file=sys.stderr)
        sys.exit(1)

    # List modes
    if "--list" in args:
        print("\n可用角色功能:\n")
        for name, func in data["functions"].items():
            print("  {:<20} {}".format(name, func['description']))
        sys.exit(0)

    if "--list-settings" in args:
        print("\n可用设定:\n")
        for setting in data["settings"]:
            display = SETTING_DISPLAY.get(setting, setting)
            print("  {} ({})".format(setting, display))
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
        print("错误: " + str(e), file=sys.stderr)
        sys.exit(1)

    # Output
    if json_output:
        print(json.dumps(results, indent=2, ensure_ascii=False))
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
