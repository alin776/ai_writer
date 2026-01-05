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
from app.models.character import Character
from app.models.location import Location
from app.models.setting import Setting
from app.schemas.worldview import (
    CharacterCreate, CharacterUpdate, CharacterResponse,
    LocationCreate, LocationUpdate, LocationResponse,
    SettingCreate, SettingUpdate, SettingResponse,
    WorkGuidelinesCreate, WorkGuidelinesUpdate, WorkGuidelinesResponse,
    WorldDataResponse,
    # 世界观同步相关
    WorldviewChangesResponse, ExtractChangesRequest, ScanChangesRequest,
    ApplyChangesRequest, ApplyChangesResponse
)
from app.services.worldview_service import WorldviewService
from app.services.ai_guidelines_service import AIGuidelinesService
from app.schemas.ai_guidelines import (
    AIGuidelinesCreate, AIGuidelinesUpdate, AIGuidelinesResponse,
    AIGuidelinesGenerateRequest, AIGuidelinesGenerateResponse
)
from app.services.work_service import WorkService
from app.services.agent.model_selector import TaskType  # ✅ 新增：用于成本追踪
from app.utils.datetime_utils import get_utc_now

router = APIRouter()
logger = logging.getLogger(__name__)


# ==================== 辅助函数：缓存处理 ====================

