"""
图书分析核心服务

整合各个模块,提供完整的图书分析功能
"""

import os
import hashlib
import asyncio
import logging
from datetime import datetime
from typing import List, Dict, Optional, Any
from uuid import UUID
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.models.book_analysis import BookAnalysisJob, JobStatus
from app.models.worldview_suggestion import WorldviewSuggestion
from app.models.knowledge_item import KnowledgeItem, KnowledgeCategory
from app.services.book_analysis.strategy import strategy_registry
from app.services.book_analysis.smart_sampling import SmartSamplingAnalyzer, ChapterData

logger = logging.getLogger(__name__)
from app.services.book_analysis.suggestion_generator import SuggestionGenerator
from app.services.ai.http_ai_service import HTTPAIService
from app.services.knowledge_service import KnowledgeService


class BookAnalysisService:
    """
    图书分析核心服务

    负责整个分析流程的编排
    """

    def __init__(
        self,
        db: AsyncSession,
        ai_service: HTTPAIService,
        knowledge_service: KnowledgeService
    ):
        self.db = db
        self.ai_service = ai_service
        self.knowledge_service = knowledge_service
        self.sampler = SmartSamplingAnalyzer()
        self.suggestion_generator = SuggestionGenerator(ai_service)

    async def create_job(
        self,
        file_path: str,
        original_filename: str,
        file_size_bytes: int,
        user_id: UUID,
        book_title: Optional[str] = None,
        strategy_id: str = "web_novel_11d",
        work_id: Optional[UUID] = None
    ) -> BookAnalysisJob:
        """
        创建分析任务

        Args:
            file_path: 文件路径
            original_filename: 原始文件名
            file_size_bytes: 文件大小
            user_id: 用户ID
            book_title: 图书标题 (可选)
            strategy_id: 策略ID
            work_id: 关联作品ID (可选)

        Returns:
            创建的任务对象
        """
        # 计算文件哈希
        file_hash = await self._calculate_file_hash(file_path)

        # 检查是否已存在
        stmt = select(BookAnalysisJob).where(BookAnalysisJob.file_hash == file_hash)
        result = await self.db.execute(stmt)
        existing_job = result.scalar_one_or_none()

        if existing_job:
            raise ValueError(f"该图书已分析过,任务ID: {existing_job.id}")

        # 创建任务
        job = BookAnalysisJob(
            user_id=user_id,
            book_title=book_title or original_filename,
            original_filename=original_filename,
            file_format=os.path.splitext(original_filename)[1][1:],
            file_size_bytes=file_size_bytes,
            file_hash=file_hash,
            file_path=file_path,
            strategy_id=strategy_id,
            status=JobStatus.PENDING,
            extra_data={"work_id": str(work_id)} if work_id else {}
        )

        self.db.add(job)
        await self.db.commit()
        await self.db.refresh(job)

        return job

    async def analyze_book(
        self,
        job_id: UUID,
        user_id: UUID
    ):
        """
        执行图书分析 (异步任务)

        Args:
            job_id: 任务ID
            user_id: 用户ID
        """
        import logging
        logger = logging.getLogger(__name__)
        logger.info(f"📖 analyze_book 开始: job_id={job_id}, user_id={user_id}")

        # 获取任务
        job = await self.db.get(BookAnalysisJob, job_id)
        if not job:
            logger.error(f"❌ 任务不存在: {job_id}")
            raise ValueError(f"任务不存在: {job_id}")

        logger.info(f"✅ 获取到任务: {job.book_title}, file_path={job.file_path}")

        if job.user_id != user_id:
            raise ValueError(f"无权访问该任务")

        try:
            # 1. 更新状态为解析中
            job.status = JobStatus.PARSING
            job.started_at = datetime.utcnow()
            job.current_step = "正在解析图书结构..."
            await self.db.commit()
            logger.info(f"📄 开始解析文件: {job.file_path}")

            # 2. 解析图书
            chapters = await asyncio.to_thread(
                self.sampler.parse_txt_file,
                job.file_path
            )
            logger.info(f"📊 解析完成,识别到 {len(chapters)} 个章节")
            if len(chapters) == 0:
                logger.warning(f"⚠️ 未识别到任何章节!文件: {job.file_path}")
            else:
                for i, ch in enumerate(chapters[:3]):  # 只显示前3章
                    logger.info(f"  章节{i+1}: {ch.title} ({ch.word_count}字)")

            job.total_chapters = len(chapters)
            job.current_step = f"已识别 {len(chapters)} 个章节"
            job.progress = 10
            await self.db.commit()

            # 3. 选择分析章节
            selected_chapters = self.sampler.select_chapters_to_analyze(chapters)
            job.current_step = f"将分析 {len(selected_chapters)} 个章节"
            job.progress = 15
            await self.db.commit()

            # 4. 执行分析
            job.status = JobStatus.ANALYZING
            await self.db.commit()

            analysis_result = await self._analyze_chapters(
                job=job,
                selected_chapters=selected_chapters,
                strategy_id=job.strategy_id
            )

            # 5. 生成知识条目
            knowledge_items = await self._create_knowledge_items(
                job=job,
                analysis_result=analysis_result,
                user_id=user_id
            )
            job.extracted_items_count = len(knowledge_items)
            job.progress = 85
            await self.db.commit()

            # 6. 生成智能建议
            suggestions = await self._create_suggestions(
                job=job,
                analysis_result=analysis_result,
                user_id=user_id
            )
            job.suggestions_count = len(suggestions)
            job.progress = 95
            await self.db.commit()

            # 7. 完成
            job.status = JobStatus.COMPLETED
            job.current_step = f"分析完成! 提取了 {len(knowledge_items)} 个知识点, 生成了 {len(suggestions)} 个智能建议"
            job.progress = 100
            job.completed_at = datetime.utcnow()
            await self.db.commit()

        except Exception as e:
            # 错误处理
            job.status = JobStatus.FAILED
            job.error_message = str(e)
            job.retry_count += 1
            await self.db.commit()
            raise

    async def _analyze_single_chapter(
        self,
        chapter: ChapterData,
        chapter_index: int,
        is_incremental: bool,
        existing_settings: Optional[Dict[str, Any]],
        strategy,
        system_prompt: str
    ) -> tuple[int, Optional[Dict[str, Any]], Optional[str]]:
        """
        分析单个章节 (用于并行调用)

        Args:
            chapter: 章节数据
            chapter_index: 章节索引
            is_incremental: 是否增量分析
            existing_settings: 已有的分析结果
            strategy: 分析策略
            system_prompt: 系统提示词

        Returns:
            (章节索引, 分析结果dict, 错误信息)
        """
        try:
            # 构建提示词
            content = self.sampler.truncate_content(chapter.content)
            user_prompt = strategy.build_user_prompt(
                content=content,
                existing_settings=existing_settings if is_incremental else None,
                is_incremental=is_incremental,
                chapter_num=chapter.index
            )

            # 调用AI
            response_text = await self.ai_service.call_ai(
                system_prompt=system_prompt,
                user_prompt=user_prompt,
                max_tokens=3000,
                temperature=0.3
            )

            # 保存AI响应到临时文件(调试用)
            import os
            debug_dir = os.path.join(os.getcwd(), 'debug_ai_responses')
            os.makedirs(debug_dir, exist_ok=True)
            debug_file = os.path.join(debug_dir, f'ch{chapter_index+1}_{chapter.title[:10]}.txt')
            with open(debug_file, 'w', encoding='utf-8') as f:
                f.write(response_text)
            logger.info(f"💾 AI响应已保存到: {debug_file}")

            # 解析响应
            chapter_result = strategy.parse_ai_response(response_text)
            logger.info(f"✅ 章节{chapter_index+1} '{chapter.title}' 分析成功,获得 {len(chapter_result)} 个维度")

            # 检查是否无新内容
            if chapter_result.get("no_new_content"):
                return (chapter_index, None, None)

            return (chapter_index, chapter_result, None)

        except Exception as e:
            error_msg = f"章节{chapter_index+1} '{chapter.title}' 分析失败: {type(e).__name__}: {e}"
            logger.error(f"❌ {error_msg}")
            return (chapter_index, None, error_msg)

    async def _analyze_chapters(
        self,
        job: BookAnalysisJob,
        selected_chapters: List[Dict[str, Any]],
        strategy_id: str
    ) -> Dict[str, Any]:
        """
        分析选中的章节 (改进的并行化版本)

        策略: 前N章深度分析(串行)，后续章节并行增量分析

        Args:
            job: 任务对象
            selected_chapters: 选中的章节列表
            strategy_id: 策略ID

        Returns:
            聚合的分析结果
        """
        strategy = strategy_registry.get(strategy_id)
        if not strategy:
            raise ValueError(f"策略不存在: {strategy_id}")

        aggregated_result = {}
        total = len(selected_chapters)
        system_prompt = strategy.build_system_prompt()

        # 分组: 深度分析章节(串行) vs 增量分析章节(可并行)
        deep_chapters = selected_chapters[:self.sampler.deep_analysis_chapters]
        incremental_chapters = selected_chapters[self.sampler.deep_analysis_chapters:]

        logger.info(f"📊 开始分析 {total} 个章节: {len(deep_chapters)}个深度分析(串行), {len(incremental_chapters)}个增量分析(并行)")

        # === 阶段1: 深度分析章节 (串行, 建立基础) ===
        for i, item in enumerate(deep_chapters):
            chapter: ChapterData = item["chapter"]

            # 更新进度
            job.current_step = f"深度分析: {chapter.title} ({i+1}/{len(deep_chapters)})"
            job.progress = 20 + int((i / len(deep_chapters)) * 30)
            job.analyzed_chapters = i + 1
            await self.db.commit()

            logger.info(f"🔍 深度分析章节 {i+1}: {chapter.title}")

            try:
                chapter_index, chapter_result, error_msg = await self._analyze_single_chapter(
                    chapter=chapter,
                    chapter_index=i,
                    is_incremental=False,  # 深度分析不是增量
                    existing_settings=None,
                    strategy=strategy,
                    system_prompt=system_prompt
                )

                if error_msg:
                    logger.error(f"❌ 章节分析失败: {error_msg}")
                    continue

                if chapter_result:
                    # 合并到聚合结果
                    for dim_id, data in chapter_result.items():
                        if dim_id not in aggregated_result:
                            aggregated_result[dim_id] = data
                        else:
                            # 更新描述
                            existing_desc = aggregated_result[dim_id].get("description", "")
                            new_desc = data.get("description", "")
                            if new_desc and new_desc not in existing_desc:
                                aggregated_result[dim_id]["description"] = existing_desc + "\n" + new_desc

                            # 合并子元素
                            existing_children = aggregated_result[dim_id].get("children", [])
                            new_children = data.get("children", [])
                            aggregated_result[dim_id]["children"] = existing_children + new_children

                # 避免API限流
                await asyncio.sleep(0.5)

            except Exception as e:
                logger.error(f"❌ 深度分析异常: {e}")
                continue

        logger.info(f"✅ 深度分析完成, 建立了 {len(aggregated_result)} 个维度的基础")

        # === 阶段2: 增量分析章节 (并行, 基于已有结果) ===
        if incremental_chapters:
            logger.info(f"🚀 开始并行增量分析 {len(incremental_chapters)} 个章节...")

            # 使用信号量控制并发
            MAX_CONCURRENT = 3
            semaphore = asyncio.Semaphore(MAX_CONCURRENT)
            progress_lock = asyncio.Lock()  # 进度更新锁

            async def analyze_incremental(i: int, item: Dict[str, Any]):
                """并行增量分析任务"""
                async with semaphore:
                    chapter: ChapterData = item["chapter"]
                    actual_index = len(deep_chapters) + i

                    # 线程安全的进度更新
                    async with progress_lock:
                        job.current_step = f"增量分析: {chapter.title} ({actual_index+1}/{total})"
                        job.progress = 50 + int((i / len(incremental_chapters)) * 30)
                        job.analyzed_chapters = actual_index + 1
                        await self.db.commit()

                    logger.info(f"📝 增量分析章节 {actual_index+1}: {chapter.title}")

                    result = await self._analyze_single_chapter(
                        chapter=chapter,
                        chapter_index=actual_index,
                        is_incremental=True,
                        existing_settings=aggregated_result.copy(),  # 传递副本避免竞态
                        strategy=strategy,
                        system_prompt=system_prompt
                    )

                    await asyncio.sleep(0.3)
                    return result

            # 并行执行增量分析
            tasks = [analyze_incremental(i, item) for i, item in enumerate(incremental_chapters)]
            results = await asyncio.gather(*tasks, return_exceptions=True)

            # 处理增量分析结果
            successful_count = 0
            failed_count = 0

            for result in results:
                if isinstance(result, Exception):
                    logger.error(f"❌ 增量分析异常: {result}")
                    failed_count += 1
                    continue

                chapter_index, chapter_result, error_msg = result

                if error_msg:
                    failed_count += 1
                    continue

                if not chapter_result:
                    continue

                successful_count += 1

                # 合并增量结果
                for dim_id, data in chapter_result.items():
                    if dim_id not in aggregated_result:
                        aggregated_result[dim_id] = data
                    else:
                        existing_desc = aggregated_result[dim_id].get("description", "")
                        new_desc = data.get("description", "")
                        if new_desc and new_desc not in existing_desc:
                            aggregated_result[dim_id]["description"] = existing_desc + "\n" + new_desc

                        existing_children = aggregated_result[dim_id].get("children", [])
                        new_children = data.get("children", [])
                        aggregated_result[dim_id]["children"] = existing_children + new_children

            logger.info(f"✅ 增量分析完成: 成功{successful_count}个, 失败{failed_count}个")

        logger.info(f"📊 章节分析全部完成, 共{len(aggregated_result)}个维度")
        return aggregated_result

    async def _create_knowledge_items(
        self,
        job: BookAnalysisJob,
        analysis_result: Dict[str, Any],
        user_id: UUID
    ) -> List[KnowledgeItem]:
        """
        从分析结果创建知识条目 (批量向量化优化版本)

        优化: 扩展到所有11个维度,不再只提取technique和plot_structure
        """
        # 维度类型到知识库类别的映射
        DIMENSION_TO_CATEGORY = {
            "technique": KnowledgeCategory.TECHNIQUE,
            "plot_structure": KnowledgeCategory.PLOT,
            "character_template": KnowledgeCategory.CHARACTER,
            "power_system": KnowledgeCategory.WORLDVIEW,
            "setting": KnowledgeCategory.WORLDVIEW,
            "worldview": KnowledgeCategory.WORLDVIEW,
            "emotional_line": KnowledgeCategory.PLOT,
            "relationship": KnowledgeCategory.PLOT,  # 关系线
            "conflict": KnowledgeCategory.PLOT,
            "theme": KnowledgeCategory.TECHNIQUE,
            "pacing": KnowledgeCategory.TECHNIQUE,
            "hook": KnowledgeCategory.TECHNIQUE,
        }

        items = []
        logger.info(f"📚 开始提取知识点,共 {len(analysis_result)} 个维度")

        for dim_id, data in analysis_result.items():
            dimension_type = data.get("dimension_type")
            logger.info(f"  - 维度 '{dim_id}': dimension_type={dimension_type}")

            # 旧策略: 只提取technique和plot_structure
            # 新策略: 提取所有维度 (根据INFO.md优化建议)
            if dimension_type not in DIMENSION_TO_CATEGORY:
                logger.info(f"    ⚠️ 未知维度类型,使用默认分类TECHNIQUE")
                category = KnowledgeCategory.TECHNIQUE
            else:
                category = DIMENSION_TO_CATEGORY[dimension_type]

            name = data.get("name", "")
            description = data.get("description", "")

            if not description:
                logger.info(f"    ❌ 跳过(描述为空)")
                continue

            logger.info(f"    ✅ 创建知识点: {name} (类别: {category.value})")

            # 创建知识条目 - 使用 KnowledgeItemCreate schema
            from app.schemas.knowledge import KnowledgeItemCreate

            # 根据类型选择合适的图标
            type_icons = {
                KnowledgeCategory.TECHNIQUE: "💡",
                KnowledgeCategory.PLOT: "📖",
                KnowledgeCategory.CHARACTER: "👤",
                KnowledgeCategory.WORLDVIEW: "🌍",
            }
            icon = type_icons.get(category, "💡")

            knowledge_create = KnowledgeItemCreate(
                title=f"{icon} {name}",
                content=description,
                category=category,
                tags=[job.book_title, name, dimension_type],
                source_type="book_analysis",  # 小写格式
                source_id=str(job.id),
                source_reference=f"{job.book_title} - {name}",
                extra_data={
                    "book_title": job.book_title,
                    "dimension_id": dim_id,
                    "dimension_name": name,
                    "extraction_type": dimension_type
                }
            )

            item = await self.knowledge_service.create_item(
                user_id=str(user_id),
                data=knowledge_create,
                skip_vectorization=True  # 跳过单个向量化,使用批量向量化
            )

            items.append(item)

        # 批量向量化所有知识条目 (优化点!)
        if items:
            logger.info(f"🚀 开始批量向量化 {len(items)} 个知识条目...")
            try:
                await self.knowledge_service.vector_service.add_knowledge_batch(items)
                logger.info(f"✅ 批量向量化成功")
            except Exception as e:
                logger.error(f"❌ 批量向量化失败: {e}")
                # 失败时回退到逐个向量化
                logger.info("⚠️ 回退到逐个向量化...")
                for item in items:
                    try:
                        await self.knowledge_service.vector_service.add_knowledge(item)
                    except Exception as item_e:
                        logger.error(f"❌ 知识条目 {item.id} 向量化失败: {item_e}")

        logger.info(f"📚 知识点提取完成,共创建 {len(items)} 个知识条目")
        logger.info(f"   - 相比旧策略,覆盖率提升: 从2个类型扩展到所有维度")
        return items

    async def _create_suggestions(
        self,
        job: BookAnalysisJob,
        analysis_result: Dict[str, Any],
        user_id: UUID
    ) -> List[WorldviewSuggestion]:
        """
        从分析结果生成智能建议
        """
        logger.info(f"💡 开始生成智能建议,共 {len(analysis_result)} 个维度")

        work_id = job.extra_data.get("work_id") if job.extra_data else None
        if work_id:
            work_id = UUID(work_id)

        # 生成建议数据
        suggestion_dicts = self.suggestion_generator.generate_suggestions(
            analysis_result=analysis_result,
            job_id=job.id,
            user_id=user_id,
            work_id=work_id,
            strategy_id=job.strategy_id
        )

        logger.info(f"💡 建议生成器返回 {len(suggestion_dicts)} 个建议")

        # 创建建议对象
        suggestions = []
        for suggestion_data in suggestion_dicts:
            suggestion = WorldviewSuggestion(**suggestion_data)
            self.db.add(suggestion)
            suggestions.append(suggestion)

        await self.db.commit()

        logger.info(f"💡 智能建议生成完成,共创建 {len(suggestions)} 个建议")
        return suggestions

    async def _calculate_file_hash(self, file_path: str) -> str:
        """计算文件SHA256哈希"""
        hasher = hashlib.sha256()
        with open(file_path, 'rb') as f:
            for chunk in iter(lambda: f.read(4096), b""):
                hasher.update(chunk)
        return hasher.hexdigest()
