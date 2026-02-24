#!/usr/bin/env python3
"""
列表验证器

分析 JSON 列表的质量指标：
- 规模 / 成熟度等级
- 重复项
- 条目长度分布
- 具体性评分

语言无关：适用于任何文本内容（中文、英文等）

用法：
  python validate_list.py list.json
  python validate_list.py data.json list_name
  python validate_list.py list.json --json
"""

import sys
import os
import json


def validate_list(items: list[str], list_name: str) -> dict:
    """验证字符串列表并返回质量报告。"""

    # ── 重复检测 ──
    seen: set[str] = set()
    duplicates: list[str] = []
    for item in items:
        normalized = item.strip().lower()
        if normalized in seen:
            duplicates.append(item)
        seen.add(normalized)

    unique_count = len(seen)

    # ── 长度统计 ──
    lengths = [len(item) for item in items]
    avg_length = sum(lengths) / len(lengths) if lengths else 0
    min_length = min(lengths) if lengths else 0
    max_length = max(lengths) if lengths else 0

    short_items = [item for item in items if len(item) < 10][:5]
    long_items = [item for item in items if len(item) > 100][:5]

    # 具体性：处于理想 20-60 字符范围的条目
    ideal_count = sum(1 for item in items if 20 <= len(item) <= 60)
    specificity_score = round((ideal_count / len(items)) * 100) if items else 0

    maturity = maturity_assessment(unique_count)

    # ── 问题与建议 ──
    issues: list[str] = []
    suggestions: list[str] = []

    if duplicates:
        issues.append(f"发现 {len(duplicates)} 个重复项")
        suggestions.append("移除重复条目")

    if maturity["level"] == "starter":
        issues.append(f"入门级（{unique_count} 条目）— 未达生产标准")
        suggestions.append(
            f"添加 {maturity['items_needed']} 个唯一条目"
            f"以达到{maturity['next_level']}"
        )
    elif maturity["next_level"]:
        suggestions.append(
            f"添加 {maturity['items_needed']} 个条目"
            f"以达到{maturity['next_level']}"
        )

    if specificity_score < 30:
        issues.append(
            f"具体性评分偏低（{specificity_score}%）"
            "— 条目可能太模糊或太复杂"
        )
        suggestions.append(
            "目标条目长度 20-60 字符以获得最佳具体性"
        )

    if len(short_items) > len(items) * 0.2:
        issues.append("大量条目过短（< 10 字符）")
        suggestions.append("过短的条目可能太模糊 — 增加具体性")

    if len(long_items) > len(items) * 0.1:
        issues.append("部分条目过长（> 100 字符）")
        suggestions.append("过长的条目可能难以使用 — 考虑拆分")

    return {
        "listName": list_name,
        "totalItems": len(items),
        "uniqueItems": unique_count,
        "duplicates": duplicates,
        "avgLength": round(avg_length, 1),
        "minLength": min_length,
        "maxLength": max_length,
        "shortItems": short_items,
        "longItems": long_items,
        "specificityScore": specificity_score,
        "maturityLevel": maturity["level"],
        "nextLevel": maturity["next_level"],
        "itemsNeededForNext": maturity["items_needed"],
        "issues": issues,
        "suggestions": suggestions,
    }


def maturity_assessment(unique_count: int) -> dict:
    """根据唯一条目数评估列表成熟度。

    返回包含 level、next_level、items_needed 的字典
    """
    if unique_count < 30:
        return {"level": "starter", "next_level": "functional",
                "items_needed": 30 - unique_count}
    elif unique_count < 75:
        return {"level": "functional", "next_level": "production",
                "items_needed": 75 - unique_count}
    elif unique_count < 150:
        return {"level": "production", "next_level": "comprehensive",
                "items_needed": 150 - unique_count}
    else:
        return {"level": "comprehensive", "next_level": None,
                "items_needed": 0}


