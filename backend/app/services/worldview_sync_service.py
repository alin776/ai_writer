"""
世界观同步服务
提供两种同步模式：
1. 方案A：章节写完后自动提取变化
2. 方案C：批量扫描指定章节范围，生成变化报告
"""
import logging
import json
import re
import asyncio
from typing import List, Dict, Any, Optional, Callable, Awaitable, Tuple
from uuid import UUID
from datetime import datetime, timezone
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.models.chapter import Chapter
from app.models.character import Character
from app.models.location import Location
from app.models.setting import Setting
from app.models.relationship import EntityRelationship
from app.services.worldview_service import WorldviewService
from app.services.ai.http_ai_service import HTTPAIService
from app.services.agent.model_selector import TaskType
from app.core.redis_client import redis_client
from app.schemas.worldview import CharacterCreate, CharacterUpdate, LocationCreate, SettingCreate
from app.services.chapter_content_provider import ChapterContentProvider
from app.utils.text_cleaner import TextCleaner
from app.core.config import settings

logger = logging.getLogger(__name__)


class WorldviewSyncService:
    """世界观同步服务"""

    def __init__(self, db: AsyncSession, user_id: str = None):
        self.db = db
        self.user_id = user_id
        self.worldview_service = WorldviewService(db)
        self.content_provider = ChapterContentProvider()

    async def extract_changes_from_chapter(
        self,
        work_id: str,
        chapter_id: str,
        chapter_content: str
    ) -> Dict[str, Any]:
        """
        方案A：从单个章节提取世界观变化

        Returns:
            {
                "new_characters": [{"name": "王五", "role": "配角", "description": "...", "first_appearance": "第10章"}],
                "updated_characters": [{"name": "李明", "changes": "性格变化：从内向变得开朗"}],
                "new_locations": [{"name": "幽暗森林", "type": "自然", "description": "..."}],
                "new_settings": [{"title": "...", "category": "...", "content": "..."}],
                "relationship_changes": [{"from": "李明", "to": "张三", "old": "朋友", "new": "敌对"}]
            }
        """
        if not chapter_content or len(chapter_content) < 100:
            return self._empty_changes()

        # 获取当前世界观数据
        existing_characters = await self.worldview_service.get_characters_by_work(work_id)
        existing_locations = await self.worldview_service.get_locations_by_work(work_id)
        existing_settings = await self.worldview_service.get_settings_by_work(work_id)

        # 构建现有世界观摘要
        existing_summary = self._build_existing_summary(
            existing_characters, existing_locations, existing_settings
        )

        # 获取章节信息
        chapter_stmt = select(Chapter).where(Chapter.id == chapter_id)
        chapter_result = await self.db.execute(chapter_stmt)
        chapter = chapter_result.scalar_one_or_none()
        chapter_title = chapter.title if chapter else "未知章节"
        chapter_order = chapter.order if chapter else 0

        # 调用 AI 提取变化
        changes = await self._ai_extract_changes(
            chapter_content=chapter_content,
            chapter_title=chapter_title,
            chapter_order=chapter_order,
            existing_summary=existing_summary
        )

        return changes

    async def scan_chapters_for_changes(
        self,
        work_id: str,
        start_chapter: int = 1,
        end_chapter: int = None,
        limit: int = 10,
        status_callback: Optional[Callable[[str], Awaitable[None]]] = None
    ) -> Dict[str, Any]:
        """
        方案C：批量扫描章节，生成世界观变化报告

        Args:
            work_id: 作品ID
            start_chapter: 起始章节号
            end_chapter: 结束章节号（None表示到最新）
            limit: 最多扫描章节数

        Returns:
            {
                "scanned_chapters": 5,
                "new_characters": [...],
                "updated_characters": [...],
                "new_locations": [...],
                "new_settings": [...],
                "relationship_changes": [...]
            }
        """
        chapters = await self.get_chapters_by_range(
            work_id=work_id,
            start_chapter=start_chapter,
            end_chapter=end_chapter,
            limit=limit
        )

        changes, _meta = await self._scan_chapters_batched(
            work_id=work_id,
            chapters=chapters,
            preface_text=None,
            progress_callback=None,
            status_callback=status_callback
        )
        return changes

    async def scan_chapters_for_changes_by_ids(
        self,
        work_id: str,
        chapter_ids: List[str],
        preface_text: Optional[str] = None,
        progress_callback: Optional[Callable[[int, int, int, int], Awaitable[None]]] = None,
        status_callback: Optional[Callable[[str], Awaitable[None]]] = None
    ) -> Tuple[Dict[str, Any], Dict[str, Any]]:
        """按章节ID批量扫描（用于导入解析）"""
        chapters = await self.get_chapters_by_ids(work_id, chapter_ids)
        return await self._scan_chapters_batched(
            work_id=work_id,
            chapters=chapters,
            preface_text=preface_text,
            progress_callback=progress_callback,
            status_callback=status_callback
        )

    async def get_chapters_by_work(self, work_id: str) -> List[Chapter]:
        result = await self.db.execute(
            select(Chapter).where(Chapter.work_id == work_id).order_by(Chapter.order)
        )
        return result.scalars().all()

    async def get_chapters_by_ids(self, work_id: str, chapter_ids: List[str]) -> List[Chapter]:
        if not chapter_ids:
            return []
        result = await self.db.execute(
            select(Chapter).where(
                Chapter.work_id == work_id,
                Chapter.id.in_(chapter_ids)
            ).order_by(Chapter.order)
        )
        return result.scalars().all()

    async def get_chapters_by_range(
        self,
        work_id: str,
        start_chapter: int,
        end_chapter: Optional[int],
        limit: int
    ) -> List[Chapter]:
        stmt = select(Chapter).where(Chapter.work_id == work_id).order_by(Chapter.order)
        if start_chapter:
            stmt = stmt.where(Chapter.order >= start_chapter)
        if end_chapter:
            stmt = stmt.where(Chapter.order <= end_chapter)
        if limit:
            stmt = stmt.limit(limit)
        result = await self.db.execute(stmt)
        return result.scalars().all()

    async def _scan_chapters_batched(
        self,
        work_id: str,
        chapters: List[Chapter],
        preface_text: Optional[str],
        progress_callback: Optional[Callable[[int, int, int, int], Awaitable[None]]],
        status_callback: Optional[Callable[[str], Awaitable[None]]] = None
    ) -> Tuple[Dict[str, Any], Dict[str, Any]]:
        if not chapters and not preface_text:
            return self._empty_changes_with_scan(0), {"batches_total": 0}

        # 获取现有世界观
        existing_characters = await self.worldview_service.get_characters_by_work(work_id)
        existing_locations = await self.worldview_service.get_locations_by_work(work_id)
        existing_settings = await self.worldview_service.get_settings_by_work(work_id)

        existing_summary = self._build_existing_summary(
            existing_characters, existing_locations, existing_settings
        )

        if status_callback:
            await status_callback("preparing")

        total_chapters = len({str(c.id) for c in chapters if c.id})
        processed_ids: set[str] = set()

        merged = self._empty_changes_with_scan(0)
        if progress_callback:
            await progress_callback(len(processed_ids), total_chapters, 0, 0)

        concurrency = max(1, settings.WORLDVIEW_SCAN_CONCURRENCY)
        fast_model = settings.WORLDVIEW_SCAN_FIRST_BATCH_MODEL
        default_model = settings.WORLDVIEW_SCAN_MODEL
        if default_model:
            fast_model = default_model
        shared_ai_service: Optional[HTTPAIService] = None
        shared_fast_ai_service: Optional[HTTPAIService] = None
        if concurrency == 1:
            if default_model:
                shared_ai_service = HTTPAIService(
                    db=self.db,
                    user_id=self.user_id,
                    model=default_model,
                    enable_model_selector=False
                )
            else:
                shared_ai_service = HTTPAIService(
                    db=self.db,
                    user_id=self.user_id,
                    model=settings.OPENAI_MODEL,
                    enable_model_selector=True
                )
            if fast_model and fast_model != default_model:
                shared_fast_ai_service = HTTPAIService(
                    db=self.db,
                    user_id=self.user_id,
                    model=fast_model,
                    enable_model_selector=False
                )

        total_batches = 0
        try:
            if concurrency == 1:
                batches_completed = 0
                started_ai = False
                for idx, batch in enumerate(self._iter_scan_batches(
                    chapters=chapters,
                    preface_text=preface_text,
                    max_chapters_per_batch=settings.WORLDVIEW_SCAN_BATCH_CHAPTERS,
                    max_chars_per_batch=settings.WORLDVIEW_SCAN_BATCH_MAX_CHARS,
                    first_batch_chapters=settings.WORLDVIEW_SCAN_FIRST_BATCH_CHAPTERS,
                    first_batch_max_chars=settings.WORLDVIEW_SCAN_FIRST_BATCH_MAX_CHARS
                )):
                    if status_callback and not started_ai:
                        await status_callback("running")
                        started_ai = True

                    ai_service = shared_ai_service
                    if idx == 0 and fast_model:
                        ai_service = shared_fast_ai_service or shared_ai_service

                    changes = await self._ai_batch_extract_changes(
                        combined_content=batch["combined_content"],
                        existing_summary=existing_summary,
                        chapter_count=batch["chapter_count"],
                        ai_service=ai_service,
                        task_type=TaskType.WORLD_BUILDING
                    )
                    merged = self._merge_changes(merged, changes)
                    processed_ids.update(batch["chapter_ids"])
                    batches_completed += 1
                    if progress_callback:
                        await progress_callback(
                            len(processed_ids),
                            total_chapters,
                            batches_completed,
                            0
                        )
                if progress_callback:
                    await progress_callback(
                        len(processed_ids),
                        total_chapters,
                        batches_completed,
                        batches_completed
                    )
                total_batches = batches_completed
            else:
                batches = self._build_scan_batches(
                    chapters=chapters,
                    preface_text=preface_text,
                    max_chapters_per_batch=settings.WORLDVIEW_SCAN_BATCH_CHAPTERS,
                    max_chars_per_batch=settings.WORLDVIEW_SCAN_BATCH_MAX_CHARS,
                    first_batch_chapters=settings.WORLDVIEW_SCAN_FIRST_BATCH_CHAPTERS,
                    first_batch_max_chars=settings.WORLDVIEW_SCAN_FIRST_BATCH_MAX_CHARS
                )
                total_batches = len(batches)
                if status_callback and total_batches > 0:
                    await status_callback("running")

                # 并发批次：为每个批次创建独立 AI 服务，避免共享 DB 会话并发问题
                sem = asyncio.Semaphore(concurrency)
                completed = 0

                async def worker(batch_idx: int, batch: Dict[str, Any]):
                    async with sem:
                        changes = await self._ai_batch_extract_changes(
                            combined_content=batch["combined_content"],
                            existing_summary=existing_summary,
                            chapter_count=batch["chapter_count"],
                            ai_service=None,
                            task_type=TaskType.WORLD_BUILDING,
                            enable_cost_tracking=False,
                            model_override=fast_model if (batch_idx == 0 and fast_model) else default_model
                        )
                        return batch_idx, batch, changes

                tasks = [worker(idx, batch) for idx, batch in enumerate(batches)]
                for coro in asyncio.as_completed(tasks):
                    batch_idx, batch, changes = await coro
                    merged = self._merge_changes(merged, changes)
                    processed_ids.update(batch["chapter_ids"])
                    completed += 1
                    if progress_callback:
                        await progress_callback(
                            len(processed_ids),
                            total_chapters,
                            completed,
                            total_batches
                        )
        finally:
            if shared_ai_service:
                await shared_ai_service.close()
            if shared_fast_ai_service:
                await shared_fast_ai_service.close()

        merged["scanned_chapters"] = len(chapters)
        return merged, {"batches_total": total_batches, "chapters_total": total_chapters}

    async def apply_changes(
        self,
        work_id: str,
        changes: Dict[str, Any],
        selected_items: Optional[Dict[str, List[str]]] = None
    ) -> Dict[str, int]:
        """
        应用世界观变化到卡片

        Args:
            work_id: 作品ID
            changes: 变化数据
            selected_items: 用户选择要应用的项（None表示全部应用）
                {
                    "new_characters": ["王五", "李四"],
                    "new_locations": ["幽暗森林"],
                    ...
                }

        Returns:
            {"characters_created": 2, "locations_created": 1, ...}
        """
        stats = {
            "characters_created": 0,
            "characters_updated": 0,
            "locations_created": 0,
            "locations_updated": 0,
            "settings_created": 0,
            "settings_updated": 0,
            "relationships_created": 0
        }

        # 应用新人物
        new_characters = changes.get("new_characters", [])
        for char in new_characters:
            if selected_items and char["name"] not in selected_items.get("new_characters", []):
                continue

            # 检查是否已存在
            existing = await self.worldview_service.get_characters_by_work(work_id)
            if any(c.name == char["name"] for c in existing):
                continue

            try:
                await self.worldview_service.create_character(CharacterCreate(
                    work_id=work_id,
                    name=char["name"],
                    role=char.get("role", "配角"),
                    description=char.get("description", ""),
                    tags=char.get("tags", [])
                ))
                stats["characters_created"] += 1
                logger.info(f"[世界观同步] 创建人物: {char['name']}")
            except Exception as e:
                logger.error(f"创建人物失败 {char['name']}: {e}")

        # 应用人物变化（追加式更新）
        updated_characters = changes.get("updated_characters", [])
        if updated_characters:
            existing_characters = await self.worldview_service.get_characters_by_work(work_id)
            char_map = {c.name: c for c in existing_characters}
            for char in updated_characters:
                name = char.get("name")
                changes_text = char.get("changes")
                if not name or not changes_text:
                    continue
                if selected_items and "updated_characters" in selected_items and name not in selected_items.get("updated_characters", []):
                    continue
                target = char_map.get(name)
                if not target:
                    continue
                existing_desc = target.description or ""
                marker = f"更新：{changes_text}"
                if marker in existing_desc:
                    continue
                new_desc = f"{existing_desc}\n{marker}".strip()
                try:
                    await self.worldview_service.update_character(
                        str(target.id),
                        CharacterUpdate(description=new_desc)
                    )
                    stats["characters_updated"] += 1
                    logger.info(f"[世界观同步] 更新人物: {name}")
                except Exception as e:
                    logger.error(f"更新人物失败 {name}: {e}")

        # 应用新地点
        new_locations = changes.get("new_locations", [])
        for loc in new_locations:
            if selected_items and loc["name"] not in selected_items.get("new_locations", []):
                continue

            existing = await self.worldview_service.get_locations_by_work(work_id)
            if any(l.name == loc["name"] for l in existing):
                continue

            try:
                await self.worldview_service.create_location(LocationCreate(
                    work_id=work_id,
                    name=loc["name"],
                    type=loc.get("type", "场景"),
                    description=loc.get("description", ""),
                    tags=loc.get("tags", [])
                ))
                stats["locations_created"] += 1
                logger.info(f"[世界观同步] 创建地点: {loc['name']}")
            except Exception as e:
                logger.error(f"创建地点失败 {loc['name']}: {e}")

        # 应用新设定
        new_settings = changes.get("new_settings", [])
        for setting in new_settings:
            if selected_items and setting["title"] not in selected_items.get("new_settings", []):
                continue

            existing = await self.worldview_service.get_settings_by_work(work_id)
            if any(s.title == setting["title"] for s in existing):
                continue

            try:
                await self.worldview_service.create_setting(SettingCreate(
                    work_id=work_id,
                    title=setting["title"],
                    category=setting.get("category", "剧情设定"),
                    content=setting.get("content", ""),
                    tags=setting.get("tags", [])
                ))
                stats["settings_created"] += 1
                logger.info(f"[世界观同步] 创建设定: {setting['title']}")
            except Exception as e:
                logger.error(f"创建设定失败 {setting['title']}: {e}")

        # 应用关系变化
        relationship_changes = changes.get("relationship_changes", [])
        # 先获取所有人物，构建名称到ID的映射
        all_characters = await self.worldview_service.get_characters_by_work(work_id)
        char_name_to_id = {c.name: str(c.id) for c in all_characters}

        for rel in relationship_changes:
            # 构建关系的唯一标识符
            rel_key = f"{rel.get('from_character') or rel.get('from')}->{rel.get('to_character') or rel.get('to')}"
            if selected_items and rel_key not in selected_items.get("relationship_changes", []):
                continue

            from_name = rel.get("from_character") or rel.get("from")
            to_name = rel.get("to_character") or rel.get("to")

            # 查找对应的人物ID
            from_id = char_name_to_id.get(from_name)
            to_id = char_name_to_id.get(to_name)

            if not from_id or not to_id:
                logger.warning(f"[世界观同步] 无法找到人物ID: {from_name}({from_id}) -> {to_name}({to_id})")
                continue

            try:
                # 检查是否已存在相同的关系
                existing_rel_stmt = select(EntityRelationship).where(
                    EntityRelationship.work_id == work_id,
                    EntityRelationship.source_id == from_id,
                    EntityRelationship.target_id == to_id,
                    EntityRelationship.source_type == "character",
                    EntityRelationship.target_type == "character"
                )
                existing_rel_result = await self.db.execute(existing_rel_stmt)
                existing_rel = existing_rel_result.scalar_one_or_none()

                new_relation = rel.get("new_relation", "相关")
                reason = rel.get("reason", "")

                if existing_rel:
                    # 更新现有关系
                    existing_rel.relationship_type = new_relation
                    existing_rel.label = new_relation
                    if reason:
                        existing_rel.description = f"{existing_rel.description or ''}\n{reason}".strip()
                    logger.info(f"[世界观同步] 更新关系: {from_name} -> {to_name}: {new_relation}")
                else:
                    # 创建新关系
                    now = datetime.now(timezone.utc)
                    new_relationship = EntityRelationship(
                        work_id=work_id,
                        source_id=from_id,
                        source_type="character",
                        target_id=to_id,
                        target_type="character",
                        relationship_type=new_relation,
                        label=new_relation,
                        description=reason or None,
                        strength=5,
                        direction="one-way",
                        created_at=now,
                        updated_at=now
                    )
                    self.db.add(new_relationship)
                    stats["relationships_created"] += 1
                    logger.info(f"[世界观同步] 创建关系: {from_name} -> {to_name}: {new_relation}")
            except Exception as e:
                logger.error(f"创建/更新关系失败 {from_name} -> {to_name}: {e}")

        await self.db.commit()
        self._invalidate_worldview_cache(
            work_id,
            ['characters', 'locations', 'settings', 'guidelines']
        )
        return stats

    def _iter_scan_batches(
        self,
        chapters: List[Chapter],
        preface_text: Optional[str],
        max_chapters_per_batch: int,
        max_chars_per_batch: int,
        first_batch_chapters: Optional[int] = None,
        first_batch_max_chars: Optional[int] = None
    ):
        """迭代构建分批扫描内容（不截断，超长章节拆分）"""
        current_blocks: List[str] = []
        current_len = 0
        current_ids: List[str] = []
        batches_emitted = 0
        def emit():
            nonlocal current_blocks, current_len, current_ids, batches_emitted
            if not current_blocks:
                return None
            batch = {
                "combined_content": "\n\n".join(current_blocks),
                "chapter_count": len({cid for cid in current_ids}),
                "chapter_ids": list({cid for cid in current_ids})
            }
            current_blocks = []
            current_len = 0
            current_ids = []
            batches_emitted += 1
            return batch

        # 前言/设定段落只放入首个批次
        if preface_text:
            preface_clean = TextCleaner.html_to_clean_text(preface_text, preserve_structure=True)
            if preface_clean:
                block = f"【前言/设定】\n{preface_clean}"
                current_blocks.append(block)
                current_len += len(block)

        for chapter in chapters:
            content = self.content_provider.read_content(str(chapter.work_id), str(chapter.id)) or ""
            if not content:
                continue
            clean_content = TextCleaner.html_to_clean_text(content, preserve_structure=True)
            if not clean_content:
                continue

            parts = []
            if max_chars_per_batch and len(clean_content) > max_chars_per_batch:
                # 超长章节拆分为多个片段
                for idx in range(0, len(clean_content), max_chars_per_batch):
                    parts.append(clean_content[idx:idx + max_chars_per_batch])
            else:
                parts = [clean_content]

            for part_idx, part in enumerate(parts):
                suffix = f"（片段{part_idx + 1}/{len(parts)}）" if len(parts) > 1 else ""
                block = f"【第{chapter.order}章 {chapter.title}{suffix}】\n{part}"

                current_max_chapters = max_chapters_per_batch
                current_max_chars = max_chars_per_batch
                if batches_emitted == 0 and first_batch_chapters:
                    current_max_chapters = first_batch_chapters
                    if first_batch_max_chars:
                        current_max_chars = first_batch_max_chars

                if current_blocks and (
                    (current_max_chapters and len({cid for cid in current_ids}) >= current_max_chapters) or
                    (current_max_chars and current_len + len(block) > current_max_chars)
                ):
                    batch = emit()
                    if batch:
                        yield batch

                current_blocks.append(block)
                current_len += len(block)
                if chapter.id:
                    current_ids.append(str(chapter.id))

        batch = emit()
        if batch:
            yield batch

    def _build_scan_batches(
        self,
        chapters: List[Chapter],
        preface_text: Optional[str],
        max_chapters_per_batch: int,
        max_chars_per_batch: int,
        first_batch_chapters: Optional[int] = None,
        first_batch_max_chars: Optional[int] = None
    ) -> List[Dict[str, Any]]:
        """构建分批扫描内容（不截断，超长章节拆分）"""
        return list(self._iter_scan_batches(
            chapters=chapters,
            preface_text=preface_text,
            max_chapters_per_batch=max_chapters_per_batch,
            max_chars_per_batch=max_chars_per_batch,
            first_batch_chapters=first_batch_chapters,
            first_batch_max_chars=first_batch_max_chars
        ))

    def _merge_changes(self, base: Dict[str, Any], incoming: Dict[str, Any]) -> Dict[str, Any]:
        """合并多批次的世界观变化结果"""
        merged = {
            "new_characters": [],
            "updated_characters": [],
            "new_locations": [],
            "new_settings": [],
            "relationship_changes": [],
            "scanned_chapters": base.get("scanned_chapters", 0)
        }

        def importance_rank(value: Optional[str]) -> int:
            mapping = {"高": 3, "中": 2, "低": 1}
            return mapping.get(value or "", 0)

        def merge_entity(existing: Dict[str, Any], new: Dict[str, Any], text_field: str) -> Dict[str, Any]:
            if new.get(text_field) and (not existing.get(text_field) or len(new.get(text_field, "")) > len(existing.get(text_field, ""))):
                existing[text_field] = new.get(text_field)
            for field in ["role", "type", "category", "first_appearance"]:
                if field in new and new.get(field) and not existing.get(field):
                    existing[field] = new.get(field)
            if "importance" in new and importance_rank(new.get("importance")) > importance_rank(existing.get("importance")):
                existing["importance"] = new.get("importance")
            if "tags" in new and new.get("tags"):
                existing_tags = set(existing.get("tags") or [])
                existing["tags"] = list(existing_tags.union(set(new.get("tags") or [])))
            return existing

        def merge_list(field: str, key_field: str, text_field: str):
            items = {}
            for item in base.get(field, []):
                items[item.get(key_field)] = dict(item)
            for item in incoming.get(field, []):
                key = item.get(key_field)
                if not key:
                    continue
                if key in items:
                    items[key] = merge_entity(items[key], item, text_field)
                else:
                    items[key] = dict(item)
            merged[field] = list(items.values())

        merge_list("new_characters", "name", "description")
        merge_list("new_locations", "name", "description")
        merge_list("new_settings", "title", "content")

        # 更新人物变化合并
        updated_map = {}
        for item in base.get("updated_characters", []):
            updated_map[item.get("name")] = item.get("changes", "")
        for item in incoming.get("updated_characters", []):
            name = item.get("name")
            changes = item.get("changes")
            if not name or not changes:
                continue
            if name in updated_map and changes not in updated_map[name]:
                updated_map[name] = f"{updated_map[name]}\n{changes}".strip()
            else:
                updated_map[name] = changes
        merged["updated_characters"] = [{"name": name, "changes": changes} for name, changes in updated_map.items()]

        # 关系变化合并
        rel_map = {}
        for item in base.get("relationship_changes", []):
            key = f"{item.get('from_character') or item.get('from')}->{item.get('to_character') or item.get('to')}"
            rel_map[key] = dict(item)
        for item in incoming.get("relationship_changes", []):
            key = f"{item.get('from_character') or item.get('from')}->{item.get('to_character') or item.get('to')}"
            if key in rel_map:
                rel_map[key].update(item)
            else:
                rel_map[key] = dict(item)
        merged["relationship_changes"] = list(rel_map.values())

        return merged

    def _empty_changes_with_scan(self, scanned: int) -> Dict[str, Any]:
        return {
            "new_characters": [],
            "updated_characters": [],
            "new_locations": [],
            "new_settings": [],
            "relationship_changes": [],
            "scanned_chapters": scanned
        }

    def _invalidate_worldview_cache(self, work_id: str, cache_types: Optional[List[str]] = None) -> None:
        """Invalidate worldview-related cache entries after background sync."""
        if not redis_client.is_available():
            return

        types = cache_types or ['characters', 'locations', 'settings', 'guidelines']
        for cache_type in types:
            cache_key = f"worldview:{cache_type}:{work_id}"
            try:
                redis_client.client.delete(cache_key)
                logger.info(f"[Worldview Sync] Cache invalidated: {cache_key}")
            except Exception as e:
                logger.error(f"[Worldview Sync] Cache invalidation failed: {cache_key}, error={e}")

        if any(cache_type in {'characters', 'locations', 'settings', 'guidelines'} for cache_type in types):
            worlddata_key = f"worldview:worlddata:{work_id}"
            try:
                redis_client.client.delete(worlddata_key)
                logger.info(f"[Worldview Sync] Cache invalidated: {worlddata_key}")
            except Exception as e:
                logger.error(f"[Worldview Sync] Cache invalidation failed: {worlddata_key}, error={e}")

    def _build_existing_summary(
        self,
        characters: List[Character],
        locations: List[Location],
        settings: List[Setting]
    ) -> str:
        """构建现有世界观摘要"""
        parts = []

        if characters:
            char_names = [f"{c.name}({c.role or '角色'})" for c in characters]
            parts.append(f"【已有人物】{', '.join(char_names)}")

        if locations:
            loc_names = [f"{l.name}({l.type or '地点'})" for l in locations]
            parts.append(f"【已有地点】{', '.join(loc_names)}")

        if settings:
            setting_titles = [f"{s.title}({s.category or '设定'})" for s in settings]
            parts.append(f"【已有设定】{', '.join(setting_titles)}")

        return "\n".join(parts) if parts else "（暂无世界观数据）"

    async def _ai_extract_changes(
        self,
        chapter_content: str,
        chapter_title: str,
        chapter_order: int,
        existing_summary: str
    ) -> Dict[str, Any]:
        """调用 AI 从单章提取变化"""
        prompt = f"""你是一个专业的小说世界观分析师。请分析以下章节内容，找出与现有世界观相比的**新增和变化**。

【现有世界观】
{existing_summary}

【待分析章节】第{chapter_order}章 {chapter_title}
{chapter_content[:15000]}

【任务要求】
请识别出：
1. 新出现的人物（不在现有人物列表中的）
2. 新出现的地点（不在现有地点列表中的）
3. 新的设定/规则（不在现有设定中的）
4. 人物关系的变化

请以JSON格式返回，格式如下：
{{
  "new_characters": [
    {{"name": "人物名", "role": "主角/配角/反派/路人", "description": "简要描述（50字内）", "first_appearance": "第X章"}}
  ],
  "updated_characters": [
    {{"name": "已有人物名", "changes": "具体变化描述"}}
  ],
  "new_locations": [
    {{"name": "地点名", "type": "城市/建筑/自然/其他", "description": "简要描述（50字内）"}}
  ],
  "new_settings": [
    {{"title": "设定名称", "category": "力量体系/世界规则/剧情设定", "content": "设定内容（100字内）"}}
  ],
  "relationship_changes": [
    {{"from": "人物A", "to": "人物B", "old_relation": "原关系", "new_relation": "新关系", "reason": "变化原因"}}
  ]
}}

【重要提醒】
1. 只提取**新增或变化**的内容，已存在的不要重复
2. 人物名要准确，不要提取"路人"、"某人"等泛称
3. 如果没有发现变化，对应数组返回空 []
4. 返回严格的JSON格式"""

        try:
            # 统一使用快模型进行世界观分析
            ai_service = HTTPAIService(
                db=self.db,
                user_id=self.user_id,
                model=settings.WORLDVIEW_SINGLE_CHAPTER_MODEL or "gemini-2.5-flash",
                enable_model_selector=False
            )
            full_response = ""

            async for chunk, usage in ai_service._stream_chat(
                messages=[
                    {"role": "system", "content": "你是专业的小说世界观分析师，擅长识别故事中的人物、地点和设定变化。请以JSON格式返回分析结果。"},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=2000,
                temperature=0.3,
                task_type=TaskType.WORLD_BUILDING
            ):
                if chunk:  # 忽略空chunk（最后一个是空的，只包含usage）
                    full_response += chunk

            # 解析 JSON
            return self._parse_changes_json(full_response)

        except Exception as e:
            logger.error(f"AI提取世界观变化失败: {e}")
            return self._empty_changes()

    async def _ai_batch_extract_changes(
        self,
        combined_content: str,
        existing_summary: str,
        chapter_count: int,
        ai_service: Optional[HTTPAIService] = None,
        task_type: Optional[TaskType] = None,
        enable_cost_tracking: bool = True,
        model_override: Optional[str] = None
    ) -> Dict[str, Any]:
        """调用 AI 批量提取变化"""
        prompt = f"""你是一个专业的小说世界观分析师。请分析以下{chapter_count}个章节的内容，找出与现有世界观相比的**所有新增和变化**。

【现有世界观】
{existing_summary}

【待分析内容】
{combined_content}

【任务要求】
请综合分析所有章节，识别出：
1. 新出现的人物（不在现有人物列表中的）- 合并多次出现的同一人物
2. 新出现的地点（不在现有地点列表中的）
3. 新的设定/规则
4. 人物关系的重要变化

请以JSON格式返回：
{{
  "new_characters": [
    {{"name": "人物名", "role": "主角/配角/反派", "description": "综合描述（100字内）", "first_appearance": "首次出现章节", "importance": "高/中/低"}}
  ],
  "updated_characters": [
    {{"name": "已有人物名", "changes": "主要变化描述"}}
  ],
  "new_locations": [
    {{"name": "地点名", "type": "类型", "description": "描述（50字内）", "importance": "高/中/低"}}
  ],
  "new_settings": [
    {{"title": "设定名称", "category": "分类", "content": "内容（100字内）"}}
  ],
  "relationship_changes": [
    {{"from": "人物A", "to": "人物B", "old_relation": "原关系", "new_relation": "新关系"}}
  ]
}}

【重要提醒】
1. 合并重复的实体，不要多次列出同一人物/地点
2. 按重要性排序，重要的放前面
3. 人物名要准确，过滤掉"路人甲"等无意义名称
4. 返回严格的JSON格式"""

        created_service = False
        try:
            logger.debug(f"[世界观同步] 开始AI分析，章节数: {chapter_count}, 内容长度: {len(combined_content)}")
            logger.debug(f"[世界观同步] 现有世界观: {existing_summary[:200]}...")
            logger.debug(f"[世界观同步] db={self.db}, user_id={self.user_id}")

            # 使用 gemini 模型进行世界观分析（更稳定）
            if ai_service is None:
                if model_override:
                    ai_service = HTTPAIService(
                        db=self.db if enable_cost_tracking else None,
                        user_id=self.user_id if enable_cost_tracking else None,
                        model=model_override,
                        enable_model_selector=False,
                        enable_cost_tracking=enable_cost_tracking
                    )
                else:
                    ai_service = HTTPAIService(
                        db=self.db if enable_cost_tracking else None,
                        user_id=self.user_id if enable_cost_tracking else None,
                        model=settings.OPENAI_MODEL,
                        enable_model_selector=True,
                        enable_cost_tracking=enable_cost_tracking
                    )
                created_service = True
            if created_service:
                logger.info(f"[世界观同步] AI服务初始化完成: api_key={'***' + ai_service.api_key[-4:] if ai_service.api_key else 'None'}, base_url={ai_service.base_url}, model={ai_service.model}")
            full_response = ""

            async for chunk, usage in ai_service._stream_chat(
                messages=[
                    {"role": "system", "content": "你是专业的小说世界观分析师。请综合分析多个章节，提取世界观变化，以JSON格式返回。"},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=3000,
                temperature=0.3,
                task_type=task_type
            ):
                if chunk:  # 忽略空chunk（最后一个是空的，只包含usage）
                    full_response += chunk

            logger.debug(f"[世界观同步] AI响应长度: {len(full_response)}")
            logger.debug(f"[世界观同步] AI响应内容: {full_response[:500]}...")

            result = self._parse_changes_json(full_response)
            logger.info(f"[世界观同步] 解析结果: 新人物={len(result.get('new_characters', []))}, 新地点={len(result.get('new_locations', []))}, 新设定={len(result.get('new_settings', []))}")

            return result

        except Exception as e:
            logger.error(f"AI批量提取世界观变化失败: {e}", exc_info=True)
            return self._empty_changes()
        finally:
            if created_service and ai_service:
                await ai_service.close()

    def _parse_changes_json(self, response: str) -> Dict[str, Any]:
        """解析 AI 返回的 JSON"""
        try:
            # 查找 JSON
            json_start = response.find('{')
            json_end = response.rfind('}') + 1

            if json_start >= 0 and json_end > json_start:
                json_str = response[json_start:json_end]
                data = json.loads(json_str)

                # 确保所有必需的键存在
                return {
                    "new_characters": data.get("new_characters", []),
                    "updated_characters": data.get("updated_characters", []),
                    "new_locations": data.get("new_locations", []),
                    "new_settings": data.get("new_settings", []),
                    "relationship_changes": data.get("relationship_changes", [])
                }

        except json.JSONDecodeError as e:
            logger.error(f"JSON解析失败: {e}")

        return self._empty_changes()

    def _empty_changes(self) -> Dict[str, Any]:
        """返回空的变化结构"""
        return {
            "new_characters": [],
            "updated_characters": [],
            "new_locations": [],
            "new_settings": [],
            "relationship_changes": []
        }
