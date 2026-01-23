"""
Verify chapter file storage and content indexes.

Usage:
    python scripts/verify_chapter_storage.py
    python scripts/verify_chapter_storage.py --limit 20 --fail-on-issues
"""
import argparse
import asyncio
import hashlib
import logging
import sys
from pathlib import Path

# 添加项目根目录到 Python 路径
sys.path.insert(0, str(Path(__file__).parent.parent))

from sqlalchemy import func, select

import app.models.bookshelf  # noqa: F401
from app.core.database import async_session_maker
from app.models.chapter import Chapter
from app.models.chapter_content_index import ChapterContentIndex
from app.utils.chapter_file_storage import chapter_storage

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)


def _hash_content(html_content: str) -> str:
    return hashlib.sha256((html_content or "").encode("utf-8")).hexdigest()


def _sample(items: list[str], limit: int) -> str:
    if limit <= 0 or not items:
        return ""
    return ", ".join(items[:limit])


async def verify_storage(limit: int, fail_on_issues: bool) -> int:
    async with async_session_maker() as db:
        total = await db.scalar(select(func.count()).select_from(Chapter)) or 0

        non_empty_count = await db.scalar(
            select(func.count()).select_from(Chapter).where(
                func.length(func.trim(Chapter.content)) > 0
            )
        ) or 0

        non_empty_sample = []
        if non_empty_count > 0 and limit > 0:
            sample_rows = await db.execute(
                select(Chapter.id, Chapter.work_id)
                .where(func.length(func.trim(Chapter.content)) > 0)
                .limit(limit)
            )
            non_empty_sample = [
                f"{row[0]} (work={row[1]})" for row in sample_rows.all()
            ]

        index_rows = await db.execute(
            select(ChapterContentIndex.chapter_id, ChapterContentIndex.content_hash)
        )
        index_map = {
            str(chapter_id): content_hash
            for chapter_id, content_hash in index_rows.all()
        }

        chapter_rows = await db.execute(
            select(Chapter.id, Chapter.work_id, Chapter.word_count)
            .order_by(Chapter.work_id, Chapter.order)
        )

        missing_files = []
        empty_files = []
        index_missing = []
        hash_mismatch = []
        checked_with_content = 0

        for chapter_id, work_id, _word_count in chapter_rows.all():
            chapter_id_str = str(chapter_id)
            work_id_str = str(work_id)
            html_content = chapter_storage.read_content(work_id_str, chapter_id_str)

            if html_content is None:
                missing_files.append(f"{chapter_id_str} (work={work_id_str})")
                continue
            if not html_content.strip():
                empty_files.append(f"{chapter_id_str} (work={work_id_str})")
                continue

            checked_with_content += 1
            index_hash = index_map.get(chapter_id_str)
            if not index_hash:
                index_missing.append(f"{chapter_id_str} (work={work_id_str})")
                continue

            file_hash = _hash_content(html_content)
            if file_hash != index_hash:
                hash_mismatch.append(f"{chapter_id_str} (work={work_id_str})")

        logger.info("=" * 60)
        logger.info("章节文件化校验结果")
        logger.info("=" * 60)
        logger.info(f"章节总数: {total}")
        logger.info(f"DB content 非空: {non_empty_count}")
        logger.info(f"文件缺失: {len(missing_files)}")
        logger.info(f"文件为空: {len(empty_files)}")
        logger.info(f"索引缺失: {len(index_missing)}")
        logger.info(f"索引哈希不一致: {len(hash_mismatch)}")
        logger.info(f"有内容文件检查数: {checked_with_content}")

        if non_empty_sample:
            logger.warning(f"DB content 非空示例: {_sample(non_empty_sample, limit)}")
        if missing_files:
            logger.warning(f"文件缺失示例: {_sample(missing_files, limit)}")
        if empty_files:
            logger.warning(f"文件为空示例: {_sample(empty_files, limit)}")
        if index_missing:
            logger.warning(f"索引缺失示例: {_sample(index_missing, limit)}")
        if hash_mismatch:
            logger.warning(f"索引哈希不一致示例: {_sample(hash_mismatch, limit)}")

        issues = (
            non_empty_count
            or missing_files
            or empty_files
            or index_missing
            or hash_mismatch
        )
        if issues:
            logger.warning("检测到问题，请按示例章节进行排查。")
            return 1 if fail_on_issues else 0

        logger.info("校验通过：DB content 为空、文件与索引一致。")
        return 0


def _parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Verify chapter storage consistency")
    parser.add_argument(
        "--limit",
        type=int,
        default=20,
        help="Limit sample output for each issue type",
    )
    parser.add_argument(
        "--fail-on-issues",
        action="store_true",
        help="Exit with code 1 if any issue is detected",
    )
    return parser.parse_args()


if __name__ == "__main__":
    args = _parse_args()
    try:
        exit_code = asyncio.run(
            verify_storage(limit=args.limit, fail_on_issues=args.fail_on_issues)
        )
    except KeyboardInterrupt:
        logger.info("校验被用户中断")
        exit_code = 1
    except Exception as exc:
        logger.error(f"校验失败: {exc}")
        exit_code = 1
    raise SystemExit(exit_code)
