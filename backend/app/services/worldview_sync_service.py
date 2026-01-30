"""
世界观同步服务
提供两种同步模式：
1. 方案A：章节写完后自动提取变化
2. 方案C：批量扫描指定章节范围，生成变化报告
"""
import logging
import json
import re
from typing import List, Dict, Any, Optional
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
from app.core.redis_client import redis_client
from app.schemas.worldview import CharacterCreate, LocationCreate, SettingCreate
from app.services.chapter_content_provider import ChapterContentProvider

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
        limit: int = 10
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
        # 获取章节列表
        stmt = select(Chapter).where(
            Chapter.work_id == work_id
        ).order_by(Chapter.order)

        if start_chapter:
            stmt = stmt.where(Chapter.order >= start_chapter)
        if end_chapter:
            stmt = stmt.where(Chapter.order <= end_chapter)

        stmt = stmt.limit(limit)

        result = await self.db.execute(stmt)
        chapters = result.scalars().all()

        if not chapters:
            return {
                "scanned_chapters": 0,
                "new_characters": [],
                "updated_characters": [],
                "new_locations": [],
                "new_settings": [],
                "relationship_changes": []
            }

        # 合并所有章节内容
        combined_content = ""
        for chapter in chapters:
            content = self.content_provider.read_content(str(chapter.work_id), str(chapter.id)) or ""
            logger.debug(f"[世界观同步] 章节 {chapter.order} '{chapter.title}': 内容长度={len(content)}")
            if content:
                combined_content += f"\n\n【第{chapter.order}章 {chapter.title}】\n{content}"

        logger.debug(f"[世界观同步] 合并 {len(chapters)} 个章节，总内容长度: {len(combined_content)}")
        logger.debug(f"[世界观同步] 内容预览: {combined_content[:500]}...")

        # 如果没有内容，返回空结果
        if len(combined_content) < 100:
            logger.warning(f"[世界观同步] 章节内容过少 ({len(combined_content)} 字符)，无法分析")
            return {
                "scanned_chapters": len(chapters),
                "new_characters": [],
                "updated_characters": [],
                "new_locations": [],
                "new_settings": [],
                "relationship_changes": []
            }

        # 限制内容长度
        if len(combined_content) > 50000:
            combined_content = combined_content[:50000] + "\n...[内容截断]"

        # 获取现有世界观
        existing_characters = await self.worldview_service.get_characters_by_work(work_id)
        existing_locations = await self.worldview_service.get_locations_by_work(work_id)
        existing_settings = await self.worldview_service.get_settings_by_work(work_id)

        existing_summary = self._build_existing_summary(
            existing_characters, existing_locations, existing_settings
        )

        # AI 批量提取
        changes = await self._ai_batch_extract_changes(
            combined_content=combined_content,
            existing_summary=existing_summary,
            chapter_count=len(chapters)
        )

        changes["scanned_chapters"] = len(chapters)
        return changes

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
            "settings_created": 0,
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
            # 使用 gemini 模型进行世界观分析（更稳定）
            ai_service = HTTPAIService(db=self.db, user_id=self.user_id, model="gemini-2.5-pro")
            full_response = ""

            async for chunk, usage in ai_service._stream_chat(
                messages=[
                    {"role": "system", "content": "你是专业的小说世界观分析师，擅长识别故事中的人物、地点和设定变化。请以JSON格式返回分析结果。"},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=2000,
                temperature=0.3
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
        chapter_count: int
    ) -> Dict[str, Any]:
        """调用 AI 批量提取变化"""
        prompt = f"""你是一个专业的小说世界观分析师。请分析以下{chapter_count}个章节的内容，找出与现有世界观相比的**所有新增和变化**。

【现有世界观】
{existing_summary}

【待分析内容】
{combined_content[:40000]}

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

        try:
            logger.debug(f"[世界观同步] 开始AI分析，章节数: {chapter_count}, 内容长度: {len(combined_content)}")
            logger.debug(f"[世界观同步] 现有世界观: {existing_summary[:200]}...")
            logger.debug(f"[世界观同步] db={self.db}, user_id={self.user_id}")

            # 使用 gemini 模型进行世界观分析（更稳定）
            ai_service = HTTPAIService(db=self.db, user_id=self.user_id, model="gemini-2.5-pro")
            logger.info(f"[世界观同步] AI服务初始化完成: api_key={'***' + ai_service.api_key[-4:] if ai_service.api_key else 'None'}, base_url={ai_service.base_url}, model={ai_service.model}")
            full_response = ""

            async for chunk, usage in ai_service._stream_chat(
                messages=[
                    {"role": "system", "content": "你是专业的小说世界观分析师。请综合分析多个章节，提取世界观变化，以JSON格式返回。"},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=3000,
                temperature=0.3
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
