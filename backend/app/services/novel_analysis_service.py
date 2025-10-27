"""
小说分析服务层
处理小说分析任务的创建、进度更新、结果存储等业务逻辑
"""
from typing import Optional, List, Dict, Any
from datetime import datetime, timezone
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.orm import selectinload
import logging

from app.models.novel_analysis import NovelAnalysis, AnalysisStatus, AnalysisStage
from app.models.work import Work
from app.models.chapter import Chapter
from app.schemas.novel_analysis import (
    NovelAnalysisCreate,
    NovelAnalysisUpdate,
    MicroAnalysisChunk
)

logger = logging.getLogger(__name__)


class NovelAnalysisService:
    """小说分析服务"""

    def __init__(self, db: AsyncSession):
        self.db = db
    
    # ==================== 核心方法 ====================
    
    async def create_analysis(self, work_id: str) -> NovelAnalysis:
        """
        创建小说分析任务
        
        Args:
            work_id: 作品ID
            
        Returns:
            NovelAnalysis: 创建的分析任务
            
        Raises:
            ValueError: 如果作品不存在或已有分析任务
        """
        # 1. 检查作品是否存在
        work = await self._get_work_with_chapters(work_id)
        if not work:
            raise ValueError(f"Work with id {work_id} not found")
        
        # 2. 检查是否已有分析任务
        existing = await self.get_analysis_by_work(work_id)
        if existing:
            # 如果已有任务且未完成，返回现有任务
            if existing.status in [AnalysisStatus.PENDING, AnalysisStatus.ANALYZING]:
                logger.info(f"Analysis already exists for work {work_id}, status: {existing.status}")
                return existing
            # 如果已完成或失败，删除旧任务创建新任务
            await self.db.delete(existing)
            await self.db.commit()
            logger.info(f"Deleted old analysis for work {work_id}, creating new one")
        
        # 3. 获取章节总数
        total_chapters = len(work.chapters)
        if total_chapters == 0:
            raise ValueError(f"Work {work_id} has no chapters to analyze")
        
        # 4. 创建分析任务
        analysis = NovelAnalysis(
            work_id=work_id,
            status=AnalysisStatus.PENDING,
            current_stage=AnalysisStage.MICRO_ANALYSIS,
            total_chapters=total_chapters,
            analyzed_chapters=0,
            micro_results=None,
            macro_results=None,
            started_at=None,
            completed_at=None
        )
        
        self.db.add(analysis)
        await self.db.commit()
        await self.db.refresh(analysis)
        
        logger.info(f"Created analysis task for work {work_id}, total_chapters: {total_chapters}")
        return analysis
    
    async def get_analysis_by_work(self, work_id: str) -> Optional[NovelAnalysis]:
        """
        根据作品ID获取分析任务
        
        Args:
            work_id: 作品ID
            
        Returns:
            Optional[NovelAnalysis]: 分析任务，如果不存在返回None
        """
        result = await self.db.execute(
            select(NovelAnalysis).where(NovelAnalysis.work_id == work_id)
        )
        return result.scalar_one_or_none()
    
    async def get_analysis_by_id(self, analysis_id: str) -> Optional[NovelAnalysis]:
        """
        根据分析ID获取分析任务
        
        Args:
            analysis_id: 分析任务ID
            
        Returns:
            Optional[NovelAnalysis]: 分析任务，如果不存在返回None
        """
        result = await self.db.execute(
            select(NovelAnalysis).where(NovelAnalysis.id == analysis_id)
        )
        return result.scalar_one_or_none()
    
    async def update_progress(
        self,
        analysis_id: str,
        analyzed_chapters: int,
        current_stage: Optional[AnalysisStage] = None,
        status: Optional[AnalysisStatus] = None
    ) -> Optional[NovelAnalysis]:
        """
        更新分析进度

        Args:
            analysis_id: 分析任务ID
            analyzed_chapters: 已分析章节数
            current_stage: 当前阶段（可选）
            status: 任务状态（可选）

        Returns:
            Optional[NovelAnalysis]: 更新后的分析任务
        """
        try:
            analysis = await self.get_analysis_by_id(analysis_id)
            if not analysis:
                logger.error(f"Analysis {analysis_id} not found")
                return None

            # 更新进度
            analysis.analyzed_chapters = analyzed_chapters

            # 更新阶段
            if current_stage:
                analysis.current_stage = current_stage

            # 更新状态
            if status:
                analysis.status = status
                # 如果开始分析，记录开始时间
                if status == AnalysisStatus.ANALYZING and not analysis.started_at:
                    analysis.started_at = datetime.now(timezone.utc)
                # 如果完成或失败，记录完成时间
                if status in [AnalysisStatus.COMPLETED, AnalysisStatus.FAILED]:
                    analysis.completed_at = datetime.now(timezone.utc)

            await self.db.commit()
            await self.db.refresh(analysis)

            logger.info(f"Updated analysis {analysis_id} progress: {analyzed_chapters}/{analysis.total_chapters}, stage: {current_stage}, status: {status}")
            return analysis
        except Exception as e:
            logger.error(f"Error updating progress: {e}", exc_info=True)
            await self.db.rollback()
            raise
    
    async def save_micro_result(
        self,
        analysis_id: str,
        chapter_id: str,
        micro_data: Dict[str, Any]
    ) -> Optional[NovelAnalysis]:
        """
        保存单个章节的微观分析结果

        Args:
            analysis_id: 分析任务ID
            chapter_id: 章节ID
            micro_data: 微观分析JSON数据

        Returns:
            Optional[NovelAnalysis]: 更新后的分析任务
        """
        try:
            analysis = await self.get_analysis_by_id(analysis_id)
            if not analysis:
                logger.error(f"Analysis {analysis_id} not found")
                return None

            # 初始化 micro_results（如果为空）
            if analysis.micro_results is None:
                analysis.micro_results = []

            # 添加新的微观分析结果
            micro_results = analysis.micro_results if isinstance(analysis.micro_results, list) else []
            micro_results.append({
                "chapter_id": chapter_id,
                **micro_data
            })

            analysis.micro_results = micro_results
            analysis.analyzed_chapters = len(micro_results)

            await self.db.commit()
            await self.db.refresh(analysis)

            logger.info(f"Saved micro result for analysis {analysis_id}, chapter {chapter_id}, total: {len(micro_results)}")
            return analysis
        except Exception as e:
            logger.error(f"Error saving micro result: {e}", exc_info=True)
            await self.db.rollback()
            raise

    async def batch_save_micro_results(
        self,
        analysis_id: str,
        results: List[Dict[str, Any]]
    ) -> Optional[NovelAnalysis]:
        """
        批量保存微观分析结果(解决并发冲突问题)

        Args:
            analysis_id: 分析任务ID
            results: 结果列表,每个元素格式:
                {
                    'chapter_id': str,
                    'data': Dict[str, Any]  # 微观分析数据
                }

        Returns:
            Optional[NovelAnalysis]: 更新后的分析任务
        """
        try:
            analysis = await self.get_analysis_by_id(analysis_id)
            if not analysis:
                logger.error(f"Analysis {analysis_id} not found")
                return None

            # 初始化 micro_results
            if analysis.micro_results is None:
                analysis.micro_results = []

            # 批量添加所有结果
            micro_results = analysis.micro_results if isinstance(analysis.micro_results, list) else []

            for result in results:
                micro_results.append({
                    "chapter_id": result['chapter_id'],
                    **result['data']
                })

            analysis.micro_results = micro_results
            analysis.analyzed_chapters = len(micro_results)

            # 一次性提交所有结果
            await self.db.commit()
            await self.db.refresh(analysis)

            logger.info(f"Batch saved {len(results)} micro results for analysis {analysis_id}, total: {len(micro_results)}")
            return analysis
        except Exception as e:
            logger.error(f"Error batch saving micro results: {e}", exc_info=True)
            await self.db.rollback()
            raise
    
    async def save_macro_result(
        self,
        analysis_id: str,
        macro_report: str
    ) -> Optional[NovelAnalysis]:
        """
        保存宏观分析报告

        Args:
            analysis_id: 分析任务ID
            macro_report: 宏观分析报告文本

        Returns:
            Optional[NovelAnalysis]: 更新后的分析任务
        """
        try:
            analysis = await self.get_analysis_by_id(analysis_id)
            if not analysis:
                logger.error(f"Analysis {analysis_id} not found")
                return None

            # 保存宏观分析结果
            analysis.macro_results = macro_report
            analysis.current_stage = AnalysisStage.COMPLETED
            analysis.status = AnalysisStatus.COMPLETED
            analysis.completed_at = datetime.now(timezone.utc)

            await self.db.commit()
            await self.db.refresh(analysis)

            logger.info(f"Saved macro result for analysis {analysis_id}, marked as completed")
            return analysis
        except Exception as e:
            logger.error(f"Error saving macro result: {e}", exc_info=True)
            await self.db.rollback()
            raise
    
    async def get_analysis_result(self, work_id: str) -> Optional[NovelAnalysis]:
        """
        获取完整的分析结果（包含微观和宏观）
        
        Args:
            work_id: 作品ID
            
        Returns:
            Optional[NovelAnalysis]: 完整的分析结果
        """
        analysis = await self.get_analysis_by_work(work_id)
        if not analysis:
            logger.warning(f"No analysis found for work {work_id}")
            return None
        
        if analysis.status != AnalysisStatus.COMPLETED:
            logger.warning(f"Analysis for work {work_id} is not completed yet, status: {analysis.status}")
        
        return analysis
    
    async def mark_as_failed(
        self,
        analysis_id: str,
        error_message: str
    ) -> Optional[NovelAnalysis]:
        """
        标记分析任务为失败

        Args:
            analysis_id: 分析任务ID
            error_message: 错误消息

        Returns:
            Optional[NovelAnalysis]: 更新后的分析任务
        """
        try:
            analysis = await self.get_analysis_by_id(analysis_id)
            if not analysis:
                logger.error(f"Analysis {analysis_id} not found")
                return None

            analysis.status = AnalysisStatus.FAILED
            analysis.error_message = error_message
            analysis.completed_at = datetime.now(timezone.utc)

            await self.db.commit()
            await self.db.refresh(analysis)

            logger.error(f"Marked analysis {analysis_id} as failed: {error_message}")
            return analysis
        except Exception as e:
            logger.error(f"Error marking analysis as failed: {e}", exc_info=True)
            await self.db.rollback()
            raise
    
    async def delete_analysis(self, work_id: str) -> bool:
        """
        删除分析任务
        
        Args:
            work_id: 作品ID
            
        Returns:
            bool: 是否删除成功
        """
        analysis = await self.get_analysis_by_work(work_id)
        if not analysis:
            return False
        
        await self.db.delete(analysis)
        await self.db.commit()
        
        logger.info(f"Deleted analysis for work {work_id}")
        return True
    
    # ==================== 辅助方法 ====================
    
    async def _get_work_with_chapters(self, work_id: str) -> Optional[Work]:
        """
        获取作品及其章节
        
        Args:
            work_id: 作品ID
            
        Returns:
            Optional[Work]: 作品对象（包含章节）
        """
        result = await self.db.execute(
            select(Work)
            .options(selectinload(Work.chapters))
            .where(Work.id == work_id)
        )
        return result.scalar_one_or_none()
    
    async def get_chapters_for_analysis(self, work_id: str) -> List[Chapter]:
        """
        获取作品的所有章节（用于分析）
        
        Args:
            work_id: 作品ID
            
        Returns:
            List[Chapter]: 章节列表（按顺序排列）
        """
        result = await self.db.execute(
            select(Chapter)
            .where(Chapter.work_id == work_id)
            .order_by(Chapter.order)
        )
        return result.scalars().all()
