"""
作品级评审服务

功能:
- 封装BookReviewAnalyzer
- 提供统一接口
- 集成缓存和异步任务
"""

from typing import Dict, Any, List, Optional
import logging
from uuid import UUID

from app.services.review.book_review_analyzer import BookReviewAnalyzer
from app.core.cache import cache_review

logger = logging.getLogger(__name__)


class BookReviewService:
    """作品级评审服务"""

    def __init__(self):
        self.analyzer = BookReviewAnalyzer()

    @cache_review(expire=7200, key_prefix="book_review")  # 缓存2小时
    async def review_book(
        self,
        novel_id: UUID,
        book_title: str,
        chapters: List[Dict[str, Any]],
        author_notes: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        评审完整作品

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

        # 调用分析器
        analysis_result = await self.analyzer.analyze_full_book(
            book_title=book_title,
            chapters=chapters,
            author_notes=author_notes
        )

        # 添加额外元数据
        analysis_result["novel_id"] = str(novel_id)

        logger.info(f"[BookReviewService] 评审完成, 总分={analysis_result.get('overall_score', 0)}")

        return analysis_result

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
