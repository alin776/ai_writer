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
from app.models.ai_call_log import AICallLog
from app.schemas.admin import UsersGrowthParams, RecentActivitiesParams, UserActionResponse, UserBasicInfo, UpdateUserHonorRequest
from app.utils.datetime_utils import get_utc_now

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

    # 统计 AI 调用次数（从 ai_call_logs 表）
    ai_calls_count = await db.scalar(select(func.count(AICallLog.id))) or 0

    # 统计总成本（从 ai_call_logs 表，单位：美元）
    total_cost = await db.scalar(select(func.sum(AICallLog.total_cost))) or 0.0

    # 计算本月的 AI 调用次数和成本
    current_month_start = get_utc_now().replace(day=1, hour=0, minute=0, second=0, microsecond=0)
    this_month_ai_calls = await db.scalar(
        select(func.count(AICallLog.id)).where(AICallLog.created_at >= current_month_start)
    ) or 0
    this_month_cost = await db.scalar(
        select(func.sum(AICallLog.total_cost)).where(AICallLog.created_at >= current_month_start)
    ) or 0.0

    # 计算上月的 AI 调用次数和成本
    last_month_start = (current_month_start - timedelta(days=1)).replace(day=1)
    last_month_end = current_month_start
    last_month_ai_calls = await db.scalar(
        select(func.count(AICallLog.id)).where(
            AICallLog.created_at >= last_month_start,
            AICallLog.created_at < last_month_end
        )
    ) or 0
    last_month_cost = await db.scalar(
        select(func.sum(AICallLog.total_cost)).where(
            AICallLog.created_at >= last_month_start,
            AICallLog.created_at < last_month_end
        )
    ) or 0.0
    
    # 计算本月的用户数和作品数
    this_month_users = await db.scalar(
        select(func.count(User.id)).where(User.created_at >= current_month_start)
    ) or 0
    this_month_works = await db.scalar(
        select(func.count(Work.id)).where(Work.created_at >= current_month_start)
    ) or 0

    # 计算上月的用户数和作品数
    last_month_users = await db.scalar(
        select(func.count(User.id)).where(
            User.created_at >= last_month_start,
            User.created_at < last_month_end
        )
    ) or 0
    last_month_works = await db.scalar(
        select(func.count(Work.id)).where(
            Work.created_at >= last_month_start,
            Work.created_at < last_month_end
        )
    ) or 0

    # 计算变化率
    def calculate_change(current: int, previous: int) -> str:
        """计算变化率百分比"""
        if previous == 0:
            return "+100%" if current > 0 else "0%"
        change = ((current - previous) / previous) * 100
        sign = "+" if change >= 0 else ""
        return f"{sign}{change:.1f}%"

    users_change = calculate_change(this_month_users, last_month_users)
    works_change = calculate_change(this_month_works, last_month_works)
    ai_calls_change = calculate_change(this_month_ai_calls, last_month_ai_calls)

    # 成本变化率（注意：成本下降是好事）
    if last_month_cost == 0:
        cost_change = "+100%" if this_month_cost > 0 else "0%"
    else:
        cost_change_value = ((this_month_cost - last_month_cost) / last_month_cost) * 100
        sign = "+" if cost_change_value >= 0 else ""
        cost_change = f"{sign}{cost_change_value:.1f}%"
    
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
    params: UsersGrowthParams = Depends(),
    current_user: User = Depends(check_admin_permission),
    db: AsyncSession = Depends(get_db)
):
    """
    获取用户增长趋势数据

    Args:
        params: 查询参数，包含days（统计天数，范围1-90天）

    性能优化：使用GROUP BY一次性查询，从N*2次优化到4次查询
    返回最近N天的数据，包括今天
    """
    days = params.days

    # 计算日期范围：最近days天，包括今天
    # 例如days=7时，统计从6天前到今天，共7天
    now = get_utc_now()
    last_day_start = now.replace(hour=0, minute=0, second=0, microsecond=0)
    first_day_start = last_day_start - timedelta(days=days - 1)

    # 0. 查询first_day_start之前的累计基础值（2次查询）
    base_users_count = await db.scalar(
        select(func.count(User.id)).where(User.created_at < first_day_start)
    ) or 0
    base_works_count = await db.scalar(
        select(func.count(Work.id)).where(Work.created_at < first_day_start)
    ) or 0

    # 1. 一次性查询时间窗口内的用户，按日期分组（1次查询）
    # 查询范围：[first_day_start, 明天0点) - 包括今天一整天
    tomorrow_start = last_day_start + timedelta(days=1)
    users_by_date_result = await db.execute(
        select(
            func.date(User.created_at).label('date'),
            func.count(User.id).label('count')
        )
        .where(User.created_at >= first_day_start)
        .where(User.created_at < tomorrow_start)
        .group_by(func.date(User.created_at))
    )
    users_by_date = {row.date: row.count for row in users_by_date_result}

    # 2. 一次性查询时间窗口内的作品，按日期分组（1次查询）
    works_by_date_result = await db.execute(
        select(
            func.date(Work.created_at).label('date'),
            func.count(Work.id).label('count')
        )
        .where(Work.created_at >= first_day_start)
        .where(Work.created_at < tomorrow_start)
        .group_by(func.date(Work.created_at))
    )
    works_by_date = {row.date: row.count for row in works_by_date_result}

    # 3. 在Python中计算累计值（总计：从N*2次查询优化为4次查询！）
    growth_data = []
    cumulative_users = base_users_count  # 从历史基础值开始
    cumulative_works = base_works_count  # 从历史基础值开始

    for i in range(days):
        target_date = first_day_start + timedelta(days=i)
        target_date_only = target_date.date()

        # 累加该日新增的用户和作品
        cumulative_users += users_by_date.get(target_date_only, 0)
        cumulative_works += works_by_date.get(target_date_only, 0)

        growth_data.append({
            "date": target_date.strftime("%m-%d"),
            "users": cumulative_users,
            "works": cumulative_works
        })

    return {
        "data": growth_data
    }


