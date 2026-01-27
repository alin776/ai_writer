# -*- coding: utf-8 -*-
"""
HybridRetriever: 结合向量检索与全文模糊匹配，提高长文本作品的召回率。

设计要点：
- 先用 ChapterVectorService 做语义召回，再用章节全文 ILIKE 做精确/模糊命中。
- 可选 current_order / look_ahead 控制时序窗口，默认包含当前章及之后少量章节。
- 结果去重后按 similarity 倒序返回。
- 全文检索使用 jieba 分词提取关键词，OR 条件匹配（避免完整 query 无法命中）。
- v2.0: 增加 Rerank 重排序，使用 CrossEncoder 提升精准度。
- v2.1: 增加 Rerank 缓存，避免重复计算（同一 query + candidates 组合）。
"""

import asyncio
import hashlib
import logging
import os
import re
import time
from collections import OrderedDict
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
from threading import Lock
from typing import List, Dict, Any, Optional
from uuid import UUID

import jieba
import jieba.analyse
from sqlalchemy import select, or_
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.chapter import Chapter
from app.models.chapter_content_index import ChapterContentIndex
from app.services.chapter_content_provider import ChapterContentProvider
from app.services.chapter_vector_service import ChapterVectorService

logger = logging.getLogger(__name__)

# ==================== Reranker 全局单例 ====================
_global_reranker = None
_RERANKER_MODEL = "BAAI/bge-reranker-base"  # 中文优化的 reranker 模型
_rerank_executor = ThreadPoolExecutor(max_workers=1, thread_name_prefix="reranker")

# ==================== Reranker 缓存 ====================
_RERANK_CACHE_MAX_SIZE = 100  # 最多缓存 100 个结果
_RERANK_CACHE_TTL = 600  # 缓存有效期 10 分钟
_rerank_cache: OrderedDict[str, tuple] = OrderedDict()  # key -> (result, timestamp)
_rerank_cache_lock = Lock()


def _get_rerank_cache_key(query: str, candidates: List[Dict[str, Any]]) -> str:
    """生成 Rerank 缓存的 key（基于 query + candidates 唯一标识的 hash）

    v2.2: 使用 chapter_id + paragraph_index 作为唯一标识，避免内容截断导致的哈希碰撞
    """
    # 使用 chapter_id + paragraph_index 作为唯一标识（比内容截断更可靠）
    ids = []
    for c in candidates:
        chapter_id = c.get("chapter_id", "")
        para_idx = c.get("paragraph_index", "")
        chapter_order = c.get("chapter_order", "")
        # 优先使用 chapter_id，兜底使用 chapter_order + content hash
        if chapter_id:
            unique_id = f"{chapter_id}:{para_idx}"
        else:
            content_hash = hashlib.md5(c.get("content", "").encode()).hexdigest()[:8]
            unique_id = f"{chapter_order}:{para_idx}:{content_hash}"
        ids.append(unique_id)

    # 排序确保相同 candidates 不同顺序产生相同 key
    ids.sort()
    combined = f"{query}||{'|'.join(ids)}"
    return hashlib.md5(combined.encode()).hexdigest()


def _get_from_rerank_cache(cache_key: str) -> Optional[List[Dict[str, Any]]]:
    """从缓存获取 Rerank 结果"""
    with _rerank_cache_lock:
        if cache_key not in _rerank_cache:
            return None
        result, timestamp = _rerank_cache[cache_key]
        # 检查是否过期
        if time.time() - timestamp > _RERANK_CACHE_TTL:
            del _rerank_cache[cache_key]
            return None
        # LRU: 移动到末尾
        _rerank_cache.move_to_end(cache_key)
        return result


def _set_to_rerank_cache(cache_key: str, result: List[Dict[str, Any]]) -> None:
    """设置 Rerank 缓存"""
    with _rerank_cache_lock:
        # 如果缓存已满，删除最旧的
        while len(_rerank_cache) >= _RERANK_CACHE_MAX_SIZE:
            _rerank_cache.popitem(last=False)
        _rerank_cache[cache_key] = (result, time.time())


