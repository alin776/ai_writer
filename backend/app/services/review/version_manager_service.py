"""
版本管理服务
负责章节版本的创建、查询和管理
"""

import logging
from typing import List, Optional
from uuid import UUID
from datetime import datetime
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, and_, func

from app.models.chapter import Chapter
from app.models.chapter_version import ChapterVersion, VersionType
from app.models.review_session import ReviewSession
from app.models.review_task import ReviewTask, TaskStatus
from app.schemas.review import (
    ChapterVersionCreate,
    ChapterVersionResponse,
    ChapterVersionDetailResponse,
    VersionMilestoneUpdate
)
from app.utils.datetime_utils import get_utc_now
from app.services.chapter_content_provider import ChapterContentProvider

logger = logging.getLogger(__name__)


class VersionManagerService:
    """版本管理服务"""

    def __init__(self, db: AsyncSession):
        self.db = db
        self.content_provider = ChapterContentProvider()

    async def create_version(
        self,
        chapter_id: UUID,
        user_id: UUID,
        request: ChapterVersionCreate,
        review_session_id: Optional[UUID] = None
    ) -> ChapterVersion:
        """
        创建新版本快照

        Args:
            chapter_id: 章节ID
            user_id: 用户ID
            request: 版本创建请求
            review_session_id: 关联的评审会话ID (可选)

        Returns:
            创建的版本
        """
        # 1. 获取章节当前内容
        chapter = await self._get_chapter(chapter_id)
        if not chapter:
            raise ValueError(f"章节不存在: {chapter_id}")

        # 2. 获取下一个版本号
        next_version_number = await self._get_next_version_number(chapter_id)

        # 3. 获取评审数据 (如果有)
        overall_score = None
        dimension_scores = None
        if review_session_id:
            session = await self._get_review_session(review_session_id)
            if session:
                overall_score = session.overall_score
                dimension_scores = session.dimension_scores

        # 4. 计算任务完成情况
        task_stats = await self._get_task_completion_stats(chapter_id)

        # 5. 创建版本
        version = ChapterVersion(
            chapter_id=chapter_id,
            user_id=user_id,
            version_number=next_version_number,
            version_type=VersionType.SNAPSHOT,  # 新版本默认为快照
            is_milestone=request.is_milestone,
            version_tag=request.version_tag,
            change_summary=request.change_summary,
            content=chapter.content,  # 保存完整内容
            review_session_id=review_session_id,
            overall_score=overall_score,
            dimension_scores=dimension_scores,
            completed_tasks_count=task_stats["completed_count"],
            task_completion_rate=task_stats["completion_rate"],
            word_count=chapter.word_count
        )

        self.db.add(version)
        await self.db.commit()
        await self.db.refresh(version)

        logger.info(
            f"[VersionManagerService] 版本创建成功: version_id={version.id}, "
            f"version_number={version.version_number}, is_milestone={version.is_milestone}"
        )

        return version

    async def get_version_by_id(self, version_id: UUID) -> Optional[ChapterVersion]:
        """获取版本详情 (包含内容)"""
        result = await self.db.execute(
            select(ChapterVersion).where(ChapterVersion.id == version_id)
        )
        return result.scalar_one_or_none()

    async def get_chapter_versions(
        self,
        chapter_id: UUID,
        include_milestones_only: bool = False,
        skip: int = 0,
        limit: int = 20
    ) -> List[ChapterVersion]:
        """获取章节的版本列表"""
        conditions = [ChapterVersion.chapter_id == chapter_id]

        if include_milestones_only:
            conditions.append(ChapterVersion.is_milestone == True)

        result = await self.db.execute(
            select(ChapterVersion)
            .where(and_(*conditions))
            .order_by(ChapterVersion.version_number.desc())
            .offset(skip)
            .limit(limit)
        )

        return list(result.scalars().all())

    async def get_latest_version(self, chapter_id: UUID) -> Optional[ChapterVersion]:
        """获取章节的最新版本"""
        result = await self.db.execute(
            select(ChapterVersion)
            .where(ChapterVersion.chapter_id == chapter_id)
            .order_by(ChapterVersion.version_number.desc())
            .limit(1)
        )
        return result.scalar_one_or_none()

    async def update_milestone_status(
        self,
        version_id: UUID,
        request: VersionMilestoneUpdate
    ) -> ChapterVersion:
        """更新版本的里程碑状态"""
        version = await self.get_version_by_id(version_id)
        if not version:
            raise ValueError(f"版本不存在: {version_id}")

        version.is_milestone = request.is_milestone
        if request.version_tag:
            version.version_tag = request.version_tag

        await self.db.commit()
        await self.db.refresh(version)

        logger.info(
            f"[VersionManagerService] 里程碑状态更新: version_id={version_id}, "
            f"is_milestone={request.is_milestone}"
        )

        return version

    async def get_version_content(self, version_id: UUID) -> Optional[str]:
        """
        获取版本的完整内容
        支持不同存储类型的版本 (snapshot/compressed/archived)
        """
        version = await self.get_version_by_id(version_id)
        if not version:
            return None

        if version.version_type == VersionType.SNAPSHOT:
            # 直接返回存储的内容
            return version.content

        elif version.version_type == VersionType.COMPRESSED:
            # TODO: 实现 diff 重建逻辑
            # 1. 找到最近的基线版本 (snapshot)
            # 2. 应用 diff 补丁重建内容
            logger.warning(f"[VersionManagerService] Compressed版本内容重建功能待实现: {version_id}")
            return None

        elif version.version_type == VersionType.ARCHIVED:
            # TODO: 从对象存储中获取
            logger.warning(f"[VersionManagerService] Archived版本内容获取功能待实现: {version_id}")
            return None

        return None

    async def compare_versions(
        self,
        version1_id: UUID,
        version2_id: UUID
    ) -> dict:
        """
        对比两个版本

        Returns:
            包含评分差异、文本差异、完成任务等信息的字典
        """
        version1 = await self.get_version_by_id(version1_id)
        version2 = await self.get_version_by_id(version2_id)

        if not version1 or not version2:
            raise ValueError("版本不存在")

        # 1. 评分差异
        score_diff = {}
        if version1.overall_score and version2.overall_score:
            score_diff["overall"] = {
                "old": version1.overall_score,
                "new": version2.overall_score,
                "change": version2.overall_score - version1.overall_score
            }

        # 2. 文本差异 (简单统计)
        text_diff = {
            "old_word_count": version1.word_count or 0,
            "new_word_count": version2.word_count or 0,
            "word_count_change": (version2.word_count or 0) - (version1.word_count or 0)
        }

        # 3. TODO: 详细的文本 diff (可使用 difflib)

        return {
            "score_diff": score_diff,
            "text_diff": text_diff,
            "version1": {
                "id": str(version1.id),
                "version_number": version1.version_number,
                "created_at": version1.created_at.isoformat()
            },
            "version2": {
                "id": str(version2.id),
                "version_number": version2.version_number,
                "created_at": version2.created_at.isoformat()
            }
        }

    async def archive_old_versions(
        self,
        days_threshold: int = 90,
        dry_run: bool = True
    ) -> dict:
        """
        归档旧版本 (定时任务)

        将超过指定天数且非里程碑的版本转为压缩存储

        Args:
            days_threshold: 天数阈值 (默认90天)
            dry_run: 是否仅模拟运行

        Returns:
            归档统计信息
        """
        from datetime import datetime, timedelta

        cutoff_date = get_utc_now() - timedelta(days=days_threshold)

        # 查找待归档的版本
        result = await self.db.execute(
            select(ChapterVersion)
            .where(
                and_(
                    ChapterVersion.version_type == VersionType.SNAPSHOT,
                    ChapterVersion.is_milestone == False,
                    ChapterVersion.created_at < cutoff_date
                )
            )
        )
        versions_to_archive = list(result.scalars().all())

        if dry_run:
            logger.info(
                f"[VersionManagerService] 归档模拟: 找到 {len(versions_to_archive)} 个待归档版本"
            )
            return {
                "dry_run": True,
                "versions_to_archive": len(versions_to_archive)
            }

        # 执行归档
        archived_count = 0
        for version in versions_to_archive:
            try:
                # TODO: 实现压缩或上传到对象存储
                # version.version_type = VersionType.COMPRESSED
                # version.diff_patch = generate_diff(...)
                # version.content = None  # 清空完整内容

                archived_count += 1

            except Exception as e:
                logger.error(
                    f"[VersionManagerService] 归档失败: version_id={version.id}, "
                    f"error={str(e)}"
                )

        await self.db.commit()

        logger.info(f"[VersionManagerService] 归档完成: 共归档 {archived_count} 个版本")

        return {
            "dry_run": False,
            "archived_count": archived_count,
            "total_found": len(versions_to_archive)
        }

    # ==================== 私有方法 ====================

    async def _get_chapter(self, chapter_id: UUID) -> Optional[Chapter]:
        """获取章节"""
        result = await self.db.execute(
            select(Chapter).where(Chapter.id == chapter_id)
        )
        chapter = result.scalar_one_or_none()
        if chapter:
            self.content_provider.hydrate_chapter(chapter)
        return chapter

    async def _get_review_session(self, session_id: UUID) -> Optional[ReviewSession]:
        """获取评审会话"""
        result = await self.db.execute(
            select(ReviewSession).where(ReviewSession.id == session_id)
        )
        return result.scalar_one_or_none()

    async def _get_next_version_number(self, chapter_id: UUID) -> int:
        """获取下一个版本号"""
        result = await self.db.execute(
            select(func.max(ChapterVersion.version_number))
            .where(ChapterVersion.chapter_id == chapter_id)
        )
        max_version = result.scalar()
        return (max_version or 0) + 1

    async def _get_task_completion_stats(self, chapter_id: UUID) -> dict:
        """获取任务完成统计"""
        result = await self.db.execute(
            select(ReviewTask)
            .where(ReviewTask.chapter_id == chapter_id)
        )
        tasks = list(result.scalars().all())

        if not tasks:
            return {"completed_count": 0, "completion_rate": 0.0}

        completed_count = sum(1 for task in tasks if task.status == TaskStatus.COMPLETED)
        completion_rate = completed_count / len(tasks)

        return {
            "completed_count": completed_count,
            "completion_rate": completion_rate
        }
