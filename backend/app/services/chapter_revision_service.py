from datetime import datetime
from typing import List, Optional, Tuple
import re

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.chapter_revision import ChapterRevision, ChapterRevisionStatus
from app.services.chapter_service import ChapterService
from app.schemas.chapter import ChapterUpdate
from app.services.agent.tools.position_inferrer import position_inferrer
from app.utils.datetime_utils import get_utc_now


class ChapterRevisionService:
    """Service for managing pending chapter revisions."""

    def __init__(self, db: AsyncSession):
        self.db = db

    async def create_revision(
        self,
        *,
        request_id: str,
        work_id: str,
        chapter_id: str,
        user_id: Optional[str],
        operation: str,
        new_text: str,
        original_text: Optional[str] = None,
        position: Optional[dict] = None,
        before_anchor: Optional[str] = None,
        after_anchor: Optional[str] = None,
        node_id: Optional[str] = None,
        paragraph_index: Optional[int] = None,
        base_version: Optional[int] = None,
        description: Optional[str] = None,
    ) -> ChapterRevision:
        revision = ChapterRevision(
            request_id=request_id,
            work_id=work_id,
            chapter_id=chapter_id,
            user_id=user_id,
            status=ChapterRevisionStatus.PENDING,
            operation=operation,
            new_text=new_text,
            original_text=original_text,
            position=position,
            before_anchor=before_anchor,
            after_anchor=after_anchor,
            node_id=node_id,
            paragraph_index=paragraph_index,
            base_version=base_version,
            description=description,
        )
        self.db.add(revision)
        await self.db.commit()
        await self.db.refresh(revision)
        return revision

    async def get_revision_by_request_id(self, request_id: str) -> Optional[ChapterRevision]:
        result = await self.db.execute(
            select(ChapterRevision).where(ChapterRevision.request_id == request_id)
        )
        return result.scalar_one_or_none()

    async def get_pending_revisions_by_chapter(self, chapter_id: str) -> List[ChapterRevision]:
        result = await self.db.execute(
            select(ChapterRevision)
            .where(
                ChapterRevision.chapter_id == chapter_id,
                ChapterRevision.status == ChapterRevisionStatus.PENDING,
            )
            .order_by(ChapterRevision.created_at.asc())
        )
        return list(result.scalars().all())

    async def mark_status(
        self,
        revision: ChapterRevision,
        status: ChapterRevisionStatus,
        applied_at: Optional[datetime] = None,
    ) -> ChapterRevision:
        revision.status = status
        if applied_at is not None:
            revision.applied_at = applied_at
        await self.db.commit()
        await self.db.refresh(revision)
        return revision

    async def apply_revision(
        self,
        revision: ChapterRevision,
    ) -> Tuple[Optional[object], str]:
        chapter_service = ChapterService(self.db)
        chapter = await chapter_service.get_chapter_by_id(str(revision.chapter_id))
        if not chapter:
            return (None, "chapter_not_found")

        if revision.status != ChapterRevisionStatus.PENDING:
            return (chapter, "")

        base_version_mismatch = (
            revision.base_version is not None and chapter.version != revision.base_version
        )

        new_content, error = self._build_new_content(chapter.content or "", revision)
        if error:
            if base_version_mismatch:
                revision.status = ChapterRevisionStatus.CONFLICT
                await self.db.commit()
                return (None, "conflict")
            return (None, error)

        updated, update_error = await chapter_service.update_chapter_with_lock(
            chapter_id=str(chapter.id),
            chapter_data=ChapterUpdate(content=new_content),
            expected_version=chapter.version,
            modifier="agent",
        )
        if update_error:
            if update_error == "conflict":
                revision.status = ChapterRevisionStatus.CONFLICT
                await self.db.commit()
                return (None, "conflict")
            return (None, update_error)

        revision.status = ChapterRevisionStatus.ACCEPTED
        revision.applied_at = get_utc_now()
        await self.db.commit()
        await self.db.refresh(revision)

        return (updated, "")

    def _build_new_content(
        self,
        old_content: str,
        revision: ChapterRevision,
    ) -> Tuple[Optional[str], str]:
        actual_content = revision.new_text or ""
        if not actual_content.strip():
            return (None, "empty_content")

        operation = revision.operation
        position = revision.position
        before_anchor = revision.before_anchor
        after_anchor = revision.after_anchor
        original_text = revision.original_text
        node_id = revision.node_id
        paragraph_index = revision.paragraph_index

        def _replace_by_node_id(raw: str, target_id: str, replacement: str):
            if not target_id:
                return None
            pattern = rf'(<(p|h[1-6]|blockquote|pre)[^>]*\sdata-id=["\']{re.escape(target_id)}["\'][^>]*>)(.*?)(</\2>)'
            match = re.search(pattern, raw, re.DOTALL | re.IGNORECASE)
            if not match:
                return None
            return raw[:match.start(3)] + replacement + raw[match.end(3):]

        def _insert_after_node_id(raw: str, target_id: str, insertion: str):
            if not target_id:
                return None
            pattern = rf'(<(p|h[1-6]|blockquote|pre)[^>]*\sdata-id=["\']{re.escape(target_id)}["\'][^>]*>.*?</\2>)'
            match = re.search(pattern, raw, re.DOTALL | re.IGNORECASE)
            if not match:
                return None
            insert_at = match.end(1)
            return raw[:insert_at] + insertion + raw[insert_at:]

        def _get_paragraph_text(raw: str, idx: int):
            if idx is None or idx < 0:
                return None
            if '<p' in raw:
                pattern = r'<(p|h[1-6]|blockquote|pre)[^>]*>(.*?)</\1>'
                matches = re.findall(pattern, raw, re.DOTALL | re.IGNORECASE)
                if 0 <= idx < len(matches):
                    inner_html = matches[idx][1]
                    text_value = re.sub(r'<[^>]+>', '', inner_html).strip()
                    return text_value or None
                return None
            paragraphs = [p.strip() for p in re.split(r'\n\n+|\n', raw) if p.strip()]
            if 0 <= idx < len(paragraphs):
                return paragraphs[idx]
            return None

        if operation == "append":
            return (old_content + actual_content, "")

        # replace_all: 整体替换章节内容（不需要定位）
        if operation == "replace_all":
            return (actual_content, "")

        if operation == "insert":
            insert_pos = None
            new_content = None
            if isinstance(position, dict):
                insert_pos = position.get("from") or position.get("to")

            if insert_pos is None and node_id:
                inserted = _insert_after_node_id(old_content, node_id, actual_content)
                if inserted is not None:
                    new_content = inserted

            if new_content is None and insert_pos is None and paragraph_index is not None:
                para_text = _get_paragraph_text(old_content, paragraph_index)
                if para_text:
                    idx = old_content.find(para_text)
                    if idx != -1:
                        insert_pos = idx + len(para_text)

            if new_content is None and insert_pos is None and (before_anchor or after_anchor):
                inferred = position_inferrer.find_by_anchors(
                    content=old_content,
                    before_anchor=before_anchor,
                    after_anchor=after_anchor,
                    fallback="end",
                )
                insert_pos = inferred.get("position")

            if new_content is None:
                if insert_pos is None:
                    insert_pos = len(old_content)
                if isinstance(insert_pos, int) and 0 <= insert_pos <= len(old_content):
                    new_content = old_content[:insert_pos] + actual_content + old_content[insert_pos:]

            if new_content is None:
                return (None, "locate_failed")
            return (new_content, "")

        if operation == "replace":
            replaced = None
            if isinstance(position, dict) and "from" in position and "to" in position:
                try:
                    start_pos = int(position.get("from"))
                    end_pos = int(position.get("to"))
                    if 0 <= start_pos <= end_pos <= len(old_content):
                        replaced = old_content[:start_pos] + actual_content + old_content[end_pos:]
                except (TypeError, ValueError):
                    replaced = None
            if replaced is None and node_id:
                replaced = _replace_by_node_id(old_content, node_id, actual_content)
            if replaced is None and original_text:
                if original_text in old_content:
                    replaced = old_content.replace(original_text, actual_content, 1)
            if replaced is None and paragraph_index is not None:
                para_text = _get_paragraph_text(old_content, paragraph_index)
                if para_text and para_text in old_content:
                    replaced = old_content.replace(para_text, actual_content, 1)
            if replaced is None and before_anchor and after_anchor:
                before_idx = old_content.find(before_anchor)
                if before_idx != -1:
                    start_idx = before_idx + len(before_anchor)
                    after_idx = old_content.find(after_anchor, start_idx)
                    if after_idx != -1:
                        replaced = old_content[:start_idx] + actual_content + old_content[after_idx:]

            if replaced is None:
                if not original_text and not before_anchor and not after_anchor and not node_id and paragraph_index is None:
                    replaced = actual_content
                else:
                    return (None, "locate_failed")
            return (replaced, "")

        return (None, "invalid_operation")
