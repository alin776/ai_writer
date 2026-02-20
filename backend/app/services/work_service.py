import re
from pathlib import Path
from typing import Any, List, Optional
from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import func, or_, select
from sqlalchemy.orm import selectinload
from datetime import datetime, timezone

from app.models.work import Work
from app.models.chapter import Chapter, ChapterStatus
from app.schemas.work import WorkCreate, WorkUpdate
from app.utils.cache import cache_result, CacheInvalidator
from app.core.redis import CacheKey, CacheExpire
from app.services.agent.deep_agent import DATA_ROOT
from app.services.agent.deep_agent.frontmatter import parse_chapter


_FS_CHAPTER_ID_RE = re.compile(r"^fs-(\d+)$", re.IGNORECASE)
_FS_CHAPTER_FILE_RE = re.compile(r"^(\d+)-.+\.md$")


class WorkService:
    """作品服务"""
    
    def __init__(self, db: AsyncSession):
        self.db = db

    @staticmethod
    def _split_chapter_ids(chapter_ids: List[str]) -> tuple[list[UUID], list[int]]:
        """Split chapter ids into DB UUID ids and fs-N numeric orders."""
        uuid_ids: list[UUID] = []
        fs_orders: list[int] = []
        for raw in chapter_ids:
            text = (raw or "").strip()
            if not text:
                continue
            fs_match = _FS_CHAPTER_ID_RE.match(text)
            if fs_match:
                fs_orders.append(int(fs_match.group(1)))
                continue
            try:
                uuid_ids.append(UUID(text))
            except ValueError:
                continue
        return uuid_ids, fs_orders

    @staticmethod
    def _load_fs_chapters(work: Work) -> dict[int, dict[str, Any]]:
        """Load chapter metadata/content from filesystem for the given work."""
        chapters_dir = DATA_ROOT / str(work.author_id) / "works" / str(work.id) / "chapters"
        if not chapters_dir.exists():
            return {}

        fs_chapters: dict[int, dict[str, Any]] = {}
        for md_file in sorted(chapters_dir.glob("*.md")):
            if not md_file.is_file():
                continue
            match = _FS_CHAPTER_FILE_RE.match(md_file.name)
            if not match:
                continue
            order = int(match.group(1))
            try:
                raw = md_file.read_text("utf-8")
                parsed = parse_chapter(raw)
            except Exception:
                continue

            title = (parsed.get("title") or "").strip()
            if not title:
                stem_parts = Path(md_file.stem).name.split("-", 1)
                title = stem_parts[1] if len(stem_parts) > 1 else f"Chapter {order}"

            fs_chapters[order] = {
                "title": title,
                "content": parsed.get("content") or "",
                "word_count": int(parsed.get("word_count") or 0),
            }

        return fs_chapters
    
    async def get_work_by_id(self, work_id: str, use_cache: bool = True) -> Optional[Work]:
        """
        根据 ID 获取作品
        
        Args:
            work_id: 作品ID
            use_cache: 是否使用缓存（暂时禁用读取，只保留失效功能）
        """
        # TODO: 暂时禁用缓存读取，因为 SQLAlchemy 模型序列化有问题
        # 需要使用 Pydantic 模型或其他序列化方案
        
        # 从数据库查询
        result = await self.db.execute(
            select(Work)
            .options(selectinload(Work.chapters))
            .where(Work.id == work_id)
        )
        work = result.scalar_one_or_none()
        
        return work
    
    async def get_works(
        self,
        author_id: Optional[str] = None,
        skip: int = 0,
        limit: int = 100,
        search: Optional[str] = None
    ) -> tuple[List[Work], int]:
        """获取作品列表"""
        query = select(Work)
        count_query = select(func.count(Work.id))
        
        if author_id:
            query = query.where(Work.author_id == author_id)
            count_query = count_query.where(Work.author_id == author_id)
        
        if search:
            query = query.where(Work.title.ilike(f"%{search}%"))
            count_query = count_query.where(Work.title.ilike(f"%{search}%"))
        
        # 获取总数
        total_result = await self.db.execute(count_query)
        total = total_result.scalar()
        
        # 获取列表
        query = query.offset(skip).limit(limit).order_by(Work.updated_at.desc())
        result = await self.db.execute(query)
        works = result.scalars().all()
        
        return works, total
    
    async def create_work(self, author_id: str, work_data: WorkCreate) -> Work:
        """创建作品"""
        work = Work(
            author_id=author_id,
            **work_data.model_dump()
        )
        
        self.db.add(work)
        await self.db.commit()
        await self.db.refresh(work)
        
        return work
    
    async def update_work(self, work_id: str, work_data: WorkUpdate) -> Optional[Work]:
        """更新作品"""
        work = await self.get_work_by_id(work_id, use_cache=False)
        if not work:
            return None
        
        # 更新字段
        update_data = work_data.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(work, field, value)
        
        await self.db.commit()
        await self.db.refresh(work)
        
        # 使缓存失效
        await CacheInvalidator.invalidate_work(work_id)
        
        return work
    
    async def delete_work(self, work_id: str) -> bool:
        """删除作品"""
        work = await self.get_work_by_id(work_id, use_cache=False)
        if not work:
            return False
        
        await self.db.delete(work)
        await self.db.commit()
        
        # 使缓存失效
        await CacheInvalidator.invalidate_work(work_id)
        
        return True
    
    async def update_work_stats(self, work_id: str):
        """更新作品统计信息"""
        work = await self.get_work_by_id(work_id)
        if not work:
            return

        # 统计章节数和总字数
        result = await self.db.execute(
            select(
                func.count(Chapter.id),
                func.sum(Chapter.word_count)
            ).where(Chapter.work_id == work_id)
        )
        chapter_count, total_words = result.one()

        work.total_chapters = chapter_count or 0
        work.total_words = total_words or 0

        await self.db.commit()

    async def publish_work(self, work_id: str, chapter_ids: List[str]) -> Optional[Work]:
        """
        发布作品到小说广场

        Args:
            work_id: 作品ID
            chapter_ids: 要发布的章节ID列表

        Returns:
            更新后的作品对象
        """
        work = await self.get_work_by_id(work_id, use_cache=False)
        if not work:
            return None

        # 设置作品为已发布
        work.is_published = True
        work.published_at = datetime.now(timezone.utc)

        # 兼容两种章节 ID：
        # 1) UUID（历史 DB 章节） 2) fs-N（文件系统章节）
        uuid_ids, fs_orders = self._split_chapter_ids(chapter_ids or [])
        fs_selected = set(fs_orders)
        fs_chapters = self._load_fs_chapters(work) if fs_selected else {}

        selected_filters = []
        if uuid_ids:
            selected_filters.append(Chapter.id.in_(uuid_ids))
        if fs_selected:
            selected_filters.append(Chapter.order.in_(sorted(fs_selected)))

        selected_chapters: list[Chapter] = []
        if selected_filters:
            result = await self.db.execute(
                select(Chapter).where(
                    Chapter.work_id == work.id,
                    or_(*selected_filters),
                )
            )
            selected_chapters = list(result.scalars().all())

        # fs-N 对应章节在 DB 不存在时，按 order 补建一条，避免发布时报 UUID 错误
        if fs_selected:
            existing_by_order = {int(ch.order): ch for ch in selected_chapters}
            for order in sorted(fs_selected):
                payload = fs_chapters.get(order)
                if payload is None:
                    continue

                chapter = existing_by_order.get(order)
                if chapter is None:
                    chapter = Chapter(
                        work_id=work.id,
                        title=payload["title"],
                        content=payload["content"],
                        order=order,
                        word_count=payload["word_count"],
                        status=ChapterStatus.DRAFT,
                        is_published=False,
                    )
                    self.db.add(chapter)
                    selected_chapters.append(chapter)
                    existing_by_order[order] = chapter
                else:
                    # 用文件系统最新数据刷新基础字段，避免发布列表标题/字数过旧
                    chapter.title = payload["title"]
                    chapter.content = payload["content"]
                    chapter.word_count = payload["word_count"]

        publish_at = datetime.now(timezone.utc)
        for chapter in selected_chapters:
            chapter.is_published = True
            chapter.status = ChapterStatus.PUBLISHED
            chapter.published_at = publish_at

        # 文件系统章节作为主源时，同步作品统计到最新值
        if fs_chapters:
            work.total_chapters = len(fs_chapters)
            work.total_words = sum(int(item.get("word_count", 0)) for item in fs_chapters.values())

        await self.db.commit()
        await self.db.refresh(work)

        # 使缓存失效
        await CacheInvalidator.invalidate_work(work_id)

        return work

    async def unpublish_work(self, work_id: str) -> Optional[Work]:
        """
        取消发布作品

        Args:
            work_id: 作品ID

        Returns:
            更新后的作品对象
        """
        work = await self.get_work_by_id(work_id, use_cache=False)
        if not work:
            return None

        # 设置作品为未发布
        work.is_published = False

        # 同时取消所有章节的发布状态
        result = await self.db.execute(
            select(Chapter).where(Chapter.work_id == work_id)
        )
        chapters = result.scalars().all()
        for chapter in chapters:
            chapter.is_published = False

        await self.db.commit()
        await self.db.refresh(work)

        # 使缓存失效
        await CacheInvalidator.invalidate_work(work_id)

        return work