@router.get("/ai-usage")
async def get_ai_usage(
    current_user: User = Depends(check_admin_permission),
    db: AsyncSession = Depends(get_db)
):
    """
    获取 AI 模型使用统计

    统计每个模型的调用次数和总成本
    """
    # 按模型分组统计
    from sqlalchemy import desc

    results = await db.execute(
        select(
            AICallLog.model_name,
            func.count(AICallLog.id).label('calls'),
            func.sum(AICallLog.total_cost).label('cost')
        )
        .group_by(AICallLog.model_name)
        .order_by(desc('calls'))
    )

    model_stats = []
    for row in results:
        model_stats.append({
            "model": row.model_name,
            "calls": row.calls,
            "cost": float(row.cost) if row.cost else 0.0
        })

    # 如果没有数据,返回空数组
    if not model_stats:
        model_stats = []

    return {
        "data": model_stats
    }


@router.get("/recent-activities")
async def get_recent_activities(
    params: RecentActivitiesParams = Depends(),
    current_user: User = Depends(check_admin_permission),
    db: AsyncSession = Depends(get_db)
):
    """
    获取最近活动记录

    Args:
        params: 查询参数，包含limit（返回记录数量，范围1-100条）
    """
    limit = params.limit
    # TODO: 实现真实的活动记录
    # 需要从活动日志表查询

    # 暂时返回空数组
    return {
        "data": []
    }


# ==================== 用户管理功能 ====================

@router.patch("/users/{user_id}/ban", response_model=UserActionResponse)
async def ban_user(
    user_id: UUID,
    current_user: User = Depends(check_admin_permission),
    db: AsyncSession = Depends(get_db)
) -> UserActionResponse:
    """
    封禁用户

    Args:
        user_id: 用户ID

    Returns:
        封禁成功的消息和用户信息
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

    return UserActionResponse(
        message="User banned successfully",
        user=UserBasicInfo.model_validate(user)
    )


@router.patch("/users/{user_id}/unban", response_model=UserActionResponse)
async def unban_user(
    user_id: UUID,
    current_user: User = Depends(check_admin_permission),
    db: AsyncSession = Depends(get_db)
) -> UserActionResponse:
    """
    解封用户

    Args:
        user_id: 用户ID

    Returns:
        解封成功的消息和用户信息
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

    return UserActionResponse(
        message="User unbanned successfully",
        user=UserBasicInfo.model_validate(user)
    )


