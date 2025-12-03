"""
世界观 API 路由
提供人物、地点、设定、作品规范的 CRUD 接口
"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from uuid import UUID
import logging

from app.core.database import get_db
from app.core.security import get_current_active_user
from app.core.redis_client import redis_client
from app.models.user import User
from app.schemas.worldview import (
    CharacterCreate, CharacterUpdate, CharacterResponse,
    LocationCreate, LocationUpdate, LocationResponse,
    SettingCreate, SettingUpdate, SettingResponse,
    WorkGuidelinesCreate, WorkGuidelinesUpdate, WorkGuidelinesResponse,
    WorldDataResponse
)
from app.services.worldview_service import WorldviewService
from app.services.ai_guidelines_service import AIGuidelinesService
from app.schemas.ai_guidelines import (
    AIGuidelinesCreate, AIGuidelinesUpdate, AIGuidelinesResponse,
    AIGuidelinesGenerateRequest, AIGuidelinesGenerateResponse
)
from app.services.work_service import WorkService
from app.services.agent.model_selector import TaskType  # ✅ 新增：用于成本追踪

router = APIRouter()
logger = logging.getLogger(__name__)


# ==================== 辅助函数：缓存处理 ====================

def _get_cached_worldview_data(cache_key: str):
    """尝试从缓存获取世界观数据"""
    if redis_client.is_available():
        cached = redis_client.get_json(cache_key)
        if cached:
            logger.info(f"✅ [Worldview] 缓存命中: {cache_key}")
            return cached
        logger.info(f"⚠️ [Worldview] 缓存未命中: {cache_key}")
    return None


def _orm_to_dict(obj) -> dict:
    """
    将 SQLAlchemy ORM 对象转换为字典

    🔧 2025-12-02: P0修复 - 支持 Setting/AIGuidelines 等 ORM 对象的序列化
    """
    from datetime import datetime, date
    from uuid import UUID as PyUUID

    result = {}
    for column in obj.__table__.columns:
        value = getattr(obj, column.name)
        # 处理特殊类型
        if isinstance(value, (datetime, date)):
            value = value.isoformat()
        elif isinstance(value, PyUUID):
            value = str(value)
        result[column.name] = value
    return result


def _cache_worldview_data(cache_key: str, data, ttl: int = 300):
    """
    缓存世界观数据 (默认TTL=300秒，即5分钟)

    🔧 2025-12-02: P0修复 - 改进序列化处理
    - 添加 SQLAlchemy ORM 对象处理（Setting/AIGuidelines）
    - 添加空列表处理
    - 添加Pydantic v1/v2兼容性
    - 添加异常处理
    """
    if not redis_client.is_available():
        return

    try:
        # 🔧 P0修复: 处理 SQLAlchemy ORM 对象（检查 __table__ 属性）
        if hasattr(data, '__table__'):
            data = _orm_to_dict(data)
        # 处理Pydantic对象序列化
        elif hasattr(data, 'model_dump'):
            # Pydantic v2
            data = data.model_dump()
        elif hasattr(data, 'dict'):
            # Pydantic v1
            data = data.dict()
        elif isinstance(data, list):
            if not data:
                # 空列表直接缓存
                pass
            elif hasattr(data[0], '__table__'):
                # 🔧 P0修复: SQLAlchemy ORM 对象列表
                data = [_orm_to_dict(item) for item in data]
            elif hasattr(data[0], 'model_dump'):
                # Pydantic v2 列表
                data = [item.model_dump() for item in data]
            elif hasattr(data[0], 'dict'):
                # Pydantic v1 列表
                data = [item.dict() for item in data]

        success = redis_client.set_json(cache_key, data, expire=ttl)
        if success:
            logger.info(f"💾 [Worldview] 缓存已保存: {cache_key} (expire={ttl}s)")
        else:
            logger.warning(f"⚠️ [Worldview] 缓存保存失败: {cache_key}")

    except Exception as e:
        logger.error(f"⚠️ [Worldview] 缓存序列化失败: {cache_key}, error={e}", exc_info=True)


def _invalidate_worldview_cache(work_id: str, cache_types: list):
    """
    失效指定作品的世界观缓存

    Args:
        work_id: 作品ID
        cache_types: 需要失效的缓存类型列表，如 ['characters', 'locations']

    🔧 2025-12-02: Review修复 - 自动失效worlddata聚合缓存
    当失效characters/locations/settings/guidelines时，自动失效worlddata缓存
    """
    if not redis_client.is_available():
        return

    # 失效指定的缓存类型
    for cache_type in cache_types:
        cache_key = f"worldview:{cache_type}:{work_id}"
        try:
            redis_client.client.delete(cache_key)
            logger.info(f"🗑️ [Worldview] 缓存已失效: {cache_key}")
        except Exception as e:
            logger.error(f"⚠️ [Worldview] 缓存失效失败: {cache_key}, error={e}")

    # 🔧 Review修复: 如果失效的是worlddata的组成部分，自动失效worlddata聚合缓存
    worlddata_components = {'characters', 'locations', 'settings', 'guidelines'}
    if any(cache_type in worlddata_components for cache_type in cache_types):
        worlddata_key = f"worldview:worlddata:{work_id}"
        try:
            redis_client.client.delete(worlddata_key)
            logger.info(f"🗑️ [Worldview] 聚合缓存已失效: {worlddata_key}")
        except Exception as e:
            logger.error(f"⚠️ [Worldview] 聚合缓存失效失败: {worlddata_key}, error={e}")


async def _preheat_worldview_cache(work_id: str, cache_type: str, worldview_service: WorldviewService):
    """
    P1修复: 缓存预热 - 失效后立即重新加载并缓存最新数据

    解决并发请求导致的缓存未命中问题：
    - 请求A创建数据 → 失效缓存 → 预热缓存（最新数据）
    - 请求B读取 → 命中预热后的缓存

    Args:
        work_id: 作品ID
        cache_type: 缓存类型 (characters, locations, settings, guidelines)
        worldview_service: WorldviewService实例
    """
    if not redis_client.is_available():
        return

    try:
        cache_key = f"worldview:{cache_type}:{work_id}"

        # 根据类型加载最新数据
        if cache_type == 'characters':
            data = await worldview_service.get_characters_by_work(work_id)
        elif cache_type == 'locations':
            data = await worldview_service.get_locations_by_work(work_id)
        elif cache_type == 'settings':
            data = await worldview_service.get_settings_by_work(work_id)
        elif cache_type == 'guidelines':
            data = await worldview_service.get_guidelines_by_work(work_id)
        else:
            logger.warning(f"⚠️ [Worldview] 未知的缓存类型: {cache_type}")
            return

        # 缓存最新数据
        _cache_worldview_data(cache_key, data)
        logger.info(f"🔥 [Worldview] 缓存预热完成: {cache_key}")

    except Exception as e:
        logger.error(f"⚠️ [Worldview] 缓存预热失败: {cache_type}, error={e}")


# ==================== 辅助函数：自动从AI规范提取数据到世界观各标签 ====================

async def _auto_populate_worldview_from_guidelines(
    work_id: str,
    guidelines_data: AIGuidelinesUpdate,
    worldview_service: WorldviewService,
    db: AsyncSession,  # 2025-12-01: 添加db参数以支持成本追踪
    user_id: str  # 2025-12-01: 添加user_id参数以支持成本追踪
):
    """从AI规范自动提取并创建人物、地点、设定"""
    
    # 1. 创建主角人物
    if guidelines_data.protagonist_name:
        character_data = CharacterCreate(
            work_id=work_id,
            name=guidelines_data.protagonist_name or "主角",
            description=f"{guidelines_data.protagonist_identity or ''}\n\n性格：{guidelines_data.protagonist_traits or ''}\n\n目标：{guidelines_data.protagonist_goal or ''}".strip(),
            role="主角"
        )
        try:
            await worldview_service.create_character(character_data)
            logger.info(f"[自动创建] 主角人物: {guidelines_data.protagonist_name}")
        except Exception as e:
            logger.error(f"创建主角人物失败: {e}", exc_info=True)
    
    # 2. 解析并创建地点
    if guidelines_data.main_locations:
        locations_text = guidelines_data.main_locations
        # 按顿号、分号、逗号分割
        location_names = [loc.strip() for loc in locations_text.replace('、', ',').replace('；', ',').replace(';', ',').split(',') if loc.strip()]
        
        for loc_name in location_names[:10]:  # 最多创建10个地点
            location_data = LocationCreate(
                work_id=work_id,
                name=loc_name,
                description=f"来自AI生成的主要场景",
                type="场景"  # 注意：Schema字段是type不是location_type
            )
            try:
                await worldview_service.create_location(location_data)
                logger.info(f"[自动创建] 地点: {loc_name}")
            except Exception as e:
                logger.error(f"创建地点失败 {loc_name}: {e}", exc_info=True)
    
    # 3. 创建设定卡片
    settings_to_create = []
    
    # 力量体系
    if guidelines_data.power_system_name:
        settings_to_create.append({
            "name": guidelines_data.power_system_name,
            "content": f"等级划分：{guidelines_data.power_levels or ''}\n\n代价限制：{guidelines_data.power_cost or ''}".strip(),
            "category": "力量体系"
        })
    
    # 世界规则
    if guidelines_data.world_rules:
        settings_to_create.append({
            "name": "世界规则",
            "content": guidelines_data.world_rules,
            "category": "世界观设定"
        })
    
    # 世界观简介
    if guidelines_data.world_intro:
        settings_to_create.append({
            "name": "世界观简介",
            "content": guidelines_data.world_intro,
            "category": "世界观设定"
        })
    
    # 冲突设计
    if guidelines_data.conflict_design:
        settings_to_create.append({
            "name": "冲突设计",
            "content": guidelines_data.conflict_design,
            "category": "剧情设定"
        })
    
    for setting_info in settings_to_create:
        setting_data = SettingCreate(
            work_id=work_id,
            title=setting_info["name"],  # 注意：Schema字段是title不是name
            content=setting_info["content"],
            category=setting_info["category"]
        )
        try:
            await worldview_service.create_setting(setting_data)
            logger.info(f"[自动创建] 设定: {setting_info['name']}")
        except Exception as e:
            logger.error(f"创建设定失败 {setting_info['name']}: {e}")
    
    # 4. 创建作品规范（WorkGuidelines）
    # 小说类型与题材
    outline_parts = []
    if guidelines_data.primary_genre or guidelines_data.secondary_tags:
        outline_parts.append("## 小说类型与题材\n")
        if guidelines_data.primary_genre:
            outline_parts.append(f"**一级类型**：{guidelines_data.primary_genre}\n")
        if guidelines_data.secondary_tags:
            outline_parts.append(f"**二级标签**：{guidelines_data.secondary_tags}\n")
        if guidelines_data.creative_tone:
            outline_parts.append(f"**创作基调**：{guidelines_data.creative_tone}\n")
    
    # 剧情构思
    notes_parts = []
    if guidelines_data.act_one or guidelines_data.act_two or guidelines_data.act_three:
        notes_parts.append("## 剧情构思\n")
        if guidelines_data.act_one:
            notes_parts.append(f"**第一幕**\n{guidelines_data.act_one}\n\n")
        if guidelines_data.act_two:
            notes_parts.append(f"**第二幕**\n{guidelines_data.act_two}\n\n")
        if guidelines_data.act_three:
            notes_parts.append(f"**第三幕**\n{guidelines_data.act_three}\n\n")
    
    if outline_parts or notes_parts:
        work_guidelines_data = WorkGuidelinesCreate(
            work_id=work_id,
            outline="\n".join(outline_parts).strip() if outline_parts else None,
            notes="\n".join(notes_parts).strip() if notes_parts else None,
            tone=guidelines_data.creative_tone,
            target_audience=guidelines_data.target_audience,
            main_theme=guidelines_data.primary_genre
        )
        try:
            await worldview_service.create_or_update_guidelines(work_id, work_guidelines_data)
            logger.info(f"[自动创建] 作品规范（类型题材+剧情构思）")
        except Exception as e:
            logger.error(f"创建作品规范失败: {e}", exc_info=True)


# ==================== 世界观数据聚合接口 ====================

@router.get("/works/{work_id}/worlddata", response_model=WorldDataResponse)
async def get_world_data(
    work_id: str,
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db)
):
    """
    获取作品的完整世界观数据（聚合端点）

    包含：角色、地点、设定、作品规范
    带Redis缓存，TTL=300秒
    """
    # 🔧 2025-12-02: Review修复 - 先验证权限（安全第一）
    work_service = WorkService(db)
    work = await work_service.get_work_by_id(work_id)
    if not work:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Work not found")
    if str(work.author_id) != str(current_user.id):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized")

    # 🔧 2025-12-02: Review修复 - 添加缓存（性能优化）
    cache_key = f"worldview:worlddata:{work_id}"
    cached = _get_cached_worldview_data(cache_key)
    if cached:
        return WorldDataResponse(**cached)

    # 获取世界观数据（4次数据库查询）
    worldview_service = WorldviewService(db)
    characters = await worldview_service.get_characters_by_work(work_id)
    locations = await worldview_service.get_locations_by_work(work_id)
    settings = await worldview_service.get_settings_by_work(work_id)
    guidelines = await worldview_service.get_guidelines_by_work(work_id)

    response = WorldDataResponse(
        characters=characters,
        locations=locations,
        settings=settings,
        guidelines=guidelines
    )

    # 缓存聚合结果
    _cache_worldview_data(cache_key, response)

    return response


# ==================== Character（人物） 接口 ====================

@router.get("/works/{work_id}/characters", response_model=List[CharacterResponse])
async def get_characters(
    work_id: str,
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db)
):
    """获取作品的所有人物 (带Redis缓存，TTL=300秒)"""
    # 🔧 2025-12-02: P0修复 - 先验证权限，再检查缓存
    # 1. 先验证作品权限（防止权限绕过漏洞）
    work_service = WorkService(db)
    work = await work_service.get_work_by_id(work_id)
    if not work:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Work not found")
    if str(work.author_id) != str(current_user.id):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized")

    # 2. 权限验证通过后，检查缓存
    cache_key = f"worldview:characters:{work_id}"
    cached = _get_cached_worldview_data(cache_key)
    if cached:
        return [CharacterResponse(**item) for item in cached]

    # 3. 缓存未命中，查询数据库
    worldview_service = WorldviewService(db)
    characters = await worldview_service.get_characters_by_work(work_id)

    # 4. 缓存结果
    _cache_worldview_data(cache_key, characters)
    return characters


@router.post("/characters", response_model=CharacterResponse, status_code=status.HTTP_201_CREATED)
async def create_character(
    character_data: CharacterCreate,
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db)
):
    """创建人物"""
    # 验证作品权限
    work_service = WorkService(db)
    work = await work_service.get_work_by_id(character_data.work_id)
    if not work:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Work not found")
    if str(work.author_id) != str(current_user.id):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized")

    worldview_service = WorldviewService(db)
    result = await worldview_service.create_character(character_data)

    # 🔧 2025-12-02: P1修复 - 失效缓存 + 预热
    _invalidate_worldview_cache(character_data.work_id, ['characters'])
    await _preheat_worldview_cache(str(character_data.work_id), 'characters', worldview_service)

    return result


@router.put("/characters/{character_id}", response_model=CharacterResponse)
async def update_character(
    character_id: str,
    character_data: CharacterUpdate,
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db)
):
    """更新人物"""
    worldview_service = WorldviewService(db)
    character = await worldview_service.get_character_by_id(character_id)
    if not character:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Character not found")

    # 验证作品权限
    work_service = WorkService(db)
    work = await work_service.get_work_by_id(str(character.work_id))
    if str(work.author_id) != str(current_user.id):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized")

    updated = await worldview_service.update_character(character_id, character_data)

    # 🔧 2025-12-02: P1修复 - 失效缓存 + 预热
    _invalidate_worldview_cache(str(character.work_id), ['characters'])
    await _preheat_worldview_cache(str(character.work_id), 'characters', worldview_service)

    return updated


@router.delete("/characters/{character_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_character(
    character_id: str,
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db)
):
    """删除人物"""
    worldview_service = WorldviewService(db)
    character = await worldview_service.get_character_by_id(character_id)
    if not character:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Character not found")

    # 验证作品权限
    work_service = WorkService(db)
    work = await work_service.get_work_by_id(str(character.work_id))
    if str(work.author_id) != str(current_user.id):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized")

    work_id = str(character.work_id)
    await worldview_service.delete_character(character_id)

    # 🔧 2025-12-02: P0修复 - 失效缓存
    _invalidate_worldview_cache(work_id, ['characters'])


# ==================== Location（地点） 接口 ====================

@router.get("/works/{work_id}/locations", response_model=List[LocationResponse])
async def get_locations(
    work_id: str,
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db)
):
    """获取作品的所有地点 (带Redis缓存，TTL=300秒)"""
    # 🔧 2025-12-02: P0修复 - 先验证权限，再检查缓存
    # 1. 先验证作品权限（防止权限绕过漏洞）
    work_service = WorkService(db)
    work = await work_service.get_work_by_id(work_id)
    if not work:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Work not found")
    if str(work.author_id) != str(current_user.id):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized")

    # 2. 权限验证通过后，检查缓存
    cache_key = f"worldview:locations:{work_id}"
    cached = _get_cached_worldview_data(cache_key)
    if cached:
        return [LocationResponse(**item) for item in cached]

    # 3. 缓存未命中，查询数据库
    worldview_service = WorldviewService(db)
    locations = await worldview_service.get_locations_by_work(work_id)

    # 4. 缓存结果
    _cache_worldview_data(cache_key, locations)
    return locations


@router.post("/locations", response_model=LocationResponse, status_code=status.HTTP_201_CREATED)
async def create_location(
    location_data: LocationCreate,
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db)
):
    """创建地点"""
    # 验证作品权限
    work_service = WorkService(db)
    work = await work_service.get_work_by_id(location_data.work_id)
    if not work:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Work not found")
    if str(work.author_id) != str(current_user.id):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized")

    worldview_service = WorldviewService(db)
    result = await worldview_service.create_location(location_data)

    # 🔧 2025-12-02: P1修复 - 失效缓存 + 预热
    _invalidate_worldview_cache(location_data.work_id, ['locations'])
    await _preheat_worldview_cache(str(location_data.work_id), 'locations', worldview_service)

    return result


@router.put("/locations/{location_id}", response_model=LocationResponse)
async def update_location(
    location_id: str,
    location_data: LocationUpdate,
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db)
):
    """更新地点"""
    worldview_service = WorldviewService(db)
    location = await worldview_service.get_location_by_id(location_id)
    if not location:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Location not found")

    # 验证作品权限
    work_service = WorkService(db)
    work = await work_service.get_work_by_id(str(location.work_id))
    if str(work.author_id) != str(current_user.id):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized")

    updated = await worldview_service.update_location(location_id, location_data)

    # 🔧 2025-12-02: P1修复 - 失效缓存 + 预热
    _invalidate_worldview_cache(str(location.work_id), ['locations'])
    await _preheat_worldview_cache(str(location.work_id), 'locations', worldview_service)

    return updated


@router.delete("/locations/{location_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_location(
    location_id: str,
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db)
):
    """删除地点"""
    worldview_service = WorldviewService(db)
    location = await worldview_service.get_location_by_id(location_id)
    if not location:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Location not found")

    # 验证作品权限
    work_service = WorkService(db)
    work = await work_service.get_work_by_id(str(location.work_id))
    if str(work.author_id) != str(current_user.id):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized")

    work_id = str(location.work_id)
    await worldview_service.delete_location(location_id)

    # 🔧 2025-12-02: P0修复 - 失效缓存
    _invalidate_worldview_cache(work_id, ['locations'])


# ==================== Setting（设定） 接口 ====================

@router.get("/works/{work_id}/settings", response_model=List[SettingResponse])
async def get_settings(
    work_id: str,
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db)
):
    """获取作品的所有设定 (带Redis缓存，TTL=300秒)"""
    # 🔧 2025-12-02: P0修复 - 先验证权限，再检查缓存
    # 1. 先验证作品权限（防止权限绕过漏洞）
    work_service = WorkService(db)
    work = await work_service.get_work_by_id(work_id)
    if not work:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Work not found")
    if str(work.author_id) != str(current_user.id):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized")

    # 2. 权限验证通过后，检查缓存
    cache_key = f"worldview:settings:{work_id}"
    cached = _get_cached_worldview_data(cache_key)
    if cached:
        return [SettingResponse(**item) for item in cached]

    # 3. 缓存未命中，查询数据库
    worldview_service = WorldviewService(db)
    settings = await worldview_service.get_settings_by_work(work_id)

    # 4. 缓存结果
    _cache_worldview_data(cache_key, settings)
    return settings


@router.post("/settings", response_model=SettingResponse, status_code=status.HTTP_201_CREATED)
async def create_setting(
    setting_data: SettingCreate,
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db)
):
    """创建设定"""
    # 验证作品权限
    work_service = WorkService(db)
    work = await work_service.get_work_by_id(setting_data.work_id)
    if not work:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Work not found")
    if str(work.author_id) != str(current_user.id):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized")

    worldview_service = WorldviewService(db)
    result = await worldview_service.create_setting(setting_data)

    # 🔧 2025-12-02: P1修复 - 失效缓存 + 预热
    _invalidate_worldview_cache(setting_data.work_id, ['settings'])
    await _preheat_worldview_cache(str(setting_data.work_id), 'settings', worldview_service)

    return result


@router.put("/settings/{setting_id}", response_model=SettingResponse)
async def update_setting(
    setting_id: str,
    setting_data: SettingUpdate,
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db)
):
    """更新设定"""
    worldview_service = WorldviewService(db)
    setting = await worldview_service.get_setting_by_id(setting_id)
    if not setting:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Setting not found")

    # 验证作品权限
    work_service = WorkService(db)
    work = await work_service.get_work_by_id(str(setting.work_id))
    if str(work.author_id) != str(current_user.id):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized")

    updated = await worldview_service.update_setting(setting_id, setting_data)

    # 🔧 2025-12-02: P1修复 - 失效缓存 + 预热
    _invalidate_worldview_cache(str(setting.work_id), ['settings'])
    await _preheat_worldview_cache(str(setting.work_id), 'settings', worldview_service)

    return updated


@router.delete("/settings/{setting_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_setting(
    setting_id: str,
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db)
):
    """删除设定"""
    worldview_service = WorldviewService(db)
    setting = await worldview_service.get_setting_by_id(setting_id)
    if not setting:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Setting not found")

    # 验证作品权限
    work_service = WorkService(db)
    work = await work_service.get_work_by_id(str(setting.work_id))
    if str(work.author_id) != str(current_user.id):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized")

    work_id = str(setting.work_id)
    await worldview_service.delete_setting(setting_id)

    # 🔧 2025-12-02: P0修复 - 失效缓存
    _invalidate_worldview_cache(work_id, ['settings'])


# ==================== WorkGuidelines（作品规范） 接口 ====================

@router.get("/works/{work_id}/guidelines", response_model=WorkGuidelinesResponse)
async def get_guidelines(
    work_id: str,
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db)
):
    """获取作品规范 (带Redis缓存，TTL=300秒)"""
    # 🔧 2025-12-02: P0修复 - 先验证权限，再检查缓存
    # 1. 先验证作品权限（防止权限绕过漏洞）
    work_service = WorkService(db)
    work = await work_service.get_work_by_id(work_id)
    if not work:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Work not found")
    if str(work.author_id) != str(current_user.id):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized")

    # 2. 权限验证通过后，检查缓存
    cache_key = f"worldview:guidelines:{work_id}"
    cached = _get_cached_worldview_data(cache_key)
    if cached:
        return WorkGuidelinesResponse(**cached)

    # 3. 缓存未命中，查询数据库
    worldview_service = WorldviewService(db)
    guidelines = await worldview_service.get_guidelines_by_work(work_id)
    if not guidelines:
        # 返回默认的空guidelines而不是404
        from datetime import datetime
        from uuid import uuid4
        now = datetime.now()
        result = WorkGuidelinesResponse(
            id=uuid4(),  # 生成新的UUID作为临时ID
            work_id=UUID(work_id),
            genre="",
            theme="",
            background="",
            plot_outline="",
            main_conflict="",
            tone="",
            target_audience="",
            narrative_style="",
            pacing="",
            point_of_view="",
            setting_description="",
            world_rules="",
            magic_system="",
            technology_level="",
            cultural_elements="",
            created_at=now,
            updated_at=now
        )
        # 缓存默认响应
        _cache_worldview_data(cache_key, result)
        return result

    # 4. 缓存结果
    _cache_worldview_data(cache_key, guidelines)
    return guidelines


@router.post("/works/{work_id}/guidelines", response_model=WorkGuidelinesResponse, status_code=status.HTTP_201_CREATED)
async def create_or_update_guidelines(
    work_id: str,
    guidelines_data: WorkGuidelinesUpdate,
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db)
):
    """创建或更新作品规范"""
    # 验证作品权限
    work_service = WorkService(db)
    work = await work_service.get_work_by_id(work_id)
    if not work:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Work not found")
    if str(work.author_id) != str(current_user.id):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized")

    worldview_service = WorldviewService(db)
    result = await worldview_service.create_or_update_guidelines(work_id, guidelines_data)

    # 🔧 2025-12-02: P1修复 - 失效缓存 + 预热
    _invalidate_worldview_cache(work_id, ['guidelines'])
    await _preheat_worldview_cache(str(work_id), 'guidelines', worldview_service)

    return result


@router.delete("/works/{work_id}/guidelines", status_code=status.HTTP_204_NO_CONTENT)
async def delete_guidelines(
    work_id: str,
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db)
):
    """删除作品规范"""
    # 验证作品权限
    work_service = WorkService(db)
    work = await work_service.get_work_by_id(work_id)
    if not work:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Work not found")
    if str(work.author_id) != str(current_user.id):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized")

    worldview_service = WorldviewService(db)
    await worldview_service.delete_guidelines(work_id)

    # 🔧 2025-12-02: P0修复 - 失效缓存
    _invalidate_worldview_cache(work_id, ['guidelines'])


# ==================== AI创作规范 ====================

@router.get("/works/{work_id}/ai-guidelines", response_model=AIGuidelinesResponse)
async def get_ai_guidelines(
    work_id: str,
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db)
):
    """获取AI创作规范 (带Redis缓存，TTL=300秒)"""
    # 🔧 2025-12-02: P0修复 - 先验证权限，再检查缓存
    # 1. 先验证作品权限（防止权限绕过漏洞）
    work_service = WorkService(db)
    work = await work_service.get_work_by_id(work_id)
    if not work:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Work not found")
    if str(work.author_id) != str(current_user.id):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized")

    # 2. 权限验证通过后，检查缓存
    cache_key = f"worldview:ai-guidelines:{work_id}"
    cached = _get_cached_worldview_data(cache_key)
    if cached:
        return AIGuidelinesResponse(**cached)

    # 3. 缓存未命中，查询数据库
    ai_service = AIGuidelinesService(db)
    # 将 str 转换为 UUID
    work_uuid = UUID(work_id)
    guidelines = await ai_service.get_by_work_id(work_uuid)

    if not guidelines:
        # 返回默认的空ai-guidelines而不是404
        from datetime import datetime
        from uuid import uuid4
        now = datetime.now()
        result = AIGuidelinesResponse(
            id=uuid4(),  # 生成新的UUID作为临时ID
            work_id=work_uuid,
            business_goal="",
            target_audience="",
            commercial_benchmark="",
            high_concept="",
            core_paradox="",
            dominant_emotion="",
            core_ip_symbols="",
            protagonist_arc="",
            core_conflict="",
            narrative_rhythm="",
            writing_style="",
            style_notes="",
            chapter_length="",
            content_taboos="",
            primary_genre="",
            secondary_tags="",
            creative_tone="",
            world_intro="",
            main_locations="",
            world_rules="",
            power_system_name="",
            power_levels="",
            power_cost="",
            protagonist_name="",
            protagonist_identity="",
            protagonist_traits="",
            protagonist_goal="",
            conflict_design="",
            act_one="",
            act_two="",
            act_three="",
            is_active=True,
            created_at=now,
            updated_at=now
        )
        # 缓存默认响应
        _cache_worldview_data(cache_key, result)
        return result

    # 4. 缓存结果
    _cache_worldview_data(cache_key, guidelines)
    return guidelines


@router.post("/works/{work_id}/ai-guidelines", response_model=AIGuidelinesResponse, status_code=status.HTTP_201_CREATED)
async def create_or_update_ai_guidelines(
    work_id: str,
    guidelines_data: AIGuidelinesUpdate,
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db)
):
    """创建或更新AI创作规范，并自动将数据分散到人物/地点/设定列表"""
    work_service = WorkService(db)
    work = await work_service.get_work_by_id(work_id)
    if not work:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Work not found")
    if str(work.author_id) != str(current_user.id):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized")

    ai_service = AIGuidelinesService(db)
    worldview_service = WorldviewService(db)

    # 将 str 转换为 UUID
    work_uuid = UUID(work_id)

    # 检查是否已存在
    existing = await ai_service.get_by_work_id(work_uuid)
    if existing:
        # 更新
        logger.info(f"[AI Guidelines] 更新 work_id={work_id} 的AI规范")
        result = await ai_service.update(work_uuid, guidelines_data)
    else:
        # 创建
        logger.info(f"[AI Guidelines] 创建 work_id={work_id} 的AI规范")
        create_data = AIGuidelinesCreate(work_id=work_uuid, **guidelines_data.model_dump(exclude_unset=True))
        result = await ai_service.create(create_data)

        # 首次创建时，自动提取数据并创建人物/地点/设定
        # 2025-12-01: 传递db和user_id以支持成本追踪
        await _auto_populate_worldview_from_guidelines(work_id, guidelines_data, worldview_service, db, str(current_user.id))

    # 🔧 2025-12-02: P0修复 - 失效缓存（失效ai-guidelines以及可能被自动填充的相关缓存）
    _invalidate_worldview_cache(work_id, ['ai-guidelines', 'characters', 'locations', 'settings', 'guidelines'])

    return result


@router.delete("/works/{work_id}/ai-guidelines", status_code=status.HTTP_204_NO_CONTENT)
async def delete_ai_guidelines(
    work_id: str,
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db)
):
    """删除AI创作规范"""
    work_service = WorkService(db)
    work = await work_service.get_work_by_id(work_id)
    if not work:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Work not found")
    if str(work.author_id) != str(current_user.id):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized")

    ai_service = AIGuidelinesService(db)
    # 将 str 转换为 UUID
    work_uuid = UUID(work_id)
    await ai_service.delete(work_uuid)

    # 🔧 2025-12-02: P0修复 - 失效缓存
    _invalidate_worldview_cache(work_id, ['ai-guidelines'])


@router.post("/ai-guidelines/generate", response_model=AIGuidelinesGenerateResponse)
async def generate_phase2_content(
    request: AIGuidelinesGenerateRequest,
):
    """
    AI生成阶段二内容
    基于阶段一的15个用户输入，智能生成阶段二的17个核心设定字段
    
    注意：此接口不需要认证，因为它只是AI生成，不涉及用户数据
    """
    from app.services.ai.http_ai_service import HTTPAIService
    import json
    
    # 构建prompt用于AI生成
    prompt = f"""你是一名资深商业IP总策划师。现在需要根据用户提供的创作规范信息，为他们生成完整的小说核心设定。

