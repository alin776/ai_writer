"""
章节向量服务
专门用于RAG续写上下文检索，与分析系统解耦
"""
import logging
import os
import re
import time
from pathlib import Path
from typing import List, Dict, Any, Optional, Tuple
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, delete as sql_delete, func, or_, and_

# 确保在导入 sentence_transformers 前设置好镜像与缓存目录，避免访问 huggingface.co 超时
_default_hf_endpoint = os.getenv("HF_ENDPOINT", "https://hf-mirror.com")
os.environ.setdefault("HF_ENDPOINT", _default_hf_endpoint)
_hf_cache_dir = Path(__file__).resolve().parents[2] / "data" / "hf_cache"
_hf_cache_dir.mkdir(parents=True, exist_ok=True)
os.environ.setdefault("HF_HOME", str(_hf_cache_dir))
os.environ.setdefault("HF_HUB_CACHE", str(_hf_cache_dir))

from sentence_transformers import SentenceTransformer
import numpy as np

from app.models.novel_chapter_vector import NovelChapterVector
from app.models.chapter import Chapter
from app.models.chapter_content_index import ChapterContentIndex
from app.services.agent.utils.performance import MemoryCache

logger = logging.getLogger(__name__)

VECTOR_FRESHNESS_CACHE_TTL_SECONDS = 10
_VECTOR_FRESH_CACHE = MemoryCache(max_size=2000, default_ttl=None)


def _get_cached_vector_freshness(cache_key: str) -> Optional[bool]:
    cached = _VECTOR_FRESH_CACHE.get(cache_key)
    if not cached:
        return None
    expires_at = cached.get("expires_at")
    if not expires_at or expires_at <= time.time():
        _VECTOR_FRESH_CACHE.delete(cache_key)
        return None
    return cached.get("value")


def _set_cached_vector_freshness(cache_key: str, value: bool) -> None:
    _VECTOR_FRESH_CACHE.set(
        cache_key,
        {"value": value, "expires_at": time.time() + VECTOR_FRESHNESS_CACHE_TTL_SECONDS},
        ttl=None
    )


def invalidate_vector_fresh_cache(work_id: str) -> None:
    if not work_id:
        return
    prefix = f"{work_id}:"
    try:
        cache = _VECTOR_FRESH_CACHE
        with cache._lock:
            keys = [key for key in cache._cache.keys() if key.startswith(prefix)]
    except Exception:
        return
    for key in keys:
        _VECTOR_FRESH_CACHE.delete(key)