def format_report(report: dict) -> str:
    """将验证报告格式化为可读文本。"""
    lines: list[str] = []

    lines.append(f"# 列表验证：{report['listName']}\n")

    # 成熟度
    emoji_map = {
        "comprehensive": "★", "production": "✓",
        "functional": "~", "starter": "⚠",
    }
    desc_map = {
        "comprehensive": "参考级质量（150+）",
        "production": "生产就绪（75-150）",
        "functional": "可用但有限（30-75）",
        "starter": "仅为入门示例（< 30）",
    }
    level = report["maturityLevel"]
    lines.append("## 成熟度等级")
    lines.append(f"{emoji_map.get(level, '?')} **{level.upper()}** - {desc_map.get(level, '')}")
    lines.append(f"   {report['uniqueItems']} 个唯一条目")
    if report["nextLevel"]:
        lines.append(f"   → 还需 {report['itemsNeededForNext']} 个条目达到 {report['nextLevel']}")
    if report["duplicates"]:
        lines.append(f"   ⚠ 发现 {len(report['duplicates'])} 个重复项")
    lines.append("")

    # 具体性
    score = report["specificityScore"]
    spec_emoji = "✓" if score >= 50 else ("~" if score >= 30 else "⚠")
    lines.append("## 具体性")
    lines.append(f"{spec_emoji} 评分：{score}%（处于理想 20-60 字符范围的条目）")
    lines.append(f"   平均长度：{report['avgLength']} 字符"
                 f"（范围：{report['minLength']}-{report['maxLength']}）")
    if report["shortItems"]:
        preview = "、".join(report["shortItems"][:3])
        more = "…" if len(report["shortItems"]) > 3 else ""
        lines.append(f"   过短条目（< 10 字符）：{preview}{more}")
    if report["longItems"]:
        lines.append(f"   过长条目（> 100 字符）：发现 {len(report['longItems'])} 个")
    lines.append("")

    # 问题
    if report["issues"]:
        lines.append("## 问题")
        for issue in report["issues"]:
            lines.append(f"- ⚠ {issue}")
        lines.append("")

    # 建议
    if report["suggestions"]:
        lines.append("## 建议")
        for s in report["suggestions"]:
            lines.append(f"- {s}")
        lines.append("")

    # 评估
    if not report["issues"]:
        lines.append("## 评估")
        lines.append("✓ 列表通过验证检查\n")

    return "\n".join(lines)


# ── 命令行接口 ──

def main() -> None:
    args = sys.argv[1:]

    if "--help" in args or "-h" in args:
        print(
            "列表验证器 - 检查列表质量\n\n"
            "用法：\n"
            "  python validate_list.py <file.json>\n"
            "  python validate_list.py <file.json> <list_name>\n"
            "  python validate_list.py <file.json> --json\n\n"
            "选项：\n"
            "  --json    以 JSON 格式输出\n"
            "  --help    显示此帮助\n"
        )
        sys.exit(0)

    json_output = "--json" in args
    file_path = next((a for a in args if a.endswith(".json")), None)
    list_name = next(
        (a for a in args if not a.startswith("--") and not a.endswith(".json")),
        None,
    )

    if not file_path:
        print("错误：未指定 JSON 文件", file=sys.stderr)
        sys.exit(1)

    if not os.path.isfile(file_path):
        print(f"错误：文件未找到：{file_path}", file=sys.stderr)
        sys.exit(1)

    with open(file_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    reports: list[dict] = []

    if isinstance(data, list):
        reports.append(validate_list(data, file_path))
    elif isinstance(data, dict):
        if list_name:
            if list_name not in data:
                print(f"错误：在 {file_path} 中未找到列表 \"{list_name}\"",
                      file=sys.stderr)
                print(f"可用列表：{', '.join(data.keys())}", file=sys.stderr)
                sys.exit(1)
            reports.append(validate_list(data[list_name], list_name))
        else:
            for name, items in data.items():
                if isinstance(items, list):
                    reports.append(validate_list(items, name))
    else:
        print("错误：文件必须包含 JSON 数组或对象", file=sys.stderr)
        sys.exit(1)

    if json_output:
        print(json.dumps(reports, ensure_ascii=False, indent=2))
    else:
        for i, report in enumerate(reports):
            print(format_report(report))
            if len(reports) > 1 and i < len(reports) - 1:
                print("---\n")


if __name__ == "__main__":
    main()