def _get_reranker():
    """获取全局 Reranker 模型（懒加载单例）"""
    global _global_reranker
    if _global_reranker is None:
        try:
            from sentence_transformers import CrossEncoder

            # 设置 HuggingFace 镜像
            _default_hf_endpoint = os.getenv("HF_ENDPOINT", "https://hf-mirror.com")
            os.environ.setdefault("HF_ENDPOINT", _default_hf_endpoint)
            _hf_cache_dir = Path(__file__).resolve().parents[2] / "data" / "hf_cache"
            _hf_cache_dir.mkdir(parents=True, exist_ok=True)
            os.environ.setdefault("HF_HOME", str(_hf_cache_dir))

            logger.info(f"[Reranker] 正在加载模型: {_RERANKER_MODEL}")
            _global_reranker = CrossEncoder(_RERANKER_MODEL, max_length=512)
            logger.info("[Reranker] 模型加载成功")
        except Exception as e:
            logger.warning(f"[Reranker] 模型加载失败，将跳过重排序: {e}")
            _global_reranker = False  # 标记为加载失败，避免重复尝试
    return _global_reranker if _global_reranker else None


def _sync_rerank(reranker, pairs: List[tuple]) -> List[float]:
    """同步执行 rerank（在线程池中运行）"""
    return reranker.predict(pairs).tolist()

# 中文停用词（疑问词、助词等）
_STOPWORDS = {
    "的", "是", "在", "了", "和", "与", "或", "有", "什么", "怎么", "如何",
    "为什么", "哪里", "哪个", "谁", "吗", "呢", "吧", "啊", "呀", "哦",
    "这", "那", "这个", "那个", "一个", "一些", "这些", "那些",
}


