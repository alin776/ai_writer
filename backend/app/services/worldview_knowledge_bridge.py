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


def _append_meta(item: dict[str, Any], key: str, value: str) -> None:
    """Keep unknown markdown keys in structured meta instead of polluting正文."""
    field = (key or "").strip()
    if not field:
        return
    text = (value or "").strip()
    meta = item.setdefault("meta", {})
    existing = meta.get(field)
    if existing is None:
        meta[field] = text
        return
    if isinstance(existing, list):
        if text and text not in existing:
            existing.append(text)
        return
    if text and text != existing:
        meta[field] = [existing, text]


def _normalize_heading(value: str) -> str:
    return re.sub(r"\s+", "", (value or "").strip()).lower()


def _is_characters_root_heading(value: str) -> bool:
    normalized = _normalize_heading(value)
    return normalized in {
        "人物设定",
        "人物",
        "角色设定",
        "角色",
        "character",
        "characters",
    }


def _is_probable_character_group_heading(value: str) -> bool:
    normalized = _normalize_heading(value)
    if not normalized:
        return False
    if normalized in {"主角", "配角", "反派", "次要角色", "其他人物", "人物关系"}:
        return True
    return normalized.endswith(("组", "阵营", "派系", "清单", "列表", "group", "team", "faction"))


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
        sync_mode: str = "upsert",
    ) -> dict[str, Any]:
        """
        Parse tracked knowledge markdown files and upsert card data.

        Notes:
        - Upsert by natural key (name/title).
        - Optional strict mode can delete DB rows missing in markdown.
        """
        resolved_work_dir = await self._resolve_work_dir(work_id, work_dir)
        if not resolved_work_dir:
            return {"created": {}, "updated": {}, "deleted": {}, "mirrored_files": []}

        mode = self._normalize_sync_mode(sync_mode)
        strict_mode = mode == "strict"

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
        deleted = {"characters": 0, "locations": 0, "settings": 0}

        if sync_characters:
            characters_path = self._pick_existing_path(
                resolved_work_dir,
                "knowledge/characters.md",
                "characters.md",
            )
            if characters_path and characters_path.exists():
                raw_text = characters_path.read_text(encoding="utf-8")
                parsed_characters = self._parse_characters_markdown(raw_text)
                c_created, c_updated = await self._upsert_characters(work_id, parsed_characters)
                created["characters"] += c_created
                updated["characters"] += c_updated
                if strict_mode:
                    deleted["characters"] += await self._delete_missing_characters(work_id, parsed_characters)

        if sync_worldview:
            worldview_path = self._pick_existing_path(
                resolved_work_dir,
                "knowledge/worldview.md",
                "worldview.md",
            )
            if worldview_path and worldview_path.exists():
                raw_text = worldview_path.read_text(encoding="utf-8")
                parsed_worldview = self._parse_worldview_markdown(raw_text)
                l_created, l_updated = await self._upsert_locations(work_id, parsed_worldview["locations"])
                s_created, s_updated = await self._upsert_settings(work_id, parsed_worldview["settings"])
                created["locations"] += l_created
                updated["locations"] += l_updated
                created["settings"] += s_created
                updated["settings"] += s_updated
                if strict_mode:
                    deleted["locations"] += await self._delete_missing_locations(work_id, parsed_worldview["locations"])
                    deleted["settings"] += await self._delete_missing_settings(work_id, parsed_worldview["settings"])

        has_db_changes = (
            any(value > 0 for value in created.values())
            or any(value > 0 for value in updated.values())
            or any(value > 0 for value in deleted.values())
        )
        if has_db_changes:
            await self.db.commit()
            self._invalidate_worldview_cache(work_id)

        mirror_result = {"updated_files": []}
        # Only rewrite markdown when DB actually changed, avoid overriding user formatting on no-op edits.
        if has_db_changes and (sync_characters or sync_worldview):
            mirror_result = await self.mirror_from_cards(work_id, work_dir=resolved_work_dir)

        return {
            "created": created,
            "updated": updated,
            "deleted": deleted,
            "mirrored_files": mirror_result.get("updated_files", []),
            "has_db_changes": has_db_changes,
            "sync_mode": mode,
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
    def _normalize_sync_mode(sync_mode: Optional[str]) -> str:
        mode = (sync_mode or "upsert").strip().lower()
        if mode not in {"upsert", "strict"}:
            logger.warning("[WorldviewKnowledgeBridge] unknown sync_mode=%s, fallback to upsert", sync_mode)
            return "upsert"
        return mode

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
        pending_h2_title: Optional[str] = None
        current_group: Optional[str] = None

        heading_re = re.compile(r"^\s*(#{1,6})\s+(.+?)\s*$")
        kv_re = re.compile(r"^\s*[-*]\s*([^:：]+)\s*[:：]\s*(.*)\s*$")

        def flush_current() -> None:
            nonlocal current
            if current and current.get("name"):
                entries.append(current)
            current = None

        for raw_line in text.splitlines():
            line = raw_line.rstrip("\r\n")
            heading_match = heading_re.match(line)
            if heading_match:
                level = len(heading_match.group(1))
                title = heading_match.group(2).strip()
                if level == 2:
                    flush_current()
                    pending_h2_title = title
                    current_group = None
                    last_field = None
                    continue
                if level == 3:
                    flush_current()
                    if pending_h2_title and not _is_characters_root_heading(pending_h2_title):
                        current_group = pending_h2_title
                    else:
                        current_group = None
                    pending_h2_title = None
                    current = {"name": title}
                    if current_group:
                        current["group"] = current_group
                last_field = None
                continue

            if current is None:
                stripped = line.strip()
                if not stripped:
                    continue
                if pending_h2_title and not _is_probable_character_group_heading(pending_h2_title):
                    current = {"name": pending_h2_title}
                    pending_h2_title = None
                else:
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
                    _append_meta(current, kv_match.group(1), value)
                    last_field = None
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

        flush_current()

        return entries

    @staticmethod
    def _parse_worldview_markdown(text: str) -> dict[str, list[dict[str, Any]]]:
        locations: list[dict[str, Any]] = []
        settings: list[dict[str, Any]] = []

        section = "ignore"
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
                    elif section == "settings":
                        current_item = {"title": title}
                        if section_default_category:
                            current_item["category"] = section_default_category
                        current_kind = "setting"
                    else:
                        current_item = None
                        current_kind = None
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
                        _append_meta(current_item, kv_match.group(1), value)
                        last_field = None
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
                        _append_meta(current_item, kv_match.group(1), value)
                        last_field = None
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

        explicit_prefixes = ("设定:", "setting:", "category:")
        for prefix in explicit_prefixes:
            if lowered.startswith(prefix):
                category = title.split(":", 1)[1].strip() if ":" in title else ""
                return "settings", category or None

        known_setting_categories = {
            "物品", "势力", "组织", "种族", "历史", "规则", "力量体系", "文化", "宗教", "科技", "经济", "政治",
            "items", "item", "factions", "faction", "rules", "rule", "culture", "religion", "technology",
        }
        if lowered in known_setting_categories:
            return "settings", title

        # Unknown section headers are ignored to avoid accidental upsert from notes/reference blocks.
        return "ignore", None

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

    async def _delete_missing_characters(self, work_id: str, items: list[dict[str, Any]]) -> int:
        keep = {_normalize_key((item.get("name") or "").strip()) for item in items if (item.get("name") or "").strip()}
        if not keep:
            logger.debug("[WorldviewKnowledgeBridge] strict delete skipped for characters: parsed list empty")
            return 0
        existing = (
            await self.db.execute(select(Character).where(Character.work_id == work_id))
        ).scalars().all()
        deleted = 0
        for row in existing:
            if _normalize_key(row.name) not in keep:
                await self.db.delete(row)
                deleted += 1
        return deleted

    async def _delete_missing_locations(self, work_id: str, items: list[dict[str, Any]]) -> int:
        keep = {_normalize_key((item.get("name") or "").strip()) for item in items if (item.get("name") or "").strip()}
        if not keep:
            logger.debug("[WorldviewKnowledgeBridge] strict delete skipped for locations: parsed list empty")
            return 0
        existing = (
            await self.db.execute(select(Location).where(Location.work_id == work_id))
        ).scalars().all()
        deleted = 0
        for row in existing:
            if _normalize_key(row.name) not in keep:
                await self.db.delete(row)
                deleted += 1
        return deleted

    async def _delete_missing_settings(self, work_id: str, items: list[dict[str, Any]]) -> int:
        keep = {_normalize_key((item.get("title") or "").strip()) for item in items if (item.get("title") or "").strip()}
        if not keep:
            logger.debug("[WorldviewKnowledgeBridge] strict delete skipped for settings: parsed list empty")
            return 0
        existing = (
            await self.db.execute(select(Setting).where(Setting.work_id == work_id))
        ).scalars().all()
        deleted = 0
        for row in existing:
            if _normalize_key(row.title) not in keep:
                await self.db.delete(row)
                deleted += 1
        return deleted

    @staticmethod
    def _invalidate_worldview_cache(work_id: str) -> None:
        if not work_id:
            return
        try:
            from app.services.agent.utils.tool_cache import ToolCache

            ToolCache.invalidate(work_id=str(work_id), include_work_scope=True)
        except Exception as exc:
            logger.debug("[WorldviewKnowledgeBridge] cache invalidation skipped: %s", exc)
