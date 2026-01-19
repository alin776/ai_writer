# -*- coding: utf-8 -*-
"""
HybridRetriever: 结合向量检索与全文模糊匹配，提高长文本作品的召回率。

设计要点：
- 先用 ChapterVectorService 做语义召回，再用章节全文 ILIKE 做精确/模糊命中。
- 可选 current_order / look_ahead 控制时序窗口，默认包含当前章及之后少量章节。
- 结果去重后按 similarity 倒序返回。
- 全文检索使用 jieba 分词提取关键词，OR 条件匹配（避免完整 query 无法命中）。
- v2.0: 增加 Rerank 重排序，使用 CrossEncoder 提升精准度。
"""

import asyncio
import logging
import os
import re
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
from typing import List, Dict, Any, Optional
from uuid import UUID

import jieba
import jieba.analyse
from sqlalchemy import select, or_
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.chapter import Chapter
from app.services.chapter_vector_service import ChapterVectorService

logger = logging.getLogger(__name__)

# ==================== Reranker 全局单例 ====================
_global_reranker = None
_RERANKER_MODEL = "BAAI/bge-reranker-base"  # 中文优化的 reranker 模型
_rerank_executor = ThreadPoolExecutor(max_workers=1, thread_name_prefix="reranker")


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

    async def _rerank(self, query: str, candidates: List[Dict[str, Any]], top_k: int) -> List[Dict[str, Any]]:
        """
        使用 CrossEncoder 对候选结果进行重排序（异步，不阻塞事件循环）。

        Args:
            query: 用户查询
            candidates: 候选结果列表
            top_k: 返回数量

        Returns:
            重排序后的结果列表
        """
        if not candidates:
            return []

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
            current_chapter_order=current_order if current_order is not None else 10**6,
            query=query,
            top_k=top_k * 2,  # 放宽 top_k，后续重排截断
            similarity_threshold=similarity_threshold,
            include_current=include_current,
            look_ahead=look_ahead if look_ahead is not None else 10**6,
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
                stmt = select(Chapter).where(Chapter.work_id == work_uuid)
                # 时序窗口限制：与向量检索保持一致
                # current_order=None 时用 10**6（表示检索所有章节）
                # look_ahead=None 时用 10**6（表示不限制向后看的章节数）
                effective_order = current_order if current_order is not None else 10**6
                effective_look_ahead = look_ahead if look_ahead is not None else 10**6
                upper = effective_order + effective_look_ahead
                if include_current:
                    stmt = stmt.where(Chapter.order <= upper)
                else:
                    stmt = stmt.where(Chapter.order < upper)

                # OR 条件：任一关键词命中即可
                # 注意：keywords 已确保非空，or_(*keyword_conditions) 是安全的
                keyword_conditions = [
                    Chapter.content.ilike(f"%{kw}%") for kw in keywords
                ]
                stmt = stmt.where(or_(*keyword_conditions)).limit(top_k * 3)

                rows = await self.db.execute(stmt)
                chapters = rows.scalars().all()

                # 为每个命中章节提取 snippet
                for ch in chapters:
                    content = ch.content or ""
                    # 清理 HTML 标签和实体
                    content = re.sub(r'<[^>]+>', '', content)
                    content = content.replace('&nbsp;', ' ').replace('&lt;', '<').replace('&gt;', '>').replace('&amp;', '&')
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

                    # 根据匹配关键词数量调整基础分
                    base_score = 0.50 + 0.05 * len(matched_keywords)

                    text_results.append(
                        {
                            "chapter_id": str(ch.id),  # 新增
                            "chapter_title": ch.title,
                            "chapter_order": ch.order,
                            "paragraph_index": None,  # 全文检索无段落级信息
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

