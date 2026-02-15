import logging
import re
from typing import Any, Dict, List

logger = logging.getLogger(__name__)

_CONTROL_CHARS = re.compile(r"[\x00-\x08\x0B\x0C\x0E-\x1F]")
_HTML_TAG = re.compile(r"<[^>]+>")
_MULTI_SPACE = re.compile(r"[ \t]+")
_MULTI_NEWLINE = re.compile(r"\n{3,}")


class ContentSanitizer:
    def sanitize_text(self, text: Any, max_length: int = 500) -> str:
        if text is None:
            return ""
        value = str(text)
        value = value.replace("\r\n", "\n").replace("\r", "\n")
        value = _CONTROL_CHARS.sub("", value)
        if "<" in value and ">" in value:
            value = _HTML_TAG.sub("", value)
        value = _MULTI_SPACE.sub(" ", value)
        value = _MULTI_NEWLINE.sub("\n\n", value)
        value = value.strip()
        if max_length and len(value) > max_length:
            value = value[:max_length] + "..."
        return value

    def sanitize_worldview_item(
        self,
        item: Any,
        max_field_length: int = 500,
        max_list_items: int = 80,
        _depth: int = 4,
    ) -> Any:
        if _depth <= 0:
            return None
        if isinstance(item, dict):
            sanitized: Dict[str, Any] = {}
            for key, value in item.items():
                sanitized[key] = self._sanitize_value(
                    value,
                    max_field_length=max_field_length,
                    max_list_items=max_list_items,
                    depth=_depth - 1,
                )
            return sanitized
        return self._sanitize_value(item, max_field_length=max_field_length, max_list_items=max_list_items, depth=_depth - 1)

    def sanitize_worldview_data(
        self,
        data: Any,
        max_field_length: int = 600,
        max_list_items: int = 200,
    ) -> Dict[str, Any]:
        if not isinstance(data, dict):
            return {}
        sanitized: Dict[str, Any] = {}
        for key, value in data.items():
            sanitized[key] = self._sanitize_value(
                value,
                max_field_length=max_field_length,
                max_list_items=max_list_items,
                depth=5,
            )
        return sanitized

    def _sanitize_list(
        self,
        values: Any,
        max_items: int,
        max_item_length: int,
        depth: int,
    ) -> List[Any]:
        if not isinstance(values, list):
            return []
        sanitized: List[Any] = []
        for item in values:
            if len(sanitized) >= max_items:
                break
            cleaned = self._sanitize_value(
                item,
                max_field_length=max_item_length,
                max_list_items=max_items,
                depth=depth - 1,
            )
            if cleaned is None:
                continue
            sanitized.append(cleaned)
        return sanitized

    def _sanitize_value(
        self,
        value: Any,
        max_field_length: int,
        max_list_items: int,
        depth: int,
    ) -> Any:
        if depth <= 0:
            return None
        if value is None:
            return None
        if isinstance(value, (int, float, bool)):
            return value
        if isinstance(value, str):
            return self.sanitize_text(value, max_length=max_field_length)
        if isinstance(value, dict):
            return self.sanitize_worldview_item(
                value,
                max_field_length=max_field_length,
                max_list_items=max_list_items,
                _depth=depth - 1,
            )
        if isinstance(value, list):
            return self._sanitize_list(
                value,
                max_items=max_list_items,
                max_item_length=max_field_length,
                depth=depth - 1,
            )
        return self.sanitize_text(value, max_length=max_field_length)


content_sanitizer = ContentSanitizer()

__all__ = ["ContentSanitizer", "content_sanitizer"]

