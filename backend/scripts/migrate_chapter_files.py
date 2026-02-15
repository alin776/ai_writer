"""
迁移脚本：为现有章节生成章节文件

用法：
    python scripts/migrate_chapter_files.py
    python scripts/migrate_chapter_files.py --force
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
from app.utils.chapter_file_storage import chapter_storage

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)


def _is_fresh(chapter: Chapter) -> bool:
    if not chapter.updated_at:
        return False
    return chapter_storage.is_fresh(
        str(chapter.work_id),
        str(chapter.id),
        chapter.updated_at.timestamp(),
    )


async def migrate_existing_chapters(force: bool = False) -> None:
    async with async_session_maker() as db:
        logger.info("=" * 60)
        logger.info("开始迁移章节文件")
        logger.info("=" * 60)

        stmt = select(Chapter).where(
            Chapter.content.isnot(None),
            Chapter.content != "",
        ).order_by(Chapter.work_id, Chapter.order)

        result = await db.execute(stmt)
        chapters = result.scalars().all()

        logger.info(f"找到 {len(chapters)} 个有内容的章节")
        if not chapters:
            return

        success_count = 0
        skipped_count = 0
        failed_count = 0

        for index, chapter in enumerate(chapters, 1):
            content = chapter.content or ""
            if not content.strip():
                skipped_count += 1
                continue

            if not force and _is_fresh(chapter):
                skipped_count += 1
                continue

            try:
                chapter_storage.write_content(
                    str(chapter.work_id), str(chapter.id), content
                )
                success_count += 1
                if index % 50 == 0:
                    logger.info(f"已处理 {index}/{len(chapters)} 章")
            except Exception as exc:
                failed_count += 1
                logger.warning(
                    f"写入失败: chapter_id={chapter.id} error={exc}"
                )

        logger.info("=" * 60)
        logger.info("迁移完成")
        logger.info("=" * 60)
        logger.info(f"成功: {success_count}")
        logger.info(f"跳过: {skipped_count}")
        logger.info(f"失败: {failed_count}")


def _parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="迁移章节内容到文件系统")
    parser.add_argument(
        "--force",
        action="store_true",
        help="覆盖已存在的章节文件",
    )
    return parser.parse_args()


if __name__ == "__main__":
    args = _parse_args()
    try:
        asyncio.run(migrate_existing_chapters(force=args.force))
    except KeyboardInterrupt:
        logger.info("迁移被用户中断")
    except Exception as exc:
        logger.error(f"迁移失败: {exc}")
        sys.exit(1)
