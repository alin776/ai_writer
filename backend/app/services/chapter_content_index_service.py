# -*- coding: utf-8 -*-
"""
Chapter content index service (derived from file content).
"""
import hashlib
import logging
from typing import Optional

from sqlalchemy import select, delete, func
from sqlalchemy.dialects.postgresql import insert as pg_insert
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.chapter_content_index import ChapterContentIndex
from app.utils.chapter_file_storage import chapter_storage
from app.utils.text_cleaner import TextCleaner

logger = logging.getLogger(__name__)


class ChapterContentIndexService:
    def __init__(self, db: AsyncSession):
        self.db = db

    def _hash_content(self, html_content: str) -> str:
        return hashlib.sha256((html_content or "").encode("utf-8")).hexdigest()

    def _build_summary(self, plain_text: str, max_length: int = 200) -> str:
        if not plain_text:
            return ""
        compact = " ".join(plain_text.split())
        if len(compact) <= max_length:
            return compact
        return compact[:max_length].rstrip() + "..."

    def _build_index_data(self, html_content: str) -> dict:
        plain_text = TextCleaner.html_to_clean_text(html_content or "", preserve_structure=True)
        return {
            "plain_text": plain_text,
            "summary": self._build_summary(plain_text),
            "content_hash": self._hash_content(html_content or ""),
        }

    async def upsert_from_content(
        self,
        work_id: str,
        chapter_id: str,
        html_content: str,
        commit: bool = True,
    ) -> bool:
        index_data = self._build_index_data(html_content)
        existing_hash = await self._get_existing_hash(chapter_id)
        if existing_hash == index_data["content_hash"]:
            return False

        stmt = pg_insert(ChapterContentIndex).values(
            chapter_id=chapter_id,
            work_id=work_id,
            plain_text=index_data["plain_text"],
            summary=index_data["summary"],
            content_hash=index_data["content_hash"],
            updated_at=func.now(),
        )
        stmt = stmt.on_conflict_do_update(
            index_elements=[ChapterContentIndex.chapter_id],
            set_={
                "work_id": work_id,
                "plain_text": index_data["plain_text"],
                "summary": index_data["summary"],
                "content_hash": index_data["content_hash"],
                "updated_at": func.now(),
            },
        )
        await self.db.execute(stmt)
        if commit:
            await self.db.commit()
        return True

    async def upsert_from_file(self, work_id: str, chapter_id: str, commit: bool = True) -> bool:
        html_content = chapter_storage.read_content(work_id, chapter_id)
        if html_content is None:
            logger.warning(f"[ChapterContentIndex] Missing file: work={work_id} chapter={chapter_id}")
            return False
        return await self.upsert_from_content(work_id, chapter_id, html_content, commit=commit)

    async def delete_index(self, chapter_id: str, commit: bool = True) -> None:
        await self.db.execute(
            delete(ChapterContentIndex).where(ChapterContentIndex.chapter_id == chapter_id)
        )
        if commit:
            await self.db.commit()

    async def _get_existing_hash(self, chapter_id: str) -> Optional[str]:
        result = await self.db.execute(
            select(ChapterContentIndex.content_hash).where(
                ChapterContentIndex.chapter_id == chapter_id
            )
        )
        return result.scalar_one_or_none()
