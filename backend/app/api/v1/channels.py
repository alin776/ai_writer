from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy import select, func, and_, or_, case
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload, joinedload
from typing import Optional, List
from uuid import UUID
import logging
import uuid

from app.core.database import get_db
from app.core.security import get_current_active_user
from app.models.user import User
from app.models.work import Work
from app.models.channel import Channel, ChannelType, ChannelStatus
from app.models.channel_member import ChannelMember, MemberRole
from app.models.channel_message import ChannelMessage, MessageType
from app.models.message_report import MessageReport
from app.models.channel_read_state import ChannelReadState
from app.schemas.channel import (
    ChannelCreate,
    FangroupCreate,
    ChannelUpdate,
    ChannelResponse,
    ChannelListResponse,
    ChannelMemberCreate,
    ChannelMemberResponse,
    ChannelMessageCreate,
    ChannelMessageUpdate,
    ChannelMessageResponse,
    ChannelMessageListResponse,
)

router = APIRouter()
logger = logging.getLogger(__name__)


async def check_channel_access(channel: Channel, user: User, db: AsyncSession) -> bool:
    """
    检查用户是否满足频道进入要求

    Returns:
        bool: True 表示可以访问，False 表示不满足要求
    """
    if not channel.join_requirement:
        return True

    try:
        import json
        requirement = json.loads(channel.join_requirement)
        req_type = requirement.get('type')

        if req_type == 'published_works':
            # 检查用户是否有已发布的作品
            min_count = requirement.get('min_count', 1)
            result = await db.execute(
                select(func.count(Work.id)).where(
                    Work.author_id == user.id,
                    Work.is_published == True
                )
            )
            published_count = result.scalar() or 0
            return published_count >= min_count

        return True
    except:
        # 如果解析失败，默认允许访问
        return True


def build_channel_response(channel: Channel, work: Optional[Work] = None) -> dict:
    """构建频道响应数据"""
    data = {
        "id": channel.id,
        "name": channel.name,
        "description": channel.description,
        "cover_image": channel.cover_image,
        "type": channel.type,
        "status": channel.status,
        "creator_id": channel.creator_id,
        "work_id": channel.work_id,
        "is_permanent": channel.is_permanent,
        "is_pinned": channel.is_pinned,
        "trial_end_at": channel.trial_end_at,
        "member_count": channel.member_count,
        "message_count": channel.message_count,
        "last_message_at": channel.last_message_at,
        "warning_days": channel.warning_days,
        "created_at": channel.created_at,
        "updated_at": channel.updated_at,
        "locked_at": channel.locked_at,
        "join_requirement": channel.join_requirement,
    }

    # 如果是作品频道，添加作品信息
    if channel.type == "work" and work:
        data["book_title"] = work.title
        data["author"] = work.author.username if work.author else None
        data["collect_count"] = work.favorite_count

    return data


import re


async def extract_mentions(content: str, db: AsyncSession) -> List[str]:
    """从消息内容中提取 @ 的用户名"""
    # 匹配 @用户名 格式（用户名可以是中文、英文、数字）
    pattern = r'@([^\s@]+)'
    matches = re.findall(pattern, content)
    return list(set(matches))  # 去重


async def update_unread_counts(
    db: AsyncSession,
    channel_id: UUID,
    message_id: UUID,
    sender_id: UUID,
    mentioned_usernames: List[str]
):
    """更新频道成员的未读消息数和@提醒数"""
    # 获取所有频道成员（除了发送者）
    members_result = await db.execute(
        select(ChannelMember)
        .where(
            ChannelMember.channel_id == channel_id,
            ChannelMember.user_id != sender_id
        )
        .options(selectinload(ChannelMember.user))
    )
    members = members_result.scalars().all()

    for member in members:
        # 获取或创建已读状态记录
        read_state_result = await db.execute(
            select(ChannelReadState).where(
                ChannelReadState.user_id == member.user_id,
                ChannelReadState.channel_id == channel_id
            )
        )
        read_state = read_state_result.scalar_one_or_none()

        if not read_state:
            read_state = ChannelReadState(
                id=uuid.uuid4(),
                user_id=member.user_id,
                channel_id=channel_id,
                unread_count=0,
                mention_count=0
            )
            db.add(read_state)

        # 增加未读数
        read_state.unread_count += 1

        # 检查是否被@
        if member.user and member.user.username in mentioned_usernames:
            read_state.mention_count += 1

        # 检查 @全体成员
        if "全体成员" in mentioned_usernames:
            read_state.mention_count += 1

    await db.flush()


@router.post("/create-fangroup", response_model=ChannelResponse)
async def create_fangroup(
    data: FangroupCreate,
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db)
):
    """
    创建粉丝群频道（私域）
    创作者手动创建，拥有公告、@全体成员权限
    """
    logger.info(f"[创建粉丝群] 用户 {current_user.username} 开始创建粉丝群: {data.name}")

    # 创建频道
    channel = Channel(
        id=uuid.uuid4(),
        name=data.name,
        description=data.description,
        cover_image=data.cover_image,
        type='fangroup',
        status='active',
        creator_id=current_user.id,
        is_permanent=False,
        is_pinned=False,
    )

    db.add(channel)

    # 创建者自动成为频道所有者，并获得"群主"称号
    owner_member = ChannelMember(
        id=uuid.uuid4(),
        channel_id=channel.id,
        user_id=current_user.id,
        role='owner',
        custom_title='群主',
        title_color='#FF6B6B'
    )
    db.add(owner_member)

    # 更新频道成员数
    channel.member_count = 1

    await db.commit()
    await db.refresh(channel)

    response_data = build_channel_response(channel)
    logger.info(f"[创建粉丝群] 响应数据 - is_permanent={response_data.get('is_permanent')}")

    return ChannelResponse(**response_data)


