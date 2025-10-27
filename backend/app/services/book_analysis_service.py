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

    async def _analyze_chapters(
        self,
        job: BookAnalysisJob,
        selected_chapters: List[Dict[str, Any]],
        strategy_id: str
    ) -> Dict[str, Any]:
        """
        分析选中的章节

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

        for i, item in enumerate(selected_chapters):
            chapter: ChapterData = item["chapter"]
            is_deep = item["is_deep_analysis"]

            # 更新进度
            job.current_step = f"正在分析: {chapter.title} ({i+1}/{total})"
            job.progress = 20 + int((i / total) * 60)
            job.analyzed_chapters = i + 1
            await self.db.commit()

            # 构建提示词
            content = self.sampler.truncate_content(chapter.content)

            # 增量分析模式
            is_incremental = i >= self.sampler.deep_analysis_chapters
            user_prompt = strategy.build_user_prompt(
                content=content,
                existing_settings=aggregated_result if is_incremental else None,
                is_incremental=is_incremental,
                chapter_num=chapter.index
            )

            # 调用AI
            system_prompt = strategy.build_system_prompt()

            try:
                response_text = await self.ai_service.call_ai(
                    system_prompt=system_prompt,
                    user_prompt=user_prompt,
                    max_tokens=1000,  # 降低token数加快响应
                    temperature=0.3
                )

                # 解析响应
                chapter_result = strategy.parse_ai_response(response_text)

                # 检查是否无新内容
                if chapter_result.get("no_new_content"):
                    continue

                # 合并到聚合结果
                for dim_id, data in chapter_result.items():
                    if dim_id not in aggregated_result:
                        aggregated_result[dim_id] = data
                    else:
                        # 更新描述 (追加新内容)
                        existing_desc = aggregated_result[dim_id].get("description", "")
                        new_desc = data.get("description", "")
                        if new_desc and new_desc not in existing_desc:
                            aggregated_result[dim_id]["description"] = existing_desc + "\n" + new_desc

                        # 合并子元素
                        existing_children = aggregated_result[dim_id].get("children", [])
                        new_children = data.get("children", [])
                        # TODO: 更智能的合并逻辑
                        aggregated_result[dim_id]["children"] = existing_children + new_children

            except Exception as e:
                logger.error(f"❌ 分析章节失败: {chapter.title}, 错误: {type(e).__name__}: {e}")
                continue

            # 避免API限流
            await asyncio.sleep(1)

        return aggregated_result

    async def _create_knowledge_items(
        self,
        job: BookAnalysisJob,
        analysis_result: Dict[str, Any],
        user_id: UUID
    ) -> List[KnowledgeItem]:
        """
        从分析结果创建知识条目

        将 TECHNIQUE 类型的维度创建为知识库条目
        """
        items = []

        for dim_id, data in analysis_result.items():
            dimension_type = data.get("dimension_type")

            # 只有 TECHNIQUE 和 PLOT_STRUCTURE 类型创建为知识条目
            if dimension_type not in ["technique", "plot_structure"]:
                continue

            name = data.get("name", "")
            description = data.get("description", "")

            # 创建知识条目
            item = await self.knowledge_service.create(
                user_id=user_id,
                title=f"💡 {name}",
                content=description,
                category=KnowledgeCategory.TECHNIQUE,
                tags=[job.book_title, name],
                source_type="BOOK_ANALYSIS",
                source_id=str(job.id),
                source_reference=f"{job.book_title} - {name}",
                extra_data={
                    "book_title": job.book_title,
                    "dimension_id": dim_id,
                    "dimension_name": name,
                    "extraction_type": dimension_type
                }
            )

            items.append(item)

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

        # 创建建议对象
        suggestions = []
        for suggestion_data in suggestion_dicts:
            suggestion = WorldviewSuggestion(**suggestion_data)
            self.db.add(suggestion)
            suggestions.append(suggestion)

        await self.db.commit()

        return suggestions

    async def _calculate_file_hash(self, file_path: str) -> str:
        """计算文件SHA256哈希"""
        hasher = hashlib.sha256()
        with open(file_path, 'rb') as f:
            for chunk in iter(lambda: f.read(4096), b""):
                hasher.update(chunk)
        return hasher.hexdigest()
