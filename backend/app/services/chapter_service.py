from typing import List, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from sqlalchemy.orm.attributes import set_committed_value
import re
import logging

from app.models.chapter import Chapter, ChapterStatus
from app.schemas.chapter import ChapterCreate, ChapterUpdate
from app.utils.cache import CacheInvalidator
from app.core.redis import redis_client, CacheKey, CacheExpire
from app.services.chapter_history_service import ChapterHistoryService
from app.services.chapter_word_stat_service import ChapterWordStatService
from app.services.chapter_content_provider import ChapterContentProvider
from app.services.chapter_content_index_service import ChapterContentIndexService
from app.utils.chapter_file_storage import chapter_storage

logger = logging.getLogger(__name__)


def calculate_word_count(content: str) -> int:
    """
    计算文本字数（去除HTML标签）
    - 移除所有HTML标签
    - 中文：按字符数
    - 英文：按单词数
    - 数字：按字符数
    """
    if not content:
        return 0
    
    # 移除HTML标签
    text = re.sub(r'<[^>]+>', '', content)
    
    # 移除多余的空白字符
    text = re.sub(r'\s+', ' ', text).strip()
    
    # 计算中文字符数
    chinese_chars = len(re.findall(r'[\u4e00-\u9fff]', text))
    
    # 计算英文单词数
    english_words = len(re.findall(r'[a-zA-Z]+', text))
    
    # 计算数字字符数
    digits = len(re.findall(r'[0-9]', text))
    
    # 返回总字数（中文字符 + 英文单词 + 数字）
    return chinese_chars + english_words + digits