@router.get("/my-channels", response_model=ChannelListResponse)
async def get_my_channels(
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db)
):
    """
    获取当前用户加入的所有频道
    包括：官方频道（所有人自动可见）+ 用户主动加入的频道
    """
    # 1. 获取所有官方频道（所有人都可以看到）
    # 按照固定顺序排序：公共酒馆 -> 作者酒馆 -> 读者茶馆 -> 官方实验室
    official_channels_query = (
        select(Channel)
        .where(Channel.type == "official")
        .options(selectinload(Channel.work).selectinload(Work.author))
        .order_by(
            case(
                (Channel.name == '公共酒馆', 1),
                (Channel.name == '作者酒馆', 2),
                (Channel.name == '读者茶馆', 3),
                (Channel.name == '官方实验室', 4),
                else_=99
            )
        )
    )
    official_result = await db.execute(official_channels_query)
    official_channels = official_result.scalars().all()

    # 2. 查询用户主动加入的非官方频道
    user_channels_query = (
        select(Channel)
        .join(ChannelMember, Channel.id == ChannelMember.channel_id)
        .where(
            ChannelMember.user_id == current_user.id,
            ChannelMember.is_banned == False,
            Channel.type != "official"  # 排除官方频道，避免重复
        )
        .options(
            selectinload(Channel.work).selectinload(Work.author)
        )
    )
    user_result = await db.execute(user_channels_query)
    user_channels = user_result.scalars().all()

    # 3. 合并并排序所有频道
    all_channels = list(official_channels) + list(user_channels)
    all_channels.sort(
        key=lambda c: (
            not c.is_pinned,  # 置顶的在前
            c.type != "official",  # 官方频道在前
            c.type != "fangroup",  # 粉丝群其次
            c.type != "work",  # 作品频道最后
            -c.created_at.timestamp() if c.created_at else 0  # 同类型按创建时间倒序
        )
    )

    # 查询当前用户在所有频道中的成员关系
    channel_ids = [c.id for c in all_channels]
    if channel_ids:  # 只有在有频道时才查询
        members_query = select(ChannelMember).where(
            ChannelMember.channel_id.in_(channel_ids),
            ChannelMember.user_id == current_user.id,
            ChannelMember.is_banned == False
        )
        members_result = await db.execute(members_query)
        members = {m.channel_id: m for m in members_result.scalars().all()}
    else:
        members = {}

    # 构建响应
    channel_responses = []
    for channel in all_channels:
        channel_data = build_channel_response(channel, channel.work)
        # 添加当前用户在该频道中的角色
        member = members.get(channel.id)
        if member:
            channel_data['current_user_role'] = member.role
        elif channel.type == 'official':
            # 官方频道默认为member角色（如果用户是管理员，会在自动加入时设置为owner）
            channel_data['current_user_role'] = 'owner' if current_user.is_admin else 'member'
        else:
            channel_data['current_user_role'] = None

        # 检查用户是否满足进入要求
        can_access = await check_channel_access(channel, current_user, db)
        channel_data['can_access'] = can_access

        channel_responses.append(ChannelResponse(**channel_data))

    return ChannelListResponse(
        channels=channel_responses,
        total=len(channel_responses)
    )


@router.get("/available-channels", response_model=ChannelListResponse)
async def get_available_channels(
    skip: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=100),
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db)
):
    """
    获取可加入的频道（不包括已加入的）
    """
    # 查询用户已加入的频道ID
    joined_channels_query = select(ChannelMember.channel_id).where(
        ChannelMember.user_id == current_user.id
    )
    joined_result = await db.execute(joined_channels_query)
    joined_ids = [row[0] for row in joined_result.all()]

    # 查询可加入的频道（排除官方频道，因为官方频道所有人都默认加入）
    query = (
        select(Channel)
        .where(
            Channel.status == "active",
            Channel.type != "official",
            Channel.id.notin_(joined_ids) if joined_ids else True
        )
        .options(
            selectinload(Channel.work).selectinload(Work.author)
        )
        .order_by(Channel.created_at.desc())
    )

    # 获取总数
    count_query = select(func.count(Channel.id)).where(
        Channel.status == "active",
        Channel.type != "official",
        Channel.id.notin_(joined_ids) if joined_ids else True
    )
    count_result = await db.execute(count_query)
    total = count_result.scalar() or 0

    # 分页查询
    result = await db.execute(query.offset(skip).limit(limit))
    channels = result.scalars().all()

    # 构建响应
    channel_responses = []
    for channel in channels:
        channel_data = build_channel_response(channel, channel.work)
        channel_responses.append(ChannelResponse(**channel_data))

    return ChannelListResponse(
        channels=channel_responses,
        total=total
    )


@router.post("/join", response_model=ChannelMemberResponse)
async def join_channel(
    data: ChannelMemberCreate,
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db)
):
    """
    加入频道
    """
    # 检查频道是否存在
    channel_result = await db.execute(
        select(Channel).where(Channel.id == data.channel_id)
    )
    channel = channel_result.scalar_one_or_none()

    if not channel:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="频道不存在"
        )

    # 检查频道状态
    if channel.status == "locked":
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="频道已折叠，无法加入"
        )

    # 检查是否已经是成员
    existing_member = await db.execute(
        select(ChannelMember).where(
            ChannelMember.channel_id == data.channel_id,
            ChannelMember.user_id == current_user.id
        )
    )
    if existing_member.scalar_one_or_none():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="已经是频道成员"
        )

    # 创建成员记录
    # 如果是官方频道且用户是管理员，则设置为owner角色
    member_role = 'owner' if (channel.type == 'official' and current_user.is_admin) else 'member'
    member = ChannelMember(
        id=uuid.uuid4(),
        channel_id=data.channel_id,
        user_id=current_user.id,
        role=member_role
    )
    db.add(member)

    # 更新频道成员数
    channel.member_count += 1

    await db.commit()
    await db.refresh(member)

    return ChannelMemberResponse(
        id=member.id,
        channel_id=member.channel_id,
        user_id=member.user_id,
        role=member.role,
        is_muted=member.is_muted,
        is_banned=member.is_banned,
        custom_title=member.custom_title,
        title_color=member.title_color,
        joined_at=member.joined_at,
        last_read_at=member.last_read_at,
        user_name=current_user.username,
        user_avatar=current_user.avatar
    )


