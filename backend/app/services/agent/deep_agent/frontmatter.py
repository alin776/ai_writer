"""
Frontmatter 解析工具

解析和构建章节 Markdown 文件的 YAML frontmatter。
章节文件格式：
    ---
    title: 黎明
    status: draft
    ---

    正文内容...
"""

import re

import yaml

# Windows 保留文件名（大小写不敏感）
_WINDOWS_RESERVED = frozenset(
    ["CON", "PRN", "AUX", "NUL"]
    + [f"COM{i}" for i in range(1, 10)]
    + [f"LPT{i}" for i in range(1, 10)]
)


def sanitize_title(title: str) -> str:
    """移除文件名不安全字符，保留中文/字母/数字/连字符"""
    safe = re.sub(r'[^\w\u4e00-\u9fff\-]', '', title)
    safe = safe[:50] or "untitled"
    if safe.upper() in _WINDOWS_RESERVED:
        safe = f"_{safe}"
    return safe


def chapter_filename(num: int, title: str) -> str:
    """构建章节文件名：01-考核之日.md"""
    return f"{num:02d}-{sanitize_title(title)}.md"


def parse_chapter(content: str) -> dict:
    """分离 YAML frontmatter 和正文。

    Args:
        content: 完整的章节 Markdown 文件内容

    Returns:
        {"title": str, "status": str, "content": str, "word_count": int}
    """
    title = ""
    status = "draft"
    body = content

    if content.startswith("---"):
        parts = content.split("---", 2)
        # parts[0] 是空字符串（--- 之前），parts[1] 是 YAML，parts[2] 是正文
        if len(parts) >= 3:
            try:
                meta = yaml.safe_load(parts[1]) or {}
            except yaml.YAMLError:
                meta = {}
            title = meta.get("title", "")
            status = meta.get("status", "draft")
            body = parts[2].lstrip("\n")

    word_count = len(body.replace("\n", "").replace(" ", ""))
    return {
        "title": title,
        "status": status,
        "content": body,
        "word_count": word_count,
    }


def build_chapter(title: str, status: str, content: str) -> str:
    """构建带 frontmatter 的章节文件内容。

    Args:
        title: 章节标题
        status: 章节状态（draft/completed）
        content: 正文内容

    Returns:
        完整的 Markdown 文件内容（frontmatter + 正文）
    """
    meta = yaml.dump(
        {"title": title, "status": status},
        allow_unicode=True,
        default_flow_style=False,
    ).strip()
    return f"---\n{meta}\n---\n\n{content}"
