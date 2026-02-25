"""
Bridge service between worldview cards and knowledge markdown files.

Rules:
- Worldview cards (DB) are the single source of truth.
- knowledge/characters.md and knowledge/worldview.md are auto-generated mirrors.
- When those markdown files are edited (manually or by AI), we parse and upsert
  into cards, then regenerate the mirror files to keep format stable.
"""

from __future__ import annotations

import logging
import re
from pathlib import Path
from typing import Any, Optional

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.character import Character
from app.models.location import Location
from app.models.setting import Setting
from app.models.work import Work
from app.services.agent.deep_agent import DATA_ROOT

logger = logging.getLogger(__name__)


def _normalize_path(path: str) -> str:
    normalized = (path or "").replace("\\", "/").strip()
    if normalized.startswith("./"):
        normalized = normalized[2:]
    if normalized.startswith("/"):
        normalized = normalized[1:]
    return normalized.lower()


def _normalize_key(value: str) -> str:
    return re.sub(r"\s+", "", (value or "").strip()).lower()


def _split_tags(value: str) -> list[str]:
    if not value:
        return []
    items = re.split(r"[、,，;/；\s]+", value.strip())
    return [item.strip() for item in items if item.strip()]


def _join_lines(existing: Optional[str], line: str) -> str:
    cleaned = (line or "").strip()
    if not cleaned:
        return existing or ""
    if existing:
        return f"{existing}\n{cleaned}"
    return cleaned


def _flatten_text(value: Optional[str]) -> str:
    if not value:
        return ""
    return re.sub(r"\s*\n+\s*", " / ", value.strip())


def _normalize_character_role(value: Optional[str]) -> Optional[str]:
    if value is None:
        return None
    text = str(value).strip().replace("\\*", "*")
    if not text:
        return None
    text = re.sub(
        r"^(?:[-*]\s*)?(?:角色|role|定位)\s*[:：]\s*",
        "",
        text,
        flags=re.IGNORECASE,
    ).strip()
    return text or None


def _normalize_character_description(
    value: Optional[str],
    role: Optional[str] = None,
) -> tuple[str, Optional[str]]:
    """Normalize noisy character descriptions parsed from markdown lists."""
    text = (value or "").strip().replace("\\*", "*")
    inferred_role = _normalize_character_role(role)
    if not text:
        return "", inferred_role

    text = re.sub(r"\s*\n+\s*", " / ", text)

    role_desc_re = re.compile(
        r"^(?:[-*]\s*)?(?:角色|role|定位)\s*[:：]\s*(.*?)\s*/\s*"
        r"(?:[-*]\s*)?(?:描述|简介|description|content)\s*[:：]\s*(.+)$",
        flags=re.IGNORECASE,
    )
    for _ in range(10):
        match = role_desc_re.match(text)
        if not match:
            break
        extracted_role = _normalize_character_role(match.group(1))
        if not inferred_role and extracted_role:
            inferred_role = extracted_role
        text = match.group(2).strip()

    text = re.sub(
        r"^(?:[-*]\s*)?(?:描述|简介|description|content)\s*[:：]\s*",
        "",
        text,
        flags=re.IGNORECASE,
    ).strip()
    return text, inferred_role


def _safe_tags(value: Any) -> list[str]:
    if not value:
        return []
    if isinstance(value, list):
        result: list[str] = []
        for item in value:
            text = str(item).strip()
            if text:
                result.append(text)
        return result
    if isinstance(value, str):
        return _split_tags(value)
    text = str(value).strip()
    return [text] if text else []


