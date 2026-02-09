"""
OpenSearch chapter paragraph search service.

This service provides keyword paragraph retrieval for Explore exact search.
"""

import asyncio
import logging
import time
from datetime import datetime, timedelta, timezone
from typing import Any, Dict, List, Optional, Tuple
from uuid import UUID

from opensearchpy import OpenSearch, helpers
from sqlalchemy import func, or_, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import settings
from app.models.chapter import Chapter
from app.models.novel_chapter_vector import NovelChapterVector
from app.models.opensearch_sync_status import OpenSearchSyncStatus, OpenSearchSyncStatusEnum
from app.models.work import Work

logger = logging.getLogger(__name__)

OPENSEARCH_SEARCH_MAX_PAGES = 500
OPENSEARCH_SEARCH_MAX_RESULTS = 5000


class OpenSearchChapterSearchService:
    """Keyword paragraph search powered by OpenSearch."""

    _client: Optional[OpenSearch] = None
    _index_ready: bool = False
    _synced_work_ids: set[str] = set()
    _last_runtime_sync_check_ts: Dict[str, float] = {}

    def __init__(self, db: AsyncSession):
        self.db = db
        self.index_name = (settings.OPENSEARCH_INDEX_NAME or "novel_chapter_vectors").strip()

    @classmethod
    def _get_client(cls) -> OpenSearch:
        if cls._client is not None:
            return cls._client

        hosts = [h.strip() for h in (settings.OPENSEARCH_HOSTS or "").split(",") if h.strip()]
        if not hosts:
            hosts = ["http://localhost:9200"]

        kwargs: Dict[str, Any] = {
            "hosts": hosts,
            "timeout": settings.OPENSEARCH_TIMEOUT_SECONDS,
            "use_ssl": settings.OPENSEARCH_USE_SSL,
            "verify_certs": settings.OPENSEARCH_VERIFY_CERTS,
        }
        if settings.OPENSEARCH_USERNAME:
            kwargs["http_auth"] = (
                settings.OPENSEARCH_USERNAME,
                settings.OPENSEARCH_PASSWORD or "",
            )

        cls._client = OpenSearch(**kwargs)
        return cls._client

    async def ensure_index(self) -> None:
        if self.__class__._index_ready:
            return

        client = self._get_client()

        exists = await asyncio.to_thread(client.indices.exists, index=self.index_name)
        if exists:
            self.__class__._index_ready = True
            return

        body = {
            "settings": {
                "index": {
                    "number_of_shards": 1,
                    "number_of_replicas": 0,
                }
            },
            "mappings": {
                "properties": {
                    "work_id": {"type": "keyword"},
                    "chapter_id": {"type": "keyword"},
                    "chapter_order": {"type": "integer"},
                    "chapter_title": {
                        "type": "text",
                        "fields": {
                            "keyword": {
                                "type": "keyword",
                                "ignore_above": 512,
                            }
                        },
                    },
                    "paragraph_index": {"type": "integer"},
                    "chunk_text": {"type": "text"},
                    "node_id": {"type": "keyword"},
                }
            },
        }

        await asyncio.to_thread(client.indices.create, index=self.index_name, body=body)
        self.__class__._index_ready = True
        logger.info("[OpenSearchSearch] index created: %s", self.index_name)

    @classmethod
    def reset_sync_cache(cls) -> None:
        cls._synced_work_ids.clear()

    @staticmethod
    def _utcnow() -> datetime:
        return datetime.now(timezone.utc)

    @staticmethod
    def _safe_uuid(value: Any) -> Optional[UUID]:
        if isinstance(value, UUID):
            return value
        if isinstance(value, str):
            text = value.strip()
            if not text:
                return None
            try:
                return UUID(text)
            except Exception:
                return None
        return None

    @staticmethod
    def _coerce_positive_int(value: Any, default: int) -> int:
        try:
            result = int(value)
        except Exception:
            result = int(default)
        if result <= 0:
            return int(default)
        return int(result)

    def _compute_retry_delay_seconds(self, retry_count: int) -> int:
        base_delay = self._coerce_positive_int(settings.OPENSEARCH_SYNC_RETRY_BASE_DELAY_SECONDS, 30)
        max_delay = self._coerce_positive_int(settings.OPENSEARCH_SYNC_RETRY_MAX_DELAY_SECONDS, 900)
        retry_step = max(int(retry_count) - 1, 0)
        delay = base_delay * (2 ** min(retry_step, 8))
        return int(min(max(delay, base_delay), max_delay))

    async def _resolve_chapter_meta(
        self,
        chapter_id: str,
        work_id: Optional[str] = None,
        chapter_order: Optional[int] = None,
    ) -> Tuple[Optional[str], Optional[int]]:
        resolved_work_id = str(work_id) if work_id else None
        resolved_chapter_order = chapter_order if isinstance(chapter_order, int) else None
        if resolved_work_id and resolved_chapter_order is not None:
            return resolved_work_id, resolved_chapter_order

        chapter_uuid = self._safe_uuid(chapter_id)
        if chapter_uuid is None:
            return resolved_work_id, resolved_chapter_order

        vector_stmt = (
            select(NovelChapterVector.work_id, NovelChapterVector.chapter_order)
            .where(NovelChapterVector.chapter_id == chapter_uuid)
            .order_by(NovelChapterVector.chunk_index.asc())
            .limit(1)
        )
        vector_row = (await self.db.execute(vector_stmt)).first()
        if vector_row:
            if not resolved_work_id and vector_row[0]:
                resolved_work_id = str(vector_row[0])
            if resolved_chapter_order is None and vector_row[1] is not None:
                resolved_chapter_order = int(vector_row[1])

        if resolved_work_id and resolved_chapter_order is not None:
            return resolved_work_id, resolved_chapter_order

        chapter_stmt = (
            select(Chapter.work_id, Chapter.order)
            .where(Chapter.id == chapter_uuid)
            .limit(1)
        )
        chapter_row = (await self.db.execute(chapter_stmt)).first()
        if chapter_row:
            if not resolved_work_id and chapter_row[0]:
                resolved_work_id = str(chapter_row[0])
            if resolved_chapter_order is None and chapter_row[1] is not None:
                resolved_chapter_order = int(chapter_row[1])

        return resolved_work_id, resolved_chapter_order

    async def _count_db_vectors_for_chapter(self, chapter_id: str) -> int:
        chapter_uuid = self._safe_uuid(chapter_id)
        if chapter_uuid is None:
            return 0
        stmt = select(func.count(NovelChapterVector.id)).where(NovelChapterVector.chapter_id == chapter_uuid)
        count_val = (await self.db.execute(stmt)).scalar()
        return int(count_val or 0)

    async def _count_index_vectors_for_chapter(self, chapter_id: str) -> int:
        await self.ensure_index()
        client = self._get_client()
        resp = await asyncio.to_thread(
            client.count,
            index=self.index_name,
            body={"query": {"term": {"chapter_id": str(chapter_id)}}},
        )
        return int((resp or {}).get("count", 0))

    async def _get_sync_status_row(self, chapter_id: str) -> Optional[OpenSearchSyncStatus]:
        chapter_uuid = self._safe_uuid(chapter_id)
        if chapter_uuid is None:
            return None
        stmt = (
            select(OpenSearchSyncStatus)
            .where(OpenSearchSyncStatus.chapter_id == chapter_uuid)
            .limit(1)
        )
        result = await self.db.execute(stmt)
        return result.scalars().first()

    async def mark_chapter_sync_success(
        self,
        chapter_id: str,
        *,
        work_id: Optional[str] = None,
        chapter_order: Optional[int] = None,
        operation: str = "upsert",
        db_vector_count: Optional[int] = None,
        index_vector_count: Optional[int] = None,
    ) -> Dict[str, Any]:
        chapter_uuid = self._safe_uuid(chapter_id)
        if chapter_uuid is None:
            return {"updated": False, "reason": "invalid_chapter_id"}

        resolved_work_id, resolved_order = await self._resolve_chapter_meta(
            chapter_id=str(chapter_id),
            work_id=work_id,
            chapter_order=chapter_order,
        )
        work_uuid = self._safe_uuid(resolved_work_id)
        if work_uuid is None:
            logger.warning(
                "[OpenSearchSync] mark success skipped: chapter_id=%s reason=work_id_missing",
                chapter_id,
            )
            return {"updated": False, "reason": "work_id_missing"}

        db_count = int(db_vector_count) if isinstance(db_vector_count, int) else await self._count_db_vectors_for_chapter(str(chapter_id))
        if isinstance(index_vector_count, int):
            index_count = int(index_vector_count)
        else:
            try:
                index_count = await self._count_index_vectors_for_chapter(str(chapter_id))
            except Exception as count_exc:
                logger.warning(
                    "[OpenSearchSync] index count failed on success mark: chapter_id=%s error=%s",
                    chapter_id,
                    count_exc,
                )
                index_count = -1

        if (operation or "").lower() == "delete" and db_count == 0 and index_count == 0:
            status_val = OpenSearchSyncStatusEnum.DELETED
        elif db_count == index_count:
            status_val = OpenSearchSyncStatusEnum.SYNCED
        else:
            status_val = OpenSearchSyncStatusEnum.DESYNCED

        row = await self._get_sync_status_row(str(chapter_id))
        if row is None:
            row = OpenSearchSyncStatus(
                work_id=work_uuid,
                chapter_id=chapter_uuid,
            )
            self.db.add(row)

        row.work_id = work_uuid
        row.chapter_id = chapter_uuid
        row.chapter_order = resolved_order
        row.sync_status = status_val
        row.last_operation = (operation or "upsert")[:16]
        row.db_vector_count = db_count
        row.index_vector_count = index_count
        row.last_synced_at = self._utcnow()
        if status_val in (OpenSearchSyncStatusEnum.SYNCED, OpenSearchSyncStatusEnum.DELETED):
            row.retry_count = 0
            row.next_retry_at = None
            row.last_error = None
        elif row.next_retry_at is None:
            row.next_retry_at = self._utcnow()

        try:
            await self.db.commit()
        except Exception as exc:
            await self.db.rollback()
            logger.warning(
                "[OpenSearchSync] mark success commit failed: chapter_id=%s error=%s",
                chapter_id,
                exc,
            )
            return {"updated": False, "reason": "commit_failed"}

        return {
            "updated": True,
            "chapter_id": str(chapter_id),
            "status": status_val.value,
            "db_vector_count": db_count,
            "index_vector_count": index_count,
        }

    async def mark_chapter_sync_failure(
        self,
        chapter_id: str,
        *,
        work_id: Optional[str] = None,
        chapter_order: Optional[int] = None,
        operation: str = "upsert",
        error_message: str = "",
        db_vector_count: Optional[int] = None,
        index_vector_count: Optional[int] = None,
    ) -> Dict[str, Any]:
        chapter_uuid = self._safe_uuid(chapter_id)
        if chapter_uuid is None:
            return {"updated": False, "reason": "invalid_chapter_id"}

        resolved_work_id, resolved_order = await self._resolve_chapter_meta(
            chapter_id=str(chapter_id),
            work_id=work_id,
            chapter_order=chapter_order,
        )
        work_uuid = self._safe_uuid(resolved_work_id)
        if work_uuid is None:
            logger.warning(
                "[OpenSearchSync] mark failure skipped: chapter_id=%s reason=work_id_missing",
                chapter_id,
            )
            return {"updated": False, "reason": "work_id_missing"}

        db_count = int(db_vector_count) if isinstance(db_vector_count, int) else await self._count_db_vectors_for_chapter(str(chapter_id))
        if isinstance(index_vector_count, int):
            index_count = int(index_vector_count)
        else:
            try:
                index_count = await self._count_index_vectors_for_chapter(str(chapter_id))
            except Exception as count_exc:
                logger.warning(
                    "[OpenSearchSync] index count failed on failure mark: chapter_id=%s error=%s",
                    chapter_id,
                    count_exc,
                )
                index_count = -1

        row = await self._get_sync_status_row(str(chapter_id))
        if row is None:
            row = OpenSearchSyncStatus(
                work_id=work_uuid,
                chapter_id=chapter_uuid,
            )
            self.db.add(row)

        previous_retry = int(row.retry_count or 0)
        next_retry_count = previous_retry + 1
        delay_seconds = self._compute_retry_delay_seconds(next_retry_count)

        row.work_id = work_uuid
        row.chapter_id = chapter_uuid
        row.chapter_order = resolved_order
        row.sync_status = OpenSearchSyncStatusEnum.FAILED
        row.last_operation = (operation or "upsert")[:16]
        row.db_vector_count = db_count
        row.index_vector_count = index_count
        row.retry_count = next_retry_count
        row.next_retry_at = self._utcnow() + timedelta(seconds=delay_seconds)
        row.last_error = (error_message or "unknown sync error")[:2000]

        try:
            await self.db.commit()
        except Exception as exc:
            await self.db.rollback()
            logger.warning(
                "[OpenSearchSync] mark failure commit failed: chapter_id=%s error=%s",
                chapter_id,
                exc,
            )
            return {"updated": False, "reason": "commit_failed"}

        logger.warning(
            "[OpenSearchSync] enqueue retry: chapter_id=%s operation=%s retry_count=%s next_retry_in=%ss error=%s",
            chapter_id,
            row.last_operation,
            row.retry_count,
            delay_seconds,
            row.last_error,
        )
        return {
            "updated": True,
            "chapter_id": str(chapter_id),
            "status": OpenSearchSyncStatusEnum.FAILED.value,
            "retry_count": int(row.retry_count or 0),
            "next_retry_in_seconds": delay_seconds,
        }

    async def process_retry_queue(self, limit: Optional[int] = None) -> Dict[str, Any]:
        max_attempts = self._coerce_positive_int(settings.OPENSEARCH_SYNC_RETRY_MAX_ATTEMPTS, 6)
        default_limit = self._coerce_positive_int(settings.OPENSEARCH_SYNC_RETRY_BATCH_SIZE, 20)
        run_limit = min(self._coerce_positive_int(limit, default_limit), 200)
        now_ts = self._utcnow()

        stmt = (
            select(OpenSearchSyncStatus)
            .where(
                OpenSearchSyncStatus.sync_status.in_(
                    [OpenSearchSyncStatusEnum.FAILED, OpenSearchSyncStatusEnum.DESYNCED]
                ),
                OpenSearchSyncStatus.retry_count < max_attempts,
                or_(
                    OpenSearchSyncStatus.next_retry_at.is_(None),
                    OpenSearchSyncStatus.next_retry_at <= now_ts,
                ),
            )
            .order_by(OpenSearchSyncStatus.next_retry_at.asc().nullsfirst(), OpenSearchSyncStatus.updated_at.asc())
            .limit(run_limit)
        )
        due_rows = (await self.db.execute(stmt)).scalars().all()

        summary = {
            "due": len(due_rows),
            "processed": 0,
            "succeeded": 0,
            "failed": 0,
            "exhausted": 0,
        }
        for row in due_rows:
            chapter_id_text = str(row.chapter_id)
            operation = (row.last_operation or "upsert").strip().lower()
            try:
                if operation == "delete":
                    await self.delete_chapter_vectors(chapter_id_text)
                    await self.mark_chapter_sync_success(
                        chapter_id_text,
                        work_id=str(row.work_id),
                        chapter_order=row.chapter_order,
                        operation="delete",
                    )
                else:
                    await self.upsert_chapter_vectors(chapter_id_text)
                    await self.mark_chapter_sync_success(
                        chapter_id_text,
                        work_id=str(row.work_id),
                        chapter_order=row.chapter_order,
                        operation="upsert",
                    )
                summary["succeeded"] += 1
            except Exception as exc:
                await self.mark_chapter_sync_failure(
                    chapter_id_text,
                    work_id=str(row.work_id),
                    chapter_order=row.chapter_order,
                    operation=operation or "upsert",
                    error_message=f"retry failed: {exc}",
                )
                summary["failed"] += 1
            summary["processed"] += 1

        exhausted_stmt = select(func.count(OpenSearchSyncStatus.id)).where(
            OpenSearchSyncStatus.sync_status.in_(
                [OpenSearchSyncStatusEnum.FAILED, OpenSearchSyncStatusEnum.DESYNCED]
            ),
            OpenSearchSyncStatus.retry_count >= max_attempts,
        )
        exhausted_count = (await self.db.execute(exhausted_stmt)).scalar()
        summary["exhausted"] = int(exhausted_count or 0)
        return summary

    async def _collect_db_counts_by_work(self, work_id: str) -> Dict[str, Dict[str, Optional[int]]]:
        work_uuid = self._safe_uuid(work_id)
        if work_uuid is None:
            return {}

        stmt = (
            select(
                NovelChapterVector.chapter_id,
                func.min(NovelChapterVector.chapter_order).label("chapter_order"),
                func.count(NovelChapterVector.id).label("db_count"),
            )
            .where(NovelChapterVector.work_id == work_uuid)
            .group_by(NovelChapterVector.chapter_id)
        )
        rows = (await self.db.execute(stmt)).all()
        result: Dict[str, Dict[str, Optional[int]]] = {}
        for chapter_id_val, chapter_order_val, db_count_val in rows:
            if not chapter_id_val:
                continue
            result[str(chapter_id_val)] = {
                "chapter_order": int(chapter_order_val) if chapter_order_val is not None else None,
                "count": int(db_count_val or 0),
            }
        return result

    async def _collect_index_counts_by_work(self, work_id: str) -> Dict[str, Dict[str, Optional[int]]]:
        await self.ensure_index()
        client = self._get_client()
        body = {
            "size": 0,
            "query": {"term": {"work_id": str(work_id)}},
            "aggs": {
                "by_chapter": {
                    "terms": {"field": "chapter_id", "size": 10000},
                    "aggs": {"chapter_order": {"max": {"field": "chapter_order"}}},
                }
            },
        }
        try:
            resp = await asyncio.to_thread(client.search, index=self.index_name, body=body)
        except Exception as exc:
            logger.warning("[OpenSearchSync] collect index counts failed: work_id=%s error=%s", work_id, exc)
            return {}

        buckets = (((resp or {}).get("aggregations") or {}).get("by_chapter") or {}).get("buckets") or []
        result: Dict[str, Dict[str, Optional[int]]] = {}
        for bucket in buckets:
            chapter_id_key = str(bucket.get("key") or "").strip()
            if not chapter_id_key:
                continue
            chapter_order_raw = (((bucket.get("chapter_order") or {}).get("value")))
            chapter_order_val: Optional[int] = None
            if isinstance(chapter_order_raw, (int, float)):
                chapter_order_val = int(chapter_order_raw)
            result[chapter_id_key] = {
                "chapter_order": chapter_order_val,
                "count": int(bucket.get("doc_count") or 0),
            }
        return result

    async def audit_work_consistency(
        self,
        work_id: str,
        chapter_limit: Optional[int] = None,
    ) -> Dict[str, Any]:
        work_uuid = self._safe_uuid(work_id)
        if work_uuid is None:
            return {
                "work_id": str(work_id),
                "chapters_checked": 0,
                "status_counts": {},
                "mismatched_examples": [],
                "error": "invalid_work_id",
            }

        db_counts = await self._collect_db_counts_by_work(str(work_id))
        index_counts = await self._collect_index_counts_by_work(str(work_id))
        status_stmt = select(OpenSearchSyncStatus).where(OpenSearchSyncStatus.work_id == work_uuid)
        existing_rows = (await self.db.execute(status_stmt)).scalars().all()
        row_by_chapter = {str(row.chapter_id): row for row in existing_rows if row.chapter_id}

        chapter_ids = set(db_counts.keys()) | set(index_counts.keys()) | set(row_by_chapter.keys())
        if isinstance(chapter_limit, int) and chapter_limit > 0 and len(chapter_ids) > chapter_limit:
            chapter_ids = set(sorted(chapter_ids)[:chapter_limit])

        now_ts = self._utcnow()
        max_attempts = self._coerce_positive_int(settings.OPENSEARCH_SYNC_RETRY_MAX_ATTEMPTS, 6)
        status_counts: Dict[str, int] = {
            OpenSearchSyncStatusEnum.SYNCED.value: 0,
            OpenSearchSyncStatusEnum.DESYNCED.value: 0,
            OpenSearchSyncStatusEnum.FAILED.value: 0,
            OpenSearchSyncStatusEnum.DELETED.value: 0,
        }
        mismatched_examples: List[Dict[str, Any]] = []

        for chapter_id_text in chapter_ids:
            chapter_uuid = self._safe_uuid(chapter_id_text)
            if chapter_uuid is None:
                continue

            db_meta = db_counts.get(chapter_id_text) or {}
            index_meta = index_counts.get(chapter_id_text) or {}
            row = row_by_chapter.get(chapter_id_text)

            db_count = int(db_meta.get("count") or 0)
            index_count = int(index_meta.get("count") or 0)
            chapter_order_val: Optional[int] = None
            if isinstance(db_meta.get("chapter_order"), int):
                chapter_order_val = int(db_meta.get("chapter_order"))
            elif isinstance(index_meta.get("chapter_order"), int):
                chapter_order_val = int(index_meta.get("chapter_order"))
            elif row is not None and isinstance(row.chapter_order, int):
                chapter_order_val = int(row.chapter_order)

            if row is None:
                row = OpenSearchSyncStatus(
                    work_id=work_uuid,
                    chapter_id=chapter_uuid,
                )
                self.db.add(row)

            if db_count == 0 and index_count == 0:
                new_status = OpenSearchSyncStatusEnum.DELETED
            elif db_count == index_count:
                new_status = OpenSearchSyncStatusEnum.SYNCED
            else:
                if row.sync_status == OpenSearchSyncStatusEnum.FAILED:
                    new_status = OpenSearchSyncStatusEnum.FAILED
                else:
                    new_status = OpenSearchSyncStatusEnum.DESYNCED

            row.work_id = work_uuid
            row.chapter_id = chapter_uuid
            row.chapter_order = chapter_order_val
            row.sync_status = new_status
            row.last_operation = "audit"
            row.db_vector_count = db_count
            row.index_vector_count = index_count
            row.last_synced_at = now_ts
            if new_status in (OpenSearchSyncStatusEnum.SYNCED, OpenSearchSyncStatusEnum.DELETED):
                row.retry_count = 0
                row.next_retry_at = None
                row.last_error = None
            else:
                if row.retry_count is None:
                    row.retry_count = 0
                if row.retry_count >= max_attempts:
                    row.last_error = row.last_error or "retry exhausted"
                elif row.next_retry_at is None:
                    row.next_retry_at = now_ts

            status_key = new_status.value
            status_counts[status_key] = status_counts.get(status_key, 0) + 1
            if db_count != index_count and len(mismatched_examples) < 20:
                mismatched_examples.append(
                    {
                        "chapter_id": chapter_id_text,
                        "chapter_order": chapter_order_val,
                        "db_count": db_count,
                        "index_count": index_count,
                        "status": status_key,
                    }
                )

        try:
            await self.db.commit()
        except Exception as exc:
            await self.db.rollback()
            logger.warning(
                "[OpenSearchSync] audit work commit failed: work_id=%s error=%s",
                work_id,
                exc,
            )
            return {
                "work_id": str(work_id),
                "chapters_checked": 0,
                "status_counts": {},
                "mismatched_examples": [],
                "error": "commit_failed",
            }

        return {
            "work_id": str(work_id),
            "chapters_checked": len(chapter_ids),
            "status_counts": status_counts,
            "mismatched_examples": mismatched_examples,
        }

    async def runtime_consistency_guard(self, work_id: str) -> Dict[str, Any]:
        if not settings.OPENSEARCH_RUNTIME_SYNC_CHECK_ENABLED:
            return {"checked": False, "reason": "disabled"}

        work_key = str(work_id)
        now_ts = time.time()
        interval_seconds = self._coerce_positive_int(
            settings.OPENSEARCH_RUNTIME_SYNC_CHECK_INTERVAL_SECONDS,
            180,
        )
        last_ts = self.__class__._last_runtime_sync_check_ts.get(work_key, 0.0)
        if now_ts - last_ts < float(interval_seconds):
            return {"checked": False, "reason": "interval_skip"}
        self.__class__._last_runtime_sync_check_ts[work_key] = now_ts

        retry_summary = await self.process_retry_queue(
            limit=self._coerce_positive_int(settings.OPENSEARCH_SYNC_RETRY_BATCH_SIZE, 20),
        )

        work_uuid = self._safe_uuid(work_key)
        if work_uuid is None:
            return {"checked": True, "retry": retry_summary, "reason": "invalid_work_id"}

        pending_stmt = select(func.count(OpenSearchSyncStatus.id)).where(
            OpenSearchSyncStatus.work_id == work_uuid,
            OpenSearchSyncStatus.sync_status.in_(
                [OpenSearchSyncStatusEnum.FAILED, OpenSearchSyncStatusEnum.DESYNCED]
            ),
        )
        pending_count = int((await self.db.execute(pending_stmt)).scalar() or 0)
        if pending_count <= 0:
            return {"checked": True, "retry": retry_summary, "pending": 0}

        chapter_limit_cfg = int(settings.OPENSEARCH_SYNC_AUDIT_CHAPTER_LIMIT_PER_WORK or 0)
        chapter_limit = chapter_limit_cfg if chapter_limit_cfg > 0 else None
        audit_summary = await self.audit_work_consistency(work_key, chapter_limit=chapter_limit)
        logger.info(
            "[OpenSearchSync] runtime audit: work_id=%s pending=%s retry=%s chapters_checked=%s",
            work_key,
            pending_count,
            retry_summary.get("processed", 0),
            audit_summary.get("chapters_checked", 0),
        )
        return {
            "checked": True,
            "retry": retry_summary,
            "pending": pending_count,
            "audit": audit_summary,
        }

    async def audit_all_works(
        self,
        work_limit: Optional[int] = None,
        chapter_limit_per_work: Optional[int] = None,
    ) -> Dict[str, Any]:
        retry_summary = await self.process_retry_queue(
            limit=self._coerce_positive_int(settings.OPENSEARCH_SYNC_RETRY_BATCH_SIZE, 20),
        )
        stmt = select(Work.id).order_by(Work.created_at.asc())
        if isinstance(work_limit, int) and work_limit > 0:
            stmt = stmt.limit(work_limit)

        rows = (await self.db.execute(stmt)).all()
        work_ids = [str(row[0]) for row in rows if row and row[0]]
        status_totals: Dict[str, int] = {
            OpenSearchSyncStatusEnum.SYNCED.value: 0,
            OpenSearchSyncStatusEnum.DESYNCED.value: 0,
            OpenSearchSyncStatusEnum.FAILED.value: 0,
            OpenSearchSyncStatusEnum.DELETED.value: 0,
        }
        summary = {
            "works_total": len(work_ids),
            "works_checked": 0,
            "chapters_checked": 0,
            "errors": 0,
            "retry": retry_summary,
            "status_totals": status_totals,
        }

        chapter_limit = (
            int(chapter_limit_per_work)
            if isinstance(chapter_limit_per_work, int) and chapter_limit_per_work > 0
            else None
        )
        for work_id_text in work_ids:
            try:
                report = await self.audit_work_consistency(work_id_text, chapter_limit=chapter_limit)
                summary["works_checked"] += 1
                summary["chapters_checked"] += int(report.get("chapters_checked", 0) or 0)
                for status_key, count_val in (report.get("status_counts") or {}).items():
                    status_totals[status_key] = status_totals.get(status_key, 0) + int(count_val or 0)
            except Exception as exc:
                summary["errors"] += 1
                logger.warning("[OpenSearchSync] audit work failed: work_id=%s error=%s", work_id_text, exc)

        return summary

    async def clear_index(self) -> None:
        """Clear all documents in the current index without deleting mappings."""
        await self.ensure_index()
        client = self._get_client()
        await asyncio.to_thread(
            client.delete_by_query,
            index=self.index_name,
            body={"query": {"match_all": {}}},
            conflicts="proceed",
            refresh=True,
        )
        self.__class__.reset_sync_cache()
        logger.info("[OpenSearchSearch] index cleared: %s", self.index_name)

    async def recreate_index(self) -> None:
        """Recreate index (drop + create)."""
        client = self._get_client()
        try:
            await asyncio.to_thread(client.indices.delete, index=self.index_name)
        except Exception:
            # index may not exist; ignore and continue
            pass
        self.__class__._index_ready = False
        self.__class__.reset_sync_cache()
        await self.ensure_index()

    async def sync_work_vectors(self, work_id: str) -> int:
        """Sync all vectors of a work from DB to OpenSearch index."""
        await self.ensure_index()
        client = self._get_client()

        work_uuid = UUID(work_id) if isinstance(work_id, str) else work_id

        stmt = (
            select(NovelChapterVector)
            .where(NovelChapterVector.work_id == work_uuid)
            .order_by(NovelChapterVector.chapter_order, NovelChapterVector.chunk_index)
        )
        result = await self.db.execute(stmt)
        vectors = result.scalars().all()

        await asyncio.to_thread(
            client.delete_by_query,
            index=self.index_name,
            body={"query": {"term": {"work_id": str(work_id)}}},
            conflicts="proceed",
            refresh=True,
        )

        if not vectors:
            self.__class__._synced_work_ids.add(str(work_id))
            logger.info("[OpenSearchSearch] sync work=%s, vectors=0", work_id)
            try:
                await self.audit_work_consistency(str(work_id))
            except Exception as audit_exc:
                logger.warning(
                    "[OpenSearchSync] post-sync audit skipped: work_id=%s error=%s",
                    work_id,
                    audit_exc,
                )
            return 0

        actions: List[Dict[str, Any]] = []
        for vector in vectors:
            actions.append(
                {
                    "_op_type": "index",
                    "_index": self.index_name,
                    "_id": str(vector.id),
                    "_source": {
                        "work_id": str(vector.work_id),
                        "chapter_id": str(vector.chapter_id),
                        "chapter_order": int(vector.chapter_order),
                        "chapter_title": vector.chapter_title or "",
                        "paragraph_index": int(vector.chunk_index),
                        "chunk_text": vector.chunk_text or "",
                        "node_id": vector.node_id or "",
                    },
                }
            )

        def _bulk_upsert() -> int:
            success, errors = helpers.bulk(
                client,
                actions,
                raise_on_error=False,
                refresh="wait_for",
            )
            if errors:
                logger.warning("[OpenSearchSearch] bulk index errors=%s", len(errors))
            return int(success or 0)

        success_count = await asyncio.to_thread(_bulk_upsert)
        self.__class__._synced_work_ids.add(str(work_id))
        logger.info(
            "[OpenSearchSearch] sync work=%s, vectors=%s, indexed=%s",
            work_id,
            len(vectors),
            success_count,
        )
        try:
            await self.audit_work_consistency(str(work_id))
        except Exception as audit_exc:
            logger.warning(
                "[OpenSearchSync] post-sync audit skipped: work_id=%s error=%s",
                work_id,
                audit_exc,
            )
        return success_count

    async def upsert_chapter_vectors(self, chapter_id: str) -> int:
        """Upsert one chapter's vectors to OpenSearch."""
        await self.ensure_index()
        client = self._get_client()

        chapter_uuid = UUID(chapter_id) if isinstance(chapter_id, str) else chapter_id
        stmt = (
            select(NovelChapterVector)
            .where(NovelChapterVector.chapter_id == chapter_uuid)
            .order_by(NovelChapterVector.chunk_index)
        )
        result = await self.db.execute(stmt)
        vectors = result.scalars().all()

        await asyncio.to_thread(
            client.delete_by_query,
            index=self.index_name,
            body={"query": {"term": {"chapter_id": str(chapter_id)}}},
            conflicts="proceed",
            refresh=True,
        )

        if not vectors:
            return 0

        actions: List[Dict[str, Any]] = []
        for vector in vectors:
            actions.append(
                {
                    "_op_type": "index",
                    "_index": self.index_name,
                    "_id": str(vector.id),
                    "_source": {
                        "work_id": str(vector.work_id),
                        "chapter_id": str(vector.chapter_id),
                        "chapter_order": int(vector.chapter_order),
                        "chapter_title": vector.chapter_title or "",
                        "paragraph_index": int(vector.chunk_index),
                        "chunk_text": vector.chunk_text or "",
                        "node_id": vector.node_id or "",
                    },
                }
            )

        def _bulk_upsert() -> int:
            success, errors = helpers.bulk(
                client,
                actions,
                raise_on_error=False,
                refresh="wait_for",
            )
            if errors:
                logger.warning(
                    "[OpenSearchSearch] chapter bulk errors chapter_id=%s errors=%s",
                    chapter_id,
                    len(errors),
                )
            return int(success or 0)

        success_count = await asyncio.to_thread(_bulk_upsert)
        if vectors:
            self.__class__._synced_work_ids.add(str(vectors[0].work_id))
        return success_count

    async def delete_chapter_vectors(self, chapter_id: str) -> None:
        await self.ensure_index()
        client = self._get_client()
        await asyncio.to_thread(
            client.delete_by_query,
            index=self.index_name,
            body={"query": {"term": {"chapter_id": str(chapter_id)}}},
            conflicts="proceed",
            refresh=True,
        )

    async def ensure_work_synced(self, work_id: str) -> None:
        work_key = str(work_id)
        if work_key in self.__class__._synced_work_ids:
            return

        await self.ensure_index()
        client = self._get_client()

        count_resp = await asyncio.to_thread(
            client.count,
            index=self.index_name,
            body={"query": {"term": {"work_id": work_key}}},
        )
        existing = int((count_resp or {}).get("count", 0))
        if existing > 0:
            self.__class__._synced_work_ids.add(work_key)
            return

        await self.sync_work_vectors(work_key)

    def _build_query(
        self,
        work_id: str,
        keywords: List[str],
        chapter_range: Optional[Tuple[Optional[int], Optional[int]]],
        match_mode: str,
        terms_required: Optional[List[str]] = None,
        terms_optional: Optional[List[str]] = None,
        terms_excluded: Optional[List[str]] = None,
        proximity_terms: Optional[List[str]] = None,
        proximity_window: Optional[int] = None,
    ) -> Dict[str, Any]:
        must: List[Dict[str, Any]] = [{"term": {"work_id": str(work_id)}}]
        should: List[Dict[str, Any]] = []
        must_not: List[Dict[str, Any]] = []

        if chapter_range:
            min_order, max_order = chapter_range
            range_body: Dict[str, Any] = {}
            if min_order is not None:
                range_body["gte"] = int(min_order)
            if max_order is not None:
                range_body["lte"] = int(max_order)
            if range_body:
                must.append({"range": {"chapter_order": range_body}})

        required_terms = [kw for kw in (terms_required or []) if isinstance(kw, str) and kw.strip()]
        optional_terms = [kw for kw in (terms_optional or []) if isinstance(kw, str) and kw.strip()]
        excluded_terms = [kw for kw in (terms_excluded or []) if isinstance(kw, str) and kw.strip()]
        proximity_list = [kw for kw in (proximity_terms or []) if isinstance(kw, str) and kw.strip()]
        all_terms = [kw for kw in keywords if isinstance(kw, str) and kw.strip()]
        if not required_terms:
            required_terms = list(all_terms)
        if not all_terms:
            all_terms = list(required_terms) + list(optional_terms)

        for term in excluded_terms:
            must_not.append(
                {
                    "bool": {
                        "should": [
                            {"match_phrase": {"chunk_text": term}},
                            {
                                "match": {
                                    "chunk_text": {
                                        "query": term,
                                        "operator": "and",
                                    }
                                }
                            },
                        ],
                        "minimum_should_match": 1,
                    }
                }
            )

        if match_mode == "phrase":
            phrase_term = required_terms[0] if required_terms else (all_terms[0] if all_terms else "")
            if phrase_term:
                must.append({"match_phrase": {"chunk_text": phrase_term}})
            for kw in optional_terms:
                should.append({"match_phrase": {"chunk_text": {"query": kw, "boost": 1.4}}})
        elif match_mode == "all":
            for kw in required_terms:
                must.append({"match_phrase": {"chunk_text": kw}})
            for kw in optional_terms:
                should.append({"match_phrase": {"chunk_text": {"query": kw, "boost": 1.2}}})
        else:
            # recall 层：使用 match（宽松召回），并保留 phrase 提升分数以减少纯噪声
            recall_terms = required_terms or all_terms
            recall_should: List[Dict[str, Any]] = []
            for kw in recall_terms:
                recall_should.append(
                    {
                        "match": {
                            "chunk_text": {
                                "query": kw,
                                "operator": "and",
                                "minimum_should_match": "70%",
                            }
                        }
                    }
                )
                recall_should.append(
                    {
                        "match_phrase": {
                            "chunk_text": {
                                "query": kw,
                                "boost": 2.0,
                            }
                        }
                    }
                )
            if recall_should:
                must.append({"bool": {"should": recall_should, "minimum_should_match": 1}})
            for kw in optional_terms:
                should.append({"match_phrase": {"chunk_text": {"query": kw, "boost": 1.2}}})

        proximity_window_val = 12
        if isinstance(proximity_window, int) and proximity_window > 0:
            proximity_window_val = min(proximity_window, 50)
        proximity_candidates = proximity_list or required_terms[:2]
        if len(proximity_candidates) >= 2:
            pair_limit = min(len(proximity_candidates), 3)
            for i in range(pair_limit):
                for j in range(i + 1, pair_limit):
                    pair_query = f"{proximity_candidates[i]} {proximity_candidates[j]}".strip()
                    if not pair_query:
                        continue
                    should.append(
                        {
                            "match_phrase": {
                                "chunk_text": {
                                    "query": pair_query,
                                    "slop": proximity_window_val,
                                    "boost": 1.8,
                                }
                            }
                        }
                    )

        bool_query: Dict[str, Any] = {"must": must}
        if should:
            bool_query["should"] = should
        if must_not:
            bool_query["must_not"] = must_not
        return {"bool": bool_query}

    async def search_paragraphs(
        self,
        work_id: str,
        keywords: Optional[List[str]] = None,
        chapter_range: Optional[Tuple[Optional[int], Optional[int]]] = None,
        match_mode: str = "any",
        limit: int = 100,
        terms_required: Optional[List[str]] = None,
        terms_optional: Optional[List[str]] = None,
        terms_excluded: Optional[List[str]] = None,
        proximity_terms: Optional[List[str]] = None,
        proximity_window: Optional[int] = None,
    ) -> List[Dict[str, Any]]:
        def _normalize_pairs(values: Optional[List[str]]) -> List[Tuple[str, str]]:
            pairs: List[Tuple[str, str]] = []
            seen = set()
            for raw in values or []:
                if not isinstance(raw, str):
                    continue
                text = raw.strip()
                if not text:
                    continue
                key = text.lower()
                if key in seen:
                    continue
                seen.add(key)
                pairs.append((text, key))
            return pairs

        kw_pairs = _normalize_pairs(keywords)
        required_pairs = _normalize_pairs(terms_required)
        optional_pairs = _normalize_pairs(terms_optional)
        excluded_pairs = _normalize_pairs(terms_excluded)
        proximity_pairs = _normalize_pairs(proximity_terms)

        if not kw_pairs and not required_pairs and not optional_pairs and not proximity_pairs:
            logger.warning("[OpenSearchSearch] keywords empty")
            return []
        if not kw_pairs:
            kw_pairs = list(required_pairs) or list(optional_pairs) or list(proximity_pairs)

        try:
            limit_val = int(limit)
        except Exception:
            limit_val = 1
        if limit_val <= 0:
            limit_val = 1

        mode = (match_mode or "any").strip().lower()
        if mode not in ("any", "all", "phrase"):
            mode = "any"

        def _coerce_int(value: Any) -> Optional[int]:
            if isinstance(value, int):
                return value
            if isinstance(value, str):
                text = value.strip()
                if text.isdigit():
                    return int(text)
            return None

        try:
            await self.runtime_consistency_guard(str(work_id))
        except Exception as guard_exc:
            logger.warning("[OpenSearchSync] runtime consistency guard failed: work=%s error=%s", work_id, guard_exc)

        await self.ensure_work_synced(str(work_id))
        client = self._get_client()

        query = self._build_query(
            work_id=str(work_id),
            keywords=[kw for kw, _ in kw_pairs],
            chapter_range=chapter_range,
            match_mode=mode,
            terms_required=[kw for kw, _ in required_pairs],
            terms_optional=[kw for kw, _ in optional_pairs],
            terms_excluded=[kw for kw, _ in excluded_pairs],
            proximity_terms=[kw for kw, _ in proximity_pairs],
            proximity_window=proximity_window,
        )

        # limit 语义：单页大小（page_size），检索会自动翻页聚合命中
        page_size = min(max(limit_val, 1), 200)
        estimated_total: Optional[int] = None
        target_total: int
        try:
            count_resp = await asyncio.to_thread(
                client.count,
                index=self.index_name,
                body={"query": query},
            )
            estimated_total = int((count_resp or {}).get("count", 0))
        except Exception as exc:
            logger.warning("[OpenSearchSearch] count failed, fallback estimate: %s", exc)

        if estimated_total is not None and estimated_total <= 0:
            logger.info(
                "[OpenSearchSearch] search work=%s mode=%s range=%s keywords=%s hits=0 pages=0 page_size=%s est_total=0 target_total=0 truncated=False dropped_locator=0 dropped_unmatched=0",
                work_id,
                mode,
                chapter_range,
                [kw for kw, _ in kw_pairs][:3],
                page_size,
            )
            return []

        if estimated_total is not None:
            target_total = min(max(estimated_total, page_size), OPENSEARCH_SEARCH_MAX_RESULTS)
        else:
            target_total = min(max(page_size * 20, page_size), OPENSEARCH_SEARCH_MAX_RESULTS)

        search_after: Optional[List[Any]] = None
        page_count = 0
        max_pages = OPENSEARCH_SEARCH_MAX_PAGES
        results: List[Dict[str, Any]] = []
        seen_positions: set[Tuple[int, int]] = set()
        dropped_missing_locator = 0
        dropped_unmatched_keywords = 0
        dropped_excluded_terms = 0
        weak_literal_matches = 0
        paging_stop_reason = "unknown"
        while len(results) < target_total and page_count < max_pages:
            body: Dict[str, Any] = {
                "size": page_size,
                "query": query,
                "sort": [
                    {"chapter_order": {"order": "asc"}},
                    {"paragraph_index": {"order": "asc"}},
                ],
                "_source": [
                    "chapter_id",
                    "chapter_order",
                    "chapter_title",
                    "paragraph_index",
                    "chunk_text",
                    "node_id",
                ],
            }
            if search_after:
                body["search_after"] = search_after

            resp = await asyncio.to_thread(
                client.search,
                index=self.index_name,
                body=body,
            )
            hits = ((resp or {}).get("hits") or {}).get("hits") or []
            if not hits:
                paging_stop_reason = "no_more_hits"
                break

            page_count += 1
            for hit in hits:
                source = hit.get("_source") or {}
                chapter_order = _coerce_int(source.get("chapter_order"))
                paragraph_index = _coerce_int(source.get("paragraph_index"))
                if chapter_order is None or paragraph_index is None:
                    dropped_missing_locator += 1
                    continue

                text = source.get("chunk_text") or ""
                text_lower = text.lower()
                matched_keywords = [kw for kw, kw_lower in kw_pairs if kw_lower in text_lower]
                matched_required = [kw for kw, kw_lower in required_pairs if kw_lower in text_lower]
                matched_optional = [kw for kw, kw_lower in optional_pairs if kw_lower in text_lower]
                matched_excluded = [kw for kw, kw_lower in excluded_pairs if kw_lower in text_lower]
                if matched_excluded:
                    dropped_excluded_terms += 1
                    continue
                matched_by_recall = False
                if not matched_keywords:
                    # recall 或 analyzer 命中但字面不包含时，不再直接丢弃；
                    # 保留给上层 EvidenceJudge 判定，并在元数据中打弱命中标记。
                    matched_by_recall = True
                    weak_literal_matches += 1
                    if mode != "any":
                        dropped_unmatched_keywords += 1

                position_key = (chapter_order, paragraph_index)
                if position_key in seen_positions:
                    continue
                seen_positions.add(position_key)

                results.append(
                    {
                        "chapter_id": source.get("chapter_id") or "",
                        "chapter_order": chapter_order,
                        "chapter_title": source.get("chapter_title") or "",
                        "paragraph_index": paragraph_index,
                        "text": text,
                        "snippet": text[:200] + "..." if len(text) > 200 else text,
                        "node_id": source.get("node_id") or "",
                        "matched_keywords": matched_keywords,
                        "matched_required_terms": matched_required,
                        "matched_optional_terms": matched_optional,
                        "matched_by_recall": matched_by_recall,
                        "match_count": len(matched_keywords),
                        "weak_literal_match": matched_by_recall and not matched_keywords,
                    }
                )
                if len(results) >= target_total:
                    break

            last_sort = hits[-1].get("sort")
            if not isinstance(last_sort, list) or not last_sort:
                paging_stop_reason = "missing_search_after_sort"
                break
            search_after = last_sort

        if paging_stop_reason == "unknown":
            if len(results) >= target_total:
                paging_stop_reason = "target_total_reached"
            elif page_count >= max_pages:
                paging_stop_reason = "max_pages_reached"
            else:
                paging_stop_reason = "loop_exit"

        truncated = (
            len(results) >= target_total
            and (
                (estimated_total is not None and estimated_total > target_total)
                or page_count >= max_pages
            )
        )
        logger.info(
            "[OpenSearchSearch] search work=%s mode=%s range=%s keywords=%s hits=%s pages=%s page_size=%s est_total=%s target_total=%s truncated=%s dropped_locator=%s dropped_unmatched=%s dropped_excluded=%s weak_literal=%s stop_reason=%s",
            work_id,
            mode,
            chapter_range,
            [kw for kw, _ in kw_pairs][:3],
            len(results),
            page_count,
            page_size,
            estimated_total,
            target_total,
            truncated,
            dropped_missing_locator,
            dropped_unmatched_keywords,
            dropped_excluded_terms,
            weak_literal_matches,
            paging_stop_reason,
        )
        return results
