"""管理后台系统配置 API"""

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from typing import Any

from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.core.security import get_current_admin_user
from app.models.user import User
from app.services.system_config_service import SystemConfigService


router = APIRouter()


class ConfigUpdateRequest(BaseModel):
    """配置更新请求"""
    value: Any


@router.get("/config/{key}")
async def get_config(
    key: str,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_admin_user),
):
    """获取系统配置（仅管理员）"""
    value = await SystemConfigService.get(db, key)
    if value is None:
        raise HTTPException(status_code=404, detail=f"配置项 '{key}' 不存在")
    return {"key": key, "value": value}


@router.put("/config/{key}")
async def update_config(
    key: str,
    body: ConfigUpdateRequest,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_admin_user),
):
    """更新系统配置（仅管理员）"""
    await SystemConfigService.set(db, key, body.value, user_id=current_user.id)
    return {"key": key, "value": body.value}
