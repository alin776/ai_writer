"""
世界观服务层
处理人物、地点、设定、作品规范的业务逻辑
"""
from typing import List, Optional
import logging
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.orm import selectinload

from app.models.character import Character
from app.models.location import Location
from app.models.setting import Setting
from app.models.glossary_term import GlossaryTerm
from app.models.work_guidelines import WorkGuidelines
from app.schemas.worldview import (
    CharacterCreate, CharacterUpdate,
    LocationCreate, LocationUpdate,
    SettingCreate, SettingUpdate,
    WorkGuidelinesCreate, WorkGuidelinesUpdate,
    GlossaryTermCreate, GlossaryTermUpdate
)

logger = logging.getLogger(__name__)


class WorldviewService:
    """世界观服务"""
    
    def __init__(self, db: AsyncSession, *, auto_sync_knowledge: bool = True):
        self.db = db
        self.auto_sync_knowledge = auto_sync_knowledge

    def _invalidate_worldview_cache(self, work_id: str) -> None:
        """失效世界观相关缓存（按作品维度）"""
        if not work_id:
            return
        try:
            from app.services.agent.utils.tool_cache import ToolCache
            ToolCache.invalidate(work_id=str(work_id), include_work_scope=True)
        except Exception as e:
            logger.debug(f"[WorldviewService] 缓存失效失败: {e}")

    async def _sync_knowledge_mirror(self, work_id: str) -> None:
        """将世界观卡片自动镜像到 knowledge/*.md。"""
        if not self.auto_sync_knowledge or not work_id:
            return
        try:
            from app.services.worldview_knowledge_bridge import WorldviewKnowledgeBridge

            bridge = WorldviewKnowledgeBridge(self.db)
            await bridge.mirror_from_cards(work_id)
        except Exception as e:
            # Best effort only; card writes should not fail because mirror write failed.
            logger.warning(f"[WorldviewService] 知识库镜像失败: {e}")
    
    # ==================== Character 相关 ====================
    
    async def get_characters_by_work(self, work_id: str) -> List[Character]:
        """获取作品的所有人物"""
        result = await self.db.execute(
            select(Character).where(Character.work_id == work_id)
        )
        return result.scalars().all()
    
    async def get_character_by_id(self, character_id: str) -> Optional[Character]:
        """根据ID获取人物"""
        result = await self.db.execute(
            select(Character).where(Character.id == character_id)
        )
        return result.scalar_one_or_none()
    
    async def create_character(self, character_data: CharacterCreate) -> Character:
        """创建人物"""
        character = Character(**character_data.model_dump())
        self.db.add(character)
        await self.db.commit()
        await self.db.refresh(character)
        self._invalidate_worldview_cache(str(character.work_id))
        await self._sync_knowledge_mirror(str(character.work_id))
        return character
    
    async def update_character(self, character_id: str, character_data: CharacterUpdate) -> Optional[Character]:
        """更新人物"""
        character = await self.get_character_by_id(character_id)
        if not character:
            return None
        
        update_data = character_data.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(character, field, value)
        
        await self.db.commit()
        await self.db.refresh(character)
        self._invalidate_worldview_cache(str(character.work_id))
        await self._sync_knowledge_mirror(str(character.work_id))
        return character
    
    async def delete_character(self, character_id: str) -> bool:
        """删除人物"""
        character = await self.get_character_by_id(character_id)
        if not character:
            return False
        work_id = str(character.work_id)
        await self.db.delete(character)
        await self.db.commit()
        self._invalidate_worldview_cache(work_id)
        await self._sync_knowledge_mirror(work_id)
        return True
    
    # ==================== Location 相关 ====================
    
    async def get_locations_by_work(self, work_id: str) -> List[Location]:
        """获取作品的所有地点"""
        result = await self.db.execute(
            select(Location).where(Location.work_id == work_id)
        )
        return result.scalars().all()
    
    async def get_location_by_id(self, location_id: str) -> Optional[Location]:
        """根据ID获取地点"""
        result = await self.db.execute(
            select(Location).where(Location.id == location_id)
        )
        return result.scalar_one_or_none()
    
    async def create_location(self, location_data: LocationCreate) -> Location:
        """创建地点"""
        location = Location(**location_data.model_dump())
        self.db.add(location)
        await self.db.commit()
        await self.db.refresh(location)
        self._invalidate_worldview_cache(str(location.work_id))
        await self._sync_knowledge_mirror(str(location.work_id))
        return location
    
    async def update_location(self, location_id: str, location_data: LocationUpdate) -> Optional[Location]:
        """更新地点"""
        location = await self.get_location_by_id(location_id)
        if not location:
            return None
        
        update_data = location_data.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(location, field, value)
        
        await self.db.commit()
        await self.db.refresh(location)
        self._invalidate_worldview_cache(str(location.work_id))
        await self._sync_knowledge_mirror(str(location.work_id))
        return location
    
    async def delete_location(self, location_id: str) -> bool:
        """删除地点"""
        location = await self.get_location_by_id(location_id)
        if not location:
            return False
        work_id = str(location.work_id)
        await self.db.delete(location)
        await self.db.commit()
        self._invalidate_worldview_cache(work_id)
        await self._sync_knowledge_mirror(work_id)
        return True
    
    # ==================== Setting 相关 ====================
    
    async def get_settings_by_work(self, work_id: str) -> List[Setting]:
        """获取作品的所有设定"""
        result = await self.db.execute(
            select(Setting).where(Setting.work_id == work_id)
        )
        return result.scalars().all()
    
    async def get_setting_by_id(self, setting_id: str) -> Optional[Setting]:
        """根据ID获取设定"""
        result = await self.db.execute(
            select(Setting).where(Setting.id == setting_id)
        )
        return result.scalar_one_or_none()
    
    async def create_setting(self, setting_data: SettingCreate) -> Setting:
        """创建设定"""
        setting = Setting(**setting_data.model_dump())
        self.db.add(setting)
        await self.db.commit()
        await self.db.refresh(setting)
        self._invalidate_worldview_cache(str(setting.work_id))
        await self._sync_knowledge_mirror(str(setting.work_id))
        return setting
    
    async def update_setting(self, setting_id: str, setting_data: SettingUpdate) -> Optional[Setting]:
        """更新设定"""
        setting = await self.get_setting_by_id(setting_id)
        if not setting:
            return None
        
        update_data = setting_data.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(setting, field, value)
        
        await self.db.commit()
        await self.db.refresh(setting)
        self._invalidate_worldview_cache(str(setting.work_id))
        await self._sync_knowledge_mirror(str(setting.work_id))
        return setting
    
    async def delete_setting(self, setting_id: str) -> bool:
        """删除设定"""
        setting = await self.get_setting_by_id(setting_id)
        if not setting:
            return False
        work_id = str(setting.work_id)
        await self.db.delete(setting)
        await self.db.commit()
        self._invalidate_worldview_cache(work_id)
        await self._sync_knowledge_mirror(work_id)
        return True
    
    # ==================== WorkGuidelines 相关 ====================
    
    async def get_guidelines_by_work(self, work_id: str) -> Optional[WorkGuidelines]:
        """获取作品的规范"""
        result = await self.db.execute(
            select(WorkGuidelines).where(WorkGuidelines.work_id == work_id)
        )
        return result.scalar_one_or_none()
    
    async def create_or_update_guidelines(
        self, 
        work_id: str, 
        guidelines_data: WorkGuidelinesCreate | WorkGuidelinesUpdate
    ) -> WorkGuidelines:
        """创建或更新作品规范"""
        # 尝试获取现有规范
        existing = await self.get_guidelines_by_work(work_id)
        
        if existing:
            # 更新现有规范
            update_data = guidelines_data.model_dump(exclude_unset=True)
            for field, value in update_data.items():
                setattr(existing, field, value)
            await self.db.commit()
            await self.db.refresh(existing)
            self._invalidate_worldview_cache(str(work_id))
            return existing
        else:
            # 创建新规范
            if isinstance(guidelines_data, WorkGuidelinesUpdate):
                guidelines_data = WorkGuidelinesCreate(work_id=work_id, **guidelines_data.model_dump())
            
            guidelines = WorkGuidelines(**guidelines_data.model_dump())
            self.db.add(guidelines)
            await self.db.commit()
            await self.db.refresh(guidelines)
            self._invalidate_worldview_cache(str(work_id))
            return guidelines
    
    async def delete_guidelines(self, work_id: str) -> bool:
        """删除作品规范"""
        guidelines = await self.get_guidelines_by_work(work_id)
        if not guidelines:
            return False
        await self.db.delete(guidelines)
        await self.db.commit()
        self._invalidate_worldview_cache(str(work_id))
        return True

    # ==================== Glossary 相关 ====================

    async def get_glossary_by_work(self, work_id: str) -> List[GlossaryTerm]:
        """获取作品术语表"""
        result = await self.db.execute(
            select(GlossaryTerm).where(GlossaryTerm.work_id == work_id)
        )
        return result.scalars().all()

    async def get_glossary_term_by_id(self, term_id: str) -> Optional[GlossaryTerm]:
        """根据ID获取术语"""
        result = await self.db.execute(
            select(GlossaryTerm).where(GlossaryTerm.id == term_id)
        )
        return result.scalar_one_or_none()

    async def create_glossary_term(self, term_data: GlossaryTermCreate) -> GlossaryTerm:
        """创建术语"""
        term = GlossaryTerm(**term_data.model_dump())
        self.db.add(term)
        await self.db.commit()
        await self.db.refresh(term)
        self._invalidate_worldview_cache(str(term.work_id))
        return term

    async def update_glossary_term(self, term_id: str, term_data: GlossaryTermUpdate) -> Optional[GlossaryTerm]:
        """更新术语"""
        term = await self.get_glossary_term_by_id(term_id)
        if not term:
            return None
        update_data = term_data.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(term, field, value)
        await self.db.commit()
        await self.db.refresh(term)
        self._invalidate_worldview_cache(str(term.work_id))
        return term

    async def delete_glossary_term(self, term_id: str) -> bool:
        """删除术语"""
        term = await self.get_glossary_term_by_id(term_id)
        if not term:
            return False
        work_id = str(term.work_id)
        await self.db.delete(term)
        await self.db.commit()
        self._invalidate_worldview_cache(work_id)
        return True
