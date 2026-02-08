"""
重建 OpenSearch 章节段落索引。

用法：
    python scripts/reindex_opensearch_vectors.py
    python scripts/reindex_opensearch_vectors.py --work-id <WORK_ID>
    python scripts/reindex_opensearch_vectors.py --work-id <W1> --work-id <W2>
    python scripts/reindex_opensearch_vectors.py --recreate-index
"""

import argparse
import asyncio
import logging
import sys
from pathlib import Path
from typing import List

# 添加项目根目录到 Python 路径
sys.path.insert(0, str(Path(__file__).parent.parent))

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)


def _dedupe_keep_order(items: List[str]) -> List[str]:
    seen = set()
    out: List[str] = []
    for item in items:
        value = (item or "").strip()
        if not value or value in seen:
            continue
        seen.add(value)
        out.append(value)
    return out


async def reindex_opensearch_vectors(
    work_ids: List[str],
    recreate_index: bool = False,
    clear_index: bool = False,
    limit: int = 0,
) -> None:
    from sqlalchemy import select
    from app.core.database import async_session_maker
    from app.models.work import Work
    from app.services.search.opensearch_chapter_search_service import OpenSearchChapterSearchService

    async with async_session_maker() as db:
        search_service = OpenSearchChapterSearchService(db)

        if recreate_index:
            logger.info("[reindex] recreate index enabled")
            await search_service.recreate_index()
        elif clear_index:
            logger.info("[reindex] clear index enabled")
            await search_service.clear_index()
        else:
            await search_service.ensure_index()

        target_work_ids = _dedupe_keep_order(work_ids)
        if not target_work_ids:
            stmt = select(Work.id).order_by(Work.created_at.asc())
            result = await db.execute(stmt)
            target_work_ids = [str(row[0]) for row in result.all() if row and row[0]]

        if limit > 0:
            target_work_ids = target_work_ids[:limit]

        total_works = len(target_work_ids)
        if total_works == 0:
            logger.info("[reindex] no works found")
            return

        logger.info("[reindex] start, works=%s", total_works)
        total_indexed = 0
        failed = 0

        for index, work_id in enumerate(target_work_ids, 1):
            try:
                indexed = await search_service.sync_work_vectors(work_id)
                total_indexed += int(indexed or 0)
            except Exception as exc:
                failed += 1
                logger.warning("[reindex] work failed: work_id=%s error=%s", work_id, exc)

            if index % 20 == 0 or index == total_works:
                logger.info(
                    "[reindex] progress: %s/%s, indexed=%s, failed=%s",
                    index,
                    total_works,
                    total_indexed,
                    failed,
                )

        logger.info(
            "[reindex] done, works=%s, indexed=%s, failed=%s",
            total_works,
            total_indexed,
            failed,
        )


def _parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Reindex chapter vectors to OpenSearch")
    parser.add_argument(
        "--work-id",
        action="append",
        default=[],
        help="指定作品ID（可重复传多个）；不传则默认全量",
    )
    parser.add_argument(
        "--recreate-index",
        action="store_true",
        help="先删除并重建索引，再执行重建",
    )
    parser.add_argument(
        "--clear-index",
        action="store_true",
        help="先清空索引文档（保留 mapping），再执行重建",
    )
    parser.add_argument(
        "--limit",
        type=int,
        default=0,
        help="限制处理作品数量（0 表示不限制）",
    )
    return parser.parse_args()


if __name__ == "__main__":
    args = _parse_args()
    try:
        asyncio.run(
            reindex_opensearch_vectors(
                work_ids=args.work_id or [],
                recreate_index=bool(args.recreate_index),
                clear_index=bool(args.clear_index),
                limit=max(0, int(args.limit or 0)),
            )
        )
    except KeyboardInterrupt:
        logger.info("Reindex interrupted")
    except Exception as exc:
        logger.error(f"Reindex failed: {exc}")
        sys.exit(1)
