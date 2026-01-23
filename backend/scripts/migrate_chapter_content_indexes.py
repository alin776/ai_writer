"""
Migration: generate content indexes from chapter files.

Usage:
    python scripts/migrate_chapter_content_indexes.py
    python scripts/migrate_chapter_content_indexes.py --clear-db-content
"""
import argparse
import asyncio
import logging
import sys
from pathlib import Path

# 添加项目根目录到 Python 路径
sys.path.insert(0, str(Path(__file__).parent.parent))

from sqlalchemy import select

from app.core.database import async_session_maker
from app.models.chapter import Chapter
from app.services.chapter_content_index_service import ChapterContentIndexService
from app.utils.chapter_file_storage import chapter_storage

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)


async def migrate_indexes(clear_db_content: bool = False) -> None:
    async with async_session_maker() as db:
        logger.info("=" * 60)
        logger.info("Starting chapter content index migration")
        logger.info("=" * 60)

        stmt = select(Chapter).order_by(Chapter.work_id, Chapter.order)
        result = await db.execute(stmt)
        chapters = result.scalars().all()

        if not chapters:
            logger.info("No chapters to process")
            return

        index_service = ChapterContentIndexService(db)
        success_count = 0
        skipped_count = 0
        failed_count = 0

        for index, chapter in enumerate(chapters, 1):
            content = chapter_storage.read_content(str(chapter.work_id), str(chapter.id))
            if not content or not content.strip():
                skipped_count += 1
                continue

            try:
                updated = await index_service.upsert_from_content(
                    str(chapter.work_id),
                    str(chapter.id),
                    content,
                    commit=False,
                )
                if updated:
                    success_count += 1
                else:
                    skipped_count += 1

                if clear_db_content:
                    chapter.content = ""
            except Exception as exc:
                failed_count += 1
                await db.rollback()
                logger.warning(f"Index failed: chapter_id={chapter.id} error={exc}")

            if index % 100 == 0:
                logger.info(f"Processed {index}/{len(chapters)} chapters")

        try:
            await db.commit()
        except Exception as exc:
            await db.rollback()
            logger.warning(f"Index commit failed: {exc}")

        logger.info("=" * 60)
        logger.info("Migration completed")
        logger.info("=" * 60)
        logger.info(f"Success: {success_count}")
        logger.info(f"Skipped: {skipped_count}")
        logger.info(f"Failed: {failed_count}")


def _parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Migrate chapter content indexes")
    parser.add_argument(
        "--clear-db-content",
        action="store_true",
        help="Clear chapters.content after indexing",
    )
    return parser.parse_args()


if __name__ == "__main__":
    args = _parse_args()
    try:
        asyncio.run(migrate_indexes(clear_db_content=args.clear_db_content))
    except KeyboardInterrupt:
        logger.info("Migration interrupted")
    except Exception as exc:
        logger.error(f"Migration failed: {exc}")
        sys.exit(1)
