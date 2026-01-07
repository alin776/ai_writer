# -*- coding: utf-8 -*-
"""
HybridRetriever: 结合向量检索与全文模糊匹配，提高长文本作品的召回率。

设计要点：
- 先用 ChapterVectorService 做语义召回，再用章节全文 ILIKE 做精确/模糊命中。
- 可选 current_order / look_ahead 控制时序窗口，默认包含当前章及之后少量章节。
- 结果去重后按 similarity 倒序返回。
- 全文检索使用 jieba 分词提取关键词，OR 条件匹配（避免完整 query 无法命中）。
"""

import logging
import re
from typing import List, Dict, Any, Optional
from uuid import UUID

import jieba
import jieba.analyse
from sqlalchemy import select, or_
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.chapter import Chapter
from app.services.chapter_vector_service import ChapterVectorService

logger = logging.getLogger(__name__)

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
        look_ahead: int = 2,
        similarity_threshold: float = 0.25,
    ) -> List[Dict[str, Any]]:
        """
        混合检索入口。

        Args:
            work_id: 作品ID
            query: 用户查询
            current_order: 当前章节序号（可选，用于窗口限制）
            top_k: 期望返回数量
            include_current: 是否包含当前章
            look_ahead: 允许向后看的章节数
            similarity_threshold: 向量相似度阈值
        """
        # ========== 1) 向量检索 ==========
        vector_results = await self.vector_service.retrieve_for_writing(
            work_id=work_id,
            current_chapter_order=current_order if current_order is not None else 10**6,
            query=query,
            top_k=top_k * 2,  # 放宽 top_k，后续重排截断
            similarity_threshold=similarity_threshold,
            include_current=include_current,
            look_ahead=look_ahead,
        )

        # 清理向量检索结果中的 HTML 标签
        formatted_vector = []
        for r in vector_results:
            chunk_text = r["chunk_text"]
            # 清理 HTML 标签和实体
            chunk_text = re.sub(r'<[^>]+>', '', chunk_text)
            chunk_text = chunk_text.replace('&nbsp;', ' ').replace('&lt;', '<').replace('&gt;', '>').replace('&amp;', '&')
            formatted_vector.append({
                "chapter_title": r["chapter_title"],
                "chapter_order": r["chapter_order"],
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
                if current_order is not None:
                    upper = current_order + (look_ahead or 0)
                    stmt = stmt.where(Chapter.order <= upper)

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

                    # 找到第一个命中的关键词位置
                    best_idx = -1
                    matched_kw = ""
                    for kw in keywords:
                        idx = content_lower.find(kw.lower())
                        if idx != -1 and (best_idx == -1 or idx < best_idx):
                            best_idx = idx
                            matched_kw = kw

                    if best_idx == -1:
                        continue

                    # 提取上下文 snippet
                    start = max(0, best_idx - 60)
                    end = min(len(content), best_idx + len(matched_kw) + 60)
                    snippet = content[start:end]

                    text_results.append(
                        {
                            "chapter_title": ch.title,
                            "chapter_order": ch.order,
                            "content": snippet,
                            "similarity": 0.51,  # 基础分，确保能与向量结果并排
                            "source": "text",
                            "matched_keyword": matched_kw,  # 调试用
                        }
                    )
        except Exception as e:
            logger.error(f"[HybridRetriever] 文本检索失败: {e}", exc_info=True)

        # ========== 3) 合并去重 & 排序 ==========
        merged: Dict[tuple, Dict[str, Any]] = {}

        def _put(item: Dict[str, Any]):
            key = (item["chapter_order"], item["content"][:80])
            if key not in merged or item["similarity"] > merged[key]["similarity"]:
                merged[key] = item

        for item in formatted_vector:
            _put(item)
        for item in text_results:
            _put(item)

        merged_list = sorted(
            merged.values(), key=lambda x: x["similarity"], reverse=True
        )

        return merged_list[:top_k]