def _get_cached_worldview_data(cache_key: str, log_miss: bool = True):
    """
    尝试从缓存获取世界观数据

    Args:
        cache_key: 缓存键
        log_miss: 是否记录未命中日志（并发场景下可设为False减少噪音）
    """
    if redis_client.is_available():
        cached = redis_client.get_json(cache_key)
        if cached:
            logger.info(f"✅ [Worldview] 缓存命中: {cache_key}")
            return cached
        if log_miss:
            logger.debug(f"[Worldview] 缓存未命中: {cache_key}")  # 改为debug级别
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
    db: AsyncSession,
    user_id: str
):
    """
    从AI规范自动提取并创建人物、地点、设定卡片
    优化版：充分解析AI生成的详细内容，生成更丰富的卡片
    """
    from sqlalchemy import select
    from uuid import UUID
    import re

    work_uuid = UUID(work_id)

    # ════════════════════════════════════════════════════════════════
    # 1. 创建主角人物卡片（详细版）
    # ════════════════════════════════════════════════════════════════
    if guidelines_data.protagonist_name:
        exists_stmt = select(Character.id).where(
            Character.work_id == work_uuid,
            Character.name == guidelines_data.protagonist_name
        )
        exists_result = await db.execute(exists_stmt)
        if not exists_result.scalar_one_or_none():
            # 构建详细的人物描述
            desc_parts = []

            if guidelines_data.protagonist_identity:
                desc_parts.append(f"【身份背景】\n{guidelines_data.protagonist_identity}")

            if guidelines_data.protagonist_traits:
                desc_parts.append(f"【性格特点】\n{guidelines_data.protagonist_traits}")

            if guidelines_data.protagonist_goal:
                desc_parts.append(f"【目标追求】\n{guidelines_data.protagonist_goal}")

            character_data = CharacterCreate(
                work_id=work_id,
                name=guidelines_data.protagonist_name,
                description="\n\n".join(desc_parts) if desc_parts else "主角",
                role="主角",
                tags=["主角", "核心人物"]
            )
            try:
                await worldview_service.create_character(character_data)
                logger.info(f"[自动创建] 主角人物: {guidelines_data.protagonist_name}")
            except Exception as e:
                logger.error(f"创建主角人物失败: {e}", exc_info=True)

    # ════════════════════════════════════════════════════════════════
    # 2. 解析并创建地点卡片（智能解析格式）
    # ════════════════════════════════════════════════════════════════
    if guidelines_data.main_locations:
        locations_text = guidelines_data.main_locations

        # 尝试解析新格式：【场景名】类型 | 特色描述 | 氛围关键词
        # 按换行分割
        location_lines = [line.strip() for line in locations_text.split('\n') if line.strip()]

        for line in location_lines[:10]:  # 最多创建10个地点
            # 尝试解析【】格式
            match = re.match(r'【(.+?)】(.+)', line)
            if match:
                loc_name = match.group(1).strip()
                loc_detail = match.group(2).strip()

                # 进一步解析 | 分隔的内容
                parts = [p.strip() for p in loc_detail.split('|')]
                loc_type = parts[0] if len(parts) > 0 else "场景"
                loc_desc = parts[1] if len(parts) > 1 else loc_detail
                loc_atmosphere = parts[2] if len(parts) > 2 else ""

                full_desc = loc_desc
                if loc_atmosphere:
                    full_desc += f"\n\n氛围：{loc_atmosphere}"
            else:
                # 回退到旧逻辑：按顿号、分号、逗号分割
                loc_names_simple = [loc.strip() for loc in line.replace('、', ',').replace('；', ',').replace(';', ',').split(',') if loc.strip()]
                for loc_name in loc_names_simple:
                    exists_stmt = select(Location.id).where(
                        Location.work_id == work_uuid,
                        Location.name == loc_name
                    )
                    exists_result = await db.execute(exists_stmt)
                    if exists_result.scalar_one_or_none():
                        continue

                    location_data = LocationCreate(
                        work_id=work_id,
                        name=loc_name,
                        description="AI生成的主要场景",
                        type="场景"
                    )
                    try:
                        await worldview_service.create_location(location_data)
                        logger.info(f"[自动创建] 地点: {loc_name}")
                    except Exception as e:
                        logger.error(f"创建地点失败 {loc_name}: {e}", exc_info=True)
                continue

            # 检查是否已存在
            exists_stmt = select(Location.id).where(
                Location.work_id == work_uuid,
                Location.name == loc_name
            )
            exists_result = await db.execute(exists_stmt)
            if exists_result.scalar_one_or_none():
                continue

            location_data = LocationCreate(
                work_id=work_id,
                name=loc_name,
                description=full_desc,
                type=loc_type
            )
            try:
                await worldview_service.create_location(location_data)
                logger.info(f"[自动创建] 地点: {loc_name} ({loc_type})")
            except Exception as e:
                logger.error(f"创建地点失败 {loc_name}: {e}", exc_info=True)

    # ════════════════════════════════════════════════════════════════
    # 3. 创建设定卡片（更丰富的分类）
    # ════════════════════════════════════════════════════════════════
    settings_to_create = []

    # 力量体系（详细版）
    if guidelines_data.power_system_name:
        power_content_parts = [f"体系名称：{guidelines_data.power_system_name}"]

        if guidelines_data.power_levels:
            power_content_parts.append(f"\n【等级划分】\n{guidelines_data.power_levels}")

        if guidelines_data.power_cost:
            power_content_parts.append(f"\n【代价与限制】\n{guidelines_data.power_cost}")

        settings_to_create.append({
            "name": f"力量体系：{guidelines_data.power_system_name}",
            "content": "\n".join(power_content_parts),
            "category": "力量体系"
        })

    # 世界观简介
    if guidelines_data.world_intro:
        settings_to_create.append({
            "name": "核心世界观",
            "content": guidelines_data.world_intro,
            "category": "世界观设定"
        })

    # 世界规则
    if guidelines_data.world_rules:
        settings_to_create.append({
            "name": "世界规则",
            "content": guidelines_data.world_rules,
            "category": "世界观设定"
        })

    # 创作基调
    if guidelines_data.creative_tone:
        settings_to_create.append({
            "name": "创作基调",
            "content": guidelines_data.creative_tone,
            "category": "写作风格"
        })

    # 冲突设计
    if guidelines_data.conflict_design:
        settings_to_create.append({
            "name": "核心冲突设计",
            "content": guidelines_data.conflict_design,
            "category": "剧情设定"
        })

    # 三幕剧情大纲
    plot_parts = []
    if guidelines_data.act_one:
        plot_parts.append(f"【第一幕：开局与建置】\n{guidelines_data.act_one}")
    if guidelines_data.act_two:
        plot_parts.append(f"【第二幕：冲突与发展】\n{guidelines_data.act_two}")
    if guidelines_data.act_three:
        plot_parts.append(f"【第三幕：高潮与结局】\n{guidelines_data.act_three}")

    if plot_parts:
        settings_to_create.append({
            "name": "三幕剧情大纲",
            "content": "\n\n".join(plot_parts),
            "category": "剧情设定"
        })

    # 批量创建设定卡片
    for setting_info in settings_to_create:
        exists_stmt = select(Setting.id).where(
            Setting.work_id == work_uuid,
            Setting.title == setting_info["name"]
        )
        exists_result = await db.execute(exists_stmt)
        if exists_result.scalar_one_or_none():
            continue

        setting_data = SettingCreate(
            work_id=work_id,
            title=setting_info["name"],
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
        now = get_utc_now()
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
        now = get_utc_now()
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

    # 自动提取数据并创建人物/地点/设定（幂等去重，更新场景下也执行以补足首次缺失的数据）
    try:
        await _auto_populate_worldview_from_guidelines(work_id, guidelines_data, worldview_service, db, str(current_user.id))
    except Exception as e:
        logger.error(f"[AI Guidelines] 自动分发世界观数据失败: {e}", exc_info=True)

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
async def generate_ai_guidelines(
    request: AIGuidelinesGenerateRequest,
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db)
):
    """
    AI生成世界观内容

    支持两种模式：
    1. 🆕 方案C：基于story_concept（故事梗概）生成完整31个字段
    2. 旧版本：基于15个创作规范字段生成17个核心设定字段
    """
    user_id = str(current_user.id)
    from app.services.ai.http_ai_service import HTTPAIService
    import json

    # 🆕 判断使用哪种模式
    if request.story_concept:
        # ========== 方案C：基于故事梗概一键生成完整31字段 ==========
        logger.info(f"[AI Guidelines] 方案C：基于故事梗概生成完整设定")
        prompt = f"""你是一名资深小说策划师。用户提供了一个故事梗概，你需要基于这个梗概，生成**完整且详细**的22个小说创作设定字段。

【用户的故事梗概】
{request.story_concept}

【生成要求】
请以JSON格式返回完整的22个字段：

{{
  // === 核心创作规范（5个字段）===
  "target_audience": "目标读者画像（年龄、性别、阅读偏好，50字左右）",
  "high_concept": "高概念卖点，一句话总结核心吸引力",
  "dominant_emotion": "主导情感体验（如：逆袭的爽感、被理解的慰藉、探索的惊奇等）",
  "writing_style": "文字风格（如：冷峻简洁、华丽诗性、幽默诙谐、平实感人等）",
  "chapter_length": "平均章节字数（如：2000-3000字）",

  // === 小说类型（3个字段）===
  "primary_genre": "一级类型（玄幻/都市/仙侠/科幻/悬疑/言情等）",
  "secondary_tags": "二级标签，用顿号分隔（如：系统流、无敌流、种田文，至少3个）",
  "creative_tone": "创作基调（整体氛围和情感色彩，50字左右）",

  // === 世界背景（3个字段）===
  "world_intro": "核心世界观（200-300字）。包括：①与现实/常规的核心差异 ②基本运行法则 ③普通人生活状态 ④独特吸引点",
  "main_locations": "主要场景（每个50-80字）。格式：【场景名】类型 | 特色 | 氛围，至少3个，换行分隔",
  "world_rules": "世界核心规则（150-200字）。包括：①社会阶层格局 ②资源获取方式 ③普通人上升路径 ④禁忌底线",

  // === 力量体系（3个字段）===
  "power_system_name": "力量体系名称（有独特性，避免通用名）",
  "power_levels": "等级划分。格式：等级名 | 实力 | 能力 | 地位，6-9个等级，换行分隔",
  "power_cost": "力量代价与限制（100-150字）。包括：①获取代价 ②使用限制 ③副作用风险 ④天花板",

  // === 主角设定（4个字段）===
  "protagonist_name": "主角姓名（符合世界观，有寓意更好）",
  "protagonist_identity": "主角身份背景（150-200字）。包括：①出身 ②开局处境 ③与世界观关系 ④特殊之处",
  "protagonist_traits": "主角性格（100-150字）。包括：①3个核心标签 ②形成原因 ③优点 ④缺陷 ⑤标志性行为",
  "protagonist_goal": "主角目标层次（100字）。包括：①表层目标 ②深层目标 ③终极目标",

  // === 剧情构思（4个字段）===
  "conflict_design": "核心冲突（150-200字）。包括：①vs自我 ②vs他人 ③vs世界 ④升级节点",
  "act_one": "第一幕（150-200字）。包括：①开篇钩子 ②日常被打破 ③引出冲突 ④转折点",
  "act_two": "第二幕（200-250字）。包括：①尝试挫折 ②成长阶段 ③配角引入 ④中点转折 ⑤最低谷",
  "act_three": "第三幕（150-200字）。包括：①最终觉悟 ②决战设计 ③结局类型 ④核心表达"
}}

【重要提醒】
1. 所有字段都要**具体详细**，避免泛泛而谈
2. 内容要有**独特性和辨识度**，基于故事梗概深度推演
3. 各字段要**相互呼应**，形成完整体系
4. 返回严格的JSON格式，不要有任何解释文字
5. 所有22个字段都必须填写，不能为空"""

        max_tokens = 6000  # 方案C需要更多token

    else:
        # ========== 旧版本：基于15个字段生成17个字段 ==========
        logger.info(f"[AI Guidelines] 旧版本：基于创作规范生成核心设定")
        prompt = f"""你是一名资深商业IP总策划师和专业小说架构师。现在需要根据用户提供的创作规范，生成**详细且可执行**的小说核心设定。

【用户提供的创作规范】

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

【生成要求】
请以JSON格式返回17个核心设定字段：

{{
  "primary_genre": "一级类型",
  "secondary_tags": "二级标签",
  "creative_tone": "创作基调",
  "world_intro": "核心世界观",
  "main_locations": "主要场景",
  "world_rules": "世界规则",
  "power_system_name": "力量体系名称",
  "power_levels": "等级划分",
  "power_cost": "力量代价",
  "protagonist_name": "主角姓名",
  "protagonist_identity": "主角身份",
  "protagonist_traits": "主角性格",
  "protagonist_goal": "主角目标",
  "conflict_design": "冲突设计",
  "act_one": "第一幕",
  "act_two": "第二幕",
  "act_three": "第三幕"
}}

【重要提醒】
返回严格的JSON格式，不要有任何解释文字"""

        max_tokens = 4000

    # 调用AI服务生成内容
    full_response = ""
    try:
        ai_service = HTTPAIService(db=db, user_id=user_id)

        async for chunk, usage in ai_service._stream_chat(
            messages=[
                {"role": "system", "content": "你是一名资深商业IP总策划师和专业小说架构师。请根据用户提供的信息，生成详细、具体、有独特性的小说设定。必须以严格的JSON格式返回，不要有任何解释文字。"},
                {"role": "user", "content": prompt}
            ],
            max_tokens=max_tokens,
            temperature=0.8,
            task_type=TaskType.CONTENT_CREATION
        ):
            full_response += chunk

        logger.info(f"AI生成的原始响应: {full_response[:500]}...")

        # 提取JSON
        json_start = full_response.find('{')
        json_end = full_response.rfind('}') + 1

        if json_start >= 0 and json_end > json_start:
            json_str = full_response[json_start:json_end]
            generated_data = json.loads(json_str)

            # 构建响应
            response = AIGuidelinesGenerateResponse(**generated_data)
            logger.info(f"AI生成成功，主类型: {response.primary_genre}, 主角: {response.protagonist_name}")
            return response
        else:
            logger.error(f"无法从AI响应中提取JSON: {full_response[:200]}")
            raise ValueError("AI返回的内容不是有效的JSON格式")

    except json.JSONDecodeError as e:
        logger.error(f"JSON解析失败: {e}, 响应内容: {full_response[:500] if full_response else 'N/A'}")
        await db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"AI生成的内容格式错误: {str(e)}"
        )
    except Exception as e:
        logger.error(f"AI生成失败: {e}")
        await db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"AI生成失败: {str(e)}"
        )