@router.delete("/{channel_id}/leave")
async def leave_channel(
    channel_id: UUID,
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db)
):
    """
    退出频道

    - 普通成员：退出频道
    - 粉丝群创建者：解散频道（删除频道及所有成员、消息）
    - 作品频道创建者：不能退出
    - 官方频道：不能退出
    """
    # 查找成员记录
    member_result = await db.execute(
        select(ChannelMember)
        .where(
            ChannelMember.channel_id == channel_id,
            ChannelMember.user_id == current_user.id
        )
        .options(selectinload(ChannelMember.channel))
    )
    member = member_result.scalar_one_or_none()

    if not member:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="未加入该频道"
        )

    channel = member.channel

    # 不能退出官方频道
    if channel.type == "official":
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="不能退出官方频道"
        )

    # 粉丝群创建者退出 = 解散频道
    if member.role == 'owner' and channel.type == 'fangroup':
        # 删除整个频道（级联删除会自动删除所有成员和消息）
        await db.delete(channel)
        await db.commit()

        return {
            "message": "频道已解散",
            "disbanded": True
        }

    # 作品频道创建者不能退出
    if member.role == 'owner' and channel.type == 'work':
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="作品频道创建者不能退出频道"
        )

    # 普通成员退出
    # 删除成员记录
    await db.delete(member)

    # 更新频道成员数
    channel.member_count -= 1

    await db.commit()

    return {
        "message": "已退出频道",
        "disbanded": False
    }


@router.get("/{channel_id}/members")
async def get_channel_members(
    channel_id: UUID,
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db)
):
    """
    获取频道成员列表
    """
    # 检查是否是频道成员
    member_check = await db.execute(
        select(ChannelMember).where(
            ChannelMember.channel_id == channel_id,
            ChannelMember.user_id == current_user.id
        )
    )
    if not member_check.scalar_one_or_none():
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="您不是该频道的成员"
        )

    # 获取所有成员
    result = await db.execute(
        select(ChannelMember)
        .where(ChannelMember.channel_id == channel_id)
        .options(selectinload(ChannelMember.user))
        .order_by(ChannelMember.joined_at)
    )
    members = result.scalars().all()

    return {
        "members": [
            {
                "id": member.id,
                "user_id": member.user_id,
                "username": member.user.username if member.user else "已删除用户",
                "avatar": member.user.avatar if member.user else None,
                "role": member.role,
                "custom_title": member.custom_title,
                "title_color": member.title_color,
                "is_muted": member.is_muted,
                "muted_until": member.muted_until.isoformat() if member.muted_until else None,
                "joined_at": member.joined_at,
            }
            for member in members
        ],
        "total": len(members)
    }


@router.delete("/{channel_id}/members/{user_id}")
async def kick_member(
    channel_id: UUID,
    user_id: UUID,
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db)
):
    """
    踢出频道成员（仅创建者可操作）
    """
    # 检查当前用户是否是频道创建者
    current_member_result = await db.execute(
        select(ChannelMember)
        .where(
            ChannelMember.channel_id == channel_id,
            ChannelMember.user_id == current_user.id
        )
        .options(selectinload(ChannelMember.channel))
    )
    current_member = current_member_result.scalar_one_or_none()

    if not current_member:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="您不是该频道的成员"
        )

    if current_member.role != 'owner':
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="只有频道创建者可以踢出成员"
        )

    # 不能踢出自己
    if user_id == current_user.id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="不能踢出自己"
        )

    # 查找要踢出的成员
    target_member_result = await db.execute(
        select(ChannelMember).where(
            ChannelMember.channel_id == channel_id,
            ChannelMember.user_id == user_id
        )
    )
    target_member = target_member_result.scalar_one_or_none()

    if not target_member:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="该用户不是频道成员"
        )

    # 删除成员
    await db.delete(target_member)

    # 更新频道成员数
    channel = current_member.channel
    channel.member_count -= 1

    await db.commit()

    return {"message": "成员已被踢出"}


@router.get("/{channel_id}/messages", response_model=ChannelMessageListResponse)
async def get_channel_messages(
    channel_id: UUID,
    skip: int = Query(0, ge=0),
    limit: int = Query(50, ge=1, le=100),
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db)
):
    """
    获取频道消息列表
    """
    # 检查是否是频道成员
    member_result = await db.execute(
        select(ChannelMember).where(
            ChannelMember.channel_id == channel_id,
            ChannelMember.user_id == current_user.id
        )
    )
    if not member_result.scalar_one_or_none():
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="未加入该频道"
        )

    # 查询消息
    query = (
        select(ChannelMessage)
        .where(
            ChannelMessage.channel_id == channel_id,
            ChannelMessage.is_deleted == False
        )
        .options(
            selectinload(ChannelMessage.user)
        )
        .order_by(ChannelMessage.created_at.asc())
    )

    # 获取总数
    count_query = select(func.count(ChannelMessage.id)).where(
        ChannelMessage.channel_id == channel_id,
        ChannelMessage.is_deleted == False
    )
    count_result = await db.execute(count_query)
    total = count_result.scalar() or 0

    # 分页查询
    result = await db.execute(query.offset(skip).limit(limit))
    messages = result.scalars().all()

    # 获取成员信息（用于显示用户称号）
    member_dict = {}
    if messages:
        user_ids = list(set(msg.user_id for msg in messages if msg.user_id))
        if user_ids:
            members_result = await db.execute(
                select(ChannelMember).where(
                    ChannelMember.channel_id == channel_id,
                    ChannelMember.user_id.in_(user_ids)
                )
            )
            for member in members_result.scalars():
                member_dict[member.user_id] = member

    # 构建响应
    message_responses = []
    for msg in messages:
        member = member_dict.get(msg.user_id)
        message_responses.append(ChannelMessageResponse(
            id=msg.id,
            channel_id=msg.channel_id,
            user_id=msg.user_id,
            content=msg.content,
            type=msg.type,
            is_pinned=msg.is_pinned,
            is_deleted=msg.is_deleted,
            reply_to_id=msg.reply_to_id,
            reaction_count=msg.reaction_count,
            created_at=msg.created_at,
            updated_at=msg.updated_at,
            deleted_at=msg.deleted_at,
            user_name=msg.user.username if msg.user else "已删除用户",
            user_avatar=msg.user.avatar if msg.user else None,
            user_honor=msg.user.honor if msg.user else None,
            user_title=member.custom_title if member else None,
            user_title_color=member.title_color if member else None
        ))

    has_more = skip + limit < total

    return ChannelMessageListResponse(
        messages=message_responses,
        total=total,
        has_more=has_more
    )