class ChapterVectorService:
    """章节向量服务 - 专门用于RAG续写"""

    # 使用与VectorStoreService相同的模型（保持一致性）
    MODEL_NAME = "paraphrase-multilingual-MiniLM-L12-v2"
    VECTOR_DIM = 384
    MAX_CHUNKS = 2000  # 保护性上限，防止超大文本生成过多向量
    MAX_CONTENT_SCAN_LEN = 200_000

    def __init__(self, db: AsyncSession):
        """
        初始化服务

        Args:
            db: 数据库会话
        """
        self.db = db

    def _get_model(self) -> SentenceTransformer:
        """
        获取Embedding模型（复用全局预加载的模型）

        Returns:
            SentenceTransformer: 模型实例
        """
        from app.services.vector_store_service import VectorStoreService

        # 复用VectorStoreService的全局模型
        if VectorStoreService._global_model is None:
            logger.info(f"正在加载Embedding模型: {self.MODEL_NAME}")
            VectorStoreService._global_model = SentenceTransformer(
                self.MODEL_NAME, cache_folder=str(VectorStoreService.CACHE_DIR)
            )
            logger.info("Embedding模型加载成功")

        return VectorStoreService._global_model

    def _split_by_paragraphs(self, content: str, max_paragraphs: Optional[int] = None) -> List[str]:
        """
        按段落切分内容（与前端编辑器结构对齐）

        Args:
            content: 章节内容（HTML 格式）
            max_paragraphs: 段落数量上限

        Returns:
            List[str]: 段落文本列表，索引即为 paragraph_index

        注意：不过滤短段落，保持与 locate_tools._split_paragraphs 索引一致
        """
        paragraphs = []

        # 优先按 HTML <p> 标签分割（与前端 Tiptap 一致）
        if '<p' in content:
            block_pattern = r'<(p|h[1-6]|blockquote|pre)[^>]*>(.*?)</\1>'
            matches = re.findall(block_pattern, content, re.DOTALL | re.IGNORECASE)

            for tag, inner_html in matches:
                # 去除内部 HTML 标签，只保留文本
                text = re.sub(r'<[^>]+>', '', inner_html).strip()
                if text:  # 只跳过空段落，不过滤短段落
                    paragraphs.append(text)
        else:
            # 纯文本模式：按换行分割
            raw_paragraphs = re.split(r'\n\n+|\n', content)
            for para in raw_paragraphs:
                para = para.strip()
                if para:  # 只跳过空段落
                    paragraphs.append(para)

        if max_paragraphs is not None and len(paragraphs) > max_paragraphs:
            logger.warning(f"段落数量 {len(paragraphs)} 超过上限 {max_paragraphs}，将截断")
            paragraphs = paragraphs[:max_paragraphs]

        return paragraphs

    def _split_by_paragraph_nodes(
        self,
        content: str,
        max_paragraphs: Optional[int] = None
    ) -> List[Dict[str, Any]]:
        """
        按段落切分内容，保留 node_id（与 locate_tools._split_paragraphs 对齐）
        """
        try:
            from app.services.agent.tools.locate_tools import _split_paragraphs
            paragraphs = _split_paragraphs(content)
        except Exception:
            paragraphs = []

        if max_paragraphs is not None and len(paragraphs) > max_paragraphs:
            logger.warning(f"段落数量 {len(paragraphs)} 超过上限 {max_paragraphs}，将截断")
            paragraphs = paragraphs[:max_paragraphs]

        return paragraphs

    def _cosine_similarity(self, a: np.ndarray, b: np.ndarray) -> float:
        """
        计算余弦相似度

        Args:
            a: 向量A
            b: 向量B

        Returns:
            float: 相似度（0-1）
        """
        return float(np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b)))

    async def store_chapter_vector(
        self,
        work_id: str,
        chapter_id: str,
        chapter_order: int,
        chapter_title: str,
        content: str,
        chunk_size: int = 500,
        max_chunks: Optional[int] = None
    ) -> int:
        """
        Store chapter content embeddings (idempotent).
        按段落生成向量，chunk_index 即为 paragraph_index。
        """
        try:
            logger.info(f"Vectorizing chapter: {chapter_title} (order={chapter_order})")

            # 1) delete old vectors (idempotent)
            stmt = sql_delete(NovelChapterVector).where(
                NovelChapterVector.chapter_id == chapter_id
            )
            await self.db.execute(stmt)
            await self.db.flush()

            # 2) 按段落切分（与编辑器结构对齐，保留 node_id）
            paragraphs = self._split_by_paragraph_nodes(content, max_paragraphs=max_chunks or self.MAX_CHUNKS)
            text_list = [p.get("text", "") for p in paragraphs if isinstance(p, dict)]

            if len(text_list) == 0:
                logger.warning(f"Skip vectorizing (no valid paragraphs): {chapter_title}")
                await self.db.commit()
                return 0

            # 3) encode
            model = self._get_model()
            embeddings = model.encode(text_list, normalize_embeddings=True)

            # 4) batch insert
            from uuid import UUID
            work_uuid = UUID(work_id) if isinstance(work_id, str) else work_id
            chapter_uuid = UUID(chapter_id) if isinstance(chapter_id, str) else chapter_id

            vectors = []
            for idx, (para, embedding) in enumerate(zip(paragraphs, embeddings)):
                if not isinstance(para, dict):
                    continue
                para_text = para.get("text", "")
                node_id = para.get("node_id")
                chunk_index = para.get("index", idx)
                vectors.append(NovelChapterVector(
                    work_id=work_uuid,
                    chapter_id=chapter_uuid,
                    chapter_order=chapter_order,
                    chapter_title=chapter_title,
                    chunk_index=chunk_index,  # chunk_index 即为 paragraph_index
                    chunk_text=para_text,
                    node_id=node_id,
                    embedding=embedding.tolist()
                ))

            self.db.add_all(vectors)
            await self.db.commit()

            logger.info(f"Stored chapter vectors: {chapter_title} ({len(text_list)} paragraphs)")
            return len(text_list)

        except Exception as e:
            logger.error(f"store_chapter_vector failed: {e}", exc_info=True)
            await self.db.rollback()
            raise
    async def retrieve_for_writing(
        self,
        work_id: str,
        current_chapter_order: int,
        query: str,
        top_k: int = 5,
        similarity_threshold: float = 0.3,
        include_current: bool = True,
        look_ahead: int = 0,
        min_order: Optional[int] = None,
        max_order: Optional[int] = None
    ) -> List[Dict[str, Any]]:
        """
        Retrieve context for continuation.
        返回 chapter_id 和 paragraph_index（chunk_index），支持精确定位。
        """
        try:
            logger.info(
                f"RAG retrieve work_id={work_id}, current_order={current_chapter_order}, query={query[:50]}..."
            )

            # 1) encode query
            model = self._get_model()
            query_embedding = model.encode([query], normalize_embeddings=True)[0]

            # 2) fetch vectors with window
            from uuid import UUID
            work_uuid = UUID(work_id) if isinstance(work_id, str) else work_id

            upper_order = max_order if max_order is not None else current_chapter_order + (look_ahead or 0)
            conditions = [NovelChapterVector.work_id == work_uuid]
            if isinstance(min_order, int):
                conditions.append(NovelChapterVector.chapter_order >= min_order)
            if include_current:
                conditions.append(NovelChapterVector.chapter_order <= upper_order)
            else:
                conditions.append(NovelChapterVector.chapter_order < upper_order)

            stmt = select(NovelChapterVector).where(*conditions)
            result = await self.db.execute(stmt)
            vectors = result.scalars().all()

            if len(vectors) == 0:
                logger.warning(f"no vectors for work {work_id} (order<= {upper_order})")
                return []

            # 3) similarity
            results = []
            for vector in vectors:
                embedding = np.array(vector.embedding)
                similarity = self._cosine_similarity(query_embedding, embedding)
                if similarity >= similarity_threshold:
                    results.append({
                        'chapter_id': str(vector.chapter_id),  # 新增
                        'chapter_title': vector.chapter_title,
                        'chapter_order': vector.chapter_order,
                        'paragraph_index': vector.chunk_index,  # 新增：chunk_index 即 paragraph_index
                        'chunk_text': vector.chunk_text,
                        'node_id': vector.node_id,
                        'similarity': float(similarity)
                    })

            results.sort(key=lambda x: x['similarity'], reverse=True)
            results = results[:top_k]

            logger.info(
                f"RAG retrieved {len(results)} segments within order<={upper_order}"
            )
            return results

        except Exception as e:
            logger.error(f"RAG retrieve failed: {e}", exc_info=True)
            return []
    async def delete_chapter_vectors(self, chapter_id: str) -> int:
        """
        删除章节的向量数据

        Args:
            chapter_id: 章节ID

        Returns:
            int: 删除的记录数
        """
        try:
            from uuid import UUID
            chapter_uuid = UUID(chapter_id) if isinstance(chapter_id, str) else chapter_id

            stmt = sql_delete(NovelChapterVector).where(
                NovelChapterVector.chapter_id == chapter_uuid
            )
            result = await self.db.execute(stmt)
            await self.db.commit()

            deleted_count = result.rowcount
            logger.info(f"删除章节 {chapter_id} 的 {deleted_count} 条向量记录")
            return deleted_count

        except Exception as e:
            logger.error(f"删除章节向量失败: {e}", exc_info=True)
            await self.db.rollback()
            raise

    async def get_stats(self, work_id: str) -> Dict[str, Any]:
        """
        获取作品的向量统计

        Args:
            work_id: 作品ID

        Returns:
            Dict: 统计信息
        """
        try:
            from uuid import UUID
            from sqlalchemy import func

            work_uuid = UUID(work_id) if isinstance(work_id, str) else work_id

            stmt = select(
                func.count(NovelChapterVector.id).label('total_vectors'),
                func.count(func.distinct(NovelChapterVector.chapter_id)).label('total_chapters')
            ).where(NovelChapterVector.work_id == work_uuid)

            result = await self.db.execute(stmt)
            row = result.first()

            return {
                'total_vectors': row.total_vectors if row else 0,
                'total_chapters': row.total_chapters if row else 0,
                'vector_dimension': self.VECTOR_DIM,
                'model_name': self.MODEL_NAME
            }

        except Exception as e:
            logger.error(f"获取向量统计失败: {e}", exc_info=True)
            return {
                'total_vectors': 0,
                'total_chapters': 0,
                'vector_dimension': self.VECTOR_DIM,
                'model_name': self.MODEL_NAME
            }

    # ==================== 精确搜索方法（Explore V2）====================

    async def are_vectors_fresh(
        self,
        work_id: str,
        chapter_ranges: Optional[List[Tuple[int, int]]] = None
    ) -> bool:
        """
        判断指定章节范围内的向量是否最新（vector.updated_at >= content_index.updated_at）
        """
        from uuid import UUID

        ranges_key = ""
        if chapter_ranges:
            ranges_key = ",".join(f"{start}-{end}" for start, end in chapter_ranges)
        cache_key = f"{work_id}:{ranges_key}"
        cached = _get_cached_vector_freshness(cache_key)
        if cached is not None:
            return cached

        try:
            work_uuid = UUID(work_id) if isinstance(work_id, str) else work_id

            stmt = select(Chapter.id).where(Chapter.work_id == work_uuid)
            if chapter_ranges:
                range_conditions = []
                for min_order, max_order in chapter_ranges:
                    conds = []
                    if min_order is not None:
                        conds.append(Chapter.order >= min_order)
                    if max_order is not None:
                        conds.append(Chapter.order <= max_order)
                    if conds:
                        range_conditions.append(and_(*conds))
                if range_conditions:
                    stmt = stmt.where(or_(*range_conditions))
            result = await self.db.execute(stmt)
            chapter_ids = [row[0] for row in result.all()]

            if not chapter_ids:
                _set_cached_vector_freshness(cache_key, True)
                return True

            index_stmt = select(
                ChapterContentIndex.chapter_id,
                ChapterContentIndex.updated_at
            ).where(ChapterContentIndex.chapter_id.in_(chapter_ids))
            index_result = await self.db.execute(index_stmt)
            index_map = {row[0]: row[1] for row in index_result}

            vec_stmt = (
                select(
                    NovelChapterVector.chapter_id,
                    func.max(NovelChapterVector.updated_at).label("updated_at"),
                    func.count(NovelChapterVector.id).label("vector_count")
                )
                .where(NovelChapterVector.chapter_id.in_(chapter_ids))
                .group_by(NovelChapterVector.chapter_id)
            )
            vec_result = await self.db.execute(vec_stmt)
            vector_map = {row[0]: {"updated_at": row[1], "count": row[2]} for row in vec_result}

            stale_count = 0
            for chapter_id in chapter_ids:
                content_updated_at = index_map.get(chapter_id)
                if content_updated_at is None:
                    stale_count += 1
                    continue
                vector_info = vector_map.get(chapter_id)
                if vector_info is None:
                    stale_count += 1
                    continue
                if vector_info["count"] >= self.MAX_CHUNKS:
                    stale_count += 1
                    continue
                if vector_info["updated_at"] < content_updated_at:
                    stale_count += 1

            if stale_count > 0:
                logger.info("[vector_freshness] stale=%s total=%s", stale_count, len(chapter_ids))
                _set_cached_vector_freshness(cache_key, False)
                return False

            _set_cached_vector_freshness(cache_key, True)
            return True

        except Exception as e:
            logger.error(f"[vector_freshness] 判断失败: {e}", exc_info=True)
            return False

    async def exact_search_paragraphs(
        self,
        work_id: str,
        keywords: List[str],
        chapter_range: Optional[tuple] = None,
        match_mode: str = "any",
        limit: int = 100
    ) -> List[Dict[str, Any]]:
        """
        精确搜索：在段落文本中搜索包含关键词的段落（确定性，不走向量）

        Args:
            work_id: 作品ID
            keywords: 关键词列表
            chapter_range: 章节范围 (min_order, max_order)，None 表示全部
            match_mode: 匹配模式
                - "any": 任一关键词匹配（OR）
                - "all": 所有关键词都匹配（AND）
                - "phrase": 第一个关键词作为精确短语匹配
            limit: 返回结果数量上限

        Returns:
            List[Dict]: 命中的段落列表
        """
        from uuid import UUID
        from sqlalchemy import or_, and_

        try:
            work_uuid = UUID(work_id) if isinstance(work_id, str) else work_id

            if not keywords:
                logger.warning("[exact_search] 关键词为空")
                return []
            try:
                limit_val = int(limit)
            except Exception:
                limit_val = 0
            if limit_val <= 0:
                logger.warning("[exact_search] limit非法(%s)，已回退为1", limit)
                limit_val = 1

            # 构建基础查询
            stmt = select(NovelChapterVector).where(
                NovelChapterVector.work_id == work_uuid
            )

            # 章节范围约束
            if chapter_range:
                min_order, max_order = chapter_range
                if min_order is not None:
                    stmt = stmt.where(NovelChapterVector.chapter_order >= min_order)
                if max_order is not None:
                    stmt = stmt.where(NovelChapterVector.chapter_order <= max_order)

            # 关键词匹配条件
            if match_mode == "phrase":
                # 精确短语匹配（第一个关键词）
                stmt = stmt.where(
                    NovelChapterVector.chunk_text.ilike(f"%{keywords[0]}%")
                )
            elif match_mode == "all":
                # AND：所有关键词都必须匹配
                conditions = [
                    NovelChapterVector.chunk_text.ilike(f"%{kw}%")
                    for kw in keywords
                ]
                stmt = stmt.where(and_(*conditions))
            else:
                # OR：任一关键词匹配（默认）
                conditions = [
                    NovelChapterVector.chunk_text.ilike(f"%{kw}%")
                    for kw in keywords
                ]
                stmt = stmt.where(or_(*conditions))

            # 按章节和段落排序
            stmt = stmt.order_by(
                NovelChapterVector.chapter_order,
                NovelChapterVector.chunk_index
            ).limit(limit_val)

            # 执行查询
            result = await self.db.execute(stmt)
            vectors = result.scalars().all()

            # 构建返回结果
            results = []
            for v in vectors:
                # 记录匹配到的关键词
                matched = [kw for kw in keywords if kw.lower() in v.chunk_text.lower()]
                results.append({
                    "chapter_id": str(v.chapter_id),
                    "chapter_order": v.chapter_order,
                    "chapter_title": v.chapter_title,
                    "paragraph_index": v.chunk_index,
                    "text": v.chunk_text,
                    "snippet": v.chunk_text[:200] + "..." if len(v.chunk_text) > 200 else v.chunk_text,
                    "node_id": v.node_id,
                    "matched_keywords": matched,
                    "match_count": len(matched)
                })

            logger.info(
                f"[exact_search] work={work_id}, keywords={keywords[:3]}..., "
                f"mode={match_mode}, range={chapter_range}, hits={len(results)}"
            )

            return results

        except Exception as e:
            logger.error(f"[exact_search] 精确搜索失败: {e}", exc_info=True)
            return []

    async def exact_search_paragraphs_from_content(
        self,
        work_id: str,
        keywords: List[str],
        chapter_range: Optional[tuple] = None,
        match_mode: str = "any",
        limit: int = 100
    ) -> List[Dict[str, Any]]:
        """
        精确搜索（实时正文版）：直接读取最新章节内容切段后匹配

        Args:
            work_id: 作品ID
            keywords: 关键词列表
            chapter_range: 章节范围 (min_order, max_order)，None 表示全部
            match_mode: 匹配模式（any/all/phrase）
            limit: 返回结果数量上限

        Returns:
            List[Dict]: 命中的段落列表
        """
        from uuid import UUID
        from app.services.chapter_content_provider import ChapterContentProvider
        from app.services.agent.tools.locate_tools import _split_paragraphs

        try:
            work_uuid = UUID(work_id) if isinstance(work_id, str) else work_id

            kw_pairs = [(kw, kw.lower()) for kw in (keywords or []) if isinstance(kw, str) and kw.strip()]
            if not kw_pairs:
                logger.warning("[exact_search_content] 关键词为空")
                return []
            try:
                limit_val = int(limit)
            except Exception:
                limit_val = 0
            if limit_val <= 0:
                logger.warning("[exact_search_content] limit非法(%s)，已回退为1", limit)
                limit_val = 1

            def _iter_paragraphs_stream(html_content: str):
                index = 0
                if any(tag in html_content for tag in ("<p", "<li", "<h", "<blockquote", "<pre")):
                    block_pattern = re.compile(
                        r"<(p|h[1-6]|blockquote|pre|li)([^>]*)>(.*?)</\1>",
                        re.DOTALL | re.IGNORECASE
                    )
                    matched_any = False
                    for match in block_pattern.finditer(html_content):
                        inner_html = match.group(3)
                        text = re.sub(r"<[^>]+>", "", inner_html).strip()
                        if not text:
                            continue
                        node_id = None
                        attrs = match.group(2) or ""
                        id_match = re.search(r'data-id=["\']([^"\']+)["\']', attrs, re.IGNORECASE)
                        if id_match:
                            node_id = id_match.group(1)
                        yield {"index": index, "text": text, "node_id": node_id}
                        index += 1
                        matched_any = True
                    if matched_any:
                        return

                for para in re.split(r"\n\n+|\n", html_content):
                    text = para.strip()
                    if not text:
                        continue
                    yield {"index": index, "text": text, "node_id": None}
                    index += 1

            stmt = select(Chapter).where(Chapter.work_id == work_uuid)
            if chapter_range:
                min_order, max_order = chapter_range
                if min_order is not None:
                    stmt = stmt.where(Chapter.order >= min_order)
                if max_order is not None:
                    stmt = stmt.where(Chapter.order <= max_order)
            stmt = stmt.order_by(Chapter.order)

            result = await self.db.execute(stmt)
            chapters = result.scalars().all()

            content_provider = ChapterContentProvider()
            results: List[Dict[str, Any]] = []

            for chapter in chapters:
                if len(results) >= limit_val:
                    break
                content = content_provider.read_content(str(chapter.work_id), str(chapter.id)) or ""
                if not content:
                    continue

                content_lower = content.lower()
                if match_mode == "phrase":
                    if kw_pairs[0][1] not in content_lower:
                        continue
                elif match_mode == "all":
                    if any(kw_lower not in content_lower for _, kw_lower in kw_pairs):
                        continue
                else:
                    if not any(kw_lower in content_lower for _, kw_lower in kw_pairs):
                        continue

                if len(content) > self.MAX_CONTENT_SCAN_LEN:
                    paragraph_iter = _iter_paragraphs_stream(content)
                else:
                    paragraphs = _split_paragraphs(content)
                    if not paragraphs:
                        rough = []
                        for idx, part in enumerate([p for p in content.split("\n\n") if p.strip()]):
                            rough.append({"index": idx, "text": part.strip(), "node_id": None})
                        if not rough:
                            chunk_size = 500
                            parts = [
                                content[i:i + chunk_size]
                                for i in range(0, len(content), chunk_size)
                                if content[i:i + chunk_size].strip()
                            ]
                            for idx, part in enumerate(parts):
                                rough.append({"index": idx, "text": part.strip(), "node_id": None})
                        paragraphs = rough
                    paragraph_iter = paragraphs

                for para in paragraph_iter:
                    text = (para.get("text") or "").strip()
                    if not text:
                        continue
                    text_lower = text.lower()

                    matched: List[str] = []
                    if match_mode == "phrase":
                        first_kw, first_kw_lower = kw_pairs[0]
                        if first_kw_lower in text_lower:
                            matched = [first_kw]
                    elif match_mode == "all":
                        if all(kw_lower in text_lower for _, kw_lower in kw_pairs):
                            matched = [kw for kw, kw_lower in kw_pairs if kw_lower in text_lower]
                    else:
                        matched = [kw for kw, kw_lower in kw_pairs if kw_lower in text_lower]

                    if not matched:
                        continue

                    results.append({
                        "chapter_id": str(chapter.id),
                        "chapter_order": chapter.order,
                        "chapter_title": chapter.title,
                        "paragraph_index": para.get("index", 0),
                        "text": text,
                        "snippet": text[:200] + "..." if len(text) > 200 else text,
                        "node_id": para.get("node_id"),
                        "matched_keywords": matched,
                        "match_count": len(matched)
                    })

                    if len(results) >= limit_val:
                        logger.info(
                            f"[exact_search_content] work={work_id}, keywords={keywords[:3]}..., "
                            f"mode={match_mode}, range={chapter_range}, hits={len(results)}"
                        )
                        return results

            logger.info(
                f"[exact_search_content] work={work_id}, keywords={keywords[:3]}..., "
                f"mode={match_mode}, range={chapter_range}, hits={len(results)}"
            )
            return results

        except Exception as e:
            logger.error(f"[exact_search_content] 实时精确搜索失败: {e}", exc_info=True)
            return []

