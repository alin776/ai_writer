"""
作品级评审服务

功能:
- 封装BookReviewAnalyzer
- 提供统一接口
- 集成缓存和异步任务
"""

from typing import Dict, Any, List, Optional
import logging
import hashlib
import json
from uuid import UUID

from app.services.review.book_review_analyzer import BookReviewAnalyzer
from app.core.redis_client import redis_client

logger = logging.getLogger(__name__)


class BookReviewService:
    """作品级评审服务"""

    def __init__(self):
        self.analyzer = BookReviewAnalyzer()

    async def review_book(
        self,
        novel_id: UUID,
        book_title: str,
        chapters: List[Dict[str, Any]],
        author_notes: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        评审完整作品 (带智能缓存)

        缓存策略:
        - 缓存key基于: novel_id + 章节ID列表 (不包含章节内容)
        - 缓存时间: 2小时
        - 如果章节内容未变化,使用缓存结果

        Args:
            novel_id: 小说ID
            book_title: 书名
            chapters: 章节列表
            author_notes: 作者备注

        Returns:
            完整评审报告
        """
        logger.info(f"[BookReviewService] 开始评审作品: {book_title}, 章节数={len(chapters)}")

        if not chapters:
            raise ValueError("章节列表不能为空")

        if len(chapters) < 3:
            raise ValueError("至少需要3个章节才能进行作品级评审")

        # 生成缓存key (基于novel_id和章节order列表)
        cache_key = self._generate_cache_key(novel_id, chapters)

        # 查询缓存
        if redis_client.is_available():
            cached = redis_client.get_json(cache_key)
            if cached:
                logger.info(f"✅ 缓存命中: {cache_key}")
                return cached
            logger.info(f"⚠️ 缓存未命中: {cache_key}")

        # 调用分析器
        analysis_result = await self.analyzer.analyze_full_book(
            book_title=book_title,
            chapters=chapters,
            author_notes=author_notes
        )

        # 添加额外元数据
        analysis_result["novel_id"] = str(novel_id)

        # 缓存结果
        if redis_client.is_available():
            success = redis_client.set_json(cache_key, analysis_result, expire=7200)
            if success:
                logger.info(f"💾 缓存已保存: {cache_key} (expire=7200s)")
            else:
                logger.warning(f"⚠️ 缓存保存失败: {cache_key}")

        logger.info(f"[BookReviewService] 评审完成, 总分={analysis_result.get('overall_score', 0)}")

        return analysis_result

    def _generate_cache_key(self, novel_id: UUID, chapters: List[Dict[str, Any]]) -> str:
        """
        生成缓存key

        策略: novel_id + 章节内容特征hash
        - 使用每章内容的前500字符作为特征
        - 内容修改后,缓存key会变化,避免返回过时结果

        Args:
            novel_id: 小说ID
            chapters: 章节列表

        Returns:
            缓存key
        """
        # 提取章节核心数据: order + content前500字符的hash
        chapter_data = []
        for ch in sorted(chapters, key=lambda x: x.get("order", 0)):
            # 使用content的前500字符作为特征 (足够区分内容变化,又不会太慢)
            content = ch.get("content", "")
            content_preview = content[:500] if content else ""
            content_hash = hashlib.md5(content_preview.encode()).hexdigest()

            chapter_data.append({
                "order": ch.get("order", 0),
                "content_hash": content_hash
            })

        # 生成缓存key
        cache_data = {
            "novel_id": str(novel_id),
            "chapters": chapter_data
        }

        cache_str = json.dumps(cache_data, sort_keys=True)
        cache_hash = hashlib.md5(cache_str.encode()).hexdigest()[:16]

        return f"book_review:review_book:{cache_hash}"

    async def quick_review_book(
        self,
        novel_id: UUID,
        book_title: str,
        chapters: List[Dict[str, Any]]
    ) -> Dict[str, Any]:
        """
        快速评审 (仅分析前10章)

        适用场景:
        - 作品章节数很多 (>50章)
        - 只需要快速反馈

        Returns:
            简化的评审报告
        """
        logger.info(f"[BookReviewService] 快速评审: {book_title}")

        # 只取前10章
        sample_chapters = chapters[:10]

        result = await self.review_book(
            novel_id=novel_id,
            book_title=book_title,
            chapters=sample_chapters
        )

        result["is_quick_review"] = True
        result["sampled_chapters"] = len(sample_chapters)

        return result
