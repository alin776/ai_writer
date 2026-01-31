# -*- coding: utf-8 -*-
"""
Chapter content reader (files are the source of truth).
"""
import logging
from typing import Optional

from sqlalchemy.orm.attributes import set_committed_value

from app.utils.chapter_file_storage import chapter_storage

logger = logging.getLogger(__name__)


class ChapterContentProvider:
    def read_content(self, work_id: str, chapter_id: str) -> Optional[str]:
        content = chapter_storage.read_content(work_id, chapter_id)
        if content is None:
            logger.warning(f"[ChapterContentProvider] Missing file: work={work_id} chapter={chapter_id}")
        return content

    def hydrate_chapter(self, chapter) -> str:
        content = self.read_content(str(chapter.work_id), str(chapter.id))
        set_committed_value(chapter, "content", content or "")
        return chapter.content