class HybridRetriever:
    def __init__(self, db: AsyncSession):
        self.db = db
        self.vector_service = ChapterVectorService(db)
        self.content_provider = ChapterContentProvider()

    async def _rerank(self, query: str, candidates: List[Dict[str, Any]], top_k: int) -> List[Dict[str, Any]]:
        """
        使用 CrossEncoder 对候选结果进行重排序（异步，不阻塞事件循环）。

        v2.1: 增加缓存机制，避免重复计算同一 query + candidates 组合。

        Args:
            query: 用户查询
            candidates: 候选结果列表
            top_k: 返回数量

        Returns:
            重排序后的结果列表
        """
        if not candidates:
            return []

        # v2.1: 检查缓存
        cache_key = _get_rerank_cache_key(query, candidates)
        cached_result = _get_from_rerank_cache(cache_key)
        if cached_result is not None:
            logger.info(f"[Rerank] 缓存命中: {len(cached_result)} 个结果")
            return cached_result[:top_k]

        reranker = _get_reranker()
        if reranker is None:
            # Reranker 不可用，返回原始排序
            logger.warning("[Rerank] ⚠️ Reranker 模型不可用，检索质量可能下降。请检查 BAAI/bge-reranker-base 模型是否正确加载。")
            return candidates[:top_k]

        try:
            # 构建 query-document pairs
            pairs = [(query, c["content"]) for c in candidates]

            # 在线程池中执行同步的 rerank 操作，避免阻塞事件循环
            loop = asyncio.get_running_loop()
            scores = await loop.run_in_executor(_rerank_executor, _sync_rerank, reranker, pairs)

            # 更新分数并排序
            for i, c in enumerate(candidates):
                c["rerank_score"] = float(scores[i])

            # 按 rerank_score 降序排序
            reranked = sorted(candidates, key=lambda x: x["rerank_score"], reverse=True)

            # v2.1: 存入缓存
            _set_to_rerank_cache(cache_key, reranked)

            logger.info(f"[Rerank] 重排序完成: {len(candidates)} 个候选 -> top {top_k}")
            return reranked[:top_k]

        except Exception as e:
            logger.warning(f"[Rerank] 重排序失败，使用原始排序: {e}")
            return candidates[:top_k]

    def _extract_keywords(self, query: str, topK: int = 5) -> List[str]:
        """
        从查询中提取关键词（使用 jieba TF-IDF）。

        Args:
            query: 用户查询
            topK: 最多返回关键词数量

        Returns:
            关键词列表（已去除停用词），可能为空列表
        """
        if not query or not query.strip():
            return []

        # 1. 尝试 TF-IDF 提取（自动过滤停用词）
        keywords = jieba.analyse.extract_tags(query, topK=topK, withWeight=False)

        # 2. TF-IDF 无结果时，退回普通分词
        if not keywords:
            words = jieba.cut(query)
            keywords = [
                w for w in words
                if len(w) >= 2 and w not in _STOPWORDS
            ][:topK]

        # 3. 最终安全过滤：确保无停用词（TF-IDF 可能遗漏某些词）
        keywords = [kw for kw in keywords if kw and kw not in _STOPWORDS]

        logger.debug(f"[HybridRetriever] query={query!r} -> keywords={keywords}")
        return keywords

    def _split_by_paragraphs(self, content: str) -> List[str]:
        if not content:
            return []
        paragraphs: List[str] = []
        if "<p" in content:
            block_pattern = r"<(p|h[1-6]|blockquote|pre)[^>]*>(.*?)</\1>"
            matches = re.findall(block_pattern, content, re.DOTALL | re.IGNORECASE)
            for _, inner_html in matches:
                text = re.sub(r"<[^>]+>", "", inner_html).strip()
                if text:
                    paragraphs.append(text)
        else:
            raw_paragraphs = re.split(r"\n\n+|\n", content)
            for para in raw_paragraphs:
                para = para.strip()
                if para:
                    paragraphs.append(para)
        return paragraphs

    def _infer_paragraph_index(
        self,
        content: str,
        snippet: str,
        keywords: List[str]
    ) -> Optional[int]:
        paragraphs = self._split_by_paragraphs(content)
        if not paragraphs:
            return None

        anchor = re.sub(r"\s+", " ", (snippet or "").strip())
        if anchor:
            anchor_lower = anchor.lower()
            if len(anchor_lower) > 80:
                anchor_lower = anchor_lower[:80]
            for idx, para in enumerate(paragraphs):
                if anchor_lower in para.lower():
                    return idx

        if keywords:
            lowered_paras = [p.lower() for p in paragraphs]
            for kw in keywords:
                kw_lower = kw.lower()
                if not kw_lower:
                    continue
                for idx, para in enumerate(lowered_paras):
                    if kw_lower in para:
                        return idx

        return None

    async def search(
        self,
        work_id: str,
        query: str,
        current_order: Optional[int] = None,
        top_k: int = 8,
        include_current: bool = True,
        look_ahead: Optional[int] = None,
        similarity_threshold: float = 0.25,
        min_keyword_match: int = 1,
        min_order: Optional[int] = None,
        max_order: Optional[int] = None,
    ) -> List[Dict[str, Any]]:
        """
        混合检索入口。

        Args:
            work_id: 作品ID
            query: 用户查询
            current_order: 当前章节序号（可选，用于窗口限制）
            top_k: 期望返回数量
            include_current: 是否包含当前章
            look_ahead: 允许向后看的章节数（None 表示不限制）
            similarity_threshold: 向量相似度阈值
            min_keyword_match: 全文检索最少需要匹配的关键词数量（默认1）
        """
        # ========== 1) 向量检索 ==========
        # look_ahead=None 表示不限制时序窗口
        vector_results = await self.vector_service.retrieve_for_writing(
            work_id=work_id,
            current_chapter_order=max_order if max_order is not None else (current_order if current_order is not None else 10**6),
            query=query,
            top_k=top_k * 2,  # 放宽 top_k，后续重排截断
            similarity_threshold=similarity_threshold,
            include_current=include_current,
            look_ahead=look_ahead if look_ahead is not None else 10**6,
            min_order=min_order,
            max_order=max_order,
        )

        # 清理向量检索结果中的 HTML 标签
        formatted_vector = []
        for r in vector_results:
            chunk_text = r["chunk_text"]
            # 清理 HTML 标签和实体
            chunk_text = re.sub(r'<[^>]+>', '', chunk_text)
            chunk_text = chunk_text.replace('&nbsp;', ' ').replace('&lt;', '<').replace('&gt;', '>').replace('&amp;', '&')
            formatted_vector.append({
                "chapter_id": r.get("chapter_id"),  # 新增
                "chapter_title": r["chapter_title"],
                "chapter_order": r["chapter_order"],
                "paragraph_index": r.get("paragraph_index"),  # 新增
                "node_id": r.get("node_id"),
                "content": chunk_text,
                "similarity": float(r["similarity"]),
                "source": "vector",
            })

        # ========== 2) 全文模糊匹配（jieba 分词优化）==========
        text_results: List[Dict[str, Any]] = []
        try:
            work_uuid = UUID(work_id) if isinstance(work_id, str) else work_id

            # 提取关键词
            keywords = self._extract_keywords(query, topK=5)

            # ✅ P0防护：keywords 为空时跳过全文检索，仅依赖向量检索
            # 场景：纯停用词查询（如"是什么"）、空查询、特殊字符
            if not keywords:
                logger.warning(f"[HybridRetriever] 无法从 query={query!r} 提取关键词，跳过全文检索")
            else:
                stmt = (
                    select(Chapter, ChapterContentIndex.plain_text)
                    .join(ChapterContentIndex, ChapterContentIndex.chapter_id == Chapter.id)
                    .where(Chapter.work_id == work_uuid)
                )
                # 时序窗口限制：与向量检索保持一致
                # current_order=None 时用 10**6（表示检索所有章节）
                # look_ahead=None 时用 10**6（表示不限制向后看的章节数）
                effective_order = current_order if current_order is not None else 10**6
                effective_look_ahead = look_ahead if look_ahead is not None else 10**6
                upper = max_order if max_order is not None else effective_order + effective_look_ahead
                if include_current:
                    stmt = stmt.where(Chapter.order <= upper)
                else:
                    stmt = stmt.where(Chapter.order < upper)
                if isinstance(min_order, int):
                    stmt = stmt.where(Chapter.order >= min_order)

                # OR 条件：任一关键词命中即可
                # 注意：keywords 已确保非空，or_(*keyword_conditions) 是安全的
                keyword_conditions = [
                    ChapterContentIndex.plain_text.ilike(f"%{kw}%") for kw in keywords
                ]
                stmt = stmt.where(or_(*keyword_conditions)).limit(top_k * 3)

                rows = await self.db.execute(stmt)
                chapters = rows.all()

                # 为每个命中章节提取 snippet
                for ch, plain_text in chapters:
                    content = plain_text or ""
                    content_lower = content.lower()

                    # 统计命中的关键词数量
                    matched_keywords = []
                    best_idx = -1
                    for kw in keywords:
                        idx = content_lower.find(kw.lower())
                        if idx != -1:
                            matched_keywords.append(kw)
                            if best_idx == -1 or idx < best_idx:
                                best_idx = idx

                    # 检查是否满足最小匹配数量要求
                    if len(matched_keywords) < min_keyword_match:
                        continue

                    if best_idx == -1:
                        continue

                    # 提取上下文 snippet（增加到 500 字符，提升 Rerank 效果）
                    start = max(0, best_idx - 250)
                    end = min(len(content), best_idx + 250)
                    snippet = content[start:end]
                    html_content = self.content_provider.read_content(str(ch.work_id), str(ch.id)) or ""
                    paragraph_index = self._infer_paragraph_index(html_content, snippet, matched_keywords)

                    # 根据匹配关键词数量调整基础分
                    base_score = 0.50 + 0.05 * len(matched_keywords)

                    text_results.append(
                        {
                            "chapter_id": str(ch.id),  # 新增
                            "chapter_title": ch.title,
                            "chapter_order": ch.order,
                            "paragraph_index": paragraph_index,
                            "content": snippet,
                            "similarity": base_score,
                            "source": "text",
                            "matched_keywords": matched_keywords,  # 调试用
                        }
                    )
        except Exception as e:
            logger.error(f"[HybridRetriever] 文本检索失败: {e}", exc_info=True)

        # ========== 3) 合并去重 ==========
        merged: Dict[tuple, Dict[str, Any]] = {}

        def _has_paragraph(item: Dict[str, Any]) -> bool:
            return item.get("paragraph_index") is not None

        def _should_replace(existing: Dict[str, Any], candidate: Dict[str, Any]) -> bool:
            existing_has_para = _has_paragraph(existing)
            candidate_has_para = _has_paragraph(candidate)
            if candidate_has_para and not existing_has_para:
                return True
            if candidate_has_para == existing_has_para:
                return candidate["similarity"] > existing["similarity"]
            return False

        def _put(item: Dict[str, Any]):
            key = (item["chapter_order"], item.get("content", "")[:80])
            if key not in merged or _should_replace(merged[key], item):
                merged[key] = item

        for item in formatted_vector:
            _put(item)
        for item in text_results:
            _put(item)

        # 先按原始 similarity 排序，取 top_k * 3 作为 rerank 候选
        merged_list = sorted(
            merged.values(), key=lambda x: x["similarity"], reverse=True
        )
        candidates = merged_list[:top_k * 3]

        # ========== 4) Rerank 重排序 ==========
        return await self._rerank(query, candidates, top_k)

