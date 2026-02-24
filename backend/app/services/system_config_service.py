"""系统配置服务

内存缓存 + DB 持久化，支持定价、汇率等配置的实时修改。
"""

from typing import Any, Optional
from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.system_config import SystemConfig


# 默认定价（无 DB 连接时的 fallback）
_DEFAULT_MODEL_PRICING = {
    "gpt-5.2": {
        "input": 0.875,
        "cached_input": 0.875,
        "output": 7.0,
        "reasoning": 7.0,
        "cache_creation": 0.875,
    },
    "default": {
        "input": 1.0,
        "cached_input": 0.5,
        "output": 2.0,
        "reasoning": 2.0,
        "cache_creation": 1.0,
    },
}

_DEFAULT_CREDITS_PER_DOLLAR = 12400


class SystemConfigService:
    """系统配置服务，内存缓存 + DB 持久化"""

    _cache: dict[str, Any] = {}

    @classmethod
    async def get(cls, db: AsyncSession, key: str, default: Any = None) -> Any:
        """读取配置（优先内存缓存）"""
        if key in cls._cache:
            return cls._cache[key]
        result = await db.execute(
            select(SystemConfig).where(SystemConfig.key == key)
        )
        config = result.scalar_one_or_none()
        if config:
            cls._cache[key] = config.value
            return config.value
        return default

    @classmethod
    async def set(
        cls,
        db: AsyncSession,
        key: str,
        value: Any,
        description: Optional[str] = None,
        user_id: Optional[UUID] = None,
    ) -> None:
        """写入配置（同步刷新缓存）"""
        config = await db.get(SystemConfig, key)
        if config:
            config.value = value
            config.updated_by = user_id
            if description is not None:
                config.description = description
        else:
            config = SystemConfig(
                key=key, value=value, description=description, updated_by=user_id
            )
            db.add(config)
        await db.commit()
        cls._cache[key] = value

    @classmethod
    async def get_model_pricing(cls, db: AsyncSession) -> dict:
        """获取模型定价配置"""
        pricing = await cls.get(db, "model_pricing", default=_DEFAULT_MODEL_PRICING)
        # 始终合并：_DEFAULT_MODEL_PRICING 打底，DB/缓存值覆盖
        # 防止缓存或 DB 只有部分模型键（如只有 "default" 没有 "gpt-5.2"）
        return {**_DEFAULT_MODEL_PRICING, **(pricing or {})}

    @classmethod
    async def get_credits_per_dollar(cls, db: AsyncSession) -> int:
        """获取美元兑积分比例"""
        return await cls.get(db, "credits_per_dollar", default=_DEFAULT_CREDITS_PER_DOLLAR)

    @classmethod
    def invalidate_cache(cls, key: Optional[str] = None) -> None:
        """手动清除缓存（测试用）"""
        if key:
            cls._cache.pop(key, None)
        else:
            cls._cache.clear()