# ==================== 世界观同步接口（方案A + 方案C） ====================

@router.post("/works/{work_id}/worldview/extract-changes", response_model=WorldviewChangesResponse)
async def extract_changes_from_chapter(
    work_id: str,
    request: ExtractChangesRequest,
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db)
):
    """
    方案A：从单个章节提取世界观变化

    章节写完后调用此接口，AI 会分析章节内容，提取出新出现的人物、地点、设定等变化。
    返回变化列表供用户确认，不会自动应用。
    """
    from app.services.worldview_sync_service import WorldviewSyncService
    from sqlalchemy import select
    from app.models.chapter import Chapter

    # 验证作品权限
    work_service = WorkService(db)
    work = await work_service.get_work_by_id(work_id)
    if not work:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Work not found")
    if str(work.author_id) != str(current_user.id):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized")

    # 获取章节内容
    chapter_content = request.chapter_content
    if not chapter_content:
        # 从数据库读取章节内容
        chapter_stmt = select(Chapter).where(Chapter.id == request.chapter_id)
        chapter_result = await db.execute(chapter_stmt)
        chapter = chapter_result.scalar_one_or_none()
        if not chapter:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Chapter not found")
        chapter_content = chapter.content or ""

    if len(chapter_content) < 100:
        # 内容太短，返回空结果
        return WorldviewChangesResponse()

    # 调用同步服务提取变化
    sync_service = WorldviewSyncService(db, user_id=str(current_user.id))
    changes = await sync_service.extract_changes_from_chapter(
        work_id=work_id,
        chapter_id=request.chapter_id,
        chapter_content=chapter_content
    )

    logger.info(f"[世界观同步] 从章节 {request.chapter_id} 提取变化完成: "
                f"新人物={len(changes.get('new_characters', []))}, "
                f"新地点={len(changes.get('new_locations', []))}")

    return WorldviewChangesResponse(**changes)