class WorldviewKnowledgeBridge:
    """Synchronize worldview cards with mirrored knowledge markdown files."""

    TRACKED_PATHS = {
        "knowledge/characters.md",
        "knowledge/worldview.md",
        "characters.md",
        "worldview.md",
    }

    @classmethod
    def is_tracked_path(cls, path: str) -> bool:
        return _normalize_path(path) in cls.TRACKED_PATHS

    @classmethod
    def has_tracked_path(cls, paths: list[str] | None) -> bool:
        if not paths:
            return False
        return any(cls.is_tracked_path(path) for path in paths)

    def __init__(self, db: AsyncSession):
        self.db = db

    async def mirror_from_cards(self, work_id: str, work_dir: Optional[Path] = None) -> dict[str, Any]:
        """Generate or overwrite mirrored knowledge markdown files from cards."""
        resolved_work_dir = await self._resolve_work_dir(work_id, work_dir)
        if not resolved_work_dir:
            return {"updated_files": []}

        characters = (
            await self.db.execute(
                select(Character)
                .where(Character.work_id == work_id)
                .order_by(Character.name.asc(), Character.created_at.asc())
            )
        ).scalars().all()

        locations = (
            await self.db.execute(
                select(Location)
                .where(Location.work_id == work_id)
                .order_by(Location.name.asc(), Location.created_at.asc())
            )
        ).scalars().all()

        settings = (
            await self.db.execute(
                select(Setting)
                .where(Setting.work_id == work_id)
                .order_by(Setting.title.asc(), Setting.created_at.asc())
            )
        ).scalars().all()

        mirrors = {
            "knowledge/characters.md": self._render_characters_markdown(characters),
            "knowledge/worldview.md": self._render_worldview_markdown(locations, settings),
        }

        updated_files: list[str] = []
        for rel_path, content in mirrors.items():
            target = resolved_work_dir / rel_path
            target.parent.mkdir(parents=True, exist_ok=True)

            previous = target.read_text(encoding="utf-8") if target.exists() else None
            if previous != content:
                target.write_text(content, encoding="utf-8")
                updated_files.append(rel_path)

        return {
            "updated_files": updated_files,
            "characters_count": len(characters),
            "locations_count": len(locations),
            "settings_count": len(settings),
        }

    async def sync_cards_from_knowledge(
        self,
        work_id: str,
        *,
        touched_paths: Optional[list[str]] = None,
        work_dir: Optional[Path] = None,
    ) -> dict[str, Any]:
        """
        Parse tracked knowledge markdown files and upsert card data.

        Notes:
        - Upsert by natural key (name/title).
        - No auto-delete for missing markdown entries.
        """
        resolved_work_dir = await self._resolve_work_dir(work_id, work_dir)
        if not resolved_work_dir:
            return {"created": {}, "updated": {}, "mirrored_files": []}

        touched = {_normalize_path(path) for path in (touched_paths or [])}
        touched_has_data = bool(touched)

        sync_characters = (not touched_has_data) or bool(
            touched & {"knowledge/characters.md", "characters.md"}
        )
        sync_worldview = (not touched_has_data) or bool(
            touched & {"knowledge/worldview.md", "worldview.md"}
        )

        created = {"characters": 0, "locations": 0, "settings": 0}
        updated = {"characters": 0, "locations": 0, "settings": 0}

        if sync_characters:
            characters_path = self._pick_existing_path(
                resolved_work_dir,
                "knowledge/characters.md",
                "characters.md",
            )
            if characters_path and characters_path.exists():
                parsed_characters = self._parse_characters_markdown(characters_path.read_text(encoding="utf-8"))
                c_created, c_updated = await self._upsert_characters(work_id, parsed_characters)
                created["characters"] += c_created
                updated["characters"] += c_updated

        if sync_worldview:
            worldview_path = self._pick_existing_path(
                resolved_work_dir,
                "knowledge/worldview.md",
                "worldview.md",
            )
            if worldview_path and worldview_path.exists():
                parsed_worldview = self._parse_worldview_markdown(worldview_path.read_text(encoding="utf-8"))
                l_created, l_updated = await self._upsert_locations(work_id, parsed_worldview["locations"])
                s_created, s_updated = await self._upsert_settings(work_id, parsed_worldview["settings"])
                created["locations"] += l_created
                updated["locations"] += l_updated
                created["settings"] += s_created
                updated["settings"] += s_updated

        has_db_changes = any(value > 0 for value in created.values()) or any(value > 0 for value in updated.values())
        if has_db_changes:
            await self.db.commit()
            self._invalidate_worldview_cache(work_id)

        mirror_result = {"updated_files": []}
        # Keep markdown format stable after markdown-driven edits.
        if sync_characters or sync_worldview:
            mirror_result = await self.mirror_from_cards(work_id, work_dir=resolved_work_dir)

        return {
            "created": created,
            "updated": updated,
            "mirrored_files": mirror_result.get("updated_files", []),
            "has_db_changes": has_db_changes,
        }

    async def _resolve_work_dir(self, work_id: str, fallback: Optional[Path]) -> Optional[Path]:
        if fallback:
            return fallback

        result = await self.db.execute(
            select(Work).where(Work.id == work_id)
        )
        work = result.scalar_one_or_none()
        if not work:
            logger.warning("[WorldviewKnowledgeBridge] work not found while resolving dir: %s", work_id)
            return None
        return DATA_ROOT / str(work.author_id) / "works" / str(work.id)

    @staticmethod
    def _pick_existing_path(work_dir: Path, preferred_rel: str, legacy_rel: str) -> Optional[Path]:
        preferred = work_dir / preferred_rel
        if preferred.exists():
            return preferred
        legacy = work_dir / legacy_rel
        if legacy.exists():
            return legacy
        return preferred

    @staticmethod
    def _render_characters_markdown(characters: list[Character]) -> str:
        lines = [
            "# 人物设定",
            "",
            "> 本文件由世界观卡片自动生成。建议优先在世界观卡片中编辑。",
            "",
        ]

        if not characters:
            lines.extend(["（暂无人物卡片）", ""])
            return "\n".join(lines).rstrip() + "\n"

        for character in characters:
            role = _normalize_character_role(character.role)
            description, inferred_role = _normalize_character_description(character.description, role)
            final_role = role or inferred_role

            lines.append(f"## {character.name}")
            if final_role:
                lines.append(f"- 角色：{final_role}")
            lines.append(f"- 描述：{_flatten_text(description) or '待补充'}")
            tags = _safe_tags(character.tags)
            if tags:
                lines.append(f"- 标签：{'、'.join(tags)}")
            lines.append("")

        return "\n".join(lines).rstrip() + "\n"

    @staticmethod
    def _render_worldview_markdown(locations: list[Location], settings: list[Setting]) -> str:
        lines = [
            "# 世界观设定",
            "",
            "> 本文件由世界观卡片自动生成。建议优先在世界观卡片中编辑。",
            "",
            "## 地点",
            "",
        ]

        if locations:
            for location in locations:
                lines.append(f"### {location.name}")
                if location.type:
                    lines.append(f"- 类型：{location.type}")
                lines.append(f"- 描述：{_flatten_text(location.description) or '待补充'}")
                tags = _safe_tags(location.tags)
                if tags:
                    lines.append(f"- 标签：{'、'.join(tags)}")
                lines.append("")
        else:
            lines.extend(["（暂无地点卡片）", ""])

        lines.extend(["## 设定", ""])
        if settings:
            for setting in settings:
                lines.append(f"### {setting.title}")
                if setting.category:
                    lines.append(f"- 分类：{setting.category}")
                if setting.content:
                    lines.append(f"- 内容：{_flatten_text(setting.content)}")
                else:
                    lines.append("- 内容：")
                tags = _safe_tags(setting.tags)
                if tags:
                    lines.append(f"- 标签：{'、'.join(tags)}")
                lines.append("")
        else:
            lines.extend(["（暂无设定卡片）", ""])

        return "\n".join(lines).rstrip() + "\n"

    @staticmethod
    def _parse_characters_markdown(text: str) -> list[dict[str, Any]]:
        entries: list[dict[str, Any]] = []
        current: Optional[dict[str, Any]] = None
        last_field: Optional[str] = None

        heading_re = re.compile(r"^\s*(#{1,6})\s+(.+?)\s*$")
        kv_re = re.compile(r"^\s*[-*]\s*([^:：]+)\s*[:：]\s*(.*)\s*$")

        for raw_line in text.splitlines():
            line = raw_line.rstrip("\r\n")
            heading_match = heading_re.match(line)
            if heading_match:
                level = len(heading_match.group(1))
                title = heading_match.group(2).strip()
                if level == 2:
                    if current and current.get("name"):
                        entries.append(current)
                    current = {"name": title}
                last_field = None
                continue

            if current is None:
                continue

            kv_match = kv_re.match(line)
            if kv_match:
                key = kv_match.group(1).strip().lower()
                value = kv_match.group(2).strip()
                if key in {"角色", "role", "定位"}:
                    current["role"] = _normalize_character_role(value)
                    last_field = None
                elif key in {"描述", "简介", "description"}:
                    desc, inferred_role = _normalize_character_description(value, current.get("role"))
                    current["description"] = desc
                    if inferred_role and not current.get("role"):
                        current["role"] = inferred_role
                    last_field = "description"
                elif key in {"标签", "tags"}:
                    current["tags"] = _split_tags(value)
                    last_field = None
                else:
                    current["description"] = _join_lines(current.get("description"), f"{kv_match.group(1).strip()}：{value}")
                    last_field = "description"
                continue

            stripped = line.strip()
            if not stripped:
                last_field = None
                continue

            if line.startswith("  ") or line.startswith("\t"):
                if last_field == "description":
                    current["description"] = _join_lines(current.get("description"), stripped)
                continue

            current["description"] = _join_lines(current.get("description"), stripped)
            last_field = "description"

        if current and current.get("name"):
            entries.append(current)

        return entries

    @staticmethod
    def _parse_worldview_markdown(text: str) -> dict[str, list[dict[str, Any]]]:
        locations: list[dict[str, Any]] = []
        settings: list[dict[str, Any]] = []

        section = "settings"
        section_default_category: Optional[str] = None
        current_item: Optional[dict[str, Any]] = None
        current_kind: Optional[str] = None
        last_field: Optional[str] = None

        heading_re = re.compile(r"^\s*(#{1,6})\s+(.+?)\s*$")
        kv_re = re.compile(r"^\s*[-*]\s*([^:：]+)\s*[:：]\s*(.*)\s*$")

        def flush_current() -> None:
            nonlocal current_item, current_kind
            if not current_item:
                return
            if current_kind == "location" and current_item.get("name"):
                locations.append(current_item)
            if current_kind == "setting" and current_item.get("title"):
                settings.append(current_item)
            current_item = None
            current_kind = None

        for raw_line in text.splitlines():
            line = raw_line.rstrip("\r\n")

            heading_match = heading_re.match(line)
            if heading_match:
                level = len(heading_match.group(1))
                title = heading_match.group(2).strip()

                if level == 2:
                    flush_current()
                    section, section_default_category = WorldviewKnowledgeBridge._classify_worldview_section(title)
                    last_field = None
                    continue

                if level == 3:
                    flush_current()
                    if section == "locations":
                        current_item = {"name": title}
                        current_kind = "location"
                    else:
                        current_item = {"title": title}
                        if section_default_category:
                            current_item["category"] = section_default_category
                        current_kind = "setting"
                    last_field = None
                    continue

                last_field = None
                continue

            if current_item is None:
                continue

            kv_match = kv_re.match(line)
            if kv_match:
                key = kv_match.group(1).strip().lower()
                value = kv_match.group(2).strip()
                if current_kind == "location":
                    if key in {"类型", "type"}:
                        current_item["type"] = value or None
                        last_field = None
                    elif key in {"描述", "简介", "description"}:
                        current_item["description"] = value or ""
                        last_field = "description"
                    elif key in {"标签", "tags"}:
                        current_item["tags"] = _split_tags(value)
                        last_field = None
                    else:
                        current_item["description"] = _join_lines(
                            current_item.get("description"),
                            f"{kv_match.group(1).strip()}：{value}",
                        )
                        last_field = "description"
                elif current_kind == "setting":
                    if key in {"分类", "category"}:
                        current_item["category"] = value or None
                        last_field = None
                    elif key in {"内容", "描述", "content", "description"}:
                        current_item["content"] = value or ""
                        last_field = "content"
                    elif key in {"标签", "tags"}:
                        current_item["tags"] = _split_tags(value)
                        last_field = None
                    else:
                        current_item["content"] = _join_lines(
                            current_item.get("content"),
                            f"{kv_match.group(1).strip()}：{value}",
                        )
                        last_field = "content"
                continue

            stripped = line.strip()
            if not stripped:
                last_field = None
                continue

            if line.startswith("  ") or line.startswith("\t"):
                if last_field == "description":
                    current_item["description"] = _join_lines(current_item.get("description"), stripped)
                elif last_field == "content":
                    current_item["content"] = _join_lines(current_item.get("content"), stripped)
                continue

            if current_kind == "location":
                current_item["description"] = _join_lines(current_item.get("description"), stripped)
                last_field = "description"
            elif current_kind == "setting":
                current_item["content"] = _join_lines(current_item.get("content"), stripped)
                last_field = "content"

        flush_current()
        return {"locations": locations, "settings": settings}

    @staticmethod
    def _classify_worldview_section(section_title: str) -> tuple[str, Optional[str]]:
        title = (section_title or "").strip()
        lowered = title.lower()

        if any(token in title for token in ("地点", "地理", "场景")) or any(
            token in lowered for token in ("location", "locations", "place", "places")
        ):
            return "locations", None

        generic_setting_titles = {"设定", "setting", "settings"}
        if lowered in generic_setting_titles:
            return "settings", None

        # Unknown sections are treated as setting categories (e.g. "物品", "势力").
        return "settings", title or None

    async def _upsert_characters(self, work_id: str, items: list[dict[str, Any]]) -> tuple[int, int]:
        existing = (
            await self.db.execute(select(Character).where(Character.work_id == work_id))
        ).scalars().all()
        existing_map = {_normalize_key(row.name): row for row in existing}

        created = 0
        updated = 0
        seen: set[str] = set()

        for item in items:
            name = (item.get("name") or "").strip()
            if not name:
                continue
            key = _normalize_key(name)
            if key in seen:
                continue
            seen.add(key)

            desc, inferred_role = _normalize_character_description(item.get("description"), item.get("role"))
            if "role" in item:
                role = _normalize_character_role(item.get("role"))
            else:
                role = inferred_role
            has_role_update = ("role" in item) or (inferred_role is not None)

            if key in existing_map:
                target = existing_map[key]
                changed = False

                if "description" in item or desc:
                    if desc and target.description != desc:
                        target.description = desc
                        changed = True
                if has_role_update:
                    if target.role != role:
                        target.role = role
                        changed = True
                if "tags" in item:
                    tags = _safe_tags(item.get("tags"))
                    if _safe_tags(target.tags) != tags:
                        target.tags = tags
                        changed = True

                if changed:
                    updated += 1
                continue

            character = Character(
                work_id=work_id,
                name=name,
                description=(desc or "待补充"),
                role=role,
                tags=_safe_tags(item.get("tags")) if "tags" in item else [],
            )
            self.db.add(character)
            created += 1

        return created, updated

    async def _upsert_locations(self, work_id: str, items: list[dict[str, Any]]) -> tuple[int, int]:
        existing = (
            await self.db.execute(select(Location).where(Location.work_id == work_id))
        ).scalars().all()
        existing_map = {_normalize_key(row.name): row for row in existing}

        created = 0
        updated = 0
        seen: set[str] = set()

        for item in items:
            name = (item.get("name") or "").strip()
            if not name:
                continue
            key = _normalize_key(name)
            if key in seen:
                continue
            seen.add(key)

            if key in existing_map:
                target = existing_map[key]
                changed = False

                if "description" in item:
                    desc = (item.get("description") or "").strip()
                    if desc and target.description != desc:
                        target.description = desc
                        changed = True
                if "type" in item:
                    location_type = (item.get("type") or "").strip() or None
                    if target.type != location_type:
                        target.type = location_type
                        changed = True
                if "tags" in item:
                    tags = _safe_tags(item.get("tags"))
                    if _safe_tags(target.tags) != tags:
                        target.tags = tags
                        changed = True

                if changed:
                    updated += 1
                continue

            location = Location(
                work_id=work_id,
                name=name,
                description=((item.get("description") or "").strip() or "待补充"),
                type=((item.get("type") or "").strip() or None) if "type" in item else None,
                tags=_safe_tags(item.get("tags")) if "tags" in item else [],
            )
            self.db.add(location)
            created += 1

        return created, updated

    async def _upsert_settings(self, work_id: str, items: list[dict[str, Any]]) -> tuple[int, int]:
        existing = (
            await self.db.execute(select(Setting).where(Setting.work_id == work_id))
        ).scalars().all()
        existing_map = {_normalize_key(row.title): row for row in existing}

        created = 0
        updated = 0
        seen: set[str] = set()

        for item in items:
            title = (item.get("title") or "").strip()
            if not title:
                continue
            key = _normalize_key(title)
            if key in seen:
                continue
            seen.add(key)

            if key in existing_map:
                target = existing_map[key]
                changed = False

                if "content" in item:
                    content = (item.get("content") or "").strip() or None
                    if target.content != content:
                        target.content = content
                        changed = True
                if "category" in item:
                    category = (item.get("category") or "").strip() or None
                    if target.category != category:
                        target.category = category
                        changed = True
                if "tags" in item:
                    tags = _safe_tags(item.get("tags"))
                    if _safe_tags(target.tags) != tags:
                        target.tags = tags
                        changed = True

                if changed:
                    updated += 1
                continue

            setting = Setting(
                work_id=work_id,
                title=title,
                content=((item.get("content") or "").strip() or None),
                category=((item.get("category") or "").strip() or None) if "category" in item else None,
                tags=_safe_tags(item.get("tags")) if "tags" in item else [],
            )
            self.db.add(setting)
            created += 1

        return created, updated

    @staticmethod
    def _invalidate_worldview_cache(work_id: str) -> None:
        if not work_id:
            return
        try:
            from app.services.agent.utils.tool_cache import ToolCache

            ToolCache.invalidate(work_id=str(work_id), include_work_scope=True)
        except Exception as exc:
            logger.debug("[WorldviewKnowledgeBridge] cache invalidation skipped: %s", exc)
