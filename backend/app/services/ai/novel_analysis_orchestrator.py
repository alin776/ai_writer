"""
小说分析流程编排器
负责协调整个分析流程：微观分析 -> 向量存储 -> 宏观分析 -> 结果存储
"""
import logging
import asyncio
from typing import Optional
from sqlalchemy.ext.asyncio import AsyncSession
from datetime import datetime

from app.services.novel_analysis_service import NovelAnalysisService
from app.services.ai.novel_micro_analysis import NovelMicroAnalysisService
from app.services.ai.novel_macro_analysis import NovelMacroAnalysisService
from app.services.vector_store_service import VectorStoreService
from app.models.novel_analysis import AnalysisStatus, AnalysisStage

logger = logging.getLogger(__name__)


class NovelAnalysisOrchestrator:
    """小说分析流程编排器"""
    
    def __init__(self, db: AsyncSession):
        """
        初始化编排器
        
        Args:
            db: 数据库会话
        """
        self.db = db
        self.analysis_service = NovelAnalysisService(db)
        self.vector_service = VectorStoreService(db)
        self.micro_service = None
        self.macro_service = None
    
    async def run_full_analysis(self, work_id: str) -> bool:
        """
        运行完整的小说分析流程
        
        Args:
            work_id: 作品ID
            
        Returns:
            bool: 是否分析成功
        """
        analysis = None
        
        try:
            logger.info(f"=" * 60)
            logger.info(f"开始分析作品: {work_id}")
            logger.info(f"=" * 60)
            
            # 1. 获取或创建分析任务
            analysis = await self.analysis_service.get_analysis_by_work(work_id)
            if not analysis:
                logger.error(f"未找到作品 {work_id} 的分析任务")
                return False
            
            # 2. 更新状态为"分析中"
            await self.analysis_service.update_progress(
                analysis_id=str(analysis.id),
                analyzed_chapters=0,
                status=AnalysisStatus.ANALYZING,
                current_stage=AnalysisStage.MICRO_ANALYSIS
            )
            
            # 3. 初始化AI服务
            logger.info("初始化AI分析服务...")
            self.micro_service = NovelMicroAnalysisService()
            self.macro_service = NovelMacroAnalysisService()
            
            # 4. 获取所有章节
            chapters = await self.analysis_service.get_chapters_for_analysis(work_id)
            
            if not chapters:
                raise Exception(f"作品 {work_id} 没有章节可供分析")
            
            logger.info(f"共获取 {len(chapters)} 个章节，开始微观分析...")
            
            # 5. 执行微观分析（逐章分析）
            micro_results = []
            for idx, chapter in enumerate(chapters):
                try:
                    logger.info(f"-" * 40)
                    logger.info(f"[{idx + 1}/{len(chapters)}] 分析章节: {chapter.title}")
                    
                    # 分析章节
                    micro_result = await self.micro_service.analyze_chapter(
                        chapter_text=chapter.content,
                        chapter_id=str(chapter.id),
                        chapter_title=chapter.title,
                        chapter_number=chapter.order
                    )
                    
                    # 保存微观结果
                    await self.analysis_service.save_micro_result(
                        analysis_id=str(analysis.id),
                        chapter_id=str(chapter.id),
                        micro_data=micro_result
                    )
                    
                    micro_results.append(micro_result)
                    
                    # 存储向量（用于RAG检索）
                    try:
                        logger.info(f"存储章节 {chapter.title} 的向量...")
                        await self.vector_service.store_micro_analysis_vector(
                            work_id=work_id,
                            chapter_id=str(chapter.id),
                            analysis_id=str(analysis.id),
                            micro_data=micro_result,
                            chunk_index=0
                        )
                        logger.info(f"✓ 向量存储成功")
                    except Exception as ve:
                        # 向量存储失败不影响主流程
                        logger.warning(f"向量存储失败（不影响分析）: {ve}")
                    
                    # 更新进度
                    await self.analysis_service.update_progress(
                        analysis_id=str(analysis.id),
                        analyzed_chapters=idx + 1
                    )
                    
                    logger.info(f"✓ 章节 {chapter.title} 分析完成")
                    
                    # 短暂延迟，避免API限流
                    await asyncio.sleep(0.5)
                    
                except Exception as e:
                    logger.error(f"✗ 章节 {chapter.title} 分析失败: {e}", exc_info=True)
                    # 继续分析其他章节，不中断整个流程
                    continue
            
            logger.info(f"微观分析完成，成功分析 {len(micro_results)}/{len(chapters)} 个章节")
            
            # 6. 检查是否有足够的微观结果
            if not micro_results:
                raise Exception("所有章节的微观分析都失败了")
            
            if len(micro_results) < len(chapters) * 0.5:  # 至少成功50%
                logger.warning(f"微观分析成功率较低: {len(micro_results)}/{len(chapters)}")
            
            # 7. 更新阶段为"宏观分析"
            await self.analysis_service.update_progress(
                analysis_id=str(analysis.id),
                analyzed_chapters=len(micro_results),
                current_stage=AnalysisStage.MACRO_ANALYSIS
            )
            
            logger.info(f"=" * 60)
            logger.info("开始宏观分析...")
            logger.info(f"=" * 60)
            
            # 8. 执行宏观分析
            macro_report = await self.macro_service.analyze_novel_macro(micro_results)
            
            logger.info(f"宏观分析完成，报告长度: {len(macro_report)} 字符")
            
            # 9. 保存宏观结果
            await self.analysis_service.save_macro_result(
                analysis_id=str(analysis.id),
                macro_report=macro_report
            )
            
            logger.info(f"=" * 60)
            logger.info(f"作品 {work_id} 分析全部完成！")
            logger.info(f"微观分析: {len(micro_results)} 章")
            logger.info(f"宏观报告: {len(macro_report)} 字符")
            
            # 打印向量存储统计
            try:
                vector_stats = await self.vector_service.get_vector_stats(work_id)
                logger.info(f"向量存储: {vector_stats['total_vectors']} 条，"
                          f"覆盖 {vector_stats['total_chapters']} 章")
            except Exception:
                pass
            
            logger.info(f"=" * 60)
            
            return True
            
        except Exception as e:
            logger.error(f"分析流程失败: {e}", exc_info=True)
            
            # 标记任务为失败
            if analysis:
                await self.analysis_service.mark_as_failed(
                    analysis_id=str(analysis.id),
                    error_message=str(e)
                )
            
            return False
            
        finally:
            # 清理资源
            await self._cleanup()
    
    async def _cleanup(self):
        """清理资源"""
        try:
            if self.micro_service:
                await self.micro_service.close()
            if self.macro_service:
                await self.macro_service.close()
            logger.info("AI服务资源已清理")
        except Exception as e:
            logger.error(f"清理资源时出错: {e}")


async def run_novel_analysis_task(work_id: str, db: AsyncSession) -> bool:
    """
    运行小说分析任务（可作为后台任务调用）
    
    Args:
        work_id: 作品ID
        db: 数据库会话
        
    Returns:
        bool: 是否成功
    """
    orchestrator = NovelAnalysisOrchestrator(db)
    return await orchestrator.run_full_analysis(work_id)