@router.get("/{channel_id}/announcements", response_model=ChannelMessageListResponse)
async def get_channel_announcements(
    channel_id: UUID,
    skip: int = Query(0, ge=0),
    limit: int = Query(50, ge=1, le=100),
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db)
):
    """
    获取频道公告列表
    """
    # 检查是否是频道成员
    member_result = await db.execute(
        select(ChannelMember).where(
            ChannelMember.channel_id == channel_id,
            ChannelMember.user_id == current_user.id
        )
    )
    if not member_result.scalar_one_or_none():
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="未加入该频道"
        )

    # 查询公告消息（只查询公告类型的消息）
    query = (
        select(ChannelMessage)
        .where(
            ChannelMessage.channel_id == channel_id,
            ChannelMessage.is_deleted == False,
            ChannelMessage.type == MessageType.ANNOUNCEMENT
        )
        .options(
            selectinload(ChannelMessage.user)
        )
        .order_by(ChannelMessage.created_at.desc())  # 最新的公告在前
    )

    # 获取总数
    count_query = select(func.count(ChannelMessage.id)).where(
        ChannelMessage.channel_id == channel_id,
        ChannelMessage.is_deleted == False,
        ChannelMessage.type == MessageType.ANNOUNCEMENT
    )
    count_result = await db.execute(count_query)
    total = count_result.scalar() or 0

    # 分页查询
    result = await db.execute(query.offset(skip).limit(limit))
    messages = result.scalars().all()

    # 获取成员信息（用于显示用户称号）
    member_dict = {}
    if messages:
        user_ids = list(set(msg.user_id for msg in messages if msg.user_id))
        if user_ids:
            members_result = await db.execute(
                select(ChannelMember).where(
                    ChannelMember.channel_id == channel_id,
                    ChannelMember.user_id.in_(user_ids)
                )
            )
            for member in members_result.scalars():
                member_dict[member.user_id] = member

    # 构建响应
    message_responses = []
    for msg in messages:
        member = member_dict.get(msg.user_id)
        message_responses.append(ChannelMessageResponse(
            id=msg.id,
            channel_id=msg.channel_id,
            user_id=msg.user_id,
            content=msg.content,
            type=msg.type,
            is_pinned=msg.is_pinned,
            is_deleted=msg.is_deleted,
            reply_to_id=msg.reply_to_id,
            reaction_count=msg.reaction_count,
            created_at=msg.created_at,
            updated_at=msg.updated_at,
            deleted_at=msg.deleted_at,
            user_name=msg.user.username if msg.user else "已删除用户",
            user_avatar=msg.user.avatar if msg.user else None,
            user_honor=msg.user.honor if msg.user else None,
            user_title=member.custom_title if member else None,
            user_title_color=member.title_color if member else None
        ))

    has_more = skip + limit < total

    return ChannelMessageListResponse(
        messages=message_responses,
        total=total,
        has_more=has_more
    )


@router.post("/{channel_id}/messages", response_model=ChannelMessageResponse)
async def send_message(
    channel_id: UUID,
    content: str = Query(..., min_length=1),
    message_type: MessageType = Query("normal"),
    reply_to_id: Optional[UUID] = Query(None, description="回复的消息ID"),
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db)
):
    """
    发送频道消息
    官方频道：自动创建成员记录（如果不存在）
    其他频道：需要先加入
    """
    # 获取频道信息
    channel_result = await db.execute(
        select(Channel).where(Channel.id == channel_id)
    )
    channel = channel_result.scalar_one_or_none()

    if not channel:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="频道不存在"
        )

    # 检查频道成员身份
    member_result = await db.execute(
        select(ChannelMember)
        .where(
            ChannelMember.channel_id == channel_id,
            ChannelMember.user_id == current_user.id
        )
    )
    member = member_result.scalar_one_or_none()

    # 如果不是成员
    if not member:
        # 官方频道：自动加入
        if channel.type == "official":
            # 如果用户是管理员，则设置为owner角色
            member_role = "owner" if current_user.is_admin else "member"
            member = ChannelMember(
                id=uuid.uuid4(),
                channel_id=channel_id,
                user_id=current_user.id,
                role=member_role,
                joined_at=func.now()
            )
            db.add(member)
            await db.flush()  # 确保member有ID

            # 更新频道成员数
            channel.member_count += 1
        else:
            # 非官方频道：必须先加入
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="未加入该频道"
            )

    # 检查是否被禁言
    from datetime import datetime, timezone
    if member.is_muted:
        # 检查禁言是否已过期
        if member.muted_until and datetime.now(timezone.utc) >= member.muted_until:
            # 自动解除禁言
            member.is_muted = False
            member.muted_until = None
            await db.commit()
        else:
            # 仍在禁言期间
            mute_info = ""
            if member.muted_until:
                mute_info = f"，禁言至 {member.muted_until.strftime('%Y-%m-%d %H:%M:%S')} UTC"
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"您已被禁言{mute_info}"
            )

    # 检查频道状态
    if channel.status == "locked":
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="频道已折叠，无法发送消息"
        )

    # 只有粉丝群和官方频道的创建者可以发送公告
    if message_type == "announcement":
        if (channel.type not in ['fangroup', 'official']) or member.role != 'owner':
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="只有频道创建者可以发送公告"
            )

    # 如果是回复消息，检查被回复的消息是否存在
    if reply_to_id:
        reply_msg_result = await db.execute(
            select(ChannelMessage).where(
                ChannelMessage.id == reply_to_id,
                ChannelMessage.channel_id == channel_id
            )
        )
        if not reply_msg_result.scalar_one_or_none():
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="被回复的消息不存在"
            )

    # 创建消息
    message = ChannelMessage(
        id=uuid.uuid4(),
        channel_id=channel_id,
        user_id=current_user.id,
        content=content,
        type=message_type,
        reply_to_id=reply_to_id
    )
    db.add(message)

    # 更新频道消息数和最后消息时间
    member.channel.message_count += 1
    member.channel.last_message_at = func.now()

    await db.flush()

    # 提取 @ 的用户名并更新未读计数
    mentioned_usernames = await extract_mentions(content, db)
    await update_unread_counts(db, channel_id, message.id, current_user.id, mentioned_usernames)

    # 更新每日频道发言任务进度
    from app.services.task_service import TaskService
    await TaskService.check_channel_message_task(db, current_user.id)

    await db.commit()
    await db.refresh(message)

    return ChannelMessageResponse(
        id=message.id,
        channel_id=message.channel_id,
        user_id=message.user_id,
        content=message.content,
        type=message.type,
        is_pinned=message.is_pinned,
        is_deleted=message.is_deleted,
        reply_to_id=message.reply_to_id,
        reaction_count=message.reaction_count,
        created_at=message.created_at,
        updated_at=message.updated_at,
        deleted_at=message.deleted_at,
        user_name=current_user.username,
        user_avatar=current_user.avatar,
        user_honor=current_user.honor,
        user_title=member.custom_title,
        user_title_color=member.title_color
    )


