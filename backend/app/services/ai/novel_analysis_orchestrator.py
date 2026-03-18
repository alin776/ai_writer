"""
小说分析流程编排器
负责协调整个分析流程：微观分析 -> 向量存储 -> 宏观分析 -> 结果存储
"""
import logging
import asyncio
import time
from typing import Optional, List, Dict, Any
from uuid import UUID
from sqlalchemy.ext.asyncio import AsyncSession
from datetime import datetime

from app.services.novel_analysis_service import NovelAnalysisService
from app.services.ai.novel_micro_analysis import NovelMicroAnalysisService
from app.services.ai.novel_macro_analysis import NovelMacroAnalysisService
from app.services.vector_store_service import VectorStoreService
from app.models.novel_analysis import AnalysisStatus, AnalysisStage
from app.core.config import settings

logger = logging.getLogger(__name__)


class _ChapterObj:
    """将 dict 包装为可通过属性访问的对象，兼容下游 .title/.content 等调用。"""
    def __init__(self, d: dict):
        self.id = d.get("num", d.get("id", ""))
        self.title = d.get("title", "")
        self.content = d.get("content", "")
        self.order = d.get("num", d.get("order", 0))
        self.word_count = d.get("word_count", 0)
        self.status = d.get("status", "")


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
        运行完整的小说分析流程（带整体超时控制）
        
        Args:
            work_id: 作品ID
            
        Returns:
            bool: 是否分析成功
        """
        analysis = None
        start_time = time.time()
        
        try:
            # 使用asyncio.wait_for设置整体超时
            return await asyncio.wait_for(
                self._run_analysis_internal(work_id),
                timeout=settings.ANALYSIS_TIMEOUT
            )
        except asyncio.TimeoutError:
            elapsed = time.time() - start_time
            logger.error(
                f"分析超时！作品 {work_id} 分析耗时 {elapsed:.1f}秒，"
                f"超过最大允许时间 {settings.ANALYSIS_TIMEOUT}秒"
            )
            # 标记任务为失败
            try:
                analysis = await self.analysis_service.get_analysis_by_work(work_id)
                if analysis:
                    await self.analysis_service.mark_as_failed(
                        analysis_id=str(analysis.id),
                        error_message=f"分析超时（超过{settings.ANALYSIS_TIMEOUT}秒）"
                    )
            except Exception as e:
                logger.error(f"标记超时失败: {e}")
            return False
        except Exception as e:
            logger.error(f"分析流程异常: {e}", exc_info=True)
            return False
        finally:
            await self._cleanup()
    
    async def _run_analysis_internal(self, work_id: str) -> bool:
        """
        内部分析流程实现

        Args:
            work_id: 作品ID

        Returns:
            bool: 是否分析成功
        """
        analysis = None
        start_time = time.time()

        try:
            logger.info(f"=" * 60)
            logger.info(f"开始分析作品: {work_id}")
            logger.info(f"=" * 60)

            # 1. 获取或创建分析任务
            analysis = await self.analysis_service.get_analysis_by_work(work_id)
            if not analysis:
                logger.error(f"未找到作品 {work_id} 的分析任务")
                return False

            # 获取作品的user_id (用于token记录)
            from app.services.work_service import WorkService
            work_service = WorkService(self.db)
            work = await work_service.get_work_by_id(work_id)
            # ✅ 修复：Work模型使用的是author_id，不是user_id
            user_id = str(work.author_id) if work and work.author_id else None

            # 2. 更新状态为"分析中"
            await self.analysis_service.update_progress(
                analysis_id=str(analysis.id),
                analyzed_chapters=0,
                status=AnalysisStatus.ANALYZING,
                current_stage=AnalysisStage.MICRO_ANALYSIS
            )

            # 3. 初始化AI服务（传入user_id和db用于token记录）
            logger.info("初始化AI分析服务...")
            self.micro_service = NovelMicroAnalysisService(
                user_id=user_id,
                db=self.db,
                work_id=work_id
            )
            self.macro_service = NovelMacroAnalysisService(
                user_id=user_id,
                db=self.db,
                work_id=work_id
            )

            # 4. 获取所有章节
            chapters_raw = await self.analysis_service.get_chapters_for_analysis(work_id)

            if not chapters_raw:
                raise Exception(f"作品 {work_id} 没有章节可供分析")

            # 统一转为对象，兼容下游 .title/.content 等属性访问
            chapters = [
                _ChapterObj(ch) if isinstance(ch, dict) else ch
                for ch in chapters_raw
            ]

            # ✅ 检查章节内容是否为空
            from app.core.config import settings
            MIN_CONTENT_LENGTH = settings.ANALYSIS_MIN_CONTENT_LENGTH
            empty_chapters = []
            for ch in chapters:
                if not ch.content or len(ch.content.strip()) < MIN_CONTENT_LENGTH:
                    chapter_label = ch.title or f"第{ch.order}章"
                    empty_chapters.append({
                        "label": chapter_label,
                        "length": len(ch.content.strip()) if ch.content else 0
                    })

            if empty_chapters:
                # 构建详细的错误消息
                chapter_list = []
                for ec in empty_chapters[:5]:  # 最多显示5个
                    chapter_list.append(f"  - {ec['label']} (当前{ec['length']}字符)")

                error_msg = (
                    f"无法开始分析：以下 {len(empty_chapters)} 个章节内容为空或过短\n\n"
                    f"{chr(10).join(chapter_list)}"
                )

                if len(empty_chapters) > 5:
                    error_msg += f"\n  - ...还有 {len(empty_chapters)-5} 个章节"

                error_msg += (
                    f"\n\n要求：每个章节至少需要 {MIN_CONTENT_LENGTH} 字符的内容\n"
                    f"建议：填写章节内容后再触发分析，以获得完整的分析报告"
                )

                logger.error(f"分析前验证失败: {len(empty_chapters)}/{len(chapters)} 章节内容不足")
                raise ValueError(error_msg)

            logger.info(f"共获取 {len(chapters)} 个章节，内容验证通过，开始微观分析...")

            # 查询用户是否管理员（用于计费豁免）
            from app.models.user import User
            from sqlalchemy import select
            is_admin = False
            if user_id:
                user_stmt = select(User.is_admin).where(User.id == UUID(user_id))
                user_result = await self.db.execute(user_stmt)
                is_admin = bool(user_result.scalar())

            # 使用聚合计费上下文：整个分析流程只产生 1 条使用记录
            from app.core.billing_context import billing_context
            work_title = work.title if work else work_id
            async with billing_context(
                user_id=user_id,
                description=f"小说分析 · {work_title}({len(chapters)}章)",
                operation_type="novel_analysis",
                is_admin=is_admin,
            ):
                # 5. 执行微观分析（并行版本）⚡
                logger.info(f"⚡ 使用并行分析模式 (并发数: {settings.NOVEL_ANALYSIS_MAX_CONCURRENT})")
                micro_results, failed_chapters = await self._analyze_chapters_parallel(
                    chapters=chapters,
                    analysis_id=str(analysis.id),
                    work_id=work_id
                )

                micro_elapsed = time.time() - start_time
                success_rate = len(micro_results) / len(chapters) * 100

                logger.info(f"=" * 60)
                logger.info(f"微观分析完成统计:")
                logger.info(f"  成功: {len(micro_results)}/{len(chapters)} 章节 ({success_rate:.1f}%)")
                logger.info(f"  失败: {len(failed_chapters)} 章节")
                logger.info(f"  总耗时: {micro_elapsed:.1f}秒 (平均 {micro_elapsed/len(chapters):.1f}秒/章)")

                if failed_chapters:
                    logger.warning(f"失败章节列表:")
                    for fc in failed_chapters:
                        logger.warning(f"  - {fc['title']}: {fc['error']}")

                logger.info(f"=" * 60)

                # 6. 检查是否有足够的微观结果
                if not micro_results:
                    raise Exception("所有章节的微观分析都失败了")

                if len(micro_results) < len(chapters) * 0.5:  # 至少成功50%
                    logger.warning(f"微观分析成功率较低: {success_rate:.1f}%")

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
                macro_start_time = time.time()
                macro_report = await self.macro_service.analyze_novel_macro(micro_results)
                macro_elapsed = time.time() - macro_start_time

                logger.info(f"宏观分析完成，报告长度: {len(macro_report)} 字符，耗时: {macro_elapsed:.1f}秒")
            
            # 9. 保存宏观结果
            await self.analysis_service.save_macro_result(
                analysis_id=str(analysis.id),
                macro_report=macro_report
            )
            
            # 计算总耗时
            total_elapsed = time.time() - start_time
            
            logger.info(f"=" * 60)
            logger.info(f"作品 {work_id} 分析全部完成！")
            logger.info(f"=" * 60)
            logger.info(f"📊 分析统计:")
            logger.info(f"  微观分析: {len(micro_results)}/{len(chapters)} 章 (成功率 {success_rate:.1f}%)")
            logger.info(f"  宏观报告: {len(macro_report)} 字符")
            logger.info(f"  总耗时: {total_elapsed:.1f}秒 ({total_elapsed/60:.1f}分钟)")
            logger.info(f"  平均速度: {total_elapsed/len(chapters):.1f}秒/章")
            
            # 打印向量存储统计
            try:
                vector_stats = await self.vector_service.get_vector_stats(work_id)
                logger.info(f"  向量存储: {vector_stats['total_vectors']} 条，"
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

    async def _analyze_chapters_parallel(
        self,
        chapters: list,
        analysis_id: str,
        work_id: str
    ) -> tuple[list, list]:
        """
        并行分析章节（批量保存模式）- 解决并发冲突

        Args:
            chapters: 章节列表
            analysis_id: 分析任务ID
            work_id: 作品ID

        Returns:
            (成功结果列表, 失败章节列表)
        """
        from app.core.config import settings

        # 创建Semaphore限制并发数
        semaphore = asyncio.Semaphore(settings.NOVEL_ANALYSIS_MAX_CONCURRENT)
        successful_results = []
        failed_chapters = []
        completed_count = 0

        # 用于线程安全的计数
        progress_lock = asyncio.Lock()

        async def analyze_single_chapter(idx: int, chapter):
            """分析单个章节 - 只返回结果,不保存"""
            nonlocal completed_count

            async with semaphore:
                chapter_start_time = time.time()
                try:
                    logger.info(f"[{idx+1}/{len(chapters)}] 🔄 开始分析: {chapter.title}")

                    # 添加超时控制
                    micro_result = await asyncio.wait_for(
                        self.micro_service.analyze_chapter(
                            chapter_text=chapter.content,
                            chapter_id=str(chapter.id),
                            chapter_title=chapter.title,
                            chapter_number=chapter.order
                        ),
                        timeout=settings.NOVEL_ANALYSIS_CHAPTER_TIMEOUT
                    )

                    chapter_elapsed = time.time() - chapter_start_time
                    logger.info(f"[{idx+1}/{len(chapters)}] ✓ 分析完成: {chapter.title} ({chapter_elapsed:.1f}秒)")

                    # 更新计数(用于进度显示)
                    async with progress_lock:
                        completed_count += 1
                        if completed_count % settings.NOVEL_ANALYSIS_BATCH_UPDATE_SIZE == 0:
                            logger.info(f"📊 进度更新: {completed_count}/{len(chapters)} 章")

                    # 只返回结果,不保存
                    return {
                        'status': 'success',
                        'chapter_id': str(chapter.id),
                        'chapter_title': chapter.title,
                        'data': micro_result
                    }

                except asyncio.TimeoutError:
                    chapter_elapsed = time.time() - chapter_start_time
                    error_msg = f"分析超时({settings.NOVEL_ANALYSIS_CHAPTER_TIMEOUT}秒)"
                    logger.error(
                        f"[{idx+1}/{len(chapters)}] ⏰ 超时: {chapter.title} ({chapter_elapsed:.1f}秒)"
                    )
                    return {
                        'status': 'failed',
                        'chapter_id': str(chapter.id),
                        'chapter_title': chapter.title,
                        'error': error_msg
                    }

                except Exception as e:
                    chapter_elapsed = time.time() - chapter_start_time
                    logger.error(
                        f"[{idx+1}/{len(chapters)}] ✗ 失败: {chapter.title} ({chapter_elapsed:.1f}秒) - {e}"
                    )
                    return {
                        'status': 'failed',
                        'chapter_id': str(chapter.id),
                        'chapter_title': chapter.title,
                        'error': str(e)
                    }

        # 创建所有并发任务
        tasks = [
            analyze_single_chapter(idx, chapter)
            for idx, chapter in enumerate(chapters)
        ]

        logger.info(f"⚡ 启动 {len(tasks)} 个并发分析任务...")

        # 并发执行所有任务
        results = await asyncio.gather(*tasks, return_exceptions=True)

        # 分类处理结果
        for result in results:
            if isinstance(result, Exception):
                # 处理未捕获的异常
                logger.error(f"Unexpected error in task: {result}")
                failed_chapters.append({
                    'title': 'Unknown',
                    'id': 'unknown',
                    'error': str(result)
                })
            elif result['status'] == 'success':
                successful_results.append(result)
            else:
                failed_chapters.append({
                    'title': result['chapter_title'],
                    'id': result['chapter_id'],
                    'error': result['error']
                })

        logger.info(f"⚡ 并行分析完成: 成功 {len(successful_results)}/{len(chapters)} 章")

        # 批量保存成功的结果
        if successful_results:
            logger.info(f"💾 开始批量保存 {len(successful_results)} 个分析结果...")
            try:
                await self.analysis_service.batch_save_micro_results(
                    analysis_id=analysis_id,
                    results=successful_results
                )
                logger.info(f"✅ 批量保存完成: {len(successful_results)} 个结果")
            except Exception as e:
                logger.error(f"❌ 批量保存失败: {e}", exc_info=True)
                # 批量保存失败,将所有结果标记为失败
                for result in successful_results:
                    failed_chapters.append({
                        'title': result['chapter_title'],
                        'id': result['chapter_id'],
                        'error': f"保存失败: {str(e)}"
                    })
                # 保存失败,直接返回,不继续向量存储
                return [], failed_chapters

        # 批量存储向量
        if successful_results:
            logger.info(f"🔍 开始批量存储向量...")
            try:
                await self._batch_store_vectors(
                    work_id=work_id,
                    analysis_id=analysis_id,
                    results=successful_results
                )
                logger.info(f"✅ 批量向量存储完成")
            except Exception as e:
                logger.warning(f"⚠️ 批量向量存储失败(不影响分析): {e}")

        # 注意: 进度已在batch_save_micro_results中更新,无需重复更新

        # 提取微观分析数据返回
        micro_results = [r['data'] for r in successful_results]

        return micro_results, failed_chapters

    async def _batch_store_vectors(
        self,
        work_id: str,
        analysis_id: str,
        results: List[Dict[str, Any]]
    ):
        """批量存储向量"""
        for result in results:
            try:
                await self.vector_service.store_micro_analysis_vector(
                    work_id=work_id,
                    chapter_id=result['chapter_id'],
                    analysis_id=analysis_id,
                    micro_data=result['data'],
                    chunk_index=0
                )
            except Exception as e:
                logger.warning(f"向量存储失败(章节 {result['chapter_id']}): {e}")

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
