"""
章节历史记录服务 - 自动备份和版本恢复
"""
from typing import List, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.orm.attributes import set_committed_value
from uuid import UUID
import re

from app.models.chapter_history import ChapterHistory
from app.models.chapter import Chapter
from app.schemas.chapter import ChapterUpdate
from app.utils.chapter_file_storage import chapter_storage
from app.services.chapter_content_provider import ChapterContentProvider
from app.services.chapter_content_index_service import ChapterContentIndexService


def calculate_word_count(content: str) -> int:
    """计算文本字数（去除HTML标签）"""
    if not content:
        return 0

    # 移除HTML标签
    text = re.sub(r'<[^>]+>', '', content)
    text = re.sub(r'\s+', ' ', text).strip()

    # 中文字符 + 英文单词 + 数字
    chinese_chars = len(re.findall(r'[\u4e00-\u9fff]', text))
    english_words = len(re.findall(r'[a-zA-Z]+', text))
    digits = len(re.findall(r'[0-9]', text))

    return chinese_chars + english_words + digits


class ChapterHistoryService:
    """章节历史记录服务"""

    def __init__(self, db: AsyncSession):
        self.db = db

    async def save_history(
        self,
        chapter_id: str,
        content: str,
        version: int,
        modified_by: str,
        operation: str = None,
        description: str = None
    ) -> ChapterHistory:
        """
        保存章节历史版本

        Args:
            chapter_id: 章节ID
            content: 内容快照
            version: 版本号
            modified_by: 修改者 ("user" | "agent")
            operation: 操作类型 ("append" | "replace" | "insert" | "manual")
            description: 操作描述
        """
        history = ChapterHistory(
            chapter_id=UUID(chapter_id) if isinstance(chapter_id, str) else chapter_id,
            content=content,
            word_count=calculate_word_count(content),
            version=version,
            modified_by=modified_by,
            operation=operation,
            description=description
        )
        self.db.add(history)
        await self.db.commit()
        await self.db.refresh(history)
        return history

    async def get_histories(
        self,
        chapter_id: str,
        limit: int = 20
    ) -> List[ChapterHistory]:
        """获取章节历史记录"""
        chapter_uuid = UUID(chapter_id) if isinstance(chapter_id, str) else chapter_id

        result = await self.db.execute(
            select(ChapterHistory)
            .where(ChapterHistory.chapter_id == chapter_uuid)
            .order_by(ChapterHistory.created_at.desc())
            .limit(limit)
        )
        return list(result.scalars().all())

    async def get_history_by_id(self, history_id: str) -> Optional[ChapterHistory]:
        """根据ID获取历史记录"""
        history_uuid = UUID(history_id) if isinstance(history_id, str) else history_id
        result = await self.db.execute(
            select(ChapterHistory).where(ChapterHistory.id == history_uuid)
        )
        return result.scalar_one_or_none()

    async def restore_version(
        self,
        chapter_id: str,
        history_id: str
    ) -> Optional[Chapter]:
        """
        恢复到指定历史版本

        Args:
            chapter_id: 章节ID
            history_id: 历史记录ID

        Returns:
            恢复后的章节对象，如果失败返回None
        """
        history = await self.get_history_by_id(history_id)
        if not history or str(history.chapter_id) != chapter_id:
            return None

        # 获取章节
        chapter_uuid = UUID(chapter_id) if isinstance(chapter_id, str) else chapter_id
        result = await self.db.execute(
            select(Chapter).where(Chapter.id == chapter_uuid)
        )
        chapter = result.scalar_one_or_none()

        if not chapter:
            return None

        content_provider = ChapterContentProvider()
        current_content = content_provider.read_content(str(chapter.work_id), str(chapter.id)) or ""

        # 保存当前内容到历史（作为恢复前的备份）
        await self.save_history(
            chapter_id=chapter_id,
            content=current_content,
            version=chapter.version,
            modified_by="user",
            operation="restore",
            description=f"恢复前备份 (将恢复到版本 {history.version})"
        )

        restored_content = history.content or ""

        # 更新章节内容元数据（内容本体写入文件）
        chapter.word_count = history.word_count
        chapter.version = chapter.version + 1
        chapter.last_modified_by = "user"

        await self.db.commit()
        await self.db.refresh(chapter)
        set_committed_value(chapter, "content", restored_content)

        try:
            chapter_storage.write_content(
                str(chapter.work_id), str(chapter.id), restored_content
            )
            index_service = ChapterContentIndexService(self.db)
            await index_service.upsert_from_content(
                str(chapter.work_id), str(chapter.id), restored_content
            )
        except Exception:
            # 不阻断恢复流程
            pass

        try:
            from app.services.agent.utils.explore_cache import invalidate_explore_result_cache
            await invalidate_explore_result_cache(str(chapter.work_id))
        except Exception:
            pass

        return chapter

    async def get_latest_agent_edit(self, chapter_id: str) -> Optional[ChapterHistory]:
        """获取最近一次Agent编辑的历史记录"""
        chapter_uuid = UUID(chapter_id) if isinstance(chapter_id, str) else chapter_id

        result = await self.db.execute(
            select(ChapterHistory)
            .where(
                ChapterHistory.chapter_id == chapter_uuid,
                ChapterHistory.modified_by == "agent"
            )
            .order_by(ChapterHistory.created_at.desc())
            .limit(1)
        )
        return result.scalar_one_or_none()

    async def cleanup_old_histories(
        self,
        chapter_id: str,
        keep_count: int = 50
    ) -> int:
        """
        清理旧的历史记录，只保留最近的N条

        Returns:
            删除的记录数
        """
        chapter_uuid = UUID(chapter_id) if isinstance(chapter_id, str) else chapter_id

        # 获取所有历史记录ID
        result = await self.db.execute(
            select(ChapterHistory.id)
            .where(ChapterHistory.chapter_id == chapter_uuid)
            .order_by(ChapterHistory.created_at.desc())
        )
        all_ids = [row[0] for row in result.all()]

        # 删除超出保留数量的记录
        if len(all_ids) > keep_count:
            ids_to_delete = all_ids[keep_count:]
            for history_id in ids_to_delete:
                result = await self.db.execute(
                    select(ChapterHistory).where(ChapterHistory.id == history_id)
                )
                history = result.scalar_one_or_none()
                if history:
                    await self.db.delete(history)

            await self.db.commit()
            return len(ids_to_delete)

        return 0
