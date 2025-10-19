"""
世界观提取服务
从小说分析结果中自动提取角色、地点和设定信息
"""
import logging
import re
from typing import List, Dict, Any, Optional, Set, Tuple
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.novel_analysis import NovelAnalysis, AnalysisStatus
from app.services.worldview_service import WorldviewService
from app.schemas.worldview import (
    CharacterCreate, LocationCreate, SettingCreate
)

logger = logging.getLogger(__name__)


class WorldviewExtractionService:
    """世界观提取服务"""
    
    def __init__(self, db: AsyncSession):
        self.db = db
        self.worldview_service = WorldviewService(db)
    
    # ==================== 主要方法 ====================
    
    async def extract_from_analysis(
        self,
        work_id: str,
        analysis: NovelAnalysis,
        options: Optional[Dict[str, bool]] = None
    ) -> Dict[str, Any]:
        """
        从小说分析结果中提取并创建/更新世界观数据
        
        Args:
            work_id: 作品ID
            analysis: 小说分析对象
            options: 提取选项，例如 {"characters": True, "locations": True, "settings": True}
            
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
        
        logger.info(f"开始从分析结果提取世界观数据，work_id={work_id}")
        
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
        
        # 4. 创建/更新角色
        if options.get("characters", True):
            char_stats = await self._upsert_characters(work_id, merged_data['characters'])
            result["characters"] = char_stats
            logger.info(f"角色处理完成: 创建 {char_stats['created']}, 更新 {char_stats['updated']}")
        
        # 5. 创建/更新地点
        if options.get("locations", True):
            loc_stats = await self._upsert_locations(work_id, merged_data['locations'])
            result["locations"] = loc_stats
            logger.info(f"地点处理完成: 创建 {loc_stats['created']}, 更新 {loc_stats['updated']}")
        
        # 6. 创建/更新设定
        if options.get("settings", True):
            set_stats = await self._upsert_settings(work_id, merged_data['settings'])
            result["settings"] = set_stats
            logger.info(f"设定处理完成: 创建 {set_stats['created']}, 更新 {set_stats['updated']}")
        
        logger.info(f"世界观提取完成: {result}")
        return result
    
    # ==================== 微观分析提取 ====================
    
    def _is_valid_entity_name(self, name: str, entity_type: str) -> bool:
        """
        验证实体名称是否有效
        
        Args:
            name: 实体名称
            entity_type: 实体类型 (character/location/other)
        
        Returns:
            bool: 是否有效
        """
        # 基本长度限制
        if len(name) < 2 or len(name) > 20:
            return False
        
        # 不能全是数字
        if name.isdigit():
            return False
        
        # 通用黑名单（过滤描述性词汇、时间词汇等）
        common_blacklist = [
            '章节', '第', '初期', '中期', '末期', '阶段', '报告', '分析',
            '主角', '配角', '人物', '角色', '地点', '场所', '事件', '矛盾',
            '关系', '转折', '关键', '核心', '演变', '时间', '地图', '世界观',
            '主要', '次要', '重要', '一般', '描述', '概括', '总结', '具体',
            '大约', '左右', '之间', '以上', '以下', '等等', '以及', '还有'
        ]
        
        # 角色特定黑名单
        character_blacklist = [
            '他', '她', '它', '我', '你', '他们', '她们', '我们', '你们',
            '某人', '某个', '一个', '两个', '三个', '几个', '所有', '全部',
            '成长', '弧光', '状态', '心理', '性格', '变化', '发展'
        ]
        
        # 地点特定黑名单
        location_blacklist = [
            '这里', '那里', '某处', '某地', '一处', '多处', '到处', '各处',
            '功能', '定位', '布局', '空间', '位置', '方向', '距离'
        ]
        
        # 检查黑名单
        for word in common_blacklist:
            if word in name:
                return False
        
        if entity_type == 'character':
            for word in character_blacklist:
                if word in name:
                    return False
        elif entity_type == 'location':
            for word in location_blacklist:
                if word in name:
                    return False
        
        return True
    
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
        
        # 1. 提取主角名称
        protagonist_match = re.search(r'主角[:：]\s*([^\s,，。\n]+)', macro_results)
        if protagonist_match:
            result["protagonist_name"] = protagonist_match.group(1).strip()
        
        # 2. 提取人物成长轨迹信息（更严格的匹配）
        character_section = self._extract_section(macro_results, "人物成长轨迹报告")
        if character_section:
            # 只匹配明确的人物名称格式（2-8个字符，更严格）
            character_matches = re.findall(r'([一-龥a-zA-Z]{2,8})[:：]\s*([^\n]{15,})', character_section)
            for name, desc in character_matches:
                name = name.strip()
                # 严格验证人名
                if self._is_valid_entity_name(name, 'character') and len(desc.strip()) >= 15:
                    result["character_arcs"][name] = desc.strip()[:200]  # 限制描述长度
        
        # 3. 提取主要地点（更严格的匹配）
        world_section = self._extract_section(macro_results, "世界观图谱与时间线报告")
        if world_section:
            # 只匹配明确的地点格式（包含"地"、"城"、"山"等地点关键字，或者2-10个汉字）
            location_matches = re.findall(r'([一-龥]{2,10}(?:城|镇|村|山|河|湖|海|岛|宫|殿|楼|阁|院|府|街|道|港|站|厅|室|馆)|[一-龥]{2,10})[:：\-—]\s*([^\n]{15,})', world_section)
            for name, desc in location_matches:
                name = name.strip()
                # 严格验证地名
                if self._is_valid_entity_name(name, 'location') and len(desc.strip()) >= 15:
                    # 额外检查：地名应该不包含动词
                    if not any(verb in name for verb in ['发生', '进行', '产生', '出现', '导致', '造成', '引起']):
                        result["major_locations"][name] = desc.strip()[:200]
        
        # 4. 提取关键事件
        if world_section:
            events_text = re.findall(r'关键事件[：:]\s*([^\n]+)', world_section)
            for event_line in events_text:
                events = event_line.split('、')
                result["key_events"].extend([e.strip() for e in events if len(e.strip()) > 5])
        
        # 5. 提取核心矛盾
        conflict_section = self._extract_section(macro_results, "核心矛盾演变报告")
        if conflict_section:
            # 提取初期、中期、末期矛盾
            for stage in ['初期', '中期', '末期']:
                conflict_match = re.search(f'{stage}[^：:]*[:：]\s*([^\n]{{20,200}})', conflict_section)
                if conflict_match:
                    result["conflicts"].append(f"{stage}矛盾：{conflict_match.group(1).strip()}")
        
        logger.debug(f"从宏观分析提取到: 主角={result['protagonist_name']}, "
                    f"人物={len(result['character_arcs'])}, "
                    f"地点={len(result['major_locations'])}, "
                    f"事件={len(result['key_events'])}, "
                    f"矛盾={len(result['conflicts'])}")
        
        return result
    
    def _extract_section(self, text: str, section_title: str) -> Optional[str]:
        """从文本中提取指定章节的内容"""
        # 匹配章节标题到下一个章节标题之间的内容
        pattern = f'{section_title}[^\\n]*\\n+(.*?)(?=\\n+[#*]{{2,}}|$)'
        match = re.search(pattern, text, re.DOTALL)
        if match:
            return match.group(1).strip()
        return None
    
    # ==================== 数据合并 ====================
    
    def _merge_entity_data(
        self,
        entities: Dict[str, List[Dict[str, Any]]],
        macro_data: Dict[str, Any]
    ) -> Dict[str, List[Dict[str, str]]]:
        """
        合并微观和宏观提取的数据
        
        Returns:
            {
                "characters": [{name, description, role}],
                "locations": [{name, description, type}],
                "settings": [{title, content, category}]
            }
        """
        # 1. 合并角色数据
        characters = []
        char_names_seen = set()
        
        # 从微观数据添加角色
        for char in entities['characters']:
            name = char['name']
            descriptions = char['descriptions']
            
            # 过滤掉太短或太长的描述
            valid_descs = [d for d in descriptions if 10 <= len(d) <= 200]
            if not valid_descs:
                continue
            
            # 合并所有描述（去重）
            unique_descs = list(dict.fromkeys(valid_descs))  # 保持顺序去重
            combined_desc = " | ".join(unique_descs[:3])  # 最多保留3条描述
            
            # 检查是否是主角
            role = "配角"
            if name == macro_data.get('protagonist_name'):
                role = "主角"
                # 补充宏观分析中的成长轨迹
                arc_desc = macro_data['character_arcs'].get(name, '')
                if arc_desc:
                    combined_desc = f"{arc_desc} | {combined_desc}"
            elif name in macro_data['character_arcs']:
                role = "重要角色"
                arc_desc = macro_data['character_arcs'][name]
                combined_desc = f"{arc_desc} | {combined_desc}"
            
            characters.append({
                "name": name,
                "description": combined_desc[:1000],  # 限制长度
                "role": role
            })
            char_names_seen.add(name)
        
        # 添加宏观分析中独有的角色
        for name, arc_desc in macro_data['character_arcs'].items():
            if name not in char_names_seen:
                role = "主角" if name == macro_data.get('protagonist_name') else "重要角色"
                characters.append({
                    "name": name,
                    "description": arc_desc[:1000],
                    "role": role
                })
        
        # 2. 合并地点数据
        locations = []
        loc_names_seen = set()
        
        # 从微观数据添加地点
        for loc in entities['locations']:
            name = loc['name']
            descriptions = loc['descriptions']
            
            # 过滤掉太短或太长的描述
            valid_descs = [d for d in descriptions if 10 <= len(d) <= 200]
            if not valid_descs:
                continue
            
            unique_descs = list(dict.fromkeys(valid_descs))
            combined_desc = " | ".join(unique_descs[:3])
            
            # 检查宏观分析中是否有补充描述
            if name in macro_data['major_locations']:
                macro_desc = macro_data['major_locations'][name]
                combined_desc = f"{macro_desc} | {combined_desc}"
            
            locations.append({
                "name": name,
                "description": combined_desc[:1000],
                "type": "未分类"  # 默认类型
            })
            loc_names_seen.add(name)
        
        # 添加宏观分析中独有的地点
        for name, desc in macro_data['major_locations'].items():
            if name not in loc_names_seen:
                locations.append({
                    "name": name,
                    "description": desc[:1000],
                    "type": "主要场景"
                })
        
        # 3. 创建设定数据（从其他实体和关键信息）
        settings = []
        
        # 从其他实体创建设定
        for item in entities['other']:
            name = item['name']
            descriptions = item['descriptions']
            
            # 过滤掉太短或太长的描述
            valid_descs = [d for d in descriptions if 10 <= len(d) <= 200]
            if not valid_descs:
                continue
            
            unique_descs = list(dict.fromkeys(valid_descs))
            combined_desc = " | ".join(unique_descs[:2])
            
            settings.append({
                "title": name,
                "content": combined_desc[:2000],
                "category": "物品/概念"
            })
        
        # 从关键事件创建设定
        if macro_data['key_events']:
            events_content = "\n".join(f"- {event}" for event in macro_data['key_events'][:10])
            settings.append({
                "title": "关键历史事件",
                "content": events_content[:2000],
                "category": "世界观设定"
            })
        
        # 从核心矛盾创建设定
        if macro_data['conflicts']:
            conflicts_content = "\n".join(f"- {conflict}" for conflict in macro_data['conflicts'])
            settings.append({
                "title": "核心矛盾演变",
                "content": conflicts_content[:2000],
                "category": "剧情设定"
            })
        
        logger.debug(f"合并后: 角色={len(characters)}, 地点={len(locations)}, 设定={len(settings)}")
        
        return {
            "characters": characters,
            "locations": locations,
            "settings": settings
        }
    
    # ==================== 辅助方法 ====================
    
    def _merge_descriptions(self, old_desc: str, new_desc: str) -> str:
        """
        智能合并新旧描述，去除重复内容
        
        Args:
            old_desc: 已有的描述
            new_desc: 新提取的描述
            
        Returns:
            str: 合并后的描述
        """
        if not old_desc:
            return new_desc
        if not new_desc:
            return old_desc
        
        # 如果新旧描述完全相同，直接返回
        if old_desc == new_desc:
            return old_desc
        
        # 将描述按分隔符拆分
        # 支持 | 和 换行符作为分隔符
        old_parts = self._split_description(old_desc)
        new_parts = self._split_description(new_desc)
        
        # 合并并去重（保持顺序）
        # 先添加旧的，再添加新的（新的不在旧的中）
        merged_parts = []
        seen_normalized = set()
        
        # 添加旧的部分
        for part in old_parts:
            normalized = self._normalize_text(part)
            if normalized and normalized not in seen_normalized:
                merged_parts.append(part)
                seen_normalized.add(normalized)
        
        # 添加新的部分（去重）
        for part in new_parts:
            normalized = self._normalize_text(part)
            if normalized and normalized not in seen_normalized:
                merged_parts.append(part)
                seen_normalized.add(normalized)
        
        # 重新组合（使用 | 分隔，保持整洁）
        result = " | ".join(merged_parts)
        
        # 限制总长度（避免无限增长）
        max_length = 2000
        if len(result) > max_length:
            # 保留前面的重要信息
            result = result[:max_length] + "..."
        
        return result
    
    def _split_description(self, text: str) -> List[str]:
        """
        拆分描述文本
        
        Args:
            text: 描述文本
            
        Returns:
            List[str]: 拆分后的片段列表
        """
        # 先按 | 拆分
        parts = text.split('|')
        
        # 清理每个片段（去除首尾空格）
        parts = [part.strip() for part in parts if part.strip()]
        
        # 如果只有一个片段且很长，尝试按换行符拆分
        if len(parts) == 1 and len(parts[0]) > 200:
            sub_parts = parts[0].split('\n')
            sub_parts = [p.strip() for p in sub_parts if p.strip()]
            if len(sub_parts) > 1:
                parts = sub_parts
        
        return parts
    
    def _normalize_text(self, text: str) -> str:
        """
        规范化文本用于比较（去除空格、标点等）
        
        Args:
            text: 原始文本
            
        Returns:
            str: 规范化后的文本
        """
        import re
        # 去除所有空白字符
        text = re.sub(r'\s+', '', text)
        # 去除常见标点
        text = re.sub(r'[，。！？、；：""''《》（）【】\.,!?;:\'"()\[\]]+', '', text)
        # 转为小写（如果有英文）
        text = text.lower()
        return text
    
    # ==================== 创建/更新数据 ====================
    
    async def _upsert_characters(
        self,
        work_id: str,
        characters_data: List[Dict[str, str]]
    ) -> Dict[str, int]:
        """创建或更新角色"""
        created = 0
        updated = 0
        
        # 获取现有角色
        existing_characters = await self.worldview_service.get_characters_by_work(work_id)
        existing_names = {char.name: char for char in existing_characters}
        
        for char_data in characters_data:
            name = char_data['name']
            
            if name in existing_names:
                # 更新：补充描述信息，而不是替换
                existing_char = existing_names[name]
                old_desc = existing_char.description or ""
                new_desc = char_data['description']
                
                # 合并新旧描述（去重）
                merged_desc = self._merge_descriptions(old_desc, new_desc)
                
                # 如果合并后的描述与原描述不同，则更新
                if merged_desc != old_desc:
                    from app.schemas.worldview import CharacterUpdate
                    await self.worldview_service.update_character(
                        str(existing_char.id),
                        CharacterUpdate(
                            description=merged_desc,
                            role=char_data['role']
                        )
                    )
                    updated += 1
                    logger.debug(f"更新角色（补充描述）: {name}")
            else:
                # 创建新角色
                await self.worldview_service.create_character(
                    CharacterCreate(
                        work_id=work_id,
                        name=name,
                        description=char_data['description'],
                        role=char_data['role']
                    )
                )
                created += 1
                logger.debug(f"创建角色: {name}")
        
        return {"created": created, "updated": updated}
    
    async def _upsert_locations(
        self,
        work_id: str,
        locations_data: List[Dict[str, str]]
    ) -> Dict[str, int]:
        """创建或更新地点"""
        created = 0
        updated = 0
        
        existing_locations = await self.worldview_service.get_locations_by_work(work_id)
        existing_names = {loc.name: loc for loc in existing_locations}
        
        for loc_data in locations_data:
            name = loc_data['name']
            
            if name in existing_names:
                # 更新：补充描述信息
                existing_loc = existing_names[name]
                old_desc = existing_loc.description or ""
                new_desc = loc_data['description']
                
                # 合并新旧描述
                merged_desc = self._merge_descriptions(old_desc, new_desc)
                
                if merged_desc != old_desc:
                    from app.schemas.worldview import LocationUpdate
                    await self.worldview_service.update_location(
                        str(existing_loc.id),
                        LocationUpdate(
                            description=merged_desc,
                            type=loc_data['type']
                        )
                    )
                    updated += 1
                    logger.debug(f"更新地点（补充描述）: {name}")
            else:
                # 创建
                await self.worldview_service.create_location(
                    LocationCreate(
                        work_id=work_id,
                        name=name,
                        description=loc_data['description'],
                        type=loc_data['type']
                    )
                )
                created += 1
                logger.debug(f"创建地点: {name}")
        
        return {"created": created, "updated": updated}
    
    async def _upsert_settings(
        self,
        work_id: str,
        settings_data: List[Dict[str, str]]
    ) -> Dict[str, int]:
        """创建或更新设定"""
        created = 0
        updated = 0
        
        existing_settings = await self.worldview_service.get_settings_by_work(work_id)
        existing_titles = {setting.title: setting for setting in existing_settings}
        
        for setting_data in settings_data:
            title = setting_data['title']
            
            if title in existing_titles:
                # 更新：补充内容信息
                existing_setting = existing_titles[title]
                old_content = existing_setting.content or ""
                new_content = setting_data['content']
                
                # 合并新旧内容
                merged_content = self._merge_descriptions(old_content, new_content)
                
                if merged_content != old_content:
                    from app.schemas.worldview import SettingUpdate
                    await self.worldview_service.update_setting(
                        str(existing_setting.id),
                        SettingUpdate(
                            content=merged_content,
                            category=setting_data['category']
                        )
                    )
                    updated += 1
                    logger.debug(f"更新设定（补充内容）: {title}")
            else:
                # 创建
                await self.worldview_service.create_setting(
                    SettingCreate(
                        work_id=work_id,
                        title=title,
                        content=setting_data['content'],
                        category=setting_data['category']
                    )
                )
                created += 1
                logger.debug(f"创建设定: {title}")
        
        return {"created": created, "updated": updated}
