"""
管理后台 API

提供系统统计数据、用户管理等功能
"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func, update
from datetime import datetime, timedelta
from typing import List, Optional
from uuid import UUID

from app.core.database import get_db
from app.core.security import get_current_active_user
from app.models.user import User
from app.models.work import Work
from app.models.chapter import Chapter

router = APIRouter()


def check_admin_permission(current_user: User = Depends(get_current_active_user)) -> User:
    """检查是否为管理员"""
    if not current_user.is_admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Admin permission required"
        )
    return current_user


@router.get("/statistics")
async def get_statistics(
    current_user: User = Depends(check_admin_permission),
    db: AsyncSession = Depends(get_db)
):
    """
    获取系统统计数据
    
    返回：
    - 总用户数
    - 总作品数
    - 总章节数
    - 总字数
    - AI 调用次数（暂时返回模拟数据）
    - 总成本（暂时返回模拟数据）
    """
    
    # 统计用户数
    users_count = await db.scalar(select(func.count(User.id)))
    
    # 统计作品数
    works_count = await db.scalar(select(func.count(Work.id)))
    
    # 统计章节数
    chapters_count = await db.scalar(select(func.count(Chapter.id)))
    
    # 统计总字数
    total_words = await db.scalar(select(func.sum(Work.total_words))) or 0
    
    # TODO: AI 调用次数需要从日志表或 Redis 统计
    # 暂时返回模拟数据
    ai_calls_count = 0
    
    # TODO: 总成本需要从成本记录表统计
    # 暂时返回模拟数据
    total_cost = 0
    
    # 计算变化率（与上月对比）
    # TODO: 实现真实的时间范围统计
    # 暂时返回模拟数据
    users_change = "+12.5%"
    works_change = "+8.2%"
    ai_calls_change = "+23.1%"
    cost_change = "-5.3%"
    
    return {
        "users": {
            "total": users_count,
            "change": users_change
        },
        "works": {
            "total": works_count,
            "change": works_change
        },
        "chapters": {
            "total": chapters_count
        },
        "words": {
            "total": total_words
        },
        "ai_calls": {
            "total": ai_calls_count,
            "change": ai_calls_change
        },
        "cost": {
            "total": total_cost,
            "change": cost_change
        }
    }


@router.get("/users-growth")
async def get_users_growth(
    days: int = 7,
    current_user: User = Depends(check_admin_permission),
    db: AsyncSession = Depends(get_db)
):
    """
    获取用户增长趋势数据
    
    Args:
        days: 统计天数（默认7天）
    """
    # TODO: 实现真实的用户增长统计
    # 需要按日期分组统计
    
    # 暂时返回模拟数据
    mock_data = []
    for i in range(days):
        date = (datetime.now() - timedelta(days=days-i-1)).strftime("%m-%d")
        mock_data.append({
            "date": date,
            "users": 820 + i * 50,
            "works": 1200 + i * 200
        })
    
    return {
        "data": mock_data
    }


@router.get("/ai-usage")
async def get_ai_usage(
    current_user: User = Depends(check_admin_permission),
    db: AsyncSession = Depends(get_db)
):
    """
    获取 AI 模型使用统计
    """
    # TODO: 实现真实的 AI 使用统计
    # 需要从日志表或 Redis 统计
    
    # 暂时返回模拟数据
    return {
        "data": [
            {
                "model": "Gemini-2.5-Pro",
                "calls": 0,
                "cost": 0
            }
        ]
    }


@router.get("/recent-activities")
async def get_recent_activities(
    limit: int = 10,
    current_user: User = Depends(check_admin_permission),
    db: AsyncSession = Depends(get_db)
):
    """
    获取最近活动记录
    
    Args:
        limit: 返回记录数量（默认10条）
    """
    # TODO: 实现真实的活动记录
    # 需要从活动日志表查询
    
    # 暂时返回空数组
    return {
        "data": []
    }


# ==================== 用户管理功能 ====================

@router.patch("/users/{user_id}/ban")
async def ban_user(
    user_id: UUID,
    current_user: User = Depends(check_admin_permission),
    db: AsyncSession = Depends(get_db)
):
    """
    封禁用户
    
    Args:
        user_id: 用户ID
    
    Returns:
        封禁成功的消息
    """
    # 查询用户
    user = await db.get(User, user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    # 不能封禁自己
    if user.id == current_user.id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Cannot ban yourself"
        )
    
    # 设置为非激活状态
    user.is_active = False
    await db.commit()
    await db.refresh(user)
    
    return {
        "message": "User banned successfully",
        "user": {
            "id": str(user.id),
            "username": user.username,
            "email": user.email,
            "is_active": user.is_active,
            "is_admin": user.is_admin
        }
    }


@router.patch("/users/{user_id}/unban")
async def unban_user(
    user_id: UUID,
    current_user: User = Depends(check_admin_permission),
    db: AsyncSession = Depends(get_db)
):
    """
    解封用户
    
    Args:
        user_id: 用户ID
    
    Returns:
        解封成功的消息
    """
    # 查询用户
    user = await db.get(User, user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    # 设置为激活状态
    user.is_active = True
    await db.commit()
    await db.refresh(user)
    
    return {
        "message": "User unbanned successfully",
        "user": {
            "id": str(user.id),
            "username": user.username,
            "email": user.email,
            "is_active": user.is_active,
            "is_admin": user.is_admin
        }
    }


@router.patch("/users/{user_id}/toggle-admin")
async def toggle_admin_role(
    user_id: UUID,
    current_user: User = Depends(check_admin_permission),
    db: AsyncSession = Depends(get_db)
):
    """
    切换用户管理员角色
    
    Args:
        user_id: 用户ID
    
    Returns:
        操作成功的消息
    """
    # 查询用户
    user = await db.get(User, user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    # 不能修改自己的角色
    if user.id == current_user.id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Cannot modify your own admin role"
        )
    
    # 切换管理员状态
    user.is_admin = not user.is_admin
    await db.commit()
    await db.refresh(user)
    
    return {
        "message": f"User {'promoted to' if user.is_admin else 'demoted from'} admin successfully",
        "user": {
            "id": str(user.id),
            "username": user.username,
            "email": user.email,
            "is_active": user.is_active,
            "is_admin": user.is_admin
        }
    }