@router.post("/{channel_id}/messages/{message_id}/report")
async def report_message(
    channel_id: UUID,
    message_id: UUID,
    reason: str = Query(..., description="举报原因: spam, inappropriate, harassment, other"),
    description: str = Query(None, description="详细描述"),
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db)
):
    """
    举报频道消息
    """
    # 检查是否是频道成员
    member_check = await db.execute(
        select(ChannelMember).where(
            ChannelMember.channel_id == channel_id,
            ChannelMember.user_id == current_user.id
        )
    )
    if not member_check.scalar_one_or_none():
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="您不是该频道的成员"
        )

    # 检查消息是否存在
    message_result = await db.execute(
        select(ChannelMessage).where(
            ChannelMessage.id == message_id,
            ChannelMessage.channel_id == channel_id
        )
    )
    message = message_result.scalar_one_or_none()
    if not message:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="消息不存在"
        )

    # 检查是否已经举报过
    existing_report = await db.execute(
        select(MessageReport).where(
            MessageReport.message_id == message_id,
            MessageReport.reporter_id == current_user.id
        )
    )
    if existing_report.scalar_one_or_none():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="您已经举报过这条消息"
        )

    # 创建举报记录
    report = MessageReport(
        message_id=message_id,
        reporter_id=current_user.id,
        reason=reason,
        description=description,
        status="pending"
    )
    db.add(report)
    await db.commit()

    return {"message": "举报已提交，我们会尽快处理"}


@router.put("/{channel_id}", response_model=ChannelResponse)
async def update_fangroup(
    channel_id: UUID,
    data: ChannelUpdate,
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db)
):
    """
    更新粉丝群信息（仅创建者可操作）
    """
    # 查找频道
    channel_result = await db.execute(
        select(Channel).where(Channel.id == channel_id)
    )
    channel = channel_result.scalar_one_or_none()

    if not channel:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="频道不存在"
        )

    # 检查是否为粉丝群
    if channel.type != "fangroup":
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="只能更新粉丝群频道"
        )

    # 检查是否为创建者
    if channel.creator_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="只有创建者可以更新频道"
        )

    # 更新字段
    if data.name is not None:
        channel.name = data.name
    if data.description is not None:
        channel.description = data.description
    if data.cover_image is not None:
        channel.cover_image = data.cover_image

    await db.commit()
    await db.refresh(channel)

    return ChannelResponse(**build_channel_response(channel))


@router.delete("/{channel_id}")
async def delete_fangroup(
    channel_id: UUID,
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db)
):
    """
    删除粉丝群（仅创建者可操作）
    """
    # 查找频道
    channel_result = await db.execute(
        select(Channel).where(Channel.id == channel_id)
    )
    channel = channel_result.scalar_one_or_none()

    if not channel:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="频道不存在"
        )

    # 检查是否为粉丝群
    if channel.type != "fangroup":
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="只能删除粉丝群频道"
        )

    # 检查是否为创建者
    if channel.creator_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="只有创建者可以删除频道"
        )

    # 删除频道（级联删除成员和消息）
    await db.delete(channel)
    await db.commit()

    return {"message": "频道已删除"}


# ===== 未读消息和@提醒相关 API =====

@router.post("/{channel_id}/mark-read")
async def mark_channel_as_read(
    channel_id: UUID,
    message_id: Optional[UUID] = Query(None, description="标记到哪条消息为已读，不传则标记全部已读"),
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db)
):
    """
    标记频道消息为已读
    """
    # 检查是否是频道成员
    member_check = await db.execute(
        select(ChannelMember).where(
            ChannelMember.channel_id == channel_id,
            ChannelMember.user_id == current_user.id
        )
    )
    if not member_check.scalar_one_or_none():
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="未加入该频道"
        )

    # 获取或创建已读状态记录
    read_state_result = await db.execute(
        select(ChannelReadState).where(
            ChannelReadState.user_id == current_user.id,
            ChannelReadState.channel_id == channel_id
        )
    )
    read_state = read_state_result.scalar_one_or_none()

    if not read_state:
        read_state = ChannelReadState(
            id=uuid.uuid4(),
            user_id=current_user.id,
            channel_id=channel_id,
            unread_count=0,
            mention_count=0
        )
        db.add(read_state)

    # 更新已读位置和计数
    if message_id:
        read_state.last_read_message_id = message_id

    read_state.unread_count = 0
    read_state.mention_count = 0
    read_state.last_read_at = func.now()

    await db.commit()

    return {"message": "已标记为已读"}