@router.patch("/users/{user_id}/toggle-admin", response_model=UserActionResponse)
async def toggle_admin_role(
    user_id: UUID,
    current_user: User = Depends(check_admin_permission),
    db: AsyncSession = Depends(get_db)
) -> UserActionResponse:
    """
    切换用户管理员角色

    Args:
        user_id: 用户ID

    Returns:
        操作成功的消息和用户信息
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

    return UserActionResponse(
        message=f"User {'promoted to' if user.is_admin else 'demoted from'} admin successfully",
        user=UserBasicInfo.model_validate(user)
    )


# ========== 推荐作品管理 ==========


@router.get("/featured-novels")
async def get_featured_novels_admin(
    current_user: User = Depends(check_admin_permission),
    db: AsyncSession = Depends(get_db)
):
    """
    获取所有推荐作品（管理员）
    """
    result = await db.execute(
        select(Work).where(Work.is_featured == True).order_by(Work.published_at.desc())
    )
    works = result.scalars().all()

    return {
        "total": len(works),
        "items": [
            {
                "id": str(work.id),
                "title": work.title,
                "author_id": str(work.author_id),
                "is_published": work.is_published,
                "published_at": work.published_at,
                "view_count": work.view_count,
            }
            for work in works
        ]
    }


@router.post("/featured-novels/{work_id}")
async def add_featured_novel(
    work_id: str,
    current_user: User = Depends(check_admin_permission),
    db: AsyncSession = Depends(get_db)
):
    """
    将作品设为推荐（最多5本）
    """
    # 检查作品是否存在且已发布
    work_result = await db.execute(
        select(Work).where(Work.id == work_id, Work.is_published == True)
    )
    work = work_result.scalar_one_or_none()

    if not work:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="作品不存在或未发布"
        )

    # 检查推荐作品数量
    featured_count_result = await db.execute(
        select(func.count(Work.id)).where(Work.is_featured == True)
    )
    featured_count = featured_count_result.scalar() or 0

    if featured_count >= 5 and not work.is_featured:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="推荐作品已达上限(5本)，请先取消其他作品的推荐"
        )

    # 设为推荐
    work.is_featured = True
    await db.commit()

    return {
        "message": f"《{work.title}》已设为推荐作品",
        "work_id": str(work.id)
    }


@router.delete("/featured-novels/{work_id}")
async def remove_featured_novel(
    work_id: str,
    current_user: User = Depends(check_admin_permission),
    db: AsyncSession = Depends(get_db)
):
    """
    取消作品推荐
    """
    # 检查作品是否存在
    work_result = await db.execute(
        select(Work).where(Work.id == work_id)
    )
    work = work_result.scalar_one_or_none()

    if not work:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="作品不存在"
        )

    # 取消推荐
    work.is_featured = False
    await db.commit()

    return {
        "message": f"《{work.title}》已取消推荐",
        "work_id": str(work.id)
    }


# ========== 用户称号管理 ==========


@router.patch("/users/{user_id}/honor", response_model=UserActionResponse)
async def update_user_honor(
    user_id: UUID,
    request: UpdateUserHonorRequest,
    current_user: User = Depends(check_admin_permission),
    db: AsyncSession = Depends(get_db)
) -> UserActionResponse:
    """
    更新用户称号

    Args:
        user_id: 用户ID
        request: 包含新称号的请求体

    Returns:
        操作成功的消息和用户信息
    """
    # 查询用户
    user = await db.get(User, user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )

    # 更新称号
    old_honor = user.honor
    user.honor = request.honor
    await db.commit()
    await db.refresh(user)

    if request.honor:
        message = f"用户 {user.username} 的称号已更新为「{request.honor}」"
    else:
        message = f"用户 {user.username} 的称号已清除"

    return UserActionResponse(
        message=message,
        user=UserBasicInfo.model_validate(user)
    )


# ========== 频道管理 ==========


@router.get("/channels")
async def get_all_channels(
    skip: int = 0,
    limit: int = 100,
    channel_type: Optional[str] = None,
    channel_status: Optional[str] = None,
    search: Optional[str] = None,
    current_user: User = Depends(check_admin_permission),
    db: AsyncSession = Depends(get_db)
):
    """
    获取所有频道列表（管理员专用）

    Args:
        skip: 分页偏移
        limit: 分页大小
        channel_type: 频道类型筛选 (official/fangroup/work)
        channel_status: 频道状态筛选 (active/warning/locked)
        search: 搜索关键词

    Returns:
        频道列表和总数
    """
    from app.models.channel import Channel, ChannelType, ChannelStatus
    from sqlalchemy.orm import selectinload

    # 构建查询
    query = select(Channel).options(
        selectinload(Channel.work)
    )

    # 类型筛选
    if channel_type:
        query = query.where(Channel.type == channel_type)

    # 状态筛选
    if channel_status:
        query = query.where(Channel.status == channel_status)

    # 搜索
    if search:
        query = query.where(Channel.name.ilike(f"%{search}%"))

    # 排序：按创建时间倒序
    query = query.order_by(Channel.created_at.desc())

    # 获取总数
    count_query = select(func.count()).select_from(query.subquery())
    total = await db.scalar(count_query) or 0

    # 分页
    query = query.offset(skip).limit(limit)

    result = await db.execute(query)
    channels = result.scalars().all()

    # 构建响应
    channel_list = []
    for channel in channels:
        channel_data = {
            "id": str(channel.id),
            "name": channel.name,
            "description": channel.description,
            "type": channel.type,
            "status": channel.status,
            "creator_id": str(channel.creator_id) if channel.creator_id else None,
            "work_id": str(channel.work_id) if channel.work_id else None,
            "member_count": channel.member_count or 0,
            "message_count": channel.message_count or 0,
            "is_permanent": channel.is_permanent,
            "warning_days": channel.warning_days,
            "created_at": channel.created_at.isoformat() if channel.created_at else None,
            "updated_at": channel.updated_at.isoformat() if channel.updated_at else None,
            "locked_at": channel.locked_at.isoformat() if channel.locked_at else None,
        }

        # 如果是作品频道，添加作品信息
        if channel.type == "work" and channel.work:
            channel_data["book_title"] = channel.work.title

        channel_list.append(channel_data)

    return {
        "total": total,
        "channels": channel_list
    }


@router.patch("/channels/{channel_id}/status")
async def update_channel_status(
    channel_id: UUID,
    new_status: str,
    current_user: User = Depends(check_admin_permission),
    db: AsyncSession = Depends(get_db)
):
    """
    更新频道状态（管理员专用）

    Args:
        channel_id: 频道ID
        new_status: 新状态 (active/warning/locked)

    Returns:
        更新后的频道信息
    """
    from app.models.channel import Channel, ChannelStatus

    # 验证状态值
    valid_statuses = ["active", "warning", "locked"]
    if new_status not in valid_statuses:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"无效的状态值，必须是: {', '.join(valid_statuses)}"
        )

    # 查询频道
    channel = await db.get(Channel, channel_id)
    if not channel:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="频道不存在"
        )

    old_status = channel.status
    channel.status = new_status

    # 如果是锁定，记录锁定时间
    if new_status == "locked":
        channel.locked_at = get_utc_now()
    elif old_status == "locked" and new_status != "locked":
        # 解锁时清除锁定时间
        channel.locked_at = None

    await db.commit()
    await db.refresh(channel)

    return {
        "message": f"频道状态已从 {old_status} 更新为 {new_status}",
        "channel": {
            "id": str(channel.id),
            "name": channel.name,
            "status": channel.status,
            "locked_at": channel.locked_at.isoformat() if channel.locked_at else None
        }
    }