@router.post("/works/{work_id}/worldview/scan-changes", response_model=WorldviewChangesResponse)
async def scan_chapters_for_changes(
    work_id: str,
    request: ScanChangesRequest,
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db)
):
    """
    方案C：批量扫描章节，生成世界观变化报告

    扫描指定范围的章节，综合分析所有内容，提取出与现有世界观相比的新增和变化。
    适用于：写了多章后想一次性同步世界观的场景。
    """
    from app.services.worldview_sync_service import WorldviewSyncService

    # 验证作品权限
    work_service = WorkService(db)
    work = await work_service.get_work_by_id(work_id)
    if not work:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Work not found")
    if str(work.author_id) != str(current_user.id):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized")

    # 调用同步服务批量扫描
    sync_service = WorldviewSyncService(db, user_id=str(current_user.id))
    changes = await sync_service.scan_chapters_for_changes(
        work_id=work_id,
        start_chapter=request.start_chapter,
        end_chapter=request.end_chapter,
        limit=request.limit
    )

    logger.info(f"[世界观同步] 批量扫描完成: 扫描章节数={changes.get('scanned_chapters', 0)}, "
                f"新人物={len(changes.get('new_characters', []))}, "
                f"新地点={len(changes.get('new_locations', []))}")

    return WorldviewChangesResponse(**changes)


@router.post("/works/{work_id}/worldview/apply-changes", response_model=ApplyChangesResponse)
async def apply_worldview_changes(
    work_id: str,
    request: ApplyChangesRequest,
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db)
):
    """
    应用世界观变化到卡片

    将提取出的变化（新人物、新地点、新设定）应用到世界观卡片中。
    支持选择性应用：通过 selected_items 参数指定要应用的项目。
    """
    from app.services.worldview_sync_service import WorldviewSyncService

    # 验证作品权限
    work_service = WorkService(db)
    work = await work_service.get_work_by_id(work_id)
    if not work:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Work not found")
    if str(work.author_id) != str(current_user.id):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized")

    # 将 Pydantic 模型转换为字典
    changes_dict = request.changes.model_dump()

    # 调用同步服务应用变化
    sync_service = WorldviewSyncService(db, user_id=str(current_user.id))
    stats = await sync_service.apply_changes(
        work_id=work_id,
        changes=changes_dict,
        selected_items=request.selected_items
    )

    logger.info(f"[世界观同步] 应用变化完成: {stats}")

    # 失效相关缓存
    _invalidate_worldview_cache(work_id, ['characters', 'locations', 'settings'])

    return ApplyChangesResponse(**stats)