@router.get("/unread-summary")
async def get_unread_summary(
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db)
):
    """
    获取所有频道的未读统计（用于左侧频道列表）
    返回每个频道的未读数和@我的数量
    """
    # 获取用户加入的所有频道
    channels_result = await db.execute(
        select(ChannelMember)
        .where(ChannelMember.user_id == current_user.id)
        .options(selectinload(ChannelMember.channel))
    )
    members = channels_result.scalars().all()

    channel_ids = [m.channel_id for m in members]

    # 获取所有频道的已读状态
    read_states_result = await db.execute(
        select(ChannelReadState).where(
            ChannelReadState.user_id == current_user.id,
            ChannelReadState.channel_id.in_(channel_ids)
        )
    )
    read_states = {rs.channel_id: rs for rs in read_states_result.scalars().all()}

    # 构建返回数据
    summary = []
    for member in members:
        read_state = read_states.get(member.channel_id)
        summary.append({
            "channel_id": member.channel_id,
            "unread_count": read_state.unread_count if read_state else 0,
            "mention_count": read_state.mention_count if read_state else 0,
            "has_mention": (read_state.mention_count > 0) if read_state else False
        })

    return {"channels": summary}


@router.get("/{channel_id}/unread-info")
async def get_channel_unread_info(
    channel_id: UUID,
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db)
):
    """
    获取单个频道的详细未读信息
    包括第一条未读消息ID、最近一条@我的消息ID等
    """
    # 检查是否是频道成员
    member_check = await db.execute(
        select(ChannelMember).where(
            ChannelMember.channel_id == channel_id,
            ChannelMember.user_id == current_user.id
        )
    )
    if not member_check.scalar_one_or_none():
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="未加入该频道"
        )

    # 获取已读状态
    read_state_result = await db.execute(
        select(ChannelReadState).where(
            ChannelReadState.user_id == current_user.id,
            ChannelReadState.channel_id == channel_id
        )
    )
    read_state = read_state_result.scalar_one_or_none()

    if not read_state or not read_state.last_read_message_id:
        # 没有已读记录，获取第一条消息
        first_unread_result = await db.execute(
            select(ChannelMessage.id)
            .where(ChannelMessage.channel_id == channel_id)
            .order_by(ChannelMessage.created_at.asc())
            .limit(1)
        )
        first_unread_id = first_unread_result.scalar_one_or_none()
    else:
        # 获取最后已读消息之后的第一条
        last_read_msg_result = await db.execute(
            select(ChannelMessage).where(
                ChannelMessage.id == read_state.last_read_message_id
            )
        )
        last_read_msg = last_read_msg_result.scalar_one_or_none()

        if last_read_msg:
            first_unread_result = await db.execute(
                select(ChannelMessage.id)
                .where(
                    ChannelMessage.channel_id == channel_id,
                    ChannelMessage.created_at > last_read_msg.created_at
                )
                .order_by(ChannelMessage.created_at.asc())
                .limit(1)
            )
            first_unread_id = first_unread_result.scalar_one_or_none()
        else:
            first_unread_id = None

    # 查找@我的最新消息
    mention_pattern = f"@{current_user.username}"
    latest_mention_result = await db.execute(
        select(ChannelMessage.id)
        .where(
            ChannelMessage.channel_id == channel_id,
            or_(
                ChannelMessage.content.contains(mention_pattern),
                ChannelMessage.content.contains("@全体成员")
            )
        )
        .order_by(ChannelMessage.created_at.desc())
        .limit(1)
    )
    latest_mention_id = latest_mention_result.scalar_one_or_none()

    return {
        "unread_count": read_state.unread_count if read_state else 0,
        "mention_count": read_state.mention_count if read_state else 0,
        "first_unread_message_id": first_unread_id,
        "latest_mention_message_id": latest_mention_id,
        "last_read_message_id": read_state.last_read_message_id if read_state else None
    }


# ===== 公告系统相关 API =====

@router.get("/{channel_id}/announcements")
async def get_channel_announcements(
    channel_id: UUID,
    skip: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=100),
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db)
):
    """
    获取频道的所有公告列表
    """
    # 检查是否是频道成员
    member_check = await db.execute(
        select(ChannelMember).where(
            ChannelMember.channel_id == channel_id,
            ChannelMember.user_id == current_user.id
        )
    )
    if not member_check.scalar_one_or_none():
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="未加入该频道"
        )

    # 获取所有公告消息
    announcements_result = await db.execute(
        select(ChannelMessage)
        .where(
            ChannelMessage.channel_id == channel_id,
            ChannelMessage.type == "announcement",
            ChannelMessage.is_deleted == False
        )
        .options(selectinload(ChannelMessage.user))
        .order_by(ChannelMessage.created_at.desc())
        .offset(skip)
        .limit(limit)
    )
    announcements = announcements_result.scalars().all()

    # 获取总数
    total_result = await db.execute(
        select(func.count(ChannelMessage.id)).where(
            ChannelMessage.channel_id == channel_id,
            ChannelMessage.type == "announcement",
            ChannelMessage.is_deleted == False
        )
    )
    total = total_result.scalar()

    # 构建响应
    announcement_list = []
    for msg in announcements:
        # 获取发送者的成员信息（用于称号）
        member_result = await db.execute(
            select(ChannelMember).where(
                ChannelMember.channel_id == channel_id,
                ChannelMember.user_id == msg.user_id
            )
        )
        member = member_result.scalar_one_or_none()

        announcement_list.append({
            "id": msg.id,
            "content": msg.content,
            "created_at": msg.created_at,
            "user_name": msg.user.username if msg.user else "已删除用户",
            "user_avatar": msg.user.avatar if msg.user else None,
            "user_title": member.custom_title if member else None,
            "user_title_color": member.title_color if member else None,
            "is_pinned": msg.is_pinned
        })

    return {
        "announcements": announcement_list,
        "total": total,
        "has_more": skip + limit < total
    }


