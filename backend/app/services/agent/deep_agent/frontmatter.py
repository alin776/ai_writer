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


def _strip_leaked_frontmatter(body: str) -> str:
    """清理正文中意外嵌入的 frontmatter 残留。

    处理以下情况（循环清理，支持多层嵌套）：
    1. 带 --- 分隔符的完整 frontmatter（如 ---\\nstatus: draft\\ntitle: x\\n---）
    2. Milkdown 损坏的 frontmatter：编辑器将 --- 转换为 ***、___、--------- 等
       Markdown thematic break，导致 frontmatter 无法被正常解析
    3. 不带前导分隔符的 YAML 残留 + 关闭分隔符（如 status: draft\\ntitle: x\\n---）
    4. 不带任何分隔符的纯 YAML 元数据残留（如 status: draft\\ntitle: x）
    """
    # Markdown thematic break：3 个以上 *、-、_ 字符
    _TB = r'[*_-]{3,}'

    while True:
        stripped = body.lstrip("\n")

        # 情况 1：带 --- 分隔符的完整 frontmatter 嵌入
        # 仅当首行恰好是 "---" 时使用 split 解析（避免 --------- 等长序列被错误拆分）
        if stripped.startswith("---"):
            first_nl = stripped.find("\n")
            first_line = stripped[:first_nl].strip() if first_nl >= 0 else stripped.strip()
            if first_line == "---":
                parts = stripped.split("---", 2)
                if len(parts) >= 3:
                    try:
                        meta = yaml.safe_load(parts[1]) or {}
                        if isinstance(meta, dict) and ("title" in meta or "status" in meta):
                            body = parts[2].lstrip("\n")
                            continue
                    except yaml.YAMLError:
                        pass

        # 情况 2：Milkdown 损坏的 frontmatter
        # 编辑器将 --- 转换为 ***、___、--------- 等 thematic break
        # 模式：thematic_break \n+ YAML行 \n thematic_break（可选）
        corrupted_match = re.match(
            r'^' + _TB + r'[ \t]*\n+'
            r'((?:(?:title|status):[^\n]*\n)+)'
            r'(?:' + _TB + r'[ \t]*\n?)?',
            stripped,
        )
        if corrupted_match:
            yaml_text = corrupted_match.group(1)
            has_title = 'title:' in yaml_text
            has_known_status = bool(re.search(
                r'\bstatus:\s*(?:draft|completed|published|archived)',
                yaml_text,
            ))
            if has_title or has_known_status:
                body = stripped[corrupted_match.end():].lstrip("\n")
                continue

        # 情况 3：不带前导分隔符的 YAML 残留 + 关闭分隔符
        fm_match = re.match(
            r'^((?:(?:title|status):[^\n]*\n)+)' + _TB + r'[ \t]*\n?',
            stripped,
        )
        if fm_match:
            body = stripped[fm_match.end():].lstrip("\n")
            continue

        # 情况 4：不带任何分隔符的纯 YAML 元数据残留（如 status: draft\ntitle: x）
        # 必须同时包含 title 和 status 行才视为残留，且 status 必须为已知值，
        # 避免误清理用户正文中恰好以 "title:"/"status:" 开头的文本
        bare_fm_match = re.match(
            r'^((?:(?:title|status):[^\n]*\n?)+)',
            stripped,
        )
        if bare_fm_match:
            matched_text = bare_fm_match.group(1)
            has_title = 'title:' in matched_text
            has_known_status = bool(re.search(
                r'\bstatus:\s*(?:draft|completed|published|archived)\s*$',
                matched_text, re.MULTILINE,
            ))
            if has_title and has_known_status:
                body = stripped[bare_fm_match.end():].lstrip("\n")
                continue

        break

    return body


def parse_chapter(content: str) -> dict:
    """分离 YAML frontmatter 和正文。

    支持正常的 --- 分隔符以及 Milkdown 损坏的 thematic break 分隔符
    （***、___、--------- 等）。

    Args:
        content: 完整的章节 Markdown 文件内容

    Returns:
        {"title": str, "status": str, "published_at": str|None, "content": str, "word_count": int}
    """
    title = ""
    status = "draft"
    published_at = None
    body = content

    if content.startswith("---"):
        # 仅当首行恰好是 "---" 时使用 split 解析（避免 --------- 等长序列被错误拆分）
        first_nl = content.find("\n")
        first_line = content[:first_nl].strip() if first_nl >= 0 else content.strip()
        if first_line == "---":
            parts = content.split("---", 2)
            # parts[0] 是空字符串（--- 之前），parts[1] 是 YAML，parts[2] 是正文
            if len(parts) >= 3:
                try:
                    meta = yaml.safe_load(parts[1]) or {}
                except yaml.YAMLError:
                    meta = {}
                title = meta.get("title", "") or ""
                status = meta.get("status", "draft") or "draft"
                raw_pa = meta.get("published_at")
                if raw_pa is not None:
                    published_at = str(raw_pa)
                body = parts[2].lstrip("\n")

    # 如果正常解析未提取到 title，尝试从 Milkdown 损坏的 thematic break
    # frontmatter 中提取（如 ***\nstatus: draft\ntitle: xxx\n---------）
    if not title:
        _TB = r'[*_-]{3,}'
        corrupted = re.match(
            r'^' + _TB + r'[ \t]*\n+'
            r'((?:(?:title|status):[^\n]*\n)+)'
            r'(?:' + _TB + r'[ \t]*\n?)?',
            body.lstrip("\n"),
        )
        if corrupted:
            yaml_text = corrupted.group(1)
            title_m = re.search(r'title:\s*(.+)', yaml_text)
            status_m = re.search(
                r'status:\s*(draft|completed|published|archived)', yaml_text
            )
            if title_m or status_m:
                title = title_m.group(1).strip() if title_m else ""
                status = status_m.group(1).strip() if status_m else "draft"

    # 清理正文中可能残留的 frontmatter（历史 bug 导致的数据污染）
    body = _strip_leaked_frontmatter(body)

    word_count = len(body.replace("\n", "").replace(" ", ""))
    return {
        "title": title,
        "status": status,
        "published_at": published_at,
        "content": body,
        "word_count": word_count,
    }


def build_chapter(title: str, status: str, content: str, published_at: str = None) -> str:
    """构建带 frontmatter 的章节文件内容。

    Args:
        title: 章节标题
        status: 章节状态（draft/completed/published）
        content: 正文内容
        published_at: 发布时间 ISO 格式字符串（可选）

    Returns:
        完整的 Markdown 文件内容（frontmatter + 正文）
    """
    # 在构建前清理内容中可能残留的 frontmatter，防止二次包裹
    content = _strip_leaked_frontmatter(content)
    meta_dict = {"title": title, "status": status}
    if published_at:
        meta_dict["published_at"] = published_at
    meta = yaml.dump(
        meta_dict,
        allow_unicode=True,
        default_flow_style=False,
    ).strip()
    return f"---\n{meta}\n---\n\n{content}"