【用户提供的创作规范（阶段一）】

一、战略定位
- 商业目标：{request.business_goal or '未指定'}
- 目标读者：{request.target_audience or '未指定'}
- 商业对标：{request.commercial_benchmark or '未指定'}
- 高概念卖点：{request.high_concept or '未指定'}

二、IP架构
- 核心悖论/设定：{request.core_paradox or '未指定'}
- 主导情感：{request.dominant_emotion or '未指定'}
- 核心IP符号：{request.core_ip_symbols or '未指定'}

三、叙事引擎
- 主角弧光：{request.protagonist_arc or '未指定'}
- 核心关系冲突：{request.core_conflict or '未指定'}
- 叙事节奏：{request.narrative_rhythm or '未指定'}

四、文字质感
- 文笔风格：{request.writing_style or '未指定'}
- 文风注意事项：{request.style_notes or '未指定'}

五、技术规范
- 章节长度：{request.chapter_length or '未指定'}
- 内容禁忌：{request.content_taboos or '未指定'}

【请你生成以下内容】

请基于上述信息，生成完整的核心设定内容，要求简洁、具体、可执行。请以JSON格式返回，格式如下：

{{
  "primary_genre": "小说一级类型（如：玄幻、都市、武侠等）",
  "secondary_tags": "二级标签（多个标签用顿号分隔）",
  "creative_tone": "创作基调描述",
  "world_intro": "核心世界观简介（100字左右）",
  "main_locations": "主要场景/地点",
  "world_rules": "世界规则",
  "power_system_name": "力量体系名称",
  "power_levels": "等级划分",
  "power_cost": "代价与限制",
  "protagonist_name": "主角姓名/代号",
  "protagonist_identity": "主角身份与背景",
  "protagonist_traits": "主角性格特点",
  "protagonist_goal": "主角终极目标",
  "conflict_design": "冲突设计",
  "act_one": "第一幕剧情",
  "act_two": "第二幕剧情",
  "act_three": "第三幕剧情"
}}