@router.get("/{channel_id}/latest-announcement")
async def get_latest_announcement(
    channel_id: UUID,
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db)
):
    """
    获取频道最新的一条公告（用于顶部悬浮显示）
    """
    # 检查是否是频道成员
    member_check = await db.execute(
        select(ChannelMember).where(
            ChannelMember.channel_id == channel_id,
            ChannelMember.user_id == current_user.id
        )
    )
    if not member_check.scalar_one_or_none():
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="未加入该频道"
        )

    # 获取最新公告
    latest_result = await db.execute(
        select(ChannelMessage)
        .where(
            ChannelMessage.channel_id == channel_id,
            ChannelMessage.type == "announcement",
            ChannelMessage.is_deleted == False
        )
        .options(selectinload(ChannelMessage.user))
        .order_by(ChannelMessage.created_at.desc())
        .limit(1)
    )
    latest = latest_result.scalar_one_or_none()

    if not latest:
        return {"announcement": None}

    # 获取发送者的成员信息
    member_result = await db.execute(
        select(ChannelMember).where(
            ChannelMember.channel_id == channel_id,
            ChannelMember.user_id == latest.user_id
        )
    )
    member = member_result.scalar_one_or_none()

    return {
        "announcement": {
            "id": latest.id,
            "content": latest.content,
            "created_at": latest.created_at,
            "user_name": latest.user.username if latest.user else "已删除用户",
            "user_avatar": latest.user.avatar if latest.user else None,
            "user_title": member.custom_title if member else None,
            "user_title_color": member.title_color if member else None
        }
    }


# ===== 消息管理相关 API =====

@router.delete("/{channel_id}/messages/{message_id}/recall")
async def recall_message(
    channel_id: UUID,
    message_id: UUID,
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db)
):
    """
    撤回消息
    - 普通用户：只能撤回自己发送后5分钟内的消息
    - 创建者：可以撤回所有人的消息，无时间限制
    """
    # 获取频道信息,检查是否为创建者
    channel_result = await db.execute(
        select(Channel).where(Channel.id == channel_id)
    )
    channel = channel_result.scalar_one_or_none()

    if not channel:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="频道不存在"
        )

    is_creator = channel.creator_id == current_user.id

    # 获取消息
    message_result = await db.execute(
        select(ChannelMessage).where(
            ChannelMessage.id == message_id,
            ChannelMessage.channel_id == channel_id
        )
    )
    message = message_result.scalar_one_or_none()

    if not message:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="消息不存在"
        )

    # 检查是否已经被删除
    if message.is_deleted:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="消息已被删除"
        )

    # 如果不是创建者,进行普通用户的权限检查
    if not is_creator:
        # 检查是否是消息发送者
        if message.user_id != current_user.id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="只能撤回自己的消息"
            )

        # 检查是否超过5分钟
        from datetime import datetime, timedelta, timezone
        time_limit = timedelta(minutes=5)
        now = datetime.now(timezone.utc)

        if message.created_at.tzinfo is None:
            created_at = message.created_at.replace(tzinfo=timezone.utc)
        else:
            created_at = message.created_at

        if now - created_at > time_limit:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="超过撤回时限（5分钟）"
            )

    # 标记为已删除
    message.is_deleted = True
    message.deleted_at = func.now()
    message.content = "[此消息已被撤回]"

    await db.commit()

    return {"message": "消息已撤回"}


# ===== 搜索功能 API =====

@router.get("/{channel_id}/search")
async def search_messages(
    channel_id: UUID,
    keyword: str = Query(..., min_length=1, description="搜索关键词"),
    user_id: Optional[UUID] = Query(None, description="筛选发送者"),
    start_date: Optional[str] = Query(None, description="起始日期 YYYY-MM-DD"),
    end_date: Optional[str] = Query(None, description="结束日期 YYYY-MM-DD"),
    skip: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=100),
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db)
):
    """
    搜索频道内的消息
    支持按关键词、发送者、日期范围筛选
    """
    # 检查是否是频道成员
    member_check = await db.execute(
        select(ChannelMember).where(
            ChannelMember.channel_id == channel_id,
            ChannelMember.user_id == current_user.id
        )
    )
    if not member_check.scalar_one_or_none():
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="未加入该频道"
        )

    # 构建查询条件
    conditions = [
        ChannelMessage.channel_id == channel_id,
        ChannelMessage.is_deleted == False,
        ChannelMessage.content.contains(keyword)
    ]

    if user_id:
        conditions.append(ChannelMessage.user_id == user_id)

    if start_date:
        from datetime import datetime
        start_dt = datetime.fromisoformat(start_date)
        conditions.append(ChannelMessage.created_at >= start_dt)

    if end_date:
        from datetime import datetime, timedelta
        end_dt = datetime.fromisoformat(end_date) + timedelta(days=1)
        conditions.append(ChannelMessage.created_at < end_dt)

    # 执行搜索
    search_result = await db.execute(
        select(ChannelMessage)
        .where(and_(*conditions))
        .options(selectinload(ChannelMessage.user))
        .order_by(ChannelMessage.created_at.desc())
        .offset(skip)
        .limit(limit)
    )
    messages = search_result.scalars().all()

    # 获取总数
    total_result = await db.execute(
        select(func.count(ChannelMessage.id)).where(and_(*conditions))
    )
    total = total_result.scalar()

    # 构建响应
    message_list = []
    for msg in messages:
        member_result = await db.execute(
            select(ChannelMember).where(
                ChannelMember.channel_id == channel_id,
                ChannelMember.user_id == msg.user_id
            )
        )
        member = member_result.scalar_one_or_none()

        message_list.append({
            "id": msg.id,
            "content": msg.content,
            "type": msg.type,
            "created_at": msg.created_at,
            "user_id": msg.user_id,
            "user_name": msg.user.username if msg.user else "已删除用户",
            "user_avatar": msg.user.avatar if msg.user else None,
            "user_title": member.custom_title if member else None,
            "user_title_color": member.title_color if member else None
        })

    return {
        "messages": message_list,
        "total": total,
        "has_more": skip + limit < total
    }


