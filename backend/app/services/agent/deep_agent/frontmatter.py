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

import yaml


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