请确保返回的是严格的JSON格式，不要有任何其他解释文字。"""
    
    # 调用AI服务生成内容
    full_response = ""
    try:
        # 2025-12-01: 传递db和user_id以启用成本追踪
        ai_service = HTTPAIService(db=db, user_id=user_id)
        
        # 收集AI流式响应
        async for chunk in ai_service._stream_chat(
            messages=[
                {"role": "system", "content": "你是一名资深商业IP总策划师。请根据用户提供的信息，生成小说核心设定，以JSON格式返回。"},
                {"role": "user", "content": prompt}
            ],
            max_tokens=2000,
            temperature=0.7,
            task_type=TaskType.CONTENT_CREATION  # ✅ 新增：AI设定生成属于内容创作
        ):
            full_response += chunk
        
        logger.info(f"AI生成的原始响应: {full_response[:500]}...")
        
        # 尝试提取JSON
        # 查找JSON代码块
        json_start = full_response.find('{')
        json_end = full_response.rfind('}') + 1
        
        if json_start >= 0 and json_end > json_start:
            json_str = full_response[json_start:json_end]
            generated_data = json.loads(json_str)
            
            # 构建响应
            response = AIGuidelinesGenerateResponse(**generated_data)
            logger.info(f"AI生成成功，生成的类型: {response.primary_genre}")
            return response
        else:
            logger.error(f"无法从AI响应中提取JSON: {full_response[:200]}")
            raise ValueError("AI返回的内容不是有效的JSON格式")
            
    except json.JSONDecodeError as e:
        logger.error(f"JSON解析失败: {e}, 响应内容: {full_response[:500] if full_response else 'N/A'}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"AI生成的内容格式错误: {str(e)}"
        )
    except Exception as e:
        logger.error(f"AI生成失败: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"AI生成失败: {str(e)}"
        )