# ===== 频道设置相关 API =====

@router.put("/{channel_id}/settings")
async def update_channel_settings(
    channel_id: UUID,
    name: Optional[str] = Query(None, min_length=1, max_length=50),
    description: Optional[str] = Query(None, max_length=500),
    cover_image: Optional[str] = Query(None),
    slow_mode_seconds: Optional[int] = Query(None, ge=0, le=300, description="慢速模式间隔(秒)"),
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db)
):
    """
    更新频道设置（仅创建者）
    """
    # 获取频道
    channel_result = await db.execute(
        select(Channel).where(Channel.id == channel_id)
    )
    channel = channel_result.scalar_one_or_none()

    if not channel:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="频道不存在"
        )

    # 检查是否是创建者
    if channel.creator_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="只有创建者可以修改频道设置"
        )

    # 更新设置
    if name is not None:
        channel.name = name
    if description is not None:
        channel.description = description
    if cover_image is not None:
        channel.cover_image = cover_image

    await db.commit()
    await db.refresh(channel)

    return {"message": "频道设置已更新", "channel": build_channel_response(channel)}


# ===== 成员权限管理相关 API =====

@router.post("/{channel_id}/members/{user_id}/mute")
async def mute_member(
    channel_id: UUID,
    user_id: UUID,
    duration_minutes: int = Query(..., ge=1, le=43200, description="禁言时长(分钟)"),
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db)
):
    """
    禁言成员（仅创建者）
    """
    # 检查操作者权限
    operator_member = await db.execute(
        select(ChannelMember).where(
            ChannelMember.channel_id == channel_id,
            ChannelMember.user_id == current_user.id
        )
    )
    operator = operator_member.scalar_one_or_none()

    if not operator or operator.role != 'owner':
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="只有创建者可以禁言成员"
        )

    # 获取目标成员
    target_member_result = await db.execute(
        select(ChannelMember).where(
            ChannelMember.channel_id == channel_id,
            ChannelMember.user_id == user_id
        )
    )
    target_member = target_member_result.scalar_one_or_none()

    if not target_member:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="成员不存在"
        )

    # 不能禁言创建者
    if target_member.role == 'owner':
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="不能禁言创建者"
        )

    # 设置禁言
    from datetime import datetime, timedelta, timezone
    target_member.is_muted = True
    target_member.muted_until = datetime.now(timezone.utc) + timedelta(minutes=duration_minutes)

    await db.commit()

    return {
        "message": "成员已被禁言",
        "muteUntil": target_member.muted_until.isoformat() if target_member.muted_until else None
    }


@router.post("/{channel_id}/members/{user_id}/unmute")
async def unmute_member(
    channel_id: UUID,
    user_id: UUID,
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db)
):
    """
    取消禁言（仅创建者）
    """
    # 检查操作者权限
    operator_member = await db.execute(
        select(ChannelMember).where(
            ChannelMember.channel_id == channel_id,
            ChannelMember.user_id == current_user.id
        )
    )
    operator = operator_member.scalar_one_or_none()

    if not operator or operator.role != 'owner':
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="只有创建者可以取消禁言"
        )

    # 获取目标成员
    target_member_result = await db.execute(
        select(ChannelMember).where(
            ChannelMember.channel_id == channel_id,
            ChannelMember.user_id == user_id
        )
    )
    target_member = target_member_result.scalar_one_or_none()

    if not target_member:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="成员不存在"
        )

    # 取消禁言
    target_member.is_muted = False
    target_member.muted_until = None

    await db.commit()

    return {"message": "已取消禁言"}


@router.patch("/{channel_id}/members/{user_id}/title")
async def update_member_title(
    channel_id: UUID,
    user_id: UUID,
    title_data: dict,
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db)
):
    """
    修改成员称号（仅创建者）

    参数:
    - custom_title: 自定义称号（可选，最多50字符，null表示清除）
    - title_color: 称号颜色（可选，hex格式如#FF6B6B）
    """
    # 检查操作者权限
    operator_member = await db.execute(
        select(ChannelMember).where(
            ChannelMember.channel_id == channel_id,
            ChannelMember.user_id == current_user.id
        )
    )
    operator = operator_member.scalar_one_or_none()

    if not operator or operator.role != 'owner':
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="只有创建者可以修改成员称号"
        )

    # 获取目标成员
    target_member_result = await db.execute(
        select(ChannelMember).where(
            ChannelMember.channel_id == channel_id,
            ChannelMember.user_id == user_id
        )
    )
    target_member = target_member_result.scalar_one_or_none()

    if not target_member:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="成员不存在"
        )

    # 更新称号信息
    if 'custom_title' in title_data:
        custom_title = title_data['custom_title']
        if custom_title is not None and len(custom_title) > 50:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="称号长度不能超过50个字符"
            )
        target_member.custom_title = custom_title

    if 'title_color' in title_data:
        target_member.title_color = title_data['title_color']

    await db.commit()
    await db.refresh(target_member)

    return {
        "message": "称号已更新",
        "custom_title": target_member.custom_title,
        "title_color": target_member.title_color
    }


@router.post("/fix-fangroup-permanent")
async def fix_fangroup_permanent(
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db)
):
    """
    临时修复端点：将所有粉丝群设置为非永久状态
    仅管理员可用
    """
    if not current_user.is_admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="需要管理员权限"
        )

    # 更新所有粉丝群
    result = await db.execute(
        select(Channel).where(Channel.type == 'fangroup')
    )
    fangroups = result.scalars().all()

    count = 0
    for channel in fangroups:
        if channel.is_permanent:
            channel.is_permanent = False
            count += 1

    await db.commit()

    return {
        "message": f"成功修复 {count} 个粉丝群",
        "total_fangroups": len(fangroups),
        "updated": count
    }

