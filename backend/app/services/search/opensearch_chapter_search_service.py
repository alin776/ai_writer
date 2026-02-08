"""
OpenSearch chapter paragraph search service.

This service provides keyword paragraph retrieval for Explore exact search.
"""

import asyncio
import logging
from typing import Any, Dict, List, Optional, Tuple
from uuid import UUID

from opensearchpy import OpenSearch, helpers
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import settings
from app.models.novel_chapter_vector import NovelChapterVector

logger = logging.getLogger(__name__)

OPENSEARCH_SEARCH_MAX_PAGES = 500
OPENSEARCH_SEARCH_MAX_RESULTS = 5000


class OpenSearchChapterSearchService:
    """Keyword paragraph search powered by OpenSearch."""

    _client: Optional[OpenSearch] = None
    _index_ready: bool = False
    _synced_work_ids: set[str] = set()

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
    ) -> Dict[str, Any]:
        must: List[Dict[str, Any]] = [{"term": {"work_id": str(work_id)}}]

        if chapter_range:
            min_order, max_order = chapter_range
            range_body: Dict[str, Any] = {}
            if min_order is not None:
                range_body["gte"] = int(min_order)
            if max_order is not None:
                range_body["lte"] = int(max_order)
            if range_body:
                must.append({"range": {"chapter_order": range_body}})

        if match_mode == "phrase":
            must.append({"match_phrase": {"chunk_text": keywords[0]}})
            return {"bool": {"must": must}}

        if match_mode == "all":
            for kw in keywords:
                must.append({"match_phrase": {"chunk_text": kw}})
            return {"bool": {"must": must}}

        should = [{"match_phrase": {"chunk_text": kw}} for kw in keywords]
        must.append({"bool": {"should": should, "minimum_should_match": 1}})
        return {"bool": {"must": must}}

    async def search_paragraphs(
        self,
        work_id: str,
        keywords: Optional[List[str]] = None,
        chapter_range: Optional[Tuple[Optional[int], Optional[int]]] = None,
        match_mode: str = "any",
        limit: int = 100,
    ) -> List[Dict[str, Any]]:
        kw_pairs = [
            (kw.strip(), kw.strip().lower())
            for kw in (keywords or [])
            if isinstance(kw, str) and kw.strip()
        ]
        if not kw_pairs:
            logger.warning("[OpenSearchSearch] keywords empty")
            return []

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

        await self.ensure_work_synced(str(work_id))
        client = self._get_client()

        query = self._build_query(
            work_id=str(work_id),
            keywords=[kw for kw, _ in kw_pairs],
            chapter_range=chapter_range,
            match_mode=mode,
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
                if not matched_keywords:
                    dropped_unmatched_keywords += 1
                    continue

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
                        "match_count": len(matched_keywords),
                    }
                )
                if len(results) >= target_total:
                    break

            last_sort = hits[-1].get("sort")
            if not isinstance(last_sort, list) or not last_sort:
                break
            search_after = last_sort

        truncated = (
            len(results) >= target_total
            and (
                (estimated_total is not None and estimated_total > target_total)
                or page_count >= max_pages
            )
        )
        logger.info(
            "[OpenSearchSearch] search work=%s mode=%s range=%s keywords=%s hits=%s pages=%s page_size=%s est_total=%s target_total=%s truncated=%s dropped_locator=%s dropped_unmatched=%s",
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
        )
        return results
