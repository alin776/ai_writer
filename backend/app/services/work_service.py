import re
from pathlib import Path
from typing import Any, List, Optional
from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import func, or_, select
from sqlalchemy.orm import selectinload
from datetime import datetime, timezone
import asyncio
from pathlib import Path

from app.models.work import Work
from app.models.chapter import Chapter, ChapterStatus
from app.schemas.work import WorkCreate, WorkUpdate
from app.utils.cache import cache_result, CacheInvalidator
from app.core.redis import CacheKey, CacheExpire
from app.services.agent.deep_agent import DATA_ROOT
from app.services.agent.deep_agent.frontmatter import parse_chapter, build_chapter


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

    @staticmethod
    def _get_work_dir(user_id: str, work_id: str) -> Path:
        return DATA_ROOT / user_id / "works" / work_id

    @staticmethod
    def _list_chapter_files(chapters_dir: Path) -> list[tuple[int, Path]]:
        import re
        if not chapters_dir.exists():
            return []
        result = []
        for f in chapters_dir.iterdir():
            if f.is_file() and f.suffix == ".md":
                match = re.match(r"^(\d+)-(.+)\.md$", f.name)
                if match:
                    result.append((int(match.group(1)), f))
        result.sort(key=lambda x: x[0])
        return result

    async def publish_work(self, work_id: str, chapter_nums: List[int], user_id: str) -> Optional[Work]:
        """
        发布作品到小说广场

        Args:
            work_id: 作品ID
            chapter_nums: 要发布的章节序号列表 (如 [1, 2, 3])
            user_id: 用户ID (用于定位文件系统目录)

        Returns:
            更新后的作品对象
        """
        work = await self.get_work_by_id(work_id, use_cache=False)
        if not work:
            return None

        # 设置作品为已发布（仅首次发布时设置 published_at）
        work.is_published = True
        if work.published_at is None:
            work.published_at = datetime.now(timezone.utc)

        # 更新文件系统中章节的 status 和 published_at
        now_iso = datetime.now(timezone.utc).isoformat()
        chapters_dir = self._get_work_dir(user_id, work_id) / "chapters"
        if chapters_dir.exists():
            chapter_files = await asyncio.to_thread(self._list_chapter_files, chapters_dir)
            nums_set = set(chapter_nums)
            for num, path in chapter_files:
                raw = await asyncio.to_thread(path.read_text, "utf-8")
                parsed = parse_chapter(raw)
                if num in nums_set:
                    # 发布章节：如果尚未发布或缺少 published_at，则更新 frontmatter
                    if parsed["status"] != "published" or not parsed.get("published_at"):
                        new_content = build_chapter(
                            parsed["title"] or f"Chapter {num}",
                            "published",
                            parsed["content"],
                            published_at=parsed.get("published_at") or now_iso,
                        )
                        await asyncio.to_thread(path.write_text, new_content, "utf-8")
                elif num not in nums_set and parsed["status"] == "published":
                    # 取消发布的章节：恢复为 draft
                    new_content = build_chapter(parsed["title"] or f"Chapter {num}", "draft", parsed["content"])
                    await asyncio.to_thread(path.write_text, new_content, "utf-8")

        await self.db.commit()
        await self.db.refresh(work)

        # 使缓存失效
        await CacheInvalidator.invalidate_work(work_id)

        return work

    async def unpublish_work(self, work_id: str, user_id: str) -> Optional[Work]:
        """
        取消发布作品

        Args:
            work_id: 作品ID
            user_id: 用户ID

        Returns:
            更新后的作品对象
        """
        work = await self.get_work_by_id(work_id, use_cache=False)
        if not work:
            return None

        # 设置作品为未发布
        work.is_published = False

        # 将所有 FS 章节 status 从 published 恢复为 draft
        chapters_dir = self._get_work_dir(user_id, work_id) / "chapters"
        if chapters_dir.exists():
            chapter_files = await asyncio.to_thread(self._list_chapter_files, chapters_dir)
            for num, path in chapter_files:
                raw = await asyncio.to_thread(path.read_text, "utf-8")
                parsed = parse_chapter(raw)
                if parsed["status"] == "published":
                    new_content = build_chapter(parsed["title"] or f"Chapter {num}", "draft", parsed["content"])
                    await asyncio.to_thread(path.write_text, new_content, "utf-8")

        await self.db.commit()
        await self.db.refresh(work)

        # 使缓存失效
        await CacheInvalidator.invalidate_work(work_id)

        return work