class ChapterService:
    """章节服务"""
    
    def __init__(self, db: AsyncSession):
        self.db = db
        self.content_provider = ChapterContentProvider()
        self.index_service = ChapterContentIndexService(db)
    
    async def get_chapter_by_id(self, chapter_id: str) -> Optional[Chapter]:
        """根据 ID 获取章节"""
        result = await self.db.execute(
            select(Chapter).where(Chapter.id == chapter_id)
        )
        chapter = result.scalar_one_or_none()
        if chapter:
            self.content_provider.hydrate_chapter(chapter)
        return chapter
    
    async def get_chapters_by_work(
        self,
        work_id: str,
        skip: int = 0,
        limit: int = 1000
    ) -> List[Chapter]:
        """获取作品的章节列表"""
        from uuid import UUID
        import logging
        logger = logging.getLogger(__name__)
        
        # 将字符串转换为UUID对象
        if isinstance(work_id, str):
            work_id_uuid = UUID(work_id)
        else:
            work_id_uuid = work_id
        
        logger.info(f"[ChapterService] Querying chapters for work_id={work_id_uuid}, type={type(work_id_uuid)}")
        
        result = await self.db.execute(
            select(Chapter)
            .where(Chapter.work_id == work_id_uuid)
            .order_by(Chapter.order)
            .offset(skip)
            .limit(limit)
        )
        chapters = list(result.scalars().all())

        logger.info(f"[ChapterService] Found {len(chapters)} chapters")
        if chapters:
            logger.info(f"  - Chapter: {chapters[0].title}, order={chapters[0].order}")
            if len(chapters) > 2:
                logger.info(f"  - ... ({len(chapters) - 2} more chapters)")
            if len(chapters) > 1:
                logger.info(f"  - Chapter: {chapters[-1].title}, order={chapters[-1].order}")

        for chapter in chapters:
            self.content_provider.hydrate_chapter(chapter)

        return chapters
    
    async def create_chapter(self, chapter_data: ChapterCreate) -> Chapter:
        """创建章节"""
        # 如果没有指定顺序，自动计算
        if chapter_data.order is None:
            result = await self.db.execute(
                select(func.max(Chapter.order))
                .where(Chapter.work_id == chapter_data.work_id)
            )
            max_order = result.scalar()
            order = (max_order or 0) + 1
        else:
            order = chapter_data.order
        
        # 计算字数（去除HTML标签）
        content_text = chapter_data.content or ""
        word_count = calculate_word_count(content_text)

        # 解析章节状态
        status_value = ChapterStatus.DRAFT
        if getattr(chapter_data, "status", None) is not None:
            raw_status = chapter_data.status.value if hasattr(chapter_data.status, "value") else chapter_data.status
            status_value = ChapterStatus(raw_status)
        elif getattr(chapter_data, "is_published", None) is not None:
            status_value = ChapterStatus.PUBLISHED if chapter_data.is_published else ChapterStatus.DRAFT
        
        is_published = (
            chapter_data.is_published
            if getattr(chapter_data, "is_published", None) is not None
            else status_value == ChapterStatus.PUBLISHED
        )
        
        chapter = Chapter(
            work_id=chapter_data.work_id,
            title=chapter_data.title,
            content="",
            order=order,
            word_count=word_count,
            status=status_value,
            is_published=is_published,
        )
        
        self.db.add(chapter)
        await self.db.commit()
        await self.db.refresh(chapter)
        set_committed_value(chapter, "content", content_text)

        try:
            chapter_storage.write_content(
                str(chapter.work_id), str(chapter.id), content_text
            )
            await self.index_service.upsert_from_content(
                str(chapter.work_id), str(chapter.id), content_text
            )
        except Exception as exc:
            logger.error(f"[ChapterService] 写入章节文件或索引失败: {exc}")

        # 记录历史，便于后续增量统计
        history_service = ChapterHistoryService(self.db)
        try:
            await history_service.save_history(
                chapter_id=str(chapter.id),
                content=content_text,
                version=chapter.version,
                modified_by="user",
                operation="create",
                description="初始创建快照"
            )
        except Exception:
            # 不影响主流程
            pass

        # 记录增量（新建章节，delta = 总字数）
        try:
            stat_service = ChapterWordStatService(self.db)
            # 获取 edit_event_id（如果前端传递了）
            edit_event_id = getattr(chapter_data, 'edit_event_id', None)
            await stat_service.add_delta(chapter.id, word_count, edit_event_id=edit_event_id)
        except Exception as e:
            logger.warning(f"Failed to record word count delta for chapter {chapter.id}: {e}")
            pass

        return chapter

    async def create_chapter_simple(
        self,
        work_id: str,
        title: str,
        content: str = "",
        order: Optional[int] = None,
        chapter_id: Optional[str] = None
    ) -> Chapter:
        """
        简化版创建章节（供 Agent 审批流程使用）

        Args:
            work_id: 作品ID
            title: 章节标题
            content: 章节内容
            order: 章节顺序（可选，默认追加到末尾）
            chapter_id: 预生成的章节ID（可选）

        Returns:
            创建的章节对象
        """
        from app.schemas.chapter import ChapterCreate

        chapter_data = ChapterCreate(
            work_id=work_id,
            title=title,
            content=content,
            order=order
        )

        # 如果提供了预生成的 chapter_id，需要特殊处理
        if chapter_id:
            # 如果没有指定顺序，自动计算
            if order is None:
                result = await self.db.execute(
                    select(func.max(Chapter.order))
                    .where(Chapter.work_id == work_id)
                )
                max_order = result.scalar()
                order = (max_order or 0) + 1

            content_text = content or ""
            word_count = calculate_word_count(content_text)

            chapter = Chapter(
                id=chapter_id,  # 使用预生成的 ID
                work_id=work_id,
                title=title,
                content="",
                order=order,
                word_count=word_count,
                status=ChapterStatus.DRAFT,
                is_published=False,
            )

            self.db.add(chapter)
            await self.db.commit()
            await self.db.refresh(chapter)
            set_committed_value(chapter, "content", content_text)
            try:
                chapter_storage.write_content(
                    str(chapter.work_id), str(chapter.id), content_text
                )
                await self.index_service.upsert_from_content(
                    str(chapter.work_id), str(chapter.id), content_text
                )
            except Exception as exc:
                logger.error(f"[ChapterService] 写入章节文件或索引失败: {exc}")
            return chapter

        # 否则使用标准创建流程
        return await self.create_chapter(chapter_data)

    async def update_chapter(self, chapter_id: str, chapter_data: ChapterUpdate) -> Optional[Chapter]:
        """更新章节"""
        chapter = await self.get_chapter_by_id(chapter_id)
        if not chapter:
            return None
        
        work_id = str(chapter.work_id)
        original_content = chapter.content or ""
        original_version = chapter.version
        original_word_count = chapter.word_count or 0
        history_service = ChapterHistoryService(self.db)
        stat_service = ChapterWordStatService(self.db)
        
        # 更新字段
        update_data = chapter_data.model_dump(exclude_unset=True)
        content_updated = "content" in update_data
        new_content = None

        # 如果更新了内容，重新计算字数（去除HTML标签）
        if content_updated:
            new_content = update_data.pop("content")
            new_content = new_content or ""
            update_data["word_count"] = calculate_word_count(new_content)

        # 协调 status 与 is_published 字段
        if "status" in update_data:
            raw_status = update_data["status"].value if hasattr(update_data["status"], "value") else update_data["status"]
            status_enum = ChapterStatus(raw_status)
            update_data["status"] = status_enum
            update_data["is_published"] = status_enum == ChapterStatus.PUBLISHED
        elif "is_published" in update_data:
            status_enum = ChapterStatus.PUBLISHED if update_data["is_published"] else ChapterStatus.DRAFT
            update_data["status"] = status_enum
        
        for field, value in update_data.items():
            setattr(chapter, field, value)

        # 版本+1，标记修改者
        chapter.version = (chapter.version or 0) + 1
        chapter.last_modified_by = "user"
        
        await self.db.commit()
        await self.db.refresh(chapter)
        if content_updated:
            set_committed_value(chapter, "content", new_content)

        if content_updated:
            try:
                chapter_storage.write_content(
                    str(chapter.work_id), str(chapter.id), new_content
                )
                await self.index_service.upsert_from_content(
                    str(chapter.work_id), str(chapter.id), new_content
                )
            except Exception as exc:
                logger.error(f"[ChapterService] 写入章节文件或索引失败: {exc}")
        
        # 使缓存失效
        await CacheInvalidator.invalidate_chapter(chapter_id, work_id)

        # 记录历史，便于后续增量统计：先保存旧版本，再保存新版本
        try:
            await history_service.save_history(
                chapter_id=str(chapter.id),
                content=original_content,
                version=original_version,
                modified_by="user",
                operation="before_update",
                description="更新前快照"
            )
            await history_service.save_history(
                chapter_id=str(chapter.id),
                content=new_content if content_updated else original_content,
                version=chapter.version,
                modified_by="user",
                operation="update",
                description="自动保存快照"
            )
        except Exception:
            # 不影响主流程
            pass

        # 记录增量（delta = 新旧字数差）
        try:
            new_word_count = chapter.word_count or 0
            delta = new_word_count - original_word_count
            # 获取 edit_event_id（如果前端传递了）
            edit_event_id = getattr(chapter_data, 'edit_event_id', None)
            await stat_service.add_delta(chapter.id, delta, edit_event_id=edit_event_id)
        except Exception as e:
            logger.warning(f"Failed to record word count delta for chapter {chapter.id}: {e}")
            pass
        
        return chapter
    
    async def delete_chapter(self, chapter_id: str) -> bool:
        """删除章节"""
        chapter = await self.get_chapter_by_id(chapter_id)
        if not chapter:
            return False

        work_id = chapter.work_id
        work_id_str = str(work_id)
        order = chapter.order
        
        # 删除章节
        await self.db.delete(chapter)
        
        # 重新排序后续章节
        result = await self.db.execute(
            select(Chapter)
            .where(Chapter.work_id == work_id, Chapter.order > order)
        )
        subsequent_chapters = result.scalars().all()
        
        for ch in subsequent_chapters:
            ch.order -= 1
        
        await self.db.commit()

        try:
            chapter_storage.delete_content(str(work_id), chapter_id)
            await self.index_service.delete_index(chapter_id)
        except Exception as exc:
            logger.warning(f"[ChapterService] 删除章节文件或索引失败: {exc}")
        
        # 使缓存失效
        await CacheInvalidator.invalidate_chapter(chapter_id, work_id_str)
        
        return True
    
    async def reorder_chapters(self, work_id: str, chapter_ids: List[str]) -> bool:
        """重新排序章节"""
        for index, chapter_id in enumerate(chapter_ids):
            chapter = await self.get_chapter_by_id(chapter_id)
            if chapter and chapter.work_id == work_id:
                chapter.order = index + 1

        await self.db.commit()
        return True

    async def update_chapter_with_lock(
        self,
        chapter_id: str,
        chapter_data: ChapterUpdate,
        expected_version: int,
        modifier: str = "user"
    ) -> tuple[Optional[Chapter], str]:
        """
        带乐观锁的章节更新

        Args:
            chapter_id: 章节ID
            chapter_data: 更新数据
            expected_version: 期望的版本号
            modifier: 修改者 ("user" | "agent")

        Returns:
            (chapter, error_message)
            成功时返回 (chapter, "")
            失败时返回 (None, "conflict" | "not_found")
        """
        chapter = await self.get_chapter_by_id(chapter_id)
        if not chapter:
            return (None, "not_found")

        # 检查版本号
        if chapter.version != expected_version:
            return (None, "conflict")

        work_id = str(chapter.work_id)
        original_word_count = chapter.word_count or 0

        # 更新数据
        update_data = chapter_data.model_dump(exclude_unset=True)
        content_updated = "content" in update_data
        new_content = None

        # 如果更新了内容，重新计算字数
        if content_updated:
            new_content = update_data.pop("content")
            new_content = new_content or ""
            update_data["word_count"] = calculate_word_count(new_content)

        # 协调 status 与 is_published 字段
        if "status" in update_data:
            raw_status = update_data["status"].value if hasattr(update_data["status"], "value") else update_data["status"]
            status_enum = ChapterStatus(raw_status)
            update_data["status"] = status_enum
            update_data["is_published"] = status_enum == ChapterStatus.PUBLISHED
        elif "is_published" in update_data:
            status_enum = ChapterStatus.PUBLISHED if update_data["is_published"] else ChapterStatus.DRAFT
            update_data["status"] = status_enum

        # 更新版本号和修改者
        update_data["version"] = chapter.version + 1
        update_data["last_modified_by"] = modifier

        for field, value in update_data.items():
            setattr(chapter, field, value)

        await self.db.commit()
        await self.db.refresh(chapter)
        if content_updated:
            set_committed_value(chapter, "content", new_content)

        if content_updated:
            try:
                chapter_storage.write_content(
                    str(chapter.work_id), str(chapter.id), new_content
                )
                await self.index_service.upsert_from_content(
                    str(chapter.work_id), str(chapter.id), new_content
                )
            except Exception as exc:
                logger.error(f"[ChapterService] 写入章节文件或索引失败: {exc}")

        # 使缓存失效
        await CacheInvalidator.invalidate_chapter(chapter_id, work_id)

        # 记录增量（delta = 新旧字数差）
        try:
            stat_service = ChapterWordStatService(self.db)
            new_word_count = chapter.word_count or 0
            delta = new_word_count - original_word_count
            # 获取 edit_event_id（如果前端传递了）
            edit_event_id = getattr(chapter_data, 'edit_event_id', None)
            await stat_service.add_delta(chapter.id, delta, edit_event_id=edit_event_id)
        except Exception as e:
            logger.warning(f"Failed to record word count delta for chapter {chapter.id}: {e}")
            pass

        return (chapter, "")

    async def apply_agent_edit(
        self,
        chapter_id: str,
        content: str,
        operation: str,
        position: int = None
    ) -> Optional[Chapter]:
        """
        应用Agent编辑操作

        Args:
            chapter_id: 章节ID
            content: 要添加的内容
            operation: 操作类型 ("append" | "replace" | "insert")
            position: 插入位置（仅insert操作需要）

        Returns:
            更新后的章节
        """
        chapter = await self.get_chapter_by_id(chapter_id)
        if not chapter:
            return None

        original_word_count = chapter.word_count or 0

        base_content = chapter.content or ""

        # 根据操作类型构建新内容
        if operation == "append":
            new_content = base_content + content
        elif operation == "replace":
            new_content = content
        elif operation == "insert":
            pos = position if position is not None else len(base_content)
            new_content = base_content[:pos] + content + base_content[pos:]
        else:
            return None

        # 更新章节
        chapter.word_count = calculate_word_count(new_content)
        chapter.version = chapter.version + 1
        chapter.last_modified_by = "agent"

        await self.db.commit()
        await self.db.refresh(chapter)
        set_committed_value(chapter, "content", new_content)

        try:
            chapter_storage.write_content(
                str(chapter.work_id), str(chapter.id), new_content
            )
            await self.index_service.upsert_from_content(
                str(chapter.work_id), str(chapter.id), new_content
            )
        except Exception as exc:
            logger.error(f"[ChapterService] 写入章节文件或索引失败: {exc}")

        # 使缓存失效
        await CacheInvalidator.invalidate_chapter(chapter_id, str(chapter.work_id))

        # 记录增量（delta = 新旧字数差）
        try:
            stat_service = ChapterWordStatService(self.db)
            new_word_count = chapter.word_count or 0
            delta = new_word_count - original_word_count
            # 为 Agent 编辑生成唯一的事件 ID（基于章节 ID + 版本号）
            agent_event_id = f"agent:{chapter_id}:v{chapter.version}"
            await stat_service.add_delta(chapter.id, delta, edit_event_id=agent_event_id)
        except Exception as e:
            logger.warning(f"Failed to record word count delta for chapter {chapter.id}: {e}")
            pass

        return chapter
