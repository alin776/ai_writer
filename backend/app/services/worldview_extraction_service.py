"""
世界观提取服务
从小说分析结果中自动提取角色、地点和设定信息
支持配置化批次大小、自动重试和进度持久化
"""
import logging
import re
import asyncio
import json
from typing import List, Dict, Any, Optional, Set, Tuple
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.novel_analysis import NovelAnalysis, AnalysisStatus
from app.services.worldview_service import WorldviewService
from app.services.worldview_progress_service import WorldviewProgressService
from app.schemas.worldview import (
    CharacterCreate, LocationCreate, SettingCreate,
    CharacterUpdate, LocationUpdate, SettingUpdate
)
from app.core.config import settings

logger = logging.getLogger(__name__)


class WorldviewExtractionService:
    """世界观提取服务"""

    def __init__(self, db: AsyncSession):
        self.db = db
        self.worldview_service = WorldviewService(db)
        self.progress_service = WorldviewProgressService(db)

    async def extract_from_analysis(
        self,
        work_id: str,
        analysis: NovelAnalysis,
        options: Optional[Dict[str, bool]] = None,
        resume: bool = False
    ) -> Dict[str, Any]:
        """
        从小说分析结果中提取并创建/更新世界观数据

        Args:
            work_id: 作品ID
            analysis: 小说分析对象
            options: 提取选项，例如 {"characters": True, "locations": True, "settings": True}
            resume: 是否从中断处恢复

        Returns:
            Dict[str, Any]: 提取结果统计
                {
                    "characters": {"created": 5, "updated": 2},
                    "locations": {"created": 3, "updated": 1},
                    "settings": {"created": 4, "updated": 0}
                }
        """
        if not analysis or analysis.status != AnalysisStatus.COMPLETED:
            raise ValueError("分析未完成，无法提取数据")

        # 默认全部提取
        if options is None:
            options = {"characters": True, "locations": True, "settings": True}

        result = {
            "characters": {"created": 0, "updated": 0},
            "locations": {"created": 0, "updated": 0},
            "settings": {"created": 0, "updated": 0}
        }

        logger.info(f"开始从分析结果提取世界观数据，work_id={work_id}, resume={resume}")

        try:
            # 1. 从微观分析提取实体
            entities = self._extract_entities_from_micro(analysis.micro_results)
            logger.info(f"从微观分析提取到 {len(entities['characters'])} 个角色, "
                       f"{len(entities['locations'])} 个地点, "
                       f"{len(entities['other'])} 个其他实体")

            # 2. 从宏观分析提取结构化信息
            macro_data = self._extract_from_macro(analysis.macro_results)
            logger.info(f"从宏观分析提取到补充信息")

            # 3. 合并微观和宏观数据
            merged_data = self._merge_entity_data(entities, macro_data)

            # 4. 初始化或恢复进度
            if resume and settings.WORLDVIEW_ENABLE_PROGRESS_PERSISTENCE:
                resume_point = await self.progress_service.get_resume_point(work_id)
                if resume_point:
                    logger.info(f"从恢复点继续处理: {resume_point}")
                    result = resume_point.get("results", result)
                else:
                    logger.info("未找到有效的恢复点，从头开始处理")
                    resume = False

            if not resume or not settings.WORLDVIEW_ENABLE_PROGRESS_PERSISTENCE:
                # 创建新的进度记录
                await self.progress_service.create_progress(
                    work_id=work_id,
                    characters_total=len(merged_data['characters']),
                    locations_total=len(merged_data['locations']),
                    settings_total=len(merged_data['settings']),
                    metadata={"analysis_id": str(analysis.id), "options": options}
                )

                await self.progress_service.update_totals(
                    work_id=work_id,
                    characters_total=len(merged_data['characters']),
                    locations_total=len(merged_data['locations']),
                    settings_total=len(merged_data['settings'])
                )

            # 5. 处理角色 - 使用优化的分批处理和重试机制
            if options.get("characters", True) and merged_data['characters']:
                char_stats = await self._upsert_characters_with_retry(
                    work_id, merged_data['characters'], resume
                )
                result["characters"] = char_stats
                logger.info(f"角色处理完成: 创建 {char_stats['created']}, 更新 {char_stats['updated']}")

            # 6. 处理地点 - 使用优化的分批处理和重试机制
            if options.get("locations", True) and merged_data['locations']:
                loc_stats = await self._upsert_locations_with_retry(
                    work_id, merged_data['locations'], resume
                )
                result["locations"] = loc_stats
                logger.info(f"地点处理完成: 创建 {loc_stats['created']}, 更新 {loc_stats['updated']}")

            # 7. 处理设定 - 使用优化的分批处理和重试机制
            if options.get("settings", True) and merged_data['settings']:
                set_stats = await self._upsert_settings_with_retry(
                    work_id, merged_data['settings'], resume
                )
                result["settings"] = set_stats
                logger.info(f"设定处理完成: 创建 {set_stats['created']}, 更新 {set_stats['updated']}")

            # 8. 标记完成
            if settings.WORLDVIEW_ENABLE_PROGRESS_PERSISTENCE:
                await self.progress_service.mark_completed(work_id)

            logger.info(f"世界观提取完成: {result}")
            return result

        except Exception as e:
            logger.error(f"世界观提取过程中出错: {e}", exc_info=True)

            # 记录错误到进度
            if settings.WORLDVIEW_ENABLE_PROGRESS_PERSISTENCE:
                await self.progress_service.mark_failed(work_id, str(e))

            # 确保数据库连接正确关闭
            try:
                await self.db.rollback()
            except Exception as rollback_error:
                logger.error(f"回滚失败: {rollback_error}")
            raise

    # ==================== 带重试机制的安全处理方法 ====================

    async def _upsert_characters_with_retry(
        self,
        work_id: str,
        characters_data: List[Dict[str, str]],
        resume: bool = False
    ) -> Dict[str, int]:
        """带重试机制的角色批量处理"""
        created = 0
        updated = 0

        # 使用配置化的批次大小
        batch_size = settings.WORLDVIEW_CHARACTER_BATCH_SIZE
        total_batches = (len(characters_data) + batch_size - 1) // batch_size

        # 获取恢复点
        start_batch = 0
        if resume:
            resume_point = await self.progress_service.get_resume_point(work_id)
            if resume_point:
                start_batch = resume_point["characters"]["next_batch"]
                created = resume_point["results"]["characters"]["created"]
                updated = resume_point["results"]["characters"]["updated"]

        logger.info(f"开始分批处理 {len(characters_data)} 个角色，批次大小: {batch_size}, 从批次 {start_batch} 开始")

        for batch_idx in range(start_batch, total_batches):
            start_idx = batch_idx * batch_size
            end_idx = min(start_idx + batch_size, len(characters_data))
            batch = characters_data[start_idx:end_idx]

            # 重试处理当前批次
            batch_result = await self._process_batch_with_retry(
                work_id=work_id,
                batch=batch,
                batch_idx=batch_idx,
                phase="characters",
                processor=self._process_character_batch
            )

            if batch_result:
                created += batch_result["created"]
                updated += batch_result["updated"]

                # 更新进度
                processed_count = min((batch_idx + 1) * batch_size, len(characters_data))
                await self.progress_service.update_phase_progress(
                    work_id=work_id,
                    phase="characters",
                    processed_count=processed_count,
                    batch_index=batch_idx,
                    total_batches=total_batches,
                    results=batch_result
                )

                # 定期保存进度
                if settings.WORLDVIEW_ENABLE_PROGRESS_PERSISTENCE and \
                   (batch_idx + 1) % settings.WORLDVIEW_PROGRESS_SAVE_INTERVAL == 0:
                    logger.info(f"定期保存进度: 已完成 {batch_idx + 1}/{total_batches} 批次")

        return {"created": created, "updated": updated}

    async def _upsert_locations_with_retry(
        self,
        work_id: str,
        locations_data: List[Dict[str, str]],
        resume: bool = False
    ) -> Dict[str, int]:
        """带重试机制的地点批量处理"""
        created = 0
        updated = 0

        batch_size = settings.WORLDVIEW_LOCATION_BATCH_SIZE
        total_batches = (len(locations_data) + batch_size - 1) // batch_size

        # 获取恢复点
        start_batch = 0
        if resume:
            resume_point = await self.progress_service.get_resume_point(work_id)
            if resume_point:
                start_batch = resume_point["locations"]["next_batch"]
                created = resume_point["results"]["locations"]["created"]
                updated = resume_point["results"]["locations"]["updated"]

        logger.info(f"开始分批处理 {len(locations_data)} 个地点，批次大小: {batch_size}, 从批次 {start_batch} 开始")

        for batch_idx in range(start_batch, total_batches):
            start_idx = batch_idx * batch_size
            end_idx = min(start_idx + batch_size, len(locations_data))
            batch = locations_data[start_idx:end_idx]

            batch_result = await self._process_batch_with_retry(
                work_id=work_id,
                batch=batch,
                batch_idx=batch_idx,
                phase="locations",
                processor=self._process_location_batch
            )

            if batch_result:
                created += batch_result["created"]
                updated += batch_result["updated"]

                processed_count = min((batch_idx + 1) * batch_size, len(locations_data))
                await self.progress_service.update_phase_progress(
                    work_id=work_id,
                    phase="locations",
                    processed_count=processed_count,
                    batch_index=batch_idx,
                    total_batches=total_batches,
                    results=batch_result
                )

        return {"created": created, "updated": updated}

    async def _upsert_settings_with_retry(
        self,
        work_id: str,
        settings_data: List[Dict[str, str]],
        resume: bool = False
    ) -> Dict[str, int]:
        """带重试机制的设定批量处理"""
        created = 0
        updated = 0

        batch_size = settings.WORLDVIEW_SETTING_BATCH_SIZE
        total_batches = (len(settings_data) + batch_size - 1) // batch_size

        # 获取恢复点
        start_batch = 0
        if resume:
            resume_point = await self.progress_service.get_resume_point(work_id)
            if resume_point:
                start_batch = resume_point["settings"]["next_batch"]
                created = resume_point["results"]["settings"]["created"]
                updated = resume_point["results"]["settings"]["updated"]

        logger.info(f"开始分批处理 {len(settings_data)} 个设定，批次大小: {batch_size}, 从批次 {start_batch} 开始")

        for batch_idx in range(start_batch, total_batches):
            start_idx = batch_idx * batch_size
            end_idx = min(start_idx + batch_size, len(settings_data))
            batch = settings_data[start_idx:end_idx]

            batch_result = await self._process_batch_with_retry(
                work_id=work_id,
                batch=batch,
                batch_idx=batch_idx,
                phase="settings",
                processor=self._process_setting_batch
            )

            if batch_result:
                created += batch_result["created"]
                updated += batch_result["updated"]

                processed_count = min((batch_idx + 1) * batch_size, len(settings_data))
                await self.progress_service.update_phase_progress(
                    work_id=work_id,
                    phase="settings",
                    processed_count=processed_count,
                    batch_index=batch_idx,
                    total_batches=total_batches,
                    results=batch_result
                )

        return {"created": created, "updated": updated}

    async def _process_batch_with_retry(
        self,
        work_id: str,
        batch: List[Dict[str, str]],
        batch_idx: int,
        phase: str,
        processor
    ) -> Optional[Dict[str, int]]:
        """处理单个批次，带自动重试机制"""
        max_retries = settings.WORLDVIEW_BATCH_MAX_RETRIES
        retry_delay = settings.WORLDVIEW_RETRY_DELAY

        for attempt in range(max_retries + 1):
            try:
                logger.info(f"处理{phase}批次 {batch_idx + 1}, 尝试 {attempt + 1}/{max_retries + 1}")

                result = await processor(work_id, batch)

                if attempt > 0:
                    logger.info(f"批次 {batch_idx + 1} 在第 {attempt + 1} 次尝试后成功")

                return result

            except Exception as e:
                logger.error(f"处理{phase}批次 {batch_idx + 1} 时出错 (尝试 {attempt + 1}): {e}")

                if attempt < max_retries:
                    logger.info(f"等待 {retry_delay} 秒后重试批次 {batch_idx + 1}")
                    await asyncio.sleep(retry_delay)
                    retry_delay *= 2  # 指数退避
                else:
                    logger.error(f"批次 {batch_idx + 1} 在 {max_retries + 1} 次尝试后仍然失败")

                    # 记录失败的批次
                    if settings.WORLDVIEW_ENABLE_PROGRESS_PERSISTENCE:
                        await self.progress_service.add_failed_batch(
                            work_id=work_id,
                            phase=phase,
                            batch_index=batch_idx,
                            error_message=str(e),
                            batch_data=batch
                        )

                    return None

        return None

    # ==================== 具体的批次处理方法 ====================

    async def _process_character_batch(
        self,
        work_id: str,
        batch: List[Dict[str, str]]
    ) -> Dict[str, int]:
        """处理单个角色批次"""
        from app.core.database import create_db_session
        async with create_db_session() as batch_db:
            batch_service = WorldviewService(batch_db)

            # 获取现有角色
            existing_characters = await batch_service.get_characters_by_work(work_id)
            existing_names = {char.name: char for char in existing_characters}

            batch_created = 0
            batch_updated = 0

            # 处理当前批次
            for char_data in batch:
                name = char_data['name']

                if name in existing_names:
                    # 更新现有角色
                    existing_char = existing_names[name]
                    old_desc = existing_char.description or ""
                    new_desc = char_data['description']

                    merged_desc = self._merge_descriptions(old_desc, new_desc)
                    if merged_desc != old_desc:
                        await batch_service.update_character(
                            str(existing_char.id),
                            CharacterUpdate(description=merged_desc)
                        )
                        batch_updated += 1
                else:
                    # 创建新角色
                    await batch_service.create_character(
                        CharacterCreate(
                            work_id=work_id,
                            name=name,
                            description=char_data['description'],
                            role=char_data.get('role', '')
                        )
                    )
                    batch_created += 1

            await batch_db.commit()
            return {"created": batch_created, "updated": batch_updated}

    async def _process_location_batch(
        self,
        work_id: str,
        batch: List[Dict[str, str]]
    ) -> Dict[str, int]:
        """处理单个地点批次"""
        from app.core.database import create_db_session
        async with create_db_session() as batch_db:
            batch_service = WorldviewService(batch_db)

            existing_locations = await batch_service.get_locations_by_work(work_id)
            existing_names = {loc.name: loc for loc in existing_locations}

            batch_created = 0
            batch_updated = 0

            for loc_data in batch:
                name = loc_data['name']

                if name in existing_names:
                    existing_loc = existing_names[name]
                    old_desc = existing_loc.description or ""
                    new_desc = loc_data['description']

                    merged_desc = self._merge_descriptions(old_desc, new_desc)
                    if merged_desc != old_desc:
                        await batch_service.update_location(
                            str(existing_loc.id),
                            LocationUpdate(description=merged_desc)
                        )
                        batch_updated += 1
                else:
                    await batch_service.create_location(
                        LocationCreate(
                            work_id=work_id,
                            name=name,
                            description=loc_data['description'],
                            location_type=loc_data.get('location_type', '')
                        )
                    )
                    batch_created += 1

            await batch_db.commit()
            return {"created": batch_created, "updated": batch_updated}

    async def _process_setting_batch(
        self,
        work_id: str,
        batch: List[Dict[str, str]]
    ) -> Dict[str, int]:
        """处理单个设定批次"""
        from app.core.database import create_db_session
        async with create_db_session() as batch_db:
            batch_service = WorldviewService(batch_db)

            existing_settings = await batch_service.get_settings_by_work(work_id)
            existing_titles = {setting.title: setting for setting in existing_settings}

            batch_created = 0
            batch_updated = 0

            for setting_data in batch:
                title = setting_data['title']

                if title in existing_titles:
                    existing_setting = existing_titles[title]
                    old_content = existing_setting.content or ""
                    new_content = setting_data['content']

                    merged_content = self._merge_descriptions(old_content, new_content)
                    if merged_content != old_content:
                        await batch_service.update_setting(
                            str(existing_setting.id),
                            SettingUpdate(content=merged_content)
                        )
                        batch_updated += 1
                else:
                    await batch_service.create_setting(
                        SettingCreate(
                            work_id=work_id,
                            title=title,
                            content=setting_data['content'],
                            category=setting_data.get('category', '')
                        )
                    )
                    batch_created += 1

            await batch_db.commit()
            return {"created": batch_created, "updated": batch_updated}

    # ==================== 原有的提取方法（保持不变） ====================

    def _is_valid_entity_name(self, name: str, entity_type: str) -> bool:
        """验证实体名称是否有效"""
        if len(name) < 2 or len(name) > 20:
            return False

        if name.isdigit():
            return False

        # 黑名单过滤
        common_blacklist = [
            '章节', '第', '初期', '中期', '末期', '阶段', '报告', '分析',
            '主角', '配角', '人物', '角色', '地点', '场所', '事件', '矛盾',
            '关系', '转折', '关键', '核心', '演变', '时间', '地图', '世界观'
        ]

        for word in common_blacklist:
            if word in name:
                return False

        return True

    def _merge_descriptions(self, old_desc: str, new_desc: str) -> str:
        """合并描述信息"""
        if not old_desc:
            return new_desc
        if not new_desc:
            return old_desc

        # 简单合并：如果新描述不为空且不包含在旧描述中，则追加
        if new_desc not in old_desc:
            return f"{old_desc}\n\n{new_desc}"
        return old_desc

    # ==================== 微观分析提取 ====================

    def _extract_entities_from_micro(
        self,
        micro_results: List[Dict[str, Any]]
    ) -> Dict[str, List[Dict[str, Any]]]:
        """
        从微观分析结果中提取所有实体（严格过滤）

        Returns:
            {
                "characters": [{name, descriptions: [desc1, desc2, ...]}],
                "locations": [{name, descriptions: [...]}],
                "other": [{name, descriptions: [...]}]
            }
        """
        # 使用字典存储，key是name，value是描述列表
        characters_dict = {}
        locations_dict = {}
        other_dict = {}

        for chapter_data in micro_results:
            detailed_events = chapter_data.get('detailed_events', [])

            for event in detailed_events:
                entities = event.get('entities_involved', [])

                for entity in entities:
                    entity_type = entity.get('type', '').lower()
                    name = entity.get('name', '').strip()
                    description = entity.get('description', '').strip()

                    if not name or not description:
                        continue

                    # 描述太短的跳过（可能是低质量数据）
                    if len(description) < 10:
                        continue

                    # 根据类型分类并验证
                    if 'character' in entity_type or '角色' in entity_type or '人物' in entity_type:
                        if not self._is_valid_entity_name(name, 'character'):
                            continue
                        if name not in characters_dict:
                            characters_dict[name] = []
                        characters_dict[name].append(description)

                    elif 'location' in entity_type or '地点' in entity_type or '场所' in entity_type:
                        if not self._is_valid_entity_name(name, 'location'):
                            continue
                        if name not in locations_dict:
                            locations_dict[name] = []
                        locations_dict[name].append(description)

                    else:  # artifact, item, concept等
                        if not self._is_valid_entity_name(name, 'other'):
                            continue
                        if name not in other_dict:
                            other_dict[name] = []
                        other_dict[name].append(description)

        # 转换为列表格式
        return {
            "characters": [
                {"name": name, "descriptions": descs}
                for name, descs in characters_dict.items()
            ],
            "locations": [
                {"name": name, "descriptions": descs}
                for name, descs in locations_dict.items()
            ],
            "other": [
                {"name": name, "descriptions": descs}
                for name, descs in other_dict.items()
            ]
        }

    # ==================== 宏观分析提取 ====================

    def _extract_from_macro(self, macro_results: Optional[str]) -> Dict[str, Any]:
        """
        从宏观分析报告中提取结构化信息

        Returns:
            {
                "protagonist_name": str,
                "character_arcs": {name: arc_description},
                "major_locations": {name: description},
                "key_events": [event1, event2, ...],
                "conflicts": [conflict1, conflict2, ...]
            }
        """
        if not macro_results:
            return {
                "protagonist_name": None,
                "character_arcs": {},
                "major_locations": {},
                "key_events": [],
                "conflicts": []
            }

        result = {
            "protagonist_name": None,
            "character_arcs": {},
            "major_locations": {},
            "key_events": [],
            "conflicts": []
        }

        # 简化的提取逻辑（保持原有的核心功能）
        try:
            # 提取主角名字
            import re
            protagonist_match = re.search(r'主角[：:]\s*([^\n，。]{2,20})', macro_results)
            if protagonist_match:
                result["protagonist_name"] = protagonist_match.group(1).strip()

            # 提取主要地点
            location_section = self._extract_section(macro_results, "主要地点")
            if location_section:
                locations = re.findall(r'([^\n，。]{2,20})[：:]\s*([^\n]{10,200})', location_section)
                for name, desc in locations:
                    if self._is_valid_entity_name(name, 'location'):
                        result["major_locations"][name] = desc.strip()

            # 提取关键事件
            events_section = self._extract_section(macro_results, "关键事件")
            if events_section:
                events = re.findall(r'[•·-]\s*([^\n]{20,200})', events_section)
                result["key_events"] = [event.strip() for event in events if len(event.strip()) > 10]

        except Exception as e:
            logger.warning(f"宏观分析提取时出错: {e}")

        return result

    def _extract_section(self, content: str, section_title: str) -> Optional[str]:
        """从内容中提取指定标题的部分"""
        import re
        pattern = rf'{re.escape(section_title)}[：:]\s*\n(.*?)(?=\n\n|\n[一二三四五六七八九十]|\Z)'
        match = re.search(pattern, content, re.DOTALL)
        return match.group(1).strip() if match else None

    def _merge_entity_data(self, entities: Dict, macro_data: Dict) -> Dict[str, List]:
        """合并微观和宏观分析的数据"""
        # 将微观分析的描述合并为单个描述
        def merge_descriptions_list(descriptions: List[str]) -> str:
            if not descriptions:
                return ""
            # 去重并合并
            unique_descs = list(set(descriptions))
            return "\n\n".join(unique_descs)

        result = {
            "characters": [
                {
                    "name": char["name"],
                    "description": merge_descriptions_list(char["descriptions"]),
                    "role": "角色"
                }
                for char in entities["characters"]
            ],
            "locations": [
                {
                    "name": loc["name"],
                    "description": merge_descriptions_list(loc["descriptions"]),
                    "location_type": "地点"
                }
                for loc in entities["locations"]
            ],
            "settings": [
                {
                    "title": other["name"],
                    "content": merge_descriptions_list(other["descriptions"]),
                    "category": "其他设定"
                }
                for other in entities["other"]
            ]
        }

        # 添加宏观分析中的地点
        for name, desc in macro_data.get("major_locations", {}).items():
            if name not in [loc["name"] for loc in result["locations"]]:
                result["locations"].append({
                    "name": name,
                    "description": desc,
                    "location_type": "主要地点"
                })

        return result