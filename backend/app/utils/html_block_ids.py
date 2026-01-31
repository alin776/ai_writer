import random
import re
from typing import Set


_BLOCK_TAGS = ("p", "h1", "h2", "h3", "h4", "h5", "h6", "blockquote", "pre", "li")
_ID_PATTERN = re.compile(r'\sdata-id=["\']([^"\']+)["\']', re.IGNORECASE)
_ID_CHARS = "abcdefghijklmnopqrstuvwxyz0123456789"
_RNG = random.SystemRandom()


def _generate_id(used: Set[str]) -> str:
    while True:
        candidate = "".join(_RNG.choice(_ID_CHARS) for _ in range(8))
        if candidate not in used:
            return candidate


def ensure_block_ids(html: str) -> str:
    if not html or "<" not in html:
        return html

    used: Set[str] = set()
    result = html

    for tag in _BLOCK_TAGS:
        pattern = re.compile(rf"<{tag}([^>]*)>(.*?)</{tag}>", re.IGNORECASE | re.DOTALL)

        def _repl(match):
            attrs = match.group(1) or ""
            body = match.group(2)
            id_match = _ID_PATTERN.search(attrs)
            node_id = id_match.group(1) if id_match else None
            if node_id and node_id not in used:
                used.add(node_id)
                return match.group(0)

            new_id = _generate_id(used)
            used.add(new_id)

            if id_match:
                attrs_clean = _ID_PATTERN.sub("", attrs)
            else:
                attrs_clean = attrs
            attrs_clean = attrs_clean.rstrip()
            if attrs_clean:
                attrs_clean = f"{attrs_clean} data-id=\"{new_id}\""
            else:
                attrs_clean = f" data-id=\"{new_id}\""

            return f"<{tag}{attrs_clean}>{body}</{tag}>"

        result = pattern.sub(_repl, result)

    return result
