# -*- coding: utf-8 -*-
"""
章节文件存储

路径格式: {root}/{work_id}/{chapter_id}.html
"""
import logging
import os
import re
import tempfile
from pathlib import Path
from typing import Optional

from app.core.config import settings

logger = logging.getLogger(__name__)

_SAFE_SEGMENT_RE = re.compile(r"[^a-zA-Z0-9_-]")


def _sanitize_segment(value: str) -> str:
    return _SAFE_SEGMENT_RE.sub("_", value or "")


class ChapterFileStorage:
    def __init__(self, root_dir: Optional[str] = None):
        self.root_dir = Path(root_dir or settings.CHAPTER_STORAGE_ROOT).resolve()
        self.root_dir.mkdir(parents=True, exist_ok=True)
        logger.info(f"[ChapterStorage] root_dir={self.root_dir}")

    def get_chapter_path(self, work_id: str, chapter_id: str) -> Path:
        safe_work = _sanitize_segment(work_id)
        safe_chapter = _sanitize_segment(chapter_id)
        return self.root_dir / safe_work / f"{safe_chapter}.html"

    def read_content(
        self,
        work_id: str,
        chapter_id: str,
        min_mtime: Optional[float] = None,
    ) -> Optional[str]:
        path = self.get_chapter_path(work_id, chapter_id)
        if not path.exists():
            return None
        if min_mtime is not None:
            try:
                if path.stat().st_mtime < min_mtime:
                    return None
            except OSError:
                return None
        try:
            return path.read_text(encoding="utf-8")
        except Exception as exc:
            logger.warning(f"[ChapterStorage] read failed: {path} error={exc}")
            return None

    def write_content(self, work_id: str, chapter_id: str, content: str) -> None:
        path = self.get_chapter_path(work_id, chapter_id)
        path.parent.mkdir(parents=True, exist_ok=True)

        fd, tmp_path = tempfile.mkstemp(
            prefix=f".{path.name}.", suffix=".tmp", dir=str(path.parent)
        )
        try:
            with os.fdopen(fd, "w", encoding="utf-8") as handle:
                handle.write(content or "")
            os.replace(tmp_path, path)
        except Exception:
            try:
                os.unlink(tmp_path)
            except OSError:
                pass
            raise

    def delete_content(self, work_id: str, chapter_id: str) -> bool:
        path = self.get_chapter_path(work_id, chapter_id)
        try:
            if path.exists():
                path.unlink()
                return True
        except Exception as exc:
            logger.warning(f"[ChapterStorage] delete failed: {path} error={exc}")
        return False

    def is_fresh(
        self,
        work_id: str,
        chapter_id: str,
        min_mtime: Optional[float] = None,
    ) -> bool:
        path = self.get_chapter_path(work_id, chapter_id)
        if not path.exists():
            return False
        if min_mtime is None:
            return True
        try:
            return path.stat().st_mtime >= min_mtime
        except OSError:
            return False


chapter_storage = ChapterFileStorage()
