import argparse
import asyncio
import logging
import os
import sys
import uuid
from typing import Optional

from sqlalchemy import select

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.join(SCRIPT_DIR, "backend"))

from app.core.database import AsyncSessionLocal  # noqa: E402
from app.models.chapter import Chapter  # noqa: E402
from app.services.chapter_content_index_service import ChapterContentIndexService  # noqa: E402
from app.utils.chapter_file_storage import chapter_storage  # noqa: E402
from app.utils.html_block_ids import ensure_block_ids  # noqa: E402


logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")


async def normalize_chapters(work_id: Optional[str], dry_run: bool) -> None:
    async with AsyncSessionLocal() as db:
        stmt = select(Chapter)
        if work_id:
            stmt = stmt.where(Chapter.work_id == uuid.UUID(work_id))
        result = await db.execute(stmt)
        chapters = list(result.scalars().all())

        index_service = ChapterContentIndexService(db)
        updated = 0

        for chapter in chapters:
            work_id_str = str(chapter.work_id)
            chapter_id_str = str(chapter.id)
            content = chapter_storage.read_content(work_id_str, chapter_id_str)
            if content is None:
                continue
            normalized = ensure_block_ids(content)
            if normalized == content:
                continue
            updated += 1
            if dry_run:
                logging.info("Would update: work=%s chapter=%s", work_id_str, chapter_id_str)
                continue
            chapter_storage.write_content(work_id_str, chapter_id_str, normalized)
            await index_service.upsert_from_content(work_id_str, chapter_id_str, normalized, commit=False)

        if not dry_run:
            await db.commit()
        logging.info("Chapters scanned: %s, updated: %s, dry_run=%s", len(chapters), updated, dry_run)


def main() -> None:
    parser = argparse.ArgumentParser(description="Normalize chapter HTML block data-id attributes.")
    parser.add_argument("--work-id", dest="work_id", help="Limit to a single work UUID")
    parser.add_argument("--dry-run", action="store_true", help="Report changes without writing")
    args = parser.parse_args()
    asyncio.run(normalize_chapters(args.work_id, args.dry_run))


if __name__ == "__main__":
    main()
